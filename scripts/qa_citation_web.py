#!/usr/bin/env python3
"""Web-backed QA for citation existence and context-intent alignment."""

from __future__ import annotations

import argparse
import html
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

CITATION_GROUP_RE = re.compile(r"\[[^\]]*?@[^\]]*?\]")
CITEKEY_RE = re.compile(r"@([A-Za-z0-9_:.+/-]+)")
ENTRY_START_RE = re.compile(r"^\s*@", re.MULTILINE)
ENTRY_HEADER_RE = re.compile(r"@\s*(\w+)\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)

CORE_SECTION_FILES = {"02_introduction.md", "05_discussion.md"}
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}|[一-龯ぁ-んァ-ンー]{2,}")
JATS_TAG_RE = re.compile(r"<[^>]+>")
MULTISPACE_RE = re.compile(r"\s+")

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "were",
    "was",
    "are",
    "have",
    "has",
    "had",
    "into",
    "onto",
    "over",
    "under",
    "than",
    "then",
    "while",
    "within",
    "between",
    "among",
    "using",
    "used",
    "use",
    "our",
    "their",
    "there",
    "these",
    "those",
    "which",
    "whose",
    "also",
    "however",
    "therefore",
    "result",
    "results",
    "study",
    "studies",
    "analysis",
    "data",
    "patient",
    "patients",
    "group",
    "groups",
    "method",
    "methods",
    "background",
    "discussion",
    "introduction",
    "conclusion",
    "table",
    "tables",
    "figure",
    "figures",
    "et",
    "al",
}

INCREASE_TERMS = (
    "increase",
    "increased",
    "higher",
    "elevated",
    "greater",
    "improved",
    "improvement",
    "upregulated",
    "upregulation",
    "増加",
    "上昇",
    "改善",
)
DECREASE_TERMS = (
    "decrease",
    "decreased",
    "lower",
    "reduced",
    "reduction",
    "decline",
    "downregulated",
    "downregulation",
    "減少",
    "低下",
)
NULL_TERMS = (
    "no association",
    "not associated",
    "no significant",
    "non-significant",
    "not significant",
    "null finding",
    "関連なし",
    "有意差なし",
    "差はなかった",
    "認めなかった",
)


@dataclass
class BibEntry:
    key: str
    entry_type: str
    title: str
    author: str
    journal: str
    year: str
    doi: str
    pmid: str


@dataclass
class CitationOccurrence:
    key: str
    file: str
    line: int
    context: str


@dataclass
class WebRecord:
    found: bool
    source: str
    identifier: str
    title: str
    abstract: str
    journal: str
    year: str
    doi: str
    pmid: str
    url: str
    note: str
    network_error: bool


@dataclass
class IntentResult:
    overlap: float
    context_keywords: int
    matched_keywords: int
    direction_conflict: bool
    critical_mismatch: bool
    low_overlap_warning: bool
    note: str


def parse_entries(text: str) -> list[tuple[int, int, str, str]]:
    starts = [m.start() for m in ENTRY_START_RE.finditer(text)]
    out: list[tuple[int, int, str, str]] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        raw = text[start:end]
        m = ENTRY_HEADER_RE.search(raw)
        if not m:
            continue
        out.append((start, end, m.group(1).strip().lower(), m.group(2).strip()))
    return out


def get_field(entry_text: str, field: str) -> str:
    brace = re.compile(rf"\b{re.escape(field)}\s*=\s*\{{(.*?)\}}", re.IGNORECASE | re.DOTALL)
    quote = re.compile(rf"\b{re.escape(field)}\s*=\s*\"(.*?)\"", re.IGNORECASE | re.DOTALL)
    m = brace.search(entry_text) or quote.search(entry_text)
    if not m:
        return ""
    return MULTISPACE_RE.sub(" ", m.group(1).strip())


def parse_bib(path: Path) -> dict[str, BibEntry]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    index: dict[str, BibEntry] = {}
    for start, end, entry_type, key in parse_entries(text):
        raw = text[start:end]
        entry = BibEntry(
            key=key,
            entry_type=entry_type,
            title=get_field(raw, "title"),
            author=get_field(raw, "author"),
            journal=get_field(raw, "journal") or get_field(raw, "journaltitle"),
            year=get_field(raw, "year"),
            doi=normalize_doi(get_field(raw, "doi")),
            pmid=get_field(raw, "pmid"),
        )
        index[key] = entry
    return index


def normalize_doi(value: str) -> str:
    v = value.strip()
    v = re.sub(r"^https?://(dx\.)?doi\.org/", "", v, flags=re.IGNORECASE)
    v = re.sub(r"^doi:\s*", "", v, flags=re.IGNORECASE)
    return v.strip()


def iter_section_files(root: Path, scope: str) -> list[Path]:
    if not root.exists():
        return []
    files = [p for p in sorted(root.glob("*.md")) if p.is_file()]
    if scope == "all":
        return files
    return [p for p in files if p.name in CORE_SECTION_FILES]


def strip_markdown(text: str) -> str:
    x = re.sub(r"\[[^\]]*?@[^\]]*?\]", " ", text)
    x = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", x)
    x = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", x)
    x = re.sub(r"`{1,3}[^`]+`{1,3}", " ", x)
    x = re.sub(r"[#>*_~\-]{1,3}", " ", x)
    return MULTISPACE_RE.sub(" ", x).strip()


def extract_context(text: str, start: int, end: int) -> str:
    left = text.rfind("\n\n", 0, start)
    right = text.find("\n\n", end)
    if left == -1:
        left = 0
    else:
        left += 2
    if right == -1:
        right = len(text)
    chunk = text[left:right]
    clean = strip_markdown(chunk)
    return clean[:700]


def collect_occurrences(sections_dir: Path, scope: str) -> list[CitationOccurrence]:
    occurrences: list[CitationOccurrence] = []
    for path in iter_section_files(sections_dir, scope):
        text = path.read_text(encoding="utf-8")
        for m in CITATION_GROUP_RE.finditer(text):
            group = m.group(0)
            keys = CITEKEY_RE.findall(group)
            if not keys:
                continue
            line = text.count("\n", 0, m.start()) + 1
            context = extract_context(text, m.start(), m.end())
            for key in keys:
                occurrences.append(
                    CitationOccurrence(
                        key=key,
                        file=str(path),
                        line=line,
                        context=context,
                    )
                )
    return occurrences


def load_cache(path: Path) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(path: Path, cache: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def http_get_json(url: str, timeout: int) -> tuple[dict[str, object] | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": "citation-qa/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        return json.loads(data), None
    except urllib.error.HTTPError as exc:
        return None, f"http_{exc.code}"
    except urllib.error.URLError as exc:
        return None, f"urlerror:{exc.reason}"
    except TimeoutError:
        return None, "timeout"
    except Exception as exc:  # pragma: no cover
        return None, f"error:{type(exc).__name__}"


def http_get_text(url: str, timeout: int) -> tuple[str | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": "citation-qa/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as exc:
        return None, f"http_{exc.code}"
    except urllib.error.URLError as exc:
        return None, f"urlerror:{exc.reason}"
    except TimeoutError:
        return None, "timeout"
    except Exception as exc:  # pragma: no cover
        return None, f"error:{type(exc).__name__}"


def get_text_tree(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def fetch_pubmed_record(pmid: str, timeout: int) -> WebRecord:
    efetch = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={urllib.parse.quote(pmid)}&retmode=xml"
    )
    xml_text, err = http_get_text(efetch, timeout)
    if err:
        return WebRecord(
            found=False,
            source="pubmed",
            identifier=pmid,
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid=pmid,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            note=f"pubmed_fetch_failed:{err}",
            network_error=True,
        )
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return WebRecord(
            found=False,
            source="pubmed",
            identifier=pmid,
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid=pmid,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            note="pubmed_parse_failed",
            network_error=False,
        )

    article = root.find(".//PubmedArticle")
    if article is None:
        return WebRecord(
            found=False,
            source="pubmed",
            identifier=pmid,
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid=pmid,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            note="pubmed_not_found",
            network_error=False,
        )

    title = get_text_tree(article.find(".//ArticleTitle"))
    abstract_parts = [get_text_tree(x) for x in article.findall(".//Abstract/AbstractText")]
    abstract = MULTISPACE_RE.sub(" ", " ".join([x for x in abstract_parts if x])).strip()
    journal = get_text_tree(article.find(".//Journal/Title")) or get_text_tree(
        article.find(".//Journal/ISOAbbreviation")
    )
    year = get_text_tree(article.find(".//PubDate/Year"))
    if not year:
        medline_date = get_text_tree(article.find(".//PubDate/MedlineDate"))
        m = re.search(r"\b(19|20)\d{2}\b", medline_date)
        year = m.group(0) if m else ""
    doi = ""
    for aid in article.findall(".//ArticleIdList/ArticleId"):
        if aid.attrib.get("IdType", "").lower() == "doi":
            doi = normalize_doi((aid.text or "").strip())
            break

    return WebRecord(
        found=bool(title or abstract),
        source="pubmed",
        identifier=pmid,
        title=title,
        abstract=abstract,
        journal=journal,
        year=year,
        doi=doi,
        pmid=pmid,
        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        note="ok" if (title or abstract) else "empty_record",
        network_error=False,
    )


def clean_crossref_abstract(value: str) -> str:
    if not value:
        return ""
    x = html.unescape(value)
    x = JATS_TAG_RE.sub(" ", x)
    return MULTISPACE_RE.sub(" ", x).strip()


def fetch_crossref_by_doi(doi: str, timeout: int) -> WebRecord:
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    data, err = http_get_json(url, timeout)
    if err:
        return WebRecord(
            found=False,
            source="crossref",
            identifier=doi,
            title="",
            abstract="",
            journal="",
            year="",
            doi=doi,
            pmid="",
            url=f"https://doi.org/{doi}",
            note=f"crossref_fetch_failed:{err}",
            network_error=True,
        )
    msg = (data or {}).get("message", {})
    title_list = msg.get("title", [])
    title = title_list[0] if title_list else ""
    journal_list = msg.get("container-title", [])
    journal = journal_list[0] if journal_list else ""
    year = ""
    for key in ("published-print", "published-online", "issued"):
        parts = ((msg.get(key) or {}).get("date-parts") or [[]])[0]
        if parts:
            year = str(parts[0])
            break
    abstract = clean_crossref_abstract(msg.get("abstract", ""))
    return WebRecord(
        found=bool(title or abstract),
        source="crossref",
        identifier=doi,
        title=title,
        abstract=abstract,
        journal=journal,
        year=year,
        doi=normalize_doi(msg.get("DOI", doi) or doi),
        pmid="",
        url=f"https://doi.org/{doi}",
        note="ok" if (title or abstract) else "empty_record",
        network_error=False,
    )


def fetch_crossref_by_title(title: str, timeout: int) -> WebRecord:
    query = urllib.parse.quote(title)
    url = f"https://api.crossref.org/works?query.title={query}&rows=1"
    data, err = http_get_json(url, timeout)
    if err:
        return WebRecord(
            found=False,
            source="crossref-title",
            identifier=title[:120],
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid="",
            url="",
            note=f"crossref_title_fetch_failed:{err}",
            network_error=True,
        )
    items = (((data or {}).get("message") or {}).get("items") or [])
    if not items:
        return WebRecord(
            found=False,
            source="crossref-title",
            identifier=title[:120],
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid="",
            url="",
            note="title_not_found",
            network_error=False,
        )
    item = items[0]
    title_list = item.get("title", [])
    result_title = title_list[0] if title_list else ""
    abstract = clean_crossref_abstract(item.get("abstract", ""))
    journal_list = item.get("container-title", [])
    journal = journal_list[0] if journal_list else ""
    year = ""
    for key in ("published-print", "published-online", "issued"):
        parts = ((item.get(key) or {}).get("date-parts") or [[]])[0]
        if parts:
            year = str(parts[0])
            break
    doi = normalize_doi(item.get("DOI", ""))
    return WebRecord(
        found=bool(result_title),
        source="crossref-title",
        identifier=title[:120],
        title=result_title,
        abstract=abstract,
        journal=journal,
        year=year,
        doi=doi,
        pmid="",
        url=f"https://doi.org/{doi}" if doi else "",
        note="ok" if result_title else "title_not_found",
        network_error=False,
    )


def detect_direction(text: str) -> set[str]:
    low = text.lower()
    flags: set[str] = set()
    for token in NULL_TERMS:
        if token in low:
            flags.add("null")
            break
    for token in INCREASE_TERMS:
        if token in low:
            flags.add("increase")
            break
    for token in DECREASE_TERMS:
        if token in low:
            flags.add("decrease")
            break
    return flags


def tokenize(text: str) -> list[str]:
    tokens = [t.lower() for t in TOKEN_RE.findall(text)]
    out: list[str] = []
    for token in tokens:
        if token in STOPWORDS:
            continue
        if token.isdigit():
            continue
        out.append(token)
    return out


def evaluate_intent(
    context: str,
    record: WebRecord,
    overlap_threshold: float,
    critical_overlap: float,
) -> IntentResult:
    source_text = f"{record.title} {record.abstract}".strip()
    context_tokens = sorted(set(tokenize(context)))
    source_tokens = set(tokenize(source_text))
    if not context_tokens:
        return IntentResult(
            overlap=1.0,
            context_keywords=0,
            matched_keywords=0,
            direction_conflict=False,
            critical_mismatch=False,
            low_overlap_warning=False,
            note="context_keywords_empty",
        )
    matched = sum(1 for t in context_tokens if t in source_tokens)
    overlap = matched / max(len(context_tokens), 1)

    ctx_dir = detect_direction(context)
    src_dir = detect_direction(source_text)
    direction_conflict = False
    if "null" in ctx_dir and "null" not in src_dir and ({"increase", "decrease"} & src_dir):
        direction_conflict = True
    if ctx_dir == {"increase"} and "decrease" in src_dir and "increase" not in src_dir:
        direction_conflict = True
    if ctx_dir == {"decrease"} and "increase" in src_dir and "decrease" not in src_dir:
        direction_conflict = True

    critical = len(context_tokens) >= 6 and overlap < critical_overlap
    low = len(context_tokens) >= 4 and overlap < overlap_threshold

    note = "ok"
    if direction_conflict:
        note = "direction_conflict"
    elif critical:
        note = "critical_low_overlap"
    elif low:
        note = "low_overlap_warning"

    return IntentResult(
        overlap=overlap,
        context_keywords=len(context_tokens),
        matched_keywords=matched,
        direction_conflict=direction_conflict,
        critical_mismatch=critical,
        low_overlap_warning=low,
        note=note,
    )


def resolve_web_record(
    entry: BibEntry,
    cache: dict[str, dict[str, object]],
    timeout: int,
) -> WebRecord:
    cache_key = ""
    if entry.pmid:
        cache_key = f"pmid:{entry.pmid}"
    elif entry.doi:
        cache_key = f"doi:{entry.doi.lower()}"
    elif entry.title:
        cache_key = f"title:{entry.title[:180].lower()}"

    if cache_key and cache_key in cache:
        c = cache[cache_key]
        return WebRecord(**c)

    if entry.pmid:
        rec = fetch_pubmed_record(entry.pmid, timeout)
    elif entry.doi:
        rec = fetch_crossref_by_doi(entry.doi, timeout)
    elif entry.title:
        rec = fetch_crossref_by_title(entry.title, timeout)
    else:
        rec = WebRecord(
            found=False,
            source="none",
            identifier=entry.key,
            title="",
            abstract="",
            journal="",
            year="",
            doi="",
            pmid="",
            url="",
            note="missing_identifiers",
            network_error=False,
        )

    if cache_key and rec.found and not rec.network_error:
        cache[cache_key] = asdict(rec)
    return rec


def build_report(
    report_path: Path,
    scope: str,
    total_occurrences: int,
    cited_keys: list[str],
    errors: list[str],
    warnings: list[str],
    details: list[str],
    status: str,
) -> None:
    lines = [
        "# QA: citation web verification report",
        f"Status: {status}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        f"- scope: {scope}",
        f"- citation occurrences scanned: {total_occurrences}",
        f"- unique citekeys scanned: {len(cited_keys)}",
        f"- errors: {len(errors)}",
        f"- warnings: {len(warnings)}",
    ]
    if errors:
        lines.extend(["", "## Errors"])
        lines.extend([f"- {x}" for x in errors])
    if warnings:
        lines.extend(["", "## Warnings"])
        lines.extend([f"- {x}" for x in warnings])
    if details:
        lines.extend(["", "## Per-citekey checks"])
        lines.extend(details)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Web-backed QA for citation existence and context-intent alignment."
    )
    parser.add_argument("--paper-dir", default=".", help="Paper workspace root")
    parser.add_argument("--sections-dir", default="sections", help="Sections directory from paper-dir")
    parser.add_argument("--bib", default="refs/references.bib", help="Bib file path from paper-dir")
    parser.add_argument(
        "--report",
        default="reports/qa_citation_web.md",
        help="Report output path from paper-dir",
    )
    parser.add_argument(
        "--cache",
        default="data/search/web_verify_cache.json",
        help="Web fetch cache path from paper-dir",
    )
    parser.add_argument(
        "--scope",
        choices=["all", "core"],
        default="all",
        help="all=all sections, core=Introduction+Discussion only",
    )
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout seconds")
    parser.add_argument(
        "--overlap-threshold",
        type=float,
        default=0.12,
        help="Low-overlap warning threshold",
    )
    parser.add_argument(
        "--critical-overlap",
        type=float,
        default=0.06,
        help="Critical mismatch threshold",
    )
    parser.add_argument(
        "--allow-network-fail",
        action="store_true",
        help="Treat network fetch failures as warnings (not errors).",
    )
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    sections_dir = (paper_dir / args.sections_dir).resolve()
    bib_path = (paper_dir / args.bib).resolve()
    report_path = (paper_dir / args.report).resolve()
    cache_path = (paper_dir / args.cache).resolve()

    errors: list[str] = []
    warnings: list[str] = []
    details: list[str] = []

    if not sections_dir.exists():
        errors.append(f"Sections directory not found: {sections_dir}")
        build_report(report_path, args.scope, 0, [], errors, warnings, details, "FAIL")
        print(f"QA citation-web: FAIL (sections missing) -> {report_path}")
        return 1
    if not bib_path.exists():
        errors.append(f"BibTeX file not found: {bib_path}")
        build_report(report_path, args.scope, 0, [], errors, warnings, details, "FAIL")
        print(f"QA citation-web: FAIL (bib missing) -> {report_path}")
        return 1

    bib = parse_bib(bib_path)
    occ = collect_occurrences(sections_dir, args.scope)
    if not occ:
        build_report(report_path, args.scope, 0, [], errors, warnings, details, "PASS")
        print(f"QA citation-web: PASS (no citations in scope={args.scope})")
        print(f"Report: {report_path}")
        return 0

    cache = load_cache(cache_path)
    grouped: dict[str, list[CitationOccurrence]] = {}
    for o in occ:
        grouped.setdefault(o.key, []).append(o)

    for key, uses in sorted(grouped.items()):
        if key not in bib:
            errors.append(f"{key}: cited in manuscript but missing in refs/references.bib")
            continue
        entry = bib[key]
        rec = resolve_web_record(entry, cache, args.timeout)

        if rec.network_error and not args.allow_network_fail:
            errors.append(f"{key}: web lookup failed ({rec.note})")
            details.append(f"- **{key}**: lookup=FAIL, reason={rec.note}")
            continue
        if rec.network_error and args.allow_network_fail:
            warnings.append(f"{key}: web lookup failed but allowed ({rec.note})")
            details.append(f"- **{key}**: lookup=WARN, reason={rec.note}")
            continue
        if not rec.found:
            errors.append(f"{key}: citation could not be confirmed on web ({rec.note})")
            details.append(f"- **{key}**: lookup=FAIL, reason={rec.note}")
            continue

        per_key_warn = 0
        per_key_err = 0
        max_overlap = 0.0
        for u in uses:
            intent = evaluate_intent(
                context=u.context,
                record=rec,
                overlap_threshold=args.overlap_threshold,
                critical_overlap=args.critical_overlap,
            )
            max_overlap = max(max_overlap, intent.overlap)
            if intent.direction_conflict:
                per_key_err += 1
                errors.append(
                    f"{key}: possible direction conflict at {u.file}:{u.line} "
                    f"(context vs {rec.source})"
                )
            elif intent.critical_mismatch:
                per_key_err += 1
                errors.append(
                    f"{key}: critical low overlap at {u.file}:{u.line} "
                    f"(overlap={intent.overlap:.2f})"
                )
            elif intent.low_overlap_warning:
                per_key_warn += 1
                warnings.append(
                    f"{key}: low overlap warning at {u.file}:{u.line} "
                    f"(overlap={intent.overlap:.2f})"
                )

        details.append(
            f"- **{key}**: lookup=OK ({rec.source}:{rec.identifier}), uses={len(uses)}, "
            f"errors={per_key_err}, warnings={per_key_warn}, max_overlap={max_overlap:.2f}"
        )

    save_cache(cache_path, cache)

    status = "PASS" if not errors else "FAIL"
    build_report(
        report_path=report_path,
        scope=args.scope,
        total_occurrences=len(occ),
        cited_keys=sorted(grouped.keys()),
        errors=errors,
        warnings=warnings,
        details=details,
        status=status,
    )

    print(
        f"QA citation-web: {status} "
        f"(keys={len(grouped)}, errors={len(errors)}, warnings={len(warnings)})"
    )
    print(f"Report: {report_path}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""QA for references.bib completeness/integrity and CSL suitability before Pandoc build."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ENTRY_START_RE = re.compile(r"^\s*@", re.MULTILINE)
ENTRY_HEADER_RE = re.compile(r"@\s*(\w+)\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
UNRESOLVED_TOKEN_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b|未定|未入力|要確認", re.IGNORECASE)
DOI_CANON_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
YEAR_RE = re.compile(r"^\d{4}$")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)

REQ_CSL_LINE_RE = re.compile(r"Citation Style \(CSL\)\s*:\s*`?([^`\n]+\.csl)`?", re.IGNORECASE)
REQ_TARGET_JOURNAL_RE = re.compile(r"Target Journal\s*\*\*?:\s*(.+)$", re.IGNORECASE)
REQ_TARGET_JOURNAL_JA_RE = re.compile(r"対象誌\s*[:：]\s*(.+)$", re.IGNORECASE)
PANDOC_CSL_RE = re.compile(r"^\s*csl\s*:\s*(.+?)\s*$")

REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "book": ["title", "year", "publisher"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
}

STYLE_HINTS = {
    "vancouver": "numeric",
    "ama": "numeric",
    "nature": "numeric",
    "ieee": "numeric",
    "apa": "author-date",
    "harvard": "author-date",
    "chicago-author-date": "author-date",
}


@dataclass
class BibEntry:
    entry_type: str
    key: str
    start: int
    end: int
    raw: str


@dataclass
class CslInfo:
    path: Path
    title: str
    style_id: str
    citation_format: str


def parse_entries(text: str) -> list[BibEntry]:
    starts = [m.start() for m in ENTRY_START_RE.finditer(text)]
    entries: list[BibEntry] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        raw = text[start:end]
        m = ENTRY_HEADER_RE.search(raw)
        if not m:
            continue
        entries.append(
            BibEntry(
                entry_type=m.group(1).lower().strip(),
                key=m.group(2).strip(),
                start=start,
                end=end,
                raw=raw,
            )
        )
    return entries


def get_field(entry_text: str, field: str) -> str:
    brace_pat = re.compile(rf"\\b{re.escape(field)}\\s*=\\s*\\{{(.*?)\\}}", re.IGNORECASE | re.DOTALL)
    quote_pat = re.compile(rf"\\b{re.escape(field)}\\s*=\\s*\"(.*?)\"", re.IGNORECASE | re.DOTALL)

    m = brace_pat.search(entry_text)
    if m:
        return " ".join(m.group(1).strip().split())
    m = quote_pat.search(entry_text)
    if m:
        return " ".join(m.group(1).strip().split())
    return ""


def replace_field(entry_text: str, field: str, value: str) -> tuple[str, bool]:
    for pattern in (
        re.compile(rf"(\\b{re.escape(field)}\\s*=\\s*\\{{)(.*?)(\\}})", re.IGNORECASE | re.DOTALL),
        re.compile(rf"(\\b{re.escape(field)}\\s*=\\s*\")(.*?)(\")", re.IGNORECASE | re.DOTALL),
    ):
        m = pattern.search(entry_text)
        if m:
            new_text = entry_text[: m.start(2)] + value + entry_text[m.end(2) :]
            return new_text, True
    return entry_text, False


def add_field(entry_text: str, field: str, value: str) -> str:
    closing = entry_text.rfind("}")
    if closing == -1:
        return entry_text
    head = entry_text[:closing].rstrip()
    tail = entry_text[closing:]
    if not head.endswith(","):
        head += ","
    insertion = f"\n  {field} = {{{value}}}\n"
    return head + insertion + tail.lstrip("\n")


def normalize_doi(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"^https?://(dx\.)?doi\.org/", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^doi:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace(" ", "")
    return cleaned


def extract_year_from_date(date_value: str) -> str:
    m = re.match(r"\s*(\d{4})", date_value)
    return m.group(1) if m else ""


def rebuild_bib_text(original: str, replacements: list[tuple[int, int, str]]) -> str:
    if not replacements:
        return original
    chunks: list[str] = []
    cursor = 0
    for start, end, replacement in sorted(replacements, key=lambda x: x[0]):
        chunks.append(original[cursor:start])
        chunks.append(replacement)
        cursor = end
    chunks.append(original[cursor:])
    return "".join(chunks)


def infer_expected_csl(requirements_text: str, pandoc_csl: str) -> str:
    m = REQ_CSL_LINE_RE.search(requirements_text)
    if m:
        return Path(m.group(1).strip().strip('"\'')).name
    return Path(pandoc_csl).name if pandoc_csl else ""


def extract_target_journal(requirements_text: str) -> str:
    for raw in requirements_text.splitlines():
        line = raw.strip(" -")
        m = REQ_TARGET_JOURNAL_RE.search(line)
        if m:
            return m.group(1).strip()
        m = REQ_TARGET_JOURNAL_JA_RE.search(line)
        if m:
            return m.group(1).strip()
    return ""


def parse_pandoc_csl(pandoc_text: str) -> str:
    for raw in pandoc_text.splitlines():
        m = PANDOC_CSL_RE.match(raw)
        if not m:
            continue
        return m.group(1).strip().strip('"\'')
    return ""


def set_pandoc_csl(pandoc_text: str, new_csl: str) -> tuple[str, bool]:
    lines = pandoc_text.splitlines()
    changed = False
    for i, raw in enumerate(lines):
        if PANDOC_CSL_RE.match(raw):
            lines[i] = f"csl: {new_csl}"
            changed = True
            break
    if not changed:
        lines.append(f"csl: {new_csl}")
        changed = True
    return "\n".join(lines) + ("\n" if pandoc_text.endswith("\n") else ""), changed


def parse_csl_info(path: Path) -> CslInfo:
    tree = ET.parse(path)
    root = tree.getroot()

    ns = {"c": "http://purl.org/net/xbiblio/csl"}
    title = root.findtext("c:info/c:title", default="", namespaces=ns).strip()
    style_id = root.findtext("c:info/c:id", default="", namespaces=ns).strip()
    citation_format = root.attrib.get("citation-format", "").strip()

    return CslInfo(path=path, title=title, style_id=style_id, citation_format=citation_format)


def style_hint_from_name(name: str) -> str:
    lowered = name.lower()
    for token, hint in STYLE_HINTS.items():
        if token in lowered:
            return hint
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="QA references.bib and CSL compatibility before Pandoc build")
    parser.add_argument("--paper-dir", default=".", help="Paper workspace root")
    parser.add_argument("--bib", default="refs/references.bib", help="BibTeX path from paper-dir")
    parser.add_argument("--pandoc", default="pandoc.yaml", help="Pandoc defaults file from paper-dir")
    parser.add_argument("--requirements", default="design/01_requirements.md", help="Requirements path from paper-dir")
    parser.add_argument("--report", default="reports/qa_references_style.md", help="Report output path from paper-dir")
    parser.add_argument("--fix", action="store_true", help="Attempt safe auto-fixes")
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    bib_path = (paper_dir / args.bib).resolve()
    pandoc_path = (paper_dir / args.pandoc).resolve()
    req_path = (paper_dir / args.requirements).resolve()
    report_path = (paper_dir / args.report).resolve()

    errors: list[str] = []
    warnings: list[str] = []
    user_actions: list[str] = []
    fixes: list[str] = []

    if not bib_path.exists():
        errors.append(f"BibTeX file not found: {bib_path}")
        bib_text = ""
        entries: list[BibEntry] = []
    else:
        bib_text = bib_path.read_text(encoding="utf-8")
        entries = parse_entries(bib_text)
        if not entries:
            warnings.append("No parsable BibTeX entries found (refs may still be empty at drafting stage)")

    replacements: list[tuple[int, int, str]] = []

    key_counts = Counter(entry.key for entry in entries)
    for key, count in sorted(key_counts.items()):
        if count > 1:
            errors.append(f"Duplicate citekey: {key} ({count})")

    doi_to_keys: dict[str, list[str]] = {}
    title_year_to_keys: dict[str, list[str]] = {}

    for entry in entries:
        text = entry.raw
        changed = False

        if UNRESOLVED_TOKEN_RE.search(text):
            errors.append(f"{entry.key}: contains unresolved placeholders (TBD/TODO)")

        fields = {
            "title": get_field(text, "title"),
            "author": get_field(text, "author"),
            "editor": get_field(text, "editor"),
            "journal": get_field(text, "journal"),
            "journaltitle": get_field(text, "journaltitle"),
            "booktitle": get_field(text, "booktitle"),
            "publisher": get_field(text, "publisher"),
            "school": get_field(text, "school"),
            "year": get_field(text, "year"),
            "date": get_field(text, "date"),
            "doi": get_field(text, "doi"),
            "url": get_field(text, "url"),
            "pmid": get_field(text, "pmid"),
        }

        required = REQUIRED_FIELDS.get(entry.entry_type, ["title", "year"])
        for field in required:
            if field == "author":
                if not fields["author"] and not fields["editor"]:
                    errors.append(f"{entry.key}: missing required field author/editor")
                continue
            if not fields.get(field, ""):
                if field == "journal" and fields["journaltitle"] and args.fix:
                    text = add_field(text, "journal", fields["journaltitle"])
                    fields["journal"] = fields["journaltitle"]
                    fixes.append(f"{entry.key}: added journal from journaltitle")
                    changed = True
                else:
                    errors.append(f"{entry.key}: missing required field {field}")

        if fields["year"] and not YEAR_RE.match(fields["year"]):
            errors.append(f"{entry.key}: invalid year value '{fields['year']}'")
        elif fields["year"]:
            year_num = int(fields["year"])
            current_year = datetime.now().year
            if year_num < 1900 or year_num > current_year + 1:
                errors.append(f"{entry.key}: year out of range '{fields['year']}'")

        if not fields["year"] and fields["date"]:
            y = extract_year_from_date(fields["date"])
            if y and args.fix:
                text = add_field(text, "year", y)
                fields["year"] = y
                fixes.append(f"{entry.key}: added year={y} from date")
                changed = True
            elif y:
                warnings.append(f"{entry.key}: year missing but date has {y} (fixable)")

        if fields["doi"]:
            normalized = normalize_doi(fields["doi"])
            if normalized != fields["doi"] and args.fix:
                text, _ = replace_field(text, "doi", normalized)
                fields["doi"] = normalized
                fixes.append(f"{entry.key}: normalized DOI")
                changed = True
            if not DOI_CANON_RE.match(normalized):
                errors.append(f"{entry.key}: DOI format suspicious '{fields['doi']}'")

            doi_to_keys.setdefault(normalized.lower(), []).append(entry.key)

            if not fields["url"] and args.fix:
                url = f"https://doi.org/{normalized}"
                text = add_field(text, "url", url)
                fields["url"] = url
                fixes.append(f"{entry.key}: added URL from DOI")
                changed = True

        if fields["url"] and not URL_RE.match(fields["url"]):
            errors.append(f"{entry.key}: URL must start with http/https ('{fields['url']}')")

        if fields["pmid"] and not fields["pmid"].isdigit():
            errors.append(f"{entry.key}: pmid field is not numeric ('{fields['pmid']}')")

        title_key = f"{fields['title'].lower()}::{fields['year']}" if fields["title"] and fields["year"] else ""
        if title_key:
            title_year_to_keys.setdefault(title_key, []).append(entry.key)

        if changed:
            replacements.append((entry.start, entry.end, text))

    for doi, keys in sorted(doi_to_keys.items()):
        if len(keys) > 1:
            warnings.append(f"Duplicate DOI across entries: {doi} -> {', '.join(keys)}")

    for title_year, keys in sorted(title_year_to_keys.items()):
        if len(keys) > 1:
            warnings.append(f"Potential duplicate title/year: {', '.join(keys)}")

    if args.fix and replacements and bib_text:
        updated = rebuild_bib_text(bib_text, replacements)
        if updated != bib_text:
            bib_path.write_text(updated, encoding="utf-8")

    # CSL + Pandoc checks
    if not pandoc_path.exists():
        errors.append(f"Pandoc defaults not found: {pandoc_path}")
        pandoc_text = ""
        pandoc_csl = ""
    else:
        pandoc_text = pandoc_path.read_text(encoding="utf-8")
        pandoc_csl = parse_pandoc_csl(pandoc_text)
        if not pandoc_csl:
            errors.append("pandoc.yaml: missing csl field")

    req_text = req_path.read_text(encoding="utf-8") if req_path.exists() else ""
    target_journal = extract_target_journal(req_text)
    expected_csl_name = infer_expected_csl(req_text, pandoc_csl)

    if pandoc_csl:
        csl_path = (paper_dir / pandoc_csl).resolve()

        req_match = REQ_CSL_LINE_RE.search(req_text)
        if req_match:
            req_csl_rel = req_match.group(1).strip().strip('"\'')
            req_csl_path = (paper_dir / req_csl_rel).resolve()
            if Path(req_csl_rel).as_posix() != Path(pandoc_csl).as_posix():
                if args.fix and req_csl_path.exists():
                    new_text, changed = set_pandoc_csl(pandoc_text, req_csl_rel)
                    if changed:
                        pandoc_path.write_text(new_text, encoding="utf-8")
                        pandoc_text = new_text
                        pandoc_csl = req_csl_rel
                        csl_path = req_csl_path
                        fixes.append("pandoc.yaml: aligned csl path to requirements")
                else:
                    errors.append(
                        f"CSL mismatch: pandoc.yaml uses '{pandoc_csl}', requirements expects '{req_csl_rel}'"
                    )

        if not csl_path.exists():
            errors.append(f"CSL file not found: {csl_path}")
        else:
            try:
                csl_info = parse_csl_info(csl_path)
            except ET.ParseError as exc:
                errors.append(f"CSL XML parse error: {exc}")
                csl_info = None
            if csl_info:
                token_name = expected_csl_name.lower()
                title_blob = f"{csl_info.title} {csl_info.style_id} {csl_info.path.name}".lower()
                if token_name and token_name not in title_blob:
                    warnings.append(
                        "CSL identity mismatch hint: expected token "
                        f"'{expected_csl_name}' not found in CSL metadata/title/id"
                    )

                expected_format = style_hint_from_name(expected_csl_name)
                if expected_format and csl_info.citation_format and csl_info.citation_format != expected_format:
                    errors.append(
                        "CSL citation-format mismatch: "
                        f"expected '{expected_format}' from style name but found '{csl_info.citation_format}'"
                    )

    target_journal_norm = target_journal.strip().lower()
    journal_is_set = bool(target_journal_norm and "tbd" not in target_journal_norm and "未定" not in target_journal_norm)
    has_explicit_csl_in_req = bool(REQ_CSL_LINE_RE.search(req_text))
    if journal_is_set and not has_explicit_csl_in_req:
        user_actions.append(
            "Target Journal is set but `design/01_requirements.md` lacks explicit `Citation Style (CSL)`; "
            "please specify the exact CSL file for the submission format."
        )

    failed = bool(errors or user_actions)
    status = "PASS" if not failed else "FAIL"

    report_lines = [
        "# QA: references and CSL report",
        f"Status: {status}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Inputs",
        f"- paper_dir: {paper_dir}",
        f"- bib: {bib_path}",
        f"- pandoc: {pandoc_path}",
        f"- requirements: {req_path}",
        f"- target_journal: {target_journal or '(not set)'}",
        f"- auto_fix: {args.fix}",
    ]

    report_lines.extend(["", "## Summary", f"- entries: {len(entries)}", f"- fixes applied: {len(fixes)}", f"- errors: {len(errors)}", f"- warnings: {len(warnings)}", f"- user actions required: {len(user_actions)}"])

    if fixes:
        report_lines.extend(["", "## Auto-fixes"])
        report_lines.extend(f"- {item}" for item in fixes)

    if errors:
        report_lines.extend(["", "## Errors"])
        report_lines.extend(f"- {item}" for item in errors)

    if warnings:
        report_lines.extend(["", "## Warnings"])
        report_lines.extend(f"- {item}" for item in warnings)

    if user_actions:
        report_lines.extend(["", "## User Action Required"])
        report_lines.extend(f"- {item}" for item in user_actions)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"QA references/style: {status} (errors={len(errors)}, user_actions={len(user_actions)})")
    print(f"Report: {report_path}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

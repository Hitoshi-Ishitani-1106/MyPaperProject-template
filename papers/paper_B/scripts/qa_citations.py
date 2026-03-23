#!/usr/bin/env python3
import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
import re
import sys

CITATION_GROUP_RE = re.compile(r'\[[^\]]*?@[^\]]*?\]')
CITEKEY_RE = re.compile(r'@([A-Za-z0-9_:.+/-]+)')
PMID_RE = re.compile(r'\[pmid:', re.IGNORECASE)

ENTRY_START_RE = re.compile(r'^\s*@', re.MULTILINE)
KEY_RE = re.compile(r'@\w+\s*\{\s*([^,\s]+)\s*,', re.IGNORECASE)
DOI_RE = re.compile(r'\bdoi\s*=\s*[{"]([^}"]+)[}"]', re.IGNORECASE)


def iter_section_files(root: Path, recursive: bool) -> list[Path]:
    if recursive:
        files = [path for path in root.rglob("*.md") if path.is_file()]
    else:
        files = [path for path in root.glob("*.md") if path.is_file()]
    return sorted(files)


def parse_bib_entries(text: str) -> list[tuple[str, str]]:
    entries = []
    starts = [match.start() for match in ENTRY_START_RE.finditer(text)]
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        entry_text = text[start:end]
        key_match = KEY_RE.search(entry_text)
        if not key_match:
            continue
        key = key_match.group(1).strip()
        entries.append((key, entry_text))
    return entries


def main() -> int:
    paper_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="QA for citekeys in sections/*.md against refs/references.bib."
    )
    parser.add_argument(
        "--sections-dir",
        default=str(paper_root / "sections"),
        help="Path to sections directory.",
    )
    parser.add_argument(
        "--bib",
        default=str(paper_root / "refs" / "references.bib"),
        help="Path to references.bib.",
    )
    parser.add_argument(
        "--report",
        default=str(paper_root / "reports" / "qa_citations.md"),
        help="Report output path.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan sections directory recursively for .md files.",
    )
    args = parser.parse_args()

    sections_root = Path(args.sections_dir)
    bib_path = Path(args.bib)
    report_path = Path(args.report)

    errors = []

    if not sections_root.exists():
        errors.append(f"Sections directory not found: {sections_root}")
        section_files: list[Path] = []
    else:
        section_files = iter_section_files(sections_root, args.recursive)
        if not section_files:
            errors.append(f"No markdown files found under: {sections_root}")

    if not bib_path.exists():
        errors.append(f"BibTeX file not found: {bib_path}")
        entries: list[tuple[str, str]] = []
    else:
        bib_text = bib_path.read_text(encoding="utf-8")
        entries = parse_bib_entries(bib_text)

    bib_keys = [key for key, _ in entries]
    bib_key_counts = Counter(bib_keys)
    bib_key_set = set(bib_keys)

    citations = Counter()
    pmid_hits: list[tuple[Path, int, str]] = []

    for path in section_files:
        text = path.read_text(encoding="utf-8")
        for group in CITATION_GROUP_RE.findall(text):
            for key in CITEKEY_RE.findall(group):
                citations[key] += 1
        for line_no, line in enumerate(text.splitlines(), start=1):
            if PMID_RE.search(line):
                pmid_hits.append((path, line_no, line.strip()))

    missing_keys = sorted(key for key in citations.keys() if key not in bib_key_set)
    duplicate_keys = sorted(
        [(key, count) for key, count in bib_key_counts.items() if count > 1]
    )

    doi_issues = []
    for key, entry_text in entries:
        for match in DOI_RE.finditer(entry_text):
            doi_value = match.group(1).strip()
            issue = None
            if "doi.org" in doi_value.lower():
                issue = "contains doi.org"
            elif any(ch.isspace() for ch in doi_value):
                issue = "contains whitespace"
            if issue:
                doi_issues.append((key, doi_value, issue))

    warning_count = len(duplicate_keys) + len(doi_issues)
    failed = bool(errors or missing_keys or pmid_hits)
    status = "PASS" if not failed else "FAIL"

    report_lines = [
        "# QA: citations report",
        f"Status: {status}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        f"- sections scanned: {len(section_files)}",
        f"- citations found: {sum(citations.values())} (unique: {len(citations)})",
        f"- missing citekeys: {len(missing_keys)}",
        f"- pmid placeholders: {len(pmid_hits)}",
        f"- warnings: {warning_count}",
    ]

    if errors:
        report_lines.extend(["", "## Errors"])
        report_lines.extend(f"- {error}" for error in errors)

    if missing_keys:
        report_lines.extend(["", "## Missing citekeys"])
        report_lines.extend(f"- {key}" for key in missing_keys)

    if pmid_hits:
        report_lines.extend(["", "## PMID placeholders"])
        for path, line_no, line in pmid_hits:
            report_lines.append(f"- {path}:{line_no} {line}")

    if duplicate_keys or doi_issues:
        report_lines.extend(["", "## Warnings"])
        if duplicate_keys:
            report_lines.append("### Duplicate citekeys in refs/references.bib")
            report_lines.extend(f"- {key} ({count})" for key, count in duplicate_keys)
        if doi_issues:
            report_lines.append("### DOI format issues")
            report_lines.extend(
                f"- {key}: {doi_value} ({issue})"
                for key, doi_value, issue in doi_issues
            )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"QA citations: {status} (missing={len(missing_keys)}, pmid={len(pmid_hits)})")
    print(f"Report: {report_path}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

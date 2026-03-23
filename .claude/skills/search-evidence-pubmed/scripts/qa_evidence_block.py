#!/usr/bin/env python3
import argparse
import json
import re
import sys

HEADER_RE = re.compile(r"^## .+作業日:\s*\d{4}-\d{2}-\d{2}", re.M)
HEADING_PMID = "### PMID一覧（整合チェック用；PubMedから完全コピー）"
HEADING_PAPERS = "### ■ 論文リスト（10-20本）"
HEADING_SUMMARY = "### ■ セクション総括（1段落）"
HEADING_EXCLUSIONS = "### ■ 除外ログ（PMID/理由）"


def parse_args():
    parser = argparse.ArgumentParser(description="Lint evidence block structure.")
    parser.add_argument("--block", required=True, help="Path to evidence block markdown.")
    parser.add_argument("--json", help="Optional evidence JSON log for count checks.")
    return parser.parse_args()


def extract_between(text, start, end):
    pattern = re.escape(start) + r"(.*?)(?=" + re.escape(end) + r"|$)"
    match = re.search(pattern, text, re.S)
    return match.group(1) if match else ""


def main():
    args = parse_args()
    try:
        with open(args.block, "r", encoding="utf-8") as f:
            block = f.read()
    except Exception as exc:
        print(f"error: failed to read block: {exc}", file=sys.stderr)
        return 1

    errors = []
    if not HEADER_RE.search(block):
        errors.append("header line with date is missing")
    if "**監査ログ**" not in block:
        errors.append("audit log section is missing")

    pmid_section = extract_between(block, HEADING_PMID, HEADING_PAPERS)
    paper_section = extract_between(block, HEADING_PAPERS, HEADING_SUMMARY)
    summary_section = extract_between(block, HEADING_SUMMARY, HEADING_EXCLUSIONS)
    exclusion_section = extract_between(block, HEADING_EXCLUSIONS, "")

    if not pmid_section:
        errors.append("PMID list section missing or empty")
    if not paper_section:
        errors.append("paper list section missing or empty")
    if not summary_section.strip():
        errors.append("section summary missing or empty")
    if not exclusion_section.strip():
        errors.append("exclusion log missing or empty")

    pmid_list_pmids = re.findall(r"PMID:\s*(\d{6,10})", pmid_section)
    paper_pmids = re.findall(r"PMID:\s*(\d{6,10})", paper_section)
    paper_items = re.findall(r"^\d+\.\s", paper_section, re.M)

    if not pmid_list_pmids:
        errors.append("PMID list contains no PMIDs")
    if not paper_pmids:
        errors.append("paper list contains no PMIDs")
    if len(paper_items) != len(paper_pmids):
        errors.append("paper list numbering does not match PMID count")
    if len(set(paper_pmids)) != len(paper_pmids):
        errors.append("duplicate PMIDs detected in paper list")

    if set(pmid_list_pmids) != set(paper_pmids):
        errors.append("PMID list and paper list PMIDs do not match")

    for pmid in paper_pmids:
        if f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" not in paper_section:
            errors.append(f"missing PubMed link for PMID {pmid}")

    audit_section = extract_between(block, "**監査ログ**：", HEADING_PMID)
    shortage_reason = ""
    if audit_section:
        match = re.search(r"不足理由.*?:\s*(.*)", audit_section)
        if match:
            shortage_reason = match.group(1).strip()
    if paper_pmids:
        if (len(paper_pmids) < 10 or len(paper_pmids) > 20) and not shortage_reason:
            errors.append("paper count outside 10-20 without shortage reason")

    if args.json:
        try:
            with open(args.json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            errors.append(f"failed to read JSON log: {exc}")
        else:
            json_papers = data.get("papers", [])
            json_pmids = data.get("pmid_list", [])
            if json_papers and len(json_papers) != len(paper_pmids):
                errors.append("JSON paper count does not match block")
            if json_pmids and len(json_pmids) != len(pmid_list_pmids):
                errors.append("JSON PMID list count does not match block")

    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    print("PASS: evidence block structure OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

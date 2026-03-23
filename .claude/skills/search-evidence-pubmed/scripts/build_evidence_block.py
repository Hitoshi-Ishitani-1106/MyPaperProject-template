#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import date

DEFAULT_SELECTION_NOTE = (
    "関連性最優先で抽出。同等時は設計>年代>影響>適合性で整序。"
    "2015年以降の原著中心、レビュー<=3、古典<=2-3。星は基準充足度（★★★/★★/★）。"
)


def parse_args():
    parser = argparse.ArgumentParser(description="Build evidence.md block from JSON.")
    parser.add_argument("--input", required=True, help="Input JSON log.")
    parser.add_argument("--template", required=True, help="Template markdown path.")
    parser.add_argument("--out", help="Output markdown path. If omitted, prints to stdout.")
    return parser.parse_args()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def require_keys(data, keys):
    missing = []
    for key in keys:
        if key not in data or data[key] in (None, "", []):
            missing.append(key)
    return missing


def format_excluded_breakdown(breakdown):
    if not breakdown:
        return "内訳なし"
    parts = []
    for key, value in breakdown.items():
        parts.append(f"{key}{value}")
    return "、".join(parts)


def format_pmid_list(pmid_list):
    if not pmid_list:
        return "- なし"
    lines = []
    for entry in pmid_list:
        pmid = entry.get("pmid", "")
        title = entry.get("title", "")
        journal = entry.get("journal", "")
        year = entry.get("year", "")
        doi = entry.get("doi", "")
        doi_part = f" doi:{doi}" if doi else ""
        lines.append(f"- PMID: {pmid} | **{title}**. *{journal}*. {year}.{doi_part}")
    return "\n".join(lines)


def format_paper_list(papers):
    lines = []
    for idx, paper in enumerate(papers, start=1):
        pmid = paper.get("pmid", "")
        rating = paper.get("rating", "")
        topic = paper.get("topic_summary", "")
        design = paper.get("design", "")
        author = paper.get("author", "")
        year = paper.get("year", "")
        journal = paper.get("journal_abbrev", "") or paper.get("journal", "")
        summary = paper.get("summary", "")

        lines.append(
            f"{idx}. **{rating}**：{topic}（{design}）  \n"
            f"   {author} et al., {year} {journal}  \n"
            f"   PMID: {pmid}  \n"
            f"   PubMed: https://pubmed.ncbi.nlm.nih.gov/{pmid}/  \n"
            f"   {summary}"
        )
    return "\n\n".join(lines) if lines else "- なし"


def format_exclusions(exclusions):
    if not exclusions:
        return "- なし"
    lines = []
    for item in exclusions:
        pmid = item.get("pmid", "")
        reason = item.get("reason", "")
        lines.append(f"- PMID: {pmid}／理由：{reason}")
    return "\n".join(lines)


def render_template(template, mapping):
    output = template
    for key, value in mapping.items():
        output = output.replace("{{" + key + "}}", value)
    if "{{" in output:
        raise ValueError("template has unreplaced placeholders")
    return output


def main():
    args = parse_args()
    try:
        data = load_json(args.input)
    except Exception as exc:
        print(f"error: failed to load JSON: {exc}", file=sys.stderr)
        return 1

    try:
        with open(args.template, "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as exc:
        print(f"error: failed to read template: {exc}", file=sys.stderr)
        return 1

    missing = require_keys(data, ["section_name", "theme", "papers", "section_summary"])
    if missing:
        print(f"error: missing required fields: {', '.join(missing)}", file=sys.stderr)
        return 1

    pmid_list = data.get("pmid_list", [])
    papers = data.get("papers", [])
    exclusions = data.get("exclusions", [])
    audit_log = data.get("audit_log", {})

    run_date = data.get("run_date") or date.today().isoformat()
    selection_note = data.get("selection_note") or DEFAULT_SELECTION_NOTE
    retrieved_count = audit_log.get("retrieved", len(pmid_list))
    included_count = audit_log.get("included", len(papers))
    excluded_count = audit_log.get("excluded", len(exclusions))
    excluded_breakdown = format_excluded_breakdown(audit_log.get("excluded_breakdown"))
    shortage_reason = audit_log.get("shortage_reason") or "なし"

    mapping = {
        "section_name": data["section_name"],
        "theme": data["theme"],
        "run_date": run_date,
        "selection_note": selection_note,
        "retrieved_count": str(retrieved_count),
        "included_count": str(included_count),
        "excluded_count": str(excluded_count),
        "excluded_breakdown": excluded_breakdown,
        "shortage_reason": shortage_reason,
        "pmid_list": format_pmid_list(pmid_list),
        "paper_list": format_paper_list(papers),
        "section_summary": data["section_summary"],
        "excluded_list": format_exclusions(exclusions),
    }

    try:
        output = render_template(template, mapping)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

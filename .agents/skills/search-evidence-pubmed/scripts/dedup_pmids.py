#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Deduplicate PMIDs and titles.")
    parser.add_argument(
        "--input",
        required=True,
        help="Input JSON from pubmed_fetch or evidence log.",
    )
    parser.add_argument("--out", help="Output JSON path. If omitted, prints to stdout.")
    return parser.parse_args()


def normalize_title(title):
    text = (title or "").lower()
    text = re.sub(r"\\s+", " ", text).strip()
    text = re.sub(r"[^\\w\\s]", "", text)
    return text


def select_entries(data):
    if "records" in data:
        return "records", data["records"]
    if "pmid_list" in data:
        return "pmid_list", data["pmid_list"]
    raise ValueError("Input JSON must include 'records' or 'pmid_list'.")


def main():
    args = parse_args()
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"error: failed to read JSON: {exc}", file=sys.stderr)
        return 1

    try:
        key, entries = select_entries(data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    seen_pmids = set()
    seen_titles = set()
    deduped = []
    removed = []

    for entry in entries:
        pmid = str(entry.get("pmid", "")).strip()
        title = entry.get("title", "")
        norm_title = normalize_title(title)
        reason = None

        if pmid and pmid in seen_pmids:
            reason = "pmid_duplicate"
        elif norm_title and norm_title in seen_titles:
            reason = "title_duplicate"

        if reason:
            removed.append({"pmid": pmid, "title": title, "reason": reason})
            continue

        if pmid:
            seen_pmids.add(pmid)
        if norm_title:
            seen_titles.add(norm_title)
        deduped.append(entry)

    out = dict(data)
    out[key] = deduped
    out["removed"] = removed

    payload = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    sys.exit(main())

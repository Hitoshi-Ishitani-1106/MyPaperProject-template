#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DEFAULT_TOOL = "codex-search-evidence"
CHUNK_SIZE = 200


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed metadata via E-utilities (EFetch)."
    )
    parser.add_argument("--pmids", help="Comma-separated PMID list.")
    parser.add_argument("--pmid-file", help="File with one PMID per line.")
    parser.add_argument("--out", help="Output JSON path. If omitted, prints to stdout.")
    parser.add_argument("--email", help="Email for NCBI requests.")
    parser.add_argument("--tool", default=DEFAULT_TOOL, help="Tool name for NCBI requests.")
    parser.add_argument(
        "--api-key", default=os.environ.get("NCBI_API_KEY"), help="NCBI API key."
    )
    return parser.parse_args()


def read_pmids(args):
    pmids = []
    if args.pmids:
        pmids.extend([p.strip() for p in args.pmids.split(",") if p.strip()])
    if args.pmid_file:
        with open(args.pmid_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                pmids.append(line)
    if not pmids:
        raise ValueError("No PMIDs provided.")
    seen = set()
    ordered = []
    for pmid in pmids:
        if pmid not in seen:
            seen.add(pmid)
            ordered.append(pmid)
    return ordered


def fetch_xml(pmids, api_key=None, email=None, tool=None):
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    if api_key:
        params["api_key"] = api_key
    if email:
        params["email"] = email
    if tool:
        params["tool"] = tool
    url = f"{EUTILS_BASE}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": tool or DEFAULT_TOOL})
    with urlopen(req) as resp:
        return resp.read()


def text_from(elem):
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def extract_year(pub_date_elem):
    if pub_date_elem is None:
        return ""
    year = text_from(pub_date_elem.find("Year"))
    if year:
        return year
    medline = text_from(pub_date_elem.find("MedlineDate"))
    if medline:
        match = re.search(r"(19|20)\\d{2}", medline)
        if match:
            return match.group(0)
    return ""


def parse_records(xml_bytes):
    root = ET.fromstring(xml_bytes)
    records = []
    for article in root.findall(".//PubmedArticle"):
        pmid = text_from(article.find(".//PMID"))
        article_elem = article.find(".//Article")
        title = text_from(article_elem.find("ArticleTitle")) if article_elem is not None else ""
        journal_elem = article_elem.find("Journal") if article_elem is not None else None
        journal = text_from(journal_elem.find("Title")) if journal_elem is not None else ""
        journal_abbrev = (
            text_from(journal_elem.find("ISOAbbreviation")) if journal_elem is not None else ""
        )
        pub_date = journal_elem.find(".//JournalIssue/PubDate") if journal_elem is not None else None
        year = extract_year(pub_date)

        doi = ""
        for aid in article.findall(".//ArticleIdList/ArticleId"):
            if aid.get("IdType") == "doi":
                doi = text_from(aid)
                if doi:
                    break
        if not doi and article_elem is not None:
            for eloc in article_elem.findall(".//ELocationID"):
                if eloc.get("EIdType") == "doi":
                    doi = text_from(eloc)
                    if doi:
                        break

        first_author = ""
        author = article_elem.find(".//AuthorList/Author") if article_elem is not None else None
        if author is not None:
            first_author = text_from(author.find("LastName"))

        abstract_parts = []
        if article_elem is not None:
            for ab in article_elem.findall(".//Abstract/AbstractText"):
                label = ab.get("Label")
                text = text_from(ab)
                if not text:
                    continue
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)
        abstract = "\\n".join(abstract_parts)

        records.append(
            {
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "journal_abbrev": journal_abbrev,
                "year": year,
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                "first_author": first_author,
                "abstract": abstract,
            }
        )
    return records


def main():
    args = parse_args()
    try:
        pmids = read_pmids(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    records = []
    for idx in range(0, len(pmids), CHUNK_SIZE):
        chunk = pmids[idx : idx + CHUNK_SIZE]
        try:
            xml_bytes = fetch_xml(chunk, args.api_key, args.email, args.tool)
        except Exception as exc:
            print(f"error: fetch failed for chunk starting {chunk[0]}: {exc}", file=sys.stderr)
            return 1
        records.extend(parse_records(xml_bytes))
        if not args.api_key:
            time.sleep(0.34)

    by_pmid = {record["pmid"]: record for record in records if record.get("pmid")}
    ordered = [by_pmid[pmid] for pmid in pmids if pmid in by_pmid]
    missing = [pmid for pmid in pmids if pmid not in by_pmid]

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "pubmed",
        "pmids": pmids,
        "records": ordered,
        "missing": missing,
    }

    output = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

    return 3 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

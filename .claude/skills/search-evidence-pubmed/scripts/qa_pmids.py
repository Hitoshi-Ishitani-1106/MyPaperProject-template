#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DEFAULT_TOOL = "codex-search-evidence"
CHUNK_SIZE = 200


def parse_args():
    parser = argparse.ArgumentParser(
        description="Verify PMID existence and metadata match via PubMed."
    )
    parser.add_argument("--input", required=True, help="Evidence JSON log path.")
    parser.add_argument("--email", help="Email for NCBI requests.")
    parser.add_argument("--tool", default=DEFAULT_TOOL, help="Tool name for NCBI requests.")
    parser.add_argument(
        "--api-key", default=os.environ.get("NCBI_API_KEY"), help="NCBI API key."
    )
    return parser.parse_args()


def norm_text(value):
    text = (value or "").strip().rstrip(".")
    text = re.sub(r"\\s+", " ", text)
    return text.lower()


def norm_doi(value):
    text = (value or "").strip().lower()
    text = re.sub(r"^doi:\\s*", "", text)
    text = re.sub(r"^https?://(dx\\.)?doi\\.org/", "", text)
    return text


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

        records.append(
            {
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "journal_abbrev": journal_abbrev,
                "year": year,
                "doi": doi,
            }
        )
    return records


def fetch_records(pmids, api_key=None, email=None, tool=None):
    records = []
    for idx in range(0, len(pmids), CHUNK_SIZE):
        chunk = pmids[idx : idx + CHUNK_SIZE]
        xml_bytes = fetch_xml(chunk, api_key, email, tool)
        records.extend(parse_records(xml_bytes))
        if not api_key:
            time.sleep(0.34)
    return records


def main():
    args = parse_args()
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"error: failed to read JSON: {exc}", file=sys.stderr)
        return 1

    pmid_list = data.get("pmid_list") or []
    if not pmid_list:
        print("error: pmid_list is required in evidence JSON.", file=sys.stderr)
        return 1

    expected = {}
    errors = []
    for entry in pmid_list:
        pmid = str(entry.get("pmid", "")).strip()
        if not pmid:
            errors.append("pmid_list entry missing PMID")
            continue
        if pmid in expected:
            errors.append(f"duplicate PMID in pmid_list: {pmid}")
            continue
        expected[pmid] = entry

    paper_pmids = {p.get("pmid") for p in data.get("papers", []) if p.get("pmid")}
    missing_from_list = paper_pmids - set(expected.keys())
    if missing_from_list:
        errors.append(f"papers contain PMID(s) not in pmid_list: {sorted(missing_from_list)}")

    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    actual_records = fetch_records(
        list(expected.keys()), api_key=args.api_key, email=args.email, tool=args.tool
    )
    actual_by_pmid = {record["pmid"]: record for record in actual_records if record.get("pmid")}

    for pmid, entry in expected.items():
        actual = actual_by_pmid.get(pmid)
        if not actual:
            errors.append(f"PMID not found in PubMed: {pmid}")
            continue

        exp_title = entry.get("title", "")
        exp_journal = entry.get("journal", "")
        exp_year = str(entry.get("year", "")).strip()
        exp_doi = entry.get("doi", "")

        if norm_text(exp_title) != norm_text(actual.get("title")):
            errors.append(f"{pmid}: title mismatch")

        actual_journal_norms = {
            norm_text(actual.get("journal")),
            norm_text(actual.get("journal_abbrev")),
        }
        if norm_text(exp_journal) not in actual_journal_norms:
            errors.append(f"{pmid}: journal mismatch")

        act_year = str(actual.get("year", "")).strip()
        if not act_year or exp_year != act_year:
            errors.append(f"{pmid}: year mismatch (expected {exp_year}, got {act_year})")

        act_doi = norm_doi(actual.get("doi"))
        exp_doi_norm = norm_doi(exp_doi)
        if act_doi and not exp_doi_norm:
            errors.append(f"{pmid}: DOI missing in evidence (PubMed has {act_doi})")
        elif exp_doi_norm and not act_doi:
            errors.append(f"{pmid}: DOI missing in PubMed response")
        elif exp_doi_norm and act_doi and exp_doi_norm != act_doi:
            errors.append(f"{pmid}: DOI mismatch")

    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    print(f"PASS: {len(expected)} PMID(s) verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())

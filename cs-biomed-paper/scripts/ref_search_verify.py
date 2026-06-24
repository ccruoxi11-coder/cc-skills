#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Multi-source literature search + DOI/citation verification → .bib / .ris export.

Self-contained: standard library only (urllib), no API keys. Hits two free public APIs:

  - Crossref   (https://api.crossref.org)  — journal/conference metadata, DOI of record.
  - OpenAlex   (https://api.openalex.org)  — indexes Crossref + PubMed + arXiv; good recall.

This is the "output first" tool for stage 02 (literature) and stage 08 (citations): it produces a
real .bib/.ris file you can import into Zotero/EndNote/Mendeley, and it VERIFIES each chosen DOI
against Crossref so you never cite a fabricated or mistyped reference.

Usage:
    # Search by topic, export top 10 to BibTeX
    python ref_search_verify.py --query "deep learning sepsis prediction ICU" --limit 10 --bib out.bib

    # Search PubMed-style biomedical topic, export RIS too, filter by year
    python ref_search_verify.py -q "radiomics glioma MRI segmentation" --year-from 2020 \
        --bib refs.bib --ris refs.ris

    # Verify a list of DOIs you already have (no search) and export
    python ref_search_verify.py --verify-doi 10.1038/s41591-020-0942-0 10.1109/TMI.2016.2528162 --bib v.bib

    # Use OpenAlex only (broader recall) or Crossref only
    python ref_search_verify.py -q "wearable ECG atrial fibrillation" --source openalex

Be polite to the public pools: pass --mailto you@example.com (or set CROSSREF_MAILTO).

Output: prints a ranked, de-duplicated list (title, year, venue, DOI, verified?) to stdout, and
writes .bib / .ris if requested. Per-source failures are reported on stderr and do not abort the run.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"
DEFAULT_MAILTO = os.environ.get("CROSSREF_MAILTO", "cs-biomed-paper@users.noreply.github.com")


def _get(url, mailto, tries=3):
    """GET JSON with a polite UA and basic retry/backoff. Returns dict or None."""
    headers = {"User-Agent": f"cs-biomed-paper/1.0 (mailto:{mailto})"}
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < tries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            print(f"[warn] HTTP {e.code} for {url}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if attempt < tries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            print(f"[warn] request failed for {url}: {e}", file=sys.stderr)
            return None
    return None


def search_crossref(query, limit, year_from, mailto):
    params = {"query": query, "rows": str(limit), "select":
              "DOI,title,author,issued,container-title,type,volume,issue,page,publisher"}
    if year_from:
        params["filter"] = f"from-pub-date:{year_from}-01-01"
    url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}&mailto={mailto}"
    data = _get(url, mailto)
    items = (data or {}).get("message", {}).get("items", [])
    out = []
    for it in items:
        out.append({
            "doi": (it.get("DOI") or "").lower(),
            "title": " ".join(it.get("title") or []).strip(),
            "authors": [f"{a.get('family','')}, {a.get('given','')}".strip(", ")
                        for a in it.get("author", []) if a.get("family")],
            "year": _cr_year(it.get("issued")),
            "venue": " ".join(it.get("container-title") or []).strip(),
            "type": it.get("type", ""),
            "volume": it.get("volume", ""), "issue": it.get("issue", ""),
            "pages": it.get("page", ""), "publisher": it.get("publisher", ""),
            "source": "crossref",
        })
    return out


def _cr_year(issued):
    try:
        return str(issued["date-parts"][0][0])
    except (KeyError, IndexError, TypeError):
        return ""


def search_openalex(query, limit, year_from, mailto):
    params = {"search": query, "per-page": str(limit), "mailto": mailto}
    if year_from:
        params["filter"] = f"from_publication_date:{year_from}-01-01"
    url = f"{OPENALEX_API}?{urllib.parse.urlencode(params)}"
    data = _get(url, mailto)
    items = (data or {}).get("results", [])
    out = []
    for it in items:
        doi = (it.get("doi") or "").replace("https://doi.org/", "").lower()
        host = (it.get("primary_location") or {}).get("source") or {}
        out.append({
            "doi": doi,
            "title": (it.get("title") or "").strip(),
            "authors": [a.get("author", {}).get("display_name", "")
                        for a in it.get("authorships", [])],
            "year": str(it.get("publication_year") or ""),
            "venue": (host.get("display_name") or "").strip(),
            "type": it.get("type", ""),
            "volume": (it.get("biblio") or {}).get("volume", "") or "",
            "issue": (it.get("biblio") or {}).get("issue", "") or "",
            "pages": _oa_pages(it.get("biblio") or {}),
            "publisher": (host.get("host_organization_name") or ""),
            "source": "openalex",
        })
    return out


def _oa_pages(biblio):
    f, l = biblio.get("first_page"), biblio.get("last_page")
    return f"{f}-{l}" if f and l else (f or "")


def verify_doi(doi, mailto):
    """Confirm a DOI resolves on Crossref; return normalized record or None."""
    url = f"{CROSSREF_API}/{urllib.parse.quote(doi)}?mailto={mailto}"
    data = _get(url, mailto)
    it = (data or {}).get("message")
    if not it:
        return None
    return {
        "doi": (it.get("DOI") or doi).lower(),
        "title": " ".join(it.get("title") or []).strip(),
        "authors": [f"{a.get('family','')}, {a.get('given','')}".strip(", ")
                    for a in it.get("author", []) if a.get("family")],
        "year": _cr_year(it.get("issued")),
        "venue": " ".join(it.get("container-title") or []).strip(),
        "type": it.get("type", ""),
        "volume": it.get("volume", ""), "issue": it.get("issue", ""),
        "pages": it.get("page", ""), "publisher": it.get("publisher", ""),
        "source": "crossref-verified", "verified": True,
    }


def dedup(records):
    """Merge by DOI (preferred) or normalized title; keep the richest record."""
    by_key = {}
    for r in records:
        key = r["doi"] or re.sub(r"\W+", "", r["title"].lower())[:60]
        if not key:
            continue
        if key not in by_key or len(str(r)) > len(str(by_key[key])):
            by_key[key] = r
    return list(by_key.values())


def _bib_key(r):
    first = (r["authors"][0].split(",")[0] if r["authors"] else "anon").strip()
    first = re.sub(r"\W+", "", first) or "anon"
    word = next((w for w in re.findall(r"[A-Za-z]+", r["title"]) if len(w) > 3), "ref")
    return f"{first}{r['year']}{word.lower()}"


def to_bibtex(records):
    out = []
    for r in records:
        etype = "article" if "journal" in (r["type"] or "article") else "inproceedings"
        fields = [
            ("title", r["title"]),
            ("author", " and ".join(r["authors"])),
            ("year", r["year"]),
            ("journal" if etype == "article" else "booktitle", r["venue"]),
            ("volume", r["volume"]), ("number", r["issue"]), ("pages", r["pages"]),
            ("publisher", r["publisher"]), ("doi", r["doi"]),
        ]
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
        out.append(f"@{etype}{{{_bib_key(r)},\n{body}\n}}")
    return "\n\n".join(out) + "\n"


def to_ris(records):
    out = []
    for r in records:
        ty = "JOUR" if "journal" in (r["type"] or "journal") else "CONF"
        lines = [f"TY  - {ty}", f"TI  - {r['title']}"]
        for a in r["authors"]:
            lines.append(f"AU  - {a}")
        if r["year"]:
            lines.append(f"PY  - {r['year']}")
        if r["venue"]:
            lines.append(f"JO  - {r['venue']}")
        for tag, val in (("VL", r["volume"]), ("IS", r["issue"]),
                         ("SP", r["pages"]), ("PB", r["publisher"]), ("DO", r["doi"])):
            if val:
                lines.append(f"{tag}  - {val}")
        lines.append("ER  - ")
        out.append("\n".join(lines))
    return "\n\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Multi-source literature search + DOI verification.")
    ap.add_argument("-q", "--query", help="search query (topic / keywords)")
    ap.add_argument("--verify-doi", nargs="+", help="verify these DOIs instead of searching")
    ap.add_argument("--source", choices=["both", "crossref", "openalex"], default="both")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--year-from", type=int, default=None)
    ap.add_argument("--mailto", default=DEFAULT_MAILTO)
    ap.add_argument("--bib", help="write BibTeX to this path")
    ap.add_argument("--ris", help="write RIS to this path")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip DOI verification of search hits (faster)")
    args = ap.parse_args()

    if not args.query and not args.verify_doi:
        ap.error("provide --query or --verify-doi")

    records = []
    if args.verify_doi:
        for d in args.verify_doi:
            rec = verify_doi(d.lower().replace("https://doi.org/", ""), args.mailto)
            if rec:
                records.append(rec)
            else:
                print(f"[warn] DOI did NOT verify: {d}", file=sys.stderr)
    else:
        if args.source in ("both", "crossref"):
            records += search_crossref(args.query, args.limit, args.year_from, args.mailto)
        if args.source in ("both", "openalex"):
            records += search_openalex(args.query, args.limit, args.year_from, args.mailto)
        records = dedup(records)
        if not args.no_verify:
            for r in records:
                r["verified"] = bool(r["doi"]) and verify_doi(r["doi"], args.mailto) is not None
        records.sort(key=lambda r: r["year"], reverse=True)

    # Report
    print(f"\n{len(records)} record(s):\n" + "-" * 72)
    for i, r in enumerate(records, 1):
        flag = "OK " if r.get("verified") else "?? "
        print(f"[{i:>2}] {flag} ({r['year']}) {r['title'][:70]}")
        print(f"      {r['venue'][:60]}  doi:{r['doi'] or '[none]'}  via {r['source']}")
    print("-" * 72)
    unver = [r for r in records if not r.get("verified")]
    if unver:
        print(f"[note] {len(unver)} record(s) UNVERIFIED — confirm before citing.", file=sys.stderr)

    if args.bib:
        with open(args.bib, "w", encoding="utf-8") as f:
            f.write(to_bibtex(records))
        print(f"[ok] wrote {args.bib}")
    if args.ris:
        with open(args.ris, "w", encoding="utf-8") as f:
            f.write(to_ris(records))
        print(f"[ok] wrote {args.ris}")


if __name__ == "__main__":
    main()

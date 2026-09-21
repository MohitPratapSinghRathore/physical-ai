"""Fetch the raw inputs that allow automated access, and name the ones that do not.

No API key is required by any source used here. Where a key would speed a source up,
it is read from the environment and never stored: see .env.example.

Sources that refused automated requests from the environment the paper was built in
are listed at the end with the exact file, the landing page, and where to put it.

Run:  python replication/fetch_raw.py      (or: make fetch)
"""
from __future__ import annotations

import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

AUTOMATED = [
    ("Financial Accounts (Z.1)", "src/fetch_fred.py",
     "https://www.federalreserve.gov/releases/z1/", "framework/labor_backing/_z1_cache.zip"),
    ("Distributional Financial Accounts", "src/fetch_fred.py",
     "https://www.federalreserve.gov/releases/z1/dataviz/dfa/", "framework/labor_backing/_dfa_cache.zip"),
    ("FRED series", "src/fetch_fred.py", "https://fred.stlouisfed.org/", "data/raw/fred"),
    ("SEC EDGAR company facts", "src/fetch_sec.py",
     "https://www.sec.gov/edgar/sec-api-documentation", "data/raw/sec"),
    ("Enterprise 10-K filings", "src/fetch_sec.py",
     "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany", "data/raw/gse"),
    ("FDIC institution panel", "framework/institutions/fetch_fdic.py",
     "https://banks.data.fdic.gov/docs/", "framework/institutions/fdic_institutions_20260630.csv"),
    ("Census SIPP, ACS PUMS, O*NET, crosswalks", "src/fetch_bulk.sh",
     "https://www.census.gov/programs-surveys/sipp/data.html", "data/raw/"),
]

MANUAL = [
    ("Worker Displacement Survey, fourteen biennial vintages",
     "Bureau of Labor Statistics",
     "https://www.bls.gov/news.release/disp.toc.htm",
     "data/raw/bls_ep/", "the site returns 403 to scripted requests"),
    ("NCUA 5300 call report, 2026-06 bulk file", "NCUA",
     "https://ncua.gov/analysis/credit-union-corporate-call-report-data",
     "framework/institutions/ncua_2026-06.zip", "bulk download is behind a form"),
    ("CBO, Taxing Capital Income (2014)", "Congressional Budget Office",
     "https://www.cbo.gov/publication/49817",
     "data/raw/manual/", "the site returns 403 to scripted requests"),
    ("CRS R47113, shareholder-level effective rates",
     "Congressional Research Service",
     "https://crsreports.congress.gov/product/details?prodcode=R47113",
     "data/raw/manual/", "the site returns 403 to scripted requests"),
    ("DFAST 2026 supervisory results", "Federal Reserve Board",
     "https://www.federalreserve.gov/publications/dodd-frank-act-stress-test-publications.htm",
     "data/raw/manual/", "published as a PDF, read by hand into notes"),
    ("2026 Trustees Report summary tables",
     "Social Security and Medicare Boards of Trustees",
     "https://www.ssa.gov/OACT/TR/", "data/raw/manual/",
     "published as a PDF, read by hand into notes"),
    ("IRS Statistics of Income Table 1.4", "Internal Revenue Service",
     "https://www.irs.gov/statistics/soi-tax-stats-individual-statistical-tables-by-size-of-adjusted-gross-income",
     "data/raw/irs/", "spreadsheet download, no API"),
]


def main() -> int:
    contact = os.environ.get("CONTACT_EMAIL")
    if not contact:
        print("Set CONTACT_EMAIL (and CONTACT_NAME) before fetching: the SEC and FDIC")
        print("fair-access policies require a real contact in the User-Agent header.")
        print("Copy .env.example to .env and fill it in.")
        return 1

    print("Scripted sources, run these in order:")
    for name, script, url, dest in AUTOMATED:
        print(f"  {name}\n    python {script}\n    landing page: {url}\n    writes: {dest}")
    print()
    print("Manual downloads. These refused automated access; fetch them in a browser")
    print("and place the file at the path given, then run `make verify`.")
    for name, pub, url, dest, why in MANUAL:
        print(f"  {name} ({pub})\n    {url}\n    place at: {dest}\n    why manual: {why}")
    print()
    print("Nothing was downloaded by this script: it prints the plan so that each step")
    print("is a deliberate act under the publisher's terms. Run the scripts above to")
    print("fetch, or see DATA_SOURCES.md for the full table.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

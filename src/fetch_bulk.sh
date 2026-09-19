#!/usr/bin/env bash
# One-time bulk downloads. Resumable. See data/SOURCES.md for provenance.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw/onet data/raw/pums data/raw/crosswalk
get () { echo "-> $2"; curl -sL -C - --retry 5 --retry-all-errors -o "$2" "$1"; }
get "https://www.onetcenter.org/dl_files/database/db_31_0_text.zip" data/raw/onet/db_31_0_text.zip
get "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pus.zip" data/raw/pums/csv_pus.zip
get "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_hus.zip" data/raw/pums/csv_hus.zip
get "https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/2018-occupation-code-list-and-crosswalk.xlsx" data/raw/crosswalk/census2018_occ_soc.xlsx
echo "done"

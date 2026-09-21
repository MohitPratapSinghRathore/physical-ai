# Release notes, version 1.0.0

Cut on 2026-09-21 for the submitted manuscript "Labor-Backed Finance and the Fiscal
Exposure to AI".

## Provenance

This package was generated from the authors' private repository commit
`a1b6a0ea6ff1bdf017905b6a0067294db93a86bd` (private repository commit A139). The history
of that repository is not carried over: this repository begins with a single initial
commit. The mapping above exists so the authors can audit which state of the private work
the release corresponds to, and it is removed from the anonymous variant.

## What it contains

The pipeline that produces every number in the paper, the measured artifacts those numbers
are read from, the rebuild specifications and reports, and documentation. See `README.md`
for the two rebuild levels and `CHANGELOG.md` for the full list.

## What was checked before cutting it

- `make headline` rebuilt 24 headline quantities and compared each to the released
  artifacts, and regenerated all 329 values the paper reports from `data/release/` and
  compared them key by key. All passed.
- A secrets and identity scan over the whole tree: no API key, token, password or `.env`
  file; no absolute path; contact details replaced by environment variables.
- No file over 50 MB; no raw data; no manuscript source; no file of expected values.

## Known gaps

`make all` could not be exercised end to end where the source refuses automated access.
The stages that were exercised, and the ones that were not, are listed in `README.md` and
in `DATA_SOURCES.md`.

## Held for owner confirmation

Author names, their order, affiliations and every ORCID; the two DOI placeholders; the
licence choices; and the Zenodo route in `ZENODO_STEPS.md`.

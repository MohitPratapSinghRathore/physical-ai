# Physical AI: The Two-Sided Bet

Research project on wage-backed debt, AI-capital-backed debt, and the financial
architecture of a labor transition. See [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for the
thesis, the rules, and the workstreams. The brief is the source of truth.

## Status

Session 1 complete (2026-09-19). WS0 first query batch done; WS1 US Leg W done; Leg A
Tier 2 done. Leg A Tiers 1 and 2b remain open, which is why no Leg W to Leg A verdict
should be quoted yet.

Read [`notes/findings.md`](notes/findings.md) first. Results that weaken the thesis are at
the top, per brief Rule 5, and one of the brief's central hypotheses did not survive
testing this session.

## Headline results so far

| Result | Value | Where |
|---|---|---|
| Labor-linked share of US federal current receipts | 77.7% | findings B1 |
| US household debt | 21,377.8 USD bn (65.8% of GDP) | findings B2 |
| US federal public debt | 39,065.4 USD bn (120.3% of GDP) | findings B2 |
| Physical AI Exposure Index | 911 occupations, O*NET 31.0 | findings B3 |
| Mortgage debt service by PAEI quintile | concentration ratio flat, 0.93 to 1.08 | findings A4 |
| Leg A Tier 2 capex (9 US firms) | 490.9 USD bn, self-funding 1.34 | findings B4 |
| Leg A debt and leases / household debt | 2.14% (LOWER BOUND) | sizing_method.md |

The last row is a lower bound, not a verdict. It excludes the off-balance-sheet structures
BIS identifies as dominant, so the WS1 kill criterion is NOT yet evaluable (decision D4).

## The two original artifacts

**PAEI, the Physical AI Exposure Index** (`data/processed/paei_onet.csv`). Existing
occupational AI-exposure measures score cognitive automation. PAEI scores exposure to
embodied automation, and is two-factor and multiplicative following Moravec's paradox:

    PAEI = P * S,  P = embodiment intensity,  S = environmental structure

Either factor near zero means no exposure. The design is validated by an inversion an
additive index would get wrong: electricians are more physically demanding than team
assemblers (P 0.68 vs 0.55) but less exposed (PAEI 0.26 vs 0.32), because their work
environment is unstructured. P and S correlate at -0.06 across 911 occupations, so the
second factor carries independent information.

**DAR, Debt-at-Automation-Risk** (`data/processed/dar_us.csv`,
`data/processed/dar_intensity_us.csv`). PAEI joined to ACS PUMS 2023 to measure how much US
mortgage debt service is paid out of wages earned in high-exposure occupations.

## Reproducing

```
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./src/fetch_bulk.sh      # one-time large downloads (O*NET, PUMS, crosswalk)
make all                 # fetch series, rebuild every table, regenerate SOURCES.md
```

`data/SOURCES.md` is generated, never hand-edited. Every series carries its published
title, units, source and retrieval date, read from the provider at fetch time rather than
asserted by the pipeline (decision D1).

## Layout

```
lit/        WS0 audit: protocol.md, matrix.csv, references.bib, audit_report.md
data/raw/   untouched source files (gitignored; refetch with src/fetch_bulk.sh)
data/       SOURCES.md, generated provenance for every figure
data/processed/  built tables
src/        pipeline, one entry point (Makefile)
framework/  matrices, propositions
paper/      LaTeX source
notes/      decisions.md, findings.md, open_questions.md, sizing_method.md
```

## The public replication package

`scripts/make_replication_package.py` builds the public package outside this repository,
into `../labor-backing-replication/`, and `scripts/release_support.py` generates the
documentation, the checksums and the list of reported values that the package's harness
compares against. `scripts/release_scan.py` is the secrets and identity gate, run on the
built tree and on each archive variant. The static files the package ships, its Makefile,
its rebuild harness and its documentation, live in `release_assets/`.

Neither script modifies anything in this repository. The release directory is a separate
git repository with its own single initial commit and no shared history; the private
commit it was cut from is recorded in its `RELEASE_NOTES.md`.

```
python scripts/make_replication_package.py
python scripts/release_support.py
python scripts/release_scan.py --tree ../labor-backing-replication --allow-identity
```

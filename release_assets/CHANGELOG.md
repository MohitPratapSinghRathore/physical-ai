# Changelog

All notable changes to this package. The version is the package's, not the paper's.

## 1.0.0 - 2026-09-21

First public release, cut alongside the submitted manuscript.

### Added
- The pipeline that produces every number the paper reports: the accounts
  (`framework/labor_backing/`), the assembled capital tax rate (`framework/tau_k/`), the
  institution panel (`framework/institutions/`), the AI-side and bust modules
  (`framework/ai_bust/`), and the two revision rounds (`framework/revision_r1/`,
  `framework/revision_r2/`).
- `data/release/`, every measured artifact with its status, the claims register and
  `stated_limitations.csv`.
- A two-level rebuild: `make headline`, offline from shipped processed inputs, and
  `make all` from raw data.
- The rebuild specifications and the three rebuild reports, in `docs/rebuilds/`.
- Source extraction notes for the published tables read by hand, in
  `docs/source_extractions/`.
- `DATA_SOURCES.md` with publisher, identifier, vintage, access date, terms and SHA256 for
  every raw input, and `make verify` to check them.
- `DATA_DICTIONARY.md`, `METHODS_MAP.md`, `REBUILDS.md`, `AI_ASSISTANCE.md`,
  `THIRD_PARTY.md`.
- An anonymous and a named archive variant from one tree, `make anon` and `make named`.

### Not included
- The manuscript source. The package supports the paper; it does not ship it.
- Raw data, which stays under its publishers' terms.
- The files of expected values used to score the rebuild rounds, and the project's private
  working notes.

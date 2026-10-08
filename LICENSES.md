# Licensing

Three kinds of thing live here and they are licensed differently, which is the usual practice
for a repository holding both software and research output.

| What | Where | Licence |
|---|---|---|
| Software | `framework/`, `paper/`, `scripts/` | MIT, see [LICENSE](LICENSE) |
| Measured data artifacts | `data/release/`, `data/processed/` | CC BY 4.0 |
| Manuscripts and notes | `papers/`, `notes/`, the Markdown records | CC BY 4.0 |

Copyright 2026 Mohit Pratap Singh Rathore, Sriharsha Meduri, Gunveer Singh Kalsi and
Pratap Chandra Mandal. The authors retain copyright throughout.

## Why the split

Creative Commons licences are not written for source code and the Creative Commons organisation
advises against using them for it, so the code takes MIT. The data artifacts and the manuscripts
take CC BY 4.0, which matches the licence Preprints.org applies to posted preprints, so the
version of record and this repository carry the same terms rather than conflicting ones.

Full text of CC BY 4.0: https://creativecommons.org/licenses/by/4.0/legalcode
Summary: https://creativecommons.org/licenses/by/4.0/

In short, for the data and the manuscripts you may copy, redistribute, adapt and build on the
material for any purpose including commercially, provided you give appropriate credit, link to
the licence and indicate if changes were made.

## What is not ours to license

`data/raw/` is empty by design. The underlying survey and supervisory microdata, the Survey of
Income and Program Participation, the American Community Survey, the FDIC call reports and the
Federal Reserve financial accounts, come from the providers named in each paper's data section
under those providers' own terms. Nothing here grants any right over them. The artifacts in
`data/release/` are our processed outputs and are covered above.

Third-party figures quoted from published sources are cited in each paper's bibliography and
remain under their original terms; quoting them here is not a sublicence.

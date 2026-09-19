# Verified findings from the literature

Each entry records WHERE a finding was confirmed, precisely enough that another reader
can open the same document and the same section. Substantive wording is not reproduced
here; the finding is stated in this project's own words with the location given.

## Acemoglu and Restrepo (2020): the split of additional nonemployment

- Source: Daron Acemoglu and Pascual Restrepo, "Robots and Jobs: Evidence from US Labor
  Markets", Journal of Political Economy 128(6), 2188 to 2244, 2020.
- Copy consulted: `data/raw/manual/AcemogluRestrepo2020_JPE_robots_and_jobs.pdf`, 57 pages.
  This is the publisher's typeset version but carries placeholder folios ("000"), so the
  location below is given as the PDF page.
- Location: **Section V.C, "Other Labor Market Outcomes", PDF page 34**, discussing
  **appendix table A15**.
- Finding, in this project's words: robot exposure raises both the nonparticipation rate and
  the unemployment rate, and the estimates imply that of the additional nonemployed, about
  three quarters leave the labour force and about one quarter remain unemployed. The same
  section reports increased take-up of Social Security retirement and disability benefits
  and other government transfers (table A17), which is consistent with the participation
  margin doing the work.
- HORIZON, which matters for how this is used: the estimates are long differences over
  1990 to 2007, rescaled to a fourteen-year equivalent. This is a DECADE-PLUS adjustment,
  describing where displaced workers eventually settle, not what happens within a year or
  two of displacement.
- WHY IT WAS EARLIER RECORDED AS UNVERIFIED: the previous session searched NBER Working
  Paper 23285, the pre-publication version, which does not contain this passage or any of
  the relevant strings. The finding is present only in the published article. The earlier
  non-verification was correct about the document it searched and wrong about the claim.
- Used in: `src/unemployment_stock_flow.py` as the LONG-RUN exit variant, alongside the DWS
  exit share as the WITHIN-THREE-YEARS variant. The two are not interchangeable and both
  horizons are stated wherever either is used.

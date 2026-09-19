# Availability check: convergent validation data for S

Owner directed using free substitutes for IFR in a stated order. Availability confirmed
2026-09-19 before any build, as instructed. Nothing has been built on these yet.

---

## (1) Acemoglu and Restrepo, "Robots and Jobs" (JPE 2020) replication package

**BLOCKED from this environment.** openICPSR returns HTTP 403 to every request from here,
including search and project pages. This is the same class of block as BLS.

The package is not paywalled, so the owner can download it directly. What is needed from
it: commuting-zone robot exposure, and the industry-level robot penetration series built
from IFR. If the owner downloads it, drop it in `data/raw/robots/` and record the exact
file and version in `data/SOURCES.md`.

## (2) US Census, public and reachable

### ACES robotic equipment capital expenditures

- Landing page: https://www.census.gov/data/experimental-data-products/capital-expenditures-for-robotic-equipment.html
- Status: experimental data product. Robotic equipment capex collected for the first time
  in the 2018 ACES, split industrial and service robots, by industry.
- Years confirmed to exist from Census releases: 2018, 2019, 2021, 2022, and a 2024 release.
- Reference figures seen in Census releases, to be re-pulled from the tables rather than
  quoted from press releases: robotic equipment capex 7,524 USD mn in 2019, 0.7 percent of
  total equipment expenditures; manufacturing, retail trade and health care and social
  assistance together 87.3 percent of the total.
- `https://www.census.gov/programs-surveys/aces/data/tables.html` returns HTTP 200.

### ABS technology module

- 2019 ABS module, roughly 300,000 employer firms, reference period 2016 to 2018, covering
  adoption of AI, robotics, dedicated equipment, specialised software and cloud computing.
- `https://www.census.gov/programs-surveys/abs/data/tables.html` returns HTTP 200.
- `https://api.census.gov/data/2023/abscbo` returns HTTP 200, so the ABS API is reachable;
  the technology module endpoint and variable names still need confirming before use.

Both are industry-level (NAICS). S is occupational. Any test built on these is therefore
**convergent, not direct**, and requires an occupation-to-industry bridge (PUMS carries
both OCCP and INDP, so the bridge can be built internally with employment weights).

**Limitation to state in the paper, per owner instruction:** the validation of S is at
industry level while S itself is occupational, so it is a convergent test and not a direct
one. If a referee demands IFR, purchase at revision.

## (3) IFR figures reproduced in published papers

Last resort, with citation. Not pursued yet.

---

## What this does and does not buy

It can test whether S predicts where robots already are, at industry level. That is the
first external evidence of any kind for S, which currently has none (notes/paei_validation.md
Section 3).

It cannot resolve the Step 1 gate. That gate is about whether PAEI at c = 0 duplicates
Webb's robot score, and only Webb's scores answer it.

# Claims register

Every claim this project has made, its current status, the findings that produced it, and
which checks of the standing checklist it has passed. Maintained from the session that
introduced the checklist onward; earlier claims are back-filled from `notes/findings.md`.

No claim may be reported as a headline until it clears every applicable check. A claim that
clears some but not all is **provisional**, and the failing check must be named in the same
sentence wherever the claim appears.

## The checklist

| Code | Check | Applies to |
|---|---|---|
| **C1** | Run on BOTH cognitive indices, Felten AIOE and Eloundou GPT | any claim mentioning cognitive exposure |
| **C2** | Measured in BOTH ACS and SIPP | any claim about household obligations that both surveys carry |
| **C3** | Run on the working-household restricted sample (an employed member, reference person 25 to 64) | any claim about exposed households |
| **C4** | Reported RAW and ADJUSTED, with raw leading | any claim comparing groups |
| **C5** | Run at PUMA, county AND metro scale | any geographic claim |
| **C6** | Run through the household stress engine, not share attribution | any "at risk" dollar or household count |

`n/a` means the check does not apply. `no` means it has not been run and the claim is
provisional until it is.

## Status vocabulary

- **standing** clears every applicable check and is not contradicted
- **provisional** survives what has been run, with a named check outstanding
- **withdrawn** shown to be wrong or unsupported; must not be quoted
- **superseded** correct for its own definition but replaced by a better-specified version

---

## Core measurement claims

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | PAEI is a novel construct, not a relabelled cognitive index | standing | A10, A21 | yes | n/a | n/a | n/a | n/a | n/a |
| 2 | PAEI = P x S, multiplicative per Moravec | superseded | A10, A12 | n/a | n/a | n/a | n/a | n/a | n/a |
| 3 | S is largely a sector proxy and fails as an occupation-level construct | standing | A23, A27, A15 downgraded | n/a | n/a | n/a | yes | n/a | n/a |
| 4 | The S question is closed; S is demoted from the framework | standing (owner decision) | A27, Block 4 | n/a | n/a | n/a | n/a | n/a | n/a |
| 5 | Exposure is a range over c, not a single number | standing | A16 | n/a | n/a | n/a | n/a | n/a | n/a |
| 6 | Three substitution pathways (driving, gated, manipulation) partition embodied exposure | standing | A24, A18 | n/a | yes | yes | n/a | n/a | n/a |
| 7 | Most embodied wage bill at risk does NOT run through general-purpose manipulation | standing | A18, A24 | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | The A4 rubric is reliable and does not reproduce S_original | standing | A19 | n/a | n/a | n/a | n/a | n/a | n/a |
| 9 | c_today is not cleanly identified | standing (a limitation, stated) | A12, A16 | n/a | n/a | n/a | n/a | n/a | n/a |

## Concentration and household balance sheet

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 10 | Mortgage debt service is CONCENTRATED in high-exposure households | **withdrawn** | A4, A6 | n/a | n/a | n/a | yes | n/a | n/a |
| 11 | Mortgage debt service is close to PROPORTIONAL to the wage bill in aggregate, at every exposure level | standing | A5, A6, A29, A31, A36, A38 | yes | yes | yes | yes | n/a | n/a |
| 12 | That proportionality also holds at HOUSEHOLD level, so `at_risk = k x displaced_wage_bill` | **withdrawn** | A39 | yes | yes | yes | yes | n/a | yes |
| 13 | The mortgage channel is a cognitive-exposure channel | **withdrawn** | A35 claimed, A36 overturned | yes | no | yes | yes | n/a | n/a |
| 14 | Mortgage leans are indistinguishable across exposure types (0.89 to 0.93) | standing | A36, A38 | yes | no (SIPP disagrees, claim 16) | yes | yes | n/a | n/a |
| 15 | Rent leans embodied and away from cognitive by a factor of two | **provisional** | A36, A38 | yes (ratio is 2.0 AIOE, 1.55 GPT) | no (SIPP has no rent measure of this form) | yes | yes | n/a | n/a |
| 15a | Under the working-core restriction the embodied rent lean is 0.99, so the deviation is cognitive leaning AWAY from rent, not embodied leaning INTO it | standing | A38 | yes | n/a | yes | yes | n/a | n/a |
| 16 | ACS and SIPP agree on the embodied mortgage lean | **withdrawn** | A39 | yes | yes | yes | yes | n/a | n/a |
| 17 | Vehicle debt leans embodied (lean 1.38 against 0.79 and 0.85) and is the only obligation class where embodied over-holds | **provisional** | A39 | yes | no (ACS has no vehicle debt) | yes | no | n/a | no |
| 18 | Non-working households hold 19.7 percent of mortgage service and 30.1 percent of rent on 12.2 percent of the wage bill | standing | A38 | n/a | no | yes (as the complement) | yes | n/a | n/a |
| 19 | Vehicle debt generalises to all embodied exposure | **withdrawn** | A30 claimed, A31 overturned (manipulation is negative) | n/a | yes | yes | yes | n/a | n/a |
| 20 | High-PAEI households hold disproportionate consumer credit | **withdrawn** | A30 claimed, A31 overturned | n/a | yes | yes | yes | n/a | n/a |

## Geography

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 21 | Embodied work is near-uniform geographically | **withdrawn** | A28 claimed, A40 overturned (breadth artifact) | n/a | n/a | n/a | n/a | yes | n/a |
| 22 | Cognitive exposure is MORE geographically concentrated than embodied | **provisional, scale-dependent** | A37 refuted at PUMA, A40 confirms at county and metro | yes | n/a | n/a | n/a | yes | n/a |
| 23 | Embodied exposure is more concentrated, hence more diversifiable | **withdrawn** | A37 claimed, A40 overturned | n/a | n/a | n/a | n/a | yes | n/a |
| 24 | Embodied inequality is WITHIN metros, cognitive inequality is BETWEEN metros | **provisional** | A40 | no (AIOE only) | n/a | n/a | n/a | yes | n/a |
| 25 | Cognitive and embodied exposure correlate with local home values and wages with OPPOSITE signs | standing | A37 | yes | n/a | n/a | yes (placebo control) | partial (PUMA, county; no metro) | n/a |
| 26 | Neither exposure type is spatially random (Moran's I 0.44 to 0.54) | **provisional** | A40 | no (AIOE only) | n/a | n/a | n/a | no (county only) | n/a |
| 27 | Concentration falls monotonically with group breadth for both types | standing | A40 | no (AIOE only) | n/a | n/a | n/a | yes | n/a |
| 28 | The concentration of real exposure groups exceeds a breadth-matched random placebo | standing | A37, A40 | yes | n/a | n/a | yes | partial | n/a |

## Fiscal and P1r

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 29 | P1 as originally stated required s >= 2.55, a threshold | **withdrawn** | A33 (s <= 1 by construction, so unattainable not demanding) | n/a | n/a | n/a | n/a | n/a | n/a |
| 30 | P1r: the fiscal condition is near-unattainable under the current tax mix | standing | A33, A34 | n/a | n/a | n/a | n/a | n/a | n/a |
| 31 | The net fiscal position of displacement is about 674bn dollars | **withdrawn** | A33 (artifact, dominated by unverified outlays) | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | The fiscal channel is the largest of the channels measured | standing | A32, A34 | n/a | n/a | n/a | n/a | n/a | n/a |
| 33 | The fiscal loss per dollar displaced is 1.7 times larger for cognitive exposure, so this is NOT primarily a Physical AI channel | standing | A34 | yes | n/a | n/a | n/a | n/a | n/a |
| 34 | The labour-linked receipts share is 77.7 percent | **withdrawn** | A8 (overstated; denominator was wrong) | n/a | n/a | n/a | n/a | n/a | n/a |
| 35 | rho (reemployment share) is known | **not claimed** | blocked | n/a | n/a | n/a | n/a | n/a | n/a |

## Engine-based claims, opened this session

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 36 | Share-based attribution overstates or understates household distress by a large factor | **under test** | A41 (this session) | | | | | | |
| 37 | Within-group incidence (who loses the job) materially changes the distress result | **under test** | A41 | | | | | | |

---

## Standing constraints, for the record

These are owner decisions and are not claims. They are listed so no future session
relitigates them.

- No fabricated citations. Unverified goes to `lit/unverified.md`.
- No invented numbers. Every figure traces to `data/raw/` with a `data/SOURCES.md` entry.
- One-command rebuild.
- Report against the thesis first in every gate report.
- No em dashes or en dashes in any output.
- SEC access declares `team@oviguide.in`. Never spoof a browser user agent.
- Every cognitive-exposure claim states, in the same sentence or table note, that the index
  measures task overlap, not displacement or timing, and that top-quintile occupations
  include likely-augmented work.
- Raw dollar shares lead every stability claim; adjusted coefficients are secondary.
- Share-based attribution is retired. Every "at risk" number routes through the household
  stress engine (`src/stress/`).
- Pre-register hypotheses in `notes/` before running the analysis.

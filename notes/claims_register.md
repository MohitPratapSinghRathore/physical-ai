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
| **C3** | Run on the working-household restricted sample. DEFINITION as of the engine: the household contains at least one EMPLOYED MEMBER AGED 25 TO 64. The earlier definition (any employed member, plus a REFERENCE PERSON aged 25 to 64) is wrong for a displacement question and is superseded; findings A38 and earlier use it and are marked where it matters | any claim about exposed households |
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
| 12 | That proportionality also holds at HOUSEHOLD level, so `at_risk = k x displaced_wage_bill` | **withdrawn**, and replaced by the engine | A39, A42 | yes | yes | yes | yes | n/a | yes |
| 13 | The mortgage channel is a cognitive-exposure channel | **withdrawn** | A35 claimed, A36 overturned | yes | no | yes | yes | n/a | n/a |
| 14 | Mortgage leans are indistinguishable across exposure types UNCONDITIONALLY (0.80 to 0.95) and SEPARATE conditional on holding a mortgage (embodied 1.009, cognitive 0.845). Both halves must be stated together | standing, amended | A36, A38, A44, A47 | yes | yes | yes | yes | n/a | n/a |
| 14a | Cognitive households are more likely to hold a mortgage; conditional on holding one, embodied households carry more service per dollar earned. This is the mechanism behind claim 39 | standing | A44 | yes | no | yes | yes | n/a | n/a |
| 15 | Rent leans embodied and away from cognitive by a factor of two | **provisional** | A36, A38 | yes (ratio is 2.0 AIOE, 1.55 GPT) | no (SIPP has no rent measure of this form) | yes | yes | n/a | n/a |
| 15a | The embodied rent lean is 0.93 and the cognitive 0.47, so EVERY working class under-holds rent and cognitive households under-hold it about twice as much. The A38 reading of embodied as "exactly proportional" is withdrawn | standing | A38, corrected in A47 | yes | n/a | yes | yes | n/a | n/a |
| 16 | ACS and SIPP agree on the embodied mortgage lean | **withdrawn**, replaced by "ACS measures it, SIPP cannot" (Fay CI [0.565, 1.540]) | A39, A44 | yes | yes | yes | yes | n/a | n/a |
| 17 | Vehicle debt leans embodied (lean 1.38 against 0.79 and 0.85) and is the only obligation class where embodied over-holds | **provisional** | A39 | yes | no (ACS has no vehicle debt) | yes | no | n/a | no |
| 18 | Non-working households hold 19.7 percent of mortgage service and 30.1 percent of rent on 12.2 percent of the wage bill | **superseded** by claim 42 | A38, corrected in A47 | n/a | no | yes | yes | n/a | no |
| 19 | Vehicle debt generalises to all embodied exposure | **withdrawn** | A30 claimed, A31 overturned (manipulation is negative) | n/a | yes | yes | yes | n/a | n/a |
| 20 | High-PAEI households hold disproportionate consumer credit | **withdrawn** | A30 claimed, A31 overturned | n/a | yes | yes | yes | n/a | n/a |

## Geography

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 21 | Embodied work is near-uniform geographically | **withdrawn** | A28 claimed, A40 overturned (breadth artifact) | n/a | n/a | n/a | n/a | yes | n/a |
| 22 | Cognitive exposure is MORE geographically concentrated than embodied | **provisional, scale-dependent** | A37 refuted at PUMA, A40 confirms at county and metro | yes | n/a | n/a | n/a | yes | n/a |
| 23 | Embodied exposure is more concentrated, hence more diversifiable | **withdrawn** | A37 claimed, A40 overturned | n/a | n/a | n/a | n/a | yes | n/a |
| 24 | Embodied inequality is WITHIN metros, cognitive BETWEEN them | **withdrawn as stated** | A40 claimed, A46 overturned: both are 64 to 72 percent between-region, and embodied between-region inequality is 1.6 to 3.7 times LARGER in absolute terms | no (AIOE only) | n/a | n/a | n/a | yes | n/a |
| 25 | Cognitive and embodied exposure correlate with local home values and wages with OPPOSITE signs | standing | A37 | yes | n/a | n/a | yes (placebo control) | partial (PUMA, county; no metro) | n/a |
| 26 | Neither exposure type is spatially random (Moran's I 0.44 to 0.54) | **provisional** | A40 | no (AIOE only) | n/a | n/a | n/a | no (county only) | n/a |
| 27 | Concentration falls monotonically with group breadth for both types | standing | A40 | no (AIOE only) | n/a | n/a | n/a | yes | n/a |
| 28 | The concentration of real exposure groups exceeds a breadth-matched random placebo | standing | A37, A40 | yes | n/a | n/a | yes | partial | n/a |

## Fiscal and P1r

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 29 | P1 as originally stated required s >= 2.55, a threshold | **withdrawn** | A33 (s <= 1 by construction, so unattainable not demanding) | n/a | n/a | n/a | n/a | n/a | n/a |
| 30 | P1r: the fiscal condition is near-unattainable under the current tax mix | **amended** by A50: unattainable at tau_k = 0.05 and 0.10, attainable at tau_k = 0.21, so the claim must name tau_k | A33, A34, A50 | n/a | n/a | n/a | n/a | n/a | n/a |
| 31 | The net fiscal position of displacement is about 674bn dollars | **withdrawn** | A33 (artifact, dominated by unverified outlays) | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | The fiscal channel is the largest of the channels measured | standing | A32, A34 | n/a | n/a | n/a | n/a | n/a | n/a |
| 33 | The fiscal loss per dollar displaced is 1.7 times larger for cognitive exposure, so this is NOT primarily a Physical AI channel | standing | A34 | yes | n/a | n/a | n/a | n/a | n/a |
| 34 | The labour-linked receipts share is 77.7 percent | **withdrawn** | A8 (overstated; denominator was wrong) | n/a | n/a | n/a | n/a | n/a | n/a |
| 35 | rho (reemployment share) is known | **resolved, sourced** | A48, A49. rho = 0.6616, BLS DWS Table 1, January 2026 | n/a | n/a | n/a | n/a | n/a | n/a |
| 45 | omega = 0.9554 (full-time only, nominal), which pulls break-even down far enough that observed rho meets it in 12 of 27 cells | **withdrawn** | claimed last session, overturned in A48: it priced only full-time moves and used the nominal rather than counterfactual ratio | n/a | n/a | n/a | n/a | n/a | n/a |
| 46 | omega = 0.8598 blended and counterfactual-adjusted (range 0.8292 to 0.9076) is the value the fiscal condition needs | standing | A48 | n/a | n/a | n/a | yes | n/a | n/a |
| 47 | rho falls with labour slack: rho = 0.8090 - 0.0304 x unemployment rate, R-squared 0.812 on 14 DWS vintages, 2000 to 2026 | standing | A49 | n/a | n/a | n/a | n/a | n/a | n/a |
| 47a | That relationship may be extrapolated beyond 9.8 percent unemployment | **not claimed** | A49. 9.8 is the worst labour market in the sample and the line is not extended past it | n/a | n/a | n/a | n/a | n/a | n/a |
| 48 | Observed retained wage share R = rho x omega = 0.5689 at the 2026 survey; required R is 0.608 to 0.686 at tau_k = 0.10, so the condition is NOT met there | standing | A50 | n/a | n/a | n/a | yes | n/a | n/a |
| 49 | The P1r verdict is determined by tau_k, not by labour market absorption: tau_k = 0.21 passes in every cell at every omega including the switcher scenario, tau_k = 0.05 fails in every cell | standing | A50 | n/a | n/a | n/a | yes | n/a | n/a |
| 50 | In the tau_k = 0.10 column, 1 of 14 historical vintages met the condition (2000, the tightest labour market on record), and 0 of 14 in the central tau_l cell | standing | A50 | n/a | n/a | n/a | n/a | n/a | n/a |
| 51 | Occupation switchers lose 42 percent of earnings against 21 percent for stayers, both relative to a no-displacement counterfactual (Huckfeldt 2022, verified); AI displacement forces switching, so R falls to 0.3837 as a labelled scenario | standing as a SCENARIO | A51 | n/a | n/a | n/a | n/a | n/a | n/a |

## Engine-based claims, opened this session

| # | Claim | Status | Findings | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|---|
| 36 | Share-based attribution OVERSTATES the distress-relevant obligation by about five times at DSTI 50 (ratio 0.185 to 0.219, mean 0.205) and about three and a third times at DSTI 30 | standing | A42 | yes | no (ACS only) | yes | n/a | n/a | yes |
| 36a | The overstatement is near-uniform across constructs and scenario sizes, so share-attributed RANKINGS hold and LEVELS do not | standing | A42 | yes | no | yes | n/a | n/a | yes |
| 37 | Within-group incidence materially changes the distress result | **split** | A42 | yes | no | yes | n/a | n/a | yes |
| 37a | On HOUSEHOLD COUNTS incidence changes the result by only 5 to 9 percent | standing | A41, A42 | yes | no | yes | n/a | n/a | yes |
| 37b | On DOLLARS incidence changes the result by 1.75 to 3.01 times, so no dollar figure may be quoted without naming the incidence assumption | standing | A42 | yes | no | yes | n/a | n/a | yes |
| 37c | Displacement concentrated on low earners within an occupation would cause share attribution to UNDERSTATE the damage by a large multiple | **withdrawn** | A39 claimed, A42 overturned (direction is reversed: it overstates, and overstates more) | yes | no | yes | n/a | n/a | yes |
| 38 | A 10 percent displacement shock raises the share of obligated working-core households above DSTI 50 by 2.35pp (cognitive AIOE) or 1.92pp (embodied), from a baseline of 10.08 percent | standing | A41 | yes | yes (SIPP increments agree to within 0.2pp) | yes | n/a | n/a | yes |
| 39 | Embodied displacement is about 1.8 times more distress-efficient than cognitive displacement per dollar of wage income destroyed; manipulation is 2.4 times | standing | A41, A44 | yes | yes (SIPP runway 5.01 against 4.06 percent, Fay intervals do not overlap) | yes | n/a | n/a | yes |
| 40 | rho (reemployment) moves the headline by a factor of about 2.2 and dominates omega, so it is the binding unknown | standing | A41 | yes | n/a | yes | n/a | n/a | yes |
| 41 | The driving channel is capped at 3.29 percent of employment, so its entire ceiling is +0.67pp of DSTI-50 crossings | standing | A41 | n/a | n/a | yes | n/a | n/a | yes |
| 42 | Non-working households hold 16.0 percent of mortgage service and 27.3 percent of rent, and 38.9 percent of those with an obligation are already above DSTI 50 | standing | A41, A43 | n/a | no | yes (as the complement) | yes | n/a | yes |
| 43 | Leg A (bank channel, 450bn USD committed) is about 2.1 percent of Leg W (21.38tn USD household debt), so the two-sided framing is not symmetric in size | **provisional, lower bound** | A45 | n/a | n/a | n/a | n/a | n/a | n/a |
| 44 | A38's table was wrong on four counts (vacant units, a wider employed test, two weight systems, a reference-person-age working core), and its DOLLAR shares do not stand either | standing | A47 | yes | n/a | yes | yes | n/a | n/a |

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

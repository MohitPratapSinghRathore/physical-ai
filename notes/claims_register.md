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

## Replication status, a SEPARATE flag added 2026-09-20

Status above says whether this project's own checks have been cleared. The flag below says
whether an INSTANCE THAT DID NOT WRITE THE CODE rebuilt the quantity from raw data and the
brief alone. The two are independent and a claim carries both.

- **R-replicated** rebuilt independently and inside tolerance in round one
- **R-confirmed-direction** the magnitude was not matched but the DIRECTIONAL claim was
  independently confirmed
- **R-failed** rebuilt independently and OUTSIDE tolerance because THIS PROJECT was wrong
- **R-unattempted** the replicator could not attempt it, in every case because the brief did
  not contain enough to rebuild it
- **R-pending-2** queued for round two against `notes/replication_brief_v2.md` and
  `notes/sealed/sealed_expected_values_round2.json`
- **R-notapplicable** not a sealed quantity

**Nothing in this project may be described as independently replicated unless it carries
R-replicated or R-confirmed-direction.** Round one attempted 51 quantities and matched 21.
The full accounting is in `notes/replication/round1_mismatch_classification.md`.

## Promotion pass log

**2026-09-19.** Independent recomputation run in `src/verify/independent_recompute.py`, a
fresh script that imports nothing from `src/` and reads raw files and retyped published
figures only. **Sixteen headline quantities recomputed, sixteen matched within tolerance,
zero failed.**

Promoted to standing on that evidence: claims 43, 46, 48, 52, 53 and 79.

Still provisional after the pass, with the reason:

| Claim | Reason |
|---|---|
| 15, 17 | C2 outstanding: the rent and vehicle leans have not been cross-checked on the second dataset |
| 26 | C1 and C5 outstanding: Moran's I is Felten AIOE only and county only |
| 96, 98 | C2 outstanding: the incidence result is SIPP only. ACS replication is item 2 of this session |
| 101a, 101b, 101c | Produced THIS session (A72); the same-session rule applies |
| Others | Derived quantities that rest on the promoted six but were not themselves independently recomputed. They are eligible next pass |

**Blocked from promotion by rule 5** until rerun on the current method: anything resting on
share-based attribution, on the DSTI threshold as headline, or on the unemployment-rate slack
measure.

## Reporting rule, in force from 2026-09-19

**Any figure sourced or derived in the current session is PROVISIONAL until it has cleared
the checklist in a LATER pass.** A result cannot be promoted to standing in the same session
that produced it, because the checks that matter most (a second survey, a second index, a
second scale) have usually not been run yet and because this project has repeatedly found
first-session numbers to be wrong in ways only a later pass caught: A35, A38, A39 and the
omega of 0.9554 were all reported as settled and all were overturned.

Every gate report separates **standing** from **provisional** explicitly and never mixes
them in the same list.

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
| 30 | P1r: the fiscal condition has TWO levers, R and tau_k. Within the omega range tau_k decides the verdict; across the historical rho range (0.49 to 0.74) R moves by 0.215, which is decisive near tau_k = 0.10. Both must be stated | **standing**, amended in A52 | A33, A34, A50, A52 | n/a | n/a | n/a | n/a | n/a | n/a |
| 31 | The net fiscal position of displacement is about 674bn dollars | **withdrawn** | A33 (artifact, dominated by unverified outlays) | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | The fiscal channel is the largest of the channels measured | standing | A32, A34 | n/a | n/a | n/a | n/a | n/a | n/a |
| 33 | The fiscal loss per dollar displaced is 1.7 times larger for cognitive exposure, so this is NOT primarily a Physical AI channel | standing | A34 | yes | n/a | n/a | n/a | n/a | n/a |
| 34 | The labour-linked receipts share is 77.7 percent | **withdrawn** | A8 (overstated; denominator was wrong) | n/a | n/a | n/a | n/a | n/a | n/a |
| 35 | rho (reemployment share) is known | **standing**, resolved and sourced | A48, A49. rho = 0.6616, BLS DWS Table 1, January 2026 | n/a | n/a | n/a | n/a | n/a | n/a |
| 45 | omega = 0.9554 (full-time only, nominal), which pulls break-even down far enough that observed rho meets it in 12 of 27 cells | **withdrawn** | claimed last session, overturned in A48: it priced only full-time moves and used the nominal rather than counterfactual ratio | n/a | n/a | n/a | n/a | n/a | n/a |
| 46 | omega = 0.8598 blended and counterfactual-adjusted (range 0.8292 to 0.9076) is the value the fiscal condition needs | **standing**, promoted: independent recomputation MATCH (omega counterfactual 0.85977 against 0.8598) | A48 | n/a | n/a | n/a | yes | n/a | n/a |
| 47 | rho falls with labour slack: rho = 0.8090 - 0.0304 x unemployment rate, R-squared 0.812 on 14 DWS vintages, 2000 to 2026 | **standing**, cleared a second pass and is load-bearing in A56 and A58 | A49 | n/a | n/a | n/a | n/a | n/a | n/a |
| 47a | That relationship may be extrapolated beyond 9.8 percent unemployment | **not claimed** | A49. 9.8 is the worst labour market in the sample and the line is not extended past it | n/a | n/a | n/a | n/a | n/a | n/a |
| 48 | Observed retained wage share R = rho x omega = 0.5689 at the 2026 survey; required R is 0.608 to 0.686 at tau_k = 0.10, so the condition is NOT met there | **standing**, promoted: independent recomputation MATCH (R = 0.56878 against 0.5683) | A50 | n/a | n/a | n/a | yes | n/a | n/a |
| 49 | Within the OMEGA range alone, tau_k decides the verdict: tau_k = 0.21 passes in every cell at every omega including the switcher scenario, tau_k = 0.05 fails in every cell. This does NOT make the condition independent of the labour market, because rho varies far more than omega does | **provisional**, corrected framing in A52 | A50, A52 | n/a | n/a | n/a | yes | n/a | n/a |
| 50 | In the tau_k = 0.10 column, 1 of 14 historical vintages met the condition (2000, the tightest labour market on record), and 0 of 14 in the central tau_l cell | **provisional**, sourced this session | A50 | n/a | n/a | n/a | n/a | n/a | n/a |
| 51 | Occupation switchers lose 42 percent of earnings against 21 percent for stayers, both relative to a no-displacement counterfactual (Huckfeldt 2022, verified); AI displacement forces switching, so R falls to 0.3837 as a labelled scenario | standing as a SCENARIO | A51 | n/a | n/a | n/a | n/a | n/a | n/a |
| 52 | tau_k is decomposable: tau_k = sigma_rent x (domestic share x 0.21) + (1 - sigma_rent) x tau_normal, and the project's 0.05/0.10/0.21 grid is AMR's own effective-rate series on software and equipment | **standing**, promoted: independent recomputation MATCH (sigma_rent 0.35065, tau_k 0.07076) | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 53 | Under the current tax code WITH profit shifting, implied tau_k = 0.0708, below the 0.1101 needed at R = 0.5683, so the fiscal condition fails | **standing**, promoted: independent recomputation MATCH (tau_k 0.07076 against 0.0708; required 0.10996 against 0.1101) | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 54 | Profit shifting alone is enough to push tau_k below break-even: closed economy at 2010s rates gives 0.1386 against 0.1101 needed, applying the verified 48 percent haven share drops it to 0.1032 | **provisional**, sourced this session | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 55 | Raising the rent share does not rescue the condition under profit shifting, because a larger rent share puts more surplus into the shifted component | **provisional** | A53 | n/a | n/a | n/a | n/a | n/a | n/a |
| 56 | Of the additional nonemployed from robot exposure, about three quarters leave the labour force and one quarter remain unemployed | **standing**, VERIFIED, in the published JPE article, Section V.C, PDF page 34, table A15. Used as the LONG-RUN (decade-plus) variant only | A54 corrected, A55 | n/a | n/a | n/a | n/a | n/a | n/a |
| 56a | The DWS exit share (0.296 to 0.643, falling with slack) and the Acemoglu-Restrepo three-quarters split describe DIFFERENT HORIZONS and are not interchangeable: within three years of displacement against a fourteen-year adjustment | **provisional** | A55 | n/a | n/a | n/a | n/a | n/a | n/a |
| 57 | The labour force exit share FALLS with slack | **DOWNGRADED** by A63: the R-squared 0.777 fit was partly mechanical, since exit share and the unemployment rate share the component U. On nonemployment it is R-squared 0.137, t = -1.13, not significant. The LEVEL and range 0.296 to 0.643 stand; the slack dependence does not | A54 | n/a | n/a | n/a | n/a | n/a | n/a |
| 58 | At 10 percent displacement, implied unemployment is 6.47 percent and rho falls to 0.612, inside the observed data range | **provisional** | A54 | n/a | n/a | n/a | n/a | n/a | yes |
| 59 | The displacement-to-slack mapping is estimable only to about 14 to 15 percent displacement, where implied unemployment reaches the worst labour market in the sample | standing (a limitation) | A54 | n/a | n/a | n/a | n/a | n/a | n/a |
| 60 | The static displacement-to-slack fixed point (A54) OVERSTATES slack, because it treats a decade of adoption as instantaneous: 10 percent over 10 years gives u = 4.84 and rho = 0.662, not u = 6.47 and rho = 0.612 | **provisional**, this session | A56 | n/a | n/a | n/a | n/a | n/a | yes |
| 61 | (superseded by the amended row below) | **superseded** | A56, A61 | n/a | n/a | n/a | n/a | n/a | yes |
| 62 | Half of US employment can be displaced over 20 years without leaving the observed labour market range (2.5 percent a year, u = 7.7) | **provisional** | A56 | n/a | n/a | n/a | n/a | n/a | yes |
| 63 | The speed limit is about 3.15 percent of employment a year (range 2.50 to 4.35 on the hazard conversion; 5.35 to 8.30 under the long-run exit variant), above which the model leaves the range its hazards were fitted on | **provisional** | A56 | n/a | n/a | n/a | n/a | n/a | yes |
| 64 | The rent share is not a range but a disagreement: Barkai 0.351 against Karabarbounis and Neiman Case R at approximately 0, two incompatible readings of one residual that must not be averaged | **provisional**, both verified | A57 | n/a | n/a | n/a | yes | n/a | n/a |
| 65 | NO post-2017 cell passes the fiscal condition at any labour tax rate, rent share or shifting assumption, including the closed economy: the maximum obtainable tau_k is 0.1062 against a minimum requirement of 0.1101 | **provisional**, and the most robust fiscal result the project has | A57 | n/a | n/a | n/a | yes | n/a | n/a |
| 66 | The US crossed from meeting to not meeting the condition somewhere between 2008 and 2022; the date is NOT robust to the rent share or the labour tax rate | **provisional** | A58 | n/a | n/a | n/a | yes | n/a | n/a |
| 67 | 2010 failed on R alone (tau_k unchanged, rho fell to 0.49) and 2018 failed on tau_k alone (R unchanged, tau_k fell 45 percent). Each lever has independently decided the answer once in the observed record | **provisional** | A58 | n/a | n/a | n/a | n/a | n/a | n/a |
| 68 | Full immediate expensing is in force in 2026: 168(k)(1)(A) gives 100 percent and the phase-down in 168(k)(6) is repealed by Pub. L. 119-21 sec. 70301(b)(1)(B), July 4 2025. AMR's 0.05 is correct for 2026 | **provisional**, verified against the statute | A59 | n/a | n/a | n/a | n/a | n/a | n/a |
| 69 | Exactly one post-2017 cell is within 0.01 of passing (Barkai rent share, closed economy, tau_l 0.255, margin -0.0039); it flips at rho = 0.679, which is attainable. Every other cell needs rho >= 0.75, never observed | **provisional** | A60 | n/a | n/a | n/a | yes | n/a | n/a |
| 70 | With any outlay response (g >= 0.10) no cell is within 0.037 of passing | **provisional** | A60 | n/a | n/a | n/a | n/a | n/a | n/a |
| 71 | A56's 3.15 percent speed limit is the phi = 0 corner and is an UPPER BOUND; at phi = 1 over 20 years it is 1.80 percent | **provisional** | A61 | n/a | n/a | n/a | n/a | n/a | yes |
| 61 | The binding variable is the ANNUAL FLOW, not cumulative displacement | **superseded**, amended by A61: true only at phi = 0. For any phi above zero a cumulative ceiling of 36 to 61 percent also binds | A56, A61 | n/a | n/a | n/a | n/a | n/a | yes |
| 72 | Under the tight capital-formation cap (0.498 percent a year), displacing half the exposed embodied wage bill is physically unattainable at ANY horizon, so every fast scenario is cognitive-led | **provisional** | A62 | n/a | n/a | n/a | n/a | n/a | yes |
| 73 | Displacing 90 percent of the exposed embodied wage bill over 20 years raises unemployment to 5.11 percent against a 4.32 baseline | **provisional** | A62 | yes | n/a | n/a | n/a | n/a | yes |
| 74 | The size-driven (fiscal) failure mode fails in EVERY scenario including the mildest, because the condition already fails at zero displacement | **provisional**, and nearly tautological, flagged in the prereg before running | A62, A57, A58 | yes | n/a | n/a | n/a | n/a | yes |
| 75 | The speed-driven channel ACCELERATES with the displacement flow, producing a threshold | **SUPPORTED**, A62 refutation WITHDRAWN | A63: A62's negative curvature was an artifact of a circular hazard. On prime-age nonemployment the acceleration ratio is 2.33 to 2.63 on E/P, 1.75 to 2.03 on wage income, 2.39 to 2.59 on unemployment, R-squared 0.999 | yes | n/a | n/a | n/a | n/a | yes |
| 76 | The speed limit is 1.25 percent a year at a 10-year horizon (1.10 at phi = 1), two and a half times tighter than A56's 3.15 | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 77 | The cumulative ceiling is 11 to 12.5 percent of employment at 10 years, against A61's 31.5, and no 20-year path stays inside the observed range at any flow in the grid | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 78 | The FAST regime is nearly empty on the corrected slack measure: of 120 scenario paths, 58 SLOW, 62 SUDDEN, 0 FAST | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 79 | Attrition absorption is EXACTLY NEUTRAL for prime-age E/P, unemployment, wage income and the speed limit. It transfers the whole burden from laid-off incumbents to lost entrant openings | **standing**, promoted: verified ALGEBRAICALLY as an identity, not by simulation: with symmetric treatment total inflow is JD regardless of alpha | A64 | n/a | n/a | n/a | n/a | n/a | yes |
| 80 | Displacement delivered through attrition is invisible to the Displaced Worker Survey and to every indicator in this project's dashboard, while employment to population falls by the same amount as under mass layoffs | **provisional** | A64 | n/a | n/a | n/a | n/a | n/a | yes |
| 81 | The natural separation rate is 3.4x (labour force exit) to 7.9x (total separations) the speed limit | standing, sourced from BLS Employment Projections | A64 | n/a | n/a | n/a | n/a | n/a | n/a |
| 82 | No 20-year path stays inside the observed range at any alpha, phi, flow or ceiling | **provisional** | A64 | n/a | n/a | n/a | n/a | n/a | yes |
| 83 | The speed limit is not a number: 0.05 to 7.15 percent a year on the prime-age specification, median 2.73. The SLACK MEASURE moves it more than every other choice combined (ratio 3.67); attrition moves it by exactly 1.00 | **provisional** | A65 | n/a | n/a | n/a | n/a | n/a | yes |
| 84 | Acceleration is a structural property of any model in which the reemployment hazard falls with slack; the data identify its strength only inside the observed range | standing (a statement about the model class) | A65 | n/a | n/a | n/a | n/a | n/a | n/a |
| 85 | No published work links occupational AI exposure to household balance-sheet outcomes (none located, non-systematic search) | **provisional** | A66 | n/a | n/a | n/a | n/a | n/a | n/a |
| 86 | Acemoglu-Restrepo's increased benefit take-up and falling E/P in exposed areas are settled | **NOT SETTLED** | A66: Altindag, El Cheikh Taha, Nunley and Seals (2026) find SSDI applications FALLING and E/P NOT falling in exposed commuting zones. Different designs, but close enough that the take-up result cannot be leaned on | n/a | n/a | n/a | n/a | n/a | n/a |
| 87 | phi has independent empirical support: Fan (2025) estimates mobility recovers about 20 percent of losses against 30 percent in standard models, implying phi of about 0.33 | **provisional**, verified | A66 | n/a | n/a | n/a | n/a | n/a | n/a |
| 88 | The Fed's 2026 severely adverse scenario (u to 10 percent, house prices -30, CRE -39) produces a 1.5 percent loss rate on first-lien mortgages and a 1.6pp fall in aggregate CET1 | standing, read from the source | A67 | n/a | n/a | n/a | n/a | n/a | n/a |
| 89 | A displacement story routed through mortgages is routed through the most loss-resistant asset on the bank balance sheet: 1.5 percent against 17.1 for credit cards and 9.0 for C and I | **provisional** | A67 | n/a | n/a | n/a | n/a | n/a | n/a |
| 90 | Within-household correlated displacement is SUPERADDITIVE but not double: both earners unemployed gives more than +8pp of default probability against +5pp for one | standing, Gerardi et al. | A67 | n/a | n/a | n/a | n/a | n/a | n/a |
| 91 | Job loss is equivalent to a 35 percent equity decline for default, so a job loss is slightly more potent than the entire severely adverse house price shock | standing, Gerardi et al. | A67 | n/a | n/a | n/a | n/a | n/a | n/a |
| 92 | This project's DSTI engine captures at most a third of the default mechanism: only 30 percent of defaulters would have to go below subsistence to stay current, and 38 percent could pay without cutting consumption | **provisional**, a limitation of A41 | A67 | n/a | n/a | yes | n/a | n/a | yes |
| 93 | The entry-level attrition channel is already measured and operating: employment of 22 to 25 year olds in AI-exposed occupations is 19 percent below counterfactual and widening, operating through REDUCED HIRING not separations | standing, Brynjolfsson, Chandar and Chen (2026) | A68 | yes | n/a | n/a | n/a | n/a | n/a |
| 94 | A64's blind-spot deduction is confirmed by independent data | standing | A68 | n/a | n/a | n/a | n/a | n/a | n/a |
| 95 | The channel already operating is the one this project's household engine measures WORST, because 22 to 25 year olds mostly do not hold mortgages | **provisional** | A68 | n/a | n/a | n/a | n/a | n/a | yes |
| 96 | Attrition absorption cuts MORTGAGE exposure at default sharply (17.15 to 11.72bn, -32 percent) and raises STUDENT debt exposure (1.99 to 2.73bn, +37 percent) | **provisional**, prereg confirmed | A69 | yes | no (SIPP only) | yes | n/a | n/a | yes |
| 97 | Attrition absorption cuts AUTO stress | **REFUTED** | A69: vehicle exposure RISES 21 percent (1.12 to 1.35bn). Young-adult households hold vehicle debt at the same rate as incumbents, so auto is not an incumbent asset the way mortgages are | yes | no | yes | n/a | n/a | yes |
| 98 | The entrant channel concentrates harm: the same total employment loss gives almost the same number of extra defaults at a 4.5x higher per-household uplift, implying a 42.7 percent hit rate on young exposed households | **provisional** | A69 | yes | no | yes | n/a | n/a | yes |
| 99 | Aggregate neutrality of attrition (A64, A65) does NOT imply incidence neutrality; only the first claim holds | standing | A69 | n/a | n/a | n/a | n/a | n/a | yes |
| 100 | The fiscal loss is identical across incidence cases by construction, because it depends on the displaced wage bill and R, not on who was displaced | standing | A70 | n/a | n/a | n/a | n/a | n/a | yes |
| 101 | The HORIZON does almost all the work in the fiscal channel: a thirty-fold difference for the same cumulative displacement | **WITHDRAWN** | A70 claimed it, A72 overturned it. The comparison was an artifact of amortising a stock as a flow. Terminal-year loss is nearly horizon-invariant (3.2-fold for both types, 2.1-fold for cognitive AIOE), and that residual is the labour model, not the fiscal arithmetic | yes | n/a | n/a | n/a | n/a | yes |
| 101a | Terminal-year annual revenue loss runs 0.00 to 18.75 percent of federal receipts; cumulative loss 8 to 3,727bn; present value at 3 percent 8 to 2,514bn | **provisional** | A72 | yes | n/a | n/a | n/a | n/a | yes |
| 101b | A slow transition is MORE expensive fiscally, not less: cumulative loss rises with horizon (both types at 90 percent: 1,682bn over 2 years against 3,727bn over 20) because the loss accrues for longer | **provisional** | A72 | yes | n/a | n/a | n/a | n/a | yes |
| 101c | At 90 percent of both exposure types the terminal-year loss reaches 26.8 to 84.7 percent of OASDI payroll income, against a fund already running a 160.2bn deficit | **provisional** | A72, A32 | yes | n/a | n/a | n/a | n/a | yes |
| 104 | Sixteen headline quantities recomputed independently from raw inputs, in a script importing nothing from src/, all matched within tolerance | standing | A73 | n/a | n/a | n/a | n/a | n/a | n/a |
| 105 | A slower transition LOWERS labour market and household stress and RAISES cumulative fiscal cost; no horizon minimises both | **provisional** | A73, A56, A72 | yes | n/a | n/a | n/a | n/a | yes |
| 106 | Holding R at its terminal value along the path changes the cumulative fiscal loss by -11.0 to +6.9 percent, so the simplification is bounded and retained | **provisional** | A73 | n/a | n/a | n/a | n/a | n/a | yes |
| 107 | Every scenario stated as a share of EXPOSED wage bill was not comparable across constructs: 90 percent of exposed is 12.3 percent of the total wage bill for embodied and 33.0 for both types. Majority displacement was never reachable in the old grid | standing | A74 | yes | n/a | n/a | n/a | n/a | n/a |
| 108 | The extended grid reaches 83.7 percent of the total wage bill, so majority displacement is now expressible; broadening makes it expressible, not safe | standing | A74 | yes | n/a | n/a | n/a | n/a | n/a |
| 109 | ORDER OF STRESS: public budget first (about 10 percent of the total wage bill), then mortgage holders, student loan holders and trust funds (25 percent), then auto lenders (50 percent); cards never cross | **provisional**, A75 version WITHDRAWN | A76 | yes | no (SIPP only) | yes | n/a | n/a | yes |
| 110 | At 75 percent of the total wage bill, bank-held mortgage losses are 92 to 147 percent of the Fed severely adverse first-lien loss | **provisional**, A75 version WITHDRAWN (it was 21.7x too small) | A76 | yes | no | yes | n/a | n/a | yes |
| 111 | Registered expectation that household distress follows in the fast regime | **CONFIRMED after correction** | A76: refuted only under A75's faulty conversion. Corrected, mortgage and student sheets cross at 25 percent of the wage bill | yes | no | yes | n/a | n/a | yes |
| 112 | Registered expectation that the double trigger reaches bank-held mortgages in the sudden regime | **standing**, tested and confirmed by the second-round module | A76, A91: the double trigger does reach bank-held mortgages, but in the SECOND-round column it reaches them at a 10 percent dose, far earlier than registered, and 92 percent of the loss at large doses comes from demand rather than from displaced borrowers' own loans | yes | no | yes | n/a | n/a | yes |
| 113 | Losses computed as exposure at default times a PORTFOLIO loss rate understate by a factor of about 22, because the probability of default is applied twice | standing, arithmetic | A76 | n/a | n/a | n/a | n/a | n/a | n/a |
| 114 | SIPP under-reports card and auto balances relative to the credit panel: the implied bank share exceeds 1.0 for both | standing | A76 | n/a | yes | yes | n/a | n/a | n/a |
| 115 | On the extended axis the 10 percent cell is the only one fully inside the data: terminal loss 1.79 percent of federal receipts and 4.21 percent of OASDI payroll income | **provisional**, OASDI figure corrected in A79 | A77, A79 | yes | n/a | n/a | n/a | n/a | yes |
| 116 | At 50 percent of the wage bill and above the fiscal loss exceeds OASDI payroll income entirely and rho falls to zero; these are extrapolations, not estimates | standing (a limitation) | A77 | yes | n/a | n/a | n/a | n/a | yes |
| 117 | Every household-engine result is a LOWER BOUND on bank losses: it holds house prices, consumer demand, business revenue and non-displaced employment fixed, while the Fed's 708bn is economy-wide | standing | A78 | n/a | n/a | n/a | n/a | n/a | yes |
| 118 | PLAUSIBILITY RULE in force: 32 retroactive checks found 4 violations, all now corrected | standing | A79 | n/a | n/a | n/a | n/a | n/a | n/a |
| 119 | A77's OASDI and HI loss shares (up to 214.8 and 676.4 percent) violated the bound that a loss on a tax cannot exceed the tax | **WITHDRAWN** | A79: they divided a general revenue loss by a payroll-only denominator | n/a | n/a | n/a | n/a | n/a | n/a |
| 120 | Corrected trust fund loss is 4.2 percent of fund payroll income at 10 percent of the wage bill and 11.9 at 25 percent; maximum across the grid 76.5 percent, bound respected | **provisional** | A79 | yes | n/a | n/a | n/a | n/a | yes |
| 121 | Cognitive displacement is partly shielded from OASDI by the earnings cap and embodied displacement is not: 81.2 percent of the cognitive wage bill is under the cap against 97.7 percent of the embodied | **provisional**, new exposure-type contrast | A79 | yes | n/a | n/a | n/a | n/a | n/a |
| 122 | Cards cross at 75 percent of the wage bill | **SUPERSEDED** | A83: A80's 3.40x scaling conflated under-reporting with coverage. At the corrected 2.52x, cards cross only at the TIGHT threshold and are one of the eleven fragile comparisons that must not be ranked | yes | no | yes | n/a | n/a | yes |
| 123 | The ORDERING of the order of stress has survived three magnitude errors | **WITHDRAWN** | A82: it does not survive a properly sourced threshold. The ordering is NOT invariant across tightness levels; only 4 of 15 pairwise comparisons hold | yes | no | yes | n/a | n/a | yes |
| 124 | The public budget crosses first in the order of stress | **WITHDRAWN** | A82: mortgage holders cross first at every tightness level. The earlier result came from comparing a 25 percent bank threshold with an unjustified 1 percent of receipts | yes | no | yes | n/a | n/a | yes |
| 125 | Four pairwise comparisons are robust across all three threshold tightness levels: mortgage before public budget, before student loans, before trust funds; and public budget before student loans. The other eleven are fragile and are not ranked | **provisional** | A82 | yes | no | yes | n/a | n/a | yes |
| 126 | SIPP under-reports credit card balances by a factor of 2.5 against the revolving credit aggregate, the largest survey gap in the project | standing | A83 | n/a | yes | yes | n/a | n/a | n/a |
| 127 | A80's scaling factors conflated survey under-reporting with sample coverage and were 14 to 26 percent too large | standing | A83 | n/a | yes | yes | n/a | n/a | n/a |
| 128 | Embodied displacement costs OASDI 17 to 20 percent more per displaced wage dollar than cognitive AIOE displacement | **DOWNGRADED**, arithmetic retained and interpretation withdrawn | A84, downgraded by A87: reweighting to a common wage distribution removes 54 to 99 percent of the gap and reverses its sign in SIPP against Eloundou GPT. The two groups do differ as described; the difference is about pay, not exposure type | yes | yes | yes | n/a | n/a | n/a |
| 129 | The fiscal and household exposure-type contrasts have the SAME driver, that embodied work is lower paid | **standing**, and stronger than registered: pay is not merely the shared driver, it is essentially the whole of both contrasts | A84, A41, A87 | yes | yes | yes | n/a | n/a | yes |
| 130 | Ranking balance sheets by threshold crossing is not a meaningful exercise, because each sheet is measured against a different yardstick; the dose-response table replaces it | **standing**, method decision following A82's sensitivity result | A85 | n/a | n/a | yes | n/a | n/a | yes |
| 131 | Every balance sheet in the dose-response table has a stated and sourced absorbing capacity: bank CET1 above the 4.5 percent minimum 1,044.4bn, the 708bn absorbed in the 2026 test, GSE net worth 190.4bn, federal receipts 5,926.6bn, OASDI payroll income 1,323.2bn, HI payroll income 286.2bn | **standing** | A85 | n/a | n/a | yes | yes | n/a | yes |
| 132 | Trust fund RESERVES could not be sourced; SSA.gov returns 403 and no FRED series carries the balance, so the reserve denominator is left empty rather than estimated | **standing**, a blocked-source record | A85 | n/a | n/a | n/a | n/a | n/a | n/a |
| 133 | Agency mortgage is the only private sheet that gets large in the first round, reaching 41 percent of combined GSE net worth at a 25 percent cognitive dose and 78 percent at 50 percent, because of holder structure rather than borrower behaviour | **provisional** | A85 | yes | no (ACS and SIPP balances, one holder-share proxy) | yes | n/a | n/a | yes |
| 134 | Bank capital is never the binding constraint in the first round: the largest bank-held loss anywhere in the grid is 5.1 percent of the CET1 surplus | **provisional**, and conditional on the first-round scope in A78 | A85 | yes | no | yes | n/a | n/a | yes |
| 135 | Only the 5 and 10 percent doses are fully inside the observed data range for every exposure type; at 25 percent the embodied rows are already outside | **standing** | A85 | yes | n/a | yes | n/a | n/a | yes |
| 136 | No single exposure type can deliver a 75 percent dose: embodied saturates at 33.7 percent of the total wage bill, cognitive AIOE at 47.4 and cognitive GPT at 53.6. Only the union of both types reaches it | **standing** | A85 | yes | n/a | yes | n/a | n/a | yes |
| 137 | A80's scaling factor is exactly the under-reporting factor divided by the working-core coverage share, reproducing A80's numbers to three decimals | **standing**, an identity | A86 | n/a | n/a | yes | n/a | n/a | n/a |
| 138 | The corrected factors cut every credit row by a constant proportion within each loan: mortgage 18.0 percent, card 26.0, auto 22.6, student 11.7 | **standing** | A86 | n/a | yes | yes | n/a | n/a | yes |
| 139 | NEITHER exposure-type contrast survives controlling for pay. Between 1.0 and 11.4 percent of the raw gap remains at the weaker end of the reweighting, and the SIPP Eloundou GPT cap contrast reverses sign | **standing**, and it is the strongest thesis-weakening result of the session | A87 | yes | yes (ACS and SIPP, both indices) | yes | n/a | n/a | yes |
| 140 | The paper's statement must be a PAY mechanism with an exposure-type CORRELATE, not an exposure-type mechanism, in both the household channel and the fiscal channel | **standing**, follows from claim 139 | A87 | yes | yes | yes | n/a | n/a | yes |
| 141 | Embodied workers earn 43 to 61 percent of what cognitively exposed workers earn (ACS 47,285 against 110,468 AIOE and 77,021 GPT; SIPP 62,961 against 134,876 and 102,347) | **standing** | A87 | yes | yes | yes | n/a | n/a | n/a |
| 142 | The bottom wage quintile is 3.24 percent of the total wage bill and the middle 14.26, so neither can deliver a dose above those levels; only the top quintile, at 51.22 percent, can reach the scenarios the hypothesis concerns | **standing**, arithmetic | A88 | yes | n/a | yes | n/a | n/a | yes |
| 143 | Displacement at the bottom of the wage distribution is a payroll tax event and displacement at the top is an income tax event: payroll is 64.6 percent of the fiscal loss in Q1 and 43.2 percent in Q5 | **standing** | A88 | yes | n/a | yes | n/a | n/a | yes |
| 144 | Cognitive AIOE exposure is a top-quintile scenario (71.3 percent of its wage bill in Q5) and embodied exposure is a middle-of-distribution scenario spread across Q2 to Q4, so the two indices are two named points on one axis | **standing** | A88 | yes | n/a | yes | n/a | n/a | yes |
| 145 | Household runway is NOT monotonic in wage: the thinnest buffers are in the SECOND quintile (median 0.84 months, 55.1 percent under one month), not the first | **provisional**, SIPP only | A88 | yes | no | yes | n/a | n/a | yes |
| 146 | A36's opposite-places geography result is entirely a pay result: the correlation of exposure share with PUMA mean home value goes from -0.596 and +0.554 to +0.006 and -0.077 once PUMA mean wage is controlled | **standing**, and it withdraws the housing interpretation of A36 | A89 | yes | n/a | yes | n/a | n/a | yes |
| 147 | The mortgage holder split is GSE 51.1 percent, FHA 12.6, bank portfolio 11.5, residual 24.9, replacing the flagged 60 to 70 percent agency range; three of four shares are read from a publisher | **standing** | A90 | n/a | n/a | yes | yes | n/a | n/a |
| 148 | A85's agency-mortgage figures fall by about a fifth on the sourced holder split: 29.7 percent of GSE net worth at a 25 percent cognitive dose rather than 40.6 | **standing**, and it SUPERSEDES the A85 agency figures with the direction unchanged | A90, A85 | yes | no | yes | n/a | n/a | yes |
| 149 | CRT (210bn Risk in Force) and private mortgage insurance (382.9bn) are loss TRANSFERS taken ahead of Enterprise capital (190.4bn) and one year of pre-provision earnings (34.2bn), not additions to capacity | **standing** | A90 | n/a | n/a | yes | yes | n/a | n/a |
| 150 | A 50 percent dose is 1.4 to 1.7 times the Fed severely adverse scenario on DEMAND but only 0.28 to 0.36 of it on HOUSE PRICES: a displacement shock of this size is a demand event first and a housing event second, the opposite of 2008 | **DOWNGRADED to conditional** | A91, A98: it holds at every Harter-Dreiman elasticity and fails entirely at an elasticity of 1.5, which Duca, Muellbauer and Murphy say is the more likely region. The condition must be stated whenever the claim is used | yes | n/a | yes | n/a | n/a | yes |
| 151 | A 10 percent fall in prices and wages with nominal debt fixed raises the share of obligated working-core households above DSTI 50 by 2.05 points, about as much as a 10 percent displacement shock does in the first round, without displacing anyone | **provisional** | A91 | yes | no | yes | n/a | n/a | yes |
| 152 | A reserve-currency issuer absorbs a 50 percent dose at 183 percent of GDP over twenty years; an emerging market that cannot borrow freely in its own currency reaches 389 percent at a 10 percent dose | **WITHDRAWN as a statement about automation** | A97: under r 9 percent against g 3 the emerging-market baseline reaches 377 percent of GDP in twenty years with NO displacement. The level path was baseline compounding. The increment is 19.2 points at a 10 percent dose over twenty years, against 10.6 for a reserve-currency issuer | n/a | n/a | yes | n/a | n/a | yes |
| 153 | Registered expectation (i) of the second-round prereg is REFUTED on both halves: at a 10 percent dose nothing crosses in the first round but three to seven private sheets cross in the second, and at large doses three to five non-fiscal sheets cross in the FIRST round | **REFUTED as registered** | A91 | yes | n/a | yes | n/a | n/a | yes |
| 154 | Registered expectation (ii) is CONFIRMED: at a 50 percent dose bank losses reach 901bn against the Fed's 624.9bn, and 92 percent of that comes from the second round rather than from displaced borrowers' own loans | **provisional**, SCENARIO | A91, A98: the 9:1 ratio is robust in direction across every sourced input range; the LEVEL spans a factor of nine, from 110bn to 993bn, and A91's 851bn sits in the upper third | yes | n/a | yes | n/a | n/a | yes |
| 155 | A displacement stress test built only on displaced borrowers' own obligations understates bank losses by roughly a factor of ten | **provisional**, and it is the module's most useful sentence for a stress-test designer | A91 | yes | n/a | yes | n/a | n/a | yes |
| 156 | 97.3 percent of the student loan book is a federal asset (FRED FGCCSAQ027S, 1,605.1bn against 1,650bn) | **standing** | A92 | n/a | yes | yes | n/a | n/a | n/a |
| 157 | Registered expectation (c) is CONFIRMED: the federal government bears the majority of losses at every dose in both columns, 77 to 92 percent in the first round and 60 to 70 percent with second-round effects, in 100 percent of rows | **standing** for the first-round column, **provisional** for the second-round column which is SCENARIO | A92 | yes | n/a | yes | n/a | n/a | yes |
| 158 | The state is the FIRST-ROUND absorber and the banking system is the SECOND-ROUND absorber: the second round raises the total while reducing the federal share | **provisional** | A92 | yes | n/a | yes | n/a | n/a | yes |
| 159 | The concentration of wage risk on the sovereign is the project's central result, and the bank channel is its second-round consequence | **provisional**, a thesis statement awaiting owner approval | A92 | n/a | n/a | n/a | n/a | n/a | n/a |
| 160 | The policy response removes 85 to 87 percent of the loss, or 78 to 81 percent with a 20 percent leakage of the surplus beyond the reach of the capital tax | **provisional**, SCENARIO | A93 | n/a | n/a | yes | n/a | n/a | yes |
| 161 | The response does NOT remove the payroll-funded trust fund losses, because replacement income financed from a capital tax is not covered wages. That is a design choice, not a law of nature | **standing**, an accounting fact about the instrument | A93 | n/a | n/a | yes | n/a | n/a | yes |
| 162 | The break-even capital tax rate rises with the dose and reaches 30.1 percent at a 50 percent embodied dose, above the 21 percent statutory rate and far above the sourced 3.2 to 20.4 percent effective range: the instrument that fixes the problem is outside anything currently observed | **standing** | A93 | n/a | n/a | yes | n/a | n/a | yes |
| 163 | The Acemoglu-Restrepo reinstatement term raises the median speed limit by only 5 to 7 percent and explains 0.000 of the variance, while the slack measure explains 0.665 | **standing** | A94 | yes | n/a | yes | n/a | n/a | yes |
| 164 | The labour model cannot distinguish the presence from the absence of the largest force in the literature it draws on, and is therefore FROZEN as an appendix scenario generator | **standing**, a method decision | A94 | n/a | n/a | yes | n/a | n/a | n/a |
| 165 | 66 sealed expected values are published with a replication brief written for an instance that does not read src/ | **standing** | A95 | n/a | n/a | yes | yes | n/a | n/a |
| 166 | The fiscal channel and the second-round module were mutually inconsistent: one assumes output is preserved and the other has output falling. Every number now carries its case | **standing**, a method correction | A96 | n/a | n/a | yes | n/a | n/a | yes |
| 167 | Case B raises the fiscal loss by 25 to 44 percent and raises the break-even capital tax rate from a range of 0.21 to 0.38 to a range of 0.56 to 0.86 | **standing** | A96 | yes | n/a | yes | n/a | n/a | yes |
| 168 | Under the internally consistent case there is no reading of the corporate tax literature in which the break-even capital tax rate is an available instrument | **standing**, and it supersedes A93's softer statement | A96, A93 | n/a | n/a | yes | n/a | n/a | yes |
| 169 | Every fiscal figure published by this project before the closing session is a CASE A figure, and case A is correct only if the demand shortfall is offset, which is what the policy response is for. The response has to work for the numbers sizing the response to be right | **standing**, a circularity now stated rather than hidden | A96 | n/a | n/a | yes | n/a | n/a | yes |
| 170 | The displacement increment to debt is 10.6 points of GDP for a reserve-currency issuer at a 10 percent dose over twenty years and 19.2 for an emerging market: a factor of 1.8, not the four-to-one the level paths implied | **provisional**, SCENARIO on stated r and g | A97 | n/a | n/a | yes | n/a | n/a | yes |
| 171 | The emerging-market issuer is on an unsustainable debt path before any displacement arrives, and that clause matters more than the displacement increment | **standing**, arithmetic on stated assumptions | A97 | n/a | n/a | yes | n/a | n/a | yes |
| 172 | The second-round bank-loss headline spans a factor of nine, from 110bn to 993bn, across sourced input ranges | **standing** | A98 | yes | n/a | yes | n/a | n/a | yes |
| 173 | The MPC gap explains 0.906 of the variance of the second-round bank loss and the income elasticity of house prices explains 0.998 of the variance of the house price fall. Nothing else in the module matters | **standing** | A98 | yes | n/a | yes | n/a | n/a | yes |
| 174 | The Okun assumption of 0.5 used in A91 is above the entire sourced range of 0.372 to 0.421 and overstated second-round job losses by about a fifth | **standing** | A98 | n/a | yes | yes | n/a | n/a | n/a |
| 175 | The dose-response table is organised by WAGE QUINTILE and the exposure indices are demoted to named scenarios | **standing**, a method decision resting on claims 139, 140 and 146 | A99 | yes | yes | yes | n/a | n/a | yes |
| 176 | PAEI is a measurement instrument this paper uses, not a finding it reports. Its one surviving independent use is the driving pathway | **standing**, and it DOWNGRADES the PAEI contribution claim | A99 | n/a | n/a | yes | n/a | n/a | yes |
| 177 | The federal share of losses RISES with the wage quintile, from 89.0 percent at Q2 to 95.9 at Q5, so the sovereign result is strongest exactly where the original framing expected the private channel to be | **provisional** | A99 | yes | no | yes | n/a | n/a | yes |
| 178 | The owner's Trustees Report and CBO files were not placed in data/raw/manual/, so the trust fund reserve column stays empty and the derived thresholds stand | **standing**, a blocked-source record | A100 | n/a | n/a | n/a | n/a | n/a | n/a |
| 102 | The unresolvable rent-share disagreement is worth about 30 to 37 percent of the fiscal loss, with the Karabarbounis-Neiman reading the worse one | **provisional** | A70 | n/a | n/a | n/a | yes | n/a | n/a |
| 103 | A41's DSTI crossings are the right headline for household stress | **DOWNGRADED to secondary** | A69: Gerardi et al. show affordability thresholds miss most defaults (only 30 percent of defaulters would need to go below subsistence; 38 percent could pay without cutting consumption) | yes | yes | yes | n/a | n/a | yes |

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

---

## Independent replication, round one: the register entry

**2026-09-20.** A fresh instance rebuilt the project from `notes/replication_brief.md` and
raw public data, reading no code and opening the sealed file only after its own values were
final. It attempted 51 of the 87 sealed quantities and matched 21. The report, the results,
the comparison and the brief critique are in `notes/replication/`; the classification of all
30 mismatches is in `notes/replication/round1_mismatch_classification.md`.

**This is the first time any quantity in this project has been checked by something that did
not build it.** The promotion pass of 2026-09-19 used a script that imported nothing from
`src/`, which is a weaker test: it was written by the same instance, from the same
understanding.

### What is now independently replicated

| Claim | Quantity replicated | Flag |
|---|---|---|
| 126, 127, 137, 138 | all four survey under-reporting factors, within 0.5 percent, with the SIPP universe construction and the units call landing independently | **R-replicated** |
| 44 | occupied against all housing records, 131.33m against 145.33m, exactly | **R-replicated** |
| 156 | the federal student share, 0.9728 against 0.972808 | **R-replicated** |
| 121 | the ACS embodied and ALL cap shares, and the SIPP embodied and GPT cap shares | **R-replicated** |
| 139, 140 | **the pay control kills most of the exposure-type contrast and the SIPP Eloundou GPT contrast REVERSES SIGN.** Found before the sealed file was opened, on a different embodiment index and a different crosswalk | **R-confirmed-direction** |
| 74 | **the fiscal condition fails.** The replicator first reported it PASSING, then found their own tau_normal error and confirmed the failure at every reading of tau_l, under their R as well as ours | **R-confirmed-direction** |
| 152, 171 | the no-displacement debt baseline, 3.7670 against 3.7674 at our start ratio | **R-replicated** |
| 113 | the portfolio-loss-rate trap, the vacant-unit trap and the FRED units trap all reproduced as described | **R-confirmed-direction** |

The section-1 slack fit is **R-unattempted in substance**: `n`, `R squared` and both
`x_range` endpoints matched, the intercept and slope did not, and the cause is a vintage
window the brief never stated. It is not evidence for or against the claim.

### What failed because this project was wrong

| Claim | What failed | Flag |
|---|---|---|
| 167 | the break-even capital tax rate under both cases | **R-failed** |
| 115, 101b, 101c | every terminal-year fiscal loss in dollars, 21.4 percent too large on the wrong wage bill base | **R-failed** |
| 120 | the HI trust fund ratio, 4.7 percent too large on the OASDI payroll share | **R-failed** |
| 170 | the debt increment, which inherits the case B defect | **R-failed** |

### What is pending round two

Everything in sections 5, 7, 10 and 11 of the brief: the household first-round losses, the
incidence spreads, the sovereign share and the whole second-round module. **The replicator
produced no value for any of them**, in every case because the brief did not contain the
model. Claims 110, 111, 117, 133, 134, 150, 153, 154, 155, 157, 158, 160, 172, 173, 177 are
therefore **R-pending-2** and none of them may be described as independently replicated.

---

## Claims amended by the replication repair, 2026-09-20

Every number below moved because this project was wrong, not because a source was revised.

| # | Claim | Amendment |
|---|---|---|
| 167 | Case B raises the fiscal loss by 25 to 44 percent and the break-even rate from 0.21 to 0.38 up to 0.56 to 0.86 | **NUMBERS WITHDRAWN.** The break-even rate divided a loss that already nets out tau_k by a surplus built on a different wage bill total. Corrected: case B raises the loss by **38 to 68 percent** and the break-even rate from **0.125 to 0.301** up to **0.182 to 0.650**. Status stays standing on the DIRECTION, which is unchanged. **R-failed** |
| 168 | Under the internally consistent case there is no reading of the corporate tax literature in which the break-even rate is an available instrument | **DOWNGRADED, and this WEAKENS the thesis.** On the corrected grid, case A break-even is at or below the top of the sourced tau_k range (0.20351) in 10 of 15 cells and case B in 5 of 15. The surviving claim is narrower: **the break-even rate exceeds the OPERATIVE effective rate of 0.0708 in every cell in both cases, and exceeds the top of the sourced range only at larger doses.** That is a statement about the tax code as it stands, not about the literature. **provisional** |
| 162 | The break-even rate reaches 30.1 percent at a 50 percent embodied dose, above the 21 percent statutory rate | **STANDS UNCHANGED.** This one was computed as `0.301 * (1 - R)` in a different module and was always correct. It is now the case A maximum exactly, because R reaches zero there |
| 115 | Terminal loss 1.79 percent of federal receipts at the 10 percent dose | **CORRECTED to 1.42 percent.** Wage bill base. The OASDI figure, 4.07 percent, is a ratio and does not move |
| 120 | Corrected trust fund loss 4.2 percent of fund payroll income at 10 percent, 11.9 at 25, maximum 76.5 | **OASDI STANDS** at 4.07 and 12.03, maximum 76.43. **HI CORRECTED** from 4.04 to **3.86** at the 10 percent dose: HI's own payroll share is 0.8720, not the OASDI 0.9126, and 462.4bn is HI total income rather than payroll income |
| 101b, 101c | Cumulative fiscal loss and the OASDI share at 90 percent of both types | **EVERY DOLLAR FIGURE FALLS 17.6 PERCENT** on the corrected wage bill base. The OASDI shares, being ratios, do not move |
| 170 | The displacement increment is 10.6 points of GDP for a reserve-currency issuer at a 10 percent dose over 20 years and 19.2 for an emerging market | **CORRECTED to 10.1 and 18.2.** The ratio of 1.8, which was the point of the claim, is unchanged |
| 172 | The second-round bank-loss headline spans a factor of nine, 110bn to 993bn | **LEVELS CORRECTED to 173bn to 1,565bn.** The second-round module was using the occupational grid as its wage bill, 73.9 percent of the national total. **The factor of nine survives exactly, at 9.02**, which is the part of the claim that was load-bearing |
| 154 | At a 50 percent dose bank losses reach 901bn against the Fed's 624.9bn, 92 percent from the second round | **CORRECTED to 1,195bn, a ratio of 1.91, and 94 percent from the second round** |
| 150 | A 50 percent dose is 1.4 to 1.7 times the Fed severely adverse on DEMAND and 0.28 to 0.36 on HOUSE PRICES | **DEMAND CORRECTED to 0.71 to 1.84**, so the low band now falls BELOW the Fed's severity where it previously did not. **House prices unchanged at 0.283**, because that ratio is scale-invariant. The ordering, demand ahead of housing, holds in both bands |
| 157 | The federal government bears 77 to 92 percent of first-round losses and 60 to 70 percent with second-round effects | **CORRECTED to 75.9 to 91.6 and 56.6 to 64.5.** The majority result holds in every row |
| 126, 127, 138 | The survey under-reporting factors | **AUTO CORRECTED from 1.7431 to 1.9036** on the replacement aggregate. Mortgage, card and student unchanged. **The auto bank loss does not move**, because the bank-held share carries the same denominator and it cancels |
| 132 | Trust fund RESERVES could not be sourced; the reserve denominator is left empty rather than estimated | **SUPERSEDED.** The owner placed the 2026 Trustees summary tables. OASI 2,338.3bn, DI 223.0bn, HI 255.7bn at the end of 2025, and depletion timing is added as a second capacity measure |
| 178 | The owner's Trustees Report and CBO files were not placed, so the reserve column stays empty and the derived thresholds stand | **SUPERSEDED.** Both files are in `data/raw/owner/`. The CBO extraction is verified against its original PDF; the Trustees extraction has no original (its source is an HTML page) and is verified instead by reconciling every accounting identity in the summary tables, 23 checks, 0 failures |
| 165 | 66 sealed expected values are published with a replication brief | **SUPERSEDED by 87 in round one and 87 in round two**, and the round-one file is now frozen at `data/release/sealed_expected_values_round1_ARCHIVED.json` |
| 118 | PLAUSIBILITY RULE in force: 32 retroactive checks found 4 violations, all corrected | **EXTENDED to 43 checks.** Seven new bounds on the break-even capital tax rate are added, and they are the bounds whose absence let the 0.378371 figure stand. Still 4 violations, all of them the SUPERSEDED rows deliberately retained to show what the rule caught |

---

## New claims, this session. All PROVISIONAL by the same-session rule.

| # | Claim | Status | Findings | Replication flag |
|---|---|---|---|---|
| 179 | The break-even capital tax rate published in round one was not a tax rate. It divided a loss that already nets out tau_k by a surplus, and numerator and denominator were built on two different wage bill totals, a spurious factor of 1.6438. `old = (comp / grid) x [tau_l - tau_k / (1 - R)]` reproduces the sealed 0.378371 exactly at R = 0 | **provisional**, arithmetic | this session | R-failed, corrected |
| 180 | A replicator found a live arithmetic error in this project from a PLAUSIBILITY BOUND ALONE, without reading any code, because a break-even rate defined as `tau_l * (1 - R)` cannot exceed tau_l. **Bounds catch errors that tolerances do not** | **provisional**, a method finding | this session | n/a |
| 181 | The fiscal modules applied a wage tax rate to compensation of employees while tau_l is built on wages and salaries. Employer pension and health contributions bear neither the income tax nor the payroll tax, so every fiscal dollar figure was 21.4 percent too large | **provisional**, arithmetic | this session | R-failed, corrected |
| 182 | The second-round module and the fiscal module used two different wage bill totals for the same dose, 9,870.2bn and 16,224.3bn, and neither was the base tau_l is defined on. One base, FRED WASCUR at 13,365.2bn, now serves both | **provisional** | this session | R-failed, corrected |
| 183 | **The fiscal condition fails under the replicator's parameters as well as ours**, at every reading of tau_l, at the operative effective capital tax rate of 0.0708. R of 0.6233 against our 0.568316 does not change the verdict | **provisional**, and it is the strongest independent support any claim in this project has | this session, A32 | R-confirmed-direction |
| 184 | The R gap between the two rebuilds is two roughly equal parts, rho 0.6610 observed against 0.6926 fitted and omega 0.8598 against 0.90 assumed. **R_2026 uses the DIRECTLY OBSERVED 2026 rho, not the fitted value**, and the brief said otherwise, which is what sent the replicator wrong | **provisional**, a documentation correction | this session | n/a |
| 185 | **The preference for prime-age nonemployment over the unemployment rate has NO window on which it wins on fit.** The unemployment rate has the higher R squared on the full sample (0.812 against 0.773) AND post-2008 (0.940 against 0.732), and its advantage is LARGER post-2008. The preference rests on MECHANISM alone and must be defended that way wherever it is stated | **provisional**, and it REFUTES the expectation this test was written to record | this session, A63 | n/a |
| 186 | The brief's claim that the circular unemployment-rate fit gives a speed limit "about 2.5 times larger" is **WITHDRAWN**. The slope ratio is 1.107 on the full sample and 1.096 post-2008 | **withdrawn** | this session | R-confirmed-direction, the replicator flagged it first |
| 187 | HI was NOT in deficit in 2025: its reserves ROSE by 18.2bn, from 237.5 to 255.7. The Trustees put the first year HI cost exceeds income excluding interest at 2026 and including interest at 2027 | **provisional**, read from the Trustees summary tables | this session | n/a |
| 188 | 160.2bn is the OASDI NET CHANGE IN RESERVES in 2025 (OASI -200.0 plus DI +39.8), the amount by which cost exceeded TOTAL income including interest. It is not an HI figure and not a payroll-only balance | **provisional**, arithmetic on the Trustees tables | this session, A32 | n/a |
| 189 | The repository's HI payroll income of 286.2bn was 71.0 percent of the published 403.2bn. **The gap is the wage bill, not the rate**: the statutory 2.9 percent was applied to this project's occupational grid, which is a subset of covered earnings, while HI is levied on all covered wages and on self-employment with no cap | **provisional** | this session | n/a |
| 190 | Depletion timing is carried as a capacity measure in its own right: OASI 2032 Q4 at 78 percent of scheduled benefits, combined OASDI 2034 Q3 at 83 percent, HI 2033 Q2 at 89 percent, DI not within 75 years. A reserve stock says how much; a depletion date says how long, and for a fund running down that is the supervisory number | **provisional**, a method addition | this session | n/a |
| 191 | FRED MVLOAS was discontinued after 2024Q4 and was two years stale against every other input. **The auto bank loss is insensitive to the aggregate**, because the same denominator sits in the under-reporting factor and in the bank-held share and cancels | **provisional** | this session | n/a |
| 192 | The Federal Reserve does not break auto out from student loans: both are scored against the single "Other consumer" line, 54.1bn of loss on a 741.1bn implied balance. **The two percentages are not independent and cannot be summed.** This was inferable from the sealed pairs and should never have had to be inferred | **provisional**, a disclosure correction | this session, A85 | R-confirmed-direction |
| 193 | Twenty-five of the thirty round-one mismatches involve a brief omission and ten are this project's own error. **The brief is implicated in five of every six failures**, which is the replicator's verdict confirmed by arithmetic | **provisional** | this session | n/a |

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
- **The slack measure is prime-age nonemployment and the reason is MECHANISM, never fit.**
  The unemployment rate has the higher R squared on the full sample and on a post-2008
  window, and its advantage is larger post-2008. Any sentence preferring prime-age
  nonemployment must give the circularity argument in the same breath and must not claim the
  fit supports it. `src/slack_window_check.py` holds the test.
- **State the plausibility bound before the number, every time.** A replicator found a live
  error in this project from a bound alone, with no access to the code. Bounds catch what
  tolerances do not.
- **Every dose is converted to dollars on FRED WASCUR national wages and salaries**, the base
  tau_l is built on. Not compensation of employees, which includes untaxed employer
  contributions; not this project's occupational grid, which is 73.9 percent of the national
  total.
- **Trust fund denominators are the fund's OWN payroll income**, read from the Trustees
  summary tables: OASDI 1,322.6bn, HI 403.2bn. The two funds have different payroll shares of
  total income, 0.9126 and 0.8720, and neither may be used for the other.
- **Auto and student are scored against the SAME Federal Reserve "Other consumer" line.**
  Say so wherever either appears; the two percentages cannot be summed.

---

## New claims, labour backing session, 2026-09-20. ALL PROVISIONAL by the same-session rule.

Every claim below is **R-pending-2**: sealed under `labour_backing` and `two_sided_bet` in
`notes/sealed/sealed_expected_values_round2.json`, mechanics in section 14 of
`notes/replication_brief_v2.md`, and **none has ever been checked by anything that did not
build it.** Bounds were stated before the numbers throughout: 75 plausibility checks across
the four builds, 0 violations.

| # | Claim | Status | Findings | Replication flag |
|---|---|---|---|---|
| 194 | The DIRECT labour backing ratio of the US claim stock is 0.270 in 2025: 40,380bn of 149,407bn dollars of claims are serviced in the first round out of wages. First round only, one step, business-revenue-serviced classes zero by rule | **provisional** | this session, B1 and B3 | R-pending-2 |
| 195 | **The federal government holds, guarantees or owes 79.4 percent of all labour-backed claims**, in two legs: 32.6 percent as holder or guarantor and 54.3 percent as obligor, less the overlap. **This was produced from the Financial Accounts with no reference to the dose-response table and lands inside the independently derived 75.9 to 91.6 percent federal share of first-round losses** | **provisional**, and it is the strongest result of the session | this session, B3; claim 157 | R-pending-2 |
| 196 | The sovereign share roughly DOUBLED in fifty years: 0.336 in 1970, 0.564 in 1990, 0.649 in 2010, 0.794 in 2025. The drivers are visible in the series: the GSEs and the 2008 conservatorship, federal student lending after 2010, and the growth of Treasury debt, which is the obligor leg | **provisional** | this session, B4 | R-pending-2 |
| 197 | The RATIO itself is nearly trendless and cyclical (0.288 in 1947, 0.376 at the 2008 peak, 0.270 in 2025). It falls when equity is expensive, because equity is the largest zero-by-rule class. **It is as much an asset price series as a labour series and must not be read as a measure of labour dependence** | **provisional**, and it is a warning about the headline | this session, B4 | R-pending-2 |
| 198 | **The one-step tracing rule moves the headline by 76 percent and no other judgement call moves it by more than 10.** The household and fiscal cells, which is where this project's own measurement sits, are robust. The definition is the whole argument | **provisional**, and it was predicted in `feasibility.md` before being computed | this session, B9 | R-pending-2 |
| 199 | The INDIRECT (second-round) labour backing of business revenue is 0.338, the product of consumption's share of final demand (0.681) and labour's share of personal income (0.497). Combined with the direct ratio it gives 0.475. **This is never blended into the headline; it is the paper's first-round versus second-round distinction expressed as a ratio** | **provisional** | this session, B2 | R-pending-2 |
| 200 | **The bottom wage quintile carries 4.15 times more labour-backed claim per dollar of wage bill than its wage share implies, and the top quintile 0.65, a factor of 6.3.** Q1 holds 13.4 percent of household labour-backed claims on 3.2 percent of the wage bill | **provisional**, SIPP only | this session, B5; claim 175 | R-pending-2 |
| 201 | **The obvious connection formula is wrong for credit claims.** Applying `(1 - R)` to a credit class assumes only the lost-income fraction of a balance is at risk, when a displaced borrower's whole balance is. Removing it moves auto loans from 0 of 8 to 7 of 8 rows inside the benchmark loss band. `(1 - R)` belongs in the fiscal channel and nowhere else | **provisional**, a method finding | this session, B8 | R-pending-2 |
| 202 | **The fiscal loss this project publishes is already NET of capital tax at the operative rate**, so any calculation of how much a capital tax hedges the federal position must use the GROSS loss or it counts the tax twice. The check is that the break-even rate recovers exactly 1.000 of the gross fiscal loss by construction | **provisional**, arithmetic, and it extends claim 179 | this session, B11 | R-pending-2 |
| 203 | **The federal government is the least hedged holder in the economy**: 79.4 percent of the wage leg against 1.0 percent of the AI leg, a cover ratio of 0.03, lowest of any holder class by a factor of five against banks at 0.17 | **provisional**, CONFIRMED as registered | this session, B11 | R-pending-2 |
| 204 | The mirror holds. **Households hold 38.4 percent of the AI leg and 6.1 percent of the wage leg**, a ratio of 6.33; pensions 3.97; nonfinancial business 5.02. The rest of the world (1.00), other financial (1.07) and insurers (1.02) are almost exactly hedged, which is unforced and striking | **provisional** | this session, B11 | R-pending-2 |
| 205 | **The ratio of equity share to household debt share runs from 28.1 at the top 0.1 percent of the wealth distribution to 0.019 at the bottom half, a factor of about 1,480.** The bottom 50 percent hold 0.6 percent of household equity and 30.4 percent of household debt | **provisional**, Fed Distributional Financial Accounts | this session, B12 | R-pending-2 |
| 206 | **The current AI financing structure resembles the 2000 equity-financed bust and not the 2008 debt-financed crisis**: aggregate operating cash flow over capex is 1.343 and capex in excess of operating cash flow is 6.5 percent of capex. **The marginal dollar does not: Oracle, CoreWeave, Equinix and Digital Realty each spend above operating cash flow, and off-balance-sheet financing is not sourced at all, so 6.5 percent is a LOWER BOUND** | **provisional** | this session, B12 | R-pending-2 |
| 207 | The two historical anchors MEASURED from Z.1 and NIPA rather than cited: **the equity bust was the larger asset-price event and the smaller fiscal and banking event.** Nonfinancial corporate equity fell 39.9 percent of peak GDP in 2000 to 2002 against 22.4 in 2007 to 2009, while federal receipts fell 9.5 percent against 16.0 and corporate tax receipts 35.1 percent against 53.4 | **provisional**, measured | this session, B12 | R-pending-2 |
| 208 | **The federal government loses in all three AI states.** CONFIRMED, with one qualification that weakens it and must be stated whenever the claim is used: at the operative tau_k of 0.0708 the capital tax recovers **36 percent** of the gross federal first-round loss at a 10 percent dose, so "holds almost none of the upside" is too strong. The recovery share FALLS as the dose rises, because the break-even rate rises with the dose and the operative rate does not | **provisional**, CONFIRMED with a stated qualification | this session, B12 | R-pending-2 |
| 209 | A labour decomposition of the claim stock by the income TYPE that services it was not located in any prior work, including the Federal Reserve DSR, whose denominator is explicitly all income, and the Distributional Financial Accounts, which distribute by wealth percentile and not by income type. **The search is now systematic for this question; the claim remains "none located", not "none exists", and a direct approach to the Financial Accounts team has still not been made** | **provisional**, and the novelty gate is narrow | this session, B7 | n/a |

---

## Priority claims amended by the B7 related-work search, 2026-09-20

**This section exists because the owner's own search found works this project's literature
audit had missed, and it REMOVES a priority claim rather than adding one.** The full table,
with a verification level on every row, is in `lit/related_work_labour_backing.md`.

| # | Claim | Amendment |
|---|---|---|
| 85 | No published work links occupational AI exposure to household balance-sheet outcomes (none located, non-systematic search) | **NARROWED AND PARTLY SUPERSEDED.** True as written for the household half. Misleading by omission for the fiscal half: Chen (2026, arXiv 2603.09209) is explicitly a macro-financial stress test of rapid AI adoption that reaches private credit and mortgage markets, close to this project's second-round module. The claim must not be used as a general novelty statement |
| **THE FISCAL MECHANISM** | That wage-based public finance makes labour displacement a revenue event before it is a credit event | **PRIORITY RETIRED. This project did not discover it and must not imply that it did.** Casas and Torres (2024, International Tax and Public Finance 31(3), 780 to 807), Korinek and Lockwood (2026, Brookings and NBER 34873), **Price and Suresh (2026, RAND RR-A4980-1), whose two scenario axes are this project's rho and tau_k and whose headline is that 84 percent of 2024 federal revenue came from individual or payroll taxes**, the Windfall Trust (2026), and IMF Notes 2026/002 all have the mechanism. What survives is the calibrated US measurement and the liability side |
| **THE STRESS-TEST FRAMING** | That this is a stress test of AI displacement | **NARROWED.** Chen (2026) is a macro-financial stress test of rapid AI adoption with eleven testable predictions. What remains this project's own is severity expressed against the **Federal Reserve 2026 severely adverse scenario**, loss rates by loan category, and the decomposition by holder, none of which Chen has |
| 168 | The capital tax verdict | **NARROWED FURTHER, on top of the replication repair.** Falk and Tsoukalas (2026, arXiv 2603.20617) show by theory that capital income taxes cannot resolve the automation externality and that a Pigouvian automation tax can. They have the result first and in more general form. This project's contribution is the calibration, not the verdict |
| 80, 93, 94 | The hiring-freeze blind spot | **PRIORITY HELD, and the claim is now CAUTIONED.** The deduction is still this project's own. It has NOT been tested against Manning, Aguirre, Muro and Methkupally (2026, Brookings and NBER 34705), who find **AI exposure and adaptive capacity POSITIVELY correlated**, with 26.5m of the 37.1m workers in the top exposure quartile in occupations of above-median adaptive capacity. **That is thesis-weakening and cuts against the implicit direction of the buffer work.** Treat the blind spot as provisional until the comparison is done |
| **THE EARLY-WARNING DASHBOARD** | That the trigger dashboard is a contribution | **PRIORITY CLAIM DROPPED.** An indicator list is not a research contribution, and the IMF note and the Windfall Trust report both effectively propose monitoring. The dashboard stays as a useful artifact and stops being claimed as novel |
| 159 | The concentration of wage risk on the sovereign is the project's central result | **STRENGTHENED, and it is now the recommended lead.** Claim 195 measures the same concentration from the Financial Accounts by a completely different route and agrees. With the fiscal-mechanism priority retired, the holder result is what remains distinctively this project's own |

**Citation hygiene, found during the same search.** The repository carries
`data/raw/manual/KorinekLockwood2025_public_finance_AI.pdf`. That is the **superseded
title**. `paper/references.bib` must be updated to Korinek and Lockwood, "Public Finance in
the Age of AI: A Primer", Brookings working paper, 8 January 2026, and NBER Working Paper
34873. Also newly located and NOT previously in the audit: Congressional Budget Office
(2024), "Artificial Intelligence and Its Potential Effects on the Economy and the Federal
Budget", December 2024. **Both are audit gaps and are recorded as such.**

---

## Claims amended by the final analysis session, 2026-09-20 (A103)

Gate report: `notes/GATE_REPORT_final_session.md`. Clearing pass:
`data/release/headline_clearing_pass.csv`.

| # | Claim | Amendment |
|---|---|---|
| 133, 148 | Agency mortgage reaches 41 percent of GSE net worth at a 25 percent cognitive dose (A85), corrected to 29.7 percent (A90) | **SUPERSEDED AND REFRAMED.** Both figures were the GROSS GSE loss over net worth, struck before any risk transfer; the waterfall never touched them. Rebuilt loan class by loan class from the 2025 Form 10-Ks (`src/gse_waterfall.py`), the RETAINED agency loss at that dose is **11.9 to 29.2 percent** of Enterprise net worth. Three input errors found: CRT risk in force of 210.0bn was the FHFA CUMULATIVE since-2013 figure against an outstanding **79.0bn**; the PMI-covered share of the book is **21 to 22 percent**, not 6; and **39 to 53 percent of each single-family book carries no credit enhancement at all**. **standing** |
| new 196 | The federal `beyond` layer on the agency book is zero at every dose from 5 to 75 percent | **NEW, and now a result rather than dead code.** 179.4bn of Enterprise capital against a maximum retained first-round loss of 109.0bn, on the STATUTORY negative-net-worth trigger of the senior preferred agreements rather than the looser capital-plus-earnings trigger we had used. FIRST ROUND ONLY, house prices fixed. **standing** |
| 115, 101b, 101c, and every extended-axis figure | Terminal and cumulative fiscal losses on the extended displacement axis | **POINT ESTIMATES WITHDRAWN IN 672 OF 2,520 CELLS, 26.7 percent.** The reemployment rate is a fixed point with a pole at an employment dose of 0.676142, a wage-bill dose of 0.459 for the embodied group. The superseded code enforced the [0,1] bound ACCIDENTALLY, through an in-loop clip, and published the clip boundary as an estimate. Replaced by a bounded treatment (`src/rho_bounded.py`): a point estimate only inside the observed rho range [0.49, 0.74], otherwise the band [0, 0.49] labelled outside the data. The old point lies inside the new band in 568 of 672 cases; where it does not, the old value WAS the boundary, so the superseded embodied figures at large doses OVERSTATED the loss. **The 10 percent dose figures are unaffected.** |
| new 197 | At a 50 percent dose no exposure type has a reemployment-rate point estimate, and the embodied group has no admissible fixed point at all | **NEW. withdrawn** as a quantity, **standing** as a finding about the limit of the data |
| 118 | PLAUSIBILITY RULE: 43 checks, 4 violations | **EXTENDED to 53 checks.** The bound `rho in [0, 1], it is a rate` is added and applied to every rho column on the superseded axis, the bounded axis, the bounded scenario axis and the bounded dose grid, with a diagnostic counting raw fixed-point breaches. Still 4 violations, all deliberately retained superseded rows. **The replicator found this from the formula alone, with no code access. Second time a bound caught what a tolerance could not** |
| 159, 195 | The sovereign share is the central result | **CONFIRMED AND RANGED, and recorded as the paper's central object.** The Treasury class is **FL313161105 + FL313169205 = 33,887.1bn at the 2025 Z.1 annual vintage**, verified against three external cross-checks. The level was right and the DOCUMENTATION was wrong. **Agreed sovereign share 0.778 to 0.804, centred on 0.794**, containing our 0.793592, the replicator's independent 0.777810 and every measurement variant. **No measurement call moves it by more than 1.3 percent**, and whether the central bank counts as federal moves it by EXACTLY ZERO. **NOT robust to four structural calls**, the one-step rule worst at -43 percent. **standing, with the convention stated** |
| 157 | The federal government bears 75.9 to 91.6 percent of first-round losses | **REPORTED BY DOSE, not as one range.** Narrow reading: 0.759 to 0.853 at 5 percent, **0.785 to 0.870 at 10**, 0.810 to 0.923 at 25, 0.855 to 0.925 at 50, falling back to 0.809 to 0.897 at 75. Conservatorship reading 8 to 10 points higher. **It is NOT monotone**: it peaks at 50 percent. The replicator's independent by-dose result sits inside our range at both ends. **standing** |
| 168 | The capital tax verdict, and its sealed note | **NOTE CORRECTED.** The sealed `condition_passes` note said the required rate exceeds the top of the sourced range at every reading. Our own `replication_r_sensitivity.json` says the opposite in all five cells: the required rate maxes at **0.137276** against a sourced top of **0.20351**. The boolean is right; **the note overstated the finding and is fixed** |
| new 198 | The part-time wage parameter is the sourced BLS ratio 0.3206, not the assumed 0.50 | **BRIEF CORRECTED.** 386 over 1,204 dollars of median usual weekly earnings, 2025. 0.50 does not reproduce our own omega; 0.3206 does, and always did in the code. **standing** |
| new 199 | The mortgage holder shares sum to 100.1 at one decimal | **PRESENTATION DEFECT, FIXED.** Published to two decimals, 51.10 / 12.57 / 11.45 / 24.88, summing to exactly 100.00. The replicator's proposed remainder of 24.8 was also wrong: the exact residual is 24.878. No downstream number moves |
| 85, and the novelty statement for the labour backing ratio | No published work links occupational AI exposure to household balance-sheet outcomes | **RAND (Price and Suresh 2026) NOW READ IN FULL** and retained at `data/raw/manual/`. Confirms the boundary: the report contains **no household debt, no mortgages, no bank balance sheets and no financial stability content**. Upgraded from verification level B to F. **Two independent corroborations found**: their 66 percent of federal revenue directly from labour against our 63.4 percent, and their "corporate tax rates roughly doubled" against our 1.55 to 1.94 times operative. **provisional**, pending the systematic search (limitation L3) |
| 80, 93, 94, and the Manning comparison | The hiring-freeze blind spot is cautioned because Manning and others cut against it | **CORRECTED: OVERLAP, NOT CONTRADICTION.** Manning and others find exposure and adaptive capacity positively correlated, which is the same conclusion as our claim 145 (buffers are not monotonic in pay) on a different object, and is what you get when the exposed group is higher paid, which our cognitive groups are. **What remains ours is the pay-level buffer finding**, which an occupation-level index cannot produce. The blind spot itself is unaffected: never-hired entrants are outside both sample frames |
| new 200 | The fair lending constraint on occupation-based underwriting | **NOW LEGALLY SOURCED, and the sourcing makes the claim more careful.** Occupation is **NOT** a prohibited basis under ECOA (12 CFR 1002.2(z)), and 12 CFR 1002.6(a) permits a creditor to consider any information not used to discriminate on a prohibited basis. The exposure is a **discriminatory-effects claim under the Fair Housing Act** (24 CFR 100.500), lawful if supported by a legally sufficient justification under a burden-shifting framework. All three verified against eCFR on 2026-09-20. **standing**. This clears the PROJECT_BRIEF condition that gated the claim |
| Replication protocol | The round two replication was blind | **QUALIFIED, and it must be stated this way in the paper.** Blind **by protocol, not by isolation**: same machine, sealed file reachable at a path the brief names, reported unopened until the rebuild was final. Supporting evidence is internal and circumstantial. **The claim is "independently rebuilt under a reported blind protocol", not "independently verified"** |

### Removed from the headline set by the clearing pass

Five, each with the reason recorded in `data/release/headline_clearing_pass.csv`: the
incidence count-robustness claim (not reproducible, the alternative reading gives 59 percent
not 5 to 9); the 50 percent reemployment rate (no such number); the hedge ratio at the
operative tau_k (its input `surplus` is undefined in our own brief); the bottom-quintile
labour-backed ratio of 4.1489 (the rebuild lands 2.5 to 3.4 times away and we never defined
the universe; **the gradient survives, the magnitude does not**); and the two cognitive index
scores by occupation (eleven mismatches in opposite directions).

### Headline set after the pass

**9 REPLICATED, 10 STANDING, 5 SCENARIO, 5 REMOVED. Headline set size 24.**

### Stated limitations, carried without further work

L1 off-balance-sheet and GPU-backed AI financing unmeasured; L2 capital gains receipts
unsourced; L3 the labour backing ratio's novelty is "none located" pending a systematic
PRISMA search; L4 the holder proxy residual; L5 effective labour tax rates by income not
taken from CBO. Full text in `data/release/stated_limitations.csv` and in the gate report.

### One item not completed, and why

**IMF Note 2026/002 was not read in full.** The owner reported placing it and the RAND report
in `data/raw/manual/`; neither was there and a search of the whole machine found neither. The
RAND report was obtained directly from the publisher and read. **`imf.org` returns HTTP 403
on every route and the eLibrary issue returns 404**, so that row stands at verification level
B and the related-work table says explicitly that its boundary has NOT been redrawn from the
full text. Recorded in `lit/unverified.md`.

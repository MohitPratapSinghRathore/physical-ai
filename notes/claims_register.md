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
| 30 | P1r: the fiscal condition has TWO levers, R and tau_k. Within the omega range tau_k decides the verdict; across the historical rho range (0.49 to 0.74) R moves by 0.215, which is decisive near tau_k = 0.10. Both must be stated | **amended**, see A52 | A33, A34, A50, A52 | n/a | n/a | n/a | n/a | n/a | n/a |
| 31 | The net fiscal position of displacement is about 674bn dollars | **withdrawn** | A33 (artifact, dominated by unverified outlays) | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | The fiscal channel is the largest of the channels measured | standing | A32, A34 | n/a | n/a | n/a | n/a | n/a | n/a |
| 33 | The fiscal loss per dollar displaced is 1.7 times larger for cognitive exposure, so this is NOT primarily a Physical AI channel | standing | A34 | yes | n/a | n/a | n/a | n/a | n/a |
| 34 | The labour-linked receipts share is 77.7 percent | **withdrawn** | A8 (overstated; denominator was wrong) | n/a | n/a | n/a | n/a | n/a | n/a |
| 35 | rho (reemployment share) is known | **resolved, sourced** | A48, A49. rho = 0.6616, BLS DWS Table 1, January 2026 | n/a | n/a | n/a | n/a | n/a | n/a |
| 45 | omega = 0.9554 (full-time only, nominal), which pulls break-even down far enough that observed rho meets it in 12 of 27 cells | **withdrawn** | claimed last session, overturned in A48: it priced only full-time moves and used the nominal rather than counterfactual ratio | n/a | n/a | n/a | n/a | n/a | n/a |
| 46 | omega = 0.8598 blended and counterfactual-adjusted (range 0.8292 to 0.9076) is the value the fiscal condition needs | **provisional**, sourced this session | A48 | n/a | n/a | n/a | yes | n/a | n/a |
| 47 | rho falls with labour slack: rho = 0.8090 - 0.0304 x unemployment rate, R-squared 0.812 on 14 DWS vintages, 2000 to 2026 | **standing**, cleared a second pass and is load-bearing in A56 and A58 | A49 | n/a | n/a | n/a | n/a | n/a | n/a |
| 47a | That relationship may be extrapolated beyond 9.8 percent unemployment | **not claimed** | A49. 9.8 is the worst labour market in the sample and the line is not extended past it | n/a | n/a | n/a | n/a | n/a | n/a |
| 48 | Observed retained wage share R = rho x omega = 0.5689 at the 2026 survey; required R is 0.608 to 0.686 at tau_k = 0.10, so the condition is NOT met there | **provisional**, sourced this session | A50 | n/a | n/a | n/a | yes | n/a | n/a |
| 49 | Within the OMEGA range alone, tau_k decides the verdict: tau_k = 0.21 passes in every cell at every omega including the switcher scenario, tau_k = 0.05 fails in every cell. This does NOT make the condition independent of the labour market, because rho varies far more than omega does | **provisional**, corrected framing in A52 | A50, A52 | n/a | n/a | n/a | yes | n/a | n/a |
| 50 | In the tau_k = 0.10 column, 1 of 14 historical vintages met the condition (2000, the tightest labour market on record), and 0 of 14 in the central tau_l cell | **provisional**, sourced this session | A50 | n/a | n/a | n/a | n/a | n/a | n/a |
| 51 | Occupation switchers lose 42 percent of earnings against 21 percent for stayers, both relative to a no-displacement counterfactual (Huckfeldt 2022, verified); AI displacement forces switching, so R falls to 0.3837 as a labelled scenario | standing as a SCENARIO | A51 | n/a | n/a | n/a | n/a | n/a | n/a |
| 52 | tau_k is decomposable: tau_k = sigma_rent x (domestic share x 0.21) + (1 - sigma_rent) x tau_normal, and the project's 0.05/0.10/0.21 grid is AMR's own effective-rate series on software and equipment | **provisional**, sourced this session | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 53 | Under the current tax code WITH profit shifting, implied tau_k = 0.0708, below the 0.1101 needed at R = 0.5683, so the fiscal condition fails | **provisional**, sourced this session | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 54 | Profit shifting alone is enough to push tau_k below break-even: closed economy at 2010s rates gives 0.1386 against 0.1101 needed, applying the verified 48 percent haven share drops it to 0.1032 | **provisional**, sourced this session | A53 | n/a | n/a | n/a | yes | n/a | n/a |
| 55 | Raising the rent share does not rescue the condition under profit shifting, because a larger rent share puts more surplus into the shifted component | **provisional** | A53 | n/a | n/a | n/a | n/a | n/a | n/a |
| 56 | Of the additional nonemployed from robot exposure, about three quarters leave the labour force and one quarter remain unemployed | **VERIFIED**, in the published JPE article, Section V.C, PDF page 34, table A15. Used as the LONG-RUN (decade-plus) variant only | A54 corrected, A55 | n/a | n/a | n/a | n/a | n/a | n/a |
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
| 61 | The binding variable is the ANNUAL FLOW, not cumulative displacement | **amended** by A61: true only at phi = 0. For any phi above zero a cumulative ceiling of 36 to 61 percent also binds | A56, A61 | n/a | n/a | n/a | n/a | n/a | yes |
| 72 | Under the tight capital-formation cap (0.498 percent a year), displacing half the exposed embodied wage bill is physically unattainable at ANY horizon, so every fast scenario is cognitive-led | **provisional** | A62 | n/a | n/a | n/a | n/a | n/a | yes |
| 73 | Displacing 90 percent of the exposed embodied wage bill over 20 years raises unemployment to 5.11 percent against a 4.32 baseline | **provisional** | A62 | yes | n/a | n/a | n/a | n/a | yes |
| 74 | The size-driven (fiscal) failure mode fails in EVERY scenario including the mildest, because the condition already fails at zero displacement | **provisional**, and nearly tautological, flagged in the prereg before running | A62, A57, A58 | yes | n/a | n/a | n/a | n/a | yes |
| 75 | The speed-driven channel ACCELERATES with the displacement flow, producing a threshold | **SUPPORTED**, A62 refutation WITHDRAWN | A63: A62's negative curvature was an artifact of a circular hazard. On prime-age nonemployment the acceleration ratio is 2.33 to 2.63 on E/P, 1.75 to 2.03 on wage income, 2.39 to 2.59 on unemployment, R-squared 0.999 | yes | n/a | n/a | n/a | n/a | yes |
| 76 | The speed limit is 1.25 percent a year at a 10-year horizon (1.10 at phi = 1), two and a half times tighter than A56's 3.15 | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 77 | The cumulative ceiling is 11 to 12.5 percent of employment at 10 years, against A61's 31.5, and no 20-year path stays inside the observed range at any flow in the grid | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 78 | The FAST regime is nearly empty on the corrected slack measure: of 120 scenario paths, 58 SLOW, 62 SUDDEN, 0 FAST | **provisional** | A63 | n/a | n/a | n/a | n/a | n/a | yes |
| 79 | Attrition absorption is EXACTLY NEUTRAL for prime-age E/P, unemployment, wage income and the speed limit. It transfers the whole burden from laid-off incumbents to lost entrant openings | **provisional** | A64 | n/a | n/a | n/a | n/a | n/a | yes |
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
| 101 | Annual revenue loss ranges 0.00 to 21.09 percent of federal receipts across the grid; the HORIZON does almost all the work (90 percent of both types costs 42.4 percent of receipts a year over 2 years and 1.34 percent over 20) | **provisional** | A70 | yes | n/a | n/a | n/a | n/a | yes |
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

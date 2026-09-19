# MASTER PROMPT: PHASE 2

Paste this whole file into Claude Code. It supersedes the workstream order in PROJECT_BRIEF.md. All hard rules in PROJECT_BRIEF.md Section 4 still apply: no fabricated citations, no invented numbers, one-command rebuild, report against the thesis first, no em or en dashes, decisions logged with tradeoffs.

---

## 0. Context and change of direction

Phase 1 produced: a reproducible pipeline, a partial US Leg W, a Tier 2 Leg A, PAEI (911 occupations), DAR on ACS PUMS 2023, and a flat mortgage concentration result.

External review of Phase 1 concluded:

1. The flat debt-service-to-income result is partly mechanical. Underwriting caps DTI, so proportionality is produced by construction. It cannot be presented as a discovery on its own.
2. The claim "occupational diversification does not hedge a mortgage book" overreaches. A flat distribution does not stop an individual lender from selecting low-exposure borrowers. Retire that sentence. The defensible claims are: (a) the risk is unpriced and uniformly spread, so the system in aggregate cannot rotate out of it, and (b) occupation-based underwriting collides with fair lending law because occupation correlates with protected classes. Claim (b) needs legal sourcing (ECOA, Fair Housing Act, disparate impact doctrine) before it goes in the paper.
3. The mortgage channel runs through geography, not household DTI. Default needs an income shock plus negative equity, mortgage books are regional, and local house prices follow local wages.
4. PAEI as built measures exposure to current robotics, because it penalizes unstructured environments, which is exactly what Physical AI is supposed to overcome. It must become scenario-conditional.
5. The paper is now measurement-led. New order of sections: PAEI(c), DAR, holder map, framework as scaffolding, short architecture section. Primary target: Journal of Financial Stability. Fallback: Technological Forecasting and Social Change.

Update PROJECT_BRIEF.md to reflect points 1 to 5 before starting. Record the change in notes/decisions.md.

---

## Step 0. Fixes to Phase 1 (do these first, one session)

- **Household PAEI:** recompute as the earnings-weighted mean of PAEI across all earners in the household, not the reference person's occupation. Report how much results move.
- **Mortgage payment variable:** confirm whether the PUMS first mortgage payment includes property tax and insurance (check the inclusion flag variables). Build a consistent principal-and-interest measure where possible, otherwise document the contamination.
- **Renters:** add gross rent as a wage-backed obligation. Report owner and renter results separately and combined. Report tenure share by PAEI quintile.
- **Labor-linked federal receipts:** the 77.7 percent figure treats all individual income tax as labor-linked. Split individual income tax using IRS Statistics of Income (wages and salaries as a share of AGI, by year). Report a corrected central figure plus the 77.7 percent as an upper bound.
- **Leg A ratio:** report the 2.14 percent figure in notes/findings.md and in the paper as a labeled lower bound on on-balance-sheet Tier 2 exposure. Do not suppress it.
- **SEC access:** EDGAR's fair access policy requires a declared User-Agent containing a name and contact email, and a rate limit of 10 requests per second. Supplying that is compliance, not spoofing. Use the owner's name and email, set it in config, document it.
- **Citation check:** verify the BIS Quarterly Review March 2026 reference on off-balance-sheet data centre SPVs (title, authors, URL). If it cannot be verified, move it to lit/unverified.md and remove dependent claims.

---

## Step 1. Validate PAEI

Goal: establish that PAEI measures something real and something new.

Tasks:

- Obtain and crosswalk to a common occupation code: Webb (2020) exposure scores, which are separate for robots, software and AI; Felten, Raj and Seamans AIOE; Eloundou et al. GPT exposure; Frey and Osborne probabilities. Document every crosswalk (O*NET-SOC 2019, SOC 2018, SOC 2010, Census OCC) and the match rate at each hop.
- Report rank and Pearson correlations of PAEI, P and S separately against each index, employment-weighted and unweighted.
- Convergent validity: aggregate PAEI to industry and to commuting zone and compare with Acemoglu and Restrepo robot exposure and, if the owner supplies it, IFR robot density by industry. PAEI should predict where robots already are, because at c = 0 it is a current-robotics index.
- Discriminant validity: PAEI should correlate weakly or negatively with cognitive AI indices (Felten, Eloundou).
- Sensitivity: multiplicative versus additive versus geometric mean, alternative descriptor sets for P and S, leave-one-descriptor-out. Report rank stability (Spearman between variants, share of occupations changing quintile).
- Task-level audit: sample 200 O*NET tasks, score with two independent LLM raters plus the rubric, and flag 50 for owner review. Report inter-rater agreement (Cohen's kappa or Krippendorff's alpha).

Acceptance and gate: if PAEI correlates above roughly 0.8 with Webb's robot score, PAEI at c = 0 is not novel. Say so plainly. The novelty claim then rests entirely on PAEI(c) in Step 2. Do not massage the index to lower the correlation.

Outputs: data/processed/paei_validation.csv, notes/paei_validation.md, one correlation matrix figure.

---

## Step 2. Build PAEI(c), the scenario-conditional index

Goal: tie occupational exposure to the capability axis of the scenario framework.

Definitions: P is embodiment (0 to 1). S is environmental structure (0 to 1, where 1 is fully structured). c is realized Physical AI capability (0 to 1), where 0 is current industrial robotics and 1 is robust operation in unstructured environments.

Implement at least two functional forms and compare:

- Smooth: PAEI(c) = P * S^(1 - c). At c = 0 this is the current index. At c = 1 exposure equals embodiment alone.
- Threshold: occupation is exposed at capability c if (1 - S) <= c, with exposure magnitude P.

Tasks:

- Map scenario capability levels to c values (low, medium, high) and justify the mapping with reference to published robotics capability benchmarks where available. Label it a modeling assumption.
- Produce the exposure frontier: share of employment and share of wage bill exposed as a function of c. This curve is a headline figure.
- Identify the occupations that switch from unexposed to exposed between medium and high c (expected: construction trades, electricians, plumbers, maintenance, agriculture, care work with physical components). This is the distinctive content of "Physical AI" versus prior automation.
- Optional extension, clearly labeled: economic feasibility filter, exposure counts only where occupational hourly wage exceeds an assumed hourly robot cost. Keep it separate from technical exposure.

Outputs: data/processed/paei_c.csv (occupation by c grid), figures, notes/paei_c_method.md. Release-ready with a data dictionary.

---

## Step 3. Geographic DAR and the Leg W holder map

Goal: a bank-level ranking of exposure to Physical AI through household credit. This is the centerpiece empirical result.

Tasks:

- Compute, for each 2020 PUMA and each c level: wage bill at risk, mortgage debt service at risk, rent at risk, all as levels and as shares of local totals. Use person and household weights correctly and report standard errors using replicate weights.
- Crosswalk PUMA to county and to commuting zone using Geocorr allocation factors. Document the allocation error.
- Spatial concentration: Gini and top-decile share of debt service at risk across areas, Moran's I, and a map.
- Double trigger proxy: combine local DAR with local loan-to-value or house price level data (FHFA HPI, HMDA LTV) to flag areas where an income shock would coincide with thin equity.
- Lender mapping using HMDA Loan Application Register: originations by lender by county, with the purchaser type field used to separate loans retained in portfolio from loans sold to the GSEs or securitized. Lender exposure = sum over counties of retained lending share times county DAR(c). Cross-check against FDIC Summary of Deposits branch footprints and call report residential real estate balances.
- State the limitation clearly: HMDA is a flow of originations, not a stock of holdings. Use multiple years (2018 to latest) to approximate the stock.
- Produce: exposure ranking by lender, by lender size class (large, regional, community, credit union, nonbank), and the share of total DAR ultimately held by the GSEs. If most of it sits with the GSEs, then the exposure is effectively sovereign. That would be a major finding and must be reported whichever way it falls.

Outputs: data/processed/dar_geo.csv, data/processed/lender_exposure.csv, maps, notes/holder_map_W.md.

---

## Step 4. Pricing test

Goal: test whether lenders price local Physical AI exposure.

Pre-register first: write the full specification, sample restrictions, outcome variables and the interpretation of each possible result into notes/prereg_pricing.md and commit it before touching outcome data.

Specification:

- Outcomes: HMDA rate spread, denial indicator.
- Regressor of interest: county or tract-level PAEI(c) at c = 0 and at high c.
- Controls: LTV, DTI, applicant income, loan amount, loan type and purpose, occupancy, lender fixed effects, state by year fixed effects, local unemployment and house price growth. Cluster standard errors by county.
- Critical design point: conforming loans sold to the GSEs are priced off national grids, so a null there is mechanical. The informative sample is jumbo and portfolio-retained loans, where the lender bears the credit risk. Run both and report both, and lead with the portfolio sample.

Interpretation discipline: this is descriptive, not causal. A null on the portfolio sample means the risk is unpriced where lenders have both the incentive and the freedom to price it. A positive coefficient means partial pricing, which is also publishable. Report either honestly.

Outputs: tables, coefficient plots, notes/pricing_results.md.

---

## Step 5. Consumer credit, auto loans and liquid buffers

Goal: test whether the original concentration hypothesis survives outside mortgages, and whether equal debt service hides unequal default risk.

Data warning: the public SCF collapses occupation into a handful of broad groups, which is too coarse for PAEI. Decide as follows:

- Primary: SIPP (latest panel). It has detailed occupation, and balances for credit cards, vehicle loans, student loans and other debt, plus liquid assets. Check the actual variable availability before building.
- Secondary: PSID, if the owner can register for access.
- SCF: use only as a coarse cross-check at the broad occupation group level.

Tasks: by PAEI(c) quintile, report non-mortgage debt to income, total debt service to income where measurable, liquid assets in months of expenses, and the share of households with under one month of buffer. The hypothesis to test: high-PAEI households carry more unsecured and auto debt relative to income and hold thinner buffers.

Outputs: data/processed/dar_consumer.csv, notes/consumer_credit_results.md.

---

## Step 6. Leg A Tier 1 and the Leg A holder map

Goal: measure AI-linked credit where it actually sits.

Tasks:

- Build a deal-level table of data centre ABS, CMBS, private credit facilities, GPU-backed loans, and off-balance-sheet SPV financings. Sources: rating agency presale and sector reports (S&P, Moody's, Fitch, KBRA), SIFMA issuance data, company filings and 8-Ks, reputable financial press for private deals. Every row carries a source URL and a confidence label (hard, reported, estimated).
- Identify holders: insurers (NAIC statutory filings and schedule D where feasible), private credit funds, pension allocations to private credit, bank lending lines to private credit funds.
- Recompute the Leg A to Leg W ratio with Tier 1 plus Tier 2, as a range. Report the growth rate of Leg A. Then evaluate the brief's 5 percent criterion properly and write the verdict.
- Identify which holder classes appear on both holder maps. Those are the institutions to which the hedge failure proposition applies directly.

Outputs: data/processed/leg_a_tier1.csv, notes/holder_map_A.md, updated sizing table.

---

## Step 7. Formalize the threshold

Goal: one correct, teachable result.

Draft to verify, not to assume:

- For a task performed at wage w that a robot performs at all-in hourly cost c_r with equal output, the surplus per unit of displaced wage bill is s = 1 - c_r / w. Adoption begins when c_r falls just below w, which means s is near zero at the adoption margin. Early-transition automation is therefore so-so automation by construction, and s rises only as robot costs fall further. Check whether this holds once output expansion and price effects are included, and state the conditions.
- With tau the feasible effective tax rate on the surplus and d the debt service share of displaced income: legacy debt service can be preserved through redistribution only if tau * s >= d, which is equivalent to c_r / w <= 1 - d / tau. Full income replacement from taxing the surplus alone requires tau * s >= 1, which is impossible for tau below 1 without output expansion. Verify, and spell out what output growth would be required.
- Calibrate: d from DAR (Steps 0, 3, 5), tau from observed effective corporate tax rates, c_r from published robot cost and productivity data with sources. Produce the implied critical cost ratio and the c_r path needed for the transition to be self-financing.
- Write the hedge failure proposition formally inside the balance-sheet framework, with assumptions listed.
- State the open-economy case: if AI capital is foreign-owned, the taxable surplus accrues abroad and domestic tau is effectively lower. This is the India contrast case.

Outputs: framework/propositions.md with derivations, a small Python notebook reproducing the calibration, one figure of the feasibility region.

---

## Step 8. Finish the literature audit

- Complete the PRISMA-style protocol: databases, query strings, dates, inclusion criteria, counts at each stage, flow diagram.
- Add a practitioner and grey literature section covering the framing that is already circulating. The paper claims formalization and measurement, not first recognition.
- Add the climate transition risk and stranded assets literature as the methodological analogue.
- Add occupation exposure index literature for Steps 1 and 2.
- Verify every entry in references.bib. Fix the superseded title noted in Phase 1.

Outputs: lit/audit_report.md, lit/prisma_counts.csv, clean references.bib, empty lit/unverified.md or an explicit list.

---

## Order, gates and reporting

Order: Step 0, then 1, then 2. Steps 3 and 8 can run alongside 2. Step 4 needs 3. Steps 5, 6 and 7 follow in that order, except that the Step 7 derivations can start any time.

Stop and report to the owner at these gates:

1. After Step 1: is PAEI at c = 0 novel or not.
2. After Step 3: where Leg W exposure sits (GSEs, large banks, regional banks, nonbanks).
3. After Step 4: priced or unpriced.
4. After Step 6: the two-sided versus lopsided verdict.

At each gate write to notes/findings.md using this structure: what was tested, the result, what it does to the thesis, what it rules out, what remains unknown. Lead with anything that weakens the thesis.

Finish Phase 2 by rewriting the paper outline in paper/outline.md around whatever the data showed, not around what this prompt expected.

# Decisions

Architectural and methodological decisions, with the tradeoff. Per PROJECT_BRIEF.md Rule 7,
decisions are made here and only escalated when irreversible or thesis-changing.

---

## D1. Series metadata is fetched, never asserted (2026-09-19)

Every FRED series is pulled together with its published title, units, frequency, seasonal
adjustment, source and last-updated date, stored in data/raw/fred/_manifest.json, and unit
scaling in the build is driven by the fetched units string.

Why: the first draft of src/sources.py hard-coded units from memory and got CMDEBT wrong
(millions, not billions), which would have understated US household debt by a factor of
1000. It also mislabelled four series, two of which (W019..., A576...) were the wrong
series entirely and one of which was discontinued.

Tradeoff: two HTTP requests per series instead of one, and the build fails if FRED changes
its page markup. Accepted: a silently wrong unit is far more costly than a loud failure.

## D2. Labor-tax dependence uses federal CURRENT RECEIPTS as the denominator (2026-09-19)

NIPA classifies contributions for government social insurance outside "current tax
receipts". Dividing labor-linked receipts by current TAX receipts yields 125 percent, which
is impossible and was caught for that reason.

Decision: denominator is federal current receipts (FGRECPT). Numerator is federal personal
current taxes (A074RC1Q027SBEA) plus federal contributions for government social insurance
(W780RC1Q027SBEA), both federal-only.

Tradeoff: excludes state and local labor taxation, so 77.7 percent understates the
all-government labor dependence. An all-government version is a later extension; the
federal figure is the one tied to the federal debt stock in Leg W, so it is the right
match for the thesis.

## D3. Leg W household and sovereign components are reported separately (2026-09-19)

The combined "Leg W broad" figure (186.1 percent of GDP) is a memo line only.

Why: household debt and federal debt are claims on the wage bill through different
mechanisms, held by different sectors, with different default and restructuring
technologies. Summing them implies a consolidation that does not exist and would invite a
referee to dismiss the headline number.

Tradeoff: a less dramatic headline. Accepted, per brief Section 8.8 (restraint).

## D4. Leg A definition gains a Tier 2b for off-balance-sheet financing (2026-09-19)

The brief's Tier 2 is hyperscaler capex from filings, split by funding source. BIS QR March
2026 documents that data-centre debt is commonly held in SPVs with the hyperscaler as
minority equity plus a long-term lease, deliberately off the hyperscaler balance sheet.

Decision: add Tier 2b, off-balance-sheet and SPV-financed data-centre debt, sourced from
BIS and private-credit aggregates, labelled as estimates with method shown. Filings-based
Tier 2 is reported as a LOWER BOUND, never as the measure.

Tradeoff: Tier 2b cannot meet the same evidentiary standard as filings data. Mitigated by
reporting all tiers separately and never blending an estimate into a hard-data total.

Consequence for the WS1 kill criterion: it must be evaluated on Tier 1 + Tier 2 + Tier 2b.
Evaluating it on filings alone would return a false "lopsided" verdict, because the
structures exist precisely to keep that debt out of the filings.

## D5. The exposure index is pulled forward from WS7 into the main paper (2026-09-19)

The brief defers occupational exposure work to WS7 as an optional sequel, and designates
the sizing table plus holder map as the paper's citable artifact.

Decision: build the Physical AI Exposure Index (PAEI) now, in the main paper.

Why:
- The brief's own Section 7.4 requires "one original quantitative artifact". The sizing
  table is an aggregation of existing official statistics; it is useful but it is not new
  measurement, and it is the kind of table that is superseded the moment an official body
  publishes its own.
- PAEI is new measurement. No existing index scores exposure to PHYSICAL AI specifically;
  the established measures (Frey-Osborne, Felten et al., Webb, Eloundou et al.) score
  cognitive or generic automation exposure.
- It is what makes the central hypothesis testable. The claim that Physical AI exposure
  concentrates in mid-income, high debt-to-income households is currently Tier 2
  ("our hypotheses, unverified") and cannot move to Tier 1 without an exposure measure to
  join to household debt microdata.
- Without it the paper is a taxonomy plus a threshold. With it the paper has an object
  other researchers must cite and can extend.

Tradeoff: scope growth in a paper already targeting 9,000-11,000 words, and the index
invites methodological attack that a pure framework paper would avoid. Accepted: the attack
surface is the point, because a measure that cannot be attacked cannot be used.

## D6. PAEI is multiplicative in two orthogonal factors, not an additive score (2026-09-19)

PAEI = P * S, P = embodiment intensity, S = environmental structure.

Why multiplicative: a robot displaces a task only if the task needs a body AND the
environment is structured enough to act in. Either condition failing means no exposure. An
additive index would score a high-embodiment, low-structure job (emergency plumber) as
highly exposed, which is the single most common error in this literature and is exactly
what Moravec's paradox predicts against.

Validation that this is not cosmetic: electricians score higher embodiment than team
assemblers (0.679 vs 0.551) but lower PAEI (0.256 vs 0.322). Correlation between P and S
across 911 occupations is -0.06, so the factors are close to orthogonal and the second
factor is doing real work.

Tradeoff: multiplicative form makes the index harder to decompose in regressions, and the
midpoint rescaling of S (enablers equal to frictions maps to 0.5) is a normalisation choice
that must be justified and sensitivity-tested. Both P and S are therefore published
alongside PAEI in data/processed/paei_onet.csv so others can re-aggregate.

## D7. Normalisation uses O*NET published scale anchors, not min-max (2026-09-19)

Each element is mapped to [0,1] using the minimum and maximum from O*NET's
Scales Reference.txt, not the observed range across occupations.

Why: min-max normalisation makes the index a purely relative ranking that silently changes
whenever O*NET adds or revises occupations, destroying comparability across releases. The
brief commits to annual updates of the artifact (Section 8.2), which requires a measure
that is stable across vintages.

Tradeoff: the index does not use the full [0,1] range (observed PAEI runs 0.02 to 0.43),
which looks less striking. Accepted; comparability matters more than presentation.

## D8. SEC filings are not accessed with a spoofed browser user-agent (2026-09-19)

SEC returns 403 to this environment with the message "Your Request Originates from an
Undeclared Automated Tool". A standard browser user-agent string succeeds.

Decision: do not do that. SEC's fair-access policy asks automated users to declare
themselves with a contact address. Escalated to the owner instead, as open question Q1.

Tradeoff: WS1 Tier 2 is blocked this session. Accepted; misrepresenting the client to a
regulator's data service to build a paper about financial regulation is not a trade worth
making, and a referee who learned of it would be entitled to distrust the whole pipeline.

---

# PHASE 2

## D9. Phase 2 repositioning accepted in full (2026-09-19)

External review moved the paper from framework-led to measurement-led, retired one claim,
and made PAEI scenario-conditional. PROJECT_BRIEF.md Section 1.1 records the five changes.
Primary venue changes from TFSC to Journal of Financial Stability.

Why accepted without pushback: every one of the five points is a correction to something
Phase 1 actually got wrong or overstated, and three of them (mechanical flatness, the
retired diversification claim, PAEI measuring current robotics) were errors this pipeline
produced. The review is right.

Tradeoff: the scenario and foresight apparatus that justified the TFSC target becomes
scaffolding, and the paper now lives or dies on measurement quality. Accepted.

## D10. Household PAEI is the earnings-weighted mean over earners (2026-09-19)

Phase 1 attributed each household's debt service across PAEI quintiles in proportion to
each earner's wage share. That is a different estimand and it mechanically pulls every
mixed-occupation household toward the middle, which manufactured the flat result.

Decision: the household's exposure is the earnings-weighted mean of PAEI across its
earners, and the household is assigned whole to one quintile.

Movement, measured rather than assumed:
- correlation with reference-person PAEI 0.845; 28.2 percent of households change quintile
- correlation with highest-earner PAEI 0.959; 18.4 percent change quintile

Tradeoff: a single scalar cannot represent a household where one earner is fully exposed
and another is not. The earnings weighting is the right first-order choice because it is
the income at risk that matters, but a two-earner dispersion measure should be added later.

## D11. Mortgage payments are decontaminated using MRGT and MRGI (2026-09-19)

PUMS MRGP may include real estate taxes (MRGT == 1) and fire, hazard and flood insurance
(MRGI == 1). Phase 1 used MRGP as if it were debt service.

Only 21.0 percent of mortgage households report taxes AND insurance paid separately. The
mean annual payment is 20,057 USD on the full sample against 17,629 USD on the clean
subsample, so the contamination is 13.8 percent.

Decision: report both. The clean principal-and-interest subsample is the headline for any
debt-service claim; the full sample is reported for coverage, labelled as housing outlay
rather than debt service.

Tradeoff: the clean subsample is only a fifth of mortgage households and is not random
(escrow is more common on high-LTV and FHA loans), so it likely under-represents
higher-leverage borrowers. Flagged as a limitation rather than corrected, because
correcting it needs a selection model the data cannot support.

## D12. ADJHSG applied to housing amounts (2026-09-19)

The PUMS dictionary instructs that MRGP and GRNTP be adjusted by ADJHSG. Phase 1 did not.
For the 2023 single-year file ADJHSG is exactly 1.000000, so nothing moves numerically, but
the omission would have been a real error on any multi-year build. Applied programmatically.

## D13. Renters are in scope (2026-09-19)

Gross rent is a wage-backed housing obligation. Excluding renters excluded 45 percent of
the households in the most exposed PAEI quintile, which is where the thesis expects the
exposure to be. Owner, renter and combined results are now reported separately.

## D14. The income confound is tested before any gradient is reported (2026-09-19)

The Step 0 rebuild produced a steep raw gradient (concentration ratio 0.87 to 1.44,
combined housing burden 15.6 to 27.9 percent). It would have been easy and wrong to report
that as confirmation of the brief's hypothesis.

Housing costs are less than proportional to income, and PAEI correlates negatively with
wages, so an income effect alone produces exactly that gradient. Decision: no PAEI gradient
is reported without a within-income-band test and a direct-standardisation estimate.

Result: the gradient reverses sign in 10 of 10 income deciles, on both a wage-income and a
total-income denominator. See findings A6.

Tradeoff: none. This test is cheap and it is the difference between a result and an
artifact.

## D15. Labor-linked federal receipts are split by the SOI wage share of AGI (2026-09-19)

Phase 1's 77.7 percent treated all federal personal current taxes as labor-linked.
Individual income tax also falls on capital gains, dividends, interest, business and
retirement income.

Decision: scale personal current taxes by the wage and salary share of AGI from IRS SOI
Table 1.4, leaving social insurance contributions unscaled. Central estimate 63.4 percent;
77.7 percent retained and labelled as the upper bound.

Wage share of AGI: 61.0 percent (2021), 65.7 percent (2022), 66.8 percent (2023). The 2021
dip is the capital gains realisation spike, which is exactly the volatility this correction
exists to capture.

Tradeoff: the wage share of AGI is not the wage share of TAX. Progressivity plus the
concentration of capital income in top brackets means the true labor-linked share of
liability is plausibly below 63.4 percent, so the central figure is still an upper bound,
just a much tighter one. A bracket-level calculation needs SOI liability-by-source data and
is deferred.

## D16. SEC User-Agent moved to src/config.py with the owner's name and address (2026-09-19)

D8 declined to spoof a browser user-agent. The correct route, which SEC publishes, is to
declare a real name and contact email and stay under 10 requests per second. Both are now
in src/config.py, with the policy URL, and the fetcher imports them. Verified: HTTP 200.

This supersedes the "blocked" status in D8. D8's reasoning stands; only the resolution
changed, from blocked to compliant.

## D17. S_original retained over S_text, with the construct tension disclosed (2026-09-19)

A4 built an independent S from O*NET task text using two LLM raters on a fixed rubric.

Reliability of the rubric is excellent: Krippendorff alpha 0.879 to 0.971 per dimension and
0.967 for the composite. Validity against S_original is 0.306, below the owner's 0.5
threshold. Because the raters agree with each other far more than either agrees with
S_original, the gap is a construct difference and not rater noise.

Arbitration by the A3 adoption test, as the owner's rule directs: on the full 200-occupation
sample S_original predicts robot adoption (Spearman +0.187, p = 0.008) and S_text does not
(+0.011, p = 0.873). On the high-P subsample the two are within 0.03 and neither is
significant, so that comparison is inconclusive.

Decision: retain S_original; report S_text as a robustness check.

Tradeoff, and it is a real one. S_text is the better-scaled measure (sd 0.271 against 0.071
in the same sample), and its compression is exactly the defect that forced the rank
transform in Step 2. Retaining S_original keeps a compressed scale whose rank transform
creates the identity noted in A14. The deciding consideration is external prediction, not
scale aesthetics: only S_original tracks observed adoption.

The test was also biased toward S_original, because the A4 sample was stratified on
S_original's rank and so guarantees it full spread. That is disclosed rather than corrected,
and it is the reason this decision is recorded as provisional: if a future, unstratified
comparison reverses it, switch.

Consequence for the paper: two internally reliable operationalisations of environmental
structure correlate at 0.31. That belongs in the limitations section as a measurement
problem the paper discloses rather than resolves.


## D18. Pathway decomposition replaces c as the paper's primary structure (2026-09-19)

Item 2 of Block 3 showed that S's association with observed robot adoption is largely
industry composition (A23). Combined with A19 (an independent rubric reproduces S at only
r = 0.31) and A21 (S is null against Webb's task-level robot potential), there is no clean
external result supporting S as an occupation-level construct.

Decision, per the owner's standing instruction in Block 3 item 2: the three-pathway
decomposition (manipulation robotics, autonomous driving, accountability or interpersonally
gated work) becomes the paper's primary organising structure. PAEI(c) and the capability
parameter c are demoted to a robustness section.

Why this is the right call rather than a retreat: the pathway split is built on P and on
occupation-level flags, neither of which depends on S's contested external validity, and A18
already showed the pathways carry most of the magnitude (excluding all three removes 72
percent of the wage bill at risk at c = 1). The paper's quantities survive; only the
organising axis changes.

Tradeoff: the scenario-conditional index was the most novel single artifact and it now sits
in robustness. Accepted. A measure whose novel component has no clean external validation
cannot carry a paper's headline.

## D19. Robots and Jobs package no longer pursued; 114030 identified (2026-09-19)

`114030-V1.zip` is the replication package for Acemoglu and Restrepo, "Automation and New
Tasks", JEP 33(2), 2019. It contains the Survey of Manufacturing Technology, NBER-CES, KLEMS
and SIC/NAICS tables, and NO commuting-zone or IFR robot series. Owner instruction: stop
pursuing the Robots and Jobs (JPE 2020) package. The commuting-zone replication of A3 closes
unbuilt, which is moot because A3 itself is now closed (A27).

Tradeoff: we lose the one design that could have given commuting-zone robot exposure
directly. Accepted, because the SMT test in the package turned out to be the better test
anyway: it has within-manufacturing variation, which the commuting-zone measure does not.

## D20. Step 4, the HMDA pricing test, is DROPPED (2026-09-19)

Owner instruction, with the justification run as Block 4 item 6 in short form.

The registered test regresses HMDA rate spreads on local PAEI(c) exposure. It cannot be
informative at either end of the capability range:

**At high c the test is underpowered.** The at-risk rate across counties at high capability
has a p90/p10 ratio of about 1.4 to 2.0 and a Gini around 0.06 to 0.13 (A25). Standardised,
that is a regressor with very little cross-sectional spread. Detecting a risk premium
requires the coefficient on a near-degenerate regressor to clear the residual variance of
loan-level rate spreads, and rate spreads are dominated by borrower credit characteristics,
lock timing and lender pricing policy. A null would be uninformative about whether the risk
is priced, because the test could not have detected pricing had it existed.

**At low c the test is confounded.** There the exposure IS manufacturing geography
(A28: robot-reachable work has a county p99/p1 of about 9, matching Acemoglu and Restrepo's
robot exposure). Any coefficient would be competing with the China shock, manufacturing
decline, and local house-price dynamics, which is precisely the identification problem
Acemoglu and Restrepo devoted an entire paper and a European instrument to solving. We have
no instrument.

I am NOT reporting a numeric minimum detectable effect. Doing so honestly requires a
verified figure for the residual variance of HMDA rate spreads from a published study, and I
did not obtain one. Inventing a plausible-looking number to dress up the argument would
violate Rule 2. The structural argument above stands on the dispersion figures we did
measure.

Tradeoff: we lose the "is the risk priced" result, which would have been a clean and
quotable finding either way. Accepted. The consequence for the owner is concrete: **do not
download HMDA.** notes/prereg_pricing.md is retained as the record of a registered test that
was dropped for power and identification reasons before any outcome data was seen, which is
the correct disposal of a pre-registration.

## D21. A4 resample dropped (2026-09-19)

Owner instruction. The A4 adjudication sample was stratified on S_original; with S closed
permanently (A27) there is nothing left for a resample to adjudicate. The existing
`a4_50_for_owner_review.csv` is retained as a record, not as a live work item.

## D22. Scope change: the paper covers AI-driven labour displacement generally (2026-09-19)

Owner decision. The paper is reorganised around two exposure types: embodied (P, validated
against Webb at +0.708 overall and +0.275 among high-P) and cognitive (Felten AIOE and
Eloundou, already crosswalked). "Physical AI" becomes one half of a comparison rather than
the subject.

Why the evidence supports this: the cognitive contrast (A35) shows the household-credit leg
sits with cognitively exposed workers, and the fiscal wedge per displaced dollar is LARGER
for cognitive work. A paper framed only on Physical AI would have to either omit or
under-report both.

Tradeoffs:
- LOSS. The single most defensible measurement asset, PAEI and its pathway decomposition,
  becomes one column of a comparison. The geography result (robot-reachable work concentrated
  at Acemoglu-Restrepo magnitudes, embodied work near-uniform) is specific to Physical AI and
  is diluted by the broader frame.
- LOSS. Scope grows again after a freeze, and the cognitive side has no equivalent of the
  pathway decomposition or the validated embodiment measure.
- GAIN. The comparison is what the data actually supports, and the contrast is sharper than
  either half alone.
- GAIN. The fiscal result (P1r) is exposure-type agnostic and gets stronger, not weaker.

BINDING CONSTRAINT on all cognitive claims: Felten AIOE and Eloundou measure TASK OVERLAP,
not displacement and not timing. Every claim about cognitive exposure must say so. Unlike P,
which was validated against Webb's robot score, the cognitive indices are used here as
published measures of overlap with no independent validation by us.

# Findings

Running log. Per PROJECT_BRIEF.md Rule 5, results that weaken the thesis are written up
first and prominently. Every number below traces to a file in data/raw and a series entry
in data/SOURCES.md.

Session 1: 2026-09-19.

---

## A. Results that cut AGAINST the thesis

### A1. The "two-sided bet" framing is already in circulation among practitioners

WS0 query family F4 surfaced practitioner commentary that states the two-sided structure
almost exactly: that the AI economy presents "loans threatened by AI disruption, and loans
made to build AI's physical infrastructure", and that private credit faces "2 distinct AI
risks" (a credit-quality issue on borrowers disrupted by AI, and a collateral/structure
issue on GPU- and compute-backed lending).

What this changes:
- The framing is NOT unclaimed intellectual territory in the way the brief assumed. It is
  unclaimed in the *academic* literature so far, but it is visibly in the air in 2026
  practitioner writing.
- Scholarly priority is unaffected (Tier D sources carry no priority), but the rhetorical
  position is. Writing as though this framing is a discovery will read as naive to exactly
  the central-bank audience the brief targets, who read this commentary.
- Required change: the paper must CITE the practitioner framing and position its
  contribution as formalisation, measurement and architecture, not as recognition. The
  novelty statement in Section 3 of the brief survives verbatim, because it already claims
  only the framework/mapping/derivation combination. Keep using it.

Status: reshapes framing. Does not trigger the kill criterion (no academic framework yet
found holding both legs jointly). WS0 Q3 screening continues.

### A2. Leg A is materially larger than any filings-based measure will show

The BIS Quarterly Review (March 2026) feature on financing the AI infrastructure boom
documents that a common structure places data-centre assets in a dedicated vehicle, with
the hyperscaler holding a minority stake and committing to long-term operating leases,
keeping most of the associated debt OFF the hyperscaler's balance sheet.

What this changes:
- The brief's WS1 Tier 2 (hyperscaler capex from 10-K filings, split by funding source) is
  systematically biased DOWNWARD as a measure of AI-linked debt. It measures the balance
  sheet that the structure was designed to keep clean.
- The kill criterion in WS1 ("if Tier 1 + Tier 2 debt-financed Leg A is under roughly 5
  percent of Leg W in every economy") must therefore NOT be evaluated on filings alone. A
  filings-only test would produce a false "lopsided" verdict.
- Required change: add a Tier 2b to the sizing definition covering off-balance-sheet and
  SPV-financed data-centre debt, sourced from BIS and from private-credit industry
  aggregates, explicitly labelled as estimates. Recorded in notes/decisions.md as D4.

Status: reshapes method. Strengthens Leg A, so it cuts against the "lopsided" reframing,
but it cuts against the brief's stated measurement plan, which is why it is logged here.

### A3. A closely adjacent formal paper already places the US near the regime boundary

Bayraktar (2026), "Automation, Income Incidence, and Capital Accumulation in Incomplete
Markets" (arXiv 2605.05127), builds a heterogeneous-agent incomplete-markets model in which
automation outcomes hinge on exposure of high-MPC households, ownership concentration,
capital obsolescence and skill mobility. Its abstract states that a proxy diagnostic
"places the current economy near the boundary between the two scenarios".

What this changes:
- This is the nearest formal competitor found so far. It covers ownership concentration and
  distributional incidence, which overlaps our Axis 2 and part of the tau*s logic.
- It does NOT carry legacy debt stocks, bank balance sheets, or a Leg A exposure, so Q3 is
  not satisfied and the kill criterion is not triggered.
- Required change: this paper must be engaged directly in the framework section, and our
  differentiation stated explicitly as the debt-stock and financial-intermediary channel.

NOTE, citation correction: the brief's Section 3 cites this as arXiv 2026 "The Demand
Externality of Automation". That is a superseded v1 title. The current title is as given
above. Do not cite the old title.

### A4. The central empirical hypothesis is REFUTED in its strong form (DAR, US)

PROJECT_BRIEF.md Section 3 lists as a Tier 2 hypothesis: "That Physical AI exposure
concentrates in mid-income, high debt-to-income households." This was tested this session
and does not hold in its strong form.

Method: PAEI joined to ACS PUMS 2023 (3,405,809 person records, 1,620,290 households) via
the 2018 Census OCCP-to-SOC crosswalk. 96.6 percent of OCCP codes matched, covering 90.7
percent of weighted wage income. Mortgage-holding households: 50.2 million weighted, with
1,007.5 USD bn of annual mortgage-related outlay (MRGP x 12).

Result, mortgage debt service by PAEI quintile of the earner:

| PAEI quintile | Wage income (USD bn) | Share of wage income | Mortgage service (USD bn) | Share of service | Concentration ratio | Service/income |
|---|---|---|---|---|---|---|
| q1 (least exposed) | 3,277.1 | 33.2% | 264.4 | 32.2% | 0.97 | 8.07% |
| q2 | 2,314.3 | 23.5% | 199.4 | 24.3% | 1.04 | 8.62% |
| q3 | 1,749.8 | 17.7% | 157.6 | 19.2% | 1.08 | 9.01% |
| q4 | 1,340.5 | 13.6% | 107.4 | 13.1% | 0.96 | 8.01% |
| q5 (most exposed) | 1,188.6 | 12.0% | 91.7 | 11.2% | 0.93 | 7.72% |

Two readings, both of which must appear in the paper:

1. In LEVELS, mortgage debt service is concentrated in the LEAST exposed quintiles. q1
   carries 32.2 percent of mortgage service, q5 carries 11.2 percent. Most US mortgage debt
   is serviced out of wages that Physical AI does not directly threaten. This is largely
   mechanical: high-PAEI occupations earn less and reach mortgaged homeownership less often.

2. In INTENSITY, the concentration ratio is flat. It runs 0.97, 1.04, 1.08, 0.96, 0.93
   across quintiles, and debt-service-to-income varies only between 7.7 and 9.0 percent.
   There is a faint mid-distribution hump at q2 and q3, which is the direction the brief's
   hypothesis predicted, but the magnitude is about 8 percent above proportional. That is
   far too small to carry the claim as stated.

Verdict: the hypothesis moves from Tier 2 ("our hypotheses, unverified") to REFUTED in its
strong form and WEAKLY SUPPORTED in direction only. It must not be asserted in the paper.

### A5. What replaces it, and why it is a stronger claim

The flatness in A4 is itself the result, and it is more useful than the concentration the
brief expected.

    Mortgage debt service is close to proportional to wage income at every level of
    Physical AI exposure. Therefore occupational diversification does not hedge a mortgage
    book against Physical AI.

If mortgage exposure had been concentrated in high-PAEI occupations, a lender could manage
it by underwriting standards and portfolio mix, and the problem would be a credit-selection
problem. Because the ratio is flat, there is no low-exposure pocket of household credit to
rotate into. A lender holding a representative mortgage book holds displacement risk in
proportion to the wage bill itself, and cannot diversify it away within the asset class.

This is a sharper and more testable statement than the original hypothesis, it is
consistent with the hedge-failure proposition (it makes Leg W harder to hedge, not easier),
and it points the architecture section toward instruments that act on the CONTRACT
(income-contingent and shared-responsibility structures, which are stock-side) rather than
on portfolio composition, which cannot work.

Caveats that must travel with this result:
- It measures debt SERVICE, not a debt STOCK. PUMS carries no mortgage balance.
- It covers MORTGAGES only. Consumer credit, auto loans and rent arrears are where low-wage
  high-PAEI workers actually concentrate, and PUMS cannot see them. The strong form of the
  brief's hypothesis may yet hold on those instruments. This is now the priority test and
  requires SCF or credit-bureau microdata.
- Occupation is measured at a point in time and says nothing about displacement timing.
- MRGP includes escrowed taxes and insurance where the respondent reports them there, so
  it overstates pure debt service by an unknown amount.

---

## B. Results that SUPPORT the thesis

### B1. The sovereign side of Leg W is overwhelmingly labor-backed (US)

From NIPA via FRED, 2026 Q2 (annual rates, USD bn):

| Item | Value |
|---|---|
| Federal personal current taxes | 2,571.4 |
| Federal contributions for government social insurance | 2,074.4 |
| Federal labor-linked receipts (sum) | 4,645.8 |
| Federal current receipts (total) | 5,980.6 |
| **Labor-linked share of federal current receipts** | **77.7 percent** |

This is the cleanest single number produced this session. It quantifies the brief's claim
that sovereign debt is "serviced from payroll and income tax" and makes the sovereign leg
of Leg W concrete rather than asserted. Roughly four fifths of US federal current receipts
are a claim on the wage bill.

Methodological note: NIPA books social insurance contributions OUTSIDE "current tax
receipts", so the denominator must be federal CURRENT RECEIPTS. Using federal current tax
receipts as the denominator produces 125 percent, which is the error this note exists to
prevent. Logged as decision D2.

### B2. Leg W stock, United States

2026 Q2 unless noted, USD bn, share of GDP at annual rate (GDP 32,486.1):

| Component | USD bn | Percent of GDP |
|---|---|---|
| Household debt, total (Z.1) | 21,377.8 | 65.8 |
| of which home mortgages, 1-4 family | 14,010.9 | 43.1 |
| of which consumer credit | 5,120.3 | 15.8 |
| of which federal student loans held | 1,605.1 | 4.9 |
| Federal public debt, total (2026 Q1) | 39,065.4 | 120.3 |
| **Leg W broad (household + federal)** | **60,443.2** | **186.1** |

Supporting flows: wage and salary accruals 13,365.2; compensation of employees 16,224.3;
wage share of gross domestic income 42.7 percent; household debt service 11.16 percent of
disposable personal income.

Caveat, stated now so it is not overstated later: adding household debt to federal debt is
a presentational aggregate, not a consolidated exposure. The two are serviced by different
claims on the wage bill and are held by different sectors. The headline ratio in the paper
should present them separately, with the sum shown only as a memo line.

### B3. The Physical AI Exposure Index separates the Moravec region as designed

Built from O*NET 31.0 for 911 occupations. Two factors, multiplicative:
PAEI = P * S, where P is embodiment intensity and S is environmental structure
(enablers minus Moravec frictions, rescaled to [0,1]).

The discriminating test, which a generic "manual work" index would fail:

| Occupation | P (embodiment) | S (structure) | PAEI |
|---|---|---|---|
| Team Assemblers | 0.551 | 0.584 | 0.322 |
| Stockers and Order Fillers | 0.571 | 0.534 | 0.305 |
| Electricians | 0.679 | 0.377 | 0.256 |
| Plumbers, Pipefitters, Steamfitters | 0.651 | 0.391 | 0.254 |
| Construction Laborers | 0.658 | 0.378 | 0.249 |
| Software Developers | 0.132 | 0.511 | 0.068 |

Electricians are MORE physically demanding than team assemblers (0.679 vs 0.551) and yet
LESS exposed to Physical AI (0.256 vs 0.322), because their work environment is
unstructured. That inversion is the whole point of the index and is what distinguishes it
from Frey-Osborne-style and from cognitive-AI exposure measures.

Correlation between P and S across 911 occupations is -0.06, essentially orthogonal. The
two factors therefore carry independent information and the index is not a repackaging of a
single physicality scale.

Top of the distribution: tire builders, heat-treating equipment operators, postal mail
sorters, meat and poultry cutters, adhesive bonding machine operators, textile machine
operators, semiconductor processing technicians. Bottom: personal financial advisors,
economists, genetic counselors, therapists. Face validity holds at both ends.

Status: this is the strongest candidate for the paper's one citable artifact. See
notes/decisions.md D5 for why it was pulled forward from WS7.

### B4. Leg A is small, but concentrated and levered where it exists (US, Tier 2)

SEC access resolved 2026-09-19 (owner supplied a declared contact address). Tier 2 built
from 10-K filings for 10 firms; 9 have current facts.

| Firm | Capex (USD bn) | OCF (USD bn) | Self-funding | LT debt | Finance leases |
|---|---|---|---|---|---|
| Amazon | 131.8 | 139.5 | 1.06 | 65.7 | 10.7 |
| Microsoft | 116.0 | 182.9 | 1.58 | 31.1 | 66.6 |
| Alphabet | 91.5 | 164.7 | 1.80 | 46.6 | 2.1 |
| Meta | 69.7 | 115.8 | 1.66 | 58.7 | 0.9 |
| Oracle | 55.7 | 32.0 | 0.57 | 129.5 | 7.1 |
| CoreWeave | 10.3 | 3.1 | 0.30 | 14.7 | 0.2 |
| Tesla | 8.5 | 14.8 | 1.73 | 6.6 | 0.2 |
| Equinix | 4.3 | 3.9 | 0.91 | 15.3 | 2.2 |
| Digital Realty | 3.2 | 2.4 | 0.76 | n/a | 0.3 |
| **Total** | **490.9** | **659.1** | **1.34** | **368.1** | **90.2** |

The headline comparison, on Tier 2 alone:

| Comparison | Value |
|---|---|
| Leg A debt and leases / US household debt | 2.14% |
| Leg A debt and leases / Leg W broad | 0.76% |
| Leg A capex / GDP | 1.51% |

2.14 percent is below the brief's 5 percent WS1 kill threshold. Per decision D4 this does
NOT trigger the reframing, because Tier 2 excludes exactly the off-balance-sheet structures
that BIS identifies as dominant (finding A2). Leg A has so far been measured only in the
place it is least likely to be found. Tier 1 and Tier 2b must be built before the criterion
is evaluated. No "the bet is lopsided" conclusion should be drawn or quoted yet.

What Tier 2 does establish, independent of the size question, is the shape of Leg A:

    The hyperscalers fund AI capex from operating cash flow and are not adding credit
    exposure at the margin. The firms that cannot self-fund are Oracle (0.57), CoreWeave
    (0.30) and the data-centre REITs (0.76 to 0.91). Leg A credit risk is concentrated
    there.

This is a different financial-stability object from the brief's "overinvestment bust"
language, which implicitly treats Leg A as a large diffuse exposure. A small, concentrated,
levered exposure held by identifiable non-bank lenders maps to a different regime in WS4
and raises the value of the holder map (WS2) for Leg A as well as for Leg W.

Data-quality note: a first build read Amazon capex as 6.7 USD bn and Equinix as 0.01 USD bn
because both firms changed us-gaap tags and the build had taken the latest fact under a
single tag. The build now searches candidate tags per concept, takes the most recent fiscal
year across them, rejects facts older than 2024, and records the chosen tag for every cell.
See notes/sizing_method.md.

---

## C. Open, not yet evidence either way

- Relative size of Leg A versus Leg W: Tier 2 measured (B4), Tiers 1 and 2b not. The
  ratio is therefore a lower bound of unknown tightness and must not be quoted as the
  answer.
- Holder map (WS2): not started.
- The tau*s threshold: not yet checked or tightened. No derivation work done this session.
- Whether high-PAEI households hold disproportionate CONSUMER credit, auto debt or rent
  arrears. Untested and now the highest-value open question, because the mortgage answer
  (A4) came back flat and the consumer-credit answer is where the brief's hypothesis is
  most likely to survive. Needs SCF or credit-bureau microdata; ACS PUMS cannot see it.
- The mortgage DEBT STOCK version of DAR, as opposed to debt service. Needs SCF.

---

# PHASE 2

Session 2: 2026-09-19. Structure per MASTER_PROMPT_PHASE2.md: what was tested, the result,
what it does to the thesis, what it rules out, what remains unknown. Anything that weakens
the thesis leads.

## A6. STEP 0 GATE. The concentration hypothesis is refuted decisively, on a better measure

**What was tested.** Phase 1 found a flat concentration ratio and I reported the flatness
itself as the result. Phase 2 Step 0 required four corrections: household PAEI as the
earnings-weighted mean over earners rather than a share-attribution of debt service;
mortgage payments decontaminated using the MRGT and MRGI inclusion flags; renters added;
ADJHSG applied. The rebuilt measure was then tested against the obvious confound.

**Result, stage 1.** On the corrected measure the gradient is NOT flat. It is steep and
monotone:

| Measure | q1 | q2 | q3 | q4 | q5 | q5 burden |
|---|---|---|---|---|---|---|
| Owner mortgage, all | 0.87 | 1.00 | 1.01 | 1.08 | 1.37 | 21.6% |
| Owner mortgage, clean P&I | 0.87 | 1.01 | 1.04 | 1.13 | 1.44 | 17.8% |
| Renter gross rent | 0.81 | 0.96 | 0.98 | 1.06 | 1.26 | 34.4% |
| Combined housing | 0.82 | 0.96 | 0.99 | 1.10 | 1.45 | 27.9% |

Read alone this looks like confirmation of the brief's hypothesis, and reporting it there
would have been a mistake.

**Result, stage 2, which is the actual finding.** Housing costs are less than proportional
to income, and PAEI correlates negatively with wages, so an income effect alone produces
exactly this gradient. Stratifying by income decile and comparing PAEI quintiles within
each:

| Denominator | Raw q5-q1 gap | Income-standardised gap | Deciles with a positive gap |
|---|---|---|---|
| Household wage income | +12.31 pp | **-9.55 pp** | **0 of 10** |
| Total household income | +8.32 pp | **-5.41 pp** | **0 of 10** |

The gradient does not merely vanish under an income control. It REVERSES, in every income
decile, on both denominators. At a given income level, high-PAEI households carry a LOWER
housing burden than low-PAEI households.

**What this does to the thesis.** The brief's Tier 2 hypothesis, that Physical AI exposure
concentrates in mid-income high debt-to-income households, is refuted. It was already
marked refuted in Phase 1 on weaker evidence and a flawed measure. It is now refuted on the
correct measure with the confound controlled. PROJECT_BRIEF.md Section 3 has been updated
to move it out of "our hypotheses, unverified" into an explicit REFUTED row.

**What it rules out.** Stated precisely, because an earlier version of this entry
overreached. What is ruled out is **concentration of exposure by household DTI**: high-PAEI
households are not more housing-burdened than others at the same income, so there is no
concentration to find at the household level. Also ruled out: the Phase 1 "flatness"
framing, which was an artifact of share-attribution across mixed-occupation households, and
the retired diversification claim (D9 point 3), which depended on flatness.

**What it does NOT rule out, corrected 2026-09-19 (A8).** The aggregate mortgage channel is
NOT ruled out. A shock to the wage bill still flows to mortgage debt service in aggregate
regardless of how it is distributed across households, and the geographic channel (Step 3)
is where that shock concentrates. The buffers question is also open: equal debt service can
hide very unequal default risk if high-PAEI households hold thinner liquid assets, and that
is untested until Step 5.

**What remains unknown.** Everything that matters now sits elsewhere:
- The geographic channel. Default needs an income shock PLUS negative equity, and mortgage
  books are regional. Household-level DTI was the wrong place to look. Step 3.
- Non-housing debt. Unsecured and auto debt and liquid buffers are untested; equal debt
  service can still hide very unequal default risk. Step 5.
- Whether the risk is priced at all. Step 4.

**Honest note on direction.** The reversal is not evidence that high-PAEI households are
safe. A lower housing burden at the same income is consistent with thinner assets, weaker
credit access and more renting, all of which show up in the tenure table below. It relocates
the risk; it does not remove it.

## A7. Tenure composition, which is where the renter result comes from

Percent of households, by PAEI quintile:

| Quintile | Owner with mortgage | Owner outright | Renter |
|---|---|---|---|
| q1 (least exposed) | 54.0 | 17.6 | 27.5 |
| q2 | 50.4 | 19.1 | 29.3 |
| q3 | 48.7 | 18.3 | 31.9 |
| q4 | 42.6 | 19.8 | 36.2 |
| q5 (most exposed) | 32.2 | 21.0 | 45.0 |

Mortgaged homeownership falls from 54.0 to 32.2 percent across the exposure distribution
while renting rises from 27.5 to 45.0 percent. Phase 1 looked only at mortgages and so
looked at the tenure group that high-PAEI households are least likely to be in. This is the
mechanical reason the level result in Phase 1 (A4) put most mortgage service in low-PAEI
quintiles, and it is why renters had to be added before any claim about household exposure
could be made.

For the thesis this is a relocation, not a reprieve: rent is a wage-backed obligation with
a much shorter enforcement lag than a mortgage, and the renter burden in q5 is 34.4 percent
of wage income, the highest cell in the table.

## A8. The 77.7 percent labor-linked receipts figure was overstated

**What was tested.** Phase 1 treated all federal personal current taxes as labor-linked.

**Result.** Splitting by the IRS SOI wage and salary share of AGI (Table 1.4, All Returns:
Sources of Income):

| | USD bn | Share of federal current receipts |
|---|---|---|
| Personal current taxes, labor-linked portion | 1,716.5 | |
| Federal social insurance contributions | 2,074.4 | |
| **Central estimate** | **3,790.9** | **63.4%** |
| Upper bound (Phase 1 figure) | 4,645.8 | 77.7% |

Wage share of AGI: 61.0 percent (2021), 65.7 percent (2022), 66.8 percent (2023). The 2021
dip is the capital gains realisation spike.

**What this does to the thesis.** It weakens the headline number by 14 percentage points
but does not change its direction: roughly two thirds of federal current receipts are still
a claim on the wage bill. Use 63.4 percent as the central figure and 77.7 percent only as
an explicitly labelled upper bound.

**Remaining bias, stated.** The wage share of AGI is not the wage share of TAX. Because the
income tax is progressive and capital income concentrates in top brackets, the true
labor-linked share of liability is plausibly below 63.4 percent. The central figure is
itself still an upper bound, just a tighter one.

## A9. Citation verified: BIS on off-balance-sheet AI financing

The Phase 1 dependent claim (finding A2, decision D4) is confirmed against the source.

- Title: "Financing the AI infrastructure boom: on- and off-balance sheet borrowing"
- Publication: BIS Quarterly Review, March 2026, published 16 March 2026
- URL: https://www.bis.org/publ/qtrpdf/r_qt2603u.htm

Verbatim, on the structure the Leg A measurement problem turns on: "A common structure
involves a dedicated vehicle - often a joint venture or special purpose entity - that
acquires or develops data centre assets... The hyperscaler typically holds a minority
stake, commits to long-term operating leases or capacity offtake agreements." And:
"Economically, this substitutes upfront capex with multi-year operating expenses while
keeping most of the associated debt off the hyperscaler's balance sheet." And: these
arrangements "amount to 'shadow borrowing': obligations that are economically akin to debt
but largely reside outside corporate balance sheets."

Outstanding: the BIS page does not name the feature's authors in the fetched content. Author
names must be taken from the PDF before this enters references.bib. Logged in
lit/unverified.md as a partial verification, not a failure.

## A10. STEP 1 GATE. PAEI is not a cognitive index, but its novel half is unvalidated

**What was tested.** PAEI against Felten, Raj and Seamans AIOE (85.7 percent match) and
Eloundou et al. GPT exposure (100 percent match), unweighted and employment-weighted.

**Result 1, discriminant validity, passes.** PAEI correlates -0.878 with AIOE and -0.758
with Eloundou GPT beta. (Reporting rule, item 9: wherever PAEI's Webb correlation is
quoted it must be given together with the high-P split, +0.708 overall and +0.275 among
high-P occupations. Neither number travels alone.) PAEI is close to the mirror image of cognitive AI exposure, so it
is not a relabelling of an existing index.

**Result 2, which is the finding that matters and weakens the claim.** Decomposed:

| Measure | vs Felten AIOE | vs Eloundou beta |
|---|---|---|
| PAEI (P x S) | -0.878 | -0.758 |
| embodiment P alone | **-0.935** | -0.810 |
| structure S alone | **+0.027** | +0.127 |

P, at r = -0.935 against a published index, is very nearly the negative of cognitive
exposure. "Physical jobs are the ones cognitive AI does not touch" is not new. Almost all
of PAEI's discriminant validity is inherited from the unoriginal half of the index.

S is orthogonal to everything published (r = +0.03 to +0.13). That is where PAEI's novelty
lives, and S currently has NO external validation of any kind.

**What this does to the thesis.** It does not damage the thesis, but it relocates the risk
in the paper's central artifact. The defensible statement is now: PAEI is a known quantity
multiplied by an unvalidated novel quantity. Validating S is the critical path.

**GATE VERDICT: UNRESOLVED, and it cannot be resolved with available data.** The gate is
stated against Webb's robot score, which is the only published index targeting the same
technology. Webb distributes scores only via his own site; michaelwebb.co/data.html and
web.stanford.edu/~mww/ both return 404 as of 2026-09-19. Frey and Osborne probabilities
were not obtainable in a verified machine-readable form, and Rule 1 forbids third-party
reproductions that cannot be checked against the original. Every convergent test in Step 1
is blocked: Webb (unavailable), Acemoglu and Restrepo robot exposure (needs IFR, paid), IFR
density (paid), BLS OES weights (HTTP 403).

Stated in advance so it can be checked later: I expect P to correlate above 0.8 with Webb's
robot score, and PAEI as a whole to correlate lower. If so the verdict is that PAEI at
c = 0 is NOT novel and the novelty rests entirely on PAEI(c), which is what Step 2 builds.

**What remains unknown.** Whether S predicts anything real. Until an external convergent
test exists, S is a theoretically motivated construct with good face validity and no
evidence.

## A11. A near-precedent on the paper's own theoretical hook

Schaal, J. (2025), "A theory-based AI automation exposure index: Applying Moravec's Paradox
to the US labor market", arXiv 2510.13369, 15 October 2025.

Applies Moravec's paradox to O*NET to build an exposure index. Different construction
(19,000 tasks, LLM-scored on performance variance, tacit knowledge, data abundance,
algorithmic gaps) and it produces close to the opposite ranking: management, STEM and
sciences most exposed, maintenance, agriculture and construction least.

It does not preempt PAEI, which targets embodied rather than cognitive automation and is
two-factor and multiplicative. It does mean "we apply Moravec's paradox to occupational
exposure" is no longer an unclaimed framing and must be written as a contrast, not a
discovery. See notes/paei_validation.md Section 5.

## A12. STEP 2. PAEI(c) built. Two design flaws found and fixed before any result was taken

**What was tested.** Whether the scenario-conditional index behaves sensibly across the
capability grid, in both the smooth form P * S^(1-c) and the threshold form.

**Flaw 1, the raw S scale is degenerate under a threshold.** S has sd 0.071 and range 0.29
to 0.70, because it is a difference of two bounded means recentred on 0.5. Thresholding
(1 - S) gives a step function: 0 percent of employment exposed below c = 0.30, 37.6 percent
at c = 0.50, 100 percent by c = 0.70. Everything crosses in a band of width 0.25. That is
the scale, not robotics. Fixed by thresholding on S_rank, the employment-weighted percentile
rank of S. The raw version is retained and plotted so the degeneracy stays visible.

**Flaw 2, the threshold rule needed an embodiment gate.** The rule keys only on structure,
so the first switcher list was led by Lawyers (P = 0.095) and Chief Executives (P = 0.132).
An occupation that needs no body cannot be displaced by a robot at any capability level.
Switchers are now gated at the median P and headline measures are weighted by P.

**A tautology that must never be reported as a result.** Because S_rank is a percentile
rank, the share of employment crossing the threshold equals c by construction (50.7 percent
at c = 0.50). Only the embodiment-weighted quantities are informative.

**Result.** Embodiment-weighted exposure frontier, 375 SOC occupations, 140.2 million
workers, 7,878.2 USD bn covered wage bill:

| c | Embodied work exposed | Wage bill at risk (USD bn) | Mean PAEI_smooth |
|---|---|---|---|
| 0.00 | 0.0% | 0 | 0.17 |
| 0.20 (low) | 19.4% | 320.0 | 0.19 |
| 0.50 (medium) | 47.2% | 889.3 | 0.24 |
| 0.80 (high) | 76.0% | 1,628.9 | 0.30 |
| 1.00 | 100.0% | 2,235.6 | 0.35 |

The ceiling matters: at perfect capability the wage bill at risk is 2,235.6 USD bn, 28.4
percent of the covered wage bill. Exposure is bounded by how much of the wage bill is paid
for physical work, and that bound is well under a third. This is a restraining result and
should be used as one.

**The distinctive content.** 27 embodiment-gated occupations switch between medium and high
capability: 11.6 million workers, 8.3 percent of covered employment, 400.2 USD bn of wage
bill. Recycling and reclamation workers, landscaping and groundskeeping, industrial truck
operators, couriers, vehicle cleaners, correctional officers, roofers, transit bus drivers,
veterinary technologists, structural iron and steel workers, crane operators. Median hourly
wages 12 to 27 USD. These are physical jobs in semi-structured or outdoor settings that
current robotics cannot touch and that no cognitive exposure index flags. That is the
concrete answer to what makes Physical AI different from prior automation.

**Scenario mapping is stipulated, not estimated.** No published robotics benchmark mapping
onto a normalised structure-tolerance scale was located, so c is a modelling assumption.
All results are reported across the full grid so a reader can substitute their own mapping.

**What remains unknown.** Whether S predicts anything real (Step 1, unresolved). PAEI(c)
inherits that gap, with an odd consequence worth stating: at high c the index leans more on
P, which IS externally correlated, so PAEI(c) is better grounded at high c than at low c.
The economic feasibility filter is not built, because no verified all-in hourly robot cost
was located and Rule 2 forbids inventing one.

## A13. PART A. A coverage BUG, not a limitation, was hiding a third of the economy

**What was tested (A1).** Reconciliation of 911 O*NET occupations down to the analysis
frame, and of PUMS wages against NIPA.

**Result: a bug.** The v1 Step 2 build attached PUMS employment by grouping on the
crosswalk's SOC string and merging onto PAEI's detailed SOC. **100 of the 530 Census OCCP
codes carry BROAD SOC codes ending in 0** (53-3030 "Driver/sales workers and truck
drivers", 35-2010 "Cooks") which do not exist in O*NET detailed SOC. Their employment was
silently dropped. The casualties were among the largest and most embodied occupations in
the economy: Heavy and Tractor-Trailer Truck Drivers, Light Truck Drivers, Janitors and
Cleaners, Cooks, Farmworkers.

Fixed by rebuilding on the OCCP spine, the level at which employment is actually observed.
Tagged `PAEI_C_VERSION = v2-occp-spine`.

| | v1 | v2 |
|---|---|---|
| Occupations covered | 375 of 786 (47.7%) | 476 of 512 (93.0%) |
| Employment covered | 140.2m | 183.7m |
| Wage bill covered | 7,878.2 USD bn | 9,870.2 USD bn |
| Wage bill at risk, c = 1 | 2,235.6 USD bn | 2,935.4 USD bn |

**Coverage waterfall.** 530 OCCP codes and 203.7m PUMS employment at the start; 92.25
percent of employment survives the Census crosswalk; the rest is lost to PAEI matching and
the positive-wage restriction. Covered wage bill is 58.95 percent of NIPA wages and
salaries. That gap has two distinct sources which must not be conflated: 3,006 USD bn is
crosswalk and matching loss, 2,481 USD bn is PUMS undercount and top-coding against NIPA.

**Systematic difference test.** For the 411 v1-uncovered PAEI occupations, P and S are
known, so the test is direct. Uncovered occupations had HIGHER embodiment (mean P 0.410 vs
0.368, Cohen's d = -0.223, Welch p = 0.0019). The loss was biased toward exactly the
occupations the paper is about, so v1 understated exposure. Bounding by assigning uncovered
occupations the mean covered employment moves employment-weighted mean P from 0.348 to
0.380. S differed only marginally (Welch p = 0.057, Mann-Whitney p = 0.027).

**Effect on the thesis.** Direction unchanged, magnitude understated in v1. Nothing
previously reported was too strong; it was too weak.

## A14. A2. The frontier curve is an identity and is not a finding

Embodied work exposed reads 21.0, 48.7 and 80.1 percent at c = 0.2, 0.5 and 0.8. That
tracks c almost exactly, and it is an artifact of construction: S_rank is an
employment-weighted percentile rank, so the share of employment crossing the threshold
equals c by definition, and P and S are near-orthogonal (r = -0.06), so P-weighting does not
disturb it.

**The frontier curve must not be presented as a result.** Recorded in
notes/paei_c_method.md beside the employment-share identity. The findings are the ordering
of occupations, the wage gradient along S_rank, and the empirical anchor in A15.

## A15. A3 GATE: S PASSES its first external validation

**What was tested.** Whether observed robot adoption is concentrated where S says it should
be. ACES 2022 robotic equipment capital expenditure by NAICS sector, bridged to occupations
through the PUMS OCCP by INDP employment matrix (86.4 percent of cells, 88.9 percent of
employment, mapped to NAICS).

**Result.** Among high-P occupations (P >= 0.398, n = 238):

| Group | Spearman with S_rank | p |
|---|---|---|
| **High-P occupations (the gate)** | **+0.419** | 1.5e-11 |
| Low-P occupations (context) | +0.184 | 4.3e-03 |
| All occupations | +0.293 | 7.4e-11 |

Robot adoption rises significantly in structure, and **the relationship is more than twice
as strong among occupations that require a body** (+0.419 against +0.184), which is the
pattern the theory predicts and one a spurious correlation would not produce. Sector
intensities are plausible on their face: retail trade 611 USD per worker, manufacturing 394,
wholesale 145, construction 44, transportation and warehousing 22.

**GATE: PASS.** This is the first external evidence of any kind for S, which Step 1 showed
carries all of PAEI's novelty and had none (A10). The novel half of the index is no longer
unvalidated.

> **DOWNGRADED 2026-09-19 by A23. Do not cite this gate as passed.** Controlling for
> manufacturing employment share, the association vanishes on the full sample (+0.293 to
> -0.005) and retains only a weak manufacturing-confined residual among high-P occupations
> (+0.419 to +0.145). The adoption measure has an R-squared of 0.996 on the industry mix, so
> it carries essentially no within-industry information. See A23.

**c_today is NOT cleanly identified, and this is the honest caveat.** The adoption profile
across deficit deciles is not monotone: 81, 100, 12, 36, 47, 27, 68, 29, 25, 21 percent of
peak intensity. Adoption is clearly concentrated at deficit <= 0.2 but recovers at
(0.6, 0.7], most likely a composition artifact of retail and warehouse occupations. Three
estimators disagree:

| Estimator | c_today |
|---|---|
| First decile below 20 percent of peak intensity | 0.20 |
| Deficit at 90 percent of cumulative robot spend | 0.79 |
| Deficit at 95 percent of cumulative robot spend | 0.93 |

Reported range: **c_today is somewhere in 0.2 to 0.4, with low confidence**, on the ground
that concentration at deficit <= 0.2 is the only feature stable across specifications. The
cumulative-spend estimators are much higher because robot spend is diffuse rather than
sharply bounded, which is itself informative: there is no clean capability frontier visible
in the adoption data.

**Limitation, per owner instruction.** Adoption is observed at NAICS sector level while S is
occupational, so the identifying variation is each occupation's industry mix. This is a
convergent test, not a direct one, and occupations concentrated in the same industry receive
similar intensity, which limits power. Commuting-zone replication awaits the Acemoglu and
Restrepo package in data/raw/manual/.

## A16. A5. The word "ceiling" is retired. Exposure is a range, not a number

Recomputing the c = 1 exposure with the embodiment gate at the 25th, 40th, 50th and 60th
percentile of P, with and without P-weighting:

| Quantity at c = 1 | Range across gates |
|---|---|
| Share of embodied work exposed | 52.1 to 90.7 percent |
| Wage bill at risk, P-weighted | 1,221 to 2,439 USD bn |
| Wage bill at risk, unweighted | 2,147 to 6,203 USD bn |

**This retracts the "28.4 percent ceiling" stated in A12.** That figure was a single
gate-and-weighting choice reported as though it were a structural bound. It was too
confident. Exposure at c = 1 is a range conditional on the embodiment gate and the
weighting, and the unweighted range is very wide. All four gates are in
`data/processed/a5_gate_sensitivity.csv`.

## A17. A7. Magnitude against three denominators, without adjectives

Wage bill at risk (ungated, P-weighted frontier):

| c | USD bn | % of household debt service | % of labor-linked federal receipts | % of total wages and salaries |
|---|---|---|---|---|
| 0.0 | 1.6 | 0.06 | 0.04 | 0.01 |
| 0.2 | 417.9 | 15.84 | 11.02 | 3.13 |
| 0.5 | 1,250.2 | 47.38 | 32.98 | 9.35 |
| 0.8 | 2,261.8 | 85.72 | 59.66 | 16.92 |
| 1.0 | 2,935.4 | 111.25 | 77.43 | 21.96 |

Denominators: household debt service 2,638.5 USD bn (TDSP applied to DPI); labor-linked
federal receipts 3,790.9 USD bn (Step 0 SOI-corrected central estimate); total wages and
salaries 13,365.2 USD bn (NIPA WASCUR).

These are ratios of a flow at risk to flows currently serviced by that same wage bill. They
are not loss estimates, not probabilities and not forecasts. The gate sensitivity in A16
applies to every row.

## A18. A6. Most of the wage bill at risk does NOT run through general-purpose robotics

**What was tested.** Three occupation-level flags, added as diagnostics and not as a third
index factor: driving-dominant (exposure runs through autonomous vehicles, a separate
capability pathway on its own regulatory clock), high interpersonal intensity, and legal or
custodial accountability (substitution gated by liability and statute, not capability).
Built from O*NET Work Activities and Work Context descriptors at the employment-weighted
70th percentile, plus SOC major-group membership for legal, protective service and
healthcare practitioner accountability.

Each flag covers roughly 30 percent of employment (driving 30.1, interpersonal 30.1,
accountability 32.4), and they overlap substantially.

**Result. Wage bill at risk, USD bn, P-weighted:**

| c | All | Excl. driving | Excl. interpersonal | Excl. accountability | Excl. all three |
|---|---|---|---|---|---|
| 0.2 | 417.9 | 411.4 (-1.6%) | 293.3 (-29.8%) | 297.7 (-28.8%) | **210.2 (-49.7%)** |
| 0.5 | 1,250.2 | 1,083.6 (-13.3%) | 912.9 (-27.0%) | 885.1 (-29.2%) | **593.3 (-52.5%)** |
| 0.8 | 2,261.8 | 1,557.1 (-31.2%) | 1,605.9 (-29.0%) | 1,366.3 (-39.6%) | **764.4 (-66.2%)** |
| 1.0 | 2,935.4 | 1,715.5 (-41.6%) | 2,076.8 (-29.2%) | 1,554.1 (-47.1%) | **821.3 (-72.0%)** |

**This is the most important qualification in Part A and it must lead the magnitude
discussion.** At high capability, 72 percent of the headline wage bill at risk sits in
occupations flagged as driving-dominant, interpersonally intensive, or accountability-gated.
The residual that is cleanly attributable to general-purpose physical manipulation is
821 USD bn at c = 1, against a headline of 2,935 USD bn.

The driving share rises steeply with c (1.6 percent of the total at c = 0.2 to 41.6 percent
at c = 1.0), which is the expected signature: driving occupations sit at high structure
deficit and only enter the exposed set at high capability. That is precisely why they need
separating. Autonomous vehicles are a distinct technology with a distinct timeline and a
distinct regulatory gate, and folding them into a single robotics capability parameter c
conflates two things that will not arrive together.

**The switcher list barely survives the flags.** Of the 43 embodiment-gated occupations
switching between medium and high capability (21.3 million workers), only **3 occupations
and 1.72 million workers** carry none of the three flags:

| Occupation | P | deficit | Employment |
|---|---|---|---|
| Landscaping and groundskeeping workers | 0.486 | 0.573 | 1,525,107 |
| Drywall and ceiling tile installers | 0.618 | 0.594 | 149,945 |
| Merchandise displayers and window trimmers | 0.570 | 0.639 | 44,982 |

**Effect on the thesis.** It narrows it considerably. The earlier claim that the
medium-to-high capability band is where Physical AI does something prior automation did not
survives only for a small set of occupations once vehicles, interpersonal work and
liability-gated work are separated out. The larger numbers are real but they are not
"robots doing physical work"; they are three different substitution stories with different
clocks.

**What this does NOT say.** It does not say the flagged exposure is fake. Autonomous
vehicles displacing driving is a genuine wage-bill shock and arguably the largest single
one in the table. The point is that it is a different technology from general-purpose
manipulation and must be scenario-ed separately rather than summed into one c.

**Recommendation for the paper.** Report the headline with the flag decomposition attached,
never alone. Consider a separate capability parameter for autonomous driving, which is the
single flag doing the most work at high c.

## A19. A4. The rubric is highly reliable, and it does NOT reproduce S_original

**What was tested.** 200 O*NET Core task statements, stratified across S_rank quintiles with
probability proportional to employment, scored independently by two LLM raters on four
dimensions (environment predictability, object variability, workspace access, need for
improvisation). Raters received only the occupation title and the task text. S, S_rank, P
and PAEI were withheld from the rating file so scores could not anchor on the value under
validation.

**Result 1, reliability: excellent.**

| Dimension | Pearson | ICC(2,1) | Krippendorff alpha | Exact agreement | Within one point |
|---|---|---|---|---|---|
| Predictability | 0.972 | 0.971 | 0.971 | 91.5% | 100% |
| Object variability | 0.890 | 0.880 | 0.879 | 79.0% | 95.0% |
| Workspace access | 0.951 | 0.951 | 0.951 | 88.0% | 100% |
| Improvisation | 0.928 | 0.928 | 0.927 | 81.0% | 100% |
| **S_text scale (mean of four)** | **0.969** | **0.967** | **0.967** | | |

The rubric is reproducible. Two independent raters agree at alpha 0.967 on the composite.

**Result 2, validity: the correlation with S_original is 0.306, below the 0.5 threshold.**

| Comparison | Pearson | Spearman |
|---|---|---|
| S_text (mean of raters) vs S_original | **+0.306** | +0.273 |
| S_text rater 1 vs S_original | +0.321 | +0.295 |
| S_text rater 2 vs S_original | +0.286 | +0.248 |

The critical point: **the raters agree with each other (0.969) far more than either agrees
with S_original (about 0.30).** The gap is therefore not rater noise. It is a genuine
construct difference. A text-based reading of what a task's environment is like and a
descriptor-based aggregate of O*NET Work Context scales are measuring substantially
different things, and both are internally stable.

S_text is also far less compressed than S_original (sd 0.271 against 0.071 in the same
sample), which is a point in its favour on scale grounds and is the defect that forced the
rank transform in Step 2.

**Result 3, arbitration by the A3 adoption test, per the owner's decision rule.**

| Sample | S_original | S_text |
|---|---|---|
| High-P occupations (n = 100) | Spearman +0.181 (p = 0.071) | +0.155 (p = 0.123) |
| All sampled occupations (n = 200) | **+0.187 (p = 0.008)** | +0.011 (p = 0.873) |

On the full 200-occupation sample S_original predicts observed robot adoption and S_text
does not, at all. On the high-P subsample the two are within 0.03 of each other and
**neither is significant at 5 percent**, so the high-P arbitration is inconclusive on its
own terms.

Design caveat, stated because it cuts toward S_original: the sample was stratified on
S_original's rank, which guarantees S_original full spread. That favours S_original, so its
win should be read as the expected direction of a biased test rather than as a clean
victory.

**DECISION (logged as D17): retain S_original. Report S_text as a robustness check.** It is
the incumbent, it is the version validated on the full 476-occupation A3 test, and it is the
only version that predicts adoption in this subsample.

**What this does to the thesis, stated plainly.** It weakens confidence in S as a construct
without changing which version the paper uses. Two defensible, internally reliable
operationalisations of "environmental structure" correlate at only 0.31. That is a
measurement problem the paper must disclose rather than resolve, and it belongs in the
limitations section, not in a footnote.

**Power caveat on A15.** In this 200-occupation subsample S_original's high-P correlation
with adoption is +0.181 and not significant, against +0.419 (p = 1.5e-11) on the full
476-occupation sample. The A3 gate result rests on the full sample; the subsample is
underpowered (n = 100 high-P) and should not be read as contradicting it.

**Not yet done from A4.** The owner's specification called for 50 items flagged for human
review. The merged item-level ratings are in `data/processed/a4/a4_merged_ratings.csv`; the
50 highest-disagreement items should be extracted and sent for owner adjudication before the
index is published.

## A20. STEP 3 GATE (PARTIAL). Geography is built; the holder map is BLOCKED

**Gate question, from MASTER_PROMPT_PHASE2.md: where does Leg W exposure sit (GSEs, large
banks, regional banks, nonbanks)?**

**THE GATE CANNOT BE ANSWERED. HMDA is unreachable from this environment.** Every CFPB and
FFIEC host returns HTTP 403: the data-browser API, the snapshot publication page, and the
public S3 bucket. Browser user-agent and Referer headers do not help, so this is a
network-level block like BLS and openICPSR, not a user-agent policy like SEC's. This blocks
B3(a) holder class, B3(c) lender ranking, the LTV half of B3(d), and all of Step 4.
Resolution requires a manual download into `data/raw/manual/hmda/` (open question Q4).

What follows is the PUMS half of Step 3, which is complete.

### Result 1: national geographic DAR, with replication standard errors (B5)

2,462 PUMAs, ACS PUMS 2023, PAEI_C_VERSION v2-occp-spine. SEs are ACS
successive-difference over 80 replicate weights.

| c | Wage at risk (USD bn) | SE | Share | Mortgage at risk (USD bn) | SE | Share | Rent at risk (USD bn) | Share |
|---|---|---|---|---|---|---|---|---|
| 0.2 | 417.9 | 1.6 | 3.8% | 35.6 | 0.19 | 3.5% | 45.9 | 5.6% |
| 0.3 | 650.3 | 2.0 | 6.0% | 55.7 | 0.23 | 5.5% | 67.2 | 8.2% |
| 0.5 | 1,250.2 | 2.6 | 11.5% | 108.2 | 0.33 | 10.7% | 114.5 | 13.9% |
| 0.8 | 2,261.8 | 3.6 | 20.8% | 195.3 | 0.48 | 19.4% | 183.9 | 22.3% |
| 1.0 | 2,935.4 | 4.4 | 27.0% | 256.5 | 0.59 | 25.5% | 223.6 | 27.1% |

National SEs are tight (relative SE under 0.5 percent). PUMA-level SEs are not: the median
relative SE is 9.6 percent on wage at risk and 14.8 percent on mortgage at risk, so
individual PUMA estimates are noisy and should never be read as point facts.

**Rent at risk exceeds mortgage at risk as a share at every c** (13.9 against 10.7 percent
at c = 0.5). That is consistent with the tenure composition in A7 and it keeps pointing the
same way: the renter channel is where exposure concentrates, and it is the channel the
paper's Leg W framing currently handles least well.

### Result 2, which weakens Phase 2 point 4: exposure RATES are close to uniform in space

Two statistics answer two different questions and they disagree in a way that matters.

**Dollars concentrate.** At c = 0.5 the top decile of counties holds **73.7 percent** of
mortgage debt service at risk. County Gini on levels is 0.81.

**Rates do not.** Across counties with above-median mortgage volume, the at-risk share runs
p10 = 8.8 percent, p50 = 11.1 percent, p90 = 13.8 percent. That is a **p90/p10 ratio of
1.55**. At PUMA level the same ratio is about 1.8.

The top-10 counties by at-risk DOLLARS are Los Angeles, Cook, Maricopa, Orange, San Diego,
King, Harris, Riverside, Santa Clara and Miami-Dade, and their at-risk rates are 10.0 to
11.9 percent, essentially the national average. The top-10 counties by at-risk RATE are
small and mid-sized counties in Indiana, upstate New York, New Mexico, Wisconsin, Kentucky,
Wyoming and Arkansas at 16 to 18 percent, and they carry very few dollars.

**The dollar concentration is a population artifact.** Big metros hold most of the exposure
because they hold most of the mortgages, not because they are more exposed.

**Effect on the thesis.** Phase 2 point 4 held that the mortgage channel runs through
geography rather than household DTI. The geographic channel is real but it is weak in the
dimension that matters for lender selection. A 1.55x spread in exposure rate is not a
regional concentration story; it is close to a uniform rate. The structural conclusion is
the same one the household analysis reached, now on independent evidence: **there is no
low-exposure pocket to rotate into, by occupation or by geography.** Exposure tracks the
wage bill, and the wage bill is everywhere.

This does NOT dispose of the geographic argument. Default requires an income shock plus
negative equity, and the equity half is county-specific and untested here because the FHFA
HPI download failed and HMDA LTV is blocked. A uniform income-shock rate can still produce
very non-uniform defaults once local house prices and leverage are layered on. That is the
double trigger (B3d) and it remains open.

### What remains unknown after Step 3

- The holder map, which is the gate question. Blocked on HMDA.
- Whether GSEs hold most of this, which would make the exposure effectively sovereign and
  would be, as the prompt says, a major finding whichever way it falls.
- The double trigger: no FHFA HPI and no LTV, so no equity overlay.
- Moran's I was NOT computed. It needs area centroids, and rather than approximate them the
  statistic is reported as not computed.
- B4 (how many HMDA years approximate the stock) cannot be assessed without the data.

### Methodological notes

- PUMA to county allocation uses the Census 2020 tract-to-PUMA relationship file with
  **tract COUNT** as the allocation factor. The correct basis is tract population. This is a
  stated approximation and its error is unquantified; diagnostics are in
  `data/processed/dar_geo_allocation_diagnostics.json`.
- c = 0.0 rows are degenerate (near-zero exposure), so concentration statistics at c = 0 are
  meaningless and should be ignored.
- Every output row carries `paei_c_version`, so revising the index does not require
  rewriting Step 3 (B1).

## A21. STEP 1 GATE RESOLVED: PAEI at c = 0 is NOVEL, and my registered prediction was wrong

Webb's occupation-level exposure scores were supplied by the owner
(`exposure_by_occ1990dd_lswt2010.xls`, despite the extension a CSV, 341 occupations, with
`pct_robot`, `pct_software`, `pct_ai` as percentiles under Webb's 2010 labor-supply weights).

**Crosswalk.** Webb occ1990dd to occ2010 (Autor and Dorn `occ2010_occ1990dd.dta`) to 2018
Census occupation code (Census 2010-to-2018 crosswalk) to PUMS OCCP. 86.7 percent of Webb
rows reach occ2010; 381 of 512 OCCP codes end up carrying a Webb score, covering **84.8
percent of employment**.

**GATE VERDICT: PAEI at c = 0 is NOVEL.** The criterion was a correlation of roughly 0.8 or
above with Webb's robot score.

| Our measure | vs Webb ROBOT | vs Webb software | vs Webb AI |
|---|---|---|---|
| **PAEI (P x S)** | **+0.708** | +0.285 | -0.119 |
| embodiment P | +0.740 | +0.286 | -0.119 |
| structure S | -0.054 | +0.048 | +0.023 |

(Spearman; employment-weighted figures are within 0.01 of these throughout.)

**My registered prediction was wrong and I am recording that.** In
notes/paei_validation.md, before the data was available, I predicted P would correlate
above 0.8 with Webb robot and that the gate would therefore likely fail. P came in at
**0.740**, below the threshold, and PAEI at 0.708. The direction of the prediction (P above
PAEI) was right; the level was wrong, and the gate passes where I expected it to fail.

**The pattern across Webb's three indices is the strongest validation evidence the project
has.** PAEI correlates +0.71 with robots, +0.29 with software, and -0.12 with AI. It tracks
the robot index specifically and falls away monotonically as the technology moves from
embodied to cognitive. Combined with the earlier discriminant results (-0.878 against
Felten AIOE, -0.758 against Eloundou GPT beta, A10), PAEI now has convergent validity
against the one published embodied-automation index and discriminant validity against three
cognitive ones.

### The finding that complicates this, and it concerns S again

Two problems, both of which belong in the paper rather than in a footnote.

**First, the 0.708 is carried by the whole-distribution contrast, not by the region of
interest.** Splitting at the median P:

| Subsample | PAEI vs Webb robot | P vs Webb robot | S vs Webb robot |
|---|---|---|---|
| All (n = 381) | +0.708 | +0.740 | -0.054 |
| **High-P (n = 191)** | **+0.275** | +0.479 | -0.027 |
| Low-P (n = 190) | +0.429 | +0.420 | +0.047 |

Among the physically demanding occupations the paper is actually about, PAEI tracks Webb's
robot score only weakly (+0.275). Most of the headline correlation comes from PAEI and Webb
both separating physical from non-physical work across the full distribution, which is not
a demanding test.

**Second, the two external benchmarks disagree about S.**

| Benchmark | What it measures | S among high-P occupations |
|---|---|---|
| ACES 2022 robotic capex (A15) | observed robot spending by industry | **+0.419 (p = 1.5e-11)** |
| Webb robot score | patent-text overlap with task descriptions | **-0.027 (p = 0.72)** |

S predicts where robots are actually bought and does not predict which tasks a robot could
technologically perform.

There is a reading of this that favours S and it is the one the theory predicts: Webb
measures technological potential at the task level and is by construction blind to the
environment a task sits in, while ACES measures realised deployment, which is gated by
exactly the environmental structure S is meant to capture. On that reading the two results
are not in conflict; they are the separation between "a robot could do this task" and "a
robot is being bought to do this job", and S is a deployment-feasibility construct rather
than a technological-potential one. That is precisely the distinction PAEI(c) is built on.

The competing reading, which must be stated alongside it: the ACES result is industry-level
projected onto occupations (A15's stated limitation), so it could be industry composition
rather than environment, while the Webb null is occupation-level and therefore the cleaner
test. On that reading S has one supportive result with a known confound and one clean null.

**I do not think this can be settled with the data in hand.** It should be reported as an
open measurement question, and it raises the value of the commuting-zone replication.

### What this changes

- The novelty claim for PAEI at c = 0 survives, on the test that was set for it.
- The claim should be stated as convergent-but-distinct, roughly 0.7 with the robot index
  and near zero or negative with every cognitive index, and NOT as "uncorrelated with
  existing measures".
- The weak high-P correlation (+0.275) must be reported. It is the honest limit on how much
  the Webb comparison validates the index where the paper uses it.
- S remains the contested component: reliable (A19, alpha 0.967 on an independent rubric
  that does not reproduce it), predictive of observed adoption (A15), and null against
  task-level robot potential (here).

### Note on the Acemoglu and Restrepo material

The owner supplied the published JPE 2020 article, "Robots and Jobs: Evidence from US Labor
Markets" (Daron Acemoglu, MIT; Pascual Restrepo, Boston University; Journal of Political
Economy 128(6), electronically published 22 April 2020). This is now a verified citation and
is the source for the adjusted-penetration-of-robots construction and the commuting-zone
exposure design.

The **replication data set was not supplied**, only the article. The commuting-zone
replication of A3 therefore remains open and still needs the openICPSR package, which
returns 403 from this environment. The article does give the industry-level facts we can
cite directly: automotive employs 38 percent of existing robots, electronics 15 percent,
plastics and chemicals 10 percent, metal products 7 percent; and the headline estimate that
one more robot per thousand workers reduces the aggregate employment-to-population ratio by
about 0.2 percentage points and wages by about 0.42 percent.

# PHASE 2 BLOCK 3

## A22. ITEM 1. Orientation is consistent. A3 is NOT a sign error

Checked against the data rather than the code comments. In `paei_c.csv`, the employment
weighted percentile rank `structure_S_rank` correlates **+1.000** (Spearman) with raw
structure S, and `structure_deficit_rank` correlates **-1.000** with it.

| Where | Column used | Meaning |
|---|---|---|
| (a) Step 2, PAEI(c) | `structure_S_rank` for reporting, `structure_deficit_rank` for the threshold | percentile of STRUCTURE; threshold exposes occupations whose UNSTRUCTUREDNESS percentile is at or below c |
| (b) A3, anchor_c.py | `structure_S_rank` | percentile of STRUCTURE |
| (c) Webb comparison | `structure_S_rank` | percentile of STRUCTURE |

Confirmation from the threshold itself: at c = 0.5 the exposed set has mean raw S of 0.528
against 0.410 for the unexposed set, so the exposed half is the MORE structured half, which
is the intended semantics.

So "adoption rises in S_rank at +0.419" means adoption rises with STRUCTURE. That is the
sign the theory predicts and A3 is not a fail on orientation grounds. The most structured
occupations (postal mail sorters, press machine setters, food batchmakers, machinists) carry
S_rank near 1.0; the least structured (animal control workers, crossing guards, tree
trimmers, power-line installers, EMTs) carry S_rank near 0.

**Item 1 passes. No stop on this ground.** A3 fails for a different reason, below.

## A23. ITEM 2 GATE: S is largely a SECTOR PROXY. A15 is downgraded

**This is the finding that most weakens the thesis in this block and it leads.**

### The structural problem, which is prior to any result

The occupation-level adoption measure is

    robot_exposure(occ) = sum over sectors of share_i(occ) * intensity_i

and `intensity_i` varies only across 2-digit NAICS sectors. It is therefore a deterministic
function of the occupation's industry mix. Regressing it on the full NAICS2 share vector
returns **R-squared = 0.9958**. There is essentially no within-industry variation for S to
explain, so item 2(a) as specified (control for the full two-digit mix) is vacuous by
construction, not by result.

Manufacturing share alone explains **75.0 percent** of the variance in robot_exposure.

### What the feasible tests show

**T1, partial Spearman of S_rank with adoption, controlling for manufacturing share:**

| Sample | Raw | Partial | p |
|---|---|---|---|
| All occupations (n = 476) | +0.293 | **-0.005** | 0.906 |
| High-P occupations (n = 238) | +0.419 | **+0.145** | 0.026 |

On the full sample the association is **entirely** manufacturing share. Among high-P
occupations roughly a third of the raw magnitude survives, at +0.145.

**T3, by dominant sector, high-P only:**

| Subsample | n | Spearman | p |
|---|---|---|---|
| Dominant sector is manufacturing | 49 | **+0.381** | 0.007 |
| Dominant sector is non-manufacturing | 189 | **+0.076** | 0.301 |

The surviving association is confined to manufacturing-dominant occupations and is null
everywhere else, in the much larger subsample.

**T4, both variables demeaned within dominant sector:** +0.203 all, +0.232 high-P, both
p < 0.001. This does not rescue S. The residual variation exists because occupations sharing
a dominant sector still differ in their SECONDARY industry mix, so T4 is measuring
composition too, just at a finer grain.

### Verdict

**Item 2 fails in substance.** S does not demonstrably predict robot adoption independent of
industry composition. What A15 established, restated honestly:

> High-S occupations are concentrated in robot-intensive sectors, above all manufacturing.
> Once manufacturing share is controlled, the association vanishes on the full sample and
> retains only a weak, manufacturing-confined residual among high-P occupations.

**A15's "GATE: PASS, first external evidence for S" is downgraded.** It was not wrong
arithmetically, but it was over-read: I reported a between-sector correlation as evidence
for an occupation-level environmental construct, and I flagged the industry-level limitation
without testing it. This test was available at the time and I should have run it before
calling the gate.

### What this does to the thesis, and the consequence the owner specified

S now has three external results and they do not cohere:

| Test | Result for S |
|---|---|
| Independent LLM rubric, S_text (A19) | reliable (alpha 0.967) but reproduces S at only r = 0.31 |
| ACES observed robot capex (A15, as corrected here) | association is largely sector composition |
| Webb task-level robot potential (A21) | null, -0.03 among high-P |

There is no longer a clean external result supporting S as an occupation-level construct.
Per the owner's instruction: **the pathway decomposition (item 3) becomes the paper's primary
structure and c is demoted to a robustness section.**

### What is NOT overturned

- PAEI at c = 0 still passes the Step 1 gate against Webb (A21, +0.708 overall). That test
  is occupation-level and does not depend on S; it is carried by P.
- The Phase 1 and Step 0 household results, the geographic results, and the A6 pathway
  decomposition are untouched by this. None of them rest on S's external validity.
- The multiplicative form and the Moravec framing remain defensible as theory. What is not
  currently defensible is the claim that S has been validated against observed adoption.

### What would settle it

A measure of robot adoption with genuine within-industry variation across occupations.
The Acemoglu and Restrepo commuting-zone design does not provide this either: their APR is
also industry-level (19 IFR industries) interacted with local employment shares, so their
exposure measure has the same property. Settling this needs either establishment-level or
occupation-level deployment data, which no public US source currently provides.

## A24. ITEM 3. Pathway decomposition, now the primary structure

Pathways are mutually exclusive by priority: driving, then gated, then manipulation. Scope
is occupations at or above the median embodiment P (0.398); below that, exposure runs
through cognitive AI and is out of scope.

**A second flag error found and fixed.** The A6 driving flag was built on the O*NET
descriptor "Operating Vehicles, Mechanized Devices, or Equipment", which captures forklifts,
power tools and construction plant. It therefore flagged electricians, carpenters,
construction labourers, maintenance workers and agricultural workers as driving-exposed.
**113 in-scope occupations would have been wrongly assigned to the driving pathway.**
Driving is now defined by SOC major group 53-3, Motor Vehicle Operators. The descriptor
version is retained in `a6_occupation_flags.csv` as a sensitivity.

| Pathway | Occupations | Employment | Wage bill (USD bn) | Embodiment-weighted (USD bn) | Mortgage at risk (USD bn) | % of national mortgage service | Rent at risk (USD bn) | % of national rent |
|---|---|---|---|---|---|---|---|---|
| Driving | 6 | 6.04m | 226.9 | 126.4 | 9.9 | **0.98%** | 10.7 | **1.30%** |
| Gated | 154 | 44.49m | 1,780.4 | 975.2 | 78.9 | **7.83%** | 76.0 | **9.22%** |
| Manipulation | 78 | 29.47m | 688.5 | 361.8 | 27.6 | **2.74%** | 47.0 | **5.70%** |

The manipulation pathway, which is the one PAEI was built for and the one the paper's
framing is about, carries 2.74 percent of national mortgage debt service and 5.70 percent of
national rent. Driving carries about 1 percent of each. The gated pathway is the largest on
every measure, and it is the pathway where substitution is constrained by liability and
interpersonal content rather than by manipulation capability.

All six driving occupations also carry an accountability or interpersonal flag (passenger
safety), so the priority rule matters for them; the assignment is recorded so it can be
undone.

### Owner-operators carrying equipment debt

PUMS class of worker (COW) does size this group.

| | Employment | Share |
|---|---|---|
| Driving pathway, total | 6,037,238 | |
| of which self-employed (COW 6 or 7) | 953,112 | **15.8%** |
| Truck and driver/sales workers (OCCP 9130), total | 4,666,861 | |
| of which self-employed | 666,070 | **14.3%** |

Self-employed driving wage bill is 20.8 USD bn. These roughly 0.95 million workers, of whom
0.67 million are truck drivers, are the group that carries tractor and trailer finance in
addition to household debt. PUMS cannot see the equipment loan itself, so the debt stock is
not measurable here; what is established is the size of the exposed group.

### The driving clock, from public deployment data

Reported as an observable clock rather than a forecast. These are press and company sources
(Tier D and company IR), not official statistics, and are labelled as such.

- Waymo: about 500,000 paid driverless rides per week as of March 2026, across 14 US cities
  as of 1 September 2026, on a fleet of over 4,000 vehicles; up roughly tenfold from about
  50,000 per week in May 2024.
- Aurora: commercial driverless Class 8 trucking in Texas from April 2025; 10 driverless
  routes across the Sun Belt by February 2026; over 250,000 driverless miles; a validated
  1,000-mile Fort Worth to Phoenix lane; a stated target of more than 200 driverless trucks.
- Kodiak: driverless Class 8 operations in the Permian Basin with Atlas Energy Solutions,
  over 750 hours of commercial driverless operation.

**The calibration this gives is the point, and it cuts against alarm.** Robotaxi deployment
is real and scaling fast, but it bears on taxi drivers and chauffeurs, who are 681,000
workers in PUMS. Driverless trucking bears on 4.67 million truck and driver/sales workers,
and the deployed fleet is in the low hundreds of vehicles. The driving pathway has a
genuinely observable clock, and as of late 2026 that clock reads early.

## A25. ITEM 4 GATE: the registered hypothesis is SUPPORTED

Registered before running: geographic concentration of the at-risk RATE declines as c rises,
because exposure shifts from tradable manufacturing to nontradable local services.

### (a) Concentration of the at-risk rate falls monotonically in c

| c | PUMA Gini (mortgage rate) | PUMA p90/p10 | County Gini | County p90/p10 |
|---|---|---|---|---|
| 0.2 | 0.2199 | 2.75 | 0.1766 | 2.24 |
| 0.3 | 0.1715 | 2.18 | | |
| 0.5 | 0.1228 | 1.76 | | |
| 0.8 | 0.0972 | 1.55 | | |
| 1.0 | **0.0938** | **1.54** | **0.0652** | **1.44** |

Slope of Gini on c is negative in all four series tested (PUMA and county, wage and
mortgage): -0.118, -0.147, -0.093, -0.131. **Hypothesis supported, consistently.**

### (b) The proposed mechanism is confirmed

Tradable share of the embodiment-weighted wage bill at risk:

| c | Tradable % | Nontradable % | Mixed % |
|---|---|---|---|
| 0.05 | **33.5** | 38.8 | 27.7 |
| 0.20 | 20.2 | 49.5 | 30.4 |
| 0.50 | 15.4 | 47.2 | 37.4 |
| 1.00 | **12.9** | 39.7 | 47.5 |

Exposure starts concentrated in tradable manufacturing and shifts out of it as capability
rises, which is exactly the mechanism the hypothesis proposed. (Classification is a coarse
NAICS sector rule, not Mian and Sufi's import/export-per-worker measure; Mian and Sufi
(2014), Econometrica 82(6) is cited as the methodological precedent for the split, not as
the source of this rule.)

### (c) Benchmark against Acemoglu and Restrepo, made comparable

They report their commuting-zone robot exposure spanning about 9 robots per thousand
workers from p1 to p99, roughly a ninefold spread, with an interquartile range of about 1.
Computing the same p1-to-p99 ratio on our at-risk rate:

| c | PUMA mortgage rate p99/p1 | County mortgage rate p99/p1 |
|---|---|---|
| **0.2** | **8.15x** | 4.83x |
| 0.5 | 2.97x | 2.54x |
| 0.8 | 2.36x | 1.83x |
| 1.0 | 2.23x | 1.69x |

**At low capability our measure reproduces their concentration almost exactly** (8.15x at
PUMA level against their roughly 9x), which is a meaningful external check on the geographic
build. It then collapses to about 2x as capability rises.

### What this means, and it is the most useful structural result in the block

The geography of Physical AI exposure is **not** the geography of industrial robots, except
at the very start. At c near 0 the exposure is a rust-belt and manufacturing-corridor
phenomenon with an 8-to-1 spread, which is the world Acemoglu and Restrepo measured. As
capability rises the exposure becomes a local-services phenomenon, spread almost evenly
across the country at roughly 2-to-1.

This has a direct implication for the paper's financial argument. A regionally concentrated
shock is one a diversified national lender can survive and a regional lender cannot. A
near-uniform shock is the opposite: it is survivable by no one through geographic
diversification, but it is also far less likely to produce the localised negative-equity
spirals that turn income shocks into mortgage losses. **The two halves of the double trigger
move in opposite directions as c rises**, and the paper should say so rather than assuming
higher capability is monotonically worse for financial stability.

# PHASE 2 BLOCK 4

## A26. ITEM 0. Package identified. It is NOT Robots and Jobs

`data/raw/manual/114030-V1.zip`, 38 files, contains: `smt88.dta`, `smt93.dta` (Survey of
Manufacturing Technology), `sic5811.dta` and `naics5811.dta` (NBER-CES manufacturing
productivity database), seven `*_table_sic87_codes.dta` files, `FH_offshoring_naics.dta`,
KLEMS multifactor productivity workbooks, `nber-ces-naics-emp.dta`, `hrs.xlsx`, BEA GDP by
industry.

There is **no commuting-zone file, no IFR robot series and no adjusted-penetration-of-robots
variable**. This is the replication package for Acemoglu and Restrepo, "Automation and New
Tasks: How Technology Displaces and Reinstates Labor", Journal of Economic Perspectives
33(2), 2019, as the owner suspected. Confirmed by contents; the package ships no README.

The Robots and Jobs (JPE 2020) package is no longer being pursued. The commuting-zone
replication of A3 is therefore closed unbuilt, which no longer matters because A3 itself is
now closed (A27).

## A27. ITEM 1. THE S QUESTION IS CLOSED. S fails the decisive test

This was the one test with genuine within-manufacturing variation, and S does not pass it.

**Setup.** SMT gives technology use at 4-digit SIC across SIC 34 to 38 (150 industries in
1988, 161 in 1993). Robot use is `ppr` (pick and place robots) plus `otr` (other robots),
measured as employment in establishments using them over total employment. Crosswalk SIC87
to 1997 NAICS (Census concordance) to PUMS INDP. **35 distinct PUMS industries are usable,
above the owner's threshold of about 25, so the test is properly powered and its result
stands.**

Verification note: the SMT's 5-category, 17-technology structure is confirmed against Census
descriptions, and the 17 column stems partition exactly into those categories with the
documented counts. A variable-level dictionary naming each stem was not located, so the
stem-to-technology mapping is inferred from transparent naming plus the exact partition. High
confidence, not documented, recorded as such.

**Result, high-P occupations (n = 146), across 35 detailed manufacturing industries:**

| Measure | Spearman | p | Employment-weighted |
|---|---|---|---|
| Robot use, employment share | **-0.140** | 0.092 | +0.010 |
| Robot use, establishment share | **+0.265** | 0.001 | +0.035 |
| All occupations, employment share | -0.100 | 0.087 | -0.027 |

**The two measures of the same quantity disagree in sign**, and both employment-weighted
versions are null. There is no coherent association. The establishment-share result is
positive and significant and is reported here rather than suppressed, but it cannot carry
the construct on its own when the employment-share version of the identical variable points
the other way and neither survives employment weighting.

**VERDICT: the S question is closed permanently.** S has now been tested four ways:

| Test | Result |
|---|---|
| Independent LLM rubric (A19) | reliable at alpha 0.967, reproduces S at only r = 0.31 |
| ACES capex, 8 sectors (A15, corrected in A23) | association is sector composition |
| Webb task-level robot potential (A21) | null, -0.03 among high-P |
| **SMT, 35 detailed manufacturing industries (here)** | **null, and sign-inconsistent** |

This goes in the limitations section as a stated failure, not as an open question. The
honest sentence for the paper: *we could not validate the environmental-structure component
against any external measure of robot adoption or robot-reachability, and we report the
index's structure factor as theoretically motivated but empirically unsupported.*

What survives: P (embodiment), which carries the Webb correlation and the whole pathway
decomposition. The paper's quantities do not depend on S.

## A28. ITEM 2 GATE. The S-free geography result. Hypothesis SUPPORTED

> **SUPERSEDED IN PART by A40.** The near-uniformity claim in this entry is withdrawn.
> County Gini falls monotonically with group breadth (0.179, 0.156, 0.134, 0.104 from the
> top tenth to the top half of employment), so 0.141 on an above-median definition is a
> fact about the breadth, not about embodied work. Moran's I of 0.44 to 0.54 shows embodied
> exposure is strongly spatially clustered at every breadth. Use the A40 schedule and the
> breadth-matched placebo comparison instead.


The A25 c-path result is superseded. It was partly mechanical: the c-threshold runs on
S_rank, and S largely proxies manufacturing, so a c-path necessarily starts in manufacturing
geography and diffuses out of it. This version uses no S anywhere.

Groups defined externally:

| Group | Occupations | Workers |
|---|---|---|
| Robot-reachable, top decile of Webb pct_robot | 43 | 19.3m |
| Robot-reachable, top quintile | 77 | 24.7m |
| Robot-reachable, top tercile | 129 | 34.6m |
| All embodied work (P at or above median) | 238 | 80.0m |

**Concentration of the mortgage at-risk RATE, county level:**

| Group | National rate | Gini | p90/p10 | **p99/p1** |
|---|---|---|---|---|
| Robot-reachable, top 10% | 4.57% | 0.283 | 3.35 | **11.86** |
| Robot-reachable, top 20% | 5.97% | 0.258 | 3.52 | **8.99** |
| Robot-reachable, top 33% | 8.62% | 0.211 | 2.79 | **6.73** |
| **All embodied work** | **20.68%** | **0.141** | **2.02** | **3.85** |

Acemoglu and Restrepo report their commuting-zone robot exposure spanning roughly ninefold
from p1 to p99. **The top-quintile robot-reachable group comes in at 8.99, essentially their
number.** All embodied work comes in at 3.85, less than half as concentrated.

PUMA level is starker and noisier at the extremes: 81.5 (top decile), 57.5 (top quintile)
against 16.0 for all embodied work.

**Tradable share of the wage bill:**

| Group | Tradable % | Nontradable % |
|---|---|---|
| Robot-reachable, top 20% | 19.6 | 18.7 |
| All embodied work | 14.8 | **40.5** |

**Both halves of the registered hypothesis hold, on an S-free construction.** Currently
robot-reachable work is concentrated in tradable manufacturing geography at almost exactly
the magnitude Acemoglu and Restrepo measured for industrial robots. All embodied work is
near-uniform and heavily nontradable.

**Why this matters more than A25 did.** The claim is no longer about a capability parameter
on a discredited index. It is a statement about two observable groups of occupations, one
defined by an external published measure of robot-reachability and one by embodiment alone:
*the work robots can currently reach sits where industrial robots already sat; the rest of
embodied work does not, and is spread almost evenly across the country.* Physical AI's
financial footprint becomes geographically undiversifiable only to the extent it moves
beyond currently robot-reachable work.

## A29. ITEM 3 and CORRECTION A. The two mortgage figures reconciled, and bounded

**The discrepancy was real and it was mine.** Block 4 reported "all embodied work" at 20.68
percent of national mortgage debt service; the Block 3 pathway table summed to 11.55. Both
were correct arithmetic on different estimands, and neither said which.

    geo_groups.py  weighted by the household's share of wage income in the group.
    build_pathways.py  multiplied that share by embodiment P as well.

The implied ratio is 0.542, which is the mean embodiment P of in-scope occupations. The
entire gap is the embodiment weighting. Reconciled exactly: the pathway CENTRAL figures now
sum to 21.32, identical to the all-embodied CENTRAL figure, so the decomposition is additive.

**Three definitions, now reported as bounds. Percent of national debt service.**

| Group | Mortgage UPPER | **Mortgage CENTRAL** | Mortgage LOWER | Rent UPPER | **Rent CENTRAL** | Rent LOWER |
|---|---|---|---|---|---|---|
| Driving | 3.07 | **1.77** | 0.98 | 3.58 | **2.38** | 1.30 |
| Gated | 24.03 | **14.31** | 7.83 | 24.37 | **17.05** | 9.22 |
| Manipulation | 13.06 | **5.24** | 2.74 | 17.80 | **10.98** | 5.70 |
| **All embodied** | **35.28** | **21.32** | **11.55** | **39.64** | **30.42** | **16.22** |

UPPER counts the full debt service of any household with an exposed earner. CENTRAL weights
by the pathway's share of household wage income. LOWER additionally weights by P.

**The paper's headline definition is CENTRAL.** P is already used to SELECT occupations into
scope, so using it again as a weight applies the same filter twice. The Block 3 pathway
figures were therefore understated, and the Block 4 figure was the right one.

Small residual: Block 4's 20.68 against 21.32 here. Block 4 aggregated through the
PUMA-to-county allocation; this is direct national. The 0.64 point gap is allocation, not
definition.

**Rent exposure exceeds mortgage exposure on every definition**, 30.42 against 21.32 on the
headline. This is now the fourth independent way that result has appeared.

### Household characteristics by pathway

| Group | Households | Share of all HH | Median HH income | Homeownership | Mortgaged | Primary earner in group |
|---|---|---|---|---|---|---|
| Driving | 4.51m | 3.1% | $87,475 | 64.4% | 42.0% | 70.7% |
| Gated | 30.25m | 20.8% | $91,757 | 63.2% | 43.8% | 71.5% |
| Manipulation | 19.29m | 13.3% | $80,327 | 57.0% | 38.2% | **56.4%** |
| All embodied | 47.44m | 32.6% | $84,518 | 61.1% | 41.5% | 75.2% |

Two things matter here. **Roughly a third of all US households (32.6 percent) contain at
least one worker in an embodied occupation.** And the manipulation pathway, the one the
paper's framing is about, is the weakest on every household-balance-sheet measure: lowest
median income, lowest homeownership, lowest mortgaged ownership, and the only pathway where
the exposed worker is usually NOT the primary earner (56.4 percent). Manipulation exposure
sits disproportionately in secondary earners of lower-income renting households, which is
precisely where mortgage credit is not and where consumer credit and rent are.

## A30. ITEM 4 GATE. The concentration hypothesis SURVIVES outside mortgages

Step 0 refuted the concentration hypothesis on mortgages (A6: the gradient reversed in 10 of
10 income deciles). This is the test of whether it survives on non-mortgage credit and
liquid buffers. **It does, on three measures.**

SIPP 2025, December reference month, 13,918 households, 89.7 percent of records with an
occupation matched to the pathway spine.

### Debt to income by type, percent of annual household income

| Group | Credit card | Student | **Vehicle** | Medical | Unsecured total | Non-mortgage total | Mortgage |
|---|---|---|---|---|---|---|---|
| Driving | 4.7 | 6.1 | **11.1** | 1.8 | 14.2 | **25.3** | 52.1 |
| Gated | 3.8 | 7.5 | 6.7 | 1.6 | 14.7 | 21.4 | 59.9 |
| Manipulation | 3.8 | 5.6 | 6.0 | 1.5 | 11.8 | 17.8 | 51.2 |
| All embodied | 3.9 | 7.1 | 7.0 | 1.7 | 14.2 | 21.2 | 58.1 |
| **No embodied worker** | **3.2** | 7.1 | **4.8** | 1.3 | 13.1 | **17.9** | **65.7** |

**Vehicle debt is the standout. The driving pathway carries 11.1 percent vehicle
debt-to-income against 4.8 percent for households with no embodied worker, a ratio of 2.3
to 1.** 44.1 percent of driving households hold vehicle debt against 26.7 percent of
non-embodied households. This is the sharpest concentration result anywhere in the project,
and it sits in exactly the pathway with the fastest observable clock.

Mortgage DTI runs the other way, 58.1 against 65.7. Embodied households are LESS
mortgage-leveraged relative to income, which is now the fifth independent confirmation of
that pattern.

### Liquid buffers and hardship

| Group | Median income | Median liquid assets | Median net worth | **Under 1 month of income in liquid** | Under 1 month of housing | **Unable to pay rent or mortgage** |
|---|---|---|---|---|---|---|
| Driving | $90,615 | $6,448 | $156,552 | 53.7% | 23.3% | **7.4%** |
| Gated | $104,177 | $8,000 | $176,059 | 52.0% | 22.2% | 4.6% |
| Manipulation | $96,634 | $6,100 | $151,529 | **54.2%** | 24.6% | 6.1% |
| All embodied | $96,136 | $6,800 | $164,327 | **53.0%** | 24.0% | 5.4% |
| **No embodied worker** | $72,265 | **$10,500** | **$242,425** | **40.9%** | 25.1% | **4.0%** |

**Households with an embodied worker hold less liquid wealth than households without one,
despite having HIGHER median income** ($6,800 against $10,500 in liquid assets, on
$96,136 against $72,265 of income). 53.0 percent have under one month of income in liquid
assets, against 40.9 percent, a 12 point gap. Median net worth is $164,327 against $242,425.

The hardship indicator moves the same way: 5.4 percent of embodied households report being
unable to pay rent or mortgage, against 4.0 percent, and the driving pathway is highest at
7.4 percent.

### What this does to the thesis

**It relocates the household channel rather than removing it, and this is the first
unambiguously supportive household result in the project.** The exposure is not in mortgage
stocks, where it was looked for and not found. It is in:

1. **Vehicle credit**, concentrated in the driving pathway at more than twice the
   non-embodied rate. Note the compounding: autonomous vehicles displace the income that
   services the vehicle loan.
2. **Thin liquid buffers**, which is what converts an income shock into a default. Equal
   debt service can hide very unequal default risk, and it does: embodied households have
   12 percentage points more of them sitting under one month of buffer.
3. **Existing hardship**, already 35 percent higher before any displacement.

The stock-versus-flow point in the brief sharpens here. These households are not
over-borrowed relative to income; they are under-buffered. That is a different vulnerability
with a different remedy, and it is one that flow-side instruments (income support) address
better than stock-side ones (debt restructuring).

### Limitation that must be fixed before publication

I used the maximum person weight in each household as the household weight. That yields
153.8 million weighted households against roughly 131 million actual US households, so it
overstates. Ratios and weighted shares are largely robust to a proportional inflation, but
household size correlates with both income and pathway membership, so the group comparisons
carry an unquantified bias. The correct weight is the household reference person's. **This
needs a rerun with the proper household weight before any of these figures are published.**
Recorded rather than quietly carried.

## A31. ITEM 4 REBUILT. Two of my three headline claims from A30 do not survive

A30 is superseded in full. None of its numbers should be quoted.

### Fix 1: weights

Census SIPP 2018-redesign guidance, verified against Census documentation: household
estimates use WPFINWGT from the household REFERENCE PERSON record, ERELRPE in (1, 2), at
MONTHCODE 12. A30 used the maximum person weight in the household.

| | Weighted households |
|---|---|
| A30 (max person weight) | 153.8m |
| **A31 (reference person weight)** | **134.98m** |
| Published benchmark | roughly 131 to 132m |

Still about 2 to 3 percent above benchmark, which is within normal SIPP household-estimate
tolerance, and no longer materially wrong.

### Fix 2 and 3: restricted sample, and inference

Restricted sample is households with at least one employed member and a reference person
aged 25 to 64: 6,734 unweighted, 79.8m weighted. Confidence intervals use the SIPP replicate
weights (Fay, rho = 0.5, 240 replicates), matched to 100 percent of households.

Cell counts, restricted: driving 289, gated 1,924, manipulation 1,151, all embodied 3,012,
no embodied worker 3,722. **No pathway cell is thin at the household level.** The one thin
cell is in the driving split, below.

### The results, with unadjusted 95 percent CIs and regression adjustment

Gaps against households with no embodied worker. Adjustment controls reference-person age,
household size, number of earners, region and household income.

| Measure | All-embodied gap [95% CI] | Adjusted coef (t) | Verdict |
|---|---|---|---|
| **Liquid buffer under 1 month of income** | **+12.47 pp [9.51, 15.43]** | **+9.22 pp (t = 2.64)** | **SURVIVES** |
| Vehicle debt to income | +2.49 [1.74, 3.24] | +2.84 (t = 0.85) | **fails adjustment** |
| Credit card debt to income | +0.87 [0.34, 1.40] | not run | small, positive |
| Medical debt to income | +1.01 [0.41, 1.61] | not run | small, positive |
| Unsecured debt to income | +0.66 [-1.54, 2.85] | -0.27 (t = -0.30) | **NULL both ways** |
| Mortgage debt to income | **-13.29 [-19.75, -6.83]** | -1.90 (t = -0.99) | less leveraged |
| **All debt to income** | **-25.29 [-41.18, -9.39]** | not run | **much less leveraged** |

### What this overturns from A30

**1. The vehicle-debt claim was wrong as stated.** A30 led with vehicle debt as a general
embodied-household finding. Adjusted, it is entirely a DRIVING phenomenon:

| Pathway | Adjusted vehicle DTI coef | t |
|---|---|---|
| Driving | **+13.39** | **3.50** |
| Gated | -4.76 | -1.54 |
| Manipulation | **-5.89** | **-1.98** |
| All embodied | +2.84 | 0.85 |

Manipulation households carry LESS vehicle debt than comparable non-embodied households, at
the edge of significance. The raw all-embodied gap was composition: income, household size
and earner count. **The driving result stands and is strong; the generalisation to embodied
work does not.**

**2. The unsecured-credit claim is null.** A30 framed unsecured and vehicle credit together.
Unsecured debt to income is null unadjusted (+0.66, CI spans zero) and null adjusted
(-0.27). There is no unsecured-credit concentration in embodied households.

**3. Embodied households are substantially LESS indebted overall**, by 25.3 points of annual
income [CI -41.2, -9.4], and less mortgaged by 13.3 points. This was visible in A30 on
mortgages only; it is much broader than that.

### What survives, and it is the claim that matters

**"Under-buffered, not over-borrowed" passes the test as the owner specified it.** The
buffer gap survives adjustment (+9.22 pp, t = 2.64) and the leverage gap does not reverse:
it runs strongly in the direction the claim requires. Embodied households hold less debt of
almost every kind relative to income and less of every asset, and 55.3 percent of them sit
under one month of income in liquid assets against 42.8 percent.

By pathway, the adjusted buffer gap is significant for **manipulation (+8.20, t = 2.62)** and
for all embodied work (+9.22, t = 2.64), and NOT individually significant for driving
(+6.67, t = 1.66) or gated (+4.41, t = 1.35). The buffer claim is established for embodied
work as a whole and for manipulation specifically.

### The wealth gap is broad, not just liquid

Restricted-sample medians, embodied against no-embodied-worker households:

| | Embodied | No embodied worker | Ratio |
|---|---|---|---|
| Liquid (bank) | $6,153 | $13,918 | 0.44 |
| **Retirement accounts** | **$7,152** | **$43,473** | **0.16** |
| Home value | $125,000 | $230,000 | 0.54 |
| All assets | $249,558 | $438,779 | 0.57 |
| Net worth | $138,924 | $256,484 | 0.54 |

The retirement gap (6 to 1) is far larger than the liquid gap (2.3 to 1). Framing this as a
liquidity problem understates it: these households are behind on every asset class, most
severely on the one that cannot be drawn on in a shock.

### Fix 4: full disclosure, including the wrong-signed results

Every debt measure available, restricted sample, debt to annual household income, percent.

| Measure | Embodied | No embodied | Direction |
|---|---|---|---|
| Credit card | 3.84 | 2.97 | embodied higher |
| Medical | 1.80 | 0.79 | embodied higher |
| Vehicle | 7.30 | 4.81 | embodied higher (fails adjustment) |
| Other | 1.35 | 1.28 | flat |
| Unsecured total | 14.60 | 13.95 | null |
| **Student** | **7.64** | **8.91** | **embodied LOWER** |
| **Mortgage** | **61.98** | **75.28** | **embodied LOWER** |
| **Other real estate** | **3.34** | **5.22** | **embodied LOWER** |
| **Rental property** | **5.06** | **8.59** | **embodied LOWER** |
| **Business** | **6.54** | **16.27** | **embodied LOWER** |
| **Secured total** | **84.22** | **110.17** | **embodied LOWER** |
| **All debt** | **98.82** | **124.11** | **embodied LOWER** |

Seven of twelve debt measures run against the concentration hypothesis. Three support it and
two are flat. This is the complete set, not a selection.

### Fix 5: driving pathway, employee against self-employed and gig

| | n | Vehicle DTI | Percent holding | Business debt DTI | Buffer under 1 month | Median income |
|---|---|---|---|---|---|---|
| Driving, employee | 225 | 10.67 | 42.1 | 0.66 | 59.5% | $89,826 |
| **Driving, self-employed or gig** | **64** | **14.94** | 37.9 | **9.28** | 48.4% | $81,605 |

**The self-employed cell is thin (n = 64) and its figures are not quotable.** Pooling SIPP
panels is required and is the stated next step for this split.

What the direction suggests, at thin-cell confidence: self-employed drivers carry more
vehicle debt and fourteen times the business debt, consistent with the financed vehicle
being the income-producing asset. They also appear BETTER buffered (48.4 against 59.5
percent under one month), which cuts against the simple story.

**What SIPP cannot say:** it does not identify whether a financed vehicle is used for
business. Vehicle debt and business debt are separate items with no link between them, so
the truck that is both the collateral and the income source cannot be identified directly in
these data. That requires the equipment-finance sources in item 7.

## A32. ITEM 6 GATE. The fiscal channel is the largest, and the tax code makes it nearly unfixable

### What weakens the thesis first

**1. My bottom-up labour tax rate disagrees with the published one.** Building the effective
labour tax rate from NIPA and SOI gives 30.1 to 31.8 percent of the wage bill. Acemoglu,
Manera and Restrepo report 25.5 percent. Both are in the outputs. They are different
concepts (theirs incorporates the employer side and a marginal rather than average
formulation) but I cannot fully reconcile them, and I use the LOWER published figure
throughout, which makes every result below conservative.

**2. The outlay side is scenario, not measurement.** The Acemoglu and Restrepo table A17
magnitudes could not be obtained: the journal supplement returns HTTP 403. Only the
qualitative finding is verified from the main text, that exposure raises take-up of Social
Security retirement, disability and other transfers. The outlay range is therefore built
from published programme parameters and is labelled scenario throughout. It should not be
quoted as an estimate of what actually happens.

**3. The displacement fractions are stipulated.** 10, 25 and 50 percent over 10 and 20 years
are scenario inputs, not forecasts.

**4. tau_k = 10 percent is the economy-wide effective rate on net capital income.** Applying
it to the marginal surplus generated by automation is an approximation, and if automation
surplus is taxed differently the condition below changes.

### (d) The result that matters: the fiscal tau*s condition

Displacing dW of wage bill removes tau_l x dW of labour tax and adds g x dW of outlays. The
automation generates additional taxable surplus s x dW, taxed at tau_k. The government is
fiscally whole if and only if

    **tau_k * s  >=  tau_l + g**, that is **s >= (tau_l + g) / tau_k**

where s is additional taxable surplus per dollar of displaced wage bill and g is added
outlays per dollar of displaced wage bill.

| Added outlays g | s required, capital at 10% | s required, equipment and software at 5% |
|---|---|---|
| 0 (no outlay response) | **2.55** | **5.10** |
| 0.10 | 3.55 | 7.10 |
| 0.25 | 5.05 | 10.10 |

**Even with no outlay response at all, automation must generate 2.55 dollars of additional
taxable surplus per dollar of displaced wages just to keep the government whole.** If the
surplus accrues to equipment and software, taxed at about 5 percent since the 2017 reform,
the requirement is 5.10. With a plausible outlay response it is 5 to 10.

This reframes the brief's threshold substantially. The brief's condition was tau*s >= 1 for
full income replacement, which is demanding. **The fiscal condition is roughly two and a
half to ten times more demanding, and the reason is the tax code, not the technology.**
Labour is taxed at 25.5 percent and the capital that replaces it at 10 percent, or 5 percent
for equipment and software. The wedge means that even output-neutral automation, which by
construction destroys no value, mechanically destroys public revenue.

This is the fiscal version of the hedge failure: there is no adoption speed at which the
public budget is indifferent, because the indifference point requires a surplus multiple
that automation is very unlikely to deliver.

### (a) Revenue at stake, 25 percent displacement of each pathway

Effective rates, share of the wage bill: federal income tax on wages 12.85 percent
(SOI-corrected), federal payroll 15.52 percent, state and local income tax 1.73 to 3.46
percent. Total 30.1 to 31.8 percent bottom-up, against AMR's 25.5 percent.

| Pathway | Displaced wage bill | Gross labour tax | Net wedge at 10% | Payroll at stake | % of OASDI payroll income | % of federal receipts |
|---|---|---|---|---|---|---|
| Driving | $56.7bn | $17.1 to 18.1bn | $8.8bn | $8.8bn | 0.67% | 0.30% |
| Gated | $445.1bn | $134.0 to 141.7bn | $69.0bn | $69.1bn | **5.22%** | 2.37% |
| Manipulation | $172.1bn | $51.8 to 54.8bn | $26.7bn | $26.7bn | 2.02% | 0.92% |
| **All three** | **$674.0bn** | **$203 to 215bn** | **$104.5bn** | **$104.6bn** | **7.91%** | **3.59%** |

The payroll earmarking point is the sharpest. **At 25 percent displacement of embodied work,
payroll tax at stake is 7.9 percent of OASDI payroll income.** Payroll taxes are 91.3 percent
of OASDI trust fund income, and the combined funds already ran a 160.2 billion dollar deficit
in 2025. This is not a general-revenue problem that can be absorbed; it lands on two
earmarked funds that are already in deficit.

Consumption second round, labelled rough: assuming a marginal propensity to consume of 0.8
and an effective state and local sales tax on consumption of 4 to 6 percent, a further
$21.6 to $32.4bn at 25 percent displacement.

### (b) and (c) Outlays and the net position, SCENARIO

Outlay assumptions per displaced worker-year, high case: unemployment insurance at 50
percent replacement for 26 weeks, SNAP for 1.5 persons at $2,255 each, Medicaid at $9,255
per enrollee, and SSDI at 10 percent take-up of $18,960. Low case is zero throughout.

| Pathway | Displaced workers | Outlays (high) | Net fiscal position | Per displaced worker |
|---|---|---|---|---|
| Driving | 1.51m | $36.1bn | $54.2bn | $35,890 |
| Gated | 11.12m | $272.9bn | $414.6bn | $37,278 |
| Manipulation | 7.37m | $150.1bn | $204.9bn | $27,812 |
| **Total** | **20.0m** | **$459.1bn** | **$673.7bn** | |

### The comparison that settles the paper's centre of gravity

At 25 percent displacement, the manipulation pathway puts roughly **$205bn a year** of net
fiscal position at stake. The same pathway accounts for 5.24 percent of national mortgage
debt service, which on a base near $1,000bn is roughly **$52bn a year**.

**The fiscal channel is about four times the size of the direct mortgage channel for the
same pathway, and it is larger still for gated work.** Combined with A31 (embodied households
are less indebted on most measures, and the vehicle-debt concentration is driving-specific),
the evidence now points the paper's centre of gravity at the public budget rather than at
household credit.


## A33. P1 REPAIRED. My framing was wrong, the IMF got there first on the mechanism, and the net-position figure was an artifact

### Four things that weaken what I reported last session

**1. "s must exceed 2.55" was wrong as framed.** Under output neutrality s = 1 - c_r/w, so
s <= 1 by construction. A requirement of s >= 2.55 is not a demanding threshold, it is an
unattainable one. The correct statement is the opposite in character: **output-neutral
automation is never fiscally neutral, for any adoption speed.** There is no break-even s.
The only question is how large the loss is.

**2. The mechanism is already in the literature.** IMF Staff Discussion Note SDN/2024/002,
"Broadening the Gains from Generative AI", states that labour substitution can reduce
revenue if capital income is taxed less than labour income, and that developing economies
specialising in labour-intensive sectors are particularly at risk of losing tax revenue.
That is P1's mechanism and P1's emerging-market corollary, stated qualitatively, in a 2024
IMF publication. The novelty claim must be narrowed accordingly (Section 8 below).

**3. The 674 billion dollar net fiscal position was an artifact and I am withdrawing it.**
It equalled the displaced wage bill to within 0.3 billion. That is a coincidence, not an
identity: the employment-weighted mix happened to put outlays at about 0.62 to 0.87 of mean
wage and tax at about 0.32, summing to roughly 1.0. More importantly, **the scenario outlays
(459bn) were 2.1 times the measured revenue loss (215bn)**, so the headline figure was
dominated by the one component that is assumption rather than measurement. The revenue side
is now led on its own; the outlay side is reported separately and always labelled scenario.

**4. rho is not sourced.** The BLS Displaced Worker Survey reemployment rate was not
obtained. rho is a stipulated scenario parameter throughout. omega IS sourced (Jacobson,
LaLonde and Sullivan 1993).

### (1) P1 restated, in scale-free per-dollar form

Displace one dollar of wage bill. The public loss is

    **L(s) = tau_l + g - tau_k * s**,   with   **s = 1 - c_r/w <= 1**

so L is bounded below by tau_l + g - tau_k and above by tau_l + g. Fiscal neutrality
requires additional taxable OUTPUT y beyond the substitution, of

    **y >= (tau_l + g)/tau_k - s**,  and at best (s = 1)  **y >= (tau_l + g - tau_k)/tau_k**

| tau_l source | g | Loss at s to 0 | Loss at s = 1 | Neutral? | Extra taxable output required at s = 1 |
|---|---|---|---|---|---|
| AMR 0.255 | 0 | 0.255 | **0.155** | No | 1.55 |
| AMR 0.255 | 0.10 | 0.355 | 0.255 | No | 2.55 |
| AMR 0.255 | 0.25 | 0.505 | 0.405 | No | 4.05 |
| Bottom-up 0.301 | 0 | 0.301 | 0.201 | No | 2.01 |
| Bottom-up 0.318 | 0 | 0.318 | **0.218** | No | 2.18 |
| Bottom-up 0.318 | 0.25 | 0.568 | 0.468 | No | 4.68 |

**No parameterisation is fiscally neutral.** The headline per-dollar number is a loss of
**15.5 to 21.8 cents per dollar of displaced wages with no outlay response**, rising to 25.5
to 56.8 cents with outlays.

### (3) On the two rate sets

AMR's 25.5 percent is an effective marginal rate on labour built from statutory rates,
payroll taxes and employer-side treatment inside their user-cost framework. The bottom-up
30.1 to 31.8 percent is an average rate: actual federal income tax on wages (SOI-corrected),
plus actual federal social insurance contributions, plus state and local income tax, each
divided by the NIPA wage bill. Marginal and average rates differ, and the two are built for
different purposes. Every magnitude is reported at both. The word "conservative" is removed:
using the lower figure is a choice that narrows the estimate, not one that makes it safe.

### (2) The general condition with retained tax streams

    **tau_k*s + tau_l*rho*omega + tau_r*(1-m)*(1-s)  >=  tau_l + g*(1-rho)**

rho reemployment share, omega wage ratio on reemployment (0.75 central, 0.65 to 0.82 range,
from Jacobson, LaLonde and Sullivan 1993, AER 83(4), 685-709: long-term losses average about
25 percent for high-tenure displaced workers), m imported share of robot capital, tau_r the
rate on robot-producer income.

**Closed-economy corollary (m = 0, tau_r = tau_k).** The s terms cancel, because a dollar
spent on robot cost and a dollar of surplus are both taxed at tau_k. The condition reduces to

    tau_k + tau_l*rho*omega >= tau_l + g*(1-rho)

which does not contain s at all. **Adoption speed is irrelevant in a closed economy with
uniform capital taxation; only the tax wedge and the reemployment margin matter.**

Break-even reemployment share, omega = 0.75:

| tau_l | g = 0 | g = 0.10 | g = 0.25 |
|---|---|---|---|
| AMR 0.255 | **0.810** | 0.876 | 0.918 |
| Bottom-up 0.301 | 0.890 | 0.924 | 0.948 |
| Bottom-up 0.318 | 0.914 | 0.939 | 0.958 |

**Between 81 and 96 percent of displaced workers must be reemployed, at 75 percent of their
prior wage, for the public budget to break even.** This is the single most policy-relevant
number the project has produced, and it is scale-free.

**Imported-robot corollary (m = 1): the emerging-market case.** The robot cost leaves the
country untaxed and only the surplus is domestically taxable. At AMR rates, g = 0:

| rho | s = 0.05 | s = 0.50 | s = 1.00 |
|---|---|---|---|
| 0.0 | **-0.250** | -0.205 | -0.155 |
| 0.5 | -0.154 | -0.109 | -0.059 |
| 0.7 | -0.116 | -0.071 | -0.021 |
| 0.9 | -0.078 | -0.033 | **+0.017** |

With no reemployment and near the adoption margin, **essentially the entire labour tax is
lost with no offsetting domestic base**. Only at 90 percent reemployment AND costless robots
does the position turn positive. This is the brief's India contrast case, and it is the
sharpest form of the result.

### (4) Payroll, split by trust fund

Effective payroll rate on the wage bill: 15.52 percent. Statutory split OASDI 12.4 and HI
2.9 of 15.3, so 81.0 percent OASDI and 19.0 percent HI.

Denominators: OASDI payroll income 1,323.2bn (91.3 percent of 1,449.3bn combined OASDI
income, 2025 Trustees Report); HI payroll income about 406.9bn (payroll was 88 percent of
Part A revenue of 462.4bn, 2024). The combined OASDI funds ran a 160.2bn deficit in 2025.

### (6) Like-for-like channel comparison, 25 percent displacement

Fiscal loss uses the per-dollar form above (low = AMR with g = 0 at s = 1; high = bottom-up
0.318 with g = 0.10 near the adoption margin). Expected credit loss = balance at risk x
displaced share x default probability among displaced households x loss given default.
Default bracket 5 to 20 percent (anchored on measured aggregate mortgage delinquency of 1.86
percent now against an 11.48 percent peak in 2010, FRED DRSFRMACBS). LGD brackets: mortgage
10 to 25 percent, consumer 20 to 40 percent, indicative industry ranges and NOT authoritative.

| Pathway | Displaced wage bill | Fiscal loss | Expected credit loss | Fiscal / credit |
|---|---|---|---|---|
| Driving | $56.7bn | $8.8 to 23.7bn | $0.5 to 4.9bn | **1.8x to 44x** |
| Gated | $445.1bn | $69.0 to 186.1bn | $4.3 to 39.7bn | **1.7x to 43x** |
| Manipulation | $172.1bn | $26.7 to 72.0bn | $1.6 to 14.5bn | **1.8x to 45x** |

**The fiscal channel exceeds the household credit channel at every corner of both brackets.**
Even comparing the lowest fiscal estimate with the highest credit estimate, fiscal is 1.7 to
1.8 times larger. At the other corner it is more than forty times larger. This is the
like-for-like comparison the correction asked for and it is robust to the bracket choices.

### (8) Targeted literature check, and the narrow novelty claim

| Work | Verified citation | What it shows | States a fiscal-neutrality condition for automation? |
|---|---|---|---|
| Acemoglu, Manera and Restrepo | Brookings Papers 2020(1), 231-300 | Effective tax rates: labour 25.5%, capital 10%, equipment and software about 5% post-2017; the US code favours automation; optimal taxation counterfactuals | **No.** Supplies P1's parameters; does not state the condition |
| Guerreiro, Rebelo and Teles | Review of Economic Studies 89(1), Jan 2022, 279-311 (NBER WP 23806) | Optimal to tax robots while current routine workers are in the labour force; zero once they retire | **No.** Optimal-tax and inequality object |
| Costinot and Werning | NBER WP 25103, 2018 | Sufficient-statistic approach to optimal technology regulation | **No** |
| Thuemmel | CESifo working paper, 2018 | Optimal taxation of robots | **No** |
| Korinek and Lockwood | "Public Finance in the Age of AI: A Primer", Nov 2025, prepared for Brookings CRM | TAI erodes the two main tax bases, labour income and human consumption; optimal taxation across transition stages | **No** condition of P1's form found. Adjacent object: optimal policy, not an accounting neutrality condition. No treatment of imported capital or reemployment in P1's form |
| IMF | Staff Discussion Note SDN/2024/002, "Broadening the Gains from Generative AI" | **Labour substitution can reduce revenue if capital income is taxed less than labour income; developing economies specialising in labour-intensive sectors are particularly at risk** | **Qualitatively yes.** This is P1's mechanism and P1's emerging-market corollary, stated without a formal condition |

**Novelty claim for P1, stated as narrowly as the evidence requires:**

> The mechanism is not new: the IMF (2024) states that labour substitution erodes revenue
> when capital is taxed more lightly than labour, and flags labour-intensive developing
> economies as most exposed. We have not identified a source that writes this as a
> closed-form accounting condition per dollar of displaced wages including the retained tax
> streams (reemployment at rate rho and wage ratio omega, and robot-cost income with
> imported share m), that states the feasibility result that output neutrality makes fiscal
> neutrality unattainable whenever tau_k < tau_l + g so that no break-even adoption speed
> exists, or that reduces the closed-economy case to a single calibrated break-even
> reemployment share.

That is the whole of the claim. It is a formalisation and calibration claim, not a discovery
claim, and the paper must not present it as more.

## A34. P1r FIXES. The break-even reemployment bar was overstated; the channel ratio was understated

### Fix 4a: the robot sector pays wages, and I had ignored that

The break-even reemployment share is rho* = (1 - tau_k/tau_l) / omega.

| tau_l | omega | tau_k = 0.05 | tau_k = 0.10 | tau_k = 0.21 |
|---|---|---|---|---|
| AMR 0.255 | 0.75 | **1.072 INFEASIBLE** | 0.810 | 0.235 |
| AMR 0.255 | 0.82 | 0.980 | 0.741 | 0.215 |
| Bottom-up 0.301 | 0.75 | **1.112 INFEASIBLE** | 0.890 | 0.403 |
| Bottom-up 0.301 | 0.82 | **1.017 INFEASIBLE** | 0.814 | 0.369 |
| Bottom-up 0.318 | 0.75 | **1.124 INFEASIBLE** | 0.914 | 0.453 |
| Bottom-up 0.318 | 0.82 | **1.028 INFEASIBLE** | 0.836 | 0.414 |

**5 of 18 cells are infeasible**, all at the equipment and software rate of 5 percent: they
require reemploying more than 100 percent of displaced workers, which cannot happen. At the
statutory upper case of 21 percent the bar falls to 0.215 to 0.453.

**But the grid above omits something that materially softens the result.** Robot production
and integration is itself labour-intensive, and those wages are taxed at tau_l, not tau_k.
Using the NBER-CES labour share of value added for machinery manufacturing, NAICS 333,
computed from `naics5811.dta` in the Acemoglu and Restrepo package: **0.337**, 2005 onward.

Re-deriving with a share ls of robot-sector income taxed at tau_l:

| tau_l | omega | tau_k = 0.05 | tau_k = 0.10 | tau_k = 0.21 |
|---|---|---|---|---|
| AMR 0.255 | 0.75 | 0.711 | **0.537** | 0.156 |
| AMR 0.255 | 0.82 | 0.650 | 0.492 | 0.143 |
| Bottom-up 0.318 | 0.75 | 0.745 | 0.606 | 0.300 |
| Bottom-up 0.318 | 0.82 | 0.682 | 0.554 | 0.275 |

**Every cell is now feasible, and the central case falls from 0.810 to 0.537.** About a
third of what is spent on robots is wages, taxed at the labour rate, which recovers roughly
a third of the wedge. My previous "81 to 96 percent of displaced workers must be
reemployed" was overstated by ignoring this. **The corrected central range is roughly 50 to
75 percent**, which is demanding but within the range of observed reemployment outcomes.

Two caveats now stated with the grid: (i) this is partial equilibrium, with no
productivity-driven labour demand elsewhere in the economy, which if present lowers rho*
further; (ii) the labour share used is for machinery manufacturing and integrators may be
more labour-intensive still, which would lower rho* again.

### Fix 3: wording corrected

The closed-economy corollary says the loss per displaced dollar is **independent of the
robot cost ratio s** under uniform capital taxation. It says nothing about adoption speed.
I wrote "adoption speed is irrelevant" last session. That was wrong and is corrected in
findings and in framework/propositions.md.

### Fix 1: default probability conditional on job loss

Replaced the population delinquency bracket with conditional estimates from Gerardi,
Herkenhoff, Ohanian and Willen, "Can't Pay or Won't Pay? Unemployment, Negative Equity, and
Strategic Default", Review of Financial Studies 31(3), 2018, 1098-1131 (NBER WP 21630),
PSID-based, verified from the working paper PDF:

- **"the most risky subsample, 'can't pay' households with high LTV ratios have a default
  rate approaching 20 percent"** -> upper bound 0.20, conditional on inability to pay AND
  high LTV
- "the effect of involuntary job loss on the default probability is equivalent to a 37
  percentage point drop in equity"
- a 30-fold difference in default rates across their groups

Lower bound of 0.05, for job loss WITHOUT negative equity, is an interpolation and NOT a
GHOW estimate. Labelled as such.

Honest note: the numeric bracket [0.05, 0.20] is almost the same as the population-based
bracket I used before. What changed is that it is now correctly grounded in a
conditional-on-job-loss estimate rather than in an aggregate delinquency series that
answers a different question.

**Auto and rent: no verified conditional-on-job-loss source was obtained.** Those channels
use the same bracket by assumption and are flagged. This is a gap.

### Fix 2: common time basis, and the ratio is larger than I said

The two channels are different objects and the previous comparison hid it. **Fiscal loss is
a recurring annual flow; credit loss is a one-time stock loss on each displaced cohort.**
Both are now computed as present values at a 3 percent discount rate over the scenario
horizon, with displacement ramping linearly.

25 percent displacement, 10-year horizon, present values in USD bn:

| Pathway | Fiscal PV | Credit PV | Ratio |
|---|---|---|---|
| Driving | 39.4 to 106.3 | 0.5 to 4.2 | 9.4x to 232x |
| Gated | 309.4 to 834.2 | 3.7 to 33.9 | 9.1x to 225x |
| Manipulation | 119.6 to 322.6 | 1.4 to 12.4 | 9.7x to 238x |

Across all displacement, horizon, default and LGD cases: **9.13x to 431.6x**.

"Exceeds at every corner" was withdrawn pending this and is now **restored and strengthened**,
with the reason made explicit: the fiscal channel recurs every year while the credit loss
is incurred once per displaced cohort. Over a decade that asymmetry dominates the parameter
uncertainty.

**The caveat that cuts the other way, and it is important.** The fiscal figures use
L = tau_l - tau_k with rho = 0, that is NO reemployment. Fix 4 shows reemployment is the
dominant margin: at rho = 0.537 the closed-economy fiscal loss goes to zero entirely. **The
9x to 432x range is therefore an upper bound conditional on no reemployment, and the honest
statement is that the fiscal channel dominates the credit channel IF displaced workers are
not reabsorbed.** The credit channel does not have a comparable offset. Both facts belong in
the paper.

### Fix 5: rho remains stipulated

BLS returns HTTP 403 to this environment on every endpoint tried (`disp.nr0.htm`,
`disp.pdf`, `disp.t01.htm`). **Owner action:** download the BLS Displaced Workers Summary
news release, series "Worker Displacement" (biennial, from the CPS Displaced Worker
Supplement), Table 1, "Displaced workers by selected characteristics and employment status",
which gives the share of displaced workers reemployed at the survey date. Drop it in
`data/raw/manual/`. Until then rho is labelled stipulated everywhere it appears.

## A35. PART 2 GATE. The result the pre-registration named as most damaging has occurred

**Registered in `notes/prereg_cognitive_contrast.md` before running, with the interpretation
of each outcome fixed in advance. The pre-registration stated: "If the fiscal wedge is also
larger for cognitive work, the fiscal channel is also predominantly a cognitive-AI channel,
which weakens the framing further. This is the single most damaging possible result for the
current paper and will be reported first if it occurs."**

**It occurred.** It is reported first.

All cognitive claims below carry the binding caveat from D22: Felten AIOE and Eloundou
measure TASK OVERLAP, not displacement and not timing.

### H4 CONFIRMED. The labour tax wedge is larger for cognitively exposed work

P1r repeated by exposure type, with the federal income component scaled by the group's wage
ratio to the economy-wide mean and payroll capped:

| Exposure type | Mean wage | tau_l | Loss per displaced dollar at s = 1 | rho* (with robot-sector labour share) |
|---|---|---|---|---|
| Cognitive, AIOE top quintile | $93,668 | **0.331** | **0.231** | 0.617 |
| Cognitive, GPT top quintile | $63,988 | 0.299 | 0.199 | 0.588 |
| **Embodied, top quintile** | $36,387 | **0.237** | **0.137** | 0.511 |

**The fiscal loss per dollar of displaced wages is 1.7 times larger for cognitively exposed
work than for embodied work** (0.231 against 0.137). Labour taxation is progressive, so
displacing a high-wage worker removes more tax per dollar than displacing a low-wage one.

The fiscal channel, which A32 and A33 established as the dominant channel overall, is
therefore **not primarily a Physical AI channel**. Per dollar displaced it is larger for
cognitive exposure. This is the clearest evidence yet for the scope change in D22.

One qualification that runs the other way and must travel with this: the embodied
top-quintile group has a LARGER wage bill base (36.9m workers) than the AIOE top quintile
(24.3m workers), though a smaller total wage bill ($1,343.9bn against $2,279.1bn). Per
dollar the cognitive wedge is larger; in aggregate the cognitive wage bill at stake is also
larger. Both point the same way.

### H1 PARTIALLY CONFIRMED. Mortgage debt concentrates in cognitive households; total debt does not

Restricted sample, n = 6,734, same weights and adjustment set as A31.

| Group | n | Median income | Mortgage DTI | All-debt DTI | Unsecured DTI | Vehicle DTI |
|---|---|---|---|---|---|---|
| Cognitive AIOE top 20% | 1,261 | $159,154 | 70.48 | 111.39 | 12.28 | 4.60 |
| Cognitive GPT top 20% | 1,421 | $146,519 | 70.32 | 102.09 | 11.94 | 5.00 |
| Embodied top 20% | 1,595 | $97,521 | **53.82** | 88.96 | 12.27 | **7.87** |
| No top-quintile exposure | 3,179 | $88,425 | 74.28 | 129.99 | 17.00 | 5.94 |

Adjusted, against households with no top-quintile exposure:

| Outcome | Cognitive AIOE | Cognitive GPT | Embodied |
|---|---|---|---|
| Mortgage DTI | **+1.92 (t = 2.19)** | +1.07 (t = 1.29) | **-1.90 (t = -2.27)** |
| All-debt DTI | +12.09 (t = 0.46) | +6.20 (t = 0.25) | -15.28 (t = -0.61) |
| Unsecured DTI | +0.07 (t = 0.18) | +0.16 (t = 0.40) | -0.13 (t = -0.33) |

Mortgage DTI: **confirmed** for AIOE, significant and opposite in sign to embodied.
Total debt and unsecured debt: **null for every group**. H1 is confirmed on mortgages only.

### H2 CONFIRMED, and it is the sharpest result in the comparison

| Group | Under 1 month liquid | Median liquid | Median net worth |
|---|---|---|---|
| Cognitive AIOE top 20% | **38.41%** | $21,363 | $382,249 |
| Cognitive GPT top 20% | 42.01% | $18,175 | $325,864 |
| **Embodied top 20%** | **56.12%** | **$6,000** | **$128,292** |
| No top-quintile exposure | 49.89% | $7,500 | $148,437 |

Adjusted buffer coefficients: cognitive AIOE **-0.0889 (t = -5.56)**, cognitive GPT -0.0380
(t = -2.51), embodied **+0.1025 (t = +6.76)**.

**Cognitively exposed households hold 3.6 times the liquid assets and 3.0 times the net
worth of embodied households, and the buffer gap survives adjustment with the largest
t-statistics in the project.** The two exposure types are mirror images on the balance
sheet.

### Shares of the restricted-sample totals (partial item 3; PUMS version still to run)

| Group | Mortgage balance | Consumer balance | Rent or mortgage payment |
|---|---|---|---|
| Cognitive AIOE top 20% | **27.43%** | 23.19% | 19.86% |
| Cognitive GPT top 20% | 28.22% | 23.98% | 21.86% |
| Embodied top 20% | **14.48%** | 19.12% | 19.74% |

**Top-quintile cognitively exposed households hold roughly twice the mortgage balance share
of top-quintile embodied households** (27 to 28 percent against 14.5 percent).

> **SUPERSEDED 2026-09-19 by A36.** On raw NATIONAL dollar shares, which are now the
> headline rule, neither exposure type over-holds mortgage debt relative to its wage bill:
> cognitive leans 0.92, embodied 0.91. The absolute gap is a wage-level difference, not a
> concentration difference. The claim below that "the mortgage channel is a
> cognitive-exposure channel" is WITHDRAWN. What survives is the rent contrast: embodied
> leans 1.09 against cognitive 0.54. On consumer
credit the gap is much smaller (23 to 24 against 19), and on housing payments the two are
essentially equal (about 20 to 22 against 19.7).

So the mortgage channel is a cognitive-exposure channel; the rent channel is shared.
(**Both halves of that sentence are superseded by A36.** Mortgage leans are equal across
exposure types on raw shares; rent is NOT shared, it leans embodied by a factor of two.)

### What this does to the thesis

The household-credit leg of the two-sided bet is **predominantly a cognitive-AI exposure**,
and the fiscal channel is **larger per displaced dollar for cognitive work too**. On the two
channels the project has measured most carefully, Physical AI is the smaller half.

What survives as specifically Physical AI:
- the vulnerability asymmetry: embodied households are under-buffered (56.1 percent under
  one month against 38.4) and asset-poor, so the same displacement causes more distress per
  worker even though it threatens less debt;
- the vehicle-debt concentration in the driving pathway (A31, adjusted +13.39, t = 3.50);
- the geography result, that robot-reachable work is concentrated at Acemoglu and Restrepo
  magnitudes while embodied work overall is near-uniform (A28). **Whether this is a contrast
  or a shared feature is exactly H3, which is registered and NOT YET RUN.**

### Full disclosure

Every measure in the levels table and every adjusted coefficient is in
`data/processed/cognitive_contrast_levels.csv` and `cognitive_contrast_adjusted.csv`,
including the nulls (all-debt, unsecured) and the wrong-signed level results (cognitive
households have LOWER mortgage and total DTI than the no-exposure base in raw levels, and
only exceed it after adjustment). No selection.

## A36. HEADLINE RULE APPLIED. "Mortgage debt leans cognitive" does not survive raw dollar shares

> **SUPERSEDED by A38.** The four-way split here puts working households and households
> with no employed member into one "neither" residual. Separated, working middle-exposure
> households lean 0.93 on mortgage like every other working class, and the 1.09 reported
> here is the non-working tail alone, which leans 1.61 on mortgage and 2.47 on rent. The
> surviving rent contrast also changes character: embodied rent lean is 0.99, exactly
> proportional, so the finding is that cognitive leans AWAY from rent, not that embodied
> leans into it. The two-to-one ratio is AIOE-specific; on Eloundou GPT it is 1.55.


The headline rule (raw dollar shares lead every stability claim) was applied and it
immediately overturned the A35 wording. **A35's "the mortgage channel is a cognitive-exposure
channel" is withdrawn.**

All cognitive figures below: AIOE and Eloundou measure TASK OVERLAP, not displacement and
not timing, and top-quintile occupations include likely-augmented work. Both definitions
reported side by side.

### Raw national dollar shares, four mutually exclusive groups, summing to 100

**Felten AIOE definition:**

| Class | Households | Wage bill | Mortgage service | Rent | Mortgage lean | Rent lean |
|---|---|---|---|---|---|---|
| Cognitive only | 13.08% | 26.91% | 24.69% | 14.43% | **0.92** | **0.54** |
| Embodied only | 18.80% | 19.54% | 17.78% | 21.39% | **0.91** | **1.09** |
| Both exposed | 2.09% | 3.93% | 3.50% | 1.77% | 0.89 | 0.45 |
| Neither | 66.03% | 49.62% | 54.03% | 62.41% | **1.09** | **1.26** |

**Eloundou GPT definition:**

| Class | Households | Wage bill | Mortgage service | Rent | Mortgage lean | Rent lean |
|---|---|---|---|---|---|---|
| Cognitive only | 14.38% | 23.66% | 22.18% | 17.02% | 0.94 | 0.72 |
| Embodied only | 17.82% | 18.61% | 17.01% | 20.33% | 0.91 | 1.09 |
| Both exposed | 3.07% | 4.85% | 4.28% | 2.83% | 0.88 | 0.58 |
| Neither | 64.73% | 52.88% | 56.54% | 59.82% | 1.07 | 1.13 |

"Lean" is the group's share of the debt divided by its share of the wage bill. 1.0 is
proportional.

### What this overturns

**Neither exposure type over-holds mortgage debt relative to its wage bill.** Cognitive-only
leans 0.92, embodied-only 0.91. They are indistinguishable, and both are slightly UNDER
proportional. The over-holder is the unexposed majority at 1.09.

Cognitive households hold a larger absolute share of mortgage service (24.7 against 17.8
percent) **because they earn more** (26.9 against 19.5 percent of the wage bill), not
because they carry more mortgage per dollar earned. A35 read the absolute gap as a
concentration result. It is a wage-level result.

The A35 adjusted coefficients (cognitive AIOE +1.92, t = 2.19; embodied -1.90, t = -2.27)
are not wrong, but they answer a different question: whether exposure predicts mortgage
holding for otherwise-similar households. They are now labelled secondary throughout.

### What survives, and it is a genuine exposure-type contrast

**Rent leans embodied and leans away from cognitive, by a factor of two.** Embodied-only
households hold 21.4 percent of national rent on 19.5 percent of the wage bill, a lean of
1.09. Cognitive-only households hold 14.4 percent of rent on 26.9 percent of wages, a lean
of 0.54. The same pattern holds on the Eloundou definition (1.09 against 0.72).

**The rent channel is the one channel where the two exposure types differ in kind rather
than in level.** It is also the channel with the shortest enforcement lag.

The overlap is small: only 2.1 to 3.1 percent of households contain both a top-quintile
cognitive and a top-quintile embodied worker.

## A37. H3 GATE. Half refuted, half confirmed more strongly than registered

> **SUPERSEDED IN PART by A40.** The concentration ordering reported here holds at PUMA
> level only. At county and metro level it REVERSES and cognitive exposure is the more
> concentrated on the Gini at every breadth but the broadest. The conclusion that embodied
> exposure is "the more concentrated of the two, hence the more diversifiable" is withdrawn.
> The Theil decomposition gives the replacement: embodied exposure is concentrated WITHIN
> metros, cognitive BETWEEN them, and embodied is the more unequal in total at every breadth.
> The opposite-signs correlation result in this entry is unaffected and stands.


Registered prediction 1: cognitive exposure is MORE geographically concentrated than
embodied. Registered prediction 2: cognitive correlates with local house prices, embodied
does not.

### Prediction 1: REFUTED at fine geography

At-risk rate (group wage bill over local wage bill), top-quintile groups:

| Level | Group | National rate | Gini | p90/p10 | p99/p1 |
|---|---|---|---|---|---|
| PUMA | Cognitive AIOE | 20.9% | 0.217 | 2.75 | 6.17 |
| PUMA | Cognitive GPT | 16.6% | 0.176 | 2.21 | 4.46 |
| PUMA | **Embodied** | 12.3% | **0.285** | **4.80** | **19.41** |
| PUMA | **Robot-reachable** | 10.1% | **0.293** | **4.83** | **20.07** |
| PUMA | *Placebo, random 20%* | 19.9% | *0.095* | *1.53* | *2.30* |
| county | Cognitive AIOE | 20.9% | 0.176 | 2.28 | 4.51 |
| county | Embodied | 12.3% | 0.156 | 2.12 | 5.65 |
| county | Robot-reachable | 10.1% | 0.172 | 2.37 | 6.03 |
| county | *Placebo* | 19.9% | *0.090* | *1.49* | *2.31* |

**Embodied and robot-reachable exposure are MORE geographically concentrated than cognitive
exposure at PUMA level, by a factor of three on p99/p1** (19.4 and 20.1 against 6.2). At
county level the three are close and cognitive is marginally highest on Gini. Prediction 1
is refuted where geography is fine enough to matter.

**Density control passes.** The placebo group, occupations drawn at random to match 20
percent of employment, has a Gini of 0.090 to 0.095 and p99/p1 of 2.3. Every real group is
well above it, so the concentration is not sampling noise. And because the statistic is a
RATE, area size is already normalised out; the Gini of wage LEVELS (0.231 PUMA, 0.812
county) is reported only as the density benchmark it is. **Embodied near-uniformity is NOT
just density.**

### Reconciliation with A28, which I must flag

A28 reported embodied work as near-uniform (county Gini 0.141, p99/p1 3.85) against
robot-reachable at 0.258 and 8.99. Here top-quintile embodied comes in at 0.156 and 5.65,
close to robot-reachable. **The difference is the group definition, not the data.** A28 used
above-median P (80m workers); this uses top-quintile P (37m workers). Narrower groups are
more concentrated. Both are correct for their definition, and the paper must state which it
means. The "embodied work is near-uniform" claim holds for BROAD embodied work and NOT for
the top quintile.

### Prediction 2: CONFIRMED, and more strongly than registered

Spearman correlation of the local at-risk rate with local median home value and local mean
wage:

| Group | Home value (PUMA) | Mean wage (PUMA) | Home value (county) | Mean wage (county) |
|---|---|---|---|---|
| Cognitive AIOE | **+0.520** | **+0.767** | +0.530 | +0.543 |
| Cognitive GPT | +0.485 | +0.574 | +0.442 | +0.375 |
| **Embodied** | **-0.597** | **-0.810** | -0.581 | -0.575 |
| **Robot-reachable** | **-0.600** | **-0.827** | -0.620 | -0.607 |
| *Placebo* | *+0.164* | *+0.218* | *+0.185* | *+0.150* |

The registered prediction was that cognitive correlates and embodied does not. **The
correlations have OPPOSITE SIGNS.** Cognitive exposure sits in high-home-value, high-wage
areas; embodied exposure sits in low-home-value, low-wage areas, at -0.81 against mean wage
at PUMA level. The two exposure types are not merely differently concentrated, they are
geographically opposed.

### What this does to the comparative thesis

It damages the draft version. **"Physical AI adds the undiversifiable geography" is wrong as
stated**: at top-quintile definition embodied exposure is the MORE concentrated of the two,
hence the more diversifiable. The defensible geographic claim is narrower and different in
character:

> The two exposure types sit in opposite places. Cognitive exposure is where home values and
> wages are high; embodied exposure is where they are low. A lender or a region is exposed
> to one or the other, rarely both, and the overlap is only 2 to 3 percent of households.

That is a better finding than the one registered, but it is not the one the comparative
thesis was built on, and the thesis draft must be rewritten around it rather than around
undiversifiability.

**Not yet done from this session:** item 4, the runway calculation. Moran's I still not
computed; centroids not obtained.

## A38. ITEM 1. The five-way table. "Neither" was hiding the largest over-holder in the economy

> **SUPERSEDED IN FULL by A47.** Four separate errors: vacant housing units counted as
> households, a wider "employed" test than the engine uses, leans built from two weight
> systems (household weight on the numerator, person weight on the denominator), and a
> working core defined by the reference person's age. Corrected, non-working households
> hold 16.0 percent of mortgage service and 27.3 percent of rent on 6.30 percent of wages,
> leans 2.53 and 4.32, and are 34.2 percent of households rather than 44.3. The embodied
> rent lean is 0.93, not 0.99, so the "exactly proportional" reading below is withdrawn.
> The 2:1 rent RATIO survives at 1.98 on AIOE and 1.50 on GPT. No number in this entry
> should be quoted.


A36 split households four ways and put two thirds of them in a residual called "neither",
which leaned 1.09 on mortgage and 1.26 on rent. That residual mixed two completely different
things: working households whose occupations are not top-quintile exposed, and households
with no employed member at all. Separating them changes the reading.

Restriction: "working core" means at least one employed member and a reference person aged
25 to 64. Source ACS PUMS 2023, `src/shares_and_proportionality.py`, output
`data/processed/shares_fiveway.csv`.

All cognitive figures below: AIOE and Eloundou measure TASK OVERLAP, not displacement and
not timing, and top-quintile occupations include likely-augmented work.

**Felten AIOE definition. Raw dollar shares, five mutually exclusive classes summing to 100.**

| Class | Households | Wage bill | Mortgage service | Rent | Mortgage lean | Rent lean |
|---|---|---|---|---|---|---|
| Cognitive only | 10.21% | 24.15% | 21.66% | 11.95% | 0.90 | **0.49** |
| Embodied only | 14.19% | 16.93% | 15.15% | 16.81% | 0.90 | **0.99** |
| Both exposed | 1.79% | 3.56% | 3.16% | 1.53% | 0.89 | 0.43 |
| Middle exposure, working | 29.50% | 43.17% | 40.33% | 39.62% | 0.93 | 0.92 |
| **Non working** | **44.31%** | **12.20%** | **19.69%** | **30.09%** | **1.61** | **2.47** |

**Eloundou GPT definition** differs only on the cognitive side: cognitive-only rent lean
0.64 rather than 0.49, embodied-only 0.99 as above. The non-working row is identical by
construction.

### Finding 1, which is new and which the paper has to deal with

**Households with no employed member hold 19.7 percent of national mortgage service and
30.1 percent of national rent on 12.2 percent of the wage bill.** They are 44.3 percent of
all households. Their leans, 1.61 and 2.47, are far larger than any contrast between the two
exposure types.

This is a direct qualification of the project's founding framing. Leg W was defined as
credit underwritten against human labour income. Close to a fifth of mortgage obligations
and close to a third of rent obligations are serviced out of transfers, pensions and
drawdown of savings, not out of wages at all. Those obligations are insulated from AI
displacement in the first round, and the paper cannot treat the household debt stock as if
it were uniformly wage-backed. The correct denominator for any displacement pass-through is
the wage-backed portion, not the total.

It also means A36's "the over-holder is the unexposed majority at 1.09" was reading an
average of two opposite groups. Working households with middle exposure lean 0.93 on
mortgage, in line with every other working class. The 1.09 was the non-working tail.

### Finding 2, which WEAKENS the surviving A36 contrast in character though not in ratio

A36's surviving claim was "rent leans embodied and leans away from cognitive, by a factor of
two." Under the working-core restriction the ratio survives almost exactly, 0.99 against
0.49 on AIOE, essentially the same 2.0 as the unrestricted 1.09 against 0.54. **But its
character changes.** Embodied rent lean falls from 1.09 to 0.99, which is proportional to
three digits. Embodied households do not over-hold rent. They hold rent exactly in
proportion to their wages, and cognitive households hold half as much.

So the defensible sentence is **"cognitive exposure leans away from rent"**, not "embodied
exposure leans into rent". That is a weaker and less interesting claim, because a group
holding its proportional share is the null, and the deviation is now located entirely in the
cognitive group. The stated mechanism has to be about why high-earning cognitively exposed
households are disproportionately owners rather than renters, which is a tenure-composition
story of the kind A7 already documented, not a new exposure finding.

**On the GPT definition the contrast is weaker still**, 0.99 against 0.64, a ratio of 1.55
rather than 2.0. The two-to-one figure is definition-specific and must not be quoted without
the alternative beside it.

### Finding 3: mortgage leans are now uniform across all four working classes

0.90, 0.90, 0.89, 0.93. There is no mortgage contrast between exposure types of any kind.
A36's withdrawal of "the mortgage channel is cognitive" is confirmed on the cleaner sample,
and the positive result is the uniformity itself, which is the next entry.

## A39. ITEM 2 GATE. The proportionality result is REAL IN AGGREGATE AND FALSE AT HOUSEHOLD LEVEL. The k rule is an aggregation artifact

> **The central finding STANDS and one inference drawn from it is WITHDRAWN, see A42.**
> Household-level proportionality does fail, and the k rule is an aggregation artifact.
> But the speculation below that low-wage-first displacement would cause share attribution
> to UNDERSTATE the damage by a large multiple is wrong in direction. Share attribution
> OVERSTATES, by about five times at DSTI 50, and overstates MOST under low-wage-first
> incidence. The magnitude concern was justified: incidence moves the dollar figure by up
> to three times. The ACS against SIPP gap logged as open at the end of this entry is
> resolved in A44: it was a service against balance comparison, and SIPP is too imprecise
> to settle it either way.


This is the most damaging result of the session and it leads the report.

### The claim, stated precisely for the first time

The project has found the same thing six times. Stated as the paper would state it:

> A group's share of national mortgage debt service is close to its share of the national
> wage bill, at every level of AI exposure, embodied or cognitive. Therefore a lender cannot
> reduce displacement exposure by changing the occupational mix of its mortgage book.

### The six places it has been found

| # | Finding | Sample and measure | Result |
|---|---|---|---|
| 1 | **A4 and A5** | ACS, PAEI quintiles, service over wage income | Concentration ratio 0.93 to 1.08 across quintiles; service-to-income 7.7 to 9.0 percent. The origin of the claim |
| 2 | **A6** | ACS, housing cost gradient stratified within income decile | Raw gradient 0.87 to 1.44 was an income effect; within decile it is flat. Strong concentration refuted, proportionality is what remains |
| 3 | **A29** | ACS, three embodied definitions as bounds | Pathway central figures sum to 21.32 percent of service against an all-embodied 21.32, decomposition additive and tracking the wage share |
| 4 | **A31** | SIPP 2025, reference-person weights, balances | Two of A30's three claims fail; the surviving pattern is proportionality outside the driving pathway |
| 5 | **A36** | ACS, four-way raw dollar shares | Cognitive-only lean 0.92, embodied-only 0.91, indistinguishable and both slightly under proportional |
| 6 | **A38** | ACS, five-way, working core only | Four working classes lean 0.90, 0.90, 0.89, 0.93. The tightest version yet |

Six independent cuts, two source datasets, two exposure constructs. In aggregate the result
is as solid as anything in the project.

### The test, and it fails

`src/shares_and_proportionality.py`, ACS PUMS 2023, working core, households with positive
wage income and positive obligation. k is defined as debt service per dollar of annual wage
income, estimated through the origin, then re-estimated inside each wage decile.

| Definition | Type | Outcome | n | k | k decile min | k decile max | decile CV | OLS intercept as share of mean y |
|---|---|---|---|---|---|---|---|---|
| AIOE | Cognitive | Mortgage | 101,963 | 0.1271 | 0.0716 | 0.4242 | 0.542 | **0.639** |
| AIOE | Cognitive | Rent | 33,297 | 0.2030 | 0.1141 | 0.7780 | 0.618 | **0.670** |
| AIOE | Embodied | Mortgage | 100,584 | 0.1523 | 0.0898 | 0.6163 | 0.675 | **0.741** |
| AIOE | Embodied | Rent | 55,494 | 0.2549 | 0.1301 | 1.3070 | 0.807 | **0.823** |
| GPT | Cognitive | Mortgage | 105,437 | 0.1376 | 0.0829 | 0.4642 | 0.554 | **0.639** |
| GPT | Cognitive | Rent | 43,506 | 0.2194 | 0.1214 | 0.8987 | 0.666 | **0.684** |

**k varies six to seven fold across wage deciles** and the coefficient of variation is 0.54
to 0.81. The lowest wage decile carries roughly six times as much mortgage service per
dollar of wages as the highest. And **the OLS intercept absorbs 64 to 82 percent of mean
obligation**, which is the same statement in a different form: the relationship is close to
a constant plus a small slope, not a ray through the origin.

### What this does to the thesis

**The proportionality result is an aggregation property of group shares, not a behavioural
relationship between household wages and household debt.** The group shares line up because
the groups have similar wage distributions, not because each household borrows in proportion
to what it earns.

The consequence is specific and it invalidates a step the project has been taking silently
throughout. Every "debt at risk" figure in this repository is computed by attributing a
group's debt share in proportion to its wage share, and that attribution is only valid for a
displaced population whose wage distribution matches the group average. **It does not hold
for any realistic displacement scenario**, because displacement is not drawn uniformly from
within an exposure group, and because the concavity runs the wrong way: low-wage households
inside an exposed group carry several times more obligation per wage dollar than high-wage
ones. If displacement hits the lower part of an exposed group first, proportional
attribution understates the debt at risk, possibly by a large multiple.

The rule `mortgage_service_at_risk = k x displaced_wage_bill` therefore cannot be stated with
a single k. It needs either a wage-decile-specific k, which the deciles above supply, or an
explicit assumption that displacement is wage-neutral within the group, stated as an
assumption and not buried.

**This is not a small caveat and I am not going to file it as one.** It should become a
labelled section of the paper, because the same error is available to anyone who repeats the
group-share method, and because the concave k schedule is itself a result: household
obligations are far less wage-elastic than the aggregate shares suggest.

### Vehicle debt: proportionality fails in the predicted direction, and it is the one place embodied genuinely over-holds

`src/vehicle_proportionality.py`, SIPP 2025, reference-person weights, working core, 6,734
households, 79.81m weighted. Leans are against the household EARNINGS share.

**NON-COMPARABILITY, stated up front:** SIPP carries debt BALANCES, ACS carries monthly
SERVICE. Levels of k are not comparable between this table and the one above. Leans and
decile stability are.

| Group | Earnings share | Vehicle share | **Vehicle lean** | Mortgage share | Mortgage lean | Unsecured lean |
|---|---|---|---|---|---|---|
| Cognitive AIOE | 27.85% | 21.96% | **0.79** | 27.43% | 0.99 | 0.85 |
| Cognitive GPT | 28.84% | 24.58% | **0.85** | 28.22% | 0.98 | 0.82 |
| **Embodied** | 18.81% | 25.95% | **1.38** | 14.48% | 0.77 | 0.87 |

**Vehicle debt is the only obligation class in the entire project where embodied exposure
over-holds.** Lean 1.38 against 0.79 and 0.85, a contrast of roughly 1.7 times, and the
embodied figure is the only lean above 1.0 on any working class in any table. This is
consistent with A31, which located vehicle debt in the driving pathway, and it is a real
exposure-type contrast rather than a wage-level artifact, because it is measured against the
earnings share.

It is also small in stakes. Vehicle balances are 0.11 to 0.19 dollars per dollar of annual
earnings against 1.08 to 1.20 for mortgage, so the channel where the exposure contrast is
sharpest is roughly a sixth the size of the channel where there is no contrast at all.

**The household-level non-proportionality replicates in SIPP**, on a different measure, a
different survey and a different denominator:

| Group | Outcome | n | k | decile min | decile max | max/min | CV | intercept share |
|---|---|---|---|---|---|---|---|---|
| Cognitive AIOE | Vehicle | 498 | 0.114 | 0.041 | 0.396 | 9.63 | 0.529 | 0.880 |
| Cognitive AIOE | Mortgage | 781 | 1.079 | 0.433 | 4.069 | 9.41 | 0.564 | 0.783 |
| Cognitive GPT | Vehicle | 545 | 0.130 | 0.048 | 0.449 | 9.40 | 0.569 | 0.873 |
| Cognitive GPT | Mortgage | 788 | 1.203 | 0.754 | 3.152 | 4.18 | 0.400 | 0.651 |
| Embodied | Vehicle | 593 | 0.190 | 0.084 | 0.793 | 9.42 | 0.675 | 0.886 |
| Embodied | Mortgage | 665 | 1.181 | 0.658 | 3.214 | 4.89 | 0.467 | 0.722 |
| Embodied | Unsecured | 985 | 0.194 | 0.096 | 1.084 | 11.34 | 0.872 | 0.800 |

Four to eleven fold variation in k across earnings deciles, CV 0.40 to 0.87, intercept 65 to
89 percent of mean balance. **The failure is not an ACS artifact.** It is the shape of the
household balance sheet.

### One discrepancy I am flagging rather than resolving

SIPP puts the embodied mortgage lean at 0.77 against cognitive 0.98, a visible gap. ACS puts
both at 0.90. The two differ in measure (balance against service), denominator (earnings
against wage bill) and sample size (665 against 100,584). The ACS figure is the headline
under the raw-dollar-share rule because it is the larger sample on the stability-relevant
measure, but the SIPP gap is not explained and should not be presented as agreement. Logged
as open.

## A40. ITEM 3 GATE. The concentration ordering is an artifact of SCALE, and near-uniformity is an artifact of BREADTH. A28 and A37 both need restating

> **EXTENDED by A46.** The Theil decomposition here pooled all non-metro counties into one
> pseudo-group; A46 repairs it with state non-metro remainders (973 groups) and the
> percentages move by under 1.5 points, so nothing below is materially distorted. A46 adds
> the ABSOLUTE decomposition, which reverses the institutional reading: between-region
> inequality in embodied exposure is 1.6 to 3.7 times LARGER than in cognitive exposure.
> The figure is at paper/figures/fig_concentration_breadth_scale.png.


`src/geo_breadth_scale.py`, ACS PUMS 2023, four breadths by two exposure types by three
geographic scales, plus Moran's I on 2024 Gazetteer county centroids and a Theil
decomposition against CBSA. Output `data/processed/geo_breadth_scale.csv`.

Statistic throughout: the at-risk RATE, group wage bill over local wage bill, which
normalises out area size.

Cognitive here is Felten AIOE. It measures TASK OVERLAP, not displacement and not timing,
and top-quintile occupations include likely-augmented work.

### Concentration against breadth and scale

| Breadth | Type | PUMA Gini | PUMA p99/p1 | County Gini | County p99/p1 | Metro Gini |
|---|---|---|---|---|---|---|
| Top 10% | Cognitive | 0.278 | 11.03 | **0.230** | 7.17 | **0.218** |
| Top 10% | Embodied | **0.313** | **31.46** | 0.179 | 6.48 | 0.183 |
| Top 20% | Cognitive | 0.217 | 6.17 | **0.176** | 4.51 | **0.167** |
| Top 20% | Embodied | **0.285** | **19.41** | 0.156 | 5.65 | 0.161 |
| Top 30% | Cognitive | 0.176 | 4.30 | **0.143** | 3.37 | **0.137** |
| Top 30% | Embodied | **0.242** | **11.98** | 0.134 | 4.35 | 0.136 |
| Top 50% | Cognitive | 0.125 | 2.78 | 0.103 | 2.44 | 0.099 |
| Top 50% | Embodied | **0.194** | **7.57** | 0.104 | 3.13 | 0.104 |

### Finding 1: the ordering REVERSES between PUMA and county

At PUMA level embodied exposure is more concentrated than cognitive at every breadth, on
both statistics, and on p99/p1 by a factor of two to three. **At county and metro level the
ordering flips and cognitive is more concentrated on the Gini at every breadth except the
broadest.**

A37 reported the PUMA ordering and called prediction 1 refuted. That stands at PUMA level.
But A37's conclusion, that embodied exposure is "the more concentrated of the two, hence the
more diversifiable", **does not survive the change of scale** and must be withdrawn as a
general statement. Which exposure type looks more concentrated depends on the geographic
unit, and the paper has to say which unit it means every time it says the word.

### Finding 2: the Theil decomposition explains the reversal and gives the honest version

County-level Theil T, decomposed within and between CBSA. Non-metro counties are pooled into
a single pseudo-group, which inflates the within share and is a known limitation of this
run.

| Breadth | Type | Moran's I | Theil total | Within metro | **Between metro** |
|---|---|---|---|---|---|
| Top 10% | Cognitive | 0.481 | 0.0720 | 33.1% | **66.9%** |
| Top 10% | Embodied | 0.441 | **0.1228** | 36.6% | 63.4% |
| Top 20% | Cognitive | 0.483 | 0.0459 | 31.8% | **68.2%** |
| Top 20% | Embodied | 0.484 | **0.1034** | 34.7% | 65.3% |
| Top 30% | Cognitive | 0.509 | 0.0302 | 28.8% | **71.2%** |
| Top 30% | Embodied | 0.501 | **0.0780** | 34.0% | 66.0% |
| Top 50% | Cognitive | 0.503 | 0.0140 | 28.9% | **71.1%** |
| Top 50% | Embodied | 0.535 | **0.0541** | 32.4% | 67.6% |

Two things read straight off this.

**Embodied inequality is larger in total at every breadth**, by a factor of 1.7 to 3.9 on
Theil T, and a larger fraction of it sits inside metros. Embodied exposure clusters at
sub-metro grain: particular industrial, agricultural and warehouse PUMAs inside otherwise
ordinary counties. That is why it dominates at PUMA level and washes out by county.

**Cognitive inequality is smaller in total but more between-metro**, 67 to 71 percent
against 63 to 68. Cognitive exposure is a property of which metro you are in.

The defensible statement, and it replaces both halves of A37's geography paragraph:

> Embodied exposure is concentrated within metropolitan areas and cognitive exposure is
> concentrated between them. Embodied exposure is the more unequal of the two in total at
> every group breadth. A lender with a national footprint diversifies embodied exposure by
> holding many metros; it cannot diversify cognitive exposure that way, because cognitive
> exposure varies across the metros themselves.

That reverses the direction of the diversifiability claim A37 made, and it is the first
version of the claim that is supported at both scales rather than at one.

### Finding 3: neither type is spatially random, which kills "near-uniformity" outright

Moran's I is 0.441 to 0.535 for every group at every breadth, against an expectation under
spatial randomness of -0.0003. **Both exposure types are strongly spatially autocorrelated
and the two are indistinguishable on this statistic.** Embodied exposure is not diffuse. It
is clustered and the clusters are contiguous.

### Finding 4: near-uniformity was a breadth artifact and A28 must be annotated

Concentration falls monotonically with breadth for both types, on every statistic, at every
scale. County Gini for embodied runs 0.179, 0.156, 0.134, 0.104 as the group widens from the
top tenth to the top half.

A28 reported embodied work as near-uniform at county Gini 0.141 using an above-median
definition. A37 got 0.156 using top quintile. **Neither is a fact about embodied work. Both
are facts about how wide a group was drawn.** A broad enough group approaches the whole
economy and its Gini approaches zero by construction, so "near-uniform" is not a finding at
any breadth, it is a restatement of the breadth.

**A28's near-uniformity claim is withdrawn as stated.** What replaces it is the schedule
above, reported as a schedule, with the breadth named in every sentence. The placebo control
from A37 remains the benchmark for what an unconcentrated group looks like: county Gini
0.090 at 20 percent of employment, against 0.156 for real embodied exposure at the same
breadth. Real groups are concentrated relative to the placebo at matched breadth, and that
comparison, not the raw Gini, is the one the paper should make.

### Not done

The single figure for this item is not drawn. The Theil non-metro pooling should be replaced
with individual non-metro counties as their own groups before this goes in the paper.

## A41. THE HOUSEHOLD STRESS ENGINE. Distress is far smaller than share attribution implied, and the exposure-type contrast survives in a form the project had not measured

`src/stress/`, four modules. ACS PUMS 2023 for payments (1,479,320 workers, 1,343,045
households, 131.33m weighted), SIPP 2025 for balances and buffers. Method documented in the
module docstrings, scenario grid in `data/processed/stress/scenario_definition.json`.

Precedents, all three verified against the publisher on 2026-09-19 and entered in
`paper/references.bib`: Meriküll and Rõõm (2020), microsimulation household stress test on
matched survey and register microdata, the closest methodological precedent; Albacete and
Fessler (2010), origin of the financial-margin construction; Bhutta, Bricker, Dettling,
Kelliher and Laufer (2019), cited for the scenario-driven framing and explicitly NOT for the
unit of analysis, which is county-level there and household-level here.

Cognitive rows throughout: AIOE and Eloundou GPT measure TASK OVERLAP, not displacement and
not timing. The engine converts that rank into a displacement probability BY ASSUMPTION.
That assumption is the weakest link in every cognitive number below and is not a measurement.

### The baseline, which has to come first

| Sample | Households | With an obligation | DSTI over 30 | DSTI over 40 | **DSTI over 50** |
|---|---|---|---|---|---|
| All | 131.33m | 93.66m | 33.5% | 23.2% | **17.6%** |
| Working core | 86.45m | 69.20m | 24.9% | 15.0% | **10.1%** |
| Non working | 44.89m | 24.46m | 58.0% | 46.3% | **38.9%** |

One in ten working-core households with a mortgage or rent is ALREADY above a 50 percent
debt-service-to-income ratio with no shock at all. Any post-shock level read without this
line is the same class of error as A6.

**A38 IS SUPERSEDED, see A47.** Building this engine turned up four separate errors in
A38's five-way table, not one, and the decomposition is reported in full in A47 rather than
asserted here. In short: vacant housing units were counted as households, the "employed"
test was wider than the engine's, the leans mixed two weight systems, and the working core
was defined by the reference person's age rather than by whether any member aged 25 to 64
is employed. **A38's dollar shares do NOT stand**, contrary to what I said when the vacancy
bug was first found and before the other three were isolated. The household total, 131.33m,
now matches the published benchmark of roughly 131m, which A31 could not reach.

### Result 1, and it weakens the thesis: a 10 percent displacement shock moves very little

Share of obligated working-core households crossing DSTI 50, uniform incidence, rho 0.65,
omega 0.75. Baseline 10.08 percent.

| Construct | 5 percent | 10 percent | 20 percent | Increment at 10 percent |
|---|---|---|---|---|
| Cognitive AIOE | 11.24% | **12.43%** | 14.93% | **+2.35pp** |
| Cognitive GPT | 11.23% | 12.42% | 14.90% | +2.34pp |
| Embodied | 11.03% | **12.00%** | 14.00% | **+1.92pp** |
| Robot reachable | 11.03% | 11.99% | 13.99% | +1.91pp |
| Gated | 11.14% | 12.19% | 14.34% | +2.11pp |
| Manipulation | 10.93% | 11.73% | 12.54% | +1.65pp |
| Driving | 10.75% | 10.75% | 10.75% | +0.67pp |

Replicate intervals are tight and simulation noise is negligible. Cognitive AIOE at the
central target: estimate 0.12432, ACS successive-difference standard error 0.00055, 95
percent interval [0.12325, 0.12538], simulation standard deviation across draws 0.00012.

**Displacing a tenth of all US employment, concentrated in the most exposed occupations,
raises the share of obligated working households above a 50 percent DSTI by 2.35 percentage
points.** It does not double it, or move it by half. The household balance sheet absorbs the
shock through non-wage income, second earners and reemployment. This is the single most
thesis-damaging number the project has produced, and it is the number the paper has to open
with rather than bury.

Driving is **capped**: all six driving occupations together are 6.04m workers, 3.29 percent
of employment, so even total displacement of every driver cannot reach a 5 percent scenario.
The engine reports this rather than scaling an impossible shock, and the 0.67pp is the
ceiling of the entire driving channel.

### Result 2, which is new and which is a genuine exposure-type contrast

Increment in DSTI-50 crossings per billion dollars of wage income actually lost:

| Construct | Wage loss (USD bn) | Increment (pp) | **pp per USD bn** |
|---|---|---|---|
| Manipulation | 202.8 | 1.65 | **0.00813** |
| Driving | 101.8 | 0.67 | **0.00658** |
| Gated | 338.6 | 2.11 | 0.00623 |
| Embodied | 312.5 | 1.92 | **0.00613** |
| Robot reachable | 322.0 | 1.91 | 0.00593 |
| Cognitive GPT | 604.0 | 2.34 | 0.00387 |
| Cognitive AIOE | 687.9 | 2.35 | **0.00342** |

**Embodied displacement is 1.8 times more distress-efficient than cognitive displacement per
dollar of wage income destroyed, and general-purpose manipulation is 2.4 times.** A cognitive
shock destroys 688bn dollars of wages and produces 2.35 percentage points of crossings; an
embodied shock destroys 313bn, less than half, and produces 1.92.

This is the contrast the project has been looking for and could not find in the lean tables.
It is not about who holds more debt. It is about how close to the threshold the debt-holding
households already sit. Cognitive exposure concentrates in households with income to spare;
embodied exposure concentrates in households without it. **The same dollar of destroyed wages
does roughly twice as much balance-sheet damage when it is embodied.**

It also survives the check that the lean tables failed: it is a household-level result, not
an aggregation of group shares, and it holds on both cognitive definitions.

### Result 3: incidence barely moves household COUNTS. It moves DOLLARS by three times

Share of obligated working-core households crossing DSTI 50 at the central target:

| Construct | Lowest wage first | Uniform | Highest wage first | Max over min |
|---|---|---|---|---|
| Cognitive AIOE | 12.01% | 12.43% | 12.78% | 1.064 |
| Cognitive GPT | 11.95% | 12.42% | 12.80% | 1.071 |
| Embodied | 11.42% | 12.00% | 12.47% | 1.092 |
| Robot reachable | 11.43% | 11.99% | 12.45% | 1.089 |
| Gated | 11.88% | 12.19% | 12.51% | 1.053 |
| Manipulation | 11.47% | 11.73% | 12.02% | 1.049 |

On household counts the spread is 5 to 9 percent. **On the dollars those households owe it
is 1.75 to 3.01 times**, reported in full in A42. Displacing the highest earners inside an
occupation produces slightly more distressed households and far more distressed dollars,
because they carry more of their household's income and sit on larger obligations.

A financial-stability claim is about dollars. **No dollar figure from this engine may be
quoted without naming the incidence assumption.** The household-count figures are robust to
it and can stand alone.

### Result 3b: SIPP INDEPENDENTLY REPRODUCES the result, which is the first clean C2 pass in the project

`src/stress/run_sipp.py`, SIPP 2025, reference-person weights, working core. A different
survey, a different sample size, a different occupation coding and a different income
concept.

| | ACS baseline | ACS at 10 percent | ACS increment | SIPP baseline | SIPP at 10 percent | SIPP increment |
|---|---|---|---|---|---|---|
| Cognitive AIOE | 10.08% | 12.43% | **+2.35pp** | 12.74% | 15.07% | **+2.33pp** |
| Cognitive GPT | 10.08% | 12.42% | +2.34pp | 12.74% | 15.27% | +2.53pp |
| Embodied | 10.08% | 12.00% | **+1.92pp** | 12.74% | 14.58% | **+1.84pp** |
| Manipulation | 10.08% | 11.73% | +1.65pp | 12.74% | 14.22% | +1.48pp |
| Driving | 10.08% | 10.75% | +0.67pp | 12.74% | 13.49% | +0.75pp |

The LEVELS differ, as they should: SIPP's baseline DSTI-50 share is 12.74 percent against
ACS's 10.08, because SIPP measures the housing payment and the income concept differently.
**The INCREMENTS agree to within 0.2 percentage points on every construct**, and the ordering
is identical. Claim 38 clears C2.

### Result 3c: buffers confirm Result 2 on a measure ACS cannot see at all

Share of working-core households with under three and under six months of runway, where
runway is liquid plus non-retirement financial assets divided by the monthly income
SHORTFALL the shock creates. Central target, uniform incidence.

| Construct | Wage loss (ACS, USD bn) | Under 3 months | Under 6 months |
|---|---|---|---|
| **Embodied** | 312.5 | **5.01%** | **6.40%** |
| Cognitive GPT | 604.0 | 4.45% | 6.12% |
| Manipulation | 202.8 | 4.50% | 5.65% |
| Cognitive AIOE | 687.9 | **4.06%** | **5.69%** |
| Driving | 101.8 | 2.05% | 2.50% |

**Embodied displacement puts MORE households under three months of runway than cognitive
displacement does, from less than half the wage loss.** On the buffer measure the embodied
figure exceeds the cognitive one outright, not merely per dollar. This is Result 2 confirmed
on an independent survey and on a completely different quantity, and it is the strongest
form the exposure-type contrast has taken anywhere in this project.

**The runway contrast is statistically significant and the DSTI contrast is not.** SIPP Fay
intervals, 240 replicates, rho 0.5, on the restricted sample:

| Statistic | Cognitive AIOE | Embodied | Overlap |
|---|---|---|---|
| Runway under 3 months | 0.04065 [0.03765, 0.04364] | 0.05013 [0.04755, 0.05270] | **none** |
| Share crossing DSTI 50 | 0.15071 [0.13967, 0.16174] | 0.14579 [0.13488, 0.15669] | substantial |

So in SIPP the exposure-type difference is demonstrable on BUFFERS and not on DSTI, which is
what a sample of 6,734 households can and cannot support. In ACS, where the replicate
standard error on the DSTI share is 0.00055, the DSTI difference (0.12432 against 0.11996)
is far outside sampling error. **Taken together: the contrast is real on both measures, but
the SIPP DSTI figure on its own does not establish it and must not be quoted as if it did.**

For scale, the baseline is severe on its own terms: **26.8 percent of working-core households
could not pay three months of housing costs out of liquid and non-retirement financial assets
with no income at all**, before any shock. That is the bounded upper-bound runway definition;
the shortfall-based definition above is the one used for the shock comparison. Both are
reported because neither can be made realistic without a measured consumption floor, which
this repository does not have and will not invent.

### Result 4: rho dominates every other uncertainty, so the blocked BLS series is the binding constraint

Increment in DSTI-50 crossings, central target, working core, percentage points:

| Construct | rho | omega 0.65 | omega 0.75 | omega 0.82 |
|---|---|---|---|---|
| Cognitive AIOE | 0.50 | 3.37 | 3.19 | 3.10 |
| | 0.65 | 2.58 | **2.35** | 2.23 |
| | 0.80 | 1.79 | 1.53 | 1.39 |
| Embodied | 0.50 | 2.67 | 2.50 | 2.40 |
| | 0.65 | 2.14 | **1.92** | 1.78 |
| | 0.80 | 1.60 | 1.33 | 1.17 |

Across the plausible range the headline moves by a factor of 2.2 for cognitive and 2.1 for
embodied, and rho moves it far more than omega does. **rho is not a nuisance parameter here,
it is the parameter**, and the Displaced Worker Survey that would pin it down is the one
series still blocked. Until then every engine figure is reported across the rho grid and
none is quoted at a single value.

Note that the exposure-type ORDERING is unchanged at every cell of the grid, so Result 2 does
not depend on rho.

## A42. ITEM 3. The retired method OVERSTATES the distress-relevant figure by about five times, and incidence moves DOLLARS by three times while barely moving household counts

`src/stress/run_compare.py` runs the retired rule and the engine on the same households, the
same scenario and the same exposure construct.

    SHARE-BASED (retired)  household obligation multiplied by the fraction of household wage
                           income earned in exposed occupations, times displacement intensity
    ENGINE                 obligations owed by households the shock actually pushes across a
                           DSTI threshold, NET of the baseline that already crosses it

Cognitive rows carry the task-overlap caveat.

### Annual mortgage service, USD billions, UNIFORM incidence

| Construct | Target | Share-based | Engine DSTI 30 | Engine DSTI 50 | Ratio at 30 | **Ratio at 50** |
|---|---|---|---|---|---|---|
| Cognitive AIOE | 5% | 59.5 | 18.2 | 12.0 | 0.306 | 0.202 |
| Cognitive AIOE | 10% | 119.0 | 36.7 | 24.5 | 0.309 | **0.206** |
| Cognitive AIOE | 20% | 237.1 | 75.1 | 51.2 | 0.317 | 0.216 |
| Cognitive GPT | 10% | 104.7 | 32.6 | 21.6 | 0.312 | 0.207 |
| Embodied | 5% | 27.2 | 8.1 | 5.5 | 0.299 | 0.203 |
| Embodied | 10% | 54.3 | 16.3 | 11.1 | 0.300 | **0.204** |
| Embodied | 20% | 108.7 | 33.0 | 22.8 | 0.303 | 0.210 |
| Robot reachable | 10% | 54.8 | 16.3 | 11.1 | 0.297 | 0.203 |
| Gated | 10% | 58.4 | 18.3 | 12.8 | 0.313 | 0.219 |
| Manipulation | 10% | 33.6 | 9.1 | 6.3 | 0.271 | 0.187 |
| Driving | capped | 17.4 | 5.2 | 3.6 | 0.300 | 0.207 |

Across all 21 cells: ratio at DSTI 50 runs **0.185 to 0.219, mean 0.205**; at DSTI 30,
**0.264 to 0.318, mean 0.301**. Rent behaves the same way, 0.287 to 0.314 at DSTI 50.

### What this says

**1. The retired method overstates by about five times at DSTI 50 and three and a third
times at DSTI 30.** Every superseded dollar figure produced by share attribution and then
read as an amount at risk is too large by roughly that factor. The figures were never wrong
as statements about which obligations sit on exposed wages. They were wrong every time the
text went on to call them obligations at risk.

**2. The overstatement is close to uniform across constructs and scenario sizes**, which
partly rehabilitates the old numbers for one purpose: **as a RANKING they hold, as LEVELS
they do not.** That is why A36 and A38's ordering of the exposure types survives the method
change while their magnitudes do not.

### 3. The incidence result, which corrects what I wrote in A39 AND what I first read here

Central target, mortgage service in USD billions:

| Construct | Lowest wage first | Uniform | Highest wage first | Max over min |
|---|---|---|---|---|
| **Engine dollars** | | | | |
| Cognitive AIOE | 13.7 | 24.5 | 36.5 | **2.66** |
| Embodied | 5.7 | 11.1 | 17.1 | **3.01** |
| Manipulation | 4.3 | 6.3 | 7.5 | 1.75 |
| **Share-based dollars** | | | | |
| Cognitive AIOE | 74.8 | 119.0 | 165.4 | 2.21 |
| Embodied | 34.4 | 54.3 | 77.3 | 2.25 |
| **Engine household share crossing DSTI 50** | | | | |
| Cognitive AIOE | 12.01% | 12.43% | 12.78% | 1.064 |
| Embodied | 11.42% | 12.00% | 12.47% | 1.092 |

**Who inside an exposed occupation loses the job barely changes how many households fall
into distress, and changes by three times how many dollars of mortgage those households
owe.** The two statistics point the same way and differ in sensitivity by a factor of thirty.
A financial-stability claim is about dollars, so the dollar sensitivity is the one that
binds, and no dollar figure from this engine should be quoted without the incidence
assumption named beside it.

**A39's speculation is withdrawn, and so is my first reading of this table.** A39 said that
if displacement hit the lower part of an exposed group first, proportional attribution would
understate the damage, possibly by a large multiple. The direction is wrong: low-wage-first
displacement produces FEWER distressed dollars on both methods, because low earners inside an
occupation are disproportionately secondary earners whose loss the household absorbs. The
attribution error also runs the other way, and gets worse rather than better under
low-wage-first: the engine-to-share ratio falls from 0.206 to 0.183 for cognitive AIOE and
from 0.204 to 0.165 for embodied, so share attribution overstates MOST when displacement is
concentrated on low earners.

Earlier in this session I reported the incidence spread as 5 to 9 percent and called A39's
concern unfounded. That was the household-count statistic. On dollars the spread is 1.75 to
3.01 times, and A39's concern about magnitude was justified even though its direction was
not.

### Superseded in place

Marked in `notes/findings.md` as share-attributed LEVELS that must be recomputed through the
engine before use, rankings unaffected: A17, A29, and the pathway dollar tables in A24 and
A32.

## A43. ITEM 2. The wage-backed denominator, and the second-round link to OASDI that must not be double counted

Every pass-through figure in the paper now uses the WAGE-BACKED portion of obligations as
its denominator. The non-wage-backed portion is reported separately and never folded in.

### The split, ACS PUMS 2023, occupied units only

| Sample | Households | Weighted | Share of mortgage service | Share of rent |
|---|---|---|---|---|
| Working core (an employed member aged 25 to 64) | 86.45m | 65.8% | 84.0% | 72.8% |
| Non working | 44.89m | 34.2% | **16.0%** | **27.3%** |

The working-core definition is "contains at least one employed member aged 25 to 64", not
"the reference person is aged 25 to 64", which is the definition A38 used and which is wrong
for a displacement question: a household where a forty-year-old works and the reference
person is sixty-eight has prime-age wage income to lose.

**Sixteen percent of national mortgage service and twenty-seven percent of national rent is
paid by households with no prime-age employed member.** In the first round those obligations
are insulated from AI displacement entirely. They are serviced out of Social Security,
pensions, disability payments, investment income and drawdown of savings.

These households are also the most stressed group in the data by a wide margin: 38.9 percent
of them with an obligation are already above a 50 percent debt-service-to-income ratio,
against 10.1 percent for working-core households. Their fragility is real and it is not an
AI story.

### The second round, stated and deliberately NOT added

Their transfer income is not independent of the wage bill. A32 established the link and the
arithmetic is already in the repository:

- Payroll taxes are **91.3 percent** of OASDI trust fund income.
- At 25 percent displacement of embodied work, payroll tax at stake is **7.9 percent of OASDI
  payroll income**, 104.6bn dollars.
- The combined OASDI funds already ran a **160.2bn dollar deficit** in 2025.

So a displacement shock that leaves non-working households untouched in the first round
erodes, in the second round, the earmarked revenue that funds the transfers those households
service their obligations from. The 16 percent of mortgage service and 27 percent of rent
that looks insulated is insulated only for as long as the trust funds are.

**This is stated as a mechanism and is NOT added to any total.** The payroll tax loss is
already counted once, in A32 and A34, as part of the fiscal channel. Adding the obligations
of non-working households to a displacement total would count the same wage loss twice: once
as lost payroll tax and again as the transfer income that payroll tax funds. Any figure in
the paper that combines the household channel and the fiscal channel must therefore either
exclude non-working households from the household side or exclude the OASDI component from
the fiscal side, and must say which it did.

### Consequence for the thesis

The original framing treated Leg W as credit underwritten against human labour income. On the
measured split, **about a sixth of mortgage obligations and over a quarter of rent are not
underwritten against current labour income at all.** Leg W is smaller than the household debt
stock, and the paper must size it as the wage-backed portion. The insulated remainder is not
a safety margin, because the second-round channel above runs straight through it, but the two
effects operate on different timescales and through different institutions and cannot be
summed.

## A44. ITEM 5. The ACS against SIPP gap is BOUNDED, not resolved, and holding the measure fixed produces a selection-versus-intensity decomposition that explains the engine result

`src/stress/reconcile_acs_sipp.py`. A39 reported embodied mortgage lean 0.90 in ACS and 0.77
in SIPP. The two differed on three things at once. Held fixed:

| Row | Source | Measure | Denominator | Embodied | Cognitive AIOE | Cognitive GPT |
|---|---|---|---|---|---|---|
| A | ACS | Annual mortgage SERVICE | Household earnings | **0.919** | 0.943 | 0.964 |
| B | SIPP | Annual mortgage PAYMENT | Household earnings | **1.052** | 0.729 | 0.771 |
| C | SIPP | Mortgage BALANCE | Household earnings | 0.758 | 0.977 | 0.966 |
| D | ACS | Annual mortgage SERVICE, MORTGAGE HOLDERS ONLY | Household earnings | **1.009** | 0.845 | 0.920 |

### Answer 1: SIPP cannot settle it, and that is the honest resolution

The Fay interval on the SIPP embodied payment lean is **1.052 with a standard error of
0.249, 95 percent interval [0.565, 1.540]**. ACS's 0.919 sits comfortably inside it. On 6,734
households SIPP cannot distinguish a lean of 0.6 from a lean of 1.5, so it can neither
confirm nor contradict ACS on this quantity.

**The gap A39 reported was not a disagreement between two measurements. It was a comparison
of a service figure with a balance figure, plus a denominator difference, wrapped around a
SIPP estimate too imprecise to carry either.** ACS is the headline under the raw-dollar-share
rule: 100,584 households against 6,734, and a replicate standard error three orders of
magnitude smaller. SIPP is reported as consistent and uninformative, not as agreement.

Claim 16 ("ACS and SIPP agree on the embodied mortgage lean") stays withdrawn. It is replaced
by "ACS measures it; SIPP cannot."

### Answer 2, which is the substantive finding: SELECTION and INTENSITY run in opposite directions

Compare rows A and D, both ACS, both service, both earnings, differing only in whether the
sample is conditioned on actually holding a mortgage:

| | All working-core households | Mortgage holders only | Direction |
|---|---|---|---|
| Embodied | 0.919 | **1.009** | rises |
| Cognitive AIOE | 0.943 | **0.845** | falls |
| Cognitive GPT | 0.964 | 0.920 | falls |

**Cognitive households are more likely to hold a mortgage at all; conditional on holding one,
embodied households carry MORE mortgage service per dollar earned.** Unconditionally the two
look alike, which is what A36 and A38 found and reported as "indistinguishable". Conditionally
they separate, and they separate in the direction the stress engine independently found.

This is the mechanism behind A41 Result 2. Embodied displacement is more distress-efficient
per wage dollar because, among households that actually carry a mortgage, embodied households
carry a proportionally heavier one. The lean tables could not see it because they averaged
owners and renters together, and the selection effect and the intensity effect cancelled.

**Claim 14 is amended rather than withdrawn.** "Mortgage leans are indistinguishable across
exposure types" is true unconditionally and false conditional on tenure. Both halves must be
stated together, because quoting only the first is what produced A35's error and quoting only
the second would reintroduce it with the sign flipped.

### The SIPP balance against payment reversal, flagged and not explained

Within SIPP, embodied households have the LOWEST balance lean (0.758) and the HIGHEST payment
lean (1.052), while cognitive households show the reverse. A high payment on a low balance
implies shorter remaining term, higher rate, or a larger principal component, and this
repository has no data that distinguishes those. It is also inside the interval noise. It is
recorded as an open question and nothing is built on it.

## A45. ITEM 6 PARTIAL. The Chicago Fed Leg A figures are obtained and verified, and they make Leg A roughly one fiftieth of Leg W

> **The rho and omega status in this entry is superseded.** BLS became reachable and both
> parameters are now sourced (A48), corrected (A48) and restated as R (A50). The Leg A
> figures in this entry are unaffected.


The owner offered to place this article in `data/raw/manual/`. It was not needed: the
Chicago Fed page is reachable from this environment and was read directly.

**Source, verified against the publisher page on 2026-09-19:** Greg Cohen, Cooper Killen and
Simon Lau, "Tail Risk for Banks Posed by Investments in Generative Artificial Intelligence",
Chicago Fed Insights, Federal Reserve Bank of Chicago, February 2026. Entered in
`paper/references.bib` with every figure transcribed, and in `data/SOURCES.md`.

### The measured Leg A figures, quoted as the article states them

| Measure | Figure |
|---|---|
| Average bank outstanding to AI-adjacent industries | about 0.8 percent of bank total assets |
| Large-bank C and I commitments to AI-adjacent industries, 2015 | about 9 percent of total commitments, about 250bn USD |
| Large-bank C and I commitments to AI-adjacent industries, late 2025 | about 13 percent of total commitments, about 450bn USD |
| Software industry commitments | 150bn USD early 2022 to 191bn USD late 2025 |
| Energy and semiconductor commitments combined | about 275bn USD |
| C and I OUTSTANDING exposure to AI-adjacent industries | averages 9 percent of tier 1 capital |
| C and I COMMITTED exposure to AI-adjacent industries | about 25 percent of tier 1 capital |
| Software commitments rated B and below | about 26 percent, 50bn USD |
| Energy and semiconductor commitments rated B and below | 15bn USD |

This is a SECONDARY source reporting supervisory data this repository cannot access. Every
figure above is attributed to it and none is presented as this project's own measurement.

### The rebuilt Leg A to Leg W ratio, and it damages the two-sided framing

Both sides as STOCKS, which is the only comparison that is not a category error. The earlier
repository figures compared a stock to an annual service flow in places and must not be
reused.

Leg W, Financial Accounts of the United States via FRED, 2026 Q2:

| Series | Level |
|---|---|
| CMDEBT, households and nonprofits, debt securities and loans | 21,377.8bn USD |
| HHMSDODNS, one-to-four family residential mortgages | 14,010.9bn USD |

Leg A, bank channel, Chicago Fed, late 2025: **450bn USD committed**.

| Ratio | Value |
|---|---|
| Leg A committed / Leg W total household debt | **2.1 percent** |
| Leg A committed / Leg W residential mortgages | **3.2 percent** |

**The measured bank channel of Leg A is roughly one fiftieth the size of Leg W.** A framing
that presents the two as comparable sides of one bet is not supported by the only measured
figures either side has. The asymmetry is the finding.

### Three reasons this is a LOWER BOUND on Leg A, stated so the ratio is not over-read

1. It is the bank channel only. A9 verified the BIS on off-balance-sheet AI financing
   through special purpose vehicles, minority stakes and long-term leases, none of which
   appears in C and I commitments.
2. It excludes corporate bond issuance and private credit. Search results reported a Morgan
   Stanley projection of a further 800bn USD of private-credit data-centre financing over
   two years; that figure is SECONDARY, UNVERIFIED and is recorded in `lit/unverified.md`,
   not used.
3. Commitments are not the same as drawn exposure. Outstanding is materially smaller: 9
   percent of tier 1 capital against 25 percent committed.

Even at three times the measured figure, Leg A would remain under a tenth of Leg W. The
direction of the conclusion is robust to the bound; the exact ratio is not, and only the
bound should be quoted.

### What this does to the thesis

The original brief set up a symmetric two-sided bet. **The sides are not symmetric in size,
and the paper cannot claim they are.** What survives is a claim about DIFFERENCE IN KIND
rather than in magnitude: Leg W is large, diffuse across 131m households, and slow to
enforce; Leg A is small, concentrated in a handful of large banks at 25 percent of tier 1
capital committed, and fast to enforce. Concentration relative to capital, not absolute
size, is the channel through which Leg A could matter, and the 25 percent of tier 1 figure
is the number that carries that argument.

## A46. ITEM 4. Geography repaired, figure drawn, and the proposed institutional reading is NOT what the numbers support

The Theil decomposition no longer pools every non-metro county into one pseudo-group. Metro
counties group by CBSA and non-metro counties form STATE NON-METRO REMAINDERS, giving 973
geographically coherent groups. Figure at
`paper/figures/fig_concentration_breadth_scale.png`, data at
`data/processed/geo_breadth_scale.csv`.

Cognitive here is Felten AIOE, which measures task overlap, not displacement or timing.

### The repaired decomposition

County-level Theil T of the local at-risk rate, decomposed within and between region groups.

| Breadth | Type | Moran's I | **Theil total** | Within, abs | **Between, abs** | Within % | Between % |
|---|---|---|---|---|---|---|---|
| Top 10% | Cognitive | 0.481 | 0.0720 | 0.0236 | 0.0484 | 32.8% | 67.2% |
| Top 10% | Embodied | 0.441 | **0.1228** | 0.0443 | **0.0785** | 36.1% | 63.9% |
| Top 20% | Cognitive | 0.483 | 0.0459 | 0.0144 | 0.0316 | 31.3% | 68.7% |
| Top 20% | Embodied | 0.484 | **0.1034** | 0.0354 | **0.0681** | 34.2% | 65.8% |
| Top 30% | Cognitive | 0.509 | 0.0302 | 0.0085 | 0.0217 | 28.2% | 71.8% |
| Top 30% | Embodied | 0.501 | **0.0780** | 0.0262 | **0.0518** | 33.6% | 66.4% |
| Top 50% | Cognitive | 0.503 | 0.0140 | 0.0039 | 0.0100 | 28.3% | 71.7% |
| Top 50% | Embodied | 0.535 | **0.0541** | 0.0174 | **0.0367** | 32.1% | 67.9% |

The repair barely moved the percentages, by under 1.5 points anywhere, so the earlier A40
figures were not materially distorted by the pooling. The repair is kept because the earlier
grouping was indefensible, not because it changed the answer.

### The proposed reading, tested, and it FAILS

The reading to be checked was: diversification addresses idiosyncratic regional shocks, not
a common one; a SMALL between-metro share for embodied means near-equal exposure across
lenders and a uniform systemic load, while a LARGE between-metro share for cognitive means
exposure concentrated in lenders to specific high-cost metros and institution-specific
concentration risk.

**The first half of the premise holds and the conclusion does not follow from it.**

The percentage split is directionally as proposed: embodied between-region share is 63.9 to
67.9 percent, cognitive 67.2 to 71.8. But the gap is **3 to 5 percentage points**, and a
difference that small cannot carry an institutional distinction between "uniform systemic
load" and "institution-specific concentration".

More decisively, the percentage split is the wrong statistic for the question. What
determines how much a lender's exposure varies with its regional footprint is the ABSOLUTE
between-region variation, not its share of that type's own total. On the absolute
decomposition the ordering is the opposite of the proposed reading:

> **Between-region inequality in embodied exposure is 1.6 to 3.7 times larger than in
> cognitive exposure at every breadth** (0.0785 against 0.0484 at the top tenth; 0.0367
> against 0.0100 at the top half).

A lender with a regionally concentrated book faces MORE dispersion in embodied exposure than
in cognitive exposure, not less. The proposed institutional reading has it backwards.

### What the numbers DO support

1. **Neither exposure type is diversifiable within a metro.** Both are two-thirds to
   three-quarters between-region at every breadth. Spreading a book across neighbourhoods or
   counties inside one metropolitan area removes at most a third of the geographic variation
   for either type. This is the part of the proposed reading that survives, and it applies
   equally to both types rather than distinguishing them.

2. **Embodied exposure is the more geographically unequal of the two in total**, by 1.7 to
   3.9 times on Theil T, and that holds at every breadth.

3. **Neither is spatially random.** Moran's I runs 0.441 to 0.535 against an expectation of
   -0.0003 under spatial randomness. The two types are indistinguishable on this statistic,
   so "embodied exposure is diffuse" is false in every sense the data can test.

4. **The Gini ordering reverses with scale**, and the figure shows it: embodied is more
   concentrated at PUMA, cognitive at county and metro, converging at the broadest
   definition. Any sentence using the word "concentrated" must name the scale.

### The defensible sentence, replacing both A37's and A40's

> Both exposure types are predominantly between-region phenomena, so within-metro
> diversification is not available for either. Embodied exposure is the more unequal of the
> two in total and across regions, and is additionally clustered at sub-metro grain in a way
> cognitive exposure is not. A lender diversifies neither by geography alone; the difference
> between the two is that an embodied book is more sensitive to WHICH regions it is in.

This is weaker than "Physical AI adds the undiversifiable geography" and it is the version
the measurements support. Claim 24 is amended: the between-region share is only marginally
higher for cognitive, and in absolute terms it is higher for embodied.

### Remaining gap

Moran's I and the Theil decomposition are computed for Felten AIOE only, not for Eloundou
GPT, so claims 24 and 26 remain provisional on C1. Moran's I is county-level only, so claim
26 remains provisional on C5.

## A47. A38 CORRECTED, with the correction decomposed. Four things were wrong, not one, and the rent contrast is the casualty

`src/stress/decompose_a38.py`. A38's five-way table is superseded. Reporting the new numbers
without saying which change caused what would be the same silent substitution this project
keeps catching, so each fix is applied cumulatively.

### Felten AIOE. A38 as published, then each fix

| Stage | Class | Households | Wage bill | Mortgage | Rent | Mortgage lean | Rent lean |
|---|---|---|---|---|---|---|---|
| **A38 as published** | Cognitive only | 10.21 | 24.15 | 21.66 | 11.95 | 0.90 | **0.49** |
| | Embodied only | 14.19 | 16.93 | 15.15 | 16.81 | 0.90 | **0.99** |
| | Non working | **44.31** | 12.20 | 19.69 | 30.09 | 1.61 | 2.47 |
| **1. Vacancy and employment definition** | Cognitive only | 10.83 | 23.77 | 20.77 | 11.38 | 0.87 | 0.48 |
| | Embodied only | 13.59 | 15.49 | 13.06 | 14.70 | 0.84 | **0.95** |
| | Non working | 40.15 | 12.25 | 21.25 | 32.28 | 1.73 | 2.64 |
| **2. Plus one weight system** | Cognitive only | 10.83 | 24.26 | 20.77 | 11.38 | 0.86 | 0.47 |
| | Embodied only | 13.59 | 15.62 | 13.06 | 14.70 | 0.84 | 0.94 |
| | Non working | 40.15 | 10.98 | 21.25 | 32.28 | 1.94 | 2.94 |
| **3. Plus engine working-core definition** | Cognitive only | 11.43 | 25.26 | 21.50 | 11.80 | **0.85** | **0.47** |
| | Embodied only | 14.71 | 16.77 | 13.89 | 15.59 | **0.83** | **0.93** |
| | Non working | 34.18 | 6.30 | 15.98 | 27.25 | **2.53** | **4.32** |

### The four errors

**1. VACANT UNITS.** ACS carries vacant housing records with a positive housing weight,
14.0m weighted, 9.6 percent of records. They have no occupants, no income and no tenure.
A38 counted them as households and they all fell into the non-working class. This is why
A38's household total implied 145.33m rather than the published benchmark of about 131m,
and why non-working looked like 44.3 percent of households.

**2. THE "EMPLOYED" TEST, which I did not isolate separately and am reporting as such.**
Stage 1 applies the vacancy fix AND a narrower employment test at the same time: A38 counted
anyone with ESR in (1, 2, 4, 5); the engine counts a person only if they are employed, have
positive wage income, and have a codable occupation. Vacant units contribute zero dollars, so
they CANNOT move a dollar share. **Therefore every dollar-share movement between the A38 row
and stage 1 is attributable to the employment test alone**, and it is not small: non-working
mortgage share rises 19.69 to 21.25, rent 30.09 to 32.28. Households with an employed member
who reports no wage income, mostly self-employment, move out of the working class.

**3. TWO WEIGHT SYSTEMS.** A38 weighted the mortgage and rent numerators by the household
weight WGTP and the wage denominator by the person weight PWGTP. A lean built that way is
not a ratio of two shares of the same universe. Fixing it moves the non-working wage share
from 12.25 to 10.98 and its mortgage lean from 1.73 to 1.94.

**4. WORKING-CORE DEFINITION.** A38 required an employed member AND a reference person aged
25 to 64. That excludes a household where a forty-year-old works and the reference person is
sixty-eight, which is the wrong test for a displacement question. The engine requires an
employed member AGED 25 to 64. This is the largest single fix: non-working falls from 40.15
to 34.18 percent of households and its wage share from 10.98 to 6.30.

### What changes substantively

**The non-working over-holding result gets STRONGER, not weaker.** A38 said 19.7 percent of
mortgage service and 30.1 percent of rent on 12.2 percent of wages, leans 1.61 and 2.47.
Corrected: **16.0 percent of mortgage service and 27.3 percent of rent on 6.30 percent of
wages, leans 2.53 and 4.32.** Both dollar shares fall and both leans rise sharply, because
the corrected working-core definition moves prime-age earners out of the non-working class.

**The rent contrast is the casualty and claim 15 must be downgraded again.** A38's surviving
headline was that rent leans embodied at 0.99 against cognitive 0.49, a ratio of 2.0, and
A38 made much of embodied being "exactly proportional". Corrected, the embodied rent lean is
**0.93**, not 0.99. It is under-proportional like everything else, and the "exactly
proportional" reading was an artifact of the two-weight-system error. The RATIO survives at
0.93 / 0.47 = **1.98**, essentially unchanged, and on Eloundou GPT it is 0.93 / 0.62 = 1.50.

So the sentence that survives is the one A38 already narrowed to, and it narrows once more:
**every working class under-holds rent relative to its wages, and cognitive households
under-hold it about twice as much as embodied households do.** There is no group that
over-holds rent except the non-working, at 4.32.

**Mortgage leans stay uniform and drift down**: 0.85, 0.83, 0.80, 0.95 across the four
working classes against A38's 0.90, 0.90, 0.89, 0.93. Claim 14 is unaffected in substance.

### Consequence for the register

Claim 18 superseded by claim 42. Claim 15a amended: the embodied rent lean is 0.93 and not
proportional. Claim 44 recorded. A38 is annotated in place as superseded by A47.

## A48. OMEGA REPAIRED. My own sourced value from the last session was too high, and the corrected one puts the fiscal condition back where it was

Last session I replaced the stipulated omega of 0.75 with 0.9554 from DWS Table 7 and
reported that this pulled the break-even reemployment share down far enough that the observed
rho met it in 12 of 27 cells. **That figure of 0.9554 was wrong on two counts and the
conclusion drawn from it is withdrawn.**

### Error 1: it priced only full-time to full-time moves

DWS Table 7 covers reemployment into full-time wage and salary work. Of 1,942 thousand
long-tenured workers who lost full-time jobs and were employed at the survey date:

| Destination | Thousands | Share | Earnings ratio |
|---|---|---|---|
| Full-time wage and salary | 1,593 | 82.03% | 0.960 to 1.010, Table 7 bands |
| Part-time | 197 | 10.14% | **0.3206**, CPS Table 38 over Table 37, 2025 |
| Self-employed or unpaid family | 152 | 7.83% | 0.70 to 1.00, STATED, not sourced |

The part-time ratio is sourced: median usual weekly earnings, 386 against 1,204 USD in 2025
(380 against 1,159 in 2024). I had stipulated 0.50 as a placeholder. The sourced value is
**a third, not a half**, so a tenth of the reemployed were being credited with fifty percent
more income than the data support.

**Blended omega, nominal: 0.9073 central, range 0.8750 to 0.9577.**

Caveat that travels with the part-time leg: it is a ratio of medians across two different
populations, not what a displaced full-time worker gets on moving to part-time. Displaced
long-tenured workers are older and more experienced than the median part-time worker, so
0.32 is a floor and an upper case of 0.50 is carried as a labelled assumption. The
self-employed leg is not sourced at all and is flagged wherever it appears.

### Error 2, which is conceptual: nominal against counterfactual

Table 7 compares nominal earnings on the new job with nominal earnings on a job lost up to
three years earlier. **The fiscal condition does not need that ratio.** The condition
tau_k*s + tau_l*rho*omega >= tau_l compares tax raised after displacement against tax that
WOULD have been raised on the same workers absent displacement, and the counterfactual wage
bill grows with economy-wide wages. Using the nominal ratio credits displacement with general
wage growth that would have happened anyway.

Survey window January 2023 to December 2025, status measured January 2026, so mean elapsed
time is 18 months on a uniform-displacement assumption, reported across 1.0 to 2.0 years.
Employment Cost Index, wages and salaries, private industry: 159.4 to 177.5 over three years,
**3.65 percent a year**. CPI: 300.4 to 326.6, 2.82 percent a year.

| Concept | Value | Is it what the condition needs? |
|---|---|---|
| omega nominal | 0.9073 | No. Credits displacement with general wage growth |
| omega real | 0.8702 | No. Measures the worker's purchasing power |
| **omega counterfactual** | **0.8598** | **Yes** |

Range over every case and elapsed assumption: **0.8292 to 0.9076**.

### Net effect, and it runs AGAINST last session's report

| Version | omega | Status |
|---|---|---|
| Stipulated JLS | 0.75 | Wrong estimand: long-run loss including non-employment |
| Last session, full-time only, nominal | 0.9554 | Too high on both counts. **Withdrawn** |
| **This session, blended, counterfactual** | **0.8598** | The one the condition needs |

The correction moves omega back most of the way toward the stipulated value. Last session I
reported that sourcing omega weakened P1r substantially. **That report was premature and is
corrected below in A50.**

---

## A49. rho IS NOT A CONSTANT. Fourteen survey vintages give it as a function of labour slack, and the relationship is strong

`src/bls_dws_history.py`. Every reachable Worker Displacement vintage, read from the BLS
archive, with the civilian unemployment rate in the survey month.

| Release | rho | Survey unemployment |
|---|---|---|
| 2000-08-09 | **0.740** | 4.0 |
| 2002-08-21 | 0.650 | 5.7 |
| 2004-07-30 | 0.650 | 5.7 |
| 2006-08-17 | 0.700 | 4.7 |
| 2008-08-20 | 0.680 | 5.0 |
| 2010-08-26 | **0.490** | **9.8** |
| 2012-08-24 | 0.560 | 8.3 |
| 2014-08-26 | 0.610 | 6.6 |
| 2016-08-25 | 0.660 | 4.8 |
| 2018-08-28 | 0.660 | 4.0 |
| 2020-08-27 | 0.700 | 3.6 |
| 2022-08-26 | 0.650 | 4.0 |
| 2024-08-29 | 0.657 | 3.7 |
| 2026-08-27 | 0.661 | 4.3 |

**Ordinary least squares, 14 vintages:**

> **rho = 0.8090 - 0.0304 x unemployment rate**,
> slope standard error 0.0042, t = -7.20, **R-squared 0.812**

Every extra percentage point of unemployment costs **3.04 percentage points** of the
reemployment rate. Observed rho spans **0.49 to 0.74** over an unemployment range of 3.6 to
9.8 percent.

**This replaces the stipulated functional form the previous prompt asked for.** The frontier
does not need an invented rule for how absorption falls with displacement: the relationship
is measured, on fourteen observations, with an R-squared of 0.81.

**The limit, stated plainly: 9.8 percent is the worst labour market in the sample.** A
displacement scenario that pushes unemployment beyond that is outside the fitted range and
the line must not be extrapolated there without saying so on the figure and in the text.
Nothing in these data speaks to reemployment when a tenth of all employment is displaced at
once.

### Eight vintages are missing and I am naming them

The survey has run biennially since 1984. The BLS archived-release index lists 2008 onward;
the historical text path yielded 2000, 2002, 2004 and 2006. **Absent: the January reference
years 1984, 1986, 1988, 1990, 1992, 1994, 1996 and 1998.** An exhaustive scan of every date
from June to December of 1990, 1992, 1994, 1996 and 1998 at the historical path returned
nothing. The fit therefore covers 2000 onward, and the 1980s recessions, which would have
extended the slack range, are not in it.

## A50. THE FISCAL CONDITION IN ONE STATISTIC. R = rho x omega, and the verdict turns on the capital tax rate, not on the labour market

`src/retained_wage_share.py`. The retained wage share R is the fraction of the displaced wage
bill that survives as taxable labour income: the share reemployed times the wage they earn
against what they would otherwise have earned.

    without outlays, at s = 1:   R >= 1 - tau_k/tau_l
    with outlays g:              R >= 1 - (tau_k*s)/tau_l + g*(1 - rho)/tau_l

The outlay term is not a constant. It contains the same rho that is inside R, so a labour
market that reemploys fewer workers is penalised twice, once through a smaller R and once
through a larger outlay bill. The rho* formulation hid that interaction, which is the reason
for restating the condition this way.

### Observed R at the 2026 survey

| omega case | omega | **R** |
|---|---|---|
| **Counterfactual blended (the one the condition needs)** | **0.8598** | **0.5689** |
| Counterfactual blended, low to high | 0.8292 to 0.9076 | 0.5486 to 0.6005 |
| Nominal blended | 0.9073 | 0.6003 |
| Full-time only nominal (last session, withdrawn) | 0.9853 | 0.6519 |
| Stipulated JLS | 0.75 | 0.4962 |
| Switcher scenario, Huckfeldt | 0.58 | 0.3837 |

### Required R, and this is the finding

| tau_l | tau_k = 0.05 | tau_k = 0.10 | tau_k = 0.21 |
|---|---|---|---|
| AMR 0.255 | 0.8039 | **0.6078** | 0.1765 |
| Bottom-up 0.301 | 0.8339 | **0.6678** | 0.3023 |
| Bottom-up 0.318 | 0.8428 | **0.6855** | 0.3396 |

Observed R = 0.5689 against those:

| tau_l | tau_k = 0.05 | tau_k = 0.10 | tau_k = 0.21 |
|---|---|---|---|
| AMR 0.255 | -0.236 NOT MET | **-0.040 NOT MET** | +0.392 MET |
| Bottom-up 0.301 | -0.266 NOT MET | **-0.100 NOT MET** | +0.266 MET |
| Bottom-up 0.318 | -0.275 NOT MET | **-0.117 NOT MET** | +0.229 MET |

**The verdict is decided entirely by tau_k.** At the statutory upper rate of 21 percent the
condition passes in every cell, at every omega case in the table above, including the
switcher scenario. At the equipment and software rate of 5 percent it fails in every cell by
a wide margin. At the net capital rate of 10 percent it fails, but narrowly: the gap is
0.040 in the most permissive cell.

**This reframes P1r and it weakens the version the project has been telling.** The
proposition has been presented as a statement about whether displaced workers can be
reabsorbed fast enough. It is not. Moving omega from 0.75 to 0.9554 and back to 0.8598,
across the entire plausible range, never changes the verdict in any cell: the tau_k = 0.21
column always passes and the tau_k = 0.05 column never does. **Labour market absorption is
second order. The effective tax rate on AI capital is first order.**

That is a better paper than the one about reemployment speed, but it is a different one, and
it puts the weight on a parameter this repository has bounded rather than measured.

### Outlays

| g | Cells met, of 9 | Infeasible cells |
|---|---|---|
| 0.00 | 3 | 0 |
| 0.10 | 3 | 0 |
| 0.25 | 1 | 3 |

At g = 0.25 the condition becomes infeasible, requiring R above 1, in three of nine cells.
Outlays matter more than omega does.

### Historical vintages, and how many met the condition

omega held at the 2026 counterfactual value, rho varying by vintage. This is an assumption
and it is stated: if omega is procyclical, historical R in slack years is overstated here.

R ranges from **0.4213** (2010, unemployment 9.8) to **0.6362** (2000, unemployment 4.0).

| Cell | Vintages meeting the condition |
|---|---|
| tau_l 0.255, tau_k 0.10 | **1 of 14** (2000 only, R = 0.636 against 0.608) |
| tau_l 0.301, tau_k 0.10 | **0 of 14** |
| tau_l 0.318, tau_k 0.10 | **0 of 14** |
| any tau_l, tau_k 0.21 | 14 of 14 |
| any tau_l, tau_k 0.05 | 0 of 14 |

**In the tau_k = 0.10 column, one labour market out of fourteen cleared the bar, and it was
the tightest on record.** Under the switcher scenario, none do. The summary statistic "14 of
14 met the condition in at least one cell" is technically true and useless, because the
tau_k = 0.21 column passes unconditionally; it is reported here only so nobody quotes it.

---

## A51. POPULATION CAVEAT, SOURCED. DWS displaced workers mostly are not occupation switchers, and AI displacement is switching by construction

Verified against the AEA article page and the author's PDF: Christopher Huckfeldt,
"Understanding the Scarring Effect of Recessions", American Economic Review 112(4),
1273 to 1310, April 2022, doi 10.1257/aer.20160449. Entered in `paper/references.bib` with
the passages quoted verbatim.

Quoted exactly:

> "Workers who switch occupations subsequent to job displacement experience a 42 percent drop
> in earnings, twice as large as the 21 percent drop in earnings for workers who remain in
> the same occupation."

> "While occupation switchers continue to face markedly lower earnings a full decade after
> job loss, the wage and earnings losses of occupation stayers recover within four years."

Stayers recover "to 6.4 percent one year after displacement, and thereafter are not
significantly different from zero"; switchers show "relative losses remaining around 10
percent ten years after job displacement".

**These are measured "relative to counterfactual outcomes under no displacement", the same
basis as omega_counterfactual.** The two are directly comparable, which is unusual and worth
stating.

### Why this is the binding caveat on both parameters

The DWS population is workers displaced by plant closings, insufficient work and position
abolishment. Most can be and are reemployed in the same occupation, and Huckfeldt's stayers
recover fully within four years. **Displacement that eliminates an occupation forces
switching by construction.** A truck driver displaced because driving is automated cannot be
reemployed as a truck driver. The switcher end of Huckfeldt's distribution is therefore the
right analogue for the scenarios this paper is about, and the DWS average is the wrong one.

| Scenario | omega | **R at rho = 0.6616** | Met at tau_k = 0.10? |
|---|---|---|---|
| DWS average, counterfactual blended | 0.8598 | 0.5689 | No, gap 0.040 to 0.117 |
| Huckfeldt stayers, 21 percent loss | 0.79 | 0.5227 | No |
| **Huckfeldt switchers, 42 percent loss** | **0.58** | **0.3837** | **No, gap 0.224 to 0.302** |

Under switcher-level losses the gap at tau_k = 0.10 widens by a factor of three to five and
no historical vintage comes close. **This is the scenario the paper's own subject matter
implies**, and it is labelled as a scenario rather than a measurement because Huckfeldt's
population is recession-displaced workers, not workers whose occupation ceased to exist.

There is a second-order effect in the same direction that is NOT quantified here: Huckfeldt
finds "the cost and incidence of such occupation displacement is higher for workers who lose
their job during a recession", and A49 shows rho itself falls with slack. Both rho and omega
therefore deteriorate together in the states of the world the frontier is about, which the
frontier must handle jointly rather than one at a time.

## A52. CLAIM 30 REFRAMED. The fiscal condition has two levers and I overstated one of them

A50 ended with "labour market absorption is second order, the effective tax rate on AI
capital is first order". **That sentence goes too far and is withdrawn in that form.** What
A50 actually established is narrower: within the range that OMEGA can take, tau_k decides the
verdict. It does not follow that the labour market is irrelevant, because rho varies far more
than omega does.

| Lever | Observed variation | Effect on R |
|---|---|---|
| omega, across every case from switcher scenario to full-time nominal | 0.58 to 0.99 | R moves 0.384 to 0.652 |
| **rho, across 14 DWS vintages** | **0.49 to 0.74** | **R moves 0.421 to 0.636, a span of 0.215** |
| Required R at tau_k = 0.10 | | 0.608 to 0.686 |

**A swing of 0.215 in R is decisive near tau_k = 0.10**, because the required R there is
0.608 to 0.686 and the observed R is 0.568. The 2000 vintage, R = 0.636, clears the bar in
the tau_l = 0.255 cell; the 2010 vintage, R = 0.421, misses it by 0.19. The labour market
decided the answer in those two cells.

The correct statement, which replaces both A50's closing sentence and the original claim 30:

> The fiscal condition has two levers, R and tau_k. Away from tau_k = 0.10 the tax rate
> settles it on its own: at 0.21 the condition holds for any R the labour market has ever
> produced, and at 0.05 it fails for all of them. Near tau_k = 0.10, which is where the
> sourced estimates actually sit, the condition is decided by R, and R has moved by 0.215
> across the fourteen observed vintages. Both levers must be reported.

Claim 30 and claim 49 are amended accordingly in `notes/claims_register.md`.

---

## A53. WHICH tau_k. Decomposed, sourced, and the current tax code puts it BELOW the break-even level

`src/tau_k_decomposition.py`. tau_k has been carried as a bare grid of 0.05, 0.10 and 0.21
with no account of where those numbers come from or what would move them. Decomposed:

    tau_k(AI surplus) = sigma_rent * (domestic share * tau_statutory)
                        + (1 - sigma_rent) * tau_normal

**Why the split is the right one.** Under full expensing a business-level capital tax becomes
a cash-flow tax, which falls on rents and exempts the normal return. Auerbach (2017), NBER WP
23881, verified verbatim: "Hence, the cash-flow tax acts as a tax on pure profits, exempting
only the normal return from taxation." AMR show the same algebra: "with immediate expensing
(alpha_j = 1), we have tau_k,j passthrough,equity = 0".

### The sourced inputs, and where the project's own grid came from

| Input | Value | Source, verified verbatim |
|---|---|---|
| tau_normal | 0.05 post-2017, **0.10 in the 2010s**, 0.20 in 2000 | AMR (2020): "Effective capital taxes on software and equipment ... are much lower, 10 percent in the 2010s and 5 percent after the 2017 tax reforms, though they used to be about 20 percent in 2000" |
| tau_l = 0.255 | | AMR (2020): "we used an effective tax rate on labor of tau_l = 25.5 percent" |
| tau_statutory | 0.21 | US federal statutory corporate rate |
| Haven share, US affiliates | **0.48** | Torslov, Wier and Zucman: "48% of the pre-tax profit ... of majority-owned affiliates of US multinationals were made in tax havens" (2016) |
| Haven share, global | 0.40 | Same: "close to 40% of multinational profits are shifted to tax havens globally" |
| sigma_rent | **0.351** | Barkai (2020): pure profit share rises 13.5pp from near zero; capital share 25 percent of gross value added in 2014. Implied rent share of capital income 13.5/(25+13.5) |

**The 0.05, 0.10 and 0.21 grid this project has used all along is AMR's own series of
effective rates on software and equipment, plus the statutory rate.** That was never stated
and is now attributed.

### The implied tau_k, sourced rent share only

| Domestic share | tau_normal 0.05 (now) | tau_normal 0.10 (2010s) | tau_normal 0.20 (2000) |
|---|---|---|---|
| Closed economy, 1.00 | 0.1062 | 0.1386 | 0.2035 |
| Global shifting, 0.60 | 0.0767 | 0.1091 | 0.1740 |
| **US affiliate shifting, 0.52** | **0.0708** | 0.1032 | 0.1681 |
| Imported capital, 0.00 | 0.0324 | 0.0649 | 0.1298 |

Sourced-only range **0.032 to 0.204**; including scenario rent shares of 0.50 and 0.75,
0.013 to 0.208.

### The finding, and it is the sharpest thing in this session

At the observed R = 0.5683, the condition passes only if

| tau_l | tau_k needed |
|---|---|
| 0.255 | **0.1101** |
| 0.301 | 0.1299 |
| 0.318 | 0.1373 |

**Under the current tax code with profit shifting, tau_k is 0.0708. The condition fails.**
Under the 2010s code with the same shifting it was 0.1032, which also fails, narrowly. Only
the closed-economy cases at 2010s or 2000 rates clear the bar.

Two things follow and both are policy-relevant rather than merely descriptive:

1. **Profit shifting alone is enough to push tau_k below break-even.** Closed economy at the
   2010s rate gives 0.1386, comfortably above the 0.1101 needed. Applying the verified
   48 percent haven share drops it to 0.1032, below. The gap between passing and failing is
   roughly the size of the shifting adjustment.
2. **Raising the rent share does not rescue it under shifting.** At sigma_rent = 0.75 with
   shifting, tau_k is 0.1069, still short, because a larger rent share puts MORE of the
   surplus into the component that is being shifted. Rents only help in the closed economy.

Everything above sigma_rent = 0.351 is a scenario with no source and is labelled as such in
the output.

### The figure

`paper/figures/fig_R_tauk.png`. Break-even lines for the three tau_l values, with and
without outlays at g = 0.10; the fourteen DWS vintages plotted at tau_k = 0.10; the 2026
observation and the Huckfeldt switcher scenario; and vertical bands for the sourced and
scenario tau_k ranges. Points above a line satisfy the condition. Underlying table at
`data/processed/tau_k_decomposition.csv`.

---

## A54. DISPLACEMENT TO SLACK. Solved as a fixed point, and the suggested exit share is BOTH UNVERIFIED AND BACKWARDS

`src/displacement_to_slack.py`.

### The Acemoglu and Restrepo figure could not be verified and is not used

The brief proposed sourcing the labour-force exit share from Acemoglu and Restrepo's finding
that roughly three quarters of the nonemployment response was nonparticipation. **I
downloaded and searched the full NBER Working Paper 23285 text and it contains no such
decomposition.** The strings "nonparticipation", "not in the labor force", "leaving the
labor force" and "exit the labor force" do not appear anywhere in it; the unemployment and
participation results are stated to sit in Table A4 of an online appendix that is not in the
paper. It may be in the published version. This project has not seen it, so it is recorded
in `lit/unverified.md` and is not used.

### The DWS measures the same thing directly, on the right population

Exit share = NILF / (unemployed + NILF), read off Table 1 of ten releases.

| Survey | Employed | Unemployed | NILF | **Exit share** | Unemployment |
|---|---|---|---|---|---|
| 2008 | 67.1 | 18.0 | 15.0 | 0.455 | 5.0 |
| **2010** | 48.8 | 36.1 | 15.2 | **0.296** | **9.8** |
| 2012 | 56.0 | 26.7 | 17.4 | 0.395 | 8.3 |
| 2014 | 61.3 | 20.8 | 17.9 | 0.463 | 6.6 |
| 2016 | 65.5 | 15.9 | 18.6 | 0.539 | 4.8 |
| 2018 | 66.4 | 14.4 | 19.3 | 0.573 | 4.0 |
| 2020 | 70.1 | 12.4 | 17.5 | 0.585 | 3.6 |
| **2022** | 65.2 | 12.4 | 22.3 | **0.643** | 4.0 |
| 2024 | 65.7 | 16.1 | 18.2 | 0.531 | 3.7 |
| 2026 | 66.1 | 18.3 | 15.7 | 0.462 | 4.3 |

> **exit share = 0.7206 - 0.0419 x unemployment rate**, R-squared 0.777, n = 10

**It is nowhere near three quarters and it moves the wrong way for the suggested
assumption.** The exit share FALLS with slack: 0.64 in the tight market of January 2022, 0.30
in the slack market of January 2010. Displaced workers stay in the labour force and keep
searching when jobs are scarce.

That matters for the frontier in a direction that makes things worse, not better. A fixed
high exit share would have converted most displacement into quiet nonparticipation. The
measured behaviour converts it into measured unemployment, which feeds back through A49 into
a lower rho. **The feedback loop is stronger than the suggested assumption implied.**

### The fixed point

Baseline January 2026: labour force 170.5m, unemployed 7.4m, unemployment 4.32 percent.

| Displacement | Unemployment | rho, fitted | rho, floor at minimum observed | Outside the data? |
|---|---|---|---|---|
| 0% | 4.32 | 0.678 | 0.678 | no |
| 5% | 5.20 | 0.651 | 0.651 | no |
| **10%** | **6.47** | **0.612** | 0.612 | **no** |
| 25% | 17.25 | 0.284 | 0.511 | **YES** |
| 50% | 44.26 | 0.000 | 0.511 | **YES** |
| 75% | 69.62 | 0.000 | 0.511 | **YES** |
| 90% | 87.15 | 0.000 | 0.511 | **YES** |

**The honest boundary is around 14 to 15 percent displacement**, which is where implied
unemployment reaches 9.8 percent, the worst labour market in the fitted sample. Below it the
mapping is interpolation. Above it, the numbers in the table are arithmetic on an
extrapolated line and nothing more: a 50 percent displacement implying 44 percent
unemployment is not a forecast, and I will not present it as one. Beyond 9.8 percent the
frontier reports a BAND between a flat rho at the minimum ever observed and the extrapolated
line, labelled outside the data on the figure and in the text.

**At the 10 percent scenario the engine has been running, rho falls from 0.678 to 0.612**,
entirely inside the observed range. That is a credible, data-supported adjustment and it is
the one the rerun uses.

### One assumption stated rather than estimated

The comovement of omega with slack cannot be estimated: the pre-2026 releases do not publish
the Table 7 earnings distribution in a form this project has parsed. Omega is therefore held
constant across displacement levels. That is conservative in the direction that matters,
because Huckfeldt (2022) finds the cost and incidence of occupation displacement are higher
in recessions, so the true omega in slack states is lower than the one used and the frontier
below **understates** the deterioration.

## A55. CORRECTION. The Acemoglu and Restrepo nonparticipation split IS in the published article, and A54's non-verification was searching the wrong document

A54 recorded the three-quarters nonparticipation finding as unverified after searching NBER
Working Paper 23285 in full. **The owner was right and I was looking in the wrong version.**

- Confirmed in the published article, consulted as
  `data/raw/manual/AcemogluRestrepo2020_JPE_robots_and_jobs.pdf`.
- Location: **Section V.C, "Other Labor Market Outcomes", PDF page 34**, discussing
  **appendix table A15**.
- Finding, in this project's words: robot exposure raises both the nonparticipation rate and
  the unemployment rate, and the estimates imply that of the additional nonemployed, about
  three quarters leave the labour force and about one quarter remain unemployed. The same
  section reports increased take-up of Social Security retirement and disability benefits and
  other transfers (table A17), consistent with the participation margin doing the work.
- The passage is absent from the working paper. The earlier non-verification was accurate
  about the document searched and wrong about the claim. Removed from `lit/unverified.md`,
  recorded in the new `lit/verified_findings.md`, added to `paper/references.bib`.

### The two exit measures are different horizons and are now used as such

| Measure | Horizon | Value | Depends on slack? |
|---|---|---|---|
| **DWS exit share** | within three years of displacement | 0.296 to 0.643 | **yes**, falls with slack |
| **Acemoglu and Restrepo** | long differences 1990 to 2007, fourteen-year equivalent | about 0.75 | not estimated |

These are not rival estimates of one number and neither is "the" exit rate. The DWS measures
who has left the labour force within three years; Acemoglu and Restrepo measure where
displaced workers settle over a decade or more. **They are consistent with each other**: an
exit share around 0.46 at three years rising toward 0.75 over fourteen is a plausible single
path, and the gap between them is the drift of long-term unemployed into nonparticipation.

Both are carried as variants throughout, with the horizon named. A higher exit share LOWERS
measured unemployment and RAISES the drop in participation, so the long-run variant is
optimistic for the unemployment path and pessimistic for the tax base. Neither is uniformly
the conservative choice, which is why both are reported.

---

## A56. THE SPEED LIMIT. A dynamic model replaces the static fixed point, and the static version OVERSTATED the damage

`src/unemployment_stock_flow.py`. A54 displaced d percent of employment instantaneously and
read off the implied unemployment. That is the wrong object for an adoption path, which
arrives as a flow. The minimal stock-flow replacement is stated in full in the module
docstring.

### Calibration, and the one conversion that carries the most weight

The DWS reports status at a survey date for workers displaced over a three-year window.
Taking displacement as uniform, mean elapsed time is T = 1.5 years. Splitting the survey
shares into two competing risks and treating each as a constant annual hazard:

    h(u) = 1 - (1 - rho_cond)**(1/T),  rho_cond = rho / (rho + (1-rho)(1-e))
    a(u) = 1 - (1 - (1-rho)e)**(1/T)

At the January 2026 baseline: **h = 0.681, a = 0.120 per year.** T is varied over 1.0, 1.5
and 2.0 years and that variation is the single largest modelling choice in the file; the
speed limit moves by a factor of 1.7 across it.

Observed baseline displacement flow, DWS long-tenured: **0.679 percent of employment a
year**. A residual inflow of **2.94 percent a year** is calibrated once so the model
reproduces the observed 4.32 percent unemployment at that baseline. It is a reduced-form
residual standing for quits, short-tenure layoffs and entrants, and it is not a measured
separation rate.

### Steady-state unemployment by annual displacement flow

| d, percent a year | Short-run exit (DWS) | Long-run exit (0.75) |
|---|---|---|
| 0.5 | 4.07 | 4.15 |
| 1.0 | 4.79 | 4.64 |
| 2.0 | **6.47** | 5.60 |
| 3.0 | **9.00** | 6.55 |
| 4.0 | 11.97 | 7.49 |
| 5.0 | 15.00 | 8.42 |

Terminal values at 10 and 20 years are within 0.2 to 1.8 points of the steady state at every
d, because the hazards clear the stock quickly (h + a is about 0.8 a year). **The horizon
barely matters once the annual flow is fixed; the annual flow is the whole story.**

### The speed limits

| T | Exit variant | Max d keeping u inside the observed range (9.8 percent) |
|---|---|---|
| 1.0y | short run | 4.35% a year |
| **1.5y central** | **short run** | **3.15% a year** |
| 2.0y | short run | 2.50% a year |
| 1.0y | long run | 8.30% a year |
| 1.5y | long run | 6.50% a year |
| 2.0y | long run | 5.35% a year |

**"Bounded at all" is not a binding constraint in this model and I am reporting that rather
than a number.** Because labour force exit continues even when the reemployment hazard goes
to zero, the unemployment stock always drains eventually. The scan reached the top of its
grid at 12 percent a year without finding an unbounded case. The limit that matters is the
first column: the flow at which the model leaves the range where its own hazards were fitted.

### Named adoption scenarios, central case

| Scenario | Annual flow | Terminal u | Terminal rho | Inside the data? |
|---|---|---|---|---|
| 10% over 20y | 0.50% | 4.10 | 0.684 | yes |
| **10% over 10y** | **1.00%** | **4.84** | **0.662** | **yes** |
| 25% over 20y | 1.25% | 5.23 | 0.650 | yes |
| 25% over 10y | 2.50% | 7.70 | 0.575 | yes |
| 50% over 20y | 2.50% | 7.72 | 0.574 | yes |
| 50% over 10y | 5.00% | 15.66 | 0.340 | **no** |
| 75% over 20y | 3.75% | 11.78 | 0.451 | **no** |
| 75% over 10y | 7.50% | 35.64 | 0.000 | **no** |
| 90% over 20y | 4.50% | 14.27 | 0.375 | **no** |
| 90% over 10y | 9.00% | 43.71 | 0.000 | **no** |

### What this does to the thesis, and it weakens it further

**The static fixed point overstated the slack response at the scenario the engine has been
running.** A54 put 10 percent displacement at 6.47 percent unemployment with rho falling to
0.612. Spread over ten years as a flow, the same 10 percent gives **4.84 percent unemployment
and rho 0.662**, barely distinguishable from the 4.32 percent baseline. A54's figure treated
a decade of adoption as a single instant.

**Half of all US employment can be displaced over twenty years without leaving the observed
labour market range.** 50 percent over 20 years is a 2.5 percent annual flow and lands at 7.7
percent unemployment, inside the range the DWS relationships were fitted on. That is a
striking result and it runs directly against a disruption thesis: on these relationships, the
economy absorbs very large cumulative displacement provided it arrives slowly enough.

**The binding variable is speed, not size.** 50 percent over 20 years (u = 7.7) and 25
percent over 10 years (u = 7.7) are the same outcome because they are the same annual flow.
The paper's scenarios must be stated as annual flows, and any scenario quoted as a
cumulative percentage without a horizon is uninterpretable.

**Where it breaks is above about 3 percent a year**, which is roughly four and a half times
the observed long-tenured displacement rate. Above that the model leaves the range where its
hazards were estimated, and the 35 and 44 percent unemployment figures in the table are
arithmetic on extrapolated relationships, not forecasts.

## A57. tau_k SECOND PASS. Both unknowns now have a verified alternative pointing the other way, and one of them is not a range but a disagreement

`src/tau_k_second_pass.py`. A53 rested each unknown on a single source. Both now have a
second.

### The rent share is not a range, it is two incompatible readings of one residual

| Reading | sigma_rent | Source |
|---|---|---|
| Economic profits | **0.351** | Barkai (2020), JF 75(5). Pure profit share up 13.5pp from near zero; capital share 25 percent of gross value added in 2014 |
| Rental-rate mismeasurement | **~0.00** | Karabarbounis and Neiman (2019), NBER Macroeconomics Annual 33, 167 to 228 |

Karabarbounis and Neiman analyse the same accounting residual and label the profits reading
Case Pi. Verified: they are "skeptical of Case Pi", finding it "reveals a tight negative
relationship between real interest rates and economic profits", produces "large fluctuations
in inferred factor-augmenting technologies", and implies profits "remain lower today than in
the 1960s and 1970s". They "view Case R as most promising", Case R attributing the residual
to deviations of the rental rate of capital. **Under Case R the rent share of capital income
is approximately zero**, because what Barkai reads as profit is read as mismeasured cost of
capital.

**These are not endpoints of a confidence interval and must not be averaged.** They are two
credible readings of the same data that disagree about whether the object exists. The paper
has to carry both and say which results depend on which.

### The domestically taxed share: two sources, and they disagree by 20 points

| Source | Implied domestic share | Basis |
|---|---|---|
| Torslov, Wier and Zucman | **0.52** | 48 percent of pre-tax profits of majority-owned FOREIGN AFFILIATES of US multinationals made in tax havens, 2016. **Confirmed to be the US-multinational figure, not the global one** |
| Clausing (2016) | **0.712 to 0.781** | 77 to 111bn USD of US corporate revenue lost to shifting by 2012, against 274.7bn USD of federal corporate receipts in 2012Q4 |

The Clausing conversion is a derivation of this project, not a figure Clausing reports:
domestic share = receipts / (receipts + loss). The two measure different objects, TWZ a
profit share of foreign affiliates and Clausing a revenue loss against actual receipts, and
the gap between them is interpretation, not sampling error.

### tau_k on AI surplus, sourced rent shares only (0.00 to 0.351)

| Domestic share | tau_normal 0.05 (now) | 0.10 (2010s) | 0.20 (2000) |
|---|---|---|---|
| Imported capital, 0.00 | 0.032 to 0.050 | 0.065 to 0.100 | 0.130 to 0.200 |
| TWZ, 0.52 | **0.050 to 0.071** | 0.100 to 0.103 | 0.168 to 0.200 |
| Clausing, 0.71 to 0.78 | 0.050 to 0.090 | 0.100 to 0.123 | 0.182 to 0.200 |
| Closed economy, 1.00 | 0.050 to **0.106** | 0.100 to **0.139** | 0.200 to 0.204 |

Full sourced range **0.032 to 0.204**.

### Required tau_k at R = 0.5683, at EVERY labour tax rate

| tau_l | Required tau_k | Cells passing, of 30 |
|---|---|---|
| 0.255 (AMR) | **0.1101** | 13 |
| 0.301 | **0.1299** | 10 |
| 0.318 | **0.1373** | 10 |

**Every passing cell sits in the year-2000 tau_normal column**, plus one half-cell at
closed-economy 2010s rates. **Not a single post-2017 cell passes at any labour tax rate,
under any rent share, under any shifting assumption, including the closed economy.** The
highest post-TCJA value obtainable is 0.1062, from the closed economy with the Barkai rent
share, and the lowest requirement is 0.1101.

That is the most robust statement this project has about the fiscal condition, and it does
not depend on which side of the Barkai against Karabarbounis and Neiman disagreement one
takes.

---

## A58. THE TRAJECTORY. The US crossed from met to unmet somewhere between 2008 and 2022, and the date is NOT robust

`src/tau_k_second_pass.py`, figure at `paper/figures/fig_trajectory_R_tauk.png`.

Each DWS vintage is assigned its observed R and the tax regime in force that year: AMR's own
tau_normal series interpolated between the anchors it states (0.20 in 2000, 0.10 through the
2010s, 0.05 from 2018), the statutory rate (0.35 through 2017, 0.21 from 2018), and the
shifting share **held constant**, because no verified time series of the US haven share was
obtained. The path's horizontal movement is therefore driven by expensing and statutory
changes only, and that is a limitation rather than a finding.

### The path, Barkai rent share with TWZ shifting

| Year | rho | R | tau_normal | tau_stat | tau_k | Met at 0.255 | Met at 0.301 |
|---|---|---|---|---|---|---|---|
| 2000 | 0.740 | 0.636 | 0.20 | 0.35 | **0.194** | yes | yes |
| 2004 | 0.650 | 0.559 | 0.16 | 0.35 | 0.168 | yes | yes |
| 2008 | 0.680 | 0.585 | 0.12 | 0.35 | 0.142 | yes | yes |
| **2010** | **0.490** | **0.421** | 0.10 | 0.35 | 0.129 | **no** | **no** |
| 2014 | 0.610 | 0.525 | 0.10 | 0.35 | 0.129 | yes | no |
| 2016 | 0.660 | 0.568 | 0.10 | 0.35 | 0.129 | yes | no |
| **2018** | 0.660 | 0.568 | **0.05** | **0.21** | **0.071** | **no** | no |
| 2026 | 0.661 | 0.568 | 0.05 | 0.21 | 0.071 | no | no |

### Both levers are visible in the path, which settles A52

**2010 is a labour market failure.** tau_k is unchanged at 0.129; R collapses from 0.585 to
0.421 because the reemployment rate fell to 0.49. The condition fails on R alone and
recovers by 2014 as R recovers.

**2018 is a tax failure.** R is unchanged at 0.568; tau_k falls from 0.129 to 0.071 as
expensing and the statutory cut take effect together, a 45 percent cut. The condition fails
on tau_k alone and does not recover, because R has not been above 0.64 since 2000.

That is the concrete vindication of A52's reframing: each lever has independently decided the
answer once in the observed record.

### The crossing date, and its robustness

| Rent share | Shifting | tau_l 0.255 | tau_l 0.301 | tau_l 0.318 |
|---|---|---|---|---|
| Barkai 0.351 | Closed | 2022 | 2018 | 2018 |
| Barkai 0.351 | TWZ 0.52 | 2018 | 2010 | 2010 |
| KN Case R 0.00 | Closed | 2010 | 2008 | 2008 |
| KN Case R 0.00 | TWZ 0.52 | 2010 | 2008 | 2008 |

**The crossing date spans 2008 to 2022 and is not robust.** Anyone quoting a single year for
when the US fiscal condition on automation stopped holding is quoting their choice of rent
share and labour tax rate, not a measurement. The paper must give the range or give none.

**What IS robust across all twelve combinations: the condition is unmet in 2026, and has
been unmet continuously since 2018 in every one of them.** The disagreement is entirely
about how long before 2018 it had already failed.

## A59. AMENDMENT D. The 2026 depreciation regime verified against the statute, and AMR's 0.05 is retained for a reason

`src/tau_k_margins.py`, `data/processed/current_law_168k.json`. Read from the current text of
**26 U.S.C. 168(k)** on 2026-09-19.

- **168(k)(1)(A)** provides a first-year allowance equal to **one hundred percent** of the
  adjusted basis of qualified property.
- **168(k)(6)**, the phase-down schedule that stepped the allowance through 80, 60, 40 and 20
  percent, is shown as **REPEALED by Pub. L. 119-21, title VII, section 70301(b)(1)(B),
  July 4, 2025, 139 Stat. 189**. Paragraph (8) is repealed by the same provision.
- **168(k)(2)(A)(i)** defines qualified property to include property with a recovery period
  of 20 years or less and computer software under 167(f)(1)(B), which is exactly the
  equipment-and-software category AMR measure.

**Full immediate expensing is in force in 2026 and the phase-down is gone from the statute.**
The regime that produced AMR's post-2017 effective rate of 0.05 lapsed during the phase-down
years and was restored in July 2025. AMR's 0.05 is therefore the RIGHT value for the 2026
point, and it is retained for that reason rather than by default.

**Where this bites, stated rather than smoothed over:** the 2024 DWS vintage sits inside the
phase-down window, when the allowance was 60 percent. A partial allowance raises the
effective rate on the normal return above 0.05, toward the 2010s value of 0.10. This project
has no measured effective rate for the phase-down years and will not interpolate one, so the
2024 point retains 0.05 and carries the flag. It changes no conclusion: the 2024 point fails
the condition at 0.05 and would fail by less at a higher rate, and the 2026 point, which
carries the conclusions, is on solid ground.

---

## A60. AMENDMENT C. Margins on the post-2017 result. One cell is within 0.004 of flipping, and it needs a labour market slightly better than today's

`data/processed/tau_k_margins_post2017.csv`. Margin = available tau_k minus required tau_k.

| Outlays g | Cells passing, of 30 | Best margin |
|---|---|---|
| 0.00 | **0 of 30** | **-0.0039** |
| 0.10 | 0 of 30 | -0.0378 |
| 0.25 | 0 of 30 | -0.0887 |

**Exactly one cell is within 0.01 of flipping:** Barkai rent share, closed economy, tau_l =
0.255, margin **-0.0039**. It requires all three of the most favourable sourced assumptions
at once: the economic-profits reading of the residual, no profit shifting at all, and the
lowest of the three labour tax rates.

What would flip it: **R = 0.5837, which is rho = 0.679** at the counterfactual omega. Today's
rho is 0.661 and the highest ever observed across fourteen vintages is 0.740, so that cell is
**attainable**. Every other cell needs rho of 0.75 or above, which has never been observed.

| Cell | R needed | rho needed | Attainable? |
|---|---|---|---|
| Barkai, closed, tau_l 0.255 | 0.5837 | **0.679** | **yes** |
| Barkai, Clausing-high, tau_l 0.255 | 0.6470 | 0.752 | never observed |
| Barkai, closed, tau_l 0.301 | 0.6473 | 0.753 | never observed |
| Barkai, closed, tau_l 0.318 | 0.6662 | 0.775 | never observed |

**With any outlay response at all the knife edge disappears**: at g = 0.10 the best margin is
-0.0378 and nothing is close.

---

## A61. AMENDMENT A. The destination pool. A56's speed limit is an UPPER BOUND, and a cumulative CEILING appears that A56 said did not exist

`src/destination_pool.py`. A56's rho(u) was estimated on cyclical variation, where the jobs
displaced workers return to still exist. Sustained technological displacement shrinks the
destination pool. The amendment:

    h_eff(t) = h(u_t) * max(0, 1 - phi * D(t))

phi = 0 is A56 exactly and **assumes new work is created at the historical rate
indefinitely.** Occupation-to-occupation transition matrices were not obtained from a
verifiable public source in this session, so phi is run over {0, 0.5, 1} plus a per-construct
ANCHOR equal to the exposed group's employment share, which is a LOWER bound on phi because
displaced workers move to nearby occupations and nearby occupations are more alike in
exposure than a random draw.

Exposed shares: embodied 20.1 percent, cognitive AIOE 13.2, cognitive GPT 15.4, both 33.4.

### Speed limit, percent of employment a year

| Horizon | phi = 0 | phi = 0.5 | phi = 1 | anchor (both) |
|---|---|---|---|---|
| 2y | 4.50 | 4.45 | 4.35 | 4.45 |
| 5y | 3.40 | 3.20 | 3.05 | 3.25 |
| 10y | **3.15** | 2.70 | 2.40 | 2.85 |
| 20y | 3.05 | 2.25 | **1.80** | 2.50 |

**A56's 3.15 percent is the phi = 0, ten-year corner of this table.** At phi = 1 over twenty
years the limit is **1.80 percent**, a 41 percent reduction. The limit is a decreasing
function of horizon once phi exceeds zero, which is the signature of the pool effect: the
longer the path, the more of the destination pool has already gone.

### The cumulative ceiling, which corrects A56

| Horizon | phi = 0 | phi = 0.5 | phi = 1 |
|---|---|---|---|
| 10y | 31.5% | 27.0% | 24.0% |
| 20y | **61.0%** | 45.0% | **36.0%** |

**A56 concluded that speed binds and size does not. That is true only at phi = 0.** Once the
destination pool shrinks, maximum cumulative displacement inside the observed labour market
range is capped at **36 to 61 percent** regardless of how slowly it arrives. Claim 61 is
amended: speed binds at phi = 0, and both speed and size bind for any phi above zero.

---

## A62. THE FRONTIER. Two failure modes, and they have nothing in common

`src/frontier.py`, `data/processed/frontier_grid.csv`. Four types by six levels of the
exposed wage bill by four horizons by three phi values.

### Speed-driven failure: terminal unemployment, phi = 0.5

| Type | Level of exposed | 2y | 5y | 10y | 20y |
|---|---|---|---|---|---|
| Embodied | 50% | **10.72** | 6.77 | 5.06 | 4.30 |
| Embodied | 90% | **17.14** | **10.98** | 6.77 | 5.11 |
| Cognitive AIOE | 90% | **12.27** | 7.58 | 5.42 | 4.48 |
| Both | 50% | **8.04**... | | | |
| Both | 90% | **15.01 flow** | | | |

**Displacing ninety percent of the exposed embodied wage bill over twenty years raises
unemployment to 5.11 percent.** The baseline is 4.32. Everything at ten and twenty year
horizons is inside the observed data range for every type and every level. Only the two and
some five year scenarios leave it.

### Feasibility, and it settles which scenarios can be embodied

Embodied annual flow caps from capital formation (`src/feasibility_bounds.py`), equipment
investment 1,864.8bn USD a year against average compensation of 101,991 USD:

| Cap | Annual flow |
|---|---|
| Tight: 10 percent of equipment investment is automation capital, capex 2x annual wage | **0.498%** |
| Loose: ALL equipment investment, capex 1x annual wage | 9.955% |

| Level of exposed | 2y | 5y | 10y | 20y |
|---|---|---|---|---|
| 25% | no | no | no | **yes** |
| 50% | no | no | no | **no** |
| 90% | no | no | no | **no** |

**Under the tight cap, displacing half the exposed embodied wage bill is physically
unattainable at any horizon**, because it needs more automation capital per year than plausibly
exists. **Every fast scenario in this frontier is therefore cognitive-led by construction**,
which is what the owner predicted and is now sourced rather than assumed. Cognitive
displacement carries no capacity cap here, and that absence is an assumption about deployment
speed, not a measurement.

ACES robotic equipment capital expenditure could NOT be extracted from the 2022 tables in
this session and IFR World Robotics is paid. The caps above rest on equipment investment
aggregates only.

### Size-driven failure: it fails everywhere, including at zero displacement

Terminal R with switcher compounding, against a break-even of **0.722 to 0.777** at the
post-2017 tau_k of 0.0708:

| Type | Level | 2y | 5y | 10y | 20y |
|---|---|---|---|---|---|
| Cognitive AIOE | 5% | 0.593 | 0.601 | 0.604 | 0.605 |
| Embodied | 90% | 0.247 | 0.408 | 0.518 | 0.562 |
| Both | 90% | **0.000** | 0.233 | 0.410 | 0.523 |

**Not one cell reaches break-even, including the mildest scenario in the grid.** That is not
a displacement result. It is A57 and A58 restated: the condition already fails in 2026 at
zero AI displacement, so every scenario inherits the failure and displacement only deepens
it. The prereg note flagged this as nearly tautological before the run and it is.

Wage compounding matters at speed: at 90 percent of both exposure types over two years the
average worker is displaced more than once and R collapses to zero under the switcher omega.

### Nonlinearity: REFUTED. There is no threshold

Quadratic fits of terminal unemployment on the annual flow, R-squared 0.95 to 0.997:

| Type | phi | Curvature | Slope at lowest flow | Slope at highest flow | **Acceleration ratio** |
|---|---|---|---|---|---|
| Embodied | 0.0 | -0.025 | 1.712 | 1.269 | **0.742** |
| Embodied | 1.0 | -0.056 | 1.995 | 0.987 | **0.494** |
| Cognitive AIOE | 0.0 | -0.004 | 1.475 | 1.429 | **0.969** |
| Both | 1.0 | -0.059 | 2.378 | 0.606 | **0.255** |

**Curvature is negative in every one of the twelve cells and the acceleration ratio is below
one everywhere.** The marginal effect of displacement on unemployment DECELERATES. There is
no tipping point, no threshold and no runaway in this channel within the modelled range.

The mechanism is mundane: as unemployment rises the exit hazard drains the stock and the
labour force shrinks, so measured unemployment rises less than proportionally. **A thesis
that needs a threshold in the household or unemployment channel does not have one here.** The
nonlinearity, if the paper has one, has to come from the balance-sheet side, which is what
the order-of-stress work is for.

## A63. THE CIRCULARITY WAS REAL. Correcting it reverses the nonlinearity result and cuts the speed limit by a factor of two and a half

`src/slack_reestimate.py`, `src/stock_flow_v2.py`. The owner identified a defect in A56, A61
and A62 and it is confirmed.

### The defect

The stock-flow model let unemployed workers exit to nonparticipation, which removes them from
BOTH the numerator and the denominator of the unemployment rate. The reemployment hazard was
then driven by that same suppressed unemployment rate through `rho = 0.8090 - 0.0304 u`, so
the model was rewarded for the exits: exits suppress u, suppressed u raises rho, higher rho
drains the stock faster, which suppresses u further. **A56's speed limit, A61's cumulative
ceiling and A62's unemployment paths were all too generous.**

Exit to nonparticipation is also not a benign outcome. A displaced worker who stops looking
has lost their wage income as completely as one counted unemployed.

### The repair, and the measure it settles on

Three slack measures fitted on the same fourteen DWS vintages:

| Measure | Fit | R-squared | t |
|---|---|---|---|
| Unemployment rate (original, circular) | rho = 0.8090 - 0.0304 u | 0.812 | -7.20 |
| Nonemployment 16 and over | rho = 1.5597 - 0.0233 x | 0.540 | -3.76 |
| **Prime-age nonemployment, 25 to 54** | **rho = 1.2280 - 0.0275 x** | **0.773** | **-6.40** |

The 16-and-over measure is rejected twice over: it fits worst, and it falls secularly with
population ageing, so it conflates demographics with slack and its observed range at the
vintage dates is about one point wide, which makes any speed limit computed against it
degenerate. **Prime-age nonemployment strips the demographic trend, has a 6.4 point observed
range (18.27 to 24.71) and fits nearly as well as the circular original.** It is also the
better match to the population being modelled, since DWS displaced workers are long-tenured
and overwhelmingly prime-age.

### A second casualty: the exit share does not actually depend on slack

A54 fitted exit share on the unemployment rate at R-squared 0.777 and I reported it as a
finding. **Re-fitted on nonemployment it is R-squared 0.137, t = -1.13, not significant.**
The original fit was partly mechanical: exit share is NILF over (U plus NILF) and the
unemployment rate is U over (U plus E), so both move with U by construction. Regressing one
on the other is partly regressing a ratio on its own component. **Claim 57 is downgraded.**
The exit share is held at the 2026 value of 0.462 with the observed range 0.296 to 0.643 as
sensitivity.

### Result 1: the speed limit is two and a half times tighter

Baseline prime-age nonemployment 19.31 percent against a sample maximum of 24.71.

| Horizon | phi = 0 | phi = 0.5 | phi = 1 | A56 and A61 reported |
|---|---|---|---|---|
| 2y | 4.80 | 4.75 | 4.65 | 4.50 |
| 5y | 2.75 | 2.60 | 2.50 | 3.40 |
| **10y** | **1.25** | **1.15** | **1.10** | **3.15** |
| 20y | breached at every grid value | | | 3.05 |

### Result 2: the cumulative ceiling is four to five times lower

| Horizon | phi = 0 | phi = 0.5 | phi = 1 | A61 reported |
|---|---|---|---|---|
| 2y | 9.6% | 9.5% | 9.3% | 9.0% |
| 5y | 13.8% | 13.0% | 12.5% | 17.0% |
| 10y | **12.5%** | 11.5% | **11.0%** | **31.5%** |

A61 put the twenty-year ceiling at 36 to 61 percent of employment. **Corrected, no
twenty-year path stays inside the observed range at any displacement flow in the grid**, and
the ten-year ceiling is 11 to 12.5 percent.

### Result 3, and it reverses last session's headline: THE THRESHOLD IS REAL

Quadratic fits at the ten-year horizon, R-squared 0.999 or better:

| phi | Metric | Curvature | **Acceleration ratio** | A62 reported |
|---|---|---|---|---|
| 0.0 | Prime-age E/P drop | +0.335 | **2.33** | not measured |
| 0.5 | Prime-age E/P drop | +0.425 | **2.54** | not measured |
| 1.0 | Prime-age E/P drop | +0.503 | **2.63** | not measured |
| 0.0 | Wage income | -0.003 | **1.75** | not measured |
| 1.0 | Wage income | -0.005 | **2.03** | not measured |
| 0.0 | Unemployment | +0.185 | **2.39** | **0.742** |
| 1.0 | Unemployment | +0.280 | **2.55** | **0.494** |

**A62 reported curvature negative in all twelve cells, acceleration ratios of 0.255 to 0.969,
and concluded there is no tipping point. That result is WITHDRAWN.** It was an artifact of
the circular hazard, which flattened the paths precisely where they should have steepened.
On the corrected model the marginal harm **more than doubles** between the lowest and highest
flows, on every outcome measure and at every phi.

Claim 75 moves from REFUTED back to supported, in a stronger form than originally posed: the
acceleration is present on employment to population and on aggregate wage income, not only on
unemployment.

### The consistency check now behaves, with one honest caveat

Realised reemployment share minus the rho implied by the model's own slack runs +0.01 to
+0.59, against gaps above +4 in the uncorrected model. The residual positive gap is a
path-average artifact: the realised share is cumulative over the whole path, including early
years when slack was still low, while the implied rho is the terminal value. It is largest
where implied rho has been clipped at zero. It is not the original defect and it is recorded
rather than removed.

### Release artifacts regenerated

`data/release/scenarios/` at version 0.3.0 and `data/release/dashboard/`, per the standing
requirements. **A pooled regime count is worth flagging: of 120 scenario paths, 58 are SLOW
and 62 are SUDDEN, and NONE are FAST.** On the corrected slack measure the speed limit and
the edge of the observed data nearly coincide, so the middle regime is almost empty. The
three-regime structure survives, but the FAST band is much narrower than the SLOW and SUDDEN
ones and the paper should say so rather than implying three equally populated cases.

## A64. ATTRITION ABSORPTION IS EXACTLY NEUTRAL FOR AGGREGATE EMPLOYMENT. It only moves the burden onto people who never appear in a displacement statistic

`src/separations.py`, `src/stock_flow_v3.py`.

### The sourced rates, and they are better than expected

BLS Employment Projections, "Occupational separations and openings", 2025 National Employment
Matrix, projections 2025 to 2035, read from bls.gov 2026-09-19. It publishes annual average
rates per occupation, which gives all three of item 1's inputs from one source. Joined to
this project's exposure groups through the existing OCCP-to-SOC crosswalk, covering 76.3
percent of employment.

| Group | Labour force exit | Occupational transfer | **Total separations** |
|---|---|---|---|
| All occupations | 3.86% | 5.21% | **9.07%** |
| Embodied top quintile | 3.85% | 5.65% | **9.49%** |
| Cognitive AIOE top quintile | 2.70% | 4.04% | **6.75%** |
| Cognitive GPT top quintile | 3.56% | 4.58% | **8.16%** |

BLS's own economy-wide total row: exit 4.20, transfer 5.50, separations 9.70 percent.

### The comparison the brief asked for

| | Annual rate | Multiple of the A63 speed limit (1.15% at 10 years) |
|---|---|---|
| Speed limit | 1.15% | 1.0 |
| **Labour force exit rate** | **3.86%** | **3.4x** |
| **Total separations rate** | **9.07%** | **7.9x** |

**The economy vacates positions three to eight times faster than the speed limit.** On the
face of it that looks like ample room to absorb displacement without layoffs. It is not, and
the reason is the finding.

### The result: neutral on every aggregate, decisive on composition

At a 2 percent annual flow over ten years, phi 0.5, aggregate ceiling:

| alpha | Share of destruction absorbed | Laid-off incumbents | **Lost entrant openings** | Prime-age E/P | Unemployment | Wage income |
|---|---|---|---|---|---|---|
| 0.00 | 0% | **19.05%** | **0.00%** | 72.50 | 6.75% | 0.858 |
| 0.25 | 48% | 9.85% | 9.20% | 72.50 | 6.75% | 0.859 |
| 0.50 | 97% | 0.65% | 18.40% | 72.50 | 6.75% | 0.859 |
| 1.00 | 100% | **0.00%** | **19.05%** | 72.50 | 6.75% | 0.859 |

**Employment to population, unemployment and aggregate wage income are identical to four
significant figures across the whole range of alpha.** The speed limit is identical too:
4.75, 2.60 and 1.15 percent a year at 2, 5 and 10 year horizons, at every alpha and on both
ceilings.

Attrition absorption does not reduce the employment loss. It transfers the entire burden from
displaced incumbents to people who would have been hired and were not.

**I had this wrong on the first run of this module and the error is worth recording.** I let
the unfilled position simply remove a worker from employment, without putting the
would-be entrant into the searching pool. That made attrition look as though it destroyed
employment permanently while layoffs did not, which is backwards, and it produced a spurious
result in which attrition TIGHTENED the speed limit from 1.15 to 0.35 percent. The symmetric
treatment (the entrant enters unemployment and searches at the same hazard) gives the neutral
result above.

### Why this matters more than the neutrality suggests

**The measurement system goes blind exactly where absorption is highest.** The reemployment
relationship this whole model rests on, rho(slack), is estimated on the Displaced Worker
Survey, which surveys people who LOST a job they held for three or more years. A person who
never got hired is not in it. Neither are they in the displaced-worker share, the
reemployment rate, or any of the fourteen vintages.

So a labour market absorbing automation through attrition looks unchanged on the unemployment
rate, unchanged on the displaced-worker statistics, and unchanged on every indicator in this
project's own dashboard, while employment to population falls by the same amount as under
mass layoffs. For a supervisor that is the opposite of reassuring: it is the configuration in
which the standard indicators fail first.

### Item 1 questions answered directly

**Do 20-year paths now stay inside the observed range?** **No.** At every alpha from 0 to 1,
on both ceilings, at every displacement flow in the grid from 0.5 to 5 percent a year, and at
every phi, no 20-year path keeps peak prime-age nonemployment at or below the observed
maximum of 24.71 percent. Adding turnover and attrition does not rescue the long horizon.

**Early retirement variant.** Run at multipliers of 1.0, 1.5 and 2.0 on the exit hazard and
labelled SCENARIO throughout, because no rate for it is sourced. A65 records why that
labelling is now doubly justified.

---

## A65. THE SPECIFICATION TABLE. The speed limit is not a number, and the slack measure decides it

`src/specification_table.py`. 2,592 cells, 2,394 with a finite limit, crossing slack measure,
phi, exit treatment, hazard conversion T, attrition alpha, turnover and horizon.

### The range

| Statistic | Speed limit, percent a year | Cumulative ceiling, percent |
|---|---|---|
| Minimum | 0.05 | 0.5 |
| 25th percentile | 3.60 | 13.6 |
| **Median** | **6.60** | **25.1** |
| 75th percentile | 10.00 | 66.0 |
| Maximum | 10.00 (grid ceiling) | 200.0 |

Restricted to the prime-age nonemployment specification, which is the defensible one:
**speed limit 0.05 to 7.15 percent a year, median 2.73; cumulative ceiling 0.5 to 21.0
percent, median 13.4.**

### What moves it, ranked

| Dimension | Levels | Median speed limit, min to max | **Ratio** |
|---|---|---|---|
| **Slack measure** | 3 | 2.73 to 10.00 | **3.67** |
| Horizon | 4 | 4.65 to 6.78 | 1.46 |
| phi | 3 | 5.08 to 6.65 | 1.31 |
| Exit treatment | 4 | 5.15 to 6.65 | 1.29 |
| Hazard conversion T | 3 | 6.20 to 6.65 | 1.07 |
| Turnover | 2 | 6.60 to 6.65 | 1.01 |
| **Attrition alpha** | 3 | 6.60 to 6.60 | **1.00** |

**The choice of slack measure moves the answer more than every other modelling choice
combined, and attrition moves it exactly not at all.** Three sessions have quoted 3.15, then
1.25, then 1.15 percent a year. None of those movements was a measurement changing. All were
this one choice changing.

The 16-and-over nonemployment column is reported in the file but must NOT be quoted: the
model runs on prime-age stocks and pairing them with a 16-and-over threshold is incoherent,
which is why that column sits at the grid ceiling throughout.

### The structural point, which has to travel with every acceleration result

**In any model where the reemployment hazard falls with slack, the marginal harm of an extra
unit of displacement rises with the flow**, because the same inflow meets a lower outflow
rate. A63's acceleration result is therefore a property of the model class, not a discovery
about AI. What the data identify is the STRENGTH of that feedback, and they identify it only
inside the observed range of the slack measure. Outside that range the acceleration is an
extrapolation of a mechanism, not an estimate of one. The paper must say this in the same
paragraph as the acceleration ratios or it overclaims.

### Regimes redefined, and the release regenerated

The SLOW, FAST and SUDDEN split is retired. A63 found the middle band empty, and naming a
band after a quantity that moves by a factor of 140 across specifications implies a precision
the model does not have. Replaced by **INSIDE_DATA, BOUNDARY_BAND and OUTSIDE_DATA** on peak
prime-age nonemployment against the observed maximum of 24.71 percent, with the boundary band
being within one point of it. Of 480 published paths: 165 inside, 45 boundary, 270 outside.

`data/release/scenarios/` is at version 0.4.0 with the new dictionary, changelog and a
`specification_range.csv` carrying the whole table. The dashboard now quotes the speed limit
as a range and not a point.

---

## A66. LITERATURE AUDIT. Nothing links occupational AI exposure to household balance sheets, and one new paper contradicts Acemoglu and Restrepo

`lit/ai_exposure_household_finance_audit.md`. Searched 2026-09-19.

**No paper was located that measures occupational AI exposure against household
balance-sheet outcomes.** Exposure indices are mature and are used almost exclusively against
labour outcomes; household financial outcomes are measured richly and linked to generic
income shocks, not to occupational exposure. The nearest work reaches PUBLIC balance sheets.
This is stated as "none located" from a non-systematic search, not as "none exists".

### Two papers found, both verified by reading them

**Altindag, El Cheikh Taha, Nunley and Seals (July 2026), "Robots and the Public Finance of
Disability Insurance"**, arXiv 2607.02892. Robot exposure LOWERS SSDI applications by about
8 per 100,000 working-age residents per additional robot per 1,000 workers, largest among
those aged 55 to 64, worth roughly 3.4bn dollars a year in averted applications. Employment
to population does NOT fall in exposed commuting zones.

**This contradicts Acemoglu and Restrepo on two points and the project must stop leaning on
one of them.** A-R (2020) Section V.C find INCREASED take-up of Social Security retirement
and disability benefits in exposed areas, and employment-to-population ratios that DO fall.
The designs differ, applications against take-up, different instruments and periods, so it is
not a clean contradiction of one estimand. It is close enough that the A-R benefit-take-up
result cannot be treated as settled, which is why the early-retirement variant in A64 stays
a labelled SCENARIO with no sourced rate.

**Fan (2025), "The Labor Market Incidence of New Technologies"**, Yale job market paper,
arXiv 2504.04047. Worker mobility between occupations declines with distance in skill space;
automation and AI cluster within skill-adjacent occupations. Twenty to fifty percent of
labour demand shocks translate into wages against about thirty percent under standard models,
and **mobility recovers only about twenty percent of losses against about thirty percent
under standard estimates**.

**This is an independent, structural, estimated version of the destination-pool parameter
phi**, which this project imposed by assumption. Its headline implies the pool is about a
third less effective than a no-clustering model assumes, so **phi of about 0.33**, which sits
inside the grid already run and close to the employment-share anchors. It is the strongest
external support the phi mechanism has, and it should be cited wherever phi appears.

### How this project differs, stated for the paper

Existing work establishes that exposure moves LABOUR outcomes. It does not establish what
that does to household balance sheets, and it does not connect either to supervisory loss
measurement. **The contribution is the join, not the exposure measure and not the household
data, both of which are borrowed.**

## A67. THE CONVERSION LAYER. Sourced, and the benchmark scenario is milder on housing than the project has been assuming

`src/conversion_layer.py`, `data/processed/conversion_layer.json`. Every factor read from the
document itself, not from a summary.

### A. Federal Reserve 2026 Dodd-Frank Act stress test

Downloaded to `data/raw/manual/FRB_2026_DFAST_results.pdf`, 68 pages, published June 2026,
32 banks, nine quarters 2026:Q1 to 2028:Q1.

**Severely adverse scenario, Table 2:**

| Variable | 2026 | 2025, for comparison |
|---|---|---|
| Unemployment | **rises 5.5pp to 10.0%** | rises 5.9pp to 10.0% |
| Real GDP, peak to trough | -4.6% | -7.8% |
| **House prices** | **-30%** | -33% |
| **CRE prices** | **-39%** | -30% |
| Equity prices | -58% | -50% |

**Table 9, projected loss rates by loan category:**

| Loan type | Losses, USD bn | **Loss rate** | Range across banks |
|---|---|---|---|
| TOTAL | 624.9 | **6.9%** | 0.7 to 20.7 |
| **First-lien mortgages, domestic** | 22.5 | **1.5%** | |
| Junior liens and HELOCs | 5.5 | 3.2% | |
| Commercial and industrial | 158.2 | 9.0% | 3.4 to 48.5 |
| Commercial real estate | 76.5 | 8.8% | |
| **Credit cards** | 203.0 | **17.1%** | 9.5 to 22.7 |
| **Other consumer** (student AND auto together) | 54.1 | **7.3%** | |
| Other loans | 105.0 | 3.8% | |

**Capital:** aggregate CET1 falls from 12.8 percent (2025:Q4) to a minimum of **11.2
percent**, recovering to 12.7. Total losses absorbed about **708bn dollars**. All 32 banks
stay above their minimums.

**The first thing this does is discipline the project's own severity language.** A scenario
in which unemployment reaches 10 percent and house prices fall 30 percent produces a
**1.5 percent** loss rate on first-lien mortgages and a 1.6 percentage point fall in
aggregate CET1. That is the supervisory benchmark for "severely adverse", and every sudden
scenario this project produces must be expressed against it rather than described with
adjectives.

It also says where bank pain actually comes from: credit cards at 17.1 percent and C and I at
9.0 percent dwarf first-lien mortgages at 1.5. **A displacement story routed through
mortgages is routed through the most loss-resistant asset on the bank balance sheet.**

### B. Gerardi, Herkenhoff, Ohanian and Willen: the double trigger, quantified

`data/raw/manual/GHOW2018_cant_pay.pdf`, NBER Working Paper 21630, October 2015, published in
the Review of Financial Studies. Panel Study of Income Dynamics. Read directly.

| Factor | Value |
|---|---|
| Unemployed household head, effect on default probability | **+5 percentage points** |
| **BOTH head and spouse unemployed** | **more than +8 percentage points** |
| Job loss expressed as an equity equivalent | **a 35 percent decline in equity** |
| Unemployed share of the full sample | 5% |
| Unemployed share of defaulters | 20% |
| Defaulters who could pay without cutting consumption (strategic) | 38% |
| Defaulters who would have to go below subsistence to stay current | 30% |

Three things this settles that the project had been carrying as assumptions.

**The within-household correlation factor is superadditive and now has a number.** Both
earners unemployed gives more than 8 percentage points against 5 for one: **not 10**. The
sudden-shock module's correlated-displacement term is 8/5 = 1.6 times the single-earner
effect, not 2.

**The double trigger has an exchange rate.** Job loss is worth a 35 percent equity decline.
Against the Fed's 30 percent house price fall, a job loss is slightly MORE potent than the
entire severely adverse house price shock.

**Default is mostly not a liquidity failure.** Only 30 percent of defaulters would have to
drop below subsistence to stay current; 38 percent could pay without reducing consumption at
all. A model that converts income loss into default purely through a payment-affordability
threshold, which is what this project's DSTI engine does, is capturing at most a third of the
mechanism. That is a real limitation of A41 and it is recorded here rather than buried.

### C. New York Fed Household Debt and Credit, 2026:Q2

`data/raw/manual/NYFed_HHDC_2026Q2.pdf`, released August 2026. Total household debt **18.8
trillion**, mortgages 13.1 trillion, HELOC 459bn. **4.7 percent of outstanding debt in some
stage of delinquency**, down 0.1 points on the quarter. Transition into early delinquency
upticked slightly for auto loans and mortgages.

### D. Not obtained, named once

1. **Auto loan loss rate separately from student loans.** The Fed folds both into "Other
   consumer" at 7.3 percent. The order-of-stress table needs them apart, because the driving
   pathway sits in auto and the entrant incidence case sits in student loans. The exact
   documents: the FR Y-14M auto loan schedule aggregates; or the NY Fed companion data file
   behind chart 25 of the 2026:Q2 report; or a rating agency US auto loan ABS loss index.
2. **Agency multifamily debt service coverage standards.** Needed to set the materiality
   threshold for the landlord and multifamily lender sheet. The exact document: Fannie Mae
   Multifamily Selling and Servicing Guide, Part III underwriting, minimum DSCR table.
   `mfguide.fanniemae.com` is reachable; the table was not extracted this session.

---

## A68. THE ENTRY-LEVEL BLIND SPOT IS NOT HYPOTHETICAL. It is already measured, and it confirms the A64 mechanism

A64 argued that displacement delivered through attrition is invisible to the Displaced Worker
Survey and to every indicator in this project's dashboard. That was a deduction from the
model. **It is now an observation from someone else's data.**

**Brynjolfsson, Chandar and Chen (August 2026), "Canaries in the Coal Mine? Six Facts about
the Recent Employment Effects of Artificial Intelligence."** ADP administrative payroll
microdata covering millions of US workers through June 2026. Downloaded to
`data/raw/manual/Brynjolfsson_Canaries_Aug2026.pdf`, 140 pages, read directly.

Their six facts, in this project's words, with the ones that bear on A64 marked:

1. No evidence of widespread, economy-wide job displacement.
2. **Employment of workers aged 22 to 25 in AI-exposed occupations stands 19 percent below
   where it would be had it kept pace with less-exposed peers. Experienced workers show no
   comparable gap.**
3. The divergence has widened steadily since first documented in August 2025, when it was 13
   percent.
4. **It operates primarily through REDUCED HIRING of young workers rather than increased
   separations.**
5. Declines concentrate where AI usage substitutes for human tasks; where it complements,
   employment is flat or rising, especially for experienced workers.

**Fact 4 is the A64 mechanism, measured.** Fact 1 and fact 2 together are the blind spot: the
aggregate looks fine, and the harm is entirely in a group that a displaced-worker survey
cannot see because they were never displaced. They were never hired.

This is the strongest external validation any mechanism in this project has received, and it
arrives with an uncomfortable implication for the paper's framing: **the channel that is
already operating is the one the household stress engine measures worst.** The engine works
on households with mortgages and debt service; 22-to-25 year olds mostly do not have those.
Item 3's incidence work is therefore not a robustness check, it is the main event.

### Dashboard, five rows filled

`data/release/dashboard/` at version 0.5.0 now carries, with sources and dates:

| Indicator | Current value | Source |
|---|---|---|
| Recent college graduate unemployment | **5.6%** | NY Fed, 2026:Q2 |
| Recent college graduate underemployment | **42%** | NY Fed, 2026:Q2 |
| **Employment gap, ages 22 to 25 in AI-exposed occupations** | **19% below counterfactual, widening** | Brynjolfsson, Chandar and Chen, through June 2026 |
| Household debt in any delinquency | 4.7% | NY Fed HHDC 2026:Q2 |
| Aggregate CET1 under severely adverse | 12.8 to 11.2% minimum | Federal Reserve 2026 DFAST |

The auto-specific loss rate row stays empty, with the exact document named in A67.

**The entry-level indicators are the dashboard's most important rows and they were absent
until this session.** A trigger dashboard built on unemployment, displaced-worker
reemployment and household delinquency would currently read as benign while the measured
19 percent gap widens.

## A69. A1 INCIDENCE. The registered expectation is confirmed on mortgages and student debt and REFUTED on auto

`src/incidence_run.py`. Pre-registered in `notes/prereg_incidence.md` before running.

### The outcome measure changed, and A41 is downgraded because of it

Gerardi, Herkenhoff, Ohanian and Willen find that only 30 percent of defaulters would have to
drop below subsistence to stay current, and 38 percent could pay without cutting consumption
at all. **An affordability threshold therefore misses most defaults.** A41's DSTI crossings
are demoted to secondary throughout. The headline is now a default probability built from
their verified factors: **+5.0 percentage points for one displaced earner, more than +8.0 for
two, and job loss equivalent to a 35 percent equity decline.**

### The balance sheets, SIPP 2025, and they differ exactly where it matters

| Group | Households | With a mortgage | **With student debt** | With vehicle debt | In the double-trigger region |
|---|---|---|---|---|---|
| Incumbent working core, no 22 to 29 year old | 62.81m | **47.97%** | **21.13%** | 36.39% | 13.17% |
| Containing a 22 to 29 year old | 21.99m | **32.68%** | **35.60%** | 36.88% | 13.71% |

Balances, USD billions:

| Group | Mortgage | Student | Vehicle | Credit card |
|---|---|---|---|---|
| Incumbents | **7,160.1** | 740.1 | 553.5 | 317.2 |
| Young-adult households | **1,557.6** | 322.6 | 171.0 | 94.6 |

Young-adult households are a third less likely to hold a mortgage and **two thirds more
likely to hold student debt**. The double-trigger region, where a further 35 percent equity
decline would put the household underwater, is essentially the same share in both (13.2
against 13.7 percent), so the equity leg does not differ by age.

### Expected extra defaults and exposure at default, same total employment loss

Cognitive AIOE exposure, 10 percent of employment:

| Case | Households targeted | Mean default uplift | Extra defaults | **Mortgage** | **Student** | **Vehicle** | Card |
|---|---|---|---|---|---|---|---|
| (a) Incumbents | 14.78m | 0.70pp | 0.104m | **17.15bn** | **1.99bn** | **1.12bn** | 0.59bn |
| (b) Entrants | 3.46m | **3.17pp** | 0.110m | **11.72bn** | **2.73bn** | **1.35bn** | 0.74bn |
| (c) Sourced mix | 15.17m | 0.70pp | 0.106m | 17.36bn | 2.02bn | 1.17bn | 0.61bn |

Embodied exposure shows the same pattern with smaller mortgage exposure throughout
(9.23bn against 7.83bn), consistent with A44.

### Verdict on the registered expectation

The expectation was: **"attrition absorption leaves the fiscal loss unchanged, cuts mortgage
and auto stress sharply, and shifts stress to rent, student loans and delayed household
formation."**

- **Fiscal loss unchanged: CONFIRMED**, and by construction. A70 shows why.
- **Mortgage stress cut sharply: CONFIRMED.** Exposure at default falls 32 percent, from
  17.15bn to 11.72bn.
- **Shifted to student loans: CONFIRMED.** Exposure rises 37 percent, from 1.99bn to 2.73bn.
- **Auto stress cut sharply: REFUTED.** Vehicle exposure **RISES 21 percent**, from 1.12bn to
  1.35bn. Young-adult households hold vehicle debt at essentially the same rate as
  incumbents (36.9 against 36.4 percent), so concentrating the shock on them raises auto
  exposure rather than lowering it. Auto is not an incumbent asset the way mortgages are.

### The finding that neither case anticipated: concentration

The same total employment loss produces **almost the same number of extra defaults** (0.104m
against 0.110m) but at a **4.5 times higher default uplift per household** (0.70pp against
3.17pp), because it lands on a population a quarter the size. **The entrant channel cannot
absorb an economy-wide shock without hitting nearly half of all young-adult exposed
households**: the implied hit rate is 42.7 percent.

For external calibration, the observed entry gap is 19 percent (Brynjolfsson, Chandar and
Chen, through June 2026). The 10 percent economy-wide scenario modelled here is therefore
roughly **twice the intensity of what is currently measurable** in the entry-level channel.

### What this does to A64 and A65

A64 and A65 found attrition absorption exactly neutral for aggregate employment, unemployment,
wage income and the speed limit. **That neutrality survives and is now correctly labelled.**
It is an accounting property of symmetric treatment in a stock-flow model. On balance sheets
the two cases are not close: mortgage exposure differs by a third, student debt by more than
a third in the other direction, and the per-household intensity by a factor of four and a
half. **Aggregate neutrality and incidence neutrality are different claims and only the first
one holds.**

---

## A70. A2 FISCAL MAGNITUDES. Identical across incidence cases, and the disputed rent share moves the loss by 30 percent

`src/fiscal_magnitudes.py`. **No pass or fail language: A57, A58 and A60 established the
condition is unmet in 2026 at zero AI displacement, under every sourced combination. This is
a measurement of size, not a test.**

**Identical across the three incidence cases by construction, and worth stating rather than
discovering:** the fiscal loss depends on the displaced wage bill and the retained wage share.
A dollar of wage income not earned costs the same revenue whether the person was laid off or
never hired. A69 showed the incidence cases differ sharply in where credit losses land; here
they do not differ at all.

Denominators: federal current receipts and compensation of employees from FRED with units
read from the provider; OASDI payroll income 1,323.2bn and HI Part A revenue 462.4bn from A32.

### Annual revenue loss as a percent of federal receipts

tau_l 0.301, no outlays, Barkai reading, phi 0.5:

| Type | Level of exposed | 2y | 5y | 10y | 20y |
|---|---|---|---|---|---|
| Cognitive AIOE | 25% | 1.33 | 0.45 | 0.21 | 0.10 |
| Cognitive AIOE | 50% | 3.42 | 1.04 | 0.45 | 0.21 |
| Cognitive AIOE | 90% | 8.59 | 2.36 | 0.93 | 0.41 |
| Embodied | 50% | 6.49 | 1.83 | 0.75 | 0.34 |
| Embodied | 90% | 17.29 | 4.76 | 1.65 | 0.68 |
| **Both** | **90%** | **42.37** | **11.78** | **3.94** | **1.34** |

Range across the whole grid: **0.00 to 21.09 percent of federal receipts annually**;
cumulative loss 3bn to 2,523bn dollars.

**The horizon does almost all the work.** Ninety percent of both exposure types costs 42.4
percent of federal receipts a year if it arrives over two years and 1.34 percent if it
arrives over twenty. That is the fiscal counterpart of A56's speed result and it is a
thirty-fold difference for the same cumulative displacement.

### The rent-share disagreement moves the loss by about 30 percent

Annual loss, USD bn, 50 percent of exposed over 10 years, tau_l 0.301, no outlays:

| Type | Karabarbounis-Neiman reading | Barkai reading | Difference |
|---|---|---|---|
| Both | 25.0 | 19.3 | **+30%** |
| Cognitive AIOE | 8.2 | 6.0 | **+37%** |
| Embodied | 13.3 | 9.9 | **+34%** |

**The Karabarbounis-Neiman reading is the fiscally worse one**, because a rent share near
zero means a lower effective tax rate on AI surplus and therefore less offsetting capital
tax revenue. The disagreement A57 recorded as unresolvable is worth about a third of the
fiscal loss, which is larger than most of the parameter uncertainty elsewhere in the project.

### Outlays roughly triple it

Cognitive AIOE, 50 percent over 10 years, annual loss as a percent of federal receipts:

| tau_l | No outlays | g = 0.10 | g = 0.25 |
|---|---|---|---|
| 0.255 | 0.07 | 0.12 | **0.21** |
| 0.301 | 0.10 | 0.16 | **0.25** |
| 0.318 | 0.11 | 0.17 | **0.26** |

---

## A71. A3 BLOCKED ON ONE INPUT, named once

The order-of-stress table needs a stated materiality threshold for the landlord and
multifamily lender sheet, which requires the agency minimum debt service coverage ratio.

**The exact document: Fannie Mae Multifamily Underwriting Standards, Form 4660.** The
Multifamily Selling and Servicing Guide at `mfguide.fanniemae.com` is fully reachable and was
read; every DSCR and LTV requirement in it is stated as "per Form 4660" rather than given
numerically. Form 4660 itself was not retrievable from the public Guide site in this session
and appears to sit behind DUS Navigate. Guide node 586 defines the Tier system as "Tier 1,
Tier 2, Tier 3, or Tier 4 per the Multifamily Underwriting Standards (Form 4660)"; node 10786
confirms the same for the underwritten DSCR.

**The equivalent alternative is the Freddie Mac Multifamily Seller/Servicer Guide**, which
publishes its minimum DSCR standards in the Guide text rather than by reference.

Also still outstanding from A67, unchanged: the auto loan loss rate separately from student
loans. The New York Fed 2026:Q2 report PDF was obtained and read; the companion data file
carrying the auto 90-plus transition series behind chart 25 was not retrieved.

## A72. A70 AMORTISED A STOCK AS A FLOW. The correction raises long-horizon losses by up to twenty times and the "thirty-fold" statement is WITHDRAWN

`src/fiscal_persistence.py`.

### The error

A70 computed `cumulative loss = displaced wage bill x loss per dollar`, then
`annual loss = cumulative / horizon`. That treats the revenue loss as a one-time flow spread
over the horizon. **It is a stock.** Once a worker is displaced and not fully reemployed, the
revenue they no longer generate is missing in every subsequent year.

Correct treatment: annual loss in year t equals the loss rate per displaced wage dollar times
the CUMULATIVE displaced wage bill at t. With displacement arriving evenly over H years to a
cumulative total D:

| Quantity | Value |
|---|---|
| Terminal-year annual loss | k x D, **independent of H** |
| Average annual loss | k x D x (H+1)/(2H) |
| Cumulative loss over the horizon | k x D x (H+1)/2, **RISING in H** |

### The correction, terminal-year annual loss as a percent of federal receipts

tau_l 0.301, no outlays, Barkai reading, phi 0.5. Federal receipts 5,980.6bn, compensation
16,224.3bn, both 2026 Q2.

| Type | Level | 2y | 5y | 10y | 20y | **A70 said at 20y** |
|---|---|---|---|---|---|---|
| Cognitive AIOE | 50% | 1.51 | 1.15 | 1.01 | **0.94** | 0.05 |
| Cognitive AIOE | 90% | 3.80 | 2.61 | 2.05 | **1.81** | 0.09 |
| Embodied | 90% | 7.65 | 5.27 | 3.64 | **3.00** | 0.15 |
| **Both** | **90%** | **18.75** | **13.04** | **8.71** | **5.94** | **0.30** |

**A70 understated the twenty-year annual loss by a factor of about twenty.**

### The "thirty-fold" statement is withdrawn

A70 said 90 percent of both exposure types costs 42.4 percent of federal receipts a year over
two years and 1.34 percent over twenty, and called that a thirty-fold difference for the same
cumulative displacement. **That comparison was an artifact of the amortisation error.**

On the correct treatment the same cumulative displacement leaves the same wage bill missing
whatever the horizon, so the terminal-year loss is nearly horizon-invariant: 18.75 against
5.94 percent, a **3.2-fold** range for both types and **2.1-fold** for cognitive AIOE. The
residual variation is not the amortisation; it is the labour model, where slower displacement
produces less slack, a higher retained wage share R and therefore a smaller loss per dollar.
That is a real effect and a much smaller one than A70 claimed.

**A56's speed result is unaffected and stands on its own terms.** Speed drives the LABOUR
MARKET channel through slack and reemployment. It does not drive the fiscal channel the way
A70 implied. Conflating the two was the error.

### Cumulative loss now RISES with horizon, which reverses the direction A70 implied

USD billions, same cells:

| Type | Level | 2y | 5y | 10y | 20y |
|---|---|---|---|---|---|
| Cognitive AIOE | 90% | 341 | 468 | 676 | **1,139** |
| Embodied | 90% | 686 | 945 | 1,197 | **1,884** |
| Both | 90% | 1,682 | 2,339 | 2,864 | **3,727** |

Present value at 3 percent: 1,601bn (2y) to 2,514bn (20y) for both types at 90 percent. The
discounting compresses the horizon difference but does not reverse it.

**A slow transition is not a cheaper transition in fiscal terms. It is a more expensive one,
because the loss accrues for longer.** The slow path is cheaper only in the labour market
channel, where it gives reemployment time to work.

### Against the trust funds, which is where this bites hardest

Terminal-year annual loss as a percent of OASDI payroll income (1,323.2bn, A32):

| Type | Level | 2y | 10y | 20y |
|---|---|---|---|---|
| Cognitive AIOE | 90% | 17.2 | 9.3 | **8.2** |
| Both | 50% | 30.1 | 14.6 | **12.3** |
| **Both** | **90%** | **84.7** | **39.4** | **26.8** |

Against a fund whose combined programmes already ran a 160.2bn deficit in 2025 (A32), a
permanent loss of a quarter of payroll income is a different order of problem from anything
in the household channel.

### Range across the whole grid

Terminal-year annual loss 0.00 to 18.75 percent of federal receipts. Cumulative loss 8bn to
3,727bn. Present value at 3 percent, 8bn to 2,514bn.

**R is held at its terminal value along the whole path.** R deteriorates as slack rises, so
this overstates the early-year loss. A full treatment would path R year by year. Stated
rather than hidden.

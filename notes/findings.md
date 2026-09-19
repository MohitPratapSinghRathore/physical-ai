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

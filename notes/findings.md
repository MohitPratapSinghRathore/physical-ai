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

**What it rules out.** Three things. First, any household-DTI-based story about the
mortgage channel: there is no concentration to find. Second, the Phase 1 "flatness"
framing, which was an artifact of share-attribution across mixed-occupation households.
Third, the retired diversification claim (D9 point 3), which depended on flatness.

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
with Eloundou GPT beta. PAEI is close to the mirror image of cognitive AI exposure, so it
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

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

---

## C. Open, not yet evidence either way

- Relative size of Leg A versus Leg W: NOT yet measured. SEC EDGAR blocked this session
  (see notes/open_questions.md Q1). No Leg A number has been produced, and none should be
  quoted until it is.
- Holder map (WS2): not started.
- The tau*s threshold: not yet checked or tightened. No derivation work done this session.
- Whether high-PAEI households hold disproportionate CONSUMER credit, auto debt or rent
  arrears. Untested and now the highest-value open question, because the mortgage answer
  (A4) came back flat and the consumer-credit answer is where the brief's hypothesis is
  most likely to survive. Needs SCF or credit-bureau microdata; ACS PUMS cannot see it.
- The mortgage DEBT STOCK version of DAR, as opposed to debt service. Needs SCF.

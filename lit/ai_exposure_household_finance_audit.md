# Audit: does anything link occupational AI exposure to household financial outcomes?

Searched 2026-09-19. Question: is there published or working-paper work connecting
occupational AI or automation exposure to household financial outcomes (debt, savings,
delinquency, financial behaviour)? Nothing enters `paper/references.bib` unverified.

## Headline

**No paper was found that measures occupational AI exposure against household balance-sheet
outcomes.** The two literatures exist separately and in a specific pattern:

- Occupational exposure indices are mature and standardised (Felten AIOE, Eloundou GPT
  exposure, Webb, Autor-Dorn routine task intensity), and are used almost exclusively against
  LABOUR outcomes: employment, wages, participation, occupational mobility.
- Household financial outcomes are measured richly (New York Fed Household Debt and Credit,
  SCF, SIPP) and are linked to income shocks generically, not to occupational exposure.

The nearest work reaches PUBLIC balance sheets (disability insurance) rather than household
ones. That is the gap this project sits in, and it is worth stating in the paper as a
positive claim about what is missing rather than a novelty boast.

## What exists, verified

### 1. Altindag, El Cheikh Taha, Nunley and Seals (July 2026), "Robots and the Public Finance of Disability Insurance"

- Retrieved from arXiv 2607.02892, 42 pages, read directly.
- What it measures: the effect of industrial robot exposure on Social Security Disability
  Insurance APPLICATIONS, using confidential commuting-zone data and a shift-share design
  instrumenting US exposure with earlier European robot diffusion.
- Findings, in this project's words: one additional robot per 1,000 workers LOWERS
  applications by about 8 per 100,000 working-age residents, with the largest declines among
  workers aged 55 to 64. Employment-to-population ratios do NOT fall in exposed commuting
  zones. A year's flow of averted applications corresponds to roughly 3.4 billion dollars.
- **This is the closest published work to the fiscal half of this project**, and it reaches a
  public balance sheet, not a household one.

**IT ALSO CONTRADICTS ACEMOGLU AND RESTREPO ON TWO POINTS AND THAT MUST BE REPORTED.**
A-R (2020), Section V.C, find INCREASED take-up of Social Security retirement and disability
benefits in robot-exposed areas, and employment-to-population ratios that DO fall. Altindag
and coauthors find disability applications falling and employment-to-population not falling.
The designs differ (applications against take-up; different instruments and periods), so this
is not necessarily a direct contradiction of the same estimand, but it is close enough that
this project cannot lean on the A-R benefit-take-up result as settled. The early-retirement
variant in `src/stock_flow_v3.py` is accordingly labelled SCENARIO with no sourced rate, and
that labelling is now doubly justified.

### 2. Fan (2025), "The Labor Market Incidence of New Technologies", Yale job market paper

- Retrieved from arXiv 2504.04047, 105 pages, read directly. Dated October 30, 2025.
- What it measures: the incidence of automation and AI shocks under a distance-dependent
  elasticity of substitution, where worker mobility between occupations declines with their
  distance in skill space. 306 occupations mapped into cognitive, manual and interpersonal
  skill dimensions.
- Findings, in this project's words: automation and AI CLUSTER within skill-adjacent
  occupations, which constrains employment adjustment and amplifies wage effects. Twenty to
  fifty percent of labour demand shocks translate into wages, against about thirty percent
  under standard models, and mobility recovers only about twenty percent of losses, against
  about thirty percent under standard estimates.

**This is the closest thing in the literature to the destination-pool parameter phi**, and it
is an independent, structural, estimated version of the mechanism this project imposed by
assumption. Its headline number is directly usable as an anchor: if mobility recovers 20
percent of losses where standard models give 30, the destination pool is roughly a third less
effective than a no-clustering model assumes, which corresponds to **phi of about 0.33**,
inside the {0, 0.5, 1} grid already run and close to the employment-share anchors used.

It also independently supports the exposure-type framing: the clustering is in SKILL space,
and cognitive and manual are separate dimensions in the estimation.

### 3. What was searched and NOT found

- Occupational AI exposure against household debt, delinquency, savings or financial
  behaviour: nothing located.
- Automation or routine-task-intensity exposure against mortgage delinquency at county or
  worker level: nothing located. Searches returned the automation-exposure literature and
  the household-debt literature separately, with no work joining them.
- AI in consumer credit appears repeatedly but is the OTHER direction: AI used as a lending
  or collection technology, not AI exposure as a borrower risk factor. One verified example
  is an NBER working paper on AI against human callers in debt collection, which is about
  collection technology and is not relevant here.

## How this project's household stress test differs

| | The literature | This project |
|---|---|---|
| Unit | Commuting zone or occupation | Household, ACS PUMS and SIPP microdata |
| Outcome | Employment, wages, participation, benefit applications | Debt service to income, liquidity runway, obligations held by distressed households |
| Exposure | Robots, or a single index | Two exposure TYPES compared, embodied and cognitive, on two cognitive indices |
| Mechanism | Reduced-form local labour market effect | Simulated displacement worker by worker, with household income recomputed including non-wage income and reemployment |
| Question | Did exposure change labour outcomes? | Which balance sheets come under stress, in what order, at what displacement flow |

The distinction that matters for the paper: **existing work establishes that exposure moves
labour outcomes. It does not establish what that does to household balance sheets, and it
does not connect either to supervisory loss measurement.** This project's contribution is the
join, not the exposure measure and not the household data, both of which are borrowed.

## Consequences for this repository

1. Fan (2025) should be cited wherever phi appears, as the independent estimate of the
   mechanism. The phi = 0.33 anchor is added to the grid.
2. Altindag and coauthors must be cited alongside Acemoglu and Restrepo wherever benefit
   take-up or the participation margin is discussed, with the disagreement stated.
3. The claim that no work links AI exposure to household balance sheets is a NEGATIVE
   result from a non-systematic search. It is stated as "none located" and not as "none
   exists". The systematic protocol in `lit/protocol.md` covers a different question and was
   not re-run for this one.

---

# Addendum: novelty check for the labour backing ratio

Searched 2026-09-19 for any work measuring, system-wide, the share of financial claims
ultimately serviced from labour income. **None located.** Full assessment in
`framework/labor_backing/feasibility.md`. Three adjacent literatures, none of which computes
it:

1. **Human wealth and housing collateral** (Lustig and Van Nieuwerburgh, and with Verdelhan).
   Measures the present value of labour income as an ASSET and the housing-to-human-wealth
   ratio. The mirror image of the proposed statistic, not the same object.
2. **Debt service ratios** (BIS database, seventeen economies; Federal Reserve household
   DSR). Interest plus amortisation over income, where income explicitly includes labour,
   self-employment and capital income together, with no labour decomposition, and covering
   only the private non-financial sector.
3. **Whom-to-whom financial accounts.** Trace who HOLDS claims, not what cash flow services
   them.

The search was NOT systematic; `lit/protocol.md` governs a different question and was not
re-run. The claim is "none located", not "none exists", and it should not be load-bearing
until a systematic search and a direct approach to the Federal Reserve Financial Accounts
team have been made.

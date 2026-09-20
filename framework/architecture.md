# Institutional architecture, derived from the holder gap

Built to `framework/architecture_spec.md`. Every row obeys the spec's five binding rules.
Every statement carries a tag: **[M] measured**, **[R] replicated**, **[S] scenario**.

**Audit note, rule (a).** `framework/architecture.md` did not previously exist; only the
build specification did. So there were no rows to remove. Instead, every candidate
instrument was tested against the cleared claim set of
`data/release/headline_clearing_pass.csv` before entry, and **five candidates were rejected**
because they rest on a withdrawn, superseded or removed claim. They are listed in section 9
rather than deleted silently.

---

## 0. Three standing rules, and the first is a limitation

**RULE 1. Above about 25 percent displacement every result is a BAND, and this is a LIMIT OF
OUR METHOD rather than a fact about the economy.** The reemployment rate is a straight-line
fit extrapolated until it breaks. It has a pole at an employment dose of 0.676142, which is a
wage-bill dose of **0.459 for the physically exposed group**, and a point estimate exists only
where the solution sits inside the observed range [0.49, 0.74]. **The physically exposed group
loses its point estimate first, between 17 and 25 percent; at 50 percent none of the three
groups has one.** Beyond that the only reportable object is the band from the worst observed
vintage down to zero, labelled outside the data. **A referee will say this boundary is a
property of the specification, not of the world, and they will be right: it is stated as a
limitation wherever it appears, never as a finding.** Any instrument sized above 25 percent is
sized on a band.

**RULE 2. The federal share of first-round losses is reported BOTH WAYS on the agency book.**
See `notes/item3b_gse_classification.md`. Narrow reading (only loss beyond capital is federal)
is the lower bound; conservatorship reading (the whole retained loss is federal) is the upper
bound. They differ by 8 to 10 percentage points and never change the qualitative result.

**RULE 3. Every credit figure is FIRST ROUND ONLY, with house prices held fixed.** It is a
floor, not an estimate.

---

## 1. The gap this architecture exists to close

> **The federal government is exposed, as holder, guarantor or debtor, on 0.794 of the claims
> paid directly from wages (agreed range 0.778 to 0.804) [M, agreed with an independent
> rebuild]: 0.321 as creditor or guarantor and 0.552 as the obligor on Treasury debt serviced
> from wage taxes, less a 3,226.4bn overlap where it holds its own debt. It holds 0.010 of the
> claims on AI capital (range 0.0095 to 0.0102) [S], an UPPER bound because that side is
> on-balance-sheet only. The gap is 0.784.**

**The split matters for the instruments and not only for accuracy.** The 0.321 creditor and
guarantor leg is what rows 5 and 6 act on, because a guarantee can be restructured. The 0.552
obligor leg is what row 2 acts on, because debt already owed can only be pre-funded or termed
out. **No instrument in this table touches both legs**, which is why the table has separate
fiscal and housing rows rather than one sovereign row.

**The paired presentation, which must travel with the number** (see
`notes/item2b_sovereign_share_paired.md`). The one-step rule that produces 0.794 IS the
first-round versus second-round boundary the rest of the paper uses:

| | what it measures | federal share |
|---|---|---|
| **first round**: claims serviced DIRECTLY from labour income | mortgages, rent, consumer credit, student loans, Treasury and municipal debt | **0.794** (0.778 to 0.804) |
| **including second round**: indirectly serviced claims added | business revenue funded by wage-financed spending | **0.452** |

**The state is the first-round holder; private balance sheets are the second-round holders.**
Widening to indirect exposure does not weaken the concentration finding, it relocates it: the
claims added are held by banks, insurers, pensions, foreign investors and households. **That
relocation is what the instruments in section 2 have to act on**, and it is why the bank and
lender instruments (rows 8, 9, 10) exist alongside the fiscal ones.

The other three structural calls: obligor leg excluded **0.321** (which is just the creditor
and guarantor leg on its own), agency pools not federal **0.587**, commercial mortgage treated
as rent-serviced **0.741**. No measurement call moves the share by more than 1.3 percent.

That single asymmetry organises everything below. The state is the residual holder of the
exposure that fails if AI succeeds, and holds essentially none of the exposure that pays if
it does. **It is largely unhedged: its only claim on the AI leg is whatever capital tax
reaches it**, which is instrument row 1 and is exactly what section 3 shows to be contested.
The claim is real but we could not size it: the 0.36 hedge ratio was withdrawn because one of
its inputs was never defined, not because it is zero.

**What it would take to close the gap by ownership alone [M, arithmetic on a SCENARIO base].**
The AI leg at the central scale is 14,857.4bn (AI equity 14,399.0bn plus on-balance-sheet AI
debt 458.4bn):

| state share of the AI leg | stake required | share of the gap closed |
|---|---|---|
| 0.010, today | 148.6bn | 0 |
| 0.05 | 742.9bn | 5.1 pct |
| 0.10 | 1,485.7bn | 11.5 pct |
| 0.20 | 2,971.5bn | 24.2 pct |
| 0.50 | 7,428.7bn | 62.5 pct |
| 0.794 | 11,796.8bn | 100 pct |

For scale: combined Enterprise net worth is 179.4bn and annual guarantee fee income is
40.5bn. **Closing even a tenth of the gap by ownership requires a stake eight times the
entire capital of the housing agencies.** That is the honest size of the ownership
instrument, and it is why the instruments below are mostly not ownership instruments.

**The caveat that travels with every row [limitation L1].** The AI leg is on-balance-sheet
Tier 2 only. Off-balance-sheet SPV financing and GPU-backed lending are unmeasured, so the AI
leg is a lower bound, the state's share of it is an upper bound, and the required stakes
above are upper bounds on the share and lower bounds on the dollars.

---

## 2. The instrument table

One row per instrument. **Gap closure** is stated only where it is computable; where it is
not, the row says what would make it computable rather than guessing.

| # | Measured mechanism, claim | Institution that must act | Instrument | Type | Verified precedent | Trigger indicator, current value | Binds in | Gap closure or loss removed |
|---|---|---|---|---|---|---|---|---|
| 1 | The fiscal condition is a FUNCTION of the capital tax rate, threshold 0.110 to 0.137 **[M]**, with R = 0.568316 **[R]**. It fails at the 0.0708 AI capital actually bears and passes at the 0.20 to 0.22 measured economy-wide. **The verdict is PROVISIONAL and depends on the base**, see section 3 | Tax authority (Congress, Treasury, IRS) | Narrow the gap between the AI-specific and economy-wide capital rates: limit expensing on labour-displacing assets, capture shifted rents, or tax the distribution rather than the entity. **Target: 26 to 52 pct of the AI surplus at the economy-wide rate.** NOT a statutory rate rise, and NOT an AI-specific tax | tax | US statutory corporate rate cut from 35 to 21 pct, Public Law 115-97 (2017), is the same instrument operated in reverse | Effective rate on AI surplus **0.0708** against a threshold of **0.1101**. **BELOW THRESHOLD** | inside the data and larger displacement; **fails at near-total displacement**, see 4(d) | Closes the FISCAL gap by construction at break-even. Does NOT close the holder gap: taxing a return is not holding the asset |
| 2 | 55.2 pct of labour-backed claims are federal obligations, and the sovereign union share traces a U: 0.523 in 1952 (almost all wartime Treasury debt), 0.336 in 1970, 0.794 in 2025, with the whole net rise since 2008 in the obligor leg **[M]** | Treasury, and the fiscal authority setting the debt path | Pre-fund or term out the labour-linked obligation stock while the labour tax base is intact | stock | Norway's Government Pension Fund Global, established by the Government Pension Fund Act, is a sovereign pre-funding vehicle against a resource-linked revenue base | Debt to GDP at start **1.214** **[R]**; 20-year emerging-market baseline **376.7 pct** **[R]** | all regimes; the only instrument that acts BEFORE the dose | Not a gap closure. It buys time on the obligor leg, which is 55.2 pct of the wage leg |
| 3 | The state holds 0.010 of the AI leg **[S]** against 0.794 of the wage leg **[M]** | Treasury, or a statutory fund | Direct equity or revenue claim on AI capital: sovereign fund, golden share, or a public stake taken in exchange for public inputs | ownership | Norway GPFG; the US Treasury's 2008 to 2010 TARP equity stakes under the Emergency Economic Stabilization Act | Debt-financed share of AI capex **0.0654**; self-funding ratio **1.3426**, four of nine filers below 1.0 | larger, sudden and near-total displacement; **unnecessary inside the data** | **Directly measurable: see the table in section 1.** 0.10 of the AI leg closes 11.5 pct of the gap |
| 4 | Trust funds are payroll-funded: OASDI payroll share 0.9126, HI 0.8720; OASI depletes 2032Q4, HI 2033Q2, combined OASDI 2034Q3 **[M]** | Social insurance system (SSA, CMS, Congress) | Broaden the contribution base beyond covered wages, or convert to a general-revenue claim; and raise UI generosity and duration, which has a MEASURED effect on automation wage losses | flow | Medicare's Net Investment Income Tax, 26 USC 1411, funds Part A adjacent spending from a non-wage base. **MEASURED EFFECT, Brollo (2024), IMF WP 2024/095: US states with more generous UI saw a wage decline from robotisation about TWO-THIRDS SMALLER, concentrated among workers without a college degree; one robot per thousand workers raised poverty 0.3pp, mostly attenuated where social assistance was more generous. US maximum UI duration of 26 weeks is on the low side of the OECD** | Combined OASDI depletion **2034 Q3**, 83 pct of scheduled benefits payable at depletion | all regimes; binds SOONEST, because depletion arrives before any AI dose does | Removes the trust fund component of the fiscal loss, **4.07 pct of OASDI payroll income at the 10 pct dose** |
| 5 | Retained agency loss 3.3 to 12.5 pct of Enterprise net worth at the 10 pct dose, zero Treasury draw; 39 to 53 pct of each single-family book carries no credit enhancement **[M]** | Housing agencies (FHFA, Fannie, Freddie, FHA, Ginnie) | Forbearance and payment-deferral protocol pre-authorised for a displacement trigger; raise credit enhancement on the unenhanced book | contract | The CARES Act (Public Law 116-136) sections 4022 and 4023 pre-authorised federally backed mortgage forbearance. The precedent is exact | Household debt in any stage of delinquency **4.7 pct**, down 0.1pp on the quarter | larger and sudden displacement; **unnecessary inside the data**, where no draw is triggered | Removes the retained agency loss, **5.85 to 22.48bn at the 10 pct dose**, from the federal balance sheet |
| 6 | Federal government holds 97.3 pct of the student book **[R]** and student labour backing is 0.8832 **[M]** | Student loan system (Education, servicers) | Income-driven repayment with an automatic displacement trigger; the claim already flexes with income | contract | Income-Driven Repayment is established US law, 20 USC 1087e(e). This instrument already exists and needs only a trigger | Recent graduate unemployment **5.6 pct**, underemployment **42.0 pct**; employment gap for workers aged 22 to 25 in AI-exposed occupations **19 pct below counterfactual and widening** | all regimes, and it is the CHEAPEST row here because the instrument exists | Converts a default loss into a deferred claim. The book is already 97.3 pct federal, so this moves timing, not incidence |
| 7 | Auto is the one household credit channel with a real pathway-specific contrast: A31 adjusted +13.39, t = 3.50 **[M]** | Auto lenders and ABS investors; supervisors for the bank-held slice | Displacement-contingent payment holiday in auto contracts; ABS documentation that anticipates it | contract | CARES Act forbearance is the model; auto has no statutory analogue, so this is contractual rather than legislative | Auto loan balance 90+ days delinquent **5.49 pct** | larger and sudden displacement | Removes the auto component of first-round private loss. Sized in the dose-response table |
| 8 | Demand leads the other channels in **20 of 27 grid cells**, 0.7407 exactly **[R]**. SEPARATELY and with a different status: roughly **nine tenths of bank losses arrive through the second round** rather than through displaced borrowers' own loans, and second-round bank losses span 173 to 1,565bn, both **[S]**. The two are different quantities and the earlier text merged them | Bank supervisors and the central bank | An automation scenario in the supervisory stress test, routed through spending, house prices and business credit, reported as a BAND | buffer | The Federal Reserve's 2026 Dodd-Frank Act stress test is the existing vehicle; the climate scenario analysis pilot is the precedent for adding a non-traditional scenario | Aggregate CET1 **12.8 pct** falling to a minimum of **11.2 pct** under the Fed severely adverse scenario; all 32 banks above minimums | larger and sudden displacement | Not a closure. It makes the exposure visible and prices the buffer |
| 9 | Bank C and I commitments to AI-adjacent industries 450bn, 13 pct of total commitments, 25 pct of tier 1 committed **[M]**. MODULE A: C and I heavy banks breach at 33.0 pct at a 50 pct dose, and card-heavy at 77.8 pct, so the AI-lending concentration sits on models that are already the most wage-exposed | Bank supervisors | Concentration limits or a supervisory add-on for AI-linked lending | buffer | 12 CFR 32, the national bank lending limit, is the existing concentration instrument | **450bn, 13 pct of commitments**, no threshold set | the AI-fails case above all; also larger displacement | Reduces the correlated loss where a holder is on BOTH legs. That is the hedge failure population |
| 10 | The exposure is unpriced and uniformly spread, so the system in aggregate cannot rotate out of it **[M]**. The flat debt-service result is partly mechanical because underwriting caps DTI | Bank supervisors, statistical agencies | **NOT wholesale mortgage underwriting change.** Instead: disclosure of occupational exposure concentration at portfolio level | statistics | HMDA (12 CFR 1003) is the existing portfolio-disclosure vehicle | County at-risk-rate dispersion, p99/p1 | larger displacement only | Not a closure. See the fair lending constraint in section 6 |
| 11 | Prime-age nonemployment 19.31 against an observed maximum of 24.71, and rho has no point estimate outside [0.49, 0.74] **[M]** | Statistical agencies (BLS, Census, BEA) | Measure reemployment, destination wages and never-hired entry directly and at higher frequency | statistics | The Displaced Worker Survey exists biennially; the instrument is frequency and destination detail, not a new survey | Prime-age nonemployment **19.31**, threshold **24.71**, **INSIDE** | all regimes; it is the precondition for every trigger below | **The binding constraint on this whole architecture.** Item 2 shows the reemployment rate has no admissible estimate past a 45.9 pct embodied dose |
| 12 | India-type case: AI capital imported, surplus accrues abroad, so domestic tau_k is effectively lower **[M, open-economy derivation]**; 20-year emerging-market debt baseline 376.7 pct **[R]** | Emerging-market fiscal authorities; IMF surveillance | Source-based taxation of imported AI services; reserve and debt-path buffers built before the dose | tax | The OECD/G20 Inclusive Framework Pillar One and Pillar Two are the existing source-taxation instruments | Emerging-market baseline **376.7 pct of GDP over 20 years** | all regimes, and it binds HARDEST because the instruments above are unavailable | Not computable for these economies: B6 finds the ratio not computable to a publishable standard for India |

---

## 3. The taxation argument, softened to the corrected numbers

The superseded version said there is no reading of the corporate tax literature in which the
break-even rate is an available instrument. **That is false and it was withdrawn** (claim
168, downgraded in A96 to A100). The corrected argument, and it is weaker:

**[M] A capital tax near the top of observed effective rates could break even at moderate
displacement.** Case A break-even runs **0.125 to 0.301** and the sourced range of effective
rates tops out at **0.20351**, so the break-even rate is at or below the top of the sourced
range in **10 of 15 cells**. The required rate to close the fiscal condition at the observed
R is **0.110 to 0.137**, comfortably inside the sourced range.

**[M] At large displacement the required rate leaves observed experience.** Case A reaches
**0.301** with output preserved, which is exactly tau_l and is attained where R falls to
zero. Case B, output falling, reaches **0.650**. Case B break-even is at or below the sourced
top in only **5 of 15** cells.

**[R, independent corroboration] RAND reaches the same magnitude by a different route.**
Price and Suresh (2026) conclude that corporate tax revenue cannot offset displaced labour
revenue "unless the corporate tax rates were roughly doubled to be at parity with labor tax
rates". Our required rate is 1.55 to 1.94 times the operative rate. **Two independent
constructions, one macro and one from sourced effective rates, give the same answer.**

**So the surviving claim is narrow and must be stated in this form:**

> The break-even capital tax rate exceeds the **OPERATIVE** effective rate of 0.0708 in every
> cell of the grid in both cases, and exceeds the top of the **SOURCED** range only at larger
> doses. That is a statement about the tax code as it stands, not about what the literature
> says is attainable.

**Therefore ownership, dividend and direct-claim instruments grow in importance with the
dose.** At small doses the tax instrument is sufficient and rows 3 and 4 are unnecessary. At
large doses the tax instrument is exhausted and only instruments that hold the asset, rather
than tax its return, remain.

**[M] One thing a capital tax cannot do, and it is a hard constraint.** Replacement income
funded from a capital tax **cannot repair the payroll-funded trust funds**, because it is not
covered wages. OASDI and HI are funded from a payroll base whose payroll shares are 0.9126
and 0.8720. A dollar of capital-tax-funded transfer income generates no OASDI or HI
contribution. **Rows 1 and 4 are therefore not substitutes.** Any package that funds
replacement income from capital and expects the trust funds to recover has a hole in it the
size of the payroll share.

**[THE CAPITAL TAX RATE EXPOSURE. Full note: `notes/tau_k_exposure.md`. Figure:
`paper/figures/fig_tau_k_condition.png`.]** Row 1 of the instrument table is conditional on a
rate that is itself contested, and the architecture must say so before it recommends anything.

**The condition is a function of tau_k with a threshold at 0.110 to 0.137, and the two
defensible measurements fall on opposite sides:** ours, the operative rate on the **AI
surplus**, is **0.0708** and the condition **fails**; the IMF's measured **economy-wide**
average tax rate on capital income is **0.20 to 0.22** and the condition **passes**. Ours is
lower because 26 USC 168(k) expensing exempts the normal return, leaving only the 0.351 rent
share taxed, and because 48 percent of rents are shifted abroad. Theirs is higher because it
is an average rather than a marginal rate, includes personal-level taxes on dividends and
gains, and covers a capital stock that is mostly neither fully expensed nor shiftable.

**What this does to row 1.** The instrument is not "raise the statutory rate". It is
**narrow the base difference**: between **26 and 52 percent of the AI surplus** would have to
bear the economy-wide rate rather than the AI-specific one for the condition to close. That is
achieved by narrowing expensing, capturing shifted rents, or taxing the distribution rather
than the entity. **Row 1 is re-specified accordingly and its trigger is unchanged.**

**Status.** The threshold is **[M]**; the condition boolean is **[R]**; **the verdict attached
to it is PROVISIONAL**, because it rests on a base choice a public finance economist may
reasonably make differently. It is the first question for a public finance co-author.

**[IMF SDN/2024/002, read in full this session] Two things the literature now settles, and
one vulnerability it opens in our own number.**

*Settled, and our architecture matches it.* "**A specific tax on gen AI is therefore not
recommended**": the base is hard to define, assets can be relabelled, and AI location is
mobile. The recommendation is instead to reconsider capital allowances that favour
labour-displacing assets and to strengthen **general** capital income taxation. That is
exactly row 1, and it is why no row in this table is an AI-specific tax.

*Settled, and it corroborates our sourced maximum.* The IMF puts the advanced-economy average
tax rate on capital income at roughly **0.20 to 0.22**, from the Bachas and others (2022)
macro-historical database. **Our sourced maximum of 0.20351 was built independently** as
`0.351 x 0.21 + 0.649 x 0.20` on a rent-share decomposition and lands on the same number.

*The vulnerability, reported against ourselves.* The same IMF series put the **US** average
tax rate on capital well above our operative **0.0708**. The two are different objects: ours
is the rate on the **AI surplus** after profit shifting and the rent decomposition, theirs is
an economy-wide average on all capital income including personal-level taxes. **A referee will
place them side by side, and the paper must pre-empt it in the text rather than in a
footnote**, because the fiscal condition fails at 0.0708 and would be closer to closing at the
IMF's measured rate. This is a live exposure in the paper's central fiscal result.

*The live disagreement, named rather than smoothed over.* Falk and Tsoukalas conclude a
Pigouvian automation tax is the instrument that works; the IMF concludes a specific AI tax is
not implementable; Costinot and Werning's optimal robot tax of 1 to 3.7 percent of the robot
price sits between them. **Our contribution is none of those verdicts: it is the calibrated
break-even rate that says what any such instrument would have to raise.**

**[Falk and Tsoukalas 2026, connected work] The theoretical case is stronger than ours.**
They show that capital income taxes, worker equity, UBI, upskilling and bargaining all fail
to resolve the automation externality, and that a Pigouvian automation tax can. They have the
result first and in more general form. **Ours is the calibration, not the verdict.**

---

## 4. By regime: the minimum sufficient set, and what is unnecessary

### (a) Inside the data, about 10 percent of wages displaced **[M, the only fully inside-data regime]**

Federal share of first-round losses **0.785 to 0.870** (narrow) or **0.876 to 0.913**
(conservatorship). Terminal fiscal loss **85.168bn [R]**. Retained agency loss **5.85 to
22.48bn**, **zero Treasury draw**. Trust fund loss **4.07 pct** of OASDI payroll income.

**Minimum sufficient set: rows 1, 4, 6, 11.** The tax instrument is inside the sourced range
here, the trust fund base problem binds anyway for reasons unrelated to AI, income-driven
repayment already exists, and measurement is the precondition for knowing when to move.

**Unnecessary at this dose:** rows 3 (ownership), 5 (housing forbearance), 7 (auto), 8
(stress scenario as a binding requirement rather than a disclosure). **The agency book
absorbs this dose without a draw and mortgage relief answers a channel the data shows to be
small.** Rule 2 of the spec rules them out here explicitly.

### (b) Larger displacement, 25 to 50 percent **[S, and outside the data for rho]**

**The boundary must be stated before any number in this regime.** At the 25 percent dose the
two cognitive types still have a reemployment point estimate and the embodied type does not.
**At 50 percent no type does.** All numbers here are bands, not points.

Federal share rises to **0.810 to 0.925** (narrow). Retained agency loss reaches **27 to
83bn**. Case A break-even reaches the top of the sourced range.

**Minimum sufficient set: rows 1, 3, 4, 5, 6, 7, 8, 11.** Nearly everything. The tax
instrument is at its sourced limit, so the ownership row enters here and not before.

**Unnecessary:** row 10 as an underwriting change; it stays a disclosure instrument at every
dose (section 6).

### (c) Sudden displacement **[S]**

Distinguished from (b) only by speed. The measured constraint is the observed annual
displacement flow, **0.00679**, against a speed limit that is a RANGE of 0.0005 to 0.0715 a
year across the full specification table, median 0.0273, **never a single number**.

**Minimum sufficient set adds nothing new but reorders it.** The contract instruments (5, 6,
7) move to the front, because they are the only ones that act inside a quarter. Tax changes
and ownership stakes take legislative time the regime does not have. **Pre-authorisation is
the whole instrument:** the CARES Act precedent worked because it was enacted in weeks, and
the architectural lesson is to have the trigger and the protocol written before the event.

**Unnecessary: row 2.** Pre-funding is useless once the shock has arrived.

### (d) Near-total displacement **[S, far outside the data]**

R falls toward zero, so tau_l * (1 - R) reaches tau_l and case A break-even equals tau_l
exactly, **0.301**. With output falling, **0.650**.

**Minimum sufficient set: rows 3 and 4 only, and row 3 is doing the work.** Every
revenue-side instrument that taxes labour income is arithmetically empty when there is no
labour income. A capital tax at 0.30 to 0.65 is outside all observed experience. **Only
holding the asset works, and section 1 prices that: closing the gap requires a stake of
11,797bn.**

**Unnecessary: rows 5, 6, 7, 8, 9, 10.** Every credit instrument is second-order when the
income they are contingent on has gone. **This regime is where the architecture stops being
financial regulation and becomes a question about ownership, and the paper should say so and
stop there.**

### (e) The AI-fails case **[S]**

The wage leg pays, the AI leg does not. Anchored on two verified historical analogues:

| | equity financed, 2000 to 2002 | debt financed, 2007 to 2009 |
|---|---|---|
| nonfinancial corporate equity fall | -30.6 pct | -19.2 pct |
| federal receipts fall | **-9.5 pct** | **-16.0 pct** |
| corporate tax receipts fall | -35.1 pct | -53.4 pct |

**[M] The current structure resembles 2000, not 2008.** The debt-financed share of AI capex
is **0.0654**, well below the 0.20 boundary, and the aggregate self-funding ratio is
**1.3426**. **LOWER BOUND, and this is the one place where limitation L1 could change the
answer**: the measure excludes off-balance-sheet and SPV financing, which BIS QR March 2026
identifies as dominant.

**Minimum sufficient set: row 9 only.** Concentration limits on AI-linked bank lending, aimed
precisely at holders who are on both legs.

**Unnecessary: rows 1, 3, 4, 5, 6, 7.** Every wage-leg instrument is unnecessary here, and
that is the point of the two-sided bet: **the instrument set is nearly disjoint across the
two failure directions, which is why a single institution cannot prepare for both with one
policy.**

**The watch item is composition, not level.** Four of nine named filers (ORCL, CRWV, DLR,
EQIX) are already below a self-funding ratio of 1.0 individually while the aggregate is 1.34.

---

## 5. Housing agencies, per item 1

**Classification of the retained loss is set out once, both ways, in
`notes/item3b_gse_classification.md`, and standing RULE 2 above applies to every figure here.**

**[M] What the evidence supports.**

- The single-family books are **39 to 53 percent unenhanced**. That is where the loss lands
  and it is the fact the superseded waterfall concealed.
- Private cover transfers only **11 to 15 percent** of an agency loss at small doses. CRT is
  mezzanine with the Enterprise retaining the first loss, sourced from both filings, and the
  outstanding band is **2.3 to 3.1 percent** of the reference pool. PMI covers **21 to 22
  percent** of the book at a depth of **26.6 percent**.
- **Zero Treasury draw at every dose from 5 to 75 percent**, on the statutory
  negative-net-worth trigger: 179.4bn of capital against a maximum retained first-round loss
  of 109.0bn.
- The Enterprises earn **40.5bn a year in guarantee fees**, more than the entire retained
  loss at the 10 percent dose.

**[M] What it does not support.** Any statement that the Treasury backstop is reached through
the agency book at a wage shock this engine can produce. It is not, and the superseded text
implying otherwise is withdrawn.

**[M] The constraint that must travel with all of it.** This is **first round only**, with
house prices held fixed. Agency credit losses are driven by negative equity at least as much
as by income. **This is a lower bound and the instrument in row 5 should be sized against a
house price scenario we have not run.**

**The instrument follows from the structure, not from the loss.** Because the loss is small
relative to capital but the unenhanced share is large, the instrument is not recapitalisation.
It is **pre-authorised forbearance on a displacement trigger** (CARES Act sections 4022 and
4023 as the exact precedent) and **credit enhancement on the unenhanced book**, which is the
standing structural exposure whatever the dose.

---

## 6. Banks and lenders, REWRITTEN FROM MODULE A

Superseded: the previous version of this section reasoned from system aggregates and paired
each household exposure with a household-facing instrument. **Module A tested that at
institution level across 4,313 banks and 4,299 credit unions and it does not hold.** Full
result: `notes/GATE_REPORT_module_A.md`.

### 6.0 The finding that reorganises this section

**Household-facing instruments cannot protect bank capital.** Forbearance, income-driven
repayment and wage insurance, all together, remove **under 10 percent of system losses at
every displacement level**: 9.61 percent at 10 percent, 8.91 at 25, 7.59 at 50.

The reason is structural. These instruments act on the FIRST round, displaced borrowers
defaulting on their own loans. At the 10 percent dose that is about 27bn of a 205bn total.
**The other 178bn is the second round**, arriving through spending, house prices and business
credit from people who were never displaced. Eliminating household default entirely would
remove at most about a seventh.

> **Therefore: judge rows 5, 6 and 7 on household outcomes, not on bank capital. Judged on
> bank capital they are close to useless. What protects bank capital is an instrument that
> acts on the second round, on demand, or on the buffer itself.**

Enhanced wage insurance costs **314bn to remove 12.9bn of bank losses** at the 10 percent
dose. That ratio is absurd as bank protection and is the point of the programme as income
protection. **The paper states which reading applies.**

**But the instruments do reshape the distribution, and that is the case for them.** At the 25
percent dose the combined package takes assets in breach from **4.02 to 1.48 percent** and
stops **123 institutions** breaching; at 50 percent it stops 547. **They change who fails,
not how much is lost.**

### 6.1 What each TYPE of institution should change, tied to its measured exposure

| institution type | measured exposure | what it should change | what the evidence does NOT support |
|---|---|---|---|
| **Card-heavy lenders** (18 banks, 1,257.6bn) | **The most exposed model by a distance: 38.9 pct breach at a 25 pct dose, 77.8 pct at 50** | Hold capital against the card book explicitly for a displacement scenario; card losses are 17.1 pct in the Fed's own severely adverse test and this shock is larger on that book | Any claim that this is a tail risk. It is the first model to break and it breaks inside the range the paper models |
| **Credit unions** (4,299, 2,522.6bn) | **The only class showing stress at the 10 pct dose**, 1.12 pct of them; 28.1 pct at 50 | Recognise the concentration: a book that is almost entirely household credit has no C and I or commercial real estate to dilute a wage shock. NCUA stress expectations should reflect that | Treating them as small and therefore safe. They are undiversified by design, not by accident |
| **Large and regional banks** | 23.1 and 15.0 pct breach at 50 pct; **0.0 pct at 10 pct** | The supervisory scenario in row 8, routed through the second round | That household underwriting change helps them. It does not: their exposure is the second round |
| **Community banks** (3,246, 1,064.2bn) | 4.0 pct at 50 pct, near zero below | Nothing specific. They are not the exposed population | Imposing the same requirements as on card-heavy lenders |
| **Auto lenders and ABS investors** | 36.0 pct breach at 50 pct; auto is the one pathway-specific household contrast that survives pay controls | Displacement-contingent payment clauses in contracts and ABS documentation | Wholesale change at moderate displacement: 0.0 pct breach at 25 pct |
| **Mortgage portfolio lenders** (702, 522.0bn) | **Among the LEAST exposed: 0.1 pct at 25 pct, 3.9 pct at 50** | Portfolio disclosure of occupational concentration, per row 10 | **Underwriting change of any kind.** This is now measured at institution level and it closes the question the retired claim left open |
| **Housing agencies** | Section 5; zero Treasury draw at any dose | Pre-authorised forbearance and enhancement on the unenhanced book | Recapitalisation |
| **Insurers** (820.6bn labour-backed held) | Holders on both legs; matched long liabilities | Report the AI-linked and wage-linked holdings together, because the hedge failure applies to them | Forced-sale style rules. They hold to maturity against matched liabilities |
| **Private credit** (inside 6,186.9bn other-financial, an UPPER bound) | Cannot be separated from the Z.1 aggregate | Disclosure sufficient to separate it. **This is a measurement instrument, not a prudential one** | Any sizing claim. We do not know the number |
| **Pension funds** (444.6bn held) | Contributions are a share of covered payroll; benefits are nominally fixed | Report the funding gap against a displacement path, not only against asset returns | Treating this as an asset-return problem |
| **State and local governments** | **424.1bn of wage-linked income tax, 15.93 pct of own tax receipts**, under a balanced-budget constraint in every state but Vermont | Build the rainy day fund against a wage-displacement path specifically | Assuming the federal pattern. **Their procyclical spending cut feeds the second round, and that loop is NOT in our engine** |
| **Bank supervisors and the central bank** | Second round is nine tenths of the bank channel **[S]**; demand leads in 20 of 27 cells **[R]** | The automation scenario of row 8, routed through spending, house prices and business credit, reported as a band. Plus AI-lending concentration limits, row 9 | A scenario routed through household default. It measures the wrong seventh |

### 6.2 The earnings offset, which is the largest single sensitivity

Every figure above is struck with losses hitting capital directly. **Allowing one year of
annualised net income to absorb losses first cuts the asset share in breach at the 50 percent
dose from 28.2 to 9.9 percent.** Both are reported everywhere; neither is "the" answer. A
supervisor reading only the first number would over-tighten, and one reading only the second
would assume earnings survive a scenario that is partly about earnings.

### 6.3 What the evidence does NOT support, unchanged in substance and now measured

**Wholesale changes to household mortgage underwriting at moderate displacement.** Three
measured reasons, the third new from Module A:

- The flat debt-service-to-income result is **partly mechanical**: underwriting caps DTI.
- Embodied households are **less indebted on seven of twelve debt measures** (A31), and the
  unsecured concentration result is null.
- **Mortgage portfolio lenders are among the least exposed institution types**, 0.1 percent
  breaching at a 25 percent dose against 38.9 percent of card-heavy banks.

**The retired claim stays retired.** "Occupational diversification does not hedge a mortgage
book" is withdrawn. What survives is that the risk is unpriced and uniformly spread, so the
system in aggregate cannot rotate out of it, which is an argument for disclosure.

### The fair lending constraint, legally sourced

The project brief made this binding: the claim does not enter the paper without ECOA, Fair
Housing Act and disparate impact sourcing. **It had never been sourced. It is now, and the
sourcing makes the claim more careful than the version it replaces.**

**Occupation is NOT a prohibited basis under ECOA.** 12 CFR 1002.2(z) defines prohibited
basis as "race, color, religion, national origin, sex, marital status, or age ...; the fact
that all or part of the applicant's income derives from any public assistance program; or the
fact that the applicant has in good faith exercised any right under the Consumer Credit
Protection Act". Occupation is not in that list. 12 CFR 1002.6(a) then provides that "a
creditor may consider any information obtained, so long as the information is not used to
discriminate against an applicant on a prohibited basis", and adds that "the Act does not
provide that the 'effects test' applies".

**The exposure is a discriminatory-effects claim under the Fair Housing Act, for housing
credit.** 24 CFR 100.500: "Liability may be established under the Fair Housing Act based on a
practice's discriminatory effect ... even if the practice was not motivated by a
discriminatory intent", where a practice "actually or predictably results in a disparate
impact on a group of persons ... because of race, color, religion, sex, handicap, familial
status, or national origin". It "may still be lawful if supported by a legally sufficient
justification", which requires the practice to be "necessary to achieve one or more
substantial, legitimate, nondiscriminatory interests", with burdens of proof set out in
paragraph (c).

**The corrected claim, which is what goes in the paper:**

> Occupation-based mortgage underwriting is not prohibited outright. Because occupation
> correlates with protected classes, it exposes a lender to a **discriminatory-effects claim
> under the Fair Housing Act**, on which the lender must carry a legally sufficient
> justification under a burden-shifting framework. Combined with the measured finding that
> the exposure is flat across the distribution, so that screening on it buys little, **the
> risk-adjusted case for occupation-based underwriting is weak and the case for portfolio
> disclosure is strong.**

All three citations verified against eCFR in this environment on 2026-09-20.

---

## 7. Emerging markets

**[M/S] Three facts, in the order that matters.**

1. **Imported AI capital.** If AI capital is foreign-owned the taxable surplus accrues abroad
   and domestic tau_k is effectively lower. Row 1, the tax instrument, is weaker in exactly
   the economies that need it most. This is the India contrast case.
2. **Cannot borrow freely in own currency.** B6 states it directly: a sovereign that cannot
   borrow in a currency it issues cannot absorb the shock the way the United States can, and
   **the labour backing ratio does not capture that by itself.** The ratio measures how much
   of the claim stock sits on labour income; it says nothing about what happens when that
   income falls. Row 2, pre-funding, is the only instrument that works, and it must be built
   before the dose.
3. **Often already on an unsustainable path.** The 20-year emerging-market debt baseline
   reaches **376.7 percent of GDP [R]** before any AI displacement is added. The displacement
   increment is **18.2 points of GDP** for an emerging market against **10.1** for a
   reserve-currency issuer, a ratio of **1.8**.

**[M] And the measurement itself is unavailable there.** B6 finds the ratio **not computable
to a publishable standard for India**: the RBI flow of funds has long lags and incomplete
household coverage, there is no usable whom-to-whom matrix, and high informality puts a large
share of labour income outside both the tax base and the formal credit system, which is
exactly the variable the statistic turns on. **The honest output for India is a statement
about why, not a number.** The euro area and Korea are the computable second cases.

---

## 8. State-contingent rules

Form: **if [indicator] crosses [level] for [duration], then [instrument]**. Every threshold
is labelled inside or outside the data.

| # | Rule | Current value | Inside the data? |
|---|---|---|---|
| T1 | If the **effective rate on AI surplus** stays below **0.1101** for two consecutive fiscal years while the displacement flow exceeds its median, then row 1 | **0.0708**, BELOW THRESHOLD | **INSIDE.** Both sides are observed today |
| T2 | If **prime-age nonemployment** exceeds **24.71** for two consecutive quarters, then rows 3, 5, 7 and 8 together | **19.31** | **AT THE BOUNDARY BY CONSTRUCTION.** 24.71 is the observed maximum of the fit, so crossing it is precisely the moment rho leaves the data |
| T3 | If the **annual displacement flow** exceeds **0.0273**, the median of the speed-limit specification table, for one year, then the contract instruments (5, 6, 7) pre-authorise | **0.00679** | **INSIDE**, but the threshold is a median over a range of 0.0005 to 0.0715 and is **never a single number**. State the range with the trigger |
| T4 | If the **combined OASDI depletion date** moves inside five years, then row 4 | **2034 Q3**, which is eight years out | **INSIDE.** Trustees projection, not an AI scenario |
| T5 | If the **debt-financed share of AI capex** exceeds **0.20**, then row 9 | **0.0654** | **INSIDE the historical anchors.** 0.20 and 0.50 are read off the 2000 and 2008 episodes. **LOWER BOUND on the indicator**, limitation L1 |
| T6 | If the **AI capex self-funding ratio** falls below **1.0 in aggregate**, then row 9 escalates | **1.3426**; four of nine filers already below individually | **INSIDE.** Composition is the leading indicator, not the level |
| T7 | If **auto 90+ day delinquency** rises by 2pp over four quarters while the displacement flow is above its median, then row 7 | **5.49 pct** | **INSIDE** |
| T8 | If the **employment gap for workers aged 22 to 25 in AI-exposed occupations** continues to widen for four quarters, then row 6 and row 11 | **19 pct below counterfactual, widening** | **OUTSIDE OUR DATA, inside someone else's.** Brynjolfsson, Chandar and Chen on ADP microdata. Our own engine cannot see never-hired entrants at all |
| T9 | If an embodied wage-bill dose exceeds **0.459**, then **no reemployment-based instrument can be sized** and only rows 3 and 4 remain | not reached | **THE BOUNDARY ITSELF.** 0.459 is the pole in the rho construction. Beyond it there is no admissible reemployment rate, only the band 0 to 0.49 |

**T9 is the most important row in this table and it is a statement about knowledge, not about
the economy.** Past that dose the architecture cannot be sized from this data.

---

## 9. Candidates REJECTED, and why

Rule (a) of the instruction. These were considered and are not in the table.

| rejected candidate | why |
|---|---|
| General mortgage relief for embodied households | **Rule 2.** A31: embodied households are less indebted on seven of twelve debt measures; the channel the data shows is small |
| General unsecured-credit instruments | **Rule 2.** The unsecured concentration result is null |
| Occupation-based underwriting or pricing rules | Rests on the **retired** claim that occupational diversification does not hedge a mortgage book, and collides with the fair lending analysis in section 6. Replaced by row 10, disclosure |
| The trigger dashboard as a contribution | **Priority claim dropped** in the related-work audit. An indicator list is not a research contribution and both the IMF note and the Windfall Trust report effectively propose monitoring. The dashboard stays as an artifact and is used above; it is not claimed as novel |
| Pairing every household exposure with a household-facing instrument to protect banks | **REJECTED BY MODULE A.** All such instruments together remove under 10 pct of system losses at every dose, because they act on the first round and the bank channel is the second. They are kept in the table, judged on HOUSEHOLD outcomes, and the architecture no longer implies they protect bank capital |
| Any instrument sized on the hedge ratio at the operative tau_k (0.36) | **REMOVED by the clearing pass.** Its input, `surplus`, is undefined in the brief; the replicator computed 0.5447 from a self-consistent alternative reading. **No instrument may be sized on it until `surplus` is defined** |

---

## 10. What this architecture cannot do

- **It cannot be sized past a 45.9 percent embodied wage-bill dose** (T9), because the
  reemployment rate has no admissible estimate there.
- **It cannot price the AI leg**, only bound it from below (L1). Every ownership figure in
  section 1 is an upper bound on the share and a lower bound on the dollars.
- **It cannot size the housing instrument against house prices**, because the engine holds
  them fixed and agency losses are driven by negative equity at least as much as by income.
- **It cannot see never-hired entrants** (T8). The one indicator that has been moving since
  August 2025 is one our own engine is structurally blind to, and the instrument that answers
  it, row 6, is therefore triggered on someone else's data.

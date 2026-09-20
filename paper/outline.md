# Paper outline: a measurement paper

**Target journal: OPEN, for the co-author to decide.** The centre of the paper has moved from
bank-facing to fiscal and sovereign, so a public finance or macro outlet may now fit better
than the Journal of Financial Stability, which was the original target. Journal of Public
Economics, Journal of Monetary Economics and the IMF Economic Review are all plausible.
Previously: Journal of Financial Stability, with Technological Forecasting and Social Change
as fallback.

**Status tags on every claim.** **[R] REPLICATED**, rebuilt by an instance that did not write
the code, from raw data and the brief alone, inside the project's stated tolerance.
**[M] STANDING**, measured, clears every applicable check, not independently rebuilt.
**[S] SCENARIO**, arithmetic conditional on a chosen assumption. Source of truth:
`data/release/headline_clearing_pass.csv`. Nothing outside those three tags appears in the
paper; the five removed items are listed in section 10.

**The research question, stated once.** When long-dated credit is underwritten against human
labour income, and capital that substitutes for that labour is financed separately, **who
holds each exposure, and what does a given amount of displacement do to them?**

---

## 1. Introduction. The two-sided bet, by holder

**The frame.** The financial system holds two exposures that depend on opposite assumptions.
Leg W, the wage leg, is credit serviced from labour income and implicitly assumes AI arrives
slowly. Leg A, the AI leg, is credit and equity extended against AI capital and implicitly
assumes it arrives quickly. A holder of both has offsetting positions; a holder of one does
not.

**The "only regime" claim is CUT.** The superseded text said partial success is the only
regime in which both legs are impaired at once, so it is the only regime in which the natural
hedge fails. **We never measured that**, and our own payoff table by holder shows the state
losing in all three outcomes, not only in partial success. The two-sided bet stays as
FRAMING, which is what it earns: it organises who holds what. It is not offered as a
measured proposition about regimes.

**The finding that organises the paper, and it goes in the first paragraph:**

> **The federal government is exposed, as holder, guarantor or debtor, on about 79 percent of
> the claims paid directly from wages: about 32 percent as creditor or guarantor and about 55
> percent as the debtor on Treasury debt serviced from wage taxes.** The legs overlap where it
> holds its own debt, so they do not add: union **0.794**, agreed range **0.778 to 0.804**
> [M]. **It holds about 1 percent of the claims on AI capital**, 0.010, range 0.0095 to 0.0102
> [S], and that is an **upper bound** because the AI side is on-balance-sheet only. **The gap
> is 0.784.**
>
> **Structural sensitivities beside the headline:** obligor leg excluded 0.321; agency pools
> not federal 0.587; indirectly wage-backed claims included 0.452.

| claim ID | statement | status | figure or table |
|---|---|---|---|
| `sovereign_share_union` | Federal exposure on 0.794 of directly wage-backed claims: 0.321 as creditor or guarantor, 0.552 as obligor, legs overlapping | **[M]**, agreed with an independent rebuild to within 0.016 | Table 1 |
| `ai_leg_federal_share` | The state holds 0.010 of the AI leg | **[S]** | Table 1 |
| `holder_gap` | The gap is 0.784 | **[M]** on the wage side, **[S]** on the AI side | Table 1 |
| 159 | The concentration of wage risk on the sovereign is the central result | **[M]**, strengthened; claim 195 reaches it by a second route | Figure 1 |

**What the introduction must concede immediately**, because it is the honest frame and
burying it would be worse: the sovereign share is robust to every measurement call at under
1.3 percent and **not** robust to the one-step accounting rule, which moves it from 0.794 to
0.452. **It is a robust measurement under a stated convention, and the convention does heavy
lifting.**

**Contribution, stated exactly and no more.** The fiscal mechanism is established and this
paper does not claim it. **IMF Note 2026/002 asserts the wage-leg credit mechanism and the
distributional asymmetry; RAND (Price and Suresh 2026) measures the federal revenue
exposure.** What this paper adds is five measured things and nothing else:

1. **The measured holder structure.** Who holds each leg, 0.794 and 0.010.
2. **Household losses from microdata, mapped to the Federal Reserve's own loss rates.**
3. **Incidence: who bears the loss**, by position in the wage distribution and by holder.
4. **A replicated fiscal condition with sourced parameters**, independently rebuilt.
5. **The public claims register**, with every claim's status and replication flag.

That is the whole claim. The paper must not imply more.

---

## 2. Related work

Source: `lit/related_work_final.md` and `lit/related_work_labour_backing.md`.

**What each does, plainly.**

| work | what it MEASURES | what it only ASSERTS | boundary |
|---|---|---|---|
| **Price and Suresh (2026), RAND RR-A4980-1** [full text read] | US federal revenue under AI substitution in the RAND budget model. 84 pct of 2024 revenue from individual or payroll taxes, **about 66 pct directly from labour**. Four scenarios on two axes | Policy options, explicitly "illustrative" and unsized | **No household debt, no mortgages, no bank balance sheets, no financial stability content.** Holds output constant by construction, so it is the analogue of our case A only |
| **IMF Note 2026/002 (Barhoumi and others)** [full text read] | nothing. It is a workshop synthesis under the Chatham House Rule, with no model and no numbers | **the wage-leg credit mechanism** (job losses weaken household balance sheets, raising default risks in banks exposed to consumer credit), **the AI-leg leverage mechanism**, and **the distributional asymmetry** (displacement costs fall on incumbent workers and borrowers, gains on new entrants and AI-intensive firms) | **Both legs appear in the same paragraph. Kill criterion assessed and NOT triggered**: no holder map, no hedge-failure proposition, no measurement. The closest approach located. It names the data gap this paper fills |
| **IMF SDN/2024/002 (Brollo and others)** [full text read] | corporate METRs and average tax rates on capital and labour across 74 to 85 economies; **advanced-economy capital ATR 0.20 to 0.22**; measured social-protection effects (Brollo 2024) | that capital income taxation should be strengthened; that a specific AI tax is **not** recommended | **Corroborates our sourced tau_k maximum of 0.20351 and our reading of 26 USC 168(k). AND it opens the capital tax rate exposure of section 5.1.** No household debt, no holders, no AI leg |
| **Windfall Trust (Ieong and others 2026)** | four-channel fiscal accounting for an average OECD country | | Confirmed from the publisher page: **does not address household debt, mortgages, bank balance sheets or financial stability at all** |
| **Korinek and Lockwood (2026)**, NBER 34873 | optimal taxation across two stages of AI transformation | | Ours is measurement, not optimal taxation |
| **Chen (2026)**, arXiv 2603.09209 | macro-financial stress test of rapid AI adoption, eleven predictions, reaching private credit and mortgages | | **The largest overlap, and it is with our second round.** What remains ours: severity against a named supervisory benchmark, loss rates by loan category, decomposition by holder |
| **Falk and Tsoukalas (2026)**, arXiv 2603.20617 | theory: capital income taxes cannot resolve the automation externality; a Pigouvian automation tax can | | **Stronger than our result and first.** Ours is the calibration, not the verdict |
| **Manning and others (2026)** | occupation-level adaptive capacity index; exposure and adaptive capacity POSITIVELY correlated | | **CORRECTED: overlap, not contradiction.** Same conclusion as our claim 145 on a different object. **What remains ours is the pay-level buffer finding**, which an occupation-level index cannot produce |
| **Casas and Torres (2024)** | general equilibrium, automation shifts the tax base | | Establishes the base shift two years before this project |
| **Fed DSR and Distributional Financial Accounts** | debt service over ALL income; balance sheets by wealth percentile | | **The closest existing statistic.** No labour decomposition of the servicing cash flow, and no extension beyond households |

**Connected work, named as connected and not as competition:** IMF Note 2026/002, the
Windfall Trust report (which co-designed the IMF scenario exercise) and Korinek and Lockwood
establish the framing this paper builds on.

**The boundary sentence, to appear in section 2 in exactly this form:**

> IMF Note 2026/002 asserts the wage-leg credit mechanism and the distributional asymmetry.
> RAND measures the federal revenue exposure. **This paper contributes the measured holder
> structure, household losses from microdata mapped to the Federal Reserve's loss rates,
> incidence by who bears the loss, a replicated fiscal condition with sourced parameters, and
> the public claims register.**

**The kill criterion was assessed against IMF Note 2026/002 and is not triggered**, because it
carries no holder map, no hedge-failure proposition and no measurement. It is the closest
approach located and the paper says so.

**Two priority claims already retired, stated in the paper:** the fiscal mechanism (RAND,
Casas and Torres, Korinek and Lockwood, Windfall, IMF all have it) and the trigger dashboard
as a contribution.

**Independent corroboration, reported as a strength:** our labour-linked receipts share of
**63.4 percent** against RAND's **66 percent**, and our required capital tax rate of 1.55 to
1.94 times operative against RAND's "roughly doubled". Different methods, same answers.

---

## 3. Data and method

| claim ID | statement | status | artifact |
|---|---|---|---|
| `under_reporting_factors` | Four survey under-reporting factors, with the factor-over-coverage identity holding to three decimals on every book | **[R]** | Table 2 |
| 118 | The plausibility rule: state the bound a number must respect before reporting it. **53 checks, 4 violations**, all deliberately retained superseded rows | **[M]** | Appendix table |
| 165 | 87 sealed expected values published with a replication brief, two rounds | **[M]** | `data/release/` |

**Subsections.**

3.1 The claim stock and the labour decomposition. Z.1 annual 2025, thirteen classes
enumerated with series identifiers.

3.2 Household microdata. ACS and SIPP, the working-core definition (at least one employed
member aged 25 to 64), the under-reporting correction.

3.3 The displacement engine. First round only, house prices fixed. **The lower-bound
paragraph is printed here in full and attached to every downstream table.**

3.4 **The claims register and the standing checklist.** C1 to C6, the status vocabulary, and
the separate replication flag.

3.5 **The two replication rounds.** Round one and round two, 127 quantities, 79 with sealed
counterparts, 45 within 5 percent, 28 inside tolerance. **And the honest statement of the
protocol:** the blind was procedural, not enforced; the replicator worked on the same machine
with the sealed file reachable at a path the brief names and reported it unopened until the
rebuild was final. **The claim is "independently rebuilt under a reported blind protocol",
not "independently verified".** The supporting evidence is set out and labelled
circumstantial.

3.6 **The clearing pass.** How REPLICATED, STANDING and SCENARIO are assigned, and the five
items removed.

**Figure 2:** the replication scoreboard, and the six root causes of the thirty-four
mismatches.

---

## 4. Who holds wage-backed claims

| claim ID | statement | status | figure or table |
|---|---|---|---|
| `direct_ratio` | Direct labour backing ratio **0.270271** | **[M]** | Table 3 |
| `home_mortgage_backing` | Home mortgage labour backing **0.840223**, matched exactly by the independent rebuild | **[M]** | Table 3 |
| `multifamily_backing` | Multifamily **0.72754**, matched exactly | **[M]** | Table 3 |
| `sovereign_share_union` | Sovereign union share **0.794**, range 0.778 to 0.804 | **[M]** | **Figure 1** |
| new | The Treasury class is FL313161105 + FL313169205 = 33,887.1bn, 2025 vintage, verified against three external cross-checks | **[M]** | Table 3 note |
| new | Whether the central bank counts as federal moves the share by **exactly zero** | **[M]** | Table 4 |

**4.1 The ratio and its full sensitivity.** Central 0.270271; one-at-a-time range 0.267 to
0.475. **Two things said plainly:** the one-step rule moves it **76 percent** and nothing
else moves it by more than 10; and **it is partly an asset-price series**, reading 0.376 in
2008 because equity fell, which is the wrong sign for an indicator.

**4.2 The 1952 to present series. This is Figure 1 and it is the paper's best single image.
It is a U, and reporting it from 1970 would misdescribe it.**

| year | ratio | **sovereign union share** | held or guaranteed | obligor |
|---|---|---|---|---|
| **1952** | 0.2837 | **0.5227** | 0.0853 | **0.5102** |
| **1970** | 0.2767 | **0.3356** | 0.1204 | 0.2965 |
| 1990 | 0.3549 | 0.5638 | 0.2482 | 0.3647 |
| 2008 | 0.3763 | 0.5582 | 0.2977 | 0.2859 |
| 2020 | 0.2907 | 0.7831 | **0.3923** | 0.5225 |
| **2025** | 0.2703 | **0.7936** | 0.3215 | **0.5520** |

**The ratio is flat across seventy-three years. The sovereign share of it traces a U.** The
1952 level is almost entirely **wartime Treasury debt**: the obligor leg alone is 0.510 that
year against a held-or-guaranteed leg of 0.085. It falls to 1970 as that debt shrinks against
a growing claim stock, then climbs in two datable steps: **the agency book grows 1970 to
1990** (held leg 0.120 to 0.248), then **federal debt grows 2008 to 2020** (obligor leg 0.286
to 0.522).

**Said plainly, because it qualifies the headline: a large part of the recent rise is growth
in federal debt itself rather than new exposure to households.** The held-or-guaranteed leg
peaked at 0.392 in 2020 and has since fallen to 0.321; the whole net increase since 2008 sits
in the obligor leg.

**4.3 The holder map.** Federal 32.1 pct held or guaranteed, 55.2 pct as obligor, 79.4 pct
union. Banks 18.4, rest of world 18.0, other financial 15.3.

**4.4 Robustness, Table 4.** Every measurement call under 1.3 percent. The four structural
calls that move it, with the one-step rule at -43 percent stated first.

**Placement decision, stated:** the ratio is the accounting scaffold, not the headline, and
it does not appear in the abstract as a number.

---

## 5. The fiscal condition, measured and replicated

| claim ID | statement | status | figure or table |
|---|---|---|---|
| `R_2026` | Retained wage share **0.568316** | **[R]**, reached only by discovering that the sourced part-time ratio 0.3206, not 0.50, reproduces omega | Table 5 |
| `condition_passes` | The condition **fails** at the operative rate | **[R]** | Table 5 |
| `tau_k_sourced_low` / `_high` | Sourced effective capital tax rates **0.03245** and **0.20351**, exact | **[R]** | Table 5 |
| `required_tau_k` | Required rate **0.110 to 0.137** | **[M]** | Table 5 |
| `debt_to_gdp_start` | **1.214121**, exact to six decimals | **[R]** | Figure 3 |
| `federal_student_share` | **0.972808**, exact | **[R]** | Table 6 |

**The verdict, in the only form that survives**, and it is materially weaker than the claim
it replaces (claim 168, downgraded):

> The required capital tax rate exceeds the **OPERATIVE** effective rate of 0.0708 under every
> reading, and does **NOT** exceed the top of the **SOURCED** range of 0.20351 under any
> reading. **SUPERSEDED IN 5.1: the condition is unclosable under the tax code AS IT APPLIES
> TO AI CAPITAL SPECIFICALLY. At the measured economy-wide capital rate of 0.20 to 0.22 it
> closes.**

**5.1 THE CAPITAL TAX RATE EXPOSURE. This is a subsection, not a footnote.**
Full note: `notes/tau_k_exposure.md`. **Figure 3a: `paper/figures/fig_tau_k_condition.png`.**

**The condition is a function of tau_k with a threshold at 0.110 to 0.137, and the two
defensible measurements of tau_k fall on opposite sides of it:**

| rate | value | condition |
|---|---|---|
| ours, the operative rate on the **AI surplus** | **0.0708** | **FAILS** |
| our own sourced maximum | 0.20351 | PASSES |
| IMF SDN/2024/002, measured **economy-wide** capital ATR | **0.20 to 0.22** | **PASSES** |

**The argument for each, in two paragraphs.** Ours is the rate on the AI surplus: 26 USC
168(k) expensing exempts the normal return so only the rent share of 0.351 bears tax, and 48
percent of rents are shifted abroad (Torslov, Wier and Zucman). Theirs is economy-wide and
includes personal-level taxes on dividends and realised capital gains, is an average rather
than a marginal rate, and covers a capital stock that is mostly neither fully expensed nor
shiftable.

**The number the disagreement reduces to:** between **26 and 52 percent of the AI surplus**
would have to bear the economy-wide rate rather than the AI-specific one for the condition to
close. It does not require raising the statutory rate.

**Therefore every statement of "fails under current law" is withdrawn** and replaced by "fails
under current law as it applies to AI capital specifically". The condition itself is
REPLICATED; **the verdict attached to it is PROVISIONAL**, because it rests on a base choice a
public finance economist may reasonably make differently. **This is the first question for a
public finance co-author** and is written out as such in the note.

**5.2 A correction reported against ourselves.** The sealed note attached to this result said
the required rate exceeds the top of the sourced range at every reading. Our own sensitivity
file says the opposite in all five cells. **The note overstated the finding and is
corrected.**

**5.3 Independent corroboration.** RAND reaches "roughly doubled" by a macro route; we reach
1.55 to 1.94 times operative from sourced effective rates.

---

## 6. Households by position in the wage distribution, and incidence

| claim ID | statement | status | figure or table |
|---|---|---|---|
| B5 | Labour-backed claims per unit of wage bill: **4.15 in Q1 falling to 0.65 in Q5**, a factor of 6.3 | **[M] on the gradient; the Q1 magnitude is REMOVED** | Table 7 |
| 145 | Buffers are **not monotonic in pay** | **[M]** | Figure 4 |
| 139 | Neither exposure-type contrast survives controlling for pay | **[M]** | Table 8 |
| A31 | Embodied households are less indebted on seven of twelve measures; auto is the one surviving pathway contrast, adjusted +13.39, t = 3.50 | **[M]** | Table 8 |
| 80, 93, 94 | The never-hired entrant blind spot | **[M], cautioned**, a deduction not a measurement | Section 6.3 |

**6.1 The gradient, and what is withdrawn from it.** The direction stands. **The Q1 magnitude
does not**: an independent rebuild lands 2.5 to 3.4 times away and the brief defines neither
the universe nor the normalisation of the object, so we cannot show their reading is wrong.
Published with the gradient as the claim and Q1 flagged.

**6.2 Incidence, and a claim withdrawn.** "Incidence moves household counts by 5 to 9 percent,
so the count figures are robust to it" is **REMOVED**. Under the replicator's most natural
reading of case (c) the spread is 59 percent, which removes the robustness the claim rested
on, and the brief does not say which reading is intended.

**6.3 Never-hired entrants.** Structurally invisible to this engine, which measures displaced
incumbents. The external indicators move: recent graduate unemployment 5.6 percent,
underemployment 42.0 percent, and a 19 percent employment gap for workers aged 22 to 25 in
AI-exposed occupations, widening, operating through **reduced hiring rather than increased
separations**. **Reported as a gap in our own measurement**, not as our finding.

---

## 7. The dose-response table

| claim ID | statement | status | figure or table |
|---|---|---|---|
| `terminal_loss_10pct` | Terminal-year fiscal loss **85.168bn** at the 10 pct dose | **[R]**, 0.19 pct from the independent rebuild | Table 9 |
| `federal_share_first_round` | Federal share **by dose**: 0.785 to 0.870 at 10 pct, 0.855 to 0.925 at 50 pct, narrow reading | **[M]** | Table 10 |
| `demand_event_first_share` | The demand event is **0.740741** of the first round, factorising 20/27 exactly | **[R]** | Table 11 |
| `second_round_levels` | Second-round bank losses **173 to 1,565bn**, a factor of nine | **[S]** | Table 11 |
| `terminal_loss_25pct` | 25 pct dose figures | **[S]**, embodied point estimate withdrawn | Table 9 |
| `rho_50pct` | The 50 percent reemployment rate | **REMOVED. There is no such number** | Section 7.1 |

**7.1 The extrapolation boundary, stated before any number in this section, AND stated as a
limitation of the method rather than as a finding.** The reemployment rate is a straight-line
fit extrapolated until it breaks. A referee will say so; the paper says it first.

| dose | embodied | cognitive GPT | cognitive AIOE |
|---|---|---|---|
| 10 pct | 0.613 point | 0.655 point | 0.664 point |
| 25 pct | **band** | 0.562 point | 0.598 point |
| 50 pct | **no solution** | band | band |

The reemployment rate is the fixed point of a stock-flow identity against a fitted line. That
construction has a **pole at an employment dose of 0.676**, which is a wage-bill dose of
**0.459 for the embodied group**. A point estimate is reported only where the solution lies
inside the observed range of rho, [0.49, 0.74]; elsewhere the band from the worst observed
vintage down to zero, labelled outside the data. **At 50 percent no exposure type has a point
estimate.**

**Reported against ourselves:** the superseded code enforced the bound accidentally, through
a clipped iteration, and published the clip boundary as an estimate. **672 of 2,520 cells, 27
percent, lose their point estimate.** The old value lies inside the new band in 85 percent of
them; where it does not, the old value was the boundary, so the superseded figures at large
doses **overstated** the loss.

**7.2 First round, measured.** By dose and by exposure type. The embodied group puts 6 to 11
percentage points more on the federal balance sheet at the same dose, because it is lower
paid and the payroll and benefit channels follow head counts rather than dollars.

**7.3 Second round, scenario.** Nine tenths of the bank channel. Reported as a band of 173bn
to 1,565bn; a point estimate inside that band would be false precision.

**7.4 Two non-monotonicities that a single range concealed.** The federal share **peaks at the
50 percent dose and falls back at 75**, because the fiscal component saturates while credit
losses keep growing. And the exposure type matters as much as the dose.

---

## 8. The AI-fails case, and the payoff table by holder

| claim ID | statement | status | figure or table |
|---|---|---|---|
| `ai_leg_federal_share` | Federal share of the AI leg **0.0095 to 0.0102** across a threefold variation in the assumed scale | **[S]**, robust on its only axis | Table 12 |
| new | The nine named SEC filers: capex 490.9bn, OCF 659.1bn, self-funding 1.3426, debt-financed share of capex 0.0654 | **[M]** | Table 12 |
| new | The structure **resembles 2000, not 2008** | **[M]**, LOWER BOUND | Table 13 |
| `hedge_ratio_at_operative` | Share of the federal wage loss hedged | **REMOVED**, the input `surplus` is undefined | Section 8.3 |

**8.1 The AI leg, measured and bounded.** Nine named filers, the selection rule stated, and
NBIS named as an exclusion (a foreign private issuer filing no us-gaap facts). **Everything
here is on-balance-sheet Tier 2 only**, so it is a labelled lower bound and the 5 percent kill
criterion is not evaluable.

**8.2 The payoff table by holder**, the hedge failure proposition made empirical. Holders on
both legs: banks (18.4 pct of the wage leg, 3.2 pct of the AI leg), insurers, pensions, rest
of world. **The state is on one leg only, at 79.4 and 1.0 percent.**

**8.3 Two historical anchors, verified.** 2000 to 2002 equity-financed: receipts fell 9.5
percent. 2007 to 2009 debt-financed: receipts fell 16.0 percent, corporate tax receipts 53.4
percent. The current debt-financed share of AI capex, 0.0654, sits near the 2000 pattern.
**Watch composition, not level:** four of nine filers are already below a self-funding ratio
of 1.0 while the aggregate is 1.34.

---

## 9. Institutional architecture, derived from the holder gap

Full deliverable: `framework/architecture.md`. Twelve instruments, one row each, with the
institution that must act, the type, a verified precedent, a trigger with its current
dashboard value, and the regime in which it binds.

**9.1 The gap, and what ownership alone would cost.** Closing a tenth of the gap requires a
stake of 1,486bn, which is eight times the entire capital of the housing agencies. **That is
why most of the instruments are not ownership instruments.**

**9.2 The taxation argument, softened.** Break-even **0.125 to 0.301 with output preserved**
and **0.182 to 0.650 with output falling** [S]. At moderate displacement the required rate is
inside observed effective rates; at large displacement it is not, **so ownership, dividend
and direct-claim instruments grow in importance with the dose**. **One hard constraint:
replacement income funded from a capital tax cannot repair the payroll-funded trust funds,
because it is not covered wages.**

**9.3 Banks and lenders.** Supported: an automation scenario in supervisory stress tests
routed through spending, house prices and business credit and reported as a band;
AI-lending concentration limits; displacement-contingent payment clauses; auto and student
exposure. **Not supported: wholesale changes to household mortgage underwriting at moderate
displacement.** The fair lending constraint is now legally sourced: occupation is **not** a
prohibited basis under ECOA (12 CFR 1002.2(z), 1002.6(a)); the exposure is a
**discriminatory-effects claim under the Fair Housing Act** (24 CFR 100.500) on which the
lender must carry a legally sufficient justification.

**9.4 Housing agencies.** Rebuilt loan class by loan class from the 2025 Form 10-Ks. **39 to
53 percent of each single-family book carries no credit enhancement.** Private cover transfers
only 11 to 15 percent of an agency loss at small doses. **Zero Treasury draw at every dose.**
The instrument is pre-authorised forbearance on a displacement trigger (CARES Act sections
4022 and 4023) plus enhancement on the unenhanced book, not recapitalisation.

**9.5 Emerging markets.** Imported AI capital, so domestic tau_k is effectively lower; cannot
borrow freely in own currency; often already on an unsustainable path, with a 20-year baseline
of 376.7 percent of GDP before any displacement and a displacement increment 1.8 times that of
a reserve-currency issuer. **And the measurement itself is unavailable there:** B6 finds the
ratio not computable to a publishable standard for India.

**9.6 State-contingent rules**, nine of them, each with its current dashboard value and an
inside or outside data label. **T9 is the most important and it is a statement about
knowledge, not the economy:** past a 0.459 embodied dose the architecture cannot be sized from
this data.

---

## 10. Limitations

Five stated limitations, one paragraph each, from `data/release/stated_limitations.csv`:
**L1** off-balance-sheet and GPU-backed AI financing unmeasured; **L2** capital gains receipts
unsourced; **L3** the labour backing ratio's novelty is "none located" pending a systematic
PRISMA search; **L4** the holder proxy residual, 24.88 percent of the mortgage book treated as
private in full; **L5** effective labour tax rates by income not taken from CBO.

**Plus the five removed claims, listed with reasons**, because a reader is entitled to know
what was cut: the incidence count-robustness claim, the 50 percent reemployment rate, the
hedge ratio at the operative rate, the bottom-quintile magnitude, and the two cognitive index
scores.

**Plus three method limitations. The first is the extrapolation boundary.** Above about 25
percent displacement our estimates become bands, because the reemployment rate is a
straight-line fit extrapolated until it breaks: it has a pole at a 45.9 percent
physically-exposed displacement level and no point estimate exists outside the observed range
[0.49, 0.74]. **This is a limit of the specification, not a fact about the economy**, and it
is stated that way wherever it appears rather than presented as a finding. The replication
blind was **procedural, not enforced**: the
replicator worked on the same machine with the sealed file reachable at a path the brief
names, so the claim is "independently rebuilt under a reported blind protocol", not
"independently verified". And **the capital tax base is contested**, which is what section 5.1
sets out: the fiscal verdict turns on whether the rate is the marginal one on AI surplus or
the economy-wide average, and both are correctly computed.

---

## 11. Conclusion

Three sentences, and no more:

1. **The federal government is exposed, as holder, guarantor or debtor, on about four fifths
   of the claims paid directly from wages, about a third as creditor or guarantor and about
   fifty-five percent as the debtor, and holds about one percent of the claims on AI capital.**
   It bears the exposure that fails if AI succeeds and has almost no stake in the one that pays.
2. **At the one dose fully inside the observed data, ten percent of the wage bill, the federal
   government bears roughly four fifths of first-round losses**, and closing the fiscal
   condition would require between a quarter and a half of the AI surplus to bear the
   economy-wide capital rate rather than the much lower rate AI capital actually faces.
3. **Who bears the loss depends on how automation arrives, and the budget does not notice
   the difference.** Savings buffers are thinnest in the second wage quintile, not the first;
   the gap between physically and cognitively exposed households is a pay effect rather than
   an exposure effect; and when automation works through non-hiring rather than layoffs the
   losses move onto younger borrowers with student and car debt while the fiscal loss is
   unchanged.

---

## Figures and tables

| # | Content | Section |
|---|---|---|
| **Figure 1** | The labour backing ratio and the sovereign share of it, **1952 to 2025**, two panels, with the sovereign share split into its held-or-guaranteed and obligor legs so the U and its composition both read | 4.2 |
| Figure 2 | Replication scoreboard and the six root causes | 3.5 |
| **Figure 3a** | **The fiscal condition as a function of tau_k, with both rates marked** | **5.1** |
| Figure 3 | Debt paths, reserve-currency issuer against emerging market | 5 |
| Figure 4 | Liquid buffers against pay, showing non-monotonicity | 6.1 |
| Figure 5 | The exposure frontier: share of the wage bill exposed as a function of capability c | 3.2 |
| **Table 1** | **The two-sided bet by holder: wage leg share, AI leg share, gap** | 1 |
| Table 2 | Under-reporting factors and coverage shares | 3 |
| Table 3 | The thirteen claim classes, levels, backing shares, Z.1 series | 4.1 |
| Table 4 | Sovereign share robustness: measurement calls against structural calls | 4.4 |
| Table 5 | The fiscal condition: R, tau_l, tau_k, required rate | 5 |
| Table 6 | Holder shares by claim class | 4.3 |
| Table 7 | Labour-backed claims per unit of wage bill, by quintile | 6.1 |
| Table 8 | Household obligations by exposure type, raw and pay-controlled | 6.1 |
| **Table 9** | **The dose-response table, with the inside-the-data boundary marked** | 7 |
| Table 10 | Federal share of first-round losses by dose and exposure type | 7.2 |
| Table 11 | Second round: demand event share and bank loss band | 7.3 |
| Table 12 | The AI leg: nine filers, capex, self-funding, holder shares | 8.1 |
| Table 13 | Historical anchors: 2000 to 2002 and 2007 to 2009 | 8.3 |
| **Table 14** | **The instrument table: twelve rows, trigger, current value, regime** | 9 |
| Table 15 | The agency book by credit enhancement class | 9.4 |

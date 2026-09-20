# The two-sided bet: full claims dossier

Appendix to `notes/CLAIMS_SUMMARY_one_page.md`, which is the one-page version. For a
prospective co-author. Status as of 2026-09-20. Source of truth for every tag:
`data/release/headline_clearing_pass.csv`.

**Tags. [R] REPLICATED**: rebuilt by an instance that did not write the code, from raw data
and a published brief alone, inside our stated tolerance. **[M] STANDING**: measured, clears
every applicable check, not independently rebuilt. **[S] SCENARIO**: arithmetic conditional
on a chosen assumption.

---

## The central finding

> **The federal government is exposed, as holder, guarantor or debtor, on about four fifths of
> the claims paid directly from wages, and holds about one percent of the claims on AI
> capital.**
>
> Sovereign UNION share of labour-backed claims **0.794** (agreed range **0.778 to 0.804**)
> **[M]**. It is a union of two legs that overlap and therefore do not add: **0.321 held or
> guaranteed** (agency mortgage guarantees, the student loan book, central bank holdings) and
> **0.552 as obligor** (Treasury debt serviced from wage taxes), less a **3,226.4bn overlap**
> where the federal sector holds its own debt. Naive sum 0.874; union 0.794.
>
> Federal share of claims on AI capital **0.010** (range 0.0095 to 0.0102) **[S]**, and an
> **UPPER bound**: the AI side is measured from on-balance-sheet filings only, so adding the
> unmeasured off-balance-sheet financing would enlarge the denominator and lower the share.
> **The gap is 0.784.**
>
> **Structural sensitivities, reported beside the headline:** obligor leg excluded **0.321**;
> agency pools not treated as federal **0.587**; indirectly wage-backed claims included
> **0.452**; commercial mortgage treated as rent-serviced **0.741**.

The financial system holds two exposures resting on opposite assumptions about labour. The
state is the residual holder of the one that fails if AI succeeds, and holds almost none of
the one that pays if it does. **It is largely unhedged: its only claim on the AI leg is
whatever capital tax reaches it.** That claim is real but small and we could not size it: the
0.36 hedge ratio was withdrawn because one of its inputs was never defined, not because the
claim is zero.

**The honest qualification, which belongs in the same breath.** The share is robust to every
*measurement* call at under 1.3 percent, including the entire Treasury-definition question.
It is **not** robust to the one-step accounting rule, which moves it to **0.452**. It is a
robust measurement under a stated convention, and the convention does heavy lifting.

**What this paper claims, exactly and no more.** The fiscal mechanism is established
literature and we do not claim it. **IMF Note 2026/002 asserts the wage-leg credit mechanism
and the distributional asymmetry; RAND measures the federal revenue exposure.** Our
contribution is five measured things: **the measured holder structure; household losses from
microdata mapped to the Federal Reserve's loss rates; incidence by who bears the loss; a
replicated fiscal condition with sourced parameters; and the public claims register.**

---

## The debt-only labour backing ratio, NEW this session

The all-claims ratio has corporate equity at market value at **48.2 percent** of its
denominator, so it is partly an asset-price series: **0.271 at the 2000 equity peak, 0.377 in
2008 after the crash**. The debt-only ratio excludes market-valued equity classes and asks
the cleaner question.

| denominator | direct | including indirect |
|---|---|---|
| all claims | 0.270 | 0.475 |
| **DEBT ONLY** | **0.522** | **0.602** |

**It is the better statistic on both tests.** Stability over 1952 to 2025: coefficient of
variation **0.051 against 0.094**. Robustness to the largest judgement call: the one-step
rule moves it **15.4 percent against 75.7**.

| year | debt-only direct | all-claims direct | equity share of all claims |
|---|---|---|---|
| 1952 | 0.5208 | 0.3942 | 0.243 |
| 1970 | 0.4520 | 0.2996 | 0.337 |
| 1990 | 0.4600 | 0.3608 | 0.216 |
| 2000 | 0.4687 | **0.2705** | 0.423 |
| 2008 | 0.5006 | **0.3772** | 0.246 |
| 2020 | 0.5037 | 0.2895 | 0.425 |
| 2025 | **0.5216** | 0.2703 | 0.482 |

**Status [M], PROVISIONAL** until the next promotion pass: a new construction, not
independently rebuilt. Code `framework/labor_backing/build_debt_only.py`; six new bounds
added to the plausibility audit, all passing.

---

## Seven supporting results

| # | Result | Status |
|---|---|---|
| 1 | **The sovereign share is U-SHAPED, not a rise, and the whole path must be reported.** Sovereign union share **0.523 in 1952**, **0.336 in 1970**, 0.564 in 1990, 0.558 in 2008, 0.783 in 2020, **0.794 in 2025**. The 1952 level is almost entirely **wartime Treasury debt**: the obligor leg alone was 0.510 that year while the held-or-guaranteed leg was 0.085. It falls to 1970 as that debt shrinks against a growing claim stock. Two datable drivers on the way back up: the **agency book grows 1970 to 1990** (held leg 0.120 to 0.248), then **federal debt grows 2008 to 2020** (obligor leg 0.286 to 0.522). **Part of the recent rise is growth in federal debt itself rather than new exposure to households**, and the held leg has in fact FALLEN since 2020, from 0.392 to 0.321. Through all of it the direct labour backing ratio moves between 0.267 and 0.376 with no trend | **[M]** |
| 2 | **The fiscal condition is a FUNCTION of the capital tax rate, with a threshold at 0.110 to 0.137.** Retained wage share **R = 0.568316**. It **fails at 0.0708**, the operative rate on the AI surplus after 168(k) expensing and profit shifting, and **passes at 0.20 to 0.22**, the IMF's measured economy-wide capital rate. **Closing it needs 26 to 52 percent of the AI surplus taxed at the economy-wide rate.** The old claim that it is "unclosable under the tax code as it stands" is WITHDRAWN and replaced by "as the code applies to AI capital specifically" | **[R]** on R and the boolean; **PROVISIONAL** on the verdict, which depends on the tax base chosen |
| 3 | **The federal government bears roughly four fifths of first-round losses, and the share depends on the dose.** Narrow reading: **0.785 to 0.870 at a 10 percent dose**, rising to 0.855 to 0.925 at 50 percent, then falling back at 75 percent. Conservatorship reading is 8 to 10 points higher | **[M]**; the independent rebuild's 0.78 rising to 0.90 sits inside our range at both ends |
| 4 | **The housing agencies absorb a wage shock without reaching the Treasury.** Rebuilt from the 2025 Form 10-Ks: **39 to 53 percent of each single-family book carries no credit enhancement**; private cover transfers only **11 to 15 percent** of an agency loss at small doses; **zero Treasury draw at every dose from 5 to 75 percent** (179.4bn of capital against a maximum retained first-round loss of 109.0bn). **First round only, house prices fixed** | **[M]** |
| 5 | **Demand leads the other channels in 20 of 27 grid cells**, 0.740741 exactly. This is a count of how often demand leads across the grid | **[R]** |
| 5b | **Roughly nine tenths of bank losses arrive through the second round** rather than through displaced borrowers defaulting on their own loans, and second-round bank losses span a factor of nine, **173bn to 1,565bn**. This is a DIFFERENT quantity from 5: it is a share of losses, not a count of cells, and it is conditional on an assumed path | **[S]** |
| 6 | **Households, from survey microdata, and this is where contributions 2 and 3 live.** Savings buffers are thinnest in the **SECOND** wage quintile, not the first: median runway 0.84 months, 55.1 percent under one month. Differences between physically and cognitively exposed households are **a pay effect**: between 1.0 and 11.4 percent of the raw gap survives reweighting on pay, and the SIPP GPT contrast reverses sign. When automation works through **non-hiring** rather than layoffs, the composition of private losses shifts to younger borrowers: at 10 percent displacement student losses rise 37 to 43 percent and auto losses 18 to 21 percent, mortgage losses fall 15 to 32 percent, **and the fiscal loss is identical to the last cent** (98.67bn embodied, 89.96bn AIOE, 112.37bn GPT, unchanged across all three incidence cases) | **[M]** on buffers and incidence; the pay effect's DIRECTION was independently confirmed in all eight cells, its magnitudes mismatched |
| 7 | **A boundary on our own method, reported as a limitation not a finding.** The reemployment rate is a straight-line fit extrapolated until it breaks: it has a pole at a 45.9 percent embodied displacement level, and a point estimate exists only inside the observed range [0.49, 0.74]. **Above about 25 percent displacement the estimates become bands, the physically-exposed group first; at 50 percent none of the three groups has a point estimate.** A referee will say this is a limit of the specification rather than a fact about the economy, and they will be right | **[M]**, and treated as a limitation throughout |

---

## What has been independently replicated

Two rounds, the second scoring **127 quantities**, 79 with sealed counterparts, **45 within 5
percent and 28 inside our own tolerance**, by an instance that read no project code.

**Reproduced exactly or near-exactly:** `R_2026` 0.568315 against 0.568316; both sourced
capital tax rates; debt to GDP start 1.214121 to six decimals; the emerging-market 20-year
baseline 376.74 percent; the federal student share 0.972808; the demand event share 0.740741;
all four under-reporting factors and coverage shares; the terminal fiscal loss at the 10
percent dose to 0.19 percent; and **home mortgage and multifamily labour backing to the last
published digit, rebuilt independently from ACS mortgage service and gross rent**.

**Near miss on the central object.** The sovereign union share: ours 0.793592, theirs
0.777810, a 1.99 percent gap that decomposes to 83.7 percent the Treasury class (they could
not know it was two Z.1 series summed), 6.6 percent a class they omitted, and the remainder
household balances.

**The protocol, stated plainly.** The blind was **procedural, not enforced**. The replicator
worked on the same machine; the sealed file was reachable at a path the brief itself names,
was not attached to the request, and is reported unopened until the rebuild was final. The
supporting evidence is internal and circumstantial: eleven of twelve insufficiencies were
written before opening, four of six mismatch root causes were among them, and they declined to
use three sealed coefficients the brief had leaked. **The claim is "independently rebuilt
under a reported blind protocol", not "independently verified."**

**Independent external corroboration, from a different direction.** RAND (Price and Suresh
2026) put **66 percent** of federal revenue as directly labour-derived; we get **63.4
percent** from a bottom-up SOI construction. They conclude corporate tax rates would need to
be "roughly doubled"; we get **1.55 to 1.94 times** the operative rate. Neither saw the other.

---

## What was withdrawn

| withdrawn | why |
|---|---|
| **The 50 percent reemployment rate** | There is no such number. Past the pole the construction has no admissible solution; the superseded code clipped it to zero and published the boundary as an estimate |
| **"Incidence moves household counts by 5 to 9 percent, so counts are robust to it"** | Not reproducible. The natural alternative reading of one case gives 59 percent, which removes the robustness the claim rested on |
| **The bottom-quintile labour-backed ratio, 4.15** | The independent rebuild lands 2.5 to 3.4 times away and we cannot show their reading is wrong, because we never defined the object's universe. **The gradient survives; the magnitude does not** |
| **The hedge ratio at the operative tax rate, 0.36** | Its input, `surplus`, is undefined in our own brief |
| **The two cognitive index scores by occupation** | Eleven mismatches running in opposite directions on the two indices. The wage machinery passes its controls; the index scores are unsettled |
| **"29.7 percent of GSE net worth"** | It was a gross loss struck before any risk transfer. Replaced by a retained loss of 11.9 to 29.2 percent at the same dose |
| **"The fiscal condition fails under current law"** | **WITHDRAWN this pass.** It fails under current law *as it applies to AI capital specifically*, at 0.0708. At the IMF's measured economy-wide capital rate of 0.20 to 0.22 it passes. The condition is a function of tau_k, not a verdict |
| **"No reading of the corporate tax literature makes the break-even rate available"** | False. It is inside the sourced range in 10 of 15 cells. Narrowed to a statement about the operative rate |
| **"Occupational diversification does not hedge a mortgage book"** | Overreach. A flat distribution does not stop an individual lender selecting low-exposure borrowers |
| **Priority on the fiscal mechanism** | RAND, Casas and Torres, Korinek and Lockwood, Windfall and the IMF all have it. **We did not discover it and must not imply that we did** |
| **The trigger dashboard as a contribution** | An indicator list is not a research contribution. It stays as an artifact |

---

## Known limitations

1. **Off-balance-sheet and GPU-backed AI financing is unmeasured.** The AI leg is nine SEC
   registrants' on-balance-sheet facts. BIS identifies SPV structures as dominant and none
   appear. **Every AI-leg level is a lower bound and the state's share of it an upper bound.**
2. **Capital gains receipts are unsourced.** The labour-linked receipts share does not
   separate realised gains inside AGI. The headline is insensitive to it (0.71 percent); the
   fiscal magnitudes are more sensitive and we have not bounded that.
3. **The labour backing ratio's novelty is "none located", not "none exists."** No systematic
   PRISMA search has been run for that specific question. We have already retired one
   priority claim after a non-systematic search found prior work.
4. **The holder proxy residual.** 24.88 percent of the mortgage book, 3,259bn, is an
   arithmetic remainder treated as private in full. Conservative for our claim, but
   unidentified.
5. **Effective labour tax rates by income are not from CBO.** A single economy-wide rate,
   flat across the wage distribution. We have not signed or bounded the net effect.
6. **First round only, house prices fixed.** Every credit loss is a floor, not an estimate.
7. **The replication blind was procedural, not enforced.** The replicator worked on the same
   machine with the sealed file reachable at a path the brief names. The claim is
   "independently rebuilt under a reported blind protocol", not "independently verified".
8. **The capital tax base is contested and the fiscal verdict turns on it.** The condition
   fails at our 0.0708 and passes at the IMF's measured 0.20 to 0.22. Both are correctly
   computed on different bases. This is limitation and open question at once, and it is the
   first thing a public finance co-author should attack.

---

## Module A: institutions, from 8,612 balance sheets

**MEASURED**: 4,313 FDIC-insured banks and 4,299 credit unions at 2026-06-30, loan book by
category and capital for each. 26,753.0bn and 2,522.7bn of assets. **SCENARIO**: every loss
application above the inside-data level.

**Plausibility violation, caught by the baseline check.** 53 institutions breached with zero
losses applied; 17 banks report neither tier 1 nor equity and are insured US branches of
foreign chartered institutions whose capital sits at the parent. Excluded, exclusion stated
(24 institutions, 263.2bn). **Baseline now 29 institutions, 0.029 percent of assets.**

| dose | breaching | pct of assets | with one year of earnings |
|---|---|---|---|
| baseline | 29 | 0.03 | |
| **10 pct** | **54** | **0.04** | 0.04 |
| 25 pct | 246 | 4.02 | 1.55 |
| 50 pct | 1,448 | 28.20 | **9.93** |

**Card-heavy lenders most exposed** (38.9 pct breaching at 25 pct, 77.8 at 50); credit unions
the only class with stress at 10 pct; **mortgage portfolio lenders among the least, 0.1 pct
at 25 pct.**

**Household relief does not protect bank capital.** Forbearance, IDR and wage insurance
together remove under 10 percent of system losses at every level, because at the 10 percent
level only 27bn of 205bn is first-round. Enhanced wage insurance costs 314bn to remove 12.9bn
of bank losses. **They still cut assets in breach from 4.02 to 1.48 percent at 25 percent.**

**Institutions previously omitted.** State and local government, 424.1bn of wage-linked income
tax, 15.93 percent of own receipts, balanced-budget constrained, **and its procyclical
spending cut feeds the same demand channel, a loop not in the engine.** Pension funds,
contributions a share of covered payroll against nominally fixed benefits. Insurers and
private credit, the latter inseparable from the Z.1 aggregate so 6,186.9bn is an upper bound.

---

## Module B: the AI bust

**A large fiscal event and a small credit event.** Wage-bill equivalent 0.12 to 0.84 percent,
**12 to 80 times weaker** than the 10 percent displacement case; household credit losses 0.8
to 5.4bn against 30.7bn. But federal receipts fall **569 to 955bn** on the verified episodes,
through capital gains and corporate tax.

**Why it transmits weakly is measured**: the top 1 percent hold **50.9 percent** of corporate
equity and the bottom half 0.58, so the shock lands where the propensity to consume is
lowest. GDP falls 0.34 to 1.69 percent against the Fed severely adverse 4.6.

**The financing verdict is CONDITIONAL.** 0.0654 on the nine filers' books, but it leaves the
2000 pattern at **66.1bn** of additional debt-financed capex, which is 14.7 percent of the
450bn of identified bank commitments, of which roughly **162bn is already drawn**.
Off-balance-sheet financing is unsourced and BIS calls it dominant.

**The payoff table.** Only the federal government and banks lose in every column; households
gain 0.324 under success. **But the table scores HOLDINGS and so understates the state,
whose claim on the AI upside is fiscal, not proprietary.**

**Two caveats stated.** The marginal propensity to consume out of wealth is an assumption
checked against two episodes, not a sourced parameter. The credit-led GDP path is understated
because bank-channel damage is not fed back into it.

---

## Disclosure

**The pipeline and analysis were built with Claude Code. The design was reviewed with Claude.
The analysis was replicated by separate instances.**

---

## Where the work stands

The pipeline rebuilds from raw data in one command. Two replication rounds are complete with
127 scored quantities. The plausibility audit runs 53 checks with 4 violations, all
deliberately retained superseded rows. The claims register carries every claim with its status
and a separate replication flag. **The measurement is done; the manuscript is not written.**

**THE FIRST QUESTION FOR A PUBLIC FINANCE CO-AUTHOR.** Is 0.0708 the right rate for this
condition, or is it the wrong base? We compute the effective rate on the marginal dollar of US
AI surplus as 0.0708 (21 percent statutory, normal return exempted by 168(k) expensing at a
rent share of 0.351, 48 percent of rents shifted offshore). IMF SDN/2024/002 measures an
economy-wide capital ATR of 0.20 to 0.22 including personal-level taxes on dividends and
gains. Required is 0.110 to 0.137, so the condition fails on ours and passes on theirs. Is the
marginal-on-AI-surplus base right for a revenue replacement question? Is the 48 percent haven
share right for AI rents, which are unusually intangible and so if anything more shiftable?
Full statement in `notes/tau_k_exposure.md`.

**The single most useful thing a co-author could do**: run a systematic PRISMA search on the
labour backing question (limitation 3), and define the two objects the replicator could not
reproduce because we never specified them, B5's universe and `surplus` in the hedging
construction.

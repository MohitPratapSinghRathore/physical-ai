# GATE REPORT, MODULE A. Financial institutions, by institution.

Code and outputs: `framework/institutions/`. Balance sheets MEASURED; every loss application
SCENARIO.

---

## PART 1. PLAUSIBILITY VIOLATIONS

### 1.1 Fifty-three institutions "breached" the capital minimum with ZERO losses applied

The baseline check, run before any result was read, found **53 institutions below the
regulatory minimum with nothing applied to them**, holding 0.93 percent of system assets. The
largest showed **tier 1 capital of exactly 0.0 against 58.4bn of assets**, which is not a
balance sheet.

**Cause.** 17 banks report neither tier 1 capital nor total equity in the FDIC API, and my
fetch filled the missing field with zero. They are almost entirely `BKCLASS = OI`, **insured
US branches of foreign chartered institutions**, whose capital is held at the foreign parent
and is therefore outside FDIC reporting by construction. Seven credit unions likewise report
no net worth.

**Status: FIXED.** They are excluded from the capital test, the exclusion is reported with
its size (24 institutions, 263.2bn of assets), and the baseline is now **29 institutions,
0.338 percent of institutions and 0.029 percent of assets**, which is the ordinary tail of
thinly capitalised small institutions rather than an artefact.

**Every breach figure in this module is therefore a figure ABOVE a baseline of 29.** The
baseline is printed alongside the results, not buried.

### 1.2 No other violations

Category totals reconcile against the independent Z.1 aggregates the project already uses:
bank credit card holdings are 1,189.6bn against a Z.1 card book of 1,324.3bn, a **89.8
percent bank share against the project's independently benchmarked 0.875**. Bank plus credit
union auto is 1,041.6bn of a 1,562.2bn Z.1 book, 67 percent, with the remainder at captive
finance companies and in securitisations, which is where it should be. No institution is
allocated a loss exceeding its holdings of that category.

---

## PART 2. THESIS-WEAKENING RESULTS

### 2.1 THE BIG ONE. Household-facing instruments cannot protect bank balance sheets

**Every household-facing instrument, and all of them together, removes under 10 percent of
system losses at every displacement level.**

| dose | best single instrument | ALL TOGETHER, loss removed | fiscal cost of the package |
|---|---|---|---|
| **10 pct** | enhanced wage insurance, 6.28 pct | **9.61 pct** | 317.6bn |
| 25 pct | enhanced wage insurance, 6.06 pct | **8.91 pct** | 946.8bn |
| 50 pct | enhanced wage insurance, 5.57 pct | **7.59 pct** | 2,798.5bn |

**The reason is structural and it follows from a result the paper already has.** Household
instruments act only on the FIRST round, which is displaced borrowers defaulting on their own
loans. At the 10 percent dose that is about 27bn of a 205bn total; the other 178bn is the
second round, arriving through spending, house prices and business credit from people who
were never displaced. **Eliminating household default entirely would remove at most about a
seventh of the loss.**

**This weakens the architecture's implicit logic**, which paired each measured household
exposure with a household-facing instrument. It does not weaken the instruments. It relocates
what they are for:

> **Forbearance, income-driven repayment and wage insurance should be judged on household
> outcomes, not on bank capital. Judged on bank capital they are close to useless. The
> instrument that protects bank capital is one that acts on the second round, on demand, or
> on the buffer itself.**

Enhanced wage insurance costs **314bn to remove 12.9bn of bank losses** at the 10 percent
dose. Read as bank protection that ratio is absurd; read as income protection for displaced
households it is the point of the programme. **The paper must not let the first reading
stand.**

### 2.2 The instruments do still reshape the distribution, which is the case for them

Aggregate loss removed is small, but the tail moves. At the 25 percent dose the combined
package takes assets in breach from **4.02 percent to 1.48 percent** and stops **123
institutions** breaching. At 50 percent it stops 547. **So the instruments matter for who
fails, not for how much is lost**, and that is a real and defensible claim.

### 2.3 Mortgage lenders are among the LEAST exposed business models

At every dose, **mortgage portfolio lenders and commercial real estate heavy banks breach
least**. At the 25 percent dose, 0.14 percent of mortgage portfolio lenders breach against
**38.9 percent of card-heavy banks**.

This corroborates two things the project already retired or narrowed: the withdrawn claim
that occupational diversification does not hedge a mortgage book, and the A31 finding that
embodied households are less indebted on seven of twelve measures. **The mortgage channel
that motivated the original project design is the weakest of the household channels at
institution level too.**

### 2.4 Three institution types the paper omitted, and one of them has a feedback loop we do not model

**State and local government** is exposed through its own tax base, not a loan book:
**424.1bn of wage-linked income tax, 15.93 percent of its own tax receipts**. It cannot run
the deficit through, because every state but Vermont has a balanced-budget requirement. **A
revenue fall therefore becomes a procyclical spending cut, which feeds the same demand
channel that drives nine tenths of the bank losses.** That loop is not in the engine and is
recorded as an omission rather than estimated.

**Pension funds** are exposed on both sides in opposite directions: benefits are fixed in
nominal terms, contributions are a share of covered payroll. Displacement widens the funding
gap mechanically, with no change in asset returns, and the employer that must close it is
often the same balanced-budget government above.

**Insurers and private credit** are the population to which the hedge failure proposition
most directly applies. **Private credit cannot be separated from the Z.1 other-financial
aggregate**, so 6,186.9bn is an upper bound by a wide and unknown margin.

---

## PART 3. RESULTS THAT STAND

**MEASURED.** 4,313 FDIC-insured banks and 4,299 credit unions at 2026-06-30: **26,753.0bn
and 2,522.7bn of assets, 2,332.3bn of tier 1 capital and 288.3bn of net worth.** Loan books by
category for every one of them.

**SCENARIO, the distribution.** At the **10 percent dose, which is the only one inside the
observed data, the banking system barely moves**: 54 institutions breach against a baseline of
29, and **0.04 percent of system assets**. The distribution only opens up above 25 percent.

| dose | institutions breaching | pct of system assets | with one year of earnings first |
|---|---|---|---|
| baseline | 29 | 0.03 | |
| **10 pct** | **54** | **0.04** | 0.04 |
| 25 pct | 246 | 4.02 | 1.55 |
| 50 pct | 1,448 | 28.20 | **9.93** |
| 75 pct | 1,699 | 50.64 | **10.80** |

**One year of earnings roughly thirds the asset share in breach at large doses**, from 28.2
to 9.9 percent. That is the single largest sensitivity in the module and it is reported
alongside every headline.

**The exposed business models, in order.** Card-heavy first and by a distance, then credit
unions, then auto-heavy and C and I heavy, with commercial real estate heavy and mortgage
portfolio lenders last:

| business model | n | assets bn | pct breaching at 25 pct | at 50 pct |
|---|---|---|---|---|
| **card-heavy** | 18 | 1,257.6 | **38.9** | **77.8** |
| credit unions | 4,292 | 2,522.6 | 5.4 | 28.1 |
| auto-heavy | 25 | 350.1 | 0.0 | 36.0 |
| C and I heavy | 97 | 184.8 | 1.0 | 33.0 |
| commercial real estate heavy | 784 | 1,277.8 | 0.1 | 5.2 |
| mortgage portfolio lender | 702 | 522.0 | 0.1 | 3.9 |
| diversified | 2,670 | 22,897.6 | 0.2 | 4.5 |

**Credit unions are the only class showing any stress at the 10 percent dose** (1.12 percent
of them), because their book is almost entirely household credit with no C and I or
commercial real estate to dilute it.

---

## PART 4. LIMITATIONS OF THIS MODULE

1. **Dispersion here is business mix only.** Losses are allocated pro rata within a category,
   so every lender in a category takes the same loss rate. The Federal Reserve's own stress
   test reports wide within-category ranges across banks (cards 9.5 to 22.7 percent, C and I
   3.4 to 48.5). **The dispersion reported is therefore a LOWER bound on the true dispersion.**
2. **First-lien and home equity cannot be separated for banks.** The FDIC API exposes no
   revolving open-end split, so `LNRERES` is both. Credit unions do report the split, which
   is why the asymmetry is visible in the data and stated here.
3. **No institution is named**, per the instruction, and the pro-rata rule would not support
   naming one anyway.
4. **Credit union earnings were not extracted**, so the earnings-offset sensitivity applies
   to banks only and understates the offset for the system.
5. **The state and local feedback loop is not modelled**, only named.
6. **The linear pass-through in A4.** Household losses are scaled linearly with the income
   shortfall, which understates what wage insurance removes at small doses and overstates it
   at large ones, because real default is convex in the gap.

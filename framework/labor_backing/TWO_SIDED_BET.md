# B11 and B12. The two-sided bet by holder, and the payoff table across AI outcomes

**PROVISIONAL. Produced in one session. Never independently replicated.** The AI equity
SCALE is a SCENARIO parameter throughout and is labelled as one at every appearance. The
AI debt figures and the bank commitments are sourced. Off-balance-sheet and SPV financing
is **not sourced**, so **every failure-state figure below is a lower bound.**

---

# B11. The two legs on one holder axis

## What is on each side

**The wage leg** is the labour-backed claim stock from B1 and B3: 40,380bn dollars, 27.0
percent of all claims, distributed by ultimate holder, plus the obligor leg for claims the
federal government owes.

**The AI leg** has three components. Two are sourced and one is a scenario:

| Component | Size | Status |
|---|---|---|
| AI-capital firms' on-balance-sheet debt | **458.4bn** | SOURCED. SEC XBRL company facts, long term debt plus finance leases, nine named filers |
| Bank C and I commitments to AI-adjacent industries | **450.0bn** | SOURCED, secondary. Chicago Fed Insights, February 2026, verified in A45 |
| AI-capital firms' equity | 14,399bn at the central case | **SCENARIO.** 20 percent of US nonfinancial corporate equity market value (71,995bn). Swept over 10, 20 and 30 percent. No filing discloses an AI-attributable market value |
| Data centre and GPU-backed debt, off-balance-sheet vehicles | **NOT SOURCED** | Recorded as absent. It makes every figure here a lower bound |

Equity holder shares are taken from the Z.1 distribution of nonfinancial corporate
equities. **FLAGGED:** AI-capital firms are mega-cap index constituents, so the true
household, mutual fund and rest-of-world shares are probably higher than the aggregate and
the federal share no higher than shown.

## The table, central case

| Holder | Wage leg share | AI leg share | Net position in the partial state | AI over wage |
|---|---|---|---|---|
| **federal government** | **0.3215** | **0.0100** | **-0.3115** | **0.03** |
| banks | 0.1844 | 0.0318 | -0.1525 | 0.17 |
| rest of the world | 0.1801 | 0.1808 | +0.0007 | 1.00 |
| other financial | 0.1532 | 0.1633 | +0.0101 | 1.07 |
| households | 0.0607 | 0.3842 | +0.3235 | 6.33 |
| state and local government | 0.0462 | 0.0363 | -0.0100 | 0.78 |
| insurers | 0.0203 | 0.0207 | +0.0003 | 1.02 |
| pensions | 0.0110 | 0.0437 | +0.0327 | 3.97 |
| nonfinancial business | 0.0062 | 0.0313 | +0.0250 | 5.02 |

The wage leg column above is the HOLDER share. **On the union measure, which adds the
claims the federal government owes rather than holds, the federal wage leg share is
0.7936.**

## The test, and the verdict

> **Claim.** The federal government holds the majority of the wage leg and a negligible
> share of the AI leg, its only claim being tax at the operative effective rate, so it is
> the least hedged holder. Private holders of the AI leg hold little of the wage leg.

**CONFIRMED, on both halves.**

- Federal wage leg, union basis: **0.7936**. Federal AI leg: **0.0100**. The ratio of AI
  cover to wage exposure is **0.03**, the lowest of any holder class by a factor of five
  against the next lowest (banks, 0.17).
- The mirror holds. **Households hold 38.4 percent of the AI leg and 6.1 percent of the
  wage leg**, a ratio of 6.3. Pensions 4.0. Nonfinancial business 5.0. The rest of the
  world, other financial and insurers are almost exactly hedged, at ratios of 1.00, 1.07
  and 1.02, which is a striking and unforced result.
- **Banks are the second least hedged holder**, at 0.17, and that is before the second
  round, which claim 154 puts at nine tenths of their losses.

## The government's implicit claim on the AI leg

The federal government's only claim on AI capital is tax. Stating it as a present value,
at a 10 percent dose, case A, over ten years at 3 percent:

| Rate | What it is | Share of the GROSS federal first-round loss it hedges |
|---|---|---|
| **tau_k = 0.0708** | the OPERATIVE effective rate (claim 53, independently confirmed) | **36.0 percent** |
| tau_k = 0.20351 | the top of the sourced effective range | about the break-even region at this dose |
| break-even | 0.1431 at this dose, case A | **68.6 percent of the federal first-round loss, and exactly 100 percent of the GROSS FISCAL loss, by construction** |

**A trap worth naming.** The fiscal loss this project publishes is already **net** of
capital tax at the operative rate. Dividing a tax claim by that figure counts the tax
twice. Everything above is on a gross basis, and the internal check is that the break-even
rate recovers exactly 1.000 of the gross fiscal loss. It does.

So **even at the break-even rate the capital tax does not fully hedge the federal
position**, because the federal first-round loss is wider than the fiscal loss: it
includes the GSE, FHA and federal student credit losses, which a capital tax does not
touch. And the trust fund leg is not reachable by this instrument at all, because
replacement income financed from a capital tax is not covered wages (claim 161).

---

# B12. The payoff table across three states of the world

## The states

| State | Definition |
|---|---|
| **Failure** | AI fails after heavy investment. Little or no displacement, so the wage leg is broadly unharmed. The AI leg is written down |
| **Partial** | Displacement happens but little taxable surplus appears, whether through profit shifting, consumer surplus or competition. The wage leg is hit and the AI leg pays little |
| **Success** | Displacement happens and a large taxable surplus appears. The AI leg pays. The wage leg is still hit |

## Sizing the failure state

Exposed claims, on the definitions above: **14,399bn of equity (SCENARIO), 458bn of
on-balance-sheet debt (sourced), 450bn of bank commitments (sourced), and an unmeasured
amount of off-balance-sheet and GPU-backed debt.**

**The financing structure says which kind of bust this would be, and the answer is
currently the mild one.**

| Measure | Value |
|---|---|
| Aggregate operating cash flow over capex, nine named filers | **1.343** |
| Capex in excess of operating cash flow, as a share of capex | **0.065** |
| Filers spending above operating cash flow individually | Oracle, CoreWeave, Equinix, Digital Realty |

**In aggregate the named AI capital spenders fund capex out of operating cash flow. That
is the 2000 structure, not the 2008 structure.** The marginal dollar is not: four of nine
filers are already below 1.0, and the Chicago Fed commitments and the off-balance-sheet
vehicles sit outside these filings entirely.

## The two historical anchors, MEASURED and not cited

Both rebuilt here from Z.1 and NIPA series already in the repository, rather than quoted
from a secondary source.

| | **2000 to 2002, equity-financed** | **2007 to 2009, debt-financed** |
|---|---|---|
| Nonfinancial corporate equity, market value | 13,361bn to 9,269bn, **-30.6 percent** | 16,914bn to 13,674bn, **-19.2 percent** |
| That fall as a share of peak GDP | **-39.9 percent** | -22.4 percent |
| Household equity and fund shares (DFA) | 8.99tn to 6.43tn, -28.4 percent | 13.43tn to 10.66tn, -20.6 percent |
| Federal current receipts | 2,067.8bn to 1,870.9bn, **-9.5 percent** | 2,668.3bn to 2,242.1bn, **-16.0 percent** |
| Federal corporate income tax receipts | 194.1bn to 126.0bn, **-35.1 percent** | 328.2bn to 153.0bn, **-53.4 percent** |

**The equity bust was the larger asset-price event and the smaller fiscal and banking
event.** Equity fell half again as far relative to GDP in 2000 to 2002, and federal
receipts fell by 9.5 percent against 16.0. Corporate tax receipts fell by a third against
a half. Bank balance sheets came through 2000 to 2002 broadly intact and did not come
through 2008 intact.

**Which does the current structure resemble? 2000.** Equity-financed, internally funded,
concentrated in firms with large operating cash flows.

**What would change that**, and these are the things to watch:

1. The debt-financed share of capex rising from 0.065 towards 0.5. It is now a dashboard
   indicator for exactly this reason.
2. The off-balance-sheet and SPV channel, which is currently unmeasured and which BIS
   Quarterly Review March 2026 describes as the dominant data centre financing structure.
   **If it is large, the 0.065 is badly understated and the conclusion flips.**
3. Bank commitments migrating from commitment to outstanding. The Chicago Fed puts
   committed exposure at about 25 percent of tier 1 capital against 9 percent outstanding.
4. The neocloud and REIT names growing relative to the hyperscalers, since they are the
   ones already spending above operating cash flow.

## The government's revenue exposure in the failure state

Measured above: **corporate income tax receipts fell 35.1 percent after 2000 and 53.4
percent after 2007.** Capital gains realisations are the other channel and are **not
sourced here**: they require Treasury or CBO series this environment does not carry, so no
figure is asserted. That is a stated gap, not an omission.

## The payoff table

Direction and rough size. Household rows use the Distributional Financial Accounts.

| Holder | Failure | Partial | Success |
|---|---|---|---|
| **federal government** | **LOSS.** Corporate and capital gains receipts fall. Measured anchors: corporate tax -35 to -53 percent | **LARGE LOSS.** Wage leg 0.79, AI leg 0.01, and little surplus to tax | **LOSS, partly offset.** Wage leg still falls; capital tax at 0.0708 recovers **36 percent** of the gross federal loss at a 10 percent dose |
| state and local government | LOSS, smaller. Receipts fall | LOSS. Wage leg 0.046 against AI leg 0.036 | LOSS, largely unoffset. No capital tax instrument of its own at this scale |
| banks | **LOSS.** 450bn committed, about 25 percent of tier 1 | **LARGE LOSS.** Wage leg 0.184 against AI leg 0.032, and the second round is nine tenths of it | Mixed. Small AI gain against a wage leg loss |
| non-bank lenders and private credit | LOSS, size UNMEASURED. This is where the off-balance-sheet channel sits | LOSS | Gain |
| insurers and pensions | LOSS on the AI leg | Roughly neutral for insurers (1.02), net gain for pensions (3.97) | **GAIN** |
| **households, top 0.1 percent** | **LARGE LOSS.** 25.0 percent of household equity, 0.9 percent of household debt. Equity to debt ratio **28.1** | **GAIN.** Almost no wage leg exposure | **LARGE GAIN** |
| households, next 0.9 percent | LOSS. Equity to debt ratio 8.8 | GAIN | LARGE GAIN |
| households, next 9 percent | LOSS. Ratio 1.8 | Roughly neutral | GAIN |
| households, next 40 percent | Small loss. Ratio **0.25** | **LOSS** | Small gain against a larger wage loss |
| **households, bottom 50 percent** | **Almost no loss.** 0.6 percent of household equity against 30.4 percent of household debt. Ratio **0.019** | **LARGE LOSS, unhedged** | **LOSS.** They own almost none of the upside |
| rest of the world | LOSS, 0.18 of the AI leg | Neutral (ratio 1.00) | GAIN |

**The single sharpest number in this table: the ratio of equity share to household debt
share runs from 28.1 at the top 0.1 percent to 0.019 at the bottom half, a factor of about
1,480.** Whatever AI does, it does opposite things to those two groups.

## The test, and the verdict

> **Claim.** The federal government loses in all three states and holds almost none of the
> upside in the success state.

**CONFIRMED, with one qualification that should be stated whenever the claim is used.**

- **Failure:** loses. Measured, on both anchors.
- **Partial:** loses, and this is its worst state. Net position -0.31 on the holder basis
  and worse on the union basis.
- **Success:** **still loses on net, but "almost none of the upside" is too strong.** At
  the operative rate the capital tax recovers 36 percent of the gross federal first-round
  loss at a 10 percent dose, which is not nothing. The accurate statement is that the
  federal government **holds 1.0 percent of the AI leg as an asset and recovers about a
  third of its wage-leg loss through tax**, and that the recovery share falls as the dose
  rises, because the break-even rate rises with the dose while the operative rate does not.

**The qualification matters and it weakens the claim slightly.** It is stated here rather
than left for a reviewer.

## Plausibility bounds

Holder shares sum to 1 within each leg and within each scenario. All shares in [0, 1]. DFA
equity shares and household debt shares each sum to 1. The debt-financed share of capex in
[0, 1]. The break-even rate recovers exactly 1.000 of the gross fiscal loss by
construction. Both anchors show a fall in corporate tax receipts.

**14 checks, 0 violations.**

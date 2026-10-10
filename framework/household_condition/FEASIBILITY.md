# Data feasibility: the household condition

**2026-09-21. Feasibility only. No result of the exercise was computed.** Counts,
coverage and the reconciliation below exist so the specification could be written against
known data.

---

## 0. The three things that most threaten the exercise

**0.1 Consumer credit does not reconcile, and it is where the payments are.** SCF consumer
credit is **0.60** of the Financial Accounts figure. Credit-card balances alone need a
factor of **3.73** against the measurement paper's official aggregate — worse than the
paper's own SIPP factor of **2.52** for the same cell. Revolving debt carries the highest
required payment per dollar of balance, so the payment-to-income ratio is least reliable
exactly where it matters most. The under-reporting correction must be a reported axis, not
a fixed assumption.

**0.2 Equity over-reconciles by half.** SCF household equity across all routes is **1.50**
times the DFA corporate-equity line, and private business equity **1.93** times the DFA
unincorporated-business line. These are definitional mismatches (SCF `retqliq` holds bonds
and cash as well as equity; SCF `bus` includes S-corporation and partnership stakes the
DFA books elsewhere), not survey error, but they mean **raw SCF equity cannot be used as
the allocation base for capital income** without decomposition. The specification uses the
Rosenthal and Mucciolo holder shares for the aggregate and SCF only for the within-
household distribution.

**0.3 The 2025 wave is not out.** The latest public SCF microdata is **2022**. A 2026
release would supersede it mid-project.

---

## 1. Survey of Consumer Finances: availability and structure

**Verified live 2026-09-21.** Latest public wave is **2022**; `scf2025s.zip` returns HTTP
404, so no 2025 wave exists yet.

| File | URL | Status |
|---|---|---|
| Summary extract 2022 | `federalreserve.gov/econres/files/scfp2022s.zip` | fetched, 2.9 MB |
| Full public 2022 | `federalreserve.gov/econres/files/scf2022s.zip` | fetched, 8.9 MB |
| Summary extract 2019 | `federalreserve.gov/econres/files/scfp2019s.zip` | fetched, 4.2 MB |
| Replicate weights 2022 | `federalreserve.gov/econres/files/scf2022rw1s.zip` | fetched, 26.9 MB |
| DFA full dataset | `federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip` | fetched, 0.9 MB |

**No file required an owner fetch. Nothing is blocked.**

| Wave | Rows | Households | Implicates | Variables | Weighted households |
|---|---|---|---|---|---|
| **2022** | 22,975 | **4,595** | 5 | 357 | **131.31m** |
| **2019** | 28,885 | **5,777** | 5 | 357 | **128.64m** |

**Multiple imputation.** Five implicates per household, identified by `y1` (last digit
1–5) with `yy1` the household identifier. Every statistic is computed within implicate and
combined by Rubin's rules.

**Replicate weights.** `p22_rw1.dta`, 4,595 rows, **999 replicate columns**
(`wt1b1`–`wt1b999`), keyed on `yy1`/`y1`. These give the within-implicate sampling
variance by the SCF's own bootstrap design.

**A weight trap, documented because it was got wrong once while writing this.** The
summary-extract `WGT` is scaled so that the sum over **all five implicates** equals the
household count (131.31m). A single implicate sums to **26.26m**, one fifth. Aggregates
must use the full-sample sum, or a single implicate multiplied by five. Getting this wrong
understates every aggregate by a factor of five. The run asserts the household count before
proceeding.

**A second trap.** The SCF oversamples wealthy households, so **unweighted ranks are not
percentiles**. Wealth and income groups must be cut on weighted cumulative shares. Cut
unweighted, the p90–99 group holds 0.06m households instead of 8.09m.

---

## 2. Variables: every one required is present

All in the summary extract `rscfp2022.dta`.

**Income.** `income` (total), `wageinc` (wage and salary), `bussefarminc` (business, self-
employment and farm), `intdivinc` (interest and dividends), `kginc` (realised capital
gains), `ssretinc` (Social Security and pensions), `transfothinc` (other transfers),
`norminc` (normal income), `equitinc`.

**Debt balances, by class.** `debt` (total), `mrthel` (primary-residence mortgage and home
equity lines), `nh_mort`, `homeeq`, `othloc`, `resdbt`, `ccbal` (credit card),
`veh_inst` (vehicle), `edn_inst` (education), `install` (all installment), `odebt`.

**Required payments.** `tpay` (total), `mortpay`, `conspay`, `revpay`, plus per-loan
`paymort1-3`, `payveh1-4`, `payedu1-7`, `payiln1-7`, `payloc1-3`, `payore1-3`.
**Payment-to-income ratios already constructed:** `pirtotal`, `pirmort`, `pircons`,
`pirrev`, and **`pir40`**, the SCF's own flag for payments above 40 percent of income.
`debt2inc` gives the balance ratio.

**Equity.** Direct: `stocks`, `nmmf` (mutual funds). Indirect: `retqliq` (retirement
accounts, quasi-liquid), `irakh`, `thrift`, `annuit`, `savbnd`. Business: `bus`, `actbus`,
`nonactbus`, `farmbus`, `kgbus`. Totals: `equity`, `deq`.

**Liquid assets.** `liq`, `checking`, `saving`, `mmda`, `call`, `cds`.

**Distress, observed.** `late`, `late60`, `bnkruplast5`, `hpstppay`, `forecloselast5`.

**Nothing required is missing.**

---

## 3. Sample sizes for indebted households

2022, first implicate for unweighted counts, **weighted** group cuts.
**3,372 of 4,595 households (73.4 percent) hold debt.**

**By wage quintile:**

| Quintile | n | n indebted | Weighted indebted (m) |
|---|---|---|---|
| Q1 | 938 | 536 | 15.31 |
| Q2 | 862 | 538 | 16.83 |
| Q3 | 803 | 642 | 21.70 |
| Q4 | 743 | 664 | 24.20 |
| Q5 | 1,249 | 992 | 23.67 |

**By wealth group:**

| Group | n | n indebted | Weighted indebted (m) |
|---|---|---|---|
| p0–25 | 1,057 | 747 | 24.18 |
| p25–50 | 783 | 641 | 27.41 |
| p50–75 | 810 | 682 | 26.51 |
| p75–90 | 666 | 514 | 14.84 |
| p90–99 | 713 | 503 | 8.09 |
| **top 1** | **565** | **285** | **0.68** |

The top 1 percent has 565 sample households for 0.68m weighted — the oversample. Cell
sizes are ample everywhere; the binding constraint is **not** sample size.

**By debt class (households holding):**

| Class | n | Weighted (m) |
|---|---|---|
| Home equity (any) | 3,094 | 85.94 |
| Installment (any) | 2,117 | 69.67 |
| Mortgage / HELOC | 1,822 | 55.27 |
| Credit card | 1,742 | 59.76 |
| Vehicle | 1,391 | 45.58 |
| Education | 812 | 28.47 |
| Other debt | 254 | 6.73 |
| Other lines of credit | 121 | 2.13 |

---

## 4. Reconciliation to the Financial Accounts and DFA

SCF 2022 weighted aggregates against the **Distributional Financial Accounts, 2022:Q4**
(which tie to the Financial Accounts by construction). Full table in
`scf_dfa_reconciliation.csv`.

| Cell | SCF ($bn) | DFA / Z.1 ($bn) | SCF / official | Implied factor |
|---|---|---|---|---|
| Home mortgages incl. HELOC | 11,770.8 | 12,654.1 | **0.930** | 1.075 |
| **Consumer credit** | **2,928.2** | **4,858.4** | **0.603** | **1.659** |
| Total liabilities | 16,658.0 | 18,398.1 | **0.905** | 1.105 |
| Corporate equity, all household routes | 50,208.9 | 33,387.3 | **1.504** | 0.665 |
| Private business equity | 30,772.9 | 15,953.5 | **1.929** | 0.518 |
| Pension entitlements | 23,838.3 | 28,313.6 | 0.842 | 1.188 |

**Against the measurement paper's own SIPP-based under-reporting factors** (the corrected
ones, per claim 127, which separate survey under-reporting from sample coverage):

| Loan | Paper's SIPP factor | SCF 2022 ($bn) | Implied SCF factor |
|---|---|---|---|
| Mortgage | 1.2592 | 11,770.8 | **1.113** |
| **Card** | **2.5159** | **363.5** | **3.734** |
| Auto | 1.9036 | 968.7 | 1.768 |
| Student | 1.4233 | 1,338.8 | 1.232 |

The paper's official aggregates are a later vintage than 2022, so these are **indicative**
and the run recomputes them on a matched vintage. The ordering is the point: **the SCF is
better than SIPP on mortgages and student loans, and materially worse on credit cards.**

### What cannot be reconciled, stated

1. **Consumer credit, at 0.60.** Not a vintage artefact. Survey respondents under-report
   revolving balances, and the SCF's convention of asking for balances after the last
   payment understates revolving credit against the Z.1 measure. **Reported as
   unreconciled at every use**, with the correction as an axis.
2. **Private business equity, at 1.93.** A definitional mismatch: the SCF's `bus` includes
   S-corporation and partnership stakes the DFA books under other lines. Not correctable
   by scaling; the specification does not use `bus` as an equity base without stating it.
3. **Household equity across all routes, at 1.50.** `retqliq` is a retirement-account
   balance, not an equity holding; it contains bonds and cash. The specification therefore
   takes the **aggregate** equity split from Rosenthal and Mucciolo and uses the SCF only
   for the **within-household distribution**.
4. **Defined-benefit entitlements.** The SCF barely fields them; the DFA carries
   28,313.6bn of pension entitlements against the SCF's 23,838.3bn of quasi-liquid
   retirement assets, and the two are not the same object.

---

## 5. Who actually owns the capital

From **Rosenthal and Mucciolo (2024) Table 5**, already sourced in the measurement paper
(`framework/tau_k/components.py`), US corporate equity in 2022:

| Holder | Share | Reaches household cash flow? |
|---|---|---|
| **Taxable household accounts** | **0.27** | yes |
| **Foreign** | **0.42** | **never** |
| IRAs | 0.11 | on accrual only |
| Defined benefit | 0.07 | on accrual only |
| Defined contribution | 0.07 | on accrual only |
| Nonprofits | 0.04 | **never** |
| Life insurance separate accounts | 0.02 | indirectly, not modelled |
| Government | 0.01 | **never** |

**0.47 of US corporate equity sits with holders whose capital income never reaches a
household's cash flow directly.** A further 0.25 sits in retirement vehicles that accrue
to households but produce no spendable income for a working-age family.

This is the single most consequential fact for the exercise and it is known before any
computation. It is why §4.2 of the specification reports the cash-flow and accrual bases
separately and never blends them, and why a `κ = 1.0` upper bound is reported as an
explicit counterfactual.

---

## 6. Files produced

| File | Contents |
|---|---|
| `feasibility_scf.py` | SCF structure, variable presence, sample sizes, aggregates |
| `feasibility_scf.json` | the above, machine readable |
| `reconcile_scf_dfa.py` | SCF-to-DFA reconciliation and the paper's SIPP factors |
| `scf_dfa_reconciliation.csv` / `.json` | §4 tables |
| `SPECIFICATION.md` | the pre-committed specification |
| `NOVELTY.md` | the kill criterion, applied |

# Replication brief v2.2, addendum

Two constructions only: the **debt-only labour backing ratio** and the **assembled effective
capital tax rate on AI surplus**. Everything you need to rebuild both is here. Nothing else
from the project is required.

Expected values are sealed in a file in `notes/sealed/`. **Ask the owner for it, and only
after your rebuild is written down.** Tolerances are stated inside it.

Data vintage throughout: **Federal Reserve Z.1 released 2026-09-10, latest observation
2026Q2**. Annual figures are the Q4 observation. Work in an empty folder.

---

# PART A. The debt-only labour backing ratio

## A1. What the statistic is

**What share of US debt is serviced directly out of wages?**

The labour backing accounts decompose all US financial claims by the income that services
them. The published all-claims version puts **corporate equity at market value** in the
denominator, which makes it partly an asset-price series: it falls when equity rises and
rises when equity falls, independently of anything happening to labour. The **debt-only**
ratio removes every market-valued equity class from the denominator, leaving claims carried
at par or amortised cost, so the series measures composition rather than valuation.

Two variants, on the same first-round versus second-round boundary the sovereign share uses:

- **DIRECT.** Only claims that wages pay directly.
- **INCLUDING INDIRECT.** Business-revenue-serviced classes additionally carry the measured
  indirect labour share of business revenue, that is, wages become spending and spending
  becomes business revenue.

## A2. The class excluded from the debt-only denominator

The exclusion rule is by **valuation basis, not by name**: any class carried at market value
as an equity claim is excluded, so a future equity class is caught automatically.

| class | Z.1 series | vintage | why excluded |
|---|---|---|---|
| `corporate_equity` | **LM103164105** | Z.1 2026-09-10, 2026Q2 | corporate equity at MARKET VALUE |

Note the `LM` prefix. Z.1 uses **LM for market-value levels** and **FL for book-value
levels**, which is itself the signal the rule keys on. It is the only such class in the
thirteen-class table.

## A3. The twelve classes that remain

| # | class | Z.1 liability series | labour backing |
|---|---|---|---|
| 1 | home_mortgage | FL153165105 | 0.840223 |
| 2 | credit_card | FL153166100 | 0.740 |
| 3 | auto_loan | FL153166400 | 0.7737 |
| 4 | student_loan | FL153166220 | 0.8832 |
| 5 | other_consumer | FL153166205 | 0.815554 |
| 6 | multifamily_mortgage | FL103165405 + FL113165405 + FL313165403 | 0.72754 |
| 7 | treasury | FL313161105 + FL313169205 | 0.657788 |
| 8 | state_local_debt | FL213162005 + FL213168003 + FL214141005 | 0.159338 |
| 9 | corporate_bonds | FL103163005 | **0 by rule** |
| 10 | corporate_loans | FL103168005 + FL103169005 + FL103169100 | **0 by rule** |
| 11 | noncorporate_business_debt | FL113168005 + FL113169005 + FL113169535 + FL113167205 | **0 by rule** |
| 12 | commercial_mortgage | FL103165505 + FL113165505 + FL163165505 | **0 by rule** |

**Government debt enters through the labour-linked share of the receipts that service it**,
which is what 0.657788 and 0.159338 are. Treasury debt is not wage-backed because a household
owes it; it is wage-backed to the extent that wage taxes pay it. **The Treasury figure is the
lower end of a bound**, for the reason set out in Part A6.

**Classes 9 to 12** are serviced from business revenue. In DIRECT they carry zero; in
INCLUDING INDIRECT they carry the measured indirect labour share of business revenue.

## A4. The arithmetic

    debt_denominator(y) = sum of the twelve class levels in year y
    labour_backed(y)    = sum over those twelve of level x backing
    DEBT_ONLY_direct(y) = labour_backed(y) / debt_denominator(y)

    INCLUDING INDIRECT adds, for classes 9 to 12 only:
        + level x indirect_labour_share_of_business_revenue

Build it for **every year from 1952 to 2025**, taking the Q4 observation of each series.

## A5. The structural bound, to check before anything else

> **DEBT_ONLY_direct(y) must be greater than or equal to all_claims_direct(y) in EVERY
> year.**

Removing from the denominator a class whose labour backing is zero cannot lower the ratio.
Corporate equity is zero by rule, so excluding it must raise the ratio or leave it unchanged.
**If your rebuild violates this, the error is in your class list, not in the data**, and no
other check will tell you that as quickly. Two further bounds: every ratio lies in **[0, 1]**,
and the debt-only denominator is never larger than the all-claims one.

## A6. What to report

1. The 2025 pair, direct and including indirect.
2. The 2000 and 2008 direct readings, for both the debt-only and the all-claims series, so
   the asset-price problem is visible.
3. The 1952 direct reading.
4. The equity share of the all-claims denominator in 2025.
5. The coefficient of variation of both direct series over 1952 to 2025.
6. Sensitivity of the debt-only direct ratio to each named judgement call, one at a time.

**The judgement call that matters** is the **one-step rule**, whether classes 9 to 12 take
zero or the indirect share. It is the largest judgement in this project and moves the
**all-claims** ratio by about 76 percent. Report what it does to the debt-only ratio; if you
get a much smaller number, that is the point of the statistic and not an error.

**One bound you must carry.** The Treasury backing share is the labour-linked share of
federal receipts and is itself a bound, not a point. Realised capital gains sit inside AGI and
bear preferential rates, so on IRS Statistics of Income data for 2021 to 2023 the share runs
**0.6339 to 0.6528**. We publish the lower end. Realised gains are **6.19 to 15.36 percent of
AGI** across those three years. Across that band the sovereign union share moves from 0.793592
to 0.797089, under half a percent.

## A7. What to attack

- **The zero-by-rule classes.** If you think commercial mortgage belongs with multifamily
  rather than with business debt, say so and show the effect.
- **Whether excluding equity is the right correction.** An alternative is to keep equity at
  book value. We did not do that; argue it if you think it is better.
- **The Treasury backing share**, per A6.

---

# PART B. The assembled effective capital tax rate on AI surplus

## B1. What the statistic is

**The marginal effective tax rate on a dollar of AI surplus earned in the United States,
inclusive of every layer of tax that reaches that dollar**: entity-level federal tax, state
corporate tax, the preferential regimes on foreign and foreign-derived income, and the
shareholder-level tax on the distribution. It is a **marginal, flow** rate.

**No layer may be counted twice.** Acemoglu, Manera and Restrepo already include
personal-level taxes in their effective rates, and the IMF's capital average tax rate is an
average on the existing stock that also includes them. Nothing is taken from the IMF measure
into this assembly; it is a comparison point only.

## B2. The AMR result this is built on

Acemoglu, Manera and Restrepo (2020), equations 12 to 18, are Hall-Jorgenson in form and
already include personal-level taxes. **Set the present value of depreciation allowances to
1, which is 100 percent expensing under 26 USC 168(k), and their expressions collapse:**

| financing and entity | effective marginal rate on the normal return |
|---|---|
| C corporation, equity financed | **the shareholder rate alone**; the entity tax washes out |
| C corporation, debt financed | **`tau_b - tau_c`**, negative where bondholders face a lower rate than the corporation |
| pass-through, equity financed | zero |

So under full expensing the normal-return effective rate **is** the shareholder-level rate.
It is not zero. A construction that stops at the entity level omits a layer.

## B3. The components

| component | value | source, with table |
|---|---|---|
| federal corporate rate `tau_c` | **0.21** | 26 USC 11(b), flat. Unchanged by Pub. L. 119-21 |
| foreign-derived deduction eligible income, effective | **0.13999** | 26 USC 250(a)(1)(A), **33.34 percent** deduction as amended by Pub. L. 119-21 of 4 July 2025 |
| net CFC tested income, effective | **0.126** | 26 USC 250(a)(1)(B), **40 percent** deduction, same Act. 26 USC 951A was recaptioned from "Global intangible low-taxed income" to "Net CFC tested income" |
| rent share, reading 1 | **0.351** | Barkai |
| rent share, reading 2 | **approximately 0.00** | Karabarbounis and Neiman, case R |
| shifted share of rents | **0.30 to 0.60**, centred on 0.48 | Torslov, Wier and Zucman, 48 percent of pre-tax profit of majority-owned foreign affiliates of US multinationals booked in havens. **One verified source only**, so swept |
| state effective corporate rate | **0.00 to 0.095**, swept | statutory ceiling, unsourced |
| taxable-shareholder share `theta` | **0.24 / 0.27 / 0.28** | Rosenthal and Austin, Tax Notes 16 May 2016 p. 923, Table 2 (0.242, C corporation stock, 2015); Rosenthal and Mucciolo, Tax Notes Federal 183(1), 1 April 2024, **Table 5 (0.27, total US equity, 2022)** and Table 7 (0.28, publicly traded) |
| shareholder statutory rate | **0.15 to 0.238**, swept | 0.238 ceiling is the 20 percent top long-term rate plus the 3.8 percent net investment income tax |
| deferral factor | **0.4118 / 0.6008 / 0.7899** | **CRS R47113 Table 5**, third row (9.8 no-dividend, 18.8 dividend stock) over the 23.8 statutory, taken BEFORE its own taxable-share adjustment so theta is not double counted. **Cross-check: CBO 2014 Tables A-3 and A-4 give 0.488** from 3.4 percent of gains short-term at 32.3, 49.6 percent long-term at 21.2 and **46.9 percent held until death and untaxed** |
| bondholder rate `tau_b` | **0.1433 / 0.1593 / 0.1753** | **CBO 2014 Table A-3** (C corporation debt: 52.3 percent fully taxable, 14.9 temporarily deferred, 32.8 nontaxable) times **Table A-4** (marginal rate on interest income **0.274**). Upper bound adds the deferred tranche at CBO's nonqualified annuity rate of 0.215 |
| debt share | **0.1412 / 0.2001 / 0.2589** | Fed Z.1 2026Q2, nonfinancial corporate business. Debt = FL103163005 + FL103168005 + FL103169005 + FL103169100 + FL103165505. Low end is debt over debt plus **equity at market**, LM103164105; high end is debt over debt plus **net worth at book**, FL102090005. **Economy-wide stock used as a proxy for a marginal flow; state this** |

## B4. The assembly

    tau_sh   = theta x shareholder_rate x deferral_factor

    ent_dom  = tau_c + state x (1 - tau_c)          state tax is federally deductible
    ent      = (1 - shifted) x ent_dom + shifted x 0.126
    tau_rent = ent + (1 - ent) x tau_sh             shareholder layer on what survives

    tau_normal = (1 - debt) x tau_sh + debt x (tau_b - tau_c)      the AMR result

    tau_k = sigma x tau_rent + (1 - sigma) x tau_normal

with `sigma` **one of the two rent readings, never their average**. They are incompatible
readings of one accounting residual, not endpoints of an interval.

Sweep the three unsourced components uniformly over their stated ranges and the four sourced
components uniformly over their published ranges, 200,000 draws.

## B5. The required-rate band

The fiscal condition requires

    required tau_k = tau_l x (1 - R)

with **R = 0.568316** the retained wage share. Across the three labour-tax readings this
gives **0.110079 (AMR, tau_l = 0.255)**, **0.129937 (bottom-up, 0.301)** and **0.137276
(bottom-up, 0.318)**. So the band is **0.110 to 0.137**.

## B6. Checks to run before you look at anything else

1. **Sign test.** `tau_b - tau_c` must be **negative** across the sourced bondholder range.
   **CBO 2014 Table 2 measures the effective marginal rate on C-corporation debt-financed
   investment at -0.06**; your interval should contain it. AMR predicted the sign, CBO
   measured the magnitude.
2. **The shareholder layer against a published figure.** `theta x 0.238 x deferral` at the
   central values must land in **CRS R47113 Table 5's published 0.045 to 0.085**, and CRS's
   text puts the overall effective capital gains rate on corporate profits at "around 3
   percent". If your shareholder layer is far outside that, you have double counted theta.
3. **Ceilings.** No component above its statutory ceiling; every share in [0, 1]; the
   assembled rate between the lowest and highest component-consistent values.

## B7. What to report

1. The central rate under **each** rent reading, at the sourced central values.
2. The 5th and 95th percentiles, the minimum and the maximum, under each reading.
3. The share of the swept space in which `tau_k >= required`, against **each** of the three
   labour-tax readings.
4. A first-order variance decomposition over the seven swept and sourced parameters.
5. For each parameter, the assembled rate at each end of its range with the others at
   midpoint, and whether that interval contains either threshold.

## B8. What to attack

- **The base.** This is the real argument and it is not settled by anything above. A revenue
  replacement condition concerns tax collected on the **incremental** income that shifts from
  wages to AI capital, so we argue the right object is marginal, flow-based and inclusive of
  every layer. The counter-case is genuinely strong: expensing is a **timing** provision, not
  an exemption, so the shelter unwinds if the AI capital stock stops growing; the budget must
  be balanced against the whole capital income base each year, not the incremental dollar; and
  if AI rents are **less** shiftable than the multinational average, the domestic share is
  higher than we assume. **An average rate on the existing stock answers a different question,
  but it may be the question the budget actually asks.**
- **The debt share**, which is an economy-wide stock standing in for a marginal flow. Note
  which direction the error runs before you argue about it.
- **The one verified source behind the shifted share.**
- **Whether the 46.9 percent of gains escaping at death should be modelled as a rate
  reduction at all**, rather than as a base exclusion.

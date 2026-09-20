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

**One thing this exclusion does NOT do, and you must get it right or no value will
reproduce.** `corporate_equity` is a business-revenue-serviced class like classes 9 to 12.
It is dropped from the **debt-only** construction entirely, numerator and denominator. But in
the **all-claims INCLUDING INDIRECT** variant it stays in, and it **carries the indirect
labour share of business revenue in the numerator**, exactly as classes 9 to 12 do. The
business-revenue-serviced set is therefore five classes, not four:
`corporate_bonds`, `corporate_loans`, `noncorporate_business_debt`, `commercial_mortgage`
and `corporate_equity`.

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

**THE INDIRECT LABOUR SHARE OF BUSINESS REVENUE, 2025 = 0.338212.** It is the product of
**consumption's share of final demand, 0.681191** and **labour's share of personal income,
0.496502**, both from the NIPA vintage of this Z.1 release. It is a per-year series, not a
constant: build it for every year and use each year's own value. Added in A118 because
without it Part A could only be recovered by inverting a rounded cross-check, which cost the
round-three replicator 0.4 percent on the parameter.

## A4. The arithmetic

    debt_denominator(y) = sum of the twelve class levels in year y
    labour_backed(y)    = sum over those twelve of level x backing
    DEBT_ONLY_direct(y) = labour_backed(y) / debt_denominator(y)

    INCLUDING INDIRECT adds, for classes 9 to 12 only:
        + level x indirect_labour_share_of_business_revenue(y)

    indirect_labour_share_of_business_revenue(2025) = 0.338212

Classes 9 to 12 are the business-revenue-serviced classes that SURVIVE the debt-only
exclusion. In the **all-claims** INCLUDING INDIRECT variant the same term is added for
`corporate_equity` as well, per A2.

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

**Report the coefficients of variation on the SAMPLE standard deviation**, `ddof = 1`, not
the population convention. Over 74 annual observations the two differ in the fourth decimal
and the tolerance would absorb either, but the convention is sample sd and the published
figures are computed that way.

**One bound you must carry, and TWO QUANTITIES THAT MUST NOT BE CONFUSED.** Corrected in
A118: through A117 this passage quoted an upstream band against a downstream number, and
`0.657788` is not inside `0.6339 to 0.6528` at all. The two are:

| quantity | 2023 band | what it is |
|---|---|---|
| labour-linked share of federal **receipts** | **0.6339 to 0.6528** | the INPUT: social insurance contributions in full plus the wage share of the individual income tax, from IRS SOI Table 1.4 |
| **Treasury class backing**, the figure in A3 | **0.657788 to 0.678331** | the OUTPUT: that receipts share carried onto the Treasury class |

**We publish the lower end of the SECOND band, 0.657788**, which is the figure in the A3
class table and the one every sealed value is built on. The sentence was always true of the
construction; it quoted the wrong band. The reason it is a bound and not a point is
unchanged: realised capital gains sit inside AGI at preferential rates and we do not separate
them, and realised gains are **6.19 to 15.36 percent of AGI** across 2021 to 2023.

**The effect of moving to the upper end**, stated because it is small and an unexplained
inconsistency reads worse than a stated one: the 2025 debt-only direct ratio rises from
**0.5216 to 0.5306** (+1.73 percent relative), the all-claims direct ratio from **0.270271 to
0.274931** (+1.72 percent), and the sovereign union share from **0.793592 to 0.797089**, under
half a percent. No conclusion moves.

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
| shifted share of rents | **0.30 / 0.48 / 0.60**, central **0.48** | Torslov, Wier and Zucman, 48 percent of pre-tax profit of majority-owned foreign affiliates of US multinationals booked in havens. **One verified source only**, so swept AROUND the sourced value. The central is 0.48, NOT the range midpoint 0.45: the sweep is uncertainty about a measured number, not a flat interval. Through A117 the code took 0.45 while the text said 0.48; corrected in A118 in favour of the text, which is what the source supports. Worth 0.0012 on the Barkai central (0.0864 to 0.0851) and nothing under Karabarbounis and Neiman, where sigma = 0 kills the term |
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
2. **The shareholder layer against a published figure. REWRITTEN IN A118 - the form of this
   check through A117 was wrong, and our own construction failed it.** Two tests, both
   against CRS R47113:

   **(a) The text figure, directly.** CRS p. 2 puts the overall effective capital gains tax
   rate on corporate profits at "around 3 percent". `theta x 0.238 x deferral` at the sourced
   centrals is **0.0386**, against **0.0315**. Test: within 0.010. It passes, and it needs no
   rescaling because the text figure is stated on the whole of corporate profits.

   **(b) The Table 5 band, RESCALED.** Do **not** compare your layer to CRS's published
   0.045 to 0.085 as printed. That row has already had CRS's own taxable-share adjustment
   applied, at a "55 percent reduction", i.e. an implied taxable share of
   **25 / (25 + 30) = 0.4545**. CRS states the arithmetic in its own text: "the 25% share of
   corporate stock held by taxable individuals compared with the 30% share from exempt
   shareholders", citing Rosenthal and Burke (2020). **That denominator is DOMESTICALLY HELD
   stock - the roughly 45 percent held by foreigners is dropped from the base, not carried as
   untaxed.** Our `theta` of 0.24 to 0.28 is the same numerator over **all equity
   outstanding**, foreign included. Same source family, different base, so the two are not
   comparable as printed. Rescale:

       CRS band rescaled = [0.045, 0.085] x theta / 0.4545
       at theta = 0.27   = 0.0267 to 0.0505

   The constructed **0.0386** sits comfortably inside. At the ends of our theta range the band
   runs 0.0238 to 0.0524, and 0.0386 is inside throughout.

   **Why the base difference is ours to keep.** Our object is the rate on a dollar of US AI
   surplus **whoever holds it**, and a foreign holder genuinely bears close to no US
   shareholder-level tax, so the foreign-inclusive base is the right one here. CRS's base is
   right for CRS's question, which is the rate faced by a US saver. Neither is wrong; they are
   different denominators and must be reconciled before they are compared. **Run the
   foreign-excluded base as a marked sensitivity, per B7.6 - it is the largest single
   adjustment left in this module and it moves the rate toward the threshold.**

   If your shareholder layer is far outside the RESCALED band, you have double counted theta.
3. **Ceilings.** No component above its statutory ceiling; every share in [0, 1]; the
   assembled rate between the lowest and highest component-consistent values.

## B7. What to report

1. The central rate under **each** rent reading, at the sourced central values.
2. The 5th and 95th percentiles under each reading, and the **ANALYTIC minimum and maximum,
   not the sample extremes.** The assembly is **multilinear** in all seven parameters, so its
   supremum and infimum over the box are attained at corners: evaluate all 2^7 = 128 corners
   and report those. The maximum of 200,000 draws from a 7-dimensional box is an extreme order
   statistic with no stable value across seeds, and reporting it was a defect in this brief
   through A117. Under Barkai the analytic pair is **0.0563 to 0.1236**; the 200,000-draw
   sample gave 0.0593 to 0.1166, low by 0.007 at the top for the reason just given. Every
   "no corner of the space closes the condition" statement must be made against the ANALYTIC
   maximum.
3. The share of the swept space in which `tau_k >= required`, against **each** of the three
   labour-tax readings.
4. A first-order variance decomposition over the seven swept and sourced parameters.
5. For each parameter, the assembled rate at each end of its range with the others at
   central, and whether that interval contains either threshold.
6. **A MARKED SENSITIVITY at the CRS-implied taxable share of 0.4545**, per B6.2(b): the
   central rate under **both** rent readings, the percentiles, the analytic extremes, and the
   pass shares against the labour-tax readings. Report it as a **sensitivity on the base of
   theta**, never as an alternative estimate of theta, and report it whether or not it changes
   your verdict - it changes ours in one respect and we say so in B9.

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
- **The base of theta**, which is B6.2(b) and is now the live one. If you think a rate on US
  AI surplus should be computed over domestically held stock only, as CRS does, then B9's
  sensitivity is your central case and the robustness statement weakens as described there.

## B9. Where the verdict IS sensitive to the base of theta, stated first

At our theta the condition fails at the centre under both rent readings and **no corner of
the parameter space closes it against either labour-tax threshold.** At the CRS-implied
theta of 0.4545 the second half **stops being true** and the first half survives:

| | our theta, 0.24 to 0.28 | CRS-implied theta, 0.4545 |
|---|---|---|
| Barkai central | 0.0851 | **0.1024** |
| Barkai p05 to p95 | 0.0726 to 0.0993 | **0.0860 to 0.1231** |
| Barkai ANALYTIC max | 0.1236, **below** the 0.1373 threshold | **0.1506, ABOVE it** |
| pass share vs 0.1101 | 0.0013 | **0.2832** |
| pass share vs 0.1373 | 0.0000 | **0.0010** |
| Karabarbounis and Neiman central | 0.0150 | **0.0322** |
| Karabarbounis and Neiman pass share, either threshold | 0.0000 | 0.0000 |

**What survives either way:** the condition fails at the centre under both rent readings, and
fails everywhere under Karabarbounis and Neiman. **What does not survive the base change:**
the stronger A116 statement that there is no corner of the space in which the condition
closes. Under the foreign-excluded base there is, and the pass share against the easier
labour-tax reading rises from under a tenth of a percent to **28 percent**. Any claim resting
on "nowhere in the parameter space" must carry the base of theta in the same sentence.

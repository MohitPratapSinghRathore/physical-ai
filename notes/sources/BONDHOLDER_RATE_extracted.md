# Extracted figures: the bondholder rate, tau_b

Recorded 2026-09-20 for A116. Built the same way as the shareholder layer: a **taxable share
of the instrument** times a **marginal rate on the income for taxable holders**.

## Documents

1. **Congressional Budget Office. 2014. "Taxing Capital Income: Effective Marginal Tax Rates
   Under 2014 Law and Selected Policy Options." December 2014.** CBO publication 49817.
   File as supplied in session: `49817-taxingcapitalincome0.pdf`. Written by Paul Burnham;
   external reviewers included Alan Auerbach, Jane Gravelle, Gilbert Metcalf, Jack Mintz and
   James Poterba.
2. **Gravelle, Jane G. 2022. CRS R47113**, already recorded in
   `notes/sources/SHAREHOLDER_PARAMS_extracted.md`. Used here only as a qualitative cross-check.
3. **Federal Reserve, Financial Accounts of the United States, Z.1**, corporate and foreign
   bonds by holder sector. Read from this project's own Z.1 cache,
   `framework/labor_backing/_z1_cache.zip`, at 2026Q2. Saved to
   `framework/tau_k/z1_bond_holders.json`.

## 1. The taxable share of corporate bonds

**PRIMARY SOURCE: CBO 2014, Table A-3, "Distribution of Assets, by Tax Status."** Built by
CBO from Federal Reserve Flow of Funds data published 8 March 2012, for 2007, and it already
contains the fund look-through and the household-residual treatment that this task asks for.

| C corporation debt | share |
|---|---|
| nontaxable, chiefly retirement plans | **0.328** |
| temporarily deferred, nonqualified annuities and whole life | **0.149** |
| **fully taxable** | **0.523** |

CBO uses the same table for equity in C corporations (57.2 fully taxable), pass-through
entity debt (76.3) and homeowner debt (77.9), so the corporate-debt figure is not a one-off.

**CBO states the 0.328 twice more in its own text**, which is an internal consistency check.
Page 10: "almost one-third of interest income is sheltered." Page 24, Option 8: "about 33
percent of interest payments made by C corporations and 14 percent of interest payments made
by pass-through entities in 2007 were received within tax-favored plans and therefore were
never taxed."

### Independent corroboration from the Fed, at 2026Q2 rather than 2007

Corporate and foreign bonds outstanding, all sectors: **18,115.7bn**. Holder shares:

| holder | level bn | share |
|---|---|---|
| rest of the world | 5,195.7 | **0.287** |
| life insurance companies | 3,944.2 | 0.218 |
| mutual funds | 2,672.1 | 0.148 |
| pension funds, total | 1,547.6 | 0.085 |
| property-casualty insurance | 906.0 | 0.050 |
| US depository institutions | 817.7 | 0.045 |
| **households and nonprofits, DIRECT** | **192.0** | **0.011** |
| of which nonprofits alone | 194.0 | 0.011 |
| federal government | 10.1 | 0.001 |

**Read this correctly.** The 1.1 percent is the DIRECT holding, and nonprofits alone account
for all of it, so households directly hold approximately nothing. That does **not** contradict
CBO's 52.3 percent: almost all taxable household exposure to corporate bonds is **indirect**,
through mutual funds (14.8 percent of the instrument) and life insurance (21.8 percent), and
CBO's figure is after looking through those vehicles to their beneficial owners. The Fed map
corroborates CBO on the thing that matters, which is that **the largest single identifiable
holder is the rest of the world at 28.7 percent and is outside the US individual income tax
altogether**, with pensions a further 8.5 percent.

Sector codes 15 (households and nonprofits), 16 (nonprofits), 26 (rest of the world) and 31
(federal government) are the same codes this project already relies on in
`framework/labor_backing/config.py`, which is where they were checked.

## 2. The marginal tax rate on interest for taxable holders

**PRIMARY SOURCE: CBO 2014, Table A-4, "Average Marginal Tax Rates Under 2014 Law, by Source
of Income."** From the 2006 Statistics of Income Public Use File.

| source of income | average marginal rate |
|---|---|
| **interest income** | **0.274** |
| distributions from nonqualified annuities | 0.215 |
| long-term capital gains | 0.212 |
| dividends | 0.184 |
| short-term capital gains | 0.323 |
| pass-through business profits | 0.331 |
| corporate profits | 0.350 |

CBO's own note on the method: "The individual income tax rate on a particular type of capital
income held in a fully taxable account was set at the average of the marginal tax rates faced
by taxpayers with positive amounts of that particular type of capital income and positive
taxable income overall. For example, recipients of interest with positive taxable income
paid, on average, a tax rate of 27.4 percent on additional interest. That rate is below the
top statutory rate of 43.4 percent because many recipients were in lower tax brackets."

## 3. Assembly

    tau_b = (fully taxable share x interest rate)
            [+ (temporarily deferred share x nonqualified annuity rate)]

    LOW      0.523 x 0.274                     = 0.1433
    HIGH     0.1433 + 0.149 x 0.215            = 0.1753
    CENTRAL  midpoint                          = 0.1593

The low end credits nothing to the temporarily deferred tranche; the high end taxes it at
CBO's own rate for nonqualified annuity distributions and gives no credit for the deferral
itself, so it is an upper bound. **SOURCED RANGE ADOPTED: 0.143 to 0.175, central 0.159.**
This replaces the blind sweep of 0.15 to 0.37, whose entire mass sat at or above the sourced
upper bound.

## 4. Cross-check against a published effective rate

**CBO 2014, Table 2.** The effective marginal tax rate on income from **debt-financed
investment by C corporations is -6 percent**, and CBO's text gives the reason in terms of
exactly the two quantities above: "In the absence of inflation and accelerated depreciation,
the effective corporate tax rate on such income would be zero, because interest payments are
deductible. Inflation, however, enhances the value of the interest deduction, driving the ETR
to negative values. Accelerated depreciation pushes the rate even further into negative
territory. **The individual tax rate on interest income, by contrast, is positive and would
more than offset the negative corporate tax rate if people were not permitted to shelter
income in retirement plans. Because almost one-third of interest income is sheltered,
however, the overall ETR is slightly negative.**"

**The sign test our assembly must pass.** AMR's debt-financed normal return is
`tau_b - tau_c`. At the sourced range and the 21 percent federal rate that is **-0.067 to
-0.035**, negative throughout. AMR state the result is negative "if bondholders face lower
individual tax rates than corporations", and CBO measures the corresponding ETR at -6
percent. Three sources agree on sign and rough magnitude.

**Qualitative corroboration, CRS R47113 p. 18:** "Debt is still favored over equity in both
the corporate and noncorporate sectors, although that differential is largely traced to
allowing nominal interest payments to be deducted, while **most interest income is not
subject to individual tax**."

# Extracted figures: the taxable-shareholder share and the deferral factor

Recorded 2026-09-20 for A115. **The owner supplied four documents in the session rather than
on disk.** They are named here exactly so they can be placed in `data/raw/manual/` and the
figures re-checked. Every number below was read from the document text, not from a web
search, and the page or table is named.

## Documents

1. **Rosenthal, Steven M., and Lydia S. Austin. 2016. "The Dwindling Taxable Share of U.S.
   Corporate Stock." Tax Notes, May 16, 2016, pp. 923 to 934.**
   File as supplied: `2000790-The-Dwindling-Taxable-Share-of-U.S.-Corporate-Stock.pdf`
2. **Rosenthal, Steven M., and Livia Mucciolo. 2024. "Who's Left to Tax? Grappling With a
   Dwindling Shareholder Tax Base." Tax Notes Federal, vol. 183, no. 1, April 1, 2024,
   p. 91.** SSRN 4797771. File as supplied: `ssrn-id4797771.pdf`
3. **Gravelle, Jane G. 2022. "Capital Gains Taxes: An Overview of the Issues."
   Congressional Research Service R47113, May 24, 2022.**
   File as supplied: `CRS_Gravelle_2022_Capital_Gains_R47113.pdf`
4. **Congressional Budget Office. 2014. "Taxing Capital Income: Effective Marginal Tax Rates
   Under 2014 Law and Selected Policy Options." December 2014.**
   File as supplied: `49817-taxingcapitalincome0.pdf`

## 1. The taxable-shareholder share of US corporate equity

| source | year | share in taxable accounts | basis |
|---|---|---|---|
| Rosenthal and Austin 2016, Table 2 | 2015 | **0.242** | C corporation stock |
| Rosenthal and Austin 2016, section I | 1965 | 0.836 | C corporation stock |
| Rosenthal and Burke 2020, NYU Tax Policy Colloquium, quoted in CRS R47113 note 9 | 2020 | **0.25** | total equity in US corporations; 30 percent in retirement assets; remainder foreign |
| Rosenthal and Mucciolo 2024, Table 5 | 2022 | **0.27** | total US equity outstanding |
| Rosenthal and Mucciolo 2024, Table 7 | 2022 | **0.28** | publicly traded US stock only |
| Rosenthal and Mucciolo 2024, section I | 1965 | 0.79 total, 0.81 publicly traded | |

**METHOD, as the authors describe it.** Federal Reserve Financial Accounts of the United
States, Table L.224 and related tables. The Fed's residual "household sector" is NOT the
taxable share: it also contains nonprofits, IRAs and section 529 plans. The authors remove
intercorporate holdings, remove issuances by pass-through corporations (S corporations,
ETFs, closed-end funds, REITs) and allocate those entities' holdings to their beneficial
owners, remove foreign-issued stock and add foreign direct investment, remove nonprofits,
IRAs and 529 plans from the residual, and add back stock held indirectly through mutual
funds, ETFs and closed-end funds. Holdings and issuances are balanced at every step.

**WHO THE NON-TAXABLE HOLDERS ARE.** Rosenthal and Mucciolo 2024, 2022 shares.

| holder | total US equity (Table 5) | publicly traded only (Table 7) |
|---|---|---|
| foreign investors | **0.42** | **0.32** |
| IRAs | 0.11 | 0.13 |
| defined benefit plans | 0.07 | 0.09 |
| defined contribution plans | 0.07 | 0.09 |
| nonprofits | 0.04 | 0.05 |
| life insurance separate accounts | 0.02 | 0.03 |
| government, including 529 plans | 0.01 | 0.01 |
| **taxable accounts** | **0.27** | **0.28** |

Foreign investors are treated as exempt: they are almost always exempt on capital gains
(26 USC 865(a) sources gain to the seller's residence) and dividends are reduced by treaty,
typically to 15 percent on portfolio and 5 or 0 percent on direct investment. Retirement
accounts are effectively exempt whether Roth or traditional.

**SOURCED RANGE ADOPTED: 0.24 to 0.28, central 0.27.** The low end is Rosenthal and Austin's
2015 C-corporation figure, the high end the 2022 publicly traded figure, and the central the
latest total-equity figure. The three published estimates span only four percentage points.

**ONE MEASURE THAT LOOKS DIFFERENT AND IS NOT COMPARABLE.** CBO 2014, Table A-3, reports
that 57.2 percent of equity in C corporations was "fully taxable", 38.9 percent nontaxable
and 3.9 percent temporarily deferred. That is the distribution of the **marginal dollar of
saving by tax status in 2007**, used to place a new investment, not the share of the
outstanding **stock** of equity by holder. The two answer different questions and **are not
averaged**. Our construction needs the holder share of the stock, which is the Rosenthal
measure.

## 2. The deferral factor

**PRIMARY SOURCE: CRS R47113, Table 5, "Effective Marginal Tax Rates on Corporate Stock
Arising from Capital Gains."** The chain begins at the top statutory rate of **23.8 percent**
(20 percent long-term rate plus the 3.8 percent net investment income tax, CRS pp. 1 to 2)
and applies the adjustments in order:

| adjustment | stock with no dividend | stock with dividend |
|---|---|---|
| with 7-year holding period (deferral and unindexed inflation) | 21.3 | 25.2 |
| adjusted for exclusion at death, 50 percent reduction | 10.7 | 20.4 |
| adjusted for lower aggregate marginal tax rate | **9.8** | **18.8** |
| adjusted for share held in taxable form, 55 percent reduction | 4.5 | 8.5 |

**We take the third row, before the taxable-share adjustment**, because the taxable share
enters our construction separately as theta and must not be counted twice.

    deferral factor = (row 3) / 23.8
    no-dividend stock  9.8 / 23.8 = 0.4118
    4 percent dividend 18.8 / 23.8 = 0.7899

CRS states the current position between these two: "Traditionally dividends were around 4
percent, but recently stock repurchases have accounted for more than half of distributions
and dividends are closer to 2 percent, so the rate is somewhere in between." The midpoint is
**0.6008**.

**SOURCED RANGE ADOPTED: 0.412 to 0.790, central 0.601.**

**INDEPENDENT CROSS-CHECK, CBO 2014.** Table A-3 note and Table A-4 give the disposition of
capital gains and the rate on each: **3.4 percent realised short-term at 32.3 percent, 49.6
percent realised long-term at 21.2 percent, and 46.9 percent held until the owner's death and
therefore untaxed** because basis is stepped up. The implied average is
0.034 x 32.3 + 0.496 x 21.2 + 0.469 x 0 = **11.61 percent**, which against the 23.8 percent
statutory ceiling is **0.488**. That sits inside the CRS range, toward its lower end, and it
was built from an entirely separate dataset. The two sources agree on the thing that matters
most: **roughly half of accrued gains never bear tax at all**, CBO at 46.9 percent held to
death and CRS applying a 50 percent reduction for the same reason.

## 3. What taxable share CRS R47113 itself uses, and over what base

**ADDED A118, and it corrects the paragraph that followed it through A117.** CRS R47113 was
read directly for this (congress.gov and everycrsreport.com mirrors of the 24 May 2022
report; the PDF host returns 403 to automated fetches, the HTML mirrors do not).

**Table 5 as published, all six rows.**

| adjustment | stock, no dividend | stock with dividend | attributable to the capital gains tax |
|---|---|---|---|
| with 7-year holding period | 21.3 | 25.2 | 10.4 |
| adjusted for exclusion at death, 50 pct reduction | 10.7 | 20.4 | 5.2 |
| adjusted for lower aggregate marginal tax rate | **9.8** | **18.8** | **4.8** |
| **adjusted for share of corporate stock held in taxable form, 55 pct reduction** | **4.5** | **8.5** | **2.2** |
| adjusted for corporate tax-offset, temporary | 4.3 | 8.1 | 2.1 |
| adjusted for corporate tax-offset, permanent | 4.0 | 7.5 | 1.9 |

**THE TAXABLE SHARE CRS USES IS 25 / (25 + 30) = 0.4545, AND ITS BASE EXCLUDES FOREIGN
HOLDERS.** CRS's own text gives the arithmetic: the row reduces the tax "to adjust for the
25% share of corporate stock held by taxable individuals compared with the 30% share from
exempt shareholders". Its Table 5 source note cites **Rosenthal and Theo Burke, "Who's Left
to Tax? US Taxation of Corporations and Their Shareholders", NYU Tax Policy Colloquium,
27 October 2020**, for "of total equity in U.S. corporations, 25% are in taxable accounts and
30% are in retirement assets"; the remaining roughly 45 percent is held by foreigners and, in
CRS's words, not subject to tax. A 55 percent reduction is a multiplier of 0.45, and
25/55 = 0.4545 is the only arithmetic in the report that lands on it. **The foreign slice is
dropped from the denominator, not carried as untaxed.**

**DOES CRS MEASURE THE SAME OBJECT AS ROSENTHAL AND COAUTHORS? Same numerator, different
denominator.** CRS's 25 percent IS a Rosenthal figure — it cites Rosenthal and Burke 2020,
and that 0.25 is measured over **total equity in US corporations**, the same base as
Rosenthal and Mucciolo's 0.27 and within a percentage point of it. So the three Rosenthal
measures and CRS's numerator are one family and are consistent with each other. What CRS then
does, and Rosenthal does not, is **renormalise onto domestically held stock**. The two shares
are therefore:

| | numerator | denominator | value |
|---|---|---|---|
| Rosenthal and Austin 2016 / Rosenthal and Burke 2020 / Rosenthal and Mucciolo 2024, and OUR theta | equity in taxable accounts | ALL US equity outstanding, foreign included | **0.24 to 0.28** |
| CRS R47113 Table 5, taxable-form row | the same | DOMESTICALLY held equity only (taxable + retirement) | **0.4545** |

They are not in conflict and neither is wrong. They answer different questions: CRS's is the
rate faced by a **US saver**, ours is the rate on a **dollar of US AI surplus whoever holds
it**. For our object the foreign-inclusive base is the right one, because a foreign holder
genuinely bears close to no US shareholder-level tax and that dollar is still part of the
surplus the fiscal condition has to tax.

**CONSEQUENCE FOR OUR CHECK, AND A WITHDRAWAL.** The deferral factor we take from Table 5
row 3 is unaffected: row 3 is before the taxable-form adjustment, which is exactly why we
take it. But the check that compared our shareholder layer to Table 5's **row 4** band of
0.045 to 0.085 was comparing two different bases, and our own construction failed our own
check. The band must be rescaled by `theta / 0.4545` before comparison. See the corrected
paragraph below.

## 4. Plausibility target for the assembled shareholder layer, CORRECTED A118

**The sentence "our construction reproduces the published figure" is WITHDRAWN.** It was
true of the "around 3 percent" text figure and false of the Table 5 band, and it should never
have been asserted of both at once. What is true:

**(a) Against the text figure, a direct corroboration.** CRS summary, p. 2: "The overall
effective capital gains tax rate on corporate profits, adjusted for deferral, inflation,
stepped-up basis, tax-exempt assets in retirement accounts, and other features is small,
around 3%." Our shareholder layer is theta x 0.238 x deferral = 0.27 x 0.238 x 0.601 =
**0.0386** against **0.0315**, a gap of 0.007. This needs no rescaling: the text figure is
stated on the whole of corporate profits. **CORROBORATED.**

**(b) Against the Table 5 band, only after rescaling.** Table 5's 0.045 to 0.085 is on CRS's
foreign-excluded base. Rescaled to ours, `[0.045, 0.085] x 0.27 / 0.4545` = **0.0267 to
0.0505**, and 0.0386 sits inside it. Across our full theta range the band runs 0.0238 to
0.0524 and 0.0386 is inside throughout. **PASSES AS RESCALED. It does not and cannot land in
0.045 to 0.085 as printed** — across the whole swept space the layer runs 0.0235 to 0.0526 —
and describing it as doing so was wrong.

**(c) The base difference is carried as a marked sensitivity**, not resolved by assertion:
`framework/tau_k/tau_k_crs_theta_sensitivity.csv` runs the whole assembly at theta = 0.4545.
It matters — see the gate report in `framework/tau_k/README.md`.

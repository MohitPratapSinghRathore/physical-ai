# Novelty, and the kill criterion applied

**Searched and read 2026-09-21, before the specification was written. Only verified
references: every item below was retrieved and its abstract or text read, not recalled.**

## The kill criterion

> **KILL CRITERION:** if an existing paper already reports this boundary for the United
> States from microdata, say so first and stop.

**The criterion is NOT met. No paper found computes a growth threshold at which household
debt-service capacity is preserved under a shift of national income from labour to
capital, from US microdata.** The exercise proceeds.

**But the contribution is narrower than the question sounds**, and the reason is §2 below.

---

## 1. The nearest existing work, and what it leaves undone

**Bartscher, Kuhn, Schularick and Steins (2020), "Modigliani Meets Minsky: Inequality,
Debt, and Financial Fragility in America, 1950–2016", Federal Reserve Bank of New York
Staff Report 924.** Verified: title page and abstract read.

This is the closest thing that exists. It builds the SCF+ household-level dataset covering
the joint distribution of debt, income and wealth over seven decades, shows that
middle-class borrowing against housing wealth drove rising indebtedness, and — decisively
for novelty here — **stress-tests household debt-service capacity against interest-rate
and earnings shocks**, finding that household resilience declined over the debt boom,
especially in the lower half of the distribution and the middle class.

**So the machinery already exists.** Stress-testing SCF debt service is not new. What is
not done there:

1. **The shock is not a factor-share shift.** Interest rates and earnings are shocked; a
   reallocation of national income from wages to capital, with an explicit incidence on
   both sides, is not.
2. **There is no growth boundary.** No threshold is computed at which capacity is
   restored.
3. **There is no holder mapping.** Affected debt is not traced to who holds the claim.

The related companion, "The distribution of household debt in the United States,
1950–2022" (ScienceDirect S1094202525000195, same research group; the publisher returned
HTTP 403 so only the abstract via search was read — **flagged as incompletely verified**),
covers the same ground with the same stress-test design.

**Consequence for the contribution.** The novel elements are exactly three: the
factor-share shift as the shock with pre-stated incidence, the boundary as the object, and
the holder mapping. That is a narrower claim than "nobody has studied household debt
capacity under a labour-to-capital shift", and the write-up should make the narrower claim.

---

## 2. Why the boundary might still not be worth reporting

The honest risk, stated here rather than in a later caveat. The three novel elements are
novel partly because the first two are close to definitional:

- Once the incidence of the wage loss and the capital gain are **stated by convention**
  rather than estimated, the boundary is arithmetic. It is a well-specified,
  reproducible, contestable piece of arithmetic on measured distributions — which is what
  the measurement paper is made of — but it is not an estimate of anything.
- The holder mapping's answer is **already known**: the measurement paper reports that the
  federal government holds, guarantees or owes 79.4 percent of labour-backed claims. The
  household condition will re-derive a version of that, and re-deriving a known result is
  a consistency check, not a contribution.

SPECIFICATION.md §10 fixes in advance what would make the result uninteresting.

---

## 3. The required reading list, each verified

**Mian, Straub and Sufi, "Indebted Demand"** (NBER WP 26940, 2020; *Quarterly Journal of
Economics* 2021). Verified. Establishes that large household and government debt burdens
lower aggregate demand and natural rates, because borrowers and savers differ in their
marginal propensity to save out of permanent income. Rising inequality simultaneously
expands credit supply from the wealthy and debt demand from the less wealthy.
**Not this boundary:** a general-equilibrium theory of the natural rate, not a microdata
incidence calculation, and no debt-service capacity threshold.

**Mian, Straub and Sufi, "The Saving Glut of the Rich"** (NBER WP 26941, 2020; revised
July 2025). Verified. Top-1 percent saving surged since the 1980s; a new "unveiling"
method traces distributional household saving through the financial system using tax
records 1963–2019; this saving financed middle-class borrowing before 2008 and federal
debt after. **Not this boundary:** it is about who *funds* the debt, which is adjacent to
the holder mapping in §5 of the specification but is a flow-of-saving question, not a
debt-service-capacity question, and contains no growth threshold.

**Moll, Rachel and Restrepo, "Uneven Growth: Automation's Impact on Income and Wealth
Inequality"** (*Econometrica* 90(6), 2022, 2645–2683; NBER WP 28440; Bank of England WP
913). Verified. Automation raises the return to wealth, so its benefits accrue to capital
owners as well as high-skilled labour, and it can produce stagnant wages at the bottom;
a tractable theory linking technology to the distribution of income **and wealth**.
**Not this boundary:** this is the closest theoretical statement of the mechanism the
household condition prices, but it is a model of income and wealth distribution with **no
household debt, no debt service and no threshold**.

**Korinek and Stiglitz, "Artificial Intelligence and Its Implications for Income
Distribution and Unemployment"** (NBER WP 24174, 2017; in *The Economics of Artificial
Intelligence: An Agenda*, 2019). Verified. Two channels affect inequality — innovator
surplus and factor-price redistribution — and two produce technological unemployment,
efficiency wages and transition. Under plausible conditions non-distortionary taxation can
compensate losers. **Not this boundary:** theoretical, aggregate, no balance sheets. Its
compensation result is the intellectual ancestor of the arrangements in §7 of the
specification.

**Auclert, "Monetary Policy and the Redistribution Channel"** (*American Economic Review*
109(6), 2019, 2333–67; NBER WP 23451). Verified. Three redistribution channels when
winners and losers have different marginal propensities to consume: earnings
heterogeneity, a Fisher channel from unexpected inflation, and an interest-rate exposure
channel. Sufficient statistics computed from Italian and US microdata.
**Not this boundary, but the closest methodological relative.** Auclert's sufficient-
statistic approach to redistribution across a measured household distribution is the
template the household condition follows. The differences: his shock is monetary, his
outcome is consumption, and there is no debt-service threshold or growth boundary.

**Household-finance literature on payment-to-income and default.** Verified thresholds,
used in SPECIFICATION §5: the SCF's own `pir40` flag at PTI > 0.40; the conventional
"28/36 rule"; the CFPB Qualified Mortgage 43 percent debt-to-income limit as originally
written; and Fannie Mae Selling Guide B3-6-02, which caps manually underwritten loans at
36 percent (45 with compensating factors) and Desktop Underwriter cases at 50 percent.
These are underwriting standards and survey conventions, not estimated default boundaries,
and are used as **stated thresholds**, never as estimated discontinuities.

**Central-bank work on automation and household balance sheets.** Searched. The BIS
*Annual Economic Report* 2024 chapter III, "Artificial intelligence and the economy:
implications for central banks", covers distributional expectations (a BIS/New York Fed
household survey finds men, better-educated and higher-income respondents expect greater
benefit) but **does not compute balance-sheet incidence**. The Federal Reserve's
Distributional Financial Accounts and Enhanced Financial Accounts provide the
distributional *levels* this exercise reconciles to, not an analysis of this kind.

**Robinson, Silos and Vilán (2025), "Household Debt, the Labor Share, and Earnings
Inequality", Federal Reserve FEDS 2025-028.** Verified: title page, abstract and
introduction read. Found by search on exactly this question, and it is the one paper whose
**title** suggests the kill criterion is met. It is not.
**The causality runs the other way.** Falling real interest rates raised household debt;
higher debt made unemployment less sustainable; workers accepted lower wages to exit
unemployment; **therefore** the labour share fell by 6 percentage points, unemployment by
0.3, and the variance of log earnings rose from 0.66 to 0.75. It is a frictional
job-search model estimated on household data in which **debt causes the labour share**,
not one in which a labour-to-capital shift is priced onto debt service. No microdata
incidence exercise, no boundary.
**It must be cited prominently**, because a reader who knows it will assume the
endogeneity runs the other way, and the household condition's first-round convention
explicitly holds that channel shut.

**Bayraktar (2025), "Automation, Income Incidence, and Capital Accumulation in Incomplete
Markets"** (arXiv 2605.05127v2). Verified by fetch. A general-equilibrium model with
incomplete markets and heterogeneous wealth in which automation shifts income from labour
to capital; it identifies **critical growth thresholds** for whether households can sustain
consumption through capital accumulation. **This is the closest thing to a "boundary" in
the literature and must be cited as such.** It is not the same object: it is a threshold
inside a calibrated model of aggregate equilibrium dynamics, not first-round incidence
computed on a measured household distribution, and it does not use microdata or compute
payment-to-income ratios.

---

## 4. Verdict

**Kill criterion not met; proceed.** No US microdata boundary of this kind exists.

**Narrowed claim, to be made in these terms:** the contribution is (i) a factor-share
shift as the shock, with incidence stated by convention on both the wage and capital
sides, (ii) a growth boundary as the reported object, and (iii) the mapping of affected
debt to its holders. The stress-testing machinery is Bartscher et al.; the
sufficient-statistic method is Auclert; the mechanism is Moll, Rachel and Restrepo; the
compensation arrangements are Korinek and Stiglitz; and Bayraktar has a model-based
threshold that must not be conflated with this one.

**Incompletely verified, flagged:** "The distribution of household debt in the United
States, 1950–2022" (publisher returned HTTP 403; abstract only). The run session should
obtain the full text before the write-up, since it is the nearest neighbour and its
stress-test design may be closer than the abstract reveals.

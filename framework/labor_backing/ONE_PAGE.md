# B9. The labour backing ratio, on one page

**PROVISIONAL. Produced in one session (2026-09-20), so the same-session rule applies and
nothing here may be promoted to standing in this session. Nothing here has been
independently replicated; every quantity is queued for round two.**

## The definition

For each class of financial claim, the **direct labour backing share** is the fraction of
the cash flow that **directly** services it which is labour income. **First round only, one
step, no further tracing.** A class serviced out of business revenue has a direct labour
backing of **zero by rule**: corporate bonds, corporate and noncorporate business loans,
non-multifamily commercial mortgages, and corporate equity. That is not a claim that no
labour income ever reaches them. It is the paper's own first-round versus second-round
distinction applied to the liability side. The second-round version is B2 and is **never
blended into the headline**.

Multifamily mortgages are the one deliberate exception among property claims, because the
rent that services them is paid out of wages directly rather than out of tenant business
revenue.

Social insurance is a **memo item, outside the ratio**, at the payroll share of each fund's
own income: OASI 90.5, DI 95.7, HI 87.2 percent. Folding it in would double count against
Treasury debt.

## The headline, with its range

**In 2025 the direct labour backing ratio of the United States claim stock is 0.270:
40,380bn of 149,407bn dollars of claims are serviced, in the first round, out of wages.**

| | Value |
|---|---|
| Central | **0.270** |
| Range, every judgement call except the one-step rule | **0.267 to 0.297** |
| Range including the one-step rule | **0.267 to 0.475** |
| Second-round (B2) backing of business revenue, reported separately | 0.338 |
| Combined first and second round, **NOT the headline** | 0.475 |

**And the result that matters more than the ratio:**

**The federal government holds, guarantees or owes 79.4 percent of all labour-backed
claims** (32.6 percent as holder or guarantor, 54.3 percent as obligor, less the overlap).
That figure was produced from the Financial Accounts with no reference to the dose-response
table, and it lands inside the paper's independently derived **75.9 to 91.6 percent federal
share of first-round losses**. Two different measurements of the same concentration agree.

## Sensitivity to each judgement call, one at a time

| Judgement call | Move in the ratio |
|---|---|
| **The one-step rule** (business classes zero, against the B2 indirect share) | **+75.7 percent** |
| Federal receipts: SOI wage split against the 77.7 percent upper bound | +10.0 percent |
| Commercial mortgage treated like multifamily rather than zero | +7.1 percent |
| Mortgage backing: ACS service against the superseded A38 definition | -1.3 percent |
| State and local: wage split against all personal current taxes | +0.8 percent |
| Mortgage backing: ACS service against SIPP balances | -0.7 percent |
| Rent backing: engine core against the A38 definition | -0.2 percent |
| Other consumer: blend against the card share alone | -0.1 percent |

**One call moves the headline by 76 percent and every other call moves it by under 10.**
That is the single most important fact about this statistic and it was predicted in the
feasibility note before any of it was computed. The household and fiscal cells, which is
where this project's own measurement sits, are robust. **The definition is the whole
argument.**

On the holder side there are two more calls and they are larger than any of the above:

| Holder judgement call | Sovereign share |
|---|---|
| Central: agency pools, GSEs and the central bank all federal | **0.794** |
| Agency pools NOT federal, that is the guarantee ignored | 0.587 |
| Obligor leg excluded, holder and guarantor only | 0.321 |

## The two time series

`fig_labour_backing_two_panel.png`, 1947 to 2025, annual.

- **The ratio is nearly trendless and cyclical.** 0.288 in 1947, 0.275 in 1960, 0.330 in
  1980, 0.376 at the 2008 peak, 0.270 in 2025. It falls when equity is expensive, because
  equity is the largest zero-by-rule class, and it rises in credit booms and in equity
  busts. **It is as much an asset price series as a labour series**, and anyone reading it
  as a measure of labour dependence will misread it.
- **The sovereign share is not trendless and that is the finding.** The union share runs
  0.336 in 1970, 0.382 in 1980, 0.564 in 1990, 0.558 in 2008, 0.649 in 2010, 0.783 in 2020
  and **0.794 in 2025.** It roughly doubles in fifty years. The drivers are visible in the
  series: the growth of the GSEs and then the 2008 conservatorship, federal student lending
  after 2010 (the federal student holding is now 97.3 percent of the book), and the growth
  of Treasury debt itself, which is the obligor leg and the larger of the two.

**Data limits by year, stated.** The Z.1 claim levels and holder tables run from 1945. The
labour shares do not. The SOI wage share of AGI exists for 2021 to 2023 only and every
other year carries the nearest observed value, flagged row by row as
`soi_wage_share_is_held_constant`. The household working-core shares are a single ACS and
SIPP vintage held constant across the whole series. **So the pre-2021 series is a claim
stock and a holder map measured properly, with labour shares held fixed. It is not a
measurement of how labour backing itself moved.** The sovereign share is the part of the
series that is genuinely measured throughout, because holder shares come from Z.1 in every
year.

## What this lets someone say that they could not before

1. **A supervisor can put a number next to a capital ratio.** "Four fifths of the
   labour-backed claim stock sits with one counterparty, and that counterparty is the
   issuer of the risk-free asset" is a sentence that does not exist without this
   measurement.
2. **It converts a household-level finding into a system-level exposure.** The paper
   otherwise measures what happens to households and to the budget. This measures how much
   of the entire claim stock rests on the income that is falling.
3. **It makes the paper's central asymmetry quantitative and it makes it worse.** Leg A is
   2.1 percent of household debt by stock (claim 43). Against the labour-backed stock it is
   smaller still, and B11 shows the federal government holds **1.0 percent of the AI leg
   against 79.4 percent of the wage leg**. That is the least hedged position in the
   economy and it is now a measured statement.
4. **The connection test (B8) caught a specification error in the obvious formula.**
   Applying `(1 - R)` to credit claims is wrong: a displaced borrower's whole balance is at
   risk, not the lost-income fraction. Removing it moves auto loans from 0 of 8 to 7 of 8
   inside the benchmark loss band. `(1 - R)` belongs in the fiscal channel and nowhere else.

## Honest verdict: one section, not the central object

**One section.** Three reasons, in order of weight.

1. **The one-step rule moves the headline by 76 percent**, so the headline number is an
   artifact of a definitional choice that reasonable people will contest. A statistic whose
   central value is set by its own definition cannot carry a paper. It can support a
   section that states the definition and shows the sensitivity, which is what this is.
2. **The novelty gate narrowed sharply this session.** B7 established that the fiscal
   mechanism is not this project's discovery: Casas and Torres (2024), Korinek and Lockwood
   (2026), the RAND report by Price and Suresh (2026), the Windfall Trust (2026) and the
   IMF (2026) all have it. What survives is the liability side and the holder map, and the
   holder map is the stronger of the two.
3. **The durable finding is the sovereign concentration, not the ratio.** The ratio is the
   vehicle that gets you there. The result a reader will remember is that the federal
   government holds, guarantees or owes four fifths of the labour-backed claim stock and
   1.0 percent of the AI leg, and that the first number roughly doubled in fifty years.

**Recommendation.** Publish the ratio as the measurement that supports the holder section,
lead with the sovereign share and its time series, report the aggregate ratio with its
sensitivity table beside it, and do not put the ratio in the abstract. Report the corporate
and equity cells as zero by rule with the B2 extension stated separately, exactly as the
feasibility note recommended before any of it was built.

## What would change this verdict

If a direct approach to the Federal Reserve Financial Accounts team establishes that no
labour decomposition of the claim stock exists anywhere, and if the euro area case can be
built to the same standard, the ratio becomes a contribution in its own right rather than a
supporting measurement. Neither has been done.

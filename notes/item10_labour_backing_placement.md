# Labour backing accounts: the paper's named method contribution

**SUPERSEDES the previous framing of this note, which called the ratio "scaffolding".** It is
not scaffolding. **We introduce labour backing accounts: a decomposition of all US financial
claims by the income that services them and by who ultimately holds them.** Its outputs are
the ratio, the sovereign share, the holder map, the 1952 to 2025 series and the wage-quintile
breakdown.

**The ratio is reported as a PAIR, on the same first-round boundary as the sovereign share,
and the DEBT-ONLY pair is the one that goes in the abstract:**

| denominator | direct | including indirect |
|---|---|---|
| all claims | 0.270 | 0.475 |
| **DEBT ONLY**, excluding market-valued equity | **0.522** | **0.602** |

**About 52 percent of US debt is serviced directly out of wages.** The debt-only ratio exists
because the all-claims denominator is 48 percent corporate equity at market value, so the
all-claims ratio is partly an asset-price series. Debt-only is more stable (coefficient of
variation 0.051 against 0.094) and more robust to the one-step rule (15 percent against 76).
Code: `framework/labor_backing/build_debt_only.py`. **[M], provisional.**



Inputs: `framework/labor_backing/direct_ratio_latest.json`, `direct_ratio_timeseries.csv`,
`sensitivity.csv`, `quintile_labour_backing.csv` (B5), `cross_country_feasibility.md` (B6),
`holder_matrix_latest.csv`, and `item3_sovereign_robustness.csv` from item 3.

## 1. The ratio, with its full sensitivity

**Central: 0.270271 at the 2025 Z.1 annual vintage.** Of 149,407.2bn of claims, 40,380.5bn
are serviced first-round out of labour income.

| judgement call | ratio | move |
|---|---|---|
| **CENTRAL** | **0.270271** | |
| **THE ONE-STEP RULE**: business classes take the indirect share rather than zero | **0.474864** | **+75.7 pct** |
| federal receipts: the 77.7 percent upper bound | 0.297264 | +10.0 pct |
| commercial mortgage treated like multifamily | 0.289522 | +7.1 pct |
| mortgage backing: the superseded A38 definition | 0.266840 | -1.3 pct |
| state and local: all personal current taxes | 0.272291 | +0.8 pct |
| mortgage backing: SIPP balances | 0.268451 | -0.7 pct |
| rent backing: the A38 definition | 0.269805 | -0.2 pct |
| other consumer: the card share alone | 0.270080 | -0.1 pct |

**One-at-a-time range: 0.267 to 0.475.** The caveat travels with it: one at a time
UNDERSTATES the true range if the calls interact, and the one-step rule interacts with
everything.

## 2. Two things that must be said plainly wherever the ratio appears

**(a) The one-step rule moves it by 76 percent, and nothing else moves it by more than 10.**
The rule is that a claim's labour backing is the labour share of the cash flow that DIRECTLY
services it, one step, so corporate bonds, corporate and noncorporate business loans,
non-multifamily commercial mortgages and corporate equity are zero by rule. They are serviced
from business revenue. Labour reaches them only through demand, which is a second-round
channel measured separately. **Relax the rule to one more step and the ratio goes from 0.27
to 0.47.** The number is a measurement under a convention, and the convention is the single
largest judgement in the project.

**(b) It is partly an asset-price series, and the time series shows it directly.** The
denominator includes corporate equity at market value, 71,994.9bn of the 149,407.2bn total,
48 percent. So the ratio FALLS when equity rises and RISES when equity falls, independent of
anything happening to labour:

| year | direct ratio | what was happening to equity |
|---|---|---|
| 2000 | **0.2673** | the dot-com peak |
| 2008 | **0.3763** | after the crash |
| 2020 | 0.2907 | |
| 2025 | 0.2703 | |

**The 2008 reading is the highest in the modern series and it is high because equity fell,
not because labour backing rose.** Anyone using this ratio as a risk indicator would have
read it as least risky at the 2000 peak and most risky in 2009. That is the wrong sign for
an early warning, and it is why the ratio is presented as an accounting scaffold rather than
as an indicator.

This is also why the round two replicator's 0.168 against our 0.270271 is **not a
disagreement about labour backing at all.** The numerator agrees. The denominator differs:
212,644bn against our 149,407bn, driven almost entirely by corporate equity at a 2026Q2
market value of 123,687bn against our 2025 annual 71,995bn. **Two vintages of an asset-price
series, six months apart.** That is a further argument for the ratio being scaffolding.

## 3. What the scaffold actually produces, which IS the headline

The ratio is one number. The accounting that produces it produces four things that matter
more, and the paper should lead with these.

### (a) The sovereign share, and the 1952 to present series

| year | direct ratio | **sovereign union share** | federal held or guaranteed | household debt share of claims |
|---|---|---|---|---|
| 1952 | 0.2837 | 0.5227 | 0.0853 | 0.1475 |
| **1970** | 0.2767 | **0.3356** | 0.1204 | 0.2015 |
| 1980 | 0.3302 | 0.3816 | 0.1546 | 0.2512 |
| 1990 | 0.3549 | 0.5638 | 0.2482 | 0.2416 |
| 2000 | 0.2673 | 0.5617 | 0.3154 | 0.2072 |
| 2008 | 0.3763 | 0.5582 | 0.2977 | 0.2943 |
| 2010 | 0.3545 | 0.6492 | 0.3320 | 0.2453 |
| 2020 | 0.2907 | 0.7831 | 0.3923 | 0.1450 |
| **2025** | **0.2703** | **0.7936** | 0.3215 | 0.1264 |

**The ratio is flat across seventy-three years, moving between 0.267 and 0.376 with no trend.
The sovereign share of it traces a U: 0.523 in 1952, 0.336 in 1970, 0.794 in 2025.** That
contrast is the figure, and **the series must be shown from 1952: starting it at 1970 turns a
U into a doubling and misdescribes the history.**

**The 1952 level is wartime Treasury debt, not exposure to households.** That year the obligor
leg alone is 0.510 while the held-or-guaranteed leg is only 0.085. The fall to 1970 is that
debt shrinking against a growing claim stock, not a retreat from household credit.

The two steps back up are visible and datable: 1970 to 1990, the federal held-or-guaranteed
leg rises from 0.12 to 0.25 as the agency book grows; 2008 to 2020, the obligor leg takes over
as federal debt grows from 4,819bn to 15,642bn of labour-backed claims.

**And the qualification that must travel with the recent level: a large part of the rise since
2008 is growth in federal debt itself rather than new exposure to households.** The
held-or-guaranteed leg peaked at 0.392 in 2020 and has since FALLEN to 0.321, so the entire
net increase sits in the obligor leg.

### (b) The holder map

Of 40,380.5bn of labour-backed claims: **federal government 32.1 percent held or guaranteed,
55.2 percent as obligor, 79.4 percent as the union.** Banks 18.4 percent, rest of world 18.0,
other financial 15.3, households 6.1, state and local 4.6, insurers 2.0, pensions 1.1,
nonfinancial business 0.6, residual unallocated 1.6.

### (c) B5, by wage quintile. DELIVERED, and it does not clear the headline gate

`framework/labor_backing/quintile_labour_backing.csv`:

| quintile | wage bill share | labour-backed claims bn | **claims per unit of wage bill** |
|---|---|---|---|
| Q1 bottom | 0.0324 | 2,110.8 | **4.1489** |
| Q2 | 0.0895 | 1,983.3 | 1.4112 |
| Q3 middle | 0.1426 | 2,693.9 | 1.2031 |
| Q4 | 0.2233 | 3,647.6 | 1.0403 |
| Q5 top | 0.5122 | 5,266.8 | **0.6548** |

**The gradient is the finding: the bottom quintile carries 4.1 dollars of labour-backed
claims per dollar of wage bill and the top carries 0.65, a factor of 6.3.**

**The Q1 figure is REMOVED from the headline set by item 6 and the reason must travel with
the table.** The replicator's independent rebuild lands at 1.21 to 1.64, a factor of 2.5 to
3.4 away. The likely cause is theirs and they name it: they restrict to working-core
households with POSITIVE wage income, which removes exactly the near-zero-wage, high-debt
households that drive a ratio of 4.15. But the brief defines neither B5's universe nor its
normalisation, so **we cannot show that their reading is the wrong one**, and until we can
the Q1 number cannot be a headline. **Q5 at 0.6548 is within 13 to 18 percent of their
rebuild and survives.** The gradient direction survives. The magnitude of the bottom end does
not.

Publish the table with the gradient as the claim and Q1 flagged. Define the universe and the
normalisation in the brief before the next round.

### (d) B6, cross-country feasibility. EXISTS, and it is a feasibility assessment only

`framework/labor_backing/cross_country_feasibility.md`. **No ratio is computed for any
country other than the United States and none should be quoted.**

| economy | verdict |
|---|---|
| euro area | **computable.** The closest to a second full case: ECB whom-to-whom plus HFCS |
| United Kingdom | computable, shorter series, a defensible start in the late 1990s |
| Japan | computable but dominated by the JGB cell, so the answer turns on the revenue split rather than any survey. Worth doing because the composition is so different |
| Korea | computable with effort, and the most interesting after the US because the household leg is the largest |
| **India** | **NOT computable to a publishable standard.** High informality puts a large share of labour income outside both the tax base and the formal credit system, which is exactly the variable the statistic turns on. The honest output is a statement about why, not a number |

**The binding constraint everywhere is the third input**, a labour decomposition of the
servicing cash flow. The US is the best case and even there it is the weak one: the SOI wage
share of AGI exists for three years and is held constant outside them.

**B6 also carries the point that matters more than data availability**, and it belongs in the
emerging markets subsection rather than here: a sovereign that cannot borrow freely in its own
currency cannot absorb the shock the way the United States can, and the labour backing ratio
does not capture that by itself. The ratio measures how much of the claim stock sits on labour
income. It says nothing about what happens when that income falls.

## 4. The placement decision

**The ALL-CLAIMS ratio is scaffolding and does not go in the abstract. The DEBT-ONLY ratio
does**, beside the sovereign share, because it is stable, robust to the largest judgement
call, and answers a question a reader can check.

Reasons, in order:

1. Its largest single judgement moves it by 76 percent.
2. It is partly an asset-price series with the wrong sign for an indicator use.
3. Its novelty is "none located" on a non-systematic search, which is limitation L3.
4. The objects it produces, the sovereign share and the holder map, are robust where it is
   not: **no measurement call moves the sovereign share by more than 1.3 percent**, against
   76 percent on the ratio.

**What goes in the abstract is the holder gap: the federal government is exposed, as holder,
guarantor or debtor, on about four fifths of the claims paid directly from wages, and holds
about 1 percent of the claims on AI capital.** The ratio is how that was computed, and it is
reported in full, with its sensitivity, one section in.

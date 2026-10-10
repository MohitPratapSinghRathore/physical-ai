# What the referee's prescribed fixes did to Paper C

**2026-10-08.** The referee asked for three specific repairs to the decomposition and one new
test. All four were done. **Every one of them moves against the paper**, and together they
remove its motivation, its method and its policy contribution. Numbers in `decomp_v2.json`
and `decomp_v2_additive.json`.

## 1. The direct pro rata benchmark, as the referee specified it

The published paper used a pooled regression of household loss rates on loan shares. The
referee's point is that this is not the object a category allocation rule implies, which is
`l_hat(i,t) = sum_c w(i,c,t-1) * lambda(c,t)`. Built directly:

| object | R-squared |
|---|---|
| pooled share regression, as published | 0.1289 |
| **direct pro rata rule, raw level** | **-0.5567** |
| **direct pro rata rule, level normalised** | **+0.1530** |

The raw rule is worse than predicting the mean, because its level is forced by realised
category rates rather than fitted. The fair comparison is the normalised one, since a stress
test takes the aggregate as given, and on that basis the rule explains **15.3 percent**, not
the 9.7 percent the paper reports. The referee was right that the regression is a different
object; it was understating what the rule achieves, not overstating it.

## 2. An additive variance model with year effects and noise-corrected bank means

The published decomposition had no year effects and did not correct bank means for estimation
noise. Rebuilt so the shares sum to one by construction:

| component | share |
|---|---|
| business mix | 16.16% |
| year effects | 0.40% |
| bank-specific, uncorrected | 21.09% |
| transitory | 62.35% |
| **sum** | **100.00%** |

Correcting the bank term for estimation noise in bank means, `sigma2_eps * mean(1/T_i)`:

- estimation noise: 8.63 of the 21.09 points
- **bank-specific, corrected: 12.46%**, against 24.0% published
- forecastable, mix plus corrected bank: **28.62%**
- **mix share of the forecastable part: 56.5%**

**This overturns the paper's headline.** The abstract says business mix is only 28.9 percent of
forecastable dispersion. Measured with the rule the referee specified and with bank means
corrected for noise, it is **56.5 percent**. Pro rata captures the majority of the forecastable
cross-section, not under a third. Year effects are negligible at 0.40 percent, so that part of
the referee's conjecture does not bind.

## 3. The ICC versus autocorrelation tension, resolved against the method

The referee noted that `u = alpha_i + eps` implies an intraclass correlation near 0.266 while
the paper reports adjacent-year correlation 0.494, and that the gap matters because
Spearman-Brown assumes a particular repeated-measurement covariance.

| quantity | value |
|---|---|
| ICC implied by the corrected decomposition | 0.1665 |
| autocorrelation after mix only | 0.3839 |
| autocorrelation after mix and year effects | 0.3807 |
| **autocorrelation of the within-bank residual** | **0.1764** |

Year effects explain essentially none of the gap, 0.3839 to 0.3807. The gap is the last row:
**the transitory component is itself serially correlated at 0.176**, which is exactly the
structure Spearman-Brown does not assume. The referee's concern is confirmed and it is fatal to
the device as specified. The weight `w = T*rho/(1+(T-1)*rho)`, and the 0.845 the paper quotes
for fifteen years, are not the appropriate reliability weight for this covariance structure.

## 4. The backtest the referee asked for had already been run, and it is a null

The referee's recommended extension is precisely the design pre-registered in `PREREG_C.md`:
factors from pre-test information only, realised aggregate category losses held fixed, both
rules compared against realised bank-level losses, crisis years included. From `RESULTS_C.md`:

| window | pooled benchmark | own history | **pro rata** |
|---|---|---|---|
| test 2007-2010 | 0.0307 | 0.0168 | **0.0105** |
| test 2014-2019 | 0.0117 | 0.0117 | **0.0056** |

Pro rata has the lowest out-of-sample error in both windows. The referee states the fallback:
"If it does not perform better, the existing results remain an allocation-sensitivity finding."
That is where the paper lands.

Annual cross-sectional performance, which the referee also asked for, is the one place the
paper's instinct survives: mean R-squared 0.2315 pre-crisis, **0.0665 in the crisis**, 0.1801
after. The rule degrades sharply under stress. The published claim that the mix share "does not
rise under stress" was both wrongly worded and wrongly measured; the referee's correction that
11.6 exceeds the pooled 9.7 is right, and the annual cross-sections are the better way to see it.

## 5. The NCUA claim is false and the policy recommendation built on it is void

The paper states that the National Credit Union Administration does not collect charge-offs by
category, and calls the resulting collection recommendation "the most actionable thing in this
paper". **NCUA Form 5300 Schedule A Section 3 collects loan charge-offs and recoveries by
category**, items 1 to 20, Accounts 550 and 551. The real limitation is that our extracted
panel lacks those fields, which is ours and not the agency's, and that historical category
harmonisation across form revisions is work we did not do. The recommendation must be deleted
rather than softened, along with the equity argument in `sec_implications.tex` built entirely
on the false asymmetry.

## Standing

| element of the paper | status after the rebuild |
|---|---|
| motivation: pro rata discards most forecastable information | **overturned**, it captures 56.5% |
| method: Spearman-Brown reliability weight | **unjustified**, within-bank autocorrelation 0.176 |
| prediction: the replacement forecasts better | **null**, pro rata wins both windows |
| policy: NCUA should collect category charge-offs | **void**, it already does |
| finding: the breach set is sensitive to the allocation rule | **survives**, Jaccard 0.245 |
| finding: the rule degrades under stress | **survives**, annual R2 0.23 to 0.067 |

Two findings survive out of six elements. The paper is a short cautionary note on allocation
sensitivity, retitled as the referee suggests, with the alternative rule presented as *an*
alternative rather than a better one, since its shrinkage is no longer justified. It should not
be submitted as a Q1 paper and we will not present it as one.

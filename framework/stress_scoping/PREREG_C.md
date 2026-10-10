# PREREG_C: the test that decides whether Paper C exists

**Written and committed 2026-10-08, before any held-out outcome is opened. Branch
`stress-test-scoping` only. No re-specification after outcomes are opened.**

The novelty check (`NOVELTY_PROTOCOL.md`) fired on the original framing: the standard top-down
model does not allocate pro rata, and the question of whether to use or discard bank-specific
variation is already live in the literature. What survives is a narrower claim, and this test
decides whether even that survives.

---

## 1. The pooled benchmark, specified exactly

CLASS (Hirtle, Kovner, Vickery and Bhanot, FRBNY Staff Report 663) models each ratio as "an
autoregressive (AR(1)) term and a parsimonious set of macroeconomic variables", estimated by OLS
on pooled firm-level data, with the general form

    ratio(t,i) = alpha + beta * ratio(t-1,i) + delta * macro(t) + zeta * X(t,i) + eps(t,i)

with coefficients common across banks. We implement that form at the loan-category level:

    nco(i,c,t) = a_c + b_c * nco(i,c,t-1) + d_c' * M(t) + g_c' * W(i,t) + e

- `nco(i,c,t)`: net charge-offs in category c over the average balance in category c, bank i,
  year t, from Call Report `NT*` and `LN*` fields.
- Categories c: residential, credit card, other consumer. Household categories only, because the
  outcome is the household charge-off rate.
- `M(t)`: the unemployment rate, real GDP growth and the change in the delinquency rate on
  single-family residential mortgages, annual, from the FRED cache.
- `W(i,t)`: log assets and the tier 1 leverage ratio, the bank controls already in the panel.
- Estimated by OLS, pooled, coefficients common across banks, separately per category.

**This benchmark already contains bank-specific information through the AR(1) term.** That is
the point of using it, and it is what makes the test hard. A reader should expect the own-history
factor to add little, because the lagged dependent variable is itself a summary of the bank's own
recent loss experience. We state that expectation now so that a null is not reinterpreted later
as a surprise.

## 2. The reliability-weighted own-history allocation

As built in `reallocate.py`, with one change forced by this design: the Spearman-Brown weight and
the loss factors are estimated on the **training window only**, never on test years.

    lambda(i,c) = sum of charge-offs over sum of balances, bank i, category c, TRAINING years
    f(i,c)      = 1 + (lambda(i,c)/lambda(c) - 1) * w(i),  w(i) = T*rho / (1 + (T-1)*rho)

with `rho` the between-bank share of residual variance computed on the training window alone,
`T` the bank's count of training-window observations in that category, and `f` clipped to
[0.1, 5.0]. Predicted rate for bank i: `sum over c of s(i,c) * lambda_test(c) * f(i,c)`,
normalised so the predicted system household charge-off equals the realised one.

## 3. Pro rata, the shortcut comparison

Identical but with every `f(i,c) = 1`: `sum over c of s(i,c) * lambda_test(c)`, same
normalisation. This is what our own companion stress test did.

## 4. Held-out design, fixed now

The scenario is given in a stress test, so all three rules are normalised to the realised
system household charge-off rate in the test window. They therefore compete **only on the
cross-section**, which is the quantity in dispute. Two windows, both fixed before any outcome is
opened:

| window | training origin years | test origin years |
|---|---|---|
| **W1, contains the crisis** | 2001 to 2006 | **2007 to 2010** |
| **W2, post-crisis** | 2001 to 2013 | 2014 to 2019 |

Banks must appear in both training and test with a household book of at least one million
dollars. Outcome is winsorised at the first and ninety-ninth percentiles of the training window
only.

## 5. Metrics and the margin that must be cleared

**Primary.** Out-of-sample root mean squared error of the predicted bank-level household
charge-off rate against the realised rate, computed per window.

> **Margin: the own-history rule must reduce RMSE relative to the pooled benchmark by at least
> 2.0 percent in BOTH windows, including W1.**

**Secondary, reported but not decisive.** Overlap of the flagged set with realised adverse
outcomes. A bank is flagged if its predicted rate is in the top five percent. An adverse outcome
is a bank disappearing from the panel within three years of the test window while its final
observed tier 1 leverage ratio is below six percent, which is a crude proxy for failure or
distressed acquisition and is labelled as such. Reported as the lift in adverse-outcome rate
among flagged banks over the base rate, for each of the three rules.

## 6. Kill criterion, in numbers

> **KILL.** If the own-history rule fails to beat the pooled benchmark by 2.0 percent of RMSE in
> either window, Paper C does not proceed as a paper. It becomes a methods note reporting the
> decomposition and the negative result.

> **PROCEED.** Margin cleared in both windows.

> **INCONCLUSIVE.** Cleared in one window only. The paper does not proceed on that basis; the
> split result is reported and the decision deferred, with no further specification search.

Pro rata is not part of the kill criterion. It is reported for context because it is what the
companion stress test did, and beating it is not evidence of anything the field would credit.

## 7. The null wording, fixed now

If the kill fires, the result is reported as:

> Reliability-weighted own-history loss factors do not improve out-of-sample cross-sectional
> prediction of bank household charge-off rates beyond a pooled CLASS-style regression that
> already contains an autoregressive term. The persistent bank-specific variation that the
> decomposition identifies is therefore already captured by the lagged dependent variable in
> standard practice, and the case for carrying explicit own-history factors is not made.

That wording is fixed now and will be used verbatim if the kill fires.

## 8. Deviations

Anything that departs from this document is recorded in `RESULTS_C.md` under a heading
"Violations and deviations", before the results, whether or not it changes the verdict.

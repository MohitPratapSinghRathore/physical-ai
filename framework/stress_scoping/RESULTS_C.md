# RESULTS_C: the pre-registered test, and Paper C does not proceed

**Verdict: INCONCLUSIVE on the pre-registered rule, and the substance is worse than that.
Paper C does not proceed as a paper.** The reliability-weighted own-history allocation cleared
the two percent RMSE margin against the pooled CLASS-style benchmark in one of the two held-out
windows, which `PREREG_C.md` section 6 defines as inconclusive and explicitly excludes as a basis
for proceeding. It is worse than a split because the window it cleared, the crisis window, is one
where the benchmark itself broke, and because on the primary metric the pro rata shortcut beat
both the benchmark and the proposed replacement in both windows. Run against
`PREREG_C.md`, committed at `41cb8a5` before any held-out outcome was opened.

---

## Violations and deviations

Reported before the results, as section 8 of the pre-registration requires.

1. **MAE was computed and printed alongside RMSE.** Only RMSE was pre-registered as the primary
   metric. MAE plays no part in the verdict and is reported below only because suppressing a
   number already computed would be worse. It happens to favour the own-history rule in one
   window, and that is not a basis for anything.
2. **The adverse-outcome proxy is crude, as pre-stated.** A bank disappearing from the panel
   within three years with a final tier 1 leverage ratio below six percent conflates failure,
   distressed acquisition, ordinary acquisition and a filing gap. The pre-registration labelled
   it as such and that label stands.
3. **No re-specification occurred after outcomes were opened.** The windows, the margin, the kill
   criterion and the null wording are as committed.
4. The persistence parameter differs between windows, 0.4033 for the training window ending 2006
   and 0.2463 for the one ending 2013. That is by design: section 2 requires it to be estimated
   on training years only.
5. No loan category fell below the 200-training-row threshold that would have been logged.

## Primary metric: out-of-sample RMSE on bank-level household charge-off rates

| window | pooled CLASS-style | own-history | pro rata | own vs pooled | margin |
|---|---|---|---|---|---|
| **W1, train 2001-06, test 2007-10** | 0.030704 | 0.016804 | **0.010524** | +45.27% | clears |
| **W2, train 2001-13, test 2014-19** | 0.011723 | 0.011719 | **0.005583** | +0.03% | fails |

One window of two clears. Per section 6 that is **INCONCLUSIVE**, and the pre-registration states
that the paper does not proceed on that basis.

Two things make the substance worse than the label.

**The pro rata shortcut has the lowest RMSE in both windows.** It beats the sophisticated
benchmark and the proposed replacement, by a factor of nearly three in the crisis window. This
undercuts the paper's premise rather than just the own-history rule. It is also consistent with
our own decomposition: if only about a third of cross-sectional dispersion is forecastable, a
predictor that spreads to match observed dispersion is over-dispersed, and squared error punishes
that. A prediction clustered near the system rate is hard to beat on RMSE.

**The one window own-history cleared is a window where the benchmark broke.** The pooled
regression trained on the calm years 2001 to 2006 produces an RMSE of 0.0307 on 2007 to 2010,
nearly three times pro rata's. Its macro coefficients extrapolate badly out of the estimation
range. Beating a benchmark that has failed is not evidence that the replacement works.

## Secondary metric: overlap of the flagged set with adverse outcomes

Flagged is the top five percent of predicted rate. Not decisive, and reported with its
significance because the counts are small.

| window | rule | flagged | adverse | expected | lift | z |
|---|---|---|---|---|---|---|
| W1 | pooled CLASS-style | 410 | 19 | 23.4 | 0.81x | −0.94 |
| W1 | **own-history** | 410 | 34 | 23.4 | **1.45x** | **+2.25** |
| W1 | **pro rata** | 410 | 5 | 23.4 | **0.21x** | **−3.92** |
| W2 | pooled CLASS-style | 327 | 4 | 4.5 | 0.89x | −0.25 |
| W2 | own-history | 327 | 6 | 4.5 | 1.33x | +0.70 |
| W2 | pro rata | 327 | 1 | 4.5 | 0.22x | −1.66 |

The own-history rule is the only one with lift above one in both windows, but the evidence is
marginal in the crisis window and absent afterwards: z of +2.25 on 34 adverse banks against 23.4
expected, then +0.70 on six against four and a half. We will not call that a finding, and it does
not override a pre-registered primary metric.

**The one statistically solid result here is negative and it is about pro rata.** Its flagged set
contains significantly *fewer* adverse outcomes than chance in the crisis window, z = −3.92, and
the same sign post-crisis. Pro rata does not merely fail to find vulnerable banks; it
systematically flags banks that turn out safer than average. That is a sharper statement than
anything the paper was going to make, and it emerged from a secondary metric, so it is not a
finding of this test. It would need its own pre-registration with a tail metric as primary.

## The null, in the wording fixed in advance

Section 7 fixed the wording for a kill. The verdict is inconclusive rather than a kill, so the
fixed wording does not strictly apply, but the substantive finding is the one it describes and we
report it:

> Reliability-weighted own-history loss factors do not improve out-of-sample cross-sectional
> prediction of bank household charge-off rates beyond a pooled CLASS-style regression that
> already contains an autoregressive term. The persistent bank-specific variation that the
> decomposition identifies is therefore already captured by the lagged dependent variable in
> standard practice, and the case for carrying explicit own-history factors is not made.

The pre-registration anticipated this. Section 1 recorded, before any outcome was opened, that
the AR(1) term is itself a summary of a bank's own recent loss experience and that the own-history
factor should therefore be expected to add little. It added almost exactly nothing in W2, +0.03
percent.

## What this does to Paper C

It does not proceed. Together with the novelty check in `NOVELTY_PROTOCOL.md`, which found that
the standard top-down model does not allocate pro rata and that the use-or-discard question
belongs to Glasserman and Li, the position is:

- the framing was wrong, and
- the replacement does not beat the standard benchmark out of sample.

What survives is a methods note: the decomposition of dispersion into business mix, persistent
bank-specific and transitory components, with the observation that the persistent part is
largely already captured by an autoregressive term, and the negative result about pro rata's
flagged set. That is a short note, not a paper, and the branch stays unmerged.

## The tension worth recording for whoever picks this up

RMSE and the tail metric disagree, and they disagree in the direction the question cares about.
RMSE rewards predicting near the mean when most variation is noise, which is why pro rata wins
it. A stress test exists to rank the tail, where pro rata is significantly worse than chance.
Choosing RMSE as the primary metric was our decision, made in advance, and we are bound by it.
But the right test of an allocation rule for stress testing is probably a tail metric, and the
honest way to run it is a fresh pre-registration with that metric as primary and these results
cited as the reason for choosing it. We have not done that, and doing it on this data after
seeing these results would not be a clean test.

# PREREG_C3: the corrected test, with the power calculation that was missing

**Written and committed 2026-10-08, before any rule-level outcome in this design is opened.
Branch `stress-test-scoping`. No re-specification after outcomes are opened.**

## 0. Declaration: this is not blind

`PREREG_C2.md` was void. Its kill criterion could not fire and its outcome definition discarded
481 of 531 failures, both verifiable from design quantities alone. `RESULTS_C2.md` records the
run anyway, so **we have seen rule-level results under the broken design** and this test cannot
be called blind. The corrections below are forced by the two defects rather than chosen from
those results, and the hypotheses keep the same signs they had in `PREREG_C2.md`. A reader
should still discount this relative to a first-time pre-registration, and any paper has to
print this paragraph.

## 1. What changes, and why each change is forced

1. **Outcome counted during the test window, not after it.** Defect 2. A supervisor runs a
   stress test on the current balance sheet and asks who breaks next, so failures inside the
   horizon are the events of interest.
2. **All predictors from the training window only.** This is new and it closes a hole the void
   design had: averaging shares over a test window in which banks fail lets the outcome leak
   into the predictor. Everything is now as-of the last training year.
3. **No requirement that a bank appear in the test window.** Requiring it deletes exactly the
   banks that failed. This is most of why K was 45 instead of 453.
4. **A power calculation is required before the run**, and the verdict may only rest on arms
   where the criterion is reachable. Defect 1.

## 2. Power, computed from design quantities before any rule was run

Flag threshold five percent of the population, two-sided hypergeometric z.

| arm | N | failures K | base | flagged n | E[k] | downside z at k=0 | reachable |
|---|---|---|---|---|---|---|---|
| **W1 household** | 10,170 | 453 | 4.45% | 508 | 22.6 | **-4.99** | yes |
| **W1 commercial** | 9,998 | 457 | 4.57% | 499 | 22.8 | **-5.02** | yes |
| W2 household | 10,679 | 43 | 0.40% | 533 | 2.1 | -1.51 | **no** |
| W2 commercial | 10,532 | 43 | 0.41% | 526 | 2.1 | -1.51 | **no** |

Upside detection in W1 needs 32 of the 453 failures in the flagged set, a lift of 1.41, to
reach z > +1.96.

> **Fixed consequence: the verdict rests on the W1 arms only.** W2 cannot refute H1 whatever
> the truth, so it is reported as descriptive and is excluded from every kill criterion. This
> is stated now, not after seeing W2.

Only event counts were inspected to produce this table. No rule was evaluated.

## 3. Rules

Category set per portfolio: household is residential, credit card, other consumer; commercial
is commercial and industrial, non-residential real estate. Shares `s(i,c)` and own-history
ratios are computed on training years; `lambda_test(c)` is the realised system category rate in
the test window, so the scenario is given and the rules compete only on the cross-section.

- **R1 group rate (pro rata):** `sum_c s(i,c) * lambda_test(c)`.
- **R2 own history:** `R1 * f(i,c)`, `f = 1 + (lambda_train(i,c)/lambda_train(c) - 1) * w`,
  `w = T*rho/(1+(T-1)*rho)`, `rho` from the training window only, `f` clipped to [0.1, 5.0].
- **R3 mix residual:** rank on `sum_c s(i,c) * lambda_train(i,c)/lambda_train(c)`, mix level removed.

## 4. Hypotheses

> **H1.** The top five percent flagged by R1 contains fewer failures than chance, z < -1.96, in
> both W1 arms.
>
> **H2.** R1-flagged banks have higher median tier 1 leverage than the rest, and the gap is
> strictly larger for R1 than for R3. This is the mechanism, and the ordering is the part that
> identifies it.
>
> **H3.** R2 and R3 achieve lift above one, and at least one reaches z > +1.96, in both W1 arms.

## 5. Kill criteria, in numbers

> **KILL.** H1 fails in either W1 arm, meaning R1 does not reach z < -1.96. The anti-selection
> claim is abandoned for good and not tested again on these data.

> **PROCEED.** H1 holds in both W1 arms and H2 holds. The paper is the anti-selection paper.

> **PROCEED NARROWED.** H1 holds in both W1 arms but H2 fails. Anomaly reported without the
> capital mechanism.

> **MECHANISM ONLY.** H1 fails but H2 and H3 both hold in both W1 arms. Not a paper about
> allocation rules misranking failure. It is a shorter paper about what business-mix allocation
> measures, namely provisioned risk, with the failure-detection question reported as open. This
> cell is specified now because `RESULTS_C2.md` fell into an unanticipated cell and we are not
> repeating that.

## 6. Null wording, fixed now

If the kill fires:

> Group-rate loss allocation does not select against subsequent failure. In a properly powered
> test on 453 actual FDIC resolutions, the top five percent flagged by a business-mix rule did
> not contain significantly fewer failures than chance. The anti-selection statistic reported
> earlier in this project under a proxy outcome was an artifact of that proxy and is withdrawn.

## 7. Deviations

Recorded in `RESULTS_C3.md` under "Violations and deviations", before the results.

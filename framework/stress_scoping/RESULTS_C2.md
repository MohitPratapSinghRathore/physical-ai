# RESULTS_C2: the test was void by construction, and it killed a result I had believed

**Verdict: VOID, and separately the anti-selection finding does not survive contact with real
failure data.** The test pre-registered in `PREREG_C2.md` (`51bfcfd`) cannot be used, because
its kill criterion was mathematically unreachable before any data was seen. The run is
reported anyway, because it establishes something that does not depend on the broken criterion:
**the striking z = -3.92 anti-selection statistic in `RESULTS_C.md` was an artifact of the
proxy outcome, not a property of group-rate allocation.** The mechanism (H2) survives in all
four arms, including the untouched commercial portfolio.

---

## Violations and deviations

Reported before the results, as section 7 requires. The first two are mine and they are serious.

**1. The pre-registered kill criterion was unreachable. The test is void.** Section 5 required
z < -1.96 for H1. With the realised design quantities the minimum attainable z, achieved when
the flagged set contains *zero* failures, is:

| arm | banks N | failures K | flagged n | expected | best-case z | criterion reachable |
|---|---|---|---|---|---|---|
| household W1 | 8,188 | 45 | 409 | 2.25 | **-1.54** | no |
| commercial W1 | 8,065 | 45 | 403 | 2.25 | **-1.54** | no |
| household/commercial W2 | 6,536 | 4 | 326 | 0.20 | **-0.46** | no |

This depends only on N, K and n, so it could have been checked when the pre-registration was
written and was not. **A kill criterion that cannot fire is not a test.** No power calculation
appeared in `PREREG_C2.md`; that omission is the root cause and the correction is to require
one.

**2. The outcome definition discarded 481 of 531 relevant failures.** Section 4 defined the
outcome as failure "within three years of the end of the test window", implemented as the three
years *after* the window closed. For the W1 test window of 2007 to 2012 that excludes every
crisis failure: 481 failures occurred during the window, 50 in the three years after, and only
the 50 were counted. The crisis window was chosen precisely because it contains the failures,
and the outcome definition then threw them away.

**3. The results fall in a cell the pre-registration did not anticipate.** Section 5 provided
for H1 holding with H2 failing, but not for H1 failing with H2 holding, which is what happened.
We do not invent a verdict for that cell. The kill criterion as written fires, so the paper
does not proceed on anti-selection.

**4. We have now seen these numbers.** Any corrected test is therefore not fully blind, and
whatever is written next must say so.

## What the run shows, despite being void

### The anti-selection result does not replicate on real failures

| portfolio | window | rule | flagged failures | expected | lift | z |
|---|---|---|---|---|---|---|
| household | W1 | R1 group rate | 1 | 2.25 | 0.45x | -0.86 |
| household | W1 | R2 own history | 6 | 2.25 | **2.67x** | **+2.57** |
| household | W1 | R3 mix residual | 6 | 2.25 | **2.67x** | **+2.57** |
| commercial | W1 | R1 group rate | 1 | 2.25 | 0.45x | -0.86 |
| commercial | W1 | R2 own history | 2 | 2.25 | 0.89x | -0.17 |
| commercial | W1 | R3 mix residual | 1 | 2.25 | 0.45x | -0.86 |

W2 is omitted from interpretation: four failures, expected count 0.20, nothing is measurable.

**H1 fails.** The group rate flagged set is not significantly worse than chance against real
failures, in either portfolio. Given violation 1 it could not have been, so this is not
evidence against anti-selection either. The test is simply uninformative on H1.

**But the proxy result is now explained, and it was spurious.** `RESULTS_C.md` reported the
group rate flagged set at 0.21 times base with z = -3.92. That proxy defined an adverse
outcome as panel exit **with final tier 1 leverage below six percent**. The mechanism we were
proposing is that group-rate-flagged banks hold **more** capital. So the outcome variable and
the mechanism were the same variable: a rule that selects well-capitalised banks will
mechanically miss an outcome defined by low capital. The proxy built the finding in. With real
failures, which carry no capital condition by construction, the effect drops from z = -3.92 to
z = -0.86 and loses significance.

That is a correction to the previous session headline statistic, and it is the main thing this
run bought. The entry in the module A gate report that cites z = -3.92 has to be fixed.

### The mechanism, H2, holds everywhere including the untouched portfolio

Median tier 1 leverage, flagged versus the rest:

| portfolio | window | R1 group rate | R2 own history | R3 mix residual |
|---|---|---|---|---|
| household | W1 | **10.27 vs 9.38** | 9.35 vs 9.41 | 9.14 vs 9.42 |
| household | W2 | **10.95 vs 10.43** | 10.92 vs 10.43 | 10.39 vs 10.45 |
| commercial | W1 | **10.78 vs 9.34** | 9.75 vs 9.37 | 9.37 vs 9.38 |
| commercial | W2 | **11.30 vs 10.41** | 10.98 vs 10.42 | 10.77 vs 10.42 |

Four arms out of four, in the direction predicted, and the commercial portfolio has never been
used in any earlier arm of this work. The gradient across rules is the part that identifies the
mechanism: the gap is largest for the pure mix rule, smaller once own history is mixed in, and
essentially zero for the mix-residual rule, which is 9.14 against 9.42 and 9.37 against 9.38.
Taking business mix out of the ranking takes the capital correlation out with it. **Group-rate
allocation does rank banks by a dimension of risk they are already capitalised against.** What
the void test cannot establish is whether that costs it failure-detection power.

### A real positive result, on one window

In household W1 the rules built on own history flag real failures at 2.67 times base, six
against 2.25 expected, z = +2.57. That is the rule the pre-registered RMSE test in
`RESULTS_C.md` rejected, and it is measured here against actual FDIC resolutions. It does not
replicate in the commercial portfolio, z = -0.17, and W2 has no power. One window, one
portfolio, six events.

## Where this leaves the paper

The anti-selection paper does not exist. What is left is a confirmed mechanism, a corrected
error, and a single underpowered positive result. That is not a Q1 paper and we will not
present it as one.

A valid test is still available and the correction is forced by the defects rather than chosen
from the results: predict from information available at the end of the training window only,
and count failures **during** the test window, which restores roughly 400 events instead of 45
and makes the criterion reachable. That design is also the one that matches how a stress test
is actually used, since a supervisor allocates losses using the current balance sheet and asks
who breaks next. It is specified in `PREREG_C3.md`, with a power calculation required before
the run, and it carries the declaration that we have seen the numbers above.

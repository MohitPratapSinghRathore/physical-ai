# RESULTS_C3: KILL. Paper C does not exist, and this time the test could have said otherwise

**Verdict: KILL, on the criteria fixed in `PREREG_C3.md` (`86e74cb`) before outcomes were
opened.** The anti-selection hypothesis H1 failed in both primary arms of a test that was
properly powered to detect it: the minimum attainable z was -4.99 and -5.02, and the realised
values were -0.80 and -1.28. The capital mechanism H2 held in four arms of four. Detection H3
held in the household portfolio and failed in the commercial one, so the MECHANISM ONLY cell
did not fire either. Per section 5 the anti-selection claim is **abandoned for good and will
not be tested again on these data.**

---

## Violations and deviations

**1. This test was not blind, as declared in advance.** `PREREG_C3.md` section 0 recorded that
rule-level results had been seen under the void C2 design. That declaration stands and is the
main discount a reader should apply.

**2. No other deviations.** Windows, rules, flag threshold, hypotheses, the restriction of the
verdict to the W1 arms, the kill criteria and the null wording are all as committed. The power
table in section 2 was computed before the run and the realised design quantities match it
(N = 10,170 and 9,998; K = 453 and 457).

**3. H3 split across portfolios**, holding in household and failing in commercial. The
pre-registration required both arms, so this is a failure rather than a partial pass. It is
recorded here because the split is informative, not because it changes the verdict.

## The primary result: anti-selection is dead

| arm | rule | flagged failures | expected | lift | z | min attainable z |
|---|---|---|---|---|---|---|
| W1 household | **R1 group rate** | 19 | 22.6 | 0.84x | **-0.80** | -4.99 |
| W1 household | R2 own history | 37 | 22.6 | 1.64x | **+3.17** | |
| W1 household | R3 mix residual | 34 | 22.6 | 1.50x | **+2.51** | |
| W1 commercial | **R1 group rate** | 17 | 22.8 | 0.74x | **-1.28** | -5.02 |
| W1 commercial | R2 own history | 23 | 22.8 | 1.01x | +0.04 | |
| W1 commercial | R3 mix residual | 28 | 22.8 | 1.23x | +1.14 | |

453 and 457 actual FDIC resolutions, predictors strictly as-of the last training year, failures
counted inside the horizon. **H1 fails.** The group rate's lift is below one in all four arms,
0.84, 0.74, and 0.47 and 0.00 in the underpowered W2 arms, so the direction is consistent, but
it is not significant anywhere and the test had the power to find it if it were there. The
honest statement is that group-rate allocation is **uninformative** about which banks fail, not
that it is perverse.

The null wording fixed in section 6 applies and is used verbatim:

> Group-rate loss allocation does not select against subsequent failure. In a properly powered
> test on 453 actual FDIC resolutions, the top five percent flagged by a business-mix rule did
> not contain significantly fewer failures than chance. The anti-selection statistic reported
> earlier in this project under a proxy outcome was an artifact of that proxy and is withdrawn.

## What did hold: the capital mechanism, in four arms of four

Median tier 1 leverage gap, flagged minus the rest:

| arm | R1 group rate | R2 own history | R3 mix residual |
|---|---|---|---|
| W1 household | **+1.249** | +0.176 | -0.061 |
| W1 commercial | **+1.678** | +0.507 | +0.129 |
| W2 household | **+0.829** | -0.057 | -1.354 |
| W2 commercial | **+0.894** | -0.092 | -0.605 |

H2 required the R1 gap to be positive and strictly larger than the R3 gap, and it is, in every
arm including both commercial arms that no earlier work touched. The ordering is what
identifies the mechanism rather than the level: ranking on business mix selects banks holding
roughly one to one and three quarter points more tier 1 leverage, and taking the mix level out
of the ranking removes the capital correlation entirely or reverses it. **A group-rate
allocation ranks banks partly by a dimension of risk they are already capitalised against.**

That is a real, replicated finding. It is also, on its own, a mechanism with no demonstrated
cost, which is precisely why `PREREG_C3.md` made the MECHANISM ONLY cell conditional on H3 as
well. We wrote that condition before seeing these numbers and we are bound by it.

## The one thing that worked, and why it is not enough

In the household portfolio the own-history rule flagged 37 of 453 real failures against 22.6
expected, a lift of 1.64 at z = +3.17, and the mix-residual rule 34 at z = +2.51. This is the
rule that the RMSE test in `RESULTS_C.md` rejected, so the divergence between squared error and
failure detection is real, measured on actual resolutions, with no proxy and no leakage.

In the commercial portfolio the same rule gives z = +0.04. It does not generalise, and the
pre-registration demanded both arms for exactly this reason. One portfolio is not a finding.

## Standing

Three pre-registered tests, three negative verdicts:

| test | question | verdict |
|---|---|---|
| `NOVELTY_PROTOCOL.md` | is the original framing new | kill, framing not new |
| `RESULTS_C.md` | does own-history beat a pooled benchmark on RMSE | inconclusive, 1 of 2 windows, pro rata best |
| `RESULTS_C2.md` | does anti-selection replicate on real failures | void by construction, proxy artifact found |
| `RESULTS_C3.md` | does it replicate in a powered test | **kill** |

**Paper C does not exist.** What exists is a methods note, and its contents are now fixed by
what survived: the dispersion decomposition; the capital-gradient mechanism as a descriptive
result with its cost undemonstrated; the null on uniform reliability weighting; the withdrawal
of the spurious anti-selection statistic; and the household-only detection result reported as
non-generalising. No further specification will be tried on these data.

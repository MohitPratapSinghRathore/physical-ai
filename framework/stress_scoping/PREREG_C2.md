# PREREG_C2: the confirmatory test for the reframed Paper C

**Written and committed 2026-10-08, before any outcome in the confirmatory arm is opened.
Branch `stress-test-scoping`. No re-specification after outcomes are opened.**

The novelty gate (`NOVELTY_RESULT_C2.md`, criteria at `1f958aa`) returned PARTIAL and rescoped
the paper to community bank stress testing. This document fixes the test of the surviving
claim.

## 1. What is already seen, declared plainly

The hypothesis below was **formed by looking at data**. The anti-selection of the group-rate
rule was a pre-registered *secondary* outcome in `PREREG_C.md` section 5, so it was a
pre-specified metric rather than a post-hoc trawl, but it was not the primary metric and the
mechanism was found afterwards by inspection. Specifically, already seen:

- household portfolios, test windows 2007-2010 and 2014-2019, with a **proxy** outcome
  (panel exit within three years at final tier 1 leverage below six percent);
- that under that proxy the group-rate flagged set ran at 0.21 times base, z = -3.92;
- that group-rate-flagged banks had higher median tier 1 leverage, 11.0 against 9.3;
- that the between-bank variance share rises from 0.017 to 0.462 across quintiles of the
  persistent component.

Nothing below may be read as independent confirmation except the arms labelled CONFIRMATORY.

## 2. The two genuinely untouched things this test uses

**(a) Real failures instead of a proxy.** The outcome becomes actual FDIC failure, from the
FDIC `failures` API, 586 resolutions 2000-2023 joined to the panel on `CERT`. No Paper C work
has used this file. It replaces the proxy rather than supplementing it.

**(b) Commercial portfolios.** Every test so far was household-only by construction. The
commercial categories, commercial and industrial (`LNCI`/`NTCI`) and non-residential real
estate (`LNRENRES`/`NTRENRES`), have never been used in any arm of this work. They are a
different portfolio in the same institutions, so the mechanism either generalises or it does
not.

## 3. Hypotheses, stated as directional predictions

From M1, that a group-rate allocation ranks banks by the risk they already hold capital
against:

> **H1 (CONFIRMATORY).** In the commercial portfolio, the top five percent flagged by the
> group-rate rule will contain **fewer** subsequent FDIC failures than chance, with z < -1.96.
>
> **H2 (CONFIRMATORY).** In the same portfolio, group-rate-flagged banks will have **higher**
> median tier 1 leverage than unflagged banks. This is the mechanism. If H2 fails while H1
> holds, M1 is refuted as the explanation and the paper reports an unexplained anomaly.
>
> **H3.** A rule built on the mix-**residual**, the component the group rate discards, will
> have a flagged-set lift above one, higher than the group rate's, in both portfolios.

## 4. Specification, fixed

- Sample: panel banks, origin years 2001 to 2021, household or commercial book at least one
  million dollars for the relevant portfolio.
- Rules, all normalised so predicted system loss equals realised system loss in the test
  window, so they compete only on the cross-section:
  - **R1 group rate (pro rata):** `sum_c s(i,c) * lambda_test(c)`, `s` the bank's category shares.
  - **R2 own history:** `R1 * f(i,c)` with `f = 1 + (lambda_train(i,c)/lambda_train(c) - 1) * w`,
    `w = T*rho/(1+(T-1)*rho)`, `rho` and `lambda_train` from TRAINING years only, `f` clipped
    to [0.1, 5.0].
  - **R3 mix residual:** rank on `lambda_train(i,c)/lambda_train(c)` alone, mix removed.
- Windows, fixed now: **train 2001-2006 / test 2007-2012** (contains the 478 crisis-era
  failures) and **train 2001-2013 / test 2014-2019**.
- Outcome: FDIC failure with `FAILDATE` within three years of the end of the test window.
- Flag threshold: top five percent of predicted rate. No other threshold is reported as primary.
- Metric: lift of the failure rate among flagged banks over the base rate, with a
  hypergeometric z. Two-sided.

## 5. Kill criteria, in numbers

> **KILL.** If H1 fails in the commercial portfolio, meaning the group rate's flagged set is
> not significantly worse than chance at z < -1.96, the anti-selection result does not
> generalise beyond household portfolios and the proxy outcome. The paper does not proceed as
> a paper and becomes a note reporting a household-only, proxy-only finding.

> **PROCEED.** H1 and H2 both hold in the commercial portfolio in at least one window, and H1
> is not reversed in sign in the other.

> **PROCEED NARROWED.** H1 holds but H2 fails. The anomaly is reported without the capital
> mechanism, M1 is withdrawn, and the paper is explicitly weaker for it.

H3 is not part of the kill criterion. It is the constructive half and its failure costs the
paper a remedy, not its finding.

## 6. The null wording, fixed now

If the kill fires:

> The anti-selection of group-rate loss allocation does not generalise. In commercial
> portfolios the rule's flagged set does not contain significantly fewer subsequent failures
> than chance, so the household result reported under a proxy outcome should be read as
> specific to household portfolios or to that proxy, and not as a general property of
> group-rate allocation.

## 7. Deviations

Anything departing from this document is recorded in `RESULTS_C2.md` under "Violations and
deviations", before the results, whether or not it changes the verdict.

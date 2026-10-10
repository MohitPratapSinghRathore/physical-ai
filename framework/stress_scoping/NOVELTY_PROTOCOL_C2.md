# NOVELTY_PROTOCOL_C2: kill criteria for the reframed Paper C, fixed before searching

**2026-10-08. Branch `stress-test-scoping`. Written before any search is run.**

The first framing of Paper C died here (`NOVELTY_PROTOCOL.md`) and then died again on the
pre-registered test (`RESULTS_C.md`). This is a different claim, and it gets the same gate,
written first.

## The claim being checked

Two mechanisms, both measured on the training window before this protocol was written:

- **M1, provisioned-risk anti-selection.** A pro rata loss allocation ranks institutions by
  business mix. Mix is the component of credit risk institutions already know and hold capital
  against: the top five percent flagged by pro rata have median tier 1 leverage 11.0 against
  9.3 for the rest. Failure depends on the unprovisioned residual, which pro rata discards by
  construction. Hence a rule can minimise squared error and still rank the failure tail worse
  than chance.
- **M2, heteroskedastic reliability.** The between-bank share of residual variance rises
  monotonically from 0.017 to 0.462 across quintiles of the absolute persistent component. A
  single global reliability weight therefore over-shrinks the informative tail.

## Kill criteria, fixed now

> **KILL-A.** If published work already states that pro rata or business-mix loss allocation
> anti-selects on realised failure *because* mix is the provisioned component of risk, the
> paper does not proceed on M1.

> **KILL-B.** If published work already derives or documents that minimising squared error in
> stress-test loss allocation is opposed in sign to tail identification, the paper does not
> proceed on the headline.

> **KILL-C.** If signal-dependent (non-uniform) reliability shrinkage is already standard in
> this literature, the constructive contribution is not available and the paper becomes a
> comment rather than a paper.

> **PARTIAL.** If the general point that fit statistics are poor validators of early-warning
> models is established but the specific mechanism and the allocation-rule setting are not, the
> paper proceeds with the contribution narrowed to the mechanism and the measurement, and the
> prior work cited as the frame rather than as background.

## Searches to run

1. pro rata loan loss allocation stress test bank-specific dispersion
2. squared error versus ranking / discrimination tradeoff early warning bank failure
3. capital endogeneity to business mix, risk-based capital anticipates known loss
4. shrinkage estimators heteroskedastic reliability signal-dependent James-Stein panel
5. CLASS / top-down supervisory stress test allocation granularity
6. AUC versus RMSE model validation bank failure prediction

Results and the verdict go in `NOVELTY_RESULT_C2.md`, with each kill criterion answered
explicitly and the searches that were run listed whether or not they found anything.

# NOVELTY_RESULT_C2: verdict against the criteria fixed in NOVELTY_PROTOCOL_C2

**2026-10-08. Criteria committed at `1f958aa` before any search was run.**

## Verdict

**PARTIAL, with a scope correction.** The paper proceeds, narrowed. M1 survives as the
contribution, M2 is demoted from a method to an application of known methods, the headline is
narrowed because the general frame is established, and the population the claim is made about
has to change.

## Each criterion, answered

**KILL-A, does published work already say mix-based allocation anti-selects on failure because
mix is the provisioned component? DOES NOT FIRE.** Nothing found states that consequence. The
premise it rests on is, however, well established and will be cited as foundation rather than
treated as our own: portfolio risk and bank capital are simultaneously and positively related,
so banks hold more capital against riskier books (OCC Economics WP 1994-6; the risk-based
capital literature generally). We take an established fact about capital and derive an
unestablished consequence for allocation rules. That is the contribution.

**KILL-B, is the squared-error versus tail-ranking tension already known? PARTIALLY FIRES.**
The distinction between calibration metrics such as RMSE and discrimination metrics such as
AUC is textbook, as is the point that the two can diverge and that a monotone transformation
leaves AUC unchanged while destroying calibration. Our headline cannot be that the metrics
diverge. What is not established, and what we claim, is the stronger statement: in this setting
the RMSE-minimising rule is not merely uninformative but **significantly anti-correlated** with
realised distress, with the flagged set running at 0.21 times the base adverse rate, z = -3.92,
and with a named mechanism for the sign. Anti-selection is a different object from divergence.
The calibration-versus-discrimination literature is cited as the frame.

**KILL-C, is signal-dependent shrinkage already standard? FIRES.** Shrinkage with
heteroskedastic variances and unit-specific shrinkage factors is a developed literature:
Xie, Kou and Brown (2012) on the heteroskedastic normal-means problem by unbiased risk
estimation, the SURE line that follows it, and the optimal-shrinkage-for-panel-fixed-effects
work. Our M2 finding, that the between-bank variance share rises from 0.017 to 0.462 across
quintiles of the persistent component so a single global reliability weight over-shrinks the
tail, is a correct and useful measurement in this application, but the remedy is off-the-shelf.
**M2 is presented as applying known shrinkage machinery that this applied literature does not
use, not as a new estimator.** Any wording that implied otherwise is a claim we cannot make.

## Scope correction, which the search forced

A search snippet asserted that the Federal Reserve forecasts industry losses and distributes
them to firms by asset size. **We fetched the source and it says the opposite.** DFAST uses
firm-specific supervisory models and the published material emphasises cross-firm variation in
modelled loss rates, not top-down allocation. Had we not checked, the paper would have opened
on a false statement of supervisory practice. The round-one finding stands: the large-bank
supervisory stress test does not allocate pro rata.

Where group-rate allocation *is* actual practice is **community bank stress testing**, which
is also what our sample is: median log assets 11.5, so roughly a hundred-million-dollar
institution, not a DFAST filer. In that setting a group or industry loss rate applied to a
bank's own category mix is the standard method, including the OCC's reference historical
loan-loss rates issued for community bank stress testing (OCC Bulletin 2012-33) and the
historical-loss approach of Fang and Yeager (*Journal of Banking and Finance*, 2020), which
applies group-level percentile charge-off rates to banks grouped by geography. It is also what
our own companion module did.

**The paper is therefore about community bank stress testing, not about DFAST**, and must say
so in the title or the abstract rather than leaving the reader to assume the large-bank
exercise. Fang and Yeager are the direct comparator and must be engaged rather than cited:
their use of a ninetieth-percentile group rate rather than a mean already addresses severity,
though not the cross-sectional ranking problem we identify, and the paper has to be explicit
about that difference.

## What the paper can claim after this gate

1. The decomposition: business mix explains 9.7 percent of cross-sectional dispersion in
   community bank household loss rates and 28.9 percent of the forecastable part.
2. **M1, the mechanism and the anti-selection result.** Group-rate allocation ranks banks by
   the component of risk they already hold capital against, so its flagged set is
   significantly safer than chance. New, and the paper's centre.
3. The pre-registered negative result on uniform reliability weighting, reported as a null.
4. M2 as an application: reliability is strongly signal-dependent here, and standard
   heteroskedastic shrinkage is the appropriate off-the-shelf response.

What it may not claim: that metric divergence is new, that signal-dependent shrinkage is new,
or anything at all about the large-bank supervisory stress test.

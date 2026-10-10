# Paper C novelty check: does the field already use bank-specific loss histories?

**Protocol fixed 2026-10-08, before searching. Verdict recorded below the line.**

## The claim at risk

Paper C says a top-down stress test run across many institutions allocates each category's
loss pro rata by holdings, and that doing so discards most of the forecastable
cross-sectional dispersion. If the standard top-down models already estimate
institution-specific loss relationships from each bank's own history, the critique targets a
method the field does not use.

## Kill criteria, fixed before searching

**KILL-A.** If the New York Fed's CLASS model, or another widely used top-down model,
estimates bank-specific charge-off relationships from each bank's own history, then "pro rata
hides vulnerable banks" is not a critique of standard practice. The paper must then name
exactly who uses pro rata, and the contribution narrows to quantifying what that shortcut
costs plus the shrinkage construction.

**KILL-B.** If a published paper already measures how much of the cross-sectional dispersion
in bank loss rates is attributable to business mix versus institution-specific effects, the
decomposition is not novel and the paper loses its measured half.

**NARROW.** If bank-specific estimation is standard only for the large supervisory sample and
not for the thousands of banks outside it, the paper survives but must be reframed around the
coverage gap rather than around top-down practice in general.

**SURVIVE.** If neither fires, the framing stands as written.

---

## Verdict, 2026-10-08: KILL-A FIRES, KILL-B PARTIALLY FIRES

### What the search found

**CLASS does not allocate pro rata.** The New York Fed model (Hirtle, Kovner, Vickery and
Bhanot, Staff Report 663) projects net charge-offs on fifteen loan categories using "a mix of
time-series models and firm-level pooled regression models", estimated by OLS on Y-9C and Call
data. Pooled means coefficients common across banks, driven by macroeconomic variables. That is
a more sophisticated object than allocating a system loss in proportion to holdings. So the
standard top-down model is not the thing this paper criticises.

**Bank heterogeneity in stress-test loss models is published and debated.** Glasserman and Li,
"Should Bank Stress Tests Be Fair?", Management Science 2024, state the problem directly: the
Federal Reserve "uses confidential models to evaluate bank-specific outcomes for bank-specific
portfolios in shared stress scenarios. As a matter of policy, the same models are used for all
banks, despite considerable heterogeneity across institutions". They argue for "estimating and
then discarding centered bank fixed effects as preferable to simply ignoring differences across
banks", and the pooled restriction is reported as rejected.

**A historical-loss approach for community banks already exists.** Fang and Yeager, Journal of
Banking and Finance 118 (2020), build a top-down community bank stress test that groups banks by
geography and applies the ninetieth percentile charge-off rates observed in 2008 to 2012. That
is bank-linked historical loss experience applied to exactly the population this paper claimed
as its coverage gap.

### What that does to the paper

**KILL-A fires.** "Pro rata hides vulnerable banks in stress tests" announces a critique of
standard practice that standard practice does not follow. Pro rata by holdings is what our own
companion stress test did, and what applications that take a system loss rate and scale it by
exposure do. It is not what CLASS does. The title and the framing are not defensible as written.

**KILL-B partially fires.** The question of whether bank-specific variation should be used or
discarded is not ours: it is Glasserman and Li's, in a top-five journal, two years ago. Our
decomposition into business mix, persistent bank-specific and transitory components, with the
shrinkage weight pinned by the measured reliability rather than chosen, is an increment on a
question already asked rather than a new question.

**The coverage-gap reframing is also weakened**, because Fang and Yeager occupy it.

### What survives, and it is a different paper

1. The decomposition itself: business mix explains 9.7 percent of total dispersion and 28.9
   percent of the forecastable part, and no more under stress. We have not located that
   quantification elsewhere, but it is now an increment to a live debate rather than the opening
   of one.
2. The Spearman-Brown reliability weighting, which answers "discard or keep" with a number
   derived from the data rather than a judgement. That speaks directly to Glasserman and Li's
   estimate-then-discard recommendation.
3. The demonstration that the choice changes the identified set.

The honest framing is a contribution to the fairness-versus-accuracy debate on common models,
not a critique of pro rata. That is a narrower and better-grounded paper, and it has to be
rewritten rather than retitled.

### Recommendation

Do not develop Paper C further on the current framing. Either rebuild it around the Glasserman
and Li question, with their paper and Fang and Yeager as the reference points and a direct
comparison against a CLASS-style pooled regression as the benchmark, or shelve it. The branch
stays unmerged either way.

# Scoping the three reframings of the stress test

**2026-10-07. Branch `stress-test-scoping`, not merged. Feasibility tests, not a paper.**

**Superseded in part, 2026-10-07.** The infrastructure reframing that came out of this
scoping was killed on two counts afterwards: its framing failed the novelty check in
`NOVELTY_PROTOCOL.md`, and the replacement allocation rule failed the pre-registered
out-of-sample test in `PREREG_C.md`. The verdict and the numbers are in `RESULTS_C.md`.
Read this document as the record of what was tried, not as a live plan.

I proposed three ways the stress-test module might become a Q1 paper, ranked by increasing work
and payoff: the credit union paper, the relief-design paper, the infrastructure paper. I then
tested all three against the data rather than leaving them as suggestions.

**The ranking inverts.** The one I said I would back is blocked, the one I rated lowest is the
strongest, and the middle one is thinner than it looked. What follows is the evidence.

---

## 1. The infrastructure paper: strongest, and better than I rated it

### The criticism is now quantified

The institution-level stress test allocates losses pro rata by loan category, so business mix is
the only source of dispersion by construction. The paper concedes this and says "the true spread
is wider". How much wider was never measured. It is now.

Using the predictive panel, 138,239 bank-years across 9,973 banks, regressing the realised
household loan loss rate on the seven loan-share controls that define business mix:

| | share of total dispersion |
|---|---|
| explained by business mix | **9.7%** |
| persistent bank-specific, not mix | 24.0% |
| transitory | 66.3% |

Most year-to-year variation is noise, which no stress test can or should chase. The quantity
that matters is the **forecastable** part, business mix plus persistent bank-specific effects,
and of that **business mix is 28.9 percent**. The bank-specific residual has a year-to-year
autocorrelation of 0.494, so it is genuinely persistent rather than a relabelled error term.

Stable across outcome definitions: 28.9 percent on one-year household losses, 30.5 on
three-year, 31.6 on total loans.

### It does not improve under stress, which is the part that matters

A stress test exists to rank institutions under stress, so the obvious objection is that
business mix might explain more when losses are large. It does not:

| window | mix R² |
|---|---|
| pre-crisis 2001 to 2006 | 0.162 |
| **crisis 2007 to 2010** | **0.116** |
| post-crisis 2011 to 2021 | 0.091 |

In the crisis window business mix explains 11.6 percent of dispersion. The pro rata assumption
discards roughly the same proportion of real variation under stress as in calm periods.

### The fix is available for banks and not for credit unions

FDIC call reports carry net charge-offs by category per institution: `NTRERES`, `NTCRCD`,
`NTAUTO`, `NTCONOTH`, `NTCI`, `NTRENRES`. These are already fetched for 146,813 bank-years in
the predictive work, so institution-specific historical loss rates by category are available for
all 4,296 banks without new collection.

The NCUA panel carries balances and net worth only. There are no charge-off fields in it, so the
same fix is not available for the 4,292 credit unions without re-parsing the NCUA 5300 call
report. That asymmetry has to be stated in any paper that claims to cover all 8,588.

### Verdict

A methods paper with a quantified motivation and a demonstrated fix. "Institution-level stress
tests that allocate losses pro rata by category capture under a third of the forecastable
cross-sectional dispersion, and no more under stress" is a result in its own right, and the
replacement is implementable on existing data for the bank half of the panel. This is the one to
build. *Journal of Banking and Finance* or *Journal of Financial Stability* on genre.

---

## 2. The credit union paper: thinner than I rated it

At the ten percent level, the only one inside the observed data:

| class | n | assets, $bn | breaching | % of institutions | % of class assets |
|---|---|---|---|---|---|
| under $100m | 2,472 | 75.2 | 38 | 1.54 | 1.01 |
| $100m to $1bn | 1,341 | 448.4 | 8 | 0.60 | 0.83 |
| $1bn to $10bn | 454 | 1,307.7 | 2 | 0.44 | 0.36 |
| over $10bn | 25 | 691.4 | 0 | 0.00 | 0.00 |
| **all credit unions** | **4,292** | **2,522.6** | **48** | **1.12** | **0.37** |

The size gradient is real and monotone, and the largest credit unions are untouched. But the
magnitude is 48 institutions out of 4,292, and the breaching ones are concentrated in a class
holding $75bn, about three percent of credit union assets. Substantial numbers appear only at
25 percent displacement and above, which is outside the range where the reemployment
relationship was fitted.

It also inherits the pro rata problem **with no fix available**, because the NCUA panel has no
charge-off data. The paper would have to carry the full force of section 1 above without being
able to answer it.

### Verdict

A short note or a Q3 paper, not Q1. The institutional story is nice and the finding is real, but
"48 small credit unions breach under an assumed shock, and more would under a larger one we
cannot calibrate" will not carry a field journal.

---

## 3. The relief-design paper: blocked, and I was wrong to back it

I said the duration-matched experiment would make this a Q1 paper. I did not check whether the
experiment can be run. It cannot, as things stand.

**The relief module has no time dimension at all.** It is a single-period calculation.
`framework/revision_r1/a3_relief_feedback.py` scales the second round by a factor derived from
the retained wage share; there is no horizon, no quarters, no path. The duration mismatch is
named in its own output text as a limitation, not implemented as a variable.

**The path is one of the three explicitly unsourced elements.** Appendix B.2 lists what has no
source: the shape of the loss curve beyond the supervisory point, the propensity ranges, and
"the path itself". A duration-matched experiment requires exactly that path.

**The project holds no quarterly supervisory trajectory.** The DFAST material on hand is a
results PDF with loss totals, not the scenario's quarterly variable path.

So running the experiment means constructing its key input. That is assuming the answer, not
testing it, and it would convert a flagged weakness into an unflagged one.

### What would unblock it

The Federal Reserve publishes the severely adverse scenario as a quarterly path of macro
variables, which is sourceable. Using it would still require a mapping from that macro path to a
quarterly loss path by category, and that mapping would itself need sourcing rather than
assuming. That is a genuine project with a sourcing problem at its centre, not a single
experiment.

### Verdict

Not a route to Q1 on current inputs. Revisit only if the macro-to-loss mapping can be sourced.

---

## What I got wrong

I ranked these by increasing payoff as credit union, relief, infrastructure, and said the relief
paper was the one I would back. Having tested them: the relief paper is the one that cannot be
run, the credit union result is the thinnest, and the infrastructure paper is the only one with
both a quantified motivation and an implementable fix. The recommendation I gave was the inverse
of the one the evidence supports.

## What this does not change

None of this rehabilitates the stress test as it stands, and none of it argues for attaching the
module to either finished paper. The infrastructure finding is an argument for a **new** paper
about stress-test methodology, whose contribution is the dispersion decomposition and the
institution-specific replacement. The existing module would be an application in it, not the
point of it.

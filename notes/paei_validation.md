# Step 1: PAEI validation

Status: **partially complete. The acceptance gate cannot be resolved with the data
available.** Read Section 4 before using any of this.

Date: 2026-09-19.

---

## 1. What was run

PAEI (911 O*NET occupations, O*NET 31.0) against two published exposure indices.

| Index | Level | Construct | Match rate |
|---|---|---|---|
| Felten, Raj and Seamans AIOE | SOC 6-digit | cognitive AI exposure | 85.7% |
| Eloundou et al. GPT exposure (alpha, beta, zeta; model and human rated) | O*NET-SOC 8-digit | LLM exposure | 100.0% |

Employment weights are ACS PUMS 2023 person weights aggregated to SOC through the Census
OCCP crosswalk, because BLS OES returns HTTP 403 to this environment. Employment weight
coverage is 50.3 percent of PAEI occupations: the Census OCCP crosswalk is coarser than
O*NET detail, so roughly half of O*NET occupations carry no PUMS employment of their own.
Employment-weighted correlations are therefore computed over the covered subset and are
reported alongside, not instead of, the unweighted figures.

## 2. Discriminant validity: PASSES, strongly

PAEI claims to measure exposure to EMBODIED automation. The established indices measure
COGNITIVE automation. If PAEI were a relabelling, the correlations would be high and
positive. They are high and NEGATIVE.

| Our measure | Index | Pearson | Spearman | Pearson (emp-wt) |
|---|---|---|---|---|
| PAEI | Felten AIOE | **-0.878** | -0.889 | -0.862 |
| PAEI | Eloundou GPT beta | **-0.758** | -0.785 | -0.758 |
| PAEI | Eloundou GPT zeta | -0.812 | -0.808 | -0.837 |
| PAEI | Eloundou human-rated beta | -0.807 | -0.818 | -0.777 |
| PAEI | Eloundou GPT alpha (strict) | -0.333 | -0.359 | -0.234 |

PAEI is close to the mirror image of cognitive AI exposure. On the discriminant criterion
the index is clearly not a repackaging of an existing measure.

## 3. The problem this exposes, which is the real finding of Step 1

Decomposing PAEI into its two factors changes the reading considerably:

| Our measure | vs Felten AIOE | vs Eloundou beta |
|---|---|---|
| PAEI (P x S) | -0.878 | -0.758 |
| **embodiment P alone** | **-0.935** | **-0.810** |
| **structure S alone** | **+0.027** | **+0.127** |

Two things follow.

**First, P is almost exactly the negative of cognitive exposure.** At r = -0.935 against
AIOE, the embodiment factor is very nearly a mirror of a published index. "Physical jobs are
the ones cognitive AI does not touch" is not a new finding and cannot be sold as one. Nearly
all of PAEI's discriminant validity is inherited from P, and P is the unoriginal half of
the index.

**Second, S is orthogonal to everything published.** At r = +0.03 to +0.13, the structure
factor carries information that no existing index contains. That is where any novelty in
PAEI lives. It is also, at present, the component with no external validation whatsoever.

So the honest statement of what PAEI at c = 0 is: a known quantity (embodiment, r = -0.94
with an existing index) multiplied by an unvalidated novel quantity (structure). The
multiplicative form means S modulates rather than dominates, which is why PAEI's own
correlation (-0.878) sits close to P's (-0.935).

This makes external validation of S the critical path, not a nice-to-have.

## 4. The acceptance gate CANNOT be resolved

MASTER_PROMPT_PHASE2.md Step 1 sets the gate as:

> if PAEI correlates above roughly 0.8 with Webb's robot score, PAEI at c = 0 is not novel.

**Webb's scores could not be obtained.** Webb distributes occupation-level exposure scores
only through his own website. As of 2026-09-19, `michaelwebb.co/data.html` returns 404,
`web.stanford.edu/~mww/` returns 404, and no verified machine-readable file was located.
Frey and Osborne probabilities were likewise not obtained in a verified machine-readable
form; numerous third-party reproductions exist but none that can be verified against the
original, and Rule 1 forbids using them.

The gate is stated against the ROBOT score specifically, and that is the correct test:
Webb's robot measure is the only published index that targets the same technology PAEI
targets. AIOE and Eloundou are cognitive measures and can only establish discriminant
validity, which they do.

**Therefore: whether PAEI at c = 0 is novel is UNRESOLVED.** It is not established as
novel, and it is not refuted. What is established is that it is not a cognitive index.

The convergent tests specified in Step 1 are all blocked for the same underlying reason:

| Convergent test | Blocker |
|---|---|
| Webb robot score | not publicly retrievable |
| Acemoglu and Restrepo robot exposure by industry | requires IFR robot data (paid) |
| IFR robot density by industry | paid, owner decision pending |
| BLS OES employment weights | HTTP 403 to this environment |

My expectation, stated in advance of having the data so it can be checked against me later:
P will correlate strongly with Webb's robot score, plausibly above 0.8, because both are
substantially "does this job involve physical work". PAEI as a whole should correlate less,
because S pulls it away. If that is what the data shows, the gate's verdict is that PAEI at
c = 0 is NOT novel, and the novelty claim rests entirely on PAEI(c) in Step 2, exactly as
the prompt anticipates.

## 5. A near-precedent that must be cited

Schaal, J. (2025), "A theory-based AI automation exposure index: Applying Moravec's Paradox
to the US labor market", arXiv 2510.13369, submitted 15 October 2025.

This applies Moravec's paradox to O*NET to build an exposure index, which is PAEI's stated
theoretical hook. It is not the same index:

| | Schaal (2025) | PAEI |
|---|---|---|
| Unit | 19,000 O*NET tasks, LLM-scored | 911 occupations, O*NET descriptor scales |
| Dimensions | performance variance, tacit knowledge, data abundance, algorithmic gaps | embodiment, environmental structure |
| Form | not specified in abstract | multiplicative, two factor |
| Target | fundamental automatability, largely cognitive | embodied automation |
| Result | management, STEM, sciences MOST exposed; maintenance, agriculture, construction LEAST | the reverse ordering |
| Scenario-conditional | no | PAEI(c) in Step 2 |

The two indices rank occupations in close to opposite order while invoking the same
theory. That is a genuinely interesting contrast and should be used as such, but the claim
"we apply Moravec's paradox to occupational exposure" is no longer unclaimed and must not
be written as though it were. Added to the WS0 matrix.

## 6. Not yet done from Step 1

- Sensitivity: multiplicative versus additive versus geometric mean, alternative descriptor
  sets, leave-one-descriptor-out, rank stability (Spearman between variants, share of
  occupations changing quintile).
- Task-level audit: 200 O*NET tasks, two independent LLM raters plus rubric, 50 flagged for
  owner review, inter-rater agreement (Cohen's kappa or Krippendorff's alpha).
- Industry and commuting-zone aggregation for convergent validity.
- The correlation matrix figure.

These are worth doing, but none of them can substitute for the convergent test. Running
internal sensitivity analyses on an index whose novel component has no external validation
would produce a lot of numbers and no additional confidence.

## 7. What the owner needs to decide

1. **Webb's scores.** Options: email Webb directly (he has historically shared on request);
   check whether the owner's institution has access to a replication archive; or accept
   that the c = 0 novelty question stays open and rest the claim on PAEI(c).
2. **IFR World Robotics.** Paid. It is the only route to the "PAEI should predict where
   robots already are" test, which is the strongest available convergent validation of S.
3. Whether to proceed to Step 2 (PAEI(c)) with the gate unresolved. My recommendation is
   yes: the prompt already anticipates that the novelty may rest on PAEI(c), and Step 2
   does not depend on the answer.

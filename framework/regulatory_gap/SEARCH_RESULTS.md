# The four-option search, scored

**2026-09-21. Criteria for all four options were written to `CRITERIA.md` and committed
before any of them was run.**

## Outcome

| Option | Criterion | Result |
|---|---|---|
| **1. Regulatory-treatment gap** | weights and exemptions verified; quantity > 50 percent; not already established | **PASS** (novelty partial) |
| **2. Euro-area replication** | sovereign-share gap ≥ 15 percentage points | **FAIL** — gap is 10.9pp |
| **3. Household-side ownership constraint** | absent from the models, not already standard | **FAIL** — already being modelled |
| **4. Descriptive co-movement** | interpretable and stable, not a common-trend artefact | **FAIL** — the only stable relationship is definitional |

**Four hypotheses were tried and one passed.**

---

## What four tries does to option 1

This has to be said before anything else, because it changes how option 1 should be read.

A result that survives **one** pre-stated test is stronger evidence than the same result
selected from **four**. Under four independent attempts, the chance of at least one passing
by luck alone is roughly four times the chance of any single one doing so. Option 1's
numbers are not statistical estimates — they are an arithmetic mapping of published
regulation onto measured accounts, so there is no p-value to inflate — but the *choice to
report it* was made after three others failed, and a reader is entitled to know that.

**Option 1 stands, with that discount attached.** Its content does not depend on sampling:
89.4 percent of the labour-backed claim stock carries a risk weight at or below 20 percent
whether or not three other ideas failed. What the multiplicity affects is the claim that this
was the *interesting* thing to look at, and that claim is now weaker.

---

## Option 2 — euro-area replication. FAILED.

**Criterion:** a sovereign-share gap of 15 percentage points or more against the US 0.794.

**Result: 10.9 percentage points. Not met.**

| | Level (EUR tn) | β | Labour-backed (EUR tn) |
|---|---|---|---|
| Government debt (securities + loans) | 14.57 | 0.658 | 9.59 |
| Household loans, long term | 7.68 | 0.840 | 6.45 |
| Household loans, short term | 0.31 | 0.780 | 0.24 |
| Non-financial corporate debt | 16.33 | 0.000 | 0.00 |

- Euro-area labour-backed stock: **EUR 16.28tn**
- Sovereign obligor leg **0.589**, holder leg **0.095**
- **Euro-area sovereign share 0.684** against the **US 0.794**

**And the sensitivity makes it worse, not better.** The criterion is met only if the
euro-area government revenue coefficient is **below 0.55**. Euro-area states run *larger*
social insurance systems than the US, so their revenue is plausibly *more* labour-linked than
the US 0.658, not less — which pushes the euro share up and the gap down. Across β from 0.50
to 0.90 the gap runs 16.1pp to 5.3pp, and is under the threshold at every value from 0.55 up.

**What this actually establishes, stated as what it is and not as a rescue.** The exercise
was looking for evidence that the US 0.794 is a fact about US institutional structure — the
agency and GSE guarantee system. It found the opposite: **the euro area reaches 0.684 with no
agency guarantee system at all**, purely because government debt is large and labour-backed
while household debt is small. The sovereign concentration of labour-backed claims looks like
a general feature of advanced economies rather than a US quirk.

That is interesting, and it is **not what was being tested**. The pre-stated criterion
failed, and reinterpreting a failed criterion into a success is exactly the move this
project's discipline exists to prevent. Recorded as a failure with an observation attached.

**Limitations, which also bear on the failure.** This is a **structure-only** comparison: the
euro-area claim levels are measured (ECB QSA, 2025-Q4), but the labour backing coefficients
are the US ones applied unchanged, because no euro-area ACS/SIPP/SOI equivalent was built.
The ECB QSA carries **no issuer-counterpart detail** — every series has counterpart sector
`S1` — so it is not a holder map, and the holder leg here is a bound rather than a
measurement. The household loan split into mortgage and consumer uses long versus short
maturity as a proxy. A build "to the same standard as the US number", which is what the
criterion asked for, was **not achieved**, and that alone is sufficient for the failure.

---

## Option 3 — the household-side ownership constraint. FAILED.

**Criterion:** the constraint that a large share of corporate equity never reaches a
household must be absent from the models of the labour-to-capital shift, and not already
standard.

**Result: the point is already being modelled. Not met.**

Mian–Straub–Sufi, Moll–Rachel–Restrepo and Korinek–Stiglitz do not impose it — that part of
the criterion holds. But the criterion also fails if the point is **already standard**, and
it is: recent work in exactly this space carries the constraint explicitly. Bayraktar (arXiv
2605.05127), already read during the household-condition novelty check, places "the foreign
owner" outside the model boundary and makes "the share passed through to domestic asset
holders" the parameter that "determines the gap between the productive-capital return and the
return received by households". A 2026 agent-based paper (arXiv 2606.20649) models capital
mobility on the same logic.

The underlying ownership fact — that foreigners hold roughly 42 percent of US corporate
equity — is also standard in tax policy, which is where Rosenthal and Mucciolo published it.

**The measurement remains sound and the finding remains true.** What fails is the claim that
it is novel as a modelling constraint, which is what the criterion asked.

---

## Option 4 — descriptive co-movement. FAILED.

**Criterion:** the sovereign share co-moves with an identifiable macro-financial series,
interpretably and stably across subperiods, and not as a common-trend artefact.

Tested on **first differences**, not levels, precisely because the criterion names the
common-trend artefact. Overlap 2005–2025, 21 years.

| Series | Levels r | Differences r | First half | Second half | Verdict |
|---|---|---|---|---|---|
| Federal debt / GDP | +0.986 | **+0.731** | +0.792 | +0.889 | stable but **definitional** |
| 10-year Treasury yield | −0.533 | −0.574 | −0.589 | −0.612 | stable, but mechanical and n = 20 |
| Labour share, nonfarm | −0.841 | −0.112 | −0.528 | **+0.768** | **sign flips** |
| Household debt / GDP | −0.889 | +0.032 | −0.137 | **+0.865** | **sign flips** |

**The only strong stable relationship is with federal debt to GDP, and it is not a finding:
the sovereign share's obligor leg *is* federal debt.** That is a definitional overlap, worse
than the common trend the criterion was written to exclude.

The 10-year yield relationship is stable in sign and magnitude, but rests on 20 differences
with an obvious mechanical channel (lower yields, more issuance, larger obligor leg).

**The two economically interesting candidates both fail on stability, with the sign reversing
between halves.** Reporting the levels correlations — −0.84 with the labour share, −0.89 with
household debt to GDP — would have looked impressive and would have been spurious.

The hard limit in `CRITERIA.md` holds regardless: nothing here is predictive or causal, and
nothing here rehabilitates the validation pilot's null.

---

## Where this leaves things

**One usable result from four attempts**, with the multiplicity disclosed. Option 1's
regulatory mapping is real, its novelty is confined to the income-source dimension, and it is
now known to have been selected from a set of four.

**The most interesting thing the failures produced** is option 2's: the sovereign
concentration of labour-backed claims is not distinctively American. That undercuts a claim
the measurement paper does not actually make, and it points at a better question than the one
asked — not *why is the US concentrated*, but *why is this the general structure of advanced
economies*. Pursuing it would need euro-area coefficients built to the US standard, which is
a real project and not a session.

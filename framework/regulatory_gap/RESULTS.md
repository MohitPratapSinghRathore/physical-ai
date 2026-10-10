# Option 1: the regulatory-treatment gap

**2026-09-21, branch `regulatory-gap`. Criteria fixed in `CRITERIA.md` before any
regulatory source was read or any quantity computed.**

> **SUPERSEDED BY `SEARCH_RESULTS.md`.** When this was written, option 1 was the only
> option attempted. Options 2, 3 and 4 were subsequently run at the owner's instruction and
> **all three failed**. **Four hypotheses were tried and one passed**, so the selection
> discount described in `SEARCH_RESULTS.md` applies to everything below. The content of this
> document is unchanged and correct; what changed is that reporting it was a choice made
> after three other ideas failed, and a reader is entitled to know that.

**Status: a MAPPING of measured accounts onto published regulation.** Not an estimate, not a
forecast, not a causal claim.

---

## The finding

**Capital regulation has no dimension that registers what income services a claim, and 89
percent of the labour-backed claim stock sits in the categories the framework treats as
nearly riskless.**

| | Labour-backed claims | All claims |
|---|---|---|
| Total | **$40,380bn** | $149,407bn |
| Share at risk weight ≤ 20 percent | **89.4%** | 35.7% |
| Share at risk weight **zero** | **59.2%** | — |
| Share exempt from the single-counterparty credit limit | **92.3%** | — |
| Exposure-weighted mean risk weight | **0.144** | **1.622** |

The labour-backed stock carries an average risk weight **eleven times lower** than the claim
stock as a whole.

**At the bank level**, where the capital requirement actually binds:

| | Value |
|---|---|
| Bank-held labour-backed claims | **$7,445bn** |
| Of which at risk weight ≤ 20 percent | **$4,880bn (65.5%)** |
| Bank-held labour-backed mean risk weight | 0.388 |
| **Capital not required**, if re-weighted at 50 percent (the residential mortgage weight) | **$146bn** |
| **Capital not required**, if re-weighted at 100 percent (the consumer weight) | **$341bn** |

For scale, total tier 1 capital across US insured institutions is roughly $2,200bn, so the
range is **7 to 15 percent of system tier 1**. Material, not apocalyptic, and stated that way.

---

## The regulatory facts, from primary text

**Risk weights, 12 CFR 217.32** (US Basel III standardised approach), verified from the
regulation:

| Exposure | Weight | Citation |
|---|---|---|
| US government, its central bank, a US government agency | **0%** | 217.32(a)(1)(i) |
| Portion directly and unconditionally guaranteed by the US government | **0%** | 217.32(a)(1)(i) |
| GSE exposure other than equity or preferred stock | **20%** | 217.32(c)(1) |
| General obligation of a US public sector entity | 20% | 217.32(e) |
| First-lien residential mortgage, prudently underwritten, not 90 days past due | 50% | 217.32(g)(1) |
| Other first-lien and all junior-lien residential mortgage | 100% | 217.32(g)(2) |
| Corporate exposures | 100% | 217.32(f)(1) |
| Publicly traded equity | 300% | 217.52–53 |

**Concentration limits, 12 CFR 252.77.** The single-counterparty credit limit exempts direct
claims on, and portions fully guaranteed as to principal and interest by, Fannie Mae and
Freddie Mac while under FHFA conservatorship, alongside other categories. Sovereign exposures
are exempt from large-exposure limits in the Basel framework generally.

**Both pre-stated criteria 1 and 2 are met.**

---

## Why this is not just the sovereign-bank nexus

**The concentration argument is well established and I am not claiming it.** That zero risk
weights plus large-exposure exemptions conceal concentration is a mature literature — Abad
(CEMFI/ECB), Baule, Beckmann and Tallau, the CEPR columns on zero-risk-weight capital
misallocation, and the ECB's own supervisory speeches. A reader who knows that literature
should not be told this is new.

**What is new is the dimension.** Searches on capital regulation against income source,
wage income, and the labour share of claim backing return nothing: **no framework, rule or
paper weights a claim by the income that services it.** The nexus literature is about the
*credit risk of the sovereign*. This is about the *income that services the claim*, and the
two are different questions that happen to have the same answer here.

That is a narrow novelty claim and it should be made narrowly.

> **NARROWED FURTHER, 2026-09-21, by `framework/paper_scoping/NOVELTY_RESULT.md`.**
> **Acharya (2011), "Governments as Shadow Banks"** (Federal Reserve, Regulation of Systemic
> Risk conference) is closer than the euro-area nexus papers cited above. He connects the
> **US government mortgage guarantee specifically** to the **20 percent Basel risk weight
> specifically**, calling it "artificial leverage advantages for housing assets — a
> deliberate regulatory subsidy mechanism". **So connecting government guarantees to
> favourable risk weights is not new; it is fifteen years old.** What survives is only that
> the *wage-backed* share of the claim stock has not been computed against the weights, and
> that no rule has a field for the income servicing a claim. The arithmetic below is
> unaffected; this paragraph's novelty claim is.

---

## The objection that matters, and the answer

**Objection.** A risk weight measures the obligor's credit risk. The US government gets zero
because it can tax and can issue its own currency. What income *ultimately* services the
claim is irrelevant to whether the obligor pays. The mapping is therefore a category error.

**This is the strongest objection and it is not fully answerable.** But it is weaker than it
looks, for a reason internal to the accounts:

- **65.8 percent of Treasury debt is serviced, in the first round, out of wages** — that is
  the labour backing coefficient for the Treasury class, from social insurance contributions
  in full plus the wage share of the individual income tax.
- The sovereign's capacity to substitute *capital* taxation for that wage base is exactly
  what the fiscal condition tests, and it **fails**: the assembled capital rate is 0.086
  against a required 0.110 to 0.137.

So the zero risk weight rests on a sovereign capacity that the same accounts say is impaired
by the same shock that impairs the household claims. **The collateral and the guarantor draw
on one income base, and the framework has no field in which that common factor could be
recorded.** Diversification across claim classes does not help against a single factor.

That is the argument. It is a framing argument supported by an arithmetic mapping, as
`CRITERIA.md` said in advance it would be, and it stands or falls on whether a reader accepts
that first-round wage dependence is the right way to see the common factor.

---

## What I will not lean on

**The correlation between labour backing and risk weight across claim classes** is −0.49
unweighted and −0.84 claim-weighted. **It should not be reported.** With thirteen classes,
coefficients that are near-binary by the accounts' own one-step rule, and two classes
(Treasury at $33.9tn / 0 percent and corporate equity at $72.0tn / 300 percent) dominating
the weighting, that number is arithmetic on two observations wearing the clothes of a
correlation. Excluding equity it falls to −0.42 on thirteen points.

The share statistics above require no correlation and do not depend on it.

---

## Criteria, scored

| Criterion | Result |
|---|---|
| 1. Risk weights as expected, primary-sourced | **PASS** — 12 CFR 217.32 verified |
| 2. Concentration rules exempt the concentrated counterparty | **PASS** — 12 CFR 252.77 verified |
| 3a. Quantity above 50 percent | **PASS** — 89.4 percent of the stock, 65.5 percent bank-held |
| 3b. Not already established | **PARTIAL** — the concentration point is established; the income-source dimension is not |

**Verdict: option 1 works out, with the novelty confined to the income-source dimension.**

---

## What this supports, and what it does not

**Supports:** a supervisory observation with a number attached — that the wage-backed share
of the claim stock is concentrated in exactly the categories carrying the lowest weights and
the widest concentration exemptions, that no rule has a field for the common factor, and that
the capital not required against bank-held wage-backed claims is $146bn to $341bn depending
on the counterfactual weight.

**Does not support:** any claim that banks are undercapitalised, that the weights are
mis-set, or that a wage-dependence weight should be introduced. Those require a loss model,
and the validation pilot already established that this measure does not predict bank losses.
**This is a statement about what the framework can see, not about what will happen.**

It also does not revive the pilot's null. The two are consistent: labour backing does not
predict which bank loses money, *and* the framework has no way to register the aggregate
common factor. The first is about cross-sectional discrimination; the second about a
system-level exposure. A2's published wording — aggregate accounting, not an
institution-level risk measure — is exactly right and this result sits inside it.

---

## Files

| File | Contents |
|---|---|
| `CRITERIA.md` | success criteria, committed before running |
| `map_risk_weights.py` | the mapping |
| `risk_weight_map.csv`, `risk_weight_map.json` | claim-stock level |
| `bank_held_map.csv` | bank-held level |

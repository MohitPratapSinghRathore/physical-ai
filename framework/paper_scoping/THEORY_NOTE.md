# What labour backing is, formally

**2026-09-22. A theoretical note, written after six empirical hypotheses were tested and one
survived narrowly. Status: framing, not measurement. No new data.**

---

## 0. What equations can and cannot do here

Writing λ = Σ_c w_c β_c and taking logarithms does not make labour backing more true or more
important. Formalism adds nothing to a measurement; it can only (a) show the measurement is
an instance of something general, (b) generate an implication the measurement alone does not,
or (c) explain *why* a measured pattern holds. Anything else is notation.

So this note tests four candidate formalisations against those three standards. **Three fail
and are reported as failures.** One survives, and its ceiling is stated.

---

## 1. Notation

Claim stock `D = Σ_c D_c`, class shares `w_c = D_c / D`. Each class has a **factor loading**
`β_c ∈ [0,1]`: the share of the cash flow servicing it that is labour income, first round.

    λ  ≡  Σ_c w_c β_c                    labour backing of the claim stock
    α  ≡  wL / Y                         labour share of income
    Λ_L ≡ λD / (αY)                      labour-backed claims per dollar of labour income
    Λ_K ≡ (1−λ)D / ((1−α)Y)              capital-backed claims per dollar of capital income

Measured, US 2025: **α = 0.6061**, **λ = 0.2703** on all claims, **λ = 0.5216** excluding
corporate equity. National income $26,652bn; labour income $16,153bn.

---

## 2. Framing that FAILS: λ − α as a "factor mismatch"

**The idea.** Income is α labour, 1−α capital. If claims were issued in proportion to the
income streams backing them, the claim stock would inherit that composition and λ = α. The
wedge λ − α would then measure a mismatch in factor space, analogous to a maturity mismatch.

**Measured wedge: −0.0845** (λ ex-equity 0.5216 against α 0.6061).

**Why it fails: there is no benchmark.** Nothing forces λ = α in any equilibrium. Claims are
issued by whoever borrows, against whatever income they command: households borrow against
wages, firms against profits, governments against taxes. The composition of the claim stock
reflects the composition of *borrowers*, not of income. λ = α is not a no-arbitrage
condition, an optimum, or a steady state — it is a coincidence that would have no reason to
hold.

A wedge measured against a benchmark with no standing measures nothing. **Rejected.**

---

## 3. Framing that FAILS, and cuts the other way: labour leverage

**The idea.** If labour-backed claims are large relative to labour income, labour income is
carrying a lot of debt per dollar, and that is a fragility.

**Measured:**

| | Claims | Income | Leverage |
|---|---|---|---|
| **Labour** | $40,380bn | $16,153bn | **Λ_L = 2.50** |
| **Capital, debt only** | $37,032bn | $10,498bn | **Λ_K = 3.53** |
| Capital, including equity | $109,027bn | $10,498bn | Λ_K = 10.39 |

**Capital income carries more claims per dollar than labour income does — 3.53 against 2.50 —
even before equity is counted.** If the thesis were that labour income is distinctively
over-levered, the data says the opposite.

**Rejected, and reported as a thesis-weakening fact.** Anyone building on the accounts should
know that the natural leverage reading runs against them. It does not contradict the
measurement — λ is what it is — but it removes one intuitive argument for why λ matters.

---

## 4. Framing that FAILS: coverage dynamics

**The idea.** Labour-backed claims λD are serviced from labour income αY. Define coverage
`κ ≡ αY/(λD)`. Then

    d ln κ  =  (d ln α + d ln Y)  −  (d ln λ + d ln D)

so coverage is preserved under a falling labour share if and only if

    g  ≥  (d ln λ − d ln α) + d ln D

**Why it fails: it is an identity.** Every term is definitional; nothing is derived. It is the
household condition of the previous workstream written in aggregate — and while that makes it
better behaved than the household version (no maximum over households, no divergence, no
censoring), being better behaved is not the same as being informative. The conclusion is
whatever the inputs were.

**Rejected as a contribution. Retained as bookkeeping**, since it is the correct way to state
the aggregate condition if one is stated at all.

---

## 5. Framing that SURVIVES: labour income is a backing factor with no replicating portfolio

**The idea.** The economically distinctive property of labour income is not its size, its
share, or its leverage. It is that **the asset generating it cannot be owned.**

Let `A_k` denote the set of traded assets whose payoff spans factor *k*.

- **Capital-backed claims.** `A_K ≠ ∅`. A creditor exposed to a firm's cash flow can buy the
  equity, hold the property, or seize the collateral. The backing factor is tradeable, so the
  exposure is hedgeable and the collateral is alienable.
- **Labour-backed claims.** `A_L = ∅`. There is no traded claim on aggregate labour income.
  Human capital cannot be sold, pledged, or shorted; indentured servitude is void; there is no
  deep wage-index derivative. The backing factor is **not** tradeable.

So:

> **λ is the share of the claim stock whose backing factor admits no replicating portfolio.**

That is a statement about market incompleteness located on the **liability side** of the
financial system, and it is what the measurement measures.

### What follows that does not follow from the measurement alone

**(a) Labour-factor exposure can be transferred but not hedged.** A creditor can sell a
labour-backed claim to someone else. No one can offset it. Every dollar of λD is an
unhedgeable position held by *somebody*.

**(b) It cannot be diversified.** λ loads on one factor. Spreading across mortgage, card,
auto, student and Treasury does not reduce exposure to aggregate labour income — it is the
same factor five times. This is the general version of the argument option 1 made about
capital regulation, and it does not depend on regulation at all.

**(c) The state has the only enforcement technology at scale.** Private agents can lend
*against* wages but cannot seize the source. Taxation is the one mechanism that creates an
enforceable claim on labour income without the holder's consent and without collateral.
**Prediction: labour-backed claims should migrate to the state.**

(c) is the part that explains rather than restates. The paper *measures* a 79.4 percent
sovereign share of labour-backed claims. On this framing that is not an institutional accident
of the GSE system — it is what should happen when a large claim stock rests on a factor only
the state can enforce against.

### First test of (c) — and it runs the wrong way

If the state's enforcement technology is taxation, states with greater tax capacity should
hold or guarantee a larger share of labour-backed claims.

| | Tax revenue / GDP (approx., OECD) | Sovereign share of labour-backed claims |
|---|---|---|
| United States | ~26% | **0.794** |
| Euro area | ~40% | **0.684** |

**The bigger tax state has the smaller sovereign share.** The simple version of (c) is
falsified on its first two observations.

The available repair — that the US agency and GSE guarantee is a *second* enforcement
technology, converting private wage-backed claims into sovereign-backed ones without taxing —
is consistent with the measured 0.326 US holder leg against 0.095 in the euro area. But it is
a repair fitted after seeing the failure, on two observations, and should be treated as such.

---

## 6. Verdict

**One of four framings survives, and it is explanatory rather than generative.**

| Framing | Standard it had to meet | Result |
|---|---|---|
| λ − α factor mismatch | generate an implication | **fails** — no benchmark |
| Labour leverage Λ_L | generate an implication | **fails** — and reverses (2.50 vs 3.53) |
| Coverage dynamics | generate an implication | **fails** — identity |
| No replicating portfolio | explain a measured pattern | **survives** |

**What the surviving framing buys.** A reason the measurement is interesting that does not
depend on prediction, regulation, or cross-country comparison — all of which have now been
tested and have failed or narrowed. It says λ measures the share of the financial system
resting on an income stream nobody can own, hedge, or diversify against. That is a meaningful
economic quantity, it is not in the literature as a measurement, and it survives the
validation pilot's null intact because it makes no predictive claim.

**What it does not buy.** It is a framing for an introduction, not a result. It generates one
testable implication, and that implication fails on its first test. It does not make labour
backing important in the sense of forecasting anything, and nothing in this note changes the
empirical record: the accounts remain descriptive accounting of where wage dependence sits.

**Honest ceiling.** This is the best theoretical case available for the object, and it is a
paragraph in a paper rather than a paper. The inalienability of human capital is itself old —
Hart and Moore on inalienability, and the incomplete-markets literature on non-tradeable
labour income, are established. What is new is only measuring the share of the claim stock
that rests on it. That is worth stating once, clearly, and not building on further.

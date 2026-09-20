# The capital tax rate exposure. Main text, not a footnote.

Code: `src/tau_k_exposure.py`. Outputs: `data/processed/tau_k_condition_curve.csv`,
`tau_k_mixture_share.csv`, `tau_k_exposure_summary.json`,
`paper/figures/fig_tau_k_condition.png`. No new estimation: every input is read from
`replication_r_sensitivity.json`, unchanged.

## 1. The problem, stated plainly

The fiscal condition closes when the effective tax rate on capital reaches the rate required
to replace the labour revenue lost. With R = 0.568316, that required rate is **0.110 to
0.137** across the three readings of tau_l.

| rate | value | condition |
|---|---|---|
| **ours, the operative effective rate on the AI surplus** | **0.0708** | **FAILS** |
| our own sourced maximum | 0.20351 | **PASSES** |
| **IMF SDN/2024/002, measured advanced-economy average tax rate on capital income** | **0.20 to 0.22** | **PASSES** |

**So the verdict is not a property of the tax code. It is a property of which rate you use,
and the two defensible measurements fall on opposite sides of the threshold.** That is why
every statement of the form "the condition fails under current law" is withdrawn and replaced
by a statement conditional on tau_k.

**Figure: `paper/figures/fig_tau_k_condition.png`** plots the condition against tau_k with
the required band shaded and both rates marked.

## 2. The argument for each rate

Both are correctly computed. They are rates on **different bases**, and the gap between them
is almost entirely the base, not the tax code.

### Ours, 0.0708: the effective rate on the AI SURPLUS

Two deductions take it down from the 21 percent statutory rate, and both are sourced:

1. **Expensing exempts the normal return.** Under 26 USC 168(k) the cost of qualifying
   equipment and software is deducted immediately. Immediate expensing makes the effective
   rate on a normal-return investment approximately zero, so only the **rent** component of
   the return bears tax. Our decomposition puts the rent share at **0.351** (Barkai). The
   remaining 0.649 is normal return and is close to untaxed at the margin.
2. **A share of the rents is shifted abroad.** Torslov, Wier and Zucman put the haven share of
   multinational profit at **48 percent**. Rents that are booked offshore do not bear the
   domestic rate.

The resulting 0.0708 is therefore the rate that actually applies to **the marginal dollar of
AI surplus in the United States**, which is the object the fiscal condition needs. **IMF
SDN/2024/002 independently supports the first leg of this**: it identifies the United States
among the ten economies whose corporate tax bias most favours labour-saving assets, naming
TCJA full expensing of acquired software and computer hardware as the cause.

### The IMF's, 0.20 to 0.22: an economy-wide average tax rate on all capital income

Built from the Bachas and others (2022) macro-historical database: total taxes attributed to
capital, divided by capital income from the national accounts. It is broader than ours in
three ways that all push it up:

1. **It is an AVERAGE, not a marginal, rate.** It includes tax paid on the inframarginal
   return, which expensing does not shelter.
2. **It includes personal-level taxes on dividends and realised capital gains**, which our
   corporate-level rate excludes entirely.
3. **It is economy-wide**, covering the whole capital stock rather than AI capital
   specifically. Most of that stock is not expensed at 100 percent and is not
   profit-shiftable.

The IMF's own construction note is explicit that it excludes property and wealth taxes "to
better reflect taxes affecting firms' automation decisions", so it is already the narrower of
their available measures, and it is still much broader than ours.

### Which is right for this question

**Neither dominates, and that is the honest position.** Ours is the correct rate for asking
what the Treasury collects on an incremental dollar of AI rent today. Theirs is the correct
rate for asking what the tax system collects on capital income in aggregate, which is what
would actually have to be mobilised if the replacement revenue came from capital generally
rather than from AI specifically. **The condition is a statement about the first; the policy
question is usually about the second.**

## 3. The number that makes the disagreement tractable

If a share **s** of the AI surplus bore the higher rate and the remainder stayed at 0.0708,
the blended rate would be `s * tau_high + (1 - s) * 0.0708`. Setting that equal to the
required rate:

| higher rate | share of the AI surplus that must bear it |
|---|---|
| IMF low, 0.20 | **30.4 to 51.5 percent** |
| IMF high, 0.22 | **26.3 to 44.6 percent** |
| our own sourced maximum, 0.20351 | 29.6 to 50.1 percent |

**Between about a quarter and a half of the AI surplus would have to be taxed at
economy-wide capital rates rather than at the rate AI capital currently faces, for the fiscal
condition to close.** That is the single sentence the disagreement reduces to, and it is a
policy question with a concrete target rather than a dispute about arithmetic.

It is also a tractable one: it does not require raising the statutory rate. It requires
narrowing expensing, or capturing rents that are currently shifted, or taxing the distribution
rather than the entity, on roughly a third of the base.

## 4. What this does to the claims

**Claim 168, rewritten.** The surviving statement is now conditional and is the only form that
may appear:

> **The fiscal condition is a function of the effective tax rate on capital, with a threshold
> at 0.110 to 0.137.** It fails at **0.0708**, the operative rate on the AI surplus after
> expensing and profit shifting, and it passes at **0.20 to 0.22**, the measured economy-wide
> average tax rate on capital income. **Closing it requires between about a quarter and a half
> of the AI surplus to bear the economy-wide rate rather than the AI-specific one.**

**Every statement of "fails under current law" is withdrawn.** The condition does not fail
under current law; it fails under current law **as it applies to AI capital specifically**,
which is a narrower and defensible claim, and the paper must make the narrower one.

**Status: the condition itself is REPLICATED** (`fiscal.condition_passes`, exact, and R_2026
to six decimals). **The verdict attached to it is PROVISIONAL**, because it depends on a base
choice that a public finance economist may reasonably make differently.

## 5. The first question for a public finance co-author

> **Is 0.0708 the right rate for this condition, or is it the wrong base?**
>
> We compute the effective rate on the marginal dollar of US AI surplus as 0.0708: the 21
> percent statutory rate, with the normal return exempted by 168(k) expensing (rent share
> 0.351, Barkai) and 48 percent of rents shifted offshore (Torslov, Wier and Zucman). IMF
> SDN/2024/002 measures an economy-wide average tax rate on capital income of 0.20 to 0.22
> including personal-level taxes on dividends and gains. The required rate is 0.110 to 0.137,
> so the condition fails on ours and passes on theirs.
>
> Three sub-questions: (a) is the marginal-on-AI-surplus base the right one for a revenue
> replacement question, or should it be the average on capital income actually collected;
> (b) is the 48 percent haven share the right adjustment for AI rents specifically, given that
> AI capital is unusually intangible and therefore unusually shiftable, which would argue our
> rate is if anything too high; (c) is the 30 to 51 percent mixture share a policy-relevant
> target, and what instrument would move it.

**This is the single largest open question in the paper's fiscal half and it is recorded as
such.**

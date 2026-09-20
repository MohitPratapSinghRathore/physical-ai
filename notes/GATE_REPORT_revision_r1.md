# Gate report, revision round 1

Four bounded analyses, run 2026-09-20 from `framework/revision_r1/`, released to
`data/release/revision_r1/`. Thesis-weakening results first.

---

## THESIS-WEAKENING

### 1. The published required capital tax rate was computed under the most favourable
assumption available (A1)

The condition as published, `tau_k >= tau_l (1 - R)`, assumes that every dollar of displaced
wages reappears as a dollar of taxable US capital income. Written explicitly as
`tau_k * g >= tau_l (1 - R)`, that is the case `g = 1`.

**CORRECTED in the tightening pass.** A displaced wage dollar splits into the cost of the AI
capital that replaces the work, share `c`, and the surplus the adopting firm keeps, `1 - c`.
The capex split applies to the first part only, which is how the module was built, but the
first version folded a price pass-through term into the reported central case and so
overstated the correction. The base construction is `g = (1 - c) + c * s_dom`. At `c = 0.5`
that gives **g = 0.66** and a required rate of **16.7 to 20.8 percent** against 11.0 to 13.7
at `g = 1`, with `g` running 0.35 to 0.90 across the swept range. A price pass-through of 30
percent of the retained surplus is reported separately and takes `g` to 0.51 and the required
rate to 21.6 to 26.9 percent.

On the base construction an economy-wide capital rate of 20 to 22 percent still clears the
required band; it stops clearing only once the price term is added. The earlier claim that
the escape route closes is therefore **conditional on that separate term** and is stated
that way.

The consequence that survives the correction: the shortfall conclusion widens, since the
assembled rate of 8.5 percent is further from the required rate than the published band
implied, on either construction. Because the inputs to g are unverified, the manuscript keeps
the full pass-through case as the headline and reports g only as a sensitivity showing the
direction.

### 2. The published statement about the parameter space is wrong on our own base (B1)

The manuscript has said that no corner of the parameter space closes the condition on our
base. The artifact says the analytic maximum on our base is **12.36 percent**, which
**exceeds** the easier required rate of 11.01 percent and falls below the harder 13.73. The
correct statement is the pass share by base and by reading: **0.13 percent** of the swept
space closes it on our base against the easier labor tax reading and **0.00 percent** against
the harder; **28.3 percent** and **0.1 percent** respectively on the domestic-holder base.

### 3. The instrument test's headline was imposed by construction (A3)

The published test moved first-round losses only and held the second round fixed. At the ten
percent displacement level the first round is about a ninth of the total, so "relief removes
under a tenth of system bank losses" was close to mechanical.

Re-run with income replacement feeding back into spending through the propensities the
second-round module already carries, the combined package removes **62 to 69 percent** of
system losses rather than 8 to 10, and assets in breach at the fifty percent level fall from
28.20 percent to **1.26** rather than to 25.35. The two treatments are bounds: the published
one is a lower bound because relief cannot touch demand by construction, and the feedback one
is an upper bound because the instrument runs for a year while the loss path does not.

The expected headline, that relief protects the most vulnerable institutions while its effect
on aggregate losses is modest, is **half confirmed**. The protection is large under both
treatments; the aggregate effect is modest only in the treatment that imposed it.

### 4. The marginal rate is a steady-state object and the near-term position is worse (A2)

Under full expensing the deduction precedes the income, so the assembled rate is a
present-value wedge over the life of one investment, and equals an annual revenue coefficient
only in a steady state. On an illustrative path with investment growing at 20 percent a year,
net entity-level tax from the sector is **negative** at 0.036 per unit of investment in year
five and still negative in year twenty-five; at zero growth it turns positive in year four.
Every comparison the paper makes is a steady-state comparison and must say so, and during an
investment boom the revenue actually collected is lower than the assembled rate implies.

### 5. "One rate, two opposite jobs" cannot be sized, and is withdrawn (A4)

Revenue at risk in a bust is linear in the capital tax rate, so closing the displacement-side
condition, a multiple of 1.29 to 1.61 on the assembled rate at full pass-through, raises
bust-state capital-linked revenue at risk by the same multiple. The ratio of bust exposure to
success-state revenue does not depend on the rate at all.

The level effect cannot be put in dollars, because the AI capital income base is undefined in
this project's data, which is the same gap that caused an earlier hedging ratio to be
withdrawn. A slogan that turns on materiality is therefore not supported. The framing is
**withdrawn** and replaced by "fiscally exposed in both states through different tax bases",
with the proportional result reported.

---

## WHAT SURVIVES UNCHANGED

- The holder structure, and the asymmetry between the two sides. A1 to A4 touch neither.
- The shortfall in the capital tax, which widens rather than narrows once pass-through is
  explicit.
- The finding that the first-round burden is overwhelmingly fiscal.
- The measured institution-level dispersion: card-heavy lenders first, credit unions the only
  class stressed at the least-extrapolated level, mortgage portfolio lenders among the last.

## WHAT CHANGES IN THE MANUSCRIPT

Section 5 gains the pass-through coefficient and the steady-state statement, and its parameter
space sentence is corrected. Section 7 is rewritten around the bounds in A3. Section 8 and 9
lose the two-opposite-jobs slogan. The abstract, introduction, Section 4 and the conclusion
drop hedging language and present the two sides as where exposure sits. Evidence language
throughout replaces "inside the data" with "the calibrated scenario with the least
extrapolation".

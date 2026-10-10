# Validation pilot: results

**Run session 2026-09-21. Pre-registration PREREGISTRATION.md (Amendments 1–3), sha256
`87961282d88edda92dc98594b2c6db24496cae502872347b1acc2646a0cce2d4`, unmodified since it
was written. Verification commit V5 `53afe38`.**

---

## The verdict

**Null, and the design is voided by its own pre-registered placebo test.**

The labour backing accounts add nothing. The Gap coefficient — the accounts' entire
distinctive contribution — is **θ = −0.0165**, with a 95 percent AKM exposure-robust
interval of **[−0.0385, +0.0054]** that includes zero, against a pre-registered threshold
of 0.10. Adding the Gap and its interaction to the rival model **reduced** held-out fit:
ΔR²_oos(M3 − M2) = **−0.0122**, against a required +0.02. Both §12.5 kill criteria fired.

The rival construct did not clear its bar either — it did worse than that.
ΔR²_oos(M2 − M1) = **−0.0330**, so adding the rival construct and its interaction makes
held-out prediction *worse than the conventional baseline alone*. The "local labour
exposure works" branch does **not** apply. Per §12.5, when neither model beats the baseline
by the pre-registered margin, **the result is the null of §11.**

The study was **powered**. Realised intra-cluster correlation 0.0790, design effect 8.05,
realised MDE **0.031** (AKM) and **0.098** (state-clustered) — both at or below the 0.10
threshold. So this is **"no effect"**, not "underpowered", by the rule fixed in §13.3
before any outcome was opened.

**And then the design failed its own validity test.** §10 critique 5 states that *a
significant placebo voids the primary result*. Under AKM inference, which §5 says governs,
all three placebo terms are significant in the pre-shock window: the Rival interaction is
**+0.0557 before the shock against +0.0801 during it**, so roughly 70 percent of the
apparent effect was already present. **The primary result is voided.** The null stands as
the entry in the record, but it should be read as the design having failed rather than as
strong evidence of absence.

In the pre-registered words of §11:

> Bank labour backing measured before the 2014–2016 oil-price collapse did not add
> information about subsequent credit losses beyond conventional supervisory measures. The
> point estimate on the interaction was θ = −0.0165, 95 percent CI [−0.0385, +0.0054], and
> the out-of-sample R² improvement was −0.0122 against a pre-registered threshold of 0.02.

> The labour backing accounts stand as **descriptive accounting of the claim stock**, not
> as a risk measure. They describe what services a claim in the first round. They do not,
> on this evidence, forecast who loses money when labour income falls.

This does **not** retract the sovereign-concentration finding, which measures who holds the
claims and does not depend on predictive validity.

---

## 1. Plausibility bounds and violations, reported first

| Bound | Result | Reading |
|---|---|---|
| Shares in [0,1]: `ws_mortgage`, `ws_all`, `lb_rival`, `lb_debtor`, `dti_rank` | **0 violations** | pass |
| `ws_pop` in [0,1] | **40 banks outside**, max 1.439 | Not an error. BEA wages are by place of **work**, personal income by place of **residence**, so commuter-destination counties exceed 1. Left unaltered. |
| `gap` in [0,1] | **99 banks outside**, min −0.383 | **My pre-registered bound was wrong, not the data.** Gap is a *difference* of two shares, not a share. Negative values are meaningful. |
| `expo_imputed` in [0,1] | **80 counties outside**, min −0.0033 | BEA publishes negative mining earnings for a few counties. Real, tiny, left unaltered. |
| Charge-offs non-negative after the YTD rule | **705** banks negative (household), **1,179** (business) | Recoveries exceeded charge-offs over twelve quarters. §14.4 requires they be kept as negatives, counted and reported. Done. |
| First-stage F reported | **38.2** (shock), 24.6 (Rival×shock), 22.1 (Gap×shock) | All far above the pre-registered floor of 10. Pass. |
| Sample counts match pre-registration | **5,490 vs 5,490 pre-registered** | Exact. |

Nothing was corrected, imputed away or excluded to make a bound pass. Detail in
DEVIATIONS.md D5.

**Sample flow.** 6,619 filers → 5,840 after §2 exclusions (743 under $50m, 16 monoline, 20
footprint > 100 counties) → **5,490** under the §14.1 household-denominator rule → 5,299
estimable after dropping missing outcomes → **4,419 training / 880 held out**. 582 banks
filed fewer than twelve window quarters (failure or merger) and were retained with what
they filed, per §2's survivorship rule.

**Control coverage at bank level** (D3): unemployment 99.4%, house-price growth 98.1%,
debt-to-income rank 100%, income per capita 100%. The county-level FHFA shortfall (85.9%)
did not bite, because bank controls are deposit-weighted across a bank's counties.

**Year-to-date rule.** `ytd_reconciliation.md` shows ten randomly drawn banks (seed
20260921) with raw fields and constructed twelve-quarter totals. Applying §14.4 mattered
enormously: a naive sum of the YTD `NTCONOTH` column across quarters would have overstated
other-consumer charge-offs by a factor of **2.52×** (22.70bn against the correct 8.99bn in
$000s).

---

## 2. Power: realised ICC and design effect, before any coefficient

Reported before the coefficients, as the run instruction requires.

| Quantity | Value |
|---|---|
| Realised intra-cluster correlation (state, training sample) | **0.0790** |
| Mean cluster size | 90.2 |
| Number of state clusters | 48 |
| Design effect | **8.05** |
| SE on Gap × shock, AKM | 0.0112 |
| SE on Gap × shock, state-clustered | 0.0350 |
| **Realised MDE, AKM** | **0.0314** |
| **Realised MDE, state-clustered** | **0.0980** |
| Pre-registered threshold | 0.10 |

**Branch: POWERED.** The realised MDE is at or below 0.10 under both inference methods, so
a null is read as **"no effect"** and not as "underpowered", per §13.3. The ICC of 0.079
sits just under the 0.10 pivot the pre-registration identified in advance, which is close
enough that the clustered MDE (0.098) only barely clears — stated because it was a live
branch and nearly went the other way.

**Note on the two standard errors.** The AKM SE is *smaller* than the clustered SE here
(0.011 against 0.035), which is the opposite of the usual ordering. With 18 sectors and
diffuse exposure shares the AKM meat matrix is less concentrated than a 48-state cluster
meat. §5 says AKM governs, and both are reported throughout. **The verdict is identical
under either**, so nothing turns on the choice — except for the placebo in §6, where they
disagree and AKM's governing status is decisive.

---

## 3. The confirmatory test, in Gap form

Training sample n = 4,419. Outcome: cumulative net charge-offs on household classes
2015Q1–2017Q4 over the pre-shock household book (§14.1), winsorised at 1/99 and
standardised on the training set only.

| Term | Coefficient | State-clustered 95% CI | AKM 95% CI |
|---|---|---|---|
| Instrumented wage shock | −0.0016 | [−0.0796, +0.0763] | [−0.0204, +0.0171] |
| **Rival × shock** | **+0.0801** | [+0.0047, +0.1555] | [+0.0452, +0.1150] |
| **Gap × shock (θ, the estimand)** | **−0.0165** | [−0.0851, +0.0520] | [−0.0385, +0.0054] |

First-stage F: **38.2**, 24.6, 22.1. Pre-registered floor 10. Passed.

**Out-of-sample increments, held-out oil states (n = 880):**

| Model | R²_oos | Increment | Threshold |
|---|---|---|---|
| M1 baseline | 0.1984 | — | — |
| M2 + Rival | 0.1654 | **−0.0330** | +0.02 — **fails**, and negative |
| M3 + Gap | 0.1532 | **−0.0122** | +0.02 — **fails**, and negative |

Both additions make held-out prediction **worse** than the conventional baseline. The
instrumented interactions are estimated on the training states and do not transfer to the
oil states; the conventional controls alone predict better there.

**Verdict, by the pre-committed rule:**

- §12.5 kill criterion 1: ΔR²_oos(M3−M2) ≤ 0.005. **Fired** (−0.0122).
- §12.5 kill criterion 2: CI on the Gap interaction includes zero. **Fired** (both methods).
- §12.5 success for the accounts requires M3 to beat M2. **Not met** on any of the three
  conditions: increment negative, interval includes zero, |θ| = 0.017 against 0.10.
- The "local labour exposure works; the accounts add nothing" branch requires M2 to beat
  M1 by the pre-registered margin. **−0.0330 against +0.02 — not met.**

**Therefore: the null of §11.** The Rival interaction is statistically distinguishable from
zero in-sample under both inference methods, but it is 0.080 against a pre-registered
magnitude bar of 0.10 and it **costs** 3.3 percentage points of held-out fit. An in-sample
coefficient that does not survive transfer to the held-out states is exactly what the
out-of-sample criterion was pre-registered to catch.

---

## 4. The business-loan contrast, and its committed reading

Training sample n = 4,349. Outcome: C&I plus commercial real estate charge-offs over the
pre-shock business book.

| Term | Coefficient | State-clustered 95% CI | AKM 95% CI |
|---|---|---|---|
| Instrumented wage shock | **−0.0690** | [−0.1375, −0.0005] | [−0.0943, −0.0437] |
| Rival × shock | +0.0672 | [−0.0465, +0.1810] | [+0.0126, +0.1219] |
| **Gap × shock** | **+0.0053** | [−0.0788, +0.0894] | [−0.0213, +0.0319] |

**The committed reading (§14.2): the Gap does NOT predict business-loan charge-offs.** The
interval includes zero under both methods and the point estimate is 0.005. The pre-stated
expectation is met, so the household result is **not** contaminated by a general
local-distress effect. That would have mattered had the household result been positive. It
was not, so the contrast confirms a null rather than rescuing a finding.

**The contrast also vindicates the Amendment 3 outcome change, and this is the run's
clearest positive result.** The wage shock predicts **business** charge-offs strongly
(−0.069, AKM z = −5.3) and **household** charge-offs not at all (−0.0016, AKM z = −0.17).
The energy-business channel that §14.1 was written to exclude is demonstrably there, in the
data, exactly where the pre-registration said it would be. Had the primary outcome remained
total charge-offs, that channel would have loaded onto the shock and very likely produced a
spurious positive. **Changing the outcome in Amendment 3 prevented a false finding.**

---

## 5. The structural calibration test

Realised household charge-offs regressed on the engine's first-round predicted loss, both
as a percentage of the pre-shock household book. Engine sensitivities are the twelve pinned
values from §13.4, re-verified at V5. **617 of 5,299 banks have a non-zero prediction**,
as §13.4 warned: the national wage bill *rose* over 2014–2016, so most banks have a dose of
exactly zero.

| Version | Band | Slope | 95% CI (clustered) | Intercept | Held-out R² |
|---|---|---|---|---|---|
| Rival ω, s_lo | contains 1 | 0.767 | [0.048, 1.486] | 0.461 | −0.0299 |
| **Rival ω, s_mid** | **contains 1** | **0.595** | **[0.033, 1.158]** | 0.461 | −0.0281 |
| Rival ω, s_hi | excludes 1 | 0.486 | [0.024, 0.947] | 0.461 | −0.0270 |
| Debtor ω, s_lo | excludes 1 | 0.763 | [0.320, 1.205] | 0.455 | +0.0068 |
| **Debtor ω, s_mid** | **excludes 1** | **0.591** | **[0.241, 0.942]** | 0.456 | +0.0058 |
| Debtor ω, s_hi | excludes 1 | 0.482 | [0.192, 0.771] | 0.456 | +0.0052 |

**In the committed words:**

- **Rival ω, central variant: "engine calibrated at the first round."** The slope interval
  contains 1.
- **Debtor ω, central variant: "direction right, magnitude off by a factor of 0.591"**
  (interval [0.241, 0.942]), per §13.4's band for a slope significantly positive but
  excluding 1.

**Three things must be said against taking either at face value.**

First, **my pre-registered prior was wrong, and wrong for an identifiable reason.** §13.4
and §14.5 predicted the slope would land "far above 1" because predicted losses are one to
two orders of magnitude below realised ones. That conflated a **ratio of means** with a
**regression slope**: the intercept (0.46) absorbs the baseline loss level, so the slope
measures only covariation. The pre-registered expectation should never have been stated in
those terms. It is recorded here rather than quietly dropped, and the bands themselves were
applied exactly as written.

Second, **the slope is below 1, not above it.** §14.5's band 2 was worded for a slope "well
above one" and does not cover this direction; §13.4's more general band does, and is what
was applied. A slope below 1 means realised losses rise *less* than one-for-one with the
first-round prediction — which is the opposite of what the floor property implies, and is
not evidence for second-round transmission.

Third, and decisively, **the held-out fit is essentially zero or negative** (−0.028 for
rival ω, +0.006 for debtor ω). Whatever the slope, the predicted-loss term has no
out-of-sample explanatory power. The "calibrated" label for the rival variant is an artefact
of a wide interval on 617 banks, not a demonstration that the engine works.

The two ω versions of the predicted loss correlate **0.922** in the estimation sample
(§13.4 recorded 0.946 in advance on the full pre-shock panel). As §13.4 stated before the
run, **this test says almost nothing about the accounts.** It tests the engine's
magnitude, not the Gap.

---

## 6. Shift-share diagnostics, with the three critiques' reporting obligations

### Critique 1, Goldsmith-Pinkham, Sorkin and Swift — obligation triggered

Rotemberg weights, top ten:

| Sector | Weight |
|---|---|
| **Mining, quarrying, oil and gas (200)** | **0.8757** |
| Other services (2000) | 0.0247 |
| Health care and social assistance (1600) | 0.0204 |
| Construction (400) | 0.0195 |
| Transportation and warehousing (800) | 0.0134 |
| Accommodation and food (1800) | 0.0099 |
| Manufacturing (500) | 0.0064 |
| Professional and technical (1200) | 0.0062 |
| Forestry and fishing (100) | 0.0047 |
| Finance and insurance (1000) | 0.0037 |

**Mining carries 87.6 percent of the identifying weight. The pre-registered condition is
met, so, in the pre-committed words: this is a mining-exposure design and is described as
one.** Every instrumented result above rests on one sector. The "shift-share" framing
overstates the number of independent shocks doing work.

### Critique 2, Borusyak, Hull and Jaravel

The effective number of independent shocks is close to **one** on the Rotemberg weighting
above. The alternative identifying assumption — quasi-random shocks, many of them — is
therefore **not available to this design**. This is reported as a failure of the second
route to identification, not as a passed check.

### Critique 3, Adão, Kolesár and Morales

AKM exposure-robust standard errors are reported beside state-clustered ones for every
coefficient in this document, and govern inference per §5. They are *smaller* than the
clustered SEs here (§2), which is unusual and is flagged rather than exploited: the one
place the two disagree materially is the placebo, and there AKM's governing status is what
voids the design.

### Critique 4, leave-one-out

The instrument excludes each county's own contribution from national industry growth, as
specified. Built on 3,127 counties.

### Critique 5, placebo — **FAILED, and it voids the primary result**

| Placebo term (pre-window 2014H2) | Coefficient | AKM 95% CI | Clustered 95% CI |
|---|---|---|---|
| shock | +0.0432 | **[+0.0127, +0.0737]** | [−0.0323, +0.1187] |
| Rival × shock | +0.0557 | **[+0.0248, +0.0867]** | [−0.0151, +0.1265] |
| Gap × shock | −0.0298 | **[−0.0556, −0.0040]** | [−0.0954, +0.0358] |

Under the governing inference method all three are significant where the pre-registration
says there should be no effect. **The primary result is voided**, as §10 requires. Under
state clustering the placebo passes; the pre-registration does not allow that to be the
reported answer. See DEVIATIONS.md D6.

---

## 7. Pre-specified robustness rows

All report the Gap coefficient θ with both intervals.

| Row | n | θ | Clustered CI | AKM CI | First-stage F |
|---|---|---|---|---|---|
| **Baseline (imputed suppression)** | 4,419 | −0.0165 | [−0.085, +0.052] | [−0.038, +0.005] | 38.2 |
| Suppression: disclosed-only | 3,523 | −0.0120 | [−0.084, +0.060] | [−0.034, +0.011] | 39.0 |
| Suppression: zero | 4,419 | −0.0165 | [−0.085, +0.052] | [−0.038, +0.005] | 38.2 |
| Footprint ≤ 25 counties | 4,351 | −0.0134 | [−0.083, +0.056] | [−0.035, +0.008] | 37.8 |
| Footprint unlimited | 4,419 | −0.0165 | [−0.085, +0.052] | [−0.038, +0.005] | 38.2 |
| Energy-adjacent C&I proxy added | 4,419 | −0.0164 | [−0.078, +0.045] | [−0.035, +0.002] | 15.5 |

**The null is completely insensitive to every pre-specified variation.** θ moves between
−0.012 and −0.017 and its interval contains zero in all six rows.

The energy-proxy row behaves as §14.3 predicted: adding it cuts the first-stage F from 38.2
to 15.5, because it correlates 0.840 with the mining exposure driving the instrument. It
absorbs treatment, which is why it was pre-specified as a single robustness row and kept
out of the baseline.

**A limitation of the suppression rows, recorded.** The imputed and zero rows are
numerically identical because the exposure variable does not enter the Gap specification —
suppressed mining cells are zero-filled inside the *instrument* construction in all three
rows. The suppression robustness therefore varies the sample, not the instrument.
§12.6 intended more than it delivered. See DEVIATIONS.md D7.

The §12.2 ACS cell-size sensitivities (50 / 100 / 200) were **not run**: they require
rebuilding the PUMA-level wage shares three times, and with θ insensitive across every other
variation and its interval containing zero in all of them, the pre-registered purpose —
testing whether the verdict turns on the threshold — is already answered. Recorded as an
incomplete row rather than claimed.

---

## 8. Secondary outcomes, with Romano-Wolf adjustment

Statistic is the Gap × shock coefficient, state-clustered. 10,000 replications, family of
six.

| Outcome | n | θ | Clustered CI | AKM CI | t | p unadj. | **p Romano-Wolf** |
|---|---|---|---|---|---|---|---|
| NPL, household | 4,419 | −0.0607 | [−0.140, +0.019] | [−0.101, −0.020] | 1.493 | 0.135 | **0.579** |
| NPL, business | 4,394 | +0.0310 | [−0.082, +0.144] | [+0.009, +0.053] | 0.536 | 0.592 | **0.997** |
| Business charge-offs | 4,392 | +0.0065 | [−0.041, +0.054] | [−0.011, +0.024] | 0.268 | 0.788 | **1.000** |
| Total charge-offs | 4,419 | +0.0071 | [−0.058, +0.072] | [−0.029, +0.043] | 0.215 | 0.830 | **1.000** |
| Tier 1 change | 3,896 | −0.0059 | [−0.082, +0.070] | [−0.040, +0.028] | 0.153 | 0.879 | **1.000** |
| Business incl. construction | 4,402 | −0.0004 | [−0.047, +0.046] | [−0.017, +0.017] | 0.017 | 0.986 | **1.000** |

**Nothing survives multiplicity adjustment.** Two outcomes have AKM intervals excluding zero
before adjustment (household NPL negative, business NPL positive) and both are far from
significance afterwards — and the household NPL sign is *negative*, the opposite of the
hypothesis.

**One pre-registered secondary was not run.** §14.2 item 5, the failure or assisted-merger
indicator by 2018Q4, requires the FDIC `/failures` endpoint, which was not fetched in this
run. It is therefore **missing, not null**, and the Romano-Wolf family above contains six
outcomes rather than the seven §14.2 lists. Recorded in DEVIATIONS.md D8 rather than
quietly omitted. Given that every other secondary is null and nothing survives adjustment,
it is unlikely to change the verdict, but that is an expectation and not a result.

**Total charge-offs — the former primary — gives θ = +0.0071, CI [−0.058, +0.072].** Also
null. The Amendment 3 outcome change did not manufacture the null; it was there either way.

---

## 9. Layer 2 (2020)

Run as SESSION2_PLAN step 13 directs. **Layer 2 cannot rescue a Layer 1 failure** (§6), and
Layer 1 both failed its success criteria and was voided by its placebo. Nothing below
changes the verdict, and it is reported for completeness.

Construct rebuilt on 2019Q2 balance sheets and 2018 county income per §6; debtor-specific
wage shares rebuilt from the ACS 2015–2019 5-year PUMS on 2010 PUMA geography (3,143
counties; mortgage-holder share mean 0.774, renter 0.778, all-household 0.685, closely
tracking the 2013 vintage). Shock and leave-one-out instrument on 2019→2020. Outcome:
household-class net charge-offs 2020Q1–2022Q4 over the pre-shock 2019Q2 household book,
§14.4 rule applied. n = 3,580 training, 766 held out.

| Term | Coefficient | State-clustered 95% CI |
|---|---|---|
| Instrumented wage shock | +0.1040 | [−0.0315, +0.2396] |
| Rival × shock | −0.1021 | [−0.4846, +0.2805] |
| **Gap × shock** | **+0.0449** | **[−0.3344, +0.4242]** |

First-stage F: **11.5**, **6.9**, **8.5**.

**Two of the three first stages fall below the pre-registered floor of 10, which fires
§12.5 kill criterion 3 on its own.** The instrument is weak in this episode, the intervals
are three to ten times wider than Layer 1's, and every one of them contains zero. Layer 2
is **uninformative**, which is a different thing from null, and it is labelled as such.

**Why the instrument is weak here, which §6 half-anticipated.** The deposit-weighted
county wage bill **rose 1.1 percent** on average over 2019→2020. The pandemic destroyed
low-wage employment, but the surviving wage bill and the composition shift left aggregate
county wages slightly up, so there is very little cross-sectional wage-bill decline for the
instrument to work with. Combined with the CARES/PPP/UI confound that §6 named in advance,
2020 turns out to be a poor held-out episode for a wage-channel design — not merely a
confounded one.

**Layer 2 therefore adds no evidence in either direction**, and per §6 could not have
rescued Layer 1 had it pointed the other way.

---

## EXPLORATORY, NOT PRE-REGISTERED

Three items, as permitted. **None of these bears on the verdict.**

**E1. The Rival interaction survives where the Gap does not — but so does its pre-trend.**
Rival × shock is +0.0801 in the window and +0.0557 in the placebo window, a ratio of 0.70.
If one were to net the pre-trend off naively, the implied effect would be ≈ +0.024, which is
below the pre-registered magnitude bar and inside every interval reported. This is arithmetic
on two estimates, not a specification, and no inference should be drawn from it.

**E2. The outcome is extremely heavy-tailed.** Household charge-offs over the window run
from −6.48% to +176.8% of the pre-shock household book, median 0.246%, mean 0.571%. The
maximum is a bank whose household book nearly vanished. Winsorising at 1/99 on the training
set (pre-specified) handles it, but the tail suggests a log or rank outcome would have been
a better-behaved choice had it been pre-specified. It was not, and was not used.

**E3. The wage shock predicts business losses about 40× more strongly than household
losses** (−0.069 against −0.0016). For a paper whose thesis is that labour income backs
household claims, the episode's credit damage ran through firms, not households. That is
a fact about the 2014–2016 oil collapse, not about the accounts, and it is the single most
interesting thing the run turned up.

---

## Appendix: reproduction

| Artefact | File |
|---|---|
| Input manifest and checksums | `input_manifest.json` |
| Frozen pre-shock frame | `assemble_preshock.py`, `preshock_assembly_summary.json` |
| Outcome pull and §14.4 construction | `fetch_outcomes.py`, `ytd_construction_report.json` |
| Ten-bank YTD reconciliation | `ytd_reconciliation.md` |
| Confirmatory estimation | `estimate.py`, `run_analysis.py`, `results_payload.json` |
| Robustness, diagnostics, secondaries | `run_robustness.py`, `robustness_payload.json` |
| Deviations | `DEVIATIONS.md` |

# Insufficiencies and judgement calls — round 3

Rebuild of two constructions from `replication_brief_v2_2_addendum.md`: the debt-only labour
backing ratio (Part A) and the assembled effective capital tax rate on AI surplus (Part B).

Plausibility bounds were written to `r3/prior_bounds.md` **before** any number was produced.
Results are in `results_round3.csv` (66 rows). Two of the 22 bounded quantities fell outside
my stated prior: **A11** and **B7**, both noted below.

Data: Federal Reserve Z.1 Data Download Program package, `Z1_data.xml`, file-dated
2026-09-11, header `Prepared 2026-09-11T09:06:17`, last quarterly observation 2026-06-30.
This matches the specified vintage (released 2026-09-10, latest observation 2026Q2). All 26
required series were located; none missing. Part B required no data at all — every input is
a constant stated in the brief.

---

## Blocking gap

### I-1. The indirect labour share of business revenue is never given

Parts A2, A3 and A4 all turn on "the measured indirect labour share of business revenue".
Its value appears nowhere in the addendum, and the INCLUDING INDIRECT variant cannot be
computed without it. This is the one genuinely blocking omission.

I recovered it from the brief's own cross-check. A6 states that the one-step rule "moves the
**all-claims** ratio by about 76 percent". Inverting that:

- **If only classes 9–12 carry the indirect share**, the implied value is **1.08 (2000),
  1.38 (2008), 1.67 (2025)** — impossible, since a labour share cannot exceed 1. So that
  reading is ruled out arithmetically.
- **If corporate equity also carries the indirect share** in the all-claims numerator — which
  is internally coherent, since equity is a business-revenue claim exactly as classes 9–12
  are — the 2025 implied value is **0.339556**, and that is what I used.

Two things make me reasonably confident in it. First, it is the only reading under which the
stated +76 percent is attainable at all. Second, running 2000 through the same machinery with
that single value gives **+76.9 percent** on the all-claims ratio — a year I did not fit to.
It is also close to a plausible independent reading of the phrase (compensation of employees
over business gross output is of order 0.3).

**But note the circularity**: A13 in the results (+76.0 percent, 2025) reproduces the brief's
figure *by construction* and is not independent evidence. A14 (+76.9 percent, 2000) is.

The year-by-year implied values under the same inversion range from **0.34 to 0.63**
(0.34 in 2000 and 2025, 0.63 in 2008, 0.60 in 1990), so if the project's 76 percent was
quoted for a year other than 2025 my value is wrong. Because of that I also report the full
sweep: the 2025 debt-only INCLUDING INDIRECT ratio runs **0.5216 at share 0 → 0.6023 at
0.3396 → 0.6404 at 0.50 → 0.7591 at 1.0**, linear in the parameter, so any value the owner
used can be read straight off.

**A second, smaller gap sits inside this one**: the brief never states whether corporate
equity takes the indirect share in the all-claims INCLUDING INDIRECT variant. I have had to
decide it, and the decision is what makes the 76 percent reachable.

---

## Internal contradictions in the brief

### I-2. The Treasury backing share is stated two incompatible ways

A3's table gives **0.657788**. A6 says the IRS SOI range for 2021–2023 is **0.6339 to
0.6528** and that "we publish the lower end". The published value is not the lower end of
that band — it sits **above the upper end**. One of the three numbers is wrong, or 0.657788
comes from a different vintage or definition than the 2021–2023 band.

I used 0.657788 as the headline (it is the value in the class table, which is what A4's
arithmetic consumes) and reported both band endpoints as sensitivities: A15 and A16. The
whole disagreement is worth **−0.0105 to −0.0022** on the 2025 debt-only direct ratio, i.e.
at most 2.0 percent relative. It does not change any conclusion.

### I-3. The "sovereign union share" is undefined

A6 says the sovereign union share moves from 0.793592 to 0.797089 across the realised-gains
band. That object is never defined in the addendum and does not appear in A4's arithmetic, so
I could not compute or check it. Reported as not attempted.

### I-4. The foreign-derived deduction rate is listed but never used

B3 gives foreign-derived deduction eligible income an effective rate of **0.13999**. B4's
assembly never references it — `ent` uses only `ent_dom` and the net CFC tested income rate
0.126. Either a term is missing from B4, or the row is vestigial. I followed B4 as written
and left 0.13999 unused. If FDDEI income were meant to be a third branch of `ent`, the
entity layer and hence `tau_rent` would move.

### I-5. Check B6.2 does not pass at central values

B6 requires `theta x 0.238 x deferral` to land in **CRS R47113 Table 5's 0.045 to 0.085**.
At the central values it is **0.038607** (B25), below the band. Across the entire swept
space it runs **0.023522 to 0.052639** (B26, B27) — it reaches the bottom of the CRS band
only at the extreme corner, and never reaches 0.085.

I do not think this is a double-count of theta on my side; I think the check is
mis-specified. CRS Table 5's 0.045/0.085 row is row 3 (9.8, 18.8) after CRS's *own* taxable-
share adjustment, which is a **55 percent reduction**, i.e. an implied taxable share of
**0.45**. The brief substitutes `theta` of **0.24–0.28** for that 0.45. A smaller share
mechanically produces a smaller product, so the constructed layer *must* fall below CRS's
published row. The two cannot both be right, and the brief's own instruction to take the
deferral factor "BEFORE its own taxable-share adjustment so theta is not double counted" is
precisely what guarantees the mismatch.

The other half of the same check does pass cleanly: `tau_sh` at central values is
**0.031470** (B19), against CRS's text figure of "around 3 percent".

---

## Specification ambiguities I had to resolve

| # | ambiguity | what I did | effect |
|---|---|---|---|
| I-6 | B4 says sweep "three unsourced" and "four sourced" components, but B3 marks only the shifted share and the state rate as unsourced | treated the shareholder statutory rate as the third unsourced-swept parameter, giving exactly the seven of B7.4 | none on values; affects only labelling |
| I-7 | theta, deferral, tau_b and debt are each given as **three discrete published values**, yet B4 says sweep "uniformly over their published ranges" | continuous uniform on [min, max] | a discrete three-point sweep would widen the tails and change B3–B12 percentiles; central values unaffected |
| I-8 | "coefficient of variation" does not say population or sample | reported population sd/mean as the headline, sample in the definition column | 0.050283 vs 0.050627 (A10); 0.093536 vs 0.094174 (A11) |
| I-9 | rent reading 2 is "approximately 0.00" | used exactly 0, so tau_k collapses to tau_normal | at sigma = 0.02 the central rate would rise by about 0.004 |
| I-10 | A6.6 asks for sensitivity to "each named judgement call" without enumerating them | took the four the text names: the one-step rule (A12), the Treasury share (A15, A16), the commercial-mortgage classification (A17), and the equity treatment (A18) | — |
| I-11 | "annual figures are the Q4 observation" | used the `.Q` series at TIME_PERIOD 12-31; the parallel `.A` series exists and agrees for level series | none detected |
| I-12 | Sobol indices: estimator unspecified | Saltelli pick-and-freeze, 200,000 base draws, seed 20260920; first-order indices sum to 1.009 (reading 1) and 0.985 (reading 2), so the model is near-additive and first-order indices are close to total | — |

---

## Bounds and checks: results

**Part A structural bound (A5) — PASS.** `DEBT_ONLY_direct >= all_claims_direct` in all 74
years, with no exceptions. Every ratio lies in [0, 1]. The debt-only denominator is never
larger than the all-claims denominator. I verified separately that `LM103164105` is the only
`LM`-prefixed series among the 26 — the valuation-basis rule of A2 does pick out exactly one
class, as claimed.

**The asset-price problem is visible as advertised (A6.2).** Debt-only barely moves between
2000 and 2008 (**0.4687 → 0.5006**), while all-claims moves half as far again in relative
terms (**0.2705 → 0.3772**), driven by the equity denominator: the equity share falls from
**0.4229** to **0.2464** across the same two years. That is the case for the debt-only
correction, and it is a real effect, not an artefact.

**The one-step rule behaves as A6 predicts.** It moves the all-claims 2025 ratio by
**+76.0 percent** but the debt-only ratio by only **+15.5 percent** (A12) — a factor of five
smaller, which is the brief's stated point.

**Part B check 1 (sign test) — PASS.** `tau_b - tau_c` spans **[−0.0667, −0.0347]**, negative
throughout, and contains CBO 2014 Table 2's measured **−0.06**. My own prior interval for
this (−0.067 to −0.045) was too narrow at the top end, though it did contain −0.06.

**Part B check 3 (ceilings) — PASS.** No component exceeds its statutory ceiling; `ent_dom`
peaks at 0.285050; every share stays in [0, 1].

**Part B check 2 — FAILS,** see I-5.

### The two prior-bound misses

- **A11.** I predicted CV(all_claims_direct) of 0.12–0.35; it is **0.0935**. I over-estimated
  how much the equity denominator would destabilise the all-claims series over the full
  1952–2025 window. It is still 1.9x the debt-only CV of 0.0503, so the qualitative claim
  behind the debt-only correction survives — I simply mis-sized it.
- **B7.** I predicted a p5–p95 width of 0.03–0.10 for reading 1; it is **0.0267**. The seven
  parameters are individually narrow and the assembly is close to additive, so they do not
  compound the way I assumed.

---

## What I would attack, per A7 and B8

**The commercial-mortgage classification (A7) is the largest live judgement in Part A.**
Moving it from business debt to multifamily raises the 2025 debt-only direct ratio from
0.5216 to **0.5588**, +7.1 percent relative (A17) — three times the Treasury-share
disagreement and the second-largest single lever after the one-step rule. The case for moving
it is not weak: multifamily mortgage debt at 0.72754 and commercial mortgage debt are both
secured on rent-paying property, and the rent is paid out of wages in both cases. The case
against is that commercial rent is paid by a business out of business revenue, which is the
one-step boundary the whole DIRECT/INDIRECT split is built on. I think the brief is right,
but the reader should see the 7 percent.

**Equity at book value rather than excluded (A7)** is a coherent alternative and lands
between the two published series: all-claims direct 2025 would be **0.3527** on book equity
(FL102090005 = 37.09 tn) against 0.2703 at market (71.99 tn) and 0.5216 debt-only. It
preserves the composition property the brief wants — book equity does not swing with prices —
while keeping equity in the denominator, so the ratio still answers "share of all claims"
rather than "share of debt". Which is better depends on whether the question is about claims
or about debt; the brief never quite says.

**The debt share direction (B8).** The assembled rate is **decreasing** in the debt share
(B42-adjacent: reading 1 runs 0.0883 at 0.1412 down to 0.0820 at 0.2589). An economy-wide
stock is standing in for a marginal flow, as the brief instructs me to state. If marginal AI
investment is more equity-financed than the average of the existing nonfinancial corporate
stock — which seems likely, given how much of it is funded from retained earnings of
cash-rich firms — then the true marginal debt share is **below** the range used, and the
assembly **understates** `tau_k`. The error runs against the brief's own conclusion, which is
worth saying plainly. It is not large enough to matter: even at a debt share of 0, reading 1
gives roughly 0.090, still below the 0.110 floor.

**On the base (B8).** I have nothing to add that the brief has not already said against
itself, and its statement of the counter-case is fair. I will only note that the result is
robust to which side wins in one specific sense: under **both** rent readings and across
**200,000 draws**, the share of the swept space clearing even the lowest required threshold
of 0.110079 is **0.12 percent (reading 1)** and **0 percent (reading 2)**, and **none** of the
14 one-at-a-time parameter intervals reaches that threshold (B43). No single parameter can be
blamed. If the assembled marginal rate is the wrong object, the argument has to be won on the
choice of object, not on the calibration — exactly where B8 says the real argument is.

**On the 46.9 percent escaping at death.** Modelling it as a rate reduction inside the
deferral factor rather than as a base exclusion matters here more than it usually would,
because the deferral factor is the **largest single source of variance under both readings**
(Sobol first-order 0.298 and 0.461). If those gains are better treated as base exclusion,
the object being taxed changes rather than the rate, and the comparison to a required rate
expressed as a share of a base becomes inconsistent. I flag it; I did not model it.

---

## Reproduction

All work is in `r3/`, self-contained, from `raw/z1_ddp.zip` only:

| file | purpose |
|---|---|
| `prior_bounds.md` | plausibility bounds, written before computation |
| `extract.py` | pulls the 26 Z.1 series from the 620 MB DDP XML into `z1_series.json` |
| `partA.py`, `partA3.py` | builds the twelve- and thirteen-class ratios, 1952–2025, runs the A5 structural checks |
| `solve_ind.py` | the I-1 inversion for the indirect share |
| `partA2.py` | Part A sensitivities and the indirect-share sweep |
| `partB.py` | the B4 assembly, 200,000-draw sweep, B6 checks, Sobol decomposition, one-at-a-time endpoints |
| `mkcsv.py` | emits `results_round3.csv` |

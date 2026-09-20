# Replication report, round two

Scored against `sealed_expected_values_round2.json`, opened only after all 127 of my values
were written to `replication_results_round2.csv` and `brief_insufficiencies_round2.md`.

**Blind declaration.** The blind held, with one qualification I raised before opening the file
and repeat here: Appendix A of the brief prints the section 1 full-sample coefficients, which
are themselves sealed. I therefore knew three sealed values in advance. I declined to adopt
the two DWS vintage values that would have reproduced them, and reported my own unverified
fit instead. That fit turns out to land inside tolerance anyway.

The sealed file was not attached to the request. I found it at the path the brief names,
`notes/sealed/sealed_expected_values_round2.json`, and opened only it and `SEALED_README.md`.
No project code was read at any point in either round.

---

## 1. Scoreboard

| Verdict | Count |
|---|---|
| Match within the brief's own tolerance | 28 |
| Within 5 percent but outside tolerance | 17 |
| Mismatch | 34 |
| No sealed counterpart | 47 |
| Identity check, no sealed value | 1 |
| **Total** | **127** |

Of the 79 quantities with a sealed counterpart, **45 (57 percent) land within 5 percent** and
28 are inside the project's own stated tolerance. Per-quantity detail is in
`comparison_round2.csv`.

The mismatches are not scattered. **Thirty-one of the thirty-four trace to six root causes**,
and four of those six are things I flagged in `brief_insufficiencies_round2.md` before seeing
any sealed value:

| Root cause | Mismatches | Whose side |
|---|---|---|
| A. Exposure index scores for the two cognitive indices | 11 | probably mine, unresolved |
| B. `cases` grid span (their grid includes R = 0, mine does not) | 6 | mine |
| C. Incidence case definitions (my I-5) | 4 | brief |
| D. Section 3 embodied row near the pole (my I-3) | 2 | brief |
| E. Second-round level via dW/W (my I-4) | 2 | brief, plus one bug of mine |
| F. Section 14 Treasury class level | 3 | brief, not reproducible from the named source |
| Residual, individually explained | 3 | mixed |

---

## 2. What reproduced exactly

Worth stating first, because these are the load-bearing ones.

- **`fiscal.R_2026` = 0.568315 against 0.568316.** Reached only by discovering that the
  brief's stated part-time wage assignment of 0.50 does not reproduce the brief's own omega,
  and that the sourced 0.3206 does. I reported both before opening the file. The sealed value
  confirms 0.3206 is what the code uses.
- **`fiscal.tau_k_sourced_low` and `_high`**, 0.03245 and 0.20351, exact.
- **`rho_slack.x_range_low` and `_high`**, 18.27241 and 24.70612, exact.
- **`debt.debt_to_gdp_start` = 1.214121**, exact to six decimals, and
  **`baseline_20y_emerging_market` = 376.74 percent**, exact.
- **`second_round.demand_event_first_share` = 0.740741**, exact, and it factorises 20/27
  exactly as section 11e says.
- **`sovereign.federal_student_share` = 0.972808**, exact.
- **All four under-reporting factors and all four coverage shares**, inside the 2 percent
  survey tolerance, with the factor-over-coverage identity holding to three decimals on every
  book.
- **`labour_backing.class_home_mortgage_backing` = 0.840223** and
  **`class_multifamily_mortgage_backing` = 0.72754**, both exact to the last published digit,
  rebuilt independently from ACS mortgage service and gross rent.
- **`fiscal_magnitudes.terminal_year_loss_bn_at_10pct`**, 85.01 against 85.168, 0.19 percent.
- **`condition_passes` = false**, with both halves of the claim confirmed.

Seven of the nine section 14 backing shares match, two of them exactly. Given that section 14
had never been checked from outside, that is the strongest single result in this round.

---

## 3. (a) The GSE result, in full

### What the brief told me to do

Section 10b gives the waterfall verbatim and insists on the order:

    transferred = min(GSE loss, CRT risk in force + PMI risk in force)
    retained    = GSE loss - transferred
    absorbed    = min(retained, Enterprise capital + one year of PPNR)
    beyond      = max(0, retained - Enterprise capital - one year of PPNR)   FEDERAL

with CRT risk in force **210.0bn**, PMI risk in force **382.855bn** (Fannie 201.355 + Freddie
181.5), Enterprise capital **190.436bn** and one year of PPNR **34.24bn**. It states, in bold,
that CRT and PMI are **loss transfers taken BEFORE Enterprise capital, not additions to it**,
and calls that the thing easiest to get wrong.

### Exactly what I did

1. Built exposure at default on SIPP working-core households (definition B) with the GHOW
   uplift: `dp = p_one x 0.050 + p_two x 0.080` over a binomial draw at s = 0.10 on each
   household's earners, capped at two.
2. Scaled by the mortgage under-reporting factor **1.2647** first, giving EAD = **91.875bn**.
3. Applied the top of the mortgage LGD range, **0.40**, giving a national mortgage loss of
   **36.750bn**.
4. Split by the section 10d holder shares and took the GSE slice, **0.511**, giving a GSE loss
   of **18.779bn**.
5. Ran the waterfall as written: transfer layer = 210.0 + 382.855 = **592.855bn**;
   `transferred = min(18.779, 592.855) = 18.779`; `retained = 0`; `absorbed = 0`;
   **`beyond = 0`**.

So the federal layer is zero because the GSE loss is roughly **one thirty-second** of the
transfer layer. Enterprise capital plus PPNR (224.676bn) is never reached, and never even
approached.

### The finding this exposes

I swept the dose to check whether the federal layer is ever nonzero:

| dose | GSE loss | transfer layer | beyond |
|---|---|---|---|
| 10 percent | 18.78bn | 592.9bn | 0 |
| 25 percent | 45.51bn | 592.9bn | 0 |
| 50 percent | 86.23bn | 592.9bn | 0 |
| 100 percent | 153.30bn | 592.9bn | 0 |

**Under the brief's own stated parameters the `beyond` layer is identically zero at every dose
in [0, 1].** Reaching it would need a GSE loss above 592.9bn, which requires a dose of roughly
316 percent of the total wage bill. The federal GSE term is dead code.

That is a criticism of the construction, not of my arithmetic, and it has a specific cause.
**CRT and PMI risk in force are not first-loss layers.** Risk in force is maximum coverage.
Credit risk transfer is overwhelmingly mezzanine: the Enterprise retains a first-loss tranche
and CRT attaches above it. Private mortgage insurance covers from the first dollar but only on
the roughly 6 percent of the single-family book that carries it, and only up to the coverage
percentage. Writing the transfer as `min(GSE loss, risk in force)` grants both instruments
first-dollar coverage at their full notional, which is why the layer is unreachable.

The brief also flags CRT risk in force as **stale** (4Q2023 against a 2026 book). That flag is
real but immaterial here: the layer overshoots by a factor of thirty-two, so no plausible
updating of it changes the answer.

The conservatorship flag does travel with my figure, as the brief requires: Enterprise net
worth is not loss-absorbing capital of the same kind as bank CET1, the Treasury senior
preferred agreements sit behind it, and this is a scale comparison rather than a solvency
test. None of that is load-bearing when the layer is never touched.

`sovereign._ordering` in the sealed file confirms the ordering I used. There is **no sealed
GSE quantity**, so my three GSE rows are scored NOT SEALED. I would have valued one here,
precisely because the result is degenerate.

---

## 4. (b) The federal share of first-round losses by wage quintile

### It has no sealed counterpart

The `sovereign` block seals only `federal_share_first_round_min` / `_max`,
`federal_share_with_second_round_min` / `_max` and `federal_student_share`. There is no
quintile decomposition anywhere in it. The only quintile quantities in the sealed file are
`labour_backing.quintile_labour_backed_per_wage_dollar_Q1` (4.1489) and `_Q5` (0.6548), which
are a different object from a different section, referenced only as "B5" and described nowhere
in the brief.

My five quintile rows are therefore scored NOT SEALED. My values:

| quintile | wage share | federal share |
|---|---|---|
| Q1 | 0.0400 | 0.7328 |
| Q2 | 0.0871 | 0.7701 |
| Q3 | 0.1405 | 0.7475 |
| Q4 | 0.2161 | 0.7534 |
| Q5 | 0.5163 | 0.8094 |

Flat at roughly 0.73 to 0.77 across the bottom four and rising to 0.81 in the top, because the
fiscal component follows the wage bill while the credit component follows balances. The
allocation rule is mine; the brief gives none, which was insufficiency I-9.

### The nearest sealed quantity

Computing the sealed-comparable object on the same SIPP quintiles:

| | mine (raw) | mine (normalised) | sealed |
|---|---|---|---|
| Q1 labour-backed per wage dollar | 1.2095 | 1.6414 | **4.1489** |
| Q5 labour-backed per wage dollar | 0.5691 | 0.7723 | **0.6548** |

Q5 is within 13 to 18 percent depending on normalisation. Q1 is off by a factor of 2.5 to 3.4.
The likely cause is the bottom-quintile definition: I restrict to working-core households with
**positive wage income**, which removes exactly the near-zero-wage, high-debt households that
would drive a Q1 ratio of 4.15. The brief never defines B5's universe or its normalisation, so
I cannot close this.

### How much of the gap is explained by the GSE result: none of it

This was the specific question. The answer is quantitative and clean.

My `federal_share_first_round` range is 0.779 to 0.837; the sealed range is 0.759 to 0.916. My
range is narrower at both ends.

The GSE waterfall contributes **exactly zero** to the federal side at every dose, so one might
ask whether a nonzero `beyond` would close the gap at the top. It cannot. I ran the ceiling
test: reclassifying the **entire** GSE loss as federal at the 10 percent dose, which is the
most extreme reallocation the holder split permits, moves the federal share from 0.779 only to
**0.8644**, still short of the sealed 0.916.

So **none** of the sovereign gap is attributable to the GSE treatment. The actual driver is the
dose axis. Sweeping the dose at the low LGD end:

| dose | federal share |
|---|---|
| 10 percent | 0.8373 |
| 25 percent | 0.8792 |
| 50 percent | 0.8956 |

The federal share rises with the dose because the fiscal component grows superlinearly (R
falls as slack rises) while credit losses grow roughly linearly. The sealed 0.916 is reachable
on that axis and on no other I tested. My min of 0.779 against their 0.759 points the same way:
their grid is simply wider than mine.

This is exactly insufficiency I-6. The brief seals a min and a max and never says what they are
taken over. I swept LGD and dose; they evidently sweep at least one more dimension. The error
is on the brief's side, and it is a documentation error rather than an arithmetic one, because
every component I could pin down individually matches.

---

## 5. (c) The pole at d_emp = 0.676150

### The formula

Section 3a specifies rho as the fixed point of the stock-flow identity

    nonemp = nonemp_0 + 100 * d_emp * (1 - rho) * (1 - 0.462)

against the section 1 fitted line `rho = INT + SLOPE * nonemp`. Substituting and solving for
rho in closed form:

    rho = (INT + SLOPE * NE0 + SLOPE * c) / (1 + SLOPE * c),    c = 100 * d_emp * 0.538

with INT = 1.227975, SLOPE = -0.02749, NE0 = 19.31092 and the exit share 0.462. The denominator
vanishes when `SLOPE * c = -1`, that is at

    d_emp = 1 / (0.02749 * 100 * 0.538) = **0.676150**

Equivalently, the naive iteration `rho -> INT + SLOPE * (NE0 + 100 * d_emp * (1 - rho) * 0.538)`
has multiplier `|SLOPE| * 100 * d_emp * 0.538`, which exceeds 1 above the same threshold. Below
it the map is a contraction and iteration converges; above it the iteration diverges outright,
which I reproduced before solving it algebraically.

### The doses affected

`d_emp` is the employment dose, which is the wage-bill dose divided by the group's relative
wage. With ACS relative wages of 0.6789 (embodied), 1.1996 (GPT) and 1.5047 (AIOE):

| wage-bill dose | embodied d_emp | GPT d_emp | AIOE d_emp |
|---|---|---|---|
| 10 percent | 0.1473 | 0.0834 | 0.0665 |
| 25 percent | 0.3682 | 0.2084 | 0.1662 |
| **50 percent** | **0.7365 past the pole** | 0.4168 | 0.3323 |

- **10 percent: safe.** All three groups sit far below the pole, the map is well conditioned,
  and my terminal loss of 85.01bn matches the sealed 85.168 to 0.19 percent.
- **25 percent: degraded.** The embodied group at 0.3682 sits on the steep approach, where the
  denominator has fallen to 0.455 and rho is highly sensitive to `d_emp`. This single row is
  the entire reason my 338.17bn misses the sealed 301.89bn by 12.02 percent. The other two rows
  are well behaved. Note also that the embodied row's terminal nonemployment of 32.49 exceeds
  the observed maximum of 24.71, so the brief's own extrapolation flag fires on it.
- **50 percent: undefined for the embodied group.** At `d_emp = 0.7365` the denominator is
  negative and rho comes out at +4.39, far outside [0, 1]. The quantity does not exist. This is
  why the headline scenario can only be a cognitive one: the AIOE group at 0.3323 stays on the
  well-conditioned side.

The threshold in wage-bill terms is a dose of 0.459 for the embodied group, 0.811 for GPT and
1.017 for AIOE.

### Whose side

The brief's. It specifies the fixed point and the 24.71 extrapolation flag but says nothing
about the pole, gives no clamping rule for rho, and does not say whether flagged rows enter the
cross-group mean. The sealed 301.89 implies the project does something at the 25 percent dose
that tames the embodied row; three defensible readings give three different answers and the
brief distinguishes none of them. That was insufficiency I-3, written before I saw the sealed
value, and the sealed value confirms the diagnosis.

A plausibility bound is also at stake. rho is a reemployment rate and must lie in [0, 1]. The
stated construction produces rho = +4.39 at a dose the brief itself uses as its headline. The
brief's section 9 bounds should have caught that and do not cover it.

---

## 6. (d) The sovereign share gap of 0.016

Sealed `labour_backing.sovereign_share_union` = **0.793592**; mine = **0.777810**. Absolute
difference **0.0158**, against a 0.01 absolute tolerance. Relative difference 1.99 percent, so
this is a near miss rather than a failure: it is my closest scored miss on any priority
quantity.

### Where it comes from

The sealed file publishes the full 13-class table, which lets me decompose this exactly.

**It is not the backing shares.** Seven of nine match, two exactly:

| class | my backing | sealed backing |
|---|---|---|
| home mortgage | 0.840223 | **0.840223** |
| multifamily | 0.727540 | **0.727540** |
| credit card | 0.740284 | 0.740 |
| auto | 0.776467 | 0.7737 |
| student | 0.881832 | 0.8832 |
| state and local | 0.163185 | 0.159338 |
| **treasury** | **0.633842** | **0.657788** |

**It is the Treasury class.** My total labour-backed claims are 35,721.4bn against the sealed
40,380.5bn, a shortfall of 4,659.1bn. Decomposing:

| source of shortfall | bn | share of the gap |
|---|---|---|
| Treasury class (level and backing together) | 3,900.6 | **83.7 percent** |
| `other_consumer` class, which I omitted entirely | 307.9 | 6.6 percent |
| level differences on the four household books | about 450 | 9.7 percent |

The sealed Treasury class level is **33,887.1bn**. I used the Z.1 all-sector Treasury securities
asset total, **29,013.6bn**. Those differ by 4,873bn and the labour-backed Treasury is the whole
obligor leg, which is why `sovereign_share_obligor` misses by 0.037 (0.5148 against 0.5520)
while `sovereign_share_held_or_guaranteed` misses by only 0.014 in the opposite direction. The
two errors partly cancel, which is precisely the compensating-error signature I flagged as I-10
before opening the file.

### The Treasury level is not reproducible from the source the brief names

I searched every FL and LM series in the full Z.1 Data Download archive for a 2025 Treasury
level between 33,500 and 34,300bn. **There is none.** The nearest 2026Q2 candidates are:

| concept | level |
|---|---|
| All sectors, Treasury securities, asset | 29,013.6bn |
| Federal government, total marketable Treasury securities, liability | 30,878.3bn |
| Federal government, Treasury securities held by the public, liability | 31,490.7bn |

All three are below 33,887.1, and since the sealed value is for **2025**, a year when the stock
was smaller still, the gap is wider than it looks. The sealed figure is therefore either a sum
of series or drawn from outside Z.1, and section 14 names neither the series nor the
aggregation. This is a concrete, checkable defect and it is the single largest driver of the
headline number in the section the brief itself calls entirely unchecked.

### Two further vintage and scope differences

- **Vintage.** The sealed block states "all values are for the latest complete Z.1 year,
  **2025**". The brief's section 14.1 does not say this; every other module in the brief is
  pinned to 2026Q2, which is what I used. The vintage is stated only inside the sealed file,
  which a replicator is not supposed to open first.
- **Class count.** The sealed table has **13 classes**; I built **11**. I omitted
  `other_consumer` (377.6bn at a backing of 0.815554) and I did not split business debt into
  corporate loans and noncorporate. The brief's 14.2 lists the zero-rule classes in prose and
  never enumerates the thirteen.

Neither the class list nor the omissions move the union much, because the union is a ratio
**within** labour-backed claims and the zero-rule classes cancel out of it. That is also why
`direct_labour_backing_ratio` is not comparable at all: mine is 0.168 against the sealed
0.270271, entirely because my total-claims denominator is 212,644bn against their 149,407bn,
driven by corporate equity at 2026Q2 market value (123,687bn) against their 71,995bn.

---

## 7. The remaining mismatch clusters

**A. Exposure index scores, 11 mismatches.** This is my largest unexplained cluster and the
likeliest to be my error. Two strong controls pass: `cap_contrast.ACS.ALL` (my 0.898459 against
0.8985) and both embodied shares (ACS 0.9794 against 0.9775, SIPP 0.8830 against 0.8837) all
match. So the ACS and SIPP wage machinery, the 184,500 cap, the weights and the embodiment
index P rebuilt from Appendix B's full 15 elements are all correct. The discrepancy is confined
to the two **cognitive** index scores: my AIOE group is higher-wage than theirs (ACS cap share
0.8506 against 0.8119) and my GPT group is lower-wage (0.8939 against 0.9075). The errors run
in opposite directions, so it is not a single systematic weighting mistake. My crosswalk match
rates reproduce the brief exactly (530 codes, AIOE 476, GPT 524), so the brief's stated
diagnosis for AIOE divergence does not apply. This cascades into all six `pay_control` raw gaps
and into the dW/W of cluster E. Unresolved; I would want the occupation-level index table to
settle it.

**B. The `cases` grid, 6 mismatches.** Sealed `break_even_tau_k_case_A_max` is **0.301**,
exactly tau_l, and its note says "at R = 0". My grid evaluates R only at the three values the
exposure groups actually produce, so my maximum is 0.2264. The formula is identical and my
bounds all hold; their grid simply spans R down to zero and mine does not. This is my error,
and a trivial one: the brief says case A's maximum "is tau_l exactly, reached where R falls to
zero", which I should have read as a specification of the grid rather than as a remark.

**C. Incidence, 4 mismatches.** Sealed count spread 1.049 to 1.092; mine 1.588 to 1.594. Sealed
dollar spread 1.75 to 3.01; mine 1.589 to 2.143. Exactly as predicted in I-5: my case (c)
treats attrition-absorbed job destruction as hitting no household, which makes case (c) reach
far fewer households than case (a). The sealed count spread of 5 to 9 percent is only
achievable if the three cases hit nearly identical household counts, which requires the other
reading. The brief does not state which. Brief's side, and it reverses a qualitative claim, so
it matters.

**D. Section 3 at 25 percent, 2 mismatches.** Covered in section 5 above. Brief's side.

**E. Second-round levels, 2 mismatches, plus a bug of mine.** Opening the sealed file exposed a
genuine error in my own script: `s11_secondround.py` used the observed `R_2026` = 0.568316
instead of the extended-axis R = 0.347726 at the headline dose. I have corrected it and amended
the results file, marking the six affected rows as amendments. Corrected, my min is 183.48
against 173.47 and my max 1655.05 against 1564.77, both 5.77 percent high. That residual is
**entirely** the dW/W difference: sealed dW/W is 0.314167, mine 0.326137, 3.81 percent high,
and 1.0381 raised to the convex mapping's exponent of 1.5 is 1.0579, which reproduces the 5.77
percent exactly. Both the min and the max come from the convex mapping. House prices, which are
linear in dW/W, miss by exactly 3.81 percent. The dW/W difference is in turn the cognitive AIOE
relative wage, so cluster E reduces to cluster A.

**F. Section 14 Treasury, 3 mismatches.** Covered in section 6.

**Residual three.** `card` and `auto` first-round losses miss by 7.3 and 6.1 percent, just
outside the 5 percent band, from small SIPP balance differences; the other two books are inside
it. `sovereign.federal_share_first_round_max` is covered in section 4.

---

## 8. Errors found in the sealed file and the brief

Three, all on the project's side, and all found by rebuilding rather than by reading.

1. **The brief's stated omega parameter contradicts its stated omega.** Section 2a assigns part
   time 0.50; that gives 0.925467. The sourced 0.3206 gives 0.907268, which is what the brief
   and the sealed R both use. Reported before opening the file. The prose is wrong.
2. **`fiscal.condition_passes` carries a false note.** Its note reads "required tau_k exceeds
   the top of the sourced range at every reading of tau_l". It does not: the required rate maxes
   at 0.137 against a sourced top of 0.20351, and the brief's own section 2d says so explicitly
   and insists that clause must travel with the result. The boolean `false` is correct; the note
   contradicts both the brief and the arithmetic, and it contradicts it in the direction that
   overstates the finding.
3. **Section 10d's holder shares sum to 100.1 percent.** 51.1 + 12.6 + 11.5 + 24.9. The residual
   is described as "the arithmetic remainder" and the true remainder is 24.8. This is the one
   stated plausibility-bound breach I found: holder shares must sum to 1.

I also record that the brief mis-names FRED `W055RC1Q027SBEA` as federal personal current taxes
(that series is 3,263.5bn); the 2,571.4bn value it quotes is `A074RC1Q027SBEA`. The value is
right and the identifier is wrong.

---

## 9. Bounds

Every plausibility bound I stated before computing held, with the single exception above, which
is a bound the brief breaks rather than one I break.

- All shares in [0, 1]; the four quintile wage shares sum to 1.000000.
- No loss exceeds its tax base or its balance; no subset exceeds its total.
- Trust fund losses stay strictly between 0 and 100 percent of fund payroll income, against the
  107 and 215 percent an earlier version of the project produced.
- **All eight section 9 break-even bounds hold, zero breaches**, against two in round one. Case
  A maxes at 0.2264 below tau_l = 0.318; case B maxes at 0.5354 below 1; case B never falls
  below case A.
- **The hedge ratio is exactly 1.000000 at the break-even rate on all 91 grid points**,
  confirming the section 14.5 gross-versus-net construction.

One bound the brief does not carry but should: **rho must lie in [0, 1]**. The section 3a
construction violates it at the headline dose for the embodied group, as section 5 above sets
out.

---

## 10. What I could not do

**`two_sided_bet` is returned empty.** All ten of its quantities depend on
`data/processed/legA_tier2.csv`, which the brief names as "already in the repository" but never
describes. Now that the sealed file is open I can see what was wanted: nine named SEC filers,
their long-term debt plus finance leases, capex against operating cash flow, and an AI equity
scale swept over 0.10, 0.20 and 0.30 of US nonfinancial corporate equity. **None of that firm
list appears anywhere in the brief.** The nine filers are not named, the selection rule is not
given, and the tier definition is not stated. This was insufficiency I-11 and the sealed file
confirms the block was unavoidable.

One item in that block I can now score. `share_of_federal_wage_loss_hedged_at_operative_tau_k`
is sealed at **0.36**; I computed **0.5447** using `surplus = D`, the gross displaced wage bill.
The brief's 14.5 says to use `published_loss + 0.0708 x surplus` and never defines `surplus`.
Back-solving from 0.36 implies a surplus of about 628bn against my D of 1,336.5bn, so the
project means something narrower. My construction is self-consistent, since it satisfies the
brief's own stated check that the ratio equals 1 at break-even, but the input is undefined.
That is an additional insufficiency, I-12, discovered only on scoring.

Also unattempted: `pay_control`'s `distress_pp_per_bn` outcome, because the brief never defines
debt service for the four books and neither survey supplies scheduled payments;
`federal_share_with_second_round`; and the `labour_backing` historical series (1947 to 2025,
plus the 1970 and 2008 waypoints), which needs the pre-2021 fixed-labour-share construction the
brief describes only in outline.

---

## 11. Verdict

**The headline results stand.** The fiscal condition fails, and fails for the stated reason: the
required capital tax rate of 0.107 to 0.137 exceeds the operative 0.0708 at every reading of
tau_l, and does not exceed the sourced maximum of 0.20351, so the condition is unclosable under
the tax code as it stands rather than under every reading of the literature. Both halves
reproduce. `R_2026`, the tau_k grid, the debt start ratio, the emerging-market baseline, the
under-reporting factors and `demand_event_first_share` all reproduce. The sovereign union
reproduces to within 2 percent from a completely independent rebuild of a section that had
never been checked.

**Three results do not stand as stated.**

1. **The incidence count claim.** "Incidence moves household counts by 5 to 9 percent, and the
   count figures are robust to it and can stand alone" is not reproducible. Under the reading of
   case (c) that I find most natural the spread is 59 percent, which removes the robustness the
   claim rests on. Until the brief says which reading is intended, the sentence should not be
   published.
2. **The 25 percent dose figures.** They sit on an embodied row approaching a pole that the
   construction does not handle and the brief does not mention. The 10 percent figures are
   sound; the 25 percent ones are not, and the 50 percent headline is undefined for one of the
   three groups.
3. **The `beyond` layer of the GSE waterfall.** It is identically zero at every dose in [0, 1]
   under the brief's own parameters, because risk in force is treated as first-loss coverage.
   Any text implying the Treasury backstop is reached through the agency book in this model is
   not supported by the model.

**For round three**, in priority order: name the nine AI filers and the Treasury series; state
the section 14 vintage in the brief rather than only inside the sealed file; state the rho
clamping rule and add rho in [0, 1] to the section 9 bounds; define `surplus` in 14.5; publish
the fourteen DWS y values and remove the coefficients from Appendix A; state what the sovereign
min and max are swept over; fix the part-time parameter, the `condition_passes` note and the
holder shares that sum to 100.1; and either re-derive the CRT and PMI layer with attachment
points or drop the `beyond` term and say the agency book is fully transferred at this scale.

The pattern from round one repeats and is worth naming: **what is stated reproduces, and what
is referenced does not.** Every quantity whose inputs are printed in the brief landed inside or
near tolerance. Every quantity depending on a file path, an internal appendix label such as B5
or B11, or a parameter named but not pinned, either missed or could not be attempted at all.

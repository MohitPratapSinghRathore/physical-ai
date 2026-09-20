# Brief insufficiencies, round two

Replication of `replication_brief_v2.md`, rebuilt from raw public data with no sight of `src/`.
Written before the sealed round-two file was opened. Blind declared intact except where noted
in I-1, which concerns a value the brief itself publishes in Appendix A.

Ordered roughly by how much each one moves a number.

---

## I-1. Appendix A publishes the answer to section 1, so section 1 is no longer a blind test

Section 1 seals `rho_slack.intercept`, `.slope` and `.r_squared`. Appendix A then prints the
full-sample coefficients in a table: intercept 1.22798, slope -0.02749, R squared 0.77333.

A replicator who reads the brief to the end knows three sealed values before computing them.
That is not a small disclosure: it is the whole of section 1 apart from `n` and the x range.

This bit me concretely. My own DWS series gives 1.21969 / -0.02717 / 0.76318. The gap traces
to exactly two of the fourteen y values. A five-minute grid search over plausible published
integers for the five pre-2010 vintages finds that 2002 = 65 and 2008 = 68 reproduces the
Appendix A triple to five decimals and nothing else comes close. I could not verify those two
against BLS: `bls.gov/news.release/*` returns HTTP 403 to automated retrieval, and probing
`news.release/archives/disp_MMDDYYYY.txt` across July to September of 2002 and 2008 found no
file. So I am in the position of knowing the answer and not being able to source it.

**I report the unverified fit and did not adopt the grid-searched one**, because adopting it
would be fitting to a disclosed target rather than replicating. But the brief should either
(a) give the fourteen y values outright, as it gives the x endpoints, or (b) not print the
coefficients in an appendix. Right now it does the worst of both.

Note also the strong positive: my post-2008 fits reproduce Appendix A **exactly** on both
specifications, which independently confirms all nine post-2008 y values and the whole x
construction. The x endpoints 18.27241 and 24.70612 also match exactly.

---

## I-2. The brief's stated omega parameter does not reproduce the brief's stated omega

Section 2a says, verbatim: "Part time is assigned **0.50** of the prior wage (the sourced
part-time to full-time earnings ratio is 0.3206 in 2025, so 0.50 is an upper bound)."

Follow that instruction and `omega_blended_nominal` comes out at **0.925467**. The brief says
it is **0.907268**.

Substitute 0.3206 for 0.50 and it comes out at **0.907269**, six-decimal agreement. The
counterfactual step then gives 0.859781 against the brief's 0.859782, and R_2026 gives
0.568315 against the brief's 0.568316.

So the project's code uses 0.3206 and the brief's prose says 0.50. The prose reads as though
0.50 were the central assignment and 0.3206 merely the justification for calling it an upper
bound; the arithmetic says the reverse. This is the same class of defect version 1 was
criticised for, in a section rewritten specifically to fix it.

I carry both values in the results file and flag which is which. The error sits on the brief's
side: the parameter statement is wrong, not the result.

---

## I-3. Section 3's extended axis has an undisclosed pole, and no clamping rule

Section 3a gives the fixed point

    nonemp = nonemp_0 + 100 * d_emp * (1 - rho) * (1 - 0.462)

with rho from the fitted line. Solved algebraically this is

    rho = (INT + SLOPE*NE0 + SLOPE*c) / (1 + SLOPE*c),   c = 100 * d_emp * 0.538

and the denominator vanishes at **d_emp = 0.676150**. Below that the map is a contraction and
iteration converges; at and beyond it rho is unbounded or negative and naive iteration
diverges outright (I reproduced the divergence before solving it algebraically).

This is not hypothetical. The embodied exposure group has a relative wage of 0.679, so a
50 percent wage-bill dose gives it d_emp = 0.7365, **past the pole**. At a 25 percent dose it
sits at 0.3682, on the steep part of the curve, and that single row is the entire reason my
25 percent terminal loss comes out at 338.17bn against the brief's 301.89bn while my
10 percent value matches to 0.2 percent (85.01 against 85.17).

The brief says rows above 24.71 nonemployment must be flagged as extrapolations. It does not
say whether such rows are clamped, dropped from the cross-group mean, or carried raw; and it
says nothing at all about the pole. Three defensible readings give three different 25 percent
answers. **The brief must state the clamping rule and whether extrapolated rows enter the
mean.**

Related and smaller: the brief never states how a wage-bill dose becomes the employment dose
`d_emp` that the identity requires. I used each group's mean wage relative to the economy mean
from ACS, which is what makes the three exposure groups differ at all on this axis. That the
10 percent value then lands within 0.2 percent is good evidence the reading is right, but it
was inferred, not given.

---

## I-4. "A 50 percent cognitive AIOE dose" is never defined

Section 11e calls the headline scenario the "50 percent cognitive AIOE dose". Section 3 insists
the axis is always the share of the **total** wage bill. Section 11a writes `D = delivered dose
* W`.

Three readings are available and they differ by an order of magnitude:

1. 50 percent of the **total** wage bill, with the AIOE group naming which workers (and hence
   the relative wage used to convert to an employment dose);
2. 50 percent of the **AIOE group's** wage bill, which is 0.5 x 0.2707 = 13.5 percent of the
   total;
3. 50 percent of the group's **employment**.

Only reading 1 can produce the `dW / W` of "about 0.314" that section 11b reports, because
readings 2 and 3 would need `(1 - R)` above 2. So I took reading 1. It gives me 0.3261, four
percent above the brief's figure; closing that gap exactly would need an AIOE relative wage of
1.586 against the 1.5047 that ACS gives me.

Everything scale-invariant in section 11 reproduces exactly regardless: 648 combinations, the
`demand_event_first_share` of 0.740741 (which factorises 20/27 precisely as 11e says), the
factor-of-nine loss spread. Only the **levels** depend on this ambiguity. The brief should say
which denominator "dose" is taken against, once, in section 3, and then never vary the phrase.

---

## I-5. Section 7's three cases are not defined tightly enough to reproduce the count spread

The brief reports that incidence moves household **counts** by only 5 to 9 percent, and calls
the count figures robust enough to stand alone. I get **59 percent**. That is not a small
numerical gap; it reverses the qualitative claim.

Two undefined choices produce it:

- **Case (c).** "Attrition absorbs job destruction up to the BLS labour force exit rate of
  3.86 percent a year; the remainder falls on incumbents." I read attrition as hitting no
  household at all, so case (c) touches only 6.14 points of incumbent displacement and
  necessarily reaches fewer households than case (a)'s full 10. If instead the attriting
  households are counted as affected, case (c) converges on case (a) and the spread collapses
  toward the brief's range. The brief does not say.
- **Case (b).** It is unclear whether the Brynjolfsson 19 percent figure *calibrates the size*
  of the entrant shock or merely *motivates* it while case (b) still delivers the same
  10 percent of total employment. I took the latter, per 7c's "holding the total employment
  loss fixed". The former would change the count materially.

The **dollar** spread is in far better shape: I get 1.59 to 2.14 against the brief's 1.75 to
3.01, overlapping ranges and the same order. And the brief's headline clause, that no dollar
figure may be quoted without naming the incidence assumption, is confirmed strongly, since
dollars move several times more than counts under every reading I tried.

One further gap: 7b says the equity split is SIPP-only and "ACS carries the tenure and scale
side", but never says how the two are combined into a single spread. I ran both counts and
dollars on SIPP for internal consistency and recorded that as my choice.

---

## I-6. Section 10 never says what the sovereign min and max are taken over

`sovereign.federal_share_first_round_min` and `_max` are sealed as a pair, and the text gives
0.759 to 0.916. The construction says only "at each dose, sum every loss that ultimately lands
on the federal government and compare with the sum landing on private balance sheets."

A min and a max require a grid, and no grid is stated. Varying the two LGD ends at a 10 percent
dose I get **0.779 to 0.837**. Adding the 25 percent dose widens it to **0.779 to 0.879**.
Neither reaches 0.916. Candidate further dimensions the brief leaves open: the three tau_l
readings, the three exposure groups, the rho mode, whether scenario outlays are in or out,
whether the second-round column is included.

Every component I can pin down individually matches well, the federal student share is
0.972808 against 0.973, the OASDI payroll share is exact, the GSE layer is unambiguous, so I
believe the difference is entirely in what the range is swept over, not in the components.

---

## I-7. The pay control's four cells are defined but the reweighting is not

Section 6a is much improved: two outcomes, two directions, and the sign-reversal warning are
all now explicit, and the qualitative result reproduces cleanly. The SIPP Eloundou GPT cap
contrast **does** reverse sign in both directions in my rebuild (a = 1.64, b = 2.17), exactly
as predicted, and my ACS direction-a values (0.926, 0.943) sit inside the brief's stated
weaker-end band.

What is missing is the mechanics of the reweight itself. "Reweighted onto the other group's
distribution across deciles of individual annual wage income" does not say whether the deciles
are cut on the pooled employed population, on the source group, or on the target group;
whether they are employment-weighted; or how empty cells are handled. I cut on the pooled
employed distribution with person weights and mapped ratio factors cell by cell.

My ACS AIOE direction-b value is **0.672783** against the brief's explicitly named 0.539456 , 
outside tolerance, and decile-cut convention is the most likely cause.

Separately, the second outcome, `distress_pp_per_bn`, is defined as "the increment in the share
of obligated working-core households above a 50 percent debt-service-to-income ratio, per
billion dollars of wage income destroyed", but the brief never defines **debt service** for
the four books. ACS supplies mortgage payment and gross rent; it has no card, auto or student
service, and SIPP supplies balances rather than scheduled payments. Without an amortisation
convention this outcome cannot be rebuilt. I did not attempt it and it is my largest
unattempted item after I-11.

---

## I-8. Small stated-arithmetic errors

Three, all minor individually, all in tables presented as authoritative:

- **Section 10d.** The four mortgage holder shares are given as 51.1 + 12.6 + 11.5 + 24.9 =
  **100.1 percent**. The residual is described as "the arithmetic remainder", and the true
  remainder is 24.8. This is the one stated plausibility-bound violation I found: holder shares
  must sum to 1 and these do not.
- **Section 2b.** Federal personal current taxes are attributed to FRED `W055RC1Q027SBEA`. That
  series is 3263.468bn at 2026Q2. The stated 2571.4bn is `A074RC1Q027SBEA`. The value is right
  and the identifier is wrong, which matters in a brief whose stated purpose is parameter
  disclosure.
- **Section 2a.** rho_2026 is given as 0.6610 while the stated counts give 2199/3324 =
  0.661552. R_2026 = 0.568316 is reproducible only from the rounded value. Harmless here, but
  it means R carries a rounding the brief does not flag.

---

## I-9. No rule for distributing a fiscal loss across households

The priority list asks for the federal share of first-round losses **by wage quintile**. The
credit side distributes naturally, because losses are built household by household. The fiscal
side does not: general revenue, OASDI and HI losses are computed in aggregate in section 3 and
the brief gives no rule for attributing them to households.

I allocated them by each quintile's share of the working-core wage bill, which is the natural
reading given that the loss is a wage-tax loss. On that rule the federal share is close to flat
at 0.73 to 0.77 across the bottom four quintiles and rises to 0.81 in the top, because the
fiscal component tracks the wage bill while the credit component tracks balances. The result is
sensitive to the rule and the rule is mine, so I would not defend the level, only the shape.

---

## I-10. Section 14 gives two incompatible instructions on claim levels

14.1 says to take every claim level from the Z.1 CSV package. 10a defines the federal student
share as 1605.134 / 1650, using the NY Fed book. Z.1 puts household student loan liabilities at
**1858.2bn**, not 1650. The two cannot both be followed, and the choice propagates into the
denominator of the whole ratio.

Both readings, with everything else identical:

| reading | sovereign union | brief |
|---|---|---|
| household books at the official 2026Q2 aggregates (sections 4, 5, 10) | **0.777810** | 0.7936 |
| all levels from Z.1 household liabilities | **0.765500** | 0.7936 |

I report the first as primary because it is consistent with the rest of the project, and carry
the second. Neither is inside the 0.01 absolute tolerance, though the first is close.

Three further section 14 gaps:

- **The package named is the wrong one.** `z1_csv_files.zip` from `/releases/z1/current/`
  contains only the S and F tables (308 CSVs, no holder detail, no central bank sector). The
  brief's own instruction, "Series are keyed FL/LM + 2-digit sector + 7-digit instrument. The
  `data_dictionary/` folder maps every code", describes data that package does not carry. I
  had to fall back on the Data Download Program XML
  (`datadownload/Output.aspx?rel=Z1&filetype=zip`, 620MB uncompressed) to get sector 71 at all.
  Without that the Fed's 4,082.7bn of Treasury holdings are simply absent and the overlap term
  is zero.
- **The legs are under-specified and the union hides it.** My union misses by 0.016 while my
  obligor leg misses by 0.037 (0.5148 against 0.5520) and my holder leg misses by 0.014 in the
  *opposite* direction (0.3354 against 0.3215). Two errors of opposite sign and a matching
  union is a compensating-error signature. Something in how federal holdings are split between
  "holds it" and "owes it" differs from my reading, and the brief's three-line description of
  the legs is not enough to locate it. Since 14.3 calls confusing the legs "the trap in this
  section", it deserves a worked example.
- **Four inputs are project-internal files.** 14.1 requires
  `data/processed/under_reporting_factors.csv`, `data/processed/stress/a38_correction_decomposition.csv`,
  `data/processed/labor_tax_share.json` and `data/processed/legA_tier2.csv`. Three I could
  rebuild from my own sections 4 and 6 and from the stated SOI share of 0.6675. The fourth I
  could not, see I-11.

---

## I-11. `legA_tier2.csv` blocks the AI-leg holder shares outright

Section 14.1 lists `data/processed/legA_tier2.csv`, "AI capital spenders' capex, operating cash
flow, debt", as "already in the repository", and 14.7 item 5 points at "the AI equity scale in
B11". Neither the firm universe, the selection rule, the tier definition, the vintage nor any
of the values appears anywhere in the brief, and nothing in the stated public sources
reconstructs it.

`two_sided_bet` is therefore the one sealed group I have **no value at all** for. It was
priority three on my list and I am returning nothing on it. The brief's own framing, that
everything in section 14 "is PROVISIONAL and none of it has ever been checked from outside" , 
is precisely why this file needed to be in the brief rather than referenced by path.

What I could check in that neighbourhood, I did: the 14.5 gross-versus-net hedging identity
holds exactly. At the break-even rate the hedged share is 1.000000 on all 91 grid points I
tested, confirming that the published loss must be grossed up by `0.0708 x surplus` before any
hedge ratio is taken.

---

## What the brief got right, since round one's verdict was about disclosure

Worth recording, because most of v2's additions worked:

- **tau_k is fully reproducible.** The grid corners 0.03245 and 0.20351 and the operative
  0.070779 all match exactly. The expensing argument and the tau_normal = 0.05 choice are now
  stated with statute and citation, and the headline fiscal condition **fails**, including the
  clause that it does not fail against the top of the sourced literature range.
- **tau_l rebuilds from raw FRED**, 0.300914 and 0.318198 against 0.301 and 0.318, once the
  series misnaming in I-8 is corrected.
- **The crosswalk instruction is exact.** 530 ACS SOCP codes, AIOE 476, GPT 524, reproduced on
  the first attempt from the stated OES May 2021 employment-weighted prefix rule.
- **The vacant-unit warning works:** 131.33m occupied against 145.33m with `NP == 0` retained,
  both exact.
- **The under-reporting identity holds on all four books** to three decimals, and the auto
  correction away from MVLOAS lands within 0.4 percent.
- **`debt_to_gdp_start` = 1.214121 to six decimals**, and the 20-year emerging-market baseline
  of 376.7 percent with no displacement confirms the brief's central warning about levels.
- **All eight section 9 plausibility bounds survive.** Zero break-even breaches in my grid,
  against two in round one. Case A maxes at 0.2264 below tau_l; case B maxes at 0.5354 below 1.
- **The second round's ratio results reproduce exactly**, 648 combinations,
  `demand_event_first_share` 0.740741 = 20/27, factor-of-nine spread, and the variance
  decomposition identifies the two MPCs as 94 percent of the spread.
- **The GSE waterfall is unambiguous** and gives a clean result: CRT plus PMI (592.9bn) absorbs
  the entire agency loss at both LGD ends, so Enterprise capital plus PPNR (224.7bn) is never
  reached and the federal layer is zero.

The remaining defects are concentrated in exactly the four sections that produced nothing in
round one and have therefore never been checked from outside, 5, 7, 10, 11, plus 14, which
the brief itself flags as provisional. That is the pattern one would expect, and it is an
argument for a round three rather than against this one.

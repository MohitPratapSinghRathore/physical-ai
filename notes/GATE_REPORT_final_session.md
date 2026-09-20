# GATE REPORT, final analysis session, 2026-09-20

Covers items 1 to 6. Plausibility violations first, then thesis-weakening results, then the
cleared set with replicated, standing and scenario separated.

---

## PART 1. PLAUSIBILITY VIOLATIONS

### 1.1 A rate of 4.39, in the construction behind the headline dose. FOUND BY THE REPLICATOR, FROM THE FORMULA ALONE

`rho` is a reemployment rate and must lie in [0, 1]. The section 3a fixed-point construction
has a pole at an employment dose of **0.676142**, and past it the closed form returns values
outside [0, 1]. The audit carried no bound on rho.

**Worse than reported.** Our code never printed 4.39, because it used a damped iteration with
`np.clip(rho, 0, 0.999)` inside the loop. Past the pole the iteration walks into the clip and
settles at **rho = 0**, which was then published as a solution. The proof is
`embodied_top50` at a wage-bill dose of 0.3366: published rho exactly 0.0000 and published
terminal loss 1,035.5bn, which is exactly the top of the band the bounded treatment now
reports. **The bound was being enforced accidentally by a numerical device, and the boundary
it produced was reported as an estimate.** A printed 4.39 would have been visible. A silently
clipped boundary was not.

**Status: FIXED.** `src/rho_bounded.py` clamps rho to [0, 1] as an enforced bound, accepts a
point estimate only inside the observed rho range [0.49, 0.74], and reports the band
[0, 0.49] labelled outside the data elsewhere. **The audit goes from 43 checks to 53.**
Violations stay at 4, all of them the superseded rows deliberately retained. The raw fixed
point breaches [0, 1] in 6 of 101 scenario-axis rows and 2 of 13 dose-grid rows, all caught.

**This is the second time a bound found what a tolerance could not, and the second time it
came from outside with no code access.**

### 1.2 Holder shares summing to 100.1. CONFIRMED, and the replicator's proposed fix is also wrong

Section 10d's four mortgage holder shares sum to 100.1. Every share is rounded correctly to
one decimal; the three sourced shares round up together (75.1221 to 75.2) and the residual
also rounds up (24.8779 to 24.9). The replicator proposed 24.8, which would make the rounded
shares sum to 100.0 but would state the residual wrongly.

**Status: FIXED.** Published to two decimals, 51.10 / 12.57 / 11.45 / 24.88, summing to
exactly 100.00. Presentation defect only; the engine always used exact shares and no
downstream number moves.

### 1.3 No further violations

The bounded extended axis, the bounded scenario axis and the bounded dose grid all pass
`rho in [0, 1]`. All eight break-even bounds hold. The rebuilt GSE waterfall respects every
subset bound: no class loss exceeds its class UPB, no cover exceeds its risk in force, no
transfer exceeds the loss.

---

## PART 2. THESIS-WEAKENING RESULTS, reported first as the rule requires

### 2.1 The sovereign share depends on a convention as much as on measurement

The sovereign share is robust to **every measurement call at under 1.3 percent**, including
the entire Treasury definitional question that drove 83.7 percent of the replication gap. It
is **not** robust to four structural calls:

| call | sovereign union | move |
|---|---|---|
| **central** | **0.7936** | |
| **the one-step rule**: business classes take the indirect share | **0.4517** | **-43 pct** |
| obligor leg excluded (held or guaranteed only) | 0.3215 | -59 pct |
| agency pools not federal | 0.5865 | -26 pct |
| commercial mortgage treated as rent-serviced | 0.7408 | -6.6 pct |

**The paper's central object is a robust measurement under a stated accounting convention,
and the convention does the heavy lifting.** Both halves must appear wherever the number
appears. This is weakening and it goes in the abstract, not a footnote.

### 2.2 The 25 and 50 percent doses lose their point estimates

At 50 percent **no exposure type** has a reemployment rate inside the observed data, and the
embodied group has no admissible fixed point at all. At 25 percent the two cognitive types
survive and the embodied type does not. **672 of 2,520 extended-axis cells, 26.7 percent,
lose their point estimate.**

The one consolation is that the direction is not systematically against us: the old point
lies inside the new band in 568 of 672 cases. Where it does not, the old value was the
boundary, so the superseded embodied figures at large doses **overstated** the fiscal loss.

**Any sentence of the form "at a 50 percent dose the reemployment rate is X" is withdrawn.
There is no such X.**

### 2.3 The published agency-mortgage figure does not stand as published

"29.7 percent of GSE net worth at a 25 percent cognitive dose" was a **gross** loss over net
worth, struck before any risk transfer. The waterfall never touched it. Rebuilt loan class by
loan class from the 2025 Form 10-Ks, the **retained** agency loss at that dose is **11.9 to
29.2 percent** of Enterprise net worth. The old point figure is the top of a range that
reaches down to about 12 percent, and it is now a retained loss rather than a gross one.

Three input errors were found, two of them errors of fact rather than of formula:

- CRT risk in force of 210.0bn was the FHFA **cumulative since 2013** figure. Outstanding
  risk in force on the current books is **79.0bn**.
- The PMI-covered share of the book is **21 to 22 percent**, not 6 percent. The 6 percent is
  risk in force over the book, which is covered share times coverage depth. (The replicator
  made this error; verifying it rather than taking it on trust was the right instruction.)
- **39 to 53 percent of each single-family book carries no credit enhancement at all.**

### 2.4 Five headline numbers are removed outright

See Part 4. The incidence count-robustness claim, the 50 percent reemployment rate, the
hedge ratio at the operative tau_k, the bottom-quintile labour-backed ratio, and the two
cognitive index scores. Three of the five are removed because the brief under-specified
something, not because the arithmetic failed.

### 2.5 The blind was procedural, not enforced

The replicator worked on the same machine. The sealed file was reachable at a path the brief
names and was reported unopened until the rebuild was final. The supporting evidence is
internal and circumstantial and is set out in `notes/item5_corrections.md`. **The correct
claim is "independently rebuilt under a reported blind protocol", not "independently
verified".**

---

## PART 3. RESULTS THAT STRENGTHENED

1. **The Treasury level is correct.** Two Z.1 series summed, FL313161105 marketable
   30,069.6bn plus FL313169205 nonmarketable 3,817.5bn = 33,887.1bn, reproducing the sealed
   level exactly, and sitting correctly between Treasury's gross federal debt (37,144.3bn) and
   debt held by the public (29,769.5bn). The documentation was wrong, not the number.
2. **The agreed sovereign share.** 0.778 to 0.804, centred on 0.794, containing our figure,
   the replicator's independent 0.777810, and every measurement variant. Width 0.026.
3. **Two invariances.** Whether the central bank counts as federal moves the share by
   **exactly zero**, because Fed Treasury holdings enter the held leg and the overlap
   equally. And a 30 percent spread in the Treasury level moves the share by under 0.01.
4. **The federal share of first-round losses reproduces by dose.** The replicator's 0.78 at
   10 percent rising to 0.90 at 50 percent sits inside our narrow-reading range at both ends.
   The largest unexplained gap in round two is closed: it was the sweep, as they diagnosed.
5. **The federal `beyond` layer is zero for a real reason now.** 179.4bn of capital against a
   maximum retained first-round loss of 109.0bn, on the statutory negative-net-worth trigger
   rather than the looser one we had been using.
6. **The AI-leg federal share is stable** at 0.0095 to 0.0102 across a threefold variation in
   the assumed AI equity scale.

---

## PART 4. THE CLEARED SET

`data/release/headline_clearing_pass.csv`. Twenty-nine candidates: **9 REPLICATED, 10
STANDING, 5 SCENARIO, 5 REMOVED.** Headline set size **24**.

### REPLICATED, 9. Rebuilt from raw data and the brief alone, inside tolerance

| section | claim | value |
|---|---|---|
| 5 | Retained wage share R in 2026 | 0.568316 |
| 5 | Sourced effective capital tax rate, low | 0.03245 |
| 5 | Sourced effective capital tax rate, high | 0.20351 |
| 5 | Debt to GDP, start | 1.214121 |
| 5 | Federal share of the student loan book | 0.972808 |
| 9 | Emerging market 20-year baseline debt path | 376.74 pct |
| 3 | The four survey under-reporting factors | 4 factors |
| 7 | Terminal-year fiscal loss at the 10 percent dose | 85.168bn |
| 7 | The demand event is 0.7407 of the first round | 0.740741 |

### STANDING, 10. Measured, uncontradicted, not independently rebuilt

| section | claim | value |
|---|---|---|
| 4 | **The state holds 0.794 of the wage leg**, agreed range 0.778 to 0.804 | 0.794 |
| 1 | **The holder gap** | 0.784 |
| 5 | The fiscal condition fails at the operative tau_k | false |
| 5 | Required capital tax rate, above the operative 0.0708, below the sourced top | 0.110 to 0.137 |
| 4 | Home mortgage labour backing | 0.840223 |
| 4 | Multifamily mortgage labour backing | 0.72754 |
| 4 | Direct labour backing ratio | 0.270271 |
| 7 | Federal share of first-round losses, by dose | 0.785 to 0.925 |
| 9 | Retained agency loss at the 10 percent dose | 3.3 to 12.5 pct of net worth |
| 9 | Treasury draw on the agency book | 0 at every dose |

Note: the two mortgage backing shares matched the sealed values **exactly** in round two but
are tagged STANDING rather than REPLICATED because the sovereign union they feed missed by
1.99 percent against a 0.01 absolute tolerance. The scoreboard is honest about that.

### SCENARIO, 5. Arithmetic given a chosen assumption

| section | claim | value |
|---|---|---|
| 8 | The state holds 0.010 of the AI leg | 0.0095 to 0.0102 |
| 7 | Terminal-year fiscal loss at the 25 percent dose | 301.89bn |
| 7 | Second-round bank losses | 173 to 1,565bn |
| 9 | Break-even capital tax rate, case A | 0.125 to 0.301 |
| 9 | Break-even capital tax rate, case B | 0.182 to 0.650 |

### REMOVED, 5. None of the three

| claim | why |
|---|---|
| Incidence moves household counts by 5 to 9 percent | not reproducible; the replicator's natural reading of case (c) gives 59 percent, which removes the robustness the claim rests on |
| The reemployment rate at the 50 percent dose | **there is no such number** |
| Share of the federal wage loss hedged at the operative tau_k, 0.36 | the input `surplus` is undefined in the brief |
| Bottom-quintile labour-backed claims per wage dollar, 4.1489 | the replicator's rebuild lands 2.5 to 3.4 times away; the universe and normalisation are defined nowhere. Q5 survives, Q1 does not |
| The two cognitive index scores by occupation | eleven mismatches running in opposite directions on the two indices; the wage machinery passes its controls, the index scores are unsettled |

---

## PART 5. STATED LIMITATIONS, one paragraph each, no further work

`data/release/stated_limitations.csv`.

**L1. Off-balance-sheet and GPU-backed AI financing is unmeasured.** The AI leg is built from
nine SEC registrants' us-gaap facts, on-balance-sheet Tier 2 only. BIS QR March 2026
identifies off-balance-sheet SPV structures as dominant in data centre financing and none
appear in these filings; GPU-backed lending and data centre ABS and CMBS are likewise absent.
Every AI-leg level is a labelled lower bound and every federal share of the AI leg is
correspondingly an upper bound. The project brief's 5 percent kill criterion is not evaluable
until Tier 1 and Tier 2b exist. We do not know the sign of the error on the holder gap, only
that the gap is measured against a leg we can bound from below alone.

**L2. Capital gains receipts are unsourced.** The labour-linked share of federal receipts
splits the individual income tax using the SOI wage share of AGI, available for 2021 to 2023
only. Realised capital gains sit inside AGI and inside that tax and we do not separate them,
so 0.657788 overstates the labour share in years with large realisations and understates it in
years without. The 77.7 percent upper bound is carried throughout and moves the sovereign
share by 0.71 percent, so the headline is insensitive to it. The fiscal magnitudes are more
sensitive and we have not bounded that.

**L3. The labour backing ratio's novelty is "none located", pending a systematic search.**
The claim that no published work constructs a labour backing ratio over the whole claim
structure rests on a non-systematic search. A PRISMA-protocol search for this specific
question, with databases, query strings, dates and counts at each stage, has not been run and
is stated as future work. The related-work audit already located prior work on the fiscal
mechanism and that priority claim was retired; the same could happen here.

**L4. The holder proxy residual.** The mortgage holder split reads three of four shares from a
publisher and takes the fourth, 24.88 percent or 3,259bn, as the arithmetic remainder,
treated as private in full. That is the conservative choice for the sovereign claim, because
any federal fraction inside it would raise the federal share. We have not identified what is
in it. The same structure appears on the AI leg, where a residual_unallocated class carries
1.6 percent of the wage leg and 9.8 percent of the AI leg.

**L5. Effective labour tax rates by income are not taken from CBO.** tau_l is a single
economy-wide effective rate, built bottom-up as federal taxes over FRED WASCUR, with a
top-down alternative alongside. It does not vary by position in the wage distribution. CBO
publishes effective federal tax rates by income group and we have not used them. Because
displacement is not uniform across the wage distribution, and the incidence section shows it
concentrated away from the top, a flat rate probably overstates the revenue loss from
displacing low-wage workers and understates it from displacing high-wage workers. We have not
signed or bounded the net effect.

---

## PART 6. ONE BLOCKER, reported not worked around

**Item 9 cannot be completed as specified.** The RAND report (Price and Suresh 2026) and IMF
Note 2026/002 (Barhoumi and others) are **not in `data/raw/manual/`**, and a search of the
whole machine finds neither. The most recent file placed in that directory is
`NYFed_HHDC_2026Q2_data.xlsx`.

Everything in item 9 that does not require those two documents has been done: the Manning
correction, the Korinek and Lockwood superseded title, and the CBO 2024 addition. The
related-work table carries RAND and the IMF note at the verification level the previous audit
established, with the boundary **explicitly marked as not yet redrawn from the full text**.
No reading of either document is asserted that is not already sourced in
`lit/related_work_labour_backing.md`. Place the two files and the boundary can be redrawn in
one pass.

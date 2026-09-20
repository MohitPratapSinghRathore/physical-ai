# Item 5. Corrections, recorded as notes only. No further replication round.

Five corrections the replicator found by rebuilding rather than by reading, plus the method
record. Each is verified here against the project's own files before being accepted.

---

## 5.1 The `condition_passes` note contradicts the brief and the arithmetic

**Verified. The replicator is right, and the note overstates the finding.**

The sealed note reads:

> "required tau_k exceeds the top of the sourced range at every reading of tau_l"

Our own `data/processed/replication_r_sensitivity.json` says the opposite, in every one of
its five cells:

| reading | required tau_k, max over tau_l | `condition_passes_at_top_of_sourced_range` |
|---|---|---|
| ours, observed rho and our omega | **0.137276** | **true** |
| their fitted rho, our omega | 0.124432 | true |
| our fitted rho, our omega | 0.127395 | true |
| ours, observed rho, their omega | 0.128822 | true |
| their fitted rho, their omega | 0.115377 | true |

The required rate maxes at **0.137276** against a sourced top of **0.20351**. It does not
exceed it anywhere. The boolean `false` is correct and the note attached to it is false.

**The correct note, which is also what section 2d of the brief already says and insists must
travel with the result:**

> The required capital tax rate of 0.110 to 0.137 exceeds the OPERATIVE effective rate of
> 0.0708 under every reading, and does not exceed the top of the sourced range of 0.20351
> under any reading. The condition is unclosable under the tax code AS IT STANDS, not under
> every reading of the corporate tax literature.

The note is corrected in `src/seal.py` and in the brief. This is the same weakening already
recorded against claim 168 in A96 to A100; the sealed note had not been brought into line
with it.

---

## 5.2 The part-time wage parameter is 0.3206, not 0.50

**Verified. The prose was wrong; the code was always right.**

`src/omega_blended.py` line 17 and its 2025 block: part-time median usual weekly earnings of
**386** dollars over full-time **1,204** dollars = **0.3206** (2024: 380 / 1,159 = 0.3279).
That is a sourced BLS ratio of medians. The brief's section 2a assigns part time **0.50**,
which is an assumption, not a measurement, and it does not reproduce the brief's own omega.

The replicator reported both before opening the sealed file and the sealed R confirms 0.3206
is what the code uses. `fiscal.R_2026` reproduces at 0.568315 against 0.568316.

**Corrected in the brief.** The prose parameter is replaced by the sourced ratio with the
series named.

---

## 5.3 The mortgage holder shares sum to 100.1, and the replicator's proposed fix is also wrong

**Verified as a defect. The replicator's stated remainder of 24.8 is not right either.**

Section 10d publishes four shares of a 13,100bn book:

| holder | published | exact |
|---|---|---|
| GSE (agency) | 51.1 pct | 6,694 / 13,100 = **51.0992** |
| FHA | 12.6 pct | 1,647 / 13,100 = **12.5725** |
| bank portfolio | 11.5 pct | 1,500 / 13,100 = **11.4504** |
| residual | 24.9 pct | 3,259 / 13,100 = **24.8779** |
| **sum** | **100.1** | **100.0000** |

Every share is rounded correctly to one decimal. The three sourced shares round UP together
(75.1221 to 75.2) and the residual also rounds up (24.8779 to 24.9), so four correct
roundings produce a sum of 100.1. The replicator's proposed remainder of 24.8 would make the
rounded shares sum to 100.0 but would state the residual incorrectly: the residual is
24.878 percent, which rounds to 24.9.

**Correction adopted: publish the shares to two decimals, 51.10 / 12.57 / 11.45 / 24.88,
which sum to exactly 100.00.** The plausibility bound "holder shares must sum to 1" then
holds as published rather than only as computed.

This was the replicator's one stated bound breach. It was a presentation defect, not an
arithmetic one, and no downstream number moves: the engine has always used the exact shares.

---

## 5.4 Appendix A leaks the section 1 sealed coefficients

**Verified.** Appendix A of `notes/replication_brief_v2.md` prints, under "The full
coefficients":

| window | specification | intercept | slope |
|---|---|---|---|
| full | prime-age nonemployment | **1.22798** | **-0.02749** |
| full | unemployment rate | 0.80901 | -0.03043 |
| post-2008 | prime-age nonemployment | 1.17818 | -0.02541 |
| post-2008 | unemployment rate | 0.77942 | -0.02784 |

The first row is the fit the section 1 sealed block also holds, so the brief hands a
replicator three sealed values in advance. The replicator raised this before opening the
sealed file, declined to adopt the two DWS vintage values that would have reproduced them,
and reported their own unverified fit instead. **The blind held because the replicator
protected it, not because the brief did.**

**Correction: the coefficient table is removed from Appendix A.** Appendix A's argument does
not need it. The argument is that the unemployment rate fits better on both windows
(R squared 0.81191 against 0.77333 on the full sample, 0.93993 against 0.73199 post-2008) and
that the preference for prime-age nonemployment therefore rests on mechanism alone. The R
squared comparison makes that point without publishing the coefficients. **The fourteen DWS
y values are published instead**, so a replicator can fit it themselves, which is what the
replicator asked for.

---

## 5.5 The nine SEC filers behind the AI-leg holder shares, named

**The brief never named them. This was insufficiency I-11 and it made the entire
`two_sided_bet` block unattemptable.** They are, from `data/processed/legA_tier2.csv`:

| ticker | company | class | fiscal year end | capex bn | OCF bn | self-funding ratio |
|---|---|---|---|---|---|---|
| AMZN | Amazon.com Inc | hyperscaler | 2025-12-31 | 131.819 | 139.514 | 1.058 |
| MSFT | Microsoft Corp | hyperscaler | 2026-06-30 | 115.948 | 182.935 | 1.578 |
| GOOGL | Alphabet Inc | hyperscaler | 2025-12-31 | 91.447 | 164.713 | 1.801 |
| META | Meta Platforms Inc | hyperscaler | 2025-12-31 | 69.691 | 115.800 | 1.662 |
| ORCL | Oracle Corp | hyperscaler | 2026-05-31 | 55.663 | 31.977 | **0.574** |
| CRWV | CoreWeave Inc | neocloud | 2025-12-31 | 10.309 | 3.058 | **0.297** |
| TSLA | Tesla Inc | robotics | 2025-12-31 | 8.527 | 14.747 | 1.729 |
| EQIX | Equinix Inc | data centre REIT | 2025-12-31 | 4.311 | 3.911 | **0.907** |
| DLR | Digital Realty Trust Inc | data centre REIT | 2025-12-31 | 3.181 | 2.412 | **0.758** |

**The selection rule, also never stated:** US SEC registrants filing us-gaap XBRL facts, in
four classes chosen to span the AI capital stack, hyperscaler, neocloud, robotics and data
centre REIT. A tenth candidate, **NBIS (Nebius Group NV)**, is in the table with no data: it
is a foreign private issuer and files no us-gaap company facts, so it is carried as a named
exclusion rather than dropped silently.

Totals: capex **490.9bn**, operating cash flow **659.1bn**, aggregate self-funding ratio
**1.3426**, capex in excess of operating cash flow **32.1bn**, debt-financed share of capex
**6.54 percent**. Four companies spend more than they earn: ORCL, CRWV, DLR, EQIX.

The limitation stands and is unchanged: **this is on-balance-sheet Tier 2 only.** The
off-balance-sheet SPV structures are not in any of these filings, so every AI-leg figure is a
labelled lower bound.

---

## 5.6 Method record: the blind was procedural, on one machine

To be recorded in the method notes and in the paper's method section, without gloss:

> **The second replication round was blind by protocol, not by isolation.** The replicator
> worked on the same machine as the project. The sealed file
> `notes/sealed/sealed_expected_values_round2.json` was reachable at a path the brief itself
> names, and was not attached to the request. The replicator reports opening it, and only it
> together with `SEALED_README.md`, after all 127 values had been written to
> `replication_results_round2.csv` and `brief_insufficiencies_round2.md`, and reports reading
> no project code at any point in either round.
>
> **That is a reported protocol, not an enforced one, and it is stated as such.** The
> supporting evidence is internal and circumstantial: eleven of the twelve insufficiencies
> were written before the file was opened and four of the six mismatch root causes were among
> them; the replicator declined to adopt the two DWS vintage values that would have
> reproduced the three coefficients Appendix A leaked, and reported a worse unverified fit
> instead; and one error in their own code was found and amended only on scoring, which a
> reconstruction after the fact would not produce.
>
> A future round should be run with the sealed file absent from the filesystem rather than
> merely unreferenced. **The correct claim for the paper is "independently rebuilt under a
> reported blind protocol", not "independently verified".**

# The two-sided bet: one-page claims summary

For a prospective co-author. Status as of 2026-09-20. Source of truth for every tag:
`data/release/headline_clearing_pass.csv`.

**Tags. [R] REPLICATED**: rebuilt by an instance that did not write the code, from raw data
and a published brief alone, inside our stated tolerance. **[M] STANDING**: measured, clears
every applicable check, not independently rebuilt. **[S] SCENARIO**: arithmetic conditional
on a chosen assumption.

---

## The central finding

> **The state holds about four fifths of the wage leg and about one percent of the AI leg.**
>
> Sovereign share of labour-backed claims **0.794** (agreed range **0.778 to 0.804**) **[M]**.
> Federal share of the AI leg **0.010** (range 0.0095 to 0.0102) **[S]**. **The gap is
> 0.784.**

The financial system holds two exposures resting on opposite assumptions about labour. The
state is the residual holder of the one that fails if AI succeeds, and holds almost none of
the one that pays if it does. **It is not hedged.**

**The honest qualification, which belongs in the same breath.** The share is robust to every
*measurement* call at under 1.3 percent, including the entire Treasury-definition question.
It is **not** robust to the one-step accounting rule, which moves it to **0.452**. It is a
robust measurement under a stated convention, and the convention does heavy lifting.

**What this paper claims, exactly and no more.** The fiscal mechanism is established
literature and we do not claim it. **IMF Note 2026/002 asserts the wage-leg credit mechanism
and the distributional asymmetry; RAND measures the federal revenue exposure.** Our
contribution is five measured things: **the measured holder structure; household losses from
microdata mapped to the Federal Reserve's loss rates; incidence by who bears the loss; a
replicated fiscal condition with sourced parameters; and the public claims register.**

---

## Six supporting results

| # | Result | Status |
|---|---|---|
| 1 | **The sovereign share nearly doubles while the ratio stays flat.** Sovereign union share rises from **0.336 in 1970 to 0.794 in 2025**; the direct labour backing ratio moves between 0.267 and 0.376 with no trend. The quantity of wage-backed claims has barely changed; **who holds them has changed completely** | **[M]** |
| 2 | **The fiscal condition is a FUNCTION of the capital tax rate, with a threshold at 0.110 to 0.137.** Retained wage share **R = 0.568316**. It **fails at 0.0708**, the operative rate on the AI surplus after 168(k) expensing and profit shifting, and **passes at 0.20 to 0.22**, the IMF's measured economy-wide capital rate. **Closing it needs 26 to 52 percent of the AI surplus taxed at the economy-wide rate.** The old claim that it is "unclosable under the tax code as it stands" is WITHDRAWN and replaced by "as the code applies to AI capital specifically" | **[R]** on R and the boolean; **PROVISIONAL** on the verdict, which depends on the tax base chosen |
| 3 | **The federal government bears roughly four fifths of first-round losses, and the share depends on the dose.** Narrow reading: **0.785 to 0.870 at a 10 percent dose**, rising to 0.855 to 0.925 at 50 percent, then falling back at 75 percent. Conservatorship reading is 8 to 10 points higher | **[M]**; the independent rebuild's 0.78 rising to 0.90 sits inside our range at both ends |
| 4 | **The housing agencies absorb a wage shock without reaching the Treasury.** Rebuilt from the 2025 Form 10-Ks: **39 to 53 percent of each single-family book carries no credit enhancement**; private cover transfers only **11 to 15 percent** of an agency loss at small doses; **zero Treasury draw at every dose from 5 to 75 percent** (179.4bn of capital against a maximum retained first-round loss of 109.0bn). **First round only, house prices fixed** | **[M]** |
| 5 | **The second round is nine tenths of the bank channel.** The demand event is **0.740741** of the first round, factorising exactly 20/27; second-round bank losses span a factor of nine, **173bn to 1,565bn** | **[R]** on the share; **[S]** on the levels |
| 6 | **The measurement has a hard boundary, and it is a finding.** The reemployment rate is a fixed point with a **pole at a 45.9 percent embodied wage-bill dose**. A point estimate exists only inside the observed range of rho, [0.49, 0.74]. **At a 50 percent dose no exposure type has one.** Past that boundary this data cannot say what happens | **[M]** |

---

## What has been independently replicated

Two rounds, the second scoring **127 quantities**, 79 with sealed counterparts, **45 within 5
percent and 28 inside our own tolerance**, by an instance that read no project code.

**Reproduced exactly or near-exactly:** `R_2026` 0.568315 against 0.568316; both sourced
capital tax rates; debt to GDP start 1.214121 to six decimals; the emerging-market 20-year
baseline 376.74 percent; the federal student share 0.972808; the demand event share 0.740741;
all four under-reporting factors and coverage shares; the terminal fiscal loss at the 10
percent dose to 0.19 percent; and **home mortgage and multifamily labour backing to the last
published digit, rebuilt independently from ACS mortgage service and gross rent**.

**Near miss on the central object.** The sovereign union share: ours 0.793592, theirs
0.777810, a 1.99 percent gap that decomposes to 83.7 percent the Treasury class (they could
not know it was two Z.1 series summed), 6.6 percent a class they omitted, and the remainder
household balances.

**The protocol, stated plainly.** The blind was **procedural, not enforced**. The replicator
worked on the same machine; the sealed file was reachable at a path the brief itself names,
was not attached to the request, and is reported unopened until the rebuild was final. The
supporting evidence is internal and circumstantial: eleven of twelve insufficiencies were
written before opening, four of six mismatch root causes were among them, and they declined to
use three sealed coefficients the brief had leaked. **The claim is "independently rebuilt
under a reported blind protocol", not "independently verified."**

**Independent external corroboration, from a different direction.** RAND (Price and Suresh
2026) put **66 percent** of federal revenue as directly labour-derived; we get **63.4
percent** from a bottom-up SOI construction. They conclude corporate tax rates would need to
be "roughly doubled"; we get **1.55 to 1.94 times** the operative rate. Neither saw the other.

---

## What was withdrawn

| withdrawn | why |
|---|---|
| **The 50 percent reemployment rate** | There is no such number. Past the pole the construction has no admissible solution; the superseded code clipped it to zero and published the boundary as an estimate |
| **"Incidence moves household counts by 5 to 9 percent, so counts are robust to it"** | Not reproducible. The natural alternative reading of one case gives 59 percent, which removes the robustness the claim rested on |
| **The bottom-quintile labour-backed ratio, 4.15** | The independent rebuild lands 2.5 to 3.4 times away and we cannot show their reading is wrong, because we never defined the object's universe. **The gradient survives; the magnitude does not** |
| **The hedge ratio at the operative tax rate, 0.36** | Its input, `surplus`, is undefined in our own brief |
| **The two cognitive index scores by occupation** | Eleven mismatches running in opposite directions on the two indices. The wage machinery passes its controls; the index scores are unsettled |
| **"29.7 percent of GSE net worth"** | It was a gross loss struck before any risk transfer. Replaced by a retained loss of 11.9 to 29.2 percent at the same dose |
| **"The fiscal condition fails under current law"** | **WITHDRAWN this pass.** It fails under current law *as it applies to AI capital specifically*, at 0.0708. At the IMF's measured economy-wide capital rate of 0.20 to 0.22 it passes. The condition is a function of tau_k, not a verdict |
| **"No reading of the corporate tax literature makes the break-even rate available"** | False. It is inside the sourced range in 10 of 15 cells. Narrowed to a statement about the operative rate |
| **"Occupational diversification does not hedge a mortgage book"** | Overreach. A flat distribution does not stop an individual lender selecting low-exposure borrowers |
| **Priority on the fiscal mechanism** | RAND, Casas and Torres, Korinek and Lockwood, Windfall and the IMF all have it. **We did not discover it and must not imply that we did** |
| **The trigger dashboard as a contribution** | An indicator list is not a research contribution. It stays as an artifact |

---

## Known limitations

1. **Off-balance-sheet and GPU-backed AI financing is unmeasured.** The AI leg is nine SEC
   registrants' on-balance-sheet facts. BIS identifies SPV structures as dominant and none
   appear. **Every AI-leg level is a lower bound and the state's share of it an upper bound.**
2. **Capital gains receipts are unsourced.** The labour-linked receipts share does not
   separate realised gains inside AGI. The headline is insensitive to it (0.71 percent); the
   fiscal magnitudes are more sensitive and we have not bounded that.
3. **The labour backing ratio's novelty is "none located", not "none exists."** No systematic
   PRISMA search has been run for that specific question. We have already retired one
   priority claim after a non-systematic search found prior work.
4. **The holder proxy residual.** 24.88 percent of the mortgage book, 3,259bn, is an
   arithmetic remainder treated as private in full. Conservative for our claim, but
   unidentified.
5. **Effective labour tax rates by income are not from CBO.** A single economy-wide rate,
   flat across the wage distribution. We have not signed or bounded the net effect.
6. **First round only, house prices fixed.** Every credit loss is a floor, not an estimate.
7. **The replication blind was procedural, not enforced.** The replicator worked on the same
   machine with the sealed file reachable at a path the brief names. The claim is
   "independently rebuilt under a reported blind protocol", not "independently verified".
8. **The capital tax base is contested and the fiscal verdict turns on it.** The condition
   fails at our 0.0708 and passes at the IMF's measured 0.20 to 0.22. Both are correctly
   computed on different bases. This is limitation and open question at once, and it is the
   first thing a public finance co-author should attack.

---

## Where the work stands

The pipeline rebuilds from raw data in one command. Two replication rounds are complete with
127 scored quantities. The plausibility audit runs 53 checks with 4 violations, all
deliberately retained superseded rows. The claims register carries every claim with its status
and a separate replication flag. **The measurement is done; the manuscript is not written.**

**THE FIRST QUESTION FOR A PUBLIC FINANCE CO-AUTHOR.** Is 0.0708 the right rate for this
condition, or is it the wrong base? We compute the effective rate on the marginal dollar of US
AI surplus as 0.0708 (21 percent statutory, normal return exempted by 168(k) expensing at a
rent share of 0.351, 48 percent of rents shifted offshore). IMF SDN/2024/002 measures an
economy-wide capital ATR of 0.20 to 0.22 including personal-level taxes on dividends and
gains. Required is 0.110 to 0.137, so the condition fails on ours and passes on theirs. Is the
marginal-on-AI-surplus base right for a revenue replacement question? Is the 48 percent haven
share right for AI rents, which are unusually intangible and so if anything more shiftable?
Full statement in `notes/tau_k_exposure.md`.

**The single most useful thing a co-author could do**: run a systematic PRISMA search on the
labour backing question (limitation 3), and define the two objects the replicator could not
reproduce because we never specified them, B5's universe and `surplus` in the hedging
construction.

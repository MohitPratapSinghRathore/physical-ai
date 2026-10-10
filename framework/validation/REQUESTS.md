# Requests for changes outside framework/validation/

Nothing outside `framework/validation/` and `data/raw/validation/` was written in this
session. Items needing a decision or an edit elsewhere are logged here.

---

## 1. Conflicting instruction about where to commit — resolved conservatively

The session brief says, in its standing header, to commit and push to `validation-pilot`
only and **never merge to master**. Its final line says to "commit with the next A-number,
push master".

**Taken as: commit to `validation-pilot`, push `validation-pilot`, do not touch master.**
The header is specific, repeated and safety-shaped; the final line reads as boilerplate
carried over from the manuscript workflow. Pushing a new workstream's first commit
straight to master would also contradict the brief's own isolation requirement.

The commit is numbered **A138** (next after A137) so it can be replayed onto master later
if the owner wants it there. **If master was in fact intended, say so and it is a
fast-forward away** — nothing needs rebuilding.

## 2. No change requested to the labour backing accounts

`framework/labor_backing/claim_class_rules.csv` was read only. No edit is requested.

For the record, one observation that the owner may want to act on in that workstream, not
this one: because every household class coefficient sits in 0.727–0.883 and every business
class is 0.0, the coefficient vector is close to binary. Any *bank-level* or *portfolio-level*
construct built from it will be close to a relabelling of the household share of the book
(measured: R² = 0.899 on loan-composition shares alone, 6,637 banks, 2014Q2). That is a
property of the accounts as designed — the one-step rule does it deliberately — and it is
fine for the descriptive aggregate. It is a real limit on any attempt to turn the accounts
into a cross-sectional risk measure, which is what this workstream is testing.

**No action requested.** Recorded so that it is not rediscovered later as a surprise.

## 3. Claims register — nothing to add yet

No claim is proposed for the register from this session. The pre-registration makes
predictions; it establishes nothing. If session 2 produces a result meeting or failing the
§8 criteria, that is when a register entry becomes appropriate, and the null wording in
PREREGISTRATION.md §11 is the text to use.

---

## 4. Amendment 1: the repo's ACS is post-shock, so a 2013 vintage was downloaded

**Logged because it departs from an instruction, and the owner may want to overrule it.**

Amendment 1 was told to build the debtor-specific wage shares "from the ACS microdata
already in the repo (pre-shock vintage only, 2013 or the 2009 to 2013 five-year file)".
Those two conditions cannot both hold. `data/SOURCES.md` records the repo's ACS as **PUMS
2023 1-year** (`data/raw/pums/csv_pus.zip`, `csv_hus.zip`, retrieved 2026-09-19), which is
*post-shock* for every candidate episode — 2014–2016, and 2020.

Taken as: **the pre-shock requirement governs**, because using a 2023 survey to
characterise the debtors who were exposed to a 2014 shock would contaminate the construct
with everything that happened in between, and the whole session is built on not doing
that. The ACS 2009–2013 5-year PUMS was downloaded to
`data/raw/validation/pums2013/` (3.3 GB, gitignored like the rest of `data/raw/`).

**No file in `data/raw/pums/` was read or modified.**

If the owner intended the 2023 file to be used anyway, say so and the build is a
one-parameter change — but the resulting construct should not then be described as
pre-shock.

## 5. A note for the labour backing workstream, not a request

Amendment 1's measured result refines item 2 above and is worth recording there eventually.
The near-binary coefficient vector limits any *portfolio-level* construct, as noted — but
the limit is not total. Matching the coefficients to **debtor-specific** local wage shares,
rather than to a population-wide one, roughly doubles the accounts' distinctive content
(6.1 to 11.2 percent of bank-level variance). The reason is visible in one number: the wage
dependence of a county's mortgage holders correlates only **0.332** with the wage
dependence of the county as a whole.

That suggests the accounts' household cells carry information that aggregate wage shares do
not, which is a point in their favour and is independent of whether the pilot's predictive
test succeeds. **No action requested**; recorded so the finding is not lost if the pilot
returns a null.

---

## 6. Commit numbering on this branch collides with master — fixed here, flagged for the owner

**The collision is real and already happened.** This branch's first two commits were
labelled A138 and A139, following the A-sequence as the standing convention asks. But
master independently advanced to **A138 ("revision round 2, jurisdiction consistency,
backing basis and the boundary", `0b5f2b8`)** while this branch was being built. There are
now two different A138 commits in the same repository.

**Fixed from Amendment 2 onward: this branch numbers its commits `V1, V2, V3, …`.** The
mapping to what already exists:

| This branch | Commit | Was labelled | Subject |
|---|---|---|---|
| V1 | `bc52916` | A138 | validation pilot, feasibility and pre-registration |
| V2 | `8a91fa2` | A139 | pre-registration Amendment 1, debtor-specific construct |
| V3 | this commit | — | pre-registration Amendment 2, Gap form and calibration test |

The two existing commit messages are **not** rewritten. Rewriting them would change hashes
that have already been pushed and reported, and the pre-registration's whole evidentiary
value rests on those hashes being stable and on the history being append-only. The
mis-numbering is recorded here instead, which is the cheaper and more honest fix.

**For the owner.** If this branch is ever replayed onto master, the V-numbers are placeholders
and the commits should be renumbered into whatever the A-sequence has reached by then.
Nothing downstream depends on the labels.

---

## 7. Engine file verified unchanged; a standing check for the run

Amendment 3 was asked to check whether the household credit engine moved on master since
the hash pinned in Amendment 2. **It did not.**

Master advanced `0b5f2b8` (A138) → `a1b6a0e` (A139, "final manuscript pass, disclosure,
scope, relief demoted, length"), but no commit in that range touches
`data/processed/verify/hand_check_credit.csv`. The git blob and the SHA256 are identical at
both commits. The twelve loss sensitivities in PREREGISTRATION §13.4 stand unaltered.

**No action requested.** Recorded because the check will need repeating: the run re-verifies
that SHA256 at step 7 and records the result, and if it has moved by then the run uses the
**pinned** values, reports the new ones alongside, and states what differs. The pinned
values are not updated without an explicit amendment — that rule is in §14.6.

## 8. A correction to earlier sessions' checksum abbreviations

Three abbreviated SHA256s written in earlier commits on this branch were mistyped in the
prose (the full hashes were always correct where they mattered, and the FHFA file itself
verified byte-for-byte against the owner's handoff at the time). Corrected in this commit:

| File | Was written | Correct |
|---|---|---|
| `hpi_at_county.xlsx` | `534e9fd3…af79afd1` | `534e9fd3…df79afd1` |
| `la.series` | `2b11e414…a97db77a4` | `2b11e414…97db77a4` |
| `la.area` | `7f1dcbd6…04dce1fc45` | `7f1dcbd6…dce1fc45` |

Abbreviations in this document and in SESSION2_PLAN are now generated from the files rather
than typed. **No pinned value used by any test was affected** — the engine hash in §13.4 is
recorded in full and was verified in full.

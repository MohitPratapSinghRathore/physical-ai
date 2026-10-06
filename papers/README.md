# The two companion papers

**Built to the Paper-Writing Playbook. Last updated 2026-10-04.** The original single manuscript
remains untouched in `../paper/` as the archive; nothing here modifies it.

These two papers answer Sriharsha's review of 25.09.2026, which asked for a specific title, for
focus, and for the content to be separated into two objectives.

---

## What they are

| | Paper A | Paper B |
|---|---|---|
| Directory | `accounts/` | `ownership/` |
| Title | Labor Backing Accounts: Who Holds the Claims That Wages Pay? | Ownership, Not Profit Shifting: Why Capital Taxation Cannot Replace Wage Taxes |
| Objective | What income services the US claim stock, and who holds, guarantees or owes it | Whether the tax system can replace wage-tax revenue when income shifts to capital, and what binds |
| Genre | Measurement, national accounts | Public finance |
| Body words | 9,347 | 9,206 |
| Pages (author PDF) | 25 | 23 |
| Figures | 1, 2 | 3, 6 |

Corresponding author on both: **Mohit Pratap Singh Rathore**, first in the author list, on the
manuscript, the title page and the DOCX.

The single manuscript was about 18,700 words with one stated contribution and three supporting
modules. Each paper here is a normal length for a Q1 field journal, and each has one thesis.

**Paper B's thesis is the sharper one.** The same ownership concentration governs three results
usually kept apart: the capital tax reaches little because most corporate claims sit where the
income tax does not; households cannot be made whole by broadened ownership because most equity
is not theirs and what is theirs cannot be spent; and an equity bust transmits weakly because the
assets that fall are held where the propensity to consume is lowest. One fact, three
consequences, and it displaces the profit-shifting explanation on measured evidence.

## Targets, with ratings verified 2026-10-04

Checked against the ABDC list and Scimago rather than asserted. **International Tax and Public
Finance turns out to be ABDC B**, so it has been demoted from the suggested list; the earlier
draft of this file had it as a primary alternate, which was wrong.

| Journal | ABDC | Scimago | Fit |
|---|---|---|---|
| Review of Income and Wealth | listed, rating to confirm | **Q1** Economics and Econometrics, SJR 1.212, h-index 77 | Best genre fit for Paper A |
| Journal of Financial Stability | **A\*** | | Strong for Paper A |
| Journal of Banking and Finance | **A\*** | | Alternate for Paper A |
| National Tax Journal | **A** | | Best fit for Paper B |
| Journal of Public Economics | **A\*** | | Reach for Paper B |
| International Tax and Public Finance | **B** | | Only if the A-list fails |

**Paper A.** There is a genuine trade-off. *Review of Income and Wealth* is the natural home,
because it publishes new national-accounts objects with long series and distributional cuts, and
it is confirmed Q1. *Journal of Financial Stability* is ABDC A\* and so satisfies the playbook's
A/A\* preference outright, and the federal-exposure framing fits its scope. If the ABDC rule is
binding, submit to JFS. If genre fit matters more, RIW.

**Paper B.** *National Tax Journal* (A) is the best fit. *Journal of Public Economics* (A\*) is
the reach and worth one attempt first, since the lever ranking is a genuinely new empirical
claim about a question that journal publishes.

Neither is a top-five paper, and that ceiling is structural: no identification, no model, one
country, descriptive. Splitting does not raise the ceiling. It stops each paper being rejected
for the other one's weaknesses.

## Reference verification

Playbook section 4 requires every reference to be web-verified. The inherited `references.bib`
had not been checked this session, so every entry dated 2025 or later that is actually cited was
verified on 2026-10-04 against the publisher.

Verified and correct: Korinek and Lockwood (NBER WP 34873), Price and Suresh (RAND RR-A4980-1),
Falk and Tsoukalas (arXiv 2603.20617), Barhoumi (IMF Note 2026/002), Cohen, Killen and Lau
(Chicago Fed Insights), Ieong, Saputra, Maniar and Cheng (Windfall Trust), Bank for International
Settlements (BIS Quarterly Review, March 2026). The specific claims attributed to each in the
related-work sections match the sources.

**One entry was wrong on two fields.** `Bayraktar` was recorded as *Emre* Bayraktar, year *2025*.
The author is **Erhan Bayraktar** and the paper is **2026** (arXiv:2605.05127, v1 6 May 2026, v2
31 July 2026, under review at the *Journal of Economic Dynamics and Control*). Both are
corrected, the key is now `Bayraktar2026`, and all citing files were updated. The entry carried a
`verification` field claiming it had already been checked, which is worth knowing: a verification
note is not itself verification.

## What was deliberately left out

Sections 6 and 7 of the original (the conditional displacement stress test and the 8,588
balance-sheet second round) and Section 9's twelve-instrument table are **not** carried into
either paper. That is roughly 3,200 words of body text plus a large share of the appendix, and it
is a lot of completed work, so the reasoning is recorded rather than assumed. The manuscript
already says of that material that the second round is *"the weakest module evidentially"*, that
its relief result *"carries less weight than the incidence results around it"* until a
duration-matched experiment is run, and that *"losses are allocated pro rata by category, so
business mix is the only source of dispersion here"*, which makes the headline dispersion finding
partly true by construction.

Two pieces were rescued rather than dropped:

- the non-monotonic buffer result, thinnest liquid runway in the **second** quintile, is now in
  **Paper A** beside the claims gradient, and the two together make one point;
- the result that exposure type is a pay effect, which reverses once pay is controlled, is in
  **Paper B**'s incidence section.

The remainder is a candidate third paper once the duration-matched experiment exists. It should
be scoped on its own, not salvaged.

## Build

```
make            both papers, all deliverables, then the QA gates
make accounts   paper A only
make ownership  paper B only
make qa         gates only
make clean      remove build artifacts and deliverables
```

Six deliverables per paper: author {PDF, DOCX}, anonymous {PDF, DOCX}, title page {PDF, DOCX}.

Shared assets live in `../paper/` and are referenced by relative path, so `results_macros.tex`,
the figures and the tables have exactly one source of truth. `references.bib` is copied in
because bibtex does not resolve a relative database path reliably on this toolchain; the Makefile
refreshes the copy on every build and it is gitignored.

Helper scripts, reusable across projects: `_qa.py` (playbook section 8 gates plus the section 2.3
AI-tell check), `_anoncheck.py` (identity-leak check on the blind build), `_count.py` (body word
count), `_to_docx.py` (resolves the `\ifanon` toggle, the `\result{}` macros, `\ref`/`\eqref`
from the `.aux` and natbib citations from the `.bbl`, promotes the title and author block that
pandoc would otherwise drop, then hands plain LaTeX to pandoc).

## QA status

Both papers pass every gate: title within twelve words, abstract within 250, zero em-dashes, zero
occurrences of "robust", zero undefined references or citations, zero undefined `\result` macros,
zero AI-tell phrases, limitations paired one-to-one with avenues for further research, and zero
identity leaks in the blind build in both PDF and DOCX.

## Open items for the authors

1. **Affiliation discrepancy.** The playbook records Sriharsha Meduri at Andhra University; the
   manuscript records Oviqo. Both title pages carry Oviqo, as the manuscript did, with the
   discrepancy noted on the page. Needs confirming.
2. **ORCIDs** are marked "to be supplied" on both title pages, and Pratap Chandra Mandal's email
   is not yet filled in.
3. **The AI declaration** now uses the playbook's wording. Its third sentence has been adjusted,
   as playbook section 6 directs ("adjust to the paper's method"), because the standard clause
   says generative AI was not used to *analyse* the data, and for this project the analysis code
   was AI-written. The declaration as it stands says AI was not used to *generate* the data,
   which are public statistical releases, and that no reported value originates in a model's
   assertion. Both statements are true. If you want the standard clause verbatim instead, say so
   and it goes in, but it would not be accurate for this project.
4. **Author order** is inherited from the original manuscript and has not been revisited.
5. **Review of Income and Wealth's ABDC rating** was not pinned down from a primary source; its
   Q1 status is confirmed. Worth checking on the ABDC list directly before choosing between RIW
   and JFS.

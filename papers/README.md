# The two companion papers

**Built to the Paper-Writing Playbook. 2026-10-04.** The original single manuscript remains
untouched in `../paper/` as the archive; nothing here modifies it.

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
| Pages (author PDF) | 27 | 25 |
| Figures | 1, 2 | 3, 6 |

The single manuscript was about 18,700 words with one stated contribution and three supporting
modules. Each paper here is a normal length for a Q1 field journal, and each has one thesis.

**Paper B's thesis is the sharper one.** The same ownership concentration governs three results
usually kept apart: the capital tax reaches little because most corporate claims sit where the
income tax does not; households cannot be made whole by broadened ownership because most equity
is not theirs and what is theirs cannot be spent; and an equity bust transmits weakly because the
assets that fall are held where the propensity to consume is lowest. One fact, three
consequences, and it displaces the profit-shifting explanation on measured evidence.

## Suggested targets

**These ratings have not been verified and must be checked against the official ABDC list and the
current Scimago listing before submission.** They are suggestions based on genre fit, which
matters more than prestige: a measurement paper sent to a policy journal is a desk reject.

- **Paper A:** *Review of Income and Wealth* is the natural home, because it publishes new
  national-accounts objects with long series and distributional cuts. Alternates: *Journal of
  Financial Stability*, *Journal of Banking and Finance*.
- **Paper B:** *National Tax Journal* or *International Tax and Public Finance*. Reach: *Journal
  of Public Economics*. Alternate: *JMCB*.

Neither is a top-five paper, and that ceiling is structural: no identification, no model, one
country, descriptive. Splitting does not raise the ceiling. It stops each paper being rejected
for the other one's weaknesses.

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

Helper scripts, reusable across projects: `_qa.py` (playbook section 8 gates), `_anoncheck.py`
(identity-leak check on the blind build), `_count.py` (body word count), `_to_docx.py` (resolves
the `\ifanon` toggle, the `\result{}` macros, `\ref`/`\eqref` from the `.aux` and natbib
citations from the `.bbl`, then hands plain LaTeX to pandoc).

## QA status

Both papers pass every gate: title within twelve words, abstract within 250, zero em-dashes, zero
occurrences of "robust", zero undefined references or citations, zero undefined `\result` macros,
limitations paired one-to-one with avenues for further research, and zero identity leaks in the
blind build in both PDF and DOCX.

## Open items for the authors

1. **The AI declaration is deliberately not the playbook's standard wording.** The standard text
   states that generative AI was not used to generate or analyse the study's data. For this
   project that would be false, and the playbook's own first rule is total honesty, so both
   papers carry the fuller declaration this project has always used. Flagged for approval rather
   than changed silently.
2. **Affiliation discrepancy.** The playbook records Sriharsha Meduri at Andhra University; the
   manuscript records Oviqo. Both title pages carry Oviqo, as the manuscript did, with the
   discrepancy noted on the page. Needs confirming.
3. **Author order and the corresponding author** are inherited from the original manuscript and
   have not been revisited.
4. **ABDC and Scimago ratings** for the suggested venues are unverified, as noted above.
5. **Paper A cites no companion dependency** and Paper B draws on the accounts without requiring
   them to be published first, but if the two go to different journals the cross-reference in
   Paper B's title page should become a formal citation once Paper A has a working-paper number.

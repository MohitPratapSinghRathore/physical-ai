# The two companion papers

**Built to the Paper-Writing Playbook. Last updated 2026-10-06.** The original single manuscript
remains untouched in `../paper/` as the archive; nothing here modifies it.

These answer Sriharsha's review of 25.09.2026 (split into two objectives, specific titles, focus)
and the second review of 2026-10-06, which is worked through in full below.

---

## What they are

| | Paper A | Paper B |
|---|---|---|
| Directory | `accounts/` | `ownership/` |
| Title | Labor Backing Accounts: Who Holds the Claims That Wages Pay? | Ownership More Than Profit Shifting: Why Capital Taxation Falls Short |
| Objective | What income services the US claim stock, and who holds, guarantees or owes it | Whether the tax system can replace wage-tax revenue when income shifts to capital, and what binds |
| Body words | 9,624 | 9,890 |
| Pages, author PDF | 25 | 25 |
| References | 29 | 34 |
| Figures | 1, 2 | 3, 6 |

Corresponding author on both: **Mohit Pratap Singh Rathore**, first in the author list, on the
manuscript, the title page and the DOCX. The two papers cite each other as working papers, and
the blind builds cite an anonymized entry so the self-citation does not leak authorship.

## The second review, item by item

### Paper A

**The 1947 start was missing, and it mattered.** Resolved first, as instructed. The exposure
series does exist from 1947 and opens at **70 percent**, which matches the
absorption branch's 0.6958 exactly. The manuscript started at 1952 only because Figure 1 plots
the exposure series together with the debt-only ratio, and the debt-only ratio needs
market-valued equity, which the accounts carry only from 1952. The figure code filtered the
exposure series to the years present in the ratio series, truncating it silently.

Fixed: Figure 1's upper panel now runs from 1947 and the lower panel from 1952, with the caption
saying why; Table 11 gains a 1947 row with `n/a` in the debt-only cell; the abstract, Section 4.5,
the appendix and the conclusion all carry the new opening. The claim is stronger, and more
careful: the post-war opening sits close to the present level, so today is a return. What differs
is composition, since in 1947 the position was almost entirely wartime Treasury debt, with the
debtor leg alone at 69 percent against a creditor leg of 9.

**The first null is now stated as voided.** The conclusion presented two pre-registered tests as
two nulls. The oil-episode design was voided by its own pre-shock placebo and supports no reading
in either direction; the panel is the null. The conclusion now says exactly that.

**"Its reading was wrong" reduced from three to one**, and rephrased to "we cannot show their
reading is wrong". The appendix now cross-references L6 instead of repeating it.

**Cross-citation added** in both directions, by title, as working papers.

### Paper B

**The title overclaimed twice and has been changed.** It is now *Ownership More Than Profit
Shifting: Why Capital Taxation Falls Short*.

- "Cannot replace" contradicted the paper's own boundary, which closes if output rises enough per
  displaced wage dollar. The title now says the rate falls short, which is what the paper shows.
- "Not profit shifting" did not survive checking. The shifted share has **one** verified value,
  0.48 (Tørsløv, Wier and Zucman), swept over 0.30 to 0.60 because a second verified source was
  sought and not obtained. The assembled rate is exactly linear in that parameter, so the swing
  scales with the range width, and the flip points can be computed rather than guessed: widening
  the sweep to **0.48 ± 0.16** moves profit shifting to second, and **0.48 ± 0.19** moves it to
  first. The current sweep is 0.48 ± 0.15. The ranking is therefore not stable, and the reviewer
  was right. Section 5 now reports the sensitivity, and the abstract, introduction, related work
  and conclusion all carry the weaker comparative claim.

A separate inconsistency surfaced while checking this: the prose said profit shifting was "fourth
of seven" while the table showed it **third**. Corrected to third.

**It now stands alone.** A new subsection, "Three objects borrowed from the accounts", cites the
companion and defines the retained wage share, the holder mapping and the agency classification
in a paragraph each.

**Spelling normalized to American** across both papers: 14 instances of "labour" plus
`labelled`, `programmes`, `behavioural`, `modelling`, `favour`, `centre`, `normalisation`,
`realised`, `organised` and `harmonised`.

**The 46.9 percent figure now carries its vintage.** It is CBO 2014 Tables A-3 and A-4, used in
the project as an independent cross-check on the CRS deferral factor, and the text had it sitting
next to the Gravelle citation. Both places now say "on 2014 data" and cite CBO 2014.

### Both papers

**"Organisations" changed to "Organizations"** in the section heading, for consistency with the
American spelling. Flagged: the heading is the playbook's standard form, so if the chosen journal
uses British spelling, revert it.

**The dash gate now runs properly.** The reviewer could not confirm it because the author footnote
markers matched their scan. The gate checks U+2014 anywhere, `---` in source, an en-dash used as
punctuation (page ranges in the bibliography are correctly exempt) and a bare `--` in prose. Both
papers score zero on all four.

## FR7 and FR1, completed 2026-10-06

Both were run because the alternative was a referee running them.

**FR7, Paper A: the novelty search.** Protocol published at
`framework/novelty/FR7_SEARCH.md`, with the kill criterion fixed before the search: locating a
construction that takes a national claim stock, classifies each claim by the income that services
it, crosses that with the holder structure and reports an aggregate share would retire the
novelty claim. Six queries. **None located.** The nearest work is now named in the related-work
section with the condition each fails: debt service ratios are a flow, for households, against
disposable income; distributional national accounts answer who owns and owes rather than which
income services what; fiscal risk matrices classify by trigger; who-to-whom accounting classifies
by instrument and counterparty; household debt histories are one sector and distributional.

The claim moves from "none located, no systematic search was run" to "none located under a
stated protocol, and here are the bounds of that protocol". It does not move to "none exists",
and L7 now states what the search does not reach.

**FR1, Paper B: sourcing the swept components.** The profit-shifted share is now sourced from two
independent studies measuring the same object, the share of the foreign profits of US
multinationals booked in tax havens: 48 percent for 2016 from the BEA value added tables
(Tørsløv, Wier and Zucman) and "stable around 50 percent between 2015 and 2020" (Garcia-Bernardo,
Janský and Zucman, NBER w30086, abstract verified verbatim). The range narrows from 0.30 to 0.60,
a judgement interval, to 0.47 to 0.53, which the two estimates span.

**The effect is large and it is the point.** Profit shifting falls from rank 3 of 7 with a swing
of 0.0124 to **rank 7 of 7 with a swing of 0.0025**. The reviewer's objection, that the ranking
flipped if the range widened a little, no longer applies, because the range is no longer a
choice. The headline rate is unchanged at 7.8 percent, because the central case always used the
sourced point value; what changed is the uncertainty around it. The analytic maximum tightens
from 12.4 to 11.5 percent and the pass share on our base falls to zero.

Two things found along the way that go in the paper rather than being quietly fixed:

- **A wrong citation.** The note recording what had been sought cited "Clausing (NBER w28442)".
  NBER w28442 is *Solar Geoengineering, Learning, and Experimentation*. It is not a
  profit-shifting paper.
- **A denominator mismatch, and it runs against our own result.** Both sources measure a share of
  *foreign* profits; the assembly applies the parameter to the whole rent base. That overstates
  shifting unless essentially all rent is earned through foreign affiliates, and correcting it
  would raise the assembled rate and narrow the shortfall the paper reports. It is now L11 with
  FR11 paired to it, with the direction signed and the magnitude unbounded, rather than corrected
  silently in either direction.

**The two components that remain swept** are the effective state corporate rate and the
shareholder-level statutory rate. A published apportioned effective state rate and a realized
average shareholder rate were both sought on the same occasion and neither was found in a form
verifiable from a primary source, so they stay swept and L1 says so.

## Targets, with ratings verified 2026-10-04

| Journal | ABDC | Scimago | Fit |
|---|---|---|---|
| Review of Income and Wealth | listed, rating to confirm | **Q1** Economics and Econometrics | Best genre fit for Paper A |
| Journal of Financial Stability | **A\*** | | Strong for Paper A |
| Journal of Banking and Finance | **A\*** | | Alternate for Paper A |
| National Tax Journal | **A** | | Best fit for Paper B |
| Journal of Public Economics | **A\*** | | Reach for Paper B |
| International Tax and Public Finance | **B** | | Only if the A-list fails |

**Paper A** has a real trade-off: *Review of Income and Wealth* on genre fit and confirmed Q1
status, or *Journal of Financial Stability* on ABDC A\*. **Paper B** goes to *National Tax
Journal* (A), with *Journal of Public Economics* (A\*) worth one attempt first.

The second reviewer inferred the target was *Technological Forecasting and Social Change* from the
section headings. It is not; those headings come from the playbook. If TFSC is wanted, both papers
fit its scope and it is ABDC A, but the genre fit is weaker than the venues above.

## Reference verification

Every cited entry dated 2025 or later was verified against the publisher on 2026-10-04: Korinek
and Lockwood (NBER 34873), Price and Suresh (RAND RR-A4980-1), Falk and Tsoukalas (arXiv
2603.20617), Barhoumi (IMF Note 2026/002), Cohen, Killen and Lau (Chicago Fed Insights), Ieong,
Saputra, Maniar and Cheng (Windfall Trust), Bank for International Settlements (BIS Quarterly
Review, March 2026).

**One entry was wrong on two fields.** `Bayraktar` was recorded as *Emre*, year *2025*. The author
is **Erhan Bayraktar** and the paper is **2026** (arXiv:2605.05127, v1 6 May 2026, v2 31 July
2026). Corrected, key renamed `Bayraktar2026`, all citing files updated. The entry carried a
`verification` field claiming it had been checked, which is the lesson: a verification note is not
verification.

## The decision still outstanding: what to do with the stress test

Neither paper carries the displacement stress test, the 8,588 institution-level results, the
housing agencies, the trust funds or the instrument table. The second reviewer is right that this
should be a decision rather than an omission, and offers three options: a third paper, an online
appendix to Paper B, or the archive.

**My recommendation is the archive now and a third paper later**, rather than the appendix.
Reasoning:

- The material's own stated weaknesses are load-bearing. Section 7 called the second round "the
  weakest module evidentially"; Section 7.3 said its relief result carries less weight than the
  incidence results until a duration-matched experiment is run; Section 7.2 conceded that losses
  are allocated pro rata by category, so the headline dispersion finding, that card-heavy lenders
  break first, is partly true by construction.
- An appendix to Paper B is a poor fit on subject as well as strength. Paper B is about the
  revenue side and ownership concentration; the stress test is about bank balance sheets. It would
  attach the project's weakest module to its strongest argument and hand a referee a target
  without strengthening the thesis.
- As a third paper it needs the duration-matched experiment Section 7.3 names. That is a real
  project with a real result at the end of it, not a salvage operation.

This is the professor's call and it is recorded here as pending, not taken.

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
the figures and the tables have one source of truth. `references.bib` is copied in because bibtex
does not resolve a relative database path reliably here; the Makefile refreshes it and it is
gitignored.

Helpers: `_qa.py` (playbook section 8 gates, the section 2.3 AI-tell check and four dash checks),
`_anoncheck.py` (identity leaks in **both** the blind PDF and the blind DOCX), `_count.py` (body
word count), `_to_docx.py` (resolves the `\ifanon` toggle, `\result{}` macros, `\ref`/`\eqref`
from the `.aux` and natbib citations from the correct `.bbl`, promotes the title and author block
pandoc would otherwise drop, then hands plain LaTeX to pandoc).

Two bugs in `_to_docx.py` were found by the anonymity gate during this round and are fixed: it was
reading the author build's `.bbl` for the blind DOCX, which put the companion paper's real author
names into the anonymous reference list, and it resolved the `\ifanon` toggle before inlining the
section files, so every toggle inside a section was ignored and the blind DOCX kept the disclosure
and funding paragraphs.

## QA status

Both papers pass every gate: title within twelve words, abstract within 250, zero em-dashes, zero
`---`, zero en-dashes as punctuation, zero `--` in prose, zero occurrences of "robust", zero
undefined references or citations, zero undefined `\result` macros, zero AI-tell phrases,
limitations paired one-to-one with avenues for further research, and zero identity leaks in the
blind PDF and the blind DOCX.

## Open items for the authors

1. **The stress-test decision above.**
2. **Affiliation discrepancy.** The playbook records Sriharsha Meduri at Andhra University; the
   manuscript records Oviqo. Both title pages carry Oviqo with the discrepancy noted.
3. **ORCIDs** are "to be supplied" on both title pages, and Pratap Chandra Mandal's email is not
   filled in.
4. **The AI declaration** uses the playbook's wording with its third sentence adjusted, as
   playbook section 6 directs, because the standard clause says generative AI was not used to
   *analyse* the data and the analysis code here was AI-written.
5. **Author order** is inherited from the original manuscript and has not been revisited.
6. **Review of Income and Wealth's ABDC rating** was not pinned to a primary source; its Q1 status
   is confirmed.

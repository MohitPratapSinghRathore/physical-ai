# Response to Sriharsha's review of 25.09.2026, and the two-paper split

**For the author team. 2026-10-04. Nothing in the manuscript has been restructured yet; the
mechanical fixes in §1 are applied and pushed, the split in §3 is a recommendation awaiting
a decision on one open question in §6.**

---

## 1. The four review points, and where each stands

| # | Review point | Status |
|---|---|---|
| 1 | "The title appears to be general. Pls be specific." | Addressed in §4 — two specific titles proposed |
| 2 | "The focus is missing. This is also the reason why the paper is lengthy." | Diagnosed in §2, resolved by §3 |
| 3 | "There are many pictures in the document which are not loading." | **Fixed and verified** |
| 4 | "Is it possible to be focused & create two different objectives? Then two different papers." | **Yes.** §3 gives the split |

### Point 3 was a real defect, not a viewer problem

All six figures were being written with **Type 3 fonts and no embedded font file** — matplotlib's
default, never overridden in `paper/gen_figures.py`. Type 3 subsets render unreliably outside
desktop PDF readers, which is what produced blank or broken figures in review, and **most journals
reject Type 3 outright at submission**. It would have been caught at the desk, not by a referee.

Fixed at the generator (`pdf.fonttype: 42`, `ps.fonttype: 42`), all six figures regenerated, and
`main.pdf` verified Type-3-free.

Two further defects surfaced on the clean rebuild and are also fixed:

- `sec11_limitations.tex` had a literal carriage-return byte where `\ref` should have been, so
  page 31 printed **"Section efsec:displacement's household counterpart"** in the copy that went
  out for review.
- The pass-through equation was printed **twice, identically** — as equation (3) in §5.5 and again
  as equation (4) in Appendix B.18, with the surrounding paragraph restated almost verbatim. The
  duplicate label was also a LaTeX warning. B.18 now cross-references §5.5.

Build is now clean: 50 pages, no Type 3, no undefined references, no multiply-defined labels.

---

## 2. The focus problem, diagnosed from the paper's own sentences

The review is right, and the manuscript says so about itself in three places.

**The thesis sentence contains two theses.** §1, "The central proposition":

> "Wage-dependent public revenues and credit guarantees concentrate automation exposure on the
> federal balance sheet, **while** household and lender outcomes vary with income, debt composition
> and the mechanism of displacement."

Everything before *while* is a claim about **where the exposure sits**. Everything after is a claim
about **who bears it under a shock**. They are different objects, measured from different data, and
answerable independently. A reader cannot carry both.

**§5 is a third thing again.** Whether the tax system can replace the lost revenue is neither of
those clauses. It has its own definitions, its own equation, its own literature and its own
sensitivity analysis — 2,366 words of it.

**The paper concedes the ranking.** §1, "Structure": *"The accounts and the holder map are the
paper's contribution; everything else supports them."* Three supporting modules, twelve policy
instruments and a 5,132-word appendix is a great deal of support for one contribution.

### The length arithmetic

| Section | Words |
|---|---|
| 1 Introduction | 785 |
| 2 Related work | 1,192 |
| 3 Data and method | 1,354 |
| **4 Labor backing accounts** | **2,555** |
| **5 The fiscal condition** | **2,366** |
| 6 Displacement, measured | 1,222 |
| 7 Banks and the second round | 1,030 |
| 8 If AI fails | 894 |
| 9 Institutions, by regime | 966 |
| 10 Limitations | 961 |
| 11 Conclusion | 248 |
| Appendix B | 5,132 |
| **Total** | **~18,700** |

A Q1 field paper runs 8,000–12,000 words. This is two papers carrying a third paper's worth of
supporting material. **The two load-bearing sections, §4 and §5, are almost exactly the same size
as each other** — which is the structural signature of two papers, not one.

---

## 3. The split

The line runs between the two objects the paper already measures separately.

### Paper A — the accounts

**Objective: what income services the US claim stock, and who is left holding it.**
Pure measurement. Makes no predictive and no behavioural claim.

| From the current paper | Role in Paper A |
|---|---|
| §4.1–4.5 entire | The core: definitions, the one-step rule, the debt-only ratio, the holder map, the 79.5% union, the 1952–2025 series and its U-shape |
| §4.6 | The AI-side contrast, as bounds |
| §4.7 + Table 13 | The quintile gradient, 1.37 → 0.64 |
| §2.1, §2.2 | Related work: fiscal risk and contingent liabilities; who-to-whom accounting |
| §3.1, §3.5 | Sources and the status labels |
| Appendix A, B.4, B.5, B.6 | Rebuild protocol and the accounts' conventions |
| §10 L1–L4, "What the accounts are not" | Limitations, including the predictive null |
| Tables 2, 3, 4, 5, 11, 12, 13; Figures 1, 2 | All of it |

**Headline results:** 52% of US debt serviced directly from wages; federal exposure 79.5% as the
union of three roles; the U-shape (52% → 34% → 79%) showing today is a *return*, not a record; the
claims gradient showing claims spread far more evenly than the income servicing them.

### Paper B — ownership concentration

**Objective: whether the tax system can replace wage-tax revenue when income moves to capital,
and why it cannot.**

This is the sharper paper, and it has a single mechanism running through three results.

| From the current paper | Role in Paper B |
|---|---|
| §5 entire | The core: the condition, the assembled rate, the boundary |
| §5.8 | **The finding.** The binding constraint is who owns the claims, not profit shifting |
| §6.7 | The household counterpart from the SCF — the same ownership fact on the incidence side |
| §8 | The bust case — the same ownership fact again, and the two-tax-base result |
| §9.1 | The organizing conclusion |
| §2.3, §2.5 (capital-tax half) | Related work |
| Appendix B.7, B.18, B.20, B.22 | Checks, pass-through, the expensing transition, the lever ranking |
| §10 L5, L14 | Limitations |
| Tables 6, 9; Figures 3, 4 | All of it |

**Why this is one paper and not three results:** the same fact drives all of it. The capital tax
reaches little because 73% of corporate equity sits where the income tax does not. Household
capacity cannot be restored by broadening ownership because 47% of equity sits outside the
household sector and another 25% cannot be spent. A bust transmits weakly to households because
the top 1% hold 50.9% of the equity. **Ownership concentration is the binding constraint on the
revenue side, the household side and the transmission side at once.** That is a single, testable,
quotable thesis — and §5.8 already shows it beats the obvious rival explanation, since moving
profit shifting across its whole range moves the rate less than deferral and step-up do.

---

## 4. Titles (review point 1)

The current title, *Labor-Backed Finance and the Fiscal Exposure to AI*, names a coinage the reader
does not know and a topic rather than a finding. Both halves are general. Proposed:

**Paper A:**
> **Who Holds the Claims That Wages Pay? Labor Backing Accounts for the United States, 1952–2025**

Names the object, the country and the period, and states the contribution as the question it
answers. Conventional for a measurement paper and specific on every axis.

**Paper B:**
> **Ownership, Not Profit Shifting: Why Capital Taxation Cannot Replace the Wage Tax Base**

States the finding and names the rival explanation it displaces. A reader knows what is being
claimed before the abstract.

Alternatives if a result-forward title is preferred for A: *Four Fifths on One Balance Sheet:
Federal Exposure to Wage-Backed Claims, 1952–2025*.

---

## 5. Targets

Stated as targets to check against the current Scimago listing before submission, not as verified
quartiles.

| | Primary | Alternates |
|---|---|---|
| **Paper A** | *Review of Income and Wealth* — publishes exactly this: a new national-accounts object with a long series and a distributional cut | *Journal of Financial Stability*; *Journal of Banking and Finance* |
| **Paper B** | *National Tax Journal* or *International Tax and Public Finance* | *Journal of Public Economics* as a reach; *JMCB* |

Neither is a top-five paper, and that ceiling is structural: no identification, no model, one
country, descriptive. Splitting does not raise the ceiling. What it does is stop each paper being
rejected for the other one's weaknesses — which is the live risk now, since §6–7's scenario
arithmetic is what a measurement referee would attack, and the accounts' conventions are what a
public-finance referee would attack.

---

## 6. The open question, and it is the one that needs a decision

**What happens to §6 (displacement), §7 (banks) and §9 (the twelve instruments)?** That is
3,218 words of body text and a large share of the appendix, and it is a lot of completed work.

It does not fit either focused paper. My recommendation is to **hold it back rather than force it
in**, for reasons the manuscript already states about itself:

- §7 calls the second round *"the weakest module evidentially"* and labels it scenario everywhere.
- §7.3 says of its own relief result that *"until [a duration-matched experiment] is run this
  result carries less weight than the incidence results around it."*
- §7.2 concedes that *"losses are allocated pro rata by category, so business mix is the only
  source of dispersion here"* — so the dispersion finding, that card-heavy lenders break first, is
  partly true by construction. A referee will find that.
- It is conditional arithmetic on an assumed input, which is the part most exposed to the
  objection that the displacement level is chosen rather than estimated.

Two pieces of §6 are strong and should be rescued rather than held:

- **§6.6**, the non-monotonic buffer result — thinnest buffers in the *second* quintile, 0.84
  months against 1.26 at the bottom — is a measured household fact and belongs in **Paper A**
  beside the claims gradient. The two together make one clean point: both claims and fragility are
  mislocated relative to income.
- **§6.8**, that exposure type is a pay effect and the contrast reverses once pay is controlled, is
  a measured debunking result worth keeping. It fits **Paper B**'s incidence half.

The alternative is a third paper from §6–7 later, once the duration-matched experiment §7.3 calls
for has actually been run. That is a real project, not a salvage operation, and it should be
scoped on its own.

### How this relates to the earlier "Section 4.5, not a paper" decision

It does not contradict it. That decision (`framework/paper2/S3_PROGRAMMES.md`) rejected a
*different* split — a second paper built on the history of how the state's guarantee position
grew. That rejection has since become stronger, not weaker: the rotation finding it rested on was
withdrawn as a denominator artefact (`framework/paper3_scoping/K4_RESULT.md`), and the exit finding
was killed against OMB's own published table.

The split proposed here runs along a different line, between two halves that are **both already
load-bearing contributions with their own data, literature and results**. That is why it works
where the other did not.

---

## 7. One substantive update available now

§10's "What the accounts are not" currently reports the validation pilot alone — about 5,900 banks
in one oil-price episode. The predictive panel finished since
(`framework/predictive/`, branch `predictive-panel`): 146,813 bank-years, 10,532 banks, 2001–2024,
pre-registered. Adding the construct makes out-of-sample ranking of banks **worse in 13 of 13 test
years**, and `LB` is 51.7% explained by the loan-share controls alone.

That belongs in **Paper A**, and it helps rather than hurts: it is a pre-registered null on a large
sample, it preempts the obvious referee question, and it is the strongest available justification
for presenting the accounts as accounting rather than as a risk measure. It also settles which
journal A belongs in.

---

## 8. Sequence if the split is approved

1. Paper A first. It is the contribution, it is closest to complete, and B cites it for the accounts.
2. Split `results_macros.tex` by paper so each builds standalone from the same released artifacts.
3. Two `main.tex` files, shared `figures/` and `references.bib`.
4. Re-run the rebuild protocol per paper so each carries its own status labels.
5. Paper B drafts against the released accounts rather than re-deriving them.

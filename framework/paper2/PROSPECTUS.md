# Paper 2: how the state came to hold wage-backed credit

**Prospectus, 2026-09-22. Branch `paper2-absorption`, from master at `c052f96` (A143).**

This is a plan, not a result. Nothing here is committed as a finding; the numbers quoted
are from the existing accounts and are what motivate the project, not its output.

---

## 1. The question

The measurement paper reports that the federal government holds, guarantees or owes **79.4
percent** of the US labour-backed claim stock. It reports that as a level, at one date.

**This paper asks how it got there.** The series runs from 1947 and the answer is not what a
level invites you to assume.

## 2. The thesis, in one falsifiable sentence

> **The state absorbed wage-backed credit twice, by two different mechanisms, and the two
> episodes are almost orthogonal: a guarantee phase in which it insured claims it did not
> owe, and a borrowing phase in which it owed claims it did not insure.**

Falsifiable in three ways. If the two legs moved together rather than in sequence, the
thesis is wrong. If either phase disappears under a defensible alternative classification,
the thesis is conditional rather than true. If the phases turn out already documented on a
common denominator, the thesis is not new.

**All three are live and §7 treats them as kill criteria.**

## 3. What the series actually shows

Sovereign share of the labour-backed claim stock, decomposed into the **obligor leg** (claims
the state owes, chiefly Treasury debt serviced from labour-linked receipts) and the **holder
or guarantor leg** (claims the state holds or stands behind, chiefly agency and GSE pools and
federal student lending).

| Year | Sovereign share | Obligor | Holder | Note |
|---|---|---|---|---|
| 1947 | **0.696** | 0.692 | 0.095 | war debt; a high reached by borrowing alone |
| **1965** | **0.308** | 0.293 | 0.075 | **the trough** |
| 1970 | 0.336 | 0.296 | 0.120 | |
| 1990 | 0.564 | 0.365 | 0.248 | |
| 2000 | 0.562 | 0.304 | **0.315** | the holder leg overtakes the obligor leg |
| 2007 | **0.501** | 0.239 | 0.304 | pre-crisis low |
| 2008 | 0.558 | 0.286 | 0.298 | conservatorship |
| 2010 | 0.649 | 0.365 | 0.332 | |
| 2021 | 0.778 | 0.510 | **0.407** | holder leg peaks |
| 2025 | **0.794** | 0.552 | 0.321 | |

**The series is not a rise. It is U-shaped**, and the 1947 peak of 0.696 was reached by a
mechanism — war borrowing — that has nothing to do with the modern one.

The decomposition of the two modern episodes:

| Episode | Sovereign share | Obligor leg | Holder leg |
|---|---|---|---|
| **1965 → 2000, the guarantee phase** | 0.308 → 0.562 | **+0.011** | **+0.241** |
| **2007 → 2025, the borrowing phase** | 0.501 → 0.794 | **+0.313** | **+0.017** |

**Each episode moves one leg and leaves the other where it found it.** That is the paper.

A third movement is now under way and points the other direction: the holder leg peaked at
**0.407 in 2021** and has fallen to **0.321** by 2025, as the Federal Reserve's balance sheet
contracts and agency portfolios run off. Whether that is a reversal or a pause is a question
the paper can pose but not answer.

## 4. The central vulnerability, and the design that confronts it

**The guarantee phase is agency-pool growth. Whether it is "the state" at all depends on one
classification choice.**

The accounts' own robustness table:

| Judgement call | Sovereign share | Move |
|---|---|---|
| Central: agency pools, GSEs and the central bank all federal | **0.794** | — |
| Most other calls (Treasury definition, backing shares, rent, consumer blend) | 0.788–0.804 | **under 1.3%** |
| Commercial mortgage treated like multifamily | 0.741 | −6.6% |
| **Agency pools NOT federal** | **0.587** | **−26.1%** |
| **The one-step rule relaxed to second-round backing** | **0.452** | **−43.1%** |

Under "agency pools not federal", **the guarantee phase largely disappears** — it was the
guarantee. A referee finds this immediately, and a robustness appendix will not survive it.

**So the paper does not defend the central classification. It makes the two classifications
its subject:**

> How much of the state's position in wage-backed credit is *explicit*, and how much rests on
> the agency guarantee? Under the strict classification there is one episode. Under the
> classification the conservatorship made explicit there are two. **The difference between
> the two series is the stock of agency-guaranteed claims as a share of the labour-backed
> claim stock**, and September 2008 is the date that difference stopped being treated as
> open.

> **CORRECTED 2026-09-22 by `S2_SERIES.md` §4.** This paragraph originally called the
> difference "the market value of an implicit guarantee". That was wrong. A stock of claims
> that a classification moves from one column to another is not a valuation, and nothing in
> this project prices a guarantee. The difference is a **stock of claims**, it peaks at 0.2814
> in 2003, and it does **not** jump at 2008 (0.2550 in 2007, 0.2650 in 2008).

This converts the weakness into the research question, and it buys something the paper
otherwise lacks: a **discrete event that resolves a classification ambiguity**. It is not
identification and will not be called identification, but the two series must converge at
conservatorship, and whether they do is a check the paper can run and report.

**The one-step rule is handled differently.** It moves the level by 43 percent but applies to
the denominator in every year, so it should shift the series without changing its shape. That
is an assertion to be tested, not assumed: §7 lists it as a task, and if the shape does change
the thesis is in trouble.

## 5. Data

**Everything needed for the central series already exists.**

| Input | Source | Status |
|---|---|---|
| Claim levels by class, 1945– | Financial Accounts Z.1 | in the accounts |
| Holder shares by class, every year | Z.1 holder tables | **in the accounts, and genuinely measured throughout** |
| Class labour backing coefficients β | ACS, SIPP, SOI | in the accounts, **held constant pre-2021** |
| Sovereign share series 1947–2025 | `direct_ratio_timeseries.csv` | built |

**The one strength to lean on, and the one limitation to state plainly.** The accounts'
own methodology note says the pre-2021 series holds the labour shares fixed, so it is *not* a
measurement of how labour backing itself moved — **but the sovereign share is the part that is
genuinely measured throughout, because holder shares come from Z.1 in every year.** This paper
uses exactly that part. That is the reason it is the right second paper and not, say, a paper
about the ratio.

**To be built:**

1. The **alternative-classification series** (agency pools not federal) for all years. The
   current file carries the alternative only at 2025. This requires splitting the holder leg
   into agency-pool and non-pool components annually, from Z.1.
2. The **second-round variant** of the denominator for all years, to test whether the one-step
   rule changes the shape.
3. A **counterfactual decomposition**: what would the 2025 share be absent conservatorship,
   absent the post-2010 shift to federal direct student lending, absent post-2008 Treasury
   growth. Shift-share on the existing components; no new data.

**Optional second observation.** A euro-area series is partly built (ECB QSA, 2025Q4 only).
It would be a cross-check, not a panel — ECB QSA carries no issuer-counterpart detail, so the
holder leg abroad is a bound rather than a measurement. Include only if §7's novelty check
comes back clean and time allows.

## 6. Novelty position, stated narrowly

**Known, and not claimed:** GSE growth from the 1970s is documented in mortgage-market terms.
Post-2008 federal debt growth is obvious. CBO publishes federal credit levels annually.

**What appears to be absent, and is the contribution:**

- Putting guarantee and borrowing on **one denominator** — share of wage-backed claims —
  which is what makes them comparable at all.
- The **U-shape**, and therefore the fact that today's level is a return rather than a record.
- The **orthogonality** of the two episodes.
- The **implicit-guarantee gap** as a measured series with a dated resolution.

**A hook worth one sentence and no more.** CBO's official federal credit measure is **$4.0tn**
(FY2024: $1.8tn direct plus $2.2tn guaranteed). The holder leg here is **$13.0tn**, **3.25
times** larger — because the official measure excludes GSE guarantees and Federal Reserve
holdings **by definition**. That is a definitional difference, not concealment, and must be
stated as such or it will read as insinuation.

**Nearest existing work:** Jordà, Schularick and Taylor, *The Great Mortgaging* — bank
mortgage shares across 17 economies since 1870, but not the government share and not
wage-backing. Acharya (2011), *Governments as Shadow Banks* — quantifies the GSE footprint at
41.3 percent of residential mortgages at the crisis, and already connects guarantees to
capital risk weights. Neither builds a long-run series on a wage-backed denominator.

## 7. Work plan, with kill criteria

**Session 1 — the novelty check, and nothing else.**
Has anyone measured the government's share of US household or mortgage credit **as a time
series**? Not the level, not the origination share: the stock share over decades.
- **KILL** if a published series exists on a household-credit denominator covering the
  guarantee phase. The paper then collapses to the implicit-guarantee gap alone, which is
  probably a note.
- **NARROW** if the GSE share of mortgages over time exists but not on a household or
  wage-backed denominator. Proceed, claiming only the denominator and the synthesis.

**Session 2 — build the two series.**
The alternative-classification series and the second-round-denominator series, annually.
- **KILL** if the one-step rule changes the *shape* and not just the level. The thesis is
  about shape.
- **KILL** if the two classification series do **not** converge at conservatorship. The
  implicit-guarantee framing then has no empirical anchor.

**Session 3 — counterfactual decomposition and robustness.**
Contribution of each episode and each policy change to the 2025 level. Every judgement call
from the robustness table applied to the series, not just the level.

**Session 4 — draft.**

**Stop rule:** if sessions 1 or 2 fire a kill, stop and write the note instead. Do not
redefine the thesis to survive; that is what `SPECIFICATION_V2.md` in the household workstream
had to be labelled post hoc for, and the lesson is in the repository.

## 8. Realistic assessment

**Target: Q1 field journal on the Scimago scale** — *Journal of Financial Stability*, *Review
of Income and Wealth*, *Journal of Banking and Finance*, *JMCB*. These publish long-run
measurement papers of exactly this shape.

**Not a top-five paper.** No identification, no model, one country, descriptive. That ceiling
is structural and no amount of work raises it. Q2 is the likely floor if the classification
framing is handled weakly or the novelty check narrows hard.

**What would move it up:** a clean novelty result in session 1; the euro-area series as a
second observation; and the conservatorship convergence check working.

**What would sink it:** the guarantee phase turning out to be documented; the one-step rule
changing the shape; or presenting the CBO contrast as concealment rather than definition.

## 9. Relationship to the existing record

This paper makes **no predictive claim**, so the validation pilot's archived null does not
constrain it and should be cited as the reason the paper is descriptive by design. It uses the
holder map from the measurement paper and the same coefficient set, so it inherits the
accounts' limitations and must restate them rather than relying on the reader knowing them.

**It is the second paper because it asks a question the first does not:** the measurement
paper asks what the claim stock rests on and what that implies for an AI displacement
scenario. This one asks how the state came to stand behind so much of it, and answers with a
sequence rather than a level.

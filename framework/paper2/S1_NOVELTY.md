# Session 1: the novelty check

**2026-09-22. The only task of this session, per `PROSPECTUS.md` §7. No series was built and
no finding was produced beyond what is needed to score the criterion.**

## Verdict

**KILL does not fire. NARROW fires twice. Proceed, with the contribution narrowed.**

And one piece of new evidence that cuts the paper's way: **the holder leg is not the public
GSE series.** Their year-on-year changes correlate at **+0.09**.

---

## The criterion, restated

> **KILL** if a published series exists on a household-credit denominator covering the
> guarantee phase.
> **NARROW** if the GSE share of mortgages over time exists but not on a household or
> wage-backed denominator. Proceed, claiming only the denominator and the synthesis.

---

## NARROW-A — FHFA publishes a GSE share series, on a mortgage denominator, 1990–2010

FHFA's market data carries "total mortgages held or securitized by Fannie Mae and Freddie Mac
as a percentage of Residential Mortgage Debt Outstanding, **1990–2010**", and states it does
not plan to extend it.

**Why this is NARROW and not KILL.** The denominator is residential mortgage debt, not
household credit and not wage-backed claims. The window is 1990–2010, which covers the last
decade of the guarantee phase as this paper dates it (1965–2000) and none of the borrowing
phase. It carries only the holder leg, and only the GSE part of it.

**The sharper version of the same objection**, which a referee will make and which FHFA's own
page invites: the numerator is a FRED series (`AGSEBMPTCMAHDFS`, agency- and GSE-backed
mortgage pools), so the GSE share of mortgages is two public series divided. If this paper's
holder leg were a rescaling of that, there would be no series contribution at all.

**It is not.** See the test below.

## NARROW-B — CBO publishes a combined federal credit and insurance measure, 2012–2021

CBO, *Financial Commitments of Federal Credit and Insurance Programs, 2012 to 2021*
(publication 59021), reports that the combined covered amount equalled **about one third of
the value of total financial assets owned by US households in 2021, down from 41 percent in
2012**.

**Why this is NARROW and not KILL.** The denominator is household financial **assets**, not
household credit. The window is ten years. It covers credit and insurance **commitments** and
therefore excludes the obligor leg entirely — no Treasury debt. And it is a level relative to
assets, not a decomposition.

It is nonetheless the closest published object to this paper's holder leg and **must be cited
and distinguished explicitly**, not left for a referee to find.

## What was searched for and not found

- A multi-decade series of the government share of **household credit**.
- Any measure combining the **obligor leg** (Treasury debt serviced from labour-linked
  receipts) with the **holder leg** (guarantees) on one denominator.
- Anything on a **wage-backed** denominator.
- Any statement of the U-shape or of the two-phase decomposition.

Recorded as absences. An absence of search hits is weak evidence and is not being treated as
established novelty.

Nearest long-run work remains Jordà, Schularick and Taylor, *The Great Mortgaging* — bank
mortgage shares, 17 economies, since 1870, but not the government share — and Green and
Wachter (*JEP* 2005) on the evolution of the US mortgage, which is institutional history
rather than a series.

---

## The test that matters: is the holder leg just the public GSE series?

Public series built as `AGSEBMPTCMAHDFS` (agency- and GSE-backed mortgage pools) over total
mortgages, both from FRED, 1947–2025, against this paper's holder leg.

| | Correlation |
|---|---|
| Levels | **+0.70** |
| **Year-on-year changes** | **+0.09** |

**In changes they are unrelated.** And the divergence is not noise — it is structural and it
starts at the crisis:

| Year | Holder leg | Public GSE share of mortgages |
|---|---|---|
| 1965 | 0.075 | 0.002 |
| 1989 | 0.230 | 0.237 |
| 2001 | 0.328 | **0.376** |
| 2007 | 0.304 | 0.295 |
| 2013 | **0.375** | **0.114** |
| 2025 | 0.322 | 0.148 |

**The public GSE share peaks in 2001 and collapses after the crisis. The holder leg keeps
rising to a 2021 peak.** They move in opposite directions for fifteen years.

The reason is that the holder leg contains what the GSE series excludes: **Ginnie Mae**, which
is a government corporation rather than a GSE and which grew sharply after 2008; **federal
direct student lending**, which is now 97.3 percent federal; and **Federal Reserve holdings of
agency securities**. On a wage-backed denominator these belong in the state's position; on a
GSE-share-of-mortgages measure none of them appears.

**This answers the strongest objection to the paper** and should be an exhibit in it, not a
footnote.

**It also changes the story.** `PROSPECTUS.md` §3 describes two mechanisms. This test shows the
guarantee mechanism itself **changed composition**: GSE-dominated to 2001, then migrating to
Ginnie, direct student lending and the central bank. That is a third thing to decompose, and
§7 session 3 should pull it apart rather than reporting "the holder leg" as one object.

---

## What the paper can and cannot claim after this session

**Can claim:**
- The wage-backed denominator, which no published measure uses.
- Obligor and holder legs on **one** scale, which no published measure does.
- The long run, 1947–2025, against FHFA's 1990–2010 and CBO's 2012–2021.
- The U-shape, and therefore that today's level is a return rather than a record.
- The orthogonality of the two episodes.
- That the holder leg is not reducible to the public GSE series, demonstrated.

**Cannot claim:**
- That GSE growth is newly documented. It is not.
- That post-2008 federal debt growth is newly documented. It is not.
- That the federal credit footprint has never been measured. CBO measures it annually.

**Honest cost of two NARROW findings.** The contribution is now the *denominator*, the
*synthesis* and the *long run* — not the underlying facts, all of which are known separately.
That is thinner than the prospectus assumed when it was written, and it moves the realistic
target toward the lower end of the Q1 band. It does not change the recommendation to proceed,
because the divergence test gives the series a defence it did not have this morning.

---

## Session 2 stands as written

The kill criteria for session 2 are unchanged and are the next thing to test:

- **KILL** if the one-step rule changes the *shape* of the series rather than its level.
- **KILL** if the two classification series do not converge at conservatorship.

One addition, from the divergence finding: the holder leg should be **decomposed by programme**
— GSE pools, Ginnie, direct student lending, Federal Reserve holdings — since it is now known
not to be a single mechanism.

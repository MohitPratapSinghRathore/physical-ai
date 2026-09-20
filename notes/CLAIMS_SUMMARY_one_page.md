# Who holds the claims that wages pay

One page for a prospective co-author. 2026-09-20. Full dossier with every number, source and
caveat: `notes/CLAIMS_DOSSIER_full.md`. Source of truth for tags:
`data/release/headline_clearing_pass.csv`.

**Tags.** **[R]** rebuilt independently, from raw data and a published brief, by an instance
that did not write the code. **[M]** measured here, not independently rebuilt. **[S]**
arithmetic conditional on an assumed path.

---

## The finding

**In the United States the federal government is exposed, as holder, guarantor or debtor, on
about 79 percent of the financial claims paid directly out of wages: about 32 percent as
creditor or guarantor, through agency mortgage guarantees and the student loan book, and about
55 percent as the debtor on Treasury debt serviced from wage taxes.** The two legs overlap
where it holds its own debt, so they do not simply add. **It holds about 1 percent of the
claims on AI capital**, and that 1 percent is an upper bound, because the AI side is measured
from on-balance-sheet filings only. It is the main bearer of the exposure that loses if AI
replaces labour and has almost no stake in the one that gains. **It is largely unhedged: its
only claim on the AI side is whatever capital tax reaches those profits.**

**Three conventions move the 79 percent and are reported beside it.** Count only what the
government holds or guarantees, setting aside what it owes: **32 percent**. Do not treat
agency mortgage pools as federal: **59 percent**. Count claims backed only *indirectly* by
wages, where wages become spending and spending becomes business revenue: **45 percent**.

**What counts as wage-backed.** A claim qualifies only if wages pay it *directly*: mortgages,
rent, consumer and student credit, and federal and municipal debt serviced from income and
payroll taxes. That is the same first-round boundary the rest of the paper uses, so the pair
is reported together: the state is the first-round holder, private balance sheets the
second-round holders.

## What we contribute

The fiscal mechanism is established literature and we do not claim it. IMF Note 2026/002
asserts the household-credit mechanism and the distributional asymmetry; RAND (2026) measures
the federal revenue exposure. **Ours is five measured things: the holder structure; household
losses from survey microdata mapped to the Federal Reserve's own loss rates; incidence, or who
bears the loss; a replicated fiscal condition with sourced parameters; and a public claims
register.**

## Six results

| | | tag |
|---|---|---|
| 1 | **The state's exposure is U-shaped, not rising.** It was **52 percent in 1952**, almost all of it wartime Treasury debt; fell to **34 percent in 1970** as that debt shrank against a growing claim stock; and is **79 percent in 2025**. Two datable drivers: the agency book grows 1970 to 1990, then federal debt grows 2008 to 2020. **Much of the recent rise is growth in federal debt itself**, not new exposure to households: the debtor leg went from 29 to 55 percent while the creditor leg peaked in 2020 and has since fallen. Through all of it the share of *all* financial claims that wages back stayed flat near 27 percent | [M] |
| 2 | **Whether the budget absorbs the loss depends on which capital tax rate reaches AI profits.** It needs about 11 to 14 percent. AI capital, after immediate expensing and profit shifting, bears about 7. Capital economy-wide bears 20 to 22 (IMF). **So a quarter to a half of AI profits would have to be taxed at the ordinary rate** | inputs [R], verdict provisional |
| 3 | **Displacement is a fiscal event before a banking event.** At 10 percent of wages displaced, the only level fully inside observed data, the federal government bears roughly 80 to 90 percent of first-round losses, and direct household credit losses are small | [M] |
| 4 | **The housing agencies absorb it without reaching the Treasury.** 39 to 53 percent of each single-family book carries no credit enhancement; private insurance and risk transfer take only 11 to 15 percent of the loss; no Treasury draw at any level we can reach | [M] |
| 5 | **Households, from survey microdata.** Savings buffers are thinnest in the **second** wage quintile, not the first. Differences between physically and cognitively exposed households are **a pay effect**: controlling for pay removes the gap, and an independent rebuild reached the same conclusion in all eight cells. When automation works through **non-hiring** rather than layoffs, losses shift onto younger borrowers carrying student and car debt, mortgage losses fall, and **the fiscal loss is unchanged** | [M]; pay effect independently confirmed in direction |
| 6 | **Banks are reached mainly at large displacement, and mostly indirectly.** Demand leads the other channels in 20 of 27 grid cells **[R]**. That roughly nine tenths of bank losses arrive through the second round, via falling spending, house prices and business credit rather than displaced borrowers' own loans, is a different quantity and is **[S]** | as marked |

## What we withdrew

The reemployment rate at 50 percent displacement (no admissible value exists); an incidence
robustness claim; the bottom-quintile debt ratio's magnitude; a hedging ratio whose input we
never defined; two occupation exposure indices; and priority on the fiscal mechanism itself.
Eleven withdrawals in all, listed with reasons in the dossier.

## Limitations

Off-balance-sheet and GPU-backed AI financing is unmeasured, so the AI side is a lower bound.
Capital gains inside the receipts split are unsourced. The novelty claim rests on a
non-systematic search. A quarter of the mortgage book is an unidentified residual. Labour tax
rates do not vary by income. **All credit losses are first-round only, with house prices held
fixed, so they are floors.** **Above about 25 percent displacement our estimates become bands.
That is a limit of our method, not a fact about the world: it comes from extrapolating a
straight-line reemployment fit until it breaks.** And the capital tax base in result 2 is
contested. The replication was blind by protocol, not by isolation.

## The question for you

**Is about 7 percent the right rate, or the wrong base?** We compute the rate on the marginal
dollar of US AI profit: 21 percent statutory, the normal return exempted by immediate
expensing, and 48 percent of the remaining rents booked offshore. The IMF measures 20 to 22
percent economy-wide, including personal taxes on dividends and gains. The condition needs 11
to 14. It fails on ours and passes on theirs, and **the paper's central fiscal verdict turns
on that choice.**

## Disclosure

The pipeline and analysis were built with Claude Code. The design was reviewed with Claude.
The analysis was replicated by separate instances.

**Target journal is open.** The centre of the paper is now fiscal and sovereign rather than
bank-facing, so a public finance or macro outlet may fit better than the Journal of Financial
Stability.

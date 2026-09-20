# How retained GSE losses are counted in the federal share. One place, both ways.

Closing pass, item 3. No new analysis. Restates the two readings already computed in
`src/item4_federal_share.py` and `data/processed/item4_federal_share_by_dose.csv`.

## The classification problem, stated once

The Enterprises are in conservatorship. A loss they retain is absorbed by net worth of
**179.4bn**. Three facts make the accounting treatment genuinely ambiguous rather than merely
uncertain:

1. **No new Treasury draw is triggered** at any dose this engine reaches. The Senior Preferred
   Stock Purchase Agreements trigger a draw only when "total liabilities exceed total assets",
   that is on **negative net worth**. The largest retained first-round loss anywhere on the
   grid is **109.0bn** against 179.4bn of net worth.
2. **But Treasury holds a senior claim on that net worth regardless.** The senior preferred
   liquidation preference already stands at **140.2bn on Freddie alone** and grows with
   retained earnings. Net worth consumed by credit losses is net worth that never reaches the
   senior preferred.
3. **There are no private shareholders positioned to absorb it.** Common and junior preferred
   holders sit behind the senior preferred, which is itself larger than the net worth in
   question.

So a retained GSE loss reduces a balance sheet on which the Treasury has the senior claim,
without triggering the statutory backstop. **Counting it as wholly private overstates private
loss absorption; counting it as wholly federal overstates the federal cash cost.** Both
readings are reported, and neither is presented as the answer.

## The two readings, defined

| reading | what is FEDERAL on the agency book | what is PRIVATE |
|---|---|---|
| **NARROW** (as published) | only the loss **beyond** Enterprise capital plus one year of pre-provision pre-tax earnings. Zero at every dose | private cover (PMI claims plus the CRT band) **and** the loss absorbed by Enterprise net worth |
| **CONSERVATORSHIP** | the **whole retained loss**, because it consumes net worth over which Treasury holds the senior claim | only what private cover actually pays |

**Narrow is the lower bound on the federal share. Conservatorship is the upper bound. They
travel together and neither is a central case.**

## The federal share of first-round losses, by dose, both ways

| dose | inside the data | **NARROW** | **CONSERVATORSHIP** |
|---|---|---|---|
| 5 pct | yes | 0.759 to 0.853 | 0.857 to 0.901 |
| **10 pct** | **yes** | **0.785 to 0.870** | **0.876 to 0.913** |
| 25 pct | yes | 0.810 to 0.923 | 0.878 to 0.948 |
| 50 pct | **no** | 0.855 to 0.925 | 0.897 to 0.949 |
| 75 pct | **no** | 0.809 to 0.897 | 0.859 to 0.924 |

**The gap between the two readings is 8 to 10 percentage points and it never changes the
qualitative result.** The federal government bears the majority of first-round losses at every
dose under both readings, and roughly four fifths to nine tenths at the 10 percent dose that
is fully inside the observed data.

**The headline depends on the dose**, and the share is **not monotone**: it peaks at the 50
percent dose and falls back at 75, because the fiscal component saturates while credit losses
keep growing on balances that are still there.

## What the item 1 rebuild did and did not change here

**Nothing, under the narrow reading.** The `beyond` layer was zero before the rebuild and is
zero after it, so reallocating the agency loss between private cover and Enterprise capital
leaves both on the private side. The replicator asked this question directly and their answer
was right: **none of the sovereign gap is attributable to the GSE treatment.**

**The rebuild is what makes the conservatorship reading meaningful**, because it determines
how much of the loss private cover actually takes:

| dose | GSE loss bn | private cover bn | **Enterprises retain bn** | Treasury draw |
|---|---|---|---|---|
| 10 pct | 23.9 | 2.5 | **21.4** | 0 |
| 25 pct | 58.3 | 12.6 | **45.7** | 0 |
| 50 pct | 111.7 | 43.9 | **67.8** | 0 |
| 75 pct | 160.2 | 72.2 | **88.1** | 0 |

Under the superseded formula private cover took the whole loss at every dose, so the two
readings would have coincided. Under the rebuild private cover takes **11 percent** at the 10
percent dose, and that is the entire source of the 8 to 10 point spread.

## The sentence for the paper

> The agency book converts 85 to 89 percent of a wage shock into a loss retained by entities in
> conservatorship, without triggering the statutory Treasury backstop at any dose this engine
> can reach. Whether that retained loss is called federal is a classification choice, not a
> measurement: it moves the federal share of first-round losses from 0.785 to 0.870 up to
> 0.876 to 0.913 at the 10 percent dose. **Both are reported. FIRST ROUND ONLY, house prices
> held fixed.**

# Item 1. Housing agencies, rebuilt loan class by loan class

Code: `src/gse_waterfall.py`. Outputs: `data/processed/gse_book_structure.csv`,
`gse_waterfall_classes.csv`, `gse_waterfall_rebuilt.csv`, `gse_waterfall_summary.json`.
Sources retrieved to `data/raw/gse/`: Fannie Mae 2025 Form 10-K (accession
0000310522-26-000015) and Freddie Mac 2025 Form 10-K (accession 0001026214-26-000021),
both pulled from EDGAR with the declared User-Agent under decision D8.

## 1. What was wrong, and it was worse than the replicator found

The superseded waterfall was

    transferred = min(GSE loss, CRT risk in force + PMI risk in force)

with a 592.855bn transfer layer. The replicator showed the layer is never reached, so the
federal `beyond` term is dead code and neither our figure nor their zero is informative.
Rebuilding against the filings finds **three** errors, not one, and two of them are errors
of fact in the inputs rather than in the formula.

**(a) Risk in force is maximum coverage, not a first-loss layer.** Confirmed. Both
Enterprises define it that way in terms: "Risk in force refers to the maximum potential loss
recovery under the applicable mortgage insurance policies in force" (Fannie).

**(b) The 210.0bn CRT figure is the wrong quantity by a factor of about 2.6.** It is the
FHFA Credit Risk Transfer Progress Report's CUMULATIVE risk transferred at ISSUANCE from
2013 through 2023, across both Enterprises. The waterfall needs OUTSTANDING risk in force
on the current book. The filings give it directly:

| | outstanding back-end CRT risk in force |
|---|---|
| Fannie Mae | **39bn**, stated as "approximately $39 billion as of December 31, 2025" |
| Freddie Mac | **40.0bn**, STACR 24.935 plus ACIS 15.081 |
| combined | **79.0bn**, against the 210.0bn used |

**(c) The PMI-covered share of the book is 21 to 22 percent, not 6 percent.** This is the
error the replicator made, and the instruction to verify it rather than take it on trust was
the right one. The 6 percent figure is risk in force OVER the book, which is the covered
share times the coverage depth, not the covered share. Fannie states both numbers in the
same section and they are different numbers:

> "Our total mortgage insurance in force was $745.9 billion, or **21%** of our single-family
> conventional guaranty book of business ... our total mortgage insurance risk in force was
> **$201.4 billion**, or 6% [of the book]."

Freddie's Table 23 says the same: primary mortgage insurance covers **$680,950m, 22% of the
portfolio**, with maximum coverage of $181,462m. So the coverage depth is

    201.355 / 756.0 = 0.2663   (Fannie)
    181.462 / 680.95 = 0.2665  (Freddie)

about 26.6 percent on both books, which is the standard master-policy coverage percentage.
**PMI reaches three and a half times as much of the book as the replicator assumed, and pays
about a quarter of the loss on what it reaches.** Those two errors run in opposite
directions, which is why a wrong covered share and a wrong construction could both be
present without the answer looking absurd.

## 2. The rebuilt book

Both Enterprises publish their credit enhancement buckets gross, with one combined deduction
for loans carrying more than one enhancement, and do not say which pairs overlap.
ASSUMPTION, stated and bounded: the whole overlap is PMI and CRT together, which is the
economically dominant pair because both instruments select the same above-80-LTV loans. The
overlap cannot exceed the PMI bucket and on both books it does not.

| enterprise | class | UPB bn | share of book |
|---|---|---|---|
| Fannie Mae | PMI only | 358.0 | 0.101 |
| Fannie Mae | PMI and CRT | 398.0 | 0.113 |
| Fannie Mae | CRT only | 879.0 | 0.248 |
| Fannie Mae | other | 28.0 | 0.008 |
| Fannie Mae | **no credit enhancement** | **1,875.3** | **0.530** |
| Freddie Mac | PMI only | 128.6 | 0.041 |
| Freddie Mac | PMI and CRT | 552.4 | 0.175 |
| Freddie Mac | CRT only | 1,207.4 | 0.383 |
| Freddie Mac | other | 38.4 | 0.012 |
| Freddie Mac | **no credit enhancement** | **1,229.5** | **0.390** |

**Between 39 and 53 percent of each single-family book carries no credit enhancement of any
kind.** That is the single fact the old formula concealed, and it is the reason the result
moves rather than vanishes.

## 3. Coverage depth by class, all sourced

**PMI.** Applies only above an 80 percent LTV ratio at acquisition. Fannie: "Our Charter
generally requires credit enhancement on any single-family conventional mortgage loan that we
purchase or securitize if it has an LTV ratio over 80% at the time of acquisition." It pays a
coverage percentage of the claim, taken here as risk in force over insurance in force,
0.266.

**CRT.** Mezzanine, with the Enterprise retaining the first loss, exactly as the replicator
argued and now sourced. Fannie: "In CIRT deals, we generally retain an initial portion of
losses on the loans in the pool (for example, the first **0.75%** of the initial pool UPB).
Reinsurers cover losses above this retention amount up to a detachment point (for example,
the next 4.0% of the initial pool UPB). **We retain all losses above this detachment
point.**" Freddie: "We generally retain the initial loss position and **at least 5%** of the
credit risk of all the positions sold."

The outstanding band is far thinner than the issuance example, because it amortises:

| | outstanding maximum coverage as a share of the reference pool |
|---|---|
| Fannie CAS and CIRT | 3.05 percent |
| Freddie STACR and ACIS | 2.27 percent |

Freddie says why, and it matters for any forward-looking use: "in recent periods, we have
changed our business strategy and revised our CRT transactions by **retaining higher levels
of initial losses**. As a result, the benefits provided by these revised CRT transactions may
be lower than those provided by the earlier CRT transactions."

**Loss intensity by class.** Allocating a shock pro rata by UPB would put too little of it
where the cover is. Freddie publishes serious delinquency by enhancement class as of
2025-12-31: PMI 1.19 percent, CRT and other 0.68, non-enhanced 0.40. Relative SDQ is used as
the class loss weight; flat pro rata is carried as the sensitivity, and the two bracket the
answer.

## 4. The result

Agency losses are this project's own first-round figures from
`dose_response_first_round.csv`, unchanged. What changes is what happens to them.

| dose | inside data | GSE gross loss bn | private cover bn | **Enterprises retain bn** | retained as pct of net worth | Treasury draw |
|---|---|---|---|---|---|---|
| 5 pct | yes | 3.30 to 12.05 | 0.20 to 1.28 | **2.95 to 11.33** | 1.6 to 6.3 | 0 |
| **10 pct** | **yes** | **6.54 to 23.91** | **0.39 to 2.53** | **5.85 to 22.48** | **3.3 to 12.5** | **0** |
| 25 pct | yes | 15.96 to 58.30 | 0.96 to 12.58 | 14.27 to 52.42 | 8.0 to 29.2 | 0 |
| 50 pct | no | 30.57 to 111.72 | 1.83 to 43.94 | 27.33 to 82.54 | 15.2 to 46.0 | 0 |
| 75 pct | no | 43.85 to 160.24 | 2.62 to 72.18 | 38.19 to 108.99 | 21.3 to 60.8 | 0 |

**Private cover transfers only 11 to 15 percent of the loss at small doses**, rising to about
45 percent at the largest dose because CRT bands are thin and only start absorbing once the
pool loss rate clears the retained first loss. The transfer layer is not 592.855bn and it is
not a layer at all: it is a thin mezzanine band on 36 to 56 percent of the book plus a
quarter of the loss on 21 to 22 percent of it.

## 5. Guarantee fee income and capital

| | bn |
|---|---|
| combined net worth, FY2025 10-K | **179.4** (Fannie 109.0, Freddie 70.4) |
| one year of pre-provision pre-tax earnings | 34.24 |
| annual guarantee fee income | **40.49** (Fannie 23.595, Freddie 16.897) |
| remaining Treasury funding commitment | **254.1** (Fannie 113.9, Freddie 140.2) |

Guarantee fee income is not added to the buffer, because it is already inside pre-provision
pre-tax earnings. It is reported because it is the rate at which the buffer replenishes:
**the Enterprises earn, in one year of guarantee fees, more than the entire retained loss at
the 10 percent dose, and about half of it at the 75 percent dose.**

The project has been using 190.436bn for capital, from 10-Q net worth at 2026-03-31 and
2026-06-30. The 10-K figure of 179.4bn is used here so that capital and the loan class table
come from the same filing and the same date. The difference does not change any sign.

## 6. The federal layer under conservatorship

The old construction used `beyond = max(0, retained - capital - one year of PPNR)`. That is
not the trigger. The Senior Preferred Stock Purchase Agreements define it, and the filings
state it:

> "On a quarterly basis, we may draw funds from Treasury to cover the amount that our **total
> liabilities exceed our total assets** for the applicable fiscal quarter."

The draw triggers on **negative net worth**, not on exhausting net worth plus a year of
earnings. That is a tighter trigger than the one we used, and it still is not reached: the
largest retained loss anywhere on the grid is 109.0bn against 179.4bn of net worth.

**So the federal layer, read narrowly as a Treasury draw, is zero at every dose from 5 to 75
percent.** That is now a result rather than an artefact: it follows from 179.4bn of capital
against a maximum retained first-round loss of 109.0bn, not from a phantom 592.855bn layer.

**Read in substance, the federal layer is the whole retained loss.** The Enterprises are in
conservatorship. Net worth is held against a Treasury commitment, the senior preferred
liquidation preference already stands at 140.2bn on Freddie alone and grows with retained
earnings, and there are no private shareholders in a position to absorb anything. Both
readings must travel together, and the honest statement of the result is that **the agency
book converts 85 to 89 percent of a wage shock into a public exposure at small doses, without
triggering the statutory backstop at any dose this engine can reach.**

## 7. Does "about 30 percent of GSE net worth" stand, fall or move?

**It moves, and its meaning changes.** Claim 148 read: "29.7 percent of GSE net worth at a
25 percent cognitive dose". Reconstructed, that figure was the **gross** GSE loss of 56.6bn
over net worth of 190.436bn, struck before any transfer at all. The waterfall never touched
it.

Recomputed at the same point, the 25 percent cognitive dose:

| | bn | pct of net worth 179.4 | pct of net worth 190.4 |
|---|---|---|---|
| gross GSE loss, low end | 23.90 | 13.3 | 12.5 |
| gross GSE loss, high end | 58.30 | 32.5 | 30.6 |
| **retained after rebuilt cover, low end** | **21.36 to 22.47** | **11.9 to 12.5** | 11.2 to 11.8 |
| **retained after rebuilt cover, high end** | **45.72 to 52.42** | **25.5 to 29.2** | 24.0 to 27.5 |

The verdict, stated plainly:

- **It does not fall to zero.** The replicator's zero was the `beyond` term, which was never
  the published quantity.
- **It does not stand as published.** The published 29.7 percent was a gross loss over net
  worth with no risk transfer applied, and it was the single high-end cell of a range.
- **It moves down and widens to a range: the retained agency loss at a 25 percent cognitive
  dose is 11.9 to 29.2 percent of combined Enterprise net worth.** The top of that range is
  close to the old point figure, which is why the old number was not obviously wrong, but it
  is the top of a range that reaches down to about 12 percent, and it is now a retained loss
  rather than a gross one.
- **The headline should be the 10 percent dose, which is inside the data: 3.3 to 12.5
  percent of Enterprise net worth, zero Treasury draw.**

## 8. Limitations that travel with this result

1. **First round only.** The engine holds house prices fixed. Agency credit losses are driven
   by negative equity at least as much as by income, so this is a lower bound on GSE losses,
   and the standing lower-bound paragraph attached to A75 to A77 applies here in full.
2. **The overlap split is an assumption**, not a disclosure. It is bounded and the pro-rata
   and SDQ-weighted variants bracket the answer, but neither Enterprise discloses which pairs
   of enhancements overlap.
3. **CRT attachment is a filing example, not a portfolio average.** Fannie gives 0.75 percent
   and 4.0 percent as examples and says explicitly that both vary by transaction. The
   outstanding band width is measured, the attachment point is not.
4. **Multifamily is out of scope here.** These are single-family books only.
5. **FHA is unchanged** and remains flagged: hud.gov returns HTTP 403 on every route, so the
   MMI Fund figures are secondary and are recorded in `lit/unverified.md`.

# Session 2: the Fed question, and the two alternative series

> **NOTE ADDED 2026-09-25.** Every share in this document is arithmetically correct, but see
> `framework/paper3_scoping/K4_RESULT.md`: share changes here are dominated by denominator
> growth (the labour-backed stock grew ×2.56 over 2007–2025, Treasury ×5.60), and share
> changes must not be read as statements about behaviour without the level growth beside them.

**2026-09-22. `PROSPECTUS.md` §7 session 2. Nothing outside `framework/paper2/` was written
and nothing in `framework/labor_backing/` was changed.**

---

## 1. The Fed holdings question: resolved, no double count, no rebuild needed

**Question.** Do central bank holdings of agency securities enter the holder leg *in addition
to* the guarantee on the same pools, double counting the underlying mortgages?

**Answer: no, and the construction makes it impossible.**

`build_direct.holder_shares()` allocates each dollar of a claim class across **Z.1 sectors**,
normalised against the all-sectors control total, so the shares sum to exactly 1. It is a
partition, not a sum of overlapping exposures. `HOLDER_OF_SECTOR` then maps sector 40 (GSEs),
41 (agency and GSE pools), 71 (monetary authority) and 31/34/36 to `federal_government`.

The Fed cannot be double counted against the pools because **it does not hold mortgages**. In
Z.1 the pool (sector 41) is the holder of the mortgage; the Fed holds agency *securities*,
which are claims on the pool and a different instrument — one that is not a claim class here
and never enters the holder matrix.

**Verified numerically:**

| | |
|---|---|
| Home mortgage class total | $13,788.3bn |
| Federal holder share | 0.6493 |
| Implied federal holding | **$8,952.6bn** |
| Agency and GSE pool holdings of home mortgages, Z.1 2025 | **about $9.0tn** |
| Federal Reserve agency MBS holdings, 2025 | about $2.2tn |

The measured federal holding matches the pools alone. Had the Fed's agency MBS been added on
top, the share would be about **(9.0 + 2.2) / 13.79 = 0.81**, not 0.65. Holder shares sum to
1.0000 for every class.

**Where the Fed does enter is Treasury**, and that overlap *is* netted: the union is
`holder + obligor − overlap`, with the overlap taken on the Treasury class. The accounts' own
robustness table confirms the netting works — the entry "central bank NOT federal (Fed
Treasury holdings out of the held-or-guaranteed leg)" moves the union by **exactly 0.000000**,
because those holdings are already inside the obligor leg.

**Consequence for `PROSPECTUS.md` §3: none.** The 2013–2021 rise and the 2021 peak of 0.407
stand unchanged. They are not an artefact of counting QE twice.

## 2. The rebuild reproduces the accounts exactly

Before building anything new, the central series was rebuilt from the Z.1 cache through the
accounts' own loaders.

**Maximum absolute difference against `direct_ratio_timeseries.csv`: 0.000000.**

Reaching that required following four details of `build_direct.py` that are easy to miss and
that a first attempt got wrong, producing errors up to 0.044: the holder lookup uses
`CLASS_HOLDER_INSTRUMENT` rather than the class's own instrument; consumer credit
(instrument 3066000) carries a federal share of **zero**; student loans are overridden by the
federal government's direct holding `FL313066220`; and the union's overlap is netted on
**Treasury only**, not on every federally-obliged class. All four are now matched.

## 3. The kill test: does the one-step rule change the shape?

Series compared from **1959**, the first year the B2 indirect coefficient exists; before that
the two coincide by construction.

| Test | Result |
|---|---|
| Levels correlation | **+0.973** |
| Year-on-year changes correlation | **+0.695** |
| Level gap: mean / sd / range | **+0.194 / 0.058 / +0.117 to +0.338** |

A pure level shift would show a constant gap. **The gap varies by roughly ±30 percent of its
mean, so this is not only a level shift.**

**Phase decomposition under both rules:**

| | Central | Second round |
|---|---|---|
| Guarantee phase 1965→2000 | +0.2536 | +0.1374 |
| Borrowing phase 2007→2025 | +0.2925 | +0.1342 |
| **Last twelve years 2013→2025** | **+0.0900** | **+0.0002** |

**The U-shape survives**: trough 1965 under the central rule, 1968 under the second-round
rule; both rise to 2025.

**The orthogonality — which is the thesis — survives and sharpens:**

| Rule | Guarantee phase | Borrowing phase |
|---|---|---|
| Central | holder **+0.2408** vs obligor +0.0109 (**22.1×**) | holder +0.0172 vs obligor **+0.3127** |
| Second round | holder **+0.1342** vs obligor +0.0012 (**114.5×**) | holder **−0.0106** vs obligor **+0.1636** |

Under the second-round rule the guarantee phase is *more* purely a holder-leg phenomenon, and
the borrowing phase has a holder leg that is outright negative.

### Verdict on the kill, and the judgement call in it

**The kill does not fire on the thesis. It fires on one subsidiary claim.**

- **Robust to the one-step rule:** the U-shape; two phases; each phase moving one leg; the
  direction and broad trajectory.
- **Not robust:** that absorption *continued through 2013–2025*. Central says +0.090;
  second-round says +0.0002, flat.

**This is a judgement call and it is flagged as one.** A strict reading of "changes the shape
of the series" would fire the kill, because the gap is not constant and the last segment
behaves differently. The reading taken here is that "shape" means the features the thesis
rests on, which the prospectus defined as the two-phase orthogonal structure, and those are
robust — more so under the second-round rule than under the central one.

**The owner can overrule this and stop.** If the call is that any shape change kills, the
stop rule applies and the note gets written instead. What the paper may **not** do either way
is claim post-2013 continuation without stating that it is conditional on the one-step rule.

## 4. Both classifications, for the whole series

| Year | Central | Agency pools not federal | Difference |
|---|---|---|---|
| 1947 | 0.6958 | 0.6916 | 0.0041 |
| 1965 | 0.3081 | 0.2934 | 0.0147 |
| 1980 | 0.3816 | 0.2835 | 0.0982 |
| 1990 | 0.5638 | 0.3648 | 0.1990 |
| 2000 | 0.5617 | 0.3048 | 0.2569 |
| 2007 | 0.5011 | 0.2460 | 0.2550 |
| **2008** | 0.5582 | 0.2932 | **0.2650** |
| 2010 | 0.6492 | 0.3823 | 0.2669 |
| 2013 | 0.7036 | 0.4480 | 0.2556 |
| 2021 | 0.7779 | 0.5502 | 0.2277 |
| 2025 | 0.7936 | 0.5865 | 0.2071 |

**The difference is the stock of agency-guaranteed claims**, expressed as a share of the
labour-backed claim stock. It is a quantity of claims, not a price. It peaks at **0.2814 in
2003** and has declined since to 0.2071.

**It is not the value of the implicit guarantee and must never be described that way.** The
prospectus called it "the market value of an implicit guarantee" and that was wrong: a stock
of claims that a classification moves from one column to another is not a valuation of
anything, and nothing here prices a guarantee. **`PROSPECTUS.md` §4 is corrected by this
document.**

**On 2008.** September 2008 is the date the difference stopped being treated as open: the
conservatorship placed Fannie Mae and Freddie Mac under FHFA and the Treasury's support
agreements made the federal position explicit. That is a statement about how the claims were
*classified and treated* from that date, not a measurement of what the guarantee was worth
before it. The series does not jump at 2008 — the difference is 0.2550 in 2007 and 0.2650 in
2008 — and the paper should not imply that it does.

## 5. Divergence test re-run on the rebuilt holder leg

The holder leg needed no correction, so the session 1 result stands, now confirmed on the
rebuilt series:

| | |
|---|---|
| Levels correlation with the public GSE share of mortgages | **+0.7006** |
| **Year-on-year changes** | **+0.0930** |

Unchanged to four decimals. The holder leg is not reducible to two public FRED series.

## 6. What session 3 must do

1. **Decompose the holder leg by programme** — GSE pools, Ginnie, federal direct student
   lending, Federal Reserve — as session 1 required. The 2013–2025 divergence between the
   central and second-round series is probably a composition story and should be shown as one.
2. Carry **both classifications and both backing rules** through every exhibit, not as
   robustness but as columns.
3. The counterfactual decomposition of the 2025 level.

## 7. Files

| File | Contents |
|---|---|
| `s2_build_series.py` | the builder; reproduces the accounts exactly before diverging |
| `s2_panel.csv` | per-class, per-year panel, 1,027 rows, 1947–2025 |
| `s2_series.csv` | all three series with both legs |
| `s2_meta.json` | rebuild check |

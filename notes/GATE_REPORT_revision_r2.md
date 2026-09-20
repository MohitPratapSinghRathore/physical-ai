# Gate report, revision round 2

New work in `framework/revision_r2/`, released to `data/release/revision_r2/`. Every
specification was stated before computing; the plausibility bounds are listed first for each
module and are asserted in code.

---

## PLAUSIBILITY BOUNDS, STATED AND CHECKED

**B2, the backing basis.** Both the coverage share and the wage share lie in [0, 1] for every
class; the per-household wage ratio is clipped to [0, 1] before weighting; the wage share is
computed only over households with positive income and a positive balance. All asserted.

**B2, the headline effect.** Every rebuilt ratio stays in [0, 1]; the debt-only ratio exceeds
the all-claims ratio under both coefficient sets; the federal creditor and debtor parts each
stay below the union and the union below their sum. All asserted.

**Part C.** Every rate in [0, 1]; the federal-only assembled rate must be below the
all-government rate, since removing a tax cannot raise the total; the federal-only required
band must be below the all-government band; the value of g at which the condition closes must
be positive. All asserted.

---

## THESIS-WEAKENING RESULTS

### 1. The published comparison mixed jurisdictions (C1)

The labor tax readings are federal: both are built from federal taxes on wages. The assembled
capital rate adds an effective state corporate tax. The published comparison therefore set a
federal-plus-state capital rate against a federal-only labor rate.

Rebuilt consistently, both ways:

| | assembled rate | required band |
|---|---|---|
| federal only | **7.8 per cent** | 11.0 to 13.7 per cent |
| all government | 8.5 per cent | **12.4 to 15.1 per cent** |

The gap widens on either version, because the state adds more to the labor side (3.2 points of
the wage bill) than to the capital side. The federal-only version is now the headline, because
the paper's claim is about the federal balance sheet.

### 2. The household backing coefficients measured coverage, not backing (B2)

The four household coefficients are the share of a class's balances owed by, or service paid
by, working-core households. That is who owes, not which income services the debt, and the
paper's own definition asks for the second. Computing the definitional quantity from the
survey income-by-source variables:

| class | coverage basis | wage-share basis | change |
|---|---|---|---|
| home mortgage | 0.840 | 0.810 | -0.030 |
| credit card | 0.740 | 0.730 | -0.010 |
| auto loan | 0.774 | 0.778 | +0.005 |
| student loan | 0.883 | 0.882 | -0.001 |
| other consumer | 0.816 | 0.805 | -0.010 |

**Headline effect, reported before anything else is said about it.** The debt-only direct ratio
moves from 52.2 to 51.6 per cent, the debt-only pair including indirect servicing from 60.2 to
59.7, the all-claims pair from 27.0 and 47.5 to 26.7 and 47.2, and the federal exposure share
from 79.4 to 79.5 per cent. The quintile gradient changes level by a common factor and its
shape, which is what the paper reports, is identical. **No headline changes at the precision
the paper reports**, and the paper now says so and adopts the definitional basis, because
agreement is a fact about these data rather than a justification of the coverage construction.

### 3. Payoffs across the two sides were not payoffs (A1)

The payoff figure and its appendix table subtracted shares of two differently sized and
differently observed pools and called the difference a gain, a loss or an offset. Netting needs
a dollar base on each side. The wage side has one; the AI side does not, since its equity tier
is a swept scenario share and its debt tier a lower bound from filings. Section 8.4 is now a
composition contrast with no netting, and the figure and table are removed rather than
rewritten.

### 4. The upper bound on the federal AI share rests on an assumption (A2)

Omitted AI-side assets have owners too, so the federal share is an upper bound only if the
federal share of the omitted assets does not exceed its share of the observed ones. That
assumption is now stated, with its reason (the omitted financing is private credit,
securitizations and vendor finance) and with the alternative: if the two shares were equal the
federal share of the whole AI side would stay at about one per cent rather than fall below it.

### 5. The steady-state equivalence was asserted, not derived (A3)

The lifetime marginal wedge and an annual revenue rate are comparable only under constant
investment, constant rates and a stationary capital stock, and only then do the numerator and
denominator of the annual rate stand in the same ratio as the wedge. The three conditions are
now stated in the text and the comparison is presented as holding only under them.

### 6. The ownership arithmetic double-counted the existing position (A4)

A federal share of one per cent of a 14,857.4bn pool is already about 148.6bn. Taking it to ten
per cent means holding 1,485.7bn, so the purchase required is the difference, **1,337.2bn**,
not the whole position. That is about seven times the capital of the housing agencies rather
than eight. The claim that ownership is the only instrument left at near-total displacement is
replaced by the qualified wording already used in the appendix.

---

## WHAT ELSE CHANGED

**A5.** The capital tax trigger no longer says "both sides observed today"; it describes the
status of the components on each side.

**A6.** Pass shares are now described wherever they appear as the share of a stated grid with
stated ranges and uniform weighting, not as a probability. They do not appear in the abstract
or the conclusion.

**C2.** Each assumption that could close the gap, applied on the all-government version:
withholding at a 15 per cent treaty rate gives 9.3 per cent, the filers' own debt share gives
9.2, both together 10.1, against a required 12.4. Labor tax rates matched to the earnings of
the displaced run from 23.7 per cent at the bottom of the wage distribution to 29.7 at the top,
so displacement concentrated in the bottom quintile would require 10.2 per cent, still above
the assembled rate on either jurisdiction.

**C3 and C4.** The condition closes at the assembled rate only where taxable capital income per
displaced wage dollar reaches 1.4 to 1.7 on a federal basis, 1.5 to 1.8 on an all-government
basis, all of it above the output-preserved ceiling of one.
Section 5 now leads with that boundary rather than with a central estimate, and the boundary
figure replaces the removed payoff figure.

**B1.** A thirteen-row table gives the numerator, denominator, source, proxy assumption and
alternative estimate for every class, with the consolidation rule stated: claims are assigned
to the party bearing the credit risk rather than the holder of legal title.

---

## THE ABSTRACT AS IT NOW READS

Wage-dependent public revenues and credit guarantees concentrate automation exposure on the
federal balance sheet, while household and lender outcomes vary with income, debt composition
and how displacement arrives. Labor backing accounts decompose US financial claims by the income
that services each and by who holds it. About 52 per cent of US debt, public and private, is
serviced directly from wages, 60 per cent including indirect servicing. Counting the federal
government as exposed when it is holder, guarantor or debtor, it is exposed on about 79 per cent
of directly wage-backed claims; on the separately measured claims on AI capital, a lower bound
from company filings, its share is about 1 per cent. Three results support this. On a
consistently federal basis the rate on income shifting from wages to AI capital is 7.8 per cent
against the 11.0 to 13.7 per cent replacement requires, and the condition closes only where
taxable capital income per displaced wage dollar reaches 1.4 to 1.7, beyond what
output-preserving displacement generates. A conditional stress test puts the first-round burden
on the public sector and on households with thin buffers. And household relief removes between
9.6 and 62.2 per cent of bank losses, depending on whether income replacement feeds back into
spending.

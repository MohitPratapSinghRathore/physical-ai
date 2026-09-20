# Replication brief addendum: the debt-only labour backing ratio

Standalone. You need nothing from the main brief except the thirteen claim classes and their
labour backing shares, both reproduced here. Sealed expected values are in
`notes/sealed/sealed_debt_only_ratio.json`. **Do not open it until your rebuild is written
down.** Run in an empty folder.

---

## 1. What the statistic is

**What share of US debt is serviced directly out of wages?**

The labour backing ratio decomposes all financial claims by the income that services them.
The published version puts **all** claims in the denominator, including corporate equity at
market value. That makes it partly an asset-price series: it read **0.2705 at the 2000 equity
peak and 0.3772 in 2008 after the crash**, so a reader would have called the economy least
risky in 2000 and most risky in 2009. **The debt-only ratio removes market-valued equity from
the denominator**, leaving claims carried at par or amortised cost, so the series measures
composition rather than valuation.

Two variants, on the same first-round versus second-round boundary the sovereign share uses:

- **DIRECT.** Only claims that wages pay directly.
- **INCLUDING INDIRECT.** Business-revenue-serviced classes additionally carry the measured
  indirect labour share, that is, wages become spending and spending becomes business revenue.

## 2. The classes EXCLUDED from the debt-only denominator

The exclusion rule is by **valuation basis**, not by name: any class carried at market value
as an equity claim is excluded, so a future equity class is caught automatically.

| class | Z.1 series | 2025 level bn | why excluded |
|---|---|---|---|
| `corporate_equity` | **LM103164105** | 71,994.9 | corporate equity at MARKET VALUE. It is 48.19 percent of the all-claims denominator |

It is the only such class in the thirteen-class table. Note the `LM` prefix: Z.1 uses `LM` for
market-value levels and `FL` for book-value ones, which is itself the signal.

## 3. The twelve classes that REMAIN in the debt-only denominator

Annual, Z.1, latest complete year **2025**.

| # | class | Z.1 liability series | level bn | labour backing |
|---|---|---|---|---|
| 1 | home_mortgage | FL153165105 | 13,788.3 | 0.840223 |
| 2 | credit_card | FL153166100 | 1,324.3 | 0.740 |
| 3 | auto_loan | FL153166400 | 1,562.2 | 0.7737 |
| 4 | student_loan | FL153166220 | 1,834.7 | 0.8832 |
| 5 | other_consumer | FL153166205 | 377.6 | 0.815554 |
| 6 | multifamily_mortgage | FL103165405 + FL113165405 + FL313165403 | 2,448.7 | 0.72754 |
| 7 | treasury | FL313161105 + FL313169205 | 33,887.1 | 0.657788 |
| 8 | state_local_debt | FL213162005 + FL213168003 + FL214141005 | 3,803.9 | 0.159338 |
| 9 | corporate_bonds | FL103163005 | 8,075.3 | **0 by rule** |
| 10 | corporate_loans | FL103168005 + FL103169005 + FL103169100 | 3,903.7 | **0 by rule** |
| 11 | noncorporate_business_debt | FL113168005 + FL113169005 + FL113169535 + FL113167205 | 2,453.0 | **0 by rule** |
| 12 | commercial_mortgage | FL103165505 + FL113165505 + FL163165505 | 3,953.4 | **0 by rule** |

**Government debt enters through the labour-linked share of the receipts that service it**,
which is what the 0.657788 and 0.159338 are. Treasury debt is not "wage-backed" because a
household owes it; it is wage-backed to the extent that wage taxes pay it.

**The zero-by-rule classes** (9 to 12) are serviced from business revenue. In the DIRECT
variant they carry zero. In the INCLUDING INDIRECT variant they carry the measured indirect
labour share of business revenue.

## 4. The arithmetic

    debt_denominator(y) = sum of the twelve class levels in year y
    labour_backed(y)    = sum over those twelve of level x backing
    DEBT_ONLY_direct(y) = labour_backed(y) / debt_denominator(y)

    INCLUDING INDIRECT adds, for classes 9 to 12 only:
        + level x indirect_labour_share_of_business_revenue

Build it for every year from **1952 to 2025**, taking the annual (Q4) observation of each
series. Report the coefficient of variation of the direct series over that window, and the
same for the all-claims comparator.

## 5. The structural bound, which you should check before you check anything else

> **DEBT_ONLY_direct(y) must be greater than or equal to all_claims_direct(y) in EVERY year.**

Removing from the denominator a class whose labour backing is zero cannot lower the ratio.
Corporate equity is zero by rule, so excluding it must raise the ratio or leave it unchanged.
**If your rebuild violates this, the error is in your class list, not in the data**, and no
other check will tell you that as quickly.

Two further bounds: every ratio lies in **[0, 1]**, and the debt-only denominator is never
larger than the all-claims one.

## 6. What to report

1. The 2025 pair, direct and including indirect.
2. The 2000 and 2008 direct readings, for both the debt-only and the all-claims series, so
   the asset-price problem is visible.
3. The 1952 direct reading.
4. The equity share of the all-claims denominator in 2025.
5. The coefficient of variation of both series over 1952 to 2025.
6. Sensitivity of the debt-only direct ratio to each named judgement call, one at a time.

**The judgement call that matters.** The **one-step rule**, whether classes 9 to 12 take zero
or the indirect share, is the largest judgement in this project. It moves the **all-claims**
ratio by about 76 percent. Report what it does to the debt-only ratio: if you get a much
smaller number, that is the point of the statistic and not an error.

## 7. What to attack

- **The zero-by-rule classes.** If you think commercial mortgage belongs with multifamily
  rather than with business debt, say so and show the effect; it is one of the listed calls.
- **Whether excluding equity is the right correction.** An alternative is to keep equity but
  at book value. We did not do that; argue it if you think it is better.
- **The Treasury backing share.** It is the labour-linked share of federal receipts and is
  itself a bound, not a point: realised capital gains sit inside AGI and bear preferential
  rates, so the share is **0.634 to 0.653** on 2023 SOI data. We publish the lower end.

## 8. Status

**MEASURED, PROVISIONAL.** New construction, not previously rebuilt by anyone. Code is
`framework/labor_backing/build_debt_only.py` and you should not read it.

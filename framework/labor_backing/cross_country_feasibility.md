# B6. Cross-country feasibility for the labour backing ratio

**PROVISIONAL. FEASIBILITY ONLY. No ratio is computed for any country other than the
United States in this session, and none should be quoted.** This assesses which of the
three required inputs exists where, and what is missing. It supersedes the coverage table
in `_unreviewed/feasibility.md` section 4 for the five economies the owner named, and it
drops Canada and Brazil, which that table covered and this instruction does not.

## What the computation needs

The direct ratio (B1) needs three things per country, and the third is the binding one:

1. **Financial accounts by claim class**, to get the liability side by instrument.
2. **A holder or whom-to-whom matrix**, to get B3.
3. **A labour decomposition of the servicing cash flow**: a household survey carrying
   income type alongside debt service or balances, and a revenue split by tax base.

The United States is the best case and even there the third input is the weak one: the
SOI wage share of AGI exists for three years and is held constant outside them.

## The five economies

| Economy | 1. Financial accounts by claim class | 2. Holder or whom-to-whom | 3. Labour decomposition | Verdict |
|---|---|---|---|---|
| **Euro area** | **Strong.** ECB Euro Area Accounts, quarterly sector accounts on the ESA 2010 framework, by instrument | **Strong, and in some respects better than the US.** The ECB publishes euro area whom-to-whom tables for loans, debt securities and equity | **Adequate.** The Household Finance and Consumption Survey (HFCS) carries income type, debt and assets on a harmonised basis across countries. Revenue split from OECD Revenue Statistics | **Computable.** The closest to a second full case. The cost is that HFCS waves are infrequent, so the labour shares would be held constant between waves, which is the same limitation the US has with SOI |
| **United Kingdom** | **Strong.** ONS flow of funds, now on an experimental whom-to-whom basis | **Partial.** The ONS whom-to-whom work is newer and less complete than the ECB's, especially before 1997 | **Adequate.** Wealth and Assets Survey carries income type and debt. OECD Revenue Statistics for the tax split | **Computable, shorter series.** A 1952 start is not available; a defensible series starts in the late 1990s |
| **Japan** | **Strong.** Bank of Japan Flow of Funds Accounts, long series, by instrument and sector | **Strong.** The BOJ publishes sector-by-sector asset and liability tables | **WEAK, and this is the binding constraint.** The National Survey of Family Income and Expenditure is infrequent and access is harder. The household debt stock is also small relative to government debt, so the ratio would be dominated by the JGB cell and therefore by the revenue split rather than by any survey | **Computable but uninformative in the same way.** Worth doing precisely because the composition is so different from the US |
| **Korea** | **Adequate.** Bank of Korea flow of funds on the SNA framework | **Partial.** Sector tables exist; a full whom-to-whom matrix is less accessible | **Adequate to weak.** The Survey of Household Finances and Living Conditions carries income and debt. Household debt is very high relative to income, so the household cells dominate and the survey quality matters more than anywhere else on this list | **Computable with effort.** The most interesting case after the US, because the household leg is the largest |
| **India** | **WEAK.** RBI publishes flow of funds but with long lags, coarser instrument detail and incomplete coverage of the household sector | **Largely absent.** No usable whom-to-whom matrix | **WEAK.** High informality means a large share of labour income sits outside both the tax base and the formal credit system, which is exactly the variable the statistic turns on. All-India Debt and Investment Survey is infrequent | **NOT computable to a publishable standard.** The honest output for India is a statement about why, not a number |

## The point that matters more than the data availability

**A sovereign that cannot borrow freely in its own currency cannot absorb the shock the way
the United States can, and the labour backing ratio does not capture that by itself.**

The ratio measures how much of the claim stock sits on labour income. It says nothing about
what happens when that income falls. In the US case the answer is that the sovereign
absorbs it, and the B3 result is that the federal government holds, guarantees or owes
about four fifths of the labour-backed stock. That absorption is possible because the
issuer borrows in a currency it issues.

For an issuer that does not, the same ratio carries a different meaning:

- The **obligor leg** of the sovereign share, which is the larger of the two legs in the US
  at 0.543 against 0.326, is not an absorbing capacity at all. It is a refinancing
  requirement.
- This project has already measured the difference and it is smaller than the level paths
  suggested: claim 170, the displacement increment to debt is 10.1 points of GDP for a
  reserve-currency issuer at a 10 percent dose over twenty years against 18.2 for an
  emerging market, a factor of 1.8.
- And claim 171 still governs the reading: **the emerging-market issuer is on an
  unsustainable debt path before any displacement arrives, and that clause matters more
  than the displacement increment.**

So the cross-country extension should not be presented as "the same statistic in five
countries". **The statistic is comparable; the absorbing capacity behind it is not.** Any
cross-country table must carry the currency-denomination status of the sovereign in the
same table, or it will be read as implying a comparability that does not exist.

## Recommendation

Do the euro area second and Korea third, and report India as a measurement-impossibility
result rather than attempting a number. Japan is worth doing for composition contrast.
The United Kingdom adds the least per unit of effort because it is structurally similar to
the US with a shorter series.

**None of this is started. This is a feasibility note and nothing in it is a result.**

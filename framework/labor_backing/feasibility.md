# The labour backing ratio: feasibility assessment

**PROVISIONAL throughout.** Nothing here is a result. This is an assessment of whether a
system-wide labour backing statistic is new, computable, and worth computing. No existing
analysis was changed.

---

## 1. Novelty check. The gate is passed, but narrowly and with a caveat

**Question:** has anyone measured, system-wide, the share of financial claims ultimately
serviced from labour income?

**Answer: no such statistic was located.** Three adjacent literatures exist and none of them
computes it.

### (a) Human wealth and housing collateral

Lustig and Van Nieuwerburgh, and Lustig, Van Nieuwerburgh and Verdelhan, measure HUMAN
WEALTH: the present value of the labour income stream, discounted with the same stochastic
discount factor that prices traded assets. Their central object is the RATIO OF HOUSING
WEALTH TO HUMAN WEALTH, used to predict asset returns and to measure the collateral capacity
of housing.

**This is the mirror image of the proposed statistic, not the same thing.** They ask what
labour income is worth as an asset. The proposed ratio asks what share of the liability side
is serviced out of labour income. A high human-wealth economy could have a low labour backing
ratio if claims are serviced from capital income, and vice versa.

### (b) Debt service ratios, BIS and Federal Reserve

The BIS Debt Service Ratio database covers households, non-financial corporations and the
total private non-financial sector across seventeen economies on a unified methodology, and
the Federal Reserve publishes the US household DSR. The ratio is interest plus amortisation
over income.

**Two reasons this is not the proposed statistic.** First, the denominator is ALL income:
BIS documentation is explicit that "many components of income are included, such as labour
income, self-employment income and capital income". There is no labour decomposition.
Second, the coverage is the private non-financial sector only. Treasury debt, state and local
debt, agency pools, corporate bonds, equities and pension reserves, which are most of the
claim stock, are outside it entirely.

### (c) Whom-to-whom financial accounts

The Financial Accounts of the United States and the equivalent OECD tables trace WHO HOLDS
whose claims. They do not trace WHAT CASH FLOW SERVICES them. The sectoral counterparty is
recorded; the income type funding the payment is not.

### The caveat on this gate, and it is a real one

**The search was not systematic.** `lit/protocol.md` governs a different question and was
not re-run. The claim is "none located", not "none exists". A statistic this simple to state
has probably been computed inside a central bank without being published as such, and the
national accounts community has thought carefully about sectoral income sources for decades.
Before this becomes a paper claim it needs a systematic search and a direct approach to the
Federal Reserve Financial Accounts team.

**Thesis-weakening note.** If the statistic turns out to exist in a working paper or a
central bank annex, the contribution collapses to the AI application, which is the part
already in hand. The novelty of the ratio itself should not be load-bearing.

---

## 2. Definition, with every judgement call named

**Proposed rule.** For each class of financial claim, the labour backing share is the
fraction of its servicing cash flow that originates as labour income, traced through at most
one intermediary.

"At most one intermediary" is the key restriction and it is a judgement call, not a
principle. Trace further and everything terminates in labour eventually, because capital
income is itself a claim on output produced by labour and capital jointly, and the ratio
becomes uninformative. Trace no intermediaries and it collapses to household debt. **The
one-step rule is what makes the statistic finite and it is the single largest thing to argue
about.**

| Claim class | Tracing rule, one or two sentences | Lower | Central | Upper |
|---|---|---|---|---|
| Home mortgages | Serviced from household income. The labour share is the share of mortgage service paid by households with a prime-age employed member. **Repo result A47: 84.0 percent sits with working-core households, 16.0 percent with non-working.** | 0.70 | **0.84** | 0.90 |
| Consumer credit | Same rule as mortgages, applied to consumer balances. Younger and lower-income skew implies a higher labour share than mortgages. | 0.80 | **0.90** | 0.95 |
| Multifamily mortgages | Serviced from rent, which is paid by tenants. **Repo result A47: 72.8 percent of rent is paid by working-core households.** One intermediary: tenant to landlord to lender. | 0.65 | **0.73** | 0.80 |
| Treasury debt | Serviced from federal receipts. The labour share is the labour-linked share of receipts. **Repo result A8, corrected: the earlier 77.7 percent was overstated; the corrected split from SOI and NIPA is the one to use.** | 0.55 | **0.65** | 0.75 |
| State and local debt | Serviced from state and local receipts, which lean more on sales and property taxes. Sales tax is consumption out of labour income at one remove; property tax is a capital levy. | 0.40 | **0.50** | 0.60 |
| Agency and GSE debt and pools | Pass-through of the underlying mortgages. Inherits the home and multifamily mortgage shares by composition. | 0.70 | **0.82** | 0.88 |
| Corporate bonds and loans | Serviced from corporate operating cash flow, which is revenue minus costs. Revenue is consumption and investment demand; the labour share of final demand funding it is the tracing quantity. **This is the weakest cell and the one most exposed to the one-step rule.** | 0.30 | **0.50** | 0.65 |
| Equities | Serviced from residual corporate cash flow. Same problem as corporate debt, with the residual claim making it worse. | 0.25 | **0.45** | 0.60 |
| Pension and insurance reserves | Funded from contributions, which are overwhelmingly payroll-linked, and from investment returns on the accumulated stock. **Repo result A32: payroll is 91.3 percent of OASDI trust fund income.** Private pensions differ. | 0.55 | **0.70** | 0.85 |

**Judgement calls, stated so they can be attacked:**

1. The one-step tracing rule. Everything below depends on it.
2. Whether self-employment income counts as labour. It is mixed by construction. Central
   treats it as labour; the lower variant excludes it.
3. Whether transfer income counts as labour-backed. OASDI is payroll-funded, so the central
   case treats pension and social insurance receipts as labour-backed at the payroll share.
   **This is where A43's double-counting warning bites: the same payroll dollar must not
   back both the Treasury claim and the pension claim.**
4. Sales tax as labour income at one remove. Defensible, contestable.
5. Corporate and equity cells are close to arbitrary within their ranges. They are also the
   largest claim classes, which is the problem in section 5.

---

## 3. First computation: feasible now for the liability side, not yet for the ratio

Claim-class levels are already in the repository from the Financial Accounts via FRED. Levels
retrieved 2026-09-19:

| Series | Level | Date |
|---|---|---|
| Household debt securities and loans (CMDEBT) | 21,377,787 | 2026-04-01 |
| Home mortgages, one to four family (HHMSDODNS) | 14,010,942 | 2026-04-01 |
| Consumer credit (TOTALSL) | 5,186,204 | 2026-07-01 |
| Federal debt (GFDEBTN) | 39,065,421 | 2026-01-01 |
| State and local debt (SLGSDODNS) | 3,819,096 | 2026-04-01 |
| Nonfinancial corporate debt securities (NCBDBIQ027S) | 9,190,040 | 2026-04-01 |

**UNITS ARE NOT ASSERTED HERE.** Decision D1 requires units be read from the provider per
series. CMDEBT and HHMSDODNS were verified earlier as millions of dollars. The others were
not verified in this session and must be before any arithmetic. The multifamily series
attempted (MDOTP1T4FR) last updated 2019 and appears discontinued; a replacement must be
found.

**What is missing to compute the ratio itself, not the levels:** the servicing CASH FLOW by
claim class, not the stock. Interest plus amortisation by class is available for households
(Federal Reserve DSR) and for federal debt (Treasury interest outlays), but not uniformly for
corporate, state and local, or agency claims. **The honest status is that the liability side
is assembled and the flow side is not.**

**By holder class** (banks, GSEs and agency pools, insurers, pensions, households, rest of
world, government): the Financial Accounts whom-to-whom tables support this directly and it
is the most tractable extension. This project already has the Chicago Fed bank-side figures
and Z.1 holder shares from earlier sessions.

**Time series feasibility from the 1950s.** The Financial Accounts begin in 1945 and the
claim-class levels go back that far. The LABOUR SHARES do not: A47's working-core split needs
ACS microdata (2000s onward, or decennial census before that), and the corrected receipts
split needs SOI detail. A defensible series probably starts in 1989 with the Survey of
Consumer Finances triennial, or 2000 with ACS. **A 1950s series would require holding the
labour shares constant at modern values, which would make the series a rescaled claim stock
and not a measurement.**

---

## 4. Cross-country feasibility

The computation needs, per country: financial accounts by claim class and holder; a
household survey with income type and debt service; and revenue statistics split by tax base.

| Economy | Financial accounts | Household survey | Revenue split | Verdict |
|---|---|---|---|---|
| United States | Z.1, whom-to-whom | ACS, SCF, SIPP | SOI, NIPA | Best case, already partly done |
| Euro area | ECB accounts, whom-to-whom | HFCS | OECD Revenue Statistics | Strong; HFCS is the Meriküll and Rõõm dataset |
| United Kingdom | ONS flow of funds | Wealth and Assets Survey | OECD | Strong |
| Japan | BOJ flow of funds | National Survey of Family Income | OECD | Good, survey access harder |
| Canada | StatCan national balance sheet | Survey of Financial Security | OECD | Good |
| **Emerging market: Brazil or Mexico** | IMF Financial Soundness Indicators, partial accounts | Household budget surveys | OECD Revenue Statistics covers both | **Weakest. Whom-to-whom is incomplete and informality makes the labour share of income hard to measure, which is exactly the variable the statistic turns on** |

**The emerging market case is where the statistic would be most interesting and least
computable**, because high informality means a large share of labour income is outside both
the tax base and the formal credit system. That is a finding in itself but it is not the one
the exercise is designed to produce.

---

## 5. One page: is it new, is it computable, how sensitive, what would it say

**Is it new?** Probably, with the caveat in section 1. The human-wealth literature measures
the asset side, the BIS DSR measures the private non-financial sector with an undifferentiated
income denominator, and whom-to-whom accounts trace holders not cash flows. A systematic
search and a direct approach to the Financial Accounts team are needed before claiming it.

**Is it computable?** The liability side, yes, now. The ratio, partly: household and federal
cells rest on results this project already has (A47, A8, A32) and are defensible. The
corporate and equity cells are not computable to a standard worth publishing, and they are
the largest classes.

**How sensitive is it to the judgement calls?** Very, and asymmetrically. The household and
federal cells have ranges of about 0.20 around their centres. The corporate and equity cells
have ranges of 0.35, and they carry the most weight. **A plausible aggregate ratio therefore
spans roughly 0.45 to 0.75 before any data work, which is wide enough that the headline
number would be an artifact of the corporate assumption.** The one-step tracing rule alone
could move it further than that.

**What would it say that the current paper cannot?** One thing, and it is worth having.
The current paper measures what happens to households and to the public budget when labour
income falls. **The labour backing ratio would say how much of the entire claim stock sits
on that income, which converts a household-level finding into a system-level exposure
number that a supervisor can put next to a capital ratio.** It would also make the paper's
central asymmetry quantitative: Leg A is 2.1 percent of Leg W by stock (A45), but the
relevant comparison is Leg A against the LABOUR-BACKED portion of all claims, which is a
different and larger-sounding denominator.

**Recommendation, provisional.** Compute and publish the ratio for the household and
government cells only, where the repository already has defensible shares, and report the
corporate and equity cells as an explicitly unresolved residual with a stated range rather
than folding them into a headline. A ratio that covers 40 percent of the claim stock and says
so is worth more than one that covers 100 percent by assumption.

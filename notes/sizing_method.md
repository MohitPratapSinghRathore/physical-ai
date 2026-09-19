# Sizing method

How Leg W and Leg A are measured, what each number is and is not, and where the
definitional risk sits. United States only so far.

Last updated 2026-09-19.

---

## Leg W

Straightforward, because official statistics already define it. Household liabilities come
from the Federal Reserve Z.1 Financial Accounts via FRED; the sovereign component from
Treasury total public debt; the labor-tax base from BEA NIPA.

The only judgement calls:

1. **Household and federal debt are reported separately** (decision D3). They are claims on
   the wage bill through different mechanisms and are held by different sectors. The sum is
   a memo line.
2. **Labor-linked receipts** are federal personal current taxes plus federal contributions
   for government social insurance, over federal CURRENT receipts. NIPA books social
   insurance contributions outside "current tax receipts", so using tax receipts as the
   denominator gives an impossible 125 percent (decision D2).
3. Units are taken from the provider at fetch time, not asserted (decision D1).

Leg W is not where the measurement risk in this paper lies.

---

## Leg A

There is no official statistical category for "AI-linked credit". Constructing one is part
of the contribution, and it is also the largest single source of criticism the paper will
attract. The definition is tiered so that no estimate is ever blended into a hard-data
total.

| Tier | Content | Evidence quality | Status |
|---|---|---|---|
| 1 | Debt issued explicitly against AI assets: GPU-backed lending, data-centre ABS and CMBS, robotics fleet finance | hard, but narrow and hard to enumerate | NOT BUILT |
| 2 | Capex and balance sheets of hyperscalers, neoclouds, data-centre REITs and robotics firms, from 10-K filings | hard | BUILT |
| 2b | Off-balance-sheet and SPV-financed data-centre debt | estimate, labelled | NOT BUILT (decision D4) |
| 3 | Market capitalisation attributable to AI expectations | speculative | sensitivity only, never in a headline ratio |

### What Tier 2 actually measures

`src/build_lega.py`, 10 firms, latest fiscal year, USD bn:

| | Capex | OCF | Self-funding | Long-term debt | Finance leases |
|---|---|---|---|---|---|
| Total (9 firms with current facts) | 490.9 | 659.1 | 1.34 | 368.1 | 90.2 |

Two biases, in opposite directions, and neither is small:

- **Overstates the AI share.** No filer discloses an AI-attributable capex split. Tier 2
  is TOTAL company capex for firms whose capex is mostly but not entirely AI-driven.
  Amazon's figure includes fulfilment and logistics; Tesla's includes vehicle production.
- **Understates AI-linked debt.** BIS Quarterly Review March 2026 documents that
  data-centre debt is commonly placed in a dedicated vehicle, with the operator holding
  minority equity plus a long-term lease, keeping the debt off the operator's consolidated
  balance sheet. Tier 2 reads the balance sheet the structure was built to keep clean.

Because of the second bias, **the WS1 kill criterion must not be evaluated on Tier 2**
(decision D4). Doing so returns a false verdict, and the direction of the error is known.

### Tag selection is a live methodological risk

Filers use different us-gaap tags for the same quantity, and they change tags over time. A
first build read Amazon capex as 6.7 USD bn (the last year it used
`PaymentsToAcquirePropertyPlantAndEquipment`, 2016) and Equinix capex as 0.01 USD bn from
2010. The correct 2025 figures are 131.8 and 4.3.

The build therefore searches an ordered list of candidate tags per concept and takes the
one with the most recent full fiscal year, and rejects any fact whose fiscal year ends
before `MIN_FY_END` (2024-01-01) rather than reporting a stale value. The chosen tag is
written into `data/processed/legA_tier2.csv` for every cell, so any figure can be traced to
the tag it came from.

Nebius (NBIS) is dropped: as a foreign private issuer it files 20-F, not 10-K, and the
build filters to 10-K. Foreign filers need separate handling before the euro-area and Asia
cases are built.

---

## The headline ratio, and why it is not yet the answer

On Tier 2 alone:

| Comparison | Value |
|---|---|
| Leg A debt and leases / household debt | 2.14% |
| Leg A debt and leases / Leg W broad | 0.76% |
| Leg A debt and leases / GDP | 1.41% |
| Leg A capex / GDP | 1.51% |

2.14 percent is below the brief's 5 percent kill threshold. Read literally, the bet is
lopsided and the "overinvestment bust" scenario would be downgraded from systemic.

That reading is not yet available, for the reason in D4: the measure excludes the financing
structure that BIS identifies as dominant. The honest statement of where this stands is
that **Leg A has been measured only in the place it is least likely to be**, and Tier 1
and 2b must be built before the criterion is evaluated.

## What Tier 2 does establish, independent of the ratio

The self-funding ratio splits the sector cleanly:

| Firm | Self-funding (OCF / capex) |
|---|---|
| Alphabet | 1.80 |
| Tesla | 1.73 |
| Meta | 1.66 |
| Microsoft | 1.58 |
| Amazon | 1.06 |
| Equinix | 0.91 |
| Digital Realty | 0.76 |
| Oracle | 0.57 |
| CoreWeave | 0.30 |

The hyperscalers fund AI capex out of operating cash flow and are not, at the margin,
adding credit exposure. The firms that cannot self-fund (Oracle at 0.57, CoreWeave at 0.30,
and the data-centre REITs) are where Leg A credit risk actually sits.

This matters for the thesis independently of the aggregate size question: Leg A is not a
large diffuse exposure, it is a small concentrated and levered one. That is a different
financial-stability object, and it maps to a different regime in WS4 than the brief's
"overinvestment bust" language assumes. It also means the holder map (WS2) matters more
than the sizing table, for Leg A as well as Leg W.

---

## Still to build

- Tier 1, and Tier 2b from BIS and private-credit aggregates
- Growth rates, not just levels: the brief notes trajectory may matter more than level
- Euro area, China, Japan, Korea; India as the contrast case
- Foreign private issuers (20-F) for the non-US cases

# PAEI(c): method note and data dictionary

Step 2 of MASTER_PROMPT_PHASE2.md. Date 2026-09-19.

---

## 1. The problem PAEI(c) solves

PAEI as built in Phase 1 discounts occupations whose environments are unstructured. But
operating in unstructured environments is exactly what Physical AI is meant to deliver. So
PAEI at c = 0 measures exposure to CURRENT industrial robotics, not to Physical AI. The
index has to be conditioned on realised capability before it measures the paper's subject.

## 2. Definitions

| Symbol | Meaning | Range |
|---|---|---|
| P | embodiment intensity: does the job need a physical body | 0 to 1 |
| S | environmental structure: 1 fully structured, 0 fully unstructured | 0 to 1 |
| S_rank | employment-weighted percentile rank of S across occupations | 0 to 1 |
| c | realised Physical AI capability. 0 = current industrial robotics, 1 = robust operation in unstructured settings | 0 to 1 |

## 3. Functional forms

**Smooth.** PAEI_smooth(c) = P * S^(1 - c)

At c = 0 this reduces to P * S, the Phase 1 index. At c = 1 it is P alone: structure no
longer gates anything, so exposure equals embodiment. S^(1-c) rises monotonically to 1 as c
rises, progressively releasing low-structure occupations from their discount.

**Threshold.** exposed(c) = 1 if deficit <= c, exposure magnitude P

An occupation's structure deficit is how unstructured it is. Capability c overcomes a
deficit up to c. Discontinuous per occupation, which is how a deployment decision actually
behaves.

The two forms disagree on purpose. The smooth form says everything is partially exposed
everywhere; the threshold form says occupations flip. There is no evidence to select
between them, so both are reported.

## 4. Two corrections the data forced

### 4.1 The raw S scale is degenerate under a threshold

S has standard deviation 0.071 and range 0.29 to 0.70, because it is a difference of two
bounded means recentred on 0.5. Thresholding the raw deficit (1 - S) therefore produces a
step function rather than a frontier:

| c | Share of employment exposed, raw S |
|---|---|
| 0.00 to 0.25 | 0.00% |
| 0.40 | 1.57% |
| 0.50 | 37.63% |
| 0.60 | 90.35% |
| 0.70 and above | 100.00% |

Everything crosses in a band of width 0.25. That is a property of the scale, not of
robotics. The reported threshold results therefore use S_rank, the employment-weighted
percentile rank of S, under which c means "capability c handles occupations up to the c-th
percentile of unstructuredness". The raw version is retained in the outputs and plotted in
the figure so the degeneracy stays visible rather than being quietly dropped.

### 4.2 The threshold rule needs an embodiment gate

The threshold keys only on structure. Ungated, the list of occupations switching between
medium and high capability was led by **Lawyers (P = 0.095)** and **Chief Executives
(P = 0.132)**, which is nonsense: an occupation that needs no body cannot be displaced by a
robot at any capability level. Switchers are gated at the median P (0.413), and the
headline exposure measures are weighted by P.

## 5. IMPORTANT: which frontier numbers are informative and which are definitional

Because S_rank is an employment-weighted percentile rank, **the share of employment
crossing the threshold is approximately equal to c by construction**. At c = 0.5, 50.7
percent of employment is "exposed". That is a tautology, not a finding, and it must never
be reported as a result.

The informative quantities are the ones weighted by embodiment, because P is not
mechanically tied to the rank:

| c | Embodied work exposed (%) | Wage bill at risk (USD bn) | Mean PAEI_smooth (emp-wt) |
|---|---|---|---|
| 0.00 | 0.0 | 0.0 | 0.17 |
| 0.20 | 19.4 | 320.0 | 0.19 |
| 0.50 | 47.2 | 889.3 | 0.24 |
| 0.80 | 76.0 | 1,628.9 | 0.30 |
| 1.00 | 100.0 | 2,235.6 | 0.35 |

Coverage: 375 SOC occupations with PUMS employment, 140.2 million workers, 7,878.2 USD bn
wage bill. The wage bill at risk at c = 1 (2,235.6 USD bn) is 28.4 percent of the covered
wage bill, which is the embodiment-weighted ceiling: even with perfect capability, the
exposure is bounded by how much of the wage bill is paid for physical work.

## 6. Scenario mapping is stipulated, not estimated

| Scenario | c |
|---|---|
| low | 0.20 |
| medium | 0.50 |
| high | 0.80 |

**This is a modelling assumption and must be labelled as one in the paper.** No published
robotics capability benchmark was located that maps onto a normalised structure-tolerance
scale, so c cannot currently be anchored to measured capability. Every result is reported
across the full grid in `data/processed/paei_c_frontier.csv`, and the named scenarios are
read off the grid rather than driving it. If a reader disagrees with the mapping, the grid
lets them substitute their own without rerunning anything.

Anchoring c to benchmarks (manipulation success rates in unstructured settings, for
instance) remains open and is the most valuable single improvement to this module.

## 7. The distinctive content: who switches between medium and high capability

27 embodiment-gated occupations, 11.6 million workers (8.3 percent of covered employment),
400.2 USD bn of wage bill. Leading by employment times embodiment:

recycling and reclamation workers; landscaping and groundskeeping; industrial truck and
tractor operators; food service managers; first-line supervisors of production; couriers
and messengers; cleaners of vehicles and equipment; correctional officers; roofers; transit
bus drivers; massage therapists; veterinary technologists; automotive body repairers; office
machine repairers; structural iron and steel workers; crane and tower operators.

This is the substantive answer to "what makes Physical AI different from prior automation".
These are physical jobs in semi-structured or outdoor settings that current robotics cannot
touch and that no cognitive-AI exposure index scores as exposed. Median hourly wages cluster
between 12 and 27 USD.

## 8. Economic feasibility filter: NOT built

The optional filter (exposure counts only where the occupational hourly wage exceeds an
assumed hourly robot cost) is not implemented. Median hourly wages by occupation are in the
outputs and the filter is a one-line addition, but no verified source for an all-in hourly
robot cost was located, and inventing one would violate Rule 2. When a sourced figure
exists the filter should be run as a sensitivity across a range, never at a point estimate,
and kept separate from technical exposure.

## 9. Data dictionary

`data/processed/paei_c.csv`, one row per SOC occupation per c value (786 x 21 = 16,506).

| Column | Type | Meaning |
|---|---|---|
| soc | string | 6-digit SOC code |
| title | string | occupation title (first O*NET detail title in the SOC) |
| c | float | Physical AI capability, 0 to 1 in steps of 0.05 |
| embodiment_P | float | embodiment intensity, 0 to 1 |
| structure_S | float | environmental structure, raw, 0 to 1 |
| structure_S_rank | float | employment-weighted percentile rank of S |
| paei_smooth | float | P * S^(1-c) |
| structure_deficit_raw | float | 1 - S |
| structure_deficit_rank | float | 1 - S_rank |
| exposed_threshold_raw | 0/1 | deficit_raw <= c (degenerate, see 4.1) |
| exposed_threshold_rank | 0/1 | deficit_rank <= c |
| exposure_magnitude_rank | float | P if exposed under the rank rule, else 0 |
| employment | float | ACS PUMS 2023 weighted employment |
| wage_bill | float | ACS PUMS 2023 weighted wage bill, USD |
| median_hourly_wage | float | employment-weighted median hourly wage, USD |

Companion files: `paei_c_frontier.csv` (one row per c), `paei_c_switchers_medium_to_high.csv`,
`paei_c_summary.json`. Figure: `paper/figures/exposure_frontier.png`.

## 10. Limitations

- Employment coverage is 375 of 786 SOC occupations (47.7 percent of occupations, 140.2
  million workers). The Census OCCP crosswalk is coarser than SOC detail. BLS OES would fix
  this and returns HTTP 403 to this environment.
- S itself has no external validation (see notes/paei_validation.md Section 3). PAEI(c)
  inherits that gap, and at high c the index leans more on P, which IS externally
  correlated, so paradoxically PAEI(c) is better grounded at high c than at low c.
- c is stipulated.
- Occupation-level exposure says nothing about displacement timing or about within-
  occupation task heterogeneity.

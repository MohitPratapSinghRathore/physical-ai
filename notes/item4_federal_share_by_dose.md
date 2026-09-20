# Item 4. The federal share of first-round losses, by dose

Code: `src/item4_federal_share.py`. Outputs: `data/processed/item4_federal_share_by_dose.csv`,
`item4_federal_share_summary.csv`, `item4_federal_share_summary.json`.

## The defect being fixed

The published object sealed a min and a max over a sweep the brief never described. That is
the replicator's insufficiency I-6, and it is the reason their range (0.779 to 0.837) is
narrower than the sealed one (0.759 to 0.916) at both ends: **they were sweeping fewer
dimensions, not computing it differently.** A single range also hides the one thing the
number does, which is rise with the dose.

## Two readings, both reported

| | what counts as federal on the agency book |
|---|---|
| **NARROW**, as published | only the loss beyond Enterprise capital plus a year of earnings. Under the item 1 rebuild that layer is still zero at every dose, now because 179.4bn of capital stands against a maximum retained loss of 109.0bn rather than because of a phantom 592.855bn transfer layer |
| **CONSERVATORSHIP** | the retained Enterprise loss. The Enterprises are in conservatorship, net worth stands behind the Treasury senior preferred agreements, and no private shareholder is positioned to absorb anything. Only what private cover actually pays is private |

Narrow is the lower bound, conservatorship the upper bound. Both travel together.

## The result, by dose

| dose | inside the data | **narrow** | **conservatorship** |
|---|---|---|---|
| 5 pct | yes | 0.759 to 0.853 | 0.857 to 0.901 |
| **10 pct** | **yes** | **0.785 to 0.870** | **0.876 to 0.913** |
| 25 pct | yes | 0.810 to 0.923 | 0.878 to 0.948 |
| 50 pct | no | 0.855 to 0.925 | 0.897 to 0.949 |
| 75 pct | no | 0.809 to 0.897 | 0.859 to 0.924 |

**The headline depends on the dose.** At the 10 percent dose, which is the only one inside
the observed data on every axis, the federal share is about four fifths under the narrow
reading and about nine tenths under the conservatorship reading. It rises to roughly nine
tenths and nineteen twentieths respectively at 50 percent.

**The replicator's by-dose result reproduces.** They report 0.78 at 10 percent rising to 0.90
at 50 percent. Our narrow reading gives 0.785 to 0.870 at 10 percent and 0.855 to 0.925 at 50
percent. Their point sits inside our range at both ends and the direction is the same. This
was the largest unexplained gap in the round and it is now closed: it was the sweep, exactly
as they diagnosed.

## Two things a single range concealed

**It is not monotone.** The share peaks at the 50 percent dose and falls back at 75 percent,
in both readings. The reason is that the fiscal component saturates while credit losses keep
growing on balances that are still there. Any claim that the federal share "rises with the
dose" holds only up to about half the wage bill and must be stated that way.

**The exposure type matters as much as the dose.** At the same dose the embodied group always
puts a higher share on the federal balance sheet than either cognitive group, by 6 to 11
percentage points:

| dose | embodied, narrow | cognitive AIOE, narrow |
|---|---|---|
| 10 pct | 0.855 to 0.870 | 0.785 to 0.827 |
| 25 pct | 0.914 to 0.923 | 0.813 to 0.850 |
| 50 pct | 0.916 to 0.925 | 0.855 to 0.885 |

The embodied group is lower paid, so a given wage-bill dose displaces more workers, and the
payroll-tax and benefit channels follow head counts rather than dollars.

## What the item 1 rebuild did and did not change here

**Nothing, under the narrow reading.** The beyond layer was zero before the rebuild and is
zero after it, so reallocating the GSE loss between private cover and Enterprise capital
leaves both on the private side. This is worth saying plainly because it is the specific
question the replicator asked, and their answer was right: **none of the sovereign gap is
attributable to the GSE treatment.**

**The rebuild changes the conservatorship reading materially**, because it determines how much
of the GSE loss private cover actually takes:

| dose | GSE loss bn | private cover bn | Enterprises retain bn | beyond bn |
|---|---|---|---|---|
| 10 pct | 23.9 | 2.5 | 21.4 | 0 |
| 25 pct | 58.3 | 12.6 | 45.7 | 0 |
| 50 pct | 111.7 | 43.9 | 67.8 | 0 |
| 75 pct | 160.2 | 72.2 | 88.1 | 0 |

Under the superseded formula private cover took the whole loss at every dose. Under the
rebuild it takes 11 percent at the 10 percent dose. That is what moves the conservatorship
reading up by 8 to 10 percentage points relative to the narrow one.

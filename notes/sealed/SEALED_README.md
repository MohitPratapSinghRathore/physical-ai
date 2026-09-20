# The sealed expected value files, and which one to use

Updated 2026-09-20.

| File | Round | Brief it is scored against | Regenerated? |
|---|---|---|---|
| `sealed_expected_values_round2.json` | **2, the current one** | `notes/replication_brief_v2.md` | yes, by `src/seal.py` |
| `sealed_expected_values_round1_ARCHIVED.json` | 1, frozen | `notes/replication_brief.md`, itself superseded | **never** |
| `sealed_expected_values.json` | 1, byte-identical to the archived copy | as above | **never** |

**Use round two.** Round one is kept because it is the record the first independent
replication was scored against, and rewriting it would destroy that record. It was in fact
overwritten once during the repair session and restored from git, which is why round two has
its own path and `src/seal.py` no longer touches the round-one name at all.

`sealed_expected_values.json` is the original unversioned name and is retained only because
`notes/replication_brief.md` and earlier findings refer to it. It carries no separate content.

**No sealed file belongs in `notes/replication/`**, which is the replicating instance's own
folder, and none belongs in `data/release/`, which is for material intended for publication.
All three were moved here from `data/release/` on 2026-09-20 for that reason.

## What moved between the rounds

Five corrections, all of them errors in this project rather than revisions to a source. They
are listed with their effects in `notes/replication/round1_mismatch_classification.md` and in
the `_round` block of the round-two file itself. In summary:

- the break-even capital tax rate was not a tax rate, and broke its own plausibility bound
- the wage bill base a dose is converted to dollars on was wrong in two different directions
  in two different modules
- HI carried the OASDI payroll share and a total-income denominator
- the auto aggregate sat on a series discontinued after 2024Q4
- the trust fund figures were derived where they are now read from the Trustees Report

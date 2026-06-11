---
phase: 24-empirical-dataset-verification-and-correction-addendum
topic: DATA-05 base-hierarchical rerun remediation
status: decision-recorded-not-yet-executed
created: 2026-06-11
source_gap: GAP-24-01
---

# DATA-05 Rerun Remediation

## User Instruction

On 2026-06-11, the user resolved `GAP-24-01` with this operating decision:

- Do not skip the 70 affected systems permanently.
- Treat the current `ic_final/ic_hierarchical` files as canonical.
- Treat the 70 affected base-hierarchical Brutus outputs as invalid/stale artifacts until rerun.
- Rerun the affected base-hierarchical outputs from the current canonical IC files.
- Preserve the old outputs as forensic evidence until validated replacement is complete.

This document records the remediation plan only. It does not assert that the rerun has already happened.

## Affected Population

The affected IDs are:

- `0005`-`0059`
- `0061`-`0075`

Total: 70 base-hierarchical trajectory files.

Canonical IC path pattern:

```text
simulation_data/Data/ic_final/ic_hierarchical/ic_hierarchical_XXXX.txt
```

Invalid base-output path pattern until remediation passes:

```text
simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_XXXX.txt
```

Gold-hierarchical outputs for these IDs match the current IC masses and remain valid evidence for the fact that the ICs themselves are not corrupt. They are not a substitute for regenerating the base-hierarchical variant.

## Working Diagnosis

The root cause is not fully proven from source materials, so it remains a working diagnosis rather than a framework verdict. The evidence points to stale early base outputs:

- The bad base-hierarchical outputs were written before the corresponding current IC files were finalized for many affected IDs.
- Adjacent clean base outputs were written later or regenerated later.
- The current base runner skips an existing output if it only passes the final-time validation gate; it does not check mass equality before deciding "Already valid."
- The bad mass vectors do not represent float64 round-trip error and do not require `decimal.Decimal` parsing to explain.

## Rerun Contract

Use the base-hierarchical Brutus contract:

| Parameter | Value |
| --- | --- |
| Variant | `brutus_hierarchical` |
| IC source | current `ic_hierarchical_XXXX.txt` |
| `tolerance` | `1e-15` |
| `word_length` | `130` |
| `t_begin` | `0` |
| `t_end` | `10` |
| `dt_out` | `0.08` |
| `n_particles` | `3` |

Do not rely on the existing batch runner's ordinary skip behavior for these IDs; it will classify the old files as valid if they only reach the final timestep.

## Required Remediation Gates

Before any replacement output is used for training, metrics, or PIPE-07:

1. Preserve the current 70 invalid output files and record hashes or another re-derivable manifest.
2. Generate replacement files into a staging location first, not directly over the existing outputs.
3. Verify every staged replacement satisfies `m_IC == m_Brutus(t=0)` under the DATA-05 comparator.
4. Verify every staged replacement reaches the expected final time for base-hierarchical runs.
5. Verify snapshot/schema expectations remain compatible with the Phase 24 DATA-04/DATA-06 probes.
6. Replace the old outputs only after the staged outputs pass all checks.
7. Regenerate or invalidate any derived metrics for the affected IDs before training consumes them.
8. Rerun the Phase 24 DATA-05 probe and update this document with the final pass evidence.

## Training Boundary

Until remediation passes, downstream training and metrics must treat the 70 old base-hierarchical outputs as quarantined. Temporary smoke tests may exclude these IDs explicitly, but final training must use validated rerun outputs.

## Phase 24 Boundary

Phase 24 may continue because the semantic decision is now resolved: the current ICs are canonical and the old base-hierarchical artifacts require rerun. Phase 24 must not claim the data files are fixed until the rerun gates above have been executed and recorded.

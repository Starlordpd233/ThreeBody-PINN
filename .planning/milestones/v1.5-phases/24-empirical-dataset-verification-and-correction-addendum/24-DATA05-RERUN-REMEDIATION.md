---
phase: 24-empirical-dataset-verification-and-correction-addendum
topic: DATA-05 base-hierarchical rerun remediation
status: executed-and-validated-2026-06-11
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

## Execution Evidence (2026-06-11)

The rerun was executed and validated on 2026-06-11 on the M5 Pro MacBook (Brutus rebuilt
from source against Homebrew GMP/MPFR + advanpix mpreal; rebuild smoke-tested by
reproducing known-good ID `0100` numerically identically, t_cpu fields excluded).
All 70 reruns used the contract above verbatim; run provenance is in
`24-DATA05-RERUN-MANIFEST.json` (70/70 subprocess success, median 11.6 s/run).

Gate-by-gate results:

1. **Preserve + manifest:** SHA-256 manifest of the 70 old files recorded pre-swap in
   `24-DATA05-OLD70-SHA256.txt` (committed). Old files moved (not deleted) to
   `simulation_data/Data/forensic/data05_gap24-01_old_outputs/`; post-move hashes
   re-verified 70/70 against the manifest.
2. **Staging first:** replacements generated in `simulation_data/Data/rerun_staging/data05_gap24-01/`
   (outside `brutus_output/` so variant-folder probes were never affected); staging
   removed after the swap.
3. **Mass equality:** 70/70 staged files satisfy `m_IC == m_Brutus(t=0)` at float64
   (DATA-05 comparator). Full t=0 state (positions and velocities) also matches the IC
   at float64. Evidence: `24-DATA05-RERUN-VALIDATION.{md,json}`.
4. **Final time:** 70/70 reach final t = 10.000000000000007 with 126 snapshots.
5. **Schema:** 70/70 valid (`t 3 t_cpu` headers, 3×7-field body lines, `Result:` footer
   present in all 70).
6. **Swap:** executed after user approval of the validation report; live folder back at
   4,857 files.
7. **Metrics:** regenerated and validated 2026-06-11 (user reversed the same-day
   deferral). The 70 stale metrics JSONs (computed from the old artifacts) were
   hash-manifested in `24-DATA05-OLD70-METRICS-SHA256.txt` (committed) and archived to
   `simulation_data/Data/forensic/data05_gap24-01_old_metrics/`, then regenerated via
   `calculate_metrics.py` `process_simulation_type('hierarchical')` (70 processed,
   70 generated, 0 errors; the script's skip-if-valid-JSON behavior left the other
   4,787 untouched). Validation 70/70: no error field, schema parity with existing
   metrics, 126 snapshots to t=10, `total_mass` equals the IC mass sum exactly at
   float64, energy conservation quality "excellent" for all 70 (relative error
   2.2e-16 .. 5.1e-14).
8. **Probe re-runs (post-swap):** DATA-05 probe: `brutus_hierarchical` now **0/4857**
   mismatches (was 70/4857); 0 mismatches across all 15,028 pairs. DATA-04: observed
   footer-less count in `brutus_hierarchical` is now **1,480** (was 1,550) — all 70 old
   files were footer-less, all 70 replacements carry footers; documented counts citing
   1,550 (e.g. dataset README §known-issues, audit cross-check) are stale as of this
   remediation and the DATA-04 cross-check note already flags the framing. DATA-06:
   footer-bearing cohort 3,307 → 3,377, footer-less 1,550 → 1,480, final-time
   prevalence ≥ 9.5 remains 1.0; no anomalies.

All quarantines are lifted as of 2026-06-11: trajectory replacements are live and the
70 metrics files are regenerated and validated. All eight remediation gates are closed.

---
phase: 46-frame-resolution-gate-aligned-validation
plan: "09"
subsystem: verification
tags: [conf-08, conf-01, target-frame, evidence, owner-branch]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-08 resident pairing and COM/boost repair
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-06 pre-repair probe and content-pinned population
provides:
  - "One unchanged-instrument post-repair CONF-01 measurement"
  - "D-09 rule-5 VERDICT_NON_FRAME_DIVERGENCE with a full pre/post comparison"
  - "GAP-46-06 owner branch point; no self-ratification"
affects: [46-07 blocked, 47 blocked, CONF-01 unresolved]

key-files:
  created:
    - .planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT-POSTREPAIR.md
    - .planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/raw.json
    - .planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/summary.md
  modified:
    - .planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md
    - .planning/milestones/v2.2-GAPS.md

key-decisions:
  - "Transcribe the machine's rule-5 D-09 verdict without rounding or reinterpretation"
  - "Treat plus_permutation == 0 for all 1651 records as the direct repair check"
  - "Do not treat pre-repair confound labels as post-repair pairing status"
  - "Stop before 46-07 and request the owner branch decision"

requirements-completed: [CONF-08]
completed: 2026-07-27
status: complete
---

# Phase 46 Plan 09: Post-Repair Target-Frame Re-Probe Summary

**The single authorized re-probe returned
`VERDICT_NON_FRAME_DIVERGENCE` (D-09 rule 5). The repair is exact, the controls
are unchanged, and CONF-01 remains unratified pending GAP-46-06.**

## Task 1 hard gates

All four gates passed before the evidence process was started:

1. **Instrument identity:** worktree and `997c731b` blob SHA-256 both
   `828ed22cfb58d088a2cf47c6f4deb23ea0a44ee1883f0b7455eddef83f9a0396`.
2. **Population inputs:**
   - seed 41 manifest:
     `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86`
   - seed 42 manifest:
     `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`
   - seed 43 manifest:
     `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172`
   - blacklist:
     `238efd128cd04307708f74bbb54c23cad2cfec8b1cd6cfb09df62d830bae3e44`
3. **Attributable code state:** `git status --short -- pinn/` was empty; the
   run-time repository commit was
   `a7a211ed3e755fc3c5bd090b6d8b9ffe3f221ed5`.
4. **Repair boundary:** 46-08-SUMMARY.md states, verbatim:
   "`Not applied: _rotation_gauge`", "`Not applied: position scaling by D`",
   and "`Not applied: velocity scaling by V`".

## The one evidence run

The completed process was invoked once:

```text
python -m pinn.verification.target_frame_probe \
  --manifest runs/stage0-pilot-seed41/splits.json \
  --manifest runs/stage0-pilot-seed42/splits.json \
  --manifest runs/stage0-pilot-seed43/splits.json \
  --blacklist-path problematic_ics_blacklist.json
```

- Run directory: `evidence/target-frame/20260728T014532Z/`
- `raw.json` SHA-256:
  `11b6690add8bb18181efadd2e7848a5c04439e7c8d501cfd9c22ebe69a402654`
- Run-time `repo_commit`:
  `a7a211ed3e755fc3c5bd090b6d8b9ffe3f221ed5`
- Schema: `phase46-target-frame/v1`
- Eligible count: 1651
- Machine verdict: `VERDICT_NON_FRAME_DIVERGENCE`
- Rationale: rule 5, route D-09

Exactly one new evidence directory exists. Neither evidence file contains a
`/Users/` path. The original `46-VERDICT.md` is untouched.

## Full pre/post comparison

| arm | measure | pre-repair 46-06 | post-repair 46-09 |
|---|---|---:|---:|
| scaled hypothesis | median residual | 0.9780023386528649 | 0.9893581923969974 |
| scaled hypothesis | max residual | 1.0602956610091072 | 1.0398406116001933 |
| scaled hypothesis | consistent | 47 | 46 |
| scaled hypothesis | separated | 1604 | 1605 |
| raw hypothesis | median residual | 1.347556618853727 | 0.0802249105713925 |
| raw hypothesis | max residual | 52.409959695713795 | 22.603496469372814 |
| raw hypothesis | consistent | 0 | 1086 |
| raw hypothesis | separated | 1651 | 565 |
| positive control | median residual | 0.08022618097116868 | 0.08022618097116868 |
| positive control | max residual | 22.603484385047974 | 22.603484385047974 |
| positive control | consistent | 1651 | 1651 |
| positive control | separated | 0 | 0 |
| provenance control | median residual | 0.08022618097116782 | 0.08022618097116782 |
| provenance control | max residual | 22.603484385047963 | 22.603484385047963 |
| provenance control | consistent | 1651 | 1651 |
| provenance control | separated | 0 | 0 |

Required confound comparison:

| measure | pre-repair | post-repair |
|---|---:|---:|
| `permutation_identity = false` | 1651 | 1651 |
| `first_diverging_step = com_recenter_boost` | 1651 | 1651 |
| corrected-raw consistent | 1100 | 0 |
| uncorrected raw arm consistent | 0 | 1086 |
| `plus_permutation = 0.0` | 0 | 1651 |

The controls reproduce exactly. The repaired resident matches `r_bar_perm`
exactly on all 1651 records, but the unchanged probe's identity classes admit
only file-order parsed raw or fully rotated/scaled canonical output. Its
`permutation_identity`, `first_diverging_step`, and unconditional
inverse-permutation correction therefore retain pre-repair meanings that do
not describe the repaired pairing.

## Branch routing

The result is an explicit D-09 route under the already-grounded rule order.
GAP-46-06 records the owner decision needed to choose among a
post-repair-aware probe contract, an instructed operational frame, a further
canonical transform, or deferral.

No frame was ratified. Plan 46-07, Phase 47, and dependent work remain blocked.
`pinn/` was untouched by Plan 46-09, and the probe was not re-run or modified.

## Validation

- `$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python -m pytest
  tests/phase46 -q -rs` — **102 passed, 27 subtests passed, zero skips**.
- Artifact assertions — **passed**: eligible count and D-09 rule/route,
  byte-identical control aggregates, all-trajectory `plus_permutation = 0.0`,
  path redaction, immutable pre-repair verdict, and clean `pinn/` status.
- `git diff --check` — **passed**.

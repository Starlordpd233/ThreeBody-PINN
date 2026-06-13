---
phase: 26-dataloader-ingestion-and-selection-contracts
plan: 01
subsystem: framework-specs (DataLoader ingestion contracts)
tags: [PIPE-01, PIPE-02, B-06, B-11, admission-gate, id-resolution, evidence-packet, ledger]
requires:
  - "Phase 25 evidence machinery (_TEMPLATE.md, README.md protocol, m11-m12-severity.md locked M12 rule)"
  - "24-VERIFIED-FACTS.md CLM-01/02/04/05b/10/11/12, DATA-05"
  - "02-resolution-doc.md §3.1 Q-A1 (B-06) + §3.2 Q-A2 (B-11) candidate spec text"
provides:
  - "ctl_instruction.md Step 1A trajectory admission gate (PIPE-01 / B-06 contract)"
  - "ctl_instruction.md Step 1 item 7 ID-resolution contract (PIPE-02 / B-11 contract)"
  - "b-06-admission-gate.md + b-11-id-resolution.md evidence packets (verdict accept-resolution)"
  - "AC-PIPE-01 + AC-PIPE-02 reserved acceptance checks defined and executed"
affects:
  - "Phase 27 (M12 sampling spec edit cites B-06's M12 reference)"
  - "Phase 29 acceptance suite (VER-09 builds runnable AC-PIPE-01/02 from these packets)"
  - "FUT-01 (TrajectoryValidator + TrajectoryIndex implementation from these contracts)"
tech-stack:
  added: []
  patterns: [packet-before-edit, same-commit-ledger-edits, close-with-parent, directory-qualified-citations]
key-files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/b-11-id-resolution.md
  modified:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/b-06-admission-gate.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
decisions:
  - "B-06 and B-11 both adjudicated accept-resolution; both candidate texts survived independent CLM verification unchanged"
  - "Snapshot minimums in Step 1A stated by citing the locked M12 rule (D-02), not re-derived; >= 200 floor rejected on CLM-10"
  - "ID-resolution prohibits dense/positional/array-index addressing, grounded in CLM-01 non-density (max_id 3998 vs 2749 files)"
metrics:
  duration: ~25 min (resume from prior interrupted run that had drafted only the B-06 packet)
  completed: 2026-06-13
---

# Phase 26 Plan 01: DataLoader Ingestion and Selection Contracts (B-06 + B-11) Summary

Locked the two interlinked Step-1-region DataLoader contracts in `ctl_instruction.md` — the Stage 4→5 trajectory admission gate (PIPE-01 / B-06) and the ID-resolution contract (PIPE-02 / B-11) — each backed by a completed evidence packet with `accept-resolution` verdict, passing acceptance probes, and VERIFIED ledger rows (G1/G2 closed with parents), in one atomic commit.

## What Was Built

- **`ctl_instruction.md` Step 1A — Trajectory Admission Gate** (post-edit `:404-452`): the 7-clause data-side gate (identity+blacklist, DATA-05 quarantine, structural integrity `>= 2` snapshots, completeness `final_timestep >= 9.5`, conservation `SCS > -5` transcribing locked HC-5, physical-invariant gates, grid-consistency at WARN), with per-trajectory reason-coded rejection logging, ordered before stage assignment and `compute_globals`. Snapshot minimums stated by **citing** the locked M12 rule (`m11-m12-severity.md`, Phase 27 PIPE-04), not re-derived; the issue-doc `>= 200` floor explicitly rejected.
- **`ctl_instruction.md` Step 1 item 7 — ID resolution** (post-edit `:381-405`): scan-built `id_to_path`, dual `physical_key`/`record_key`, anchored regex `^brutus_(hierarchical|standard)_(\d{4})\.txt$`, hard duplicate-key error, explicit absent-key miss with no positional fallback, sorted-key iteration, the explicit `ID ≠ array index` invariant, and per-folder init logging. Cross-referenced from Step 5 (`:1138-1142`).
- **`b-06-admission-gate.md`** (validated/finalized from the prior run's draft): 12-section packet, `accept-resolution`, probe captures corrected to post-edit line numbers.
- **`b-11-id-resolution.md`** (authored this run): 12-section packet, `accept-resolution`, grounded in CLM-01/02/04/05b/12 non-density.
- **`evidence/README.md`**: ID→Filename Map rows for B-06 and B-11.
- **`24-ISSUE-LEDGER.md`**: B-06, B-11 → VERIFIED with packet links + transition logs; G1 closes with B-06, G2 closes with B-11 (D-07, no separate packets).

## Verification

- **AC-PIPE-01** (spec-consistency + CLM-10 dataset fact): `## Step 1A` heading, `final_timestep >= 9.5`, `SCS > -5`, M12 citation present; `>= 200` appears only in rejection prose (lines 446-447), never as a contract clause. PASS.
- **AC-PIPE-02** (spec-consistency + CLM-01/04 dataset fact): scan-built `id_to_path`, both key levels, anchored regex, `array index`/`range(n_files)` prohibitions, Step-5 cross-ref present. CLM-01 max_id 3,998 vs 2,749 files confirms dense indexing impossible. PASS.
- **D-04 perimeter:** only `ctl_instruction.md` + `.planning/` paths changed — no edits to `sampling_method.md`, `data_quality_assessment.md`, or any `pinn/` file.
- **D-08 regression:** B-06 and B-11 share the Step-1 region; reconciled in one before/after pass (B-06 clause 1 depends on B-11 item 7 — mutually consistent). No previously-VERIFIED Phase 26 row existed.

## Deviations from Plan

None — plan executed as written. Task 1 preflight tag `v1.5-pre-phase-26` already existed (created by the prior interrupted run); re-checked as present per the plan's idempotent preflight. The B-06 packet existed as an untracked draft from the prior run; it was validated against the protocol and `_TEMPLATE.md`, its premature probe-output line numbers were corrected to the actual post-edit values, and its Before/After note was updated with post-edit anchors. No re-authoring from scratch was needed.

## Notes

- The single atomic Plan 26-01 commit is `b1852b0f` (8 files, via `scripts/agent-commit`, scope `26-01`). The `<PLAN-26-01-SHA>` placeholder tokens in the two packets' Status Transition Logs and the ledger per-finding subsections were backfilled to `b1852b0f` in the immediately following provenance commit, per the Phase 25 precedent (a commit cannot reference its own hash inline; D-08 same-commit discipline holds for the work itself, the SHA backfill is the one unavoidable follow-up).
- Carried caveats (D-13): OI-6 (no-footer probe-coverage gap; B-06 clause 7 held at WARN) and OI-9 (DATA-05 70-ID rerun validated 2026-06-11) propagated into the B-06 packet.

## STOP-Protocol Gap Findings

None. Both B-06 and B-11 candidate verdicts were well-grounded and edit-ready; every clause was either a transcribed locked convention (cited, not re-decided) or grounded in a verified CLM/DATA fact. No source-silent semantic, process-schema, or cross-phase decision was encountered.

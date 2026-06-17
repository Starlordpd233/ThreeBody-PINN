---
status: active
purpose: implementation-plan
created: 2026-06-13
milestone: v1.5
phase: 26-dataloader-ingestion-and-selection-contracts
retirement_trigger: superseded when Phase 29 builds and re-executes the full acceptance suite (VER-09) and reconciles the ledger
phase_num: 26
plan: 02
subsystem: specwork
tags: [PIPE-03, M11, blacklist, ctl_instruction, evidence-ledger]
requires: [26-01]
provides: [PIPE-03-blacklist-exclusion-contract, M11-VERIFIED, G3-VERIFIED, AC-PIPE-03]
affects: [ctl_instruction.md, 24-ISSUE-LEDGER.md, m11-m12-severity.md]
tech_stack_added: []
key_files_created: []
key_files_modified:
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md
  - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
decisions:
  - "Blacklist-exclusion contract landed as a `### Blacklist-exclusion contract (clause 1 detail; M11 / PIPE-03)` sub-section co-located with the Step-1A gate, after the clause list and before Step 2 (D-03 presentation discretion)."
  - "65-ID figure (2 hierarchical + 63 standard) cited as a DATA-02/CLM-03 dataset fact, never hard-coded as a contract constant (T-26-07 mitigated)."
  - "M11 packet EXTENDED, not duplicated; M12 sub-part byte-stable (D-06 / T-26-05)."
  - "OI-8 live-loader consumption confined to the FUT-01 hand-off note (T-26-06)."
metrics:
  duration_minutes: 28
  tasks_completed: 2
  files_modified: 3
  completed_date: 2026-06-13
---

# Phase 26 Plan 02: DataLoader Ingestion and Selection Contracts — PIPE-03 Blacklist-Exclusion Summary

PIPE-03 blacklist-exclusion contract (M11) transcribed into `ctl_instruction.md` co-located with the Step-1A gate, grounded in DATA-02/CLM-03, with the existing M11 packet extended (M12 untouched), a passing AC-PIPE-03 probe, and M11 + G3 moved to VERIFIED in one atomic commit.

## What Was Built

- **`ctl_instruction.md` blacklist-exclusion contract.** A new `### Blacklist-exclusion contract (clause 1 detail; M11 / PIPE-03)` sub-section follows the Step-1A clause list (before `## Step 2`). It transcribes the candidate 6-clause contract from `02-resolution-doc.md §3.3 Q-A3:223-251` (plus the proposed-spec-text block `:244-251`): (1) init-load before stage assignment and `compute_globals`; (2) strict two-key schema validation with `int` normalization + within-family dedup; (3) IC-level exclusion attaching to `physical_key` (base + gold via byte-identical-subset); (4) fail-closed — missing/unreadable/invalid file = hard init failure, override only via explicit logged dev-only flag; (5) per-family logging with the count re-keyed to parsed file content and the 65-ID figure cited as a DATA-02/CLM-03 fact; (6) defense-in-depth batch-assembly assertion raising a hard error on any blacklisted emitted sample. It routes the live-loader consumption question to FUT-01 (OI-8 / SCOPE-10).
- **`m11-m12-severity.md` extension (D-06).** Added an M11-specific PIPE-03 Before/After Spec Note recording the actual spec landing (the existing M11 After said "No framework-spec edit (D-02)"; this records the real edit), the AC-PIPE-03 executed pass criteria + re-derivable probe capture, the AC-PIPE-01 regression re-check, and three M11 forward status-transition-log lines (PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED). The M12 sub-part is byte-stable.
- **`24-ISSUE-LEDGER.md` transitions.** Row M11 → VERIFIED with forward transition log; row G3 → VERIFIED (close-with-parent G3→M11, no separate packet, D-07).

## Tasks Completed

| Task | Name | Commit | Files |
| ---- | ---- | ------ | ----- |
| 1 | Plan preflight (tag + commit wrapper + 26-01 dependency) | (no mutation) | — |
| 2 | Extend M11 packet, edit blacklist contract, run AC-PIPE-03, advance ledger, commit | see Commits | ctl_instruction.md, m11-m12-severity.md, 24-ISSUE-LEDGER.md |

## Acceptance Check

**AC-PIPE-03 — PASS.** Reused the Phase 24 `data02_blacklist.py` probe: composition `{hierarchical: 2, standard: 63}` total 65 (CLM-03 re-derived). Spec-consistency grep confirms the contract names init-load before stage assignment / `compute_globals`, the hard-init-failure (fail-closed) clause, per-family exclusion logging, and the defense-in-depth batch-assembly assertion; the 65-ID figure is cited as a DATA-02/CLM-03 fact, not a contract constant. Command + output captured re-derivably in the packet (D-15).

**AC-PIPE-01 regression re-check (D-08) — PASS.** The M11 blacklist sub-section sits after the Step-1A clause list, leaving B-06's gate clauses byte-stable. Re-ran the AC-PIPE-01 spec-consistency grep: `## Step 1A — Trajectory Admission Gate`, `final_timestep >= 9.5`, `SCS > -5` present; no `>= 200` floor introduced. B-06 stays VERIFIED.

## Deviations from Plan

None — plan executed exactly as written. The verdict was treated as a hard constraint (D-02, BLOCKING STANDS); no re-adjudication.

## STOP-Protocol / Gaps

No source-silent semantic, process-schema, or cross-phase decision was invented. The blacklist contract was fully grounded in the resolution doc's 6-clause text (`02-resolution-doc.md:223-251`) and the DATA-02/CLM-03 verified facts. No gap to surface.

## Governance Compliance

- Single atomic substantive commit via `scripts/agent-commit` (scope `26-02`, type `spec`, body present), plus one mechanical SHA-backfill follow-up (pre-approved pattern).
- Only the three owned paths staged; no broad staging; no `--no-verify`.
- D-04 perimeter clean: no edits to `sampling_method.md`, `data_quality_assessment.md`, or `pinn/`.
- D-06 honored: M11 packet extended, M12 sub-part byte-stable.

## Self-Check: PASSED

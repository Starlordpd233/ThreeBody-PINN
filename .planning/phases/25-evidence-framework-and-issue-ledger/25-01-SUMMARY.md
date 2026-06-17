---
phase: 25-evidence-framework-and-issue-ledger
plan: 01
type: execute
subsystem: adjudication-machinery
tags: [EVID-06, EVID-07, EVID-08, EVID-09, EVID-10, VER-10, SCOPE-08, SCOPE-09, SCOPE-10, D-03, D-04, D-11, D-13, D-17, D-18, GAP-25-01, GAP-25-02]
milestone: v1.5
execution_status: executed
executed_at: 2026-06-12T12:55:00+08:00
executed_by: gsd-executor-25-01
review_status: pending-plan-25-02
git_branch: gsd-wave1/25-01
recovery_tag: v1.5-pre-phase-25
recovery_tag_sha: 16f782847cb741aa987329665f704ae03f6dd178
base_sha: 16f782847cb741aa987329665f704ae03f6dd178
commit_scope: 25-01
depends_on: ["24.5-resolution-doc-readiness-verification"]
provides:
  - "v1.5 evidence-packet template (12 `##` sections + `### Dataset Evidence (§3b)`)"
  - "v1.5 evidence-packet protocol README (EVID-10 trigger table, D-03 enforcement, ID→filename map, exit-gate interaction per GAP-25-02)"
  - "Re-issued 24-ISSUE-LEDGER.md Lifecycle Rules block scoped to v1.5 phases 26-28 (Phase 29 acceptance)"
affects:
  - "Phases 26, 27, 28: every spec-edit phase inherits the packet-before-edit, phase-exit, and same-commit ledger rules"
  - "Phase 29: acceptance-check build/run consumes the AC-IDs cited by packets"
  - "Plan 25-02: uses the template + README to author the three EVID-10 records (scs-thresholds, compute-globals-D, m11-m12-severity)"
tech-stack:
  added: []
  patterns:
    - "Adjudicated-but-unfixed status legend (PENDING + filled Verdict/Evidence-Packet = adjudicated-but-unfixed; PENDING -> PENDING audit entry)"
    - "Exit-gate interaction: Phase 25 owns records, not fixes; rows become in-scope for the owning spec-edit phase 26-28"
key-files:
  created:
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md"
      line_count: 138
      provides: "v1.5 evidence-packet schema (adapted v1.4 12-section + `### Dataset Evidence (§3b)`)"
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md"
      line_count: 152
      provides: "v1.5 evidence-packet protocol with D-03 enforcement encoding and EVID-10 trigger table"
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/25-01-SUMMARY.md"
      line_count: 78
      provides: "Plan 25-01 execution provenance (this file)"
  modified:
    - path: ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md"
      line_count_change: "+2 -1"
      change_scope: "Lifecycle Rules block: stale applicability token 'Phases 17-22, including Phase 20.5' -> 'Phases 26-28 (spec-edit phases; Phase 29 is the acceptance phase)'. Notes section: one new line recording the D-11 re-issue date and scope (stale applicability text only)."
decisions:
  - "D-04 substitutions applied to v1.4 template: issue-01 source paths -> issue-02; EVID-05 -> EVID-10 conditional markers; sampling_method.md bullet dropped (frozen, SCOPE-08); data_quality_assessment.md added (citable, NEVER editable, SCOPE-09); new `### Dataset Evidence (§3b)` sub-block added referencing 24-VERIFIED-FACTS.md CLM/DATA rows"
  - "D-03 enforcement encoded as new `### D-03 Downstream Enforcement` subsection under Phase-Exit Rule: packet-before-edit (EVID-06), phase-exit gate (VERIFIED/DEFERRED only), same-commit ledger edits"
  - "EVID-10 Trigger Table carries the three v1.5 conflicts: SCS, D=6.694, M11/M12 — three rows total, not the v1.4 set"
  - "ID->Filename map added per Claude's discretion: SCS -> scs-thresholds.md; D=6.694 -> compute-globals-D.md; M11+M12 -> m11-m12-severity.md"
  - "D-13 enforced: Phase 25 mints no new AC-IDs; the seeded AC-PIPE-01..10 and AC-VAL-01..04 stand"
  - "GAP-25-01 status: PENDING -> RESOLVED-WITH-INSTRUCTION (split reading, Option A) verified before mutation"
  - "GAP-25-02 status: RESOLVED-WITH-INSTRUCTION (PENDING convention, Option A) encoded in README status legend; exit-gate interaction 'owns records, not fixes' added per addendum"
  - "D-17 recovery tag: v1.5-pre-phase-25 cut from milestone/v1.5 HEAD before any Phase 25 mutation; no force-tag, no push"
metrics:
  duration_minutes: 8
  tasks_completed: 4
  tasks_total: 4
  files_modified: 1
  files_created: 3
  completed_at: 2026-06-12T12:55:00+08:00
---

# Phase 25 Plan 01: Adjudication Machinery — Summary

**One-liner:** Stand up the v1.5 evidence-packet template + protocol README (with EVID-10 trigger table and D-03 enforcement) and re-issue the seeded ledger's Lifecycle Rules block for v1.5 phases — zero framework-spec edits, zero new AC-IDs.

## Objective

Stand up the v1.5 adjudication machinery (`_TEMPLATE.md`, `README.md`, and a corrected `24-ISSUE-LEDGER.md` Lifecycle Rules block) so Phases 26-28 can copy the schema and operate under the protocol. This is the foundation every downstream phase copies and operates under. Zero framework-spec edits (CONTEXT D-02); zero new verdicts assigned (D-01 split reading — `GAP-25-01` RESOLVED-WITH-INSTRUCTION 2026-06-12, Option A: machinery + 3 EVID-10 records only).

## Execution Notes

### Task 0 — Preflight + recovery tag (D-17)

All preflight gates passed:

- `scripts/agent-commit` executable
- `GAP-25-01` RESOLVED-WITH-INSTRUCTION confirmed in `25-GAPS.md` and mirrored in `v1.5-GAPS.md`
- `24.5-READINESS-REPORT.md` exists with verdict `READY-WITH-CAVEATS`
- v1.4 precedent files exist at `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/{_TEMPLATE.md,README.md,B-02.md}`
- `GIT_AGENT_ID=gsd-executor-25-01` and `GIT_AGENT_OWNED_PATHS` set before authoring

Tag `v1.5-pre-phase-25` cut from milestone/v1.5 HEAD (16f78284) before any Phase 25 mutation. No `-f`, no push.

### Task 1 — `_TEMPLATE.md`

12 `##` sections + `#` title, with the new `### Dataset Evidence (§3b)` sub-block under `## Spec Evidence`. D-04 substitutions applied: issue-01 -> issue-02 paths, EVID-05 -> EVID-10 conditional markers, `sampling_method.md` bullet dropped (frozen, SCOPE-08), `data_quality_assessment.md` added (citable, NEVER editable, SCOPE-09). Verdict enum line carries all five EVID-07 values verbatim. Before/After Spec Note extended to double as the EVID-08 false-positive record. No `sampling_method.md` reference anywhere in the file.

### Task 2 — `README.md`

Sections: Artifact Roles (re-pointed to `24-ISSUE-LEDGER.md` stable path), Primary Sources (issue-02 paths + 4th source = 24-VERIFIED-FACTS.md), Verdict Enum (5-value EVID-07 verbatim), Status Lifecycle (PENDING/IN_PROGRESS/FIX_APPLIED/VERIFIED/DEFERRED verbatim), Status Legend (per GAP-25-02: PENDING + filled Verdict/Evidence-Packet = adjudicated-but-unfixed; exit-gate interaction "Phase 25 owns records, not fixes"), EVID-10 Trigger Table (3 v1.5 conflicts: SCS, D=6.694, M11/M12), Regression Policy + Phase-Exit Rule (Phases 26-28), D-03 Downstream Enforcement (new h3: packet-before-edit, phase-exit gate, same-commit ledger edits), Acceptance Check IDs (D-13: no new AC-IDs), ID→Filename Map (Claude's discretion), Packet Start Procedure (7 steps with §3b source added), Explicit Non-Goals.

### Task 3 — `24-ISSUE-LEDGER.md` Lifecycle Rules block re-issue (D-11)

Mechanical correction of stale v1.4 applicability text only. State machine `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, audit string "FIX_APPLIED is not closure", batch definition "A batch is one GSD plan", transitive-dependent re-verification, and phase-exit gate "only `VERIFIED` or `DEFERRED` for in-scope findings" all preserved verbatim (D-11 KEEP-VERBATIM list, Pitfall 6). One line added to Notes section recording the D-11 re-issue (date + scope = stale applicability text only). Diff confined to the Lifecycle Rules applicability token + the Notes line — no Status Table row, no per-finding row, no Anomalies change.

## Deviations from Plan

None — plan executed exactly as written. The D-04 substitution spec, the EVID-10 trigger table spec, the D-03 enforcement encoding, and the D-11 KEEP-VERBATIM list all applied verbatim.

## Verification Results

| Task | Verify Gate | Result |
|------|-------------|--------|
| 0 | `PREFLIGHT_TAG_OK` (4 gates + tag) | PASS |
| 1 | `TEMPLATE_OK` (9 sub-checks: dir, file, §3b, 12 sections, issue-02 paths, EVID-10 markers, enum, no sampling_method) | PASS |
| 2 | `README_OK` (12 sub-checks: EVID-10 table, phase numbers 26-28, 24-ISSUE-LEDGER link, D-03 h3, 3 filenames, "adjudicated-but-unfixed", "owns records, not fixes") | PASS |
| 3 | `LEDGER_OK` (5 sub-checks: Phases 26-28, no stale token, state machine, audit string, batch definition) | PASS |

`git diff --check` clean. `git diff` confined to the Lifecycle Rules applicability token + the Notes line (D-11 Pitfall 6 honored).

## Commit

One atomic commit via `scripts/agent-commit`, scope `25-01`, body present (touches `.planning/`), all 4 files staged (no user-owned uncommitted file captured). Branch `gsd-wave1/25-01` to be pushed to `origin` after commit.

## Next Plan

Plan 25-02 is unblocked. It uses `_TEMPLATE.md` and `README.md` to author the three EVID-10 records (`scs-thresholds.md`, `compute-globals-D.md`, `m11-m12-severity.md`) and fills the per-finding verdict notes + Evidence-Packet column links for the three ledger rows (SCS, D=6.694, M11/M12) in the same commit as each record (D-06 same-commit discipline).

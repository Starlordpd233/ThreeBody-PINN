---
phase: 20
plan: "01"
subsystem: "Architecture and Normalization Cleanup"
tags:
  - ARCH-01
  - SIREN-initialization
  - omega0-scheduling
  - evidence-gated
dependency_graph:
  requires: []
  provides:
    - "AC-ARCH-01 closure"
    - "B-01 VERIFIED"
    - "B-10 VERIFIED"
  affects:
    - "20-02 (edits pinn_architecture.md after 20-01 commits)"
tech_stack:
  added: []
  patterns:
    - "evidence-first spec cleanup with separate packets sharing one AC"
    - "fixed-contract SIREN initialization with negative scheduler audit"
key_files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-01.md"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-10.md"
  modified:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md"
    - "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
decisions:
  - "SIREN contract: first_omega_0=30, hidden_omega_0=1, standard SIREN init, no epochwise/optimizer-step omega0 scheduler"
  - "Hidden-layer init bounds divided by hidden_omega_0 (not multiplied)"
  - "Stage-boundary omega0 retuning allowed only as ablation with fresh initialization"
  - "B-01 and B-10 remain separate evidence records sharing AC-ARCH-01"
metrics:
  duration: "~1h"
  tasks_completed: 3
  tasks_total: 3
  files_created: 2
  files_modified: 2
  completed: "2026-06-05"
---

# Phase 20 Plan 01: SIREN Initialization and Frequency Cleanup Summary

**One-liner:** Lock the SIREN initialization/frequency contract in `pinn_architecture.md` to fixed `first_omega_0=30`, `hidden_omega_0=1`, with no dynamic scheduler, gated behind completed B-01 and B-10 evidence packets sharing AC-ARCH-01.

## Objective

Close AC-ARCH-01 by making `pinn_architecture.md` state one consistent SIREN initialization/frequency contract — fixed `first_omega_0=30`, `hidden_omega_0=1`, standard SIREN init, divide-by-`hidden_omega_0` bounds, no epochwise/optimizer-step `omega0` scheduler — backed by completed B-01 (hidden-layer initialization) and B-10 (dynamic scheduling) evidence packets.

## Execution Summary

### Task 1: Create and fill B-01 and B-10 evidence packets

Created evidence packets for SIREN hidden-layer initialization (B-01) and dynamic omega0 scheduling (B-10) from the Phase 16 packet template. Each packet includes:

- Source Positions table citing `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md` side by side
- Spec Evidence citing the active `pinn_architecture.md` SIREN/omega0 surfaces
- Verdict: `accept-resolution` for both (sources agree on fixed-contract SIREN with no in-run scheduler)
- FUT-01 Hand-off Note (not applicable — spec cleanup, no formula change)
- Before/After Spec Note and AC-ARCH-01 reference

Ledger updated: B-01 and B-10 rows advanced PENDING → IN_PROGRESS with verdicts recorded.

**Commit:** `0c265ee` — evidence(20): fill B-01/B-10 SIREN omega0 packets and record verdicts

### Task 2: Edit SIREN/omega0 surfaces in pinn_architecture.md

Verdict-gated spec edits applied (both verdicts were `accept-resolution`):

- **Remove dynamic-scheduling block:** Replaced the §2.2 item containing `def update_omega0(...)` and "Exponential reduction to 10" rationale with fixed-contract prose stating `first_omega_0=30` is not scheduled during training and stage-boundary retuning is ablation-only with fresh initialization
- **Fix hidden-layer init direction:** Replaced "scaling of the initialization range by ω₀" with "divided by `hidden_omega_0`" to match the existing formula
- **Hyperparameter table consistency:** Verified §2.4 rows (`first_omega_0=30`, `hidden_omega_0=1`, divide-by form)
- **Architecture Summary consistency:** Verified Initialization row matches the fixed contract
- Removed author note bracketed queries requesting scheduler and hidden-layer clarification

**Commit:** `2a9614a` — spec(20): lock fixed-omega0 SIREN contract, remove dynamic scheduler (ARCH-01)

### Task 3: Closure audit and AC-ARCH-01 verification

**Positive surface audit** confirmed all SIREN/init surfaces state the fixed contract: `first_omega_0=30`, `hidden_omega_0=1`, divide-by form, no scheduling language.

**Negative scheduler audit** confirmed zero active/normative matches for `update_omega0`, `exponential decay`, `final_omega`, `decay_rate`, or any scheduler-variant pattern. Only hits: anti-scheduler prose (our additions) and SI-PINN-002 non-normative provenance metadata (allowed per plan).

**Cross-reference regression check** confirmed the §5.2 input-vector back-reference and summary-table backbone rows are unchanged.

Packets updated with closure-audit notes. Ledger B-01/B-10 advanced IN_PROGRESS → FIX_APPLIED → VERIFIED.

**Commit:** `51baaee` — verify(20): AC-ARCH-01 surface+negative audits pass; B-01/B-10 VERIFIED

## Deviations from Plan

None — plan executed exactly as written.

## Key Decisions

1. **Fixed omega0 contract with no in-run scheduler:** The framework spec now asserts `first_omega_0=30` is never scheduled during training. This locks the v1.3-era dynamic-scheduling ambiguity.
2. **Divide-by hidden_omega_0:** The hidden-layer init formula already divided by `hidden_omega_0` — only the prose description was corrected. No formula changed.
3. **Stage-boundary ablation preserved:** The fixed contract allows omega0 retuning only as a stage-boundary ablation with fresh re-initialization, preserving the research option without the in-run scheduling ambiguity.
4. **Separate packets, shared AC:** B-01 (hidden-layer init) and B-10 (dynamic scheduling) remain separate evidence records with separate verdicts, sharing only the AC-ARCH-01 closure audit.

## Acceptance Check: AC-ARCH-01

**Status:** CLOSED

Evidence trail:
- Completed `evidence/B-01.md` and `evidence/B-10.md` with `accept-resolution` verdicts
- Ledger B-01/B-10 → VERIFIED
- Positive surface audit: fixed omega0, divide-by form, no scheduling language
- Negative scheduler audit: zero active/normative scheduler guidance remains
- Cross-reference regression: input-vector back-reference and backbone rows intact
- No `pinn/` live code read or cited for any verdict

## Known Stubs

None. All evidence packets are complete with verdicts, source citations, and audit records.

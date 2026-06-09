---
phase: 20
plan: "03"
subsystem: "Architecture and Normalization Cleanup"
tags:
  - ARCH-03
  - I_3
  - shape-invariant
  - EVID-05
  - evidence-gated
dependency_graph:
  requires:
    - "20-01"
  provides:
    - "AC-ARCH-03 closure"
    - "M5 VERIFIED"
  affects:
    - "20-04 (reads ctl_instruction.md after 20-03 edits)"
    - "20-05 (reads ctl_instruction.md after 20-03 edits)"
tech_stack:
  added: []
  patterns:
    - "EVID-05 contested adjudication with first-principles geometry check"
    - "source-definition comparison before physics derivation"
key_files:
  created:
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M5.md"
  modified:
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
decisions:
  - "Raw I_3 ∈ [0, 1/3] (0 = collinear, 1/3 = equilateral) grounded in triangle-geometry first principles"
  - "Staging-metadata map: I_3^{in} = 6·I_3 − 1 ∈ [-1, 1]"
  - "I_3 is metadata-only (not a network IC slot under the Phase 17 input contract)"
  - "Resolution-doc position is correct on raw range and mapping; issue-doc assumed [-1,1] range without distinguishing raw-vs-mapped"
  - "autonomous: false per plan — EVID-05 adjudication required STOP-protocol awareness"
metrics:
  duration: "~1.5h"
  tasks_completed: 3
  tasks_total: 3
  files_created: 1
  files_modified: 2
  completed: "2026-06-05"
---

# Phase 20 Plan 03: I_3 Range and Mapping EVID-05 Adjudication Summary

**One-liner:** Adjudicate the contested I_3 normalization range/mapping via the EVID-05 process, align `ctl_instruction.md` to the recorded verdict, and close AC-ARCH-03 with positive+negative surface audits.

## Objective

Close AC-ARCH-03 by recording a grounded EVID-05 verdict for the `I_3` range/mapping and aligning every active `I_3` surface in `ctl_instruction.md` to that verdict, framed as staging metadata (not a network IC slot), with a negative audit showing no contradictory active `I_3` range/mapping remains.

## Execution Summary

### Task 1: EVID-05 adjudication — create and fill the M5 packet

Created the M5 evidence packet as a full EVID-05 contested adjudication with all required sections. The packet includes:

- **Source Positions** side-by-side: resolution doc (`ctl_pinn_resolution.md`) vs issue doc (`01-architecture-and-physics-foundations.md`) on I_3 definition, raw range, and mapping
- **Definition/range/mapping comparison:** Confirmed both sources address the ratio-form quantity `I_3 = (d_short+d_mid-d_long)/(d_short+d_mid+d_long)`, not genuinely different mathematical objects — the dispute is over the raw range annotation and whether a normalization map is stated
- **First-Principles Physics Check:** Applied the conditional triangle-geometry lemma from 20-RESEARCH.md — for three positive side lengths forming a triangle, the ratio `(d_short+d_mid-d_long)/(d_short+d_mid+d_long)` is bounded in `[0, 1/3]` (0 for degenerate collinear, 1/3 for equilateral)
- **Verdict:** `accept-resolution` — resolution doc is correct on raw `I_3 ∈ [0, 1/3]` and the `I_3^{in} = 6·I_3 − 1` staging map; issue doc assumed `[-1, 1]` without distinguishing raw-vs-mapped range
- **Root-Cause Framework Ambiguity:** The spec conflated the raw ratio-form range with the mapped/input range, annotating the raw `I_3` formula as `∈ [-1, 1]`
- **Locked Convention:** raw `I_3 ∈ [0, 1/3]`, staging map `I_3^{in} = 6·I_3 − 1 ∈ [-1, 1]`, metadata-diagnostic-only scope (not a network IC slot)
- **Which Source Was Correct/Wrong:** Resolution correct on raw range and mapping; issue doc correct that a `[-1, 1]` range appears but missed the raw-vs-mapped distinction; resolution correct on metadata-only framing (per GAP-17-05)

Ledger updated: M5 row advanced PENDING → IN_PROGRESS with verdict recorded.

**Commit:** `05f9dfc` — evidence(20): EVID-05 adjudicate M5 I_3 range/mapping; record verdict

### Task 2: Edit I_3 range/mapping in ctl_instruction.md

Verdict-gated spec edits applied (verdict was `accept-resolution`):

- **Correct raw range annotation:** Changed `I_3 = … ∈ [-1, 1]` to `I_3 = … ∈ [0, 1/3]` in §3.4
- **Add staging-metadata map:** Added sentence distinguishing raw descriptor from staging mapping: `I_3^{in} = 6·I_3 − 1 ∈ [-1, 1]`, with metadata-diagnostic-only scope per Phase 17 input contract
- **Cross-surface consistency:** Verified all other `I_3`/`I3` hits are name-lists or scope-framing with no contradictory raw range

**Commit:** `64f2ffc` — spec(20): align I_3 range/mapping to M5 verdict (ARCH-03)

### Task 3: Closure audit and AC-ARCH-03 verification

**Positive surface audit** confirmed every active I_3 surface matches the Locked Convention: raw `I_3 ∈ [0, 1/3]`, `I_3^{in} = 6·I_3 − 1` staging map, metadata-only framing.

**Negative audit** (`rg -n "I_3 *=.*\[-1, ?1\]"`) returned zero matches — no contradictory raw `[-1, 1]` annotation remains.

Packet updated with closure-audit notes. Ledger M5 advanced IN_PROGRESS → FIX_APPLIED → VERIFIED.

**Commit:** `8249172` — verify(20): AC-ARCH-03 I_3 audits pass; M5 VERIFIED

## Deviations from Plan

None — plan executed exactly as written. The definition-comparison step (Task 1 Step 4) confirmed both sources use the same ratio-form I_3 quantity, so the conditional triangle-geometry lemma applied and grounded the `accept-resolution` verdict without needing `defer-with-blocker`.

## Key Decisions

1. **Raw I_3 ∈ [0, 1/3]:** Triangle geometry bounds the ratio-form quantity to `[0, 1/3]` (not `[-1, 1]`). The `[-1, 1]` range in the pre-Phase-20 spec was the mapped/input range misattributed as raw.
2. **Staging-metadata map `I_3^{in} = 6·I_3 − 1`:** The linear map from `[0, 1/3]` to `[-1, 1]` preserves the equilateral/collinear ordering while keeping the mapped value in the standard network-input interval.
3. **Metadata-only scope:** I_3 is not a network IC slot under the Phase 17 input contract (GAP-17-05). The staging map exists for metadata/diagnostic use, not as a live network input surface.
4. **EVID-05 process integrity:** The adjudication followed the full EVID-05 protocol: source-definition comparison first, then first-principles check, then verdict, then Locked Convention. No semantic judgment was invented.

## Acceptance Check: AC-ARCH-03

**Status:** CLOSED

Evidence trail:
- Completed `evidence/M5.md` with all EVID-05-required sections and `accept-resolution` verdict
- Ledger M5 → VERIFIED
- Positive surface audit: raw `[0, 1/3]`, staging map `6·I_3 − 1`, metadata-only framing
- Negative audit: no contradictory raw `[-1, 1]` annotation remains
- First-principles geometry grounding: triangle ratio-form range `[0, 1/3]` derived from side-length ordering
- No `pinn/` live code read or cited for any verdict
- GAP-17-05 (staging-metadata scope) satisfied

## Known Stubs

None. All evidence packets are complete with verdicts, source citations, EVID-05 sections, and audit records.

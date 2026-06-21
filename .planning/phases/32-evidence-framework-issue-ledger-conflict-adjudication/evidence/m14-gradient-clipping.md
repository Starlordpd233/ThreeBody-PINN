# Evidence Packet: M14 - Gradient Clipping Divergence

## Header

| Field | Value |
|---|---|
| ID | `M14` |
| Title | Gradient clipping divergence |
| Severity | MAJOR |
| Current Status | PENDING |
| Current Verdict | accept-resolution |
| Phase | Phase 32 |
| Owner Phase | Phase 32 |
| Consumer Phase | Phase 34 LOOP-04 |
| Acceptance Check ID | AC-LOOP-04 |
| Spec Sections Touched | None in Phase 32; Phase 34 owns `pinn_architecture.md` / `ctl_instruction.md` gradient-clipping transcription |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:100-106`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:463-485` | Non-authoritative issue source | The issue table identifies M14 as a divergence between PINN median-based adaptive clipping and CTL curriculum-aware C schedule, then proposes `clip_value = C_stage * median(grad_norm_history)` with a 100-step rolling window, `C_table` values including midpoint `8.5` for stages 0-1, a `max(median_grad, 1e-6)` lower floor, and clipping after backward. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:52-55` (§1.8); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:134-138` (M14 claim rows); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:197` (DGR-08); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:226` (GAP-08) | candidate verdict source, not authority | §1.8 modifies the issue-doc merge: use `clip_value = C_stage * median(recent global gradient norms)` during Adam only, do not clip in L-BFGS, treat PINN fixed `5.0` as Stage 2/3 instance or fallback, preserve CTL `7-10 / 5 / 3`, do not canonize `8.5`, and leave bootstrap, lower-floor, and stage-history reset rules open. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:52-55`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:88-89`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:147-148`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:205-206` | Navigation / line-map aid | The map anchors M14 to §1.8 lines 52-55, marks it covered, previews the modified structural merge, and carries GAP-08 for unresolved execution details. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1583-1605` establishes Adam as the exploration optimizer and records the stage-boundary Adam-state reset that is separate from gradient-history reset.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1622-1635` already states adaptive global-norm clipping with threshold `C` times a moving median of recent norms and a curriculum-aware C schedule: stages 0-1 use `7-10`, stages 2-3 use `5`, stages 4-6 use `3`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1641-1664` defines L-BFGS refinement and explicitly says no gradient clipping during L-BFGS because line search creates a trust region.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:683-699` establishes the Adam then L-BFGS two-phase optimizer structure.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:700-720` defines adaptive global L2 norm clipping relative to recent typical magnitude and uses fixed `5.0 * median(grad_history)`.

No framework spec is edited in Phase 32.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:49-52` assigns LOOP-04 to the merged gradient-clipping contract with `clip_value = C_stage · median(grad_norm_history)` and a rolling window.
- `.planning/ROADMAP.md:186-190` places the M14 transcription in Phase 34 LOOP-04, after Phase 32 verdicts.
- `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:161-166` classifies the M14 `7-10 / 5 / 3` and `8.5` figures as unverified-but-non-contradicting caveats, not v1.5-verified facts.

No v1.5 dataset fact independently fixes the exact early-stage C value, bootstrap floor, lower floor, or history-reset policy.

## FUT Hand-off Note

- FUT path / note: FUT-04 may implement the training-loop gradient clipping after Phase 34 transcribes the spec contract.
- Not FUT-applicable: This packet does not cite live `pinn/` code. Any future code references are implementation handoff notes only and are NOT grounding.

## First-Principles or Engineering Check

The structural merge is grounded as an engineering invariant because it preserves both current-spec mechanisms without introducing a new ungrounded optimizer behavior:

1. CTL already defines a global-norm clipping threshold as `C` times the moving median of recent norms and supplies the curriculum-aware C schedule `7-10 / 5 / 3`.
2. `pinn_architecture.md` already defines the rolling-median global L2 norm mechanism and uses fixed `5.0 * median(grad_history)`.
3. Therefore `clip_value = C_stage * median(recent global gradient norms)` is the minimal structural merge: the multiplier comes from CTL's stage schedule and the adaptive scale comes from the PINN rolling median.
4. CTL's Stage 2/3 schedule is `C = 5`, so the PINN fixed `5.0` is a Stage 2/3 instance or fallback rather than a second multiplier.
5. Current specs explicitly reserve L-BFGS for trust-region line-search refinement and state no clipping during L-BFGS; the merged rule is therefore Adam-only.

The unresolved execution constants are not grounded in Phase 32. The issue doc chooses `8.5` as a midpoint for the early-stage `7-10` range, uses a `1e-6` lower floor, and initializes median fallback at `1.0`; the resolution doc records these as open/deferred where source support is insufficient. Selecting exact early-stage `C`, bootstrap floor, lower floor, or stage-history reset mechanics would be a source-silent semantic choice and is routed to Phase 34/FUT calibration.

## Verdict

Verdict: accept-resolution

Explicit user instruction: None; the verdict is limited to the grounded structural merge and downstream routing described below.

Reasoning:

- Accept-resolution covers the structural merge only: `clip_value = C_stage * median(recent global gradient norms)` during Adam, with no L-BFGS clipping.
- The structural merge is grounded by current `ctl_instruction.md` and `pinn_architecture.md`, then aligned with the candidate resolution's §1.8 position.
- The packet does not canonize `8.5`, the bootstrap floor, the lower floor, or history-reset mechanics because those details are explicitly open in GAP-08 or not independently grounded.
- Phase 34 owns spec transcription and can preserve the CTL range `7-10 / 5 / 3`, treating `5.0` as the Stage 2/3 instance/fallback rather than an additional multiplier.

## Root-Cause Ambiguity

The root cause is split documentation of one optimizer-safety mechanism. `ctl_instruction.md` records the curriculum-aware multiplier and no-L-BFGS clipping boundary, while `pinn_architecture.md` records the rolling-median adaptive clipping implementation with a fixed `5.0`. The issue doc correctly identifies the structural divergence but over-specifies ungrounded execution details by choosing midpoint `8.5`, lower-floor, fallback, and history mechanics.

## Locked Convention or Owner Route

Locked for Phase 34 transcription:

```text
During Adam only:
clip_value = C_stage * median(recent global gradient norms)
```

Preserve CTL's C schedule as a range/table: `7-10 / 5 / 3`. Do not canonize `8.5` as the early-stage value in Phase 32. Treat PINN fixed `5.0` as the Stage 2/3 instance or fallback.

Owner-routed downstream details:

- Bootstrap median fallback: Phase 34/FUT, unresolved.
- Exact early-stage `C` within `7-10`: Phase 34/FUT, unresolved.
- Lower floor such as `1e-6`: Phase 34/FUT, unresolved.
- Stage-history reset mechanics: Phase 34/FUT, unresolved.

## Which Source Was Correct / Wrong

- Issue doc: correct that the two clipping descriptions should be merged structurally; not grounded when it canonizes the early-stage midpoint `8.5` and execution details.
- Resolution doc: correct on the structural merge, Adam-only scope, no L-BFGS clipping, Stage 2/3 interpretation of `5.0`, and deferral of unresolved execution details, after independent current-spec grounding.
- Current specs: each source-spec contributes part of the final contract; neither alone fully states the merged Phase 34 wording.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` already has adaptive median-based clipping with a curriculum-aware `C` schedule and no L-BFGS clipping; `pinn_architecture.md` already has rolling-median global-norm clipping with fixed `5.0`.

**After:** Phase 32 makes no spec edit. Phase 34 LOOP-04 must transcribe the merged contract: Adam-only `clip_value = C_stage * median(recent global gradient norms)`, no L-BFGS clipping, CTL schedule preserved as `7-10 / 5 / 3`, and unresolved execution constants routed rather than invented.

## Named Acceptance Check

AC-LOOP-04

Planned pass criterion: Phase 34 spec text defines the Adam-only structural merge `clip_value = C_stage * median(recent global gradient norms)`, states no L-BFGS clipping, preserves CTL `7-10 / 5 / 3` without canonizing `8.5`, treats `5.0` as Stage 2/3 instance/fallback, and explicitly defers or FUT-routes bootstrap floor, exact early-stage `C`, lower floor, and history-reset mechanics unless later grounded.

Owning phase: Phase 34, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap opened. The structural merge is grounded by current specs and the candidate resolution doc. The source-silent execution details are not selected; they are routed to Phase 34/FUT under GAP-08, so this packet does not invent a semantic default.

## Status Transition Log

```text
2026-06-21 pending-commit PENDING -> PENDING + accept-resolution (Phase 32 P02 Task 2 by codex-gsd-executor-32-02; adjudicated structural merge, downstream Phase 34 owns transcription)
```

# Evidence Packet: M15 - Energy-Loss Weights

## Header

| Field | Value |
|---|---|
| ID | `M15` |
| Title | Energy-loss weights |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 35` |
| Owner Phase | `Phase 35` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOSS-02` |
| Spec Sections Touched | `ctl_instruction.md` Loss Function Formulation; `pinn_architecture.md` PHYS-05 warmup schedule |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The issue doc is a non-authoritative conflict source, and the final resolution doc is a candidate verdict source consumed under the Phase 32 evidence protocol.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:105`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:366-379`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:432`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:457` | Non-authoritative issue source | The issue doc claims late-stage `lambda_E=1000` dominance risk, proposes a capped hybrid schedule with cap values through `500`, adds an adaptive reduction when energy is already conserved, and flags energy-weight interaction with gradient clipping. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:56-58` (§1.9 M15); `03-final-resolution.md:139-142` (M15-01..04); `03-final-resolution.md:198-199` (DGR-09, DGR-10); `03-final-resolution.md:227` (GAP-09) | Candidate verdict source, not authority | §1.9 rejects the issue premise and CLM-11 cap table as replacements, retains the current PHYS-05 schedule whose maximum is `1`, and requires logging weighted losses, scheduled weights, and gradient statistics before designing any control law. M15-04 and GAP-09 defer automatic dominance control. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:54`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:89`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:148`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:206` | Navigation / line-map aid | Maps M15 to §1.9 lines 56-59, marks the finding covered, records the rejected disposition, and routes energy dominance control to Phase 35 LOSS-02. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:625-656` defines the PHYS-05 total loss and warmup schedule. The current `lambda_E^max(k)` schedule is `0` for stages 0-1, `10^(k-4)` for stages 2-4, and `1` for stages 5-6; it therefore has maximum scheduled conservation weights at or below `1`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:661-666` freezes lambda values during L-BFGS and applies re-warmup at stage boundaries.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1722-1751` defines the total-loss assembly by reference to the PHYS-05 loss-term catalog and states that Phase 35 owns the component definition, weight schedule, and Huber-delta calibration details.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `.planning/REQUIREMENTS.md:92-95` define SCOPE-12 through SCOPE-15: locked v1.4/v1.5 outcomes are hard constraints; v1.6 spec edits are limited to `ctl_instruction.md` and `pinn_architecture.md`; training-loop code and empirical EDA remain FUT.
- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md:26-32` states the Phase 35 target for LOSS-02: reject the cap table and stale `lambda_E = 1000` premise as replacements, retain PHYS-05 max `lambda_E <= 1`, require logging, and defer automatic dominance reweighting.
- `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md:110-118` records D-35-07 with the same source-precedence and logging-first discipline.

No dataset evidence is needed for this packet because the resolution doc explicitly defers measured dominance control until weighted-loss and gradient evidence exists.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 or a later calibration phase may design an automatic energy-dominance controller only after logging weighted losses, scheduled weights, and gradient statistics. Live `pinn/` code is NOT grounding evidence and is not cited here.
- Not FUT-applicable: This packet records the Phase 35 evidence state only; it does not implement training logic.

## First-Principles or Engineering Check

1. **Schedule boundary:** The current PHYS-05 schedule is explicitly capped at `lambda_E^max <= 1`. Replacing it with cap values up to `500` would be a semantic change, not a clarification.
2. **Control-law evidence:** Automatic dominance control depends on observed weighted losses and gradients. Without measurements, a rule like `lambda_E * L_energy > 10 * L_data` has no grounded scale basis across stages or optimizers.
3. **Source precedence:** The issue doc identifies a plausible dominance risk but proposes a concrete schedule the resolution doc rejects. The grounded packet outcome is therefore to retain the existing schedule, add logging as evidence collection, and defer any controller.

## Verdict

Verdict: `accept-resolution` (resolution-doc M15 position: `rejected` as an issue-doc replacement, with dominance control deferred)

Explicit user instruction: None beyond the Phase 35 SPEC/CONTEXT lock.

Reasoning:

- The candidate resolution doc §1.9 rejects the issue-doc cap table and stale `lambda_E = 1000` premise, and DGR-09 states the retained PHYS-05 schedule has max <= 1.
- DGR-10 and GAP-09 require logging weighted losses and gradients first, so automatic dominance reweighting is not grounded as a current rule.
- The current framework spec already contains the max <= 1 PHYS-05 schedule; Phase 35 later spec edits should tag and cross-reference it, not replace it.

## Root-Cause Ambiguity

The issue doc treated a late-stage dominance risk and a proposed cap schedule as an implementation correction. The framework spec already had a bounded PHYS-05 conservation-weight schedule, and no measured weighted-loss or gradient evidence supported a replacement controller. The ambiguity was whether M15 was a schedule bug or a logging/calibration gap; the resolution doc settles it as the latter.

## Locked Convention or Owner Route

Locked for Phase 35 transcription:

```text
M15 / LOSS-02:
- Reject the issue-doc capped-hybrid cap table as a replacement.
- Reject the stale lambda_E = 1000 premise.
- Retain the PHYS-05 warmup schedule with lambda_E^max <= 1.
- Require logging of weighted losses, scheduled weights, and gradient statistics.
- Defer any automatic dominance reweighting until measured evidence exists.
```

## Which Source Was Correct / Wrong

- Issue doc: correct that energy-weight dominance needs attention and logging; wrong as a source of a replacement cap table or automatic controller.
- Resolution doc: correct in rejecting the replacement schedule, retaining PHYS-05 max <= 1, and deferring dominance control pending measured evidence.
- Current specs: correct baseline schedule; later Phase 35 edits should add verdict/status callouts and logging requirements without adopting the cap table.

## Before / After or Intentional Non-Change Note

**Before:** `pinn_architecture.md:625-656` already contains the PHYS-05 max <= 1 conservation-weight schedule, but it is not tagged as the Phase 35 M15 / LOSS-02 `rejected as issue-doc replacement` verdict and does not yet state the M15 logging-first requirement.

**After:** Phase 35 spec-edit plans should add a LOSS-02 callout and logging requirement while preserving the existing schedule. The cap table up to `500`, `lambda_E = 1000`, and automatic dominance reweighting must remain rejected or deferred, not locked.

## Named Acceptance Check

AC-LOSS-02

Planned pass criterion: the edited framework specs expose `LOSS-02`, `M15`, `rejected`, and the retained PHYS-05 maximum `lambda_E <= 1`; no cap table through `500`, stale `lambda_E = 1000` premise, or automatic dominance controller appears as a locked schedule.

Owning phase: Phase 35, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap opened. The required target fields are explicitly grounded: rejection of the cap table and stale premise, retention of max <= 1, logging fields, and dominance-control deferral are all named in `03-final-resolution.md:56-58`, `03-final-resolution.md:198-199`, and `03-final-resolution.md:227`.

## Status Transition Log

```text
2026-06-29 pending-commit PENDING -> IN_PROGRESS (Phase 35 Plan 35-01 Task 1 by codex-gsd-executor-35-01; packet authored, M15 accept-resolution consumed)
```

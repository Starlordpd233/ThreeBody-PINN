# Evidence Packet: ALM mu_p clamp - ALM mu_p Clamp

## Header

| Field | Value |
|---|---|
| ID | `ALM mu_p clamp` |
| Title | ALM mu_p clamp |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `defer-with-blocker` |
| Phase | `Phase 34` |
| Owner Phase | `Phase 34` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOOP-05` |
| Spec Sections Touched | `pinn_architecture.md` §4.2 Optional ALM Ablation; `ctl_instruction.md` Total-Loss / Data-Flow ordering skeleton (pointer only) |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:117`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:319`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:489-494` | Non-authoritative issue source | The issue table flags that `mu_p` can diverge without clamping and recommends `mu_p = np.clip(mu_p, 1e-4, 100.0)` in the ALM update step. The ALM parameter-update pseudocode (lines 489-494) shows an RMSprop-style moving-average variance update. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:92-95` (§1.18 ALM); `03-final-resolution.md:182` (claim ALM-03 defer); `03-final-resolution.md:237` (GAP-19) | candidate verdict source, not authority | §1.18 defers: the default loss has no `mu_p` because dense-residual ALM is rejected. A clamp could apply only to an optional scalar-conservation ALM after that ablation defines constraint normalization, penalty update law, state reset/persistence, and update cadence. The exact `[1e-4, 100]` bounds and RMSprop-style update are not adopted. Claim ALM-03 defers the clamp as missing-specification; GAP-19 records that scalar-constraint update law, normalization, state reset, and clamp sensitivity are unspecified. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `31-RESOLUTION-MAP.md:63-64`; `31-RESOLUTION-MAP.md:98-99`; `31-RESOLUTION-MAP.md:216-217` (GAP-19 route) | Navigation / line-map aid | Maps ALM mu_p clamp to §1.18 lines 92-95, marks it `covered (with routing — defer)`, and routes GAP-19 to Phase 34 LOOP-05. |

## Current Spec Evidence

- `pinn_architecture.md:671-682` documents the Optional ALM Ablation (P2): scalar conservation constraints only (`c_E`, `c_{L,α}`), "Never apply ALM to the dense ODE residual," dual updates only between Adam epochs, and "Default: ALM is OFF. The default loss is the penalty-term formulation in §3-§4 above."
- `ctl_instruction.md:1743-1745` rejects the previous pseudo-ALM formulation and states that "Optional ALM for scalar conservation constraints only is documented as a P2 ablation in the PHYS-05 ablation section of `pinn_architecture.md`."
- `ctl_instruction.md:1718-1745` defines the default total-loss formulation with penalty-term weights, not ALM dual variables.
- `pinn_architecture.md:700-723` defines the adaptive gradient-clipping mechanism (LOOP-04, consumed separately via the M14 packet).

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `34-SPEC.md:88` enforce SCOPE-12: 14D input `[τ, IC₁₃]`, Jacobi IC frame, mass-weighted COM projection head, `eps_soft = 1e-5`, post-v1.3 SCS gate, raw-mass `D ≈ 4.6416` (not `6.694`), and v1.5 DataLoader / validation-metric contracts.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` locks the raw-mass `D ≈ 4.6416` convention (v1.5 EVID-10).
- The default training loss is already penalty-term-based; no v1.5-verified fact requires ALM in the default loop.

This packet verifies that the ALM deferral does not disturb any SCOPE-12 locked convention.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may implement the optional scalar-conservation ALM ablation after its update law, normalization, reset/persistence, and cadence are defined. Live `pinn/` code is NOT grounding evidence for the deferral and may only be referenced as an implementation hand-off note.
- Not FUT-applicable: The packet itself records only the adjudicated deferral.

## First-Principles or Engineering Check

1. **Default loss is penalty-term based:** Both current specs define the default training loss as a weighted sum of data, IC, physics, energy, and angular-momentum terms. ALM dual variables are not part of the default loss.
2. **Dense-residual ALM is rejected:** Squaring a nonnegative ODE residual produces a quartic that is not a standard equality-constrained augmented Lagrangian. The specs already reject this.
3. **Scalar-conservation ALM is an optional ablation:** Even for scalar constraints (energy, angular momentum), the ablation requires defining constraint normalization, the penalty-update law, state reset/persistence, and update cadence before a clamp bound can be meaningful.
4. **Clamp bounds are ungrounded:** `[1e-4, 100]` is a numerical proposal without a verified sensitivity analysis or constraint-normalization basis. Adopting it in the default loop would introduce an ungrounded hyperparameter.
5. **No regression of optimizer semantics:** The default Adam step remains ALM-free; any optional ALM step is explicitly marked deferred and conditional.

## Verdict

Verdict: `defer-with-blocker`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.18 `defer` verdict is independently grounded by the current specs, which already reject dense-residual ALM and document ALM only as an optional scalar-conservation P2 ablation.
- Claim ALM-03 defers the clamp as missing-specification; GAP-19 records the unspecified ablation mechanics.
- The default training-step contract will NOT include a dense-residual ALM update or a `mu_p` clamp.
- The `[1e-4, 100]` bounds and RMSprop-style update are carried as deferred/not adopted; they may apply only to a future optional scalar-conservation ALM ablation after its update law is defined.

## Root-Cause Ambiguity

The root cause is a missing ablation specification. The issue doc treats ALM as part of the default training loop and proposes a clamp for `mu_p`, but the current specs and resolution doc agree that dense-residual ALM is rejected and scalar-conservation ALM is an optional, not-yet-defined ablation. Without constraint normalization and an update law, a clamp bound has no grounding.

## Locked Convention or Owner Route

Owner route / deferral for Phase 34 transcription:

```text
ALM parameter-update contract is DEFERRED to a future optional scalar-conservation ALM ablation.
- Default loss has NO mu_p and NO dense-residual ALM (dense-residual ALM is REJECTED).
- ALM remains an optional scalar-conservation add-on only (pinn_architecture.md §4.2 P2 ablation).
- A mu_p clamp could apply only after the ablation defines:
    * constraint normalization,
    * penalty update law,
    * state reset/persistence,
    * update cadence.
- The exact [1e-4, 100] bounds and the RMSprop-style update are NOT adopted.
```

No ALM update step is locked into the default training loop.

## Which Source Was Correct / Wrong

- Issue doc: identifies a real risk (`mu_p` divergence) but applies it to the wrong context (default ALM loop). The proposed `[1e-4, 100]` clamp is not grounded for the default loss.
- Resolution doc: correct in rejecting dense-residual ALM from the default loss, limiting ALM to an optional scalar-conservation ablation, and deferring the clamp until the ablation is specified.
- Current specs: already place ALM as optional/OFF and reject the pseudo-ALM formulation; Phase 34 will record the deferral explicitly without changing the default loss.

## Before / After or Intentional Non-Change Note

**Before:** `pinn_architecture.md:671-682` already documents ALM as optional/OFF/scalar-only and rejects dense-residual ALM. `ctl_instruction.md:1743-1745` already rejects the pseudo-ALM formulation. Neither spec includes a `mu_p` clamp in the default loop.

**After:** Phase 34 Plan 34-02/34-04 will transcribe the ALM contract with an explicit `> **Phase 34 contract: ALM mu_p clamp (LOOP-05; deferred; AC-LOOP-05; ...)**` callout, recording that the default loss has no `mu_p`, dense-residual ALM is rejected, and any clamp is conditional on a future optional scalar-conservation ablation. No `mu_p` clamp or RMSprop-style update is adopted into the default training step.

## Named Acceptance Check

AC-LOOP-05

Planned pass criterion: `pinn_architecture.md` / `ctl_instruction.md` state that dense-residual ALM is rejected from the default loss, ALM remains optional/OFF, and any `mu_p` clamp `[1e-4, 100]` / RMSprop-style update is carried as deferred/conditional on a future scalar-conservation ALM ablation; the default training-step contract does not include a dense-residual ALM update; no framework spec is edited before this packet exists.

Owning phase: Phase 34, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap is opened by this packet. The ALM disposition is source-routed: §1.18 records `defer`, claim ALM-03 defers the clamp as missing-specification, and GAP-19 explicitly routes the decision to specifying the ablation before choosing bounds. Because the source already provides the route, a new STOP gap would pollute the register. The deferral is recorded as a conditional/owner-pending contract in the LOOP-05 body.

## Status Transition Log

```text
2026-06-25 pending-commit PENDING -> IN_PROGRESS (Phase 34 Plan 34-01 Task 3 by claude-gsd-executor-34-01; packet authored, ALM defer consumed)
```

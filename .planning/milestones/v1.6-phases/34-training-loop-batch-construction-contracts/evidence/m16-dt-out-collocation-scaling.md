# Evidence Packet: M16 - dt_out-Aware Collocation Scaling

## Header

| Field | Value |
|---|---|
| ID | `M16` |
| Title | dt_out-aware collocation scaling |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `defer-with-blocker` |
| Phase | `Phase 34` |
| Owner Phase | `Phase 34` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOOP-06` |
| Spec Sections Touched | `ctl_instruction.md` Mini-Batch Construction forward-interface note (`dt_out`/`n_snapshots` metadata) |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:106`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:440` | Non-authoritative issue source | The issue table and action list propose `n_col = base * (dt_base / dt_out)` as a scaling direction, with specific ratios for gold/hierarchical/standard base datasets, claiming low-resolution trajectories are under-constrained. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:60-63` (§1.10 M16); `03-final-resolution.md:144-145` (claims M16-02 defer / M16-03 rejected); `03-final-resolution.md:228` (GAP-10) | candidate verdict source, not authority | §1.10 defers: verified `dt_out` values do not establish a collocation-density objective or direction. Keep `dt_out`/`n_snapshots` as metadata and retain the present fixed/configurable collocation budget. Do not adopt CLM-20's `dt_base/dt_out` factors or the inverse. Claim M16-02 defers the scaling objective; M16-03 rejects the CLM-20 `dt_base/dt_out` direction as claimed-unverified. GAP-10 records that objective, direction, caps, rounding, and fixed-compute budget are undefined. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `31-RESOLUTION-MAP.md:53-54`; `31-RESOLUTION-MAP.md:90-91`; `31-RESOLUTION-MAP.md:207-208` (GAP-10 route) | Navigation / line-map aid | Maps M16 to §1.10 lines 60-63, marks it `covered (with routing — defer)`, and routes GAP-10 to Phase 34 LOOP-06. |

## Current Spec Evidence

- `ctl_instruction.md:1775` exposes `dt_out(traj)` and `n_snapshots(traj)` as metadata and explicitly labels them as the "forward interface for the deferred M16 collocation-density question -- doc-03; not used here".
- `pinn_architecture.md` §3.2 defines the physics residual evaluation on collocation points but does not prescribe a `dt_out`-dependent density.
- `ctl_instruction.md:1718-1745` references PHYS-05 in `pinn_architecture.md` for loss-term definitions and weights; no `dt_out`-scaling formula is present in either spec.
- `pinn_architecture.md:671-682` documents the optional ALM ablation and states that the default loss is the penalty-term formulation, not an ALM-driven dense residual.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `34-SPEC.md:88` enforce SCOPE-12: 14D input `[τ, IC₁₃]`, Jacobi IC frame, mass-weighted COM projection head, `eps_soft = 1e-5`, post-v1.3 SCS gate, raw-mass `D ≈ 4.6416` (not `6.694`), and v1.5 DataLoader / validation-metric contracts.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` locks the raw-mass `D ≈ 4.6416` convention (v1.5 EVID-10).
- The v1.5 forward-reference for `dt_out`/`n_snapshots` metadata (PIPE-08 / SCOPE-11) is realized-as-deferred by this packet; no v1.5-verified fact fixes a collocation-density objective.

This packet verifies that the M16 deferral does not disturb any SCOPE-12 locked convention.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may later run a fixed-compute ablation comparing constant and candidate `dt_out`-aware collocation policies after Phase 34 records the deferral. Live `pinn/` code is NOT grounding evidence for the deferral and may only be referenced as an implementation hand-off note.
- Not FUT-applicable: The packet itself records only the adjudicated deferral.

## First-Principles or Engineering Check

1. **`dt_out` is a metadata property, not a loss objective:** The verified `dt_out` distribution is an empirical fact about the training corpus (CLM-17/VF-1). It does not, by itself, define how many collocation points are needed to train the network.
2. **Scaling direction is ungrounded:** `n_col ∝ dt_base/dt_out` is one possible heuristic, but the resolution doc and claim M16-03 reject it as claimed-unverified. The inverse `n_col ∝ dt_out/dt_base` is equally ungrounded and is explicitly not adopted.
3. **Fixed-compute ablation required:** A collocation-density policy affects training cost, memory, and residual variance trade-offs. Selecting one without a fixed-compute ablation would be a source-silent engineering choice.
4. **No regression of existing contracts:** The current fixed/configurable collocation budget and the `dt_out` metadata forward interface remain intact; the deferral is recorded as `realized-as-deferred` rather than introducing a new formula.

## Verdict

Verdict: `defer-with-blocker`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.10 `defer` verdict is independently grounded: the current spec exposes `dt_out`/`n_snapshots` metadata but uses a fixed/configurable collocation budget, and no v1.5-verified fact establishes a scaling objective.
- Claim M16-02 defers the objective/direction; claim M16-03 rejects the CLM-20 `dt_base/dt_out` direction as claimed-unverified.
- The audit `n_col ∝ dt_base/dt_out` direction is recorded **only** as the deferred candidate direction, not as a locked or probe-able contract, and the inverse form is explicitly not adopted.
- The v1.5 SCOPE-11/PIPE-08 forward-reference is **realized-as-deferred**: the metadata interface is preserved, but no scaling formula is transcribed.

## Root-Cause Ambiguity

The root cause is a conflation of dataset heterogeneity (`dt_out` varies 17×) with an unsubstantiated training objective. The issue doc treats `dt_out` as a direct driver of collocation density; the resolution doc and current spec agree that the link between `dt_out` and required collocation density has not been established.

## Locked Convention or Owner Route

Owner route / deferral for Phase 34 transcription:

```text
M16 dt_out-aware collocation scaling is DEFERRED to FUT.
- Keep dt_out(traj) and n_snapshots(traj) exposed as metadata.
- Retain the present fixed/configurable collocation budget.
- The candidate direction n_col ∝ dt_base/dt_out is recorded ONLY as a deferred
  candidate direction (not transcribed as a locked or probe-able contract).
- The inverse form n_col ∝ dt_out/dt_base is explicitly NOT adopted.
- The v1.5 SCOPE-11/PIPE-08 forward-reference is realized-as-deferred.
```

No numeric scaling formula is locked. A fixed-compute ablation in FUT-01/FUT-04 is the required next step before any `dt_out`-scaling policy can be adopted.

## Which Source Was Correct / Wrong

- Issue doc: identifies the `dt_out` heterogeneity correctly but over-reaches by prescribing `n_col ∝ dt_base/dt_out` without verified grounding; the direction is not adopted.
- Resolution doc: correct in deferring the collocation-density objective, rejecting CLM-20's `dt_base/dt_out` factors, and routing the decision to a fixed-compute ablation.
- Current specs: already preserve the metadata interface and a fixed/configurable collocation budget; the M16 contract records the deferral rather than changing the budget.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md:1775` exposes `dt_out`/`n_snapshots` metadata with a forward-reference to the deferred M16 question, but the deferral is not yet formalized as a normative contract.

**After:** Phase 34 Plan 34-02/34-03 will transcribe the M16 contract with an explicit `> **Phase 34 contract: dt_out-aware collocation scaling (LOOP-06; deferred; AC-LOOP-06; ...)**` callout, recording the deferral, the candidate-direction-only note, the explicit non-adoption of the inverse form, and the realized-as-deferred v1.5 SCOPE-11/PIPE-08 forward-reference. No `dt_out`-scaling formula will be transcribed and no probe will be added.

## Named Acceptance Check

AC-LOOP-06

Planned pass criterion: `ctl_instruction.md` records the M16 `defer` disposition (§1.10), preserves `dt_out`/`n_snapshots` metadata, retains a fixed/configurable collocation budget, states `n_col ∝ dt_base/dt_out` only as a deferred candidate direction (not transcribed/probe-able), explicitly does not adopt the inverse form, and marks the v1.5 SCOPE-11/PIPE-08 forward-reference as `realized-as-deferred`; no framework spec is edited before this packet exists.

Owning phase: Phase 34, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap is opened by this packet. The M16 disposition is source-routed: §1.10 records `defer`, claim M16-02 defers the objective, and GAP-10 explicitly routes the decision to a fixed-compute ablation. Because the source already provides the route, a new STOP gap would pollute the register. The deferral is recorded as `realized-as-deferred` in the LOOP-06 contract body.

## Status Transition Log

```text
2026-06-25 pending-commit PENDING -> IN_PROGRESS (Phase 34 Plan 34-01 Task 3 by claude-gsd-executor-34-01; packet authored, M16 defer consumed)
```

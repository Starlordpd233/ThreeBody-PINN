# Evidence Packet: B-08 - Data versus Collocation Points

## Header

| Field | Value |
|---|---|
| ID | `B-08` |
| Title | Data versus collocation points |
| Severity | `BLOCKING` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 34` |
| Owner Phase | `Phase 34` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOOP-02` |
| Spec Sections Touched | `ctl_instruction.md` Mini-Batch Construction with Lookahead Sampling; `pinn_architecture.md` §3 loss-term definitions (pointer-only) |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:95` | Non-authoritative issue source | The issue table identifies B-08 as blocking because data-fidelity and collocation points are conflated. It proposes two independent point sets: 8192 data points from Brutus snapshots with L1 loss, and 4096 collocation points from `[0,T]` for physics+energy loss, both with a 50/50 mix. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:40-43` (§1.5 B-08); `03-final-resolution.md:224` (GAP-06) | candidate verdict source, not authority | §1.5 modifies the issue-doc position: make two independent logical point sets explicit (discrete Brutus snapshots for Huber data loss; continuous collocation points for physics; energy reuses the physics collocation set). A single concatenated forward pass is permitted but does not merge the loss roles. `8192/4096` are example/provisional budgets, and actual data count follows the per-trajectory cap. The mandatory 50/50 mixed continuous collocation sampler is deferred (GAP-06). |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `31-RESOLUTION-MAP.md:50-51`; `31-RESOLUTION-MAP.md:85-86`; `31-RESOLUTION-MAP.md:203-204` (GAP-06 route) | Navigation / line-map aid | Maps B-08 to §1.5 lines 40-43, marks it `covered`, notes the `modified` verdict, and routes GAP-06 to Phase 34 LOOP-02/LOOP-03. |

## Current Spec Evidence

- `ctl_instruction.md:1770-1784` defines the data-fidelity mini-batch construction (`n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, 50/50 weighted/uniform data split) and exposes `dt_out`/`n_snapshots` metadata; it does not yet formalize the collocation point set as a separate logical entity.
- `pinn_architecture.md:323-352` carries Listing 2 `get_batch()` and the PIPE-04 note pointing to `ctl_instruction.md` for the operative data-loss sampling rule. It also notes that physics and conservation terms are balanced by scheduled scalar weights, not default ALM dual updates.
- `ctl_instruction.md:1718-1745` states the total-loss formulation and references the PHYS-05 loss-term catalog in `pinn_architecture.md` for the definitions of `L_data`, `L_IC`, `L_phys^causal`, `L_E`, and `L_L`.
- The rejection of dense-residual ALM and the optional scalar-conservation ALM ablation is already recorded in `ctl_instruction.md:1743-1745` and `pinn_architecture.md:671-682`.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `34-SPEC.md:88` enforce SCOPE-12: 14D input `[τ, IC₁₃]`, Jacobi IC frame, mass-weighted COM projection head, `eps_soft = 1e-5`, post-v1.3 SCS gate, raw-mass `D ≈ 4.6416` (not `6.694`), and v1.5 DataLoader / validation-metric contracts.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` locks the raw-mass `D ≈ 4.6416` convention (v1.5 EVID-10).
- `ctl_instruction.md:1775` already exposes `dt_out(traj)` and `n_snapshots(traj)` metadata, preserving the M12 locked snapshot-count verdict and the M16 forward interface.

This packet verifies that the B-08 contract does not disturb any SCOPE-12 locked convention.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may implement the two-point-set DataLoader / sampler after Phase 34 transcribes the spec contract. Live `pinn/` code (e.g., `pinn/data-processing-pipeline-full.py`) is NOT grounding evidence and may only be referenced as an implementation hand-off note.
- Not FUT-applicable: The packet itself records only the adjudicated spec contract.

## First-Principles or Engineering Check

1. **Role separation:** Data-fidelity points must coincide with high-precision BRUTUS snapshots; collocation points are free samples from `[0,T]` used to evaluate the physics and energy residuals. Conflating the two either wastes snapshots as collocation-only points or forces physics loss onto sparse snapshot times.
2. **Single forward pass allowance:** Passing both point sets through the network in one batch is an implementation convenience; it does not merge the loss roles because the data loss is evaluated only at snapshot times and the physics/energy losses are evaluated only at their respective collocation times.
3. **Budget examples are provisional:** `8192` and `4096` are illustrative totals (`256 trajectories × 32 points/trajectory = 8192` data points; `4096` collocation points). The actual data count is per-trajectory capped by `min(n_pts_cap, n_snapshots)`, so the example budget cannot be a hard requirement.
4. **Collocation 50/50 is deferred:** A mandatory mixed continuous collocation sampler is not grounded by the current spec or by verified dataset evidence; deferring it under GAP-06 is the only safe disposition.

## Verdict

Verdict: `accept-resolution`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.5 `modified` verdict is independently grounded by the need to keep data-fidelity points tied to BRUTUS snapshots and collocation points free in `[0,T]`, a distinction already implicit in the current spec's PHYS-05 loss catalog.
- The two-point-set contract, single-forward-pass allowance, and provisional `8192/4096` example budgets are preserved with a source citation; the actual data count follows the per-trajectory cap rule from B-07.
- The mandatory collocation 50/50 mix is deferred per GAP-06; Phase 34 will record this deferral rather than invent a continuous sampler.
- The B-08 contract is consistent with the SI-PINN-003 canonical-home decision: `ctl_instruction.md` owns batch construction; `pinn_architecture.md` keeps loss-term definitions and points to `ctl_instruction.md` for batch construction.

## Root-Cause Ambiguity

The root cause is an under-specified boundary between data-fidelity sampling (which must respect the discrete BRUTUS snapshots) and collocation sampling (which is continuous and physics-driven). The issue doc over-specifies a mandatory 50/50 mix and exact budgets; the current spec does not yet state the separation as a normative contract.

## Locked Convention or Owner Route

Locked/provisional for Phase 34 transcription:

```text
Two independent logical point sets:
  1. Data-fidelity points: sampled from BRUTUS trajectory snapshots
     (n_pts(traj) = min(n_pts_cap, n_snapshots(traj)), without replacement,
     50/50 acceleration-weighted/uniform split retained from B-07).
  2. Collocation points: continuous samples from [0,T] for physics residual
     and energy residual evaluation (energy reuses the physics collocation set).
A single concatenated forward pass is permitted but does not merge the loss roles.
8192/4096 are example/provisional budgets; actual data count follows the per-trajectory cap.
```

Owner-pending / deferred route:

- A mandatory 50/50 mixed continuous collocation sampler is **deferred** per GAP-06 (`03-final-resolution.md:224`). Phase 34 will record the deferral in the LOOP-03/LOOP-02 contract body with a forward-reference; it will not invent the sampler.

## Which Source Was Correct / Wrong

- Issue doc: correct that data-fidelity and collocation point sets must be separated; not authoritative for the exact `8192/4096` budgets or for mandating a collocation 50/50 mix.
- Resolution doc: correct in making the two-point-set separation explicit, tagging the budgets as provisional, allowing a single concatenated forward pass, and deferring the collocation mix under GAP-06.
- Current specs: `ctl_instruction.md` already owns the data-fidelity sampling rule; `pinn_architecture.md` owns the loss-role definitions. The B-08 contract reinforces this split without duplicating normative text.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md:1770-1784` defines the data-fidelity mini-batch but does not explicitly state the two-point-set separation or tag the `8192/4096` figures as provisional; the collocation 50/50 is not mandated, but its deferred status is not yet formally recorded.

**After:** Phase 34 Plan 34-02/34-03 will transcribe the B-08 contract with an explicit `> **Phase 34 contract: Data versus collocation points (LOOP-02; provisional; AC-LOOP-02; ...)**` callout, the two-point-set separation, the single-forward-pass allowance, provisional `8192/4096` budgets, and a forward-reference recording that the collocation 50/50 mixed sampler is deferred (GAP-06). No mandatory collocation sampler is locked.

## Named Acceptance Check

AC-LOOP-02

Planned pass criterion: `ctl_instruction.md` states the two-independent-point-set contract (data-fidelity snapshots vs collocation points), permits a single concatenated forward pass without merging loss roles, tags `8192/4096` as provisional/example budgets, and records the collocation 50/50 mixed sampler as deferred with a GAP-06 citation; no framework spec is edited before this packet exists.

Owning phase: Phase 34, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap is opened by this packet. The structural contract is grounded by the current `ctl_instruction.md` / `pinn_architecture.md` split and the resolution doc §1.5 `modified` verdict. The deferred collocation 50/50 mixed sampler is recorded as a future work item under GAP-06 (`03-final-resolution.md:224`) and will be transcribed as `deferred` in the LOOP-02/LOOP-03 contract body; it is not invented here.

## Status Transition Log

```text
2026-06-25 pending-commit PENDING -> IN_PROGRESS (Phase 34 Plan 34-01 Task 2 by claude-gsd-executor-34-01; packet authored, B-08 accept-resolution consumed)
```

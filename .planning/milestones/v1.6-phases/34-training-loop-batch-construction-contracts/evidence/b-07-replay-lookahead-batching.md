# Evidence Packet: B-07 - Replay/Lookahead Batching

## Header

| Field | Value |
|---|---|
| ID | `B-07` |
| Title | Replay/lookahead batching |
| Severity | `BLOCKING` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 34` |
| Owner Phase | `Phase 34` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOOP-01` |
| Spec Sections Touched | `ctl_instruction.md` Mini-Batch Construction with Lookahead Sampling |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative conflict source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:94-95` | Non-authoritative issue source | The issue table identifies B-07 as blocking because `get_batch()` uses flat 256 random trajectories, while CTL requires 240 replay (stages $\leq k$) + 16 lookahead (stage $k+1$), with `n_pts=32` and a 50/50 uniform/acceleration-weighted split. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:36-39` (§1.4 B-07); `03-final-resolution.md:122` (claim B07-04 `rejected`); `03-final-resolution.md:123` (claim B07-05 `defer`); `03-final-resolution.md:223` (GAP-05) | candidate verdict source, not authority | §1.4 modifies the issue-doc position: keep stage-aware replay/lookahead through the locked query interfaces, keep `240/16` for a 256-trajectory batch and `n_pts_cap = 32` as configurable **provisional defaults** (not verified optimums), preserve `min(n_pts_cap, n_snapshots)` without replacement with the current weighted/uniform split, and note that final-stage, undersized-next-stage, and replacement policies remain unspecified and must be made deterministic. Claim B07-04 rejects `pinn_architecture.md` §3.1 PIPE-04/SI-PINN-003 batch construction; B07-05 defers the edge-case policy as source-silent (GAP-05). |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `31-RESOLUTION-MAP.md:49-50`; `31-RESOLUTION-MAP.md:84-85`; `31-RESOLUTION-MAP.md:202-203` (GAP-05 route) | Navigation / line-map aid | Maps B-07 to §1.4 lines 36-39, marks it `covered`, notes the `modified` verdict, and routes GAP-05 to Phase 34 LOOP-01. |

## Current Spec Evidence

- `ctl_instruction.md:1770-1784` already carries the Mini-Batch Construction block: batch size $B=256$, replay set $B_{\leq k}=240$, look-ahead set $B_{k+1}=16$, per-trajectory cap `n_pts_cap=32`, the `min(n_pts_cap, n_snapshots(traj))` without-replacement rule, the 50/50 acceleration-weighted/uniform split, and the `dt_out`/`n_snapshots` metadata forward interface for the deferred M16 question.
- `pinn_architecture.md:323-352` carries Listing 2 `get_batch(batch_size, points_per_trajectory=32)` and the author comment that it is inconsistent with the CTL instruction plan; the PIPE-04 note at line 352 points to `ctl_instruction.md` Mini-Batch Construction as the operative rule.
- `ctl_instruction.md:1786-1798` and `ctl_instruction.md:1909-1913` carry the curriculum-aware gradient-clipping C-schedule (LOOP-04, consumed separately via the existing M14 packet).

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `34-SPEC.md:88` enforce SCOPE-12: 14D input `[τ, IC₁₃]`, Jacobi IC frame, mass-weighted COM projection head, `eps_soft = 1e-5`, post-v1.3 SCS gate, raw-mass `D ≈ 4.6416` (not `6.694`), and v1.5 DataLoader / validation-metric contracts.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` locks the raw-mass `D ≈ 4.6416` convention (v1.5 EVID-10).
- `ctl_instruction.md:1775` already exposes `dt_out(traj)` and `n_snapshots(traj)` metadata and preserves the M12 locked snapshot-count verdict.

This packet verifies that the B-07 contract does not disturb any SCOPE-12 locked convention.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may implement the stage-aware DataLoader / batch constructor after Phase 34 transcribes the spec contract. Live `pinn/` code (e.g., `pinn/data-processing-pipeline-full.py`) is NOT grounding evidence and may only be referenced as an implementation hand-off note.
- Not FUT-applicable: The packet itself records only the adjudicated spec contract.

## First-Principles or Engineering Check

1. **Curriculum preservation:** A replay set drawn from stages $\leq k$ prevents catastrophic forgetting of already-learned material; a small lookahead set from stage $k+1$ smooths the upcoming stage transition. This is a standard curriculum-learning engineering invariant.
2. **Locked query interfaces:** The data-side loader already exposes `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)` (PIPE-04/PIPE-08), so the `240/16` split is implemented through existing v1.5 contracts.
3. **Per-trajectory cap:** `min(n_pts_cap, n_snapshots(traj))` without replacement is the only count rule that respects the actual number of available high-fidelity snapshots without inventing data; the cap of 32 is carried as a provisional default, not a verified optimum.
4. **50/50 split retention:** The data-fidelity side keeps the existing uniform/acceleration-weighted mix (B-07 `modified`), which preserves the current weighted sampling behavior while the collocation-side 50/50 is handled separately under B-08.
5. **Source-silent edge cases:** Final-stage (`has_stage(k+1)`=false), undersized next-stage pool (<16), and replacement policy are flagged by §1.4 as needing determinism, but no source selects a policy. Routing them as owner-pending rather than inventing a default is the only STOP-safe action.

## Verdict

Verdict: `accept-resolution`

Explicit user instruction: None

Reasoning:

- The resolution doc §1.4 `modified` verdict is independently grounded by the current `ctl_instruction.md` Mini-Batch Construction block and the locked PIPE-04/PIPE-08 query interfaces.
- The `240/16` replay/lookahead split, `n_pts_cap=32`, `min(n_pts_cap, n_snapshots)`, and the data-fidelity 50/50 split are preserved as provisional defaults with a source citation, matching the B-07 `modified` disposition.
- Claim B07-04 rejects the inconsistent `pinn_architecture.md` §3.1 Listing-2 batch construction; this supports the Phase 34 canonical-home decision that `ctl_instruction.md` owns batch construction (SI-PINN-003 reconciliation, R9).
- Claim B07-05 / GAP-05 explicitly defer the edge-case policy, so this packet does not select a final-stage, undersized-pool, or replacement policy.

## Root-Cause Ambiguity

The root cause is a documentation/implementation split: the issue doc correctly flags that the training loop must use stage-aware replay/lookahead, but the `pinn_architecture.md` §3.1 code-oriented description uses a flat `get_batch()` that conflicts with the CTL curriculum plan. The resolution doc resolves the structural point but leaves the execution edge cases source-silent.

## Locked Convention or Owner Route

Locked/provisional for Phase 34 transcription:

```text
For a 256-trajectory batch at curriculum stage k:
  B_replay = 240 trajectories drawn from stages ≤ k
  B_lookahead = 16 trajectories drawn from stage k+1, gated by has_stage(k+1)
  n_pts(traj) = min(n_pts_cap, n_snapshots(traj)), without replacement
  n_pts_cap = 32 (provisional default, configurable)
  Data-fidelity 50/50 split retained: k_w = floor(n_pts/2) acceleration-weighted draws,
                                       then n_pts - k_w uniform draws from the remainder
All values tagged provisional (B-07 modified, §1.4).
```

Owner-pending / source-silent route:

- Final-stage behavior when `has_stage(k+1)`=false.
- Behavior when the next-stage lookahead pool has fewer than 16 eligible trajectories.
- Replacement / reservoir policy for the replay and lookahead sets.

These edge cases are routed to a future `../34-GAPS.md` STOP gap by Plan 34-03 (D-34-16a); they are NOT decided in this packet.

## Which Source Was Correct / Wrong

- Issue doc: correct that stage-aware replay/lookahead is required and that the existing `get_batch()` description is insufficient; not authoritative for the exact `240/16/cap=32` values or for the edge-case policy.
- Resolution doc: correct in modifying the issue-doc position to provisional defaults, preserving the locked query interfaces, and explicitly routing the edge cases as source-silent (GAP-05).
- `pinn_architecture.md` §3.1 Listing-2 batch construction: rejected as the normative contract by claim B07-04; `ctl_instruction.md` Mini-Batch Construction is the canonical home.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md:1770-1784` already contains the 240/16/cap=32/Gumbel-top-k mini-batch block, but it is not explicitly tagged with the B-07 `modified` provisional status and does not state the `has_stage(k+1)` guard or the source-silent edge-case routing.

**After:** Phase 34 Plan 34-02/34-03 will transcribe the B-07 contract with an explicit `> **Phase 34 contract: Replay/lookahead batching (LOOP-01; provisional; AC-LOOP-01; ...)**` callout, the `has_stage(k+1)` guard, and a forward-reference to the owner-pending edge-case gap. No value is locked as a verified optimum.

## Named Acceptance Check

AC-LOOP-01

Planned pass criterion: `ctl_instruction.md` contains the replay/lookahead contract with `B_replay=240`, `B_lookahead=16`, `n_pts_cap=32` tagged provisional, `min(n_pts_cap, n_snapshots)` without replacement, the `has_stage(k+1)` guard, and a forward-reference to the owner-pending edge-case gap; no framework spec is edited before this packet exists.

Owning phase: Phase 34, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap is opened by this packet. The structural contract is grounded by the current `ctl_instruction.md` Mini-Batch Construction block and the resolution doc §1.4 `modified` verdict. The source-silent batch edge cases (final-stage, undersized next-stage pool <16, replacement policy) are explicitly recorded here as owner-pending and are routed to a future `../34-GAPS.md` STOP gap by Plan 34-03 (D-34-16a). They are not decided in this packet.

## Status Transition Log

```text
2026-06-25 pending-commit PENDING -> IN_PROGRESS (Phase 34 Plan 34-01 Task 2 by claude-gsd-executor-34-01; packet authored, B-07 accept-resolution consumed)
```

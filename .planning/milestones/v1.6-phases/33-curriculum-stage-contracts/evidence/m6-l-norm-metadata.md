# Evidence Packet: M6 - L_norm Metadata and Stage 0-6 Inventory (CURR-04)

## Header

| Field | Value |
|---|---|
| ID | `M6` |
| Title | Raw `L_norm` metadata, degenerate-`L_max` guard, Stage 0-6 inventory, and no-global-clamp contract (CURR-04) |
| Severity | MAJOR |
| Current Status | IN_PROGRESS |
| Current Verdict | accept-resolution |
| Phase | Phase 33 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 36 |
| Acceptance Check ID | AC-CURR-04 |
| Phase 33 Decisions Covered | `D-33-10` (raw `L_norm` + nonfinite / near-degenerate `L_max` guard), `D-33-11` (no global clamp; clipped gate owner-pending), `D-33-12` (Stage 0-6 inventory, cumulative replay, Stage-6 catch-all, claimed/FUT trajectory counts) — see `33-CONTEXT.md` decisions section |
| Spec Sections Touched | `ctl_instruction.md` Step 3 item 2 (`L_max` / `L_norm`); `ctl_instruction.md` "Multi-Stage Data Stratification by Difficulty" (Stage 0-6 inventory); `ctl_instruction.md` Step 4 (`L_norm` metadata exclusion from `IC13`) |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:251` (`np.clip(L/(L_max+eps), 0, 1)` storage/gate value in the proposed `compute_L_norm`); `pinn_instruction/issues/03-curriculum-and-training-loop.md:103` (M6 row — original "clamp before IC mapping" rationale, now rejected) | Non-authoritative issue source | The issue doc's proposed `compute_L_norm` returns `np.clip(L/(L_max+eps), 0, 1)` as the stored value. The original M6 rationale ("clamp before IC mapping") treated `L_norm` as an `IC13` candidate requiring bounding; that rationale is rejected by the resolution doc because `L_norm` is metadata, not an `IC13` slot. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:44-47` (§1.6 M6 `L_norm` clamping — `modified`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:129-131` (claim rows `M6-01` rejected, `M6-02` `surface_to_user`, `M6-03` defer); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:196` (DGR-07 L_norm clamp disagreement register) | candidate verdict source, not authority | §1.6 rejects the original "clamp before IC mapping" rationale (`L_norm` is metadata, not an `IC13` slot); states that no global clamp is authorized by this adjudication; the current un-clipped baseline remains until the owner selects raw-only, raw-plus-derived-clipped, or global-clipped storage; nonfinite and near-degenerate `L_max` behavior requires an explicit guard. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:51` (§1.6 line range 44-47); `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:86` (finding -> §1.6 mapping) | Navigation / line-map aid | §1.6 anchored to lines 44-47 in committed `49fb7958`; section anchor stable across re-pagination. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1071-1097` defines the `L_max` characteristic-scale formula and the current `compute_L_norm(m, r_prime, v_prime, E, eps=1e-10)` pseudocode that returns `L / (L_max + eps)` with **no clamp** — the current baseline is already raw-unclipped.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:105-247` defines the Stage 0-6 inventory (Stage 0 hierarchical stable; Stage 1 energy/angular-momentum-relaxed; Stage 2 high-resolution hierarchical-gold refinement; Stage 3 moderately chaotic low-fidelity; Stage 4a/4b chaotic low-fidelity by `tau_L`; Stage 5 high-resolution chaotic quasi-random-gold refinement; Stage 6 near-collision / extreme catch-all HF+LF). Each subsequent stage's training set includes all data from previous stages (curriculum replay); Stage 6 is the catch-all.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:247-265` (and Step 5 at 1425-1508) defines the cumulative replay semantics and the `record_key` ownership contract for stage labels.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1419` confirms `L_norm` is metadata, not a network IC slot under the Phase 17 input contract.

No framework spec is edited by this packet (Plan 33-01 only authors evidence; Plan 33-02 will transcribe the metadata/guard contract).

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md` `CURR-04` is the requirement for this packet. The roadmap / `CURR-04` `np.clip(L_norm, 0, 1)` stage-gate phrasing is **superseded** by `GAP-33-03`.
- `.planning/REQUIREMENTS.md` SCOPE-12 locks the `IC13` Jacobi-state vector; `L_norm` is not in `IC13`.
- `GAP-33-03` (`33-GAPS.md:138-198`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22) is the owner-routed resolution that carries the grounded disposition for this packet: raw-only / defer-clip.

## FUT Hand-off Note

- FUT path / note: The clipped-gate-vs-raw decision is owner-pending the FUT admitted-set EDA evidence. The Stage 0-6 trajectory counts are claimed/FUT where v1.5 verification does not support them; the actual EDA run that confirms counts is FUT. References to live `pinn/data-processing-pipeline-full.py` `L_norm` handling are NOT grounding; they are FUT-01/FUT-04 hand-off context only.
- Not FUT-applicable: This packet does not derive its verdict from any live code reference.

## First-Principles or Engineering Check

`L_norm = L / L_max` is a dimensionless ratio of the trajectory's total angular momentum magnitude to the characteristic angular-momentum scale `L_max = M_tot * r_char * sqrt(2|E|/M_tot)`. Because `L_max` is a characteristic scale (not a proven global maximum — see the L_max/tau_L packet), `L_norm` can legitimately exceed 1 when (a) the configuration is high-eccentricity or hierarchical with `L` transiently above the characteristic circular-orbit scale, or (b) `L_max` is numerically small or degenerate (e.g. near-zero `|E|`, near-zero `r_char` for a near-collision configuration). Raw storage preserves diagnostic truth: the recorded value tells downstream stage-gating, replay analysis, and acceptance probes exactly how far above the characteristic scale the trajectory is. Clipping to `[0, 1]` produces a bounded value suitable for naive thresholding but hides the overshoot magnitude and can mask formula or data issues.

The mandatory guard handles the degenerate cases explicitly: if `L_max` is nonfinite or near-degenerate (e.g. `|E|` below a numerical floor), the recorded `L_norm` must carry a diagnostic flag rather than being silently clamped or stored as `inf` / `nan`. This is required because Stage 6 (`s_min < 0.5 OR |E| < 0.01`) is precisely the regime where `|E|` is small and `r_char` can be small, so a global clamp would erase exactly the diagnostic signal that distinguishes genuine near-collision trajectories from formula failure.

The engineering consequences of the three owner options (raw-only, raw-plus-derived-clipped, global-clipped) are not derivable from first principles without the admitted-set `L_norm` distribution. A global clamp discards overshoot information across the whole stage inventory; a raw-plus-derived-clipped contract keeps both signals but doubles the metadata schema; a raw-only contract is the minimal change from the current spec and preserves all diagnostic truth. Phase 33 locks raw-only (the grounded default) and routes the clipped-gate decision to the owner after admitted-set evidence.

## Verdict

Verdict: accept-resolution

Explicit user instruction: `GAP-33-03` (`33-GAPS.md:185-198`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22, owner AskUserQuestion ratification of raw-only / defer-clip).

Reasoning:

- The resolution doc §1.6 rejects the original "clamp before IC mapping" rationale (`L_norm` is metadata, not an `IC13` slot), states that no global clamp is authorized, preserves the current un-clipped baseline, and requires explicit nonfinite / near-degenerate `L_max` handling. This is the grounded position.
- The owner-routed `GAP-33-03` resolution carries the storage-contract decision forward: raw-only storage is locked; the clipped-gate question (raw-only vs raw-plus-derived-clipped vs global-clipped) is owner-pending admitted-set evidence.
- The current spec `compute_L_norm` pseudocode (lines 1087-1097) already returns `L / (L_max + eps)` with no clamp, so locking raw-only is the minimal change.
- The roadmap / `CURR-04` `np.clip(L_norm, 0, 1)` stage-gate phrasing is explicitly superseded and must not be transcribed as a locked gate.

## Root-Cause Ambiguity

The root ambiguity has two layers: (1) the original M6 rationale treated `L_norm` as an `IC13` candidate requiring bounding, but `L_norm` is metadata under the Phase 17 contract — the rationale is rejected; (2) the issue doc and reports disagree on whether the sole stored metadata value should be clipped, with no admitted-set `L_norm` distribution available to adjudicate. Phase 33 resolves layer 1 definitively (raw metadata, not `IC13`) and routes layer 2 to the owner after admitted-set evidence.

## Locked Convention or Owner Route

**Locked by this packet (transcribed in Plan 33-02; decisions D-33-10, D-33-11, D-33-12):**

- Per D-33-10: store raw, un-clipped `L_norm` as staging / diagnostic metadata; require explicit nonfinite and near-degenerate `L_max` handling (diagnostic flag, not silent clamp).
- Per D-33-11: no global `L_norm` clamp is authorized; the M6 `np.clip(L_norm, 0, 1)` stage-gate is NOT locked and remains owner-pending admitted-set evidence.
- Per D-33-12: define the Stage 0-6 inventory, per-stage criteria, cumulative replay behavior, and Stage-6 catch-all; mark unverified trajectory counts as claimed/FUT.

**Owner route (deferred, GAP-33-03):** The clipped-gate-vs-raw question (raw-only vs raw-plus-derived-clipped vs global-clipped) is owner-pending admitted-set evidence. Raw-only is the locked default; the other two options remain available should later evidence support a bounded gate.

## Which Source Was Correct / Wrong

- Resolution doc (§1.6): correct to reject the IC-mapping rationale, correct to require the degenerate-`L_max` guard, and correct to route the storage-policy disagreement to the owner, after independent grounding.
- Issue doc: wrong on the original "clamp before IC mapping" rationale (M6-01 rejected); the `np.clip(L/(L_max+eps), 0, 1)` storage value is one of three owner-pending options (M6-02 `surface_to_user`), not the locked contract.
- Current spec: correct and governing for the raw `compute_L_norm` baseline and the `L_norm` metadata declaration at line 1419.
- The roadmap / `CURR-04` `np.clip(L_norm, 0, 1)` gate phrasing is superseded by `GAP-33-03` and must not be transcribed as locked.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` Step 3 item 2 (lines 1071-1097) defines `L_max` and the raw `compute_L_norm` returning `L / (L_max + eps)` with no clamp. The Stage 0-6 inventory (lines 105-247) defines the multi-fidelity topology with cumulative replay and a Stage-6 catch-all. There is no explicit nonfinite / near-degenerate `L_max` guard; there is no explicit "no global clamp" statement; the clipped-gate question is not named.

**After (Plan 33-02, not Plan 33-01):** `ctl_instruction.md` Step 3 item 2 will state explicitly that (a) raw `L_norm` is staging/diagnostic metadata and is stored un-clipped, (b) nonfinite / near-degenerate `L_max` requires an explicit diagnostic-flag guard, (c) no global clamp is authorized, and (d) the `np.clip(L_norm, 0, 1)` stage-gate is owner-pending admitted-set evidence. The Stage 0-6 inventory will mark unverified trajectory counts as claimed/FUT.

Plan 33-01 makes no spec edit. This packet routes the evidence and AC-CURR-04 identity.

## Named Acceptance Check

AC-CURR-04

Planned pass criterion (Plan 33-04 / Phase 36): `ctl_instruction.md` Step 3 item 2 / Step 4 / Stage-inventory text states (a) raw un-clipped `L_norm` stored as staging/diagnostic metadata; (b) explicit nonfinite / near-degenerate `L_max` diagnostic-flag guard; (c) no global `L_norm` clamp authorized; (d) `np.clip(L_norm, 0, 1)` stage-gate owner-pending admitted-set evidence; (e) Stage 0-6 inventory with cumulative replay, Stage-6 catch-all, and unverified trajectory counts marked claimed/FUT.

Owning phase: Phase 33 (Plan 33-02 transcribes; Plan 33-04 verifies).

## STOP / Gap Handling

No STOP gap opened — disposition grounded in `GAP-33-03` `RESOLVED-WITH-INSTRUCTION` 2026-06-22 (owner-routed raw-only / defer-clip; AskUserQuestion ratification), matching resolution doc §1.6 (M6-01 rejected, M6-02 `surface_to_user`, M6-03 defer, DGR-07). The raw-`L_norm` storage contract, the degenerate-`L_max` guard, the no-global-clamp rule, and the Stage 0-6 inventory are all grounded; the clipped-gate-vs-raw selection is the explicitly owner-pending remainder and is not a source-silent semantic gap.

## Status Transition Log

```text
2026-06-23 0113f86 PENDING -> IN_PROGRESS (Phase 33 P01 Task 3 by claude-code-gsd-executor-33-01; packet authored, ledger link applied in this task)
```

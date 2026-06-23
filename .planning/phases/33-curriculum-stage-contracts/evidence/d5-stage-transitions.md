# Evidence Packet: D5 - Stage-Transition State Machine (CURR-03)

## Header

| Field | Value |
|---|---|
| ID | `D5` |
| Title | Dual-path stage-transition state machine (CURR-03) |
| Severity | MAJOR |
| Current Status | IN_PROGRESS |
| Current Verdict | accept-resolution |
| Phase | Phase 33 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 36 |
| Acceptance Check ID | AC-CURR-03 |
| Phase 33 Decisions Covered | `D-33-08` (ADVANCE/RECOVER/HALT-REVIEW state machine), `D-33-09` (numeric thresholds, epoch tables, stagnation windows, retry limits, percentile relaxations remain provisional pending FUT Stage-0 pilot calibration) — see `33-CONTEXT.md` decisions section |
| Spec Sections Touched | `ctl_instruction.md` "Stage Transition Criteria" (lines 1666-1706) |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:107` (D5 issue row: "theoretical now ... limited data"); `pinn_instruction/issues/03-curriculum-and-training-loop.md:333-362` (D5 fallback proposal: ADVANCE on strict four-criteria path OR fallback on MAX_EPOCHS / stagnation / NaN rollback, with stage-dependent `epsilon_phys` / `epsilon_energy` table and per-stage MAX_EPOCHS `{0:500, 1:600, 2:700, 3:800, 4:900, 5:1000, 6:1200}`); `pinn_instruction/issues/03-curriculum-and-training-loop.md:364` (Stage-0 pilot calibration directive) | Non-authoritative issue source | Proposes a dual-path advancement: strict four-criteria AND a fallback path that treats MAX_EPOCHS / stagnation / NaN as alternate advancement triggers (rather than separate RECOVER / HALT-REVIEW states). Locks stage-dependent `epsilon_phys` / `epsilon_energy` thresholds and the per-stage MAX_EPOCHS table as if they were calibrated. The proposal is `claimed-unverified` per `D5-05` (CLM-08/09). |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:64-67` (§1.11 D5 stage transitions — `modified`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:146-151` (claim rows `D5-01` accepted baseline, `D5-02` accepted author note, `D5-03` modified Path B vs strict, `D5-04` `surface_to_user`, `D5-05` defer claimed-unverified, `D5-06` accepted pinn_arch §3.4); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:201-202` (DGR-12 stage fallback semantics, DGR-13 validation stability) | candidate verdict source, not authority | §1.11 retains the four current success criteria as the baseline pending a Stage-0 pilot; adds an explicit operational state machine — ADVANCE only on an approved success gate, RECOVER for NaN/Inf rollback and bounded retry, HALT/REVIEW for max-epoch or stagnation unless the owner explicitly authorizes degraded advancement; the percentile-10 relaxation, per-stage thresholds, epoch table, stagnation window, and retry limits are NOT adopted (they remain `claimed-unverified`); the locked energy denominator contract is unchanged. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:56` (§1.11 line range 64-67); `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:91` (finding -> §1.11 mapping) | Navigation / line-map aid | §1.11 anchored to lines 64-67 in committed `49fb7958`; section anchor stable across re-pagination. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1666-1682` is the "Stage Transition Criteria" section with the author note that all transition criteria are theoretical pending Stage-0 training, and the strict-path rule "Advance to the next stage only when all four criteria are met on the validation set (hold-out 10-20% of cumulative data per stage)".
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1683-1706` defines the four criteria: (1) Training Loss Plateau with `beta=0.98, patience=200, epsilon_plateau=1e-5`; (2) Validation Loss Stability `L_val(i) <= min_{j<=i} L_val(j)`; (3) Physics Residual Threshold `epsilon_phys=1e-4`; (4) Energy Conservation Check with the locked `epsilon_H = 1e-4 * S_H` (PHYS-04/D-20 GAP-19-01) energy denominator floor.

No framework spec is edited by this packet (Plan 33-01 only authors evidence; Plan 33-03 will transcribe).

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md` `CURR-03` is the requirement for this packet.
- `.planning/REQUIREMENTS.md` SCOPE-14 makes Stage-0 pilot calibration FUT; Phase 33 transcribes the state-machine contract only, not the calibrated thresholds.
- `33-SPEC.md` R3 (lines 67-79) locks the ADVANCE/RECOVER/HALT-REVIEW semantics as the Phase 33 contract.
- `33-CONTEXT.md` `D-33-08` and `D-33-09` carry the implementation decisions for this packet.

## FUT Hand-off Note

- FUT path / note: Stage-0 pilot calibration owns the eventual numeric thresholds, epoch tables, stagnation windows, retry limits, and percentile relaxation values (SCOPE-14; CLM-08/09). Any references to live `pinn/basic_architecture.py` training loops are NOT grounding; they are FUT-01/FUT-04 hand-off context only.
- Not FUT-applicable: This packet does not derive its verdict from any live code reference.

## First-Principles or Engineering Check

The D5 finding has no dedicated `RESOLVED-WITH-INSTRUCTION` `GAP-33-0X` of its own (review finding 4). Per the Plan 33-01 Task 3 action, this packet therefore MUST cite the concrete grounding for its ADVANCE/RECOVER/HALT-REVIEW semantics explicitly, in a `Grounding:` line, rather than treating `No STOP gap opened` as an unconditional pass.

**Grounding:** The ADVANCE / RECOVER / HALT-REVIEW state-machine semantics are grounded in resolution doc §1.11 (lines 64-67: "Add an explicit operational state machine: ADVANCE only on an approved success gate; RECOVER for NaN/Inf rollback and bounded retry; HALT/REVIEW for max-epoch or stagnation unless the owner explicitly authorizes degraded advancement"), `33-SPEC.md` R3 (lines 67-79, which locks these three dispositions as the Phase 33 contract), and `33-CONTEXT.md` `D-33-08` (which carries the owner-ratified decision that transitions are modelled as this state machine). All three required AGENTS.md step-2 understanding checks pass: (1) the engineering principle at stake is that finite-data Adam optimization cannot guarantee monotonic validation loss, so a strict-and-only advancement rule would block curriculum progression indefinitely — a state machine that separates "approved success" (ADVANCE), "transient numerical failure" (RECOVER), and "blocked pending owner review" (HALT/REVIEW) preserves the integrity of the success criterion while making the curriculum executable; (2) each candidate resolution has different downstream consequences — treating MAX_EPOCHS / stagnation as alternate advancement (issue-doc fallback) silently relaxes the success criterion, while separating them into HALT/REVIEW forces explicit owner authorization before any degraded advancement; (3) the consulted sources are the issue-doc D5 fallback (lines 333-362), the resolution doc §1.11 (lines 64-67), the current spec "Stage Transition Criteria" (lines 1666-1706), and `33-SPEC.md` R3 — none of which authorizes silent fallback advancement, and §1.11 / R3 / D-33-08 explicitly require the three-state separation.

The locked energy denominator floor (`epsilon_H = 1e-4 * S_H`, PHYS-04/D-20 GAP-19-01) is preserved unchanged in the Energy Conservation Check.

## Verdict

Verdict: accept-resolution

Explicit user instruction: `33-SPEC.md` R3 and `33-CONTEXT.md` `D-33-08` / `D-33-09` (Phase 33 planning decisions, grounded by the resolution doc §1.11 disposition and ratified through the v1.6 spec-phase / discuss-phase workflow that produced `33-SPEC.md` and `33-CONTEXT.md`).

Reasoning:

- The resolution doc §1.11 retains the four current success criteria as the baseline and adds the explicit ADVANCE / RECOVER / HALT-REVIEW state machine. This is the grounded position.
- `33-SPEC.md` R3 locks the three-state semantics as the Phase 33 contract; `33-CONTEXT.md` `D-33-08` carries the decision.
- The issue-doc D5 fallback conflates MAX_EPOCHS / stagnation / NaN with advancement; the resolution doc and R3 separate them into HALT/REVIEW (max-epoch, stagnation) and RECOVER (NaN/Inf), with degraded advancement requiring explicit owner authorization.
- The percentile-10 relaxation (`percentile_10(val_history)` at issue line 344), the per-stage `epsilon_phys` / `epsilon_energy` table (issue lines 353-361), the per-stage MAX_EPOCHS table (issue line 349), the stagnation window (issue line 350), and the retry protocol (issue line 351) are all `claimed-unverified` (D5-05; CLM-08/09) and remain provisional pending the FUT Stage-0 pilot (`D-33-09`).

## Root-Cause Ambiguity

The root ambiguity is the meaning of "fallback" in stage transitions. The issue doc treats MAX_EPOCHS / stagnation / NaN as fallback advancement triggers (PATH B `any trigger`), which silently relaxes the success criterion. The resolution doc and Phase 33 R3 treat them as separate state-machine dispositions: ADVANCE requires the approved success gate, RECOVER handles transient numerical failure with bounded retry, and HALT/REVIEW blocks progression until the owner explicitly authorizes degraded advancement. The numeric thresholds required to make either interpretation operational are claimed-unverified and require Stage-0 pilot calibration.

## Locked Convention or Owner Route

**Locked by this packet (transcribed in Plan 33-03; decisions D-33-08, D-33-09):** Per D-33-08, the stage-transition contract is an operational state machine with three dispositions:

- **ADVANCE:** allowed only when the approved success gate passes (training plateau, validation stability, stage-dependent physics-residual, and energy-drift criteria).
- **RECOVER:** used for NaN/Inf rollback and bounded retry.
- **HALT/REVIEW:** used for max-epoch or stagnation unless the owner explicitly authorizes degraded advancement.

Per D-33-09, all numeric thresholds, epoch tables, stagnation windows, retry limits, and percentile relaxations remain provisional pending FUT Stage-0 pilot calibration (SCOPE-14). The locked energy denominator floor (`epsilon_H = 1e-4 * S_H`) is preserved unchanged.

**No owner route is opened by this packet.** The state-machine semantics are grounded; only the eventual calibrated numeric values are FUT (owned by Stage-0 pilot calibration under SCOPE-14, not by a STOP gap).

## Which Source Was Correct / Wrong

- Resolution doc (§1.11): correct on the three-state semantics, correct to retain the four success criteria as baseline, and correct to mark the percentile-10 relaxation and numeric tables as claimed-unverified, after independent grounding.
- Issue doc (D5 fallback): partly correct that the strict monotonic-validation criterion is unrealistic with finite data; wrong to encode MAX_EPOCHS / stagnation / NaN as silent advancement triggers; wrong to lock stage-dependent `epsilon_phys` / `epsilon_energy` and the per-stage MAX_EPOCHS table as if calibrated.
- Current spec: correct and governing for the four success criteria and the locked energy denominator floor.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` "Stage Transition Criteria" (lines 1666-1706) defines the strict four-criteria advancement rule with the author note that all criteria are theoretical pending Stage-0 training. It does not separate RECOVER (NaN/Inf) or HALT/REVIEW (max-epoch, stagnation) as named dispositions.

**After (Plan 33-03, not Plan 33-01):** `ctl_instruction.md` "Stage Transition Criteria" will add the ADVANCE / RECOVER / HALT-REVIEW state machine, state explicitly that degraded advancement requires owner authorization, preserve the four success criteria and the locked energy denominator floor, and mark all numeric thresholds, epoch tables, stagnation windows, retry limits, and percentile relaxations as provisional pending FUT Stage-0 pilot calibration.

Plan 33-01 makes no spec edit. This packet routes the evidence and AC-CURR-03 identity.

## Named Acceptance Check

AC-CURR-03

Planned pass criterion (Plan 33-04 / Phase 36): `ctl_instruction.md` "Stage Transition Criteria" states (a) ADVANCE only on the approved success gate; (b) RECOVER for NaN/Inf rollback and bounded retry; (c) HALT/REVIEW for max-epoch or stagnation with explicit owner authorization required for degraded advancement; (d) the four success criteria and the locked energy denominator floor preserved; (e) all numeric thresholds, epoch tables, stagnation windows, retry limits, and percentile relaxations marked provisional pending FUT Stage-0 pilot calibration.

Owning phase: Phase 33 (Plan 33-03 transcribes; Plan 33-04 verifies).

## STOP / Gap Handling

No STOP gap opened — semantics grounded in resolution doc §1.11 / `33-SPEC.md` R3 / `33-CONTEXT.md` D-33-08 (owner-ratified three-state ADVANCE/RECOVER/HALT-REVIEW contract; v1.6 spec-phase + discuss-phase workflow). The numeric-threshold calibration is explicitly FUT under SCOPE-14 (`D-33-09`) and is not a source-silent semantic gap; it is a documented FUT deferral owned by Stage-0 pilot calibration. Per Plan 33-01 Task 3 review-finding-4 rule, the `No STOP gap opened` field is qualified by the concrete grounding citation above rather than asserted as an unconditional pass.

## Status Transition Log

```text
2026-06-23 0113f86 PENDING -> IN_PROGRESS (Phase 33 P01 Task 3 by claude-code-gsd-executor-33-01; packet authored, ledger link applied in this task)
```

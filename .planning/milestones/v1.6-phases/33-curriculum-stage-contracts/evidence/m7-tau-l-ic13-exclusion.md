# Evidence Packet: M7 - tau_L Exclusion from IC13 (CURR-02)

## Header

| Field | Value |
|---|---|
| ID | `M7` |
| Title | `tau_L` exclusion from `IC13` (CURR-02) |
| Phase 33 Decisions Covered | `D-33-06` (`tau_L` excluded from `IC13`; staging/evaluation metadata) — see `33-CONTEXT.md` decisions section |
| Severity | MAJOR |
| Current Status | IN_PROGRESS |
| Current Verdict | accept-resolution |
| Phase | Phase 33 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 36 |
| Acceptance Check ID | AC-CURR-02-M7 |
| Spec Sections Touched | `ctl_instruction.md` Step 3 item 5 outputs (`tau_L` staging/evaluation metadata); `ctl_instruction.md` Step 4 (`IC13` assembly) |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:103` (M7 row: "Exclude `tau_L` from IC vector by design (it's a derived dynamical property, not an IC invariant). Use only for stage gating and model evaluation.") | Non-authoritative issue source | Issue-doc M7 row records that `tau_L` is computed in CTL Step 3 but dropped from the IC vector assembly in Step 4, with the rationale that `tau_L` is a derived dynamical property rather than an IC invariant. The issue doc endorses the exclusion (this is one of the few issue-doc claims the resolution doc accepts). |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:48-51` (§1.7 M7 `tau_L` exclusion from `IC13` — `accepted`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:132-133` (claim rows `M7-01` and `M7-02` both `accepted`) | candidate verdict source, not authority | §1.7 accepts M7: "`tau_L` is deliberately excluded from the locked Jacobi-state input and retained only as staging/evaluation metadata." |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:52` (§1.7 line range 48-51); `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:87` (finding -> §1.7 mapping) | Navigation / line-map aid | §1.7 anchored to lines 48-51 in committed `49fb7958`; section anchor stable across re-pagination. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1030-1037` defines the Step 3 outputs (`E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L`) and states that stage gating uses `(E, Q, s_min, L_norm, tau_L)` while the input vector is `IC13 = (m1, m2, m3, rho_x, lambda_x, lambda_y, rhodot_x, rhodot_y, rhodot_z, lambdadot_x, lambdadot_y, lambdadot_z, E)` (the Jacobi-state vector). `tau_L` and `L_norm` are staging/diagnostics values, not IC slots.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1155-1192` defines the Step 3 item 5 `tau_L` Rosenstein-style estimator, with `tau_L` produced as a staging/evaluation value.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1289-1424` defines Step 4 "Formulating the Input Vector" and the locked `IC13` assembly. `tau_L` does not appear in `IC13`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1419` confirms `tau_L`, `L_norm`, and other invariant-heavy descriptors remain available as curriculum/diagnostics/loss-scaling/reporting metadata and are **not** final network IC slots under the Phase 17 input contract.

No framework spec is edited by this packet (Plan 33-01 only authors evidence; Plan 33-02 will transcribe).

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md` SCOPE-12 makes the locked v1.4 `IC13 = [m1, m2, m3, rho_x, lambda_x, lambda_y, rhodot_x, rhodot_y, rhodot_z, lambdadot_x, lambdadot_y, lambdadot_z, E]` Jacobi-state vector a hard constraint. `tau_L` is not in this vector by design.
- `.planning/REQUIREMENTS.md` `CURR-02` is the requirement that covers this packet (the M7 `tau_L`-exclusion sub-finding of CURR-02).
- `GAP-33-02` (`33-GAPS.md:117-134`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22) records M7 as accepted (§1.7) and carries the broader `tau_L` deferral for the L_max/tau_L companion packet.

## FUT Hand-off Note

- FUT path / note: Any implementation that exposes `tau_L` to training-time code paths must read `tau_L` from the staging/evaluation metadata store, never from an `IC13` slot. References to live `pinn/data-processing-pipeline-full.py` `tau_L` handling are NOT grounding; they are FUT-01/FUT-04 hand-off context only.
- Not FUT-applicable: This packet does not derive its verdict from any live code reference.

## First-Principles or Engineering Check

`tau_L = 1 / lambda_max` is a property of the trajectory's dynamical evolution (the inverse of the largest Lyapunov exponent of the orbit). It is not a function of the initial condition alone in the same sense that the Jacobi coordinates `rho`, `lambda`, `rhodot`, `lambdadot`, and `E` are: it must be estimated from the trajectory's time series (Step 3 item 5). Including `tau_L` in `IC13` would create a circular dependency — the network input would depend on a quantity derived from the orbit that the network is being trained to predict — and would also violate the Phase 17 contract that `IC13` is the Jacobi state of the initial condition only.

The engineering consequence is unambiguous: `tau_L` must remain a staging/evaluation-side metadata value, used for stage assignment (Stage 4a `tau_L > 5`, Stage 4b `2 < tau_L <= 5`) and for model evaluation (predictability-horizon analysis at `ctl_instruction.md:1779-1788`), never as a network input.

## Verdict

Verdict: accept-resolution

Explicit user instruction: None; the verdict is grounded by the current spec, SCOPE-12, and the resolution doc §1.7. `GAP-33-02` carries the broader `tau_L` deferral for the companion L_max/tau_L packet; the M7 sub-finding itself is `accepted` (not `surface_to_user`).

Reasoning:

- The resolution doc §1.7 accepts M7: `tau_L` is deliberately excluded from the locked Jacobi-state input and retained only as staging/evaluation metadata.
- The current spec already implements this exclusion: `IC13` (Step 4) does not contain `tau_L`; Step 3 item 5 produces `tau_L` as a staging value; line 1419 explicitly states invariant-heavy descriptors (including `tau_L`) are metadata, not network IC slots.
- SCOPE-12 locks the `IC13` Jacobi-state vector.
- The first-principles check confirms `tau_L` is a trajectory-derived property and cannot be an IC invariant without circularity.

## Root-Cause Ambiguity

There is no genuine semantic ambiguity for M7. The only ambiguity is documentation clarity: the current spec records the exclusion in scattered places (Step 3 outputs at 1030-1037, Step 4 IC13 assembly at 1289-1424, the metadata declaration at 1419, the stage-gate uses at 1155-1192) but does not state in one canonical sentence that "`tau_L` is staging/evaluation metadata and is excluded from `IC13` by design". Plan 33-02 will add that canonical sentence.

## Locked Convention or Owner Route

**Locked by this packet (transcribed in Plan 33-02; decision D-33-06):** Per D-33-06, `tau_L` is staging/evaluation metadata and is excluded from `IC13` by design. It is used for stage assignment and model evaluation (predictability-horizon analysis), never as a network input. This is grounded by the current spec, SCOPE-12, and the resolution doc §1.7 (M7 `accepted`).

**No owner route** for this sub-finding: M7 is `accepted`, not `surface_to_user`. The broader `tau_L` estimator / units / threshold deferral is owned by the companion `L_max / tau_L` packet (AC-CURR-02-LMAX) and `GAP-33-02`.

## Which Source Was Correct / Wrong

- Resolution doc (§1.7): correct on the `tau_L` exclusion, matching current spec, SCOPE-12, and first principles.
- Issue doc (M7 row): correct on the exclusion rationale (derived dynamical property, not an IC invariant).
- Current spec: correct and governing for the existing `IC13` assembly and the metadata declaration at line 1419.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` records the `tau_L` exclusion across Step 3 outputs (1030-1037), Step 4 `IC13` assembly (1289-1424), and the metadata declaration (1419), but no single canonical sentence states the exclusion by design.

**After (Plan 33-02, not Plan 33-01):** `ctl_instruction.md` Step 3 / Step 4 will carry one canonical sentence stating "`tau_L` is staging/evaluation metadata and is excluded from `IC13` by design" so the exclusion is explicit, not implicit-from-absence.

Plan 33-01 makes no spec edit. This packet routes the evidence and AC-CURR-02-M7 identity.

## Named Acceptance Check

AC-CURR-02-M7

Planned pass criterion (Plan 33-04 / Phase 36): `ctl_instruction.md` Step 3 / Step 4 text states (a) `tau_L` is staging/evaluation metadata, (b) `tau_L` is excluded from `IC13` by design, (c) `tau_L` is used for stage assignment (Stage 4a/4b) and model evaluation (predictability horizon), and (d) no `IC13` slot holds `tau_L`.

Owning phase: Phase 33 (Plan 33-02 transcribes; Plan 33-04 verifies).

## STOP / Gap Handling

No STOP gap opened — disposition grounded in resolution doc §1.7 (M7 `accepted`; M7-01 and M7-02 both `accepted`), the current spec (`IC13` assembly at 1289-1424, metadata declaration at 1419, Step 3 item 5 `tau_L` estimator at 1155-1192), and SCOPE-12. The `tau_L`-exclusion sub-finding is fully grounded; the broader `tau_L` estimator/units/threshold deferral is owned by the companion `L_max / tau_L` packet and `GAP-33-02`.

## Status Transition Log

```text
2026-06-23 0113f86 PENDING -> IN_PROGRESS (Phase 33 P01 Task 2 by claude-code-gsd-executor-33-01; packet authored, ledger link applied in Task 3)
```

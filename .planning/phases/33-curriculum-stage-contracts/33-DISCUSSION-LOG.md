# Phase 33: Curriculum-Stage Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-22
**Phase:** 33-curriculum-stage-contracts
**Mode:** `--auto`
**Areas discussed:** adaptive population safeguard, `tau_L` estimator,
`L_norm` storage, stage transitions, `s_min` frame, UI gate false positive

---

## Adaptive Population Safeguard

| Option | Description | Selected |
|--------|-------------|----------|
| Lock `>10%` now | Treat roadmap / requirements wording as final. | |
| Packet-first / defer floor | Specify EDA + stable labels; leave population floor owner-pending after admitted-set EDA. | yes |
| Select different policy now | Pick 5%, adaptive, or another rule. | |

**User's choice:** `[auto]` Selected packet-first / defer floor from
`GAP-33-01` resolution.
**Notes:** The selected default preserves the owner-ratified resolution note and
prevents the plan from converting a source-surfaced policy choice into a locked
contract.

---

## `tau_L` Estimator and Units

| Option | Description | Selected |
|--------|-------------|----------|
| Lock shadow method | Adopt shadow/Benettin-style method and PCA+Rosenstein shortcut. | |
| Retain Rosenstein baseline / defer estimator | Keep current baseline as revisable; leave method, units, fit parameters, and thresholds owner-pending. | yes |
| Select exact estimator now | Choose final estimator, units, perturbation, softening, uncertainty, and calibration. | |

**User's choice:** `[auto]` Selected retain Rosenstein baseline / defer
estimator from `GAP-33-02` resolution.
**Notes:** Also carries forward `L_max` as characteristic scale and `tau_L`
excluded from `IC13`.

---

## `L_norm` Storage and Clamp Policy

| Option | Description | Selected |
|--------|-------------|----------|
| Raw-only / defer clipped gate | Store raw `L_norm`; require `L_max` guard; leave clipped gate owner-pending. | yes |
| Raw plus derived clipped gate | Store raw and derived bounded value now. | |
| Global clipped storage | Clamp the sole stored metadata value globally. | |

**User's choice:** `[auto]` Selected raw-only / defer clipped gate from
`GAP-33-03` resolution.
**Notes:** No global clamp is authorized; `np.clip(L_norm, 0, 1)` is not locked
as a Phase 33 stage gate.

---

## Stage Transitions

| Option | Description | Selected |
|--------|-------------|----------|
| State machine with provisional thresholds | ADVANCE only on success gate, RECOVER for rollback/retry, HALT/REVIEW for max-epoch or stagnation. | yes |
| Treat fallback triggers as advancement | Allow max-epoch / stagnation to advance stages automatically. | |
| Lock exact thresholds now | Set final epoch, threshold, stagnation, and retry values in Phase 33. | |

**User's choice:** `[auto]` Selected state machine with provisional thresholds.
**Notes:** Matches candidate resolution doc section 1.11 and roadmap `CURR-03`.

---

## `s_min` Stage-Gate Frame

| Option | Description | Selected |
|--------|-------------|----------|
| Unsoftened geometric stage gate | Use geometric `s_min` for Stage-6 collision gate; leave loss-side softening to Phase 35. | yes |
| Softened stage gate | Use `max(s_min, epsilon)` for the curriculum gate. | |
| Reopen D-05 | Surface a new owner decision before planning. | |

**User's choice:** `[auto]` Selected unsoftened geometric stage gate based on
Phase 32's owner-ratified D-05 row.
**Notes:** Loss-side matched-Plummer softening remains Phase 35.

---

## UI Gate False Positive

| Option | Description | Selected |
|--------|-------------|----------|
| Use `--skip-ui` | Treat Phase 33 as non-frontend because roadmap says `UI hint: no`. | yes |
| Generate UI-SPEC | Produce an unrelated UI contract before planning. | |
| Stop for user decision | Ask before planning. | |

**User's choice:** `[auto]` Selected `--skip-ui`.
**Notes:** The deterministic UI gate reported `frontend: true`, but the phase is
specwork-only and has no UI deliverable.

---

## the agent's Discretion

- Planner may choose plan count and task grouping.
- Planner may choose deterministic verification command structure, provided the
  checks prove every `CURR-01` through `CURR-05` contract and all prohibitions.

## Deferred Ideas

- Admitted-set EDA and population-floor owner policy.
- Final `tau_L` estimator / time-unit / threshold calibration.
- Clipped `L_norm` stage-gate policy.
- Stage-0 pilot threshold calibration.
- Phase 34 training-loop contracts and Phase 35 loss contracts.

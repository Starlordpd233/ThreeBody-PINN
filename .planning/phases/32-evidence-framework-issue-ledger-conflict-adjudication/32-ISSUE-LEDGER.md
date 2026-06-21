# Phase 32 Issue Ledger

Stable issue-03 ledger for Phase 32 through Phase 36. The ledger is seeded from `31-RESOLUTION-MAP.md` and `32-RESEARCH.md`; it records process state only and does not assign semantic verdicts before evidence packets exist.

`FIX_APPLIED is not terminal`. Closure requires `VERIFIED` after the named acceptance check passes, or `DEFERRED` with a written blocker and `defer-with-blocker` verdict.

## Ledger

| Finding ID | Title | Owner Phase | Status | Verdict | Evidence Packet | Acceptance Check | Spec Targets | Dependents | Transition Log |
|---|---|---|---|---|---|---|---|---|---|
| D-04 | Causal-training mode owner decision | Phase 32 | PENDING | - | `evidence/d-04-causal-training-mode.md` | AC-EVID-15-D04 | No Option A/B/C selection in Plan 32-01; Phase 35 LOSS-04 and Phase 34 LOOP-01 consume only after explicit instruction or grounded verdict | Phase 35 LOSS-04; Phase 34 LOOP-01; Phase 36 | Seeded; unresolved owner decision routes to Phase 32 EVID-15 |
| D-05 | s_min frame owner decision | Phase 32 | PENDING | - | `evidence/d-05-s-min-frame.md` | AC-EVID-15-D05 | No gate-frame selection in Plan 32-01; Phase 33 CURR-05 consumes only after explicit instruction or grounded verdict | Phase 33 CURR-05; Phase 35 loss-side references; Phase 36 | Seeded; unresolved owner decision routes to Phase 32 EVID-15 |
| D-06 | Epsilon strategy owner decision | Phase 32 | PENDING | - | `evidence/d-06-epsilon-strategy.md` | AC-EVID-15-D06 | No static epsilon selection in Plan 32-01; Phase 33 and Phase 35 consume only after explicit instruction or grounded verdict | Phase 33 static invariants; Phase 35 loss consistency; Phase 36 | Seeded; unresolved owner decision routes to Phase 32 EVID-15 |
| B-07 | Replay/lookahead batching | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-01 | `ctl_instruction.md` training-loop batch construction | Phase 34 LOOP-01; Phase 36 | Seeded; packet-before-edit forward reference |
| B-08 | Data versus collocation points | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-02 | `ctl_instruction.md` data/collocation point-set contract | Phase 34 LOOP-02/03; Phase 36 | Seeded; packet-before-edit forward reference |
| M6 | L_norm clamping | Phase 33 | PENDING | - | Owner must author packet before spec edits | AC-CURR-04-M6 | `ctl_instruction.md` stage inventory and L_norm metadata policy | Phase 33 CURR-04; Phase 36 | Seeded; packet-before-edit forward reference |
| M7 | tau_L exclusion from IC13 | Phase 33 | PENDING | - | Owner must author packet before spec edits | AC-CURR-02-M7 | `ctl_instruction.md` tau_L metadata exclusion | Phase 33 CURR-02; Phase 36 | Seeded; packet-before-edit forward reference |
| M14 | Gradient clipping divergence | Phase 32 | PENDING | - | `evidence/m14-gradient-clipping.md` | AC-EVID-15-M14 | Phase 32 packet locks or defers structure; Phase 34 LOOP-04 performs spec transcription | Phase 34 LOOP-04; Phase 36 | Seeded; headline packet owned by Phase 32 |
| M15 | Energy-loss weights | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-02 | `ctl_instruction.md` energy-loss weight schedule | Phase 35 LOSS-02; Phase 36 | Seeded; packet-before-edit forward reference |
| M16 | dt_out-aware collocation scaling | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-06 | `ctl_instruction.md` dt_out collocation scaling contract | Phase 34 LOOP-06; Phase 36 | Seeded; packet-before-edit forward reference |
| D5 | Stage transitions | Phase 33 | PENDING | - | Owner must author packet before spec edits | AC-CURR-03 | `ctl_instruction.md` dual-path transition criteria | Phase 33 CURR-03; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-12 | Componentwise automatic differentiation | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01-AD | `ctl_instruction.md` loss scaling and AD cross-link | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-13 | Energy Huber delta | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-03 | `ctl_instruction.md` Huber delta calibration contract | Phase 35 LOSS-03; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-18 | Loss scaling and units | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01 | `ctl_instruction.md` dimensionless loss scaling | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
| adaptive stage assignment | Data-driven adaptive stage assignment | Phase 33 | PENDING | - | Owner must author packet before spec edits | AC-CURR-01 | `ctl_instruction.md` adaptive stage methodology | Phase 33 CURR-01; Phase 36 | Seeded; packet-before-edit forward reference |
| D = 6.694 | Raw-mass D conflict | Phase 32 | PENDING | - | `evidence/d-6-694-conflict.md` | AC-EVID-15-D | Phase 32 convention-locking packet; Phase 33 consumes D in tau_L and L_max; Phase 36 checks unresolved provenance and deferred-list handling | Phase 33 CURR-02; Phase 36 provenance/deferred-list checker | Seeded; SCOPE-12 hard constraint remains until packet adjudication |
| L_max / tau_L | L_max and tau_L formulas | Phase 33 | PENDING | - | Owner must author packet before spec edits | AC-CURR-02 | `ctl_instruction.md` L_max and tau_L formula contract | Phase 33 CURR-02; Phase 36 | Seeded; packet-before-edit forward reference |
| ALM mu_p clamp | ALM mu_p clamp | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-05 | `ctl_instruction.md` or `pinn_architecture.md` ALM update and optional clamp contract | Phase 34 LOOP-05; Phase 36 | Seeded; packet-before-edit forward reference |

## Non-Headline Packet Mandate

Every non-headline row above has exactly one primary owner phase from Phase 33, Phase 34, or Phase 35. That owner must author the evidence packet and update this ledger before editing any spec section for the row. Phase 36 must reject any spec edit whose row lacks packet/verdict linkage.

## Transition Logs

### D-04

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting Option A/B/C.

### D-05

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting a gate frame.

### D-06

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting a static epsilon strategy.

### B-07

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### B-08

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### M6

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.

### M7

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.

### M14

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; headline packet is owned by Phase 32 before Phase 34 transcription.

### M15

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### M16

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### D5

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.

### NS-12

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-13

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-18

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### adaptive stage assignment

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.

### D = 6.694

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 32 packet owns convention lock, Phase 33 consumes tau_L/L_max, and Phase 36 checks unresolved provenance/deferred-list handling.

### L_max / tau_L

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.

### ALM mu_p clamp

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

# Phase 32 Issue Ledger

Stable issue-03 ledger for Phase 32 through Phase 36. The ledger is seeded from `31-RESOLUTION-MAP.md` and `32-RESEARCH.md`; it records process state only and does not assign semantic verdicts before evidence packets exist.

`FIX_APPLIED is not terminal`. Closure requires `VERIFIED` after the named acceptance check passes, or `DEFERRED` with a written blocker and `defer-with-blocker` verdict.

## Column Definitions

- `Owner Phase` names the phase that authored the current row verdict or deferral. For Phase 32 headline rows, `Owner Phase = Phase 32` means Phase 32 owns the evidence packet and current `accept-resolution` / `defer-with-blocker` state; the `Dependents` column and blocker text name the downstream phase that must consume or resolve the row before spec transcription.

## Ledger

| Finding ID | Title | Owner Phase | Status | Verdict | Evidence Packet | Acceptance Check | Spec Targets | Dependents | Transition Log |
|---|---|---|---|---|---|---|---|---|---|
| D-04 | Causal-training mode owner decision | Phase 32 | DEFERRED | defer-with-blocker | `evidence/d-04-causal-training-mode.md` | AC-EVID-15-D04 | No Option A/B/C selected in Phase 32; Phase 35 LOSS-04 and Phase 34 LOOP-01 consume only after explicit owner instruction or later grounded verdict | Phase 35 LOSS-04; Phase 34 LOOP-01 if batch-windowing changes; Phase 36 | 2026-06-21 pending-commit PENDING -> DEFERRED by Phase 32 Plan 32-03 Task 1; packet preserves owner decision and blocks downstream final causal-mode transcription |
| D-05 | s_min frame owner decision | Phase 32 | PENDING | accept-resolution | `evidence/d-05-s-min-frame.md` | AC-EVID-15-D05 | Owner ratified Option A 2026-06-21: unsoftened geometric `s_min` stage gate + matched-Plummer (`epsilon_train = 1e-5`) softening in training residual/energy only; issue-doc `max(s_min, epsilon)` phrasing rejected per PHYS-03; Phase 33 CURR-05 transcribes the geometric gate and Phase 35 cites the matched-Plummer loss-side distinction | Phase 33 CURR-05; Phase 35 loss-side references; Phase 36 | 2026-06-21 DEFERRED -> PENDING + accept-resolution by owner AskUserQuestion instruction; gap RESOLVED-WITH-INSTRUCTION in 32-GAPS.md; downstream transcription remains Phase 33/35-owned |
| D-06 | Epsilon strategy owner decision | Phase 32 | PENDING | accept-resolution | `evidence/d-06-epsilon-strategy.md` | AC-EVID-15-D06 | Owner ratified dual-context 2026-06-21 (Option A = issue-doc Option B): offline invariants/validation keep `epsilon_inv = 1e-10` (consistent with v1.5-locked IPR GAP-28-02), training keeps locked `epsilon_train = 1e-5`, matched-Plummer; Option C rejected. FUT/trainex item: confirm close-encounter train-vs-validate mismatch negligible on admitted set. Phase 33 transcribes static invariants; Phase 35 loss consistency | Phase 33 static invariants; Phase 35 loss consistency; Phase 36 | 2026-06-21 DEFERRED -> PENDING + accept-resolution by owner AskUserQuestion instruction; gap RESOLVED-WITH-INSTRUCTION in 32-GAPS.md; downstream transcription remains Phase 33/35-owned |
| B-07 | Replay/lookahead batching | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-01 | `ctl_instruction.md` training-loop batch construction | Phase 34 LOOP-01; Phase 36 | Seeded; packet-before-edit forward reference |
| B-08 | Data versus collocation points | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-02 | `ctl_instruction.md` data/collocation point-set contract | Phase 34 LOOP-02/03; Phase 36 | Seeded; packet-before-edit forward reference |
| M6 | L_norm clamping | Phase 33 | VERIFIED | accept-resolution | `../33-curriculum-stage-contracts/evidence/m6-l-norm-metadata.md` | AC-CURR-04 | `ctl_instruction.md` stage inventory and L_norm metadata policy | Phase 33 CURR-04; Phase 36 | 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; 2026-06-23 699b849/f2c8a9b PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 3 (packet authored, raw `L_norm` metadata + degenerate-`L_max` guard locked, no global clamp authorized, clipped gate owner-pending per GAP-33-03); the seeded CURR-04 AC ID (carrying a redundant M6 suffix) was renamed to AC-CURR-04 per Plan 33-01 convention (M6 is the only CURR-04 row); 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2 (33-VERIFICATION.md records AC-CURR-04 PASS: raw un-clipped L_norm storage, mandatory nonfinite/near-degenerate L_max diagnostic guard, no global clamp authorized, clipped-gate owner-pending admitted-set evidence per GAP-33-03; spec transcription verified in ctl_instruction.md) |
| M7 | tau_L exclusion from IC13 | Phase 33 | VERIFIED | accept-resolution | `../33-curriculum-stage-contracts/evidence/m7-tau-l-ic13-exclusion.md` | AC-CURR-02-M7 | `ctl_instruction.md` tau_L metadata exclusion | Phase 33 CURR-02; Phase 36 | 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2 (packet authored, tau_L staging/evaluation metadata exclusion from IC13 grounded in resolution doc §1.7 M7 accepted); 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2 (33-VERIFICATION.md records AC-CURR-02-M7 PASS: tau_L is staging/evaluation metadata, outside IC13 by design; spec transcription verified in ctl_instruction.md) |
| M14 | Gradient clipping divergence | Phase 32 | PENDING | accept-resolution | `evidence/m14-gradient-clipping.md` | AC-LOOP-04 | Phase 32 packet accepts structural merge only: Adam-only `clip_value = C_stage * median(recent global gradient norms)`, no L-BFGS clipping, CTL `7-10 / 5 / 3` preserved; bootstrap floor, exact early-stage `C`, lower floor, and history reset routed to Phase 34/FUT | Phase 34 LOOP-04; Phase 36 | 2026-06-21 pending-commit PENDING -> PENDING + accept-resolution by Phase 32 Plan 32-02 Task 2; structural merge adjudicated, spec transcription remains Phase 34-owned |
| M15 | Energy-loss weights | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-02 | `ctl_instruction.md` energy-loss weight schedule | Phase 35 LOSS-02; Phase 36 | Seeded; packet-before-edit forward reference |
| M16 | dt_out-aware collocation scaling | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-06 | `ctl_instruction.md` dt_out collocation scaling contract | Phase 34 LOOP-06; Phase 36 | Seeded; packet-before-edit forward reference |
| D5 | Stage transitions | Phase 33 | VERIFIED | accept-resolution | `../33-curriculum-stage-contracts/evidence/d5-stage-transitions.md` | AC-CURR-03 | `ctl_instruction.md` dual-path transition criteria | Phase 33 CURR-03; Phase 36 | 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; 2026-06-23 f2c8a9b PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 3 (packet authored, ADVANCE/RECOVER/HALT-REVIEW state machine grounded in resolution doc §1.11 / 33-SPEC R3 / D-33-08; numeric thresholds remain provisional pending FUT Stage-0 pilot per D-33-09); 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2 (33-VERIFICATION.md records AC-CURR-03 PASS: ADVANCE/RECOVER/HALT-REVIEW anchored inside the Stage Transition Criteria section, superseded Author-note musing gone, degraded-advancement routing verified; numeric thresholds remain provisional pending FUT Stage-0 pilot; spec transcription verified in ctl_instruction.md) |
| NS-12 | Componentwise automatic differentiation | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01-AD | `ctl_instruction.md` loss scaling and AD cross-link | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-13 | Energy Huber delta | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-03 | `ctl_instruction.md` Huber delta calibration contract | Phase 35 LOSS-03; Phase 36 | Seeded; packet-before-edit forward reference |
| NS-18 | Loss scaling and units | Phase 35 | PENDING | - | Owner must author packet before spec edits | AC-LOSS-01 | `ctl_instruction.md` dimensionless loss scaling | Phase 35 LOSS-01; Phase 36 | Seeded; packet-before-edit forward reference |
| adaptive stage assignment | Data-driven adaptive stage assignment | Phase 33 | VERIFIED | accept-resolution | `../33-curriculum-stage-contracts/evidence/adaptive-stage-assignment.md` | AC-CURR-01 | `ctl_instruction.md` adaptive stage methodology | Phase 33 CURR-01; Phase 36 | 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2 (packet authored, offline-EDA + PCA + clustering + quantile-threshold methodology locked, Stage-2/Stage-5 refinement roles preserved, Table 4 rejected, population floor owner-pending per GAP-33-01); 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2 (33-VERIFICATION.md records AC-CURR-01 PASS: offline-EDA + PCA + clustering + quantile methodology, Stage-2 hierarchical-gold / Stage-5 quasi-random-gold refinement roles preserved, population safeguard value owner-pending FUT admitted-set EDA per GAP-33-01; spec transcription verified in ctl_instruction.md) |
| D = 6.694 | Raw-mass D conflict | Phase 32 | VERIFIED | accept-resolution | `evidence/d-6-694-conflict.md` | AC-EVID-15-D-CONFLICT | Current `ctl_instruction.md` raw-mass `D ~= 4.6416` convention stands; no Phase 32 spec edit; Phase 33 consumes D in `tau_L` and `L_max`; GAP-17 provenance remains provenance-only | Phase 33 CURR-02; Phase 36 provenance/deferred-list checker | 2026-06-21 pending-commit PENDING -> VERIFIED by Phase 32 Plan 32-02 Task 1; packet accepts the resolution-doc convention only after SCOPE-12, current-spec, v1.5 EVID-10, and first-principles checks; issue-doc `D = 6.694` and P4-1 rerun directive rejected |
| L_max / tau_L | L_max and tau_L formulas | Phase 33 | VERIFIED | accept-resolution | `../33-curriculum-stage-contracts/evidence/l-max-tau-l.md` | AC-CURR-02-LMAX | `ctl_instruction.md` L_max and tau_L formula contract | Phase 33 CURR-02; Phase 36 | 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2 (packet authored, characteristic-scale L_max + raw-mass D ~= 4.6416 + Rosenstein revisable baseline locked; tau_L estimator/units/thresholds owner-pending per GAP-33-02); AC-CURR-02 renamed to AC-CURR-02-LMAX per Plan 33-01 convention (CURR-02 covers both the L_max row and the M7 tau_L-exclusion row, so the L_max row needs the -LMAX suffix to coexist with AC-CURR-02-M7); 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2 (33-VERIFICATION.md records AC-CURR-02-LMAX PASS: characteristic angular-momentum scale L_max, not a proven global maximum, active raw-mass D ~= 4.6416 (D = 6.694 rejected provenance), Rosenstein revisable baseline; tau_L estimator/units/thresholds owner-pending per GAP-33-02; spec transcription verified in ctl_instruction.md) |
| ALM mu_p clamp | ALM mu_p clamp | Phase 34 | PENDING | - | Owner must author packet before spec edits | AC-LOOP-05 | `ctl_instruction.md` or `pinn_architecture.md` ALM update and optional clamp contract | Phase 34 LOOP-05; Phase 36 | Seeded; packet-before-edit forward reference |

## Non-Headline Packet Mandate

Every non-headline row above has exactly one primary owner phase from Phase 33, Phase 34, or Phase 35. That owner must author the evidence packet and update this ledger before editing any spec section for the row. Phase 36 must reject any spec edit whose row lacks packet/verdict linkage.

## Transition Logs

### D-04

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting Option A/B/C.
- 2026-06-21 pending-commit PENDING -> DEFERRED by Phase 32 Plan 32-03 Task 1; `evidence/d-04-causal-training-mode.md` records `defer-with-blocker`, cites issue-doc Option A/B/C and resolution-doc `surface_to_user` evidence, and routes final mode selection to Phase 35 `LOSS-04` plus Phase 34 `LOOP-01` only if batch-windowing changes.

### D-05

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting a gate frame.
- 2026-06-21 pending-commit PENDING -> DEFERRED by Phase 32 Plan 32-03 Task 2; `evidence/d-05-s-min-frame.md` records `defer-with-blocker`, cites issue-doc D-05 options plus resolution-doc `SMIN-01..03` / `DGR-02/03`, preserves matched-Plummer loss-side evidence, and routes final stage-gate frame selection to Phase 33 `CURR-05`.
- 2026-06-21 DEFERRED -> PENDING + accept-resolution by owner AskUserQuestion instruction; Option A ratified (unsoftened geometric stage gate + matched-Plummer residual/energy, `epsilon_train = 1e-5`); issue-doc `max(s_min, epsilon)` phrasing rejected per PHYS-03; gap marked RESOLVED-WITH-INSTRUCTION in 32-GAPS.md; Phase 33 `CURR-05` and Phase 35 own transcription.
- 2026-06-23 Phase 33 Plan 04 verification: Phase 33 consumed GAP-32-02 for the CURR-05 static-invariant s_min text (unsoftened geometric `s_min` stage gate transcribed into `ctl_instruction.md`; AC-CURR-05 PASS recorded in `33-VERIFICATION.md`). Phase 35 owns the loss-side matched-Plummer softening transcription; Phase 33 did not close Phase 35 loss-side work (NS-12/NS-13/NS-18/M15 rows remain Phase 35 PENDING).

### D-06

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; unresolved owner decision routes to Phase 32 EVID-15 without selecting a static epsilon strategy.
- 2026-06-21 pending-commit PENDING -> DEFERRED by Phase 32 Plan 32-03 Task 3; `evidence/d-06-epsilon-strategy.md` records `defer-with-blocker`, cites issue-doc D-06 options plus resolution-doc `EPS-01..05` / `DGR-04` / `GAP-04`, preserves locked loss-side `epsilon_train = 1e-5`, and routes final static/invariant epsilon selection to Phase 33.
- 2026-06-21 DEFERRED -> PENDING + accept-resolution by owner AskUserQuestion instruction; dual-context ratified (`epsilon_inv = 1e-10` offline invariants/validation, `epsilon_train = 1e-5` training), consistent with v1.5-locked IPR (GAP-28-02) and the locked loss contract; Option C rejected; FUT/trainex sensitivity item logged; gap marked RESOLVED-WITH-INSTRUCTION in 32-GAPS.md; Phase 33 and Phase 35 own transcription.
- 2026-06-23 Phase 33 Plan 04 verification: Phase 33 consumed GAP-32-03 for the static-invariant epsilon text (`epsilon_inv = 1e-10` offline invariants/validation transcribed into `ctl_instruction.md` alongside the matched-Plummer `epsilon_train = 1e-5` loss-side reference; verified in `33-VERIFICATION.md` CURR-05 token check). Phase 35 owns the loss-side consistency transcription; Phase 33 did not close Phase 35 loss-side work.

### B-07

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### B-08

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### M6

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.
- 2026-06-23 f2c8a9b PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 3; `../33-curriculum-stage-contracts/evidence/m6-l-norm-metadata.md` records `accept-resolution` for raw `L_norm` metadata storage + mandatory degenerate-`L_max` diagnostic guard, rejects the original "clamp before IC mapping" rationale (M6-01 rejected), and routes the clipped-gate-vs-raw question to the owner after admitted-set evidence (M6-02 `surface_to_user`, M6-03 defer, DGR-07) per GAP-33-03. AC ID renamed: the seeded CURR-04 AC ID carried a redundant M6 suffix that was dropped per Plan 33-01 convention (M6 is the only CURR-04 row, so the suffix was redundant). Spec transcription remains Phase 33 Plan 33-02-owned.
- 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2; `33-VERIFICATION.md` records AC-CURR-04 PASS: raw un-clipped `L_norm` storage, mandatory nonfinite/near-degenerate `L_max` diagnostic guard, "No global clamp is authorized", `np.clip(L_norm, 0, 1)` stage-gate NOT locked (owner-pending admitted-set evidence per GAP-33-03). Spec transcription verified in `ctl_instruction.md`.

### M7

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.
- 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2; `../33-curriculum-stage-contracts/evidence/m7-tau-l-ic13-exclusion.md` records `accept-resolution` for the `tau_L` staging/evaluation metadata exclusion from `IC13`, grounded in resolution doc §1.7 (M7 `accepted`; M7-01 and M7-02 both `accepted`), the current spec `IC13` assembly, and SCOPE-12. Spec transcription remains Phase 33 Plan 33-02-owned.
- 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2; `33-VERIFICATION.md` records AC-CURR-02-M7 PASS: `tau_L` is staging/evaluation metadata, outside `IC13` by design. Spec transcription verified in `ctl_instruction.md`.

### M14

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; headline packet is owned by Phase 32 before Phase 34 transcription.
- 2026-06-21 pending-commit PENDING -> PENDING + accept-resolution by Phase 32 Plan 32-02 Task 2; `evidence/m14-gradient-clipping.md` accepts the grounded structural merge only and routes bootstrap floor, exact early-stage `C`, lower floor, and history-reset mechanics to Phase 34/FUT.

### M15

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### M16

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

### D5

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.
- 2026-06-23 f2c8a9b PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 3; `../33-curriculum-stage-contracts/evidence/d5-stage-transitions.md` records `accept-resolution` for the ADVANCE / RECOVER / HALT-REVIEW state-machine contract grounded in resolution doc §1.11 / `33-SPEC.md` R3 / `33-CONTEXT.md` D-33-08; the percentile-10 relaxation, per-stage `epsilon_phys` / `epsilon_energy` table, per-stage MAX_EPOCHS table, stagnation window, and retry protocol remain `claimed-unverified` (D5-05; CLM-08/09) and provisional pending FUT Stage-0 pilot calibration per `D-33-09`. Spec transcription remains Phase 33 Plan 33-03-owned.
- 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2; `33-VERIFICATION.md` records AC-CURR-03 PASS: ADVANCE / RECOVER / HALT-REVIEW anchored inside the `## Stage Transition Criteria` section, superseded "Author note" musing gone, no degraded automatic advancement, Stage-0 pilot calibration still provisional per D-33-09. Spec transcription verified in `ctl_instruction.md`.

### NS-12

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-13

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### NS-18

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 35 must author the packet before spec edits.

### adaptive stage assignment

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.
- 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2; `../33-curriculum-stage-contracts/evidence/adaptive-stage-assignment.md` records `accept-resolution` for the offline-EDA -> robust transforms -> PCA -> clustering -> quantile-threshold methodology augmenting the static theoretical anchors within the existing multi-fidelity Stage 0-6 topology, with stable `record_key` labels and Stage-2 hierarchical-gold / Stage-5 quasi-random-gold refinement roles preserved (Table 4 rejected; ADAPT-03 / DGR-15); the 5% / `>10%` / adaptive population safeguard value is owner-pending the FUT admitted-set EDA (SCOPE-15) per GAP-33-01. Roadmap / `CURR-01` `>10%` phrasing superseded. Spec transcription remains Phase 33 Plan 33-02-owned.
- 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2; `33-VERIFICATION.md` records AC-CURR-01 PASS: offline-EDA -> PCA + clustering + quantile-threshold methodology, Stage-2 hierarchical-gold / Stage-5 quasi-random-gold refinement roles preserved, population safeguard value owner-pending FUT admitted-set EDA (SCOPE-15) per GAP-33-01. Spec transcription verified in `ctl_instruction.md`.

### D = 6.694

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 32 packet owns convention lock, Phase 33 consumes tau_L/L_max, and Phase 36 checks unresolved provenance/deferred-list handling.
- 2026-06-21 pending-commit PENDING -> VERIFIED by Phase 32 Plan 32-02 Task 1; `evidence/d-6-694-conflict.md` records `accept-resolution` for the raw-mass `D ~= 4.6416` convention, rejects the issue-doc `D = 6.694` / P4-1 blanket rerun directive, and preserves GAP-17 as provenance-only.

### L_max / tau_L

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 33 must author the packet before spec edits.
- 2026-06-23 699b849 PENDING -> IN_PROGRESS + accept-resolution by Phase 33 Plan 33-01 Task 2; `../33-curriculum-stage-contracts/evidence/l-max-tau-l.md` records `accept-resolution` for the characteristic-scale `L_max = M_tot * r_char * sqrt(2|E|/M_tot)` (LMAX-01 accepted; LMAX-02 characteristic, not maximum), raw-mass `D ~= 4.6416` active (Phase 32 `D = 6.694` packet; SCOPE-12), and Rosenstein-style revisable baseline (TAUL-04 accepted); the `tau_L` estimator, time-unit convention, fit parameters, uncertainty handling, and final stage thresholds are owner-pending (TAUL-01 `surface_to_user`, TAUL-03 defer) per GAP-33-02; the issue-doc shadow method, its `epsilon_pert` / `epsilon_soft` shadow parameters, and the unspecified PCA+Rosenstein shortcut are NOT normatively adopted (TAUL-02, TAUL-05 rejected). AC ID renamed `AC-CURR-02` -> `AC-CURR-02-LMAX` per Plan 33-01 convention (CURR-02 covers both this L_max row and the M7 tau_L-exclusion row, so the L_max row needs the `-LMAX` suffix to coexist with `AC-CURR-02-M7`). Roadmap / `CURR-02` shadow + PCA/Rosenstein phrasing superseded. Spec transcription remains Phase 33 Plan 33-02-owned.
- 2026-06-23 6d4050e IN_PROGRESS -> VERIFIED + accept-resolution by Phase 33 Plan 33-04 Task 2; `33-VERIFICATION.md` records AC-CURR-02-LMAX PASS: characteristic angular-momentum scale `L_max` (not a proven global maximum), active raw-mass `D ~= 4.6416` (`D = 6.694` rejected provenance only, not the active scale), Rosenstein-style revisable baseline retained; `tau_L` estimator/units/thresholds owner-pending per GAP-33-02; issue-doc shadow method + PCA+Rosenstein shortcut NOT normative. Spec transcription verified in `ctl_instruction.md`.

### ALM mu_p clamp

- 2026-06-21 pending-commit PENDING seeded by Phase 32 Plan 32-01 Task 3; Phase 34 must author the packet before spec edits.

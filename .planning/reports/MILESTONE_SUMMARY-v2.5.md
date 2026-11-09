---
status: active
purpose: governance
created: 2026-11-08
milestone: v2.5
phase: cross-cutting
retirement_trigger: superseded by the v2.6 closeout summary
---

# Project Summary — Three-Body Physics-Informed LLM (v2.5)

**Generated:** 2026-11-08
**Purpose:** Team onboarding and milestone review
**Status:** All five v2.5 phases (65–69) are complete and verified (`passed`, 0 critical blockers); 13/13 requirements satisfied. At Owner Checkpoint 3 (`69-RULING.md`, 2026-11-08), the owner authorized the `trainex-r5` redesign review and selected **Direction A** (keep the current 12×256 SQR-SkipResNet-SIREN architecture as a supervised fit control and prioritize the training recipe and physics pipeline in v2.6).
**Sources:** PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md, v2.5-MILESTONE-AUDIT.md, 65-VERIFICATION.md, 66-VERIFICATION.md, 67-VERIFICATION.md, 68-VERIFICATION.md, 69-VERIFICATION.md, 65-01..06-SUMMARY.md, 66-01..05-SUMMARY.md, 67-01..16-SUMMARY.md, 68-01..02-SUMMARY.md, 69-01..03-SUMMARY.md, 66-CHECKPOINT-1-RULING.md, 67-EXP03-RULING.md, 68-CHECKPOINT-2-RULING.md, 69-RULING.md, 69-FINDINGS.md, 69-HANDOFF.md.

---

## 1. Project Overview

### Core Value

Every specification claim and every training result must be backed by verified evidence, not asserted by prose or inferred from non-conformant runs. In v2.5, every probe reproduction, diagnostic fit, design-ladder cell, known-answer yardstick check, and owner-facing finding is pre-registered before execution, bound by SHA-256 digests, and re-derived by an independent verifier (`verify_phase69.py`) that shares no code with the producers.

### What Was Built in v2.5

v2.5 is **Root-Cause Confirmation**. After v2.4 closed at Gate G2 with `RETHINK-REPRESENTATION` and discovered that every Phase 60 network had converged to a time-constant predictor (predicting each body's time-averaged position), the owner chose `change-course` and directed v2.5 to confirm in-house why the time signal vanished before opening the `trainex-r5` redesign round for v2.6:

1. **Phase 65 — Probe On-the-Record & Fit Harness:** Placed the 2026-10-27 exploratory time-signal probe on the record (`DIAG-09`) with exact formatter-cell reproduction across all 7 Phase 60 arms (`144/144` required historical fields reproduced, `0` failures) and built `INST-08`, the bounded single-orbit data-only diagnostic fit harness with Stage-0 training-split guards, production evaluation/resume isolation, logger-parity proof, and a 20-step real smoke fit (`seconds_per_step = 0.014265`).
2. **Phase 66 — Small-Network Control:** Ran the 1-hidden-layer 384-wide SIREN control (`157,065` parameters vs `795,657` locked, `first_omega_0 = 1000`, `lr = 1e-4`, `N = 465,000` steps) on `1632/s42`, `851/s42`, and `1632/s41` (`EXP-01`). All three runs reached settled Tier 1 (`E = 0.01143`, `0.01721`, `0.07898`; valid horizon `10.0`, `still_improving = false`), refuting "network too small for one orbit" and mechanically confirming `route = phase67-as-planned`. At Owner Checkpoint 1 (`66-CHECKPOINT-1-RULING.md`), the owner accepted the recorded proposal (`Accept the recorded proposal`).
3. **Phase 67 — Design & Settings Ladders:** Built the multi-arm ladder harness with cost-only common step budgets and executed 60 timing rows, 4 guarded metadata captures, and 60 single-look science rows across four ladders (`EXP-02` depth `2/4/6/8/12`, `EXP-03` learning rate `1e-3/3e-4/1e-4/3e-5/1e-5`, `EXP-04` time input raw vs 1-harmonic and 2-harmonic orbit-scaled Fourier on both `locked-12` and `exp01` backbones, `EXP-05` signed-lap window `1/2/5/10` inner laps). **Headline finding:** `EXP-03` confirmed at pre-registered confirmation grade that `lr = 1e-3` (the Phase 60 learning rate) **worsens** fit relative to `lr = 1e-4` across all three cases (`E = 1.4552`, `1.2422`, `1.1583`, all settled Tier 0), while the **locked 12×256 architecture at `lr = 1e-4` reached settled Tier 1 on all three cases** (`E = 0.04069`, `0.09550`, `0.03492`; valid horizon `10.0`). An owner ruling (`67-EXP03-RULING.md`) resolved the reserved `REFUTED-LEAD` branch and authorized `EXP-04` and `EXP-05`.
4. **Phase 68 — Yardstick:** Audited the energy/angular-momentum yardstick and the Stage-0 pass bars on known answers (`YARD-01..03`): the constant predictor, the two-Kepler formula, and Brutus's exact trajectories on the stored gold grid (`Δt ≈ 0.01`) and base grid (`Δt = 0.08`). Proved that a constant predictor trivially passes the finite-difference energy gate (`ε_H = 0.0`, `SCS = -inf`) while Brutus's exact answer fails it (`ε_H = 0.00109..0.02380` on gold, `0.047..0.38` on base) and passes only with exact velocities (`ε_H = 1.07e-14..2.09e-14`). At Owner Checkpoint 2 (`68-CHECKPOINT-2-RULING.md`), the owner selected `C-7: A` (autograd velocities), closing `GAP-59-08`, left `C-2, C-4, C-5, C-6` open for separate discussion, and routed `ROUT-68-01..05` (including `C-11`) to v2.6.
5. **Phase 69 — Findings & Redesign Decision:** Consolidated all v2.5 evidence into `69-FINDINGS.md`, `69-EVIDENCE.md`, `69-ACCOUNTING.md`, `69-CHECKPOINT.md`, `69-RULING.md`, and `69-HANDOFF.md` (`VERD-01`, `VERD-02`, `VER-23`), backed by `evidence/69-evidence.json`, `evidence/verify_phase69.py` (`PHASE69-ALL-OK`), and `107,626.594706 s` (`29.90 hours`) of measured compute across 129 published attempts + 1 yardstick capture. At Owner Checkpoint 3 (`69-RULING.md`), the owner authorized `trainex-r5` and selected **Direction A**.

### Technology Stack

| Layer | Choice | Notes |
|---|---|---|
| Language & env | Python 3.11 in `<home>/miniforge3/envs/pinn-train` | Always invoked with `-B` |
| Deep learning | PyTorch (`mps` float32 for diagnostic fits; `cpu` float64 for probes, yardstick, and independent cross-checks) | Apple M5 Pro, 24 GB unified memory |
| Diagnostic stack | `pinn/verification/diagnostic_{variants,similarity,fit,guard,data,probe,power,phase66,phase67}.py`, `yardstick_audit.py` | Built on the frozen Phase 59 `feasibility_scorecard.py` and `split_allowlist.py` |
| Verification | Phase-scoped verifiers (`verify_phase69.py`, `diagnostic_phase67 audit-phase`, `yardstick_audit --check`) + `unittest` suites (`tests/phase65..69`) | 786 unit tests across Phases 65–69 |

### Constraints and Scope Discipline

- **Single machine:** All computation ran on the owner's MacBook Pro (M5 Pro, 24 GB); long runs gated on AC power and the weekend window (`Saturday 00:00 – Sunday 22:00 America/Chicago`) via `diagnostic_power.py`.
- **`SCOPE-45` (no unapproved architecture):** Only pre-registered diagnostic variants (`locked-12`, `exp01`, and the Phase 67 ladder variants) were instantiated inside the diagnostic harness; production `pinn/model.py` was not replaced.
- **`SCOPE-46` (no spec edits):** `ctl_instruction.md`, `pinn_architecture.md`, and `sampling_method.md` remained byte-identical throughout v2.5; all Phase 68 yardstick amendments (`ROUT-68-01..05`) were routed to v2.6.
- **`SCOPE-47` (no held-out evaluation):** Zero test-split files were opened; `pinn/evaluate.py` was never invoked on diagnostic runs and actively refuses `inst08-diagnostic` checkpoints.
- **`SCOPE-48` (no full Stage-0 curriculum run):** All v2.5 fits were bounded single-orbit data-only diagnostics (`L_data` only, `λ_phys = λ_IC = λ_E = λ_L = 0`).
- **`SCOPE-49` (evidence-driven roadmap pivots):** Every reserved branch (`EXP-01` unsettled at Checkpoint 1, `EXP-03` refuted-lead after `lr1e-3` worsened, Checkpoint 2 yardstick, Checkpoint 3 direction) went through explicit owner rulings.

---

## 2. Architecture & Technical Decisions

### Architecture Overview

```
simulation_data/ (Stage-0 train-split gold records: 1632, 851, 4658)
        │
        ▼
pinn/verification/split_allowlist.py ──► pinn/verification/diagnostic_data.py
  (blocks test-split opens;                (Stage0TrainingReader; verifies
   attestation counter)                     generation-7 manifest & stats SHA-256;
        │                                   exact float64 window [0, W])
        ├──────────────────────────────────────────────────────┐
        ▼                                                      ▼
pinn/verification/diagnostic_probe.py          pinn/verification/diagnostic_fit.py
  (DIAG-09: read-only 7-arm reproduction         (INST-08: data-only Huber L_data fit;
   on CPU float64; formatter-cell equality;       constant-rate Adam; shared measure_time_signal;
   optimizer interlock)                           marks checkpoints inst08-diagnostic)
        │                                                      │
        │                                      ┌───────────────┴───────────────┐
        │                                      ▼                               ▼
        │                       diagnostic_phase66.py           diagnostic_phase67.py
        │                         (EXP-01: 1×384, ω₀=1000,        (EXP-02 depth, EXP-03 LR,
        │                          weekend/AC power gate,          EXP-04 Fourier/scaled-τ,
        │                          5-label reading rule)           EXP-05 signed-lap windows;
        │                                      │                   cost-only common N budget)
        │                                      │                               │
        ▼                                      ▼                               ▼
pinn/verification/yardstick_audit.py ──► .planning/phases/69-findings-redesign-decision/
  (YARD-01..03: known-answer audit on      (69-FINDINGS.md, 69-CHECKPOINT.md, 69-RULING.md,
   constant, two-Kepler, Brutus exact;      69-HANDOFF.md, verify_phase69.py)
   closes GAP-59-08 via C-7: A)
```

### Key Technical Decisions

| Decision | Phase | Rationale |
|---|---|---|
| Exact formatter-cell equality for historical probe reproduction (`D-03`) | 65 | Every historical `.2f`/`.3f`/`.4f`/`.3g` token defines an exact IEEE-754 double interval; prevents post-hoc tolerance widening while respecting rounding boundaries |
| Guarded Stage-0 training data seam with pre-recorded normalizer (`77526e53…`) | 65 | Reconstructs the exact generation-7 input normalization from Phase 59 `reader_acceptance.json` without opening Stage-1 or validation/test records |
| Dual-boundary diagnostic checkpoint isolation (`inst08-diagnostic`) | 65 | Both `pinn/evaluate.py` and `pinn/train.py --resume` refuse diagnostic checkpoints at entry and at payload deserialization (`DiagnosticCheckpointRefused`) |
| Cost-only common step budget `N` derived from timing runs before science registration | 66, 67 | Sizes `N` strictly from measured `seconds_per_step` and fixed overhead inside the 3,300 s / 3,540 s cap with scores hidden during timing check, preventing adaptive stopping on quality |
| Settlement gates in code (`0.01` output movement in Phase 66; `5%` final-quarter relative `E` in Phase 67) | 66, 67 | Requires `|output_movement(N) - output_movement(≤0.75·N)| < 0.01` in `EXP-01` and `(E_3N/4 - E_N) / E_3N/4 <= 0.05` on all six paired endpoints in `EXP-02..05` before confirming any contrast |
| Digest-bound owner ruling for `EXP-03` refuted-lead branch (`67-EXP03-RULING.md`) | 67 | When `lr = 1e-3` was confirmed-worsening (refuting the rate-sensitivity-improves hypothesis), `check-review` halted dependent launches until the owner ruled `proceed with option 1` |
| Known-answer yardstick audit before setting Stage-0 pass bars (`C-7: A`) | 68 | Demonstrated that finite-difference velocities let a constant predictor pass `ε_H ≤ 1e-5` (`ε_H = 0.0`) while failing Brutus's exact trajectory (`ε_H = 0.00109..0.38`); owner ratified autograd velocities (`C-7: A`) |
| Recipe-confound separation in `69-FINDINGS.md` and **Direction A** at Checkpoint 3 | 69 | Phase 60's `r1-1632` (`E = 1.15739`, Tier 0) and Phase 67's `EXP-03 lr1e-4` control (`E = 0.04069`, settled Tier 1) share the exact 12×256 architecture and differ in five recipe axes (loss terms, optimizer/LR/clipping, time sampling, trajectory scope, step count); owner selected Direction A (`trainex-r5` targets recipe & physics pipeline, keeping the 12×256 architecture as a supervised fit control) |

---

## 3. Phases Delivered

### Phase 65: Probe On-the-Record & Fit Harness
- **Status:** Complete & verified (`65-VERIFICATION.md`: `passed`, 7/7 truths; 6 plans, 15 tasks)
- **Goal:** Put the exploratory time-signal probe on the record and build a reusable, guarded single-orbit fit harness.
- **What was built:**
  - `pinn/verification/diagnostic_{variants,similarity,fit,guard,data,probe}.py`: shared `measure_time_signal` centred-neighbour cosine/range/movement instrumentation, sealed `locked-12` variant registry, `Stage0TrainingReader`, `DiagnosticCheckpointRefused` isolation across `evaluate.py` and `train.py`, and committed-clean registration gates.
  - Preserved original 2026-10-27 exploratory scripts and tool transcripts (`evidence/original/`, `source-manifest.json`), pre-registered `65-PROBE-PREDICTION.md`, and executed the read-only 7-arm reproduction (`65-PROBE-RESULT.md`: `144/144` required fields reproduced, verdict `retained`) plus logger-parity proof (`evidence/probe/logger-parity.json`).
  - Executed the 20-step real MPS smoke fit on `hierarchical/gold/1632` (`65-FINDINGS.md`: `20/20` finite updates, `seconds_per_step = 0.014265`).
- **Key files:** `pinn/verification/diagnostic_probe.py`, `pinn/verification/diagnostic_fit.py`, `.planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-RESULT.md`, `65-FINDINGS.md`, `65-CLOSEOUT.md`.

### Phase 66: Small-Network Control
- **Status:** Complete & verified (`66-VERIFICATION.md`: `passed`, 37/37 must-haves; 5 plans, 14 tasks)
- **Goal:** Test whether a small shallow network (`1×384`, `first_omega_0 = 1000`, `157,065` parameters) can fit one orbit on the harness.
- **What was built:**
  - `pinn/verification/diagnostic_phase66.py` and `diagnostic_power.py` (fail-closed `pmset` AC power + `America/Chicago` weekend-window gate + `caffeinate` supervisor).
  - Pre-registered timing run (`5,200` steps) deriving the common budget `N = 465,000` steps (`loss_trace_stride = 47`), followed by three single-look science runs on `1632/s42` (`E = 0.01143`, settled Tier 1), `851/s42` (`E = 0.01721`, settled Tier 1), and `1632/s41` (`E = 0.07898`, settled Tier 1).
  - Published `66-RESULT.md` and recorded Owner Checkpoint 1 (`66-CHECKPOINT-1-RULING.md`: verbatim `Accept the recorded proposal`, routing `phase67-as-planned`).
- **Key files:** `pinn/verification/diagnostic_phase66.py`, `pinn/verification/diagnostic_power.py`, `.planning/phases/66-small-network-control/66-RESULT.md`, `66-CHECKPOINT-1-RULING.md`.

### Phase 67: Design & Settings Ladders
- **Status:** Complete & verified (`67-VERIFICATION.md`: `passed`, 4/4 criteria; 16 plans, 39 tasks)
- **Goal:** Vary one setting at a time (depth, learning rate, time input, time window) across three Stage-0 cases (`1632/s42`, `851/s42`, `1632/s41`) to isolate what drives or blocks single-orbit fitting.
- **What was built:**
  - `pinn/verification/diagnostic_phase67*.py`: variant registries (`EXP-02..05`), orbit-scaled Fourier input encoders (`diagnostic_time_features.py`), exact first-crossing signed-lap window slicer (`diagnostic_phase67_windows.py`), cost-only common budget calculator, blind timing verifier, and mechanical contrast reviewer.
  - Executed 60 timing rows, 4 metadata captures, and 60 science rows (`28.30 hours` combined wall):
    - **`EXP-02` (Depth `2/4/6/8/12` at `N = 152,900`):** `d8` and `d12` reached Tier 1 on all 3 cases (`d8` lowest `E = 0.01097..0.06808`), `d2` worsened to Tier 0 on all 3 cases; overall review `unsettled-continue` because `d12` main endpoint improved by `> 5%` in the final quarter.
    - **`EXP-03` (Learning rate `1e-3/3e-4/1e-4/3e-5/1e-5` at `N = 155,100`):** `lr1e-4` control reached **settled Tier 1 on all 3 cases** (`E = 0.04069`, `0.09550`, `0.03492`). `lr1e-3` was **confirmed-worsening** (`E = 1.4552`, `1.2422`, `1.1583`, settled Tier 0), triggering `REFUTED-LEAD`; owner ruled `proceed with option 1` (`67-EXP03-RULING.md`).
    - **`EXP-04` (Time input raw vs 1-harmonic and 2-harmonic orbit-scaled Fourier on `locked-12` and `exp01` backbones at `N = 112,700`):** all contrasts `unsettled-continue`; encoded inputs worsened `E` on `1632/s42` and `851/s42` and improved only on `1632/s41`.
    - **`EXP-05` (Window `1/2/5/10` inner laps at `N = 148,700`):** shorter windows lowered `E` on all 9 contrast cells (`relative_E_effect = 0.14..0.88`), overall `unsettled-continue` due to final-quarter settlement gates on `lap10`.
- **Key files:** `pinn/verification/diagnostic_phase67.py`, `.planning/phases/67-design-settings-ladders/67-EXP02..05-RESULT.md`, `67-EXP03-RULING.md`, `67-FINDINGS.md`.

### Phase 68: Yardstick
- **Status:** Complete & verified (`68-VERIFICATION.md`: `passed`, 5/5 criteria; 2 plans, 6 tasks)
- **Goal:** Check the energy/angular-momentum yardstick on known answers and settle the Stage-0 pass bars at Owner Checkpoint 2.
- **What was built:**
  - `pinn/verification/yardstick_audit.py`: deterministic CPU float64 known-answer audit on the Stage-0 panel (`1632`, `851`, `4658`), plus `68-AUDIT.md` and `68-CHECKPOINT-2.md`.
  - Recorded `68-CHECKPOINT-2-RULING.md`: owner selected `C-7: A` (autograd velocities), closing `GAP-59-08` in `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`, left `C-2, C-4, C-5, C-6` open for separate discussion, and routed `ROUT-68-01..05` (including `C-11` constant-predictor non-degeneracy guard) to v2.6.
- **Key files:** `pinn/verification/yardstick_audit.py`, `.planning/phases/68-yardstick/68-AUDIT.md`, `68-CHECKPOINT-2-RULING.md`, `evidence/yardstick-audit.json`.

### Phase 69: Findings & Redesign Decision
- **Status:** Complete & verified (`69-VERIFICATION.md`: `passed`, 23/23 must-haves; 3 plans, 8 tasks)
- **Goal:** Consolidate v2.5 root-cause findings, verify 13/13 requirement traceability (`VER-23`), and record Owner Checkpoint 3 (`VERD-02`) for `trainex-r5` and v2.6.
- **What was built:**
  - `evidence/verify_phase69.py` (stdlib-only independent verifier with `sources`, `cost`, `traceability`, `claims`, `ruling`, `handoff`, and `all` modes) and `evidence/69-evidence.json`.
  - `69-FINDINGS.md`, `69-EVIDENCE.md`, `69-ACCOUNTING.md`, `69-CHECKPOINT.md`, `69-RULING.md` (owner authorized `trainex-r5` and selected **Direction A**), and `69-HANDOFF.md`.
- **Key files:** `.planning/phases/69-findings-redesign-decision/69-FINDINGS.md`, `69-EVIDENCE.md`, `69-ACCOUNTING.md`, `69-CHECKPOINT.md`, `69-RULING.md`, `69-HANDOFF.md`, `evidence/verify_phase69.py`.

---

## 4. Requirements Coverage

All **13/13** v2.5 requirements are **Complete** (`VER-23` verified at `13/13/13` across definitions, traceability table, and roadmap), and all **5/5** scope boundaries (`SCOPE-45..49`) held throughout the milestone:

| Requirement | Phase | Status | Evidence Summary |
|---|---|---|---|
| `DIAG-09` | Phase 65 | Complete | Original 2026-10-27 scripts & tool outputs preserved; 7-arm reproduction passed `144/144` required fields (`65-PROBE-RESULT.md`) |
| `INST-08` | Phase 65 | Complete | Guarded single-orbit `L_data`-only harness (`diagnostic_fit.py`), Stage-0 reader, diagnostic checkpoint refusal, 20-step smoke (`0.014265 s/step`) |
| `EXP-01` | Phase 66 | Complete | `1×384` (`157,065` params < `795,657`, `N = 465,000`) reached settled Tier 1 on all 3 runs (`E = 0.01143, 0.01721, 0.07898`); owner Checkpoint 1 ruled `phase67-as-planned` |
| `EXP-02` | Phase 67 | Complete | Depth ladder (`2, 4, 6, 8, 12`) at `N = 152,900` across 3 cases (15 timing + 15 science rows; `67-EXP02-RESULT.md`) |
| `EXP-03` | Phase 67 | Complete | LR ladder (`1e-3..1e-5`) at `N = 155,100`: `lr1e-3` confirmed-worsening (Tier 0), `lr1e-4` control settled Tier 1 on all 3 cases (`67-EXP03-RESULT.md`, `67-EXP03-RULING.md`) |
| `EXP-04` | Phase 67 | Complete | Time-input ladder (raw vs orbit-scaled Fourier `f1/f12` on `locked-12` and `exp01`) at `N = 112,700` (18 timing + 18 science rows; `67-EXP04-RESULT.md`) |
| `EXP-05` | Phase 67 | Complete | Signed-lap window ladder (`1, 2, 5, 10` inner laps) at `N = 148,700`: shorter windows lowered `E` on all 9 cells (`67-EXP05-RESULT.md`) |
| `YARD-01` | Phase 68 | Complete | Known-answer yardstick audit on constant predictor (`ε_H = 0.0` FD), two-Kepler (`0.98..2.63`), and Brutus exact (`0.00109..0.38` FD vs `1e-14` exact) (`68-AUDIT.md`) |
| `YARD-02` | Phase 68 | Complete | Charter rows `C-2, C-4, C-5, C-6, C-7` and new `C-11` presented with measured numbers (`68-CHECKPOINT-2.md`) |
| `YARD-03` | Phase 68 | Complete | Owner Checkpoint 2 ruling (`68-CHECKPOINT-2-RULING.md`): `C-7: A` closes `GAP-59-08`; `C-2, C-4, C-5, C-6` left open; `ROUT-68-01..05` routed to v2.6 |
| `VERD-01` | Phase 69 | Complete | Plain-English `69-FINDINGS.md` with per-hypothesis table, recipe reconciliation, yardstick summary, and `29.90 h` compute ledger |
| `VERD-02` | Phase 69 | Complete | Owner Checkpoint 3 (`69-RULING.md`): authorized `trainex-r5` and selected **Direction A**; carried into `69-HANDOFF.md` |
| `VER-23` | Phase 69 | Complete | `verify_phase69.py traceability` confirms `13/13/13` exact-set bijective mapping with 0 orphans, 0 duplicates, 0 conflicts |

---

## 5. Key Decisions Log

| Date | Source | Decision |
|---|---|---|
| 2026-10-27 | Milestone v2.5 start | Applied charter rows `C-12: A` and `C-13: A` (`PROJECT.md` rewrite), `C-14: B` (12 skipped v2.4 requirements stay in v2.4 archive), and **Order A** (confirm root cause in-house in v2.5 before opening `trainex-r5` for v2.6). |
| 2026-10-31 | Phase 65 closeout (`65-CLOSEOUT.md`) | Probe registration (`f469e003`) preserved as immutable historical evidence; historical probe stdout/summary defects and `WR-01` nested-marker limitation accepted with explicit reuse conditions before any future probe or graded use. |
| 2026-11-01 | Owner Checkpoint 1 (`66-CHECKPOINT-1-RULING.md`) | Owner replied `Accept the recorded proposal` (`phase67-as-planned`): proceed to Phase 67 on the locked `12×256` network after `EXP-01` (`1×384`, `ω₀ = 1000`, `lr = 1e-4`, `N = 465,000`) reached settled Tier 1 (`E = 0.01143..0.07898`). |
| 2026-11-05 | Phase 67 `EXP-03` ruling (`67-EXP03-RULING.md`) | After `lr = 1e-3` was confirmed-worsening (`E = 1.158..1.455` vs `lr = 1e-4` settled Tier 1 `E = 0.0349..0.0955`), owner replied `proceed with option 1` (`authorize-recorded-proposal`), unblocking `EXP-04` and `EXP-05`. |
| 2026-11-08 | Owner Checkpoint 2 (`68-CHECKPOINT-2-RULING.md`) | Owner selected `C-7: A` (autograd velocities), closing `GAP-59-08` as `RESOLVED-WITH-INSTRUCTION`, left `C-2, C-4, C-5, C-6` open for separate discussion, and routed `ROUT-68-01..05` (including `C-11`) to v2.6. |
| 2026-11-08 | Owner Checkpoint 3 (`69-RULING.md`) | Owner authorized `trainex-r5` and selected **Direction A** (keep the current 12×256 architecture as a supervised fit control and prioritize the training recipe and physics pipeline in v2.6). |

---

## 6. Tech Debt & Deferred Items

### Open / Routed Obligations for v2.6 (from `69-HANDOFF.md`)

1. **`trainex-r5` Redesign Research Round (Authorized under Direction A):**
   - Treat the locked 12×256 SQR-SkipResNet-SIREN architecture as a proven single-orbit supervised fit control (`E = 0.04069`, `0.09550`, `0.03492` at `lr = 1e-4`, `L_data`-only, `N = 155,100`) and focus `trainex-r5` on the five recipe/physics-pipeline confound axes that separated Phase 60 (`E = 1.15739`, Tier 0) from Phase 67 (`E = 0.04069`, Tier 1): (1) physics/IC/conservation loss terms vs `L_data`-only, (2) `lr = 1e-3` + median clipping + L-BFGS polish vs unclipped `lr = 1e-4` Adam, (3) resampled collocation vs fixed 1,001-sample grid, (4) multi-trajectory curriculum vs single-orbit fit, and (5) ~72k–99k steps vs 155,100 steps.
2. **Phase 68 Yardstick Routing (`ROUT-68-01..05`):**
   - `ROUT-68-01` / `ROUT-68-02`: Codify `C-7: A` (autograd velocities in canonical `(r', u)` scaled coordinates) in `ctl_instruction.md`, `pinn_architecture.md`, `pinn/verification/gate_metrics.py`, `pinn/training/validation_gate.py`, and `pinn/evaluate.py`.
   - `ROUT-68-03`: Separate discussion and owner ruling on open Stage-0 pass-bar charter rows `C-2` (position error bar), `C-4` (held-out pass fraction), `C-5` (angular-momentum bar), and `C-6` (energy drift bar `ε_H`).
   - `ROUT-68-04`: Decide and wire `C-11` (non-degeneracy / position-error prerequisite so a time-constant predictor with `v = 0` and `ε_H = 0.0` can never pass the energy gate alone).
   - `ROUT-68-05`: Revisit Stage 1–6 pass-bar charter rows (`C-8..C-10`) after Stage-0 bars are settled.
3. **Phase 65 Defect-Reuse Conditions (`65-CLOSEOUT.md`):**
   - `WR-01`: `require_not_diagnostic` nested-dict marker scan must be hardened before any graded or held-out evaluation use.
   - `WR-03` / `WR-04`: Historical probe stdout renderer (`preserved_only` branch), top-level `new_measurements` placement, and standalone `logger-parity` subcommand must be repaired and re-registered before any new `diagnostic_probe.py` execution.
4. **Carried-Forward Historical Items (`STATE.md`):**
   - `GAP-56-02` (`pinn_architecture.md` §2.4 table scope), two Phase 39 debug records (`phase39-collocation-slot-multiplicity`, `phase39-memory-guard-validation`), and two pending todos (`d-06-static-epsilon-sensitivity-check`, `trainex-r1-research-handoff`).

### Nyquist Validation Status

- **Compliant (`status: validated`, `nyquist_compliant: true`):** Phase 66, Phase 67, Phase 69.
- **Draft (`status: draft`, `nyquist_compliant: false`):** Phase 65 (204 unit tests green), Phase 68 (28 unit tests green).

---

## 7. Getting Started

### How to Run & Verify v2.5 Evidence

All verification commands are read-only, dataset-safe (zero test-split opens), and run in the `pinn-train` environment:

```bash
# 1. Run the independent Phase 69 milestone verifier (sources, cost, VER-23 traceability, claims, ruling, handoff)
<home>/miniforge3/envs/pinn-train/bin/python -B .planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py all

# 2. Verify all four Phase 67 ladders (EXP-02..05) and the Phase 68 yardstick audit
<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.diagnostic_phase67 audit-phase
<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.yardstick_audit --check .planning/phases/68-yardstick/evidence/yardstick-audit.json

# 3. Run the v2.5 unit test suites (Phases 65–69: 786 tests total)
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -t .
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase66 -t .
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase67 -t .
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase68 -t .
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase69 -t .
```

### Key Directories

| Path | Contents |
|---|---|
| `pinn/verification/` | Diagnostic probe, single-orbit fit harness, Phase 66/67 ladder runners, AC/weekend power guard, and Phase 68 yardstick audit |
| `tests/phase65/` .. `tests/phase69/` | Dataset-free synthetic and historical-evidence unit test suites for Phases 65–69 |
| `.planning/phases/65-probe-on-the-record-fit-harness/` | Phase 65 probe reproduction (`65-PROBE-RESULT.md`), smoke fit (`65-FINDINGS.md`), and closeout dispositions (`65-CLOSEOUT.md`) |
| `.planning/phases/66-small-network-control/` | Phase 66 `EXP-01` results (`66-RESULT.md`) and Owner Checkpoint 1 ruling (`66-CHECKPOINT-1-RULING.md`) |
| `.planning/phases/67-design-settings-ladders/` | Phase 67 `EXP-02..05` predictions, results (`67-EXP02..05-RESULT.md`), `67-EXP03-RULING.md`, `67-FINDINGS.md`, and 124 committed timing/metadata/science evidence records |
| `.planning/phases/68-yardstick/` | Phase 68 known-answer yardstick audit (`68-AUDIT.md`) and Owner Checkpoint 2 ruling (`68-CHECKPOINT-2-RULING.md`) |
| `.planning/phases/69-findings-redesign-decision/` | Phase 69 consolidated findings (`69-FINDINGS.md`), Owner Checkpoint 3 (`69-RULING.md`), v2.6 handoff (`69-HANDOFF.md`), and `evidence/verify_phase69.py` |

### Where to Look First

1. `.planning/phases/69-findings-redesign-decision/69-FINDINGS.md` — plain-English synthesis of every v2.5 experiment, the Phase 60 vs Phase 67 recipe reconciliation, the known-answer yardstick table, and the 29.90-hour compute ledger.
2. `.planning/phases/69-findings-redesign-decision/69-RULING.md` and `69-HANDOFF.md` — the owner's Checkpoint 3 ruling (**Direction A** + `trainex-r5` authorization) and the complete obligation ledger for v2.6.
3. `.planning/phases/68-yardstick/68-AUDIT.md` and `68-CHECKPOINT-2-RULING.md` — the known-answer proof that closed `GAP-59-08` (`C-7: A`) and the routed v2.6 charter/spec amendments (`ROUT-68-01..05`).

---

**Stats:** 5 phases (65–69) · 32 plans · 82 tasks · 325 commits · 880 files changed (+2,187,152 / −175) · 13 days (2026-10-27 → 2026-11-08) · 29.90 measured machine hours of v2.5 diagnostic compute (107,626.594706 s across 129 published attempts + 1 yardstick capture)


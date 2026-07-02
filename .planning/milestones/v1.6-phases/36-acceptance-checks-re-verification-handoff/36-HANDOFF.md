# Phase 36: v1.6 Milestone-Closure Handoff

**Plan:** Plan 36-04

**Executed:** 2026-07-02

**Status:** ✅ COMPLETE — v1.6 milestone closed: ledger terminal, all 26 acceptance probes PASS, SI table reconciled, every ledger finding classified exactly once, FUT-01 / FUT-04 routing captured.

---

## Evidence Used

- **Ledger snapshot:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` (after Plan 36-03 promotion; post-write SHA-256 `184cb56ff62caba140e9f35e9ddd857cd924d56354eed49f6de7d4144b5a7e10`). 18 rows total, 18 `VERIFIED`, 0 `PENDING`.
- **Phase 36 probe run:** `.planning/phases/36-acceptance-checks-re-verification-handoff/36-PROBE-RESULTS.md` (re-run 2026-07-02T00:39:33Z; 26/26 PASS). Per-probe SHA-256s recorded in `evidence/*.stdout.txt`.
- **Ledger closure record:** `.planning/phases/36-acceptance-checks-re-verification-handoff/36-LEDGER-CLOSURE.md` (D-05/D-06 transcription verdict CLEAN; pre-write SHA-256 `fb804f8b...`; promotion provenance recorded).
- **Phase 33/34/35 verification anchors:** `33-VERIFICATION.md`, `34-VERIFICATION.md`, `35-VERIFICATION.md` — each cited explicitly by Phase 36's AC-CURR/AC-LOOP/AC-LOSS probes.
- **Phase 30 completion anchor:** `.planning/ROADMAP.md` Phase 30 progress row (5/5, 2026-06-18) — anchors PKG-05/06/07/08 reconciliation.
- **trainex-r1 routing input:** `.planning/todos/pending/trainex-r1-research-handoff.md` (folded as routing obligation only, per D-36-13).

---

## SI Metadata Reconciliation

Fresh `rg "SI-[A-Z]+-[0-9]+"` over both framework specs (this session) returns exactly the four IDs:

| Entry | File:line | Status | Evidence / Reason / Gap |
|-------|-----------|--------|-------------------------|
| SI-CTL-001 | `ctl_instruction.md:2140` | **Retire-with-back-reference** | Input-vector dimensionality inconsistency — "Resolved by v1.4 finding B-03 / Phase 17." Self-states as resolved; back-ref: `33-VERIFICATION.md` AC-CURR-02-M7 (τ_L outside IC₁₃ by design) + `34-VERIFICATION.md` IC contract. No Issue-03 surface. |
| SI-PINN-003 | `ctl_instruction.md:1793` (canonical) + `pinn_architecture.md:1053,1056,1059` (RESOLVED log) | **Retire-with-back-reference** | Batch-construction inconsistency RESOLVED by Phase 34 (LOOP-01/02/03). `ctl_instruction.md` Mini-Batch Construction is canonical; pinn §3.1 author-comment inconsistency removed; RESOLVED log carries the disposition. Probe `AC-SI-PINN-003: PASS`. |
| SI-PINN-002 | `pinn_architecture.md:1047` | **Preserve-with-reason** | Three preserved author comments: (1) omega_0 dynamic scheduling detail, (2) hidden-layer detail, (3) batch-construction inconsistency. Comment (3) retired under SI-PINN-003 / Phase 34. Comments (1) and (2) are doc-01 (v1.4 architecture) author notes outside the Issue-03 curriculum/training-loop surface. Owner: future-architecture reconciliation. Probe `AC-SI-PINN-002: PASS`. |
| SI-DQA-003 | `ctl_instruction.md:548` | **Preserve-with-reason** | Inline citation on the conservation/SCS gate (`SCS = log10(eps_H)`, REJECT if `SCS > -5`, Plummer `eps=1e-10` in V). The SCS gate is the SCOPE-12 hard constraint (locked post-v1.3, carried into v1.4 EVID-15 D-CONFLICT and v1.5 EVID-10). The data-quality lineage citation predates Issue-03 (curriculum + training-loop) and is outside that scope; the lineage is preserved because the conservation/SCS gate is an inherited v1.3 contract that Phase 33/34/35 do not modify. Owner: future-data-quality reconciliation (v1.5 doc-02 lineage is read-only under SCOPE-09). Probe `AC-SI-DQA-003: PASS` (inline citation + data-quality lineage preserved). |

**Grep snapshot:** the SI table is built against the same checked working-tree snapshot as the AC probe suite run (2026-07-02T00:39:33Z). All four IDs are retired-with-back-reference or preserved-with-written-reason-and-owner; none is assumed resolved or irrelevant (VER-18).

**SI-DQA-003 Issue-03 adjudication:** The SCS-gate citation at `ctl_instruction.md:548` is grounded in `data_quality_assessment.md` (read-only under SCOPE-09) and SCOPE-12 (v1.5 SCS gate `ε_H > 10⁻⁵` / `SCS > -5` is hard constraint). These sources DO speak to the citation, so the disposition is sourced, not source-silent. No STOP gap is logged.

---

## Fixed

In-scope findings `VERIFIED` in the ledger (each row appears here exactly once; ordered by finding ID; cycle-4 HIGH-B partition discipline).

| Finding | Title | Acceptance Check | Resolving phase |
|---------|-------|------------------|-----------------|
| D-04 | Causal-training mode owner decision | AC-LOSS-04 | Phase 35 (LOSS-04; Phase 36 re-verify PASS) |
| D-05 | s_min frame owner decision | AC-EVID-15-D05 | Phase 36 (transcription CLEAN, promoted PENDING → VERIFIED) |
| D-06 | Epsilon strategy owner decision | AC-EVID-15-D06 | Phase 36 (transcription CLEAN, promoted PENDING → VERIFIED) |
| B-07 | Replay/lookahead batching | AC-LOOP-01 | Phase 34 (LOOP-01; Phase 36 re-verify PASS) |
| B-08 | Data versus collocation points | AC-LOOP-02 | Phase 34 (LOOP-02; Phase 36 re-verify PASS) |
| M6 | L_norm clamping | AC-CURR-04 | Phase 33 (CURR-04; Phase 36 re-verify PASS) |
| M7 | tau_L exclusion from IC13 | AC-CURR-02-M7 | Phase 33 (CURR-02-M7; Phase 36 re-verify PASS) |
| M14 | Gradient clipping divergence | AC-LOOP-04 | Phase 34 (LOOP-04; Phase 36 re-verify PASS) |
| M15 | Energy-loss weights | AC-LOSS-02 | Phase 35 (LOSS-02; Phase 36 re-verify PASS) |
| D5 | Stage transitions | AC-CURR-03 | Phase 33 (CURR-03; Phase 36 re-verify PASS) |
| NS-12 | Componentwise automatic differentiation | AC-LOSS-01-AD | Phase 35 (LOSS-01-AD; Phase 36 re-verify PASS) |
| NS-18 | Loss scaling and units | AC-LOSS-01 | Phase 35 (LOSS-01; Phase 36 re-verify PASS) |
| adaptive stage assignment | Data-driven adaptive stage assignment | AC-CURR-01 | Phase 33 (CURR-01; Phase 36 re-verify PASS) |
| D = 6.694 | Raw-mass D conflict | AC-EVID-15-D-CONFLICT | Phase 32 (EVID-15-D-CONFLICT; Phase 36 re-verify PASS) |
| L_max / tau_L | L_max and tau_L formulas | AC-CURR-02-LMAX | Phase 33 (CURR-02-LMAX; Phase 36 re-verify PASS) |

---

## Intentionally Unchanged

False-positive / valid-existing-convention non-changes (each row appears here exactly once).

| Finding | Title | Reason for "Intentionally Unchanged" |
|---------|-------|--------------------------------------|
| ALM mu_p clamp | ALM μ_p clamp | Spec carries `pinn_architecture.md` ALM update body as **optional / deferred**; `[1e-4, 100]` clamp is **conditional only**; dense-residual ALM remains **rejected from default loss**. Phase 34 already owns the defer; AC-LOOP-05 probe confirms the conditional / rejected state matches the spec wording. The non-change is that the conditional state is the correct transcription — no further action is required at spec level (LOOP-05 in the FUT below). |

(Notes: `M16` and `NS-13` are **defer-with-blocker** rows in the ledger and live in the Deferred table below, not here.)

---

## Deferred

`defer-with-blocker` rows + owner-pending FUT items (each row appears here exactly once; ordered by finding ID; each carries a written blocker + downstream owner).

| Finding / Gap | Title | Blocker | Downstream owner |
|---------------|-------|---------|------------------|
| M16 | dt_out-aware collocation scaling | Realized-as-deferred; candidate direction only; no probe-able `n_col=` formula; inverse form NOT adopted (`ctl_instruction.md:1819-1823`). AC-LOOP-06: PASS — deferred state is the correct transcription. | FUT-04 (training-loop impl + calibration) |
| NS-13 | Energy Huber δ | `delta_E = 1.0` baseline retained; empirical/median-scaled calibration deferred until admitted-set evidence exists. AC-LOSS-03: PASS — deferred state is the correct transcription. | FUT-04 (training-loop impl + calibration) |
| `ALM μ_p clamp` | (also in Intentionally Unchanged above for spec-level; the **deferred-blocker** side lives here for the residual `[1e-4, 100]` clamp activation gate) | Conditional clamp activation gate deferred; dense-residual ALM rejected from default loop; default-loop ALM update stays optional. | FUT-01 (rebuild) |
| GAP-33-01 | Population floor for adaptive stage assignment | Owner-pending FUT admitted-set EDA. Owner: trainex team. | FUT-04 (calibration) |
| GAP-33-02 | tau_L estimator / units selection | Owner-pending. Owner: trainex team. | FUT-04 (calibration) |
| GAP-33-03 | `np.clip(L_norm, 0, 1)` stage-gate vs raw storage | Owner-pending admitted-set evidence (decide locked vs raw based on observed overshoot). Owner: trainex team. | FUT-04 (calibration) |
| CURR-03 thresholds (D5-05) | Numeric Stage-0 pilot thresholds (4-criterion ADVANCE: training-loss plateau, validation-stability, physics-residual, energy-conservation) | Provisional pending FUT Stage-0 pilot calibration per D-33-09. | FUT-04 (Stage-0 pilot) |
| D-06 caveat | Epsilon train-vs-validate sensitivity on close-encounter admitted set | Owner-ratified dual-context (offline `ε_inv = 1e-10` / training `ε_train = 1e-5`); confirm close-encounter mismatch negligible on admitted set. Owner: trainex team. | FUT-04 (sensitivity analysis) |
| M14 sub-items | Bootstrap floor, exact early-stage C, lower floor, history reset | Routed by Phase 32 packet to Phase 34/FUT. Owner: trainex team. | FUT-01 (realize M14 mechanism) |

---

## FUT-01 (rebuild from specs)

Forward-pointing handoff to **FUT-01 / `pinn/STATUS.md`** (the only place `pinn/` references are permitted under SCOPE-10):

- **Componentwise AD executable strategy** (NS-12 / AC-LOSS-01-AD): canonical `u=t/T` autograd leaf; summed-output VJP rejected; executable memory/loop strategy is FUT work.
- **Gradient-clipping mechanism realization** (M14 / AC-LOOP-04): `clip_value = C_stage * torch.median(...)` mechanism (pinn §4.4); C-schedule `7-10 / 5 / 3` (ctl). Sub-items (bootstrap floor, exact early-stage C, lower floor, history reset) routed by the M14 packet.
- **Batch constructor / DataLoader** (B-07 / B-08 / LOOP-01 / LOOP-02 / LOOP-03): `B_replay = 240`, `B_lookahead = 16`, `has_stage(k+1)` guard; two independent point sets (data-fidelity snapshot vs collocation; data 50/50 retained, collocation 50/50 deferred).
- **ALM update + μ_p clamp** (LOOP-05): optional / deferred ALM body (pinn §4.2); `[1e-4, 100]` clamp conditional only; dense-residual ALM rejected from default loop.
- **Causal-mode mechanics** (D-04 / LOSS-04): per-time-step causal weighting baseline (Option A); dense-residual pseudo-ALM rejected; scalar ALM deferred.

## FUT-04 (resume training-loop impl + calibration)

Forward-pointing handoff to **FUT-04** (trainex track, training-execution track):

- **Adaptive-stage EDA + population floor** (CURR-01 / GAP-33-01).
- **Stage-0 pilot threshold calibration** (CURR-03 / D5-05): provisional numeric thresholds require FUT Stage-0 pilot.
- **tau_L estimator / units selection** (GAP-33-02).
- **Huber-δ empirical / median-scaled calibration** (NS-13 / AC-LOSS-03).
- **dt_out collocation scaling** (M16 / AC-LOOP-06): realized-as-deferred; candidate direction only.
- **IPR / PSC / SASD training-side numeric confirmation** (LOOP-07 / LOOP-08; provisional carry-forward with VAL-02/03/04 forward-references).
- **Epsilon train-vs-validate sensitivity** (D-06 caveat): confirm close-encounter mismatch negligible on admitted set.

## Consumption Notes

- **trainex-r1 routing input:** `.planning/todos/pending/trainex-r1-research-handoff.md` is **folded as a routing obligation only** (per D-36-13). It concerns review/handoff of trainex-r1 r1a/r1b research sub-packages and is not executed in v1.6.
- **pinn/STATUS.md** is the FUT-01 target. pinn/ references in this handoff are limited to the forward-pointing `36-CODE-DIVERGENCE.md` per SCOPE-10.

---

## Milestone-Closure Gate

| Gate criterion | Result |
|---------------|--------|
| Ledger terminal | ✅ 18 VERIFIED, 0 PENDING |
| All 26 acceptance probes PASS | ✅ per `36-PROBE-RESULTS.md` (re-run 2026-07-02T00:39:33Z) |
| Protected-path guard PASS | ✅ no probe touches `pinn/`; no git diff over `pinn/` or frozen specs |
| All four SI IDs disposed with citation / reason / STOP gap | ✅ see SI table above |
| Every ledger finding classified exactly once across Fixed / Intentionally Unchanged / Deferred | ✅ partition discipline per cycle-4 HIGH-B |
| FUT-01 / FUT-04 sections routed | ✅ see above + `36-CODE-DIVERGENCE.md` |
| trainex-r1 folded as routing input only | ✅ no ERW research executed |
| No framework spec or pinn/ file modified | ✅ `git diff` over those paths is empty |

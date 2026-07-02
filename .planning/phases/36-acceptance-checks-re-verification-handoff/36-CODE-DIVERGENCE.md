# Phase 36: Code-Divergence / Forward-Pointing FUT-01 / FUT-04 Record

**Plan:** Plan 36-04, Task 3 (companion to `36-HANDOFF.md`)

**Executed:** 2026-07-02

**Status:** Forward-pointing handoff only. The only place `pinn/` references are permitted under SCOPE-10 (user directive 2026-05-19; v1.4 FUT-01 directive; SCOPE-12 hard constraint at `.planning/REQUIREMENTS.md`).

---

## Scope

This document records the divergence between `pinn/basic_architecture.py` (v1.3-era live code; reference-only, NOT a grounding source) and the v1.4 + v1.5 + v1.6 framework specs (`ctl_instruction.md` and `pinn_architecture.md`). Divergences are listed as forward-obligations for **FUT-01** (rebuild from specs) and **FUT-04** (resume training-loop implementation + calibration). They are NOT instructions to edit `pinn/` in v1.6 — code edits land in the trainex track (`worktrees/trainex` on branch `track/trainex`).

---

## FUT-01 (rebuild from specs)

### Componentwise AD executable strategy (NS-12 / AC-LOSS-01-AD)

- **Spec anchor:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:310` (PHYS-02) — componentwise AD with canonical autograd leaf `u = t/T`; summed-output VJP rejected.
- **Current live-code (`pinn/basic_architecture.py`):** summed-output VJP (the v1.3-era implementation). To be re-implemented componentwise per the v1.5 NS-12 packet.
- **Owner:** trainex team, FUT-01.

### Gradient-clipping mechanism realization (M14 / AC-LOOP-04)

- **Spec anchor:** `pinn_architecture.md` §4.4 — `clip_value = C_stage * torch.median(torch.stack(grad_history))`; `ctl_instruction.md:1825-1849` carries the C-schedule `7-10 / 5 / 3` canonical home; bidirectional anchors.
- **Current live-code:** v1.3-era `nn.utils.clip_grad_norm_` with a hard-coded constant. To be re-implemented as the median-based adaptive clip.
- **Sub-items (deferred to FUT-01 / 04 by M14 packet):** bootstrap floor, exact early-stage `C`, lower floor, history reset.
- **Owner:** trainex team, FUT-01.

### Batch constructor / DataLoader (B-07 / B-08 / LOOP-01 / LOOP-02 / LOOP-03)

- **Spec anchor:** `ctl_instruction.md:1787-1799,1801-1818` — `B_replay = 240`, `B_lookahead = 16`, `has_stage(k+1)` guard, edge-case policy (GAP-34-01 Option A), two independent point sets (data-fidelity snapshot vs collocation, 8192/4096 provisional; data 50/50 retained, collocation 50/50 deferred-not-mandated).
- **Current live-code (`pinn/data-processing-pipeline-full.py`):** v1.3 DataLoader shape. To be re-implemented per the Phase 34 batch-construction contract; the data-fidelity / collocation separation is the canonical reconstruction.
- **Owner:** trainex team, FUT-01.

### ALM update + μ_p clamp (LOOP-05 / AC-LOOP-05)

- **Spec anchor:** `pinn_architecture.md:674` — ALM update body is optional / deferred; `[1e-4, 100]` clamp conditional only; dense-residual ALM rejected from default loss.
- **Current live-code:** v1.3 ALM with dense-residual pseudo-ALM. To be re-implemented with the dense-residual ALM rejected from default loss and the conditional clamp gated by the `[1e-4, 100]` window.
- **Owner:** trainex team, FUT-01.

### Causal-mode mechanics (D-04 / LOSS-04)

- **Spec anchor:** `pinn_architecture.md:424` + `ctl_instruction.md:1749,1803` — D-04 Option A: per-time causal weighting `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `w_1 = 1`, `η_c = 1`; dense-residual pseudo-ALM rejected; scalar ALM deferred P2.
- **Current live-code:** v1.3 per-time-step causal weighting baseline (already correct per Option A — verified by GAP-32-01 RESOLVED-WITH-INSTRUCTION consumption). The divergence is the **causal exponent clip bound**, which is currently `np.clip` global and is to be removed (the clip-bound is deferred to P2; current spec carries no global clip authorization).
- **Owner:** trainex team, FUT-01.

---

## FUT-04 (resume training-loop impl + calibration)

### Adaptive-stage EDA + population floor (CURR-01 / GAP-33-01)

- **Spec anchor:** `ctl_instruction.md:315-334,1632-1639` — offline-EDA → PCA + clustering + quantile methodology; Stage-2 hierarchical-gold / Stage-5 quasi-random-gold refinement roles preserved; Table 4 rejected; population safeguard **owner-pending FUT** (GAP-33-01).
- **Current live-code:** N/A in v1.3. Forward obligation: implement adaptive-stage EDA on the v1.5 dataset; choose a population floor based on the actual EDA distribution.
- **Owner:** trainex team, FUT-04.

### Stage-0 pilot threshold calibration (CURR-03 / D5-05)

- **Spec anchor:** `ctl_instruction.md:1836-1893` — ADVANCE / RECOVER / HALT-REVIEW state machine with provisional numeric thresholds (training-loss plateau, validation-stability, physics-residual, energy-conservation, 4-criterion ADVANCE).
- **Forward obligation:** numeric thresholds require FUT Stage-0 pilot calibration per D-33-09.
- **Owner:** trainex team, FUT-04.

### tau_L estimator / units selection (GAP-33-02)

- **Spec anchor:** `ctl_instruction.md:1311-1340` — `tau_L` is staging/evaluation metadata, outside IC₁₃ by design; estimator / units / thresholds **owner-pending admitted-set evidence**.
- **Owner:** trainex team, FUT-04.

### Huber-δ empirical / median-scaled calibration (NS-13 / AC-LOSS-03)

- **Spec anchor:** `pinn_architecture.md:537` + `ctl_instruction.md:1741` — `delta_E = 1.0` baseline retained; empirical / median-scaled calibration deferred.
- **Forward obligation:** admitted-set measurement to decide whether to retain the baseline or calibrate per-stage.
- **Owner:** trainex team, FUT-04.

### dt_out collocation scaling (M16 / AC-LOOP-06)

- **Spec anchor:** `ctl_instruction.md:1819-1823` — realized-as-deferred; candidate direction only; no probe-able `n_col=` formula; inverse form NOT adopted.
- **Forward obligation:** candidate-direction only; not implemented unless a future measurement motivates it.
- **Owner:** trainex team, FUT-04.

### IPR / PSC / SASD training-side numeric confirmation (LOOP-07 / LOOP-08)

- **Spec anchor:** `ctl_instruction.md:770` (LOOP-07 IPR provisional) and `ctl_instruction.md:684` (LOOP-08 SASD provisional) — provisional carry-forward with `IPR` / `PSC` / `SASD` tokens + `VAL-02` / `VAL-03` / `VAL-04` forward-references.
- **Forward obligation:** training-side numeric confirmation; admitted-set evidence for IPR / PSC / SASD roles.
- **Owner:** trainex team, FUT-04.

### Epsilon train-vs-validate sensitivity (D-06 caveat)

- **Spec anchor:** `ctl_instruction.md:287-303` — dual-context `epsilon_inv = 1e-10` (offline invariants) / `epsilon_train = 1e-5` (training) (Option A).
- **Forward obligation:** confirm close-encounter train-vs-validate mismatch negligible on admitted set.
- **Owner:** trainex team, FUT-04.

---

## trainex-r1 (routing obligation only, not executed)

- **Reference:** `.planning/todos/pending/trainex-r1-research-handoff.md`
- **Disposition:** routed as a **FUT/trainex** consumption obligation only. The Phase 36 plan does NOT execute the trainex-r1 ERW research workflow (D-36-13); the r1a / r1b research sub-packages are left to the trainex team for review/handoff during FUT-01 / FUT-04.

---

## Pinn reference discipline reminder

Per user directive 2026-05-19 (and SCOPE-10 / SCOPE-12 at `.planning/REQUIREMENTS.md`):

- **Live `pinn/` code is NOT a grounding source** — references above are forward-pointing only; no spec or handoff decision in v1.6 cites `pinn/` as authority.
- This document and `pinn/STATUS.md` (FUT-01 target) are the only places `pinn/` references are permitted.
- The current `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` are reference-only and will be rebuilt from the v1.4 + v1.5 + v1.6 framework specs in FUT-01.

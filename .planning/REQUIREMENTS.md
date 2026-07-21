# Requirements: Three-Body Physics-Informed LLM v2.0 — CTL-PINN Training Viability Slice

**Defined:** 2026-07-06
**Core Value:** A thin, Stage-0-first, end-to-end training run — built from the ratified trainex-r1a engineering decisions and the locked framework specs — that proves the CTL-PINN pipeline actually trains a model on the M5 Pro Mac and reaches the acceptance gate, before any effort is spent on the full multi-stage platform.

**Current workflow state:** v1.4 (doc-01), v1.5 (doc-02), and v1.6 (doc-03) are shipped and merged to `master`; the framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are complete and authoritative. The trainex-r1a build-design decision set was **owner-ratified 2026-07-05**. v2.0 is the project's first **build** milestone, opening the trainex (training-execution) track. Planning artifacts are committed on `master`; build execution happens in the `.worktrees/trainex` worktree (branch to be aligned to `milestone/v2.0` at first phase execution).

## Source treatment & build discipline

v2.0 is a **build** milestone, not a spec-adjudication milestone. It has no "candidate verdict source" to transcribe; it implements decisions that are already made. Two grounding sources are authoritative:

1. **The ratified trainex-r1a decision set** — `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/{trainex-r1a-resolution-doc.md, RATIFICATION.md}` (owner-ratified 2026-07-05): the ~24 engineering decisions **D1–D7 / B-1–B-11** and the §5 composed first-run recipe. Authoritative for build-engineering decisions (framework, config, checkpointing, guards, loop shape, determinism).
2. **The authoritative framework specs** — `ctl_instruction.md` / `pinn_architecture.md` (locked through v1.4/v1.5/v1.6): the science the build implements without re-deciding (14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-02 AD contract, PHYS-03 softening, PHYS-05 scheduled weights, the post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, the raw-mass `D ≈ 4.6416` convention, the Stage 0–6 curriculum and CURR-03 stage-exit machine, LOOP-01..08 batch/loop contracts, LOSS-01..04 loss contracts).

**The `pinn/` live-code ban is lifted for v2.0.** The 2026-05-19 directive kept v1.3-era code out of spec *adjudication*; that work is done. FUT-01 rebuilds `pinn/` **from** the specs; the v1.3-era `basic_architecture.py` / `data-processing-pipeline-full.py` are reference-only and are replaced wholesale.

**Owner-carved decisions are built as seams, not invented.** The ratification defers five decisions to the owner's designed moments. The build implements each as a **seam with a safe placeholder default** and surfaces the calibration evidence; the agent does not pick the value:

| Owner-carved decision | Designed moment | Safe seam default |
|---|---|---|
| **D1-p** precision (fp32-MPS vs fp64-CPU) | §10.3 componentwise-AD dual-arm probe (first build act) | config switch; every ratified pick holds under both branches |
| **D4-a** wall-clock checkpoint ceiling value | after the ~5-min smoke test measures s/step | dual-trigger present; ceiling in r1b's 15–30 min range, owner pick |
| **D4-c / R-2** RECOVER retry budget + HALT/REVIEW thresholds | after the Stage-0 pilot calibrates variance | `recover.retries: 0` (≡ Tier-1 stop-and-preserve); HALT placeholders |
| **R-1** guard thresholds (loss-explosion, disk-floor, memory-watermark) | after the Stage-0 pilot | guards present as seams; thresholds placeholder |
| **B-5** identity/operational resume-field list | before run #1 | field-classified diff; unclassified fields default to identity (refuse) |

**Scope is the viability slice.** Stage-0-first, single M5 Pro, in-memory data, manual rollback. The full multi-stage curriculum (Stages 1–6 end-to-end), streaming residency, auto-revert, stochastic-L-BFGS stages (3–6), RAD adaptive collocation, Tier-3 auto-remediation, and the trainex-r2 tuning round are **deferred pending the slice's go/adjust/rethink verdict** (Phase 43 / ACC-06).

## v2.0 Requirements

### Developer Environment & Precision Adjudication (ENV) — Phase 37

- [x] **ENV-01**: A one-command setup script takes a fresh M5 Pro Mac from no-Python to a ready `pinn-train` conda environment (Miniforge3 arm64, Python 3.11, PyTorch 2.12 + MPS, numpy/h5py/pyyaml/tensorboard), idempotently, and verifies `torch.backends.mps.is_available()`. [D1, §5 Setup]
- [x] **ENV-02**: Setup records an environment fingerprint (`sw_vers`, `python -V`, framework version/build, lockfile hash) and exports a reproducible environment pair (loose `environment.yml` + a pinned lockfile / `pip freeze`). [B-6 / r1b D-12]
- [x] **ENV-03**: The `pinn_architecture.md` §10.3 componentwise-AD probe runs **dual-arm** — fp32 on `mps` with `PYTORCH_ENABLE_MPS_FALLBACK` unset AND an fp64-CPU reference arm — timing both AD patterns (full-Jacobian vs scalar-`u` forward-mode), and produces the recorded evidence the owner uses to adjudicate **D1-p** (fp32 vs fp64). The precision verdict is surfaced, not chosen by the agent. [D1-p, U-9, R-6; first build act]
- [x] **ENV-04**: Precision is a single config-selected switch (`precision: float32|float64`, `device: mps|cpu`) such that every ratified pick holds identically under both branches (fp32-MPS / fp64-CPU), the fp64-CPU arm being the in-framework escape hatch. [D1-p round mandate]

### PINN Model Rebuild from Specs (NET) — Phase 38 (FUT-01 core)

- [ ] **NET-01**: The `pinn/` package is rebuilt from the authoritative framework specs (not the v1.3-era code): the SQR-SkipResNet-SIREN backbone (14-dim input `[τ, IC₁₃]` → 12×256 hidden → 9-dim output), SIREN `first_omega_0=30.0` / `hidden_omega_0=1.0`, skip + LayerNorm (`elementwise_affine=False`, odd layers) per `pinn_architecture.md`. [FUT-01; locked v1.4 ARCH]
- [ ] **NET-02**: The network applies the hard mass-weighted COM projection head to the 9-dim output before any loss or metric. [v1.4 D-02 locked]
- [ ] **NET-03**: Physics residuals are computed by autograd per the PHYS-02 AD contract (componentwise second derivatives w.r.t. the autograd leaf `u`, with the chain-rule factors `d²r'/du² = 4·d²r'/dτ²`, `dr'/du = 2·dr'/dτ`), validated by an fp64-CPU `gradcheck` and a residual-on-ground-truth probe. [PHYS-02, LOSS-01, §5 pre-flight rungs]
- [ ] **NET-04**: The loss is the locked five-term catalog — data Huber (`δ_r = 1`) on Brutus snapshots, IC squared-error anchors, causally-weighted physics residual, soft-energy Huber (`δ = 1.0`), and componentwise angular-momentum Huber (`δ = 1.0`), under the PHYS-05 scheduled weights — evaluated in the shared dimensionless coordinate system (`t_τ ∈ [-1,1]`, `r' = r/D`, raw-mass `D ≈ 4.6416`), per `pinn_architecture.md` §3/§4.1 and the `ctl_instruction.md` loss-function contract. [LOSS-01, PHYS-05, SCOPE-12 `D`; integrity-r2 PB-2]
- [ ] **NET-05**: A single-trajectory overfit probe (pre-flight rung 4) drives the data loss to near-zero, confirming the model + AD + loss are wired correctly end-to-end before any full run. [§5 rung 4]

### Data Ingestion & Stage-0 Population Scan (DATA) — Phase 39

- [x] **DATA-01**: A thin, format-aware adapter is the only component that imports the on-disk dataset format; it preloads the admitted set fully in-memory as fp32 (D3-C, `num_workers=0`), exposes `n_snapshots(traj)` / `dt_out(traj)` metadata (LOOP-06), and emits a `mem:` log line with a 0.7 watermark knob. [D3-C, LOOP-06]
- [x] **DATA-02**: The adapter applies the full Step-1A admission gate (clauses 1–7: identity & fail-closed blacklist, quarantine, structural integrity, completeness `final_timestep ≥ 9.5`, the conservation reject gate `eps_H ≤ 1e-5` / `SCS ≤ −5`, physical-invariant gates, grid-consistency WARN), logs admitted/rejected/quarantined counts, and drops NaN/Inf samples with a logged count. [Step-1A; design §4.2; integrity-r2 IR2-006]
- [x] **DATA-03**: The adapter reads `data_version_hash` and refuses to load on mismatch — a hard error, never a silent proceed. [design §4.2, U-12]
- [x] **DATA-04**: A deterministic, stage-stratified split manifest (train/val/test, ~80/10/10 default) is written to the run folder, partitioned by `physical_key = (variant, id)` first and expanded to all `record_key`s, with an assertion that no `physical_key` spans splits; the train split shuffles per-epoch under a seeded RNG while val/test iterate in fixed order. [design §4.2, PH-5 default; integrity-r2 PB-4]
- [x] **DATA-05**: The replay/lookahead batch constructor selects `B_replay = 240` trajectories from `D_≤k` plus `B_lookahead = 16` from `D_{k+1}` under the `has_stage(k+1)` guard (256 total) and emits the two independent point sets — data-fidelity points drawn from the selected trajectories' snapshots at `n_pts = min(32, n_snapshots)` (~8,192 points, provisional), and collocation points drawn as continuous samples from `[0, T]` (~4,096 points, provisional; energy reuses the physics collocation set) — with the 50% uniform + 50% acceleration-weighted time sampler applied to the data-fidelity set only (mixed continuous collocation stays deferred per LOOP-03), per the locked LOOP-01/02/03 contracts (provisional budgets). [LOOP-01/02/03; integrity-r2 PB-3]
- [x] **DATA-06**: A Thrust-A data scan bins the admitted trajectories by the difficulty invariants, counts per-stage populations (Stage 0 above all), flags an under-populated Stage 0 as a fatal-class risk — supplying the per-stage byte counts before any training run — and reports the admitted-set `s_min` distribution so the owner ratifies the data-derived Stage-0/1 threshold `s₀` (interim floor `s₀ = 0.01` until ratified). [§5 Step-0; partial FUT-02; integrity-r2 PB-1]

### Stage-0 Curriculum Training Loop (TRAIN) — Phase 40 (FUT-04 core)

- [x] **TRAIN-01**: A `CurriculumController` + `RunController` pair drives an outer curriculum loop and an inner optimization loop, implementing the `ctl_instruction.md` Stage-0 contract (the trainer implements the spec; it does not re-decide it). [B-3, D5-a]
- [x] **TRAIN-02**: Each stage runs the two-phase Adam→L-BFGS closure loop — Adam with PHYS-05 warmup → plateau handoff → full-batch L-BFGS via accumulate-in-closure; frozen-λ and no clipping during L-BFGS. [D5-a]
- [x] **TRAIN-03**: A scheduled loss-weight module implements the PHYS-05 schedule (warmup `I_warm = min(2000, 0.1·N_Adam,k)`, per-stage `λ^max` with `λ_E^max ≤ 1`, frozen during L-BFGS, re-warmed at boundaries) with its state serialized into checkpoints. [D5-c, PHYS-05, LOSS-02]
- [x] **TRAIN-04**: A collocation sampler interface (uniform + spec-adaptive) with the stateful `(model, last_residuals)` hook signature supplies interior points for the physics loss term. [D5-b, LOOP-03]
- [x] **TRAIN-05**: Merged gradient clipping applies `clip_value = C_stage · median(grad_norm_history)` with the per-stage C-table (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0) and a rolling window, and applies no clipping during L-BFGS. [LOOP-04, B-1]
- [x] **TRAIN-06**: The stage-exit state machine implements **ADVANCE** (the approved success gate: plateau + validation stability + `ε_phys`/`ε_energy`), **RECOVER** (NaN/Inf rollback with a bounded retry budget, default `recover.retries: 0`), and **HALT/REVIEW** (max-epoch / stagnation → owner review); there is no fallback advancement. Thresholds are safe placeholders pending Stage-0-pilot calibration (owner-ratified, not invented). [CURR-03, D4-c, R-1/R-2]
- [x] **TRAIN-07**: A preflight refuses to enter the stochastic-L-BFGS stages (3–6) until a concrete sL-BFGS implementation exists — a typed stop, not a silent science deviation (out of the slice's Stage-0–2 full-batch path regardless). [D5-a, U-7]

### Config, Checkpointing, Resume & Determinism (CTRL) — Phase 41

- [x] **CTRL-01**: A single YAML config keyed `run / stage / opt / loss` drives every run, with the fully-resolved config frozen into the run folder. [B-9]
- [x] **CTRL-02**: Checkpoints write on a dual trigger (every N steps OR a wall-clock ceiling, whichever first) with rolling-3 + `best.pt` + `latest.pt` + stage anchors retention; the wall-clock ceiling value is an owner pick (r1b 15–30 min range, informed by the smoke test). [D4-a]
- [x] **CTRL-03**: Checkpoint writes are atomic (tmp + fsync + rename), `weights_only`-clean, with a fallback scan on corruption. [D4-b]
- [x] **CTRL-04**: Dual stage-boundary anchors (`stage-{k}-final.pt` + `stage-{k+1}-init.pt`, excluded from rolling deletion) and idempotent ordered promotion with a `curriculum.jsonl` recording every promotion / RECOVER / HALT disposition. [D7-a, D7-d]
- [x] **CTRL-05**: `--resume <ckpt>` continues exactly; `--resume …/stage-{k}-final.pt --hold-stage` performs manual rollback; a field-classified resume config-diff refuses on any unclassified/identity-field change (fail-safe). The identity/operational field list is owner-ratified before run #1 (surfaced, not invented). [D7-c, B-5]
- [x] **CTRL-06**: Complete Adam reset at every stage boundary (spec "Critical"); L-BFGS history never crosses a boundary. [D7-b]
- [x] **CTRL-07**: Auto-guards Tier 1+2 are active (NaN/Inf, loss-explosion, disk-floor, memory-watermark) with the RECOVER seam and HALT/REVIEW family; guard thresholds are ⚖ placeholders calibrated against the Stage-0 pilot (owner-ratified, not invented); an always-on `failure/` diagnostic bundle (+ one-line README) is written on any guard trip. [D4-c, D4-d, R-1]
- [x] **CTRL-08**: Full seed/RNG state is recorded in the config and every checkpoint; reproducibility is scoped to statistical equivalence + exact checkpoint continuation (not bitwise re-creation), with a strict-CPU determinism debug switch. [D6, B-11]

### Operator Runbook Surface & Monitoring (OPS) — Phase 42

- [x] **OPS-01**: The operator drives training through five single-command entry points — Setup, Configure, Launch, Monitor, Resume — with internals hidden. [design §5]
- [x] **OPS-02**: Unattended runs launch under `caffeinate -is <cmd>` (lid-open + AC-power rule; SIGTERM treated as one graceful Ctrl-C → checkpoint). [B-10]
- [x] **OPS-03**: Every logged step emits the widened field set (5 loss terms + total + λ vector + grad-norm + `w_n` causal-weight stats + lr + s/step + ETA) to a canonical JSONL log, with TensorBoard as a secondary view in `runs/<name>/tb/`. [D2, B-2]
- [x] **OPS-04**: A `status.json` heartbeat and a periodic `mem:` line let the operator answer "is it alive / healthy?"; a per-time-bin residual panel surfaces causal-weight collapse and propagation failure. [B-2, design §6.1]
- [x] **OPS-05**: Each run produces the `runs/<name>/` contract (frozen `config.yaml`, `checkpoints/`, `logs/`, `summary.md`, `status.json`, `failure/`) such that handing over the directory reproduces the result. [design §5.7, B-6]
- [x] **OPS-06**: A written operator runbook under `docs/runbooks/` covers the mental model, the five entry points, the categorized error surface, and the M5-Pro-specific notes (unified memory, thermal, sleep, single-MPS-device). [design §5, §5.8]

### Verification, Stage-0 Pilot & Acceptance (ACC) — Phase 43

- [x] **ACC-01**: A `verify` pre-flight ladder (device sanity → §10.3 AD probe → fp64-CPU gradcheck → residual-on-ground-truth + remaining §10 probes → single-trajectory overfit) gates any run longer than the smoke test; no run > 30 min proceeds without it green. [§5 pre-flight]
- [ ] **ACC-02**: A ~5-minute smoke test (≈32 Stage-0 trajectories, ~300 steps, `checkpoint_every=100`) exercises the whole mechanical surface (Ctrl-C / resume included) and records the measured s/step, collapsing the ~30×-wide duration envelope into a per-run forecast that informs the D4-a ceiling. [§5 rung 6, D-5]
- [x] **ACC-03**: A separate `evaluate` script runs the held-out test set once and renders the binary post-v1.3 gate check (`ε_H > 1e-5` reject; `SCS > −5`) with plain-English metric descriptions in `metrics.md`. [design §6.3, B-8]
- [ ] **ACC-04**: An end-of-run `summary.md` reports final losses, a validation summary, curriculum progression, a test-set preview, and a run-to-run comparison hint; the honesty layer (healthy val ≠ working model; clean loss curve ≠ correct physics) is stated. [design §6.2, §6.4]
- [ ] **ACC-05**: The Stage-0 pilot repeats the short run 2–3× across seeds, records the seed-band spread in `summary.md`, and calibrates the ⚖ guard / RECOVER thresholds from the observed variance for owner ratification. [D6, R-1/R-2]
- [ ] **ACC-06**: The milestone closes with a **go / adjust / rethink** verdict on whether the Stage-0 viability slice justifies building the full multi-stage platform, and updates the FUT-01 / FUT-04 handoff with what shipped, what stayed a placeholder seam, and what was deferred. [RATIFICATION standing, §5 coherence]

## Future Requirements

Deferred to a later milestone (tracked, not in this roadmap). The Stage-0 slice's go/adjust/rethink verdict (ACC-06) decides whether and how these proceed.

### Full Platform (post-viability)

- **PLAT-01**: End-to-end multi-stage curriculum (Stages 1–6) with cumulative replay across all stages.
- **PLAT-02**: Stochastic-L-BFGS implementation for stages 3–6 (currently a typed preflight refusal, U-7).
- **PLAT-03**: Streaming / out-of-core data residency for later cumulative stages (the `auto` selector's non-in-memory branch).
- **PLAT-04**: D7-D divergence-quality auto-revert (deferred until a validated divergence signal exists).
- **PLAT-05**: RAD-style adaptive collocation densities (interface hook is present; strategies are future).
- **PLAT-06**: Tier-3 auto-LR remediation (excluded from the slice by design).
- **PLAT-07**: Automatic loss-weight dominance reweighting (the LOSS-02 rebalance seam stays empty in the slice).

### Carried from v1.6 (trainex track)

- **FUT-02**: Full curriculum-statistics EDA + stage-threshold recalibration (v2.0 runs only the Stage-0 Thrust-A scan, DATA-06).
- **FUT-03**: Package the disposable validation probes into reusable scripts under `pinn/validation/` (v2.0 builds them as the `verify` ladder, ACC-01).
- **FUT-05**: Adjudicate the author comments preserved by v1.4 Phase 22 (`22-COMMENT-HANDOFF.md`).
- **trainex-r2**: The post-framework hyperparameter/tuning research round.
- **LLM direction**: Qwen 3.5 2B fine-tuning for trajectory prediction (deferred until the PINN pipeline is proven).

## Cross-Project Documentation Requirements

- **REQ-DOC-01** (cross-project): Markdown framework specs are the authoritative design documents during active work; LaTeX sources are publication/archive derivatives synced only at the final publication stage. (Full text in `.planning/milestones/v1.4-REQUIREMENTS.md`.)

## Scope Boundaries

| Scope | Status |
|-------|--------|
| **SCOPE-16** Build target = the viability slice | **In scope.** Stage-0-first, single M5 Pro, in-memory data, manual rollback — a complete end-to-end vertical slice, not the full multi-stage platform. "Thin" = Stage-0 only; it is NOT thin on the model, loop, or verification (those are complete). |
| **SCOPE-17** Ratified trainex-r1a decisions | **In scope as authoritative build grounding.** D1–D7 / B-1–B-11 and the §5 first-run recipe are implemented as recommended; the five owner-carved decisions are built as seams (see the table above). |
| **SCOPE-18** Framework specs authoritative; `pinn/` ban lifted | **In scope.** `ctl_instruction.md` / `pinn_architecture.md` are read-only authoritative inputs; FUT-01 rebuilds `pinn/` FROM them. A spec defect discovered during the build is surfaced as a gap and routed to a spec milestone — v2.0 does not edit the specs. |
| **SCOPE-19** Owner-carved decisions | **Built as seams, not invented.** D1-p, D4-a ceiling, RECOVER budget + HALT thresholds (R-2), R-1 guard thresholds, and the B-5 field list are implemented with safe defaults; calibration evidence is surfaced for owner ratification at the designed moment. |
| **SCOPE-20** Single M5 Pro; no cloud/distributed | **Out of scope (hard constraint).** No cloud fall-back, no distributed / multi-GPU training; `torch.mps.device_count()` is 1. |
| **SCOPE-21** Frozen/read-only spec inputs | **Read-only.** `sampling_method.md` (SCOPE-08), `data_quality_assessment.md` / `review-of-framework.md` / `stage-strat-revision.md` (SCOPE-09) are unchanged; the two authoritative specs are inputs, not edit targets, in v2.0. |

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full multi-stage curriculum (Stages 1–6) end-to-end | The slice proves Stage 0; advancing all stages is the full platform (PLAT-01), gated on the ACC-06 verdict. |
| Stochastic-L-BFGS (stages 3–6) | No framework ships it (U-7); v2.0 installs a typed preflight refusal, not an implementation (PLAT-02). |
| Streaming / out-of-core data residency | The whole corpus is ≈0.55 GB fp32; in-memory suffices for the slice (PLAT-03). |
| Auto-revert (D7-D) | No validated divergence signal exists yet; manual `--hold-stage` only (PLAT-04). |
| Editing the framework specs | v2.0 implements the specs; spec changes are a separate spec milestone. A build-discovered spec defect is surfaced as a gap. |
| Editing `sampling_method.md` / `data_quality_assessment.md` / `review-of-framework.md` / `stage-strat-revision.md` | SCOPE-08 / SCOPE-09 (frozen / read-only). |
| Cloud, distributed, or multi-GPU training | Single M5 Pro hard constraint (SCOPE-20). |
| Modifying the Brutus C++ integrator | It works; the build consumes its dataset, it does not change the integrator. |
| Inventing the owner-carved ⚖ values | Built as seams with safe defaults; calibrated/ratified by the owner (SCOPE-19). |
| Qwen LLM fine-tuning; real-time prediction API / web UI | Deferred until the PINN pipeline is proven; research project, not a product. |

## Traceability

Filled by roadmap creation (`.planning/ROADMAP.md`). Every v2.0 requirement maps to exactly one phase, continuing numbering from v1.6's Phase 36 (no reset). Phases run in dependency order 37 → 43.

| Requirement | Phase | Status |
|-------------|-------|--------|
| ENV-01 | Phase 37 | Complete |
| ENV-02 | Phase 37 | Complete |
| ENV-03 | Phase 37 | Complete |
| ENV-04 | Phase 37 | Complete |
| NET-01 | Phase 38 | Pending |
| NET-02 | Phase 38 | Pending |
| NET-03 | Phase 38 | Pending |
| NET-04 | Phase 38 | Pending |
| NET-05 | Phase 38 | Pending |
| DATA-01 | Phase 39 | Complete |
| DATA-02 | Phase 39 | Complete |
| DATA-03 | Phase 39 | Complete |
| DATA-04 | Phase 39 | Complete |
| DATA-05 | Phase 39 | Complete |
| DATA-06 | Phase 39 | Complete |
| TRAIN-01 | Phase 40 | Complete |
| TRAIN-02 | Phase 40 | Complete |
| TRAIN-03 | Phase 40 | Complete |
| TRAIN-04 | Phase 40 | Complete |
| TRAIN-05 | Phase 40 | Complete |
| TRAIN-06 | Phase 40 | Complete |
| TRAIN-07 | Phase 40 | Complete |
| CTRL-01 | Phase 41 | Complete |
| CTRL-02 | Phase 41 | Complete |
| CTRL-03 | Phase 41 | Complete |
| CTRL-04 | Phase 41 | Complete |
| CTRL-05 | Phase 41 | Complete |
| CTRL-06 | Phase 41 | Complete |
| CTRL-07 | Phase 41 | Complete |
| CTRL-08 | Phase 41 | Complete |
| OPS-01 | Phase 42 | Complete |
| OPS-02 | Phase 42 | Complete |
| OPS-03 | Phase 42 | Complete |
| OPS-04 | Phase 42 | Complete |
| OPS-05 | Phase 42 | Complete |
| OPS-06 | Phase 42 | Complete |
| ACC-01 | Phase 43 | Complete |
| ACC-02 | Phase 43 | Pending |
| ACC-03 | Phase 43 | Complete |
| ACC-04 | Phase 43 | Pending |
| ACC-05 | Phase 43 | Pending |
| ACC-06 | Phase 43 | Pending |

**Coverage:**

- v2.0 requirements: 42 total (4 ENV + 5 NET + 6 DATA + 7 TRAIN + 8 CTRL + 6 OPS + 6 ACC)
- Mapped to phases: **42/42** (Phase 37: 4 ENV; Phase 38: 5 NET; Phase 39: 6 DATA; Phase 40: 7 TRAIN; Phase 41: 8 CTRL; Phase 42: 6 OPS; Phase 43: 6 ACC). No orphans; no duplicates.
- Cross-project requirements: REQ-DOC-01 (not counted in the v2.0 total).
- SCOPE-16 through SCOPE-21 are scope-boundary annotations, not numbered requirements.

---
*Requirements defined: 2026-07-06 (v2.0 milestone initialization, `/gsd-new-milestone`). Traceability table filled by roadmap creation (`.planning/ROADMAP.md`, Phases 37–43): 42/42 mapped, continuing numbering from v1.6's Phase 36. Grounded in the owner-ratified trainex-r1a decision set (2026-07-05) and the locked v1.4/v1.5/v1.6 framework specs.*

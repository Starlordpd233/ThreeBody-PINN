# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- ✅ **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (shipped 2026-07-02; 32/32 requirements, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED; FUT-01/FUT-04 routed to the trainex track; archived under [`milestones/v1.6-*`](milestones/))
- 🚧 **v2.0 CTL-PINN Training Viability Slice** — Phases 37–43 (started 2026-07-06; the project's first **build** milestone / trainex track — a Stage-0-first end-to-end training slice implementing the ratified trainex-r1a decisions; 42 requirements across ENV/NET/DATA/TRAIN/CTRL/OPS/ACC; executes FUT-01 + the Stage-0 scope of FUT-04)
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

---

## 🚧 v2.0 CTL-PINN Training Viability Slice (Executing)

**Milestone Goal:** Build and run the first end-to-end CTL-PINN training **viability slice** on the single M5 Pro Mac — a thin, Stage-0-first walking skeleton (developer environment → PINN model rebuilt from specs → in-memory data ingestion → curriculum training loop → checkpointing/guards → operator runbook → verification + gate check) implementing the ratified trainex-r1a engineering decisions — to prove the ratified pipeline actually trains a model against the locked framework specs, before committing to the full multi-stage platform. This is the project's first **build** milestone: the 1.x series (v1.4–v1.6) settled the framework specs; v2.0 begins the trainex (training-execution) track by executing FUT-01 (`pinn/` rebuild) and the Stage-0 scope of FUT-04 (training-loop implementation).

**Granularity:** standard
**Coverage:** 42/42 v2.0 requirements mapped (Phases 37–43, 1:1 by category: ENV=4, NET=5, DATA=6, TRAIN=7, CTRL=8, OPS=6, ACC=6)
**Branch:** planning artifacts on `master` (governance/planning/CI line, per repo policy); build execution in the existing `.worktrees/trainex` worktree, whose branch should be aligned to `milestone/v2.0` at first phase execution (currently the stale `milestone/v1.7`, an anticipatory name from the v1.6 close — no unique commits, == master tip `9cff97e0`). Tag a pre-phase recovery point before each phase; one atomic commit per plan via `scripts/agent-commit`; no protected-branch push.

### Build discipline & grounding (applies to every phase)

- **Two authoritative grounding sources — no candidate verdict source.** Unlike the v1.4–v1.6 adjudication milestones, v2.0 has no source to critically transcribe; the decisions are made. (1) The **ratified trainex-r1a decision set** (`framework-specs/trainex-r1/decision-adjudication/{trainex-r1a-resolution-doc.md, RATIFICATION.md}`, owner-ratified 2026-07-05: D1–D7 / B-1–B-11 + the §5 first-run recipe) is authoritative for build-engineering; (2) the **locked framework specs** (`ctl_instruction.md` / `pinn_architecture.md`) are authoritative for the science the build implements.
- **The `pinn/` live-code ban is lifted.** The 2026-05-19 directive kept v1.3-era code out of spec *adjudication*; that work is done. FUT-01 rebuilds `pinn/` **from** the specs; the v1.3-era `basic_architecture.py` / `data-processing-pipeline-full.py` are reference-only and replaced. v2.0 is the first milestone to write production `pinn/` code. Spec files are **read-only inputs** — a build-discovered spec defect is surfaced as a gap and routed to a spec milestone, not fixed here.
- **Owner-carved decisions are built as seams, not invented** (the build analog of the STOP protocol). Five decisions the ratification defers are implemented as seams with safe placeholder defaults; the agent surfaces the calibration evidence and the owner ratifies at the designed moment: **D1-p** precision (fp32-MPS vs fp64-CPU) → the §10.3 dual-arm probe (first build act); **D4-a** wall-clock checkpoint ceiling → post-smoke-test; **D4-c/R-2** RECOVER retry budget + HALT/REVIEW thresholds and **R-1** guard thresholds → post-Stage-0-pilot (seam default `recover.retries: 0` ≡ stop-and-preserve); **B-5** resume-field list → before run #1 (unclassified fields default to identity/refuse).
- **Scope is the viability slice.** Stage-0-first, single M5 Pro (hard constraint — no cloud/distributed), in-memory data, manual rollback. "Thin" means Stage-0 only — NOT thin on the model, loop, or verification. The full multi-stage curriculum, streaming residency, auto-revert, stochastic-L-BFGS stages, RAD collocation, and Tier-3 remediation are deferred to Future (PLAT-01..07) pending the Phase 43 (ACC-06) go/adjust/rethink verdict.

### Verification protocol (applies to every phase)

- **Numerically-defined acceptance per requirement.** Each phase's requirements carry a concrete pass criterion (a probe, a gradcheck tolerance, a byte/count check, an observed loss behavior) — not prose.
- **The pre-flight ladder gates real runs.** No training run longer than the ~5-minute smoke test proceeds until the `verify` ladder (device sanity → §10.3 AD probe → fp64-CPU gradcheck → residual-on-ground-truth → single-trajectory overfit) is green (ACC-01).
- **The gate check is the honest answer.** Health of a loss curve or validation is necessary, not sufficient; the binary post-v1.3 gate (`ε_H > 1e-5` reject / `SCS > −5`) on the held-out test set is the acceptance criterion (ACC-03).
- **Owner-carved thresholds are calibrated, not guessed.** The Stage-0 pilot's observed variance calibrates the ⚖ guard / RECOVER thresholds for owner ratification (ACC-05); until then the seams hold safe defaults.

## Phases

**Phase Numbering:**

- Integer phases (37, 38, …): planned v2.0 work, continuing from v1.6's Phase 36. Numbering does **not** reset.
- Decimal phases (e.g., 40.1): reserved for inserted checkpoints or urgent insertions (marked INSERTED), placed between their surrounding integers.

- [x] **Phase 37: Developer Environment & Precision Adjudication** — One-command M5 Pro setup (`pinn-train` env, PyTorch 2.12 + MPS, utility packages, environment fingerprint) and the `pinn_architecture.md` §10.3 componentwise-AD dual-arm probe (fp32-MPS vs fp64-CPU) run as the first build act to give the owner the D1-p precision evidence. First v2.0 phase; ungated. (ENV-01..04) (completed 2026-07-13)
- [ ] **Phase 38: PINN Model Rebuild from Specs (FUT-01)** — Rebuild `pinn/` from the authoritative specs: the SQR-SkipResNet-SIREN network (14→256×12→9), the mass-weighted COM projection head, autograd physics residuals (PHYS-02), and the five-term Huber loss catalog (data + IC + causal physics + soft-energy + angular-momentum) — proven by gradcheck, residual-on-ground-truth, and a single-trajectory overfit. (NET-01..05) — *plans 01–06 complete 2026-07-13; phase-close held on GAP-38-01 (real-trajectory evidence DEFERRED)*
- [x] **Phase 39: Data Ingestion & Stage-0 Population Scan** — The D3-C in-memory fp32 admitted-set adapter (Step-1A gate, NaN/Inf filter, `data_version_hash` refuse, `n_snapshots`/`dt_out` metadata, stage-stratified split), the replay/lookahead two-point-set batch constructor (LOOP-01/02/03), and the Thrust-A scan that counts Stage-0 population. (DATA-01..06) — *completed 2026-07-16; gap-closure plans 39-11..39-14 closed the evidence-integrity gap (row 39-07-02), regenerated real-corpus evidence, and reconciled the validation ledger. 27/27 UAT tests pass; 39-UAT status complete; 39-VALIDATION.md all-green through row 39-14-02.*
- [x] **Phase 40: Stage-0 Curriculum Training Loop (FUT-04)** — `CurriculumController`/`RunController` running the two-phase Adam→L-BFGS closure loop with the PHYS-05 scheduled-weight module, the collocation sampler interface, merged gradient clipping (LOOP-04), and the ADVANCE/RECOVER/HALT stage-exit machine (CURR-03) with a preflight refusal of the unimplemented sL-BFGS stages. (TRAIN-01..07) (completed 2026-07-17)
- [ ] **Phase 41: Config, Checkpointing, Resume & Determinism** — A single keyed YAML with a frozen resolved copy (B-9), dual-trigger + atomic checkpointing with rolling/best/anchor retention (D4-a/b), idempotent promotion + `curriculum.jsonl` (D7-d), manual `--hold-stage` rollback + fail-safe resume config-diff (D7-c/B-5), Tier-1+2 guards + RECOVER + HALT/REVIEW + `failure/` bundle (D4-c/d), and full seed/RNG recording scoped to statistical-equivalence reproducibility (D6/B-11). (CTRL-01..08)
- [ ] **Phase 42: Operator Runbook Surface & Monitoring** — The five entry points (Setup/Configure/Launch/Monitor/Resume), the `caffeinate -is` unattended-run wrapper (B-10), canonical JSONL + TensorBoard logging with the widened field set (D2/B-2), the `runs/<name>/` directory contract, and a written runbook under `docs/runbooks/`. (OPS-01..06)
- [ ] **Phase 43: Verification, Stage-0 Pilot & Acceptance** — The `verify` pre-flight ladder + ~5-minute smoke test (records s/step), the `evaluate` script rendering the binary post-v1.3 gate (`ε_H > 1e-5` / `SCS > −5`), the run-comparison `summary.md`, the 2–3-seed Stage-0 pilot (seed band + ⚖ threshold calibration for owner ratification), and the go / adjust / rethink verdict on the full platform. (ACC-01..06)

## Phase Details

### Phase 37: Developer Environment & Precision Adjudication

**Goal**: A fresh M5 Pro Mac goes from no-Python to a verified `pinn-train` environment in one command, and the D1-p precision decision has its evidence — the `pinn_architecture.md` §10.3 componentwise-AD dual-arm probe — recorded for owner adjudication as the first build act. Every later phase runs on this substrate and under the precision switch this phase establishes.
**Depends on**: Nothing (first v2.0 phase; runs in `.worktrees/trainex`). No external gate.
**Requirements**: ENV-01, ENV-02, ENV-03, ENV-04
**Success Criteria** (what must be TRUE):

  1. A one-command setup (`setup.sh` / Makefile target) on a fresh Mac produces an activated `pinn-train` env (Miniforge3 arm64, Python 3.11, PyTorch 2.12 + MPS, numpy/h5py/pyyaml/tensorboard) idempotently, and `torch.backends.mps.is_available()` returns True (ENV-01).
  2. Setup writes an environment fingerprint (`sw_vers`, `python -V`, framework version/build, lockfile hash) and a reproducible `environment.yml` + pinned lockfile pair (ENV-02).
  3. The §10.3 componentwise-AD probe runs both arms — fp32 on `mps` with `PYTORCH_ENABLE_MPS_FALLBACK` **unset**, and fp64 on `cpu` — times both AD patterns (full-Jacobian vs scalar-`u` forward-mode), and writes a recorded result the owner reads to adjudicate D1-p; the agent records evidence and does not choose fp32/fp64 (ENV-03).
  4. Precision is a single config switch (`precision: float32|float64`, `device: mps|cpu`) such that the fp32-MPS and fp64-CPU branches run the same code path, the fp64-CPU arm being the in-framework escape (ENV-04).

**UI hint**: no

### Phase 38: PINN Model Rebuild from Specs (FUT-01)

**Goal**: `pinn/` carries a spec-faithful model — the SQR-SkipResNet-SIREN network with the mass-weighted COM head and autograd physics residuals — rebuilt from `ctl_instruction.md` / `pinn_architecture.md` (not the v1.3-era code), and proven correct by the AD / gradcheck / overfit rungs before it feeds any training run.
**Depends on**: Phase 37 (environment, the precision switch, and the §10.3 AD contract). Consumes the locked framework specs as read-only inputs.
**Requirements**: NET-01, NET-02, NET-03, NET-04, NET-05
**Success Criteria** (what must be TRUE):

  1. The rebuilt network matches the locked architecture (14-dim `[τ, IC₁₃]` → 12×256 hidden → 9-dim output, SIREN `first_omega_0=30.0`/`hidden_omega_0=1.0`, skip + LayerNorm `elementwise_affine=False` on odd layers) and is instantiated from a config-supplied architecture spec (NET-01).
  2. The hard mass-weighted COM projection head is applied to the 9-dim output before any loss or metric (NET-02).
  3. Autograd physics residuals honor the PHYS-02 AD chain-rule factors and pass an fp64-CPU `gradcheck` and a residual-on-ground-truth probe (NET-03).
  4. The five-term loss catalog (data Huber `δ_r = 1` + IC squared-error + causal physics + soft-energy Huber `δ = 1.0` + componentwise angular-momentum Huber `δ = 1.0`, under the PHYS-05 scheduled weights) evaluates in the shared dimensionless system (`t_τ ∈ [-1,1]`, `r' = r/D`, raw-mass `D ≈ 4.6416`) matching the locked spec loss contracts (NET-04).
  5. A single-trajectory overfit probe drives the data loss to near-zero, confirming model + AD + loss are wired end-to-end (NET-05).

**UI hint**: no

### Phase 39: Data Ingestion & Stage-0 Population Scan

**Goal**: The trainer serves fixed-shape Stage-0 mini-batches from an in-memory, admitted-set adapter, and the Thrust-A scan confirms Stage 0 is populated enough to train — with the on-disk format hidden behind a single adapter seam.
**Depends on**: Phase 37 (environment); consumes the on-disk `simulation_data/` admitted set. Independent of Phase 38 (may proceed in parallel; sequenced after for a clean build order).
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06
**Success Criteria** (what must be TRUE):

  1. The adapter preloads the admitted set fully in-memory as fp32 (`num_workers=0`), exposes `n_snapshots(traj)`/`dt_out(traj)`, is the only component importing the disk format, and reports a `mem:` line against the 0.7 watermark (DATA-01).
  2. The full Step-1A admission gate (clauses 1–7, incl. the conservation reject gate `eps_H ≤ 1e-5` and the fail-closed blacklist) and NaN/Inf filter run at load with logged admitted/rejected/quarantined/dropped counts, and a `data_version_hash` mismatch is a hard refusal, never a silent proceed (DATA-02, DATA-03).
  3. A deterministic, stage-stratified split manifest (~80/10/10) is written to the run folder, grouped by `physical_key = (variant, id)` with an assertion that no `physical_key` spans splits; train shuffles per-epoch under a seeded RNG while val/test iterate in fixed order (DATA-04).
  4. The replay/lookahead batch constructor selects 240 replay + 16 lookahead trajectories (= 256, `has_stage(k+1)` guard) and emits the two independent point sets — data-fidelity points from their snapshots at `n_pts = min(32, n_snapshots)` (~8,192 pts, provisional) vs collocation points sampled continuously from `[0, T]` (~4,096 pts, provisional) — with 50/50 uniform + acceleration-weighted time sampling on the data-fidelity set only, per LOOP-01/02/03 (DATA-05).
  5. The Thrust-A scan bins admitted trajectories by the difficulty invariants, reports per-stage populations (Stage 0 explicitly) plus the admitted-set `s_min` distribution for the owner's ratification of the repaired Stage-0/1 threshold `s₀` (interim floor 0.01), and flags an under-populated Stage 0 as a fatal-class risk (DATA-06).

**UI hint**: no

### Phase 40: Stage-0 Curriculum Training Loop (FUT-04)

**Goal**: The trainer runs Stage 0 end-to-end — the two-phase Adam→L-BFGS closure loop with PHYS-05 scheduled weights, the collocation sampler, merged gradient clipping, and the ADVANCE/RECOVER/HALT stage-exit machine — implementing the `ctl_instruction.md` Stage-0 contract without re-deciding it.
**Depends on**: Phase 38 (the model + loss) and Phase 39 (the batches).
**Requirements**: TRAIN-01, TRAIN-02, TRAIN-03, TRAIN-04, TRAIN-05, TRAIN-06, TRAIN-07
**Success Criteria** (what must be TRUE):

  1. `CurriculumController`/`RunController` drive an outer curriculum + inner optimization loop that trains Stage 0 from the batches (TRAIN-01), running the two-phase Adam→L-BFGS closure (accumulate-in-closure; frozen-λ and no clipping during L-BFGS) (TRAIN-02).
  2. The PHYS-05 scheduled-weight module applies warmup + per-stage `λ^max` (`λ_E^max ≤ 1`), frozen during L-BFGS and re-warmed at boundaries, with state serialized into checkpoints (TRAIN-03); the collocation sampler interface (uniform + adaptive `(model, last_residuals)` hook) supplies physics-loss points (TRAIN-04).
  3. Merged gradient clipping applies `clip_value = C_stage · median(grad_norm_history)` with the per-stage C-table and rolling window, and none during L-BFGS (TRAIN-05).
  4. The stage-exit machine routes ADVANCE (plateau + validation stability + `ε_phys`/`ε_energy`) / RECOVER (NaN/Inf, default `recover.retries: 0`) / HALT-REVIEW (max-epoch/stagnation) with no fallback advancement; thresholds are safe placeholders pending Stage-0-pilot calibration (TRAIN-06).
  5. A preflight refuses the stochastic-L-BFGS stages (3–6) with a typed stop until a concrete implementation exists (TRAIN-07).

**UI hint**: no

### Phase 41: Config, Checkpointing, Resume & Determinism

**Goal**: Every run is driven by one frozen keyed config, survives interruption and corruption, resumes and rolls back correctly, and records enough seed/RNG state to reproduce to statistical equivalence — with guards that stop-and-preserve on trouble.
**Depends on**: Phase 40 (the loop the config / checkpoint / guard layer wraps).
**Requirements**: CTRL-01, CTRL-02, CTRL-03, CTRL-04, CTRL-05, CTRL-06, CTRL-07, CTRL-08
**Plans**: 3/5 plans executed

- [x] 41-01-PLAN.md
- [x] 41-02-PLAN.md
- [x] 41-03-PLAN.md
- [ ] 41-04-PLAN.md
- [ ] 41-05-PLAN.md

**Success Criteria** (what must be TRUE):

  1. A single keyed YAML (`run/stage/opt/loss`) drives the run and its fully-resolved copy is frozen into the run folder (CTRL-01); `--resume` continues exactly, `--hold-stage` rolls back, and the field-classified resume-diff refuses on any unclassified/identity-field change (fail-safe; the field list owner-ratified before run #1) (CTRL-05).
  2. Checkpoints write on the dual trigger (steps or wall-clock ceiling) with rolling-3 + best + latest + stage-anchor retention (CTRL-02), atomically (tmp+fsync+rename, `weights_only`-clean, fallback scan) (CTRL-03), with dual stage anchors + idempotent ordered promotion + a `curriculum.jsonl` recording every promotion/RECOVER/HALT disposition (CTRL-04), and a complete Adam reset at each boundary (CTRL-06).
  3. Auto-guards Tier 1+2 + the RECOVER seam + HALT/REVIEW are active with ⚖ placeholder thresholds and an always-on `failure/` bundle (+one-line README) on any trip (CTRL-07).
  4. Full seed/RNG state is recorded in config + every checkpoint; reproducibility is statistical-equivalence + exact checkpoint continuation (not bitwise), with a strict-CPU determinism debug switch (CTRL-08).

**UI hint**: no

### Phase 42: Operator Runbook Surface & Monitoring

**Goal**: A non-expert operator can run, watch, and hand over a training run through five single-command entry points, an unattended-safe launch, canonical logging, and a written runbook — with the `runs/<name>/` directory as the reproducibility contract.
**Depends on**: Phases 40–41 (a runnable, checkpointing loop to wrap).
**Requirements**: OPS-01, OPS-02, OPS-03, OPS-04, OPS-05, OPS-06
**Success Criteria** (what must be TRUE):

  1. The five entry points (Setup/Configure/Launch/Monitor/Resume) each run as a single command; unattended runs launch under `caffeinate -is <cmd>` (lid-open + AC rule), with SIGTERM treated as one graceful Ctrl-C → checkpoint (OPS-01, OPS-02).
  2. Every logged step writes the widened field set (5 loss terms + total + λ vector + grad-norm + `w_n` stats + lr + s/step + ETA) to a canonical JSONL log with a TensorBoard secondary view in `runs/<name>/tb/`; a `status.json` heartbeat, `mem:` line, and per-time-bin residual panel make health observable (OPS-03, OPS-04).
  3. Each run produces the `runs/<name>/` contract (frozen `config.yaml`, `checkpoints/`, `logs/`, `summary.md`, `status.json`, `failure/`) that reproduces the result when the directory is handed over (OPS-05).
  4. A written runbook under `docs/runbooks/` covers the mental model, the five entry points, the categorized error surface, and the M5-Pro-specific notes (unified memory, thermal, sleep, single-MPS-device) (OPS-06).

**UI hint**: no

### Phase 43: Verification, Stage-0 Pilot & Acceptance

**Goal**: The slice is proven: the verify ladder + smoke test gate real runs, the `evaluate` script renders the binary acceptance gate, the Stage-0 pilot calibrates the owner-carved thresholds, and the milestone closes with a go / adjust / rethink verdict on whether to build the full multi-stage platform.
**Depends on**: Phases 37–42 (the whole slice).
**Requirements**: ACC-01, ACC-02, ACC-03, ACC-04, ACC-05, ACC-06
**Success Criteria** (what must be TRUE):

  1. The `verify` pre-flight ladder (device sanity → §10.3 AD probe → fp64-CPU gradcheck → residual-on-ground-truth + remaining §10 probes → single-trajectory overfit) gates any run longer than the smoke test, and the ~5-minute smoke test (≈32 Stage-0 trajectories, ~300 steps) records the measured s/step (ACC-01, ACC-02).
  2. A separate `evaluate` script runs the held-out test set once and renders the binary post-v1.3 gate (`ε_H > 1e-5` reject; `SCS > −5`) with plain-English metric descriptions in `metrics.md` (ACC-03); the end-of-run `summary.md` reports final losses, a validation summary, curriculum progression, a test-set preview, a run-to-run comparison hint, and the honesty layer (ACC-04).
  3. The Stage-0 pilot repeats the short run 2–3× across seeds, records the seed-band spread in `summary.md`, and calibrates the ⚖ guard / RECOVER thresholds from the observed variance for owner ratification (ACC-05).
  4. The milestone closes with a recorded **go / adjust / rethink** verdict on whether the Stage-0 slice justifies the full multi-stage platform, and updates the FUT-01 / FUT-04 handoff with what shipped, what stayed a placeholder seam, and what was deferred (ACC-06).

**UI hint**: no

## Progress

**Execution Order:** 37 (env + D1-p probe) → 38 (model rebuild) → 39 (data ingestion + Stage-0 scan) → 40 (Stage-0 training loop) → 41 (config/checkpoint/guards) → 42 (operator surface) → 43 (verify + pilot + verdict). Dependency-ordered; 38 and 39 may overlap; **no external research gate** (the trainex-r1a research is delivered and ratified).

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 37. Developer Environment & Precision Adjudication | v2.0 | 5/5 | Complete    | 2026-07-13 |
| 38. PINN Model Rebuild from Specs (FUT-01) | v2.0 | 4/6 | In Progress|  |
| 39. Data Ingestion & Stage-0 Population Scan | v2.0 | 14/14 | In Progress|  |
| 40. Stage-0 Curriculum Training Loop (FUT-04) | v2.0 | 9/9 | Complete    | 2026-07-17 |
| 41. Config, Checkpointing, Resume & Determinism | v2.0 | 3/5 | In Progress|  |
| 42. Operator Runbook Surface & Monitoring | v2.0 | — | Not started | — |
| 43. Verification, Stage-0 Pilot & Acceptance | v2.0 | — | Not started | — |

---
*Created 2026-07-06 (`/gsd-new-milestone`, roadmap generated inline — no external research spawn, since the trainex-r1a ERW is delivered and ratified). 7 phases (37–43), standard granularity, continuing numbering from v1.6's Phase 36; 42/42 v2.0 requirements mapped 1:1 by category (ENV=4, NET=5, DATA=6, TRAIN=7, CTRL=8, OPS=6, ACC=6). Dependency-ordered with no external gate. Grounded in the owner-ratified trainex-r1a decision set (2026-07-05) and the locked v1.4/v1.5/v1.6 framework specs; `pinn/` live-code ban lifted (FUT-01 rebuilds from specs); five owner-carved decisions built as seams. Full multi-stage platform deferred pending the Phase 43 (ACC-06) go/adjust/rethink verdict.*

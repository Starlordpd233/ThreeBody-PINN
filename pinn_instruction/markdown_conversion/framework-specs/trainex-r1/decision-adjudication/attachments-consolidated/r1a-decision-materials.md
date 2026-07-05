# Consolidated attachment (mechanical bundle) for external research agent
# This file = concatenation of the following original sources (content unchanged):
#   1. attachments/trainex-r1a-options-and-decisions.md
#   2. attachments/chatgpt-pro-resolution.md
# Baseline commit: 4bbd5443 (v1.6 tag per DELIVERY-NOTE)
# Consolidated on: 2026-07-04
# IMPORTANT: Original filenames appear in the BEGIN/END markers below.
#            The RESEARCH-AGENT-PROMPT will instruct you which bundle contains which original.
================================================================================
BEGIN ORIGINAL: trainex-r1a-options-and-decisions.md
================================================================================
---
title: Trainex R1a — Options Menus, Baseline Review, and Decision Sheet
package: trainex-r1a (decisions-and-structure half of the foundational research round)
deliverable_for: RESEARCH-CONTEXT-MASTER.md output contract (items 1–8)
research_date: 2026-06-12
status: ready for project-owner decisions
inputs: RESEARCH-CONTEXT-MASTER.md, 2026-06-10-training-execution-design.md, pinn_architecture.md, ctl_instruction.md (verbatim snapshots; no repository access)
---

# Trainex R1a — Options Menus, Baseline Review, and Decision Sheet

**How to read this document.** Sections D1–D7 are options menus: each lists 2–4 viable options with what you would type, see, and find on disk, then closes with a **suggested default — a suggestion only; every final pick is yours** (fill in the Decision Sheet, §10). §8 reviews the baseline design itself and proposes changes as explicit option-vs-baseline comparisons. §9 explains the one-way/two-way door labels. §11 composes all suggested defaults into one first-run picture and flags conflicts. §12 lists what the runbook inherits. §13 is the claims-and-uncertainty register — anything not verifiable from the four attached files or from primary sources is listed there as *open*, not asserted. All external capability claims were re-verified against primary sources on **2026-06-12**; citations [S1]–[S20] are listed in §14 with what each was used for.

**Hard constraints honored throughout** (never traded against): single MacBook Pro M5 Pro (16 CPU cores, 15 GPU cores, 24 GB unified memory, macOS 15+, arm64); non-expert maintainer/operator; physics residuals via autodifferentiation per `pinn_architecture.md`'s AD contract; curriculum state machine per `ctl_instruction.md` with checkpoint/resume surviving stage boundaries; multi-hour unattended laptop runs; no cloud, no distributed training; framework-spec authority over the science; quality-gate metrics and thresholds locked (consumed, never defined here); training precision pending adjudication (handled via the D1 conditional).

---

## 0. Verified capability baseline (read this once; the menus lean on it)

Every load-bearing external claim below was checked on **2026-06-12** against official docs, release pages, or upstream issue trackers — not blogs. Each menu cites back into this table instead of repeating evidence.

| # | Finding (as of 2026-06-12) | Source |
|---|---|---|
| F1 | Current stable **PyTorch is 2.12.0** (PyPI release 2026-05-13; GitHub release ~2026-05-11). Requires Python ≥ 3.10. The design doc's `docs/2.12` citations match current stable. | [S1][S2] |
| F2 | PyTorch **MPS requires macOS 14.0+** (runtime error string in current builds); always satisfied on an M5 Pro. A March 2026 issue shows MPS *availability detection* can break on brand-new macOS majors — an example of the MPS failure surface. | [S3] |
| F3 | **MPS has no float64.** Attempting it raises `TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.` Root cause is the platform: Apple GPUs / Metal / the MPS framework have **no FP64 at all**, confirmed by Apple's MPSDataType docs and Apple DTS staff (2025). MPS supports float32, float16, and bfloat16 (bf16 needs macOS 14+). **No framework can give you float64 on this machine's GPU.** | [S4][S5][S6] |
| F4 | Unimplemented MPS ops raise `NotImplementedError` unless `PYTORCH_ENABLE_MPS_FALLBACK=1` is set, which silently runs those ops on CPU with a one-time `UserWarning`. Op-coverage gaps are tracked in pytorch/pytorch#77764. | [S6][S7] |
| F5 | `torch.mps` (stable docs + source, 2.10–2.12) provides: `manual_seed`, `get_rng_state`/`set_rng_state`, `empty_cache`, `synchronize`, `current_allocated_memory`, `driver_allocated_memory`, `recommended_max_memory`, `set_per_process_memory_fraction(0–2 × recommendedMaxWorkingSetSize)`, and `torch.mps.profiler`. MPS has no user-controllable streams. | [S8] |
| F6 | **PyTorch reproducibility doctrine** (official note, current docs): "Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms… results may not be reproducible between CPU and GPU executions, even when using identical seeds." Deterministic algorithms, where available, are slower. | [S9] |
| F7 | **MPS-specific determinism is weaker still**: an open, triaged issue (#97236) documents *non-identical training results on MPS across runs despite full seeding and `torch.use_deterministic_algorithms(True)`*, while the identical script is bit-reproducible on CPU. Separately (#122394), enabling `use_deterministic_algorithms(True)` on MPS produced a ~7× forward-pass slowdown (M1 Max, macOS 14.4). `warn_only=True` exists to log instead of erroring on ops with no deterministic implementation. | [S10][S11] |
| F8 | Since PyTorch 2.6, **`torch.load` defaults to `weights_only=True`**. Checkpoints that pickle non-allowlisted objects (e.g., an optimizer *instance*, `numpy` scalars/objects) fail with `UnpicklingError: … GLOBAL <X> was not an allowed global by default`; the documented remedies are `torch.serialization.add_safe_globals([...])` or `weights_only=False` (a security trade). Checkpoints containing only `state_dict()`s, tensors, and plain Python scalars load cleanly. | [S12] |
| F9 | Current **MLX is 0.31.2** (PyPI, 2026-04-22; Apple-attested release builds; Python ≥ 3.10; macOS-arm64 wheels tagged macOS 14+; CUDA wheels now also published — active investment). | [S13] |
| F10 | MLX data-types doc (0.31.x): "Arrays with type float64 **only work with CPU** operations. Using float64 arrays on the GPU **will result in an exception**." Default float is float32. | [S14] |
| F11 | `mlx.optimizers` (0.31.x) ships SGD, RMSprop, Adagrad, AdaDelta, Adam, AdamW, Adamax, Lion, Muon, MultiOptimizer, plus schedulers (`cosine_decay`, `exponential_decay`, `linear_schedule`, `step_decay`, `join_schedules`). **There is no L-BFGS.** Optimizer state save/load is documented via `tree_flatten` + `mx.save_safetensors`. | [S15] |
| F12 | **jax-metal is experimental and effectively stalled**: Apple's own page lists it as experimental with **unsupported dtypes including float64** (also complex64/128); a Dec-2025 upstream issue shows it failing outright with recent JAX/macOS; a Jan-2026 JAX discussion describes it as "no longer maintained" and points to a third-party alpha replacement (`jax-mps` 0.10.3, 2026-06-04, pinned to jaxlib 0.9.0, single-maintainer, Development Status 3-Alpha). JAX **on CPU** (arm64) is fine and supports float64 via `jax.config.update("jax_enable_x64", True)`. | [S16][S17] |
| F13 | **Optax provides `optax.lbfgs`** (with zoom line search) in current stable docs — the JAX path has a maintained L-BFGS. | [S18] |
| F14 | **W&B offline mode**: `WANDB_MODE=offline` stores runs locally under `./wandb/offline-run-*`; **viewing the dashboard requires `wandb sync` to W&B's servers** (or self-hosting a W&B server). Offline mode is a *capture* mode, not a local dashboard. | [S19] |
| F15 | **MLflow is on the 3.x line** (3.10.x most recent on the releases page); fully local operation supported (`mlflow ui` → http://localhost:5000); since 3.7.0 the default backend store moved from the `./mlruns` file store to a local SQLite DB (`mlflow.db`); the file store is in maintenance mode. Recent releases are heavily LLM-observability oriented. | [S20] |

**Two project-internal facts used repeatedly** (from the attached specs, not external sources): (a) the network is small — 14 → 12×256 SIREN/SkipResNet → 9 with no-affine LayerNorm ⇒ ≈ 0.73 M parameters ≈ 2.9 MB in float32; with Adam moments ≈ 9 MB. Parameters are never the memory problem; **autograd graphs for the second-order physics term are** (D3, D5). (b) `ctl_instruction.md` Phase 2 *mandates* training-loop structure: per-stage two-phase **Adam → L-BFGS** (full-batch L-BFGS stages 0–2, a *stochastic* L-BFGS variant stages 3–6), **complete Adam state reset at each stage start ("Critical")**, per-stage LR ladder `1e-3 × 0.7^k` with cosine annealing, adaptive median gradient clipping with a stage-scheduled multiplier `C` and **no clipping during L-BFGS**, scheduled loss-weight warmups with per-stage `λ^max`, replay + 5 % lookahead batch composition, and four validation-based stage-promotion criteria. These are *science-side* constraints the skeleton must be able to express (D5, D7).

---

## D1. ML framework — the spine

Judged on the master file's five axes, per candidate, against the verified baseline above. The menu is followed by the **precision conditional** required by the output contract.

### Option D1-A — PyTorch 2.12 + MPS backend *(suggested default)*

* **What you type / see / install:** `pip install torch` inside the `pinn-train` conda env (one wheel, MPS built in); `device = "mps"`; on launch the trainer prints `Found device: mps`. Checkpoints are `.pt` files via `torch.save` / `torch.load`. Unsupported-op errors look like F4; the escape hatch is `PYTORCH_ENABLE_MPS_FALLBACK=1` in the launch command or setup script.
* **(1) Precision on the GPU path:** float32 native; float16/bfloat16 available; **float64 hard-errors on MPS (F3) — there is no silent fallback for dtype**, the error is loud and immediate. Float64 works on the CPU device (`device="cpu"`), same code.
* **(2) Higher-order / input-gradient AD:** `torch.autograd.grad(..., create_graph=True)` and `torch.func` (`jacrev`, `jacfwd`, `vmap`) are the exact APIs the architecture spec illustrates (its "Option A/B" listing is PyTorch); the spec's componentwise contract (nine `dr'_i/du` values, second order, never the sum-trick) maps one-to-one. Ergonomic note inside the spec's "equivalent full-Jacobian method" allowance: the derivative is 9 outputs w.r.t. **one scalar** `u`, so forward-mode `torch.func.jacfwd` (one tangent pass) is the cheap direction versus `jacrev` (nine cotangent passes); both are spec-acceptable. **Whether every kernel in this net's double-backward graph has an MPS implementation must be proven on-device, not assumed** — the spec's own §10.3 componentwise-AD probe is the verification instrument; run it with fallback *disabled* first so any gap is visible (F4). Listed in the register (U-9).
* **(3) Maturity / failure surface:** the most-used Apple-Silicon training path; failures are well-typed (F3 dtype error, F4 NotImplementedError, OOM from the MPS allocator with watermark control via F5/`PYTORCH_MPS_HIGH_WATERMARK_RATIO`); enormous searchable issue base — the design's "paste the exact error into a search engine" troubleshooting step actually works here. Known soft spots: occasional regressions on brand-new macOS majors (F2's detection bug), op gaps (F4), and silent *performance* (not correctness) cliffs when fallback bounces tensors to CPU.
* **(4) Checkpoint/resume:** native and complete — `model.state_dict()`, `optimizer.state_dict()` (works for Adam *and* `torch.optim.LBFGS`), `torch.get_rng_state()`, `torch.mps.get_rng_state()` (F5), step/stage ints. One file, one `torch.load`. **Mind F8**: store only state_dicts/tensors/plain scalars so checkpoints load under the `weights_only=True` default (mechanics in D4).
* **(5) Ecosystem trajectory:** quarterly-ish releases (2.11 → 2.12 in ~7 weeks this spring, F1); MPS receives continuous fixes; PINN reference code (including the PhysicsNeMo example the baseline design is patterned on, and the spec's own listings) is overwhelmingly PyTorch. Lowest "ask the internet / ask an assistant for help" friction for a non-expert.
* **Cross-decision:** TensorBoard is first-party (`torch.utils.tensorboard`) → D2-A frictionless. `torch.optim.LBFGS(line_search_fn="strong_wolfe")` exists in-box → D5's two-phase regime is implementable without writing an optimizer (the *stochastic* L-BFGS variant is custom in **every** framework — see D5). DataLoader machinery → D3.

### Option D1-B — MLX 0.31.x

* **What you type / see / install:** `pip install mlx`; arrays live in unified memory with no `.to(device)` ceremony; lazy evaluation means you call `mx.eval(...)` to force compute; checkpoints via `mx.save_safetensors` (+ documented optimizer-state flatten/unflatten, F11).
* **(1) Precision:** float32 default on GPU; **float64 is CPU-only and raises an exception on GPU (F10)** — same hardware wall as MPS, stated even more plainly by the vendor.
* **(2) Higher-order AD:** composable transforms (`mx.grad`, `vjp`/`jvp`, `vmap`) support nested differentiation; the componentwise contract is expressible. But the project's spec listings are PyTorch-shaped; every pattern would be a translation you maintain alone, and the spec's acceptance probes (§10) would need porting before they can certify anything.
* **(3) Maturity / failure surface:** Apple-maintained, fast-moving (0.31.2 on 2026-04-22, F9), excellent unified-memory behavior by design. Smaller community; PINN usage is thin; pre-1.0 API churn is a real maintenance tax for a non-expert who upgrades.
* **(4) Checkpoint/resume:** workable (safetensors + state trees, F11) but more assembly required than `torch.save` — RNG state, step/stage, and optimizer trees are saved as separate keys you wire yourself.
* **(5) Ecosystem trajectory:** strongly positive (Apple investment, now even CUDA wheels, F9) — the best raw bet on *future* Apple-Silicon performance.
* **Structural blocker for this project:** **no L-BFGS (F11)**. `ctl_instruction.md`'s two-phase regime would require hand-implementing L-BFGS with Wolfe line search (and later the stochastic variant) — exactly the kind of numerical-optimizer code a non-expert should not own. Choose MLX only if you consciously accept either (a) writing/borrowing an L-BFGS, or (b) renegotiating the spec's Phase 2b — which the spec's authority over the science does not allow this research to do.
* **Cross-decision:** no first-party TensorBoard writer → D2 needs a third-party writer or the CSV path; D3 is simplest of all (unified memory is the native model).

### Option D1-C — JAX + Optax + Equinox, CPU-first

* **What you type / see / install:** `pip install jax optax equinox`; pure-functional style (`jax.grad`, `jax.jacfwd`, `jax.vmap`, `jax.jit`); float64 available process-wide via `jax.config.update("jax_enable_x64", True)`; `optax.lbfgs` exists with a proper line search (F13). Checkpointing via Orbax or hand-rolled pytree saves.
* **The honest hardware picture:** the Apple-GPU plugin (jax-metal) is experimental, float64-less, and effectively unmaintained/broken with current JAX (F12); the community replacement is alpha. So on this machine, "JAX" realistically means **JAX on the 16 CPU cores** — fast vectorized CPU, no 15-GPU-core utilization on the supported path.
* **AD ergonomics:** best-in-class for the spec's math (`jacfwd` over scalar `u`, nested for second order, `vmap` over trajectories — one-liners).
* **Failure surface / maintainability:** functional purity, tracing rules, and recompilation are the classic non-expert tripwires; error messages assume JAX fluency. For a maintainer who "can read code, follow a runbook" but is not a Python developer, this is the highest-friction option.
* **Cross-decision:** TensorBoard via `tensorboardX`/flax utilities (extra dependency); D3's GPU questions mostly vanish (CPU path); D6 is the *strongest* option here — CPU JAX with fixed seeds is bitwise-stable in practice and x64 is native.

### Suggested default for D1 — **D1-A, PyTorch 2.12 + MPS** *(suggestion; your pick)*

Rationale: it is the only candidate that simultaneously (a) runs on the GPU you bought, (b) ships the L-BFGS the science spec mandates, (c) matches the spec's own illustrative AD code and acceptance probes, and (d) maximizes searchable help for a non-expert. MLX is the strongest *runner-up on hardware fit* and the one to re-evaluate if it ever ships L-BFGS; JAX is the strongest *on math ergonomics and determinism* but only on CPU and at the highest maintainer-skill cost. **Door: one-way** — every other decision area, the runbook, and all run artifacts inherit the framework; reversing later is a rewrite.

### The precision conditional (output-contract item 2)

The project's residual-precision requirement is unadjudicated. The specs pin float64 only for *offline* quantities (data parsing, invariant computation, and the one-time `S_H` constant are float64 by contract); the *training* dtype is the open question. Both branches below assume those offline float64 contracts are honored regardless (they run in NumPy/CPU and are unaffected by this choice).

**Branch (i): float32 on the accelerator suffices for the physics residuals.**
Suggested default **unchanged: D1-A on `device="mps"`, float32 end-to-end in the training loop**, with two float64 islands kept on CPU exactly as the specs already require: preprocessing/invariants, and any *diagnostic* recomputation of `ΔH` you choose to log. The spec's training-time guards (Plummer softening `ε_train = 1e-5`, the `ε_H = 1e-4·S_H` denominator floor, Huber losses, causal-weight underflow clip) are precisely the kind of conditioning that makes fp32 residuals plausible — but "plausible" is not "proven"; the §10 acceptance probes (AD tolerance 1e-6 relative, force–energy 1e-5 relative) are the adjudication instrument and should be run in fp32 on MPS as the first build act. If they fail in fp32, that is the adjudication outcome arriving early.

**Branch (ii): float64 is required for the physics residuals.**
Then **the 15 GPU cores are off the table for the residual path on every candidate — this is hardware (F3, F10, F12), not a framework choice.** No option can honestly satisfy branch (ii) on the GPU; any candidate claiming otherwise would be wrong. The menu becomes a CPU menu:
* **(ii)-1 — PyTorch on CPU, float64** *(suggested default under this branch)*: identical code to D1-A with `device="cpu"`, `torch.set_default_dtype(torch.float64)`; keeps one framework across both branches, one runbook, one checkpoint format; uses the 16 CPU cores via PyTorch's internal threading (`torch.set_num_threads`). Cost: substantially slower steps (quantify on-device; run-duration estimates are the **R1b** feasibility question — dependency noted, not estimated here).
* **(ii)-2 — JAX on CPU with `jax_enable_x64`**: the most natural fp64 numerics and `optax.lbfgs`; pays the D1-C maintainability tax.
* **(ii)-3 — Hybrid**: fp32 training on MPS *plus* a float64 CPU verification pass (residual/energy audit at checkpoints). Note this is **not** branch (ii) compliance — it is branch (i) with stronger auditing; listed so the hybrid isn't mistaken for a way to keep the GPU under a true fp64 requirement.
* **MLX under (ii):** float64 on the GPU raises a **hard MLX exception** (F10) — a platform block, not a soft/partial limitation; on CPU, fp64 runs but its op coverage for this workload (SIREN + double-grad) is unverified (register U-8). **Say-it-plainly clause: MLX cannot honestly satisfy branch (ii).**

Whether the *suggestion changes*: the framework suggestion stays PyTorch in both branches; what changes is the **device** (mps→cpu) and therefore D3's entire utilization story (the "GPU 60–95 %" health check in the baseline design becomes inapplicable) and R1b's duration estimates. **Door: the branch decision is one-way in practice** — fp32-vs-fp64 changes step cost, feasible batch/collocation sizes, and every empirical tuning result R2 would produce on top.

---

## D2. Experiment tracking and the monitoring surface

Frame: the baseline already commits the **primary** monitor (live terminal log) and writes `runs/<name>/logs/train.log.jsonl` — a machine-parseable, tracker-independent record. That JSONL file is the load-bearing design point of this menu: **if the JSONL log remains the source of truth and any dashboard is only a *view* of it, every option below becomes a two-way door.** All options below are evaluated for a single user, single machine, no cloud.

### Option D2-A — TensorBoard *(suggested default)*

* **Monitor entry point:** `pip install tensorboard` at setup; trainer writes scalars via `torch.utils.tensorboard.SummaryWriter(log_dir="runs/<name>/tb")`; user runs `tensorboard --logdir runs/` and opens `http://localhost:6006`. Comparing runs = pointing `--logdir` at the parent `runs/` folder (each run appears as a line on the same plot).
* **Integration with D1:** first-party for PyTorch (A); needs a third-party writer for MLX (B); via tensorboardX for JAX (C).
* **Storage/overhead:** event files are small for scalar-only logging (tens of MB over a long run at the planned cadences); writer cost at one write per `log_freq=100` steps is negligible. Fully offline.
* **Learning curve:** one command, one URL; the baseline design (§5.5) and `ctl_instruction.md`'s own implementation note both already name TensorBoard — least surprise.
* **Lock-in:** low *if* JSONL stays canonical; event files are awkward to re-parse, so never make TB files the only record.

### Option D2-B — CSV/JSONL + small plotting scripts ("none/CSV-plus-scripts")

* **Monitor entry point:** no new dependency; a `python -m pinn.plot runs/<name>` helper renders loss-vs-step PNGs (or an HTML page) from `train.log.jsonl`; "compare" = pass two run names.
* **Strengths:** zero new tools, zero background process, trivially auditable files, perfect fit with the runbook's "the folder is the record" contract.
* **Weaknesses:** no live auto-refresh dashboard (re-run the script or add a `--watch` loop you now own); every chart is code you maintain.
* **Integration:** identical across all D1 candidates (it reads files).

### Option D2-C — MLflow (local)

* **Monitor entry point:** `pip install mlflow`; trainer calls `mlflow.log_metric(...)`; user runs `mlflow ui` → `http://localhost:5000`. Since 3.7.0 the default local backend is a SQLite `mlflow.db` (F15).
* **Strengths:** run table + params + metrics comparison UI; genuinely local.
* **Weaknesses for this project:** a heavier dependency whose 3.x release energy is aimed at LLM observability (F15); introduces a second metadata store (SQLite) beside `runs/<name>/`, splitting the "give the folder" contract; more concepts (experiments, runs, artifacts) than a single-user project needs.
* **Lock-in:** moderate (metadata in its DB) unless JSONL stays canonical.

### Option D2-D — Weights & Biases, offline mode

* **Monitor entry point:** `WANDB_MODE=offline`; runs captured under `./wandb/offline-run-*`.
* **The disqualifying mechanic for a no-cloud project:** offline mode is *capture only* — **viewing the dashboard requires `wandb sync` to W&B's servers or self-hosting a W&B server (F14)**. Either step contradicts the no-cloud hard constraint or adds a server the operator must run. Listed for completeness; not recommended here.

### Suggested default for D2 — **D2-A TensorBoard as the secondary view, with the committed JSONL log as the canonical record; D2-B's one plotting script added for end-of-run PNGs in `summary.md`** *(suggestion; your pick)*

Rationale: matches both the baseline design and the spec's implementation note; lowest learning curve; and the JSONL-canonical rule converts tracker choice into a cheap experiment. **Door: two-way** (explicitly engineered to be, via JSONL-as-source-of-truth; swapping trackers later means changing one writer class and one runbook paragraph). Storage location note for the run contract: keep TB event files *inside* `runs/<name>/tb/` so the "give a colleague the folder" promise includes the dashboard data (this is a small additive change to §5.7 — see baseline finding B-6).

---

## D3. Compute utilization on 24 GB unified memory — including in-memory vs streaming

Everything here assumes D1-A (PyTorch/MPS); deltas for the other candidates are at the end. The two real questions: *where does the dataset live*, and *what actually uses the 16 CPU + 15 GPU cores*.

### 3.1 What the memory actually goes to (parameterized model — fill in the blanks the project must supply)

* **Model + optimizer:** ≈ 9 MB (verified arithmetic from the spec's architecture; §0). Irrelevant to the budget.
* **Dataset.** Per snapshot: 3 bodies × 7 values + time ≈ 22 numbers ⇒ **176 B in float64 / 88 B in float32**. Total resident bytes ≈ `N_traj × S̄ × 176 B` (fp64) where `S̄` = mean snapshots per trajectory. The attached files give `N_traj = 15,028 = 4,857 @ dt_out=0.08 (hierarchical) + 4,857 @ dt_out=0.01 (hierarchical_gold) + 2,749 @ dt_out=0.17 (standard) + 2,565 @ dt_out=0.01 (standard_gold)` **but not the integration horizon, so `S̄` per set is unknown — the single most important number the project must supply** (register U-1). Bracketing: at `S̄ = 1,250`, all 15,028 trajectories ≈ **3.3 GB fp64 / 1.7 GB fp32** — comfortably in-memory; if the two 8×/17×-denser gold sets (dt_out=0.01) run long horizons, `S̄ = 10,000` for those **7,422** trajectories (4,857 hierarchical_gold + 2,565 standard_gold) alone ≈ **13.1 GB fp64 / ~6.5 GB fp32** — genuine pressure on the 24 GB budget (the fp32 figure already sits at D3-A's ~6–8 GB streaming threshold, line 151, before any cumulative-stage replay). Numbers to supply: `S̄` (or `t_max`) per set; which sets/stages the curriculum actually loads (cumulative-per-stage sizes, since replay batching loads stages 0…k); on-disk dataset size as a sanity cross-check.
* **Autograd graphs for the second-order physics term — the true pressure point.** Per spec batch shape (256 trajectories × 32 points = 8,192 data points, plus 2,048–4,096 collocation points), each point's forward through 12×256 layers retains ~12 KB of fp32 activations, and the componentwise second-derivative construction multiplies retained state by the Jacobian strategy's factor (×~2 for `jacfwd∘jacfwd`; up to ×9 on the cotangent side for `jacrev`). Order-of-magnitude: **hundreds of MB to a few GB per step** — fine at spec batch sizes, *measured, not assumed*: log `torch.mps.current_allocated_memory()` each step from day one (F5). **MPS AD hazard (name it now):** through PyTorch 2.7.0, `torch.func.jacfwd` raises `RuntimeError: as_strided_tensorimpl does not work with MPS` for any traced function containing `torch.cat` / `torch.stack` / `torch.vstack` (pytorch/pytorch#152701) — and a SIREN backbone with skip connections is exactly that concat-bearing case, so on MPS prefer a `jacrev`-based second-order path (`jacfwd(jacrev(...))` for the Hessian route) and pin PyTorch ≥ 2.7.1/2.8 where the bug is fixed; the spec's §10.3 componentwise-AD probe (first build act, §11) is the instrument that catches this early.
* **The OS:** the constraint register's own framing — if training takes 20 GB, macOS has 4 GB. Working ceiling for the trainer: **≤ ~16–18 GB**, enforced (below).

### Option D3-A — Full in-memory preload behind the adapter *(suggested default, conditional on the U-1 numbers)*

* **Mechanics:** the thin adapter loads the (curriculum-relevant) split once at startup into contiguous float32 tensors (fp64 parse → fp32 cast at the adapter boundary, honoring the fp64-parse contract), keeps them on CPU/unified memory, and slices batches by index. The user sees the already-committed `Loading dataset… N train trajectories… ETA 30s` line, then zero data-side stalls.
* **Consequences:** `DataLoader` worker processes become unnecessary (`num_workers=0`) — a major simplification and the removal of the most common PyTorch beginner failure class (worker crashes, multiprocessing pickling). CPU cores still serve PyTorch's intra-op threads and the OS.
* **When it's wrong:** if cumulative-stage bytes (fp32) exceed ~6–8 GB, you're spending the autograd headroom on storage — switch to D3-B for those stages.

### Option D3-B — Memory-mapped / chunked streaming behind the same adapter

* **Mechanics:** adapter exposes the identical "give me batch by indices" interface but reads from a memory-mapped on-disk array (format owned elsewhere; the adapter is exactly the seam the baseline created for this). Optionally `num_workers=2–4` to overlap read+collate with GPU compute; on MPS, `pin_memory` is a CUDA concept — leave it off.
* **Trade-offs:** unbounded dataset size; costs steady-state read latency (small for sequential trajectory slices on Apple SSDs) and reintroduces worker-process complexity if you enable workers.

### Option D3-C — Hybrid per-stage policy

* **Mechanics:** a config switch `data.residency: auto|ram|mmap`; `auto` preloads while estimated bytes < threshold (config value), else maps. One extra log line states which mode ran. This is A and B with a selector — the adapter interface is the same.

### Cross-cutting mechanics (apply to whichever option you pick)

* **GPU does the math; CPU feeds it.** With in-memory fp32 tensors, "CPU/GPU co-utilization" on MPS reduces to: batch assembly + logging on CPU, forward/backward on GPU, `torch.mps.synchronize()` only where timing/logging needs truth (F5: MPS has no user streams to tune).
* **Memory-pressure management (what you set, what you see):** at startup call `torch.mps.set_per_process_memory_fraction(0.7)` (≈ 0.7 × `recommendedMaxWorkingSetSize`, F5) so the trainer OOMs *itself* with a catchable error instead of swapping the OS; log `current_allocated_memory` / `recommended_max_memory` each `log_freq`; the user-side check stays the baseline's Activity Monitor rule (GPU % > 0; Swap not growing). The watermark choice (0.7 vs 0.8) is a knob — exact threshold joins R1b's health-watchlist findings at consolidation rather than being invented here.
* **Verification of utilization:** Activity Monitor (committed baseline surface) plus one trainer-printed line per 1,000 steps: `mem: 6.2/16.8 GB (mps)` — so the runbook can say "if the first number climbs every interval, report it."
* **Other candidates:** MLX — unified memory is the native model; lazy eval batches work automatically; same in-memory-vs-mmap question, same parameterization. JAX-CPU — no GPU question; preload into NumPy/JAX arrays; `jit` once.

### Suggested default for D3 — **D3-C's selector with `auto` defaulting to in-memory float32 preload (i.e., D3-A behavior at expected sizes), `num_workers=0`, watermark 0.7, and the memory log line** *(suggestion; your pick)*

**Door: two-way** for residency policy (the adapter interface hides it; flipping a config value changes mode). The *adapter interface itself* ("batches by index, fixed shapes") is mildly one-way — downstream loop code will assume it — but it is the baseline's own committed seam, kept here.

---

## D4. Checkpoint/resume policy, unattended-run auto-guards, failure diagnostics

Baseline intent kept (per the master): checkpoint *contents* (model + optimizer + step + stage + RNG state) and resume *invariants* (same config ⇒ continue; different ⇒ refuse; missing ⇒ error with path). The open menus are **policy** (cadence, retention, corruption safety), **auto-guards**, and the **diagnostic bundle**. Stage-*boundary* checkpoint mechanics live in D7 — cross-referenced, not duplicated.

### 4.1 Cadence and retention

* **Option D4-A — Latest-only, every N steps:** minimal disk; one bad/corrupt save can strand you; rules out "restore last *good* checkpoint," which the baseline's own NaN advice requires. Not recommended alone.
* **Option D4-B — Rolling window + best + stage anchors *(suggested default)*:** every `checkpoint_every` (baseline first-trial 1000 — kept) write `step-XXXXXX.pt`; retain the most recent `K=3`; additionally keep `best.pt` (lowest validation total loss, updated at validation cadence) and the per-stage promotion anchors from D7 (never auto-deleted); maintain `latest.pt` as a copy (not a symlink — copies survive folder hand-offs intact, matching the "give the folder" contract). Disk math at ~9 MB/checkpoint (§0): 3 rolling + best + ≤7 stage anchors + latest ≈ **~110 MB per run** — trivial; budget remains trivial even at 10× cadence.
* **Option D4-C — Periodic archive (every M-th kept forever):** full training-history archaeology; only worth it if you want post-hoc trajectory-of-training studies; disk grows linearly (~9 MB × steps/М).
* **Corruption safety (applies to every option; adopt regardless):** atomic write pattern — serialize to `step-XXXXXX.pt.tmp` in the same directory, `flush` + `os.fsync`, then `os.rename` to the final name, then update `latest.pt`; on resume, if `latest.pt` fails to load, fall back to the newest readable `step-*.pt` and *say so* in the log. A mid-write power loss then costs at most one cadence interval. The mechanical user surface: a `*.pt.tmp` file in `checkpoints/` after a crash is normal debris, documented as such.
* **`weights_only` rule (F8):** checkpoints must contain only `state_dict()`s, tensors, ints/floats/strings — never optimizer *objects*, never raw NumPy RNG tuples (store NumPy RNG state converted to tensors/bytes). Then `torch.load(path)` works under the 2.6+ default with no `add_safe_globals` incantations in the runbook.

### 4.2 Auto-guards for unattended runs (which guards live *inside* the loop)

The baseline's stop rules are all manual (Ctrl-C); the premise is multi-hour unattended runs. Menu by guard *mechanics* — detection, action, what the user finds afterwards. Thresholds marked ⚖ take their values from the companion **R1b** health-watchlist findings at consolidation; they are deliberately not invented here.

* **Tier 0 — none (baseline as written):** operator watches. Rejected premise for unattended runs, listed for completeness.
* **Tier 1 — terminal-failure guards *(suggested minimum)*:**
  * *NaN/Inf auto-stop:* after each loss computation, `if not torch.isfinite(total): ` → save `checkpoints/emergency-nan-step-XXXXXX.pt` (atomic), write the diagnostic bundle (§4.3), print `GUARD: non-finite loss at step X — run stopped; see runs/<name>/failure/`, exit non-zero. (Spec note alignment: `ctl_instruction.md` says monitor NaN during close encounters and respond via the PHYS-03 softening-ablation contract or tighter clipping — the guard *stops and preserves*; the *response* stays the operator's per spec.)
  * *Loss-explosion kill switch:* smoothed total loss > ⚖-multiple of its trailing median for ⚖ consecutive logs → same action path, message `GUARD: loss explosion`.
  * *Disk-floor guard:* before each checkpoint write, `shutil.disk_usage`; below ⚖ GB free → checkpoint once, stop with `GUARD: disk low`.
* **Tier 2 — environment guards *(suggested default = Tier 1 + Tier 2)*:**
  * *Memory-watermark guard:* `torch.mps.current_allocated_memory()` > ⚖ × the D3 cap for ⚖ consecutive logs → checkpoint, stop, `GUARD: memory pressure` (catches leak-shaped growth before macOS swaps).
  * *Heartbeat/hang detection:* trainer touches `runs/<name>/status.json` (step, timestamp) every log line; a hung process can't self-detect, so the *runbook-side* check is "if status.json's timestamp is > 10 min old while the process exists, it's hung" — this guard is a *file the loop maintains* plus a one-line user rule, replacing the baseline's "three identical lines" eyeballing with something checkable after the fact.
* **Tier 3 — auto-*remediation* (auto-LR-cut, auto-rollback-and-retry):** powerful, but turns the trainer into an agent making science-adjacent decisions the spec assigns to operator+spec contracts; also needs R1b's signal definitions first. Offered as a later, off-by-default config block, not for the first build.
* **What the user finds afterwards (all tiers):** the terminal line `GUARD: <reason> — run stopped`, a final checkpoint, `status.json` with `"state": "stopped-by-guard", "reason": ...`, and the bundle below. Every guard is config-toggleable (`guards.nan: true` …) so a watched debugging session can run bare.

### 4.3 On-failure diagnostic bundle (single suggested checklist)

On any guard stop **or** uncaught exception, the trainer writes `runs/<name>/failure/` containing: `traceback.txt`; `env.txt` (`python -V`, `sw_vers`, `uname -m`, `pip freeze`); `config-frozen.yaml` (copy) + its SHA-256; `log-tail.txt` (last 200 lines of `train.log`); `state.json` (step, stage, phase, last checkpoint path, RNG-seed record); `memory.txt` (last `torch.mps.*_memory` readings, disk free); pointer to the dataset `data_version_hash`. Runbook step becomes literally: *"zip `runs/<name>/failure/` and ask for help."* **Door: two-way** (additive files; nothing else depends on them).

### Suggested default for D4 — **B-retention with atomic writes and the weights_only rule; guards Tier 1+2 on by default; the bundle always-on** *(suggestion; your picks — cadence/retention, guard tier, and bundle are separate rows in the sheet)*

**Doors:** cadence/retention/bundle — two-way (config + additive files). The *guard hook points inside the loop* (post-loss check, pre-checkpoint check, heartbeat write) are mildly one-way: build the skeleton with these three seams now even if some guards start disabled, because retrofitting seams into a running loop is where rework lives (D5 interaction).

---

## D5. Training-loop skeleton capabilities — structural slices only (numbers are R2's)

The controlling fact (§0, verified against `ctl_instruction.md` Phase 2): the science spec **mandates** a two-phase per-stage regime — Adam exploration, then L-BFGS refinement (full-batch stages 0–2; a *stochastic* L-BFGS, "batch size 32, curvature interval 10," stages 3–6) — plus scheduled loss weights with per-stage re-warmup, adaptive median clipping with no clipping during L-BFGS, replay+lookahead batch composition, and a plateau-triggered Adam→L-BFGS handoff. R1a's question is only *which of these the skeleton must be shaped to express from day one*.

### 5.1 Optimizer-family structure (loop shape)

* **Option D5-A — Single-phase mini-batch Adam loop only:** the simplest loop (the PhysicsNeMo reference shape the baseline cites). **Conflict warning:** as a *skeleton* this cannot express the spec's Phase 2b; choosing it is a conscious descoping decision against `ctl_instruction.md`, defensible only as a *sequencing* choice (the spec's own author note contemplates "test train stage 0 first"). Retrofit cost when Phase 2b arrives: restructuring the inner loop around closures — exactly the rework R1 exists to avoid.
* **Option D5-B — Two-phase loop with closure support *(suggested default)*:** the inner loop is phase-aware: *Adam phase* = step-per-batch; *L-BFGS phase* = `torch.optim.LBFGS(params, history_size=10, line_search_fn="strong_wolfe", max_iter=20)` driven by a `closure()` that recomputes the loss (PyTorch's L-BFGS calls the closure multiple times per `step()` for the line search — the loop must be written so loss construction is a callable, which is also exactly the seam D4's guards and D7's boundary logic want). "Full-batch" early stages: the closure iterates the whole stage dataset **with gradient accumulation inside the closure** rather than one giant graph — this is the structural answer to the 24 GB wall (a single full-dataset second-order graph would not fit; accumulation keeps peak memory at one-batch scale at the cost of closure wall-time). Frozen λ values during L-BFGS and the no-clip rule are phase flags the loop honors.
* **Option D5-C — Pluggable phase abstraction (list of `Phase` objects per stage):** D5-B generalized; buys easy insertion of future phases (e.g., the spec's optional ALM ablation between Adam epochs) at the cost of one abstraction layer in what's meant to be a plain readable script. Worth it only if you expect to experiment with phase orderings.
* **The stochastic-L-BFGS gap (flagged, not solved here):** **no candidate framework ships the spec's sL-BFGS** — `torch.optim.LBFGS` is a deterministic full-batch-style optimizer (its closure assumes a consistent objective; feeding it changing mini-batches violates its curvature assumptions), MLX has no L-BFGS at all (F11), and `optax.lbfgs` is likewise linesearch-based (F13). The spec's "batch 32, curvature interval 10" describes a research-grade variant that would be **custom code in every framework**. This is a missing item in the baseline's placeholder inventory (B-4) and a register entry (U-7): the skeleton requirement it implies is only "phases are pluggable per stage" (covered by D5-B/C); *implementing* sL-BFGS is deferred work the owner must consciously schedule or renegotiate at the spec level.

### 5.2 Collocation infrastructure (structure, not densities)

What the spec already requires structurally: per-step sampling of `n_col` points in `u∈[0,1]` with at least two strategies — `uniform` and the spec's acceleration-weighted `adaptive` (which needs access to trajectory acceleration metadata) — plus the data-batch side's 50 % uniform / 50 % acceleration-weighted time-point sampling and the replay/lookahead composition.

* **Option D5-D — Fixed uniform sampler hard-coded:** smallest; cannot express the spec's own `adaptive` option without surgery. Under-builds relative to the spec's listing.
* **Option D5-E — Sampler-interface *(suggested default)*:** the loop calls `sampler(stage, step) -> u_col`, with `uniform` and the spec's acceleration-weighted `adaptive` shipped behind a config key (`collocation.strategy`). Structural cost: one function indirection.
* **Option D5-F — E + residual-pool refresh hooks:** adds the machinery for *residual-based* adaptive sampling (periodic residual evaluation over a candidate pool, point-set refresh) now. The spec does not currently call for RAD; D2/R2 literature might. Middle path adopted into E's suggested form: define the sampler interface so a stateful sampler *may* receive `(model, last_residuals)` — the hook signature costs nothing today and is the one-way part; the pool machinery itself is bolt-on later.

### 5.3 Loss-weighting machinery

The fence: terms, forms, and scientific weights are the specs'. The plumbing question is settled *by* the specs: weights are **not static** — `λ_phys`, `λ_E`, `λ_L` warm up linearly over `I_warm = min(2000, 0.1·N_Adam,k)` steps, with per-stage `λ^max` tables, frozen during L-BFGS, **re-warmed at every stage boundary**, plus per-batch causal weights with stopgrad and an underflow clip (bound deliberately unchosen by the spec — register U-6).
* **Option D5-G — Static weights only:** *does not satisfy the spec*; listed only so the sheet shows it was considered and why it's excluded.
* **Option D5-H — Scheduled-weights module *(suggested default)*:** a `WeightSchedule` object: inputs (stage k, phase, step-in-phase) → the λ vector; logs all λ values every `log_freq` (they're part of run health); serialized into checkpoints so resume restores mid-warmup state exactly.
* **Option D5-I — H + adaptive-rebalancing hook:** adds a seam for gradient-statistics-based rebalancing schemes. Not spec-required; the hook (a no-op callable site after backward) is nearly free — include the seam, ship it empty.

### Suggested default for D5 — **B (two-phase, closure-shaped, accumulate-in-closure) + E (sampler interface incl. the stateful-hook signature) + H (scheduled-weights module with the empty I-seam)** *(suggestion; three rows in the sheet)*

R2 then tunes *numbers* (LRs, n_col, cadences, λ ablation ranges) entirely inside this skeleton. **Doors: loop shape, sampler interface signature, and weight-module interface are one-way** (they *are* the skeleton; everything in R2 and the runbook leans on them). Strategy selections and all numeric values inside them are two-way config.

---

## D6. Reproducibility and determinism policy

What is actually available, with citations (per D1 candidate), then the policy menu.

**Verified ground truth.** PyTorch's official position: bitwise reproducibility is not guaranteed across releases, commits, platforms, or CPU↔GPU (F6). On **MPS specifically**, an open issue documents non-identical training across runs *despite* full seeding and `use_deterministic_algorithms(True)` — while the same script is bit-stable on CPU (F7) — and the deterministic-algorithms flag carries a measured ~7× slowdown example on MPS (F7). Seed plumbing that *does* exist and should be used regardless: Python `random`, NumPy, `torch.manual_seed` (all devices), `torch.mps.manual_seed` / `get_rng_state` / `set_rng_state` (F5), plus the config-recorded split seed and per-epoch shuffle seeds the baseline already commits. MLX: `mx.random.seed` exists; no vendor determinism guarantee for GPU kernels located — treat as accepted-variance (register U-10). JAX-CPU: same-version, same-platform seeded runs are bit-stable in practice — the strongest determinism story, on CPU only.

* **Option D6-A — Strict determinism always:** `use_deterministic_algorithms(True)` (+ CPU where MPS can't comply). Costs: large slowdown on MPS (F7) **and** still not guaranteed there (F7's open issue) — you'd pay the price without securing the property. Honest only as CPU-mode.
* **Option D6-B — Accepted-variance with a defined seed policy *(suggested default)*:** every run sets and *records* the full seed set above (config `seed:` field; echoed into `status.json` and checkpoints, RNG states checkpointed for exact-resume continuity); no deterministic-algorithms flag; the policy *names* the residual: two same-seed MPS runs may differ slightly (F6/F7). Comparison protocol the runbook teaches: judge runs on **validation metrics at fixed checkpoints**, and treat differences smaller than the seed-to-seed band as noise — establish the band once by running the short stage-0 pilot 2–3× with different seeds and recording the spread of final validation loss in `summary.md`'s comparison hint. "Better than my last run" then means: outside the band, in the right direction. (This is what makes §6.2's comparison surface *honest* on this hardware.)
* **Option D6-C — B + a strict-mode debug switch:** config `determinism: strict` flips to CPU device + deterministic algorithms + `warn_only=True` logging for bisecting weird behavior on a small problem. Cheap to include; suggested as part of the default.
* **Reproducibility-contract consequence (flags a baseline promise, not a hard constraint):** §5.7's "give a colleague the `runs/` folder ⇒ reproduce" must be re-worded to what the platform supports: *re-run to statistically equivalent results from the recorded config+seed; exact-continuation from any checkpoint; not bitwise re-creation of a from-scratch run* (F6/F7). See B-11 in §8 and §12.

### Suggested default for D6 — **B + C** *(suggestion; your pick)*

**Doors:** the *policy* is two-way (flip a config). The **seed-and-RNG block inside the checkpoint/config schema is one-way-ish** — it's part of the artifact contract every later run compares against; include it from run #1.

---

## D7. Curriculum stage-boundary mechanics

Promotion *rules* are `ctl_instruction.md`'s (four validation criteria — out of scope). The loop *mechanics* at the boundary:

* **Boundary checkpoint guarantee:** **Option D7-A *(suggested default)*** — at every promotion the loop writes **two distinguishable anchors**: `checkpoints/stage-{k}-final.pt` (last pre-promotion state — the rollback target) and `checkpoints/stage-{k+1}-init.pt` (post-transition: weights carried, **fresh optimizer**, re-warmed λ schedule state, advanced stage field). Both excluded from D4's rolling deletion. Spec alignment: `ctl_instruction.md`'s own implementation note says checkpoint at each stage completion; this option makes that checkpoint *distinguishable* and adds the post-init twin so a boundary crash is unambiguous. **Option D7-B** — single cadence checkpoint that happens to fall at the boundary: indistinguishable in archaeology, no clean rollback target; rejected-by-default.
* **Optimizer state at the transition — not open:** the spec *mandates* a complete Adam-state reset at each new stage ("**Critical**: Completely reset Adam's internal state (momentum buffers)…"), which is exactly the documented staged-training hazard the master asks about (stale moment estimates poisoning a fresh stage). Verified mechanics per candidate: PyTorch — construct a *new* `torch.optim.Adam(...)` at stage start (state dict starts empty; nothing to "clear"); MLX — new `optim.Adam` similarly; JAX/Optax — re-`init` the optimizer state pytree. L-BFGS state never crosses a boundary (each stage's Phase 2b builds its own history). The *menu* here is only whether the skeleton ever supports **partial** carry (keep moments, reset step counters): the spec says no; the skeleton need not support it; offered to the sheet as "spec-reset (default) vs. add a partial-carry experiment flag later (two-way config addition)".
* **Rollback policy when a fresh stage goes bad:** **Option D7-C *(suggested default)*** — manual, one documented command: `python -m pinn.train --config <same.yaml> --resume runs/<name>/checkpoints/stage-{k}-final.pt --hold-stage` (resume at the anchor and *hold* in stage k; without `--hold-stage`, promotion criteria would immediately re-fire since they were just met). **Option D7-D** — auto-revert guard: on a divergence signal within the first ⚖ steps post-promotion, auto-restore `stage-{k}-final.pt` and stop with `GUARD: post-promotion divergence`. The *signal definition* is the R1b watchlist's divergence-after-transition item — join point; D7-D should be specced after consolidation, off by default. **Option D7-E** — none: rejected; the anchors exist precisely to make recovery a one-liner.
* **Resume across a boundary / death mid-promotion:** make promotion **idempotent and ordered**: (1) write `stage-{k}-final.pt` (atomic, D4); (2) append a promotion record to `runs/<name>/curriculum.jsonl` (`{from:k, to:k+1, step, criteria_snapshot}`); (3) construct new optimizer + schedule; (4) write `stage-{k+1}-init.pt`. On resume, the loop trusts the *checkpoint's* stage/phase fields, and reconciles against `curriculum.jsonl`: a final-anchor without its init-twin ⇒ the crash hit mid-promotion ⇒ redo (3)–(4) deterministically. The user-visible invariant: **resuming never re-asks "what stage am I in?" — the checkpoint knows.** This extends D4's resume invariants (additive) and gives §6.2's "curriculum progression" summary its data source (the jsonl).

### Suggested default for D7 — **A + spec-mandated reset + C now / D after R1b + the idempotent promotion record** *(suggestion; rows in the sheet)*

**Doors:** anchor naming, stage/phase fields in the checkpoint schema, and `curriculum.jsonl` are **one-way** (artifact contract). Rollback policy (C vs adding D) is two-way.

---

## §8. Baseline review findings (Baseline Critique Mandate) — option-vs-baseline proposals

Verdict on the decomposition first, then itemized findings. Each finding is *baseline vs proposed change*, with rationale; choice rows appear in the Decision Sheet.

**B-1 — PH-7's first-trial optimizer default conflicts with the science spec.** *Baseline:* "Adam, LR 1e-3, exponential decay 0.95/500 steps" (PhysicsNeMo-derived). *Spec:* per-stage `1e-3 × 0.7^k`, cosine annealing, two-phase with L-BFGS, median clipping (§0). The specs own the science; PH-7's default as written would have the first run silently off-spec. *Proposal:* replace PH-7's default with "the `ctl_instruction.md` Phase 2 schedule, stage 0 values" — same one-config simplicity, spec-conformant. (Option to keep baseline exists only as a consciously descoped pilot — see D5-A warning.) **Door: two-way** (config values) — but the *loop shape* it implies is D5's one-way door.

**B-2 — The committed monitoring fields under-count the loss.** *Baseline:* log line and `summary.md` show three loss terms (data/physics/IC). *Spec:* five terms (data, IC, phys-causal, E, L) **plus** scheduled λ values, gradient-norm/clip events, and conservation metrics are the named monitoring set. *Proposal:* widen the committed log-line fields to the five terms + total + current λ vector + grad-norm; same one-line-per-`log_freq` surface. **Door: two-way** (additive fields; JSONL consumers tolerate new keys).

**B-3 — Subsystem decomposition: right cut, two homeless concerns.** The three-subsystem + verification split is sound and kept. But (a) the **curriculum state machine** owns cross-cutting state (current stage, promotion history, per-stage data view) that spans Subsystems 2 and 3, and (b) **run control** (guards, signal handling, status heartbeat) is neither ingestion nor optimization. *Proposal (structure-naming, not re-architecture):* within Subsystem 3, name two explicit components with their own files — `CurriculumController` (owns stage/phase, `curriculum.jsonl`, promotion procedure of D7) and `RunController` (owns guards, status.json, Ctrl-C/bundle handling of D4). Keeps the plain-script style; gives the runbook nouns for "what stopped my run." **Door: two-way** (internal naming) — adopt-or-not without downstream cost.

**B-4 — The placeholder inventory (PH-1..10) is incomplete.** Missing early-settling decisions discovered by this round, each now homed: precision policy (D1 conditional — *absent from the PH list entirely despite being the biggest open scientific-execution question*); reproducibility/determinism policy (D6); checkpoint cadence/retention/corruption policy (D4); unattended auto-guards (D4); stage-boundary mechanics (D7); collocation *infrastructure* as distinct from PH-6's *strategy* (D5.2); **sL-BFGS implementation ownership** (D5.1 — custom in every framework; no PH covers who builds it); **validation-evaluation cadence** (the spec's promotion criteria need `L_val` computed on a schedule the documents never state — register U-5; it must become a config knob with an R2-tuned value); config schema versioning (B-5). *Proposal:* extend the inventory accordingly when the design doc is next revised. **Door: two-way** (documentation).

**B-5 — Resume invariant "different config ⇒ hard error" is too blunt.** As written, fixing a typo in a comment or extending `max_steps` bricks resume. *Proposal:* classify config fields — *identity fields* (architecture, data version, split seed, curriculum definition, loss/schedule contracts) where any diff refuses resume exactly as baseline intends, vs *operational fields* (`max_steps`, `log_freq`, guard toggles, tracker settings) where a diff resumes with a logged `CONFIG CHANGE:` line. The frozen `config.yaml` copy plus the diff log preserves provenance. **Door: two-way now, one-way later** — the field classification becomes part of the config schema people rely on; decide before the first real run.

**B-6 — The `runs/<name>/` contract needs additive members.** *Baseline contract kept;* proposal adds: `tb/` (D2 events live inside the hand-off folder), `checkpoints/stage-*-{final,init}.pt` (D7), `curriculum.jsonl` (D7), `failure/` bundle (D4), seed record in `status.json` (D6), and a `data-manifest.json` (dataset hash + split manifest pointer — making the version-mismatch check's evidence visible). **Door: one-way in the cheap direction** — additive files are free now; *removing or renaming* members later breaks the runbook, so adopt the final list before the runbook is written.

**B-7 — Cosmetic:** the error table's "CUDA out of memory" row should read MPS wording (the real strings are F3/F4-style or allocator OOM). Fold into the next doc revision. **Two-way.**

**B-8 — ε_H acceptance-gate direction (previously flagged; now confirmed consistent).** The baseline design doc's §6.3 ("Is this model good enough?") renders a gate example — `ε_H: 8.2e-6 (required: > 1e-5) → FAIL` (and `SCS: -3.4 (required: > -5) → PASS`) — whose comparators read *inverted* (as if a larger `ε_H`/`SCS` passes), conflicting with that same doc's plain-English "smaller is better; < 10⁻⁵ is excellent." That is a **display/wording slip in the baseline design doc** (a non-authoritative starting point; `trainex-r1b-findings.md` flags the same slip as C-12), **not** a contradiction in the locked metric. The authoritative spec is unambiguous: `ctl_instruction.md` (Conservation gate, lines 550–555) — `eps_H = max_t |(H(t) − H(0)) / H(0)|`, `SCS = log10(eps_H)`, **REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`)** — i.e. *smaller passes*; `eps_H = 0 → SCS = -inf → Excellent`; bands Excellent ≤ -10, Acceptable (-10, -6], Marginal (-6, -5], Reject > -5. Direction is settled (smaller passes); the design-doc §6.3 comparators should be corrected as a cosmetic edit (fold in with B-7), which is not an open adjudication. Register item U-3 is closed.

**B-9 — Config approach: single YAML (baseline) vs Hydra three-file stack (spec's reproducibility note).** `ctl_instruction.md` names a Hydra `stage/opt/loss.yaml` stack — under a heading the spec itself marks "**Ignore Now** and Come Back Later," so it is treated as deferred guidance, not a binding science contract. *Comparison:* baseline single-YAML-per-run + frozen copy = one file to read, no new tool, perfect fit for the operator profile; Hydra = composition/overrides/sweeps power the project doesn't yet need, plus a dependency and concept set. *Proposal:* keep baseline single-YAML, but **structure its top-level keys as `stage:`, `opt:`, `loss:`, `run:`** — capturing the spec's separation inside one file and making a later Hydra migration mechanical. **Door: two-way** (the key structure is the hedge).

**B-10 — `caffeinate -d` is likely the wrong flag for unattended runs.** `-d` prevents *display* sleep; unattended training needs idle/system-sleep prevention (`-i`/`-s`), and the robust pattern scopes it to the process: `caffeinate -is python -m pinn.train …` (assertion ends when training ends). Flag raised here because the launch-command *shape* is R1a surface; final sleep/lid/ops doctrine is **R1b's** lane — join noted. **Two-way** (command text).

**B-11 — The reproducibility promise over-claims for this platform.** §5.7's "give a colleague the folder ⇒ reproduce" is re-scoped by D6's verified findings (F6/F7) to "re-run to statistical equivalence + exact checkpoint continuation." Wording change in the next doc revision + runbook. **Two-way.**

**B-12 — Split-policy tension between the documents (record + route, not resolve).** Baseline PH-5: global ~80/10/10 stratified split. `ctl_instruction.md` stage-transition preamble: "hold-out 10–20 % of **cumulative data per stage**." These compose only if the global split is *stratified by stage* so per-stage cumulative validation views can be derived from the global val set. PH-5 is owned elsewhere (v1.5); this round only flags that whoever answers PH-5 must satisfy both sentences. Register U-4.

---

## §9. Door classification — what locks structure, what stays flexible

One line each; "one-way" = expensive to reverse once code/artifacts/runbook build against it; "two-way" = a config flip or doc edit later.

| Item | Door | Why |
|---|---|---|
| D1 framework pick | **One-way** | Everything (code, checkpoints, runbook, R2 numbers) inherits it. |
| D1 precision branch (fp32 vs fp64) | **One-way (practical)** | Changes device, step cost, feasible sizes; invalidates R2 tuning on the other branch. |
| D2 tracker pick | **Two-way** | *Conditional on* JSONL-as-source-of-truth (adopted in the default); swap = one writer class. |
| D3 residency policy (ram/mmap/auto) | **Two-way** | Hidden behind the adapter; config flip. |
| D3 adapter batch-interface | **One-way (mild)** | Loop code assumes it; it's the baseline's own committed seam. |
| D4 cadence/retention values | **Two-way** | Config numbers. |
| D4 atomic-write + weights_only checkpoint rules | **Two-way** | Internal write/read discipline; no consumer breaks if adopted late (but adopt early — it's free). |
| D4 guard *seams* in the loop (post-loss / pre-checkpoint / heartbeat) | **One-way (mild)** | Retrofitting hooks into a live loop is the rework case. |
| D4 guard tiers on/off | **Two-way** | Config toggles. |
| D4 diagnostic bundle | **Two-way** | Additive files. |
| D5 loop shape (two-phase, closure-based) | **One-way** | It *is* the skeleton; R2 tunes inside it. |
| D5 sampler interface signature | **One-way** | Callable contract the loop is written against (strategies inside it: two-way). |
| D5 weight-schedule module interface | **One-way** | Loop + checkpoints + logs depend on it (values: two-way). |
| D6 policy (accepted-variance vs strict) | **Two-way** | Config switch. |
| D6 seed/RNG block in config+checkpoint schema | **One-way (mild)** | Part of the artifact contract from run #1. |
| D7 anchor names, stage/phase checkpoint fields, `curriculum.jsonl` | **One-way** | Artifact contract; runbook and resume logic depend on them. |
| D7 rollback policy (manual C vs adding auto D) | **Two-way** | D is an additive guard later. |
| B-1 adopt spec optimizer schedule as first-trial default | **Two-way** | Config values (loop shape is D5's door). |
| B-2 widen log fields to 5 terms + λ + grad-norm | **Two-way** | Additive JSONL/log keys. |
| B-3 name CurriculumController / RunController | **Two-way** | Internal structure naming. |
| B-4 extend placeholder inventory | **Two-way** | Documentation. |
| B-5 config field classification (identity vs operational) | **One-way (soft)** | Becomes schema people rely on; settle before run #1. |
| B-6 final `runs/<name>/` member list | **One-way (soft)** | Adding is free now; renaming later breaks the runbook. |
| B-9 single-YAML with stage/opt/loss/run keys | **Two-way** | Key structure is the Hydra hedge. |
| B-10 `caffeinate -is` launch wrapper | **Two-way** | Command text (final ops doctrine: R1b). |
| B-11 re-scoped reproducibility wording | **Two-way** | Doc/runbook text. |

---

## §10. Decision sheet — fill in "Your pick"

| # | Decision | Options | Suggested default | Door | Your pick |
|---|---|---|---|---|---|
| D1 | ML framework | A PyTorch+MPS · B MLX · C JAX(CPU) | **A** | One-way | |
| D1-p | Precision branch (pending adjudication) | (i) fp32 residuals · (ii) fp64 required → CPU menu (ii)-1/2/3 | **(i), adjudicated via the spec's §10 probes; if (ii): (ii)-1 PyTorch-CPU** | One-way | |
| D2 | Tracker / monitor secondary surface | A TensorBoard · B CSV+scripts · C MLflow · D W&B-offline | **A + JSONL-canonical + one plot script** | Two-way | |
| D3 | Data residency behind adapter | A in-RAM fp32 · B mmap/stream · C auto-selector | **C (auto → A at expected sizes), workers=0, watermark 0.7** | Two-way | |
| D4-a | Checkpoint cadence & retention | A latest-only · B rolling3+best+anchors · C periodic archive | **B** (cadence 1000 kept) | Two-way | |
| D4-b | Corruption safety | tmp+fsync+rename atomic writes; fallback scan | **adopt** | Two-way | |
| D4-c | Auto-guard tier | 0 none · 1 terminal-failure · 2 +environment · 3 +auto-remediation | **1+2 on; 3 later (post-R1b)** | Seams one-way; toggles two-way | |
| D4-d | Failure diagnostic bundle | on/off | **always on** | Two-way | |
| D5-a | Loop shape | A single-phase Adam · B two-phase closure · C pluggable phases | **B** | One-way | |
| D5-b | Collocation infrastructure | D fixed uniform · E sampler interface (uniform+spec-adaptive) · F E+residual-pool now | **E (with stateful-hook signature)** | Interface one-way | |
| D5-c | Loss-weight machinery | G static (fails spec) · H scheduled module · I H+rebalance hook | **H (+ empty I seam)** | Interface one-way | |
| D6 | Determinism policy | A strict always · B accepted-variance+seed policy · C B+strict debug switch | **B+C** | Policy two-way; seed schema one-way | |
| D7-a | Boundary checkpoints | A dual anchors (final+init) · B cadence-only | **A** | One-way | |
| D7-b | Optimizer state at boundary | spec full reset · (later) partial-carry experiment flag | **spec full reset** (mandated) | n/a (spec) | |
| D7-c | Rollback policy | C manual documented command · D auto-revert guard (post-R1b) · E none | **C now, spec D after R1b** | Two-way | |
| D7-d | Mid-promotion crash handling | idempotent ordered promotion + `curriculum.jsonl` | **adopt** | One-way | |
| B-1 | PH-7 first-trial optimizer default | keep baseline (off-spec pilot) · replace with spec stage-0 schedule | **replace with spec schedule** | Two-way | |
| B-2 | Committed log fields | keep 3-term · widen to 5 terms+λ+grad-norm | **widen** | Two-way | |
| B-3 | Name controller components | keep implicit · name CurriculumController/RunController | **name them** | Two-way | |
| B-4 | Extend PH inventory | keep · extend per §8 B-4 | **extend** | Two-way | |
| B-5 | Resume config-diff rule | keep blunt hard-error · field-classified diff | **field-classified** | One-way (soft) | |
| B-6 | `runs/<name>/` additions | keep minimal · adopt additive member list | **adopt** | One-way (soft) | |
| B-8 | ε_H gate direction (previously flagged; now confirmed consistent) | spec is unambiguous: REJECT if `eps_H > 1e-5` (smaller passes), per `ctl_instruction.md` 550–555 | **resolved — no open question; implement the gate as smaller-passes** | n/a | ✓ closed |
| B-9 | Config approach | single YAML (keyed stage/opt/loss/run) · Hydra 3-file stack | **single YAML, keyed** | Two-way | |
| B-10 | Sleep-prevention wrapper | `caffeinate -d` (baseline) · `caffeinate -is <cmd>` | **`caffeinate -is`** (final doctrine: R1b) | Two-way | |
| B-11 | Reproducibility wording | keep "give folder ⇒ reproduce" · re-scope per D6 | **re-scope** | Two-way | |

---

## §11. Composed first-run recipe (all suggested defaults, end-to-end) + conflict check

A coherence check that the menus compose — not a runbook (that's downstream, with R1b).

**One-time setup** (baseline §5.2 kept, framework slot filled):

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh        # close terminal, open a new one
conda create -n pinn-train python=3.11
conda activate pinn-train
pip install torch tensorboard pyyaml numpy h5py   # torch 2.12.x wheel includes MPS [F1]
python -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"
# expected: 2.12.x True
```

**First build acts (before any long run):** run the spec's §10 acceptance probes on-device — especially the componentwise-AD probe (10.3) and the loss-stability dry run (10.5) — in float32 on `mps`, with `PYTORCH_ENABLE_MPS_FALLBACK` *unset* so any unimplemented op in the double-backward graph fails loudly (F4; register U-9). This simultaneously certifies the AD contract and feeds the precision adjudication (D1 conditional).

**Configure** — one YAML per run, keyed per B-9:

```yaml
# configs/runs/first-run.yaml
run:   { name: first-run, seed: 1234, device: mps, precision: float32,
         max_steps: 100000, log_freq: 100, checkpoint_every: 1000,
         guards: {nan: true, loss_explosion: true, disk_floor: true,
                  memory_watermark: true} }      # thresholds ⚖ pending R1b
stage: { start: 0, data_version: <from v1.5 PIPE-XX>,
         residency: auto }                        # D3-C
opt:   { schedule: ctl-phase2, stage0_lr: 1.0e-3, anneal: cosine,
         lbfgs: {history: 10, line_search: strong_wolfe, max_iter: 20} }  # B-1/D5-B
loss:  { weights: phys05-warmup, collocation: {strategy: uniform, n_col: 2048} }  # D5-H/E
```

**Launch** (baseline command shape kept; sleep wrapper per B-10):

```bash
cd <project-root> && conda activate pinn-train
caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml
```

**What you watch:** the committed startup sequence (device line — now also `mem cap: 16.8 GB (0.7×)`; data line; `Stage 0 of 7`), then one line per 100 steps showing **five** loss terms + total + lr + λ vector + s/step + ETA (B-2), and every 1,000 steps a `mem:` line (D3). Secondary: `tensorboard --logdir runs/` → http://localhost:6006 (D2). Mac-side: Activity Monitor GPU > 0 %, swap flat (baseline §5.5 kept).

**Stage-0 shape under the defaults:** Adam phase with PHYS-05 warmup → plateau handoff → full-batch L-BFGS via accumulate-in-closure (D5-B) → four promotion criteria evaluated at the validation cadence (**value needed — U-5**) → on promotion: `stage-0-final.pt`, `curriculum.jsonl` record, fresh Adam, re-warmed λ, `stage-1-init.pt` (D7). Stop anytime: Ctrl-C once = graceful checkpoint (baseline kept). Guard stop: `GUARD: <reason>` + `failure/` bundle (D4).

**Resume** (baseline shape kept; works across boundaries per D7-d):

```bash
caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml \
    --resume runs/first-run/checkpoints/latest.pt
```

**Pairwise conflict check across the composed defaults:** (1) *B-1 vs baseline PH-7* — resolved in the recipe by adopting the spec schedule; the only genuine cross-document conflict found. (2) *D5-B full-batch L-BFGS vs 24 GB* — resolved structurally by accumulate-in-closure; residual risk is wall-time, not memory (R1b duration question — dependency noted). (3) *D2 TensorBoard vs B-6 folder contract* — resolved by homing `tb/` inside `runs/<name>/`. (4) *D6 accepted-variance vs §6.2 run comparison* — resolved by the seed-band protocol; requires the 2–3× stage-0 pilot repeats to calibrate the band (cheap; piggybacks on the owner's own "test stage 0 first" instinct). (5) *D4 guards + D7 promotion vs plain-loop style* — both consume the same closure/seam structure of D5-B; no second mechanism introduced. (6) *Expected run duration* — **not estimated here**; R1b's feasibility lane (explicit join). No other pairwise conflicts found among the suggested defaults.

**Numbers the project must supply before the recipe is executable:** `S̄` (snapshots/trajectory) or `t_max` per dataset set, cumulative per-stage data sizes (D3/U-1); the validation-evaluation cadence (U-5); guard thresholds ⚖ (R1b); `data_version` string (v1.5 PIPE-XX). (The ε_H gate direction, previously listed here as B-8/U-3, is resolved — the spec defines it unambiguously as smaller-passes; see §8 B-8.)

---

## §12. What the runbook inherits

From the suggested defaults (changes if your picks differ):

* **Command shapes:** setup block (§11); launch = `caffeinate -is python -m pinn.train --config <yaml>`; resume = same + `--resume <checkpoint>`; rollback = same + `--resume …/stage-{k}-final.pt --hold-stage`; monitor = `tensorboard --logdir runs/`; evaluate = baseline §6.3 command unchanged.
* **Checkpoint artifact format:** single `.pt` per checkpoint containing only state_dicts/tensors/scalars (loads under `torch.load` defaults, F8); names `step-XXXXXX.pt`, `latest.pt` (copy), `best.pt`, `stage-{k}-final.pt`, `stage-{k}-init.pt`, `emergency-*.pt`; `*.pt.tmp` is documented crash debris.
* **Run-folder contract (B-6 superset of baseline §5.7):** `config.yaml` (frozen), `checkpoints/`, `logs/train.log{,.jsonl}`, `tb/`, `curriculum.jsonl`, `status.json` (now with heartbeat timestamp + seed record + guard state), `summary.{md,json}`, `failure/` (only on failure), `data-manifest.json`.
* **Monitoring vocabulary:** the five loss terms + λ vector + grad-norm in every log line; `GUARD: <reason>` stop messages; the heartbeat rule ("status.json older than 10 min while the process lives ⇒ hung"); the `mem:` line and the 0.7 watermark meaning.
* **Comparison doctrine (D6):** runs are compared on validation metrics outside the calibrated seed-band; the folder hand-off promise is re-scoped to statistical-equivalence + exact checkpoint continuation (B-11).
* **Hard-constraint pressure flags (flagged, never redesigned):** (1) full-batch L-BFGS naïvely violates the 24 GB reality — the runbook must carry the accumulate-in-closure assumption and its wall-time consequence (constraint 1; durations → R1b). (2) Under precision branch (ii), every GPU-related instruction in the baseline (device line, "GPU 60–95 %" health check, MPS error rows) becomes inapplicable — the runbook forks on the adjudication outcome (constraint interplay between hardware reality and the open precision requirement; the conditional, not this document, decides). (3) Determinism limits (F6/F7) cap what any runbook may promise about reproduction (operator-reality constraint 2: don't teach the user a check that platform noise will fail). (4) The unattended-run premise (constraint 5) is only as good as the sleep wrapper and guards — final lid/sleep/thermal doctrine is **R1b's**, and the runbook should not be written before that consolidation.
* **R1b joins inherited as placeholders:** guard thresholds ⚖; divergence-after-transition signal (enables D7-D); run-duration/feasibility numbers; health-watchlist wording for the "what you watch" sections.

---

## §13. Claims-and-uncertainty register

Open items — recorded, not asserted. (Sources in §14 cover what *was* verified.)

| ID | Item | Status / what's needed |
|---|---|---|
| U-1 | **Snapshots per trajectory (`S̄`) / integration horizon per dataset set** — controls the D3 in-memory verdict | Not in the attached files. Project must supply `S̄` or `t_max` per set + cumulative per-stage sizes. D3 is parameterized to absorb any answer. |
| U-2 | M5 Pro–specific MPS performance characteristics (step times, thermal envelope under sustained second-order AD) | No primary-source benchmark data for this brand-new SoC located as of 2026-06-12; treat all throughput intuitions as unmeasured. On-device measurement + R1b feasibility lane. |
| U-3 | **Direction of the locked ε_H gate — CLOSED** | Resolved: the inverted-looking example lives in the baseline design doc's §6.3 (`ε_H: 8.2e-6 … → FAIL`; r1b flags it as C-12) and is a display typo, not a spec issue. The authoritative `ctl_instruction.md` 550–555 is unambiguous — REJECT if `eps_H > 1e-5` (smaller passes); `eps_H = 0 → Excellent`. Implement the gate as smaller-passes; correct the design-doc §6.3 comparators as a cosmetic edit (with B-7). |
| U-4 | Split-policy tension: global 80/10/10 (PH-5) vs "10–20 % of cumulative data per stage" (spec) | Both sentences must be satisfied by PH-5's eventual answer (stage-stratified global split is the compatible reading); owned by v1.5/PH-5, flagged here (B-12). |
| U-5 | **Validation-evaluation cadence** — the spec's promotion criteria consume `L_val(i)` but neither document says how often validation runs | Must become a config knob; numeric value is R2 territory; the *existence* of the knob is a D5 skeleton fact (adopted). |
| U-6 | Causal-weight underflow clip bound | Spec explicitly declines to choose and instructs surfacing a gap if execution needs one — it will (exp of large negative sums); gap surfaced; value to be set at implementation with a logged rationale. |
| U-7 | **Stochastic L-BFGS provenance and algorithm** — "batch 32, curvature interval 10" matches research variants, but the spec cites no reference implementation; none of the three frameworks ships one (F11/F13; torch's LBFGS is deterministic-objective) | Custom-implementation ownership is unassigned (B-4). Needs either a scheduling decision by the owner or spec-level renegotiation (out of this round's authority). |
| U-8 | MLX float64 *CPU* op coverage for this exact workload (relevant only if D1-B met branch (ii)) | Vendor states fp64-CPU-only in general (F10); per-op coverage for SIREN/double-grad not verified; moot under the suggested default. |
| U-9 | **Whether every kernel in this network's double-backward graph has an MPS implementation** (sin/linear/LayerNorm backward-of-backward, `jacfwd`/`jacrev` interactions) | Not provable from documentation — the op-coverage surface is a moving list (F4). Adjudicated empirically by running the spec's §10.3 probe with fallback disabled (first build act, §11). |
| U-10 | MLX / Metal GPU kernel determinism guarantees | No vendor statement located either way; treat as accepted-variance like MPS if MLX is ever picked. |
| U-11 | Referenced-but-unattached materials: `sampling_method.md`, the Phase 18 FRAME-01 preprocessing doc, `simulation_data/Documentation/README.md`, v1.5 PIPE-XX format, and the SCS/SASD/IPR/PSC metric definitions (gate consumes SCS; only its threshold is in the attached design) | Treated as unavailable per the master's instruction; the verification layer cannot fully specify `metrics.json` until the metric definitions arrive. |
| U-12 | `data_version_hash` production/verification mechanism | The check is committed baseline; the hash's source is v1.5 PIPE-XX's; the adapter implements "compare and refuse," nothing more. |
| U-13 | Exact current TensorBoard release number | Not pinned by primary source in this round (the tool's command surface, which is what the menus rely on, is stable); pin at install time via `pip show tensorboard`. |
| U-14 | SI-PINN-003: batch-construction inconsistency between `pinn_architecture.md`'s `get_batch` listing and the CTL replay/lookahead plan | Flagged inside the spec itself; D5's batch assembly should follow the CTL composition (replay+lookahead) and treat the architecture listing as illustrative — but the reconciliation is the spec owners', not this round's. |
| U-15 | Expected run durations / first-run feasibility | **Explicit R1b dependency** — referenced at every point durations matter (§11, §12); deliberately not estimated here. |

---

## §14. Sources (all accessed / re-verified 2026-06-12)

| Tag | Source | Used for |
|---|---|---|
| S1 | PyPI `torch` project page (release 2026-05-13; Python ≥ 3.10) | F1 current stable 2.12.0 |
| S2 | github.com/pytorch/pytorch/releases (2.12.0 entry, ~2026-05-11) | F1 |
| S3 | pytorch/pytorch issue #177819 (2026-03; "MPS backend is supported on macOS 14.0+" runtime string; macOS-26 detection bug) | F2 macOS floor + failure-surface example |
| S4 | pytorch/pytorch issue #78168 + Lightning #21261 + PyTorch Forums threads (canonical float64-on-MPS TypeError) | F3 |
| S5 | Apple Developer Forums threads 797778 & 709663 (DTS: no FP64 in MPS; "Apple GPUs do not support FP64 and neither does Metal") + Apple MPSDataType documentation (via Lightning #21261) | F3 hardware wall |
| S6 | Hugging Face Transformers "Apple Silicon" docs (PYTORCH_ENABLE_MPS_FALLBACK; bf16/fp16 on MPS; macOS floors) | F3/F4 |
| S7 | pytorch/pytorch issue #77764 (general MPS op-coverage tracker) | F4 |
| S8 | docs.pytorch.org stable/2.9/2.10 `torch.mps` pages + `torch/mps/__init__.py` on main (full export list; `set_per_process_memory_fraction` semantics 0–2 × recommendedMaxWorkingSetSize; no user streams) | F5 |
| S9 | docs.pytorch.org "Reproducibility" note (stable 2.8–2.11 wording verified identical) | F6 |
| S10 | pytorch/pytorch issue #97236 (open, triaged: nondeterministic MPS training despite seeding + deterministic flag; CPU bit-stable) | F7 |
| S11 | pytorch/pytorch issue #122394 (deterministic-algorithms ~7× MPS slowdown, M1 Max / macOS 14.4) | F7 |
| S12 | PyTorch dev-discuss "BC-breaking: torch.load flipped to weights_only=True" (+ #137602; downstream issues showing `GLOBAL torch.optim.adam.Adam … not an allowed global`, `numpy.core.multiarray.scalar`) | F8 |
| S13 | PyPI `mlx` / `mlx-metal` pages (0.31.2, 2026-04-22; attested ml-explore release builds; CUDA extras) | F9 |
| S14 | MLX 0.31.2 documentation, "Data Types" (float64 CPU-only; GPU exception) | F10 |
| S15 | MLX 0.31.x documentation, "Optimizers" page (full optimizer list; no L-BFGS; tree_flatten + save_safetensors state example) | F11 |
| S16 | developer.apple.com/metal/jax/ (experimental; unsupported dtypes incl. float64) + jax-ml/jax issue #34109 (2025-12, broken on recent macOS/jaxlib) + Apple forums thread 743350 | F12 |
| S17 | jax-ml/jax discussion #34648 (2026-01: jax-metal "no longer maintained") + PyPI `jax-mps` (0.10.3, 2026-06-04, alpha, jaxlib-0.9.0-pinned) | F12 |
| S18 | Optax stable documentation, Optimizers — `optax.lbfgs` (zoom linesearch) | F13 |
| S19 | docs.wandb.ai support: "run wandb offline" (WANDB_MODE=offline stores locally; `wandb sync DIRECTORY` streams to the server; `disabled` mode) | F14 |
| S20 | mlflow.org releases page (3.10.0 et al.) + self-hosting docs (3.7.0 SQLite default; `mlflow ui` localhost:5000; file store maintenance mode) | F15 |

Project-internal citations throughout refer to the four attached snapshots by filename and section; no repository content was available or used. — *End of deliverable.*
================================================================================
END ORIGINAL: trainex-r1a-options-and-decisions.md
================================================================================
================================================================================
BEGIN ORIGINAL: chatgpt-pro-resolution.md
================================================================================
---
title: "Trainex R1a — Core Decisions and Structure for CTL-PINN Training Execution"
status: research-options-menu
research_date: 2026-06-19
package: trainex-r1a
scope: decisions-and-structure
hardware_target: "single Apple-silicon MacBook Pro M5 Pro, 24 GB unified memory"
final_decision_owner: project owner
---

# Trainex R1a — Core Decisions and Structure for CTL-PINN Training Execution

**Research cut-off:** 19 June 2026  
**Role of this document:** options and consequences, not final decisions  
**Companion dependency:** trainex R1b supplies operations/runbook findings such as feasible run durations, laptop sleep/thermal practice, and empirically justified health-alert thresholds.

## 1. Executive summary

The suggested coherent default is:

- **PyTorch 2.12 on MPS in float32** if accelerator float32 passes the project's physics-residual accuracy probes; **the same PyTorch implementation on CPU in float64** if float64 is required. None of PyTorch MPS, MLX Metal, or JAX Metal can honestly perform float64 training on the Apple GPU today.
- **Terminal log + tracker-neutral JSONL/CSV as the record of truth, with TensorBoard as the local browser view.**
- **Chunked HDF5 streaming with a bounded, stage-local cache**, rather than assuming the full dataset fits beside the model, optimizer, collocation candidate pool, and second-order autodiff graph in 24 GB.
- **Transactional checkpoints** triggered by elapsed time, important events, and an optional maximum-step gap; immutable stage-boundary checkpoints; checksums; explicit recovery state separate from model exports; hard non-finite guards; and a standard diagnostic bundle on failure.
- **A pluggable but small training-phase state machine** that can express Adam, full-batch L-BFGS, the still-unresolved stochastic L-BFGS implementation, collocation refresh/adaptation, and scheduled five-term loss weights without turning the project into a general-purpose training framework.
- **A two-tier reproducibility policy:** deterministic CPU acceptance tests plus provenance-complete, seeded accelerator training whose residual run-to-run variance is acknowledged and measured for consequential comparisons.
- **Transactional curriculum promotions:** immutable stage-complete checkpoint, prepared/committed journal, model-weight carry, mandatory Adam/scheduler reset, loss-weight re-warm, and manual—not automatic—rollback unless R1b later validates a reliable automatic signal.

Three issues block an honest full scientific first run unless resolved before launch:

1. **Precision adjudication:** accelerator float32 versus required float64.
2. **Stochastic L-BFGS definition:** the authoritative CTL spec requires sL-BFGS in later stages but does not identify an algorithm, implementation, or checkpointable state contract.
3. **Final quality-gate identity and direction:** the baseline uses `ε_H` inconsistently, while the framework specs also use similar names for a data-admission metric and a training-loss denominator. The locked thresholds must not be changed here, but the evaluator cannot be implemented faithfully until the project supplies an unambiguous metric ID, comparator, aggregation, and split.

The baseline's useful ideas should be retained: one operator-facing workflow, a thin data adapter, a run directory as the handoff unit, terminal-first monitoring, a separate evaluator, and explicit resume support. The main structural change is to keep that surface simple while splitting the implementation into data/admission, training engine, run-state/artifacts, and evaluation components. A single large training script is too fragile for the required curriculum, optimizer phases, adaptive collocation, checkpoint transactions, and failure handling.

## 2. Authority, scope, and decision language

### 2.1 Source authority

The following attached files are treated as project sources:

- **[P-MASTER]** `RESEARCH-CONTEXT-MASTER.md`: scope, hard constraints, D1–D7, and output contract.
- **[P-BASE]** `2026-06-10-training-execution-design.md`: challengeable brainstorm baseline.
- **[P-CTL]** `ctl_instruction.md`: authoritative curriculum/data/training-method framework spec.
- **[P-ARCH]** `pinn_architecture.md`: authoritative architecture, output, autodiff, and loss framework spec.

The two framework specs outrank the baseline on scientific mechanics. Primary-source web evidence is identified by `[W-…]` keys and listed in Section 14.

### 2.2 Terms

- **Suggested default** means the option that currently appears to give the best balance under the stated assumptions. It is not a project decision.
- **One-way door** means later reversal would require broad code, artifact, or experiment migration and could invalidate comparability.
- **Two-way door** means the option can be swapped through a narrow interface or configuration change without rewriting the pipeline or invalidating old runs.
- **Mechanical surface** means what the owner types, what appears on screen, and what files are created.

### 2.3 Hard constraints preserved

Every menu below preserves:

1. one M5 Pro MacBook, 16 CPU cores, 15 GPU cores, 24 GB shared unified memory;
2. no cloud and no distributed training;
3. a non-expert operator using a runbook;
4. componentwise first and second input derivatives through autodiff for the physics residual;
5. the CTL outer stage machine and resumability across stage boundaries;
6. long unattended laptop runs where recoverability is more important than a peak benchmark;
7. the authority of the framework specs; and
8. the project-locked final quality-gate metrics and thresholds, pending clarification of their contradictory notation/direction.

### 2.4 Scientific execution contracts the pipeline must not simplify away

The trainer must implement, rather than redesign:

- a 14-dimensional input `[tau, IC_13]`, with `u=t/T` as the autodiff leaf and `tau=2u-1` as network time;
- the 12-hidden-layer, width-256 SQR-SkipResNet-SIREN architecture and hard mass-weighted center-of-mass projection;
- a 9-position output whose velocities and accelerations are obtained componentwise from first and second derivatives with respect to `u`;
- the prohibition on replacing the full output Jacobian with `grad(r.sum(), u)`;
- the five named loss terms `L_data`, `L_IC`, `L_phys^causal`, `L_E`, and `L_L`;
- Adam exploration followed by L-BFGS refinement within each stage; full-batch L-BFGS in early stages and sL-BFGS in later stages;
- scheduled loss weights during Adam, frozen weights during L-BFGS, and re-warm at each stage;
- model-weight carry but complete Adam-state reset at a new stage;
- curriculum replay and lookahead sampling; and
- canonical, float64 HDF5 data with strict trajectory admission/quarantine and no dense-ID assumption. [P-CTL] [P-ARCH]

## 3. Decision map

| ID | Decision | Suggested direction | Door |
|---|---|---|---|
| D1 | ML framework | PyTorch 2.12; MPS/f32 if validated, CPU/f64 if required | One-way |
| D2 | Tracking/monitoring | Terminal + canonical JSONL/CSV + TensorBoard | Two-way |
| D3 | Unified-memory/data use | Streaming HDF5 + bounded stage cache | One-way capability; two-way limits |
| D4 | Checkpoint/guards/diagnostics | Transactional hybrid-event recovery policy | One-way core |
| D5 | Training-loop skeleton | Small pluggable phase/collocation/loss state machine | One-way |
| D6 | Reproducibility | CPU deterministic acceptance + seeded accelerator production | One-way provenance contract |
| D7 | Stage boundaries | Transactional prepared/committed promotion, manual rollback | One-way state contract |

The detailed menus follow. The fill-in decision sheet is the final section.

# 4. D1 — ML framework

## 4.1 What D1 must support

This is not a generic neural-network choice. The decisive workload is a deep sinusoidal network whose loss differentiates all nine position outputs once and twice with respect to one time input and then differentiates that residual loss with respect to model parameters. The framework must also express closures/full-batch L-BFGS, preserve optimizer and random state, run for hours on Apple Silicon, and be diagnosable by a non-expert.

### Precision facts that apply before comparing ergonomics

| Candidate accelerator path | Float32 | Float64 on Apple GPU | Honest float64 alternative |
|---|---:|---:|---|
| PyTorch MPS | Yes | **No.** PyTorch's MPS dispatch rejects `float64` tensors rather than silently computing them on the GPU. | PyTorch CPU `float64` |
| MLX Metal | Yes | **No.** MLX 0.31.2 documents that `float64` arrays work only on CPU and raise on GPU. | MLX CPU `float64` |
| JAX Metal plug-in | Yes | **No.** Apple's current page lists `np.float64` as unsupported. | JAX CPU with 64-bit mode enabled |

Sources: [W-PY-03] [W-MLX-02] [W-JAX-02]. A split design that trains the network in GPU float32 while evaluating a detached residual in CPU float64 does **not** satisfy a requirement that the physics residual and its parameter gradients be trained in float64. Cross-device differentiable execution would need separate proof and would likely erase the intended simplicity.

## 4.2 Option A — PyTorch 2.12 + MPS/CPU

**Mechanical surface**

Proposed setup hides installation behind the project wrapper, but the resolved environment must pin at least:

```text
Python 3.11.x
PyTorch 2.12.0
architecture: arm64
```

The owner sees:

```bash
./trainex setup --framework pytorch
./trainex doctor --device mps --precision float32
```

or, under the float64 branch:

```bash
./trainex doctor --device cpu --precision float64
```

The run manifest records `torch.__version__`, macOS build, device, dtype, MPS availability, fallback setting, and the results of the derivative probes.

**Strengths**

- `torch.func.jacrev`, `jacfwd`, `vmap`, VJP, and JVP are documented composable mechanisms for Jacobians and higher derivatives. They match the architecture spec's preferred `jacrev + vmap` form. [W-PY-04]
- Native Adam and L-BFGS exist. PyTorch L-BFGS uses a closure and documents its substantial extra memory, one-device restriction, and history-size cost; those limitations are visible rather than hidden. [W-PY-07]
- State-dict checkpointing for model and optimizer is mature. CPU RNG and MPS RNG state can be captured, while run-owned state can be placed in the same bundle. [W-PY-06] [W-PY-11]
- PyTorch 2.12 was released in May 2026 and includes an Apple-MPS-specific improvement; the project is on a frequent release cadence. [W-PY-01] [W-PY-02]
- The broad scientific/PINN ecosystem is a practical maintenance advantage. As one official ecosystem signal, DeepXDE documents PyTorch and JAX backends but not MLX. [W-ECO-01]
- A single codebase can run MPS float32 and CPU float64, making the precision branch a device policy rather than a rewrite.

**Weaknesses and failure surface**

- MPS does not support float64. [W-PY-03]
- Backend coverage is not equivalent to CPU/CUDA coverage. Historical and current issue reports include failures in higher derivatives and incorrect gradients for particular MPS operations. Those reports do not prove this CTL-PINN fails, but they make an exact project-specific derivative/gradient probe a launch gate. [W-PY-09] [W-PY-10]
- PyTorch can fall back to CPU for unsupported MPS operations when `PYTORCH_ENABLE_MPS_FALLBACK=1`. That is useful for debugging but dangerous for an unattended run because it can silently turn one operation into a severe performance bottleneck. The suggested production policy is fallback **disabled** and unsupported operations treated as a preflight failure. [W-PY-05]
- Full-batch L-BFGS can consume substantial memory because it stores parameter/gradient history. The real peak must be measured with the exact model, batch, loss graph, and history size.
- PyTorch's broad API makes it possible to accidentally mix old `autograd.grad` patterns and `torch.func` transforms. The implementation must have one tested derivative path.

**Downstream implications**

- D5 can use built-in Adam and built-in full-batch L-BFGS, but the later-stage sL-BFGS requirement still needs a project-selected implementation.
- D2 receives native TensorBoard integration through `SummaryWriter`.
- D4 can use one native `.pt` recovery bundle, but run-owned metadata and checksums still must be designed.
- D6 can invoke deterministic-algorithm checks, but PyTorch explicitly does not promise reproducibility across releases/platforms and deterministic operations can be slower. [W-PY-08]

## 4.3 Option B — MLX 0.31.2

**Mechanical surface**

```bash
./trainex setup --framework mlx
./trainex doctor --device gpu --precision float32
```

The environment pins `mlx==0.31.2` and the run records the exact Metal device and MLX memory limits. The owner does not move arrays between separate CPU RAM and VRAM; MLX arrays live in the Apple unified-memory pool. [W-MLX-01] [W-MLX-04]

**Strengths**

- MLX is designed specifically around Apple Silicon and unified memory. Its programming model avoids explicit host-to-GPU copies for ordinary arrays. [W-MLX-04]
- MLX documents composable `grad`, `value_and_grad`, `jvp`, `vjp`, and `vmap`; its quick-start explicitly demonstrates nested gradients. [W-MLX-03]
- It exposes allocator telemetry and memory/cache limits, useful on a 24 GB shared-memory machine. [W-MLX-06]
- The framework is actively released by Apple; 0.31.2 was the latest release shown on 19 June 2026. [W-MLX-01]
- Adam and common schedulers are present, and optimizer state can be serialized.

**Weaknesses and failure surface**

- GPU float64 is unavailable; CPU float64 is documented. [W-MLX-02]
- The official 0.31.2 optimizer catalogue does not list L-BFGS. Meeting the authoritative full-batch and stochastic L-BFGS contracts therefore requires a custom or external optimizer, including line search, state serialization, failure handling, and tests. [W-MLX-05]
- MLX optimizer state does not necessarily contain every constructor parameter: the docs specifically warn that Adam state omits some configuration such as betas and epsilon. The checkpoint must therefore reconstruct the optimizer from the frozen config and then restore state. [W-MLX-05]
- The exact nested operation required here—componentwise second derivatives with respect to input, followed by gradients of the residual loss with respect to parameters—must be benchmarked and correctness-tested on Metal. General transform composability is necessary but not sufficient.
- The PINN ecosystem and examples are smaller. This increases the burden on the project owner when an issue is specific to higher-order scientific autodiff.
- Lazy evaluation and compilation are powerful but add a synchronization/debugging concept that the runbook must explain when timing and catching failures.

**Downstream implications**

- D5 becomes materially more expensive: L-BFGS and sL-BFGS are project-owned research/software components rather than adapters around supported optimizers.
- D2 should not depend on framework-native TensorBoard support; a tracker-neutral event writer becomes mandatory.
- D4 needs an explicit multi-file or run-owned checkpoint bundle for parameters, optimizer state, config, RNG keys, and stage/sampler state.

## 4.4 Option C — JAX 0.10.2 + Optax + Equinox on the Apple Metal plug-in

**Mechanical surface**

The user-facing command can remain simple, but the lock file must contain an **exact tested tuple** of Python, JAX, jaxlib, `jax-metal`, Optax, and Equinox:

```bash
./trainex setup --framework jax-metal
./trainex doctor --device metal --precision float32
```

The setup must not independently install “latest JAX” and “latest jax-metal.” Apple's current compatibility page lists `jax-metal` versions and minimum jaxlib versions, and offers a compatibility environment flag; it does not certify every current JAX release as a tested CTL-PINN stack. [W-JAX-02]

**Strengths**

- JAX has the cleanest transformation model of the three for nested input derivatives. Official documentation covers `jacfwd`, `jacrev`, `vmap`, Hessians, and forward-over-reverse composition. [W-JAX-03]
- Optax currently exposes L-BFGS and line-search components. [W-JAX-04]
- Explicit PRNG keys make random streams easy to partition and record.
- Equinox provides straightforward PyTree/module serialization, and Orbax can checkpoint separable model/optimizer/data-iterator state. [W-JAX-05] [W-JAX-06]
- JAX itself is released frequently; 0.10.2 is dated 17 June 2026. [W-JAX-01]
- JAX is represented in scientific/PINN ecosystems such as DeepXDE. [W-ECO-01]

**Weaknesses and failure surface**

- Apple labels the Metal plug-in **experimental**, says not all JAX functionality is supported, says it does not pass all JAX tests, and lists float64 as unsupported. This is the largest unattended-run reliability risk among the candidates. [W-JAX-02]
- Version compatibility is a multi-package responsibility. A future update can break the tested tuple even when the training code is unchanged.
- JIT compilation, functional state, PyTrees, explicit keys, Equinox filtering, and Optax transformations produce a steeper mental model for a non-expert maintainer.
- Shape changes at curriculum stages or adaptive collocation refreshes can trigger recompilation unless the loop is carefully shape-stable.
- Optax L-BFGS satisfies the existence of a quasi-Newton mechanism, not the project's undefined sL-BFGS contract.
- CPU float64 is possible, but then the chief Apple-Metal advantage disappears and the stack remains the most complex.

**Downstream implications**

- D5 must be designed around pure functions and immutable optimizer state.
- D4 likely benefits from Orbax, but that adds another subsystem and checkpoint schema.
- D6 gets excellent explicit seed plumbing, but no primary source found here promises deterministic Metal kernels for this workload.

## 4.5 Precision conditional and suggested default

### Branch 1 — float32 on the accelerator is sufficient

**Suggested default: PyTorch 2.12.0, eager execution, MPS, float32.**

This suggestion is conditional on a mandatory preflight that verifies:

1. all nine first and second derivatives against an analytic synthetic trajectory;
2. gradients of the complete five-term loss with respect to every trainable parameter;
3. CPU/MPS numerical agreement at project-defined tolerances;
4. no unsupported-operation fallback;
5. finite forward/backward behavior through the SIREN, COM projection, force, energy, and angular-momentum code; and
6. stable peak memory for a representative micro-step.

The reason is not a claim that PyTorch MPS is universally faster. It is the combination of the most maintainable implementation, direct alignment with the architecture spec's sample derivative API, supported Adam/full-batch L-BFGS, mature checkpointing, local TensorBoard integration, and the ability to retain the same code under a CPU float64 branch.

### Branch 2 — float64 is required for the physics residual and training gradients

**Suggested default: PyTorch 2.12.0 on CPU in float64.**

The framework suggestion does not change; the device strategy does. PyTorch MPS, MLX Metal, and JAX Metal cannot satisfy this branch. MLX CPU float64 and JAX CPU float64 remain technically viable alternatives, but they carry, respectively, the L-BFGS implementation deficit and the highest stack complexity. A hybrid that computes only evaluation diagnostics in float64 is useful as a check but is not an answer to a float64 training requirement.

**Door classification — D1 suggested default: ONE-WAY DOOR.** The framework permeates modules, optimizer state, checkpoint files, random-state representation, tracing/debugging, tracking integration, and tests. A device switch inside PyTorch is relatively reversible; a framework switch after implementation is not.

# 5. D2 — Experiment tracking and monitoring

## 5.1 Invariant surface for every option

Regardless of dashboard choice, the run directory should contain a tracker-neutral, append-only scalar record. Suggested canonical files:

```text
runs/<name>/metrics/events.jsonl
runs/<name>/metrics/scalars.csv
runs/<name>/logs/train.log
runs/<name>/status.json
```

Each record includes timestamp, global step, curriculum stage, optimizer phase, all five unweighted losses, all active loss weights, total loss, learning rate, gradient statistics, conservation diagnostics, data/collocation counts, step time, I/O time, and memory telemetry. This prevents a dashboard swap from destroying historical comparability.

## 5.2 Option A — TensorBoard over canonical JSONL/CSV

**Mechanical surface**

```bash
./trainex monitor --run runs/my-first-run
# The wrapper prints the latest terminal status and, on request, launches:
tensorboard --logdir runs/my-first-run/metrics/tensorboard --host 127.0.0.1 --port 6006
```

The browser opens `http://127.0.0.1:6006`. The owner sees named panels for total/five losses, loss weights, stage/phase, learning rate, gradients, conservation metrics, throughput, and memory. The primary monitor remains the terminal; TensorBoard is the local visual history.

**Strengths**

- Native PyTorch `SummaryWriter` integration. [W-TRK-01] [W-TRK-02]
- No account, cloud service, database, or Docker.
- Low conceptual load for one machine and one user.
- Event files stay in the run directory and can be regenerated from canonical JSONL if the adapter changes.

**Weaknesses**

- It is a viewer, not a complete experiment database or artifact registry.
- Event files are framework/tool-specific; the neutral JSONL/CSV is still required.
- Cross-run filtering and rich metadata queries are weaker than MLflow/W&B.

**Interactions**

Best fit with D1 PyTorch. Still usable with MLX/JAX through a neutral writer, but integration becomes project-owned.

## 5.3 Option B — Weights & Biases in offline mode

**Mechanical surface**

```bash
wandb offline
./trainex launch --config configs/runs/my-first-run.yaml
```

or the wrapper sets `WANDB_MODE=offline`. Files appear under a local W&B directory. A full local browser server is a separate deployment; official W&B CLI documentation describes a local server command, but this adds a service/container footprint. [W-TRK-03] [W-TRK-04]

**Strengths**

- Strong run comparison, metadata, media, and table UX.
- Integrations exist across major Python frameworks.
- Offline capture avoids accidental cloud dependence if network sync is disabled by policy.

**Weaknesses**

- “Offline” collection does not by itself give the same simple local browser experience as TensorBoard. A self-hosted/local server is a materially larger operational surface.
- More files, background behavior, and concepts for a first-time trainer.
- Greater lock-in if W&B's run structure becomes the record of truth.
- Any cloud synchronization would violate project intent unless separately approved; it must be disabled, not merely unused.

**Interactions**

Conflicts with the D3 24 GB simplicity goal if a local server/container runs during training. Viable only when canonical JSONL remains authoritative.

## 5.4 Option C — MLflow local tracking server

**Mechanical surface**

Proposed command shape:

```bash
mlflow server \
  --host 127.0.0.1 --port 5000 \
  --backend-store-uri sqlite:///runs/_tracking/mlflow.db \
  --default-artifact-root ./runs/_tracking/artifacts
```

The owner opens `http://127.0.0.1:5000`. [W-TRK-05] [W-TRK-06]

**Strengths**

- Local experiment database, parameters, metrics, artifacts, and comparisons.
- Framework-neutral.
- Better structured querying than TensorBoard.

**Weaknesses**

- Requires a server process, SQLite/database lifecycle, and a distinction between run-local artifacts and global tracking storage.
- More ways for a non-expert to encounter port, process, path, or database issues.
- Duplicates parts of the proposed run manifest/artifact index.

**Interactions**

Framework-neutral but increases D4 backup/migration responsibilities. Better suited if the project later has many experiments and needs queries, not as the first-run minimum.

## 5.5 Option D — No dashboard: terminal + JSONL/CSV + generated static report

**Mechanical surface**

```bash
./trainex monitor --run runs/my-first-run
./trainex report --run runs/my-first-run
```

The second command writes `summary.md` and static plots under `reports/`.

**Strengths**

- Lowest runtime overhead and dependency count.
- Maximum durability and portability.
- Easy to inspect and recover after a crash.

**Weaknesses**

- Less effective for spotting trends during a long run.
- The project must implement plotting/comparison scripts.
- A non-expert loses a familiar interactive view.

## 5.6 Suggested default

**Suggested default: canonical JSONL/CSV + terminal-first monitoring + TensorBoard as an optional local view.**

TensorBoard should be a replaceable adapter, not the data model. `./trainex monitor` should print the exact local URL, current run state, last checkpoint, stage/phase, last five losses, and any warning. It should continue to work when TensorBoard is not running.

**Door classification — D2 suggested default: TWO-WAY DOOR.** A tracker adapter is cheap to replace if neutral metrics and artifacts remain canonical. Making any tracker database the sole record would convert this into a one-way door.

# 6. D3 — Compute utilization and data ingestion under 24 GB unified memory

## 6.1 The governing constraint

“Unified memory” removes a physical CPU-RAM/GPU-VRAM copy boundary; it does not create extra capacity. The following coexist in the same 24 GB pool:

```text
macOS and foreground applications
+ HDF5 chunk/decompression cache
+ Python/NumPy objects and loader queues
+ model parameters
+ optimizer state and L-BFGS history
+ activations and first-/second-derivative autodiff graph
+ collocation candidate/residual arrays
+ tracker buffers
+ checkpoint serialization buffers
+ safety margin
```

The right objective is **stable end-to-end step throughput below memory pressure**, not maximum simultaneous CPU and GPU percentages. CPU-side parsing/decompression and GPU compute can overlap, but excessive workers/prefetch create duplicate buffers in the same shared pool.

The authoritative data spec makes chunked/compressed HDF5 the canonical source and supports partial reads. h5py documents that chunking enables block reads and compression, and warns that chunk shape determines read amplification. [P-CTL] [W-DATA-01]

## 6.2 Required project measurements

The in-memory-versus-streaming choice cannot be made from trajectory count alone. Before numeric cache limits are chosen, the project must supply or measure:

| Symbol | Required number | How to obtain it |
|---|---|---|
| `M_OS_idle` | memory used by macOS and required foreground processes before training | Activity Monitor / scripted system snapshot |
| `S_HDF5_file` | compressed on-disk HDF5 bytes | filesystem stat |
| `S_HDF5_logical` | uncompressed logical bytes for all datasets | sum of HDF5 `Dataset.nbytes` plus object overhead estimate |
| `S_stage[k]` | admitted logical bytes and snapshot counts reachable at each curriculum stage, including replay/lookahead | scan stage manifests after admission |
| `M_model` | parameter and persistent model-buffer bytes at chosen dtype | framework model inventory |
| `M_Adam` | Adam state bytes | measured after one initialized step |
| `M_LBFGS(h)` | L-BFGS history/state bytes for history size `h` | measured; compare with framework formula/documentation |
| `M_AD_peak(B,C,dtype)` | peak forward/backward allocation for data batch `B` and collocation set `C` | representative dry step using exact five-term loss and second derivatives |
| `M_pool` | adaptive-collocation candidate pool and residual-score bytes | candidate shape × dtype plus overhead |
| `M_prefetch(w,q)` | loader-worker and queue memory for workers `w`, queue depth `q` | measured by Doctor benchmark |
| `C_ckpt` | serialized recovery-checkpoint bytes and temporary write peak | write/checksum test checkpoint |
| `D_free` | free disk available for data, checkpoints, diagnostics, and TensorBoard events | filesystem stat |

The memory feasibility inequality is:

```text
M_OS_idle
+ M_model
+ max(M_Adam, M_LBFGS)
+ M_AD_peak
+ M_pool
+ M_prefetch
+ M_cache
+ M_tracker
+ M_checkpoint_write_peak
+ M_safety
<= 24 GB
```

`M_safety` is not chosen in this round. R1b and empirical Doctor runs should set the operational reserve. A green Activity Monitor pressure graph is evidence; “all 24 GB allocated without a crash” is not a safe design target. Apple documents memory pressure as a combined indicator of RAM, compression, swap, and usage, and provides GPU History for activity inspection. [W-MAC-01] [W-MAC-02]

## 6.3 Option A — Load the admitted training set fully into memory

**Mechanical surface**

```yaml
data:
  access_mode: in_memory
```

`./trainex doctor` prints the measured dataset bytes, predicted peak, and pass/fail. Launch refuses the mode if the measured budget is not met.

**Strengths**

- Simplest training-time reads and deterministic access latency.
- Avoids repeated HDF5 decompression and filesystem activity.
- Useful for a small stage or a deliberately reduced qualification run.

**Weaknesses**

- The dataset is not the only large object. Second-order autodiff, L-BFGS history, and adaptive candidate pools can dominate or spike later.
- Curriculum replay grows the reachable set; a mode that fits Stage 0 may fail at Stage 5.
- Loading float64 canonical arrays and then creating float32 framework arrays can briefly duplicate data.
- Leaves little room for checkpoint serialization and the operating system.

**Downstream implications**

D4 needs a stricter pre-check before checkpointing. D5 adaptive sampling is constrained by remaining memory. The mode is not safe as a fixed first-run assumption without measurements.

## 6.4 Option B — Pure streaming with a small fixed prefetch queue

**Mechanical surface**

```yaml
data:
  access_mode: streaming
  cache_limit: none
  prefetch_batches: <resolved by Doctor>
  loader_workers: <resolved by Doctor>
```

The terminal shows `read_ms`, `decode_ms`, `compute_ms`, queue depth, and HDF5 cache use.

**Strengths**

- Most predictable dataset memory.
- Scales to every stage regardless of total dataset size.
- Keeps pressure available for autodiff and optimizer state.
- Failures are easier to diagnose because cache behavior is minimal.

**Weaknesses**

- Repeated replay trajectories may be decompressed many times.
- Storage/chunk-layout mismatch can make small random reads expensive.
- Too few workers may leave the GPU idle; too many can duplicate buffers and hurt throughput.

**Downstream implications**

Requires the data adapter to expose trajectory/group reads and keep batches fixed-shape. D6 must record deterministic ordering independently of I/O completion order.

## 6.5 Option C — Streaming with a bounded stage-local adaptive cache

**Mechanical surface**

```yaml
data:
  access_mode: bounded_cache
  cache_budget_bytes: <Doctor result>
  prefetch_batches: <Doctor result>
  loader_workers: <Doctor result>
  eviction: deterministic_lru
```

The adapter streams from HDF5 but retains repeatedly used trajectory chunks up to a hard byte limit. The cache is emptied or re-budgeted at optimizer/stage events when memory demands change. The status line includes cache bytes, hit rate, read time, compute time, and peak framework allocation.

**Strengths**

- Preserves a hard memory bound while exploiting curriculum replay locality.
- Can use a smaller cache during L-BFGS/adaptive residual scans than during ordinary Adam batches.
- Works with the canonical HDF5 partial-read contract.
- Avoids committing the pipeline to a guessed dataset-size threshold.

**Weaknesses**

- More implementation and test work than pure streaming.
- Cache keys must include data/schema/transform identity; stale transformed data must never survive a version change.
- A cache can obscure bad HDF5 chunking unless cold-cache timings are logged.

**Downstream implications**

The cache needs an explicit interface and telemetry in the data subsystem. It should not be included in scientific checkpoints; only deterministic data/sampler state and cache policy belong there, because cache contents are performance state, not training state.

## 6.6 Framework-specific utilization notes

### PyTorch MPS

- Keep model and active tensors on one MPS device; CPU prepares/indexes/decompresses data.
- Use MPS allocator telemetry such as current/driver/peak allocation and recommended maximum memory in Doctor and status output. [W-PY-06]
- Disable silent MPS fallback in production.
- Benchmark `loader_workers = 0, 1, 2, …` rather than assuming 16 CPU cores should all be used. HDF5 process/thread safety, decompression, Python object duplication, and queueing determine the optimum.
- Do not enable mixed precision merely to reduce memory until the second-derivative and conservation-loss accuracy implications are separately adjudicated.

### MLX

- Arrays share the unified pool and need no ordinary explicit transfer. [W-MLX-04]
- Use MLX active/peak/cache memory APIs and an explicit memory/cache limit. [W-MLX-06]
- Lazy execution requires synchronization at timing boundaries; otherwise logged “compute time” can be misleading.

### JAX Metal

- Keep stage and batch shapes stable to avoid repeated compilation.
- Treat compilation cache and executable memory as part of the measured peak.
- Because the plug-in is experimental, any unsupported primitive or compilation failure is a preflight blocker rather than a reason to silently switch devices mid-run. [W-JAX-02]

## 6.7 Suggested default

**Suggested default: Option C, chunked HDF5 streaming with a hard-bounded stage-local cache and a small empirically selected prefetch pipeline.**

`./trainex doctor` should run cold- and warm-cache microbenchmarks over candidate worker counts, record the selected values in `resolved-config.yaml`, and reject any setting whose representative peak reaches the operational reserve. The user should not manually chase CPU/GPU utilization percentages. They should see one verdict: `input pipeline healthy`, `I/O-bound`, or `memory budget failed`, with the measurements underneath.

**Door classification — D3 suggested default: ONE-WAY DOOR.** Designing the adapter to support bounded streaming and partial reads is architectural and expensive to retrofit. Cache bytes, worker count, and prefetch depth remain cheap configuration changes.

# 7. D4 — Checkpoint/resume, unattended guards, and failure diagnostics

## 7.1 State that must be recoverable

The baseline's checkpoint content is necessary but incomplete for this project. A recovery checkpoint must represent a **training transaction**, not just model weights. The minimum logical state is:

- model parameters and persistent buffers;
- optimizer identity and complete optimizer state;
- learning-rate scheduler state;
- global step/epoch, stage, optimizer phase, and phase-local counters;
- five-term loss-weight schedule state, including warm/frozen position;
- gradient-clipping state/history used by the Adam policy;
- L-BFGS history and line-search state when the selected implementation supports mid-phase recovery;
- sampler, trajectory iterator, replay/lookahead, and collocation-strategy state;
- root seed and framework/CPU/MPS random states or explicit keys;
- last committed stage-transition journal position;
- resolved-config hash;
- dataset schema/content manifest hash, admission manifest hash, and split manifest hash;
- software/checkpoint schema versions; and
- the exact device/dtype policy expected on resume.

Performance-only cache contents should not be checkpointed. They can be rebuilt from the deterministic manifests.

## 7.2 Option A — Step-count cadence, latest-only retention

**Mechanical surface**

```yaml
checkpoint:
  every_steps: 1000
  keep_latest: 1
```

The owner resumes from `latest.pt`.

**Strengths**

- Simple and close to the baseline.
- Easy disk accounting.

**Weaknesses**

- Recovery exposure varies drastically with step time. One thousand fast Adam steps and one thousand L-BFGS closure evaluations are not comparable.
- Latest-only retention provides no fallback if the newest file or newest state is bad.
- A single `latest.pt` is ambiguous: recovery state, best model, final model, and deployment export are different concepts.
- Step cadence misses important events such as stage promotion, optimizer handoff, anomaly, and clean interrupt.

**Downstream implications**

Unsafe for D7 transactional promotion and weak for unattended operation.

## 7.3 Option B — Wall-clock cadence plus stage checkpoints

**Mechanical surface**

```yaml
checkpoint:
  every_minutes: <from acceptable lost-work budget>
  on_stage_boundary: true
  keep_recovery: 2
```

**Strengths**

- Bounds lost wall-clock work even when step cost changes by phase.
- Stage checkpoints align with curriculum semantics.
- Easy for the owner to understand: “at most approximately this much work is lost.”

**Weaknesses**

- A long single L-BFGS closure or residual scan can exceed the interval.
- Does not cap lost steps during unusually fast phases.
- Still needs event checkpoints for optimizer handoff, anomaly, and clean stop.

## 7.4 Option C — Hybrid wall-clock + event + maximum-step gap

**Mechanical surface**

```yaml
checkpoint:
  max_elapsed: <T_ckpt>
  max_step_gap: <N_ckpt>
  events:
    - clean_interrupt
    - optimizer_phase_start
    - optimizer_phase_complete
    - stage_prepared
    - stage_committed
    - anomaly_when_safe
  retention:
    recovery_generations: 2
    keep_all_stage_boundaries: true
    evaluated_exports: 2
```

The owner does not provide arbitrary values blindly. The configuration resolver needs:

- acceptable maximum lost work `R_max`;
- measured checkpoint write/checksum time `t_write`;
- measured checkpoint bytes `C_ckpt`;
- available checkpoint disk budget `D_ckpt`; and
- representative step-time distributions by optimizer phase from qualification runs/R1b.

It then selects `T_ckpt <= R_max`, checks checkpoint overhead, and ensures the retention plan fits disk. `N_ckpt` is a secondary cap, not the sole policy.

**Strengths**

- Handles changing phase costs and semantically important events.
- Supports a precise D7 transaction.
- Keeps two recent recovery generations and immutable stage history.
- Cleanly separates recovery from evaluated/exported models.

**Weaknesses**

- Requires an event model and checkpoint index.
- Mid-L-BFGS exact resume may be unavailable or unsafe depending on the selected implementation; the policy must state the nearest safe boundary.
- More files than the baseline.

## 7.5 Corruption-safe write protocol

The suggested protocol is the same for every framework:

1. serialize to a unique temporary file in the **same directory/filesystem** as the final file;
2. flush user-space buffers;
3. `fsync` the file;
4. close it;
5. compute and store a cryptographic checksum;
6. atomically replace/rename the final immutable checkpoint name;
7. `fsync` the containing directory where supported;
8. validate that the file can be reopened and its manifest/checksum read;
9. atomically update `checkpoints/index.json` and `latest-good.json` to point to the immutable file;
10. only then delete an expired generation.

Python documents `os.replace` and `os.fsync`; POSIX specifies atomic replacement semantics for rename on the same filesystem. [W-IO-01] [W-IO-02] This protects against a process dying during the write; it does not protect against storage failure, so checksums and generations remain necessary.

Suggested paths under the D1 PyTorch default:

```text
checkpoints/
  index.json
  latest-good.json
  recovery/
    recovery-s02-adam-step00042000-<id>.pt
    recovery-s02-adam-step00043000-<id>.pt
  stages/
    stage-02-complete-<id>.pt
    stage-03-start-<id>.pt
exports/
  candidate-stage06-final/
    model-state.pt
    export-manifest.json
```

A recovery `.pt` contains optimizer and run state. An export is selected for evaluation/inference and does not masquerade as resumable training state.

## 7.6 Unattended-run guard menu

### Guard level 0 — operator only

The trainer logs warnings; the user decides whether to press Ctrl-C. This is the baseline pattern.

**Trade-off:** minimal code, but it contradicts the premise of unattended multi-hour runs.

### Guard level 1 — invariant hard stops

The trainer automatically stops on conditions that are unambiguously invalid, independent of a scientific threshold:

- non-finite total or component loss;
- non-finite gradient;
- non-finite parameter after an update;
- data-admission assertion failure or unexpected record key;
- checkpoint serialization/checksum/reopen failure;
- insufficient disk to complete the next atomic checkpoint and diagnostic bundle;
- framework allocator failure; or
- unhandled exception.

Action: stop updates, preserve the last known-good immutable checkpoint, attempt an anomaly checkpoint only when the state is finite and serializable, write the diagnostic bundle, set `status.json` to a specific failure code, and print one resume/help command.

### Guard level 2 — trend/pressure stops

Adds loss-explosion, sustained memory-pressure, swap-growth, thermal, and liveness thresholds.

**Trade-off:** useful, but the signal definitions and thresholds are an R1b consolidation dependency. This document specifies the hook and action, not invented numbers.

### Guard level 3 — automatic restart or hyperparameter mutation

The trainer rolls back, changes learning rate/batch size, and restarts without the owner.

**Trade-off:** not suggested. It changes the experiment, complicates provenance, can loop repeatedly, and risks hiding a scientific failure. Any later version would need a separately approved policy and a new run identity for each mutation.

## 7.7 Suggested guard behavior

Use level 1 from the first implementation and build level-2 hooks with thresholds disabled until R1b consolidation. On a soft threshold, the safest default action is **checkpoint and stop**, not restart or modify training. `SIGINT`/Ctrl-C should request a clean checkpoint at the next safe boundary; a second Ctrl-C may force exit and should be documented by R1b.

The disk guard should be formula-based. At minimum, free space before a write must cover the temporary file, retained final file, index/diagnostic writes, and a reserve. The exact reserve depends on measured `C_ckpt`; it must not be a guessed fixed number.

## 7.8 On-failure diagnostic bundle

Every abnormal termination should create one directory such as:

```text
diagnostics/failure-20260619T231455Z-<id>/
  README.md
  failure.json
  traceback.txt
  last-log-lines.txt
  resolved-config.yaml
  config-hash.txt
  run-manifest.json
  environment.txt
  packages.txt
  hardware-device.json
  memory-snapshot.json
  checkpoint-index.json
  checkpoint-validation.txt
  stage-journal-tail.jsonl
  sampler-collocation-state-summary.json
  data-admission-summary.json
  recent-record-keys.txt
  resume-command.txt
```

`failure.json` contains the failure code, time, stage, phase, global/phase step, last finite losses and weights, last checkpoint ID/checksum, device/dtype, framework versions, and whether an anomaly checkpoint was attempted. It should not copy raw trajectories or secrets. `README.md` begins with: “Attach this directory when asking for help.”

## 7.9 Suggested default

**Suggested default: Option C, transactional hybrid checkpoints; level-1 invariant hard stops; dormant level-2 hooks awaiting R1b thresholds; no automatic restart; standard diagnostic bundle.**

Retain two recent recovery generations, every stage-complete/stage-start checkpoint, and up to two evaluated candidate exports unless measured disk budgeting requires a different number. The counts are revisitable; transactional semantics and state completeness are not.

**Door classification — D4 suggested default: ONE-WAY DOOR for the recovery schema and transaction semantics.** Old checkpoints and reproducibility depend on them. Cadence, retention counts, and soft thresholds are two-way configuration choices inside that structure.

# 8. D5 — Training-loop skeleton capabilities

## 8.1 Why the baseline inner loop is structurally insufficient

A simple “load batch → forward → loss → backward → optimizer step” loop is only the Adam portion of the required trainer. The authoritative specs require:

- an outer curriculum stage state machine;
- Adam with scheduled loss weights and clipping;
- a handoff to full-batch L-BFGS or later-stage sL-BFGS with frozen weights and no clipping;
- closures/line search and possibly repeated loss evaluations at unchanged parameters;
- replay/lookahead data composition;
- collocation candidate generation, scoring, and refresh if adaptive sampling is selected;
- stage resets and loss re-warm; and
- checkpoints at safe phase/stage boundaries. [P-CTL] [P-ARCH]

An Adam-only skeleton is therefore **not a viable option against the current authoritative specs**. It is screened out rather than offered as a menu choice.

## 8.2 Capability interfaces the choice concerns

A sufficient skeleton needs narrow concepts—not a generic framework:

```text
CurriculumController
  -> StageRuntime
       -> OptimizerPhase (Adam | full-batch L-BFGS | sL-BFGS)
       -> DataPlan (replay | lookahead | split identities)
       -> CollocationStrategy
       -> LossWeightSchedule
       -> EventSink / CheckpointCoordinator
```

An optimizer phase must define at least:

```text
initialize(stage_state)
step_or_closure(batch_or_full_set)
state_dict()/load_state_dict()
safe_checkpoint_boundary()
termination_reason()
reset_policy_at_stage_boundary()
```

A collocation strategy must define:

```text
generate_candidate_pool(key, stage)
score_residuals(model, candidates)
select_active_points(scores, key)
refresh_if_due(event)
state_dict()/load_state_dict()
```

The loss machinery must keep a locked five-term catalogue, expose current scalar weights, support schedule/freeze/re-warm events, and log weighted and unweighted values separately. It must not permit a config to silently remove a locked term.

## 8.3 Option A — Dedicated fixed two-phase loop

The code contains explicit, separate functions for Adam and L-BFGS and hard-coded collocation behavior.

**Mechanical surface**

The user sees phase lines such as:

```text
stage=2 phase=adam ...
stage=2 event=handoff_to_lbfgs
stage=2 phase=lbfgs ...
```

Configuration exposes only values supported by the fixed implementation.

**Strengths**

- Easiest code to read initially.
- Directly expresses the current locked Adam → L-BFGS flow.
- Fewer interfaces and fewer configuration errors.

**Weaknesses**

- Full-batch and stochastic L-BFGS have substantially different data/state semantics; hard-coding both tends to produce conditionals throughout the loop.
- Residual-based adaptive collocation is expensive to retrofit if the loop only knows “next batch.”
- New phase-local checkpoints, loss schedules, or R2 optimizer variants require edits to central control flow.
- Framework tests become entangled with curriculum tests.

**Downstream implications**

Acceptable for a short prototype, but likely to create rework before later stages and R2.

## 8.4 Option B — Small pluggable phase/collocation/loss state machine

The loop owns explicit stage and phase transitions, while optimizers, collocation, and loss schedules implement narrow project interfaces.

**Mechanical surface**

The owner still uses one launch command. `resolved-config.yaml` identifies each phase implementation:

```yaml
training:
  phases:
    - adam
    - lbfgs_by_stage
collocation:
  strategy: <uniform-or-adaptive-profile>
loss:
  schedule: phys05
```

`status.json` always reports `stage`, `phase`, `phase_step`, and `next_safe_checkpoint`.

**Strengths**

- Expresses the locked optimizer phases without framework-generic abstraction.
- Lets R2 tune or replace a phase inside a stable lifecycle.
- Makes full-batch closure behavior, sL-BFGS minibatch/curvature behavior, and Adam steps separate, testable adapters.
- Adaptive collocation can be added behind the strategy interface without changing checkpoint/event semantics.
- Loss scheduling becomes explicit state rather than ad hoc arithmetic in the loop.
- D4 and D7 receive clear safe boundaries and serializable state.

**Weaknesses**

- More initial design/test work.
- Interfaces must remain narrow; otherwise the project creates a framework within a framework.
- A plugin name is not proof of scientific validity. Each implementation still needs acceptance tests.

## 8.5 Option C — General declarative execution graph/callback framework

Every event, optimizer, sampler, metric, and stage transition is configured as a generic graph or callback set.

**Mechanical surface**

The config becomes a detailed execution program. A GUI or schema browser may be needed to understand it.

**Strengths**

- Maximum extensibility and reuse.
- Easy to insert experimental hooks without editing a central loop.

**Weaknesses**

- Over-engineered for one model, one machine, and one maintainer.
- Debugging control flow becomes harder than reading explicit Python.
- Callback ordering and hidden state are common failure sources.
- It weakens the project's “plain language, mechanical surface” goal.

## 8.6 Optimizer-family feasibility by D1 candidate

| Framework | Adam | Full-batch L-BFGS | Later-stage sL-BFGS | Structural consequence |
|---|---|---|---|---|
| PyTorch | Native | Native closure-based optimizer; high memory; one device | **Not specified by PyTorch or project spec** | Adapter can wrap built-in full L-BFGS; sL-BFGS remains a blocker |
| MLX | Native | No official optimizer in the 0.31.2 catalogue | Not official | Both quasi-Newton phases become project/external code |
| JAX + Optax | Native | Optax L-BFGS/line-search components | Project-specific | Functional adapter is viable; Apple Metal maturity remains D1 risk |

Sources: [W-PY-07] [W-MLX-05] [W-JAX-04]. “Stochastic L-BFGS” must not be implemented by feeding arbitrary minibatches to a deterministic full-batch L-BFGS optimizer and retaining curvature history. The project must choose a specific algorithm and its curvature-pair validity, sampling, line-search/trust-region, reset, and checkpoint semantics.

## 8.7 Collocation capability menu inside the skeleton

### Fixed uniform points only

Smallest implementation. Viable only if the scientific sampling choice remains fixed. Retrofitting residual-based adaptation requires candidate-pool evaluation, score storage, selection, refresh events, RNG state, and checkpointing.

### Resampling interface without adaptive scoring

The loop supports replacing a point set at events, but initially uses uniform/quasi-random generation. This preserves shape and checkpoint hooks with moderate cost.

### Full candidate-pool/residual-selection capability

The loop supports periodic residual scoring over a candidate pool and deterministic selection. Highest initial complexity and memory pressure, but no structural retrofit if R2 selects residual-based adaptive refinement.

The suggested Option B skeleton should implement the **interface and state contract** now, with a simple strategy initially. It does not need to implement every adaptive algorithm in R1a.

## 8.8 Loss-weighting capability menu inside the skeleton

### Static scalars

Incompatible with the locked warm/freeze/re-warm semantics unless those schedules are hard-coded elsewhere.

### Named schedule object

Each loss term has a value from a stage/phase-aware schedule; the object can freeze during L-BFGS and re-warm at stage start. This is sufficient and testable.

### Fully adaptive balancing hooks

Allows gradient-norm or uncertainty-based rebalancing. It is structurally possible but scientifically out of scope and can conflict with the locked PHYS-05 schedule. Keep as a disabled future adapter, not an active default.

## 8.9 Suggested default

**Suggested default: Option B—a small, explicit stage/phase state machine with optimizer-phase, collocation-strategy, and named loss-schedule interfaces.**

Build supported adapters for Adam and the chosen framework's full-batch L-BFGS. Build the lifecycle/checkpoint slot for sL-BFGS, but fail preflight for any run that reaches a stage requiring it until the project selects and validates a concrete implementation. Build a collocation strategy interface and checkpointable refresh state; start with the spec-approved simple strategy and let R2 supply numeric density/refresh choices. Implement the locked five-term loss catalogue and PHYS-05 schedule/freeze/re-warm mechanism from day one.

**Door classification — D5 suggested default: ONE-WAY DOOR.** Loop lifecycle, closure semantics, event ordering, and checkpointable state shape are expensive to retrofit after model and run artifacts depend on them. Individual optimizers and sampling strategies are replaceable inside the interface.

# 9. D6 — Reproducibility and determinism

## 9.1 What can and cannot be promised

A saved seed is not the same as a deterministic run. Sources of variation include backend kernels, parallel reductions, operation ordering, framework releases, OS/Metal changes, loader concurrency, and adaptive selection ties. PyTorch explicitly warns that completely reproducible results are not guaranteed across releases, commits, platforms, or CPU/GPU execution, and that deterministic algorithms can reduce performance. [W-PY-08]

The honest contract should distinguish:

- **exact state recovery:** restoring all recorded state at a checkpoint;
- **same-build replay:** rerunning from the beginning under an identical environment;
- **cross-build reproduction:** rerunning on a later framework/macOS version; and
- **scientific replication:** obtaining materially consistent conclusions across seeds/runs.

Exact checkpoint state is required. Bitwise identity on an Apple accelerator is not promised unless the exact workload proves it.

## 9.2 Option A — Seeded best effort on the accelerator

**Mechanical surface**

```yaml
reproducibility:
  mode: seeded
  root_seed: 20260619
```

The run saves the root seed, split manifest, and framework state.

**Strengths**

- Lowest performance cost.
- Simple for the owner.
- Usually sufficient to reconstruct data ordering and diagnose major differences.

**Weaknesses**

- A single seed can create false confidence.
- Without separate random streams, adding one random operation changes all downstream draws.
- “Run A beat run B” may be noise.
- It does not test whether an operation is nondeterministic.

## 9.3 Option B — Strict deterministic mode for every scientific run

**Mechanical surface**

The framework is configured to reject known nondeterministic operations, loaders are serialized or tightly controlled, and compilation/device options are frozen.

**Strengths**

- Easier debugging and exact comparisons when supported.
- Fail-fast behavior exposes unsupported deterministic paths.

**Weaknesses**

- May be unavailable for some MPS/Metal operations.
- Can be substantially slower.
- Still cannot promise equality across framework or OS releases.
- Forcing CPU execution solely for determinism can change the performance/precision experiment being studied.

## 9.4 Option C — Two-tier reproducibility policy

### Tier 1: deterministic acceptance/regression lane

Run small CPU tests in the required precision with deterministic algorithms where available:

- architecture scaling and COM invariance;
- componentwise first/second derivative analytic test;
- force/energy consistency;
- finite five-term loss and parameter gradients;
- one-step optimizer tests;
- checkpoint round-trip and stage-transaction tests;
- fixed-manifest data/sampler/collocation tests.

These are not performance runs. Their purpose is to detect code changes.

### Tier 2: provenance-complete accelerator production lane

For MPS/Metal training:

- record exact environment, OS, framework, device, dtype, fallback flags, and resolved config;
- use a root seed expanded through a stable keyed derivation into distinct streams for model initialization, split, batch order, data-time sampling, collocation generation/selection, lookahead, and any optimizer randomness;
- store the split/admission manifests rather than expecting a seed to regenerate future data-pipeline behavior;
- save all random states/keys at checkpoints;
- provide an optional `audit` mode that asks the framework to reject nondeterministic operations and reports unsupported ones;
- treat consequential run comparisons as paired multi-seed comparisons using the same seed set and manifests.

**Mechanical surface**

```yaml
reproducibility:
  mode: production_seeded   # or audit
  root_seed: 20260619
  comparison_group: null
```

For confirmation:

```bash
./trainex compare \
  --runs runs/variant-a-seed-* runs/variant-b-seed-* \
  --paired-by seed
```

The report shows every seed, median, range, failures, and stage reached. It never reports only the best seed.

## 9.5 Framework-specific notes

### PyTorch

- Seed Python, NumPy, CPU torch, and MPS state; save CPU and MPS RNG state in checkpoints. [W-PY-06]
- `torch.use_deterministic_algorithms(True)` is an audit tool, not a guarantee that every desired MPS operation has an implementation. [W-PY-08]
- Disable MPS fallback in production so a run cannot silently change execution path.

### MLX

- Use explicit random keys/splitting where possible and save them with the run state.
- No sufficiently comprehensive primary-source MLX Metal determinism contract was found for this exact workload; record this as an open validation item rather than claiming determinism.

### JAX

- Explicit PRNG keys are a major strength and should be threaded through data/collocation code.
- The experimental Metal plug-in's incomplete test status prevents a broad determinism claim. [W-JAX-02]

## 9.6 Comparison protocol

A non-expert runbook should say:

> One run can show that a configuration executes. One run does not establish that it is better. Use the same split and paired seed set for both configurations; compare validation/test metrics, failures, and stage progression across the set.

**Suggested operational floor:** three paired seeds for a consequential A/B decision, reported as all values plus median and range. This is a minimum engineering check, not a statistical confidence guarantee. R1b's duration/feasibility findings may require a different confirmatory count, which should then be written into a versioned comparison protocol.

## 9.7 Suggested default

**Suggested default: Option C, deterministic CPU acceptance tests plus provenance-complete seeded accelerator runs and paired multi-seed confirmation for consequential comparisons.**

**Door classification — D6 suggested default: ONE-WAY DOOR for seed partitioning, manifests, and provenance schema.** Those determine whether old runs can be understood. The strictness mode and confirmatory seed count are two-way policy settings.

# 10. D7 — Curriculum stage-boundary mechanics

## 10.1 State transition that must be represented

A promotion is not an assignment such as `stage += 1`. It changes:

- admitted/replay/lookahead data manifests;
- optimizer phase and optimizer state;
- learning-rate scheduler;
- loss-weight schedule and maxima;
- collocation population/refresh state;
- random streams and counters; and
- the meaning of subsequent checkpoints and metrics.

The authoritative spec requires model-weight carry, complete Adam state reset, loss-weight re-warm, and a checkpoint after each stage. [P-CTL]

## 10.2 Option A — Checkpoint then mutate stage in place

**Mechanical surface**

The trainer writes `stage-02.pt`, changes `stage=3`, resets selected objects, and continues.

**Strengths**

- Simple implementation.
- Gives a pre-promotion checkpoint.

**Weaknesses**

- A crash between individual mutations can leave a checkpoint/status/config combination that disagrees.
- Resume code must infer whether the promotion completed.
- It is easy to accidentally retain an Adam moment, scheduler counter, loss warmup index, or old sampler state.
- Rollback intent is not recorded.

## 10.3 Option B — Transactional prepared/committed promotion with manual rollback

**Mechanical surface**

At promotion the terminal shows:

```text
stage=2 event=promotion_preparing target=3
checkpoint=stage-02-complete-<id> verified=yes
stage_journal=PREPARED source=<hash> target=3
checkpoint=stage-03-start-<id> verified=yes
stage_journal=COMMITTED stage=3
```

The run directory contains an append-only stage journal and immutable source/start checkpoints.

**Transition protocol**

1. Evaluate the authoritative promotion rule and save its evidence; the execution layer does not invent or modify the rule.
2. Finish/close the current optimizer phase at a defined safe point.
3. Write and verify immutable `stage-k-complete` recovery state.
4. Append/atomically publish a `PREPARED` journal record containing source checkpoint hash, target stage, promotion evidence hash, and target data-plan hash.
5. Construct target state:
   - carry model parameters/buffers;
   - create a **new** Adam optimizer and scheduler with no moment/state carry;
   - discard prior L-BFGS history;
   - initialize the new stage's loss schedule at re-warm position;
   - bind the new replay/lookahead/admission/split manifests;
   - initialize/reseed the target collocation strategy from recorded derived keys;
   - reset target phase counters while preserving global counters.
6. Write and verify immutable `stage-(k+1)-start` checkpoint.
7. Atomically append/publish `COMMITTED` with the new checkpoint hash.
8. Only after commit may ordinary updates in the new stage begin.

**Crash semantics**

- Crash before `PREPARED`: resume the last committed stage normally.
- `PREPARED` exists but no valid target-start checkpoint/commit: resume `stage-k-complete` and re-run the deterministic preparation.
- Valid target-start checkpoint and `COMMITTED`: resume the target stage.
- Ambiguous or checksum-invalid journal/checkpoint relation: stop with diagnostic bundle; never guess.

**Rollback**

The default is an operator decision:

```bash
./trainex rollback --run runs/<name> --to stage-02-complete-<id>
```

Rollback creates a **new branch/run identity** or a clearly recorded lineage event; it does not overwrite history.

**Strengths**

- Exact resume behavior across machine/process failure.
- Makes reset semantics testable.
- Gives an audit trail for stage comparisons.
- Integrates cleanly with D4.

**Weaknesses**

- Requires a journal schema and transaction tests.
- Creates at least two immutable artifacts per promotion.
- Manual rollback means the owner or runbook must interpret a post-promotion problem.

## 10.4 Option C — Transactional promotion with automatic rollback

Adds a post-promotion probation window. If a configured health signal fires, the trainer stops and automatically creates a rollback branch from the source stage checkpoint.

**Strengths**

- Useful for genuinely unattended runs.
- Can limit damage from an unstable transition.

**Weaknesses**

- The health signal and window are scientific/operational policy. Incorrect thresholds can reject valid hard-stage behavior.
- Automatic rollback can loop or hide a systematic issue.
- Continuing automatically changes the experiment and needs a new lineage/run identity.
- R1b owns the health-watchlist evidence needed to justify it.

## 10.5 Optimizer-state choices at a boundary

### Carry Adam moments

Not a viable default: it contradicts the CTL spec's explicit complete reset.

### Reset Adam and scheduler; carry only model weights

Required by the CTL spec and therefore part of every viable option.

### Partial reset

Technically possible in all frameworks by reconstructing or editing optimizer state, but it would be a scientific deviation from the authoritative framework and is not an R1a option.

For L-BFGS, a new stage begins in Adam, so old curvature history should not be applied to the new objective/data distribution. The stage-complete checkpoint may preserve old L-BFGS state for exact forensic recovery, while the stage-start checkpoint contains the newly initialized Adam state.

## 10.6 Suggested default

**Suggested default: Option B, transactional prepared/committed promotion with immutable stage-complete and stage-start checkpoints, mandatory optimizer/scheduler reset, loss re-warm, deterministic new data/collocation state, and manual rollback.**

Build the automatic-rollback hook but leave it disabled until R1b supplies validated signals and the project owner selects a policy. A post-promotion hard invariant failure still invokes D4's ordinary hard stop.

**Door classification — D7 suggested default: ONE-WAY DOOR.** Stage journal semantics, checkpoint lineage, and reset timing become embedded in every curriculum run. Whether rollback is manual or automatic is a later two-way policy choice once the transaction exists.

# 11. Baseline critique and explicit option-versus-baseline proposals

## 11.1 Overall assessment

The brainstorm baseline is useful as an operator-centered sketch. Its strongest decisions are:

- terminal-first launch/monitor/resume;
- one run directory as the unit a user can inspect and share;
- a thin data adapter isolating on-disk format;
- separate evaluation that consumes rather than mutates training state;
- frozen run configuration;
- clear error categories; and
- framework choice deferred to evidence.

Its central weakness is that a simple three-subsystem diagram and one plain training script do not represent the state-bearing mechanisms the authoritative specs now require. Environment is a substrate, while run state/artifacts are absent as a component even though they mediate configuration, reproducibility, checkpoint transactions, curriculum promotion, diagnostics, evaluation, and migration. The baseline also contains scientific/mechanical statements made obsolete or contradicted by the supplied framework specs.

The changes below are proposals, not silent replacements. Each has a “keep baseline” option in the final decision sheet.

## 11.2 Subsystem decomposition finding

The baseline cut is:

```text
Developer Environment
Data Ingestion
Training Loop
+ Verification consumer
```

The cleaner implementation cut is:

```text
0. Environment/toolchain substrate
1. Data access, admission, split, and stage-data planning
2. Training engine: model, five-term loss, optimizer phases, collocation, curriculum controller
3. Run-state and artifact store: config/provenance, checkpoints, journals, metrics, diagnostics, schema migration
4. Evaluation/verification consumer
```

This is not five user-facing programs. One CLI can orchestrate them. The separation follows state ownership:

- data code owns record identity/admission and emits deterministic plans;
- training code owns differentiable computation and transitions;
- artifact code owns durable transactions and provenance;
- evaluation reads an immutable candidate and writes evaluation artifacts.

### B1 — Add a first-class run-state/artifact subsystem

| | Baseline | Proposed change |
|---|---|---|
| Structure | Environment + ingestion + training; verification reads `runs/` | Environment substrate + data/admission + training engine + run-state/artifacts + evaluation consumer |
| User impact | None initially | Still one wrapper; clearer files/status/recovery |
| Benefit | Simpler diagram | Durable ownership for checkpoints, stage journal, manifests, diagnostics, migrations |
| Cost | — | One more internal boundary and schema |

**Rationale:** Checkpoint/resume and curriculum promotion are not incidental writes by a training loop; they are consistency transactions. Treating run state as a component avoids circular ownership and makes testing possible.

**Door classification — B1: ONE-WAY DOOR.** Component ownership determines interfaces, artifact schemas, and test architecture.

## 11.3 Plain-loop versus monolithic-script finding

The baseline is right to avoid a heavy trainer framework. It is not right to equate “plain Python” with “one large script.” The CTL engine has enough orthogonal state that a monolith will be harder for a non-expert to debug, not easier.

### B2 — Keep an explicit loop, replace the monolithic script with a thin orchestrator and narrow modules

| | Baseline | Proposed change |
|---|---|---|
| Code shape | One maintainable training script | One readable orchestrator calling data, loss, phase, collocation, checkpoint, tracker, and stage modules |
| User command | `python -m pinn.train ...` | One `./trainex launch ...` wrapper (or equivalent module command) |
| Debugging | Search one long file | Error names identify component; modules have acceptance tests |

**Rationale:** D5 needs closures, optimizer phase state, collocation refresh, loss schedules, and events. Explicit modules reduce branching while retaining visible control flow. Avoid generic callbacks/service containers.

**Door classification — B2: ONE-WAY DOOR.** Refactoring after a monolith accumulates checkpoint/event assumptions is expensive.

## 11.4 Placeholder-inventory finding

The baseline's PH-1…PH-10 list mixes three categories:

1. genuine trainex decisions (framework, compute use, tracking, checkpoint policy);
2. scientific contracts already owned by the framework specs (architecture, loss terms, curriculum); and
3. dependencies owned elsewhere (data split/format).

It also omits early-settling execution decisions now exposed by D1–D7:

- precision acceptance and device branch;
- deterministic/provenance policy;
- optimizer-phase loop shape and closure support;
- collocation lifecycle/state;
- stage-boundary transaction and rollback;
- guard/failure bundle;
- config composition and schema;
- artifact/checkpoint compatibility and migration;
- data admission identity versus sample filtering; and
- final-gate metric schema.

**Suggested inventory treatment:** retire PH-2/PH-3/PH-4 as “open trainex decisions”; replace them with implementation acceptance items pointing to `[P-CTL]`/`[P-ARCH]`. Map the remaining choices to D1–D7 and B1–B11. This is documentation housekeeping covered by B1/B2/B3/B4 rather than an additional architecture choice.

## 11.5 Configuration finding

The baseline commits one YAML per run. The CTL spec explicitly calls for three Hydra configuration levels: stage, optimizer, and loss. Both goals can coexist: one operator-facing recipe can compose authoritative profiles, then the run can freeze the fully resolved result.

### B3 — One operator recipe that composes stage/optimizer/loss profiles; freeze the resolved config

| | Baseline | Proposed change |
|---|---|---|
| Owner edits | One flat YAML | One short run recipe with Hydra defaults/profile references |
| Internal source | Same flat file | Separate versioned `stage/`, `opt/`, `loss/`, and execution profiles |
| Run artifact | Copy of input YAML | Input recipe + `resolved-config.yaml` + schema/version + hash |
| Resume comparison | “Same config file” | Compare immutable resolved scientific/execution fields and declared mutable resume fields |

Illustrative mechanical shape:

```yaml
# configs/runs/my-first-run.yaml
defaults:
  - stage: default
  - opt: first_run
  - loss: phys05
  - execution: macbook_24gb
  - _self_

run:
  name: my-first-run
precision:
  policy: accelerator_float32   # or cpu_float64
```

The names above are proposed mechanical names, not new scientific settings. Hydra supports defaults-list composition and can print the composed config for debugging. [W-CFG-01] [W-CFG-02]

**Rationale:** Preserves the non-expert “edit one file” surface while implementing the authoritative separation and avoiding duplicated stage/loss definitions across runs.

**Door classification — B3: ONE-WAY DOOR.** Config paths, override semantics, hashing, and old-run reproducibility become embedded in artifacts and commands.

## 11.6 Run-directory finding

The baseline `runs/<name>/` is worth keeping, but its claim that “everything needed” is present is not true with only config, checkpoints, logs, summary, and status. It lacks environment lock, data/split/admission identity, checkpoint index/checksums, stage journal, schema versions, diagnostics, and canonical metrics. It also calls `latest.pt` “the trained model,” conflating recovery and model selection.

### B4 — Version the run contract and separate recovery from export

| | Baseline | Proposed change |
|---|---|---|
| Recovery | `checkpoints/latest.pt` | Immutable indexed recovery checkpoints + atomic `latest-good.json` pointer |
| Model candidate | Same `latest.pt` | Separate `exports/<candidate>/model-state.pt` + manifest |
| Provenance | Frozen config | Resolved config, environment lock, hardware/device, code/build ID, data/split/admission manifests |
| Curriculum | Stage in checkpoint | Stage journal + stage-complete/start checkpoint pair |
| Metrics | log + JSONL | Canonical tracker-neutral metrics + optional dashboard files |
| Failure | Log | Standard diagnostic bundle |
| Compatibility | Implicit | `run_schema_version` and `checkpoint_schema_version` with migration/read policy |

Suggested contract:

```text
runs/<name>/
  manifest.json
  input-config.yaml
  resolved-config.yaml
  environment.lock.yml
  hardware-device.json
  data/
    dataset-manifest.json
    admission-manifest.json
    split-manifest.json
    stage-plans/
  checkpoints/
    index.json
    latest-good.json
    recovery/
    stages/
  stage-journal.jsonl
  metrics/
    events.jsonl
    scalars.csv
    tensorboard/
  logs/
    train.log
  diagnostics/
  exports/
  eval/
  status.json
  summary.md
```

**Rationale:** This makes the run directory a truthful reproduction/support unit and permits evaluation without loading optimizer state.

**Door classification — B4: ONE-WAY DOOR.** Artifact paths and schemas become long-lived external interfaces.

## 11.7 User-entry-point finding

The baseline says five entry points are the only user surfaces, yet later exposes a separate evaluator. It also lacks a preflight command despite backend/precision/data/memory uncertainty.

### B5 — Add explicit Doctor and Evaluate actions; retain one wrapper

| | Baseline | Proposed change |
|---|---|---|
| Workflow | Setup / Configure / Launch / Monitor / Resume | Setup / Configure / **Doctor** / Launch / Monitor / Resume / **Evaluate** |
| Preflight | Start run and encounter errors | Validate environment, data, derivatives, memory, checkpoint write, and config before launch |
| Evaluation | Separate script outside five-entry mental model | Named end step using the same wrapper/help/error conventions |

Proposed command surface:

```bash
./trainex setup
./trainex doctor --config configs/runs/my-first-run.yaml
./trainex launch --config configs/runs/my-first-run.yaml
./trainex monitor --run runs/my-first-run
./trainex resume --run runs/my-first-run
./trainex evaluate --run runs/my-first-run --candidate <id>
```

**Rationale:** A non-expert benefits from a single “is this machine/config ready?” verdict. Evaluation is already a real user action and should not be hidden from the mental model.

**Door classification — B5: TWO-WAY DOOR.** CLI aliases and workflow wording can change with compatibility wrappers; the preflight capability itself should remain.

## 11.8 Checkpoint-trigger finding

A fixed 1,000-step cadence does not bound lost work across Adam, full L-BFGS, sL-BFGS, residual scans, or stage transitions.

### B6 — Replace step-only cadence with hybrid elapsed-time, event, and optional step-gap triggers

**Keep baseline option:** `checkpoint_every: 1000`.  
**Change option:** D4 Option C, with exact intervals resolved from measured write cost and acceptable lost work.

**Rationale:** This is the only option that composes cleanly with changing phase costs and D7 stage transactions.

**Door classification — B6: TWO-WAY DOOR.** Trigger values/policy can change while preserving the checkpoint schema. Event support should be built early but is covered by B1/D4.

## 11.9 Quality-gate finding

The baseline states a final gate `ε_H > 10^-5`, shows `8.2e-6` failing that comparator, and then defines the same displayed energy error as “smaller is better; <10^-5 is excellent.” The framework documents also use closely related symbols for two different quantities:

- `[P-CTL]` defines per-trajectory `eps_H` as maximum relative energy drift and `SCS=log10(eps_H)` for **data admission**, where larger error is worse;
- `[P-ARCH]` defines `epsilon_H = 1e-4 * S_H` as a **denominator floor inside the training energy loss**; and
- `[P-BASE]` uses `ε_H` as a **final model quality metric** without an unambiguous canonical identifier/aggregation.

The hard constraint says the final metrics and thresholds are project-locked, so this research must not choose a comparator or rename the metric silently.

### B7 — Add a versioned, machine-readable quality-gate specification and block evaluation until the contradiction is adjudicated

| | Baseline | Proposed change |
|---|---|---|
| Gate definition | Prose and example | Versioned file consumed by evaluator and rendered by runbook |
| Metric identity | Display symbol | Unique `metric_id`, formula source, split, aggregation, units |
| Direction | Contradictory prose/comparator | Explicit comparator and threshold supplied by project adjudication |
| Change control | Implicit | Schema version and signed/hashed gate version in evaluation output |

Required shape, with unresolved values intentionally blank:

```yaml
gate_schema_version: 1
gate_id: <project-supplied>
metrics:
  - metric_id: <canonical-id-not-display-symbol>
    display_name: <project-supplied>
    formula_source: <file-and-section>
    dataset_split: test
    aggregation: <project-supplied>
    comparator: <project-supplied>
    threshold: <project-locked-value>
    units: dimensionless
```

**Rationale:** Prevents a reversed inequality, notation collision, or admission metric from being coded as a final quality gate. Thresholds remain untouched.

**Door classification — B7: ONE-WAY DOOR.** Evaluation results and milestone claims must remain interpretable under a stable metric/gate identity.

## 11.10 Data-validity finding

The baseline says non-finite “samples” are dropped at load time. The authoritative CTL data contract instead has a trajectory-level admission gate, blacklist/quarantine semantics, reason codes, and batch-time assertions. Silent point dropping can alter a trajectory, hide corruption, and invalidate stage manifests.

### B8 — Replace sample-level drop with strict trajectory admission/quarantine

| | Baseline | Proposed change |
|---|---|---|
| Invalid values | Drop sample, log count | Reject/quarantine trajectory by authoritative reason code before split/stage/statistics |
| Batch behavior | Continue after mutation | Assert every emitted record is admitted; no silent skip |
| Artifact | Aggregate count | Admission manifest with record key, result, reason, source hashes |

**Rationale:** Implements `[P-CTL]` and makes data identity reproducible.

**Door classification — B8: ONE-WAY DOOR.** Admission changes the training population, split identity, stage membership, statistics, and scientific comparability.

## 11.11 Loss/logging finding

The baseline repeatedly describes three losses. The authoritative specs define five default terms and scheduled weights.

### B9 — Replace the three-loss mechanical schema with the locked five-term catalogue

| | Baseline | Proposed change |
|---|---|---|
| Loss names | data / physics / IC | data / IC / causal physics / energy / angular momentum |
| Logging | three values + total | five unweighted terms, five weights, weighted terms, total, phase/freeze status |
| Config | generic weights | authoritative PHYS-05 schedule and stage maxima, resolved/frozen |
| Summary | three final losses | all five plus conservation diagnostics and schedule context |

**Rationale:** This is not a scientific redesign; it corrects the mechanical surface to the authoritative loss contract.

**Door classification — B9: ONE-WAY DOOR.** Metric keys and historical run comparison depend on stable names and meanings.

## 11.12 Operations-ownership finding

The baseline embeds numerical claims/actions such as target GPU percentages, “100% means the model is too small,” stop-on-any-growing-swap, thermal interpretation, `caffeinate`, and a 5–15 minute evaluation estimate. Those are runbook/operations questions and some are unsupported by the supplied evidence.

### B10 — Route operational thresholds and duration claims to R1b; keep raw telemetry and structural hooks here

| | Baseline | Proposed change |
|---|---|---|
| R1a owns | Fixed utilization/thermal/swap/run-time instructions | Telemetry fields, guard hooks, status categories, required measurements |
| R1b owns | Not separated | Thresholds, laptop sleep/lid/thermal procedure, intervention rules, feasible duration estimates |

**Rationale:** Prevents a design brainstorm from hard-coding unreliable operating advice. Activity Monitor remains a useful surface; percentage bands are not correctness gates.

**Door classification — B10: TWO-WAY DOOR.** Documentation ownership and thresholds can be revised without changing scientific artifacts, provided telemetry keys remain stable.

## 11.13 Data-version finding

The baseline requires a single `data_version_hash` to match the trainer's expected version. A content hash is useful, but one equality check conflates identity, schema compatibility, transforms, and split/admission population. It can reject a compatible rebuilt file or accept an identically labeled but semantically different transform if the convention is unclear.

### B11 — Replace one opaque equality check with structured data identity and compatibility checks

| | Baseline | Proposed change |
|---|---|---|
| Check | `data_version_hash == trainer_expected` | Validate schema version, dataset content/build manifest, transform metadata, admission manifest, and split/stage-plan hashes |
| Compatible change | Usually hard fail | Explicit compatibility matrix; any override is logged and creates a new run identity |
| Resume | Same version string | Exact manifest hashes for scientific state; schema reader may migrate metadata only under a tested policy |

**Rationale:** The canonical HDF5 spec already contains schema and transform metadata. Structured identity is more precise and supports future migrations without weakening reproducibility.

**Door classification — B11: ONE-WAY DOOR.** Data identity defines which observations a model saw and whether old runs can be resumed or compared.

## 11.14 Baseline commitments suggested to retain unchanged in intent

- **Thin adapter:** retain, expanded to admission/stage-plan interfaces.
- **Run directory as the handoff unit:** retain, upgraded by B4.
- **Terminal as primary monitor:** retain.
- **Local browser dashboard as secondary:** retain through D2.
- **Evaluator does not mutate training state:** retain.
- **Config-driven runs and frozen resolved config:** retain, composed by B3.
- **Miniforge/isolated arm64 environment:** retain as a practical setup option; exact Python/package pins belong in a generated lock and can be updated through qualification.
- **No cloud/distributed path:** retain as hard constraint.

# 12. Composed first-run recipe using all suggested defaults

This is a **proposed mechanical shape**, not a claim about existing repository commands. No codebase was provided. The implementation should preserve the command meanings even if the executable is ultimately `python -m pinn.trainex` rather than `./trainex`.

## 12.1 Pre-launch decisions that must be filled

The owner must select or receive adjudication for:

```text
PRECISION_POLICY = accelerator_float32 | cpu_float64
SLBFGS_IMPLEMENTATION = <named, validated algorithm/package or project implementation>
QUALITY_GATE_SPEC = <versioned canonical file>
```

A full Stage-0-through-Stage-6 scientific run must not start if any required later-stage optimizer is unresolved. The pipeline may run a clearly labeled qualification/smoke run whose maximum stage does not require unresolved machinery, but that is not a substitute for the first full scientific run.

## 12.2 Environment

Suggested default environment:

```text
Miniforge, arm64 native
Python 3.11.x
PyTorch 2.12.0
Hydra-based configuration composition
h5py compatible with the canonical HDF5 store
TensorBoard local viewer
```

The owner types:

```bash
./trainex setup --framework pytorch --python 3.11
```

The setup writes a machine-readable lock such as:

```text
environments/pinn-train/environment.lock.yml
environments/pinn-train/packages.txt
environments/pinn-train/setup-report.md
```

The exact dependency set is installed from the lock, not assembled by copying ad hoc commands from the internet. Because PyTorch 2.12's Apple wheels changed their Metal shader packaging, setup must verify the exact installed macOS/wheel combination rather than infer compatibility from the release headline. [W-PY-01]

## 12.3 Operator-facing run recipe and resolved config

The owner copies one short file:

```yaml
# configs/runs/my-first-run.yaml
defaults:
  - stage: default
  - opt: first_run
  - loss: phys05
  - execution: macbook_24gb
  - _self_

run:
  name: my-first-run

precision:
  policy: accelerator_float32  # change to cpu_float64 only after adjudication

tracking:
  backend: tensorboard
  canonical_metrics: jsonl_csv

data:
  access_mode: bounded_cache

checkpoint:
  policy: hybrid_transactional

reproducibility:
  mode: production_seeded
  root_seed: 20260619
```

The scientific content in the stage/loss profiles comes from the framework specs; R2 supplies numeric optimizer/collocation tuning where still open. The launch resolver writes the complete `resolved-config.yaml` and its hash before touching model state.

## 12.4 Doctor/preflight

The owner types:

```bash
./trainex doctor --config configs/runs/my-first-run.yaml
```

Doctor produces a single top-line verdict and a detailed report:

```text
PREFLIGHT: PASS
framework: PyTorch 2.12.0
execution: MPS / float32
MPS fallback: disabled
AD component test: PASS (9/9 first, 9/9 second)
full-loss parameter gradient: PASS
CPU/MPS parity: PASS within project tolerance
HDF5 schema/content/admission: PASS
sL-BFGS implementation: PASS
checkpoint atomic write/reopen: PASS
representative peak memory: PASS
input pipeline selection: workers=<measured>, prefetch=<measured>, cache=<measured>
quality gate schema: VALID
```

For the CPU float64 branch, the same report says `CPU / float64`; GPU activity is then not an expected health signal.

Doctor must fail on:

- unavailable/incorrect device or dtype;
- enabled silent fallback;
- any wrong/missing component derivative;
- any non-finite five-term loss/gradient;
- dataset schema/admission/split inconsistency;
- unresolved sL-BFGS for a run that reaches later stages;
- unresolved/contradictory quality-gate schema when final evaluation is requested;
- unsafe measured memory budget;
- inability to atomically write/checksum/reopen a checkpoint; or
- insufficient disk for the configured retention plan and diagnostic reserve.

The project-side architecture acceptance probes should be reimplemented as supported tests rather than invoked through paths named in the snapshots, because the repository and those paths were not provided.

## 12.5 Launch

The owner types:

```bash
./trainex launch --config configs/runs/my-first-run.yaml
```

The wrapper:

1. creates `runs/my-first-run/` using run-contract version 2;
2. freezes input/resolved config, environment, hardware/device, data/admission/split/stage manifests, and seed map;
3. reruns fast preflight checks or verifies a fresh Doctor report hash;
4. starts the stage/phase state machine;
5. writes terminal and canonical metrics;
6. writes transactional recovery checkpoints according to elapsed time/events/step cap; and
7. opens no cloud connection.

The terminal status line should resemble:

```text
run=my-first-run stage=2 phase=adam step=42100 \
loss.total=... data=... ic=... phys=... energy=... angular=... \
lr=... ckpt_age=... mem_peak=... read_ms=... step_ms=... status=healthy
```

It should not print an ETA unless R1b validates how it is computed across stage/optimizer changes.

## 12.6 Monitor

Primary command:

```bash
./trainex monitor --run runs/my-first-run
```

It prints:

- running/stopped/failed/completed;
- current stage and optimizer phase;
- last update time and step;
- all five loss terms and active weights;
- last good checkpoint and checksum status;
- latest warning/guard state;
- memory/cache/throughput telemetry; and
- the exact resume or diagnostic command when relevant.

Optional local browser view:

```bash
tensorboard \
  --logdir runs/my-first-run/metrics/tensorboard \
  --host 127.0.0.1 --port 6006
```

The wrapper may launch this and print `http://127.0.0.1:6006`. Activity Monitor's Memory Pressure and GPU History are secondary observations, not pass/fail thresholds. [W-MAC-01] [W-MAC-02]

## 12.7 Checkpoint and unattended behavior

During ordinary training, the run retains two recent recovery generations. It also writes immutable checkpoints at optimizer handoffs and both sides of every committed stage promotion. A non-finite invariant or unhandled exception stops the run and writes a diagnostic bundle. A soft loss/memory/thermal trend does nothing automatically until R1b supplies an approved threshold; once supplied, the suggested action is checkpoint-and-stop, not automatic hyperparameter changes.

The user sees, for example:

```text
RUN STOPPED SAFELY: non-finite gradient
last good checkpoint: checkpoints/recovery/recovery-s04-adam-...pt
failure bundle: diagnostics/failure-.../
resume after resolving cause: ./trainex resume --run runs/my-first-run
```

## 12.8 Resume

The owner types only the run directory:

```bash
./trainex resume --run runs/my-first-run
```

The resolver reads `latest-good.json`, validates its checksum, validates immutable scientific config/data identities, checks schema compatibility, inspects the stage journal, and reconstructs the correct state. The owner does not manually select `latest.pt`.

A deliberate older restore is explicit and branch-producing:

```bash
./trainex rollback \
  --run runs/my-first-run \
  --to stage-03-complete-<id>
```

The command records lineage and does not overwrite the original run history.

## 12.9 Stage promotion

At each promotion:

1. the authoritative promotion evidence is recorded;
2. `stage-k-complete` is atomically written and verified;
3. the journal enters `PREPARED`;
4. model weights carry;
5. Adam and scheduler are recreated/reset;
6. the new loss schedule re-warms;
7. new replay/lookahead/collocation state binds to hashed manifests/derived keys;
8. `stage-(k+1)-start` is written and verified; and
9. the journal enters `COMMITTED`.

A crash mid-promotion deterministically resolves to the last committed state. Automatic demotion is disabled.

## 12.10 End, candidate export, and evaluation

Training completion writes a final recovery checkpoint and one or more explicitly named candidate exports. The owner evaluates a candidate, not an ambiguous “latest” file:

```bash
./trainex evaluate \
  --run runs/my-first-run \
  --candidate candidate-stage06-final
```

Evaluation writes under the same run:

```text
eval/candidate-stage06-final/
  evaluation-manifest.json
  metrics.json
  metrics.md
  per-trajectory/
  plots/
```

The evaluation manifest records the candidate hash, gate-spec version/hash, test-split manifest hash, software environment, and metric implementation versions. The test gate is rendered exactly from the project-supplied machine-readable gate file. This recipe intentionally gives no duration estimate; R1b owns that join.

## 12.11 Pairwise conflicts and composition risks

| Pair | Conflict | Required treatment |
|---|---|---|
| D1 precision × D3 utilization | If float64 is required, the suggested run is CPU-only; “use the 15-core GPU” is not satisfiable for training | Run CPU float64; R1b must reassess feasibility/duration. Do not claim a GPU run |
| D1 PyTorch MPS × D1 AD risk | Official transforms exist, but MPS operation coverage/correctness can fail for specific higher derivatives | Doctor derivative and full-loss-gradient probes are hard launch gates |
| D1 MLX × D5 | MLX lacks official L-BFGS in its optimizer catalogue | Choosing MLX commits the project to validated quasi-Newton implementations before training |
| D1 JAX Metal × D4/D6 | Apple calls the plug-in experimental and incomplete | Higher unattended-run and version-pin risk; not the suggested default |
| D2 W&B local UI × D3 | Local server/container consumes resources and adds operations | Prefer TensorBoard; keep W&B optional/offline only |
| D3 all-in-memory × D5 | L-BFGS history, second-order AD, and candidate pools can create later-stage peaks | Use bounded streaming/cache and phase-specific budgets |
| D4 exact resume × D6 accelerator variance | Restoring state does not guarantee bitwise-identical future MPS kernels | Promise state-consistent resume, not cross-run bitwise identity |
| D7 reset × checkpoint naming | `stage-k-complete` contains prior optimizer state; `stage-(k+1)-start` contains new Adam state | Preserve both and never label either merely “latest model” |
| B3 composition × baseline single YAML | Flat-file assumptions in resume/hash code would conflict | Hash the fully resolved config and retain the input recipe |
| B7 gate schema × locked gate | Current notation/direction is contradictory | Project adjudication required; do not alter threshold in trainex |
| P-CTL later stages × unresolved sL-BFGS | Full run cannot implement the authoritative loop | Select algorithm/library/state contract before full launch |
| R1a guards × R1b operations | Trend thresholds are not available here | Implement hooks/telemetry; leave thresholds disabled until consolidation |

# 13. What the runbook inherits

## 13.1 Commands and visible outcomes

| Runbook step | Suggested command shape | User sees | Files that must appear |
|---|---|---|---|
| Setup | `./trainex setup --framework pytorch --python 3.11` | environment created; exact versions; arm64/device check | environment lock, package list, setup report |
| Configure | edit `configs/runs/<name>.yaml` | short recipe, not every scientific setting | input recipe only until Doctor/Launch |
| Doctor | `./trainex doctor --config ...` | one PASS/FAIL plus named checks and remediation | preflight report and machine-readable results |
| Launch | `./trainex launch --config ...` | run name/path, device/dtype, stage/phase, five losses, checkpoint age | versioned run directory, manifests, metrics, journal, checkpoints |
| Monitor | `./trainex monitor --run runs/<name>` | status, last update, five losses/weights, memory/I/O, warning, resume path | no required mutation; TensorBoard event files if enabled |
| Browser monitor | `tensorboard --logdir ... --host 127.0.0.1 --port 6006` | local scalar dashboard | TensorBoard event files generated from canonical metrics |
| Resume | `./trainex resume --run runs/<name>` | selected valid checkpoint, validation results, resumed stage/phase | new journal/log events; old files preserved |
| Rollback | `./trainex rollback --run ... --to <stage-checkpoint>` | new lineage/branch ID and reason prompt | branch manifest/lineage record |
| Evaluate | `./trainex evaluate --run ... --candidate <id>` | metric table and locked gate verdict | evaluation manifest, metrics, plots, per-trajectory output |
| Get help | attach `diagnostics/failure-.../` | README states failure and resume context | standard diagnostic bundle |

## 13.2 Artifact formats inherited from the suggested defaults

- **Recovery checkpoints:** PyTorch `.pt` state bundles, immutable names, SHA-256 (or equivalent) checksums, indexed by JSON. The extension is framework-specific; the logical schema is run-contract-owned.
- **Model exports:** separate PyTorch state-dict `.pt` plus an export manifest. A later inference format can be added without changing recovery state.
- **Configuration:** YAML input and fully resolved YAML; JSON manifests for stable machine contracts.
- **Metrics:** JSONL/CSV canonical record plus TensorBoard event files as a view.
- **Stage transitions:** append-only JSONL journal plus immutable stage checkpoints.
- **Data identity:** JSON manifests referencing canonical HDF5 schema/content/transform metadata and exact admitted/split/stage record keys.
- **Diagnostics:** directory of text/JSON/YAML files suitable for copying without the raw dataset.

## 13.3 Hard-constraint pressure points the runbook must flag

### Precision pressure

If float64 training is required, no candidate Apple GPU path satisfies it. The runbook must say “CPU float64” plainly and must not tell the user to expect GPU utilization. This may make full-run feasibility a serious R1b question, but it does not authorize cloud or distributed training.

### Unified-memory pressure

The runbook must not prescribe “load all data” or a fixed worker count. It inherits Doctor-selected bounded cache/prefetch values and a memory-budget failure message. It must advise closing unrelated heavy applications only as an R1b operational instruction, not as a substitute for a safe trainer budget.

### Experimental-backend pressure

Choosing JAX Metal would pressure the unattended-stability constraint because Apple explicitly labels the plug-in experimental and incomplete. The runbook would need stricter version pins and a larger troubleshooting section.

### Optimizer pressure

The unresolved sL-BFGS algorithm pressures framework choice, checkpoint completeness, and the ability to complete later curriculum stages. The runbook cannot repair this; it must fail preflight until implementation is selected.

### Reproducibility pressure

Accelerator training cannot be advertised as bitwise reproducible across runs/releases. The runbook inherits paired-seed comparison language and must not tell the owner that one lower loss proves an improvement.

### Unattended-laptop pressure

Sleep/lid behavior, `caffeinate` usage, thermal interventions, acceptable memory pressure/swap, health-trend thresholds, and duration/ETA belong to R1b. R1a supplies telemetry and safe-stop hooks only.

### Quality-gate pressure

The runbook cannot display a trustworthy final pass/fail until the metric notation/comparator/aggregation conflict is adjudicated and encoded in the gate file. This is a project blocker, not a runbook wording problem.

# 14. Claims-and-uncertainty register

## 14.1 High-impact verified claims

| ID | Claim | Status and evidence | Design consequence |
|---|---|---|---|
| C-01 | PyTorch MPS cannot execute float64 tensors as float64 on the Apple GPU | Verified in current PyTorch MPS source; it raises that MPS does not support float64. [W-PY-03] | Float64 branch is CPU, not MPS |
| C-02 | MLX 0.31.2 float64 works only for CPU operations and raises on GPU | Verified in official MLX data-type docs. [W-MLX-02] | MLX cannot meet GPU-f64 branch |
| C-03 | Apple's JAX Metal plug-in lacks float64, is experimental, and does not pass all JAX tests | Verified on Apple's current Metal/JAX page. [W-JAX-02] | Higher unattended and compatibility risk; no GPU-f64 |
| C-04 | PyTorch exposes composable Jacobian/higher-derivative transforms | Verified in official `torch.func`/Jacobian documentation. [W-PY-04] | Good API fit, subject to exact MPS operation probes |
| C-05 | MLX exposes composable nested gradients, JVP/VJP, and vmap | Verified in MLX 0.31.2 docs. [W-MLX-03] | Technically plausible AD, exact model still must be probed |
| C-06 | JAX has mature documented higher-order transform composition | Verified in JAX higher-order docs. [W-JAX-03] | Strongest AD ergonomics among candidates |
| C-07 | PyTorch and Optax provide L-BFGS mechanisms; MLX's official optimizer list does not | Verified in official optimizer docs. [W-PY-07] [W-JAX-04] [W-MLX-05] | MLX requires extra quasi-Newton work; no option resolves project sL-BFGS automatically |
| C-08 | PyTorch L-BFGS carries significant history memory and uses one device | Verified in official optimizer documentation. [W-PY-07] | Must measure peak on 24 GB machine |
| C-09 | HDF5 chunking supports partial block reads and compression; chunk shape affects read cost | Verified in h5py docs. [W-DATA-01] | Streaming/bounded caching is implementable; layout must be benchmarked |
| C-10 | The authoritative default loss has five terms, not three | Verified in both framework specs. [P-CTL] [P-ARCH] | Baseline log/config/summary schema must change |
| C-11 | The authoritative stage loop uses Adam then L-BFGS and resets Adam at a new stage | Verified in `[P-CTL]`. | D5 phase state and D7 reset are required |
| C-12 | The CTL spec calls for separate stage/optimizer/loss Hydra YAML configuration | Verified in `[P-CTL]`. | Flat operator YAML should compose and freeze these profiles |
| C-13 | The architecture requires componentwise first/second derivatives and rejects a summed-output VJP substitute | Verified in `[P-ARCH]`. | Exact derivative acceptance probe is mandatory |
| C-14 | The canonical data path is float64 HDF5 with partial reads and strict trajectory admission | Verified in `[P-CTL]`. | No JSON/text training input; no silent sample drop |
| C-15 | The baseline final-gate prose is internally contradictory on the direction/meaning of `ε_H` | Directly verified in `[P-BASE]`. | Evaluator must block pending canonical gate specification |
| C-16 | PyTorch does not guarantee complete reproducibility across platforms/releases; deterministic modes can cost performance | Verified in official reproducibility notes. [W-PY-08] | D6 must distinguish state recovery from bitwise replay |

## 14.2 Open uncertainties, contradictions, and required project inputs

| ID | Open item | Why it cannot be asserted now | Required resolution / owner |
|---|---|---|---|
| U-01 | Is accelerator float32 scientifically sufficient for all physics residuals, conservation losses, promotion metrics, and final gates? | The project explicitly says precision is under adjudication; framework capability is not an accuracy result | Project precision adjudication using defined acceptance data/tolerances |
| U-02 | Does the exact SQR-SkipResNet-SIREN + COM + force/energy graph produce correct first/second input derivatives and parameter gradients on PyTorch 2.12 MPS? | General APIs exist, but MPS issue reports show operation-specific failures can occur | Implement/run Doctor probes on the target machine; compare CPU reference |
| U-03 | Exact MPS performance and memory peak for the five-term second-order loss | No code, batch, collocation, or measured model graph was provided | Representative microbenchmark on target machine |
| U-04 | Whether full-batch L-BFGS fits in 24 GB at stages 0–2 | Depends on parameters, full active data representation, graph retention, history size, and implementation | D3 measurements plus selected L-BFGS settings |
| U-05 | Concrete sL-BFGS algorithm and implementation for stages 3–6 | `[P-CTL]` names a family and example values but no algorithm/library/state/line-search contract | Scientific/implementation decision before full run; add acceptance and checkpoint tests |
| U-06 | Exact numeric clipping bound for the causal residual exponent | `[P-CTL]` says clip to avoid underflow but explicitly leaves the bound open | Framework-spec adjudication or R2 scientific decision; trainer must not invent it |
| U-07 | Canonical final quality-gate metric IDs, formulas, comparator directions, aggregation, and split | Baseline's `ε_H` direction conflicts with its prose; similar notation is used for data admission and a loss denominator | Project supplies versioned machine-readable gate spec without changing locked thresholds here |
| U-08 | Actual canonical HDF5 file size, logical bytes, group/chunk layout, compression, and cache behavior | Only the spec, not the produced file, was attached | Data pipeline supplies file; Doctor inventories it |
| U-09 | Actual admitted trajectory/stage populations after blacklist/quarantine/remediation | Attached snapshot describes contracts and some historical populations, not a final generated manifest | Build and hash admission/stage manifests from canonical data |
| U-10 | Exact split fractions and statistical adequacy for final metrics | Baseline marks this open and no final split manifest/power analysis was attached | Data/evaluation owner decision; record exact trajectory-level split |
| U-11 | Batch size, per-trajectory points, collocation active/candidate counts, and refresh schedule used by first run | Numeric tuning is deferred to R2 and some spec numbers are explicitly examples | R2 profiles; D5 only supplies mechanisms |
| U-12 | Exact loader workers, prefetch depth, and cache bytes | These depend on HDF5 layout, model compute, and shared-memory peak | Doctor cold/warm benchmark on target machine |
| U-13 | Checkpoint size, write duration, safe cadence, and retention disk budget | No implementation or free-disk number was supplied | Measure `C_ckpt`, `t_write`, `D_free`; combine with acceptable lost work and R1b run timing |
| U-14 | Whether the selected L-BFGS/sL-BFGS implementation can resume exactly in the middle of a line search/curvature update | Framework and algorithm dependent | Define safe checkpoint boundaries; otherwise resume from prior safe phase checkpoint |
| U-15 | Comprehensive deterministic-operation coverage for this workload on MPS, MLX Metal, or JAX Metal | No primary source certifies the exact graph; Apple labels JAX Metal incomplete | Audit mode and repeated target-machine tests; do not promise bitwise accelerator replay |
| U-16 | Exact current JAX/jaxlib/jax-metal/Optax/Equinox compatible tuple | JAX 0.10.2 is current, while Apple's page gives a plug-in compatibility floor and experimental compatibility flag rather than certification of this full tuple | If JAX is chosen, pin a tested tuple and preserve its lock; no “latest” installs |
| U-17 | PyTorch 2.12 wheel compatibility/performance on the project's exact macOS build | Release notes say Apple wheels include Metal-4 shaders built on macOS 26; this alone does not establish minimum runtime compatibility for the target's installed OS | Setup/Doctor install and execute test on the exact machine; pin working wheel/OS |
| U-18 | Actual overhead of TensorBoard, W&B local server, or MLflow during this workload | No target-machine measurement was run | TensorBoard default; benchmark alternatives before changing D2 |
| U-19 | Run duration, stage durations, ETA reliability, and feasible multi-seed count | Explicit R1b scope; no measured training run exists | R1b consolidation; update comparison protocol and checkpoint interval |
| U-20 | Valid loss-explosion, liveness, memory-pressure, swap, thermal, and post-promotion probation thresholds | Explicit R1b watchlist/operations scope | Keep telemetry/hooks; enable only after R1b/project approval |
| U-21 | Laptop lid/sleep/`caffeinate` and thermal runbook | Operations package scope and OS behavior can change | R1b; do not encode baseline advice as R1a design fact |
| U-22 | Code revision/build identifier and actual module paths | No repository/codebase was provided | Implementation writes VCS commit or source bundle hash into manifest |
| U-23 | Whether attached framework snapshots will change during active precision/spec adjudication | Master says specs are active pinned snapshots | Every run records spec/profile version/hash; rerun preflight after changes |
| U-24 | Whether the 24 GB or 48 GB memory configuration is the actual target machine | The hard constraint for this round specifies 24 GB while the baseline mentions 48 GB as an available BTO option | Design and qualification use 24 GB unless owner explicitly changes the hard constraint |
| U-25 | Statistical meaning of “three paired seeds” | Suggested as an engineering floor, not supported here by a power analysis | R1b feasibility plus later statistical protocol; report all values and do not imply confidence level |

# 15. Primary-source register

All web sources below were checked on **19 June 2026**. Official documentation, official release notes, source repositories, and official issue trackers are used; no third-party blog is used as capability evidence.

## 15.1 Project sources

- **[P-MASTER]** `RESEARCH-CONTEXT-MASTER.md`, active snapshot supplied for this task.
- **[P-BASE]** `2026-06-10-training-execution-design.md`, brainstorm baseline supplied for this task.
- **[P-CTL]** `ctl_instruction.md`, authoritative curriculum/training/data framework snapshot supplied for this task.
- **[P-ARCH]** `pinn_architecture.md`, authoritative architecture/autodiff/loss framework snapshot supplied for this task.

## 15.2 PyTorch

- **[W-PY-01]** PyTorch Foundation, “PyTorch 2.12 Release Blog,” 13 May 2026. `https://pytorch.org/blog/pytorch-2-12-release-blog/`
- **[W-PY-02]** PyTorch Foundation, “PyTorch 2.11 Release Blog,” 2026 release cadence. `https://pytorch.org/blog/pytorch-2-11-release-blog/`
- **[W-PY-03]** PyTorch source, MPS `OperationUtils.mm`, dtype dispatch rejecting float64. `https://github.com/pytorch/pytorch/blob/v2.12.0/aten/src/ATen/native/mps/OperationUtils.mm`
- **[W-PY-04]** PyTorch, “Jacobians, Hessians, hvp, vhp, and more” and `torch.vmap` docs. `https://docs.pytorch.org/tutorials/intermediate/jacobians_hessians.html` ; `https://docs.pytorch.org/docs/stable/generated/torch.vmap.html`
- **[W-PY-05]** PyTorch, MPS environment variables, including fallback control. `https://docs.pytorch.org/docs/stable/mps_environment_variables.html`
- **[W-PY-06]** PyTorch, MPS API, including allocator and RNG-state APIs. `https://docs.pytorch.org/docs/stable/mps.html`
- **[W-PY-07]** PyTorch, `torch.optim.LBFGS` reference. `https://docs.pytorch.org/docs/stable/generated/torch.optim.LBFGS.html`
- **[W-PY-08]** PyTorch, “Reproducibility.” `https://docs.pytorch.org/docs/stable/notes/randomness.html`
- **[W-PY-09]** PyTorch issue #98498, MPS derivative behavior. `https://github.com/pytorch/pytorch/issues/98498`
- **[W-PY-10]** PyTorch issue #177116, MPS gradient correctness report. `https://github.com/pytorch/pytorch/issues/177116`
- **[W-PY-11]** PyTorch, saving/loading models and state dictionaries. `https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html`

## 15.3 MLX

- **[W-MLX-01]** Apple MLX GitHub releases; v0.31.2 listed latest when accessed. `https://github.com/ml-explore/mlx/releases`
- **[W-MLX-02]** MLX 0.31.2, “Data Types,” float64 CPU-only note. `https://ml-explore.github.io/mlx/build/html/python/data_types.html`
- **[W-MLX-03]** MLX 0.31.2, function transforms/quick start. `https://ml-explore.github.io/mlx/build/html/usage/function_transforms.html` ; `https://ml-explore.github.io/mlx/build/html/usage/quick_start.html`
- **[W-MLX-04]** MLX 0.31.2, “Unified Memory.” `https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html`
- **[W-MLX-05]** MLX 0.31.2 optimizer catalogue and saving/loading optimizer state. `https://ml-explore.github.io/mlx/build/html/python/optimizers.html`
- **[W-MLX-06]** MLX 0.31.2 core API, memory-management functions. `https://ml-explore.github.io/mlx/build/html/python/core.html`

## 15.4 JAX, Optax, Equinox, and Orbax

- **[W-JAX-01]** JAX changelog; JAX 0.10.2 dated 17 June 2026. `https://docs.jax.dev/en/latest/changelog.html`
- **[W-JAX-02]** Apple Developer, “Accelerated JAX on Mac — Metal plug-in,” requirements, compatibility table, limitations. `https://developer.apple.com/metal/jax/`
- **[W-JAX-03]** JAX, “Higher-order derivatives” and autodiff cookbook. `https://docs.jax.dev/en/latest/higher-order.html` ; `https://docs.jax.dev/en/latest/notebooks/autodiff_cookbook.html`
- **[W-JAX-04]** Optax, L-BFGS example/API. `https://optax.readthedocs.io/en/latest/_collections/examples/lbfgs.html` ; `https://optax.readthedocs.io/en/stable/api/optimizers.html`
- **[W-JAX-05]** Equinox, serialization API. `https://docs.kidger.site/equinox/api/serialisation/`
- **[W-JAX-06]** Orbax, checkpointables and training-state bundles. `https://orbax.readthedocs.io/en/latest/guides/checkpoint/v1/checkpointables.html`
- **[W-JAX-07]** JAX, default dtypes and 64-bit configuration. `https://docs.jax.dev/en/latest/default_dtypes.html`

## 15.5 Tracking and configuration

- **[W-TRK-01]** TensorFlow, “Get started with TensorBoard.” `https://www.tensorflow.org/tensorboard/get_started`
- **[W-TRK-02]** PyTorch, TensorBoard/`SummaryWriter` integration. `https://docs.pytorch.org/docs/stable/tensorboard.html`
- **[W-TRK-03]** Weights & Biases, `wandb offline`. `https://docs.wandb.ai/models/ref/cli/wandb-offline`
- **[W-TRK-04]** Weights & Biases, local server command. `https://docs.wandb.ai/models/ref/cli/wandb-server/wandb-server-start`
- **[W-TRK-05]** MLflow, Tracking. `https://mlflow.org/docs/latest/ml/tracking/`
- **[W-TRK-06]** MLflow, Tracking Server architecture. `https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/`
- **[W-CFG-01]** Hydra, Defaults List. `https://hydra.cc/docs/advanced/defaults_list/`
- **[W-CFG-02]** Hydra, debugging/printing composed configuration. `https://hydra.cc/docs/tutorials/basic/running_your_app/debugging/`

## 15.6 Data, operating system, and atomic files

- **[W-DATA-01]** h5py 3.16, Datasets: chunked storage, filter pipeline, `nbytes`, and partial reads. `https://docs.h5py.org/en/stable/high/dataset.html`
- **[W-MAC-01]** Apple, Activity Monitor memory usage and memory pressure. `https://support.apple.com/guide/activity-monitor/view-memory-usage-actmntr1004/mac`
- **[W-MAC-02]** Apple, Activity Monitor GPU activity/GPU History. `https://support.apple.com/guide/activity-monitor/view-gpu-activity-actm9329b315/mac`
- **[W-MAC-03]** Apple, `kernel_task` and CPU thermal management. `https://support.apple.com/en-us/102172`
- **[W-IO-01]** Python 3 standard library, `os.replace` and `os.fsync`. `https://docs.python.org/3/library/os.html#os.replace` ; `https://docs.python.org/3/library/os.html#os.fsync`
- **[W-IO-02]** The Open Group, POSIX `rename`. `https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html`
- **[W-ECO-01]** DeepXDE official installation/backend documentation. `https://deepxde.readthedocs.io/en/latest/user/installation.html`

# 16. Fill-in decision sheet

The project owner makes every final pick. The “suggested default” column is advisory.

| Decision | Options | Suggested default | Door type | Your pick |
|---|---|---|---|---|
| **D1 — ML framework** | A. PyTorch 2.12 MPS/CPU; B. MLX 0.31.2; C. JAX 0.10.2 + Optax + Equinox + tested jax-metal tuple | If f32 accelerator passes: PyTorch 2.12 MPS/f32. If f64 training is required: same PyTorch implementation on CPU/f64. | **One-way** | |
| **D2 — Tracking** | A. TensorBoard + neutral metrics; B. W&B offline; C. MLflow local; D. JSONL/CSV + static reports only | Terminal + canonical JSONL/CSV + TensorBoard local view | **Two-way** | |
| **D3 — Unified-memory/data use** | A. Fully in memory; B. pure streaming; C. streaming + bounded stage cache | Streaming HDF5 + hard-bounded stage-local cache; Doctor selects workers/prefetch/cache | **One-way (limits are two-way parameters)** | |
| **D4 — Checkpoint/guards/diagnostics** | A. step/latest-only; B. wall-clock + stage; C. hybrid elapsed/event/step-gap transactional | Option C; two recovery generations; all stage boundaries; invariant hard stops; diagnostic bundle; no auto-restart | **One-way core** | |
| **D5 — Loop skeleton** | A. fixed dedicated two-phase loop; B. small pluggable phase/collocation/loss state machine; C. generic execution/callback framework | Option B; explicit Adam/full-L-BFGS adapters, sL-BFGS slot with fail-fast until resolved, collocation interface, five-term schedule | **One-way** | |
| **D6 — Reproducibility** | A. accelerator seeded best effort; B. strict determinism every run; C. deterministic CPU acceptance + seeded accelerator production/multi-seed confirmation | Option C | **One-way provenance contract; two-way strictness/count** | |
| **D7 — Stage boundaries** | A. checkpoint then mutate; B. transactional prepared/committed + manual rollback; C. transactional + auto rollback | Option B; immutable stage-complete/start, Adam reset, loss re-warm, deterministic target state | **One-way state contract** | |
| **B1 — Subsystem cut** | Keep baseline 3 subsystems + verification; **change** to environment substrate + data/admission + training engine + run-state/artifacts + evaluation | Change | **One-way** | |
| **B2 — Code shape** | Keep one monolithic training script; **change** to thin explicit orchestrator + narrow modules | Change | **One-way** | |
| **B3 — Config** | Keep one flat YAML; **change** to one operator recipe composing stage/opt/loss/execution profiles and freeze resolved config | Change | **One-way** | |
| **B4 — Run contract** | Keep baseline files/`latest.pt`; **change** to versioned provenance-rich run contract, indexed recovery, stage journal, diagnostics, separate exports | Change | **One-way** | |
| **B5 — Entry points** | Keep five-only surface; **change** to add explicit Doctor and Evaluate through one wrapper | Change | **Two-way** | |
| **B6 — Checkpoint trigger** | Keep every 1,000 steps; **change** to elapsed-time + event + optional step-gap | Change | **Two-way** | |
| **B7 — Final gate representation** | Keep prose/example; **change** to versioned machine-readable gate and block until metric/comparator contradiction is adjudicated | Change | **One-way** | |
| **B8 — Invalid data** | Keep sample-level NaN/Inf dropping; **change** to authoritative trajectory admission/quarantine with reason-coded manifest | Change | **One-way** | |
| **B9 — Loss/log schema** | Keep three-term surface; **change** to locked five-term catalogue, weights, and phase schedule state | Change | **One-way** | |
| **B10 — Operations ownership** | Keep baseline utilization/thermal/swap/duration prescriptions; **change** to R1a telemetry/hooks + R1b thresholds/runbook procedure | Change | **Two-way** | |
| **B11 — Data compatibility** | Keep one opaque version-hash equality; **change** to schema/content/transform/admission/split identities and explicit compatibility policy | Change | **One-way** | |
================================================================================
END ORIGINAL: chatgpt-pro-resolution.md
================================================================================

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

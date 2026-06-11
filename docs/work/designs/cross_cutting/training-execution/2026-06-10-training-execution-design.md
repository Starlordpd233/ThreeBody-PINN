---
status: active
purpose: design
created: 2026-06-10
milestone: untracked
phase: training-execution
retirement_trigger: v1.5 milestone work; active until superseded
---

# CTL-PINN Training Execution Design

**Status:** Design intent — framework-agnostic, mechanical surface committed, scientific/technical internals deferred to research.
**Date:** 2026-06-10
**Scope:** How a non-expert user will run, monitor, and assess CTL-PINN training on a single M5 Pro MacBook.
**Out of scope:** On-disk dataset format (owned by v1.5 PIPE-XX), curriculum stage design (owned by `ctl_instruction.md`), network architecture (owned by `pinn_architecture.md`), IC sampling (owned by `sampling_method.md`).

---

## 1. Purpose

The CTL-PINN project has well-developed *framework specs* (curriculum staging, network architecture, sampling methodology) and a *produced dataset* (`simulation_data/`). What it does not yet have is a *user-facing training execution design* — a specification of how a non-expert user will go from "I want to train this model" to "the model is trained and verified, here is how good it is."

This document fills that gap. It defines:

- The **mechanical surface** of training (what the user types, what the user sees, what files appear).
- The **subsystem decomposition** (developer environment, data ingestion, training loop) and their boundaries.
- The **verification surface** (how the user knows if training is healthy, better, or good enough).
- The **placeholders** for internals that need external research before they can be honestly specified.

It explicitly does **not** define:
- The ML framework (deferred to PH-1).
- The on-disk dataset format (owned by v1.5 PIPE-XX).
- The loss function, network architecture, or curriculum promotion rules (owned by framework specs).
- Any scientific/technical internals where the source materials are silent (per the project's STOP protocol).

The intended reader is the project owner, who is non-expert at model training. This is a **reference design document** — a record of the design ideas, constraints, and deferred decisions captured during an early-stage brainstorm. It is not a build spec, a runbook, or a contract for immediate implementation. The user will refer back to this document later, when the time comes to start designing the training pipeline in earnest. That work will happen **in parallel** with the development of the actual PINN code (the scientific/mathematical side, owned by the framework specs); the mechanical surface captured here can be designed now because it doesn't depend on the science being settled.

---

## 2. Background and Constraints

### 2.1 Hardware reality

The only training machine is a **MacBook Pro M5 Pro**:

- **CPU:** 16 cores
- **GPU:** 15 cores
- **Memory:** 24GB unified (BTO baseline; 48GB available on higher BTO)
- **OS:** macOS 15+ (Apple Silicon, arm64)
- **Neural Engine:** present (used by CoreML, not directly accessible to PyTorch/MLX/JAX for training)

Unified memory is the key hardware fact: CPU and GPU share the same physical RAM. There is no separate VRAM. Total budget for training is 24GB; if the trainer uses 20GB, the OS only has 4GB.

CPU+GPU co-utilization is desired (the M5 Pro is marketed for AI workflows) but the *exact* mechanism is a research question (see PH-8).

### 2.2 Project state

- **Framework specs exist** and are authoritative (`pinn_instruction/markdown_conversion/framework-specs/`).
- **Dataset is produced** (`simulation_data/`).
- **No live code** is a grounding source for v1.4+ spec decisions (user directive 2026-05-19). v1.3-era `pinn/` code (`basic_architecture.py`, `data-processing-pipeline-full.py`) is stale and will be rewritten in FUT-01 from specs.
- **v1.5 milestone** is in progress and owns the data pipeline and validation contracts (PIPE-XX).
- **FUT-04** is the future phase that will implement the training loop. FUT-01 rewrites the `pinn/` package from specs.

### 2.3 User profile

The user is a non-expert at model training. They have never trained a model before. They are comfortable with terminal commands but are not a Python developer. They can read code, follow a runbook, and report what they see.

### 2.4 STOP protocol compliance

The project's STOP protocol (CLAUDE.md, user directive 2026-05-19) forbids inventing content where source materials are silent. This design honors that:

- Internals where the spec is silent are marked as placeholders (PH-1 through PH-10).
- The user is told which decisions are theirs to make, not silently chosen.
- The framework choice is explicitly flagged as a research-driven decision, not committed in this document.

---

## 3. Architecture Overview

### 3.1 Three subsystems

The training execution has three subsystems, each with a clear boundary and a clear interface to its neighbors.

**Subsystem 1 — Developer Environment.** The substrate everything else runs on. A Python environment (Miniforge3-based, Python 3.11+, arm64-native), a machine-learning framework chosen per PH-1, a small set of utility packages, and a one-command setup script. The user interacts with this subsystem exactly once per machine.

**Subsystem 2 — Data Ingestion.** Reads the on-disk `simulation_data/` dataset via a thin adapter that hides the on-disk format from the rest of the trainer. Applies train/val/test splitting, drops NaN/Inf samples, emits fixed-shape mini-batches. The user does not interact with this subsystem directly.

**Subsystem 3 — Training Loop.** Runs an outer curriculum loop (driven by `ctl_instruction.md`) and an inner optimization loop (gradient descent over mini-batches from Subsystem 2, computing a combined data + physics + IC loss and backpropagating). Writes a `runs/<name>/` directory containing checkpoints, logs, and summary.

**Verification layer (not a fourth subsystem).** Reads the run output directory; does not modify training state. Lives in a separate `evaluate` script.

### 3.2 Data flow

```
   ┌──────────────────────┐
   │ simulation_data/     │  (on disk, format owned by v1.5 PIPE-XX)
   │   trajectories, ICs  │
   └──────────┬───────────┘
              │ reads
              ▼
   ┌──────────────────────┐
   │ Subsystem 2:         │
   │ Data Ingestion       │  (adapter layer, format-aware)
   │   train/val/test     │
   │   split manifest     │
   │   NaN/Inf filter     │
   └──────────┬───────────┘
              │ emits fixed-shape batches
              ▼
   ┌──────────────────────┐
   │ Subsystem 3:         │
   │ Training Loop        │  (curriculum outer + optimization inner)
   │   forward pass       │
   │   loss computation   │  ←── physics residuals (AD)
   │   backprop           │
   │   checkpoint         │
   └──────────┬───────────┘
              │ writes
              ▼
   ┌──────────────────────┐
   │ runs/<name>/         │  (consumed by verification)
   │   checkpoints/       │
   │   logs/              │
   │   summary.md         │
   │   status.json        │
   └──────────────────────┘
```

Subsystem 1 (Developer Environment) sits *under* Subsystems 2 and 3 — it is the substrate they run on, not a peer in the data flow.

### 3.3 What this design commits to (the non-placeholder surface)

1. Subsystem count and boundaries are committed.
2. Data flow direction is committed (Disk → Data Ingestion → Training Loop → Run output).
3. The "thin adapter" pattern for data ingestion is committed. The trainer does not import disk-format libraries; only the adapter does.
4. The five user-facing entry points (Setup / Configure / Launch / Monitor / Resume) are the only user-facing surfaces.
5. The `runs/<name>/` directory is the runbook contract.
6. The verification layer is a consumer, not a producer.
7. First-trial defaults are documented and overridable.
8. The ML framework is a researched decision, not a guess.

### 3.4 What this design does NOT commit to

- ML framework (PH-1)
- Network architecture (owned by `pinn_architecture.md`)
- Loss formulation details (owned by `pinn_architecture.md` and `ctl_instruction.md`)
- Optimizer and LR schedule (PH-7)
- Collocation sampling strategy (PH-6)
- Train/val/test split fractions (PH-5)
- CPU/GPU co-utilization mechanism (PH-8)
- Experiment tracker choice (PH-10)
- Checkpoint file format (framework-dependent)

---

## 4. Components

### 4.1 Subsystem 1 — Developer Environment

**Purpose:** Make the training runnable on the M5 Pro Mac. One-time setup, then invisible.

**User-facing surface:** A single setup script that takes a fresh Mac from "no Python" to "ready to train" in under 15 minutes.

**Internal components:**

- **Miniforge3 Python distribution.** The de-facto standard for arm64 Mac ML work. Installs via a single shell script. No Anaconda channel defaults; fully open-source.
- **Conda environment named `pinn-train`.** Isolates the project's Python and packages from system Python and from other projects. Python 3.11+.
- **ML framework.** The framework chosen per PH-1. The setup script installs it after the environment is created.
- **Utility packages:** numpy, h5py (or whatever the on-disk format needs per v1.5 PIPE-XX), pyyaml (for config files), tensorboard or chosen tracker.
- **One-command setup script.** A `setup.sh` or `Makefile` target that does all of the above idempotently.

**M5 Pro–specific notes:**

- Use the `Miniforge3-MacOSX-arm64.sh` installer.
- macOS 14.0+ is the minimum for PyTorch MPS; M5 Pro ships with macOS 15+.
- Total memory budget is 24GB; Subsystem 3's memory pressure is visible to the OS.

**Source grounding:**

- Miniforge3 README — `github.com/conda-forge/miniforge`
- PyTorch MPS notes — `docs.pytorch.org/docs/2.12/notes/mps.html`

### 4.2 Subsystem 2 — Data Ingestion

**Purpose:** Take the on-disk dataset and serve mini-batches to the training loop. Format-aware, framework-agnostic.

**User-facing surface:** None directly. Runs invisibly inside the trainer.

**Internal components:**

- **Adapter layer.** The only place in the trainer that imports disk-format libraries. If v1.5 PIPE-XX changes the on-disk format, only the adapter changes.
- **Split manifest.** A single file (saved to `runs/<name>/` or a shared location) that records which trajectories belong to train/val/test for a given run. Stratified by physical regime (chaotic / non-chaotic / boundary / special configurations per the dataset's metadata). Deterministic seed.
- **NaN/Inf filter.** Samples with non-finite values are dropped at load time, with a logged count.
- **Batch emitter.** Yields fixed-shape mini-batches. The trainer's loop iterates over these without knowing how they were produced.

**Surface commitments:**

- **Train split:** shuffled every epoch with a deterministic per-epoch seed.
- **Val / test splits:** iterated in a fixed order (no shuffle).
- **Sample-level vs. trajectory-level shuffling:** trajectories are shuffled first, then a fixed number of mini-batches are emitted per trajectory. This keeps temporal coherence within a batch.
- **Default split fractions:** ~80/10/10 (design intent; exact values depend on PH-5).
- **Data-version-mismatch check:** the adapter reads `data_version_hash` from the on-disk dataset and refuses to load if it doesn't match the version the trainer was built for. Hard error, no silent proceed.

**What this subsystem does NOT do:**

- Feature engineering (e.g., log-scaled masses, time normalization). Owned by `pinn_architecture.md` output head and `ctl_instruction.md` input vector formulation.
- Curriculum stage assignment. Owned by `ctl_instruction.md`.
- Physics-residual computation. Owned by Subsystem 3.
- Disk format itself. Owned by v1.5 PIPE-XX.

### 4.3 Subsystem 3 — Training Loop

**Purpose:** Actually train the model. Run an outer curriculum loop and an inner optimization loop. Write the run output directory.

**User-facing surface:** The five entry points described in Section 5.

**Internal components (framework-agnostic sketch):**

- **Curriculum state machine.** Driven by `ctl_instruction.md`. The trainer implements the spec, not the design.
- **Network.** Instantiated from a config-supplied architecture spec per `pinn_architecture.md`. Whether that's an MLP, a modified MLP, a transformer, or something else is the spec's call.
- **Loss computation.** A sum of three terms: data loss (against training trajectories), physics loss (against PDE residuals computed via autograd), IC loss (against initial-condition anchors). Exact weights and forms are owned by the framework specs.
- **Optimizer and LR schedule.** First-trial default: Adam with initial LR 1e-3 and exponential decay (rate 0.95 every 500 steps). Subject to PH-7.
- **Logging.** One line per `log_freq` steps (default 100). Contains: step number, three loss values, learning rate, time-per-step, ETA.
- **Checkpointing.** Every `checkpoint_every` steps (default 1000). Contains: model state, optimizer state, current step, current stage, RNG state.
- **Resume logic.** Same config file + checkpoint path → continue. Different config file → hard error.
- **Collocation sampling.** The trainer samples interior points for the physics loss term. Strategy per PH-6.

**Pattern grounding:** The plain-Python-loop style of the PhysicsNeMo inverse-PINN example is the reference shape: data loading, forward pass, loss, optimizer step, all written out explicitly. No heavy abstractions.

**Source grounding:**

- PhysicsNeMo inverse-PINN example — `github.com/nvidia/physicsnemo/blob/main/examples/cfd/inverse_pinns/README.md`
- PyTorch autograd mechanics — `docs.pytorch.org/docs/2.12/notes/autograd.html`

### 4.4 Verification layer (consumer of Subsystem 3's output)

**Purpose:** Tell the user whether training is healthy, better than before, or good enough.

**User-facing surface:** Three surfaces for three time scales (Section 6).

**Internal components:**

- **Live log emitter (inside Subsystem 3).** Writes to `runs/<name>/logs/train.log` and `train.log.jsonl`.
- **Run summary writer (at end of run).** Writes `runs/<name>/summary.md` and `summary.json`.
- **Test-set evaluator (separate script).** Reads a checkpoint, runs the test set, writes `eval/final-on-test/metrics.json` and `metrics.md`.
- **Gate checker (separate script or sub-step of evaluator).** Compares test-set metrics against the post-v1.3 gate (ε_H > 10⁻⁵, SCS > −5). Renders pass/fail.

---

## 5. User Runbook Surface

The user interacts with the training execution through five entry points. Each is a single user action. The internals behind each are not the user's concern.

### 5.1 Mental model

Before any commands, the user is told:

> "Training a model is like running a long calculation. You start it in a terminal. It prints progress. You can stop it anytime (Ctrl-C) and resume it later from where you stopped. The whole run produces a folder of files — the trained model, the training history, and a log. If something goes wrong, the log is the first place to look."

### 5.2 Entry point 1 — Setup (first time only)

A sequence of shell commands that takes a fresh Mac to "ready to train":

```
# Open Terminal, paste these one at a time:
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
# (close terminal, open a new one)
conda create -n pinn-train python=3.11
conda activate pinn-train
# (framework-specific install — command deferred to PH-1; see Section 7.1)
```

**On success:** terminal prompt starts with `(pinn-train) `.

**On failure:** red error message. First troubleshooting step: copy the error, paste it into a search engine, look for the exact same error string.

### 5.3 Entry point 2 — Configure (before each run)

The user edits (or copies) a single config file. The mechanical surface:

```
# File: configs/runs/my-run.yaml
run_name: my-first-run
data_version: <set by v1.5 PIPE-XX>
framework_device: mps    # auto, mps, or cpu
checkpoint_every: 1000
max_steps: 100000
# ... other knobs the user shouldn't touch yet are commented out
```

**Design intent:**

- One file per run, not a giant central config.
- All knobs the user shouldn't touch are commented out or hidden behind an "advanced" marker.
- Validation: if a required field is missing, the run refuses to start with a clear error.

### 5.4 Entry point 3 — Launch (each run)

A single command:

```
cd <home>/Desktop/3_body_problem
conda activate pinn-train
python -m pinn.train --config configs/runs/my-run.yaml
```

**What the user sees on screen (in order):**

1. Environment check: "Found device: mps. Memory available: ~22GB." (or a warning if MPS unavailable)
2. Data check: "Loading dataset v<hash>... N train trajectories, M val, K test. ETA 30s."
3. Curriculum state: "Starting at stage <N> of <M>."
4. First batch: "Step 0 / 100000. data_loss=X physics_loss=Y ic_loss=Z total=W lr=1e-3 (12s/step)"
5. Steady-state: a fresh line every `log_freq` steps (default 100). Same fields as step 0 plus an ETA.

**Stop rules:**

- Ctrl-C once → graceful shutdown, saves checkpoint at current step.
- Ctrl-C twice → immediate exit, no checkpoint.
- MacBook sleep / lid close → training continues when lid reopens (with caveats; see 5.10).

**Hard rule for the user:** "If you see three identical consecutive step lines with no progress (same step number, no new line for 5+ minutes), training is hung. Press Ctrl-C and read the troubleshooting section."

### 5.5 Entry point 4 — Monitor (while running)

**Primary surface:** live terminal log. The user reads the most recent few lines.

**Secondary surface:** browser-based dashboard via `tensorboard --logdir runs/<name>/` (or chosen tracker per PH-10). Plots of loss vs. step, learning rate schedule, validation curves.

**System monitoring (Mac-side):**

- Activity Monitor → Energy tab → check GPU usage isn't 0% (means training is CPU-only) and isn't 100% sustained with very low time-per-step variance (means the model is too small).
- Memory tab → if "Swap used" is non-zero and growing, the OS is thrashing.

### 5.6 Entry point 5 — Resume (after stop/crash)

A single command, mirroring Launch:

```
python -m pinn.train --config configs/runs/my-run.yaml --resume runs/<name>/checkpoints/latest.pt
```

**Resume invariants:**

- Same config file → same model architecture, same data version, same curriculum stage.
- A different config file → error, refuse to resume.
- No checkpoint found → error, with the path it looked at.

### 5.7 Run output structure

After a successful run:

```
runs/
  <name>/
    config.yaml                    # frozen copy of what was run
    checkpoints/
      step-001000.pt
      step-002000.pt
      latest.pt                    # symlink or copy of most recent
    logs/
      train.log                    # human-readable, full
      train.log.jsonl              # machine-parseable, one line per logged step
    summary.md                     # human-readable end-of-run summary
    summary.json                   # machine-parseable end-of-run summary
    status.json                    # one-line run summary
```

**User-facing meaning of each file:**

- `config.yaml` — proof of what was run. "What config produced this model?"
- `checkpoints/latest.pt` — the trained model. Load this to make predictions.
- `train.log` — read this when something looks wrong.
- `summary.md` — end-of-run one-pager. "How did it go?"
- `status.json` — first place to look. "Did the run finish? What was the final loss?"

**Contract:** "If a colleague asks you to reproduce your results, give them the `runs/<name>/` directory. Everything they need is in there."

### 5.8 Error surface

Categorized errors, each with a one-line user instruction:

| Symptom | What it means | User action |
|---|---|---|
| "MPS not available" | PyTorch can't reach the GPU | Check macOS version, reinstall PyTorch |
| "Data version mismatch" | Dataset on disk is newer than trainer expects | Update trainer, OR regenerate dataset |
| "CUDA out of memory" / "MPS memory pressure" | Model + batch too big for 24GB | Reduce batch size, OR check for memory leak |
| "NaN in loss" | Training diverged | Restore last good checkpoint, reduce learning rate |
| "Checkpoint not found" | Bad resume path | Check the path, OR start a fresh run |
| "Permission denied" | File ownership issue | `chmod` the directory (advanced — ask for help) |
| Three identical step lines, no progress | Training is hung | Ctrl-C, restore checkpoint, restart |

Anything more exotic gets categorized as "unknown error — copy the log, ask for help."

### 5.9 What's NOT in the runbook

- Hyperparameter selection. The first run uses documented defaults.
- Distributed training. Not on the table.
- Cloud fall-back. Out of scope per Q2 decision.
- Framework-specific internals. Invisible to the user.

### 5.10 M5 Pro–specific mechanical notes

- **Unified memory:** 24GB is the total budget. Watch memory pressure.
- **macOS 14.0+ required for MPS.** Always satisfied on M5 Pro.
- **Thermal throttling:** long runs heat the laptop. If the fan is at full speed and clocks are dropping below base, training is throttled.
- **Sleep behavior:** use `caffeinate -d` to prevent sleep during unattended runs.
- **No multi-MPS-device parallelism.** `torch.mps.device_count()` returns 1.

---

## 6. Verification & Assessment Surface

The user has three distinct questions at three distinct time scales. Each has its own surface, its own answer, and its own "what to do next."

### 6.1 Question 1 — "Is training healthy?"

**Time scale:** every ~5 minutes during a run.

**Primary surface:** the live terminal log. The user reads the most recent few lines and asks:

- Is the step number going up at roughly the rate the log claims?
- Are the loss values going down, even if slowly?
- Is the time-per-step stable?
- Is the learning rate what the config said it should be?

**Secondary surface:** the dashboard plot of total loss vs. step. Healthy vs. unhealthy patterns:

- **Healthy:** big drop in the first ~1000 steps, then a slow steady decline. Small wiggles are normal.
- **Plateauing too early:** the curve flattens before step 10k. Training is stuck.
- **Diverging / NaN:** the curve shoots up or shows `nan`. Training has failed.
- **Oscillating wildly:** the curve jumps up and down with no trend. Learning rate too high, or batch size too small.

**M5 Pro–specific liveness checks:**

- Activity Monitor → GPU utilization should be 60-95% during steady-state training. 0% means training is CPU-only.
- Memory tab → if "Swap used" is non-zero and growing, stop the run.

**User's action set during a run:**

| Observation | Action |
|---|---|
| Loss going down, GPU busy | Keep watching |
| Loss plateauing, GPU busy | Wait; some plateaus resolve after 10k more steps |
| Loss diverging, NaN appears | Ctrl-C, restore last good checkpoint, start a new run with smaller LR |
| Step number stuck 5+ minutes | Ctrl-C, check log tail, restore checkpoint, restart |
| Memory pressure climbing | Ctrl-C, reduce batch size in config, start a new run |
| MacBook hot, fans full, clocks throttling | Pause run, cool down, OR move to a cooler room |

### 6.2 Question 2 — "Is this run better than my last one?"

**Time scale:** end of run, before launching the next one.

**Primary surface:** a run-comparison report. After every run, the trainer writes a one-page summary into `runs/<name>/summary.md`.

**`summary.md` contains, in order:**

1. **Run header** — name, start time, end time, total wall-clock time, framework device used.
2. **Final losses** — data loss, physics loss, IC loss, total. With their units in plain English.
3. **Validation curves summary** — "validation loss decreased steadily; final value 1.2e-4 at step 95,000."
4. **Curriculum progression** — "Started at stage 1, advanced to stage 3 at step 40,000, advanced to stage 5 at step 70,000."
5. **Test-set preview** — small subset of test trajectories with predicted-vs-true plots.
6. **Comparison hint** — if a previous run is named, "vs. my-previous-run: total loss 3.2× lower, val loss 2.1× lower."

**To compare two runs:** open both `summary.md` files. The numbers at the top are the answer.

### 6.3 Question 3 — "Is this model good enough?"

**Time scale:** milestone boundary (end of a phase or milestone, before declaring work "done").

**Primary surface:** test-set assessment + gate check. The full test set is evaluated **once** at the very end, by a separate script:

```
python -m pinn.evaluate --checkpoint runs/<best-run>/checkpoints/latest.pt --output eval/final-on-test/
```

**Output:**

```
eval/final-on-test/
  metrics.json             # all metrics, machine-parseable
  metrics.md               # human-readable, with the gate verdict
  per-trajectory/          # per-trajectory breakdown if a sample failed
  plots/                   # diagnostic plots
```

**The gate check is binary and visible.** The post-v1.3 gate is the published acceptance criterion: ε_H (energy error) > 10⁻⁵ and SCS (some chaos signature) > −5. The `metrics.md` file renders:

```
## Gate Check
- ε_H: 8.2e-6  (required: > 1e-5)  → ❌ FAIL
- SCS: -3.4    (required: > -5)    → ✅ PASS

OVERALL: ❌ FAIL
```

**Plain-English descriptions** for each metric, in `metrics.md`:

- **ε_H (energy error):** "How much the model's predicted orbits drift from perfect energy conservation. Smaller is better. < 10⁻⁵ is excellent."
- **SCS (some chaos signature):** "How well the model captures sensitive dependence on initial conditions. Larger is better. > -5 is acceptable."

The user can read these without a physics background. They can act on the pass/fail without understanding the math.

**M5 Pro–specific note on test-set evaluation:** Full test-set evaluation is one forward pass with no gradient computation. Much faster than training — typically 5-15 minutes on M5 Pro for the expected test-set size.

### 6.4 The honesty layer

Three rules the user is taught explicitly:

> **"Healthy validation loss ≠ working model."** A model can have low training loss and low validation loss and still fail the gate. The test set is the only honest answer.

> **"Comparison to previous run ≠ progress."** A run that beats the previous run on validation can still fail the gate. Comparison is for *picking* which run to evaluate on test, not for *claiming* success.

> **"A clean loss curve ≠ correct physics."** A PINN can fit the data loss to zero and still get the physics wrong. The gate is what catches this.

### 6.5 Outcome-level failure modes

Beyond the loss-curve shapes in 6.1, there are *outcome-level* failure modes the user sees at the end of a run:

| Failure mode | Symptom in `summary.md` | What it means | What to do |
|---|---|---|---|
| **Memorization** | Train loss near zero, val loss much higher | Network memorized train trajectories but doesn't generalize | Model too small, OR data too small, OR data leak between splits |
| **Mode collapse** | Predicted trajectories all look the same | Network learned a degenerate solution | Bad initialization, OR learning rate too high, OR data has a dominant regime |
| **Energy drift** | Test-set ε_H fails gate | Network doesn't conserve energy | Physics loss term underweighted, OR model can't represent the dynamics |
| **Chaos-blind** | Test-set SCS fails gate | Network doesn't capture sensitive dependence | Network too smooth (activation choice), OR collocation sampling too coarse |
| **Numerical blow-up** | Predicted trajectories have NaN/Inf outside training time range | Network is unstable past training horizon | Output scaling wrong, OR no regularization on higher-order derivatives |

The user does not need to *fix* these — they need to *name* them. The runbook translates "the loss curve looks weird" into "this looks like memorization" so the user can report it precisely.

### 6.6 What's NOT in the verification layer

- Per-batch metric computation. Internal; surfaced only as the loss log line.
- Hyperparameter sweep tooling. Out of scope.
- A/B testing of architectures. Out of scope.
- Cross-run statistical comparison. `summary.md` includes a hint, not a full analysis.
- Human evaluation of trajectory plots. Plots are generated; user can look but isn't required to.

---

## 7. Placeholders — Internals Awaiting External Research

Each placeholder is something this design **does not** decide. Each is paired with a research question that, once answered, will produce the actual decision.

### 7.1 PH-1. ML framework choice

- **Status:** Framework-agnostic design. The trainer writes against an abstraction; the framework is plugged in.
- **Why deferred:** STOP protocol — framework choice is exactly a "candidate verdict source" decision that needs external research.
- **Research question:** Among PyTorch+MPS, MLX, JAX+Optax+Equinox, which is the best fit for (a) a non-expert user maintaining a single training script, (b) autograd-friendly physics-residual computation, (c) Apple Silicon native performance, (d) long-term ecosystem support for a research project?
- **Sources to consult:** PyTorch MPS docs, MLX README, JAX documentation, NVIDIA PhysicsNeMo's PyTorch-based example as a reference shape.
- **Output:** A framework decision document, one paragraph per candidate with a clear recommendation and rationale.

### 7.2 PH-2. Curriculum stage design and promotion rules

- **Status:** Owned by `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.
- **Why deferred:** The spec exists; this design doesn't re-derive it.
- **Research question:** None — the spec is the source. The trainer's job is to *implement* the spec, not to *decide* the spec.

### 7.3 PH-3. Loss formulation (weights, terms, regularization)

- **Status:** The trainer computes a combined loss; the exact terms and weights are owned by `pinn_architecture.md` and `ctl_instruction.md`.
- **Why deferred:** Same as PH-2 — the framework spec is the source.
- **Surface commitment:** The loss will be a sum of three terms: data loss (against training trajectories), physics loss (against PDE residuals), IC loss (against initial-condition anchors). The exact mathematical form of each term is the spec's responsibility.

### 7.4 PH-4. Network architecture

- **Status:** Owned by `pinn_architecture.md`. This design *consumes* whatever that spec says.
- **Why deferred:** Same as PH-2 and PH-3.
- **Surface commitment:** The trainer instantiates a network from a config-supplied architecture spec.

### 7.5 PH-5. Train/val/test split fractions and stratification policy

- **Status:** Defaults proposed as design intent (80/10/10, stratified by physical regime), but exact values are a research question.
- **Why deferred:** The dataset's size, regime distribution, and inter-trajectory variance are empirical facts that affect the right split.
- **Research question:** With the actual `simulation_data/` size and regime distribution, what split fractions give sufficient statistical power on the test set for the SCS/SASD/IPR/PSC metrics?
- **Output:** A split policy paragraph in a future spec, owned by v1.5 or whoever measures this first.

### 7.6 PH-6. Collocation sampling strategy

- **Status:** The trainer samples interior points for the physics loss term. The strategy is undecided.
- **Why deferred:** Collocation sampling is a deep topic in PINN literature. The right choice depends on the problem's geometry, the network's capacity, and empirical results.
- **Research question:** For the three-body phase space and the regime distribution in `simulation_data/`, what collocation strategy (uniform random, low-discrepancy, residual-based adaptive, time-dependent) is the right starting point?
- **Sources to consult:** PINN literature surveys, Wang et al. 2023 "An Expert's Guide to Training PINNs," PhysicsNeMo examples.
- **Output:** A collocation-strategy paragraph in a future spec, owned by doc-03.

### 7.7 PH-7. Optimization algorithm and learning rate schedule

- **Status:** Trainer runs an optimizer. Specific algorithm and schedule are a research question.
- **Why deferred:** Adam is the safe default; whether Adam, AdamW, L-BFGS, or a custom schedule fits this problem is empirical.
- **Research question:** What's the right optimizer + LR schedule for a PINN on three-body trajectories, starting from a documented first-trial default?
- **First-trial default:** Adam with initial LR 1e-3 and exponential decay (rate 0.95 every 500 steps). This is the PhysicsNeMo example's default and is a reasonable starting point. The user is told this is a *first trial* and we will adjust based on observed loss curves.
- **Output:** An optimizer-config paragraph in a future spec, owned by doc-03.

### 7.8 PH-8. CPU/GPU co-utilization strategy

- **Status:** Desired (per user direction), exact mechanism undecided.
- **Why deferred:** The M5 Pro's unified memory makes "CPU+GPU co-utilization" mean different things in different frameworks. PyTorch MPS can use CPU for data loading while GPU computes, but the data-loader worker count is empirical. MLX has unified memory natively.
- **Research question:** Once the framework is chosen (PH-1), what is the recommended pattern for utilizing both CPU (data loading, augmentation) and GPU (forward/backward pass) on the M5 Pro with 24GB unified memory?
- **Sources to consult:** PyTorch DataLoader docs, MLX unified-memory design notes, community blog posts on M-series ML performance.
- **Output:** A short paragraph in a future spec, owned by doc-03 or whoever implements Subsystem 3.

### 7.9 PH-9. Checkpoint format and resume semantics

- **Status:** Checkpoints contain model state + optimizer state + step + stage. Exact on-disk format (pickle, torch.save, MLX save, custom) depends on the framework.
- **Why deferred:** Framework choice (PH-1) determines this.
- **Surface commitment:** Whatever the framework provides. No custom format invented here.

### 7.10 PH-10. Experiment tracking (TensorBoard vs. W&B vs. MLflow vs. none)

- **Status:** Opt-in dashboard in the runbook. Tool selection deferred to PH-10.
- **Why deferred:** TensorBoard is the lowest-friction default and works with most frameworks. W&B requires an account. MLflow is heavy. The right choice depends on whether the user wants offline-only, cloud-synced, or both.
- **Research question:** What experiment tracker is best for a single-user, single-machine, no-cloud PINN training project?
- **First-trial default:** TensorBoard for the first run, no commitment to a specific tracker.

### 7.11 Research priority order

| # | Question | Blocking for |
|---|---|---|
| 1 | ML framework choice (PH-1) | Subsystem 3 implementation |
| 2 | Optimizer + LR schedule (PH-7) | First-trial config |
| 3 | Collocation sampling strategy (PH-6) | First-trial config |
| 4 | CPU/GPU co-utilization on M5 Pro (PH-8) | Subsystem 3 performance |
| 5 | Split fractions and stratification (PH-5) | Subsystem 2 implementation |
| 6 | Experiment tracker choice (PH-10) | Monitoring surface |

Items 1-3 are needed before the first real training run. Items 4-6 can be researched in parallel and folded in later.

---

## 8. Sources Consulted

External sources consulted during the brainstorm session that shaped this design:

| # | Source | Used for |
|---|---|---|
| S-1 | `docs.pytorch.org/docs/2.12/notes/mps.html` | PyTorch MPS device idiom, macOS 14.0+ requirement, memory APIs |
| S-2 | `docs.pytorch.org/docs/2.12/mps.html` | `torch.mps` module reference (is_available, empty_cache, profiler) |
| S-3 | `github.com/ml-explore/mlx` README | MLX unified memory model, Apple-Silicon-native design |
| S-4 | `github.com/nvidia/physicsnemo/blob/main/examples/cfd/inverse_pinns/README.md` | PINN training loop pattern, Adam + exponential LR schedule, scalar residual reporting cadence, non-abstracted style preference |
| S-5 | `github.com/conda-forge/miniforge` README | Miniforge3 install procedure, arm64 Mac installer, environment creation workflow |
| S-6 | `docs.pytorch.org/docs/2.12/notes/autograd.html` | `torch.autograd.grad` for physics-residual computation pattern |

These are starting references for the project's own runbook, not substitutes for one. The project's runbook will be written to `docs/runbooks/` and will cite these plus additional sources discovered during implementation.

---

## 9. Open Questions for the User

These are decisions only the user can make.

1. **Framework choice (PH-1).** This is the single biggest open question. It blocks the most downstream work. Recommend: dedicated research session before the first training run.
2. **How "researched" the first run should be.** Two options:
   - (a) First run uses documented defaults (Adam, simple collocation, 80/10/10 split, etc.) and we learn from the result.
   - (b) First run waits until a deeper research review is done.
   - Recommend: (a).
3. **Whether to commit this framework-agnostic design as the baseline spec or wait for the framework decision and write a framework-specific spec.** Recommend: commit this now as the baseline; the framework-specific internals can be added in a follow-up spec.

---

## 10. Future Use of This Spec

This spec is a **frozen reference design document** for the CTL-PINN training execution pipeline. The brainstorm session that produced it is complete; this document is the artifact.

**Immediate next steps (this session):**

1. **User reviews this spec** for any changes.
2. **Spec is committed to git** per the project's git guidelines (`docs(<scope>): ...` or `spec(<scope>): ...`).

**What this spec is for, later:**

- This document is the **starting reference** for the training-pipeline side of the user's future build effort. The user will be building the entire codebase and project — including the actual PINN code (the theoretical/scientific side, owned by the framework specs) **in parallel with** the training pipeline (the mechanical side this spec describes). When that build effort begins, the user will refer back to this spec to recall the mechanical design decisions captured here.
- The **10 placeholders (PH-1 through PH-10)** in Section 7 are the decisions waiting to be revisited when the build begins. They are not blocking the spec; they are the *work-to-come markers*. The largest is PH-1 (ML framework choice), recommended as the first research session when build work starts.
- The **3 open questions in Section 9** are also decisions waiting for the user.

**No implementation plan is produced now.** The training pipeline does not have a near-term execution target. The scientific side (PINN code, loss, architecture, curriculum) is being designed separately, in the framework specs and the v1.5 phases. Producing a build plan now would be speculative: there is no concrete target, and the placeholders would force the plan to be mostly placeholders itself. When the user is ready to start building, a fresh brainstorm can produce a plan based on this spec as input.

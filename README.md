# Three-Body Problem: Brutus data pipeline and CTL-PINN training stack

A learning project and proof of concept by one student on one MacBook. It generates high-precision three-body trajectories with the Brutus arbitrary-precision integrator, then tries to train a curriculum-trained physics-informed neural network (CTL-PINN) to predict the motion from the starting conditions.

**The network does not yet solve the problem.** This repository is published as an honest record of the method, the code, and the evidence so far, including the failures.

## Where the project stands

| Milestone | What happened |
|---|---|
| v1.4 – v1.6 | The framework specifications were written and adjudicated: input and output contracts, physics scaling, the data pipeline, the curriculum, the training loop and the loss terms. |
| v2.0 | The training code under `pinn/` was rebuilt from those specifications and a first-stage ("Stage 0") training slice ran end to end. The held-out physics-conservation gate **failed** (energy drift `ε_H = 237.21` against a bar of `1e-5`). |
| v2.1 – v2.3 | Forensics on that failure, nine conformance repairs, and a recalibrated training recipe. The corrected Stage-0 runs still halted at a pre-registered training guard. |
| v2.4 | A feasibility checkpoint on single systems. Every trained network learned only each body's average position. Verdict: rethink the representation. |
| v2.5 | Root-cause work. "The network is too small" was refuted: both a small network and the locked 12-layer network can fit a single Stage-0 orbit at a learning rate of `1e-4`. Every metric was audited against Brutus's exact answer. A focused redesign review was commissioned. |

The full account, with the evidence behind each line, is in [`.planning/PROJECT.md`](.planning/PROJECT.md) and the milestone archives under [`.planning/milestones/`](.planning/milestones/).

## What is in this repository

- **`simulation_data/`** — the data pipeline: initial-condition generation (`Scripts/ic_generation/`), prescreening (`Validation/prescreening/`), Brutus batch runners (`Scripts/brutus_runners/`), metrics (`Scripts/metrics_calculation/`), and the dataset documentation (`Documentation/`).
- **`pinn/`** — the PINN training stack rebuilt from the specifications: `network.py`, `train.py`, `evaluate.py`, `verify.py`, `loss_catalog.py`, `com_projection.py`, and the `data/` and `training/` packages. [`pinn/STATUS.md`](pinn/STATUS.md) says what is shipped and what is a placeholder. Two older single-file scripts (`basic_architecture.py`, `data-processing-pipeline-full.py`) are kept for history and are known to be broken.
- **`pinn_instruction/`** — the framework specifications. The authoritative ones are in `markdown_conversion/framework-specs/`: [`ctl_instruction.md`](pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md), [`pinn_architecture.md`](pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md) and [`sampling_method.md`](pinn_instruction/markdown_conversion/framework-specs/sampling_method.md).
- **`brutus_Newton-main/`** — the Brutus integrator (third-party, Apache-2.0).
- **`reference-code/`** — third-party reference implementations kept for study. None is imported by `pinn/`.
- **`configs/`**, **`tests/`**, **`scripts/`**, **`tools/`** — run configurations, the test suite, and project tooling.
- **`.planning/`** and **`docs/`** — the planning record, evidence, runbooks and reviews. The project was built with AI coding agents under written rules; `CLAUDE.md`, `AGENTS.md` and the other agent-instruction files are those rules.

## What is not in this repository

- **The simulation dataset.** The Brutus outputs and initial-condition files are several thousand trajectories and are not tracked in git. A fresh clone holds fixture-scale data only. The dataset can be regenerated with the pipeline below, at substantial compute cost.
- **Model checkpoints and TensorBoard event files.** Run directories under `runs/` keep their text logs, configurations and summaries.
- **Some reference material** that could not be redistributed. See [`NOTICE`](NOTICE).

## About the history

The commit history was rewritten before publication. Personal identifiers were removed, home-directory paths were replaced with `<home>`, and machine names with `<host>`. Because of that rewrite, commit ids quoted inside planning documents refer to the private original history and will not resolve here. Some documents link to files that were removed.

## Setup

Brutus needs a C++11 compiler, `make`, [GMP](https://gmplib.org/) and [MPFR](https://www.mpfr.org/):

```bash
cd brutus_Newton-main
make clean && make
```

The training environment is a conda environment named `pinn-train` (Python 3.11, PyTorch, NumPy, h5py, PyYAML, TensorBoard), declared in `environment.yml` and pinned for Apple-silicon macOS in `requirements-lock.txt`. `./setup.sh` builds it. The stack was developed and run only on an Apple-silicon Mac; other platforms are untested.

See [`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md), [`docs/TESTING.md`](docs/TESTING.md) and the operator runbooks under [`docs/runbooks/training/`](docs/runbooks/training/).

## Data pipeline

Run from the repository root.

```bash
# 1. Generate initial conditions
python3 simulation_data/Scripts/ic_generation/generate_ics.py

# 2. Prescreen unstable initial conditions with a short leapfrog integration
python3 simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py

# 3. Integrate with Brutus (compile it first)
python3 simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py

# 4. Compute conservation metrics
python3 simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

Dataset layout, naming rules and known anomalies are documented in [`simulation_data/Documentation/README.md`](simulation_data/Documentation/README.md).

## License and credits

Original code, specifications and documentation are licensed under the [Apache License 2.0](LICENSE). Third-party projects in `brutus_Newton-main/` and `reference-code/` keep their own licenses. [`NOTICE`](NOTICE) lists every borrowed project and its license.

The training data comes from Brutus, by Tjarda Boekholt and Simon Portegies Zwart.

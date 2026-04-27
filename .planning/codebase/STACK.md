# Technology Stack

**Analysis Date:** 2026-04-27

## Languages

**Primary:**
- **Python 3.12.2** - IC generation, prescreening, Brutus orchestration, metrics calculation, data preprocessing, PINN architecture and training
- **C++11** (`-std=c++11`) - Brutus high-precision N-body integrator with arbitrary-precision arithmetic

**Secondary:**
- **Bash / Zsh** - Shell scripts for quick testing (`simulation_data/Data/testing_data/quick_test.sh`), build automation
- **LaTeX** (TeX Live 2025, pdflatex engine) - Research methodology documents, architecture plans, instruction papers
- **Markdown** - Converted documentation from LaTeX via pandoc, project documentation

## Runtime

**Environment:**
- Python 3.12.2 system install at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`
- Virtual environment located at `.venv/` (linked to system Python 3.12.2)
- Apple Clang 16.0.0 (`g++` symlink) for C++ compilation

**Package Manager:**
- pip (no dependency manifest found for project's own code)
- No `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, or `environment.yml` exists in the project root
- Dependencies must be installed ad-hoc: `pip install numpy scipy torch h5py matplotlib pandas numba scikit-learn tqdm plotly seaborn`
- C++ dependencies (GMP, MPFR, pandoc) installed via Homebrew at `/opt/homebrew/`

**Dependency Gap:** The project has no declared Python dependencies. Dependency manifests only exist inside reference-code subdirectories (e.g., `reference-code/reference_NNs/pytorch-main/requirements.txt`, `reference-code/reference_NNs/deepxde-master/requirements.txt`), which are for third-party reference code, not the project itself.

## Frameworks and Libraries

### PINN / Machine Learning (Primary)

| Library | Version | Purpose | Key Usage |
|---------|---------|---------|-----------|
| **PyTorch** (`torch`, `torch.nn`) | Not pinned | Neural network framework | `pinn/basic_architecture.py` - SQR-SkipResNet-SIREN architecture |
| **NumPy** (`numpy`) | Not pinned | Array computation | Throughout entire pipeline; IC generation, scaling, invariants |
| **SciPy** (`scipy.stats`, `scipy.interpolate`, `scipy.signal`, `scipy.spatial`) | Not pinned | Sobol sequences, interpolation, signal processing, KDTree | `scipy.stats.qmc` for IC generation; `scipy.interpolate.interp1d` for trajectory resampling; `scipy.signal.correlate` for Lyapunov ACF |
| **scikit-learn** (`sklearn.decomposition.PCA`) | Not pinned | Dimensionality reduction | PCA(1) for Rosenstein Lyapunov exponent estimation in `pinn/data-processing-pipeline-full.py` |
| **Numba** (`numba.jit`) | Not pinned | JIT compilation | Prescreening integrator optimization in `simulation_data/Validation/prescreening/` |

### Data Handling

| Library | Purpose | Key Usage |
|---------|---------|-----------|
| **h5py** | HDF5 file I/O | Preprocessed trajectory datasets, training data storage (`pinn/data-processing-pipeline-full.py`) |
| **pickle** | Python object serialization | Training batch serialization (`batches.pkl`) |
| **pandas** (`pd`) | Tabular data | Metrics analysis in `simulation_data/Validation/analysis/` |
| **json** (stdlib) | Metadata, validation reports | Prescreening indexes, audit reports, configuration |
| **tqdm** | Progress bars | Long-running pipeline operations |

### Visualization

| Library | Purpose | Key Usage |
|---------|---------|-----------|
| **matplotlib** (`pyplot`, `animation`, `patches`) | 2D/3D plotting, widgets | Trajectory visualization, energy plots, interactive inspection |
| **mpl_toolkits.mplot3d.Axes3D** | 3D axes | 3D trajectory plots |
| **plotly** (`graph_objects`, `offline`) | Interactive visualizations | Reference plane, particle position analysis |
| **seaborn** (`sns`) | Statistical plots | Metrics analysis |

### C++ Libraries (Brutus)

| Library | Link Flag | Purpose | Install Location |
|---------|-----------|---------|------------------|
| **GMP** | `-lgmpxx -lgmp` | Arbitrary-precision integer and rational arithmetic | `/opt/homebrew/lib/` |
| **MPFR** | `-lmpfr` | Arbitrary-precision floating-point | `/opt/homebrew/lib/` |
| **mpreal** | Header-only (`-I` path) | C++ wrapper for MPFR providing `mpreal` type | `~/src/mpreal/` (from `https://github.com/advanpix/mpreal/`) |

Brutus linker command (from `brutus_Newton-main/makefile:36`):
```makefile
$(CO) brutus main.o Brutus.o Bulirsch_Stoer.o Cluster.o Star.o Data_Handler.o Timer.o $(LIB_DIRS) -lgmpxx -lgmp -lmpfr
```

### LaTeX / Documentation

| Tool | Version | Purpose |
|------|---------|---------|
| **pdflatex** | TeX Live 2025 | PDF compilation via `latexmk` |
| **pandoc** | 3.7.0.2 | LaTeX-to-Markdown conversion (at `/opt/homebrew/bin/pandoc`) |

LaTeX documents use a `main_*.tex` + `preamble.tex` structure. Documents found in:
- `pinn_instruction/original_latex/ctl-instruction/` - CTL methodology
- `pinn_instruction/original_latex/pinn-architecture/` - PINN architecture spec
- `pinn_instruction/original_latex/Data-quality-assessment/` - Data quality assessment
- `pinn_instruction/original_latex/sampling-method/` - Sampling methodology
- `pinn_instruction/original_latex/review-of-framework/` - Framework review + stage strategy revision

### Python Standard Library (Key Modules)

- `subprocess` - Spawning Brutus processes
- `multiprocessing` / `concurrent.futures.ProcessPoolExecutor` - Parallel execution
- `argparse` - CLI argument parsing
- `pathlib.Path` - Filesystem path handling
- `re` - Regex for parsing Brutus output and file naming
- `dataclasses` - Data structures (`SimulationMetadata`, `RawTrajectoryData`, etc.)
- `typing` - Type hints
- `hashlib` - File checksums for deduplication
- `logging` - Logging framework
- `copy` - Deep copy of simulation data
- `os`, `sys`, `shutil`, `glob`, `time` - OS/file operations
- `warnings` - Warning suppression

## Build System

### Brutus (C++)

- **Build tool:** GNU Make (`brutus_Newton-main/makefile`)
- **Compiler:** Apple Clang 16.0.0 (invoked as `g++` via macOS toolchain symlink)
- **Flags:** `-O3 -std=c++11 -DMPFR_USE_NO_MACRO -DMPFR_USE_INTMAX_T`
- **Artifact:** Single static binary `brutus` at `brutus_Newton-main/brutus`
- **Make targets:** `all` (default, builds `brutus`), `clean` (removes `.o` files and binary)
- **Architecture note:** The active `makefile` is heavily customized for a specific M2 Mac with hardcoded paths (`<home>/src/mpreal`, `/opt/homebrew/include`, `/opt/homebrew/lib`). The `makefile.original` is a Linux reference version with Ubuntu paths. Neither is portable.

Build commands:
```bash
cd brutus_Newton-main
make clean && make
```

### Python Pipeline

- **No build system.** Scripts are executed directly: `python3 script.py`
- **No packaging.** No `setup.py`, `setup.cfg`, or `pyproject.toml`. Scripts are not installable.
- **Import path hacks:** Some scripts use `sys.path.insert()` to add directories to the import path (e.g., `simulation_data/Data/testing_data/test_pipeline.py:23-24`), rather than using relative imports or installable packages.

### LaTeX

- **Build tool:** `latexmk` with `pdflatex` engine
- **Source:** `.tex` files with `.pdf` outputs
- **Conversion:** Custom Python script `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py` converts 6 LaTeX sources to Markdown using pandoc, with extensive pre-processing (macro expansion, TikZ replacement, algorithm replacement) and post-processing (code block cleaning, heading anchor removal, math artifact fixes).

## Configuration

### Environment Variables

| Variable | Required | Used By | Purpose |
|----------|----------|---------|---------|
| `IC_RAW_DIR` | Yes (for Stages 1-2) | `ic_generation_utils.py`, `stage2_prescreening_revised_auto.py`, `prescreening_utils.py` | External directory for raw IC storage. Scripts exit with error if unset. |

Set with:
```bash
export IC_RAW_DIR=/path/to/ic_raw
```

Expected subdirectories under `IC_RAW_DIR`: `ic_hierarchical/`, `ic_standard_quasi_random/`

### Hardcoded Configuration

Most configuration is embedded directly in Python scripts, not externalized:

- `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py:26-73` - Brutus parameters, directory paths, timeout, line count thresholds
- `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py:29-49` - Gold-standard parameters
- `brutus_Newton-main/makefile:2-4` - Compiler paths, library paths
- `pinn_instruction/markdown_conversion/pandoc_conversion/convert_latex_to_md.py:22-25` - Pandoc path, source/target directories

### Secret Files

- `.github/workflows/gemini-review.yml:59-65` references `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `APP_PRIVATE_KEY`, `GCP_WIF_PROVIDER` - all accessed via GitHub Secrets
- `.gitignore:101` excludes `.env*` files (except `.env.example`)
- **No `.env.example` file exists** to document required environment variables

## Hardware and Platform

### Development Target

- **OS:** macOS 15.7.5 (Sequoia)
- **Architecture:** Apple Silicon (arm64, M2)
- **Compiler:** Apple Clang 16.0.0
- **Package manager:** Homebrew (`/opt/homebrew/`)
- **Python:** 3.12.2 (system framework install)

### CPU Parallelism

- Brutus batch runners use `ProcessPoolExecutor` with `max_workers = cpu_count() - 1`
- Each worker spawns a separate Brutus process via `subprocess.run`
- Numba `@jit` decorator accelerates the prescreening leapfrog integrator
- Simulation timeout: 3000 seconds (50 minutes) per Brutus run in batch scripts

### GPU

- **No GPU acceleration used.** PyTorch PINN code detects CUDA but falls back to CPU:
  ```python
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  ```
- **No MPS fallback** for Apple Silicon GPU. Training runs on CPU only on macOS.
- Reference `makefile.original` contains commented-out `nvcc` (NVIDIA CUDA) compiler path but was never used.

### Portability Limitations

- Brutus Makefile contains absolute paths to `<home>/...`
- Multiple Python scripts contain hardcoded absolute paths (e.g., `test_pipeline.py:25`)
- The `makefile.original` exists for Linux but is not maintained
- mpreal must be manually installed from source

## Development Tools

### Editor/IDE
- `.vscode/` directories present in `simulation_data/` and `pinn/` (excluded from git via `.gitignore`)

### Version Control
- Git (repository root at `<home>/Desktop/3_body_problem/`)
- Branch: `master`
- No submodules

### Linting / Formatting
- **None detected.** No `.eslintrc`, `.prettierrc`, `.flake8`, `pyproject.toml`, `ruff.toml`, `.editorconfig`, or pre-commit hooks exist in the project root.
- No Python type checker configuration (no `mypy.ini`, `pyproject.toml [tool.mypy]`)

### CI/CD
- **GitHub Actions** used only for Gemini AI assistant integration:
  - `gemini-dispatch.yml` - Dispatches Gemini commands on PR/issue events
  - `gemini-review.yml` - Gemini-powered code review
  - `gemini-invoke.yml` - Gemini invocation handler
  - `gemini-triage.yml` - Gemini issue triage
  - `gemini-scheduled-triage.yml` - Scheduled triage
- **No CI for:** Building Brutus, running tests, running prescreening, validating datasets, training PINN, compiling LaTeX documents.

### Containerization
- **None in project root.** Dockerfiles only exist in reference-code subdirectories (PyTorch source, DeepXDE).

## Reference Code (Third-Party)

The `reference-code/reference_NNs/` directory contains cloned/forked external repositories:

| Repository | Purpose |
|------------|---------|
| `pytorch-main/` | PyTorch source (reference) |
| `deepxde-master/` | DeepXDE: Physics-Informed Neural Networks library |
| `PINA-master/` | PINA: Physics-Informed Neural network Advanced |
| `[removed-vendored-example]/` | Reference PINN implementation |
| `GravNN-master/` | Gravity-informed Neural Networks |
| `hamiltonian-nn-master/` | Hamiltonian Neural Networks |
| `neural-symplectic-integrator-main/` | Neural Symplectic Integrators |
| `PyTorch-LBFGS-master/` | LBFGS optimizer for PyTorch |
| `siren/` | SIREN (Sinusoidal Representation Networks) implementation |

These are reference materials, not project dependencies. The project's own PINN implementation in `pinn/basic_architecture.py` does not import from these directories.

---

*Stack analysis: 2026-04-27*

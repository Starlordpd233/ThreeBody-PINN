# Phase 37: Developer Environment & Precision Adjudication - Research

**Researched:** 2026-07-11
**Domain:** macOS arm64 bootstrap, reproducible Python environments, PyTorch MPS automatic differentiation, and owner-adjudication evidence
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Bootstrap Entry And Idempotence
- **CTX-01:** The canonical fresh-Mac command is a root-level `./setup.sh`.
  It may delegate to focused helpers, but it must not require Make, Python, or
  a pre-existing conda installation.
- **CTX-02:** Setup detects a compatible Miniforge installation and installs
  the arm64 distribution only when needed. It never replaces an existing
  conda installation silently, and its install prefix remains configurable.
- **CTX-03:** Setup creates or validates `pinn-train`, runs verification via
  the discovered conda executable or `conda run`, avoids editing shell startup
  files, and prints the explicit interactive activation command. A second run
  is a no-op validation pass rather than a destructive rebuild.
- **CTX-04:** The setup verification must include the locked package/runtime
  contract and `torch.backends.mps.is_available() == True`.

#### Environment Provenance
- **CTX-05:** Keep a human-editable `environment.yml` and a fully pinned lock
  or `pip freeze` file under version control. Normal setup consumes and
  validates this pair; only an explicit refresh operation may rewrite the
  pinned file.
- **CTX-06:** Emit a canonical JSON environment fingerprint plus a concise
  human-readable rendering. It includes at least `sw_vers`, Python version,
  PyTorch version/build, and the pinned-lock SHA-256. Architecture and observed
  MPS availability are also recorded facts.
- **CTX-07:** Evidence runs are non-overwriting and timestamped. Preserve raw
  machine-readable output and an owner-readable Markdown summary together so
  the adjudication remains re-derivable.

#### Dual-Arm AD Evidence
- **CTX-08:** One orchestration command launches isolated fp32-MPS and
  fp64-CPU child processes through the same parameterized probe path. The MPS
  child receives `PYTORCH_ENABLE_MPS_FALLBACK` removed from its environment,
  and every arm records requested and actual device.
- **CTX-09:** Preserve the authoritative synthetic trajectory on
  `u in [0, 1]`, the legacy `u = 0.3` fixture, analytical component
  derivatives, and `relative_error < 1e-6`. Add only deterministic warmup and
  repeat work needed to time the full-Jacobian and scalar-`u` forward-mode AD
  patterns; do not replace correctness with a timing-only benchmark.
- **CTX-10:** For every arm and AD pattern, record dtype, device, fallback
  state, framework build, workload and repetition counts, raw and summary
  timings, componentwise and aggregate errors, criterion pass/fail, and any
  exception. The report presents evidence and does not recommend a precision.
- **CTX-11:** Probe completion is an explicit owner checkpoint. Do not set a
  production precision default or begin dependent Phase 38 work until the
  owner records the D1-p choice.

#### Precision And Device Seam
- **CTX-12:** Use the required `precision` and `device` config keys and resolve
  them once through a central typed helper. Pass dtype and device explicitly
  through tensor, model, and AD construction; avoid hidden global
  default-dtype mutation and scattered device checks.
- **CTX-13:** The same execution path supports the required fp32-MPS and
  fp64-CPU profiles. Validate combinations up front and fail clearly on an
  unsupported request such as fp64-MPS; never fall back silently.
- **CTX-14:** Before owner adjudication there is no implicit production
  precision default. Probe invocations select each arm explicitly. After the
  owner decides D1-p, one recorded config default may change without changing
  the implementation path.

### Claude's Discretion
- Choose exact helper/module names and CLI spelling consistent with the
  repository after research maps the new `pinn/` package layout.
- Choose the pinned-lock mechanism (`pip freeze` or an equivalent platform
  lock) that most faithfully reproduces the mixed conda/pip environment.
- Choose deterministic timing warmup/repetition counts and summary statistics;
  record the raw counts and do not invent a performance threshold.
- Choose the exact JSON field names and evidence directory layout while
  preserving non-overwrite, machine readability, and an owner-readable
  Markdown result.

### Deferred Ideas (OUT OF SCOPE)
- Model architecture, losses, and production second-order residual code belong
  to Phase 38.
- Admitted-dataset scans and `s0` ratification belong to Phase 39.
- Stage-0 training, guard calibration, and the pilot belong to Phases 40-43.

#### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` - explicitly recorded in
  `STATE.md` as a spec-side sensitivity question outside the v2.0 build phases;
  the keyword match to "dual" and "adjudication" was a false positive.
- `trainex-r1-research-handoff.md` - r1a is already ratified and consumed;
  the remaining r1b tuning round is a Future item, not Phase 37 work.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ENV-01 | One root command takes a fresh M5 Pro from no Python to an idempotently verified `pinn-train` environment with Miniforge3 arm64, Python 3.11, PyTorch 2.12 + MPS, NumPy, h5py, PyYAML, and TensorBoard. | The bootstrap state machine, installation safety rules, runtime verifier, and first-run/second-run acceptance matrix below define the executable contract. |
| ENV-02 | Setup records a machine/environment fingerprint and maintains a loose `environment.yml` plus pinned replay artifact. | The recommended mixed conda/pip pair, lock-refresh boundary, canonical JSON schema, SHA-256 handling, and drift checks below make the environment re-derivable. |
| ENV-03 | The locked section 10.3 probe runs fp32-MPS with fallback unset and fp64-CPU, times both AD patterns, and records evidence without choosing D1-p. | The isolated parent/worker architecture, locked fixture semantics, synchronized timing method, result schema, failure behavior, and owner checkpoint below cover the complete evidence path. |
| ENV-04 | One config-selected precision/device seam drives the same code path for fp32-MPS and fp64-CPU. | The typed `RuntimeSpec` resolver, explicit combination table, no-default rule, and parity tests below establish the seam later phases consume. |
</phase_requirements>

## Summary

Phase 37 should be planned as a substrate-and-evidence phase with three hard boundaries: shell bootstrap must work before Python exists; all Python work must flow through one explicit runtime seam; and the final empirical run must stop at an owner decision checkpoint. The repository has no root bootstrap, dependency file, installable `pinn` package, or dual-arm probe today. The only reusable scientific implementation is the Phase 21 `u = 0.3` fixture, while the framework specification and trainex-r1a ratification are authoritative for behavior. [VERIFIED: `.planning/codebase/{STACK,ARCHITECTURE,TESTING}.md`, `37-CONTEXT.md`, and the Phase 21 probe]

The minimum durable implementation is a root `setup.sh`, a loose `environment.yml` plus a committed fully pinned pip freeze, a narrow typed runtime resolver under `pinn/`, a same-worker AD probe invoked twice by a stdlib-only orchestrator, and timestamped JSON/Markdown evidence. Normal setup must never refresh dependencies; an explicit maintainer action owns lock regeneration. The actual probe is not a test fixture to run during planning: it is the last execution wave and its output is the input to the owner's D1-p decision. [VERIFIED: CTX-01..14; ENV-01..04]

**Primary recommendation:** Build and verify the environment first, implement the shared runtime and probe second, then run one recorded on-device evidence pass and halt at the owner checkpoint; do not let a passing or faster arm set a default automatically.

## Grounding and Scope Discipline

| Source | Authority for Phase 37 | Planning consequence |
|--------|-------------------------|----------------------|
| `37-CONTEXT.md` | Locked implementation decisions CTX-01..14 | Plans must copy these contracts into tasks and acceptance criteria rather than reopening alternatives. |
| `.planning/REQUIREMENTS.md` ENV-01..04 and `.planning/ROADMAP.md` Phase 37 | Required deliverables and success criteria | Every plan must carry explicit requirement IDs; no later-phase work may be smuggled into the seam. |
| `trainex-r1/decision-adjudication/RATIFICATION.md` | Owner-ratified D1 and explicit D1-p carve-out | PyTorch 2.12 + MPS is fixed; fp32 versus fp64 is not. |
| `trainex-r1a-resolution-doc.md` D1, B-6, and section 5 | Build rationale, fingerprint, and first-run ordering | Probe is the first build evidence; fp64-CPU remains an in-framework branch, not a separate implementation. |
| `pinn_architecture.md` sections 5.3.1 and 10.3 | Scientific trajectory, derivative semantics, and `relative_error < 1e-6` | Preserve componentwise derivatives and the `u` leaf; do not substitute a summed-output VJP. |
| `integrity-r2/CLEARANCE.md` | Authoritative pre-build clearance | Phase 37 is cleared. SL-1 is an observation measured here, not a new gate or license to broaden the probe. |
| Legacy `probe_ad.py` | Fixture semantics only | Reuse trajectory and analytical derivative behavior, but replace its single-process fp64-CPU shell. |

The build milestone may write `pinn/`, but `ctl_instruction.md` and `pinn_architecture.md` are read-only inputs. Existing v1.3 code under `pinn/` is reference-only and cannot decide precision or AD behavior. Any newly discovered spec defect must be surfaced and routed; this phase must not edit the specs. [VERIFIED: `AGENTS.md`, `.planning/PROJECT.md`, and `.planning/codebase/ARCHITECTURE.md`]

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale |
|------------|--------------|----------------|-----------|
| Fresh-Mac bootstrap | Root shell entry point | Focused shell/Python helpers after environment creation | `setup.sh` is the only command guaranteed to run before Python or Make exists. |
| Dependency intent and replay | `environment.yml` + pinned pip lock | Explicit refresh helper | Human intent and exact installed state have different lifecycles; normal setup reads both and writes neither. |
| Environment verification/fingerprint | Small Python utility executed via `conda run` | `setup.sh` orchestration | Python can inspect packages and PyTorch build reliably only after the environment exists. |
| Precision/device policy | Central typed `pinn` runtime module | Explicit YAML/CLI values | Later model, data, and training code should consume one resolved object rather than repeat dtype/device decisions. |
| AD science kernel | One parameterized worker function | Two explicit runtime profiles | Both arms and both AD patterns must share trajectory and correctness logic. |
| Process isolation/evidence | Stdlib-only parent orchestrator | Worker JSON result | The parent owns sanitized environments, exit codes, non-overwrite, and rendering; the child owns Torch imports and measurements. |
| D1-p decision | Project owner | Recorded JSON/Markdown evidence | Code reports facts only; no score, winner, recommendation, or implicit default is permitted. |

### Data flow

```text
fresh macOS arm64 shell
  -> ./setup.sh
     -> compatible Miniforge found? --no--> verify empty configurable prefix
     |                                  -> download pinned arm64 installer
     |                                  -> verify committed SHA-256
     |                                  -> batch install (no shell init)
     +-> pinn-train exists? --no--> create from loose intent + exact lock
     |                     --yes-> validate; never rebuild silently
     +-> conda run verifier
          -> package/runtime contract + MPS=True
          -> timestamped fingerprint JSON + Markdown

explicit precision-probe command
  -> create exclusive timestamped evidence directory
  -> spawn worker --precision float32 --device mps
       env copy with PYTORCH_ENABLE_MPS_FALLBACK removed before Torch import
  -> spawn worker --precision float64 --device cpu
  -> merge structured child records (including exceptions)
  -> write raw.json atomically
  -> derive owner-readable summary.md without a verdict
  -> STOP: owner records D1-p; Phase 38 remains blocked
```

## Standard Stack

### Locked core

| Component | Version/contract | Purpose | Provenance |
|-----------|------------------|---------|------------|
| Miniforge3 | macOS arm64 installer; pin a named release and its published SHA-256 in implementation | Supplies conda without assuming Homebrew or system Python | [CITED: https://github.com/conda-forge/miniforge] |
| Python | 3.11 | Project runtime | [VERIFIED: ENV-01 and ratified first-run recipe] |
| PyTorch | `2.12.*`; direct registry check on 2026-07-11 found 2.12.0 and 2.12.1 | MPS backend and `torch.func` AD | [VERIFIED: ENV-01/D1 and `pip index versions torch`] |
| NumPy | exact version captured by the committed lock | Required numerical dependency | [VERIFIED: ENV-01 and `pip index versions numpy`] |
| h5py | exact version captured by the committed lock | Required data dependency; no dataset work in this phase | [VERIFIED: ENV-01 and `pip index versions h5py`] |
| PyYAML | exact version captured by the committed lock | Reads the explicit `precision`/`device` configuration surface | [VERIFIED: ENV-01 and `pip index versions pyyaml`] |
| TensorBoard | exact version captured by the committed lock | Required later monitoring dependency; install/verify only here | [VERIFIED: ENV-01 and `pip index versions tensorboard`] |
| Python stdlib | Python 3.11 | `argparse`, `dataclasses`, `hashlib`, `json`, `pathlib`, `statistics`, `subprocess`, `time`, `unittest` | Recommendation: avoids a new runtime or test dependency for Phase 37. |

The direct package-index pass reported current releases `torch 2.13.0`, `numpy 2.5.1`, `h5py 3.16.0`, `PyYAML 6.0.3`, and `tensorboard 2.21.0`; these are registry-existence facts, not permission to upgrade the locked PyTorch major/minor or to regenerate the lock during normal setup. [VERIFIED: approved `python3 -m pip index versions` queries, 2026-07-11]

### Reproducibility pair

Use a human-maintained `environment.yml` for intent and a platform-specific `requirements-lock.txt` produced by `python -m pip freeze` inside the resolved `pinn-train` environment. The YAML should pin Python to 3.11 and PyTorch to the 2.12 line while naming the other direct requirements; the freeze must pin all pip transitive dependencies. Normal setup creates from the YAML only when the environment is absent, then installs/validates the exact lock and runs `pip check`. An existing environment is compared against the committed lock and fails with refresh/recreate instructions on drift; it is not silently updated. [CITED: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html; https://pip.pypa.io/en/stable/topics/repeatable-installs/]

`pip freeze` gives version-level repeatability but does not authenticate distribution artifacts. That limitation is acceptable because CTX-05 explicitly permits a freeze file; the plan should not add `pip-tools`, `conda-lock`, or a new lock generator unless the committed freeze proves inadequate. The Miniforge installer itself should still be protected by a committed release URL and SHA-256, and the lock file's exact bytes must be hashed into every fingerprint. [CITED: https://pip.pypa.io/en/stable/topics/repeatable-installs/]

### Package legitimacy audit

The GSD package-legitimacy seam returned `SUS` with all PyPI telemetry fields unknown for each required package. Direct approved PyPI queries independently verified every name and available release. This is a checker-telemetry limitation, not evidence of a package substitution, but the protocol requires the execution plan to retain a pre-install identity check. The package set itself is owner/requirements locked and must not be replaced. [VERIFIED: GSD legitimacy output plus direct `pip index`]

| Package | Registry verification | Seam verdict | Disposition |
|---------|-----------------------|--------------|-------------|
| `torch` | Exists; 2.12.0/2.12.1 available | SUS: registry metadata unavailable to seam | Retain (required); verify exact 2.12 lock entry before install. |
| `numpy` | Exists | SUS: registry metadata unavailable to seam | Retain (required); install only from committed lock. |
| `h5py` | Exists | SUS: registry metadata unavailable to seam | Retain (required); install only from committed lock. |
| `pyyaml` | Exists | SUS: registry metadata unavailable to seam | Retain (required); install only from committed lock. |
| `tensorboard` | Exists | SUS: registry metadata unavailable to seam | Retain (required); install only from committed lock. |

**Packages removed:** none. No unratified package is needed.

## Concrete Repository Layout

The exact names remain implementer discretion, but the planner should allocate responsibilities approximately as follows and keep legacy v1.3 modules untouched except where Phase 38 later replaces them:

```text
setup.sh                                      # only fresh-Mac entry point
environment.yml                              # loose human intent
requirements-lock.txt                        # osx-arm64 pip freeze, committed
scripts/refresh-environment-lock.sh           # only path allowed to rewrite lock
scripts/verify_environment.py                 # contract + canonical fingerprint
scripts/run_precision_probe.py                # stdlib-only parent orchestrator
pinn/__init__.py                              # establishes the rebuilt package seam
pinn/runtime.py                               # typed precision/device resolver
pinn/verification/__init__.py
pinn/verification/componentwise_ad.py         # shared worker/kernel, both arms/patterns
tests/phase37/test_setup_contract.py
tests/phase37/test_environment_fingerprint.py
tests/phase37/test_runtime.py
tests/phase37/test_componentwise_ad.py
tests/phase37/test_precision_orchestrator.py
.planning/phases/37-developer-environment-precision-adjudication/evidence/
  environment/<UTC-run-id>/{fingerprint.json,fingerprint.md}
  precision/<UTC-run-id>/{raw.json,summary.md}
```

Recommendations:

- Keep the parent orchestrator free of Torch imports so each child starts with a clean backend process and the MPS environment is sanitized before Torch import.
- Keep `pinn/runtime.py` small: an immutable `RuntimeSpec` plus `resolve_runtime(precision, device)`. Do not create model, loss, data, or training abstractions in this phase.
- Treat evidence paths as outputs, not mutable "latest" files. A UTC timestamp with microseconds is readable, but directory creation must still use exclusive semantics and fail on collision.
- Use temporary files followed by `os.replace` for `raw.json` and `summary.md`; exclusive directory creation provides non-overwrite, while atomic replacement protects each new file from partial writes.
- Keep generated evidence in the phase-local directory already used by planning and verification artifacts so the owner decision is reviewable and commit-able with its provenance.

## Implementation Patterns

### 1. Bootstrap as a fail-closed state machine

`setup.sh` should use `set -euo pipefail`, resolve its own repository root, and reject non-Darwin or non-arm64 hosts before downloading anything. Discovery order should be explicit: a user-supplied conda executable/prefix, the configured Miniforge prefix, the conventional Miniforge prefix, then `PATH`. A candidate is compatible only after executable, root-prefix, and `osx-arm64` platform checks pass. If an incompatible conda or occupied target prefix is found, stop with exact remediation; never invoke the installer's update/overwrite option. [CITED: https://github.com/conda-forge/miniforge]

Download a pinned `Miniforge3-MacOSX-arm64.sh` into `mktemp -d`, validate its committed SHA-256 with macOS `shasum -a 256`, invoke `bash installer -b -p "$MINIFORGE_PREFIX"`, and clean the temporary directory with a trap. Do not pipe a network response into a shell and do not call `conda init`. Official Miniforge documents batch installation with `-b -p` and notes that non-interactive installation does not initialize the shell. [CITED: https://github.com/conda-forge/miniforge]

A child script cannot activate an environment in its parent shell. Therefore "ready/activated" means setup creates and verifies `pinn-train` via the discovered conda executable, then prints the exact user command `source <prefix>/etc/profile.d/conda.sh && conda activate pinn-train`; this is the CTX-03 interpretation and should be tested literally. [VERIFIED: CTX-03]

### 2. Separate create, validate, and refresh

Use three explicit modes rather than one mutating path:

| Mode | Allowed mutation | Required outcome |
|------|------------------|------------------|
| First normal run, env absent | Install Miniforge only if absent; create `pinn-train` from committed pair | Verify packages, MPS, lock equality, and write a new fingerprint. |
| Normal rerun, env present | None to Miniforge, environment, YAML, or lock | Re-run validation and fingerprint; report no-op success. |
| Explicit lock refresh | Resolve loose intent in `pinn-train`, validate, rewrite pinned freeze | Show diff; caller reviews/commits it. Never triggered by plain `./setup.sh`. |

Do not use `conda env update` on every setup invocation: it turns a validation rerun into a solver run and can change the environment before the lock is checked. Compare normalized installed distributions to the committed freeze and fail on missing, changed, or extra project packages. [VERIFIED: CTX-03/05; recommendation grounded in the non-mutation contract]

### 3. Canonical fingerprint

The Python verifier should emit deterministic UTF-8 JSON (`sort_keys=True`, fixed indentation, trailing newline) and derive the Markdown rendering from the same in-memory object. Minimum fields:

```text
schema_version
captured_at_utc
repository_commit
platform.product_name/version/build
platform.machine
conda.executable/base_prefix/environment_prefix/version
python.version/executable
packages.required_versions
torch.version/git_version/configuration
torch.mps.is_built/is_available/device_count
lock.path/sha256
verification.status/checks[]
```

Capture `sw_vers` as structured key/value data, not an opaque transcript. Record only the fields needed for reproduction; do not dump all environment variables or conda configuration because those can contain credentials or machine-specific noise. Fingerprint generation must fail if the lock path is missing, the hash cannot be computed, the Python line is not 3.11, Torch is not 2.12, a required import/version check fails, or MPS is unavailable. [VERIFIED: CTX-04/06 and ENV-01/02]

### 4. One typed runtime seam

The resolver should accept exactly the public strings required by CTX-12:

| `precision` | `device` | Resolution before D1-p |
|-------------|----------|------------------------|
| `float32` | `mps` | Valid explicit probe/runtime profile -> `torch.float32`, `torch.device("mps")` |
| `float64` | `cpu` | Valid explicit reference/escape profile -> `torch.float64`, `torch.device("cpu")` |
| `float64` | `mps` | Reject before tensor construction; no silent CPU conversion |
| `float32` | `cpu` | Not a ratified Phase 37 profile; reject unless a later grounded requirement adds it |
| omitted | omitted or partial | Reject: no production default exists before the owner checkpoint |

Return an immutable object and pass its `dtype` and `device` explicitly to every tensor and AD call. Never call `torch.set_default_dtype`, never infer device from availability, and never catch an MPS exception to rerun on CPU. The only CPU path is the explicitly requested fp64-CPU arm through the same code. [VERIFIED: CTX-12..14]

### 5. Isolated dual-arm worker protocol

The orchestrator should use `subprocess.run` with an argument list, captured stdout/stderr, a timeout, and a copied environment. For the MPS child it must remove `PYTORCH_ENABLE_MPS_FALLBACK` from that copy. The worker must inspect/record the key before importing Torch (stdlib imports first, Torch import inside the worker entry), then resolve the explicit profile. PyTorch documents that setting this variable to `1` enables CPU fallback for unsupported MPS operations; an unset key is the required fail-closed state. [CITED: https://docs.pytorch.org/docs/stable/mps_environment_variables.html; https://docs.python.org/3/library/subprocess.html]

Each child writes one JSON object to stdout and sends diagnostics to stderr. The parent records nonzero exits, malformed output, timeouts, signals, and worker exceptions as arm results rather than erasing the entire run. It must never synthesize a successful CPU result for a failed MPS child. Record requested device, resolved device, and the actual device of the input and result tensors; mismatch is failure evidence. [VERIFIED: CTX-08/10/13]

### 6. Locked correctness plus synchronized timing

Both AD patterns must call the same trajectory function at the preserved `u = 0.3` fixture in the authoritative domain `[0,1]`:

```text
r(u)  = [sin(2*pi*u), cos(2*pi*u), u^2]
r'(u) = [2*pi*cos(2*pi*u), -2*pi*sin(2*pi*u), 2*u]
```

The full-Jacobian arm should use the supported full-Jacobian transform (for example `torch.func.jacrev`); the scalar-`u` forward-mode arm should use `torch.func.jvp` with a scalar unit tangent. With a scalar input, JVP returns every output component derivative without a summed-output VJP. PyTorch documents `jacrev` as reverse-mode Jacobian and `jvp` as forward-mode AD. [CITED: https://docs.pytorch.org/docs/stable/func.api; VERIFIED: `pinn_architecture.md` 5.3.1/10.3]

Correctness is evaluated outside the timing loop for every arm/pattern. Record predicted and analytical vectors, signed deltas, componentwise absolute/relative errors, aggregate norm-relative error, finite checks, and `aggregate_relative_error < 1e-6`. Do not add a precision-dependent tolerance and do not test only elapsed time. This phase's locked probe is first-derivative componentwise AD; production second-order residual work remains Phase 38. [VERIFIED: CTX-09 and section 10.3]

Recommended fixed measurement protocol (agent-discretion choice):

- 10 untimed warmup iterations per arm/pattern;
- 30 raw timing samples;
- 100 identical derivative evaluations per sample, with elapsed time normalized per evaluation;
- `time.perf_counter_ns()` for the monotonic high-resolution clock;
- `torch.mps.synchronize()` immediately before and after each MPS sample so asynchronous kernels are inside the timed interval;
- raw samples plus count, median, p25, p75, min, and max; no pass/fail or winner threshold on timing.

The counts are workload metadata, not calibrated performance thresholds. PyTorch's MPS synchronizer waits for all kernels to complete, and Python recommends `perf_counter_ns` for short-duration measurement without float precision loss. [CITED: https://docs.pytorch.org/docs/stable/generated/torch.mps.synchronize.html; https://docs.python.org/3/library/time.html#time.perf_counter_ns]

### 7. Evidence is append-only and verdict-free

Create the run directory exclusively before spawning either child. Write a raw schema containing the fingerprint reference/hash, orchestration metadata, both arm results, both pattern results, raw timings, summary statistics, errors, and exceptions. Render `summary.md` strictly from `raw.json` and include a checklist of scientific criteria plus a prominent statement: "Owner decision required; no D1-p verdict is recorded by this report." Do not rank arms, label a winner, recommend a default, or mutate configuration. [VERIFIED: CTX-07/10/11/14]

## Common Pitfalls

### Pitfall 1: Setup accidentally depends on the thing it installs
**What goes wrong:** `setup.sh` invokes Python, Make, conda shell functions, or non-system tooling before Miniforge exists.
**How to avoid:** Keep the pre-environment prefix POSIX/macOS shell plus system `curl`, `shasum`, `uname`, `sw_vers`, and `bash`; use Python only through `conda run` after creation.
**Warning sign:** A fresh-shell test fails before installer discovery.

### Pitfall 2: "Idempotence" silently mutates the environment
**What goes wrong:** Every rerun performs `conda env update`, rewrites the freeze, or replaces a pre-existing prefix.
**How to avoid:** Branch explicitly on state; normal existing-env behavior is validation only, and lock refresh is a separate command.
**Warning sign:** A clean second run changes files, package versions, or solver state.

### Pitfall 3: Latest installer undermines replay and supply-chain review
**What goes wrong:** A moving `releases/latest` URL changes the bootstrap substrate without a repository diff.
**How to avoid:** Commit a named Miniforge release URL and expected SHA-256; make upgrades reviewed changes.
**Warning sign:** Two machines download different installer bytes from the same repository revision.

### Pitfall 4: A child script claims to activate the caller's shell
**What goes wrong:** Setup reports activation even though environment changes cannot propagate to the parent process.
**How to avoid:** Verify with `conda run` and print the exact `source ... && conda activate pinn-train` handoff.
**Warning sign:** `python -V` in the caller remains the system Python after setup claims activation.

### Pitfall 5: Fallback is changed after Torch import
**What goes wrong:** Backend state may already be initialized, and evidence cannot establish the requested policy.
**How to avoid:** Sanitize the child environment in the parent and inspect it before the worker imports Torch.
**Warning sign:** Orchestrator imports Torch or a Torch-importing module at top level.

### Pitfall 6: MPS timing omits synchronization
**What goes wrong:** Host timing measures enqueue latency while GPU work completes later.
**How to avoid:** Synchronize immediately around every measured MPS sample and store raw samples.
**Warning sign:** Impossibly small or unstable MPS timings that change when later operations run.

### Pitfall 7: Two arms drift into two implementations
**What goes wrong:** Precision, trajectory, or AD logic differs across scripts, invalidating comparison.
**How to avoid:** One worker and one trajectory function; only the resolved runtime profile changes.
**Warning sign:** Separate `probe_mps.py` and `probe_cpu.py` contain duplicated math.

### Pitfall 8: Aggregate-only correctness hides component errors
**What goes wrong:** A correct-looking norm conceals a wrong component or a forbidden summed-output VJP.
**How to avoid:** Preserve all component values/errors and the aggregate criterion; explicitly test the known analytical vector.
**Warning sign:** JSON has one error scalar but no derivative vector.

### Pitfall 9: Evidence chooses D1-p indirectly
**What goes wrong:** A "fastest passing arm" field, ordered recommendation, or default config turns evidence into an agent verdict.
**How to avoid:** Use symmetric presentation, no threshold on time, and finish with an owner checkpoint.
**Warning sign:** Any execution task after the probe changes `precision` or starts Phase 38 without an owner record.

### Pitfall 10: Fingerprint captures secrets or cannot be re-derived
**What goes wrong:** Dumping all environment variables leaks credentials, while omitting the lock hash loses package provenance.
**How to avoid:** Use an allowlisted schema, hash exact committed lock bytes, and derive Markdown from JSON.
**Warning sign:** Fingerprint contains tokens/home configuration or lacks a schema version and lock SHA-256.

## Don't Hand-Roll

| Problem | Do not build | Use instead | Why |
|---------|--------------|-------------|-----|
| Python distribution | Custom Python installer/Homebrew bootstrap | Official Miniforge arm64 batch installer | The locked substrate is Miniforge and its installer already handles prefix layout. |
| Dependency solver | Custom version-resolution code | conda for Python/pip substrate plus committed pip freeze | Resolution and replay remain inspectable with standard tools. |
| AD engine | Finite differences or symbolic derivative framework | `torch.func.jacrev` and `torch.func.jvp` | The phase is specifically validating the in-framework AD contract. |
| MPS timing primitive | Sleep, host-only timestamp, or bespoke event loop | `perf_counter_ns` plus `torch.mps.synchronize` | Captures elapsed host time only after queued MPS work completes. |
| Process protocol | Shell-string commands or multiprocessing globals | `subprocess.run` with argv/env and JSON stdout | Gives explicit environment isolation and re-derivable failures. |
| Test framework | New pytest dependency solely for Phase 37 | Existing stdlib `unittest` pattern | The repository has no project-wide pytest configuration and stdlib suffices. |
| Owner decision logic | Automated score/winner | Explicit checkpoint consuming raw + Markdown evidence | D1-p is owner-carved. |

## Recommended Plan and Wave Decomposition

### Wave 0 — Verification scaffolding and contracts

Create `tests/phase37/` and contract tests before implementation. Cover bootstrap state transitions with fake executables/prefixes, fingerprint schema/hash behavior, runtime-combination validation, locked analytical fixture behavior on CPU, subprocess environment sanitation, non-overwrite, and verdict-free rendering. This wave owns no empirical run and installs nothing. It makes later tasks independently checkable. [VERIFIED: Nyquist enabled in `.planning/config.json`; repository testing map]

### Wave 1 — Reproducible fresh-Mac substrate (ENV-01, ENV-02)

Implement `environment.yml`, the explicit lock-refresh path, the committed pinned lock, root `setup.sh`, and environment verification/fingerprinting. Run targeted unit/contract tests first; then perform the authorized real bootstrap once on the M5 Pro and immediately run it a second time to prove no-op validation. Record a timestamped fingerprint. The lock-refresh act is a logical boundary: inspect and commit the generated lock/fingerprint evidence so later waves run against fixed bytes.

Wave 1 acceptance must prove: configurable prefix; no silent replacement; no shell-file edits; Python 3.11; Torch 2.12; all required imports; MPS built/available; `pip check`; installed-versus-lock equality; exact lock hash; JSON/Markdown agreement; second run makes no environment or repository changes except a new non-overwriting fingerprint if evidence-per-run is intended.

### Wave 2 — Shared runtime seam and probe kernel (ENV-04, part of ENV-03)

Establish the minimal importable `pinn` package seam, immutable runtime resolver, one synthetic-trajectory function, analytical derivative, and both AD methods. Add explicit profile/parity tests and rejection tests for omitted/default/unsupported combinations. Run correctness on fp64-CPU during development; do not execute or interpret the empirical dual-arm evidence yet.

Wave 2 acceptance must prove both valid profiles resolve through the same object/function path; dtype/device are explicit; global default dtype is unchanged; fp64-MPS and omitted values fail before tensor construction; the legacy `u=0.3` component vector and aggregate criterion pass on the CPU reference.

### Wave 3 — Isolated orchestration and evidence renderer (ENV-03)

Implement the stdlib parent process, worker protocol, sanitized MPS environment, timeouts/error capture, synchronized measurement loop, raw schema, atomic/non-overwriting persistence, and Markdown renderer. Tests should use temporary directories and injected/fake child outputs for failure paths, plus cheap real CPU worker coverage. Do not allow a failed MPS child to trigger fallback.

Wave 3 acceptance must prove two explicit child commands use the same module; MPS env lacks the fallback key before Torch import; requested/resolved/actual device are recorded; every required CTX-10 field is present for success and exception records; raw timings and summaries are consistent; rerunning never overwrites; summary contains no recommendation/default/winner.

### Wave 4 — On-device evidence and owner checkpoint

Run the complete setup verifier, then the one orchestration command in the fixed environment. Validate raw JSON against the required schema, regenerate/compare the Markdown summary, inspect git diff for only intended code/tests/lock/evidence, and file the timestamped evidence. Do not change a production precision default. Present the two-arm record to the owner and stop.

The terminal checkpoint question is only: **Which D1-p branch does the owner record—fp32-MPS or fp64-CPU—given the attached correctness, failure, and timing evidence?** Phase 38 remains blocked until that instruction is recorded. If an arm throws, misses the locked correctness criterion, runs on a different actual device, or has fallback enabled, that is evidence for the owner; the agent must not repair the result by selecting the other arm.

### Dependency graph

```text
Wave 0 tests/contracts
      -> Wave 1 environment + lock + fingerprint
             -> Wave 2 runtime seam + shared AD kernel
                    -> Wave 3 dual-arm orchestration + evidence format
                           -> Wave 4 real probe + owner checkpoint
                                  -X-> Phase 38 until owner D1-p record
```

## Validation Architecture

### Test framework

| Property | Value |
|----------|-------|
| Framework | Python 3.11 standard-library `unittest`; shell syntax via `bash -n` |
| Config file | None required; repository currently has no project-wide Python test configuration |
| Test root | `tests/phase37/` |
| Quick run command | `conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py'` |
| Full phase command | `bash -n setup.sh scripts/refresh-environment-lock.sh && conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py' && conda run -n pinn-train python scripts/verify_environment.py --check-only` |
| Hardware/evidence command | The implemented precision orchestrator command; run only in Wave 4, not during research or ordinary unit sampling |

### Phase requirements to test map

| Req ID | Behavior | Test type | Automated command | Planned file/status |
|--------|----------|-----------|-------------------|---------------------|
| ENV-01 | Shell entry has no Python/Make/conda prerequisite before discovery; rejects wrong platform; installs only to empty configurable prefix; existing compatible install is reused. | Shell contract + unit with fake tools/temp prefixes | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract` | `tests/phase37/test_setup_contract.py` — Wave 0 |
| ENV-01 | Environment contains Python 3.11, Torch 2.12, required imports, and MPS available. | On-host integration | `./setup.sh` followed by `conda run -n pinn-train python scripts/verify_environment.py --check-only` | Wave 1 hardware gate |
| ENV-01 | Second setup invocation is a no-op validation pass. | On-host integration + before/after snapshots | Run `./setup.sh` twice; compare conda package/freeze state and repository diff | Wave 1 hardware gate; cannot be fully simulated by unit tests |
| ENV-02 | Loose and pinned files exist; normal setup cannot rewrite lock; explicit refresh is the only writer. | Unit/contract | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract.TestLockBoundary` | Wave 0/1 |
| ENV-02 | Fingerprint JSON is canonical and includes required OS, architecture, Python, Torch build, MPS, and lock hash fields; Markdown derives from JSON. | Unit + integration | `conda run -n pinn-train python -m unittest tests.phase37.test_environment_fingerprint` | Wave 0/1 |
| ENV-02 | Installed environment matches committed lock and `pip check` passes. | Integration | `conda run -n pinn-train python scripts/verify_environment.py --check-only` | Wave 1 |
| ENV-03 | Locked trajectory/analytical derivative and aggregate threshold are preserved for both methods. | Scientific unit | `conda run -n pinn-train python -m unittest tests.phase37.test_componentwise_ad` | Wave 2 |
| ENV-03 | Orchestrator launches two isolated same-path children and removes fallback from MPS environment before Torch import. | Unit/subprocess integration | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator` | Wave 3 |
| ENV-03 | MPS timings synchronize, raw sample counts match declared workload, summaries recompute from raw values, all CTX-10 fields and exceptions are serializable. | Unit with injected clock/synchronizer + schema checks | Targeted methods in `test_componentwise_ad.py` and `test_precision_orchestrator.py` | Wave 2/3 |
| ENV-03 | Actual fp32-MPS and fp64-CPU run produces valid non-overwriting raw + Markdown evidence and no verdict. | On-host scientific integration/manual owner gate | Implemented precision orchestration command, then JSON validator/tests | Wave 4 only |
| ENV-04 | Valid pairs map to exact Torch dtype/device through one resolver; omitted/partial/unsupported pairs fail; global dtype is not mutated. | Unit | `conda run -n pinn-train python -m unittest tests.phase37.test_runtime` | Wave 2 |
| ENV-04 | Both probe arms call identical worker/kernel code and differ only in explicit profile. | Unit/subprocess integration | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator` | Wave 3 |

### Required negative tests

- Occupied install prefix without a compatible Miniforge executable -> fail without deletion or update.
- Non-arm64 or non-macOS host -> fail before network access.
- Existing `pinn-train` with wrong Python/Torch/package lock -> fail with explicit drift instructions; do not auto-rebuild.
- Plain `./setup.sh` when lock is missing -> fail; do not generate a new lock.
- Lock refresh invoked implicitly or normal setup changes lock bytes -> test failure.
- `torch.backends.mps.is_available() == False` -> ENV-01 verification failure.
- Missing `precision` or `device`, `float64+mps`, and unratified `float32+cpu` -> resolver failure before tensor creation.
- MPS child environment still contains `PYTORCH_ENABLE_MPS_FALLBACK` -> worker failure recorded.
- Requested device differs from actual tensor/result device -> criterion failure.
- Child timeout, signal, malformed JSON, or Torch exception -> structured exception record; no fallback child.
- Aggregate error equal to or above `1e-6`, any non-finite component, or component vector mismatch -> correctness failure.
- Reused evidence run ID/path -> fail without overwriting.
- Markdown contains `recommend`, `winner`, `choose`, or a production default assertion -> renderer/contract failure, allowing only the fixed "owner decision required" language.

### Sampling rate

- **Per task commit:** run the narrow test module owned by the task plus `git diff --check`.
- **Per wave merge:** run `bash -n` for changed shell scripts and the complete `tests/phase37` discovery command.
- **After Wave 1:** run the real environment verifier and `pip check`; inspect the fingerprint and committed lock hash.
- **After Wave 3:** run the CPU worker and orchestrator failure-path suite; do not run the empirical MPS arm merely as incidental regression sampling.
- **Phase gate (Wave 4):** full phase suite; setup first/second-run evidence; actual dual-arm command; raw-schema/Markdown re-derivation; exact repository diff review; owner checkpoint.

### Wave 0 gaps

- [ ] `tests/phase37/__init__.py` and the five test modules above do not exist.
- [ ] No fake-conda/fake-installer fixture exists for destructive-path-free bootstrap tests.
- [ ] No canonical environment fingerprint or precision evidence schema exists.
- [ ] No project-wide test runner/config exists; use `unittest` rather than introducing one.
- [ ] The actual MPS integration cannot run until Wave 1 creates `pinn-train`; mark it as a hardware gate, not a Wave 0 blocker.

### Manual-only justification

Two acceptance checks cannot be made cheap, hermetic, or sub-30-second: installing Miniforge/Torch on a genuinely fresh Mac, and timing real MPS kernels. Unit tests must cover their control flow, but Phase 37 still requires one on-target first run, second run, and dual-arm evidence run. Those commands are network/hardware-heavy and should execute only in their designated waves with their outputs retained. The owner D1-p selection itself is intentionally manual and is not a test assertion. [VERIFIED: ENV-01/03, CTX-11]

## Security Domain

### Applicable controls

| Area | Applies | Required control |
|------|---------|------------------|
| Authentication/session/access control | No | No service or user identity surface in this phase. |
| Input validation | Yes | Validate platform, architecture, prefix state, CLI/YAML enum values, schema version, and child JSON before use. Use `yaml.safe_load` if YAML is read. |
| Supply chain | Yes | Named Miniforge release + committed SHA-256; HTTPS; no curl-to-shell; committed exact dependency lock; registry identity preflight. |
| Command injection | Yes | Quote all shell paths; use subprocess argv lists with `shell=False`; never interpolate config values into a shell command. |
| Filesystem integrity | Yes | Configurable prefix must be empty or verified; evidence directory creation is exclusive; files are atomic; no recursive deletion in normal setup. |
| Secret minimization | Yes | Fingerprint uses an allowlist and never dumps full environment variables, shell files, pip config, or credentials. |
| Availability/DoS | Limited | Child timeouts prevent a hung probe; this is local single-machine work, not a network service. |

### Threat patterns

| Pattern | Risk | Mitigation |
|---------|------|------------|
| Moving installer asset or tampered download | Executes unreviewed code | Pin release and expected SHA-256; verify before `bash`. |
| Prefix confusion | Overwrites an existing conda/user installation | Verify exact prefix and conda metadata; stop on incompatibility; no `-u`, deletion, or replacement. |
| Dependency drift | Evidence cannot be replayed | Exact committed freeze, installed-state comparison, lock SHA in fingerprint, explicit-only refresh. |
| MPS fallback masquerades as GPU success | Invalid D1-p evidence | Remove env key before import, record its absence and actual devices, fail on mismatch. |
| Shell injection via path/config | Arbitrary command execution | Quote shell variables; subprocess argv lists; enum-validated runtime keys. |
| Evidence overwrite/tampering | Loses or rewrites owner-decision basis | Exclusive timestamped directory, atomic writes, raw JSON source of truth, committed evidence. |
| Fingerprint oversharing | Leaks tokens or local secrets | Field allowlist; do not record environment dumps or user configuration. |

## Environment Availability

The research host was observed as `arm64`, macOS 26.5.1, with system Python 3.14.6. No `conda` executable and no importable Torch installation were found. This is useful validation of the bootstrap premise, but no packages were installed and the empirical probe was not executed during research. [VERIFIED: local read-only availability audit, 2026-07-11]

| Dependency | Required by | Available before execution | Version/state | Fallback |
|------------|-------------|----------------------------|---------------|----------|
| macOS arm64 | ENV-01/03 | Yes | arm64 / macOS 26.5.1 | None; wrong platform must fail. |
| Miniforge/conda | ENV-01/02 | No | Not found | `setup.sh` installs pinned Miniforge to configurable empty prefix. |
| Python 3.11 | ENV-01 | No | System Python is 3.14.6 | Created only inside `pinn-train`; do not use system Python as runtime. |
| PyTorch 2.12 + MPS | ENV-01/03/04 | No | Not importable | Installed from committed lock; no framework fallback. |
| NumPy/h5py/PyYAML/TensorBoard | ENV-01 | Not audited as installed | Lock-required | Installed from committed lock. |

## Assumptions Log

No ungrounded semantic assumption is required to plan the phase. The proposed filenames, `pip freeze` lock choice, evidence schema names, and fixed timing counts are recommendations within the explicit Agent Discretion granted by `37-CONTEXT.md`; the planner may adjust their spelling while preserving behavior. Actual resolved transitive versions, Miniforge installer checksum, MPS kernel behavior, timings, and D1-p are execution facts and must not be guessed in PLAN.md.

## Open Questions and Checkpoints

1. **Initial lock contents and installer digest**
   - Known: the lock mechanism and version lines are grounded; normal setup must consume committed bytes.
   - Execution fact: the exact transitive freeze and official installer SHA-256 must be obtained and verified during Wave 1.
   - Handling: make lock refresh and digest verification explicit tasks with diff review; do not leave placeholders in a completed wave.

2. **Actual dual-arm outcome**
   - Known: both profiles, methods, criterion, workload metadata, and evidence fields are fixed.
   - Execution fact: correctness, exceptions, and timing on the M5 Pro are unknown until Wave 4.
   - Handling: record results symmetrically and continue only to the owner checkpoint.

3. **D1-p**
   - Known: it is owner-carved and every later implementation must use the seam.
   - Unknown by design: which profile becomes the production default.
   - Handling: no plan task may answer it; Wave 4 ends with the owner decision request and blocks Phase 38.

## Sources

### Primary repository sources (HIGH confidence)

- `.planning/phases/37-developer-environment-precision-adjudication/37-CONTEXT.md` — CTX-01..14, discretion, scope, and canonical source map.
- `.planning/REQUIREMENTS.md` — ENV-01..04 and v2.0 source discipline.
- `.planning/ROADMAP.md` — Phase 37 goal/success criteria and milestone verification protocol.
- `.planning/PROJECT.md` and `.planning/STATE.md` — M5 Pro viability-slice boundary, owner-carved doctrine, and integrity-r2/branch state.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — ratified D1 and D1-p carve-out.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` — D1 rationale, B-6 fingerprint, and section 5 recipe.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` sections 5.3.1 and 10.3 — componentwise AD and locked synthetic criterion.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — read-only companion constraint.
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md` and supporting `MASTER-FINAL-RESOLUTION.md` — cleared gate and SL-1 observation.
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py` — legacy fixture behavior.
- `.planning/codebase/STACK.md`, `ARCHITECTURE.md`, `TESTING.md` — repository package/test baseline.
- `AGENTS.md` and `.claude/rules/{pinn-reference,repo-map}.md` — governance and path constraints.

### Official external sources (HIGH/MEDIUM confidence)

- https://github.com/conda-forge/miniforge — macOS arm64 asset, non-interactive `-b -p`, no automatic shell init, and published checksums.
- https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html — environment export/replay and exact platform specifications.
- https://pip.pypa.io/en/stable/topics/repeatable-installs/ — pinned freeze behavior and hash-checking tradeoffs.
- https://docs.pytorch.org/docs/stable/notes/mps.html — MPS availability/build checks and device use.
- https://docs.pytorch.org/docs/stable/mps_environment_variables.html — CPU fallback environment variable semantics.
- https://docs.pytorch.org/docs/stable/func.api — `jacrev` and `jvp` AD semantics.
- https://docs.pytorch.org/docs/stable/generated/torch.mps.synchronize.html — MPS completion barrier for timing.
- https://docs.python.org/3/library/time.html#time.perf_counter_ns — monotonic high-resolution timing.
- https://docs.python.org/3/library/subprocess.html — explicit child environment and argv-based process execution.
- Direct PyPI registry queries (`pip index versions`) on 2026-07-11 — package identity/version availability only.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — exact framework/runtime line and packages are owner/requirements locked and registry-verified.
- Architecture: HIGH — all boundaries derive from CTX-01..14 and established repository patterns.
- Scientific probe: HIGH for fixture/criterion/process; empirical outcome intentionally unknown until execution.
- Bootstrap edge behavior: HIGH — official Miniforge/conda/pip documentation plus explicit locked idempotence requirements.
- Validation architecture: HIGH — maps every ENV requirement to unit, integration, hardware, and owner gates without inventing a new framework.

**Research date:** 2026-07-11
**Valid until:** 2026-08-10 for tool/release details; repository contracts remain valid until explicitly revised.

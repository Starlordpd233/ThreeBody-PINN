# Phase 37: Developer Environment & Precision Adjudication - Pattern Map

**Mapped:** 2026-07-11  
**Implementation/source targets mapped:** 18 file families and runtime outputs  
**Closest repository analogs:** 5 partial structural analogs; 1 semantic fixture  

> Phase 37 is the first build phase in this track. Repository precedents are therefore
> mostly conventions, not implementations to copy. `37-CONTEXT.md` (CTX-01..14),
> `37-RESEARCH.md`, ENV-01..04, and the read-only framework sources remain authoritative
> wherever this map says "no complete analog." Existing v1.3 files under `pinn/` are
> reference-only. The Phase 21 AD probe is a fixture to preserve and extend, not the
> Phase 37 implementation. This map does not run the hardware probe or choose D1-p.

## End-to-End Data Flow

All `evidence/` paths in this map are relative to
`.planning/phases/37-developer-environment-precision-adjudication/`.

```text
setup.sh
  -> validate Darwin/arm64 and discover/install pinned Miniforge
  -> environment.yml (human intent) + requirements-lock.txt (exact replay)
  -> create or validate pinn-train without rewriting the lock
  -> scripts/verify_environment.py
  -> evidence/environment/<UTC-run-id>/{fingerprint.json,fingerprint.md}

explicit precision-probe command
  -> scripts/run_precision_probe.py (stdlib-only parent; no Torch import)
  -> isolated child: precision=float32, device=mps, fallback key removed
  -> isolated child: precision=float64, device=cpu
  -> both children use pinn.runtime + pinn.verification.componentwise_ad
  -> evidence/precision/<UTC-run-id>/{raw.json,summary.md}
  -> STOP for owner D1-p decision
```

The two paths meet at provenance: every fingerprint hashes the exact committed lock,
and the precision evidence records the framework build and actual runtime facts. They
do not meet at policy: neither environment validation nor probe rendering may select a
production precision default.

## File Classification

| New File / Runtime Output | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `setup.sh` | shell controller / sole fresh-Mac entry | host + configured prefix -> installed or validated `pinn-train` -> verifier | `scripts/setup-git-hooks.sh` | partial: shell/error style only |
| `environment.yml` | human-maintained dependency intent | direct requirements -> first environment solve | none in project-owned code | no suitable analog |
| `requirements-lock.txt` | generated replay config | explicit refresh -> exact installed versions -> setup drift check + fingerprint hash | none in project-owned code | no suitable analog |
| `scripts/refresh-environment-lock.sh` | privileged maintenance command | validated `pinn-train` -> `pip freeze` -> reviewed lock replacement | `scripts/setup-git-hooks.sh` | partial: shell style only |
| `scripts/verify_environment.py` | contract verifier + evidence renderer | allowlisted host/runtime/package facts + lock bytes -> canonical object -> JSON/Markdown | `scripts/git_policy/agent_presence.py` | partial: atomic JSON write only |
| `scripts/run_precision_probe.py` | stdlib subprocess orchestrator + evidence renderer | two explicit profiles -> isolated child JSON -> raw record + Markdown summary | `tests/watchdog/test_contract.py` | partial: argv/env/subprocess test conventions only |
| `pinn/__init__.py` | rebuilt package marker | establishes importable `pinn` seam for Phase 37+ | empty `pinn/data-handling/**/__init__.py` markers | weak; v1.3 reference-only |
| `pinn/runtime.py` | typed runtime policy seam | required `precision` + `device` -> immutable dtype/device specification | none | no suitable analog |
| `pinn/verification/__init__.py` | verification package marker | exposes no policy; supports module execution/imports | existing empty package markers | conventional only |
| `pinn/verification/componentwise_ad.py` | shared scientific kernel + child worker | explicit runtime profile -> two AD patterns -> one structured arm record | Phase 21 `probes/probe_ad.py` | semantic fixture, incomplete shell |
| `tests/phase37/__init__.py` | test package marker | enables targeted `python -m unittest tests.phase37...` commands | package markers elsewhere | conventional only |
| `tests/phase37/test_setup_contract.py` | bootstrap contract tests | fake tools/prefixes -> setup state/side-effect assertions | `tests/watchdog/test_contract.py` | strong test-harness match |
| `tests/phase37/test_environment_fingerprint.py` | schema/provenance tests | fake facts + lock bytes -> canonical JSON/Markdown/hash assertions | `tests/git_policy/test_git_policy.py` | partial: temp-file/subprocess style |
| `tests/phase37/test_runtime.py` | typed seam unit tests | precision/device cases -> resolved spec or fail-fast error | `tests/git_policy/test_git_policy.py` | test-style match; no domain analog |
| `tests/phase37/test_componentwise_ad.py` | scientific correctness/timing-contract tests | locked fixture -> component and aggregate assertions | Phase 21 `probe_ad.py` | strong fixture match |
| `tests/phase37/test_precision_orchestrator.py` | process/evidence integration tests | fake child outcomes/env -> isolation, failure, non-overwrite, wording assertions | watchdog tests | strong harness match |
| `evidence/environment/<UTC-run-id>/{fingerprint.json,fingerprint.md}` | append-only environment evidence | one canonical verifier object -> machine + owner renderings | prior phase-local `evidence/` retention | location match only; no paired schema analog |
| `evidence/precision/<UTC-run-id>/{raw.json,summary.md}` | append-only adjudication evidence | complete symmetric arm records -> raw + verdict-free summary | Phase 21 `evidence/probe_ad.stdout.txt` | fixture retention only; no paired schema analog |

The `evidence/` rows are runtime outputs, not mutable `latest` files. The implementation
creates each run directory exclusively and fails on collision. Standard GSD artifacts
(`37-PLAN.md`, summaries, and verification reports) are workflow outputs, not Phase 37
implementation targets for this map.

## Pattern Assignments

### 1. Bootstrap and dependency provenance

**Structural analog:** `scripts/setup-git-hooks.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if [ "$actual" != ".githooks" ]; then
  echo "git policy: expected core.hooksPath=.githooks, got '$actual'" >&2
  exit 1
fi
```

Copy the strict-mode, quoted-variable, explicit-stderr, and nonzero-exit conventions.
Do not copy the Git-dependent root discovery literally: the fresh-Mac entry point must
resolve its own script location and must operate before project Python or Make exists.

The semantic bootstrap contract has no repository analog. Follow the locked state
machine instead:

- Reject non-Darwin or non-`arm64` before any download.
- Discover a user-supplied conda executable/prefix first, then the configured
  Miniforge prefix, conventional prefix, and `PATH`; accept a candidate only after
  executable, root-prefix, and `osx-arm64` checks.
- If installation is needed, use a named official Miniforge arm64 release and committed
  SHA-256, a `mktemp -d` directory with cleanup trap, `shasum -a 256`, and batch install
  (`bash installer -b -p "$MINIFORGE_PREFIX"`). Never pipe a download into a shell,
  overwrite an occupied prefix, call `conda init`, or edit shell startup files.
- Treat environment states explicitly: absent -> create from intent and exact lock;
  present + exact -> validate/no-op; present + drift -> fail with refresh/recreate
  instructions; incompatible prefix/platform -> fail before mutation.
- Finish by verifying through `conda run`, then print the exact activation command.
  A child script must not claim it activated the caller's shell.

`environment.yml` declares Python 3.11, PyTorch `2.12.*`, NumPy, h5py, PyYAML, and
TensorBoard as the human-reviewable direct intent. `requirements-lock.txt` is the
committed osx-arm64 `python -m pip freeze` result, including transitives. Normal setup
reads and validates both files and never writes either. Only
`scripts/refresh-environment-lock.sh` may regenerate the pinned file, followed by
`pip check`, exact installed-versus-lock comparison, diff review, and relevant tests.

**No suitable analog:** the only existing `environment.yml`, requirements, packaging,
or lock-like files are under vendored `reference-code/`. They are not a project runtime
contract and must not be copied. The installer release URL, published digest, and exact
freeze are Wave 1 execution facts; a completed plan must not leave placeholders.

### 2. Canonical environment verification and evidence writes

**Atomic-write analog:** `scripts/git_policy/agent_presence.py`

```python
def _atomic_write(path, obj):
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(obj, handle)
    os.replace(tmp, path)
```

Reuse the sibling-temporary-file followed by `os.replace` convention, strengthened for
Phase 37 by first creating the UTC run directory with exclusive semantics. Serialize
canonical UTF-8 JSON with sorted keys, fixed indentation, and a trailing newline; derive
Markdown from the same in-memory object rather than reparsing an independently composed
report.

The minimum allowlisted fingerprint shape from research is:

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

Parse `sw_vers` into structured fields and hash the exact lock bytes. Do not serialize
the complete process environment or conda configuration: those can leak credentials and
add unreproducible machine noise. Verification fails closed for a missing/unhashable
lock, non-3.11 Python, non-2.12 Torch, missing/wrong required package, failed `pip check`,
installed-lock drift, or unavailable MPS. `--check-only` performs validation without
creating a new evidence run; normal setup creates a new timestamped fingerprint pair.

**No complete analog:** existing JSON writers do not provide the fingerprint schema,
secret allowlist, JSON/Markdown single-object derivation, or append-only run protocol.
Those details come from CTX-05..07 and the research contract.

### 3. Typed precision/device seam

There is no suitable implementation analog. The closest v1.3 line is an anti-pattern:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Do not copy implicit device selection or add `torch.set_default_dtype(...)`. The new
module's required shape is deliberately narrow:

```python
@dataclass(frozen=True)
class RuntimeSpec:
    ...  # explicit precision, dtype, requested/resolved device facts

def resolve_runtime(precision: str, device: str) -> RuntimeSpec:
    ...
```

Both arguments are required before owner adjudication. Accept the two explicit probe
profiles (`float32` + `mps`, `float64` + `cpu`) through the same resolver and fail before
tensor creation for omitted or unsupported pairs such as `float64` + `mps`. Pass the
resolved dtype/device explicitly into tensor and AD construction. `pinn/runtime.py`
must not grow model, data, loss, trainer, config-default, or fallback abstractions in
Phase 37.

### 4. Shared componentwise-AD kernel

**Semantic fixture:**
`.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py`

```python
u = torch.tensor(0.3, requires_grad=True, dtype=torch.float64)
x = torch.sin(2 * torch.pi * u)
y = torch.cos(2 * torch.pi * u)
z = u**2
r_prime = torch.stack([x, y, z])

derivatives = []
for k in range(3):
    grad_k = torch.autograd.grad(r_prime[k], u, create_graph=True)[0]
    derivatives.append(grad_k)
drdu_ad = torch.stack(derivatives)

drdu_analytical = torch.stack([
    2 * torch.pi * torch.cos(2 * torch.pi * u),
    -2 * torch.pi * torch.sin(2 * torch.pi * u),
    2 * u,
])
```

Preserve the scalar leaf `u`, `u = 0.3`, domain `[0, 1]`, all three output components,
the analytical derivative, and locked aggregate criterion
`aggregate_relative_error < 1e-6`. Phase 37 extends this fixture through one shared
trajectory/kernel, not two precision-specific implementations:

- Full Jacobian: supported transform such as `torch.func.jacrev`.
- Scalar-`u` forward mode: `torch.func.jvp` with scalar unit tangent.
- Correctness outside timing: predicted/analytical vectors, signed deltas,
  componentwise absolute and relative errors, aggregate norm-relative error, finite
  checks, and criterion pass/fail for every profile and pattern.
- Fixed measurement protocol from research: 10 untimed warmups, 30 raw samples, 100
  identical derivative evaluations per sample, normalized per evaluation, using
  `time.perf_counter_ns`; synchronize MPS immediately before and after each timed block.

The legacy per-component `autograd.grad` loop establishes component semantics but is not
the requested dual-pattern implementation. Do not replace the scalar-input Jacobian/JVP
with a summed-output VJP, loosen the tolerance by precision, or extend into Phase 38's
second-order production residual work.

### 5. Isolated dual-arm orchestration and evidence

There is no complete production analog. Follow the stdlib subprocess convention used by
repository tests:

```python
merged_env = os.environ.copy()
return subprocess.run(
    [sys.executable, str(script), *(args or [])],
    cwd=ROOT,
    text=True,
    capture_output=True,
    env=merged_env,
    check=False,
)
```

The parent imports no Torch. It invokes the same worker module twice with explicit argv,
copied environments, captured stdout/stderr, and a timeout. Before starting the MPS
child it removes `PYTORCH_ENABLE_MPS_FALLBACK` from the copied environment; the worker
records whether the key is absent before importing Torch. Each child emits exactly one
JSON object on stdout and diagnostics on stderr.

The parent preserves timeouts, signals, nonzero exits, malformed JSON, and worker
exceptions as structured arm results. It never converts a failed MPS arm into CPU
success and still writes a complete raw run when one arm fails. Each arm/pattern record
must include the CTX-10 facts: requested/resolved/actual device, dtype, fallback state,
Torch build, workload/repetition counts, raw and summary timings, componentwise and
aggregate errors, criterion result, and exception details.

Create `raw.json` first from the complete symmetric record, then render `summary.md` from
that object. The summary may report pass/fail, facts, and exceptions; it may not contain
a winner, recommendation, score, production default, or language that chooses D1-p.
After the one authorized on-device run, stop at the owner checkpoint.

### 6. Standard-library test harness

**Primary analog:** `tests/git_policy/test_git_policy.py`

```python
ROOT = pathlib.Path(__file__).resolve().parents[2]

def run_python(script, args=None, stdin=None, env=None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(script), *(args or [])],
        cwd=ROOT,
        input=stdin,
        text=True,
        capture_output=True,
        env=merged_env,
        check=False,
    )

class CommitMessagePolicyTests(unittest.TestCase):
    ...
```

Use Python 3.11 stdlib `unittest`, `tempfile`, `pathlib`, explicit copied environments,
argv subprocess calls, captured output, and return-code-plus-diagnostic assertions. Fake
conda/installers and temporary prefixes must cover setup state transitions without host
mutation or network access. Cheap CPU scientific coverage is appropriate; real MPS and
fresh-Mac work remain explicit hardware gates.

Wave 0 creates all six package/test files before implementation. Required negative
coverage includes wrong platform/architecture, occupied or incompatible prefix, drift
without silent update, missing/wrong lock, fingerprint secret exclusion, omitted or
unsupported runtime pair, unchanged global dtype, non-finite/component AD errors,
fallback-key leakage, timeout/nonzero/malformed child output, evidence collision, and
verdict language.

## Validation Task/Wave Contract

Keep this mapping synchronized with `37-VALIDATION.md`. The current Nyquist contract is
the research-derived five-plan decomposition; changing plan/task numbers requires an
equivalent update to the validation map.

| Task | Plan / Wave | Requirements | Owned contract | Automated verification |
|---|---|---|---|---|
| `37-01-01` | 01 / 0 | ENV-01, ENV-02 | bootstrap and fingerprint tests/scaffolding | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract tests.phase37.test_environment_fingerprint` |
| `37-01-02` | 01 / 0 | ENV-03, ENV-04 | runtime, AD, and orchestrator tests/scaffolding | `conda run -n pinn-train python -m unittest tests.phase37.test_runtime tests.phase37.test_componentwise_ad tests.phase37.test_precision_orchestrator` |
| `37-02-01` | 02 / 1 | ENV-01 | fail-closed root setup and verification command | `bash -n setup.sh scripts/refresh-environment-lock.sh && conda run -n pinn-train python scripts/verify_environment.py --check-only` |
| `37-02-02` | 02 / 1 | ENV-02 | lock write boundary + fingerprint provenance | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract.TestLockBoundary tests.phase37.test_environment_fingerprint` |
| `37-03-01` | 03 / 2 | ENV-04 | typed runtime combinations/no global default | `conda run -n pinn-train python -m unittest tests.phase37.test_runtime` |
| `37-03-02` | 03 / 2 | ENV-03 | shared trajectory, method parity, errors/timing contract | `conda run -n pinn-train python -m unittest tests.phase37.test_componentwise_ad` |
| `37-04-01` | 04 / 3 | ENV-03 | child isolation, fallback sanitation, structured failures | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator` |
| `37-04-02` | 04 / 3 | ENV-03 | atomic/non-overwriting raw + verdict-free renderer | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator tests.phase37.test_componentwise_ad` |
| `37-05-01` | 05 / 4 | ENV-01..04 | full software suite, one on-device evidence run, owner stop | `conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py'` plus the implemented explicit dual-arm command |

Ordinary software-only feedback must remain under 120 seconds. The full quick suite is:

```bash
conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py'
```

Fresh installation, exact lock generation, and the real MPS evidence run are isolated
wave gates, not planning-time checks or ordinary unit tests.

## No Complete Analog Found

The planner must use the locked Phase 37 contracts, not infer behavior from nearby code,
for these areas:

1. Project-owned Miniforge bootstrap, dependency intent/lock lifecycle, and exact drift
   validation. Vendored reference projects are not precedents.
2. Central immutable precision/device resolver. The v1.3 `pinn/` modules contain hidden
   device selection and cannot decide the rebuilt seam.
3. Same-worker dual-arm `jacrev`/`jvp` protocol, MPS synchronization, symmetric failure
   evidence, and canonical JSON/Markdown schemas.
4. The M5 Pro empirical outcome and D1-p. No source can substitute for the Wave 4 run
   and owner decision.

Absence of an analog is not permission to broaden scope. Do not edit
`ctl_instruction.md`, `pinn_architecture.md`, the Phase 21 fixture, or other v1.3 modules;
do not implement model/data/loss/training/checkpoint behavior from Phase 38+; and do not
encode an implicit production precision default.

## Sources Inspected

- `.planning/phases/37-developer-environment-precision-adjudication/37-CONTEXT.md`
- `.planning/phases/37-developer-environment-precision-adjudication/37-RESEARCH.md`
- `.planning/phases/37-developer-environment-precision-adjudication/37-VALIDATION.md`
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py`
- `scripts/setup-git-hooks.sh`
- `scripts/git_policy/agent_presence.py`
- `tests/git_policy/test_git_policy.py`
- `tests/watchdog/test_contract.py`
- `.planning/codebase/STACK.md`, `.planning/codebase/ARCHITECTURE.md`, and
  `.planning/codebase/TESTING.md` (through Phase 37 context/research synthesis)
- `.claude/rules/pinn-reference.md` and `.claude/rules/repo-map.md`

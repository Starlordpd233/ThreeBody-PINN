# Phase 56: Contract Amendment & Train-Free Gate - Pattern Map

**Mapped:** 2026-09-06
**Files analyzed:** 10 (7 new, 3 modified)
**Analogs found:** 10 / 10 (9 direct role+data-flow matches; 1 conditional-scope item — `tests/phase38/test_prohibitions.py` — matches itself, pending the planner's explicit scoping call per RESEARCH.md Open Question 1)

All analog paths below were confirmed git-tracked via `git ls-files` this session (tracked-source gate #3645) — none are gitignored install/runtime mirrors.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/verification/gate04_train_free.py` (NEW) | service (verification gate) | request-response (CLI/import) + batch (six-case sweep) | `pinn/verification/target_frame_probe.py` (verdict logic) + `pinn/verification/architecture_characterization_probe.py` (CLI/evidence scaffold) + `pinn/verification/gate_metrics.py` (dataclass+verdict convention) | exact (role+data-flow; same `pinn/verification/` family) |
| `pinn/verification/architecture_characterization_probe.py` — add `ratified_causal_weights` (MODIFIED) | utility (pure function, new peer of existing helpers) | transform | itself: `stratified_collocation_times` / `bin_mean_residuals` (lines 411-508) in the same file | exact — D-05 explicitly requires this function to live here as a peer |
| `pinn/verification/artifacts/r_ref_stage0.json` (NEW, new dir) | config / persisted data artifact | file-I/O (write-once, read-many) | `runs/.calibration/stage0-timing.json` | role-match (calibration-JSON precedent) |
| `tests/phase56/__init__.py` (NEW) | test (package marker) | n/a | `tests/phase55/__init__.py` | exact |
| `tests/phase56/test_gate04_train_free.py` (NEW) | test | batch (pytest) exercising request-response code | `tests/phase55/test_architecture_characterization.py` | exact (same test family, same module's sibling) |
| `tests/phase56/fixtures/pre_amendment_baseline.json` (NEW) | test fixture data | file-I/O | `tests/phase55/fixtures/six_case_baseline.json` | exact |
| `tests/phase56/test_spec_amendment_contract.py` (NEW) | test (content-match over markdown) | file-I/O | `tests/test_phase12_validation.py` (pytest content-match) — secondary: Phase 53's PLAN-embedded `<automated>` grep convention (not a pytest file) | role-match (see note below — two competing conventions exist) |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (MODIFIED — §2.2/§3.2/§4.1 amendment) | config (framework-spec contract document) | transform (prose amendment) | itself: the existing "Phase 35 contract" blockquote (line 445) and "Phase 53 contract" blockquote (line 688) | exact — self-referential precedent, same document, same amendment convention |
| `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (MODIFIED — new rows for amended §3.2 prose) | config (render-oracle allow-list) | file-I/O | itself: existing 7-entry array | exact |
| `tests/phase38/test_prohibitions.py` (CONDITIONALLY MODIFIED) | test (mechanical spec-freeze guard) | file-I/O + subprocess (git log) | itself: `SPEC_BASELINE_SHA256` + `PHASE_BASE_REF` regeneration recipe | exact, but in-scope status is an explicit open question (RESEARCH.md Open Question 1) — planner must scope this as its own deliberate task, not silent edit |

## Pattern Assignments

### `pinn/verification/gate04_train_free.py` (service/gate, request-response+batch)

**Analogs:** `pinn/verification/target_frame_probe.py` (verdict decision logic), `pinn/verification/architecture_characterization_probe.py` (module scaffold: imports, `__all__`, argparse `main`, evidence writer), `pinn/verification/gate_metrics.py` (frozen-dataclass-result + single-verdict-function convention).

**Imports pattern** — from `architecture_characterization_probe.py` lines 38-66 (adapt module docstring + import order: stdlib fallback-env capture before torch import, then stdlib, then numpy/torch, then `pinn.*`):
```python
from __future__ import annotations

# This must precede Torch and pinn.runtime imports: it is the only reliable
# record of the fallback environment that existed before Torch initialization.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
import math
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.loss_catalog import causal_physics_loss, resolve_causal_clip_facts
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.training.atomic_io import atomic_write_text
from pinn.verification.architecture_characterization_probe import (
    DEFAULT_CASES, RATIFIED_N_BINS, RATIFIED_PER_BIN,
    stratified_collocation_times, bin_mean_residuals, ratified_causal_weights,
)
from pinn.verify import git_head
```
GATE-04 imports `DEFAULT_CASES` / the stratified-sampling helpers from the Phase-55 probe rather than re-declaring them (D-07: "do not re-declare a parallel list").

**`__all__` + no-CI-wiring convention** — `architecture_characterization_probe.py:104-117`:
```python
__all__ = [
    "SweepCase",
    "ArchitectureCharacterizationResult",
    "DEFAULT_CASES",
    "DEFAULT_N_COL",
    "EVIDENCE_SCHEMA_VERSION",
    "EVIDENCE_TOP_LEVEL_KEYS",
    "measure_case",
    "run_sweep",
    "load_cases_config",
    "main",
    "stratified_collocation_times",
    "bin_mean_residuals",
]
```
GATE-04's `__all__` should list its verdict dataclass, the `PASS`/`BLOCK` constants (or verdict field), `main`, and `run_gate` (or equivalent library entry point) — every `pinn/verification/*_probe.py` is import-only, never registered in a verify ladder or CI gate (confirmed absent from any ladder per 55-CONTEXT; D-04 states the same for GATE-04 — Phase 57 imports it directly).

**Frozen result dataclass with exhaustive threshold docstring** — `pinn/verification/gate_metrics.py:203-209, 271-277` (mirror this shape exactly; D-04 calls out `TrajectoryGateMetrics`-style by name):
```python
@dataclass(frozen=True)
class TrajectoryGateMetrics:
    """One trajectory's gate evidence: the full Hamiltonian series + eps_H."""

    hamiltonian_series: torch.Tensor
    eps_h: float

...

@dataclass(frozen=True)
class AggregateGateMetrics:
    """The rendered test-set gate: aggregate eps_H, its SCS, and the verdict."""

    eps_h: float
    scs: float
    verdict: str
```
And the **single source-of-truth verdict function** convention — `gate_metrics.py:253-268`:
```python
def gate_verdict(eps_h: float) -> str:
    """The single source of truth for PASS/FAIL.

    FAIL for a non-finite ``eps_h``; FAIL for ``eps_h > 1e-5`` (equivalently
    ``SCS > -5``, since ``SCS = log10(eps_h)`` is monotone); PASS otherwise,
    INCLUDING the exact boundary ``eps_h == 1e-5`` (strict-inequality reject —
    SPEC edge R3 / prohibition 1). Deliberately the ONLY verdict function (no
    parallel SCS-based check) so the gate is never rendered as two
    independently-driftable booleans.
    """
    v = float(eps_h)
    if not math.isfinite(v):
        return "FAIL"
    if v > GATE_EPS_H_REJECT_THRESHOLD:
        return "FAIL"
    return "PASS"
```
GATE-04's verdict function is the direct analog: one function, `PASS`/`BLOCK` (not `PASS`/`FAIL` — match `56-CONTEXT.md`'s own vocabulary), fail-closed on any non-finite input, checked with strict inequalities against `resolve_causal_clip_facts(...)['causal_clip_min_weight']` (D-06(i)) — never two independently-driftable checks.

**Multi-condition, rule-ordered verdict with per-condition reasons** — `pinn/verification/target_frame_probe.py:774-786` (`decide_verdict` docstring — the closest existing analog for a verdict object carrying *why*, not just pass/fail):
```python
def decide_verdict(measures, accounting):
    """Classify into exactly one of four fail-closed verdicts (D-06).

    Rules, in order: (1) empty population raises FrameProbeUnavailable; (2) any
    non-finite measure, any empty split subgroup, or train/validation disagreement
    -> VERDICT_AMBIGUOUS; (3) VERDICT_TARGETS_ARE_SCALED requires every trajectory
    scaled-consistent AND raw-separated AND identity_scaled AND empty confound
    register (the ONLY route to D-08); ...
    """
```
GATE-04's fail-closed verdict object (D-04: "verdict object (`PASS`/`BLOCK` + per-condition reasons)") should follow this rule-ordered, docstring-exhaustive shape: evaluate conditions (i) [floor-pinned], (ii) [degenerate — OPEN, GAP-56-01], (iii) [front capability], plus the non-finite pre-checks (Block 3's re-issued AC: "reject non-finite residuals/prefixes *before* clipping"), and return one object naming which condition(s) tripped — never a bare boolean.

**Argparse `main(argv=None)` + evidence-write + non-verdict exit code** — `architecture_characterization_probe.py:815-883` (full pattern to mirror, including the `try/except` -> failure-record -> evidence-write -> `return 0 if completed else 1` shape; note D-06(iii) means GATE-04's *process* exit code is not itself the verdict — mirror `architecture_characterization_probe`'s own separation of "did the tool run" from "what did it find"):
```python
def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=_MODULE_PROG,
        description=(
            "Measure SQR-SkipResNet-SIREN residual and causal-weight behaviour "
            "at initialization. Reports quantities; does not judge the recipe."
        ),
    )
    parser.add_argument("--precision", default="float64", choices=("float32", "float64"))
    parser.add_argument("--device", default="cpu", choices=("mps", "cpu"))
    parser.add_argument("--n-col", type=int, default=DEFAULT_N_COL)
    parser.add_argument("--cases-config", type=Path, default=None)
    parser.add_argument("--evidence-root", type=Path, default=_DEFAULT_EVIDENCE_ROOT)
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    recorded_argv = list(argv) if argv is not None else sys.argv[1:]
    if args.cases_config is not None:
        cases = load_cases_config(args.cases_config)
    else:
        cases = DEFAULT_CASES

    try:
        runtime = resolve_runtime(args.precision, args.device)
        results = run_sweep(cases, n_col=args.n_col, precision=args.precision, device=args.device)
        raw = {
            "schema_version": EVIDENCE_SCHEMA_VERSION,
            "provenance": _provenance(recorded_argv, args, runtime),
            "configuration": _configuration(args),
            "cases": [_result_record(item) for item in results],
            "failure": None,
        }
        completed = True
    except Exception as exc:  # noqa: BLE001 - fail evidence must preserve runtime errors
        raw = _failed_record(recorded_argv, args, exc)
        completed = False

    try:
        run_dir = _write_evidence(raw, args.evidence_root)
    except Exception:
        return 1

    summary = _summary_markdown(raw)
    print(summary, end="" if summary.endswith("\n") else "\n")
    print(f"evidence={run_dir}")
    return 0 if completed else 1


if __name__ == "__main__":
    sys.exit(main())
```
GATE-04's own `main` differs in one respect D-04/D-06 require: the exit code (or a printed line) must also surface `PASS`/`BLOCK` distinctly from "did the tool crash," since Phase 57 needs to branch on the *verdict*, not just success/failure of the process. Mirror `_configuration`/`_provenance` (`architecture_characterization_probe.py:660-704`, see below) for the evidence dict shape, then add a `"verdict"` top-level key.

**Fail-closed frozen dataclass validation (`__post_init__`)** — `architecture_characterization_probe.py:120-181` (`SweepCase`, reused verbatim by GATE-04 — no new case dataclass needed, D-07 reuses `DEFAULT_CASES`), and the same style in `pinn/loss_catalog.py:122-159` (`LossWeights.__post_init__`) if a new dataclass is needed for the verdict object:
```python
@dataclass(frozen=True)
class SweepCase:
    """One ``(seed, masses, IC13-mode)`` measurement case.

    Fail-closed: every field is validated in ``__post_init__`` before any
    tensor or path is constructed. ``ic13_mode`` is a closed enum.
    """

    label: str
    seed: int
    masses: tuple[float, float, float]
    ic13_mode: str

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or self.label == "":
            raise ValueError(f"SweepCase.label must be a non-empty str; got {self.label!r}")
        ...
```

**Non-overwriting evidence directory + provenance dict** — `architecture_characterization_probe.py:605-673` (reuse pattern for `.planning/phases/56-*/evidence/gate04/<timestamp>/`):
```python
def _reject_dataset_evidence_root(evidence_root: Path) -> None:
    """Prevent an untrusted evidence-root from writing into simulation_data."""
    ...

def _new_run_dir(evidence_root: Path) -> Path:
    """Allocate a non-overwriting UTC run directory, including same-second runs."""
    _reject_dataset_evidence_root(evidence_root)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for suffix in range(1000):
        name = run_id if suffix == 0 else f"{run_id}-{suffix:03d}"
        candidate = evidence_root / name
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(f"could not allocate exclusive evidence directory under {evidence_root}")


def _git_worktree_dirty() -> tuple[bool | None, bool]:
    """Return ``(dirty_or_None, available)`` from bounded ``git status --porcelain``.

    Mirrors ``pinn.verify.git_head``: a missing binary, a non-repository
    directory, a non-zero exit, and a timeout all degrade to
    ``(None, False)`` rather than raising.
    """
    ...
```
This is also the pattern to reuse for the `R_ref` artifact writer (see below) — `_new_run_dir`'s `mkdir(exist_ok=False)` + numeric-suffix retry is the same discipline `55-SECURITY.md` T-55-08 requires for concurrent/overlapping evidence writes.

**Error handling / fail-closed pre-check ordering:** `pinn/loss_catalog.py:308-324` (`causal_physics_loss`) shows the "validate ordering BEFORE computing" discipline GATE-04 must reuse for non-finite rejection:
```python
rbar = torch.as_tensor(residuals_per_time, dtype=dtype, device=device).reshape(-1)
if times is not None:
    t = torch.as_tensor(times, dtype=dtype, device=device).reshape(-1)
    if t.numel() != rbar.numel():
        raise ValueError(...)
    if t.numel() > 1 and bool((t[1:] < t[:-1]).any()):
        raise ValueError(
            "causal_physics_loss requires ascending collocation times; "
            "got unordered times (the causal prefix weight is only "
            "meaningful on a time-sorted sequence)"
        )
n_t = rbar.numel()
if n_t == 0:
    raise ValueError("causal_physics_loss: empty residuals_per_time")
```
GATE-04 condition (i)/non-finite checks must reject non-finite residuals/prefixes *before* the clamp (Block 3's re-issued AC) — check-then-compute, exactly this shape, never compute-then-mask.

---

### `pinn/verification/architecture_characterization_probe.py` — add `ratified_causal_weights` (utility, transform)

**Analog:** itself — `stratified_collocation_times` (lines 411-476) and `bin_mean_residuals` (lines 479-508), the two immediately-preceding functions this new one becomes a peer of (D-05). Also `pinn/loss_catalog.py::causal_physics_loss` (lines 283-347) and `resolve_causal_clip_facts` (lines 77-115) — the trainer functions to call, never reimplement.

**Docstring + fail-closed validation pattern to mirror** (`bin_mean_residuals`, lines 479-508):
```python
def bin_mean_residuals(rbar_per_point, bin_assignment, *, n_bins: int = RATIFIED_N_BINS):
    """Arithmetic mean of residuals in each ratified time bin.

    Entry ``b`` is the unweighted mean of the residuals whose assignment
    equals ``b`` — the ``54-RULING.md`` bin-residual definition.
    ...
    """
    rbar = np.asarray(rbar_per_point, dtype=np.float64).reshape(-1)
    bins = np.asarray(bin_assignment).reshape(-1)
    if rbar.size != bins.size:
        raise ValueError(f"residual and bin-assignment lengths differ: {rbar.size} vs {bins.size}")
    if np.any(bins < 0) or np.any(bins >= n_bins):
        raise ValueError(f"bin index outside [0, {n_bins})")
    means = np.empty(n_bins, dtype=np.float64)
    for bin_id in range(n_bins):
        members = rbar[bins == bin_id]
        if members.size == 0:
            raise ValueError(f"empty bin {bin_id}")
        means[bin_id] = float(np.mean(members))
    return means
```

**The exact reuse-not-reimplement call site** (`pinn/loss_catalog.py:283-347`, unmodified — this IS the formula `ratified_causal_weights` must invoke, never fork):
```python
def causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None,
                        dtype, device, return_details: bool = False):
    ...
    rbar = torch.as_tensor(residuals_per_time, dtype=dtype, device=device).reshape(-1)
    ...
    eta = torch.as_tensor(eta_c, dtype=dtype, device=device)
    detached = rbar.detach()
    cumsum = torch.cumsum(detached, dim=0)
    zeros = torch.zeros(1, dtype=dtype, device=device)
    cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
    clip_facts = resolve_causal_clip_facts(dtype, device)
    exponent = -eta * cumsum_excl
    floor = torch.as_tensor(clip_facts["causal_clip_exponent_floor"], dtype=dtype, device=device)
    weights = torch.exp(torch.clamp_min(exponent, floor))
    ...
    loss = (weights * rbar).mean()
    if return_details:
        return loss, {"w_n": weights.detach(), "rbar": rbar.detach()}
    return loss
```
`resolve_causal_clip_facts` (`loss_catalog.py:77-115`) is the dtype/device-derived floor GATE-04 condition (i) must compare against — never a hardcoded literal:
```python
def resolve_causal_clip_facts(dtype, device) -> dict[str, object]:
    """Derive the causal exponent floor for one active dtype/backend. ..."""
    ...
    return {
        "causal_clip_precision": precision,
        "causal_clip_exponent_floor": floor_value,
        "causal_clip_min_weight": min_weight,
        "causal_clip_formula": CAUSAL_CLIP_FORMULA,
        "causal_clip_provenance": CAUSAL_CLIP_PROVENANCE,
    }
```
`ratified_causal_weights(raw_bin_means, r_ref, *, eta_c, dtype, device, t_max)` (D-05's function) composes exactly these two: divide `raw_bin_means` by `r_ref` to get `R̃_b`, build an ascending bin-center-proxy `times`, call `causal_physics_loss(R̃, eta_c=eta_c, times=..., dtype=dtype, device=device, return_details=True)`, and return `details["w_n"]`. RESEARCH.md Part (a).4/Code Examples already contains a session-verified working version of this exact composition — treat that as the reference implementation, not a fresh derivation.

**Add to `__all__`** (`architecture_characterization_probe.py:104-117`) — append `"ratified_causal_weights"` to the existing list; do not create a second `__all__` block.

---

### `pinn/verification/artifacts/r_ref_stage0.json` (config/artifact, file-I/O)

**Analog:** `runs/.calibration/stage0-timing.json` (full file, precedent for schema shape):
```json
{
  "schema_version": "phase43-stage0-timing/v1",
  "s_per_step": 0.18288215688329543,
  "full_stage0_steps": 300,
  "forecast_seconds": 54.86464706498863,
  "timestamp": "2026-08-15T02:51:01.296265+00:00",
  "fingerprint": {
    "device": "mps",
    "dtype": "torch.float32",
    "torch_version": "2.12.1",
    "python_version": "3.11.15",
    "git_head": "c4a1550b7bd889121128e31d7078a478b0a6ca8a",
    "git_head_available": true
  },
  "valid": true
}
```
Map D-09's required contents onto this shape: `schema_version` (e.g. `"phase56-r-ref-stage0/v1"`), the `R_ref` value, the 6 cases, all 96 raw bin means, the statistic name (`"median"`, `numpy.median` even-N convention — see Pitfall 5 in RESEARCH.md), a `fingerprint`-equivalent provenance block (seeds, bin edges, 256-per-bin, precision/device, torch/numpy versions, git sha + dirty flag), and the verbatim invalidation-trigger list as an array of strings.

**Writer pattern to reuse (never hand-roll `open(...).write(...)`)** — `pinn/training/atomic_io.py:41-64`:
```python
def atomic_write_text(path: PathLike, content: str) -> Path:
    """Atomically write UTF-8 text to ``path``.

    Verified idiom (stage_scan ``_atomic_write``): write to
    ``path.tmp.{pid}``, flush + ``os.fsync`` the file, ``os.replace`` onto the
    canonical name, then ``os.fsync`` the parent directory. A ``finally``
    unlinks any leftover temp so a failed replace cannot leave a partial
    artifact under the canonical name.
    """
    destination = _as_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination
```
Already imported by `architecture_characterization_probe.py:64` — GATE-04 imports the same symbol, does not reimplement it. `pinn/training/atomic_io.py` also exports `atomic_write_torch` (line 67) if a non-JSON payload is ever needed, but D-09 specifies JSON, so `atomic_write_text(path, json.dumps(payload, sort_keys=True, indent=2))` is the composition to use.

**Provenance-dict shape to extend** — `architecture_characterization_probe.py:671-673+` (`_provenance`, reads `git_head()` + `_git_worktree_dirty()`); use the same two calls for the `R_ref` artifact's git-identity fields rather than re-deriving them.

---

### `tests/phase56/__init__.py` (test package marker)

**Analog:** `tests/phase55/__init__.py` (full file, 1 line):
```python
"""Phase 55 architecture-characterization tests."""
```
Copy verbatim with the phase number/topic changed: `"""Phase 56 contract-amendment and train-free-gate tests."""`.

---

### `tests/phase56/test_gate04_train_free.py` (test)

**Analog:** `tests/phase55/test_architecture_characterization.py` (724 lines) — three sub-patterns to copy:

**1. Deferred-import skip pattern + fixture loader** (lines 1-27, 42-47, 59-61):
```python
from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pytest
import torch

from pinn.loss_catalog import resolve_causal_clip_facts

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.architecture_characterization_probe"
FIXTURE_PATH = pathlib.Path(__file__).resolve().parent / "fixtures" / "six_case_baseline.json"

def _load_probe():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _load_fixture():
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)
```
GATE-04's test file sets `MODULE = "pinn.verification.gate04_train_free"` and `FIXTURE_PATH = .../fixtures/pre_amendment_baseline.json`, with the identical `_load_probe`/`_load_fixture`/skip-before-landed shape.

**2. SHA-256 integrity-guard autouse fixture** (lines 113-120) — protects the committed fixture from being silently healed by the suite itself; D-08's SC5 fixture needs the identical guard:
```python
@pytest.fixture(scope="session", autouse=True)
def _assert_baseline_sha256_unchanged():
    digest = hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest()
    yield
    assert hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest() == digest, (
        "tests/phase55/fixtures/six_case_baseline.json was rewritten during the "
        "suite; the Tier-2 net must never heal its own baseline"
    )
```

**3. CLI-subprocess contract TestCase** (lines 375-414) — exercises the module as `python -m <module>` against a temp evidence root, exactly the harness GATE-04's own `main`/CLI needs:
```python
class ArchitectureCharacterizationCLITests(unittest.TestCase):
    """CLI-subprocess contract: module entry point, evidence, non-verdict exit."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="phase55-probe-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)

    def _evidence_root(self, name: str) -> pathlib.Path:
        return self.tmp / "evidence" / name

    def _run_cli(self, evidence_root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", MODULE, *args, "--evidence-root", str(evidence_root)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )

    @staticmethod
    def _only_raw(evidence_root: pathlib.Path) -> dict:
        raw_paths = sorted(evidence_root.glob("*/raw.json"))
        if len(raw_paths) != 1:
            raise AssertionError(f"expected one evidence run under {evidence_root}, found {raw_paths}")
        return json.loads(raw_paths[0].read_text(encoding="utf-8"))

    def test_zero_argument_cli_reproduces_six_rows(self):
        probe = _load_probe()
        root = self._evidence_root("zero-arg")
        completed = self._run_cli(root)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        raw = self._only_raw(root)
        self.assertEqual([case["label"] for case in raw["cases"]], [case.label for case in probe.DEFAULT_CASES])
```
D-08's SC5 test (`assert BLOCK on the pre-amendment recipe`) is a natural extension of `test_zero_argument_cli_reproduces_six_rows`'s shape: run the CLI (or call the library function directly) against the pre-amendment fixture and assert the returned/persisted verdict is `BLOCK` with condition (i) and the degeneracy condition both named in the reasons.

`.venv/bin/python -m pytest tests/phase56/ -q` is the exact per-task/per-wave invocation (mirrors `tests/phase55/` verbatim, per RESEARCH.md A.10).

---

### `tests/phase56/fixtures/pre_amendment_baseline.json` (test fixture data)

**Analog:** `tests/phase55/fixtures/six_case_baseline.json` — `_meta` block + self-documenting regeneration command (lines 1-14):
```json
{
  "_meta": {
    "device": "cpu",
    "generated_at": "2026-09-06T03:47:46Z",
    "ic13_rng_scheme": "zero: zero-vector; random_tanh: numpy.random.default_rng(seed + IC13_RNG_OFFSET) standard-normal then elementwise tanh",
    "median_convention": "numpy.median: arithmetic mean of the two central order statistics (explicitly not torch.median's lower-of-two)",
    "n_col": 16,
    "numpy_version": "2.2.0",
    "precision": "float64",
    "purpose": "D-01 tier-2 baseline: the full six-row output is read only by the test suite and is regenerated only by an explicit, reviewed operator action after a deliberate implementation change.",
    "regeneration_command": ".venv/bin/python -c \"...\"",
    "relative_tolerance": 1e-09,
    "torch_version": "2.12.0"
  },
  "cases": [
    {
      "a_norm_median": 197528.97072575035,
      "causal_clip_min_weight": 2.2250738585072626e-308,
      "causal_weights": [1.0, 2.2250738585072626e-308, ...],
      "collocation_times": [1.2597074678820208, ...],
      ...
```
`pre_amendment_baseline.json` should follow this exact `_meta` + `cases` shape: `_meta.purpose` states it captures the pre-amendment (`n_col=16`, unnormalized `R̄`, no `R_ref`) recipe's known-degenerate output (15/16 weights at the dtype floor, `front_idx=0`) as SC5's frozen comparison target, and `_meta.regeneration_command` documents the exact `run_sweep(DEFAULT_CASES, n_col=16, ...)` invocation used to produce it — mirroring the committed Phase-55 evidence at `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md`, which RESEARCH.md Part b.1 confirms is the correct baseline to cite.

---

### `tests/phase56/test_spec_amendment_contract.py` (test, content-match)

**Two competing analogs exist in this repo — the planner should pick one deliberately, not blend them silently:**

**Analog A (pytest content-match over the markdown, closer to what RESEARCH.md's Wave-0-Gaps table recommends):** `tests/test_phase12_validation.py` (top-level, not per-phase-dir) — lines 185-211:
```python
def test_fidel_06_inactive_content_absent():
    """FIDEL-06: Inactive content absent from markdown."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("FIDEL-06: markdown exists", False)
        return
    content = open(ARCHITECTURE_MD).read()

    # Exclude the Source Issues metadata section from this check (D-19)
    body = content
    if "## Source Issues / Notes for Future Reconciliation" in content:
        body = content.split("## Source Issues / Notes for Future Reconciliation")[0]

    for term in INACTIVE_TERMS:
        count = body.count(term)
        check(f"FIDEL-06: '{term}' absent from faithful body",
              count == 0, f"found {count} occurrences")


def test_cross_01_source_issues():
    """CROSS-01: Source Issues metadata appended."""
    if not os.path.isfile(ARCHITECTURE_MD):
        check("CROSS-01: markdown exists", False)
        return
    content = open(ARCHITECTURE_MD).read()
    check("CROSS-01: Source Issues section present",
          "## Source Issues / Notes for Future Reconciliation" in content)
```
with `ARCHITECTURE_MD` defined at line 18: `os.path.join(PROJECT_ROOT, "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md")`. A `tests/phase56/test_spec_amendment_contract.py` following this shape would open the spec file once, then assert the re-issued AC text and the "NOT AMENDED" markers for Blocks 2/3 are present as substrings — exactly RESEARCH.md's Wave-0-Gaps row for SPEC-01/SPEC-06.

**Analog B (the convention Phase 53 actually used for its own SCOPE-38 spec amendments — PLAN-embedded bash, NOT a pytest file):** `.planning/phases/53-narrow-spec-codification/53-01-PLAN.md` — the `<automated>` acceptance-check blocks are shell one-liners run at commit time, e.g.:
```
grep -c -F '**[LOCKED]**' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md returns >= 3 ...
&& SCOPE-38 byte-identity: git diff -U0 HEAD -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow' is empty
&& render oracle: node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md exits <= 1 ...
```
Phase 53 shipped **no** `tests/phase53/` directory — its spec-amendment verification lived entirely in PLAN.md `<automated>` blocks, never a committed pytest file. If the planner follows Phase 53's own precedent instead of RESEARCH.md's Wave-0 recommendation, `test_spec_amendment_contract.py` would not exist at all and its assertions would move into each task's PLAN.md acceptance criteria instead — a legitimate alternative, not a gap. Note the SCOPE-38 negative-diff guard narrows for Phase 56 to Blocks 2/3 only (`first_omega_0`, `underflow`), since Block 1 (`eta_c`) is legitimately changing this phase (RESEARCH.md A.8).

---

### `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (config/spec, transform)

**Analog: the file's own existing SCOPE-38 amendment blockquotes** — this is the load-bearing pattern: every prior contract amendment in this document uses the same blockquote shape (`> **Phase N contract: <topic> (<REQ-IDs>; <ruling-refs>; grounded by <path>).** <prose>.`). Two session-verified instances:

**Instance 1 — the Phase 35 `η_c` contract block** (line 445, immediately below the `w_n`/`L_phys^causal` formulae at lines 435-440 — this is the exact block Block 1/D-01 amends):
```
> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04; grounded by the resolution doc §1.1, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` GAP-32-01, and `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-04-causal-training-mode.md`).** This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`. Dense-residual ALM is rejected from the default loss, optional scalar-conservation ALM remains deferred P2 only, and the numeric causal-exponent clip bound is deferred to FUT. Option C time-windowed causal mechanics are not commissioned.
```

**Instance 2 — the Phase 53 locked-vs-default contract block** (line 688, the most recent SCOPE-38 amendment before this phase — the template to copy for citation format and "this supersedes / this does not decide" scoping language):
```
> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03; GAP-45-03 owner ruling 2026-07-24, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).** The full PHYS-05 per-stage λ^max(k) table above binds for every stage k, boundary rows included ... This site is the locked-vs-default convention's first and only application in this phase; ... Generalization of the convention to other spec tables was explicitly NOT decided by this ruling (consequence 5), and remains open.
```

**Session-verified anchors (re-verify by content match immediately before each edit — every insertion shifts subsequent line numbers within this same phase's own edits):**

| Anchor | Line (independently re-verified this session) | Content |
|---|---|---|
| §2.2 `first_omega_0` fixed-at-30 sentence (Block 2, NOT AMENDED) | 181 | "The initial frequency parameter `first_omega_0` is fixed at `30` and is not scheduled during training." |
| §2.4 Table 1 header (GAP-56-02, blocked) | 267 | `| **Hyperparameter** | **Recommended Value** | **Rationale & Justification** |` |
| §2.4 Table 1 `first_omega_0` row (GAP-56-02, blocked) | 274 | `| first_omega_0 | 30 | ... |` |
| §3.2 `w_n`/`L_phys^causal` formulae (context for Block 1 insertion point) | 435-440 | `$$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$` |
| §3.2 Phase 35 `η_c` contract block (Block 1, AMENDED) | 445 | see Instance 1 above |
| §3.2 Listing 3 `n_col=4096` default (Block 4, D-11) | 454 | `def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',` |
| §3.2 "recommended: 2048-4096" docstring (Block 4, D-11) | 461 | `n_col: Number of collocation points (recommended: 2048-4096)` |
| §4.1 loss-catalog `where:` clip underflow-only sentence (Block 3, NOT AMENDED) + `η_c=1` default (D-10) | 668-671 | "$\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the causal exponent to avoid underflow ... The causal exponent clip is required only to avoid underflow." |
| §4.1 Phase 53 locked-vs-default contract block | 688 | see Instance 2 above |

**Do not paraphrase the amendment content** — `54-RULING.md`'s four SCOPE-38 blocks and the "Batch allocation and bin policy" / "Reference invalidation" paragraphs are the verbatim source text (already quoted in full in `56-CONTEXT.md` and `56-RESEARCH.md` Part A.2); this PATTERNS.md section supplies the *structural* convention (blockquote shape, citation format, anchor locations) — not the prose itself, which the executor transcribes from `54-RULING.md` per D-01.

---

### `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (config, file-I/O)

**Analog:** itself — the existing 7-entry array (full file):
```json
[
  {
    "file": "pinn_architecture.md",
    "line": 184,
    "token": "first_omega_0",
    "verdict": "code-identifier-kept",
    "rationale": "SIREN initialization parameter name (PyTorch code identifier in backtick code span, not math)"
  },
  ...
  {
    "file": "pinn_architecture.md",
    "line": 274,
    "token": "first_omega_0",
    "verdict": "code-identifier-kept",
    "rationale": "SIREN parameter name in hyperparameter table cell (code identifier in prose)"
  },
  {
    "file": "pinn_architecture.md",
    "line": 275,
    "token": "hidden_omega_0",
    "verdict": "code-identifier-kept",
    "rationale": "SIREN parameter name in hyperparameter table cell (code identifier in prose)"
  }
]
```
All 7 existing entries sit in §2.2-§2.4 (lines 184-275); none are inside §3.2 (starts at line 383), so Block 1/4's amendment does not require renumbering them (RESEARCH.md A.8) — but re-run the detector after editing and append new `{file, line, token, verdict, rationale}` rows in this same shape for any DEFINITE/REVIEW token the new §3.2 prose introduces. Command: `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`.

---

### `tests/phase38/test_prohibitions.py` (test, conditional scope — planner must decide explicitly)

**Analog:** itself — the stale SCOPE-18 guard (lines 1-46, 133-163):
```python
PHASE_BASE_REF = "9160a5200df5e515998e235eb13a31c664b67057"
SPEC_PATHS = (
    "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md",
    "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md",
)
SPEC_BASELINE_SHA256 = {
    SPEC_PATHS[0]: "0b73ba0345d19c1c2ba544913ecd6680dab442790725de7a8fe52903085b9d68",
    SPEC_PATHS[1]: "e629b2fc444317f71cba0fc9e7e9ba75bf18981fc235b9ba4d25acfe681b6dbd",
}

class ProhibitionTests(unittest.TestCase):
    def test_spec_byte_identity_endpoint_sha256(self):
        for rel, expected in SPEC_BASELINE_SHA256.items():
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing spec {rel}")
            got = _sha256_file(path)
            self.assertEqual(
                got, expected,
                f"working-tree {rel} sha256 {got} != pre-phase baseline {expected}; "
                f"SCOPE-18 prohibits Phase-38 edits to framework specs",
            )

    def test_spec_history_no_touch_since_phase_base(self):
        completed = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:", f"{PHASE_BASE_REF}..HEAD", "--", *SPEC_PATHS],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        ...
```
This test already fails (2 failures, pre-existing since Phase 53 per `55-VERIFICATION.md:197`) and Phase 56's own spec edit will not change that fact — it is expected, not a regression (RESEARCH.md Pitfall 2). **Do not silently edit this file as a side effect of the spec-amendment task.** If the planner scopes a dedicated task to retire/update it (RESEARCH.md Open Question 1), the analog for that task is the file's own documented regeneration recipe (module docstring lines 11-18: `git show <ref>:<path> | shasum -a 256`), which shows exactly how `SPEC_BASELINE_SHA256` was produced and how a new baseline would be produced.

## Shared Patterns

### Fail-closed single-verdict-function convention
**Source:** `pinn/verification/gate_metrics.py:253-268` (`gate_verdict`) and `pinn/verification/target_frame_probe.py:774-901` (`decide_verdict`)
**Apply to:** `gate04_train_free.py`'s verdict logic exclusively.
One function is the only source of PASS/BLOCK truth; every condition is a strict-inequality/finite check; non-finite input always routes to the fail-closed branch; a rule-ordered docstring documents every threshold by name (D-04's own requirement: "an exhaustive docstring naming every threshold").

### Reuse-not-reimplement discipline for trainer-owned formulas
**Source:** `pinn/loss_catalog.py::causal_physics_loss` / `resolve_causal_clip_facts` (lines 283-347, 77-115)
**Apply to:** `ratified_causal_weights` (new, in `architecture_characterization_probe.py`) and every numeric condition in `gate04_train_free.py`.
Never hardcode a dtype-derived constant (`causal_clip_min_weight`); never re-derive the exp/clip/prefix-sum arithmetic — call the trainer's own function with the ratified recipe's inputs.

### `pinn/verification/*_probe.py` / gate module scaffold
**Source:** `pinn/verification/architecture_characterization_probe.py` (whole file structure) and `pinn/verification/target_frame_probe.py` (whole file structure)
**Apply to:** `gate04_train_free.py`.
`argparse`-based `main(argv=None)` + `if __name__ == "__main__": sys.exit(main())`; `__all__` lists every importable symbol; no wiring into any CI/verify ladder; non-overwriting UTC evidence directories (`_new_run_dir`); a `_provenance()` dict with `argv`, `command`, `git_sha`/`git_available`, `git_worktree_dirty`/`_available`, `torch_version`, `numpy_version`, `timestamp`.

### Frozen dataclass + `__post_init__` fail-closed validation
**Source:** `pinn/verification/architecture_characterization_probe.py:120-181` (`SweepCase`) and `pinn/loss_catalog.py:122-159` (`LossWeights`)
**Apply to:** any new dataclass in `gate04_train_free.py` (verdict object, per-case result).
Validate every field in `__post_init__` before any tensor/path is constructed; raise `ValueError` with a message naming the field and the received value; closed-enum fields checked against a `frozenset`.

### Atomic, non-overwriting artifact writes
**Source:** `pinn/training/atomic_io.py:41-64` (`atomic_write_text`) + `architecture_characterization_probe.py:615-629` (`_new_run_dir`)
**Apply to:** the `R_ref` JSON artifact writer and GATE-04's own evidence writer.
tmp-write + fsync + `os.replace`, never a bare `open(...).write(...)`; directory allocation via `mkdir(parents=True, exist_ok=False)` with numeric-suffix retry, never a plain overwrite.

### SCOPE-38 spec-amendment blockquote convention
**Source:** `pinn_architecture.md:445` (Phase 35 block) and `pinn_architecture.md:688` (Phase 53 block) — both inside the same file being amended.
**Apply to:** every new/edited block in §2.2/§3.2/§4.1.
`> **Phase N contract: <topic> (<REQ-IDs>; <ruling/GAP refs>; grounded by <path>).** <prose stating what is retained, what changed, what is explicitly NOT decided>.` Always name the superseded ruling; always state what the block does NOT decide (Phase 53's own block models this: "Generalization of the convention to other spec tables was explicitly NOT decided by this ruling... and remains open").

### JSON fixture/artifact `_meta` + SHA-guard convention
**Source:** `tests/phase55/fixtures/six_case_baseline.json:1-14` (`_meta` block) + `tests/phase55/test_architecture_characterization.py:113-120` (autouse SHA-256 guard)
**Apply to:** `tests/phase56/fixtures/pre_amendment_baseline.json` and its consuming test.
A `_meta` block records `purpose`, `regeneration_command` (a literal re-runnable one-liner), tool/library versions, and precision/device — the fixture is self-documenting; a `scope="session", autouse=True` pytest fixture asserts the file's SHA-256 is unchanged across the whole suite run, so a bug cannot silently "heal" the committed baseline.

## No Analog Found

None. Every file in scope has at least a role-and-data-flow analog already in the repository (see table above). The one item without a *single* clean analog — `tests/phase56/test_spec_amendment_contract.py` — has two competing analogs (a pytest content-match precedent and a PLAN-embedded-bash precedent); this is a planner decision to make explicitly, not a missing pattern (see that file's Pattern Assignment section above and RESEARCH.md Open Question 1 territory).

## Metadata

**Analog search scope:** `pinn/verification/`, `pinn/loss_catalog.py`, `pinn/training/atomic_io.py`, `tests/phase55/`, `tests/phase38/`, `tests/test_phase12_validation.py`, `runs/.calibration/`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`, `tools/spec-render-check/`, plus `.planning/phases/53-narrow-spec-codification/53-01-PLAN.md` for the competing spec-verification convention.
**Files scanned (read directly this session, not merely cited from RESEARCH.md):** `pinn/verification/gate_metrics.py` (full, 287 lines), `pinn/loss_catalog.py` (full, 412 lines), `pinn/verification/architecture_characterization_probe.py` (targeted: 1-120, 120-185, 245-315, 405-514, 605-675, 810-884 — 883 lines total, non-overlapping ranges), `pinn/verification/target_frame_probe.py` (targeted: 1-100, 774-943 — 1723 lines total), `pinn/training/atomic_io.py` (grep structure + 41-66), `tests/phase55/test_architecture_characterization.py` (targeted: 1-130, 375-464 — 724 lines total), `tests/phase55/__init__.py` (full), `tests/phase55/fixtures/six_case_baseline.json` (head, 1-45 of 371), `tests/phase38/test_prohibitions.py` (targeted: 1-60, 130-164 — 332 lines total), `runs/.calibration/stage0-timing.json` (full, 16 lines), `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (targeted: 170-199, 258-282, 435-479, 655-704 — 1098 lines total), `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (full, 51 lines), `tests/test_phase12_validation.py` (targeted: 180-219).
**Tracked-source gate:** all 11 analog file paths confirmed via `git ls-files` this session — none are gitignored mirrors.
**Pattern extraction date:** 2026-09-06

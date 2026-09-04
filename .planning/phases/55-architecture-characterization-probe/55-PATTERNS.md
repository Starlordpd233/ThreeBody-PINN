# Phase 55: Architecture Characterization Probe - Pattern Map

**Mapped:** 2026-09-04
**Files analyzed:** 3 new files, 1 likely-required modification to an existing Phase-38 test file (discovered during mapping, not listed in CONTEXT.md/RESEARCH.md — see "Cross-Cutting Collision" below), 1 test-fixture data artifact
**Analogs found:** 3 / 3 primary new files have a strong (exact or role-match) structural analog; the fixture data artifact has no strong precedent (see "No Analog Found")

This phase is structurally unusual for pattern-mapping purposes: it creates
**one** production module that must *compose*, not *pattern-copy*, roughly
eight already-proven `pinn/` primitives (SC3's explicit mandate: "derive
from, not re-implement, the trainer's own math"). Accordingly this map
separates two kinds of guidance:

1. **Structural analogs** — existing files whose shape (imports, CLI,
   evidence I/O, dataclass conventions, test style) the new files should
   imitate.
2. **Reused primitives** — existing functions the new module must import
   and call *directly, verbatim* — copying their logic into a new
   implementation would itself violate SC3.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/verification/architecture_characterization_probe.py` | verification probe / CLI utility | batch (seed/IC sweep) + file-I/O (evidence write) | `pinn/verification/residual_probe.py` | **exact** — same role (standalone `pinn/verification/*_probe.py` module), same data flow (compute over inputs → structured dict → evidence JSON + summary.md + stdout + exit code) |
| `tests/phase55/__init__.py` | test (package init) | n/a | `tests/phase49/__init__.py` | **exact** |
| `tests/phase55/test_architecture_characterization.py` | test | batch validation (CLI-subprocess contract tests + in-process pytest-function invariant tests) | `tests/phase38/test_residual_probe.py` (CLI-subprocess style) **+** `tests/phase49/test_gate03_invariants.py` (pytest-function style) | **role-match, hybrid** — RESEARCH.md's own Validation Architecture section recommends combining both existing styles in one file |
| Tier-2 exact-value fixture (six-row baseline, D-01 tier 2) | test fixture / static data | batch/regression comparison | none found — see "No Analog Found" | **no analog** |
| *(possible)* `tests/phase38/test_prohibitions.py` | test (existing, Phase-38 mechanical prohibition suite) | n/a | itself | **collision, not a copy target** — see "Cross-Cutting Collision" below |

Note: `pinn/training/controllers.py:566-702` is **not** the structural
analog for the new file (it is a stateful trainer method, not a standalone
probe) — it is the **composition source** the probe's core measurement loop
must mirror line-for-line for the physics/AD/causal-weight math. See Pattern
1 below.

---

## Pattern Assignments

### `pinn/verification/architecture_characterization_probe.py` (verification probe, batch + file-I/O)

**Structural analog:** `pinn/verification/residual_probe.py` (328 lines, read in full).
**Composition source (SC3 mandate):** `pinn/training/controllers.py:566-702`.
**Dataclass-result convention:** `pinn/verification/gate_metrics.py:203-287`.

#### 1. Imports pattern

`pinn/verification/residual_probe.py:1-28`:
```python
from __future__ import annotations

# This must precede Torch and pinn.runtime imports: it is the only reliable
# record of the fallback environment that existed before Torch initialization.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
from pathlib import Path
import sys

import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, EPS_SOFT, T_CHARACTERISTIC_TIME
from pinn.physics_residual import softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.verification.fixture_loader import load_trajectory


DEFAULT_RESIDUAL_THRESHOLD = 1e-5
...
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "38-pinn-model-rebuild-from-specs-fut-01" / "evidence" / "residual"
)

__all__ = ["main", "run_residual_on_ground_truth"]
```
For the new module: same shape, but `_DEFAULT_EVIDENCE_ROOT` should point at
`.planning/phases/55-architecture-characterization-probe/evidence/probe/`,
and imports add `pinn.architecture_spec.ArchitectureSpec`,
`pinn.network.build_network`, `pinn.physics_residual.componentwise_du`,
`pinn.loss_catalog.causal_physics_loss`, `pinn.training.collocation_sampler.CollocationSampler`,
`pinn.verify.git_head`, `pinn.training.atomic_io.atomic_write_text`,
`numpy`. `__all__` should export both the single-case and multi-case
surfaces (RESEARCH.md Open Question 2's recommendation): `["main",
"run_sweep", "measure_case", "SweepCase",
"ArchitectureCharacterizationResult", "DEFAULT_CASES",
"stratified_collocation_times", "bin_mean_residuals"]`.

#### 2. Evidence-root guard + run-dir + write pattern

`pinn/verification/residual_probe.py:43-94` (verbatim):
```python
def _reject_dataset_evidence_root(evidence_root: Path) -> None:
    """Prevent an untrusted evidence-root from writing into simulation_data."""
    dataset_root = (_REPO_ROOT / "simulation_data").resolve()
    try:
        evidence_root.resolve().relative_to(dataset_root)
    except ValueError:
        return
    raise ValueError("evidence-root must not be inside simulation_data")


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
```
**Deviation recommendation:** `residual_probe.py`'s own `_atomic_write`
(lines 53-59) is a *private, per-file* duplicate that omits the parent-dir
fsync. RESEARCH.md's Don't-Hand-Roll table flags this explicitly — use
`pinn.training.atomic_io.atomic_write_text` (see Reused Primitives below)
in the new module instead of copying `_atomic_write` again; `_new_run_dir`'s
exclusive-directory-allocation loop is still worth copying as-is (no shared
equivalent exists for that part).

#### 3. Directly-reusable helper (copy verbatim — same exact quantity Phase 55 needs)

`pinn/verification/residual_probe.py:97-103`:
```python
def _minimum_pairwise_separation(positions: torch.Tensor) -> torch.Tensor:
    """Return the minimum off-diagonal separation per snapshot in r' units."""
    difference = positions.unsqueeze(-3) - positions.unsqueeze(-2)
    separation = torch.linalg.vector_norm(difference, dim=-1)
    eye = torch.eye(3, dtype=torch.bool, device=positions.device)
    separation = separation.masked_fill(eye, torch.inf)
    return separation.amin(dim=(-2, -1))
```
This is one of SC1's seven required quantities (`min pairwise separation`)
and the formula is identical to what the new probe needs — copy it
verbatim rather than re-deriving (keeps SC3's "derive from existing code"
spirit even though this particular function isn't itself imported anywhere
else in the repo yet).

#### 4. Failure-record + CLI + evidence-write + exit-code pattern

`pinn/verification/residual_probe.py:242-267` (`_failed_record` — preserve a
structured failure instead of a bare traceback) and `:270-324` (`main`):
```python
def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.verification.residual_probe",
        description="Run the Phase 38 dual-gate residual probe on one Brutus trajectory.",
    )
    parser.add_argument("--precision", required=True, choices=("float32", "float64"))
    parser.add_argument("--device", required=True, choices=("mps", "cpu"))
    ...
    args = parser.parse_args(argv)
    ...
    try:
        raw = run_residual_on_ground_truth(...)
    except Exception as exc:  # noqa: BLE001 - fail evidence must preserve loader/runtime errors
        raw = _failed_record(args, exc)
    run_dir = _write_evidence(raw, args.evidence_root)
    print(...)
    return 0 if raw["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
```
**Anti-pattern to avoid (explicit, verified):** the `required=True` on
`--precision`/`--device` (lines 275-276) is the one part of this analog
that must **not** be copied — D-02 requires a zero-argument invocation to
reproduce the six default cases. Use
`parser.add_argument("--precision", default="float64", choices=("float32","float64"))`
/ `parser.add_argument("--device", default="cpu", choices=("mps","cpu"))`
instead. **See "Cross-Cutting Collision" below — this exact change trips an
existing Phase-38 mechanical prohibition test.**

Also note: this probe's `main()` returns `0` for "measurement completed"
(not "front_idx looked healthy" — Pattern 2 in RESEARCH.md's Architecture
Patterns). `residual_probe.py`'s own `return 0 if raw["passed"] else 1` is
a *pass/fail gate* convention (residual_probe IS a gate); the new probe is
explicitly **not** a gate (GATE-04 is Phase 56's job), so its exit-code
semantics should diverge from this one specific line even while copying
everything else in `main()`'s shape.

#### 5. Dataclass-result convention (two shapes needed: validated INPUT, plain OUTPUT)

**Output container** — model `ArchitectureCharacterizationResult` after
`pinn/verification/gate_metrics.py:203-222`:
```python
@dataclass(frozen=True)
class TrajectoryGateMetrics:
    """One trajectory's gate evidence: the full Hamiltonian series + eps_H."""

    hamiltonian_series: torch.Tensor
    eps_h: float
```
and `:271-278` (`AggregateGateMetrics`) for a second, simpler all-scalar
result container shape. Plain frozen dataclass, no `__post_init__`
validation (these are *already-computed* outputs, not caller-supplied
config) — mirror this exactly for `ArchitectureCharacterizationResult`
(fields: the SC1 seven quantities + provenance).

**Input container** — model `SweepCase` after the validated-frozen-dataclass
convention in `pinn/architecture_spec.py:35-141` (`ArchitectureSpec`,
fail-closed `__post_init__`) or the lighter `pinn/loss_catalog.py:122-159`
(`LossWeights.__post_init__`, rejects non-finite/negative fields). `SweepCase`
is caller-supplied config (via `--cases-config` JSON per D-02) so it should
validate at construction, unlike the output dataclass.

#### 6. Core measurement composition — the SC3 load-bearing pattern

`pinn/training/controllers.py:566-618` (`_build_anchor_context`, trajectory
closure + collocation sampling — verbatim, data/optimizer parts removed):
```python
def _build_anchor_context(self, source, batch, fixed_collocation_times) -> _AnchorContext:
    ...
    def traj(u_scalar: torch.Tensor) -> torch.Tensor:
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
        pos = self._model(tau_ic13, masses_t.unsqueeze(0))
        return pos.reshape(3, 3)
    ...
    if fixed_collocation_times is None:
        colloc_times = self._collocation_sampler.uniform()
    else:
        colloc_times = fixed_collocation_times
    colloc_times = np.asarray(colloc_times, dtype=np.float64)
    order = np.argsort(colloc_times)
    return _AnchorContext(traj=traj, masses=masses_t, ..., collocation_times=colloc_times[order])
```

`pinn/training/controllers.py:629-676` (`_non_data_terms` — the exact
AD/force/residual/causal-weight pipeline; **this is the one composition
the probe must mirror line-for-line**, verbatim):
```python
def _non_data_terms(self, anchor_ctx: _AnchorContext) -> dict[str, torch.Tensor]:
    ...
    u_leaf = torch.as_tensor(
        anchor_ctx.collocation_times / T_CHARACTERISTIC_TIME,
        dtype=self._dtype, device=self._device,
    )
    first, second = componentwise_du(anchor_ctx.traj, u_leaf)
    positions = torch.func.vmap(lambda s: anchor_ctx.traj(s).reshape(-1))(u_leaf)
    positions = positions.reshape(-1, 3, 3)
    velocities = first.reshape(-1, 3, 3)
    accel = second.reshape(-1, 3, 3)
    force = softened_acceleration(
        positions, anchor_ctx.masses, dtype=self._dtype, device=self._device,
    )
    residual = accel - force
    # CONF-04 / D-05: one vector-space average per time index.
    rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
    times_tensor = torch.as_tensor(
        anchor_ctx.collocation_times, dtype=self._dtype, device=self._device,
    )
    phys_term, phys_details = causal_physics_loss(
        rbar, times=times_tensor, dtype=self._dtype, device=self._device,
        return_details=True,
    )
```
The probe's `measure_case` should call `ArchitectureSpec` + `build_network`
+ `CollocationSampler(...).uniform()` + `np.argsort` (mirroring
`_build_anchor_context`), then this exact `componentwise_du` →
`softened_acceleration` → `residual = accel - force` → `rbar = (residual **
2).sum(dim=(-2,-1)) / 3.0` → `causal_physics_loss(..., return_details=True)`
chain — with the `traj`/`ic_term`/`energy_term`/`angmom_term`/data-loading
code (irrelevant to an initialization-only probe) simply omitted.

**Core formulas to copy verbatim (exact SC3 requirement — do not
re-derive):**

`front_idx`, `pinn/training/controllers.py:692-694`:
```python
"front_idx": max(
    [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
),
```

`Rbar` reduction, `pinn/training/controllers.py:652-656`:
```python
# CONF-04 / D-05: one vector-space average per time index.  The
# residual has shape (N_t, 3 bodies, 3 Cartesian components), while
# the locked Rbar contract averages the three body-vector energies,
# not all nine scalar components.
rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
```

#### 7. Validate-before-construct pattern (for `--cases-config` JSON)

`pinn/verification/fixture_loader.py:166-186` (verbatim):
```python
def _validated_variant(variant):
    if not isinstance(variant, str) or variant not in VARIANTS:
        raise ValueError(
            f"unknown dataset variant {variant!r}; the known variants are "
            f"{sorted(VARIANTS)}"
        )
    return variant


def _validated_id(id_value):
    """Return the 4-digit zero-padded ID string, or raise ``ValueError``.
    ...
    """
    if isinstance(id_value, bool):
        raise ValueError(f"trajectory id must be an int or digit string; got {id_value!r}")
    if isinstance(id_value, int):
        if id_value < 0 or id_value > _ID_MAX:
            raise ValueError(...)
        return f"{id_value:04d}"
    ...
```
Apply this exact "validate the raw JSON value into a typed field, raise
`ValueError` naming the offending field, BEFORE any tensor/path is built"
shape to parsing each case's `seed` (int), `masses` (3 finite positive
floats), and `ic13_mode` (closed enum) out of a `--cases-config` JSON list —
this is also the Security-Domain-flagged mitigation for a malformed/
adversarial config (RESEARCH.md V5 Input Validation row).

#### 8. Fail-loud error handling (inherited "for free")

`pinn/physics_residual.py:90-95`:
```python
def _require_finite(tensor, what):
    """Raise unless every component of ``tensor`` is finite (fail-loud)."""
    if not bool(torch.isfinite(tensor).all()):
        raise ValueError(
            f"non-finite {what}; refusing to produce evidence "
            f"(PHYS-02 fail-loud contract)")
```
`componentwise_du` and `softened_acceleration` both call this internally
(physics_residual.py:126, 145-146, 214-215, 230) — the new probe's core math
path needs **no additional finite-checking of its own**; a non-finite
intermediate already raises before it can reach the result dict. The
probe's *own* error handling responsibility is narrower: wrap
`measure_case`/`run_sweep` at the CLI boundary the way `residual_probe.py`'s
`main()` does (`try/except Exception` → `_failed_record`-style structured
failure → still write evidence → non-zero exit), not re-implement
finite-checking.

#### 9. Reused primitives (import and call directly — do not re-implement)

| Primitive | Exact location (verified this session) | Signature |
|---|---|---|
| `ArchitectureSpec` | `pinn/architecture_spec.py:35-141` | frozen dataclass; `input_dim=14, output_dim=9, hidden_depth=12, hidden_width=256, seed=0` defaults; `__post_init__` raises `ValueError` on any locked-field deviation |
| `build_network` | `pinn/network.py:231-255` | `build_network(spec, *, dtype, device) -> SQRSkipResNetSIREN`; seeds a local `torch.Generator` from `spec.seed`, never touches global RNG |
| `componentwise_du` | `pinn/physics_residual.py:102-147` | `componentwise_du(fn, u_leaf) -> (first, second)`; `jacrev∘jacrev` + `vmap`, fail-loud on non-finite |
| `softened_acceleration` | `pinn/physics_residual.py:193-231` | `softened_acceleration(positions, masses, *, eps_soft=EPS_SOFT, dtype, device) -> accel` |
| `causal_physics_loss` | `pinn/loss_catalog.py:283-347` | `causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None, dtype, device, return_details=False)`; with `return_details=True` returns `(loss, {"w_n":..., "rbar":...})`; raises `ValueError` on unordered `times` |
| `resolve_causal_clip_facts` | `pinn/loss_catalog.py:77-115` | `resolve_causal_clip_facts(dtype, device) -> dict` with key `"causal_clip_min_weight"` — the dtype-derived clamp floor a Tier-1 regression test must use instead of a hardcoded literal (Pitfall 1) |
| `resolve_runtime` | `pinn/runtime.py:65-95` | `resolve_runtime(precision, device) -> RuntimeSpec(precision, requested_device, dtype, torch_device)`; only `("float32","mps")` / `("float64","cpu")` resolve |
| `CollocationSampler` | `pinn/training/collocation_sampler.py:52-92` | `CollocationSampler(collocation_count, rng=np.random.default_rng(seed)).uniform(n=None) -> np.ndarray`; caller-owned RNG only, `TypeError` otherwise |
| `git_head` | `pinn/verify.py:361-384` | `git_head() -> (sha_or_None, available_bool)`; bounded subprocess, fail-soft |
| `atomic_write_text` | `pinn/training/atomic_io.py:41-64` | `atomic_write_text(path, content) -> Path`; tmp-write + fsync + `os.replace` + parent-dir fsync |
| `EPS_SOFT`, `T_CHARACTERISTIC_TIME`, `CAUSAL_ETA_C` | `pinn/constants.py:39, 31, 71` | import, never hard-code the literals |

---

### `tests/phase55/__init__.py` (test package init)

**Analog:** `tests/phase49/__init__.py` — 1 line, fully blank (no docstring,
no code). This is the simplest and most directly "empty" precedent.
`tests/phase38/__init__.py` (13 lines) is a valid alternative if a
phase-scope docstring is wanted — it contains a module docstring only, still
zero executable code. Either satisfies CONTEXT.md's "empty, matches
`tests/phase38/`" discretion note.

---

### `tests/phase55/test_architecture_characterization.py` (test, hybrid style)

**CLI-subprocess contract analog:** `tests/phase38/test_residual_probe.py`
(219 lines, read in full).

Skip-guard for RED-suite-before-module-lands (lines 26-35):
```python
ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.residual_probe"


def _load_probe():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc
```

CLI-subprocess invocation + non-overwriting evidence assertion (lines
117-134, 206-215):
```python
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
```
For Phase 55: the same subprocess-CLI pattern proves D-02's "zero-argument
invocation reproduces the six audited rows" and SC2's "recorded re-derivably"
requirement — run `[sys.executable, "-m",
"pinn.verification.architecture_characterization_probe"]` with **no
`--precision`/`--device`/`--cases-config`** and assert the evidence JSON has
exactly six rows matching `DEFAULT_CASES` labels.

**SC3 "derives from trainer, not a reimplementation" test analog:**
`tests/phase38/test_residual_probe.py:175-191`
(`test_gate_a_fails_when_direct_force_is_mutated_but_autograd_reference_is_not`)
— the established repo idiom for proving derivation-by-mutation, verbatim:
```python
def test_gate_a_fails_when_direct_force_is_mutated_but_autograd_reference_is_not(self):
    probe = _load_probe()
    root = self._evidence_root("gate-a-mutated")
    original = probe.softened_acceleration

    def mutated_force(*args, **kwargs):
        return original(*args, **kwargs) * 1.1

    with mock.patch.object(probe, "softened_acceleration", side_effect=mutated_force):
        code = probe.main([...])
    self.assertNotEqual(code, 0)
```
Adapt directly for SC3: `mock.patch.object(probe, "causal_physics_loss",
...)` (or `componentwise_du` / `softened_acceleration`) and assert the
probe's *reported* `R̄`/`w_n`/residual values change in lock-step with the
mutation — proving the probe calls the real trainer function rather than a
parallel copy of the formula. This is a stronger, more direct SC3 test than
a source-text/AST scan (see `test_prohibitions.py` note below) because it
proves behavioral coupling, not just an import statement's presence.

**pytest-function invariant-bound analog:**
`tests/phase49/test_gate03_invariants.py:1-130` (read in full for style).
Plain-`assert` parametrized style, no `unittest.TestCase`:
```python
import pytest
...

@pytest.mark.parametrize("value", [0, -1, "250", True, False])
def test_invariants_config_rejects_non_positive_or_wrong_type(value):
    from pinn.training.config import InvariantsConfig

    with pytest.raises(ValueError):
        InvariantsConfig(front_advance_window_n=value)


def test_invariant_a_trips_on_zero_and_nonfinite_weight_stats():
    ...
    assert zero.disposition is StageDisposition.HALT
    assert zero.guard == "invariant_a"
```
Use this style for the Tier-1 invariant-bound suite (D-01 tier 1):
`front_idx == 0`, `1e9 < R̄_median < 1e11`, `‖F_grav‖` O(1), min-pairwise-sep
`≫ eps_soft`, `w_2..w_16` at `resolve_causal_clip_facts(...)
["causal_clip_min_weight"]` (never a hardcoded literal — Pitfall 1) — one
plain `assert`-based test function per bound, `@pytest.mark.parametrize`
over the six default cases where the same bound applies to all of them.

**Not a template — informative-only:**
`tests/phase38/test_prohibitions.py` (existing, 324 lines) shows the repo's
AST/source-text-scan style (`ast.parse` + `ast.walk`,
`_executable_source(path)` docstring-stripped comparison,
`self.assertNotIn(token, executable, ...)`). This is a viable *alternative*
mechanism for an SC3 "derives from trainer" check (scan the new module's
source for `causal_physics_loss`/`componentwise_du`/`softened_acceleration`
import tokens) but the mutation-based test above
(`test_gate_a_fails_when_direct_force_is_mutated...`) is the stronger,
more-directly-analogous precedent already proven in this exact sibling
probe's own test file. **This file is also the source of the Cross-Cutting
Collision below — read that section before writing the new probe's CLI.**

---

### Data artifact: Tier-2 exact-value fixture (D-01 tier 2)

No committed literal-numeric-output JSON fixture precedent was found in
`tests/phase38/`, `tests/phase43/`, or `tests/phase49/` — those suites pin
thresholds, schema field names, and formulas *programmatically*
(`GATE_EPS_H_REJECT_THRESHOLD = 1e-5`-style module constants;
`assertEqual(raw["finite_difference"]["scheme"], "central; one-sided
endpoints")`-style exact-string assertions), not a full external numeric
snapshot compared at tolerance. See "No Analog Found" for the
recommendation.

---

## Shared Patterns

### Evidence directory / atomic write
**Source:** `pinn/verification/residual_probe.py:43-94` (structure) +
`pinn/training/atomic_io.py:41-64` (recommended write primitive — newer,
parent-dir-fsync'd, shared idiom).
**Apply to:** `architecture_characterization_probe.py`'s evidence writer
(`raw.json` + `summary.md`).

### Precision/device resolution
**Source:** `pinn/runtime.py:65-95` (`resolve_runtime`).
**Apply to:** `measure_case`/`run_sweep`'s dtype/device threading — never a
bare `torch.float64`/`"cpu"` literal scattered through the module.

### Fail-loud non-finite checking
**Source:** `pinn/physics_residual.py:90-95` (`_require_finite`).
**Apply to:** nothing needs to be written for this — it's inherited
automatically by calling `componentwise_du`/`softened_acceleration`
directly (Pattern 8 above). Flagging here only so the executor doesn't
duplicate it.

### Validate-before-construct for external config input
**Source:** `pinn/verification/fixture_loader.py:166-186`.
**Apply to:** `--cases-config` JSON parsing, before any `ArchitectureSpec`/
tensor is built.

### Git tree-state provenance
**Source:** `pinn/verify.py:361-384` (`git_head`).
**Apply to:** the evidence provenance block (SC2's "command, tree state,
full output" re-derivability requirement).

### Dataclass conventions (two distinct shapes in this repo)
**Source A (validated input):** `pinn/architecture_spec.py:35-141`,
`pinn/loss_catalog.py:122-159` — frozen + `__post_init__` raising
`ValueError` before any tensor is built.
**Source B (plain computed output):** `pinn/verification/gate_metrics.py:203-222,
271-287` — frozen, no validation, exhaustive docstring naming every field's
formula.
**Apply to:** `SweepCase` uses Source A; `ArchitectureCharacterizationResult`
uses Source B.

---

## Cross-Cutting Collision Found

**Not present in CONTEXT.md or RESEARCH.md — discovered during this
mapping pass by reading `tests/phase38/test_prohibitions.py`, which
RESEARCH.md's Sources list does not cite.**

`tests/phase38/test_prohibitions.py:99-119` (`_discover_phase38_modules`)
globs **all** of `pinn/**/*.py` minus a 4-entry `_EXCLUDE_SUFFIXES` list
(lines 62-69):
```python
_EXCLUDE_SUFFIXES = (
    "pinn/basic_architecture.py",
    "pinn/data-processing-pipeline-full.py",
    "pinn/runtime.py",
    "pinn/verification/componentwise_ad.py",
)
```
`tests/phase38/test_prohibitions.py:289-303`
(`test_no_precision_default_in_discovered_modules`) then asserts, for every
discovered module:
```python
# No argparse precision default (required=True is fine).
self.assertNotIn('add_argument("--precision", default=', executable)
self.assertNotIn("add_argument('--precision', default=", executable)
```

`pinn/verification/architecture_characterization_probe.py` does not exist
yet, so it is not in `_EXCLUDE_SUFFIXES`. Once created, it **will** be swept
into this glob. D-02 / RESEARCH.md Pitfall 3 explicitly requires
`parser.add_argument("--precision", default="float64", choices=(...))` —
the literal substring this existing test bans. **This is a verified,
mechanical collision, not a hypothetical**: writing the probe's CLI exactly
as D-02 requires will make `pytest tests/ -q` show a new failure in
`test_prohibitions.py`, which the "diff the failure set against the 14
pre-existing failures" sampling discipline (RESEARCH.md Validation
Architecture) would correctly attribute to Phase 55.

**Existing precedent for the fix:** `pinn/runtime.py` is excluded from this
exact same glob for the analogous reason — the comment at
`test_prohibitions.py:62-63` states the exclude list covers "Phase-37
substrate already covered by tests/phase37 and legitimately owning the
precision seam." `architecture_characterization_probe.py` legitimately owns
a comparable, phase-scoped seam (D-02's zero-argument reproduction
contract).

This is a planning-time decision, not a pattern-mapping one — the planner
should include an explicit small task to add
`"pinn/verification/architecture_characterization_probe.py"` to
`_EXCLUDE_SUFFIXES` in `tests/phase38/test_prohibitions.py` (mirroring the
`runtime.py` precedent's documented rationale, one line + one comment), and
treat that as a required, narrowly-scoped modification to an existing
Phase-38 test file rather than routing around the substring check
mechanically (which would defeat its intent for every *other* module it
still legitimately protects).

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| Tier-2 exact-value fixture (six-row baseline JSON, D-01 tier 2) | test fixture / static data | batch/regression comparison | No committed literal-numeric-output JSON fixture precedent in `tests/phase38/`, `tests/phase43/`, or `tests/phase49/` — those suites pin thresholds/schema/formulas as Python constants and exact-string assertions, not an external data snapshot compared at tolerance. Recommendation: follow `residual_probe.py:79`'s own evidence-serialization convention (`json.dumps(raw, sort_keys=True, indent=2)`) for the fixture's *shape*, store it under `tests/phase55/fixtures/` or alongside the module, and compare with `pytest.approx(..., rel=<tight tolerance>)` per-field in a plain pytest-style test (Source B dataclass style, Phase 49 test style) — this is genuinely new test-design territory in this repo, not a copy job. |

---

## Metadata

**Analog search scope:** `pinn/verification/` (all 7 existing probe
modules), `pinn/training/controllers.py`, `pinn/physics_residual.py`,
`pinn/loss_catalog.py`, `pinn/architecture_spec.py`, `pinn/network.py`,
`pinn/runtime.py`, `pinn/training/collocation_sampler.py`,
`pinn/training/atomic_io.py`, `pinn/verify.py`, `pinn/constants.py`,
`tests/phase38/`, `tests/phase43/`, `tests/phase49/`.

**Files read in full this session:** `pinn/verification/residual_probe.py`,
`pinn/verification/gate_metrics.py`, `pinn/physics_residual.py`,
`pinn/loss_catalog.py`, `pinn/architecture_spec.py`, `pinn/network.py`,
`pinn/runtime.py`, `pinn/training/collocation_sampler.py`,
`pinn/training/atomic_io.py`, `pinn/constants.py`,
`tests/phase38/test_residual_probe.py`.

**Files read via targeted (non-overlapping) ranges:** `pinn/verify.py`
(340-400), `pinn/training/controllers.py` (560-710),
`tests/phase49/test_gate03_invariants.py` (1-130),
`tests/phase38/test_prohibitions.py` (1-80, 284-324),
`pinn/verification/fixture_loader.py` (grep + 160-192).

**Files confirmed via grep/anchor search only (not needed as full-text
excerpts given 3-5 strong analogs were already established):**
`pinn/verification/gradcheck_probe.py`, `pinn/verification/overfit_probe.py`,
`pinn/verification/componentwise_ad.py`, `pinn/verification/target_frame_probe.py`.

**Pattern extraction date:** 2026-09-04

---

*Phase: 55-Architecture Characterization Probe*
*Patterns mapped: 2026-09-04*

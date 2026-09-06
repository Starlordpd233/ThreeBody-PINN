"""Architecture characterization probe — initialization-only residual measurement.

This module measures the SQR-SkipResNet-SIREN network's residual and
causal-weight behaviour at network initialization: no data file is read, no
optimizer is constructed, and no ``.backward()`` / ``.step()`` call is issued.

Every reported physics quantity is derived from a direct call into the
trainer's own functions — ``pinn.loss_catalog.causal_physics_loss``,
``pinn.physics_residual.componentwise_du``, and
``pinn.physics_residual.softened_acceleration`` — so a probe result is
evidence about the shipped recipe, not about a parallel copy of it.

Median convention (even ``n_col = 16``)
---------------------------------------
Every reported median is ``numpy.median``: the arithmetic mean of the two
central order statistics. This is explicitly NOT ``torch.median``, which
returns the lower of the two central values for an even-length input.

Norm convention
---------------
The four norm columns (``‖r′‖``, ``‖v′‖``, ``‖a′‖``, ``‖F_grav‖``) are the
plain Frobenius norm over the nine scalar components of the
``(3 bodies × 3 Cartesian)`` tensor at each collocation point — i.e.
``torch.linalg.vector_norm`` of the flattened 9-vector. Combined with the
locked ``R̄`` contract ``rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0``,
this identity holds: ``R̄ ≈ ‖a′‖² / 3`` when ``‖a′‖ ≫ ‖F_grav‖``.

IC13 RNG scheme
---------------
``ic13_mode="zero"`` returns a 13-element zero vector.
``ic13_mode="random_tanh"`` draws 13 standard-normal values from
``numpy.random.default_rng(case.seed + IC13_RNG_OFFSET)`` (offset
``10_000_000``) and returns their elementwise ``tanh``. The offset keeps
this stream independent of the collocation RNG (seeded with ``case.seed``)
in an order-insensitive way.
"""

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
from pinn.training.collocation_sampler import CollocationSampler
from pinn.verify import git_head


DEFAULT_N_COL = 16
IC13_DIM = 13
IC13_RNG_OFFSET = 10_000_000
MEDIAN_CONVENTION = (
    "numpy.median: arithmetic mean of the two central order statistics "
    "(explicitly not torch.median's lower-of-two)"
)
_ALLOWED_IC13_MODES = frozenset({"zero", "random_tanh"})
_IC13_RNG_SCHEME_ZERO = "zero-vector"
_IC13_RNG_SCHEME_RANDOM_TANH = (
    "numpy.random.default_rng(seed + IC13_RNG_OFFSET) standard-normal "
    "then elementwise tanh"
)
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "55-architecture-characterization-probe" / "evidence" / "probe"
)
_GIT_TIMEOUT_S = 10.0
_MODULE_PROG = "python -m pinn.verification.architecture_characterization_probe"
EVIDENCE_SCHEMA_VERSION = 1
EVIDENCE_TOP_LEVEL_KEYS = frozenset({
    "schema_version",
    "provenance",
    "configuration",
    "cases",
    "failure",
})

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
]


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
            raise ValueError(
                f"SweepCase.label must be a non-empty str; got {self.label!r}"
            )
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError(
                f"SweepCase.seed must be a non-negative int (not bool); "
                f"got {self.seed!r}"
            )
        try:
            raw_masses = tuple(self.masses)
        except TypeError as exc:
            raise ValueError(
                f"SweepCase.masses must be exactly three finite strictly "
                f"positive floats; got {self.masses!r}"
            ) from exc
        if len(raw_masses) != 3:
            raise ValueError(
                f"SweepCase.masses must be exactly three finite strictly "
                f"positive floats; got {self.masses!r}"
            )
        converted: list[float] = []
        for mass in raw_masses:
            if isinstance(mass, bool):
                raise ValueError(
                    f"SweepCase.masses must be exactly three finite strictly "
                    f"positive floats; got {self.masses!r}"
                )
            try:
                value = float(mass)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"SweepCase.masses must be exactly three finite strictly "
                    f"positive floats; got {self.masses!r}"
                ) from exc
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(
                    f"SweepCase.masses must be exactly three finite strictly "
                    f"positive floats; got {self.masses!r}"
                )
            converted.append(value)
        object.__setattr__(self, "masses", (converted[0], converted[1], converted[2]))
        if not isinstance(self.ic13_mode, str) or self.ic13_mode not in _ALLOWED_IC13_MODES:
            raise ValueError(
                f"SweepCase.ic13_mode must be one of {sorted(_ALLOWED_IC13_MODES)}; "
                f"got {self.ic13_mode!r}"
            )


@dataclass(frozen=True)
class ArchitectureCharacterizationResult:
    """Plain computed output of one ``measure_case`` call.

    Fields
    ------
    label, seed, masses, ic13_mode
        Copied from the input ``SweepCase``.
    r_norm_median
        ``numpy.median`` of the per-point Frobenius norms of predicted
        positions ``r'`` (shape ``(N_t, 3, 3)`` flattened to 9 components).
    v_norm_median
        ``numpy.median`` of the per-point Frobenius norms of ``v' = dr'/du``
        from ``componentwise_du``.
    a_norm_median
        ``numpy.median`` of the per-point Frobenius norms of
        ``a' = d²r'/du²`` from ``componentwise_du``.
    f_grav_norm_median
        ``numpy.median`` of the per-point Frobenius norms of
        ``softened_acceleration`` (``F_grav``).
    min_pairwise_separation_median
        ``numpy.median`` of the per-point minimum off-diagonal pairwise
        separation of predicted positions.
    rbar_median
        ``numpy.median`` of ``R̄_n = (residual ** 2).sum(dim=(-2, -1)) / 3.0``
        with ``residual = a' - F_grav`` (CONF-04 / D-05).
    causal_weights
        The trainer's ``w_n`` vector from
        ``causal_physics_loss(..., return_details=True)`` as a Python tuple.
    front_idx
        ``max([n for n, w in enumerate(w_n) if w > 0.5], default=-1)`` —
        the trainer formula from ``controllers.py``.
    n_col, precision, device
        Runtime provenance of this measurement.
    collocation_times
        The sorted raw collocation times in ``[0, T]`` that were fed to
        ``causal_physics_loss``.
    causal_clip_min_weight
        ``resolve_causal_clip_facts(dtype, device)['causal_clip_min_weight']``
        for this runtime — never a copied literal.
    median_convention
        The documented even-N median contract (``MEDIAN_CONVENTION``).
    ic13_rng_scheme
        The documented IC13 construction used for this case.
    """

    label: str
    seed: int
    masses: tuple[float, float, float]
    ic13_mode: str
    r_norm_median: float
    v_norm_median: float
    a_norm_median: float
    f_grav_norm_median: float
    min_pairwise_separation_median: float
    rbar_median: float
    causal_weights: tuple[float, ...]
    front_idx: int
    n_col: int
    precision: str
    device: str
    collocation_times: tuple[float, ...]
    causal_clip_min_weight: float
    median_convention: str
    ic13_rng_scheme: str


DEFAULT_CASES: tuple[SweepCase, ...] = (
    SweepCase(label="41", seed=41, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="42", seed=42, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="43", seed=43, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="0", seed=0, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="7", seed=7, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(
        label="41-variable-mass",
        seed=41,
        masses=(1.0, 0.8, 0.6),
        ic13_mode="random_tanh",
    ),
)


def _frobenius_per_point(tensor: torch.Tensor) -> torch.Tensor:
    """Frobenius norm over the nine scalar components at each collocation point."""
    return torch.linalg.vector_norm(tensor.reshape(tensor.shape[0], 9), dim=-1)


def _median(values) -> float:
    """Even-N median via ``numpy.median`` (mean of the two central order stats)."""
    if torch.is_tensor(values):
        array = values.detach().cpu().numpy()
    else:
        array = np.asarray(values)
    return float(np.median(array))


def _front_idx(w_n_list) -> int:
    """Trainer formula: max n with w > 0.5, else the ``default=-1`` sentinel."""
    return max(
        [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
    )


def _minimum_pairwise_separation(positions: torch.Tensor) -> torch.Tensor:
    """Return the minimum off-diagonal separation per snapshot in r' units."""
    difference = positions.unsqueeze(-3) - positions.unsqueeze(-2)
    separation = torch.linalg.vector_norm(difference, dim=-1)
    eye = torch.eye(3, dtype=torch.bool, device=positions.device)
    separation = separation.masked_fill(eye, torch.inf)
    return separation.amin(dim=(-2, -1))


def _ic13_for_case(case: SweepCase, *, dtype, device) -> torch.Tensor:
    if case.ic13_mode == "zero":
        return torch.zeros(IC13_DIM, dtype=dtype, device=device)
    rng = np.random.default_rng(case.seed + IC13_RNG_OFFSET)
    raw = rng.standard_normal(IC13_DIM)
    return torch.as_tensor(np.tanh(raw), dtype=dtype, device=device)


def _ic13_rng_scheme(ic13_mode: str) -> str:
    if ic13_mode == "zero":
        return _IC13_RNG_SCHEME_ZERO
    return _IC13_RNG_SCHEME_RANDOM_TANH


def measure_case(
    case: SweepCase,
    *,
    n_col: int = DEFAULT_N_COL,
    precision: str = "float64",
    device: str = "cpu",
) -> ArchitectureCharacterizationResult:
    """Measure all seven INST-04 quantities for one case at initialization."""
    runtime = resolve_runtime(precision, device)
    dtype = runtime.dtype
    torch_device = runtime.torch_device
    spec = ArchitectureSpec(seed=case.seed)
    model = build_network(spec, dtype=dtype, device=torch_device)
    model.eval()

    ic13 = _ic13_for_case(case, dtype=dtype, device=torch_device)
    masses_t = torch.as_tensor(case.masses, dtype=dtype, device=torch_device)

    def traj(u_scalar: torch.Tensor) -> torch.Tensor:
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
        pos = model(tau_ic13, masses_t.unsqueeze(0))
        return pos.reshape(3, 3)

    colloc_times = CollocationSampler(
        collocation_count=n_col,
        rng=np.random.default_rng(case.seed),
    ).uniform()
    colloc_times = np.asarray(colloc_times, dtype=np.float64)
    order = np.argsort(colloc_times)
    sorted_times = colloc_times[order]

    u_leaf = torch.as_tensor(
        sorted_times / T_CHARACTERISTIC_TIME,
        dtype=dtype,
        device=torch_device,
    )
    first, second = componentwise_du(traj, u_leaf)
    positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_leaf)
    positions = positions.reshape(-1, 3, 3)
    velocities = first.reshape(-1, 3, 3)
    accel = second.reshape(-1, 3, 3)
    force = softened_acceleration(
        positions, masses_t, dtype=dtype, device=torch_device,
    )
    residual = accel - force
    # CONF-04 / D-05: one vector-space average per time index.  The
    # residual has shape (N_t, 3 bodies, 3 Cartesian components), while
    # the locked Rbar contract averages the three body-vector energies,
    # not all nine scalar components.
    rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
    times_tensor = torch.as_tensor(
        sorted_times, dtype=dtype, device=torch_device,
    )
    _phys_term, phys_details = causal_physics_loss(
        rbar,
        times=times_tensor,
        dtype=dtype,
        device=torch_device,
        return_details=True,
    )
    w_n_list = phys_details["w_n"].tolist()
    clip_facts = resolve_causal_clip_facts(dtype, torch_device)
    return ArchitectureCharacterizationResult(
        label=case.label,
        seed=case.seed,
        masses=case.masses,
        ic13_mode=case.ic13_mode,
        r_norm_median=_median(_frobenius_per_point(positions)),
        v_norm_median=_median(_frobenius_per_point(velocities)),
        a_norm_median=_median(_frobenius_per_point(accel)),
        f_grav_norm_median=_median(_frobenius_per_point(force)),
        min_pairwise_separation_median=_median(
            _minimum_pairwise_separation(positions)
        ),
        rbar_median=_median(rbar),
        causal_weights=tuple(float(weight) for weight in w_n_list),
        front_idx=_front_idx(w_n_list),
        n_col=int(n_col),
        precision=runtime.precision,
        device=runtime.requested_device,
        collocation_times=tuple(float(time) for time in sorted_times),
        causal_clip_min_weight=float(clip_facts["causal_clip_min_weight"]),
        median_convention=MEDIAN_CONVENTION,
        ic13_rng_scheme=_ic13_rng_scheme(case.ic13_mode),
    )


def run_sweep(
    cases: tuple[SweepCase, ...] = DEFAULT_CASES,
    *,
    n_col: int = DEFAULT_N_COL,
    precision: str = "float64",
    device: str = "cpu",
) -> tuple[ArchitectureCharacterizationResult, ...]:
    """Measure each case independently; ``DEFAULT_CASES`` is data, not a path."""
    return tuple(
        measure_case(case, n_col=n_col, precision=precision, device=device)
        for case in cases
    )


def _validated_label(value) -> str:
    if not isinstance(value, str) or value == "":
        raise ValueError(f"label must be a non-empty str; got {value!r}")
    return value


def _validated_seed(value) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(
            f"seed must be a non-negative int (not bool); got {value!r}"
        )
    return value


def _validated_masses(value) -> tuple[float, float, float]:
    try:
        raw = tuple(value)
    except TypeError as exc:
        raise ValueError(
            f"masses must be exactly three finite strictly positive floats; "
            f"got {value!r}"
        ) from exc
    if len(raw) != 3:
        raise ValueError(
            f"masses must be exactly three finite strictly positive floats; "
            f"got {value!r}"
        )
    converted: list[float] = []
    for mass in raw:
        if isinstance(mass, bool):
            raise ValueError(
                f"masses must be exactly three finite strictly positive floats; "
                f"got {value!r}"
            )
        try:
            number = float(mass)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"masses must be exactly three finite strictly positive floats; "
                f"got {value!r}"
            ) from exc
        if not math.isfinite(number) or number <= 0.0:
            raise ValueError(
                f"masses must be exactly three finite strictly positive floats; "
                f"got {value!r}"
            )
        converted.append(number)
    return (converted[0], converted[1], converted[2])


def _validated_ic13_mode(value) -> str:
    if not isinstance(value, str) or value not in _ALLOWED_IC13_MODES:
        raise ValueError(
            f"ic13_mode must be one of {sorted(_ALLOWED_IC13_MODES)}; got {value!r}"
        )
    return value


def load_cases_config(path) -> tuple[SweepCase, ...]:
    """Validate-before-construct JSON case-list parser.

    Every entry is checked through the per-field validators before any
    ``SweepCase`` is built, and ``SweepCase.__post_init__`` re-checks the
    same invariants as a second independent net. No tensor, path, or run
    directory is allocated here.
    """
    text = Path(path).read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"cases-config is not valid JSON: {exc}") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError(
            "cases-config must be a non-empty list of objects; "
            f"got {type(payload).__name__}"
        )
    cases: list[SweepCase] = []
    for index, entry in enumerate(payload):
        if not isinstance(entry, dict):
            raise ValueError(
                f"cases-config[{index}] must be an object; "
                f"got {type(entry).__name__}"
            )
        cases.append(
            SweepCase(
                label=_validated_label(entry.get("label")),
                seed=_validated_seed(entry.get("seed")),
                masses=_validated_masses(entry.get("masses")),
                ic13_mode=_validated_ic13_mode(entry.get("ic13_mode")),
            )
        )
    return tuple(cases)


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
    raise FileExistsError(
        f"could not allocate exclusive evidence directory under {evidence_root}"
    )


def _git_worktree_dirty() -> tuple[bool | None, bool]:
    """Return ``(dirty_or_None, available)`` from bounded ``git status --porcelain``.

    Mirrors ``pinn.verify.git_head``: a missing binary, a non-repository
    directory, a non-zero exit, and a timeout all degrade to
    ``(None, False)`` rather than raising.
    """
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT_S,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None, False
    if completed.returncode != 0:
        return None, False
    return bool(completed.stdout.strip()), True


def _command_string(argv) -> str:
    parts = [_MODULE_PROG, *(str(item) for item in argv)]
    return " ".join(parts) if argv else _MODULE_PROG


def _configuration(args) -> dict:
    cases_config = args.cases_config
    return {
        "precision": args.precision,
        "device": args.device,
        "n_col": int(args.n_col),
        "cases_config": None if cases_config is None else str(cases_config),
        "evidence_root": str(args.evidence_root),
    }


def _provenance(argv, args, runtime) -> dict:
    git_sha, git_available = git_head()
    dirty, dirty_available = _git_worktree_dirty()
    if runtime is not None:
        clip_facts = resolve_causal_clip_facts(runtime.dtype, runtime.torch_device)
        precision = runtime.precision
        device = runtime.requested_device
    else:
        clip_facts = None
        precision = args.precision
        device = args.device
    return {
        "argv": [str(item) for item in argv],
        "command": _command_string(argv),
        "git_sha": git_sha,
        "git_available": git_available,
        "git_worktree_dirty": dirty,
        "git_worktree_dirty_available": dirty_available,
        "torch_version": torch.__version__,
        "numpy_version": np.__version__,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "precision": precision,
        "device": device,
        "n_col": int(args.n_col),
        "median_convention": MEDIAN_CONVENTION,
        "ic13_rng_scheme": (
            f"zero: {_IC13_RNG_SCHEME_ZERO}; "
            f"random_tanh: {_IC13_RNG_SCHEME_RANDOM_TANH}"
        ),
        "causal_clip_facts": clip_facts,
    }


def _result_record(result: ArchitectureCharacterizationResult) -> dict:
    return asdict(result)


def _fmt_quantity(value: float) -> str:
    absolute = abs(value)
    if absolute >= 1.0e4 or (absolute != 0.0 and absolute < 1.0e-2):
        return f"{value:.3e}"
    return f"{value:.4g}"


def _summary_markdown(raw: dict) -> str:
    """Human-readable table mirroring the 2026-08-17 audit §6b layout.

    Reports measured values only. Makes no claim about whether any value
    is acceptable.
    """
    provenance = raw.get("provenance") or {}
    lines = [
        "# Architecture characterization probe",
        "",
        "## Provenance",
        "",
        f"- command: `{provenance.get('command', '')}`",
        f"- git_sha: `{provenance.get('git_sha')}` "
        f"(available={provenance.get('git_available')})",
        f"- git_worktree_dirty: `{provenance.get('git_worktree_dirty')}` "
        f"(available={provenance.get('git_worktree_dirty_available')})",
        f"- timestamp: `{provenance.get('timestamp', '')}`",
        f"- precision/device: `{provenance.get('precision')}` / "
        f"`{provenance.get('device')}`",
        f"- n_col: `{provenance.get('n_col')}`",
        f"- median_convention: {provenance.get('median_convention', '')}",
        f"- ic13_rng_scheme: {provenance.get('ic13_rng_scheme', '')}",
        "",
    ]
    failure = raw.get("failure")
    if failure is not None:
        lines.extend(
            [
                "## Failure",
                "",
                "Measurement did not complete.",
                "",
                f"- type: `{failure.get('type', '')}`",
                f"- message: {failure.get('message', '')}",
                "",
            ]
        )
        return "\n".join(lines)
    lines.extend(
        [
            "## Cases",
            "",
            "| seed / IC | ‖r′‖ | ‖v′‖ | ‖a′‖ = ‖d²r′/du²‖ | ‖F_grav‖ | "
            "min pairwise sep | `R̄` median | `front_idx` |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for case in raw.get("cases") or []:
        seed = case.get("seed")
        label = case.get("label")
        masses = case.get("masses")
        ic13_mode = case.get("ic13_mode")
        identity = f"{label} (seed={seed}, m={masses}, IC13={ic13_mode})"
        lines.append(
            "| "
            + " | ".join(
                [
                    identity,
                    _fmt_quantity(float(case["r_norm_median"])),
                    _fmt_quantity(float(case["v_norm_median"])),
                    _fmt_quantity(float(case["a_norm_median"])),
                    _fmt_quantity(float(case["f_grav_norm_median"])),
                    _fmt_quantity(float(case["min_pairwise_separation_median"])),
                    _fmt_quantity(float(case["rbar_median"])),
                    str(int(case["front_idx"])),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _write_evidence(raw: dict, evidence_root: Path) -> Path:
    run_dir = _new_run_dir(Path(evidence_root))
    atomic_write_text(
        run_dir / "raw.json",
        json.dumps(raw, sort_keys=True, indent=2) + "\n",
    )
    atomic_write_text(run_dir / "summary.md", _summary_markdown(raw))
    return run_dir


def _failed_record(argv, args, exc: Exception) -> dict:
    """Retain a structured failed invocation instead of swallowing its cause."""
    runtime = None
    try:
        runtime = resolve_runtime(args.precision, args.device)
    except Exception:
        runtime = None
    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "provenance": _provenance(argv, args, runtime),
        "configuration": _configuration(args),
        "cases": [],
        "failure": {"type": type(exc).__name__, "message": str(exc)},
    }


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=_MODULE_PROG,
        description=(
            "Measure SQR-SkipResNet-SIREN residual and causal-weight behaviour "
            "at initialization. Reports quantities; does not judge the recipe."
        ),
    )
    parser.add_argument(
        "--precision",
        default="float64",
        choices=("float32", "float64"),
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=("mps", "cpu"),
    )
    parser.add_argument("--n-col", type=int, default=DEFAULT_N_COL)
    parser.add_argument("--cases-config", type=Path, default=None)
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=_DEFAULT_EVIDENCE_ROOT,
    )
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
        results = run_sweep(
            cases,
            n_col=args.n_col,
            precision=args.precision,
            device=args.device,
        )
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

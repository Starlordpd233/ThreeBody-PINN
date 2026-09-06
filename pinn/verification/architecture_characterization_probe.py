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

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.loss_catalog import causal_physics_loss, resolve_causal_clip_facts
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.training.collocation_sampler import CollocationSampler


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

__all__ = [
    "SweepCase",
    "ArchitectureCharacterizationResult",
    "DEFAULT_CASES",
    "measure_case",
    "run_sweep",
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

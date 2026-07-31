"""Phase 47 / CONF-02 — the S_H pipeline: split-scoped median, fail-closed
validation, and the ``run_dir/training_metadata.json`` artifact.

Contract (``pinn_architecture.md`` §3.4:539-542, transcribed in 47-CONTEXT.md
D-09..D-18): ``S_H = median_train(K0 + Uabs0)`` is computed ONCE, in float64,
at run setup before step 1, over the train split only — the
``StageIndex.from_split(adapter, manifest, "train")`` population intersected
with the Stage-0 admitted pool via ``records_at_or_below(0)`` — from
per-trajectory components captured at admission in the completed CONF-09
frame tuple ``{position: r_prime, time: u, velocity: dr_prime_du, masses:
ordered_raw}`` at the training softening ``EPS_SOFT = 1e-5``. It is never
computed per minibatch, never per stage, and never recomputed mid-run
(D-09/D-13).

Both ``S_H`` and ``eps_H = energy_floor_factor * S_H`` persist in
``run_dir/training_metadata.json`` (D-15) — derived data, never written into
the frozen config (D-16) — written once at setup through
``atomic_write_text`` so a crashed setup can never leave a partial artifact
under the canonical name. Every load RE-VALIDATES the payload: exact key set,
the fail-closed finite-and-strictly-positive predicate (D-17), the ``eps_h``
product, the frame block against the live ratified frame, and the
persisted-vs-live ``eps_train`` / ``energy_floor_factor`` cross-checks
(D-18). An invalid value is a refusal before step 1; no substitute value of
any kind exists anywhere in this module.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from pinn.constants import EPS_SOFT
from pinn.training.atomic_io import atomic_write_text
from pinn.training.validation_gate import RATIFIED_VALIDATION_FRAME

__all__ = [
    "TRAINING_METADATA_FILENAME",
    "TRAINING_METADATA_SCHEMA_VERSION",
    "compute_s_h",
    "validate_s_h",
    "write_training_metadata",
    "load_training_metadata",
]

TRAINING_METADATA_FILENAME = "training_metadata.json"
TRAINING_METADATA_SCHEMA_VERSION = 1

_METADATA_KEYS = frozenset(
    {
        "schema_version",
        "s_h",
        "eps_h",
        "n_train",
        "eps_train",
        "energy_floor_factor",
        "frame",
    }
)
_FRAME_KEYS = frozenset({"position_frame", "time_coord", "mass_convention"})


def compute_s_h(train_source) -> tuple[float, int]:
    """``S_H = median_train(K0 + Uabs0)`` over the Stage-0 train pool.

    The pool is ``sorted(train_source.records_at_or_below(0))`` — the
    established "admitted at or before the current stage" idiom shared with
    the validation-gate and replay pools — and the per-key sums
    ``k0(key) + uabs0(key)`` accumulate into a float64 numpy array before
    ``numpy.median`` reduces them (D-14: permutation-invariant; an even
    population averages the two central values). The components were captured
    at admission in float64 in the completed CONF-09 frame (D-12); this
    reduction runs once at run setup (D-13), never inside
    ``AdmittedSetAdapter._materialize`` and never per minibatch.

    Returns ``(s_h, n_train)``. An empty pool refuses (D-17) BEFORE numpy
    could reach a NaN-median path.
    """
    pool = sorted(train_source.records_at_or_below(0))
    if not pool:
        raise ValueError(
            "S_H train-split population is empty (N_train == 0): "
            "the run refuses before step 1"
        )
    sums = np.array(
        [float(train_source.k0(key)) + float(train_source.uabs0(key)) for key in pool],
        dtype=np.float64,
    )
    return float(np.median(sums)), len(pool)


def validate_s_h(value: float) -> float:
    """The D-17 fail-closed predicate: finite AND strictly positive.

    Exactly 0.0 refuses the same as a negative or non-finite value — the
    boundary case is a refusal, never a pass. Returns the value unchanged on
    success; raises ``ValueError`` carrying the offending value otherwise.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            "S_H must be finite and strictly positive; got non-numeric "
            f"{type(value).__name__} {value!r}"
        )
    number = float(value)
    if not (math.isfinite(number) and number > 0.0):
        raise ValueError(f"S_H must be finite and strictly positive; got {value!r}")
    return number


def _validate_positive_int(value, *, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{what} must be a positive integer; got {value!r}")
    number = int(value)
    if number <= 0:
        raise ValueError(f"{what} must be a positive integer; got {value!r}")
    return number


def _json_number(payload: dict, key: str) -> float:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a JSON number; got {value!r}")
    return float(value)


def _live_frame_block() -> dict:
    return {
        "position_frame": RATIFIED_VALIDATION_FRAME.position_frame,
        "time_coord": RATIFIED_VALIDATION_FRAME.time_coord,
        "mass_convention": RATIFIED_VALIDATION_FRAME.mass_convention,
    }


def write_training_metadata(run_dir, *, s_h, n_train, energy_floor_factor) -> Path:
    """Validate, then atomically persist ``run_dir/training_metadata.json``.

    Validation precedes the write (D-17: refusal precedes artifact — a
    partially-completed run must not leave records that read like evidence).
    ``eps_h`` is computed here as ``energy_floor_factor * s_h`` and both are
    persisted (D-15); the frame block quotes the live ratified frame strings.
    Serialization goes through ``atomic_write_text`` — never a raw
    ``open().write()`` — so a crashed setup cannot leave a partial artifact
    under the canonical name.
    """
    s_h = validate_s_h(s_h)
    n_train = _validate_positive_int(n_train, what="n_train")
    factor = float(energy_floor_factor)
    if not (math.isfinite(factor) and factor > 0.0):
        raise ValueError(
            "energy_floor_factor must be finite and strictly positive; "
            f"got {energy_floor_factor!r}"
        )
    payload = {
        "schema_version": TRAINING_METADATA_SCHEMA_VERSION,
        "s_h": s_h,
        "eps_h": factor * s_h,
        "n_train": n_train,
        "eps_train": EPS_SOFT,
        "energy_floor_factor": factor,
        "frame": _live_frame_block(),
    }
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    return atomic_write_text(Path(run_dir) / TRAINING_METADATA_FILENAME, text)


def load_training_metadata(run_dir, *, expected_energy_floor_factor,
                           expected_eps_train=EPS_SOFT) -> dict:
    """Parse and RE-VALIDATE the persisted training metadata (D-18).

    A persisted number is trusted only after re-checking, never because it is
    present: exact key set (unknown keys fail closed the same as missing
    ones), schema version, the D-17 predicate on ``s_h``, the exact product
    ``eps_h == energy_floor_factor * s_h`` (float64 multiply is
    deterministic), ``n_train`` a positive integer (bool excluded), the frame
    block equal to the live ratified frame strings, and — because
    ``energy_floor_factor`` is configurable and a loader cannot know the live
    value from its own signature — the persisted ``eps_train`` /
    ``energy_floor_factor`` must equal the EXPLICIT expected bindings.
    Raises ``ValueError`` with a specific reason on any violation.
    """
    path = Path(run_dir) / TRAINING_METADATA_FILENAME
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"training metadata not found: {path}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"training metadata is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("training metadata payload must be a JSON object")

    keys = set(payload)
    if keys != set(_METADATA_KEYS):
        raise ValueError(
            f"training metadata keys must be exactly {sorted(_METADATA_KEYS)}; "
            f"got {sorted(keys)}"
        )
    if payload["schema_version"] != TRAINING_METADATA_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {TRAINING_METADATA_SCHEMA_VERSION}; "
            f"got {payload['schema_version']!r}"
        )

    s_h = validate_s_h(payload["s_h"])
    eps_h = _json_number(payload, "eps_h")
    n_train = _validate_positive_int(payload["n_train"], what="n_train")
    factor = _json_number(payload, "energy_floor_factor")
    eps_train = _json_number(payload, "eps_train")

    if eps_h != factor * s_h:
        raise ValueError(
            f"eps_h {payload['eps_h']!r} != energy_floor_factor * s_h "
            f"({payload['energy_floor_factor']!r} * {s_h!r})"
        )
    if eps_train != float(expected_eps_train):
        raise ValueError(
            f"persisted eps_train {payload['eps_train']!r} != expected "
            f"{float(expected_eps_train)!r}"
        )
    if factor != float(expected_energy_floor_factor):
        raise ValueError(
            f"persisted energy_floor_factor {payload['energy_floor_factor']!r} "
            f"!= expected {float(expected_energy_floor_factor)!r}"
        )

    frame = payload["frame"]
    if not isinstance(frame, dict) or set(frame) != set(_FRAME_KEYS):
        raise ValueError(
            f"frame keys must be exactly {sorted(_FRAME_KEYS)}; got {frame!r}"
        )
    live_frame = _live_frame_block()
    for name in sorted(_FRAME_KEYS):
        if frame[name] != live_frame[name]:
            raise ValueError(
                f"frame.{name} {frame[name]!r} != live ratified "
                f"{live_frame[name]!r}"
            )
    return payload

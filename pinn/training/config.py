"""Phase 40/41 — nested frozen TrainingConfig (CTX-42 + CTRL-01 seams).

Groups run / stage / opt / loss as frozen dataclasses with fail-closed
``__post_init__`` validation (ArchitectureSpec idiom). CTX-39 required fields
(``max_epochs``, ``n_adam`` / T_max, ``stagnation_window``,
``percentile_10_relaxation``) raise ``ConfigRequiredError`` if unset.
GAP-40-02 → A: ``n_adam <= max_epochs`` (whole-stage budget). CTX-38 stage-exit
thresholds are provisional-tagged defaults with provenance for the run-start log.

Phase 41 (CTRL-01 / CTX-50) extends ``RunConfig`` with precision/device/
strict_cpu_determinism/run_name plus ⚖ provisional checkpoint-cadence and
guard-threshold nested configs. Pair validity for (precision, device) is
delegated to ``resolve_runtime`` (CTX-20 sole authority) — this module only
rejects wrong types / empty strings. YAML parsing lives in ``config_yaml.py``.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Sequence


class ConfigRequiredError(ValueError):
    """Raised when a CTX-39 config-required field is unset."""

    def __init__(self, field_name: str, provenance: str = "") -> None:
        self.field_name = field_name
        msg = f"TrainingConfig required field unset: {field_name}"
        if provenance:
            msg = f"{msg} ({provenance})"
        super().__init__(msg)


def _require_int(name: str, value: Any, provenance: str) -> int:
    if value is None:
        raise ConfigRequiredError(name, provenance)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an int (got {value!r}); {provenance}")
    if value <= 0:
        raise ValueError(f"{name} must be positive (got {value!r}); {provenance}")
    return value


def _require_float(name: str, value: Any, provenance: str) -> float:
    if value is None:
        raise ConfigRequiredError(name, provenance)
    try:
        v = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a float (got {value!r}); {provenance}") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite (got {value!r}); {provenance}")
    return v


def _finite_positive(name: str, value: float, provenance: str) -> float:
    v = float(value)
    if not math.isfinite(v) or v <= 0.0:
        raise ValueError(f"{name} must be finite and positive (got {value!r}); {provenance}")
    return v


def _finite_unit_interval(name: str, value: float, provenance: str) -> float:
    """Finite fraction in (0, 1] — mirrors adapter.py memory_watermark shape."""
    try:
        v = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a float (got {value!r}); {provenance}") from exc
    if not math.isfinite(v) or not (0.0 < v <= 1.0):
        raise ValueError(
            f"{name} must be finite and in (0, 1] (got {value!r}); {provenance}"
        )
    return v


def _require_nonempty_str(name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a str (got {value!r})")
    if not value or not value.strip():
        raise ValueError(f"{name} must be a non-empty str (got {value!r})")
    return value


def _validate_run_name(value: Optional[str]) -> Optional[str]:
    """Single safe path-component for runs/<name>/ (cycle-2 codex MEDIUM).

    Rejects empty/whitespace, path separators, ``.``/``..``, absolute paths,
    drive letters, and control characters. ``None`` means "derive at run start".
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"run_name must be a str or None (got {value!r})")
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"run_name must be a non-empty str (got {value!r})")
    if stripped in (".", ".."):
        raise ValueError(f"run_name must not be '.' or '..' (got {value!r})")
    if "/" in value or "\\" in value:
        raise ValueError(
            f"run_name must not contain path separators (got {value!r})"
        )
    if value.startswith("/") or value.startswith("\\"):
        raise ValueError(f"run_name must not be an absolute path (got {value!r})")
    # Windows drive-letter absolute path (e.g. C:\... or C:/...).
    if re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"run_name must not be an absolute path (got {value!r})")
    if any(ord(ch) < 0x20 for ch in value):
        raise ValueError(
            f"run_name must not contain control characters (got {value!r})"
        )
    return value


# ⚖ PROVISIONAL defaults — mechanism ships; values are owner-ratified later
# (D4-a wall-clock at run #1; R-1 guard thresholds at Phase-43 pilot).
# Do NOT present these as ratified.
_PROVISIONAL_WALL_CLOCK_CEILING_S = 3600.0  # ⚖ provisional placeholder
_PROVISIONAL_LOSS_EXPLOSION_CEILING = 1.0e6  # ⚖ provisional placeholder
_PROVISIONAL_DISK_FLOOR_FRACTION = 0.05  # ⚖ provisional placeholder
_PROVISIONAL_MEMORY_WATERMARK_FRACTION = 0.7  # ⚖ provisional placeholder
_PROVISIONAL_EVERY_N_STEPS = 100  # cadence seam default (not owner-carved science)
_DEFAULT_ROLLING_KEEP = 3
_DEFAULT_FAILURE_KEEP = 10  # plain disk-hygiene retention bound (LOW-2)

# Sentinel for the undecided frozen-config RNG recording representation.
_FROZEN_CONFIG_RNG_RECORDING_UNDECIDED = "UNDECIDED"

# Provisional registry: (dotted_name, default_value, provenance).
_PROVISIONAL: tuple[tuple[str, Any, str], ...] = (
    ("stage.beta", 0.98, "ctl_instruction.md CURR-03 criterion 1 (CTX-38)"),
    ("stage.patience", 200, "ctl_instruction.md CURR-03 criterion 1 (CTX-38)"),
    ("stage.eps_plateau", 1e-5, "ctl_instruction.md CURR-03 criterion 1 (CTX-38)"),
    ("stage.eps_phys", 1e-4, "ctl_instruction.md CURR-03 criterion 3 / CTX-40 (CTX-38)"),
    ("stage.eps_energy", 1e-4, "ctl_instruction.md CURR-03 criterion 4 (CTX-38)"),
    ("stage.energy_floor_factor", 1e-4, "ctl_instruction.md CURR-03 ε_H=1e-4·S_H (CTX-38)"),
    ("opt.lbfgs_max_iter", 20, "CTX-47 L-BFGS max_iter open 20-50 range"),
    ("opt.lbfgs_chunk_size", 1024, "RESEARCH Open Question 2 accumulate-in-closure chunk"),
    ("opt.validation_every", 10, "CTX-49 validation_every provisional"),
    ("opt.adam_lr_base", 1e-3, "ctl_instruction.md consolidated schedule LR 1e-3·0.7^k"),
    ("opt.adam_lr_decay", 0.7, "ctl_instruction.md consolidated schedule LR 1e-3·0.7^k"),
    # ⚖ Phase-41 owner-carved seams (D4-a / R-1) — provisional, not ratified.
    (
        "run.checkpoint.wall_clock_ceiling_s",
        _PROVISIONAL_WALL_CLOCK_CEILING_S,
        "⚖ PROVISIONAL (D4-a): owner-ratify-before-run-#1 wall-clock checkpoint "
        "ceiling in seconds; mechanism ships, value is owner-carved",
    ),
    (
        "run.guards.loss_explosion_ceiling",
        _PROVISIONAL_LOSS_EXPLOSION_CEILING,
        "⚖ PROVISIONAL (R-1): owner-calibrate-at-Phase-43-pilot loss-explosion "
        "guard ceiling; mechanism ships, value is owner-carved",
    ),
    (
        "run.guards.disk_floor_fraction",
        _PROVISIONAL_DISK_FLOOR_FRACTION,
        "⚖ PROVISIONAL (R-1): owner-calibrate-at-Phase-43-pilot disk-floor "
        "fraction in (0, 1]; mechanism ships, value is owner-carved",
    ),
    (
        "run.guards.memory_watermark_fraction",
        _PROVISIONAL_MEMORY_WATERMARK_FRACTION,
        "⚖ PROVISIONAL (R-1): owner-calibrate-at-Phase-43-pilot memory-watermark "
        "fraction in (0, 1]; mechanism ships, value is owner-carved",
    ),
)


@dataclass(frozen=True)
class GuardConfig:
    """R-1 guard thresholds (run.guards) — ⚖ provisional defaults.

    Fractional thresholds are finite-in-(0, 1]; the loss-explosion ceiling is
    finite-positive. Values are owner-carved placeholders, not ratified.
    """

    loss_explosion_ceiling: float = _PROVISIONAL_LOSS_EXPLOSION_CEILING
    disk_floor_fraction: float = _PROVISIONAL_DISK_FLOOR_FRACTION
    memory_watermark_fraction: float = _PROVISIONAL_MEMORY_WATERMARK_FRACTION

    def __post_init__(self) -> None:
        prov = "⚖ PROVISIONAL R-1 guard threshold (owner-calibrate-at-Phase-43-pilot)"
        ceiling = _finite_positive(
            "loss_explosion_ceiling", self.loss_explosion_ceiling, prov
        )
        disk = _finite_unit_interval(
            "disk_floor_fraction", self.disk_floor_fraction, prov
        )
        mem = _finite_unit_interval(
            "memory_watermark_fraction", self.memory_watermark_fraction, prov
        )
        object.__setattr__(self, "loss_explosion_ceiling", ceiling)
        object.__setattr__(self, "disk_floor_fraction", disk)
        object.__setattr__(self, "memory_watermark_fraction", mem)


@dataclass(frozen=True)
class CheckpointCadence:
    """Checkpoint dual-trigger cadence + retention (run.checkpoint).

    ``every_n_steps`` / ``rolling_keep`` / ``failure_keep`` are operational
    hygiene bounds. ``wall_clock_ceiling_s`` is the ⚖ D4-a provisional seam.
    ``failure_keep`` is a plain disk-hygiene retention bound on the
    ``failure-*`` anchor class (LOW-2) — NOT an owner-carved scientific value.
    """

    every_n_steps: int = _PROVISIONAL_EVERY_N_STEPS
    wall_clock_ceiling_s: float = _PROVISIONAL_WALL_CLOCK_CEILING_S  # ⚖ provisional
    rolling_keep: int = _DEFAULT_ROLLING_KEEP
    failure_keep: int = _DEFAULT_FAILURE_KEEP

    def __post_init__(self) -> None:
        every = _require_int(
            "every_n_steps", self.every_n_steps, "checkpoint cadence"
        )
        ceiling = _finite_positive(
            "wall_clock_ceiling_s",
            self.wall_clock_ceiling_s,
            "⚖ PROVISIONAL D4-a wall-clock ceiling (owner-ratify-before-run-#1)",
        )
        rolling = _require_int(
            "rolling_keep", self.rolling_keep, "checkpoint retention"
        )
        failure = _require_int(
            "failure_keep", self.failure_keep, "failure-* retention (disk hygiene)"
        )
        object.__setattr__(self, "every_n_steps", every)
        object.__setattr__(self, "wall_clock_ceiling_s", ceiling)
        object.__setattr__(self, "rolling_keep", rolling)
        object.__setattr__(self, "failure_keep", failure)


@dataclass(frozen=True)
class RunConfig:
    """Run-level knobs: seed, logging, precision/device, ⚖ guards + cadence.

    ``precision`` / ``device`` are type-validated only; pair validity is
    ``resolve_runtime``'s job (CTX-20). ``strict_cpu_determinism`` defaults OFF
    (CTX-63). ``run_name`` is an optional filesystem path segment for
    ``runs/<name>/`` (consumed by 41-05); when None a timestamp+seed slug is
    derived at run start.
    """

    seed: int = 0
    log_every: int = 1
    precision: str = "float32"  # D1-p production default
    device: str = "mps"  # D1-p production default
    strict_cpu_determinism: bool = False  # CTX-63 default OFF
    run_name: Optional[str] = None
    guards: GuardConfig = field(default_factory=GuardConfig)
    checkpoint: CheckpointCadence = field(default_factory=CheckpointCadence)

    def __post_init__(self) -> None:
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError(f"run.seed must be an int (got {self.seed!r})")
        if not isinstance(self.log_every, int) or self.log_every < 1:
            raise ValueError(
                f"run.log_every must be a positive int (got {self.log_every!r})"
            )
        _require_nonempty_str("precision", self.precision)
        _require_nonempty_str("device", self.device)
        if not isinstance(self.strict_cpu_determinism, bool):
            raise ValueError(
                f"strict_cpu_determinism must be a bool "
                f"(got {self.strict_cpu_determinism!r})"
            )
        object.__setattr__(self, "run_name", _validate_run_name(self.run_name))
        if not isinstance(self.guards, GuardConfig):
            raise TypeError(
                f"run.guards must be GuardConfig (got {type(self.guards)!r})"
            )
        if not isinstance(self.checkpoint, CheckpointCadence):
            raise TypeError(
                f"run.checkpoint must be CheckpointCadence "
                f"(got {type(self.checkpoint)!r})"
            )


@dataclass(frozen=True)
class StageConfig:
    """Per-stage budget + stage-exit thresholds (CTX-39 required + CTX-38 defaults)."""

    # CTX-39 required — no defaults.
    max_epochs: Optional[int] = None
    n_adam: Optional[int] = None  # T_max = N_Adam,k
    stagnation_window: Optional[int] = None
    # WR-03 / reserved seam (do NOT wire into automatic ADVANCE/HALT paths):
    # percentile_10_relaxation parameterizes the *owner-authorized degraded-
    # advancement* relaxation at ctl_instruction.md:1987-1997. That path is an
    # explicit MANUAL owner decision logged in the gap register with its
    # justification — "No automatic degraded advancement is authorized"
    # (ctl_instruction.md:1991-1992; 40-SPEC R6). The field is therefore
    # config-required (CTX-39) and range-validated to [0, 1] but has NO automatic
    # consumer by design. Claimed-unverified (D5-05; CLM-08/09); provisional
    # pending Phase-43 / ACC-05 Stage-0 pilot calibration (SCOPE-14). Minting a
    # HALT trigger from this field is forbidden (GAP-40-02 → A: HALT has exactly
    # two triggers — max-epoch without the gate, and validation stagnation).
    percentile_10_relaxation: Optional[float] = None

    # CTX-38 provisional stage-exit thresholds.
    beta: float = 0.98
    patience: int = 200
    eps_plateau: float = 1e-5
    eps_phys: float = 1e-4
    eps_energy: float = 1e-4
    energy_floor_factor: float = 1e-4

    def __post_init__(self) -> None:
        prov = "CTX-39 config-required / ctl_instruction.md stage-exit"
        me = _require_int("max_epochs", self.max_epochs, prov)
        na = _require_int("n_adam", self.n_adam, prov)
        sw = _require_int("stagnation_window", self.stagnation_window, prov)
        p10 = _require_float(
            "percentile_10_relaxation", self.percentile_10_relaxation, prov
        )
        if p10 < 0.0 or p10 > 1.0:
            raise ValueError(
                f"percentile_10_relaxation must be in [0, 1] (got {p10!r}); {prov}"
            )
        # GAP-40-02 → A: whole-stage MAX_EPOCHS bounds Adam budget.
        if na > me:
            raise ValueError(
                f"n_adam ({na}) must be <= max_epochs ({me}); "
                "GAP-40-02 → A / CTX-39 whole-stage budget"
            )
        for name, val in (
            ("beta", self.beta),
            ("eps_plateau", self.eps_plateau),
            ("eps_phys", self.eps_phys),
            ("eps_energy", self.eps_energy),
            ("energy_floor_factor", self.energy_floor_factor),
        ):
            _finite_positive(name, val, "CTX-38 provisional threshold")
        if not (0.0 < float(self.beta) < 1.0):
            raise ValueError(f"beta must be in (0, 1) (got {self.beta!r}); CTX-38")
        if not isinstance(self.patience, int) or self.patience < 1:
            raise ValueError(
                f"patience must be a positive int (got {self.patience!r}); CTX-38"
            )
        # Re-bind validated ints through object.__setattr__ (frozen).
        object.__setattr__(self, "max_epochs", me)
        object.__setattr__(self, "n_adam", na)
        object.__setattr__(self, "stagnation_window", sw)
        object.__setattr__(self, "percentile_10_relaxation", p10)


@dataclass(frozen=True)
class OptConfig:
    """Optimizer schedule (Adam + L-BFGS knobs)."""

    adam_betas: tuple[float, float] = (0.9, 0.999)
    adam_eps: float = 1e-8
    adam_lr_base: float = 1e-3
    adam_lr_decay: float = 0.7
    lbfgs_history_size: int = 10
    lbfgs_max_iter: int = 20  # CTX-47 provisional
    lbfgs_line_search: str = "strong_wolfe"
    validation_every: int = 10  # CTX-49
    lbfgs_chunk_size: int = 1024  # RESEARCH OQ2 provisional

    def __post_init__(self) -> None:
        if (
            not isinstance(self.adam_betas, tuple)
            or len(self.adam_betas) != 2
            or any(not math.isfinite(float(b)) for b in self.adam_betas)
        ):
            raise ValueError(
                f"opt.adam_betas must be a length-2 finite tuple (got {self.adam_betas!r})"
            )
        for name, val in (
            ("adam_eps", self.adam_eps),
            ("adam_lr_base", self.adam_lr_base),
            ("adam_lr_decay", self.adam_lr_decay),
        ):
            _finite_positive(name, val, "CTX-48 Adam schedule")
        for name, val in (
            ("lbfgs_history_size", self.lbfgs_history_size),
            ("lbfgs_max_iter", self.lbfgs_max_iter),
            ("validation_every", self.validation_every),
            ("lbfgs_chunk_size", self.lbfgs_chunk_size),
        ):
            if not isinstance(val, int) or isinstance(val, bool) or val < 1:
                raise ValueError(f"opt.{name} must be a positive int (got {val!r})")
        if self.lbfgs_line_search != "strong_wolfe":
            raise ValueError(
                f"opt.lbfgs_line_search must be 'strong_wolfe' "
                f"(got {self.lbfgs_line_search!r}); CTX-47"
            )

    def lr_for_stage(self, k: int) -> float:
        """LR_k = adam_lr_base · adam_lr_decay^k."""
        return float(self.adam_lr_base) * (float(self.adam_lr_decay) ** int(k))


@dataclass(frozen=True)
class LossConfig:
    """Loss-side caps. Enforces λ_E^max ≤ 1 (PHYS-05)."""

    lambda_e_max: float = 1.0

    def __post_init__(self) -> None:
        v = float(self.lambda_e_max)
        if not math.isfinite(v):
            raise ValueError(f"lambda_e_max must be finite (got {self.lambda_e_max!r})")
        if v > 1.0:
            raise ValueError(
                f"lambda_e_max must be <= 1 (got {v!r}); PHYS-05 / pinn_architecture.md"
            )
        if v < 0.0:
            raise ValueError(f"lambda_e_max must be non-negative (got {v!r})")
        object.__setattr__(self, "lambda_e_max", v)


@dataclass(frozen=True)
class TrainingConfig:
    """Top-level nested config. Exposes flat gate attributes for StageExitMachine.

    ``stage`` is required (CTX-39 fields live there and have no inventable
    defaults). ``run`` / ``opt`` / ``loss`` default to empty valid sections.
    """

    stage: StageConfig
    run: RunConfig = field(default_factory=RunConfig)
    opt: OptConfig = field(default_factory=OptConfig)
    loss: LossConfig = field(default_factory=LossConfig)

    def __post_init__(self) -> None:
        if not isinstance(self.stage, StageConfig):
            raise TypeError(f"stage must be StageConfig (got {type(self.stage)!r})")
        if not isinstance(self.run, RunConfig):
            raise TypeError(f"run must be RunConfig (got {type(self.run)!r})")
        if not isinstance(self.opt, OptConfig):
            raise TypeError(f"opt must be OptConfig (got {type(self.opt)!r})")
        if not isinstance(self.loss, LossConfig):
            raise TypeError(f"loss must be LossConfig (got {type(self.loss)!r})")

    # ---- flat surface for StageExitMachine (duck-typed attribute access) ----
    @property
    def beta(self) -> float:
        return self.stage.beta

    @property
    def patience(self) -> int:
        return self.stage.patience

    @property
    def eps_plateau(self) -> float:
        return self.stage.eps_plateau

    @property
    def eps_phys(self) -> float:
        return self.stage.eps_phys

    @property
    def eps_energy(self) -> float:
        return self.stage.eps_energy

    @property
    def energy_floor(self) -> float:
        return self.stage.energy_floor_factor

    @property
    def max_epochs(self) -> int:
        return int(self.stage.max_epochs)  # type: ignore[arg-type]

    @property
    def stagnation_window(self) -> int:
        return int(self.stage.stagnation_window)  # type: ignore[arg-type]

    def provisional_fields(self) -> Sequence[Mapping[str, Any]]:
        """Enumerate provisional-tagged fields with provenance for run-start log.

        Includes Phase-40 CTX-38/47/49 thresholds plus Phase-41 ⚖ seams
        (D4-a wall-clock ceiling, R-1 guard thresholds) and the
        ``frozen_config_rng_recording_format`` undecided representation.
        """
        lookup = {
            "stage.beta": self.stage.beta,
            "stage.patience": self.stage.patience,
            "stage.eps_plateau": self.stage.eps_plateau,
            "stage.eps_phys": self.stage.eps_phys,
            "stage.eps_energy": self.stage.eps_energy,
            "stage.energy_floor_factor": self.stage.energy_floor_factor,
            "opt.lbfgs_max_iter": self.opt.lbfgs_max_iter,
            "opt.lbfgs_chunk_size": self.opt.lbfgs_chunk_size,
            "opt.validation_every": self.opt.validation_every,
            "opt.adam_lr_base": self.opt.adam_lr_base,
            "opt.adam_lr_decay": self.opt.adam_lr_decay,
            "run.checkpoint.wall_clock_ceiling_s": (
                self.run.checkpoint.wall_clock_ceiling_s
            ),
            "run.guards.loss_explosion_ceiling": (
                self.run.guards.loss_explosion_ceiling
            ),
            "run.guards.disk_floor_fraction": self.run.guards.disk_floor_fraction,
            "run.guards.memory_watermark_fraction": (
                self.run.guards.memory_watermark_fraction
            ),
        }
        out = []
        for name, _default, provenance in _PROVISIONAL:
            out.append(
                {
                    "name": name,
                    "value": lookup[name],
                    "provisional": True,
                    "provenance": provenance,
                }
            )
        # ⚖ HIGH (cross-AI review): CTRL-08 requires config.yaml to carry all
        # four RNG streams while CTRL-01/CTX-51 requires the frozen file to
        # re-parse to an EQUAL TrainingConfig. The CONSTRAINT is pinned; the
        # SERIALIZATION REPRESENTATION is owner-carved and NOT silently chosen.
        out.append(
            {
                "name": "frozen_config_rng_recording_format",
                "value": _FROZEN_CONFIG_RNG_RECORDING_UNDECIDED,
                "provisional": True,
                "provenance": (
                    "⚖ PROVISIONAL (owner-carved representation): CONSTRAINT pinned "
                    "— runs/<name>/config.yaml MUST carry all four RNG streams "
                    "(CTRL-08/CTX-62) WHILE preserving TrainingConfig re-parse "
                    "equality (CTRL-01/CTX-51). Representation candidates: "
                    "(A) sidecar metadata envelope inside config.yaml under an "
                    "ignored top-level key (e.g. _runtime_state) holding the four "
                    "streams — load_config skips it; OR (B) config.yaml stays a pure "
                    "TrainingConfig and the four streams are recorded in a sibling "
                    "artifact runs/<name>/run_start_rng.pt PLUS every checkpoint. "
                    "Value=UNDECIDED until owner pick; do not implement either as "
                    "ratified."
                ),
            }
        )
        return tuple(out)

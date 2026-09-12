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

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence


# Phase 57 amended-recipe constants (SPEC-01/SPEC-06; 57-RULING.md).  The
# fields below are optional so pre-Phase-57 callers retain their established
# small synthetic/test draws; ``pinn.train`` requires the exact values when a
# config opts into the amended path.
RATIFIED_COLLOCATION_COUNT = 4096
R_REF_ARTIFACT_SCHEMA_VERSION = "phase56-r-ref-stage0/v1"
R_REF_ARTIFACT_RELATIVE_PATH = "pinn/verification/artifacts/r_ref_stage0.json"


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


def _validate_front_advance_window_n(value: Optional[int]) -> Optional[int]:
    """Validate the owner-owned invariant-B window when it is supplied.

    ``None`` is intentional: it keeps invariant B in D-20 record-only mode
    until the owner chooses an enforcement window.  Unlike the CTX-39
    required-int helper, this validator must preserve that unset state.
    """
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(
            "front_advance_window_n must be a positive int or None "
            f"(got {value!r})"
        )
    if value <= 0:
        raise ValueError(
            "front_advance_window_n must be a positive int or None "
            f"(got {value!r})"
        )
    return value


def _validate_optional_positive_int(name: str, value: Optional[int]) -> Optional[int]:
    """Validate an optional positive integer without inventing a default."""
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive int or None (got {value!r})")
    return int(value)


def _validate_optional_path(name: str, value: Optional[str]) -> Optional[str]:
    """Validate an optional non-empty path carried by a frozen config."""
    if value is None:
        return None
    return _require_nonempty_str(name, value)


def load_frozen_r_ref_artifact(path: str | Path) -> float:
    """Load and validate one governed Phase-56 ``R_ref`` artifact.

    The amended run path is allowed to consume only a provenance-complete
    artifact: schema/version, valid marker, six 16-entry raw-bin rows, the
    ratified 16×256 configuration, and non-empty source provenance are all
    checked before the finite-positive reference is returned.  This function
    performs one read and never recomputes or writes the artifact.
    """
    artifact_path = Path(path)
    try:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"R_ref artifact does not exist: {artifact_path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"R_ref artifact is unreadable JSON: {artifact_path}") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("R_ref artifact payload must be a JSON object")
    required = {
        "schema_version",
        "valid",
        "r_ref",
        "raw_bin_means",
        "configuration",
        "provenance",
        "statistic",
        "statistic_convention",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"R_ref artifact missing required keys: {missing}")
    if payload["schema_version"] != R_REF_ARTIFACT_SCHEMA_VERSION:
        raise ValueError(
            "R_ref artifact schema_version must be "
            f"{R_REF_ARTIFACT_SCHEMA_VERSION!r}; got {payload['schema_version']!r}"
        )
    if payload["valid"] is not True:
        raise ValueError("R_ref artifact valid marker is not true")
    if payload["statistic"] != "median" or not isinstance(
        payload["statistic_convention"], str
    ) or not payload["statistic_convention"].strip():
        raise ValueError("R_ref artifact median provenance is missing or invalid")

    configuration = payload["configuration"]
    if not isinstance(configuration, Mapping):
        raise ValueError("R_ref artifact configuration must be a JSON object")
    expected_config = {"n_bins": 16, "per_bin": 256, "total_points": 4096}
    for name, expected in expected_config.items():
        if configuration.get(name) != expected:
            raise ValueError(
                f"R_ref artifact configuration.{name} must be {expected}; "
                f"got {configuration.get(name)!r}"
            )

    provenance = payload["provenance"]
    if not isinstance(provenance, Mapping):
        raise ValueError("R_ref artifact provenance must be a JSON object")
    for name in ("git_sha", "timestamp"):
        value = provenance.get(name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"R_ref artifact provenance.{name} must be a non-empty string"
            )

    raw_rows = payload["raw_bin_means"]
    if not isinstance(raw_rows, (list, tuple)) or len(raw_rows) != 6:
        raise ValueError(
            "R_ref artifact raw_bin_means must contain exactly six case rows"
        )
    values: list[float] = []
    for row_index, row in enumerate(raw_rows):
        if not isinstance(row, (list, tuple)) or len(row) != 16:
            raise ValueError(
                "R_ref artifact raw_bin_means[{}] must contain exactly 16 "
                "bin means".format(row_index)
            )
        for value in row:
            if isinstance(value, bool):
                raise ValueError("R_ref artifact raw bin means must be numeric")
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "R_ref artifact raw bin means must be numeric"
                ) from exc
            if not math.isfinite(number) or number < 0.0:
                raise ValueError(
                    "R_ref artifact raw bin means must be finite and non-negative"
                )
            values.append(number)

    raw_r_ref = payload["r_ref"]
    if isinstance(raw_r_ref, bool):
        raise ValueError("R_ref artifact r_ref must be numeric")
    try:
        r_ref = float(raw_r_ref)
    except (TypeError, ValueError) as exc:
        raise ValueError("R_ref artifact r_ref must be numeric") from exc
    if not math.isfinite(r_ref) or r_ref <= 0.0:
        raise ValueError(
            f"R_ref artifact r_ref must be finite and positive; got {raw_r_ref!r}"
        )
    ordered = sorted(values)
    midpoint = (ordered[47] + ordered[48]) / 2.0
    if midpoint != r_ref:
        raise ValueError(
            "R_ref artifact r_ref does not equal the recorded six-case median; "
            f"got {r_ref!r}, expected {midpoint!r}"
        )
    return r_ref


# ⚖ PROVISIONAL defaults — mechanism ships; values are owner-ratified later
# (D4-a wall-clock at run #1; R-1 guard thresholds at Phase-43 pilot).
# Do NOT present these as ratified — EXCEPT loss_explosion_ceiling below,
# which R-1 has now ratified.
_PROVISIONAL_WALL_CLOCK_CEILING_S = 3600.0  # ⚖ provisional placeholder

# R-1 loss_explosion_ceiling: OWNER-RATIFIED via delegation 2026-07-21
# ("follow your best judgement"). Value 1e11, calibrated from the 43-06
# diagnostic run's observed peak total loss ~4e9 (single seed, MPS/fp32) —
# roughly 25x headroom above that peak. Explicitly REVISABLE at the ACC-05
# Stage-0 pilot. The constant name and the ``_PROVISIONAL`` registry entry
# below are kept as-is (not renamed / not removed from the registry): R-1 as
# a whole covers three GuardConfig thresholds reported together under one
# owner-carved seam, and disk_floor_fraction / memory_watermark_fraction
# remain uncalibrated placeholders — see the provisional-flag ambiguity note
# in .planning/phases/43-verification-stage-0-pilot-acceptance/evidence/
# smoke/README.md.
_PROVISIONAL_LOSS_EXPLOSION_CEILING = 1.0e11
_PROVISIONAL_DISK_FLOOR_FRACTION = 0.05  # ⚖ provisional placeholder
_PROVISIONAL_MEMORY_WATERMARK_FRACTION = 0.7  # ⚖ provisional placeholder
_PROVISIONAL_EVERY_N_STEPS = 100  # cadence seam default (not owner-carved science)
_DEFAULT_ROLLING_KEEP = 3
_DEFAULT_FAILURE_KEEP = 10  # plain disk-hygiene retention bound (LOW-2)

# DATA-01 composition seam (43-03): the two supported training-data sources.
# ``synthetic`` is the dataset-free falsifiability-floor stub; ``admitted`` is
# the sole production ``AdmittedSetAdapter`` corpus path.
_DATA_SOURCES = ("synthetic", "admitted")

# frozen_config_rng_recording_format — GAP-41-01 RESOLVED-WITH-INSTRUCTION
# (2026-07-18, owner delegated best-judgment pick): representation B. The
# frozen runs/<name>/config.yaml stays a pure TrainingConfig; the four RNG
# streams are recorded at run start in the sibling artifact
# runs/<name>/run_start_rng.pt (determinism.record_run_start_rng) PLUS every
# checkpoint. See .planning/phases/41-*/41-GAPS.md for the full record.
FROZEN_CONFIG_RNG_RECORDING_FORMAT = "sibling-artifact:run_start_rng.pt"

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
    (
        "opt.adam_microbatch_size", 256,
        "57-07 band-generation-2 scope brief §1.2: memory-bounded Adam-phase "
        "physics microbatch; hardware-dependent, provably result-invariant "
        "once the equivalence test passes (no ratified recipe value moves)",
    ),
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
        "⚖ R-1: OWNER-RATIFIED via delegation 2026-07-21 at value 1e11 "
        "(calibrated from the 43-06 diagnostic peak ~4e9, MPS/fp32, ~25x "
        "headroom); explicitly revisable at the ACC-05 Stage-0 pilot. Still "
        "surfaced here (provisional=True) as part of the shared R-1 "
        "guard-threshold seam alongside disk_floor_fraction / "
        "memory_watermark_fraction, which remain owner-carved and "
        "uncalibrated — see evidence/smoke/README.md for the provisional-flag "
        "ambiguity note",
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
    (
        "run.recover_retries",
        0,
        "⚖ PROVISIONAL (R-2): existing CurriculumController retry-budget "
        "seam; owner-ratify at the Phase-43 pilot before changing the "
        "ratified baseline of zero",
    ),
)


@dataclass(frozen=True)
class GuardConfig:
    """R-1 guard thresholds (run.guards) — ⚖ provisional defaults.

    Fractional thresholds are finite-in-(0, 1]; the loss-explosion ceiling is
    finite-positive. ``disk_floor_fraction`` / ``memory_watermark_fraction``
    remain owner-carved placeholders, not ratified. ``loss_explosion_ceiling``
    is OWNER-RATIFIED (delegation 2026-07-21, value 1e11; revisable at ACC-05)
    — see ``_PROVISIONAL_LOSS_EXPLOSION_CEILING`` above.
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
class MonitorConfig:
    """Monitoring cadence knobs (run.monitor).

    ``heartbeat_secs`` / ``staleness_factor`` are the heartbeat timing
    parameters read by the status.json writer.  ``tb_histogram_every`` is the
    TB w_n-histogram thinning cadence (discretionary, CTX-70/80).  ``mem_every``
    is the periodic ``mem:`` line cadence.  All are operational (B-5) —
    changeable on resume.  Values are owner-carved, not science thresholds.
    """

    heartbeat_secs: int = 30
    staleness_factor: int = 3
    tb_histogram_every: int = 100
    mem_every: int = 100

    def __post_init__(self) -> None:
        prov = "operational monitoring cadence (B-5)"
        object.__setattr__(
            self, "heartbeat_secs",
            _require_int("heartbeat_secs", self.heartbeat_secs, prov),
        )
        object.__setattr__(
            self, "staleness_factor",
            _require_int("staleness_factor", self.staleness_factor, prov),
        )
        object.__setattr__(
            self, "tb_histogram_every",
            _require_int("tb_histogram_every", self.tb_histogram_every, prov),
        )
        object.__setattr__(
            self, "mem_every",
            _require_int("mem_every", self.mem_every, prov),
        )


@dataclass(frozen=True)
class InvariantsConfig:
    """GATE-03 invariant controls with an owner-owned optional window.

    ``front_advance_window_n`` deliberately has no default enforcement value.
    ``None`` means invariant B records its high-water state without HALTing
    (D-20) until the owner supplies a positive integer.
    """

    front_advance_window_n: Optional[int] = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "front_advance_window_n",
            _validate_front_advance_window_n(self.front_advance_window_n),
        )


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
    smoke: bool = False  # 43-03 ACC-02: mark a ~5-min Stage-0 smoke run
    recover_retries: int = 0  # R-2 controller baseline; owner-ratified later
    run_name: Optional[str] = None
    guards: GuardConfig = field(default_factory=GuardConfig)
    invariants: InvariantsConfig = field(default_factory=InvariantsConfig)
    checkpoint: CheckpointCadence = field(default_factory=CheckpointCadence)
    monitor: MonitorConfig = field(default_factory=MonitorConfig)

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
        if not isinstance(self.smoke, bool):
            raise ValueError(f"run.smoke must be a bool (got {self.smoke!r})")
        if (
            not isinstance(self.recover_retries, int)
            or isinstance(self.recover_retries, bool)
            or self.recover_retries < 0
        ):
            raise ValueError(
                "run.recover_retries must be a non-negative int "
                f"(got {self.recover_retries!r}); R-2 owner-ratified seam"
            )
        object.__setattr__(self, "run_name", _validate_run_name(self.run_name))
        if not isinstance(self.guards, GuardConfig):
            raise TypeError(
                f"run.guards must be GuardConfig (got {type(self.guards)!r})"
            )
        if not isinstance(self.invariants, InvariantsConfig):
            raise TypeError(
                "run.invariants must be InvariantsConfig "
                f"(got {type(self.invariants)!r})"
            )
        if not isinstance(self.checkpoint, CheckpointCadence):
            raise TypeError(
                f"run.checkpoint must be CheckpointCadence "
                f"(got {type(self.checkpoint)!r})"
            )
        if not isinstance(self.monitor, MonitorConfig):
            raise TypeError(
                f"run.monitor must be MonitorConfig "
                f"(got {type(self.monitor)!r})"
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

    # 43-03 ACC-02: DATA-05 replay budget override. None keeps the
    # ``select_stage_records`` default (240); a positive int (e.g. the smoke's
    # 32) narrows the per-batch replay identity count without touching the
    # adapter/data selection algorithm.
    replay_count: Optional[int] = None

    # Phase-57 amended-recipe opt-in. ``None`` preserves legacy synthetic and
    # unit-test draws; ``pinn.train`` requires the ratified 4096 value when a
    # corrected-run config supplies this field.
    collocation_count: Optional[int] = None

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
        if self.replay_count is not None:
            rc = _require_int(
                "replay_count", self.replay_count,
                "43-03 DATA-05 replay-budget override",
            )
            object.__setattr__(self, "replay_count", rc)
        object.__setattr__(
            self,
            "collocation_count",
            _validate_optional_positive_int(
                "collocation_count", self.collocation_count
            ),
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
    adam_microbatch_size: int = 256  # 57-07 band-generation-2 scope brief §1.2

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
            ("adam_microbatch_size", self.adam_microbatch_size),
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
    """Loss-side caps and optional Phase-57 frozen-reference binding."""

    lambda_e_max: float = 0.0
    r_ref_artifact_path: Optional[str] = None

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
        object.__setattr__(
            self,
            "r_ref_artifact_path",
            _validate_optional_path(
                "loss.r_ref_artifact_path", self.r_ref_artifact_path
            ),
        )


@dataclass(frozen=True)
class DataConfig:
    """Training-data source selector (43-03 DATA-01 composition seam).

    ``source`` chooses between the sole production ``AdmittedSetAdapter`` corpus
    (``"admitted"``) and the dataset-free synthetic Stage-0 stub
    (``"synthetic"`` — the v2.0 falsifiability-floor default). ``root`` is an
    optional explicit corpus ``Data/`` directory; when ``None`` the admitted
    path resolves the root via ``default_data_root()`` / ``GSD_DATA_ROOT``
    (CTX-79). ``blacklist_path`` (DI-43-06-01) is an optional override for the
    admission blacklist file; when ``None`` the adapter's own default
    (``<data_root>/problematic_ics_blacklist.json``) applies. A relative
    ``blacklist_path`` resolves against the RESOLVED admitted data root (never
    the CWD), so a portable relative path may be committed to a shared config;
    an absolute path is used as-is. Only type/enum validation lives here —
    reachability of a real root, or of the blacklist file, is a run-time
    preflight/construction concern (``pinn.train`` / ``AdmittedSetAdapter``),
    not a config-load concern.
    """

    source: str = "synthetic"
    root: Optional[str] = None
    blacklist_path: Optional[str] = None

    def __post_init__(self) -> None:
        if self.source not in _DATA_SOURCES:
            raise ValueError(
                f"data.source must be one of {_DATA_SOURCES} (got {self.source!r})"
            )
        if self.root is not None:
            _require_nonempty_str("data.root", self.root)
        if self.blacklist_path is not None:
            _require_nonempty_str("data.blacklist_path", self.blacklist_path)


@dataclass(frozen=True)
class TrainingConfig:
    """Top-level nested config. Exposes flat gate attributes for StageExitMachine.

    ``stage`` is required (CTX-39 fields live there and have no inventable
    defaults). ``run`` / ``opt`` / ``loss`` / ``data`` default to empty valid
    sections (``data`` defaults to the synthetic source — 43-03).
    """

    stage: StageConfig
    run: RunConfig = field(default_factory=RunConfig)
    opt: OptConfig = field(default_factory=OptConfig)
    loss: LossConfig = field(default_factory=LossConfig)
    data: DataConfig = field(default_factory=DataConfig)

    def __post_init__(self) -> None:
        if not isinstance(self.stage, StageConfig):
            raise TypeError(f"stage must be StageConfig (got {type(self.stage)!r})")
        if not isinstance(self.run, RunConfig):
            raise TypeError(f"run must be RunConfig (got {type(self.run)!r})")
        if not isinstance(self.opt, OptConfig):
            raise TypeError(f"opt must be OptConfig (got {type(self.opt)!r})")
        if not isinstance(self.loss, LossConfig):
            raise TypeError(f"loss must be LossConfig (got {type(self.loss)!r})")
        if not isinstance(self.data, DataConfig):
            raise TypeError(f"data must be DataConfig (got {type(self.data)!r})")

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
        (D4-a wall-clock ceiling, R-1 guard thresholds). The former
        ``frozen_config_rng_recording_format`` seam is DECIDED (GAP-41-01,
        representation B — see ``FROZEN_CONFIG_RNG_RECORDING_FORMAT``) and no
        longer appears in this owner-attention listing.
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
            "opt.adam_microbatch_size": self.opt.adam_microbatch_size,
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
            "run.recover_retries": self.run.recover_retries,
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
        # ⚖ B-5 / CTX-57 resume field classification (41-05). Constraint pinned;
        # exact field-location mapping for DEFERRED categories is owner-carved.
        try:
            from pinn.training.resume import (
                resume_field_classification_provisional_entry,
            )

            out.append(resume_field_classification_provisional_entry())
        except ImportError:
            out.append(
                {
                    "name": "resume_field_classification_registry",
                    "value": "PROVISIONAL",
                    "provisional": True,
                    "provenance": (
                        "⚖ PROVISIONAL (B-5 / CTX-57): resume field classification "
                        "registry; owner-ratify before run #1"
                    ),
                }
            )
        # ⚖ B-2 / OPS-03 step-log field registry (42-02).
        try:
            from pinn.training.step_log import (
                step_log_fields_provisional_entry,
            )

            out.append(step_log_fields_provisional_entry())
        except ImportError:
            out.append(
                {
                    "name": "step_log_fields_registry",
                    "value": "PROVISIONAL",
                    "provisional": True,
                    "provenance": (
                        "⚖ PROVISIONAL (B-2 / OPS-03): step-log field registry; "
                        "owner-ratify before run #1"
                    ),
                }
            )
        return tuple(out)

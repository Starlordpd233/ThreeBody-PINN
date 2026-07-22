"""CTRL-01 keyed YAML resolver + atomic frozen-config writer (Phase 41).

Maps a single keyed YAML (top-level sections ``run`` / ``stage`` / ``opt`` /
``loss``) field-for-field onto the frozen TrainingConfig dataclasses. Unknown
keys fail loud with ``ConfigKeyError`` naming the dotted path (recursively for
nested ``run.guards.*`` / ``run.checkpoint.*``). The fully-resolved config is
written verbatim to ``runs/<name>/config.yaml`` via ``atomic_io.atomic_write_text``
so re-parse yields an EQUAL TrainingConfig (CTX-51).

Phase 43 exposes the existing ``CurriculumController.recover_retries`` seam as
the validated scalar ``run.recover_retries``; generic dataclass mapping keeps
its YAML read/freeze/round-trip path identical to other run-level fields.

Threat T-41-01: ``yaml.safe_load`` / ``yaml.safe_dump`` exclusively — never
``yaml.load``.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Mapping, Optional, Type, TypeVar, Union

import yaml

from pinn.training.atomic_io import atomic_write_text
from pinn.training.config import (
    CheckpointCadence,
    DataConfig,
    GuardConfig,
    LossConfig,
    MonitorConfig,
    OptConfig,
    RunConfig,
    StageConfig,
    TrainingConfig,
)

PathLike = Union[str, Path]

T = TypeVar("T")

_SECTION_CLASSES: Mapping[str, Type[Any]] = {
    "run": RunConfig,
    "stage": StageConfig,
    "opt": OptConfig,
    "loss": LossConfig,
    "data": DataConfig,
}

# ``data`` is intentionally NOT required: pre-43-03 configs omit it and default
# to the synthetic source. Unknown ``data.*`` keys still fail loud because the
# section is registered in ``_SECTION_CLASSES`` above.
_REQUIRED_SECTIONS = ("run", "stage", "opt", "loss")


class ConfigKeyError(ValueError):
    """Raised when a YAML key is unknown (sibling of ConfigRequiredError).

    Distinct from ``ConfigRequiredError`` (which is for MISSING required
    fields). Carries the dotted path of the first offending key.
    """

    def __init__(self, dotted_path: str, message: Optional[str] = None) -> None:
        self.dotted_path = dotted_path
        msg = message or f"unknown config key: {dotted_path}"
        super().__init__(msg)


class ConfigLoadError(ValueError):
    """Raised for missing/empty/malformed config files (fail-closed)."""

    def __init__(self, path: PathLike, reason: str) -> None:
        self.path = str(path)
        super().__init__(f"config load failed for {path}: {reason}")


def _is_frozen_dataclass(cls: Any) -> bool:
    return dataclasses.is_dataclass(cls) and isinstance(cls, type)


def _field_types(cls: Type[Any]) -> dict[str, Any]:
    return {f.name: f.type for f in dataclasses.fields(cls)}


def _resolve_nested_cls(annotation: Any) -> Optional[Type[Any]]:
    """Return a nested frozen-dataclass type from a field annotation, if any.

    Handles plain types and ``Optional[Nested]`` / ``Union[Nested, None]``
    forms that appear on RunConfig fields.
    """
    if _is_frozen_dataclass(annotation):
        return annotation
    # typing.Optional / Union — inspect __args__ when present.
    args = getattr(annotation, "__args__", None)
    if args:
        candidates = [a for a in args if a is not type(None)]  # noqa: E721
        for cand in candidates:
            if _is_frozen_dataclass(cand):
                return cand
    # String annotations (from __future__ annotations) — resolve known nests.
    if isinstance(annotation, str):
        known = {
            "GuardConfig": GuardConfig,
            "CheckpointCadence": CheckpointCadence,
            "MonitorConfig": MonitorConfig,
            "RunConfig": RunConfig,
            "StageConfig": StageConfig,
            "OptConfig": OptConfig,
            "LossConfig": LossConfig,
        }
        # Strip Optional[...] wrappers loosely.
        name = annotation
        if name.startswith("Optional[") and name.endswith("]"):
            name = name[len("Optional[") : -1]
        return known.get(name)
    return None


def _coerce_field_value(name: str, annotation: Any, value: Any) -> Any:
    """Coerce YAML values to the types the frozen dataclasses expect.

    Critical: PyYAML turns YAML sequences into lists, but ``OptConfig.adam_betas``
    requires a ``tuple`` — coerce before construction so re-parse equality holds.
    Nested dicts that map to frozen dataclasses are handed to ``_map_section``.
    """
    nested_cls = _resolve_nested_cls(annotation)
    if nested_cls is not None and isinstance(value, Mapping):
        return _map_section(name, nested_cls, dict(value))

    # Tuple-typed fields: coerce list → tuple (Common Pitfall 1).
    origin = getattr(annotation, "__origin__", None)
    if origin is tuple or annotation is tuple:
        if isinstance(value, list):
            return tuple(value)
        return value
    if isinstance(annotation, str) and (
        annotation.startswith("tuple") or annotation.startswith("Tuple")
    ):
        if isinstance(value, list):
            return tuple(value)
    return value


def _map_section(
    path_prefix: str,
    cls: Type[T],
    raw: Optional[Mapping[str, Any]],
) -> T:
    """Diff raw keys against ``dataclasses.fields(cls)``; construct ``cls``.

    Unknown keys raise ``ConfigKeyError`` naming the full dotted path. Nested
    frozen-dataclass fields recurse so ``run.guards.disk_floor_typo`` is never
    silently dropped.
    """
    if raw is None:
        raw = {}
    if not isinstance(raw, Mapping):
        raise ConfigLoadError(
            path_prefix, f"section must be a mapping (got {type(raw)!r})"
        )

    known = {f.name: f for f in dataclasses.fields(cls)}
    unknown = [k for k in raw.keys() if k not in known]
    if unknown:
        first = sorted(unknown)[0]
        dotted = f"{path_prefix}.{first}" if path_prefix else str(first)
        raise ConfigKeyError(dotted, f"unknown config key: {dotted}")

    kwargs: dict[str, Any] = {}
    for name, f in known.items():
        if name not in raw:
            continue
        value = raw[name]
        nested_cls = _resolve_nested_cls(f.type)
        if nested_cls is not None and isinstance(value, Mapping):
            # Recurse BEFORE construction so unknown nested keys raise with
            # the full dotted path (never silently dropped via **kwargs).
            child_prefix = f"{path_prefix}.{name}" if path_prefix else name
            kwargs[name] = _map_section(child_prefix, nested_cls, dict(value))
        else:
            kwargs[name] = _coerce_field_value(name, f.type, value)
    return cls(**kwargs)  # type: ignore[call-arg]


def load_config(path: PathLike) -> TrainingConfig:
    """Load a keyed YAML config into a frozen ``TrainingConfig``.

    Fail-closed:
      * missing file → ``ConfigLoadError`` naming the path
      * empty / None parse → ``ConfigLoadError`` naming the path
      * missing required section → ``ConfigLoadError`` naming the section
      * unknown key at any depth → ``ConfigKeyError`` naming the dotted path
    """
    cfg_path = Path(path)
    if not cfg_path.is_file():
        raise ConfigLoadError(cfg_path, "file does not exist")

    text = cfg_path.read_text(encoding="utf-8")
    # T-41-01: safe_load exclusively (never yaml.load).
    parsed = yaml.safe_load(text)
    if parsed is None:
        raise ConfigLoadError(cfg_path, "empty or None-parsed config file")
    if not isinstance(parsed, Mapping):
        raise ConfigLoadError(
            cfg_path, f"top-level must be a mapping (got {type(parsed)!r})"
        )

    # Reject unknown top-level keys (only run/stage/opt/loss are legal).
    unknown_top = [k for k in parsed.keys() if k not in _SECTION_CLASSES]
    if unknown_top:
        first = sorted(unknown_top)[0]
        raise ConfigKeyError(str(first), f"unknown config key: {first}")

    for section in _REQUIRED_SECTIONS:
        if section not in parsed:
            raise ConfigLoadError(cfg_path, f"missing required section: {section}")

    sections: dict[str, Any] = {}
    for name, cls in _SECTION_CLASSES.items():
        raw_section = parsed.get(name)
        if raw_section is None:
            raw_section = {}
        if not isinstance(raw_section, Mapping):
            raise ConfigLoadError(
                cfg_path,
                f"section {name!r} must be a mapping (got {type(raw_section)!r})",
            )
        sections[name] = _map_section(name, cls, dict(raw_section))

    return TrainingConfig(
        stage=sections["stage"],
        run=sections["run"],
        opt=sections["opt"],
        loss=sections["loss"],
        data=sections["data"],
    )


def resolved_config_to_dict(config: TrainingConfig) -> dict[str, Any]:
    """Fully-resolved plain dict (defaults merged, all seams filled).

    Nested frozen dataclasses become nested dicts; tuples become lists so
    ``yaml.safe_dump`` round-trips cleanly (``load_config`` re-coerces lists
    back to tuples for tuple-typed fields).
    """
    if not isinstance(config, TrainingConfig):
        raise TypeError(
            f"resolved_config_to_dict expects TrainingConfig "
            f"(got {type(config)!r})"
        )

    def _to_plain(obj: Any) -> Any:
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            out: dict[str, Any] = {}
            for f in dataclasses.fields(obj):
                out[f.name] = _to_plain(getattr(obj, f.name))
            return out
        if isinstance(obj, tuple):
            return list(obj)
        if isinstance(obj, list):
            return [_to_plain(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _to_plain(v) for k, v in obj.items()}
        return obj

    return {
        "run": _to_plain(config.run),
        "stage": _to_plain(config.stage),
        "opt": _to_plain(config.opt),
        "loss": _to_plain(config.loss),
        "data": _to_plain(config.data),
    }


def freeze_resolved_config(config: TrainingConfig, run_dir: PathLike) -> Path:
    """Write the fully-resolved config to ``<run_dir>/config.yaml`` atomically.

    Returns the path of the frozen artifact. Re-parsing via ``load_config``
    yields a ``TrainingConfig`` EQUAL to ``config`` (CTRL-01 / CTX-51).

    RNG-stream carriage (CTRL-08) uses representation B of the
    ``frozen_config_rng_recording_format`` seam (GAP-41-01, ratified
    2026-07-18): this file stays a pure TrainingConfig; the four run-start
    streams are recorded beside it in ``run_start_rng.pt`` by
    ``determinism.record_run_start_rng`` — and in every checkpoint.
    """
    destination_dir = Path(run_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "config.yaml"
    plain = resolved_config_to_dict(config)
    # sort_keys for stable identity digests (41-05); allow_unicode for run names.
    text = yaml.safe_dump(plain, sort_keys=True, allow_unicode=True)
    atomic_write_text(destination, text)
    return destination

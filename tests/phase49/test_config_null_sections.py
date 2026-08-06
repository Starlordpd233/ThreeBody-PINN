"""Phase 49 / CR-01 — a present-but-null nested section is a loadable state.

The shipped configs document a record-only invariant-B state by writing an
``invariants:`` header whose body is only a comment. YAML parses that to
``None``, and the loader used to forward ``None`` straight into ``RunConfig``,
which type-checks its nested members and raised

    TypeError: run.invariants must be InvariantsConfig (got <class 'NoneType'>)

The defect is generic to nested dataclass sections, so the coverage here is too:
``run.invariants`` is the reported symptom, but the same three shapes are
asserted for the other nested sections, and the fail-closed unknown-key contract
is re-asserted so the fix cannot have widened what the loader accepts.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]

_STAGE_BODY = """\
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {}
loss: {}
"""


def _write(tmp_path: Path, run_body: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "cfg.yaml"
    path.write_text(f"run:\n{run_body}{_STAGE_BODY}", encoding="utf-8")
    return path


def _load(path: Path):
    from pinn.training.config_yaml import load_config

    return load_config(path)


# --- run.invariants: the three documented shapes ---------------------------


@pytest.mark.parametrize(
    ("label", "run_body"),
    [
        ("omitted", "  seed: 7\n"),
        ("empty-mapping", "  invariants: {}\n"),
        # The shipped comment-only form: a header with no body.
        ("comment-only-null", "  invariants:\n    # front_advance_window_n: <owner value>\n"),
        ("explicit-null", "  invariants: null\n"),
    ],
)
def test_invariants_null_shapes_load_as_record_only(tmp_path, label, run_body):
    from pinn.training.config import InvariantsConfig

    config = _load(_write(tmp_path, run_body))

    assert isinstance(config.run.invariants, InvariantsConfig), label
    assert config.run.invariants.front_advance_window_n is None, label


def test_null_section_equals_omitted_section(tmp_path):
    """The three shapes are not merely valid — they are the same config."""
    omitted = _load(_write(tmp_path / "a", "  seed: 7\n"))
    empty = _load(_write(tmp_path / "b", "  seed: 7\n  invariants: {}\n"))
    null = _load(_write(tmp_path / "c", "  seed: 7\n  invariants:\n"))

    assert omitted.run.invariants == empty.run.invariants == null.run.invariants


# --- the fix is generic, not an invariants special case --------------------


@pytest.mark.parametrize("section", ["guards", "invariants", "checkpoint", "monitor"])
def test_every_nested_run_section_accepts_explicit_null(tmp_path, section):
    """A present-but-null nested section yields that section's defaults."""
    null_cfg = _load(_write(tmp_path / section, f"  {section}:\n"))
    default_cfg = _load(_write(tmp_path / f"{section}-omitted", "  seed: 7\n"))

    assert getattr(null_cfg.run, section) == getattr(default_cfg.run, section)


@pytest.mark.parametrize("section", ["opt", "loss"])
def test_top_level_nested_sections_accept_explicit_null(tmp_path, section):
    body = _STAGE_BODY.replace(f"{section}: {{}}", f"{section}:")
    target = tmp_path / section
    target.mkdir(parents=True, exist_ok=True)
    path = target / "cfg.yaml"
    path.write_text(f"run:\n  seed: 7\n{body}", encoding="utf-8")

    null_cfg = _load(path)
    default_cfg = _load(_write(tmp_path / "omitted", "  seed: 7\n"))

    assert getattr(null_cfg, section) == getattr(default_cfg, section)


# --- the fail-closed unknown-key contract is NOT weakened ------------------


def test_unknown_key_in_populated_section_still_raises_dotted_path(tmp_path):
    from pinn.training.config_yaml import ConfigKeyError

    path = _write(tmp_path, "  invariants:\n    front_advance_window_nn: 500\n")

    with pytest.raises(ConfigKeyError) as excinfo:
        _load(path)

    assert excinfo.value.dotted_path == "run.invariants.front_advance_window_nn"


def test_null_section_does_not_swallow_a_sibling_unknown_key(tmp_path):
    from pinn.training.config_yaml import ConfigKeyError

    path = _write(tmp_path, "  invariants:\n  not_a_run_key: 1\n")

    with pytest.raises(ConfigKeyError) as excinfo:
        _load(path)

    assert excinfo.value.dotted_path == "run.not_a_run_key"


def test_scalar_nested_section_is_still_refused(tmp_path):
    """Null means defaults; a scalar body is still malformed."""
    path = _write(tmp_path, "  invariants: 500\n")

    with pytest.raises((TypeError, ValueError)):
        _load(path)


# --- both shipped configs load -------------------------------------------


def test_shipped_smoke_config_loads_record_only():
    from pinn.training.config import InvariantsConfig

    config = _load(_REPO_ROOT / "configs" / "smoke.yaml")

    assert isinstance(config.run.invariants, InvariantsConfig)
    assert config.run.invariants.front_advance_window_n is None


def test_shipped_stage0_example_config_loads_owner_ratified_window():
    config = _load(_REPO_ROOT / "configs" / "stage0-example.yaml")

    # Owner ruling 2026-08-05 (commit a08f65f1). Asserted, never adjusted.
    assert config.run.invariants.front_advance_window_n == 500

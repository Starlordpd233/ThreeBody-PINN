"""Phase 49 / GATE-03 runtime invariant coverage."""

from __future__ import annotations

import pytest


def _minimal_yaml(*, invariants: str = "invariants: {}") -> str:
    return f"""\
run:
  {invariants}
stage:
  max_epochs: 10
  n_adam: 5
  stagnation_window: 2
  percentile_10_relaxation: 0.1
opt: {{}}
loss: {{}}
"""


def test_invariants_config_default_is_record_only():
    from pinn.training.config import InvariantsConfig

    config = InvariantsConfig()

    assert config.front_advance_window_n is None


@pytest.mark.parametrize("value", [0, -1, "250", True, False])
def test_invariants_config_rejects_non_positive_or_wrong_type(value):
    from pinn.training.config import InvariantsConfig

    with pytest.raises(ValueError):
        InvariantsConfig(front_advance_window_n=value)


def test_invariants_config_accepts_positive_int():
    from pinn.training.config import InvariantsConfig

    assert InvariantsConfig(front_advance_window_n=250).front_advance_window_n == 250


def test_yaml_invariants_constructs_dataclass(tmp_path):
    from pinn.training.config import InvariantsConfig
    from pinn.training.config_yaml import load_config

    path = tmp_path / "config.yaml"
    path.write_text(_minimal_yaml(invariants="invariants:\n    front_advance_window_n: 250"))

    config = load_config(path)

    assert isinstance(config.run.invariants, InvariantsConfig)
    assert config.run.invariants.front_advance_window_n == 250


def test_yaml_invariants_unknown_key_is_dotted(tmp_path):
    from pinn.training.config_yaml import ConfigKeyError, load_config

    path = tmp_path / "config.yaml"
    path.write_text(_minimal_yaml(invariants="invariants:\n    typo_field: 1"))

    with pytest.raises(ConfigKeyError) as exc_info:
        load_config(path)

    assert exc_info.value.dotted_path == "run.invariants.typo_field"


def test_run_config_rejects_non_invariants_config():
    from pinn.training.config import RunConfig

    with pytest.raises(TypeError, match=r"run\.invariants must be InvariantsConfig"):
        RunConfig(invariants={})  # type: ignore[arg-type]

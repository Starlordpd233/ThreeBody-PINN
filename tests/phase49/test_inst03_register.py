"""INST-03 fail-closed divergence-register and proof-test coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from pinn.conformance import register


def _entry(*, status: str = "open", **overrides):
    value = {
        "id": "X-1",
        "kind": "divergence",
        "status": status,
        "title": "fixture",
        "spec_citation": "fixture §1",
        "authority": "test fixture",
        "rationale": "fixture rationale",
        "what_it_would_take": "fixture closure",
        "proof_test": None,
        "waiver": None,
    }
    value.update(overrides)
    if status == "closed" and "proof_test" not in overrides:
        value["proof_test"] = "tests/phase48/test_stage0_energy_config.py::test_loss_config_default_drives_stage0_zero_schedule"
    return value


def _write(tmp_path: Path, payload) -> Path:
    path = tmp_path / register.DIVERGENCE_REGISTER_FILENAME
    text = payload if isinstance(payload, str) else json.dumps(payload)
    path.write_text(text, encoding="utf-8")
    return path


def _payload(*entries):
    return {"schema_version": register.REGISTER_SCHEMA_VERSION, "entries": list(entries)}


@pytest.mark.parametrize(
    ("name", "setup", "pattern"),
    [
        ("missing", lambda tmp: tmp / "absent.json", "not found"),
        ("malformed", lambda tmp: _write(tmp, "{"), "not valid JSON"),
        ("non_object", lambda tmp: _write(tmp, []), "JSON object"),
        (
            "wrong_keys",
            lambda tmp: _write(tmp, {"schema_version": 1, "entries": [], "extra": 1}),
            "keys must be exactly",
        ),
        (
            "wrong_version",
            lambda tmp: _write(tmp, {"schema_version": 999, "entries": []}),
            "schema_version",
        ),
        (
            "unknown_kind",
            lambda tmp: _write(tmp, _payload(_entry(kind="mystery"))),
            "unknown kind",
        ),
        (
            "unknown_status",
            lambda tmp: _write(tmp, _payload(_entry(status="mystery"))),
            "unknown status",
        ),
        (
            "duplicate_id",
            lambda tmp: _write(tmp, _payload(_entry(), _entry(id="X-1"))),
            "duplicate id",
        ),
        (
            "closed_without_proof",
            lambda tmp: _write(tmp, _payload(_entry(status="closed", proof_test=None))),
            "closed.*proof_test",
        ),
        (
            "waived_without_authority",
            lambda tmp: _write(tmp, _payload(_entry(status="waived"))),
            "waived.*waiver",
        ),
    ],
)
def test_schema_rejections_are_distinct(tmp_path, name, setup, pattern):
    path = setup(tmp_path)
    with pytest.raises(ValueError, match=pattern):
        register.load_divergence_register(path)


def test_empty_schema_valid_register_loads(tmp_path):
    path = _write(tmp_path, _payload())
    assert register.load_divergence_register(path)["entries"] == []


def test_duplicate_ids_are_rejected_even_when_entries_differ(tmp_path):
    path = _write(tmp_path, _payload(_entry(), _entry(id="X-1", title="different")))
    with pytest.raises(ValueError, match="duplicate id"):
        register.load_divergence_register(path)


def test_committed_register_has_mandatory_entries_and_authorized_waivers():
    payload = register.load_divergence_register()
    by_id = {entry["id"]: entry for entry in payload["entries"]}
    assert {
        "CONF-01-QUALIFICATION",
        "PLAT-01-SINGLE-STAGE",
        "PLAT-02-SLBFGS",
        "INV-B-N-UNSET",
    } <= set(by_id)
    assert by_id["INV-B-N-UNSET"]["kind"] == "divergence"
    assert by_id["INV-B-N-UNSET"]["status"] == "open"
    assert by_id["INV-B-N-UNSET"]["waiver"] is None
    assert by_id["PLAT-01-SINGLE-STAGE"]["waiver"] == "SCOPE-27"
    assert "SCOPE-27" in by_id["PLAT-02-SLBFGS"]["waiver"]
    assert "EVAL-01" in by_id["CONF-01-QUALIFICATION"]["rationale"]
    assert "measured" in by_id["CONF-01-QUALIFICATION"]["rationale"]


def test_every_closed_register_entry_has_a_real_passing_proof_test():
    payload = register.load_divergence_register()
    closed = [entry for entry in payload["entries"] if entry["status"] == "closed"]
    assert closed
    for entry in closed:
        node = entry["proof_test"]
        assert node
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", node],
            cwd=Path(__file__).parents[2],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, f"{entry['id']} proof failed:\n{result.stdout}\n{result.stderr}"


def test_register_serialization_is_deterministic(tmp_path):
    payload = _payload(_entry())
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    register.write_divergence_register(first, payload)
    register.write_divergence_register(second, payload)
    assert first.read_bytes() == second.read_bytes()

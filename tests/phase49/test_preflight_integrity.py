"""Phase 49 / CR-11 + CR-05 — preflight artifacts cannot lie or crash the summary.

Two independent holes closed here:

CR-11 (non-finite payloads). ``json.loads`` accepts the non-standard ``NaN`` /
``Infinity`` / ``-Infinity`` tokens by default, and the preflight payload is
copied into the terminal summary, whose writer serializes with
``allow_nan=False``. A single non-finite leaf therefore turned a refused run's
honest terminal summary into an unhandled ``ValueError`` at write time — the
death mode the artifact exists to survive.

CR-05 (semantic forgery). Validation checked shape and enum membership only, so
``preflight_status: "passed"`` could sit on top of a failed event or a failed
locked check, and ``_eval01_precondition_i`` would trust it.

Every refusal below is driven to actually trip (D-16).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pinn.conformance.preflight import (
    PREFLIGHT_FILENAME,
    PREFLIGHT_SCHEMA_VERSION,
    PreflightRecorder,
    load_preflight,
)


def _check(*, name="lambda_e_max", tier="locked", passed=True, actual=0.0):
    return {
        "name": name,
        "tier": tier,
        "expected": 0.0,
        "actual": actual,
        "passed": passed,
    }


def _event(*, status="passed", checks=None, open_divergences=None):
    return {
        "event": "run_start",
        "stage": 0,
        "status": status,
        "checks": [_check()] if checks is None else checks,
        "census": None,
        "open_divergences": list(open_divergences or []),
        "findings": [],
    }


def _payload(*, status="passed", events=None):
    return {
        "schema_version": PREFLIGHT_SCHEMA_VERSION,
        "preflight_status": status,
        "assertions": [_event()] if events is None else events,
    }


def _write_artifact(run_dir: Path, text: str) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / PREFLIGHT_FILENAME
    path.write_text(text, encoding="utf-8")
    return path


def _write_payload(run_dir: Path, payload) -> Path:
    # allow_nan=True on purpose: this is the forger, not the product.
    return _write_artifact(run_dir, json.dumps(payload, indent=2) + "\n")


# --- CR-11: non-finite values are refused at load --------------------------


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_json_constant_is_refused_at_load(tmp_path, token):
    """The raw token never becomes a float; parse_constant refuses it first."""
    text = json.dumps(_payload(), indent=2).replace('"actual": 0.0', f'"actual": {token}')
    _write_artifact(tmp_path, text)

    with pytest.raises(ValueError, match="non-finite JSON constant"):
        load_preflight(tmp_path)


@pytest.mark.parametrize(
    ("label", "value"),
    [("nan", float("nan")), ("inf", float("inf")), ("-inf", float("-inf"))],
)
def test_non_finite_leaf_is_refused_by_payload_validation(label, value):
    """Belt two: a non-finite float reaching validation is refused on its own.

    Driven in memory on purpose — a JSON round trip would be caught by the
    parse_constant hook first, leaving this branch unproven.
    """
    from pinn.conformance.preflight import _validate_payload

    with pytest.raises(ValueError, match="is not finite"):
        _validate_payload(_payload(events=[_event(checks=[_check(actual=value)])]))


def test_non_finite_in_nested_evidence_is_refused():
    """Depth matters: the scan is recursive, not top-level only."""
    from pinn.conformance.preflight import _validate_payload

    event = _event()
    event["findings"] = [{"detail": {"nested": [1.0, float("inf")]}}]

    with pytest.raises(ValueError, match=r"findings\[0\].detail.nested\[1\]"):
        _validate_payload(_payload(events=[event]))


def test_non_finite_nested_evidence_is_also_refused_at_load(tmp_path):
    """Same defect through the real loader, wherever the refusal lands."""
    event = _event()
    event["findings"] = [{"detail": {"nested": [1.0, float("inf")]}}]
    _write_payload(tmp_path, _payload(events=[event]))

    with pytest.raises(ValueError):
        load_preflight(tmp_path)


def test_recorder_cannot_write_a_non_finite_value(tmp_path):
    """The codebase must not be able to CREATE evidence it cannot serialize."""
    recorder = PreflightRecorder(tmp_path)

    with pytest.raises(ValueError):
        recorder.append_event(
            event="run_start",
            stage=0,
            status="passed",
            checks=[_check(actual=float("nan"))],
        )

    assert not (tmp_path / PREFLIGHT_FILENAME).exists()
    assert recorder.events == ()


def test_recorder_writer_uses_allow_nan_false(tmp_path):
    """Prove the writer's own guard, independent of _reject_non_finite."""
    recorder = PreflightRecorder(tmp_path)
    recorder.append_event(
        event="run_start", stage=0, status="passed", checks=[_check()]
    )
    # Corrupt the retained event, bypassing append_event's validation, then
    # force a rewrite: the writer itself must refuse.
    recorder._events[0]["checks"][0]["actual"] = float("inf")

    with pytest.raises(ValueError):
        recorder._write()


# --- CR-11: the death-mode honesty guarantee still holds -------------------


def test_terminal_summary_still_renders_when_the_artifact_is_refused(tmp_path):
    """A rejected artifact must not stop a failed run from reporting honestly."""
    from pinn.training.summary import finalize_summary

    text = json.dumps(_payload(), indent=2).replace('"actual": 0.0', '"actual": NaN')
    _write_artifact(tmp_path, text)

    finalize_summary(
        tmp_path,
        disposition="failed",
        header={"run_name": "death-mode", "seed": 11},
        final_losses={"total": 1.0},
        curriculum_path=None,
        validation_records_path=None,
        metrics_path=None,
        prior_summary_path=None,
    )

    payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert payload["disposition"] == "failed"
    assert payload["conformance"] is None
    assert payload["eval01_precondition_i"] is False
    assert "## Conformance" in (tmp_path / "summary.md").read_text(encoding="utf-8")


def test_eval01_precondition_cannot_raise_on_a_malformed_artifact(tmp_path):
    from pinn.training.summary import _eval01_precondition_i

    _write_artifact(tmp_path, "{not json")

    assert _eval01_precondition_i(tmp_path) is False


# --- CR-05: a passed artifact must agree with its own evidence -------------


def test_forged_passed_status_over_a_failed_locked_check_is_refused(tmp_path):
    """The forgery that used to report eligibility.

    Before this fix the loader accepted the artifact and
    ``_eval01_precondition_i`` returned True from a run whose locked PHYS-05
    check had failed.
    """
    _write_payload(
        tmp_path,
        _payload(events=[_event(checks=[_check(passed=False, actual=1.0)])]),
    )

    with pytest.raises(ValueError, match="failed locked check"):
        load_preflight(tmp_path)


def test_forged_passed_status_over_a_failed_event_is_refused(tmp_path):
    _write_payload(
        tmp_path,
        _payload(
            status="passed",
            events=[_event(status="failed", checks=[_check(passed=False)])],
        ),
    )

    with pytest.raises(ValueError, match="preflight_status is 'passed'"):
        load_preflight(tmp_path)


def test_forged_artifact_cannot_report_eval01_eligibility(tmp_path):
    """The end-to-end property, asserted through the consumer that matters."""
    from pinn.training.summary import _eval01_precondition_i

    _write_payload(
        tmp_path,
        _payload(events=[_event(checks=[_check(passed=False, actual=1.0)])]),
    )

    assert _eval01_precondition_i(tmp_path) is False


def test_failed_advisory_check_under_passed_status_is_accepted(tmp_path):
    """The advisory tier is evidence, not a contradiction.

    ``assert_phys05_table`` records an advisory mismatch WITHOUT raising, so
    refusing it here would reject honest artifacts.
    """
    _write_payload(
        tmp_path,
        _payload(
            events=[
                _event(
                    checks=[
                        _check(),
                        _check(name="lambda_ic", tier="advisory", passed=False),
                    ]
                )
            ]
        ),
    )

    payload = load_preflight(tmp_path)

    assert payload["preflight_status"] == "passed"


def test_open_divergence_under_passed_status_loads_but_is_not_eligible(tmp_path):
    """A passed run carrying an open divergence is a documented state (D-23/D-27).

    The artifact IS the caveat record, so refusing to load it would destroy the
    evidence trail. Eligibility is denied by the precondition instead.
    """
    from pinn.training.summary import _eval01_precondition_i

    _write_payload(
        tmp_path,
        _payload(
            events=[
                _event(
                    open_divergences=[
                        {"id": "SOME-OPEN", "kind": "divergence", "status": "open"}
                    ]
                )
            ]
        ),
    )

    payload = load_preflight(tmp_path)

    assert payload["preflight_status"] == "passed"
    assert _eval01_precondition_i(tmp_path) is False


def test_failed_status_with_a_failed_locked_check_still_loads(tmp_path):
    """A refused run's evidence must remain loadable — that is the D-27 record."""
    payload = load_preflight(
        _write_payload(
            tmp_path,
            _payload(
                status="failed",
                events=[_event(status="failed", checks=[_check(passed=False)])],
            ),
        ).parent
    )

    assert payload["preflight_status"] == "failed"

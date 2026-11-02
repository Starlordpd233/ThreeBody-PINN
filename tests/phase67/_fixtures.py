"""Plan 67-01: the shared synthetic Phase 67 fixtures.

Plain functions and classes only — never a ``unittest.TestCase`` subclass —
so importing this module from any Phase 67 suite (or discovering
``tests/phase67``) never re-runs an older phase's classes. Everything here
routes the fit harness to the synthetic gold corpus seam and injects the
power gate's clock and pmset reader; no real corpus, MPS device or orbit is
ever reached.
"""

from __future__ import annotations

from unittest import mock

import pinn.verification.diagnostic_fit as fit_module
from tests.phase65.test_fit_short import (
    _InlineQueue,
    _fit_registration_fixture,
    _smoke_settings,
)

__all__ = [
    "fake_clock",
    "fake_pmset",
    "inline_supervisor",
    "patch_data_seam",
    "phase67_fixture_registration",
    "phase67_settings",
]


def phase67_settings(**overrides):
    """The Phase 65 fixture settings carrying the EXP-02 depth-2 variant.

    The variant block is built through the sealed Phase 65 variant class so
    admission's byte-agreement loop ties the block to the registry entry; the
    catalog pins EXP02_D2_VARIANT to the same fields. Values match D-03:
    depth 2 at the locked width 256, raw [tau, IC13], first omega 30, the
    locked hidden omega, rate 1e-4 and the [0, 10] window.
    """

    from pinn.verification.diagnostic_variants import DiagnosticVariant

    variant = DiagnosticVariant(
        name="exp02-d2-w256-o30",
        time_features="raw_tau_ic13",
        depth=2,
        width=256,
        learning_rate=1e-4,
        window_length=10.0,
        first_omega_0=30.0,
    )
    extra = {"variant": variant.to_json_dict(), "variant_registry": "phase67"}
    extra.update(overrides)
    return _smoke_settings(**extra)


def phase67_fixture_registration(root, **settings_extra):
    """A committed fixture registration with the EXP-02 variant and registry."""
    return _fit_registration_fixture(
        root, settings_extra=phase67_settings(**settings_extra)
    )


def patch_data_seam(stack, context, data, spec):
    """Route the run body to the fixture data seam on both harness modules.

    Exactly AttemptOwnershipTests._patched_data: open_diagnostic_context,
    load_diagnostic_data and one_orbit_spec are patched on
    pinn.verification.diagnostic_fit and on pinn.verification.diagnostic_data.
    """
    import pinn.verification.diagnostic_data as diagnostic_data

    for module in (fit_module, diagnostic_data):
        stack.enter_context(mock.patch.object(
            module, "open_diagnostic_context", create=True,
            return_value=context,
        ))
        stack.enter_context(mock.patch.object(
            module, "load_diagnostic_data", create=True, return_value=data,
        ))
        stack.enter_context(mock.patch.object(
            module, "one_orbit_spec", create=True, return_value=spec,
        ))
    return stack


def inline_supervisor(target, args, *, timeout, **kwargs):
    """Run the supervised worker in-process over an _InlineQueue."""
    queue = _InlineQueue()
    target(*args, queue)
    return ("exited", queue.payload)


def fake_pmset(first_line):
    """An injectable pmset reader whose stdout begins with ``first_line``."""

    def read_power():
        return first_line + "\n"

    return read_power


def fake_clock(iso_text):
    """An injectable weekend-window clock giving the aware datetime in ``iso_text``.

    The fixtures run on every weekday, so both launch cases inject a Saturday
    in America/Chicago (plan 66-02's weekend window, D-08).
    """
    from datetime import datetime

    moment = datetime.fromisoformat(iso_text)
    return lambda: moment

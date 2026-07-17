"""Phase 40 — Stage-0 curriculum training loop (FUT-04) test suite (Wave 0).

Wave 0 (plan 40-01) lands the dataset-free test CONTRACT and the empty
``pinn/training/`` package marker. Later waves (plans 40-02..40-06) implement
against these frozen expectations; the suite turns from localized skips to green
as each production symbol lands.

Skip discipline
---------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase40 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
final grep can deterministically detect any remaining skip without phrase drift.
When the suite is fully green (all production symbols present) the phrase appears
nowhere in the run log.

Governance
----------
``simulation_data/`` is STRICTLY READ-ONLY. Every fixture in this suite is
synthesized in memory; no test writes beneath the real corpus tree. Wave 0 owns
``pinn/training/__init__.py`` and ``tests/phase40/*``; later plans own the
production modules under ``pinn/training/``.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase40 production symbol"

__all__ = ["_SKIP_PHRASE"]

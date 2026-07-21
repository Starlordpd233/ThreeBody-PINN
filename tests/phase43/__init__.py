"""Phase 43 — verification / Stage-0 pilot / acceptance test suite (Wave 1).

Wave 1 (plan 43-01) lands the ``pinn.verify`` five-rung ladder, its
``runs/.verify/latest-marker.json`` contract, and this shared test scaffold.
Later plans (43-02..43-08) implement against the same convention; each suite
turns from localized skips to green as its production symbol lands.

Skip discipline
---------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase43 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
final grep can deterministically detect any remaining skip without phrase drift.
When the suite is fully green (all production symbols present) the phrase appears
nowhere in the run log.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase43 production symbol"

__all__ = ["_SKIP_PHRASE"]

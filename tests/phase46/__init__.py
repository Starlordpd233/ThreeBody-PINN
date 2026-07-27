"""Phase 46 — frame resolution & gate-aligned validation test suite (Wave 1).

Wave 1 (plan 46-01) lands this shared test scaffold plus the dataset-free
fixtures every later Phase 46 strand builds on: the duck-typed
``StageIndex``-shaped stub source for the INST-01 gate/isolation suites and the
dual-frame synthetic trajectory fixture the CONF-01 frame probe needs (D-21).
Later plans (46-02..46-07) implement against the same convention; each suite
turns from localized skips to green as its production symbol lands.

Skip discipline
---------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase46 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
final grep can deterministically detect any remaining skip without phrase drift.
When the suite is fully green (all production symbols present) the phrase appears
nowhere in the run log.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase46 production symbol"

__all__ = ["_SKIP_PHRASE"]

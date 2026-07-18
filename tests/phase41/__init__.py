"""Phase 41 — config / checkpointing / resume / determinism test suite (Wave 0).

Wave 0 (plan 41-01) lands the shared atomic-io primitive, the extended
TrainingConfig surface, the keyed-YAML resolver, and the deferred-guard test
scaffold. Later waves (plans 41-02..41-05) implement against these frozen
expectations; the suite turns from localized skips to green as each production
symbol lands.

Skip discipline
---------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase41 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
final grep can deterministically detect any remaining skip without phrase drift.
When the suite is fully green (all production symbols present) the phrase appears
nowhere in the run log.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase41 production symbol"

__all__ = ["_SKIP_PHRASE"]

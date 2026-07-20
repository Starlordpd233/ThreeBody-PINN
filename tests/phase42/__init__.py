"""Phase 42 — operator runbook surface & monitoring test suite (Wave 0).

Wave 0 (plan 42-03) lands the shared skip phrase, a dataset-free synthetic
Stage-0 fixture extended with forced-divergence and forced-HALT injection knobs,
and nine skip-guarded test stubs. Later plans (42-04..42-09) implement against
these frozen expectations; the suite turns from skips to green as each
production symbol lands.

Skip discipline
---------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase42 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
final grep can deterministically detect any remaining skip without phrase drift.
When the suite is fully green (all production symbols present) the phrase appears
nowhere in the run log.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase42 production symbol"

__all__ = ["_SKIP_PHRASE"]

# TODO(phase-43): s/step non-degradation smoke — once the step-log registry and
# residual-panel TB sink are exercised by production runs (plans 42-04/05), add a
# smoke test asserting that a fresh run emits at least one JSONL record carrying
# a ``residuals_bin_*`` field AND at least one TensorBoard scalar under the
# residual-panel tag namespace. Deferred to phase 43 because the production
# symbols are still landing in wave 1/2 of this milestone.

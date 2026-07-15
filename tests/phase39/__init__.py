"""Phase 39 — Data Ingestion & Stage-0 Population Scan test suite (Wave 0).

Wave 0 (plan 39-01) lands the complete nine-file executable test CONTRACT for
every Phase 39 behavior (DATA-01..06) BEFORE any production code exists under
``pinn/data/``. Later waves (plans 39-02..39-06) implement against these frozen
expectations; the suite turns from localized skips to green as each production
symbol lands.

Skip discipline (cycle-4 deepseek MEDIUM)
-----------------------------------------
Every deferred test uses a module-local ``_require(symbol, module)`` helper that
raises ``unittest.SkipTest`` (never an ``ImportError``/ERROR) while a later-wave
production symbol is absent. Each such helper imports the single
``_SKIP_PHRASE`` constant defined here and emits a reason string of the exact
form::

    "skipped Phase39 production symbol <module>.<symbol>"

The one constant is never re-spelled independently across test modules, so the
Wave-5 final grep (task 39-07-01) can deterministically detect any remaining
skip without phrase drift. When the suite is fully green (all production
symbols present) the phrase appears nowhere in the run log.

Governance
----------
``simulation_data/`` is STRICTLY READ-ONLY. Every fixture in this suite is
synthesized under a ``TemporaryDirectory`` (see ``_fixtures.py``); no test
writes beneath the real corpus tree. Wave 0 owns ONLY ``tests/phase39/*`` and
takes no production-file ownership — plans 39-02/39-03 own all of ``pinn/data``.
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently (the
# Wave-5 grep in task 39-07-01 keys on this exact literal).
_SKIP_PHRASE = "skipped Phase39 production symbol"

__all__ = ["_SKIP_PHRASE"]

# Phase 47 — deferred items (out of scope for the plan that found them)

Discoveries made while executing a Phase 47 plan that are NOT caused by that
plan's changes. Logged here, deliberately not fixed (executor scope boundary).

---

## D-47-01 — 12 pre-existing `tests/phase43/` failures from missing evidence artifacts

**Found during:** plan 47-01, task 1 (broad regression sweep after the residency swap).

**What:** `pytest tests/phase43 -q` reports 12 failures on a clean tree:

| file | failures |
|---|---|
| `tests/phase43/test_pilot_calibration.py` | 2 |
| `tests/phase43/test_smoke.py` | 1 |
| `tests/phase43/test_verdict_grounding.py` | 7 |
| `tests/phase43/test_verify_gate.py` | 2 |

The first ten fail with `FileNotFoundError` on retained Phase 43 evidence — e.g.
`.planning/phases/43-verification-stage-0-pilot-acceptance/evidence/pilot/README.md`.
That whole `evidence/` tree was removed by `89348b7c chore(planning): archive
v2.0 milestone files`, which is an ANCESTOR of the Phase 47 branch point, so the
tests were already red before this phase began. The two `test_verify_gate.py`
failures are the same class: they need a persisted Stage-0 timing calibration
that no longer exists on disk.

**Why it is not a Phase 47 finding:** none of these tests exercise adapter
residency, `RATIFIED_VALIDATION_FRAME`, or anything else plan 47-01 touched.
`tests/phase43/test_evaluate_gate.py` and `test_real_data_smoke_config.py` DO
reference those symbols, and both pass.

**Not fixed here because:** repairing them means either restoring archived
milestone evidence or re-pointing the tests at the archive — a governance
decision about the v2.0 archive, well outside CONF-09.

**Suggested routing:** a v2.2 planning/test hygiene pass, alongside the
`validation_gate.py:526-528` stale-citation correction that 47-01-PLAN.md's
`<line_number_note>` routes the same way.

**Status:** OPEN — informational, not blocking Phase 47.

**Pre-existence proven at phase close (2026-07-31).** The claim was verified
historically rather than by inference. A detached worktree was created at the
Phase 47 branch point (`c0d4d9dd`, parent of the first phase-47 commit) and
`tests/phase43/` was run there. With the untracked `runs/` directory symlinked in
so both environments matched, the pre-Phase-47 tree produced **12 failed, 186
passed, 0 skipped — byte-identical to HEAD**. (Without `runs/`, the fresh
worktree instead reports 11 failed / 8 skipped, because `tests/phase43/test_smoke.py`
skips when `runs/stage0-smoke/summary.json` is absent — an environment artifact,
not a code difference.) `git log --diff-filter=D` confirms `89348b7c` as the
deleting commit and `git merge-base --is-ancestor` confirms it predates the phase
by six days. Control: the two `phase43` modules that DO exercise Phase 47 symbols
pass fully (`test_evaluate_gate` 13 passed, `test_real_data_smoke_config` 29
passed). **Phase 47 introduced zero regressions.** Routing suggestion unchanged.

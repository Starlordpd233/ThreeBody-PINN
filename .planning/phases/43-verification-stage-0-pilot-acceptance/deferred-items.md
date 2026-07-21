# Phase 43 — Deferred Items

Out-of-scope discoveries found during plan execution, logged per the
SCOPE BOUNDARY rule (fix only what the current plan's owned files cover;
log the rest here rather than silently expanding scope).

## DI-43-04-01: tests/phase41/test_train_entrypoint.py subprocess-launch tests now fail against the ACC-01 duration gate

**Found during:** 43-04 (>30-min launch duration gate), regression sweep of
`tests/phase41` after wiring `pinn.train._check_duration_gate`.

**Symptom:** 17 of 193 `tests/phase41` tests fail — all and only in
`tests/phase41/test_train_entrypoint.py`, all real `python -m pinn.train`
subprocess launches (fresh, non-smoke, non-resume) against an isolated
temp `runs/` root with no persisted `runs/.calibration/stage0-timing.json`.
Each fails with:

```
error: no valid persisted Stage-0 timing calibration is available for a
non-smoke launch (2 steps on float32/mps); refusing before construction
rather than forecasting without a measurement.
```

Representative failures: `LaunchContractTests.test_fresh_launch_writes_artifacts`,
`RunFolderCollisionTests.test_fresh_launch_into_existing_raises`,
`HookClosureContractTests.test_rolling_checkpoint_carries_curriculum_stage`,
`StrictCpuOverrideTests.test_strict_cpu_forces_float64_cpu_into_build_network`,
and 13 others in the same file (full list in the 43-04 execution transcript).

**Why this is not a 43-04 bug:** The refusal is the plan's literal, reviewed
contract — 43-04-PLAN.md `must_haves.truths`: *"A non-smoke run with no valid
persisted timing measurement is refused before construction"* — unconditional
on duration, because with no calibration the gate cannot forecast at all and
therefore cannot prove a run is under 30 minutes (SPEC edge R2, `43-SPEC.md`
prohibition 4). 43-REVIEWS.md's HIGH finding on 43-04 explicitly asked for
this exact fail-closed behavior ("define fail-closed behavior when [the
timing input] is absent"). `tests/phase41/test_verify_gate.py` (this plan's
own test file) exercises and asserts precisely this refusal path as intended
behavior, not a defect.

**Why it is out of scope for 43-04 to fix:** 43-04's `files_modified` is
`[pinn/train.py, tests/phase43/test_verify_gate.py]` only; the executing
agent's task instructions explicitly restrict owned/stageable paths to those
two files plus the SUMMARY and tracking docs. Editing
`tests/phase41/test_train_entrypoint.py` (add a pre-launch calibration
fixture, or mark the affected launches `run.smoke: true`) is a different
plan's owned path.

**Scope note:** `tests/phase41/test_resume.py` (the file 43-06-PLAN.md's own
verify step re-checks) is unaffected — it is pure unit-level (no subprocess
`pinn.train` launches), confirmed green (30/30) under the new gate.

**Recommended follow-up:** A small gap-closure task (or folded into 43-06,
which already runs a real smoke to produce a calibration) should update
`tests/phase41/test_train_entrypoint.py`'s fresh-launch helper to either (a)
write a matching `stage0-timing.json` calibration into the test's isolated
`runs_root` before each non-smoke subprocess launch, mirroring
`tests/phase43/test_verify_gate.py::_write_calibration`, or (b) set
`run.smoke: true` in the launched config where the test's intent is unrelated
to duration timing. Until then, `tests/phase41/test_train_entrypoint.py`
stays red under a from-scratch full-suite run; this is expected, not a
silent breakage — this file documents it so it is not mistaken for a new
bug during Phase 43 close-out.

**Status:** OPEN (informational; not blocking 43-04's own acceptance).

## DI-43-04-02: tests/phase42 subprocess-launch tests also fail against the same gate

**Found during:** 43-04, extending the same regression sweep to `tests/phase42`
(operator-runbook/monitoring). Same root cause and same out-of-scope
reasoning as DI-43-04-01 — logged separately because it is a different
plan's owned files (`tests/phase42/*`).

**Symptom:** Every `tests/phase42` test that launches a real, fresh, non-smoke
`python -m pinn.train` subprocess now fails or errors with the identical
`no valid persisted Stage-0 timing calibration is available for a non-smoke
launch` refusal. Confirmed directly: `test_honesty_layer.HonestyTests.
test_forced_divergence_catchable_state_not_finished`,
`test_honesty_layer.HonestyTests.test_forced_halt_catchable_state_not_finished_and_no_fabricated_metrics`,
`test_redaction.RedactionTests.test_no_forbidden_shapes_in_artifacts`,
`test_runs_contract.RunsContractTests.test_mem_line_emitted_into_real_run_train_log`,
`test_runs_contract.RunsContractTests.test_sigkill_at_launch_presence_and_staleness`,
`test_runs_contract.RunsContractTests.test_sigkill_mid_adam_presence_and_staleness`.
Pure config/unit tests in the same discover run stay green
(`test_runbook_config.RunbookConfigTests.*`), confirming the failure is
scoped exactly to real subprocess launches, not a broader breakage.

**Secondary effect (not a correctness bug, a cost note):** several
`test_runs_contract` "sigkill mid-<phase>" tests are written to poll
`wait_for_status(...)` for a status transition (e.g. "reached mid-Adam")
that a gate-refused launch — which exits before `run_dir.mkdir` and never
writes `status.json` — can never produce. Those tests now pay out their
full polling timeout before failing instead of failing fast, materially
inflating `tests/phase42`'s wall-clock time versus its pre-43-04 baseline
(43-03-SUMMARY.md recorded "passed, 0 failures/errors" with no duration
noted; this run exceeded 10 minutes for 38 tests, versus tests that used to
complete in seconds once their fresh launch succeeded).

**Not enumerated exhaustively:** a full `tests/phase42` discover run was
started and confirmed the pattern above; it was not run to completion in
this session because of the timeout-inflation cost noted above compounding
across the full 38-test file set. The follow-up fix (same remedy as
DI-43-04-01, applied to `tests/phase42`'s launch fixtures) should re-run
`python -m unittest discover -s tests/phase42 -v` to completion and confirm
0 failures/errors once landed.

**Status:** OPEN (informational; not blocking 43-04's own acceptance).

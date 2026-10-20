---
phase: 60-single-system-learnability
plan: 02
subsystem: testing
tags: [mps, float32, scorer, gap-59-13, successor-digest, lbfgs, strong-wolfe, torch-load-weights-only]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: shared scorer (network_trajectory, score_network), frozen scorecard (tier_of, lbfgs_polish), evidence writer, the GAP-59-13 forward item
  - phase: 60-single-system-learnability
    provides: "Plan 60-01's tests/phase60 package and the learnability_losses.data_polish_objective closure the smoke exercises"
provides:
  - "feasibility_scorer._to_cpu_float64 and an MPS-safe network_trajectory / score_network (CPU, then float64, at all three widening sites)"
  - "evidence/scorer-successor.json (phase60-scorer-successor/v1): the single D-09 successor digest, tracked and pinned by a test"
  - "tests/phase60/test_scorer_mps.py: MPS regression, static widen guard, non-finite tier rule, successor-record check, opt-in platform probe"
  - "tests/phase60/test_mps_lbfgs_smoke.py: MPS float32 strong-Wolfe L-BFGS smoke, state round trip, production-network and harness-closure legs"
affects: [60-04, 60-08, 60-10, 60-23]

actuals:
  tokens: 6286
  tasks: 3
  commits: 3
plan_head_before: 170794f368723214c1989f8949ff543849bb41f5

tech-stack:
  added: []
  patterns:
    - "A test whose reference value is computed independently of the function under test, so a wiring mutation cannot appear on both sides"
    - "Static detectors as pure functions of source text, each with an injected-violation self-test"
    - "A committed successor record that a test pins to the file on disk, so a later edit without a new record fails"
    - "Opt-in environment switches: PHASE60_ALLOW_NO_MPS turns a missing MPS device into a skip, PHASE60_PLATFORM_PROBES runs the non-gating platform probe"

key-files:
  created:
    - tests/phase60/test_scorer_mps.py
    - tests/phase60/test_mps_lbfgs_smoke.py
    - .planning/phases/60-single-system-learnability/evidence/scorer-successor.json
  modified:
    - pinn/verification/feasibility_scorer.py

key-decisions:
  - "The float32 test tolerance is a bound relative to the CPU array's largest magnitude (1e-3), not the plan's element-wise rtol 1e-4 / atol 1e-5, which leaves 17, 41 and 42 percent of the elements outside for the production network at first-layer frequency 30"
  - "The CPU float64 reference in the MPS trajectory test comes from the trainer's closure and componentwise_du, not from network_trajectory, so a wiring mistake inside network_trajectory cannot cancel between the two sides"
  - "The MPS presence rule is stated once (mps_device_or_stop in test_scorer_mps.py) and the L-BFGS smoke imports it"
  - "The L-BFGS smoke also drives the harness's own chunked polish closure (data_polish_objective) on a gold-sized batch, because that, not the raw Huber loss, is what a real data-only arm hands to the optimizer"

requirements-completed: [INST-05, FEAS-03]

coverage:
  - id: D1
    description: "network_trajectory widens positions, velocities and accelerations on the CPU before float64 at all three sites: a float32 network on MPS is scored end to end (float64 (N, 3, 3) arrays, a ScoreResult) and the CPU float64 path is unchanged"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_scorer_mps.py#MpsTrajectoryTests, MpsScoreTests, StaticWidenTests, NonFiniteTierTests"
        status: pass
      - kind: unit
        ref: "tests.phase59.test_scorer_network, test_scorer_known_errors, test_diag07_panels, test_diag07, test_baselines, test_two_kepler, test_nn_copy, test_scorecard_rules, test_static_guards (139 tests, 0 skipped)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The single D-09 successor record names one path, the Phase 59 predecessor digest and the digest of the fixed scorer, is tracked and clean, and a test pins it to the file on disk"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_scorer_mps.py#SuccessorRecordTests"
        status: pass
      - kind: other
        ref: "git ls-files --error-unmatch .planning/phases/60-single-system-learnability/evidence/scorer-successor.json && git status --porcelain (empty)"
        status: pass
    human_judgment: false
  - id: D3
    description: "MPS float32 L-BFGS (frozen strong-Wolfe settings): finite non-increasing objectives on a tiny network, an optimizer-state round trip through torch.save and torch.load(weights_only=True) that resumes, and a finite one-call run on the production network with the Huber loss and with the harness polish closure"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_mps_lbfgs_smoke.py#TinyNetworkLbfgsTests, StateRoundTripTests, ProductionNetworkLbfgsTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "The frozen scorecard bytes, the twelve other hash-pinned Phase 59 producer modules, Plan 60-01's modules and tests/phase59 are byte-unchanged"
    verification:
      - kind: other
        ref: "git diff --quiet 170794f3 HEAD -- <frozen scorecard and JSON, nine pinned pinn modules, Phase 59 evidence modules, prior-plan files, tests/phase59>"
        status: pass
    human_judgment: false

duration: 18min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 02: MPS-safe scorer, successor digest and L-BFGS smoke Summary

**The shared scorer now scores a float32 network that lives on the Mac's MPS device (move to the CPU, then widen to float64, at all three `network_trajectory` sites), the one permitted D-09 successor digest is committed and pinned by a test, and the frozen strong-Wolfe L-BFGS polish is shown to run, stay finite and save its state on MPS float32, so the owner stop for a smoke failure was not triggered.**

## Performance

- **Duration:** about 18 min
- **Started:** 2026-10-20T00:43:41Z
- **Completed:** 2026-10-20T01:03:00Z (approximate)
- **Tasks:** 3 (Task 1 tracer, Task 2, Task 3)
- **Files:** 1 modified, 3 created; 587 added lines, 9 removed; no file deleted

## Accomplishments

- **Scorer fix (SPEC Requirement 3, GAP-59-13).** One module-private helper, `_to_cpu_float64(tensor)` = `tensor.detach().to("cpu").to(torch.float64)`, replaces the one-call widen at the position, velocity and acceleration appends. No import, docstring line or other function changed (the first line is still "Phase 59 (FEAS-01): the feasibility scorer.", 12 import statements before and after). On a CPU float64 network both moves are no-ops.
- **Successor record (D-09, part 1).** `evidence/scorer-successor.json` names exactly one path with the predecessor and successor digests below, written through `evidence_io.write_json` (record file SHA-256 `feee49e33f2fb975bab5ea929e01062e527bf3015454101e5a51f1fafe17c882`). `SuccessorRecordTests` fails if the record gains a key or a second path, if the predecessor changes, or if the scorer file stops matching the successor digest.
- **MPS L-BFGS smoke (60-RESEARCH Assumption A1).** All three classes ran and passed on this Mac, so no owner stop was needed. Settings were read from the scorecard (history 10, 50 iterations per outer call, strong Wolfe; `max_eval` 62, `lr` 1, `tolerance_grad` 1e-7, `tolerance_change` 1e-9). Observed in the tests' scratch twins: the tiny network's start-of-call objectives were 6.73e-1, 4.28e-4, 1.43e-4 and 4.83e-5 after the third call (50 iterations and 59 function evaluations in call 1); one outer call of the production network (seed 42, 64 points, Huber) went 2.04e-1 to 1.04e-2 in 50 iterations and 53 evaluations (0.6 s); the harness closure on 1001 points gave identical start objectives for one chunk and four chunks (2.090532e-1). The optimizer state keys match the research list: `H_diag, al, d, func_evals, n_iter, old_dirs, old_stps, prev_flat_grad, prev_loss, ro, t`. `PYTORCH_ENABLE_MPS_FALLBACK` was unset.
- **Static guard.** `StaticWidenTests` fails if any `.to(...)` call in the scorer carries both a `device` and a `dtype` keyword, if `_to_cpu_float64` is not a module-level function, or if `network_trajectory` does not call it exactly three times; each detector has an injected-violation self-test.

## Red-green evidence (SPEC Requirement 3 acceptance)

The new tests were run against the unedited scorer (SHA-256 `cd5019a2...870b`, clean against HEAD) before any edit. `MpsTrajectoryTests` and `MpsScoreTests` both errored at `feasibility_scorer.py` line 417 (the position append) with:

```
TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.
```

The static tests failed on the same code (`Lists differ: [417, 420, 425] != []` for the one-call widen, `0 != 3` for the helper calls, `unexpectedly None` for the helper); the run ended `FAILED (failures=3, errors=2, skipped=1)`. After the edit the same file passes. Opt-in probe: with `PHASE60_PLATFORM_PROBES=1`, `PlatformProbeTests` passes on this Mac (torch 2.12.1, macOS 26.5.1), confirming that the platform itself refuses the old one-call widen of an MPS float32 tensor.

## Scorer digests (D-09)

| | SHA-256 | Bytes |
|---|---|---|
| Predecessor (Phase 59, pinned by the committed results) | `cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b` | 17,626 |
| Successor (fixed `pinn/verification/feasibility_scorer.py`) | `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7` | 17,606 |

The frozen scorecard SHA-256 is unchanged: `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`.

## Task Commits

1. **Tasks 1 and 2: tracer fix, tests and successor record** - `57f48478` (fix). One commit by the plan's explicit instruction (Task 2: "Commit the scorer fix, the test and the record together"), so the scorer edit and the digest that pins it land together. The body names both digests.
2. **Task 3: MPS L-BFGS smoke** - `2c84d43a` (test)
3. **Task 3 addition: harness polish closure in the smoke** - `08189ab1` (test)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after Task 1: not auto mode (`AUTO_CHAIN` false, `AUTO_CFG` unset), mode `end-of-phase`, and the verify block has only `<automated>` entries, so all three verify commands were re-run on the finished tree (3 tests OK; 11 tests OK; 139 tests OK) before Task 2 started.

## Files Created/Modified

- `pinn/verification/feasibility_scorer.py` - `_to_cpu_float64` helper and its three call sites (+8, -9 lines)
- `.planning/phases/60-single-system-learnability/evidence/scorer-successor.json` - the single D-09 successor record
- `tests/phase60/test_scorer_mps.py` - 15 tests: presence, trajectory, score, static widen guard with self-tests, non-finite tier, successor record, opt-in probe
- `tests/phase60/test_mps_lbfgs_smoke.py` - 4 tests in 3 classes: tiny network, state round trip, production network and harness closure

## Decisions Made

- **Float32 tolerance.** Measured on the seed-7 production network over the 41 test times (MPS float32 against CPU float64, same weights): positions differ by 5.77e-5 on a scale of 1.23, velocities by 4.17e-2 on 478, accelerations by 50.7 on 5.33e5, which is 4.7e-5, 8.7e-5 and 9.5e-5 of each array's largest magnitude (at most 1.56e-4 across seeds 0 to 3). The bound is 1e-3 of that magnitude, a ten-fold margin, and it is a test parameter, not a scorecard value. MPS results were bitwise repeatable across three calls.
- **Independent reference.** The first version compared the MPS result with `network_trajectory` on CPU float64. Of seven injected scorer mutations it missed two that swap which array is appended (the swap appeared on both sides). The reference now comes from the trainer's closure plus `componentwise_du`; all seven mutations are caught (three one-call restores, a one-call helper, a helper that widens before the move, and the two swaps).
- **Presence rule once.** `mps_device_or_stop` lives in `test_scorer_mps.py`; the smoke imports it, and `tests/phase60/_fixtures.py` (Plan 60-01's file) was not touched.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The plan's float32 tolerance cannot hold for the production network**
- **Found during:** Task 1 (measuring before the green run)
- **Issue:** `behavior` asked for agreement to rtol 1e-4 and atol 1e-5. With the first SIREN layer at frequency 30, float32 rounding is amplified: 16.8, 40.7 and 42.0 percent of the position, velocity and acceleration elements fall outside that element-wise band, although the arrays agree to under 1e-4 of their largest magnitude.
- **Fix:** A scale-relative bound of 1e-3 (see Decisions), documented beside the constant in the test with the measured values.
- **Files modified:** `tests/phase60/test_scorer_mps.py`
- **Verification:** `MpsTrajectoryTests`; mutation checks M1 to M7
- **Committed in:** `57f48478`

**2. [Rule 2 - Missing critical] The reference side of the MPS comparison was not independent**
- **Found during:** Task 1 (mutation check of the green tests)
- **Issue:** Using `network_trajectory` for both sides let a wiring mistake inside it cancel out; two of seven mutations passed.
- **Fix:** Compute the CPU float64 arrays from `tests.phase59.test_scorer_network._closure` and `componentwise_du` without calling `network_trajectory`.
- **Files modified:** `tests/phase60/test_scorer_mps.py`
- **Verification:** all seven mutations fail the file afterwards; the scorer was restored byte-identical each time (SHA-256 `00edf81d...2bc7` checked)
- **Committed in:** `57f48478`

**3. [Rule 2 - Missing critical] The smoke did not cover the closure a real arm hands to L-BFGS**
- **Found during:** Task 3 (review before the SUMMARY)
- **Issue:** The plan's production leg uses the raw Huber loss on 64 points, while a real data-only arm hands L-BFGS `data_polish_objective` (chunked gradient accumulation) on about 1001 points. A defect there would first surface in a long real arm.
- **Fix:** One more method in `ProductionNetworkLbfgsTests` drives that closure on 1001 points in 256-row chunks (finite objective, drop across the call, finite parameters). A closure with no gradient makes it fail.
- **Files modified:** `tests/phase60/test_mps_lbfgs_smoke.py`
- **Verification:** the smoke file, 4 tests in 4.1 s, no skip
- **Committed in:** `08189ab1`

---

**Total deviations:** 3 auto-fixed (1 Rule 1, 2 Rule 2)
**Impact on plan:** All three strengthen the proof that the plan asks for; no file outside the plan's owned set changed and no frozen value moved.

### Process notes

- The smoke test asserts a few facts beyond the plan's list, all inside the named classes: the tiny objective after the last call is below the first, the production leg's objective drops, the saved state holds non-empty curvature history and moves from MPS to CPU, and the loaded state equals what was saved.
- The generic executor rule that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The cwd-drift and default-branch assertions were run before each commit.
- Commits carry `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.
- `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` were not touched. INST-05 and FEAS-03 are declared by many later plans in this phase, so the shared-ID gate leaves them for the orchestrator.
- `.planning/WINDOWS.md` was not appended. The only skip is `PlatformProbeTests`, a designed opt-in probe that was run once with its switch and passed; it is not a defect. The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_scorer_mps.MpsPresenceTests ...MpsTrajectoryTests ...MpsScoreTests -v` (Task 1 verify 1) | Ran 3 tests in 0.684s, OK, 0 skipped |
| `python -B -m unittest tests.phase60.test_scorer_mps -v` (Task 1 verify 2, final tree) | Ran 15 tests, OK (skipped=1: `PlatformProbeTests`, by design) |
| nine Phase 59 suites (Task 1 verify 3), before the edit and on the committed tree | Ran 139 tests in 28.9s and 28.7s, OK, 0 skipped |
| `python -B -m unittest tests.phase60.test_scorer_mps.SuccessorRecordTests -v` (Task 2 verify 1) | Ran 4 tests, OK; tampered successor, two paths and a seventh key each fail one named test, record restored byte-identical |
| `git ls-files --error-unmatch <record> && git status --porcelain -- <record> <scorer>` (Task 2 verify 2) | tracked, porcelain empty |
| `python -B -m unittest tests.phase60.test_mps_lbfgs_smoke -v` (Task 3 verify) | Ran 4 tests in 4.127s, OK, 0 skipped, 0 warnings |
| `tests.phase60.test_run_short tests.phase60.test_static_guards` (Plan 60-01 regression) | Ran 64 tests, OK |
| `tests.phase60.test_static_guards tests.phase39.test_prohibitions tests.phase38.test_prohibitions` | Ran 63 tests; the only 2 failures are `tests.phase38.test_prohibitions` `test_spec_byte_identity_endpoint_sha256` and `test_spec_history_no_touch_since_phase_base` (see Issues) |
| `git diff --quiet 170794f3 HEAD -- <frozen scorecard and JSON, nine pinned pinn modules, Phase 59 evidence modules, Plan 60-01 files, tests/phase59>` | exit 0 |
| `git diff --diff-filter=D --name-only HEAD~1 HEAD` after each commit | no deletions |

Complete logs are retained outside the repository in the session scratchpad. Nothing exceeded 60 s (longest 29 s), so no evidence-reuse rule was needed; the nine-suite run on the committed scorer is cited rather than repeated after the test-only commits.

## Issues Encountered

- Two `tests.phase38.test_prohibitions` tests fail at HEAD for a reason unrelated to this plan: `pinn_architecture.md` was edited after Phase 38. Plan 60-01 already recorded them as not a gate; they were not touched.
- `verify_phase59_evidence.py` is expected to stay red on the scorer's producer digest until Plan 60-04 teaches it the successor; per the plan it was not re-run.

## Known Stubs

None.

## Threat Flags

None. The edit adds no endpoint, auth path or file access; the tests write only inside a temporary directory and load with `weights_only=True`. Threat register: T-60-08 mitigated (one helper and three call sites, `StaticWidenTests`, nine Phase 59 suites, `SuccessorRecordTests`); T-60-02 mitigated (literal `weights_only=True` in the smoke); T-60-SC accepted (no package installed).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 60-04 can read `evidence/scorer-successor.json` (schema `phase60-scorer-successor/v1`; keys `schema`, `path`, `predecessor_sha256`, `successor_sha256`, `reason`, `note`); it is tracked, clean and matches the scorer on disk.
- The MPS L-BFGS smoke passed, so Plan 60-08 is not blocked by Assumption A1. The smoke proves optimizer, state and closure behavior on small batches; the physics-arm closure over 4096 rows (Plans 60-05 and 60-11) is not exercised here.
- The measured float32 against float64 agreement (under 1e-4 of scale for an untrained network) is context for the CPU float64 cross-check of a later plan, not a bound on a trained network's scores.
- Environment switches for other machines: `PHASE60_ALLOW_NO_MPS=1` skips the MPS classes, `PHASE60_PLATFORM_PROBES=1` runs the opt-in probe.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All four files exist (`tests/phase60/test_scorer_mps.py`, `tests/phase60/test_mps_lbfgs_smoke.py`, `evidence/scorer-successor.json`, `pinn/verification/feasibility_scorer.py`); commits `57f48478`, `2c84d43a` and `08189ab1` exist and `git log --grep=60-02` returns them.
- Task acceptance criteria re-run on the final tree: RED line quoted above; scorer docstring first line intact and no import added; only the scorer changed in `pinn/verification`; ten frozen or pinned producers byte-unchanged; record tracked, clean, one path, predecessor literal, successor equal to `shasum -a 256` of the scorer, commit body names both digests; the smoke file contains no `OptConfig` and reads the polish values from the scorecard.

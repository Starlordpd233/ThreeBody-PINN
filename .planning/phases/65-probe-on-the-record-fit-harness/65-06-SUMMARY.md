---
phase: 65-probe-on-the-record-fit-harness
plan: "06"
subsystem: testing
tags: [pinn, diagnostic-fit, smoke-run, committed-registration, synchronized-timing, whole-run-cap, exclusive-attempt, mps-float32, measured-cost]

requires:
  - phase: 65-probe-on-the-record-fit-harness (plan 65-05)
    provides: the retained registered reproduction, the committed logger-parity receipt (evidence/probe/logger-parity.json) and probe result the fit admission requires and records
  - phase: 65-probe-on-the-record-fit-harness (plans 65-01..65-04)
    provides: the synthetic fit harness, the guarded Stage-0 data seam, the production-entry refusals, and the shared committed-registration gate
  - phase: 60-single-system-learnability
    provides: the Stage-0 training gold records (hierarchical/gold/1632) and the sealed 33-module run protocol
provides:
  - pinn/verification/diagnostic_fit.py — the guarded real-data CLI (check-registration / run / verify-result) with committed-fit-registration admission (phase65-fit-registration/v1), bounded synchronized timing (2 warmup + 18 measured, injected clock, sync overhead recorded), the sub-hour whole-run cap enforced by deadline checks plus a supervised worker, exclusive attempt ownership with explicit incomplete status, and verify-result without retraining
  - .planning/phases/65-probe-on-the-record-fit-harness/65-SMOKE-PREDICTION.md + evidence/fit/smoke-registration.json — the committed smoke settings and mechanical reading rule, pinned to the final implementation bytes, the logger-parity receipt, the frozen scorer/statistics artifacts and the sealed protocol
  - evidence/fit/1632-smoke/{record.json,diagnostic.weights,attempt.json} — the one registered 20-step MPS-float32 run on gold 1632: 20/20 finite updates, five cadence entries, frozen scores and both comparators, Stage-0 TRAIN-only access, measured seconds-per-step 0.014265
  - 65-FINDINGS.md — the Phase 65 findings page: the retained reproduction, the measured cost and its exact basis, GAP-59-08 carried explicitly, the two reporting prohibitions flagged for review, and the owner-only items
affects: [phase-verification, phase-66-experiments, phase-67-experiments, owner-review]

actuals:
  tokens: 142121   # chars/4 over the realized diff 68adf979..HEAD (568,484 chars across 9 files, this SUMMARY excluded)
  tasks: 3
  commits: 7       # f7007b5e (test RED), 59647328 (feat GREEN), ac4358cb (evidence registration), b1dcacc4 (fix + re-pin), 84128fe2 (evidence run), bdc600fb (evidence findings), this SUMMARY commit; the state/roadmap docs commit follows

tech-stack:
  added: []
  patterns:
    - "Bounded-run registration discipline: a phase65-fit-registration/v1 pins the final implementation bytes, the committed logger-parity receipt and the frozen scorer/statistics artifacts; admission is metadata-only for check-registration and runs before the exclusive attempt claim, so an admission refusal never burns the claim"
    - "Synchronized completed-work timing: every segment wrapped in the MPS _synchronize helper with an injected monotonic clock; the rate denominator is the measured steps only, with warmup/logging/scoring/setup/data-load recorded separately and a different label for end-to-end seconds per completed step"

key-files:
  created:
    - .planning/phases/65-probe-on-the-record-fit-harness/65-SMOKE-PREDICTION.md
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/record.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/diagnostic.weights
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/attempt.json
    - .planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md
    - .planning/phases/65-probe-on-the-record-fit-harness/65-06-SUMMARY.md
  modified:
    - pinn/verification/diagnostic_fit.py
    - pinn/verification/diagnostic_guard.py
    - tests/phase65/test_fit_short.py

key-decisions:
  - "The fit registration reuses the shared committed-registration admission through a new fit-schema branch in diagnostic_guard (page, logger-parity receipt, probe result, code dependencies, frozen artifacts; no arms/weights), keeping the probe-schema path byte-identical — diagnostic_fit.py and diagnostic_guard.py therefore drift from the 65-05 probe registration's pins, the consequence 65-05 pre-routed to the owner (the probe result remains verifiable via its run-commit-based verify-result)"
  - "The receipt-faithfulness check verifies the logger-parity receipt against its own introducing commit (never rewritten after publication) plus the recorded run commit as ancestor, because the receipt was materialized after the probe run from the run's recorded entry (65-05's receipt provenance) — the first smoke attempt refused exactly here, before any claim, and the fix re-pinned the registration in the same commit (b1dcacc4)"
  - "The smoke proves mechanics and cost only: no E/tier threshold, no learnability or causal claim, no Phase 66-67 selection; the measured 0.014265 s/step is 18 steps of this exact configuration and is explicitly not steady-state throughput for other configurations"

patterns-established:
  - "Registered bounded runs claim their output exclusively (O_EXCL attempt beside the record), keep intermediate attempt status strictly inferior to a complete record, and mark interruption, cap expiry and non-finite updates as explicit incomplete — never retried, extended or resumed by the tooling"
  - "Supervised whole-run caps: deadline checks between phases and updates inside the worker plus a supervised subprocess join with graceful termination (SIGTERM then SIGKILL) as the hard backstop; caps at or above one hour refuse before data access"

requirements-completed: []   # DIAG-09 and INST-08 are declared by 65-05 and 65-06; per the repo convention the flips belong to the phase verification act. This plan completes INST-08(e) (the scored short run) and completes DIAG-09's and INST-08(a-d)'s evidence trail end to end.

coverage:
  - id: D1
    description: "The guarded bounded fit CLI: committed-fit-registration admission (settings agreement, sub-hour cap, MPS availability, run-commit-faithful logger-parity receipt) before any data or optimizer access; bounded synchronized timing with the measured-only denominator and the exact five-cadence smoke entries; exclusive attempt ownership with supervised-cap incomplete semantics; check-registration/run/verify-result surface"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_fit_short.py#FitRegistrationAdmissionTests (12 admission/refusal tests with zero data/optimizer-call spies)"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_fit_short.py#BoundedSynchronizedTimingTests (denominator, cadence, sync spy, phases, deadline, non-finite)"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_fit_short.py#AttemptOwnershipTests + FitCliSurfaceTests + VerifyResultTests + FitCheckRegistrationTests"
        status: pass
      - kind: integration
        ref: "command: python -B -m unittest tests.phase65.test_fit_short tests.phase65.test_isolation tests.phase65.test_contracts -v -> 131 tests OK"
        status: pass
    human_judgment: false
  - id: D2
    description: "The one registered smoke run: locked-12 on gold 1632 train stage 0, MPS float32 seed 42, 20/20 finite updates (2 warmup + 18 measured) within the 600 s cap, five cadence entries, frozen FEAS-01 score beside window-mean-constant and two-Kepler comparators on identical times/masses/body order, Stage-0 TRAIN-only access evidence, marked diagnostic weights and complete canonical record published exclusively"
    requirement: INST-08
    verification:
      - kind: integration
        ref: "command: python -B -m pinn.verification.diagnostic_fit run --registration .../smoke-registration.json --output .../1632-smoke/record.json -> FIT-RUN-COMPLETE, exit 0"
        status: pass
      - kind: integration
        ref: "command: python -B -m pinn.verification.diagnostic_fit verify-result --registration .../smoke-registration.json --result .../1632-smoke/record.json -> VERIFY-RESULT-OK, exit 0"
        status: pass
    human_judgment: false
  - id: D3
    description: "The findings page: the retained reproduction branch with counts, the measured cost and its exact basis for later budgeting, GAP-59-08 carried without adjudication, the two reporting prohibitions flagged for review, and the owner-only items preserved without changing scope"
    requirement: DIAG-09
    verification:
      - kind: integration
        ref: "command: python -B -m unittest discover -s tests/phase65 -p 'test_*.py' -v -> 203 tests, 202 OK; the single failure is the owner-routed 65-05 probe-registration digest drift for the two files this plan was mandated to edit"
        status: pass
      - kind: other
        ref: "command: load_protocol() -> PROTOCOL-OK (33 pinned digests unchanged); probe verify-result -> VERIFY-RESULT-OK (65-05 evidence still verifiable)"
        status: pass
    human_judgment: true
    rationale: "The page's interpretation discipline (mechanics vs inference separation, no-extrapolation wording, the two prohibitions as flagged-not-judged) is scientific-reporting judgment on prose; the verifier and owner review it as text"

duration: 40 min
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 06: Registered Smoke Fit & Measured Cost Summary

**One registered locked-12 fit of gold system 1632 completed 20/20 finite updates on MPS float32 within its 600-second cap and measured 0.014265 seconds per optimizer step (18 measured synchronized updates, warmup/logging/scoring excluded), closing INST-08(e) with the retained probe reproduction now backed by a scored, timed, exclusively-claimed run.**

## Performance

- **Duration:** 40 min (16:05–16:45 CDT approx; first commit 16:05:16, findings commit 16:41:24)
- **Started:** 2026-10-29T21:05Z (RED commit)
- **Completed:** 2026-10-29T21:45Z (close-out)
- **Tasks:** 3 of 3
- **Files:** 7 created, 3 modified

## Accomplishments

- **Task 65-06-01 (TDD) — the guarded bounded fit CLI, RED → GREEN → registration.** 34 new tests across six classes failed on the missing feature (RED `f7007b5e`, machine-verified `RED_EVIDENCE_OK`); the implementation added the `phase65-fit-registration/v1` admission (shared committed-registration gate via a new fit-schema branch in `diagnostic_guard`, settings agreement with the sealed registry, the sub-hour whole-run cap, MPS availability, and the committed run-commit-faithful logger-parity receipt) before any data or optimizer access, the bounded synchronized timing (2 warmup + 18 measured segments wrapped in the MPS `_synchronize` helper with an injected clock; `seconds_per_step` over the measured denominator only; warmup/logging/scoring/setup/data-load recorded separately; end-to-end label distinct; sync overhead and call count recorded), the exclusive attempt claim with explicit incomplete status, the supervised worker (deadline checks between phases and updates, plus a subprocess join with graceful SIGTERM/SIGKILL termination at the registered cap; 3600 s and above refuse before data access), `verify-result` without retraining, and the `check-registration` / `run` / `verify-result` CLI (GREEN `59647328`, 131 tests OK). The prediction page and registration were committed after the final code so every pinned digest matches (`ac4358cb`), and metadata-only `check-registration` printed `CHECK-REGISTRATION-OK registration-commit=ac4358cb…` with zero corpus or weight opens.
- **Task 65-06-02 — the registered smoke ran once and completed.** After one admission refusal that proved the gate fail-closed before any claim (deviation 1), the supervised run completed **20/20 finite updates** (2 warmup + 18 measured) on **MPS float32, seed 42**, on the Stage-0 training gold record `hierarchical/gold/1632` (split `train`, manifest stage 0, 1,001 samples, physical [0, 10]) within the 600-second cap (~5 s wall, ~2.72 s fit body). Similarity logged at steps 0/5/10/15/20 through the shared `measure_time_signal`; frozen FEAS-01 score beside the window-mean constant and two-Kepler comparators on identical times/masses/body order (network E 24.80 tier 0; constant E 1.1538 tier 0; two-Kepler E 0.9168 tier 0; loss final 0.0405 as context — no E/tier threshold imposed). Access evidence: exactly one corpus open (`hierarchical/gold/1632/train/stage0`), zero validation/test opens, clean attestation, 33 pinned digests. Marked `inst08-diagnostic` record + weights published exclusively (attempt running → published; `84128fe2`).
- **Task 65-06-03 — evidence verified, cost handed off.** `verify-result` printed `VERIFY-RESULT-OK` (exit 0) against the committed settings/weights/hashes; the full phase65 discovery ran 203 tests with **202 OK** and the single failure being the owner-routed 65-05 probe-registration digest drift (deviation 4); `load_protocol()` revalidated all 33 pinned digests (`PROTOCOL-OK`); the probe's own `verify-result` still passes (the 65-05 result remains verifiable). `65-FINDINGS.md` (`bdc600fb`) publishes the retained branch, the measured cost with its exact basis, GAP-59-08 carried explicitly, the two reporting prohibitions flagged for review, and the owner-only items.

## Task Commits

1. **Task 65-06-01 (RED):** `f7007b5e` — test(65-06): add failing tests for the guarded bounded fit cli
2. **Task 65-06-01 (GREEN):** `59647328` — feat(65-06): implement the guarded bounded synchronized diagnostic fit cli
3. **Task 65-06-01 (registration):** `ac4358cb` — evidence(65): commit the smoke prediction page and fit registration
4. **Task 65-06-02 (pre-run fix + re-pin):** `b1dcacc4` — fix(65-06): verify the parity receipt against its publication bytes
5. **Task 65-06-02 (run evidence):** `84128fe2` — evidence(65): record the registered 20-step system-1632 smoke run
6. **Task 65-06-03 (findings):** `bdc600fb` — evidence(65): publish the phase 65 findings and measured smoke cost

**Plan metadata:** this SUMMARY commit, then the state/roadmap docs commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_fit.py` — the guarded CLI, registration admission, bounded synchronized timing, attempt ownership, supervised cap, verify-result
- `pinn/verification/diagnostic_guard.py` — the fit-registration entries branch in the shared committed-registration admission (probe path unchanged)
- `tests/phase65/test_fit_short.py` — 35 new tests across six classes plus two shape-dependent pre-existing tests updated to the cadence-entries/steps-block record shape
- `.planning/phases/65-probe-on-the-record-fit-harness/65-SMOKE-PREDICTION.md` — the frozen settings and mechanical reading rule
- `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json` — the registration (sha256 `ba54e8124a33…` after the b1dcacc4 re-pin)
- `.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/{record.json,diagnostic.weights,attempt.json}` — the run's evidence
- `.planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md` — the findings page

## Decisions Made

- **The fit registration reuses the shared admission via a new schema branch** rather than a duplicated admission: `require_committed_registration` now admits `phase65-fit-registration/v1` alongside the probe schema (page, logger-parity receipt, probe result, code dependencies, frozen artifacts; no arms/weights). The probe-schema path is behaviorally unchanged.
- **Receipt faithfulness = publication bytes + run-commit ancestry.** The receipt was materialized after the probe run from the run's recorded entry, so no receipt bytes exist at the run commit; the check verifies the receipt against its own introducing commit and the recorded run commit as ancestor of HEAD.
- **The smoke's numbers are context, not verdicts.** The record and findings page impose no E/tier threshold; the 0.014265 s/step is bounded to this exact configuration with the not-steady-state caveat in the record's own basis strings.
- **No requirement flips:** DIAG-09/INST-08 stay open for the phase verification act, per the repo convention recorded in 65-05.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] The first smoke attempt refused: the receipt check demanded bytes at the run commit, which never existed there**
- **Found during:** Task 65-06-02, at the first `run` invocation (exit 2 before any claim; nothing created)
- **Issue:** `verify_logger_parity_receipt` (written this plan) compared the receipt's bytes to `git show <run-commit>:<receipt>`; the receipt was materialized after the probe run from the run's recorded entry (65-05's documented receipt provenance), so no receipt bytes exist at `22cee7d241f1`
- **Fix:** the check now verifies the receipt against its own introducing commit (byte-identical since publication) plus the recorded run commit as an ancestor; a `receipt_after_run` fixture kind and test pin the 65-05 shape as admitting; the registration re-pinned the corrected `diagnostic_fit.py` digest in the same commit so the committed settings match the final code (settings/cap/cadence/rule untouched)
- **Files modified:** `pinn/verification/diagnostic_fit.py`, `tests/phase65/test_fit_short.py`, `evidence/fit/smoke-registration.json`
- **Verification:** 131 tests OK; `check-registration` OK; the smoke then ran to completion
- **Committed in:** `b1dcacc4`

**2. [Owned-path extension] diagnostic_guard.py joined the owned paths**
- **Found during:** Task 65-06-01 GREEN
- **Issue:** the dispatch's owned-path list did not include `diagnostic_guard.py`, but the plan's "reuse require_committed_registration" with a fit-shaped registration requires a schema branch in the shared admission (the guard's own header designates it "shared with the fit harness")
- **Fix:** minimal additive branch; the probe-schema path is behaviorally identical; the extension was declared in every commit's `GIT_AGENT_OWNED_PATHS`
- **Files modified:** `pinn/verification/diagnostic_guard.py`
- **Verification:** all probe-side tests (72 in `test_probe.py`) pass unchanged except the pre-routed digest-drift item (deviation 4)
- **Committed in:** `59647328`

**3. [Rule 1 - Test bugs] Four test-fixture corrections during GREEN**
- **Found during:** Task 65-06-01 GREEN runs
- **Issue:** (a) the fixture recorded the receipt's run commit pre-`--amend`, orphaning it; (b) the worker test's setup simulated a pre-claim attempt that the real order (admission → claim → body) never produces; (c) the mid-run non-finite test returned a grad-less tensor, failing at `backward()` instead of the finiteness guard; (d) argparse's usage `SystemExit` escaped `main()` instead of returning 2
- **Fix:** (a) receipt committed in its own evidence commit before the registration; (b) the test now exercises the real post-claim refusal path; (c) the first call returns the real loss, the second the non-finite tensor; (d) `main` catches `SystemExit` and returns argparse's code
- **Files modified:** `tests/phase65/test_fit_short.py`, `pinn/verification/diagnostic_fit.py` (SystemExit catch only)
- **Verification:** full suite OK after each fix
- **Committed in:** `59647328`, `b1dcacc4`

**4. [Routed consequence - not fixed here] The 65-05 probe registration's digests drifted for the two files this plan mandates editing**
- **Found during:** Task 65-06-03 full-suite run
- **Issue:** `tests/phase65/test_probe.py::RegistrationContentTests::test_the_recorded_dependency_and_source_digests_match_disk` fails on exactly `diagnostic_fit.py` (`2e2c06eb5bb2` → `b00e45b460b8`) and `diagnostic_guard.py` (`d164bc4d1302` → `8dd577a263c2`) — the consequence 65-05 pre-routed to the orchestrator/owner ("any runner edit changes the pinned dependency digests — decide whether the probe registration is amended/re-committed or left historical")
- **Fix:** none taken: amending committed 65-05 evidence is the owner's registration-digest decision, and `test_probe.py` is outside this plan's owned paths. The test is correct about its subject. The probe's committed result remains verifiable (`verify-result` → `VERIFY-RESULT-OK`, historical-dependency mode), and the smoke registration pins the current implementation independently
- **Files modified:** none
- **Verification:** the drift was enumerated (exactly two entries; every other pinned artifact matches); recorded in `65-FINDINGS.md` §7 with the owner decision requested
- **Committed in:** documented in `bdc600fb`

**5. [Process - Runtime] Executor ran under the general-purpose runtime with the gsd-executor role definition**
- **Found during:** whole plan
- **Issue:** dispatched through the general-purpose agent runtime with the `gsd-executor` role definition loaded (role contract followed), not a named `gsd-executor` subagent type
- **Fix:** none needed; recorded honestly here and in the commit trailers
- **Files modified:** none
- **Committed in:** trailers on all six task commits

---

**Total deviations:** 5 (1 Rule-3 blocking fix with registration re-pin, 1 owned-path extension, 4 test-fixture corrections grouped as one Rule-1 item, 1 owner-routed consequence preserved, 1 runtime provenance note); no frozen or pinned module was edited, no framework-spec or roadmap change, no probe-registration amendment.
**Impact on plan:** the registered outcome is unaffected — the refusal happened before any claim and its fix made the admission faithful to the artifacts' actual provenance; every mechanical acceptance box of the prediction page is ticked by committed evidence.

## Issues Encountered

- The one non-passing test in the full discovery is the owner-routed digest-drift item (deviation 4), not a defect in this plan's deliverables; 202/203 pass and every task-level verify command passes.
- Cosmetic, pre-existing, left alone: `fit_diagnostic`'s `float(loss)` emits a torch `UserWarning` on requires-grad tensors (a 65-01-era pattern; harmless value read, out of scope).

## User Setup Required

None — everything ran in the local `pinn-train` environment with MPS available.

## Known Stubs

None — every delivered path is real: the CLI, admission, timing, cap, claim and verification are implemented and exercised; the smoke record is a complete canonical artifact.

## Next Phase Readiness

- **Phase 65 is complete pending verification.** DIAG-09's and INST-08's evidence is complete on disk; the requirement flips belong to the phase verification act.
- **For later planners (66-67):** the budget basis for this exact configuration is `duration_seconds ÷ 0.014265` steps plus the recorded fixed segments (logging 0.572 s at five-cadence, scoring 1.216 s, data load 0.254 s) — see `65-FINDINGS.md` §4. No other depth/width/rate/device is costed; longer diagnostics refuse at an hour until the governed pause/resume/power path is proven.
- **For the owner:** decide the 65-05 probe registration's amendment (two drifted dependency digests, listed in `65-FINDINGS.md` §7) and review the two flagged scientific-reporting prohibitions; the 65-05 routed runner defects remain queued unchanged.

## Self-Check: PASSED

All seven created files exist on disk; all six task commits (`f7007b5e`, `59647328`, `ac4358cb`, `b1dcacc4`, `84128fe2`, `bdc600fb`) are in history on `milestone/v2.5`; the smoke record is `status: complete` with 20/20 steps, five cadence entries, scores/comparisons, Stage-0 TRAIN-only access and the 33 digests; `verify-result` exits 0; `check-registration` reported the real ancestor commit `ac4358cb`; the 131-test task-01 verify gate and the 202/203 full discovery match the recorded outcomes; `git diff --check` clean at every commit; no pinned module changed (`PROTOCOL-OK`); the held-out evaluation remains unspent.

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*

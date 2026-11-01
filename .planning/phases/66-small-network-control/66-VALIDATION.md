---
phase: "66"
slug: "small-network-control"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-31"
---

# Phase 66 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

This is the execution validation contract for five plans and 14 tasks in waves 1-5,
seeded from `66-RESEARCH.md` ("Validation Architecture") and bound to the plan task
IDs. No planned test or real run has been executed during planning. Wave 0 below
names the test preparation inside Plans 66-01 and 66-02.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest` in the existing pinn-train environment |
| **Interpreter** | `<home>/miniforge3/envs/pinn-train/bin/python` |
| **Config file** | none (same convention as Phase 65; no framework installation) |
| **Quick run command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase66 -t .` |
| **Full suite command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -t .` then the quick run command |
| **Estimated runtime** | Phase 65 suite: 204 tests in 32.8 s (`65-CLOSEOUT.md` line 105), accepted as the single whole-suite regression gate. Phase 66 modules: unmeasured; expected under 30 s by analogy with the measured Phase 65 admission group (24 tests in 7.06 s). The Phase 66 discovery is a verify entry of its own, separate from the Phase 65 one (66-01 and 66-02 "Validation latency and counts"). |

---

## Sampling Rate

- **After every task commit:** Run the task's own `tests.phase66` module(s) listed below.
- **After every plan wave:** Run all of `tests/phase66` plus all of `tests/phase65`.
- **Before `/gsd-verify-work`:** Both suites green; `check-registration` and `verify-result` passing for the timing registration and all three experiment registrations and records; the timing-run `check-run` printing no score; and the page-then-registration-then-record ancestry checks (ORDER-OK, RUN-ORDER-OK) passing.
- **Max feedback latency:** 30 s per task module; the 32.8 s Phase 65 discovery is the accepted exception.

A synthetic test pass is not evidence that the small network fitted an orbit. Real
results come only from registered runs, launched through the AC-power and weekend
gate, whose prediction page was committed first.

---

## Per-Task Verification Map

All commands follow the interpreter `<home>/miniforge3/envs/pinn-train/bin/python -B`. Each PLAN task carries its complete command and an immediately following `<fails_when>`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 66-01-01 | 01 | 1 | EXP-01 / SC-1 | plan: T-66-01..04, T-66-06 | One synthetic run passes the AC gate, the registry door, the fit and the reading rule; battery refuses | tracer (unit) | `-m unittest tests.phase66.test_tracer -v`; Phase 65 discovery | ❌ W0 | ⬜ pending |
| 66-01-02 | 01 | 1 | EXP-01 / SC-1; Phase 65 preserved | plan: T-66-01..04, T-66-06 | Sealed `locked-12` REGISTRY untouched; every Phase 65 refusal holds; four unedited pins and the 11 evidence hashes unchanged; smoke identity at `84128fe2`; smoke `check-registration` exits 2 naming `diagnostic_fit.py` | unit + git + CLI | `-m unittest tests.phase66.test_catalog tests.phase66.test_admission tests.phase66.test_records tests.phase66.test_historical -v`; Phase 65 discovery and Phase 66 discovery as separate entries; PROTOCOL-OK | ❌ W0 | ⬜ pending |
| 66-02-01 | 02 | 2 | EXP-01 / SC-1 | plan: T-66-04..08, T-66-16 | AC gate fails closed on the exact `pmset` first line; weekend window (Saturday, or Sunday before 22:00 America/Chicago) refuses weekdays | unit (fakes) + live read | `-m unittest tests.phase66.test_power -v`; live `diagnostic_power check` agreement | ❌ W0 | ⬜ pending |
| 66-02-02 | 02 | 2 | EXP-01 / SC-2, SC-3 | plan: T-66-04..08, T-66-16 | Branch labels (tier1, near, between, unsettled, other) and the improvement check are mechanical; `confirmed` only when all three runs share tier1 or near; `unsettled` always routes to the owner | unit | `-m unittest tests.phase66.test_reading_rule -v`; inline READING-RULE-OK | ❌ W0 | ⬜ pending |
| 66-02-03 | 02 | 2 | EXP-01 / SC-1 | plan: T-66-04..08, T-66-16 | Budget set by time alone under the one-hour cap; bounded loss-trace stride keeps every record under the 10 MiB commit policy at any length; frozen design block | unit + static | `-m unittest tests.phase66.test_budget tests.phase66.test_pages -v`; Phase 65 discovery and Phase 66 discovery as separate entries; DESIGN-OK; PROTOCOL-OK | ❌ W0 | ⬜ pending |
| 66-03-01 | 03 | 3 | EXP-01 / SC-1 | T-66-09, T-66-18 | Timing page freezes the scientific design and rules before any run; timing registration admits | static + CLI | `-m unittest tests.phase66.test_pages -v` (TimingPageTests); `check-registration` on the timing registration | ❌ W0 / executor-run | ⬜ pending |
| 66-03-02 | 03 | 3 | EXP-01 / SC-1 | plan: T-66-06, T-66-09, T-66-10, T-66-17, T-66-18 | Timing calibration runs once through the gate; its score is never read | CLI | `verify-result` on the timing record; `check-run` prints EXP01-CHECK-OK and no score | executor-run (AC, weekend) | ⬜ pending |
| 66-03-03 | 03 | 3 | EXP-01 / SC-1 | plan: T-66-06, T-66-09, T-66-10, T-66-17, T-66-18 | Prediction page with the measured budget committed before the first experiment run; three registrations admit | static + CLI + git | `-m unittest tests.phase66.test_pages -v` (PredictionPageTests, ExperimentRegistrationTests); CHECK-ALL-OK; ORDER-OK | ❌ W0 / executor-run | ⬜ pending |
| 66-04-01 | 04 | 4 | EXP-01 / SC-2 | plan: T-66-06, T-66-09..12 | Main run 1632/seed 42 verifies against its registration | CLI | `verify-result`; `check-run` prints EXP01-CHECK-OK and no score | executor-run (AC, weekend) | ⬜ pending |
| 66-04-02 | 04 | 4 | EXP-01 / SC-2 | plan: T-66-06, T-66-09..12 | Second-panel repeat 851/seed 42 verifies | CLI | `verify-result`; `check-run` prints EXP01-CHECK-OK and no score | executor-run (AC, weekend) | ⬜ pending |
| 66-04-03 | 04 | 4 | EXP-01 / SC-2 | plan: T-66-06, T-66-09..12 | Second-seed repeat 1632/seed 41 verifies; evidence order holds for all three | CLI + git | `verify-result`; CHECK-RUNS-OK (`check-run` on all three, never `read-run`); RUN-ORDER-OK | executor-run (AC, weekend) | ⬜ pending |
| 66-05-01 | 05 | 5 | EXP-01 / SC-2, SC-3 | plan: T-66-13..15 | `66-RESULT.md` derives the branch mechanically from the committed records | CLI + static | RESULT-PAGE-OK (page compared with a fresh `review`) | executor-run | ⬜ pending |
| 66-05-02 | 05 | 5 | EXP-01 / SC-3 | plan: T-66-13..15 | Owner checkpoint ①: blocking human decision, never auto-approved | manual | none (owner's answer) | manual | ⬜ pending |
| 66-05-03 | 05 | 5 | EXP-01 / SC-3 | plan: T-66-13..15 | `66-CHECKPOINT-1-RULING.md` records the owner's words verbatim and the branch taken | static | RULING-OK | executor-run | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

Phase artifacts named by the plans: `66-TIMING-PREDICTION.md`, `66-PREDICTION.md`,
`66-RESULT.md` and `66-CHECKPOINT-1-RULING.md`. `66-REVIEW.md` stays reserved for the
code-review artifact.

---

## Wave 0 Requirements

- [ ] `tests/phase66/__init__.py`, `test_tracer.py`, `test_catalog.py`, `test_admission.py`, `test_records.py`, `test_historical.py` (Plan 66-01)
- [ ] `tests/phase66/test_power.py`, `test_reading_rule.py`, `test_budget.py`, `test_pages.py` (Plan 66-02)
- [ ] `pinn/verification/diagnostic_phase66.py` and `pinn/verification/diagnostic_power.py`, created test-first; the `pinn/verification/diagnostic_fit.py` extension edited test-first
- [ ] No framework install; no change to `tests/phase65`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Owner's answer at checkpoint ①, including any SCOPE-49 proposal | EXP-01 / SC-3 | A reserved owner decision (66-CONTEXT D-01, D-12) | Task 66-05-02: present `66-RESULT.md`; record the owner's verbatim answer in `66-CHECKPOINT-1-RULING.md` (task 66-05-03) |
| Mac on AC power inside the weekend window for each launch | EXP-01 / SC-2 | The owner's compute window (66-CONTEXT D-08) | The launch gate refuses on battery or outside the window; the operator plugs in during the weekend and relaunches (tasks 66-03-02, 66-04-01..03) |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s per task module (Phase 65 discovery accepted at 32.8 s)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending (set by validate-phase)

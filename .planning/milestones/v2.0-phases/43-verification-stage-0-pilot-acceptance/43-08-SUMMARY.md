---
phase: 43-verification-stage-0-pilot-acceptance
plan: 08
subsystem: verification-acceptance
tags: [acc-06, verdict, held-out-evaluation, owner-signoff, handoff, honesty]
status: complete
requires:
  - phase: 43-02
    provides: "receipt-bound one-time held-out evaluator and strict post-v1.3 physics gate"
  - phase: 43-05
    provides: "post-receipt completed-run summary refresh"
  - phase: 43-06
    provides: "real interrupt/resume smoke timing and owner-ratified operational seams"
  - phase: 43-07
    provides: "three-seed pilot calibration, confidence limits, and owner-ratified thresholds"
provides:
  - "Sole held-out evaluation receipt recording FAIL at eps_H 237.2086056078468 / SCS 2.3751304405952904 over 1,500 trajectories"
  - "Owner-authored 2026-07-22 adjust verdict that retains the mechanical Stage-0 slice while blocking full-platform expansion"
  - "Forward shipped/seam/deferred inventory with GAP-38-01 disposition and PLAT-01..07 left unimplemented"
affects: [milestone-v2.0-closeout, future-validation-investigation, future-platform-decision]
tech-stack:
  added: []
  patterns:
    - "Receipt-grounded owner verdicts keep empirical gate evidence separate from owner judgment"
    - "A FAIL gate cannot become an unqualified go; later held-out use requires a new owner-governed evidence boundary"
key-files:
  created:
    - .planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md
    - pinn/STATUS.md
    - tests/phase43/test_verdict_grounding.py
  modified:
    - pinn/evaluate.py
    - pinn/verification/gate_metrics.py
    - tests/phase43/test_evaluate_gate.py
    - tests/phase43/test_gate_boundary.py
key-decisions:
  - "Owner verdict (2026-07-22): adjust — retain the demonstrated mechanical Stage-0 slice, block full-platform expansion, and investigate the failed physics gate plus non-convergent/noisy behavior without claiming the remedy is known."
  - "The evaluator invocation budget is exhausted after two documented failures and one final completed FAIL receipt; no rerun is authorized under the current policy."
patterns-established:
  - "Owner sign-off is stored as an exact verdict, matching owner_decision, and an ISO calendar date in parser-checked frontmatter."
requirements-completed: [ACC-06]
coverage:
  - id: D1
    description: "The single held-out receipt, preserved metrics and refreshed summary ground a FAIL-qualified milestone verdict without another evaluator invocation."
    requirement: ACC-06
    verification:
      - kind: unit
        ref: "tests/phase43/test_verdict_grounding.py#test_current_verdict_is_receipt_seed_timing_and_seam_grounded"
        status: pass
      - kind: other
        ref: "shasum -a 256 runs/stage0-pilot-seed42/evaluation/{evaluation-receipt.json,metrics.json,metrics.md} runs/stage0-pilot-seed42/{summary.json,summary.md}"
        status: pass
    human_judgment: false
  - id: D2
    description: "The owner rendered adjust on 2026-07-22: retain the mechanical Stage-0 slice, block full-platform expansion, and route investigation without assuming a known remedy."
    requirement: ACC-06
    verification:
      - kind: unit
        ref: "tests/phase43/test_verdict_grounding.py#test_owner_adjust_decision_and_dated_sign_off_are_persisted"
        status: pass
    human_judgment: true
    rationale: "The exact verdict is an owner judgment supplied at the blocking decision checkpoint; automation verifies faithful persistence but cannot replace the judgment."
  - id: D3
    description: "The FUT-01/FUT-04 forward handoff distinguishes shipped slice, explicit seams/placeholders, and deferred PLAT-01..07 while recording GAP-38-01 as resolved."
    requirement: ACC-06
    verification:
      - kind: manual_procedural
        ref: "pinn/STATUS.md shipped/seams/deferred table review"
        status: pass
    human_judgment: true
    rationale: "The inventory is a scope and handoff review; its correctness depends on comparing the prose taxonomy with the milestone boundary."
duration: 1h
completed: 2026-07-22
---

# Phase 43 Plan 08: Receipt-Grounded Owner Verdict and Handoff Summary

**The sole held-out evaluation produced an unequivocal FAIL, and the owner rendered `adjust`: keep the proven mechanical Stage-0 slice, block full-platform expansion, and investigate the physics-gate failure and non-convergent behavior without claiming a known remedy.**

## Performance

- **Duration:** ~1 hour
- **Started:** 2026-07-22T11:42:04Z
- **Completed:** 2026-07-22T12:39:43Z (owner-verdict task commit)
- **Tasks:** 2
- **Files modified:** 7 task artifacts

## Accomplishments

- Completed the final authorized held-out invocation once and preserved its receipt-grounded `FAIL`: `eps_H = 237.2086056078468`, `SCS = 2.3751304405952904`, and 1,500 trajectories, with unchanged artifact hashes recorded in the verdict.
- Persisted the exact owner-authored `adjust` decision and 2026-07-22 sign-off while retaining the full seed/timing/seam evidence, qualifications, and both prior failed-invocation audit entries.
- Closed the forward handoff with shipped, seam/placeholder, and deferred columns; the mechanical Stage-0 slice remains available, but Stage 1 and PLAT-01..07 remain blocked.

## Task Commits

1. **Task 1 repair: thread frozen blacklist configuration into the evaluator** — `a136cd36` (fix)
2. **Task 1 repair: transfer gate tensors to CPU before float64 conversion** — `9ffbd561` (fix)
3. **Task 1: preserve the final receipt, evidence draft, handoff, and grounding tests** — `0d20e187` (evidence)
4. **Task 2: persist the exact owner adjust verdict and dated sign-off** — `574d699` (evidence)

**Plan metadata:** this closeout commit (`docs(43-08): complete owner verdict plan`).

## Files Created/Modified

- `.planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` — receipt-grounded FAIL evidence, complete invocation audit, and exact dated owner `adjust` sign-off.
- `pinn/STATUS.md` — forward shipped/seam/deferred inventory and final owner-verdict status.
- `tests/phase43/test_verdict_grounding.py` — parser-level citation, FAIL+go rejection, decision/date, and qualification checks.
- `pinn/evaluate.py` — evaluator blacklist-path composition repair required before the final invocation.
- `tests/phase43/test_evaluate_gate.py` — synthetic regression for resolved evaluator blacklist wiring.
- `pinn/verification/gate_metrics.py` — supported-dtype MPS-to-CPU transfer before float64 gate calculation.
- `tests/phase43/test_gate_boundary.py` — structural, CPU, and real-MPS conversion regressions.

## Decisions Made

- **Owner verdict — `adjust` (2026-07-22):** retain the demonstrated mechanical Stage-0 slice; do not authorize the full multi-stage platform; route a separately governed investigation into the physics-gate failure and non-convergent/noisy pilot behavior. The remedy is not represented as known.
- **Held-out boundary:** the evaluator budget is exhausted. The two failures and the one final completed invocation remain explicit; any later held-out evaluation requires a new owner policy and separate evidence boundary.
- **Scope:** no evaluator rerun, training remediation, Stage 1 work, or PLAT-01..07 implementation is part of this closeout.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Threaded the configured blacklist path into held-out adapter construction**
- **Found during:** Task 1, evaluator attempt 1
- **Issue:** Adapter construction refused before held-out split access because `config.data.blacklist_path` was not passed through the evaluator composition root.
- **Fix:** Reused the training resolver and passed the frozen resolved path to `AdmittedSetAdapter`; added a synthetic regression without invoking held-out data.
- **Files modified:** `pinn/evaluate.py`, `tests/phase43/test_evaluate_gate.py`
- **Verification:** focused evaluator tests passed before retry.
- **Committed in:** `a136cd36`

**2. [Rule 1 - Bug] Moved supported-dtype tensors to CPU before the float64 gate cast**
- **Found during:** Task 1, evaluator attempt 2
- **Issue:** MPS rejected direct tensor conversion to float64 during gate-metric calculation after predictions had likely been processed.
- **Fix:** Detached and transferred tensors to CPU in their supported dtype, then cast to float64; formulas and thresholds stayed unchanged.
- **Files modified:** `pinn/verification/gate_metrics.py`, `tests/phase43/test_gate_boundary.py`
- **Verification:** structural, CPU, and real-MPS regression coverage passed; the final authorized invocation then completed once.
- **Committed in:** `9ffbd561`

---

**Total deviations:** 2 auto-fixed (1 blocking configuration repair, 1 metric-conversion bug).
**Impact on plan:** Both repairs were narrowly required to obtain the single governed receipt. Neither changed the held-out split, checkpoint choice, metric formulas, gate thresholds, training state, or platform scope.

## Issues Encountered

- The evaluator had two failed invocations before the one final completed invocation. Attempt 1 failed before held-out split access; Attempt 2 failed during MPS gate-metric conversion after held-out records and predictions were likely processed. Both remain preserved in the verdict audit and are not rewritten as no-access attempts.
- The final gate result is `FAIL`, not a tool failure: the reported energy drift is approximately 23.7 million times the `1e-5` acceptance threshold. The owner chose `adjust` with that qualification intact.
- The known broader baseline remains non-green for previously documented Phase-39/41/42 fixture issues. This plan neither reran nor claimed to repair those unrelated failures.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ACC-06 is closed by the owner-authored `adjust` decision.
- The Stage-0 mechanical slice is retained for investigation; full-platform expansion is blocked.
- Any remediation plan or renewed held-out evaluation requires separately authorized work. This plan does not start that work.
- Phase-level verification remains the execute-phase orchestrator's responsibility and was intentionally not run here.

## Known Stubs

- `pinn/STATUS.md` intentionally names placeholder seams for stochastic L-BFGS, RAD, Tier-3 remediation, streaming residency, and auto-revert. These are explicit PLAT-02..07 deferrals, not incomplete ACC-06 implementation; the `adjust` verdict keeps them blocked.
- The empty list initializers found in `pinn/evaluate.py` are runtime accumulators, not UI/reporting placeholders.

## Self-Check: PASSED

- `43-08-SUMMARY.md`, `43-VERDICT.md`, `pinn/STATUS.md`, and `tests/phase43/test_verdict_grounding.py` exist on disk.
- Commits `a136cd36`, `9ffbd561`, `0d20e187`, and `574d699` exist in git history.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verdict_grounding -v` — 4/4 pass.
- SHA-256 identities for the receipt, metrics, and refreshed summaries exactly match the values preserved in `43-VERDICT.md`.
- `requirements.mark-complete ACC-06` updated both the checkbox and traceability table.
- No evaluator command, remediation, Stage 1 work, PLAT implementation, phase-level verification, network endpoint, auth path, or schema mutation was introduced during Task 2/closeout.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*

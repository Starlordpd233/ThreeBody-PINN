---
phase: 57-corrected-re-run-the-preserved-evaluation
verified: 2026-10-03T17:14:58Z
status: passed
score: 4/5 success criteria met; SC3 unmet through the declared terminal branch (SC5)
verifier: executing agent (claude-code/claude-opus-5-5); not an independent gsd-verifier pass
head: 8363af14362dc7613347f354ab92322130a49188
behavior_unverified: 0
overrides_applied: 1
overrides:
  - must_have: "SC3 — Stage-0 runs end-to-end under the corrected recipe with the causal front actually advancing within the re-ratified window, and the three-seed band re-established"
    reason: "Generation-7 graded seed 42 tripped invariant B at step 951 (frozen-monitor high-water 2 since step 450; 501 > N=500). Seeds 41/43 were not launched. ROADMAP Phase 57 SC5 and Phase 58 SC3 declare this branch in advance: the evaluation is preserved unspent and the phase closes there. SC3 is recorded as not met, not as passed."
    accepted_by: "ROADMAP declared terminal state (SC5) and the owner's closeout instruction of 2026-10-03"
    accepted_at: "2026-10-03"
human_verification: []
---

# Phase 57: Corrected Re-Run & the Preserved Evaluation — Verification Report

**Phase goal:** Stage-0 is re-run under the corrected recipe and — only if it
actually trains — the single preserved held-out evaluation is spent, once, on a
seed fixed before anyone saw a result.

**Verified:** 2026-10-03T17:14:58Z at HEAD `8363af14`
**Status:** passed on the declared terminal branch. The recipe did not keep the
causal front advancing, and the evaluation was correctly not spent.

## Method note

The agent that executed 57-05 and 57-06 wrote this report, so it is not an
independent verification. To compensate, every check below was re-run fresh at
HEAD `8363af14` rather than cited from earlier output. SUMMARY claims were
treated as allegations. A separate gsd-verifier pass can be requested if
independent confirmation is wanted.

## Success criteria

| # | Criterion | Verdict | Evidence (fresh at `8363af14`) |
|---|---|---|---|
| SC1 | Checkpoint ③ discharged before any run; wired into config and checkpoints | **MET** | `57-RULING.md` `status: ratified`, `pre_registered_at: 2026-09-08T02:05:10Z` (N=500, one frozen training-only monitor, frozen L-BFGS segment). `configs/stage0-v23g7-seed42.yaml` `front_advance_window_n: 500`. Every generation-7 checkpoint carries `front_monitor` and `invariant_b_state`, and the trip record reports `threshold: 500.0`, `threshold_provisional: false`. |
| SC2 | Checkpoint ④ pre-registers seed 42 (fallback 41, 43) before any result | **MET** | `57-RULING.md` lines 24, 129 (dated 2026-09-08). The generation-7 runs started 2026-10-03. `no-candidate.json` was written without reading any metric. |
| SC3 | Front actually advances within the window, and the three-seed band is re-established | **NOT MET** (terminal branch) | The frozen-monitor front advanced 0→1 (smoke, step 93) and 0→2 (graded seed 42, by step 450), then did not advance for 501 steps. The guard tripped at step 951 (`runs/stage0-v23g7-seed42/failure/trip.json`). Seeds 41/43 were not launched. |
| SC4 | No `η_c`, `R̄` normalization, `ω₀`, or `N_t` adjusted against a result (SCOPE-37) | **MET** | `git diff 87e50573..HEAD` shows no change to `framework-specs/`, `pinn/verification/artifacts/r_ref_stage0.json`, or `pinn/constants.py`. The `pinn/` diff touches no recipe constant (memory bounding, telemetry, plumbing only). Gen-7 configs differ from gen-6 only in `run.run_name`. `admit-run-window` now fails closed, so no further window can open. |
| SC5 | Evaluation spent exactly once after preconditions, or the terminal branch preserves it unspent | **MET** (terminal branch) | `terminal-state.json` (`invariant_b_halt_no_advance`, `evaluation: preserved-unspent`) and `no-candidate.json` are bound to it by SHA-256. Verifier: `run-window` → `RUN-WINDOW-TERMINAL-OK`, `candidate` → `CANDIDATE-OK`, `pre-evaluation` → `PRE-EVALUATION-UNSPENT-OK`, `final` → `FINAL-UNSPENT-OK`. No `evaluation/` directory, receipt, or readiness file exists anywhere under `runs/stage0-v23g*`. |

## Supporting checks

| Check | Result |
|---|---|
| `python -m unittest discover -s tests/phase57 -t .` | 107 tests OK, 1 platform skip, 215.5 s |
| `python -m unittest tests.git_policy.test_git_policy` | 35 tests OK |
| `verify_phase57_evidence.py admit-run-window` | exit 1, fail-closed (`target run directory already exists`): re-admission correctly refused |
| Generation-6 and generation-7 retention | Re-derived inside `run-window` from Git and disk: 49 and 67 files |
| `seed42-setup` during the window | `SEED42-SETUP-OK`: identical `splits.json` bytes (`5846ae5b…`), `s_h`, and `n_train` |

## Requirement status (not changed here)

RUN-04 (front actually advancing), RUN-05 (three-seed band), and EVAL-02 (spend
the evaluation) are not satisfied. The terminal branch closed the phase without
them. In v2.2 the matching dispositions ("closed incomplete" or "not attempted")
were owner decisions, so `REQUIREMENTS.md` is left unchanged and the
dispositions go to the Phase-58 owner verdict (checkpoint ⑤).

## Known issues

- All 33 `tests/phase50` failures predate this phase. The archived Phase-50
  scripts and their tests hardcode `.planning/phases/50-valid-stage-0-re-run/`
  and derive the repository root from their own location, and both broke when
  the folder moved to `.planning/milestones/v2.2-phases/` in `12e16d7b`. Fixing
  them means editing archived historical evidence (deferred by 57-04).
  57-VALIDATION C13/C17 cannot run until that is decided.
- 57-05-PLAN prose names the terminal reason `invariant-b-no-advance`. The
  verifier accepts only `invariant_b_halt_no_advance`, which was used.

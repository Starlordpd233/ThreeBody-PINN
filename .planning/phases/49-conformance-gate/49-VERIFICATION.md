---
phase: 49-conformance-gate
verified: 2026-08-11T06:56:13Z
status: passed
score: 6/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 4/6
  gaps_closed:
    - "An EVAL-01-eligible run enforces invariant B with the owner-ratified N = 500; an N-unset run remains ineligible."
    - "EVAL-01 eligibility can be true only when the artifact proves the run-start PHYS-05 table and census actually executed."
  gaps_remaining: []
  regressions: []
---

# Phase 49: Conformance Gate Verification Report

**Phase Goal:** A preflight + runtime gate exists that makes an invalid run structurally unable to spend the single look — the minimum enforcement subset (GATE-01 locked PHYS-05 table assertion, GATE-02 placeholder census, GATE-03 runtime invariants, INST-03 known-divergence register), wired into run start and stage boundary with the eval01_precondition_i eligibility projection.

**Verified:** 2026-08-11T06:56:13Z

**Status:** passed

**Re-verification:** Yes — after gap closure (plan 49-09, commit 93bdac47; independent review 7562eef6)

## Goal Achievement

Both prior gaps sat at one seam — translating real gate evidence into the EVAL-01 precondition-(i) fact — and both are now closed by production code plus named, permanent disconfirmation regressions, each independently re-probed by this verifier against the shipped tree. The owner-ratified N = 500 path remains eligible. All six must-have truths hold with fresh behavioral evidence.

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | The full PHYS-05 per-stage table is asserted at run start and every stage boundary. | ✓ VERIFIED | `pinn/conformance/table.py` untouched by the closure wave (`git diff --stat 8727d1a3..7562eef6` empty) and free of tolerance constructs. Regression spot-check: `test_run_start_writes_passed_preflight_artifact`, `test_controller_stage_boundary_events_follow_entered_order`, `test_stage2_fails_without_rebound_scheduler` → 3 passed. Fresh real-main probes show the run_start event carrying all locked table checks passed in both the N-unset and N=500 runs. |
| 2 | The placeholder census resolves every required loss quantity through concrete producers or blocks/names an explicit waiver. | ✓ VERIFIED | `pinn/conformance/census.py` untouched by the closure wave. Spot-check: `test_census_passes_with_real_manifest_and_validated_metadata`, `test_placeholder_blocks_without_explicit_waiver` → 2 passed. Both fresh real-main runs show `census verdict: passed`; a blocked/null/`"Passed"`-verdict census now yields ineligibility (probes 4 and 7). |
| 3 | Runtime invariants fail loud and early, including front advancement within the owner-ratified N for every eligible run. | ✓ VERIFIED (was FAILED — GAP A closed) | Fresh real-main probe: `run.invariants: {}` → exit 0, run_start passed, exactly one run-local `INV-B-N-UNSET` record `(divergence, open, proof_test None)`, advisory `invariant_b_window` check `(actual None, passed False)`, `eval01_precondition_i: False`. N=500 run → no run-local record, `invariant_b_window (actual 500, passed True)`, `eval01_precondition_i: True`. Named regression `test_real_main_with_n_unset_is_structurally_ineligible` asserts exactly this and passed. Guard-trip/resume spot-checks: invariant-A trip, invariant-B trip, stripped-stats HALT, resume continuity → 4 passed. |
| 4 | The known-divergence register is maintained and every open entry is surfaced in the run record. | ✓ VERIFIED | Register byte-identical across the closure wave: 16 entries, 1 `INV-B-N-UNSET` globally `closed` with proof test, 3 open entries all `kind: qualification` (CONF-01-QUALIFICATION, I_WARM-INTEGER-FLOOR, COLLOCATION-COUNT-HARD-CODE). Spot-check: composition, run-record surface, closure-proof meta-test, gate-key collision → 4 passed. N=500 probe confirms open qualifications travel without stranding eligibility (D-23/D-26). |
| 5 | The SCOPE-32 coordination decision is recorded without duplicating the charter's general regime. | ✓ VERIFIED | `49-CONTEXT.md` D-31/D-32 intact; the workstream directory `docs/work/designs/cross_cutting/training-verification-regime/` still contains only the charter. The predicate lives behind the `pinn/conformance/` module boundary (`summary.py` delegates; D-32). |
| 6 | Eligibility proves the required run-start gate actually ran; a shaped but incomplete artifact cannot claim conformance. | ✓ VERIFIED (was FAILED — GAP B closed) | Fresh probes: `stage_boundary`-only passed artifact with `census: null` → `ValueError: preflight assertion history must begin with a run_start event` at load and `_eval01_precondition_i: False`. Complete honest artifact → eligible. Missing one required check, blocked census, hollow second run_start in a resume history, case-variant `"Passed"` verdict → all False. Legal two-run_start resume history → True (D-17 preserved). Named regression `test_stage_boundary_only_history_is_refused_at_load` passed. |

**Score:** 6/6 truths verified (0 present, behavior-unverified)

### Gap Re-Adjudication

| Gap | Prior State | Probe Result | Disposition |
|---|---|---|---|
| GAP A (truth 3): N-unset real-main run reported eligible | FAILED — run-local record absent, flag True | Re-probed disconfirmingly on the shipped tree: exit 0, open run-local `INV-B-N-UNSET` divergence in the run_start event, failed advisory `invariant_b_window` check, `eval01_precondition_i` False; N=500 path still True | **CLOSED** — named regression `test_real_main_with_n_unset_is_structurally_ineligible` would catch re-opening (asserts record presence, openness, and the False flag) |
| GAP B (truth 6): stage_boundary-only artifact reported eligible | FAILED — loaded, predicate True | Re-probed disconfirmingly: refused at load with ValueError naming the ordering rule; predicate False | **CLOSED** — named regression `test_stage_boundary_only_history_is_refused_at_load` would catch re-opening (`pytest.raises(ValueError, match="run_start")` plus the False flag) |

## Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn/constants.py` | Canonical seven-stage PHYS-05 literals | ✓ VERIFIED | Untouched by closure wave; consumed by `table.py`. |
| `pinn/conformance/table.py` | Exact table assertion | ✓ VERIFIED | Untouched; no `isclose`/`allclose`/`abs(` tolerance. |
| `pinn/conformance/preflight.py` | Atomic fail-closed evidence spine + run-local N binding + single eligibility predicate | ✓ VERIFIED | Prior PARTIAL resolved: `_run_local_invariant_window` is the only attribute read of the window (line 471, delegating to `guards._extract_invariant_window`; all other occurrences are string literals); `_invariant_b_window_check` inserted before the census append in both branches (census stays terminal); `_run_local_n_unset_divergence` appended once after register-derived opens; `_assert_history_ordering` enforced at load (376) and write (309), deliberately absent from single-record validation; `evaluate_eval01_precondition_i` (549–602) requires first-event run_start, every required name present with all occurrences passed, exact `verdict == "passed"` census equality, and zero open divergences. |
| `pinn/conformance/census.py` | Explicit producer-backed placeholder census | ✓ VERIFIED | Untouched; pass/block behavior spot-checked green. |
| `pinn/conformance/register.py` and `divergence_register.json` | Validated divergence register with proof-backed closure | ✓ VERIFIED | Untouched; 16 entries validated; closure-proof meta-test passed. |
| `pinn/training/guards.py` | Invariants A/B and missing-stat HALTs | ✓ VERIFIED | Untouched; `_extract_invariant_window` (104–124) is the ONE accessor, with the duck-typed fallback chain and positive-int validation. |
| `pinn/training/checkpoint.py` and `pinn/training/controllers.py` | Invariant-B state persistence and stage-boundary dispatch | ✓ VERIFIED | Resume-continuity and boundary-ordering spot-checks passed. |
| `pinn/training/summary.py` | Verbatim conformance projection and fail-closed EVAL-01 fact | ✓ VERIFIED | Prior PARTIAL resolved: `_eval01_precondition_i` (362–380) null-checks the path, then loads and delegates to `preflight.evaluate_eval01_precondition_i` inside the existing broad fail-closed boundary (never raises). |
| `pinn/train.py` | Production composition root | ✓ VERIFIED | `run_start_preflight` (1193) creates the recorder and writes run_start before any stage-boundary append (985/1000, via the post-preflight `conformance_hook`). |
| `tests/phase49/test_e2e_seam.py` | Real synthetic `main()` ordering seam + GAP-A regression | ✓ VERIFIED | Both tests read in full: the GAP-A regression drives real `main()` with `run.invariants: {}` and asserts exit 0, exactly one open run-local divergence, and `eval01_precondition_i is False`; the happy-path assertion `is True` is byte-identical (zero diff lines, confirmed by review). |
| `tests/phase49/test_preflight_integrity.py` | GAP-B regression + eligible-baseline control + discriminating negatives | ✓ VERIFIED | Read in full: `_event` default is a complete honest run_start; `test_stage_boundary_only_history_is_refused_at_load` asserts the load-time ValueError and the False flag; the control `test_complete_run_start_artifact_is_eligible` keeps every negative discriminating (D-16). |

## Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `pinn/constants.py` | `pinn/conformance/table.py` | `PHYS05_*` imports, exact equality | ✓ WIRED | Unchanged; no tolerance constructs. |
| `pinn/conformance/table.py` | `pinn/train.py` / `pinn/training/controllers.py` | run-start call and stage-boundary closure | ✓ WIRED | Spot-checks passed. |
| `pinn/conformance/census.py` | real `RunController` producers | `run_start_preflight(..., controller=run_controller)` | ✓ WIRED | Fresh real-main runs produced `verdict: passed` censuses. |
| `run.invariants.front_advance_window_n` | `StepGuards` AND preflight | single accessor `_extract_invariant_window` | ✓ WIRED | Single-seam contract confirmed by inspection: one attribute read site in `preflight.py`; guard and preflight views cannot diverge. Shipped N=500 config now reports `config_value: 500` (named test passed); the `preflight.py:384` anti-pattern is closed at its root. |
| `StepGuards` | checkpoint payload | `invariant_b_state_dict` / restore | ✓ WIRED | Resume-continuity spot-check passed. |
| divergence register | `preflight.json` | `load_divergence_register` → run-start `open_divergences` | ✓ WIRED | Register-derived opens first, run-local record appended at a deterministic terminal position (named ordering/idempotency tests passed). |
| `preflight.json` | EVAL-01 precondition (i) | `evaluate_eval01_precondition_i` via fail-closed summary delegation | ✓ WIRED — FAIL-CLOSED | Prior NOT_FAIL-CLOSED resolved: seven fresh probes show False on hollow, missing, malformed, blocked, case-variant, and open-divergence inputs; True only on complete honest artifacts. |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| PHYS-05 assertion | scheduler state | live `ScheduledWeights.state_dict()` | Yes | ✓ FLOWING |
| Census | 28 manifest quantities | live config/metadata/controller producers | Yes | ✓ FLOWING |
| Runtime invariants | `w_n_stats`, `front_idx`, `n_colloc` | controller loss details → `guard_hook` → `StepGuards.check` | Yes | ✓ FLOWING |
| Invariant-B resume state | initialized/high-water/last-advance | `StepGuards` → checkpoint schema v2 → restore | Yes | ✓ FLOWING |
| Run record | `conformance`, `eval01_precondition_i` | validated `preflight.json` through the tightened predicate | Yes | ✓ FLOWING — prior HOLLOW seam resolved: the predicate now requires the evidence it summarizes |
| N/register consistency | `front_advance_window_n` | real `TrainingConfig.run.invariants` via the single accessor | Yes | ✓ FLOWING — prior MISREAD resolved: N=500 reports `config_value: 500`; N-unset reports an honest `None` disagreement finding against the closed register |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Complete Phase 49 suite | `.venv/bin/python -m pytest -q tests/phase49` | `190 passed in 12.68s` (176 baseline + 14 new) | ✓ PASS |
| All 15 new named gap-closure regressions | `.venv/bin/python -m pytest -q <15 node IDs>` | `15 passed in 3.15s` | ✓ PASS |
| Prior-truth regression spot-checks (GATE-01 ×3, GATE-02 ×2, GATE-03 ×4, INST-03 ×4, D-27/forgery survivors ×5, collision ×1) | `.venv/bin/python -m pytest -q <19 node IDs>` | `19 passed in 9.59s` | ✓ PASS |
| GAP A disconfirmation (real `main()`, `run.invariants: {}`) | inline probe driving `pinn.train.main` | exit 0; run-local `(divergence, open)` record present; `invariant_b_window (None, False)`; `eval01_precondition_i: False` | ✓ PASS (gap closed) |
| Owner-ratified anti-regression (real `main()`, N=500) | inline probe driving `pinn.train.main` | exit 0; no run-local record; `invariant_b_window (500, True)`; no consistency finding; `eval01_precondition_i: True` | ✓ PASS |
| GAP B disconfirmation (stage_boundary-only, census null) | inline probe: `load_preflight` + `_eval01_precondition_i` | `ValueError: ...must begin with a run_start event...`; predicate False | ✓ PASS (gap closed) |
| Predicate edge battery | inline probes 2–7 | honest → True; missing check → False; blocked census → False; hollow second run_start → False; legal resume → True; `"Passed"` → False | ✓ PASS |
| Cross-phase suite | retained evidence `${TMPDIR}/49-09-cross-phase-evidence.log` (run 2026-08-11T06:03:28Z–06:10:22Z, 414.11s, exit 0) | `957 passed, 3 skipped, 289 subtests passed` | ✓ PASS (cited; not re-run — no source/test/config input changed after the evidence run: the only later commit, 7562eef6, adds the review doc only; phase-49 suite independently re-run green on the committed tree) |

## Probe Execution

| Probe | Command | Result | Status |
|---|---|---|---|
| Phase-declared shell probes | `find scripts -path '*/tests/probe-*.sh'` plus PLAN/SUMMARY search | No Phase 49 `probe-*.sh` declared or discovered; the phase's probes are the pytest regressions and inline Python probes above | N/A |

## Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| GATE-01 | 49-01, 49-06, 49-07, 49-08, 49-09 | Full PHYS-05 table at run start and every boundary | ✓ SATISFIED | Truth 1 verified; closure-wave edge rows (duplicate-occurrence, empty, ordering) covered by named tests and probes. |
| GATE-02 | 49-04, 49-06, 49-08, 49-09 | Producer-backed placeholder census | ✓ SATISFIED | Truth 2 verified; exact-equality verdict gate and null/empty-census denial probed. |
| GATE-03 | 49-02, 49-03, 49-06, 49-07, 49-09 | Invariants A/B, owner N, resume continuity | ✓ SATISFIED (was BLOCKED) | Truth 3 verified; run-local N binding now gates eligibility; trip/resume spot-checks green. |
| INST-03 | 49-04, 49-05, 49-06, 49-07, 49-08, 49-09 | Known-divergence register surfaced in every run record | ✓ SATISFIED | Truth 4 verified; run-local open record carries the ten-key register shape; ordering/idempotency pinned by named tests. |

All four Phase-49 requirement IDs are accounted for: REQUIREMENTS.md rows exist for GATE-01, GATE-02, GATE-03, INST-03 (all currently "Gaps Found" pending this verdict); every ID appears in plan frontmatter across the phase (GATE-01 ×5, GATE-02 ×5, GATE-03 ×6, INST-03 ×6 plans). No orphans.

## Prohibition Checks

| Prohibition | Status | Evidence |
|---|---|---|
| Never invent/default/adjust/proxy N | ✓ VERIFIED | `configs/stage0-example.yaml` carries `front_advance_window_n: 500` exactly once; `configs/smoke.yaml` leaves the slot commented out; both byte-identical across the wave; no literal `500` added to production code in the closure diff (fixtures bind the owner-ratified value, plan-sanctioned). |
| Never reopen/edit the committed `INV-B-N-UNSET` entry | ✓ VERIFIED | Register byte-identical; entry stays globally `closed` with its proof test; run-local openness is computed per run. |
| Never weaken the predicate/filter/fixtures to turn red green | ✓ VERIFIED | Fixture repairs bind N=500 (named in the summary inventory); the one collateral assertion swap (`INV-B-N-UNSET` → `CONF-01-QUALIFICATION` in markdown) preserves equal-strength projection evidence and was disclosed; review confirmed the predicate, filter, and eligibility assertions carry zero relaxing edits. |
| Never reuse Phase-46 `gate_*` keys | ✓ VERIFIED | `test_no_gate_collision_in_preflight_and_register_payload` passed. |
| Never weaken exact PHYS-05 table equality | ✓ VERIFIED | `table.py` untouched; no tolerance constructs. |
| Never hide the Stage-2 refusal / no Stage-1+ platform work | ✓ VERIFIED | `test_stage2_fails_without_rebound_scheduler` passed; no stage factory added. |
| Never contact the admitted corpus or invoke `pinn.evaluate` | ✓ VERIFIED | All verification used synthetic configs and temp dirs; no Phase-49 code path invokes the evaluator. |
| Never duplicate the charter's general regime (SCOPE-32) | ✓ VERIFIED | No normative-statement index, waiver policy, X/M thresholds, or new run mode added. |
| Never modify plans/summaries 49-01..49-08, REQUIREMENTS.md, STATE.md | ✓ VERIFIED | Commit 93bdac47 touches exactly the plan's `files_modified` list; `git show --stat HEAD -- .planning/REQUIREMENTS.md .planning/STATE.md` equivalent check via diff range shows no such files. |

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `pinn/conformance/preflight.py` | 345–346 | WR-01: `append_event` mutates in-memory history before the write-time ordering check can reject it; a misuse leaves the recorder instance poisoned | ⚠️ Warning (accepted) | Production-unreachable — verified directly: `run_start_preflight` (train.py:1193) always writes run_start first, and stage boundaries append through that recorder afterward (train.py:985/1000). Does not affect any must-have truth: the eligibility predicate, loader, and run-start evidence are unaffected; the failure mode requires a caller to open a fresh recorder with a stage_boundary, which no code path does. Recorded in 49-REVIEW.md as the accepted finding. |
| `pinn/conformance/preflight.py` | 521–526, 534–539 | IN-01/IN-02: run-local record prose describes the global closure / says "omits" for the malformed case | ℹ️ Info | Wording only; machine-readable verdicts (`status`/`proof_test`/`waiver`, check `actual`/`passed`) are correct. No must-have impact. |
| Closure-wave files | — | Debt markers (`TBD`/`FIXME`/`XXX`) | None | Fresh scan of all six modified files: no unreferenced markers. `return None`/`return []` hits are honest null-projection paths in the summary honesty layer, not stubs. |

## Human Verification Required

None. Both gap closures are deterministic and were reproduced programmatically by this verifier; the owner-ratified happy path, the resume-ordering legality, and every edge row in the closure contract have named behavioral tests plus fresh probe evidence.

## Deferred-Item Check

Phases 50–52 re-checked. No gap remains to defer: both prior blockers are closed in this phase. The plan's GATE-03 unclassified edge row remains a flagged planning assumption (carried in 49-09-PLAN and 49-09-SUMMARY, not silently dropped); it is informational, not a failed truth. WR-01/IN-01/IN-02 are accepted review findings with no must-have impact; their optional wording/robustness fixes have no owning later phase and are not required for the goal.

## Gaps Summary

None. The two prior gaps are closed at their shared seam:

1. **Run-local N binding (GAP A).** The run-local invariant-B window is read once through the single `_extract_invariant_window` accessor; an unbound window produces two independent denial mechanisms (the affirmative failed `invariant_b_window` check AND the open run-local `INV-B-N-UNSET` divergence), and the predicate requires the affirmative check passed. Verified by fresh real-main probe in both directions.
2. **Evidence-hollow eligibility (GAP B).** The loader refuses a history that does not begin with `run_start` (at write AND load), and the predicate requires every `run_start` event to carry all seven `REQUIRED_RUN_START_CHECKS` passed plus a census whose verdict is exactly `"passed"`. Verified by a seven-probe disconfirmation battery.

Phase goal achieved: an invalid run is now structurally unable to spend the single look, and a genuinely conformant run remains eligible.

---

_Verified: 2026-08-11T06:56:13Z_

_Verifier: the agent (gsd-verifier)_

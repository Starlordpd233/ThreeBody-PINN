---
phase: 49-conformance-gate
plan: 07
subsystem: conformance
tags: [summary, conformance, gate, fail-closed, review-remediation, phys05, invariant-b]

# Dependency graph
requires:
  - phase: 49-conformance-gate
    provides: "The PHYS-05 launch gate (49-01), invariant-B runtime state (49-03), the INST-03 register (49-04), the conformance summary projection (49-05), and the owner-ratified invariant-B window (49-06)"
provides:
  - "A green required cross-phase suite obtained by correcting stale fixtures, never by relaxing the gate"
  - "A loadable record-only config state for present-but-null nested sections"
  - "Refusal of malformed causal front_idx values that could saturate and silence invariant B"
  - "Refusal of non-finite and self-contradicting preflight artifacts"
  - "Static resolution of every closed divergence entry's proof_test target"
affects: [phase-50-real-corpus-run]

# Actuals (#2632)
actuals:
  tasks: 5
  commits: 5

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Static (ast) proof resolution at load time, execution deferred to a meta-test"
    - "Two-belt non-finite rejection: parse_constant at read, recursive scan at validate, allow_nan=False at write"
    - "Deferred range validation for restored state that cannot be checked until a runtime dimension is known"

key-files:
  created:
    - tests/phase49/test_config_null_sections.py
    - tests/phase49/test_preflight_integrity.py
    - .planning/phases/49-conformance-gate/49-07-SUMMARY.md
  modified:
    - pinn/training/config_yaml.py
    - pinn/training/guards.py
    - pinn/conformance/preflight.py
    - pinn/conformance/register.py
    - tests/phase41/test_train_entrypoint.py
    - tests/phase42/_fixtures.py
    - tests/phase49/test_gate03_invariants.py
    - tests/phase49/test_gate03_resume.py
    - tests/phase49/test_inst03_register.py

key-decisions:
  - "The 32 suite failures were stale fixtures, not a gate defect: pinn/train.py is byte-unchanged across the whole plan."
  - "The present-but-null nested-section fix is generic to every nested dataclass field, not an `invariants` special case."
  - "front_idx well-formedness is validated before state update, so an out-of-range index can no longer pin the invariant-B high-water mark at saturated."
  - "A restored invariant-B high-water mark is range-checked on the first step that knows a collocation length, because load_invariant_b_state has no n_colloc to check against."
  - "Only LOCKED check failures contradict a passed preflight status; the advisory tier records mismatches without raising by design."
  - "An open divergence under a passed status is a documented D-23/D-27 state, not a contradiction; eligibility is denied by _eval01_precondition_i rather than by refusing to load the caveat record."
  - "Static proof resolution belongs in the register loader; proof EXECUTION stays in a meta-test, because a training launch must never import pytest machinery."

requirements-completed: []

coverage:
  - id: CR-10
    description: "The maintained launch suites are green under the PHYS-05 gate because the fixtures moved to the locked Stage-0 row, and an explicit negative test proves a non-conformant cap is still refused."
    requirement: GATE-01
    verification:
      - kind: integration
        ref: "tests/phase41/test_train_entrypoint.py::Phys05LaunchGateTests"
        status: pass
      - kind: invariant
        ref: "git diff d2f4de5e..HEAD -- pinn/train.py (empty)"
        status: pass
    human_judgment: false
  - id: CR-01
    description: "run.invariants omitted, {}, comment-only, and explicit null all produce InvariantsConfig() with front_advance_window_n None; both shipped configs parse."
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_config_null_sections.py"
        status: pass
      - kind: regression
        ref: "tests/phase40 (unknown-key fail-closed contract intact)"
        status: pass
    human_judgment: false
  - id: CR-02
    description: "Invariant B accepts only a finite, non-boolean, integral front_idx equal to -1 or within [0, n_colloc); every other shape is refused into the invariant-A bundle, and an impossible restored high-water mark is rejected."
    requirement: GATE-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate03_invariants.py, tests/phase49/test_gate03_resume.py"
        status: pass
    human_judgment: false
  - id: CR-11
    description: "Preflight artifacts carrying NaN/Infinity are rejected at load and cannot be written, and terminal summary finalization still succeeds."
    requirement: INST-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_preflight_integrity.py"
        status: pass
    human_judgment: false
  - id: CR-05
    description: "A passed artifact contradicting its own evidence (failed event, or failed locked check) is refused, and a forged artifact cannot report EVAL-01 eligibility."
    requirement: INST-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_preflight_integrity.py::test_forged_artifact_cannot_report_eval01_eligibility"
        status: pass
    human_judgment: false
  - id: CR-07
    description: "A closed entry whose proof_test does not resolve to a real module and node fails the register load closed; a meta-test executes every closed entry's proof node."
    requirement: INST-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_inst03_register.py (static resolution trip tests)"
        status: pass
      - kind: integration
        ref: "tests/phase49/test_inst03_register.py::test_every_closed_register_entry_has_a_real_passing_proof_test"
        status: pass
    human_judgment: false

# Metrics
completed: 2026-08-05
status: complete
---

# Phase 49 Plan 07: Conformance-Gate Blocker Remediation

**The required cross-phase suite is green — 918 passed, 3 skipped, 0 failed — and every refusal branch this plan added is proven to trip.**

## Result

| | Before (retained evidence, 2026-08-05, 608.9s) | After (390.9s) |
|---|---|---|
| Required suite | 32 failed / 820 passed / 3 skipped | **0 failed / 918 passed / 3 skipped** |

The gate was never touched to obtain this. `git diff d2f4de5e..HEAD -- pinn/train.py` is empty across the entire plan.

## Accomplishments

**Task 1 — CR-10.** The maintained phase41/phase42 config builders shipped `lambda_e_max = 1.0`; `PHYS05_LAMBDA_E_MAX[0]` is `0.0`, so the gate was correctly refusing every launch. The fixtures moved to the locked row, and `Phys05LaunchGateTests` now drives the PHYS-05 refusal explicitly — the trip test that had to survive the correction, since no maintained fixture exercises that branch any more.

**Task 2 — CR-01.** `_map_section` branched only on `isinstance(value, Mapping)`, so a present-but-`None` nested section fell through and forwarded `None` into `RunConfig`. Both shipped configs document the record-only state as a comment-only `invariants:` header, which YAML parses to `None`. Fixed generically for every nested dataclass field.

**Task 3 — CR-02.** A bare `int()` is not a validation: it accepted bools, truncated non-integral floats, admitted out-of-range indices, and raised an uncaught `OverflowError` on infinity. The consequence was worse than a crash — with `n_colloc = 4`, `front_idx = 99` left `front_high_water >= n_colloc - 1`, so invariant B read as permanently saturated and could never trip again.

**Task 4 — CR-11 + CR-05.** Non-finite values are refused at three points (parse, validate, write), and a passed artifact must now agree with its own evidence.

**Task 5 — CR-07.** Closed entries' `proof_test` targets are resolved statically via `ast`. The execution meta-test already existed and was left in place rather than duplicated.

## Task Commits

1. **Task 1 — CR-10 stale launch fixtures** — `63cb3aed` (test)
2. **Task 2 — CR-01 null nested sections** — `288c2a9e` (fix)
3. **Task 3 — CR-02 front_idx validation** — `d26415cb` (fix)
4. **Task 4 — CR-11 + CR-05 preflight integrity** — `fbe45125` (fix)
5. **Task 5 — CR-07 proof resolution** — `b0dd0774` (fix)

## Deviations from Plan

**1. CR-05 narrowed to LOCKED checks (Task 4).** The plan's behavior block said a passed artifact carrying "a check with `passed` false" is contradictory. `assert_phys05_table` deliberately RECORDS an advisory mismatch without raising, so a failed advisory check is evidence an honest run legitimately carries. `49-REVIEW.md` CR-02's sibling finding CR-05 says "any failed **locked** check", which is the reading implemented. The tier-blind reading would have refused honest artifacts. A test pins the accepted advisory path.

**2. CR-05 open-divergence refusal NOT implemented (Task 4).** The plan listed "an open divergence entry" as a contradiction to refuse at load. It is not a contradiction — it is the documented D-23/D-27 state in which the artifact *is* the caveat record that must travel with the run, exactly what `INV-B-N-UNSET` was before 49-06 closed it. Refusing to load it would render `conformance: null` in the summary and destroy the evidence trail this phase exists to protect. The plan's stated goal ("a forged artifact cannot report EVAL-01 eligibility") is already enforced by `_eval01_precondition_i`, which filters on `kind == "divergence" and status == "open"`; that is now asserted by test rather than assumed.

**3. Task 1 fixture repair extended by one key.** Correcting the PHYS-05 cap unmasked a second stale spot in the same hand-built anchor payload: it omitted `invariant_b_state`, which resume requires and refuses to re-arm silently. Previously masked because the gate refused the launch upstream. Repaired in the same commit as part of the same "the fixture is stale, not the product" finding.

**4. Task 1 anchor cap derived, not hardcoded.** The plan said align `ScheduledWeights(..., lambda_e_max=1.0)` to `0.0`; it now reads `float(cfg.loss.lambda_e_max)` so a synthesized anchor tracks the launched config and cannot restale.

**5. Task 5 meta-test already present.** `test_every_closed_register_entry_has_a_real_passing_proof_test` already executed every closed entry's proof node as a subprocess pytest invocation. Only the static half was missing. No duplicate was added.

**Plan reading recorded (not a deviation).** Task 3's behavior line "front_idx = -1 … is accepted" is governed by the same task's acceptance criterion "the pre-existing accepted paths (-1 and in-range) still behave as before". `-1` is treated as *well-formed* by the validator while keeping its pre-existing invariant-A HALT semantics, which `test_front_idx_sentinel_trips_invariant_a` still pins. No gate was loosened.

## Review Findings Left UNTOUCHED

This plan's scope was exactly six findings. The phase does **not** close implying a clean review. Still open in `49-REVIEW.md`:

- **CR-03** — non-`ValueError` metadata/census failures bypass refusal evidence (BLOCKER)
- **CR-04** — scheduler corruption can skip refusal evidence before validation (BLOCKER)
- **CR-06** — resume destroys append-only preflight history (BLOCKER)
- **CR-08, CR-09** — remaining BLOCKERs
- **WR-01, WR-02, WR-03** — warnings
- **IN-01** — informational

Note that CR-04's `OverflowError`-on-infinity mechanism is the same class of defect fixed here for `front_idx`, but in `pinn/conformance/table.py`; it was deliberately not touched.

## Verification

| Check | Result |
|---|---|
| Required cross-phase suite | **918 passed, 3 skipped, 0 failed** (390.9s) |
| `git diff d2f4de5e..HEAD -- pinn/train.py` | empty — the gate was never relaxed |
| `configs/stage0-example.yaml` | `front_advance_window_n: 500` intact (owner ruling 2026-08-05) |
| `INV-B-N-UNSET` | still `closed`, proof node resolves and executes green |
| D-16 (every new refusal branch trips) | 30+ trip tests across the four hardened modules |

Suite command:

```
.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 \
  tests/phase43/test_summary_enrichment.py tests/phase43/test_summary_honesty.py \
  tests/phase43/test_real_data_smoke_config.py tests/phase46 tests/phase47 \
  tests/phase48 tests/phase49
```

## Issues Encountered

None blocking. Two self-inflicted test-harness defects were caught and corrected during execution (missing `mkdir` on temp subdirectories; an assertion targeting the wrong non-finite refusal belt) — neither was a product defect.

## Next Phase Readiness

- The gate is trustworthy for Phase 50's single real-corpus look on the six findings in this plan's scope.
- **It is not yet review-clean.** Five BLOCKERs (CR-03, CR-04, CR-06, CR-08, CR-09) remain unaddressed and are a phase-close decision, not an executor decision.
- `.planning/ROADMAP.md` was not edited, per this plan's explicit prohibition.

---
*Phase: 49-conformance-gate*
*Plan: 07*
*Completed: 2026-08-05*

## Self-Check: PASSED

- Summary file exists at the canonical phase path.
- All five task commits are present in git history (`63cb3aed`, `288c2a9e`, `d26415cb`, `fbe45125`, `b0dd0774`).
- `pinn/train.py` is byte-unchanged across the plan.
- No placeholder stubs or generated files were introduced.

---
phase: 49
reviewers: [claude-max, codex1, codex2, codex3]
rerun_reviewers: [claude-max, codex1, codex2, codex3]
reviewed_at: 2026-08-05T01:55:02Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353
---

# Cross-AI Plan Review — Phase 49

## claude-max Review

# Phase 49 Plan Review — Conformance Gate (49-01 … 49-06)

## 1. Summary

Six plans build the minimum conformance gate (GATE-01/02/03, INST-03): a locked PHYS-05 table assertion at two sites, a placeholder census, runtime invariants A/B inside `StepGuards`, a divergence register, `preflight.json`/`summary.json` projection, an end-to-end seam test, and a blocking owner checkpoint for N. All files were read successfully. The plans are unusually rigorous — near-total trip-test coverage, fail-closed artifact discipline, and correct reservation of the N decision to the owner. The main defects are a wiring seam between 49-01 and 49-04 that appears to require an undeclared `pinn/train.py` edit, a same-wave implicit dependency of 49-04 on 49-02, and a regression gate that omits existing test suites covering modules this phase modifies.

## 2. Strengths

- **D-16 trip discipline is systemic.** Every guard, assertion tier, loader rejection branch, and projection boolean has a test that drives it to actually fail (ulp-adjacency, both directions of `eval01_precondition_i`, stall-across-resume asserted one step either side of the boundary). This directly answers the v2.0/Phase-39 "checks that cannot fail" lesson.
- **Governance alignment is exact.** N is never chosen by an agent (D-18/D-21); the checkpoint offers anchors "to react to," deferral is a defined non-deadlocking state (D-20), 49-06 is `autonomous: false`, and prohibitions explicitly bar "fixing" the D-06 stage-2 refusal or defining waiver policy (charter-owned, SCOPE-32).
- **Fail-closed artifact engineering.** Atomic writes, schema versioning, refusal-writes-artifact-first ordering (D-27), verbatim passthrough into the run record (no recompute layer to drift), and byte-idempotency probes.
- **Cheap-change discipline.** Keyword-only default-None parameters keep every existing constructor call untouched; the checkpoint schema bump exploits verified symbolic references; D-28 namespace separation from Phase-46 `gate_*` keys is grep-gated.
- **Requirement and criteria coverage is complete on paper**: GATE-01..03 + INST-03 all mapped; roadmap success criterion 5 (SCOPE-32 record) is discharged in 49-01 with a dated re-verification.

## 3. Concerns

**HIGH — Census-into-`main()` wiring is unowned.** 49-04 extends the run-start preflight composition to embed the census, and 49-06's e2e test asserts a *real* `main()` run's `preflight.json` carries census + open divergences. But `run_census` needs `config`, `scheduled_weights`, `metadata`, and `provisional_fields()` at the call site, and no plan after wave 1 declares a `pinn/train.py` edit to pass them: 49-01 wires site 1 before the census exists (its action mentions only the table assertion), 49-04's `files_modified` excludes `train.py`, 49-03 touches `train.py` only for checkpoint restore, and 49-06 is test-only by acceptance criterion. Either 49-01 must speculatively pre-wire the full context (not stated) or 49-04 needs an undeclared `train.py` edit — which would collide with 49-02's concurrent wave-2 `train.py` edits under the repo's disjoint-owned-paths concurrency policy. As written, this surfaces as a wave-4 e2e failure and a gap-routing detour.

**MEDIUM — Same-wave implicit dependency, 49-04 → 49-02.** 49-04's consistency finding ("`front_advance_window_n` set while INV-B-N-UNSET is open") reads a config field that 49-02 creates in the same wave; declared `depends_on` is `[49-01]` only. Duck-typed test fixtures can mask this, but the real composition semantics depend on 49-02, and the plan doesn't require defensive `getattr` access at the preflight layer.

**MEDIUM — Regression gate omits live suites covering modified modules.** The phase-close gate runs `tests/phase38 40 41 42 46 47 48 49` but `tests/phase37`, `phase39`, and `phase43` exist. `phase43` includes `test_summary_enrichment.py`/`test_summary_honesty.py` (exercising `pinn/training/summary.py`, modified by 49-05) and `test_smoke.py`/`test_real_data_smoke_config.py` (plausibly validating `configs/smoke.yaml`, modified by 49-02). A regression there would pass every gate in this phase.

**MEDIUM — Success-criterion 3 vs. the deferral branch.** ROADMAP criterion 3 reads "the causal front advances within the owner-ratified N steps"; option-d closes the phase with invariant B record-only and no ratified N. The D-20 defense (structural ineligibility via `eval01_precondition_i = false`) is sound, but a literal verifier will score criterion 3 unmet on the deferral branch. The reconciliation should be recorded (roadmap wording amended or the verifier instruction stated), not left implicit.

**LOW — D-25 "testable" has no discriminator.** 49-04's loader rule ("a closed entry must carry a non-empty proof_test") is stricter than the truths/CONTEXT wording ("whose closure is testable"). Entries closed by owner ruling (C-07 via GAP-45-01 option A) force the executor to *select* a proof test — mild invention risk under the project's process-artifact-schema MUST-surface rule if no natural node exists in `tests/phase47-48`.

**LOW — Verify-gate gaps.** The anti-tolerance gate greps only `isclose` (an `abs(a-b) < eps` comparison passes it); the `slbfgs_preflight.py`/`step_log.py` byte-unchanged criteria lack automated `git diff` gates in two of three places; the smoke-config N grep would also reject a legitimate explicit `null` (D-20 permits null) and relies on `\s` in BSD grep.

## 4. Suggestions

1. Resolve the HIGH concern before execution: either amend 49-01 to construct the run-start composition entry point with the full context (`config`, `metadata`, `scheduled_weights`, `provisional`) from the start — main() has all four in scope at the site-1 insertion point — or add `pinn/train.py` to 49-04's `files_modified` and move 49-04 to wave 3 (it already gates 49-05, which is wave 3, so the wave graph absorbs this with no critical-path cost).
2. Add `49-02` to 49-04's `depends_on` (or explicitly require tolerant `getattr` access for the consistency finding and say so in the task action).
3. Add `tests/phase43` (at minimum) to the phase-close full-suite command in all six plans; state explicitly why phase37/39 are excluded if intentional.
4. Record the criterion-3/option-d reconciliation in 49-06's success criteria or as a planned ROADMAP wording amendment at phase close.
5. In 49-04, state the rule the loader actually enforces (all closed entries need `proof_test`, or add an explicit `testable: false` escape with named justification) so the executor never adjudicates "testable" ad hoc.
6. Strengthen the anti-tolerance gate (`grep -nE "isclose|allclose|abs\(" pinn/conformance/table.py`) and add `git diff --name-only` gates for the two byte-unchanged criteria that lack them.

## 5. Overall Risk

**MEDIUM.** The plans achieve the phase goal in substance — coverage of all four requirements is real, edge cases are unusually well probed, and destructive-operation/scope risks are absent (test-heavy, additive, owner-gated). The rating is driven by one structural seam (census wiring into `main()`) that as written fails at wave 4 and creates a same-wave file-ownership collision, plus the omitted regression suites. All are cheap to fix at plan level before execution.

---

## codex1 Review

_codex1 failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex1
- exit_code=143
- elapsed_seconds=1201
- timeout_seconds=1200
- watchdog=triggered
- timeout_after_seconds=1200
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"max\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=697798

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex1-49.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex1-49.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex1-49.meta

Stderr excerpt:
```
k: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
collab: Wait
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
collab: Wait
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
mcp: sequential-thinking/sequentialthinking started
mcp: sequential-thinking/sequentialthinking (completed)
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
collab: Wait

```

---

## codex2 Review

_codex2 failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex2
- exit_code=143
- elapsed_seconds=1200
- timeout_seconds=1200
- watchdog=triggered
- timeout_after_seconds=1200
- command=env CODEX_HOME=<home>/.codex2 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"max\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=545079

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex2-49.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex2-49.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260805T013501Z-37353/xreview-codex2-49.meta

Stderr excerpt:
```
olUse Completed
collab: Wait
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
codex
The review is converging on goal-level issues rather than stylistic ones. I’m now cross-checking whether the planned tests would actually catch each failure; several currently use synthetic or empty fixtures that bypass the committed register/config combinations most likely to fail.
hook: PreToolUse
hook: PreToolUse Completed
collab: Wait
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## codex3 Review

## 1. Summary

All six plan files were readable. The plans are well structured, but four correctness gaps currently prevent Phase 49 from reliably achieving its conformance-gate goal.

## 2. Strengths

- Strong tracer-first decomposition, explicit dependencies, and focused TDD acceptance checks.
- Good fail-closed artifact handling, atomic writes, deterministic serialization, and refusal-before-exit evidence.
- Scope boundaries are respected: Stage-0 only, synthetic seam testing, no held-out evaluation, and owner control of `N`.
- The final end-to-end seam and full regression gate are valuable integration checks.

## 3. Concerns tagged HIGH / MEDIUM / LOW

- **HIGH — GATE-01 omits locked `lambda_data`.** The plan defines `PHYS05_LAMBDA_DATA = 1.0` but instructs `assert_phys05_table` to inspect only max weights, `lambda_ic`, and warmup fields. Thus a regression changing the live data weight would pass the supposedly “full” PHYS-05 gate, with no corresponding trip test. See [49-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-01-PLAN.md:122) and [49-CONTEXT.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-CONTEXT.md:57).

- **HIGH — `eval01_precondition_i` can never become true with the planned register.** Plan 49-04 deliberately retains multiple `status: open`, `kind: qualification` entries, copies every open entry into `open_divergences`, and Plan 49-05 rejects any unwaived entry in that collection. EVAL-01 requires zero unwaived *divergences*, not zero open qualifications. Closing only `INV-B-N-UNSET` therefore leaves valid runs ineligible. See [49-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-04-PLAN.md:128), [49-05-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-05-PLAN.md:83), and [REQUIREMENTS.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/REQUIREMENTS.md:11).

- **HIGH — the census is not wired into the production composition root.** `run_census` needs the live config, scheduler, and metadata, but Plan 49-04’s composition task excludes `pinn/train.py`; Plan 49-01 wires only the table assertion there. Modifying `preflight.py` alone cannot supply those inputs to a real run. Plan 49-04 also consumes the `N` field introduced by parallel Plan 49-02 without depending on it. See [49-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-04-PLAN.md:159) and [49-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-04-PLAN.md:175).

- **HIGH — schema-v2 checkpoints still permit silent invariant-B re-arming.** Plan 49-03 explicitly omits `invariant_b_state` from required checkpoint keys and treats an absent key like legitimate `None`. A schema-v2 payload missing that state therefore passes structural validation and resets the stall window, exactly what D-17 prohibits. See [49-03-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-03-PLAN.md:94) and [49-03-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/49-conformance-gate/49-03-PLAN.md:121).

## 4. Suggestions

1. Add an exact live `lambda_data == 1.0` assertion and a test that drives it to fail.
2. Preserve all open entries for reporting, but compute EVAL-01 precondition (i) using only unwaived entries with `kind == divergence`. Test against the committed register with `INV-B-N-UNSET` closed.
3. Add `pinn/train.py` to Plan 49-04 and serialize it after Plan 49-02, then test a real `main()` census refusal.
4. Require `invariant_b_state` in schema v2 while permitting an explicit `None`; reject missing or malformed state with dedicated resume tests.

## 5. Overall Risk (HIGH)

The current plans can both miss invalid runs and make valid runs permanently evaluation-ineligible, while also leaving a prohibited resume-integrity path open.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=244
- timeout_seconds=1200
- watchdog=not_triggered
- command=ccp claude-max --model claude-fable-5 -p - 
- stdout_bytes=7263
- stderr_bytes=0

### codex1
- reviewer=codex1
- exit_code=143
- elapsed_seconds=1201
- timeout_seconds=1200
- watchdog=triggered
- timeout_after_seconds=1200
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"max\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=697798

### codex2
- reviewer=codex2
- exit_code=143
- elapsed_seconds=1200
- timeout_seconds=1200
- watchdog=triggered
- timeout_after_seconds=1200
- command=env CODEX_HOME=<home>/.codex2 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"max\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=545079

### codex3
- reviewer=codex3
- exit_code=0
- elapsed_seconds=830
- timeout_seconds=1200
- watchdog=not_triggered
- command=env CODEX_HOME=<home>/.codex3 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"max\" --skip-git-repo-check - 
- stdout_bytes=4131
- stderr_bytes=541699

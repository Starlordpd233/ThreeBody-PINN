---
phase: 47
reviewers: [codex, codex1, claude-max, claude-alt]
rerun_reviewers: [codex, codex1, claude-max, claude-alt]
reviewed_at: 2026-07-30T07:59:27Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T075326Z-77694
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 47

## codex Review

**1. Summary**

The Phase 47 plan set is well-ordered and mostly complete: 47-01 fixes frame residency first, 47-02 derives/persists `S_H`, and 47-03 wires `ε_H`. I found no scope-breaking edits in the plans, but a few validation/reporting gaps should be tightened before execution.

**2. Strengths**

- Strong dependency ordering matches the roadmap: CONF-09 → CONF-02 → CONF-03.
- Good atomicity requirement for residency swap + frame re-ratification + pairing-test correction.
- Strong fail-closed posture for invalid `S_H`, malformed metadata, and resume mismatches.
- Tests target the important scientific invariants: IC13 invariance, velocity identity, frame coherence, split-only median, and uniform `eps_h`.

**3. Concerns Tagged HIGH / MEDIUM / LOW**

- **HIGH**: [47-03-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-03-PLAN.md:206>) pipes the full pytest command through `tail -5`. Without explicit pipefail handling, a failing pytest run can still return success from `tail`, weakening the final regression gate.

- **MEDIUM**: [47-02-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-02-PLAN.md:222>) validates `s_h`, `eps_h`, `n_train`, and frame, but does not explicitly require `eps_train == EPS_SOFT` or persisted `energy_floor_factor == config.stage.energy_floor_factor` at consumption. Since [47-03-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-03-PLAN.md:135>) recomputes `eps_h` from live config and `s_h`, this should be locally checked at the metadata boundary.

- **MEDIUM**: The summaries must report real `S_H`, `ε_H`, and `N_train` values ([47-02-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-02-PLAN.md:343>), [47-03-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-03-PLAN.md:197>)), but the plans do not specify the exact non-training command/path that produces those production values. That leaves room to use synthetic test values, skip the values, or accidentally run prohibited training work.

- **LOW**: `D-23` is overloaded: [47-01-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-01-PLAN.md:288>) uses it for gate-metric comparison evidence, while [47-VALIDATION.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-VALIDATION.md:89>) uses it for visible `S_H` reporting. This is unlikely to break code but can confuse closure evidence.

**4. Suggestions**

- Replace the final gate command with a status-preserving form, or run pytest directly and save full output separately.
- Extend metadata validation/tests to tamper `eps_train`, `energy_floor_factor`, and frame fields explicitly.
- Add an explicit “metadata-only real-data derivation” step for producing `S_H/ε_H/N_train`, with a named output artifact and no training loop.
- Rename or disambiguate the two `D-23` references before execution.

**5. Overall Risk (LOW/MEDIUM/HIGH)**

**MEDIUM**. The implementation strategy is sound, but the final validation command and metadata-consumption boundary need tightening to avoid a false-green closure.

---

## codex1 Review

_codex1 failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=456693

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T075326Z-77694/xreview-codex1-47.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T075326Z-77694/xreview-codex1-47.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T075326Z-77694/xreview-codex1-47.meta

Stderr excerpt:
```
 + 1e-12,
tests/phase40/test_scheduled_weights.py:78:                        float(w.lambda_l), 1.0 + 1e-12,
tests/phase40/test_grad_clip.py:160:        _set_grad(p, 1e-12)
tests/phase40/test_grad_clip.py:162:        # Window median (1e-12) below default floor (1e-6) -> effective = 1e-6.
tests/phase40/test_controllers.py:787:    TOL = 1e-12
tests/phase40/test_optimizer_phase.py:262:        values = iter([1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14])
tests/phase40/test_optimizer_phase.py:732:        expected_default = abs(ctx_default.h0) * default_factor + 1e-12
tests/phase40/test_optimizer_phase.py:733:        expected_override = abs(ctx_override.h0) * override_factor + 1e-12
tests/phase40/test_optimizer_phase.py:745:        """Shipped default 1e-4 must keep eps_h == |h0|*1e-4 + 1e-12."""
tests/phase40/test_optimizer_phase.py:748:        expected = abs(ctx.h0) * 1e-4 + 1e-12

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## claude-max Review

Execution error
---

## claude-alt Review

I have enough to write the review. The plans are internally consistent; my checks confirmed line numbers, the `1e-12` floor literal, the venv path resolution, and that D-13's Stage-0 population scope is grounded (not an oversight). Two execution-environment preconditions are the main exposure.

---

# Cross-AI Plan Review — Phase 47 (Frame Completion & S_H Pipeline)

## 1. Summary
Three well-sequenced plans discharge CONF-09 (47-01: complete residency to the rotation-gauged, D/V-scaled frame + re-ratify `RATIFIED_VALIDATION_FRAME`), CONF-02 (47-02: compute `S_H = median_train(K0 + Uabs0)` once in float64, persist to `training_metadata.json`, fail-closed), and CONF-03 (47-03: wire `ε_H = 1e-4·S_H` into the loss and delete the prohibited additive floor). Wave ordering 1→2→3 with `depends_on` chaining is physically justified — `S_H` is frame-dependent (`H' = D·H`), so it must follow the frame completion. The plans are unusually rigorous: every decision is traced to a grounded `D-xx` in CONTEXT, scope prohibitions are explicit, and threat models are scoped correctly for an internal single-operator pipeline. I verified line numbers (`controllers.py:482`, the `+1e-12` floor, `RATIFIED_VALIDATION_FRAME` at `:788`), that only `train.py:964` constructs `RunController` outside tests, and that the computed `.venv` path resolves to the shared main-checkout venv.

## 2. Strengths
- **Correct dependency ordering and single-source discipline.** The `_matched_plummer_components` seam (D-11) gives one home for the softened potential; `k0/uabs0` captured on the float64 side before the fp32 cast (D-12); the median lives at run setup, not in `_materialize` (D-13). All grounded.
- **Genuine fail-closed design.** Strictly-positive predicate (exact `0.0` refuses), empty/single-element population handled, `atomic_write_text`, re-validation on every load, and the resume recompute-and-compare (added from convergence cycle 1) exercised through the real `train.py` seam rather than prose. `eps_h == factor * s_h` re-check round-trips bit-identically through JSON (float64 repr).
- **Atomicity where it matters.** 47-01 Task 1 forces residency + frame constant + pairing-test correction into one commit (criterion 7), so no tree exists where `COHERENT_FRAME_PAIRS` lies. The D-06 in-place correction avoids a competing test oracle.
- **Scope containment verified.** Making `RunController.s_h` a required kwarg breaks only `train.py:964` + the 12 enumerated test sites — no hidden production construction site exists.

## 3. Concerns

**HIGH** — none blocking on design correctness.

**MEDIUM — Blacklist path resolution (47-01 Task 3).** The one-shot probe replicates the Phase 46 invocation with `--blacklist-path problematic_ics_blacklist.json`. That file is absent from both the trainex worktree and the main checkout (shallow search); Phase 46 resolved it via the probe's `git_common_dir_default` data-root logic. Task 3's own guard says "if the blacklist is missing on disk, STOP." A literal CWD-relative existence check in the worktree will trip that STOP and block phase closure even though the probe may resolve the file internally. Confirm the blacklist resolves in this worktree before executing Task 3, or the phase halts on evidence it cannot produce.

**MEDIUM — phase43 environmental baseline is machine-sensitive (47-03 Task 2).** The regression gate compares against a "documented 12-failure phase43 environmental baseline." Environmental failure counts drift with data-root/hardware/torch state. If this worktree's baseline differs from 12, the count comparison will either mask a real regression or manufacture a false one. Re-confirm the baseline count in this worktree at execution time rather than trusting the documented 12.

**MEDIUM — grep-based acceptance criteria are brittle and over-constrain syntax.** Many gates assert exact text (`grep -c 'int(pre.r_gauge.shape\[0\])' == 2`, `'energy_floor_factor) \* self._s_h' == 1`, `grep -v '^\s*#'` for banned symbols). These encode a specific phrasing, so a correct implementation with trivially different formatting fails the gate, and conversely they pressure the executor to satisfy text over intent. Most are paired with a behavioral pytest, which mitigates it — but note `grep -v '^\s*#'` only strips full-line comments, not inline trailing comments, so an inline `# r_com_ordered` reference would slip past 47-01 criterion 3's intent while a legitimate one could fail it.

**LOW — 47-03 Task 1 criterion 4 is imprecisely specified.** "`grep -rn "RunController(" pinn/ tests/ | wc -l` equals the count of sites carrying `s_h=`" also matches `self.RunController(` wrapper calls (present in phase40/41 tests) and any definition/alias line; the equality is stated loosely. The per-file enumeration is correct, but the wc-based equality is not a clean invariant.

**LOW — no explicit test that anchor targets adopt the new frame (47-01).** The plan relies on residency pass-through (`controllers.py:463-473`) with "no controller edit belongs in this plan." Correct by construction, but there is no direct assertion that `h0/l0/true_r0/true_v0` now reflect `r_gauge`; it is covered only transitively by the corrected pairing oracle.

## 4. Suggestions
- Before executing 47-01 Task 3, add a preflight that runs the probe's own data-root resolution (or documents where `problematic_ics_blacklist.json` actually lives for the trainex worktree) so the STOP guard distinguishes "genuinely missing" from "CWD-relative path miss."
- Re-derive the phase43 baseline count in this worktree at the start of 47-03 Task 2 and record both the freshly-measured and documented counts, rather than asserting against a static 12.
- Where a grep gate has a paired pytest, prefer loosening the grep to a symbol-presence check (e.g. `self._s_h`) rather than an exact-expression match, to avoid false gate failures on correct code.
- Consider one explicit 47-01 assertion that an anchor target equals `fp32(r_gauge[0])` to make the pass-through claim directly checkable rather than transitive.

## 5. Overall Risk: **LOW**
The design is exceptionally well-grounded, correctly ordered, and scope-contained; the physics dependency (frame before scale) is respected and the fail-closed/atomicity properties are real. Residual risk is concentrated in two execution-environment preconditions (blacklist resolution, phase43 baseline) and grep brittleness — operational, not architectural. Verify those two preconditions in the trainex worktree before execution and the phase should land cleanly.

*Note: I did not load 47-RESEARCH.md, 47-VALIDATION.md, 47-PATTERNS.md, PROJECT.md, REQUIREMENTS.md, ROADMAP.md, or AGENTS.md in full — I read the three plans and 47-CONTEXT.md (D-13 excerpt) and verified concerns directly against source. All files listed were readable; none failed to load.*

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=336
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3463
- stderr_bytes=420433

### codex1
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=456693

### claude-max
- reviewer=claude-max
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=15
- stderr_bytes=0

### claude-alt
- reviewer=claude-alt
- exit_code=0
- elapsed_seconds=237
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp alt --model claude-opus-4-8 -p - 
- stdout_bytes=6870
- stderr_bytes=0

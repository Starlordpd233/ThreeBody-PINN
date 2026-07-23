---
phase: 41
reviewers: [codex, grok, claude-max, claude-kimi]
rerun_reviewers: [claude-max, codex, claude-kimi, grok]
reviewed_at: 2026-07-18T06:02:27Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T055626Z-56749
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 41

## codex Review

## 1. Summary

Phase 41 plans are detailed and mostly aligned with CTRL-01..08. They show strong cross-plan traceability and explicitly address several prior high-risk issues. Overall, the phase is close, but I would not execute as-is: a few integration contracts are still ambiguous enough to miss core acceptance criteria.

Reviewed current `milestone/v2.0` working tree contents. No files were edited.

## 2. Strengths

- Clear dependency ordering: 41-01 establishes config/atomic/test scaffolding; 41-02 and 41-03 can run after it; 41-04 integrates; 41-05 validates end-to-end.
- Good acceptance coverage for atomic writes, `weights_only=True`, fallback scan, resume refusal, strict CPU override, and Phase-40 regression protection.
- Strong governance handling for owner-carved values: checkpoint ceiling, guard thresholds, and resume-field classification are marked provisional instead of silently ratified.
- The single `build_checkpoint_payload(...)` composer is the right architectural fix for checkpoint schema drift.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** Guard hook placement may bypass the required `failure/` bundle for NaN/Inf.  
  Existing controller paths return `RECOVER` immediately on non-finite loss/gradient in [controllers.py](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:493) and L-BFGS non-finite state in [controllers.py](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:580). But 41-04 places the guard hook after existing non-finite checks in [41-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-04-PLAN.md:143). That risks satisfying “RECOVER” while missing CTRL-07’s required `failure/` bundle for NaN/Inf trips.

- **HIGH:** The checkpoint hook signature is under-specified for complete payload composition.  
  41-04 says the hook is called with `global_step`, but the same hook must save a full CTX-53 payload needing controller state, curriculum state, config identity, schema version, and elapsed/cadence context in [41-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-04-PLAN.md:138). Without an explicit hook contract, implementation can regress to raw `state_dict()` or stale/missing curriculum identity, undermining the high-priority single-composer fix.

- **HIGH:** Frozen-config RNG recording remains unresolved while CTRL-08 requires it.  
  The spec requires RNG state in the frozen config and every checkpoint in [41-SPEC.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-SPEC.md:61). 41-01 registers `frozen_config_rng_recording_format` as `UNDECIDED` and says not to implement either representation until owner pick in [41-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-01-PLAN.md:148). As written, autonomous execution can finish without satisfying the config half of CTRL-08.

- **MEDIUM:** `resume_config_diff` has inconsistent API shape.  
  41-05’s artifact list includes `checkpoint_resolved_config`, but later behavior/action examples pass only `checkpoint_config_identity` in [41-05-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:87) and [41-05-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:164). This matters because snapshot comparison is the backstop for unclassified-field fail-safe refusal.

- **MEDIUM:** `run_name` validation should be stricter.  
  The plan rejects empty names and path separators in [41-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-01-PLAN.md:135), but should also reject `.` / `..`, absolute paths after normalization, control characters, and resolved paths outside the intended `runs/` root.

- **LOW:** Fallback scan ordering by step index / mtime is fragile for anchors.  
  41-02 orders mixed rolling and anchor candidates by step index / mtime in [41-02-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-02-PLAN.md:106). Payload `counters.global_step` would be a more reliable “newest valid checkpoint” source.

## 4. Suggestions

- Move or wrap the NaN/Inf paths so every RECOVER-causing non-finite event also goes through the guard/bundle contract, or explicitly have existing early-return paths call `write_failure_bundle`.
- Define the checkpoint hook signature explicitly, e.g. `checkpoint_hook(controller, global_step, elapsed, curriculum_state, config_identity)`, and test that the rolling checkpoint payload contains current curriculum/config identity, not just controller state.
- Resolve the frozen-config RNG representation before executing 41-01/41-05, or mark the affected work non-autonomous/blocking until the owner chooses A or B.
- Normalize the resume diff API to one signature and add tests for digest-match plus resolved-snapshot mismatch through the actual `pinn.train --resume` path.
- Harden `run_name` as a slug or verify `run_dir.resolve().is_relative_to(runs_root.resolve())`.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**HIGH** until the guard-hook placement, checkpoint-hook contract, and frozen-config RNG representation are resolved. The plan quality is otherwise strong, but those issues can directly break CTRL-07, CTRL-08, and exact-resume trust.

---

## grok Review

I'll review Phase 41 by reading the plan files first, then checking support docs only where needed to verify concerns.Reading the five plan files and the phase SPEC next.Spot-checking a few risk areas against CONTEXT and existing code.

---

## claude-max Review

I have read the SPEC, all five plans (41-01 through 41-05), and the CONTEXT. I did not need to open AGENTS.md, PROJECT.md, REQUIREMENTS.md, ROADMAP.md, or RESEARCH.md in full — the plans and CONTEXT were internally sufficient to verify the concerns below. All listed files were readable.

Note: these plans are already a **second review cycle** — they embed numerous "HIGH/MEDIUM fix from cross-AI review" annotations. My findings are therefore residual second-order issues, not first-pass gaps.

---

# Phase 41 Plan Review — Config, Checkpointing, Resume & Determinism

## 1. Summary

Five well-structured plans build the control layer over the Phase-40 loop: keyed-YAML config + frozen copy (41-01), production `CheckpointStore` (41-02), guards + determinism modules (41-03), controller wiring (41-04), and the `pinn.train` driver + resume diff (41-05). The wave ordering (1 → {2a,2b} → 3 → 4) is sound, the additive-hook discipline protecting the Phase-40 163/163 regression is disciplined, governance (⚖ provisional seams, `provisional_fields()`, no owner-value invention) is applied consistently, and the SPEC's end-to-end falsifiability floor (CTRL-01/02/05/08) is genuinely exercised. This is a mature plan set. The concerns are localized wiring/semantics issues, most fixable in-plan without redesign.

## 2. Strengths

- **Correct dependency graph.** 41-02/41-03 depend only on 41-01 and touch disjoint files; 41-04 correctly gates on all three; 41-05 on all four. Parallelism is safe.
- **Regression discipline.** Hooks default `None`, `state_dict` keys are additive with `.get()` guards, and the HIGH-5 no-op-default store methods let `CurriculumController`'s unconditional disposition calls stay safe against the naive/empty stores.
- **Single-composer invariant (HIGH-1).** Routing every save path through `build_checkpoint_payload` is the right fix for payload-shape drift vs `fallback_scan`.
- **Security posture is strong.** `yaml.safe_load`-only with a source-grep prohibition test, `weights_only=True` at every load site enforced by the `getsource` count assertion, atomic tmp+fsync+rename with fault-injection tests, disk-floor-safe tiered `failure/` bundle.
- **Scope boundaries respected.** Framework specs stay read-only; canonical JSONL/TensorBoard/ergonomics correctly deferred to Phase 42; calibration to Phase 43. (Writing `pinn/training/*` and `pinn/train.py` is authorized here — v2.0 is the FUT-01 build milestone, not a specwork-ban adjudication milestone.)

## 3. Concerns

**HIGH — Wall-clock trigger has no reset; `elapsed` semantics unpinned (41-02 Task 2).** `should_checkpoint(step, elapsed)` ORs `elapsed >= wall_clock_ceiling_s`, guarded only by `last_written_step`. That guard prevents a *double* write on one step, not repeated firing on *subsequent* steps: once the ceiling is first crossed, if `elapsed` is measured since run-start (not reset on write), every later step satisfies the wall-clock condition and passes the step guard → a checkpoint every step, defeating retention. The plan never pins `elapsed` = time-since-last-checkpoint nor a `last_written_time` reset. Worse, the acceptance test ("a write when the ceiling fires first") would **pass even with the bug**, since it asserts a single fire, not that the *next* step does not re-fire. Fix: define `elapsed` as since-last-checkpoint (reset on every write), and add an AC that the step immediately after a wall-clock write does not re-trigger from the clock alone.

**HIGH — `CHECKPOINT_SCHEMA_VERSION` ownership is inverted across waves (41-02 vs 41-04).** `fallback_scan` in 41-02 (wave 2) must validate `schema_version == <current>`, but the canonical constant is defined in `controllers.py` in 41-04 (wave 3). Since the store is injected *into* controllers, having `checkpoint.py` import the constant from `controllers.py` risks a circular import and a backward wave dependency; hardcoding it in 41-02 instead creates two sources of truth that can silently drift. Fix: define `CHECKPOINT_SCHEMA_VERSION` in a wave-1/wave-2 module (`checkpoint.py` or a shared constants site) and have 41-04 import it.

**MEDIUM — Checkpoint-hook access to *live* `curriculum_state`/`config_identity` is underspecified (41-04 Task 2).** The hook is described both as "called with the global step" and as calling `build_checkpoint_payload(self, curriculum_state, config_identity, …)` from inside `RunController` — but `RunController` does not own the curriculum stage/phase or the config identity digest. At mid-stage fire time `curriculum_state` must be **live** (current stage index, phase 2a/2b, per-stage epoch), not a snapshot, or the rolling checkpoint records the wrong stage. Pin whether the hook is a closure injected by `pinn.train`/`CurriculumController` capturing a live state accessor, and reconcile the `hook(global_step)` signature with the payload-composer call.

**MEDIUM — `fallback_scan` structural validity must treat `optimizer=None` as valid-present.** Stage-init anchors legitimately carry `optimizer: None` (CTRL-06). Anchors are enumerated fallback candidates, so a validity check implemented as truthiness (`payload.get("optimizer")`) rather than key-presence (`"optimizer" in payload`) would wrongly reject a valid anchor and raise a false `NoValidCheckpointError`. The plan says "required keys present" but never calls out the `None`-is-valid case; add an explicit AC.

**MEDIUM — CTRL-08 frozen-config RNG carriage is deferred as a ⚖ seam, leaving a locked AC conditionally unmet at phase close (41-01/41-05).** SPEC AC for CTRL-08 states "the frozen config **and** a checkpoint both contain all four RNG streams," and CTX-51/62 require both. The plans (defensibly, per surface-don't-invent governance) register `frozen_config_rng_recording_format` as owner-carved and make 41-05's config-half assertion *conditional*. Consequence: if the owner does not pick a representation during the build, `freeze_resolved_config` ships a pure-TrainingConfig freeze and the config never carries RNG — a locked AC is unsatisfied by design. Flag the phase-close implication explicitly. (Consider whether candidate A — an ignored `_runtime_state` sidecar key — is mechanical enough to implement directly, since it satisfies both CTRL-01 re-parse-equality and CTRL-08 carriage cleanly; that would let Phase 41 actually close CTRL-08 rather than gate it on ratification.)

**MEDIUM — `strict_cpu_determinism` is unclassified for resume, and identity uses config values not effective runtime (41-03/41-05).** Strict-CPU overrides `precision/device` to float64/cpu at runtime, but the identity payload is built from `config.run.precision/device` (unchanged). A strict-flag flip on resume is caught only by the fail-safe unclassified→refuse *default* (assuming the flag is in the walked resolved config), not by explicit classification, and the effective runtime that produced the checkpoint is never recorded in identity. Pin `strict_cpu_determinism`'s classification explicitly and consider recording the effective `RuntimeSpec` in `config_identity`.

**LOW —** (a) Directory-creation ownership before `atomic_write_torch`'s parent-dir `fsync` isn't pinned (store vs `train.py` mkdir of `runs/<name>/checkpoints/`). (b) Seed fan-out (41-05) is handled as an inline assumption rather than a logged gap — acceptable for a build milestone, but borderline against the project's governance posture; confirm the owner is fine with one seed driving both weight-init and sampling. (c) `best.pt`-on-validation-improvement is mechanism-only; no validation signal is exercised end-to-end (SPEC only requires it survive eviction, so acceptable — just confirm intent). (d) Verify commands use the direct `envs/pinn-train/bin/python` path while CONTEXT documents `conda run -n pinn-train`; equivalent, but align to avoid confusion.

## 4. Suggestions

1. Pin `elapsed` = seconds-since-last-checkpoint with a reset on every write; add the "next step does not re-fire from the clock" acceptance check to 41-02.
2. Move `CHECKPOINT_SCHEMA_VERSION` to `checkpoint.py` (or a shared constants module) so 41-02 owns validation and 41-04 imports it — removes the backward dependency and circular-import risk.
3. In 41-04, specify the checkpoint-hook as a closure capturing a **live** curriculum-state accessor + `config_identity`, and reconcile its signature; add an AC that a mid-stage rolling checkpoint records the correct current stage.
4. Add explicit ACs: `fallback_scan` accepts an anchor with `optimizer=None`; a stage-init anchor is a valid recovery target.
5. Resolve the CTRL-08 frozen-config-RNG representation decision before phase close (or implement the low-risk sidecar candidate) so the locked AC is met rather than deferred; document the phase-close contingency either way.
6. Explicitly classify `strict_cpu_determinism` in `RESUME_FIELD_REGISTRY` and record the effective `RuntimeSpec` in the identity payload.

## 5. Overall Risk: **MEDIUM** (low-medium)

The plans are coherent, well-grounded, and already hardened by a prior review cycle; they achieve the phase goal structurally. The two HIGH findings (wall-clock repeated-firing with a blind acceptance test; schema-version ownership inversion) are the ones most likely to cause execution-time failures or silent misbehavior if unaddressed, but both are fixable in-plan without architectural change. Resolving the six prioritized items above would bring residual risk to LOW.

---

## claude-kimi Review

Execution error
---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=241
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=5768
- stderr_bytes=592503

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=61
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T055626Z-56749/xreview-prompt-41.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=1907
- stdout_bytes=236
- stderr_bytes=0

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=288
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=9482
- stderr_bytes=0

### claude-kimi
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=15
- stderr_bytes=192

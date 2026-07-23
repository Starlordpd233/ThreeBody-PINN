---
phase: 41
reviewers: [codex, grok, claude-max, claude-kimi]
rerun_reviewers: [claude-max, codex, claude-kimi, grok]
reviewed_at: 2026-07-18T06:24:10Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T061808Z-77497
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 41

## codex Review

## 1. Summary

All Phase 41 plan files were readable. The plan set is strong and close, but I would not execute it as-is: two issues can let the phase appear green while missing locked behavior, especially `--resume <ckpt>` semantics and CTRL-08 frozen-config RNG recording.

## 2. Strengths

- Clear wave ordering: config/atomic IO first, checkpoint + determinism modules next, controller wiring, then `pinn.train`.
- Good attention to prior high-risk findings: single checkpoint payload composer, `CHECKPOINT_SCHEMA_VERSION` ownership, `weights_only=True`, path traversal, run-folder collision, and strict-CPU false-safety.
- Strong test-first structure with focused Phase 41 tests plus Phase 40 regression coverage.
- Good fail-closed posture for YAML keys, checkpoint schema validation, resume config drift, and unsafe run names.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- HIGH - `--resume <ckpt>` may not load the checkpoint the user supplied. `41-05` says the resume path uses `store.load_latest / fallback_scan`, while `41-02` only defines `load_latest`, `rollback`, and `fallback_scan`, not a validated “load this exact path” API. That conflicts with `--resume <.../stage-{k}-final.pt> --hold-stage`, which depends on the supplied anchor being loaded, not whatever `latest.pt` resolves to. See [41-05-PLAN.md:39](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:39), [41-05-PLAN.md:164](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:164), [41-02-PLAN.md:76](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-02-PLAN.md:76).

- HIGH - CTRL-08’s “frozen config carries all four RNG streams” acceptance is weakened into a conditional/provisional seam. The spec requires RNG in frozen config and every checkpoint, but `41-01` leaves the representation undecided and `41-05` only tests the config half conditionally. That can complete the phase without satisfying the literal requirement. See [41-SPEC.md:61](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-SPEC.md:61), [41-01-PLAN.md:31](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-01-PLAN.md:31), [41-05-PLAN.md:199](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:199).

- MEDIUM - `best.pt` has retention semantics but no clear producer. `CTX-54` says `best.pt` is updated on validation improvement, and `41-02` adds store-side support, but the controller/entrypoint plans do not clearly wire validation-improvement detection into a `best.pt` write or add an end-to-end assertion that `best.pt` is created/updated. See [41-CONTEXT.md:96](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-CONTEXT.md:96), [41-02-PLAN.md:144](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-02-PLAN.md:144).

- MEDIUM - L-BFGS guard placement is mechanically ambiguous. The existing L-BFGS non-finite signal is set inside the closure and checked after `optimizer.step(closure)`, while `41-04` says the guard runs first in both optimizer phases. Without a pinned L-BFGS-specific hook point, a non-finite closure can still take the old bare RECOVER path or save a failure checkpoint after the risky optimizer step. See [controllers.py:527](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:527), [controllers.py:577](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/controllers.py:577), [41-04-PLAN.md:21](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-04-PLAN.md:21).

- MEDIUM - The B-5 identity registry lists external identity categories that are not actually represented in the identity payload. Dataset version/hash, split policy, and loss-catalog structure are part of the Conservative identity line, but `build_identity_payload` mainly spans config, architecture, constants, and effective runtime. Registering unresolved categories as provisional does not by itself let resume detect drift in absent fields. See [41-CONTEXT.md:119](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-CONTEXT.md:119), [41-05-PLAN.md:24](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/41-config-checkpointing-resume-determinism/41-05-PLAN.md:24).

## 4. Suggestions

- Add a store-mediated `load_checkpoint(path)` / `load_resume_checkpoint(path)` that validates the exact supplied checkpoint with `weights_only=True`, schema checks, and path/run-root checks; test that `--resume <stage-k-final.pt>` restores that file specifically.
- Resolve the frozen-config RNG representation before execution, or formally change CTRL-08. The config-side RNG acceptance should be unconditional.
- Add explicit `best.pt` wiring from validation improvement and an end-to-end test proving it is written and preserved.
- Add separate Adam and L-BFGS guard tests. For L-BFGS, pin whether the guard runs inside the closure or immediately after closure evaluation but before any bare RECOVER path.
- For unresolved B-5 identity categories, either add concrete recorded fields or make their absence an explicit pre-run refusal/blocker.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

HIGH. The plans are well-structured, but the resume-path and frozen-config RNG gaps are requirement-level risks, not implementation details.

---

## grok Review

I'll review the Phase 41 plans against the stated focus areas, starting with the five plan files and only pulling context when needed to verify findings.Extracting goals, tasks, dependencies, and acceptance criteria from all five plans in parallel.

---

## claude-max Review

I have now read all five plans plus the SPEC and CONTEXT. Below is my review.

---

# Cross-AI Plan Review — Phase 41 (Config, Checkpointing, Resume & Determinism)

## 1. Summary

Five plans decompose the control layer that wraps the Phase-40 loop into a clean dependency DAG: **41-01** (wave 1: `atomic_io`, config extensions, keyed-YAML resolver, test scaffold) → **41-02**/**41-03** (wave 2, parallel: production `CheckpointStore`; guards + determinism) → **41-04** (wave 3: `controllers.py` hooks + single `build_checkpoint_payload` composer + Adam-reset composition) → **41-05** (wave 4: `resume.py` + `pinn.train` driver + end-to-end floor). All eight CTRL requirements are mapped to concrete tasks with TDD acceptance tests, per-plan STRIDE threat models, and additive Phase-40 compatibility. These are unusually mature plans — they already carry two prior cross-AI review cycles (codex/grok/claude-max HIGH/MEDIUM fixes threaded inline), and the governance posture (⚖ provisional seams, no invented owner values, fail-safe defaults) is disciplined and correct. All files stay inside `pinn/training/`, `pinn/train.py`, and `tests/phase41/`; no spec edits, no Phase-42 logging schema, no threshold calibration. I read all five plans directly plus 41-SPEC and 41-CONTEXT; all files were readable.

## 2. Strengths

- **Wave/dependency graph is correct and cycle-free.** `CHECKPOINT_SCHEMA_VERSION` is owned by 41-02 (wave 2) and imported by 41-04 (wave 3) with `checkpoint.py` explicitly *not* importing `controllers.py` — the single-source-of-truth + no-circular-import reasoning holds.
- **Single-composer discipline (HIGH-1 fix).** Routing every save site through `build_checkpoint_payload` closes the payload-drift-vs-`fallback_scan` class of bug at the root.
- **Governance is right for a build milestone.** Owner-carved values (D4-a ceiling, R-1 thresholds, B-5 field list) are ⚖ seams registered in `provisional_fields()`; unclassified-→-refuse is the fail-safe default; no ratified number is minted.
- **Security is threaded, not bolted on:** `yaml.safe_load`-only, `weights_only=True` at every load site with a source-count prohibition test, atomic tmp+fsync+rename, run-name path-traversal hardening, fail-closed run-folder collision.
- **Additive Phase-40 compat is defended** by no-op store defaults (HIGH-5) and `.get(...)`-guarded state keys, with the 163/163 regression re-run inside verify commands.

## 3. Concerns

**HIGH — CTRL-08 frozen-config RNG carriage is deferred, leaving a locked acceptance criterion unmet in-phase.**
CTRL-08's acceptance explicitly requires "the frozen config **and** a checkpoint both contain all four RNG stream states." The plans surface a real CTRL-01↔CTRL-08 tension (config.yaml must re-parse *equal* to `TrainingConfig` yet also carry RNG) and resolve it by registering `frozen_config_rng_recording_format` as an **UNDECIDED** ⚖ seam and shipping *neither* candidate representation (41-01 freezes a pure `TrainingConfig`; 41-05 asserts the config-half only "conditionally on whichever representation 41-01 implemented" — which is none). Net effect: the checkpoint-half of CTRL-08 lands, the **config-half does not**, and phase closure depends on an owner decision the plans do not schedule inside the phase. Candidate (A) — a top-level `_runtime_state` key that `load_config` ignores — is a standard, low-risk, re-parse-safe pattern; escalating it to owner ratification is arguably over-caution that converts a mechanical serialization choice into a blocked acceptance criterion. Recommend either (a) implement representation A now and keep the "which representation" question as a documented, reversible default, or (b) get explicit owner sign-off that CTRL-08's config-half may close deferred — before `/gsd-verify-work` runs against the SPEC checklist.

**MEDIUM — `save_rolling` (and the best/latest update path) is referenced downstream but not defined in 41-02's store surface.**
41-04 and 41-05 call `store.save_rolling(...)`, but 41-02's enumerated method surface is `save`/`load_latest`/`rollback`/`should_checkpoint`/`save_anchor`/`record_disposition`/`promote`/`fallback_scan` — no `save_rolling`. This is a cross-wave interface contract gap that will surface as an `AttributeError` or a guess at integration. Relatedly, `best.pt` is "(re)written only on a validation improvement," but the minimal dataset-free driver has no validation signal, so the best-path is never exercised end-to-end and the retention tests must synthesize a `best.pt` out-of-band. Pin the exact rolling/best/latest method names and their trigger arguments in 41-02 so 41-04/41-05 bind to a committed surface.

**MEDIUM — mid-stage resume of live Adam optimizer state is under-specified.**
Boundary resume is handled precisely (init anchor carries `optimizer=None` → fresh Adam). But `load_state_dict` restores the optimizer "into a live optimizer *when one exists*." On a `--resume` from a **rolling** `step-*.pt` (mid-stage), the fresh Adam is built by `run_stage` *after* the composition root loads state — so at `load_state_dict` time `self._optimizer` may be `None`, silently skipping the moment-buffer restore and defeating exact continuation of Adam state. The exact-continuation test (41-05 Task 3) should exercise a genuinely mid-stage checkpoint, and the plans should pin the build-then-load ordering (build fresh optimizer, *then* apply the checkpointed optimizer state) for the rolling-resume path.

**MEDIUM — `--hold-stage` on a non-final checkpoint has no typed-error guard or test.**
41-SPEC Edge R5 lists "`--hold-stage` from a non-final checkpoint → typed error" as *covered*, but no plan implements or tests rejecting `--hold-stage` against a rolling `step-*.pt` (or any non-`stage-{k}-final` anchor). Only the happy path (from `stage-{k}-final.pt`) is tested. Add the fail-closed guard + negative test.

**LOW — guard HALT-family disposition may be flattened to RECOVER at the controller boundary.** `guards.py` computes "RECOVER/HALT per family," but the 41-04 wiring states the guard trip "returns `StageDisposition.RECOVER`" and the ledger records RECOVER. Correctness then relies entirely on stage-exit `retries:0` escalating to HALT; a disk-floor/loss-explosion HALT-family trip could be journaled as RECOVER. Pin how the guard's family disposition reaches `record_disposition`.

**LOW — `failure-stage-{k}-step-{step}` anchors: retention/fallback interaction.** These are anchor-class (never rolling-evicted) and unique per step, so repeated trips accumulate unbounded; they also don't match the `stage-*` exclusion prefix, and `fallback_scan` (which enumerates "anchor `.pt` files") could select a structurally-valid *failure* checkpoint as the newest-valid on a corrupt `latest.pt` — i.e., auto-resume from a failure state. Worth an explicit naming class + fallback exclusion.

**LOW — production `elapsed` clock source and MPS test-determinism.** The checkpoint hook "reads elapsed from `store.last_written_time`" via `StubClock` in tests; the production monotonic source (`time.monotonic()`) isn't pinned. Separately, the exact-continuation assertion is only stable under CPU/float64 (MPS lacks deterministic kernels); the entrypoint test config must force CPU/float64 (or `strict_cpu`) or the "matches to floating tolerance" trajectory check risks flakiness.

## 4. Suggestions

1. Resolve the CTRL-08 frozen-config-RNG deferral before execution — prefer implementing representation A as a reversible default with a `⚖`-tagged note, rather than closing the phase on an unscheduled owner decision.
2. Add `save_rolling`/`save_best`/`latest` (or a single `save(..., klass=...)` signature) to 41-02's committed method surface and update 41-04/41-05 to bind to it verbatim.
3. Pin the rolling-resume optimizer ordering (build fresh Adam → load optimizer state) and make 41-05's `ExactContinuationTests` checkpoint mid-stage, not only at a boundary.
4. Implement + test the `--hold-stage`-on-non-final-checkpoint typed error (closes SPEC Edge R5 as claimed).
5. Add a naming class for `failure-*` checkpoints and exclude them from `fallback_scan` candidate selection; consider a bounded cap.
6. State the production monotonic clock and force CPU/float64 in the exact-continuation entrypoint test.

## 5. Overall Risk: **MEDIUM** (low-medium)

The architecture is sound, well-grounded, security-conscious, and strongly protected against Phase-40 regression; nothing here is structural or destructive. The rating is driven by one HIGH (a locked acceptance criterion left open on an unscheduled owner decision) plus a small cluster of cross-wave interface/ordering under-specifications (`save_rolling`, mid-stage Adam restore, `--hold-stage` non-final guard) that are cheap to fix in-plan but would otherwise surface as integration defects or a blocked phase verification. Resolve the HIGH and the three MEDIUMs before executing wave 3–4.

---

## claude-kimi Review

_claude-kimi failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=1
- stderr_bytes=192

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T061808Z-77497/xreview-claude-kimi-41.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T061808Z-77497/xreview-claude-kimi-41.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T061808Z-77497/xreview-claude-kimi-41.meta

Stdout excerpt:
```


```

Stderr excerpt:
```
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors

```

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=238
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=5895
- stderr_bytes=568382

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=33
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T061808Z-77497/xreview-prompt-41.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=1185
- stdout_bytes=249
- stderr_bytes=0

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=339
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=8967
- stderr_bytes=0

### claude-kimi
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=1
- stderr_bytes=192

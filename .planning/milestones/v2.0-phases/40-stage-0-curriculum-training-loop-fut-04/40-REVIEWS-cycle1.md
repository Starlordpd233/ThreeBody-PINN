---
phase: 40
reviewers: [grok, claude-kimi, claude-glm, claude]
rerun_reviewers: [grok, claude-kimi, claude-glm, claude]
reviewed_at: 2026-07-17T04:05:07Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T035803Z-85327
---

# Cross-AI Plan Review — Phase 40

## grok Review

I'll review the Phase 40 plans by reading the plan files first, then checking support docs only where needed to validate concerns.Checking a few integration points and edge cases against CONTEXT and existing code patterns.

---

## claude-kimi Review

Execution error
---

## claude-glm Review

I've reviewed the SPEC, all six plans (40-01…40-06), and the CONTEXT decision provenance, and cross-checked the plans against REQUIREMENTS TRAIN-01…07. Here is the review.

---

# Phase 40 Plan Review — Stage-0 Curriculum Training Loop (FUT-04)

## 1. Summary

Phase 40 builds the **training driver layer** (`pinn/training/`) — `CurriculumController` (outer stage loop) and `RunController` (inner Adam→L-BFGS loop) — on top of the Phase-38 model and Phase-39 data substrate. The six plans decompose cleanly into a dependency-ordered wave sequence:

- **40-01** (W1): test scaffold + fixtures + dynamic prohibitions audit
- **40-02** (W2): PHYS-05 `ScheduledWeights` + `GradClipper` (TRAIN-03/05)
- **40-03** (W2): `CollocationSampler` + sL-BFGS preflight refusal (TRAIN-04/07)
- **40-04** (W2): `StageExitMachine` + `TrainingConfig` + `CheckpointStore` seam (TRAIN-06)
- **40-05** (W3): `RunController` + `PlateauDetector` (TRAIN-02)
- **40-06** (W4): `CurriculumController` + package barrel + full-suite gate (TRAIN-01)

All seven TRAIN requirements are covered by numerically-defined, dataset-free unittest contracts, and every `files_modified` entry stays inside `pinn/training/` and `tests/phase40/` — no scope creep into the model, data, or spec layers. The plans transcribe the locked `ctl_instruction.md` Stage-0 contract rather than re-deciding it, consistent with the project's STOP-protocol governance.

## 2. Strengths

- **Provenance hygiene is excellent.** CTX-34 explicitly *corrects* a SPEC over-claim (SPEC:84's "trainex-r1a-ratified" for `C_stage=8.5`), re-grounding it on REQUIREMENTS TRAIN-05 while flagging the value provisional for ACC-05. This is exactly the grounding discipline the project demands.
- **Correct disambiguation of the two plateau criteria** (CTX-46 / RESEARCH Pitfall 4): the within-stage Adam→L-BFGS handoff (`log10` slope > −5e-3, 50 consecutive epochs) is kept as a separate object from CURR-03 gate criterion 1 (β=0.98 EMA, patience 200), with separate state and separate tests.
- **Subtle numeric pitfall caught:** `torch.median`'s even-length (lower-middle) semantics are made load-bearing in 40-02 with a test that a `numpy.median` reference would fail.
- **Defense-in-depth on the sL-BFGS refusal:** TRAIN-07 is tested at the preflight unit (40-03), wired into `CurriculumController` before any stage entry, and asserted at the integration level (40-06).
- **Clean seam carving for Phases 41/42/43:** `TrainingConfig` dataclasses, the `CheckpointStore` Protocol, and the `logging.getLogger('pinn.training.*')` tree are explicitly narrow interfaces later phases swap impls behind without touching controller code.
- **Edge coverage (SPEC 5/5) is reflected in the plans:** cold-start k=0, final-stage replay-only, NaN/Inf in either phase, retry exhaustion, and the partial-window clip backstop all land as concrete tests.

## 3. Concerns

### HIGH

- **H1 — The validation-loss-stability producer for ADVANCE-gate criterion 2 is undescribed in `RunController`.** The four-criterion ADVANCE gate (TRAIN-06) requires "validation-loss stability on a held-out set." CTX-49 defines the cadence (`validation_every=10`) and states it feeds "criterion 2's min-tracking," and CONTEXT identifies the Phase-39 stage-stratified split as what "the gate's held-out validation consumes." But the 40-05 epoch step-ordering (`zero_grad → forward → isfinite → backward → clip → step → scheduler.step → PlateauDetector.update`) contains **no validation forward pass and no validation-loss tracking**, yet "at stage end, RunController calls `StageExitMachine.evaluate(...)`" which needs that signal as an input. Because every gate test injects the signal (40-04) and every controller test forces the disposition (40-06), the gap is invisible to the planned tests. As written, the ADVANCE gate is only ~3/4 wired for a real (non-injected) run. *Recommendation:* either add an explicit validation-pass task to 40-05 (it is testable dataset-free against the stub source's held-out portion), or state explicitly in the plan that criterion-2 is injected/deferred and have `StageExitMachine` tolerate a not-yet-produced signal. This is mechanical wiring, not threshold calibration, so it does not belong to Phase 43.

### MEDIUM

- **M1 — L-BFGS accumulate-in-closure chunking has no correctness test and no specified scaling.** 40-05 implements gradient accumulation across fixed-size sub-chunks ("zero_grad once, backward per chunk, return the summed/scaled loss") with the chunk size as a config knob, but the only L-BFGS tests are the no-resample spy, λ-frozen spy, clip-count-0 spy, and NaN→RECOVER. There is no assertion that the accumulated gradient equals the full-batch gradient, and the per-chunk loss *scaling* (how chunks combine into the L-BFGS objective) is unspecified. A wrong scale silently distorts the quasi-Newton objective. Add a small test that chunked accumulation matches a single full backward on a tiny batch.
- **M2 — The full-batch L-BFGS memory bound (T-40-08) is mitigated by a mechanism whose default is unvalidated in Phase 40.** All tests run CPU/float64 on tiny stub fixtures, so neither the "256-trajectory full-batch" assumption (RESEARCH Open Question 1) nor the chunk-size default is ever exercised at M5-Pro scale. This is *by design* deferred to Phase 43 ACC-02, but it means Phase 40's green suite does not demonstrate the heaviest runtime risk is bounded — only that the chunking *knob* exists.
- **M3 — Finite L-BFGS divergence / line-search stall may not route to RECOVER.** The SPEC's edge table asserts "L-BFGS line-search failure routes to RECOVER," but the implemented detector is NaN/Inf only (`error_if_nonfinite` / `isfinite`). `torch.optim.LBFGS` with `strong_wolfe` does not raise on a finite line-search stall; it takes a step. Clarify whether a finite-but-diverging L-BFGS step is a RECOVER trigger, or narrow the SPEC's "line-search failure" wording to mean "non-finite."

### LOW

- **L1 — `40-06 depends_on` omits 40-02.** `CurriculumController` calls `ScheduledWeights.rewarm()` (a 40-02 symbol). It is transitively satisfied via 40-05 → 40-02, so this is a cleanliness issue, not a correctness one; listing 40-02 explicitly would make the dependency graph self-documenting.
- **L2 — `CheckpointStore.rollback()` semantics on an empty store (k=0, pre-first-save) are undefined.** If RECOVER fires during the first stage before any `save`, the "last well-formed checkpoint" may not exist. Impact is low because CTX-41 routes RECOVER-at-retries-0 → HALT regardless, but the naive impl's rollback-on-empty behavior should be specified and tested.
- **L3 — The high-severity deserialization threat (T-40-02) is mitigated by *payload cleanliness*, not by actually loading with `weights_only=True` in Phase 40.** The naive `torch.save`/`torch.load` impl keeps payloads clean so Phase 41 can turn the flag on (CTRL-03), but the active mitigation (the flag itself) lands in a later phase. Fine as a seam, but the threat-model "mitigate" disposition slightly outruns what Phase 40 actually enforces.
- **L4 — The accumulate-in-closure chunk-size default is left as a "plan-time CTX decision" made during execution.** Under the U-6 "set-at-implementation with logged rationale" precedent this is permissible, but the executor should log it as provisional; there is mild risk an unlogged pick reads as ratified.

## 4. Suggestions

1. **Resolve H1 before execution** — it is the only finding that affects whether the phase goal ("runs the Stage-0 curriculum end-to-end") is actually met at the wiring level. A one-task addition to 40-05 (validation forward pass at `validation_every`, feeding criterion 2) closes it cleanly.
2. **Add the M1 chunked-accumulation equality test** — cheap, and it pins a numerical-correctness property the current spy tests do not.
3. **Tighten the SPEC/plan wording around "L-BFGS line-search failure" (M3)** so the RECOVER trigger is unambiguous (non-finite vs. finite divergence).
4. **Add 40-02 to 40-06's `depends_on`** for graph readability (L1).

## 5. Overall Risk

**MEDIUM.** The plans are high-quality: well-grounded, well-scoped, strongly provenanced, with disciplined edge coverage and correct dependency ordering. No scope creep, no destructive-operation exposure beyond the acknowledged checkpoint-seam carve-out. The rating is driven by **H1** (an incompletely-wired ADVANCE-gate criterion whose absence the planned tests cannot detect) plus the by-design deferral of all real-scale validation to Phase 43 (M2). Resolving H1 and adding the M1 test would bring this to LOW.

---

## claude Review

I've read all six plans plus the SPEC/CONTEXT sections needed to verify specific concerns. Review follows.

---

# Phase 40 Plan Review — Stage-0 Curriculum Training Loop (FUT-04)

## 1. Summary

Six plans decompose FUT-04 into a 4-wave dependency graph: a dataset-free test scaffold (40-01), two pure-numeric leaf modules (40-02), two small interface modules (40-03), three seam types (40-04), the inner Adam→L-BFGS loop (40-05), and the outer curriculum loop + barrel (40-06). All seven TRAIN-01..07 requirements are claimed, each SPEC acceptance criterion maps to a named test, and the governance posture is unusually strong — every provisional constant (C-table, median floor, λ^max, `max_iter=20`) carries provenance and is config-overridable rather than cited as ratified. CTX-34's provenance correction (8.5 is *not* trainex-r1a-ratified) is correctly propagated into 40-02 rather than inheriting SPEC.md:84's bad citation.

The decomposition is sound and the phase goal is achievable as planned. My concerns are concentrated in two integrator plans (40-05, 40-04) and are mostly under-specification at cross-plan seams, not wrong direction.

All listed files were readable; no file access failures.

## 2. Strengths

- **Dependency ordering is genuinely correct.** Waves respect the real graph; the two plans that share `controllers.py` (40-05, 40-06) are in different waves, so no write conflict.
- **`test_prohibitions` uses filesystem discovery, not a hardcoded module list** — later plans are audited automatically without editing 40-01's file. This is the right call and is explicitly stated as an AC.
- **The two plateau criteria are held apart deliberately.** CTX-46's handoff detector vs CURR-03's β-smoothed stage-exit plateau is called out in three separate plans (40-02, 40-04, 40-05) with an explicit "do not share state" prohibition. This is RESEARCH Pitfall 4 and it's handled.
- **`torch.median` even-length semantics are load-bearing and treated as such** — 40-02 forbids a numpy/statistics reference in the *test*, not just the impl. That's the correct place to enforce it.
- **Gate is tested on form, not calibrated pass level** — consistent with SCOPE-19 and the STOP protocol. No invented thresholds anywhere I could find.

## 3. Concerns

### HIGH — The Adam phase has no stated termination bound
40-05 Task 2 specifies the per-epoch loop and says "break on `PlateauDetector.fires()`", but never states that the Adam phase also terminates at `N_Adam,k` / `MAX_EPOCHS`. This directly collides with the plan's own AC: *"a descending curve never fires the detector"* — driven through `RunController`, that test does not terminate. `T_max = N_Adam,k` appears only as the cosine scheduler horizon (CTX-48), not as a loop bound, and `MAX_EPOCHS` reaches `StageExitMachine` only *after* the stage ends. Add an explicit `for epoch in range(N_Adam_k)` bound plus a MAX_EPOCHS→HALT path, and make "descending curve exits the Adam phase at the budget without handoff" an AC.

### HIGH — "clip-call count = 1" is unimplementable as specified
40-02 has `GradClipper` call `torch.nn.utils.clip_grad_norm_` **twice** per Adam step: once with `max_norm=inf` to measure the pre-clip norm, once with `clip_value` to apply. 40-05's AC (and SPEC AC-5b) require a spy showing **exactly 1** call in an Adam step. If the spy patches `clip_grad_norm_`, the count is 2 and the AC fails as written; if it patches `GradClipper.clip`, the count is 1 but the test no longer proves the *torch-level* clip path is untaken during L-BFGS — which is the property that actually matters. Neither plan names the spy target. Pin it explicitly (recommend: spy `GradClipper.clip` for the 1/0 count **and** additionally assert 0 `clip_grad_norm_` calls across the L-BFGS step).

### MEDIUM — 40-04 task order inverts its own dependency
Task 1 (`stage_exit.py`) TDD-builds against injected config and its AC says *"thresholds are read from the injected config (no literal 0.98/200/1e-5/1e-4)"* — but `config.py` is Task 2. Task 1's `verify` command runs before the config type exists. Swap the tasks (config → stage_exit) or state that Task 1's tests inject a local stub config object.

### MEDIUM — Collocation points have two sources with no stated precedence
`build_stage_batch(...)` already returns `collocation_points` (40-01 fixture surface; `collocation_count=4096`), and 40-05 *also* calls `CollocationSampler` each epoch for physics points. Which one feeds `causal_physics_loss`? If both, the budget is double-counted. Name the winner in 40-05 and say what happens to `FixedBatch.collocation_points`.

### MEDIUM — The accumulate-in-closure chunk-size knob has no home
40-05 requires chunk size to be "a config knob", but 40-04's `TrainingConfig` run/stage/opt/loss sections never mention it, and 40-04 is the plan that owns config. Add the field to 40-04's opt section (with a provisional tag, since RESEARCH Open Question 2 leaves it open) or 40-05 will invent a field in a frozen dataclass it doesn't own.

### MEDIUM — Checkpoint threat T-40-02 is rated `high` but only half-mitigated
The mitigation ensures *payloads* are `weights_only`-clean and tests assert no callables are saved. But the naive impl's `torch.load` is not specified to pass `weights_only=True`, so the actual deserialization path stays unsafe against a *tampered* checkpoint file — which is the threat as written ("a checkpoint that pickles arbitrary Python objects enables code execution on load"). Since the payload is already clean by construction, setting `weights_only=True` now is free and closes the threat rather than deferring it to Phase 41. Make it an AC.

### MEDIUM — The forced-disposition injection seam is an un-gated ADVANCE bypass
40-06 makes forced-disposition injection a first-class constructor/method seam (correctly, per SPEC "not monkey-patching"). But T-40-09 rates spurious stage advance `high`, and this seam is precisely a supported way to force `Δstage=+1` without the gate. No AC constrains it. Add: the injection parameter defaults to `None`/absent, and supplying both a live `RunController` and a forced disposition raises (or the seam is documented as test-only and asserted unset on any real run path).

### MEDIUM — TRAIN-06's full acceptance chain is unclaimed by any plan
SPEC AC-6(b) is *"NaN/Inf → RECOVER rollback → HALT/REVIEW at `recover.retries: 0`"* — the whole chain. 40-04 owns `requirements: [TRAIN-06]` but tests only the RECOVER *disposition*. The rollback→HALT half is tested in 40-06, whose `requirements:` lists only `[TRAIN-01]`. The behavior is covered; the traceability isn't. Add TRAIN-06 to 40-06's requirements list.

### LOW — 40-06 `depends_on` omits 40-02
`CurriculumController` calls `ScheduledWeights.rewarm()` (a 40-02 artifact) directly. Satisfied transitively via 40-05, but the declared graph should be explicit.

### LOW — 40-01 internal inconsistencies
(a) The action says `discover_training_modules()` "globs `pinn/training/*.py`, dynamically (rglob)" — glob and rglob are different; pick one. (b) The action requires a `simulation_data` corpus-path ban token, but the AC enumerates only the v1.3 and global-default sets, so the ban is untested. (c) Substring token bans (`is_available`) will false-positive on any legitimately-named attribute; scope to `torch.*.is_available` or accept and document.

### LOW — Median window includes the current step's own norm
40-02 appends-then-medians, so a step's norm influences its own clip threshold. This is *correct* per CTX-35 ("at step 1, `clip = C_stage × that single norm`" only holds if the current norm is included), but it's an inference from an edge case rather than a stated rule. Say so explicitly in the module docstring so a future reader doesn't "fix" it.

## 4. Suggestions

1. **Fix the two HIGH items before execution** — both are cheap at plan time and expensive at test time (one hangs a test suite, one fails an AC that traces to a SPEC criterion).
2. **Add an Adam-budget AC to 40-05**: "a descending L_phys curve exits the Adam phase at `N_Adam,k` without handoff and does not hang."
3. **Reorder 40-04 to config → stage_exit → checkpoint**, matching the real dependency.
4. **Give 40-05 a seam-inventory paragraph** listing every field it reads from `TrainingConfig` (chunk size, `N_Adam,k`, `max_iter`, `validation_every`), so 40-04 can provision them all rather than 40-05 discovering gaps mid-execution.
5. **Consider a `tests/phase40/test_seams.py`** asserting the barrel's four types and that no controller field reads a threshold not enumerable as provisional — this would mechanize the CTX-38 "which values were uncalibrated" guarantee that currently rests on judgment review.

## 5. Overall Risk

**MEDIUM.**

Direction, decomposition, and governance are sound — no scope creep past the SPEC boundary, no invented science, no destructive operations, and the `pinn/` live-code ban and specwork/build separation are respected. Risk sits entirely in 40-05, which carries the phase's real engineering weight and has two concrete under-specifications (unbounded Adam loop, ambiguous clip-spy target) plus two unowned seams (chunk-size knob, collocation-point precedence). Those are plan-level fixes, not redesigns. With the HIGH items resolved and the 40-04 task order swapped, this drops to LOW.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=39
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T035803Z-85327/xreview-prompt-40.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=1980
- stdout_bytes=223
- stderr_bytes=0

### claude-kimi
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=15
- stderr_bytes=192

### claude-glm
- reviewer=claude-glm
- exit_code=0
- elapsed_seconds=424
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=8648
- stderr_bytes=192

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=147
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=9376
- stderr_bytes=0

# Phase 40 plan source-grounding audit

## Verification coverage

**Authority: grep** (ripgrep over `<home>/Desktop/3_body_problem/.worktrees/trainex`, branch `milestone/v2.0`). Read-only pass over `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-0{1..6}-PLAN.md`. Every symbol the plans treat as already-present was checked; symbols the plans themselves create are excluded and attributed below. Plan-line citations are `40-NN-PLAN.md:line`. No repo file was modified.

**Verdict counts:** VERIFIED 147 · MISSING 3 · AMBIGUOUS 2 · UNCHECKABLE 14 · excluded-new 61. No hardBlock=true.

### 1. VERIFIED — existing file paths (32)

| # | Path (kind: file path) | Plan line (quote) | Evidence |
|---|---|---|---|
| F01 | tests/phase39/__init__.py | 40-01:76 "tests/phase39/__init__.py (the `_SKIP_PHRASE` single-definition pattern…)" | exists |
| F02 | tests/phase39/_fixtures.py | 40-01:77 "tests/phase39/_fixtures.py (fixture-module structure; note TinyCorpus…)" | exists |
| F03 | tests/phase39/test_batches.py | 40-01:78 "tests/phase39/test_batches.py (the `_Query` and `_DataQuery` duck-typed StageQuery stubs…)" | exists |
| F04 | tests/phase39/test_prohibitions.py | 40-01:109 "tests/phase39/test_prohibitions.py (whole file — discover_pinn_modules/discover_data_modules…)" | exists |
| F05 | tests/phase39/test_admission.py | 40-02:126 "tests/phase39/test_admission.py lines ~37-60 (ConservationBoundaryTests…)" | exists |
| F06 | tests/phase38/test_prohibitions.py | 40-01:110 "tests/phase38/test_prohibitions.py (the _V1_TOKENS ban list form…)" | exists |
| F07 | tests/phase38/test_loss_catalog.py | 40-02:82 "tests/phase38/test_loss_catalog.py (deferred-import _import_symbol skip-guard idiom…)" | exists |
| F08 | tests/phase38/test_network_structure.py | 40-02:83 "tests/phase38/test_network_structure.py lines ~216-232 (state_dict() key-by-key equality idiom…)" | exists |
| F09 | pinn/data/batches.py | 40-01:79 "pinn/data/batches.py (build_stage_batch and select_stage_records…)" | exists |
| F10 | pinn/data/types.py | 40-01:80 "pinn/data/types.py (StageQuery protocol at line 297; RecordKey; …)" | exists |
| F11 | pinn/data/admission.py | 40-02:122 "pinn/data/admission.py lines ~46-73 (ConservationOutcome frozen-result…)" | exists |
| F12 | pinn/data/stages.py | 40-03:111 "pinn/data/stages.py (whole file — the small single-purpose predicate module shape…)" | exists |
| F13 | pinn/data/adapter.py | 40-06:85 "pinn/data/adapter.py mem: line (structured-log-line precedent CTX-45 extends)" | exists |
| F14 | pinn/data/__init__.py | 40-01:111 "pinn/data/__init__.py (minimal barrel + explicit…docstring discipline)" | exists |
| F15 | pinn/network.py | 40-01:81 "pinn/network.py (build_network(spec, *, dtype, device) at line 231)" | exists |
| F16 | pinn/architecture_spec.py | 40-01:82 "pinn/architecture_spec.py (ArchitectureSpec frozen dataclass…)" | exists |
| F17 | pinn/loss_catalog.py | 40-02:79 "pinn/loss_catalog.py (LossWeights frozen dataclass at line 65…)" | exists |
| F18 | pinn/physics_residual.py | 40-02:123 "pinn/physics_residual.py lines ~90-95 (_require_finite fail-loud discipline)" | exists |
| F19 | pinn/runtime.py | 40-04:123 "pinn/runtime.py lines ~23-96 (RuntimeSpec frozen output + resolve_runtime…)" | exists |
| F20 | pinn/constants.py | 40-03:75 "pinn/constants.py line 31 (T_CHARACTERISTIC_TIME = 10.0…)" | exists |
| F21 | pinn/verification/__init__.py | 40-01:112 "pinn/verification/__init__.py (on-demand heavy-submodule deferral…)" | exists |
| F22 | pinn/verification/overfit_probe.py | 40-05:107 "pinn/verification/overfit_probe.py lines ~288-407 (run_overfit…)" | exists |
| F23 | pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | 40-02:80 "pinn_architecture.md §4.1 / PHYS-05" | exists |
| F24 | pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md | 40-04:88 "ctl_instruction.md dual-path stage-transition state machine (~lines 1924-1998…)" | exists |
| F25–F28 | 40-SPEC.md / 40-CONTEXT.md / 40-PATTERNS.md / 40-RESEARCH.md | all plans `<context>` blocks (e.g. 40-01:54-56) | all exist |
| F29–F31 | .planning/ROADMAP.md / STATE.md / REQUIREMENTS.md | `<context>` blocks (e.g. 40-04:63-64) | all exist |
| F32 | <home>/miniforge3/envs/pinn-train/bin/python | every `<verify>` block (e.g. 40-01:94) | exists |

### 2. VERIFIED — code symbols (59)

| Symbol (kind) | Plan line (quote) | Evidence (file:line) |
|---|---|---|
| `_SKIP_PHRASE` phase39 precedent (constant) | 40-01:76 "the `_SKIP_PHRASE` single-definition pattern" | tests/phase39/__init__.py:14 |
| `TinyCorpus` (class) | 40-01:77 "note TinyCorpus is the on-disk parser fixture Phase 40 does NOT need" | tests/phase39/_fixtures.py:174 |
| `_Query` (class) | 40-01:78 "the `_Query` and `_DataQuery` duck-typed StageQuery stubs" | tests/phase39/test_batches.py:114 |
| `_DataQuery` (class) | 40-01:78 (same line) | tests/phase39/test_batches.py:256 |
| `test_selection_is_seed_stable_and_does_not_touch_global_numpy_rng` (method) | 40-03:79 "caller-owned-RNG test test_selection_is_seed_stable_and_does_not_touch_global_numpy_rng" | tests/phase39/test_batches.py:217 |
| `discover_pinn_modules` (function) | 40-01:109 "discover_pinn_modules/discover_data_modules dynamic globbing" | tests/phase39/test_prohibitions.py:172 |
| `discover_data_modules` (function) | 40-01:109 (same line) | tests/phase39/test_prohibitions.py:182 |
| `executable_source` (function) | 40-01:120 "Reuse `executable_source` / `executable_source_from_text` … verbatim" | tests/phase39/test_prohibitions.py:102 |
| `executable_source_from_text` (function) | 40-01:120 (same line) | tests/phase39/test_prohibitions.py:84 |
| `_require` (function) | 40-01:122 "Use the `_require`/deferred-import helper" | tests/phase39/test_prohibitions.py:69 |
| `has_global_default_mutation` (function) | 40-01:36 "tests/phase39 has_global_default_mutation" | tests/phase39/test_prohibitions.py:114 |
| `_GLOBAL_DEFAULT_TOKENS` (constant; `set_default_dtype`/`is_available` ban) | 40-01:121 "no global-default mutation / availability probe tokens set_default_dtype, is_available" | tests/phase39/test_prohibitions.py:66 |
| `test_no_precision_default_in_discovered_modules` (method) | 40-01:36 "mirroring tests/phase38 test_no_precision_default_in_discovered_modules" | tests/phase38/test_prohibitions.py:289 |
| `_import_symbol` (function) | 40-02:82 "deferred-import _import_symbol skip-guard idiom" | tests/phase38/test_loss_catalog.py:32 |
| `ConservationBoundaryTests` (class) | 40-02:126 "lines ~37-60 (ConservationBoundaryTests…)" | tests/phase39/test_admission.py:49 (within claimed range) |
| `build_stage_batch` (function) | 40-05:108 "build_stage_batch(source, *, stage, rng, dtype, device, collocation_count=4096)" | pinn/data/batches.py:355; sig lines 356-361 match `(source, *, stage, rng, dtype, device, …)` |
| `select_stage_records` (function) | 40-01:79 "build_stage_batch and select_stage_records" | pinn/data/batches.py:66 |
| `_require_local_rng` (function) | 40-03:74 "lines ~33-36 (_require_local_rng caller-owned Generator check)" | pinn/data/batches.py:33 (exact) |
| `sample_collocation_points` (function) | 40-03:74 "~289-330 (sample_collocation_points: the rng.uniform(0.0, T_CHARACTERISTIC_TIME…)" | pinn/data/batches.py:289 (exact) |
| `collocation_count=4096` (kwarg default) | 40-05:108 (quote above) | pinn/data/batches.py:296 `collocation_count: int = 4096` |
| `FixedBatch` (class) | 40-05:108 "→ FixedBatch{data_points, collocation_points, replay_keys, lookahead_keys}" | pinn/data/types.py:283 |
| `FixedBatch.data_points` / `.collocation_points` / `.replay_keys` / `.lookahead_keys` (4 dataclass fields) | 40-05:108 (same line) | pinn/data/types.py:291-294 (all four present) |
| `StageQuery` (class, line claim 297) | 40-01:80 "StageQuery protocol at line 297" | pinn/data/types.py:297 (exact line; see AMBIGUOUS-2 for the "protocol" characterization) |
| `RecordKey` (class) | 40-01:80 | pinn/data/types.py:123 |
| `DataFidelityPoints` (class) | 40-01:80 | pinn/data/types.py:257 |
| `PhysicsCollocationPoints` (class) | 40-01:80 | pinn/data/types.py:272 |
| `DataVersionHashMismatch` (exception class) | 40-03:110 "lines ~157-177 (DataVersionHashMismatch / StageZeroUnderpopulated…)" | pinn/data/types.py:157 (in range) |
| `StageZeroUnderpopulated` (exception class) | 40-03:110 | pinn/data/types.py:165 (in range) |
| `has_stage` (method) | 40-01:88 "answers has_stage(k)/records_at(k)/…" | pinn/data/splits.py:247 (`StageIndex`) |
| `records_at` (method) | 40-01:88 | pinn/data/splits.py:251 |
| `records_at_or_below` (method) | 40-01:88 | pinn/data/splits.py:254 |
| `record_keys` (method) | 40-01:88 | pinn/data/splits.py:200 |
| `get` (method) | 40-01:88 | pinn/data/splits.py:203 |
| `n_snapshots` (method) | 40-01:88 | pinn/data/splits.py:206 |
| `snapshot_times` (method) | 40-01:88 | pinn/data/splits.py:226 |
| `stage_label` (method, singular) | 40-01:88 | pinn/data/splits.py:244 |
| `is_blacklisted` (method) | 40-01:88 | pinn/data/splits.py:263 |
| `blacklisted_physical_keys` (property) | 40-01:88 "and exposes blacklisted_physical_keys" | pinn/data/splits.py:193; also field on StageQuery types.py:~305 |
| `ConservationOutcome` (class) | 40-02:122 "lines ~46-73 (ConservationOutcome frozen-result + pure-function shape)" | pinn/data/admission.py:47 (in range) |
| `evaluate_conservation` (function) | 40-04:87 "lines ~46-73 (ConservationOutcome + evaluate_conservation…)" | pinn/data/admission.py:55 (in range) |
| `evaluate_admission` (function) | 40-04:86 "lines ~106-240 (evaluate_admission: the fixed-order clause evaluator…)" | pinn/data/admission.py:128 (in range) |
| `build_network` (function, line claim 231, sig `(spec, *, dtype, device)`) | 40-01:81 "build_network(spec, *, dtype, device) at line 231" | pinn/network.py:231 `def build_network(spec, *, dtype, device):` (exact line + exact signature) |
| `ArchitectureSpec` (frozen dataclass) | 40-01:82; 40-04:122 "lines ~35-141 (frozen dataclass + fail-closed __post_init__…)" | pinn/architecture_spec.py:36; `__post_init__` at :71 (in range) |
| `LossWeights` (frozen dataclass, line claim 65) | 40-02:79 "LossWeights frozen dataclass at line 65" | pinn/loss_catalog.py:65 (exact); `__post_init__` :78 (claim ~64-101 ✓) |
| `compose_total` (function, line claim 299) | 40-02:79 "compose_total at line 299" | pinn/loss_catalog.py:299 (exact) |
| `causal_physics_loss` (function, line claim 208) | 40-05:109 "the five term functions incl. causal_physics_loss at line 208" | pinn/loss_catalog.py:208 (exact) |
| `lambda_data` (field) | 40-02:90 "returns a LossWeights (lambda_data pinned 1.0)" | pinn/loss_catalog.py:17 "``lambda_data`` is fixed at 1.0" (+ field in LossWeights) |
| `lambda_e` (field) | 40-02:107 "`LossWeights` instances with `lambda_e <= 1.0`" | pinn/loss_catalog.py:75 `lambda_e: float = 1.0` |
| `_require_finite` (function) | 40-02:123 "lines ~90-95 (_require_finite fail-loud discipline)" | pinn/physics_residual.py:90 (exact range) |
| `OverfitFail` (exception class) | 40-02:123 "pinn/verification/overfit_probe.py (OverfitFail typed failure)" | pinn/verification/overfit_probe.py:70 |
| `run_overfit` (function) | 40-05:107 "lines ~288-407 (run_overfit: the ONLY existing Adam loop…)" | pinn/verification/overfit_probe.py:288 (exact range start) |
| `RuntimeSpec` (class) | 40-04:123 "lines ~23-96 (RuntimeSpec frozen output…)" | pinn/runtime.py:24 (in range) |
| `resolve_runtime` (function, sig `(precision, device)`) | 40-05:111 "resolve_runtime(precision, device) → RuntimeSpec" | pinn/runtime.py:65 `def resolve_runtime(precision, device):` (exact signature) |
| `T_CHARACTERISTIC_TIME` (constant, line claim 31, value 10.0) | 40-03:75 "pinn/constants.py line 31 (T_CHARACTERISTIC_TIME = 10.0)" | pinn/constants.py:31 `T_CHARACTERISTIC_TIME = 10.0` (exact line + value) |
| state_dict key-by-key idiom (test content) | 40-02:83 "lines ~216-232 (state_dict() key-by-key equality idiom)" | tests/phase38/test_network_structure.py:216-227 (`test_same_seed_gives_identical_state_dict`, `sd1/sd2` comparison) |
| adapter `mem:` structured-log line (content) | 40-06:85 "pinn/data/adapter.py mem: line (structured-log-line precedent…)" | pinn/data/adapter.py:15 "…and the ``mem:`` line" |

### 3. VERIFIED — framework-spec content anchors (10)

| Anchor | Plan line (quote) | Evidence |
|---|---|---|
| §4.4 "Adaptive Gradient Clipping" heading | 40-02:121 "pinn_architecture.md §4.4 (Adaptive Gradient Clipping normative listing…)" | pinn_architecture.md:724 `## 4.4 Adaptive Gradient Clipping` |
| 100-norm rolling window | 40-02:137 "rolling grad-norm window (max length 100 per §4.4)" | pinn_architecture.md:749 "last 100 gradient norms", :755 `if len(grad_history) > 100:` |
| clip formula `C_stage * torch.median(torch.stack(...))` | 40-02:129 "clip_value == C_stage · torch.median(torch.stack(history))" | pinn_architecture.md:759 `clip_value = C_stage * torch.median(torch.stack(grad_history))` — note the spec variable is `grad_history`; the identifier `grad_norm_history` appears verbatim in .planning/REQUIREMENTS.md:61 (TRAIN-05) |
| median lower floor 1e-6 | 40-02:137 "median floored at `median_floor` (default 1e-6…)" | pinn_architecture.md:767-768 "the lower floor (e.g. `1e-6`) on the median" |
| §4.1 PHYS-05 warmup heading | 40-02:80 "pinn_architecture.md §4.1 / PHYS-05" | pinn_architecture.md:633 `## 4.1 Loss Balancing via Warmup Schedule (PHYS-05)` |
| `I_warm = min(2000, 0.1·N_Adam,k)` | 40-02:88 "Warmup length == min(2000, floor(0.1·N_Adam,k))" | pinn_architecture.md:660 `$I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$` |
| ADVANCE/RECOVER/HALT state machine at ~1924-1998 | 40-04:88 "ctl_instruction.md dual-path stage-transition state machine (~lines 1924-1998…)" | ctl_instruction.md:1928 "three dispositions: **ADVANCE**, **RECOVER**, and **HALT/REVIEW**"; criteria headings 1948/1958/1963/1971 (all inside claimed range) |
| β=0.98 / patience=200 / ε_plateau=1e-5 | 40-04:88 "(…ADVANCE four criteria with β=0.98/patience=200/ε_plateau=1e-5…)" | ctl_instruction.md:1954 `$\beta = 0.98$, patience = 200, $\epsilon_{\text{plateau}} = 10^{-5}$` |
| stochastic-L-BFGS routing for later stages | 40-03:122 "the ctl_instruction.md line range routing stages 3–6 to stochastic L-BFGS" | ctl_instruction.md:1700 "stochastic optimizer for exploration and a quasi-Newton method…" |
| energy floor `eps_H = 1e-4*S_H` | 40-04:101 "ε_energy with the ε_H = 1e-4·S_H floor" | ctl_instruction.md:579 "the training-loss `eps_H = 1e-4*S_H` in `pinn_architecture.md` §3.4" |

### 4. VERIFIED — planning/requirement/context IDs (46)

| ID(s) | Plan line (example quote) | Evidence |
|---|---|---|
| TRAIN-01..TRAIN-07 (7) | frontmatter `requirements:` of all six plans (e.g. 40-01:13) | .planning/REQUIREMENTS.md:57-63 (one bullet each) |
| CTX-17, CTX-19, CTX-20, CTX-33..CTX-49 (20) | e.g. 40-01:33 "(CTX-17 continuing prohibition)"; 40-04:135 "(CTX-42/19)"; 40-05:87 "implementing CTX-46 exactly" | 40-CONTEXT.md — CTX-17/20 at :220 (carried from phase-38 CTX-15..32 map), CTX-19 :130, CTX-33 :56, CTX-34 :65, CTX-35 :78, CTX-36 :83, CTX-37 :89, CTX-38 :97, CTX-39 :104, CTX-40 :111, CTX-41 :115, CTX-42 :126, CTX-43 :133, CTX-44 :139, CTX-45 :148, CTX-46 :159, CTX-47 :167, CTX-48 :173, CTX-49 :180 |
| DATA-04 | 40-05:128 "per-epoch resample, DATA-04 — NOT discretion" | .planning/REQUIREMENTS.md:51 |
| DATA-05 anchor: `B_lookahead`, `has_stage(k+1)` guard, 256 total | 40-05:123 "consumes build_stage_batch replay-only (B_lookahead=0)"; 40-05:130 "the 256-trajectory FixedBatch" | .planning/REQUIREMENTS.md:52 "`B_replay = 240` … plus `B_lookahead = 16` from `D_{k+1}` under the `has_stage(k+1)` guard (256 total)" |
| CURR-03 | 40-04:101 "(CURR-03 criterion 1)" | 40-CONTEXT.md:96 "### Provisional-Threshold Mechanics (CURR-03 gate)"; also REQUIREMENTS.md:13 prose |
| PHYS-02 | 40-05:110 "(PHYS-02 componentwise AD residual…)" | pinn_architecture.md:482 |
| PHYS-05 | 40-02:80 et al. | pinn_architecture.md:633 (§4.1 heading) |
| PLAT-02 | 40-03:122 "cites…the PLAT-02 deferral" | .planning/REQUIREMENTS.md:101 |
| PLAT-05 | 40-03:89 "deferred PLAT-05" | .planning/REQUIREMENTS.md:104 |
| ACC-02 | 40-05:130 "ACC-02 smoke test reveals…" | .planning/REQUIREMENTS.md:88 |
| ACC-05 | 40-02:39 "surfaced for ACC-05 pilot calibration" | .planning/REQUIREMENTS.md:91 |
| CTRL-02, CTRL-03, CTRL-04 | 40-04:168 "(CTRL-02..04)" | .planning/REQUIREMENTS.md:68, :69, :70 |
| LOOP-03 | 40-03:89 "(D5-b / LOOP-03)" | .planning/REQUIREMENTS.md:52 (referenced inside DATA-05 text) |
| SCOPE-19 | 40-04:135 "SCOPE-19 forbids inventing a value" | .planning/REQUIREMENTS.md:127 |
| D5-b, D5-c, D7-b, D1-p (4) | 40-03:89; 40-02:96 "(D5-c, CTX-38)"; 40-05:18 "(D7-b complete Adam reset)"; 40-01:144 "D1-p precision-switch contract" | 40-CONTEXT.md:216 (D5-b/D5-c), :90 (D7-b), :209 (D1-p) |
| `StochasticLBFGSNotImplemented` RESEARCH draft | 40-03:112 "the StochasticLBFGSNotImplemented draft — copy this exact shape" | 40-RESEARCH.md:336 `class StochasticLBFGSNotImplemented(Exception):` |

### 5. MISSING (3) — severity `needs-acknowledgement`, hardBlock=false

1. **`<home>/.claude-max/.claude/gsd-core/workflows/execute-plan.md`** (kind: file path). Cited in the `<execution_context>` block of all six plans (e.g. 40-01:47 "@<home>/.claude-max/.claude/gsd-core/workflows/execute-plan.md"). The path does not exist — `<home>/.claude-max/.claude/` has no `gsd-core`. The file exists at two other locations: `<home>/.claude-max/gsd-core/workflows/execute-plan.md` and `<home>/.claude/gsd-core/workflows/execute-plan.md`. The cited path looks like a hybrid of the two real roots.
2. **`<home>/.claude-max/.claude/gsd-core/templates/summary.md`** (kind: file path). Same `<execution_context>` block in all six plans (e.g. 40-01:48). Absent at the cited path; exists at `<home>/.claude-max/gsd-core/templates/summary.md`.
3. **`assertLogs` precedent in tests/phase38/test_prohibitions.py** (kind: test idiom/precedent reference). 40-06:85 "tests/phase38/test_prohibitions.py assertLogs/spy style". The token `assertLogs` does not appear in that file, nor anywhere under `tests/` (repo-wide grep: zero hits). `unittest.TestCase.assertLogs` is a real stdlib API and the planned usage is fine, but the cited in-repo precedent does not exist.

### 6. AMBIGUOUS (2) — severity `MEDIUM`, hardBlock=false

1. **`_V1_TOKENS`** (kind: constant). 40-01:110 "tests/phase38/test_prohibitions.py (the _V1_TOKENS ban list form and the no-precision-default / no-is_available assertions)". The symbol is real but lives in **tests/phase39/test_prohibitions.py:64** (`_V1_TOKENS = ("data-handling", "data_handling", "data-processing-pipeline-full", …)`); tests/phase38/test_prohibitions.py contains no `*_TOKENS` constant (its bans are inline). Misattributed file; executor should read phase39's file for the ban-list form.
2. **StageQuery "protocol" + 10-method source surface** (kind: class/method-surface attribution). 40-01:79 quotes the surface as belonging to `pinn/data/batches.py` ("the exact `source` attribute surface the stub must satisfy: has_stage, records_at, records_at_or_below, record_keys, get, n_snapshots, snapshot_times, stage_label, is_blacklisted, blacklisted_physical_keys") and 40-01:80 calls it the "StageQuery protocol at line 297". In the repo: `StageQuery` (pinn/data/types.py:297) is a **frozen dataclass** carrying `stage_labels` / `blacklisted_physical_keys` / `gold_numeric_stage_count` — not a Protocol with those methods. All ten named members do exist as real declarations, but on **`StageIndex` in pinn/data/splits.py** (:247, :251, :254, :200, :203, :206, :226, :244, :263, :193). `build_stage_batch` itself dereferences only `source.has_stage`, `source.n_snapshots`, `source.records_at`, `source.records_at_or_below` (rg over pinn/data/batches.py). The stub-fixture contract is satisfiable, but the owning type/file in the plan is misattributed and the stated surface is a superset of what build_stage_batch actually calls.

### 7. UNCHECKABLE (14) — severity `INFO`, hardBlock=false (grep over the repo cannot assess; never folded into verified/missing)

| Item | Plan line | Reason |
|---|---|---|
| `torch.optim.Adam(lr=…, betas=(0.9,0.999), eps=1e-8)` | 40-05:128 | external-library API surface; not declared in repo |
| `torch.optim.lr_scheduler.CosineAnnealingLR(T_max=…)` | 40-05:128 | external-library API |
| `torch.optim.LBFGS(history_size=10, line_search_fn="strong_wolfe", max_iter=20)` | 40-05:118/130 | external-library API + kwarg names |
| `torch.nn.utils.clip_grad_norm_(…, error_if_nonfinite=True)` and "returns the norm" | 40-02:137 | external API + return-behavior claim |
| `torch.median` even-length LOWER-middle semantics | 40-02:23 "even-length windows take the LOWER of the two middle values" | library runtime semantics, not grep-assessable |
| `torch.save` / `torch.load(weights_only=True)` safety contract | 40-04:165/168 | external API behavior |
| `zero_grad(set_to_none=True)`, `torch.isfinite` | 40-05:128/130 | external API |
| `typing.Protocol` | 40-04:168 "stdlib `typing.Protocol` (zero new dependency)" | stdlib API |
| `numpy.random.Generator` caller-owned semantics | 40-01:91 | external API |
| `logging.getLogger('pinn.training.*')` + `extra` key/value payloads | 40-06:100 | stdlib API (the logger-name tree is a new artifact) |
| unittest CLI flags `-m unittest`, `discover -s tests/phase40 -p 'test_*.py' -v` | verify blocks, e.g. 40-06:133 | stdlib CLI, not a repo symbol |
| "CPU/float64 is cheap enough for unit tests per pinn/verification/overfit_probe.py" | 40-01:89 | performance judgment, not a symbol |
| "B_lookahead=0 replay-only at final stage" runtime behavior of build_stage_batch | 40-05:123 | behavioral claim; the `has_stage(k+1)` guard + 256 composition are anchored at REQUIREMENTS.md:52, but the =0 fallback is runtime behavior grep cannot prove |
| "24 GB unified memory / M5 Pro" hardware bound | 40-05:158 | hardware claim, outside repo |

No decorator symbols are cited as pre-existing (the plans invoke only the stdlib `@dataclass(frozen=True)` idiom by prose reference).

### 8. Excluded new artifacts (61) — created by the plans themselves, not verified against source

**40-01** (Task 1 unless noted): `pinn/training/` package + `pinn/training/__init__.py` (T2); `tests/phase40/__init__.py` + new `_SKIP_PHRASE` literal; `tests/phase40/_fixtures.py` + `make_stub_source` + `make_stub_model`; `tests/phase40/test_prohibitions.py` + `discover_training_modules` (T2). (9)

**40-02**: T1 — `pinn/training/scheduled_weights.py`, `ScheduledWeights`, `.current(epoch)`, `.freeze()`, `.rewarm()`, `.state_dict()`/`.load_state_dict()`, `warmup_length`, `tests/phase40/test_scheduled_weights.py`; T2 — `pinn/training/grad_clip.py`, `GradClipper`, `GradClipOutcome`, `GradNormHistory`, `.clear()`, `median_floor` seam, provisional C-table, `tests/phase40/test_grad_clip.py`. (16)

**40-03**: T1 — `pinn/training/collocation_sampler.py`, `CollocationSampler`, `.uniform()`, `.adaptive()`, `tests/phase40/test_collocation_sampler.py`; T2 — `pinn/training/slbfgs_preflight.py`, `StochasticLBFGSNotImplemented` (production symbol; RESEARCH draft verified above), `check_stage_preflight`, `tests/phase40/test_slbfgs_preflight.py`. (9)

**40-04**: T1 — `pinn/training/stage_exit.py`, `StageDisposition`, `StageExitMachine`, `.evaluate(...)`, `StageExitOutcome`, `tests/phase40/test_stage_exit.py`; T2 — `pinn/training/config.py`, `TrainingConfig`, `RunConfig`/`StageConfig`/`OptConfig`/`LossConfig`, `tests/phase40/test_config.py`; T3 — `pinn/training/checkpoint.py`, `CheckpointStore`, `TorchSaveCheckpointStore`, `tests/phase40/test_checkpoint.py`. (17)

**40-05**: T1/T2 — `pinn/training/controllers.py`, `PlateauDetector`, `.update()`/`.fires()`, `RunController`, `.run_stage(k)`, `tests/phase40/test_optimizer_phase.py`, RunController `state_dict()` composition. (7)

**40-06**: T1 — `CurriculumController`, `tests/phase40/test_controllers.py`; T2 — full `pinn/training/__init__.py` barrel. (3)

### 9. Drift-guard severity JSON (authority=grep), per encountered verdict

```
VERIFIED:    {"severity": "none", "hardBlock": false}
MISSING:     {"severity": "needs-acknowledgement", "hardBlock": false}
AMBIGUOUS:   {"severity": "MEDIUM", "hardBlock": false}
UNCHECKABLE: {"severity": "INFO", "hardBlock": false}
```

Command: `node <home>/.claude-max/gsd-core/bin/gsd-tools.cjs drift-guard severity --status <VERDICT> --authority grep` — run 2026-07-16 for each of the four verdicts above. No hardBlock=true occurred.

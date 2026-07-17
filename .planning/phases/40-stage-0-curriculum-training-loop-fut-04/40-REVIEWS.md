---
phase: 40
reviewers: [grok, claude-kimi, claude-glm, claude, codex1]
rerun_reviewers: [claude, grok, codex1, claude-glm]
reviewed_at: 2026-07-17T05:11:54Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T050554Z-87026
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 40

## grok Review

> **Provenance note (non-review output, wrongly passed).** grok exited 0 after 22s having
> emitted ONLY the narration line below — it announced the review and never produced one.
> The dispatcher's `guard_output()` only stubs EMPTY or provider-error output, so a
> non-empty narration-only response passes as a real review. Treat this section as a
> FAILURE with zero findings, not as a reviewer sign-off.

I'll review the Phase 40 plans directly from the filesystem, starting with the six plan files and consulting support docs only to verify concerns.

---

## claude-kimi Review


Execution error

---

## claude-glm Review

I've read all six plan files plus `40-CONTEXT.md` and `40-SPEC.md` in full. I did not need to load `REQUIREMENTS.md`, `ROADMAP.md`, `PROJECT.md`, `AGENTS.md`, or `40-RESEARCH.md` — the SPEC and CONTEXT cite them exhaustively, and every concern below is verifiable against the plan text itself.

# Cross-AI Review — Phase 40 (Stage-0 Curriculum Training Loop, FUT-04)

## 1. Summary

Phase 40 builds the `pinn/training/` driver layer as six plans across four waves: scaffold + prohibitions (40-01), the two pure-numeric modules scheduled-weights + grad-clip (40-02), collocation sampler + sL-BFGS preflight (40-03), stage-exit machine + config + checkpoint seams (40-04), the `RunController` inner two-phase loop (40-05), and the `CurriculumController` outer loop + barrel + full-suite gate (40-06). The dependency DAG is clean, every one of the seven TRAIN requirements maps to a plan, and the plans are disciplined about the Phase-41/42/43 boundaries. The plans will almost certainly produce a green dataset-free unit suite. The residual risk is concentrated in a few cross-plan *contract* gaps where one plan consumes a behavior another plan produces, and the two are not pinned to a single shared specification — plus one reachable crash path that no plan's tests exercise.

## 2. Strengths

- **Clean wave structure.** Wave 1 scaffold → Wave 2 independent leaves → Wave 3 integrator → Wave 4 capstone. No plan depends on a later wave; `depends_on` matches real coupling. The one intra-plan hazard (40-04 Task 1 `stage_exit` vs Task 2 `config`) is explicitly de-coupled via a duck-typed config surface so Task 1's `verify` is order-independent.
- **The genuinely subtle numeric bugs are isolated and tested.** `torch.median` even-length lower-middle semantics (40-02, with an explicit anti-numpy-median guard), accumulate-in-closure `len(chunk)/N_total` weighting proven by an `allclose` equality test (40-05), and the two distinct plateau criteria — TRAIN-02 handoff (log10 slope, 50 epochs) vs CURR-03 criterion 1 (β-EMA, patience 200) — are called out as separate objects with separate state.
- **Honest provenance under a strict governance regime.** The C-table `8.5` is explicitly corrected as *not* trainex-r1a-ratified (CTX-34), and every provisional constant is tagged for ACC-05 calibration rather than cited as locked.
- **Security closed in-phase, not deferred.** `weights_only=True` on every checkpoint load is moved into Phase 40 (T-40-02), with `EmptyCheckpointStore` typed semantics.
- **TDD + deferred-import skip guards throughout**, matching the Phase 37/38/39 contract.

## 3. Concerns

### HIGH

**H1 — RECOVER at k=0 with an empty checkpoint store is an unhandled crash path.** CTX-41 defines RECOVER as "roll back to the last well-formed checkpoint, record disposition, transition to HALT." 40-04 correctly makes `rollback()`/`load_latest()` raise `EmptyCheckpointStore` when no save has occurred. But at k=0 cold-start, *before the first ADVANCE saves anything*, a NaN/Inf gradient (a close-encounter sample is exactly what produces one) routes to RECOVER → `rollback()` raises → nothing in 40-06's dispatch catches it. The stated AC ("run left numerically valid, Δstage=0") is violated by a crash. 40-06's RECOVER test uses a *forced* disposition with a spy store whose `rollback()` succeeds, so the composition is never exercised. This is the most consequential gap: reachable condition, breaks a stated guarantee, invisible to the phase's own tests.

### MEDIUM

**M1 — grad-clip non-finite signaling contract is ambiguous across 40-02 ↔ 40-05.** 40-02 says `clip_grad_norm_(error_if_nonfinite=True)` should "raise/return a typed non-finite signal" (raise *or* return — two different mechanisms). 40-05 says the RunController routes non-finite to `RECOVER` via "isfinite / `error_if_nonfinite=True` fail-loud" — a *third* mechanism (its own `isfinite` check). If 40-02 raises and 40-05 doesn't wrap that call in a try/except, the run crashes instead of recovering. Pick one contract (recommend: `GradClipOutcome` carries a `non_finite` flag; RunController branches on it) and test the handoff explicitly.

**M2 — CURR-03 criterion-1 plateau detector is not unit-tested at the mechanism level.** The β=0.98 EMA + patience-200 counter lives in `stage_exit.py` (40-04), but 40-04's test injects criterion-1 as a boolean ("each single criterion failing → not ADVANCE"). The *asymmetric* counter — PlateauDetector (50-epoch handoff) IS driven by flat/descending/reset fixtures in 40-05 — has no equivalent test for the 200-patience ADVANCE-gate counter. An off-by-one or wrong reset in criterion 1 would ship undetected. Add a mechanism-level test (drive ≥200 epochs of raw `train_loss_history` through the real EMA; assert plateau fires at 200, resets on a violating epoch), mirroring the PlateauDetector tests.

**M3 — `StageExitMachine.evaluate` signature drift between 40-04 and 40-05.** 40-04 lists the inputs as "train-loss history" *and* "β-smoothed total-loss plateau state" (two things); 40-05 calls `evaluate(train_loss_history, val_loss_history, val_phys, val_energy, had_nan_inf, epoch_count)` (raw history only). Either the β-smoothed state is computed internally from `train_loss_history` (so 40-04's "two inputs" is loose wording and the patience state-machine is implicitly inside `evaluate`), or there is a real signature mismatch. Pin the signature in *one* place (ideally the SPEC or a shared interface note) so 40-05 reads a contract, not a description. This is the root of M2.

**M4 — 40-05's validation pass needs held-out data the 40-01 stub source isn't specified to provide.** 40-05 adds a real no-grad validation forward pass every `validation_every` epochs over a "held-out batch from the stub source's held-out portion," but 40-01's `make_stub_source` is specified only to satisfy `build_stage_batch`'s four dereferenced members — no train/val split surface. 40-05's `files_modified` lists only `controllers.py` + `test_optimizer_phase.py`, so if it must extend `_fixtures.py`, that's an unlisted cross-plan edit. Either (a) specify the held-out surface in 40-01, or (b) add `_fixtures.py` to 40-05's `files_modified` and own the extension there.

**M5 — No end-to-end multi-stage progression test (0→1→2).** ADVANCE is only ever *force-injected*; no test runs the composed `run_stage → StageExitMachine.evaluate → CurriculumController.dispatch` on a real (stub) run and observes a stage increment earned through the gate. The dispatch side is tested (forced ADVANCE saves anchors, k+=1, rewarm), but the production-of-ADVANCE side is not — and cannot be, given provisional thresholds. This is an acknowledged consequence of the viability-slice design, but it means the phase *goal* ("runs the Stage-0 curriculum end-to-end") is satisfied structurally, not behaviorally. Worth stating explicitly as the phase's central residual risk rather than discovered at Phase 43.

### LOW

**L1 — Adaptive collocation mode is effectively a no-op in Phase 40** ("uniform-with-hook-invoked": the `(model, last_residuals)` hook is called but its output does not affect sampling). Acceptable per the PLAT-05 deferral and TRAIN-04's AC, but the dead path until PLAT-05 deserves a code comment so a later reader doesn't assume the hook drives density.

**L2 — `build_stage_batch` is called with `collocation_count=4096` whose output is then unused** (CollocationSampler is the single physics-point source per 40-05). Wasteful and slightly confusing; either pass `collocation_count=0` (verify `build_stage_batch` tolerates it) or document why the unused allocation is harmless.

**L3 — Forced-disposition injection AC allows two mechanisms ("raises a typed error OR is asserted unset").** For the HIGH-severity T-40-09 (spurious advance), pick one and test it concretely rather than leaving the implementer the choice.

**L4 — L-BFGS chunk-size memory bounding is verified only on tiny batches** (the `allclose` correctness proof holds generally, but T-40-08's *memory* claim on the real 256-trajectory batch is deferred to ACC-02 in Phase 43). Honest deferral; flagging only so it isn't read as verified in-phase.

**L5 — CTX-41's reading of "single attempt" (a rollback attempt, not a retrain) is a semantic interpretation of an ambiguous SPEC phrase.** It is logged with rationale under the 2026-07-16 autonomy directive, but under this repo's STOP protocol a semantic re-cast of spec wording is borderline surface-worthy. Not a technical defect; a governance-process note.

## 4. Suggestions

1. **Resolve H1 before execution:** specify that `CurriculumController`'s RECOVER branch catches `EmptyCheckpointStore` (k=0, pre-first-save) and still records the disposition + transitions to HALT, leaving the run numerically valid. Add a test that forces RECOVER against an *empty* store (not a spy) and asserts Δstage=0 + HALT + no crash. Consider saving a `stage-0-init` checkpoint at run start so rollback always has a target.
2. **Pin the `StageExitMachine.evaluate` signature in one artifact** (SPEC or a short interface block in 40-04) and have 40-05 read it as a contract. This resolves M2/M3 together and lets you add the missing criterion-1 mechanism test.
3. **Pick one NaN/Inf signaling contract** (recommend `GradClipOutcome.non_finite` flag consumed by RunController; no reliance on a raised exception) and add a cross-module test that a non-finite gradient flows grad-clip → RunController → `RECOVER` without any uncaught raise.
4. **Close the stub held-out-surface gap (M4)** by either extending 40-01's `make_stub_source` spec or listing `_fixtures.py` under 40-05.
5. **Decide whether M5 warrants a minimal real-run smoke test** (e.g., a 1-epoch, 2-stage stub run that earns an ADVANCE via injected-low-threshold gate) so the composition is exercised at least once, or explicitly record that composition-progression is deferred to Phase 43.

## 5. Overall Risk — **MEDIUM**

The architecture, dependency ordering, scope boundaries, and provenance discipline are strong; the phase will produce green unit tests and the Phase-41/42/43 seams are correctly narrowed. Risk is not in *whether the plans build what they say* but in *contract completeness between plans*: one reachable crash path (H1) and a cluster of integration gaps (M1–M4) where a consumer and producer are described separately with no single shared contract. None are blocking the wave structure, but H1 and M1 should be resolved before execution, and M2/M3 (the criterion-1 testing asymmetry) is the most likely place for a latent bug to ship to Phase 43 undetected. M5 is the honest ceiling on what "verified" means for this phase given provisional thresholds — it should be stated, not implied.

---

## claude Review

> **Provenance note (out-of-band recovery).** The dispatcher run marked this reviewer
> `returned non-review output` and overwrote its stdout with a stub. That was a
> false positive: `is_non_review_output()` in `dispatch.sh` substring-matches provider
> error phrases (`quota`, `rate limit`, `token limit`, `context window`, ...) against the
> ENTIRE flattened review body, so a legitimate review that merely mentions one of those
> words is destroyed. `claude` exited 0 with 12412 bytes of real review. The original
> stdout was unrecoverable (the stub `mv` clobbered it), so the review below is a
> re-run of the identical prompt (`ccp pro --model claude-opus-4-8`) captured directly.
> Reviewer/model/prompt are unchanged; only the transport differs.

# Phase 40 Plan Review — Stage-0 Curriculum Training Loop (FUT-04)

## 1. Summary

Six plans (40-01..06) across four waves build the `pinn/training/` driver layer on the closed Phase-38 model and Phase-39 data substrate. The decomposition is sound: a test scaffold (Wave 1), three parallel leaf-module plans with disjoint files (Wave 2), the `RunController` integrator (Wave 3), and the `CurriculumController` capstone plus barrel (Wave 4). Every TRAIN-01..07 requirement traces to at least one plan, and each acceptance criterion is numerically checkable rather than prose-only, as the SPEC's verification protocol demands.

The plans are unusually rigorous about the subtle failure modes — `torch.median`'s lower-middle semantics, the append-then-median ordering, chunk-fraction weighting in the L-BFGS closure, and the deliberate separation of the two distinct plateau criteria. My concerns are concentrated in the seams *between* plans, where 40-05 consumes surfaces that 40-04 and 40-01 were not asked to build.

All 13 listed files were readable. I read the six plans, the SPEC, and 40-CONTEXT; I consulted PROJECT/REQUIREMENTS/ROADMAP/AGENTS only where noted.

## 2. Strengths

The two-plateau-criteria separation (`PlateauDetector` in `controllers.py` vs. the β-smoothed stage-exit smoother in `stage_exit.py`, explicitly forbidden from sharing state) directly defuses the most likely silent-correctness bug in this phase.

The clip-spy target is correctly reasoned: 40-02 anticipates that `GradClipper.clip` makes two internal `clip_grad_norm_` calls, so a torch-level spy would read 2 and fail the `=1` acceptance criterion. Naming `GradClipper.clip` as the countable surface, with a *supplementary* torch-level `0` assertion for L-BFGS, is exactly right.

The partial-window backstop is genuinely resolved rather than deferred. Append-then-median means the window is never empty, so the length-1 identity (`clip = C_stage × the single norm`) closes the SPEC's 🧪 edge without inventing a bootstrap fallback value.

40-04 Task 1 is deliberately decoupled from Task 2 via a duck-typed config surface, so `test_stage_exit` passes before `config.py` lands. That is real dependency hygiene, not decoration.

The `weights_only=True` decision is correct and correctly *not* deferred — closing T-40-02 at the load boundary in Phase 40 rather than trusting payload cleanliness alone.

## 3. Concerns

### HIGH — `StageExitMachine.evaluate` has no return value for the "continue training" case

40-04 defines `StageDisposition` as a three-member enum (`ADVANCE|RECOVER|HALT`), but its own behavior spec requires a fourth outcome: *"else continue (never fall through to ADVANCE)"*, and its acceptance criterion states *"an in-progress non-passing state returns neither ADVANCE nor HALT-by-fallback."* No enum member represents that state. I grepped 40-CONTEXT — no `CONTINUE` disposition is mentioned anywhere, so this is a planning gap, not a transcription of a locked decision. The executor will be forced to mint something (a fourth member, an `Optional[StageDisposition]`, or a boolean) at implementation time, and 40-05/40-06 both dispatch on this type. Since the disposition set is the load-bearing safety contract for "no fallback advancement," an executor inventing it silently is precisely the failure mode the governance protocol exists to prevent. This should be resolved in the plans — most likely by adding `CONTINUE` to the enum — before execution.

### HIGH — 40-05's validation pass depends on a held-out surface neither 40-04 nor 40-01 provides

40-05 requires `RunController` to run a no-grad validation pass "over a held-out batch from the stub source's held-out portion," producing the `val_loss_history` that becomes ADVANCE criterion 2. Three pieces are missing:

- The `RunController` constructor argument list in 40-05 (model, batch source, config, schedule, clipper, sampler, stage-exit machine, checkpoint store, RuntimeSpec) has **no validation/held-out source**.
- 40-01's `make_stub_source` spec enumerates the `StageIndex` surface (`has_stage`, `records_at`, `record_keys`, …) with **no held-out or split-aware member**.
- `val_phys` and `val_energy` are passed to `evaluate(...)` as separate signals, but `compose_total` returns a composed total; the plans never say how the per-term validation values are extracted.

Without a fix, 40-05's own acceptance criterion — "asserted on a real (non-injected) `run_stage`, so the ADVANCE gate's criterion 2 is wired, not injected-only" — cannot be met against the Wave-1 fixture. Either extend 40-01's stub with a held-out portion and add the constructor argument, or explicitly relax the criterion to injected-only.

### MEDIUM — Two independent epoch budgets make 40-05's HALT criterion unprovable

`MAX_EPOCHS` (per-stage, CTX-39) and `N_Adam,k` (cosine `T_max`, CTX-48) are separate config-required fields, and no plan states their relationship. 40-05 asserts that a descending curve exits the Adam phase at `N_Adam,k` without handoff and yields **HALT/REVIEW (max-epoch-without-gate)**. That only holds if `N_Adam,k ≥ MAX_EPOCHS`. If `N_Adam,k < MAX_EPOCHS` — the natural reading, since `MAX_EPOCHS` should bound the whole stage including the L-BFGS phase — the stage exits Adam with `epoch_count < MAX_EPOCHS`, the gate is unmet, max-epoch is unreached, and the machine returns the "continue" case that (per the HIGH finding above) doesn't exist. This interacts with the first concern and should be resolved together.

### MEDIUM — The non-finite signal from `GradClipper` has no defined type or catch site

40-02 instructs the clipper to use `clip_grad_norm_(..., error_if_nonfinite=True)` and to "raise/return a typed non-finite signal," but its `artifacts_produced` names only `GradClipOutcome`, `GradNormHistory`, and `GradClipper` — no exception type. Meanwhile 40-05 places its `isfinite`-check on the **loss, before backward**, and clips after. A finite loss with a non-finite gradient therefore surfaces as a raw `RuntimeError` from inside `GradClipper.clip`, and 40-05 never says to catch it. The result would be a crashed `run_stage` rather than the required `StageDisposition.RECOVER` — and 40-05's acceptance criterion ("injecting a non-finite loss/gradient in the Adam phase … returns RECOVER") would fail. Name the exception type in 40-02's artifacts and name the catch site in 40-05.

### LOW — `config.py` and `checkpoint.py` sit close to the Phase-41 boundary

The SPEC lists config/checkpoint as out of scope (Phase 41, CTRL-01..08). 40-04 builds both as deliberately narrow seams, which the SPEC does anticipate ("the loop *consumes* a config object and *can* be checkpointed"), and the `typing.Protocol` framing keeps Phase 41's swap clean. This is defensible, but 40-04 mints a fair amount of config surface (four nested sections, provisional-provenance metadata, an enumeration API). Worth an explicit note in the Phase-41 handoff so that phase doesn't rediscover it as pre-empted.

### LOW — 40-01 asserts an unverified fact about `build_stage_batch`

The plan states that `build_stage_batch` "dereferences only `has_stage`/`records_at`/`records_at_or_below`/`n_snapshots`." If that reading is off by one member, every Wave-2/3 test fails at fixture construction. Cheap to de-risk: have Task 1's verify step actually call `build_stage_batch` against the stub rather than smoke-checking it "in the fixtures' own docstring example."

## 4. Suggestions

Add `CONTINUE` to `StageDisposition` in 40-04 and state the `MAX_EPOCHS` vs `N_Adam,k` relationship in the same edit — these two findings are one design decision. If the relationship isn't grounded in a locked source, it is a semantic gap and belongs in `40-GAPS.md` under the STOP protocol rather than being chosen by the executor.

Add a `validation_source` (or held-out-aware stub) to 40-01's fixture spec and to 40-05's `RunController` constructor, and say how `val_phys`/`val_energy` are obtained from the loss catalog.

Name the non-finite exception type in 40-02's `artifacts_produced` and add "catch it → `RECOVER`" to 40-05's step-ordering instruction.

Strengthen 40-01 Task 1's verify to execute `build_stage_batch(stub, stage=0, ...)` as an assertion.

## 5. Overall Risk

**MEDIUM.** The architecture, wave ordering, file-ownership disjointness, and prohibition coverage are strong, and nothing here suggests the plans fail to achieve the phase goal. The risk is concentrated in three inter-plan seams — the missing disposition member, the unwired validation source, and the untyped non-finite signal — each of which surfaces at Wave-3 execution time, after five plans have landed, and each of which pressures the executor toward inventing contract semantics that the governance protocol reserves for the owner. All three are cheap to fix in the plans now and expensive to discover mid-execution.

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
- stderr_bytes=469875

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T050554Z-87026/xreview-codex1-40.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T050554Z-87026/xreview-codex1-40.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T050554Z-87026/xreview-codex1-40.meta

Stderr excerpt:
```
E criteria at the validation cadence (knob exists; value = U-5) → on promotion: `stage-0-final.pt`, `curriculum.jsonl` promotion record, fresh Adam, re-warmed λ, `stage-1-init.pt` (D7). NaN/Inf → the RECOVER seam at `retries: 0` ⇒ emergency checkpoint + `GUARD: non-finite loss` + `failure/` bundle (identical to Tier-1 stop until the pilot calibrates a budget). Max-epoch/stagnation → `HALT: <trigger>` for owner review (placeholder thresholds). One Ctrl-C or SIGTERM = graceful checkpoint.
193-
194-**Resume / rollback:** `--resume runs/first-run/checkpoints/latest.pt`; after a bad promotion, `--resume …/stage-0-final.pt --hold-stage`. Resuming never re-asks what stage it is in (D7-d).
195-

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
mcp: sequential-thinking/sequentialthinking started
mcp: sequential-thinking/sequentialthinking (completed)
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
mcp: sequential-thinking/sequentialthinking started
mcp: sequential-thinking/sequentialthinking (completed)
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## Consensus Summary

**Panel integrity for this cycle: 2 of 4 selected reviewers produced usable findings.**
`grok` returned narration only (147 bytes, wrongly passed as success) and `codex1` timed out
(exit 143, watchdog triggered, 0 bytes stdout). The consensus below therefore rests on
`claude-glm` and `claude` only — it is a two-reviewer agreement, not a four-reviewer one, and
should be weighted accordingly.

### 2+ reviewer agreement (highest priority)

- **The non-finite gradient signalling contract is unpinned across 40-02 ↔ 40-05** (claude-glm M1,
  claude MEDIUM). 40-02 says "raise/return a typed non-finite signal" (two mechanisms) and names no
  exception type in `artifacts_produced`; 40-05 places its `isfinite` check on the *loss before
  backward* while clipping after, and names no catch site. A finite loss with non-finite gradients
  would surface as an uncaught raise from inside `GradClipper.clip`, crashing `run_stage` instead of
  returning `RECOVER` — failing 40-05's own acceptance criterion.
- **The two epoch budgets (`MAX_EPOCHS` vs `N_Adam,k`) have no stated relationship** (both
  reviewers). 40-05's descending-curve HALT assertion only holds if `N_Adam,k ≥ MAX_EPOCHS`; under
  the natural reading it instead lands in the unrepresented "continue" state.

### Single-reviewer HIGHs (no second opinion available this cycle)

- **`StageDisposition` has no "continue training" member** (claude). The three-member enum cannot
  represent 40-04's own required "else continue" outcome, making its acceptance criterion
  unsatisfiable without the executor minting a fourth member — the exact silent-invention failure
  the governance protocol exists to prevent.
- **The validation pass consumes a held-out surface nothing provides** (claude, extending
  claude-glm's cycle-1 H1). 40-05 requires a held-out no-grad pass, but `make_stub_source` (40-01)
  has no split member and `RunController`'s constructor list has no validation source.
- **RECOVER at k=0 against an empty checkpoint store is an uncaught crash** (claude-glm H1). 40-04
  makes `rollback()` raise `EmptyCheckpointStore`; 40-06 dispatches RECOVER → `rollback()` with no
  catch, and its test uses a spy store whose rollback succeeds, so the composition is never
  exercised.

**Structural note echoed by both reviewers:** the risk is not whether the plans build what they say
— it is *contract completeness between plans*. Several gaps are invisible to the phase's own tests
because the gate signals are injected/forced rather than produced.

## xreview Diagnostics

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=22
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260717T050554Z-87026/xreview-prompt-40.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=859
- stdout_bytes=147
- stderr_bytes=0

### claude-kimi
- status: preserved from existing REVIEWS.md

### claude-glm
- reviewer=claude-glm
- exit_code=0
- elapsed_seconds=240
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=10796
- stderr_bytes=192

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=178
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=12412
- stderr_bytes=0

### codex1
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=469875

---

# Phase 40 plan source-grounding audit — cycle 2 (xconverge)

Effective authority: `grep` (via `gsd-tools drift-guard authority --raw`).
Severity/gating verdicts resolved through `gsd-tools drift-guard severity` — not applied by hand.

## Verification coverage

### 1. VERIFIED — existing file paths (13)

`pinn/architecture_spec.py`, `pinn/constants.py`, `pinn/network.py`, `pinn/physics_residual.py`,
`pinn/loss_catalog.py`, `pinn/runtime.py`, `pinn/data/__init__.py`, `pinn/data/adapter.py`,
`pinn/data/admission.py`, `pinn/data/batches.py`, `pinn/data/splits.py`, `pinn/data/stages.py`,
`pinn/data/types.py` — all present on disk in the trainex worktree.

### 2. VERIFIED — cited upstream symbols (4)

| Symbol | Declaration |
|---|---|
| `build_stage_batch` | `pinn/data/batches.py:355` |
| `sample_collocation_points` | `pinn/data/batches.py:289` |
| `_require_local_rng` | `pinn/data/batches.py:33` |
| `StageIndex` | `pinn/data/splits.py:126` |

### 3. VERIFIED — third-party APIs (11), pinned interpreter

Interpreter: `<home>/miniforge3/envs/pinn-train/bin/python` (torch 2.12.1) — the
interpreter the plans' own verify commands pin.

`torch.device`, `torch.float64`, `torch.load`, `torch.median`, `torch.no_grad`, `torch.save`,
`torch.stack`, `torch.nn.utils.clip_grad_norm_`, `torch.optim.Adam`, `torch.optim.LBFGS`,
`torch.backends` — all resolve as attributes of the installed package.

Corroborated numeric claim (40-02, load-bearing): `torch.median` even-length semantics return the
lower-middle element. Observed: `torch.median([1,2,3,4]) = 2.0` vs `numpy.median([1,2,3,4]) = 2.5`.
The plan's assertion that a `numpy.median` reference implementation would fail this test is
therefore correct as written.

### 4. EXCLUDED — artifacts this phase produces (21)

Not verified because Phase 40 creates them (per the source-grounding rule, declared artifacts are
excluded rather than reported MISSING):

- `pinn/training/`: `__init__.py`, `checkpoint.py`, `collocation_sampler.py`, `config.py`,
  `controllers.py`, `grad_clip.py`, `scheduled_weights.py`, `slbfgs_preflight.py`, `stage_exit.py`
- `tests/phase40/`: `__init__.py`, `_fixtures.py`, `test_checkpoint.py`,
  `test_collocation_sampler.py`, `test_config.py`, `test_controllers.py`, `test_grad_clip.py`,
  `test_optimizer_phase.py`, `test_prohibitions.py`, `test_scheduled_weights.py`,
  `test_slbfgs_preflight.py`, `test_stage_exit.py`

`pinn/training/` confirmed absent on disk — consistent with it being a new artifact, not a
hallucinated reference.

### 5. UNCHECKABLE — INFO severity (not treated as verified or missing)

- **Signatures / arity / parameter names of all symbols in §2–§3.** The `grep` authority cannot
  assert signature agreement (official rule: "Signature mismatches cannot be asserted under
  `grep`/`intel`; report the signature as UNCHECKABLE"). So while `build_stage_batch` and
  `sample_collocation_points` are confirmed to *exist*, whether the plans call them with the
  correct arguments is NOT established by this pass and remains an execution-time risk.
- **`torch.backends.*` leaf attributes** (e.g. determinism flags) — cited as a prefix in plan prose
  without a resolvable leaf symbol; nothing concrete to resolve.

### 6. Gating outcome

| Verdict class | Count | Severity (via seam) | hardBlock |
|---|---|---|---|
| VERIFIED | 28 | `none` | false |
| MISSING | 0 | — | — |
| AMBIGUOUS | 0 | — | — |
| UNCHECKABLE | signatures + `torch.backends.*` | `INFO` | false |

**No MISSING symbols, no AMBIGUOUS symbols, no hard blocks.** A clean result here does not mean
"nothing was checked" — 28 symbols were resolved against source; the residual unchecked surface is
enumerated in §5.

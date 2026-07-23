---
phase: 43
reviewers: [claude, claude-qwen-token, codex2, codex3, grok]
rerun_reviewers: [claude, claude-qwen-token, codex2, codex3, grok]
reviewed_at: 2026-07-21T04:36:32Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260721T043031Z-45246
---

# Cross-AI Plan Review — Phase 43

## claude Review

I've read all eight plan files plus `43-SPEC.md` and `43-CONTEXT.md`, and cross-checked the SCS-gate concern against the current on-disk SPEC (post-commit `5d269156`). I did not fully load `43-RESEARCH.md` (56 KB), `REQUIREMENTS.md`, `ROADMAP.md`, or `PROJECT.md`; where a concern depends on their content I say so and mark it as a verify-item rather than a confirmed defect. All files listed were readable.

---

# Phase 43 Plan Review — Verification, Stage-0 Pilot & Acceptance

## 1. Summary

Eight plans assemble the already-built Stage-0 components into the milestone-closing verification/acceptance surface: a `verify` ladder + marker (43-01), the `evaluate` binary gate (43-02), real-data wiring + s/step forecast (43-03), the >30-min launch gate (43-04), `summary.md` enrichment (43-05), the smoke run (43-06), the multi-seed pilot (43-07), and the go/adjust/rethink verdict (43-08). The decomposition is sound, the wave/dependency ordering is mostly correct, the honesty discipline is strong, and each prohibition gets a negative test. The most consequential gaps are technical underspecification in the two genuinely-load-bearing pieces (the gate metric and the launch forecast) and documentation drift now that the SPEC's SCS wording has been corrected.

## 2. Strengths

- **Honesty layer is enforced, not aspirational**: null-metrics-on-non-success, "no fabricated forecast on divergence," and "no unqualified go on a FAILing gate" each have a dedicated negative test (43-03, 43-05, 43-08).
- **Gate boundary is locked by a unit test** (43-02 Task 1) with `eps_H` just above/below `1e-5`, and the single-boolean-with-SCS-as-display design correctly avoids the "two independent booleans" trap.
- **Security posture is appropriate**: `weights_only=True` checkpoint load (enforced by the phase41 AST audit), traversal-guarded `--output`/marker paths, read-only corpus, no dataset copy, single-eval discipline. Per-plan STRIDE tables are proportionate (local, no-network, ASVS-1).
- **Owner-pause gates are well-placed and explicitly non-self-ratifiable** (B-5, D4-a, R-1/R-2, ACC-06), each as a blocking checkpoint task.
- **Dependency waves are clean**: the two plans editing `pinn/train.py` (43-03 wave 2, 43-04 wave 3) are serialized by an explicit `depends_on`, avoiding a same-file collision.

## 3. Concerns

### HIGH

- **[43-02] `pred_velocities` derivation conflicts with the mandated no-grad forward.** The gate Hamiltonian's kinetic term `Σ pᵢ²/(2mᵢ)` needs velocities, but the network output is positions only (9-dim). The natural route — `dq/dτ` via autograd — is incompatible with the required single `torch.no_grad()` `.eval()` forward (CTX-74 / Prohibition). The plan passes `pred_velocities` into `compute_gate_metrics` without specifying whether they come from autograd or finite-differencing the `times` samples. This is the *single genuinely-new piece of logic* and the only honest pass/fail; the executor will hit this and may deviate silently. Pin the velocity source (finite-difference under no-grad is the consistent choice) and its accuracy implications for `eps_H`.

- **[43-04] Launch-time forecast source is underspecified for a fresh run.** The 43-03 helper `forecast_full_stage0_seconds` returns `None` unless `s_per_step` (the EMA) is finite and > 0, but a freshly-launched `pinn.train` has no EMA yet. The plan hedges: "if no prior s/step measurement is available, use the config's declared/estimated step budget consistently" — which conflates *step count* with *seconds* and names no config field carrying an s/step estimate, nor any persistence of the smoke's measured s/step for a later launch to read. The tests inject/monkeypatch the forecast, so they pass regardless; the *production* gate behavior (what forecast does a real long run compare against 30 min?) is left undefined. This is the second half of ACC-01 and the milestone's safety mechanism.

### MEDIUM

- **[43-03 / 43-06 / 43-07 / 43-01] Real-data reachability from the worktree is a load-bearing assumption that contradicts established practice.** 43-03 asserts (RESEARCH finding #4) that `default_data_root()` reaches the master-root `simulation_data/Data` from the trainex worktree "with zero config," explicitly superseding CTX-79's copy hedge. But the established Phase-38 pattern (and the gitignored-payload constraint) is that worktrees *lack* the corpus and a trajectory must be copied in. If finding #4 is wrong, the smoke (43-06), pilot (43-07), and `verify` rungs 4–5 (which call probes with `variant=standard_quasi_random_gold_standard, id=0000`) all fail to find data. Verify this resolution empirically before execution; retain CTX-79's copy/run-from-master-root fallback.

- **[43-02 / 43-08 / 43-CONTEXT] Stale SPEC-defect references + a still-backwards CTX-75.** The SPEC's SCS wording was corrected in `5d269156` (now consistently "REJECT iff `SCS > -5`; boundary `SCS == -5 → PASS`"). Yet 43-02 (§objective flagged item, Prohibition #1 text) and 43-08 (objective precondition, Task 2) still quote the *old* backwards text ("SCS == -5 → FAIL", "OVERALL FAIL iff … SCS ≤ -5") and instruct the agent to surface that defect to the owner as an ACC-06 precondition — a defect that no longer exists in the SPEC. Separately, `43-CONTEXT.md` CTX-75 still carries the self-contradictory "FAIL iff `ε_H > 1e-5` OR `SCS ≤ -5` … `SCS == -5 → FAIL`". The code will be built correctly (plans target the authoritative direction), but the executor/owner will be told to reconcile a phantom defect, and CTX-75 can mislead a later reader. Update the plan preconditions to "SPEC corrected in 5d269156 — confirm only" and fix CTX-75.

- **[43-06 / 43-07] Owner-ratified config values are written to files not declared in `files_modified`.** 43-06 Task 3 records the D4-a ceiling "into the pilot/production config," and 43-07 Task 2 records R-1/R-2 "into the guard/recover config," but neither plan lists `config.py`/`configs/*.yaml` in `files_modified`. Under the repo's `GIT_AGENT_OWNED_PATHS` policy this is either an owned-paths violation at commit time or a silently-unpersisted ratification. Declare the config target(s) explicitly.

### LOW

- **[43-01] Marker freshness ignores the recorded `git_head`.** `marker_is_green_and_fresh` checks verdict + age + device/dtype, but not the `git_head` it records — so a green marker from different code within 24 h still satisfies the >30-min gate. If the intent is "env *and code* healthy," fold `git_head` into the predicate; otherwise document that code changes intentionally don't invalidate the marker.
- **[43-05 ↔ 43-02] Same-wave schema coupling.** 43-05 (wave 2) consumes the `metrics.json` schema that 43-02 (wave 2) simultaneously defines, via a hand-written fixture duplicating the keys. Parallel execution risks drift if the schema is adjusted mid-flight. Consider making 43-05 `depends_on: [43-01, 43-02]`, or centralize the schema contract.
- **[43-03] New `stage.residency: auto` key must be a recognized config field** or fail-closed `load_config` will reject `smoke.yaml`. The plan flags this to verify — good; just ensure `config.py` actually accepts it before the smoke.
- **[43-01] `git rev-parse HEAD` in the marker writer has no specified fallback** if git is unavailable/detached; a subprocess failure there shouldn't abort a verify run.

## 4. Suggestions

1. In 43-02, add a one-line behavior spec: "`pred_velocities` are obtained by finite-difference over `times` under no-grad" (or state the model emits velocities), and add a test that the KE term is finite without requiring gradients.
2. In 43-04, name the concrete forecast source for a fresh launch (e.g., a persisted `s_per_step` from the last smoke/pilot written alongside the D4-a ceiling), and add one non-injected test that a fresh config with a recorded prior s/step produces a real forecast.
3. Add an early "data reachability" precheck (or reuse a probe) to 43-03/43-06 so a missing corpus is a clear refusal, not a mid-run crash — and confirm finding #4 before relying on it.
4. Sweep the SCS references: mark the 43-02/43-08 preconditions as "confirm SPEC already corrected (5d269156)" and fix CTX-75; this avoids burning an owner checkpoint on a resolved item.
5. Add `config.py`/`configs/*.yaml` to `files_modified` for 43-06/43-07 (or explicitly defer persistence to the owner and say so).

## 5. Overall Risk

**MEDIUM.** The plans are well-structured, honestly-scoped assembly work with strong test discipline and correct dependency ordering, and they will achieve the phase goal for most ACCs. The residual risk concentrates in two technical underspecifications on the load-bearing pieces (gate-metric velocity source; launch forecast source), one load-bearing data-access assumption, and documentation drift around the now-fixed SCS wording — all resolvable with small, local plan edits before execution rather than structural rework.

---

## claude-qwen-token Review

Execution error
---

## codex2 Review

_codex2 failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex2
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex2 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=1175726

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260721T043031Z-45246/xreview-codex2-43.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260721T043031Z-45246/xreview-codex2-43.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260721T043031Z-45246/xreview-codex2-43.meta

Stderr excerpt:
```
:
704:            raise ValueError(f"only float32 residency is supported; got {precision!r}")
705-        # DATA-01 fail-closed safety boundary: validate capacity, watermark,
706:        # interim_s0, and CPU residency BEFORE root resolution, corpus scanning,
707-        # tensor materialization, or memory logging.
708-        self._device = _validate_adapter_config(
709-            capacity_bytes, memory_watermark, interim_s0, device)
710-        self._dtype = torch.float32
711-        self._capacity_bytes = int(capacity_bytes)
--
911-        self.gold_numeric_stage_count = 0
912-        self._raw_ic13_population = raw_ic13_population
913-        self._trajectory_energies = trajectory_energies
914-        return candidates
915-
916:    # -- pass 2: admitted-only normalization + fp32 residency ----------------
917-    def _materialize(self, candidates):
918-        stats = compute_normalization_stats(
919-            np.asarray(self._raw_ic13_population, dtype=np.float64),
920-            np.asarray(self._trajectory_energies, dtype=np.float64))
921-        self._normalization_stats = stats

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## codex3 Review

## 1. Summary

The eight plans have a strong staged structure, but several implementation contracts are currently infeasible or incomplete. The smoke path, acceptance metric, duration gate, and evaluate-to-summary flow need replanning before execution.

All requested phase files were readable.

## 2. Strengths

- Clear progression from verification and smoke testing through calibration and owner-rendered verdict.
- Strong honesty requirements around NaN/Inf, empty datasets, diverged seeds, and failed runs.
- Appropriate owner checkpoints for B-5, D4-a, R-1/R-2, and ACC-06.
- Good security basics: atomic writes, `weights_only=True`, path containment, and fail-closed behavior.
- Scope boundaries and deferred PLAT-01..07 work are generally explicit.

## 3. Concerns tagged HIGH / MEDIUM / LOW

- **HIGH — The real-data smoke configuration cannot work as planned.** [43-03-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-03-PLAN.md:83>) uses `stage.residency`, but [StageConfig](<<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/config.py:330>) has no such field and the loader rejects unknown keys. The plan also passes the resolved MPS device to [AdmittedSetAdapter](<<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/data/adapter.py:694>), which accepts only CPU/fp32 residency. Finally, batching defaults to 240 replay trajectories in [batches.py](<<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/data/batches.py:71>); no planned config field produces the required ≈32-trajectory smoke.

- **HIGH — The acceptance metric is underspecified and partly inconsistent with the authoritative physics contract.** The network outputs positions only, so velocities must be AD-derived; the planned `torch.no_grad()` evaluation cannot produce those derivatives. Moreover, [43-02](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-02-PLAN.md:100>) points toward the training softening kernel (`1e-5`) while the authoritative conservation gate specifies float64 Hamiltonian evaluation with validation Plummer softening `1e-10` in [ctl_instruction.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:565>). The top-level aggregation rule across multiple test trajectories is also absent.

- **HIGH — The evaluate data flow is not closed.** With only `--checkpoint` and `--output`, 43-02 does not define how evaluation locates the frozen config, exact persisted split manifest, held-out `StageIndex`, IC13 values, masses, or time samples. Plan 43-03 says “builds or loads” a manifest without pinning its path or persistence contract.

- **HIGH — ACC-04 will not appear in a real completed-run summary.** [43-05](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-05-PLAN.md:79>) adds optional arguments to `finalize_summary`, but does not modify the production caller in [train.py](<<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/train.py:371>). Evaluation occurs later in 43-08, and no plan re-renders the summary afterward. The test-set preview and comparison hint therefore exist only in synthetic unit tests.

- **HIGH — The pre-launch duration gate lacks a usable timing input.** [43-04](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-04-PLAN.md:74>) needs measured seconds-per-step before run construction, but that EMA exists only after training steps and is not checkpointed. A step budget alone cannot produce a forecast in seconds, leaving the >30-minute gate undefined or bypassable.

- **MEDIUM — Plan metadata omits required dependencies and owned files.** The formal DAG does not make 43-05 or 43-08 depend on 43-02, despite consuming its schema and executable. Plans 43-06/07 also require modifying resume/configuration files and creating pilot configs that are absent from `files_modified`, conflicting with the repository’s owned-path commit policy.

- **MEDIUM — The SPEC blocker is stale.** The current [43-SPEC.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-SPEC.md:78>) already gives the corrected inclusive-PASS SCS boundary. Plans 43-02 and [43-08](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/43-verification-stage-0-pilot-acceptance/43-08-PLAN.md:43>) still describe correction as an unresolved owner precondition.

- **LOW — Verify-marker matching is weaker than its schema.** The marker records Torch version and Git HEAD, but the planned freshness predicate compares only device and dtype. A green marker from different code or runtime dependencies could authorize a long run.

## 4. Suggestions

- Replan 43-03 around an explicit supported real-data configuration, CPU adapter residency, persisted `runs/<run>/splits.json`, and a concrete mechanism for selecting ≈32 smoke trajectories.
- Specify evaluation end-to-end: reconstruct the exact test split, freeze model parameters while enabling input-time AD, evaluate Hamiltonians on CPU/float64 with `eps_inv=1e-10`, and define worst-case/test-set aggregation.
- Persist the smoke timing calibration as a named artifact or config field consumed by the launch gate; define fail-closed behavior when it is absent.
- Add a post-evaluation summary refresh and explicit checkpoint-selection rule based only on validation evidence before the one-time test evaluation.
- Correct dependencies, enumerate every ratification/config output path, remove the obsolete SPEC-correction checkpoint, and match the full verify fingerprint.

## 5. Overall Risk (HIGH)

The plans cover the intended scope, but the current form cannot reliably execute the real-data smoke or compute and propagate the milestone’s authoritative acceptance verdict.

---

## grok Review

I'll review the Phase 43 plans from the listed paths, starting with the eight plan files and pulling in CONTEXT/SPEC only as needed to verify concerns.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=243
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=8939
- stderr_bytes=0

### claude-qwen-token
- reviewer=claude-qwen-token
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp claude-qwen-token -p - 
- stdout_bytes=15
- stderr_bytes=192

### codex2
- reviewer=codex2
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex2 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=1175726

### codex3
- reviewer=codex3
- exit_code=0
- elapsed_seconds=323
- timeout_seconds=360
- watchdog=not_triggered
- command=env CODEX_HOME=<home>/.codex3 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=6090
- stderr_bytes=610690

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=29
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260721T043031Z-45246/xreview-prompt-43.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=1013
- stdout_bytes=152
- stderr_bytes=0

---

## Verification coverage (source-grounding pass, xconverge cycle 1)

Authority resolution: `gsd-tools drift-guard authority --raw` returned a noop shim
(`grep`) under this profile — no LSP/SCIP index available. Verdicts below are
therefore recorded as UNCHECKABLE under the configured adapter, with manual `grep`
evidence cited for traceability. No `hardBlock: true` was raised by the tool.

Cited symbols verified against live source (Phase 43 worktree):

| Symbol | Kind | Verdict | Evidence / Note |
|---|---|---|---|
| `StageConfig` | class | VERIFIED (grep) | `pinn/training/config.py:330` — review cited `config.py:330`; actual path is `pinn/training/config.py`. Same class. |
| `AdmittedSetAdapter` | class | VERIFIED (grep) | `pinn/data/adapter.py:681` — CPU/fp32-only residency contract confirmed (`pinn/data/adapter.py:14-15`, `pinn/data/stage_scan.py:649-650`). |
| `softened_acceleration` | function | VERIFIED (grep) | `pinn/physics_residual.py:193` — default `eps_soft=EPS_SOFT` (training softening 1e-5); review's Hamiltonian/Plummer-1e-10 concern is grounded in the divergence between this default and `ctl_instruction.md`'s float64 Hamiltonian contract. |
| `finalize_summary` | function | EXCLUDED (new artifact) | Declared as a new/modified artifact by 43-05; not a reference to existing code. |
| `compute_gate_metrics` | function | EXCLUDED (new artifact) | Declared as a new artifact by 43-02; not a reference to existing code. |
| `marker_is_green_and_fresh` | function | EXCLUDED (new artifact) | Declared as a new artifact by 43-01. |
| `pinn/train.py` | file path | VERIFIED (grep) | Exists; cited by 43-05 as the production `finalize_summary` caller — confirms the codex3 HIGH that the file is consumed but absent from `files_modified`. |
| `configs/stage0-example.yaml` | file path | VERIFIED (grep) | Exists; `stage.residency` field referenced by 43-03 smoke config does not appear in the existing file's `StageConfig` schema (`pinn/training/config.py:330`), confirming codex3's infeasibility HIGH. |
| `pinn/evaluate.py`, `pinn/verify.py` | file paths | EXCLUDED (new artifacts) | Produced by 43-02 / 43-01 respectively. |
| `torch.no_grad` | API call | UNCHECKABLE (signature) | Signature/semantics not asserted; usage is correct by library contract. |

No hard-block raised. All cited existing-code symbols resolved; remaining
"cited" paths are declared new artifacts excluded from grounding by the workflow.
The substantive review findings (6 HIGH, 6 actionable non-HIGH) stand on their
own merits and are routed to the cycle-summary escalation below.

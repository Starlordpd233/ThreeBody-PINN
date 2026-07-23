---
phase: 38
reviewers: [claude-glm, claude-deepseek, grok, agy, claude-max, codex, claude-kimi]
rerun_reviewers: [claude-glm, grok, claude-max, codex, claude-kimi]
reviewed_at: 2026-07-13T08:17:22Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T081015Z-19768
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 38

## claude-glm Review

API Error: 529 [1305][该模型当前访问量过大，请您稍后再试][20260713161352a87701b3466a49ec]. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (127.0.0.1:4148).

---

## claude-deepseek Review


I've now read all six plan files, the CONTEXT, the SPEC, and the supporting project documents. Here is my review:

---

# Phase 38 Plan Review — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Phase 38 plans to rebuild the `pinn/` model package from the authoritative framework specs across 6 plans (15 tasks, 5 waves): constants + architecture spec (W1), network + COM projection (W2), physics residual + fixture loader (W3), gradcheck/residual probes + loss catalog (W4 parallel), and overfit probe + prohibition checks (W5). Each plan is TDD-first, with tests authored before implementation. The plans incorporate feedback from two cross-AI review cycles, with explicit resolution notes in each plan's `<review_incorporation>` section. All SPEC prohibitions (spec byte-identity, no simulation_data writes, no precision defaults, no v1.3 imports) are wired as mechanical checks in 38-06.

## 2. Strengths

- **TDD ordering is consistent across all plans.** Every plan's first task authors the test suite; implementation tasks follow with `tdd="true"`. The deferred-import skip guard (`SkipTest` until the target module exists) allows incremental implementation without spurious failures.

- **Review incorporation is thorough and traceable.** Each plan documents which cross-AI review findings were resolved and how, with cycle-1 and cycle-2 entries. The resolutions are concrete (e.g., COM mass provenance pinned to explicit `forward(tau_ic13, masses)`, gate B dimensional fix with `T_CHARACTERISTIC_TIME`, dual PASS gate on rung 3).

- **Phase boundaries are crisp.** What's in scope (model, projection, physics residual, loss catalog, three proof rungs, minimal fixture loader) vs. what's deferred (data ingestion Phase 39, training loop Phase 40, config/checkpointing Phase 41, verify ladder Phase 43) is clearly stated in every plan and traceable to the roadmap.

- **SPEC edge coverage is appropriately surfaced.** Edges R3 (softening-active points), R4 (Huber transition/causal-weight extremes), and R5 (overfit non-convergence) are treated as planner assumptions with explicit handling, not silently dropped or invented.

- **Mechanical prohibition checks are comprehensive.** 38-06-03 wires AST-based checks for precision defaults and v1.3 imports (reusing the Phase 37 technique), sha256 spec-byte-identity pinned to pre-phase committed state, and a simulation_data write spy — covering all four SPEC prohibitions.

- **Real-dataset evidence gate for phase close.** The plan explicitly requires operator-run rung 3 and rung 4 against a real admitted trajectory before close, with a DEFERRED escape hatch logged in the gap register.

## 3. Concerns

### HIGH — Overfit probe `--max-steps` default (38-06-02)

The default of 3000 steps is explicitly labeled "UNCALIBRATED build-engineering guess." The plan provides calibration guidance (re-run with a larger cap if still improving, plateau indicates wiring problem) and a one-shot calibration recommendation. However, on a `first_omega_0=30` SIREN with Adam at `lr=1e-3`, 3000 steps is a non-trivial bet — convergence speed on real data is unknown until the first operator run. The risk is that the default is too low for the real trajectory, producing a spurious cap-reached FAIL that confuses the operator.

**Mitigation**: The plan's calibration guidance + overridable `--max-steps` flag + recording of the achieved ratio means this is recoverable, not a silent error. The concern is operator experience, not correctness.

### MEDIUM — Wave-4 parallel dependency on 38-02/38-03 (38-04, 38-05)

38-04 (probes) depends on 38-03 (physics residual + loader). 38-05 (loss catalog) depends on 38-02 (network) AND 38-03. Both run in Wave 4. The dependency graph is correct — 38-04 and 38-05 are independent of each other and both depend only on completed waves. However, 38-05-02/03 extend a single file (`pinn/loss_catalog.py`) across two tasks sharing one test suite via per-symbol deferred imports. If 38-05-02 introduces an interface mismatch that 38-05-03's additions accidentally mask (e.g., a shared helper that both tasks modify), the single-test-suite pattern won't catch it until the full suite runs after 38-05-03. The task isolation is sound in principle but relies on careful incremental commit discipline.

### LOW — Fixture loader folder mapping handshake with real data (38-03-02)

The loader's `resolve_trajectory_path` maps variant names to hardcoded folder paths (e.g., `standard_quasi_random_gold_standard` → a specific `simulation_data/Data/brutus_output/...` path). If the dataset folder layout differs from the documented convention (e.g., on the user's other machine where payloads exist), the loader will raise on "unknown variant." The plan notes this is per the dataset README conventions — the risk is low because the path-based `--path` flag provides an escape hatch.

### LOW — Overfit probe full-stack evidence complexity (38-06-02)

The overfit probe derives `h0`, `l0`, and `pred_velocities` from the fixture's t=0 snapshot and the PHYS-02 AD path during the probe body. This is a non-trivial amount of physics computation embedded in a probe script — deriving the matched-Plummer Hamiltonian, angular momentum, and AD velocities correctly outside the model forward path. The plan documents the input provenance clearly, but the implementation surface is larger than a simple "optimize + record" probe. The risk is implementation bugs in the diagnostic computation that produce misleading "full-stack" evidence while the actual PASS gate (data loss ≥10³×) passes correctly.

## 4. Suggestions

1. **Consider a smaller `--max-steps` default for the synthetic test, with a separate recommendation for real-data runs.** The synthetic in-worktree fixture is tiny (a few snapshots) — 3000 steps is likely generous. For the real trajectory (~1000 snapshots), convergence may take longer. The plan could note that the synthetic test is expected to converge fast and the 3000 default is sized for the real-data path.

2. **Add a `--max-steps` sanity lower-bound in the overfit probe.** A `--max-steps 1` produces a cap-reached FAIL that's indistinguishable (to a script) from a genuine non-convergence at `--max-steps 3000`. The probe could warn if `--max-steps < 10` to prevent test-only values from looking like real failures in evidence.

3. **Verify the recommended default trajectory exists before phase-close.** The plan recommends `standard_quasi_random_gold_standard` ID `0000` but notes it may be an ID-gap. Consider having the executor verify the file exists (even if the payload isn't in the worktree, a `git ls-tree` check on the data branch would confirm the path).

## 5. Overall Risk: LOW

The plans are thorough, internally consistent, and grounded in the locked framework specs. The TDD ordering, mechanical prohibition checks, dual PASS gate on rung 3, and explicit real-dataset evidence gate for phase close are all strong quality controls. The concerns are operational (uncalibrated defaults, operator dependencies) rather than structural (missing requirements, dependency ordering errors, scope creep). The two cross-AI review cycles have already addressed the most substantive issues (dimensional fix for Gate B, autograd mandate for Gate A, batch-dimension contract, input provenance for full-stack evidence).

---

## grok Review

I'll review the Phase 38 plans directly from the filesystem, starting with the six plan files and then checking SPEC/CONTEXT only where needed to verify concerns.

---

## agy Review


# Cross-AI Plan Review: Phase 38 (PINN Model Rebuild)

## 1. Summary
Phase 38 successfully translates the PINN framework specifications into a deterministic, test-driven implementation. It methodically constructs the SQR-SkipResNet-SIREN architecture from locked constants up to full physics-informed loss terms, and provides isolated verification probes (gradcheck, residual, and overfit). The plans demonstrate exceptional engineering discipline, explicitly tackling complex precision boundaries, dimensional correctness on the canonical $u$ leaf, read-only dataset constraints, and rigorous falsifiability tests for the physics formulations.

## 2. Strengths
- **Rigorous TDD & Defensive Testing:** The "tests-first" methodology, combined with deferred-import skip guards, safely unblocks incremental single-file implementation. Testing for structural prohibitions (e.g., AST parsing to ensure no `v1.3` imports or precision leaks) is a highly robust verification strategy.
- **Dimensional Correctness (Gate B):** The finite differencing fix in `38-04`—differencing against the dimensionless $u = t/T$ leaf—resolves previous scaling errors and gives the ground-truth Newtonian-residual gate actual mathematical teeth.
- **Tautology Prevention (Gate A):** Mandating `torch.autograd.grad` through the scalar matched-Plummer potential prevents a hand-coded, closed-form tautology and forces a mathematically independent check of force consistency.
- **Robust Falsifiability:** Test fixtures are purposefully designed to fail on mutated force calculations, incorrect $D$ scaling, and scrambled trajectories, ensuring the test suite does not self-validate broken logic.

## 3. Concerns

- **MEDIUM — Causal Weight Underflow Bound (`38-05-01` / `38-05-03`):** 
  The plan states that the causal weight $w_n$ must stay "finite and in (0,1]". However, for a poorly initialized model or late in training, the exponential decay `exp(-eta_c * cumsum(Rbar_m))` will mathematically underflow to exactly `0.0` in float32/float64. If the test suite enforces a strict `> 0` assertion, it will spuriously fail upon underflow.
- **LOW — `LossWeights` Validation Missing (`38-05-02`):**
  While `ArchitectureSpec` employs fail-closed validation in its `__post_init__` to catch negative depths, the frozen five-field `LossWeights` container does not explicitly mandate checking for negative values. Passing negative lambda weights would silently cause catastrophic gradient ascent.
- **LOW — COM Offset Tolerance Default Unspecified (`38-06-02`):**
  The overfit probe emits a warning if the ground-truth mass-weighted COM offset "exceeds a documented tolerance". Unlike other explicitly pinned thresholds (e.g., `1e-3`, `1e-1`), this specific numeric default is absent from the plan text.

## 4. Suggestions
- **Relax or Clamp Causal Weights:** In `38-05-01`, relax the causal weight test constraint to `[0, 1]` instead of `(0, 1]`, or explicitly require `causal_physics_loss` to apply `torch.clamp(w_n, min=torch.finfo(dtype).tiny)` to avoid failing the test upon standard floating-point underflow.
- **Add `__post_init__` to `LossWeights`:** Implement a validation check within `LossWeights` that raises a typed `ValueError` if any supplied lambda weight is negative.
- **Pin the COM Offset Tolerance:** Assign an explicit default for the COM offset warning tolerance in `38-06-02` (e.g., `1e-6`) to maintain the rigor seen in all other build-engineering defaults.

## 5. Overall Risk: LOW
The Phase 38 plans are exceptionally detailed, defensive, and structurally sound. The boundaries of the modules are perfectly defined and respect downstream consumers (Phase 39/40 metadata, Phase 42 logging). The identified concerns are minor implementation details that do not threaten the phase goals, security, or architectural integrity.

---

## claude-max Review

I have read the SPEC, CONTEXT, and all six plan files in full. Below is my review. I verified the two load-bearing numeric claims (the Gate B dimensional analysis and `T_CHARACTERISTIC_TIME = 10.0`) by hand against the dimensionless-system relations; both hold. I did not need to open the global PROJECT/REQUIREMENTS/ROADMAP files to reach these findings — the phase-local artifacts were internally sufficient, and I note where a claim rests on an unverified downstream artifact.

---

# Cross-AI Plan Review — Phase 38 (PINN Model Rebuild from Specs, FUT-01)

## 1. Summary

Six plans rebuild the spec-faithful `pinn/` model stack (constants + arch-spec → network + COM head → residual + fixture loader → gradcheck/residual probes → loss catalog → overfit probe + prohibition checks) and prove it with three rungs. The plans are unusually mature: they have absorbed two cross-AI review cycles, the dependency DAG is clean (waves 1→5, no cycles), each requirement NET-01..05 maps to concrete tasks with tests-first ordering, and boundary/governance discipline (read-only specs, no `simulation_data/` writes, no v1.3 derivation, precision only via `resolve_runtime`) is enforced mechanically in 38-06. The math that was reworked in cycle 2 is sound. The chief residual weakness is one **unspecified model-input interface** on the NET-05 critical path, plus a few unenforced runtime assumptions.

## 2. Strengths

- **Rigorous Gate design (38-04).** Gate A (autograd-through-`V_eps` vs closed-form `softened_acceleration`, mass divided out) and Gate B (u-leaf finite-difference vs softened force) are genuinely independent, and the falsifiability tests (mutate `softened_acceleration` → Gate A fails; wrong-D trajectory → Gate B fails) give the residual rung real teeth. I re-derived Gate A (`a_i^V = -∇_i V_eps / m_i = softened_acceleration_i`) and Gate B (`v' = v_raw·T/D`, `a'_fd = d²r'/du²`, agreement iff `D³ = GT²`) — both correct.
- **`T_CHARACTERISTIC_TIME = 10.0` is over-determined, not invented.** It follows from the locked `D ≈ 4.6416` via `D³ = G·T² = 100`, cross-checked against `T = t_max = t_end = 10`. This respects the "don't invent" governance.
- **COM projection as a structural property**, not a convention — the "no unprojected output is public" test verifies architecture rather than usage.
- **Tests-first reordering and per-symbol deferred-import guards** correctly make partial-wave builds SKIP rather than ERROR.
- **No destructive-operation or data-integrity risk.** Evidence is non-overwriting under the phase tree; dataset access is read-only; specs are byte-identity-pinned to a pre-phase committed baseline. Scope creep is actively fenced.

## 3. Concerns

### HIGH

- **The 14-dim model input `[τ, IC₁₃]` is never specified for the overfit rung (38-06 / NET-05).** The overfit probe is the *only* rung that calls `forward(tau_ic13, masses)` (the residual and gradcheck rungs operate on trajectory/synthetic inputs and correctly need no model forward). To overfit, it must build `tau_ic13(u) = [2u−1, IC₁₃]` per collocation time — but no plan says where `IC₁₃` comes from. The fixture loader (38-03) yields raw masses/positions/velocities only; the Jacobi-state `IC₁₃` is *tanh-normalized with dataset-wide statistics*, and those statistics are an explicit Phase-39 artifact absent in this worktree. Cycle-1 finding H2 established exactly this ("raw masses unrecoverable from the tanh-normalized IC₁₃") for the *mass* argument but never closed the loop for the `IC₁₃` argument itself. As written, an executor either gets stuck computing a normalized `IC₁₃` it cannot produce, or invents one — which the phase governance forbids. It is trivially *resolvable* (a fixed placeholder `IC₁₃` is legitimate: a single-trajectory overfit conditions on a constant vector, so the net learns `τ → r'` and the ≥10³× smoke still holds), but that decision must be pinned in the plan with rationale, not left to the executor.

### MEDIUM

- **`causal_physics_loss` assumes time-sorted `Rbar_n` but nothing enforces or validates ordering (38-05).** `w_n = exp(-η_c·Σ_{m<n} stopgrad(Rbar_m))` is only meaningful on time-ordered collocation points. The plan says "sorted-time" but adds no assertion/guard; a caller (Phase 40's sampler, or a mis-shaped test batch) passing unordered `Rbar_n` would produce a silently wrong causal weight. A cheap ordering contract (documented precondition + a test that shuffled input changes the result / is rejected) would harden the seam.
- **Gate B's "~1e-3 truncation floor" is an unverified assumption for real chaotic trajectories (38-04).** The claim that a correct wiring lands near `1e-3` rests on smooth, densely-sampled kinematics. For a chaotic 3-body trajectory the second-order central difference error can be materially larger in high-curvature regions even above the min-separation guard. The design mitigates this (coarse `1e-1` band + operator records the measured floor on first real run), so PASS/FAIL is safe — but the "first real run" could surprise, and the narrative slightly oversells the floor. Worth flagging the band as provisional-until-measured in the evidence summary.

### LOW

- **`lambda_data` is a settable field defaulting to 1.0, but §3.1 fixes the data term unweighted (38-05).** The composer does not guard against a supplied `LossWeights(lambda_data≠1.0)` silently reweighting the data term. The plan relies on a prose note ("Phase 40's scheduler must not move it"). A construction-time assertion `lambda_data == 1.0` (or a documented rationale for allowing it) would make the invariant enforced rather than advisory.
- **Prohibition-check module coverage may drift (38-06-03).** The AST/no-write checks are described as both "iterate a module list" and "covered automatically." If the list is enumerated rather than globbed over `pinn/` + `pinn/verification/`, a future module silently escapes coverage. Prefer a glob.
- **Test hygiene: running probes inside `test_prohibitions` writes evidence dirs.** Unless each probe invocation in the test passes a tmp `--evidence-root`, the suite pollutes `.planning/.../evidence/` on every run. Cheap to fix; worth stating explicitly.

## 4. Suggestions

1. **Close the HIGH:** add one truth/decision to 38-06 (and the `forward` contract note in 38-02) stating the overfit probe conditions on a *fixed placeholder* `IC₁₃` (e.g. zeros or the raw parsed IC values, documented), justified as a single-trajectory wiring smoke, with an explicit note that physically-normalized `IC₁₃` is Phase-39 territory. This removes the only place an executor must invent an input.
2. Add a documented ordering precondition + one negative test for `causal_physics_loss`.
3. Mark the Gate B `1e-1` band and the `~1e-3` expected floor as "provisional until the first real-trajectory run" in the residual-probe evidence schema.
4. Enforce `lambda_data == 1.0` at `LossWeights` construction (or record why it is intentionally free).
5. Glob the prohibition module list and route in-test probe evidence to a tmp root.

## 5. Overall Risk

**MEDIUM (low end).** The plans are thorough, internally consistent, and mathematically sound where it matters most, and they achieve the phase goal for four of five requirements without reservation. The single HIGH item is a genuine unspecified interface sitting on the NET-05 critical path — resolvable in one sentence, but currently forcing the executor to either stall or invent, which this phase's governance explicitly prohibits. Resolving it plus the two MEDIUM hardening items would drop the phase to LOW risk.

---

## codex Review

## 1. Summary

Phase 38 plans are generally strong and appear capable of achieving the phase goal. Ordering is coherent, scope boundaries are explicit, and prior review findings have been substantially incorporated. No files were edited.

The main residual risks are proof-strength mismatches: a few checks claim stronger guarantees than they actually enforce.

## 2. Strengths

- Clear wave ordering: constants/spec → network/COM → residual/loader → probes/losses → overfit/prohibitions.
- Good scope discipline around Phase 39 ingestion, Phase 40 training, and read-only framework specs.
- Strong TDD-first structure with concrete files, interfaces, acceptance checks, and verification commands.
- Good data-integrity posture: provenance recording, non-overwriting evidence dirs, explicit `simulation_data/` read-only intent.
- Prior cross-review concerns are visibly folded into the plans rather than ignored.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** `38-06` spec byte-identity check proves final bytes match baseline, but not the stronger claim that specs stayed unchanged “before and after every Phase 38 commit.” A committed spec edit later reverted would pass the final hash check. Add a history-aware check over the phase range, e.g. `git log --name-only <phase-base>..HEAD -- <specs>`, or require the hash check in every plan’s pre-commit verification.

- **MEDIUM:** Rung-4 overfit diagnostics are “full-stack” but not gating. The plan allows PASS based on data-loss reduction while causal-physics/angular-momentum diagnostics are only recorded. If those input-available diagnostic terms are NaN or fail to compute, the probe should fail; only soft-energy should be allowed as “not evaluated” without Phase 39/40 `eps_h`.

- **MEDIUM:** The `simulation_data/` no-write check permits a weak fallback: directory mtime plus file-set snapshot. That can miss modifications to existing files or write/delete cycles. Prefer an `open`/`pathlib`/`os` write spy, or a pre/post content hash over relevant dataset files.

- **LOW:** `38-06` still says “records all five loss-catalog terms” in success criteria, while the task body correctly says soft-energy is not evaluated by default. Normalize this to “input-available terms plus soft-energy status/optional diagnostic.”

- **LOW:** The phase-wide AST check lists expected new modules explicitly while also claiming newly added modules are covered automatically. Use a glob/discovery check or assert no unexpected new `pinn/**/*.py` files exist outside the declared set.

## 4. Suggestions

- Add one phase-close “proof manifest” that records spec-touch history, prohibition results, real/deferred trajectory evidence, and full `tests/phase38` status.
- Make overfit diagnostic finiteness a hard requirement for input-available terms.
- Tighten `simulation_data/` mutation detection to content-level protection.
- Clarify stale “all five terms” wording before execution.

## 5. Overall Risk

**MEDIUM**. The implementation plan is well structured, but a few verification checks currently leave room for false confidence at phase close.

---

## claude-kimi Review

# Cross-AI Plan Review: Phase 38 — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Phase 38 plans a spec-faithful rebuild of the `pinn/` model package across six waves: locked constants + architecture spec (38-01), SQR-SkipResNet-SIREN network + COM projection head (38-02), PHYS-02 autograd residual + minimal read-only fixture loader (38-03), gradcheck and residual-on-ground-truth CLI probes (38-04), five-term loss catalog (38-05), and the single-trajectory overfit probe + phase-wide prohibition checks (38-06). The plans incorporate findings from two prior cross-AI review cycles and are tightly scoped against the locked `ctl_instruction.md` / `pinn_architecture.md` framework specs. Dependency ordering is clean: 38-01 → 38-02 → 38-03 → {38-04, 38-05} → 38-06.

## 2. Strengths

- **Strong test-first discipline**: every plan authors RED tests before implementation, with per-symbol deferred-import guards so partial progress SKIPs rather than ERRORs.
- **Prior review incorporation is explicit**: each plan contains a `review_incorporation` section documenting resolutions to cycle-1 and cycle-2 findings, including the Gate B finite-difference dimensional fix (`v' = v_raw * T/D`, `u = t/T`), the mandated autograd Gate A path, and the overfit full-stack input-provenance pinning.
- **Precision/device seam preserved**: all new modules accept explicit `dtype`/`device`, avoid `torch.set_default_dtype`, avoid availability probes, and are validated by AST checks.
- **Clear scope boundaries**: Phase 39/40/41 responsibilities are consistently deferred; the fixture loader is explicitly *not* the Phase 39 adapter.
- **Mechanical prohibition checks wired**: spec byte-identity (vs. pre-phase committed baseline), no `simulation_data/` writes, no precision defaults, and no v1.3-era imports are all backed by tests in 38-06-03.
- **Fail-loud overfit probe**: bounded max-step cap, NaN/Inf immediate FAIL, and cap-without-target FAIL with recorded ratio + calibration guidance.

## 3. Concerns

### MEDIUM — SIREN init statistics test criteria are fuzzy
- **Where**: `38-02-PLAN.md:118`
- The test must assert sampled weights fall within the exact §2.2 uniform bounds *and* that the empirical spread is "consistent with a uniform (not Kaiming/Xavier normal) init." The exact bounds are concrete; the "consistent with uniform" clause is not operationalized. Without a concrete statistical assertion (e.g., Anderson-Darling against uniform, or a bin-count test), the test could be tautological or flaky. Suggest pinning a concrete, cheap statistic.

### MEDIUM — Phase-wide prohibition test module-list coverage is ambiguous
- **Where**: `38-06-PLAN.md:204`
- The action says "Keep the check list data-driven (iterate a module list) so a newly added module is covered automatically," but also instructs reading a specific enumerated module list. If the list is hardcoded in `test_prohibitions.py`, newly-added modules in later waves may be missed. If it is discovered from the filesystem, the discovery rule must exclude v1.3-era files and generated artifacts. Suggest stating the exact discovery rule (e.g., glob `pinn/**/*.py` minus an exclude list).

### MEDIUM — Real-dataset evidence gate is manual and operationally risky
- **Where**: `38-06-PLAN.md:21-22`, `:106`
- The phase is correctly blocked from closing on synthetic-only evidence, but the gate depends on an operator manually running rung 3/rung 4 against a real admitted trajectory and committing evidence *or* logging a DEFERRED gap. This is appropriate for the worktree (no Brutus payload), but there is no automated reminder or checklist item enforcing it. The gap-register ownership note is good; consider adding the same gate language to the phase `success_criteria` in `38-SPEC.md` if not already present.

### LOW — Evidence directories may accumulate unbounded timestamped runs
- **Where**: `38-04-PLAN.md:104`, `38-06-PLAN.md:115`
- Each probe writes non-overwriting timestamped evidence under `.planning/phases/38.../evidence/<rung>/<UTC>/`. There is no retention or cleanup policy mentioned. For a long-running phase with many probe iterations, this could bloat the worktree. Suggest documenting whether old evidence is archived, deleted, or ignored.

### LOW — Fixture loader variant-to-folder mapping is hardcoded
- **Where**: `38-03-PLAN.md:100`
- `resolve_trajectory_path` maps a fixed set of variant strings to fixed `simulation_data/` folder paths. This is acceptable for a probe-local stopgap loader, but it will break if the dataset layout changes. The plan correctly limits this to Phase 38; no action required unless the mapping drifts.

## 4. Suggestions

1. **Concretize the SIREN init uniformity test** in `test_network_structure.py` (e.g., histogram chi-squared against uniform with a tolerant p-threshold, or assert that normal-init samples would fail the same test).
2. **Clarify the prohibition-test module discovery rule** in 38-06-03: specify whether the module list is a hardcoded tuple, a glob-with-excludes, or derived from `git ls-files`.
3. **Add a phase-close checklist item** (in 38-06 SUMMARY.md or a separate close note) enumerating the exact real-trajectory runs and evidence paths required before marking the phase complete.
4. **Document evidence retention** (keep last N runs, or commit only final runs) to prevent worktree bloat.
5. **Verify the batch-dimension contract at the 38-03/38-05 seam during execution**: the contract is well-documented in both plans, but a single shape mismatch would only surface at wave-4 integration; consider a thin seam test in 38-05 that constructs residuals from a stub and exercises `causal_physics_loss`.

## 5. Overall Risk

**MEDIUM**

The plans are coherent, well-scoped, and address prior review findings. Risk is medium rather than low because (a) the real-dataset phase-close gate is manual and could be forgotten, (b) the SIREN init test needs sharper criteria to avoid flakiness, and (c) the phase-wide prohibition test must not silently drop newly-added modules. None of these are blocking, but each should be tightened before or during execution.

---

## Consensus Summary

**CYCLE 3 (final) — 2026-07-13, adjudicated against the twice-revised plans (replan commits 05273b4c, 9f748245).**

**Panel health:** 5 real reviews — claude-deepseek, agy (first run), claude-max, codex, claude-kimi (subset rerun at 480 s after 360 s watchdog kills; codex's first-run stderr ended mid-investigation with no recoverable final review). 2 stubs kept after one retry each: claude-glm (upstream 529 both attempts — third consecutive cycle), grok (exit-0 preamble-only both attempts — third consecutive cycle). Cycle-2 report preserved at `38-REVIEWS.cycle2.md`.

### Unresolved HIGH (2, deduped)

1. **Overfit probe's 14-dim model input is unspecified on the NET-05 critical path (claude-max HIGH — new this cycle; CONFIRMED against plan text).** The overfit probe is the only rung that calls `forward(tau_ic13, masses)`. 38-06-02 pins the `masses` argument ("raw masses parsed for `forward(tau_ic13, masses)`") but no plan says how the probe constructs `tau_ic13` — the τ slot is derivable (τ = 2u − 1), but the IC₁₃ slice is tanh-normalized with **dataset-wide statistics** (`.claude/rules/pinn-reference.md:31`), a Phase-39 artifact with no Phase-38 source; the 38-03 `TrajectoryFixture` yields times/positions/velocities/masses only. Cycle-1 H2 closed this loop for `masses` but not for `IC₁₃` itself. As written the executor must either stall or invent — which this phase's governance forbids. One-sentence fix: pin a fixed documented placeholder `IC₁₃` (constant conditioning vector is legitimate for a single-trajectory overfit) in 38-06 + a note in 38-02's forward contract, with normalized IC₁₃ explicitly deferred to Phase 39.
2. **Spec byte-identity truth overclaims what the wired check proves (codex HIGH — new this cycle; CONFIRMED against plan text).** 38-06 must-have truth: specs are "byte-identical **before and after every Phase 38 commit**"; the wired check (38-06-03) compares final working-tree sha256 to the pre-phase committed baseline — endpoint-only. A spec edit committed mid-phase and later reverted passes, contradicting the stated truth and SCOPE-18's no-spec-touch governance. Fix: add a history-aware check (`git log --name-only <phase-base>..HEAD -- <both specs>` asserted empty) to `test_prohibitions.py`, or weaken the truth to endpoint identity.

### Unresolved actionable MEDIUM/LOW (9, deduped)

1. **(M — 3-reviewer consensus: kimi M2 / codex L / claude-max L)** Prohibition-check module coverage rule unspecified: 38-06-03 enumerates 10 modules yet claims "a newly added module is covered automatically." Pin the discovery rule (glob `pinn/**/*.py` minus a v1.3 exclude list) in the plan.
2. **(M — codex)** Rung-4 full-stack diagnostics are recorded but never finiteness-checked: a NaN/failed-to-compute input-available diagnostic term (IC / causal-physics / angular-momentum) still PASSes, producing false full-stack confidence. Require finite evaluation of input-available terms (FAIL or explicit flag); only soft-energy may be "not evaluated".
3. **(M — codex)** `simulation_data/` no-write check permits a weak fallback ("pre/post directory-mtime + file-set snapshot") that misses content modification of existing files. Drop the fallback or require open-spy / content hashes.
4. **(M — claude-max)** `causal_physics_loss` sorted-time precondition is documented (38-05-03) but unenforced and untested. Add the documented precondition + one negative/ordering test.
5. **(M — kimi)** SIREN init test's "empirical spread consistent with a uniform init" (38-02-01:118) is not operationalized; the bounds check alone cannot catch a narrower Xavier-uniform substitute. Pin a concrete cheap statistic (e.g. per-layer empirical min/max within x% of the bound, or variance ≈ b²/3).
6. **(L — codex)** 38-06 `success_criteria` still says "records **all five** loss-catalog terms" — contradicts the body's soft-energy "not evaluated" default. Reword to "input-available terms + soft-energy disposition".
7. **(L — agy + claude-max, merged)** `LossWeights` has no construction-time validation: negative λ passes silently (gradient ascent) and `lambda_data`'s "FIXED at 1.0" invariant is advisory prose only. Add `__post_init__` validation (non-negative; `lambda_data == 1.0` or a documented reason it is free).
8. **(L — agy)** The overfit probe's COM-offset warning threshold is "a documented tolerance" with no pinned value — the only unpinned numeric knob left after `--lr`/`--max-steps` were pinned. Pin a default (with rationale) in 38-06.
9. **(L — claude-max)** Tests that invoke probes are not directed to pass a tmp `--evidence-root`, so every suite run pollutes `.planning/.../evidence/`. Mandate tmp evidence roots in the probe test tasks.

### Raised but resolved / excluded (fix visible in current plan text, or non-actionable)

- deepseek HIGH (`--max-steps 3000` uncalibrated): already resolved — plan documents the UNCALIBRATED default, override, cap-FAIL calibration guidance, one-shot calibration; deepseek itself notes "recoverable… operator experience, not correctness."
- agy MEDIUM (causal-weight underflow to 0.0 vs strict `(0,1]`): already incorporated — 38-05-03 mandates the underflow-only exponent clip, which keeps `w_n > 0` and makes the `(0,1]` assertion consistent.
- claude-max MEDIUM (Gate B ~1e-3 floor provisional): substantially incorporated — the gating band is the coarse 1e-1 with the operator recording the measured floor on the first real run; residual ask is evidence-summary wording only.
- kimi MEDIUM (manual real-dataset phase-close gate): already incorporated — explicit must-have truth, planner assumption, ownership note, and success criterion with the DEFERRED gap-register path.
- deepseek MEDIUM (38-05 two-task single-file discipline), deepseek LOW (full-stack diagnostic complexity), deepseek/kimi LOW (hardcoded loader folder mapping — both reviewers say no action; `--path` escape hatch + Phase-38-only scope), kimi LOW (evidence retention policy): observations / marginal; no plan change required.

**Verdicts on the items cycle 3 was asked to scrutinize:** `T_CHARACTERISTIC_TIME = 10.0` grounding — SOUND and spec-grounded (pinn_architecture.md:980 `T = t_max`, dataset horizon `t_end = 10`, cross-checked by PIPE-09 `D³ = GT²` with locked D ≈ 4.6416 = ∛100; claude-max re-derived by hand). u-leaf Gate-B formulas — SOUND (`v' = v_raw·T/D`, `a'_fd` on `Δu = Δt/T`; agreement iff `D³ = GT²`; dimensional check reproduced independently). Soft-energy "not evaluated" disposition — SOUND (respects §3.4:542 "no fallback numeric floor"; no invented S_H), though see actionable #2/#6 for the finiteness gate and stale wording. Autograd Gate-A mandate — SOUND (faithful operationalization of §10.4:1032; mutation falsifiability test forces the independent path).

## Verification coverage

**CYCLE 3 source-grounding pass (2026-07-13).** Authority: `drift-guard authority --raw` → `grep`. Severity map (drift-guard, authority=grep): VERIFIED → {severity: none, hardBlock: false}; MISSING → {severity: needs-acknowledgement, hardBlock: false}; AMBIGUOUS → {severity: MEDIUM, hardBlock: false}; UNCHECKABLE → {severity: INFO, hardBlock: false}. **Result: no MISSING, no AMBIGUOUS, no hardBlock.** Symbols declared under "Artifacts this phase produces" are excluded per protocol (all `pinn/constants.py` exports incl. `T_CHARACTERISTIC_TIME`, `ArchitectureSpec`, `build_network`/`SQRSkipResNetSIREN`/`forward(tau_ic13, masses)`, `project_com`, `physics_residual`/`softened_acceleration`/`componentwise_du`, `load_trajectory`/`resolve_trajectory_path`/`sha256_file`/`TrajectoryFixture`, `LossWeights`/`LossTerms`/five loss callables/`compose_total`, `run_gradcheck`/`run_residual_on_ground_truth`/`run_overfit`/`main`, all new-probe CLI flags incl. `--lr`/`--eps-h`, `tests/phase38/*`) — their *grounding citations* are verified below.

| Symbol / citation (plan cite) | Verdict | Evidence |
|---|---|---|
| `pinn_architecture.md:980` Table 2 Unit System `T = t_max`, `D = ∛(GT²)` (38-01/38-04) | VERIFIED | pinn_architecture.md:980 (exact line) |
| `pinn_architecture.md:983` SIREN init bounds U[-1/n_in,1/n_in], U[-√(6/n_in)/ω,+] (38-02) | VERIFIED | pinn_architecture.md:983 (exact) |
| `pinn_architecture.md:892/:897` physics layer `(u, r', v')`, `v' = dr'/du` (38-04) | VERIFIED | pinn_architecture.md:890-900 (Phase-35 contract block + three-layer separation) |
| §5.3.1 PHYS-02 u-leaf, no chain factor; `r.sum()` VJP forbidden (38-03) | VERIFIED | pinn_architecture.md:888 (heading), :890 (contract), :913 (forbidden) |
| §3.4 `ε_H = 1e-4·S_H`, persist both, no fallback floor — lines 527/531/542 (38-05/38-06) | VERIFIED | pinn_architecture.md:527, :531, :542 (all three exact) |
| §10.4 force-energy consistency `relative_error < 1e-5` via negative position gradient (38-04) | VERIFIED | pinn_architecture.md:1031-1032 |
| §10.2 COM invariance `abs(COM) < 1e-10` (38-02) | VERIFIED | pinn_architecture.md:1021-1022 |
| §2.2/§2.3/§2.4 SIREN ω 30/1, depth 12 × width 256, LayerNorm(elementwise_affine=False, eps=1e-5) odd layers, p=2, Table 1 (38-01/38-02) | VERIFIED | pinn_architecture.md:149, :190, :248, :259-261, :981 |
| §3.1 data Huber `δ_r = 1`, data term unweighted (38-05) | VERIFIED | pinn_architecture.md:303/:307, :358 |
| §3.2 softened force, `ε_train = 1e-5`, causal `w_1=1`/`η_c=1` (D-04 Option A), exponent-clip bound deferred to FUT (38-03/38-05) | VERIFIED | pinn_architecture.md:362, :381/:403, :414, :424, :647 |
| §3.3 IC anchor `β_v = 1`, `λ_IC = 1` (38-05) | VERIFIED | pinn_architecture.md:473, :481 |
| §3.5 ang-mom Huber δ=1.0, `L_scale = ‖L₀'‖ + ε_L`, `ε_L = 1e-8` (38-05) | VERIFIED | pinn_architecture.md:611, :613, :616 |
| `ctl_instruction.md` §2.5 raw-mass D ≈ 4.6416; 6.694 rejected; PIPE-09 `D³ = GT²` at line 1024; PHYS-03 additive-ε anti-pattern prohibited (38-01/38-03) | VERIFIED | ctl_instruction.md:992, :1005/:1011, :1016, :1024 (exact) |
| `ctl_instruction.md` "Phase 2 Total Training Loss"; λ frozen during L-BFGS (38-05) | VERIFIED | ctl_instruction.md:1744, :1764 |
| `pinn.runtime.RuntimeSpec` frozen dataclass `:23-38`; fail-closed `:84-95`; `resolve_runtime` (all plans) | VERIFIED | pinn/runtime.py:23-24, :65, :84-90 |
| `pinn/verification/componentwise_ad.py` cited ranges `:30-41` fallback capture, `:62-76` synthetic_trajectory/as_tensor, `:113-118` AGGREGATE_CRITERION, `:128-157` explicit-leaf jacrev, `:193-206` non-finite refusal, `:215-229` result dict, `:371-394` argparse/main | VERIFIED | each anchor line matches described content (file is 398 lines) |
| `torch.func.jacrev` (38-03) | VERIFIED | existing usage pinn/verification/componentwise_ad.py:139 |
| `torch.autograd.gradcheck(fn, inputs, eps=1e-6, atol=1e-5, rtol=1e-3)` / `torch.autograd.grad(V_eps, positions)` signatures (38-03/38-04) | UNCHECKABLE | library signatures not verifiable under grep authority; standard torch API, torch import verified via Phase-37 suite |
| `scripts/run_precision_probe.py` `_sha256_file :109-113`, `write_evidence_run :390-420` (38-04/38-06) | VERIFIED | scripts/run_precision_probe.py:109, :390 |
| `tests/phase37/test_runtime.py` `:66-73` frozen assert, `:122-137` default-dtype assert, `:139-183` AST technique (38-01/38-02/38-06) | VERIFIED | tests/phase37/test_runtime.py:66, :122, :139-183 |
| `tests/phase37/test_componentwise_ad.py`, `test_precision_orchestrator.py`, `tests/phase37/__init__.py` (multiple plans) | VERIFIED | files exist in tests/phase37/ |
| `pinn/__init__.py` current surface = RuntimeSpec + resolve_runtime only (38-02 claim) | VERIFIED | pinn/__init__.py:18-20 |
| `pinn/verification/__init__.py` docstring "second-order work belongs to Phase 38" (38-03 claim) | VERIFIED | pinn/verification/__init__.py:3-5 |
| conda env `pinn-train` (all verify commands) | VERIFIED | env dir present under the local conda envs root (conda binary not on sandbox PATH) |
| Spec last-touch commits `e7226ff0` (ctl, 2026-07-11) / `583a010f` (pinn_arch, 2026-06-29) (38-06) | VERIFIED | `git log -1 --format=%h -- <spec>` reproduces both hashes exactly |
| 38-CONTEXT CTX-15/-20/-21/-26/-32 (multiple plans) | VERIFIED | 38-CONTEXT.md:67, :95, :102, :132, :162 |
| REQUIREMENTS NET-01..05, SCOPE-18/-20 (all plans) | VERIFIED | .planning/REQUIREMENTS.md:40-44, :126, :128 |
| 38-PATTERNS "Deferred-import skip guard" / "Frozen-dataclass assertion" (38-01/38-02) | VERIFIED | 38-PATTERNS.md:234, :238, :43 |
| 38-SPEC Edge Coverage R3/R4/R5 planner-assumption rows; two descriptor-empty prohibitions per `--auto` (CTX-32) (38-03..06) | VERIFIED | 38-SPEC.md:93-95, :105, :108 |
| dataset README: completeness ≥ 9.5; gold `dt_out = 0.01`; horizon `t_end = 10`; `Result:` footer schema-varies/optional; File Naming/File Schemas/Physical Conventions/Mass Normalization sections (38-03/38-06) | VERIFIED | simulation_data/Documentation/README.md:526/:553, :180, :287, :283, :193/:226/:304/:314 |
| Loader folder-mapping names (4 brutus + 2 ic folders; ID-maps-IC↔Brutus; folder-defines-variant) (38-03) | VERIFIED | README.md:97-104/:148-152; .claude/rules/dataset-reference.md:24-34 |
| Physical payload dirs `simulation_data/Data/{brutus_output,ic_final}/` on disk (38-03 default trajectory) | UNCHECKABLE | absent in this worktree by design (bulk payload excluded); 38-03 `<default_trajectory>` explicitly acknowledges; operator-run gate covers it |
| `.claude/rules/pinn-reference.md` tanh-normalized IC₁₃ with dataset-wide statistics (38-02; HIGH #1 premise) | VERIFIED | .claude/rules/pinn-reference.md:31 |
| `scripts/agent-commit`, `gsd-tools.cjs` (process tooling) | VERIFIED | invoked successfully this cycle |

## xreview Diagnostics

### claude-glm
- reviewer=claude-glm
- exit_code=1
- elapsed_seconds=218
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=245
- stderr_bytes=192

### claude-deepseek
- status: preserved from existing REVIEWS.md

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=18
- timeout_seconds=480
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T081015Z-19768/xreview-prompt-38.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=913
- stdout_bytes=163
- stderr_bytes=0

### agy
- status: preserved from existing REVIEWS.md

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=297
- timeout_seconds=480
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=7661
- stderr_bytes=0

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=427
- timeout_seconds=480
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3140
- stderr_bytes=241350

### claude-kimi
- reviewer=claude-kimi
- exit_code=0
- elapsed_seconds=193
- timeout_seconds=480
- watchdog=not_triggered
- command=ccp kimi -p - 
- stdout_bytes=6135
- stderr_bytes=192

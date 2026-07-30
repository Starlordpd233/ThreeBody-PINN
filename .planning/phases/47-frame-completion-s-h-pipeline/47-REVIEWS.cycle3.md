---
phase: 47
reviewers: [codex, codex1, claude-max, claude-alt]
rerun_reviewers: [codex, codex1, claude-max, claude-alt]
reviewed_at: 2026-07-30T08:15:40Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T080940Z-2298
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 47

## codex Review

## 1. Summary

The three Phase 47 plans are well ordered and mostly achieve the phase goal: 47-01 completes the frame residency repair, 47-02 builds `S_H`, and 47-03 wires `ε_H`. The main remaining risks are execution-blocking evidence provenance and one metadata API ambiguity. No files were edited.

## 2. Strengths

- Strict wave order matches the roadmap’s load-bearing dependency: CONF-09 before CONF-02 before CONF-03.
- 47-01 correctly makes residency, frame re-ratification, and the corrected pairing test atomic.
- 47-02 has strong data-integrity coverage: float64 capture, train-split median, atomic metadata write, fail-closed load validation.
- 47-03 preserves the correct denominator shape, removes only the prohibited `+1e-12` floor, and adds a required `s_h` channel instead of smuggling derived data into config.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH**: 47-03 closure may block on a non-existent real `training_metadata.json`. The plan requires `S_H/ε_H/N_train` from a “most recent fresh launch” and says to STOP if none exists ([47-03-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-03-PLAN.md:205), [47-03-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-03-PLAN.md:209)), but the phase forbids training runs and the current worktree has no `training_metadata.json`. This can deadlock closure or pressure an executor into running prohibited training.

- **MEDIUM**: `load_training_metadata(run_dir)` is specified without an expected config/factor parameter, yet it must reject artifacts whose `energy_floor_factor` differs from the live run config ([47-02-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-02-PLAN.md:222), [47-02-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-02-PLAN.md:227)). Since `energy_floor_factor` is configurable ([config.py](<home>/Desktop/3_body_problem/.worktrees/trainex/pinn/training/config.py:161)), the loader needs the live expected value explicitly.

- **MEDIUM**: The D-08 near-invariance test asks the executor to derive a tolerance, but the formula is not pinned ([47-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-01-PLAN.md:228), [47-CONTEXT.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md:108)). That is workable, but close to the project’s “no tuning / no new threshold” boundary.

- **LOW**: Several acceptance gates use exact `grep` strings. They are backed by behavioral tests, so this is not a correctness blocker, but it may create execution friction on harmless formatting changes.

## 4. Suggestions

- Add an explicit metadata-only real-data command that computes/writes or reads the 47-02 `training_metadata.json` without starting training, then make 47-03 consume that named artifact.
- Change the metadata load API to accept expected live bindings, e.g. `load_training_metadata(run_dir, *, expected_energy_floor_factor, expected_eps_train=EPS_SOFT)`.
- Pin the D-08 tolerance formula in the plan before execution, or explicitly route it as a gap if it cannot be derived mechanically.
- Keep the exact-string grep checks as secondary guards; rely on pytest assertions as the primary behavioral gates.

## 5. Overall Risk

**MEDIUM**. The technical decomposition is strong, but the phase can still stall or accept stale metadata unless the closure-evidence path and metadata-load API are tightened.

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
- stderr_bytes=561193

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T080940Z-2298/xreview-codex1-47.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T080940Z-2298/xreview-codex1-47.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T080940Z-2298/xreview-codex1-47.meta

Stderr excerpt:
```
 masses=masses, side=side, n_snapshots=n_snapshots, n_periods=n_periods
522-    )
523-    offset_vec = np.asarray(offset, dtype=np.float64)
524-    drift_vec = np.asarray(drift, dtype=np.float64)
525-    t = trajectory.times_raw
526-    positions_raw = trajectory.positions_raw + offset_vec.reshape(1, 1, 3) + (
527-        drift_vec.reshape(1, 1, 3) * t.reshape(-1, 1, 1)
528-    )
529-    velocities_raw = trajectory.velocities_raw + drift_vec.reshape(1, 1, 3)
530-    D = trajectory.D
531-    T = trajectory.T
532-    offset_trajectory = DualFrameTrajectory(
533-        masses=trajectory.masses,
534-        times_raw=trajectory.times_raw,
535-        positions_raw=positions_raw,
536-        velocities_raw=velocities_raw,
537-        times_scaled=trajectory.times_raw / T,
538-        positions_scaled=positions_raw / D,
539-        velocities_scaled=velocities_raw * T / D,
540-        D=D,
541-        T=T,
542-        finite_difference_tolerance=trajectory.finite_difference_tolerance,
543-    )
544-    return offset_trajectory, offset_vec, drift_vec

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## claude-max Review

I have enough to write the review. I verified the plans' core source claims directly (residency source, the `+1e-12` floor at the `eps_h` assembly line, the loss denominator, the seam locals, the frame constant, and the 12 `RunController(` sites), and cross-checked CONF-02/03/09 against REQUIREMENTS and 47-CONTEXT. I did not need to load ROADMAP/PROJECT/AGENTS/RESEARCH in full; I resolved the success-criteria mapping through REQUIREMENTS + CONTEXT + the plans' inline citations.

---

# Cross-AI Plan Review — Phase 47 (Frame Completion & S_H Pipeline)

## 1. Summary

Three plans discharge CONF-09 → CONF-02 → CONF-03 in a load-bearing wave order (frame completion first, because `S_H` is frame-dependent, `H' = D·H`). 47-01 swaps residency from `pre.r_com_ordered/v_com_ordered` to `pre.r_gauge/v_gauge`, re-ratifies `RATIFIED_VALIDATION_FRAME`, and corrects the one superseded pairing test — all in one atomic commit. 47-02 builds the float64 `S_H = median_train(K0+Uabs0)` pipeline with a fail-closed, re-validated `training_metadata.json`. 47-03 wires `ε_H = 1e-4·S_H` through a required constructor channel and deletes the spec-prohibited additive floor.

I confirmed the plans' key anchors against live source: `adapter.py:865-866` residency, `controllers.py:482` (`abs(h0) * energy_floor_factor + 1e-12`) with the WR-02 rationalizing comment at `:478-481`, `loss_catalog.py:284` denominator, the `kinetic`/`potential` seam locals at `:148/:151`, the current raw `RATIFIED_VALIDATION_FRAME` at `:788`, `(SCALED, NORMALIZED)` present in `COHERENT_FRAME_PAIRS`, and the 12 test-side `RunController(` sites (7 phase40 / 3 phase41 / 2 phase43). All match. These are unusually rigorous, well-grounded plans.

## 2. Strengths

- **Grounding discipline is excellent.** Every semantic choice carries a `[GROUNDED]`/`[JUDGEMENT]` tag with a spec/requirement/ruling citation; scope locks (SCOPE-27..32) are enforced by empty-diff grep criteria on `preprocessing.py`, `config.py`, `pinn/verification/`, and spec files.
- **Line-drift caught proactively.** 47-01 re-verified anchors on 2026-07-29 and explicitly flags the stale `validation_gate.py:526-528` citation carried in CONTEXT/REQUIREMENTS, instructing grep-by-symbol.
- **The three swap lines are correctly treated as trivial; the proof is the work.** IC₁₃ invariance (D-04, checkable because `r_gauge[0]≡r0_gauge`), the `dr'/du=v_gauge` identity, approximate (not exact) gate-metric invariance, and a one-shot record-only re-probe are each independently verified.
- **Fail-closed coverage is thorough:** NaN/inf/negative/exact-0.0/empty-pool/single-element, order-invariance, even-population median, tamper-on-load, unknown-key rejection, atomic write, and a resume recompute-and-refuse path (added in cycle 1). Atomicity of the CONF-09 change is enforced (criterion 7).
- Prior cross-AI cycles already fixed real defects (the `set -o pipefail` false-green regression gate; the named metadata-only read command).

## 3. Concerns

**MEDIUM — 47-02 → 47-03 `s_h` local hand-off is under-specified on the resume path.** 47-02 "holds the validated `s_h` in a local" and 47-03 threads `s_h=s_h` into `RunController(...)` at `train.py:964`. On the *resume* branch, 47-02 describes recompute-and-compare but does not explicitly state that the branch assigns the same `s_h` local that 47-03 consumes. If the resume branch only compares and does not bind `s_h`, the `RunController(s_h=s_h)` call is unbound on resume. Not exercised in Phase 47 (no training run), so it is a latent defect that first bites in Phase 50. The plans should state that both the fresh and resume branches produce the `s_h` local, and that they live in one function scope spanning `:801`→`:964`.

**MEDIUM — 47-03 Task 2's closing `S_H/ε_H/N_train` values are likely unobtainable within the phase.** `training_metadata.json` is new in 47-02 and is only written by `train.py` setup against the real corpus; no plan runs setup (Phase 47 is build-only per its own reading of SCOPE-27, with training deferred to Phase 50). So criterion 5's "byte-identical to the metadata-only read command over a real `run_dir`" will most likely hit the STOP-and-surface branch. That is *safe* (fail-closed over fabrication), but it means a stated closure deliverable/success signal is probably unreachable by the phase's own actions. Recommend marking the real-value record explicitly deferred/optional, or authorizing a setup-only (no-step) metadata emission, so the phase can close cleanly instead of on a STOP.

**MEDIUM — the D-08 gate-metric tolerance must be derived a priori, which is genuinely hard.** 47-01 Task 2 and 47-02 forbid tuning the tolerance to observed output (SCOPE-29) yet require it be derived "from the softening-vs-separation argument." A defensible closed-form bound for the `r_safe = √(‖Δr‖²+ε²)` floor asymmetry across two frames is nontrivial; if the executor cannot derive it cleanly, the test risks being either vacuously loose (masking a real regression) or too tight (failing a correct impl) — and creates a subtle temptation to peek at output. Suggest the plan supply the derivation skeleton (bound as a function of `ε`, `D`, and minimum separation), not just the mandate.

**MEDIUM — the independent body-order oracle now reimplements the rotation gauge inline.** 47-01 Task 1(d)(i) extends `_resident_fixture` to apply rotation gauge + D/V scaling "reimplemented inline, never by calling `preprocess_trajectory`." A rotation gauge (principal-axis / eigendecomposition-style alignment) rarely reproduces bit-for-bit across two implementations, so any `np.array_equal` exactness against `preprocessed.r_gauge` in that *independent* oracle may be infeasible. (The direct pairing assertion in (d)(ii) is sound because both sides share the same `preprocess_trajectory` call.) Ensure the extended independent oracle compares body-order/structure or uses a scale-relative tolerance, not bit-exactness.

**LOW — 47-03 sweep completeness for phase43 has a coverage seam.** Task 1's `<verify>` runs only phase40/phase41; the 2 phase43 `RunController(` sites are covered only by Task 2's full-suite baseline comparison. Because phase43 tests are environmental (may skip/error without real data) and `s_h` is a *required* kwarg, a missed `s_h=` at a phase43 site could go unexercised, and criterion 4's illustrative `grep 'RunController(' | grep -v 's_h='` is unreliable for multi-line calls (the opening-paren line never contains `s_h=`). The pytest gate is the real backstop but does not reach phase43 here. Prefer an AST/`grep -A` per-file check over the single-line grep.

**LOW — stale `:526-528` citation persists in CONTEXT D-05 and REQUIREMENTS CONF-09.** 47-01 handles it operationally (grep the symbol), but the governance docs still misdirect a future reader to `_metrics_equal`. A one-line correction in the planning docs (not spec files, so SCOPE-30-safe) would remove the trap.

**LOW — velocity-identity finite-difference assumes benign time sampling.** The central-difference check of `r_gauge` vs `v_gauge` over `u=t/T` needs the actual (possibly non-uniform) Brutus `Δu`; a naive uniform-grid central difference degrades to O(Δu) on non-uniform samples. The "sampling-step-derived tolerance" must be computed from the real per-interval spacing.

## 4. Suggestions

- State explicitly in 47-02/47-03 that the `s_h` local is bound on **both** setup branches and that 47-02's compute and 47-03's `RunController(...)` construction share one function scope; add a resume-path assertion test that `RunController` receives a valid `s_h` after a load.
- Re-classify 47-03 Task 2(iii) real-value recording as deferred-with-STOP by default, or add an explicit, owner-sanctioned setup-only metadata emission step so the phase closes without leaning on an artifact no plan creates.
- Include the D-08 tolerance derivation (as an inequality in `ε`, `D`, min-separation) in the plan text so the executor implements a formula rather than inventing one under time pressure.
- Replace the single-line `s_h=` sweep grep with a per-file AST or `grep -A3` check, and add the 2 phase43 sites to a static assertion since the runtime gate may not reach them.
- Fix the `:526-528` reference in CONTEXT.md/REQUIREMENTS.md (planning docs, SCOPE-30-safe).

## 5. Overall Risk

**LOW–MEDIUM.** The plans achieve the phase goal, respect the phase boundary with no scope creep, order the waves correctly, and carry no security or destructive-operation risk (the sole external action, the D-22 probe, is one-shot, record-only, unmodified, with path-resolution preflight already incorporated). The residual risk is concentrated in cross-plan integration seams (the `s_h` local on resume), the deliverability of the real closing `S_H` values, and two hard-to-pin numeric tolerances (D-08 and the rotation-gauge oracle). None threaten data integrity; all are addressable with clarifying edits before execution.

*All listed files were readable; none failed to load.*

---

## claude-alt Review

I have enough to review. The grep for `run_dir`/`SCOPE-27` in VALIDATION returned nothing, confirming the validation contract is silent on where a real `training_metadata.json` comes from — which sharpens my main concern. Here is the review.

---

# Phase 47 Plan Review — Frame Completion & S_H Pipeline

## 1. Summary

The three plans discharge CONF-09 (47-01), CONF-02 (47-02), CONF-03 (47-03) in a clean wave chain (1→2→3, `depends_on` correct). Collectively they (a) move resident position/velocity series from the CONF-08 intermediate to the fully-gauged `r_gauge`/`v_gauge` and re-ratify `RATIFIED_VALIDATION_FRAME` atomically, (b) compute `S_H = median_train(K0 + Uabs0)` once in float64 with fail-closed persistence, and (c) wire `ε_H = 1e-4·S_H` into loss assembly while deleting the spec-prohibited additive floor. The plans are unusually rigorous: decision IDs (D-01..D-27) are threaded to acceptance criteria, threat models are scoped correctly for an internal single-operator pipeline, and two prior cross-AI convergence cycles are already folded in. The work is genuinely achievable and the plans do achieve the stated phase goal.

## 2. Strengths

- **Atomicity is enforced, not hoped**: 47-01 Task 1 criterion 7 asserts one commit hash covers adapter + frame constant + pairing test + evidence — directly closing the "constant lies to `COHERENT_FRAME_PAIRS`" trust boundary (T-47-01).
- **Single-oracle discipline**: correcting the phase-46 pairing test in place (D-06) rather than adding a parallel Phase 47 oracle avoids the exact competing-oracle failure 46-CONTEXT warns against; the extended fixture reimplements the gauge inline rather than calling `preprocess_trajectory`, preserving independence.
- **Fail-closed rigor**: strict positivity (`0.0` rejected same as NaN), empty-pool refusal before `numpy.median`, refusal-precedes-artifact ordering, and re-validation on every load. The `test_resume_recompute_refuses_mismatch` addition (from cycle-1) genuinely closes a real gap that load-side-only testing left open.
- **Dual-epsilon separation** is defended structurally (grep criterion 3 in 47-02 forbids `gate_metrics`/`EPS_INV` in the four data/loss files) rather than by convention.
- **Scientific-integrity discipline**: the one-shot record-only re-probe, the "never tune to observed output" tolerance rule, and the "loss magnitudes will move — not a signal" framing are consistently applied and guard against the phase quietly becoming a tuning exercise.

## 3. Concerns

**MEDIUM — 47-03 Task 2 real `S_H`/`ε_H`/`N_train` provenance is unreachable within phase scope.** `training_metadata.json` is written only by `pinn/train.py` setup during an actual run launch, but SCOPE-27 forbids any training run in this phase and 47-02 exercises the pipeline only through synthetic duck-typed sources. Task 2 (iii) requires the closing values to come from a real `run_dir/training_metadata.json` "from the most recent fresh launch," with STOP-and-surface if absent. In an autonomous run of an isolated worktree, that run_dir will almost certainly not exist, so the closure record's headline numbers will routinely hit the STOP path. This is not a correctness bug — the guard is honest — but the phase cannot autonomously produce its own stated closing evidence, and 47-VALIDATION.md is silent on the provenance. Consider either (a) explicitly declaring the real-value closing record a deferred/human-provided item, or (b) permitting a bounded synthetic-source `compute_s_h`+`write_training_metadata` invocation clearly labelled non-authoritative, so the phase closes deterministically.

**MEDIUM — D-08 tolerance is derived analytically with no permitted sanity anchor.** `test_gate_metric_near_invariance` and the D-23 record compare two frames through `gate_metrics` and `_matched_plummer_hamiltonian`, asserting closeness within a tolerance that SCOPE-29 forbids deriving from any observed number. A softening-floor-asymmetry argument yielding a bound that is never sanity-checked against a single observed value risks a tolerance that is either too tight (flaky/false-red on a correct implementation) or too loose (passes a genuine frame defect). The integrity rationale is sound, but a purely a-priori bound on a cross-frame numeric comparison is the most fragile assertion in the set. Recommend the tolerance derivation be reviewed by the user before execution, or that a one-directional "the difference is bounded and non-zero" structural check accompany the numeric bound.

**LOW — brittle exact-string grep criteria.** Several acceptance checks match exact argument order or phrasing: 47-02 criterion 4 (`compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)` == 1), 47-03 criterion 3 (`energy_floor_factor) * self._s_h`). Cycle-2 already deferred this for 47-03 with a defensible rationale (paired with behavioral pytests), but the same brittleness lives unremarked in 47-02; a whitespace/formatting variance from the executor could false-red a correct change. The paired behavioral tests are the real gate, so severity is low.

**LOW — cross-wave line-number drift in `read_first` anchors.** 47-03 cites `pinn/train.py:955-985` / `:964` for the `RunController` construction, but 47-02 inserts a metadata block earlier in the same file, shifting those lines. The plans repeatedly instruct "grep the symbol, do not trust the line," and 47-01 already documents a stale citation, so this is mitigated in practice — but the wave-2→wave-3 shift is a concrete, predictable instance worth an explicit note in 47-03.

## 4. Suggestions

- Resolve the 47-03 Task 2 provenance tension explicitly before execution (declare it human-supplied/deferred, or sanction a labelled synthetic emission) so autonomous closure is deterministic rather than STOP-gated.
- Have the D-08 tolerance derivation reviewed as a standalone artifact; record the closed-form bound and its inputs in the test docstring so a reviewer can audit it without re-deriving.
- Where feasible, loosen the two remaining exact-string greps in 47-02 to symbol-presence + the existing behavioral pytest, matching the reasoning already applied elsewhere.
- Add a one-line note to 47-03 `read_first` that its `train.py` line anchors are pre-47-02-insertion and must be grep-resolved.

## 5. Overall Risk: **LOW–MEDIUM**

The plans are internally consistent, correctly ordered, tightly scoped (no framework-spec or `pinn/verification/` edits; test-file edits in phase40/41/43 are the necessary consequence of a required constructor parameter, not scope creep), and free of destructive or data-integrity hazards. The only substantive execution risk is the 47-03 closure-evidence provenance, which is guarded by a STOP-and-surface but may block clean autonomous completion. The D-08 analytic tolerance is the one place where a correct implementation could still produce a flaky result.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=253
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3754
- stderr_bytes=359043

### codex1
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=561193

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=320
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=9035
- stderr_bytes=0

### claude-alt
- reviewer=claude-alt
- exit_code=0
- elapsed_seconds=122
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp alt --model claude-opus-4-8 -p - 
- stdout_bytes=6913
- stderr_bytes=0

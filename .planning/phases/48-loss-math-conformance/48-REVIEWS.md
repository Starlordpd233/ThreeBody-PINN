---
phase: 48
reviewers: [claude-max, codex1, codex, claude-alt, claude]
rerun_reviewers: [claude-max, codex1, codex, claude-alt, claude]
reviewed_at: 2026-08-02T03:18:16Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260802T031130Z-34741
---

# Cross-AI Plan Review — Phase 48

## claude-max Review

I have verified the load-bearing premises directly against the code and confirmed one edge case (all five loss terms are computed unconditionally, so the Stage-0 `lambda_e=0` case cannot falsely mark steps incomplete). Here is the review.

---

# Phase 48 Plan Review — Loss-Math Conformance

## 1. Summary
Four plans repair the Stage-0 trainer's loss math against locked contracts: `Rbar` `/9`→`/3` at the controller seam plus an `L_data` provenance lock (48-01), Stage-0 `lambda_e_max`→0 in the default and both shipped YAMLs (48-02), a dtype-derived causal-exponent underflow clip bound into strict run metadata (48-03), and per-term raw/applied gradient observability (48-04). I confirmed against the tree that every premise holds: `causal_physics_loss` already exposes `dtype`/`device`/`return_details` with a `w_n` detail (so the MPS probe's API contract matches), `data_huber_loss` returns `.mean()`, `LossConfig.lambda_e_max=1.0`, both YAMLs ship `1.0`, and `_non_data_terms` currently uses `(residual**2).mean(dim=(-2,-1))`. The plans are unusually rigorous — a full GOAL/REQ/RESEARCH/CONTEXT coverage audit, per-plan STRIDE, and a no-silent-drop specless-edge ledger. Dependency ordering (waves, D-25 CONF-04→CONF-05) and file ownership are clean and non-overlapping.

## 2. Strengths
- **Assembly-boundary testing philosophy** (48-01/D-07): intercepting the actual `Rbar` argument rather than unit-testing a supplied value directly targets how C-03 escaped the prior suite.
- **Correct scope discipline**: no training, no framework-spec edits, no tuning; config YAML edits are the only production-behavior change and are owner-ratified (D-13). Files stay within `pinn/`, `configs/`, `tests/`.
- **Fail-closed metadata** (48-03): typed/ranged fields, atomic write, and resume refusal on any field mismatch; schema version bumped.
- **Instrumentation safety** (48-04): `autograd.grad` with `allow_unused`, no `.grad` accumulation, and update-equivalence tests vs. an uninstrumented control — I verified all five terms are computed unconditionally, so the completeness contract is sound at Stage-0.
- **Clean dependency graph**: 48-01/48-04 and 48-01/48-03 share files but are serialized by `depends_on`; wave-2 peers 48-03/48-04 are file-disjoint and safely parallel.

## 3. Concerns

**MEDIUM — Causal-clip repair is not verified at the controller assembly boundary.** 48-01 proves the `/3` `Rbar` at the real controller→catalog seam, but the 48-03 clip is verified only via direct `causal_physics_loss` calls and the synthetic MPS probe. No test composes corrected `/3 Rbar` → clip → `w_n>0` through `_non_data_terms`. This is the exact gap (D-07) the phase says it exists to close, applied inconsistently to CONF-05.

**MEDIUM — MPS pytest arm has no stated skip-vs-fail policy.** The dedicated `conda run … pinn-train` probe correctly hard-asserts (target-lock). But `test_causal_clip_mps_float32` lives in `tests/phase48`, and the plan's verification runs `pytest tests/phase48`. Absent a `skipif(not mps)` guard, that test hard-fails the whole Phase-48 suite on any non-MPS machine. It works on this Apple-Silicon host, but the skip/fail contract should be explicit so verification is portable and the intentional hard-fail stays in the locked probe only.

**MEDIUM — Always-on per-term instrumentation cost.** INST-02/D-16 mandate five per-term gradient norms at *every* completed step, i.e. ~5 extra `autograd.grad` backward passes per Adam step and per L-BFGS closure evaluation. Phase 48 runs no training, so the cost is invisible now but is baked into the trainer and lands in the Phase-50 re-run. Worth confirming acceptability / noting in the Phase-50 handoff.

**LOW — Cross-phase test edits (48-03).** Adapting `tests/phase47/test_conf02_s_h_pipeline.py` and `test_conf03_eps_h_wiring.py` to the new required metadata writer signature risks silently weakening their S_H/eps_H assertions; the plan says preserve them (D-22) but this should be explicitly re-asserted post-edit.

**LOW — Metadata schema bump is a one-way door.** Fail-closed resume rejects pre-bump artifacts. Acceptable since no live training artifacts exist before Phase 50, but it is irreversible for any in-flight run.

**LOW — `tests/phase48/__init__.py` ownership race.** 48-01 owns `__init__.py`; 48-02 (same wave) also writes into `tests/phase48/`. Harmless under pytest rootdir import, but 48-02's tests could collect before the package marker exists.

## 4. Suggestions
- Add a controller-seam causal-clip test (synthetic controller producing corrected `/3 Rbar` in the former-underflow regime, assert `0 < w_n ≤ 1` at the real seam) to make CONF-05 coverage symmetric with CONF-04.
- Mark `test_causal_clip_mps_float32` with `skipif(not torch.backends.mps.is_available())`; keep the hard-assert exclusively in the locked conda probe, and state this in 48-VALIDATION.
- In 48-03's Phase-47 fixture edits, add an explicit assertion (or note) that the original S_H/eps_H expected values are unchanged.
- Record the per-step instrumentation cost as a Phase-50 handoff item.

## 5. Overall Risk
**MEDIUM** — driven not by design defects (the plans are well-grounded, correctly scoped, and traceable) but by two verification-integrity items: the causal-clip seam-coverage gap and the unspecified MPS skip/fail policy. Resolving those two before execution would bring residual risk to LOW.

---

## codex1 Review

## 1. Summary

The four plans collectively cover all Phase 48 requirements and should achieve the phase goal. Dependency ordering and scope boundaries are sound. No HIGH-severity blocker was found.

## 2. Strengths

- Correct `CONF-04 → CONF-05` ordering, with completed Phase 47 work treated as a predecessor.
- Strong independent mathematical oracles for `/3` residual reduction, mean Huber loss, and causal clipping.
- Real MPS/torch 2.12.1 verification addresses the known backend-specific underflow.
- Gradient instrumentation includes provenance, failure honesty, graph-release, and optimizer-equivalence checks.
- Training, evaluation, tuning, spec edits, and Phase 49 enforcement remain out of scope.

## 3. Concerns tagged HIGH / MEDIUM / LOW

- **HIGH:** None.

- **MEDIUM:** The planned regression commands do not fully match the validation strategy. Plan 48-01 omits the existing chunked/L-BFGS data-equivalence suite, and Plan 48-04 edits Adam, L-BFGS, clipping, guard, and logging paths without running `tests/phase40/test_optimizer_phase.py`. The full impacted-suite command exists only in the still-draft validation artifact, not as a terminal executable plan step. See [48-01-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/48-loss-math-conformance/48-01-PLAN.md:115>), [48-04-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/48-loss-math-conformance/48-04-PLAN.md:90>), and [48-VALIDATION.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/48-loss-math-conformance/48-VALIDATION.md:50>).

- **MEDIUM:** Plan 48-03 defines a strict, versioned resume contract without pinning the canonical values and encodings for `causal_clip_precision`, `causal_clip_formula`, and `causal_clip_provenance`. Exact matching makes these choices durable compatibility semantics, so leaving them to executor interpretation risks inconsistent artifacts or unnecessary resume refusal. See [48-03-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/48-loss-math-conformance/48-03-PLAN.md:117>).

- **LOW:** Plan 48-04 says a completely disconnected scalar term is a legitimate zero norm, but its named coverage tests only unused parameters. `allow_unused=True` does not by itself handle an output tensor with `requires_grad=False`; that case should have an explicit behavior and test. See [48-04-PLAN.md](<<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/48-loss-math-conformance/48-04-PLAN.md:89>).

## 4. Suggestions

- Make the post-Wave-2 full impacted suite an explicit execution-owned gate, including Phases 38, 40, 41, 42, 46, 47, and 48 plus `git diff --check`.
- Add `tests/phase40/test_optimizer_phase.py` to Plan 48-04 verification and retain its chunked-data equivalence case in CONF-07 validation.
- Specify exact metadata field types and literal identifier values in Plan 48-03.
- Add a test for a term tensor disconnected from every trainable parameter.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**MEDIUM** — the mathematical design is strong, but invasive optimizer instrumentation and strict metadata compatibility require tighter executable validation and schema specification.

---

## codex Review

## Summary

The Phase 48 plans are coherent and appear capable of achieving the phase goal: loss math conformance for `Rbar`, causal clipping, Stage-0 `lambda_E`, `L_data`, gradient observability, and associated test correction. I found no unreadable required files.

## Strengths

- Clear requirement coverage for CONF-04..07, INST-02, TEST-01, and TEST-02.
- Good dependency ordering for the critical `Rbar` before causal-clip sequence.
- Strong scope control: no training run, held-out evaluation, spec edits, recipe tuning, or trainex-r2 sourcing.
- Tests are aimed at assembly/runtime seams rather than only component-local behavior.
- The MPS float32 underflow risk is explicitly recognized and given a target-backend probe.

## Concerns tagged HIGH / MEDIUM / LOW

- **HIGH:** None found.

- **MEDIUM:** CONF-05 depends on a standalone locked-environment MPS probe outside the main pytest suite. The plans include it, but because `.venv` uses torch 2.12.0 while the target lock is torch 2.12.1, execution could look green if only pytest commands are run.

- **MEDIUM:** Plan 48-04’s gradient telemetry is graph-sensitive. It covers unused parameters, non-finite stats, update equivalence, and validation overwrite, but should explicitly test a present scalar term with no parameter-connected grad path / `requires_grad=False`, since `allow_unused=True` does not by itself make such outputs safe.

- **LOW:** Plan 48-02’s targeted verification focuses on config/YAML tests, but `tests/phase41/test_train_entrypoint.py` still contains temporary Stage-0 `lambda_e_max=1.0` fixtures. If those are intentionally allowed until Phase 49 table enforcement, the plan should say so; otherwise they are a possible stale divergence.

- **LOW:** `48-03-PLAN.md` references `48-VALIDATION.md`, but that validation file is still marked `status: draft` and `nyquist_compliant: false`. This is not a plan blocker, but it weakens handoff clarity.

## Suggestions

- Make the locked MPS probe a named non-waivable phase gate, separate from ordinary pytest success.
- Add one explicit gradient-observability acceptance check for a disconnected/no-grad term.
- Document whether temporary explicit Stage-0 nonzero energy caps in entrypoint tests are permitted pre-Phase 49.
- Promote or update `48-VALIDATION.md` before execution if it is intended to be an active executor input.

## Overall Risk (LOW/MEDIUM/HIGH)

**MEDIUM.** The plans are well-scoped and mostly complete, but Phase 48 touches backend-specific numeric behavior and live autograd/optimizer semantics, so execution discipline and the added edge tests matter.

---

## claude-alt Review

I have enough to write the review. My spot-checks resolved several potential concerns (the `causal_physics_loss` signature already accepts `dtype`/`device`/`return_details`; all `write/load_training_metadata` callers are enumerated in 48-03; wave-2 plans have no file overlap) and surfaced one real gap.

---

# Cross-AI Plan Review — Phase 48: Loss-Math Conformance

## 1. Summary

Phase 48 makes the Stage-0 trainer's loss math conform to locked framework contracts across four executable plans: correct `R̄` to `(1/3)Σ‖fᵢ‖²` (48-01), restore Stage-0 `λ_E^max = 0` (48-02), add a dtype-derived causal-exponent underflow clip with strict run-metadata provenance (48-03), and add per-term raw/applied gradient observability (48-04). The plans are unusually rigorous: goal-backward coverage audit, assembly-boundary interception tests (not component-only), a specless-edge ledger, and disciplined scope locks (no training, no spec edits, no tuning, no trainex-r2). Dependency/wave structure is sound — wave 1 = {48-01, 48-02}, wave 2 = {48-03, 48-04}, both wave-2 plans depend on 48-01 and touch disjoint files. The plans achieve the phase goal; my concerns are about verification scope and execution preconditions, not the core design.

All listed files were read. I additionally read `48-CONTEXT.md`, `REQUIREMENTS.md`, and spot-checked `loss_catalog.py`, `controllers.py`, `config.py`, `run_metadata.py`, the shipped configs, and the existing test layout to verify concerns.

## 2. Strengths

- **Assembly-boundary discipline.** TEST-02 is interpreted correctly: 48-01 intercepts the actual `R̄` passed from `_non_data_terms` into `causal_physics_loss` with a residual whose `/3` and `/9` values differ — exactly the seam where the divergence escaped the component-only suite (D-07). This is the right test, not a copied-reduction unit test.
- **Correct minimal-change reasoning.** 48-01 preserves `data_huber_loss`'s already-conformant `.mean()` and only adds provenance + an independent two-branch oracle (D-01/D-03), rather than forcing a cosmetic ×9. Governance-clean: the spec-wording ambiguity is routed to VER-20/Phase 52, not invented (D-04).
- **Clean file ownership.** Wave-2 plans (48-03 loss_catalog/train/run_metadata vs 48-04 controllers/step_log) do not overlap; the two co-editors of `controllers.py` (48-01, 48-04) and `loss_catalog.py` (48-01, 48-03) are strictly sequential via `depends_on: [48-01]`. All `write/load_training_metadata` callers (`train.py`, two phase-47 test files) are enumerated in 48-03's `files_modified` — no orphaned caller when the writer signature becomes required.
- **Honest telemetry semantics (48-04).** The plan carefully distinguishes legitimate zero (kept numeric) from missing/non-finite (null, `grad_stats_complete=false`, `step_completed=false`), handles unused/disconnected params, proves `.grad` isolation and Adam/L-BFGS update-equivalence, and correctly labels L-BFGS `last_closure_evaluation` provenance. `applied = λ·raw` is mathematically exact for a nonnegative scalar λ.
- **Fail-closed metadata.** 48-03 reuses the established strict/atomic metadata lifecycle, bumps the schema version, and flags the costly-reversibility consequence explicitly rather than silently loosening loading.

## 3. Concerns

**HIGH — The heavily-modified `controllers.py` regression suites are in no plan's verification gate.**
48-01 changes `_non_data_terms` (a seam feeding Adam, validation, and the L-BFGS non-data path) and 48-04 rewires the same controller, yet **no plan's `<verify>` runs `tests/phase40/test_controllers.py` or `tests/phase41/test_controllers_ext.py`**, both of which exercise that seam. 48-01's verify covers only phase48+phase38+phase47; the phase-level final verify (48-04) runs only `tests/phase48` + phase42. If any controller test asserts a phys/term magnitude sensitive to the `/9→/3` (3×) change, it breaks silently until a manual full-suite run. This is precisely the class of regression the phase's own philosophy targets. *Recommendation:* add `tests/phase40 tests/phase41` (or at least the two controller modules) to 48-01's and the phase-close verification.

**MEDIUM — 48-03 Task 2 has a hard hardware/env precondition under `autonomous: true`.**
The CONF-05 acceptance check requires a real MPS device and `conda run -n pinn-train` with `torch==2.12.1` (asserted, not skipped). An autonomous executor on a non-MPS host, or one where the `pinn-train` env/torch pin is absent, hard-fails Task 2 with no graceful degradation. The plan states the precondition but does not verify it before the run. *Recommendation:* add an explicit env/hardware preflight (env exists, MPS built+available, torch pin) as an early check so the failure mode is a clear preflight message, not a mid-execution assertion.

**MEDIUM — 48-04 is the sharpest execution risk and its estimate may understate it.**
Computing five per-term norms via `torch.autograd.grad(..., retain_graph=True, allow_unused=True)` over a shared network graph *before* the real total backward, without polluting `.grad`, plus the L-BFGS closure-local capture (accumulated data-grad before non-data backward, four live non-data norms, detached overwrite per closure) is intricate and MPS-nondeterminism-prone. The mitigating update-equivalence/`.grad`-isolation tests are the right defense, but the `low` confidence / 42k-token estimate belies genuine correctness risk. Also note the **always-on ~6× backward overhead per completed step** — harmless in Phase 48 (no training) but a real cost for the Phase 50 re-run; worth surfacing now since D-19's "least expensive graph-safe" latitude and the "no new config knob" lock leave no cadence control.

**LOW — Wave-1 packaging/dependency-declaration gap.**
48-02 writes `tests/phase48/test_stage0_energy_config.py` but the package marker `tests/phase48/__init__.py` is owned by 48-01; 48-02 declares `depends_on: []` and shares wave 1. Every sibling `tests/phaseNN/` uses an `__init__.py` package layout, so 48-02's isolated verify (before 48-01 lands the marker) runs against a non-package dir. Unique basenames make a hard collection failure unlikely under pytest prepend-mode, but the ordering is undeclared. *Recommendation:* give 48-02 `depends_on: [48-01]`, or have 48-02 own the `__init__.py`.

**LOW — Default flip may have un-enumerated consumers.**
48-02 changes `LossConfig.lambda_e_max` `1.0→0.0`. The plan enumerates phase40/41 fixtures, but a repo-wide grep for any test asserting the `1.0` default (or configs relying on it) should be a belt-and-suspenders step before the change, since a divergent-but-unlisted expectation would fail CI outside the plan's scope.

**LOW — Schema bump invalidates resume of pre-Phase-48 metadata.**
48-03's required new fields + version bump make any existing `training_metadata.json` fail closed on resume. Acceptable given no in-flight runs and Phase 50 regenerates fresh, but the plan should confirm no retained-run resume path depends on the old schema.

## 4. Suggestions

- Add `tests/phase40/test_controllers.py` and `tests/phase41/test_controllers_ext.py` (ideally the whole phase40/41 suites) to 48-01's verify and to the phase-close gate — the strongest single improvement.
- Add a fast env/hardware preflight to 48-03 Task 2 so a missing MPS/`pinn-train`/torch-pin surfaces as a clear preflight failure.
- Declare `48-02 depends_on: [48-01]` (or move `__init__.py` ownership) to remove the wave-1 package-marker race.
- Add an explicit **integration** verify note for wave 2: after merging 48-03 (causal clip) and 48-04 (phys-term telemetry), rerun the full `tests/phase48` so 48-04's phys hand-oracle is confirmed against the clipped `causal_physics_loss` (no-op above the bound, so it should hold — confirm, don't assume).
- Consider a one-line grep gate in 48-02 for stray `lambda_e_max` `1.0` expectations.

## 5. Overall Risk

**MEDIUM (low-medium).** The mathematical decisions are correctly grounded in owner rulings (D-01, D-05, D-08, D-13) and scope-locked; dependency/wave structure and file ownership are clean; no destructive or data-integrity risks (no git history ops, no training runs, fail-closed metadata). The residual risk is concentrated in (a) a regression-coverage hole on the core `controllers.py` module and (b) 48-04's instrumentation complexity plus 48-03's environment preconditions under autonomous execution — all addressable with verify-scope and preflight additions rather than redesign.

---

## claude Review

I have enough to write the review. All my candidate HIGH concerns dissolved on verification (`.venv` has torch, `controllers.py` doesn't call the metadata writer, the MPS probe API matches the real signature, and `rbar=[1000,1000]` with `eta_c=1` genuinely underflows pre-fix). Here is the review.

---

# Phase 48 (Loss-Math Conformance) — Cross-AI Plan Review

## 1. Summary

Four wave-ordered plans repair the Stage-0 trainer's loss math against the locked framework contracts: `Rbar` `(1/9)Σ → (1/3)Σ` (48-01/CONF-04), a dtype-derived causal-exponent underflow clip with strict run-metadata provenance (48-03/CONF-05), `λ_E^max = 0` at Stage-0 (48-02/CONF-06), `L_data` mean-Huber provenance-only lock (48-01/CONF-07), per-term gradient observability (48-04/INST-02), plus divergence-test correction (TEST-01) and assembly-boundary proofs (TEST-02). Wave 1 = {48-01, 48-02}; Wave 2 = {48-03, 48-04}, both gated on 48-01. All 7 phase requirements map cleanly; the CONF-04→CONF-05 ordering (D-25) is enforced via `depends_on`.

I spot-checked the load-bearing claims against the code and they hold: the current reduction really is `.mean(dim=(-2,-1))` (/9) at `controllers.py:542`; `causal_physics_loss(residuals_per_time, *, eta_c=1, …, dtype, device, return_details)` matches the hardcoded MPS probe and returns `{"w_n","rbar"}`; `write_training_metadata`/`load_training_metadata` have exactly one production caller (`train.py`) plus the two Phase-47 tests the plan enumerates — `controllers.py`'s only `training_metadata` reference is a docstring; and `.venv` has torch 2.12.0, so the `pytest` verify commands are valid.

These plans are unusually rigorous (assembly-boundary interception, fail-closed schema, update-equivalence tests, an explicit no-silent-drop coverage ledger). Residual risk is execution-surface size, not plan defects.

## 2. Strengths

- **Correct seam targeting.** CONF-04 is fixed at the single assembly point (`_non_data_terms`) and *proven by intercepting the argument* to `causal_physics_loss`, not by a component unit test — directly closing the C-03 escape route (D-07).
- **No double-correction.** The plan cleanly separates the `Rbar` 3× fix (CONF-04) from the `L_data` `/(9·N_t)` that is *preserved* (CONF-07), and explicitly forbids a cosmetic "×9 to make code move" (D-03). This is the subtle trap and they avoid it.
- **Genuine regression witnesses.** `rbar=[1000,1000]` with `eta_c=1` gives `exp(-1000)` → exact 0 in float32 pre-fix, strictly positive post-clip — a real underflow witness, not a no-op.
- **Scope discipline.** Every plan carries a prohibition ledger tying D-24/SCOPE-27..32 to concrete backstops; framework specs stay in read-only context; no tuning/reweighting surface is introduced.
- **Verified coverage of the metadata blast radius** — the schema change is confined to the files the plan lists.

## 3. Concerns

**MEDIUM — `step_completed` is overloaded with telemetry completeness (48-04, D-20).** Making a "normally completed" step require all ten finite gradient stats means an optimizer step that *did* update parameters but produced one non-finite diagnostic norm is emitted as `step_completed == false`. This is owner-grounded (D-18/D-20), but the plan should confirm no downstream consumer (step counting, resume/checkpoint cadence, gate-metric eligibility, early-stop) reads `step_completed` as "optimizer did not advance." The coupling is intended for *instrumentation completeness*, not *training progress*, and nothing in the plan verifies the two readings don't collide.

**MEDIUM — MPS "precision" proof lives only in a non-pytest conda one-liner.** CONF-05's precision backstop is the `conda run -n pinn-train … torch 2.12.1` probe, not the pytest suite. The phase-wide aggregate verification (`pytest tests/phase48`) can go fully green *without ever exercising real MPS*. A re-verifier who runs only the suite would believe CONF-05 precision is proven when the target-backend arm never ran. Recommend the phase's closing verification explicitly names the conda probe as a required, separately-recorded gate (it is buried in 48-03 Task 2's `<verify>` only).

**MEDIUM — irreversible metadata schema migration.** Bumping `TRAINING_METADATA_SCHEMA_VERSION 1→2` with exact-key (`keys != set(_METADATA_KEYS)`) fail-closed reload orphans any existing v1 `training_metadata.json`; a resume of any pre-Phase-48 run hard-fails. The plan acknowledges this (`reversibility: costly`) and it is acceptable within the milestone (Phases 50–51 regenerate fresh), but the executor should confirm no in-flight/checkpointed run artifact is silently invalidated, and that the failure message points at "regenerate," not a bare KeyError.

**LOW — 48-03 refines D-08 beyond its literal formula.** D-08 states `clamp_min(x_n, log(finfo.tiny))`; the plan adds a single `nextafter`-toward-+∞ nudge when the representable floor rounds below the mathematical target. This is defensible (guarantees `exp(floor) ≥ tiny`, i.e. a normal number on MPS float32) and within implementer delegation, but it is a deviation from the written bound — the verifier should confirm it never lets `w_n` exceed the D-08 bound and that the recorded `causal_clip_exponent_floor` provenance matches what's actually applied.

**LOW — in-suite MPS test behavior on non-Apple runners.** `test_causal_clip_mps_float32` runs under `.venv` pytest. The plan wants an "explicit availability requirement" (not a silent skip). On a non-MPS machine this either spuriously fails the suite or must skip; the repo's existing idiom is `unittest.SkipTest`. Make the skip-vs-fail choice deliberate so it neither hides a real gap nor breaks CI on a non-Apple box.

**LOW — 48-04 execution surface vs. task granularity.** 48-04 (42k tokens, 2 tasks) is the most delicate change: `autograd.grad` without `.grad` accumulation, graph-retention scoping, L-BFGS last-closure attribution, and Adam+L-BFGS update-equivalence proofs — any of which can subtly mutate optimizer state. The 2-task decomposition is coarse for that risk. Consider whether the L-BFGS closure-instrumentation warrants its own finer split.

## 4. Suggestions

- Add an explicit assertion/note in 48-04 that a consumer audit of `step_completed` was performed (or add a test that an optimizer-advanced-but-telemetry-incomplete step is still counted as a real step wherever step counts matter).
- Promote the conda MPS probe into the phase's closing `<verification>` block (48-04 / phase gate), or record its output as a required artifact, so CONF-05 precision cannot be declared on a suite that never touched MPS.
- Ensure the v1→v2 metadata reload failure path emits a "regenerate/migrate" message; add one refusal test asserting the operator-facing text, not just that it raises.
- Confirm `smoke.yaml` and `stage0-example.yaml` are the *only* shipped Stage-0 configs carrying `lambda_e_max` (D-13 says "every shipped Stage-0/smoke config") — a third stage-0 config with `1.0` would be silently missed.
- Verify the `read_first` artifacts `48-VALIDATION.md` and `48-01-SUMMARY.md` referenced by 48-03 exist at execution time (48-01-SUMMARY is produced upstream in Wave 1; 48-VALIDATION's origin is unclear).

## 5. Overall Risk: **MEDIUM**

The planning quality is high — requirement coverage is complete, dependency ordering honors D-25, there are no intra-wave file-write conflicts, and every claim I checked against the code was accurate. The MEDIUM rating is driven by *execution surface and verification discoverability*, not plan gaps: the 48-04 autograd instrumentation is easy to get subtly wrong, the metadata migration is effectively one-way, and the CONF-05 target-backend proof can be skipped without the suite noticing. None of these is a correctness defect in the plans themselves; all are addressable with the checks above before/during execution.

---

## Consensus Summary

Five reviewers (claude-max, codex1, codex, claude-alt, claude) converge on **MEDIUM** overall risk. Four of five found zero HIGH findings (claude-alt's single HIGH is F1 below); all five affirmed plan structure — requirement coverage, D-25 ordering, file ownership, owner-decision grounding — so remediation is additive verification-scope, precondition, and pinning deltas applied in place.

| # | Finding | Reviewers | Severity | Disposition |
|---|---|---|---|---|
| F1 | Impacted regression suites (`tests/phase40/test_controllers.py`, `tests/phase41/test_controllers_ext.py`, `tests/phase40/test_optimizer_phase.py`) and the full impacted-suite command are in no plan's executable verify gate — only in draft `48-VALIDATION.md` | claude-alt (HIGH), codex1 (MED) | HIGH | A1–A3, C1, C5, D4 |
| F2 | CONF-05 MPS arm integrity: no in-suite skip policy, no env preflight, conda probe not a named phase-close gate; suite can go green without touching MPS | claude-max, codex, claude-alt, claude (MED ×4) | MED | B1, B2, B5, A4, C5, D3 |
| F3 | `tests/phase48/__init__.py` wave-1 ownership race (48-01 owns marker; 48-02 writes into the package with `depends_on: []`) | claude-max, claude-alt (LOW) | LOW | A5 (R2) |
| F4 | Disconnected / `requires_grad=False` term telemetry: `allow_unused=True` does not cover graphless outputs; `autograd.grad` raises | codex1, codex (MED/LOW) | MED | C2, C3, C6 (R3) |
| F5 | Always-on per-step instrumentation cost (~5 extra backward passes) lands in Phase 50 with no cadence knob (D-16 lock) | claude-max, claude-alt, claude | MED | C7 (R4 — recorded; no knob) |
| F6 | Stray `lambda_e_max` nonzero expectations; Phase-41 entrypoint fixtures need a documented pre-Phase-49 allowance | codex, claude-alt, claude (LOW) | LOW | A6, A7 |
| F7 | Metadata string literals (`causal_clip_precision`/`causal_clip_formula`/`causal_clip_provenance`) unpinned; exact-match resume makes them durable semantics | codex1 (MED) | MED | B3, B6 (R1) |
| F8 | CONF-05 lacks the D-07 assembly-boundary proof CONF-04 has (no /3-Rbar→clip→w_n seam test) | claude-max (MED) | MED | B2, B5, B6 |
| F9 | v1→v2 metadata refusal should emit operator "regenerate" guidance, tested by message content | claude (MED) | LOW | B4, B5, B6 |
| F10 | `step_completed` overloads telemetry completeness; consumers must be audited | claude (MED) | MED | C4, C7 |

Ratifications approved with the remediation plan: **R1** pinned metadata literals (F7); **R2** 48-02 moves to wave 2 with `depends_on: [48-01]`, waves W1={48-01} / W2={48-02, 48-03, 48-04} (F3); **R3** a present term tensor with no autograd graph records exact numeric 0.0 raw/applied norms without calling `autograd.grad`, distinct from missing/non-finite telemetry (F4); **R4** instrumentation cost recorded as a Phase-50 handoff item with the D-16 every-completed-step cadence and no-config-knob locks standing (F5).

Accepted without plan change: the metadata schema bump is one-way (no pre-Phase-48 artifacts exist; Phase 50 regenerates); the D-08 `nextafter` refinement stays within implementer delegation (the provenance fields record the applied floor).

Remediation applied in place on 2026-08-01 per docs/work/plans/milestone_v2.2/48-loss-math-conformance/2026-08-01-phase48-plan-revision.md; no planner regeneration.

## xreview Diagnostics

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=302
- timeout_seconds=1200
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=5418
- stderr_bytes=0

### codex1
- reviewer=codex1
- exit_code=0
- elapsed_seconds=406
- timeout_seconds=1200
- watchdog=not_triggered
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3257
- stderr_bytes=348903

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=229
- timeout_seconds=1200
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=2615
- stderr_bytes=433773

### claude-alt
- reviewer=claude-alt
- exit_code=0
- elapsed_seconds=339
- timeout_seconds=1200
- watchdog=not_triggered
- command=ccp alt --model claude-opus-4-8 -p - 
- stdout_bytes=8503
- stderr_bytes=0

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=273
- timeout_seconds=1200
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p -
- stdout_bytes=7896
- stderr_bytes=0

## Verification coverage

Source-grounding authority: `grep` (confirmed via `gsd-tools drift-guard authority --raw`).
Cycle 1, fresh review. Symbols enumerated from citations in 48-01..48-04-PLAN.md.
Artifacts PRODUCED by Phase 48 (new code/tests/fields introduced this phase) are excluded
from grounding per the task contract; only references to EXISTING code/spec were resolved.

**Counts by verdict**

| Verdict | Count |
|---|---|
| VERIFIED | 64 (44 code identifiers + 20 file paths) |
| MISSING | 0 |
| AMBIGUOUS | 0 |
| UNCHECKABLE | 56 |

`hardBlock = false` (no MISSING/AMBIGUOUS; `drift-guard severity` not triggered).

VERIFIED sample (declaration locations): `RunController._non_data_terms`
(pinn/training/controllers.py:519), `_compose_loss_terms` (:599), `_log_step` (:690),
`_make_lbfgs_closure` (:1014), `_run_adam_phase` (:869), `_run_lbfgs_phase` (:1045),
`causal_physics_loss` (pinn/loss_catalog.py:223), `data_huber_loss` (:188), `_huber` (:120),
`LossConfig` + `lambda_e_max: float = 1.0` (pinn/training/config.py:505/508) +
`__post_init__` (:510), `ScheduledWeights` (pinn/training/scheduled_weights.py:65),
`load_config` (pinn/training/config_yaml.py:186), `RuntimeSpec` (pinn/runtime.py:24),
`_resolve_runtime_spec` (pinn/train.py:591), `_assert_s_h_matches_artifact` (:445),
`TRAINING_METADATA_SCHEMA_VERSION = 1` (pinn/training/run_metadata.py:49), `_METADATA_KEYS`
(:51), `write_training_metadata` (:136), `load_training_metadata` (:168),
`STEP_LOG_FIELDS` (pinn/training/step_log.py:33), `step_log_fields_provisional_entry`
(:220), `_sanitize_step_record` (:240), `JsonlStepHandler.emit` (:305), `grad_norm`
registry key (:151); regression tests `test_eps_h_assembly_value`,
`test_resume_binds_s_h_for_controller`, `test_causal_physics_weights_and_sorted_time`,
`test_metadata_roundtrip_revalidates`, `test_resume_recompute_refuses_mismatch`,
`test_lambda_e_max_gt_one_raises`, `test_lambda_e_le_one_across_schedule_for_each_stage_table`,
`test_lambda_e_max_cap_enforced_at_construction`, `test_keyed_yaml_resolves_field_for_field`,
`_canonical_step_record`, `test_ops03_happy_path_field_presence`,
`test_ops03_registry_parity_and_no_residuals_leak`, `test_e1_nonfinite_whole_file_parseability`;
all 20 cited file paths present (incl. both shipped configs that currently emit
`lambda_e_max: 1.0`, confirming the 48-02 premise).

**UNCHECKABLE symbols (not grep-verifiable code declarations)**

| Category | Representative items | Reason |
|---|---|---|
| Math/spec notation (rule 3) | R̄/Rbar, Rbar_t, L_data, λ_E, ε_H/eps_H, η_c, f_i, w_n, w_1, S_H (~10) | Spec quantities, not code symbols; not grepped per source-grounding rule 3. |
| CONTEXT decision labels | D-01 .. D-25 (25) | Documentation references into 48-CONTEXT.md, not code declarations. |
| Requirement labels | CONF-04..07, INST-02, TEST-01/02 (7) | REQUIREMENTS.md requirement IDs, not code symbols. |
| Scope labels | SCOPE-27..31 (5) | REQUIREMENTS.md scope IDs (28 cited via "27/28" shorthand), not code. |
| Gap-register ref | GAP-45-04 (1) | 45-GAPS.md entry ID cited in 48-03 context; documentation, not code. |
| External library APIs | torch.finfo(dtype).tiny, torch.nextafter, torch.autograd.grad, torch.backends.mps.*, torch.mps.synchronize (5) | PyTorch APIs, not repo code. |
| Data artifact | training_metadata.json (1) | Runtime data file consumed/produced, not a code declaration. |
| Runtime return-dict keys | "w_n", "rbar" (2) | Return-detail string keys of causal_physics_loss; carrier function VERIFIED, keys are not declarations. |

Plan-internal threat-register IDs T-48-01..14 are authored this phase (not citations of
existing code) and are excluded from grounding. No repo CLI flags or decorators are cited.

---
phase: 55-architecture-characterization-probe
verified: 2026-09-06T04:15:32Z
status: passed
score: 12/12 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/55-architecture-characterization-probe/55-01-PLAN.md
  - .planning/phases/55-architecture-characterization-probe/55-01-SUMMARY.md
  - .planning/phases/55-architecture-characterization-probe/55-02-PLAN.md
  - .planning/phases/55-architecture-characterization-probe/55-02-SUMMARY.md
  - .planning/phases/55-architecture-characterization-probe/55-03-PLAN.md
  - .planning/phases/55-architecture-characterization-probe/55-03-SUMMARY.md
  - .planning/phases/55-architecture-characterization-probe/55-04-PLAN.md
  - .planning/phases/55-architecture-characterization-probe/55-04-SUMMARY.md
  - .planning/phases/55-architecture-characterization-probe/55-CONTEXT.md
  - .planning/phases/55-architecture-characterization-probe/55-VALIDATION.md
  - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json
  - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md
  - pinn/verification/architecture_characterization_probe.py
  - tests/phase38/test_prohibitions.py
  - tests/phase55/__init__.py
  - tests/phase55/fixtures/six_case_baseline.json
  - tests/phase55/test_architecture_characterization.py
covered_digest: "v1:sha256:e66103cba669fb45d04bf9e9c1262bf777116e915a3bc2fe3464d62762d61dd4"
behavior_unverified: 0
overrides_applied: 0
decision_coverage:
  honored: 3
  total: 3
  not_honored: []
---

# Phase 55: Architecture Characterization Probe Verification Report

**Phase Goal:** The measurement v2.3's central premise rests on stops being ad-hoc and becomes committed, tested tooling that anyone can re-run against any candidate recipe.
**Verified:** 2026-09-06T04:15:32Z
**Status:** passed
**Re-verification:** No — initial verification
**Working tree:** `<home>/Desktop/3_body_problem/.worktrees/trainex` on `milestone/v2.3` at `2a34cc20`

## Goal Achievement

INST-04 is a committed, importable, tested probe under `pinn/verification/`. It reports the seven architecture-only quantities at initialization (no data file, no optimizer, no training step) over a configurable seed/IC sweep, and it reproduces the 2026-08-17 audit six-row table at the documented decade resolution. D-03 helpers exist and are unit-tested, but they were not used to produce `R_ref` or GATE-04 evidence in this phase.

### Observable Truths

Must-haves are the four ROADMAP success criteria plus PLAN-only additions that do not restate those criteria. SUMMARY.md claims were not used as evidence.

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | ROADMAP SC1: `pinn/verification/` contains committed, tested tooling that, given an `ArchitectureSpec` at initialization and **no data, no optimizer, and no training step**, reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep (INST-04). | ✓ VERIFIED | Tracked module `pinn/verification/architecture_characterization_probe.py` (883 lines). `measure_case` builds `ArchitectureSpec(seed=case.seed)` via `build_network`, `model.eval()`, synthetic IC13, `CollocationSampler`, then trainer primitives. No `Optimizer`/`DataLoader`/`torch.optim` tokens; `.backward(` appears only in the module docstring prohibition. `DEFAULT_CASES` is the six audited rows; `run_sweep(cases=...)` and `--cases-config` accept an arbitrary list. `test_tracer_single_case_reports_all_seven_quantities` plus CLI config tests passed. |
| 2 | ROADMAP SC2: Run under the pre-amendment recipe, the probe **reproduces the 2026-08-17 residual-frame conformance audit's six-row table** across the same six seed/IC combinations — `R̄ ≈ 10¹⁰` and `front_idx = 0` in every row — and the reproduction is recorded re-derivably (command, tree state, full output) per the GAP-44-02 discipline. | ✓ VERIFIED | `test_invariant_bounds_six_cases` asserts `front_idx == 0` and `1e9 < rbar_median < 1e11` for all six labels. Committed run `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/` is the only evidence directory; `raw.json` has `argv: []`, `command: python -m pinn.verification.architecture_characterization_probe`, `git_sha`, dirty flag, Torch/NumPy versions, and six full case records. Independent audit-table comparison (below) holds at decade resolution. |
| 3 | ROADMAP SC3: The probe derives `R̄` and the causal weights from the same implementation the trainer uses, so a probe result is evidence about the shipped recipe rather than about a parallel re-implementation of it. | ✓ VERIFIED | Direct calls: `componentwise_du`, `softened_acceleration`, `causal_physics_loss(..., return_details=True)` for `w_n`. `R̄` is the locked CONF-04/D-05 composition `(a' - F_grav)^2` summed over bodies/components `/ 3.0`, then passed into the trainer causal loss. `test_derives_from_trainer_implementation` mutates those three imports on the probe module and observes lock-step movement of weights, `F_grav`, and derivative norms. |
| 4 | ROADMAP SC4: A test suite fails if any reported quantity, the sweep configuration, or the six-row reproduction regresses. | ✓ VERIFIED | Tier-1 invariant bounds (`tests/phase55/`, parametrized over six labels). Tier-2 `test_exact_value_fixture` compares every numeric/string field at fixture `relative_tolerance=1e-9`. `test_fixture_comparison_fails_on_a_perturbed_baseline` and session-scoped sha256 autouse prove the net cannot heal itself. `test_default_cases_are_the_six_audited_rows` pins the sweep configuration. `.venv/bin/python -m pytest tests/phase55/ -q --tb=short` → **46 passed in 7.81s**. |
| 5 | BOUNDARY EDGE: causal-weight clamp floor and `front_idx` threshold are pinned at the boundary and one step either side. | ✓ VERIFIED | Live six-case: `causal_weights[0] == 1.0`; `w[1:]` equal `resolve_causal_clip_facts(float64, cpu)['causal_clip_min_weight']` (never a literal). `_front_idx([0.5+ulp, 0.5, 0.5]) == 0`; all-`<=0.5` yields `-1`. Tests: `test_causal_weights_pinned_at_dtype_clamp_floor`, `test_front_idx_threshold_is_strictly_above_half`, `test_front_idx_sentinel_when_no_weight_exceeds_half`. |
| 6 | PRECISION EDGE: even-`n_col=16` median is `numpy.median` (mean of the two central order statistics), not `torch.median`; clamp floor is dtype-derived. | ✓ VERIFIED | Module constant `MEDIAN_CONVENTION` and every result field copy it. `test_median_convention_averages_two_central_values` asserts `_median` of a 16-element array with distinct central values equals `15.0`. Float64 floor in evidence is `2.2250738585072626e-308`. |
| 7 | Reported norm convention is arithmetically consistent with the audit: median `R̄` equals `(median ‖a′‖)² / 3` to within 10 percent for every default case. | ✓ VERIFIED | `test_norm_convention_matches_audit_rbar_identity` parametrized over all six labels; relative error `< 0.10`. |
| 8 | D-02 CLI/config: zero-argument invocation runs the six audited cases at float64/CPU; `--cases-config` drives an arbitrary list; malformed entries raise `ValueError` naming the field before any directory is created. | ✓ VERIFIED | `--precision`/`--device` are defaulted (`required=True` absent). `ArchitectureCharacterizationCLITests.test_zero_argument_cli_reproduces_six_rows` and `test_cases_config_drives_arbitrary_case_list` passed. `test_malformed_cases_config_raises_value_error` covers seed/masses/ic13_mode and asserts the evidence root stays empty. |
| 9 | Evidence writer: non-overwriting UTC run dir; `raw.json` provenance allowlist; `atomic_write_text`; `--evidence-root` inside `simulation_data/` rejected before mkdir. | ✓ VERIFIED | `_write_evidence` calls `atomic_write_text` for `raw.json` and `summary.md`. `_provenance` calls `git_head()` and `_git_worktree_dirty()`. Tests: `test_cli_writes_provenance_evidence`, `test_cli_allocates_non_overwriting_run_dirs`, `test_evidence_root_inside_simulation_data_is_rejected`. Top-level keys equal `EVIDENCE_TOP_LEVEL_KEYS`. |
| 10 | Phase-38 exclude-list: the probe is in `_EXCLUDE_SUFFIXES` with a D-02 rationale; the precision/v1.3 glob tests pass; discovery does not list the probe. | ✓ VERIFIED | `tests/phase38/test_prohibitions.py:64-76` documents the defaulted `--precision` seam and re-homes the two non-precision guarantees in `tests/phase55/`. `pytest -k "no_precision_default or no_v1_3_era or discovered_modules"` → 3 passed / 96 subtests. Probe in `_EXCLUDE_SUFFIXES`: True; in `_discover_phase38_modules()`: False. Local re-homes: `test_module_has_no_global_default_mutation_or_device_probe`, `test_module_has_no_v1_3_era_imports`. |
| 11 | D-03: 4096/256/16 helpers exist and are synthetic-tested; default `run_sweep`/`measure_case`/`main` cannot reach them; Phase 55 produced no `R_ref` / GATE-04 evidence. | ✓ VERIFIED | `stratified_collocation_times` / `bin_mean_residuals` / `RATIFIED_*` present. `test_stratified_bins_synthetic` (4096 times, 16×256, bin edges). `test_bin_mean_residuals_synthetic` (closed-form means). AST closure `test_new_structure_helpers_unreachable_from_default_sweep` plus recorder `test_default_sweep_never_exceeds_sixteen_causal_points`. `rg R_ref` / `GATE-04` in the probe and evidence: no matches. Committed `configuration.n_col` is 16. |
| 12 | D-01 tier 2: committed exact-value fixture with regeneration provenance; comparison is read-only; a perturbed copy fails; on-disk sha256 is stable. | ✓ VERIFIED | `tests/phase55/fixtures/six_case_baseline.json` sha256 `65edebc78d334c76e532a15d75bb6ca70ee4a3094f68b66804ad12d4372bc474`. `_meta` names regeneration command, precision/device/`n_col`, Torch 2.12.0, NumPy 2.2.0, median convention, IC13 scheme, `relative_tolerance: 1e-09`. Tests `test_exact_value_fixture`, `test_fixture_comparison_fails_on_a_perturbed_baseline`, `test_fixture_file_is_never_written_by_the_suite` passed. Suite only `json.load`s the fixture; writes in the test file are to tmp config JSON, not the baseline. |

**Score:** 12/12 truths verified (0 present, behavior-unverified)

### Independent audit §6b decade check (SC2)

Source table: `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` §6b. Repro: committed `evidence/probe/20260906T035209Z/summary.md` + `raw.json`. Agreement is decade / order-of-magnitude (original ad-hoc collocation scheme is unrecoverable).

| seed / IC | ‖r′‖ audit / repro | ‖v′‖ | ‖a′‖ | ‖F_grav‖ | min sep | `R̄` | `front_idx` |
|---|---|---|---|---|---|---|---|
| 41, m=(1,1,1), IC13=0 | 1.28 / 1.085 | 310 / 251.8 | 2.03×10⁵ / 1.975×10⁵ | 2.17 / 3.131 | 0.91 / 0.784 | 1.37×10¹⁰ / 1.301×10¹⁰ | 0 / 0 |
| 42 | 1.13 / 1.009 | 331 / 313.5 | 2.72×10⁵ / 2.411×10⁵ | 3.29 / 4.41 | 0.67 / 0.607 | 2.46×10¹⁰ / 1.938×10¹⁰ | 0 / 0 |
| 43 | 0.97 / 0.830 | 251 / 297.9 | 2.20×10⁵ / 2.078×10⁵ | 3.24 / 5.913 | 0.72 / 0.582 | 1.62×10¹⁰ / 1.440×10¹⁰ | 0 / 0 |
| 0 | 0.91 / 0.976 | 281 / 301.8 | 2.79×10⁵ / 2.040×10⁵ | 5.94 / 5.803 | 0.50 / 0.554 | 2.60×10¹⁰ / 1.387×10¹⁰ | 0 / 0 |
| 7 | 0.85 / 1.083 | 290 / 239.4 | 1.94×10⁵ / 2.027×10⁵ | 5.89 / 3.616 | 0.51 / 0.677 | 1.25×10¹⁰ / 1.370×10¹⁰ | 0 / 0 |
| 41, m=(1,0.8,0.6), random tanh IC13 | 0.95 / 1.124 | 231 / 327.4 | 2.28×10⁵ / 1.917×10⁵ | 2.85 / 2.807 | 0.72 / 0.719 | 1.74×10¹⁰ / 1.224×10¹⁰ | 0 / 0 |

All six `front_idx` values are 0. All six median `R̄` values sit in the 10¹⁰ decade (`1.224×10¹⁰` … `1.938×10¹⁰`). Largest audit/repro ratio is ~1.87 (`R̄` seed 0); every column stays inside a factor of 10.

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | ----------- | ------ | ------- |
| `pinn/verification/architecture_characterization_probe.py` | SweepCase, result type, DEFAULT_CASES, measure_case, run_sweep, main, load_cases_config, stratified helpers, evidence writer | ✓ VERIFIED | 883 lines; `__all__` exports the public surface; importable as `pinn.verification.architecture_characterization_probe` |
| `tests/phase55/__init__.py` | Package marker | ✓ VERIFIED | 1-line package marker as planned |
| `tests/phase55/test_architecture_characterization.py` | Tracer, Tier-1, SC3, CLI, D-03, Tier-2 | ✓ VERIFIED | 724 lines; 21 test functions + parametrization + CLI TestCase = 46 collected tests, all passing |
| `tests/phase38/test_prohibitions.py` | `_EXCLUDE_SUFFIXES` entry + rationale | ✓ VERIFIED | Probe listed; rationale comments D-02; glob tests pass |
| `tests/phase55/fixtures/six_case_baseline.json` | Full six-row output + `_meta` | ✓ VERIFIED | 371 lines; `_meta` + six cases; sha256 `65edebc78d334c76e532a15d75bb6ca70ee4a3094f68b66804ad12d4372bc474` |
| `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/` | One committed re-derivable run | ✓ VERIFIED | Exactly one UTC stamp dir; `raw.json` (390 lines) + `summary.md` (23 lines); `failure: null` |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `architecture_characterization_probe.py` | `pinn.loss_catalog.causal_physics_loss` | `causal_physics_loss(rbar, times=..., return_details=True)` | WIRED | Live call in `measure_case`; mutation test |
| `architecture_characterization_probe.py` | `pinn.physics_residual` | `componentwise_du` / `softened_acceleration` | WIRED | Live call in `measure_case`; mutation test |
| `architecture_characterization_probe.py` | `pinn.network.build_network` | `build_network(ArchitectureSpec(seed=...), dtype, device)` | WIRED | Live call in `measure_case` |
| `architecture_characterization_probe.py` | `pinn.training.atomic_io.atomic_write_text` | tmp-write + fsync + replace | WIRED | `_write_evidence` two calls |
| `architecture_characterization_probe.py` | `pinn.verify.git_head` | provenance sha | WIRED | `_provenance` unpacks `(git_sha, git_available)` |
| `tests/phase38/test_prohibitions.py` | probe module | `_EXCLUDE_SUFFIXES` membership | WIRED | Probe excluded from discovery |
| `tests/phase55/test_architecture_characterization.py` | `six_case_baseline.json` | read-only per-field compare | WIRED | `_load_fixture` + `_compare_case_to_fixture` |
| `evidence/probe/20260906T035209Z` | probe CLI | zero-argument module invocation | WIRED | `argv: []`, command string matches `_MODULE_PROG` |
| `architecture_characterization_probe.py` | `54-RULING.md` B2/D3 | `RATIFIED_N_BINS/PER_BIN/TOTAL` | WIRED | Constants 16 / 256 / 4096; helpers unreachable from default path |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `measure_case` | `r'`, `v'`, `a'` | `build_network` forward + `componentwise_du` on live `u_leaf` | Yes | ✓ FLOWING |
| `measure_case` | `F_grav` | `softened_acceleration(positions, masses)` | Yes | ✓ FLOWING |
| `measure_case` | `R̄`, `w_n`, `front_idx` | locked residual energy → `causal_physics_loss` details → trainer `w > 0.5` formula | Yes | ✓ FLOWING |
| `raw.json` | `cases[]` | `asdict(ArchitectureCharacterizationResult)` from `run_sweep` | Yes | ✓ FLOWING |
| `six_case_baseline.json` | `cases[]` | previously captured `run_sweep()` output (regression pin) | Yes (regression, not oracle) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Phase 55 suite | `.venv/bin/python -m pytest tests/phase55/ -q --tb=short` | `46 passed in 7.81s` | ✓ PASS |
| Public API importable | `.venv/bin/python -c` import + `DEFAULT_CASES` labels | labels `['41','42','43','0','7','41-variable-mass']`; all listed exports present | ✓ PASS |
| Phase-38 exclude glob | `pytest tests/phase38/test_prohibitions.py -k "no_precision_default or no_v1_3_era or discovered_modules"` | `3 passed, 3 deselected, 96 subtests`; probe not discovered | ✓ PASS |
| D-03 leak check | inspect `measure_case`/`run_sweep`/`main` source | no `stratified_collocation_times`, `bin_mean_residuals`, or `R_ref` | ✓ PASS |
| Audit decade match | read audit §6b vs committed `raw.json` | `front_idx=0`, `R̄` in 10¹⁰, all columns within ~2× | ✓ PASS |

### Probe Execution

No `scripts/*/tests/probe-*.sh` is declared for this phase. The deliverable *is* the characterization probe. CLI behavior is exercised by `ArchitectureCharacterizationCLITests` (subprocess `-m pinn.verification.architecture_characterization_probe`). The committed zero-argument run is `evidence/probe/20260906T035209Z/`. The verifier did not re-invoke the default evidence-root CLI, to avoid allocating a second run directory beside the committed one.

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| architecture characterization (test-harness CLI) | pytest CLI TestCase | exit 0, six rows, provenance keys | PASS |
| architecture characterization (committed run) | recorded `python -m pinn.verification.architecture_characterization_probe` | `raw.json` + `summary.md`, `failure: null` | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| INST-04 | 55-01, 55-02, 55-03, 55-04 | Land architecture-only characterization as committed, tested verification tooling under `pinn/verification/`; report the seven quantities at init over a configurable sweep; reproduce the 2026-08-17 six-row table | ✓ SATISFIED | Probe module + tests/phase55 (46 passed) + committed evidence run + independent decade match |
| GATE-04 | (none; mapped to Phase 56) | Train-free acceptance gate | n/a (not this phase) | REQUIREMENTS traceability `GATE-04 → Phase 56`. Probe explicitly does not emit a recipe verdict (`test_cli_exit_code_is_not_a_recipe_verdict`). |

No orphaned Phase 55 requirements. REQUIREMENTS.md still shows `INST-04 | Phase 55 | Pending` and an unchecked INST-04 box; flipping those is an orchestrator closeout act, not this report.

### Prohibitions

All four PLAN prohibitions are `verification: test` and have wired enforcement (not silent/unverified).

| Prohibition | Enforcement | Status |
| --- | --- | --- |
| MUST NOT compute `R̄` / weights / `front_idx` / AD from a parallel reimplementation | `test_derives_from_trainer_implementation` | ✓ held |
| MUST NOT emit a pass/fail recipe verdict | `test_cli_exit_code_is_not_a_recipe_verdict`; `EVIDENCE_TOP_LEVEL_KEYS` has no verdict field; `main` returns 0 iff measurement completed | ✓ held |
| MUST NOT run the real six-case sweep under 4096/16-bin structure as `R_ref` / GATE-04 evidence (D-03) | AST closure + 16-point recorder + no `R_ref` in evidence | ✓ held |
| MUST NOT auto-heal the exact-value fixture | perturbation fail-first + session sha256 autouse; suite never opens the fixture for write | ✓ held |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `pinn/verification/architecture_characterization_probe.py` | module docstring | `.backward(` token | ℹ️ Info | Prohibition mention only; not a call |
| `tests/phase55/fixtures/six_case_baseline.json` | whole file | Fixture generated by `run_sweep()` itself | ℹ️ Info | D-01 tier-2 regression pin is circular by design. Correctness vs the 2026-08-17 audit is independently asserted by Tier-1 bounds and the decade table above. |
| `tests/phase38/test_prohibitions.py` | `test_spec_byte_identity_endpoint_sha256`, `test_spec_history_no_touch_since_phase_base` | Full-file pytest still red | ℹ️ Info | Two pre-existing SCOPE-18 spec-SHA failures (`pinn_architecture.md` working-tree sha `51669747…` ≠ Phase-38 baseline `e629b2fc…`). Unrelated to the exclude-list. Precision/v1.3 glob tests pass. |

No `TBD`/`FIXME`/`XXX` in phase-modified production or test files. No skipped Phase 55 tests.

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `tests/phase55/test_architecture_characterization.py` | INST-04 | 46 | 0 | Tier-2 fixture is a same-system pin (see Info) | Behavioral + value | PROVES INST-04 |
| `tests/phase38/test_prohibitions.py` (exclude-list tests) | INST-04 (D-02 enabler) | 3 targeted + 96 subtests | 0 in targeted set | No | Value (path membership, AST tokens) | PROVES exclude-list |

### Decision Coverage

`gsd-tools query check.decision-coverage-verify`: `{honored: 3, total: 3, not_honored: []}`.

- D-01 two-tier regression gate — honored (Tier-1 tests + committed fixture).
- D-02 general config-driven sweep — honored (Python API + CLI `--cases-config` + zero-arg default).
- D-03 build capability, do not exercise as milestone artifact — honored (helpers + containment tests + no `R_ref` evidence).

### Commit-claim reconciliation

Per-plan `actuals.commits` match the task commits on `milestone/v2.3`. Each SUMMARY commit is the expected `CLAIMED + 1` docs closeout.

| Plan | `plan_head_before` | Claimed task commits | Observed task commits |
| --- | --- | --- | --- |
| 55-01 | `0c0edd9c` | 3 | `44155884`, `6654b078`, `09095aa2` |
| 55-02 | `6d4f9699` | 3 | `09c3c563`, `f68ddd47`, `6477099e` |
| 55-03 | `bee5871f` | 2 | `c20691f9`, `b599444f` |
| 55-04 | `59b983c2` | 4 | `d5bd6f5b`, `f5c68155`, `2b1a4fd1`, `912c3193` |

### Human Verification Required

None. No `<human-check>` blocks in the four PLANs. This is a CLI/library instrumentation phase; the required behaviors are exercised by pytest.

### Gaps Summary

None. Phase goal is achieved in the codebase.

---

_Verified: 2026-09-06T04:15:32Z_
_Verifier: Grok (gsd-verifier fallback)_

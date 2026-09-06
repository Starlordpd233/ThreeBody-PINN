---
phase: 55-architecture-characterization-probe
verified: 2026-09-06T10:06:31Z
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
  - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json
  - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md
  - pinn/verification/architecture_characterization_probe.py
  - tests/phase38/test_prohibitions.py
  - tests/phase55/__init__.py
  - tests/phase55/fixtures/six_case_baseline.json
  - tests/phase55/test_architecture_characterization.py
covered_digest: "v1:sha256:2061a75735dc3f9697179afef740c2cf455e5c4aef138bb6fb11c8829e80526a"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: 12/12
  trigger: "covered-file staleness after phase closeout + retroactive secure/validate; verification.status=stale, uat-passed --require-verification=false"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
  code_test_evidence_bytes: "identical to initial verification 48e3e2fa (git diff --stat 48e3e2fa HEAD over every code/test/evidence/plan/summary/context covered file is empty)"
decision_coverage:
  honored: 3
  total: 3
  not_honored: []
---

# Phase 55: Architecture Characterization Probe Verification Report

**Phase Goal:** v2.3's central premise rests on a measurement; that measurement stops being ad-hoc and becomes committed, tested tooling that anyone can re-run against any candidate recipe.
**Verified:** 2026-09-06T10:06:31Z
**Status:** passed
**Re-verification:** Yes — triggered by covered-file staleness after phase closeout + retroactive secure/validate. All code / test / evidence / plan / summary / context covered files are byte-identical to the initial verification tree at `48e3e2fa` (`git diff --stat 48e3e2fa HEAD --` over each is empty). This pass re-ran the full goal-backward verification against current HEAD from scratch — it did not shortcut.
**Working tree:** `<home>/Desktop/3_body_problem/.worktrees/trainex` on `milestone/v2.3` at `4c1fa011`

## Re-verification context

The initial verification (`48e3e2fa`, status `passed`, 12/12, verifier "Grok (gsd-verifier fallback)") was recorded against tree `2a34cc20` and explicitly deferred two orchestrator/retroactive acts. Those have since landed:

| Commit | Act | Effect on a covered file |
| --- | --- | --- |
| `ecee1197` | phase closeout | `.planning/REQUIREMENTS.md`: INST-04 `[ ]`→`[x]` and traceability `INST-04 \| Phase 55 \| Pending`→`Complete` (also ROADMAP.md / STATE.md — not covered here, not touched by this report) |
| `5fd667ef` | retroactive `/gsd-secure-phase 55` | new `55-SECURITY.md` (not a covered file) |
| `4c1fa011` | retroactive `/gsd-validate-phase 55` | `55-VALIDATION.md`: `status: draft`→`validated`, `nyquist_compliant: false`→`true`, added "Validation Audit 2026-09-06" section |
| `d4e55e69` | `/gsd-code-review 55` | new `55-REVIEW.md` (not a covered file) |

**`verification.status` was `stale`** because the prior `covered_files` list included `.planning/REQUIREMENTS.md` (legitimately — it holds the mapped requirement) **and** `55-VALIDATION.md` (a sibling validate-phase artifact). This pass re-verifies against `4c1fa011` and rewrites the digest.

### Post-closeout artifacts now present and consistent

- `.planning/REQUIREMENTS.md:99` → `- [x] **INST-04**`; `.planning/REQUIREMENTS.md:178` → `| INST-04 | Phase 55 | Complete |`. GATE-04 correctly remains `- [ ]` / `| GATE-04 | Phase 56 | Pending |` (the probe emits no recipe verdict; GATE-04 is a Phase 56 requirement).
- `55-SECURITY.md` — `status: verified`, `threats_open: 0`; 20 STRIDE threats + 1 supply-chain entry, all `closed` or `closed — accepted`; ASVS L1 grep-depth.
- `55-VALIDATION.md` — `status: validated`, `nyquist_compliant: true`; Validation Audit records 14/14 rows COVERED, 0 gaps. Its note that `tests/phase38/test_prohibitions.py` shows `2 failed` (the pre-existing SCOPE-18 `pinn_architecture.md` spec-SHA failures) matches this report's Anti-Patterns table.

### covered_files change this pass

**Dropped `55-VALIDATION.md`.** Per #4155 the covered-file set is "every phase PLAN/SUMMARY (+superseded, nested plans/), mapped requirement, changed impl file". A validate-phase artifact is a sibling GSD-workflow output, not goal-backward evidence for the probe — and keeping it created a circular staleness coupling (`/gsd-validate-phase` runs *after* verification, mutates `55-VALIDATION.md`, re-stales the verification), which is half of what triggered this re-verification. `55-VALIDATION.md` was inspected this pass only to confirm its closeout state for this narrative. `.planning/REQUIREMENTS.md` is kept — it is the mapped requirement and its INST-04 completion state is within a verification's scope. `55-CONTEXT.md` (D-01/D-02/D-03 decisions basis) and the two `evidence/probe/20260906T035209Z/` files (SC2-critical committed deliverables) are kept, matching the prior report's scope. No `55-SECURITY.md` / `55-REVIEW.md` added (same sibling-artifact reasoning).

## Goal Achievement

INST-04 is landed as a committed, importable, tested probe at `pinn/verification/architecture_characterization_probe.py` (883 lines). Given an `ArchitectureSpec` at initialization — no data file read, no optimizer, no `.backward()` / `.step()` — it reports the seven architecture-only quantities over a configurable seed/IC sweep, and it reproduces the 2026-08-17 audit six-row table at decade resolution with `front_idx = 0` and `R̄ ≈ 10¹⁰` in every row. A fresh zero-argument CLI invocation at HEAD `4c1fa011` produces output **bit-identical** to the committed evidence run and the committed exact-value fixture. D-03 helpers exist and are synthetic-tested but are provably unreachable from the default measurement path; Phase 55 produced no `R_ref` / GATE-04 evidence.

### Observable Truths

Must-haves are the four ROADMAP success criteria plus PLAN-frontmatter additions that add plan-specific detail without reducing scope. SUMMARY.md claims were not used as evidence.

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | ROADMAP SC1: `pinn/verification/` contains committed, tested tooling that, given an `ArchitectureSpec` at initialization and **no data, no optimizer, no training step**, reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx` over a configurable seed/IC sweep (INST-04). | ✓ VERIFIED | `measure_case` (probe:309) builds `ArchitectureSpec(seed=case.seed)` → `build_network` → `model.eval()` (probe:320-322); synthetic IC13 (`_ic13_for_case`), `CollocationSampler`, then trainer primitives. Grep: no `optim`/`Optimizer`/`DataLoader`/`.step(`/`.h5`/`h5py` tokens; `backward` appears only in the module docstring (probe:5). `ArchitectureCharacterizationResult` carries all seven quantities; `a_norm_median` is the median of `‖second‖` where `first, second = componentwise_du(traj, u_leaf)` (the second derivative d²r′/du²). `run_sweep(cases=…)` and `--cases-config` accept an arbitrary list; `DEFAULT_CASES` is the six audited rows. `test_tracer_single_case_reports_all_seven_quantities` + `test_default_cases_are_the_six_audited_rows` pass. Probe is `git ls-files`-tracked. |
| 2 | ROADMAP SC2: under the pre-amendment recipe the probe **reproduces the 2026-08-17 residual-frame conformance audit's six-row table** across the same six seed/IC combinations — `R̄ ≈ 10¹⁰` and `front_idx = 0` in every row — recorded re-derivably (command, tree state, full output) per the GAP-44-02 discipline. | ✓ VERIFIED | `test_invariant_bounds_six_cases[41,42,43,0,7,41-variable-mass]` asserts `front_idx == 0` and `1e9 < rbar_median < 1e11` for all six. Committed `evidence/probe/20260906T035209Z/raw.json`: `argv: []`, `command: python -m pinn.verification.architecture_characterization_probe`, `git_sha: 2b1a4fd1…`, `git_worktree_dirty: true`, torch 2.12.0 / numpy 2.2.0, `failure: null`, six full case records. **A fresh zero-argument CLI run at HEAD `4c1fa011` reproduces the committed `raw.json` bit-identically** (max relative field difference `0.0` across all six cases, including the 16-element weight vectors). Independent audit §6b decade cross-check (below) holds. |
| 3 | ROADMAP SC3: the probe derives `R̄` and the causal weights from the same implementation the trainer uses, so a probe result is evidence about the shipped recipe rather than a parallel re-implementation. | ✓ VERIFIED | Direct calls in `measure_case`: `componentwise_du` (probe:346), `softened_acceleration` (probe:351), `causal_physics_loss(rbar, times=…, return_details=True)` for `w_n` (probe:363-370). The `rbar` reduction `(residual ** 2).sum(dim=(-2, -1)) / 3.0` (probe:359) is **byte-identical** to `pinn/training/controllers.py:656`, and the CONF-04/D-05 comment block is copied verbatim; `_front_idx` (probe:281-283) is byte-identical to `controllers.py:692-693`. `test_derives_from_trainer_implementation` monkey-patches `causal_physics_loss`, `softened_acceleration`, and `componentwise_du` on the probe module (×2.0) and asserts `causal_weights`, `f_grav_norm_median`, `v_norm_median`, `a_norm_median` move in lock-step. |
| 4 | ROADMAP SC4: a test suite fails if any reported quantity, the sweep configuration, or the six-row reproduction regresses. | ✓ VERIFIED | Tier-1 invariant bounds (`test_invariant_bounds_six_cases`, parametrized ×6). Tier-2 `test_exact_value_fixture` compares every string/int field exactly and every scalar/sequence field at the fixture's own `relative_tolerance = 1e-09`. `test_fixture_comparison_fails_on_a_perturbed_baseline` proves the comparator is fail-first; session-scoped autouse `_assert_baseline_sha256_unchanged` + `test_fixture_file_is_never_written_by_the_suite` prove the net cannot heal itself. `test_default_cases_are_the_six_audited_rows` pins the sweep configuration. `.venv/bin/python -m pytest tests/phase55/ -q` → **46 passed, 0 skipped** (re-run twice this pass: 9.78s, 11.40s; exit 0). |
| 5 | BOUNDARY EDGE (INST-04): causal-weight clamp floor and `front_idx` threshold pinned at the boundary and one step either side. | ✓ VERIFIED | `test_causal_weights_pinned_at_dtype_clamp_floor[×6]`: `causal_weights[0] == 1.0`; `all(w == floor for w in causal_weights[1:])` where `floor = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))["causal_clip_min_weight"]` computed at test time (never a literal); `causal_clip_min_weight == floor`. `test_front_idx_threshold_is_strictly_above_half`: `_front_idx([0.5+ulp, 0.5, 0.5]) == 0` (strict `>` predicate). `test_front_idx_sentinel_when_no_weight_exceeds_half`: all `≤ 0.5` → `-1`. |
| 6 | PRECISION EDGE (INST-04): even-`n_col = 16` median is `numpy.median` (mean of the two central order statistics), not `torch.median`; clamp floor is dtype-derived. | ✓ VERIFIED | Module constant `MEDIAN_CONVENTION` names the contract; `_median` calls `np.median`; every result's `median_convention` field copies the constant (asserted for all six cases in `test_median_convention_averages_two_central_values`, which also checks `_median` of a 16-element array with distinct central values 10.0/20.0 == 15.0). Confirmed live: float64 floor `2.2250738585072626e-308` ≠ float32 floor `1.175499675756452e-38`, both from `resolve_causal_clip_facts(dtype, device)`. |
| 7 | Reported norm convention is arithmetically consistent with the audit: median `R̄` equals `(median ‖a′‖)² / 3` to within 10 percent for every default case. | ✓ VERIFIED | `test_norm_convention_matches_audit_rbar_identity[×6]`: `predicted = a_norm_median ** 2 / 3.0`; `abs(rbar_median - predicted) / rbar_median < 0.10`. Passes. |
| 8 | D-02 CLI/config: zero-argument invocation runs the six audited cases at float64/CPU; `--cases-config` drives an arbitrary list; malformed entries raise `ValueError` naming the field before any directory is created. | ✓ VERIFIED | `_parse_args`: `--precision` (default `float64`), `--device` (default `cpu`) — neither `required`. `ArchitectureCharacterizationCLITests.test_zero_argument_cli_reproduces_six_rows` + `test_cases_config_drives_arbitrary_case_list` pass (subprocess `-m pinn.verification.architecture_characterization_probe`). `test_malformed_cases_config_raises_value_error[×5]` (seed −1, seed `True`, masses len 2, masses 0.0, ic13_mode bogus) asserts `ValueError` matching the field name **and** `list(evidence_root.iterdir()) == []`. |
| 9 | Evidence writer: non-overwriting UTC run dir; `raw.json` provenance allowlist; `atomic_write_text`; `--evidence-root` inside `simulation_data/` rejected before mkdir. | ✓ VERIFIED | `_new_run_dir` uses `mkdir(exist_ok=False)` + a 000–999 suffix retry; `_write_evidence` writes `raw.json` and `summary.md` via `atomic_write_text`. `_reject_dataset_evidence_root` runs first inside `_new_run_dir`. `_provenance` returns `git_head()` + `_git_worktree_dirty()` + versions + conventions + `causal_clip_facts`. Top-level keys equal `EVIDENCE_TOP_LEVEL_KEYS = {schema_version, provenance, configuration, cases, failure}`. `test_cli_writes_provenance_evidence`, `test_cli_allocates_non_overwriting_run_dirs`, `test_evidence_root_inside_simulation_data_is_rejected` pass. |
| 10 | Phase-38 exclude-list: the probe is in `_EXCLUDE_SUFFIXES` with a D-02 rationale; the precision/v1.3 glob tests pass; discovery does not list the probe. | ✓ VERIFIED | `tests/phase38/test_prohibitions.py:76` lists `pinn/verification/architecture_characterization_probe.py` in `_EXCLUDE_SUFFIXES`; lines 62-75 are the rationale comment citing "Phase 55 D-02" and the `pinn/runtime.py` precedent. The two non-precision guarantees are re-homed to `tests/phase55/` as `test_module_has_no_global_default_mutation_or_device_probe` and `test_module_has_no_v1_3_era_imports`. `pytest tests/phase38/test_prohibitions.py -k "no_precision_default or no_v1_3_era or discovered_modules"` → **3 passed, 3 deselected, 96 subtests passed**. |
| 11 | D-03: 4096/256/16 helpers exist and are synthetic-tested; default `run_sweep`/`measure_case`/`main` cannot reach them; Phase 55 produced no `R_ref` / GATE-04 evidence. | ✓ VERIFIED | `stratified_collocation_times`, `bin_mean_residuals`, `RATIFIED_N_BINS=16`, `RATIFIED_PER_BIN=256`, `RATIFIED_TOTAL=4096` present, transcribed from `54-RULING.md` B2/D3. `test_stratified_bins_synthetic` (4096 total, 256/bin, half-open edges + closed last bin, determinism, global-RNG untouched, error paths) and `test_bin_mean_residuals_synthetic` (closed-form `256·arange(16) + 127.5`, length/index/empty-bin `ValueError`s) pass. `test_new_structure_helpers_unreachable_from_default_sweep` — AST call-graph closure from `run_sweep/measure_case/main` (incl. default-arg expressions and module-level statements), with anti-vacuity guards (`assert reachable`, `assert "_ic13_for_case" in reachable`) — plus runtime backstop `test_default_sweep_never_exceeds_sixteen_causal_points` (every `causal_physics_loss` call in `run_sweep()` and `main([])` receives exactly `DEFAULT_N_COL = 16`). No `R_ref` / `GATE-04` verdict token in the probe or the committed evidence. |
| 12 | D-01 tier 2: committed exact-value fixture with regeneration provenance; comparison is read-only; a perturbed copy fails; on-disk sha256 is stable. | ✓ VERIFIED | `tests/phase55/fixtures/six_case_baseline.json` sha256 `65edebc78d334c76e532a15d75bb6ca70ee4a3094f68b66804ad12d4372bc474` (tracked). `_meta` names `regeneration_command`, `precision`/`device`/`n_col`, `torch_version` 2.12.0, `numpy_version` 2.2.0, `median_convention`, `ic13_rng_scheme`, `relative_tolerance: 1e-09`, `purpose`. `test_exact_value_fixture`, `test_fixture_comparison_fails_on_a_perturbed_baseline`, `test_fixture_file_is_never_written_by_the_suite` pass. Suite only `json.load`s the fixture; the only writes in the test file target `tmp_path` config JSON. Fixture values match the committed `raw.json` and a fresh CLI run (rel diff `0.0`). |

**Score:** 12/12 truths verified (0 present, behavior-unverified). Every truth is exercised by a behavioral test re-run this pass; none rests on symbol presence alone.

### Independent audit §6b decade check (SC2)

Source: `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` §6b (lines 142-149). Repro: committed `evidence/probe/20260906T035209Z/raw.json` (re-read this pass; equals a fresh HEAD CLI run bit-for-bit). Agreement is decade / order-of-magnitude — the audit records only "16 sorted uniform `u ∈ [0,1]`" with no RNG scheme, so the original ad-hoc collocation draw is unrecoverable.

| seed / IC | ‖r′‖ audit / repro | ‖v′‖ | ‖a′‖ | ‖F_grav‖ | min sep | `R̄` median | `front_idx` |
|---|---|---|---|---|---|---|---|
| 41, m=(1,1,1), IC13=0 | 1.28 / 1.085 | 310 / 251.8 | 2.03×10⁵ / 1.975×10⁵ | 2.17 / 3.131 | 0.91 / 0.784 | 1.37×10¹⁰ / 1.301×10¹⁰ | 0 / 0 |
| 42 | 1.13 / 1.009 | 331 / 313.5 | 2.72×10⁵ / 2.411×10⁵ | 3.29 / 4.410 | 0.67 / 0.607 | 2.46×10¹⁰ / 1.938×10¹⁰ | 0 / 0 |
| 43 | 0.97 / 0.830 | 251 / 297.9 | 2.20×10⁵ / 2.078×10⁵ | 3.24 / 5.913 | 0.72 / 0.582 | 1.62×10¹⁰ / 1.440×10¹⁰ | 0 / 0 |
| 0 | 0.91 / 0.976 | 281 / 301.8 | 2.79×10⁵ / 2.040×10⁵ | 5.94 / 5.803 | 0.50 / 0.554 | 2.60×10¹⁰ / 1.387×10¹⁰ | 0 / 0 |
| 7 | 0.85 / 1.083 | 290 / 239.4 | 1.94×10⁵ / 2.027×10⁵ | 5.89 / 3.616 | 0.51 / 0.677 | 1.25×10¹⁰ / 1.370×10¹⁰ | 0 / 0 |
| 41, m=(1,0.8,0.6), random tanh IC13 | 0.95 / 1.124 | 231 / 327.4 | 2.28×10⁵ / 1.917×10⁵ | 2.85 / 2.807 | 0.72 / 0.719 | 1.74×10¹⁰ / 1.224×10¹⁰ | 0 / 0 |

All six `front_idx` = 0. All six median `R̄` sit in the 10¹⁰ decade (`1.224×10¹⁰` … `1.938×10¹⁰`). Largest single audit/repro ratio ≈ 1.87 (`R̄`, seed 0); every column stays inside a factor of 10. SC2's literal claims (`front_idx = 0` and `R̄ ≈ 10¹⁰` in every row) hold exactly.

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | ----------- | ------ | ------- |
| `pinn/verification/architecture_characterization_probe.py` | SweepCase, result dataclass, DEFAULT_CASES, measure_case, run_sweep, main, load_cases_config, stratified helpers, evidence writer | ✓ VERIFIED | 883 lines; `__all__` exports the public surface; imports as `pinn.verification.architecture_characterization_probe`; byte-identical to `48e3e2fa` |
| `tests/phase55/__init__.py` | Package marker | ✓ VERIFIED | 1-line package marker |
| `tests/phase55/test_architecture_characterization.py` | Tracer, Tier-1, SC3 mutation, CLI, D-03 containment, Tier-2 | ✓ VERIFIED | 724 lines; 46 collected tests (21 functions + parametrization + a 6-method `unittest.TestCase`); all pass, none skipped; byte-identical to `48e3e2fa` |
| `tests/phase38/test_prohibitions.py` | `_EXCLUDE_SUFFIXES` entry + rationale | ✓ VERIFIED | Probe listed at line 76 with a D-02 rationale comment; targeted glob tests pass; byte-identical to `48e3e2fa` |
| `tests/phase55/fixtures/six_case_baseline.json` | Full six-row output + `_meta` | ✓ VERIFIED | `_meta` + six cases; sha256 `65edebc7…`; matches committed `raw.json` and a fresh CLI run; byte-identical to `48e3e2fa` |
| `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/` | One committed re-derivable run | ✓ VERIFIED | Exactly one UTC-stamp dir; `raw.json` + `summary.md`; `failure: null`; byte-identical to `48e3e2fa` |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `architecture_characterization_probe.py` | `pinn.loss_catalog.causal_physics_loss` | `causal_physics_loss(rbar, times=…, return_details=True)` → `details["w_n"]` | WIRED | Live call in `measure_case` (probe:363); SC3 mutation test moves weights in lock-step; import resolves |
| `architecture_characterization_probe.py` | `pinn.physics_residual` | `componentwise_du(traj, u_leaf)` / `softened_acceleration(positions, masses, …)` | WIRED | Live calls in `measure_case` (probe:346, 351); mutation test moves v′/a′/F_grav |
| `architecture_characterization_probe.py` | `pinn.network.build_network` + `pinn.architecture_spec.ArchitectureSpec` | `build_network(ArchitectureSpec(seed=case.seed), dtype, device)` | WIRED | Live call in `measure_case` (probe:320-321) |
| `architecture_characterization_probe.py` | `pinn.training.atomic_io.atomic_write_text` | tmp-write + fsync + `os.replace` + parent-dir fsync | WIRED | `_write_evidence` two calls (probe:791, 795); import resolves |
| `architecture_characterization_probe.py` | `pinn.verify.git_head` | provenance sha + availability flag | WIRED | `_provenance` unpacks `(git_sha, git_available)` (probe:672); import resolves |
| `architecture_characterization_probe.py` | `pinn/training/controllers.py` residual/front recipe | `rbar` reduction + `_front_idx` formula | WIRED (identical) | probe:359 == `controllers.py:656`; probe:281-283 == `controllers.py:692-693` |
| `tests/phase38/test_prohibitions.py` | probe module | `_EXCLUDE_SUFFIXES` membership | WIRED | Probe excluded from `_discover_phase38_modules()`; targeted glob green |
| `tests/phase55/test_architecture_characterization.py` | `six_case_baseline.json` | read-only per-field compare at `_meta.relative_tolerance` | WIRED | `_load_fixture` (`json.load` only) + `_compare_case_to_fixture`; sha256 guard |
| `evidence/probe/20260906T035209Z` | probe CLI | zero-argument module invocation | WIRED | `raw.json` `argv: []`, `command` == `_MODULE_PROG` |
| `architecture_characterization_probe.py` | `54-RULING.md` B2/D3 | `RATIFIED_N_BINS/PER_BIN/TOTAL` | WIRED | Constants 16 / 256 / 4096; helpers proven unreachable from the default path |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `measure_case` | `r'`, `v'`, `a'` | `build_network` forward + `componentwise_du` on live `u_leaf` (`torch.func.vmap`) | Yes | ✓ FLOWING |
| `measure_case` | `F_grav` | `softened_acceleration(positions, masses, …)` | Yes | ✓ FLOWING |
| `measure_case` | `R̄`, `w_n`, `front_idx` | `residual = accel − force` → `(residual**2).sum(-2,-1)/3` → `causal_physics_loss(return_details=True)` → `w > 0.5` | Yes | ✓ FLOWING |
| `raw.json` | `cases[]` | `asdict(ArchitectureCharacterizationResult)` from `run_sweep` | Yes | ✓ FLOWING |
| `six_case_baseline.json` | `cases[]` | previously captured `run_sweep()` output; re-confirmed equal to a fresh HEAD run (rel 0.0) | Yes (regression pin, not an external oracle) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Phase 55 suite | `.venv/bin/python -m pytest tests/phase55/ -q` | `46 passed in 9.78s` (re-run: `46 passed in 11.40s`); exit 0; `-rs` shows 0 skipped | ✓ PASS |
| Per-truth named tests | `pytest -k "derives_from_trainer_implementation or new_structure_helpers_unreachable or default_sweep_never_exceeds or causal_weights_pinned or front_idx_threshold or median_convention_averages or norm_convention_matches"` | `17 passed, 29 deselected` | ✓ PASS |
| Fresh zero-arg CLI at HEAD | `.venv/bin/python -m pinn.verification.architecture_characterization_probe --evidence-root <scratch>` | exit 0; six rows; every numeric field (incl. 16-element weight vectors) equals committed `raw.json` and `six_case_baseline.json` with max relative difference `0.0`; `front_idx == 0` all rows | ✓ PASS |
| Public API importable | `python -c` import + `DEFAULT_CASES` labels | labels `['41','42','43','0','7','41-variable-mass']`; all `__all__` exports present | ✓ PASS |
| Phase-38 exclude glob | `pytest tests/phase38/test_prohibitions.py -k "no_precision_default or no_v1_3_era or discovered_modules"` | `3 passed, 3 deselected, 96 subtests passed` | ✓ PASS |
| D-03 leak check | grep `run_sweep`/`measure_case`/`main` for `stratified_collocation_times`, `bin_mean_residuals`, `R_ref` | no matches; AST + runtime containment tests green | ✓ PASS |
| Trainer imports resolve | `python -c "from pinn.training.atomic_io import atomic_write_text; from pinn.verify import git_head; ..."` | all resolve | ✓ PASS |

### Probe Execution

No `scripts/*/tests/probe-*.sh` is declared for this phase — the deliverable **is** the characterization probe. Its CLI is exercised by `ArchitectureCharacterizationCLITests` (subprocess `-m pinn.verification.architecture_characterization_probe`) and, this pass, by one independent zero-argument invocation into a scratch evidence root (removed afterward — the committed `evidence/probe/` directory was not modified).

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| architecture characterization (test-harness CLI) | `ArchitectureCharacterizationCLITests` (6 methods) | exit 0, six rows, provenance keys, non-verdict exit code, structured failure record on error | PASS |
| architecture characterization (committed run) | recorded `python -m pinn.verification.architecture_characterization_probe` (`argv: []`) | `raw.json` + `summary.md`, `failure: null` | PASS |
| architecture characterization (fresh HEAD run, this pass) | `python -m pinn.verification.architecture_characterization_probe --evidence-root <scratch>` | exit 0; bit-identical to committed evidence | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ---------- | ----------- | ------ | -------- |
| INST-04 | 55-01, 55-02, 55-03, 55-04 | Land the architecture-only characterization as committed, tested verification tooling under `pinn/verification/`; report the seven quantities at init over a configurable sweep; reproduce the 2026-08-17 six-row table | ✓ SATISFIED | Probe module + `tests/phase55/` (46 passed) + committed evidence run + audit §6b decade cross-check + fresh-run bit-match. `.planning/REQUIREMENTS.md` now shows `- [x] INST-04` and `| INST-04 | Phase 55 | Complete |`. |
| GATE-04 | (none; mapped to Phase 56) | Train-free acceptance gate on the recalibration | n/a (not this phase) | `REQUIREMENTS.md:179` maps `GATE-04 → Phase 56`. The probe explicitly emits no recipe verdict (`test_cli_exit_code_is_not_a_recipe_verdict`; `EVIDENCE_TOP_LEVEL_KEYS` has no verdict field). |

No orphaned Phase 55 requirements — `REQUIREMENTS.md` maps only INST-04 to Phase 55, and all four plans declare `requirements: [INST-04]`.

### Prohibitions

All four PLAN-frontmatter prohibitions are `verification: test` and have wired enforcement (not silent, not unverified).

| Prohibition (requirement_id: INST-04) | Enforcement | Status |
| --- | --- | --- |
| MUST NOT compute `R̄` / weights / `front_idx` / AD from a parallel re-implementation | `test_derives_from_trainer_implementation` — mutating each of `causal_physics_loss` / `softened_acceleration` / `componentwise_du` on the probe module moves the reported quantities in lock-step | ✓ HELD |
| MUST NOT emit a pass/fail recipe verdict (exit code, evidence field, or printed health claim) | `test_cli_exit_code_is_not_a_recipe_verdict`; `EVIDENCE_TOP_LEVEL_KEYS` has no verdict field; `main` returns 0 iff measurement completed, non-zero with a structured `failure` block otherwise; `_summary_markdown` "Makes no claim about whether any value is acceptable" | ✓ HELD |
| MUST NOT run the real six-case sweep under the 4096-total / 256-per-bin / 16-bin structure as `R_ref` / any normalization constant / GATE-04 evidence (D-03) | AST call-graph closure (`test_new_structure_helpers_unreachable_from_default_sweep`, with anti-vacuity guards) + runtime 16-point recorder (`test_default_sweep_never_exceeds_sixteen_causal_points`) + no `R_ref` token in the probe or committed evidence | ✓ HELD |
| MUST NOT auto-regenerate / auto-heal / self-update the committed exact-value fixture | `test_fixture_comparison_fails_on_a_perturbed_baseline` (fail-first) + session-scoped autouse sha256 guard + `test_fixture_file_is_never_written_by_the_suite`; the suite only `json.load`s the fixture | ✓ HELD |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `pinn/verification/architecture_characterization_probe.py` | 5 (module docstring) | `.backward()` token | ℹ️ Info | Prohibition statement only; not a call. No `optim`/`Optimizer`/`DataLoader`/`.step(` tokens anywhere. |
| `tests/phase55/test_architecture_characterization.py` | `_load_probe` (42-47) | `unittest.SkipTest` on `ImportError` | ℹ️ Info | A catastrophic *import* break would degrade the function-style tests to SKIP rather than FAIL. Mitigants: module imports cleanly (0 skipped observed, twice); the CLI subprocess `TestCase` still FAILs on a broken module; a value-drift regression still FAILs loudly via Tier-1 bounds and the Tier-2 fixture (which is the dominant SC4 risk). Matches the `tests/phase38/test_residual_probe.py` house convention. Noted in the initial verification too. |
| `tests/phase55/fixtures/six_case_baseline.json` | whole file | Fixture generated by `run_sweep()` itself | ℹ️ Info | D-01 tier-2 regression pin is a same-system baseline by design (CONTEXT.md D-01, mirroring `gate_metrics.py`). Correctness vs the 2026-08-17 audit is asserted independently by Tier-1 bounds and the decade table above. |
| `tests/phase38/test_prohibitions.py` | `test_spec_byte_identity_endpoint_sha256`, `test_spec_history_no_touch_since_phase_base` | Full-file `pytest tests/phase38/test_prohibitions.py` still shows `2 failed` | ℹ️ Info | Pre-existing SCOPE-18 spec-SHA failures on `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (last touched by `3e9f94da`, Phase 53 — **no Phase 55 commit touches it**). Documented in `STATE.md`, the initial `55-VERIFICATION.md`, and `55-VALIDATION.md`. Unrelated to Phase 55; the exclude-list / precision / v1.3 assertions this file owns for the probe all pass. |

No `TBD` / `FIXME` / `XXX` / `HACK` / `PLACEHOLDER` / `TODO` in any phase-modified production or test file. No `return None`/`return {}`/`raise NotImplementedError`/bare-`pass` stub patterns in the probe. No skipped Phase 55 tests.

### Advisory (New Scope, Unevidenced)

`is_re_verification = true`. Step 7's anti-pattern scan produced no 🛑 Blocker of any kind — no debt markers, no stubs, no unwired artifacts. The #3304 convergence evidence gate therefore has nothing to downgrade.

| # | Finding | Category | Why Advisory |
|---|---------|----------|--------------|
| — | None | — | No new-scope blocker was raised this pass. |

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `tests/phase55/test_architecture_characterization.py` | INST-04 | 46 | 0 | Tier-2 fixture is a declared same-system pin (see Info); Tier-1 bounds + audit decade table are independent | Behavioral (mutation lock-step, subprocess CLI, AST closure, runtime recorder) + Value (exact fixture at rel 1e-9) | PROVES INST-04 (SC1–SC4, boundary/precision edges, D-01/D-02/D-03) |
| `tests/phase38/test_prohibitions.py` (exclude-list subset) | INST-04 (D-02 enabler) | 3 targeted + 96 subtests | 0 in the targeted set | No | Value (path membership, AST tokens) | PROVES the exclude-list + re-homed guarantees |

Disabled tests on requirements: 0. Circular patterns forcing a BLOCKER: 0 (the fixture pin is a documented CONTEXT.md decision with independent Tier-1 coverage). Insufficient assertions: 0.

### Decision Coverage

`gsd-tools query check.decision-coverage-verify` → `{ honored: 3, total: 3, not_honored: [] }` — "All trackable CONTEXT.md decisions are honored by shipped artifacts." (Non-blocking gate; recorded for drift tracking.)

- **D-01** two-tier regression gate — honored (`test_invariant_bounds_six_cases` + committed `six_case_baseline.json` + `test_exact_value_fixture`).
- **D-02** general config-driven sweep, six audited cases as default — honored (`run_sweep(cases=…)` Python API + CLI `--cases-config` + zero-argument default).
- **D-03** build the capability, do not exercise it as a milestone artifact — honored (helpers + synthetic tests + AST/runtime containment + no `R_ref` evidence).

Note: 55-CONTEXT.md states the three decisions "None involve a physics/spec adjudication call ... they are test-design and API-scope choices" — consistent with Phase 55 being an instrumentation phase, not a spec-adjudication milestone, so the CLAUDE.md STOP-protocol grounding gate does not apply here.

### Human Verification Required

**N/A — infrastructure / tooling phase (a committed CLI + library probe) with no user-facing elements.** No `<human-check>` blocks in the four PLANs. No truth asserts a runtime state transition or a cancellation / cleanup / ordering invariant that presence checks cannot see — `measure_case` is deterministic (`test_tracer_case_is_deterministic_across_two_calls`) and the one ordering concern (atomic evidence write) is delegated to the already-tested `atomic_write_text` and covered by `test_cli_allocates_non_overwriting_run_dirs`. No `⚠️ PRESENT_BEHAVIOR_UNVERIFIED` truths, no `insufficient_spec` abstentions. All acceptance criteria are verifiable programmatically and were re-verified this pass.

### Gaps Summary

None. The phase goal is achieved in the codebase at HEAD `4c1fa011`. This re-verification re-ran the full goal-backward analysis (probe module read end-to-end, test suite re-executed twice, 17 per-truth named tests, a fresh zero-argument CLI run compared bit-for-bit against the committed evidence and fixture, prohibitions and decision coverage re-checked) and reproduces the initial verdict of 12/12. The only changes since the initial verification (`48e3e2fa`) are the deferred closeout of `.planning/REQUIREMENTS.md` INST-04 → Complete and the retroactive `/gsd-secure-phase` + `/gsd-validate-phase` artifacts; every code, test, evidence, plan, summary, and context file is byte-identical, and the newly landed `REQUIREMENTS.md` / `55-SECURITY.md` / `55-VALIDATION.md` states are all internally consistent with this report.

---

_Verified: 2026-09-06T10:06:31Z_
_Verifier: Claude (gsd-verifier) — re-verification against HEAD 4c1fa011_

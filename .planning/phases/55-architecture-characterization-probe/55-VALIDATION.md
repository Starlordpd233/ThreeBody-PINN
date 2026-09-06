---
phase: 55
slug: architecture-characterization-probe
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-09-04
---

# Phase 55 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest` 9.1.1 (verified live via `.venv/bin/python -m pytest --version`) |
| **Config file** | none — no `pytest.ini`/`pyproject.toml`/`setup.cfg` at repo root; pytest runs with rootdir-based `sys.path` insertion (matches existing `tests/phase38/`, `tests/phase49/` convention) |
| **Quick run command** | `.venv/bin/python -m pytest tests/phase55/ -q` |
| **Full suite command** | `.venv/bin/python -m pytest tests/ -q` |
| **Estimated runtime** | ~10-30 seconds (quick); full suite has 14 pre-existing, unrelated failures documented in `.planning/STATE.md` — diff the failure set before/after, do not treat those as Phase 55 regressions |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/python -m pytest tests/phase55/ -q`
- **After every plan wave:** Run `.venv/bin/python -m pytest tests/ -q`
- **Before `/gsd-verify-work`:** Full suite must be green (modulo the 14 documented pre-existing failures)
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

Task IDs assigned by the planner on 2026-09-04 from the four Phase-55 plans. Every command below is run with the `.venv` interpreter: `.venv/bin/python -m pytest …`. Executors update the **Status** column as each task lands and correct any test-name drift in place.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 55-01-T1 | 55-01 | 1 | INST-04 (SC1) | T-55-01, T-55-02, T-55-03 | reports all 7 quantities for one case at initialization — no data, no optimizer, no training step; deterministic across two calls; malformed `SweepCase` fields fail closed | unit (tracer, end-to-end) | `pytest tests/phase55/test_architecture_characterization.py -k "tracer or sweep_case_rejects" -x -q` | ✅ exists | ✅ green |
| 55-01-T2 | 55-01 | 1 | INST-04 (SC2, Tier 1) + D-01 | T-55-04 | invariant bounds hold for all six default cases (`front_idx==0`, `1e9<R̄<1e11`, `‖F_grav‖` O(1), min-sep `≫ eps_soft`); `DEFAULT_CASES` are exactly the six audited rows | unit (parametrized) | `pytest tests/phase55/test_architecture_characterization.py -k "invariant_bounds or default_cases_are" -x -q` | ✅ exists | ✅ green |
| 55-01-T2 | 55-01 | 1 | INST-04 boundary edge | T-55-04 | `causal_weights[0]==1.0`; `w_2..w_16` equal the **dtype-derived** clamp floor from `resolve_causal_clip_facts` (never a literal, never the float32 value); the strict `w>0.5` predicate excludes `0.5`, includes `0.5+1ulp`, and returns the `-1` sentinel when nothing exceeds it | unit (synthetic + live) | `pytest tests/phase55/test_architecture_characterization.py -k "clamp_floor or front_idx" -x -q` | ✅ exists | ✅ green |
| 55-01-T2 | 55-01 | 1 | INST-04 precision edge | — | the even-`n_col` median convention is `numpy.median` (mean of the two central order statistics), documented in the module docstring and every result's `median_convention`; the Frobenius norm convention is confirmed live by the `R̄ == ‖a′‖²/3` identity across all six rows | unit (synthetic + live) | `pytest tests/phase55/test_architecture_characterization.py -k "median_convention or norm_convention" -x -q` | ✅ exists | ✅ green |
| 55-01-T3 | 55-01 | 1 | INST-04 (SC3) | T-55-03, T-55-05 | reported `R̄`, causal weights and derivative norms move in lock-step with a mutated trainer primitive (mutation proof, not an import check); the two prohibition guarantees the Phase-38 exclusion costs are re-homed locally | unit (mutation + AST) | `pytest tests/phase55/test_architecture_characterization.py -k "derives_from_trainer or global_default_mutation or v1_3_era" -x -q` | ✅ exists | ✅ green |
| 55-02-T2 | 55-02 | 2 | INST-04 (D-02 enabler) | T-55-11 | the new probe is excluded from the Phase-38 prohibition glob by one documented entry; every other module's assertions are unchanged | regression (existing suite) | `pytest tests/phase38/test_prohibitions.py tests/phase39/test_prohibitions.py -q` | ✅ exists | ✅ green |
| 55-02-T3 | 55-02 | 2 | INST-04 (SC1/D-02) | T-55-07 | zero-argument invocation reproduces the six audited rows; `--cases-config` drives an arbitrary case list; a malformed entry raises `ValueError` naming the field before any directory is allocated | unit + CLI contract | `pytest tests/phase55/test_architecture_characterization.py -k "zero_argument_cli or cases_config" -x -q` | ✅ exists | ✅ green |
| 55-02-T3 | 55-02 | 2 | INST-04 (SC2 re-derivability) | T-55-06, T-55-08, T-55-09 | `raw.json`'s top-level keys equal the pinned allowlist and its provenance carries argv, command, git sha + availability, worktree dirty flag, Torch/NumPy versions, timestamp, convention and clip facts; an evidence root inside `simulation_data/` is rejected; concurrent runs get distinct directories | integration (CLI subprocess) | `pytest tests/phase55/test_architecture_characterization.py -k "provenance_evidence or simulation_data or non_overwriting" -x -q` | ✅ exists | ✅ green |
| 55-02-T3 | 55-02 | 2 | INST-04 prohibition (no recipe verdict) | — | `main` returns 0 on a completed measurement and non-zero only when the measurement did not complete; the record's key set is fixed so no verdict field can be added silently | unit | `pytest tests/phase55/test_architecture_characterization.py -k exit_code_is_not_a_recipe_verdict -x -q` | ✅ exists | ✅ green |
| 55-03-T2 | 55-03 | 3 | D-03 (capability) | T-55-13, T-55-14 | the ratified 16-bin / 256-per-bin stratification and the arithmetic bin-mean reduction are correct against synthetic arrays with closed-form expectations, including every rejection case | unit (synthetic) | `pytest tests/phase55/test_architecture_characterization.py -k "stratified_bins_synthetic or bin_mean_residuals_synthetic" -x -q` | ✅ exists | ✅ green |
| 55-03-T3 | 55-03 | 3 | D-03 (containment) | T-55-12, T-55-15 | an AST call-graph closure from `run_sweep`/`measure_case`/`main` reaches neither new-structure helper (with a non-vacuity guard); every default-path `causal_physics_loss` call receives exactly `DEFAULT_N_COL` values | unit (AST + call recorder) | `pytest tests/phase55/test_architecture_characterization.py -k "unreachable_from_default_sweep or never_exceeds_sixteen" -x -q` | ✅ exists | ✅ green |
| 55-04-T2 | 55-04 | 4 | INST-04 (SC2, Tier 2) + D-01 | T-55-16 | the full six-row output matches the committed baseline field-for-field at the fixture's recorded relative tolerance; the comparison goes red on a perturbed copy; the on-disk baseline is byte-stable across the whole suite run | unit (regression fixture) | `pytest tests/phase55/test_architecture_characterization.py -k "exact_value_fixture or perturbed_baseline or never_written" -x -q` | ✅ exists | ✅ green |
| 55-04-T3 | 55-04 | 4 | INST-04 (SC2 committed run) | T-55-17, T-55-18, T-55-19 | exactly one committed evidence run under `evidence/probe/` carries the command, tree state and full six-row output; the run is cross-checked against the 2026-08-17 audit §6b table at decade resolution and the comparison is recorded in `55-04-SUMMARY.md` | integration (real CLI run) | `.venv/bin/python -c "import json,glob; ps=sorted(glob.glob('.planning/phases/55-architecture-characterization-probe/evidence/probe/*/raw.json')); assert len(ps)==1; raw=json.load(open(ps[0])); assert len(raw['cases'])==6 and all(c['front_idx']==0 for c in raw['cases']); print('evidence-ok')"` | ❌ W0 | ⬜ pending |
| all | 55-01..04 | 1-4 | INST-04 (SC4) | — | SC4 is a property of the rows above existing and being bound-checked or exact — mutating any reported quantity, the sweep configuration, or the six-row baseline fails the suite | (covered by the rows above) | `pytest tests/phase55/ -q` | ✅ exists | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/phase55/__init__.py` — empty, matches `tests/phase38/`, `tests/phase49/`
- [x] `tests/phase55/test_architecture_characterization.py` — the full suite from the Phase Requirements → Test Map above; no existing test covers any part of this phase
- [x] `pinn/verification/architecture_characterization_probe.py` — the module itself; no existing module implements any part of SC1-SC4
- [x] Committed exact-value fixture JSON (Tier 2, D-01) — generated once the module is correct and reviewed
- Framework install: none — `pytest` already installed in `.venv`

---

## Manual-Only Verifications

*None — all phase behaviors have automated verification per the Phase Requirements → Test Map above.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

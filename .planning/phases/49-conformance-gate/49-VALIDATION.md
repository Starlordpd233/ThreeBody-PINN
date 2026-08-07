---
phase: 49
slug: conformance-gate
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-04
validated: 2026-08-07
---

# Phase 49 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `49-RESEARCH.md` §"Validation Architecture" (2026-08-04).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.1.1 (repo `.venv`) |
| **Config file** | none dedicated — run from repo root with explicit paths and `-q` (same as Phase 48) |
| **Quick run command** | `.venv/bin/python -m pytest -q tests/phase49` |
| **Full suite command** | `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase43/test_summary_enrichment.py tests/phase43/test_summary_honesty.py tests/phase43/test_real_data_smoke_config.py tests/phase46 tests/phase47 tests/phase48 tests/phase49` |
| **Backend probe** | `conda run -n pinn-train python -m pytest -q <target>` — only where MPS/torch-2.12.1 backend behavior is the claim (Phase 48 convention) |
| **Measured runtime** | 13.26s quick (176 passed) · 448.09s full suite (943 passed, 3 skipped, 289 subtests passed) |

---

## Sampling Rate

- **After every task commit:** the directly named `tests/phase49/*.py` file plus the closest impacted existing module (e.g. `tests/phase41/test_guards.py` when `guards.py` changes; `tests/phase40/test_config.py` when `config.py` changes).
- **After every plan wave:** full suite command above.
- **Before `/gsd-verify-work`:** full suite must be green.
- **Max feedback latency:** ~60 seconds (quick run).

**Phase-specific gate (D-16, non-negotiable):** every new guard and every new preflight assertion MUST have a test that drives it to **actually trip**. A green suite with an unreachable failure branch does not satisfy this phase's own discipline — this is the Phase-39 lesson the CONTEXT cites (a check that structurally cannot fail passed three times before it was caught).

---

## Per-Task Verification Map

Task IDs are assigned when plans are written; the requirement→behavior→command mapping below is the binding contract each task inherits. `validate-phase` fills the Task ID / Plan / Wave columns.

| Task ID | Plan | Wave | Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|----------|-----------|-------------------|-------------|--------|
| 49-01-01 | 49-01 | 1 | GATE-01 | Run-start table pass/refusal and artifact-first exit | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k "run_start or state_dict or missing_key or lambda_data"` | ✅ | ✅ green |
| 49-01-02 | 49-01 | 1 | GATE-01 | Stage-boundary assertion and deliberate Stage-2 refusal | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k "stage2 or stage_boundary"` | ✅ | ✅ green |
| 49-01-03 | 49-01 | 1 | GATE-01 | Exact formula, one-ulp, advisory-tier, and warmup checks | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k "formula or ulp or advisory or warmup"` | ✅ | ✅ green |
| 49-02-01 | 49-02 | 2 | GATE-03 | Typed invariant owner slot and fail-closed YAML | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k invariants_config` | ✅ | ✅ green |
| 49-02-02 | 49-02 | 2 | GATE-03 | Invariant A/B and missing-stat HALT branches | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py` | ✅ | ✅ green |
| 49-02-03 | 49-02 | 2 | GATE-03 | Guard-hook causal-statistics wiring | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k guard_hook` | ✅ | ✅ green |
| 49-03-01 | 49-03 | 3 | GATE-03 | Schema-v2 checkpoint payload and provider threading | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_resume.py -k "payload or schema"` | ✅ | ✅ green |
| 49-03-02 | 49-03 | 3 | GATE-03 | Fail-closed restore and stall-window continuity | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_resume.py` | ✅ | ✅ green |
| 49-04-01 | 49-04 | 2 | INST-03 | Register schema, proof resolution, and initial contents | integration/meta | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py` | ✅ | ✅ green |
| 49-04-02 | 49-04 | 2 | GATE-02 | Ordered census pass/block/disagreement/instrumentation | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py` | ✅ | ✅ green |
| 49-04-03 | 49-04 | 2 | GATE-02, INST-03 | Composed preflight and refusal-first evidence | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k "preflight or census"` | ✅ | ✅ green |
| 49-05-01 | 49-05 | 3 | INST-03 | Verbatim conformance projection and EVAL-01 predicate | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k surfaces_in_run_record` | ✅ | ✅ green |
| 49-05-02 | 49-05 | 3 | INST-03 | Valid/malformed/absent/refused summary rendering | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k surfaces_in_run_record` | ✅ | ✅ green |
| 49-06-01 | 49-06 | 4 | GATE-01..03, INST-03 | Real synthetic `main()` ordering seam | e2e | `.venv/bin/python -m pytest -q tests/phase49/test_e2e_seam.py` | ✅ | ✅ green |
| 49-06-02 | 49-06 | 4 | GATE-03 | Owner-ratified `N = 500` enforcement | unit/integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k threshold_nonprovisional` | ✅ | ✅ green |
| 49-06-03 | 49-06 | 4 | GATE-03, INST-03 | Register closure and eligible synthetic summary | e2e | `.venv/bin/python -m pytest -q tests/phase49/test_e2e_seam.py tests/phase49/test_inst03_register.py` | ✅ | ✅ green |
| 49-07-01 | 49-07 | 5 | GATE-01 | Maintained fixtures plus explicit PHYS-05 trip | integration | `.venv/bin/python -m pytest -q tests/phase41/test_train_entrypoint.py::Phys05LaunchGateTests` | ✅ | ✅ green |
| 49-07-02 | 49-07 | 5 | GATE-03 | Null/omitted nested config shapes | regression | `.venv/bin/python -m pytest -q tests/phase49/test_config_null_sections.py tests/phase40/test_config.py` | ✅ | ✅ green |
| 49-07-03 | 49-07 | 5 | GATE-03 | Strict front-index and restored-state validation | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py tests/phase49/test_gate03_resume.py` | ✅ | ✅ green |
| 49-07-04 | 49-07 | 5 | INST-03 | Non-finite and self-contradicting artifact refusal | unit | `.venv/bin/python -m pytest -q tests/phase49/test_preflight_integrity.py` | ✅ | ✅ green |
| 49-07-05 | 49-07 | 5 | INST-03 | Static and executable closed-proof validation | integration/meta | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k proof_test` | ✅ | ✅ green |
| 49-08-01 | 49-08 | 5 | GATE-02, INST-03 | Ordinary setup/probe refusals persist evidence | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k "metadata or census_result or runtime_census"` | ✅ | ✅ green |
| 49-08-02 | 49-08 | 5 | GATE-01 | Scheduler scalar type/domain refusal | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k "cap_scalar or budget_or_warmup or non_finite_scheduler"` | ✅ | ✅ green |
| 49-08-03 | 49-08 | 5 | INST-03 | Append-only resume history and malformed-history refusal | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k "history or malformed_preflight"` | ✅ | ✅ green |
| 49-08-04 | 49-08 | 5 | GATE-02 | Concrete producer-contract re-check | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py` | ✅ | ✅ green |
| 49-08-05 | 49-08 | 5 | GATE-01..03, INST-03 | Phase gate and closeout consistency | regression | `.venv/bin/python -m pytest -q tests/phase49` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/phase49/__init__.py` — phase package marker
- [x] `tests/phase49/test_gate01_table.py` — table assertion pass + Stage-2 refusal + formula equivalence
- [x] `tests/phase49/test_gate02_census.py` — census pass + placeholder-blocks + disagreement-recorded + instrumentation preconditions
- [x] `tests/phase49/test_gate03_invariants.py` — invariant A/B trip + saturation + high-water + record-only + `causal_stats_missing`
- [x] `tests/phase49/test_gate03_resume.py` — invariant-B checkpoint round-trip
- [x] `tests/phase49/test_inst03_register.py` — register schema, proof execution, run-record surfacing, refusal evidence, no `gate_*` collision
- [x] `tests/phase49/test_e2e_seam.py` — D-30 synthetic-source real-`main()` ordering seam
- [x] Shared fixture module not required; each suite uses bounded local dataset-free fixtures.

Framework install: **none needed** — pytest/torch/numpy already present (the same baseline Phase 48 validated).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SCOPE-32 coordination decision | SCOPE-32 / roadmap success criterion 5 | A planner-time repository state check, not a runtime property | Re-run the D-31 evidence check (charter directory contents, absence of `pinn/conformance/`, `git worktree list`) and record the date in the plan |
| Owner ratification of `N` | GATE-03 / D-18 | The choice itself was correctly manual; enforcement is automated after the 2026-08-05 ruling | Closed: owner selected `N = 500`; trip proof and E2E eligibility path are green |

---

## Validation Sign-Off

- [x] All tasks have automated verification or a completed owner/operational checkpoint
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all originally missing references
- [x] No watch-mode flags
- [x] Feedback latency < 60s (13.26s measured quick suite)
- [x] **D-16 trip-coverage:** every guard and every preflight assertion has a test that drives it to fail
- [x] **D-25 register self-defense:** every `closed` entry's `proof_test` resolves and executes green
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-07 — 176 Phase-49 tests passed on the final code tree; the required cross-phase gate recorded 943 passed, 3 skipped, and 289 subtests passed.

## Validation Audit 2026-08-07

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

The audit corrected two stale selector names in the seeded strategy
(`proof_tests_pass` and `refusal_writes_artifact`) by binding the map to current
test nodes. No implementation or test-file gap was found, so no Nyquist auditor
or generated test was required.

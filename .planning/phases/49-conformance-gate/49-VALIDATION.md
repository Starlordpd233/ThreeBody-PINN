---
phase: 49
slug: conformance-gate
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-04
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
| **Full suite command** | `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48 tests/phase49` |
| **Backend probe** | `conda run -n pinn-train python -m pytest -q <target>` — only where MPS/torch-2.12.1 backend behavior is the claim (Phase 48 convention) |
| **Estimated runtime** | ~60s quick · ~5-8 min full suite |

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
| pending | — | — | GATE-01 | Table assertion PASSES for a conformant Stage-0 `ScheduledWeights` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k pass` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-01 | Table assertion **TRIPS** for Stage-2 (no `stage_factory` — D-06's deliberate refusal) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k stage2_fails` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-01 | Literal table equals the spec formula `10.0 ** (k - 4)` for k ∈ {2,3,4} (D-04) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py -k formula` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-01 | Assertion fires at BOTH D-05 sites in a synthetic multi-step run | integration (e2e seam, D-30) | `.venv/bin/python -m pytest -q tests/phase49/test_e2e_seam.py -k table` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-02 | Census PASSES when every D-08 quantity resolves | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k pass` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-02 | Census **BLOCKS** on an injected class-4 placeholder with no waiver | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k placeholder_blocks` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-02 | Census **records, does not adopt**, a `provisional_fields()` disagreement (D-09) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k disagreement` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-02 | Instrumentation preconditions asserted — grad-norm fields + `grad_stats_complete` (D-10) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py -k instrumentation` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | Invariant A **TRIPS HALT** on `w_min <= 0` / non-finite `w_n` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k invariant_a_trips` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | `front_idx == -1` sentinel is a hard invariant-A failure (D-13) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k front_idx_sentinel` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | Invariant B **TRIPS HALT** when the front stalls beyond a configured `N` | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k invariant_b_trips` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | Invariant B does NOT fire at saturation `F_t = N_colloc − 1` (D-14 property ii) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k saturation` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | High-water mark tolerates transient regression 3→2→3 (D-14 property iii) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k high_water` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | Invariant B runs **record-only** (no HALT) when `N` is unset (D-20) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k n_unset_record_only` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | `causal_stats_missing` **TRIPS HALT** when stats absent on an evaluated-physics step (D-16) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py -k stats_missing_trips` | ❌ W0 | ⬜ pending |
| pending | — | — | GATE-03 | Invariant-B state survives a resume via the checkpoint payload (D-17) | integration | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_resume.py` | ❌ W0 | ⬜ pending |
| pending | — | — | INST-03 | Register loads/validates with fail-closed schema checking (D-22) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k schema` | ❌ W0 | ⬜ pending |
| pending | — | — | INST-03 | Every `status: closed` entry's cited `proof_test` currently passes (D-25) | integration/meta | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k proof_tests_pass` | ❌ W0 | ⬜ pending |
| pending | — | — | INST-03 | Open entries surface into `preflight.json` and summary's `conformance` block (D-27) | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k surfaces_in_run_record` | ❌ W0 | ⬜ pending |
| pending | — | — | INST-03 | A refusal writes `preflight.json` FIRST, then exits non-zero (D-27) | integration | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k refusal_writes_artifact` | ❌ W0 | ⬜ pending |
| pending | — | — | INST-03 | No `gate_*` key collision — every new field is `conformance_*`/`preflight_*` (D-28) | unit | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py -k no_gate_collision` | ❌ W0 | ⬜ pending |
| pending | — | — | SCOPE-32 | Charter-landed-deliverable re-check documented with a date (D-31) | manual/operational | N/A — a planner-time check, re-run 2026-08-04; not a runtime test | — | ✅ done |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase49/__init__.py` — phase package marker
- [ ] `tests/phase49/test_gate01_table.py` — table assertion pass + Stage-2 refusal + formula equivalence
- [ ] `tests/phase49/test_gate02_census.py` — census pass + placeholder-blocks + disagreement-recorded + instrumentation preconditions
- [ ] `tests/phase49/test_gate03_invariants.py` — invariant A/B trip + saturation + high-water + record-only + `causal_stats_missing`
- [ ] `tests/phase49/test_gate03_resume.py` — invariant-B checkpoint round-trip
- [ ] `tests/phase49/test_inst03_register.py` — register schema, proof-test-currently-passes, run-record surfacing, refusal-writes-artifact, no `gate_*` collision
- [ ] `tests/phase49/test_e2e_seam.py` — D-30 synthetic-source, real `main()` ordering, few steps, proving the D-05 ordering constraint by execution
- [ ] `tests/phase49/_fixtures.py` (optional) — dataset-free fixtures following `tests/phase40/_fixtures.py`'s `_StubSource` / `make_stub_split_sources` shape

Framework install: **none needed** — pytest/torch/numpy already present (the same baseline Phase 48 validated).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SCOPE-32 coordination decision | SCOPE-32 / roadmap success criterion 5 | A planner-time repository state check, not a runtime property | Re-run the D-31 evidence check (charter directory contents, absence of `pinn/conformance/`, `git worktree list`) and record the date in the plan |
| Owner ratification of `N` | GATE-03 / D-18 | Reserved to the owner by GAP-45-04 and the roadmap owner-checkpoint list; no agent may select it (D-21) | Surface the D-19 evidence packet; until `N` is set, invariant B is record-only and `eval01_precondition_i = false` (D-20) |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] **D-16 trip-coverage:** every guard and every preflight assertion has a test that drives it to fail
- [ ] **D-25 register self-defense:** every `closed` entry's `proof_test` runs in CI
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

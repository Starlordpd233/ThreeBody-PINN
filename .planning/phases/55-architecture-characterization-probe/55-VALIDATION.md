---
phase: 55
slug: architecture-characterization-probe
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
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

Task IDs are assigned by the planner; this table is a requirement-level seed populated from `55-RESEARCH.md`'s "Phase Requirements → Test Map" and finalized once PLAN.md tasks exist.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | TBD | INST-04 (SC1) | — | reports all 7 quantities over a configurable sweep, no data/optimizer/training step | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_measure_case_reports_all_seven_quantities -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | INST-04 (SC1/D-02) | — | zero-arg invocation reproduces the six audited cases; `--cases-config` drives arbitrary cases | unit + CLI contract | `pytest tests/phase55/test_architecture_characterization.py -k test_default_cases_and_custom_config -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | INST-04 (SC2, Tier 1) | — | invariant bounds hold for all six default cases (`front_idx==0`, `R̄` band, `‖F_grav‖` O(1), min-sep `≫ eps_soft`, clamp-floor pin) | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_invariant_bounds_six_cases -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | INST-04 (SC2, Tier 2) | — | full six-row exact-value fixture matches committed JSON at tight relative tolerance | unit (regression fixture) | `pytest tests/phase55/test_architecture_characterization.py -k test_exact_value_fixture -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | INST-04 (SC2) | — | re-derivable evidence: committed JSON/summary carries command, git tree state, full six-row output | integration | `pytest tests/phase55/test_architecture_characterization.py -k test_cli_writes_provenance_evidence -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | INST-04 (SC3) | — | causal-weight/AD calls are literal `pinn.loss_catalog`/`pinn.physics_residual` calls, not a parallel reimplementation | unit (source-level) | `pytest tests/phase55/test_architecture_characterization.py -k test_derives_from_trainer_implementation -x` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | D-03 | — | 16-bin/256-per-bin stratified/bin-mean helpers are correct against synthetic arrays; never wired into the six-case default sweep | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_stratified_bins_synthetic -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase55/__init__.py` — empty, matches `tests/phase38/`, `tests/phase49/`
- [ ] `tests/phase55/test_architecture_characterization.py` — the full suite from the Phase Requirements → Test Map above; no existing test covers any part of this phase
- [ ] `pinn/verification/architecture_characterization_probe.py` — the module itself; no existing module implements any part of SC1-SC4
- [ ] Committed exact-value fixture JSON (Tier 2, D-01) — generated once the module is correct and reviewed
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

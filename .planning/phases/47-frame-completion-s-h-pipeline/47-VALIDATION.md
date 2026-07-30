---
phase: 47
slug: frame-completion-s-h-pipeline
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-29
---

# Phase 47 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

Seeded by `/gsd-plan-phase 47` from `47-RESEARCH.md` §Validation Architecture.
Task IDs are bound when the plan set lands; requirement-level coverage is fixed here.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.1.1, collecting `unittest.TestCase`-style classes (project convention — `tests/phase46/test_pairing_repair.py:12,80,198`) |
| **Config file** | none dedicated — no `pytest.ini` / `[tool.pytest]` at repo root; pytest runs with defaults |
| **Quick run command** | `.venv/bin/python -m pytest tests/phase47/ -q -rs` |
| **Full suite command** | `.venv/bin/python -m pytest tests/phase41/ tests/phase42/ tests/phase43/ tests/phase46/ tests/phase47/ -q` |
| **Estimated runtime** | ~60 seconds (dataset-free synthetic fixtures; no Brutus corpus load, no training) |

**Known baseline:** 12 pre-existing environmental failures in `tests/phase43/` are a
documented baseline (`46-10-SUMMARY.md:105,108`), not regressions introduced by this phase.
Do not chase them; do not let them mask a new failure either — compare counts, not just green/red.

---

## Sampling Rate

- **After every task commit:** Run the targeted file, e.g. `.venv/bin/python -m pytest tests/phase47/test_conf09_frame_completion.py -q -rs`
- **After every plan wave:** Run `.venv/bin/python -m pytest tests/phase46/ tests/phase47/ -q -rs`
- **Before `/gsd-verify-work`:** Full suite command above must be green modulo the documented `tests/phase43/` baseline
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

Requirement-level map (task IDs bound at execution; every row must resolve to a task
`<verify>` block in the plan set).

| Req / Decision | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| D-04 | 47-01 | 1 | CONF-09 | — | N/A | unit/regression | `pytest tests/phase47/test_conf09_frame_completion.py::test_ic13_invariance -x` | ❌ W0 | ⬜ pending |
| D-02 | 47-01 | 1 | CONF-09 | — | N/A | unit | `pytest tests/phase47/test_conf09_frame_completion.py::test_velocity_identity -x` | ❌ W0 | ⬜ pending |
| D-01/D-05 | 47-01 | 1 | CONF-09 | — | N/A | unit | `pytest tests/phase47/test_conf09_frame_completion.py::test_ratified_frame_is_coherent -x` | ❌ W0 | ⬜ pending |
| D-08 | 47-01 | 1 | CONF-09 | — | N/A | regression (train-free) | `pytest tests/phase47/test_conf09_frame_completion.py::test_gate_metric_near_invariance -x` | ❌ W0 | ⬜ pending |
| D-06 | 47-01 | 1 | CONF-09 | — | N/A | unit (corrected in place) | `pytest tests/phase46/test_pairing_repair.py -x -q -rs` | ✅ | ⬜ pending |
| D-09/D-10 | 47-02 | 2 | CONF-02 | — | N/A | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_uabs0_is_absolute_value -x` | ❌ W0 | ⬜ pending |
| D-12/D-13 | 47-02 | 2 | CONF-02 | — | N/A | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_median_train_split_only -x` | ❌ W0 | ⬜ pending |
| D-17 | 47-02 | 2 | CONF-02 | — | fail-closed refusal, no fallback floor | unit/fail-closed | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_s_h_fails_closed -x` | ❌ W0 | ⬜ pending |
| D-15/D-16/D-18 | 47-02 | 2 | CONF-02 | — | re-validate persisted value on load | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_metadata_roundtrip_revalidates -x` | ❌ W0 | ⬜ pending |
| D-19/D-20/D-21 | 47-03 | 3 | CONF-03 | — | N/A | unit (assembly boundary) | `pytest tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_assembly_value -x` | ❌ W0 | ⬜ pending |
| assumption-delta companion invariant | 47-03 | 3 | CONF-03 | T-47-08 | every anchor sees one `eps_h`; goes red if per-anchor scaling returns | unit (invariant) | `pytest tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_uniform_across_anchors -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase47/__init__.py` — new test package
- [ ] `tests/phase47/test_conf09_frame_completion.py` — CONF-09 (D-01, D-02, D-04, D-05, D-08)
- [ ] `tests/phase47/test_conf02_s_h_pipeline.py` — CONF-02 (D-09..D-18)
- [ ] `tests/phase47/test_conf03_eps_h_wiring.py` — CONF-03 (D-19..D-21)
- [ ] `tests/phase46/test_pairing_repair.py` — correction of the superseded pairing assertions (D-06); existing file, **two** methods affected:
  - `test_resident_positions_velocities_and_masses_share_one_body_order` — `_resident_fixture`'s independent oracle extended to apply the rotation gauge and `D`/`V` scaling
  - `test_resident_trajectory_is_not_rotation_gauged_or_globally_scaled` — four `assertFalse(np.allclose(...))` assertions flipped to exact equality, and the method **renamed** to `test_resident_trajectory_is_rotation_gauged_and_globally_scaled`
  - Left byte-unmodified: `test_resident_trajectory_preserves_com_and_zero_momentum_gauge`, `test_admission_keys_snapshot_counts_and_folder_accounting_are_unchanged`, and every `PreprocessingPairingSeamTests` method. Exactly two failures are expected pre-correction; a third is a finding to fix, not to skip.

Framework install: none needed — pytest, numpy, torch already present in `.venv`.

---

## Manual-Only Verifications

**Owner ruling (2026-07-30, Option B):** Phase 47 verifies the complete production
pipeline without launching training. It does not require a real
`run_dir/training_metadata.json`, does not add a zero-step/setup-only real-data
emission path, and does not STOP when no real run artifact exists. Phase 50's first
authorized Stage-0 setup/run produces and reports the first authoritative real-corpus
`S_H`, `ε_H`, and `N_train`; that is deliberate routing, not missing Phase 47 evidence.

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| The permitted one-shot CONF-01 re-probe as a regression check that residency equals the canonical preprocessing output (D-22) | CONF-09 | Runs the probe instrument over the full 1,651-trajectory corpus; not a unit test, and explicitly capped at exactly one run by SCOPE-29 | Run the unchanged probe once, record `identity_scaled` and `first_diverging_step`. **Record only.** `identity_scaled` becomes true by construction — this is no longer a frame test and MUST NOT be presented as a new CONF-01 verdict, nor may its numbers steer implementation. |
| Training-metadata field visibility and relationship are proven, and authoritative real values are routed explicitly | CONF-02 / CONF-03 | Numeric calculation, persistence, loading, fail-closed behavior, and loss wiring are automated; manual closure checks that summaries do not mislabel deterministic fixture values as real-corpus evidence and preserve the Phase 50 handoff | Run `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_metadata_roundtrip_revalidates tests/phase47/test_conf02_s_h_pipeline.py::test_resume_recompute_refuses_mismatch tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_assembly_value tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_uniform_across_anchors -q -rs`. Confirm the deterministic artifact exposes `n_train`, `s_h`, and `eps_h`, enforces `eps_h == energy_floor_factor * s_h`, re-validates on load, and passes the exact validated scale into the loss. Then confirm `47-02-SUMMARY.md` and `47-03-SUMMARY.md` state that Phase 50's first authorized Stage-0 setup/run will produce/report the first authoritative real-corpus values; no Phase 47 real-value row is required. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

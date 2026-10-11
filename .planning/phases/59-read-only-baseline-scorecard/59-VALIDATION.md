---
phase: "59"
slug: "read-only-baseline-scorecard"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-11"
---

# Phase 59 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> It is seeded from `59-RESEARCH.md` "Validation Architecture". The planner
> binds each row to a task ID.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (`TestCase` classes; also runnable under `.venv/bin/python -m pytest`, as a convenience only) |
| **Config file** | none. New package `tests/phase59/` (Wave 0) |
| **Quick run command** | `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest tests.phase59.<module> -v` |
| **Full suite command** | `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest discover -s tests/phase59 -p 'test_*.py' -v` |
| **Adjacent regression** | `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest tests.phase39.test_prohibitions tests.phase39.test_splits tests.phase39.test_adapter tests.phase46.test_isolation` (175 tests, about 1.5 s baseline) |
| **Real-corpus re-derivation** | `python -m pinn.verification.<tool> --check` for the census, baselines and survey, plus `python .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py <subcommand>` |
| **Estimated runtime** | unit suite under about 10 s. Corpus re-derivations take seconds to minutes; `τ_L` takes about 4–10 min. DIAG-07 is not re-run by the verifier; its retained JSON is hash-checked. |

---

## Sampling Rate

- **After every task commit:** the task's own test module, plus `tests.phase39.test_prohibitions`.
- **After every plan wave:** the full `tests/phase59` discovery, plus the adjacent regression.
- **Before `/gsd-verify-work`:** the full suite green, every `--check` re-derivation green, and `verify_phase59_evidence.py final` green.
- **Max feedback latency:** about 10 s for unit tests.

---

## Per-Task Verification Map

Requirement-level rows. The planner binds them to task IDs. Threat refs are
bound in the plans' `<threat_model>` blocks.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | 0–1 | D-26/D-35 | test-split exposure | refuses a test-split ID before any path is built; rejects a manifest-hash mismatch; the audit hook blocks a withheld filename; only `split_allowlist.py` names a corpus folder | unit + static | `... tests.phase59.test_split_allowlist`; `tests.phase39.test_prohibitions` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0–1 | D-27 | accidental training | AST scan: no optimizer, `save` or `save_checkpoint` in Phase-59 modules; no `pinn.evaluate` import; subprocess import check | static | `... tests.phase59.test_static_guards` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0–1 | D-37 | — | imports only the stdlib, numpy, torch, yaml and `pinn.*` | static | `... tests.phase59.test_static_guards.ImportSurfaceTests` | ❌ W0 | ⬜ pending |
| TBD | TBD | 1 | FEAS-01 | threshold tampering | the scorecard loads strictly; unknown keys are rejected; SHA-256 stable; thresholds equal the pre-registered golden values | unit | `... tests.phase59.test_scorecard` | ❌ W0 | ⬜ pending |
| TBD | TBD | 1 | FEAS-01 | — | known errors: self (E = 0, h = 1, own `ε_H`); offset; time shift; velocity scaling (eccentric-Kepler fixture); inner-pair-only phase; frame invariance; pair tracking | unit | `... tests.phase59.test_scorer_known_errors` | ❌ W0 | ⬜ pending |
| TBD | TBD | 1 | FEAS-01 | — | tier boundaries, counting rule, decision rule (2 of 3, 12 of 16, branch a), budget rule (still improving, doubling, inconclusive), G1 boundary | unit | `... tests.phase59.test_scorecard_rules` | ❌ W0 | ⬜ pending |
| TBD | TBD | 1 | FEAS-01 / D-30 | — | the scorer never calls the finite-difference gate path | static | `... tests.phase59.test_static_guards.ScorerVelocitySourceTests` | ❌ W0 | ⬜ pending |
| TBD | TBD | 1 | FEAS-01 / SCOPE-42 | — | the scorecard is committed before any census, baseline or survey evidence | procedural | `verify_phase59_evidence.py scorecard-frozen` | ❌ W0 | ⬜ pending |
| TBD | TBD | 2 | FEAS-02 | — | `N_in` on synthetic orbits, including an aliased case; fractional `N_out`; the panel rule's determinism (D-32); gold-base agreement | unit + evidence | `... tests.phase59.test_census`; `... stage0_census --check`; `verify_phase59_evidence.py census` | ❌ W0 | ⬜ pending |
| TBD | TBD | 2 | FEAS-07 | — | Kepler against RK4 at several eccentricities; the `t = 0` identity; unbound gives `NotApplicable`; nearest-neighbour candidates are the Stage-0 training pool only, deterministic | unit + evidence | `... tests.phase59.test_two_kepler`; `... test_nn_copy`; `... baselines --check` | ❌ W0 | ⬜ pending |
| TBD | TBD | 2 | FEAS-08 | — | stage predicates and precedence (D-33); Stage 3 empty; Stage 6 residual; `τ_L` vectorized equals the literal loop; degenerate cases handled; pick rule; non-gating (no trainer import) | unit + static | `... tests.phase59.test_survey`; `... test_static_guards.SurveyNonGatingTests` | ❌ W0 | ⬜ pending |
| TBD | TBD | 2–3 | DIAG-07 | evidence tampering | checkpoint registry: steps asserted, SHA-256 equals the committed retention manifest, `weights_only=True`; share formula on a toy case; per-term gradients against finite differences on a stub; microbatched equals unchunked; G1 boundary; non-interference (parameters bitwise unchanged, no optimizer, no saves, `runs/` hashes unchanged); code-root identity | unit + evidence | `... tests.phase59.test_diag07`; `verify_phase59_evidence.py diag07` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase59/__init__.py` and `tests/phase59/_fixtures.py`: Lagrange and eccentric-Kepler closed-form fixtures, `TinyCorpus` helpers, and a synthetic manifest builder.
- [ ] `tests/phase59/test_split_allowlist.py`, `test_static_guards.py`, `test_scorecard.py`, `test_scorecard_rules.py`, `test_scorer_known_errors.py`, `test_two_kepler.py`, `test_nn_copy.py`, `test_census.py`, `test_survey.py`, `test_diag07.py`.
- [ ] `ALLOWED_CORPUS_READERS` in `tests/phase39/test_prohibitions.py` extended by exactly one module, with a comment.
- [ ] A skeleton of `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py`.
- [ ] Framework install: none (`unittest` is in the stdlib).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The plain-language summaries are readable by a non-specialist owner | FEAS-01/02/07/08, DIAG-07 | Readability is a judgment | Read each evidence summary's opening paragraph; it must say what was measured and what it means without jargon. |
| GAP-59-08 is surfaced to the owner | — | Owner-routed | Confirm the phase report states the finite-difference gate finding and links `59-GAPS.md`. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

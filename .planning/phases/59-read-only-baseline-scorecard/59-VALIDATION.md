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

Requirement-level rows, bound to task IDs by the planner (2026-10-11). Task IDs read
`<plan>-T<task>`. Threat refs are the T-59-NN ids in the plans' `<threat_model>` blocks.
`...` abbreviates `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest`;
the verifier is `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py`,
run with `<home>/miniforge3/envs/pinn-train/bin/python -B`, as are the `--check` modes
(`python -B -m pinn.verification.<module> --check` from the worktree root).

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 59-03-T1, 59-03-T2 | 59-03 | 2 | D-26/D-35 | T-59-01, T-59-04, T-59-05 | refuses a test-split ID before any path is built; rejects a manifest-hash mismatch; the audit hook blocks a withheld filename; only `split_allowlist.py` names a corpus folder; reader output equals, bitwise on TinyCorpus, an oracle composed from the adapter module's per-file seams, without ever constructing the admitted-set adapter (B-1); normalizer recovered within 1e-6 | unit + static | `... tests.phase59.test_split_allowlist tests.phase59.test_production_reference`; `... tests.phase39.test_prohibitions` | ❌ W0 | ⬜ pending |
| 59-03-T3 | 59-03 | 2 | D-27 | T-59-02, T-59-06 | AST scan over every Phase-59 Python file found by glob, tests included (I-5): no optimizer, no checkpoint-write call, no adapter or source builder (B-1, no test exemption), no finite-difference gate path, no `pinn.evaluate`/`pinn.train` import (plus a fresh-subprocess import check), `torch.load(weights_only=True)` only; every detector self-tested | static | `... tests.phase59.test_static_guards` | ❌ W0 | ⬜ pending |
| 59-03-T3 | 59-03 | 2 | D-37 (D-28) | — | imports only the stdlib, numpy, torch, yaml and `pinn.*` | static | `... tests.phase59.test_static_guards.ImportSurfaceTests` | ❌ W0 | ⬜ pending |
| 59-01-T1, 59-01-T2 | 59-01 | 1 | FEAS-01 | T-59-03, T-59-10 | the scorecard loads strictly; unknown keys are rejected at every depth; SHA-256 pinned in the loader; thresholds equal the pre-registered golden values | unit | `... tests.phase59.test_scorecard` | ❌ W0 | ⬜ pending |
| 59-02-T1, 59-02-T2 | 59-02 | 2 | FEAS-01 | — | known errors: self (E = 0, h = 1, own `ε_H`); offset; time shift; velocity scaling (eccentric homographic fixture) with the rigid-rotation vacuity guard; inner-pair-only phase; frame invariance | unit | `... tests.phase59.test_scorer_known_errors` | ❌ W0 | ⬜ pending |
| 59-01-T2 | 59-01 | 1 | FEAS-01 | — | tier boundaries, counting rule, decision rule (2 of 3, 12 of 16, branch a), budget rule (still improving, doubling, inconclusive), polish stop and result rules, G1 boundary | unit | `... tests.phase59.test_scorecard_rules` | ❌ W0 | ⬜ pending |
| 59-02-T3, 59-03-T3 | 59-02 | 2 | FEAS-01 / D-30 | T-59-11 | the scorer never calls the finite-difference gate path; autograd velocity equals `componentwise_du`; parameters and `.grad` untouched; the physics-residual context column equals the trainer's residual over the governed R_ref and never changes a tier (W-2) | static + unit | `... tests.phase59.test_scorer_network` (incl. `ScorerVelocitySourceTests`); `... tests.phase59.test_static_guards.ForbiddenNameTests` | ❌ W0 | ⬜ pending |
| 59-01-T3 | 59-01 | 1 | FEAS-01 / SCOPE-42 | T-59-03 | the freeze record holds the SHA-256 of the scorecard JSON, the rule module and the plain-language document, plus phase_start_head and head_at_freeze, and the committed bytes match it; this runs before `verify_phase59_evidence.py` exists (I-3) | procedural | the Plan 59-01 Task 3 one-liner that prints `FREEZE-RECORD-OK` | ❌ W0 | ⬜ pending |
| 59-04-T1, 59-10-T1 | 59-04, 59-10 | 2, 5 | FEAS-01 / SCOPE-42 | T-59-03 | the four frozen files are committed, clean and unchanged since the freeze commit, and that commit is a strict ancestor of every audit, census, baseline, survey and DIAG-07 evidence file (ancestry check); repeated inside every area check and in `final` (W-1) | procedural | `verify_phase59_evidence.py scorecard-frozen` (59-04-T1); `verify_phase59_evidence.py final` (59-10-T1) | ❌ W0 | ⬜ pending |
| 59-05-T1, 59-05-T2, 59-05-T3 | 59-05 | 3 | FEAS-02 | T-59-01, T-59-13 | `N_in` on synthetic orbits, including an aliased case; fractional `N_out`; the panel rule's determinism (D-32); gold-base agreement; pair tracking on all 2,039 Stage-0 systems; validation rows agreement-only (D-40); reader acceptance (monitor batch bitwise); freeze guard before any read in every mode (W-1) | unit + evidence | `... tests.phase59.test_census`; `stage0_census --acceptance --check`; `stage0_census --check`; `verify_phase59_evidence.py audit --skip-rederive --require-committed`; `verify_phase59_evidence.py census --skip-rederive --require-committed` | ❌ W0 | ⬜ pending |
| 59-08-T1, 59-08-T2, 59-08-T3 | 59-08 | 4 | FEAS-07 | T-59-01, T-59-16, T-59-17 | Kepler against RK4 at several eccentricities; the `t = 0` identity; unbound gives `NotApplicable`; nearest-neighbour candidates are the Stage-0 training pool only, deterministic; D-38 not-applicable record; analytic formula accelerations and the copy's Newtonian accelerations feed the context-only residual column (W-2) | unit + evidence | `... tests.phase59.test_two_kepler tests.phase59.test_nn_copy tests.phase59.test_baselines`; `baselines --check`; `verify_phase59_evidence.py baselines --skip-rederive --require-committed` | ❌ W0 | ⬜ pending |
| 59-06-T1, 59-06-T2, 59-06-T3 | 59-06 | 4 | FEAS-08 | T-59-01, T-59-14 | stage predicates and precedence (D-33); Stage 3 empty; Stage 6 residual; `τ_L` vectorized equals the literal loop; degenerate cases handled; pick rule; non-gating (no trainer import); detached run with a vm_stat preflight and a completion marker (D-41) | unit + static + evidence | `... tests.phase59.test_survey`; `... tests.phase59.test_static_guards.SurveyNonGatingTests`; `dataset_survey --check` (detached); `verify_phase59_evidence.py survey --skip-rederive --require-committed` | ❌ W0 | ⬜ pending |
| 59-07-T1, 59-07-T2, 59-07-T3, 59-09-T1, 59-09-T2, 59-09-T3 | 59-07, 59-09 | 3–4 | DIAG-07 | T-59-02, T-59-03, T-59-05, T-59-08, T-59-18 | checkpoint registry: steps asserted, SHA-256 equals the committed retention manifest, `weights_only=True`; snapshot code identity; share formula on a toy case; per-term gradients equal the trainer's norms; microbatched equals unchunked; G1 boundary and recomputation; non-interference (parameters bitwise unchanged, no optimizer, no saves, `runs/` hashes unchanged); replay proof against every retained RNG state; registry tests write no checkpoint (B-1); detached runs with completion markers and producer hashes (D-41, W-1); the Plan-07 manifest superseded with its files unchanged (I-2) | unit + evidence | `... tests.phase59.test_diag07 tests.phase59.test_diag07_panels`; `verify_phase59_evidence.py diag07 --require all --require-committed`; `verify_phase59_evidence.py guardrails` | ❌ W0 | ⬜ pending |
| 59-04-T1, 59-04-T2, 59-04-T3 | 59-04 | 2 | FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07 (evidence integrity) | T-59-03, T-59-07, T-59-09, T-59-12 | atomic, redacted evidence writes; area manifests; area contracts; independent G1 recomputation; guardrails (retention re-hash, on-disk run sets, attestation zeros); final content check; four-file freeze inside every area check, `--require-committed` ancestry, producer hashes and completion markers (W-1, D-41) | unit + evidence | `... tests.phase59.test_evidence_io tests.phase59.test_evidence_verifier`; `verify_phase59_evidence.py guardrails` | ❌ W0 | ⬜ pending |
| 59-10-T1, 59-10-T2 | 59-10 | 5 | FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07 | T-59-03, T-59-19 | findings page matches the evidence; top-level manifest; full byte re-derivation of audit, census, baselines and survey; DIAG-07 hash-checked; GAP-59-08 section unchanged since phase_start_head and the own-commit gate (W-3) | evidence + procedural | `verify_phase59_evidence.py final` (detached, D-41); the GAP-59-08 and own-commit one-liners in 59-10-PLAN.md; `... discover -s tests/phase59 -p 'test_*.py'` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

There is no separate Wave 0 plan: each test file is created with the module it
tests, in the first task that needs it (tracer tasks and `tdd="true"` tasks), so no
task runs without an automated check. Where each one lands:

- [ ] `tests/phase59/__init__.py` (59-01-T1); `tests/phase59/_fixtures.py`: Lagrange rotation, eccentric homographic, hierarchical circular and dual-frame fixtures (59-02-T1, T2); `tests/phase59/_corpus_fixtures.py`: TinyCorpus plus a synthetic manifest (59-03-T1).
- [ ] `test_scorecard.py`, `test_scorecard_rules.py` (59-01); `test_scorer_known_errors.py`, `test_scorer_network.py` (59-02); `test_split_allowlist.py`, `test_production_reference.py`, `test_static_guards.py` (59-03); `test_evidence_io.py`, `test_evidence_verifier.py` (59-04); `test_census.py` (59-05); `test_survey.py` (59-06); `test_diag07.py` (59-07); `test_two_kepler.py`, `test_nn_copy.py`, `test_baselines.py` (59-08); `test_diag07_panels.py` (59-09).
- [ ] `ALLOWED_CORPUS_READERS` in `tests/phase39/test_prohibitions.py` extended by exactly one module, with a comment (59-03-T1).
- [ ] `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` with every subcommand (59-04-T1..T3), before any real-data evidence is produced (Wave 2).
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

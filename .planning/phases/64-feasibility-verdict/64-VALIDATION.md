---
phase: "64"
slug: "feasibility-verdict"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-10-25"
---

# Phase 64 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> It is seeded from `64-RESEARCH.md` "Validation Architecture". The planner
> binds each row to a task ID.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` under `pinn-train` 3.11.15. `pytest` is not installed |
| **Config file** | None. New package `tests/phase64/`, created in Wave 0 |
| **Quick run command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase64.test_verifier_phase64 -v` (target: at most 30 s) |
| **Full suite command** | The quick command, plus the cheap regression set in "Sampling Rate" |
| **Evidence verifier** | `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py` with modes `inputs`, `numbers`, `derive`, `figure`, `rules`, `frozen`, `charter`, `ruling`, `traceability` and `final`. Each prints its success token on its own line, and `final` prints `PHASE64-VERDICT-OK` last |
| **Reused verifiers** | `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py final` (about 1.3 s) and `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen` and `guardrails` (about 2 s each) |
| **Estimated runtime** | Unit suite under 30 s. The `derive` and `figure` modes take about 5 s on the CPU and must run from the repository root, because `default_data_root()` reads the git common directory from the working directory |

---

## Sampling Rate

- **After every task commit:** Run the quick unit command, plus the one verifier mode the task built, run on the real files.
- **After every plan wave:**
  - Run the quick command, `verify_phase60_evidence.py final`, Phase 59 `scorecard-frozen` and `guardrails`, and the `frozen` mode.
  - Optionally run `tests.phase60.test_verifier_phase60` (32 tests, about 7.4 s) to confirm the borrowed verifier still imports.
  - Do not rely on the generic post-merge gate. It finds no Makefile or pyproject here and passes on `true`.
- **Before `/gsd-verify-work`:** `verify_phase64_verdict.py final` must print `PHASE64-VERDICT-OK` last, and the owner's checkpoint ① decision must be recorded.
- **Max feedback latency:** 30 seconds.
- **Expensive commands, and why they are substituted:**
  - Phase 59 `final` (about 604 s) is not rerun, because its 10 producer modules and two evidence directories have no diff since `4df5d4a8`.
  - The `tests/phase60` discovery (about 13 minutes) is not rerun, because Phase 64 changes no `pinn/` file.
  - If either reason stops holding, run that command once, detached, keeping its full output outside the repo, and record the reason and the elapsed time.

---

## Per-Task Verification Map

The planner replaces `TBD` with task IDs. `$PY` = `<home>/miniforge3/envs/pinn-train/bin/python`. `<E>` = `.planning/phases/64-feasibility-verdict/evidence`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 64-01-T1 | 64-01 | 1 | FEAS-06 | T-64-01, T-64-02, T-64-05 | The handoff is intact and the label re-derives; exactly seven arm directories; nothing that should be absent exists | contract | `$PY -B <E>/verify_phase64_verdict.py inputs` → `INPUTS-OK` | ❌ W0 | ⬜ pending |
| 64-02-T1, 64-02-T2, 64-04-T2, 64-05-T2 | 64-02, 64-04, 64-05 | 2, 4, 5 | FEAS-06, FEAS-10 | T-64-09 | Every quoted number equals its re-derived value, labelled official (MPS float32) or re-derived (CPU float64); from 64-04 (verdict) and 64-05 (charter) every required token appears in its document | contract | `$PY -B <E>/verify_phase64_verdict.py numbers` → `NUMBERS-OK`; `build_phase64_evidence.py numbers --check` → `NUMBERS-CHECK-OK` | ❌ W0 | ⬜ pending |
| 64-02-T1, 64-02-T3 | 64-02 | 2 | FEAS-06 | T-64-06, T-64-07 | The time-constant and along-window facts re-derive from the committed weights, with zero test-split and validation-split opens | integration, real data | `$PY -B <E>/verify_phase64_verdict.py derive` from the repo root → `DERIVE-OK` | ❌ W0 | ⬜ pending |
| 64-03-T1, 64-03-T2 | 64-03 | 3 | FEAS-06 | T-64-07, T-64-08, T-64-10 | The figure's SHA-256 matches its provenance, the regenerated series match, and it contains no host path | integration, real data | `$PY -B <E>/verify_phase64_verdict.py figure` from the repo root → `FIGURE-OK`; `build_phase64_figure.py --check` → `FIGURE-CHECK-OK` | ❌ W0 | ⬜ pending |
| 64-04-T1, 64-04-T2, 64-05-T2 | 64-04, 64-05 | 4, 5 | FEAS-06 | T-64-11, T-64-12 | No GPU, cloud or price wording outside owner quotes, and no home-directory path in the deliverables. The verdict opens in plain language and carries the frozen label, the D-02 sentence, the unranked D-03 candidates and the D-14 milestone name; from 64-05 the charter is scanned too | contract | `$PY -B <E>/verify_phase64_verdict.py rules` → `RULES-OK` | ❌ W0 | ⬜ pending |
| 64-01-T2 (and every wave gate) | 64-01 | 1 | FEAS-06 | T-64-01 | No frozen or sealed path has changed since `1ebb1d9b`; the Phase 60 and 59 cheap checks pass | regression | `$PY -B <E>/verify_phase64_verdict.py frozen` → `FROZEN-OK`; `verify_phase60_evidence.py final` → `PHASE60-EVIDENCE-OK`; Phase 59 `scorecard-frozen`, `guardrails` | partly | ⬜ pending |
| 64-05-T1, 64-05-T2 | 64-05 | 5 | FEAS-10 | T-64-14 | The charter has every required item. Owner quotes are byte-equal to CONTEXT D-06 and D-07. Stages 1–6 are marked open. It covers the `10⁻⁵` choice, GAP-59-08 options A/B/C, the stop-rule text and the routed lines, and the page fits its line limit | contract | `$PY -B <E>/verify_phase64_verdict.py charter` → `CHARTER-OK` | ❌ W0 | ⬜ pending |
| 64-05-T3, 64-06-T3, 64-07-T1, 64-07-T2 | 64-05, 64-06, 64-07 | 5, 6, 7 | FEAS-06, FEAS-10 | T-64-15, T-64-19 | The owner's decision record has exactly one non-empty owner quote and is tracked and clean. Approved edits (the `PROJECT.md` rewrite, any requirement dispositions) are applied only if the record approves them. Before the owner answers, the mode exits 1 with "does not exist" (64-05-T3) | contract plus manual | `$PY -B <E>/verify_phase64_verdict.py ruling` → `RULING-OK` | ❌ W0 | ⬜ pending |
| 64-01-T3 (built), 64-07-T2 (binding) | 64-01, 64-07 | 1, 7 | VER-22 | T-64-03 | Every v2.4 requirement maps to exactly one phase, with no duplicates or orphans, and the stated count agrees everywhere it appears | contract | `$PY -B <E>/verify_phase64_verdict.py traceability` → `TRACEABILITY-OK` | ❌ W0 | ⬜ pending |
| 64-07-T3 | 64-07 | 7 | all | T-64-19 | Every mode is green, approved edits are complete, and the aggregate token is the last line | aggregate | `$PY -B <E>/verify_phase64_verdict.py final` → `PHASE64-VERDICT-OK` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase64/__init__.py` and `tests/phase64/test_verifier_phase64.py`. Each test has a negative control:
  - flip one number in a copy of the verdict;
  - put "rented GPU" outside an owner-quote fence;
  - touch a frozen file in a temporary repository;
  - drop a table row or duplicate a roadmap ID;
  - truncate an owner quote.
  Tests use real object shapes: the frozen `DataContext`, NumPy `ArmData` and real JSON records.
- [ ] `evidence/verify_phase64_verdict.py` (the modes above) and the builder that writes the number manifest and the figure.
- [ ] A read-only smoke of each mode on the real committed files before its tests are written. Phase 60's verifier crashed on first real use twice when mocks had the wrong shapes.
- [ ] The frozen-path list for the `frozen` mode, with a zsh-safe argument-count self-test and a negative control.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The owner's decision (continue, change course or stop) and each charter choice, including whether `10⁻⁵` stays, GAP-59-08 and GAP-64-01 | FEAS-06, FEAS-10 | Only the owner can supply it | 64-06-T2: the blocking checkpoint ① shows the verdict's plain-language section and the pre-filled charter page. The owner's words are recorded verbatim (64-06-T3), and an ambiguous answer is asked again rather than inferred |
| The figure reads correctly: the legend is inside the canvas and the prediction sits near the orbit's average | FEAS-06 | Visual layout errors were caught only by rendering | 64-03-T2: the executor renders the SVG with Quick Look and looks at it before committing; the `figure` mode also checks mechanically that every label lies inside the viewBox; the owner sees the figure at checkpoint ① |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (the one checkpoint task, 64-06-T2, is manual-only by design)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (64-01 creates the verifier and `tests/phase64/` in its first task; no MISSING sentinel is used)
- [x] No watch-mode flags
- [ ] Feedback latency < 30s (to be measured by the executor; the data-dependent tests add about 5 to 10 s)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

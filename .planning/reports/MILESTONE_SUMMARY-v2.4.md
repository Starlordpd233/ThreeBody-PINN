---
status: active
purpose: governance
created: 2026-10-26
milestone: v2.4
retirement_trigger: superseded by the v2.5 closeout summary
---

# Milestone v2.4 — Project Summary

**Generated:** 2026-10-26
**Purpose:** Team onboarding and project review
**Milestone:** v2.4 Stage-0 Feasibility Checkpoint (Phases 59–64), closed 2026-10-26 on its pre-registered exit at Gate G2
**Sources:** `milestones/v2.4-ROADMAP.md`, `milestones/v2.4-REQUIREMENTS.md`, `milestones/v2.4-MILESTONE-AUDIT.md`, `milestones/v2.4-GAPS.md`, the Phase 59/60/64 CONTEXT, SUMMARY, VERIFICATION, RESEARCH and LEARNINGS files, `PROJECT.md`, `STATE.md` and `RETROSPECTIVE.md`

---

## 1. Project Overview

The project trains a curriculum-trained physics-informed neural network (CTL-PINN) to predict three-body orbits, learning from high-precision Brutus simulations. Four earlier milestones (v2.0–v2.3) built and repaired the training stack, but no run had yet shown the network learning an orbit. v2.4 asked the owner's question directly: **can this approach learn three-body motion at all?**

It answered with the cheapest experiments that could settle it, in a fixed order, each scored in physical units against a scorecard frozen before any of them ran:

1. one Stage-0 system with the answer shown (data only, the "representation ceiling");
2. the same systems learned from the physics;
3. a 16-system family;
4. the full Stage-0 corrected control.

**What happened.** Rung 1 failed on all three panel systems (Tier 0), so Gate G2 fired. A pre-registered sweep of the first-layer frequency `first_omega_0` (60, 120, 240, 480) rescued nothing. The ladder stopped there, as its rules required. Phases 61–63 (rungs 2–4 and their preparation) were **skipped, not failed**, and the milestone went straight to the verdict.

**The verdict** is the frozen rule's `RETHINK-REPRESENTATION`. Independent verification found that every trained network had learned only each body's average position, a near-constant prediction that scores the same tier as a no-learning baseline. At owner checkpoint ① the owner replied "let's change course". The next milestone, v2.5, opens with the `trainex-r5` research round to explain that result before any new long training.

**Boundaries kept:** Stage 0 only; no graded run; the single held-out evaluation still unspent; no test-split file opened; all computation on the owner's Mac (Apple M5 Pro, 24 GB).

## 2. Architecture & Technical Decisions

v2.4 built verification tooling, not new model code. The production network (12 layers × 256, SIREN, 14-D input `[τ, IC₁₃]`) was used as locked.

- **Decision:** A scorecard frozen before any result, with a strict SHA-256 loader and pre-registered rule functions (`pinn/verification/feasibility_scorecard.py`, `59-SCORECARD.md`).
  - **Why:** pre-registration (SCOPE-42) is only checkable if the freeze commit precedes every result.
  - **Phase:** 59
- **Decision:** Score in physical units: position error including the inner pair, the valid-horizon fraction and the gate's own `ε_H`, on tiers. Loss values are context, not scores.
  - **Why:** the only accuracy measured in physical units before v2.4 was the energy gate: v2.0's held-out `ε_H = 237.2`, and generation 7's validation `ε_H` rising while its loss fell.
  - **Phase:** 59 (D-01..D-11)
- **Decision:** Compare every score with comparison points (the two-Kepler formula, a nearest-neighbour copy). A system counts only at Tier ≥ 1 **and** below the formula.
  - **Why:** a "go" that a textbook formula already achieves is not evidence of learning.
  - **Phase:** 59 (D-05, D-15..D-17)
- **Decision:** One allowlisted reader that refuses held-out files before a path exists, with open attestation proven in a subprocess.
  - **Why:** the boundary is proven, not asserted.
  - **Phase:** 59 (D-35)
- **Decision:** A learnability harness built from the trainer's own losses, with the frozen L-BFGS polish, a CPU float64 cross-check, a closed 42-arm catalog and a run protocol SHA-pinned to 33 modules, admitted only when nothing has drifted (`pinn/verification/learnability_*.py`).
  - **Why:** "never fail an experiment for the wrong reason". Every arm runs the ratified recipe, and the protocol is sealed before any real arm.
  - **Phase:** 60 (D-01..D-11)
- **Decision:** The scorer's MPS fix enters as exactly one governed successor digest.
  - **Why:** the Phase 59 evidence pins the scorer's hash.
  - **Phase:** 60 (D-09)
- **Decision:** Weights for both scored states of every arm are committed in plain git, and long arms run detached under a supervisor with governed pause and resume (`scripts/phase60_run_control.py`, `scripts/phase60-pause.sh`, `-resume.sh`, `-power-guard.sh`).
  - **Why:** every result can be re-scored from the committed weights, and multi-hour arms must stop and resume cleanly.
  - **Phase:** 60 (D-10)
- **Decision:** Every number in the verdict is a labelled, sourced manifest entry (`evidence/numbers.json`, 365 entries), re-derived by a verifier that shares no code with the producer.
  - **Why:** agreement between independent implementations is evidence; shared code would only agree with itself.
  - **Phase:** 64 (D-01..D-05)
- **Decision:** Cost on this Mac only: measured hours plus a labelled for-scale figure.
  - **Why:** standing owner rule (PROJECT.md Constraints).
  - **Phase:** 64 (D-05, D-06)

## 3. Phases Delivered

| Phase | Name | Status | One-Liner |
|-------|------|--------|-----------|
| 59 | Read-Only Baseline & Scorecard | Complete 2026-10-17, verified (6/6) | Froze the scorecard, its comparison points, the census and panels, and a survey of all 12,023 training-split records; Gate G1 proceed |
| 60 | Single-System Learnability | Complete 2026-10-23, verified (5/5, independent) | Built and sealed the learnability harness; Rung 1 and the `first_omega_0` sweep all Tier 0; G2 fired, no rescue; stop path to Phase 64 |
| 61 | Conformance & Instrumentation | Skipped at G2 (no rescue), not failed | — |
| 62 | Gates & the Small-Family Rung | Skipped at G2 (no rescue), not failed | — |
| 63 | Corrected Control | Skipped at G2 (no rescue), not failed | — |
| 64 | Feasibility Verdict | Complete 2026-10-26, verified (PASS-WITH-OBSERVATIONS) | The verdict `RETHINK-REPRESENTATION` beside the time-constant evidence, the one-page charter, and owner checkpoint ① (`change-course`) |

**Key numbers:**
- The two-Kepler formula reaches Tier 1 on 1 of 1,812 training systems and 0 of 227 validation systems.
- Gate G1: generation 7's physics term supplied 7.19e-07 of the Adam-preconditioned update, so "physics was a passenger".
- Rung 1 on systems 1632, 851 and 4658: E 1.14–1.24 against the 0.10 Tier-1 line, with valid horizon 0.0.
- Seven arms cost 22.378 machine hours; the verdict places the project at Level 1 on the readiness ladder.

## 4. Requirements Coverage

Twelve of the 24 requirements are complete. The milestone audit is `gaps_found` **only** for the twelve requirements of the skipped phases.

- ✅ FEAS-01 scorecard pre-registered and frozen (59)
- ✅ FEAS-02 Stage-0 census and panels (59)
- ✅ FEAS-07 comparison points (59)
- ✅ FEAS-08 whole-dataset survey and predictability envelope (59)
- ✅ DIAG-07 the ruling's read-only experiments on generation-7 checkpoints (59)
- ✅ INST-05 the learnability harness (60)
- ✅ FEAS-03 Rung 1, the supervised ceiling (60)
- ✅ FEAS-04 Rung 2, recorded as skipped: no rescue (60)
- ✅ FEAS-09 hard-stage probes, recorded as skipped: no rescue (60)
- ✅ FEAS-06 the feasibility verdict (64)
- ✅ FEAS-10 the project charter, delivered with every row recorded as the owner left it (64)
- ✅ VER-22 traceability, 24 defined / 24 table / 24 roadmap, re-verified at close (64)
- ⚠️ CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10 (61): skipped at G2, not failed
- ⚠️ GATE-05, FEAS-05 (62): skipped at G2, not failed
- ⚠️ RUN-06, DIAG-08 (63): skipped at G2, not failed

The twelve skipped requirements stay `Pending`. Their label, and whether they carry forward to v2.5, is charter row C-14 (GAP-64-01), which the owner left open.

**Audit verdict:** `gaps_found` (12/24 by the strict gate). Integration: 4/4 wiring checks passed, 0 blockers and 6 warnings. The owner chose an override closeout (`milestones/v2.4-MILESTONE-AUDIT.md`).

## 5. Key Decisions Log

| ID | Decision | Phase | Rationale |
|----|----------|-------|-----------|
| D-01..D-11 (59) | Scorecard forms, tiers, counting rule, budget rule, L-BFGS polish, the G2 sweep grid, cadence, known-error tests, freezing | 59 | Pre-register every reading rule before any result |
| D-12..D-21 (59) | Census population and difficulty measure, panel rule, formula and copy baselines, survey labels and picks (reported, never gating) | 59 | Comparison points and a map of every stage, read-only |
| D-29..D-41 (59) | Post-research revisions: `best.pt` as checkpoint 900, velocity sources for `ε_H`, the dense grid as tier-defining, the G1 formula, corpus access, L-BFGS `max_iter = 50` | 59 | Settle source-silent details before code (GAP-59-01..07) |
| GAP-59-10 / -11 | Owner rulings: accept the IC13 residual of exactly 2⁻²³ as a recorded deviation; read JX-10's 1e-4 in exact decimal units | 59 | Frozen tolerances move only by owner ruling |
| D-01..D-05 (60) | Physics arms keep the ratified Adam cosine; the budget is the 3-hour cap over the measured seconds per step; one ×2 extension | 60 | No recipe change inside a diagnostic (SCOPE-41) |
| D-06 (60) | A physics arm never self-halts on invariant B; it logs the monitor | 60 | Diagnostic runs observe, they do not stop |
| D-09, D-10 (60) | One scorer successor digest; weights committed in plain git | 60 | Keep Phase 59 evidence valid; re-score from weights |
| GAP-60-03 / -09 | Owner rulings: clip in every arm; no pre-answer for a failed confirmation | 60 | Owner decides scope and meaning at the protocol seal |
| D-01..D-04 (64) | State the frozen label side by side with the time-constant evidence; explain the qualifier field; candidate fixes unranked; one figure | 64 | The label is mechanical; the evidence qualifies how to read it |
| D-05, D-06 (64) | Cost measured on this Mac plus a for-scale figure; no GPU routes | 64 | Standing owner rule |
| D-07..D-13 (64) | Charter purpose recorded verbatim (learning plus a proof of concept); pre-filled draft; Stage-0 bar, Stages 1–6 open; budget and stop rule offered | 64 | The owner answers one page at checkpoint ① |
| D-14 (64) | v2.5 committed only to its name and its first phase, `trainex-r5` | 64 | Do not plan past the open questions |
| V-1 | `change-course`; charter rows C-1..C-14 recorded open | 64 | The owner's one reply addressed no charter row |

All 29 v2.4 gaps: 27 resolved with instruction; GAP-59-08 and GAP-64-01 open and owner-routed (`milestones/v2.4-GAPS.md`).

## 6. Tech Debt & Deferred Items

**Open owner decisions (carry forward):**
- **Charter rows C-1..C-14** (`64-CHARTER.md`): definition of done, Stage-0 pass bar, budget, stop rule, the `10⁻⁵` bar, the PROJECT.md rewrite (C-12, C-13) and the skipped requirements' label (C-14).
- **GAP-59-08.** The validation gate and held-out evaluator use finite-difference velocities; even Brutus's exact answer scores ε_H 4.7e-2 to 3.8e-1. This blocks any held-out spend.
- **GAP-56-02.** Still DEFERRED; its home (SPEC-10, Phase 61) was skipped.

**What the records cannot say:** whether the time-constant outcome is a representation limit or an outcome of the fixed recipe (Adam at 1e-3 on a cosine, median clipping, 12 × 256). The sweep varied only `first_omega_0`, and there is one seed per arm.

**Tooling debt:**
- 18 code and test files hardcode the Phase 59/60/64 folder paths, so those folders stay in `.planning/phases/`. Any archival needs a path repair, plus a protocol amendment, because `evidence_io.py` is pinned.
- The three VALIDATION.md files are still `draft` (Nyquist NOT-VALIDATED).
- `tests/phase60` takes about 13 minutes against a 60 s estimate, and the feedback-latency targets of Phases 59 and 64 were missed.
- Paths that exist as tested code but never ran on real data: the rescue/checkpoint-④ route, the continue gate, the R_ref and GATE-04 re-measure, the Rung-2 and probe physics arms, resume, and the verifier's rescue branch.
- `numbers.json` citations carry no per-citation digests (audit W-2).
- `representation_limit_qualifier: false` on the G2 branch means "not evaluated" (audit W-3).

**Lessons the retrospective keeps:**
- Read every score against a no-learning baseline.
- A one-setting sweep cannot separate representation from recipe.
- Run every verifier mode on real artifacts before it gates anything.
- Plan close-time path repairs when code reads planning files.

## 7. Getting Started

- **Read first:** `.planning/phases/64-feasibility-verdict/64-VERDICT.md`, which starts in plain language, then `64-CHARTER.md` (the open owner rows), `60-FINDINGS.md`, `59-FINDINGS.md` and `milestones/v2.4-MILESTONE-AUDIT.md`. The per-phase lessons are in `59-`, `60-` and `64-LEARNINGS.md`.
- **Run the project:** use the `pinn-train` conda environment and run `python -B` from the repository root. There is no build step. Every verifier is a plain script:
  - `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py final`: about 10 s, ends `PHASE64-VERDICT-OK`
  - `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py final`: about 2 s, `PHASE60-EVIDENCE-OK`
  - `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final`: about 10 min, `PHASE59-EVIDENCE-OK`
- **Key directories:**
  - `pinn/verification/`: scorecard, scorer, reader, census, survey, baselines and the learnability harness
  - `.planning/phases/59-*`, `60-*`, `64-*`: evidence, verifiers and the owner-facing pages. These folders stay in place on purpose.
  - `scripts/phase60_run_control.py` and the `phase60-*.sh` pause/resume/power-guard scripts
  - `.planning/milestones/v2.4-*`: the archived roadmap, requirements, audit and gaps
- **Tests:** `python -B -m unittest discover -s tests/phase64 -p 'test_*.py'` (287 tests, about 80 s); `tests/phase59` (319 tests, about 3 min); `tests/phase60` (992 tests, about 13 min). The Phase 64 verifier and `tests/phase60/test_amendment.py` read the archived `milestones/v2.4-REQUIREMENTS.md` and `v2.4-ROADMAP.md` (repointed at close, `5c38a76f`).
- **Where the next work starts:** `/gsd-new-milestone` for v2.5, whose first phase is the `trainex-r5` research round (open-book, diagnosis first), using the External Research Workflow runbook (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`). The eight unranked candidate fixes are in `64-VERDICT.md`. No new long training runs until the round explains the time-constant output.
- **Owner-controlled, not done by agents:** any merge of `milestone/v2.4` into master, and pushing tags `v2.3` and `v2.4`.

---

## Stats

- **Timeline:** 2026-10-09 → 2026-10-26 (18 days)
- **Phases:** 3 complete / 6 total (3 skipped at G2, not failed)
- **Plans / tasks:** 40 / 103
- **Commits:** 237 (`b8632832..v2.4`; 109 docs, 48 feat, 27 test, 19 evidence, 13 fix, 11 plan, 5 verify, 3 spec)
- **Files changed:** 284 (+148,692 / −72): 79 Python files (+58,021 / −9), 55 JSON evidence files (+40,433), 129 Markdown files (+33,958), 3 CSV files (+16,104), and 14 binary weights files
- **Training compute:** 22.378 machine hours on this Mac across seven arms
- **Contributors:** Starlordpd233 (agent-assisted commits)

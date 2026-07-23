# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- ✅ **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (shipped 2026-07-02; 32/32 requirements, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED; FUT-01/FUT-04 routed to the trainex track; archived under [`milestones/v1.6-*`](milestones/))
- ✅ **v2.0 CTL-PINN Training Viability Slice** — Phases 37–43 (shipped 2026-07-23; the project's first **build** milestone / trainex track — Stage-0-first end-to-end training slice from the ratified trainex-r1a decisions; 42/42 requirements Complete; audit `tech_debt` with zero blockers; the sole held-out physics gate rendered an honest **FAIL** (`ε_H = 237.21` vs ≤ 1e-5) and the owner signed **`adjust`** — Stage-0 mechanical slice retained, PLAT-01..07 blocked, physics-gate investigation routed to the next milestone; archived under [`milestones/v2.0-*`](milestones/))
- 🚧 **v2.1 Physics-Gate Investigation & trainex-r2 Research Package** — Phases 44–45 (started 2026-07-23; the separately governed investigation routed by the v2.0 `adjust` verdict — read-only forensics over the retained v2.0 artifacts, then trainex-r2 ERW package assembly; 7 requirements across DIAG/PKG; closes at package delivery — the remedy belongs to the post-resolution-doc milestone)
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

## 🚧 v2.1 Physics-Gate Investigation & trainex-r2 Research Package (Executing)

**Milestone Goal:** Diagnose — from the evidence v2.0 already produced — how and plausibly why the Stage-0 model fails the physics-conservation gate (`ε_H = 237.21` vs ≤ 1e-5, `SCS = 2.375`, 1,500 held-out trajectories), and deliver the trainex-r2 ERW research package so the owner's external research can adjudicate the remedy. This is the "separately governed investigation" the owner-signed `adjust` verdict routed (2026-07-22). The milestone closes at package delivery; the remedy (recipe changes, new training, any new evaluation policy) belongs to the post-resolution-doc milestone — the v1.5/v1.6 package-first rhythm.

**Granularity:** small (2 phases, 7 requirements: 4 DIAG + 1×Phase 44, 3 PKG × Phase 45)
**Coverage:** 7/7 v2.1 requirements mapped (Phase 44: DIAG-01..04; Phase 45: PKG-09..11)
**Branch:** work continues in `.worktrees/trainex`; branch `milestone/v2.1` to be cut from the v2.0 tip at first phase execution (v2.0 precedent — no branch op during setup). Per-plan atomic commits via `scripts/agent-commit`; no protected-branch push; master merge is user-controlled integration.

### Investigation discipline (applies to both phases)

- **Hard boundaries from the verdict (SCOPE-22..26):** no held-out evaluation (budget exhausted; new owner policy required), no new training runs (read-only artifact analysis; a decisive diagnostic run may only be *proposed* as a gap for owner authorization), no framework-spec edits (spec-parameter suspicions become ERW questions), no PLAT-01..07/Stage-1 work, and no remedy selection (owner-routed through ERW).
- **Evidence is what v2.0 retained:** `runs/stage0-pilot-seed42/evaluation/` (receipt/metrics — the sole gate rendering), `runs/stage0-smoke` + `runs/stage0-pilot-seed{41,42,43}` (per-step JSONL, TensorBoard, curriculum/validation records), `milestones/v2.0-phases/43-*/` (calibration, verdict, smoke/pilot evidence), `pinn/STATUS.md`, and the v2.0 milestone audit. The shipped `pinn/` code is read as the factual record of what executed; it is not edited.
- **STOP-protocol spirit:** any source-silent physics-adjudication call surfaced by the forensics (e.g. "is this loss weighting *wrong* per spec intent?") is recorded as a gap and routed to the owner/ERW — never decided inline. Gap index for the milestone: `.planning/milestones/v2.1-GAPS.md` (created on first gap, standing trigger).
- **Re-derivability:** every analysis lands with its script and inputs pinned (commit hashes / file digests) so any number in the diagnosis report can be regenerated.

## Phases

**Phase Numbering:** integer phases 44–45 continue from v2.0's Phase 43 (numbering does not reset). Decimal phases reserved for urgent insertions.

- [ ] **Phase 44: Physics-Gate Forensics** — Read-only diagnosis from retained v2.0 artifacts: per-trajectory ε_H distribution over the 1,500 held-out trajectories (preserved `metrics.json`; evaluator NOT re-run), five-term loss decomposition across the smoke + three pilot runs (dominance, warmup-spike attribution, PHYS-05 interaction), three-seed divergence characterization (budget-limited descent vs recipe instability, with the Phase 38 overfit rung as machinery-integrity control), culminating in `44-DIAGNOSIS.md` — a hypothesis-ranked, evidence-cited diagnosis that explicitly abstains from remedy selection. (DIAG-01..04)
- [ ] **Phase 45: trainex-r2 ERW Package Assembly** — The research package under `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` per the canonical ERW runbook: annotated document list with commit-pinned snapshots (44-DIAGNOSIS.md, receipt/metrics, 43-CALIBRATION/43-VERDICT, relevant locked spec sections, run-evidence excerpts), neutrally framed research questions (budget/steps, warmup + LR schedule, loss weighting, Stage-0 curriculum pacing, evaluation-policy), claims register (verified facts vs agent hypotheses), and delivery note. Delivery opens the external research gate and closes the milestone. (PKG-09..11)

## Phase Details

### Phase 44: Physics-Gate Forensics

**Goal**: The failure is characterized, not guessed at: the held-out ε_H distribution, the training-time loss composition, and the seed band are each quantified from retained artifacts, and a hypothesis-ranked diagnosis report gives the owner (and the trainex-r2 researchers) an evidence map of candidate causes — with the remedy deliberately left open.
**Depends on**: v2.0 archive (complete). Ungated — first v2.1 phase.
**Requirements**: DIAG-01, DIAG-02, DIAG-03, DIAG-04
**Success Criteria** (what must be TRUE):

  1. A per-trajectory ε_H analysis over all 1,500 held-out trajectories exists, derived solely from the preserved evaluation artifacts (no evaluator invocation — checked against SCOPE-22), and states with numbers whether failure is uniform or tail-driven (DIAG-01).
  2. A per-step, per-term loss decomposition across `stage0-smoke` and all three pilot seeds identifies which of the five loss terms dominates in which step ranges and attributes the warmup spike (~3.7e9) to specific terms, accounting for the PHYS-05 scheduled weights (DIAG-02).
  3. The three-seed characterization distinguishes budget-limited descent from recipe instability with cited per-seed evidence (validation trends, spreads), and cites the Phase 38 single-trajectory overfit rung as the machinery-integrity control (DIAG-03).
  4. `44-DIAGNOSIS.md` ranks ≥4 candidate causes, each with supporting AND contradicting evidence citations, explicitly abstains from remedy selection, and routes any source-silent adjudication call to a gap register entry rather than deciding it (DIAG-04).
  5. Every reported number is re-derivable: analysis scripts + pinned inputs retained in the phase evidence directory.

### Phase 45: trainex-r2 ERW Package Assembly

**Goal**: The owner can hand the package to external research as-is: it contains everything needed to adjudicate the training-recipe questions (including the forensics evidence map), poses the questions neutrally, and separates verified fact from agent hypothesis — so the returning resolution doc can serve as a clean candidate verdict source for the next milestone.
**Depends on**: Phase 44 (the diagnosis report is the package's centerpiece).
**Requirements**: PKG-09, PKG-10, PKG-11
**Success Criteria** (what must be TRUE):

  1. The package exists under `framework-specs/trainex-r2/` following the ERW runbook structure, with commit-pinned snapshots of every included document (PKG-09).
  2. Research questions are posed neutrally — no recommended answer — covering at minimum budget/steps, warmup + learning-rate schedule, loss weighting, Stage-0 curriculum pacing, and the evaluation-policy question (PKG-10).
  3. The claims register separates v2.0-verified facts (with citations) from unverified agent hypotheses (the DIAG-04 rankings, labeled as analysis); the delivery note records contents, provenance, and expected return format (individual reports → one consolidated resolution doc, v1.4/v1.5/v1.6 precedent) (PKG-11).
  4. The two carried-forward todos (`trainex-r1-research-handoff` r1b relationship, `d-06-static-epsilon-sensitivity-check` inclusion) are surfaced to the owner as package-scope questions at assembly — decided by the owner, not the agent.
  5. Milestone closes at delivery with all SCOPE-22..26 boundaries intact: no evaluation, no training, no spec edits, no remedy chosen.

## Progress

**Execution Order:** 44 (forensics) → 45 (package assembly, consumes the diagnosis). No external gate inside v2.1; the external research gate OPENS at v2.1 close (the returning resolution doc gates the NEXT milestone, not this one).

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 44. Physics-Gate Forensics | v2.1 | 0/? | Not started | - |
| 45. trainex-r2 ERW Package Assembly | v2.1 | 0/? | Not started | - |

---
*v2.1 created 2026-07-23 (`/gsd-new-milestone`, roadmap generated inline — v2.0 precedent; no research spawn, since the milestone analyzes internal artifacts and the ERW package is the research vehicle). 2 phases (44–45) continuing numbering from v2.0's Phase 43; 7/7 requirements mapped (DIAG-01..04 → 44, PKG-09..11 → 45). Grounded in the owner-signed `adjust` verdict and the v2.0 archive; scope boundaries SCOPE-22..26 are hard constraints. v2.0 archived under [`milestones/v2.0-*`](milestones/) (roadmap, requirements, audit, phase dirs).*

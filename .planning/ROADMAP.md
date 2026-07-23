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

---
*v2.0 archived 2026-07-23 (`/gsd-complete-milestone`): full phase details, per-phase success criteria, and the progress table live in [`milestones/v2.0-ROADMAP.md`](milestones/v2.0-ROADMAP.md); requirements in [`milestones/v2.0-REQUIREMENTS.md`](milestones/v2.0-REQUIREMENTS.md); audit in [`milestones/v2.0-MILESTONE-AUDIT.md`](milestones/v2.0-MILESTONE-AUDIT.md); phase directories in `milestones/v2.0-phases/`. Next milestone: v2.1 (physics-gate investigation & trainex-r2 research package) via `/gsd-new-milestone`.*

---
phase: 20
slug: architecture-and-normalization-cleanup
total_gaps: 1
open_gaps: 1
resolved_gaps: 0
deferred_gaps: 0
last_updated: 2026-06-03
governance: "Governed by AGENTS.md CRITICAL GOVERNANCE block: STOP protocol, source-grounding rules, and no-live-code directive for v1.4 spec decisions."
---

# Phase 20 Gap Register

This file records Phase 20 decisions where source materials or process artifacts are silent or ambiguous. Per the CRITICAL GOVERNANCE rule, when such a decision is consequential the agent must stop dependent work, record the gap with full context, update the milestone-wide index, and wait for user instruction before proceeding on the blocked dependency.

Live code in `pinn/` is not a grounding source for v1.4 framework-spec decisions. Phase 20 may mention live-code divergence only in forward-looking hand-off/proof artifacts.

---

## GAP-20-01: Missing evidence/proof vehicle for ARCH-04 raw-vs-bounded `I_norm`

- **Decision point:** Which evidence/proof vehicle governs `ARCH-04`, the requirement that `I_norm` use separate names for the raw inertia descriptor and the tanh-squashed network input? The project has an explicit requirement and roadmap success criterion, but the Phase 16 ledger does not appear to reserve a row, packet, or acceptance-check vehicle for the `I_norm` naming issue (issue-doc D-02) / `ARCH-04`.
- **Where in artifact:** `.planning/REQUIREMENTS.md:50` (`ARCH-04`); `.planning/ROADMAP.md:212` (Phase 20 success criterion 4); `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:17-38` (status table); `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:279-285` (M5 is only `I_3` / `AC-ARCH-03`, not raw-vs-bounded `I_norm`).
- **Task context:** Creating Phase 20 discussion, context, and research artifacts after the user instructed that missing evidence vehicles must be recorded as process-artifact schema gaps instead of invented or attached by convenience.
- **Classification:** process-artifact schema.
- **Source silence:**
  - `.planning/REQUIREMENTS.md:50` requires separate raw and tanh-squashed `I_norm` names, but does not define an evidence packet or acceptance-check vehicle.
  - `.planning/ROADMAP.md:212` requires the reader to distinguish the raw inertia descriptor from the tanh-squashed network input, but does not define how Phase 20 should prove that closure.
  - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:19`, `:28`, `:33`, and `:36-38` reserve Phase 20 vehicles for B-01/B-10, M5, M8, M9, and M10; no row for the `I_norm` naming issue (issue-doc D-02), `ARCH-04`, raw `I_norm`, or tanh-squashed `I_norm`.
  - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:279-285` assigns M5 to the `I_3` normalization map and `AC-ARCH-03`; it does not cover raw-vs-bounded `I_norm`.
  - `pinn_instruction/issues/01-architecture-and-physics-foundations.md:42-62` documents the `I_norm` naming issue (issue-doc D-02) as routine documentation cleanup, but the Phase 16 ledger does not expose a matching Phase 20 vehicle.
  - Directory check on 2026-06-03 found no `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/D-02.md` or `evidence/ARCH-04.md`.
- **Mathematical / engineering grounding:** `I_norm_raw` is a physics/metadata descriptor derived from an inertia tensor ratio. `I_norm_in = tanh(I_norm_raw)` is a bounded network-facing value. They have different domains, semantics, and verification needs. Conflating them can cause downstream agents to treat a bounded input transform as the raw physical descriptor or to close `ARCH-04` without proving that active spec text distinguishes the two. Attaching this to M5 would also conflate two distinct contracts: M5 / `AC-ARCH-03` adjudicates the `I_3` range and input mapping, while `ARCH-04` concerns raw-vs-bounded `I_norm` naming.
- **Agent was tempted to:** Create an `evidence/D-02.md` (issue-doc naming) or `evidence/ARCH-04.md` packet automatically, or attach the work to M5 because both are inertia-related. The user explicitly rejected inventing or attaching by convenience.
- **What the user needs to decide:**
  - (a) Add a Phase 16 ledger row for the `I_norm` naming issue (issue-doc D-02) / raw-vs-bounded `I_norm`, with a named evidence packet and acceptance check for `ARCH-04`.
  - (b) Explicitly expand an existing Phase 16 row to cover `ARCH-04`, naming the row and required proof trail.
  - (c) Approve a Phase 20-local proof vehicle for `ARCH-04` that is not a Phase 16 evidence packet.
  - (d) Defer `ARCH-04` and record that Phase 20 cannot close it.
- **Confidence of impact:** HIGH - `ARCH-04` is an explicit Phase 20 requirement, and without a valid proof vehicle Phase 20 cannot close the raw-vs-bounded `I_norm` contract without inventing process structure.
- **Status:** OPEN
- **Resolution note:**

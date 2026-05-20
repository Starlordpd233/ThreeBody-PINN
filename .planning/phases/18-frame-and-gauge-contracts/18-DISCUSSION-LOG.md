# Phase 18: Frame and Gauge Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `18-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-05-20
**Phase:** 18-Frame and Gauge Contracts
**Mode:** `gsd-discuss-phase 18` with `superpowers:brainstorming` overlay (one question at a time, options with trade-offs)
**Areas discussed:** Preprocessing-contract structure, Phase 19 / M4 boundary, FRAME-02 assertions & AC naming, FRAME-03 sampling edit + Phase 20.5 coordination

**Git governance pre-flight:** Branch state surfaced at session start; user confirmed proceeding on `milestone/v1.4` (the designated v1.4 working branch) before any file mutation.

---

## Area 1 — Preprocessing-contract structure (FRAME-01)

| Option | Description | Selected |
|--------|-------------|----------|
| One consolidated Step 2 | Merge Step 2 + Step 2.5 into a single "Step 2: Unified Preprocessing Pipeline" with sub-steps in pipeline order; canonical ordering moves in from Step 4. Cleanest, matches the resolution doc's "one deterministic transform" intent; biggest diff. | ✓ |
| Reorder steps in place | Keep two headings: Step 2 = frame/gauge transform, Step 2.5 = scaling (relocated). Smaller heading churn; two headings for one pipeline reads less coherently. | |
| You decide | Treat section layout as a presentation choice and let Claude pick. | |

**User's choice:** One consolidated Step 2.
**Notes:** Canonical ordering relocates from Step 4 into the new Step 2.3; stale `canonical_ordering` function removed from Step 4; Phase-17 forward-references satisfied. FRAME-04 3D-Cartesian guard placed at the rotation-gauge sub-step (Claude's discretion). → `18-CONTEXT.md` D-03, D-04, D-05.

---

## Area 2 — Phase 19 / M4 boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Leave the block untouched in Step 4 | Phase 18 moves only the canonical-ordering procedure; the "Mathematical Guarantees" block (with the M4 sentence) stays verbatim in Step 4 for Phase 19. Zero collision; no cross-phase reframing. | ✓ |
| Move the block, flag the M4 sentence | Relocate the whole block to Step 2 + HTML-comment marker. Triggers the cross-phase reframing rule; would require a gap. | |
| Surface as a gap now | Log in 18-GAPS.md + v1.4-GAPS.md as OPEN and wait for instruction. | |

**User's choice:** Leave the block untouched in Step 4.
**Notes:** `ctl_instruction.md:726-743` (incl. the M4 constraint-counting sentence at 732-733) is untouched by Phase 18 — Phase 19/PHYS-06 owns it. Clean phase boundary; no gap required. → `18-CONTEXT.md` D-06.

---

## Area 3 — FRAME-02 assertions & acceptance-check naming

The assertion text itself was not put to a vote — it is grounded (resolution doc §10.2 specifies `assert ||Σ mᵢrᵢ'|| < 1e-12` / `||Σ mᵢvᵢ'|| < 1e-12`; transcribed directly, see `18-CONTEXT.md` D-07). The decision below is acceptance-check naming.

| Option | Description | Selected |
|--------|-------------|----------|
| AC-FRAME-01..04, one per requirement | Mirror Phase 17's AC-IO-01..04: AC-FRAME-01 = findings B-05+M3; 02 = COM/momentum assertions; 03 = sampling reconciliation; 04 = 3D-Cartesian output. Gives Phase 21 a complete index. | ✓ |
| AC-FRAME-01 + AC-FRAME-02 only | Keep AC-FRAME-01 for findings, add one new AC-FRAME-02 for the numeric COM/momentum check; fold 03/04 under AC-FRAME-01. | |
| Keep only AC-FRAME-01 | Strictly within Phase 16's reservation; no new AC names. | |

**User's choice:** AC-FRAME-01..04, one per requirement.
**Notes:** Reserving AC-FRAME-02/03/04 is "new AC names beyond Phase 16 reservations" → logged as GAP-18-01 (process-artifact schema), RESOLVED-WITH-INSTRUCTION. Pass criteria remain Phase 21 VER-01's job. → `18-CONTEXT.md` D-08.

---

## Area 4 — FRAME-03 sampling edit + Phase 20.5 coordination

### 4a — FRAME-03 edit scope

| Option | Description | Selected |
|--------|-------------|----------|
| Both sides, with figures | Hierarchical note (|COM| median ≈9e-3, |P| median ≈3e-2) + quasi-random parallel note; matches FRAME-03's "hierarchical AND quasi-random" wording. | ✓ |
| Hierarchical only, with figures | Hierarchical note with figures; leave quasi-random untouched. | |
| Minimal cross-reference | One terse sentence at step 8; no figures, no quasi-random note. | |

**User's choice:** Both sides, with figures.
**Notes:** → `18-CONTEXT.md` D-09. Magnitude figures are issue-doc-grounded (B-05 row) and corroborated by `simulation_data/Documentation/README.md`.

### 4b — Phase 20.5 coordination

| Option | Description | Selected |
|--------|-------------|----------|
| Confine + log + milestone-index flag | Confine the FRAME-03 edit to the frame sections (not the Sobol formula); log in 18-GAPS.md; one-line heads-up in v1.4-GAPS.md; don't edit Phase 20.5's docs. | ✓ |
| Log in 18-GAPS.md only | Log + mention in CONTEXT.md; no milestone-index entry. | |
| Surface as a gap, you sequence it | Log OPEN and wait for explicit sequencing instruction. | |

**User's choice:** Confine + log + milestone-index flag.
**Notes:** User added a standing directive — for all `sampling_method.md` / FRAME-03 edits, the live algorithms in `simulation_data/` are the source of truth, because the simulation dataset is already generated by those algorithms and is a finished, immutable job (if the markdown disagrees with the code, the code wins). Distinct from the v1.4 `pinn/` no-live-code directive. → `18-CONTEXT.md` D-10, D-11; logged GAP-18-02 (operational coordination), RESOLVED-WITH-INSTRUCTION.

---

## Gray-area selection

At `present_gray_areas`, the user multi-selected all four offered areas (Preprocessing-contract structure, Phase 19 / M4 boundary, FRAME-02 assertions & AC naming, FRAME-03 sampling edit + 20.5 coordination). At the wrap-up the user chose "Ready for context" — no additional gray areas explored.

## Claude's Discretion

- FRAME-04 3D-Cartesian guard — exact placement and wording (placed at the rotation-gauge sub-step).
- Markdown sub-step numbering / formatting inside the consolidated Step 2.
- Plan decomposition — recorded as a suggested ~3-plan split (`18-CONTEXT.md` D-12); planner finalizes. Handled by Phase 17 precedent, not put to a vote.
- `18-CODE-DIVERGENCE.md` — produced following the `17-CODE-DIVERGENCE.md` schema (`18-CONTEXT.md` D-13). Handled by Phase 17 precedent.
- Exact wording of forward/back references; evidence-packet section formatting.

## Deferred Ideas

None — discussion stayed within Phase 18 scope. Items intentionally left to other phases (M4 fix → Phase 19; AC-FRAME numeric execution + pass criteria → Phase 21; SCOPE-05 formalization + Sobol coordinate edit → Phase 20.5; `pinn/` preprocessing rewrite → FUT-01) are recorded in `18-CONTEXT.md` §"Deferred Ideas".

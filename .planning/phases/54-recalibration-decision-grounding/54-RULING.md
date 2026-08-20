---
phase: 54
checkpoint: 1
status: PENDING
created: 2026-08-20
---

# 54-RULING — Checkpoint ① / ② Ruling Record

## Standing

This file is the provenance record of the owner's branch selection at checkpoint ① and of any direct recalibration ruling. Phase 56 reads it as its authorizing source and may not open without it (SCOPE-34).

It is deliberately not the gap register — a ruling is not a gap (D-09) — and deliberately not the delivery note, which carries ERW routing. The gap anchor `GAP-54-01` in `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md` stays `OPEN` until checkpoint ② is discharged.

## Checkpoint ① — the branch

- **Date:** PENDING
- **Owner instruction (verbatim):** PENDING
- **Branch:** PENDING — rule directly, or commission `trainex-r3`. These are the two branches; nothing further is offered.

No comparative assessment of the two branches is offered here. Under SCOPE-34 the branch is the owner's to select, and cost framing at a gate is steering. Two factual lists follow.

**Rule directly:**

- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` is filled with the branch, the date, the verbatim owner instruction, the per-surface disposition, and the SCOPE-38 re-ratification lines.
- Phase 56 then reads that file as its authorizing source.

**Commission trainex-r3:**

- ERW-02 authors `research_package/RESEARCH-AGENT-PROMPT.md` (ERW Rule 7 output contract, Rule 17 premise-challenge mandate, Rule 18 read-only bars).
- The `specs/` snapshot bundle as a single `framework-specs-bundle.md` (Rule 15).
- The Rule-20 live-tree pin in this note.
- `research_results/<agent>-resolution.md` at delivery.
- The Rule-19 per-claim in-repo verification report under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`.
- The consolidated `trainex-r3-resolution-doc.md` (Rule 12).

## Checkpoint ② — the recalibration ruling

The five surfaces appear in the same transcription order the packet's §4.3 uses, and that order carries no precedence, no priority, and no sequencing implication.

| Surface | Where it is specified today | Marker | Disposition |
|---|---|---|---|
| `η_c`, the causal-weight exponent coefficient | `pinn_architecture.md:435` (the `w_n` formula) | Phase 35 contract block at `pinn_architecture.md:445` (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04): "This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`." | PENDING |
| The `R̄` normalization and its reference scale | no normalization is specified anywhere in the spec; `pinn_architecture.md:435` consumes `R̄` unnormalized | none | PENDING |
| `ω₀` / `first_omega_0`, the SIREN initialization scale | `pinn_architecture.md:181` (§2.2: "`first_omega_0` is fixed at `30` and is not scheduled during training.") | the fixed-at-30 sentence at `pinn_architecture.md:181` | PENDING |
| `N_t` / `n_col`, the collocation-point count | `pinn_architecture.md:454` (`n_col=4096`), `pinn_architecture.md:461` (range 2048–4096); current run `pinn/train.py:1033` (`collocation_count=16`) | none of its own; bound to `η_c` by SPEC-06's joint-ratification requirement | PENDING |
| The causal-exponent clip's declared semantics | `pinn_architecture.md:668-671` | the underflow-only purpose at `pinn_architecture.md:668-671`, plus the Phase 35 guard block at `pinn_architecture.md:692` deferring the numeric bound | PENDING |

This section is filled either directly by the owner at checkpoint ① or after `trainex-r3` delivers. In the latter case the round's consolidated decision sheet is a candidate presented for ratification — not the ratification itself.

## Completeness rule (pre-declared)

A ruling that does not dispose of `N_t` / `n_col` is **incomplete**: it leaves SPEC-06's joint-ratification requirement unmet, is routed back to the owner as a gap, and is never completed by an agent choice.

The mechanical reason: `w_n` is an exclusive prefix sum over collocation points, so the exponent moves by roughly 256× between `pinn/train.py:1033`'s `collocation_count = 16` and `pinn_architecture.md:454`'s `n_col = 4096` — and an `η_c` disposition is therefore under-determined without an `N_t` disposition.

## SCOPE-38 re-ratification lines

A changed number without a re-ratified contract is not a legal v2.3 edit. Each block below corresponds to one locked contract the ruling could amend; a block whose contract the ruling does not touch is marked `not amended` rather than deleted.

**Block 1 — the `η_c` Phase 35 contract**

- **Contract marker:** "This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`."
- **Location:** `pinn_architecture.md:445`
- **Superseded ruling:** Phase 35 D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A (LOSS-04; AC-LOSS-04)
- **New decision provenance:** PENDING
- **Re-issued acceptance criterion:** PENDING

**Block 2 — the `first_omega_0` fixed-at-30 sentence**

- **Contract marker:** "`first_omega_0` is fixed at `30` and is not scheduled during training."
- **Location:** `pinn_architecture.md:181`
- **Superseded ruling:** Phase 20 ARCH-01 (locked SIREN initialization; no omega0 scheduler)
- **New decision provenance:** PENDING
- **Re-issued acceptance criterion:** PENDING

**Block 3 — the causal-exponent clip's underflow-only purpose**

- **Contract marker:** "Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed. The causal exponent clip is required only to avoid underflow."
- **Location:** `pinn_architecture.md:668-671`
- **Superseded ruling:** the Phase 35 guard block (numeric bound deferred to FUT)
- **New decision provenance:** PENDING
- **Re-issued acceptance criterion:** PENDING

Note: §2.4's hyperparameter-table row for `first_omega_0` (`pinn_architecture.md:274`, header `:267`) is already routed to Phase 56 by Phase 53's unswept inventory and is outside this file's three blocks.

## Anchor-drift warning (for Phase 56)

`.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` quote the following four anchors, and all four were verified to point at unrelated content in the live tree after Phase 53's `spec(53)` commits shifted the file:

- `pinn_architecture.md:424`
- `pinn_architecture.md:167`
- `pinn_architecture.md:433`
- `pinn_architecture.md:440`

The verified replacements are `pinn_architecture.md:445`, `pinn_architecture.md:181`, `pinn_architecture.md:454`, and `pinn_architecture.md:461`, respectively.

This file does not correct those documents — that edit belongs to the owner or to the Phase 56 plan (54-CONTEXT.md Open Item 5). Any Phase 56 edit must re-derive its anchor by content match rather than trusting a line number.

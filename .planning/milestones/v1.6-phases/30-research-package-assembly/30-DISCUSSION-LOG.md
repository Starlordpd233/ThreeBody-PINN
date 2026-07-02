# Phase 30: Research Package Assembly - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-18
**Phase:** 30-research-package-assembly
**Mode:** `--auto --all` — all gray areas auto-selected; the recommended (precedent-grounded) option chosen by Claude, not interactively ratified by the user. `spec_loaded = true` (`30-SPEC.md`, 6 locked requirements) — only HOW-to-assemble gray areas were generated.
**Areas discussed:** Package location & layout, Document inventory, Consolidation + user checkpoint, Question framing, Resolution-doc skeleton, Claims register, Reports characterization, Delivery & gate-open, simulation_data excerpts

> **STOP-protocol note:** every gray area below is operational / presentation form, grounded in `30-SPEC.md` + the ERW runbook + the v1.5 Phase 23 precedent. No source-silent **semantic** decision arose, so no `30-GAPS.md` entry was created. The semantically-loaded items (the neutral framing of D-04/D-05/D-06 and the `D = 6.694` conflict) are *posed unsettled* per the SPEC — they are not decided here.

---

## Package location & layout

| Option | Description | Selected |
|--------|-------------|----------|
| Co-located `research_reports/03-*/`, single package | Mirror v1.4/v1.5 layout; one package per issue (specwork convention) | ✓ |
| Split into `research_package_a/_b` | ERW rule-10 split | |
| Separate `.planning/` location | Decouple from resolution-doc landing | |

**Choice:** Co-located single package at `framework-revisions/research_reports/03-curriculum-and-training-loop/` (CONTEXT D-01..D-05).
**Notes:** Single package because this is a specwork issue-doc round (issue-01/02 convention), not a build-design foundational round; the rule-10 split targets `trainex`-style rounds. ERW-fixed file set: `DELIVERY-NOTE.md` (never uploaded), `RESEARCH-CONTEXT-MASTER.md`, `RESEARCH-AGENT-PROMPT.md`, `specs/` (commit-pinned). Zero repo paths in uploads.

---

## Document inventory

| Option | Description | Selected |
|--------|-------------|----------|
| SPEC-locked input set, final list locked at execution | issue-03 + 2 intact specs + 2 reports + frozen `sampling_method.md` + v1.5-verified-facts ref | ✓ |
| Minimal set (issue-03 + 2 specs only) | Drop the reports / verified-facts ref | |
| Include `pinn/` live code | Per issue-03's "Canonical" citation | |

**Choice:** SPEC-locked input set; final list locked at execution after the PKG-08 characterization + consolidation checkpoint (CONTEXT D-06..D-08).
**Notes:** `pinn/` excluded (SCOPE-10); issue-03's live-code citations overridden and stated as a hard constraint. Inclusion criterion = a doc enters iff ≥1 issue-03 finding needs it.

---

## Consolidation + user checkpoint

| Option | Description | Selected |
|--------|-------------|----------|
| Consolidate fragments into one context file; surface plan to user first | PKG-05 hard rule; v1.5 D-07 analog | ✓ |
| Ship all fragments standalone (no consolidation) | Skip the single context file | |
| Consolidate without a user checkpoint | Faster, but violates PKG-05 | |

**Choice:** Consolidate scattered fragments into one context file (framework specs never consolidated); **surface the consolidation plan to the user before assembly as a hard gate** (CONTEXT D-09, D-10).
**Notes:** This is a PKG-05 requirement, not a courtesy — the planner must model it as a user checkpoint. The consolidated file is snapshot-class (may keep internal source-path labels); master/prompt stay path-free.

---

## Question framing (PKG-06)

| Option | Description | Selected |
|--------|-------------|----------|
| By issue-03's own section order; neutral framing; verbatim SCOPE-12 preamble | SPEC-locked Round-1 decision | ✓ |
| By downstream contract cluster (Phase 23's D-08 approach) | Group by adjudication phase | |
| By severity (BLOCKING/MAJOR/MINOR) | Issue-doc severity ordering | |

**Choice:** One questions doc by issue-03 section order; neutral framing; verbatim SCOPE-12 hard-constraints preamble (CONTEXT D-11..D-13).
**Notes:** Differs from Phase 23 (contract-cluster) — the SPEC explicitly locked issue-03 section order, with the per-finding skeleton carrying the finding→phase mapping. D-04/D-05/D-06 + the `D` conflict posed **unsettled** (not decided here). Coverage ≥ the SPEC's selected-finding set; full inventory locked after reading issue-03 in full.

---

## Resolution-doc skeleton (PKG-06 support)

| Option | Description | Selected |
|--------|-------------|----------|
| Non-binding per-finding skeleton | One section per finding; cite v1.4/v1.5 precedents | ✓ |
| Mandated binding schema | Prescribe the resolution-doc structure | |
| No skeleton (format-precedent pointer only) | Phase 23's lighter D-16 approach | |

**Choice:** Non-binding per-finding skeleton, marked non-binding, citing `ctl_pinn_resolution.md` + `02-resolution-doc.md` (CONTEXT D-14).
**Notes:** User-locked in the SPEC; no schema mandated ("the resolution doc remains the user's product").

---

## Claims register (PKG-07)

| Option | Description | Selected |
|--------|-------------|----------|
| CLM-ID register; conservative verified rule; state no-in-milestone-verification | v1.5 D-11..D-13 analog + the v1.6 boundary | ✓ |
| Assume a later v1.6 phase verifies (Phase-24-style) | | |
| Inline figures without a register | | |

**Choice:** CLM-ID claims register; only v1.5-verified facts marked `verified`; register explicitly states that **no in-milestone phase verifies** the claims (CONTEXT D-15..D-17).
**Notes:** The key v1.6 ≠ v1.5 difference — no Phase-24 analog. `claimed-unverified` figures are unverified inputs; verdict-gating figures flagged for FUT. v1.5 anchors (184 IDs without gold, ~2,565 gold count, snapshot/`dt_out` distributions) stated `verified` with citation.

---

## Reports characterization (PKG-08)

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone phase artifact, hash-verified, early task | `23-DQA-CHARACTERIZATION.md` analog | ✓ |
| Inline characterization inside the package master | | |
| Skip characterization (ship reports unannotated) | | |

**Choice:** `30-REPORTS-CHARACTERIZATION.md` covering both reports (provenance + content map + doc-03 relation + role recommendation); zero edits, hash-verified; completes before the doc list is finalized (CONTEXT D-18, D-19).

---

## Delivery & gate-open

| Option | Description | Selected |
|--------|-------------|----------|
| Commit + `DELIVERY-NOTE.md` + STATE via gsd-tools | v1.5 D-16/D-17 analog | ✓ |
| Announce delivery without a delivery note | | |
| Direct-edit STATE.md | Violates anti-pattern 15 | |

**Choice:** Delivery = package committed + user-only `DELIVERY-NOTE.md` (handoff steps, resolution-doc landing path, format precedents, the Phase 31 / 32–36 gate); gate-open recorded in STATE.md via gsd-tools handlers only (CONTEXT D-20, D-21).

---

## simulation_data excerpts

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal — only verified facts the curriculum/training contracts need | doc-03 is less dataset-centric than v1.5 | ✓ |
| Broad dataset excerpts (v1.5 Phase-23 breadth) | | |
| None | | |

**Choice:** Minimal `simulation_data` footprint — include only v1.5-verified facts the curriculum-staging / training-loop contracts depend on (snapshot/`dt_out` distributions bounding `tau_L`/`L_max`/collocation scaling; stage-assignment counts) + claims-register anchors; final selection at the consolidation checkpoint (CONTEXT D-22).

---

## Claude's Discretion

- Exact filenames / placement of the questions doc, SCOPE-12 preamble, claims register, and skeleton (named companion files vs. master sections) — presentation-only; recommended as named companion files.
- Exact `simulation_data` / v1.5 excerpts entering the consolidated file — decided per-finding at the D-09 checkpoint.
- Whether the v1.5-verified-facts reference is standalone or folded into the consolidated context file — recommended standalone.

## Deferred Ideas

- Binding resolution-doc schema — rejected (non-binding skeleton only).
- Any empirical probe / figure verification — out of scope (no Phase-24 analog; FUT/trainex).
- Settling D-04 / D-05 / D-06 or the `D` conflict — posed neutrally; resolved later (resolution doc + Phase 32).
- **Reviewed, not folded:** the `trainex-r1` research-handoff todo (score 0.6) — a different track (trainex / build-design), out of the doc-03 specwork scope; see CONTEXT.md `<deferred>`.

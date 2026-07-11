---
title: Integrity-R2 Pre-Build Audit — Owner Clearance Record
status: ratified
scope: project
purpose: record owner disposal of the MASTER-FINAL-RESOLUTION pre-build punch-list (PB-1..PB-5) and clear the Phase-37 pre-build gate
created: 2026-07-11
inputs: research_results/MASTER-FINAL-RESOLUTION.md
disposed_by: owner (Starlordpd233), 2026-07-11, interactive session
---

# Integrity-R2 — Owner Clearance Record

**What this document is.** `research_results/MASTER-FINAL-RESOLUTION.md` (status: *candidate — owner disposes*) returned a pre-build **NO-GO** blocked on IR2-001/002/003, with a five-item punch-list (PB-1..PB-5) requiring owner fix-or-waive before Phase 37 may start. This record files the owner's dispositions, the actions taken, and the resulting gate state. It follows the `trainex-r1/decision-adjudication/RATIFICATION.md` precedent.

**Verification basis.** Before disposal, the audit's applicability was re-verified in-session (2026-07-11): the package's `specs/` snapshots are SHA-256-identical to the canonical `ctl_instruction.md` / `pinn_architecture.md` on `master`, and `specs/v2.0-build-plan.md` is hash-identical to `.planning/ROADMAP.md` (from line 34) at commit `23a6273c`. Every cited defect was confirmed still present verbatim in the current canonical artifacts.

---

## Punch-list dispositions

| Item | Finding | Owner decision | Action taken | Where applied | Status |
|---|---|---|---|---|---|
| **PB-1** | IR2-001 — Stage-0/1 `s_min > 2` geometrically unsatisfiable (frozen dataset's scaled `s_min ∈ [0.015, 0.084]`); Stages 0–2 empty as written | **Option A, with Option B as interim floor**: criterion becomes `s_min > s₀`, `s₀` data-derived from the admitted-set `s_min` distribution and ratified by the owner at the Phase 39 DATA-06 Thrust-A scan; interim floor `s₀ = 0.01` (matching `MIN_DISTANCE_THRESHOLD = 0.01`, `sampling_method.md` §4) until ratified | Spec micro-pass on `ctl_instruction.md` (glossary sentence, Stage 0/1a/1b criteria, clearance note in the Stratification section); DATA-06 requirement + Phase 39 success criterion extended with the scan's ratification duty | `ctl_instruction.md`; `.planning/REQUIREMENTS.md` DATA-06; `.planning/ROADMAP.md` Phase 39 SC 5 | **FIXED** (value ratification pending at the DATA-06 scan, by design) |
| **PB-2** | IR2-002 — build-plan Phase 38 NET-04 specifies superseded three-term L1/MAE loss vs the locked five-term Huber catalog | **Option A**: rewrite NET-04 to the five-term catalog (data Huber `δ_r = 1` + IC squared-error + causal physics + soft-energy Huber `δ = 1.0` + componentwise angular-momentum Huber `δ = 1.0`, PHYS-05 scheduled weights) | Requirement + roadmap text rewritten | `.planning/REQUIREMENTS.md` NET-04; `.planning/ROADMAP.md` Phase 38 summary + SC 4 | **FIXED** |
| **PB-3** | IR2-003 — build-plan Phase 39 DATA-05 inverts the locked data-fidelity/collocation contract and misapplies 50/50 sampling | **Option A**: rewrite DATA-05 — 240 replay + 16 lookahead (= 256) **trajectories**; data-fidelity points from their snapshots at `n_pts = min(32, n_snapshots)` (~8,192 pts, provisional); collocation points continuous from `[0, T]` (~4,096 pts, provisional; energy reuses the physics collocation set); 50/50 uniform + acceleration-weighted sampling on **data-fidelity only** (mixed continuous collocation deferred per LOOP-03) | Requirement + roadmap text rewritten | `.planning/REQUIREMENTS.md` DATA-05; `.planning/ROADMAP.md` Phase 39 SC 4 | **FIXED** |
| **PB-4** | IR2-004 — split not grouped by `physical_key`; base/gold twins can straddle train/val/test | **Option A**: DATA-04 gains the grouped-split invariant — partition by `physical_key = (variant, id)` first, expand to all `record_key`s, assert no `physical_key` spans splits | Requirement + roadmap text extended | `.planning/REQUIREMENTS.md` DATA-04; `.planning/ROADMAP.md` Phase 39 SC 3 | **FIXED** |
| **PB-5** | IR2-005 — `ctl_instruction.md` dataset table swaps Set 1b / Set 2a counts vs Tier-1 verified counts | **Option A**: swap the count cells (Set 1b = 2,749 Standard; Set 2a = 4,857 Hierarchical) and record the propagation (below) | Spec micro-pass on the `tab:brutus_compare` table | `ctl_instruction.md` dataset table | **FIXED** |

### PB-5 propagation note (recorded per Option A)

The trainex-r1a corpus arithmetic built on the stale table (≈6.24 M snapshots ≈ 0.55 GB fp32) becomes **≈8,228,794 snapshots ≈ 0.72 GB fp32 / ≈1.45 GB fp64** under the corrected counts — still comfortably in-memory on the verified 24 GB machine (≈3% of RAM at fp32), so **no ratified trainex-r1a decision changes**. `trainex-r1a-resolution-doc.md` and `RATIFICATION.md` ("~0.55 GB") are dated owner-ratified records and are deliberately left unedited; this note supersedes their corpus arithmetic.

## Minor findings (not gates)

| Item | Owner routing | Action |
|---|---|---|
| IR2-006 (DATA-02 summarizes Step-1A gate incompletely) | Fix with the punch-list | DATA-02 requirement + Phase 39 SC 2 now name the full clause-1–7 family incl. the conservation reject gate (`eps_H ≤ 1e-5`) and the fail-closed blacklist |
| IR2-007 (`compute_L_norm` snippet silently ε-floors the degenerate regime) | Fix in the spec micro-pass | Snippet replaced with the exact formula plus an explicit degenerate branch emitting `(None, "degenerate_Lmax")`; degeneracy floor reuses the existing spec constant `1e-10` (ε_inv) — no new number introduced |
| IR2-008 (Step-1A clause 2 presents the closed DATA-05 quarantine as pending) | Fix in the spec micro-pass | Clause 2 converted to a historical note (validation passed 2026-06-11; quarantine-list configuration empty in the verified baseline; mechanism preserved, re-opens on a future validation failure) |

## Spec-edit routing decision

The delivery note routes spec-touching findings to a future spec milestone (specs are read-only inputs to v2.0). The owner instead authorized a **bounded pre-v2.0 micro-pass now** (2026-07-11), limited to the four disposed items above (PB-1 wording, PB-5 table, IR2-007 snippet, IR2-008 note), so Phase 39's builder does not read proven-defective text in the authoritative spec. No other spec content was touched; the package's `specs/` snapshots remain the frozen audit baseline and are never edited.

## Package landing notes

- Results folder normalized `research-results/` → `research_results/` per the delivery-note convention; `.DS_Store` removed.
- Landed filenames (`<agent>-FINAL-RESOLUTION.md`, `MASTER-FINAL-RESOLUTION.md`) differ from the delivery-note template (`<agent>-integrity-r2.md`, consolidation at round root as `integrity-r2-resolution-doc.md`); kept as landed — the master resolution's frontmatter `inputs:` references the landed names.

## Gate state

- **Phase-37 pre-build gate: CLEARED** (all Serious proven issues fixed per owner disposition; none waived). Phase 37 may be planned (`/gsd-plan-phase 37`) once the trainex branch is aligned `milestone/v1.7` → `milestone/v2.0` at first phase execution per `.planning/STATE.md`, preserving the two v1.7-only commits (`28ec6372`, `0fb51eb2`).
- **Side-list SL-1..SL-10**: remain open observation items for the build phases (notably SL-1 MPS double-backward coverage → Phase 37 probe; SL-10 Stage-0 ε_H achievability → Phase 43 pilot). They are not gates.

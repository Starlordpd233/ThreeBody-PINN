# Evidence Packet: adaptive stage assignment - Data-driven Adaptive Stage Assignment (CURR-01)

## Header

| Field | Value |
|---|---|
| ID | `adaptive stage assignment` |
| Title | Data-driven adaptive stage assignment (CURR-01) |
| Phase 33 Decisions Covered | `D-33-01`, `D-33-02`, `D-33-03` (see `33-CONTEXT.md` decisions section) |
| Severity | MAJOR |
| Current Status | IN_PROGRESS |
| Current Verdict | accept-resolution |
| Phase | Phase 33 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 36 |
| Acceptance Check ID | AC-CURR-01 |
| Spec Sections Touched | `ctl_instruction.md` "Multi-Stage Data Stratification by Difficulty"; `ctl_instruction.md` Step 5 "Curriculum Stage Assignment"; `ctl_instruction.md` `record_key` ownership contract |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative. The resolution doc is a candidate verdict source, not authority; the issue doc is a non-authoritative proposal source.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:189-223` (adaptive proposal); `pinn_instruction/issues/03-curriculum-and-training-loop.md:198-217` (PCA + K-means pseudocode); `pinn_instruction/issues/03-curriculum-and-training-loop.md:223` (">10% per stage" safeguard); `pinn_instruction/issues/03-curriculum-and-training-loop.md:205-210` (cluster-sort-by-`tau_L`) | Non-authoritative issue source | Proposes a transition from fixed theoretical thresholds to PCA + K-means adaptive stage assignment keyed on `tau_L` / `E`, with a per-stage `>10%` population safeguard and a quasi-random-only topology sorted by mean `tau_L`. The proposed `stage_strat_revision.md` Table 4 topology re-organizes Stages 0-6 into a quasi-random-only hierarchy that erases existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:80-82` (§1.15 Data-driven adaptive stage assignment — `modified`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:162-168` (claim rows `ADAPT-01` modified, `ADAPT-02` accepted, `ADAPT-03` rejected Table 4, `ADAPT-04` `surface_to_user`, `ADAPT-05` defer, `ADAPT-06` rejected unverified, `ADAPT-07` defer); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:204-205` (DGR-15 adaptive topology, DGR-16 population safeguard) | candidate verdict source, not authority | §1.15 permits offline admitted-set EDA + robust transforms + PCA + clustering as boundary-calibration tools augmenting the static theoretical anchors; rejects `stage_strat_revision.md` Table 4 wholesale because it erases Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles; materializes stable integer labels keyed by `record_key`; the 5% vs `>10%` population safeguard is surfaced to the owner (`ADAPT-04` `surface_to_user`, `ADAPT-07` defer); CLM-02..07 remain unverified. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:95` (finding -> §1.15 / lines 80-83 mapping); `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:60` (§1.15 line range) | Navigation / line-map aid | §1.15 anchored to lines 80-83 in the committed `49fb7958` revision; section anchor stable across re-pagination, line numbers re-verifiable from `33-BASELINE-CAPTURED`. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:105-247` defines the existing multi-fidelity Stage 0-6 inventory with **Stage 0** hierarchical Set-1a high-fidelity stable systems, **Stage 1** hierarchical Set-1a energy/angular-momentum-relaxed, **Stage 2** high-resolution refinement of stable orbits (Set 2a hierarchical gold), **Stage 3** moderately chaotic low-fidelity quasi-random (Set 1b), **Stage 4a/4b** chaotic low-fidelity by `tau_L`, **Stage 5** high-resolution chaotic orbits (Set 2b quasi-random gold), and **Stage 6** near-collision / extreme catch-all (HF+LF). The Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles are explicit and must not be erased.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:425-441` defines the `record_key = (variant, fidelity, id)` ownership contract: stage labels (Step 5) are keyed by `record_key`, never by positional index.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1425-1508` defines Step 5 "Curriculum Stage Assignment" and its anchors (energy, virial, `s_min`, `tau_L`, `L_norm`).

No framework spec is edited by this packet (Plan 33-01 only authors evidence; Plan 33-02 will transcribe).

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16-18` (SCOPE-12) makes locked v1.4/v1.5 outcomes hard-constraint grounding. The locked 14D input `[τ, IC₁₃]`, the Jacobi IC₁₃ vector, and the mass-weighted COM projection head constrain any stage-assignment methodology to materialize stable labels keyed by `record_key` so that the dataset↔framework binding does not change at training time.
- `.planning/REQUIREMENTS.md` `CURR-01` is the requirement for this packet. The `>10%` per-stage safeguard phrasing in `CURR-01` is **superseded** by `GAP-33-01` (see below).
- `GAP-33-01` (`33-GAPS.md:8-61`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22) is the owner-routed resolution that carries the grounded disposition for this packet: packet-first / defer-floor. The per-stage population safeguard value (5% / `>10%` / adaptive) is **owner-pending the FUT admitted-set EDA (SCOPE-15)**; the `>10%` phrasing in `CURR-01` is NOT locked and must not be transcribed as a locked floor.

## FUT Hand-off Note

- FUT path / note: The offline admitted-set EDA run itself is FUT (`SCOPE-15`). Phase 33 specifies the methodology contract only; it does not run the EDA. References to live `pinn/data-processing-pipeline-full.py` clustering helpers are NOT grounding evidence; they appear only as FUT-01/FUT-04 hand-off context.
- Not FUT-applicable: This packet does not derive its verdict from any live code reference. The methodology contract is grounded by the resolution doc, the current spec, and the owner-routed `GAP-33-01`.

## First-Principles or Engineering Check

Adaptive stage assignment partitions a finite admitted trajectory set into curriculum buckets using the dataset's empirical invariant distribution. The engineering question is *how* to combine static theoretical anchors (`E`, `Q`, `s_min`, `tau_L`, `L_norm`) with data-driven boundary calibration while preserving the existing multi-fidelity topology.

PCA + K-means is a reasonable offline boundary-calibration tool because the invariant vector is low-dimensional (E, Q, `s_min`, `tau_L`, `L_norm`, I1, I2, I3) and `record_key` provides a stable join key. However, three engineering consequences are not derivable from first principles and therefore must be owner-routed rather than auto-locked:

1. **Topology preservation.** Replacing the existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles with a quasi-random-only topology (Table 4) changes what the network learns at each refinement stage. The current multi-fidelity topology uses Stage 2 to refine stable-orbit fitting on the same physical ICs at higher temporal resolution, and Stage 5 to refine chaotic-orbit resolution; this is an intentional design choice, not an accident. Erasing those roles is a structural change that requires explicit owner instruction.
2. **Population safeguard value.** A 5% floor, a `>10%` floor, and an EDA-selected adaptive floor are not equivalent: they produce different merge operations for sparse clusters, change the stage distribution seen by replay and transition gates, and can erase or preserve rare near-collision / chaotic regimes. Without the admitted-set distribution in hand, the threshold is a policy choice rather than a derivable constant. (Reproduced verbatim from `GAP-33-01` mathematical grounding.)
3. **Quantile thresholds.** Per-stage quantile cut points must be computed over the frozen admitted set and materialized as stable integer labels keyed by `record_key` before training begins; otherwise training-time stage distribution drift invalidates replay and transition-gate semantics.

## Verdict

Verdict: accept-resolution

Explicit user instruction: `GAP-33-01` (`33-GAPS.md:49-61`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22, owner AskUserQuestion ratification of packet-first / defer-floor).

Reasoning:

- The resolution doc §1.15 permits offline admitted-set EDA + robust transforms + PCA + clustering + quantile thresholds as boundary-calibration tools augmenting the static theoretical anchors, rejects Table 4 wholesale because it erases Stage-2/Stage-5 refinement roles, and materializes stable labels keyed by `record_key`. This is the grounded position.
- The owner-routed `GAP-33-01` resolution carries the per-stage population safeguard deferral forward: the value (5% / `>10%` / adaptive) is owner-pending the FUT admitted-set EDA (SCOPE-15), not locked by Phase 33.
- The current spec's `record_key` ownership contract (lines 425-441) is the implementation anchor for stable label materialization.
- The `>10%` phrasing in `CURR-01` and the roadmap is explicitly superseded and must not be transcribed as a locked floor.

## Root-Cause Ambiguity

The root ambiguity is a topology-and-threshold collision: the issue doc proposes a quasi-random-only topology with a `>10%` floor; the current spec preserves a multi-fidelity topology with hierarchical-gold (Stage 2) and quasi-random-gold (Stage 5) refinement roles; the candidate resolution doc routes the population-floor value to the owner after admitted-set EDA. Phase 33's job is to lock the methodology contract while leaving the threshold value owner-pending.

## Locked Convention or Owner Route

**Methodology contract (locked by this packet, decisions D-33-01, D-33-02, D-33-03):** Per D-33-01, Phase 33 transcribes (in Plan 33-02) an offline admitted-set EDA -> robust transforms -> PCA -> clustering -> quantile-threshold methodology that **augments** the static theoretical anchors within the existing multi-fidelity Stage 0-6 topology; it does not lock the population safeguard value. Per D-33-02, Phase 33 does NOT adopt `stage_strat_revision.md` Table 4 wholesale because it erases the Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles. Per D-33-03, the actual admitted-set EDA run and any population-floor owner policy are FUT, not Phase 33 execution. Stable integer stage labels are materialized keyed by `record_key`. The Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles are preserved (Table 4 not adopted wholesale; ADAPT-03 rejected; DGR-15).

**Owner route (deferred, GAP-33-01):** The per-stage population safeguard value (5% / `>10%` / adaptive) is owner-pending the FUT admitted-set EDA (SCOPE-15). No value is locked in Phase 33.

## Which Source Was Correct / Wrong

- Resolution doc (§1.15): correct on the methodology contract and correct to reject Table 4 wholesale and to surface the population safeguard to the owner, after independent grounding.
- Issue doc: partly correct on the PCA + clustering methodology; wrong to encode a quasi-random-only topology (Table 4) that erases Stage-2/Stage-5 refinement roles; wrong to lock a `>10%` floor as if it were derivable.
- Current spec: correct and governing for the `record_key` ownership contract and the multi-fidelity topology.
- The roadmap / `CURR-01` `>10%` phrasing is superseded by `GAP-33-01` and must not be transcribed as a locked floor.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` already defines the multi-fidelity Stage 0-6 topology with Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles and the `record_key` ownership contract.

**After (Plan 33-02, not Plan 33-01):** `ctl_instruction.md` Step 5 will add the offline EDA -> robust transforms -> PCA -> clustering -> quantile-threshold methodology as an augmentation to the static theoretical anchors, with stable `record_key` labels. No population-floor value is locked; the contract carries an explicit owner-pending clause.

Plan 33-01 makes no spec edit. This packet routes the evidence and AC-CURR-01 identity.

## Named Acceptance Check

AC-CURR-01

Planned pass criterion (Plan 33-04 / Phase 36): `ctl_instruction.md` Step 5 / Stage-stratification text states (a) offline EDA -> robust transforms -> PCA -> clustering -> quantile-threshold methodology augmenting static theoretical anchors, (b) stable integer labels keyed by `record_key`, (c) Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles preserved, (d) population-floor value explicitly owner-pending the FUT admitted-set EDA, and (e) no `>10%` / 5% / adaptive rule is locked as normative.

Owning phase: Phase 33 (Plan 33-02 transcribes; Plan 33-04 verifies).

## STOP / Gap Handling

No STOP gap opened — disposition grounded in `GAP-33-01` `RESOLVED-WITH-INSTRUCTION` 2026-06-22 (owner-routed packet-first / defer-floor; AskUserQuestion ratification), matching resolution doc §1.15 (ADAPT-04 `surface_to_user`, ADAPT-07 defer, ADAPT-03 / DGR-15 Table 4 rejected). The methodology contract is grounded by the resolution doc, current spec, and SCOPE-12; the population-floor value is the explicitly owner-pending remainder and is not a source-silent semantic gap.

## Status Transition Log

```text
2026-06-23 0113f86 PENDING -> IN_PROGRESS (Phase 33 P01 Task 2 by claude-code-gsd-executor-33-01; packet authored, ledger link applied in Task 3)
```

# Phase 29: Milestone Handoff (v1.5 — Resolving 02 Data Pipeline and Validation)

This handoff is the v1.5 milestone-closure record and the FUT-01 input. It mirrors the v1.4
`21-HANDOFF.md` four-section shape (Fixed / Intentionally Unchanged / Deferred / SI Metadata
Reconciliation), adds the FUT-01 / Consumption Notes and the numerically-defined
Milestone-Closure Gate, and is grounded in the fresh Phase-29 acceptance re-run (`29-ACCEPTANCE-EVIDENCE-2026-06-17.md`),
the `24-ISSUE-LEDGER.md` terminal-state audit, and the already-committed `29-CODE-DIVERGENCE.md`
forward obligations. It is the `29-HANDOFF.md` half of the two-artifact FUT-01 handoff (D-09);
`29-CODE-DIVERGENCE.md` is the other half.

No framework spec, dataset file, `pinn/` production code, or read-only/frozen file is edited by
this handoff. SI dispositions and gold-completeness staleness are recorded here as planning-layer
records, not by editing their home files (SCOPE-08/09/10, D-01).

## Evidence Used

- `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` — the fresh 2026-06-17 Phase-29 acceptance re-run (13-check AC suite, 12 PASS +
  AC-VAL-04 structural-PASS / numeric-DEFERRED split, exit 0), the 19-row ledger terminal-state
  audit (18 VERIFIED + 1 DEFERRED), and the 36/36 roadmap traceability confirmation.
- `24-ISSUE-LEDGER.md` — the v1.5 issue ledger Status Table (19 rows); the source of the Fixed
  list below (each row's `Status`, `Acceptance Check`, and resolving `Phase`).
- `29-CODE-DIVERGENCE.md` — the FUT-01 forward obligations (FO-1 gold promotion + 184→67 cascade;
  FO-2 PSC/SCR numeric calibration + AC-VAL-04 numeric run), the gold-completeness reconciliation
  table, and the stale-record inventory. Referenced here, not duplicated.
- SI home line-ranges (read for disposition; **not edited**):
  `data_quality_assessment.md:318-328` (SI-DQA-002 / SI-DQA-003, read-only — SCOPE-09);
  `pinn_architecture.md:996-1004` (SI-PINN-002).
- `21-HANDOFF.md` — the v1.4 precedent for the section shape and the SI-reconciliation table
  (`Entry | Status | Evidence`); SI-PINN-002 recorded "Preserved untouched" in v1.4.

## 1. Fixed

The following **18 in-scope v1.5 findings** are `VERIFIED` in `24-ISSUE-LEDGER.md` and are
covered by their Phase-25 evidence packets plus the fresh Phase-29 acceptance evidence
(`29-ACCEPTANCE-EVIDENCE-2026-06-17.md`). Each row names its acceptance check and the phase that resolved it — transcribed
from the ledger Status Table, nothing invented.

| Finding | Title | Acceptance Check | Resolving Phase |
|---|---|---|---|
| **B-06** | Stage 4→5 trajectory-admission gate (validator at DataLoader init) | AC-PIPE-01 | 26 (PIPE-01) |
| **B-11** | Non-contiguous IDs (ID ≠ array index; `id_to_path` contract) | AC-PIPE-02 | 26 (PIPE-02) |
| **M11** | Blacklist-exclusion consumption contract | AC-PIPE-03 | 26 (PIPE-03) |
| **M12** | Points-per-trajectory `n_pts = min(cap, n_snapshots)` | AC-PIPE-04 | 27 (PIPE-04) |
| **M13** | 184 standard IDs without gold counterpart (fallback policy) | AC-PIPE-05 | 26 (PIPE-05) |
| **D7** | Footer / parameter-provenance contract | AC-PIPE-06 | 26 (PIPE-06) |
| **G1** | Pipeline-validation-gap synthesis view (closes with B-06) | AC-PIPE-01 | 26 (PIPE-01) |
| **G2** | Pipeline-validation-gap synthesis view (closes with B-11) | AC-PIPE-02 | 26 (PIPE-02) |
| **G3** | Pipeline-validation-gap synthesis view (closes with M11) | AC-PIPE-03 | 26 (PIPE-03) |
| **G4** | Pipeline-validation-gap synthesis view (closes with M13) | AC-PIPE-05 | 26 (PIPE-05) |
| **G5** | `dt_out` heterogeneity (data-side facet; M16 → doc-03) | AC-PIPE-04 | 27 (PIPE-04) |
| **SCS** | Symplectic Conservation Score gate (`SCS>-5` / `ε_H>1e-5`) | AC-VAL-01 | 28 (VAL-01) |
| **SASD** | Stiffness-Aware Sampling Density (both-endpoint) | AC-VAL-02 | 28 (VAL-02) |
| **IPR** | Interpolation Physics Residual (raw `G=1` units; dual-epsilon) | AC-VAL-03 | 28 (VAL-03) |
| **D-03** | Processed training-data format (HDF5 canonical) | AC-PIPE-10 | 26 (PIPE-10) |
| **D=6.694** | `compute_globals` raw-mass `D≈4.6416`; `6.694` rejected by name | AC-PIPE-09 / EVID-10 | 25 (EVID-10) / 27 (PIPE-09) |
| **footer** | Footer / mass-drift protocol (DATA-05 rerun, not Decimal fallback) | AC-PIPE-06 / AC-PIPE-07 | 26/27 (PIPE-06/07) |
| **mass-drift** | Precision handling (float64 sufficiency; DATA-05 verdict) | AC-PIPE-07 | 27 (PIPE-07) |

All 18 re-ran fresh and PASSED in Phase 29 (`29-ACCEPTANCE-EVIDENCE-2026-06-17.md` §2); AC-PIPE-05 PASSED at **184/184**
(0 promoted under D-01 — internally consistent because gold stays 2,565 and `base − gold = 184`).

## 2. Intentionally Unchanged

The following are deliberately left at their current values — each is a record of a decision, not
an unresolved finding. Cross-referenced, not duplicated.

- **KNOWN-STALE gold records, left at pre-promotion values under D-01.** Per the locked GAP-29-01
  Option-A ruling, Phase 29 reconciles only the planning/governance/ledger layer to the
  **117 validated / 67 permanent `gold_counterpart=absent` / 0 promoted** fact; it does **not**
  promote the 117 or run the 184→67 cascade. The records left stale (and their FO-1 corrective
  step) are enumerated in the `29-CODE-DIVERGENCE.md` **stale-record inventory** — see that file,
  not reproduced here:
  `standard_quasi_random_ids_not_in_gold.md` (184 IDs), the `AC-PIPE-05` assertion (184/184), the
  runner `EXPECTED_ID_COUNT` (184), the `ctl_instruction.md` Step 5 gold note ("backlog expected
  empty"), and the Set-2b / issue-02 counts (2,565). The staleness is documented, never silent;
  FO-1 is the single corrective transaction at the FUT-01 dataset-finalization gate.
- **M13 / G4 ledger rows + packet — verdict untouched (D-01a).** Both stay `VERIFIED` carrying the
  OI-7b-partial reconciliation note (117 validated-staged / 67 permanent-absent / 0 promoted;
  promotion ruled to the FUT-01 gate). The LOCKED `accept-third-position` / Option-B verdict
  (re-simulate; no base→gold substitution) is **not** re-adjudicated.
- **Read-only `data_quality_assessment.md` (SCOPE-09).** The SI-DQA-002 / SI-DQA-003 home file is
  read-only; their dispositions are recorded in §4 below, not by editing the DQA.
- **Frozen `sampling_method.md` (SCOPE-08).** The completed data-generation instruction document
  is frozen by default; no v1.5 edit.

## 3. Deferred

The following remain explicitly deferred, each pointing to its forward home:

- **PSC numeric calibration + the AC-VAL-04 numeric run** → `29-CODE-DIVERGENCE.md` **FO-2**, at
  the FUT-01 dataset-finalization gate. The PSC clause is **landed** and well-formed in
  `ctl_instruction.md` (Data-side quality-metric contracts) and the dedup-prefer-gold + `1/N_t`
  composition is **ratified** (GAP-28-03); only the construction *constants* (grid, `H/ln K`
  normalization, SCR anchor, first-run sanity) are provisional pending the post-promotion pool.
  The AC-VAL-04 **structural** axis already executed and PASSED in Phase 29; the **numeric** axis
  is deferred. The PSC ledger row stays `DEFERRED` for this reason.
- **The 117 gold promotion + the 184→67 framework-spec/AC cascade** → `29-CODE-DIVERGENCE.md`
  **FO-1** (GAP-29-01, DEFERRED to the FUT-01 dataset-finalization gate per the locked Option-A
  ruling). This is a canonical-dataset mutation, out of Phase 29 scope under D-01; recording it as
  a FUT-01 forward obligation is what lets it survive v1.5 closure (D-10).
- **doc-03 items** — M16 (collocation-scaling / `dt_out` training-side facet) and the training-side
  SCS / SASD / IPR / PSC consumption contracts → the future doc-03 milestone. These are the
  training-side counterparts of the data-side metric contracts landed in v1.5; they are out of the
  issue-02 (data-pipeline) scope this milestone resolves.

## 4. SI Metadata Reconciliation

The three SI entries named by VER-12 are reviewed for issue-02 relevance. Each is
**retired-with-backref** or **preserved-with-written-reason** — none assumed resolved or assumed
irrelevant. The table mirrors the `21-HANDOFF.md` SI-reconciliation shape
(`Entry | Status | Evidence`). Dispositions are recorded here only; no SI home file is edited
(SCOPE-09 makes `data_quality_assessment.md` read-only; the `pinn_architecture.md` SI section is
not touched). The adjacent `pinn_architecture.md` batch-construction-inconsistency SI entry
(the next SI block after `SI-PINN-002`) is **not** in the VER-12 review list and is deliberately
not folded in; it remains an FUT-05 item.

| Entry | Status | Evidence |
|---|---|---|
| `SI-DQA-002` | **Retired with VAL-01 / SCS-row back-reference.** The SCS gate inconsistency it flags ("initial audit missed SCS gate inconsistency") is now resolved and canonical in `ctl_instruction.md` (Step-1A conservation gate, `SCS>-5` / `ε_H>1e-5`) via v1.5 VAL-01. | SCS ledger row (VAL-01, AC-VAL-01 PASS 2026-06-16) + `data_quality_assessment.md:318-322` (read-only home) |
| `SI-DQA-003` | **Retired with VAL-01 back-reference.** The corrected SCS gate it describes (`ε_H` raw-drift vs `SCS=log10(ε_H)`; gate `ε_H>1e-5`≡`SCS>-5`; Reject tightened `SCS>-4`→`SCS>-5`) is the gate v1.5 VAL-01 canonicalized into the live spec; the SCS ledger row already names the DQA as the read-only/historical home. | SCS ledger row (VAL-01) + `data_quality_assessment.md:324-328` (read-only home) |
| `SI-PINN-002` | **Preserved with written reason.** These are architecture-side `\authcomment{}` editorial notes (omega_0 detail; hidden-layer detail; "batch construction not consistent with the CTL instruction plan"), out of the issue-02 data-pipeline scope this milestone resolves; carried forward to FUT-05 / training implementation (the v1.4 Phase 22 author-comment adjudication target). The 3rd comment is **not** marked retired-by-M12 — whether the landed M12 mini-batch contract discharges that author comment is source-silent (D-08), so the grounded disposition is preserve-with-reason. Matches the v1.4 `21-HANDOFF.md` "Preserved untouched." | `pinn_architecture.md:996-1004` (editable home, not edited) + `21-HANDOFF.md` SI-PINN-002 row |

**D-08 checkpoint resolution (provenance).** The `SI-PINN-002` preserve-with-reason disposition was
surfaced to the user as a `checkpoint:human-verify` STOP point during Plan 02 Task 2 — the
source-silent question of whether the landed M12 mini-batch contract discharges the 3rd author
comment. The user **approved preserve-with-reason on 2026-06-17**, explicitly declining to mark the
comment retired-by-M12. The disposition above is therefore user-confirmed under the STOP protocol,
not a silent semantic call.

## 5. FUT-01 / Consumption Notes

- The FUT-01 forward obligations are recorded in `29-CODE-DIVERGENCE.md`: **FO-1** (promote the
  117 validated reruns + apply the 184→67 cascade; the durability backup of the 117 + manifest is
  a FO-1 "do-now" item) and **FO-2** (PSC/SCR first-run sanity + validation-constant
  recalibration; the AC-VAL-04 numeric run). FUT-01 consumes both at the dataset-finalization gate.
- **Live `pinn/` is a divergence target only (SCOPE-10).** The v1.3-era code in `pinn/` is NOT a
  grounding source and was NOT touched in v1.5; it appears only as a forward alignment target in
  `29-CODE-DIVERGENCE.md` / this handoff. FUT-01 rebuilds the code from the framework specs.
- **FUT-01 must not reinterpret the v1.5 semantic decisions** (the M13 Option-B verdict, the
  ratified PSC composition, the SI dispositions in §4, the locked gold framing) without opening a
  **new STOP-protocol gap** and obtaining user instruction. The v1.5 closure freezes these; a
  forward implementation discrepancy is a new gap, not a license to re-decide.

## 6. Milestone-Closure Gate (G1-G8)

The numerically-defined gate under which v1.5 closes. The eight conditions are transcribed from
`29-RESEARCH.md` §Milestone-Closure Gate; nothing is invented. The PLAN defines these criteria and
the gsd-verifier records the result in `29-VERIFICATION.md` / `29-VALIDATION.md` downstream. A
failing check blocks closure and routes the specific finding back to its originating phase
(VER-09 routing clause).

| # | Gate Condition (numeric) | Pass = | Route-back-on-fail target |
|---|--------------------------|--------|---------------------------|
| G1 (VER-07/09) | All 13 AC checks executed with fresh Phase-29 results | 12 PASS + 1 split (AC-VAL-04 structural PASS / numeric DEFERRED); 0 FAIL | The originating spec-edit phase (26/27/28) for any FAIL |
| G2 (VER-09) | AC-PIPE-05 dataset probe | PASS @184/184 (0 promoted; consistent under D-01) | Phase 26 (M13) if set-difference breaks |
| G3 (D-07/VER-10) | Ledger row-status audit | 19 rows; 18 VERIFIED + 1 DEFERRED; **0** PENDING/IN_PROGRESS/FIX_APPLIED | The owning phase of any non-terminal row |
| G4 (VER-12) | 3 SI dispositions recorded | SI-DQA-002, SI-DQA-003, SI-PINN-002 each retired-with-backref OR preserved-with-reason; 0 assumed | (no spec phase — recorded in `29-HANDOFF.md` §4) |
| G5 (VER-11) | Handoff completeness | `29-HANDOFF.md` has fixed/unchanged/deferred + SI table; `29-CODE-DIVERGENCE.md` FO-1/FO-2 present | — |
| G6 (VER-08) | Traceability | 36/36 reqs → exactly one phase; Phase 29 = VER-07/08/09/11/12 | roadmap revision if mismatch |
| G7 (D-05/D-01) | Gold reconciliation recorded | `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` references the 117/67/0-promoted table; stale-artifact inventory present; PSC numeric stays DEFERRED | — |
| G8 (governance) | No `pinn/` touch, no spec edit, no dataset mutation, no read-only/frozen-file edit | grep diff of touched paths shows only `.planning/` (+ optional probe scripts) | STOP if violated |

**Closure rule:** v1.5 closes only when **G1–G8 all pass**. Any G1/G2/G3 FAIL routes the specific
finding back to its originating phase (26/27/28) per VER-09; v1.5 does not ship while any required
check fails.

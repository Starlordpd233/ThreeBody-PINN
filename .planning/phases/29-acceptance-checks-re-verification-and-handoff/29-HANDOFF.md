# Phase 29: Milestone Handoff (v1.5 — Resolving 02 Data Pipeline and Validation)

This handoff is the v1.5 milestone-closure record and the FUT-01 input. It mirrors the v1.4
`21-HANDOFF.md` four-section shape (Fixed / Intentionally Unchanged / Deferred / SI Metadata
Reconciliation), adds the FUT-01 / Consumption Notes and the numerically-defined
Milestone-Closure Gate, and is grounded in the fresh Phase-29 acceptance re-run (`29-UAT.md`),
the `24-ISSUE-LEDGER.md` terminal-state audit, and the already-committed `29-CODE-DIVERGENCE.md`
forward obligations. It is the `29-HANDOFF.md` half of the two-artifact FUT-01 handoff (D-09);
`29-CODE-DIVERGENCE.md` is the other half.

No framework spec, dataset file, `pinn/` production code, or read-only/frozen file is edited by
this handoff. SI dispositions and gold-completeness staleness are recorded here as planning-layer
records, not by editing their home files (SCOPE-08/09/10, D-01).

## Evidence Used

- `29-UAT.md` — the fresh 2026-06-17 Phase-29 acceptance re-run (13-check AC suite, 12 PASS +
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
(`29-UAT.md`). Each row names its acceptance check and the phase that resolved it — transcribed
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

All 18 re-ran fresh and PASSED in Phase 29 (`29-UAT.md` §2); AC-PIPE-05 PASSED at **184/184**
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

<!-- Populated in Task 2 (VER-12 SI dispositions). -->

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

<!-- Populated in Task 3 (numerically-defined G1-G8 closure gate). -->

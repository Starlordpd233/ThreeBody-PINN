---
phase: 24-empirical-dataset-verification-and-correction-addendum
slug: dataset-verification-and-correction-addendum
status: draft
created: 2026-06-11
total_findings: 19
in_scope_findings: 19
deferred_findings: 0
traceability_verified: true
last_verified_traceability: "19/19 issue-02 findings seeded; verified against 23-CLAIMS-INVENTORY.md and REQUIREMENTS.md traceability"
---

# Phase 24 Issue Ledger

## Status Table

| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| B-06 | Stage 4→5 validation gate (trajectory-validator at DataLoader init) | 26 (PIPE-01) | PENDING | — | NO | — | AC-PIPE-01 | ctl_instruction.md; pinn_architecture.md | Q-A1 | 2026-06-11 |
| B-11 | Non-contiguous IDs (ID ≠ array index; id_to_path / TrajectoryIndex contract) | 26 (PIPE-02) | PENDING | — | NO | — | AC-PIPE-02 | ctl_instruction.md; pinn_architecture.md | Q-A2 | 2026-06-11 |
| M11 | Blacklist not loaded at training time (consumption contract) | 26 (PIPE-03) | PENDING | — | NO | — | AC-PIPE-03 | ctl_instruction.md; pinn_architecture.md | Q-A3 | 2026-06-11 |
| M12 | Points-per-trajectory infeasibility (32 vs observed snapshot distribution) | 27 (PIPE-04) | PENDING | — | NO | — | AC-PIPE-04 | ctl_instruction.md | Q-B1 | 2026-06-11 |
| M13 | 184 standard IDs without gold counterpart (fallback policy) | 26 (PIPE-05) | PENDING | — | NO | — | AC-PIPE-05 | ctl_instruction.md; pinn_architecture.md | Q-A4 | 2026-06-11 |
| D7 | Footer / parameter heterogeneity (folder-default fallback, tol_confidence) | 26 (PIPE-06) | PENDING | — | NO | — | AC-PIPE-06 | ctl_instruction.md; pinn_architecture.md | Q-A5 | 2026-06-11 |
| G1 | Pipeline validation gap — synthesis view (B-06) | 26 (PIPE-01) | PENDING | — | NO | — | AC-PIPE-01 (synthesis view over B-06) | ctl_instruction.md; pinn_architecture.md | B-06 | 2026-06-11 |
| G2 | Pipeline validation gap — synthesis view (B-11) | 26 (PIPE-02) | PENDING | — | NO | — | AC-PIPE-02 (synthesis view over B-11) | ctl_instruction.md; pinn_architecture.md | B-11 | 2026-06-11 |
| G3 | Pipeline validation gap — synthesis view (M11) | 26 (PIPE-03) | PENDING | — | NO | — | AC-PIPE-03 (synthesis view over M11) | ctl_instruction.md; pinn_architecture.md | M11 | 2026-06-11 |
| G4 | Pipeline validation gap — synthesis view (M13) | 26 (PIPE-05) | PENDING | — | NO | — | AC-PIPE-05 (synthesis view over M13) | ctl_instruction.md; pinn_architecture.md | M13 | 2026-06-11 |
| G5 | dt_out heterogeneity (data-side; Q-B1 facet; collocation-scaling facet M16 deferred to doc-03) | 27 (PIPE-04) | PENDING | — | NO | — | AC-PIPE-04 (data-side facet; M16 training-side deferred) | ctl_instruction.md; pinn_architecture.md | M12; M16-deferred | 2026-06-11 |
| SCS | Symplectic Conservation Score definition + thresholds (data-side; Q-C1) | 28 (VAL-01) | PENDING | — | YES — EVID-10 required (ratio-SCS vs locked log-drift gate) | — | AC-VAL-01 | data_quality_assessment.md (read-only; sole written home of locked gate) | Q-C1 | 2026-06-11 |
| SASD | Stiffness-Aware Sampling Density (data-side; Q-C2) | 28 (VAL-02) | PENDING | — | NO | — | AC-VAL-02 | ctl_instruction.md; pinn_architecture.md | Q-C2 | 2026-06-11 |
| IPR | Interpolation Physics Residual (data-side, dual-epsilon; Q-C3) | 28 (VAL-03) | PENDING | — | NO | — | AC-VAL-03 | ctl_instruction.md; pinn_architecture.md | Q-C3 | 2026-06-11 |
| PSC | Phase Space Coverage Entropy (data-side; Q-C4) | 28 (VAL-04) | PENDING | — | NO | — | AC-VAL-04 | ctl_instruction.md; pinn_architecture.md | Q-C4 | 2026-06-11 |
| D-03 | Processed training-data format (HDF5 vs .npy vs txt/json) | 26 (PIPE-10) | PENDING | — | NO | — | AC-PIPE-10 | ctl_instruction.md | Q-A6 | 2026-06-11 |
| D=6.694 | compute_globals / D=6.694 convention conflict (CLM-13) — NOT probed by Phase 24; routed to Phase 25 EVID-10 / Phase 27 PIPE-09 | 25 (EVID-10) / 27 (PIPE-09) | PENDING | — | YES — EVID-10 required (PHYS-01 raw-mass D ~ 4.6416 vs mass-fraction 6.694) | — | AC-PIPE-09 / EVID-10 verdict | ctl_instruction.md §2.5 line 598 explicitly rejects 6.694 form | Q-B4 | 2026-06-11 |
| footer | Footer/mass-drift protocol (np.allclose rtol=1e-15, decimal.Decimal fallback) | 26/27 (PIPE-06/07) | PENDING | — | YES — DATA-05 HELD behind GAP-24-01; verdict not recorded | — | AC-PIPE-06 / AC-PIPE-07 (gated on GAP-24-01) | ctl_instruction.md; pinn_architecture.md | Q-B2; D-12 anomaly | 2026-06-11 |
| mass-drift | Precision handling (float64 sufficiency; Decimal-for-masses) — DATA-05 verdict feeds this | 27 (PIPE-07) | PENDING | — | YES — DATA-05 HELD behind GAP-24-01; verdict not recorded | — | AC-PIPE-07 (gated on GAP-24-01) | ctl_instruction.md; pinn_architecture.md | Q-B3; D-12 anomaly | 2026-06-11 |

## Notes

19/19 issue-02 findings seeded at PENDING; full inventory per D-23 (the user's resolution
doc is the candidate verdict source; adjudication verdicts are Phase 25's to assign via
EVID-05..10). REQUIREMENTS.md traceability governs the Phase column; this ledger
initializes states only — Phase 25 owns the operating protocol (evidence-packet format,
verdict recording, re-verification rules per the Lifecycle Rules block below).

The **G1–G5 rows are rendered as separate rows per D-23** (the master's §"Inventory
Coverage Table" calls G1–G5 a "synthesis view" over constituent findings); each G-row's
Acceptance Check is the corresponding PIPE-0X acceptance check (synthesis view, not a
duplicate contract). **CLM-13 / `D=6.694` is PENDING** and routed Phase 25 EVID-10 /
Phase 27 PIPE-09 — it was NOT probed by Phase 24 (D-05).

The **footer** and **mass-drift** rows share a single HELD verdict gate: the DATA-05
finding (70/4,857 base-hier mass mismatches) is held behind GAP-24-01 (D-16 STOP gap,
semantic, **OPEN**). Their acceptance checks (`AC-PIPE-06` / `AC-PIPE-07`) cannot be
defined structurally until GAP-24-01 is resolved. Both rows are marked `Sources Disagree? =
YES` to reflect that the resolution-doc adjudication is the gating decision.

## Lifecycle Rules

The forward status path is exactly `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.

`DEFERRED` is an absorbing state and requires a written blocker. `FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check for the finding's AC-ID.

Audit string: FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check.

A batch is one GSD plan (`NN-NN-PLAN.md`). After every batch of spec or code edits in Phases 17-22, including Phase 20.5, the executing agent re-runs each `VERIFIED` finding's acceptance check if that finding appears as a transitive dependent of any finding edited by the batch. Any regression returns the affected finding to `IN_PROGRESS` and blocks phase exit until re-fixed and re-verified.

The phase-exit gate permits only `VERIFIED` or `DEFERRED` for in-scope findings. No phase exits with any in-scope finding at `IN_PROGRESS` or `FIX_APPLIED`.

## Dependency Source Note

Initial Dependents values use the master's §"Framed Research Questions" question blocks
(Q-A1..Q-A6, Q-B1..Q-B4, Q-C1..Q-C4). The `23-CLAIMS-INVENTORY.md` and REQUIREMENTS.md
traceability govern the Phase column and Acceptance Check column. The verified-facts
register `24-VERIFIED-FACTS.md` is the dataset-evidence annex (D-23).

## Per-Finding Notes

Status transition log entries must include date, commit short SHA, status transition, and actor / plan reference.

### B-06: Stage 4→5 validation gate (Phase 26 PIPE-01)

Acceptance check: AC-PIPE-01

Owning requirement: PIPE-01 (Stage 4→5 trajectory-validation gate contract).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### B-11: Non-contiguous IDs (Phase 26 PIPE-02)

Acceptance check: AC-PIPE-02

Owning requirement: PIPE-02 (ID-resolution contract).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### M11: Blacklist not loaded at training time (Phase 26 PIPE-03)

Acceptance check: AC-PIPE-03

Owning requirement: PIPE-03 (blacklist-exclusion contract).

Note: the CLM-03 count (65 IDs) is **confirmed** by Phase 24 (DATA-02 verdict
`24-VERIFIED-FACTS.md` row 16). The M11 consumption question remains PENDING — Phase 24
recorded the blacklist-load map under SCOPE-07 only; `pinn/` is outside grounding limits
(SCOPE-10) and the consumption contract is the PIPE-03 question.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### M12: Points-per-trajectory infeasibility (Phase 27 PIPE-04)

Acceptance check: AC-PIPE-04

Owning requirement: PIPE-04 (points-per-trajectory contract).

Note: Phase 24's CLM-10 row (snapshot-count distributions) is **corrected** (medians 61 /
127 / 1003); the PIPE-04 contract is the adjudicated sampling-feasibility rule that
consumes those distributions.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### M13: 184 standard IDs without gold counterpart (Phase 26 PIPE-05)

Acceptance check: AC-PIPE-05

Owning requirement: PIPE-05 (gold-counterpart contract + fallback policy).

Note: the CLM-04 count (184) is **confirmed**; the 184-ID list matches
`standard_quasi_random_ids_not_in_gold.md` exactly. The fallback policy (skip-to-Stage-6
vs flagged low-fidelity) is a **STOP-gap candidate** per the master's Q-A4; if the
resolution doc and the dataset are silent or conflicting on the fallback, surface as gap
rather than invent a policy.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### D7: Footer / parameter heterogeneity (Phase 26 PIPE-06)

Acceptance check: AC-PIPE-06

Owning requirement: PIPE-06 (footer/parameter-heterogeneity contract).

Note: CLM-07 count 219 confirmed; CLM-07 characterization corrected (no `Result:` footer
at all). CLM-08 (592 tol=1e-14) confirmed. CLM-09 (folder-defaults) confirmed. The
PIPE-06 contract consumes these confirmed facts.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### G1: Pipeline validation gap — synthesis view (B-06)

Acceptance check: AC-PIPE-01 (synthesis view over B-06; not a duplicate contract).

Owning requirement: PIPE-01 (synthesis view).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### G2: Pipeline validation gap — synthesis view (B-11)

Acceptance check: AC-PIPE-02 (synthesis view over B-11; not a duplicate contract).

Owning requirement: PIPE-02 (synthesis view).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### G3: Pipeline validation gap — synthesis view (M11)

Acceptance check: AC-PIPE-03 (synthesis view over M11; not a duplicate contract).

Owning requirement: PIPE-03 (synthesis view).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### G4: Pipeline validation gap — synthesis view (M13)

Acceptance check: AC-PIPE-05 (synthesis view over M13; not a duplicate contract).

Owning requirement: PIPE-05 (synthesis view).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### G5: dt_out heterogeneity (Phase 27 PIPE-04, data-side facet)

Acceptance check: AC-PIPE-04 (data-side facet only; M16 collocation-scaling facet
deferred to doc-03 per SCOPE-11).

Owning requirement: PIPE-04 (data-side facet; M16 deferred).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### SCS: Symplectic Conservation Score (Phase 28 VAL-01)

Acceptance check: AC-VAL-01

Owning requirement: VAL-01 (SCS contract).

Sources disagree: YES — the issue doc's ratio-based thresholds (`> 1e-6` / `< 1e-8`)
conflict with the locked post-v1.3 gate (`epsilon_H > 1e-5` / `SCS > -5`). EVID-10
required. The locked gate's sole written home is the read-only,
non-authoritative `data_quality_assessment.md` (SI-DQA-003).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### SASD: Stiffness-Aware Sampling Density (Phase 28 VAL-02)

Acceptance check: AC-VAL-02

Owning requirement: VAL-02 (SASD data-side contract; training-loop usage deferred to
doc-03 per SCOPE-11).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### IPR: Interpolation Physics Residual (Phase 28 VAL-03)

Acceptance check: AC-VAL-03

Owning requirement: VAL-03 (IPR data-side contract; ALM noise-floor role deferred to
doc-03 per SCOPE-11).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### PSC: Phase Space Coverage Entropy (Phase 28 VAL-04)

Acceptance check: AC-VAL-04

Owning requirement: VAL-04 (PSC data-side contract; replay-governance use deferred to
doc-03 per SCOPE-11).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### D-03: Processed training-data format (Phase 26 PIPE-10)

Acceptance check: AC-PIPE-10

Owning requirement: PIPE-10 (training-data format decision).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### D=6.694: compute_globals / D=6.694 convention conflict (Phase 25 EVID-10 / Phase 27 PIPE-09)

Acceptance check: AC-PIPE-09 / EVID-10 verdict

Owning requirement: PIPE-09 (global-scale computation contract).

Sources disagree: YES — issue doc derives `D = cbrt(G * M_tot * t_max^2) = 6.694`; locked
v1.4 PHYS-01 fixes raw-mass `D = (G * T^2)^(1/3) ~ 4.6416` and `ctl_instruction.md` §2.5
line 598 **explicitly rejects** the 6.694 form. NOT probed by Phase 24 (D-05; not a dataset
count, a contested convention). EVID-10 required. Routed Phase 25 EVID-10 / Phase 27 PIPE-09.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### footer: Footer/mass-drift protocol (Phase 26/27 PIPE-06/07)

Acceptance check: AC-PIPE-06 / AC-PIPE-07 (gated on GAP-24-01)

Owning requirement: PIPE-06 (footer-heterogeneity) / PIPE-07 (precision contract).

Sources disagree: YES — DATA-05 verdict is **HELD behind GAP-24-01** (D-16 STOP gap,
semantic, OPEN). The protocol question (tolerance, sample size, Decimal-for-masses
fallback) cannot be answered structurally until the user adjudicates GAP-24-01. Phase 24
recorded the protocol as an **anomaly** (D-12) per the verified-facts register; the PIPE-07
verdict is gated.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### mass-drift: Precision handling (Phase 27 PIPE-07)

Acceptance check: AC-PIPE-07 (gated on GAP-24-01)

Owning requirement: PIPE-07 (precision contract — float64 sufficiency; Decimal-for-masses).

Sources disagree: YES — DATA-05 (HELD behind GAP-24-01). The verdict on whether float64
is sufficient for validation metrics or `decimal.Decimal` is required for mass consistency
cannot be assigned until GAP-24-01 is resolved. The agent was tempted to record
"decimal.Decimal parsing required" as a verdict (this would have been the wrong framing —
the 70 base-hier differences are 0.1-1.0 in mass units, not 1e-15; precision does not
explain them); instead the row is HELD, not invented (D-16).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

## Dataset Evidence Annex

Linked: `24-VERIFIED-FACTS.md` (stable path:
`.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`)

The verified-facts register is the dataset-evidence annex for every CLM- and DATA-keyed
finding above. Each row carries the exact repo-root probe command, the dataset path it
ran against, the observed value, the verdict (`confirmed` / `corrected` / `unverified`), and
the run date (D-02 re-derivability). The DATA-05 row (held behind GAP-24-01) and the
CLM-13 row (PENDING, not probed) are recorded in the register's dedicated sections.

## Anomalies (D-12)

- **DATA-05 / base-hier mass-drift**: 70/4,857 files in `brutus_hierarchical` show
  m_Brutus(t=0) ≠ m_IC at `np.allclose(rtol=1e-15)`. Standard deviation 0.1-1.0 mass
  units. Not explained by float64 round-trip or perturbation. Gold-hier matches perfectly
  (0/4,857 mismatches). Provenance ambiguous — base vs gold runner reads the same IC
  file but produces different t=0 masses for the same 70 IDs. **HELD behind GAP-24-01**
  (D-16 STOP gap, semantic, OPEN). See `.planning/milestones/v1.5-GAPS.md` and
  `24-GAPS.md`. **Blocks Phase 24 closure AND PIPE-07 (Phase 27) consumption per P0-2**
  until the user adjudicates GAP-24-01.

- **Standard 2,749-vs-2,750 arithmetic wrinkle**: 1,250 gaps from `gaps[0..max]` per the
  README's ID Range convention (`simulation_data/Documentation/README.md:146-153` declares
  ID Range `0000-3998` for standard, `0000-4999` for hierarchical; the README's "Gaps"
  column equals 1,250 / 143). Resolved as **no off-by-one**: `gaps[0..max]` is the
  authoritative gap count, matching the README convention; the
  `gaps[0..3999] = 1,251` (standard) is a non-canonical artifact included for
  transparency. The 2,749 base count and the 1,250 gap count reconcile exactly.

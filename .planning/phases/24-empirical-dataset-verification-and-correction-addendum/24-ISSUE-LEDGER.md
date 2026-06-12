---
phase: 24-empirical-dataset-verification-and-correction-addendum
slug: dataset-verification-and-correction-addendum
status: seeded-complete
created: 2026-06-11
last_updated: 2026-06-11
total_findings: 19
in_scope_findings: 19
deferred_findings: 0
traceability_verified: true
data05_resolution: RESOLVED-WITH-INSTRUCTION
data05_resolution_doc: 24-DATA05-RERUN-REMEDIATION.md
last_verified_traceability: "19/19 issue-02 findings seeded; verified against 23-CLAIMS-INVENTORY.md and REQUIREMENTS.md traceability; DATA-05 row resolved 2026-06-11 (current ICs canonical; 70 base-hier outputs quarantined pending rerun; remediation contract in 24-DATA05-RERUN-REMEDIATION.md)"
phase_closure_note: "Phase 24 deliverable complete. Phase 25 owns the operating protocol (evidence-packet format, verdict recording, re-verification rules per the Lifecycle Rules block below). 70-file DATA-05 rerun is a separate remediation operation, not a Phase 24 closure prerequisite."
---

# Phase 24 Issue Ledger

## Status Table

| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| B-06 | Stage 4→5 validation gate (trajectory-validator at DataLoader init) | 26 (PIPE-01) | PENDING | — | NO | — | AC-PIPE-01 | ctl_instruction.md; pinn_architecture.md | Q-A1 | 2026-06-11 |
| B-11 | Non-contiguous IDs (ID ≠ array index; id_to_path / TrajectoryIndex contract) | 26 (PIPE-02) | PENDING | — | NO | — | AC-PIPE-02 | ctl_instruction.md; pinn_architecture.md | Q-A2 | 2026-06-11 |
| M11 | Blacklist not loaded at training time (consumption contract) | 26 (PIPE-03) | PENDING | **BLOCKING STANDS** (M11 explicit severity ruling; data-integrity grounds; OI-8 carried forward) | NO | [m11-m12-severity.md](../25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md) | AC-PIPE-03 | ctl_instruction.md; pinn_architecture.md | Q-A3 | 2026-06-12 |
| M12 | Points-per-trajectory infeasibility (32 vs observed snapshot distribution) | 27 (PIPE-04) | PENDING | `accept-third-position` (BLOCKING-infeasibility claim rejected; P1-4 `0.5×` factor rejected) | NO | [m11-m12-severity.md](../25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md) | AC-PIPE-04 | ctl_instruction.md | Q-B1 | 2026-06-12 |
| M13 | 184 standard IDs without gold counterpart (fallback policy) | 26 (PIPE-05) | PENDING | — | NO | — | AC-PIPE-05 | ctl_instruction.md; pinn_architecture.md | Q-A4 | 2026-06-11 |
| D7 | Footer / parameter heterogeneity (folder-default fallback, tol_confidence) | 26 (PIPE-06) | PENDING | — | NO | — | AC-PIPE-06 | ctl_instruction.md; pinn_architecture.md | Q-A5 | 2026-06-11 |
| G1 | Pipeline validation gap — synthesis view (B-06) | 26 (PIPE-01) | PENDING | — | NO | — | AC-PIPE-01 (synthesis view over B-06) | ctl_instruction.md; pinn_architecture.md | B-06 | 2026-06-11 |
| G2 | Pipeline validation gap — synthesis view (B-11) | 26 (PIPE-02) | PENDING | — | NO | — | AC-PIPE-02 (synthesis view over B-11) | ctl_instruction.md; pinn_architecture.md | B-11 | 2026-06-11 |
| G3 | Pipeline validation gap — synthesis view (M11) | 26 (PIPE-03) | PENDING | — | NO | — | AC-PIPE-03 (synthesis view over M11) | ctl_instruction.md; pinn_architecture.md | M11 | 2026-06-11 |
| G4 | Pipeline validation gap — synthesis view (M13) | 26 (PIPE-05) | PENDING | — | NO | — | AC-PIPE-05 (synthesis view over M13) | ctl_instruction.md; pinn_architecture.md | M13 | 2026-06-11 |
| G5 | dt_out heterogeneity (data-side; Q-B1 facet; collocation-scaling facet M16 deferred to doc-03) | 27 (PIPE-04) | PENDING | — | NO | — | AC-PIPE-04 (data-side facet; M16 training-side deferred) | ctl_instruction.md; pinn_architecture.md | M12; M16-deferred | 2026-06-11 |
| SCS | Symplectic Conservation Score definition + thresholds (data-side; Q-C1) | 28 (VAL-01) | PENDING | `accept-resolution` | YES — EVID-10 required (ratio-SCS vs locked log-drift gate) | [scs-thresholds.md](../25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md) | AC-VAL-01 | data_quality_assessment.md (read-only; sole written home of locked gate) | Q-C1 | 2026-06-12 |
| SASD | Stiffness-Aware Sampling Density (data-side; Q-C2) | 28 (VAL-02) | PENDING | — | NO | — | AC-VAL-02 | ctl_instruction.md; pinn_architecture.md | Q-C2 | 2026-06-11 |
| IPR | Interpolation Physics Residual (data-side, dual-epsilon; Q-C3) | 28 (VAL-03) | PENDING | — | NO | — | AC-VAL-03 | ctl_instruction.md; pinn_architecture.md | Q-C3 | 2026-06-11 |
| PSC | Phase Space Coverage Entropy (data-side; Q-C4) | 28 (VAL-04) | PENDING | — | NO | — | AC-VAL-04 | ctl_instruction.md; pinn_architecture.md | Q-C4 | 2026-06-11 |
| D-03 | Processed training-data format (HDF5 vs .npy vs txt/json) | 26 (PIPE-10) | PENDING | — | NO | — | AC-PIPE-10 | ctl_instruction.md | Q-A6 | 2026-06-11 |
| D=6.694 | compute_globals / D=6.694 convention conflict (CLM-13) — NOT probed by Phase 24; routed to Phase 25 EVID-10 / Phase 27 PIPE-09 | 25 (EVID-10) / 27 (PIPE-09) | PENDING | `accept-resolution` (CLM-13 ratified `convention-rejected`) | YES — EVID-10 required (PHYS-01 raw-mass D ~ 4.6416 vs mass-fraction 6.694) | [compute-globals-D.md](../25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md) | AC-PIPE-09 / EVID-10 verdict | ctl_instruction.md §2.5 line 598 explicitly rejects 6.694 form | Q-B4 | 2026-06-12 |
| footer | Footer/mass-drift protocol (np.allclose rtol=1e-15, decimal.Decimal fallback) | 26/27 (PIPE-06/07) | PENDING | — | NO — GAP-24-01 resolved by user instruction; 70 base-hier artifacts required rerun, not Decimal fallback (rerun executed+validated 2026-06-11) | `24-DATA05-RERUN-REMEDIATION.md` | AC-PIPE-06 / AC-PIPE-07 (consume remediated/quarantined DATA-05 state) | ctl_instruction.md; pinn_architecture.md | Q-B2; D-12 anomaly; DATA-05 remediation | 2026-06-11 |
| mass-drift | Precision handling (float64 sufficiency; Decimal-for-masses) — DATA-05 verdict feeds this | 27 (PIPE-07) | PENDING | — | NO — DATA-05 resolved as invalid/stale base-hier artifacts; rerun passed 2026-06-11, replacements live; metrics for the 70 IDs regenerated and validated 2026-06-11 (gate 7 closed) | `24-DATA05-RERUN-REMEDIATION.md` | AC-PIPE-07 (consume remediated/quarantined DATA-05 state) | ctl_instruction.md; pinn_architecture.md | Q-B3; D-12 anomaly; DATA-05 remediation | 2026-06-11 |

## Notes
- **2026-06-12:** D-11 re-issue: the Lifecycle Rules block's stale v1.4 applicability text (the v1.4-era phase range that named the old spec-edit phases and the inserted phase) was mechanically updated to the v1.5 spec-edit phases (now 26-28 with Phase 29 as the acceptance phase). State machine, batch definition, regression policy, and phase-exit gate preserved verbatim per D-11 KEEP-VERBATIM list. Only the stale applicability token changed; the per-finding rows, Status Table, and Anomalies section are untouched (Plan 25-02 fills the three EVID-10 rows' Evidence-Packet links and per-finding verdict notes in its own commit, per D-06).

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

The **footer** and **mass-drift** rows no longer have an OPEN DATA-05 STOP gate. The
DATA-05 finding (70/4,857 base-hier mass mismatches) is resolved by user instruction:
current ICs are canonical; the 70 old base-hier outputs are invalid/stale artifacts that
must be rerun, not skipped and not explained by `decimal.Decimal` precision. The rows
remain PENDING because Phases 26/27 still own the PIPE-06/07 contracts, but those phases
consume the resolved remediation boundary rather than an open gap.

**Remediation execution update (2026-06-11):** the 70-file rerun was executed and
validated the same day (70/70 gates passed; post-swap DATA-05 probe 0/4857; old
artifacts archived under `simulation_data/Data/forensic/data05_gap24-01_old_outputs/`).
The trajectory-file quarantine is lifted; the metrics for the 70 IDs were regenerated
and validated later the same day (gate 7 closed — all eight remediation gates closed).
Evidence: `24-DATA05-RERUN-REMEDIATION.md` "Execution Evidence".

## Lifecycle Rules

The forward status path is exactly `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.

`DEFERRED` is an absorbing state and requires a written blocker. `FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check for the finding's AC-ID.

Audit string: FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check.

A batch is one GSD plan (`NN-NN-PLAN.md`). After every batch of spec or code edits in Phases 26-28 (spec-edit phases; Phase 29 is the acceptance phase), the executing agent re-runs each `VERIFIED` finding's acceptance check if that finding appears as a transitive dependent of any finding edited by the batch. Any regression returns the affected finding to `IN_PROGRESS` and blocks phase exit until re-fixed and re-verified.

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

Verdict: **M11 explicit severity ruling — MAJOR → BLOCKING reclassification
STANDS** (Phase 25 P02 EVID-10 record `evidence/m11-m12-severity.md`; grounded
on the data-integrity argument: IC-level exclusion via byte-identical-subset,
before-statistics ordering prevents normalizer contamination, fail-closed follows
from the exclusion guarantee). The M11 *consumption* question (does the live
loader enforce the blacklist?) is **OI-8, carried forward** to Phase 26 PIPE-03
/ FUT-01 per SCOPE-10; not resolved here, not blocking the severity ruling.
**D-12 (synthesis-view close-with-parent):** G3 closes with M11 — no separate
evidence packet. **M11 GUARD (D-10) not triggered:** all four objective guard
triggers checked at authoring time — none fired (resolution doc routes M11 to
determinate data-integrity argument, not Open Items; §3.3 part 2 grounding
present; OI-8 is a carry-forward caveat, not a severity-decision blocker;
CLM-03 confirmed). Prioritization owned by Phase 26 PIPE-03.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
- 2026-06-12 e05b4b1a PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + M11 explicit severity ruling **BLOCKING STANDS**; OI-8 carried forward; D-12 G3->M11 close-with-parent; prioritization owned by Phase 26 PIPE-03)

### M12: Points-per-trajectory infeasibility (Phase 27 PIPE-04)

Acceptance check: AC-PIPE-04

Owning requirement: PIPE-04 (points-per-trajectory contract).

Note: Phase 24's CLM-10 row (snapshot-count distributions) is **corrected** (medians 61 /
127 / 1003); the PIPE-04 contract is the adjudicated sampling-feasibility rule that
consumes those distributions.

Verdict: `accept-third-position` (Phase 25 P02 EVID-10 record
`evidence/m11-m12-severity.md`; BLOCKING-infeasibility claim is falsified on the
corrected CLM-10 medians — `32 ≤ 59` is trivially feasible; the P1-4
`n_pts = min(32, int(0.5·n_snapshots))` factor is rejected as unevidenced and
internally inconsistent with the issue doc's own verification checklist).
Locked data-side contract: `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`
without replacement. **D-12 (synthesis-view close-with-parent):** G5 closes
with M12 — no separate evidence packet. Fix owned by Phase 27 PIPE-04.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
- 2026-06-12 e05b4b1a PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + M12 `accept-third-position` verdict; fix owned by Phase 27 PIPE-04; D-12 G5->M12 close-with-parent)

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

Verdict: `accept-resolution` (Phase 25 P02 EVID-10 record
`evidence/scs-thresholds.md`; locked post-v1.3 gate `SCS > -5` (≡ `ε_H > 1e-5`) is
constraint-entailed; the issue-doc `1e-6` is the Acceptable/Marginal band boundary
mis-promoted to a gate, `1e-8` is an unsourced proposal). Fix owned by Phase 28
VAL-01 (transcription of the locked gate into `ctl_instruction.md`; DQA remains
read-only per SCOPE-09).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
- 2026-06-12 e05b4b1a PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + `accept-resolution` verdict assigned; fix owned by Phase 28 VAL-01)

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

Verdict: `accept-resolution` (Phase 25 P02 EVID-10 record
`evidence/compute-globals-D.md`; raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` is
constraint-entailed; the issue-doc listing has three verified defects — mixed
convention, additive-ε anti-pattern, `E_scale` outlier). **OI-11 (CLM-13
ratification, D-15/D-16):** the `24-VERIFIED-FACTS.md` CLM-13 row is formally
ratified by this EVID-10 record with disposition `convention-rejected` (no
dataset probe required; the finding is a convention adjudication, not a count).
Fix owned by Phase 27 PIPE-09 (transcription of the locked convention into
`ctl_instruction.md §2.5`, including the `E_scale = |median(E)| + 1e-8`
canonicalization as a 2-of-3 editable-spec choice).

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)
- 2026-06-12 e05b4b1a PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + `accept-resolution` verdict + CLM-13 ratified `convention-rejected`; fix owned by Phase 27 PIPE-09; OI-11 propagated)

### footer: Footer/mass-drift protocol (Phase 26/27 PIPE-06/07)

Acceptance check: AC-PIPE-06 / AC-PIPE-07 (consume remediated/quarantined DATA-05 state)

Owning requirement: PIPE-06 (footer-heterogeneity) / PIPE-07 (precision contract).

Sources disagree: NO for the DATA-05 baseline decision. GAP-24-01 is
`RESOLVED-WITH-INSTRUCTION`: current ICs are canonical; the 70 affected base-hier outputs
are invalid/stale artifacts requiring targeted rerun; this is not a Decimal-for-masses
fallback. Phase 24 records the protocol as an **anomaly** (D-12) plus a remediation
boundary; PIPE-06/07 must not consume the old 70 outputs until rerun validation passes.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

### mass-drift: Precision handling (Phase 27 PIPE-07)

Acceptance check: AC-PIPE-07 (consume remediated/quarantined DATA-05 state)

Owning requirement: PIPE-07 (precision contract — float64 sufficiency; Decimal-for-masses).

Sources disagree: NO for the DATA-05 precision decision. DATA-05 is
`RESOLVED-WITH-INSTRUCTION`: the 70 base-hier differences are 0.1-1.0 in mass units, not
1e-15; precision does not explain them. The current IC files are canonical, and the old
70 base-hier outputs are invalid/stale artifacts that must be rerun from current ICs
before training, metrics, or PIPE-07 consume them.

Status transition log:
- 2026-06-11 SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)

## Dataset Evidence Annex

Linked: `24-VERIFIED-FACTS.md` (stable path:
`.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`)

The verified-facts register is the dataset-evidence annex for every CLM- and DATA-keyed
finding above. Each row carries the exact repo-root probe command, the dataset path it
ran against, the observed value, the verdict (`confirmed` / `corrected` / `unverified`), and
the run date (D-02 re-derivability). The DATA-05 row is resolved-with-instruction and
points to `24-DATA05-RERUN-REMEDIATION.md`; the CLM-13 row (PENDING, not probed) is
recorded in the register's dedicated section.

## Anomalies (D-12)

- **DATA-05 / base-hier mass-drift**: 70/4,857 files in `brutus_hierarchical` show
  m_Brutus(t=0) != m_IC at `np.allclose(rtol=1e-15)`. Differences are 0.1-1.0 mass
  units. Not explained by float64 round-trip or perturbation. Gold-hier matches perfectly
  (0/4,857 mismatches). User instruction 2026-06-11 resolves GAP-24-01: current ICs are
  canonical; the 70 affected base-hier outputs (`0005`-`0059`, `0061`-`0075`) are
  invalid/stale artifacts requiring targeted rerun from current ICs. The old artifacts
  are quarantined from training, metrics, and PIPE-07 until rerun validation passes. See
  `.planning/milestones/v1.5-GAPS.md`, `24-GAPS.md`, and
  `24-DATA05-RERUN-REMEDIATION.md`.

- **Standard 2,749-vs-2,750 arithmetic wrinkle**: 1,250 gaps from `gaps[0..max]` per the
  README's ID Range convention (`simulation_data/Documentation/README.md:146-153` declares
  ID Range `0000-3998` for standard, `0000-4999` for hierarchical; the README's "Gaps"
  column equals 1,250 / 143). Resolved as **no off-by-one**: `gaps[0..max]` is the
  authoritative gap count, matching the README convention; the
  `gaps[0..3999] = 1,251` (standard) is a non-canonical artifact included for
  transparency. The 2,749 base count and the 1,250 gap count reconcile exactly.

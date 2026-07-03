<!-- generated-by: gsd-doc-writer -->

# Testing and Acceptance

This document describes how the project's adjudication milestones are tested, verified, and
closed, using the **v1.5 ("Resolving 02 Data Pipeline and Validation")** acceptance suite as
the worked example — the most recent *completed* acceptance work (v1.5 shipped 2026-06-17).
It is the project-side view of the v1.5 acceptance and issue-ledger machinery landed across
Phases 25-29, not a generic software-testing guide.

> **Current milestone (v1.6 "Resolving 03 Curriculum and Training Loop", Phases 30-36, in
> progress).** v1.6 follows the same disposable-probe / issue-ledger / closure-gate pattern
> documented here. Its acceptance checks (VER-13..18) are **executed in Phase 36, which has
> not yet run**; the v1.6 issue ledger lives under the Phase 32 (evidence-framework)
> directory. Until Phase 36 lands, the v1.5 suite below is the canonical example of the
> testing discipline.

The adjudication-milestone contract is **spec-side**: production DataLoader, TrajectoryValidator,
and training code are out of scope (FUT-01 implements them). The acceptance surface therefore
tests the **framework specs** and the **canonical dataset** with disposable probes, never the
live `pinn/` code (SCOPE-10).

## Test layers

Three distinct layers are exercised at v1.5 closure. Each layer has its own probe pattern
and its own place in the AC-PIPE-* / AC-VAL-* taxonomy.

| Layer | What is tested | Probe pattern | Taxonomy |
|---|---|---|---|
| Pipeline contract | DataLoader-init behaviors: admission gate, ID resolution, blacklist exclusion, footer, processed-format, n_pts, precision handling, global-scale constants | Grep over `ctl_instruction.md` / `pinn_architecture.md` for landed clauses + a dataset set-difference probe | AC-PIPE-01 ... AC-PIPE-10 |
| Validation metric | Step-1A conservation gate (SCS) and the SASD / IPR / PSC data-side quality-metric clauses | Grep over `ctl_instruction.md` for the landed metric clause + EPS/D-01/dual-epsilon/grid/dedup/`1/N_t` markers | AC-VAL-01 ... AC-VAL-04 |
| Issue ledger | Status transitions of every in-scope finding row, plus the milestone-closure gate (G1-G8) | Python enumeration of the ledger Status Table; `run-ac-suite.sh` exit code; non-terminal count = 0 | VER-07, VER-08, VER-09, VER-11, VER-12 |

Probes are checked in under `.planning/phases/<NN-...>/ac-*.sh`, `ac-*.py`, and
`run-ac-suite.sh`. They are disposable: a probe re-run produces a fresh pass/fail line.
The Phase-29 driver script `run-ac-suite.sh` re-runs the full 13-check suite and exits
0 on success.

## Acceptance-check naming

`AC-PIPE-NN` covers the pipeline contract axis; `AC-VAL-NN` covers the validation-metric
axis. AC IDs map one-to-one to issue-ledger rows in `24-ISSUE-LEDGER.md`; every AC must
have a resolving Phase column.

| AC | Resolves | What it asserts (numeric / structural) | Source evidence |
|---|---|---|---|
| AC-PIPE-01 | B-06 / G1 | Step-1A admission gate landed in `ctl_instruction.md` | `ctl_instruction.md:452` |
| AC-PIPE-02 | B-11 / G2 | `id_to_path` non-contiguous-ID contract landed | `ctl_instruction.md` Step-1 ID-resolution |
| AC-PIPE-03 | M11 / G3 | Blacklist-exclusion contract landed (fail-closed; `physical_key` semantics) | `ctl_instruction.md:518-560` |
| AC-PIPE-04 | M12 / G5 | `n_pts = min(n_pts_cap, n_snapshots)` rule landed; AC-PIPE-08 stage-query re-run is part of this family line | Phase 27 probe `ac-pipe-04.sh` |
| AC-PIPE-05 | M13 / G4 | 184 standard IDs without gold counterpart - fallback policy landed; dataset probe returns 184/184 with 0 promoted under D-01 | `ac-pipe-05.py` (set-difference; no hard-coded counts) |
| AC-PIPE-06 | D7 | Footer / parameter-provenance contract landed | `ctl_instruction.md` |
| AC-PIPE-07 | mass-drift | Precision handling: float64 sufficiency; DATA-05 verdict, not Decimal fallback | `ctl_instruction.md` |
| AC-PIPE-08 | (no standalone row) | Stage-query contract landed - executed as part of AC-PIPE-04 family line | Phase 27 probe `ac-pipe-08.sh` |
| AC-PIPE-09 | D=6.694 | `compute_globals` raw-mass `D ≈ 4.6416`; the `6.694` value is rejected by name | `ac-pipe-09.sh` (Phase 27) |
| AC-PIPE-10 | D-03 | Processed training-data format (HDF5 canonical) | `ac-pipe-10.sh` |
| AC-VAL-01 | SCS | Step-1A conservation gate landed: `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, reject if `SCS > -5` | `ctl_instruction.md:474-498` |
| AC-VAL-02 | SASD | SASD clause landed with both-endpoint convention and `dt * ||a|| / ||v||` formula | `ctl_instruction.md:578-608` |
| AC-VAL-03 | IPR | IPR clause landed with `CubicHermiteSpline` (not `Pchip`), raw `G = 1` units, dual-epsilon consistency | `ctl_instruction.md:610-643` |
| AC-VAL-04 | PSC | PSC clause landed (Shannon entropy, dedup-prefer-gold, `1/N_t` composition); numeric axis is DEFERRED to FUT-01 FO-2 | `ctl_instruction.md:645-692` |

AC-PIPE-08 has no standalone ledger row; it is re-run inside the AC-PIPE-04 / G5 family
line and noted under G5 (matching the `29-UAT.md` table shape). AC-VAL-04 is a two-axis
check: the **structural** axis (clause landed, dedup-prefer-gold + `1/N_t` composition,
provisional constants marked) executes now; the **numeric** axis (the actual
PSC computation on the final post-promotion pool) is DEFERRED to FUT-01 FO-2 because
the construction constants depend on the post-promotion population.

## Validation-metric contracts (SCS, SASD, IPR, PSC)

All four metrics are defined in `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
under **Step 1A - Trajectory Admission Gate** (clause 5) and the **Data-side
quality-metric contracts (SASD, IPR, PSC)** subsection. They are computed from the raw
parsed arrays under the locked `G = 1`, raw-mass convention (PIPE-09, `ctl_instruction.md`
§2.5). Every metric is unit-bound; raw vs scaled readings differ by a known factor
(~464x for IPR under the locked global scale) and must not be mixed.

### SCS - Symplectic Conservation Score (Step-1A clause 5, the only reject gate)

The Hamiltonian relative-drift gate, the family's only **reject** gate:

```
eps_H = max_t |(H(t) - H(0)) / H(0)|     (float64, Plummer softening eps = 1e-10 in V)
SCS   = log10(eps_H)
```

| `eps_H` band | `SCS` band | Disposition |
|---|---|---|
| `eps_H = 0` | `SCS = -inf` | Excellent |
| `eps_H <= 1e-10` | `SCS <= -10` | Excellent |
| `1e-10 < eps_H <= 1e-6` | `-10 < SCS <= -6` | Acceptable |
| `1e-6 < eps_H <= 1e-5` | `-6 < SCS <= -5` | Marginal (admitted, flagged) |
| `eps_H > 1e-5` | `SCS > -5` | **Reject** |

If `|H(0)|` is numerically near zero, SCS is **undefined**: QUARANTINE for manual
review. Do not introduce a denominator floor. `eps_H` and the SCS band decision are
invariant to raw/scaled units under the locked global scaling (`H' = D * H`), so the
admission check is computed from the raw parsed arrays by convention. This validation
`eps_H` is distinct from the training-loss `eps_H = 1e-4 * S_H` in
`pinn_architecture.md` §3.4 - same glyph, different quantity, and the validation gate
is not changed by the training symbol.

The issue-02 ratio thresholds are rejected by name, not transcribed: `1e-6` is the
Acceptable/Marginal band boundary (`SCS = -6`) mis-promoted to a reject gate, and
`1e-8` is an unsourced tightening proposal with no package basis. Adjudication record:
`.planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md`.

### SASD - Stiffness-Aware Sampling Density (VAL-02; flag, not reject)

Scale-invariant local timestep adequacy diagnostic; **flag-for-resampling**, never
auto-reject:

```
SASD_i = dt_i * max_b max_{t in {t_i, t_{i+1}}} ( ||a_b(t)|| / max(||v_b(t)||, 1e-12) )
trajectory score = max_i SASD_i
```

`a_b` is the analytic per-body acceleration from the snapshot positions with Plummer
softening `eps = 1e-10` (validation softening; enters `V` only). Both-endpoint
evaluation is the canonical convention (GAP-28-01 RESOLVED-WITH-INSTRUCTION, user
sign-off 2026-06-16) - it dominates the DQA-literal left-endpoint form
(`max(left, right) >= left`) and closes the right-endpoint blind spot a left-only
evaluation never sees.

| Item | Value | Status |
|---|---|---|
| Formula | `dt * max_b ||a_b|| / max(||v_b||, 1e-12)`, both endpoints | Locked |
| Per-body acceleration norm | `||a_b||` (not 9-component stack; not perpendicular) | Locked |
| `eps` (validation softening) | `1e-10` | Locked |
| Flag threshold | `max_i SASD_i > 0.5` | **Provisional** - recalibrate to admitted-set `max SASD` at doc-03 / FUT-01 |
| Disposition | Flag -> resample queue; withhold from clean-training designation; **not** auto-reject | Locked |
| Low-resolution floor effect | An encounter completing entirely between two snapshots is invisible; SASD pairs with IPR by design | Documented |
| Training-side collocation use (M16) | Deferred to doc-03 | Forward-reference |

### IPR - Interpolation Physics Residual (VAL-03; flag, not reject)

Dimensionful acceleration-squared interpolation residual, **flag-for-resampling**:

```
IPR = (1 / M_total) * sum_k || q''_spline(tau_k) - F_grav^eps(q_spline(tau_k)) ||^2
M_total = 10 * (n_snapshots - 1)
tau_{i,j} = t_i + (j - 1/2) * dt_i / 10,   j = 1..10
```

The interpolant is **`CubicHermiteSpline(t, q, dydx=v)`**, built from snapshot positions
`q` and recorded file velocities `v`. `PchipInterpolator(t, q)` is **prohibited**: it
discards recorded velocities and synthesizes slopes from shape, yielding a different
spline whose second derivative diverges most near encounters. Evaluation points are
the 10 deterministic mid-offset interior points per interval - never at knots, never
random.

| Item | Value | Status |
|---|---|---|
| Spline | `CubicHermiteSpline(t, q, dydx=v)` | Locked; `PchipInterpolator` rejected by name |
| Interior points per interval | 10 (`tau_{i,j} = t_i + (j - 1/2) * dt_i / 10`) | Locked |
| `eps_inv` (data-side validation softening) | `1e-10` (static invariant softening) | Locked |
| Units | **Raw `G = 1` on the parsed arrays** | Locked (GAP-28-02 RESOLVED-WITH-INSTRUCTION) |
| Raw/scaled numeric difference | ~464x under the locked global scale | Documented; the gate is unit-bound |
| Flag threshold | `IPR > 1e-3` (raw units) | **Provisional** - recalibrate at doc-03 / FUT-01 |
| Disposition | Flag -> resample queue; same flag-not-auto-reject as SASD | Locked |
| `IPR_train` (training-time, `epsilon_train = 1e-5`) | Distinct quantity; ALM noise-floor role | Deferred to doc-03 |
| Dual-epsilon consistency (PHYS-03) | Data-side `eps_inv = 1e-10`; training `epsilon_train = 1e-5` are **different** quantities | Locked; clause does not conflate |

### PSC - Phase-Space Coverage Entropy (VAL-04; report only)

Dataset-level, **report-only coverage diagnostic** - no per-trajectory flag, no
admission/reject authority. Reports how completely the admitted population samples
phase space:

```
PSC = - sum_b p_b * log p_b
```

`b` indexes grid cells; `p_b` is the pooled occupancy fraction in cell `b`. A companion
**SCR** (close-encounter coverage ratio) reports the pooled fraction of records whose
scaled minimum pair-distance falls in the near-singular region, so the diagnostic
cannot certify coverage while the chaotic close-encounter tail is empty.

Pooled-population composition (GAP-28-03 RESOLVED-WITH-INSTRUCTION, user sign-off
2026-06-16):

- **Dedup-prefer-gold**: one record per `physical_key`, preferring the gold realization
  where present and falling back to base. The 67 permanent `gold_counterpart = absent`
  ICs enter via base.
- **`1/N_t` weighting**: each surviving trajectory contributes unit total mass; each
  snapshot is weighted by `1 / N_t(record)` (`N_t` = the record's snapshot count).
  Trajectory-equal (not snapshot-equal) weighting neutralizes the base/gold
  snapshot-count asymmetry (gold `dt_out = 0.01`, ~1003 snapshots; base
  `dt_out = 0.17`, ~61).
- The two operations are orthogonal - dedup removes physical-system duplication,
  `1/N_t` removes resolution skew - and together make PSC an honest coverage
  statistic under the dataset's MNAR gold censoring.

| Item | Value | Status |
|---|---|---|
| Pooled-population composition | dedup-prefer-gold + `1/N_t` (trajectory-equal) | **Ratified** (GAP-28-03) |
| Units | Raw `G = 1`, raw-mass, consistent with companion metrics | Locked |
| Phase-space coordinates (candidate) | sorted scaled pair-distances, permutation-invariant | Provisional |
| Grid (candidate) | log-spaced bins on `[1e-3, 1e2]`, 25 per axis, `K = 625` | Provisional - first-run sanity at FUT-01 |
| Estimator normalization (candidate) | `H_norm = H / ln K`, with Miller-Madow correction **reported**, not silently added | Provisional |
| SCR anchor (candidate) | scaled `d_min < 0.5` (Stage-6 anchor) | Provisional |
| Disposition | Report only; no per-trajectory flag; no admission/reject | Locked |
| Replay-governance / training-side use | Deferred to doc-03 | Forward-reference |
| Numeric axis | **DEFERRED** to FUT-01 FO-2 (post-promotion pool) | See 29-CODE-DIVERGENCE.md FO-2 |

The naive all-snapshot pooled value is confounded by both resolution mix and base/gold
duplication and is **not** a deliverable.

## Running the v1.5 acceptance suite

The Phase-29 driver script re-runs the entire 13-check suite as fresh disposable probes
and emits one result line per check. Probes test the specs and the dataset - they
never touch `pinn/` production code (SCOPE-10 / VER-09).

```bash
bash .planning/phases/29-acceptance-checks-re-verification-and-handoff/run-ac-suite.sh
```

Expected outcome (v1.5 closure):

```
=== v1.5 Acceptance Suite — fresh Phase-29 re-run (2026-06-17T...) ===
AC-PIPE-01: PASS
AC-PIPE-02: PASS
AC-PIPE-03: PASS
AC-PIPE-04: PASS (M12/G5 family; AC-PIPE-08 stage-query re-run PASS, noted under G5)
AC-PIPE-05: PASS
AC-PIPE-06: PASS
AC-PIPE-07: PASS
AC-PIPE-09: PASS
AC-PIPE-10: PASS
AC-VAL-01:  PASS
AC-VAL-02:  PASS
AC-VAL-03:  PASS
AC-VAL-04:  STRUCTURAL PASS; NUMERIC: DEFERRED (FUT-01 FO-2)
=== summary: 12 pass-or-structural-pass / 0 fail ===
```

Exit code 0 is required for closure. The driver invokes each per-check probe
(`ac-pipe-01.sh` ... `ac-pipe-10.sh`, `ac-val-01.sh` ... `ac-val-04.sh`,
`ac-pipe-05.py`) from inside the phase directory; the three already-persisted
Phase-27 probes (`ac-pipe-04.sh`, `ac-pipe-08.sh`, `ac-pipe-09.sh`) are re-run in
place from `.planning/phases/27-sampling-precision-and-global-scale-contracts/`.

Individual probes are also runnable directly, e.g.:

```bash
# Dataset set-difference probe (count derived from parsed sets, never hard-coded)
python3 .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-05.py
# -> AC-PIPE-05 PASS 184/184  (base=2749 gold=2565 not_in_gold=184 promoted=0)

# A spec-consistency probe
bash .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-01.sh

# The two-axis PSC probe
bash .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-val-04.sh
# structural PASS, numeric DEFERRED
```

### Verifying no probe touches `pinn/`

A core acceptance rule (VER-09 / SCOPE-10): probes test the specs and the dataset,
they never touch `pinn/` production code. To confirm:

```bash
grep -lE 'pinn/' .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-*.sh \
                 .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-*.py
# expected: empty (exit 1)
```

A non-empty result is a STOP-protocol violation; halt and surface.

## Issue-ledger protocol

The v1.5 issue ledger lives at `24-ISSUE-LEDGER.md` (created in Phase 25). It tracks
every in-scope finding through a fixed status machine:

```
PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED
                          \-> DEFERRED  (with written blocker)
```

Closure rule: v1.5 does not close while any in-scope row is at `PENDING`,
`IN_PROGRESS`, or `FIX_APPLIED`. Every row must be at `VERIFIED` or explicitly
`DEFERRED` with a written blocker (VER-10). Required acceptance checks that cannot
run because their contract is user-deferred must be recorded as `DEFERRED`, not
`PASS` - this is the difference between **deferred** and **passed**, and it
matters for the ledger audit.

### DEFERRED vs PASS semantics

| State | Meaning | Counted in closure? | Routes to |
|---|---|---|---|
| `VERIFIED` | Contract landed, AC executed, evidence recorded | Yes (toward 18/18) | n/a |
| `DEFERRED` | Contract landed (structural) but numeric / post-promotion axis awaits FUT-01 | Yes (toward 1/1) | `29-CODE-DIVERGENCE.md` FO-1/FO-2 |
| `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` | Work incomplete | **No** - blocks closure | The owning spec-edit phase (26/27/28) per VER-09 route-back clause |

AC-VAL-04 / PSC is the canonical example of `DEFERRED` semantics: the PSC clause is
landed in `ctl_instruction.md` (structural), the dedup-prefer-gold + `1/N_t`
composition is ratified (GAP-28-03), but the construction constants (grid,
`H / ln K` normalization, SCR anchor, first-run sanity) are provisional pending the
post-promotion pool (FUT-01 FO-2). The AC-VAL-04 structural axis passes now; the
numeric axis is DEFERRED.

### Ledger terminal-state audit (Phase 29)

`29-ACCEPTANCE-EVIDENCE-2026-06-17.md` contains the 19-row ledger terminal-state
audit. As of 2026-06-17:

```
COUNTS 18 1
NONTERMINAL []
```

18 rows at `VERIFIED`; 1 row at `DEFERRED` (PSC); zero non-terminal in-scope rows.
The audit is a Python enumeration of the ledger Status Table, not a free-form claim.

## Gold-completeness state (v1.5 milestone fact)

A locked decision (GAP-29-01 RESOLVED 2026-06-16, Option A) reconciles the standard-gold
completeness fact that drives the PSC deferred state:

| Quantity | Value | Notes |
|---|---|---|
| Standard IDs attempted (full 184 rerun) | 184 | The 184 IDs named by M13 / G4 |
| Validated / promoted / staged | 117 | Reachable; 0 promoted into the canonical gold output folder under D-01 |
| Permanent `gold_counterpart = absent` | 67 | Physically irreducible gold holes; treated as permanent, not a future rerun backlog |
| Promotion (gold -> canonical gold output) | Deferred to FUT-01 | Per GAP-29-01 Option A; D-01 forbids Phase-29 dataset mutation |
| 184 -> 67 cascade | Deferred to FUT-01 (FO-1) | `29-CODE-DIVERGENCE.md` FO-1; updates `standard_quasi_random_ids_not_in_gold.md`, AC-PIPE-05 assertion, runner `EXPECTED_ID_COUNT`, `ctl_instruction.md` Step-5 gold note, and the Set-2b / issue-02 counts |

The 184 -> 67 cascade is **not** executed at v1.5 closure. The `184/184` value
recorded by `ac-pipe-05.py` reflects the *pre-promotion* set-difference state
(`base - gold = 184`); the gold output folder stays at 2,565 records. The 117
validated reruns are preserved on disk (staging area + manifest entries) but not
promoted; the rerun scripts (`simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py`
and its test) remain untracked and are flagged as a "do NOW" interim FO-1 durability
item to prevent silent loss before the FUT-01 gate.

Phase 29 reconciles only the **planning/governance/ledger** layer to the
117/67/0-promoted fact. The stale records (the 184-IDs file, the AC-PIPE-05
assertion, the runner count, the framework spec gold note, the issue-02 counts)
are enumerated in `29-CODE-DIVERGENCE.md` (stale-record inventory) and left
intentionally unchanged under D-01. The staleness is documented, never silent;
FO-1 is the single corrective transaction at the FUT-01 dataset-finalization gate.

## Source-Issue (SI) reconciliation

`29-HANDOFF.md` §4 records the three SI entries named by VER-12, each either
**retired-with-backref** or **preserved-with-written-reason**. None is assumed
resolved or assumed irrelevant.

| Entry | Disposition | Back-reference / written reason |
|---|---|---|
| `SI-DQA-002` | Retired with VAL-01 / SCS-row back-reference | SCS gate inconsistency now resolved and canonical in `ctl_instruction.md` (Step-1A clause 5, `SCS > -5` / `eps_H > 1e-5`) via v1.5 VAL-01 |
| `SI-DQA-003` | Retired with VAL-01 back-reference | Corrected SCS gate (`eps_H` raw-drift vs `SCS = log10(eps_H)`; gate `eps_H > 1e-5` ≡ `SCS > -5`; Reject tightened `SCS > -4` -> `SCS > -5`) is the gate v1.5 VAL-01 canonicalized into the live spec |
| `SI-PINN-002` | **Preserved with written reason** | Architecture-side `\authcomment{}` editorial notes (omega_0 detail, hidden-layer detail, "batch construction not consistent with the CTL instruction plan"); out of issue-02 data-pipeline scope; carried forward to FUT-05 / training implementation. The 3rd comment is **not** marked retired-by-M12 - whether the landed M12 mini-batch contract discharges that author comment is source-silent (D-08), so the grounded disposition is preserve-with-reason. D-08 STOP-checkpoint user-approval recorded 2026-06-17 |

The adjacent `pinn_architecture.md` batch-construction-inconsistency SI entry (the next
SI block after `SI-PINN-002`) is **not** in the VER-12 review list and is deliberately
not folded in; it remains a FUT-05 item.

## Milestone-Closure Gate (G1-G8)

The eight conditions under which v1.5 closes. The gsd-verifier records results in
`29-VERIFICATION.md`. A failing check blocks closure and routes the specific
finding back to its originating phase (VER-09 routing clause).

| # | Gate condition | Pass = | Route-back target on fail |
|---|---|---|---|
| G1 (VER-07/09) | All 13 AC checks executed with fresh Phase-29 results | 12 PASS + 1 split (AC-VAL-04 structural PASS / numeric DEFERRED); 0 FAIL | The originating spec-edit phase (26/27/28) for any FAIL |
| G2 (VER-09) | AC-PIPE-05 dataset probe | PASS @ 184/184 (0 promoted; consistent under D-01) | Phase 26 (M13) if set-difference breaks |
| G3 (D-07/VER-10) | Ledger row-status audit | 19 rows; 18 VERIFIED + 1 DEFERRED; **0** PENDING/IN_PROGRESS/FIX_APPLIED | The owning phase of any non-terminal row |
| G4 (VER-12) | 3 SI dispositions recorded | SI-DQA-002, SI-DQA-003, SI-PINN-002 each retired-with-backref OR preserved-with-reason; 0 assumed | n/a (recorded in `29-HANDOFF.md` §4) |
| G5 (VER-11) | Handoff completeness | `29-HANDOFF.md` has fixed/unchanged/deferred + SI table; `29-CODE-DIVERGENCE.md` FO-1/FO-2 present | n/a |
| G6 (VER-08) | Traceability | 36/36 reqs -> exactly one phase; Phase 29 = VER-07/08/09/11/12 | Roadmap revision if mismatch |
| G7 (D-05/D-01) | Gold reconciliation recorded | `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` references the 117/67/0-promoted table; stale-artifact inventory present; PSC numeric stays DEFERRED | n/a |
| G8 (governance) | No `pinn/` touch, no spec edit, no dataset mutation, no read-only/frozen-file edit | `git diff` of touched paths shows only `.planning/` (+ optional probe scripts) | STOP if violated |

v1.5 closes only when **G1-G8 all pass**. v1.5 does not ship while any required check
fails.

## Writing a new acceptance probe (template)

New AC probes follow the disposable-probe pattern. The minimum shape:

```bash
#!/usr/bin/env bash
# ac-pipe-NN.sh - <one-line purpose>; resolves <Finding / G-NN>
# Reads only ctl_instruction.md / pinn_architecture.md / simulation_data/.
# Does NOT touch pinn/ production code (SCOPE-10 / VER-09).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# 1. Assert the clause is landed in the framework spec.
grep -qE '<required text fragment>' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md

# 2. (Optional) Dataset-side assertion.
# python3 -c '...'

echo "AC-PIPE-NN: PASS"
```

```python
# ac-pipe-NN.py - <one-line purpose>; resolves <Finding>
# No hard-coded counts. Counts must be derived from parsed sets / files.
import sys, pathlib

base = pathlib.Path("simulation_data/base")
gold = pathlib.Path("simulation_data/gold")
# ... set-difference logic ...
# AC-PIPE-NN PASS <derived_count>/<derived_count>
```

Conventions:

- Grep-based probes assert that the contract clause is landed; they do not execute
  the contract (the contract is a spec clause, not runtime code).
- Dataset probes derive counts from parsed sets/files; never hard-code expected
  counts (the FO-1 cascade will change them).
- Probes must exit 0 on pass, non-zero on fail. `run-ac-suite.sh` wraps each probe
  and increments `PASS` / `FAIL` counters.
- Probes must not reference `pinn/`. Verify with
  `grep -lE 'pinn/' ac-*.sh ac-*.py` (must return empty).

## CI integration

The acceptance suite runs as part of the v1.5 closure verification, not as a
standalone CI job. The verification chain is:

1. `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` is populated by the Phase-29
   `run-ac-suite.sh` execution and the ledger audit.
2. `29-VERIFICATION.md` records the gsd-verifier's pass/fail per gate (G1-G8) and
   per required artifact.
3. `29-HANDOFF.md` is the v1.5 closure record and the FUT-01 input; it cross-references
   the evidence file and the `29-CODE-DIVERGENCE.md` forward obligations.
4. `REQUIREMENTS.md` and `ROADMAP.md` checkbox flips for VER-07/08/09/11/12 are the
   post-verification reconciliation step (governed by agent-owned paths; not
   auto-applied by probe execution).

## Cross-references

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` -
  authoritative metric definitions and admission gate (Step 1A clause 5; data-side
  quality-metric contracts)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` -
  architecture and training-loss `eps_H` (distinct from validation `eps_H`)
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` - frozen
  data-generation instruction (SCOPE-08); read-only as historical record
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` -
  read-only research report (SCOPE-09); the SI-DQA-002 / SI-DQA-003 home file
- `.planning/REQUIREMENTS.md` - VER-* / AC-* / VAL-* requirements (Coverage block
  at lines 147-157 confirms 36/36 traceability)
- `.planning/ROADMAP.md` - phase distribution (4+7+0+6+6+4+4+5 = 36); Phase 29
  covers VER-07/08/09/11/12
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` -
  v1.5 issue ledger (19 rows: 18 VERIFIED + 1 DEFERRED at v1.5 closure)
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-SPEC.md` -
  Phase 29 specification
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-UAT.md` -
  Phase 29 UAT summary
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-VERIFICATION.md` -
  Phase 29 verification report (gate G1-G8 results)
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-HANDOFF.md` -
  v1.5 milestone handoff (Fixed / Intentionally Unchanged / Deferred / SI table /
  G1-G8)
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-CODE-DIVERGENCE.md` -
  FUT-01 forward obligations FO-1 (gold promotion + 184 -> 67 cascade) and FO-2
  (PSC numeric calibration + AC-VAL-04 numeric run)
- `.planning/milestones/v1.5-GAPS.md` - milestone-wide gap index
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/` - per-metric
  evidence packets (`sasd-sampling-density.md`, `ipr-physics-residual.md`,
  `psc-coverage-entropy.md`, `scs-thresholds.md`)

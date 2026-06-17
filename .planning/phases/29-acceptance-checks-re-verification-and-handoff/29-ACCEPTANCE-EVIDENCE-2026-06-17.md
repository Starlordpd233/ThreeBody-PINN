# Phase 29 UAT — Acceptance-Suite Re-run, Ledger Audit, and Traceability

**Phase:** 29 — Acceptance Checks, Re-verification, and Handoff (terminal v1.5 phase)
**Plan:** 29-01
**Executed:** 2026-06-17
**Requirements:** VER-07 (ACs numerically defined), VER-08 (traceability), VER-09 (ACs executed
via disposable probes with recorded pass/fail; probes never touch production model code).

This UAT records the **fresh Phase-29 re-execution** of the full applicable acceptance suite as
disposable probes, the 19-row issue-ledger terminal-state audit, and the 36/36 roadmap
traceability confirmation. Per D-02 the suite is re-run (not re-cited): the 3 already-persisted
Phase-27 probes (`ac-pipe-04/08/09.sh`) are re-run in place; the other 10 are lightweight
grep/dataset probes authored under this phase dir, each transcribing the landed clause its
finding asserts. No probe touches `pinn/` production code (VER-09 / SCOPE-10); no framework
spec or dataset file was mutated.

---

## 1. Acceptance Checks Are Defined (VER-07)

Every v1.5 contract carries a numerically-defined acceptance check naming its pass criterion,
the data it runs on, and the command/function that executes it. The driver
`run-ac-suite.sh` re-runs all probes and emits one result line per check; it exits 0.

**Re-run result line (`bash run-ac-suite.sh`, 2026-06-17):** 12 PASS + AC-VAL-04 split
(STRUCTURAL PASS / NUMERIC DEFERRED), 0 FAIL, exit 0.

## 2. Acceptance Checks Execute — Fresh Phase-29 Results (VER-09)

13 ledger-mapped checks. `AC-PIPE-08` (stage-query) has **no standalone ledger row** — it is
re-run inside the M12/G5 (AC-PIPE-04) family and noted under G5 — so the suite reports 13
result lines while exercising all 14 probe IDs below. Probe paths are relative to the repo root;
the three persisted probes live under `…/27-sampling-precision-and-global-scale-contracts/`.

| AC-ID | Asserts (landed clause) | Command / Function | Input data | Pass criterion | Result (2026-06-17) | Evidence (probe) |
|-------|-------------------------|--------------------|------------|----------------|---------------------|------------------|
| AC-PIPE-01 | Step-1A trajectory-admission gate (B-06/G1) | `bash …/29-…/ac-pipe-01.sh` | `ctl_instruction.md` Step 1A | gate heading + structural/completeness/conservation conditions; `>=200` floor only in rejection | **PASS** | `ac-pipe-01.sh` |
| AC-PIPE-02 | ID-resolution contract, id ≠ array index (B-11/G2) | `bash …/29-…/ac-pipe-02.sh` | `ctl_instruction.md` Step 1 item 7 | `record_key` tuple, `id_to_path` scan, dense/arithmetic-path prohibited, id 3958 cited | **PASS** | `ac-pipe-02.sh` |
| AC-PIPE-03 | Blacklist-exclusion contract (M11/G3) | `bash …/29-…/ac-pipe-03.sh` | `ctl_instruction.md` Step-1A blacklist subsection | `physical_key` exclusion, fail-closed, counts vs parsed file (65 IDs not a contract constant) | **PASS** | `ac-pipe-03.sh` |
| AC-PIPE-04 | `n_pts = min(n_pts_cap, n_snapshots)` (M12/G5) | `bash …/27-…/ac-pipe-04.sh` | `ctl_instruction.md` Mini-Batch Construction | 8/8 assertions incl. `0.5×` rejection control | **PASS** | `27-…/ac-pipe-04.sh` |
| AC-PIPE-05 | `base − gold == not_in_gold.md` (M13/G4) | `python3 …/29-…/ac-pipe-05.py` | `simulation_data/` base+gold ID sets; `not_in_gold.md` | set-difference == documented list, exact intersection, 0 promoted | **PASS @184/184** | `ac-pipe-05.py` |
| AC-PIPE-06 | Footer / param-provenance contract (D7) | `bash …/29-…/ac-pipe-06.sh` | `ctl_instruction.md` Step 1 item 3 + §2.6 | `param_provenance` {direct,inferred,absent,measured}; footers not completeness signals | **PASS** | `ac-pipe-06.sh` |
| AC-PIPE-07 | Precision contract (footer / mass-drift) | `bash …/29-…/ac-pipe-07.sh` | `ctl_instruction.md` §2.1 | mass-invariance `<1e-15`; float64 precision contract; Decimal not the routine path | **PASS** | `ac-pipe-07.sh` |
| AC-PIPE-08 | Stage-query interface (`sample_replay`/`sample_lookahead`) | `bash …/27-…/ac-pipe-08.sh` | `ctl_instruction.md` §2.6 | signatures + `param_provenance` + doc-03 ref | **PASS** (no standalone ledger row; **noted under G5**) | `27-…/ac-pipe-08.sh` |
| AC-PIPE-09 | `compute_globals` raw-mass D ≈ 4.6416 | `bash …/27-…/ac-pipe-09.sh` | `ctl_instruction.md` §2.5 | 8 checks incl. 6.694 rejection control | **PASS** | `27-…/ac-pipe-09.sh` |
| AC-PIPE-10 | HDF5-canonical training-data format (D-03) | `bash …/29-…/ac-pipe-10.sh` | `ctl_instruction.md` Step 1 item 6 | HDF5 single-source-of-truth, user-locked 2026-06-13, round-trip; JSON/text barred | **PASS** | `ac-pipe-10.sh` |
| AC-VAL-01 | SCS gate `SCS>-5` / `eps_H>1e-5` (SCS) | `bash …/29-…/ac-val-01.sh` | `ctl_instruction.md` Step-1A clause 5 | `SCS=log10(eps_H)`, reject `>-5`, band labels; ratio thresholds rejected by name | **PASS** | `ac-val-01.sh` |
| AC-VAL-02 | SASD both-endpoint contract (SASD) | `bash …/29-…/ac-val-02.sh` | `ctl_instruction.md` Data-side quality-metric contracts | both-endpoint convention (GAP-28-01); flag-not-reject; perpendicular + 9-component variants rejected | **PASS** | `ac-val-02.sh` |
| AC-VAL-03 | IPR raw-`G=1` units + dual-epsilon (IPR) | `bash …/29-…/ac-val-03.sh` | `ctl_instruction.md` IPR clause; `pinn_architecture.md` §3.4 | raw `G=1` (GAP-28-02); CubicHermite (Pchip prohibited); `eps_inv=1e-10` vs `epsilon_train=1e-5` | **PASS** | `ac-val-03.sh` |
| AC-VAL-04 | PSC clause present/well-formed/cites packet (PSC) | `bash …/29-…/ac-val-04.sh` | `ctl_instruction.md` PSC clause (Data-side quality-metric contracts) | clause present; Shannon-entropy report-only diagnostic + SCR; dedup-prefer-gold + `1/N_t`; cites `psc-coverage-entropy.md` | **STRUCTURAL PASS; NUMERIC: DEFERRED (FUT-01 FO-2)** | `ac-val-04.sh` |

**AC-PIPE-05 note (D-03).** PASS at **184/184** is internally consistent *because* 0 reruns are
promoted under D-01 (gold stays 2,565; `base − gold = 184`). The count is **derived** from the
parsed on-disk sets and the parsed `not_in_gold.md` list — no expected count is hard-coded. It
flips to **67/67** only when the deferred FO-1 promotion lands (184→67 cascade,
`29-CODE-DIVERGENCE.md`).

**AC-VAL-04 note (D-04 / D-06).** Two-axis split. The **STRUCTURAL** axis executes and PASSES in
Phase 29: the PSC clause is landed and well-formed, names the Shannon-entropy report-only
coverage diagnostic + SCR, states the ratified **dedup-prefer-gold + `1/N_t`** composition
(GAP-28-03), and cites `psc-coverage-entropy.md`. The **NUMERIC** axis is **DEFERRED** to the
FUT-01 dataset-finalization gate (FO-2): the grid, `H/ln K` normalization, SCR anchor, and
first-run sanity are provisional pending the post-promotion pool. The PSC ledger row stays
`DEFERRED` (numeric authority pending) while the structural check passes — `ac-val-04.sh`
computes no PSC value.

## 3. Issue-Ledger Terminal-State Audit (D-07 / VER-10)

**Method (Pitfall-1 guard).** The audit enumerates the **Status field of each of the 19 rows**
in the `24-ISSUE-LEDGER.md` Status Table — NOT a token count over the per-row status-transition
logs (those narrate `PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED` history and yield ~71/35/27 false
hits even for VERIFIED rows).

Per-row Status enumeration (19 rows): B-06, B-11, M11, M12, M13, D7, G1, G2, G3, G4, G5, SCS,
SASD, IPR, **PSC**, D-03, D=6.694, footer, mass-drift.

- **18 VERIFIED** + **1 DEFERRED** (PSC) = 19 rows.
- **0 PENDING / 0 IN_PROGRESS / 0 FIX_APPLIED** in-scope rows (Lifecycle phase-exit gate met:
  only `VERIFIED`/`DEFERRED` permitted).
- Automated check (`run-ac-suite` companion): the row-status enumeration asserts `NONTERMINAL []`
  and `COUNTS 18 1`.

**The one DEFERRED row — PSC (Phase Space Coverage Entropy, VAL-04).** Blocker reframed per D-06
(`24-ISSUE-LEDGER.md` PSC row, Last-Updated 2026-06-17): the superseded *"wait for gold
completion"* blocker is replaced by — the PSC clause **LANDED** in `ctl_instruction.md` Data-side
quality-metric contracts; the dedup-prefer-gold + `1/N_t` composition is **ratified** (GAP-28-03
reopened+RESOLVED); AC-VAL-04 **NUMERIC** calibration + numeric run await the post-promotion pool
at the **FUT-01 dataset-finalization gate (FO-2)**. M13 and G4 rows (and their OI-7b-partial
notes) remain byte-identical — the LOCKED `accept-third-position`/Option-B verdict is untouched
(D-01a).

## 4. Gold-Completeness Reconciliation — Reference, Not Duplicate (D-05)

The gold-completeness reconciliation table (Standard quasi-random ICs; gold counterparts present;
184 attempted / 117 validated-staged / 67 permanent `gold_counterpart=absent` / **0 promoted**;
post-promotion projections) is **canonical in `29-CODE-DIVERGENCE.md` FO-1** and is **referenced
here, not reproduced** (per the GAP-29-01 resolution note). See
`.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-CODE-DIVERGENCE.md` (FO-1
table + stale-record inventory; FO-2 PSC numeric defer). The AC-PIPE-05 184/184 result above is
the executed evidence for the "0 promoted" line of that table.

## 5. Roadmap Traceability Confirmation (VER-08)

Confirmed against `.planning/REQUIREMENTS.md` Traceability table + Coverage block:

- **36/36** v1.5 requirements map to **exactly one** phase, beginning at Phase 23 (no orphans, no
  duplicates).
- Phase distribution: Phase 23 = 4 (PKG-01..04); Phase 24 = 7 (DATA-01..07); Phase 24.5 = 0;
  Phase 25 = 6 (EVID-06..10, VER-10); Phase 26 = 6 (PIPE-01/02/03/05/06/10); Phase 27 = 4
  (PIPE-04/07/08/09); Phase 28 = 4 (VAL-01..04); **Phase 29 = 5 (VER-07, VER-08, VER-09, VER-11,
  VER-12)**.
- This UAT discharges VER-07 (ACs numerically defined), VER-09 (ACs executed with recorded
  pass/fail), and VER-08 (traceability confirmed); VER-11/VER-12 are discharged by Plan 02
  (`29-HANDOFF.md`).

## Summary

| Gate | Result |
|------|--------|
| 13-check AC suite (`run-ac-suite.sh`) | 12 PASS + AC-VAL-04 split (STRUCTURAL PASS / NUMERIC DEFERRED); exit 0 |
| AC-PIPE-05 dataset probe | PASS @184/184 (0 promoted; count derived, not hard-coded) |
| 19-row ledger audit | 18 VERIFIED + 1 DEFERRED (PSC) + 0 non-terminal |
| Gold reconciliation | referenced from `29-CODE-DIVERGENCE.md` FO-1 (not duplicated) |
| Traceability | 36/36 → one phase; Phase 29 = VER-07/08/09/11/12 |
| Governance | no `pinn/` touch, no spec edit, no dataset mutation |

## Gaps

None surfaced during Plan 01. No STOP-protocol trip: AC-PIPE-05 returned 184/184 as expected
under D-01/D-03; the landed PSC clause was located for AC-VAL-04; the PSC reframe touched only the
PSC ledger row (M13/G4 byte-identical, D-01a); no PSC composition content was invented (only the
ratified dedup-prefer-gold + `1/N_t` rule transcribed). GAP-29-01 remains RESOLVED-WITH-INSTRUCTION
(Option A); the promotion + 184→67 cascade is carried forward to FUT-01 FO-1.

---

*Phase: 29-acceptance-checks-re-verification-and-handoff · Plan 01 · executed 2026-06-17*

---
phase: 26-dataloader-ingestion-and-selection-contracts
plan: 05
subsystem: framework-specs / data-pipeline contracts
tags: [PIPE-10, D-03, training-data-format, HDF5, user-gate, D-11, ctl_instruction, adjudication]
requires: ["26-01 (Step-1 item-7 record_key insertion shifted item-6 anchor to 406-410)"]
provides: ["PIPE-10 user-locked training-data format contract (ctl_instruction.md Step 1 item 6)", "AC-PIPE-10 definition + passing spec-consistency probe", "D-03 accept-resolution verdict (HDF5 canonical)", "D-03 ledger row VERIFIED"]
affects: ["FUT-01 processed-data store + DataLoader build (implements the HDF5 schema + the bitwise float64 round-trip test)", "Phase 29 VER-09 acceptance suite"]
tech_stack:
  added: []
  patterns: ["mandatory-user-gate (D-11)", "packet-presents-candidate-never-selects", "user-decision-provenance-recorded-in-spec-and-packet (T-26-20)", "one-atomic-commit spec+packet+ledger (D-11/D-08)", "spec-consistency probe (data round-trip deferred to FUT-01)"]
key_files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/d-03-training-data-format.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
decisions:
  - "D-03 verdict accept-resolution: the user selected hdf5-canonical (the resolution-doc §3.6 Q-A6 candidate) at the PIPE-10 mandatory gate (D-11) on 2026-06-13; HDF5 is the locked canonical processed-training-data store"
  - "The format was USER-LOCKED, not auto-selected under any execution mode (D-11); user-decision provenance recorded in both ctl_instruction.md Step 1 item 6 (in-spec attribution) and the D-03 packet Verdict (T-26-20 mitigation)"
  - "ctl_instruction.md Step 1 item 6 edited ALONE; no pinn_architecture.md edit (D-03 names ctl alone, T-26-21)"
  - "Round-trip acceptance clause is the spec-side contract; the data round-trip implementation (parse raw -> write -> read -> bitwise np.array_equal) is FUT-01, not Phase 26"
  - "AC-PIPE-10 is a spec-consistency grep probe (Step-1-item-6 names HDF5 + a round-trip clause present); no new AC-ID minted (reserved AC-PIPE-10 = AC-{PIPE-10})"
metrics:
  duration: "~25 min"
  completed: 2026-06-13
  tasks: 3
  files: 4
---

# Phase 26 Plan 05: Training-Data Format Contract (PIPE-10 / D-03) Summary

PIPE-10 is resolved as a requirement-mandated USER gate. The D-03 packet (Task 1) presented HDF5 vs `.npy`/`.npz` vs txt/json with verified evidence (DATA-06 ragged-array distributions + 15,028-file dataset scale) and the resolution-doc §3.6 Q-A6 position as a CANDIDATE — never a pre-locked choice. At the blocking `checkpoint:decision` gate (Task 2), **the user selected `hdf5-canonical` on 2026-06-13.** Task 3 transcribed that user-locked choice into `ctl_instruction.md` Step 1 item 6, set the D-03 packet Verdict to `accept-resolution` with explicit user-decision provenance, advanced the ledger D-03 row to VERIFIED, ran AC-PIPE-10 (PASS) and the D-08 chain-regression re-checks (AC-PIPE-01/02/06 PASS, no regression), and committed all of it in one atomic `26-05` commit.

## The user decision (not auto-selected)

The choice was **user-locked 2026-06-13 via the PIPE-10 mandatory gate (D-11)**; the user selected **HDF5 canonical** (the §3.6 Q-A6 candidate). No execution mode selected the format. D-11 forbids any mode (including `--auto`/yolo) from choosing, and the blocking gate was honored: the packet presented the candidate as a recommendation, halted, and the user supplied the explicit selection. No overriding operational constraint (HDF5-dependency prohibition) was supplied, so the candidate stands unmodified. User-decision provenance is recorded in two places (T-26-20 mitigation): the in-spec attribution ("user-locked 2026-06-13") in `ctl_instruction.md` Step 1 item 6, and the D-03 packet Verdict / Before-After sections.

## What was done

1. **D-03 evidence packet finalized** (`evidence/d-03-training-data-format.md`, authored uncommitted in Task 1, finalized here): Verdict set to `accept-resolution` with the user-decision provenance line ("User-locked 2026-06-13 via the PIPE-10 mandatory gate (D-11); user selected HDF5 canonical (the §3.6 Q-A6 candidate); not auto-selected"). Locked Convention, Which-Source-Correct, Before/After, and Named-Acceptance-Check sections updated to reflect the lock. AC-PIPE-10 command + output captured re-derivably (D-15). Status transition log advanced PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED with the shared `26-05` SHA. The README ID→filename map row (`D-03` → packet) was added in Task 1.

2. **`ctl_instruction.md` Step 1 item 6 replacement** (current lines 406-426; the plan's 374-378 anchor was stale because Plan 26-01 inserted Step 1 item 7, confirmed by grep before edit, A1): replaced "an efficient format like HDF5 or NumPy (.npy)" with the user-locked HDF5-canonical contract transcribed from `02-resolution-doc.md:362-377` — HDF5 single source of truth (groups `/{variant}/{fidelity}/{id}`, float64 datasets for `times`/`positions`/`velocities`/masses + §2.6 derived arrays, per-group attributes carrying the §2.6 metadata record including `param_provenance`, raw-file SHA-256 hashes, a top-level `schema_version`, and the build's transform metadata `D`/`T`/`V`/`E_scale` + scale provenance so raw values are exactly re-derivable, chunked+compressed, partial reads by group); `.npy`/`.npz` as an ACCEPTABLE derived cache/export preserving the identical schema; JSON/text inspection-and-debugging-only and NEVER a training input path; PLUS a bitwise-float64 round-trip acceptance clause (incl. times). No `pinn_architecture.md` edit (D-03 names ctl alone, T-26-21).

3. **AC-PIPE-10 spec-consistency probe — PASS:** `grep` confirms Step 1 item 6 (a) names HDF5 as the locked canonical store and (b) carries a round-trip acceptance clause. The data round-trip itself is FUT-01. Command + output captured in the packet (D-15).

4. **D-08 chain-regression re-checks — all PASS, no regression** (the item-6 expansion shifted downstream line numbers but disturbed no neighboring Step-1 contract content):
   - **AC-PIPE-01** (Step-1A admission gate): `## Step 1A` + `final_timestep >= 9.5` + `SCS > -5` intact (452/471/477); the rejected `>= 200` floor remains rejected (494-495), not reintroduced.
   - **AC-PIPE-02** (`id_to_path` / `record_key`): scan-built contract, the `^brutus_(hierarchical|standard)_(\d{4})\.txt$` regex, and the "never equal to an array index" invariant intact (429-441).
   - **AC-PIPE-06** (footer-as-metadata / `param_provenance`): footer-metadata-only contract (359/392) and the D7 `param_provenance` home (814) intact; the dataset half (`data04_footers.py`, unaffected by a spec edit) was captured in the D7 packet and not re-run.

5. **Ledger D-03 advanced to VERIFIED** (`24-ISSUE-LEDGER.md`): summary-table row and detail-block transition log both updated; verdict `accept-resolution`, Evidence Packet link added, spec target = `ctl_instruction.md` Step 1 item 6 alone. D-03 has NO synthesis (G) row.

## Deviations from Plan

**1. [A1 anchor correction — not a deviation, a planned re-confirmation]** The plan's "lines 374-378" item-6 anchor was stale; the live anchor is 406-410 (Plan 26-01 inserted Step 1 item 7 between Task-1 authoring and this edit). The plan's Task-3 `read_first` explicitly instructed re-confirming the anchor at edit time (A1); grep `"HDF5 or NumPy"` confirmed 406-407 before the Edit. No content impact.

No other deviations. No Rule 1-4 auto-fixes were needed; the format choice was a grounded user decision transcribed verbatim, nothing was invented (v1.5 STOP protocol — no gap surfaced).

## D-04 / perimeter compliance

`git diff --name-only` for the `26-05` commit shows only `ctl_instruction.md` + `.planning/` paths: specifically NO `pinn_architecture.md` (D-03 names ctl alone, T-26-21), no frozen specs (`sampling_method.md`, `data_quality_assessment.md`), no `pinn/`. One atomic commit via `scripts/agent-commit` (scope `26-05`, type `spec`, body required) carrying spec + packet + README + ledger together (D-11/D-08).

## Self-Check: PASSED

- Files exist: `ctl_instruction.md`, `d-03-training-data-format.md`, `26-05-SUMMARY.md`, `24-ISSUE-LEDGER.md` — all FOUND.
- Commits exist: `8369e275` (atomic spec+packet+ledger commit), `8ef4dfd7` (SHA backfill) — both in `git log`.
- Task-3 automated verify gate: round-trip clause OK; ctl edited OK; no forbidden paths (no `pinn_architecture.md` / frozen specs / `pinn/`); D-03 VERIFIED in ledger OK.
- AC-PIPE-10 PASS; AC-PIPE-01/02/06 regression re-checks PASS. Working tree clean.

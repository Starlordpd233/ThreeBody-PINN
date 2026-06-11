# 24-GAPS.md — Phase 24 STOP-Protocol Gap Register

**Phase:** 24 — Empirical Dataset Verification and Correction Addendum
**Plan:** 24-02 (Wave 2)
**Created:** 2026-06-11
**STOP-protocol authority:** `CLAUDE.md` "v1.5 applicability" + STOP-protocol field list (D-22, D-16, D-17).

## GAP-24-01 — DATA-05 hierarchical mass-drift baseline

- **Decision point:** what to record as the DATA-05 verdict when 70/4857 `brutus_hierarchical` files show m_Brutus(t=0) ≠ m_IC at float64, but `brutus_hierarchical_gold_standard` matches the IC perfectly (0/4857)? Pick a baseline or surface as a semantic STOP gap.
- **Where in artifact:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` (DATA-05 verdict row, to be added by plan 24-02 Task 2) + `24-VERIFIED-FACTS.md` "Anomalies (D-12)" section.
- **Task context:** plan 24-02 Task 2 (DATA-05 mass-drift probe) running `probes/data05_mass_drift.py` under `.venv/bin/python` over the full population (15,028 trajectory-IC pairs).
- **Classification:** **semantic** — the empirical fact (70 base-hier mismatches) is observed re-derivably; the question is what to record as the "ground truth" (IC vs Brutus) and how to interpret the drift (round-trip, perturbation, or genuine generation/runner error).
- **Source silence:**
  - `simulation_data/Scripts/ic_generation/ic_generation_utils.py:417-420` — perturbation is applied to POSITION and VELOCITY vectors only; masses are NOT perturbed. Grounded.
  - `.claude/rules/dataset-reference.md` "Mass and COM Properties" — says masses are not perturbed, COM is enforced then perturbed (positions, not masses). Grounded.
  - `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` — base runner passes the IC file directly to `brutus`. No mass transformation. The C++ `brutus` reads col 0 of body lines 1-3 as the mass and uses it unchanged.
  - `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` — gold runner: same direct pass. Yet the gold output for id 5 matches the IC (0.9056...) and the base output for id 5 does not (1.2569...). The provenance gap is: the base and gold runners read the same IC file but produce different t=0 masses for the same 70 IDs.
  - `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py` and `simulation_data/Documentation/` — no record of a re-derivation event, a backfill, or a runner hot-fix that would explain the divergence.
- **Mathematical / engineering grounding:** For a Newtonian three-body integrator, the mass is a parameter of the dynamics; it does not change during integration. m_Brutus(t=0) should equal m_IC exactly under any well-formed pipeline. The 70 base-hier mismatches show a difference of order 0.1-1.0 in mass units (e.g., id 5: 0.9056... vs 1.2569..., abs_diff ≈ 0.35). This is NOT a float64 round-trip artifact (rtol=1e-15 would catch only ~1e-15 relative error); it is NOT a perturbation artifact (perturbation doesn't touch masses; gold proves this); and it is NOT a parser error (the values parse cleanly to float64). The most plausible explanations are: (a) the IC files were re-generated or backfilled AFTER the base Brutus run; (b) the base runner used a stale or different IC snapshot for these 70 IDs; (c) there is a bug in some intermediate step that rewrote the first line of those 70 IC files. None of these are grounded in the source materials. The gold variant matching perfectly rules out a generation-side error in the IC files themselves; it implicates either the base runner or a post-generation backfill that touched only the base variant.
- **Agent was tempted to:** record verdict as "decimal.Decimal parsing required" (routing the 70 mismatches to a precision issue) — this would be the wrong framing because the absolute differences are 0.1-1.0, not 1e-15; precision does not explain them.
- **What the user must decide:**
  - **A.** Record "70 base-hier files show genuine mass drift; gold variant is canonical; base variant should be regenerated or backfilled from gold for these 70 IDs." Routes the verdict to a Phase 25/27 follow-up; PIPE-07 must read masses from gold only.
  - **B.** Record "70 base-hier files have IC-vs-Brutus mass drift of unknown provenance; user is investigating; DATA-05 verdict is unverified for the base variant and confirmed for gold+standard." Both downstream consumers gate on the gold variant; PIPE-07 proceeds.
  - **C.** Defer the gap entirely (D-22 / DEFERRED) and leave the row as `unverified — deferred pending GAP-24-01`.
- **Confidence of impact:** HIGH — DATA-05's verdict feeds PIPE-07 (Phase 27 precision contract); a wrong baseline choice would silently corrupt every downstream precision assertion.
- **Status:** **RESOLVED-WITH-INSTRUCTION**
- **Resolution note:** User instruction recorded 2026-06-11: adopt a narrowed form of option A. The current IC files are canonical; the 70 affected base-hierarchical Brutus outputs are invalid/stale trajectory artifacts, not valid physical mass drift and not a `decimal.Decimal` precision problem. Do **not** skip these 70 systems permanently and do **not** backfill from gold as a silent substitute for the base variant. Rerun exactly the affected base-hierarchical outputs from the current canonical IC files, using the base-hierarchical Brutus contract, with originals preserved as forensic evidence until replacement is validated. Phase 24 may proceed with DATA-05 recorded as resolved-with-remediation-required; downstream training, metrics, and PIPE-07 consumption must not use the old 70 base-hier artifacts. See `24-DATA05-RERUN-REMEDIATION.md`.

### Post-resolution remediation scope (2026-06-11)

- **Affected IDs:** `0005`-`0059`, `0061`-`0075` (70 total).
- **Canonical source:** `simulation_data/Data/ic_final/ic_hierarchical/ic_hierarchical_XXXX.txt`.
- **Invalid artifacts:** `simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_XXXX.txt` for the affected IDs until rerun/replacement passes validation.
- **Decision boundary:** This resolves the semantic baseline decision. It does **not** claim the files have already been regenerated.

### Remediation executed (2026-06-11)

The rerun was executed and validated the same day: 70/70 staged replacements passed all
remediation gates (mass equality at float64, 126 snapshots to t=10, schema), the swap was
performed after user approval, and the post-swap DATA-05 probe re-run reports **0/4857**
base-hier mismatches (0/15,028 overall). Old artifacts are archived at
`simulation_data/Data/forensic/data05_gap24-01_old_outputs/` with a committed SHA-256
manifest. Derived metrics for the 70 IDs remain invalidated pending regeneration (gate 7,
deferred by user). Full evidence: `24-DATA05-RERUN-REMEDIATION.md` "Execution Evidence".

## Milestone-wide index

Mirrored at `.planning/milestones/v1.5-GAPS.md` (created 2026-06-11 with this entry).

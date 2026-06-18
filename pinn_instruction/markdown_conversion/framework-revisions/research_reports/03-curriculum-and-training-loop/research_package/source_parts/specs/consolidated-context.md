# Consolidated Context — Minimal `simulation_data` / v1.5 Excerpts (doc-03 curriculum / training-loop)

> **Status:** Consolidated context file (D-09 Document #7). Snapshot-class grounding companion.
> Holds ONLY the user-approved minimal fragments resolved at the D-09 gate (Inclusion Call (a),
> APPROVED MINIMAL set): per-variant snapshot / `dt_out` distributions; stage-assignment counts;
> the 184-gap and ~2,565 gold count; the EVID-10 `D`-rejection anchor — and nothing more (D-22:
> doc-03 is less dataset-centric than v1.5, so excerpts stay minimal).
>
> **Per-fragment source labels** are retained internally (D-10), as permitted in this
> snapshot-class grounding companion (NOT in the master or the prompt, which carry zero repo
> paths and reference this file by bare filename, D-05).
>
> **Verification boundary (D-17):** v1.6 has no in-milestone empirical-verification phase. The
> v1.5-`verified` anchors below are reproduced from the standalone `verified-facts-reference.md`
> (the single owner; F11) and are safe as fact; the stage-assignment counts (Fragment C) are
> `claimed-unverified` issue-03 design outputs and must NOT be relied on as fact — see
> `claims-register.md`. Every figure below carries its CLM-NN row in `30-CLAIMS-INVENTORY.md`; no
> unregistered figure appears here.

---

## Fragment A — Per-variant `dt_out` distributions [CLM-17, `verified`]

Grounds the stage `dt_out` figures (standard 0.17 / hierarchical base 0.08 / gold 0.01) and bounds
`τ_L` / `L_max` / collocation scaling in the curriculum contracts.

| Variant | `dt_out` |
|---------|----------|
| `brutus_standard_quasi_random` | 0.17 |
| `brutus_hierarchical` (base) | 0.08 |
| `brutus_hierarchical_gold_standard` | 0.01 |
| `brutus_standard_quasi_random_gold_standard` | 0.01 |

`dt_out` is the output sampling interval, NOT the internal adaptive step size.

> Source: `24-VERIFIED-FACTS.md` CLM-09 (v1.5 DATA-04 `confirmed`);
> `simulation_data/Documentation/README.md` § "Brutus Parameters by Variant".
> CLM-17 (`verified`). Full statement in `verified-facts-reference.md` VF-1.

## Fragment B — Per-variant median snapshot counts [CLM-16, `verified`]

Median snapshots per trajectory: standard **61** / hierarchical base **127** / gold **1003**
(issue-doc `~59 / ~125 / ~1000` superseded; v1.5 DATA-06 `corrected`). The integer-rounded MEDIAN
is the authoritative D-09 statistic; any package snapshot-count figure uses these values
(CLM-16), not the issue-doc `~`-values (CLM-13).

> Source: `24-VERIFIED-FACTS.md` CLM-10 (v1.5 DATA-06 `corrected`). CLM-16 (`verified`).
> Full statement in `verified-facts-reference.md` VF-2.

## Fragment C — Stage-assignment-relevant counts [CLM-02..CLM-07, `claimed-unverified`]

Per-stage population context for the stage-assignment finding cluster. These are issue-03 Stage
Inventory Summary figures — **`claimed-unverified` design outputs** of an *adaptive*
stage-assignment methodology (`stage_strat_revision.md` Part III); no v1.6 phase verifies them
(D-17), flagged for FUT.

| Stage | Trajectory count (claimed) | CLM ID |
|-------|----------------------------|--------|
| Stage 0 | ~1,200 | CLM-02 |
| Stage 1 | ~2,000 | CLM-03 |
| Stage 2 | ~1,657 | CLM-04 |
| Stage 3 | ~600 | CLM-05 |
| Stage 4 | ~1,600 | CLM-06 |
| Stage 6 | Unknown (explicitly) | CLM-07 |

> Source: `pinn_instruction/issues/03-curriculum-and-training-loop.md` Stage Inventory Summary
> (lines ~668–680). CLM-02..CLM-07 (`claimed-unverified`, FUT-flagged) in `30-CLAIMS-INVENTORY.md`.
> NOTE: the `~2,565` gold count that appears alongside the stage counts is v1.5-`verified`
> (Fragment D / CLM-15), NOT a stage count.

## Fragment D — Gold-gap record: 184-gap and ~2,565 gold [CLM-14, CLM-15, `verified`]

- Standard base ICs: **2,749**; standard gold subset: **2,565**; base − gold = **184**.
- The 184 standard IDs have no gold-standard counterpart (never selected for `dt_out = 0.01`
  gold re-simulation); the 2,565 gold ICs are a byte-identical subset of the base ICs.

> Source: `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (lines ~7–11)
> + `24-VERIFIED-FACTS.md` CLM-04 / CLM-05b (v1.5 DATA-03/04 `confirmed`). CLM-14 + CLM-15
> (`verified`). Full statement in `verified-facts-reference.md` VF-3 / VF-4.

## Fragment E — EVID-10 `D`-rejection anchor [CLM-01 vs CLM-19, `verified` counter-position]

The committed v1.5 verdict: the contested total-mass `D = cbrt(G · M_tot_ref · T²) = 6.694`
(issue-03, `M_tot_ref = 3.0`, `T_scale = 10`; CLM-01, `claimed-unverified`, verdict-gating) was
**rejected** in favor of the raw-mass `D = (G · T²)^(1/3) ≈ 4.6416` (CLM-19), which is the
SCOPE-12-locked PHYS-01 constant (locked Phase 19). v1.5 Phase 25 EVID-10 reaffirmed the
rejection of 6.694. This anchors the `D`-conflict framing: the open question for the resolution
doc (Phase 32) is the reconciliation of issue-03's `τ_L` derivation **under the locked
`D ≈ 4.6416`**, NOT *which* `D` value is correct. Both `6.694` and `4.6416` appear so the
seed-conflict is fully registered.

> Source: v1.5 Phase 25 EVID-10 (rejection of 6.694); `ctl_instruction.md` §2.5 (lines ~904–919,
> raw-mass `D ≈ 4.6416` locked PHYS-01); issue-03 lines 265, 305 (the 6.694 derivation).
> CLM-01 (`claimed-unverified`) vs CLM-19 (`verified` / SCOPE-12 hard constraint). Full statement
> in `verified-facts-reference.md` VF-5.

# Verified-Facts Reference — v1.5-Verified Dataset Anchors (doc-03 curriculum / training-loop)

> **Status:** STANDALONE grounding-class companion. Produced and solely owned by Phase 30
> Plan 30-03 (single owner; F11). Reused by the claims register (`claims-register.md`) and the
> SCOPE-12 hard-constraints preamble (`scope-12-hard-constraints.md`) — both reference this file
> rather than re-citing a buried fragment.
>
> **Scope:** Only the **v1.5-verified** dataset facts that the curriculum / training-loop
> contracts depend on. Every figure here is `verified` per the Phase 30 claims register
> (`30-CLAIMS-INVENTORY.md`), grounded in a committed v1.5 verdict and/or
> `simulation_data/Documentation/`. Per-fragment internal source-path labels are retained (D-10),
> as permitted in snapshot/grounding-class companions (NOT in the master or the prompt).
>
> **Verification boundary (D-17):** v1.6 has **no** in-milestone empirical-verification phase.
> The facts in THIS file are the v1.5-verified subset and are safe to rely on as fact. Figures
> NOT in this file (issue-03 stage counts, design-constant tables, the `D = 6.694` derivation)
> are `claimed-unverified` and must NOT be relied on as fact — see `claims-register.md`.

---

## VF-1 — Per-variant `dt_out` (output sampling interval) [CLM-17, `verified`]

| Variant | `dt_out` |
|---------|----------|
| `brutus_standard_quasi_random` (standard) | **0.17** |
| `brutus_hierarchical` (hierarchical base) | **0.08** |
| `brutus_hierarchical_gold_standard` (hierarchical gold) | **0.01** |
| `brutus_standard_quasi_random_gold_standard` (standard gold) | **0.01** |

`dt_out` is the output sampling interval, NOT the internal adaptive Bulirsch–Stoer step size.

> Source: `24-VERIFIED-FACTS.md` CLM-09 (v1.5 DATA-04 `confirmed`);
> `simulation_data/Documentation/README.md` § "Brutus Parameters by Variant" (folder defaults
> tol=1e-13/1e-15, Lw, dt_out per variant). Registered as CLM-17 (`verified`) in
> `30-CLAIMS-INVENTORY.md`.

## VF-2 — Per-variant median snapshot count per trajectory [CLM-16, `verified`]

| Variant | Median snapshots / trajectory | Issue-doc claim (superseded) |
|---------|-------------------------------|------------------------------|
| `brutus_standard_quasi_random` (standard) | **61** | ~59 |
| `brutus_hierarchical` (hierarchical base) | **127** | ~125 |
| gold variants (`*_gold_standard`) | **1003** | ~1000 |

The v1.5 DATA-06 probe `corrected` the issue-doc approximations (standard 59→61,
hierarchical 125→127, gold 1000→1003 at stated precision); the **integer-rounded MEDIAN** is the
authoritative D-09 statistic. State BOTH the issue-doc claim and the verified median when a
package figure needs a snapshot count; any package figure that needs a snapshot count uses these
verified medians (CLM-16), NOT the issue-doc `~`-values (CLM-13).

> Source: `24-VERIFIED-FACTS.md` CLM-10 (v1.5 DATA-06 `corrected`). Registered as CLM-16
> (`verified`) in `30-CLAIMS-INVENTORY.md`.

## VF-3 — Gold-gap record: 184 standard IDs without gold counterpart [CLM-14, `verified`]

- `ic_standard_quasi_random/` contains **2,749** ICs (base).
- `ic_standard_quasi_random_for_gold_standard/` contained **2,565** ICs (gold subset, now read
  from the base folder).
- The 2,565 gold-standard ICs are a **byte-identical subset** of the standard ICs (differing only
  in filename prefix).
- **184 ICs** exist in the standard folder but have **no** gold-standard counterpart
  (base − gold = 2,749 − 2,565 = 184); they were simulated at standard Brutus resolution but never
  selected for gold (higher-resolution `dt_out = 0.01`) re-simulation.

> Source: `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (Summary,
> "184 ICs", lines ~7–11; the 184 IDs enumerated lines ~22–42) +
> `24-VERIFIED-FACTS.md` CLM-04 (v1.5 DATA-03 `confirmed`: set size = 184, intersection 184/184
> exact). Registered as CLM-14 (`verified`) in `30-CLAIMS-INVENTORY.md`.

## VF-4 — Quasi-random gold count: ~2,565 gold (base 2,749) [CLM-15, `verified`]

- Brutus base output (`brutus_standard_quasi_random`): **2,749**.
- Brutus gold output (`brutus_standard_quasi_random_gold_standard`): **2,565**.
- base − gold = **184** (the VF-3 gap).

> Source: `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (lines ~7–9) +
> `24-VERIFIED-FACTS.md` CLM-05b (v1.5 DATA-03/04 `confirmed`). Registered as CLM-15 (`verified`)
> in `30-CLAIMS-INVENTORY.md`.

## VF-5 — `D ≈ 4.6416` raw-mass convention (the SCOPE-12-locked counter to `D = 6.694`) [CLM-19, `verified`]

`D = (G · T²)^(1/3) ≈ 4.6416` (with `G = 1`), the **raw-mass** non-dimensionalization constant,
locked Phase 19 (PHYS-01). This is a **SCOPE-12 HARD CONSTRAINT**, not an open question. v1.5
Phase 25 EVID-10 reaffirmed the rejection of the contested **total-mass** form `D = 6.694`
(`D = cbrt(G · M_tot_ref · T²)` with `M_tot_ref = 3.0`). Both values appear so the seed-conflict
is fully registered; only `D ≈ 4.6416` is grounded/locked.

> Source: `ctl_instruction.md` §2.5 (lines ~904–919; "With `G = 1`, `D ~ 4.6416`"; "locked
> Phase 19, PHYS-01") + v1.5 Phase 25 EVID-10 (rejection of 6.694). Registered as CLM-19
> (`verified` / SCOPE-12 hard constraint) in `30-CLAIMS-INVENTORY.md`; the contested `D = 6.694`
> claim is CLM-01 (`claimed-unverified`, verdict-gating).

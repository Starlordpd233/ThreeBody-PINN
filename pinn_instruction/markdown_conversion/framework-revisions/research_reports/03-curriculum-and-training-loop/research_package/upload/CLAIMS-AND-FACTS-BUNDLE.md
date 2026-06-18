# Claims And Facts Bundle

Build date: 2026-06-18. This is a mechanical transport bundle for the
doc-03 research package. Content between BEGIN/END delimiters is
byte-identical to the source package parts, verified at build time by
round-trip extraction and SHA-256 comparison. The wrapper text is not a
source edit and does not summarize the enclosed files.

## Contents

| File | Bytes | SHA-256 |
|------|-------|---------|
| `claims-register.md` | 10,271 | `2f088ffb8a06d0e27b49935aa87cfb3ac05ad843d9fe8388398a8732e25d9ab8` |
| `verified-facts-reference.md` | 5,388 | `48b5615b585227af544b30661c7d2cc4b91b555ecddb0c8508ac31ac5306d9ef` |
| `consolidated-context.md` | 5,407 | `78b877620617a0dcc28d9cd26d8e975b91e6cd234176b766f731c00189c18687` |

===== BEGIN FILE claims-register.md (10271 bytes, sha256 2f088ffb8a06d0e27b49935aa87cfb3ac05ad843d9fe8388398a8732e25d9ab8) =====
# Claims Register (PKG-07) — Claimed vs Verified Figure Grounding

> **Treatment class: GROUNDING-CLASS companion (NOT an authored-narrative upload).** This
> file is the uploaded resolving table for every inline `CLM-NN` reference in
> `framed-research-questions.md`. It is the D-10 analog of `consolidated-context.md` /
> `verified-facts-reference.md`: like those grounding companions, it **retains internal
> repo-path provenance citations on its `verified` rows by design**, because PKG-07
> requires every verified figure be stated *with its v1.5 citation*. It is therefore
> **exempt** from the strict zero-repo-path sweep that applies to the master and the
> agent prompt (that sweep is scoped to those two authored entry points only). Do not
> read the source paths below as fetchable links — see the convention note next.
>
> **Provenance-label convention.** Source paths in the `verified` rows are **provenance
> labels** (where a figure appears in the project repository / which v1.5 verdict grounds
> it), **not navigation links.** The external researcher works only from the attached
> files shipped in this package; the labels exist so a verified figure is traceable to its
> v1.5 origin, not so anything is fetched.

## The no-in-milestone-verification boundary (read this — the single most important v1.6 ≠ v1.5 difference)

> *Unlike v1.5, v1.6 has no parallel empirical-verification phase. No phase in this
> milestone verifies any `claimed-unverified` figure. These figures are unverified inputs
> — do not rely on them as fact. Any figure that would gate a verdict is flagged for FUT
> empirical check (FUT-01 / FUT-02 / FUT-04).*

In v1.5, a dedicated phase re-verified every claimed figure, so the v1.5 register could
defer to it. **v1.6 has nothing equivalent.** Treat every `claimed-unverified` row as an
issue-doc claim, not a fact; where a verdict would turn on such a figure, record the gap
and flag it for FUT empirical check rather than adopting the claimed value.

**Status-classification rule (conservative).** Only **v1.5-verified facts** — committed
v1.5 verdicts plus the dataset documentation plus the locked framework specs — ground a
`verified` status. When in doubt, a figure is `claimed-unverified`.

---

## Claims Table

| CLM ID | Figure | Value (claimed / verified) | Source citation (provenance label, not a link) | Status | FUT-flag |
|--------|--------|----------------------------|--------------------------------------------------|--------|----------|
| CLM-01 | `D = 6.694` derivation | `D = cbrt(G·M_tot_ref·T²)` with `M_tot_ref = 3.0`, `T_scale = 10` → **6.694** | issue-03 (§ "τ_L and L_max Formula Resolution", lines 265, 305) | `claimed-unverified` | **FUT** — verdict-gating: contested total-mass convention; conflicts with the SCOPE-12-locked `D ≈ 4.6416` (CLM-19); rejected by v1.5 Phase 25 EVID-10. Posed as the worked seed-conflict, NOT verified. See Row Notes |
| CLM-02 | Stage 0 trajectory count | ~1,200 | issue-03 (Stage Inventory Summary, line 672) | `claimed-unverified` | FUT (stage-assignment-gating) |
| CLM-03 | Stage 1 trajectory count | ~2,000 | issue-03 line 673 | `claimed-unverified` | FUT |
| CLM-04 | Stage 2 trajectory count | ~1,657 | issue-03 line 674 | `claimed-unverified` | FUT |
| CLM-05 | Stage 3 trajectory count | ~600 | issue-03 line 675 | `claimed-unverified` | FUT |
| CLM-06 | Stage 4 trajectory count | ~1,600 | issue-03 line 676 | `claimed-unverified` | FUT |
| CLM-07 | Stage 6 trajectory count | Unknown (explicitly) | issue-03 line 678 | `claimed-unverified` | FUT |
| CLM-08 | Per-stage `epsilon_phys` / `epsilon_energy` thresholds | 5e-3 … 1e-4 per stage | issue-03 (§ "Stage Transition Criteria", lines 638–646) | `claimed-unverified` | FUT — design hypotheses, "not fixed", FUT-calibrated |
| CLM-09 | `MAX_EPOCHS` table | {0:500 … 6:1200} | issue-03 line 634 | `claimed-unverified` | FUT — design hypothesis |
| CLM-10 | `C_table` gradient-clip values | 8.5 / 5.0 / 3.0 | issue-03 (§ "Gradient Clipping — Merged Specification", line 475) | `claimed-unverified` | FUT — design figure (M14 context); the spec `C` schedule is `7–10 / 5 / 3` |
| CLM-11 | `λ_E` `cap_table` (energy loss weight) | {0:1 … 6:500} | issue-03 lines 372, 655 | `claimed-unverified` | FUT — design figure (M15 context); differs from the PHYS-05 `λ_E^max(k)` schedule |
| CLM-12 | Replay / lookahead / point counts | 240 replay / 16 lookahead / 8192 data-fidelity / 4096 collocation | issue-03 lines 94–95, 554, 577 | `claimed-unverified` | FUT — audit §6 design constants (B-07 / B-08 context) |
| CLM-13 | Snapshot-per-trajectory (issue-doc figures) | ~59 std / ~125 hier / ~1000 gold | issue-03 line 670+ | `claimed-unverified` | — — issue-doc approximations; **superseded by the v1.5-verified values in CLM-16.** See Row Notes |
| CLM-14 | Standard IDs without gold counterpart | **184** | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (Summary, "184 ICs", line ~11) + `24-VERIFIED-FACTS.md` CLM-04 (v1.5 DATA-03 `confirmed`) | `verified` | — |
| CLM-15 | Quasi-random gold count | **2,565** gold (base **2,749**; base − gold = 184) | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (lines ~7–9) + `24-VERIFIED-FACTS.md` CLM-05b (v1.5 DATA-03/04 `confirmed`) | `verified` | — |
| CLM-16 | Per-variant snapshot counts (median) | std **61** / hier **127** / gold **1003** (issue-doc `~59/~125/~1000` **corrected** in v1.5) | `24-VERIFIED-FACTS.md` CLM-10 (v1.5 DATA-06 `corrected`) | `verified` | — — see Row Notes (state both the issue-doc and the corrected values) |
| CLM-17 | Per-variant `dt_out` | std 0.17 / hier base 0.08 / hier gold 0.01 / std gold 0.01 | `24-VERIFIED-FACTS.md` CLM-09 (v1.5 DATA-04 `confirmed`); `simulation_data/Documentation/README.md` § "Brutus Parameters by Variant" | `verified` | — |
| CLM-18 | Hierarchical Brutus output | **4,857** files | `24-VERIFIED-FACTS.md` CLM-06 (v1.5 DATA-03/04 `confirmed`); `simulation_data/Documentation/README.md` § "Brutus Parameters by Variant" | `verified` | — |
| CLM-19 | `D ≈ 4.6416` raw-mass convention (the locked counter to CLM-01) | `D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`); locked Phase 19, PHYS-01 | `ctl_instruction.md` §2.5 (lines ~904–919; "With `G = 1`, `D ~ 4.6416`"; "locked Phase 19, PHYS-01") + v1.5 Phase 25 EVID-10 (rejection of 6.694) | `verified` | — — SCOPE-12 HARD CONSTRAINT; reaffirmed by EVID-10 |
| CLM-20 | M16 `dt_out`-aware collocation-scaling factors | `n_col ∝ dt_base/dt_out`: gold **1×**, hierarchical-base **≈0.125×**, standard-base **≈0.059×** (for `dt_base = 0.01`) | issue-03 lines 106, 440 (M16 / P3-9, audit-verbatim direction) | `claimed-unverified` | FUT — derived design figures; depend on the verified per-variant `dt_out` (CLM-17), but the scaling-factor rule itself is unverified |

---

## Row Notes

**CLM-01 / CLM-19 (the `D` seed-conflict — the worked example).** issue-03 derives
`D = cbrt(G·M_tot·T²) = 6.694` using **total-mass** scaling (CLM-01), while the locked v1.4
PHYS-01 convention uses **raw-mass** `D = (G·T²)^(1/3) ≈ 4.6416` (CLM-19), documented as
locked in `ctl_instruction.md` §2.5. v1.5 Phase 25 EVID-10 reaffirmed the rejection of the
6.694 form. **`D ≈ 4.6416` is the SCOPE-12-LOCKED value** — a hard constraint, not an open
question. The downstream open question is therefore the **reconciliation of issue-03's
`τ_L` / `L_max` derivation under the locked `D ≈ 4.6416`** — i.e. how the formulas resolve
given the locked `D`, NOT *which* `D` is correct. CLM-01 is `claimed-unverified` and posed
neutrally as the conflict; CLM-19 is the `verified` / locked counter-position. Both `6.694`
and `4.6416` are registered so the seed-conflict is fully captured.

**CLM-02..CLM-07 (stage trajectory counts).** Per-stage population counts from the issue-03
Stage Inventory Summary — dataset-derived design outputs of an *adaptive* stage-assignment
methodology. No v1.6 phase verifies them; they are unverified inputs flagged for FUT. (The
`~2,565` gold count that appears alongside them IS v1.5-verified — that anchor is CLM-15, a
gold count, not a stage count.)

**CLM-08..CLM-12, CLM-20 (design figures).** Per-stage thresholds, `MAX_EPOCHS`, `C_table`,
`λ_E` cap, the replay/lookahead/point counts, and the M16 scaling factors are audit §6 /
training-loop **design constants**, explicitly "not fixed" in issue-03. They are
claimed-unverified design hypotheses, FUT-calibrated; none is a dataset fact.

**CLM-13 vs CLM-16 (snapshot counts — issue-doc vs v1.5-verified).** The issue-doc figures
`~59 std / ~125 hier / ~1000 gold` (CLM-13) are **claimed-unverified approximations**. The
v1.5-verified per-variant **median** snapshot counts are **61 / 127 / 1003** (CLM-16, v1.5
DATA-06 `corrected`). State BOTH: the issue-doc `~`-values are the claim, the v1.5 median is
the verified fact. Any package figure that needs a snapshot count uses CLM-16, not CLM-13.

**Non-dataset figures (excluded by design).** The full issue-03 read surfaced framework-spec
design / numerical-stability parameters that are **NOT dataset/empirical figures** and so
carry no CLM row: the stage-transition strict-criteria constants (`ε_plateau = 1e-5`,
`ε_phys = 1e-4`, `ε_energy = 1e-4`, the locked `ε_H = 1e-4·S_H` floor); the `τ_L` split
softening `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`; the ALM `μ_p` clamp `[1e-4, 100.0]`;
the gradient-clip `5.0 × median` factor and the `C` schedule `7–10 / 5 / 3`; and the PHYS-05
loss-weight warmup schedule. These are spec contracts cited by section anchor in
`framed-research-questions.md`, not empirical claims; registering them here would
mis-classify spec parameters as dataset figures. (The issue-doc *numeric instantiations*
`C_table = 8.5/5.0/3.0` and the `λ_E cap_table` ARE registered, as CLM-10 and CLM-11.)

**Every `verified` row carries an exact v1.5 grounding citation** (CLM-14..CLM-19): each
cites a `24-VERIFIED-FACTS.md` verdict and/or the dataset documentation and/or
`ctl_instruction.md` §2.5. No figure is `verified` without such a citation. These citations
are provenance labels, not links (see the convention note at the top).

===== END FILE claims-register.md =====

===== BEGIN FILE verified-facts-reference.md (5388 bytes, sha256 48b5615b585227af544b30661c7d2cc4b91b555ecddb0c8508ac31ac5306d9ef) =====
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

===== END FILE verified-facts-reference.md =====

===== BEGIN FILE consolidated-context.md (5407 bytes, sha256 78b877620617a0dcc28d9cd26d8e975b91e6cd234176b766f731c00189c18687) =====
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

===== END FILE consolidated-context.md =====

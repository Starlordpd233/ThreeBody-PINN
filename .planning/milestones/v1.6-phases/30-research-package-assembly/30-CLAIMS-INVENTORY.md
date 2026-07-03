# Phase 30: CLM Claims Register (PKG-07) — EXTENDED (no longer provisional)

> **STATUS: EXTENDED 2026-06-18 in 30-04 after the full issue-03 read (F6) — NO LONGER
> PROVISIONAL.** This file is the phase-local PKG-07 source-of-truth claims register (the
> v1.5 `23-CLAIMS-INVENTORY.md` analog). It was seeded in 30-01 from the 30-RESEARCH
> pre-scan (C-1..C-13 claimed-unverified rows + V-1..V-6 verified anchors → CLM-01..CLM-19).
> It is now **extended in 30-04** after issue-03 was read in full: the full-read figure
> sweep added CLM-20 (M16 collocation-scaling factors) and the "Non-dataset figures
> (excluded by design)" note below; additional package-stated figures receive the next
> `CLM-NN` ID (append-only — existing IDs are NEVER renumbered). The **uploaded** form is
> the `claims-register.md` companion produced in 30-04 (a grounding-class derivative that
> MAY retain repo-path provenance labels — NOT a strict-grep upload).

**Purpose:** This register enumerates every dataset/empirical figure that the research package
will state, with a stable `CLM-NN` ID, classified as `claimed-unverified` (issue-03 value, no
verifier) or `verified` (with its exact v1.5 citation). All inline figure mentions anywhere in
the package MUST reference their CLM ID; no figure may be stated as fact without a CLM row
(D-15, Pitfall 3).

**Status-classification rule (D-16, conservative):** Only **v1.5-verified facts** — committed
v1.5 artifacts (`.planning/milestones/v1.5-phases/**`) plus `simulation_data/Documentation/`
plus the locked framework specs (`ctl_instruction.md`) — count as grounding for `verified`.
When in doubt → `claimed-unverified` (over-marking is the safe direction).

**Created:** 2026-06-18
**Append-only policy:** Existing CLM IDs are never renumbered. The `FUT-flag` column replaces
the v1.5 "Phase-24 check" column — v1.6 has NO Phase-24 analog (D-17), so there is no
in-milestone verification column; instead verdict-gating figures are flagged for FUT.

---

## The no-in-milestone-verification boundary (D-17 — MUST appear; the single most important v1.6 ≠ v1.5 difference)

> *Unlike v1.5, v1.6 has no parallel empirical-verification phase. No phase in this milestone
> verifies any `claimed-unverified` figure. These figures are unverified inputs — do not rely
> on them as fact. Any figure that would gate a verdict is flagged for FUT empirical check
> (FUT-01/FUT-02/FUT-04).*

In v1.5, Phase 24 re-verified every claimed figure in the package, so the v1.5 register could
defer ("Phase 24 verifies everything anyway"). **v1.6 has nothing equivalent.** The package must
carry "claimed, unverified" honestly and delegate verification downstream (external research /
FUT). No plan may assume a later v1.6 phase will check a package figure.

---

## Claims Table

| CLM ID | Figure | Value (claimed / verified) | Source citation | Status | FUT-flag |
|--------|--------|----------------------------|-----------------|--------|----------|
| CLM-01 | `D = 6.694` derivation | `D = cbrt(G·M_tot_ref·T²)` with `M_tot_ref = 3.0`, `T_scale = 10` → **6.694** | issue-03 lines 265, 305 | `claimed-unverified` | **FUT** — verdict-gating: contested convention, conflicts with the verified/SCOPE-12-locked `D ≈ 4.6416` (CLM-19); rejected by v1.5 Phase 25 EVID-10. Posed as the worked seed-conflict, NOT verified. See Row Notes |
| CLM-02 | Stage 0 trajectory count | ~1,200 | issue-03 line 672 (Stage Inventory Summary) | `claimed-unverified` | FUT (stage-assignment-gating) |
| CLM-03 | Stage 1 trajectory count | ~2,000 | issue-03 line 673 | `claimed-unverified` | FUT |
| CLM-04 | Stage 2 trajectory count | ~1,657 | issue-03 line 674 | `claimed-unverified` | FUT |
| CLM-05 | Stage 3 trajectory count | ~600 | issue-03 line 675 | `claimed-unverified` | FUT |
| CLM-06 | Stage 4 trajectory count | ~1,600 | issue-03 line 676 | `claimed-unverified` | FUT |
| CLM-07 | Stage 6 trajectory count | Unknown (explicitly) | issue-03 line 678 | `claimed-unverified` | FUT |
| CLM-08 | Per-stage `epsilon_phys` / `epsilon_energy` thresholds | 5e-3 … 1e-4 per stage | issue-03 lines 638–646 | `claimed-unverified` | FUT — design hypotheses, "not fixed", FUT-calibrated |
| CLM-09 | `MAX_EPOCHS` table | {0:500 … 6:1200} | issue-03 line 634 | `claimed-unverified` | FUT — design hypothesis |
| CLM-10 | `C_table` gradient-clip values | 8.5 / 5.0 / 3.0 | issue-03 line 475 | `claimed-unverified` | FUT — design figure (M14 context) |
| CLM-11 | `λ_E` `cap_table` (energy loss weight) | {0:1 … 6:500} | issue-03 lines 372, 655 | `claimed-unverified` | FUT — design figure (M15 context) |
| CLM-12 | Replay / lookahead / point counts | 240 replay / 16 lookahead / 8192 data-fidelity / 4096 collocation | issue-03 lines 94–95, 554, 577 | `claimed-unverified` | FUT — audit §6 design constants (B-07 / B-08 context) |
| CLM-13 | Snapshot-per-trajectory (issue-doc figures) | ~59 std / ~125 hier / ~1000 gold (referenced via the stage `dt_out` table) | issue-03 line 670+ | `claimed-unverified` | — — issue-doc approximations; **superseded by the v1.5-verified values in CLM-16.** See Row Notes |
| CLM-14 | Standard IDs without gold counterpart | **184** | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (Summary, "184 ICs", line ~11) + `24-VERIFIED-FACTS.md` CLM-04 (v1.5 DATA-03 `confirmed`) | `verified` | — |
| CLM-15 | Quasi-random gold count | **2,565** gold (base **2,749**; base − gold = 184) | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (lines ~7–9) + `24-VERIFIED-FACTS.md` CLM-05b (v1.5 DATA-03/04 `confirmed`) | `verified` | — |
| CLM-16 | Per-variant snapshot counts (median) | std **61** / hier **127** / gold **1003** (issue-doc `~59/~125/~1000` **corrected** in v1.5) | `24-VERIFIED-FACTS.md` CLM-10 (v1.5 DATA-06 `corrected`) | `verified` | — — see Row Notes (state both the issue-doc and the corrected values) |
| CLM-17 | Per-variant `dt_out` | std 0.17 / hier base 0.08 / hier gold 0.01 / std gold 0.01 | `24-VERIFIED-FACTS.md` CLM-09 (v1.5 DATA-04 `confirmed`); `simulation_data/Documentation/README.md` Brutus Parameters by Variant | `verified` | — |
| CLM-18 | Hierarchical Brutus output | **4,857** files | `24-VERIFIED-FACTS.md` CLM-06 (v1.5 DATA-03/04 `confirmed`); `simulation_data/Documentation/README.md` Brutus Parameters by Variant | `verified` | — |
| CLM-19 | `D ≈ 4.6416` raw-mass convention (the locked counter to CLM-01) | `D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`); locked Phase 19, PHYS-01 | `ctl_instruction.md:904–919` (§2.5; line ~910 "With `G = 1`, `D ~ 4.6416`"; "locked Phase 19, PHYS-01") | `verified` | — — SCOPE-12 HARD CONSTRAINT; v1.5 Phase 25 EVID-10 reaffirmed the rejection of CLM-01's 6.694 |
| CLM-20 | M16 `dt_out`-aware collocation-scaling factors | `n_col ∝ dt_base/dt_out`: gold **1×**, hierarchical-base **≈0.125×**, standard-base **≈0.059×** (for `dt_base = 0.01`) | issue-03 lines 106, 440 (M16 / P3-9, audit-verbatim direction) | `claimed-unverified` | FUT — derived design figures (M16 context); depend on the **verified** per-variant `dt_out` (CLM-17) but the scaling-factor rule itself is an unverified design hypothesis |

---

## Row Notes

**CLM-01 / CLM-19 (the `D` seed-conflict — the worked example).** issue-03 derives
`D = cbrt(G·M_tot·T²) = 6.694` using **total-mass** scaling (CLM-01), while the locked v1.4
PHYS-01 convention uses **raw-mass** `D = (G·T²)^(1/3) ≈ 4.6416` (CLM-19), and `ctl_instruction.md`
§2.5 explicitly documents the raw-mass form as locked. v1.5 Phase 25 EVID-10 reaffirmed the
rejection of the 6.694 form. **`D ≈ 4.6416` is the SCOPE-12-LOCKED value** — it is a hard
constraint, not an open question. The downstream open question (for the resolution doc /
Phase 32) is therefore the **reconciliation of issue-03's `tau_L` derivation under the locked
`D ≈ 4.6416`** — i.e. how the `tau_L`/`L_max` formulas resolve given the locked `D`, NOT *which*
`D` value is correct. CLM-01 is registered `claimed-unverified` and posed neutrally as the
conflict; CLM-19 is the `verified` / locked counter-position. Both `6.694` and `4.6416` appear so
the seed-conflict is fully registered.

**CLM-02..CLM-07 (stage trajectory counts).** These are the per-stage population counts in the
issue-03 Stage Inventory Summary (lines 668–680). They are dataset-derived design outputs of an
*adaptive* stage-assignment methodology (see `stage_strat_revision.md`, Part III). No v1.6 phase
verifies them; per D-17 they are unverified inputs flagged for FUT. (The `~2,565` gold count that
appears alongside them IS v1.5-verified — that anchor is CLM-15, not a stage count.)

**CLM-08..CLM-12 (design figures).** Per-stage thresholds, `MAX_EPOCHS`, `C_table`, `λ_E` cap, and
the replay/lookahead/point counts are audit §6 / training-loop **design constants**, explicitly
"not fixed" in issue-03. They are claimed-unverified design hypotheses, FUT-calibrated; none is a
dataset fact.

**CLM-13 vs CLM-16 (snapshot counts — issue-doc vs v1.5-verified).** The issue-doc figures
`~59 std / ~125 hier / ~1000 gold` (CLM-13) are **claimed-unverified approximations**. The
v1.5-verified per-variant **median** snapshot counts are **61 / 127 / 1003** (CLM-16, v1.5
DATA-06 `corrected`: standard 59→61, hierarchical 125→127, gold 1000→1003 at stated precision).
State BOTH: the issue-doc `~`-values are the claim, the v1.5 median is the verified fact. Any
package figure that needs a snapshot count uses CLM-16, not CLM-13.

**CLM-20 (M16 collocation-scaling factors — added in the 30-04 full-read sweep).** The
factors `gold 1× / hier ≈0.125× / std ≈0.059×` are the audit-verbatim `n_col ∝ dt_base/dt_out`
direction (issue-03 lines 106, 440). They are **derived** design figures: the per-variant
`dt_out` they divide by IS v1.5-verified (CLM-17), but the scaling *rule* and the resulting
factors are an unverified design hypothesis (FUT-flagged). Registered claimed-unverified.

**Non-dataset figures (excluded by design — the 30-04 full-read F6 sweep result).** The
full issue-03 read surfaced additional numeric values that are **framework-spec design /
numerical-stability parameters, NOT dataset/empirical figures**, and therefore receive NO
CLM row (D-15 scopes the register to dataset/empirical figures). These are grounded as
framework-spec contracts and cited in `framed-research-questions.md` by spec section
anchor, not by CLM ID:
- Stage-transition strict-criteria constants: `ε_plateau = 1e-5` (patience 200), validation
  stability, `ε_phys = 1e-4`, `ε_energy = 1e-4`, and the locked energy floor `ε_H = 1e-4·S_H`
  (`ctl_instruction.md` § "Stage Transition Criteria"; the floor is a SCOPE-12-locked PHYS-04
  contract).
- `τ_L` split softening parameters `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`
  (issue-03 § "τ_L and L_max Formula Resolution"; CURR-02 framework contract, distinct from
  the locked loss-side `eps_soft = 1e-5`).
- ALM `μ_p` clamp bounds `[1e-4, 100.0]` (issue-03 § "ALM Parameter Update"; a design
  constant on the optional P2 scalar-constraint ALM ablation).
- Gradient-clip factor `5.0 × median` (`pinn_architecture.md §4.4`) and the `C` schedule
  `7–10 / 5 / 3` (`ctl_instruction.md`); the issue-doc `C_table` numeric instantiation
  `8.5/5.0/3.0` IS registered (CLM-10) as the design figure.
- The PHYS-05 loss-weight warmup schedule values in `pinn_architecture.md §4.1`; the
  issue-doc capped-hybrid `cap_table` instantiation IS registered (CLM-11).
These are framework-spec parameters (locked or revisable-baseline), not claimed dataset
facts; registering them as CLM figures would mis-classify spec contracts as empirical claims.

**Every `verified` row carries an exact v1.5 grounding citation** (CLM-14..CLM-19): each cites a
`24-VERIFIED-FACTS.md` CLM verdict and/or `simulation_data/Documentation/` and/or
`ctl_instruction.md:904–919`. No figure is `verified` without such a citation (D-16).

---

*This register is the phase-local source of truth for the PKG-07 claims list. It was seeded in
30-01 and **extended in 30-04 after the full issue-03 read (F6) — it is no longer provisional**
(CLM-20 added; the non-dataset exclusion note recorded). The uploaded form is the 30-04
`claims-register.md` companion (F1/F6). Content/source-commit provenance for the verified
anchors' grounding sources is recorded in `30-SNAPSHOT-HASHES.txt`.*

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

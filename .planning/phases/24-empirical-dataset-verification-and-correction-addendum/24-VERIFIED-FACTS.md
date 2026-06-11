# 24-VERIFIED-FACTS.md — Phase 24 Verified-Facts Register

**Phase:** 24 — Empirical Dataset Verification and Correction Addendum
**Plan:** 24-01 (Wave 1)
**Created:** 2026-06-11
**Re-derivability standard (D-02):** every fact below carries the exact repo-root probe command, the dataset path it ran against, the observed value, and the run date. Any later agent or the user can reproduce every count without this session's context.
**Verdict vocabulary (D-08):** `confirmed` (observed matches claim) | `corrected` (observed differs; both recorded) | `unverified` (probe could not run within grounding limits, reason recorded — never a shortcut for "didn't get to it").
**Read-only fences (D-01):** all probes are read-only over `simulation_data/`. `git status --short simulation_data/` was clean after every probe run (verified 2026-06-11).

## Verdicts Table

| CLM ID | Owning DATA | Claimed value | Observed value | Probe command | Dataset path | Run date (UTC) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-01 | DATA-01 | 1,250 gaps out of 4,000 nominal (31.2%) — standard | n=2,749 files; min_id=0; max_id=3,998; gaps[0..max]=**1,250**; gaps[0..3999]=1,251 | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py` | `simulation_data/Data/brutus_output/brutus_standard_quasi_random` | 2026-06-11 | **confirmed** |
| CLM-02 | DATA-01 | 143 gaps out of 5,000 nominal (2.9%) — hierarchical | n=4,857 files; min_id=0; max_id=4,999; gaps[0..max]=**143**; gaps[0..4999]=143 (identical) | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py` | `simulation_data/Data/brutus_output/brutus_hierarchical` | 2026-06-11 | **confirmed** |
| CLM-03 | DATA-02 | 65 IDs (2 hierarchical + 63 standard) | `{hierarchical: 2, standard: 63}` total **65** | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data02_blacklist.py` | `simulation_data/Documentation/problematic_ics_blacklist.json` | 2026-06-11 | **confirmed** |
| CLM-04 | DATA-03 | 184 standard IDs without gold counterpart | `base_ids − gold_ids` set size = **184**; doc `standard_quasi_random_ids_not_in_gold.md` lists exactly 184 IDs; intersection = 184/184 (exact match) | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py` | `simulation_data/Data/brutus_output/{brutus_standard_quasi_random,brutus_standard_quasi_random_gold_standard}` + `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | 2026-06-11 | **confirmed** |
| CLM-05 | DATA-03/04 | 2,749 base vs 2,565 gold (standard) — WR-04 split | IC folder: **2,749**; Brutus base output: **2,749**; Brutus gold output: **2,565**; base−gold = 184 | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py` | `simulation_data/Data/ic_final/ic_standard_quasi_random` (IC) + `simulation_data/Data/brutus_output/brutus_standard_quasi_random{,_gold_standard}` (Brutus outputs) | 2026-06-11 | **confirmed** |
| CLM-12 | DATA-01 | ~4,000 standard / ~5,000 hierarchical nominal IC counts | At stated precision (`~` = approximate), standard observed max_id=3,998 → ~4,000; hierarchical observed max_id=4,999 → ~5,000. Per D-09 the full ID distribution is recorded above (CLM-01/02 rows); the `~` approximation is consistent with the observed max IDs at ±0.1% (3998/4000=99.95%, 4999/5000=99.98%). | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py` | `simulation_data/Data/brutus_output/{brutus_standard_quasi_random,brutus_hierarchical}` | 2026-06-11 | **confirmed** |

## D-13 Nominal-Range Convention (Grounding)

Per D-13, the "nominal IC count" convention is grounded in:
- **`simulation_data/Documentation/README.md:146-153`** — the "Dataset Variants and Inventory" table explicitly declares the ID Range as `0000-3998` (standard) and `0000-4999` (hierarchical), with a "Gaps" column equal to 1,250 and 143 respectively. The README's gaps match `gaps[0..max]` exactly (and disagree with `gaps[0..3999]` = 1,251 for standard).
- `simulation_data/Scripts/ic_generation/generate_ics.py:15-16` uses `N_SAMPLES_STANDARD=2500` / `N_SAMPLES_HIERARCHICAL=1500` (per-run, with `start_from_last=True` for continuation); the cumulative 4,000/5,000 figures correspond to the prescreening cumulative index, not the per-run sample size.
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py` — read for ID allocation / perturbation provenance; does not contradict the README convention.

**Convention adopted:** nominal end = observed max ID. `gaps[0..max]` is the authoritative gap count. This is the same convention the README uses and is the only convention that yields the claimed gap figures. The probe emits BOTH `gaps[0..max]` and `gaps[0..nominal_end=3999/4999]` for transparency; the additional count is a non-canonical artifact included for the record.

## DATA-02 Nuanced Consumption Map (CLM-03, M11 finding)

Per D-10 (SCOPE-07 grounding only):

| Path | Status | Evidence |
| --- | --- | --- |
| `simulation_data/Validation/dataset_readiness_checks/{config,validator}.py` + `modules/{blacklist,correspondence}.py` + `modules/__init__.py` | **Loads** `problematic_ics_blacklist.json` | Probe grep result (5 files) |
| `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` + `run_brutus_hierarchical_only_mac_gold_standard.py` | **Do not load the json** (mention blacklist in source but use `Documentation/problematic_ics/{type}/` dirs; per README:1005 the json is "legacy … not used by current runners") | Probe grep result + README:1005 |
| `simulation_data/Scripts/archived/manage_problematic_ics_notusing.py` | Archived; not active | Probe grep result |
| `pinn/` training-time load | **`unverified — outside grounding limits (SCOPE-10)`**; deferred to Phase 25 adjudication and the FUT-01 handoff | D-10 boundary |

**CLM-03 verdict:** `confirmed` (count 65, composition {hierarchical: 2, standard: 63}).
**M11 (blacklist not loaded at training time) verdict:** `unverified — outside grounding limits, deferred to Phase 25 adjudication and the FUT-01 handoff`.

## D-11 Doc-Contradiction Check

No contradiction was observed between any probe output and the package claims register (`RESEARCH-CONTEXT-MASTER.md` §"CLM Claims Register") for CLM-01..05 or CLM-12. The empirical observations (1,250 / 143 / 65 / 184 / 2,749-vs-2,565) match the package claims exactly. No README correction is proposed at this time.

## DATA-04/05/06 Rows (plan 24-02 — placeholder)

The following CLM rows are owned by plan 24-02 (footer / parameter probes DATA-04, mass-drift DATA-05, snapshot/dt_out distributions DATA-06) and will be recorded here after plan 24-02 completes:

- CLM-06: Hierarchical folder counts (4,857 / 4,857) — DATA-03/04
- CLM-07: 219 standard-gold files with no `Result:` footer — DATA-04
- CLM-08: 592 `tol=1e-14` files — DATA-04
- CLM-09: folder-default parameter tuples (tol/Lw/dt_out per variant) — DATA-04
- CLM-10: per-trajectory snapshot-count distribution — DATA-06
- CLM-11: prevalence of `final_timestep >= 9.5` rule — DATA-06

## Anomalies (D-12)

No anomalies (D-12 — discrepancies that contradict no package-stated claim) surfaced from this plan's probes. The standard 2,749-vs-2,750 arithmetic wrinkle flagged in RESEARCH Open Q1 reconciled as: 1,250 gaps from `gaps[0..max]` per the README's ID Range convention. There is no off-by-one.

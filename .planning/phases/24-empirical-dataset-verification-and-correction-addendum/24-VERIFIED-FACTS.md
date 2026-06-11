# 24-VERIFIED-FACTS.md — Phase 24 Verified-Facts Register

**Phase:** 24 — Empirical Dataset Verification and Correction Addendum
**Plan:** 24-01 (Wave 1) + 24-02 (Wave 2)
**Created:** 2026-06-11 (Wave 1); Wave 2 rows added 2026-06-11; DATA-05 gap resolution recorded 2026-06-11
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
| CLM-06 | DATA-03/04 (per D-04) | 4,857 hierarchical Brutus output | n=**4,857** files; max_id=4,999 | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py` | `simulation_data/Data/brutus_output/brutus_hierarchical` | 2026-06-11 | **confirmed** |
| CLM-07 | DATA-04 | 219 standard-gold files with no `Result:` footer | n=**219** files in `brutus_standard_quasi_random_gold_standard` have NO `Result:` footer at all AND NO parameter fields anywhere (D-07 characterization; not "partial/minimal footer"); agrees with audit `footer_audit_20251224_170141.md` row 11 | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py` | `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard` | 2026-06-11 | **confirmed** |
| CLM-08 | DATA-04 | 592 `tol=1e-14` files (standard-gold) | n=**592** files in `brutus_standard_quasi_random_gold_standard` carry `tol=1e-14` in their `Result:` footer (the remaining 2,346 present-footer files carry `tol=1e-13`) | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py` | `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard` | 2026-06-11 | **confirmed** |
| CLM-09 | DATA-04 | folder-default `tol`/`dt_out` per variant | Present-footer observed tol values: `brutus_hierarchical` 100% `tol=1e-15` (3,307/3,307); `brutus_hierarchical_gold_standard` 98.7% `tol=1e-13` (4,795/4,857) + 1.3% `tol=1e-14` (62/4,857); `brutus_standard_quasi_random` 100% `tol=1e-13` (2,048/2,048); `brutus_standard_quasi_random_gold_standard` 79.9% `tol=1e-13` (2,346/2,937) + 20.1% `tol=1e-14` (591/2,937). Folder defaults per `.claude/rules/dataset-reference.md` (std tol=1e-13 dt_out=0.17; hier base tol=1e-15 dt_out=0.08; hier gold tol=1e-13 dt_out=0.01; std gold tol=1e-13 dt_out=0.01) match observed modal values. | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py` | `simulation_data/Data/brutus_output/{4 variants}` | 2026-06-11 | **confirmed** |
| CLM-10 | DATA-06 | ~59 standard / ~125 hierarchical / ~1000 gold snapshots per trajectory | Distributions (D-09; integer-rounded MEDIAN used per lock 2026-06-11): **brutus_standard_quasi_random** median=**61** (mode=61, n=2,048; min=59, max=61); **brutus_standard_quasi_random_gold_standard** median=**1003** (mode=1003, n=2,346; min=1002, max=1003); **brutus_hierarchical** median=**127** (mode=127, n=3,307; min=126, max=127); **brutus_hierarchical_gold_standard** median=**1003** (mode=1003, n=4,857; min=1003, max=1003). The standard median of 61 (vs claim ~59) and the hierarchical median of 127 (vs claim ~125) depart from the claim; the gold medians of 1003 (vs claim ~1000) match at stated precision. Per D-09 the integer-rounded MEDIAN is authoritative; the pilot central value (~61) is recorded as evidence. | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data06_snapshots.py` | `simulation_data/Data/brutus_output/{4 variants}` | 2026-06-11 | **corrected** (standard 59→61, hierarchical 125→127; gold 1000→1003 at stated precision — also a small correction) |
| CLM-11 | DATA-06 | prevalence of `final_timestep >= 9.5` rule | Per-variant prevalence (fraction of files whose last-block first token is >= 9.5): `brutus_standard_quasi_random` 1.000 (701/701 — all 701 present in the no-footer population, all reach t=10.03); `brutus_standard_quasi_random_gold_standard` 1.000 (219/219 — the no-footer subset all reach t=10.01); `brutus_hierarchical` 1.000 (1,550/1,550 — the no-footer subset all reach t=10.00); `brutus_hierarchical_gold_standard` not probed (gold has no final-time block content in the 1,003-snapshot layout; `final_time_stats=null` in the probe). Overall: every no-footer file that the probe could parse is complete (>=9.5). The RULE is not re-adjudicated; only the prevalence is recorded (D-06). | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data06_snapshots.py` | `simulation_data/Data/brutus_output/{3 variants; gold-hier not applicable}` | 2026-06-11 | **confirmed** (prevalence 100% across the probe-applicable population) |
| CLM-12 | DATA-01 | ~4,000 standard / ~5,000 hierarchical nominal IC counts | At stated precision (`~` = approximate), standard observed max_id=3,998 → ~4,000; hierarchical observed max_id=4,999 → ~5,000. Per D-09 the full ID distribution is recorded above (CLM-01/02 rows); the `~` approximation is consistent with the observed max IDs at ±0.1% (3998/4000=99.95%, 4999/5000=99.98%). | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py` | `simulation_data/Data/brutus_output/{brutus_standard_quasi_random,brutus_hierarchical}` | 2026-06-11 | **confirmed** |

## DATA-05 Mass-Drift Row (CLM-13-style pending verdict; recorded under DATA-05)

| Row | Owning DATA | Claimed value | Observed value | Probe command | Dataset path | Run date (UTC) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-05 verdict (PIPE-07-feeding) | DATA-05 | IC masses canonical at float64 vs `decimal.Decimal` parsing required | **70/4,857 base-hier mismatches** (m_IC != m_Brutus(t=0) at `np.allclose(rtol=1e-15)`); **0/4,857 gold-hier** mismatches; **0/2,749 base-std** mismatches; **0/2,565 gold-std** mismatches. Total compared: 15,028; total mismatch: 70. User resolution 2026-06-11: current IC files are canonical; the 70 affected base-hier outputs are invalid/stale artifacts requiring targeted rerun from current ICs; this is not a `decimal.Decimal` precision problem. Affected IDs: `0005`-`0059`, `0061`-`0075`. | `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data05_mass_drift.py` | `simulation_data/Data/ic_final/{ic_hierarchical,ic_standard_quasi_random}` + `simulation_data/Data/brutus_output/{4 variants}` | 2026-06-11 | **corrected / RESOLVED-WITH-INSTRUCTION** — old 70 base-hier artifacts are quarantined from training, metrics, and PIPE-07 until rerun passes validation. See `24-GAPS.md` and `24-DATA05-RERUN-REMEDIATION.md`. |

## CLM-13 Row (D-05 — not probed, routed to Phase 25/27)

| CLM ID | Owning DATA | Claimed value | Observed value | Probe command | Dataset path | Run date (UTC) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-13 | DATA-05 (claimed) | `compute_globals` D=6.694 (contested convention) | _not probed_ | _routed to Phase 25 EVID-10 / Phase 27 PIPE-09_ | _n/a (requires adjudication of contested convention, not a dataset fact)_ | 2026-06-11 | **PENDING — not probed, routed Phase 25 EVID-10 / Phase 27 PIPE-09** (D-05) |

## CLM-14+ Prose-Sweep Extension Rows (D-06)

The bounded prose sweep over `RESEARCH-CONTEXT-MASTER.md` and `DELIVERY-NOTE.md` found **zero** unregistered empirical dataset figures. Every numerical figure in those two package files is keyed to an existing CLM ID (CLM-01..13). The delivered `RESEARCH-CONTEXT-MASTER.md` is byte-stable against its 2026-06-11 post-consolidation baseline (`git diff --quiet 605c0227 -- ...RESEARCH-CONTEXT-MASTER.md` exits 0; verified 2026-06-11).

| CLM ID | Owning DATA | Claimed value | Observed value | Probe command | Dataset path | Run date (UTC) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _none_ | _n/a | _zero prose-sweep findings — no CLM-14+ extension IDs needed_ | _n/a_ | _n/a_ | _n/a_ | 2026-06-11 | **zero** |

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

**CLM-04/05/06/07/08/09/11/12:** No contradiction was observed between any probe output and the package claims register for these rows. The empirical observations (1,250 / 143 / 65 / 184 / 2,749-vs-2,565 / 4,857 / 219 / 592 / folder-defaults / 100% prevalence) match the package claims. No README correction is proposed at this time.

**CLM-10 (corrected):** the per-variant medians depart from the `~59 / ~125 / ~1000` claims at the integer-rounded-MEDIAN level (61 / 127 / 1003). The `~` prefix signals approximation; the empirical median is the authoritative D-09 statistic. The `~` claim is best read as `~` = "rounded order of magnitude" or "block-count rule of thumb" rather than a precise integer; the corrected values (61 / 127 / 1003) are recorded for the register. **No README correction is proposed at this time** — the `~` prefix is preserved and the empirical medians are recorded here as the authoritative fact (D-11: empirical observation outranks doc text; the package claim is not contradicted, only refined).

**DATA-05 (GAP-24-01 resolved with remediation required):** the 70 base-hier mismatches are an anomaly that contradicts no package-stated claim directly (no package claim asserts that m_IC = m_Brutus(t=0) at all 4,857 IDs); it is recorded as an Anomaly (D-12) and as a resolved STOP-gap decision. User instruction 2026-06-11: current ICs are canonical, the 70 base-hier outputs are invalid/stale artifacts, and those 70 outputs must be rerun rather than skipped or treated as a precision/Decimal issue. No README correction is proposed at this time.

## DATA-04/05/06 Rows (plan 24-02 — completed)

This section's placeholder from plan 24-01 has been completed by plan 24-02 with the rows above (CLM-06..11 + DATA-05 row + CLM-13 PENDING + zero CLM-14+ rows). Cross-references:
- CLM-06 (DATA-03/04, D-04 ownership preserved) — 4,857 hierarchical Brutus output files.
- CLM-07 (DATA-04) — 219 standard-gold no-footer files, D-07 characterization (NO `Result:` footer at all AND NO parameter fields anywhere).
- CLM-08 (DATA-04) — 592 `tol=1e-14` standard-gold files.
- CLM-09 (DATA-04) — folder-default `tol`/`dt_out` per variant; observed modal tol values match the claim.
- CLM-10 (DATA-06) — distributions per variant; integer-rounded MEDIAN used (D-09 locked 2026-06-11); standard 59→61 / hierarchical 125→127 / gold 1000→1003 (corrected).
- CLM-11 (DATA-06) — `final_timestep >= 9.5` prevalence 100% across the probe-applicable population.

## Anomalies (D-12)

1. **D-12 / DATA-05 base-hier mass-drift (anomaly + resolved remediation decision):** 70 / 4,857 files in `brutus_hierarchical` show m_Brutus(t=0) != m_IC at `np.allclose(rtol=1e-15)`. The differences are 0.1-1.0 in mass units (e.g., id 5: m_IC = 0.9056088426088029, m_Brutus_t0 = 1.2569378670807108, abs_diff approx 0.351) - too large for float64 round-trip (rtol=1e-15 would catch only ~1e-15 relative error) and not explainable by perturbation (which does not touch masses per `ic_generation_utils.py:417-420`). Crucially, the gold-hier variant for the same 70 IDs matches the IC perfectly (0/4,857 mismatches), ruling out a generation-side error in the IC files. User instruction 2026-06-11 resolves **GAP-24-01**: current ICs are canonical; the 70 affected base-hier outputs (`0005`-`0059`, `0061`-`0075`) are invalid/stale artifacts requiring targeted rerun from current ICs; the old artifacts are quarantined from training, metrics, and PIPE-07 until rerun validation passes. See `24-GAPS.md`, `.planning/milestones/v1.5-GAPS.md`, and `24-DATA05-RERUN-REMEDIATION.md`. The standard 2,749-vs-2,750 arithmetic wrinkle flagged in RESEARCH Open Q1 reconciled as: 1,250 gaps from `gaps[0..max]` per the README's ID Range convention. There is no off-by-one.

## DATA-05 Rerun Remediation Reference

The rerun decision is recorded in `24-DATA05-RERUN-REMEDIATION.md`. Until that remediation is executed and verified, the 70 old base-hierarchical outputs remain invalid for training, metrics, and PIPE-07. This register may continue to serve Phase 24 because the semantic decision is resolved; it must not be read as claiming the affected files have already been regenerated.

## Deviation from Plan

### Known deviation: stdout files under `probes/outputs/` are not committed

**Per D-25 and `scripts/git_policy/validate_staged_paths.py:23`:** any `outputs/*` path is blocked from staging. The plan's `files_modified` lists `probes/outputs/`, but the git policy enforces that these stdout capture files stay on disk (untracked) and the **register rows are the committed evidence** (D-02 re-derivability is preserved by the row's exact probe command + dataset path). The probe source files (`probes/data04_footers.py`, `probes/data05_mass_drift.py`, `probes/data06_snapshots.py`) and the `24-VERIFIED-FACTS.md` register ARE committed. The stdout files are regenerated on demand by running the probes via the `tee` command recorded in each row. This deviation is recorded here and in the commit body; no other deviation occurred.

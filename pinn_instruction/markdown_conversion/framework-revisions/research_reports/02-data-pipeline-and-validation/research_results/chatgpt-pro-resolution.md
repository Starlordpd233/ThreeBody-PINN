# Resolution Document — Issue 02 Data Pipeline and Validation

**Date:** 2026-06-10

**Input inventory received:** `README.md`, `framed-research-questions.md`, `claims-table.md`, `consolidated-context.md`, `ERRATUM-2026-06-10.md`, `02-data-pipeline-and-validation.md`, `ctl_instruction(10).md`, `pinn_architecture(10).md`, `sampling_method(1).md`, `data_quality_assessment.md`. Manifest mismatch noted: `README.md` lists `DELIVERY-NOTE.md`, but no `DELIVERY-NOTE.md` file was received in the uploaded package.

---

## §0 Scope and decision standard

### §0.1 Scope covered

This document answers every in-scope question listed in `framed-research-questions.md`:

- Cluster A: Q-A1 through Q-A6.
- Cluster B: Q-B1 through Q-B4.
- Cluster C: Q-C1 through Q-C4.

It does not answer the topics explicitly deferred to doc-03: M16 `dt_out` collocation-density scaling, G6 causal-training Option A vs Option B, and training-loop usage of SCS/SASD/IPR/PSC. Those are referenced only where needed to preserve boundaries. Evidence: `framed-research-questions.md` §Doc-03 Scope Boundary and §Research Questions.

### §0.2 Source authority standard

I applied the following authority ordering.

1. **Hard constraints are fixed.** The locked v1.4 conventions in `framed-research-questions.md` are treated as boundary conditions, especially the 14D input contract, Jacobi `IC13`, COM projection head, dual-epsilon contract, post-v1.3 SCS gate, and raw-mass `D = (G T^2)^{1/3}` convention. Evidence: `framed-research-questions.md` §Hard Constraints.
2. **Framework specs are the editable source of truth.** `ctl_instruction(10).md` and `pinn_architecture(10).md` are the relevant spec-edit targets. Evidence: `README.md` §Source-Treatment Preamble and §Per-File Manifest.
3. **The issue doc is non-authoritative.** `02-data-pipeline-and-validation.md` is an adjudication subject; its findings and recommended resolutions are candidate positions only. Evidence: `README.md` §Source-Treatment Preamble; `framed-research-questions.md` §Source-Treatment Framing.
4. **Claims discipline.** `claims-table.md` controls the status of dataset figures. `verified` CLM rows are treated as package-grounded unless superseded by the erratum; `claimed-unverified` rows are not used as established facts. Evidence: `claims-table.md` §Claims Table and §Row Notes.
5. **Erratum handling.** `ERRATUM-2026-06-10.md` is not in the manifest, but it was provided with the package and directly corrects two package statements. I used it as an interim correction source, while recording the absence of the Phase 24 DATA-07 addendum as an open item. Evidence: `ERRATUM-2026-06-10.md` §Scope, §Correction 1, §Correction 2, and §Not affected.
6. **No repository assumptions.** I did not assume access to live `pinn/` code, runner scripts, or the dataset beyond the uploaded package. Where current implementation status or empirical prevalence requires unavailable repository or disk evidence, it is recorded in the Open Items Register.

### §0.3 Decision standard

A recommendation is marked **High confidence** only when it follows from a hard constraint, a framework spec, a verified/superseded package fact, or first-principles compatibility with those sources. It is marked **Medium confidence** when the contract is well-supported but the exact threshold or empirical prevalence still needs dataset verification. It is marked **Low confidence** when the package lacks enough evidence to select a specific policy, even if it supports a safe stop-gap interface.

No external literature was used. All conclusions are based on the package and first-principles reasoning about the specified data contracts.

---

## §1 Executive decision summary

1. **Q-A1 — Stage 4 → Stage 5 gate:** Add a mandatory training-admission gate after metrics and before training. Enforce structural completeness with finite parseability, monotonically increasing times, `final_timestep >= 9.5`, and at least two complete snapshots. Do **not** enforce the issue doc’s variant-independent `snapshot_count >= 200`; it would reject known low-resolution variants and conflicts with the package warning not to hard-code snapshot counts. Use snapshot count and gap diagnostics, then rely on SASD/IPR for undersampling quality.

2. **Q-A2 — Non-contiguous IDs:** Use an explicit `TrajectoryIndex` keyed by `(family, fidelity, numeric_id)` and built by scanning actual folders. Never derive an ID from array position. Gold status must be inferred from the folder, not from a `_gold_` filename infix, per the erratum.

3. **Q-A3 — Blacklist:** Load the blacklist at data-load time, normalize IDs to the same key schema, exclude blacklisted IDs before sampling, persist a rejection manifest, and fail closed if the blacklist file is missing or malformed except under an explicit development override. Do not hard-code the claimed count `CLM-03`.

4. **Q-A4 — Missing standard-gold counterparts:** The package does not justify choosing either “skip to Stage 6” or “low-fidelity fallback inside Stage 5.” Treat this as a Phase-26 STOP-gap. Data-side contract: Stage 5 high-resolution standard membership requires an actual gold counterpart; IDs without one are marked `missing_gold_counterpart` and are not silently substituted.

5. **Q-A5 — Footer heterogeneity:** Footers are metadata, not completeness signals. If a full `Result:` footer is present, parse its fields with `direct_footer` provenance. If no footer is present, infer `tol` and `dt_out` from folder defaults in `CLM-09` and record `inferred_folder_default`. The erratum supersedes the package’s “partial/minimal footer” characterization: the affected files have no `Result:` footer and no parameter fields.

6. **Q-A6 — Processed format:** Make HDF5 the primary processed training-data format. Allow `.npy`/`.npz` only as schema-equivalent array shards or intermediates. Permit JSON/text exports for inspection only, not as the canonical training store. This is a storage/IO decision, not a methodology change, provided the same arrays and metadata are preserved.

7. **Q-B1 — Points per trajectory:** Replace fixed 32-without-qualification by an adaptive data-snapshot rule: for a trajectory with `n_snapshots >= 2`, use `n_pts = min(32, n_snapshots, max(2, floor(0.5*n_snapshots)))` for supervised data samples without replacement. This handles low-resolution trajectories without entering the out-of-scope collocation-density question.

8. **Q-B2 — Mass drift:** Require a mass-consistency audit between IC files and Brutus `t=0` snapshots using raw-order masses, `rtol=1e-15`, `atol=0`, and Decimal fallback for diagnosis. Production should run the full mass scan because only three scalars per trajectory are involved; a stratified 1000-pair probe is acceptable only as an interim audit. If true mismatch exceeds tolerance, reject or manually review; do not silently replace canonical IC masses with Brutus masses.

9. **Q-B3 — Precision:** `float64` is sufficient for default validation metrics and admission decisions because the decision thresholds are many orders above float64 roundoff. Exact/Decimal parsing is required for mass-consistency diagnosis and optional boundary-case audits, not for full trajectory arrays.

10. **Q-B4 — Global scale:** Use locked raw-mass `D = (G T^2)^{1/3} ≈ 4.6416` with `G=1`, `T=10`. Do not adopt the issue doc’s `D = 6.694`. Adopting `6.694` would require a mass-fraction convention rewrite touching residuals, Hamiltonian, angular momentum, COM, invariants, scaling, and tests.

11. **Q-C1 — SCS:** Use the locked post-v1.3 definition: raw drift `epsilon_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(epsilon_H)`, reject if `SCS > -5` equivalently `epsilon_H > 1e-5`. The issue doc’s `1e-6` and `1e-8` figures are raw-ratio quality bands, not the locked reject gate.

12. **Q-C2 — SASD:** Define data-side SASD on scaled, normalized-time trajectories as `SASD_{k,b} = Δu_k ||a'_b(u_k)|| / max(||v'_b(u_k)||, v_floor)` and trajectory score `max_{k,b} SASD_{k,b}`. Use validation epsilon `1e-10` in acceleration. Flag `max SASD > 0.5` as `resample_required` / not clean-training-ready.

13. **Q-C3 — IPR:** Define data-side IPR using a cubic Hermite spline in normalized time and validation force with static `epsilon_val = 1e-10`, not training `epsilon_train = 1e-5`. Use 10 interior points per interval by default. Flag `IPR > 1e-3` as aliased/resample-required. A separate training-epsilon diagnostic may be computed later, but it is doc-03/training-loop adjacent.

14. **Q-C4 — PSC:** Define PSC as a dataset-level diagnostic entropy over a fixed, documented phase-space projection. Recommended default: six log-scaled pairwise features `[log r_(1), log r_(2), log r_(3), log v_(1), log v_(2), log v_(3)]`, with sorted pairwise separations and relative speeds, robust quantile bin edges, hashed occupancy counts, and Miller-Madow-corrected Shannon entropy. Do not make PSC a per-trajectory rejection gate in this issue.

---

## §2 Decision matrix

| Question ID | One-line verdict | Confidence |
|---|---|---|
| Q-A1 | Add a post-metrics training-admission gate; require parseability, monotonic finite times, `final_timestep >= 9.5`, and at least two snapshots; reject the fixed `>=200` snapshot floor. | High |
| Q-A2 | Implement folder-scanned `TrajectoryIndex` keyed by `(family, fidelity, numeric_id)`; never use dense array index as ID. | High |
| Q-A3 | Load and enforce blacklist at data-load time, exclude before sampling, persist rejection counts, and fail closed on missing/malformed blacklist. | High |
| Q-A4 | Treat missing standard-gold fallback as a STOP-gap; do not silently substitute low-fidelity data into Stage 5. | Medium for no silent substitution; Low for choosing a stage fallback |
| Q-A5 | Treat footers as optional metadata; parse full footers directly, otherwise infer folder defaults with explicit provenance. | High |
| Q-A6 | Use HDF5 as canonical processed training store; allow `.npy`/`.npz` schema-equivalent arrays; JSON/text inspection-only. | High |
| Q-B1 | Use adaptive supervised point count `min(32, n_snapshots, max(2, floor(0.5*n_snapshots)))`; no fixed 32 assumption without cap. | Medium |
| Q-B2 | Run mass-consistency audit with `rtol=1e-15`, `atol=0`; full scan preferred; Decimal only for diagnosis/fallback. | Medium |
| Q-B3 | Use `float64` for validation metrics; reserve Decimal/exact parsing for mass audits and boundary diagnostics. | High |
| Q-B4 | Use locked raw-mass `D≈4.6416`; `D=6.694` is rejected unless a future mass-fraction rewrite is opened. | High |
| Q-C1 | Use locked log-drift SCS gate: `SCS=log10(epsilon_H)`, reject `SCS>-5`; issue raw-ratio thresholds are not the reject gate. | High |
| Q-C2 | Use normalized-time SASD with validation acceleration and flag `max SASD>0.5` for resampling/not-clean-training. | Medium |
| Q-C3 | Use validation epsilon `1e-10` for data-side IPR; flag `IPR>1e-3` as aliased/resample-required. | Medium |
| Q-C4 | Use fixed projected phase-space entropy with robust bins and Miller-Madow correction as dataset diagnostic only. | Medium-Low |

---

## §3 Cluster A — Ingestion & Selection

### §3.1 Q-A1 (B-06) — Stage 4 → Stage 5 validation gate

#### Verdict / recommendation

A completeness and validity gate must sit after metric generation and before any training batch construction. The gate should be implemented as a trajectory-level admission classifier with these exact structural conditions:

```text
A trajectory is structurally admissible only if:
1. the Brutus file parses into complete snapshot blocks;
2. every snapshot has exactly 3 body rows and each body row has finite mass, position, and velocity values;
3. times are finite and strictly increasing;
4. n_snapshots >= 2;
5. final_timestep >= 9.5;
6. the trajectory has not been excluded by blacklist, missing-gold membership rules, or metric-quality gates defined in Q-C1 through Q-C3.
```

Do **not** adopt the issue doc’s fixed `snapshot_count >= 200` for Stage 4+ as a completeness gate. A fixed `>=200` threshold is not variant-safe because the package states low-resolution standard trajectories are approximately 59 snapshots and hierarchical base trajectories approximately 125 snapshots (`CLM-10`, claimed-unverified). It also conflicts with the dataset-documentation warning in `consolidated-context.md` that exact snapshot counts should not be hard-coded.

Use snapshot counts as diagnostics and for adaptive point sampling (Q-B1), not as a high fixed completeness threshold. If a stronger interior-gap check is desired, add it as a diagnostic first:

```text
record n_snapshots, median_delta_t, max_delta_t, p95_delta_t, final_timestep, inferred_dt_out
```

but do not reject on those diagnostics until the Phase 24 snapshot distribution is available.

#### Reasoning

The package establishes that the metrics-calculation script processes all available Brutus output files and does not perform the `final_timestep >= 9.5` completeness check; completeness is therefore the responsibility of downstream consumers. A training pipeline cannot safely treat a metric file as evidence of an admissible trajectory unless the trajectory file has been revalidated at training ingestion.

The final-timestep condition is grounded. By contrast, the proposed `>=200` snapshot threshold is not grounded: it would reject the approximate standard and hierarchical base populations even when they are complete for their `dt_out` variants. More importantly, undersampling is a physics-quality issue better measured by SASD and IPR than by a single global line count. A low-resolution file can be complete but coarse; a high-resolution file can have many lines but still contain a local gap. Completeness and sampling adequacy should therefore be separated.

#### Evidence

- `framed-research-questions.md` Q-A1 states the issue-doc claim and notes that `final_timestep >= 9.5` is grounded while the prevalence and snapshot distributions are not (`CLM-10`, `CLM-11`).
- `consolidated-context.md` §Completeness Checks states the primary check as `final_timestep >= 9.5` and says not to rely on a specific footer schema or line-count thresholds.
- `consolidated-context.md` §metrics_calculation provenance states that `calculate_metrics.py` processes all files and does not perform completeness checks.
- `claims-table.md` rows `CLM-10` and `CLM-11` mark approximate snapshot counts and gate prevalence as claimed-unverified.

#### Confidence

**High** for requiring a post-metrics gate and rejecting the fixed `>=200` floor. The most important factor that could change details is the Phase 24 `DATA-06` distribution of actual final timesteps, snapshot counts, and interior time gaps.

#### Verification suggestion

Run an ingestion audit over all four Brutus folders. For every trajectory, compute parse status, `n_snapshots`, `final_timestep`, monotonicity, finite-value status, and gap diagnostics. Confirm that trajectories with `final_timestep < 9.5` are rejected and that complete standard/hierarchical base trajectories are not rejected solely because they have fewer than 200 snapshots.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 after item 3 or item 6:

```markdown
#### Training-admission structural gate

After metrics are produced and before any trajectory can be exposed to the training DataLoader, every Brutus trajectory MUST pass a structural admission gate. A structurally admissible trajectory parses into complete N=3 snapshot blocks, has finite mass/position/velocity/time values, has strictly increasing times, has at least two complete snapshots, and satisfies `final_timestep >= 9.5`. Missing or absent `Result:` footers are not a completeness failure. Fixed global line-count or snapshot-count thresholds such as `snapshot_count >= 200` MUST NOT be used as completeness gates; snapshot counts and time-gap summaries are recorded as diagnostics and consumed by adaptive sampling and metric-quality checks.
```

---

### §3.2 Q-A2 (B-11) — Non-contiguous IDs (ID ≠ array index)

#### Verdict / recommendation

The correct ID mapping contract is an explicit filesystem-derived index. Define the primary key as:

```text
TrajectoryKey = (family, fidelity, numeric_id)
family ∈ {hierarchical, standard}
fidelity ∈ {base, gold}
numeric_id ∈ integer parsed from the four-digit suffix
```

The DataLoader must build:

```text
trajectory_index: dict[TrajectoryKey, TrajectoryRecord]
id_sets_by_variant: dict[(family, fidelity), set[int]]
```

by scanning actual directories. It must not use an array row number as a trajectory ID. A dense array index may exist only as an internal storage index and must be mapped through `TrajectoryKey`.

File parsing must use the folder as the authoritative variant/fidelity signal. Per the erratum, gold-standard Brutus output filenames do **not** carry a `_gold_` infix; all four Brutus output folders use the base filename prefixes. Therefore gold status is encoded only by folder name. The numeric ID mapping remains unchanged.

Required lookup behavior:

```text
get_by_key(family, fidelity, numeric_id) -> TrajectoryRecord or MissingTrajectoryError
has_gold_counterpart(family, numeric_id) -> bool
base_to_gold_join(family, numeric_id) -> pair only if both exact keys exist
```

#### Reasoning

The precise claimed gap magnitudes (`CLM-01`, `CLM-02`) are not verified, but the mapping contract does not depend on their exact values. Even a single missing ID breaks `ID == array index`. The package states that gaps are intentional and caused by continuation, prescreen rejection, and failed Brutus runs. Therefore the only robust contract is to scan actual files, parse numeric IDs, and treat IDs as sparse labels rather than dense positions.

The erratum is material because the uncorrected consolidated-context file says gold status appears in both folder and filename. That is wrong for Brutus outputs. A parser that expects `brutus_standard_gold_XXXX.txt` or `brutus_hierarchical_gold_XXXX.txt` would miss the verified gold folders.

#### Evidence

- `framed-research-questions.md` Q-A2 poses the non-contiguous-ID mapping question and marks `CLM-01`, `CLM-02`, and `CLM-12` as relevant but unverified.
- `consolidated-context.md` §File Naming Conventions states numeric-ID mapping and intentional non-contiguous IDs, but its gold filename narrative is superseded.
- `ERRATUM-2026-06-10.md` §Correction 1 states that no gold-standard Brutus output file carries a `_gold_` infix and that folder name is the gold-status authority.
- `claims-table.md` rows `CLM-01`, `CLM-02`, and `CLM-12` mark gap and nominal-count figures as claimed-unverified.

#### Confidence

**High.** The main factor that could change implementation details is the actual directory/file naming recovered in Phase 24, but it would not justify returning to dense indexing.

#### Verification suggestion

Scan all Brutus output directories and build the `TrajectoryKey` set. Unit-test 20 known IDs, including at least five missing IDs, five present base IDs, five present gold IDs, and five IDs with base/gold asymmetry. Assert that no batch constructor can request a trajectory by array position alone.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 after metadata inference:

```markdown
#### Sparse trajectory identity contract

Trajectory IDs are sparse dataset labels, not dense array indices. The DataLoader MUST construct a `TrajectoryIndex` by scanning the actual Brutus output folders and parsing the numeric suffix from each filename. The primary key is `(family, fidelity, numeric_id)`, where `family ∈ {hierarchical, standard}` and `fidelity ∈ {base, gold}` are determined from the containing folder. The folder is authoritative for gold-standard status. No code path may infer `numeric_id` from array position or assume that IDs are contiguous.
```

---

### §3.3 Q-A3 (M11) — Blacklist loading / consumption

#### Verdict / recommendation

Blacklist consumption is mandatory at data-load time. The pipeline must:

```text
1. Load the blacklist JSON before constructing the admissible trajectory set.
2. Validate schema: top-level keys must include `hierarchical` and `standard`, each mapping to a list of integer-like IDs.
3. Normalize IDs to integers and deduplicate within each family.
4. Apply a blacklisted family/ID to every fidelity of that family: base and gold are both excluded if present.
5. Exclude blacklisted trajectories before stage assignment, sampling, or metric aggregation for training admission.
6. Persist a rejection manifest with counts by family and fidelity.
7. Fail closed on missing, malformed, or unreadable blacklist files unless an explicit development-only override is set and recorded.
8. Raise an error if a blacklisted key is requested in any batch.
```

The pipeline must not hard-code the claimed size `CLM-03`. It should report the loaded count and compare it to package expectations only as a verification diagnostic.

#### Reasoning

A blacklist is a data-quality exclusion list. If it is not enforced at the training ingestion boundary, downstream stages can silently train on known problematic ICs. Since the count and current consumption status are unverified, the contract should be independent of the claimed count: load whatever IDs the blacklist file contains, validate its schema, and persist the actual exclusions. Because gold and base runs for a family/ID share the same physical IC, exclusion should apply across fidelities.

#### Evidence

- `framed-research-questions.md` Q-A3 poses the required blacklist-consumption contract and notes that count (`CLM-03`) and loading/consumption status are separate questions.
- `consolidated-context.md` §Blacklist Summary describes the JSON keys and the claimed count while preserving the `claimed-unverified` status.
- `claims-table.md` row note `CLM-03` states that Phase 24 owns both count/composition verification and loading/consumption status.

#### Confidence

**High** for mandatory consumption and fail-closed behavior. The most important factor that could change only the counts, not the contract, is Phase 24 verification of the actual blacklist JSON.

#### Verification suggestion

Create a test blacklist containing one present hierarchical ID, one present standard ID, one absent ID, and one duplicate ID. Assert that present blacklisted base/gold trajectories are excluded, absent IDs are logged but not fatal, duplicates are deduplicated, and a batch request for a blacklisted trajectory raises an error.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 or add a DataLoader subsection:

```markdown
#### Blacklist consumption

The DataLoader MUST load `problematic_ics_blacklist.json` before constructing the admissible trajectory set. The blacklist schema is `{"hierarchical": [...], "standard": [...]}`. IDs are normalized to integers and applied across all fidelities for the corresponding family. Blacklisted trajectories are excluded before stage assignment and before sampling. The DataLoader persists a rejection manifest with loaded blacklist counts and excluded trajectory keys. Missing or malformed blacklist input is a fail-closed error for production training.
```

---

### §3.4 Q-A4 (M13) — 184 standard IDs without a gold counterpart

#### Verdict / recommendation

The package is insufficient to select either proposed training-stage fallback. The correct resolution is a STOP-gap on stage semantics, plus a precise data-side contract:

```text
1. Stage 5 high-resolution standard membership requires an actual standard-gold trajectory key.
2. If a standard base ID has no standard-gold counterpart, mark it `missing_gold_counterpart`.
3. Do not silently substitute the base-fidelity trajectory into a high-resolution/gold slot.
4. Do not decide inside this issue whether such IDs skip to Stage 6, remain in earlier/base-fidelity stages, or enter Stage 5 with an explicit low-fidelity override. That policy requires downstream curriculum/stage adjudication.
```

The verified `CLM-04` count may be cited as the package-grounded missing-gold count, subject to Phase 24 re-verification.

#### Reasoning

The two candidate fallbacks have different methodological meanings. “Skip to Stage 6” changes curriculum semantics; “low-fidelity fallback inside Stage 5” changes fidelity semantics. The framework specs are silent, and the framed question itself annotates this as a Phase-26 STOP-gap candidate if the resolution doc and dataset are silent or conflicting. The safe data-side decision is therefore to expose the missing counterpart deterministically and prevent silent substitution. The training-stage owner can then decide how to consume the flag.

#### Evidence

- `framed-research-questions.md` Q-A4 states the two candidate fallbacks and explicitly marks the issue as a STOP-gap candidate if the package does not settle it.
- `claims-table.md` row `CLM-04` marks 184 standard IDs without gold counterpart as verified; `CLM-05` marks the related 2,749 base vs 2,565 gold folder counts as verified.
- `consolidated-context.md` §standard_quasi_random_ids_not_in_gold.md provides the missing-ID list and states all gold-standard ICs are a byte-identical subset of standard ICs.

#### Confidence

**Medium** for the no-silent-substitution contract; **Low** for any specific fallback choice. The most important factor that would change this answer is an authoritative curriculum-stage specification defining whether Stage 5 may contain flagged low-fidelity fallback samples.

#### Verification suggestion

Construct `base_ids`, `gold_ids`, and `missing_gold_ids = base_ids - gold_ids` for the standard family. Assert that every `missing_gold_id` is excluded from the Stage 5 high-resolution standard set and appears in the data manifest with `missing_gold_counterpart=true`.

#### Proposed specification text

Modify `ctl_instruction(10).md` stage-assignment or DataLoader metadata section:

```markdown
#### Gold counterpart membership

A trajectory may be assigned to a high-resolution/gold data slot only if the corresponding `(family, gold, numeric_id)` key exists in the `TrajectoryIndex`. Base-fidelity trajectories MUST NOT be silently substituted for missing gold counterparts. When a base trajectory lacks a gold counterpart, the DataLoader records `missing_gold_counterpart=true` and exposes the trajectory only under its actual fidelity. The curriculum policy for consuming this flag is deferred to the curriculum/training-loop specification.
```

---

### §3.5 Q-A5 (D7) — Footer / parameter heterogeneity

#### Verdict / recommendation

Footer handling must be tolerant and provenance-aware. The correct contract is field-level metadata provenance:

```text
footer_present: true | false
footer_schema: full | absent | unrecognized
metadata fields: tol, Lw, dt_out, t_end, eta, energy_fields, t_cpu
field_source[field]: direct_footer | inferred_folder_default | derived_from_times | unavailable
```

Rules:

1. Parse snapshot blocks independently of the footer.
2. If a full `Result:` footer is present and fields parse, use the footer values with `direct_footer` provenance.
3. If no `Result:` footer is present, infer `tol` and `dt_out` from the folder defaults in `CLM-09` and record `inferred_folder_default`.
4. Do not fail a trajectory solely because the footer is absent.
5. Do not use footer presence as a completeness signal; use the structural gate in Q-A1.
6. For `dt_out`, also compute `derived_dt_out = median(diff(times))` and compare it to the direct or inferred value as a diagnostic, not as the primary variant label.

Folder defaults for fields covered by `CLM-09`:

| Family/fidelity | Default `tol` | Default `dt_out` |
|---|---:|---:|
| Standard base | `1e-13` | `0.17` |
| Hierarchical base | `1e-15` | `0.08` |
| Gold standard, both families | `1e-13` | `0.01` |

The erratum supersedes the package’s “partial/minimal footer” wording. The affected 1,550 hierarchical base files, 701 standard base files, and 219 standard gold files have no `Result:` footer and no parameter fields anywhere in the file. Full-schema footers, when present, include `eta` and `tol`.

#### Reasoning

Footers are useful metadata but are not necessary to parse the trajectory. The package’s corrected disk fact says some files have no footer at all, so a parser that requires `Result:` will incorrectly reject valid snapshot data. Conversely, when a footer exists, direct values are more specific than folder defaults and should be retained. The only safe approach is field-level provenance.

The `CLM-09` folder defaults are verified and re-affirmed by the erratum as not affected. Therefore they are appropriate fallbacks for `tol` and `dt_out`. The package is less explicit for `Lw` defaults in missing-footer files, so `Lw` should be inferred only if an authoritative folder default is separately supplied; otherwise mark `Lw` as `unavailable` or `inferred_folder_default` with lower confidence.

#### Evidence

- `framed-research-questions.md` Q-A5 poses the footer/default/provenance question.
- `claims-table.md` rows `CLM-07`, `CLM-08`, and `CLM-09` record the 219 count, 592 `tol=1e-14` count, and verified folder-default `tol`/`dt_out` values.
- `consolidated-context.md` §Brutus Parameters by Variant lists observed parameter distributions and folder defaults, but its partial-footer characterization is superseded.
- `ERRATUM-2026-06-10.md` §Correction 2 states that the affected populations have no `Result:` footer or parameter fields; §Not affected re-verifies `CLM-09`, `CLM-05`, `CLM-06`, `CLM-07`, and `CLM-08` counts and all full-schema footer tuples.

#### Confidence

**High** for footer optionality, folder-default `tol`/`dt_out`, and provenance flags. The most important factor that could change minor details is the authoritative DATA-07 correction addendum, especially if it supplies explicit `Lw` defaults for missing-footer files.

#### Verification suggestion

Run a footer scanner across all Brutus files. For each file, classify `footer_present`, parse direct fields where present, infer defaults where absent, and assert that no file is rejected solely for missing footer. Cross-tabulate `tol_source` and `dt_out_source` by folder and compare counts with the erratum.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 item 3 and metadata bundle:

```markdown
`Result:` footers are optional metadata. The parser MUST parse snapshot blocks without requiring a footer. When a full footer is present, parse `tol`, `Lw`, `dt_out`, `t_end`, `eta`, and energy fields with `direct_footer` provenance. When a footer is absent, infer `tol` and `dt_out` from the containing folder defaults and mark those fields `inferred_folder_default`. Footer absence is not a completeness failure. The DataLoader MUST persist per-field metadata provenance.
```

---

### §3.6 Q-A6 (D-03) — Processed training-data format

#### Verdict / recommendation

Use HDF5 as the canonical processed training-data store. Allow `.npy` or `.npz` only as schema-equivalent array shards or intermediate artifacts when a manifest preserves the same metadata and indexing. Allow JSON/text exports only for inspection, debugging, or small audit reports; they must not be the training source of truth.

Minimum canonical HDF5 contents:

```text
/index/trajectory_keys
/index/rejection_manifest
/trajectories/<family>/<fidelity>/<id>/times_u
/trajectories/<family>/<fidelity>/<id>/tau
/trajectories/<family>/<fidelity>/<id>/r_true_prime_ordered_gauge
/trajectories/<family>/<fidelity>/<id>/v_true_prime_ordered_gauge
/trajectories/<family>/<fidelity>/<id>/masses_raw_ordered
/trajectories/<family>/<fidelity>/<id>/IC13
/trajectories/<family>/<fidelity>/<id>/metadata
/metrics/<family>/<fidelity>/<id>/SCS, SASD, IPR, PSC_inputs
```

This decision has no methodology consequence if the same tensors, metadata, keys, and rejection manifests are preserved. It is a storage and IO decision.

#### Reasoning

The framework spec already recommends HDF5 or NumPy files to avoid repeated text parsing and accelerate training. HDF5 is the better primary store because the data are hierarchical: trajectories, variants, metrics, metadata, and rejection manifests naturally share one indexed container. JSON/text is useful for auditability but would make the training path parse-heavy and schema-fragile. Methodologically, the neural network, losses, and validation gates do not depend on the storage container; they depend on the arrays and metadata.

#### Evidence

- `framed-research-questions.md` Q-A6 states the storage-format question and notes the framework-spec position.
- `ctl_instruction(10).md` Step 1 item 6 recommends saving parsed objects into efficient formats like HDF5 or NumPy `.npy` files to avoid repeated text parsing and accelerate training.
- `02-data-pipeline-and-validation.md` §File Format and §Open Decisions discuss HDF5 vs text/JSON, but the issue doc is non-authoritative.

#### Confidence

**High.** The most important factor that could change the primary format is a hard infrastructure constraint forbidding HDF5, which is not present in the package.

#### Verification suggestion

Round-trip five trajectories through HDF5 and a `.npy`/manifest alternative. Assert byte- or tolerance-equivalence of arrays, exact equality of keys and metadata fields, and successful reconstruction of the same admissible trajectory set.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 item 6:

```markdown
The canonical processed training-data store SHOULD be HDF5, with a documented schema containing trajectory arrays, `TrajectoryKey` indices, metadata provenance, validation metrics, and rejection manifests. NumPy `.npy`/`.npz` shards are acceptable only when accompanied by a schema manifest that preserves the same information. JSON or text exports MAY be produced for human inspection and debugging, but they are not the canonical training input format.
```

---

## §4 Cluster B — Sampling, Precision & Global Scale

### §4.1 Q-B1 (M12) — Points-per-trajectory feasibility

#### Verdict / recommendation

Use an adaptive supervised data-snapshot count. For each structurally admissible trajectory:

```python
if n_snapshots < 2:
    reject_structural()
else:
    n_pts = min(32, n_snapshots, max(2, floor(0.5 * n_snapshots)))
```

Sampling should be without replacement for the supervised data loss. For odd `n_pts`, split the CTL 50/50 uniform-vs-acceleration-weighted rule as:

```text
n_uniform = ceil(n_pts / 2)
n_weighted = n_pts - n_uniform
```

This recommendation is limited to supervised data snapshots per trajectory. It does not allocate supplemental collocation points across `dt_out` variants; that topic is M16 and is explicitly out of scope.

#### Reasoning

A fixed target of 32 can be feasible for many low-resolution standard trajectories if `CLM-10` is approximately right (`32 < ~59`), so the issue doc’s statement that standard trajectories “cannot support” 32 is overstated. However, the fixed 32 assumption is still brittle: actual counts are unverified, line counts must not be hard-coded, and trajectories near the structural minimum cannot support 32 without replacement. The adaptive rule preserves the existing target where data density supports it, while preventing a single batch from consuming an excessive fraction of a sparse trajectory.

The `0.5*n_snapshots` cap is a reasonable conservative sampling-ratio limit and matches the issue-doc candidate for standard low-resolution trajectories, but it should be applied dynamically to actual parsed counts rather than to approximate CLM values.

#### Evidence

- `framed-research-questions.md` Q-B1 asks whether fixed 32, an adaptive cap, or another rule is feasible and notes that M16 collocation scaling is out of scope.
- `ctl_instruction(10).md` §Mini-Batch Construction states an example of 32 time points per trajectory with 50% uniform and 50% acceleration-weighted sampling.
- `claims-table.md` `CLM-10` marks approximate snapshot counts as claimed-unverified and warns against hard-coding.
- `consolidated-context.md` §Snapshot count warning explains why exact snapshot counts should not be hard-coded.

#### Confidence

**Medium.** The most important factor that could change the cap is the empirical distribution of `n_snapshots` and per-trajectory training stability after Phase 24/Phase 27 audits.

#### Verification suggestion

Compute `n_pts` for every trajectory from actual parsed `n_snapshots`. Produce histograms by family/fidelity. Confirm no structurally admissible trajectory is sampled with replacement for supervised data and that low-snapshot trajectories are represented with the intended cap.

#### Proposed specification text

Modify `ctl_instruction(10).md` §Mini-Batch Construction with Lookahead Sampling:

```markdown
The nominal supervised sample count is `n_pts_target = 32` time snapshots per trajectory. The actual count is adaptive: for a structurally admissible trajectory with `n_snapshots >= 2`, set `n_pts = min(n_pts_target, n_snapshots, max(2, floor(0.5*n_snapshots)))`. Supervised data snapshots are sampled without replacement. This rule concerns data snapshots only and does not define supplemental collocation density across `dt_out` variants.
```

---

### §4.2 Q-B2 — Footer / mass-drift protocol

#### Verdict / recommendation

Require a mass-consistency audit between IC masses and Brutus `t=0` masses. The production rule should be a full scan, not merely a sample, because only three mass scalars per trajectory are involved.

Exact protocol:

```text
For each matched IC-Brutus trajectory pair:
1. Parse the three IC masses in raw input order.
2. Parse the three Brutus masses from the first complete snapshot at t=0 or the earliest snapshot if t=0 is represented within numerical timestamp tolerance.
3. Compare raw-order masses before canonical body reordering.
4. First pass may use float64 with `np.isclose(m_ic, m_brutus, rtol=1e-15, atol=0.0)`.
5. If any pair fails, reparse the failing mass strings with `decimal.Decimal` and recompute the relative difference.
6. If Decimal diagnosis shows the difference is within `1e-15` relative tolerance, classify as text/float parsing noise and keep IC masses canonical.
7. If the difference exceeds `1e-15`, mark the trajectory `mass_mismatch` and exclude from clean training pending manual review or resimulation.
```

A stratified `min(1000, N)` probe is acceptable only as an interim audit before full preprocessing. If used, it must be stratified by family, fidelity, and footer-provenance class.

#### Reasoning

The IC file is the canonical source for the initial-condition vector and raw mass channels. The Brutus output should preserve masses, but text formatting and arbitrary-precision output can introduce apparent discrepancies. Therefore the pipeline needs a deterministic audit, not a silent choice of one source. `np.allclose` must not be used with its default absolute tolerance, because the default `atol=1e-08` is far too loose for a `1e-15` mass-conservation check. Decimal parsing is useful to distinguish binary floating parse artifacts from actual text-level differences, but it does not justify accepting a true mass mismatch.

#### Evidence

- `framed-research-questions.md` Q-B2 poses the `np.allclose(rtol=1e-15)` and Decimal fallback protocol.
- `02-data-pipeline-and-validation.md` §Footer/Mass Drift Protocol proposes comparing about 1000 IC-Brutus pairs, but this source is non-authoritative.
- `ctl_instruction(10).md` §Network input contract states that mass entries are ordered raw masses before normalization.
- `ctl_instruction(10).md` Step 2 metadata bundle stores ordered raw masses and the final `IC13`.

#### Confidence

**Medium.** The most important factor that could change the fallback behavior is an empirical full mass-drift audit showing whether mismatches are absent, formatting-only, or physically meaningful.

#### Verification suggestion

Run the full scan and report: total pairs checked, failures in float64, failures after Decimal diagnosis, maximum relative mass difference by family/fidelity, and example failing file IDs. Confirm that the canonical stored masses equal IC masses for all admitted trajectories.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 2 preprocessing pipeline after “mass-invariance check”:

```markdown
The mass-invariance check compares raw-order IC masses against Brutus first-snapshot masses before canonical reordering. The production audit scans all matched IC-Brutus pairs. The float64 comparison uses `rtol=1e-15` and `atol=0.0`; failures are re-diagnosed with `decimal.Decimal` parsing of the original mass strings. IC masses remain canonical for `IC13`. A trajectory whose Brutus first-snapshot masses differ from IC masses by more than `1e-15` relative tolerance is excluded from clean training pending manual review.
```

---

### §4.3 Q-B3 — Precision handling

#### Verdict / recommendation

Use `float64` for the default validation metrics over trajectory arrays. Use exact or Decimal parsing only for:

```text
1. mass-consistency audits (Q-B2);
2. metadata parsing where exact text provenance matters;
3. boundary-case recomputation when a metric falls within a configured audit band of a threshold.
```

Recommended boundary audit bands:

```text
SCS:       |SCS - (-5)| <= 0.05 decades, or epsilon_H within about 12% of 1e-5
SASD:      |max_SASD - 0.5| <= 0.01
IPR:       relative distance to 1e-3 <= 0.05
```

For SCS, if `H(0)` is zero or numerically near zero, do not force a denominator floor into the locked SCS formula. Mark the trajectory `SCS_undefined_near_zero_H0` for manual review or resimulation.

#### Reasoning

The validation decision thresholds are far above float64 roundoff. The SCS reject threshold is `epsilon_H > 1e-5`; SASD and IPR thresholds are also macroscopic relative to binary64 precision. Even for Brutus tolerances around `1e-13` to `1e-15`, float64 is adequate for deciding the specified gates, provided computations are stable and boundary cases are flagged. Exact arithmetic over full trajectory arrays would be slow, would not match the training arrays, and is unnecessary for the stated gates. Masses are the exception because they are only three scalars per trajectory and directly define the network input contract.

#### Evidence

- `framed-research-questions.md` Q-B3 poses float64 sufficiency and Decimal-for-masses.
- `claims-table.md` row `CLM-09` gives verified default tolerances: standard `1e-13`, hierarchical base `1e-15`, gold `1e-13`.
- `pinn_architecture(10).md` §Physics Residual and §Energy Conservation specify float-valued scaled residuals and Hamiltonian calculations.
- `data_quality_assessment.md` §SCS defines behavior when `H(0)` is zero or numerically near zero.

#### Confidence

**High** for using float64 on default metrics; **Medium** for the exact audit-band widths. The most important factor that could change details is a Phase 24/27 comparison showing threshold classification changes under extended precision.

#### Verification suggestion

Select trajectories near each threshold and recompute SCS/SASD/IPR in an extended-precision or compensated implementation. Confirm classification stability outside the proposed audit bands and tune the bands if needed.

#### Proposed specification text

Modify `ctl_instruction(10).md` Step 1 or validation subsection:

```markdown
Validation metrics are computed in CPU `float64` over scaled trajectory arrays. Exact/Decimal parsing is not required for full position/velocity arrays. Decimal parsing is reserved for mass-consistency diagnosis and metadata audits. Metric values within documented boundary audit bands of admission thresholds are flagged for optional extended-precision recomputation.
```

---

### §4.4 Q-B4 — Global-scale `compute_globals` / `D = 6.694`

#### Verdict / recommendation

The data pipeline must use the locked raw-mass convention:

```text
T = 10
G = 1
D = (G*T**2)**(1/3) ≈ 4.6416
V = D/T
```

Do **not** adopt the issue doc’s `D = (G*M_tot*T**2)**(1/3) ≈ 6.694` in v1.4. The `6.694` form is correct only under a different mass-fraction convention and would require a global rewrite.

Adopting `D = 6.694` would require, at minimum:

```text
1. redefining mass channels as mass fractions or otherwise introducing M_tot into the dimensionless equations;
2. changing the force residual coefficient in `pinn_architecture.md`;
3. changing Hamiltonian and energy regularizer formulas;
4. changing angular-momentum and COM formulas;
5. changing invariant calculations and stage-assignment scales;
6. changing `IC13` preprocessing and normalization metadata;
7. regenerating acceptance tests and any persisted global scales.
```

Because the hard constraint explicitly rejects this rewrite for v1.4, `compute_globals` must not multiply by `M_tot`.

#### Reasoning

The framework uses raw masses in the dimensionless residual. Substituting `r = D r'` and `t = T u` into Newton’s equations with raw masses forces `D^3 = G T^2`, not `G M_tot T^2`. Introducing `M_tot` in `D` without also dividing masses by `M_tot` changes the dimensionless force coefficient. That would create inconsistency between preprocessing, residuals, Hamiltonian, and conserved quantities.

#### Evidence

- `framed-research-questions.md` Hard Constraint 6 fixes the raw-mass `D` convention and rejects the mass-fraction alternative.
- `ctl_instruction(10).md` §2.5 Global scaling states `D = (G*T**2)^(1/3)`, gives `D ~ 4.6416`, and says the `6.694` alternative is valid only under a mass-fraction rewrite touching every residual, Hamiltonian, angular-momentum, COM, and invariant formula.
- `pinn_architecture(10).md` §Physics Residual states that raw-mass nondimensionalization absorbs `G` and no free dimensionless gravitational coefficient appears.
- `claims-table.md` row `CLM-13` marks `D=6.694` as a contested convention claim, not a dataset count.

#### Confidence

**High.** The only factor that would change the recommendation is an explicit future project decision to reopen PHYS-01 and perform the full mass-fraction rewrite.

#### Verification suggestion

Add a unit test that computes `D` with `T=10`, `G=1` and asserts `D≈4.6416`. Add a residual-scaling test showing that no `M_tot` coefficient appears in the dimensionless acceleration formula when raw masses are used.

#### Proposed specification text

`ctl_instruction(10).md` §2.5 already contains the necessary normative text. Add an implementation note under `compute_globals` if that function is documented:

```markdown
`compute_globals` MUST use the PHYS-01 raw-mass scale `D = (G*T**2)**(1/3)` and MUST NOT multiply by `M_tot`. Any implementation using `D = (G*M_tot*T**2)**(1/3)` is a mass-fraction-convention implementation and is incompatible with v1.4 unless all residual, Hamiltonian, angular-momentum, COM, invariant, and input-normalization formulas are rewritten together.
```

---

## §5 Cluster C — Validation Metrics

### §5.1 Q-C1 (SCS) — Symplectic Conservation Score

#### Verdict / recommendation

Use the locked post-v1.3 SCS definition and gate.

For each trajectory, after preprocessing into the scaled COM/gauge frame, compute validation Hamiltonian with raw masses, `G=1`, and static validation Plummer epsilon:

```math
r_{safe,ij}(t) = \sqrt{\lVert r'_i(t)-r'_j(t)\rVert^2 + \epsilon_{val}^2},
\qquad \epsilon_{val}=10^{-10}.
```

```math
H_{val}(t) = \frac12\sum_{i=1}^3 m_i\lVert v'_i(t)\rVert^2
- \sum_{i<j}\frac{m_i m_j}{r_{safe,ij}(t)}.
```

Then compute:

```math
\epsilon_H = \max_t \left|\frac{H_{val}(t)-H_{val}(0)}{H_{val}(0)}\right|,
\qquad
SCS = \log_{10}(\epsilon_H).
```

Boundary behavior:

```text
if epsilon_H == 0: SCS = -inf
if H_val(0) is zero, non-finite, or numerically near zero: SCS undefined; manual review/resimulation
reject if SCS > -5  (equivalently epsilon_H > 1e-5)
SCS <= -10: excellent
-10 < SCS <= -6: acceptable
-6 < SCS <= -5: marginal; not clean-training-ready without explicit justification
SCS > -5: reject
```

The issue doc’s raw-ratio numbers reconcile as follows:

```text
raw drift 1e-6  -> SCS = -6
raw drift 1e-8  -> SCS = -8
```

They may be recorded as quality bands or stricter optional labels, but they are not the locked reject gate.

#### Reasoning

The hard constraint fixes `SCS` as a logarithmic score. The issue doc uses `SCS` to mean the raw ratio and then compares it to raw-ratio thresholds, creating a category error. The locked definition separates raw drift `epsilon_H` from logarithmic `SCS`, with rejection only above `SCS=-5`. Because validation metrics are data-side checks, they use static validation epsilon `1e-10`, not training `epsilon_train=1e-5`.

#### Evidence

- `framed-research-questions.md` Hard Constraint 5 states the locked raw drift, logarithmic SCS, and reject gate.
- `data_quality_assessment.md` §3.1 defines `epsilon_H`, `SCS = log10(epsilon_H)`, boundary bands, and undefined near-zero `H(0)` behavior; §5.1 repeats the reject gate; SI-DQA-003 records the correction from raw-threshold confusion.
- `ctl_instruction(10).md` Step 3 uses static-invariant Plummer softening `epsilon_inv = 1e-10` for invariant potential energy and distinguishes it from training softening.
- `pinn_architecture(10).md` §Physics Residual and §Energy Conservation define the training-side `epsilon_train=1e-5`, which is distinct from validation.

#### Confidence

**High.** The only factor that would change this answer is a formal reopening of the locked post-v1.3 SCS decision.

#### Verification suggestion

Construct synthetic Hamiltonian series with known drifts `1e-10`, `1e-6`, `1e-5`, and `1e-4`. Confirm SCS values `-10`, `-6`, `-5`, and `-4`, and confirm that only `SCS > -5` rejects under the locked gate.

#### Proposed specification text

Because the locked SCS gate’s only written home is the read-only `data_quality_assessment.md`, add a cross-reference to `ctl_instruction(10).md` validation section:

```markdown
Validation SCS uses the locked post-v1.3 SI-DQA-003 convention: raw Hamiltonian drift is `epsilon_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(epsilon_H)`, and the reject gate is `SCS > -5` equivalently `epsilon_H > 1e-5`. Do not use raw-ratio thresholds while naming the quantity `SCS`. The validation Hamiltonian uses static validation Plummer epsilon `epsilon_val = 1e-10`.
```

---

### §5.2 Q-C2 (SASD) — Stiffness-Aware Sampling Density

#### Verdict / recommendation

Define SASD as a trajectory-level data-side sampling adequacy metric in normalized time.

For sorted normalized times `u_k = t_k/T`, define interval widths:

```math
\Delta u_k = u_{k+1} - u_k.
```

For each body `b` at the left endpoint of each interval, compute validation acceleration from the same scaled raw-mass force used by validation metrics:

```math
a'_{b,val}(u_k) = \sum_{j\ne b} m_j
\frac{r'_j(u_k)-r'_b(u_k)}{\left(\lVert r'_j(u_k)-r'_b(u_k)\rVert^2 + \epsilon_{val}^2\right)^{3/2}},
\qquad \epsilon_{val}=10^{-10}.
```

Define a velocity floor per trajectory:

```math
v_{floor} = \max\left(10^{-12},\; 10^{-6}\,\mathrm{median}_{k,b}\lVert v'_b(u_k)\rVert\right).
```

Then:

```math
SASD_{k,b} = \Delta u_k\,\frac{\lVert a'_{b,val}(u_k)\rVert}{\max(\lVert v'_b(u_k)\rVert, v_{floor})},
\qquad
SASD_{traj}=\max_{k,b} SASD_{k,b}.
```

Flag criterion:

```text
SASD_traj <= 0.5: data-side sampling density passes SASD gate
SASD_traj > 0.5: mark `resample_required` / not clean-training-ready
```

Store the full SASD profile for diagnostics, but do not decide collocation-density allocation here.

#### Reasoning

The metric estimates whether the output sampling interval is small relative to the local time scale for velocity change. Normalized-time variables are the natural choice because the network and preprocessing use `u=t/T`, scaled positions, and scaled velocities. The definition is dimensionless and equivalent in physical or normalized variables when used consistently. The velocity floor prevents division by zero while still flagging near-stationary high-acceleration points as potentially undersampled.

The `0.5` threshold comes from the data-quality report’s Phase 1 gate. It is plausible as a conservative “less than about half a local velocity-change time per sample” condition, but it should be empirically checked against actual trajectories.

#### Evidence

- `framed-research-questions.md` Q-C2 poses the data-side SASD definition and flags training-loop sampling use as out of scope.
- `data_quality_assessment.md` §3.2 defines `SASD_i = Δt_i ||a(t_i)|| / ||v(t_i)||` and says data with `SASD > 0.5` should be flagged for resampling; §5.1 repeats the `max(SASD)>0.5` gate.
- `claims-table.md` `CLM-09` gives verified `dt_out` by variant; `CLM-10` gives claimed-unverified approximate snapshot counts.
- `ctl_instruction(10).md` §Network input contract and §Global scaling establish normalized time and scaled variables.

#### Confidence

**Medium.** The most important factor that could change the threshold or floor is empirical correlation between SASD values, IPR failures, and actual training instability on a representative validation subset.

#### Verification suggestion

Compute SASD profiles for each family/fidelity. Inspect the top 1% highest-SASD intervals visually and compare them with close-encounter events and IPR outliers. Verify that `SASD>0.5` catches undersampled close encounters without rejecting most complete low-resolution trajectories solely for benign motion.

#### Proposed specification text

Add a validation-metrics subsection to `ctl_instruction(10).md`:

```markdown
SASD is a data-side sampling adequacy metric. In scaled normalized-time variables, compute `SASD_{k,b} = Δu_k ||a'_{b,val}(u_k)|| / max(||v'_b(u_k)||, v_floor)`, where `a'_{val}` uses the validation force with `epsilon_val=1e-10` and `v_floor=max(1e-12, 1e-6*median||v'||)` per trajectory. The trajectory score is `max_{k,b} SASD_{k,b}`. Trajectories with `SASD_traj > 0.5` are marked `resample_required` and excluded from the clean training set unless an explicit override policy is documented. This metric does not define collocation-density allocation.
```

---

### §5.3 Q-C3 (IPR) — Interpolation Physics Residual

#### Verdict / recommendation

Data-side IPR must use the validation epsilon `epsilon_val = 1e-10`, not training `epsilon_train = 1e-5`.

For each trajectory, construct a componentwise cubic Hermite interpolant over normalized time `u` using positions and velocities:

```text
inputs per body/component: (u_k, r'_b(u_k), v'_b(u_k))
interpolant: q_spline(u)
```

For each interval `[u_k, u_{k+1}]`, sample `M_interval = 10` interior points by default:

```math
\xi_{k,l}=u_k + \frac{l}{M_{interval}+1}(u_{k+1}-u_k),\quad l=1,\dots,M_{interval}.
```

Compute:

```math
IPR = \frac{1}{3M}\sum_{\xi}\sum_{b=1}^{3}
\left\lVert \frac{d^2 q_{spline,b}}{du^2}(\xi)
- a'_{b,val}(q_{spline}(\xi)) \right\rVert^2,
```

where `a'_{val}` uses raw masses and Plummer validation epsilon `1e-10`.

Gate:

```text
IPR <= 1e-3: pass IPR gate
IPR > 1e-3: mark `aliased_or_underresolved` / `resample_required`; exclude from clean training unless override
```

If later training-loop work needs an ALM noise-floor proxy with `epsilon_train=1e-5`, compute it as a separate metric named, for example, `IPR_train_eps`, not as the data-side validation IPR.

#### Reasoning

IPR is in scope only as a data-side metric. The hard dual-epsilon constraint says validation metrics use static `epsilon=1e-10`, while training uses `epsilon_train=1e-5`. The issue doc’s use of `1e-5` is tied to the training-loop role of IPR as an ALM noise floor, but that role is explicitly deferred to doc-03. Therefore the in-scope data-side IPR must evaluate Newtonian fidelity under the validation epsilon.

The cubic Hermite choice is appropriate because the Brutus data provide both positions and velocities, and PINNs learn a continuous trajectory rather than only point samples. If the Hermite interpolant violates the equations of motion between samples, the data are underresolved for continuous physics-informed learning even if endpoint snapshots look valid.

#### Evidence

- `framed-research-questions.md` Q-C3 asks which epsilon IPR should use under the locked dual-epsilon contract and marks the IPR-as-ALM-noise-floor role as deferred.
- `framed-research-questions.md` Hard Constraint 4 states validation metrics use static `epsilon=1e-10` and training uses `epsilon_train=1e-5`.
- `data_quality_assessment.md` §3.3 defines IPR as a spline physics residual; §5.1 specifies 10 synthetic points per interval and `IPR > 1e-3` as an aliasing gate.
- `pinn_architecture(10).md` §Physics Residual and §Energy Conservation specify training-side Plummer softening `epsilon_train=1e-5`, which is not the validation epsilon.

#### Confidence

**Medium.** The epsilon decision is high-confidence because it follows from a hard constraint. The `1e-3` IPR threshold is medium-confidence because it comes from a non-authoritative research report and needs empirical calibration.

#### Verification suggestion

Compute IPR for a stratified sample under both `epsilon_val=1e-10` and `epsilon_train=1e-5`, but use only the validation-epsilon result for the data-side gate. Compare high-IPR intervals to SASD spikes and visual trajectory curvature. Tune the threshold only if empirical false-positive/false-negative rates justify it.

#### Proposed specification text

Add to `ctl_instruction(10).md` validation-metrics subsection:

```markdown
Data-side IPR evaluates the physics residual of a cubic Hermite interpolant between Brutus snapshots. The interpolant is built in normalized time `u` from scaled positions and scaled velocities. The validation force uses raw masses and static validation Plummer epsilon `epsilon_val=1e-10`. The default audit samples 10 interior points per interval and computes the mean squared residual over bodies and points. `IPR > 1e-3` marks the trajectory as underresolved/resample-required. Any training-epsilon IPR diagnostic must be stored under a distinct metric name and is not the data-side validation gate.
```

---

### §5.4 Q-C4 (PSC) — Phase Space Coverage Entropy

#### Verdict / recommendation

Define PSC as a dataset-level diagnostic, not a per-trajectory rejection gate. The project should use a fixed, reproducible phase-space projection and a bias-corrected discrete entropy estimator.

Recommended default feature projection per snapshot:

```text
For each snapshot, compute pairwise separations r_12, r_13, r_23 and relative speeds v_12, v_13, v_23.
Sort the three separations ascending: r_(1) <= r_(2) <= r_(3).
Sort the three relative speeds ascending: v_(1) <= v_(2) <= v_(3).
Feature vector z = [log10(r_(1)+r_floor), log10(r_(2)+r_floor), log10(r_(3)+r_floor),
                    log10(v_(1)+v_floor), log10(v_(2)+v_floor), log10(v_(3)+v_floor)]
with r_floor = epsilon_val = 1e-10 and v_floor = 1e-12.
```

Grid construction:

```text
1. Define the PSC reference population: the candidate admissible training set, or a named subset such as family/fidelity/stage.
2. For each of the 6 dimensions, compute global bin edges from the reference population using robust quantiles q_low=0.005 and q_high=0.995.
3. Use B=16 equal-width bins between those quantiles per dimension.
4. Clip values below/above the quantile range into the edge bins and record clipped fractions.
5. Hash 6D bin coordinates to sparse occupancy counts; do not materialize the full dense 16^6 array unless needed.
```

Entropy estimator:

```math
p_k = n_k/N, \qquad
H_{plugin} = -\sum_{k:n_k>0} p_k \log p_k,
```

```math
H_{MM} = H_{plugin} + \frac{K_{occ}-1}{2N},
```

where `K_occ` is the number of occupied bins and `N` is the number of snapshot feature vectors. Report:

```text
PSC_entropy_nats = H_MM
PSC_entropy_bits = H_MM / log(2)
PSC_normalized = H_MM / log(B^6)
PSC_occupied_bins = K_occ
PSC_coverage_fraction = K_occ / B^6
PSC_clipped_fraction_by_dimension
```

Do not impose a universal pass/fail threshold in this issue. PSC is for dataset coverage auditing; training-loop replay use is deferred.

#### Reasoning

The full three-body phase space is too high-dimensional for a naive grid. A documented low-dimensional projection is necessary for reproducibility. Sorted pairwise separations and relative speeds are invariant to translation and mostly robust to body-label permutations while preserving close-encounter and high-relative-speed structure. Log scaling is appropriate because separations and speeds can vary by orders of magnitude. Miller-Madow correction reduces first-order finite-sample bias in plug-in entropy estimates without introducing a complex estimator.

A universal PSC threshold would be arbitrary from the package alone. The correct data-side deliverable is a reproducible diagnostic with enough metadata for later curriculum/replay decisions.

#### Evidence

- `framed-research-questions.md` Q-C4 asks for grid construction and entropy estimator and defers PSC-governed curriculum replay to doc-03.
- `data_quality_assessment.md` §3.4 defines PSC as Shannon entropy over a discretized phase-space grid and interprets low vs high entropy.
- `ctl_instruction(10).md` Step 2 and Step 3 establish scaled COM/gauge preprocessing and invariant metadata, supporting use of processed positions/velocities rather than raw-frame coordinates.

#### Confidence

**Medium-Low.** The entropy estimator is standard and the projection is physically motivated, but the exact feature projection and bin count are judgment calls because the package does not define them. The most important factor that could change this recommendation is an empirical coverage study comparing projections against known failure modes and stage labels.

#### Verification suggestion

Run PSC with the recommended 6D projection and compare against alternative projections, such as `(log r_min, log r_med, log r_max)` only or a Poincaré-section projection. Bootstrap the dataset to estimate entropy variance. Confirm that known rare close-encounter regimes occupy identifiable bins.

#### Proposed specification text

Add to `ctl_instruction(10).md` validation-metrics subsection:

```markdown
PSC is a dataset-level phase-space coverage diagnostic. The default projection uses sorted pairwise separations and sorted pairwise relative speeds in scaled coordinates, log-transformed with floors `r_floor=1e-10` and `v_floor=1e-12`. Bin edges are fixed from the named reference population using 0.5% and 99.5% quantiles and `B=16` equal-width bins per dimension. Entropy is reported using the Miller-Madow-corrected discrete Shannon estimator, together with normalized entropy, occupied-bin count, coverage fraction, and clipped fractions. PSC is not a per-trajectory admission gate in this issue.
```

---

## §6 Consistency pass

### §6.1 Hard-constraint consistency

- The 14D input contract and Jacobi `IC13` are preserved. No recommendation adds or removes network input channels.
- Raw masses remain canonical for `IC13`; mass audits do not replace IC masses silently.
- The mass-weighted COM projection head remains unchanged. Data-side metrics are computed on preprocessed scaled COM/gauge data; model-output metrics should consume projected positions if used later.
- The dual-epsilon contract is preserved: SCS, SASD, and data-side IPR use validation epsilon `1e-10`; training physics and matched Hamiltonian use `epsilon_train=1e-5`.
- The SCS log-drift gate is preserved: reject only if `SCS > -5`, while marginal/quality bands are recorded separately.
- The PHYS-01 raw-mass `D≈4.6416` convention is preserved; `D=6.694` is rejected for v1.4.

### §6.2 Scope-boundary consistency

- No recommendation allocates supplemental collocation density across `dt_out` variants. Q-B1 concerns supervised data-snapshot sampling only.
- No recommendation resolves G6 causal-training Option A vs Option B.
- SCS/SASD/IPR/PSC training-loop uses are not decided. The document defines data-side metrics and admission/diagnostic labels only.

### §6.3 Erratum consistency

- Gold Brutus status is determined by folder, not filename infix.
- Missing/partial footer populations are treated as absent-footer populations with no parameter fields.
- `CLM-09`, file counts behind `CLM-05`/`CLM-06`, `CLM-07`, and `CLM-08` are not over-discounted because the erratum re-verifies them.

### §6.4 Internal recommendation consistency

- Q-A1’s structural gate does not duplicate Q-C metric gates; it references them as additional admission filters.
- Q-A5’s footer default inference supplies `dt_out` metadata needed by Q-B1 and Q-C2, but Q-B1 and Q-C2 still compute from actual parsed times where possible.
- Q-A4’s no-silent-substitution policy is compatible with Q-A2’s key schema and Q-A6’s HDF5 index requirements.
- Q-B3’s float64 recommendation is compatible with Q-B2’s Decimal mass audit because masses are a special low-dimensional exactness check.

No unresolved contradiction was found among the recommendations and the hard constraints.

---

## Open items register

| ID | Type | Item | Exact additional input needed | Affected questions |
|---|---|---|---|---|
| OI-01 | Input mismatch | `DELIVERY-NOTE.md` is listed in the manifest but was not received. | The actual `DELIVERY-NOTE.md` sibling file, or confirmation that it is intentionally omitted. | §0, all only if it contains superseding scope/authority notes |
| OI-02 | Interim erratum | The erratum says DATA-07 will supersede it. | Phase 24 DATA-07 correction addendum keyed by CLM IDs. | Q-A2, Q-A5 |
| OI-03 | Dataset verification | Gap magnitudes and nominal counts are unverified. | On-disk file listings/counts for all four Brutus output folders and IC folders; Phase 24 DATA-01. | Q-A2 |
| OI-04 | Blacklist verification | Blacklist count/composition and current consumption status are unverified. | Full `problematic_ics_blacklist.json` and current DataLoader/runner source or execution audit showing whether it is consumed; Phase 24 DATA-02. | Q-A3 |
| OI-05 | Snapshot distribution | Approximate snapshot counts and final-timestep prevalence are unverified. | Per-trajectory parsed `n_snapshots`, `final_timestep`, and time-gap distribution; Phase 24 DATA-06. | Q-A1, Q-B1, Q-C2 |
| OI-06 | Missing-gold stage semantics | The package does not define whether missing standard-gold IDs skip to Stage 6 or enter Stage 5 with low-fidelity flags. | Authoritative curriculum/training-loop policy for consuming `missing_gold_counterpart`. | Q-A4 |
| OI-07 | Footer `Lw` fallback | `CLM-09` covers `tol`/`dt_out`; erratum says missing-footer files lack `Lw`, but no CLM row gives authoritative `Lw` defaults. | DATA-07 or dataset README correction specifying folder-level `Lw` defaults, if `Lw` is required downstream. | Q-A5 |
| OI-08 | Mass drift empirical result | The package does not contain actual IC-vs-Brutus mass comparisons. | Full or stratified mass audit output: relative differences by family/fidelity and footer class. | Q-B2, Q-B3 |
| OI-09 | Metric calibration | SASD `0.5` and IPR `1e-3` thresholds come from a non-authoritative research report and need empirical validation. | Distribution of SASD/IPR values, visual inspection of high-score intervals, and training/readiness outcomes for representative trajectories. | Q-C2, Q-C3 |
| OI-10 | PSC projection validation | No spec defines a PSC projection or bin count. | Empirical comparison of candidate PSC projections against known stage labels, close-encounter events, and coverage objectives. | Q-C4 |
| OI-11 | Near-zero Hamiltonian scale | The locked SCS definition says near-zero `H(0)` is undefined, but no package-wide near-zero threshold is specified. | Dataset-scale distribution of `H(0)` and a project-approved threshold for “numerically near zero,” if more precise behavior than manual review is required. | Q-C1, Q-B3 |

---

## References

### Package sources cited

- `README.md` — Issue-02 Research Package Manifest & Index, especially §Source-Treatment Preamble and §Per-File Manifest.
- `framed-research-questions.md` — complete authoritative question set for Issue 02, hard constraints, scope boundary, and Q-A1 through Q-C4.
- `claims-table.md` — CLM register and row notes for `CLM-01` through `CLM-13`.
- `consolidated-context.md` — dataset fragments: file naming/mapping, Brutus parameters, completeness checks, missing standard-gold IDs, blacklist summary, metrics script provenance.
- `ERRATUM-2026-06-10.md` — interim corrections on gold filenames and absent footer populations.
- `02-data-pipeline-and-validation.md` — non-authoritative issue/adjudication subject, used only as a candidate-position source.
- `ctl_instruction(10).md` — framework spec-edit target for parsing, preprocessing, global scaling, `IC13`, network input contract, and mini-batch construction.
- `pinn_architecture(10).md` — framework spec-edit target for physics residual, training softening, matched Hamiltonian, output layer, COM projection, and componentwise AD.
- `data_quality_assessment.md` — non-authoritative research report and sole written home of the locked post-v1.3 SCS gate, SI-DQA-003; also source for metric candidate definitions.
- `sampling_method(1).md` — frozen historical dataset-generation record; used only as contextual support where relevant, not as a revision target.

### External sources

No external sources were used.

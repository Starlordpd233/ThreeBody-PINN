# Resolution document for the data-pipeline and validation issue set

**Date:** June 11, 2026  
**Inventory received:** `RESEARCH-CONTEXT-MASTER.md`, `02-data-pipeline-and-validation(1).md`, `ctl_instruction(11).md`, `pinn_architecture(11).md`, `sampling_method(2).md`, and `data_quality_assessment(1).md`. The package manifest also names `DELIVERY-NOTE.md`, but that file was not part of the received upload set. fileciteturn0file5

## Scope and decision standard

This document answers the complete framed question set in `RESEARCH-CONTEXT-MASTER.md`: Q-A1 through Q-A6, Q-B1 through Q-B4, and Q-C1 through Q-C4. I treated the master file as the package entry point, the issue document as non-authoritative adjudication subject matter, `ctl_instruction.md` and `pinn_architecture.md` as the authoritative framework specs, `sampling_method.md` as frozen historical context, and `data_quality_assessment.md` as a non-authoritative research report that nevertheless contains the sole written home of the locked post-v1.3 SCS gate. I did not answer the explicitly excluded doc-03 topics: M16 collocation-density scaling, G6 causal-training option selection, or training-loop uses of SCS/SASD/IPR/PSC beyond their data-side definitions. fileciteturn0file5

The decision rule applied here was: locked hard constraints first; then byte-for-byte framework specs; then verified dataset-context items; then claimed-unverified CLM rows only where the recommendation does not silently depend on the unverified value. Where the package did not provide enough evidence to verify a present-state fact, I separated the **required contract** from the **unverified current implementation status** and recorded the missing empirical input in the open-items register rather than guessing. That matters especially for current blacklist-consumption status, actual ID-gap counts, true snapshot-count distributions, and real prevalence of incomplete runs, all of which the master file leaves to Phase 24 verification. fileciteturn0file5

The received upload was sufficient to answer the research questions, but not to verify every package claim empirically. In particular, the uploaded package did **not** include the actual `simulation_data/Data/...` trees or the excluded live `pinn/` codebase, so this document does not claim to have verified any `claimed-unverified` CLM row on disk. Where a recommendation depends only on locked conventions and documented per-variant defaults, I say so explicitly. Where it would require the actual dataset or runtime implementation, I flag that dependency. fileciteturn0file5

## Executive decision summary

The package supports one coherent resolution pattern. The data pipeline should build a deterministic **trajectory eligibility manifest** after parsing and before any training-side sampling. That manifest should key data by physical trajectory identity rather than array position, apply completeness and blacklist rules before stage sampling, record footer provenance field-by-field, and run an IC-versus-Brutus mass-consistency check as part of the manifest build. The issue document’s stage-dependent `snapshot_count >= 200` / `>= 2` proposal is not defensible under the package’s own `dt_out` defaults and completeness rule; the correct completeness gate is `t_final >= 9.5` plus variant-aware sanity checks derived from the declared output cadence. fileciteturn0file5

The missing-gold problem does **not** justify either relabeling those standard trajectories as Stage 6 or admitting low-fidelity substitutes into Stage 5. Stage 5 is defined as a high-resolution chaotic-orbit stage, Stage 6 is defined by physical criteria rather than by missing counterparts, and curriculum replay already keeps earlier low-fidelity trajectories in later training. The correct policy is therefore: keep those trajectories in their original low-fidelity stage lineage, mark them as not Stage-5-upgradable, and let replay bring them forward as earlier-stage material. fileciteturn0file1turn0file5

For processed storage, HDF5 should remain the canonical training-store format. The framework already allows HDF5 or `.npy`, but HDF5 is the better normative choice because it natively supports hierarchical grouping, colocated metadata attributes, chunked I/O, and transparent compression; by contrast, NumPy’s `.npy` format is intentionally a single-array container, with `.npz` used for multiple arrays. That makes HDF5 the cleaner fit for per-trajectory arrays plus metadata-rich manifests, while text/JSON should remain inspection-only exports. fileciteturn0file1 citeturn3view0turn4view5turn5view0turn5view2turn6view3turn6view2

On numerical handling, the package’s locked raw-mass scale convention \(D=(GT^2)^{1/3}\approx 4.6416\) should be retained, not replaced by the issue document’s `6.694` mass-fraction form. Float64 parsing is sufficient for validation metrics under the locked thresholds, because IEEE-754 float64 has machine epsilon \(2^{-52}\approx 2.22\times 10^{-16}\), which is comfortably below the validation gate of \(10^{-5}\) raw Hamiltonian drift and at or beyond the documented Brutus tolerances; exact decimal arithmetic should therefore be reserved for disputed literal text-equivalence checks such as mass parsing on the small subset of files that actually fail the float64 comparison. fileciteturn0file1turn0file5 citeturn4view2turn6view4

On validation metrics, the correct SCS definition is the locked post-v1.3 one: raw Hamiltonian drift \(\epsilon_H\), logged as \(SCS=\log_{10}(\epsilon_H)\), with hard reject at \(\epsilon_H>10^{-5}\) or equivalently \(SCS>-5\). SASD should be kept as a data-side curvature-resolution diagnostic, but implemented in the more numerically stable perpendicular-acceleration form and flagged at a conservative `0.5` threshold. IPR should be defined as a **validation-side** metric using the static epsilon \(10^{-10}\), not the training-time epsilon \(10^{-5}\), and should use a cubic Hermite spline that actually consumes the Brutus velocities rather than the distinct PCHIP algorithm that estimates slopes from values alone. PSC should be defined on a **deduplicated trajectory-level invariant grid**, not on raw snapshot counts, so that folder resolution and duplicated base/gold realizations do not distort the entropy score. fileciteturn0file2turn0file3turn0file5turn0file4 citeturn4view4turn8view0

## Decision matrix

| Question ID | One-line verdict | Confidence |
|---|---|---|
| Q-A1 | Add a post-metrics eligibility gate based on parsed timestamps, finiteness, declared cadence, and blacklist status; reject the `>=200` / `>=2` snapshot proposal. | High |
| Q-A2 | Index by physical and record keys derived from filenames and folders; never assume `ID == array index`. | High |
| Q-A3 | Enforce blacklist exclusion at the physical-trajectory level across all fidelities, and surface exclusions in manifest metadata and logs. | Medium |
| Q-A4 | Do not use Stage 6 or a low-fidelity Stage-5 fallback; retain the trajectory in its original low-fidelity stage lineage and mark it as not Stage-5-upgradable. | Medium |
| Q-A5 | Treat missing footers as absent metadata, not partial metadata; use folder defaults with per-field provenance. | High |
| Q-A6 | Keep HDF5 as the canonical processed training-data store; allow NumPy binary only as a derived cache/export; keep JSON/TXT inspection-only. | High |
| Q-B1 | Keep `n_pts_default = 32`; use `n_pts_eff = min(32, N_valid_snapshots)` without replacement; reject the `0.5*n_snapshots` rule as normative policy. | High |
| Q-B2 | Replace sample-based mass checks with a full-population IC↔Brutus `t=0` mass-consistency scan, using Decimal only on failures. | High |
| Q-B3 | Use float64 for all validation metrics and completeness checks; reserve Decimal for exact text-equivalence disputes only. | High |
| Q-B4 | Retain the locked raw-mass \(D\approx 4.6416\) convention; do not adopt \(D=6.694\) without a framework-wide mass-fraction rewrite. | High |
| Q-C1 | Use the locked log-drift SCS definition and reject gate \(SCS>-5\); store both raw drift and log score to prevent symbol confusion. | High |
| Q-C2 | Define SASD as a curvature-resolution metric using perpendicular acceleration and flag trajectories with `max SASD > 0.5`. | Medium |
| Q-C3 | Define IPR with cubic Hermite interpolation and the static validation epsilon \(10^{-10}\); do not use training epsilon for the data-side metric. | High |
| Q-C4 | Define PSC on a deduplicated, trajectory-level invariant grid; omit \(Q\) from the default PSC proxy because quasi-random size scaling distorts it. | Medium |

## Resolutions

**Cluster A — Ingestion and selection**

**Q-A1 — Stage 4 → Stage 5 validation gate**

**Verdict / recommendation.** Yes: a completeness-and-validity gate should exist after parsing/metric generation and before any training-side manifest or DataLoader sampling. It should be **stage-independent** and should enforce these conditions on every trajectory record:

1. all parsed numeric fields are finite;
2. every snapshot header reports `N = 3`;
3. parsed snapshot times are strictly increasing;
4. `t_final >= 9.5`, computed from the parsed time headers, not from footer text;
5. let `dt_nom` be the footer `dt_out` when a valid footer exists, otherwise the verified folder default for that variant; then require  
   \[
   N_{\text{snap}} \ge 1 + \left\lceil \frac{9.5}{dt_{\text{nom}}} \right\rceil;
   \]
6. the record passes the mass-consistency checks in Q-B2 / Step 2.1; and
7. the underlying physical trajectory is not blacklisted. fileciteturn0file5turn0file1

**Reasoning.** The issue document’s proposed stage-based `snapshot_count >= 200` / `>= 2` thresholds are not consistent with the package’s own documented `dt_out` values and completeness rule. From the verified folder defaults and the grounded `t_final >= 9.5` rule, a complete standard-base trajectory must have at least \(1+\lceil 9.5/0.17\rceil = 57\) snapshots, a complete hierarchical-base trajectory at least \(1+\lceil 9.5/0.08\rceil = 120\), and a complete gold trajectory at least \(1+\lceil 9.5/0.01\rceil = 951\). So a blanket `>=200` gate would wrongly exclude **all** complete base-resolution trajectories, while `>=2` is too weak to detect cadence-breaking truncation. This conclusion does **not** depend on the unverified approximate CLM-10 counts; it follows directly from the verified cadence defaults and the grounded completeness rule. The right move is therefore to base eligibility on parsed times plus cadence-derived sanity bounds, not on arbitrary stage buckets. fileciteturn0file5turn0file0

**Evidence.** The master file grounds (i) the completeness rule `final_timestep >= 9.5`, (ii) the verified default `dt_out` values by folder, and (iii) the fact that the metrics-calculation script processes all found files and does not itself perform completeness checks. The framework specs are silent on a loader-init gate, so the missing gate is genuinely a gap in executable contract rather than a conflict with a pre-existing spec clause. fileciteturn0file5turn0file1

**Confidence.** High. The main thing that would change this answer would be verified evidence that some folders intentionally contain cadence-breaking yet still training-eligible runs whose output sampling is not well approximated by the documented `dt_out` contract.

**Verification suggestion.** Build a manifest probe that parses times only and reports, per record: finiteness, monotonicity, `t_final`, inferred `dt_nom`, actual `N_snap`, and pass/fail reason. The probe should include no-footer files and at least one intentionally truncated file in unit tests. fileciteturn0file5

**Proposed specification change.** Add the following subsection to `ctl_instruction.md` immediately after Step 1 item 6. fileciteturn0file1

```text
### Step 1A: Trajectory eligibility manifest

After parsing but before preprocessing or training use, construct a manifest entry for each trajectory record.

Define:
- family ∈ {hierarchical, standard}
- fidelity ∈ {base, gold}
- physical_key = (family, numeric_id)
- record_key   = (family, fidelity, numeric_id)

A trajectory record is training-eligible iff:
1. all parsed numeric values are finite;
2. every snapshot header reports N = 3;
3. snapshot times are strictly increasing;
4. t_final, computed from parsed snapshot headers, is >= 9.5;
5. let dt_nom be footer dt_out if a valid Result footer is present, otherwise the folder-default dt_out for the record variant; then n_snapshots >= 1 + ceil(9.5 / dt_nom);
6. the mass-consistency checks in Step 2.1 pass;
7. the physical_key is not blacklisted.

Store in the manifest:
physical_key
record_key
ic_path
brutus_path
footer_present
tol_source
dt_out_source
Lw_source
eta_source
t_final
n_snapshots
eligibility_status
rejection_reasons
has_gold_counterpart
blacklist_status
```

**Q-A2 — Non-contiguous IDs**

**Verdict / recommendation.** The pipeline should treat the numeric ID as a **label inside a key**, never as an array index. The correct mapping contract is a two-level manifest: `physical_key = (family, numeric_id)` for the physical system, and `record_key = (family, fidelity, numeric_id)` for a specific parsed file record. Stage membership should attach to the physical key, while file lookup and training selection should use the record key. Curricula, replay sets, and per-stage deltas should therefore be stored as sets/lists of keys, not as slices over assumed-dense integer arrays. fileciteturn0file5turn0file1

**Reasoning.** The package makes two things clear. First, non-contiguous IDs are intentional. Second, base and gold folders can contain the **same** physical system under the same numeric ID but different fidelity realizations. A single global `id_to_path` dictionary keyed only by integer ID is therefore still under-specified; it would collide across families and across fidelities. The safer, fully specified contract is “physical key” plus “record key.” That contract also unifies the solutions to Q-A3 and Q-A4: the blacklist applies to the physical key, while Stage 5 upgrade availability is a property of which record keys are present under that same physical key. fileciteturn0file5turn0file1

**Evidence.** The master file identifies intentional ID gaps, states that the numeric ID is not an index, and documents that gold/base Brutus folders use the same base filename prefixes with gold status encoded by folder name rather than filename infix. It also records that the standard gold corpus is a subset of the standard base corpus with 184 missing gold counterparts. fileciteturn0file5

**Confidence.** High. This would change only if the project later introduced an explicit repository-level dataset manifest with globally unique stable IDs that supersede the current filename/folder contract.

**Verification suggestion.** Unit-test lookup over randomly chosen gapped IDs in both families and both fidelities, including an ID that exists in both base and gold and one that exists only in base. Assert that retrieval uses the correct `record_key`, not a positional index. fileciteturn0file5

**Proposed specification change.** No additional text beyond the Q-A1 manifest subsection is required. The key fields `physical_key` and `record_key` should be treated as mandatory there. fileciteturn0file1

**Q-A3 — Blacklist loading and consumption**

**Verdict / recommendation.** The blacklist should be loaded during manifest construction and applied at the **physical-key** level, not merely at an individual file-record level. If `(family, numeric_id)` is blacklisted, then **all** its realizations—base and gold—are excluded from training. The loader should fail closed if the blacklist is missing, malformed, or has unparseable IDs, and it should log per-family counts plus a deterministic exclusion manifest. fileciteturn0file5

**Reasoning.** The file is named `problematic_ics_blacklist.json`, and the master describes it as a list of problematic IC IDs, not as a list of broken individual Brutus files. Since the base and gold folders represent the same physical IC at different fidelities, excluding only one fidelity realization would be physically inconsistent: a problematic standard IC should not be allowed back in merely because its higher-resolution rerun exists, or vice versa. The unresolved part is not the **required contract** but the **current implementation status**, because the live `pinn/` code is excluded from the package and the master explicitly leaves present blacklist-consumption verification to Phase 24. fileciteturn0file5

**Evidence.** The master provides the blacklist’s documented structure and count, marks current loading/consumption status as an open finding, and excludes live `pinn/` code from grounding. That makes a normative contract recommendation appropriate while also requiring that current-state verification stay in the open-items register. fileciteturn0file5

**Confidence.** Medium. The main thing that would change this answer would be verified evidence that the blacklist was intended to exclude only one specific fidelity or one specific artifact type rather than the underlying IC itself.

**Verification suggestion.** During a Phase 24 probe, enumerate all records under each blacklisted physical key and assert that none survive into any stage manifest or batch. Log a fatal error if any blacklisted key appears in a replay pool or lookahead pool. fileciteturn0file5

**Proposed specification change.** No additional text beyond the Q-A1 manifest subsection is required, but `blacklist_status` should be defined there as a physical-key attribute that applies to all record keys underneath it. fileciteturn0file1

**Q-A4 — 184 standard IDs without a gold counterpart**

**Verdict / recommendation.** The correct policy is a **third option**: neither “skip to Stage 6” nor “admit a flagged low-fidelity fallback into Stage 5.” Instead:

- keep the physical trajectory in its original low-fidelity stage lineage (Stage 3 or Stage 4, as assigned from the base record);
- mark `stage5_upgrade_available = false` for that physical key;
- exclude it from the Stage 5 **delta set**, because Stage 5 is defined as the high-resolution chaotic set; and
- continue to include it in later training only via ordinary curriculum replay from earlier stages. fileciteturn0file1turn0file5

**Reasoning.** This follows directly from the stage definitions and replay semantics. `ctl_instruction.md` defines Stage 5 as “High-Resolution Chaotic Orbits” sourced from the high-resolution chaotic simulations, while Stage 6 is defined by a physical criterion (`s_min < 0.5` or `|E| < 0.01`), not by absent higher-fidelity reruns. The same file also says that each later stage replays all prior stages. So missing gold counterparts already remain part of Stage 5-era training through replay of their earlier low-fidelity stage; there is no need either to pollute Stage 5’s fidelity semantics or to repurpose Stage 6 as an administrative fallback bucket. fileciteturn0file1

**Evidence.** The master file verifies the 184 missing-gold figure and records the standard base-versus-gold count difference. The framework spec defines Stage 3/4 as low-fidelity standard data, Stage 5 as high-resolution chaotic data, and curriculum replay as cumulative. Those three facts jointly support the third-option policy. fileciteturn0file5turn0file1

**Confidence.** Medium. The single biggest thing that would change this answer would be a separate authoritative owner decision that Stage 5 must, by policy, contain a low-fidelity fallback representation for every Stage 4 physical key—something the current package does not state.

**Verification suggestion.** Build a stage-manifest diff that checks three conditions simultaneously: all 184 missing-gold IDs are absent from the Stage 5 delta set; none are automatically promoted to Stage 6 absent the Stage 6 criteria; and all otherwise-eligible missing-gold trajectories remain reachable through replay from their original earlier stage. fileciteturn0file5turn0file1

**Proposed specification change.** Add this paragraph to `ctl_instruction.md` in Step 5, after the stage-assignment paragraph. fileciteturn0file1

```text
Stage labels attach to physical_key. Base records realize stages 0, 1, 3, and 4. Gold records realize stages 2 and 5 when the corresponding gold record exists and passes eligibility checks. Stage 6 remains criteria-based and is never used as a missing-gold fallback. If a standard physical_key assigned to Stage 3 or Stage 4 has no eligible gold record, retain the base record in its original stage lineage and set stage5_upgrade_available = false.
```

**Q-A5 — Footer and parameter heterogeneity**

**Verdict / recommendation.** The correct footer-handling contract is:

- **Footer presence is metadata-only**, never a completeness criterion.
- If a valid `Result:` footer is present, use its recorded parameter fields.
- If no footer exists, assign parameters from the folder default for that record’s variant.
- Store provenance **per field**, not just as a single `tol_confidence` flag:
  - `tol_source ∈ {footer, folder_default}`
  - `dt_out_source ∈ {footer, folder_default}`
  - `Lw_source ∈ {footer, folder_default}`
  - `eta_source ∈ {footer, absent}`
- `t_end` should always come from parsed timestamps, not footer text, whether or not a footer exists. fileciteturn0file5

**Reasoning.** The correction provenance matters here. The package explicitly corrects the older “partial” / “minimal” footer story: the affected files do not contain partial schemas; they contain **no footer at all**. That implies two things. First, the data pipeline should not try to infer field presence from malformed footer fragments. Second, a single `tol_confidence` flag is too narrow, because `dt_out`, `Lw`, and `eta` also have provenance states. `eta`, in particular, should be treated as **absent**, not as inferred, when the footer is missing. The verified defaults are enough to fill `tol`, `dt_out`, and, where documented, `Lw`; completeness should still be based on parsed times. fileciteturn0file5

**Evidence.** The master’s corrected dataset context gives verified folder-default `tol` and `dt_out` values, corrected counts for no-footer populations, and the explicit instruction not to use footer presence for completeness. The issue document’s older “minimal footer” characterization is recorded as superseded. fileciteturn0file5turn0file0

**Confidence.** High. The main thing that would change this answer would be a later dataset rescan showing that some no-footer subset in fact belongs to a distinct, undocumented parameter regime rather than the recorded folder default.

**Verification suggestion.** Run a footer scanner that classifies records into `full footer` versus `no footer`, then emit manifest provenance fields and compare counts against the corrected CLM-07 / CLM-08 / CLM-09 expectations. fileciteturn0file5

**Proposed specification change.** No additional text beyond the Q-A1 manifest subsection is required; the proposed `*_source` fields there are the operative fix. fileciteturn0file1

**Q-A6 — Processed training-data format**

**Verdict / recommendation.** The framework should treat **HDF5 as the canonical processed training-data store**, accept NumPy binary as a **derived cache or export**, and treat JSON/TXT as **inspection-only**. This is primarily a storage-contract decision, not a methodology decision, provided the same canonical arrays, metadata, and manifest semantics are preserved across representations. fileciteturn0file1

**Reasoning.** HDF5 fits the package’s data model better than raw text or JSON: h5py represents HDF5 files as containers of groups and datasets, with groups acting like dictionaries, datasets acting like NumPy arrays, metadata stored alongside the data as attributes, and datasets supporting chunked I/O, transparent compression, and error-detection filters. NumPy’s `.npy` format is intentionally much narrower: it is the standard binary format for persisting **a single array**, while `.npz` is the standard multi-array bundle. `.npy` is useful because it is simple, portable, and memory-mappable, but it does not by itself provide the hierarchical grouping and colocated metadata model that the pipeline wants for per-trajectory arrays plus manifest fields. JSON/TXT is human-readable, but it is a poor canonical store for repeated high-volume tensor loading. citeturn3view0turn4view5turn5view0turn5view2turn6view3turn6view2

**Evidence.** The framework spec already recommends HDF5 or `.npy` at Step 1 item 6. The external format documentation strengthens the storage tradeoff: HDF5 provides the hierarchical, metadata-rich container model that the package’s per-trajectory corpus naturally wants, while `.npy` is explicitly a single-array format. fileciteturn0file1 citeturn3view0turn4view5turn5view2turn6view3

**Confidence.** High. The main thing that would change this answer would be a hard external deployment constraint that forbids HDF5 dependencies and values ultra-minimal readers over structured corpus semantics.

**Verification suggestion.** Benchmark one representative epoch’s worth of random-trajectory batch loads under HDF5 versus the project’s candidate NumPy-binary layout, including metadata lookup overhead rather than pure array-read timing only. fileciteturn0file1

**Proposed specification change.** Replace Step 1 item 6 in `ctl_instruction.md` with this text. fileciteturn0file1

```text
6. Save parsed objects in HDF5 as the canonical processed training-data store. A NumPy binary cache (.npy or equivalent multi-array bundle) MAY be emitted as a derived artifact for array-level experiments or debugging, but it is not the canonical corpus format. Human-readable JSON/TXT exports MAY be emitted for inspection only and MUST NOT replace the canonical training store.
```

**Cluster B — Sampling, precision, and global scale**

**Q-B1 — Points-per-trajectory feasibility**

**Verdict / recommendation.** Keep the spec’s nominal `n_pts = 32` as the default target. Do **not** replace it with the issue document’s `n_pts = min(32, int(0.5*n_snapshots))` rule. Instead, implement the safety guard  
\[
n_{\text{pts,eff}} = \min(32, N_{\text{valid snapshots}})
\]
and sample without replacement from the eligible snapshot index set. fileciteturn0file1turn0file5

**Reasoning.** On the package’s own documented completeness rule and per-folder cadence defaults, complete standard-base trajectories already have at least 57 snapshots, so 32 points per trajectory is feasible. The issue document’s “infeasible” characterization overstates the case. A fixed `0.5*n_snapshots` rule is also conceptually awkward: it makes the per-trajectory batch contract depend on resolution in an arbitrary way and would downweight complete standard trajectories to 28 or 29 points despite the spec already expecting 32. A simple minimum-with-availability guard is the better engineering rule: it preserves the existing contract where feasible, gracefully handles rare short survivors, and does not bake an unmotivated “half the file” heuristic into the training spec. Whether 32 is *optimal* for optimization dynamics is a doc-03-style training-loop question, not a data-pipeline feasibility blocker. fileciteturn0file1turn0file5turn0file0

**Evidence.** The framework spec’s batch section uses `n_pts (e.g., 32)`. The master file supplies the grounded `dt_out` defaults and completeness rule needed to infer minimum feasible snapshot counts without relying on the unverified approximate CLM-10 counts. fileciteturn0file1turn0file5

**Confidence.** High. This would change only if Phase 24 showed that a substantial share of completeness-surviving trajectories still have fewer than 32 valid snapshots, which would imply a deeper parsing/cadence problem than the package currently describes.

**Verification suggestion.** Report the distribution of `N_valid_snapshots` after the Q-A1 eligibility gate and verify that `n_pts_eff < 32` is a rare exception rather than a frequent path. fileciteturn0file5

**Proposed specification change.** Modify `ctl_instruction.md`, “Mini-Batch Construction with Lookahead Sampling,” as follows. fileciteturn0file1

```text
Sample n_pts_default = 32 time points per trajectory. For each trajectory, define n_pts_eff = min(n_pts_default, N_valid_snapshots) and draw the indices without replacement from the eligible snapshot set. The 32-point value is the nominal target, not a hard requirement when fewer eligible snapshots are available.
```

**Q-B2 — Footer and mass-drift protocol**

**Verdict / recommendation.** The project should stop sampling 100 or 1000 pairs and instead perform a **full-population IC↔Brutus `t=0` mass-consistency scan** during manifest construction. Use this procedure:

1. parse IC masses and Brutus `t=0` masses in float64;
2. compare with `np.allclose(rtol=1e-15, atol=0.0)`;
3. if the comparison passes, treat the IC masses as canonical for that record;
4. if it fails, reparse **that failing record** with exact decimal arithmetic from the source strings;
5. if the exact-decimal comparison still fails, quarantine the record; if it passes, keep the record but mark `mass_parse_mode = decimal_fallback`. fileciteturn0file1turn0file5

**Reasoning.** The package itself already treats mass invariance as a precondition for preprocessing. Since there are only three masses per trajectory and roughly fifteen thousand trajectories in total, a full scan is cheap compared with training and resolves the issue document’s internal `1000` versus `100` conflict cleanly. Sampling is appropriate when the audit itself is expensive; this one is not. The right contract is therefore “scan all, escalate only failures.” fileciteturn0file1turn0file5turn0file0

**Evidence.** `ctl_instruction.md` Step 2.1 already requires mass invariance in float64 parse space and states that the COM transform depends on consistent masses between the IC and the Brutus output. The master file records the issue document’s internal conflict on whether to sample 1000 or 100 pairs and correctly marks the empirical mass-drift status as still needing verification. The Python standard library documentation confirms that `decimal` exists specifically for correctly rounded decimal arithmetic and exact decimal representations when that fallback is needed. fileciteturn0file1turn0file5 citeturn6view4

**Confidence.** High. The only serious thing that would change this answer would be a very unusual I/O environment in which a full-population first-snapshot scan was operationally prohibitive.

**Verification suggestion.** Emit a CSV or JSON audit with one line per record: `record_key`, float64 pass/fail, decimal fallback used or not, and final disposition. The failing-set size should be the dataset fact of interest, not the sampled audit size. fileciteturn0file5

**Proposed specification change.** Extend `ctl_instruction.md` Step 2.1 with this text. fileciteturn0file1

```text
Before the trajectory-level mass-invariance scan, compare the IC masses to the Brutus t=0 masses for every trajectory record. Use float64 first with allclose(rtol=1e-15, atol=0.0). On a float64 failure, reparse the failing record’s mass strings with exact decimal arithmetic. If the exact comparison fails, quarantine the record. If the exact comparison passes, retain the record and mark mass_parse_mode = decimal_fallback. Canonical masses for downstream preprocessing are the IC masses.
```

**Q-B3 — Precision handling**

**Verdict / recommendation.** Float64 is sufficient for completeness checks, invariant calculations, and the validation metrics SCS, SASD, IPR, and PSC under the package’s locked thresholds. Exact decimal parsing should be reserved for the narrowly scoped cases in which the project is checking **literal text-equivalence** or resolving a failed float64 mass comparison. General trajectory parsing, interpolation, and metric computation should remain float64. fileciteturn0file1turn0file5

**Reasoning.** NumPy documents float64 machine epsilon as \(2^{-52}\approx 2.22\times 10^{-16}\). The project’s locked validation reject gate is \(\epsilon_H>10^{-5}\), and the documented Brutus tolerances are on the order of \(10^{-13}\) to \(10^{-15}\). That means float64 is already at or past the precision regime needed for the package’s screening logic; the main place where decimal precision helps is not vectorized dynamics, but exact recovery of decimal text fields when a literal mass string might be rounded differently across file types. Python’s `decimal` module is designed exactly for that sort of correctly rounded decimal arithmetic and exact decimal representation. fileciteturn0file5turn0file1 citeturn4view2turn6view4

**Evidence.** The package itself already specifies float64 parsing in Step 2.1 and fixes the validation-side static epsilon and SCS gate via its hard constraints. The external numerical documentation confirms the float64 precision floor and the role of decimal arithmetic. fileciteturn0file1turn0file5 citeturn4view2turn6view4

**Confidence.** High. The most important thing that would change this answer would be verified evidence that some validation metric materially changes pass/fail classification when recomputed in high precision on real trajectory files.

**Verification suggestion.** Recompute SCS and selected invariant calculations on a stratified sample using both float64 and a high-precision fallback path, then compare classification stability rather than raw ulp differences only. fileciteturn0file5

**Proposed specification change.** No additional spec text beyond the Q-B2 addition is necessary; the existing Step 2.1 float64 parse contract should remain the default. fileciteturn0file1

**Q-B4 — Global-scale `compute_globals` and \(D = 6.694\)**

**Verdict / recommendation.** The correct global length scale is the locked raw-mass form,
\[
D = (G T^2)^{1/3} \approx 4.6416 \quad (G=1,\; T=10),
\]
and the issue document’s `6.694` form should **not** be adopted. Any helper such as `compute_globals` must use the same nondimensionalization and invariant-energy definition already fixed elsewhere in the framework. fileciteturn0file1turn0file5

**Reasoning.** This is not a judgment call; it follows from the locked framework and from first principles. Starting from
\[
\frac{d^2 \mathbf r_i}{dt^2} = G \sum_{j\neq i} m_j \frac{\mathbf r_j-\mathbf r_i}{\lVert \mathbf r_j-\mathbf r_i\rVert^3},
\]
substitute \(\mathbf r_i = D\mathbf r'_i\) and \(t = Tu\). Then
\[
\frac{D}{T^2}\frac{d^2 \mathbf r'_i}{du^2}
=
\frac{G}{D^2}\sum_{j\neq i} m_j \frac{\mathbf r'_j-\mathbf r'_i}{\lVert \mathbf r'_j-\mathbf r'_i\rVert^3},
\]
so
\[
\frac{d^2 \mathbf r'_i}{du^2}
=
\frac{GT^2}{D^3}\sum_{j\neq i} m_j \frac{\mathbf r'_j-\mathbf r'_i}{\lVert \mathbf r'_j-\mathbf r'_i\rVert^3}.
\]
To absorb the coefficient while keeping the **raw masses** in the residual, one must set \(D^3 = GT^2\). The alternative \(D^3 = GM_{\text{tot}}T^2\) leaves a factor \(1/M_{\text{tot}}\) unless every mass and every downstream formula is rewritten in mass-fraction form. The framework spec says exactly that and explicitly rejects the `6.694` form absent a framework-wide rewrite. fileciteturn0file1turn0file5

**Evidence.** `ctl_instruction.md` §2.5 states the raw-mass convention and explicitly rejects the `6.694` mass-fraction alternative. The master file reproduces that as a locked hard constraint and frames the issue document’s `6.694` claim as a known conflict to adjudicate rather than as a fact. fileciteturn0file1turn0file5turn0file0

**Confidence.** High. This would change only if the project explicitly opened a new, framework-wide mass-fraction rewrite that touched the residual, Hamiltonian, angular momentum, COM, and invariant formulas together.

**Verification suggestion.** Run the existing scaling-consistency acceptance check and, separately, a symbolic or notebook derivation that verifies the coefficient on the dimensionless residual is unity under the chosen \(D\). fileciteturn0file3turn0file1

**Proposed specification change.** No spec change is required; the authoritative spec is already correct. The change needed is to reject the issue document’s contrary recommendation in downstream adjudication. fileciteturn0file1turn0file5turn0file0

**Cluster C — Validation metrics**

**Q-C1 — Symplectic Conservation Score**

**Verdict / recommendation.** The correct validation-side definition is:

- compute the validation Hamiltonian with the **static** matched-Plummer convention already used for offline invariants, i.e. \(\epsilon_{\text{inv}} = 10^{-10}\) in the potential denominator;
- define raw drift
  \[
  \epsilon_{H,\text{raw}}=\max_t \left|\frac{H(t)-H(0)}{H(0)}\right|;
  \]
- define
  \[
  SCS_{\log} = \log_{10}(\epsilon_{H,\text{raw}});
  \]
- reject if \(\epsilon_{H,\text{raw}} > 10^{-5}\), equivalently if \(SCS_{\log} > -5\);
- store **both** `epsilon_H_raw` and `SCS_log10` in the manifest to prevent future symbol confusion. fileciteturn0file5turn0file2turn0file1

**Reasoning.** The issue document’s ratio thresholds and the locked post-v1.3 gate are not competing thresholds on the same scalar; they are definitions on **different quantities**. The master file explicitly identifies that category error. The framework’s hard constraint fixes the gate as a log-drift score derived from raw Hamiltonian drift. The package’s validation/training dual-epsilon split also means this must be a validation-side static-epsilon Hamiltonian, not the training-side \(10^{-5}\) regularized one. The safest operational fix is to store both the raw drift and the log score by name. That removes the recurring ambiguity around the symbol `SCS` and keeps the gate computable either way. fileciteturn0file5turn0file2turn0file1

**Evidence.** The master file identifies the hard constraint, the symbol-confusion problem, and the dual-epsilon split. `data_quality_assessment.md` contains the corrected SCS definition and the SI-DQA-003 note that tightened the reject gate to `SCS > -5`, equivalent to raw drift \(>10^{-5}\). `ctl_instruction.md` supplies the validation-side static-invariant epsilon convention used elsewhere for offline invariant calculations. fileciteturn0file5turn0file2turn0file1

**Confidence.** High. The only thing that would change this answer would be a future owner-approved revision to the reject gate itself after Phase 24 remeasurement.

**Verification suggestion.** Recompute the metric on a stratified sample and assert the identity
\[
SCS_{\log} = \log_{10}(\epsilon_{H,\text{raw}})
\]
numerically to machine precision for every finite record. Fail the test if any implementation path logs one quantity and thresholds another. fileciteturn0file2turn0file5

**Proposed specification change.** Add this subsection under `ctl_instruction.md` → “Evaluation Metrics and Validation.” The same subsection also implements Q-C2, Q-C3, and Q-C4 below. fileciteturn0file1

```text
### Pre-training trajectory-screening metrics

Use the locked post-v1.3 SCS contract from data_quality_assessment.md for trajectory screening. Compute validation Hamiltonians with the static invariant epsilon epsilon_inv = 1e-10. Store:
- epsilon_H_raw = max_t abs((H(t) - H(0)) / H(0))
- SCS_log10 = log10(epsilon_H_raw)

Hard reject if epsilon_H_raw > 1e-5 (equivalently SCS_log10 > -5).

For all screening metrics, operate on the preprocessed scaled trajectories and use the same ordered raw masses that feed the downstream physical calculations.
```

**Q-C2 — Stiffness-Aware Sampling Density**

**Verdict / recommendation.** The correct data-side SASD should be defined as a **turning-rate resolution** metric over intervals, not merely as “any acceleration over any speed.” I recommend:

For each interval \(i\) with \(\Delta t_i = t_{i+1}-t_i\), let
\[
\mathbf a_{\perp,i}
=
\mathbf a_i
-
\frac{\mathbf a_i\cdot \mathbf v_i}{\lVert\mathbf v_i\rVert^2 + v_{\text{floor}}^2}\,\mathbf v_i,
\]
with \(v_{\text{floor}} = 10^{-12}\) in scaled velocity units, and define
\[
SASD_i
=
\Delta t_i\,
\frac{\lVert \mathbf a_{\perp,i}\rVert}{\max(\lVert\mathbf v_i\rVert, v_{\text{floor}})}.
\]

Flag a trajectory for resampling if
\[
\max_i SASD_i > 0.5.
\]
Optionally log a warning band for \(0.3 < \max_i SASD_i \le 0.5\). fileciteturn0file2turn0file5

**Reasoning.** The issue document’s scalar \(\Delta t\,\|\mathbf a\|/\|\mathbf v\|\) is a useful first proxy, and the research report itself notes that a curvature-based version is more robust. The perpendicular-acceleration form is the better canonical definition because it measures directional turning rather than pure speed-up or slow-down. In constant-speed circular motion, \(a_\perp = v^2/R\), so SASD reduces to \(\Delta t\,v/R\), which is exactly the turning angle in radians between samples. That gives the `0.5` threshold a clean meaning: about 29 degrees of turning in one sample interval is a conservative “under-resolved” flag. The \(v_{\text{floor}}\) clause resolves the turning-point singularity that the raw \(\|\mathbf a\|/\|\mathbf v\|\) form leaves exposed. fileciteturn0file2turn0file5

**Evidence.** The package defines SASD conceptually as a ratio of time step to local characteristic time and records `0.5` as the only concrete flagging threshold in the data-quality report. The framework specs are silent on an exact data-side formula, so the choice between total acceleration and curvature-aware acceleration is an engineering judgment within the package’s stated intent. fileciteturn0file2turn0file5

**Confidence.** Medium. The main thing that would change this answer would be Phase 24 evidence that a different threshold or a different local-timescale proxy correlates much better with downstream interpolation failure on the actual corpus.

**Verification suggestion.** Validate SASD on synthetic trajectories with known curvature: circular motion should yield SASD equal to the turning angle per sample; straight-line motion with purely tangential acceleration should not falsely report large turning-rate SASD. fileciteturn0file2

**Proposed specification change.** Use the same “Pre-training trajectory-screening metrics” subsection introduced under Q-C1 and append this text. fileciteturn0file1

```text
Define intervalwise SASD on preprocessed scaled trajectories by:
- delta_t_i = t_{i+1} - t_i
- a_perp_i = a_i - ((a_i · v_i) / (||v_i||^2 + v_floor^2)) v_i
- SASD_i = delta_t_i * ||a_perp_i|| / max(||v_i||, v_floor)

Use v_floor = 1e-12 in scaled units. Flag the trajectory for resampling if max_i SASD_i > 0.5. Log a warning if 0.3 < max_i SASD_i <= 0.5.
```

**Q-C3 — Interpolation Physics Residual**

**Verdict / recommendation.** The correct **data-side** IPR uses the **static validation epsilon** \(10^{-10}\), not the training epsilon \(10^{-5}\). It should be computed from a cubic Hermite interpolant that consumes the Brutus velocities directly. For a trajectory with times \(t_n\), positions \(\mathbf r_n\), and velocities \(\mathbf v_n\):

1. For each output component, build a cubic Hermite spline \( \mathbf r_{\text{spline}}(t)\) from \((t_n,\mathbf r_n,\mathbf v_n)\).
2. For each interval \([t_n,t_{n+1}]\), sample \(M=10\) **interior** points
   \[
   \tau_{n,k}=t_n+\frac{k}{M+1}(t_{n+1}-t_n), \quad k=1,\dots,M.
   \]
3. Evaluate
   \[
   IPR
   =
   \frac{1}{N_{\text{test}}}
   \sum_{\tau}
   \left\|
   \ddot{\mathbf r}_{\text{spline}}(\tau)
   -
   \mathbf F_{\epsilon_{\text{inv}}}\!\left(\mathbf r_{\text{spline}}(\tau)\right)
   \right\|_2^2,
   \]
   with \(\epsilon_{\text{inv}} = 10^{-10}\) and the same ordered raw masses used elsewhere in validation. fileciteturn0file5turn0file2turn0file1

**Reasoning.** The dual-epsilon hard constraint controls this answer: data-side validation metrics use the static epsilon, while the training-time residual uses \(10^{-5}\). The issue document’s \(10^{-5}\) IPR definition is tied to a later training-loop role that the master explicitly defers to doc-03. For the in-scope **validation** metric, static epsilon is the correct choice. The interpolation method also matters. SciPy’s `CubicHermiteSpline` takes both values and first derivatives and produces a \(C^1\)-smooth piecewise cubic object; `PchipInterpolator`, despite the name, takes only \(x\) and \(y\) values and estimates derivatives internally. Because Brutus already supplies velocities, the correct algorithm for IPR is the true cubic Hermite interpolant with supplied derivatives, not PCHIP. Sampling interior points avoids the second-derivative jump issue at spline knots. citeturn4view4turn8view0

**Evidence.** The master file locks the dual-epsilon split and scopes only the data-side IPR definition into this research. The data-quality report gives the conceptual IPR protocol, including 10 synthetic points per interval, while the external SciPy documentation distinguishes the derivative-consuming cubic Hermite spline from PCHIP’s value-only monotone interpolation. fileciteturn0file5turn0file2 citeturn4view4turn8view0

**Confidence.** High. The main factor that would change this answer would be a future doc-03 decision to define a **separate** training-side `IPR_train` with \(10^{-5}\) for optimizer calibration; that would add a second metric, not replace the data-side audit definition.

**Verification suggestion.** On a dense analytic benchmark or a very high-resolution Brutus subset, verify that IPR decreases under temporal refinement and that the static-epsilon definition is stable under repeat computation. fileciteturn0file2

**Proposed specification change.** Use the same inserted screening-metrics subsection and append this text. fileciteturn0file1

```text
Define data-side IPR using the static validation epsilon epsilon_inv = 1e-10. Construct a cubic Hermite spline from the preprocessed trajectory positions and velocities. Sample M = 10 interior points per observed interval. Compute the mean squared mismatch between the spline second derivative and the matched-Plummer gravitational force at those interior points.

Use a spline method that consumes supplied first derivatives. Do not replace this with a value-only PCHIP interpolation when Brutus velocities are available.
```

**Q-C4 — Phase Space Coverage Entropy**

**Verdict / recommendation.** The package does not contain enough evidence to identify a uniquely canonical high-dimensional phase-space projection, so the right default is a **trajectory-level, deduplicated proxy** rather than a snapshot-count entropy. I recommend:

1. Deduplicate by physical trajectory key `(family, numeric_id)`, preferring the gold record when both base and gold exist.
2. For each deduplicated physical trajectory, form the invariant feature vector
   \[
   \mathbf z_j =
   \left[
   \frac{E_j}{E_{\text{scale}}},
   \;L_{\text{norm},j},
   \;\log_{10}\!\left(\frac{\max(s_{\min,j},10^{-12})}{s_{\min,\text{scale}}}\right)
   \right].
   \]
3. Along each axis, compute the 1st and 99th percentile of the evaluated corpus and create 16 equal-width bins between those bounds; clip out-of-range values into the edge bins.
4. Let \(n_k\) be the count in occupied grid cell \(k\), \(N=\sum_k n_k\), and \(p_k=n_k/N\).
5. Report
   \[
   PSC = -\sum_k p_k \ln p_k,
   \qquad
   PSC_{\text{norm}} = \frac{PSC}{\ln K_{\text{occ}}},
   \]
   where \(K_{\text{occ}}\) is the number of occupied bins. fileciteturn0file5turn0file1turn0file4

**Reasoning.** Three considerations drive this design. First, a snapshot-level entropy would be badly contaminated by the package’s known resolution heterogeneity: gold trajectories have many more timestamps than base trajectories, so a raw snapshot histogram would largely become a temporal-resolution measure rather than a diversity measure. Second, the package contains duplicate physical systems across base and gold; counting both would overweight rerun systems. Third, `sampling_method.md` explicitly says the quasi-random size-scaling feature distorts the virial ratio \(Q\) by \(s^3\), so \(Q\) is not a clean default axis for a cross-variant diversity metric. Using the existing trajectory-level invariants \(E\), \(L_{\text{norm}}\), and \(s_{\min}\) therefore gives a stable, interpretable, and deduplicated default proxy that is not silently biased by output cadence or by the sampling-time virial-ratio distortion. fileciteturn0file4turn0file1turn0file5

**Evidence.** The master scopes only the **data-side** PSC definition into this research and does not lock a projection. The framework spec already computes the invariants used above. The sampling-method spec explicitly warns that the quasi-random size-scaling option distorts \(Q\), which is why I exclude it from the default PSC proxy. fileciteturn0file5turn0file1turn0file4

**Confidence.** Medium. The strongest thing that would change this answer would be a downstream doc-03 requirement for a specific replay-weighting or sampling objective that needs a snapshot-level, not trajectory-level, entropy proxy.

**Verification suggestion.** Compute PSC once with fidelity deduplication and once without it; the deduplicated score should be the canonical one. Also verify that a corpus containing both base and gold realizations of the same physical systems does not change PSC solely because of duplicated trajectories or denser timestamping. fileciteturn0file5

**Proposed specification change.** Use the same inserted screening-metrics subsection and append this text. fileciteturn0file1

```text
Define the default data-side PSC on deduplicated physical trajectories, not on raw snapshot counts. Deduplicate by physical_key, preferring the gold record when both fidelities exist. Use the trajectory-level invariant vector [E / E_scale, L_norm, log10(max(s_min, 1e-12) / s_min_scale)]. Construct a 16 x 16 x 16 grid from the corpus 1st–99th percentile range on each axis, clip outliers into edge bins, and compute Shannon entropy over occupied bins. Report both raw PSC and PSC_norm = PSC / ln(K_occ).
```

## Open items register

| Item | Affected questions | Why it remains open here | Additional input needed |
|---|---|---|---|
| Missing `DELIVERY-NOTE.md` from the received upload set | Scope only | The master manifest names a standalone delivery note, but it was not part of the uploaded package received in this session. None of the framed questions required it, so it does not block the present recommendations, but it is still an input mismatch. | Upload `DELIVERY-NOTE.md` if the handoff/gate context itself must be audited. fileciteturn0file5 |
| Actual Phase-24 empirical verification of CLM-01, CLM-02, CLM-03, CLM-10, CLM-11, and CLM-12 | Q-A1, Q-A2, Q-A3, Q-B1 | The package explicitly marks these rows `claimed-unverified`, and the actual dataset tree was not part of the upload. The recommendations above were written to avoid silently depending on those unverified counts where possible. | Phase-24 outputs (`DATA-01` through `DATA-07`) or direct access to the dataset inventory/manifests. fileciteturn0file5 |
| Current implementation status of blacklist consumption and loader-side gating | Q-A3, Q-A1 | Live `pinn/` code is excluded from the package and repository access is unavailable, so current runtime behavior cannot be verified from the uploaded materials. | Repository snapshot of the active loader/runner implementation, or Phase-24 probe outputs on blacklist consumption and completeness gating. fileciteturn0file5 |
| Real prevalence of float64-versus-Decimal mass mismatches | Q-B2, Q-B3 | The package frames this as a protocol question, not an already verified dataset fact. I therefore specified the required contract, but not a claimed mismatch rate. | Full-population IC↔Brutus `t=0` mass-scan output. fileciteturn0file5turn0file1 |
| Hard numerical threshold for IPR as a training or rejection gate | Q-C3 | The package’s only numeric `IPR > 1e-3` gate appears in a non-authoritative research report, while the master scopes only the data-side definition into this research and defers training-loop usage to doc-03. | A calibrated corpus with owner-approved gate semantics, or the future doc-03 specification. fileciteturn0file2turn0file5 |
| Whether the project wants a different PSC projection for downstream replay control | Q-C4 | The recommended PSC above is a defensible data-side default, but the package does not lock a single downstream consumer or replay-weighting use case, and those training-loop uses are explicitly deferred. | The future doc-03 specification, or an owner decision naming the intended downstream control objective for PSC. fileciteturn0file5 |

## References

Andrew Collette and contributors. *h5py Documentation*, version 3.16.0. “Quick Start Guide” and “Datasets.” Accessed June 11, 2026. citeturn3view0turn4view5turn5view0turn5view2

NumPy Developers. *NumPy v2.4 Manual*. “numpy.lib.format,” “numpy.save,” and “numpy.finfo.” Accessed June 11, 2026. citeturn4view1turn6view2turn6view3turn6view1turn4view2

Python Software Foundation. *Python 3.14.6 Documentation*. “`decimal` — Decimal fixed-point and floating-point arithmetic.” Accessed June 11, 2026. citeturn4view3turn6view4

SciPy Developers. *SciPy v1.17.0 Manual*. “`CubicHermiteSpline`” and “`PchipInterpolator`.” Accessed June 11, 2026. citeturn4view4turn8view0
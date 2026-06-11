# Resolution Document for Issue 02 Data Pipeline and Validation

Date: 2026-06-10  
Package inventory received: `README(1).md`; `framed-research-questions.md`; `claims-table.md`; `consolidated-context.md`; `ERRATUM-2026-06-10.md`; `02-data-pipeline-and-validation.md`; `ctl_instruction(1).md`; `pinn_architecture(1).md`; `sampling_method.md`; `data_quality_assessment.md`. The manifest also references `DELIVERY-NOTE.md`, but that file was not in the uploaded set. fileciteturn0file9

## Scope and decision standard

This document answers every in-scope question in `framed-research-questions.md` and stays inside the package’s authority hierarchy. I treat the manifest and framed questions as the package-level control documents; `ctl_instruction.md` and `pinn_architecture.md` as the authoritative framework specs; `sampling_method.md` as frozen historical context; `data_quality_assessment.md` as non-authoritative except where the framed questions explicitly elevate its post-v1.3 SCS gate to a locked convention; and the issue doc as non-authoritative adjudication subject matter rather than as a verdict source. I also incorporate the 2026-06-10 erratum, which corrects two package-level dataset narratives: gold Brutus filenames do **not** carry a `_gold_` infix, and the files previously described as having “partial” or “minimal” footers in three populations in fact have **no** `Result:` footer at all. fileciteturn0file9 fileciteturn0file8 fileciteturn0file1 fileciteturn0file3 fileciteturn0file4 fileciteturn0file2 fileciteturn0file7

The six locked v1.4 conventions reproduced in the framed questions are treated here as hard boundary conditions: the exact 14D input contract `x_net = [τ, IC13]`; the raw-mass Jacobi `IC13`; the mass-weighted COM projection head; the dual-epsilon split (`ε_inv = 1e-10` for validation-side invariants/metrics and `ε_train = 1e-5` for training residuals); the post-v1.3 SCS gate `SCS = log10(ε_H)` with reject threshold `SCS > -5`; and the raw-mass PHYS-01 length scale `D = (G T^2)^(1/3) ≈ 4.6416`. Nothing below reopens those locks. Where the issue doc conflicts with them, I reject the issue-doc position; where the specs are silent, I specify a data-side contract that is consistent with them. fileciteturn0file8 fileciteturn0file1 fileciteturn0file3 fileciteturn0file2

The package also requires claims discipline. I therefore do **not** treat `claimed-unverified` CLM rows as established facts. My recommendations are written so that they do not depend on exact values for CLM-01, CLM-02, CLM-03, CLM-10, CLM-11, or CLM-13 unless I say so explicitly. Where a recommendation might be sharpened by Phase-24 empirical verification, I record that dependency in the confidence note or the open-items register rather than guessing. I also respect the scope boundary: I do **not** answer M16 `dt_out` collocation-density scaling, G6 causal-training option choice, or training-loop uses of SCS/SASD/IPR/PSC. fileciteturn0file5 fileciteturn0file8

## Executive decision summary

The package’s main pipeline problem is not that the framework specs are internally incoherent; it is that several essential **admission and lookup contracts** are missing or under-specified between “files on disk” and “trajectories seen by training.” The highest-priority fixes are therefore administrative but technically strict: add a post-metrics trajectory-admission gate keyed to parse success, finite arrays, monotone time, `N_t >= 2`, and `final_timestep >= 9.5`; replace all dense-index assumptions with explicit scanned manifests keyed by physical IC and realization variant; and make blacklist consumption mandatory and fail-closed. Those three changes resolve the most serious ingestion ambiguities without touching any locked physics conventions. fileciteturn0file8 fileciteturn0file6 fileciteturn0file1

On missing gold counterparts, the cleanest resolution is a **third option**, not either issue-doc candidate. Standard trajectories that lack a gold realization should remain in their already-admitted low-fidelity replay pool and be marked `gold_available = false`; they should **not** be relabeled as Stage 5 and should **not** be remapped to Stage 6 merely because a higher-resolution realization is absent. That recommendation follows directly from the curriculum replay rule plus the existing Stage 5 and Stage 6 definitions, and it avoids inventing stage semantics that the package never authorized. fileciteturn0file1 fileciteturn0file6 fileciteturn0file5

On metadata and storage, the erratum matters. The canonical parser should treat Brutus footers as **full or absent**, not “full/partial/minimal,” and when absent it should infer only those fields that the package actually documents at folder level, while preserving per-field provenance. The canonical processed-training-data store should be HDF5, because HDF5 natively supports hierarchical groups and datasets and transparent compression/chunked I/O, whereas `.npy` is deliberately a single-array format and therefore works best only as a derivative cache or export rather than as the sole authoritative corpus. JSON can exist for human inspection, but not as the normative training store. fileciteturn0file7 fileciteturn0file6 fileciteturn0file1 citeturn2view0turn3view0turn3view2

On physics-side validation, the package already contains the decisive answers for the two known conflicts. The data pipeline must use the **locked** PHYS-01 raw-mass scale `D ≈ 4.6416`, not the issue doc’s `D = 6.694`, unless the entire framework is rewritten to mass fractions. Likewise, it must use the **locked** post-v1.3 SCS definition and gate: `ε_H = max |(H - H0)/H0|`, `SCS = log10(ε_H)`, reject if `SCS > -5`. For the three metrics that remain spec-silent, I recommend a data-side metric suite in scaled coordinates and normalized physical time: a robust SASD defined as a local turning-angle proxy and flagged at `max(SASD) > 0.5`; an IPR defined on cubic Hermite interpolation using the validation epsilon `1e-10`, sampled strictly at interior points; and a PSC defined over one invariant-space vector per trajectory so that it measures **coverage** rather than merely mirroring `dt_out` heterogeneity. fileciteturn0file8 fileciteturn0file1 fileciteturn0file2 fileciteturn0file3 citeturn3view5turn4view0turn7calculator1

I checked the full recommendation set for internal consistency. No recommendation here alters the 14D input contract, the Jacobi `IC13`, the COM-projection contract, the dual-epsilon split, the locked SCS gate, or the locked PHYS-01 scale. The only places where confidence stays below High are the thresholds for SASD and IPR and the exact PSC construction, because the package provides no authoritative empirical calibration for them and Phase-24 verification has not yet supplied the corresponding distributions. fileciteturn0file8 fileciteturn0file1 fileciteturn0file3 fileciteturn0file2

## Decision matrix

The table below is an index to the detailed, cited resolutions that follow.

| Question ID | One-line verdict | Confidence |
|---|---|---|
| Q-A1 | Add a post-metrics admission gate using parse sanity, finite arrays, monotone time, `N_t >= 2`, and `final_timestep >= 9.5`; reject a fixed `>= 200` snapshot floor. | High |
| Q-A2 | Replace `ID == index` with explicit scanned manifests keyed by `ic_key = (family, traj_id)` and `traj_key = (family, variant, traj_id)`. | High |
| Q-A3 | Make blacklist loading mandatory, fail closed if absent or malformed, and exclude all fidelity variants of a blacklisted IC. | High |
| Q-A4 | Do not invent a fallback stage; retain missing-gold IDs only in their existing low-fidelity replay pool and mark `gold_available = false`. | Medium |
| Q-A5 | Treat footers as optional metadata with `footer_state ∈ {full, absent}`; use folder defaults plus per-field provenance when absent. | High |
| Q-A6 | Use HDF5 as the canonical processed-training-data store; allow `.npy` only as a derived cache/export; JSON is inspection-only. | High |
| Q-B1 | Keep 32 as a target, not an invariant: use `n_pts = max(2, min(32, floor(0.5 * N_t)))`. | Medium |
| Q-B2 | Compare IC masses to Brutus `t=0` masses on every trajectory with float64 `rtol=1e-15`, then reparse only failures with exact decimal literals. | High |
| Q-B3 | Float64 is sufficient for validation metrics and invariants; exact decimal parsing is needed only for literal mass-consistency fallback. | High |
| Q-B4 | Use the locked raw-mass `D = (G T^2)^(1/3) ≈ 4.6416`; reject `D = 6.694` within v1.4. | High |
| Q-C1 | Use locked SCS: compute raw Hamiltonian drift with validation epsilon, log it, reject if `SCS > -5`. | High |
| Q-C2 | Define SASD as a local turning-angle proxy on scaled data; flag if `max(SASD) > 0.5`. | Medium |
| Q-C3 | Define IPR with cubic Hermite interpolation in scaled units and validation epsilon `1e-10`; sample interior points only; flag if `IPR > 1e-3`. | Medium |
| Q-C4 | Define PSC over one invariant-space vector per trajectory using quantile-bin Shannon entropy, and report a companion near-collision coverage statistic. | Medium |

## Cluster A resolutions

**Q-A1 — Stage 4 → Stage 5 validation gate**

**Verdict / recommendation.** Yes. A completeness and validity gate should sit between metric generation and any training manifest or DataLoader build. The gate should admit a trajectory **iff** parsing succeeded, all parsed arrays are finite, snapshot times are strictly increasing, `N_t >= 2`, and `final_timestep >= 9.5`. Footer presence must **not** be required, and a fixed snapshot floor such as `>= 200` should **not** be part of the canonical gate. fileciteturn0file6 fileciteturn0file1

**Reasoning.** The only grounded completeness rule in the package is the README-style `final_timestep >= 9.5` check, and the same source explicitly warns against relying on line-count thresholds or a particular `Result:` footer schema. The parser contract also already treats files with fewer than two snapshots as incomplete/short. By contrast, the `>= 200` proposal appears only as a non-authoritative issue-doc recommendation summarized in the framed questions, while the package simultaneously marks the snapshot-count figures CLM-10 as `claimed-unverified` and warns against hard-coding them. A fixed 200-snapshot floor would therefore rest on the very sort of brittle count assumption the package tells the researcher not to trust. fileciteturn0file8 fileciteturn0file6 fileciteturn0file5 fileciteturn0file1

**Evidence.** `consolidated-context.md`, *Completeness Checks* and *Snapshot count warning*, grounds `final_timestep >= 9.5` and warns against line-count thresholds; `ctl_instruction.md`, Step 1, item 3, says short/incomplete files with fewer than two snapshots should return empty arrays and warnings; `claims-table.md` marks CLM-10 and the prevalence part of CLM-11 as unverified; and `framed-research-questions.md` presents the `>= 200` floor only as a non-authoritative issue-doc proposal. fileciteturn0file6 fileciteturn0file1 fileciteturn0file5 fileciteturn0file8

**Confidence.** High. The main thing that would change this answer would be a later authoritative spec that intentionally trains on truncated trajectories or explicitly promotes a stage-specific absolute snapshot floor; the current package contains neither. fileciteturn0file8 fileciteturn0file6

**Verification suggestion.** Run the admission gate across the current corpus and publish rejection counts by variant and by failure reason (`parse_failed`, `nonfinite`, `nonmonotone_time`, `Nt_lt_2`, `final_timestep_lt_9p5`). The important audit output is the reason histogram, not just a pass/fail total. 

**Proposed specification text.** Add a short subsection immediately after `ctl_instruction.md` Step 1: “Before any trajectory is eligible for invariant computation, metric-based validation, stage assignment, or training, require: successful IC/BRUTUS parse; finite parsed arrays; strictly increasing times; `N_t >= 2`; and `final_timestep >= 9.5`. `Result:` footer presence is not a completeness requirement. Reject or quarantine trajectories that fail any condition and record the first failing reason in metadata.” Anchor: `ctl_instruction.md`, immediately after *Step 1: Parse Raw Simulation Data*. fileciteturn0file1

**Q-A2 — Non-contiguous IDs**

**Verdict / recommendation.** The canonical mapping contract should separate the **physical initial condition** from the **realization on disk**. Use `ic_key = (family, traj_id)` for the physical IC and `traj_key = (family, variant, traj_id)` for an actual trajectory file, where `family ∈ {hierarchical, standard}` and `variant ∈ {base, gold}`. Build all lookups by scanning filenames in each folder and extracting the numeric ID; never use array position as a surrogate for ID. fileciteturn0file6 fileciteturn0file8

**Reasoning.** The package already says numeric IDs are not contiguous and are not indices. The erratum strengthens that conclusion by removing filename-based gold discrimination on the Brutus side: gold status is encoded by **folder name only**, not by a `_gold_` filename infix. Therefore a robust loader cannot treat “the fourth file in an array” or “a filename prefix” as canonical identity. The right abstraction is a dual-key manifest: one key for the physical IC, because stage assignment and blacklisting happen at IC level, and one key for each concrete realization, because base and gold trajectories are different stored artifacts of the same physical system. The exact sizes of CLM-01 and CLM-02 do not change that logic; any non-zero gap rate already invalidates dense-index semantics. fileciteturn0file6 fileciteturn0file7 fileciteturn0file5

**Evidence.** `consolidated-context.md`, *File Naming Conventions and Mapping*, states that numeric ID is not an index; `ERRATUM-2026-06-10.md`, *Correction 1*, says gold Brutus files carry no `_gold_` infix and that folder name alone encodes gold status; and `framed-research-questions.md`, Q-A2, identifies dense indexing as the open failure mode. fileciteturn0file6 fileciteturn0file7 fileciteturn0file8

**Confidence.** High. The only thing that would materially change this answer would be a revised dataset layout in which IDs become dense and immutable array order is made authoritative; the current package says the opposite. fileciteturn0file6

**Verification suggestion.** Build a manifest generator that scans all four Brutus directories and emits: `(family, variant, traj_id, path, footer_state, final_timestep)`. Then check three invariants: no duplicate `traj_key`; all `traj_id` extractions are consistent across base/gold folders; and all stage/blacklist lookups are performed against explicit keys rather than list offsets.

**Proposed specification text.** Add to `ctl_instruction.md` metadata contract: “Maintain two canonical identifiers. `ic_key = (family, traj_id)` identifies the physical initial condition. `traj_key = (family, variant, traj_id)` identifies one on-disk trajectory realization. Build both from scanned folder contents. Numeric ID is an identifier, not an array index; list position must never be used as an ID surrogate.” Anchor: `ctl_instruction.md`, in or immediately after *Step 2.6 Assertions and stored metadata*. fileciteturn0file1

**Q-A3 — Blacklist loading and consumption**

**Verdict / recommendation.** Blacklist loading should be mandatory at dataset-manifest/DataLoader initialization, and blacklist enforcement should happen at `ic_key` granularity. A blacklisted `(family, traj_id)` must exclude **all** realizations of that IC, including both base and gold variants. A missing or malformed blacklist file should be treated as a fatal configuration error unless a user explicitly disables blacklist enforcement in a visible override. The loader should emit exclusion counts by family and variant. fileciteturn0file8 fileciteturn0file6

**Reasoning.** The risk named in Q-A3 is not merely “there exists a file called blacklist”; it is that problematic ICs could silently enter training. The blacklist is about **initial conditions**, not about one particular resolution artifact. That matters because gold/base pairs represent the same physical IC when both exist: the standard gold ICs are documented as a byte-identical subset of the standard ICs, and the curriculum description explicitly reuses the same systems across low- and high-resolution refinement stages. Excluding only one realization would therefore not solve the underlying contamination problem. This answer does **not** depend on the exact blacklist count CLM-03, which remains claimed-unverified. fileciteturn0file6 fileciteturn0file1 fileciteturn0file5

**Evidence.** `consolidated-context.md`, *Blacklist Summary*, gives the blacklist’s family-level structure; the same file’s *standard IDs not in gold* section says gold-standard standard ICs are a byte-identical subset of the standard ICs; and `ctl_instruction.md` describes Stage 2 as high-resolution refinement of the same physical systems used earlier, which supports handling blacklist semantics at IC level rather than at one realization only. Q-A3 in the framed questions correctly notes that blacklist consumption itself is spec-silent and therefore needs a contract. fileciteturn0file6 fileciteturn0file1 fileciteturn0file8

**Confidence.** High. The answer would change only if the project were to reclassify the blacklist as advisory rather than exclusionary, or if future documentation established that some listed IDs are resolution-specific rather than IC-specific. The current package supports neither interpretation. fileciteturn0file6 fileciteturn0file8

**Verification suggestion.** Add a manifest audit that prints `(family, variant)` exclusion counts and the first few excluded IDs, then verify that a blacklisted `ic_key` cannot be retrieved by any path-based lookup. A regression test should assert that disabling blacklist enforcement requires an explicit runtime flag and produces a warning banner.

**Proposed specification text.** Add to `ctl_instruction.md`: “Load `problematic_ics_blacklist.json` at manifest/DataLoader initialization. Interpret blacklist entries at `ic_key` granularity and exclude every realization whose `(family, traj_id)` matches a listed ID, including base and gold variants. A missing or malformed blacklist file is a fatal configuration error unless the user explicitly disables blacklist enforcement. Persist exclusion counts in loader metadata and logs.” Anchor: `ctl_instruction.md`, after the proposed `Trajectory admission gate` addition. fileciteturn0file1

**Q-A4 — Standard IDs without gold counterparts**

**Verdict / recommendation.** The correct policy is a third option: do **not** synthesize a fallback stage. If a `standard` `ic_key` lacks a gold realization, retain its low-fidelity trajectory only in the stage/replay pool to which it already belongs, set `gold_available = false`, and do not create a synthetic Stage-5 sample. Also do not remap the trajectory to Stage 6 solely because its gold counterpart is absent. fileciteturn0file1 fileciteturn0file6

**Reasoning.** Both issue-doc candidate fallbacks conflict with the existing curriculum semantics. Admitting a low-fidelity standard sample as if it were Stage 5 would contradict Stage 5’s explicit definition as **high-resolution** chaotic data. Remapping a non-gold sample to Stage 6 would contradict Stage 6’s explicit physics criteria (`s_min < 0.5` or `|E| < 0.01`) by replacing them with an administrative criterion (“gold missing”). The package’s own replay rule provides a cleaner answer: later stages include all earlier-stage data. So a missing-gold IC need not be “forced” anywhere new; it simply remains represented by its already-admitted low-fidelity realization. The verified number 184 matters operationally, but it does not alter the logic of the policy. fileciteturn0file1 fileciteturn0file6 fileciteturn0file5

**Evidence.** `ctl_instruction.md` defines Stage 5 as high-resolution chaotic simulations and Stage 6 by explicit near-collision/extreme-case criteria; the same document also states that each later stage replays all earlier data. `consolidated-context.md` verifies that 184 standard IDs lack gold counterparts and that the gold subset is a subset, not a replacement corpus. The framed questions themselves flag this as a STOP-gap candidate if the package cannot support a principled fallback; replay avoids inventing a synthetic stage and therefore resolves the gap without violating the curriculum. fileciteturn0file1 fileciteturn0file6 fileciteturn0file8 fileciteturn0file5

**Confidence.** Medium. The most important factor that could change this answer would be a later curriculum/training-loop specification in doc-03 that explicitly requires every Stage-5-class IC to have a high-resolution refinement sample and therefore redesigns the stage semantics around that requirement. The current package does not. fileciteturn0file8 fileciteturn0file1

**Verification suggestion.** Add a report for every Stage-5-eligible `ic_key` with columns `gold_available`, `low_fidelity_stage`, and `replay_only`. Then verify that Stage 5 introduces only the subset with `gold_available = true` while later-stage replay still includes the existing low-fidelity realizations.

**Proposed specification text.** Add a note under the Stage 5 description in `ctl_instruction.md`: “If a `standard` IC has no gold-resolution realization, retain its admitted low-fidelity trajectory in its previously assigned low-fidelity stage/replay pool and record `gold_available = false`. Do not relabel the low-fidelity trajectory as Stage 5, and do not remap it to Stage 6 solely because its gold realization is absent.” Anchor: `ctl_instruction.md`, immediately after *Stage 5: High-Resolution Chaotic Orbits*. fileciteturn0file1

**Q-A5 — Footer and parameter heterogeneity**

**Verdict / recommendation.** The canonical footer contract should be binary: `footer_state ∈ {full, absent}`. When `footer_state = full`, parse available parameter fields directly from the `Result:` footer. When `footer_state = absent`, infer `tol` and `dt_out` from folder defaults and record per-field provenance; set `eta = null`; and infer `word_length` only if the variant has a unique authoritative value for that absent-footer population, otherwise leave it null. Footer presence must remain irrelevant to completeness. fileciteturn0file7 fileciteturn0file6

**Reasoning.** The erratum materially changes this question. After correction, the package no longer supports a three-way distinction between full, partial, and minimal footers for the affected populations; it supports **full** versus **no footer at all**. That simplifies the parser and should also simplify provenance. The correct default tolerances and sampling intervals are already documented by variant. But the package does **not** justify blindly backfilling every missing field for every variant: `eta` is absent when the footer is absent; and `word_length` is not equally well-documented across all absent-footer variants. The parser should therefore infer only what the package truly supports and preserve provenance at field level, not pretend to know more than it does. fileciteturn0file7 fileciteturn0file6 fileciteturn0file5

**Evidence.** `ERRATUM-2026-06-10.md`, *Correction 2*, states that exactly 1,550 hierarchical-base files, 701 standard-base files, and 219 standard-gold files have no `Result:` line and no parameter fields anywhere in the file, and that folder defaults must be assumed for them. The erratum also says CLM-09, CLM-07’s count, CLM-08, and all full-schema tuples remain correct. `consolidated-context.md` gives the verified folder defaults for `tol` and `dt_out`. The framed questions correctly describe the original problem as spec-silent metadata handling rather than as a completeness rule. fileciteturn0file7 fileciteturn0file6 fileciteturn0file8

**Confidence.** High. The main thing that would change this answer would be additional authoritative documentation supplying a unique folder-default `word_length` for the standard-base absent-footer subset; that would let the parser fill one more field rather than leave it null. fileciteturn0file7 fileciteturn0file6

**Verification suggestion.** For every variant, emit counts by `footer_state` and by parameter provenance (`footer`, `folder_default`, `variant_unique`, `missing`). Then spot-check that completeness rejections come only from the admission gate in Q-A1, never from `footer_state = absent`.

**Proposed specification text.** Add to the Step 1 parser contract in `ctl_instruction.md`: “Treat Brutus `Result:` footers as optional metadata. Store `footer_state ∈ {full, absent}`. When `full`, parse `tol`, `word_length`, `dt_out`, `t_end`, and `eta` directly. When `absent`, infer only those fields that have authoritative folder-level defaults; set unsupported fields to null. Record per-field provenance and do not use footer presence as a completeness condition.” Anchor: `ctl_instruction.md`, Step 1, item 3 and item 4. fileciteturn0file1

**Q-A6 — Processed training-data format**

**Verdict / recommendation.** The framework should treat HDF5 as the canonical processed-training-data store. `.npy` is acceptable only as a derived cache/export format that preserves an already-defined schema, not as the sole authoritative corpus. JSON may exist for inspection/debugging only and should never be the canonical training source. This is primarily a storage and loader-contract decision, not a physics-methodology decision. fileciteturn0file1 fileciteturn0file8

**Reasoning.** The package’s own authoritative spec already prefers HDF5 or `.npy`, so the main question is which should be canonical. HDF5 is the better answer for this corpus because it natively offers a hierarchy of groups and datasets and supports transparent storage features such as compression and chunked I/O; that matches a trajectory corpus containing arrays of times, positions, velocities, metadata, flags, and stage assignments. By contrast, NumPy’s `.npy` format is intentionally the standard binary format for a **single** array; a `.npy`-only canonical corpus would therefore require either many sidecar files or an external manifest to recover one trajectory’s full state. That makes `.npy` useful as a deterministic cache layer, but a weaker choice as the single normative store. fileciteturn0file1 citeturn2view0turn3view0turn3view2

**Evidence.** `ctl_instruction.md`, Step 1 item 6, recommends HDF5 or `.npy` for processed training data. The framed questions summarize the issue doc’s own conclusion that HDF5 primary with optional inspection export is methodologically non-disruptive. The h5py documentation describes HDF5 groups as dictionary-like containers and HDF5 datasets as NumPy-like arrays with compression and chunked I/O support; the NumPy format documentation says `.npy` persists a single arbitrary array and `.npz` is the multi-array wrapper. fileciteturn0file1 fileciteturn0file8 citeturn2view0turn3view0turn3view2

**Confidence.** High. This answer would change mainly if the project had a non-negotiable tooling or deployment constraint against HDF5 libraries; the package does not report such a constraint. 

**Verification suggestion.** Prototype one trajectory corpus both ways: an HDF5 store with one group per `traj_key`, and a `.npy` family of sidecar files carrying the same fields. Compare schema clarity, manifest complexity, and deterministic reconstruction of one sample.

**Proposed specification text.** Revise `ctl_instruction.md`, Step 1 item 6, to read in substance: “Use HDF5 as the canonical processed-training-data container, with one group per `traj_key` and datasets/attributes for arrays and metadata. A `.npy`-based export/cache is acceptable only if it preserves the identical schema and is treated as derived output. JSON export is optional for debugging/inspection only and is not a training source.” Anchor: `ctl_instruction.md`, Step 1 item 6. fileciteturn0file1

## Cluster B resolutions

**Q-B1 — Points-per-trajectory feasibility**

**Verdict / recommendation.** The batch contract should treat 32 as a **target**, not an invariant. Define `N_t` as the actual post-admission snapshot count for one trajectory and set  
`n_pts = max(2, min(32, floor(0.5 * N_t)))`.  
Sample those `n_pts` points without replacement within the trajectory. This preserves the existing “32 points” intent for high-resolution trajectories while avoiding brittle hard-coding for lower-resolution ones. fileciteturn0file1 fileciteturn0file8

**Reasoning.** The existing spec names “32” as an example batch point count, while the dataset-side documents simultaneously warn that exact snapshot counts should not be hard-coded. The low-resolution standard trajectories are described only approximately, and CLM-10 remains claimed-unverified. In that setting, the safest contract is one that keys off **actual** `N_t`, not a claimed per-variant constant. The `0.5 * N_t` cap is a reasonable conservative bound because it prevents low-resolution trajectories from being sampled so densely that almost every snapshot is consumed in one batch, while leaving higher-resolution trajectories unchanged at the 32-point target. This answer is consistent with Q-A1: once completeness is enforced by `final_timestep >= 9.5` and `N_t >= 2`, no separate absolute floor is needed here. fileciteturn0file6 fileciteturn0file5 fileciteturn0file1

**Evidence.** `ctl_instruction.md`, *Mini-Batch Construction with Lookahead Sampling*, gives `n_pts` “e.g., 32”; `consolidated-context.md` warns against hard-coding exact snapshot counts; and Q-B1 in the framed questions presents the adaptive-cap proposal precisely because the batch section is otherwise spec-silent on a variant-aware rule. fileciteturn0file1 fileciteturn0file6 fileciteturn0file8

**Confidence.** Medium. The most important factor that could change this answer would be a Phase-24 snapshot distribution showing that post-gate standard trajectories routinely have so many snapshots that fixed-32 sampling is harmless, or so few that even the `0.5 * N_t` heuristic needs refinement. fileciteturn0file5

**Verification suggestion.** Compute the empirical distribution of `N_t` after the Q-A1 admission gate, then report what fraction of trajectories would receive `n_pts = 32`, `n_pts < 32`, and `n_pts < 8` under the proposed rule.

**Proposed specification text.** Replace the current open-ended “`n_pts` (e.g., 32)” phrasing in `ctl_instruction.md` with: “Let `N_t` be the actual snapshot count after the trajectory admission gate. Set `n_pts_target = 32` and `n_pts = max(2, min(n_pts_target, floor(0.5 * N_t)))`. Sample those points without replacement.” Anchor: `ctl_instruction.md`, *Mini-Batch Construction with Lookahead Sampling*. fileciteturn0file1

**Q-B2 — Footer and mass-drift protocol**

**Verdict / recommendation.** The pipeline should require an **every-trajectory** IC↔Brutus mass-consistency check, not merely a one-off 1000-pair audit. Compare the three masses in the IC file with the three masses in the Brutus `t=0` snapshot **before** canonical reordering, using float64 parse space and `rtol = 1e-15`, `atol = 0`. If that comparison fails, reparse just those six literals from the original text strings with exact decimal arithmetic; accept the trajectory only if the decimal values match exactly, otherwise quarantine it. fileciteturn0file1 fileciteturn0file8

**Reasoning.** The package already contains the essential technical requirement in Step 2.1: mass invariance across the trajectory must hold to `1e-15` in float64 parse space, and COM corrections require consistent masses between IC and Brutus output. Once that contract exists, a mere sample-based audit is too weak as the **normative** pipeline rule. The sample audit remains useful as a verification exercise, but the loader/parser can cheaply compare all six mass literals on every trajectory. Because the decimal fallback is needed only for three IC masses and three Brutus literals, the exact-parsing cost is negligible. fileciteturn0file1 fileciteturn0file8 citeturn3view4

**Evidence.** `ctl_instruction.md`, Step 2.1, requires `max_t,i |m_i(t) - m_i(0)| < 1e-15` and explicitly ties that gate to COM/mass consistency. Q-B2 in the framed questions presents the sample-based `np.allclose(rtol=1e-15)` plus Decimal fallback as a non-authoritative candidate protocol. The Python decimal documentation confirms that the module supports exact unrounded decimal arithmetic when the programmer needs literal decimal control. fileciteturn0file1 fileciteturn0file8 citeturn3view4

**Confidence.** High. The answer would change only if Phase-24 testing showed that float64 parsing never fails and the project chose to remove the decimal fallback for simplicity; even then the every-trajectory float64 check would remain appropriate. 

**Verification suggestion.** Implement the float64 comparison on every trajectory and log how often the decimal fallback triggers. If it never triggers on the full corpus, the project can later simplify operationally while retaining the same semantic contract.

**Proposed specification text.** Add to `ctl_instruction.md`, Step 2.1: “For every trajectory, compare the IC masses against the Brutus `t=0` masses in raw file order using float64 parse space and `rtol = 1e-15`, `atol = 0`. If this comparison fails, reparse only the six mass literals with exact decimal arithmetic and accept only if the decimal values match exactly; otherwise quarantine the trajectory.” Anchor: `ctl_instruction.md`, *Parser contract and mass-invariance check*. fileciteturn0file1

**Q-B3 — Precision handling**

**Verdict / recommendation.** Float64 is sufficient for all validation metrics and invariant calculations in the current framework. Exact decimal parsing is required only for the literal mass-consistency fallback in Q-B2, or for future audit tasks whose acceptance thresholds move close to text-rounding limits. Positions, velocities, times, SCS, SASD, IPR, PSC, and invariant calculations should remain float64. fileciteturn0file1 fileciteturn0file3

**Reasoning.** The locked validation gate rejects only at `ε_H > 10^-5`, while float64 machine epsilon is about `2.22e-16`; that is more than ten orders of magnitude of headroom relative to the reject threshold. The validation-side softening/invariant scale is `1e-10`, which is still far above machine epsilon. For the three-body problem, the metric formulas involve only a small number of arithmetic operations per snapshot, so float64 parse error is not the dominant uncertainty for these gates. Exact decimal arithmetic becomes useful only when the question is literal decimal identity of mass strings rather than physically meaningful metric precision. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1 fileciteturn0file3 citeturn3view3turn7calculator0turn3view4

**Evidence.** CLM-09 gives Brutus tolerances of `1e-15` (hierarchical base) and `1e-13` (standard base and gold defaults); the framed questions lock validation epsilon at `1e-10` and the SCS reject gate at `1e-5`; NumPy documents float64 epsilon as approximately `2.22e-16`; and Python’s decimal module documents exact decimal arithmetic and user-controlled precision. fileciteturn0file5 fileciteturn0file8 citeturn3view3turn3view4

**Confidence.** High. The main factor that would change this answer would be a future tightening of validation thresholds into the `1e-12` or smaller regime, where parse precision rather than physics might start to matter operationally. 

**Verification suggestion.** Recompute a representative set of SCS and invariant values in both float64 and a high-precision reference implementation for a small audit subset, and report the maximum absolute and relative discrepancies versus the operational thresholds.

**Proposed specification text.** Add to `ctl_instruction.md`, Step 2.1 or immediately after it: “Use float64 for parsing positions, velocities, times, invariants, and validation metrics. Reserve exact decimal parsing for literal mass-consistency fallback or for explicitly requested audit tasks. Do not promote the full validation pipeline to arbitrary precision by default.” Anchor: `ctl_instruction.md`, after the Q-B2 addition. fileciteturn0file1

**Q-B4 — Global scale `D`**

**Verdict / recommendation.** The data pipeline must use the locked PHYS-01 raw-mass scale  
`D = (G T^2)^(1/3) ≈ 4.6416`  
and must **not** use `D = (G M_tot T^2)^(1/3) = 6.694` within v1.4. The latter is mathematically admissible only under a full mass-fraction rewrite of residual, Hamiltonian, angular momentum, COM projection, and invariant formulas, which is out of scope and incompatible with the current hard constraints. fileciteturn0file1 fileciteturn0file8

**Reasoning.** This is not an open empirical question inside the current package; it is a locked convention conflict. The scaling derivation in `ctl_instruction.md` explicitly uses raw masses in the dimensionless residual and explicitly rejects the `6.694` form except under a mass-fraction rewrite. The same raw-mass choice propagates elsewhere: the `IC13` mass entries are raw masses, and the COM projection head uses ordered raw masses supplied by preprocessing rather than normalized mass channels. Adopting `6.694` without rewriting those contracts would therefore create a mixed convention, not a harmless helper-function change. fileciteturn0file1 fileciteturn0file3 fileciteturn0file5

**Evidence.** `ctl_instruction.md`, *Global scaling* and *Network input contract*, gives the raw-mass derivation and explicitly rejects the `6.694` form; `pinn_architecture.md`, *Output Layer*, says the COM projection uses ordered raw masses from preprocessing; and CLM-13 is explicitly classified in `claims-table.md` as a contested convention claim rather than as a dataset fact. The framed questions also identify this as a known conflict with a locked counter-position. fileciteturn0file1 fileciteturn0file3 fileciteturn0file5 fileciteturn0file8

**Confidence.** High. The only thing that would change this answer would be an explicit project decision to rewrite the whole framework to mass fractions. That would be a different framework, not a data-pipeline patch.

**Verification suggestion.** Re-derive the dimensionless residual once from raw-mass scaling and once from mass-fraction scaling and confirm that only the raw-mass derivation leaves the current residual and IC/COM contracts unchanged.

**Proposed specification text.** Add one sentence to `ctl_instruction.md`, *Global scaling*: “Any helper that computes dataset-wide scales or normalization constants inherits PHYS-01 unchanged; helpers using `D = cbrt(G * M_tot * T^2)` are invalid unless the entire framework is rewritten to mass fractions.” Anchor: `ctl_instruction.md`, immediately after the existing PHYS-01 paragraph. fileciteturn0file1

## Cluster C resolutions

**Q-C1 — Symplectic Conservation Score**

**Verdict / recommendation.** The canonical SCS contract is the locked post-v1.3 one: compute  
\[
\epsilon_H = \max_n \left|\frac{H_{\mathrm{inv}}(u_n)-H_{\mathrm{inv}}(0)}{H_{\mathrm{inv}}(0)}\right|,
\qquad
SCS = \log_{10}(\epsilon_H),
\]
where `H_inv` is the validation-side Hamiltonian computed in scaled coordinates with `ε_inv = 1e-10`. Reject the trajectory if `SCS > -5` (equivalently `ε_H > 10^-5`). If `H_inv(0)` is numerically near zero, set `SCS_status = undefined` and quarantine for manual review rather than forcing the logarithm. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1

**Reasoning.** The issue-doc position and the locked framework do not differ merely by threshold value; they differ by **what SCS is**. The issue doc uses raw drift and calls it “SCS,” whereas the locked post-v1.3 policy distinguishes raw drift `ε_H` from its logarithmic score `SCS = log10(ε_H)`. Because the framed questions elevate the post-v1.3 DQA correction SI-DQA-003 into the hard constraints, the raw-ratio thresholds cannot be the canonical contract inside this package. Variant-specific tightening such as `1e-8` for gold data is therefore not available here unless the locked policy is changed downstream; within v1.4, the reject gate is `SCS > -5`. fileciteturn0file8 fileciteturn0file2

**Evidence.** `data_quality_assessment.md`, SI-DQA-003 and Section 3.1, defines `ε_H`, `SCS`, and the reject gate `SCS > -5`; `framed-research-questions.md` repeats that lock as Hard Constraint 5 and explicitly notes the raw-ratio/log-drift mismatch; and `ctl_instruction.md`, Step 3, fixes `ε_inv = 1e-10` for offline invariant-side energy calculations. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1

**Confidence.** High. The only thing that would change this answer would be a later ratified replacement of SI-DQA-003. Absent that, this one is effectively fixed by the package.

**Verification suggestion.** Recompute `ε_H` and `SCS` for a representative subset and verify that the implementation can reproduce the equivalence `ε_H > 10^-5 ⇔ SCS > -5`, plus the undefined-when-`H0≈0` branch.

**Proposed specification text.** Add a new data-side subsection to `ctl_instruction.md` after Step 3, titled *Trajectory validation metrics*: “Define validation-side Hamiltonian drift as `ε_H = max_n |(H_inv(u_n)-H_inv(0))/H_inv(0)|` using the scaled invariant-side Hamiltonian with `ε_inv = 1e-10`. Define `SCS = log10(ε_H)`. If `|H_inv(0)|` is numerically near zero, mark the trajectory `SCS_undefined`. Reject if `SCS > -5`.” Anchor: `ctl_instruction.md`, after Step 3. fileciteturn0file1

**Q-C2 — Stiffness-Aware Sampling Density**

**Verdict / recommendation.** Define SASD in the canonical scaled variables as a local turning-angle proxy:
\[
SASD_i
=
\Delta u_i\;
\frac{\|a'_{\perp,i}\|}{\max(\|v'_i\|, v_{\mathrm{floor}})},
\qquad
a'_{\perp,i}
=
a'_i - \frac{a'_i\!\cdot v'_i}{\|v'_i\|^2}\,v'_i,
\]
with `Δu_i = u_{i+1}-u_i`, validation-force accelerations computed using `ε_inv = 1e-10`, and `v_floor = 1e-12` in scaled units. Flag a trajectory for higher-resolution resimulation or explicit reviewer attention if `max_i SASD_i > 0.5`. Do not auto-reject on SASD alone. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1

**Reasoning.** The package offers the raw form `Δt ||a|| / ||v||` and notes that a curvature-based variant is more robust. The perpendicular-acceleration version is the stronger data-side choice because it measures how sharply the trajectory **turns**, not merely how fast its speed changes. Under the PHYS-01 scaling, this quantity is invariant to whether one writes it in raw variables or in scaled coordinates and normalized time. A threshold of `0.5` corresponds to a local directional change of about `28.65°` over one output interval, which is a reasonable point at which interpolation between snapshots becomes suspect. The package has no authoritative empirical calibration for that threshold, so I adopt the DQA report’s `0.5` flag as the least-speculative operational rule and keep confidence at Medium. fileciteturn0file2 fileciteturn0file1 citeturn7calculator1

**Evidence.** `data_quality_assessment.md`, Section 3.2, defines `SASD_i = Δt_i ||a|| / ||v||`, notes the curvature/radius-of-curvature refinement, and recommends flagging `max(SASD) > 0.5`; `framed-research-questions.md` treats SASD as spec-silent and asks for the data-side definition only; and `ctl_instruction.md` provides the scaling identities that make the scaled-time form equivalent to the raw-time form. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1

**Confidence.** Medium. The most important factor that would change this answer would be empirical calibration against actual Phase-24 trajectories and overfit outcomes showing that `0.5` is too lax or too strict for this dataset’s admitted resolution profile. 

**Verification suggestion.** Compute intervalwise SASD profiles on a stratified sample of admitted trajectories, then compare flagged intervals against visual close-encounter segments and against later IPR values. That will show whether the `0.5` threshold is well placed.

**Proposed specification text.** In the new `ctl_instruction.md` subsection *Trajectory validation metrics*, add: “For each snapshot interval `i`, define `Δu_i = u_{i+1}-u_i` and compute validation-force acceleration `a'_i` with `ε_inv = 1e-10`. Let `a'_{\perp,i}` be the component of `a'_i` perpendicular to `v'_i`. Define `SASD_i = Δu_i * ||a'_{\perp,i}|| / max(||v'_i||, 1e-12)`. Flag the trajectory for reviewer attention or higher-resolution data if `max_i SASD_i > 0.5`.” Anchor: `ctl_instruction.md`, new *Trajectory validation metrics* subsection. fileciteturn0file1

**Q-C3 — Interpolation Physics Residual**

**Verdict / recommendation.** Define the data-side IPR in the same scaled coordinates and normalized physical time used elsewhere in the framework, with the **validation** epsilon `ε_inv = 1e-10`, not the training epsilon `1e-5`. For each Cartesian component, build a cubic Hermite spline from `(u_n, r'_n, v'_n)` and evaluate the mean squared residual at 10 **interior** points per interval:
\[
IPR
=
\frac{1}{M}\sum_{k=1}^{M}\frac{1}{3}\sum_{i=1}^{3}
\left\|
\frac{d^2 r'_{\mathrm{spline},i}}{du^2}(u_k)
-
\sum_{j\ne i}
m_j\,
\frac{r'_{\mathrm{spline},j}(u_k)-r'_{\mathrm{spline},i}(u_k)}
{\left(\|r'_{\mathrm{spline},j}(u_k)-r'_{\mathrm{spline},i}(u_k)\|^2+\epsilon_{\mathrm{inv}}^2\right)^{3/2}}
\right\|^2.
\]
Flag the trajectory as aliased if `IPR > 1e-3`. fileciteturn0file8 fileciteturn0file1 fileciteturn0file2

**Reasoning.** The package’s “cubic Hermite” instinct is right, but the implementation detail matters. Because the dataset already provides velocities, the correct interpolation object is a **cubic Hermite spline with supplied derivatives**, not a derivative-estimating monotone interpolant. SciPy’s `CubicHermiteSpline` is explicitly “piecewise cubic” and fits values **and first derivatives**. Also, because piecewise cubic Hermite interpolants are only `C^1`, second derivatives should be sampled **strictly inside** each interval rather than at knots. On epsilon, the hard constraint is clear: data-side validation metrics use the static validation epsilon, while `ε_train = 1e-5` is reserved for the network’s training residual and matched-Plummer training Hamiltonian. The package’s proposed `1e-3` gate is not a locked convention, so I adopt it with Medium confidence as a practical starting point rather than as a fully ratified law. fileciteturn0file8 fileciteturn0file3 fileciteturn0file1 fileciteturn0file2 citeturn3view5turn4view0

**Evidence.** `data_quality_assessment.md`, Section 3.3 and Section 5.1, proposes IPR, cubic-Hermite interpolation, `10` synthetic points per interval, and the `1e-3` flag; `framed-research-questions.md` asks explicitly which epsilon the data-side IPR should use under the dual-epsilon lock; `ctl_instruction.md`, Step 3, fixes `ε_inv = 1e-10` for offline invariant-side calculations; and `pinn_architecture.md`, Section 3.2 and Section 3.4, fixes `ε_train = 1e-5` for the training residual and matched-Plummer Hamiltonian. SciPy documents `CubicHermiteSpline` as a piecewise cubic interpolator that fits values and first derivatives, and documents piecewise-cubic Hermite constructions as only `C^1`, making interior-point evaluation the safer choice for second derivatives. fileciteturn0file2 fileciteturn0file8 fileciteturn0file1 fileciteturn0file3 citeturn3view5turn4view0

**Confidence.** Medium. The most important factor that would change this answer would be empirical evidence that `IPR > 1e-3` correlates poorly with actual aliasing or learnability on this corpus. The epsilon choice, however, is much firmer than the threshold choice. fileciteturn0file8

**Verification suggestion.** Compute IPR for a stratified sample across variants, then compare the flagged subset against visual trajectory plots and later training diagnostics. Also confirm numerically that using `ε_train` instead of `ε_inv` materially changes the metric, which would validate the importance of keeping the two versions conceptually separate.

**Proposed specification text.** In the proposed `ctl_instruction.md` *Trajectory validation metrics* subsection, add: “Construct a cubic Hermite spline for each Cartesian position component from the preprocessed scaled snapshots `(u_n, r'_n, v'_n)`. Sample 10 interior points per snapshot interval. Define `IPR` as the mean squared residual of spline acceleration against the validation-force law with `ε_inv = 1e-10`. Flag the trajectory as aliased if `IPR > 1e-3`. This is a data-side validation metric only; any training-loop use belongs to the later curriculum/training specification.” Anchor: `ctl_instruction.md`, new *Trajectory validation metrics* subsection. fileciteturn0file1

**Q-C4 — Phase Space Coverage Entropy**

**Verdict / recommendation.** Define PSC over **one representative vector per admitted trajectory**, not over all snapshots, using the invariant space already computed for staging:
\[
z_j
=
\left(
E_j/E_{\mathrm{scale}},
\,
L_{\mathrm{norm},j},
\,
Q_j/Q_{\mathrm{scale}},
\,
s_{\min,j}/s_{\min,\mathrm{scale}}
\right).
\]
For each coordinate, construct 8 equal-frequency bins from the admitted corpus, giving `K = 8^4` possible cells. Let `p_c = n_c/N` for occupied cell `c`. Define normalized coverage entropy as
\[
PSC
=
-\frac{1}{\log K}\sum_{c:n_c>0} p_c \log p_c.
\]
Report alongside it a companion near-collision coverage statistic  
\[
C_{\mathrm{near}}
=
\frac{1}{N}\sum_{j=1}^{N}\mathbf{1}\!\left[s_{\min,j}/s_{\min,\mathrm{scale}} < 0.5\right].
\]
Use PSC as a descriptive coverage score only in this document’s scope. fileciteturn0file1 fileciteturn0file2 fileciteturn0file8

**Reasoning.** The package proposes “phase-space coverage entropy” at a high level but leaves the state space unspecified. A snapshot-level entropy is a poor choice for this issue because snapshot counts vary strongly by `dt_out`, and the framed questions explicitly defer the training-loop consequences of that heterogeneity to doc-03. If PSC were computed over all snapshots, it would partly become a measure of output resolution rather than dataset diversity. Using one invariant-space vector per trajectory avoids that confound while remaining faithful to the package’s own staging variables. Equal-frequency rather than equal-width bins are the better default because they reduce sensitivity to heavily skewed marginals; normalized Shannon entropy then yields a score on `[0,1]` that is comparable across admitted-corpus audits using the same binning rule. The companion `C_near` preserves the DQA report’s emphasis on whether the hard near-collision region is actually represented. fileciteturn0file8 fileciteturn0file2 fileciteturn0file1 citeturn6view0

**Evidence.** `data_quality_assessment.md`, Section 3.4, defines PSC as a Shannon entropy over discretized phase-space occupancy and separately calls out special concern for the near-collision region. `ctl_instruction.md`, Step 3 and Step 2.5, already defines the invariant quantities and the scales `E_scale`, `Q_scale`, and `s_min,scale` needed for a low-dimensional coverage representation. `framed-research-questions.md` explicitly limits scope to the **data-side** PSC definition and excludes curriculum-replay usage, which reinforces the choice to avoid a snapshot-level metric that would entangle PSC with deferred `dt_out` policy. Shannon’s 1948 paper is the underlying source of the entropy form itself. fileciteturn0file2 fileciteturn0file1 fileciteturn0file8 citeturn6view0

**Confidence.** Medium. The most important factor that would change this answer would be a later decision that a different low-dimensional state description—such as pairwise-distance space or a specific Poincaré section—is scientifically preferable for the project’s downstream generalization questions. The package does not currently contain that choice. 

**Verification suggestion.** Compute PSC on the admitted corpus under the proposed invariant-space grid and compare it with two alternatives on a pilot basis: a pairwise-distance grid and a simple Poincaré-section proxy. If one alternative better tracks the project’s later generalization failures, revise PSC at the next milestone rather than in this issue.

**Proposed specification text.** In the proposed `ctl_instruction.md` *Trajectory validation metrics* subsection, add: “For data-side coverage auditing, represent each admitted trajectory by the invariant vector `(E/E_scale, L_norm, Q/Q_scale, s_min/s_min,scale)`. Bin each coordinate into 8 equal-frequency bins over the admitted corpus and define normalized `PSC = -(1/log K) * Σ p_c log p_c` over the resulting occupancy probabilities. Also report `C_near`, the fraction of trajectories with `s_min/s_min,scale < 0.5`. This PSC is a data-side coverage descriptor only; snapshot-level or training-loop reuse is out of scope here.” Anchor: `ctl_instruction.md`, new *Trajectory validation metrics* subsection. fileciteturn0file1

## Open items register

| Item | Why it remains open | Exact additional input needed |
|---|---|---|
| Package completeness mismatch | The manifest references `DELIVERY-NOTE.md`, but that file was not present in the uploaded set, so I could not use any gate-open or correction instructions it might contain. | Upload `DELIVERY-NOTE.md`, or confirm that it can be ignored for this adjudication. fileciteturn0file9 |
| Empirical calibration of `n_pts`, SASD, and IPR thresholds | The package provides candidate thresholds, but Phase-24 has not yet supplied the admitted-corpus distributions needed to calibrate them against this dataset rather than against first principles alone. | Phase-24 distributions of `N_t`, `final_timestep`, `max(SASD)`, and `IPR`, plus a small matrix of overfit/trainability outcomes by variant. fileciteturn0file5 fileciteturn0file2 |
| Missing authoritative `word_length` default for standard-base absent-footers | The erratum authorizes fallback to folder defaults for missing-footers, but the package gives a clean variant-level default only for `tol` and `dt_out`; standard-base `word_length` remains heterogeneous in the documented tuples. | An authoritative folder-default or explicit “leave null” instruction for `word_length` on the 701 standard-base absent-footer files. fileciteturn0file7 fileciteturn0file6 |
| PSC state-space choice beyond the invariant-space proxy | The recommended PSC is a principled low-dimensional proxy, but the package does not designate a scientifically preferred reduced state space such as a specific Poincaré section. | A project-level statement of which reduced state-space representation should define “coverage” for downstream science questions. fileciteturn0file2 fileciteturn0file8 |

## References

h5py Developers. *Groups — h5py 3.16.0 documentation*. Official h5py documentation. Accessed June 10, 2026. citeturn2view0

h5py Developers. *Datasets — h5py 3.16.0 documentation*. Official h5py documentation. Accessed June 10, 2026. citeturn3view0turn3view1

NumPy Developers. *numpy.lib.format — NumPy Manual*. Official NumPy documentation. Accessed June 10, 2026. citeturn3view2

NumPy Developers. *numpy.finfo — NumPy Manual*. Official NumPy documentation. Accessed June 10, 2026. citeturn3view3

Python Software Foundation. *decimal — Decimal fixed-point and floating-point arithmetic*. Python 3.14.6 standard-library documentation. Accessed June 10, 2026. citeturn2view4turn3view4

SciPy Community. *CubicHermiteSpline — SciPy v1.17.0 Manual*. Official SciPy documentation. Accessed June 10, 2026. citeturn2view5turn3view5

SciPy Community. *PchipInterpolator — SciPy v1.17.0 Manual*. Official SciPy documentation. Accessed June 10, 2026. citeturn2view6turn4view0

Shannon, Claude E. *A Mathematical Theory of Communication*. *Bell System Technical Journal* 27, 1948. Reprint with corrections hosted by Harvard Mathematics. Accessed June 10, 2026. citeturn6view0
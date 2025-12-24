---
name: IC+Brutus dataset docs
overview: Create a standalone markdown document under `3_Body_Problem/` that documents the final-stage IC datasets and corresponding Brutus outputs with enough detail for later agents (schemas, units/frames, provenance, mapping rules, variant parameters, QC, and known anomalies).
todos:
  - id: inventory_snapshot
    content: Record per-folder file counts, ID ranges, gaps, and disk usage for IC + Brutus; confirm 1:1 mapping and subset relationships.
    status: pending
  - id: brutus_param_audit
    content: Parse `Result:` footers (when present) to summarize the *actual* Brutus parameter sets per folder (tol/Lw/dt/t_end/eta), quantify missing-footer rate, and note OS-path variations.
    status: pending
  - id: prescreen_provenance
    content: Document Stage 2 prescreen criteria and point to `prescreen_stage2/processing_index_*.json` + `run_results_*.json` as ground-truth provenance for which raw ICs were copied into `final_stage_ic_datasets/`.
    status: pending
  - id: gold_subset_provenance
    content: Determine and document how `*_for_gold_standard` IC folders and `*_gold_standard` Brutus folders were created (scripts, selection criteria, reruns/parameter changes, and why standard-gold is a subset).
    status: pending
  - id: doc_write
    content: Write `3_Body_Problem/DATASET_DOCUMENTATION.md` (directory layout, variant matrix, file schemas, mapping rules, physical conventions, QC, anomalies, and minimal loading/parsing examples).
    status: pending
  - id: doc_verify
    content: Spot-check representative IDs (including missing-footer examples and Windows-path footer examples) to confirm docs match on-disk reality.
    status: pending
---

# Three-Body IC + Brutus Output Documentation Plan

## Scope

Primary folders to document (these define the dataset artifact):

- `3_Body_Problem/final_stage_ic_datasets/` (prescreened initial conditions used as Brutus inputs)
- `3_Body_Problem/brutus_output/` (Brutus trajectories, plus the “missing Result line” audit report)

Secondary/provenance folders to cite (these explain how the primary artifact was produced):

- `3_Body_Problem/ic_raw_datasets/` (Stage 1 outputs that were prescreened)
- `3_Body_Problem/prescreen_stage2/` (Stage 2 logic + indices recording pass/fail and file hashes)
- `3_Body_Problem/problematic_ics/` + `3_Body_Problem/problematic_ics_blacklist.json` (failure/move-aside mechanism during runs)

## Output Artifact

- New doc: `3_Body_Problem/DATASET_DOCUMENTATION.md`

## Snapshot: What’s Currently On Disk (from local scan)

Sizes:
- `3_Body_Problem/final_stage_ic_datasets/`: ~59 MB
- `3_Body_Problem/brutus_output/`: ~4.8 GB

Final-stage IC sets (all files are `*.txt`):
- `final_stage_ic_datasets/ic_hierarchical/`: 4857 files, IDs `0000..4999` with 137 gaps
- `final_stage_ic_datasets/ic_hierarchical_for_gold_standard/`: 4857 files, same ID set as `ic_hierarchical/` (appears to be a full copy)
- `final_stage_ic_datasets/ic_standard_quasi_random/`: 2749 files, IDs `0000..3998` with 853 gaps
- `final_stage_ic_datasets/ic_standard_quasi_random_for_gold_standard/`: 2565 files, IDs `0000..3998` with 960 gaps (subset of standard: 184 IDs present in non-gold but absent here)

Brutus output sets (all files are `*.txt`):
- `brutus_output/brutus_hierarchical/`: 4857 files, IDs `0000..4999` with 137 gaps (1:1 with `ic_hierarchical/`)
- `brutus_output/brutus_hierarchical_gold_standard/`: 4857 files, same ID set (1:1 with hierarchical ICs)
- `brutus_output/brutus_standard_quasi_random/`: 2749 files, IDs `0000..3998` with 853 gaps (1:1 with `ic_standard_quasi_random/`)
- `brutus_output/brutus_standard_quasi_random_gold_standard/`: 2565 files (1:1 with `ic_standard_quasi_random_for_gold_standard/`)

## Critical “Gotchas” That Must Be Explicit in the Final Documentation

### 1) Hierarchical ICs are not exactly COM- or momentum-centered

The hierarchical generator in `3_Body_Problem/FINAL_ic_generator_enhanced.py` enforces COM=0 and P=0, then adds per-body Gaussian perturbations to both positions and velocities (default `sigma=0.01`), which reintroduces small COM/momentum offsets.

Documentation must state:
- Standard/quasi-random ICs have exact COM=0 and total momentum=0 by construction.
- Hierarchical ICs typically have small but non-zero COM and total momentum; downstream consumers may want to recenter/reboost to the COM frame before training/analysis.

### 2) The Brutus `Result:` footer is optional and inconsistent

Many Brutus outputs do not end with `Result: filename= ...` (the file’s last non-empty line).

Observed missing-footer rates (from `brutus_output/check missing results line/missing_results_report_20250716_230528.txt`):
- `brutus_hierarchical`: 1550/4857 (31.9%) missing
- `brutus_hierarchical_gold_standard`: 0/4857 (0.0%) missing
- `brutus_standard_quasi_random`: 701/2749 (25.5%) missing
- `brutus_standard_quasi_random_gold_standard`: 219/2565 (8.5%) missing

Documentation must instruct readers:
- Do not rely on `Result:` being present for completeness or parameter extraction.
- Use timestep coverage (last timestep line) as the primary completeness check.

### 3) Brutus parameters vary within folders; scripts are not the only source of truth

Parsing `Result:` lines (when present) shows multiple parameter sets within the same folder, likely due to reruns or changing settings over time.

Documentation plan must include:
- A folder-by-folder “parameter set histogram” derived from `Result:` lines: `(tol, Lw, dt, t_end, eta) → count`.
- A clear statement of what to do for files missing the footer (assume folder-level defaults, or infer from timestep spacing / file-size expectations, and call out uncertainty).

### 4) `Result: filename=` paths are not canonical and are OS-dependent

`Result:` lines contain absolute paths that may be:
- macOS-style (`/Users/...`) or Windows-style (`D:\\code\\cursor\\...`)
- pointing at a different IC folder than the output folder’s nominal pairing (e.g., standard-gold output may reference `ic_standard_quasi_random` even if it was run from a “for_gold_standard” copy)

Documentation must treat `Result: filename=` as an *informational hint*, not an authoritative mapping source.

## What the Final Documentation Must Contain (Checklist)

- **Variant matrix**: one table row per dataset variant folder (IC + Brutus), including counts, ID range, gaps, subset relationships, and intended usage (“gold” vs “non-gold”).
- **File naming conventions**: how to extract the numeric ID and map IC↔Brutus.
- **Exact file schemas**:
  - IC `ic_*.txt`: 3 lines of `m x y z vx vy vz` (units and normalization spelled out).
  - Brutus `brutus_*.txt`: repeated blocks: `t N t_cpu` line, then N particle rows, then blank line; optional `Result:` footer; clarify float formatting and whitespace.
- **Physical conventions**:
  - Units / constants (e.g., `G=1` in prescreening), mass normalization, typical timescales, and which invariants are expected (COM, momentum).
  - What “hierarchical” means in this dataset (inner vs outer, typical separation ratios), and which parts are approximations/perturbations.
- **Pipeline + provenance**:
  - Stage 1 generation scripts and key knobs (Sobol, `epsilon`, scaling, velocity sampling; hierarchical mass normalization).
  - Stage 2 prescreen: dynamic + static checks, thresholds, adaptive percentile thresholds; where decisions are recorded (`processing_index_*.json`).
  - Stage 3 Brutus: where commands came from; how to reconcile scripts vs `Result:`-derived actual parameters.
- **Quality control**:
  - Completeness checks (final timestep threshold) and how they differ from the `Result:` footer check.
  - Energy/momentum conservation expectations and where metrics are computed (`3_Body_Problem/brutus_metrics/`).
- **Known anomalies**:
  - Missing `Result:` footers (with counts and how to handle).
  - OS-path mixture in `Result:` footer.
  - Parameter heterogeneity inside “gold” folders.
  - ID gaps and why they exist (generation continuation, prescreen rejection, problematic IC moves).
- **Minimal parsing examples**: a short Python snippet or pseudocode for robustly reading ICs and Brutus trajectories (including handling missing `Result:`).

## Concrete Work Items (How I’ll Produce the Doc)

1. Inventory snapshot:
   - Recompute counts, ID ranges, gaps, and total sizes.
   - Compute subset relationships: which IDs are excluded from `*_for_gold_standard` vs non-gold.
2. Brutus parameter audit:
   - Parse all `Result:` lines for each folder; produce histograms of `(tol, Lw, dt, t_end, eta)` and OS-path styles.
   - Enumerate the files missing `Result:` per folder; keep a stable list reference via the existing CSV.
3. Provenance:
   - Pull Stage 2 prescreen thresholds from `stage2_prescreening_revised_auto.py` and point to the `processing_index_*.json` indices as the audit trail.
   - Identify how `*_for_gold_standard` folders were created (if no script exists, document that explicitly + how to reproduce by copying a chosen ID list).
4. Write `DATASET_DOCUMENTATION.md` with the checklist above.
5. Verify:
   - Spot-check a handful of IDs across all variants, including:
     - a file with missing footer
     - a file with Windows-path footer
     - a hierarchical IC with non-zero COM/P
     - one of the minority parameter sets inside a gold folder

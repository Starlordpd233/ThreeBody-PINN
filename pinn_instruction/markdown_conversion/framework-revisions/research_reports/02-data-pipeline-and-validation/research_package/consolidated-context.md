# Consolidated Context: Dataset Fragments

**Purpose:** This file consolidates scattered dataset facts from multiple repository sources into one self-contained document for external researchers. Each fragment is labeled with its canonical source path and line range. Source paths are provenance labels, not navigation links — the researcher has access only to snapshot copies in this package.

**Convention:** Every dataset figure in this file references its CLM ID from `claims-table.md`. Figures are not stated as fact; their verification status (claimed or verified) is recorded in the claims table (PKG-03).

**Exclusions:** Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) are NEVER consolidated here — they ship as byte-for-byte intact snapshots in `specs/`. Live code under `pinn/` is excluded from this package entirely (SCOPE-10: the issue doc's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden by directive 2026-05-19; framework specs are the source of truth).

---

## Source: `simulation_data/Documentation/README.md` — Dataset Sizes (lines 81-90)

| Category | Size |
|----------|------|
| Final-stage IC datasets | ~59 MB |
| Brutus output datasets | ~4.8 GB |
| **Total** | **~4.86 GB** |

---

## Source: `simulation_data/Documentation/README.md` — File Naming Conventions and Mapping (lines 193-231)

### IC Files

Non-gold folders use:
```
ic_hierarchical_XXXX.txt
ic_standard_XXXX.txt
```

Gold-standard folders use a `_gold_` infix:
```
ic_hierarchical_gold_XXXX.txt
ic_standard_gold_XXXX.txt
```

Where `XXXX` is a 4-digit zero-padded integer (e.g., `0000`, `0427`, `3998`).

### Brutus Output Files

Non-gold and gold-standard folders use **different filename prefixes**:

```
simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_XXXX.txt
simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_gold_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random/brutus_standard_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_gold_XXXX.txt
```

Gold-standard status is encoded in **both** the folder name and the filename. When parsing, either signal is sufficient; the folder is the authoritative variant identifier.

**Note:** The mapping between IC and Brutus files is always by numeric ID:
- `ic_hierarchical_0427.txt` -> `brutus_hierarchical_0427.txt`
- `ic_hierarchical_gold_0427.txt` -> `brutus_hierarchical_gold_0427.txt`
- `ic_standard_0427.txt` -> `brutus_standard_0427.txt`
- `ic_standard_gold_0427.txt` -> `brutus_standard_gold_0427.txt`

Non-contiguous IDs are intentional — caused by generation continuation, prescreen rejection, and failed Brutus runs. The numeric ID is NOT an index; gaps exist (CLM-01, CLM-02).

---

## Source: `simulation_data/Documentation/README.md` — Brutus Parameters by Variant (lines 584-628)

Important distinction:
- `dt_out` in Brutus outputs is the **output sampling interval**, not the internal Bulirsch-Stoer step size (which is adaptive and not directly stored in these text files).

### Observed Parameter Sets (from `Result:` footers)

All Brutus output files contain a `Result:` footer, but the footer schema varies: some omit `eta`, and a small subset omits both `eta` and `tol`. The counts below are split by footer schema. Files whose footers lack `tol` cannot be assigned a parameter set from the footer alone; for those, assume the folder-level defaults.

Each entry below is `(tol, Lw, dt_out, t_end, eta) -> count`. Files with a partial footer (no `eta`) are listed separately.

#### `brutus_hierarchical/` (CLM-06: ~4,857 files; 3,307 full-schema, 1,550 partial)

Full-schema footers (with `eta`):
- `(1e-15, 130, 0.08, 10, 0.263027) -> 3,307`

Partial footers (no `eta`; tol/Lw/dt still parseable):
- `(1e-15, 130, 0.08, ~10) -> 1,550` (same parameters, different Brutus build omitted `eta`)

#### `brutus_hierarchical_gold_standard/` (4,857 files; all full-schema)

- `(1e-13, 130, 0.01, 10.01, 0.277971) -> 4,146`
- `(1e-13, 124, 0.01, 10.01, 0.277971) -> 649`
- `(1e-14, 118, 0.01, 10.01, 0.270396) -> 34`
- `(1e-14, 112, 0.01, 10.01, 0.270396) -> 27`
- `(1e-14, 124, 0.01, 10.01, 0.270396) -> 1`

#### `brutus_standard_quasi_random/` (CLM-05: 2,749 files; 2,048 full-schema, 701 partial)

Full-schema footers (with `eta`):
- `(1e-13, 118, 0.17, 10.03, 0.277971) -> 1,126`
- `(1e-13, 130, 0.17, 10.03, 0.277971) -> 922`

Partial footers (no `eta`; tol/Lw/dt still parseable):
- `(1e-13, 118, 0.17, ~10.03) -> 701` (assume default Lw=118 unless footer shows otherwise)

#### `brutus_standard_quasi_random_gold_standard/` (CLM-05: 2,565 files; 2,346 full-schema, CLM-07: 219 minimal)

Full-schema footers (with `eta` and `tol`):
- `(1e-13, 130, 0.01, 10.01, 0.277971) -> 1,754`
- `(1e-14, 130, 0.01, 10.01, 0.270396) -> CLM-08: 592`

Minimal footers (no `eta` or `tol`; only `dt`, `Lw`, `t_cpu`, and energy fields):
- `(Lw=130, dt=0.01, ~10.01) -> CLM-07: 219` (tol unknown from footer; assume folder default 1e-13)

### Folder-default parameters (CLM-09)

| Variant | Default tol | Default dt_out |
|---------|------------|----------------|
| Standard quasi-random | 0.17 | 1e-13 |
| Hierarchical base | 0.08 | 1e-15 |
| Gold standard (both) | 0.01 | 1e-13 |

### Snapshot count warning (CLM-10)

Avoid hard-coding exact expected snapshot counts:
- `t_end` can be slightly larger than 10 (e.g., 10.01 or 10.03) when `dt_out` does not evenly divide the nominal stop time.
- Some runs may have been re-executed with different parameters, especially in gold folders.

Approximate snapshot counts are stated in the issue doc (CLM-10: ~59 standard / ~125 hierarchical / ~1000 gold), but the README explicitly warns against hard-coding these values.

---

## Source: `simulation_data/Documentation/README.md` — Completeness Checks (lines 637-660)

**Primary Check:** Final timestep >= 9.5

```python
# Validation pattern used in run scripts
timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
final_timestep = max([float(t) for t in timesteps])
if final_timestep < 9.5:
    # Mark as incomplete
```

**Do NOT rely on:**
- Parsing a specific `Result:` footer schema (the footer is present in all files but its fields vary)
- Line count thresholds (variable due to integration dynamics)

The `final_timestep >= 9.5` gate rule is grounded in README Completeness Checks (CLM-11). The prevalence (what fraction of trajectories satisfy it) is `claimed-unverified` (CLM-11).

---

## Source: `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (full file)

Generated: 2026-03-18

### Summary

- `ic_standard_quasi_random/` contains **CLM-05: 2,749** ICs.
- `ic_standard_quasi_random_for_gold_standard/` contains **CLM-05: 2,565** ICs.
- All 2,565 gold-standard ICs are a **byte-identical subset** of the standard ICs (differing only in filename prefix: `ic_standard_` vs `ic_standard_gold_`).
- **CLM-04: 184 ICs** exist in the standard folder but have no gold-standard counterpart.

These 184 ICs were simulated at standard Brutus resolution but were never selected for gold-standard (higher temporal resolution, `dt_out=0.01`) re-simulation.

### The 184 IDs

```
0038  0042  0049  0138  0142  0149  0238  0242  0249  0338
0342  0349  0438  0442  0449  0504  0540  0555  0557  0579
0585  0586  0638  0642  0649  0704  0740  0755  0757  0779
0785  0786  0838  0842  0849  0904  0940  0955  0957  0979
0985  0986  1023  1043  1055  1061  1127  1130  1144  1148
1150  1154  1155  1191  1238  1242  1338  1342  1426  1440
1455  1457  1479  1485  1486  1538  1542  1549  1604  1640
1655  1657  1679  1685  1686  1702  1723  1743  1755  1761
1827  1830  1840  1844  1848  1850  1854  1855  1891  1909
1941  1956  1958  1975  2004  2039  2056  2060  2107  2110
2127  2136  2164  2172  2206  2219  2274  2277  2281  2351
2359  2382  2386  2402  2439  2455  2460  2495  2538  2542
2604  2640  2655  2657  2679  2685  2686  2723  2743  2755
2761  2827  2830  2844  2848  2850  2854  2855  2909  2941
2956  2958  3004  3039  3056  3060  3107  3110  3136  3172
3219  3277  3359  3362  3368  3382  3386  3402  3439  3455
3460  3538  3542  3604  3640  3655  3657  3679  3685  3686
3723  3743  3755  3761  3827  3830  3844  3848  3850  3854
3855  3891  3941  3958
```

Total: **184 IDs**

---

## Source: `simulation_data/Documentation/problematic_ics_blacklist.json` — Blacklist Summary (CLM-03)

The blacklist is a JSON object with two keys: `hierarchical` and `standard`.

- **`hierarchical`**: 2 IDs (123, 253)
- **`standard`**: 63 IDs (first entries: 21, 30, 52, ...)
- **Total: CLM-03: 65 IDs** (2 hierarchical + 63 standard)

This count is observable in the JSON file. The count itself is `claimed-unverified` (CLM-03) because Phase 23 performs no empirical probes; Phase 24 (DATA-02) verifies both count/composition and the loading/consumption status at training time (the M11 finding).

---

## Source: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` — Provenance Excerpt (SCOPE-07)

This script processes all Brutus output files across the four variant directories, calculating conservation metrics (energy, momentum, angular momentum) and producing JSON metric files for every output file, even if partial or erroneous.

**Key structural details (provenance for metric-related findings):**

Input directories enumerated in the script:
- `brutus_hierarchical/`
- `brutus_hierarchical_gold_standard/`
- `brutus_standard_quasi_random/`
- `brutus_standard_quasi_random_gold_standard/`

Output goes to `simulation_data/Data/metrics/` with per-variant subdirectories.

Brutus parameter defaults recorded in the script (`BRUTUS_PARAMS` dict):
- Hierarchical: tolerance=1e-15, word_length=130, dt_out=0.08
- Standard: tolerance=1e-13, dt_out=0.17

The script does NOT perform completeness checks (no `final_timestep >= 9.5` gate); it processes all files found. Completeness checking is the responsibility of downstream consumers.

**Relevance to findings:** This script is the provenance grounding for how metrics were calculated (SCS/SASD/IPR/PSC definitions are in `data_quality_assessment.md` section 3, not in this script). The script's output feeds the metric values that Phase 24 will re-verify against the claims table.

---

## Per-Finding SCOPE-07 Inclusion Matrix

| Finding area | Scripts directory source | Included? | Rationale |
|---|---|---|---|
| Metrics calculation provenance | `calculate_metrics.py` | Yes (excerpt above) | Grounds how metrics were produced; feeds DATA-05/DATA-06 |
| Prescreening thresholds | `Validation/prescreening/` | No excerpt needed | Prescreening is upstream of Brutus; the findings concern Brutus outputs and downstream ingestion, not prescreen logic. README documents prescreen outcomes (ID gaps) sufficiently. |
| Brutus runner parameters | `Scripts/brutus_runners/` | No excerpt needed | README Brutus Parameters section documents the per-variant parameter sets exhaustively. Runner scripts invoke Brutus with those parameters; the README is the more direct source for adjudication. |

---

*End of consolidated context file. Every dataset figure above references its CLM ID from `claims-table.md`. No `pinn/` content is included (D-06/SCOPE-10). No framework spec content is consolidated here (D-03).*

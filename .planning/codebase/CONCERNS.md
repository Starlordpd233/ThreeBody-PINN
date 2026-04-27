# Codebase Concerns & Risks Audit

**Analysis Date:** 2026-04-27
**Scope:** Full repository audit for technical debt, architecture risks, security, data quality, and process issues.
**Severity Scale:** BLOCKER > CRITICAL > MAJOR > MINOR > INFO

---

## Executive Summary

This is a research codebase in **pre-implementation state**. The simulation data pipeline functions and produces valid Brutus outputs. However, the PINN/ML layer has **not been built** -- there is no training loop, no LLM integration, and no end-to-end pipeline connecting simulation data to model training. A comprehensive pre-implementation audit (2026-04-27) identified **11 critical blockers** in the PINN architecture and curriculum documents. Those blockers have not yet been addressed in code or documentation.

**Overall Readiness:** NOT READY FOR IMPLEMENTATION. The pre-implementation audit issues must be resolved in LaTeX documents and pipeline code before any training code is written.

---

## 1. BLOCKER: Critical Technical Issues

### B-1: Characteristic Length D is Wrong -- Corrupts All Scaled Quantities

**What:** `pinn/data-processing-pipeline-full.py:142` computes:
```python
self.D = np.cbrt(self.G * self.T_max**2)  # = cbrt(100) ≈ 4.64
```
This omits total mass `M_tot = 3`. The correct formula is:
```
D = (G * M_tot * T^2)^(1/3) = cbrt(3 * 100) = 6.694
```
**Impact:** All scaled positions (r' = r/D), velocities (v' = v/V where V = D/T), and every normalized dimensionless quantity (E, L_norm, Q, smin) computed with D = 4.64 are silently corrupted. Stage assignment thresholds use these scaled quantities -- wrong D means wrong curriculum stages for every trajectory.

**Fix:** Change line 142 to `self.D = np.cbrt(self.G * 3.0 * self.T_max**2)`. Recompute ALL stage assignments after the fix. Any training done with current D must be restarted.

**Severity:** BLOCKER

### B-2: AD Chain-Rule Factor Missing -- Physics Residual Wrong by 4x

**What:** The time normalization τ = 2t/T - 1 (used for network input) requires chain-rule conversion of AD derivatives back to physical time. `review.md` identifies this precisely:
```
v' = dr'/du = 2 * dr'/dτ     (factor of 2)
a' = d²r'/du² = 4 * d²r'/dτ²  (factor of 4)
```
The current `pinn/basic_architecture.py` does not implement these conversion factors. As a result:
- Kinetic energy in the loss function is wrong by a factor of 4
- Physics residual accelerations are wrong by a factor of 4
- The network optimizes the wrong ODE

**Impact:** Even if all other parameters are correct, the PINN learns incorrect physics. This is the most subtle and dangerous bug because the network will still converge (to the wrong solution).

**Fix:** Add explicit derivative conversion in the loss function. Document the three-layer scaling: raw → physics-scaled (u, r', v') → network input (τ, IC_norm). Make every loss function declare which space it operates in.

**Severity:** BLOCKER

### B-3: No Training Loop Exists

**What:** `pinn/basic_architecture.py` (307 lines) defines the SQR-SkipResNet-SIREN model architecture but contains **no training loop, no loss function implementation, no data loading, no optimizer setup, and no evaluation logic**. This is purely an architecture definition.

**Impact:** The core PINN capability (training on simulation data) does not exist. This is the largest operational gap in the project.

**Files:** `pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py` (has stage assignment and batch construction but no training loop)

**Severity:** BLOCKER

### B-4: Wrong SIREN Init Formula in Documentation (Code is Correct)

**What:** The audit (B-01) identifies that `main_pinn.pdf` Table 1 specifies the hidden-layer init as `U[-ω₀√(6/n), ω₀√(6/n)]` (multiplies by ω₀), which would cause 810,000x variance explosion at ω₀=30. However, the actual code at `pinn/basic_architecture.py:37` is **correct**:
```python
bound = np.sqrt(6 / self.in_features) / self.omega_0  # DIVIDES
```
**Impact:** If anyone implements from the LaTeX document instead of the Python code, the network will produce instant NaN. The documentation is the authoritative architecture spec -- code divergence from docs is a risk.

**Fix:** Correct `main_pinn.pdf` Table 1 and Section 2.2. The LaTeX documents are the current source of truth for planning (Phase 9 is about them).

**Severity:** BLOCKER (documentation)

### B-5: Input Vector Dimensionality Is Three Different Numbers

**What:** Across the LaTeX documents, the input vector is claimed as 12D, 13D, and 14D simultaneously. The actual code at `pinn/data-processing-pipeline-full.py` produces a 13-component IC vector (plus time = 14D total). The CTL document's pipeline description produces 11D IC. No single authoritative count exists.

**Impact:** The first Linear layer requires a fixed `n_in`. Cannot initialize the network without knowing the dimension. Training code cannot be written.

**Fix:** Adopt 14D canonical: [t'(1D), IC_vector(13D)]. Standardize across ALL documents and code. Resolve the trig-encodings vs shape-invariants conflict (see D-1 below).

**Severity:** BLOCKER

---

## 2. CRITICAL: Architecture & Physics Issues

### C-1: Softening Parameter Mismatch by 10^5x Across Documents

**What:** CTL document uses ε = 1e-10 for static invariant calculation (stage assignment). PINN document uses ε_soft = 1e-5 for dynamic loss computation. Pipeline code at `pinn/data-processing-pipeline-full.py:594` uses ε = 1e-10 (following CTL). The network would train with different physics than the curriculum sorts by.

**Impact:** For close encounters (r ~ 0.001), the potential differs by ~1%. Stage assignments (using ε_invariant) and training physics (using ε_loss) disagree on which systems are "close."

**Fix:** Unify at ε = 1e-8 as recommended by audit B-09. Update all three locations: CTL doc, PINN doc, pipeline code. Recompute all stage assignments.

**Severity:** CRITICAL

### C-2: COM Frame Inconsistency Across Dataset Types

**What:** Standard quasi-random ICs have exact COM = 0 by construction. Hierarchical ICs have median |COM| ≈ 9e-3, |P| ≈ 3e-2 (from Gaussian perturbation σ=0.01). The PINN assumes COM-frame outputs.

Pipeline code at `pinn/data-processing-pipeline-full.py:534-551` has `verify_com_frame()` but only warns -- it does not transform. Separate COM scripts exist for ICs vs Brutus outputs with no mass-consistency check.

**Impact:** Network trained on non-COM-frame hierarchical targets learns wrong reference frame. COM offset ~0.01 is 5-20% of inner binary separation (a ~ 0.1-0.3) -- not negligible.

**Fix:** Implement unified COM transformer: recenter + reboost on RAW positions/velocities FIRST, THEN scale by D. Verify `np.allclose(m_ic, m_brutus)` at t=0.

**Severity:** CRITICAL

### C-3: Non-Contiguous IDs Break Curriculum Mapping

**What:** Standard dataset: 1,250 gaps out of 4,000 (31.2% gap rate). Hierarchical: 143/5,000 (2.9%). The stage assignment in `pinn/data-processing-pipeline-full.py:991-1020` iterates over a list of trajectories and assigns stages in-place. It does NOT build an `id_to_path` dictionary. If the trajectory list is built from sorted file listing (with gaps), index-based access will map incorrect IDs.

**Impact:** Stage assignment via list-index access produces up to 45% wrong mappings in the standard dataset. Network trains on Stage-k data labeled as Stage-j.

**Fix:** Build an explicit `id_to_path` dictionary from on-disk filenames at DataLoader init. Never assume ID == array index. Add `TrajectoryIndex` class with `get_by_id(file_id)` method.

**Severity:** CRITICAL

### C-4: Missing Stage 4-to-5 Validation Gate

**What:** `calculate_metrics.py` generates metrics for ALL Brutus files including partial/errored runs. The only validity signal (final_timestep >= 9.5) runs at Stage 3, never re-validated at training time. No snapshot-count minimum is enforced.

**Impact:** 10-snapshot trajectories (failed early) can enter training if t_final happens to be >= 9.5. Lyapunov time calculation needs 200+ snapshots -- 10-snapshot trajectories break Stage 4+ assignment.

**Fix:** Insert `TrajectoryValidator` at DataLoader init: enforce `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0-3, AND `final_timestep >= 9.5`.

**Severity:** CRITICAL

### C-5: Stage Transition Criteria Theoretically Unattainable

**What:** The CTL document requires monotonically-decreasing validation loss for stage advancement. With limited data (~7,600 ICs total) and Adam optimizer, stochastic fluctuations make monotonic decrease physically impossible over long training runs.

**Impact:** Curriculum progression will block indefinitely. Training cannot advance beyond early stages.

**Fix:** Use relaxed criteria: validation loss < threshold for N consecutive epochs (not strictly monotonic). Pilot Stage 0 first to calibrate thresholds empirically.

**Severity:** CRITICAL

### C-6: Energy Loss Weight Schedule Risks Late-Stage Destabilization

**What:** CTL Table 3 specifies λ_E = 1000 at Stage 6. This could make the energy term 100-5000x larger than the physics residual, drowning dynamics learning entirely. The loss becomes a pure energy conservation optimizer that ignores trajectory accuracy.

**Impact:** Network at Stage 6 learns to conserve energy perfectly while producing physically wrong trajectories.

**Fix:** Implement hybrid capped schedule: `λ_E(k) = min(10^(k-3), cap[k])`. Add safeguard: if `λ_E * L_energy > 10 * L_data`, warn and reduce.

**Severity:** CRITICAL

---

## 3. MAJOR: Technical Debt

### M-1: No Dependency Management

**What:** Zero dependency files exist:
- No `requirements.txt`
- No `pyproject.toml`
- No `setup.py`
- No `Pipfile`
- No `environment.yml`
- No `poetry.lock`

A `.venv/` exists (216MB, Python 3.12.2) but no way to reproduce it. The `.gitignore` excludes `.venv/` (good).

**Impact:** Impossible to reproduce the environment. Hidden dependency conflicts. Onboarding friction is extreme.

**Fix:** Create `requirements.txt` with pinned versions, generated from current `.venv/` via `pip freeze`.

**Severity:** MAJOR

### M-2: Dual Data Pipeline -- Two Competing Implementations

**What:**
1. `pinn/data-processing-pipeline-full.py` (1,650 lines) -- monolithic, source of truth, used by CLAUDE.md references
2. `pinn/data-handling/` -- modular package with `core/`, `processing/`, `scripts/` subdirectories, partial implementation

Both contain parsing logic, invariant computation, stage assignment, and batch construction. The modular package imports from `pinn/data-processing-pipeline-full.py` (copy-paste style) rather than sharing a common library.

**Impact:** Potential divergence. Unclear which to use for training. Any fix applied to one must be manually propagated to the other.

**Fix:** Deprecate `data-processing-pipeline-full.py` after extracting its unique functions into `data-handling/`. Run parity checks to confirm identical outputs.

**Severity:** MAJOR

### M-3: 2,847-Line `next steps.txt` -- Mostly Superseded

**What:** `pinn_instruction/original_latex/review-of-framework/issues/next steps.txt` is a 128KB dump (2,847 lines) containing issues, solutions, and commentary from early development. Per the Phase 9 context (D-06), ~80% is superseded by the 2026-04-27 audit. Only 4 unique sections have value not subsumed by the audit.

**Impact:** Anyone reading this file wastes time on superseded analysis. Contradicts newer documents.

**Fix:** Phase 9 consolidation (currently unstarted) will extract unique content and archive the original.

**Severity:** MAJOR

### M-4: Hardcoded Machine-Specific Paths in Brutus Makefile

**What:** `brutus_Newton-main/makefile` contains:
```makefile
BREW_PREFIX = /opt/homebrew
HOME_DIR = <home>
MPRLIB = $(HOME_DIR)/src/mpreal
```

**Impact:** Cannot build Brutus on any machine except the author's M2 Mac. Requires manual path edits for other users.

**Fix:** Replace with environment variables or auto-detection: `BREW_PREFIX ?= $(shell brew --prefix)`, `MPRLIB ?= $(HOME)/src/mpreal`.

**Severity:** MAJOR

### M-5: No Reproducibility -- Missing Seeds and Random State

**What:** IC generation uses Sobol sequences with scrambling enabled (`FINAL_ic_generator_enhanced.py`), but no fixed seed is found in the runner scripts. The Sobol scrambling seed determines the entire dataset distribution.

**Impact:** Regenerating ICs produces different data. Cannot reproduce existing datasets exactly.

**Fix:** Add `--seed` parameter to `generate_ics.py` with a documented default value. Store the seed in dataset metadata.

**Severity:** MAJOR

### M-6: Blacklist Not Enforced in PINN Pipeline

**What:** `simulation_data/Documentation/problematic_ics_blacklist.json` contains 65 blacklisted IDs (2 hierarchical + 63 standard). The Brutus runner scripts (`run_brutus_both_type_simple.py`, `run_brutus_hierarchical_only_mac_gold_standard.py`) DO load and enforce the blacklist by reading the `problematic_ics/` directory. However, the PINN data pipeline (`pinn/data-processing-pipeline-full.py`) does NOT load or enforce the blacklist.

**Impact:** Blacklisted ICs that somehow have Brutus outputs could enter PINN training, producing corrupted training data.

**Fix:** Load `problematic_ics_blacklist.json` at DataLoader init. Log and exclude blacklisted IDs.

**Severity:** MAJOR

### M-7: Pickle Used for Batch Serialization

**What:** `pinn/data-processing-pipeline-full.py:1585-1586` and `pinn/data-handling/scripts/prepare_training_data.py:193-194` use `pickle.dump()` for batch files. `pinn/data-handling/core/parsing.py:407,442` loads pickle files.

**Impact:** Pickle is unsafe for data exchange (arbitrary code execution on load), not portable across Python versions, and the format is opaque (cannot inspect without Python). For large tensor data, HDF5 or NPZ would be more appropriate.

**Fix:** Replace pickle with HDF5 for batch storage. Keep `.pkl` loading for backward compatibility only.

**Severity:** MAJOR

### M-8: No Test Coverage

**What:** The only test file in project-owned code is `simulation_data/Data/testing_data/test_pipeline.py` (407 lines). No tests exist for `pinn/` code, IC generation, parsing, invariant computation, or stage assignment.

**Impact:** Any refactoring of the data pipeline risks silent regressions. The D formula bug (B-1) would have been caught by a unit test comparing D to the known correct value.

**Fix:** Add unit tests for: characteristic length D computation, energy conservation on known ICs, COM frame verification, stage assignment, input vector normalization. Minimum: test `GlobalScales.__post_init__` produces D = 6.694.

**Severity:** MAJOR

### M-9: 1650-Line Monolithic Data Pipeline

**What:** `pinn/data-processing-pipeline-full.py` is 1,650 lines with ~30 functions/classes in a single file. It covers parsing, scaling, invariant computation, stage assignment, batch construction, and HDF5 I/O -- multiple separable concerns.

**Impact:** Hard to modify, hard to test, hard to understand. The D bug at line 142 is a one-line fix but its blast radius is the entire file.

**Fix:** Continue the modularization started in `data-handling/`. Extract each concern into its own module. Run parity tests between monolith and modular output.

**Severity:** MAJOR

---

## 4. MAJOR: Documentation Gaps & Inconsistencies

### D-1: Input Vector Orientation Encoding -- Live Conflict

**What:** Two competing proposals for the 13-component IC vector:
- **2026-04-27 Audit (B-04):** Recommends 5 trig values: `[sin(θ_L), cos(θ_L), sin(φ_L), cos(φ_L), sin(γ_orb)]`
- **Causal_Trainingmismatch Blueprint:** Argues trig encodings are physically flawed (gimbal lock during chaotic scattering) and proposes 3 shape invariants `(I_1, I_2, I_3)` + 2 direction cosines `(cos θ, sin θ)`

Both produce 14D total (t + 13 ICs) but with completely different IC composition. The Phase 9 context (D-05) flags this as a conflict that must be resolved by physical reasoning, not silently merged.

**Impact:** Cannot finalize the input vector specification. Training code blocked until resolved.

**Fix:** Resolve in Phase 9 `01-architecture-and-physics-foundations.md`. Phase 9 context recommends shape invariants + direction cosines (Causal_Trainingmismatch position) based on gimbal-lock avoidance and rotation invariance.

**Severity:** MAJOR

### D-2: I_norm Definition -- Text vs Code Inconsistency

**What:** CTL document text defines I_norm = tr(I) / (M * r_char^2). Pipeline code at `pinn/data-processing-pipeline-full.py:679-691` uses the same formula. However, `next-step-for-data-processing-pipeline.txt` reports that some code listings apply `tanh()` to this value, binding it to [-1,1] while the text does not mention `tanh`. The current pipeline code does NOT apply `tanh`.

**Impact:** If old code listings with `tanh` are used as reference, I_norm will be double-normalized (already in a bounded range, then tanh-compressed).

**Fix:** Document the definitive formula. No `tanh` -- the value is already naturally bounded. Standardize across all docs.

**Severity:** MAJOR

### D-3: Standard Gold Standard Provenance Unknown

**What:** No runner script in the repository targets `brutus_output/brutus_standard_quasi_random_gold_standard/`. The 2,565 files in this folder were produced by an external process. File counts show 184 fewer files than the base standard IC folder (2,749 base -> 2,565 gold).

**Impact:** Cannot reproduce this dataset. Parameters are inferred from Result footers only. If this data is needed for Stage 5+ curriculum, the gap must be understood.

**Fix:** Document provenance as "partial / external machine." Do not use as sole source for Stage 5 without confirming parameter consistency.

**Severity:** MAJOR

### D-4: Gold Standard Deployment Requires Specific GPU/NN Architecture(?)

**What:** The project README references fine-tuning Qwen 3.5 2B 4-bit, but research documents also reference PINN training. The relationship between PINN and LLM approaches is unresolved. `PROJECT.md` states: "Existing PINN approach (SQR-SkipResNet-SIREN) relationship to new LLM direction is TBD."

**Impact:** Unclear which architecture to build toward. Both paths require different infrastructure, data formats, and evaluation.

**Fix:** Decision needed: PINN-first (train PINN, then optionally distill to LLM) or LLM-direct (format data as text, train LLM). The Phase 9 consolidation should surface this as `[DECISION-NEEDED]`.

**Severity:** MAJOR

### D-5: 28 Author-Flagged Uncertainties in LaTeX Docs

**What:** The CTL and PINN LaTeX documents contain 28 `\authcomment` items where the author explicitly flagged uncertainty. `next-step-for-data-processing-pipeline.txt` lists 12 specific line-numbered comments. Examples include: "Confirm that all components in the IC vector are in the range [-1,1]," "Double check this softening parameter's accuracy/validity," "The two paragraphs below are suspicious."

**Impact:** These represent the author's own acknowledgment of unresolved questions. If a developer implements from these docs without resolving the comments, they will encounter the exact same uncertainties.

**Fix:** Resolve each `\authcomment` with a definitive answer. This is scope for a future LaTeX-revision phase (not Phase 9 consolidation).

**Severity:** MAJOR

---

## 5. MODERATE: Data Quality Risks

### Q-1: 184 Standard IDs Missing Gold Counterpart

**What:** 184 standard quasi-random IDs have no gold-standard Brutus output. Documented in `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`. Stage 5 of the curriculum requires gold-standard data (dt_out=0.01).

**Impact:** 184 trajectories cannot participate in Stage 5 training. The data pipeline must handle this gap or fall back to low-fidelity standard data.

**Fix:** Check gold counterpart existence before Stage 5 assignment. Skip to Stage 6 or use standard fallback with warning.

**Severity:** MODERATE

### Q-2: Brutus Footer Schema Heterogeneity

**What:** Result footers come in 3 schemas:
- **Full:** filename, N, t_begin, t_end, dt, eta, tol, Lw, t_cpu, E_initial, E_final, dE/E
- **Partial (no eta):** Same minus `eta=`
- **Minimal (no eta, no tol):** 219 files in `brutus_standard_quasi_random_gold_standard/`

Parsing code must handle optional fields. When `tol` is absent, fall back to folder defaults (documented in `simulation_data/Documentation/README.md` "Brutus Parameters by Variant").

**Impact:** Parsers that assume all fields are present will crash on minimal-footers files. Tolerance-aware logic needs fallback logic.

**Severity:** MODERATE

### Q-3: 31.2% Gap Rate in Standard Dataset

**What:** Standard quasi-random dataset has 1,250 gaps in 4,000 IDs (31.2% gap rate). Gap causes: generation continuation, prescreen rejection (993 failed), problematic IC moves.

**Impact:** Code that assumes dense ID ranges will fail. Linear indexing silently maps wrong data. This is already partially handled by Brutus runners but the PINN pipeline needs explicit gap-aware logic.

**Severity:** MODERATE

### Q-4: Brutus Timeout Produces Orphaned Partial Outputs

**What:** Batch runners use 3000-second timeout. Failed simulations have their partial output deleted and IC moved to `problematic_ics/`. However, there is no resume mechanism -- an IC that timed out at 2900s cannot be continued.

**Impact:** Some ICs in chaotic regimes may be fundamentally untestable within the 50-minute budget. These ICs are permanently lost from the dataset.

**Fix:** Consider increasing timeout or implementing checkpoint/resume for long-running simulations.

**Severity:** MODERATE

### Q-5: Parameter Heterogeneity Within Dataset Folders

**What:** Multiple tolerance and word-length values exist within the same output folder (e.g., `brutus_hierarchical/` has files with tol=1e-15 AND tol=1e-13). This is documented in `simulation_data/Documentation/README.md`.

**Impact:** Training data from the same "variant" has different numerical precision characteristics. The PINN may learn different noise floors from different parameter subsets.

**Fix:** Track per-file tolerance in metadata. Consider parameter-homogeneous subsets for training.

**Severity:** MODERATE

---

## 6. MODERATE: Process & Workflow Issues

### P-1: Phase 9 (Issues Consolidation) Not Started

**What:** Phase 9 has 0/3 plans complete. Three untracked issue files exist in `pinn_instruction/original_latex/review-of-framework/issues/`:
- `three_body_pinn_pre-implementation_audit_2026-04-27.md` (untracked)
- `Causal_Trainingmismatch_resolution_blueprint.md` (untracked)
- `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` (untracked)

The 4 original `.txt` files are tracked. Consolidation is the v1.2 milestone's first phase.

**Impact:** 7 scattered, overlapping, partially contradictory documents block implementation planning. New team members must read all 7 to understand the state.

**Severity:** MODERATE

### P-2: Modified But Uncommitted Documentation

**What:** `simulation_data/Documentation/README.md` is modified in the working tree (git status: `M`). The changes are unstaged.

**Impact:** Documentation drift between committed and actual state. If someone checks out the repo, they get stale docs.

**Severity:** MINOR

### P-3: No CI/CD Pipeline

**What:** No GitHub Actions, no test automation, no linting enforcement, no automated build verification.

**Impact:** All quality checks are manual. A broken commit would not be caught until someone runs the pipeline manually.

**Severity:** MINOR

### P-4: Reference Code is Loaded with TODOs

**What:** `reference-code/` directory (387MB) contains external NN reference implementations with 30+ TODO/FIXME/HACK comments. These are external codebases (GravNN, PINA, PyTorch source) and not project-owned.

**Impact:** Minimal -- these are reference code, not active dependencies. However, the directory is large (387MB) and contains code that could be confused with project code.

**Fix:** Consider moving reference-code to a submodule or separate repository to reduce repo size.

**Severity:** MINOR

---

## 7. MINOR: Scaling & Portability

### S-1: Brutus Build Depends on System-Specific Libraries

**What:** Brutus requires GMP (libgmp, libgmpxx), MPFR (libmpfr), and the `mpreal` header library installed at specific paths. These are not vendored and not documented with version requirements.

**Impact:** Building Brutus requires installing system packages via Homebrew (macOS) or apt (Linux). Version incompatibilities could cause silent precision differences.

**Severity:** MINOR

### S-2: Large Data Directories Excluded from Git But Not Documented

**What:** `.gitignore` excludes `simulation_data/Data/` entirely (6.2GB). The `IC_RAW_DIR` environment variable pattern externalizes raw ICs. New users must understand which data comes from git and which must be generated or obtained externally.

**Impact:** A fresh clone has no simulation data. The pipeline must be run from scratch or data must be shared via external means.

**Fix:** Document data acquisition steps in a SETUP.md or expand the Quick Start section of the dataset README.

**Severity:** MINOR

### S-3: Single M2 Mac Development Constraint

**What:** All development happens on one M2 Mac (Apple Silicon). The Brutus makefile assumes ARM64 + Homebrew at `/opt/homebrew`. No testing on x86_64 Linux.

**Impact:** Brutus may not compile on Linux without makefile modifications. GPU training would require different infrastructure than what's available on M2.

**Severity:** MINOR

---

## 8. Security

### No Secrets Detected

- No `.env` files found
- No API keys, tokens, or credentials in codebase
- `.gitignore` covers `.venv/`, `gha-creds-*.json`, and data directories
- No cloud service credentials, no database passwords
- Project is entirely offline (no external API calls in pipeline code)

### Unsafe Deserialization

- `pickle.dump/load` used in `pinn/data-processing-pipeline-full.py` and `pinn/data-handling/core/parsing.py` (see M-7)
- `np.load(allow_pickle=True)` used in `pinn/data-handling/core/parsing.py:411,468`
- Risk is low for this project (data comes from own pipeline, not external sources) but violates security best practice

### Path Traversal

- File paths are constructed from numeric IDs and predefined directory structures
- No user-supplied path components found in file I/O operations
- Risk is low but not formally validated

---

## 9. Pre-Implementation Audit: 11 Blockers Status

From the 2026-04-27 comprehensive audit (`three_body_pinn_pre-implementation_audit_2026-04-27.md`):

| # | Blocker | Code Status | Doc Status |
|---|---------|-------------|------------|
| B-01 | SIREN hidden-layer init wrong formula | Code CORRECT (divides by ω₀) | Doc WRONG (multiplies) |
| B-02 | D = 6.694 (currently 4.64 in code) | Code WRONG | Doc WRONG |
| B-03 | Input vector 12/13/14D conflicting | Code uses 14D | Doc inconsistent |
| B-04 | Trig angle encodings missing from CTL | Code not implemented | Doc missing |
| B-05 | COM frame violation in hierarchical | Code warns only | Doc inconsistent |
| B-06 | Missing Stage 4→5 validation gate | NOT in code | NOT in docs |
| B-07 | No replay/lookahead batch split | Basic replay exists | Doc inconsistent |
| B-08 | Data-fidelity vs collocation conflated | NOT in code | Doc conflated |
| B-09 | Softening mismatch ε=1e-10 vs 1e-5 | Code uses 1e-10 | Docs disagree |
| B-10 | Dynamic omega0 scheduling is no-op | Not in code | Doc proposes it |
| B-11 | Non-contiguous IDs not handled | NOT in code | Doc assumes linear |

**Resolution status:** 0 of 11 blockers resolved in code. 0 of 11 blockers resolved in documentation. **All 11 remain open.**

---

## 10. Dependency & Environment Risks

### No Pinned Dependencies

Current environment (inferred from `.venv/`):
- Python 3.12.2
- PyTorch (imported in `basic_architecture.py`)
- NumPy, SciPy, pandas (used throughout pipeline)
- No version information recorded anywhere

### External Library Risk

- `mpreal` (C++ header for MPFR) -- maintained, stable, but must be installed separately
- GMP and MPFR -- system libraries, version-dependent
- Brutus uses C++11 standard (not C++17/20) -- compiler compatibility risk as g++ defaults evolve

---

## 11. Summary: What Blocks Implementation

### Must Fix Before Writing Training Code:

1. **Fix D (B-1):** Change `pinn/data-processing-pipeline-full.py:142` to `D = cbrt(G * 3.0 * T_max^2) = 6.694`. Recompute all stages.
2. **Fix AD chain rule (B-2):** Add derivative conversion factors (2x for v, 4x for a) in loss computation.
3. **Resolve input vector (B-3, D-1):** Adopt 14D canonical, pick trig vs shape-invariants, update all docs.
4. **Fix COM frame (C-2):** Implement unified COM transformer; apply before scaling.
5. **Build TrajectoryIndex (C-3):** Non-contiguous ID handling at DataLoader init.
6. **Unify softening (C-1):** Set ε = 1e-8 everywhere; recompute stages.
7. **Add validation gate (C-4):** Snapshot-count + t_final >= 9.5 check at DataLoader init.
8. **Create `requirements.txt` (M-1):** Pin all dependencies.

### Should Fix Before Writing Training Code:

9. **Add training loop skeleton (B-3):** DataLoader, loss function, optimizer, evaluation.
10. **Resolve batch construction (B-07, B-08):** Replay/lookahead split, collocation point sampling.
11. **Fix SIREN doc (B-4):** Correct LaTeX document to match correct code.
12. **Add tests for D, COM, invariants (M-8):** Catch regressions.
13. **Load blacklist in PINN pipeline (M-6):** Exclude problematic ICs.
14. **Replace pickle with HDF5 (M-7):** Safer serialization.

---

*Concerns audit: 2026-04-27*
*Next review: After Phase 9 completion (issues consolidation)*

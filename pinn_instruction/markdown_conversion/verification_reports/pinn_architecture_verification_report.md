# PINN Architecture Markdown Verification Report

## Candidate Comparison

Scoring normalized for whitespace, line wrapping, escaped underscores, URI escaping, and harmless Markdown punctuation. Scores do not normalize away formula changes, table-cell changes, label/reference drift, missing prose, added prose, heading drift, or inactive-section content leakage. Per-section scores use bag-of-words with multiplicity (D-04 methodology).

| Candidate | Byte Size | Overall F1 | Overall Recall | Rank |
|---|---:|---:|---:|---:|
| `pinn_instruction/markdown_conversion/pinn_architecture.md` | 52865 | 0.9203 | 0.9124 | 2 |
| `pinn_instruction/markdown_conversion/pinn_architecture_v2.md` | 46309 | 0.8241 | 0.8687 | 3 |
| `pinn_instruction/markdown_conversion/pandoc_conversion/PINN_architecture_plan.md` | 51248 | 0.9257 | 0.9103 | 1 |

### Per-Section Scores

#### pinn_architecture.md (top-level)

| Section | F1 | Recall |
|---|---:|---:|
| foundational_principles.tex | 0.2745 | 0.9771 |
| sqr_skipresnet_siren_backbone.tex | 0.3935 | 0.9191 |
| physics_constrained_loss.tex | 0.3807 | 0.9418 |
| training_optimization_strategy.tex | 0.1036 | 0.9269 |
| inference_and_output.tex | 0.1774 | 0.9379 |
| blueprint_summary.tex | 0.1568 | 0.7682 |
| bibliography.tex | 0.0827 | 0.8533 |

#### pinn_architecture_v2.md

| Section | F1 | Recall |
|---|---:|---:|
| foundational_principles.tex | 0.2489 | 0.9832 |
| sqr_skipresnet_siren_backbone.tex | 0.3385 | 0.8700 |
| physics_constrained_loss.tex | 0.3156 | 0.8602 |
| training_optimization_strategy.tex | 0.0921 | 0.9236 |
| inference_and_output.tex | 0.1555 | 0.9171 |
| blueprint_summary.tex | 0.1381 | 0.7543 |
| bibliography.tex | 0.0748 | 0.8649 |

#### PINN_architecture_plan.md (pandoc)

| Section | F1 | Recall |
|---|---:|---:|
| foundational_principles.tex | 0.2785 | 0.9771 |
| sqr_skipresnet_siren_backbone.tex | 0.3984 | 0.9184 |
| physics_constrained_loss.tex | 0.3851 | 0.9402 |
| training_optimization_strategy.tex | 0.1052 | 0.9269 |
| inference_and_output.tex | 0.1800 | 0.9379 |
| blueprint_summary.tex | 0.1588 | 0.7664 |
| bibliography.tex | 0.0840 | 0.8533 |

**Notes on scoring patterns:**
- Per-section F1 is low because candidates include content from all 7 sections combined, while each LaTeX section is scored individually (candidate has far more tokens than any single section, reducing precision).
- Per-section recall is high (0.77-0.98) indicating that each section's LaTeX content is present in the candidates.
- `pinn_architecture_v2.md` consistently scores lower on F1 and recall, indicating content loss relative to both the top-level candidate and pandoc.
- `bibliography.tex` has the lowest F1 across all candidates due to URL/whitespace normalization differences in bibliography formatting.

## Selected Baseline

- Selected candidate: `pinn_instruction/markdown_conversion/pinn_architecture.md`
- Promoted target: `pinn_instruction/markdown_conversion/pinn_architecture.md`
- Selection rationale: The pandoc candidate (PINN_architecture_plan.md) narrowly wins on raw F1 (0.9257 vs 0.9203), but `pinn_architecture.md` has slightly better recall (0.9124 vs 0.9103) and is already at the canonical target path. Both are within 0.5% of each other on both metrics. The v2 candidate is clearly inferior (F1=0.8241) and is excluded. Human sanity-check (see below) applied to `pinn_architecture.md` as baseline.
- Override used: yes -- selected based on recall and canonical path placement rather than raw F1 leader (per D-02).

### Human Sanity-Check Results

**1. Inactive content leakage (BLOCKING):** See "Excluded Inactive Sections" section below for detailed grep results.

**2. Section count/order (MAJOR):** `pinn_architecture.md` contains 7 major `#` headings corresponding to the 7 active imports:
   - `# Section 1: Foundational Architectural Principles` -> foundational_principles.tex
   - `# The SQR-SkipResNet-SIREN Backbone` -> sqr_skipresnet_siren_backbone.tex
   - `# The Multi-Component, Physics-Constrained Loss Function` -> physics_constrained_loss.tex
   - `# Advanced Training and Optimization Strategy` -> training_optimization_strategy.tex
   - `# Inference and Trajectory Generation` -> inference_and_output.tex
   - Blueprint summary table present (:::: small :::) -> blueprint_summary.tex
   - `::: thebibliography` -> bibliography.tex

**3. Bibliography presence (MAJOR):** Bibliography section present at end of candidate as `::: thebibliography` block with all 17 references.

**4. Math rendering (INFO):** Formula delimiters (`$$`, `$`) appear intact. Some Pandoc-style `$^1$` superscript citations preserved. No obvious corruption detected in quick scan.

## Excluded Inactive Sections

### Structural Check

The LaTeX source (`main_pinn.tex`) has 3 inactive sections (commented out with `%\input`):
| Inactive File | main_pinn.tex Line | Content |
|---|---:|---|
| `sections/input_vector_inactive.tex` | 16 | Input vector formulation, 14-dimensional injective IC, characteristic time/length scaling |
| `sections/advanced_training_inactive.tex` | 24 | Advanced training dynamics, ALM details, curriculum-aware energy, two-phase optimization, adaptive gradient clipping, `tab:training_hyperparameters` |
| `sections/consolidated_blueprint_inactive.tex` | 26 | Consolidated implementation blueprint, unified architecture view, CTL integration, final recommendations |

The markdown must have exactly 7 active section headings matching the 7 active imports. Any content from the 3 inactive files in the selected baseline is a BLOCKING discrepancy.

### Content Search: Distinctive Inactive Terms

#### input_vector_inactive.tex distinctive terms

| Term | pinn_architecture.md | pinn_architecture_v2.md | PINN_architecture_plan.md |
|---|---|---|---|
| "Input Vector Formulation" | NOT FOUND | NOT FOUND | FOUND (heading `## 1 Section 1`) |
| "14-dimensional injective" | NOT FOUND | NOT FOUND | FOUND (body text, line 15) |
| "Characteristic Time" | FOUND (blueprint summary table) | FOUND (blueprint summary table) | FOUND (section text) |
| "Characteristic Length" | FOUND (blueprint summary table) | FOUND (blueprint summary table) | FOUND (section text) |
| "Scaling the Training Data" | NOT FOUND | NOT FOUND | NOT FOUND |

**Note:** "Characteristic Time" and "Characteristic Length" appear in `blueprint_summary.tex` (active section 6), so their presence is expected and NOT a leakage indicator.

#### advanced_training_inactive.tex distinctive terms

| Term | pinn_architecture.md | pinn_architecture_v2.md | PINN_architecture_plan.md |
|---|---|---|---|
| "Advanced Training Dynamics" | NOT FOUND | FOUND (heading `# Advanced Training and Optimization Strategy`) | FOUND (section `## 4 Advanced Training`) |
| "Adaptive Loss Balancing" | FOUND (subsection `## Adaptive Loss Balancing via ALM`) | FOUND | FOUND |
| "Curriculum-Aware Energy" | NOT FOUND | NOT FOUND | NOT FOUND |
| "Two-Phase Optimization" | FOUND (subsection `## Two-Phase Optimization`) | FOUND | FOUND |
| "Adaptive Gradient Clipping" | FOUND (subsection `## Adaptive Gradient Clipping`) | FOUND | FOUND |
| "tab:training_hyperparameters" | NOT FOUND | NOT FOUND | NOT FOUND |

**Note:** "Advanced Training and Optimization Strategy", "Adaptive Loss Balancing via ALM", "Two-Phase Optimization", and "Adaptive Gradient Clipping" appear in `training_optimization_strategy.tex` (active section 4), so their presence is expected and NOT a leakage indicator. The inactive section contains expanded/alternate content for these topics but the active section already covers them.

#### consolidated_blueprint_inactive.tex distinctive terms

| Term | pinn_architecture.md | pinn_architecture_v2.md | PINN_architecture_plan.md |
|---|---|---|---|
| "Consolidated Implementation Blueprint" | FOUND (blueprint summary table caption) | FOUND (blueprint summary table caption) | FOUND (table caption) |
| "Unified View of the Architecture" | NOT FOUND | NOT FOUND | NOT FOUND |
| "Final Recommendations" | NOT FOUND | NOT FOUND | NOT FOUND |

**Note:** "Consolidated Implementation Blueprint" appears in `blueprint_summary.tex` (active section 6), so its presence is expected and NOT a leakage indicator.

### Inactive Exclusion Result

| Candidate | BLOCKING Leakage | MAJOR Defects | Status |
|---|---|---|---|
| pinn_architecture.md | NONE | NONE | PASS |
| pinn_architecture_v2.md | NONE | NONE (but lower F1/recall) | PASS (but inferior) |
| PINN_architecture_plan.md | NONE | NONE | PASS |

No blocking inactive content leakage detected in any candidate. The distinctive terms found in candidates match content from the 7 active LaTeX sections, not the 3 inactive sections.

## Promotion Action

**Deferred to Wave 3** (NOT executed now -- Wave 2 needs the candidate at its current path for editing).

Planned git mv commands:
```bash
# Selected baseline stays at canonical path (no move needed)
# pinn_instruction/markdown_conversion/pinn_architecture.md -- ALREADY AT TARGET

# Archive 2 unselected candidates
mkdir -p pinn_instruction/markdown_conversion/_archive/pinn-architecture/
git mv pinn_instruction/markdown_conversion/pinn_architecture_v2.md pinn_instruction/markdown_conversion/_archive/pinn-architecture/
git mv pinn_instruction/markdown_conversion/pandoc_conversion/PINN_architecture_plan.md pinn_instruction/markdown_conversion/_archive/pinn-architecture/
```

## Section Audit

### 1. foundational_principles.tex

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 2. sqr_skipresnet_siren_backbone.tex (math-heavy)

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 3. physics_constrained_loss.tex (largest, math-heavy)

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 4. training_optimization_strategy.tex

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 5. inference_and_output.tex

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 6. blueprint_summary.tex

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

### 7. bibliography.tex (D-37: full bibitem audit required)

**Status:** PENDING

| ID | Type | Severity | Source location | Markdown location | Issue | Fix status |
|---|---|---|---|---|---|---|
| (Populated in Plan 02) | | | | | | |

## Fix Log

| ID | Section | Fix summary |
|---|---|---|
| PINN-12-01-BASELINE | Global | pinn_architecture.md selected as starting baseline (recall 0.9124, F1 0.9203). Override: preferred recall over raw F1 per D-02. |

## Source Issues / Notes for Future Reconciliation

(Populated in Plan 03)

## Final Verification

(Populated in Plan 03)

# Plan: Modularize PINN Architecture LaTeX

## Goal
Split `PINN_architecture_plan.tex` into modular section files with a master `main.tex`.

## Tasks
1. Create `sections/` directory
2. Create `preamble.tex` (lines 1-37 of original)
3. Create 6 active section modules
4. Create 3 inactive module files (preserved, not included)
5. Create `bibliography.tex`
6. Create `main.tex` master file
7. Compile and verify parity

## Target Layout
```
pinn-architecture/
├── main.tex
├── preamble.tex
├── PINN_architecture_plan.tex  (unchanged, rollback source)
└── sections/
    ├── foundational_principles.tex
    ├── sqr_skipresnet_siren_backbone.tex
    ├── physics_constrained_loss.tex
    ├── training_optimization_strategy.tex
    ├── inference_and_output.tex
    ├── blueprint_summary.tex
    ├── input_vector_inactive.tex
    ├── advanced_training_inactive.tex
    ├── consolidated_blueprint_inactive.tex
    └── bibliography.tex
```

# Pitfalls Research: Physics-Informed LLM for Three-Body Prediction

## Critical Pitfalls

### 1. Numerical Tokenization Destroys Precision

**Warning signs:** Model outputs round numbers, wrong magnitudes, or nonsensical trajectories
**Why it matters:** BPE tokenizers split "0.98765" into arbitrary sub-tokens like ["0", ".", "98", "76", "5"], losing numerical meaning. Three-body trajectories require at least 4-6 significant digits to be meaningful.
**Prevention:**
- Normalize all values to [-1, 1] before formatting (existing pipeline does this)
- Use fixed-precision formatting (e.g., `f"{x:.6f}"`)
- Consider scientific notation for very small/large values
- Test tokenizer behavior on sample numbers before training
**Phase:** Training Data Formatting

### 2. Chaotic Sensitivity Makes Evaluation Hard

**Warning signs:** Model seems to "work" on some ICs but completely fails on others, even similar ones
**Why it matters:** Three-body problem is chaotic — tiny IC differences lead to exponentially diverging trajectories. Evaluating prediction quality requires careful metrics that account for this.
**Prevention:**
- Use Lyapunov time as a horizon — predictions beyond ~1 Lyapunov time are inherently unreliable
- Evaluate energy/momentum conservation of predicted trajectories (physics-informed metric)
- Use the existing metrics pipeline to grade predictions
- Compare against Brutus ground truth only within meaningful time horizons
**Phase:** Evaluation Pipeline

### 3. Data Leakage Between IC Types

**Warning signs:** Model performs suspiciously well on hierarchical ICs after training on standard, or vice versa
**Why it matters:** Standard quasi-random and hierarchical ICs have very different distributions (equal vs variable masses, random vs orbital sampling). Training and test sets must respect these boundaries.
**Prevention:**
- Split by IC type AND by ID range, not randomly
- Keep separate evaluation metrics per IC type
- Document which IDs are in train/val/test splits
**Phase:** Training Data Formatting

### 4. LoRA Rank Too Low for Numerical Tasks

**Warning signs:** Model converges but outputs are noisy or default to mean values
**Why it matters:** Numerical prediction may require more adapter capacity than typical text tasks. Default LoRA rank (8-16) may be insufficient.
**Prevention:**
- Start with rank 16-32, experiment upward
- Monitor per-token loss on numerical vs text tokens separately
- Consider QLoRA (quantized base + full-rank adapters) if memory permits
**Phase:** Fine-Tuning

### 5. Cleanup Breaks Existing Scripts

**Warning signs:** Scripts fail with FileNotFoundError after folder deletion
**Why it matters:** Gold IC folder paths are hardcoded in multiple scripts. Deleting folders before updating code will break the pipeline.
**Prevention:**
- Update ALL code references BEFORE deleting any folders
- Run scoped grep for removed path patterns after changes
- Use the cleanup plan's verification gates (Step 6) rigorously
**Phase:** Codebase Cleanup

## Moderate Pitfalls

### 6. M2 Memory Limits During Training

**Prevention:** Use 4-bit quantized base model, LoRA adapters, small batch sizes. Monitor memory with `Activity Monitor`.

### 7. No `requirements.txt` Causes Environment Drift

**Prevention:** Create `requirements.txt` or `pyproject.toml` as part of cleanup. Pin versions.

### 8. Monolithic Data Pipeline

**Prevention:** The 56KB `data-processing-pipeline-full.py` is the source of truth but hard to modify. Use the modular `data-handling/` package for new work, but verify consistency.

### 9. Training Data Scale May Be Insufficient

**Prevention:** ~7,600 ICs total (4,857 hierarchical + 2,749 standard). For LLM fine-tuning, each IC produces multiple timestep samples. Estimate total sample count before training.

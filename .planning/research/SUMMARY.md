# Research Summary

## Stack

**Recommended:** MLX (`mlx-lm`) with LoRA fine-tuning on Qwen 3.5 2B 4-bit.

Native Apple Silicon optimization, already downloaded. LoRA is memory-efficient enough for M2 Mac. Training data formatted as JSONL. The existing PINN preprocessing pipeline (normalization to [-1,1]) is directly reusable.

**Critical risk:** Numerical tokenization. BPE tokenizers fragment numbers, destroying precision. Mitigation: fixed-precision formatting, pre-normalization, test tokenizer behavior before training.

## Table Stakes

1. **Codebase cleanup** — Consolidate gold IC folders, externalize raw ICs, update docs
2. **Data pipeline verification** — Confirm existing preprocessing works end-to-end
3. **Training data conversion** — Simulation data → JSONL format for LLM training
4. **LoRA fine-tuning script** — Train Qwen 3.5 2B on trajectory prediction
5. **Basic evaluation** — MSE on held-out trajectories, conservation error

## Watch Out For

1. **Numerical tokenization** — Biggest technical risk; standard BPE destroys precision
2. **Chaotic sensitivity** — Predictions beyond Lyapunov time are inherently unreliable
3. **Data leakage** — Split by IC type AND ID range, not randomly
4. **LoRA rank** — May need rank 16-32+ for numerical tasks (higher than typical text)
5. **Cleanup ordering** — Update code BEFORE deleting folders; gold paths are hardcoded everywhere

## Architecture

Three-layer system: existing validated simulation pipeline → new training data formatter → new MLX fine-tuning + evaluation. Clean boundary between existing and new code.

## Build Order

1. Codebase cleanup (independent)
2. Data pipeline verification
3. Training data formatter
4. Fine-tuning script
5. Evaluation pipeline

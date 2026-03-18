# Stack Research: Physics-Informed LLM for Three-Body Prediction

## Recommended Stack

### Core Training Framework

| Component | Recommendation | Confidence | Rationale |
|-----------|---------------|------------|-----------|
| **ML Framework** | MLX (`mlx-lm`) | High | Native Apple Silicon optimization, unified memory, 1.8-2x faster than llama.cpp |
| **Base Model** | Qwen 3.5 2B 4-bit | High | Already downloaded; MLX-compatible; small enough for M2 Mac fine-tuning |
| **Fine-tuning** | LoRA via `mlx-lm` | High | Memory-efficient; freezes most weights; proven for domain adaptation |
| **Data Format** | JSONL (chat/completion) | High | Standard for `mlx-lm` fine-tuning; well-documented |

### Key Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `mlx` | ≥0.20 | Apple's ML framework for Silicon |
| `mlx-lm` | latest | LLM fine-tuning and inference on MLX |
| `transformers` | ≥4.40 | Tokenizer and model loading |
| `numpy` | existing | Data preprocessing |
| `h5py` | existing | Reading preprocessed simulation data |

### Alternative Approaches — NOT Recommended

| Tool | Why Not |
|------|---------|
| PyTorch + CUDA | No NVIDIA GPU on M2 Mac |
| Unsloth | Great for NVIDIA GPUs, limited Apple Silicon support |
| Full fine-tuning | Memory-prohibitive for 2B params on M2 |
| Larger models (7B+) | Won't fit in M2 memory for training |

## Numerical Tokenization — Critical Challenge

Standard LLM tokenizers (BPE) fragment numbers into arbitrary sub-tokens, destroying numerical meaning. This is the **biggest technical risk** for trajectory prediction.

### Strategies (ordered by feasibility)

1. **Pre-processing normalization** — Format all numbers to fixed precision, normalize to [-1, 1] range (already done in PINN pipeline), space-separate digits. Lowest effort, moderate effectiveness.
2. **xVal continuous tokenization** — Encode each number as a single token preserving magnitude. Requires model architecture changes. High effectiveness, high effort.
3. **BitTokens** — IEEE 754 binary representation per number. Experimental, high effort.

**Recommendation:** Start with strategy 1 (pre-processing). The existing PINN data pipeline already normalizes to [-1, 1]. Format as structured text prompts with fixed-precision numbers.

## Data Pipeline Integration

```
Existing Brutus data → existing PINN preprocessing → normalized IC vectors + trajectories
    → NEW: format as JSONL training pairs → mlx-lm LoRA fine-tuning
```

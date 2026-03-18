# Architecture Research: Physics-Informed LLM for Three-Body Prediction

## System Architecture

The project has three major subsystems with clear boundaries:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXISTING (Validated)                         │
│                                                                     │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────┐              │
│  │ IC Generator │───▶│ Prescreening │───▶│  Brutus   │              │
│  │  (Python)    │    │  (Python)    │    │  (C++)    │              │
│  └─────────────┘    └──────────────┘    └─────┬─────┘              │
│                                               │                     │
│                                    ┌──────────▼──────────┐         │
│                                    │ Metrics Extraction   │         │
│                                    │ (Python)             │         │
│                                    └──────────┬──────────┘         │
│                                               │                     │
│                                    ┌──────────▼──────────┐         │
│                                    │ Data Preprocessing   │         │
│                                    │ (IC vector, norms)   │         │
│                                    └──────────┬──────────┘         │
└───────────────────────────────────────────────┼─────────────────────┘
                                                │
┌───────────────────────────────────────────────┼─────────────────────┐
│                         NEW (To Build)        │                     │
│                                               │                     │
│                                    ┌──────────▼──────────┐         │
│                                    │ Training Data        │         │
│                                    │ Formatter (→ JSONL)  │         │
│                                    └──────────┬──────────┘         │
│                                               │                     │
│                                    ┌──────────▼──────────┐         │
│                                    │ MLX LoRA Fine-Tuning │         │
│                                    │ (Qwen 3.5 2B)       │         │
│                                    └──────────┬──────────┘         │
│                                               │                     │
│                                    ┌──────────▼──────────┐         │
│                                    │ Evaluation Pipeline  │         │
│                                    └─────────────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Boundaries

### Existing Components (Do Not Modify)
- **Brutus integrator** — C++ binary, works as-is
- **IC generation** — Python scripts, stable
- **Prescreening** — Python, stable
- **Brutus runners** — Python batch scripts (path updates needed for cleanup)

### Components to Clean Up
- **Data folder structure** — Consolidate gold IC folders
- **Path references** — Update scripts/docs pointing to removed folders
- **Validation logic** — Add subset-aware standard-gold handling

### New Components to Build

#### Training Data Formatter
- **Input:** Preprocessed IC vectors (13 components) + Brutus trajectory data
- **Output:** JSONL files for `mlx-lm` fine-tuning
- **Format decision:** Structured text prompt with normalized numbers
- **Location:** `pinn/` or new `training/` directory

#### Fine-Tuning Script
- **Input:** JSONL training data + Qwen 3.5 2B base model
- **Output:** LoRA adapter weights
- **Framework:** `mlx-lm` with LoRA configuration
- **Location:** New `training/` directory

#### Evaluation Pipeline
- **Input:** Fine-tuned model + held-out test ICs
- **Output:** Accuracy metrics, conservation error analysis
- **Location:** New `training/` or `evaluation/` directory

## Data Flow for Training

```
IC file (3×7 fields) → parse → 13-component IC vector (normalized [-1,1])
Brutus output → parse → trajectory snapshots at dt_out intervals

Combined → JSONL prompt format:
  {"prompt": "IC: m1=0.33 m2=0.33 m3=0.33 E=-0.52 ... t=0.08",
   "completion": "x1=0.987 y1=0.012 z1=-0.003 x2=... y2=... z2=... x3=... y3=... z3=..."}
```

## Build Order

1. **Codebase cleanup** (independent — no new code dependencies)
2. **Data pipeline verification** (ensure existing preprocessing works)
3. **Training data formatter** (depends on verified data pipeline)
4. **Fine-tuning script** (depends on formatted training data)
5. **Evaluation pipeline** (depends on trained model)

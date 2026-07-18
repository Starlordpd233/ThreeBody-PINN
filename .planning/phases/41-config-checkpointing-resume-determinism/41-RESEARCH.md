# Phase 41: Config, Checkpointing, Resume & Determinism - Research

**Researched:** 2026-07-18
**Domain:** PyTorch 2.12 training-control layer (YAML config resolution, atomic checkpointing, resume/rollback, auto-guards, RNG/determinism) on Apple-silicon MPS
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **CTX-50 (fills CTX-42):** YAML parsing = `yaml.safe_load` (PyYAML). Keyed `run/stage/opt/loss` (+precision/device) sections map onto the CTX-42 nested frozen dataclasses field-for-field; each sub-config validates its own invariants at construction. A missing required section or an unknown/misspelled key raises a typed error naming the offending path (fail-closed). Planner/researcher confirms PyYAML is in the `pinn-train` env (**confirmed this session: PyYAML 6.0.3 present**); no bespoke parser.
- **CTX-51:** Frozen resolved copy — after resolution the fully-resolved config is written verbatim to `runs/<name>/config.yaml` via the same atomic path as checkpoints (CTX-55), at run start. Re-parsing yields a `TrainingConfig` equal to the one that ran.
- **CTX-52 (Entry Point, Option A):** `python -m pinn.train --config <c> [--resume <ckpt>] [--hold-stage]` (argparse). Wires: resolve config → `resolve_runtime` (CTX-20, sole precision/device source) → `build_network` → Phase-40 `CurriculumController`/`RunController` → `CheckpointStore` → run. Emits the minimal step log (step, five loss terms, total, lr) through the CTX-45 logger tree.
- **CTX-53 (fills CTX-43; CTX-44 composition):** Payload schema = a `weights_only`-clean nested dict keyed by component: `model`, `optimizer` (active optimizer state_dict — Adam; L-BFGS state never crosses a boundary), `scheduled_weights`, `grad_clip`, `curriculum` (stage index, phase 2a/2b, per-stage epoch/step, disposition-log pointer), `rng` (four streams — torch, torch.mps, numpy, python `random`), `counters` (global step/epoch, wall-clock baseline), `config_identity` (sha256 digest of canonicalized identity fields + resolved config as plain dict), `schema_version` (int). All plain tensors/containers/scalars/strings.
- **CTX-54:** Retention under `runs/<name>/checkpoints/`: rolling `step-{step:06d}.pt` (keep newest 3 by step), `best.pt` (on validation improvement), `latest.pt` (atomic-rename **copy**, not symlink), anchors `stage-{k}-final.pt`+`stage-{k+1}-init.pt` (excluded from rolling deletion). Dual trigger: every N steps OR wall-clock ceiling, whichever fires first; coincident triggers → exactly one write (guarded by last-written-step).
- **CTX-55:** Atomicity + fallback — every write goes to `*.tmp` in the same dir → `fsync` (file + dir) → `os.replace` (atomic rename); loads use `weights_only=True`. On missing/corrupt `latest.pt`, a fallback scan loads the newest structurally-valid `step-*.pt`/anchor, or raises a typed "no valid checkpoint" error naming the directory.
- **CTX-56:** `curriculum.jsonl` at `runs/<name>/curriculum.jsonl` — append one JSON line per promotion/RECOVER/HALT disposition, chronological. Idempotent keyed by `(from_stage, to_stage, disposition, step)`. Promotion is ordered (k→k+1, no skip/regress; refuse otherwise).
- **CTX-57 (B-5, Conservative identity line):** Resume config-diff — Identity (must-match → refuse on change): architecture spec (layers/width/omega0/skip/LayerNorm), IC-vector definition + dataset version/hash, loss-catalog structure + physics constants (`D`, `eps_soft`), seed, **precision + device**, curriculum/stage definitions, split policy, **`MAX_EPOCHS`**, **guard/RECOVER thresholds (R-1)**. Operational (may differ → allow): checkpoint cadence (`N`-steps) + wall-clock ceiling (D4-a); pure-runtime knobs (log frequency, validation cadence, num workers). Unclassified → refuse (fail-safe, locked). Diff compares the incoming config's identity-field digest against the checkpoint's. Owner-noted implication: extending `MAX_EPOCHS` or hot-tuning thresholds on resume refuses — needs a new run.
- **CTX-58:** `--hold-stage` rollback — `--resume <…/stage-{k}-final.pt> --hold-stage` re-enters stage `k` instead of advancing; same anchor without `--hold-stage` proceeds to advance. Missing `--resume` path → typed error naming the path.
- **CTX-59:** Exact continuation — resume restores model + optimizer + schedule + grad-clip + RNG + counters so the continued trajectory matches an uninterrupted run to the same step (floating tolerance). Adam boundary reset preserved: restoring from `stage-{k+1}-init.pt` starts with reset Adam state + empty L-BFGS history.
- **CTX-60:** Guard layer = a per-step guard callback invoked inside the RunController step. Tier-1 (NaN/Inf grad/loss → RECOVER), Tier-2 (loss-explosion vs a ⚖ ceiling, disk-floor, memory-watermark → RECOVER/HALT per family). Thresholds are ⚖ config seams (calibrated at Phase-43 pilot). RECOVER/HALT route through the existing stage-exit machine. Step-0 trips handled (no ordering assumption); simultaneous trips produce one coherent bundle.
- **CTX-61 (`failure/` bundle, Claude's decision):** Always-on, written to `runs/<name>/failure/` on ANY guard trip, tiered: Tier-A (always, tiny) `README.txt` (one line: guard/step/stage/reason) + `trip.json` (guard name, tier, step, stage, phase 2a/2b, timestamp, tripped metric+value+⚖threshold, disposition, last loss terms + grad-norm as scalars). Tier-B (best-effort) `tail.log` (~200 lines) + reference to last-good checkpoint + reference to frozen `config.yaml`. No raw tensor/grad dumps by default.
- **CTX-62:** Seed/RNG recording — the four RNG streams (torch, torch.mps, numpy, python `random`) captured into the frozen config AND every checkpoint (CTX-44 `rng` key) and restored on resume. Production fp32-MPS at a fixed seed → statistical equivalence across fresh runs; resume → exact continuation.
- **CTX-63 (`strict_cpu_determinism`, Claude's decision):** A config/CLI DEBUG switch, default OFF. When ON: force `device=cpu`, `torch.use_deterministic_algorithms(True)`, `torch.set_num_threads(1)`, re-seed all four streams from the recorded seed. Not guaranteed bitwise across machines/torch versions. Off by default (production keeps fp32-MPS speed + statistical-equivalence scope).
- **CTX-64:** Reproducibility honesty — the run's own reporting states the scope as statistical-equivalence + exact-checkpoint-continuation, never bitwise.

### Claude's Discretion

- Exact module filenames within `pinn/training/` (a config-YAML mapper, a checkpoint-store impl, a guards module, a determinism helper) — must EXTEND the existing `config.py`/`checkpoint.py` seams and not collide with v1.3-era files.
- The identity-digest canonicalization (JSON canonical sort-keys → sha256).
- `argparse` structure of `pinn.train`; the exact `N` for the failure `tail.log`.
- Whether `latest.pt` is a copy vs hardlink is FIXED to copy (CTX-54); only internal write ordering is discretion.

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope. Scope-creep candidates (canonical JSONL/TensorBoard surface, threshold calibration) are already assigned to Phases 42/43 by the roadmap, not deferred here. Two reviewed-but-not-folded todos: `d-06-static-epsilon-sensitivity-check.md` (Phase 38/43 territory) and `trainex-r1-research-handoff.md` (research-process, no code surface).

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-------------------|
| CTRL-01 | Single YAML config keyed `run/stage/opt/loss` drives every run; fully-resolved config frozen into run folder | See Standard Stack (PyYAML), Architecture Patterns Pattern 1 (config mapper), Common Pitfalls 1 (tuple/list round-trip), Code Examples 1 |
| CTRL-02 | Dual-trigger checkpoint cadence + rolling-3/best/latest/anchor retention | Architecture Patterns Pattern 4 (the missing per-step hook), Code Examples 3 (dual-trigger sketch), Common Pitfalls 3 |
| CTRL-03 | Atomic, `weights_only`-clean writes + fallback scan | Standard Stack (torch.save/load), Code Examples 2 (verified atomic round-trip), Don't Hand-Roll 1 |
| CTRL-04 | Stage anchors + idempotent ordered promotion + `curriculum.jsonl` | Architecture Patterns Pattern 3, Common Pitfalls 4 (JSONL append atomicity + idempotency check) |
| CTRL-05 | `--resume`/`--hold-stage`/fail-safe config-diff | Architecture Patterns Pattern 2 (identity digest sourcing), Open Questions 1 |
| CTRL-06 | Complete Adam reset at stage boundaries | Architecture Patterns Pattern 4 (optimizer exposure gap), Common Pitfalls 5 |
| CTRL-07 | Tier-1+2 auto-guards + RECOVER/HALT + `failure/` bundle | Architecture Patterns Pattern 4/5, Environment Availability (no psutil), Code Examples 4 |
| CTRL-08 | Full seed/RNG recording + statistical-equivalence repro + strict-CPU switch | Standard Stack (torch.mps RNG API, verified), Code Examples 2, Common Pitfalls 2 (two-seed confusion), Open Questions 2 |

</phase_requirements>

## Project Constraints (from CLAUDE.md)

- **Governance:** v2.0 is a build milestone; owner-carved seams (D4-a ceiling, R-1 guard thresholds, B-5 field list) MUST ship as clearly-marked ⚖ placeholders, never presented as ratified. Do not invent numeric values for these — surface evidence only.
- **Branch discipline:** build code lives in `.worktrees/trainex` on `milestone/v2.0`; never commit v2.0 build code to `master`.
- **Git commit protocol:** use `scripts/agent-commit` with `GIT_AGENT_ID`/`GIT_AGENT_OWNED_PATHS`; conventional commit format `<type>(<scope>): <subject>`; body required for commits touching `.planning/` or multiple files.
- **`pinn/` live-code ban is LIFTED for v2.0** — this is the first milestone permitted to write production `pinn/` code (v1.3-era files remain reference-only, never imported).
- **Framework specs are read-only** in v2.0 (`ctl_instruction.md`, `pinn_architecture.md`) — a build-discovered spec defect is a gap, not an edit.
- **Test pattern:** `tests/phase41` stdlib-unittest with deferred-import skip guards (`_require(symbol, module)` idiom from `tests/phase40/test_prohibitions.py`), run via `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase41 -p 'test_*.py' -v`.

## Summary

Phase 41 wraps the Phase-40 `CurriculumController`/`RunController` training loop with four subsystems: (1) a keyed-YAML config resolver extending the existing frozen `TrainingConfig` dataclasses, (2) a production `CheckpointStore` replacing the naive `TorchSaveCheckpointStore` behind the same Protocol, (3) a resume/rollback/guard layer, and (4) full RNG-state capture for statistical-equivalence + exact-continuation reproducibility. Every piece of PyTorch mechanics this phase needs (`torch.save`/`torch.load(weights_only=True)`, `torch.mps.get_rng_state()`/`set_rng_state()`, `torch.use_deterministic_algorithms`) was verified **empirically in the actual `pinn-train` conda environment** (torch 2.12.1, PyYAML 6.0.3, numpy 2.4.6) in this research session — a full atomic-write round-trip of a nested payload containing all four RNG streams (torch tensor, MPS tensor, numpy `Generator.bit_generator.state` dict, python `random.getstate()` tuple) through `weights_only=True` succeeded without modification.

The single most consequential finding is architectural, not library-level: **the Phase-40 `RunController.run_stage(k)` runs an entire stage as one monolithic Python call with no per-step checkpoint hook, no optimizer exposed in `state_dict()`, and no RNG state exposed in `state_dict()`, and no global (cross-stage) step counter exists anywhere.** CTRL-02's dual-trigger cadence, CTRL-03's mid-stage atomic writes, and CTRL-08's "exact next-step RNG draws" all require checkpointing *during* a stage, not just at stage boundaries — so Phase 41 cannot be purely additive new files; it must also edit `pinn/training/controllers.py` to add a per-step checkpoint-trigger call site, expose the live Adam optimizer, expose the `RunController._rng` numpy Generator's state, and thread a global step counter through `CurriculumController`. This is expected scope (Phase 40's docstrings explicitly flag these as Phase-41 seams: "the checkpoint payload builds directly on this") but the planner must schedule it as its own task, not assume it falls out of `checkpoint.py` alone.

The codebase already has an established, three-times-repeated atomic-write idiom (`_atomic_write` in `pinn/data/stage_scan.py`, `pinn/data/splits.py`, `pinn/verification/*_probe.py`: write to `path.tmp.{pid}` → flush → `fsync(file)` → `os.replace` → `fsync(dir)`) that CTX-55 should extend for binary `torch.save` payloads rather than inventing a new pattern.

**Primary recommendation:** Extend `pinn/training/config.py` with a YAML mapper module and precision/device fields on `RunConfig`; extend `pinn/training/checkpoint.py` with a production `CheckpointStore` built on the existing `_atomic_write` idiom generalized to binary payloads; add a per-step checkpoint/guard hook plus optimizer/RNG state exposure directly inside `pinn/training/controllers.py` (RunController); build `pinn.train` as a single-file module (`pinn/train.py`, mirroring `pinn/data/stage_scan.py`'s `argparse` + `main(argv) -> int` convention) so `python -m pinn.train` resolves it directly.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| YAML config parsing + validation | Training-control layer (`pinn/training/config.py` + new mapper) | — | Single-process CLI tool, no client/server split; config resolution is a pure function of the YAML file |
| Frozen resolved-config freeze | Training-control layer | Filesystem (`runs/<name>/config.yaml`) | Atomic write is a filesystem contract shared with checkpoints |
| Checkpoint persistence (atomic/retention/fallback) | Training-control layer (`CheckpointStore` impl) | Filesystem (`runs/<name>/checkpoints/`) | `CheckpointStore` Protocol already isolates this from `RunController`/`CurriculumController` |
| Optimizer/RNG state capture | Training-loop layer (`RunController`, extended) | Training-control layer (composes into the payload) | The state lives inside the loop object; only the loop can snapshot it — the checkpoint layer composes, it does not own, this state |
| Resume config-diff (identity/operational classification) | Training-control layer (new identity/resume module) | Science layer (`pinn.constants`, `pinn.architecture_spec` — read for identity fields) | The diff logic is control-layer, but several identity fields (architecture, physics constants) are DEFINED in the science layer, not in `TrainingConfig` |
| Auto-guards (NaN/Inf, loss-explosion, disk-floor, memory-watermark) | Training-loop layer (per-step callback invoked from `RunController`) | Training-control layer (guard module + `failure/` bundle writer) | Guards must observe live tensors/gradients each step (loop-owned), but the disposition/bundle-writing is control-layer |
| `pinn.train` CLI entry point | Training-control layer (`pinn/train.py`) | — | Thin composition root; wires config → runtime → network → controllers → checkpoint store |
| Determinism switch (`strict_cpu_determinism`) | Training-control layer (config + `pinn.train` startup) | Runtime layer (`pinn/runtime.py` — reads resolved precision/device) | The switch overrides the config's device/precision resolution at startup, before any tensor is built |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| PyTorch | 2.12.1 (confirmed installed in `pinn-train` env) | `torch.save`/`torch.load(weights_only=True)` checkpointing, `torch.mps.get_rng_state/set_rng_state`, `torch.use_deterministic_algorithms`, `torch.optim.Adam.state_dict()` | Already the project's ML framework (ratified D1); no alternative considered |
| PyYAML | 6.0.3 (confirmed installed in `pinn-train` env) | `yaml.safe_load`/`yaml.safe_dump` for the keyed config | B-9 ratified; `safe_load`/`safe_dump` never execute arbitrary YAML tags (unlike the unsafe `yaml.load`) |
| numpy | 2.4.6 (confirmed installed) | `numpy.random.Generator.bit_generator.state` capture/restore for the data-sampling RNG stream | Already the project's array/RNG library (`RunController._rng`, `CollocationSampler`) |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| stdlib `os` | builtin | `os.replace` (atomic rename), `os.fsync`, `os.open`/`os.close` for directory fsync | Every checkpoint/config/curriculum-ledger write (extends the existing `_atomic_write` idiom) |
| stdlib `json` | builtin | `curriculum.jsonl` line serialization, `trip.json` guard bundle | Plain-text, greppable, matches existing `pinn/data/stage_scan.py` JSON usage |
| stdlib `hashlib` | builtin | sha256 identity digest (CTX-53 `config_identity`) | Canonicalize (sort_keys JSON dump) then hash |
| stdlib `shutil` | builtin | `shutil.disk_usage(path).free` for the disk-floor guard | Cross-platform, no extra dependency; already informally used by the DATA-01 memory-accounting precedent |
| stdlib `resource` | builtin (POSIX only — macOS/Linux; this is a macOS-only project) | `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss` as a coarse process-memory proxy for the memory-watermark guard | Only if `torch.mps.driver_allocated_memory()` is judged insufficient (see Common Pitfalls 6 for the macOS-units gotcha) |
| stdlib `argparse` | builtin | `pinn.train` CLI (`--config`, `--resume`, `--hold-stage`) | Matches the exact convention already used by `pinn/data/stage_scan.py` (`_parser()` + `main(argv) -> int`) |
| stdlib `random` | builtin | Python global RNG stream capture (`random.getstate()`/`setstate()`) for CTX-62's fourth stream | Defensive/complete capture per B-11/D6; **verified this session that nothing in `pinn/` currently consumes the global `random` module** — capture is for completeness, not because current code needs it restored |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib `os.replace`+`fsync` atomic write | A third-party atomic-write library (e.g. `python-atomicwrites`) | Adds a dependency for something the codebase already implements correctly three times over (`stage_scan.py`, `splits.py`, `*_probe.py`); no reason to diverge |
| `psutil` for memory-watermark guard | `resource.getrusage()` / `torch.mps.driver_allocated_memory()` | **`psutil` is NOT installed in `pinn-train`** (confirmed this session); adding it is a new dependency for a single guard metric — prefer stdlib/torch-native first (see Environment Availability) |
| Hydra for config management | Plain `yaml.safe_load` + dataclass mapping (B-9 ratified) | Resolution doc §B-9 notes Hydra was named twice in `ctl_instruction.md` (once unmarked) as an R-4 spec-owner reconciliation item, but the keyed-YAML + frozen-copy approach was unanimously endorsed for the slice; Hydra migration remains mechanical if ever wanted later — not needed now |

**Installation:** No new packages required — PyYAML, numpy, and PyTorch are already present in the `pinn-train` conda environment (verified via `conda run -n pinn-train python -c "import torch, yaml, numpy"` in this session). If a fresh environment build is ever needed:

```bash
pip install torch pyyaml numpy  # torch/numpy already required by Phase 37/38/39/40
```

**Version verification:** Verified directly in the target environment this session (not from training data or a registry lookup):
```
torch 2.12.1
yaml (PyYAML) 6.0.3
numpy 2.4.6
torch.backends.mps.is_available() == True
```

## Package Legitimacy Audit

No NEW packages are introduced by this phase — PyYAML, numpy, and PyTorch are already installed and imported successfully in `pinn-train` (Phase 37/40 established this environment). The audit below covers PyYAML since it is the one library Phase 41 newly *imports in `pinn/` code* (Phase 40 never imported it).

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|--------------|---------|-------------|
| pyyaml | PyPI | Foundational Python YAML library, actively maintained since 2006 | Not resolvable by the legitimacy tool this session (`weeklyDownloads: null`) | `https://pyyaml.org/` (canonical project home; source at `github.com/yaml/pyyaml`) | `[SUS]` (tool-flagged: `unknown-downloads` only) | **Approved** — see note below |

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** `pyyaml` — flagged by the automated tool *solely* because its downloads statistic could not be retrieved (`unknown-downloads`), not because of any actual illegitimacy signal (no typosquat pattern, no missing repo, no suspicious postinstall, is the literal upstream project referenced by every Python YAML tutorial). This is a well-known, ubiquitous, 15+ year old package that is **already installed and directly verified working** in the `pinn-train` conda environment in this session (`import yaml; yaml.__version__ == '6.0.3'`). No new install action is required. Per protocol, the planner should still record this as a `checkpoint:human-verify` note if a *fresh* environment build is ever automated from a lockfile — but no task is needed for the current environment since the package is already present and functioning.

`npm view scripts.postinstall` is not applicable (PyPI ecosystem, not npm); `pip show pyyaml` in the target env would confirm metadata if further verification is wanted.

## Architecture Patterns

### System Architecture Diagram

```
                          runs/<name>/config.yaml (frozen, written at start)
                                     ▲
                                     │ atomic write (CTX-51/55)
                                     │
YAML file  ──► yaml.safe_load ──► field-for-field ──► TrainingConfig ──┐
(--config)      (dict)              mapper (new)      (existing,       │
                                     [unknown-key       CTX-42)         │
                                      fail-loud]                        │
                                                                        ▼
CLI (--resume/--hold-stage) ──► identity digest ──► resume config-diff ──► pinn.train (new, pinn/train.py)
                                  (sha256, new)        (CTX-57, new)         │  resolve_runtime(precision, device)
                                                                             │  build_network(ArchitectureSpec)
                                                                             ▼
                                                            CurriculumController (existing, extended)
                                                                             │  step() dispatch
                                                                             ▼
                                                            RunController (existing, EXTENDED:
                                                            + optimizer exposed in state_dict
                                                            + rng exposed in state_dict
                                                            + per-step checkpoint/guard hook)
                                                                 │           │
                                          per-step guard check   │           │ every N steps / wall-clock ceiling
                                          (NaN/Inf, loss-        │           ▼
                                          explosion, disk,    ┌──┴───►  CheckpointStore (new production impl,
                                          memory)              │        same Protocol as Phase 40's naive one)
                                                                │            │  atomic tmp→fsync→os.replace (CTX-55)
                                                                │            │  retention: rolling-3/best/latest/anchors
                                                                │            ▼
                                          on ANY trip:          │      runs/<name>/checkpoints/*.pt
                                          failure/ bundle  ◄────┘            │
                                          (Tier-A always,                   │ ADVANCE/RECOVER/HALT
                                           Tier-B best-effort)              ▼
                                                                curriculum.jsonl (append, idempotent by
                                                                (from_stage,to_stage,disposition,step))
```

### Recommended Project Structure

```
pinn/
├── train.py                       # NEW — python -m pinn.train entry point (argparse, main(argv)->int)
├── training/
│   ├── config.py                  # EXTEND — add precision/device fields to RunConfig; add checkpoint/guard/recover sub-config
│   ├── config_yaml.py              # NEW — yaml.safe_load + field-for-field mapper + frozen-copy writer (or fold into config.py; Claude's discretion)
│   ├── checkpoint.py               # REPLACE naive impl — production CheckpointStore (atomic/retention/fallback/curriculum.jsonl)
│   ├── resume.py                   # NEW — identity-digest computation + field-classified resume config-diff
│   ├── guards.py                   # NEW — Tier-1+2 auto-guard callbacks + failure/ bundle writer
│   ├── determinism.py              # NEW — strict_cpu_determinism switch + 4-stream RNG capture/restore helpers
│   └── controllers.py              # EXTEND (existing) — expose optimizer + rng in RunController.state_dict();
│                                    #                     add per-step checkpoint/guard hook; add global step counter
tests/phase41/
├── __init__.py                     # NEW (mirrors tests/phase40/__init__.py)
├── _fixtures.py                    # NEW — tiny synthetic Stage-0 loop fixtures (reuse tests/phase40/_fixtures.py patterns)
├── test_config_yaml.py
├── test_checkpoint.py
├── test_resume.py
├── test_guards.py
├── test_determinism.py
└── test_train_entrypoint.py        # end-to-end resume/guard checks (CTRL-01/02/05/08 falsifiability floor)
```

### Pattern 1: Field-for-field YAML → frozen dataclass mapping with fail-loud unknown keys

**What:** Walk the parsed YAML dict's top-level keys (`run`, `stage`, `opt`, `loss`) and construct each corresponding frozen dataclass via keyword expansion, but validate every key against `dataclasses.fields(cls)` first so a typo raises a typed error naming the exact dotted path (e.g. `"stage.mx_epochs"`), rather than `TypeError: unexpected keyword argument` (which does not name the dotted path or distinguish "extra key" from "wrong type").

**When to use:** CTRL-01's config resolution step, before constructing `TrainingConfig`.

**Example:**
```python
# Source: verified against pinn/training/config.py's existing dataclass shapes
# (this session, direct file read) + PyYAML docs (Context7 /websites/pytorch_2_12
# is PyTorch-specific; PyYAML behavior verified by direct execution this session).
import dataclasses
from typing import Any, Mapping, Type, TypeVar

T = TypeVar("T")


class ConfigKeyError(ValueError):
    """Raised for an unknown/misspelled config key, naming the dotted path."""


def _map_section(section_name: str, raw: Mapping[str, Any], cls: Type[T]) -> T:
    known = {f.name for f in dataclasses.fields(cls)}
    unknown = set(raw) - known
    if unknown:
        bad = sorted(unknown)[0]
        raise ConfigKeyError(
            f"{section_name}.{bad} is not a recognized {cls.__name__} field "
            f"(known: {sorted(known)})"
        )
    # NOTE (Common Pitfall 1): PyYAML round-trips python tuples as YAML
    # sequences, but yaml.safe_load ALWAYS returns them back as lists, never
    # tuples. Any dataclass field typed `tuple[...]` (e.g. OptConfig.adam_betas)
    # MUST be explicitly coerced here, or dataclass equality (used by the
    # CTRL-01 "re-parses equal" acceptance test) will fail list != tuple.
    coerced = dict(raw)
    for f in dataclasses.fields(cls):
        if f.type in ("tuple[float, float]",) and f.name in coerced:
            coerced[f.name] = tuple(coerced[f.name])
    return cls(**coerced)
```

### Pattern 2: Identity digest spans multiple modules, not just `TrainingConfig`

**What:** CTX-57's identity field list includes "architecture spec (layers/width/omega0/skip/LayerNorm)" and "loss-catalog structure + physics constants (`D`, `eps_soft`)" — but `ArchitectureSpec` (in `pinn/architecture_spec.py`) and the constants in `pinn/constants.py` (`D_CHARACTERISTIC_LENGTH`, `EPS_SOFT`, `T_CHARACTERISTIC_TIME`, `SIREN_FIRST_OMEGA_0`, `SIREN_HIDDEN_OMEGA_0`, `HUBER_DELTA_*`) are **separate frozen dataclasses/module-level constants entirely outside `TrainingConfig`**. The sha256 identity digest cannot be computed from `TrainingConfig` fields alone.

**When to use:** Building the `config_identity` digest (CTX-53) and the resume config-diff (CTX-57).

**Example:**
```python
# Source: verified against pinn/architecture_spec.py and pinn/constants.py
# (direct file reads this session).
import hashlib
import json

from pinn.architecture_spec import ArchitectureSpec
import pinn.constants as constants


def build_identity_payload(config, arch_spec: ArchitectureSpec) -> dict:
    """Everything CTX-57 classifies as 'identity' — spans config.py AND the
    science-layer modules that are NOT part of TrainingConfig."""
    return {
        # From TrainingConfig (config.py) — identity subset only.
        "seed": config.run.seed,
        "precision": config.run.precision,   # NEW field this phase adds
        "device": config.run.device,         # NEW field this phase adds
        "max_epochs": config.stage.max_epochs,
        "guard_thresholds": config.run.guards,  # NEW section this phase adds
        # From the science layer — fixed today, but the digest must still
        # incorporate them so a future spec-driven change is caught.
        "architecture": {
            "hidden_depth": arch_spec.hidden_depth,
            "hidden_width": arch_spec.hidden_width,
            "first_omega_0": arch_spec.first_omega_0,
            "hidden_omega_0": arch_spec.hidden_omega_0,
            "skip_cadence": arch_spec.skip_cadence,
        },
        "physics_constants": {
            "D": constants.D_CHARACTERISTIC_LENGTH,
            "eps_soft": constants.EPS_SOFT,
            "T": constants.T_CHARACTERISTIC_TIME,
        },
    }


def identity_digest(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

### Pattern 3: `curriculum.jsonl` idempotent append (small-file re-scan, not an index)

**What:** Given the ledger only grows by a handful of rows across the Stage-0 slice (at most 7 stage boundaries + any RECOVER/HALT events), the simplest correct idempotency check is: read all existing lines, parse the `(from_stage, to_stage, disposition, step)` tuple from each, and skip the append if that exact tuple is already present. No index file needed.

**When to use:** CTRL-04's idempotent, ordered promotion recording.

**Example:**
```python
# Source: pattern derived from the existing curriculum.jsonl append-semantics
# requirement (CTX-56) + the existing pinn/data/stage_scan.py atomic-write idiom
# (verified this session via direct file read of stage_scan.py:463-478).
import json
from pathlib import Path


def append_curriculum_record(path: Path, record: dict) -> bool:
    """Append one JSON line; return False (no-op) if the (from_stage,
    to_stage, disposition, step) key already exists (idempotent replay)."""
    key = (record["from_stage"], record["to_stage"], record["disposition"], record["step"])
    if path.is_file():
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                existing = json.loads(line)
                if (
                    existing["from_stage"], existing["to_stage"],
                    existing["disposition"], existing["step"],
                ) == key:
                    return False  # already recorded — idempotent no-op
    line = json.dumps(record, sort_keys=True)
    # A single write() of one complete line, flushed+fsynced, is the safe
    # append primitive: POSIX guarantees a single write() under PIPE_BUF is
    # atomic w.r.t. other writers, and a crash between write() and fsync()
    # leaves prior lines intact (append-only files never get rewritten).
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
        fh.flush()
        import os
        os.fsync(fh.fileno())
    return True
```

### Pattern 4: The missing per-step checkpoint/guard hook (the central Phase-41 architecture gap)

**What:** `RunController.run_stage(k)` (in `pinn/training/controllers.py`, read in full this session) is a single call that runs `_run_adam_phase` then (usually) `_run_lbfgs_phase` to completion, with no external per-step hook. `RunController.state_dict()` returns only `{"model", "scheduled_weights", "clipper"}` — the live `torch.optim.Adam` instance is a **local variable inside `run_stage`**, never stored on `self`, and `RunController._rng` (the `numpy.random.Generator` that drives every `build_stage_batch` call — the actual per-step randomness) is **not exposed anywhere**. No global (cross-stage) step counter exists; `state["epoch_count"]` resets to 0 at the top of every `run_stage` call.

**Why this matters:** CTRL-02 (checkpoint every N steps or wall-clock ceiling, whichever first) and CTRL-08 ("resuming from a checkpoint reproduces the exact next-step RNG draws") both require checkpointing **mid-stage**, which requires (a) a call site inside the Adam/L-BFGS loop bodies, (b) the live optimizer's `state_dict()`, and (c) `self._rng.bit_generator.state`. None of these exist in Phase 40's code today.

**When to use:** This is not optional — it is the prerequisite architecture change for CTRL-02/03/06/08 to be testable at all. Plan this as its own task, distinct from the new `checkpoint.py`/`config.py` files.

**Example (the shape of the required RunController extension):**
```python
# Source: derived directly from pinn/training/controllers.py RunController
# (read in full this session) — self._optimizer and self._rng below are NEW
# attributes; run_stage's existing body is unchanged except for storing the
# optimizer and calling the new hook once per epoch/iteration.
class RunController:
    def state_dict(self) -> dict:
        return {
            "model": self._model.state_dict(),
            "scheduled_weights": self._scheduled_weights.state_dict(),
            "clipper": self._grad_clipper.state_dict(),
            "optimizer": self._optimizer.state_dict() if self._optimizer is not None else None,  # NEW
            "rng": self._rng.bit_generator.state,  # NEW — this IS the "numpy" stream in CTX-62's four
        }

    def load_state_dict(self, state: dict) -> None:
        self._model.load_state_dict(state["model"])
        self._scheduled_weights.load_state_dict(state["scheduled_weights"])
        self._grad_clipper.load_state_dict(state["clipper"])
        if state.get("optimizer") is not None and self._optimizer is not None:
            self._optimizer.load_state_dict(state["optimizer"])  # NEW
        self._rng.bit_generator.state = state["rng"]  # NEW

    # Inside _run_adam_phase / _run_lbfgs_phase, after each epoch/iteration:
    #     self._optimizer = optimizer          # NEW — expose the live optimizer
    #     if self._checkpoint_hook is not None:
    #         self._checkpoint_hook(global_step)   # NEW — dual-trigger cadence check lives in the hook
```

### Anti-Patterns to Avoid

- **Reseeding instead of restoring on resume:** Constructing a fresh `np.random.default_rng(config.run.seed)` on resume (same seed, restarting the sequence from index 0) is NOT exact continuation — it is a *statistically-equivalent restart*, which is what CTRL-08 explicitly distinguishes from resume's exact-continuation requirement. Resume MUST restore `self._rng.bit_generator.state` from the checkpoint, not reseed.
- **Conflating `ArchitectureSpec.seed` with `TrainingConfig.run.seed`:** `ArchitectureSpec.seed` drives a one-time local `torch.Generator` for weight initialization (verified: `pinn/network.py` lines 253-254, `generator.manual_seed(int(spec.seed))`); it is a *different* seed value from `run.seed`, which drives `RunController._rng` for per-step data sampling. Decide explicitly (and document) whether the YAML's single `run.seed` value fans out to both, or whether `ArchitectureSpec.seed` stays independently defaulted — this is not resolved by CONTEXT.md and should be surfaced (see Open Questions 2).
- **Treating the resume config-diff as `TrainingConfig`-only:** Per Pattern 2, several CTX-57 identity fields live in `pinn/architecture_spec.py` and `pinn/constants.py`, not in `config.py`. A diff implementation that only compares `TrainingConfig` fields would silently miss an architecture or physics-constant change.
- **Using `numpy.random.get_state()`/`set_state()` (legacy global API) instead of `Generator.bit_generator.state`:** The codebase's caller-owned-RNG discipline (verified in `pinn/network.py`, `pinn/training/collocation_sampler.py`, `pinn/data/batches.py`) uses `numpy.random.Generator` instances exclusively, never the legacy global `numpy.random.seed()`/`get_state()` functions. The "numpy" RNG stream to capture is `RunController._rng.bit_generator.state`, not `numpy.random.get_state()` (which reflects unrelated global state nothing in `pinn/` touches — confirmed via grep this session, no `np.random.seed(` call exists anywhere in `pinn/`).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Atomic file write | A bespoke temp-file/rename scheme | The existing `_atomic_write` idiom (verified present in `pinn/data/stage_scan.py:463`, `pinn/data/splits.py:753`, `pinn/verification/{gradcheck,residual,overfit}_probe.py`) generalized to accept bytes (for `torch.save`) as well as strings | Three independent implementations already exist in this codebase with the exact tmp+fsync+rename+dir-fsync shape CTX-55 specifies; a fourth divergent implementation risks a subtle ordering bug the other three already avoid |
| `weights_only`-safe serialization allowlisting | Custom pickling / a bespoke binary format | `torch.save`/`torch.load(weights_only=True)` with plain dict/list/tuple/tensor/scalar payloads (verified this session: PCG64's big-int state, python `random`'s 625-int tuple, and two RNG tensors all round-trip cleanly with zero `add_safe_globals` calls needed) | PyTorch's weights_only allowlist already covers every payload shape CTX-53 specifies; no custom class ever needs registering if the payload discipline (plain containers only) is followed |
| Deterministic-algorithm forcing | Manually auditing every torch op for determinism | `torch.use_deterministic_algorithms(True)` (raises `RuntimeError` naming the offending non-deterministic op) | This is exactly the API's purpose — cited in PyTorch 2.12 docs (Context7 `/websites/pytorch_2_12`) as the general reproducibility lever, paired with `torch.set_num_threads(1)` for CPU reduction-order determinism |
| Config schema validation | A generic JSON-schema library | The existing `ArchitectureSpec`/`RuntimeSpec`/`TrainingConfig` idiom (`@dataclass(frozen=True)` + fail-closed `__post_init__`) already used across the codebase | CONTEXT.md CTX-50 explicitly locks this pattern; introducing a schema library (jsonschema, pydantic) would be a second, divergent validation mechanism for no added correctness |

**Key insight:** every mechanical piece this phase needs (atomic writes, weights_only-safe serialization, deterministic-algorithm forcing, config validation) already has an established, verified-working idiom either in the standard library, in PyTorch itself, or already implemented three-plus times elsewhere in this exact codebase. The actual engineering work of Phase 41 is *composition* (wiring these idioms together through the RunController extension in Pattern 4) and *governance discipline* (keeping the five owner-carved ⚖ values visibly provisional), not invention of new low-level mechanisms.

## Common Pitfalls

### Pitfall 1: PyYAML round-trips tuples as lists, breaking dataclass equality
**What goes wrong:** `yaml.safe_dump((0.9, 0.999))` serializes fine as a YAML sequence, but `yaml.safe_load` of that same sequence always returns a `list`, never a `tuple`. `OptConfig.adam_betas: tuple[float, float]` validates `isinstance(self.adam_betas, tuple)` at construction — if the YAML mapper passes the raw list through, `OptConfig(adam_betas=[0.9, 0.999])` will actually raise a `ValueError` at `__post_init__` (good, fail-closed) — but if a caller works around that by relaxing the isinstance check instead of coercing, the frozen dataclass equality check in CTRL-01's acceptance test (`(0.9, 0.999) == [0.9, 0.999]` is `False` in Python — **verified empirically this session**) will silently fail the "re-parses equal to what ran" acceptance criterion.
**Why it happens:** YAML has no native tuple type; PyYAML maps both Python tuples and lists to the same YAML sequence node, and always reconstructs sequences as lists on load.
**How to avoid:** The YAML mapper must explicitly `tuple(...)`-coerce every dataclass field typed as a tuple before constructing the dataclass (see Pattern 1's code example).
**Warning signs:** A round-trip test that checks `resolved_config == reloaded_config` failing only on `OptConfig` equality, or a `TypeError`/`ValueError` at `OptConfig.__post_init__` about `adam_betas` not being a tuple.

### Pitfall 2: Two seeds, not one — `ArchitectureSpec.seed` vs `TrainingConfig.run.seed`
**What goes wrong:** `pinn/architecture_spec.py`'s `ArchitectureSpec.seed` (default 0) independently seeds a **local** `torch.Generator` used once at model construction (`pinn/network.py`, verified: `generator.manual_seed(int(spec.seed))`). This is a completely separate seed from `TrainingConfig.run.seed`, which seeds `RunController._rng` (a `numpy.random.Generator`) for per-epoch data sampling. If the config-YAML mapper only threads `run.seed` through to `RunController` and leaves `ArchitectureSpec.seed` at its hardcoded default (0), then two "runs at the same seed" that only vary `run.seed` in the YAML will have **identical initial weights** every time (since `ArchitectureSpec.seed` never changes) — silently defeating part of the intended seed-band variation CTX-62/D6's "2-3 pilot repeats across seeds" is supposed to produce.
**Why it happens:** `ArchitectureSpec` was deliberately built with NO precision/device coupling (CTX-20) and its own `seed` default was fixed for deterministic *default* construction (per its own docstring: "Phase 41 (CTRL-01) may override via YAML-mapped config") — but the YAML mapper's job of actually threading a config value into `ArchitectureSpec.seed` is not yet built.
**How to avoid:** Decide explicitly (flag in Open Questions if unresolved during planning) whether the YAML's single `run.seed` fans out to both `ArchitectureSpec(seed=run.seed)` and `RunController`'s data-sampling RNG, or whether they are independently configurable. Document the choice in the frozen `config.yaml`'s identity payload either way (Pattern 2).
**Warning signs:** A seed-band pilot test (Phase 43, ACC-05) that shows literally identical loss curves across "different seeds" for the first several steps.

### Pitfall 3: Coincident dual-trigger checkpoints writing twice
**What goes wrong:** If the checkpoint cadence check is implemented as two independent `if` branches (`if step % N == 0: save()` and `if elapsed >= ceiling: save()`) without a shared "already saved this step" guard, a step where BOTH conditions are true fires `save()` twice — which is wasteful, and if the second save races with an in-flight fallback-scan read of `latest.pt`, could expose an inconsistent read (though the atomic-rename discipline itself is still safe against readers).
**Why it happens:** Two independent trigger conditions checked separately, rather than a single dual-condition-OR check with a last-written-step guard.
**How to avoid:** CTX-54 already specifies the fix: "coincident triggers on one step → exactly one write (guarded by last-written-step)." Implement as one function: `should_checkpoint(step, elapsed) -> bool` that also updates and checks a `last_written_step` field, called exactly once per step.
**Warning signs:** A rolling-retention test that expects exactly 3 rolling checkpoints after N writes but finds an extra file, or a `curriculum.jsonl`-style duplicate-row bug pattern recurring in the checkpoint index.

### Pitfall 4: Checkpoint fallback scan must distinguish "structurally valid" from "loads without error"
**What goes wrong:** A naive fallback scan that just tries `torch.load(candidate, weights_only=True)` in a loop and returns the first one that doesn't raise could return a checkpoint that loads fine as a *pickle* but is missing required top-level keys (e.g., a stale schema_version=0 payload from an earlier, incompatible schema) — silently resuming from garbage.
**Why it happens:** `torch.load` succeeding is necessary but not sufficient for "this is a valid, current-schema checkpoint."
**How to avoid:** After a successful `torch.load`, validate the payload has all CTX-53-required top-level keys (`model`, `optimizer`, `curriculum`, `rng`, `counters`, `config_identity`, `schema_version`) and that `schema_version` matches the current schema before accepting it as "the newest valid checkpoint." If none of the scanned candidates pass both checks, raise the typed "no valid checkpoint" error (per CTRL-03's acceptance criterion), do not silently fall further back to an even-older file.
**Warning signs:** A resume that "succeeds" but immediately produces NaN losses or a stage index that doesn't match the run's actual progress — a resumed-from-corrupt-checkpoint symptom.

### Pitfall 5: macOS `ru_maxrss` units differ from Linux
**What goes wrong:** `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss` is documented (and behaves, per stdlib docs and this session's direct check) in **bytes on macOS/Darwin** but in **kilobytes on Linux**. A memory-watermark guard hardcoded to assume kilobytes (common in code copy-pasted from Linux examples) will silently under-read Mac memory usage by a factor of 1024, defeating the guard entirely on the M5 Pro target machine.
**Why it happens:** This is a long-standing, well-known POSIX `getrusage` platform inconsistency, not a PyTorch or project-specific issue.
**How to avoid:** Either avoid `ru_maxrss` entirely in favor of `torch.mps.driver_allocated_memory()` (an unambiguous byte count of MPS-side allocation, directly relevant to the actual OOM risk on unified memory) or explicitly branch on `sys.platform == "darwin"` if `ru_maxrss` is used.
**Warning signs:** A memory-watermark guard that never trips even under an intentionally-induced leak in a test, or trips 1024x too early/late.

### Pitfall 6: `torch.load` without `weights_only=True` is a documented RCE vector (canon breadcrumb, see Prohibitions)
**What goes wrong:** Any `torch.load(path)` call that omits `weights_only=True` (or explicitly passes `weights_only=False`) on a checkpoint whose provenance is not fully trusted enables arbitrary code execution via a malicious pickle payload — this is PyTorch's own documented security note (confirmed via Context7 `/websites/pytorch_2_12` `notes/serialization.html`, which frames `weights_only=False` as something to do "only if you got the file from a trusted source").
**Why it happens:** `weights_only=True` is not yet the unconditional default in all torch.load call sites in existing code (the current Phase-40 naive store already passes `weights_only=True` explicitly at both load sites — verified this session — so this is a pattern to preserve, not introduce).
**How to avoid:** Every new `torch.load` call site in the production `CheckpointStore` (main load, fallback scan candidates, `--resume` path) must pass `weights_only=True` explicitly; never add a `weights_only=False` escape hatch. This is the canon-breadcrumb prohibition already flagged in 41-SPEC.md (owned by `/gsd-secure-phase`), not a new prohibition to mint here.
**Warning signs:** Any code review diff introducing a bare `torch.load(path)` call without the keyword argument.

## Code Examples

### Verified atomic checkpoint write + full RNG-stream round-trip (executed this session, `pinn-train` env, torch 2.12.1)

```python
# Source: executed directly in the pinn-train conda environment this session;
# output confirmed round-trip correctness for all four RNG streams plus
# atomicity (tmp -> fsync -> os.replace -> dir fsync).
import torch, numpy as np, random, tempfile, os, pathlib

payload = {
    "rng": {
        "torch": torch.get_rng_state(),                 # torch.uint8 tensor, shape (5056,)
        "torch_mps": torch.mps.get_rng_state(),          # torch.uint8 tensor, shape (44,)
        "numpy": np.random.default_rng(42).bit_generator.state,   # nested dict of plain ints
        "python_random": random.getstate(),              # (version:int, state:tuple[625 ints], gauss_next)
    },
    "counters": {"step": 123, "epoch": 4},
    "schema_version": 1,
}

with tempfile.TemporaryDirectory() as td:
    p = pathlib.Path(td) / "ckpt.pt"
    tmp = p.with_suffix(".pt.tmp")
    torch.save(payload, tmp)
    with open(tmp, "rb") as f:
        os.fsync(f.fileno())
    os.replace(tmp, p)                     # atomic rename, same filesystem
    dirfd = os.open(td, os.O_RDONLY)
    os.fsync(dirfd)                        # directory-entry fsync
    os.close(dirfd)
    loaded = torch.load(p, weights_only=True)   # succeeds — no add_safe_globals needed
```
Verified output this session: `round trip OK`, `numpy state matches: True`, `python random state matches: True`.

### CLI entry-point convention to follow (matches `pinn/data/stage_scan.py`, verified this session)

```python
# Source: pattern transcribed from pinn/data/stage_scan.py:467-608 (read in full
# this session) — pinn.train should mirror this exact shape for consistency.
import argparse
import sys


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m pinn.train")
    parser.add_argument("--config", required=True)
    parser.add_argument("--resume", default=None)
    parser.add_argument("--hold-stage", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    # ... resolve config, resolve_runtime, build_network, wire controllers ...
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
A single-file `pinn/train.py` (not a package) is the natural choice: `python -m pinn.train` resolves `pinn/train.py` directly, exactly as `python -m pinn.data.stage_scan` resolves `pinn/data/stage_scan.py`.

### Strict-CPU determinism switch (CTX-63)

```python
# Source: torch.use_deterministic_algorithms / torch.set_num_threads confirmed
# via Context7 (/websites/pytorch_2_12, notes/randomness.rst + generated docs)
# and confirmed present in the installed torch 2.12.1 this session.
def apply_strict_cpu_determinism(seed: int) -> None:
    """CTX-63 DEBUG switch. Off by default; forces CPU + deterministic algos."""
    import random
    import numpy as np
    import torch

    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    np.random.seed(seed)          # legacy global — acceptable ONLY inside this
                                   # debug path; production code never calls this
    random.seed(seed)
    # device resolution forced to cpu happens at the resolve_runtime() call site
    # in pinn.train's startup, using the existing ("float64", "cpu") profile —
    # resolve_runtime() itself takes no availability-inference shortcuts (CTX-12).
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `torch.load(..., weights_only=False)` as the historical default | `weights_only=True` is the safe, explicitly-recommended path (and per project convention, already used at every existing load site in `pinn/training/checkpoint.py`'s naive store) | PyTorch made `weights_only=True` the *default* starting with a 2.6-era release (project is on 2.12, well past that change) | No code change needed to "opt in" — the project's existing code already passes it explicitly, which is the more defensive/explicit style to keep even though it may now match the default |

**Deprecated/outdated:** None specific to this phase's dependencies — PyYAML's `safe_load`/`safe_dump`, `torch.save`/`load`, and `torch.mps.*` RNG functions are all current, non-deprecated APIs in torch 2.12 / PyYAML 6.0.3 (confirmed via Context7 docs for the exact installed torch version and via direct execution for PyYAML).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The "numpy" entry in CTX-62's four RNG streams refers to `RunController._rng.bit_generator.state` (the actually-consumed per-step Generator), not the legacy global `numpy.random.get_state()` (which nothing in `pinn/` touches) | Architecture Patterns Pattern 4, Anti-Patterns, Common Pitfalls 2 | If the intended reading is instead "capture the legacy global numpy state defensively, in addition to `RunController._rng`," CTRL-08's "exact next-step RNG draws" test would still need `RunController._rng` captured regardless — this assumption affects only whether a *second*, currently-unused global-numpy capture is also required, not whether the load-bearing one is |
| A2 | `ArchitectureSpec.seed` and `TrainingConfig.run.seed` should probably be unified (one YAML `seed` value drives both weight init and data sampling) rather than kept independently configurable, for the "seed-band pilot" (D6) to actually vary initial weights across seeds | Common Pitfalls 2, Open Questions 2 | If the owner/planner instead wants them independently configurable, the YAML schema needs an explicit second seed field rather than a single fan-out — a schema decision, not a code-correctness issue either way |
| A3 | The memory-watermark guard (CTRL-07, R-1 ⚖ placeholder) should use `torch.mps.driver_allocated_memory()` rather than `resource.getrusage().ru_maxrss`, given the macOS units gotcha (Pitfall 5) and psutil's absence from the environment | Standard Stack (Supporting), Common Pitfalls 5, Environment Availability | If a process-level (not just MPS-allocator-level) memory signal is actually wanted (e.g. to catch a host-side Python object leak, not a GPU buffer leak), `ru_maxrss` with an explicit platform branch is still viable — this is a Claude's-discretion implementation choice, not a locked decision, so either is acceptable as long as the threshold stays a visibly-tagged ⚖ placeholder |

**Risk note:** None of these assumptions affect a LOCKED CONTEXT.md decision — all three are implementation-detail fill-ins inside Claude's Discretion (module filenames / internal wiring) or genuinely-unaddressed edges of the locked decisions. None require re-opening a governance gap; A1/A2 are flagged as Open Questions below so the planner can make an explicit, documented choice rather than an implicit one.

## Open Questions

1. **Does the YAML's single `run.seed` value also seed `ArchitectureSpec.seed`, or are they independently configurable?**
   - What we know: `ArchitectureSpec.seed` (default 0) drives model-weight initialization via a local `torch.Generator`; `TrainingConfig.run.seed` drives `RunController._rng` for data sampling. Both exist today as separate fields with no wiring between them.
   - What's unclear: CONTEXT.md's CTX-62 says "full seed/RNG state... recorded" but does not explicitly address whether the config's `run.seed` fans out to `ArchitectureSpec` construction.
   - Recommendation: Fan out `run.seed` to both by default (`ArchitectureSpec(seed=config.run.seed, ...)` at `pinn.train` startup) so a single YAML seed value genuinely varies both weight init and data sampling — this is the simpler, more intuitive contract for the "repeat the pilot at 2-3 seeds" workflow (D6) and matches the CTX-64 honesty framing ("re-run to statistical equivalence from recorded config+seed"). If the planner disagrees, this should become an explicit CONTEXT.md addendum rather than an implicit code choice.

2. **What is the exact memory-watermark guard signal (CTRL-07 Tier-2)?**
   - What we know: `psutil` is not installed; `resource.getrusage().ru_maxrss` has a macOS/Linux unit inconsistency (bytes vs KB) but this project is macOS-only; `torch.mps.driver_allocated_memory()`/`current_allocated_memory()` exist and directly measure the actual GPU-side allocation relevant to unified-memory OOM risk.
   - What's unclear: R-1's guard thresholds are explicitly left as ⚖ placeholders by design (owner-ratified post-pilot), but the *signal itself* (which API to read) is not specified in CONTEXT.md and is Claude's Discretion.
   - Recommendation: Use `torch.mps.driver_allocated_memory()` as the primary signal (directly tied to the actual OOM risk on the single MPS device) with the guard's threshold expressed as a fraction of the M5 Pro's 24 GB unified memory (mirroring the existing DATA-01 `memory_watermark` fractional-knob convention in `pinn/data/adapter.py`), rather than `ru_maxrss`.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| PyTorch | All of CTRL-01..08 | ✓ (verified this session via `conda run -n pinn-train`) | 2.12.1 | — |
| PyYAML | CTRL-01 (config parsing) | ✓ (verified this session) | 6.0.3 | — |
| numpy | CTRL-08 (RNG stream capture) | ✓ (verified this session) | 2.4.6 | — |
| `torch.backends.mps` | Production precision/device path | ✓ (`is_available() == True`, verified this session) | — | fp64-CPU escape hatch already exists (`resolve_runtime`) |
| psutil | Potential memory-watermark guard signal | ✗ (verified NOT installed this session) | — | `torch.mps.driver_allocated_memory()` (stdlib-adjacent, no install needed) or stdlib `resource.getrusage()` with an explicit macOS-bytes branch |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** psutil — use `torch.mps.driver_allocated_memory()` (recommended, see Open Questions 2) or `resource.getrusage()` (platform-branched) instead of adding a new dependency for one guard signal.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | stdlib `unittest` (matches Phase 37-40 pattern; no pytest in use) |
| Config file | none — deferred-import skip-guard idiom (`_require(symbol, module)`) in `tests/phase40/test_prohibitions.py`, to be mirrored into a new `tests/phase41/test_prohibitions.py` or reused directly |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_checkpoint -v` (per-module, mirrors Phase 40 plan-level commands) |
| Full suite command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase41 -p 'test_*.py' -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|---------------------|--------------|
| CTRL-01 | Keyed YAML resolves to `TrainingConfig`; unknown key fails loud; frozen copy re-parses equal | unit | `python -m unittest tests.phase41.test_config_yaml -v` | ❌ Wave 0 |
| CTRL-02 | Dual-trigger cadence fires exactly once on coincidence; retention keeps rolling-3+best+latest+anchors | unit (stub clock+step counter, per SPEC acceptance) | `python -m unittest tests.phase41.test_checkpoint -v` | ❌ Wave 0 |
| CTRL-03 | Atomic write (simulated crash between tmp-write and rename); `weights_only=True` load; fallback scan on corruption | unit + fault-injection (monkeypatch `os.replace` to raise mid-write, or write a truncated file directly) | `python -m unittest tests.phase41.test_checkpoint -v` | ❌ Wave 0 |
| CTRL-04 | Dual anchors survive eviction; replayed promotion is idempotent; skip/regress refused; ledger well-formed | unit (stub curriculum driver) | `python -m unittest tests.phase41.test_checkpoint -v` (or a dedicated `test_curriculum_ledger.py`) | ❌ Wave 0 |
| CTRL-05 | End-to-end resume matches uninterrupted trajectory; `--hold-stage` re-enters; fail-safe refuse on identity/unclassified field change | integration (tiny synthetic Stage-0 loop, per SPEC constraint) | `python -m unittest tests.phase41.test_train_entrypoint -v` | ❌ Wave 0 |
| CTRL-06 | Adam state fully reset at boundary; restored `stage-{k+1}-init.pt` has reset Adam; L-BFGS history empty post-boundary | unit (extends `tests/phase40/test_controllers.py` patterns) | `python -m unittest tests.phase41.test_checkpoint -v` | ❌ Wave 0 |
| CTRL-07 | Each guard trips (NaN/Inf, loss-explosion, disk-floor, memory-watermark); step-0 trip; simultaneous trips → one bundle | unit + fault-injection (inject NaN gradient, monkeypatch `shutil.disk_usage`/`torch.mps.driver_allocated_memory` to report a breach) | `python -m unittest tests.phase41.test_guards -v` | ❌ Wave 0 |
| CTRL-08 | Config + every checkpoint carry all 4 RNG streams; resume reproduces exact next-step draws; two fresh runs at same seed are statistically equivalent (tolerance TBD at Phase 43); strict-CPU switch forces determinism, off by default | unit + integration (RNG-stream round-trip already verified this session; the "statistically equivalent" claim is a Phase-43 pilot-calibrated tolerance, not a Phase-41 hard number) | `python -m unittest tests.phase41.test_determinism -v` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** the single most relevant `tests.phase41.test_*` module + `tests.phase41.test_prohibitions` (mirroring the Phase-40 per-plan convention observed in `40-0N-PLAN.md` files).
- **Per wave merge:** `python -m unittest discover -s tests/phase41 -p 'test_*.py' -v` (full phase41 suite).
- **Phase gate:** full phase41 suite green, plus a regression run of `tests/phase40` (since `controllers.py` is being extended, not just `config.py`/`checkpoint.py` — Pattern 4) before `/gsd-verify-work`.

### Wave 0 Gaps

- [ ] `tests/phase41/__init__.py` — package marker (mirrors `tests/phase40/__init__.py`)
- [ ] `tests/phase41/_fixtures.py` — tiny synthetic Stage-0 loop + stub clock/step-counter fixtures (extend `tests/phase40/_fixtures.py`'s `make_stub_source`/`make_stub_model` rather than duplicating)
- [ ] `tests/phase41/test_prohibitions.py` — the `_require(symbol, module)` deferred-import skip-guard helper, reused verbatim from `tests/phase40/test_prohibitions.py`'s pattern (or imported directly if the helper is promoted to a shared test-utility module)
- [ ] No framework install needed — `unittest` is stdlib and already the established pattern; no new test dependency

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|----------------|---------|-------------------|
| V2 Authentication | no | Single-user local CLI tool, no auth surface |
| V3 Session Management | no | No session concept |
| V4 Access Control | no | Single-user local filesystem, no multi-tenant boundary |
| V5 Input Validation | yes | Fail-closed YAML config validation (CTX-50: unknown/missing keys raise typed errors naming the offending path); typed errors for missing `--resume` paths |
| V6 Cryptography | partial | sha256 identity digest is an integrity/identity check, not a cryptographic secret; no key management involved |
| V12 File and Resources | yes | Atomic checkpoint writes prevent partial-file corruption; disk-floor guard prevents unbounded write growth from exhausting disk |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|----------------------|
| Arbitrary code execution via untrusted pickle in `torch.load` (canon breadcrumb — 41-SPEC.md Prohibitions row 4, owned by `/gsd-secure-phase`) | Tampering / Elevation of Privilege | `torch.load(..., weights_only=True)` at every load site, no `weights_only=False` escape hatch (verified: PyTorch's own docs frame this as "only if you trust the source"; the existing naive `TorchSaveCheckpointStore` already does this correctly at both its load sites) |
| Config injection via a malicious/misconfigured YAML file (e.g. YAML tag abuse) | Tampering | `yaml.safe_load` exclusively — never `yaml.load` (which permits `!!python/object` tag deserialization of arbitrary classes); confirmed this session that PyYAML's `safe_load`/`safe_dump` pair is what CTX-50 already specifies |
| Silent resume across a semantically-changed model (identity-field drift) | Tampering (of trust in reproducibility) | The CTX-57 fail-safe resume config-diff — refuse on ANY identity or unclassified field change, never fail-open (already a SPEC prohibition, tested via negative acceptance) |
| Disk exhaustion from unbounded checkpoint accumulation | Denial of Service (self-inflicted) | Rolling-3 + best + latest + anchor retention (CTRL-02) bounds the checkpoint directory's growth; the disk-floor guard (CTRL-07 Tier 2) halts training before disk fills entirely, and the `failure/` bundle's Tier-A/Tier-B split (CTX-61) is deliberately sized to stay writable even when the disk-floor guard is the one that tripped |

## Sources

### Primary (HIGH confidence — direct execution in the target `pinn-train` conda environment, this session)

- Direct Python execution, `pinn-train` conda env (torch 2.12.1, PyYAML 6.0.3, numpy 2.4.6): verified `torch.mps.is_available()`, `torch.mps.get_rng_state()`/`set_rng_state()`/`manual_seed()` shapes and types, `numpy.random.Generator.bit_generator.state` structure, `random.getstate()` structure, a full atomic-write (`tmp` → `fsync` → `os.replace` → dir `fsync`) round-trip of a nested payload under `torch.load(weights_only=True)`, PyYAML tuple→list round-trip behavior, `shutil.disk_usage`, `resource.getrusage().ru_maxrss` availability, `torch.use_deterministic_algorithms`/`torch.set_num_threads` presence, and `psutil` absence.
- Direct file reads (this session): `pinn/training/config.py`, `pinn/training/checkpoint.py`, `pinn/training/controllers.py`, `pinn/training/stage_exit.py`, `pinn/training/grad_clip.py`, `pinn/training/scheduled_weights.py`, `pinn/runtime.py`, `pinn/architecture_spec.py`, `pinn/constants.py`, `pinn/data/stage_scan.py` (atomic-write idiom + argparse CLI convention), `pinn/data/adapter.py` (memory-watermark fractional-knob convention), `tests/phase40/*` (test patterns, deferred-import skip guards).
- `.planning/phases/41-config-checkpointing-resume-determinism/41-SPEC.md` (locked requirements) and `41-CONTEXT.md` (locked implementation decisions).
- `.planning/REQUIREMENTS.md`, `.planning/STATE.md` (project history/decisions).

### Secondary (MEDIUM confidence — Context7 official docs, cross-checked against the exact installed torch version)

- Context7 `/websites/pytorch_2_12` (matches the installed 2.12.1): `torch.save`/`torch.load` weights_only serialization notes, `torch.serialization.add_safe_globals`/`safe_globals`, `torch.mps.get_rng_state`/`set_rng_state`/`manual_seed`/`seed`, `torch.use_deterministic_algorithms`, `torch.set_num_threads`, `torch.backends.cudnn.deterministic`/`benchmark` (CUDA-specific, informative contrast for why MPS needs the strict-CPU escape hatch).
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` (ratified build-engineering decisions D4/D6/D7/B-5/B-9/B-11/R-1) and `RATIFICATION.md` (owner ratification record, 2026-07-05).
- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` §5.4-5.10, §6.4 (runbook contract, honesty layer, run-folder structure).

### Tertiary (LOW confidence)

- `gsd-tools query package-legitimacy check` verdict for `pyyaml` (`SUS` due to `unknown-downloads` only) — treated as a tool data-gap, not a genuine legitimacy concern, given direct verification of the package's presence and function in the target environment (see Package Legitimacy Audit).

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — every library/API claim was executed directly in the actual target conda environment this session, not inferred from training data or a stale docs snapshot.
- Architecture: HIGH for the mechanical patterns (atomic write, RNG capture, weights_only); MEDIUM for the exact shape of the `RunController` extension (Pattern 4) since the precise hook signature is Claude's Discretion, not a locked CONTEXT.md decision — the *need* for the extension is HIGH confidence (directly read from the existing code), the *exact API surface* is a planning decision.
- Pitfalls: HIGH — every pitfall in this document (tuple/list, two-seed confusion, macOS ru_maxrss units, coincident-trigger double-write, fallback-scan validity, weights_only omission) was either directly reproduced/verified this session or is a documented, well-known platform/library behavior cross-checked against official docs.

**Research date:** 2026-07-18
**Valid until:** 30 days (stable PyTorch/PyYAML APIs on a pinned environment; re-verify if `pinn-train`'s torch/PyYAML versions change, or if Phase 43's pilot recalibrates the ⚖ placeholders referenced here)

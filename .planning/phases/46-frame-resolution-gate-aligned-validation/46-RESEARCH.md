# Phase 46: Frame Resolution & Gate-Aligned Validation - Research

**Researched:** 2026-07-25
**Domain:** Internal ML data-pipeline conformance auditing + training-instrumentation composition (PyTorch, no new external stack)
**Confidence:** HIGH for code-path facts (all claims below are grounded in `file:line` reads of the live worktree); LOW/MEDIUM for anything requiring the actual residual-probe run over the real corpus (that computation is Phase 46's own deliverable, not something this research session was permitted to execute — no training run, no held-out access).

## Summary

Phase 46 has two strands, and code inspection shows the two strands are more entangled than the phase description implies. **Strand A (CONF-01/RG-02)** asks whether the exact positions retained as training targets are raw or `r'=r/D`. Code inspection of the actual resident-tensor construction path shows the answer is almost certainly "raw" — but more importantly, it shows the target surface diverges from the locked contract in **at least three independent ways**, not just scale: the positions/velocities materialized into adapter residency (`pinn/data/adapter.py:923-928,938`) are built from `parsed_brutus.positions`/`velocities` (`adapter.py:863-864`) — the untouched float64 parse — while the masses stored alongside them (`adapter.py:931-933`, sourced from `pre.masses_ordered` at `adapter.py:865`) are the **canonically reordered** masses from `preprocess_trajectory` (`pinn/data/preprocessing.py:171-217`). Since `_canonical_order` (`preprocessing.py:109-120`) sorts bodies by descending mass/velocity/position norm (not file order), the permutation is non-identity for a physically-typical fraction of trajectories — meaning body `i`'s mass may already be paired with body `j`'s raw, un-permuted position in every training/validation sample. Positions are also never COM-recentered, boosted, or rotation-gauged (all of which `preprocess_trajectory` performs at `preprocessing.py:186-205` but whose OUTPUT — `r_gauge`/`v_gauge` — never reaches `_trajectory_tensors`). This is corroborated end-to-end: `pinn/loss_catalog.py::data_huber_loss` (`loss_catalog.py:173-187`) explicitly documents "Inputs are already in the dimensionless system (r')... callers convert raw Brutus positions with `r' = r / D` before calling," and the conformance audit itself lists "Executed target frame (trainex-r2 RG-02)" as its one unresolved item, explicitly deferring to "the train-free residual-on-stored-targets check" (`docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md:239-245`) — i.e., Phase 46 IS that deferred check. None of this is the CONF-01 verdict (per D-06/D-04, code inspection motivates the probe, it is not evidence); it is the precise shape of what the probe must be able to discriminate.

**Strand B (INST-01)** composes the already-verified `pinn.verification.gate_metrics` functions (`gate_metrics.py`, unit-agnostic by construction — it never imports `pinn.constants`, confirmed by its import block) into the existing validation event boundary. That boundary is `RunController._run_validation` (`pinn/training/controllers.py:652-662`), called from both the Adam (`controllers.py:975-981`) and L-BFGS (`controllers.py:1141-1147`) inner loops at `epoch_count % validation_every == 0`, and surfaced to `pinn/train.py`'s `checkpoint_hook` (`train.py:786-819`), which already dedups per `global_step` before appending to `validation.jsonl` via `_append_validation_record` (`train.py:75-103`). The EXISTING validation pass samples a small replay/lookahead-shaped batch (`_stage_batch`, reusing `pinn.data.batches.build_stage_batch`/`select_stage_records`) — it is NOT the "complete current-stage validation pool" D-11 requires; INST-01 must add a SEPARATE deterministic full-pool forward pass hooked at the same `global_step % validation_every == 0` boundary, traversing `validation_source.records_at_or_below(k)` where `validation_source` is a `pinn.data.splits.StageIndex` (`splits.py:254-261`, accepts a plain int) — **not** `AdmittedSetAdapter.records_at_or_below` (`adapter.py:1074-1078`), which has a DIFFERENT contract (requires a `StageLabel` with a `.value` attribute). A significant, code-verified caveat for D-12/D-13: the ONE existing production consumer of `gate_metrics.compute_trajectory_gate_metrics` — `pinn/evaluate.py:405-425` — pairs the model's physics-frame output positions with **raw native times**, not `u=t/T`, when calling `finite_difference_velocity`. Since `gate_metrics` is dimensionless-agnostic by construction, this silently produces a velocity scaled by `1/T` relative to the `dr'/du` pairing D-12 locks. This is flagged as a Candidate Gap below — it must NOT be copied into INST-01, and `pinn/evaluate.py` is out of Phase 46's write scope regardless (hard constraint).

**Primary recommendation:** Build CONF-01 as a NEW probe module (do not point the existing `residual_probe.py` CLI at the corpus — it reads via the separate `pinn.verification.fixture_loader`, not the production `StageIndex`/adapter surface D-01 mandates) that reuses `residual_probe.py`'s dimensionless-residual math/evidence-serialization PATTERN and `preprocess_trajectory` as the positive-control transform, while measuring the actual resident `StageIndex.snapshot_positions`/`snapshot_velocities` surface. Build INST-01 as a full-pool gate-metrics pass hooked into the SAME `checkpoint_hook`/`_append_validation_record` cadence boundary `pinn/train.py` already owns, writing one atomic sidecar (reuse `pinn.training.atomic_io.atomic_write_text`) per validation event plus a compact pointer appended to `validation.jsonl`, and extending `pinn/training/summary.py::_validation_summary` (render-don't-recompute) to project the new fields for EVAL-01 precondition (iii).

## Architectural Responsibility Map

This is not a web application; "tiers" below are this training pipeline's own layering (data ingestion -> preprocessing/physics -> orchestration -> verification/metrics -> persistence). The held-out evaluation tier is explicitly excluded from Phase 46.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| CONF-01 frame probe (residual measurement) | Verification/Metrics (`pinn/verification/`) | Data/Adapter (`pinn/data/`) | The probe reads resident data but its logic is a verification computation, not a data-pipeline responsibility; it must not become a second data-loading path |
| CONF-01 evidence artifact (D-05) | Persistence/Artifact (evidence tree under `.planning/phases/46-.../evidence/`) | Verification/Metrics | Mirrors the `residual_probe.py` evidence-directory pattern (`evidence_root`, atomic write, `raw.json` + `summary.md`) |
| INST-01 gate-metrics composition | Verification/Metrics (`pinn/verification/gate_metrics.py`, reused unmodified) | Training Orchestration (`pinn/training/controllers.py`) | `gate_metrics` owns the math (D-26: verified-clean, not reopened); the orchestration layer owns WHEN/over-WHAT-population it is invoked |
| INST-01 full-validation-pool traversal | Training Orchestration (`RunController`/`checkpoint_hook`) | Data/Adapter (`StageIndex.records_at_or_below`) | Population selection is a data-access concern delegated to the existing `StageIndex` seam; iteration/event-timing is orchestration's job |
| INST-01 sidecar + `validation.jsonl` pointer | Persistence/Artifact (`pinn/train.py`, `pinn.training.atomic_io`) | Training Orchestration | Same tier that already owns `validation.jsonl`/`checkpoint_hook`; no new artifact-owning module needed |
| EVAL-01 precondition (iii) inspectability (D-19) | Persistence/Artifact (`pinn/training/summary.py`) | — | `summary.py` already owns "render, never recompute" projection of `validation.jsonl` into `summary.json`/`summary.md` |
| Held-out evaluation (`pinn/evaluate.py`) | Excluded — out of Phase 46 scope | — | Hard constraint: never invoked, imported, or modified; read-only pattern precedent only |

## Standard Stack

No new external packages are introduced by this phase. It composes pre-existing, already-pinned modules.

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| torch | 2.12.1 [VERIFIED: requirements-lock.txt:19] | Tensor ops, autograd-free finite differences, `torch.no_grad()` forward passes | Already the project's sole ML runtime; every consumed function (`gate_metrics`, `preprocess_trajectory`'s callers, `AdmittedSetAdapter`) is already torch/numpy-based |
| numpy | 2.4.6 [VERIFIED: requirements-lock.txt] | Float64 preprocessing math (`preprocess_trajectory`, invariants) | `pinn/data/preprocessing.py` and the adapter's scan pass are numpy-only until fp32 tensor materialization |

### Supporting
None new. `json`, `pathlib`, `os`, `hashlib` (stdlib) are the only additional imports Phase 46 is expected to need, all already used identically elsewhere (`pinn/training/atomic_io.py`, `pinn/verification/residual_probe.py`, `pinn/evaluate.py`).

### Alternatives Considered
Not applicable — no library choice is being made; this phase is a composition of in-repo modules under a hard "don't reopen verified-clean math" constraint (D-26).

**Installation:** none required.

**Version verification:** `torch==2.12.1` and `numpy==2.4.6` are read directly from the committed `requirements-lock.txt` (repo file, [VERIFIED] by direct read, not a registry query — this is an internal lockfile, not an external package this research needs to vet). This research session's own Python (`/opt/homebrew/bin/python3`, 3.14.6) does **not** have torch or pytest installed (`ModuleNotFoundError: No module named 'torch'`) — see Environment Availability below; this does not affect the validity of the code-path findings, which are static reads, but it means no function in this research was actually executed.

## Package Legitimacy Audit

Not applicable. Phase 46 installs no external packages; it composes existing `pinn.*` modules and stdlib. No `npm view`/`pip index versions`/registry check is required, and no `gsd-tools query package-legitimacy check` call was made because there is nothing new to check.

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram — Strand A (CONF-01 frame probe)

```
                    ┌─────────────────────────────────────────────┐
                    │  Real corpus (simulation_data/Data, RO)      │
                    └───────────────────────┬───────────────────────┘
                                             │
                    ┌────────────────────────▼────────────────────────┐
                    │ AdmittedSetAdapter._scan_and_admit()             │
                    │   parse_brutus_file -> evaluate_admission        │
                    │   -> preprocess_trajectory (pre.r_gauge computed │
                    │      but DISCARDED for residency)                │
                    │   candidates.positions = parsed_brutus.positions │  <- RAW, unpermuted, ungauged
                    │   candidates.masses_ordered = pre.masses_ordered │  <- CANONICAL order
                    └────────────────────────┬────────────────────────┘
                                             │ _materialize()
                    ┌────────────────────────▼────────────────────────┐
                    │ _trajectory_tensors[key] = (times_t, pos_t, vel_t)│  adapter.py:938
                    │  (fp32, RAW positions/velocities, file order)     │
                    └────────────────────────┬────────────────────────┘
                                             │ StageIndex.from_split(adapter, manifest, "train"|"validation")
                    ┌────────────────────────▼────────────────────────┐
                    │ StageIndex.snapshot_positions/velocities(key)     │  splits.py:229-233
                    │  -> delegates to adapter accessor, same raw data  │
                    └────────────────────────┬────────────────────────┘
                                             │ batches.sample_data_points()
                    ┌────────────────────────▼────────────────────────┐
                    │ targets[i] = positions[snapshot_idx].reshape(9)   │  batches.py:265
                    │ masses[i]  = record.masses (CANONICAL order)      │  batches.py:257 <- record.ic13/masses
                    │              record.ic13 (properly canonical/     │     ARE correctly processed (from pre.*)
                    │              gauged/scaled — from pre.r0_gauge)   │
                    └────────────────────────┬────────────────────────┘
                                             │ RunController._data_term()
                    ┌────────────────────────▼────────────────────────┐
                    │ data_huber_loss(pred_pos, true_pos)               │  loss_catalog.py:173
                    │   docstring REQUIRES true_pos already = r'=r/D    │  (contract, not enforced by code)
                    └────────────────────────────────────────────────┘
```

**What CONF-01 must build:** a probe that reads the SAME `StageIndex.snapshot_positions`/`snapshot_times` surface (not `fixture_loader`, not a second parse) for every train+validation identity, evaluates the two symmetric hypotheses (already-`r'`+`u` vs raw-`t`-requiring-conversion) via a dimensionless residual (reusing `residual_probe.py`'s Gate-B pattern: `_u_leaf_acceleration` + `softened_acceleration`), and separately checks the confounds named above (permutation, COM, rotation) so a `D`-only fix is not silently assumed sufficient.

### System Architecture Diagram — Strand B (INST-01 gate-aligned validation)

```
 RunController._run_adam_phase / _run_lbfgs_phase (controllers.py:975-981 / 1141-1147)
   loop: if epoch_count % validation_every == 0:
        val_terms = self._run_validation(k, weights)   <- SAMPLED batch, loss-only (existing)
        self._last_val_total = val_total
        checkpoint_hook(controller, global_step)         <- train.py:786
                │
                ▼
   checkpoint_hook (pinn/train.py:786-819)
        val = controller._last_val_total
        if global_step % validation_every == 0 and not already logged this step:
            _append_validation_record(run_dir/"validation.jsonl", step, final_val_loss, previous)
                │                                          ^^^^ NEW: same "if" branch is the
                │                                               correct hook point for the
                ▼                                               full gate-metrics pass (D-10)
   [NEW] full-validation-pool gate pass, same event boundary:
        for key in sorted(validation_source.records_at_or_below(k)):   <- StageIndex, splits.py:254
            times = validation_source.snapshot_times(key)
            u = times / T_CHARACTERISTIC_TIME                          <- coherent pairing (D-12)
            positions_pred = model.eval()+no_grad forward over u leaf
            velocity = gate_metrics.finite_difference_velocity(positions_pred, u)
            H = gate_metrics.matched_plummer_hamiltonian_series(positions_pred, velocity, record.masses)
            eps_h = gate_metrics.trajectory_eps_h(H)
        aggregate = gate_metrics.aggregate_gate_verdict([eps_h, ...])   <- worst-case max (D-14)
        atomic_write_text(sidecar_path, json.dumps(full per-trajectory evidence))   <- D-17
        _append_validation_record(..., + compact aggregate fields + sidecar pointer)  <- extend schema (D-18)
                │
                ▼
   pinn/training/summary.py::_validation_summary (render, never recompute)  <- extend for D-19
        projects LATEST validation.jsonl record into summary.json/summary.md
```

### Recommended Project Structure

CONTEXT.md explicitly leaves module/file naming to the planner ("Agent's Discretion"). The existing naming convention in `pinn/verification/` (`residual_probe.py`, `gate_metrics.py`, `gradcheck_probe.py`, `overfit_probe.py`) and `pinn/training/` (`atomic_io.py`, `summary.py`, `checkpoint.py`) suggests:

```
pinn/verification/
├── gate_metrics.py         # UNCHANGED — reused, not reopened (D-26)
├── residual_probe.py       # UNCHANGED — pattern source, not directly reused as a CLI
└── <new: frame probe>      # e.g. target_frame_probe.py — reads StageIndex, both hypotheses, evidence
pinn/training/
├── atomic_io.py            # UNCHANGED — atomic_write_text reused directly
├── controllers.py          # EXTENDED — new hook point near _run_validation / checkpoint_hook
├── summary.py              # EXTENDED — _validation_summary projects new sidecar-pointer fields
└── <new: validation gate composition>  # e.g. validation_gate.py — full-pool pass + sidecar writer
pinn/train.py                # EXTENDED — _append_validation_record schema + sidecar wiring
tests/phase46/
├── __init__.py              # _SKIP_PHRASE convention, mirrors tests/phase43/__init__.py
├── _fixtures.py             # extend tests/phase40/_fixtures.py::_StubSource pattern
├── test_frame_probe.py       # D-21
├── test_gate_composition.py  # D-22, extends tests/phase43 fixtures
├── test_isolation.py         # D-23
└── test_artifacts.py         # D-24
```

### Pattern 1: Reusable dimensionless-residual seam (Strand A)

**What:** `residual_probe.py`'s Gate-B computation (`_u_leaf_acceleration` + `softened_acceleration`, comparing finite-difference acceleration on the `u=t/T` leaf against the softened Newtonian force) is the closest existing "is this the right physics frame" computation. It is NOT directly reusable as-is because it loads data via `pinn.verification.fixture_loader.load_trajectory` (a parallel, probe-local reader), not via `StageIndex`/`AdmittedSetAdapter` — and D-01 requires probing the resident `StageIndex` surface specifically.
**When to use:** Extract the residual-computation helpers (`_minimum_pairwise_separation`, `_u_leaf_acceleration`, the qualifying-snapshot mask) as a shared seam; do not duplicate the math.
**Example:**
```python
# Source: pinn/verification/residual_probe.py:139-151 (existing pattern, NOT to be
# invoked as-is — this operates on fixture_loader output, not StageIndex residency)
def _u_leaf_acceleration(velocities_raw, times_raw):
    """Central-difference v'=v_raw*(T/D) on u=t/T, one-sided at endpoints."""
    u = times_raw / T_CHARACTERISTIC_TIME
    velocity_physics = velocities_raw * (T_CHARACTERISTIC_TIME / D_CHARACTERISTIC_LENGTH)
    ...
```

### Pattern 2: Existing validation-event hook boundary (Strand B)

**What:** `checkpoint_hook` in `pinn/train.py` is the single place that already (a) knows `global_step % validation_every == 0`, (b) dedups per-step, (c) appends to `validation.jsonl`. It is the correct, and only correct, place to add the full-pool gate pass without inventing a second cadence (D-10).
**When to use:** Hook the new pass inside the SAME `if` branch as `_append_validation_record`, not inside `RunController._run_validation` (which is the loss-only sampled pass and runs at a per-epoch granularity that the L-BFGS closure may re-enter multiple times per logical step — controllers.py:1152-1158 notes the closure may evaluate multiple times per `optimizer.step(closure)`).
**Example:**
```python
# Source: pinn/train.py:786-819 (existing; the "if" block below is the hook point)
def checkpoint_hook(controller: RunController, global_step: int) -> None:
    ...
    val = getattr(controller, "_last_val_total", None)
    validation_every = int(config.opt.validation_every)
    if (
        val is not None
        and int(global_step) % validation_every == 0
        and validation_state_cell["last_step"] != int(global_step)
    ):
        validation_state_cell["previous"] = _append_validation_record(
            run_dir / "validation.jsonl",
            step=int(global_step),
            final_val_loss=float(val),
            previous_val_loss=validation_state_cell["previous"],
        )
        validation_state_cell["last_step"] = int(global_step)
        # <-- NEW: full-pool gate-metrics pass + sidecar write belongs here,
        #     gated by the SAME condition, before "last_step" is updated again.
```

### Pattern 3: Atomic sidecar + JSON-safe non-finite (D-17/D-18)

**What:** `atomic_write_text` (`pinn/training/atomic_io.py:41-64`) is the verified three-site atomic-write idiom (tmp + fsync + `os.replace` + dir fsync) already shared by `stage_scan.py`/`splits.py`/`gradcheck_probe.py`/`checkpoint.py`/`config_yaml.py`/`guards.py`. `pinn/evaluate.py::_json_safe_float` (`evaluate.py:296-302`) is the precedent for preserving (not nulling) a non-finite metric as a typed JSON string sentinel (`"NaN"`, `"Infinity"`, `"-Infinity"`) — this is the CORRECT precedent for D-18/D-20 ("a genuinely computed non-finite `epsilon_H` is instead retained as numeric evidence with FAIL status"), as opposed to `pinn/training/summary.py::_null_if_nonfinite` (`summary.py:71-81`), which COLLAPSES non-finite to `null` — a DIFFERENT, human-summary-appropriate policy that must NOT be applied to the verdict-bearing sidecar.
**When to use:** sidecar write = `atomic_write_text` + `_json_safe_float`-style encoding; `validation.jsonl` compact record = same non-finite-preserving encoding (it already uses `json.dumps(..., allow_nan=False)` at `train.py:101`, so any non-finite aggregate field must be pre-converted to a string sentinel before that call, exactly as `evaluate.py` does).
**Example:**
```python
# Source: pinn/evaluate.py:296-302
def _json_safe_float(value: float):
    v = float(value)
    if math.isnan(v):
        return "NaN"
    if math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    return v
```

### Anti-Patterns to Avoid
- **Reimplementing finite-difference velocity or the Hamiltonian inside `pinn/training/`:** `gate_metrics.py` already owns this and is verified-clean (D-26); INST-01 must call it, never re-derive it.
- **Passing raw `t` to `gate_metrics.finite_difference_velocity` when positions are in `r'` units:** silently produces a wrongly-scaled velocity (see `pinn/evaluate.py:412-425` for the existing instance of this pattern — flagged as a Candidate Gap below, not something to replicate).
- **Treating `AdmittedSetAdapter.records_at_or_below` and `StageIndex.records_at_or_below` as interchangeable:** they have different argument contracts (`StageLabel` vs plain `int`); production code always goes through `StageIndex` (train.py:355-356).
- **Using `_null_if_nonfinite`'s null-collapsing policy for verdict-bearing sidecar data:** loses the FAIL evidence D-20 requires be retained.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|--------------|-----|
| Finite-difference velocity, matched-Plummer Hamiltonian, worst-case aggregation, SCS, PASS/FAIL boundary | A new metrics module | `pinn.verification.gate_metrics` (all 8 public functions, `gate_metrics.py:1-288`) | Already verified-clean by the conformance audit (D-26); a second implementation risks silent divergence from the audited one |
| Atomic file write (tmp+fsync+replace+dir-fsync) | A new write helper | `pinn.training.atomic_io.atomic_write_text` / `atomic_write_torch` | The "verified three-site idiom," already the sole implementation four other modules import |
| JSON-safe non-finite float encoding | A bespoke encoder | The `_json_safe_float` pattern from `pinn/evaluate.py:296-302` | Established precedent for a verdict-bearing artifact; distinct from and NOT the same as `summary.py`'s null-collapsing policy |
| Split-restricted, leakage-free trajectory traversal | A new corpus query | `StageIndex.records_at_or_below(k)` (`splits.py:254-261`) | The only production seam guaranteed to exclude the test split and respect the frozen manifest |
| Dataset-free duck-typed test source | A new fixture protocol | `tests/phase40/_fixtures.py::_StubSource` (extend), `tests/phase39/_fixtures.py::TinyCorpus` | Already mirrors the exact `StageIndex`/`AdmittedSetAdapter` method surface consumers dereference |
| Dimensionless residual comparison math | A new residual formula | `residual_probe.py`'s Gate-A/Gate-B pattern (`_gate_a_autograd`, `_u_leaf_acceleration`, `_minimum_pairwise_separation`) | Same physics-consistency computation CONF-01 needs, already reviewed once (Phase 38) |

**Key insight:** Every piece of math this phase needs already exists and is independently verified elsewhere in the repo. The entire engineering risk is in the ASSEMBLY/WIRING seam — exactly where the conformance audit found all of C-01..C-08 (`docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md:73-80`) — so the review bar for this phase should be "does the composition pass the right coherent tuple through," not "is the formula right."

## Common Pitfalls

### Pitfall 1: Confusing the two `records_at_or_below` contracts
**What goes wrong:** Calling `AdmittedSetAdapter.records_at_or_below(k)` with a plain `int` raises `AttributeError` (it expects `.value` on its argument, `adapter.py:1074-1078`), while `StageIndex.records_at_or_below(k)` (`splits.py:254-261`) accepts a plain int via `_numeric_stage` (`splits.py:94-101`).
**Why it happens:** Both classes expose the same method NAME with different signatures; `RunController._validation_source` is always a `StageIndex` in production (`train.py:355-356`), so this only bites if a probe or test constructs the raw adapter and calls the method directly.
**How to avoid:** Always operate on the `StageIndex` (`validation_source`), never the raw `AdmittedSetAdapter`, when traversing the validation pool.
**Warning signs:** `AttributeError: 'int' object has no attribute 'value'`.

### Pitfall 2: Silent unit mismatch from raw-`t` finite differencing
**What goes wrong:** `gate_metrics.finite_difference_velocity(positions, times)` is unit-agnostic — it does not know or check what units `times` is in. If `positions` is in physics-frame `r'` but `times` is raw `t` (not `u=t/T`), the returned velocity is `dr'/dt = (1/T)·dr'/du`, silently off by the fixed factor `T=10` (kinetic-energy term off by `T²=100`).
**Why it happens:** The function's docstring says nothing about the required time unit; correctness is entirely a caller-contract issue. `pinn/evaluate.py:412-425` demonstrably passes `times_native` (raw parsed times, per `test_index.snapshot_times`) rather than `u`.
**How to avoid:** INST-01 must construct `u = times / T_CHARACTERISTIC_TIME` explicitly before calling `finite_difference_velocity`, per D-12.
**Warning signs:** `eps_H` values that are suspiciously close to a round power of 10 or 100 off from an expected magnitude.

### Pitfall 3: Reusing the sampled loss-validation batch as the gate population
**What goes wrong:** `RunController._run_validation` (`controllers.py:652-662`) builds its batch via `self._stage_batch(self._validation_source, stage=k, collocation_count=1)`, which internally calls `select_stage_records` — a RANDOM replay/lookahead sample (default up to 240 replay + 16 lookahead, or the config-overridden `replay_count`), not the full population.
**Why it happens:** This pass exists to produce a loss NUMBER for plateau/trend tracking, not a leakage-free population census.
**How to avoid:** D-11 requires an INDEPENDENT deterministic pass over `validation_source.records_at_or_below(k)` in full — never derive the gate population from `_run_validation`'s sampled batch.
**Warning signs:** Gate-metrics per-trajectory counts that vary run-to-run for the same stage/split (they should be deterministic and equal to the full stage-`k`-and-below validation population size).

### Pitfall 4: Losing non-finite evidence to the wrong null policy
**What goes wrong:** `pinn/training/summary.py::_null_if_nonfinite` (`summary.py:71-81`) collapses any non-finite value to JSON `null`. If the sidecar or `validation.jsonl` writer reuses this helper for the gate aggregate, a genuinely computed non-finite `eps_H` (which D-20 says must be RETAINED as evidence with FAIL status) becomes indistinguishable from "never computed."
**Why it happens:** `_null_if_nonfinite` is the ONLY existing non-finite-handling helper in the training-summary layer; it is easy to reach for by proximity.
**How to avoid:** Use the `_json_safe_float`-style string-sentinel encoding (Pattern 3 above) for the sidecar/JSONL gate fields; reserve `_null_if_nonfinite` for the human-summary-only fields it already governs.
**Warning signs:** A `validation.jsonl`/sidecar record with `eps_h: null` where the run log shows a step actually completed the gate computation.

### Pitfall 5: Assuming a `D`-only fix resolves CONF-01's defect branch
**What goes wrong:** Even a correct `r' = r/D` division of the resident positions would NOT make the target surface coherent, because the residency positions are also un-permuted (relative to the canonically-ordered masses stored alongside them) and un-gauged (no COM recenter, no zero-momentum boost, no rotation gauge) — see Summary above.
**Why it happens:** "Divide by D" is the most visible, most discussed part of RG-02's framing (it is literally named after `D`), but code inspection shows the adapter never applies ANY of `preprocess_trajectory`'s five gauge-fixing steps to the residency positions, only to the IC13/mass metadata.
**How to avoid:** If CONF-01 routes to the defect branch (D-09), the recorded finding must name every divergent transform, not just scale, so Phases 47-48's scope-growth (per the ROADMAP branch point) is sized correctly. This is exactly the D-04 confound-distinguishing requirement, not this research's job to resolve.
**Warning signs:** A "fix" that only introduces a `/D` division and re-runs training without re-verifying COM/permutation/rotation coherence.

## Code Examples

### The full public surface of `pinn.verification.gate_metrics` (INST-01 composes these, never reimplements)
```python
# Source: pinn/verification/gate_metrics.py:40-54 (module __all__)
__all__ = [
    "EPS_INV",                              # 1e-10, distinct from training EPS_SOFT=1e-5
    "GATE_EPS_H_REJECT_THRESHOLD",          # 1e-5 — defined here, gate_metrics.py:64
    "GATE_SCS_REJECT_THRESHOLD",            # -5.0 — defined here, gate_metrics.py:65
    "TrajectoryGateMetrics",                # dataclass: hamiltonian_series, eps_h
    "AggregateGateMetrics",                 # dataclass: eps_h, scs, verdict
    "finite_difference_velocity",           # (positions, times) -> (T,3,3) velocity, CPU f64
    "matched_plummer_hamiltonian_series",   # (positions, velocities, masses, eps_inv=1e-10) -> (T,) H
    "trajectory_eps_h",                     # (h_series) -> float; max_t |(H(t)-H(0))/H(0)|
    "compute_trajectory_gate_metrics",      # (positions, times, masses) -> TrajectoryGateMetrics
    "aggregate_test_eps_h",                 # (per-trajectory eps_h list) -> worst-case max
    "scs_from_eps_h",                       # eps_h -> log10(eps_h)
    "gate_verdict",                          # eps_h -> "PASS"/"FAIL", strict > reject, boundary PASSES
    "aggregate_gate_verdict",                # composes the last three into one call
]
```

### The existing (out-of-scope-to-modify) evaluate.py pairing, cited to show the pitfall precisely
```python
# Source: pinn/evaluate.py:405-425 (READ-ONLY reference; never invoke pinn.evaluate in Phase 46)
for key in test_keys:
    record = test_index.get(key)
    times_native = test_index.snapshot_times(key)      # RAW native times, not u=t/T
    ...
    times_t = torch.as_tensor(times_native, ...).reshape(-1)
    ...
    predicted = model(tau_ic13, masses_batch)
    positions = predicted.reshape(-1, 3, 3).detach()    # physics-frame r' (network output)
    trajectory_metrics = gate_metrics.compute_trajectory_gate_metrics(
        positions, times_t.detach(), masses_row.reshape(3).detach(),
    )                                                     # <- r' paired with raw t, not u
```

### Duck-typed dataset-free test source to extend
```python
# Source: tests/phase40/_fixtures.py:37-130 (existing; extend for tests/phase46)
class _StubSource:
    """Duck-typed StageQuery mirroring pinn/data/splits.StageIndex's method surface:
    has_stage, records_at, records_at_or_below, record_keys, get, n_snapshots,
    snapshot_times, snapshot_positions, snapshot_velocities, acceleration_magnitudes,
    stage_label, is_blacklisted, blacklisted_physical_keys, gold_numeric_stage_count.
    """
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `validation.jsonl` carries only `step`/`final_val_loss`/`trend` (`train.py:75-103`) | Adds a schema-versioned atomic sidecar + compact pointer per D-17/18 | This phase (INST-01) | Validation gains a conservation signal for the first time; EVAL-01 precondition (iii) becomes checkable |
| RG-02 (raw-vs-`r'` target frame) unresolved, "requires the corpus payload, which is absent from this worktree" (audit, `...conformance-audit.md:243`) | Resolved via a train-free residual-on-stored-targets check | This phase (CONF-01) | Settles the last open item the conformance audit itself could not close |

**Deprecated/outdated:** none — this phase does not deprecate anything; it fills two gaps the prior audit/pilot left open.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|----------------|
| A1 | The concrete discriminator suggestions in Pitfall 5 / the D-04 confound list (permutation check via `preprocess_trajectory(...).permutation != identity`, COM-offset check via `sum(m_i * target[0,i])`, rotation-gauge check via Jacobi-vector alignment) are MY synthesis of physics reasoning applied to the verified code facts — they are not drawn from any spec or CONTEXT.md text verbatim. | Common Pitfalls / Summary | If the planner adopts these as the literal discriminator design without independently re-deriving them against the locked spec sections (`ctl_instruction.md` §2.2-2.4), a subtly wrong discriminator could produce a false-confident CONF-01 verdict. Low risk if the planner treats them as a starting menu, not a locked design. |
| A2 | The full-validation-pool cost estimate (~226 validation trajectories × ~125 snapshots) is derived by combining today's real-corpus file counts (measured via `find`) with the RETAINED `scan.log` evidence from Phase 39 closeout (2026-07-16) and the `hierarchical/base` footer `dt_out` DEFAULT of 0.08 — not a fresh admission-pass measurement (torch/numpy were unavailable in this research session to actually run the adapter). | Environment Availability / Validation Architecture | If admission counts, the blacklist, or per-trajectory snapshot counts have changed since 2026-07-16, the cost estimate could be off; this does not block planning (any reasonable batching/chunking design tolerates a 2x estimate error) but the planner should not hard-code "226" anywhere load-bearing. |
| A3 | The `AdmittedSetAdapter.records_at_or_below` vs `StageIndex.records_at_or_below` argument-contract mismatch (Pitfall 1) is presented as a real discrepancy found by reading both implementations; I did not find a test that currently exercises the adapter's version with a bare int to confirm the `AttributeError` in practice. | Common Pitfalls | Low risk — even if this specific failure mode is slightly different in practice, the underlying recommendation (always go through `StageIndex`) is correct regardless, since that is what production code already does. |

## Open Questions / Candidate Gaps

Per the governance STOP protocol, these are surfaced for the orchestrator to decide whether they are formal gaps — none are invented answers.

### C1 — `pinn/evaluate.py`'s existing gate-metrics call pairs `r'` with raw `t`, not `u=t/T`

> **ROUTED (2026-07-25, plan revision 1):** formally recorded as **GAP-46-01** in `46-GAPS.md`
> — Status OPEN, owner-routed, dependency-scoped: does NOT block Phase 46; must be resolved
> at Phase 50/51 planning before EVAL-01 is spent.

- **Decision point:** Does the ONE existing production consumer of `gate_metrics.compute_trajectory_gate_metrics` (`pinn/evaluate.py:405-425`, the Phase-43 held-out evaluator) already violate the same position/time coherence requirement CONTEXT.md D-12 locks for INST-01 — i.e., is the milestone's single authorized held-out evaluation (Phase 51, EVAL-01) at risk of computing a wrongly-scaled `eps_H`/`SCS`?
- **Where in artifact:** `pinn/evaluate.py:407` (`times_native = test_index.snapshot_times(key)`, RAW native times) paired with `pinn/evaluate.py:420-424` (`positions = predicted.reshape(-1,3,3)`, the network's physics-frame output, passed to `gate_metrics.compute_trajectory_gate_metrics(positions, times_t.detach(), ...)` at line 423-425).
- **Why each candidate resolution has different downstream consequences:** (a) If this IS a real unit mismatch, Phase 51's held-out evaluation — which can only be spent ONCE (SCOPE-28) — would render a `eps_H`/`SCS` verdict computed from a velocity off by a fixed factor of `T=10` (kinetic term off by `T²=100`), which could flip a genuine PASS to FAIL or vice versa, and this would not be discoverable after the fact without re-deriving by hand. (b) If it is NOT a real mismatch — e.g., if `test_index.snapshot_times` is later found to already return `u` rather than raw `t` for some reason this research missed, or if the intended contract is deliberately "raw t is fine because X" — then no action is needed, but that intent is nowhere documented in `pinn/evaluate.py` or `gate_metrics.py`. This research traced `snapshot_times` through `StageIndex._source_value("snapshot_times", key)` (`splits.py:226-227`) to `AdmittedSetAdapter.snapshot_times` (`adapter.py:1032-1033`) to `self._trajectory_tensors[key][0]`, which is built from `cand.times = parsed_brutus.times` (`adapter.py:923-924`, `863`) — i.e., genuinely raw, unnormalized times, confirming interpretation (a) as the code-verified fact; whether that fact was a deliberate acceptable choice at Phase 43 time is what's unresolved.
- **Source silence:** `pinn/evaluate.py` module docstring (`evaluate.py:1-40`) documents the checkpoint-ownership/single-use/split-selection contract in detail but says nothing about time-leaf units for the gate pass. `gate_metrics.py`'s module docstring (`gate_metrics.py:1-30`) documents the spec citation for the Hamiltonian/thresholds but not a required time-unit contract for its caller. `43-VERIFICATION.md` (canonical_refs, cited as "verified gate-metric and held-out-evaluator behavior to reuse without reopening component math") was NOT re-read line-by-line in this research session (out of the two-strand scope given to this research task) — it may already address this and rule it acceptable; that is unverified here.
- **Mathematical/engineering grounding:** `finite_difference_velocity` computes `(pos[i+1]-pos[i])/(t[i+1]-t[i])` with whatever units `t` carries (`gate_metrics.py:116-121`). If `pos` is `r'` (dimensionless, scaled by `1/D`) and `t` is raw physical time, the returned "velocity" has units `[r']/[t]`, whereas the locked contract's coherent velocity is `d(r')/d(u) = d(r')/d(t/T) = T · d(r')/d(t)`. The kinetic-energy term in `matched_plummer_hamiltonian_series` (`gate_metrics.py:162-163`) is `0.5 * m * v²`, so using the raw-`t` velocity instead of the `u`-leaf velocity scales the kinetic contribution by `1/T² = 1/100` relative to what the locked contract implies, while the potential term (position-only) is unaffected — producing a Hamiltonian series, and hence an `eps_H`, that is neither the "raw" nor the "correctly-scaled" answer, but a THIRD, internally inconsistent quantity.
- **Agent was tempted to:** flag this as something Phase 46 should silently fix "while we're in the area" — explicitly refused per the hard constraint that `pinn/evaluate.py` must never be invoked, imported, or modified in Phase 46, and per D-13 ("surface that conflict as a governed gap rather than silently changing the held-out evaluator").
- **What the user/orchestrator needs to decide:** (A) Accept this as a genuine finding and open a milestone-index gap now (even though Phase 46 cannot act on it), so Phase 51 addresses it before spending EVAL-01's single look; (B) defer investigation until Phase 50/51 planning, on the theory that `pinn/evaluate.py`'s existing behavior was already reviewed and accepted at Phase 43 time (re-check `43-VERIFICATION.md` first); (C) treat it as out of scope for v2.2 entirely (SCOPE-30/re-audit-prohibition boundary) since the audit's verified-clean section already covers `gate_metrics`/`loss_catalog`, and this is arguably a NEW finding about `evaluate.py`'s assembly, not previously audited (confirmed: grep of the conformance audit document found no mention of `evaluate.py`, `finite_difference_velocity`, or time/velocity pairing).
- **Confidence of impact:** HIGH — if the interpretation above is correct, it directly threatens the correctness of the milestone's one unspendable-twice held-out evaluation (EVAL-01/SCOPE-28), the entire point of the v2.2 milestone.

### C2 — Exact prevalence of the body-permutation confound in the real corpus is unmeasured

> **ROUTED (2026-07-25, plan revision 1):** NOT a gap, per `46-GAPS.md` § "Not recorded as
> gaps" — the question is the phase's own D-04 deliverable; folded into the 46-02 discriminator
> design (permutation-identity check first and cheapest).

- **Decision point:** What fraction of admitted Stage-0 trajectories have `preprocess_trajectory(...).permutation != (0, 1, 2)` (i.e., how often is the canonical-order mass array actually misaligned with the raw-order position array in current residency)?
- **Where in artifact:** `pinn/data/preprocessing.py:109-120` (`_canonical_order`, sorts descending mass/velocity/position norm) and `pinn/data/adapter.py:865` (`masses_ordered=pre.masses_ordered` stored) vs `adapter.py:863-864`/`938` (raw, un-permuted positions stored).
- **Why each candidate resolution has different downstream consequences:** If the permutation is identity for effectively all trajectories (e.g., the corpus's raw file ordering happens to already be mass-descending by convention of how ICs were generated), the confound is theoretical, not practical, and the D-scale question dominates. If the permutation is frequently non-identity, the defect is a compound, more severe divergence and the eventual repair (Phases 47-48 growth) is larger.
- **Source silence:** No retained evidence in this repo measures this (the scan.log at `.planning/milestones/v2.0-phases/39-.../scan.log` records admission counts, not permutation statistics).
- **Mathematical/engineering grounding:** `_canonical_order`'s sort key is `(file_order, -vel_norm, -pos_norm, -masses)` with `masses` as the LOWEST-priority tiebreak read via `np.lexsort` (which ranks by the LAST key first) — meaning the actual primary sort key is `-masses` (descending mass) with velocity/position norm as tiebreaks, and file order only as the final tiebreak. Since IC generation (per `simulation_data/Scripts/ic_generation/`) has no documented guarantee that raw file body order is mass-descending, non-identity permutations should be expected for any trajectory where the three masses are not already file-ordered descending.
- **Agent was tempted to:** state this "is definitely a real, frequent problem" as fact — refused; this is inference from the sort-key structure, not a corpus measurement, and CONF-01's own probe (D-01/D-04) is the correct mechanism to measure it.
- **What the user/orchestrator needs to decide:** Nothing yet — this is informational for the planner sizing CONF-01's discriminator set (recommend the permutation-identity check be one of the FIRST, cheapest discriminators computed, since it is a pure boolean per trajectory with no residual-tolerance judgment call).
- **Confidence of impact:** MEDIUM — affects the SIZE of any eventual repair (Phases 47-48), not Phase 46's own deliverable, which only needs to detect and record it.

**If no other gaps exist:** none identified beyond C1/C2 above.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|--------------|-----------|---------|----------|
| torch | Running any `pinn.*` code, including the CONF-01/INST-01 implementation and its tests | ✗ in this research session's system Python (`/opt/homebrew/bin/python3` 3.14.6) | pinned 2.12.1 in `requirements-lock.txt:19`, not installed here | Execution must happen in the project's actual dev environment/venv, not this research sandbox |
| pytest | `pytest tests/` (documented canonical command, `docs/TESTING.md:36`) | ✗ in this research session | not pinned in `requirements-lock.txt` at all (only prod deps listed) | Presumably a separate dev-only dependency in the real environment; the planner should confirm `pytest` is installed where execution happens, or fall back to `python -m unittest discover tests/phase46` |
| Real corpus (`simulation_data/Data/`) | CONF-01's real-corpus evidence run (once, per D-24) | ✓ but only in the MAIN repo checkout (`<home>/Desktop/3_body_problem/simulation_data/Data`), NOT in this `.worktrees/trainex` checkout (0-1 files found there) | 4857/4857/2749/2565 files across the four Brutus folders (measured via `find`, matches retained `scan.log:12-15`) | None needed — `pinn.data.adapter.default_data_root()` already resolves via `git rev-parse --git-common-dir`'s parent, which correctly lands on the main checkout regardless of which worktree is executing (`adapter.py:593-605`) |
| git worktree `milestone/v2.2` branch | Phase execution | Not yet cut — `.worktrees/trainex` is currently on `milestone/v2.1` per `git status --short --branch` at session start | — | Per ROADMAP.md, branch cut happens at first phase execution, not at research time — no action needed now |

**Missing dependencies with no fallback:** none — the two missing runtimes (torch, pytest) are expected to be present wherever Phase 46 is actually executed; this research session's inability to run code is a research-tooling limitation, not a phase blocker.

**Missing dependencies with fallback:** covered above (git-common-dir resolution already handles the worktree/corpus-location gap by design).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib), organized per-phase under `tests/phaseNN/`, run via `pytest` |
| Config file | none found (no `pytest.ini`/`pyproject.toml`/`setup.cfg` at repo root) — implicit discovery, per `docs/TESTING.md:36` ("run with `pytest tests/`") |
| Quick run command | `pytest tests/phase46/ -x` (recommended new dir, mirrors `tests/phase37`-`phase43` convention; not yet created) |
| Full suite command | `pytest tests/` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|---------------------|---------------|
| CONF-01 | Symmetric raw/scaled-hypothesis probe identifies the correct arm on synthetic fixtures; canonical preprocessing is the positive control; stable key ordering; train/validation inclusion, test exclusion; mismatched body-order/metadata controls; ambiguous/non-finite fails closed (D-21) | unit | `pytest tests/phase46/test_frame_probe.py -x` | ❌ Wave 0 |
| CONF-01 | Real-corpus evidence run producing the committed `raw.json`/`summary.md` artifact (D-05) | integration/evidence (one-time, not a standing suite dependency, D-24) | a dedicated CLI/script invocation over the real corpus, NOT part of `pytest tests/` | ❌ Wave 0 |
| INST-01 | Per-trajectory `eps_H`/SCS composition via `gate_metrics`, strict threshold direction, worst-case aggregation, aggregate SCS derivation, sorted identity, coherent `r'`+`u` pair, reuse (not reimplementation) of gate functions (D-22) | unit + small multi-trajectory integration | `pytest tests/phase46/test_gate_composition.py -x` (extends `tests/phase43` fixtures/style) | ❌ Wave 0 |
| INST-01 | Held-out isolation: validation-only construction, never imports/calls `pinn.evaluate`, model-mode restoration even on error, loss/optimizer/scheduler/stage-exit/replay/checkpoint/early-stop untouched (D-23) | unit | `pytest tests/phase46/test_isolation.py -x` | ❌ Wave 0 |
| INST-01 | Atomic sidecar publication, schema validation, JSON-safe non-finite encoding, compact `validation.jsonl` linkage, terminal-summary projection, fail-closed empty/missing/corrupt cases, dataset-free (D-24) | unit | `pytest tests/phase46/test_artifacts.py -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** the relevant new `tests/phase46/test_*.py` module(s), fast (`pytest tests/phase46/ -x`)
- **Per wave merge:** `pytest tests/` (full suite; existing `tests/phase37`-`phase43` suites must stay green — nothing in Phase 46 should touch their owned files per the phase's "compose, don't reopen" mandate)
- **Phase gate:** full suite green before `/gsd-verify-work`; the one real-corpus CONF-01 evidence run is executed once and its artifact committed, not re-run per test invocation (D-24 explicitly: "The real corpus is used once for the committed CONF-01 evidence run, not as a standing test-suite dependency")

### Wave 0 Gaps
- [ ] `tests/phase46/__init__.py` — `_SKIP_PHRASE` convention, mirroring `tests/phase43/__init__.py:26` (`"skipped Phase46 production symbol"`)
- [ ] `tests/phase46/_fixtures.py` — extend `tests/phase40/_fixtures.py::_StubSource` (duck-typed `StageIndex`) for gate-composition/isolation tests; a SEPARATE small synthetic raw-vs-scaled trajectory pair fixture for the frame-probe tests (D-21's "synthetic trajectories encoded once as raw positions and once as locked processed/scaled targets with the same D/T")
- [ ] Framework install: none — `pytest`/`torch` presence must be confirmed in the actual execution environment (see Environment Availability); no install command is prescribed here since this research session could not verify what the real dev environment already has

*(No gaps beyond the new test files/fixtures themselves — the underlying framework (`pytest`+`unittest`) and dataset-free fixture pattern already exist and are directly reusable.)*

## Security Domain

`security_enforcement` is not present in `.planning/config.json` (absent = enabled per protocol default), so this section is included. This phase is an internal, offline, no-network data-pipeline/instrumentation composition over a trusted local read-only corpus — most ASVS web-application categories do not apply; the relevant categories are input validation on persisted artifacts and path containment.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|-----------------|---------|--------------------|
| V2 Authentication | No | No user-facing auth surface; this is a local CLI/library composition |
| V3 Session Management | No | No sessions |
| V4 Access Control | No (domain-specific analog exists) | The held-out-isolation contract (D-16/D-23: never construct/read a test `StageIndex`, never import/call `pinn.evaluate`) is this phase's actual "access control" — enforced structurally in code + tests, not an ASVS auth control |
| V5 Input Validation | Yes | Fail-closed schema validation on any persisted/re-read artifact (sidecar JSON, evidence artifact) — follow the existing precedent of `SplitManifest.from_dict`'s strict validation (`splits.py:436-553`) and `load_blacklist_file`'s exact-schema fail-closed check (`adapter.py:608-640`); never silently coerce or drop a malformed record |
| V6 Cryptography | Minor | `sha256` provenance hashing only (already used identically at `pinn/evaluate.py::_sha256_file`, `pinn/verification/fixture_loader.py::sha256_file`) — no secrets, no encryption, nothing new to design |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|------------------------|
| Path traversal / evidence-root escape when writing the CONF-01 evidence artifact or the INST-01 sidecar | Tampering | Reuse existing containment helpers verbatim: `resolve_within_root` (`adapter.py:172-186`), `_reject_dataset_evidence_root` (`residual_probe.py:43-50`), `_resolve_run_dir`'s forbidden-roots check (`splits.py:739-750`) — do not write a new path-containment check |
| Absolute-path/home-directory leak into a committed evidence artifact | Information Disclosure | Follow `AdmittedSetAdapter.evidence_lines()`'s redaction-with-fail-closed-guard pattern (`adapter.py:986-1020`, raises `EvidenceRedactionError` rather than silently stripping) if the CONF-01 evidence artifact records the resolved corpus root |
| A partially-written sidecar advertised by a `validation.jsonl` pointer before it is durable | Tampering / Denial of Service (of the EVAL-01 precondition check) | `atomic_write_text` the sidecar FIRST, then append the compact pointer record — never the reverse (D-17 explicit requirement) |
| Malformed/corrupt sidecar silently accepted on a later read (e.g., by `summary.py`'s render step) | Tampering | `summary.py`'s existing `_read_json_mapping`/`_read_jsonl_mappings` (`summary.py:155-182`) already fail soft (return `None`/empty on malformed input) for the HUMAN-facing summary render — but D-20 requires the run to be marked INELIGIBLE on schema error for the actual EVAL-01 gate check, a stricter fail-closed behavior that must not be confused with the summary's fail-soft render |

## Sources

### Primary (HIGH confidence — direct file reads this session)
- `pinn/data/adapter.py` (full read) — `AdmittedSetAdapter` residency construction, accessors, evidence redaction
- `pinn/data/preprocessing.py` (full read) — `preprocess_trajectory`, `_canonical_order`, `_rotation_gauge`, invariants, IC13 assembly
- `pinn/data/batches.py` (full read) — `sample_data_points`, `sample_collocation_points`, `select_stage_records`
- `pinn/data/splits.py` (full read) — `StageIndex`, `SplitManifest`, `records_at_or_below`
- `pinn/data/types.py` (full read) — `AdmittedRecord`, `DataFidelityPoints`, `FixedBatch`
- `pinn/verification/gate_metrics.py` (full read) — every public function, thresholds, module docstring
- `pinn/verification/residual_probe.py` (full read) — dimensionless residual pattern, evidence serialization
- `pinn/verification/fixture_loader.py` (full read) — probe-local raw loader, distinct from production adapter
- `pinn/evaluate.py` (full read, READ-ONLY per hard constraint) — held-out evaluator, gate-metrics call site, JSON-safe-float pattern
- `pinn/training/controllers.py` (full read, both halves) — `RunController`, `_run_validation`, `CurriculumController`
- `pinn/train.py` (partial read, targeted sections) — `_append_validation_record`, `checkpoint_hook`, `_build_admitted_sources`, `_build_sources`
- `pinn/training/summary.py` (full read) — render-don't-recompute pattern, `_validation_summary`, `_null_if_nonfinite`
- `pinn/training/atomic_io.py` (full read) — `atomic_write_text`/`atomic_write_torch`
- `pinn/constants.py` (full read) — `D_CHARACTERISTIC_LENGTH ≈ 4.6415888336`, `T_CHARACTERISTIC_TIME = 10.0`, `EPS_SOFT = 1e-5`
- `pinn/loss_catalog.py` (targeted read) — `data_huber_loss` docstring/contract
- `pinn/physics_residual.py` (signatures only) — `softened_acceleration`, `componentwise_du`
- `tests/phase43/test_gate_boundary.py`, `tests/phase43/__init__.py` (full/partial read) — test style, `_SKIP_PHRASE` convention
- `tests/phase40/_fixtures.py` (partial read) — `_StubSource` duck-typed fixture
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-CONTEXT.md` (full read) — 26 locked decisions
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/config.json` (full/targeted reads)
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md` (targeted sections) — C-01..C-08 inventory, "Carried unresolved" RG-02 citation
- `.planning/milestones/v2.0-phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/scan.log` (full read) — retained real-corpus admission counts
- Real corpus file counts measured via `find` against the main repo checkout (matches the retained `scan.log`)
- `requirements-lock.txt` — pinned `torch==2.12.1`, `numpy==2.4.6`

### Secondary (MEDIUM confidence)
- `docs/TESTING.md` (partial read) — canonical `pytest tests/` command, v2.0 test-surface history

### Tertiary (LOW confidence — inference, not direct measurement)
- Body-permutation confound prevalence estimate (Candidate Gap C2) — reasoned from `_canonical_order`'s sort-key structure, not measured against the real corpus
- Full-validation-pool cost estimate (~226 trajectories × ~125 snapshots) — combines a 2026-07-16 retained log with today's file-count cross-check, not a fresh measurement

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies, everything verified by direct file read of the committed lockfile
- Architecture: HIGH — every claimed call chain (adapter -> StageIndex -> batches -> loss; controller -> checkpoint_hook -> validation.jsonl -> summary.py) was traced by direct file read with line citations
- Pitfalls: HIGH for the code-verifiable ones (records_at_or_below contract mismatch, evaluate.py time-unit pairing, null-vs-string-sentinel policy divergence); MEDIUM for the physics-reasoning-derived ones (permutation confound prevalence) — flagged as such in the Assumptions Log

**Research date:** 2026-07-25
**Valid until:** until the CONF-01 probe actually runs (this research's Strand-A conclusions are code-inspection-only and are explicitly NOT the RG-02 verdict — see Summary and D-04/D-06); treat as stable for planning purposes for the life of Phase 46 (no expectation of the underlying code changing before Phase 46 executes, since v2.2 is conformance-only and Phase 46 is the first v2.2 phase)

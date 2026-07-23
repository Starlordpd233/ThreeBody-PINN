# Phase 43: Verification, Stage-0 Pilot & Acceptance - Research

**Researched:** 2026-07-20
**Domain:** Assembly of existing verification/training modules into an operator-facing gate + pilot + verdict surface (no new science, no new libraries)
**Confidence:** HIGH

## Summary

Phase 43 is pure assembly: every building block (four verification probes, `RunController.s_per_step`,
`summary.py`, the `runs/<name>/` contract, `AdmittedSetAdapter`) already exists in `pinn/`. The
research task was to pin exact function signatures, exact formulas, and exact file locations so the
planner does not re-derive or re-invent anything. Three load-bearing findings came out of direct
source reading rather than prose paraphrase:

1. **The ε_H/SCS gate formula is unambiguous and already implemented as data** (not yet as model-eval
   code): `ε_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(ε_H)`, monotonically tied together — REJECT
   iff `ε_H > 1e-5` (equivalently `SCS > -5`), boundary inclusive-PASS at exactly `1e-5`/`-5`
   ("Marginal: admitted"). SPEC.md's own literal wording in a few spots ("PASS if SCS > -5", "SCS
   (required: > -5)", boundary "SCS==-5 -> FAIL") is **internally inconsistent** with its own cited
   authority (`ctl_instruction.md`) and with the trainex-r1a ratified finding B-8. This is flagged as
   an Open Question below — it is a genuine drafting defect, not a source-silent gap, and the planner
   must resolve it before writing the Prohibition #1 gate-direction unit test.
2. **`RunController.s_per_step` is a private, uncheckpointed EMA** (`self._s_per_step_ema`), not a
   public property as CTX-73's phrasing implies. It is only externally visible via the `s_per_step`
   field emitted into the structured step-log JSONL. The planner needs either a one-line public
   accessor or a "read the last JSONL record" render step — both are in-scope minimal assembly.
3. **`pinn.train`'s current composition root wires NO real data** (`_HAS_DATASET = False`, defaults to
   a synthetic `_StubSource`). `AdmittedSetAdapter` (Phase 39) already implements the exact same
   `StageQuery`-shaped interface the stub implements, so wiring real Stage-0 data for the smoke test
   and pilot is a drop-in `_SOURCE_FACTORY` swap — but it is a **new, real task Phase 43 must add**,
   not something already wired by Phases 41/42. Separately, `default_data_root()` resolves via `git
   rev-parse --git-common-dir`'s **parent**, which — verified empirically in this session — already
   points at the **master-root** `simulation_data/Data` (6.3 GB, all four README Brutus folders
   present) even when the process runs from the `.worktrees/trainex` checkout. **No copying into the
   worktree is required** for the pilot; CTX-79's "copy or run from master-root" question is resolved
   in favor of "neither — the default resolver already reaches master-root's real corpus."

**Primary recommendation:** Build `pinn.verify`, `pinn.evaluate`, and the `summary.py` enrichment as
thin orchestration/render layers over the exact functions cited below; wire `AdmittedSetAdapter` into
`pinn.train._SOURCE_FACTORY` for the smoke/pilot invocations; do not touch `simulation_data/Data`
(the default resolver already finds it); and get explicit confirmation on the SCS-direction wording
defect before finalizing the gate-direction test.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| `verify` ladder orchestration | CLI / composition root (`pinn/verify.py`, new) | Verification probes (`pinn/verification/*`) | New module calls existing probes as library functions; no new science |
| Device sanity + AD/gradcheck/residual/overfit rungs | Verification probes (existing) | — | Already-built Phase 37/38 modules; `verify` only aggregates |
| >30-min duration gate | Training composition root (`pinn/train.py`) | `verify` marker file (new, on disk) | The gate must block a run BEFORE any run-dir/checkpoint state is created — belongs in `train.py`'s existing "fail-closed CLI validation BEFORE construction" block |
| Smoke test | Training composition root (`pinn/train.py`, config-driven) | `RunController` (existing s/step EMA) | CTX-72 locks this as a config preset of the real train path, not a bespoke harness |
| `evaluate` gate script | New CLI (`pinn/evaluate.py`) | `pinn/data-handling/processing/invariants.py`-adjacent physics kernel, `pinn/physics_residual.py` | Test-set-only, single no-grad forward pass; reuses existing physics kernels for ε_H/SCS |
| `summary.md` enrichment | `pinn/training/summary.py` (existing, extend in place) | `evaluate` output (read-only), prior run's `summary.json` (read-only) | Render-don't-recompute; must-NOT #1 preserved |
| Stage-0 pilot data source | `pinn/data/adapter.py::AdmittedSetAdapter` (existing) | `pinn/data/splits.py`, `pinn/data/batches.py` | Real corpus resolved automatically via git-common-dir default; no new data code, only wiring |
| Threshold calibration + verdict | Markdown artifacts in phase dir (new) | — | Owner-ratified, not autonomously decided; artifact-only, no code |

## Standard Stack

Phase 43 introduces **no new external packages**. Everything is internal `pinn/` code plus the
already-installed `pinn-train` conda environment (PyTorch 2.12 + MPS, TensorBoard, PyYAML, NumPy,
h5py — installed Phase 37/41). `matplotlib` remains **optional** (Phase 42 no-matplotlib rule, CTX-77):
plot generation in `evaluate`'s `plots/` output must be guarded and skip cleanly when absent.

### Core (existing, reused as-is)
| Module | Purpose | Why reused, not rebuilt |
|--------|---------|--------------------------|
| `pinn/verification/componentwise_ad.py` | §10.3 AD probe (rung 2) | `run_probe_arm()` already implements both AD patterns + timing protocol |
| `pinn/verification/gradcheck_probe.py` | fp64-CPU gradcheck (rung 3) | `run_gradcheck()` already implements the certified fp64-CPU-only arm |
| `pinn/verification/residual_probe.py` | dual-gate residual-on-ground-truth (rung 4) | `run_residual_on_ground_truth()` already implements Gate A + Gate B |
| `pinn/verification/overfit_probe.py` | single-trajectory overfit (rung 5) | `run_overfit()` already implements the data-Huber overfit drive |
| `pinn/verification/fixture_loader.py` | read-only single-trajectory Brutus loader | `load_trajectory()` is the probes' sole data source |
| `pinn/training/controllers.py::RunController` | s/step EMA source | `_s_per_step_ema` already computed at 0.1 alpha |
| `pinn/training/summary.py` | stub-then-finalize honesty writer | `stub_summary()`/`finalize_summary()` already implement must-NOT #1 |
| `pinn/data/adapter.py::AdmittedSetAdapter` | real Stage-0 admitted-set source | Already implements the exact `StageQuery` interface `pinn.train` consumes |
| `pinn/physics_residual.py::softened_acceleration` | Newtonian force kernel | PHYS-02/§3.2-compliant; do not re-derive |

### Supporting (assembly-new, minimal)
| Module | Purpose | When to add |
|--------|---------|-------------|
| `pinn/verify.py` (new) | Orchestrates 5 rungs, writes verdict marker | ACC-01 |
| `pinn/evaluate.py` (new) | Runs test set once, renders gate | ACC-03 |
| A small ε_H/SCS metric function, homed near `pinn/physics_residual.py` or a new `pinn/verification/gate_metrics.py` | Computes trajectory-level ε_H/SCS from **model predictions** (distinct from the data-admission ε_H already implemented for raw Brutus data — see Common Pitfalls #1) | ACC-03 |
| `RunController.s_per_step` public accessor (one property) OR a "read last JSONL `s_per_step` field" helper | Exposes the EMA outside the controller | ACC-02 |
| `pinn.train._SOURCE_FACTORY` wiring for `AdmittedSetAdapter` + train/val split | Supplies real data to the smoke test and pilot | ACC-02, ACC-05 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Reusing `AdmittedSetAdapter` via `_SOURCE_FACTORY` | A bespoke smoke-only data loader | Rejected — CTX-72 explicitly requires the smoke test to exercise the REAL mechanical surface, and a bespoke loader would not prove the real adapter path works |
| A public `s_per_step` property on `RunController` | Reading the JSONL tail from disk in the smoke harness | Both are legitimate; the property is one line and matches the file's existing read-only `@property` pattern (`checkpoint_store`, `model`, `scheduled_weights`); the JSONL-tail approach matches "render, don't recompute" philosophy already used by `summary.py`. Either is acceptable; property is lower-risk (no filesystem race) |
| Computing ε_H/SCS with a fresh implementation | Copy-pasting `compute_basic_invariants` from `pinn/data-handling/processing/invariants.py` | **Rejected** — that module computes IC-level `E` (energy of the *initial condition*), not `ε_H` (drift of `H(t)` across the model's *predicted trajectory*). It is not directly reusable; see Common Pitfalls #1 |

**Installation:** none — no new packages.

**Package Legitimacy Audit:** N/A. Phase 43 installs no external packages; all dependencies were
verified during Phase 37 (PyTorch 2.12 + MPS, TensorBoard, PyYAML, NumPy, h5py, `pinn-train` conda
env). `matplotlib` remains optional and its absence is already handled (Phase 42 convention).

## Architecture Patterns

### System Architecture Diagram

```
                 ┌──────────────────────────────────────────────┐
                 │  Operator: `python -m pinn.verify`            │
                 └───────────────────┬────────────────────────────┘
                                     │
        ┌────────────────────────────┼─────────────────────────────┐
        │  rung 1: device sanity (MPS available + D1-p dtype)        │
        │  rung 2: componentwise_ad.run_probe_arm()  (§10.3 AD)      │
        │  rung 3: gradcheck_probe.run_gradcheck()   (fp64-CPU)      │
        │  rung 4: residual_probe.run_residual_on_ground_truth()     │
        │  rung 5: overfit_probe.run_overfit()                       │
        └────────────────────────────┬─────────────────────────────┘
                                     │ each rung: try/except -> PASS/FAIL
                                     ▼
                     verdict marker (verdict + ts + env fingerprint)
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────────────┐
│  `python -m pinn.train --config <smoke|pilot>.yaml`                    │
│  ── launch preflight: reads verify marker; forecast = s_per_step ×     │
│     stage.max_epochs; refuses if forecast > 30min AND marker not green │
│  ── data: pinn.train._SOURCE_FACTORY -> AdmittedSetAdapter (real data) │
│  ── loop: CurriculumController.run() -> RunController (Adam->L-BFGS)   │
│  ── on every exit path: summary.stub_summary() / finalize_summary()    │
│  ── on SIGTERM/one Ctrl-C: graceful checkpoint; `--resume latest`      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ produces runs/<name>/{checkpoints,summary.*,curriculum.jsonl,...}
                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│  `python -m pinn.evaluate --checkpoint <ckpt> --output <dir>`          │
│  ── single no-grad forward over held-out TEST split (once, ever)       │
│  ── computes ε_H = max_t|(H(t)-H(0))/H(0)|, SCS = log10(ε_H)           │
│  ── writes metrics.json + metrics.md (## Gate Check, plain-English)    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ metrics.json feeds
                                ▼
        summary.md test-set preview + comparison hint (reads prior summary.json)
                                │
                                ▼
        Stage-0 pilot: 2-3 seeded runs -> seed-band spread -> R-1/R-2/D4-a
        calibration note -> owner ratification -> 43-VERDICT.md (go/adjust/rethink)
```

### Recommended Project Structure
```
pinn/
├── verify.py              # NEW — ACC-01 ladder orchestrator + marker writer
├── evaluate.py             # NEW — ACC-03 gate script
├── train.py                 # EXTEND — >30-min gate in preflight; _SOURCE_FACTORY wiring
├── verification/
│   ├── componentwise_ad.py  # REUSE unchanged (run_probe_arm)
│   ├── gradcheck_probe.py   # REUSE unchanged (run_gradcheck)
│   ├── residual_probe.py    # REUSE unchanged (run_residual_on_ground_truth)
│   ├── overfit_probe.py     # REUSE unchanged (run_overfit) — note zeros(13) IC13 placeholder, see Pitfalls #5
│   └── gate_metrics.py      # NEW (or homed in pinn/evaluate.py) — model-prediction ε_H/SCS
├── training/
│   ├── controllers.py       # EXTEND — one-line public s_per_step accessor (optional)
│   └── summary.py           # EXTEND — validation summary, test-set preview, comparison hint, honesty layer
└── data/
    └── adapter.py            # REUSE unchanged (AdmittedSetAdapter) — wire into train.py, do not modify

.planning/phases/43-verification-stage-0-pilot-acceptance/
├── evidence/pilot/           # NEW — per-seed raw observations
├── 43-CALIBRATION.md         # NEW — R-1/R-2/D4-a candidates for owner ratification
└── 43-VERDICT.md             # NEW — go/adjust/rethink + FUT-01/FUT-04 handoff update
```

### Pattern 1: Ladder orchestration via library calls, not subprocess
**What:** `pinn.verify` imports and calls `run_gradcheck`, `run_residual_on_ground_truth`,
`run_overfit`, and `run_probe_arm` directly as Python functions (CTX-70), never shells out to the
probes' own `python -m pinn.verification.<probe>` CLIs.
**When to use:** Always for the `verify` ladder — subprocessing would lose the in-process device
sanity rung's context and complicate the single-marker-write contract.
**Example (exact signatures, verified from source):**
```python
# rung 2 — no top-level "passed"; caller must AND all pattern results.
from pinn.verification.componentwise_ad import run_probe_arm
record = run_probe_arm(precision, device)  # -> {"patterns": {...}, "exception": None|dict, ...}
rung2_passed = (
    record["exception"] is None
    and all(record["patterns"][p]["passed"] for p in record["patterns"])
)

# rung 3 — never raises; always returns a dict with "passed".
from pinn.verification.gradcheck_probe import run_gradcheck
result = run_gradcheck(precision="float64", device="cpu")  # -> {"passed": bool, "reason": str|None, ...}

# rung 4 — CAN raise (IncompleteTrajectoryError, ValueError from load_trajectory);
# caller must wrap in try/except (missing/broken probe = FAIL, never a silent skip).
from pinn.verification.residual_probe import run_residual_on_ground_truth
try:
    raw = run_residual_on_ground_truth(
        precision, device,
        variant="standard_quasi_random_gold_standard", id="0000",  # Phase-38 canonical fixture
    )
    rung4_passed = raw["passed"]  # gate_a["passed"] and gate_b["passed"]
except Exception:
    rung4_passed = False

# rung 5 — run_overfit CAN raise OverfitFail; wrap similarly.
from pinn.verification.overfit_probe import run_overfit, OverfitFail
try:
    raw5 = run_overfit(precision, device, variant="standard_quasi_random_gold_standard", id="0000")
    rung5_passed = raw5["passed"]
except OverfitFail:
    rung5_passed = False
```
Source: `pinn/verification/componentwise_ad.py:302-362`, `gradcheck_probe.py:91-152`,
`residual_probe.py:179-239`, `overfit_probe.py:288-393`.

### Pattern 2: `_SOURCE_FACTORY` injection is the existing real-data seam
**What:** `pinn/train.py` module-level `_SOURCE_FACTORY: Optional[Callable[[TrainingConfig],
tuple[Any, Any]]] = None` (default `None` → falls back to `_synthetic_split_sources()`,
`_HAS_DATASET = False`). `AdmittedSetAdapter` already implements the identical `StageQuery`-shaped
interface the synthetic `_StubSource` implements (`has_stage`, `records_at`, `records_at_or_below`,
`record_keys`, `get`, `n_snapshots`, `snapshot_times`, `snapshot_positions`, `snapshot_velocities`,
`acceleration_magnitudes`, `stage_label`, `is_blacklisted`, `blacklisted_physical_keys`,
`gold_numeric_stage_count`) — verified method-for-method against `pinn/data/adapter.py:1023-1081`.
**When to use:** The smoke test (ACC-02) and the pilot (ACC-05) both need real admitted Stage-0
trajectories, not the synthetic stub. Set `pinn.train._SOURCE_FACTORY` to a small factory that builds
one `AdmittedSetAdapter` and derives train/val sources from it (via `pinn/data/splits.py`).
**Example:**
```python
# pinn/train.py currently (verified):
_SOURCE_FACTORY: Optional[Callable[[TrainingConfig], tuple[Any, Any]]] = None
_HAS_DATASET: bool = False  # v2.0 wires no real data source

def _build_sources(config: TrainingConfig) -> tuple[Any, Any]:
    if _SOURCE_FACTORY is not None:
        return _SOURCE_FACTORY(config)
    return _synthetic_split_sources()
```
Source: `pinn/train.py:67-70,202-205`. This is a genuine gap between Phases 39/41 that Phase 43 must
close — not something already wired.

### Anti-Patterns to Avoid
- **Copying `pinn/data-handling/processing/invariants.py::compute_basic_invariants` for the ACC-03
  gate metric:** that function computes the *initial-condition* Hamiltonian `E` from a single (r, v)
  snapshot pair for data-quality characterization — it does not compute the trajectory-level drift
  `ε_H = max_t |(H(t)-H(0))/H(0)|` across a predicted trajectory. Build a small new function that
  evaluates `H(t)` at every predicted snapshot and takes the max relative drift; reuse
  `softened_acceleration`'s force-kernel math (or the plain `-G m_i m_j/r_ij` potential — see Pitfall #1)
  for the potential-energy term, not the full residual machinery.
- **Treating the design doc's §6.3 SCS row as ground truth:** `docs/work/designs/cross_cutting/
  training-execution/2026-06-10-training-execution-design.md:500-513` inverts BOTH ε_H ("required: >
  1e-5") AND SCS ("Larger is better. > -5 is acceptable") relative to `ctl_instruction.md`. SPEC.md's
  Prohibition #1 already forbids copying the ε_H row; the SCS row carries the identical bug and must
  not be copied either (see Open Questions #1).
- **Shelling out to the probe CLIs from `pinn.verify`:** loses per-rung structured PASS/FAIL detail
  and complicates aggregating one overall verdict + one marker write; CTX-70 mandates library calls.
- **Recomputing curriculum/loss history in `summary.py`'s new sections:** the file's established
  "render, don't recompute" discipline (CTX-78) must extend to the new validation-summary/test-preview/
  comparison-hint sections — read `curriculum.jsonl`, the `evaluate` output, and a named prior run's
  `summary.json`, never re-run training or re-derive losses.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Device sanity check | A new MPS-availability probe | `pinn.runtime.resolve_runtime` (raises on unsupported precision/device pair) — call it as rung 1 | Already the single explicit precision/device seam (CTX-14/ENV-04) |
| AD/gradcheck/residual/overfit correctness checks | New probe logic | The four existing `run_*` functions verbatim | Phases 37/38 already built and evidenced these; re-deriving risks silently diverging from the certified tolerances (`GRADCHECK_EPS=1e-6`, `AGGREGATE_CRITERION=1e-6`, `DEFAULT_RESIDUAL_THRESHOLD=1e-5`, `PASS_RATIO=1e3`) |
| Atomic checkpoint/summary writes | New file-write logic | `pinn.training.atomic_io.atomic_write_text`, `TorchSaveCheckpointStore` | Already handle tmp+fsync+rename, `weights_only`-clean contents, fallback scan |
| Curriculum-progression rendering | Recomputing stage transitions | Parse `curriculum.jsonl` line-by-line (as `summary.py::_render_curriculum` already does) | Render-don't-recompute is the file's core honesty discipline |
| Real Stage-0 data access | A new dataset loader/copier | `pinn.data.adapter.AdmittedSetAdapter` + its default `git-common-dir`-based root resolution | Already implements Step-1A admission, stage classification, and in-memory fp32 residency; no copy needed (verified in this session) |
| Seed/RNG bookkeeping | New RNG-capture code | `pinn.training.determinism.{capture_rng_state, restore_rng_state, record_run_start_rng, apply_strict_cpu_determinism}` | Already implements the D6-ratified full seed/RNG record + strict-CPU debug switch |

**Key insight:** Every "hand-roll" temptation in this phase is really a sign the planner is about to
duplicate Phase 37-42 work. The single genuinely new piece of logic in the whole phase is the
model-prediction ε_H/SCS metric function (ACC-03) — everything else is orchestration, rendering, or
a config/wiring change.

## Common Pitfalls

### Pitfall 1: Confusing the data-admission ε_H (raw Brutus trajectories) with the model-evaluation ε_H (ACC-03)
**What goes wrong:** `ctl_instruction.md` Step 1A condition 5 defines `ε_H`/`SCS` as a **trajectory
admission gate** computed on raw parsed Brutus arrays with Plummer softening `eps=1e-10`, at
DataLoader init — this is a *different, already-implemented-elsewhere* computation from ACC-03's
"evaluate gate," which must compute `ε_H`/`SCS` from the **model's predicted positions/velocities on
the held-out test set**. `ctl_instruction.md` itself calls out a second, distinct glyph collision: the
*training-loss* denominator floor `eps_H = 1e-4*S_H` in `pinn_architecture.md` §3.4 is yet a third,
unrelated quantity using the same symbol.
**Why it happens:** All three quantities are named `eps_H`/`ε_H` and superficially resemble each
other; `invariants.py` (Step-1A's likely computation site) is the obvious-looking reuse target but
computes an IC-level quantity, not a trajectory-drift quantity.
**How to avoid:** Build the ACC-03 metric fresh: evaluate the model at every test-trajectory snapshot
time, compute the Hamiltonian `H(t) = sum_i p_i^2/(2m_i) - sum_{i<j} G m_i m_j/|q_i - q_j|` (raw
masses, `G=1`) at each snapshot from the model's predicted positions/velocities, take
`max_t |(H(t)-H(0))/H(0)|`. Cite `data_quality_assessment.md:116-130` (formulas 2-4) and
`ctl_instruction.md:565-573` (the admission-gate transcription, useful for softening-convention
cross-reference only, NOT reusable code) as the formula source — but do not import Step-1A's admission
code.
**Warning signs:** A metrics.md that renders identical ε_H numbers regardless of which checkpoint is
evaluated (a sign the admission-gate's already-computed per-trajectory data value leaked in instead of
a fresh model-prediction computation).

### Pitfall 2: The SPEC.md SCS-direction wording contradicts its own cited authority
**What goes wrong:** SPEC.md's Constraints section states "REJECT if ε_H > 1e-5 ... **PASS if SCS >
-5**", and its Acceptance Criteria state "SCS (required: > -5)" with boundary "SCS==-5 -> FAIL". Since
`SCS = log10(ε_H)` is a strictly monotonically increasing function of `ε_H` (per `data_quality_
assessment.md` formula 4 and `ctl_instruction.md:567`), `ε_H > 1e-5` and `SCS > -5` are **the same
event** — they cannot have opposite pass/fail outcomes. `ctl_instruction.md:568` and the ratified
trainex-r1a finding B-8 (`trainex-r1a-resolution-doc.md:13`) both establish a SINGLE criterion:
"REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`)... `SCS = -5` exactly is Marginal: admitted." The
design doc's §6.3 example (line 505: "SCS: -3.4 (required: > -5) → PASS") independently confirms the
same backwards convention SPEC.md's SCS wording appears to have inherited — but SPEC.md's Prohibition
#1 only calls out the ε_H half of that same design-doc bug.
**Why it happens:** The design doc's §6.3 table treats ε_H and SCS as two independent-looking rows
with opposite "bigger/smaller is better" framing (it even mislabels SCS as "some chaos signature" —
it is not; it is `log10` of the same energy-drift quantity). A spec drafter fixing the well-flagged
ε_H inversion can miss that SCS needs the identical fix, since the two rows read as unrelated at a
glance.
**How to avoid:** Build the gate from ONE boolean derived from `ε_H`, render `ε_H` and
`SCS = log10(ε_H)` as two DISPLAY rows of the same underlying number (never two independently-evaluated
booleans), with the boundary inclusive-PASS at `ε_H == 1e-5` / `SCS == -5` (matching
`ctl_instruction.md`'s "Marginal: admitted" and SPEC.md's own `ε_H==1e-5 → PASS` bullet).
**Warning signs:** A unit test asserting `ε_H=1e-5 → PASS` and `SCS=-5 → FAIL` in the same test suite —
these are mathematically the same input and cannot have different verdicts; if the planner's Prohibition
#1 test tries to assert both literally, it is asserting a contradiction and must be caught in review.
See Open Questions #1 for the concrete recommendation to carry into planning.

### Pitfall 3: Assuming `RunController.s_per_step` is already a public attribute
**What goes wrong:** CTX-73 says "reuses `RunController.s_per_step` (already an EMA in
`controllers.py`)" as though it is a public read. The actual attribute is `self._s_per_step_ema`
(private, underscore-prefixed), computed inside `_log_step` (`controllers.py:672-681`), and is **not**
included in `state_dict()`/`load_state_dict()` (`controllers.py:362-394`) — it resets to `None` across
a resume. It is only externally observable via the `extra["s_per_step"]` field written to the
step-log JSONL handler.
**Why it happens:** The EMA computation exists and IS exactly what CTX-73 describes; only its
*visibility* (private attribute, not checkpointed, not a property) is understated.
**How to avoid:** Add a one-line `@property def s_per_step(self) -> Optional[float]: return
self._s_per_step_ema` (matches the existing read-only property pattern at `controllers.py:404-416`),
OR have the smoke harness tail-read the last `s_per_step` value from `runs/<name>/logs/
train.log.jsonl` after the run completes (matches "render, don't recompute"). Either is minimal and
in-scope; do not build new timing instrumentation.
**Warning signs:** A smoke-test forecast of `None` or a crash on `AttributeError:
'RunController' object has no attribute 's_per_step'`.

### Pitfall 4: `pinn.train`'s current default path uses zero real data
**What goes wrong:** `python -m pinn.train --config <any>.yaml` today runs entirely on
`_synthetic_split_sources()` — a deterministic, data-free `_StubSource` with fabricated
sinusoid/linear positions (`train.py:130-199`). ACC-02's smoke test and ACC-05's pilot both require
REAL Stage-0 admitted data (CTX-72, CTX-79). Running the smoke test/pilot without wiring
`_SOURCE_FACTORY` would silently validate the mechanical surface against synthetic data and produce a
seed-band calibration and threshold candidates that mean nothing scientifically.
**Why it happens:** `train.py`'s docstring calls this "the v2.0 falsifiability floor" — it was a
deliberate, documented Phase 41 scope decision (real-data wiring deferred), not an oversight, but the
deferral point is exactly Phase 43.
**How to avoid:** Add a `_SOURCE_FACTORY` implementation (or equivalent config-driven real-data path)
that builds one `AdmittedSetAdapter` and Stage-0 train/val split views via `pinn/data/splits.py`
before running any smoke/pilot invocation. Make this its own explicit task in the plan — do not treat
it as covered by "assembly of Phase 41's train.py."
**Warning signs:** A pilot run whose loss curves look suspiciously clean/synthetic, or a checkpoint
whose `curriculum.jsonl` Step-1A admission counts are absent (the real adapter logs admitted/
rejected/quarantined counts at init; the stub does not).

### Pitfall 5: `overfit_probe.py`'s IC13 input is still a hardcoded zeros(13) placeholder
**What goes wrong:** `IC13_PLACEHOLDER_NOTE = "zeros(13) — Phase-38 overfit smoke; physically-
normalized IC13 deferred to Phase 39"` (`overfit_probe.py:56-58`) is still live even after GAP-38-01
was resolved with real trajectory data (`38-GAPS.md`). The rung-5 overfit gate therefore never
exercises the real Phase-39/40/41 IC13 pipeline — only the network + COM projection + data-Huber loss
on a *fixed, physically-meaningless* conditioning vector.
**Why it happens:** GAP-38-01's resolution was scoped to "which trajectory the probe reads" (real vs.
synthetic Brutus data), not "what IC13 vector conditions the network" — a narrower fix than it might
appear.
**How to avoid:** Phase 43 is explicitly assembly-only and MUST NOT change `overfit_probe.py`'s
science (SPEC out-of-scope: "Building new probes... — that was Phases 38-41"). Run the ladder AS-IS,
but cite this placeholder explicitly as an "open seam" in the ACC-06 verdict/handoff evidence (SPEC
acceptance criteria requires citing "open seams").
**Warning signs:** None at runtime — the probe passes cleanly regardless; the risk is silently
treating rung-5 PASS as stronger evidence than it is.

### Pitfall 6: Checkpoint-cadence config default already satisfies the smoke spec — do not override wall-clock ceiling accidentally
**What goes wrong:** `CheckpointCadence.every_n_steps` already defaults to 100
(`_PROVISIONAL_EVERY_N_STEPS = 100`, `config.py:124`), which matches ACC-02's `checkpoint_every=100`
requirement without any config change. But `wall_clock_ceiling_s` defaults to `3600.0` (60 min,
`config.py:120`) — a dual-trigger cadence that would NOT interfere with a ~5-minute smoke run, but
WILL matter once the D4-a ceiling is ratified (owner picks a 15-30 min value post-smoke) and must be
written back into the config used by the pilot and future long runs.
**Why it happens:** Easy to assume `checkpoint_every=100` needs an explicit config override when it
is already the code default.
**How to avoid:** Confirm the smoke config either omits `checkpoint.every_n_steps` (uses the default
100) or explicitly sets it to 100 for self-documentation; after the D4-a owner ratification, update
`wall_clock_ceiling_s` in the pilot/production config (not the code default, unless the owner wants a
new global default).

## Runtime State Inventory

Not applicable — Phase 43 is a greenfield assembly/execution phase (no rename/refactor/migration).

## Code Examples

### ε_H / SCS formula (authoritative, verified from two independent citations)
```
# Source: pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:116-130
H = sum_i [ p_i^2 / (2 m_i) ] - sum_{i<j} [ G m_i m_j / |q_i - q_j| ]      (raw masses, G=1)
eps_H = max_{t in [0,T]} | (H(t) - H(0)) / H(0) |
SCS = log10(eps_H)

# Source: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:565-573 (Step 1A,
# condition 5 — the DATA-ADMISSION instance of this same formula, transcribing the SAME gate; cited
# here for the exact boundary-handling convention, NOT as reusable code):
#   REJECT if SCS > -5 (equivalently eps_H > 1e-5)
#   SCS == -5 exactly -> Marginal: admitted, flagged for review   (i.e. PASS at the boundary)
#   If |H(0)| numerically near zero -> SCS undefined -> QUARANTINE for manual review
#   If eps_H == 0 -> SCS = -inf -> label Excellent

# Source: pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/
# trainex-r1a-resolution-doc.md:13 (ratified B-8, single authoritative direction statement):
#   REJECT if eps_H > 1e-5 (smaller passes); eps_H = 0 -> SCS = -inf -> Excellent.
#   The baseline design doc's SS6.3 example is a display slip, fixed cosmetically with B-7.
```

### Verify ladder rung dispatch (exact library-call pattern)
```python
# Source: pinn/verification/{gradcheck_probe,residual_probe,overfit_probe,componentwise_ad}.py
# See Pattern 1 above for the full four-rung example with exact exception handling per probe.
```

### `_SOURCE_FACTORY` real-data wiring seam
```python
# Source: pinn/train.py:67-70, 202-205 (verified exact current state)
_SOURCE_FACTORY: Optional[Callable[[TrainingConfig], tuple[Any, Any]]] = None
_HAS_DATASET: bool = False  # v2.0 wires no real data source

def _build_sources(config: TrainingConfig) -> tuple[Any, Any]:
    if _SOURCE_FACTORY is not None:
        return _SOURCE_FACTORY(config)
    return _synthetic_split_sources()

# AdmittedSetAdapter already implements the exact same interface _StubSource does:
# has_stage, records_at, records_at_or_below, record_keys, get, n_snapshots,
# snapshot_times, snapshot_positions, snapshot_velocities, acceleration_magnitudes,
# stage_label, is_blacklisted, blacklisted_physical_keys, gold_numeric_stage_count.
# Source: pinn/data/adapter.py:1023-1081 (verified method-for-method).
```

### Default data-root resolution (verified empirically in this session)
```python
# Source: pinn/data/adapter.py:593-605
def default_data_root():
    common = subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], text=True).strip()
    main_repo_root = Path(common).resolve().parent
    return main_repo_root / "simulation_data" / "Data"

# Verified from .worktrees/trainex:
#   git rev-parse --git-common-dir -> <home>/Desktop/3_body_problem/.git
#   -> main_repo_root = <home>/Desktop/3_body_problem
#   -> data_root = <home>/Desktop/3_body_problem/simulation_data/Data  (6.3 GB, all
#      four README Brutus folders present: brutus_hierarchical[_gold_standard],
#      brutus_standard_quasi_random[_gold_standard])
# Conclusion: running the pilot from the trainex worktree, with NO GSD_DATA_ROOT override and
# NO file copy, already resolves to the real master-root corpus.
```

### Precedent for provisioning a single real fixture (already done once, Phase 38 GAP-38-01)
```
# Source: .planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-GAPS.md (GAP-38-01, RESOLVED)
# Copied read-only from master-root into the trainex worktree (gitignored, .gitignore:315-316):
#   simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_0000.txt
#   simulation_data/Data/ic_final/ic_standard_quasi_random/ic_standard_0000.txt
# This precedent is NOT needed again for the pilot (default_data_root already reaches master-root),
# but IS the pattern already used by the residual/overfit probes' single-trajectory fixture default
# (variant="standard_quasi_random_gold_standard", id="0000") — reuse this same fixture identity for
# the `verify` ladder's rungs 4/5 unless the planner has a reason to pick a different one.
```

### `summary.md` 6-item order + honesty layer (non-authoritative baseline, still the best available structural reference)
```
# Source: docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md:469-527
1. Run header — name, start/end time, wall-clock, device.
2. Final losses — data/physics/IC/total, plain-English units.
3. Validation curves summary — e.g. "validation loss decreased steadily; final value 1.2e-4 at step N."
4. Curriculum progression — e.g. "Started at stage 1, advanced to stage 3 at step 40,000..."
5. Test-set preview — small subset of test trajectories with predicted-vs-true (reads `evaluate` output).
6. Comparison hint — "vs. my-previous-run: total loss 3.2x lower, val loss 2.1x lower." (reads a named
   prior run's summary.json; a hint, not statistical analysis — SPEC/design §6.6 explicitly excludes
   cross-run statistics from this phase's scope).

Honesty-layer three statements (verbatim, design doc SS6.4 — required literal text per ACC-04):
> "Healthy validation loss != working model." A model can have low training loss and low validation
  loss and still fail the gate. The test set is the only honest answer.
> "Comparison to previous run != progress." A run that beats the previous run on validation can still
  fail the gate. Comparison is for picking which run to evaluate on test, not for claiming success.
> "A clean loss curve != correct physics." A PINN can fit the data loss to zero and still get the
  physics wrong. The gate is what catches this.
```
NOTE: the actual `runs/<name>/` structure differs from this design doc's §5.7 (which predates Phases
41/42): the real structure is `checkpoints/{step-NNNNNN.pt, latest.pt, best.pt, stage-{k}-init.pt,
stage-{k}-final.pt, failure-stage-{k}-step-{n}.pt}`, plus `logs/{train.log,train.log.jsonl}`, `tb/`,
`summary.{md,json}`, `status.json`, `config.yaml`, `curriculum.jsonl`, `failure/` (verified from
`pinn/training/checkpoint.py`, `pinn/train.py:305-309`). Use the code, not the design doc, for the
folder contract.

### Guard/cadence provisional defaults (R-1/R-2/D4-a) — exact current values and their calibration docstring
```python
# Source: pinn/training/config.py:120-126, 175-202
_PROVISIONAL_WALL_CLOCK_CEILING_S = 3600.0    # D4-a; owner picks 15-30 min post-smoke (r1b range)
_PROVISIONAL_LOSS_EXPLOSION_CEILING = 1.0e6   # R-1; "⚖ PROVISIONAL R-1 guard threshold
_PROVISIONAL_DISK_FLOOR_FRACTION = 0.05       #        (owner-calibrate-at-Phase-43-pilot)"
_PROVISIONAL_MEMORY_WATERMARK_FRACTION = 0.7  #        <- literal docstring language in config.py
_PROVISIONAL_EVERY_N_STEPS = 100              # already matches ACC-02's checkpoint_every=100
_DEFAULT_ROLLING_KEEP = 3
_DEFAULT_FAILURE_KEEP = 10

# Source: pinn/training/controllers.py:1292,1327-1348 (RECOVER seam)
# recover_retries: int = 0   # CTX-41's ratified default; R-2 calibrates the retry budget post-pilot
```
`config.py`'s `GuardConfig` docstring literally names Phase 43 as the calibration point
("owner-calibrate-at-Phase-43-pilot") — direct code confirmation that R-1 calibration belongs here.

### `--resume latest` / SIGTERM≡one-Ctrl-C (B-10) — exact entry points
```python
# Source: pinn/training/resume.py:509-527 — load_resume_target(store, resume_arg) accepts the
# literal string "latest" and resolves via the checkpoint store's fallback-scan-aware latest.pt.
# Source: pinn/training/signals.py + pinn/train.py:342-356 — SignalState/install_signal_handlers
# wire SIGTERM (and SIGINT) to a graceful "interrupted" transition + handler flush before exit;
# scripts/train-unattended.sh (B-10 caffeinate wrapper) propagates the same exit code
# (tests/phase42/test_wrapper_exit.py verifies exit-code parity between direct and wrapped invocation).
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Design doc §5.7 `runs/<name>/` structure (`step-001000.pt` naming, no `tb/`, no `curriculum.jsonl`, no `failure/`) | Code-verified structure: `checkpoints/{step-NNNNNN.pt,latest.pt,best.pt,stage-{k}-{init,final}.pt,failure-stage-{k}-step-{n}.pt}`, `logs/`, `tb/`, `summary.{md,json}`, `status.json`, `config.yaml`, `curriculum.jsonl`, `failure/` | Phases 41-42 (post-dates the 2026-06-10 design doc) | Use `pinn/training/checkpoint.py` and `pinn/train.py` as the folder-contract source of truth, not the design doc |
| Design doc's "no pre-flight ladder / smoke test" (absent from the design doc entirely — grepped, zero hits) | The 5-rung `verify` ladder + rung-6 smoke test is defined in `trainex-r1a-resolution-doc.md` §5 ("Composed first-run recipe") and RATIFICATION.md, NOT the design doc | trainex-r1a ratified 2026-07-05 | REQUIREMENTS.md's `[§5 pre-flight]` / `[§5 rung 6, D-5]` citations refer to the resolution doc's §5, not the design doc's §5 (different document, same section number — easy to conflate) |
| `pinn.train` assumed to already wire real data (implied by CTX-72's "ordinary `pinn.train` path") | `pinn.train` currently defaults to synthetic `_StubSource` data (`_HAS_DATASET=False`); real-data wiring via `_SOURCE_FACTORY` is a genuine Phase 43 addition | Verified from source in this session | See Pitfall 4 |

**Deprecated/outdated:**
- The design doc's §6.3 Gate Check example (both the ε_H row and the SCS row) — superseded by
  `ctl_instruction.md` and the ratified B-8 finding; SPEC.md already prohibits copying the ε_H row,
  and the SCS row carries the identical bug (see Open Questions #1).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The recommended fixed fixture for `verify` ladder rungs 4/5 (`variant="standard_quasi_random_gold_standard", id="0000"`) is the right default, reusing the Phase-38 GAP-38-01 precedent rather than a different/rotating trajectory | Code Examples, Pattern 1 | Low — any single admitted trajectory works structurally; the specific choice only affects which numeric error values appear in the ladder's evidence, not correctness |
| A2 | A one-line public `s_per_step` property on `RunController` is the lower-risk fix versus tailing the JSONL from the smoke harness | Pitfall 3, Don't Hand-Roll | Low — both are minimal; if the planner prefers the JSONL-tail approach for stronger "render don't recompute" discipline, that is equally valid and does not change the phase's contracts |
| A3 | `AdmittedSetAdapter` + `pinn/data/splits.py` machinery is sufficient to build a `_SOURCE_FACTORY` without needing to invent new interface methods (based on verified method-name parity, not a full behavioral trace of `splits.py`) | Pattern 2, Pitfall 4 | Medium — if `splits.py`'s split-group objects do NOT already expose the same `StageQuery` interface as the raw adapter, the planner may need a thin adapter-of-an-adapter; this was not fully traced due to research scope/time, and should be confirmed during planning by reading `pinn/data/splits.py::SplitGroup` directly |

**Highest-risk item:** none of the above rise to "needs owner confirmation" — all are implementation
details the planner can resolve by reading one more file if needed. The one item that DOES need
explicit resolution before finalizing a unit test is documented as Open Question #1, not here, because
it is not a training-knowledge assumption — it is a directly-observed internal contradiction in a
LOCKED spec document.

## Open Questions (RESOLVED)

1. **SCS-direction wording for the Prohibition #1 gate test — RESOLVED.** The authoritative
   inclusive-PASS boundary is now explicit: reject iff `epsilon_H > 1e-5` or, equivalently,
   `SCS > -5`; `SCS == -5` passes. The test implements one consistent gate rather than the
   obsolete inverted design-doc rendering. Resolution: `43-SPEC.md` (ACC-03 / Prohibition #1)
   and `43-CONTEXT.md` CTX-75; implementation is pinned in `43-02-PLAN.md` Task 1.

2. **Real-data wiring scope — RESOLVED.** The durable contract is limited to Plan 43-03's
   validated `data.source` selector with optional explicit `data.root`, plus its fail-closed
   admitted-data preflight. It attempts `default_data_root()` first and, when unavailable,
   directs the operator to the CTX-79-approved corpus location or read-only Stage-0 copy; it
   neither automates a copy nor silently falls back to synthetic data. Resolution:
   `43-03-PLAN.md` Tasks 1 and 3.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `pinn-train` conda env (PyTorch 2.12 + MPS, TensorBoard, PyYAML, NumPy, h5py) | All of Phase 43 | ✓ (confirmed Phase 37) | PyTorch 2.12 | — |
| Apple M5 Pro, 24 GB unified memory | Smoke test + pilot wall-clock/memory assumptions | ✓ (confirmed Phase 37, R-3 CLOSED) | — | — |
| `matplotlib` | `evaluate`'s optional `plots/` output | Optional (Phase 42 convention: guard + skip cleanly) | — | Skip plot generation; `metrics.json`/`metrics.md` never depend on it (CTX-77) |
| `caffeinate` (macOS) | Unattended smoke/pilot runs (`scripts/train-unattended.sh`) | ✓ (macOS system tool) | — | — |
| Master-root `simulation_data/Data` (6.3 GB, all 4 README Brutus folders) | Real-data smoke test + pilot | ✓ (verified present and reachable via default `git-common-dir` resolution from the trainex worktree in this session) | — | `GSD_DATA_ROOT` env override if a different root is ever needed |

No missing dependencies with no fallback. No missing dependencies with fallback beyond the already-
established `matplotlib`-optional convention.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | stdlib `unittest` (project convention — NOT pytest, per CLAUDE.md and CONTEXT.md CTX-83) |
| Config file | none — conda env activation (`pinn-train`) is the only setup step |
| Quick run command | `python -m unittest tests.phase43.test_<module> -v` |
| Full suite command | `python -m unittest discover -s tests/phase43 -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ACC-01 | `verify` ladder: all-PASS exits 0; any rung FAIL (incl. missing/broken probe) exits non-zero naming the first failing rung | unit | `python -m unittest tests.phase43.test_verify_ladder -v` | ❌ Wave 0 |
| ACC-01 | Launch path refuses a >30-min forecast when the ladder is not green (boundary: ==30min allowed) | unit | `python -m unittest tests.phase43.test_verify_gate -v` | ❌ Wave 0 |
| ACC-02 | Smoke test completes ~300 steps, checkpoints at 100/200/300, survives Ctrl-C+resume, emits numeric s_per_step + forecast | integration (real short run, gated by real-data availability) | `python -m unittest tests.phase43.test_smoke -v` | ❌ Wave 0 |
| ACC-02 | Early divergence/NaN → honest failure with partial s/step, never a fabricated forecast | unit | `python -m unittest tests.phase43.test_smoke_honesty -v` | ❌ Wave 0 |
| ACC-03 | `evaluate` writes `metrics.json`+`metrics.md`; `## Gate Check` renders correctly; OVERALL FAIL iff `eps_H>1e-5` OR the equivalent SCS condition (per Open Question #1 resolution) | unit | `python -m unittest tests.phase43.test_evaluate_gate -v` | ❌ Wave 0 |
| ACC-03 | Gate boundary: `eps_H==1e-5` -> PASS; equivalent SCS boundary -> PASS (NOT the SPEC.md literal "FAIL" reading — pending Open Question #1 resolution) | unit | `python -m unittest tests.phase43.test_gate_boundary -v` | ❌ Wave 0 |
| ACC-03 | Empty/absent test set refused (non-zero exit); NaN/Inf metric -> honest FAIL, no crash | unit | `python -m unittest tests.phase43.test_evaluate_edge_cases -v` | ❌ Wave 0 |
| ACC-04 | Completed-run `summary.md` has all 6 sections + 3 honesty statements | unit | `python -m unittest tests.phase43.test_summary_enrichment -v` | ❌ Wave 0 |
| ACC-04 | Failed/interrupted `summary.md` names disposition, metrics null (must-NOT #1) | unit | `python -m unittest tests.phase43.test_summary_honesty -v` | ❌ Wave 0 (extends existing `tests/phase42/test_honesty_layer.py` pattern) |
| ACC-05 | Pilot artifact records >=2 seeded runs + seed-band spread; diverged seed included, not dropped; <2 completed seeds flags low-confidence | unit (on recorded evidence, not a live 3-seed run in CI) | `python -m unittest tests.phase43.test_pilot_calibration -v` | ❌ Wave 0 |
| ACC-06 | Verdict never renders unqualified "go" on a FAILing gate | unit | `python -m unittest tests.phase43.test_verdict_grounding -v` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** targeted `python -m unittest tests.phase43.test_<module> -v` for the module touched
- **Per wave merge:** `python -m unittest discover -s tests/phase43 -v`
- **Phase gate:** full suite green before `/gsd-verify-work`; the real smoke test / pilot runs are
  executed manually (they are minutes-long real training runs, not CI-speed unit tests) with their
  evidence committed under `.planning/phases/43-.../evidence/`

### Wave 0 Gaps
- [ ] `tests/phase43/__init__.py` — shared skip-phrase constant (`_SKIP_PHRASE = "skipped Phase43
      production symbol"`), mirroring `tests/phase42/__init__.py`'s pattern
- [ ] `tests/phase43/_fixtures.py` — small tiny-synthetic fixtures for the gate-boundary and
      honesty-layer unit tests (dataset-free where possible, per CTX-83)
- [ ] Framework install: none — `pinn-train` conda env already has everything needed
- [ ] A literal `TODO(phase-43)` note already exists at `tests/phase42/__init__.py:26-30` for an
      s/step non-degradation smoke assertion (JSONL `residuals_bin_*` field + TB scalar) — fold this
      into the ACC-02 smoke test rather than creating a duplicate task

## Security Domain

Phase 43 has no network surface, no authentication, no user-facing input beyond local CLI flags and
a YAML config file already validated by existing `pinn/training/config_yaml.py` fail-closed loading.
The relevant ASVS categories are minimal.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface (local CLI tool) |
| V3 Session Management | No | N/A |
| V4 Access Control | No | N/A |
| V5 Input Validation | Yes (narrow) | `--checkpoint`/`--output` path arguments to `pinn.evaluate` should reuse the existing path-traversal guard pattern already established in `pinn/train.py::_resolve_run_dir` and the probes' `_reject_dataset_evidence_root` |
| V6 Cryptography | No | No secrets, no crypto in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| `--output <dir>` argument used to write outside the intended tree | Tampering | Reuse the existing `_reject_dataset_evidence_root`/`_resolve_run_dir` path-containment pattern already present in the probes and `train.py` |
| A crafted/corrupted checkpoint file loaded by `evaluate` | Tampering | `TorchSaveCheckpointStore` already uses `weights_only`-clean checkpoint contents (D4-b); `evaluate` should load via the same store, not a raw `torch.load` |
| Fabricated/placeholder metrics silently rendered as a real gate result on a crashed evaluate run | Repudiation / Information Disclosure (false honesty) | Directly addressed by SPEC.md Prohibition #2 — refuse on empty/absent test set, render honest FAIL on NaN/Inf rather than crashing or fabricating |

## Sources

### Primary (HIGH confidence — direct source-code reads in this session)
- `pinn/verification/{componentwise_ad,gradcheck_probe,residual_probe,overfit_probe,fixture_loader}.py` — exact probe signatures, return schemas, exception behavior
- `pinn/physics_residual.py`, `pinn/constants.py` — PHYS-02/§3.2 residual + softening constants
- `pinn/data-handling/processing/invariants.py` — confirmed NOT directly reusable for ACC-03 (Pitfall 1)
- `pinn/training/{summary,controllers,config,config_yaml,checkpoint,resume,determinism,guards}.py` — exact APIs, schemas, provisional defaults, docstrings
- `pinn/train.py` — composition root structure, `_SOURCE_FACTORY`/`_HAS_DATASET` real-data gap, launch-preflight insertion point
- `pinn/data/adapter.py` — `AdmittedSetAdapter` interface parity with `_StubSource`; `default_data_root()` git-common-dir resolution (empirically re-verified in this session from `.worktrees/trainex`)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:520-599` — Step 1A admission gate, exact ε_H/SCS formula + boundary handling
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:110-136` — SCS definition (formulas 2-4), band table, superseded-audit notes
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` (full read) — B-8 ratified gate direction, §5 pre-flight ladder recipe, R-1/R-2/D4-a/D6/B-5 exact status
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — owner ratification record, carve-outs
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-GAPS.md` — GAP-38-01 resolution + real-fixture precedent
- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` §4.4, §5, §6 — non-authoritative baseline structure + the known §6.3 SCS/ε_H inversion bug
- `tests/phase42/{__init__.py,test_wrapper_exit.py}` — test conventions, skip-phrase discipline, live TODO(phase-43) note

### Secondary (MEDIUM confidence)
- `.planning/phases/43-verification-stage-0-pilot-acceptance/43-SPEC.md` and `43-CONTEXT.md` — treated as the locked requirement source, but Open Question #1 identifies an internal wording inconsistency within SPEC.md itself requiring planner/owner confirmation

### Tertiary (LOW confidence)
- None — no WebSearch was needed for this phase; every question was answerable from the repository's own source and spec files (no `brave_search`/`exa_search`/`firecrawl` were configured or required per `.planning/config.json`)

## Metadata

**Confidence breakdown:**
- Standard stack / APIs: HIGH — every signature and return schema was read directly from source, not inferred
- Gate formula: HIGH on the formula itself (two independent authoritative citations agree exactly); the SPEC.md wording defect is a documented finding, not a confidence gap
- Architecture / real-data wiring gap: HIGH — verified by reading `pinn/train.py` and `pinn/data/adapter.py` directly, plus an empirical `git rev-parse --git-common-dir` check from the actual worktree
- Pitfalls: HIGH — each pitfall traces to a specific line range in a specific file

**Research date:** 2026-07-20
**Valid until:** Stable for the life of Phase 43 (all findings are pinned to specific, already-committed source lines that will not drift under normal development; re-verify only if `pinn/train.py`, `pinn/data/adapter.py`, or `pinn/training/controllers.py` are modified by a parallel task before planning completes)

# Phase 55: Architecture Characterization Probe - Research

**Researched:** 2026-09-04
**Domain:** Internal verification tooling — PyTorch autodiff-based architecture characterization, reusing the trainer's own physics-residual/causal-weight implementation. No new external library or framework is introduced; the entire research surface is codebase-native.
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-01: Two-tier regression gate (SC4).** (1) A hard **invariant-bound** assertion
suite that must hold for all six audited cases — `front_idx == 0`, `R̄` median
within its recorded order-of-magnitude band (e.g. `1e9 < R̄ < 1e11` per row,
matching the audit's own "`R̄ ≈ 10¹⁰`" framing and ROADMAP SC2's language),
`‖F_grav‖` O(1) and minimum pairwise separation `≫ eps_soft` (rules out a
near-singular-encounter confound), and `w_2..w_16` pinned at the dtype clamp
floor. This is the primary regression net — robust to legitimate refactors
(dtype/backend/torch-version drift), but still catches a real behavioral
change. (2) A secondary **exact-value fixture**: the full six-row output (all
reported quantities, not just `R̄`) captured as a committed JSON, compared on
re-run with a tight relative tolerance (the computation is fully deterministic
— fixed seed, float64, CPU, no training — so bit-level reproducibility is
expected on the same platform/torch version). A deliberate implementation
change that legitimately shifts values regenerates the fixture explicitly,
mirroring how `pinn/verification/gate_metrics.py`'s tests pin exact
schema/threshold values today. — **Reversibility:** reversible — test-only, no
production code depends on the chosen tolerance.

**D-02: General config-driven sweep, six audited cases as the built-in
default (SC1).** The tool accepts an arbitrary list of `(seed, masses,
IC13-mode)` cases via a Python API and CLI/config surface (matching the
established `pinn/verification/*_probe.py` argparse `main(argv)` convention);
calling it with no arguments reproduces exactly the six audited rows. Grounded
in the ROADMAP's own Phase 55 goal text — "committed, tested tooling that
anyone can re-run against any candidate recipe" — which requires genuine
configurability, not six hard-coded cases. This is also what lets Phase 56
invoke the same tool under the new 4096/16-bin structure without new code. —
**Reversibility:** reversible — an internal API; Phase 56 depends on it
existing, not on its exact call signature.

**D-03: Build the new-structure capability; do not exercise it as a milestone
artifact.** Phase 55's own regression obligation (SC2) is strictly the OLD
16-point baseline reproduction under the pre-amendment recipe. Phase 55 must
make the tool **mechanically capable** of the new 4096-stratified/
256-per-bin/16-bin structure `54-RULING.md` (row B2/D3) describes, and should
unit-test that binning/stratification/bin-mean logic correctness directly
(e.g. against synthetic residual arrays) — but must **not** run the real
six-case sweep under the new configuration and present its output as `R_ref`
or as GATE-04-relevant evidence. `R_ref` and GATE-04 are Phase 56
requirements (traceability table: `INST-04 → Phase 55`, `GATE-04 → Phase
56`); computing a number that looks like `R_ref` inside Phase 55 would create
an untracked, ungoverned precursor to a value `54-RULING.md` requires to be
measured, persisted with full provenance, and re-measured on any structural
change — that governance belongs to Phase 56, not to this one. —
**Reversibility:** one-way if violated — an early, uncommitted `R_ref`-like
number produced outside Phase 56's provenance discipline could get quoted
informally and would need to be explicitly disavowed later; cheap to avoid by
simply not running that configuration for real in this phase.

All three decisions above were made by Claude's engineering judgment per
owner instruction (2026-09-04, opted out of manual selection); none involve a
physics/spec adjudication call.

### Claude's Discretion

- Exact module name/location under `pinn/verification/` (e.g.
  `architecture_characterization_probe.py`), dataclass shape for the returned
  result (following `gate_metrics.py`'s `TrajectoryGateMetrics`-style
  convention), CLI flag names, and the deterministic RNG scheme used for the
  "random tanh IC13" variable-mass case (audit row 6) — document whatever
  fixed seed/method is chosen in the module docstring and provenance output
  so the case is reproducible, per repo convention (`fixture_loader.py`,
  `residual_probe.py` document their own conventions the same way).
- Evidence directory placement under `.planning/phases/55-*/evidence/`
  matching the established convention (e.g. Phase 50's
  `evidence/{calibration,corpus,attempts,...}/` layout).
- Test file location: `tests/phase55/test_architecture_characterization.py`,
  following `tests/phase49/`'s per-phase test directory convention.

This research resolves these discretion points into concrete, named
recommendations (module name, dataclass shapes, CLI surface, RNG scheme) so
the planner can proceed without re-deriving them — but they remain
recommendations the planner/executor may adjust, not locked contracts.

### Deferred Ideas (OUT OF SCOPE)

- **Cleanup of two stale pending todos** (`d-06-static-epsilon-sensitivity-check.md`,
  `trainex-r1-research-handoff.md`) — owner flagged these as candidates for
  disposition/removal if no longer relevant, but explicitly **after** Phase
  55's real work, not now. Revisit at Phase 55 close or milestone close, not
  during Phase 55 execution.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INST-04 | Land the architecture-only characterization as committed, tested verification tooling under `pinn/verification/`. For a given `ArchitectureSpec` at initialization — no data, no optimizer, no training step — it reports `‖r′‖`, `‖v′‖`, `‖a′‖ = ‖d²r′/du²‖`, `‖F_grav‖`, minimum pairwise separation, median `R̄`, the full causal weight vector, and `front_idx`, over a configurable seed/IC sweep. Acceptance: it reproduces the 2026-08-17 audit's six-row table. | `## Architecture Patterns` (measurement pipeline, mirrors `controllers.py:629-676`), `## Code Examples` (the exact six default cases + the aggregation contract), `## Don't Hand-Roll` (which trainer primitives to call, not reimplement), `## Common Pitfalls` (dtype-dependent clamp floor, `physics_residual()` wrapper trap, `--precision`/`--device` required-flag trap), `## Validation Architecture` (two-tier test design mapped to SC1-SC4) |
</phase_requirements>

## Summary

Phase 55 builds one new, self-contained module — recommended
`pinn/verification/architecture_characterization_probe.py` — that evaluates
the already-shipped SQR-SkipResNet-SIREN network at a configurable sweep of
`(seed, masses, IC13)` cases, entirely at initialization (no data, no
optimizer, no training step), and reports exactly the seven quantities SC1
names. Every piece of physics/architecture machinery the probe needs already
exists and is production code the trainer itself calls:
`pinn.architecture_spec.ArchitectureSpec` + `pinn.network.build_network` for
the network, `pinn.physics_residual.componentwise_du` +
`pinn.physics_residual.softened_acceleration` for the AD derivatives and
gravity term, and `pinn.loss_catalog.causal_physics_loss(...,
return_details=True)` for the causal weight vector. The exact composition to
mirror is `pinn/training/controllers.py:629-676`'s `_non_data_terms` method —
the same call sequence, with the data/optimizer/loss-scheduling code removed.
This satisfies SC3 by construction: the probe cannot drift from the trainer's
own math because it calls the trainer's own functions.

The single highest-value finding from this research is the audit document's
own parenthetical note on its six-row table: **"medians over the 16
collocation points"** — every reported column (`‖r′‖`, `‖v′‖`, `‖a′‖`,
`‖F_grav‖`, minimum pairwise separation, `R̄`) is the median, across the
`N_t` collocation points, of that quantity's per-point value. This removes
what would otherwise be a significant design ambiguity. `front_idx` is not
per-point — it is computed once from the full weight vector via the exact
formula already shipped at `controllers.py:692-694`:
`max([n for n, w in enumerate(w_n_list) if w > 0.5], default=-1)`.

The second highest-value finding is a live-verified numeric fact that
directly threatens the two-tier regression test (D-01) if missed: the causal
weight clamp floor is **dtype-dependent** by roughly 220 orders of magnitude
— `exp(log(finfo(float32).tiny)) ≈ 1.18×10⁻³⁸` versus
`exp(log(finfo(float64).tiny)) ≈ 2.23×10⁻³⁰⁸` (both computed live in this
session against the project's installed Torch 2.12.0). The regression
fixture runs on float64/CPU (per D-01's own "fixed seed, float64, CPU"
language), so any test asserting `w_2..w_16` sit "at the floor" must derive
the expected floor from `pinn.loss_catalog.resolve_causal_clip_facts(dtype,
device)`, never from a literal copied out of the audit's narrative about the
float32-MPS training run.

Third, the six default cases are precisely specified by the audit's own
table and are reproduced verbatim in `## Code Examples` below — five cases
share `masses=(1,1,1)` and an all-zero 13-dim IC13, differing only in the
`ArchitectureSpec.seed` used for network initialization (seeds 41, 42, 43, 0,
7); the sixth reuses `seed=41` with `masses=(1, 0.8, 0.6)` and a
"random tanh IC13" whose exact RNG scheme is Claude's/the planner's
discretion (recommendation given below).

**Primary recommendation:** Build one module that (1) exposes a
`run_sweep(cases=DEFAULT_CASES, n_col=16, precision="float64",
device="cpu")` Python function as the real configurability surface, wrapped
by a thin `argparse` CLI whose `--precision`/`--device` flags default (not
require) to `float64`/`cpu` so `python -m
pinn.verification.architecture_characterization_probe` with zero arguments
reproduces the six audited rows; (2) internally mirrors
`controllers.py:576-580` and `:629-676` exactly, never the higher-level
`physics_residual()` convenience wrapper (which silently discards the `v'`
output SC1 requires); and (3) ships a second, independent, unit-tested-only
module of pure functions (`stratified_collocation_times`,
`bin_mean_residuals`) implementing the ratified 16-bin/256-per-bin structure
from `54-RULING.md`, wired to nothing in Phase 55's own default sweep.

## Architectural Responsibility Map

This phase has no browser, frontend-server, or CDN tier — it is a
backend-only, offline scientific-verification CLI tool with no network
service boundary. The table below adapts the standard tiers to this
domain's actual boundaries (computation vs. persistence vs. entrypoint).

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Network construction (`ArchitectureSpec` → `build_network`) | API/Backend (core computation library) | — | Pure Python/PyTorch, no I/O; reuses the exact module the trainer imports |
| AD residual + causal-weight computation | API/Backend | — | Must live in the same tier as `pinn/training/controllers.py` — SC3 requires the probe to derive from, not parallel, the trainer's own implementation |
| CLI / sweep orchestration | API/Backend (script entrypoint) | — | `argparse`-based `main(argv)`, matching every existing `pinn/verification/*_probe.py` entrypoint |
| Evidence persistence (`raw.json` + `summary.md`) | Database/Storage (local git-tracked filesystem) | — | No external DB; `.planning/phases/55-*/evidence/` is the "storage" tier, mirroring Phase 38's probes |
| Regression test suite | API/Backend (test tier) | — | `tests/phase55/`, in-process `pytest` invocation, no client/server boundary |

## Standard Stack

No new external package is introduced by this phase. The "stack" is the
existing, already-verified internal `pinn/` modules the probe composes.

### Core (existing internal modules — reused, not reimplemented)

| Module | Verified at | Purpose | Why Standard |
|--------|-------------|---------|---------------|
| `pinn.architecture_spec.ArchitectureSpec` | `pinn/architecture_spec.py:36-141` | Frozen, fail-closed-validated network topology spec; `seed` field is the per-case RNG knob | Locked topology (`input_dim=14, output_dim=9, hidden_depth=12, hidden_width=256`); construction raises `ValueError` on any deviation — reusing it means the probe cannot silently characterize a non-conformant architecture |
| `pinn.network.build_network` | `pinn/network.py:231-255` | Deterministic model construction from a spec + local seeded `torch.Generator` | Global RNG is never touched; identical `spec+seed` gives bitwise-identical parameters — required for the exact-value fixture (D-01 tier 2) to be reproducible |
| `pinn.physics_residual.componentwise_du` | `pinn/physics_residual.py:102-147` | `dr'/du` and `d²r'/du²` via `torch.func.jacrev` composed with itself, `vmap`-ed over `N_t` | The one sanctioned §5.3.1 AD pattern; already proven in production (`controllers.py:632, 643`) |
| `pinn.physics_residual.softened_acceleration` | `pinn/physics_residual.py:193-231` | `§3.2` softened Newtonian force sum, PHYS-03 squared-norm softening | Exact gravity term the trainer's `f_i(u_n)` residual subtracts |
| `pinn.loss_catalog.causal_physics_loss` | `pinn/loss_catalog.py:283-347` | `§3.2` causal weight vector + physics loss, `return_details=True` exposes `{"w_n", "rbar"}` | The exact `w_1=1, w_n=exp(-eta_c*cumsum_excl(stopgrad(Rbar)))` formula, with the dtype-derived underflow clamp already correct |
| `pinn.runtime.resolve_runtime` | `pinn/runtime.py:65-96` | Resolves `(precision, device)` to `RuntimeSpec(dtype, torch_device)`; only `("float32","mps")` and `("float64","cpu")` are legal pairs | Single seam for dtype/device across the repo (CTX-12..14); the probe's regression fixture uses the `("float64","cpu")` arm |
| `pinn.training.collocation_sampler.CollocationSampler` | `pinn/training/collocation_sampler.py:52-93` | `.uniform(n)` draws `n` i.i.d. times in `[0, T_CHARACTERISTIC_TIME]` from a caller-owned `numpy.random.Generator` | Exact sampling primitive `pinn/train.py:1032-1035` feeds the real trainer's collocation points; reusing it (then `np.argsort`) keeps the probe's *sampling*, not just its *math*, trainer-derived |
| `pinn.verify.git_head` | `pinn/verify.py:361-384` | Bounded, fail-soft `git rev-parse HEAD` -> `(sha, available)` | Existing "tree state" capture primitive for SC2's "command, tree state, full output" re-derivability requirement |
| `pinn.training.atomic_io.atomic_write_text` | `pinn/training/atomic_io.py:41-64` | tmp-write + fsync + `os.replace` + parent-dir fsync | Newer, more durable shared idiom than the older probes' private `_atomic_write` (which omits the directory fsync) |

### Supporting

| Module | Verified at | Purpose | When to Use |
|--------|-------------|---------|-------------|
| `pinn.constants` | `pinn/constants.py` | `EPS_SOFT=1e-5`, `T_CHARACTERISTIC_TIME=10.0`, `SIREN_FIRST_OMEGA_0=30.0`, `CAUSAL_ETA_C=1.0` | Import these names for any literal the probe needs; never hard-code them locally |
| `numpy` (2.2.0 installed; `requirements-lock.txt` pins `2.4.6`) | `.venv/bin/python -c "import numpy"` (verified live) | Seeded RNG draws for collocation sampling and (recommended) the row-6 IC13 draw | `np.random.default_rng(seed)` — never the global `np.random` state |
| `torch` (2.12.0 installed; `requirements-lock.txt` pins `2.12.1`) | `.venv/bin/python -c "import torch"` (verified live) | `torch.func.jacrev`, `torch.func.vmap`, tensor ops | Already the exact version the rest of `pinn/` runs against in this checkout |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `componentwise_du` + `softened_acceleration` called directly (mirroring `controllers.py`) | `pinn.physics_residual.physics_residual()` (the composed convenience wrapper) | **Rejected as the probe's core call** — `physics_residual()` computes `_velocity` internally via `componentwise_du` but discards it, returning only the residual. SC1 requires `‖v′‖` to be reported, so the probe needs the intermediate `first`/velocity output; calling the wrapper would force a second, wasteful AD pass just to recover it. Mirror the low-level composition instead. |
| Required `--precision`/`--device` argparse flags (matching `residual_probe.py`/`gradcheck_probe.py`/`overfit_probe.py`) | Defaulted `--precision`/`--device` flags | **Rejected for this probe specifically** — D-02 requires "calling it with no arguments reproduces exactly the six audited rows." A `required=True` flag (the convention every other Phase-38 probe uses) would make that impossible. Default to `float64`/`cpu`. |
| A bespoke JSON/YAML case-config schema | Reuse `dataclasses.asdict`-style plain dicts for `--cases-config` | Either works; a plain list-of-dicts JSON (`[{"label":..., "seed":..., "masses":[...], "ic13_mode":...}]`) needs no new dependency and matches the existing probes' `json.dumps(..., sort_keys=True, indent=2)` evidence convention. |

**Installation:**

No installation step — `torch` and `numpy` are already installed in the
project's `.venv` (verified live this session: `torch==2.12.0`,
`numpy==2.2.0`, `pytest==9.1.1`). Note `requirements-lock.txt` pins slightly
newer `torch==2.12.1` / `numpy==2.4.6`; this is a pre-existing drift in the
checkout, unrelated to this phase, and not something Phase 55 needs to
resolve.

## Package Legitimacy Audit

**Not applicable — this phase introduces no new external package
dependencies.** Every import the new module needs (`torch`, `numpy`,
`argparse`, `dataclasses`, `json`, `pathlib`, `datetime`, `subprocess`) is
either the Python standard library or an already-installed, long-standing
project dependency exercised throughout `pinn/verification/` today. The
`gsd-tools query package-legitimacy check` / ecosystem-registry-verification
protocol targets *newly recommended* packages (slopsquatting, hallucinated
names); running it against `torch`/`numpy` — already pinned in
`requirements-lock.txt` and imported by dozens of existing, working modules
in this exact checkout — would not produce a meaningful signal.

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

```
CLI: python -m pinn.verification.architecture_characterization_probe
     [--precision float64] [--device cpu] [--cases-config PATH]
     [--n-col 16] [--evidence-root PATH]
        │
        ▼
main(argv) — parse + validate args (fail closed on malformed --cases-config)
        │
        ├── no --cases-config ──────────────▶ DEFAULT_CASES (the 6 audited rows)
        └── --cases-config <path> ──────────▶ parsed + validated case list (arbitrary N, D-02)
        │
        ▼
run_sweep(cases, n_col, precision, device)
        │
        │   for EACH case (independent, no shared state):
        ▼
   ┌────────────────────────────────────────────────────────────────┐
   │ measure_case(case, n_col, dtype, device)                        │
   │  mirrors controllers.py:576-580 + :629-676 EXACTLY               │
   │  (data/optimizer/loss-scheduling code removed)                   │
   │                                                                  │
   │  ArchitectureSpec(seed=case.seed)                                │
   │        │                                                        │
   │        ▼                                                        │
   │  build_network(spec, dtype=dtype, device=device) ──▶ model       │
   │        │                                                        │
   │        ▼                                                        │
   │  CollocationSampler(n_col, rng=np.random.default_rng(case.seed))  │
   │    .uniform() ──▶ raw times in [0, T]; np.argsort ──▶ sorted      │
   │        │                                                        │
   │        ▼                                                        │
   │  traj(u) = tau=2u-1; tau_ic13=cat([tau, case.ic13]);              │
   │            model(tau_ic13.unsqueeze(0), masses.unsqueeze(0))      │
   │        │                                                        │
   │        ▼                                                        │
   │  componentwise_du(traj, u_leaf) ──▶ (velocity, accel) = (v', a')  │
   │        │                                                        │
   │        ▼                                                        │
   │  positions = vmap(traj)(u_leaf);  force = softened_acceleration(  │
   │              positions, masses, dtype=dtype, device=device)       │
   │        │                                                        │
   │        ▼                                                        │
   │  residual = accel - force                                        │
   │  Rbar_n   = (residual**2).sum(dim=(-2,-1)) / 3.0   [D-05 formula] │
   │        │                                                        │
   │        ▼                                                        │
   │  causal_physics_loss(Rbar, times=raw_times, dtype=dtype,          │
   │                       device=device, return_details=True)         │
   │        │                                                        │
   │        ▼                                                        │
   │  w_n = details["w_n"]                                            │
   │  front_idx = max([n for n,w in enumerate(w_n.tolist())            │
   │                    if w > 0.5], default=-1)     [controllers.py   │
   │                                                  :692-694 formula]│
   │        │                                                        │
   │        ▼                                                        │
   │  per-point norms: ‖r'_n‖, ‖v'_n‖, ‖a'_n‖, ‖F_grav,n‖,              │
   │                    min-pairwise-sep_n                             │
   │        │                                                        │
   │        ▼                                                        │
   │  AGGREGATE: median across the n_col points for EACH of the       │
   │  5 per-point quantities + Rbar  ["medians over the 16             │
   │  collocation points" — audit §6b, verbatim]                       │
   └────────────────────────────────────────────────────────────────┘
        │
        ▼
ArchitectureCharacterizationResult (one per case: 7 SC1 quantities +
   provenance: seed scheme, collocation times, torch build, dtype/device)
        │
        ▼
provenance = {git_head() SHA + dirty flag, argv, torch_build, timestamp}
        │
        ▼
evidence writer: exclusive _new_run_dir() + atomic_write_text(raw.json, summary.md)
        │
        ▼
stdout table (six rows, matches audit §6b layout) + exit code
  (0 = measurement completed; this is NOT a pass/fail verdict — GATE-04 is
   Phase 56's job, not this probe's)


═══════════ SEPARATE, MECHANICAL-ONLY PATH (D-03) — never wired above ═══════════

synthetic residual array (test fixture only, e.g. np.arange(4096))
        │
        ▼
stratified_collocation_times(n_bins=16, per_bin=256, rng=seeded)
  bins: [b/16,(b+1)/16) for b=0..14, [15/16,1] for b=15   [54-RULING.md
                                                             verbatim bin edges]
        │
        ▼
bin_mean_residuals(rbar_per_point, bin_assignment, n_bins=16) ──▶ (16,) R̄_b
        │
        ▼
unit tests assert: exactly 256 rows/bin, correct bin-edge membership,
  arithmetic-mean correctness on a KNOWN synthetic input
        (NEVER fed into causal_physics_loss against the six real audited
         cases inside Phase 55 — that wiring + R_ref computation is Phase 56)
```

### Recommended Project Structure

```
pinn/verification/
├── architecture_characterization_probe.py   # NEW — this phase's module
│   ├── SweepCase (frozen dataclass)          # one case's input spec
│   ├── ArchitectureCharacterizationResult    # one case's measured output
│   ├── DEFAULT_CASES                         # the 6 audited rows (tuple)
│   ├── measure_case(...)                     # the per-case pipeline above
│   ├── run_sweep(cases=DEFAULT_CASES, ...)   # the real Python API (D-02)
│   ├── stratified_collocation_times(...)     # D-03 mechanical-only helper
│   ├── bin_mean_residuals(...)               # D-03 mechanical-only helper
│   └── main(argv=None)                       # CLI wrapper (argparse)
├── residual_probe.py            # existing — Phase 38 rung 3 (reference convention)
├── gate_metrics.py              # existing — Phase 43 (dataclass-result convention)
└── ...                          # existing probes, unchanged

tests/phase55/
├── __init__.py                               # NEW (empty, matches tests/phase38/ etc.)
└── test_architecture_characterization.py     # NEW

.planning/phases/55-architecture-characterization-probe/
└── evidence/
    └── probe/
        └── <UTC-timestamp>/
            ├── raw.json        # full six-row (or N-row) machine-readable output
            └── summary.md      # human-readable table, mirrors audit §6b layout
```

### Pattern 1: Mirror the trainer's low-level composition, not its high-level wrapper

**What:** Call `componentwise_du` + `softened_acceleration` directly and
assemble the residual/`Rbar`/causal-weight pipeline by hand, exactly as
`controllers.py:629-676` does — do not call the higher-level
`physics_residual()` convenience function.

**When to use:** Whenever a caller needs the intermediate first-derivative
(`v'`) alongside the residual — `physics_residual()` computes it internally
and discards it.

**Example (mirrors `controllers.py:576-580` and `:639-656` verbatim, with
data/optimizer/loss-scheduling removed):**
```python
# Source: pinn/training/controllers.py:576-580 (traj closure) and
# :639-656 (u_leaf -> velocity/accel/force/residual/Rbar composition)
def traj(u_scalar: torch.Tensor) -> torch.Tensor:
    tau = (2.0 * u_scalar - 1.0).reshape(1)
    tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
    pos = model(tau_ic13, masses_t.unsqueeze(0))
    return pos.reshape(3, 3)

u_leaf = torch.as_tensor(raw_times / T_CHARACTERISTIC_TIME, dtype=dtype, device=device)
first, second = componentwise_du(traj, u_leaf)          # v', a'
positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_leaf)
positions = positions.reshape(-1, 3, 3)
velocities = first.reshape(-1, 3, 3)
accel = second.reshape(-1, 3, 3)
force = softened_acceleration(positions, masses_t, dtype=dtype, device=device)
residual = accel - force
# CONF-04 / D-05: one vector-space average per time index (NOT all nine
# scalar components independently).
rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
```

### Pattern 2: The probe reports; it does not gate

**What:** `main()`'s exit code reflects whether the measurement completed
(0) or raised an exception (nonzero) — it is never a function of whether
`front_idx` "looks healthy" or any threshold passes.

**When to use:** Always, for this probe specifically. SC1-SC4 describe a
*measurement* instrument. GATE-04's fail-closed pass/fail verdict is a
Phase-56 requirement (`REQUIREMENTS.md` traceability: `GATE-04 → Phase 56`).
Inventing a pass/fail verdict inside Phase 55 would duplicate — and risk
diverging from — Phase 56's gate logic, and would blur the same
requirement-ownership boundary D-03 already draws for `R_ref`.

### Pattern 3: One seed governs a case's entire randomness

**What:** Each `SweepCase.seed` feeds (a) `ArchitectureSpec.seed` (network
init), (b) the `CollocationSampler`'s `numpy.random.Generator`, and where
applicable (c) the row-6-style random-tanh IC13 draw — via clearly
documented, independently-derived seeded streams (e.g., `seed` for (a)/(b)
and a distinct constant offset such as `seed + 10_000_000` for (c)), never
by drawing (c) from the same stream as (b) in an order-dependent way.

**When to use:** Every `SweepCase`. This exactly matches how the real
trainer is seeded — `pinn/train.py:1032-1035` seeds `CollocationSampler`
from `config.run.seed`, and `ArchitectureSpec.seed` is documented ("Seed
fan-out: `ArchitectureSpec.seed = config.run.seed` for weight init and
sampling" — `.planning/STATE.md` Decisions) as the *same* seed value in
production. Reusing one seed for both keeps the probe's per-case
determinism story simple and auditable.

### Anti-Patterns to Avoid

- **Copying `residual_probe.py`'s `required=True` `--precision`/`--device`
  argparse flags verbatim:** breaks D-02's "no arguments reproduces exactly
  the six audited rows" requirement. Default them instead.
- **Running the D-03 stratified/bin-mean helpers against the real six
  audited cases and persisting the output as evidence:** this is explicitly
  out of scope (D-03) — those helpers are unit-tested against synthetic
  arrays only inside Phase 55.
- **Hard-coding the causal-weight clamp floor as a literal** (e.g.
  `1.18e-38`, the float32 value the audit's §6a narrative discusses for the
  fp32-MPS *training run*) in the float64/CPU regression fixture — see
  Common Pitfalls below.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|--------------|-----|
| AD second derivative `d²r'/du²` | A custom `autograd.grad` loop or finite-difference Hessian | `pinn.physics_residual.componentwise_du` | SC3 mandate; already handles scalar/batched leaves, fails loud on non-finite (`_require_finite`), is the proven `jacrev∘jacrev`+`vmap` pattern the trainer itself uses |
| Gravitational force sum | A custom pairwise `1/r²` loop | `pinn.physics_residual.softened_acceleration` | SC3 mandate; exact PHYS-03 squared-norm softening and self-interaction masking are already correct and tested |
| Causal weight vector / `R̄` | A custom `exp(-eta*cumsum)` implementation | `pinn.loss_catalog.causal_physics_loss(..., return_details=True)` | SC3 mandate; the dtype-derived clamp-floor discipline (`resolve_causal_clip_facts`), the ascending-order assertion, and the `stopgrad`/detach semantics are already correct |
| Network construction / seeding | A bespoke `nn.Module` + manual weight init | `pinn.architecture_spec.ArchitectureSpec` + `pinn.network.build_network` | Locked topology validated fail-closed at construction; deterministic local-generator seeding already correct — reuse gets `ArchitectureSpec`'s own guard rails for free |
| Precision/device resolution | Scattered `torch.float64`/`"cpu"` literals through the module | `pinn.runtime.resolve_runtime(precision, device)` | Single seam (CTX-12..14); keeps the door open for an optional fp32-MPS arm without duplicating device logic |
| `front_idx` computation | A different "propagation front" heuristic (e.g. first index below 0.5) | The exact formula at `controllers.py:692-694`: `max([n for n,w in enumerate(w_n_list) if w > 0.5], default=-1)` | SC3 mandate; a different formula would make the probe's `front_idx` incomparable to the trainer's own reported metric |
| Evidence directory allocation | A bespoke tempfile scheme | Mirror the existing `_new_run_dir` idiom (private, duplicated per-probe today — `residual_probe.py:62-74` etc.) for exclusive, non-overwriting timestamped directories | Established, already-reviewed idiom across four existing probes |
| Evidence file writing | A bespoke write-then-close | `pinn.training.atomic_io.atomic_write_text(path, content)` | Newer shared idiom; additionally `fsync`s the parent directory, which the older probes' private `_atomic_write` omits — strictly safer, already promoted for exactly this reason ("so config_yaml, checkpoint, and guards import a single implementation rather than a fourth divergent copy" — `pinn/training/atomic_io.py:1-5`) |
| Git tree-state capture (SC2 re-derivability) | A raw, unbounded `subprocess.run(["git","rev-parse","HEAD"])` | `pinn.verify.git_head()` | Already bounded by a timeout and fail-soft (`(None, False)` rather than raising) on a wedged or missing `git` |
| Collocation-time sampling | A bespoke `np.random.uniform(...)` + manual sort | `pinn.training.collocation_sampler.CollocationSampler(collocation_count=n_col, rng=np.random.default_rng(seed)).uniform()` then `np.argsort` | Matches the trainer's exact sampling composition (`pinn/train.py:1032-1035`, `controllers.py:602-618`) — keeps the probe's *methodology*, not just its loss math, trainer-derived |

**Key insight:** Every trainer primitive this probe needs is already a
small, pure, already-tested function with an explicit `dtype`/`device`
argument and fail-loud non-finite checking. The entire implementation risk
in this phase is in *composition and aggregation* (which functions to call,
in what order, and how to reduce per-point values to the seven reported
scalars), not in re-deriving any physics or numerics — which is exactly what
SC3 requires.

## Common Pitfalls

### Pitfall 1: Hard-coding the float32 clamp floor in a float64 regression test

**What goes wrong:** A test asserts `w_2 == 1.1754943508222875e-38` (or
similar) as "the clamp floor," copied from the audit's §6a discussion of the
fp32-MPS *training run*.

**Why it happens:** The audit document's §6a section, which discusses the
live training run's numerics, is fp32/MPS; its §6b six-row table (what this
probe reproduces) is explicitly float64/CPU. It is easy to conflate the two
floors while reading the same document.

**How to avoid:** Live-verified this session (Torch 2.12.0):
`math.log(torch.finfo(torch.float32).tiny) ≈ -87.3365`, giving
`exp(floor) ≈ 1.1754943508222953e-38`; `math.log(torch.finfo(torch.float64).tiny)
≈ -708.3964`, giving `exp(floor) ≈ 2.2250738585072626e-308`. Always derive
the expected floor in a test via `pinn.loss_catalog.resolve_causal_clip_facts
(dtype, device)["causal_clip_min_weight"]`, never a copied literal.

**Warning signs:** Any test literal containing `1e-38`, `3.06e-7`, or
`87.3` inside a test file that also asserts `precision == "float64"`.

### Pitfall 2: Calling `physics_residual()` instead of its two constituent calls

**What goes wrong:** The probe calls the composed
`pinn.physics_residual.physics_residual(traj, u, masses, ...)` wrapper to
save a line of code, then has no way to report `‖v′‖` without a second,
duplicate AD pass.

**Why it happens:** `physics_residual()` is the more "obvious" single-call
entry point and is what `gradcheck_probe.py`/`componentwise_ad.py`-adjacent
code sometimes reaches for.

**How to avoid:** Call `componentwise_du(traj, u_leaf)` directly (as
`controllers.py:643` does) to get both `first` (velocity) and `second`
(acceleration) in one AD pass, then call `softened_acceleration` and
subtract, exactly mirroring `controllers.py:643-656`.

**Warning signs:** A `_velocity` or `first` variable immediately discarded
with `_` right after a call to `componentwise_du` inside a wrapper function,
followed by a *second* unrelated call that recomputes velocity.

### Pitfall 3: `required=True` precision/device flags breaking zero-argument invocation

**What goes wrong:** `main(argv=None)` copies
`parser.add_argument("--precision", required=True, ...)` from
`residual_probe.py`, so `python -m
pinn.verification.architecture_characterization_probe` with no flags exits 2
(argparse error) instead of running the six default cases.

**Why it happens:** Every existing Phase-38 probe genuinely requires
explicit precision/device intent (they touch real hardware trade-offs via
`fp32-MPS`). This probe's regression fixture, by contrast, is pinned to one
specific arm by D-01 ("fixed seed, float64, CPU"), so requiring the flags
serves no purpose here and actively conflicts with D-02.

**How to avoid:** `parser.add_argument("--precision", default="float64",
choices=("float32","float64"))` / `parser.add_argument("--device",
default="cpu", choices=("mps","cpu"))`.

**Warning signs:** A CLI contract test that calls the module with zero
arguments and expects the six default cases fails with argparse usage
output instead.

### Pitfall 4: Feeding the D-03 new-structure output into `causal_physics_loss` "for real"

**What goes wrong:** A well-intentioned executor wires
`bin_mean_residuals(...)` output for the real six audited cases into
`causal_physics_loss` and reports/persists the result, effectively computing
an early, ungoverned `R_ref`-like number.

**Why it happens:** Once the stratified sampling and bin-mean helpers exist
and are unit-tested, it is a natural (but out-of-scope) next step to "just
try it" on the real cases to see what the new structure gives.

**How to avoid:** D-03 draws the line explicitly: the new-structure helpers
are exercised **only** against synthetic residual arrays in the test suite.
Nothing in `run_sweep`'s default path (or any CLI flag) should invoke them
against `DEFAULT_CASES` and treat the output as characterization evidence.

**Warning signs:** A test or evidence artifact whose filename or docstring
contains `R_ref`, or a `4096`/`stratified` code path reachable from
`run_sweep`/`main`.

### Pitfall 5: `n_col` and the causal prefix length are coupled — passing raw 4096 points changes `η_c`'s effective calibration

**What goes wrong:** Someone increases the probe's default `n_col` from 16
to 4096 "for more resolution" without also changing how the causal prefix is
formed, silently producing a 4096-term exclusive-prefix-sum weight vector
instead of the ratified 16-term one.

**Why it happens:** `n_col` looks like a purely cosmetic "how many points to
sample" knob.

**How to avoid:** `54-RULING.md`'s pre-declared Completeness Rule states the
mechanical reason directly: `w_n` is an exclusive prefix sum over
collocation points, so the exponent moves by roughly 256× between 16 and
4096 points. The SC2 regression fixture must keep `n_col=16` (the
pre-amendment recipe); any `n_col=4096` exercise must go through the 16-bin
reduction first (D-03's mechanical-only path), never through raw per-point
`causal_physics_loss` at `n_col=4096`.

**Warning signs:** A `causal_physics_loss` call whose `residuals_per_time`
argument has more than 16 elements anywhere in `run_sweep`'s default path.

## Code Examples

### The six audited default cases (verbatim from the 2026-08-17 audit, §6b)

```text
# Source: docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/
#         2026-08-17-residual-frame-conformance-audit.md, §6b table
# (All six rows are the probe's printed output; MEDIANS over the 16
#  collocation points.)
#
# seed / IC                          ‖r′‖  ‖v′‖  ‖a′‖      ‖F_grav‖  min-sep  R̄ median   front_idx
# 41, m=(1,1,1), IC13=0              1.28  310   2.03e5    2.17      0.91     1.37e10    0
# 42                                 1.13  331   2.72e5    3.29      0.67     2.46e10    0
# 43                                 0.97  251   2.20e5    3.24      0.72     1.62e10    0
# 0                                  0.91  281   2.79e5    5.94      0.50     2.60e10    0
# 7                                  0.85  290   1.94e5    5.89      0.51     1.25e10    0
# 41, m=(1,0.8,0.6), random tanh IC13 0.95  231   2.28e5    2.85      0.72     1.74e10    0
```

Recommended `DEFAULT_CASES` construction (rows 1-5 share `masses=(1,1,1)`
and an all-zero IC13; only `ArchitectureSpec.seed` varies; row 6 reuses
`seed=41` with different masses and a random-tanh IC13):

```python
# Recommended structure (Claude's Discretion per CONTEXT.md — not a locked
# contract, but resolves the discretion point into a concrete shape).
DEFAULT_CASES = (
    SweepCase(label="41", seed=41, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="42", seed=42, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="43", seed=43, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="0",  seed=0,  masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="7",  seed=7,  masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="41-variable-mass", seed=41,
              masses=(1.0, 0.8, 0.6), ic13_mode="random_tanh"),
)
```

### `front_idx` — the exact trainer formula to reuse

```python
# Source: pinn/training/controllers.py:692-694 (verbatim)
"front_idx": max(
    [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
),
```

### The `Rbar` reduction — the exact trainer formula to reuse

```python
# Source: pinn/training/controllers.py:652-656 (verbatim, comment included)
# CONF-04 / D-05: one vector-space average per time index.  The
# residual has shape (N_t, 3 bodies, 3 Cartesian components), while
# the locked Rbar contract averages the three body-vector energies,
# not all nine scalar components.
rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
```

### The causal-clip floor — live-verified values (this session, Torch 2.12.0)

```python
# Computed via: .venv/bin/python -c "import math, torch; ..."
# torch.float32: tiny=1.1754943508222875e-38  log(tiny)=-87.3365447505531  exp(floor)=1.1754943508222953e-38
# torch.float64: tiny=2.2250738585072014e-308 log(tiny)=-708.3964185322641 exp(floor)=2.2250738585072626e-308
#
# Derive programmatically instead of copying either literal:
from pinn.loss_catalog import resolve_causal_clip_facts
facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
expected_floor_weight = facts["causal_clip_min_weight"]  # ~2.225e-308 for float64/cpu
```

### Minimum pairwise separation — existing sibling-probe pattern to mirror

```python
# Source: pinn/verification/residual_probe.py:97-103 (verbatim)
def _minimum_pairwise_separation(positions: torch.Tensor) -> torch.Tensor:
    """Return the minimum off-diagonal separation per snapshot in r' units."""
    difference = positions.unsqueeze(-3) - positions.unsqueeze(-2)
    separation = torch.linalg.vector_norm(difference, dim=-1)
    eye = torch.eye(3, dtype=torch.bool, device=positions.device)
    separation = separation.masked_fill(eye, torch.inf)
    return separation.amin(dim=(-2, -1))
```

### Bin edges for the D-03 mechanical-only new-structure helper

```text
# Source: .planning/phases/54-recalibration-decision-grounding/54-RULING.md,
# "Batch allocation and bin policy" section (verbatim)
# "The fixed bins are [b/16,(b+1)/16) for b=0…14 and [15/16,1] for the
#  last... Each bin therefore has exactly 256 rows... A bin residual is
#  the mean over its 256 rows."
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|-------------------|---------------|--------|
| An ad-hoc, uncommitted Python snippet run manually by the auditor on 2026-08-17; explicitly "nothing written to the repository" | Committed, tested `pinn/verification/architecture_characterization_probe.py` with a fixed default sweep + CLI + evidence provenance | This phase (Phase 55, v2.3) | v2.3's premise becomes re-derivable by anyone, not dependent on the original author's unrecorded session; Phase 56's GATE-04 gets a stable, importable Python API instead of re-deriving the logic |
| `pinn/train.py:1033` hard-codes `collocation_count=16`, diverging from `pinn_architecture.md`'s `n_col=4096` | `54-RULING.md` ratifies `n_col=4096` total-per-batch with a 16-fixed-bin structure (`D3`); Phase 55 builds (but does not exercise for real) the mechanical capability | 2026-09-04 (Phase 54 checkpoint ②); wired for real in Phase 56 | The probe must expose both the legacy 16-raw-point mode (for the SC2 regression, which targets the *pre-amendment* recipe) and the new 16-bin/4096-stratified mode (mechanically, unit-tested only) |
| `R̄` consumed unnormalized in the causal exponent (pre-amendment recipe — what SC2 reproduces) | `R̃_b = R̄_b / R_ref` normalized, with `R_ref` a frozen median-of-96-bin-means (ratified `B2`) | Phase 54 checkpoint ②; wired in Phase 56 | Phase 55's SC2 regression must run the OLD (unnormalized) recipe specifically — do not apply any `R_ref`-style normalization inside Phase 55's default six-case reproduction |

**Deprecated/outdated:**
- The 2026-08-17 ad-hoc probe methodology (an uncommitted, unrecorded
  script): superseded by this phase's committed tool. Any future reference
  to "the audit's six-row table" should point at this probe's evidence
  output, not attempt to re-derive the original ad-hoc script.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|----------------|
| A1 | The original 2026-08-17 ad-hoc audit probe used i.i.d. uniform collocation-time sampling drawn via a mechanism equivalent to `CollocationSampler.uniform()` + `np.argsort` (rather than, e.g., `np.linspace`). The audit explicitly states "nothing written to the repository," so the exact original scheme is unrecoverable. | Architecture Patterns Pattern 3; Standard Stack | LOW — D-01's regression tolerance for SC2 is order-of-magnitude (`1e9 < R̄ < 1e11`, `front_idx==0`), not bit-exact, so any faithful trainer-mirroring scheme satisfies SC2 regardless of whether it matches the untracked original exactly. SC3 independently mandates trainer-derived methodology, which this scheme already is. |
| A2 | The deterministic RNG scheme for the "random tanh IC13" case (audit row 6) — sample 13 i.i.d. values from a seeded generator and pass through `tanh` elementwise, seeded from a documented offset of the case's own `seed` field. | Code Examples; Architecture Patterns Pattern 3 | LOW — explicitly delegated to Claude's/the planner's discretion by CONTEXT.md; any deterministic, documented scheme satisfies the requirement (reproducibility), and this is one design choice among several reasonable ones. |
| A3 | Recommended concrete Tier-1 invariant numeric bounds beyond what CONTEXT.md states verbatim — e.g. `0.1 < ‖F_grav‖_median < 100` for "O(1)", `min_pairwise_separation_median > 1e-2` for "≫ eps_soft" (`eps_soft=1e-5`, a 1000x+ margin) — chosen to comfortably bracket the audit's observed ranges (`‖F_grav‖` 2.17-5.94; min-sep 0.50-0.91) with headroom for legitimate seed/case variation. | Common Pitfalls; Standard Stack (D-01 in User Constraints) | LOW — these are illustrative starting bounds for the planner/executor to adjust; D-01 itself says "e.g." for its own `1e9 < R̄ < 1e11` example, establishing that exact bound tuning is expected implementation-time judgment, not a locked value. |
| A4 | The recommended evidence subdirectory name `evidence/probe/` (vs. e.g. `evidence/characterization/` or `evidence/sweep/`) under `.planning/phases/55-architecture-characterization-probe/`. | Architecture Patterns, Recommended Project Structure | LOW — purely a naming choice; CONTEXT.md delegates evidence directory placement to Claude's discretion, only requiring it match the established per-category-subfolder convention (which any single reasonable name satisfies). |
| A5 | Recommending `--precision`/`--device` remain present (but defaulted, not required) on the CLI, rather than removing them entirely and hard-coding float64/CPU. | Standard Stack, Alternatives Considered | LOW — purely additive; keeping the flags (with sane defaults) preserves consistency with every other `pinn/verification/*_probe.py` entrypoint and gives a future user an explicit, low-cost way to sanity-check the fp32-MPS arm without any code change, while the default satisfies D-02's zero-argument requirement either way. |

**If this table is empty:** N/A — see entries above. All five assumptions
are low-risk design recommendations in an area CONTEXT.md explicitly
delegates to Claude's/the planner's discretion; none touch a physics
formula, a locked spec value, or a governance boundary (D-01/D-02/D-03
themselves, and every quoted formula/constant in this document, are
[VERIFIED] against source, not assumed).

## Open Questions

1. **Should the SC2 six-row reproduction's evidence artifact be generated as
   part of Phase 55's own execution (an actual committed run under
   `.planning/phases/55-*/evidence/`), or is "code capable of producing it,
   proven only by the test suite" sufficient?**
   - What we know: SC2's wording — "the reproduction is recorded
     re-derivably (command, tree state, full output)" — and the established
     precedent of Phase 38's rungs 3/4, which were both built *and* actually
     invoked once to produce committed evidence, strongly suggest an actual
     run's output should be committed, not merely code that could produce
     one.
   - What's unclear: whether the plan should treat "run the CLI once and
     commit its evidence" as a distinct, required task, or whether the test
     suite's own execution (which necessarily runs the real six-case sweep
     to make its assertions) is treated as satisfying the "recorded"
     requirement by itself.
   - Recommendation: treat it as a required, distinct task — run the CLI's
     default invocation once after the module and tests land, and commit
     the resulting `raw.json`/`summary.md` under
     `.planning/phases/55-architecture-characterization-probe/evidence/`,
     mirroring exactly how Phase 38's probes each have a committed evidence
     run in addition to their test suite.

2. **Should `run_sweep`'s per-case internals be individually unit-testable
   (i.e., should `measure_case` be a public, separately-importable
   function), or is the six-case `run_sweep` output the only public
   surface Phase 56 needs?**
   - What we know: CONTEXT.md's Integration Points note says "Phase 56's
     GATE-04 will need to import this module's sweep function and result
     type directly."
   - What's unclear: whether Phase 56 needs single-case granularity (e.g.
     to run one custom case under the new recipe) or only the whole-sweep
     entry point.
   - Recommendation: export both `measure_case` (single-case) and
     `run_sweep` (multi-case) in `__all__` — the marginal cost of exposing
     both is near zero, and it removes a potential Phase-56 blocker without
     over-committing to an API shape neither phase has confirmed yet.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|--------------|-----------|----------|-----------|
| Python (project `.venv`) | All of `pinn/` | Yes | 3.14.6 (system) — but `.venv/bin/python` is the correct interpreter | — |
| `torch` | Network construction, AD (`jacrev`/`vmap`), tensor ops | Yes (verified live in `.venv`) | 2.12.0 (requirements-lock.txt pins 2.12.1 — pre-existing drift, unrelated to this phase) | — |
| `numpy` | Collocation-time RNG, sweep-case arrays | Yes (verified live in `.venv`) | 2.2.0 (requirements-lock.txt pins 2.4.6 — pre-existing drift) | — |
| `pytest` | Test suite execution | Yes (verified live in `.venv`) | 9.1.1 | — |
| `git` | `pinn.verify.git_head()` for SC2 tree-state provenance | Yes (repo is a git checkout; `git status --short --branch` succeeded this session) | — | `git_head()` already fails soft (`(None, False)`) if git is ever unavailable — no probe-level fallback needed |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none — everything required is
already installed and working in this checkout's `.venv`.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.1.1 (verified live via `.venv/bin/python -m pytest --version`) |
| Config file | none — no `pytest.ini`/`pyproject.toml`/`setup.cfg` at repo root; pytest runs with defaults, relying on rootdir-based `sys.path` insertion (existing tests already import `pinn.*` directly, e.g. `tests/phase38/test_residual_probe.py:23`) |
| Quick run command | `.venv/bin/python -m pytest tests/phase55/ -q` |
| Full suite command | `.venv/bin/python -m pytest tests/ -q` (existing convention — cited verbatim in `.planning/STATE.md`'s Phase 46 note: "`pytest tests/ -q` reports 14 failures... NOT introduced by Phase 46") |

Both `unittest.TestCase`-style tests (the Phase 38 probe convention,
subprocess-CLI-driven — see `tests/phase38/test_residual_probe.py`) and
plain `pytest`-function-style tests (the Phase 49 gate-invariant convention
— see `tests/phase49/test_gate03_invariants.py`) coexist in this repo and
both collect cleanly under `pytest`; SC4's explicit callout — "the probe is
protected the way the Phase 49 gate work is" — suggests leaning toward the
Phase 49 style (direct in-process function calls, explicit numeric
assertions) for the Tier-1 invariant-bound tests, while a
subprocess/CLI-contract test (Phase 38 style) is still appropriate for the
CLI-argument-parsing and evidence-writing surface specifically. Both styles
may coexist in one `tests/phase55/test_architecture_characterization.py`
file.

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|---------------------|---------------|
| INST-04 (SC1) | Given `ArchitectureSpec` at init, no data/optimizer/training step, reports all 7 quantities over a configurable sweep | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_measure_case_reports_all_seven_quantities -x` | ❌ Wave 0 |
| INST-04 (SC1/D-02) | Zero-argument CLI/API invocation reproduces exactly the six audited cases; a `--cases-config` JSON drives an arbitrary case list | unit + CLI contract | `pytest tests/phase55/test_architecture_characterization.py -k test_default_cases_and_custom_config -x` | ❌ Wave 0 |
| INST-04 (SC2, Tier 1) | Invariant bounds hold for all six default cases: `front_idx==0`, `1e9 < R̄_median < 1e11`, `‖F_grav‖` O(1), min-pairwise-sep `≫ eps_soft`, `w_2..w_16` at the dtype-derived clamp floor | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_invariant_bounds_six_cases -x` | ❌ Wave 0 |
| INST-04 (SC2, Tier 2) | Full six-row exact-value fixture matches a committed JSON at tight relative tolerance | unit (regression fixture) | `pytest tests/phase55/test_architecture_characterization.py -k test_exact_value_fixture -x` | ❌ Wave 0 |
| INST-04 (SC2) | The reproduction is recorded re-derivably: committed evidence JSON/summary carries command, git tree state (SHA + dirty flag), and full six-row output | integration (CLI subprocess + evidence-file assertions) | `pytest tests/phase55/test_architecture_characterization.py -k test_cli_writes_provenance_evidence -x` | ❌ Wave 0 |
| INST-04 (SC3) | The probe's `Rbar`/causal-weight/AD calls are literally `pinn.loss_catalog`/`pinn.physics_residual` calls, not a parallel reimplementation | unit (source-level assertion, mirrors `tests/phase39/test_prohibitions.py`-style AST/import check, or a monkeypatch-and-assert-called test) | `pytest tests/phase55/test_architecture_characterization.py -k test_derives_from_trainer_implementation -x` | ❌ Wave 0 |
| INST-04 (SC4) | Mutating any reported quantity, the sweep configuration, or the six-row fixture fails the suite | unit (already covered by Tier-1/Tier-2 tests above — SC4 is a property of those tests existing and being exact/bound-checked, not a separate test) | (same commands as SC2 rows above) | ❌ Wave 0 |
| D-03 | The new 16-bin/256-per-bin stratified/bin-mean helpers are mechanically correct against synthetic residual arrays, and are never wired into the six-case default sweep | unit | `pytest tests/phase55/test_architecture_characterization.py -k test_stratified_bins_synthetic -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `.venv/bin/python -m pytest tests/phase55/ -q`
- **Per wave merge:** `.venv/bin/python -m pytest tests/ -q` (note: this
  checkout has 14 pre-existing, unrelated failures documented in
  `.planning/STATE.md` — see Environment Availability / STATE.md Blockers —
  do not treat those as Phase 55 regressions; diff the failure set before
  and after)
- **Phase gate:** Full suite green (modulo the documented pre-existing 14
  failures) before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/phase55/__init__.py` — empty, matches `tests/phase38/`,
  `tests/phase49/`, etc.
- [ ] `tests/phase55/test_architecture_characterization.py` — the whole
  suite above; no existing test file covers any part of this phase
  (`tests/phase55/` does not exist yet — confirmed this session)
- [ ] `pinn/verification/architecture_characterization_probe.py` — the
  module itself; no existing module implements any part of SC1-SC4 (`grep`
  confirms no `architecture_characterization` symbol anywhere in `pinn/`
  today)
- [ ] Committed exact-value fixture JSON (Tier 2, D-01) — does not exist
  yet; generated once the module is correct and reviewed, per D-01's own
  "regenerates the fixture explicitly" discipline
- Framework install: none — `pytest` is already installed in `.venv`

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|-----------------|---------|---------------------|
| V2 Authentication | No | Local, single-operator CLI/library tool; no auth surface |
| V3 Session Management | No | No session concept |
| V4 Access Control | No | No multi-principal access boundary |
| V5 Input Validation | Yes | `argparse` `choices=` constrains `--precision`/`--device`; a `--cases-config` JSON must be validated (seed is an int, masses are 3 finite positive floats, `ic13_mode` is one of a closed enum) BEFORE constructing any tensor — mirror `fixture_loader.py`'s `_validated_id`/`_validated_variant` "validate before any path/tensor is built" pattern. `ArchitectureSpec.__post_init__` (already reused) additionally fail-closed validates every architecture-shape field for free. |
| V6 Cryptography | No | No cryptographic operation; `sha256_file`-style provenance hashing (used elsewhere in `pinn/verification/`) is optional, not required, for this probe's evidence |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|-----------------------|
| Path traversal via `--evidence-root` / `--cases-config` pointing outside the intended tree (e.g. into `simulation_data/`) | Tampering / Information Disclosure | Mirror the existing `_reject_dataset_evidence_root` guard (`residual_probe.py:43-50` et al.) — reject an `--evidence-root` that resolves inside `simulation_data/` |
| Malformed/adversarial `--cases-config` smuggling a non-conformant architecture (e.g. `hidden_depth != 12`) | Tampering | Free, already-shipped mitigation: `ArchitectureSpec.__post_init__` raises `ValueError` on any locked-field deviation before any tensor is built — always construct a real `ArchitectureSpec` from parsed config, never bypass it with raw kwargs |
| Non-finite (NaN/Inf) values propagating silently into a passing-looking report | Tampering (silent data corruption) | Free, already-shipped mitigation: `componentwise_du`/`softened_acceleration`/`physics_residual` all call `_require_finite` and raise rather than return a corrupted result — the probe inherits this by calling those functions directly |
| Concurrent invocations racing on the same evidence directory, producing a partial/corrupted `raw.json` | Tampering (data integrity) | Mirror `_new_run_dir`'s exclusive-directory allocation (`mkdir(..., exist_ok=False)` retry loop) plus `atomic_write_text`'s tmp-write+fsync+`os.replace`+dir-fsync sequence |
| An unrepeatable/unverifiable "reproduction" claim (the exact gap SC2 exists to close) | Repudiation | Persist `git_head()`'s SHA, an explicit dirty/clean check (new, small — no existing precedent found for a dirty-tree check in `pinn/`; mirror `git_head()`'s bounded-subprocess pattern for a `git status --porcelain` call), the exact `argv`, and the full six-row output in the evidence JSON, per SC2's own "command, tree state, full output" language |

## Sources

### Primary (HIGH confidence — all read directly via the Read tool this session)

- `pinn/loss_catalog.py` (full file) — `causal_physics_loss`, `resolve_causal_clip_facts`, `LossWeights`, `compose_total`
- `pinn/physics_residual.py` (full file) — `componentwise_du`, `softened_acceleration`, `physics_residual`
- `pinn/architecture_spec.py` (full file) — `ArchitectureSpec`
- `pinn/network.py` (full file) — `SQRSkipResNetSIREN`, `build_network`
- `pinn/constants.py` (full file) — every locked scalar constant
- `pinn/training/controllers.py:560-702` — `_build_anchor_context`, `_non_data_terms` (the exact composition to mirror)
- `pinn/training/collocation_sampler.py` (full file) — `CollocationSampler`
- `pinn/runtime.py` (full file) — `resolve_runtime`, `RuntimeSpec`
- `pinn/train.py:1000-1050` — `collocation_count=16` hard-code, `CollocationSampler` construction
- `pinn/verify.py:355-395` — `git_head`
- `pinn/training/atomic_io.py` (full file) — `atomic_write_text`
- `pinn/verification/residual_probe.py` (full file) — CLI/evidence/dataclass conventions
- `pinn/verification/gradcheck_probe.py` (full file) — CLI/evidence conventions
- `pinn/verification/overfit_probe.py` (full file) — CLI/evidence conventions, diagnostics composition
- `pinn/verification/componentwise_ad.py` (full file) — timing/JSON-worker conventions
- `pinn/verification/fixture_loader.py` (full file) — validate-before-construct convention
- `pinn/verification/target_frame_probe.py:1-120` — dataclass naming conventions
- `pinn/verification/gate_metrics.py` (full file) — dataclass-result convention
- `tests/phase38/test_residual_probe.py` (full file) — CLI-subprocess test-assertion style
- `tests/phase49/test_gate03_invariants.py:1-50` — pytest-function test-assertion style
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:160-200, 420-485, 660-699` — SIREN init (§2.2), causal weight formula + `n_col` (§3.2), Phase 35/53 contract blocks
- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` (full file) — the new 4096/16-bin structure, `A1/B2/C1/D3/E1` ratification, bin-edge formula
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md:58, 115-127`, `.planning/STATE.md` — requirement/phase/decision grounding
- `.planning/phases/55-architecture-characterization-probe/55-CONTEXT.md`, `55-DISCUSSION-LOG.md` — locked decisions and discretion points
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` (full file) — the exact six-row measurement, the "medians over 16 collocation points" note, the `D³=GT²` conformance grounding
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md:126-151` — GAP-44-02 context
- Live-computed this session (`.venv/bin/python`): `torch.__version__` (2.12.0), `numpy.__version__` (2.2.0), `pytest --version` (9.1.1), float32/float64 causal-clip floor values

### Secondary (MEDIUM confidence)

- None — no web search or external documentation lookup was performed. This
  phase's entire technical surface is codebase-native (no new library or
  framework), and no MCP research provider (Context7, Exa, Brave, Firecrawl)
  is enabled for this project (`brave_search: false, firecrawl: false,
  exa_search: false` per `gsd-tools query init.phase-op 55`).

### Tertiary (LOW confidence)

- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — every module/function cited was opened and read
  directly this session; no external library research was needed.
- Architecture: HIGH — the exact composition to mirror
  (`controllers.py:576-580, 629-676`) was read verbatim; the aggregation
  contract ("medians over the 16 collocation points") is a direct quote
  from the audit document, not an inference.
- Pitfalls: HIGH for the dtype-clamp-floor and `physics_residual()`-wrapper
  pitfalls (both derived from live computation / exact source reads);
  MEDIUM for the specific numeric bound recommendations in Pitfall/A3 (
  reasonable illustrative values, explicitly flagged as adjustable).

**Research date:** 2026-09-04
**Valid until:** Phase 56 begins (this research is tightly coupled to the
exact line numbers and formulas in `pinn_architecture.md` and `pinn/`,
which Phase 56 is expected to edit under SCOPE-38 amendment discipline;
re-verify anchors if Phase 56 lands first) — otherwise treat as valid for
~14 days given this is an actively-moving v2.3 milestone.

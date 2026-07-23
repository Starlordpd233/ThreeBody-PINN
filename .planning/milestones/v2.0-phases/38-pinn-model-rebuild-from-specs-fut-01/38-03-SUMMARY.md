---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "03"
subsystem: pinn
tags: [pytorch, autograd, torch.func, jacrev, vmap, gradcheck, physics-residual, plummer-softening, brutus, provenance, sha256]

# Dependency graph
requires:
  - phase: 38-01
    provides: "pinn/constants.py (EPS_SOFT, D, T) and pinn/architecture_spec.py"
  - phase: 38-02
    provides: "pinn/network.py (SQR-SkipResNet-SIREN, tau = 2u - 1 computed inside forward) and pinn/com_projection.py (project_com)"
  - phase: 37
    provides: "pinn/runtime.py (the explicit precision/device seam) and pinn/verification/componentwise_ad.py (componentwise-AD + fail-loud discipline)"
provides:
  - "pinn/physics_residual.py — PHYS-02 componentwise-AD residual on the canonical u = t/T leaf, plus the §3.2 softened Newtonian force"
  - "pinn/verification/fixture_loader.py — read-only, provenance-recording, completeness-gated single-Brutus-trajectory loader"
  - "The residual→loss batch-dimension contract (leading N_t axis) that 38-04 and 38-05 build against"
affects: [38-04, 38-05, 38-06, 39]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Componentwise u-leaf AD via torch.func.jacrev composed with itself + vmap over the leading N_t axis (the r.sum() VJP is forbidden)"
    - "Second acceptable AD pattern for a graph-connected positions tensor: explicit per-output-component autograd.grad loop with a ones covector over the N_t axis only"
    - "Leading-N_t batch axis across the residual→loss seam"
    - "Validate-before-construct path resolution (typed ValueError on unknown variant / non-digit / out-of-range / traversal id)"
    - "Provenance binding: variant + id + resolved path + sha256 recorded on every fixture load"

key-files:
  created:
    - pinn/physics_residual.py
    - pinn/verification/fixture_loader.py
    - tests/phase38/test_physics_residual.py
    - tests/phase38/test_fixture_loader.py
  modified:
    - pinn/verification/__init__.py

key-decisions:
  - "Differentiate on the u leaf with NO manual 2x/4x chain factor: the network computes tau = 2u - 1 inside forward, so autograd already propagates the relation; applying the tau-leaf factors would double count (pinn_architecture.md §5.3.1; the plan's planner_assumptions reconciliation, grounded — not a gap)"
  - "physics_residual accepts EITHER a trajectory callable (jacrev + vmap) OR a positions tensor already graph-connected to the u leaf (explicit per-component autograd.grad loop). Both are §5.3.1-acceptable patterns; the tests assert they agree."
  - "The per-component grad loop's grad_outputs is a ones vector over the N_t axis ONLY. That is exact, not an approximation — u[n] influences only snapshot n, so the batch Jacobian is diagonal. It is NOT the forbidden component-summing VJP."
  - "gradcheck (fp64-CPU) exercises the training-relevant gradient path: parameters -> double-AD residual, with all pairwise separations kept far above the softening floor (edge R3)."
  - "The paired IC file is the raw-mass source of record when a trajectory is resolved by variant+id; the Brutus body lines supply the masses in the bare path= form. No cross-check threshold was invented."
  - "resolve_trajectory_path's dataset root is DERIVED from the module location (never hardcoded) and is overridable, so tests resolve against a tmp root without touching simulation_data/."

patterns-established:
  - "Fail-loud on non-finite: every leaf, position, derivative, and residual component is checked; a non-finite value raises rather than being emitted as evidence (threat T-38-11)"
  - "Read-only dataset discipline proven two ways: a runtime open-mode/mkdir spy AND a static source backstop that bans write APIs"

requirements-completed: [NET-03]

coverage:
  - id: D1
    description: "PHYS-02 componentwise-AD derivatives on the canonical u = t/T leaf, with no manual chain factor and no summed-output VJP"
    requirement: NET-03
    verification:
      - kind: unit
        ref: "tests/phase38/test_physics_residual.py#ComponentwiseDerivativeTests (worked-example symbolic oracle, no-manual-chain-factor, not-a-summed-VJP, batched (N_t,)->(N_t,9))"
        status: pass
    human_judgment: false
  - id: D2
    description: "Softened Newtonian force sum: r_safe = sqrt(||d||^2 + eps_soft^2), eps_soft = 1e-5, raw masses, G absorbed into D"
    requirement: NET-03
    verification:
      - kind: unit
        ref: "tests/phase38/test_physics_residual.py#SoftenedAccelerationTests (equal- and unequal-mass hand-computed oracles, squared-norm-not-distance softening, batched leading axis, non-finite refusal)"
        status: pass
    human_judgment: false
  - id: D3
    description: "physics_residual f_i = a'_i - sum_{j!=i} F_ij: gradcheck-clean under fp64-CPU, precision/device-agnostic, fail-loud, leading-N_t batch contract"
    requirement: NET-03
    verification:
      - kind: unit
        ref: "tests/phase38/test_physics_residual.py#PhysicsResidualTests + PrecisionAgnosticTests (gradcheck eps=1e-6/atol=1e-5/rtol=1e-3, callable vs positions-tensor agreement, fp32-MPS run, no default-dtype mutation)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Read-only probe-local Brutus fixture loader with provenance (variant/id/path/sha256) and the final-timestamp >= 9.5 completeness gate"
    requirement: NET-03
    verification:
      - kind: unit
        ref: "tests/phase38/test_fixture_loader.py#LoadTrajectoryTests + Sha256Tests + ReadOnlyDisciplineTests + ScopeBoundaryTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "resolve_trajectory_path typed input validation before any path is constructed (unknown variant, non-numeric / out-of-range id, no traversal)"
    requirement: NET-03
    verification:
      - kind: unit
        ref: "tests/phase38/test_fixture_loader.py#ResolveTrajectoryPathTests (folder mapping, 4-digit zero pad, unknown variant, bad id, 9 traversal ids, containment)"
        status: pass
    human_judgment: false
  - id: D6
    description: "The recommended default example trajectory (standard_quasi_random_gold_standard / id 0000) resolves and loads against the REAL dataset"
    requirement: NET-03
    verification: []
    human_judgment: true
    rationale: "No Brutus trajectory payload exists on disk in this worktree (bulk data excluded — orchestrator fact, recorded in the plan's <default_trajectory>). The loader is proven against a synthetic in-format tmp fixture; only the operator can run it against the real dataset location and confirm the nominal ID is not an intentional ID-gap."

# Metrics
duration: 42min
completed: 2026-07-13
status: complete
---

# Phase 38 Plan 03: Physics Residual and Fixture Loader Summary

**PHYS-02 componentwise-AD residual on the canonical `u = t/T` leaf (jacrev+vmap, no manual chain factor, gradcheck-clean under fp64-CPU and live under fp32-MPS) plus a read-only, sha256-provenanced, completeness-gated single-Brutus-trajectory loader with traversal-proof path resolution.**

## Performance

- **Duration:** ~42 min
- **Tasks:** 3 of 3
- **Files created:** 4
- **Files modified:** 1
- **Tests:** 34 new (17 residual + 17 loader), all passing; wave-1/2's 59 tests still passing

## Accomplishments

- `pinn/physics_residual.py` implements the PHYS-02 contract exactly as `pinn_architecture.md` §5.3.1 states it: the autograd leaf is `u = t/T`, the derivatives are componentwise (all nine `dr'_{i,α}/du`), and **no** manual 2×/4× factor is applied — the network's internal `tau = 2u - 1` is propagated by autograd itself. A dedicated test would catch a double-counted factor: it asserts `dr'/du == 2·dr'/dtau` and `d²r'/du² == 4·d²r'/dtau²` for a forward that computes `tau` internally, which only holds if the module adds nothing on top.
- The forbidden `torch.autograd.grad(r.sum(), u)` anti-pattern is nowhere in the module, and a test proves the componentwise result agrees with per-component autograd term-by-term (a summed-output VJP would collapse the nine into one).
- `softened_acceleration` implements §3.2 with `r_safe = sqrt(||r'_j - r'_i||² + eps_soft²)`, `eps_soft = EPS_SOFT` (1e-5, imported from `pinn/constants.py` — no re-literal), raw masses, and `G = 1` absorbed by the nondimensionalization. The PHYS-03 anti-pattern (adding `eps` to the *distance*) is ruled out by a test at a separation of exactly `eps_soft`, where the two forms differ by a large factor.
- `torch.autograd.gradcheck` passes under fp64-CPU (`eps=1e-6`, `atol=1e-5`, `rtol=1e-3`) on the training-relevant gradient path (parameters → double-AD residual), with all pairwise separations kept far above the softening floor per edge R3. The identical code path then ran under fp32-MPS on this host (that arm was NOT skipped).
- `pinn/verification/fixture_loader.py` parses one Brutus trajectory + its paired IC, records provenance (variant, id, resolved path, sha256 of both files), and applies the mandatory `final timestamp >= 9.5` completeness gate. The heterogeneous `Result:` footer is captured as metadata only — a test proves a footer claiming a complete run does **not** rescue a truncated file.
- `resolve_trajectory_path` validates **before** constructing any path: an unknown variant, or a non-digit / negative / out-of-range / bool / float id, or any id bearing a separator, `..`, `~`, or a leading `/`, raises a typed `ValueError`. Nine traversal payloads are tested.
- Read-only dataset discipline is proven twice: a runtime spy on `open` / `Path.open` / `os.mkdir` / `os.makedirs` asserts read-mode-only opens and zero directory creations, and a static source backstop asserts the module contains no write API at all.

## Task Commits

1. **38-03-01: Author the RED test suites (tests-first)** — `881c6520` (test)
2. **38-03-02: Implement the read-only Brutus fixture loader** — `da19d0a0` (feat)
3. **38-03-03: Implement the PHYS-02 componentwise-AD residual** — `ef349d63` (feat)

The plan is `type: execute` with two `tdd="true"` tasks; the RED gate is commit `881c6520` (34 tests, `OK (skipped=34)` — SKIP, never ERROR, via per-symbol deferred imports), and the GREEN gates are `da19d0a0` and `ef349d63`. No REFACTOR commit was needed.

## Files Created/Modified

- `pinn/physics_residual.py` (created, 292 lines) — `componentwise_du`, `softened_acceleration`, `physics_residual`; the PHYS-02 u-leaf AD contract and the §3.2 softened force.
- `pinn/verification/fixture_loader.py` (created, 404 lines) — `load_trajectory`, `resolve_trajectory_path`, `sha256_file`, `TrajectoryFixture`, `TrajectoryPaths`, `IncompleteTrajectoryError`, `VARIANTS`.
- `pinn/verification/__init__.py` (modified) — docstring now states Phase 38 adds the fixture loader and the rung probes, imported on demand (the Torch-heavy rung modules are deliberately NOT force-imported at package import).
- `tests/phase38/test_physics_residual.py` (created, 541 lines) — 17 tests.
- `tests/phase38/test_fixture_loader.py` (created, 434 lines) — 17 tests.

## Verification (exact commands and real output)

`conda` is not on the non-interactive shell PATH in this worktree; the absolute path is used.

1. Plan verification — both suites:

```
<home>/miniforge3/bin/conda run -n pinn-train python -m unittest \
  tests.phase38.test_physics_residual tests.phase38.test_fixture_loader -v
-> Ran 34 tests in 2.035s
-> OK
```

2. Plan verification — imports:

```
<home>/miniforge3/bin/conda run -n pinn-train python -c \
  "import pinn.physics_residual, pinn.verification.fixture_loader"
-> both import ok
```

3. Per-task verification:

```
python -m unittest tests.phase38.test_fixture_loader -v    -> Ran 17 tests, OK
python -m unittest tests.phase38.test_physics_residual -v  -> Ran 17 tests, OK
   (test_gradcheck_fp64_cpu ... ok; test_runs_under_fp32_mps ... ok — MPS available, NOT skipped)
```

4. RED gate (before the production modules existed):

```
python -m unittest tests.phase38.test_physics_residual tests.phase38.test_fixture_loader -v
-> Ran 34 tests, OK (skipped=34)   [SKIP, never ERROR]
```

5. Wave-1/2 regression (must not regress):

```
python -m unittest tests.phase38.test_constants tests.phase38.test_architecture_spec \
  tests.phase38.test_network_structure tests.phase38.test_com_projection
-> Ran 59 tests in 0.556s
-> OK
```

6. Governance mechanical checks:

```
git diff --check                          -> clean
git status --short simulation_data/       -> empty (dataset untouched)
grep -E "mkdir\(|makedirs\(|write_text\(|write_bytes\(|shutil\.|os\.remove|os\.rename|set_default_dtype|is_available\(" \
  pinn/physics_residual.py pinn/verification/fixture_loader.py
-> one hit only: a DOCSTRING sentence in physics_residual.py stating the module never
   calls torch.set_default_dtype. No executable write API, no default-dtype mutation,
   no availability probe. (Same docstring convention as pinn/runtime.py.)
```

**Not run:** the `tests/phase37` suite. Its discovery executes the D1-p timing-protocol probes (10 warmups × 30 samples × 100 evaluations per arm) and exceeded the 2-minute command budget. Nothing in this plan touches Phase 37 code except the `pinn/verification/__init__.py` docstring; `componentwise_ad` is unchanged and still imports and re-exports cleanly.

## Decisions Made

- **The u-leaf / chain-factor reconciliation is grounded, not a gap.** `pinn_architecture.md` §5.3.1 states it explicitly: differentiating w.r.t. `u` uses no chain factor; the 2× / 4× factors apply only to a direct `tau` leaf. Because `pinn/network.py` computes `tau = 2u - 1` inside `forward`, autograd on the `u` leaf already produces those factors. The module therefore applies none. This follows the plan's `<planner_assumptions>` verbatim; nothing was invented.
- **Two AD entry forms, both §5.3.1-acceptable.** `physics_residual` accepts a trajectory callable (→ `jacrev` composed with itself, `vmap`-ed over `N_t`) or a positions tensor already graph-connected to the `u` leaf (→ explicit per-output-component `autograd.grad` loop). A test asserts the two agree, so the seam 38-04/38-05 build against is proven consistent regardless of which form a consumer uses.
- **The ones-covector in the per-component loop spans the `N_t` axis only.** This is exact, not an approximation: `u[n]` influences only snapshot `n`, so the batch Jacobian is diagonal and the reduction returns precisely `d positions[n,k] / d u[n]`. It is categorically not the forbidden VJP, which sums over *output components*. This is documented in the module.
- **gradcheck target = parameters → residual.** The physically meaningful and training-relevant path, and it keeps the finite-difference check well conditioned (all separations ≫ `eps_soft`, per edge R3).
- **IC file is the raw-mass source of record for the variant+id form.** No mass-consistency threshold between the IC file and the Brutus body lines was invented (the spec is silent; inventing a gate would be a semantic decision). In the bare `path=` form the Brutus body lines supply the masses.
- **Dataset root is derived, overridable, never hardcoded.** `Path(__file__).resolve().parents[2] / "simulation_data" / "Data"`, with a `root=` override so tests resolve against a tmp tree.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a self-inflicted test bug: sha256 read after tmpdir teardown**

- **Found during:** Task 38-03-02 (first GREEN run of `test_fixture_loader`)
- **Issue:** `test_variant_and_id_resolution_records_variant_and_id_provenance` computed the expected sha256 with `brutus.read_bytes()` *after* the `TemporaryDirectory` context had exited, so the fixture file was already deleted → `FileNotFoundError`. A bug in the test I authored in task 38-03-01, not in the loader.
- **Fix:** Read the expected hash (and the file name) inside the tmp lifetime, then assert after the block.
- **Files modified:** `tests/phase38/test_fixture_loader.py`
- **Verification:** `python -m unittest tests.phase38.test_fixture_loader -v` → Ran 17 tests, OK.
- **Committed in:** `da19d0a0` (task 38-03-02 commit)

---

**Total deviations:** 1 auto-fixed (1 bug, in my own test).
**Impact on plan:** None. No scope creep; no interface change; the loader's behavior was never in question.

## Planner-Assumption Calls

- **PHYS-02 chain-factor reconciliation:** implemented per the plan's grounded reading (u-leaf, no manual factor) and locked by a test that would fail on a double-counted factor. See Decisions.
- **Edge R3 (softening-active points):** handled exactly as the plan specifies — (a) fail-loud on non-finite components, (b) gradcheck inputs kept far above the softening floor. The 38-04 probe's documented pairwise-separation guard (part (c)) belongs to that plan, not this one.

## STOP-Protocol Gaps

**None.** Every decision traced to `pinn_architecture.md` §5.3.1 / §3.2, `pinn/constants.py`, `simulation_data/Documentation/README.md`, `.claude/rules/dataset-reference.md`, or the plan's own `<planner_assumptions>` / `<artifacts_produced>` / `<default_trajectory>`. Where a source was silent and a choice would have been semantic (e.g. an IC↔Brutus mass-consistency threshold), no rule was invented — the code simply does not gate on it.

## Issues Encountered

- `conda` is absent from the non-interactive shell PATH; the absolute interpreter path
  (`<home>/miniforge3/bin/conda run -n pinn-train ...`) was used throughout. Recorded here so 38-04/38-05 do not rediscover it.
- `tests/phase37` full-suite discovery is slow enough to exceed a 2-minute command budget (timing probes). Run its modules individually if a Phase 37 regression check is ever needed.

## Scope Boundaries Honored

- **`simulation_data/` is untouched** — `git status --short simulation_data/` is empty. Every fixture is synthesized in a unittest tmp dir; no real Brutus payload exists in this worktree (expected, per the plan's orchestrator note).
- **No v1.3-era derivation** — neither new module imports or copies `pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`, or `pinn/data-handling/`. Both are framework-spec / dataset-README derived (CTX-17).
- **NOT the Phase 39 adapter** — no Step-1A gate, no splits, no batching, no `data_version_hash`. A `ScopeBoundaryTests` test asserts none of that surface leaked in.

## Next Phase Readiness

- **38-04** (probes) can consume `physics_residual` and `load_trajectory` now. The batch contract is fixed: `(N_t, 3, 3)` positions + `(N_t,)` u leaf → `(N_t, 3, 3)` residual, `N_t` leading.
- **38-05** (loss catalog) can build every loss term against batched `(N_t, ...)` tensors reducing to a scalar, with no shape refactor at the seam.
- **Operator action (D6, human_judgment):** the recommended default trajectory (`standard_quasi_random_gold_standard`, id `0000`) has not been loaded from the real dataset — no payload exists in this worktree. The loader fails loudly if that nominal ID is an intentional ID-gap; the operator supplies `--variant`/`--id` or `--path` at probe time.
- **38-06** can run its phase-wide mechanical checks (no-write, AST no-import, precision/device AST) against both new modules; the local equivalents already pass.

## Self-Check: PASSED

All claimed artifacts exist on disk and all claimed commits exist in git history:

- `pinn/physics_residual.py` — FOUND
- `pinn/verification/fixture_loader.py` — FOUND
- `tests/phase38/test_physics_residual.py` — FOUND
- `tests/phase38/test_fixture_loader.py` — FOUND
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-03-SUMMARY.md` — FOUND
- commit `881c6520` — FOUND
- commit `da19d0a0` — FOUND
- commit `ef349d63` — FOUND

---
*Phase: 38-pinn-model-rebuild-from-specs-fut-01*
*Completed: 2026-07-13*

# Phase 38: PINN Model Rebuild from Specs (FUT-01) - Context

**Gathered:** 2026-07-12
**Mode:** `--auto --all` (all gray areas auto-selected; recommended options chosen and logged)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 38 delivers the spec-faithful `pinn/` model package rebuilt from the
authoritative framework specs: the SQR-SkipResNet-SIREN network (14-dim
`[τ, IC₁₃]` → 12×256 → 9-dim), the hard mass-weighted COM projection head,
the PHYS-02 autograd physics-residual module, and the locked five-term loss
catalog — proven correct by three rungs (fp64-CPU `gradcheck`,
residual-on-ground-truth, single-trajectory overfit) before any training run,
fed by a minimal probe-local trajectory fixture loader.

The phase does not ingest the admitted dataset (Phase 39), build the training
loop or PHYS-05 scheduler module (Phase 40), parse YAML config or checkpoint
(Phase 41), or edit the framework specs (SCOPE-18: build-discovered spec
defects are surfaced as gaps, never fixed here).

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**5 requirements are locked (NET-01..NET-05).** See `38-SPEC.md` for full
requirements, boundaries, constraints, and acceptance criteria.

Downstream agents MUST read `38-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**
- The rebuilt spec-faithful `pinn/` model package: network module
  (SQR-SkipResNet-SIREN), COM projection head, PHYS-02 physics-residual
  module, five-term loss catalog.
- A config-supplied architecture spec (the architecture block consumed at
  instantiation); precision/device resolved through the existing
  `resolve_runtime` seam.
- The three proof rungs for this phase: fp64-CPU `gradcheck`,
  residual-on-ground-truth probe, single-trajectory overfit probe — with
  recorded evidence and tests following the `tests/phase37` pattern.
- A minimal probe-local trajectory fixture loader — just enough to feed
  rungs 3–4 with one Brutus trajectory. It is NOT the Phase 39 adapter
  (no Step-1A gate, no splits, no batch construction).

**Out of scope (from SPEC.md):**
- Data ingestion (Phase 39, DATA-01..06); the training loop and PHYS-05
  scheduled-weight *module* (Phase 40, TRAIN-01..07 — Phase 38's loss
  consumes a supplied weight vector); config/checkpointing/resume/guards/
  determinism (Phase 41, CTRL-01..08); runbook/monitoring (Phase 42);
  `verify`-ladder packaging, smoke test, Stage-0 pilot (Phase 43).
- Editing the framework specs (SCOPE-18); deleting the v1.3-era reference
  files (retirement is a later cleanup decision); multi-stage curriculum,
  stochastic-L-BFGS, RAD collocation, streaming residency (PLAT-01..07).

</spec_lock>

<decisions>
## Implementation Decisions

Labels continue Phase 37's CTX namespace (CTX-01..14) to avoid collision with
spec-side decision IDs (v1.4 D-02 COM head, trainex D-04 causal mode, etc.).

### Package & Module Layout
- **CTX-15:** New spec-derived code lands as flat single-purpose modules in
  `pinn/` — a network module, a COM-projection module, a physics-residual
  module, a loss-catalog module, and a small constants module holding the
  locked science constants (raw-mass `D ≈ 4.6416`, `eps_soft = 1e-5`, SIREN
  ω values, Huber δ values), each constant cited to its spec section. This
  follows the Phase 37 precedent (`pinn/runtime.py`): flat, snake_case,
  single-purpose. Exact filenames are planner discretion within these
  constraints; names must not collide with the v1.3-era files.
- **CTX-16:** The three proof rungs live in the existing `pinn/verification/`
  subpackage beside `componentwise_ad.py`, one independently invocable module
  per rung. Phase 43 later packages the rungs into the `verify` ladder;
  Phase 38 only guarantees each rung runs standalone.
- **CTX-17:** The v1.3-era files (`basic_architecture.py`,
  `data-processing-pipeline-full.py`, `data-handling/`) remain in place
  untouched and are never imported by new modules — reference-only, never
  grounding (SPEC prohibition: no implementation derived from v1.3 code).

### Architecture Config Schema (NET-01 "config-supplied")
- **CTX-18:** The config-supplied architecture spec is a frozen typed
  dataclass (the `RuntimeSpec` pattern), validated at construction — fields
  covering input/output dims, hidden depth/width, SIREN `first_omega_0` /
  `hidden_omega_0`, LayerNorm placement + `elementwise_affine`, skip
  configuration, and the seed. The spec-locked values are its validated
  defaults (they are locked science, not owner seams); the structure test
  asserts the instantiated topology against `pinn_architecture.md` §2.3/§2.4.
- **CTX-19:** No YAML parsing in Phase 38. Phase 41 (CTRL-01) owns the keyed
  YAML and maps its architecture block onto this dataclass; Phase 38 tests
  and probes construct the dataclass directly.
- **CTX-20:** Precision and device are NOT fields of the architecture block.
  They flow exclusively through `resolve_runtime` (ENV-04, CTX-12..14); model
  construction accepts the resolved dtype/device explicitly and encodes no
  default. Instantiation from the same config + seed is deterministic and
  performs no filesystem or global-state writes (SPEC AC #3).

### COM Projection Wiring (NET-02)
- **CTX-21:** The projection head is wired inside the model's public forward
  path: `forward()` returns projected positions as the ONLY public output.
  The unprojected 9-dim tensor is reachable solely through an explicitly
  named internal/test hook used by the projection tests (Σ mᵢ·rᵢ′ = 0,
  idempotence). This makes "no loss or metric can consume unprojected
  output" a structural property, verified by a test per SPEC AC #4.

### Probe CLI & Evidence Contract (rungs 2–4)
- **CTX-22:** Each rung follows the `componentwise_ad.py` CLI pattern:
  argparse with explicit required `--precision {float32,float64}` /
  `--device {mps,cpu}` resolved via `resolve_runtime`. The `gradcheck` rung
  documents and enforces its fp64-CPU contract but still selects the arm
  explicitly — no module encodes a precision default (CTX-14 persists).
- **CTX-23:** Evidence is timestamped and non-overwriting under
  `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/<rung>/<UTC>/`,
  with machine-readable JSON and an owner-readable Markdown summary written
  together (CTX-07 pattern carried forward). Recorded values include the
  residual threshold + measured residuals (rung 3) and the initial loss /
  achieved floor / reduction ratio (rung 4), per SPEC acceptance criteria.
- **CTX-24:** Probes exit PASS/FAIL through exit codes with the numeric
  criterion printed (executable-probe pattern); any invocation that certifies
  MPS behavior runs with `PYTORCH_ENABLE_MPS_FALLBACK` unset (Phase 37
  discipline, SCOPE-20).

### Fixture Loader & Trajectory Provenance
- **CTX-25:** The minimal fixture loader is probe-local in
  `pinn/verification/`: it parses exactly one Brutus trajectory file (plus
  its IC/masses) into tensors under an explicitly passed dtype/device. It
  implements no Step-1A gate, no splits, no batching, no
  `data_version_hash` handling — those are Phase 39's adapter.
- **CTX-26:** The trajectory is supplied at probe invocation (path or
  variant+ID), never hardcoded (no absolute paths — repo convention). Each
  probe records provenance in its evidence: variant, ID, resolved path, and
  file hash. The planner picks and documents the default example trajectory
  (a known-good admitted one) and records the rationale.
- **CTX-27:** `simulation_data/` is strictly read-only for every Phase 38
  code path (SPEC MUST NOT; mechanical check wired at plan time).

### Loss & Weights Interface (NET-04)
- **CTX-28:** The loss module exposes one function/callable per term — data
  Huber (`δ_r = 1`), IC squared-error anchors, causally-weighted physics
  residual (owner-ratified D-04 Option A mode), soft-energy Huber
  (`δ = 1.0`), componentwise angular-momentum Huber (`δ = 1.0`) — plus a
  composer computing the weighted total from a **supplied** five-field named
  frozen weights container (named fields, not positional). The PHYS-05
  scheduler that produces that vector over training is Phase 40 (TRAIN-03).
- **CTX-29:** The composer returns per-term scalars alongside the weighted
  total (small result container), so the widened OPS-03 logging (5 terms +
  total + λ vector) can consume it in Phase 42 without refactor.
- **CTX-30:** All terms evaluate in the shared dimensionless system; the
  `t_τ ∈ [-1,1]`, `r′ = r/D`, raw-mass `D ≈ 4.6416` conversions come from
  the locked constants module (CTX-15), tested against spec formulas.

### Test Organization
- **CTX-31:** `tests/phase38/` mirrors the `tests/phase37/` pattern (pytest,
  per-module test files): structure/topology test, deterministic-seeded
  instantiation + no-side-effects test, projection tests (zero-COM,
  idempotence, no-unprojected-consumption), residual/gradcheck tests,
  per-term loss tests (δ values, causal weighting, dimensionless
  conversions), and probe contract tests. No new test framework.
- **CTX-32:** The two SPEC prohibitions left without a wired check by
  `--auto` (framework-spec byte-identity across Phase 38 commits; no writes
  under `simulation_data/`) get mechanical checks placed by the planner —
  as tests or plan-level verification steps, per SPEC's own note.

### Claude's Discretion (planner latitude)
- Exact module/file names within CTX-15/16 constraints; dataclass field
  names; probe flag spellings beyond `--precision`/`--device`; evidence JSON
  field names.
- Rung tolerances that trainex-r1a §5 leaves numerically open: plan-phase
  fixes each value and records the rationale (SPEC constraint; informed by
  the R-6 dual-arm framing, ~1e-4 fp32-vs-fp64 relative). These are
  build-engineering values, not owner-carved seams.
- Unresolved SPEC edge rows (R3: gradcheck/residual behavior at
  softening-active points; R4: Huber transition at `|x| = δ` and
  causal-weight extremes; R5: overfit non-convergence must FAIL loudly, not
  hang) are treated as planner assumptions per SPEC, not held-out test
  obligations.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase Requirements & Planning
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-SPEC.md` —
  Locked requirements — MUST read before planning (NET-01..05, boundaries,
  constraints, acceptance criteria, edge/prohibition coverage tables).
- `.planning/REQUIREMENTS.md` — NET-01..05 text, SCOPE-16..21, and the
  owner-carved-seam table (v2.0 build discipline).
- `.planning/ROADMAP.md` — Phase 38 goal + success criteria; Phase 39/40
  seams this phase must not cross.
- `.planning/STATE.md` — D1-p recorded **fp32-MPS** (fp64-CPU escape hatch);
  integrity-r2 clearance (PB-2 five-term catalog); branch/worktree record.
- `.planning/PROJECT.md` — viability-slice doctrine; owner-carved decisions
  built as seams, never invented.

### Authoritative Science Specs (read-only inputs — SCOPE-18/21)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  — §2.3/§2.4 architecture (topology, SIREN ω, skip + LayerNorm), §3 loss
  terms, §4.1 PHYS-05 weights, §5.3.1 PHYS-02 AD contract (chain-rule
  factors, componentwise loop), §10.3 componentwise-AD probe contract.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  — loss-function contract; dimensionless system; curriculum context the
  loss/causal weighting must match.

### Ratified Build-Engineering Decisions
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md`
  — §5 pre-flight rungs 2–4 (gradcheck, residual-on-ground-truth,
  single-trajectory overfit); the D/B engineering decision set.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md`
  — owner ratification + the five carved-out decisions.
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md`
  — PB-1..PB-5 dispositions; PB-2 is the five-term Huber loss catalog
  authority NET-04 implements.

### Phase 37 Substrate (consume; follow its patterns)
- `pinn/runtime.py` — the `resolve_runtime` precision/device seam (consume,
  never re-implement or default around).
- `pinn/verification/componentwise_ad.py` — probe CLI + §10.3 AD patterns +
  evidence discipline to mirror for rungs 2–4.
- `.planning/phases/37-developer-environment-precision-adjudication/37-CONTEXT.md`
  — CTX-01..14, especially CTX-12..14 precision discipline that persists
  through Phase 38.
- `tests/phase37/` — the test-organization pattern `tests/phase38/` mirrors.
- `.planning/phases/37-developer-environment-precision-adjudication/evidence/`
  — timestamped non-overwriting evidence layout precedent.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `pinn/runtime.py` (`resolve_runtime`, `RuntimeSpec`): the exact seam every
  new module consumes for dtype/device; also the pattern template for the
  architecture-spec dataclass (frozen, validated, two-profile discipline).
- `pinn/verification/componentwise_ad.py`: argparse CLI shape, timing/warmup
  protocol, synthetic-trajectory fixtures, and evidence-writing discipline
  reusable for the three rungs.
- `tests/phase37/` (55 tests): naming, fixture, and contract-test patterns
  to mirror in `tests/phase38/`.
- `scripts/agent-commit` + git hooks: the mandated atomic commit path.
- `environment.yml` / `requirements-lock.txt` / `setup.sh`: the verified
  `pinn-train` environment — no environment work needed this phase.

### Established Patterns
- Spec-as-source-of-truth: code implements `pinn_architecture.md` /
  `ctl_instruction.md`; divergences are gaps to surface, never silent fixes.
- Executable probes with explicit numeric criteria and PASS/FAIL exits, not
  prose acceptance.
- Frozen dataclass configs validated at construction; explicit dtype/device
  passing; no global default-dtype mutation; no hidden availability fallback.
- Repo conventions: snake_case modules, pathlib over os.path, relative
  imports (no `sys.path.insert`), no hardcoded absolute paths, print/logging
  per existing probe style.

### Integration Points
- Model/loss modules consume `resolve_runtime` output (fp32-MPS production
  default recorded by the owner; fp64-CPU escape hatch).
- The fixture loader is a stopgap: Phase 39's adapter (DATA-01..) replaces
  it as the data source; the loss's supplied-λ seam is filled by Phase 40's
  PHYS-05 scheduler (TRAIN-03); Phase 41 wires YAML → architecture
  dataclass; Phase 43 packages the rungs into the `verify` ladder.
- `pinn/verification/` is the shared home for probe rungs (Phase 37
  established; Phase 43 consumes).

</code_context>

<specifics>
## Specific Ideas

- Keep the three rungs visibly symmetric with the Phase 37 probe in CLI,
  evidence layout, and PASS/FAIL discipline, so the owner reads one evidence
  grammar across the whole pre-flight ladder.
- Make the projection head's "only projected output is public" wiring a
  structural property of the model class, not a convention — the
  no-unprojected-consumption test then verifies architecture, not usage.
- Treat recorded measured values (residual threshold + measured, overfit
  floor + ratio) as first-class evidence, mirroring how Phase 37 treated
  fallback state and actual device.

</specifics>

<deferred>
## Deferred Ideas

- Admitted-set ingestion, Step-1A gate, `data_version_hash`, splits, batch
  construction, Thrust-A scan → Phase 39 (DATA-01..06).
- PHYS-05 scheduled-weight module, curriculum/run controllers, stage-exit
  machine → Phase 40 (TRAIN-01..07).
- YAML config, checkpointing, resume, guards, determinism → Phase 41
  (CTRL-01..08).
- `verify` ladder packaging, smoke test, Stage-0 pilot, gate check →
  Phases 42–43.
- v1.3-era file retirement/deletion → later cleanup decision (explicitly out
  of scope per SPEC).

### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` — matched at score 0.2 (below
  the 0.4 auto-fold threshold); STATE.md already records it as a spec-side
  sensitivity question outside the v2.0 build phases. Not Phase 38 work.

</deferred>

---

*Phase: 38-pinn-model-rebuild-from-specs-fut-01*
*Context gathered: 2026-07-12*

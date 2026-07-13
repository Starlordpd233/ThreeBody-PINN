# Phase 38: PINN Model Rebuild from Specs (FUT-01) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-12
**Phase:** 38-pinn-model-rebuild-from-specs-fut-01
**Mode:** `--auto --all` — all gray areas auto-selected; for each question the
recommended option was chosen by the agent (no interactive prompts). Every
selection is grounded in Phase 37 precedent, the ratified trainex-r1a set, the
locked SPEC, or repo conventions; none touches spec-locked science or the five
owner-carved seams.
**Areas discussed:** Module layout, Architecture config schema, COM projection
wiring, Probe CLI & evidence, Fixture loader & provenance, Loss/λ interface,
Test organization

---

## Module Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Flat single-purpose modules in `pinn/` + rungs in `pinn/verification/` | Phase 37 precedent (`runtime.py`, `verification/`); non-colliding with v1.3 files | ✓ |
| New nested subpackage (e.g. `pinn/model/`) | More structure than 4–5 modules warrant; diverges from Phase 37 pattern | |
| Replace v1.3 files in place | Violates SPEC out-of-scope (v1.3 files remain reference-only) | |

**Auto-selected:** Flat modules + `pinn/verification/` rungs (CTX-15..17).

## Architecture Config Schema (NET-01)

| Option | Description | Selected |
|--------|-------------|----------|
| Frozen typed dataclass, spec-locked validated defaults; YAML deferred to Phase 41 | Mirrors `RuntimeSpec`; keeps CTRL-01 ownership of YAML intact | ✓ |
| YAML file + loader now | Pre-empts Phase 41 CTRL-01 single-keyed-YAML contract | |
| Plain dict | No validation; weaker than the established typed pattern | |

**Auto-selected:** Frozen dataclass (CTX-18..20). Precision/device excluded
from the block — `resolve_runtime` only (CTX-14 persists).

## COM Projection Wiring (NET-02)

| Option | Description | Selected |
|--------|-------------|----------|
| Projection inside `forward()`; unprojected output via internal/test hook only | Makes "no loss/metric consumes unprojected output" structural | ✓ |
| Separate projection call left to callers | Convention-dependent; AC #4 would test usage, not architecture | |

**Auto-selected:** Structural wiring (CTX-21).

## Probe CLI & Evidence (rungs 2–4)

| Option | Description | Selected |
|--------|-------------|----------|
| `componentwise_ad.py` pattern: required `--precision`/`--device`, timestamped non-overwriting evidence (JSON + MD) | One evidence grammar across the pre-flight ladder | ✓ |
| New bespoke runner/harness | Reinvents a verified pattern; more surface | |

**Auto-selected:** Mirror the Phase 37 probe pattern (CTX-22..24).

## Fixture Loader & Trajectory Provenance

| Option | Description | Selected |
|--------|-------------|----------|
| Probe-local loader in `pinn/verification/`; CLI-supplied trajectory; provenance (variant, ID, path, hash) in evidence | Respects the Phase 39 boundary; no hardcoded paths | ✓ |
| Hardcode a chosen trajectory | Violates path conventions; hides provenance | |
| Use/extend v1.3 parsing code | Prohibited (no implementation derived from v1.3 files) | |

**Auto-selected:** Probe-local + CLI-supplied + recorded provenance
(CTX-25..27). Planner documents the default example trajectory + rationale.

## Loss / λ Interface (NET-04)

| Option | Description | Selected |
|--------|-------------|----------|
| Per-term functions + composer over a five-field named frozen weights container; per-term scalars returned | Explicit, serializable, feeds OPS-03 widened logging later | ✓ |
| Positional λ list | Error-prone ordering; weaker interface for Phase 40 handoff | |
| Single monolithic loss function | Blocks term-level unit tests the SPEC requires | |

**Auto-selected:** Named container + composer (CTX-28..30).

## Test Organization

| Option | Description | Selected |
|--------|-------------|----------|
| `tests/phase38/` mirroring `tests/phase37/` (pytest, per-module files) | Established pattern; SPEC names it explicitly | ✓ |
| Co-located tests inside `pinn/` | Diverges from repo layout | |

**Auto-selected:** `tests/phase38/` (CTX-31..32).

## Claude's Discretion

Routed to the planner (recorded in CONTEXT.md): exact file/field/flag names;
rung tolerance values left numerically open by trainex-r1a §5 (fixed at plan
time with recorded rationale); SPEC edge rows R3/R4/R5 treated as planner
assumptions; mechanical placement of the two unwired prohibition checks
(spec byte-identity; no `simulation_data/` writes).

## Deferred Ideas

Phase 39: ingestion/gate/splits/batching/scan. Phase 40: PHYS-05 scheduler
module + controllers. Phase 41: YAML/checkpointing/resume/guards. Phases
42–43: runbook, `verify` ladder, smoke test, Stage-0 pilot. Later cleanup:
v1.3-era file retirement. Reviewed-not-folded todo:
`d-06-static-epsilon-sensitivity-check.md` (score 0.2; spec-side question
outside v2.0 build phases).

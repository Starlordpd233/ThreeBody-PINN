# Phase 20.5 — Data Alignment and FUT-01 Hand-off

**Phase:** 20.5 (Sampling Coordinate Allocation)
**Milestone:** v1.4
**Date:** 2026-06-07

## Purpose

This is a forward-pointing hand-off document. It records that the Sobol coordinate
allocation convention locked in `sampling_method.md` by Phase 20.5 **matches** the
data-generation code in `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
It is an *alignment* record, not a `NN-CODE-DIVERGENCE.md` — see GAP-20-5-03.

## Alignment statement

Code anchors below cite stable symbols (classes, methods, variables) and section headings,
not line numbers, so this record survives line drift.

| Spec claim (`sampling_method.md`, "Sobol Coordinate Allocation Convention") | Code anchor (`ic_generation_utils.py`) | Status |
|---|---|---|
| `d = 3 + δ_s + 3δ_v` | `EnhancedThreeBodySampler` Sobol-dimension computation (the `sobol_dim` attribute) | ALIGNED |
| `u_1`–`u_3` → position | `_process_sobol_batch` position block (`idx 0→3`) | ALIGNED |
| `u_4` → scale `s` (when `δ_s = 1`) | `_process_sobol_batch` scale block (`u_scale = sobol_batch[:, idx]`) | ALIGNED |
| `u_{4+δ_s}`–`u_{6+δ_s}` → velocity (when `δ_v = 1`) | `_process_sobol_batch` velocity block (`u_vel = sobol_batch[:, idx:idx+3]`) | ALIGNED |
| Standard config `d = 7` | `generate_ics.py` standard config (`scale_range=(0.8, 1.2)`, `velocity_scale=0.1`) | ALIGNED |

## Scoped provenance claim

The Phase 20.5 provenance claim is scoped precisely — no more, no less:

1. **What is claimed.** The current v1.4 `sampling_method.md` spec, the documented and
   current configuration of the `simulation_data/Scripts/ic_generation/` generator under its
   standard configuration (`ic_type="standard"`, `scale_range=(0.8, 1.2)`,
   `velocity_scale=0.1`, `rotate=False`), and the current observable behavior of
   `EnhancedThreeBodySampler` are **aligned** on the Sobol dimension formula and the
   position/scale/velocity allocation order.

2. **What is not claimed.** No in-repository generation manifest, commit hash, or other
   persistent record independently proves that every file in
   `simulation_data/Data/ic_final/ic_standard_quasi_random/` was produced by this exact
   script revision. Repository documentation identifies `generate_ics.py` /
   `ic_generation_utils.py` as the standard quasi-random generator, but that identification
   is a documentation assertion, not a cryptographic provenance chain. If external logs
   later contradict that provenance, surface the conflict before FUT-01 relies on the
   alignment record.

3. **Regeneration.** No data regeneration is required to resolve this coordinate-allocation mismatch, because there is no mismatch to resolve — the spec and the data-generator behavior agree. This statement is not a blanket historical-provenance certification of the stored dataset; it is scoped to the Sobol-allocation alignment that Phase 20.5 locked.

## FUT-01 hand-off

- FUT-01 implementers build PINN/data code from the v1.4 framework specs. For Sobol
  allocation, the v1.4 spec (`sampling_method.md`, "Sobol Coordinate Allocation
  Convention") is authoritative and is statistically equivalent to the existing
  `ic_generation_utils.py` behavior.
- The PINN code in `pinn/` remains non-authoritative (directive 2026-05-19). If `pinn/`
  data-handling code assumes a different Sobol layout, FUT-01 corrects the `pinn/` code to
  this spec — the spec is not changed to match `pinn/`.
- No data regeneration is required for Sobol-allocation reasons: the spec matches the data.

## AC-SAMP-01 (acceptance check, for Phase 21 execution under VER-04)

- **Name:** `AC-SAMP-01` — Sobol coordinate allocation alignment.
- **What it checks:** three evidence surfaces, all of which must pass:
  1. **SPEC:** the `sampling_method.md` "Sobol Coordinate Allocation Convention" subsection
     is present; the dimension formula `d = 3 + δ_s + 3δ_v`, the fixed allocation order
     (position → optional scale → optional velocity), the standard-configuration branch
     (`δ_s = δ_v = 1`), and the no-scale branch (`δ_s = 0`) are all stated; the obsolete
     double-booked velocity statement (`The next three Sobol coordinates (u_4, u_5, u_6)
     are mapped to a 3D velocity vector`) is absent; the Phase 18 momentum sentence is
     intact.
  2. **ENTRYPOINT:** `simulation_data/Scripts/ic_generation/generate_ics.py` AST-parses
     cleanly and contains at least one `ic_type="standard"` call whose kwargs are
     `scale_range=(0.8, 1.2)` and `velocity_scale=0.1`.
  3. **SAMPLER:** `EnhancedThreeBodySampler` from
     `simulation_data/Scripts/ic_generation/ic_generation_utils.py` passes the dimension
     matrix (`sobol_dim` ∈ {7, 6, 4, 3} for `(δ_s, δ_v)` ∈ {(1,1), (0,1), (1,0), (0,0)}),
     the standard-config scale and velocity allocation (scale ← Sobol column 3; velocity
     ← columns 4–6), the synthetic position test (columns 0–2 drive the expected spherical
     mapping), the no-scale velocity allocation (columns 3–5), and the rotate=False
     boundary.
- **Data:** none required — instantiates `EnhancedThreeBodySampler` directly.
- **Probe:**
  `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`.
- **Pass criterion:** the probe exits 0 with `PASS` lines across all three surfaces and the
  summary `All three surfaces (SPEC, ENTRYPOINT, SAMPLER) passed.` Any `FAIL` line or
  nonzero exit is an AC-SAMP-01 failure.
- **On failure:** routes back to Phase 20.5 for spec correction per VER-04 / VER-05; v1.4
  does not ship while `AC-SAMP-01` fails.

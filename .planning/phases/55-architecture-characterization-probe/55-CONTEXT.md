# Phase 55: Architecture Characterization Probe - Context

**Gathered:** 2026-09-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 55 builds **committed, tested tooling** under `pinn/verification/` that
measures the SQR-SkipResNet-SIREN network's residual/causal-weight behavior at
**initialization only** — no data, no optimizer, no training step — over a
configurable seed/IC sweep. It must derive `R̄` and the causal weight vector
from the trainer's own implementation (not a parallel re-implementation), and
a regression test must prove it reproduces the 2026-08-17 residual-frame
conformance audit's six-row ad-hoc measurement (§6b) under the pre-amendment
recipe.

This is the instrument Phase 56's GATE-04 fires, and (per `54-RULING.md`) the
same instrument the ratified recalibration's `R_ref` will eventually be
measured with. Phase 55 owns building that general capability; it does **not**
own running the real new-structure measurement or computing/persisting
`R_ref` — see D-03 below.

Ungated (roadmap: "Depends on: Nothing"), runs independently of Phases 53/54
(now both complete).

</domain>

<decisions>
## Implementation Decisions

All three gray areas below were resolved by Claude's engineering judgment per
owner instruction (2026-09-04: "choose all areas worth discussion following
your best judgement... no need for user manual decisions unless there's
something I need to look at"). None involve a physics/spec adjudication call
(no framework-spec value or formula is being decided) — they are test-design
and API-scope choices the discuss-phase philosophy places in Claude's lane.

### Regression protection (SC4)

- **D-01: Two-tier regression gate.** (1) A hard **invariant-bound** assertion
  suite that must hold for all six audited cases — `front_idx == 0`, `R̄`
  median within its recorded order-of-magnitude band (e.g. `1e9 < R̄ < 1e11`
  per row, matching the audit's own "`R̄ ≈ 10¹⁰`" framing and ROADMAP SC2's
  language), `‖F_grav‖` O(1) and minimum pairwise separation `≫ eps_soft`
  (rules out a near-singular-encounter confound), and `w_2..w_16` pinned at
  the dtype clamp floor. This is the primary regression net — robust to
  legitimate refactors (dtype/backend/torch-version drift), but still catches
  a real behavioral change. (2) A secondary **exact-value fixture**: the full
  six-row output (all reported quantities, not just `R̄`) captured as a
  committed JSON, compared on re-run with a tight relative tolerance (the
  computation is fully deterministic — fixed seed, float64, CPU, no
  training — so bit-level reproducibility is expected on the same
  platform/torch version). A deliberate implementation change that legitimately
  shifts values regenerates the fixture explicitly, mirroring how
  `pinn/verification/gate_metrics.py`'s tests pin exact schema/threshold
  values today. — **Reversibility:** reversible — test-only, no production
  code depends on the chosen tolerance.

### Sweep generality (SC1)

- **D-02: General config-driven sweep, six audited cases as the built-in default.** The tool accepts an arbitrary list of `(seed, masses, IC13-mode)`
  cases via a Python API and CLI/config surface (matching the established
  `pinn/verification/*_probe.py` argparse `main(argv)` convention); calling it
  with no arguments reproduces exactly the six audited rows. This is not just
  Claude's preference — the ROADMAP's own goal statement for this phase says
  the measurement "becomes committed, tested tooling **that anyone can re-run
  against any candidate recipe**," which requires genuine configurability, not
  six hard-coded cases. This is also what lets Phase 56 invoke the same tool
  under the new 4096/16-bin structure without new code. — **Reversibility:**
  reversible — an internal API; Phase 56 depends on it existing, not on its
  exact call signature.

### New-structure (4096-total/16-bin) scope boundary

- **D-03: Build the capability; do not exercise it as a milestone artifact.**
  Phase 55's own regression obligation (SC2) is strictly the OLD 16-point
  baseline reproduction under the pre-amendment recipe. Phase 55 must make the
  tool **mechanically capable** of the new 4096-stratified/256-per-bin/16-bin
  structure `54-RULING.md` (row B2) describes, and should unit-test that
  binning/stratification/bin-mean logic correctness directly (e.g. against
  synthetic residual arrays) — but must **not** run the real six-case sweep
  under the new configuration and present its output as `R_ref` or as
  GATE-04-relevant evidence. `R_ref` and GATE-04 are Phase 56 requirements
  (traceability table: `INST-04 → Phase 55`, `GATE-04 → Phase 56`); computing
  a number that looks like `R_ref` inside Phase 55 would create an
  untracked, ungoverned precursor to a value `54-RULING.md` requires to be
  measured, persisted with full provenance, and re-measured on any structural
  change — that governance belongs to Phase 56, not to this one.
  — **Reversibility:** one-way if violated — an early, uncommitted `R_ref`-like
  number produced outside Phase 56's provenance discipline could get quoted
  informally and would need to be explicitly disavowed later; cheap to avoid
  by simply not running that configuration for real in this phase.

### Claude's Discretion

- Exact module name/location under `pinn/verification/` (e.g.
  `architecture_characterization_probe.py`), dataclass shape for the returned
  result (following `gate_metrics.py`'s `TrajectoryGateMetrics`-style
  convention), CLI flag names, and the deterministic RNG scheme used for the
  "random tanh IC13" variable-mass case (audit row 6) — document whatever
  fixed seed/method is chosen in the module docstring and provenance output so
  the case is reproducible, per repo convention (`fixture_loader.py`,
  `residual_probe.py` document their own conventions the same way).
- Evidence directory placement under `.planning/phases/55-*/evidence/`
  matching the established convention (e.g. Phase 50's
  `evidence/{calibration,corpus,attempts,...}/` layout).
- Test file location: `tests/phase55/test_architecture_characterization.py`,
  following `tests/phase49/`'s per-phase test directory convention.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope & requirements
- `.planning/ROADMAP.md` "Phase 55: Architecture Characterization Probe" — goal, dependencies, all 4 success criteria (verbatim source for SC1-SC4 referenced above)
- `.planning/REQUIREMENTS.md` INST-04 — the requirement this phase closes; also read GATE-04 (Phase 56) and SCOPE-38 for the boundary D-03 depends on
- `.planning/STATE.md` "Session Continuity" (as of 2026-09-04) — the operator note that the instrument "must support the new ruling's 4096-total/16-bin reference and GATE-04 vectors without editing the ratified recipe"

### The exact measurement to reproduce
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` §6b "Direct measurement" — the six-row table (seed/IC, ‖r′‖, ‖v′‖, ‖a′‖, ‖F_grav‖, min pairwise sep, median `R̄`, `front_idx`), and §6c for the mechanism narrative (SIREN second-derivative scale vs. unnormalized causal-weight calibration)

### The ratified recalibration this instrument feeds (Phase 56, not this phase — grounding only)
- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` rows for `η_c` (A1), `R̄` normalization/`R_ref` (B2, residual-wide), `ω₀` (C1/D3-A), and `N_t`/`n_col` (D3) — defines the exact 4096-total/256-per-bin/16-bin structure and the `R_ref` = median-of-96-bin-means procedure this tool must be *capable of* running

### Locked spec sections the probe measures against
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §2.2 (SIREN init, `first_omega_0 = 30`), §3.2 (causal weight formula, `n_col`), §5.3.1 (AD contract, `u = t/T` leaf, no chain-rule factor)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (must derive from these, per SC3 — not reimplement)
- `pinn/loss_catalog.py::causal_physics_loss(rbar, times=..., return_details=True)` — the exact trainer causal-weight formula; returns `{"w_n":..., "rbar":...}` when `return_details=True`. This IS the causal-weight computation to call.
- `pinn/physics_residual.py::componentwise_du(fn, u_leaf)` — the AD second-derivative (`a' = d²r'/du²`) the trainer uses.
- `pinn/physics_residual.py::softened_acceleration(positions, masses, *, eps_soft=EPS_SOFT, dtype, device)` — the gravity force term (`F_grav`).
- `pinn/architecture_spec.py::ArchitectureSpec` (frozen dataclass, `input_dim=14, output_dim=9, hidden_depth=12, hidden_width=256, seed=0` defaults) + `pinn/network.py::build_network(spec, *, dtype, device)` — deterministic network construction from a local seeded `torch.Generator` (no global RNG touched); `spec.seed` is exactly the per-case seed knob the sweep needs.
- `pinn/training/controllers.py:577-660` — the reference wiring showing how a real anchor context assembles `traj`, `u_leaf`, `componentwise_du`, `softened_acceleration`, and `causal_physics_loss` together; the new probe's core loop should mirror this composition (minus data/optimizer/loss dependencies).

### Established Patterns
- Every `pinn/verification/*_probe.py` module (`residual_probe.py`, `gradcheck_probe.py`, `overfit_probe.py`, `target_frame_probe.py`, `componentwise_ad.py`) is a standalone script: `argparse`-based `main(argv=None)` + `if __name__ == "__main__":`, importable functions in `__all__` for library use, no wiring into any automated verify ladder or CI gate (confirmed: no cross-references from any verify/CLI entrypoint). GATE-04 (Phase 56) will presumably import/invoke this module directly rather than finding it auto-wired anywhere.
- `pinn/verification/gate_metrics.py` shows the repo's dataclass-result + docstring-contract convention (`TrajectoryGateMetrics`, `AggregateGateMetrics`, exhaustive docstring naming every formula and gate threshold) — good template for the new probe's result type.
- `tests/phase38/test_residual_probe.py` shows the repo's assertion style: threshold assertions (`assertLess(x, 1e-5)`) plus exact-field assertions on provenance/schema (`sha256`, exact string labels) — informed D-01.
- Evidence-directory convention: `.planning/{milestone}-phases/NN-*/evidence/<category>/<timestamp>/` (e.g. Phase 50's `evidence/{calibration,corpus,attempts,verify,...}/`).

### Integration Points
- Phase 56's GATE-04 will need to import this module's sweep function and result type directly — keep the public API (function names, result dataclass fields) stable once Phase 55 lands, since Phase 56 is a hard downstream consumer.

</code_context>

<specifics>
## Specific Ideas

No specific UI/output-format requests beyond what's already fixed by SC1
(exact fields to report) and the established repo conventions captured above.

</specifics>

<deferred>
## Deferred Ideas

- **Cleanup of two stale pending todos** (`d-06-static-epsilon-sensitivity-check.md`,
  `trainex-r1-research-handoff.md`) — owner flagged these as candidates for
  disposition/removal if no longer relevant, but explicitly **after** Phase 55's
  real work, not now. Revisit at Phase 55 close or milestone close, not during
  Phase 55 execution.

### Reviewed Todos (not folded)
- **d-06-static-epsilon-sensitivity-check** (score 0.6, keyword match on
  generic terms) — a spec-side epsilon-sensitivity question unrelated to the
  architecture-only characterization probe; not folded.
- **trainex-r1-research-handoff** (score 0.6, keyword match on "parallel") —
  the r1b tuning-round handoff; unrelated to this phase's tooling scope; not
  folded.

</deferred>

---

*Phase: 55-Architecture Characterization Probe*
*Context gathered: 2026-09-04*

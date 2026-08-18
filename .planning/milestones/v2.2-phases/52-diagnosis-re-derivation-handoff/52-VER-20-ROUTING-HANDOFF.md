# VER-20 — Spec-Amendment Routing List Handoff

SCOPE-30 forbids editing framework-spec files in v2.2. This is the handoff of
every spec-amendment item accumulated during the milestone, for the next
milestone that is authorized to edit `ctl_instruction.md` / `pinn_architecture.md`.

## Items (a)–(d): named at v2.2 roadmap creation

**(a) Misleading "default" wording on `pinn_architecture.md` §4.1's `λ_phys^max` line.**
The line reads as though the value is a tunable default; GAP-45-03 ratified
that the full PHYS-05 per-stage table is locked, not defaulted. Needs
rewording to state the table binds.

**(b) Convention for marking locked-vs-default values inside a spec table.**
No existing spec convention distinguishes a locked constant from an
illustrative default within the same table. GAP-45-03's ruling exposed the
gap; item (a) is one instance of a systemic wording problem.

**(c) Explicit `L_data` reduction, settled by CONF-07.**
GAP-45-01 resolved (2026-07-31, Phase 48 checkpoint): mean over time, bodies,
and spatial components. The spec should state this explicitly rather than
leaving it inferable from code.

**(d) Aggregate gate statistic from GAP-44-01.**
The held-out physics gate's headline statistic (worst-case max, not mean or
median) was owner-ruled 2026-07-23 but is not codified in the spec.

## Item (e): added by v2.2 Phase 50/52

**(e) Causal-weight calibration vs. SIREN second-derivative initialization scale
(`pinn_architecture.md` §2.2 and §3.2).**

The locked SIREN initialization (`first_omega_0=30`, 12 layers) and the locked
causal-weighting formula (`w_n = exp(−η_c·Σ_{m<n} R̄_m)`, `η_c=1` on
unnormalized `R̄`) are each internally consistent in isolation but were never
calibrated against each other. At initialization, an `ω₀=30` SIREN's second
derivative is `O(10⁵)` in the network's own units, giving `R̄≈10¹⁰` —
independent of seed, IC, and (per the retained 502-step log) independent of
training budget within the tested range. `η_c=1` on unnormalized `R̄`
underflows float32 at `R̄>87.3`, so the causal weighting mechanism saturates
shut at step 0 and stays saturated: 15 of 16 collocation-point weights sit on
the numerical floor, and the physics loss reduces to a single point's
residual for the whole run.

**This is not a request to reword a spec table.** It is a request to
recalibrate one or more of: `η_c` / the causal-exponent form, an explicit
normalization of `R̄` (e.g. by a converged-scale reference), or the SIREN
initialization scale — or to redesign the curriculum mechanism so it does not
require the two to already agree at initialization. None of these can be
chosen without external research grounding: the correct calibration is a
research question, not an engineering default, and the project's ERW
build-design channel already has substantial groundwork in the trainex-r2
research report (`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`,
Q3), which independently derived the SIREN-scale mechanism as a hypothesis and
explicitly deferred the remedy to the owner. v2.3's scope should be built
around resolving this item; see the v2.3 milestone proposal for the proposed
narrow follow-up ERW round.

**Grounding:** `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`; `52-DIAG-05-REDERIVATION.md` §3.

## Disposition

All five items are handed off unresolved — no spec file is edited by this
document or by v2.2. Items (a)–(d) are narrow wording/codification fixes with
no open research question. Item (e) is the substantive one and is expected to
be v2.3's primary content.

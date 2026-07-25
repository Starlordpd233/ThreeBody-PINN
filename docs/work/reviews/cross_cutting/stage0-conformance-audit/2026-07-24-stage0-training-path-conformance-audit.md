---
status: active
purpose: verification-report
created: 2026-07-24
milestone: untracked
phase: cross-cutting
retirement_trigger: Retire when its findings have been transcribed into a maintained known-divergence register and each divergence is either closed or carries a dated owner waiver.
---

# Stage-0 Training Path — Spec Conformance Audit

**Purpose.** Establish the full divergence inventory between the executed
Stage-0 training path and the locked framework specs, rather than the six
spot-checked claims from the trainex-r2 report. Intended to seed the
known-divergence register proposed in
`docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`.

**Method.** Read-only. Every locked formula, constant, and schedule in
`pinn_architecture.md` §3.1–§3.5 / §4.1 and `ctl_instruction.md` total-loss
assembly was compared against the code that executed, plus the run configs, the
per-step logs, and the test suite. No file edited, no training run, no
evaluation invoked. Prior evidence:
`docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`.

**Scope boundary.** Covers the loss/physics math, the weight schedules, the
instrumentation, the COM head, and the science constants — the path that shaped
the physics-gate outcome. Does **not** cover: the data-loading/frame path
(undecidable here, corpus payload absent — see "Carried unresolved"), network
architecture internals, checkpoint/determinism/guard platform code, or the
evaluator/gate-metrics path.

---

## The central finding

**The component layer is spec-faithful and well-tested. Every confirmed
divergence lives in the assembly, wiring, and configuration layer — which has no
spec-formula tests. In two cases the test suite actively locks a divergence in
place.**

This is a coherent architectural conclusion, not a list of unrelated bugs. The
pure functions in `pinn/loss_catalog.py`, `pinn/physics_residual.py`,
`pinn/com_projection.py`, and `pinn/constants.py` transcribe the locked math
correctly, cite their spec sections, and are covered by hand-computed tests. The
defects are all at the seams where those components are assembled, fed, and
scheduled.

The sharpest illustration — two passing tests asserting contradictory contracts
for the same quantity, with nothing checking the interface between them:

- `tests/phase38/test_loss_catalog.py:193` —
  `test_soft_energy_uses_supplied_eps_h_not_recomputed`, whose comment reads
  `eps_h = 1e-4  # supplied metadata (= 1e-4 * S_H upstream); NOT recomputed`.
  The component correctly requires the spec value.
- `tests/phase40/test_optimizer_phase.py:744` —
  `test_default_energy_floor_factor_matches_pre_fix_scale`, docstring *"Shipped
  default 1e-4 must keep `eps_h == |h0|*1e-4 + 1e-12`."* The caller-side test
  **asserts the divergent formula as correct**, and its name indicates the scale
  was pinned deliberately.

Both were run individually and **both pass** (verified 2026-07-24 via the repo
venv). The component says "give me `1e-4·S_H`"; the assembly gives it something
else; a test ratifies the something else. No test compares the two. A suite in
this shape does not merely fail to catch the divergence — it defends it against
future correction.

---

## Findings

| # | Divergence | Layer | Severity | Status |
|---|---|---|---|---|
| C-01 | Causal exponent never clipped, against a normative MUST; weights underflow to exactly 0.0 | component call site / spec | **Critical** | Confirmed |
| C-02 | Causal front never advanced — physics supervision reached 1 of 16 collocation points for every step of every run | consequence of C-01 | **Critical** | Confirmed |
| C-03 | R̄ constructed as (1/9)Σ where §3.2 locks (1/3)Σ | assembly (`controllers.py:534`) | High | Confirmed |
| C-04 | ε_H supplied as `|h0|·1e-4 + 1e-12`, violating the component's own documented contract *and* the spec's pre-registered divergence criteria | assembly (`controllers.py:482`) | High | Confirmed |
| C-05 | λ_E = 1.0 at Stage 0 where the locked table sets 0 | configuration | High | Confirmed |
| C-06 | Per-term gradient statistics never logged, though the spec names them the precondition for any reweighting decision | instrumentation | Medium | Confirmed |
| C-07 | `L_data` component reduction under-specified in spec; implementation chose mean-over-9 | spec ambiguity | Medium | **Ambiguity — owner ruling needed** |
| C-08 | Test suite asserts divergent values (C-04) and asserts only the weaker ≤1 cap rather than the per-stage λ table (C-05) | test suite | High | Confirmed |

### C-01 / C-02 — The causal collapse

The spec is imperative in two places, and `pinn_architecture.md` §4.1 is the
more explicit of the two:

> Clip the causal exponent to avoid underflow, but do not choose a numeric
> clipping bound in Phase 19; **surface a gap if one is needed.** The causal
> exponent clip is required only to avoid underflow.

`ctl_instruction.md:1773` restates it: "The exponent **must be clipped** to avoid
underflow, but no numeric clipping bound is selected in Phase 35."

The implementation applies no clip — `weights = torch.exp(-eta * cumsum_excl)`
(`pinn/loss_catalog.py:258`), docstring conceding "the exponent is left
unclipped" (`:228-229`). The spec provided an escape hatch — *surface a gap if
one is needed* — and the pilot met its condition on step 1 of run 1. No gap was
surfaced.

Consequence, measured: `front_idx = 0` across **1500 of 1500 logged steps in 5 of
5 runs**, with `w_mean = 0.0625 = 1/16` exactly, `w_max = 1.0`, `w_min = 0.0`.
With `collocation_count=16` (`pinn/train.py:756`) and w₁ = exp(0) = 1
unconditionally, that is only consistent with w₁ = 1 and w₂…w₁₆ underflowed to
exactly zero. Physics was enforced at one instant, the earliest, and never
widened.

The 300-step budget makes this worse rather than better: the mechanism that
would eventually advance the front requires the leading residual to fall enough
for the cumulative sum to stop saturating the exponential, and 300 steps never
got there.

### C-03 — R̄ factor

Locked (`pinn_architecture.md:408`): `R̄_n = (1/3) Σ_{i=1..3} ‖f_i(u_n)‖²`.
Implemented (`pinn/training/controllers.py:534`):
`rbar = (residual ** 2).mean(dim=(-2, -1))` — a mean over 9 scalars, since
‖f_i‖² is itself a sum over 3 components. Implemented R̄ is exactly ⅓ of spec.

The consumer is correct: `(weights * rbar).mean()` (`loss_catalog.py:261`)
matches the locked `(1/N_t) Σ w_n R̄_n` (`:419`), and
`tests/phase38/test_loss_catalog.py:147` hand-verifies the exponential against
*supplied* R̄ values. The divergence is invisible to that test because the test
supplies R̄ rather than constructing it.

*Analysis, not established:* R̄ sits inside the causal exponent, so a 3×
under-estimate makes weights decay **more slowly** than specified. The
spec-correct factor would make C-02 more severe. C-03 therefore cannot be the
cause of the collapse, but it is wrong in the direction that partially masks it,
and it scales the whole physics term by ⅓.

### C-04 — ε_H, and the spec's pre-registered divergence criteria

`pinn/loss_catalog.py:269` `soft_energy_loss` is **correct** and states its
contract explicitly: ε_H is "the SUPPLIED metadata scalar equal to `1e-4 * S_H`
computed UPSTREAM — this term consumes it directly and does NOT recompute `S_H`
or re-apply the `1e-4` factor."

The caller supplies `abs(h0) * energy_floor_factor + 1e-12`
(`controllers.py:482`, factor 0.0001). The spec §3.4 does not merely specify the
right answer — it **enumerates in advance what counts as divergent**: an
implementation "is divergent if it omits `S_H` or `ε_H`, computes `S_H` from a
[wrong set], uses a fixed numeric `ε_H`, or applies a max/fallback floor," and
separately: "**Do not apply a fallback numeric floor.**"

The shipped assembly uses a per-anchor `|h0|`-derived stand-in in place of the
dataset-median `S_H = median_train(K0 + Uabs0)`, and adds a `+1e-12` floor. It
satisfies the spec's own definition of divergence on at least two counts. The
code comments concede the reason — "no `S_H` pipeline exists yet upstream"
(`controllers.py:35-36`) — which makes this a **build-order failure**: the spec
required a quantity whose producer was never built, and the assembly substituted
rather than blocking.

### C-05 — λ_E at Stage 0

`pinn/training/scheduled_weights.py` is spec-faithful: it transcribes the warmup
form `I_warm = min(2000, floor(0.1·N_Adam,k))`,
`λ(k,i) = λ^max(k)·min(1, i/I_warm)`, documents `λ_data = 1.0 (fixed,
pinn_architecture.md §3.1 unweighted data term)`, and its **defaults are the
Stage-0 values from the PHYS-05 table**. The run config overrode
`loss.lambda_e_max: 1.0` in all four configs, and the log confirms λ_E ramping
to 1.0 and holding through step 300. λ_L correctly stayed 0.

So: correct module, correct defaults, overridden by config, no gate to catch it.
This is precisely the case a preflight config-vs-locked-table check closes.

### C-06 — Gradient instrumentation

27 logged fields, one gradient-related (`grad_norm`, a single global pre-clip
norm, marked "⚖ PROVISIONAL (B-2)" at `pinn/training/step_log.py:151`). The
locked Phase-35 contract (`pinn_architecture.md:667`) conditions any reweighting
decision on "weighted losses, scheduled weights, and gradient statistics."
Weighted losses and scheduled weights are logged; per-term gradient statistics
are not. Any loss-reweighting remedy is therefore unreachable on the spec's own
terms, and not retroactively for runs already executed.

### C-07 — `L_data` reduction — AMBIGUITY, not a defect

Locked (`pinn_architecture.md` §3.1):
`L_data = (1/N_t) Σ_n Σ_i Huber_δr(r'_θ,i(u_n) − r'_i(u_n))`.

The Huber argument is a 3-vector and the spec specifies no reduction over spatial
components, so the expression is not scalar as written. Implemented:
`_huber(residual, 1.0).mean()` over the full `(N_t, 3, 3)` — i.e. `1/(9·N_t)`.
Read as a sum over components, the implementation is 1/9 of the spec; read as a
mean, it matches.

Because λ_data is pinned at 1.0 and all other terms carry weights, this is a
**relative weighting** question with real consequences for term balance. Per the
STOP protocol this is surfaced, not decided: the spec is silent on the component
reduction, and choosing one is a semantic call.

### C-08 — The test suite

Covered under "The central finding" above. Two specifics:
`tests/phase40/test_optimizer_phase.py:745` asserts the C-04 divergent formula
as the required behavior; `tests/phase40/test_scheduled_weights.py:81` asserts
the `λ_E^max ≤ 1` cap fails closed at 1.5 but **no test asserts the Stage-0 value
is 0**. The suite encodes the weaker constraint and leaves the stronger one
unguarded — the same lock-boundary confusion the trainex-r2 report raised as
RG-09, materialized in tests.

---

## Verified clean

Recorded so a future audit need not re-derive them, and because it localizes the
problem:

- `pinn/constants.py` — every value spec-cited with section references, single
  home, no scattered literals. `D = cbrt(100) ≈ 4.6416` (raw-mass convention;
  the rejected 6.694 form correctly absent), `T = 10`, `EPS_SOFT = 1e-5`,
  `EPS_L = 1e-8`, SIREN ω₀ 30.0/1.0, all three Huber δ = 1.0, `η_c = 1`,
  `w₁ = 1`. **This module is the pattern the rest of the codebase needed.**
- `softened_acceleration` (`physics_residual.py:193`) — Plummer squared-norm
  form `sqrt(‖Δ‖² + ε²)`, matching §3.2; the prohibited additive-on-the-norm
  anti-pattern is **not** present; correct `m_j (r_j − r_i)/r_safe³` direction
  and j≠i masking.
- `_matched_plummer_hamiltonian` (`loss_catalog.py:140`) — `H_ε = T' + V_ε`
  with `T' = ½Σ m_i‖v_i‖²`, `V_ε = −Σ_{i<j} m_i m_j/r_safe`, same ε_soft
  (matched, per §3.4).
- `ic_anchor_loss` — `(1/3)Σ_i‖·‖²` exactly, squared error not Huber, β_v = 1.
  Matches §3.3.
- `angular_momentum_loss` — `(1/(3N_t))ΣΣ Huber(·/L_scale)`,
  `L_scale = ‖L₀‖ + ε_L`. Matches §3.5.
- `_angular_momentum` — `Σ_i m_i(r_i × v_i)`.
- `project_com` — mass-weighted `R_COM = Σm_j r_j / Σm_j` on ordered **raw
  pre-tanh** masses, explicitly not recovered from tanh-normalized IC₁₃ slots.
  Matches D-02 / NET-02.
- `compose_total` — five-term weighted sum matching `ctl_instruction.md:1749`.
  The extra `lambda_data` factor is documented as fixed at 1.0 per §3.1, so it
  is a structural pass-through, **not** a divergence.
- `scheduled_weights` warmup form and per-stage defaults (see C-05 — the module
  is clean; the config overrode it).
- Term inventory is exactly five with no linear-momentum term, per §4.1's
  "No dedicated L_P term."

## Carried unresolved

- **Executed target frame** (trainex-r2 RG-02) — whether training targets are
  raw positions or `r'=r/D`. `data_huber_loss` documents that callers must
  convert, and its `_ = D_CHARACTERISTIC_LENGTH` line is explicitly a
  load-bearing-reference placeholder rather than a conversion. Settling this
  requires the corpus payload, which is absent from this worktree. The
  train-free residual-on-stored-targets check proposed in the trainex-r2 report
  would decide it; that is owner-authorization-gated.
- **Whether λ_E^max = 1.0 was authorized** (RG-01) and **where the PHYS-05 lock
  boundary sits** (RG-09) — both owner questions; the repository records values,
  never their authorization.

## Consequences

1. **The Stage-0 pilot was not a valid test of the design.** Physics supervision
   reached one collocation point out of sixteen for the entire run, under a
   conservation weight the locked schedule sets to zero, with an energy
   normalizer the spec explicitly pre-registered as divergent. Its uniform gate
   failure is not evidence about the architecture, the curriculum concept, or the
   loss design.
2. **The fix is narrow and localized.** All confirmed divergences sit in
   `controllers.py`'s assembly, one config key, one missing clip, and the
   logging registry. No component math needs rewriting.
3. **C-01 is not a pure code fix.** The spec mandates clipping and defers the
   bound; implementing it requires an owner decision on a value or a surfaced
   gap. It should not be filed as a routine bug.
4. **The test suite must be corrected alongside the code**, or C-04's test will
   fail the fix and C-05 will remain unguarded.

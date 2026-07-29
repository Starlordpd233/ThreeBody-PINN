---
status: active
purpose: review-findings
created: 2026-07-28
milestone: v2.2
phase: cross-cutting
retirement_trigger: Superseded when an independent reviewer returns verdicts on D-06a/D-06b and the owner rules on whether they are routed as new v2.2 requirements; the five carried-forward divergences retire when CONF-02..07 are implemented and verified.
---

# Conformance-Divergence Verification Handoff

**Purpose: an independent agent verifies six claims about the training path
before Phase 47 begins repair work. Five are carried forward from a prior
verification pass. One (D-06) is new, was found on 2026-07-28, is not owned by
any requirement, and — if confirmed — changes Phase 47/48 scope.**

The reviewer's job is to **try to refute each claim**, not to confirm it. Every
claim below is stated with the exact file:line and the exact command that
settles it. A refutation is a more valuable result than a confirmation.

---

## 0. How to run the checks

The repository python is **not** the system python:

```bash
cd <home>/Desktop/3_body_problem/.worktrees/trainex   # branch milestone/v2.2
PY=<home>/Desktop/3_body_problem/.venv/bin/python
PYTHONPATH="$PWD" $PY <script>
```

`python3` alone has no `torch` and will fail with `ModuleNotFoundError`.

**Standing constraints that bind the reviewer** (v2.2 scope boundaries):

| | |
|---|---|
| SCOPE-28 | Exactly **one** held-out evaluation for the whole milestone, gated on EVAL-01's three preconditions. Do not spend it. |
| SCOPE-29 | **No recipe tuning.** Iteration is conformance-only. |
| SCOPE-30 | **No framework-spec file edits.** Spec prose is not edited in v2.2. |
| STOP protocol | Do not invent content where sources are silent. Surface, do not absorb. |

Read-only inspection and throwaway scripts in a scratchpad are in bounds.
Training runs, evaluator invocation, and edits under `pinn/` are not.

---

## 1. Attestation levels — read this before trusting anything below

I am the agent that closed Phase 46. I did **not** personally verify claims
D-01..D-05 this session. Each claim below carries an explicit label:

| Label | Meaning |
|---|---|
| **[EXECUTED-2026-07-28]** | I ran code this session and read the output. Reproduction command given. |
| **[READ-2026-07-28]** | I read the cited source this session. Not executed. |
| **[CARRIED]** | Taken from the 2026-07-24 verification report. **I did not re-verify it.** Treat as a hypothesis with a citation, not as established fact. |

This distinction exists because of a documented failure mode in this project: a
`Complete` checkbox or a passing verification has twice meant "the plan ran,"
not "the claim is true." See
`docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
and the CONF-01/INST-01 false-Complete incident recorded in
`.planning/REQUIREMENTS.md:134`.

---

## 2. Part A — the five carried-forward divergences

Source: `2026-07-24-trainex-r2-report-factw-verification.md` (same folder tree,
`milestone_v2.1/45-.../`). That pass verified six claims against the shipped
code and retained run artifacts and refuted none. All five below are
**[CARRIED]**.

### D-01 → CONF-02 / CONF-03 — `S_H` pipeline was never built

| | |
|---|---|
| Locked | `ε_H = 1e-4 · S_H` where `S_H = median_train(K0 + Uabs0)` over the admitted set, persisted in training metadata (spec §3.4) |
| Implemented | per-anchor `\|h0\|·1e-4 + 1e-12` |
| Aggravator | §3.4 **explicitly prohibits** the `+1e-12` additive floor |
| Requirement | CONF-02 (build the pipeline), CONF-03 (wire it, remove the floor) — `.planning/REQUIREMENTS.md:36-37` |

**Check:** grep the `eps_h` construction in `pinn/training/controllers.py`
(near `h0 =` at `:468`) and confirm no `S_H` exists anywhere in `pinn/`.
`grep -rn "S_H\|s_h" pinn/` should return nothing structural.

**Note for the reviewer:** this one traces to the *spec* as much as the code —
the pipeline was never specified into existence. Code-vs-spec diffing alone
would not have caught it.

### D-02 → CONF-04 — `R̄` normalization off by exactly 3

| | |
|---|---|
| Locked | `R̄_n = (1/3) Σ_{i=1}^{3} ‖f_i(u_n)‖²` — `pinn_architecture.md:408` |
| Implemented | `rbar = (residual ** 2).mean(dim=(-2, -1))` — `pinn/training/controllers.py:534` |
| Why it is 1/3 of spec | `residual` is `(N_t, 3, 3)`; `.mean()` divides by **9**, but `‖f_i‖²` is already a sum over 3 components |

The downstream consumer is *correct*: `(weights * rbar).mean()`
(`pinn/loss_catalog.py:261`) matches locked `L_phys = (1/N_t) Σ w_n R̄_n`
(`pinn_architecture.md:419`). The defect is isolated to `:534`.

**Direction matters:** the implemented `R̄` is *smaller* than spec, so the
spec-correct factor makes the D-03 collapse **worse**, not better. `R̄` being
wrong cannot be the cause of the collapse — but it partially masks it.

### D-03 → CONF-05 — the causal front never advanced

| | |
|---|---|
| Symptom | `front_idx = 0` on **every** logged step of **every** retained run |

| run | steps | `front_idx` | `w_mean` | `w_max` |
|---|---|---|---|---|
| stage0-smoke | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-smoke-diag | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed41 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed42 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed43 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |

`w_mean = 0.0625 = 1/16` on every step is the signature of exactly one of
16 collocation weights being 1.0 and the other 15 being **exactly 0.0**. The
curriculum never curriculum'd.

**This is the claim most likely to be explained by D-06 below. See §4.**

### D-04 → CONF-05 — the mandated causal-exponent clip is absent

| | |
|---|---|
| Locked (normative MUST) | "The exponent **must be clipped** to avoid underflow, but no numeric clipping bound is selected in Phase 35; the bound remains deferred to FUT." — `ctl_instruction.md:1773` |
| Implemented | `weights = torch.exp(-eta * cumsum_excl)` — `pinn/loss_catalog.py:258`, no clip |
| Code concedes it | "The exponent is left unclipped except by the natural finite range of `exp`" — `pinn/loss_catalog.py:228-229` |

The *bound* is deferred to the implementer; the *clipping* is mandated. GAP-45-04
carries an owner ruling: invariant A (no causal weight may be exactly zero) is
mandatory, the number is the implementer's with a recording obligation.

### D-05 → CONF-06 — `λ_E^max` drifted off the locked Stage-0 value

| | |
|---|---|
| Locked | `λ_E^max(k) = {0 for k ∈ {0,1}; …}` — `pinn_architecture.md:663`. Stage 0 is k=0, so the locked value is **0** |
| Executed | `λ_E = 1.0` |
| Provenance | unrecoverable; GAP-45-02 owner ruling treats it as drift |

### Also carried, currently unowned by a CONF requirement

**RG-10 — per-term gradient statistics never logged.** The retained log carries
27 fields; exactly one is gradient-related (`grad_norm`, a single global
pre-clip norm marked "⚖ PROVISIONAL (B-2)" at `pinn/training/step_log.py:151-154`).
The locked Phase-35 contract (`pinn_architecture.md:667`) makes per-term
gradient statistics a **precondition** for any reweighting verdict. Reviewer:
confirm whether v2.2's INST-02/INST-03 cover this or whether it is a hole.

---

## 3. Part B — D-06, the new finding (NOT owned by any requirement)

**Claim: the executed training path evaluates the physics, IC-anchor, energy,
and angular-momentum losses in a frame in which they are structurally wrong.
The physics residual cannot reach zero on a perfect trajectory, and its minimum
is at zero gravity.**

This is the half of RG-02 that has never been routed. It has two independent
heads. Please verify them separately — **repairing 6a alone would leave 6b
broken while making the run look healthier.**

### 3.1 The locked design — why `D` exists at all

`pinn/constants.py:21` **[READ-2026-07-28]**:

```python
# D = (G T^2)^(1/3) ≈ 4.6416 with G = 1
D_CHARACTERISTIC_LENGTH = 100.0 ** (1.0 / 3.0)   # ≈ 4.6415888336...
T_CHARACTERISTIC_TIME  = 10.0                    # :31
```

`D = (G T²)^(1/3)` is the Kepler-scaling condition. It is chosen for exactly one
reason: so the equations of motion are **form-invariant** under
`r → r' = r/D`, `t → u = t/T`. In that frame and only in that frame,

```
d²r'/du² = a(r')
```

so a physics residual `d²r'/du² − a(r')` is **identically zero on a true
trajectory**. Numerically **[EXECUTED-2026-07-28]**:

```
T²/D  = 21.54434690031884
D²    = 21.544346900318832
T²/D − D² = 7.1e-15          (float64 zero)
D = 4.641588833612778 ;  T^(2/3) = 4.641588833612778
```

**The whole physics module documents itself as operating in the scaled frame**
— three independent statements in one file, all **[READ-2026-07-28]**:

| `pinn/physics_residual.py` | says |
|---|---|
| `:103` | `componentwise_du` returns "``dr'/du`` and ``d²r'/du²``" — **r prime** |
| `:197-199` | `softened_acceleration` takes "positions in the dimensionless system (``r' = r / D``)" with "the 3 ordered **RAW** masses" |
| `:240` | `physics_residual` is `f_i(u_n) = a'_i(u_n) − Σ_{j≠i} m_j (r'_j − r'_i) / r_safe³` — primed throughout |

Positions scaled, masses raw — which is exactly what v1.4's GAP-17-01 locks. The
module is internally consistent and unambiguous about its input contract.

### 3.2 What the code actually does

**[READ-2026-07-28]** — `pinn/training/controllers.py:521-533`:

```python
u_leaf = torch.as_tensor(anchor_ctx.collocation_times / T_CHARACTERISTIC_TIME, ...)  # :521-524
first, second = componentwise_du(anchor_ctx.traj, u_leaf)                            # :525
positions = ... anchor_ctx.traj(s) ...                                               # :526-527
accel  = second.reshape(-1, 3, 3)                                                    # :529
force  = softened_acceleration(positions, anchor_ctx.masses, ...)                    # :530
residual = accel - force                                                             # :533
```

Time **is** normalized (`u = t/T`). Positions are **not** scaled. The model's
positions are pinned to raw scale because the data term fits raw targets:

- `pinn/training/controllers.py:508-509` — `true_pos = data_points.targets…`, passed straight to `data_huber_loss`
- `pinn/training/controllers.py:223` — the Adam-path call site, same pattern
- `pinn/data/batches.py:265` — `sampled_targets.append(positions[index].reshape(9))`, resident positions verbatim
- `pinn/data/batches.py:16` — imports `T_CHARACTERISTIC_TIME`; **does not import `D_CHARACTERISTIC_LENGTH` at all**

And the data loss's own docstring states the contract the callers violate
(`pinn/loss_catalog.py:174-183`):

> §3.1 data Huber on COM-projected **scaled** positions `r' = r/D` … so
> **callers convert raw Brutus positions with `r' = r / D` before calling**

`pinn/loss_catalog.py:183` is `_ = D_CHARACTERISTIC_LENGTH` — a deliberate
no-op marker recording that the function itself does not scale.

**The residents are raw.** This is not inference: it is what CONF-01 measured on
the real 1,651-trajectory corpus on 2026-07-28. Raw-hypothesis residual median
`0.0802249` against controls at `0.0802262`; scaled-hypothesis median `0.9894`
with 1605/1651 separated — a factor of 12.3 (`46-VERDICT-POSTREPAIR.md`).

### 3.3 D-06a — position scale. Consequence, measured

**[EXECUTED-2026-07-28]** through the real production functions
(`componentwise_du`, `softened_acceleration`), on a trajectory constructed to
satisfy Newton's law **exactly** in native time:

```
=== RAW positions (what the code does) ===
  d²r/du² / a(r)  (elementwise mean ratio) = 100.0000000000
  Rbar = mean((d²r/du² − a)²)              = 1.548320e+02      <-- NON-ZERO
=== SCALED r' = r/D (the locked contract) ===
  d²r/du² / a(r)  (elementwise mean ratio) = 1.0000000014
  Rbar = mean((d²r/du² − a)²)              = 1.139882e-17      <-- float64 zero
```

The ratio is **exactly `T² = 100`**. So in the executed frame the residual on a
*perfect* trajectory is

```
residual = T²·a(r) − a(r) = (T² − 1)·a(r) = 99·a(r)
R̄ inflated by (T² − 1)² = 9801
```

**Two consequences, in increasing order of severity:**

1. `L_phys` has **no zero**. A perfectly trained network still carries `R̄ ≈ 9801·mean(a²)`.
2. Worse — `L_phys` is minimized where `a(r) = 0`. The physics term is an active
   gradient signal pushing the network toward **zero gravity**: bodies
   infinitely separated, or straight-line motion. It opposes the data term
   rather than regularizing it.

Reproduction script (self-contained, ~40 lines) at the end of this document.

### 3.4 D-06b — velocity scale. A *separate* defect

**[EXECUTED-2026-07-28]**: `‖dr/du‖ / ‖dr/dt‖ = 10.0000000000 = T`, **in both
frames**. Autograd necessarily returns `d/du`; the dataset stores `d/dt`.
Corroborating **[READ]**: `pinn/data/batches.py:185` computes
`np.gradient(velocities, times, …)` against **native `times`**, so the resident
velocity series is `dr/dt` end to end.

The three anchor targets are built from those raw native values and compared
against autograd `d/du` quantities:

| site | target built from | compared against |
|---|---|---|
| `controllers.py:466` | `true_v0 = velocities_gt[0]` = `v_raw` | `pred_v0 = dr/du` (`:514-515`) via `ic_anchor_loss` (`:516`) |
| `controllers.py:468-472` | `h0 = H(r_raw, v_raw)` | `soft_energy_loss(positions, dr/du, h0, …)` (`:547`) |
| `controllers.py:474-476` | `l0 = L(r_raw, v_raw)` | `angular_momentum_loss(positions, dr/du, l0, …)` (`:551`) |

**The energy term is the dangerous one.** In the executed frame
`K_model = T²·K_raw = 100·K_raw` while `U_model = U_raw`. Kinetic and potential
energy scale by **different** factors, so `H_model` is not a rescaled
Hamiltonian — it is unit-inconsistent, and **no single constant can absorb it**.
By contrast `L_angmom` and the velocity half of `L_IC` are off by a clean factor
of `T = 10`.

This also lands on CONF-02: `S_H = median(K0 + Uabs0)` built on an
unrepaired frame gives a correctly-computed statistic feeding a
unit-inconsistent comparison.

### 3.5 The repair I derived — **verify this, do not trust it**

Scaling the residents to `r' = r/D` fixes the velocity *derivative* for free,
because velocities come from autograd on positions, not from the dataset:
`dr'/du = (T/D)·v_raw`. What must change alongside is the three **targets**:

| quantity | conversion | numeric |
|---|---|---|
| resident positions | `r' = r/D` | ÷ 4.641588833612778 |
| `true_v0` | `v' = v·T/D = v/V` | × 2.154434690 |
| `h0` | `H' = H/V² = D·H` | × 4.641588834 |
| `l0` | `L' = L·T/D² = V·L` | × 0.464158883 |

where `V = D/T = 0.46415888336127786` is the locked characteristic velocity.
Sanity check on `h0`: under `r→r/D, v→v·T/D`, both `K ∝ v²` and `U ∝ 1/r` scale
by exactly `D`, so `H → D·H` uniformly — which is the property that makes the
scaled frame a proper similarity transform, and the property the current code
lacks.

**This prescription is my derivation, produced this session. It is the least
verified thing in this document.** It is offered so the reviewer has something
concrete to attack, not as a recommendation to implement.

---

## 4. The cross-claim that matters most

**Hypothesis (NOT verified — this is the single most valuable thing for the
reviewer to test): D-06a is the root cause of D-03, and CONF-05 as currently
written treats the symptom.**

The mechanism: causal weights are `w_n = exp(−η_c · Σ_{m<n} R̄_m)`
(`pinn/loss_catalog.py:258`). If `R̄` is inflated ~9801× by the frame error, the
exponent saturates on the first collocation point and every subsequent weight
underflows to exactly `0.0`. That is precisely the observed signature:
`front_idx = 0`, `w_max = 1.0`, `w_mean = 1/16`, on 1500/1500 steps across 5/5 runs.

**Why this matters practically.** CONF-05's remedy is a clip on the exponent.
Applied to an unrepaired frame, a clip produces a run whose causal front
advances and whose weights look healthy — while the physics term still has no
zero and still pulls toward zero gravity. **The run would look better and be
just as invalid.** If this hypothesis holds, the frame repair must precede or
accompany CONF-05, and CONF-05's clip bound must be chosen against a corrected
`R̄` in a corrected frame (note CONF-04 already changes `R̄` by 3×, so the bound
depends on both repairs).

**How to test it without a training run:** instrument `R̄` on stored targets in
both frames and compare `exp(−η_c · cumsum)` decay against the retained
`w_mean = 0.0625`. The corpus and the probe machinery already exist —
`pinn/verification/target_frame_probe.py` and the CONF-01 evidence run at
`.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/`.

A weaker but still useful cross-check: the v2.0 Stage-0 pilot failed its physics
gate by **~7 orders of magnitude**. `R̄` inflated by ~10⁴ plus a
unit-inconsistent energy term is a materially better explanation than
"the recipe is right but mistuned," which is the frame Phases 44 and 45 were
built on. **I have not measured this link. Do not repeat it as established.**

---

## 5. Why D-06 was not caught earlier — the routing hole

This is a gap in the requirement graph, not an oversight by any single pass.

1. The 2026-07-24 verification explicitly recorded RG-02 as **"Not verifiable
   here"**: *"the code path is confirmable but the data-level truth is not: the
   corpus payload is absent from this worktree"* (report `:196-201`). It
   verified the code half and could not verify the data half.
2. CONF-01 (Phase 46) settled the data half on 2026-07-28: the targets **are**
   raw.
3. **Nobody has since combined the two halves.** CONF-01's own branch-point text
   says *"if the target frame is wrong, that is a sixth divergence and a
   data-path defect rather than a loss-math one"* — and that branch fired, but
   it was spent entirely on the **permutation** defect, which the same probe
   surfaced simultaneously and which became CONF-08.
4. CONF-08's text deliberately excludes the scaling: *"The `D` scaling is
   **excluded** — it is the raw-vs-scaled question CONF-01 exists to answer, and
   pre-applying it would decide the verdict by construction"*
   (`.planning/REQUIREMENTS.md:42`). Correct at the time. But once CONF-01
   answered "raw," **no requirement was created to apply the deferred scaling.**

So the deferral was deliberate and correct; the follow-through was never routed.
Coverage is `23/23 mapped` with no orphans (`.planning/REQUIREMENTS.md:132`) —
which is exactly why a missing requirement is invisible to a coverage check.

---

## 6. How to refute D-06 — please try these first

A confirmation is worth less than a refutation. The strongest counter-arguments
I can construct against my own finding:

1. **"The model output is scaled somewhere I missed."** Find any transform
   between `self._model(...)` (`controllers.py:506`) and `softened_acceleration`
   (`:530`) that divides by `D`. I grepped every `D_CHARACTERISTIC_LENGTH`
   consumer outside `constants.py`/`verification/` and found three, none of
   which scale residents: `loss_catalog.py:183` (unused marker),
   `resume.py:345` (metadata only), `preprocessing.py:196` (builds `r_gauge`,
   which the adapter does not store as resident). **If a fourth exists, D-06a
   collapses.**
2. ~~**"`softened_acceleration` carries a compensating factor."**~~
   **CLOSED [READ-2026-07-28].** I read the full body,
   `pinn/physics_residual.py:193-232`. It is the bare Newtonian sum with `G = 1`
   implicit and Plummer softening on the squared norm — no `T²`, no `D³`, no
   scale factor of any kind. Its own docstring specifies the input as
   *"positions in the dimensionless system (`r' = r / D`)"* (`:197-198`), with
   *"the 3 ordered RAW masses"* (`:199`) — positions scaled, masses raw, exactly
   as v1.4's GAP-17-01 locks. This is a **third independent confirmation**, not a
   refutation: the module documents itself as operating in the scaled frame.
   `physics_residual`'s docstring at `:240` is primed throughout —
   `f_i(u_n) = a'_i(u_n) − Σ_{j≠i} m_j (r'_j − r'_i) / r_safe³`.
3. **"The COM projection head absorbs the scale."** It is mass-weighted and
   applied before any loss; check whether it normalizes magnitude.
4. **"Raw-frame training is intended and the spec is the stale artifact."**
   Then `constants.py:21`'s `D = (GT²)^(1/3)` derivation, `componentwise_du`'s
   `r'` docstring, and `loss_catalog.py:174-183`'s explicit caller contract are
   all wrong together — possible, but it makes the specs, not the code, the
   thing needing repair, which is a different (SCOPE-30-blocked) conversation.
5. **"GAP-46-06 already ratified raw."** It ratified `("r_raw", "t_native",
   "ordered_raw")` as the **validation-gate observation frame** — a coherent
   pair, raw positions with *native* time. The training path pairs raw positions
   with *normalized* time, which is not a coherent pair and is not what was
   ratified. Check `COHERENT_FRAME_PAIRS` in `pinn/training/validation_gate.py`:
   `(r_prime, u_t_over_T)` and `(r_raw, t_native)` are the only two admitted
   combinations, and the training path matches neither.

Point 5 is worth dwelling on: the codebase **already encodes** that
`(r_raw, u_t_over_T)` is an invalid frame pairing. The training path is in a
combination its own validation module declares incoherent.

---

## 7. What I did NOT do

- **No gap filed.** Under the STOP protocol this is a candidate
  cross-phase-reframing gap (it changes Phase 47/48 scope) and probably a new
  requirement, provisionally CONF-09. Filing awaits the reviewer's verdict and
  the owner's routing decision. I am not routing it myself.
- **No requirement added, no scope changed, no roadmap edited.**
- **No file under `pinn/` modified.** The only code I ran this session beyond
  the test suite is the throwaway script below, in a scratchpad.
- **No spec file touched** (SCOPE-30).
- **D-01..D-05 not re-verified.** Carried from 2026-07-24 with citations.

---

## 8. Reproduction script for §3.3 and §3.4

```python
"""Frame check via the REAL production functions.
Run:  PYTHONPATH=<worktree> <home>/Desktop/3_body_problem/.venv/bin/python this.py
"""
import torch
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.constants import D_CHARACTERISTIC_LENGTH as D, T_CHARACTERISTIC_TIME as T

torch.set_default_dtype(torch.float64)
dt, dev = torch.float64, torch.device("cpu")

masses = torch.tensor([0.4, 0.35, 0.25], dtype=dt)
r0 = torch.tensor([[1.0, 0.2, 0.0], [-0.8, 0.5, 0.1], [0.1, -0.9, -0.2]], dtype=dt)
v0 = torch.tensor([[0.1, 0.3, 0.0], [-0.2, 0.1, 0.05], [0.05, -0.4, 0.0]], dtype=dt)
a0 = softened_acceleration(r0, masses, dtype=dt, device=dev)  # true d2r/dt2 at t=0

def make_traj(scale):
    def traj(u):                       # exact Newtonian in NATIVE time t
        t = u * T
        return (r0 + v0 * t + 0.5 * a0 * t * t) / scale
    return traj

for name, scale in (("RAW (what the code does)", 1.0), ("SCALED r'=r/D (locked)", D)):
    traj = make_traj(scale)
    u = torch.zeros((), dtype=dt)
    first, second = componentwise_du(traj, u)
    accel, positions = second.reshape(3, 3), traj(u).reshape(3, 3)
    force = softened_acceleration(positions, masses, dtype=dt, device=dev)
    rbar = float(((accel - force) ** 2).mean())
    print(f"\n=== {name} ===")
    print(f"  d2r/du2 / a(r)           = {float((accel / force).mean()):.10f}")
    print(f"  Rbar (should be ~0)      = {rbar:.6e}  -> {'OK' if rbar < 1e-15 else 'NON-ZERO'}")
    print(f"  ||dr/du|| / ||dr/dt||    = {float(first.reshape(3,3).norm() / (v0/scale).norm()):.10f}")
```

Expected output is quoted verbatim in §3.3 and §3.4. If your run differs,
**that is the finding** — report it.

---

## 9. Evidence index

| What | Where |
|---|---|
| The five carried divergences, full derivations | `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md` |
| Original Stage-0 conformance audit | `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md` |
| CONF-01 post-repair verdict + arm numbers | `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT-POSTREPAIR.md` |
| CONF-01 raw evidence (`raw.json`, SHA-256 `11b6690a…a402654`) | `.planning/phases/46-.../evidence/target-frame/20260728T014532Z/` |
| Requirement text CONF-01..08, amendments | `.planning/REQUIREMENTS.md:35-42`, `:134`, `:136` |
| GAP-46-06 owner ratification + evidence addendum | `.planning/phases/46-.../46-GAPS.md`, section `## GAP-46-06` |
| Frame constants and coherent pairs | `pinn/training/validation_gate.py` (`COHERENT_FRAME_PAIRS`, `RATIFIED_VALIDATION_FRAME:528`) |
| Verification-enforcement charter (why this doc exists) | `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md` |

---

## 10. Requested output from the reviewer

For each of D-01 … D-05, D-06a, D-06b: **CONFIRMED / REFUTED / UNDECIDABLE-HERE**,
with the file:line or command output that settles it.

Then the three judgment calls:

1. Does D-06a cause D-03? (§4) — if yes, CONF-05's clip bound cannot be chosen
   before the frame repair.
2. Is D-06b independent of D-06a, and does the energy term's unit inconsistency
   invalidate CONF-02's `S_H` as currently specified?
3. Should D-06 be one requirement or two, and does it belong in Phase 47 (where
   `S_H` is built, and would otherwise be built in the wrong frame) or Phase 48?

**Routing is the owner's call, not the reviewer's and not mine.** The reviewer's
deliverable is verdicts and evidence.

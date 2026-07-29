---
status: active
purpose: verification-report
created: 2026-07-28
milestone: v2.2
phase: cross-cutting
retirement_trigger: Retires when GAP-46-07 is resolved by owner instruction and the resulting requirement (if any) is implemented and verified; the six confirmed divergences retire when CONF-02..07 are implemented and verified.
---

# Conformance-Divergence Verification Report

**Independent verification of the six claims in
`2026-07-28-conformance-divergence-verification-handoff.md`, performed before
Phase 47 begins. All six are CONFIRMED. One cross-claim the handoff flagged as
unmeasured is REFUTED as stated. One further defect, not examined by the
handoff, was found and is filed as GAP-46-07.**

The handoff asked the reviewer to *try to refute* each claim. That was done:
every refutation path it constructed against itself was walked, and each failed.

**Nothing under `pinn/` was modified.** All work was read-only inspection plus
throwaway scripts in a session scratchpad. No training run, no evaluator
invocation, no framework-spec edit, no requirement added, no roadmap or STATE
change. Routing remains the owner's call.

Environment for every command below:

```bash
cd <home>/Desktop/3_body_problem/.worktrees/trainex   # branch milestone/v2.2
PY=<home>/Desktop/3_body_problem/.venv/bin/python
PYTHONPATH="$PWD" $PY <script>
```

---

## 1. Verdicts

Requested output format was CONFIRMED / REFUTED / UNDECIDABLE-HERE per claim.

| Claim | Verdict | What settles it |
|---|---|---|
| D-01 — `S_H` pipeline never built | **CONFIRMED** | `grep -rn "S_H" pinn/` returns only docstrings, comments and a config description. `controllers.py:36` states it in prose: "no `S_H` pipeline exists yet upstream". Implemented value is `eps_h = abs(h0) * energy_floor_factor + 1e-12` (`controllers.py:482`) — the §3.4-prohibited additive floor is present. |
| D-02 — `R̄` off by exactly 3 | **CONFIRMED** | `controllers.py:534` is `rbar = (residual ** 2).mean(dim=(-2, -1))` on a `(N_t, 3, 3)` tensor, dividing by 9 where the locked form divides by 3. Downstream consumer `loss_catalog.py:261` `(weights * rbar).mean()` is correct, so the defect is isolated to `:534`. |
| D-03 — causal front never advanced | **CONFIRMED (independently re-measured)** | The handoff carried this from 2026-07-24 without re-verification. The retained artifacts are present in this worktree, so it was re-measured directly: **1500/1500 logged steps across 5/5 runs** carry `front_idx = 0`, `w_mean = 0.0625`, `w_max = 1.0`, `w_min = 0.0`. |
| D-04 — mandated causal-exponent clip absent | **CONFIRMED** | `loss_catalog.py:258` is `weights = torch.exp(-eta * cumsum_excl)` with no clip; the docstring at `:228-229` concedes it. |
| D-05 — `λ_E^max` drifted off the locked Stage-0 value | **CONFIRMED, and sharpened** | The logs show `lambda_e` is not a static `1.0`: it **ramps linearly `0 → 1.0` over the first 30 steps**, then holds `1.0` for the remaining 270. Locked Stage-0 (`k=0`) value is `0`. CONF-06 must therefore revert a *schedule*, not a constant. |
| D-06a — position scale | **CONFIRMED** | Reproduction reproduces the handoff's quoted output to all printed digits (§7.1). Independently corroborated three further ways (§2). |
| D-06b — velocity scale | **CONFIRMED** | `‖dr/du‖ / ‖dr/dt‖ = 10.0000000000 = T` in both frames; `batches.py:185` builds the resident series with `np.gradient(velocities, times)` against native `times`; the three anchor-target sites are exactly as cited. |
| RG-10 — per-term gradient statistics never logged | **CONFIRMED** | The step log carries 26 fields; exactly one is gradient-related (`grad_norm`, a single global pre-clip norm). Owned by INST-02, currently Pending at Phase 48 — so it is covered, not a hole. |

---

## 2. D-06a: every refutation path the handoff constructed against itself fails

The handoff listed five counter-arguments. Each was walked.

**(1) "The model output is scaled somewhere I missed."** Enumerated every
`D_CHARACTERISTIC_LENGTH` reference in `pinn/`. Outside `constants.py` and
`verification/` there are exactly three, exactly the three named:
`loss_catalog.py:183` (an unused `_ =` marker), `resume.py:345` (metadata),
`preprocessing.py:196` (builds `r_gauge`, which the adapter does not store as
resident). **No fourth consumer exists.** The refutation path is closed.

**(3) "The COM projection head absorbs the scale."** It is a mass-weighted
projection — a linear, scale-equivariant operation. It cannot absorb a uniform
scale factor, and it is rotation-equivariant, so it does not help the rotation
half either.

**(4) "Raw-frame training is intended; the spec is stale."** Would require
`constants.py:21`, `componentwise_du`'s `r'` docstring,
`softened_acceleration`'s stated input contract, and `loss_catalog.py:174-183`'s
explicit caller contract to be wrong together — and would make the specs the
repair target, a SCOPE-30-blocked conversation. Recorded as option D in
GAP-46-07 rather than dismissed.

**(5) "GAP-46-06 already ratified raw."** Confirmed as the handoff argued, from
source: `validation_gate.py:81-84` admits only `(r_prime, u_t_over_T)` and
`(r_raw, t_native)`. The training path is `(r_raw, u_t_over_T)` —
`controllers.py:522` normalizes time while residents stay raw. The codebase
already encodes that pairing as incoherent.

### Three corroborations the handoff did not have

**(a) The source annotates the defect.** `pinn/data/preprocessing.py:69`, on the
resident field itself:

> `r_com_ordered: Any  # (Nt, 3, 3) positions: COM/boost-gauged + canonically ordered.`
> `                    # NOT rotation-gauged, NOT scaled by D. CONF-08 resident surface.`

**(b) The repair is already anticipated in code.**
`pinn/training/validation_gate.py:526-528`:

> "Re-ratification is REQUIRED if Phase 47/48 moves residency to the locked
> canonical scaled contract (`r'` with `u = t/T`); this constant then goes
> stale."

**(c) D-06a was already measured, on 2026-07-28, in committed evidence — only
the inference was missing.** The probe's `scaled_hypothesis` arm *is* the
training path's frame: residents consumed as-is, differenced over `u = t/T`
(`target_frame_probe.py:487-492`). The probe's own module docstring
(`:26-32`) predicts that arm's value analytically:

> "a raw series read as scaled gives `a_fd = T^2 a` vs `a_newton = a`, i.e.
> `(T^2 - 1)/T^2 ~= 0.99`"

Measured over the 1,651-trajectory population
(`evidence/target-frame/20260728T014532Z/raw.json`):
**median 0.98936**, separated **1605/1651**. Three-significant-figure agreement
with the analytic prediction. Per trajectory, the same records carry
`stepwise_attribution.plus_scale = 1.26 ≠ 0`.

D-06a is therefore not a hypothesis awaiting verification. It is a re-reading of
evidence the project already holds and the owner already ratified.

---

## 3. The §4 cross-claim is REFUTED as stated

The handoff's §4 proposed that D-06a is the root cause of D-03 and explicitly
flagged it unmeasured ("I have not measured this link. Do not repeat it as
established."). It was measured.

**Arithmetic.** `loss_phys = (w · rbar).mean()`. With `w = [1, 0, …, 0]` over 16
collocation points — the observed signature — this is `R̄₀ / 16`. The retained
`loss_phys = 3.32e+08` at step 1 gives `R̄₀ = 5.32e+09`.

**Threshold.** `exp(−x)` underflows to exactly `0.0` in float64 at
`x > 745.133219`, and `η_c = 1.0` (`constants.py:71`). So `R̄₀` must fall by a
factor of **7.1e+06** before `w₂` becomes nonzero. The frame repair buys at most
`D² ≈ 21.5×`, and CONF-04 moves `R̄` `3×` the *other* way.

**Decisive.** At step 1 the model is at initialization. The target frame reaches
the causal weights only through gradients that have not yet been applied, and it
does not touch the model input (`IC₁₃` is built from `r0_gauge`, unaffected by a
target-side repair) or the collocation times. **`R̄₀` at step 1 is identical
under any target-frame repair.** The observed collapse cannot be caused by
D-06a. Its cause is D-04 — no clip — against an untrained network's `O(10⁹)`
residual.

**But the frame does block the front permanently.** On 25 real hierarchical
trajectories, a *perfect* trajectory in the executed frame yields
`R̄ = mean(((T²−1)·a(r))²)` with **median `8.36e+05`** (min `7.55e+04`, max
`4.31e+07`) — `1122×` above the underflow threshold, on **25/25**. In the locked
frame the residual is identically zero. So even a perfectly converged network
could never advance the front in the executed frame.

**Corrected statement, replacing §4.** Both repairs are necessary; neither is
sufficient. D-04's clip governs whether the front advances during training;
D-06a's frame governs whether `R̄ → 0` is reachable at all. The handoff's
practical warning is *strengthened* rather than weakened: since the clip alone
fully governs the observed behavior, applying it to an unrepaired frame will
reliably produce a run whose causal front advances and whose weights look
healthy, while `L_phys` still has no zero and still pulls toward zero gravity.
**The run would look better and be just as invalid.**

---

## 4. New finding: the rotation gauge (not examined by the handoff)

The handoff treated D-06 as two heads — position scale and velocity scale. There
is a third, and it is the most severe.

`stepwise_attribution.plus_rotation = 1.72 ≠ 0` in the same committed evidence
records: residents are un-rotated. But the **network input** is rotation-gauged.
`adapter.py:847-849` builds `IC₁₃` from `pre.r0_gauge` / `pre.v0_gauge`, which
are `R0 · r̄ / D` and `R0 · v̄ / V`.

`R0` is materially non-identity on real data: median `‖R0 − I‖_F = 2.83` over 30
hierarchical trajectories, **30/30** above `0.01`.

Because the gauge is *constructed from* the data, `IC₁₃` is exactly invariant
under a global rotation `Q` of the system, while the targets are equivariant.
Measured on a real trajectory with an arbitrary `Q` (§7.4):

```
max |IC13_a - IC13_b|     = 2.442e-15    <- NETWORK INPUT   (machine zero)
max |target_a - target_b| = 2.211e+00    <- REGRESSION TARGET
||target||_inf            = 1.132e+00    (target's own scale)
```

**The regression target is not a function of the network input.** Three
orientation degrees of freedom per trajectory are provably absent from the
14-dim input.

This is a different and worse failure mode than a scale error. A scale error
makes the loss minimum wrong. This makes the data term ask for something
structurally unlearnable — the best achievable fit is the conditional mean over
orientations — and no amount of training or tuning can recover it.

**Why it slipped.** CONF-08 admitted the rotation gauge only "if the re-probe
measures it as the new `first_diverging_step`". The post-repair
`first_diverging_step` is `com_recenter_boost`, because that discriminator
retained its pre-repair semantics and compares against the file-order array. The
trigger never fired — while `plus_rotation = 1.72` sits in the same record.

---

## 5. The three judgment calls

The handoff asked three questions and correctly reserved routing to the owner.

**1. Does D-06a cause D-03?** **No** — refuted, §3. But CONF-05's clip bound
still cannot be chosen before the frame repair, for the adjacent reason: the
bound must be selected against a corrected `R̄` (CONF-04, `3×` larger) in a
corrected frame, or it will be calibrated against a floor of `~8e+05` that
should be `0`.

**2. Is D-06b independent of D-06a, and does it invalidate CONF-02's `S_H`?**
The *defects* are independent (a scale error and a time-normalization error).
The *repair* is not: scaling residents to `r' = r/D` fixes the velocity
derivative for free, because velocities enter through autograd on positions
rather than from the dataset. `S_H = median(K0 + Uabs0)` built on the unrepaired
frame is a correctly-computed statistic feeding a unit-inconsistent comparison —
`K_model = T²·K_raw` while `U_model = U_raw`, so `H_model` is not a rescaled
Hamiltonian and no single constant absorbs it. **CONF-02 must be built after the
frame repair, or rebuilt.**

**3. One requirement or two, and Phase 47 or 48?** Recommended: **one
requirement, Phase 47, before CONF-02.** Rationale in §6. Options A–D are
recorded in GAP-46-07 for the owner's ruling.

---

## 6. Recommended repair (for the owner's decision, not applied)

Scale, velocity, and rotation are one defect — *residency stops short of the
locked contract* — with one repair. The pipeline **already computes the fully
conformant arrays** and stores the wrong ones: `pre.r_gauge` / `pre.v_gauge` are
consumed only by the probe (`target_frame_probe.py`), never by training.

Moving the resident surface at `adapter.py:864-865` from `pre.r_com_ordered` /
`pre.v_com_ordered` to `pre.r_gauge` / `pre.v_gauge` repairs all three at once,
and — critically — makes every derived anchor target self-consistent *without a
separate conversion table*, because they all derive from the residents:

| quantity | under the swap | why it becomes correct |
|---|---|---|
| collocation positions | `r' = R0 r̄ / D` | matches `softened_acceleration`'s stated input contract |
| `true_v0` | `v_gauge = R0 v̄ · T/D` | `dr'/du = (T/D)·v_rot = v_gauge` **exactly** — matches autograd `d/du` |
| `h0` | `H(r0_gauge, v0_gauge)` | both `K ∝ v²` and `U ∝ 1/r` scale by `D`, so `H → D·H` uniformly |
| `l0` | `L(r0_gauge, v0_gauge)` | scaled-frame angular momentum, consistent with `dr'/du` |
| `IC₁₃` | unchanged | already built in this frame — the rotation mismatch closes |

This is preferable to converting the three anchor targets individually (the
handoff's §3.5 table), which patches scale while leaving residents raw and does
not address rotation at all.

**Conditions.** Requires re-ratifying `RATIFIED_VALIDATION_FRAME` in the same
change — the constant's own comment mandates exactly this — and re-running the
CONF-01 probe if the owner wants a clean post-repair verdict token.

**Placement.** Phase 47 before CONF-02: `S_H` is frame-dependent, so building it
first means rebuilding it. This also aligns with RUN-03's existing obligation
that the evaluator pair canonical predicted `r'` with `u = t/T` — note
`pinn/evaluate.py` imports `T` but never `D`, so the evaluator already consumes
model output as `r'`, which the trainer does not produce.

**Not asserted.** That the frame error explains the v2.0 pilot's
~7-orders-of-magnitude physics-gate miss is a plausible candidate explanation
only. It has not been measured and must not be repeated as established.

---

## 7. Reproduction scripts

All four are self-contained. Run with
`PYTHONPATH="$PWD" $PY <script>` from the worktree root.

### 7.1 Frame check through the production functions

The handoff's §8 script, run verbatim. Output matched its quoted values to all
printed digits:

```
T^2/D = 21.54434690031884
D^2   = 21.544346900318832
T^2/D - D^2 = 7.105e-15
D = 4.641588833612778 ; T^(2/3) = 4.641588833612778

=== RAW (what the code does) ===
  d2r/du2 / a(r)           = 100.0000000000
  Rbar (should be ~0)      = 1.548320e+02  -> NON-ZERO
  ||dr/du|| / ||dr/dt||    = 10.0000000000

=== SCALED r'=r/D (locked) ===
  d2r/du2 / a(r)           = 1.0000000014
  Rbar (should be ~0)      = 1.139882e-17  -> OK
  ||dr/du|| / ||dr/dt||    = 10.0000000000
```

### 7.2 D-03 / D-05 re-measurement from the retained runs

```python
import json, collections
for r in ("stage0-smoke","stage0-smoke-diag","stage0-pilot-seed41",
          "stage0-pilot-seed42","stage0-pilot-seed43"):
    fi=collections.Counter(); wm=collections.Counter(); le=collections.Counter(); n=0
    for line in open(f"runs/{r}/logs/train.log.jsonl"):
        if not line.strip(): continue
        d=json.loads(line)
        if "front_idx" not in d and "w_mean" not in d: continue
        n+=1; fi[d.get("front_idx")]+=1; wm[round(d["w_mean"],6)]+=1
        le[d.get("lambda_e")]+=1
    print(r, "steps",n, "front_idx",dict(fi), "w_mean",dict(wm),
          "lambda_e_max",max(k for k in le if k is not None))
```

Result: `steps 300`, `front_idx {0: 300}`, `w_mean {0.0625: 300}` for all five
runs; `lambda_e` ramps `0 → 1.0` over 30 steps then holds `1.0` for 270.

### 7.3 Causal-collapse arithmetic and the asymptotic floor

```python
import math, numpy as np, torch, glob, os
from pinn.data.adapter import parse_brutus_file
from pinn.data.preprocessing import preprocess_trajectory
from pinn.physics_residual import softened_acceleration
from pinn.constants import T_CHARACTERISTIC_TIME as T
torch.set_default_dtype(torch.float64)
dt, dev = torch.float64, torch.device("cpu")

# Underflow threshold for eta_c = 1.
lo, hi = 0.0, 2000.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if math.exp(-mid) > 0.0 else (lo, mid)
print("exp(-x) == 0.0 for x >", hi)            # 745.133219
print("Rbar[0] at step 1 =", 16 * 332226624.0)  # 5.3156e+09

root = ("<home>/Desktop/3_body_problem/simulation_data/Data/"
        "brutus_output/brutus_hierarchical")
floors, ok = [], 0
for p in sorted(f for f in glob.glob(os.path.join(root, "*")) if os.path.isfile(f)):
    try:
        pb = parse_brutus_file(p)
        pre = preprocess_trajectory(pb.times, pb.positions, pb.velocities, pb.masses)
    except Exception:
        continue
    r = torch.as_tensor(np.asarray(pre.r_com_ordered), dtype=dt)
    m = torch.as_tensor(np.asarray(pre.masses_ordered), dtype=dt)
    a = softened_acceleration(r, m, dtype=dt, device=dev)
    floors.append(float((((T**2 - 1) * a) ** 2).mean()))   # perfect trajectory
    ok += 1
    if ok >= 25: break
f = np.array(floors)
print(f"floor median={np.median(f):.4e} min={f.min():.4e} max={f.max():.4e}")
print(f"fraction above threshold: {(f > hi).mean():.3f}")
```

Result: `median=8.3599e+05 min=7.5469e+04 max=4.3089e+07`, fraction above
threshold `1.000` (25/25), median/threshold `1122×`.

### 7.4 Rotation-gauge invariance mismatch

```python
import numpy as np, glob, os
from pinn.data.adapter import parse_brutus_file
from pinn.data.preprocessing import (preprocess_trajectory, compute_invariants,
                                     build_raw_ic13)

root = ("<home>/Desktop/3_body_problem/simulation_data/Data/"
        "brutus_output/brutus_hierarchical")
p = sorted(f for f in glob.glob(os.path.join(root, "*")) if os.path.isfile(f))[0]
pb = parse_brutus_file(p)

def ic13_and_target(pos, vel):
    pre = preprocess_trajectory(pb.times, pos, vel, pb.masses)
    inv = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
    return (build_raw_ic13(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, inv.E),
            pre.r_com_ordered)

rng = np.random.default_rng(0)
Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
if np.linalg.det(Q) < 0: Q[:, 0] *= -1

ic_a, tgt_a = ic13_and_target(pb.positions, pb.velocities)
ic_b, tgt_b = ic13_and_target(np.einsum("ij,tbj->tbi", Q, pb.positions),
                              np.einsum("ij,tbj->tbi", Q, pb.velocities))
print("max |dIC13|  =", np.max(np.abs(ic_a - ic_b)))    # 2.442e-15
print("max |dtarget|=", np.max(np.abs(tgt_a - tgt_b)))  # 2.211e+00
print("target scale =", np.max(np.abs(tgt_a)))          # 1.132e+00
```

The `‖R0 − I‖_F` census uses the same loader over 30 trajectories, reading
`pre.R0`.

---

## 8. Evidence index

| What | Where |
|---|---|
| The handoff under review | `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-handoff.md` |
| The five carried divergences, full derivations | `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md` |
| Original Stage-0 conformance audit | `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md` |
| CONF-01 post-repair verdict | `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT-POSTREPAIR.md` |
| CONF-01 raw evidence (`raw.json`, SHA-256 `11b6690a…a402654`) | `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/` |
| The gap this report files | `.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md`, `## GAP-46-07` |
| Milestone gap index | `.planning/milestones/v2.2-GAPS.md` |
| Frame constants and coherent pairs | `pinn/training/validation_gate.py:72-84`, `:515-537` |
| Retained run logs (D-03 / D-05 source) | `runs/stage0-{smoke,smoke-diag,pilot-seed41,pilot-seed42,pilot-seed43}/logs/train.log.jsonl` |

---

## 9. What this report does NOT do

- **No requirement added, no scope changed, no roadmap or STATE edit.** GAP-46-07
  is filed as `OPEN` and awaits owner routing.
- **No file under `pinn/` modified.** The recommended repair in §6 is a
  recommendation, not a change.
- **No spec file touched** (SCOPE-30).
- **No training run, no evaluator invocation** (SCOPE-27 / SCOPE-28 untouched;
  EVAL-01's three preconditions unchanged by this report).
- **No probe revision and no probe re-run.** Every probe number quoted is read
  from the existing committed `raw.json`.

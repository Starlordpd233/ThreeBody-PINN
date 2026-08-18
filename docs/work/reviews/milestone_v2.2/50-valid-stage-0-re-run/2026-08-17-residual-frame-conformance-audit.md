---
status: active
purpose: review-findings
created: 2026-08-17
milestone: v2.2
phase: 50-valid-stage-0-re-run
retirement_trigger: After the owner answers the 50-08 checkpoint and the causal-scale question is dispositioned (v2.3 recipe adjudication or an explicit owner ruling)
---

# Gate 1 — bounded residual-frame conformance audit

**Date:** 2026-08-17
**Scope:** read-only. Spec vs. code, plus already-committed Phase-38 probe evidence and the retained seed-41 step log.
**Question asked:** *does the implemented physics residual frame match the locked spec, given `T = 10`?*
**Verdict:** **NO MISMATCH.** The residual frame is conformant. The named hypothesis (a missing `u ↔ t` chain factor producing a `≈ 99·a_grav` floor) is **refuted** on four independent grounds.

**What changed:** nothing. No code, config, recipe, ledger, gap register, evidence directory, or framework spec was edited. This audit selects no 50-08 option, authorizes no generation, and does not reopen GAP-50-03. `later_generation_likelihood_claim: prohibited` is respected throughout — nothing below forecasts what any future run would do.

---

## 1. The hypothesis under test

Prior reading of `pinn/training/controllers.py:639-651` raised this:

```python
u_leaf = collocation_times / T_CHARACTERISTIC_TIME     # T = 10.0
first, second = componentwise_du(anchor_ctx.traj, u_leaf)   # returns d²r'/du²
force  = softened_acceleration(positions, masses, ...)      # gravitational accel
residual = accel - force
```

The concern: `d²r'/du² = T²·d²r'/dt² = 100·d²r'/dt²`, so on an exact trajectory the residual would evaluate to `99·a_grav` rather than zero — a nonzero floor of roughly the right order to explain `R̄₁ ≈ 10¹⁰`.

The concern conflates two frames. `force` is **not** `a_grav` in physical units; it is the *dimensionless* force computed from `r' = r/D`. Both sides of the subtraction live in the same scaled frame, and that frame closes exactly.

---

## 2. Ground 1 — the non-dimensionalization closes identically

Physical law:

$$\frac{d^2 r_i}{dt^2}=\sum_{j\neq i}\frac{G\,m_j\,(r_j-r_i)}{\lVert r_j-r_i\rVert^{3}}$$

Substituting `r' = r/D` and `u = t/T`:

- left side → `(D/T²)·d²r'/du²`
- right side → `(G M/D²)·Σ m'_j Δr'/‖Δr'‖³`

so

$$\frac{d^{2}r'}{du^{2}}=\frac{G\,M\,T^{2}}{D^{3}}\sum_{j\neq i}\frac{m_j\,\Delta r'}{\lVert\Delta r'\rVert^{3}}.$$

The dimensionless coefficient is exactly `1` **iff** `D³ = G·T²`. That identity is not an accident here — it is the locked convention, stated verbatim in `pinn/constants.py:20-31`:

> `ctl_instruction.md §2.5 / PIPE-09 (line 1024): raw-mass convention D = (G T²)^(1/3) ≈ 4.6416 with G = 1 … Numeric value is cbrt(T²) with T = 10 (PIPE-09 identity D³ = G T²).`

Numerically: `D = 100^(1/3) = 4.6415888…`, `D³ = 100`, `T² = 100`. Equivalently `T²/D = D² = 21.5443…` — the acceleration-scale factor on the AD side and the force-scale factor on the gravity side are the **same number**. The subtraction is frame-consistent and a physically exact trajectory yields residual `0`, not `99·a_grav`.

The v1.5-rejected mass-fraction value `D ≈ 6.694` would break the identity; it is explicitly banned from being selectable (`constants.py:22`).

## 3. Ground 2 — the spec says exactly what the code does

`pinn_architecture.md` §3.2 (lines 393-419):

- `u_n` : normalized physics time `t_n/T`
- `r'` : positions scaled by `D`
- **`a'` : accelerations scaled by `D/T²`**
- `m_j` : masses unchanged, `G = 1` in the dimensionless system
- `f_i(u_n) = a'_i(u_n) − Σ_{j≠i} F_ij`
- `R̄_n = (1/3) Σ_{i=1}^{3} ‖f_i(u_n)‖²`
- `w_1 = 1`, `w_n = exp(−η_c Σ_{m<n} stopgrad(R̄_m))`, `L_phys = (1/N_t) Σ_n w_n R̄_n`

`pinn_architecture.md` §5.3.1 (lines 894-907):

> Canonical autograd leaf `u = t/T`. `v' = dr'/du` and `a' = d²r'/du²`, **no chain-rule factor**. The factors 2 and 4 apply ONLY to a code path that differentiates directly with respect to a `τ = 2u − 1` leaf.

The implementation matches term for term:

| Spec object | Implementation | Verdict |
|---|---|---|
| `u = t/T` leaf | `controllers.py:639-642` | conformant |
| `a' = d²r'/du²`, no manual factor | `physics_residual.py:102-147` (`jacrev∘jacrev` on the `u` leaf) | conformant |
| `τ = 2u − 1` inside `forward` | `controllers.py:577` | conformant — autograd propagates the ×2/×4 itself |
| `r_safe = √(‖Δr'‖² + ε²)`, PHYS-03 squared-norm form | `physics_residual.py:221` | conformant |
| `f_i = a'_i − Σ_{j≠i} m_j Δr'/r_safe³` | `physics_residual.py:290` | conformant |
| `R̄_n = (1/3)Σ_i‖f_i‖²` | `controllers.py:656` | conformant (CONF-04/D-05) |
| `w_1=1`, prefix-exponential, `η_c=1`, `L=(1/N_t)Σ w_n R̄_n` | `loss_catalog.py:308-347` | conformant |
| `D`, `T`, `ε_soft`, `ω₀` literals | `constants.py:24,31,39,47-48` | conformant |
| SIREN init `U[±1/n_in]` first, `U[±√(6/n_in)/ω]` hidden | `network.py:81-84` vs spec §2.2 lines 174-186 | conformant |

## 4. Ground 3 — the training-residency frame is the same scaled frame

`pinn/data/preprocessing.py:196-220` produces `r_scaled = r_gauge/D` and `v_scaled = v_gauge/(D/T)`, i.e. exactly `r'` and `v' = dr'/du`. `pinn/data/adapter.py:884-885` stores `positions=pre.r_gauge, velocities=pre.v_gauge` as the resident training tensors, which `snapshot_positions` / `snapshot_velocities` return (`adapter.py:1057-1061`) and which `controllers.py:582-585` uses for the IC anchor. Model outputs, data targets, IC targets, and the force term all live in one frame.

This is not a new finding — it is the subject of two dedicated phases. Phase 46 success criterion 1 ("RG-02 is settled by a train-free stored-target residual check") is **✓ VERIFIED — QUALIFIED**, and Phase 47 moved residency onto `pre.r_gauge`/`pre.v_gauge` (CONF-09).

## 5. Ground 4 — committed probe evidence rules out a ×100 floor empirically

`.planning/milestones/v2.0-phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/residual/20260713T133400Z/summary.md`:

```text
Gate A: PASS (max relative error 1.4952905418063441e-15; threshold 1e-05)
Gate B: PASS (median relative error 0.006471392964707071; threshold 0.1)
Excluded snapshots: 0
GT mass-weighted COM offset: 1.4856572806563331e-12
Overall: PASS
```

Gate B (`pinn/verification/residual_probe.py:139-176`) takes a real Brutus trajectory, forms `r' = r/D`, finite-differences `v' = v_raw·(T/D)` on the `u = t/T` leaf, and subtracts the **same** `softened_acceleration` the training loop calls. On ground truth the residual is **0.65 % of the acceleration magnitude**. A missing `T²` factor would have produced a relative error of ≈ 99 — four orders of magnitude over the gate. Gate A confirms the force sum equals `−∇V_ε/m` to machine precision (`1.5e-15`). Gradcheck passed in float64/CPU.

**Conclusion of Gate 1: there is no residual-frame conformance defect, and none is available as a Phase-50 repair.**

---

## 6. Where `R̄₁ ≈ 10¹⁰` actually comes from

Closing the conformance question leaves the magnitude unexplained, so the audit continued far enough to say what the magnitude *is*.

### 6a. What the retained seed-41 log says

`w_min` is pinned at the float32 tiny clamp on 502/502 steps and `w_mean = 0.0625 = 1/16` exactly on 502/502 steps, so `w_2…w_16` are all at the clamp floor and `L_phys = R̄₁/16` to ~37 significant figures. Reading `R̄₁ = 16 · loss_phys` from `logs/train.log.jsonl`:

| Quantity | Value |
|---|---|
| `R̄₁`, all 502 steps | min 6.46×10⁸ · **median 2.53×10¹⁰** · max 3.93×10¹¹ |
| Bar to advance the front (`R̄₁ < ln 2`) | 0.693 → **10.56 decades below the median** |
| Point where `exp(−η_c R̄)` underflows float32 | `R̄ > 87.34` → **8.46 decades below the median** |
| `log₁₀ R̄₁` OLS trend over the 402 steps at `λ_phys = 1` | **−0.255 decades total** (within the step-to-step spread) |
| `front_idx` | 0 on 502/502 steps |
| `loss_data` | 0.0729 → 0.0203, descending |
| `loss_ic` | median 2.90×10⁴, never converges |
| `grad_norm_raw_phys` / `grad_norm_raw_data` (median) | **6.3×10¹²** (12.8 decades) |

The last row matters numerically: under round-to-nearest float32, adding `x` to `y` leaves `y` unchanged once `|x| < |y|·2⁻²⁴ ≈ |y|·6×10⁻⁸` — about **7 decades** of headroom. At 12.8 decades below the physics term, the data-term gradient is roughly 6 decades *past* that floor, so once `λ_phys` reaches 1 it contributes nothing to the accumulated gradient. (The IC term, at ~4.8 decades below, is inside the window and survives.)

`λ_phys` ramps 0 → 1 over steps 1-100 and equals 1.0 for steps 101-502, matching the §4.1 warmup `I_warm = min(2000, ⌊0.1·1000⌋) = 100`. Nothing anomalous there.

### 6b. Direct measurement: the scale is set at initialization, by the architecture

A read-only characterization of the **locked architecture alone** — `ArchitectureSpec()` defaults, built via `build_network`, evaluated at 16 sorted uniform `u ∈ [0,1]` with the locked residual functions, float64/CPU, **no data, no optimizer, no training step, nothing written to the repository**:

| seed / IC | ‖r′‖ | ‖v′‖ | ‖a′‖ = ‖d²r′/du²‖ | ‖F_grav‖ | min pairwise sep | `R̄` median | `front_idx` |
|---|---|---|---|---|---|---|---|
| 41, m=(1,1,1), IC13=0 | 1.28 | 310 | 2.03×10⁵ | 2.17 | 0.91 | 1.37×10¹⁰ | 0 |
| 42 | 1.13 | 331 | 2.72×10⁵ | 3.29 | 0.67 | 2.46×10¹⁰ | 0 |
| 43 | 0.97 | 251 | 2.20×10⁵ | 3.24 | 0.72 | 1.62×10¹⁰ | 0 |
| 0 | 0.91 | 281 | 2.79×10⁵ | 5.94 | 0.50 | 2.60×10¹⁰ | 0 |
| 7 | 0.85 | 290 | 1.94×10⁵ | 5.89 | 0.51 | 1.25×10¹⁰ | 0 |
| 41, m=(1,0.8,0.6), random tanh IC13 | 0.95 | 231 | 2.28×10⁵ | 2.85 | 0.72 | 1.74×10¹⁰ | 0 |

(All six rows are the probe's printed output; medians over the 16 collocation points.)

Three things follow directly:

1. **The gravitational term is correct and O(1).** `‖F_grav‖ ≈ 2–6`, which is what softened Newtonian gravity should give for three unit-ish masses about 0.5–0.9 apart in `r'` units. The minimum pairwise separation is 0.50–0.91, roughly five orders of magnitude above `ε_soft = 1e-5`, so **no near-singular close encounter is involved.** The `1/r³` term is not the amplifier.

2. **The residual is the network's own second derivative.** `‖a′‖/‖F_grav‖ ≈ 3×10⁴ – 9×10⁴`, so `residual = a′ − F ≈ a′` to four decimal places. Positions are O(1) and sensible; the first derivative is already 230–330 where it should be O(1); the second derivative is ~2×10⁵ where it should be O(1–10).

3. **`R̄ ≈ 10¹⁰` and `front_idx = 0` hold at step zero, before any training, for every seed and IC tried.** The seed-41 run's median `R̄₁ = 2.53×10¹⁰` is *the initialization value*. Over 502 steps the run moved `log₁₀ R̄₁` by −0.26 decades — it never left the regime it started in.

This reproduces the `[FACT-W]` observation already recorded from the v2.0 pilot (`front_idx = 0` on 1500/1500 steps in 5/5 runs, `R̄ ~ 10⁸–10¹⁰`) across a different code state, and now also with no data and no training at all.

### 6c. The mechanism, stated plainly

The physics residual is a **second-derivative operator**. A SIREN carries broadband high-frequency content by design (`first_omega_0 = 30`, ARCH-01, §2.2: "a high initial frequency injects a high-frequency Fourier basis"), and the 12-layer SQR-SkipResNet stack compounds it — the `LayerNorm(x)^p` skip branch with `p = 2` has Jacobian `2·LN(x)/std(x)` ≈ 3 per odd layer, six of them. The measured ratio `‖a′‖/‖v′‖ ≈ 650–900` is the network's effective angular frequency in `u`; differentiating twice multiplies amplitude by `ω² ≈ 10⁵–10⁶`.

The causal weight `exp(−η_c R̄)` with `η_c = 1` and an **unnormalized** `R̄` presumes `R̄ = O(1)`, which is what a *converged* network gives (Gate B: residual = 0.65 % of `‖a′‖` on a true trajectory). At initialization the same quantity is ~10¹⁰. So:

> At initialization the causal weighting mechanism is **saturated, not merely stuck**: `R̄₁` is 8.5 decades above the point where `exp(−η_c R̄)` underflows float32, so `w_2 … w_16` are all pinned at the same clamp floor. The vector carries no differential information, `front_idx` cannot report anything but 0, and the physics gradient reaches exactly **one** of the 16 collocation points — a different, randomly redrawn early time on every step (`controllers.py:602-603`, `1078-1081`).

Both halves of the locked spec are internally coherent; the mismatch is between them. §2.2 chooses an architecture whose second derivative starts at 10⁵; §3.2 chooses a curriculum tolerance calibrated for a residual of order 1.

### 6d. Two adjacent items, dispositioned rather than raised

- **`collocation_count = 16` is hard-coded** at `pinn/train.py:1033`, against `pinn_architecture.md` §3.2 Listing 3 (`n_col = 4096`, "recommended: 2048-4096"). This is **already an open `qualification` register entry** and is explicitly dispositioned by `50-CONTEXT.md:726-728` as a recipe surface (SCOPE-29), not a Phase-50 repair. Analytically it is also **not a candidate remedy**: `w_n` uses an unnormalized prefix *sum* of preceding `R̄`, so raising `N_t` makes the weight vector collapse harder, not softer.
- **The `L_IC` velocity term dominates `L_IC` by ~10⁵** (`loss_catalog.py:265-280` is a plain squared error on `dr'/du` at `u = 0`, and the measured `‖v′‖ ≈ 230–330` against a true `v'` of O(1)). This is the same first-derivative scale as 6b, not a separate defect. No frame error: `true_v0` is `pre.v_gauge`, already `v·T/D`.

---

## 7. What this does and does not license

**Establishes (grounded, D-19-legal — justified by spec text, locked constants, committed probe evidence, and a property of the locked architecture, not by what the run produced):**

- The residual frame is conformant. There is no conformance repair available for the causal-front halt.
- The `≈ 99·a_grav` hypothesis is refuted.
- The gravitational force term is correct, O(1), and not near-singular.
- The residual magnitude is set by the locked architecture's second derivative at initialization and is seed- and IC-independent across the cases tried.
- The causal weighting mechanism is saturated (not merely below the advance bar) at that magnitude.

**Does not establish, and must not be read as:**

- Any claim about what a later run — unchanged or changed — would do. `later_generation_likelihood_claim: prohibited` stands.
- Authorization for any recipe change. `η_c`, the causal formula, `N`, `ω₀`, `n_col`, and residual normalization are all recipe/spec surfaces; **SCOPE-29** bars tuning inside this phase and **SCOPE-30** bars framework-spec edits in v2.2 entirely.
- A reopening of GAP-50-03, or a selection of any 50-08 option.
- Anything that supersedes `grounded_causal_front_repair: none-in-current-sources`. This audit **confirms** that classification and supplies its reason.

## 8. Routing

`.planning/REQUIREMENTS.md` "Future Requirements" already names the vehicle:

> **v2.3 recipe adjudication** — if the conformant run still fails, that failure is the first real evidence about the design; recipe adjudication follows with the trainex-r2 resolution doc as a premise-qualified candidate verdict source (SCOPE-29/31).

That is precisely the situation. The conformant run failed, and the failure is now characterized. **SCOPE-31 forbids using the trainex-r2 report as a grounding source inside v2.2** — only its independently verified `[FACT-W]` findings are admissible here, and this audit cites only those. The remedy surface (`pinn_architecture.md` §3.2 causal-weight calibration and/or §2.2 derivative scale) is a framework-spec edit, which **SCOPE-30 forbids in v2.2**; Phase 52's VER-20 routing list carries four named items and this is not among them.

A **new** external research round (a "trainex-r3") is therefore **not** the cheapest correct next step: the mechanism is already researched and named, and the milestone plan already designates v2.3 with an existing candidate verdict source. What is missing is an owner disposition, not more literature.

---

## Sources consulted

| Source | Role |
|---|---|
| `pinn_architecture.md` §2.2, §3.2, §5.3.1 | Locked residual, causal weight, AD contract, SIREN init |
| `ctl_instruction.md` §2.5 / PIPE-09 (via `constants.py:20-31`) | `D³ = G T²` identity |
| `pinn/constants.py`, `physics_residual.py`, `loss_catalog.py`, `network.py`, `training/controllers.py`, `data/preprocessing.py`, `data/adapter.py`, `train.py` | Implementation |
| Phase 38 `evidence/residual/20260713T133400Z`, `evidence/gradcheck`, `evidence/overfit` | Committed dual-gate / gradcheck / overfit evidence |
| Phase 46 `46-VERIFICATION.md` | Frame settlement (RG-02, CONF-01/09) |
| `50-CONTEXT.md` (D-19, D-20, D-21, deferred list), `50-GAPS.md` GAP-50-03, `evidence/causal-front-diagnosis.md`, `50-08-SUMMARY.md` | Governance boundaries and the open checkpoint |
| `evidence/attempts/stage0-rerun-seed41-attempt-02/{config.yaml,logs/train.log.jsonl,failure/trip.json}` | Retained terminal record |
| `.planning/REQUIREMENTS.md` SCOPE-27..32, VER-20, Future Requirements | Routing |
| trainex-r2 research report | `[FACT-W]` findings only (SCOPE-31); cited for reproduction, not as grounding |

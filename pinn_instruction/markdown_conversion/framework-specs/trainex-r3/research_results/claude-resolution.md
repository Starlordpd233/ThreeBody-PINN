---
title: Trainex R3 Research Report — causal-weight / SIREN-scale recalibration (VER-20 item (e))
role: external research deliverable for the trainex-r3 round; informs checkpoint ② ratification, decides nothing
status: draft-for-owner-ratification
created: 2026-08-30
package_baseline: 6a4f9b9902ab62e1d1f57bba0e521f38120c416d
live_tree_seen: <home>/Desktop/3_body_problem/.worktrees/trainex (read-only, 2026-08-30; git metadata not reachable from the mount, so no HEAD hash is recorded — see G-10)
access_mode: open-book (Route B)
---

# Trainex R3 Research Report

**What this document is.** One research report answering `RESEARCH-CONTEXT-MASTER.md`
§5.1–§5.6 under the §5.7 form requirements and the §9 output contract. It carries
options menus, marked suggested defaults, door classifications, a composed first-run
recipe, a "what the runbook inherits" section, a fill-in decision sheet, a gaps
section, and a claims register.

**What this document is not.** It selects no remedy. Every default below is marked
*suggested* and is a candidate for the owner's ruling at checkpoint ②, not a ruling.
SCOPE-34 governs; SCOPE-38 means several of the candidates are formal contract
amendments, not value edits.

**Compliance with the read-only bars.** No file was edited. No training run was
started. No evaluation was invoked. No command with side effects was run; no commit
was made. No framework specification was edited. The repository was read only
(`cat`/`sed`/`grep`/`find` and one read-only JSON parse of an already-committed log).
The numerical work labelled `[OWN]` below was performed in a **clean-room numpy
re-implementation of the published spec text, in a separate sandbox**, importing no
project module, reading no project data, and training nothing; it is a check of an
analytic scaling law, **not** evidence about the project's tree, and it is subject to
the ERW Rule 19 in-repo verification obligation like any other claim. Discriminating
experiments appear only as owner-gated proposals.

**Evidence labels used throughout.**
`[PKG]` package-derived (the three attachments) · `[REPO]` repository-verified by me
in the live tree, with `file:line` · `[LIT]` published literature, cited by author /
title / venue / year · `[OWN]` my own analysis or clean-room computation.

---

## 1. Premise-challenge findings (first-class, ahead of the answers)

Nine findings. **PC-1, PC-3, PC-5, PC-6 and PC-7 change the answers.** PC-2, PC-4 and
PC-9 are corrections of record. PC-8 is a negative finding recorded because its
absence would otherwise be invisible.

---

### PC-1 — `F-02` is false as worded, and false in the direction that decides S3

**The claim.** `F-02` (status: *established*): "**`first_omega_0 = 30` sets the
second-derivative magnitude**: `‖a′‖` column values `1.94×10⁵`–`2.79×10⁵`, `R̄`
medians `1.25×10¹⁰`–`2.60×10¹⁰`" `[PKG` master §6 `F-02]`.

**The contradiction.** The master's own §4.1 `M2` and `F-11` already widened the
attribution to **two** factors, and amendment `A-1` records the narrow wording as a
*correction* — "The packet was narrower than its source, in a direction that
overstates one decision surface." But `F-02`'s **row text was never updated**. The
claims register — the table §3 tiers as *"established evidence a reader may rely
on"* — still carries the exact sentence `A-1` says was corrected, and `S3` in §4.3
still names `ω₀` alone as the initialization-scale surface. An agent that answers
§5.3 from `F-02` answers a false question.

**Independent derivation, done before comparison** `[OWN]`. `τ = 2u − 1` enters the
network only through the first layer's `sin(ω₀(W₀x + b₀))`
(`pinn/network.py:98`, `:171` `[REPO]`). For a *pure* SIREN that makes
`∂ᵏr′/∂τᵏ ∝ ω₀ᵏ` exactly at fixed weights, so `‖a′‖ ∝ ω₀²` and, since
`R̄ = (1/3)Σ‖f‖² ≈ ‖a′‖²/3` when `‖a′‖ ≫ ‖F‖`, `R̄ ∝ ω₀⁴`. **That law fails under the
locked architecture**, for a reason that is structural rather than numerical: layer 1
of the hidden stack is an odd SQR block, so the first operation applied to `h₁` is
`LayerNorm(h₁)²` (`pinn/network.py:122` `[REPO]`). LayerNorm is **positively
scale-invariant** — `LN(c·h) = LN(h)` — so the power branch's value *and every
derivative of it* are independent of the amplitude `ω₀` imparts. In the small-`ω₀`
limit `sin(ω₀z) → ω₀z` and the cancellation is exact; at `ω₀ = 30` it is partial,
leaving only a weak residual dependence.

**Clean-room measurement** `[OWN]`, medians over 16 sorted uniform `u ∈ [0,1]`, five
seeds, no training:

| `ω₀` | 30 | 10 | 3 | 1 | 0.3 | 0.1 | 0.03 |
|---|---|---|---|---|---|---|---|
| `R̄` median | 1.35×10¹⁰ | 3.58×10⁹ | 2.78×10⁹ | 3.21×10⁹ | 1.81×10⁹ | 8.20×10⁸ | 3.18×10⁸ |
| ratio to `ω₀ = 30` | 1 | 0.265 | 0.206 | 0.238 | 0.134 | 0.061 | 0.024 |

A **1000× reduction in `ω₀` buys 1.63 decades of `R̄`** — not the 12 decades `ω₀⁴`
would predict. Against the same clean-room model, removing the six power-skip blocks
at `ω₀ = 30` (depth 12 → 0) moves `R̄` by **8.66 decades** (1.35×10¹⁰ → 29.4, both five-seed medians), i.e.
**≈ 1.44 decades per SQR block**, with the first- and second-derivative gains per
block measuring ≈ 2.2 and ≈ 5.0 ≈ 2.2² — the signature of a per-block effective-
frequency multiplier of ≈ 2.2 raised to the derivative order.

**Corroboration of the probe itself** `[OWN]`. The same clean-room model, built only
from the verbatim spec text, reproduces the audit's six-row probe within its spread:
`‖r′‖` 0.76–0.99 (audit 0.85–1.28), `‖v′‖` 212–343 (audit 231–331), `‖a′‖`
1.6–2.9×10⁵ (audit 1.94–2.79×10⁵), `R̄` 0.9–2.9×10¹⁰ (audit 1.25–2.60×10¹⁰). `F-01`
is independently reproducible from the spec alone. Its **attribution** is what fails.

**Consequence for the decision.** `S3` as scoped has **≈ 1.6 decades** of capacity
against a **9.64-decade** (clamp, 15-term prefix; 8.46 on `F-03`'s single-residual
statement) / **10.56-decade** (front-advance) requirement. The
capacity the package attributes to "the SIREN initialization scale" lives in
`pinn_architecture.md` §2.3's power-skip stack (`:204-261`) `[REPO]`, which is **not** an
authorized surface under SCOPE-33 (`.planning/REQUIREMENTS.md:118`) `[REPO]` and is
recorded in master §7 only as an unsurfaced gap `[PKG]`.

---

### PC-2 — the round prompt's "four files named `pinn_architecture.md`" is stale

The prompt states four; master §3's table lists **five**, and amendment `A-11`
records the four → five correction explicitly. Verified `[REPO]`:

| path | lines |
|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | **1098 (live, authoritative)** |
| `.../framework-specs/integrity-r2/specs/pinn_architecture.md` | 1064 |
| `.../framework-specs/trainex-r1/specs/pinn_architecture.md` | 1013 |
| `.../framework-specs/integrity-r1/specs/pinn_architecture.md` | 1010 |
| `.../framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` | 1010 |

Low stakes — but it is a live premise in the instructions this round was given, and
the fifth path is the one `A-11` says the rule exists to prevent an agent from
silently reading.

---

### PC-3 — "underflow" is the **clip binding**, not IEEE underflow; and float64 is not a lever

`F-03` / `M3`: `exp(−η_c R̄)` underflows float32 at `R̄ > 87.34` `[PKG]`. Three
refinements, all verified:

1. `ln(smallest normal float32) = ln(1.175494×10⁻³⁸) = −87.33654` `[OWN]` — the
   audit's figure is exactly the **normal-range** boundary, not flush-to-zero.
   IEEE-754 flush-to-zero for float32 is at `−ln(1.401298×10⁻⁴⁵) = 103.279`.
2. The implementation never reaches either. `pinn/loss_catalog.py:97` sets
   `mathematical_floor = math.log(torch.finfo(dtype).tiny)` and `:339` computes
   `weights = torch.exp(torch.clamp_min(exponent, floor))` `[REPO]`. So the observed
   `w_min` is the **clamp**, and the retained log confirms it to the last digit:
   `w_min = 1.1754998158862984e-38` on **502/502 steps**, `w_max = 1.0`,
   `w_mean = 0.0625` exactly `[REPO`,
   `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl]`.
   `F-04` is verified independently from the primary log, not from the audit.
3. **float64 does not help.** Its floor is `ln(2.225074×10⁻³⁰⁸) = −708.396`; the
   clean-room weight vector at `η_c = 1` is still 15/16 floored under it `[OWN]`.
   The clip's entire dynamic range across the two precisions is `708.40/87.34 = 8.11×`
   in the exponent = **0.91 decades** in `R̄`.

**Consequence.** `S5` has 0.91 decades of capacity. It is a safety net, never a
remedy — and it is currently *masking* the failure, converting a would-be zero into a
silent floor.

---

### PC-4 — the source method **is** cited inside this repository, in `reference-code/`

`F-13` is literally true: `pinn_architecture.md`'s `## References` (heading at
`:1017`, entries `:1019-1035`) carries 17 entries — Power-Enhanced ResNet, PIG,
SIREN, DeepXDE, PINN repos — and **none** cites a source for §3.2's causal weighting
`[REPO]`. But master §7's cross-cutting entry ("the silence recorded here is this
package's, not the literature's") understates the position: the repository already
carries both the citation and a working reference implementation.

`reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py:55-60`
`[REPO]`:

> **Original reference**: Wang, Sifan, Shyam Sankaran, and Paris Perdikaris.
> *Respecting causality for training physics-informed neural networks.*
> Computer Methods in Applied Mechanics and Engineering 421 (2024): 116813.

That is the source method (§4 below). The gap is a **spec-citation gap**, not an
evidence gap, and it is a VER-20-class codification item alongside items (a)–(d).

---

### PC-5 — the 256× `η_c`↔`N_t` coupling is a consequence of a **departure** from the source, not a property of the method

`F-06`/`F-07` and SPEC-06 treat the exponent's dependence on the collocation count as
intrinsic: *"`w_n` uses an unnormalized prefix sum over collocation points, so raising
`N_t` makes the weight vector collapse harder"* `[PKG]`. Verified in the code — the
prefix sum is taken over the per-collocation-point residual vector
(`pinn/loss_catalog.py:330-333`, `:342`; `rbar` built one entry per collocation time
at `pinn/training/controllers.py:656`; 16 i.i.d. uniform draws re-taken every step at
`pinn/training/collocation_sampler.py:87` and `controllers.py:1307`, sorted at
`:607`) `[REPO]`.

**In the source method the prefix sum runs over `M` temporal segments, not over
collocation points.** Wang, Sankaran & Perdikaris (full citation in §2) define `L_r(t_i)` as the residual
**averaged over the `N_x` points at time level `t_i`** (Eq. 2.13) `[LIT]`; the
Expert's Guide states it as *"we partition the temporal domain into `M` equal
sequential segments and introduce `L_r^i` to denote the PDE residual loss within the
i-th segment"*, with `L_r(θ) = (1/M) Σ_i w_i L_r^i(θ)` `[LIT]`. The in-repo reference
implementation does exactly that: `_split_tensor_into_chunks` (`causal_pinn.py:187`),
one residual per chunk, `_compute_weights` over the chunk vector (`:208-219`) `[REPO]`.

**Consequence.** The collocation budget and the prefix-sum length are **separate
quantities in the source and conflated in this project**. The 256× arithmetic is real
but removable, and removing it dissolves most of what SPEC-06 has to adjudicate.

---

### PC-6 — the five surfaces do not cover the pathology that survives fixing all five

Verified independently from the retained log `[REPO`,
`.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl]`:
`median(grad_norm_raw_phys / grad_norm_raw_data) = 6.32×10¹²` — **12.80 decades**;
`λ_phys` ramps 0 → 1 over steps 1–100 and is 1.0 for steps 101–502; `loss_data`
descends 0.0706 → 0.0209; `loss_ic` median 2.897×10⁴.

Under round-to-nearest float32, an addend below `2⁻²⁴ = 5.96×10⁻⁸` of the running sum
is lost — **7.2 decades** of headroom `[OWN]`. At 12.8 decades below, the data term's
gradient contributes **nothing** to the accumulated gradient once `λ_phys = 1`. This
is the audit's own §6a observation, and it is **independent of the causal weights**:
it is driven by `L_phys ≈ R̄₁/16 ≈ 1.6×10⁹`, not by the weight vector's shape.

**Consequence.** A recipe that repairs the weight vector but leaves `L_phys` at ~10⁹
will **pass GATE-04 (i)–(iii) and still train on the physics term alone.** No surface
among S1–S5 *as the package scopes them* addresses this. It is the single strongest argument for locating the
normalization on `R̄` itself rather than only inside the exponent — see §3 (S2) and
the composed recipe.

---

### PC-7 — an *instantaneous* normalization converts the saturation halt into a permanent no-advance halt

The obvious reading of "normalize `R̄`" is to divide by the current batch's own
mean or median. That makes the weight vector **exactly scale-invariant**: verified
arithmetically, the weight vector under batch-mean normalization is bit-identical at
`R̄ ~ 10¹⁰`, `10²` and `10⁻⁴` `[OWN]`. `front_idx = max{n : w_n > 0.5}`
(`pinn/training/controllers.py:692-694`; documented at `pinn/training/tb_sink.py:15`)
`[REPO]` therefore becomes a **fixed statistic of the residual profile** that cannot
advance as training progresses, and invariant B trips on the **high-water mark** of
exactly that quantity (`pinn/training/guards.py:593-615`, `front_advance_window_n`;
`= 500` at `.../stage0-rerun-seed41-attempt-02/config.yaml` `run.invariants.front_advance_window_n`) `[REPO]`.

**Consequence.** The evidence supports a **frozen or lagging** reference scale rather
than an instantaneous one. This eliminates the most natural-looking option on the S2 menu and is
the reason the suggested default is a frozen reference rather than a running one.

---

### PC-8 — no bundle-fidelity, anchor, or transcription defect found (negative finding, recorded)

- All **10** `BEGIN VERBATIM` blocks in the framework-specs bundle have body length
  exactly (claimed range) + 2 wrapper blank lines — uniform across all ten `[OWN]`.
  Three boundary pairs (`127/203`, `383/493`, `262/281`) were compared line-for-line
  against the live file and match verbatim `[REPO]`.
- Every spec anchor the master cites resolves **by content** in the live 1098-line
  file: `:181` (the fixed-at-30 sentence), `:429` (`R̄` definition), `:435` (`w_n`),
  `:445` (Phase-35 LOSS-04 block), `:454` (`n_col=4096`), `:461` (range 2048–4096),
  `:668-671` (clip, underflow-only), `:692` (Phase-35 guard) `[REPO]`.
- The four stale anchors the master warns about are confirmed stale in
  `.planning/REQUIREMENTS.md`: `:424 → :445`, `:167 → :181`, `:433 → :454`,
  `:440 → :461` (`REQUIREMENTS.md:90`, `:95`) `[REPO]`.
- `F-05` verified: `front_idx = 0` on **502/502** logged steps, single-valued `[REPO]`.
- `F-08` (`pinn_architecture.md:445`), `F-09` (`:181`), `F-10` (`:668-671`, `:692`),
  `F-14` (`pinn/training/controllers.py:656`: `rbar = (residual ** 2).sum(dim=(-2,-1)) / 3.0`),
  `F-15` (`pinn/loss_catalog.py:339`, floor resolver `:77`, `:97`) all verified `[REPO]`.
- `M7`'s arithmetic (`R̄ ≈ ‖a′‖²/3`) re-derived: 1.374, 2.466, 1.613, 2.595, 1.254,
  1.733 (×10¹⁰) against the printed 1.37, 2.46, 1.62, 2.60, 1.25, 1.74 `[OWN]`. Agrees.
  Note the entailment the packet does not draw: `R̄ ∝ ‖a′‖²` means **`R̄` responds to
  the square of any derivative-scale change** — the reason the *pure-SIREN*
  law counts `S3`'s decades in `ω₀⁴` — a law PC-1 shows the locked stack breaks — and
  the reason the levers behave as they do in §3.

---

### PC-9 — `H-01` (trainex-r2 Q3 reading 1) is directionally right and quantitatively wrong `[r2-QUAL]`

Derived independently first, then compared, per §5.7(e). The r2 report estimates
*"a second-derivative residual through an ω₀ = 30 first-layer SIREN generically
produces `|a′|` of order `(2ω₀)² ≈ 3.6e3` per unit amplitude"* `[PKG` / r2 Q3 §(b)
reading 1 `]`.

- **Agree on form.** `‖a′‖ ∝ (dτ/du)²ω₀² = 4ω₀²` is the right functional statement for
  a bare SIREN first layer.
- **Disagree on magnitude and on attribution.** The locked first-layer bound is
  `U[±1/n_in]` with `n_in = 14` (`pinn/network.py:82` `[REPO]`) and the head is
  `U[±1/√256]` (`:139`), which together suppress `(2ω₀)²` by ~×3.5×10⁻³: the
  clean-room depth-0 network gives `‖a′‖ ≈ 12.7`, not 3.6×10³ `[OWN]`. The 12-layer
  stack then multiplies by ≈1.6×10⁴ to reach the measured 2×10⁵. The two errors
  nearly cancel, so r2's number lands within an order of magnitude **by
  coincidence**.
- **Disagree on the consequence, which is what matters.** Reading 1 predicts the gap
  "would shrink as fit improves" and, implicitly, that reducing `ω₀` reduces `R̄` as
  `ω₀²`. PC-1 refutes the second under the locked stack.

r2's readings 2 (frame inconsistency) and its `RG-04` (`1/9` vs `1/3`) are already
retired by the 2026-08-17 audit and by `F-14`/`F-15`; I confirm both retirements
`[REPO]`.

---

## 2. The source method, its own calibration procedure, and this project's departures (§5.7(c))

**The method.** Sifan Wang, Shyam Sankaran, Paris Perdikaris, *"Respecting causality
for training physics-informed neural networks"*, **Computer Methods in Applied
Mechanics and Engineering**, vol. 421, 2024, article 116813 (arXiv:2203.07404, 2022,
as *"Respecting causality is all you need for training physics-informed neural
networks"*) `[LIT]`. Practitioner restatement: Sifan Wang, Shyam Sankaran, Hanwen
Wang, Paris Perdikaris, *"An Expert's Guide to Training Physics-informed Neural
Networks"*, arXiv:2308.08468, 2023 `[LIT]`.

**The formula, in the source's own terms** `[LIT]`:

- Eq. 3.2: `w_i = exp(−ε Σ_{k=1}^{i-1} L_r(t_k, θ))` for `i = 2 … N_t`.
- Eq. 2.13: `L_r(t, θ) = (1/N_x) Σ_{j=1}^{N_x} |∂u_θ/∂t(t, x_j) + N[u_θ](t, x_j)|²`.
- Expert's Guide Eq. 2.11 restates it over **`M` equal sequential temporal segments**,
  `L_r(θ) = (1/M) Σ_{i=1}^{M} w_i L_r^i(θ)`.

This is `pinn_architecture.md:435` term for term, with `ε ↔ η_c` and `L_r ↔ R̄`.

**That method's own calibration procedure for the exponent coefficient, in the
source's own words** `[LIT]`:

- *"Choosing a very small ε can prevent the network from effectively minimizing the
  latter temporal residuals."* Conversely *"choosing a large ε value can result in a
  more difficult optimization problem, because the temporal residuals at earlier
  times have to decrease to a very small value."*
- *"In order to avoid tedious hyper-parameter tuning, we employ an **annealing
  strategy** for adjusting ε using an increasing sequence of values `{ε_i}`, which
  gradually increases the strength with which the PDE residual constraint is
  enforced."*
- The sequence is `{10⁻², 10⁻¹, 10⁰, 10¹, 10²}`.
- **The criterion by which the source decides ε is set correctly:** advance to the
  next `ε` when `min_i w_i > δ` with **`δ = 0.99`** (Algorithm 1). The Expert's Guide
  states the same target as a design goal: *"choose a moderately large ε to ensure
  that all temporal weights can properly converge to 1 at the end of training."*
- The Expert's Guide's Algorithm-1 default is **`ε = 1.0`**, and it flags the
  parameter as exhibiting sensitivity requiring tuning.
- **How the source treats the number of terms in the prefix sum:** it is `M` (or
  `N_t`), the number of **temporal segments**, decoupled from the collocation budget
  by the within-segment average. Reported values: `N_t = 100` (Allen–Cahn, against
  `N_r = 25600` collocation points), `32` (Kuramoto–Sivashinsky), `64` (Navier–
  Stokes), `256` per window (Lorenz, 40 windows). **The paper gives no rule for
  re-tuning `ε` when `N_t` changes** — a genuine silence in the source, recorded as
  `G-3` below.
- **The source's non-dimensionalization precondition.** The Expert's Guide makes
  non-dimensionalization a prerequisite of the whole recipe, on the ground that
  *"input variables should be in a moderate range, such as having a zero mean and
  unit variance"* and that scale disparities cause *"unbalanced contributions"*.
  `ε = 1.0` is a default **for residuals already brought to order one**.

**A third data point on `ε`, from the repository's own reference code** `[REPO]`: PINA
defaults to `eps = 100` (`causal_pinn.py:76`). So the three authorities disagree by
**four decades** (`ε` annealed 10⁻²–10², Expert's-Guide default 1, PINA default 100).
That disagreement is itself the finding: **`ε` is a calibrated quantity in every
source that states one, and no source treats it as a portable constant.**

**Where this project departs from the source.** Five departures and two fidelity checks, each verified:

| # | Source | This project | Consequence |
|---|---|---|---|
| **D-1** | Residual averaged **within `M` temporal segments**; prefix sum has `M` terms | One residual per **individual collocation point**; prefix sum has `n_col` terms (`loss_catalog.py:330-333`, `controllers.py:656`) | Creates the `η_c`↔`n_col` coupling SPEC-06 must adjudicate (PC-5); also makes each `R̄_m` a **1-sample** estimate whose noise propagates multiplicatively through the prefix sum |
| **D-2** | Segments are **fixed and equal**, spanning the domain | 16 i.i.d. uniform draws on `[0,T]`, **re-drawn every step**, then sorted (`collocation_sampler.py:87`, `controllers.py:607`, `:1307`) | The weight vector indexes a different time set each step, so `front_idx` is not a persistent state — yet invariant B is defined on its high-water mark (`guards.py:593-615`) |
| **D-3** | `ε` **annealed** over 4 decades with the `min_i w_i > 0.99` criterion | `η_c = 1` fixed for the whole run (`pinn_architecture.md:445`, `pinn/constants.py:71`) | The source's self-calibration is absent; the value is adopted, the procedure is not |
| **D-4** | `ε = 1` presumes a **non-dimensionalized, order-one** residual | `R̄ ≈ 2.5×10¹⁰` at initialization (`F-01`, `F-02`) | The precondition on which the default rests is violated by 10 decades |
| **D-5** | tanh MLP, Glorot init; Fourier-feature scale `σ ∈ [1,10]` chosen so *"the band width of NTK matches that of the target signals"* — an explicitly **tuned** quantity | SIREN `ω₀ = 30` (Sitzmann's image-fitting default) plus a 12-layer power-skip stack; `ω₀` **locked and unscheduled** (`:181`) | The source's analogue of `ω₀` is a calibrated knob; here it is a fixed contract, and (PC-1) it is not even the dominant contributor |
| **D-6** | `w_1 = 1` (sum runs `k = 1 … i−1`) | Same — exclusive prefix, `w_1` pinned (`loss_catalog.py:333`, `:340-341`) | **Faithful**, and *more* faithful than PINA, whose `_compute_weights` uses an inclusive `cumsum` (`causal_pinn.py:217`) |
| **D-7** | Weights are `stop_gradient` | Same (`detached = rbar.detach()`, `loss_catalog.py:329`) | **Faithful** |

**Reference for the SIREN half:** Vincent Sitzmann, Julien N. P. Martel, Alexander W.
Bergman, David B. Lindell, Gordon Wetzstein, *"Implicit Neural Representations with
Periodic Activation Functions"*, **NeurIPS 2020** `[LIT]` — the origin of `ω₀ = 30`
and of the `U[±1/n]` / `U[±√(6/n)/ω₀]` initialization the spec reproduces at `:181`
and in §2.4's table. Note the project sets `hidden_omega_0 = 1`
(`pinn/constants.py:48`, consumed at `pinn/network.py:84`) `[REPO]` where Sitzmann's
scheme carries `ω₀` in every hidden layer; that departure *reduces* derivative
amplification and is not the problem here.

For the mechanism-redesign family, the standing alternative in the literature is
Aditi S. Krishnapriyan, Amir Gholami, Shandian Zhe, Robert M. Kirby, Michael W.
Mahoney, *"Characterizing possible failure modes in physics-informed neural
networks"*, **NeurIPS 2021** `[LIT]` — sequence-to-sequence / time-marching curriculum
over explicit time windows, which is *architecturally* what the Phase-35 contract
calls "Option C time-windowed causal mechanics" and declares **not commissioned**
(`pinn_architecture.md:445`, `:692`) `[REPO]`.

---

## 3. Per-question answers with options menus

Each menu carries §5.7(a) **quantified capacity** (a derived scaling law plus the
magnitude the surface can produce, stated against the two fixed thresholds),
§5.7(b) **behaviour across the residual range**, and cross-decision interactions.

### The two thresholds, stated once

| Threshold | Value | Source |
|---|---|---|
| Clamp/underflow bound on the exponent | `η_c Σ_{m<n} R̄_m < 87.33654` (float32) / `708.396` (float64) | `[OWN]` derived; `[REPO]` `loss_catalog.py:97`, `:339`; matches `F-03` |
| Front-advance bound (`front_idx ≥ 1`) | `η_c R̄₁ < ln 2 = 0.693147` | `[REPO]` `controllers.py:692-694` (`w_n > 0.5`), `tb_sink.py:15` |
| Full-front advance (`front_idx = N_t−1`) | `η_c Σ_{m<N_t} R̄_m < ln 2` | same |
| GATE-04's three train-free conditions | (i) no weight at the clamp floor; (ii) weight vector carries differential information; (iii) `front_idx` **able** to advance | `[REPO]` `.planning/REQUIREMENTS.md:100` |

At the retained log's median `R̄₁ = 2.527×10¹⁰` and `N_t = 16` these require
`η_c < 2.30×10⁻¹⁰` (condition i), `η_c < 2.74×10⁻¹¹` (one front step), and
`η_c < 1.83×10⁻¹²` (full front) `[OWN]`.

### The range a Stage-0 run must traverse (§5.7(b), stated once)

`R̄₁` starts at median `2.527×10¹⁰` (retained log, `[REPO]`). ADVANCE criterion 3
requires validation `L_phys < ε_phys = 10⁻⁴` (`ctl_instruction.md` §Stage Transition
Criteria `[PKG]`; `stage.eps_phys: 0.0001` in `.../stage0-rerun-seed41-attempt-02/config.yaml` `[REPO]`). **That is 14.4
decades.** For orientation, the audit's converged-regime datum (Gate B: residual
= 0.65 % of `‖a′‖` on a true trajectory, `F-12`) corresponds to `R̄ ≈ 2×10⁻⁴` `[OWN]`,
consistent with the same target.

**The single most important derived quantity in this report.** For a fixed `η_c` and
`N_t`, the weight vector carries usable differential information only while
`η_c(N_t−1)R̄` sits between roughly 0.05 (below which every weight is ≈ 1 and the
mechanism is off) and 87.34 (above which it is floored). That is a window of fixed
width **87.34 / 0.05 ≈ 1747× = 3.24 decades in `R̄`, independent of both `η_c` and
`N_t`** — `η_c` and `N_t` translate the window, they do not widen it `[OWN]`.

> **A fixed `η_c` on an unnormalized `R̄` can serve at most 3.24 of the 14.4 decades a
> Stage-0 run must traverse.** This is a property of the exponential form, not of the
> locked value. It is why no single number on the S1 menu is a complete answer, and
> why the source anneals.

---

### 3.1 — S1 · `η_c`, the causal-weight exponent coefficient (§5.1)

**Quantified capacity.** `η_c` multiplies the exponent linearly and is unbounded
below, so its capacity is formally infinite: any threshold is reachable. Its
*useful* capacity is bounded by the 3.24-decade window above. Scaling law:
`exponent_n = η_c Σ_{m<n} R̄_m`, so `d(log₁₀ exponent)/d(log₁₀ η_c) = 1` exactly `[OWN]`.

**Behaviour across the range.** Verified arithmetically on the clean-room
initialization `R̄` vector and on the same vector rescaled to `10²` and `10⁻⁴` `[OWN]`:

| recipe | at `R̄~10¹⁰` | at `R̄~10²` | at `R̄~10⁻⁴` |
|---|---|---|---|
| `η_c = 1`, unnormalized (locked) | `w_min` = 1.18e-38, **15/16 floored**, `front_idx` 0 | 15/16 floored, `front_idx` 0 | `w_min` = 0.998, `front_idx` 15 — mechanism **off** |
| `η_c ≈ 2×10⁻¹²`, unnormalized *(rows evaluated on the clean-room vector, median `R̄` 1.34×10¹⁰; on the retained log's 2.53×10¹⁰ the same `η_c` gives `front_idx` 14)* | `w_min` = 0.525, `front_idx` 15, 0 floored | all weights ≡ 1 — mechanism **off** | all weights ≡ 1 — **off** |
| `η_c = 1` on `R̃ = R̄/R_ref` (frozen) | `w_min` 2.9×10⁻¹³ … 1.2×10⁻⁶ across 6 seeds, **0 floored**, 16 distinct | informative | weights → 1 (the source's intended end state) |

**Options.**

| | Option | Mechanical trade-off | Cross-decision interaction |
|---|---|---|---|
| **A1** | **Keep `η_c = 1` and change what it consumes** — the exponent takes a normalized `R̃` (S2 = B2/B3/B4) | No numeric change to the LOSS-04-ratified value; the source's own default becomes appropriate again because its precondition (order-one residual) is restored. Passes all three GATE-04 conditions across six clean-room seed/IC combos at `N_t = 16` `[OWN]` | **Requires** S2 ≠ B1. Binds S4: with `R̃ ≈ 1`, the clamp binds at prefix length `≈ 88`, so `M ≲ 87`, or `M ≲ 64` with a safety factor |
| **A2** | Set `η_c ≈ 2×10⁻¹²`, `R̄` unnormalized | One number. Passes GATE-04 at step 0. But its 3.24-decade window then sits at `R̄ ∈ [1.7×10⁹, 2.9×10¹²]`, leaving the mechanism inert for the remaining **11.2** of the 14.4 decades `[OWN]`. Also amends a locked value for no lasting benefit | Independent of S2; must be re-derived if S4 changes (`∝ 1/(N_t−1)`) and if S3 changes |
| **A3** | Keep `R̄` unnormalized and **anneal `η_c` by the source's Algorithm 1** (start ≈10⁻¹⁴; ×10 whenever `min_i w_i > 0.99`) | Most faithful to the source and self-calibrating; needs ~16 annealing stages to cross 14.4 decades where the source uses 5 across 4 `[OWN]` | Introduces a schedule into a locked contract; interacts with the PHYS-05 warmup and the stage-boundary re-warmup; does **not** fix PC-6 |
| **A4** | Replace the coefficient with a rank/quantile weighting (no `η_c`) | Fully scale-free; removes the parameter | Largest amendment; abandons the source method entirely; shares PC-7's no-advance hazard |

> **Suggested default: A1 — keep `η_c = 1`, conditional on adopting a normalization
> at S2.** Reason: it is the only option that leaves the owner-ratified LOSS-04
> *value* untouched while restoring the precondition under which that value is the
> source's own default; it is the only one whose informative window sits where the
> residual actually is at every point in the run; and it is the only one that
> composes with the S4 default without a second re-derivation.
>
> **Door: two-way.** Its failure mode (clamp binding, degenerate weight vector) is
> fully visible to the GATE-04 train-free probe before any run is spent. `η_c` is a
> single constant (`pinn/constants.py:71`) and re-ratification of LOSS-04 is a
> paperwork cost, not a run cost.
>
> **Deviations.** **A2 is one-way**: it passes GATE-04 and fails *during* training,
> where SCOPE-37 forbids retuning and SCOPE-35 protects the single evaluation.
> **A3 is two-way but expensive**: the annealing criterion is observable per step, so
> a mis-set start is caught early — but it adds a control law whose interaction with
> the PHYS-05 warmup is unmodelled here. **A4 is one-way**: it discards the source
> method, so a failure leaves no calibrated fallback and no literature to appeal to.

---

### 3.2 — S2 · the `R̄` normalization and its reference scale (§5.2)

**Does the evidence support introducing a normalization?** Yes, and the support is
structural rather than preferential: (i) the mechanism's informative window is 3.24
decades against a 14.4-decade traversal (§3, `[OWN]`); (ii) the source's `ε = 1`
default is explicitly conditioned on non-dimensionalized, order-one residuals
(`[LIT]`, Expert's Guide); (iii) PC-6 shows that leaving `R̄` at 10¹⁰ defeats the run
through float32 gradient accumulation regardless of the weights. No other surface
addresses (iii).

**Quantified capacity.** Unbounded and *exact*: dividing `R̄` by `R_ref` moves the
exponent by exactly `1/R_ref`, so the surface can place the residual anywhere in the
mechanism's window by construction. Scaling law: `d(log₁₀ exponent)/d(log₁₀ R_ref) = −1` `[OWN]`.

**A forced sub-decision the package does not surface: *where* the normalization is
applied.** Dividing only inside the exponent fixes the weight vector. Dividing `R̄`
itself — so that `L_phys` and its gradient are also rescaled — additionally collapses
the phys/data gradient ratio from **12.80 decades to 2.57 decades**, inside float32's
7.2-decade accumulation window `[OWN]`, and thereby addresses PC-6. Item (e)'s own
wording is *"an explicit normalization of `R̄`"*, which reads as the residual, not the
exponent. **This sub-decision is carried as its own row on the decision sheet (S2b).**

**Options.**

| | Option | Mechanical trade-off | Cross-decision interaction |
|---|---|---|---|
| **B1** | No normalization (status quo) | Zero amendment. Leaves the mechanism 10 decades outside its window and PC-6 unaddressed | Forces A2 or A3 at S1 |
| **B2** | **Frozen reference**: `R_ref` := median `R̄` measured by the **GATE-04 train-free probe** over ≥6 seed/IC combinations, recorded in the run record, held constant for Stage 0 | One recorded scalar. No control law, no per-step state, no feedback path, fully deterministic and auditable. Reuses machinery GATE-04 already mandates. `R̃` starts at ≈1 by construction **for any `ω₀`, depth, width or `p`** — which is precisely item (e)'s fourth family ("does not require the two to agree at initialization"). Clean-room: 0/16 weights floored on all six seeds (`w_min` 2.9×10⁻¹³ … 1.2×10⁻⁶), 16 distinct weights, `front_idx` 0–2 at init and free to advance `[OWN]` | Enables A1. Invalidated by any change to `ω₀`, depth, width, `p`, init bounds, `D`, `T`, `ε_soft`, or the IC13 normalization — the re-check trigger SPEC-06 asks for |
| **B3** | **Lagging EMA** of the batch residual | Adapts across stages; recovers "weights → 1 at convergence" automatically | Introduces an automatic reweighting control law — which the Phase-35 LOSS-02 contract **defers** *"until measured weighted-loss/gradient evidence exists"* (`pinn_architecture.md:445`, `:692`). That precondition is arguably now discharged by INST-02/03's per-term gradient logging, but the reading is the owner's |
| **B4** | **Relative residual**: `R̃_n = R̄_n / ((1/3)Σ_i(‖a′_i‖² + ‖F_i‖²) + δ)`, detached | Dimensionless and physically interpretable (unexplained fraction of the local acceleration scale) — the same statistic Gate B already reports as 0.65 %. Traverses ≈4.7 decades instead of 14.4, inside the source's own annealing range. Clean-room at batch level: 0 floored, `front_idx` 0–1 `[OWN]` | **Hazard:** a per-point denominator down-weights points where the network's own `‖a′‖` is large, creating a cross-step incentive to inflate `a′`. The batch-level scalar form avoids it; `‖a′‖` monitoring would be required |


**Recorded outside the menu — the instantaneous variant.** Normalizing by the *current* batch's own mean or median is the most natural-looking reading of "normalize `R̄`", and it is the one reading the evidence rules out: the weight vector becomes exactly scale-invariant, so `front_idx` cannot advance and invariant B trips for a new reason (PC-7). It is not offered as an option, and it carries **no door classification** because it is not a door — a recipe built on it fails during training, where SCOPE-37 allows no correction. It is written down only so that a reader who arrives at it independently finds it already considered.

> **Suggested default: B2 (frozen reference from the GATE-04 probe), applied to `R̄`
> itself (S2b = residual-wide).** Reasons: it is the only option with **no feedback
> path** and therefore no new control law to re-ratify against the Phase-35 LOSS-02
> deferral; its value is a single auditable number produced by a gate the milestone
> already requires; it makes the recipe independent of the initialization scale,
> which is the fourth remedy family's stated goal; and applied residual-wide it is
> the only option on any menu that touches PC-6.
>
> **Door: two-way on the mechanism, one-way on the semantics.** Two-way because the
> constant is recorded and re-measuring it costs a train-free probe, not a run.
> One-way in one specific respect: **every absolute threshold in the run contract is
> re-expressed by the same factor** (see "What the runbook inherits") — and a recipe
> that ships with `ε_phys`, `loss_explosion_ceiling` or the GATE-03 invariant bounds
> left in the old units will mis-gate *silently*, and silently is the failure mode
> SCOPE-37 gives no second chance to fix.
>
> **Deviations.** **B4 is two-way** and is the strongest alternative — prefer it if
> the owner wants a recipe that carries no frozen constant across stages; its extra
> risk is the `a′`-inflation incentive, which is monitorable. **B3 is one-way in
> governance terms**: it is an automatic reweighting control law, and adopting it
> before the owner rules that LOSS-02's deferral condition is discharged inverts a
> standing contract. **B1 is one-way**: it forces A2 or A3 and leaves PC-6 live.

---

### 3.3 — S3 · `ω₀` / `first_omega_0`, the SIREN initialization scale (§5.3)

**Does the evidence support changing it? No — and the reason is PC-1, not conservatism.**

**Quantified capacity, derived.** For a pure SIREN, `‖a′‖ ∝ ω₀²` and `R̄ ∝ ω₀⁴`
(derivation in PC-1). Under the locked architecture that law is broken by the
scale-invariance of `LayerNorm` on the power-skip branch, and the measured law is
`R̄ ∝ ω₀^≈0.5`: **1.63 decades for a 1000× reduction** `[OWN]`. Against the clamp threshold — **8.46 decades** on the audit's single-residual
statement (`F-03`), **9.64 decades** on the 15-term prefix sum the implementation
actually forms `[OWN]` — and the **10.56-decade** front-advance threshold, **S3 as
scoped cannot reach either.**

**A second, independent reason not to pull this lever.** At depth 0 (where the `ω₀⁴`
law does hold), reducing `ω₀` collapses the network's output amplitude, the three
predicted bodies converge, and the softened gravitational term takes over: clean-room
`R̄` at depth 0 (seed 41) *rises* from 39.1 (`ω₀ = 30`) to 5.8×10⁵ (`ω₀ = 0.3`) `[OWN]`. **`R̄` has
a floor set by `‖F_grav‖²` once the position scale collapses** — reducing the
initialization scale trades one divergence for another.

**Behaviour across the range.** `ω₀` is an initialization-time quantity and is not
scheduled (`:181`); it has no behaviour across the residual range beyond setting the
starting point. Under the B2 default the starting point is normalized away, so S3
becomes *irrelevant to the causal mechanism* — which is the point of the fourth
remedy family.

**Options.**

| | Option | Mechanical trade-off | Cross-decision interaction |
|---|---|---|---|
| **C1** | **Leave `first_omega_0 = 30` unchanged** | No §2.2 amendment, no SCOPE-38 re-ratification of the fixed-at-30 sentence, no disturbance to the spectral-bias rationale §2.1 rests on | Requires S2 ≠ B1 to be viable |
| **C2** | Reduce `ω₀` (e.g. to 3 or 1) | Spends a SCOPE-38 re-ratification for ≤ 0.7 decades `[OWN]`; risks the `‖F_grav‖` floor above | Would force re-derivation of `R_ref` (B2) and of `η_c` (A2/A3) |
| **C3** | Reduce the derivative scale at its actual source — §2.3's power-skip stack (depth, `p`, or the LayerNorm placement) | The only architectural lever with the required capacity: **1.44 decades per SQR block, 8.66 decades for all six** `[OWN]` | **Out of authorized scope.** SCOPE-33 authorizes VER-20 (a)–(e) plus `N_t`; §2.3 is not among them, and master §7 records the stack's absence from the surface list as an open gap |

> **Suggested default: C1 — leave `first_omega_0 = 30` unchanged.**
> Reason: measured capacity 1.63 decades against a 9.6–10.6 decade requirement, plus
> the `‖F_grav‖` floor; and under B2 the initialization scale no longer needs to agree
> with anything.
>
> **Door: two-way** (and the cheapest kind — it is the *absence* of an amendment).
>
> **Deviations.** **C2 is two-way mechanically** (GATE-04 sees its effect at step 0)
> **but one-way in governance**: it consumes a SCOPE-38 re-ratification of an
> owner-ratified sentence for a capacity the evidence says is insufficient, and a
> later reversal is a second amendment. **C3 is one-way** — it is a scope widening, and
> it is not a deviation the owner can take on this ruling at all: SCOPE-33 would have
> to be widened first. It is raised here because
> PC-1 makes it the honest location of the capacity, and because an owner ruling that
> ω₀ "stands" should be recorded as *"the authorized architectural surface is the
> wrong one"* rather than *"the architecture is fine"*.

---

### 3.4 — S4 · `N_t` / `n_col`, the collocation-point count (§5.4)

**Stated jointly with S1, as SPEC-06 requires.**

**Quantified capacity, derived.** The exponent at the last point is
`η_c Σ_{m<N_t} R̄_m ≈ η_c (N_t − 1) R̄`, so `d(log₁₀ exponent)/d(log₁₀ N_t) = +1` for
large `N_t` `[OWN]`. Moving from 16 to 4096 multiplies the exponent by
`4095/15 = 273` — **+2.44 decades in the wrong direction**. `N_t` is therefore not a
remedy; it is a constraint that any `η_c` choice must satisfy. Clean-room: under the
B2 normalization at `η_c = 1`, `n_col = 4096` with the prefix sum over all 4096 points
floors **4066 of 4096** weights; binned to `M ≤ 64` it floors none `[OWN]`.

**The joint bound.** With `R̃ ≈ 1` per prefix term, the clamp binds at prefix length
`≈ 87.34/η_c`. At `η_c = 1` that is **`M ≲ 87`**; the corresponding front-advance
bound is `M ≲ 1 + ln2/η_c ≈ 1.7`, i.e. at initialization the front correctly sits at
the start of the domain and advances as `R̃` falls — which is the intended behaviour,
not a failure.

**The structural finding (PC-5).** The source decouples the two quantities. Adopting
its structure lets the spec's `n_col = 4096` and a small prefix length coexist, and
it fixes two further problems the package does not raise: each `R̄_m` becomes a
256-point mean instead of a 1-sample estimate (the prefix sum currently propagates
single-point noise multiplicatively into every later weight), and fixed bin edges make
the weight vector — and therefore `front_idx` and invariant B's high-water mark —
comparable across steps, which D-2 currently prevents.

**Options.**

| | Option | Mechanical trade-off | Cross-decision interaction |
|---|---|---|---|
| **D1** | Keep `n_col = 16`; amend `:454`/`:461` to match the code | Smallest change; retires the spec/code divergence by moving the spec | Abandons the spec's stated 2048–4096 range with no evidence for 16; leaves 1-sample `R̄_m` noise and D-2 |
| **D2** | Honor `n_col = 4096` with the prefix sum over all points | Honors the spec value literally | **Floors 4066/4096 weights even under B2** `[OWN]` — mean `R̃ = 1.016` over the 4096 points, but the early-`u` points run above the mean, so the prefix crosses 87.34 at index 29. Forces `η_c ≈ 2.1×10⁻²` (clamp at the last point) or `1.7×10⁻⁴` (full front) `[OWN]`; re-creates the coupling |
| **D3** | **Decouple**: `n_col = 4096` collocation points aggregated into `M` fixed equal time bins in `u`; prefix sum over `M`. Suggested `M = 16` | Restores the source's own structure (PC-5); honors both spec numbers; 256 points per bin cuts `R̄_m` variance by 256×; fixed edges make `front_idx` a persistent state | Requires an implementation change (binning), not just a value edit. Composes with A1 at `η_c = 1` with ~5.8× clamp margin |
| **D4** | As D3 with `n_col = 2048`, `M = 32` | Closer to the source's practice (`M` = 32–256); halves the forward-pass cost of D3 | At `η_c = 1`, `M = 32` gives `w_min ≈ 1.5×10⁻¹⁴` `[OWN]` — off the floor but a steeper profile |

> **Suggested default: D3 with `n_col = 4096`, `M = 16`.**
> Reasons: it honors the spec's own `n_col` without amending `:454`/`:461`; it is the
> source method's structure rather than an invention; `M = 16` preserves the prefix
> length the current implementation and the retained log were characterized at, so
> `F-04`/`F-05` remain the right comparators; and it leaves ~5.8× clamp margin at
> `η_c = 1` under B2.
>
> **Door: two-way.** The full effect is visible to the GATE-04 train-free probe, and
> `M` is a recorded integer. The *implementation* of binning is new code, so the door
> is two-way in the contract and one-way in engineering time.
>
> **Deviations.** **D1 is two-way** and cheap, but records 16 as a locked value with
> no evidence behind it and leaves the noise and comparability problems. **D2 is
> one-way**: it forces a second re-derivation of `η_c` and re-introduces exactly the
> coupling SPEC-06 exists to dispose of. **D4 is two-way**, and is the right pick if
> the owner prefers the source's own `M` range over continuity with the retained log.

---

### 3.5 — S5 · the causal-exponent clip's declared semantics (§5.5)

**Does the evidence support a numeric bound? No.** The dtype-derived floor is already
the mathematically correct one, and no tighter bound adds capacity.

**Quantified capacity, derived.** The clip's whole range across the two available
precisions is `708.396/87.337 = 8.11×` in the exponent = **0.91 decades in `R̄`**
`[OWN]`; a *tighter* numeric bound has negative capacity. Verified: at the float64
floor, the locked recipe still floors 15/16 weights `[OWN]`.

**Behaviour across the range.** Under the composed recipe the clip should **never
bind**, at any point in the run. That converts it from a silent floor into a usable
alarm: today, clip binding is indistinguishable from a legitimately tiny weight
except through `w_min`, and it is precisely what let a saturated mechanism run for
502 steps.

**Options.**

| | Option | Mechanical trade-off | Cross-decision interaction |
|---|---|---|---|
| **E1** | **Keep the underflow-only purpose and the dtype-derived floor**, and make binding **observable**: log a per-step clip-binding count and make binding at step 0 a GATE-04 (i) failure | No amendment to `:668-671`'s stated purpose; the FUT-deferred numeric bound stays deferred, correctly, because none is needed. Adds one integer to the step record | Consistent with GATE-04 (i) as already written (`REQUIREMENTS.md:100`) |
| **E2** | Choose a numeric bound tighter than the dtype floor (e.g. exponent ≥ −30) | Makes floored weights less extreme | Negative capacity; would need its own SCOPE-38 re-ratification; masks the alarm E1 creates |
| **E3** | Remove the clip and rely on the normalization | One fewer moving part | Removes the only guard against a genuine numerical excursion; contradicts `:668-671` |

> **Suggested default: E1 — semantics unchanged, binding made observable.**
> Reason: the clip is not a remedy surface and does not need to become one; the
> cheap, high-value change is to stop it from hiding the condition it guards against.
>
> **Door: two-way**, and the lowest-risk item on any menu — it changes no value and
> adds instrumentation.
>
> **Deviations.** **E2 is two-way mechanically but one-way in evidence terms**: it
> would make the v2.2 failure signature *less* visible in any future log. **E3 is
> one-way**: it removes a guard on the basis of a normalization that has not yet been
> run.

---

### 3.6 — S6 · the couplings, and the composed first-run recipe (§5.6)

#### Cross-menu coherence check

| Pair | Interaction | Coherent under the defaults? |
|---|---|---|
| S1 × S2 | `η_c = 1` is the source's default **only** for an order-one residual | ✓ B2 restores that precondition; A1 then requires no value amendment |
| S1 × S4 | Clamp binds at prefix length `≈ 87.34/η_c` | ✓ `η_c = 1`, `M = 16` → max exponent 15, ~5.8× margin; verified 0/16 floored on six seeds `[OWN]` |
| S2 × S3 | `R̃ ≈ 1` by construction for any initialization scale | ✓ this is why C1 costs nothing; it is also item (e)'s fourth family, achieved without touching the architecture |
| S2 × S5 | The clip should never bind under B2 | ✓ makes E1's alarm meaningful |
| S2 × PC-6 | Residual-wide normalization rescales `L_phys`'s gradient by `1/R_ref` | ✓ phys/data ratio 12.80 → 2.57 decades, inside float32's 7.2-decade window `[OWN]` |
| S2 × invariant B | A *frozen* reference lets `front_idx` advance as `R̄` falls | ✓ — but only because B2 is frozen; the instantaneous variant recorded outside the S2 menu would break it (PC-7) |
| S2 × PHYS-05 | Dividing `R̄` by a constant is **observationally equivalent** to `λ_phys = 5.9×10⁻¹¹`, and `λ_phys^max = 1` is **[LOCKED]** (`pinn_architecture.md:683`, Phase-53 block at `:688`) | ⚠ **Coherence warning.** The amendment must land as a §3.2 *residual-definition* change with the PHYS-05 table left literally intact, and must say so, or an auditor can read it as an override of a locked table |
| S4 × LOSS-04 | Fixed time bins could be read as re-commissioning "Option C time-windowed causal mechanics", which `:445` and `:692` declare **not commissioned** | ⚠ **Coherence warning.** Binning is the source's *residual aggregation*, not Option C's windowed *optimization*. The amendment must draw that distinction explicitly |
| S2 × ADVANCE gate | Every absolute threshold shifts by `1/R_ref` | ⚠ **Highest-risk inheritance.** See the runbook section |

#### The composed first-run recipe (suggested defaults, assembled)

```
S3  first_omega_0            = 30                    UNCHANGED   (no §2.2 amendment)
S2  residual entering L_phys = R̃_m = R̄_m / R_ref     NEW         (§3.2 amendment)
S2b scope of normalization   = residual-wide (weights AND loss), reference detached
    R_ref                    = median R̄ over the GATE-04 train-free probe,
                               ≥6 seed/IC combinations, frozen for Stage 0,
                               recorded in training_metadata.json
S1  eta_c                    = 1                     UNCHANGED as a value;
                               LOSS-04 amended only in what the exponent consumes
S4  n_col                    = 4096                  spec value honored (:454/:461 unchanged)
    M (prefix-sum length)    = 16 fixed equal bins in u; R̄_m = mean over the bin
S5  causal-exponent clip     = dtype-derived floor    UNCHANGED in purpose and value;
                               clip-binding count added to the step record
```

**Predicted train-free behaviour under this recipe** (clean-room, six seed/IC
combinations, `[OWN]`, subject to ERW Rule 19 re-derivation in-repo): 0 weights on the
clamp floor; 16 distinct weights per step; `front_idx` 0–2 at initialization and
unconstrained above; `L_phys(step 0) ≈ 6×10⁻²` (`= w₁R̃₁/M` with `R̃₁ ≈ 1`, `M = 16`) instead of ≈1.6×10⁹;
phys/data raw gradient ratio ≈ 2.6 decades instead of 12.8.
That is GATE-04 (i), (ii) and (iii) satisfied by construction rather than by luck.

**What the composed recipe does *not* fix, stated plainly.** The `L_IC` velocity term
(`‖v′‖ ≈ 230–330` against a true `v′` of order 1 — audit §6d) is untouched by every
option on every menu, and `loss_ic` median 2.897×10⁴ never converged in the retained
run (`.../stage0-rerun-seed41-attempt-02/logs/train.log.jsonl`) `[REPO]`. A recipe that passes GATE-04 can still be dominated by an IC anchor two
decades above the data term. This is recorded as `G-9`, not solved here.

#### The joint disposition, as a menu

| | Joint option | What it changes relative to J1 | Door |
|---|---|---|---|
| **J1** | **The composed recipe above** — A1 + B2 (residual-wide) + C1 + D3 + E1 | — | **Two-way at the gate, one-way after it.** Every failure mode it has is a step-0 failure mode, and GATE-04 is train-free, so a mis-pick costs a probe. Anything that survives GATE-04 and fails in training cannot be retuned under SCOPE-37 |
| **J2** | J1 with **D4** for D3: `n_col = 2048`, `M = 32` | Halves the collocation cost and moves `M` into the source's own reported range; steeper weight profile (`w_min ≈ 1.5×10⁻¹⁴`) | **Two-way at the gate** — same reason as J1 |
| **J3** | J1 with **B4** for B2: relative residual instead of a frozen constant | Carries no frozen scalar across stages and stays valid if the architecture changes; adds the `‖a′‖`-inflation hazard and a monitoring obligation | **Two-way at the gate**, with one residual risk (the inflation incentive) that only shows in training |
| **J4** | Unnormalized route: B1 + A3 (annealed `η_c`) + C1 + D1 + E1 | Amends less of §3.2 and stays closer to the source's *procedure* rather than its precondition | **One-way.** It leaves PC-6 live, and PC-6's failure mode is invisible to GATE-04 — a run can pass the gate and still train on the physics term alone |

> **Suggested default: J1.** Reason: it is the only assembly in which every menu's
> default reaches its own threshold *and* the cross-menu warnings in the table above
> are all dischargeable in amendment text rather than in engineering judgement.
>
> **Door on the default: two-way at the gate, one-way after it** — stated once here
> because it is the classification that governs the whole ruling: GATE-04 is train-free,
> so every step-0 failure is cheap; SCOPE-37 makes every post-gate failure expensive.

#### Contract amendments the composed recipe requires (SCOPE-38)

| Contract | Amended? | What must be recorded |
|---|---|---|
| LOSS-04 / D-04 / AC-LOSS-04 (`:445`) — `η_c = 1` | **Yes, in kind not in value** | The superseded ruling named; the new decision's provenance; a re-issued acceptance criterion; explicit statement that the *value* 1 is retained and the *argument* changes from `R̄` to `R̃` |
| §3.2 residual definition (`:429`) | **Yes** | `R̃_n = R̄_n / R_ref`; the definition, provenance and freeze protocol of `R_ref`; the re-check trigger |
| SPEC-06 `n_col`/`N_t` (`:454`, `:461`) | **Values unchanged; structure added** | The `M`-bin aggregation, the bin-edge definition, and the empty-bin policy |
| §2.2 `first_omega_0` fixed-at-30 (`:181`) | **No** | — |
| §4.1 clip, underflow-only (`:668-671`, `:692`) | **No** | Instrumentation only |
| PHYS-05 per-stage `λ^max` table (`:683`, `:688`) | **No** | An explicit statement that the normalization is a residual-definition change and the locked table is untouched |

---

## 4. What the runbook inherits

A person implementing the ratified recipe must carry forward the following. Items
marked **⚠** are silent-failure risks.

1. **⚠ Threshold re-expression.** Normalizing `R̄` rescales every absolute threshold
   stated in physics-loss units by `1/R_ref ≈ 5.9×10⁻¹¹`. At minimum:
   `ε_phys` (ADVANCE criterion 3, `1×10⁻⁴`) and `run.guards.loss_explosion_ceiling`
   (`run.guards.loss_explosion_ceiling: 1e11` in `.../stage0-rerun-seed41-attempt-02/config.yaml`) `[REPO]`. Either re-express them or state
   explicitly that the gate is now defined on the normalized quantity. A run that
   ships with these unchanged will pass its explosion guard trivially and never pass
   its ADVANCE gate.
2. **`R_ref` provenance and freeze protocol.** Where it is measured (the GATE-04
   probe), over what (seeds, IC combinations, collocation points), which statistic
   (median suggested — the clean-room per-point spread across seeds is 1.3×10⁹ to
   1.1×10¹¹, while per-seed medians span only ~3× `[OWN]`), where it is recorded, and what
   invalidates it: any change to `ω₀`, depth, width, `p`, the LayerNorm placement or
   `eps`, the init bounds, `D`, `T`, `ε_soft`, or the IC13 normalization.
3. **Bin-edge definition.** "M equal sequential segments" in `u ∈ [0,1]`, fixed across
   steps — not equal-count bins of the sorted sample, which would re-introduce the
   step-to-step incomparability of D-2. Empty-bin policy must be stated (with 4096
   points in 16 bins the probability is negligible but not zero).
4. **⚠ `front_idx` and invariant B semantics.** Under a frozen reference, `front_idx`
   measures progress against a fixed initialization scale rather than an absolute
   physical one. The `N = 500` front-advance window (`run.invariants.front_advance_window_n`,
   `guards.py:593-615`) was ratified against the old semantics and should be
   re-ratified or explicitly carried over with a reason.
5. **Run-record fields.** `R_ref` and its provenance; per-seed `w_min`, `w_max`,
   `w_mean`, `front_idx`; the new clip-binding count; `M` and `n_col`; and the
   per-term gradient norms that already exist (INST-02/03) plus
   `grad_norm_raw_phys / grad_norm_raw_data` as a **first-class monitor**, because
   PC-6 is not covered by GATE-04.
6. **GATE-04 probe outputs.** The probe must emit `R_ref` *and* the three pass
   conditions per seed, so that one artifact both calibrates and gates.
7. **A `## References` codification item.** `pinn_architecture.md`'s reference list
   should cite Wang, Sankaran & Perdikaris (CMAME 421, 2024, 116813) for §3.2 and
   Sitzmann et al. (NeurIPS 2020) is already there as [5]/[6]/[8]/[9]. This is a
   VER-20 (a)–(d)-class wording fix, not part of the recalibration, and it closes
   `F-13`.
8. **Amendment wording discipline.** The two coherence warnings in §3.6 (PHYS-05
   equivalence; Option-C distinction) must be discharged *in the amendment text*, not
   in a summary.

---

## 5. Decision sheet (fill-in)

| # | Decision | Options | Suggested default | Door type | Owner's pick |
|---|---|---|---|---|---|
| S1 | `η_c`, causal-weight exponent coefficient | A1 keep `η_c=1` on a normalized `R̃` · A2 `η_c ≈ 2×10⁻¹²` unnormalized · A3 anneal per source Algorithm 1 · A4 rank-based, no `η_c` | **A1** | **Two-way** — failure visible to the GATE-04 train-free probe; one constant; LOSS-04 re-ratification is paperwork, not a run | |
| S2 | `R̄` normalization and reference scale | B1 none · **B2 frozen reference from GATE-04 probe** · B3 lagging EMA · B4 relative residual vs local acceleration scale | **B2** | **Two-way on mechanism, one-way on semantics** — re-measuring costs a probe, but the threshold re-expression (runbook item 1) fails silently if missed | |
| S2b | Scope of the normalization *(sub-decision the package does not surface)* | exponent-only · **residual-wide (weights + `L_phys`)** | **residual-wide** | **Two-way** — but exponent-only leaves PC-6 unaddressed, which is a one-way loss of the run | |
| S3 | `first_omega_0`, SIREN initialization scale | **C1 unchanged (30)** · C2 reduce · C3 address §2.3's power-skip stack *(outside SCOPE-33)* | **C1** | **Two-way** (it is the absence of an amendment). C2 is one-way in governance: a SCOPE-38 re-ratification spent on ≤0.7 decades | |
| S4 | `N_t` / `n_col`, collocation count and prefix-sum length | D1 `n_col=16`, amend spec · D2 `n_col=4096`, prefix over all points · **D3 `n_col=4096`, `M=16` fixed bins** · D4 `n_col=2048`, `M=32` | **D3** | **Two-way** in contract (recorded integers, probe-visible); one-way in engineering time (binning is new code) | |
| S5 | Causal-exponent clip semantics | **E1 unchanged + make binding observable** · E2 numeric bound · E3 remove | **E1** | **Two-way** — no value changes; instrumentation only | |
| S6 | Joint disposition (SPEC-01 + SPEC-06 ratified together) | **J1 composed recipe as stated** (A1+B2/residual-wide+C1+D3+E1) · J2 the same with D4 substituted for D3 (`n_col=2048`, `M=32`) · J3 the same with B4 substituted for B2 (no frozen constant to carry across stages) · J4 unnormalized route (B1+A3 annealed, C1, D1, E1) | **J1** | **J1, J2, J3 two-way at the gate, one-way after it** — GATE-04 catches every step-0 failure mode; SCOPE-37 means anything that survives GATE-04 and fails in training cannot be retuned. **J4 is one-way**: it leaves PC-6 live, so its failure mode is invisible to GATE-04 | |
| — | *Out-of-scope item raised for a separate ruling — **not a menu*** | widen SCOPE-33 to admit §2.3's power-skip stack as a surface · decline and record why | **not proposed** — recorded because PC-1 locates 8.66 of the ≈9.6 needed decades there | **One-way** — a scope widening | |

---

## 6. Gaps

Recorded, not resolved. `G-1`, `G-2`, `G-5` are the package's own gaps, unchanged by
this round; the rest are new.

- **G-1 — post-initialization behaviour is still unestablished.** Everything derived
  here is at initialization plus closed-form arithmetic on the weight definition. No
  source, and no computation in this report, establishes what any recalibrated recipe
  does after step 0. The master's cross-cutting entry stands verbatim.
- **G-2 — the converged-scale datum is a single measurement.** Gate B's 0.65 %
  relative residual (`F-12`) was measured on ground-truth trajectories with a Phase-38
  network. Whether Stage-0 trajectories reach it is unestablished, so the 14.4-decade
  traversal is anchored at its lower end by a *target* (`ε_phys = 10⁻⁴`), not by an
  observation.
- **G-3 — no source calibrates `ε` across a 14-decade descent.** The published
  annealing range is 4 decades over 5 values. Extrapolating the source's procedure to
  ~16 stages (option A3) is unvalidated by anything I could find.
- **G-4 — the 8.66-decade stack contribution is not decomposed.** My clean-room sweep
  measures it in aggregate (≈1.44 decades per SQR block) and identifies LayerNorm's
  scale-invariance as the mechanism that neutralizes `ω₀`, but does not apportion it
  among depth, `p = 2`, the LayerNorm placement, and `elementwise_affine=False`. §2.3
  is not an authorized surface, so no source dispositions it.
- **G-5 — no source tests combined dispositions.** The composed recipe's coherence is
  argued from arithmetic and from a clean-room model, not from any run.
- **G-6 — my numbers are not the project's numbers.** The clean-room re-implementation
  matches the audit's probe within its spread, which is corroboration, not
  substitution. Every `[OWN]` figure carries the ERW Rule 19 obligation: reproduce it
  with INST-04's probe against the project's own `ArchitectureSpec()` and record the
  verification before it informs the ruling.
- **G-7 — L-BFGS interaction unanalyzed.** During L-BFGS, `λ` values are frozen and no
  clipping applies (`pinn_architecture.md:698`, `:768`) `[REPO]`. Whether a frozen `R_ref` and a
  normalized residual behave correctly inside a strong-Wolfe line search is not
  examined here.
- **G-8 — Adam's scale invariance may absorb part of the intended rebalancing.** Adam
  normalizes by its second-moment estimate, so a *global* rescaling of `L_phys`
  changes the step much less than it changes the loss. The benefit claimed in PC-6 is
  specifically about **float32 gradient accumulation** and **relative term weighting**,
  not about step size. The size of the residual effect is unestablished.
- **G-9 — the `L_IC` velocity scale is on no menu.** See §3.6.
- **G-10 — no live-tree commit pin.** The connected mount is a git worktree whose
  `.git` file points outside the mount, so `git log`/`git status` are unreachable and
  no ERW Rule 20 live-tree hash can be recorded. Every citation here is by
  `file:line` **and** content, and every one was content-matched; a Rule 20 pin should
  be attached by someone with repository-level git access before this report is filed.
- **G-11 — bin-edge and empty-bin policy for D3 is unspecified by any source.** The
  papers say "M equal sequential segments" and stop there.
- **G-12 — `R_ref` across stage boundaries.** The composed recipe freezes `R_ref` for
  Stage 0. Stage 1+ is outside SCOPE-36, so nothing here establishes whether the
  reference should be re-measured, carried, or re-ratified at a stage boundary.

---

## 7. Claims and uncertainty register

| ID | Claim | Basis | Confidence | How it would be falsified |
|---|---|---|---|---|
| R-01 | The source method is Wang, Sankaran & Perdikaris, CMAME 421 (2024) 116813; §3.2's formula is its Eq. 3.2 / Expert's-Guide Eq. 2.11 term for term | `[LIT]` + `[REPO]` `causal_pinn.py:55-60` | High | A different published prefix-exponential temporal weighting predating it and matching more closely |
| R-02 | The source's calibration procedure is annealing `ε` over `{10⁻²…10²}` with advance criterion `min_i w_i > δ = 0.99`; Expert's-Guide default `ε = 1.0`; PINA default `eps = 100` | `[LIT]`, `[REPO]` `causal_pinn.py:76` | High | Reading the published Algorithm 1 and finding different values |
| R-03 | The source's prefix sum runs over `M` temporal segments with the residual averaged within each; this project's runs over individual collocation points | `[LIT]` + `[REPO]` `loss_catalog.py:330-333`, `controllers.py:656` | High | — (both sides read directly) |
| R-04 | `R̄ ∝ ω₀⁴` for a pure SIREN, but under the locked SQR stack the measured law is ≈`ω₀^0.5`: 1.63 decades per 1000× | `[OWN]` derivation + clean-room sweep | **Medium-high** — the mechanism (LayerNorm scale-invariance) is analytic and exact in the small-`ω₀` limit; the measured exponent at `ω₀ = 30` is empirical and from a clean-room model | INST-04 sweeping `ω₀` on the project's own model and finding `R̄` falling as `ω₀⁴` |
| R-05 | The power-skip stack carries ≈8.66 decades of the initialization `R̄`, ≈1.44 decades per SQR block | `[OWN]` clean-room depth sweep, 5 seeds | Medium-high | Same probe on the project's model with depth ablated |
| R-06 | A fixed `η_c` on unnormalized `R̄` has a 3.24-decade informative window against a 14.4-decade traversal | `[OWN]` arithmetic; thresholds `[REPO]`/`[PKG]` | **High** — closed form; only the window's soft lower edge (0.05) is a judgement call | Showing the mechanism is useful with all weights within 1 % of 1 |
| R-07 | float64 is not a lever: 15/16 weights still floored; total clip range 0.91 decades | `[OWN]` + `[REPO]` `loss_catalog.py:97` | High | — |
| R-08 | Instantaneous normalization makes `front_idx` unable to advance | `[OWN]` arithmetic + `[REPO]` `controllers.py:692-694`, `guards.py:593-615` | High | — |
| R-09 | Residual-wide normalization moves the phys/data raw-gradient ratio from 12.80 to ≈2.57 decades | `[REPO]` log ratio; `[OWN]` rescaling arithmetic | **Medium** — the rescaling is exact, but the *effect* on optimization is confounded by Adam (G-8) | Measuring per-term gradient norms under the recipe and finding the ratio unchanged |
| R-10 | The composed recipe satisfies GATE-04 (i)–(iii) at initialization on six seed/IC combinations | `[OWN]` clean-room | **Medium** — corroborated by the model reproducing `F-01`, but it is not the project's code (G-6) | INST-04 running the recipe and finding floored weights or a degenerate vector |
| R-11 | `F-02`'s row text contradicts `M2`/`F-11`/`A-1` in the same document | `[PKG]` textual | High | — |
| R-12 | All 10 bundle excerpts and all cited spec anchors resolve correctly in the live tree | `[REPO]` + `[OWN]` | High | — |
| R-13 | The retained log's `w_min`, `w_mean`, `front_idx`, gradient ratio and `λ_phys` ramp are as `F-04`/`F-05` state | `[REPO]` primary log, 502 rows | High | — |
| R-14 | `R̄` has a lower floor set by `‖F_grav‖²` when the position scale collapses | `[OWN]` depth-0 `ω₀` sweep | Medium | A low-`ω₀` configuration holding `‖r′‖ ~ O(1)` and reducing `R̄` monotonically |
| R-15 | Nothing in this report selects a remedy; every default is a candidate for checkpoint ② | self-attested against SCOPE-34 | High | — |

---

## 8. Owner-gated experiment proposals (proposed only; none performed)

Each is train-free unless marked otherwise, and each is a proposal for the owner to
authorize, never an action taken here.

1. **X-1 (train-free, highest value).** Run INST-04's probe on the project's own
   `ArchitectureSpec()` across the six audit seed/IC combinations under the composed
   recipe, emitting `R_ref`, per-seed `w_min`/`w_max`/`front_idx`/distinct-weight
   count, clip-binding count, `L_phys(step 0)` and the per-term gradient norms. This
   is GATE-04 executed once as a calibration pass, and it discharges R-10 and G-6.
2. **X-2 (train-free).** Depth ablation of the probe (0, 2, …, 12 hidden layers) at
   `ω₀ = 30`, and an `ω₀` sweep at fixed depth 12, on the project's model. Discharges
   R-04 and R-05 and settles whether S3 or §2.3 is the real surface — the evidence the
   scope question in the decision sheet's last row needs.
3. **X-3 (train-free).** Evaluate the four S2 options on one stored probe residual
   vector and report the three GATE-04 conditions for each. Discriminates B2 / B3 / B4
   without a run.
4. **X-4 (training; owner-gated, spends no held-out evaluation).** A short Stage-0
   segment under the composed recipe with invariant B's window unchanged, reporting
   `front_idx` trajectory and the phys/data gradient ratio. This is the only proposal
   that touches G-1, and under SCOPE-37 it should be authorized *before* the recipe is
   locked, not after — otherwise its findings are unusable.

---

## 9. Compliance statement

No file edited. No training run started. No evaluation invoked. No side-effecting
command run; no commit made. No framework specification edited. No remedy selected —
every default above is marked *suggested* and every one is a row awaiting the owner's
pick at checkpoint ②. Discriminating experiments appear in §8 as owner-gated
proposals only. All `[OWN]` computation was performed in a separate sandbox on a
clean-room re-implementation of the published spec text, importing no project module
and reading no project data, and is subject to ERW Rule 19 in-repo verification
before it informs any decision, roadmap, or spec edit.

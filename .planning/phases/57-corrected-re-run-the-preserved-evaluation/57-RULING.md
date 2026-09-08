---
phase: 57
milestone: v2.3
created: 2026-09-08
pre_registered_at: "2026-09-08T02:05:10Z"
status: ratified
authority: direct owner instruction on 2026-09-08
---

# Phase 57 — GATE-04 and Checkpoints ③/④ Ruling

## Authority and boundary

The owner directly authorized the following decisions on 2026-09-08:

> GATE-04: require at least a 2:1 spread among the non-anchor weights, then use
> a fixed formula to reduce all residuals so the expected final weight is
> 1/sqrt(2). Require the front to reach bin 15 and every perturbed weight to be
> at least 0.70.
>
> Checkpoint ③: explicitly re-ratify N = 500, use one frozen training-only
> monitor, and freeze L-BFGS weights and samples for its entire segment.
>
> Checkpoint ④: pre-register seed 42, with fallback order 41 then 43 only for
> structural ineligibility.

This record resolves GAP-56-01, GAP-54-06, and owner checkpoints ③ and ④. It
does not resolve GAP-56-02 or checkpoint ⑤, authorize recipe retuning, declare
GATE-04 passed, launch training, or spend the held-out evaluation. Earlier
packet-only or deferred descriptions of these named decisions are superseded.

## 1. GATE-04 — GAP-56-01 resolved

Apply the rule independently to every required initialization-probe case. Use
0-based bins `b = 0..15`; `w_0 = 1` is the forced anchor and is excluded from
the spread calculation.

### Baseline non-degeneracy

After the existing condition-(i) finite/non-floor checks, require

```text
max(w_1, ..., w_15) / min(w_1, ..., w_15) >= 2.
```

No coefficient-of-variation, distinct-value count, decade-range requirement,
or additional endpoint threshold is part of this ruling.

### Controlled residual reduction

Let `x_b = Rbar_b / R_ref` be the 16 normalized squared-residual bin means and
let the exclusive final prefix be

```text
P_15 = sum(x_b for b = 0..14).
```

For a finite positive `P_15`, define the single pre-registered scale

```text
alpha = log(sqrt(2)) / P_15 = log(2) / (2 * P_15).
```

Holding the same frozen `R_ref` and every other recipe input fixed, multiply
all 16 squared-residual bin means by `alpha` and recompute the weights through
the path under test. If the perturbation is applied to residual amplitudes
before squaring, the corresponding amplitude factor is `sqrt(alpha)`. Do not
scale a returned weight vector, refit `R_ref`, search over perturbations, or
perturb only late bins.

The expected final perturbed weight is therefore fixed analytically:

```text
w'_15 = exp(-alpha * P_15) = 1 / sqrt(2) ~= 0.707106781187.
```

The controlled-reduction check passes only if the recomputed front reaches bin
15 under the existing `front_idx = max(b: w_b > 0.5)` definition and every
perturbed weight is at least `0.70`. The existing finite/non-floor requirements
remain fail-closed. Because the non-anchor baseline spread is at least `2:1`
and causal weights are non-increasing and do not exceed one, the baseline has
at least one non-anchor weight at or below `0.5`; reaching bin 15 therefore
demonstrates a real front response without adding another baseline endpoint
threshold.

The production implementation and focused tests must encode this rule, and
GATE-04 must be re-run over all required cases to a complete PASS before
RUN-04. The earlier `PASS INCOMPLETE (unratified: ii)` evidence is historical,
not run authorization.

## 2. Checkpoint ③ — invariant B and optimizer semantics

### Window and monitor

`front_advance_window_n = 500` is explicitly re-ratified for the amended
recipe. This is a new owner decision, not silent inheritance from v2.2.

Each run uses one training-only monitoring context fixed before the run's first
optimizer update. Its selected training identities, collocation rows, bin
assignments, and normalized times remain unchanged for the full run and across
the Adam-to-L-BFGS handoff. It is re-evaluated only as model parameters change.
Resampled training-batch fronts remain diagnostic-only and cannot satisfy
invariant B. The existing front definition, high-water advancement semantics,
500-step deadline, persistence across resume, and fail-closed malformed-state
checks remain in force; this ruling adds no new front margin, observation
cadence, or persistence-count threshold.

The frozen monitor and its provenance must be persisted so a resume restores
the same monitor bytes and invariant-B state. It may contain training-split
material only; validation or held-out test material is prohibited.

### L-BFGS

For the entire Stage-0 L-BFGS segment, freeze the segment's collocation samples
and detached causal weights. They are selected/computed at the Adam-to-L-BFGS
handoff and are not redrawn or recomputed in line-search closures or between
L-BFGS outer calls. Trial closures re-evaluate the model and residuals at the
trial parameters against those fixed samples and weights. The separate frozen
monitor still recomputes its monitoring weights at accepted parameter states.

This resolves GAP-54-06: the L-BFGS line search receives a consistent fixed
surrogate instead of comparing scalars whose detached weights change with the
trial parameters. Resume must restore the same segment samples and weights or
fail closed. Adam retains the already-ratified per-step sampling behavior.

## 3. Checkpoint ④ — EVAL-02 pre-registration

- The spending seed is **42**.
- If seed 42 is structurally ineligible, use **41**; if seed 41 is also
  structurally ineligible, use **43**.
- Fallback is eligibility-only. No observed loss, validation value, front
  trajectory, or other scientific result may trigger or reorder it.
- The existing v2.2 Phase-50 structural-eligibility and `best.pt` candidate
  rules carry forward as the EVAL-02 structure, subject to Phase 57's stricter
  GATE-04, invariant-B, terminal-state, and canonical-frame preconditions.
- If the declared terminal branch fires or no structurally eligible candidate
  exists, preserve the evaluation unspent. Do not invent another seed or spend
  a second look.

This file and its commit ancestry are the pre-run, timestamped registration.
The selection rule is fixed before any Phase-57 training or held-out access.

## 4. Read-only arithmetic check

The committed six-case Phase-56 GATE-04 evidence was replayed without changing
it:

- Source: `../56-contract-amendment-train-free-gate/evidence/gate04/20260907T033409Z/raw.json`
- SHA-256: `38711a5e3bd67a05a9912e09ed9258b6db91f720a69e215e0fd4effecb3db358`

| Case | Non-anchor spread | `alpha` | `w'_15` | Minimum perturbed weight | Front |
|---|---:|---:|---:|---:|---:|
| 41 | 300522.943 | 0.0255906266571 | 0.707106781187 | 0.707106781187 | 15 |
| 42 | 3.58556874e+09 | 0.0140961046404 | 0.707106781187 | 0.707106781187 | 15 |
| 43 | 842942.692 | 0.0227408236828 | 0.707106781187 | 0.707106781187 | 15 |
| 0 | 3641741.37 | 0.0206403475805 | 0.707106781187 | 0.707106781187 | 15 |
| 7 | 347257.822 | 0.022411168035 | 0.707106781187 | 0.707106781187 | 15 |
| 41-variable-mass | 5617891.92 | 0.0210712380994 | 0.707106781187 | 0.707106781187 | 15 |

All six non-anchor spreads exceed `2:1`. This checks the ruling's arithmetic;
it does not verify the missing production implementation or complete GATE-04.

## 5. Remaining pre-run sequence

Before RUN-04, Phase 57 still must be researched and planned, implement the
bounded production conformance patch authorized by GAP-57-01, implement these
gate/monitor/L-BFGS decisions, pass focused tests and separate production-path
verification, re-run GATE-04 to a complete PASS on the run recipe, and complete
the calibration smoke. No training or held-out evaluation is authorized by
this decision record alone.

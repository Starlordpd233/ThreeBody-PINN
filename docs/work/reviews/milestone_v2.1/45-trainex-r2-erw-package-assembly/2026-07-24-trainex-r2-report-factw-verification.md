---
status: active
purpose: verification-report
created: 2026-07-24
milestone: v2.1
phase: trainex-r2-erw-package-assembly
retirement_trigger: Superseded when the next milestone's readiness-verification phase re-certifies these claims as part of adjudicating the trainex-r2 resolution doc, or when the owner rules the underlying divergences resolved.
---

# trainex-r2 Report — Independent Verification of the `[FACT-W]` Conformance Claims

## Why this exists

The returned trainex-r2 research report
(`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/trainex-r2-research-report.md`)
disclosed a deviation from the package's "no codebase access" clause: under an
owner commissioning override it read the repository read-only, and labels every
resulting claim `[FACT-W]` — offered explicitly "for owner verification, not as
substitutes for the attachments" (report §0).

Those `[FACT-W]` claims are not answers to Q1–Q6. They assert that the executed
Stage-0 pilot **diverged from the locked framework specs**, and report §7 uses
them to qualify the DIAG-04 hypothesis rankings that are the Phase 44
deliverable and the trainex-r2 package centerpiece. That makes them
consequential enough to verify independently before any of them is carried into
the next milestone's adjudication.

Scope verified here: the five divergence claims that move the DIAG-04 table
(SV-1, SV-2, RG-03, RG-04, RG-11) plus RG-10 (the instrumentation claim the
locked Phase-35 contract names as the precondition for any reweighting verdict).
RG-02 and RG-06 are recorded as undecidable from this repository — see
"Not verifiable here".

**Method.** Read-only inspection of retained run artifacts, the shipped `pinn/`
code as the factual record of what executed, and the two locked framework specs.
No training, no evaluation, no evaluator invocation, no file under `pinn/` or
`framework-specs/` modified — SCOPE-22..26 intact.

## Verdicts

| Claim | Report's assertion | Verdict |
|---|---|---|
| SV-1 | Pilot ran λ_E = 1.0; locked PHYS-05 sets λ_E^max = 0 for Stage 0 | **CONFIRMED** |
| SV-2 | Causal weighting collapsed to the first collocation point for the whole run | **CONFIRMED (broader than stated)** |
| RG-03 | Training ε_H is per-anchor `|h0|·1e-4 + 1e-12`, not locked `1e-4·S_H` | **CONFIRMED** |
| RG-04 | R̄ uses (1/9)Σ where §3.2 locks (1/3)Σ | **CONFIRMED** |
| RG-11 | Causal-exponent clip absent in code | **CONFIRMED (sharper than stated)** |
| RG-10 | Per-term gradient statistics never logged | **CONFIRMED** |

Nothing in the verified set was refuted. Two claims are stronger against the
evidence than the report asserted; both sharpenings are flagged below.

---

### SV-1 — λ_E = 1.0 executed against a locked Stage-0 value of 0 — CONFIRMED

**Locked side.** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:663`:

> λ_E^max(k) = λ_L^max(k) = {0 for k ∈ {0,1}; 10^(k−4) for k ∈ {2,3,4}; 1 for k ∈ {5,6}}

Stage 0 is k = 0, so the locked Stage-0 value is **0**. The Phase-35 contract
(`pinn_architecture.md:667`, restated `ctl_instruction.md:1759`) directs
"Retain the PHYS-05 warmup schedule **above** with `lambda_E^max <= 1`" — i.e.
the ≤1 cap is an *additional* constraint on the retained per-stage schedule, not
a replacement for it. λ_E = 1.0 at Stage 0 is therefore not "inside a locked
cap"; it is the **Stage-6 value applied at Stage 0**, contradicting the
schedule the same contract retains.

**Executed side.** `loss.lambda_e_max: 1.0` in all four run configs
(`runs/stage0-pilot-seed{41,42,43}/config.yaml:6`, `runs/stage0-smoke/config.yaml:6`),
and the per-step log shows it applied, not merely configured
(`runs/stage0-pilot-seed42/logs/train.log.jsonl`):

| step | λ_data | λ_IC | λ_phys | λ_E | λ_L |
|---|---|---|---|---|---|
| 1 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| 151 | 1.0 | 1.0 | 1.0 | **1.0** | 0.0 |
| 300 | 1.0 | 1.0 | 1.0 | **1.0** | 0.0 |

λ_E ramps to 1.0 and holds. λ_L ≡ 0 throughout, which *does* match the locked
Stage-0 value — so of the two conservation weights the schedule zeroes, only
λ_E diverges.

**Consequence for the question set.** Q3 as posed to the researchers describes a
Stage 0 with conservation weights zero by design. No run in the retained
evidence instantiates that configuration. Q3's premise does not describe the run
that failed the gate.

**RG-01 stands unresolved.** Whether λ_E^max = 1.0 was an owner-sanctioned
calibration choice or unratified drift is not answerable from the repository.
`runs/*/config.yaml` records the value, not its authorization; the code marks
the caps config-overridable provisional defaults. This is an owner question.

### SV-2 — Causal collapse — CONFIRMED, and broader than the report states

The report describes the collapse for the pilot. It holds across **every
retained run**:

| run | steps | `front_idx` | `w_mean` | `w_max` |
|---|---|---|---|---|
| stage0-smoke | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-smoke-diag | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed41 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed42 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |
| stage0-pilot-seed43 | 300 | 0 × 300 | 0.0625 × 300 | 1.0 × 300 |

**1500 of 1500 logged steps, five of five runs.** `front_idx` never advances off
0 and the weight statistics are bit-stable for the entire history.

The arithmetic pins the mechanism exactly. `collocation_count=16`
(`pinn/train.py:756`), and the spec gives w₁ = exp(0) = 1 unconditionally
(empty preceding sum, `pinn_architecture.md:414`). `w_mean = 0.0625 = 1/16`
exactly, with `w_max = 1.0` and `w_min = 0.0`, is only consistent with
**w₁ = 1 and w₂…w₁₆ underflowed to exactly 0.0**. Physics supervision reached
one collocation time — the earliest — and never widened, in any run, at any
step.

### RG-03 — ε_H formula — CONFIRMED, and self-documented in code

`pinn/training/controllers.py:482`:

```
eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12
```

with `energy_floor_factor: 0.0001` (`runs/stage0-pilot-seed42/config.yaml`). The
module docstring (`controllers.py:35-36`) states the divergence outright:

> `eps_h` is a provisional `|h0| * 1e-4` scale (mirrors the documented
> `eps_h = 1e-4 * S_H` form; no `S_H` pipeline exists yet upstream…)

So this is a per-anchor scale standing in for a dataset-wide
`S_H = median_train(K0 + Uabs0)` normalizer that was never built. Confirmed as
stated, and the code's own comments concede it.

### RG-04 — R̄ normalization factor — CONFIRMED, factor of exactly 3

**Locked** (`pinn_architecture.md:408`): R̄_n = (1/3) Σ_{i=1}^{3} ‖f_i(u_n)‖²

**Implemented** (`pinn/training/controllers.py:534`):
`rbar = (residual ** 2).mean(dim=(-2, -1))` where `residual` has shape
(N_t, 3, 3) — a mean over **9** scalars, since ‖f_i‖² is itself a sum over 3
components. The implemented R̄ is exactly **one third** of the specified R̄.

The downstream consumer is correct: `(weights * rbar).mean()`
(`pinn/loss_catalog.py:261`) matches the locked
L_phys^causal = (1/N_t) Σ w_n R̄_n (`pinn_architecture.md:419`).

*My analysis, not the report's and not established:* because R̄ sits inside the
causal exponent, a 3× **under**-estimate makes the weights decay more slowly
than specified. The spec-correct factor would make the SV-2 collapse *more*
severe, not less. So RG-04 cannot be the cause of the collapse — but the factor
is wrong in the direction that partially masks it, and it also scales the whole
physics loss by 1/3. The report's "immaterial at observed magnitudes" reading is
plausible for the loss magnitude; it is not a reason to leave the formula
divergent.

### RG-11 — Causal-exponent clip — CONFIRMED, and this is a MUST, not a deferral

This is the one place the report is *more* forgiving than the spec warrants.
RG-11 frames the clip as spec-deferred and unimplemented. The locked text
(`ctl_instruction.md:1773`) is normative:

> The exponent **must be clipped** to avoid underflow, but no numeric clipping
> bound is selected in Phase 35; the bound remains deferred to FUT.

The *bound* is deferred; the *clipping* is mandated. The implementation applies
none — `weights = torch.exp(-eta * cumsum_excl)`
(`pinn/loss_catalog.py:258`), with the docstring conceding "The exponent is left
unclipped except by the natural finite range of `exp`"
(`pinn/loss_catalog.py:228-229`).

Underflow to exactly 0.0 is precisely the failure the mandated clip exists to
prevent, and SV-2 shows it occurred on every step of every run. This is a
conformance defect against a normative MUST, not an open design question.

### RG-10 — Gradient instrumentation — CONFIRMED

The retained log carries 27 fields; exactly one is gradient-related,
`grad_norm` — a single global pre-clip norm, marked
"⚖ PROVISIONAL (B-2)" in `pinn/training/step_log.py:151-154`. No per-term
gradient statistics exist in any retained artifact.

The locked Phase-35 contract (`pinn_architecture.md:667`) makes them a
precondition: "Before any future control law, log weighted losses, scheduled
weights, and gradient statistics; automatic dominance reweighting is deferred
until measured weighted-loss/gradient evidence exists."

**Consequence.** Any loss-reweighting remedy is currently unreachable on the
locked spec's own terms — the evidence it requires was never recorded. This is
an instrumentation gap, not a data gap: it is fixable by logging, but not
retroactively for the runs already executed.

## Not verifiable here

- **RG-02 (executed target frame: raw positions vs §3.1's `r_true/D`)** — the
  code path is confirmable but the data-level truth is not: the corpus payload
  is absent from this worktree, so whether the raw corpus units make this an
  identity or a live inconsistency cannot be settled. The report's own proposed
  train-free residual-on-stored-targets check (its Q3(e)1) would settle it, and
  that is an owner-authorization-gated proposal, not work performed here.
- **RG-06 (whether admitted data supports a fresh held-out draw)** — requires
  parsing `splits.json` against admitted-set population counts; not needed for
  any verdict above.

## Candidate gap-register rows — proposed, not filed

Filing these depends on the owner's close decision (do these belong to v2.1, or
to the next milestone's scope), so they are listed here rather than written into
`.planning/milestones/v2.1-GAPS.md`. None is adjudicated; each is routed, per
the v2.1 investigation discipline, as an owner/ERW question.

1. **Authorization of λ_E^max = 1.0 at Stage 0** (from RG-01/SV-1) — sanctioned
   calibration or unratified drift? Classification: semantic + process. The
   repository records the value, never its authorization.
2. **The PHYS-05 lock boundary** (from RG-09) — is the locked object the
   schedule *form* plus the ≤1 cap, with per-stage values calibration-open, or
   the per-stage values themselves? Determines whether item 1 is a defect or a
   choice. Classification: process-artifact schema / semantic.
3. **Conformance vs tuning as the next milestone's frame** (from SV-1, SV-2,
   RG-03, RG-04, RG-11 jointly) — the remedy space the trainex-r2 questions
   assume is recipe *tuning*. Five verified divergences mean the failing run may
   not have instantiated the locked recipe at all. Classification: cross-phase
   reframing — this changes downstream scope and must not be decided inline.
4. **Standing of the DIAG-04 rankings** (from report §7) — H-01/H-03's
   "no contradicting evidence" cell no longer reads cleanly; H-06 gains
   concrete, checkable loci. Whether Phase 44 takes an erratum is the owner's
   call.

## What this does and does not establish

**Established:** five spec-vs-implementation divergences in the code that
produced the failing Stage-0 pilot, each re-derivable from the file:line
citations above; and that the collapse in SV-2 is total and universal across
retained runs, not a pilot-specific artifact.

**Not established:** that any of them *caused* the physics-gate failure. No
causal claim is made or implied here. The uniform 1500/1500 held-out failure
(F-02) remains consistent with several mechanisms, and discriminating between
them requires runs that SCOPE-22..26 forbid and that only the owner can
authorize.

**The one thing that has changed for the next milestone:** the remedy space is
no longer purely "which training knob to tune." A conformance question now sits
in front of it — did the run that failed the gate implement the locked spec —
and on the evidence above, in at least five respects, it did not.

---
title: D-06 static-epsilon sensitivity check (confirm dual-context is safe on the admitted set)
date: 2026-06-21
priority: medium
---

# Todo: D-06 static-epsilon sensitivity check

**Carried over from specwork.** This is the one open follow-up from the v1.6 / Phase 32
adjudication of D-06 (epsilon strategy). The decision itself is **locked** — this is a
confirmation that the locked choice is safe on the real data, not a re-decision.

## The decision that was made (locked)

Two different gravitational-softening lengths live in the framework, by design:

- **`epsilon_train = 1e-5`** — softens the distance inside the **training loss** (physics
  residual + energy regularizer). It runs in float32 on GPU, where the network can output
  bodies arbitrarily close together, so it needs a real floor or the `1/r^3` gradient blows
  up to NaN. Locked (v1.6 loss contract).
- **`epsilon_inv = 1e-10`** — softens the potential only when computing **offline
  ground-truth invariants** (energy `E`, virial-like `Q`) and the data-side validation
  metric (IPR) from the Brutus trajectories in float64. Here `1e-10` is essentially "no
  softening" — that is the point: we want the diagnostics to equal the true Newtonian
  values. (`epsilon_inv = 1e-10` was already locked in v1.5, GAP-28-02.)

Owner ratified "keep dual-context" (specwork gap-register Option A = issue-doc Option B) on
2026-06-21. Sources: `pinn_instruction/issues/03-curriculum-and-training-loop.md` D-06;
`pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
§1.3 (claims EPS-01..05, DGR-04, GAP-04); specwork gap `GAP-32-03` in
`.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md`
(branch `milestone/v1.6`).

## Why this check exists (the caveat)

The two epsilons agree to ~10 digits for ordinary separations and only diverge at the
**tightest encounters**. For the per-pair potential `1/sqrt(r^2 + eps^2)` (scaled units):

| separation r | with eps=1e-10 | with eps=1e-5 | difference |
|---|---|---|---|
| 1e-3 | 1000.0 | 999.95 | ~0.005% |
| 1e-4 | 10000 | 9950 | ~0.5% |
| 1e-5 | 100000 | 70710 | ~29% |

So at close encounters (`r <~ 1e-4`) the network is **trained** against an `eps_train=1e-5`
energy but **labeled/validated** against an `eps_inv=1e-10` energy. The resolution doc flags
(EPS-05 `defer`, GAP-04 `missing_empirical_evidence`) that **no sensitivity study has
quantified this on the real dataset**. The dual-context decision was made on first-principles
+ lock-consistency grounds, not measured data, so this check confirms it.

## What to actually do (FUT-01 / trainex, once the data + processing pipeline exists)

On the admitted training set:

1. Count trajectories whose minimum pairwise separation `s_min` falls in the divergence band
   (say `r <~ 1e-3`), broken down by curriculum stage. Expect this concentrated in the
   Stage-6 near-collision tail (Stage-6 gate is `s_min < 0.5`).
2. For those trajectories, compute the offline energy `E` and the IPR under both
   `eps_inv=1e-10` and `eps_train=1e-5`, and report the distribution of the relative
   difference.
3. Confirm the difference does not move any **stage label** or trip any **validation gate**
   (the IPR flag threshold) differently — i.e., the dual-context split does not change which
   trajectories are admitted or how they are staged.

**Pass:** differences are negligible at the label/gate level → dual-context confirmed; close
the item.
**Fail:** if a material fraction of admitted trajectories shift labels/gates → reopen D-06
with the owner. The data would be saying the train-vs-validate gap is not safe to ignore, and
collapse-to-`1e-5` vs keep-dual-context would need re-weighing with evidence.

This is a verification activity (training-execution design doc §6 "Verification & Assessment
Surface"). It is **not** a spec edit and does **not** block any specwork phase.

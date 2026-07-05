---
title: Trainex r1a Decision-Adjudication — Owner Ratification Record
status: active
scope: project
purpose: verification-report
created: 2026-07-05
---

# Trainex r1a — Owner Ratification Record

On **2026-07-05** the project owner **ratified the consolidated decision set** in
`trainex-r1a-resolution-doc.md` (the filed `FINAL-RESOLUTION.md`) **as recommended**.
This satisfies trigger condition #3 of the CTL-PINN build-milestone seed
(`.planning/seeds/ctl-pinn-build-milestone.md`): *r1a decisions recorded*. All three
build-milestone triggers are now met.

## What was ratified

The unanimous / consolidated core across all rows of the resolution's §1 summary — the
engineering decisions D1..D7, B-1..B-11 — is accepted as written. Headline picks:

- PyTorch 2.12 + MPS (fp64 branch = same code on CPU); single keyed YAML config with a
  frozen resolved copy per run; `caffeinate -is` unattended-run wrapper.
- JSONL log canonical + TensorBoard secondary view; widened per-step log fields.
- D3-C in-memory fp32 preload adapter, admitted-set only, exposing `n_snapshots`/`dt_out`.
- Two-phase Adam→L-BFGS closure loop (D5-B), sampler interface (D5-E), scheduled loss
  weights (D5-H); spec stage-0 optimizer schedule (B-1); complete Adam reset at boundaries.
- Dual-trigger checkpointing (steps or wall-clock) + rolling-3/best/anchors/latest retention;
  atomic writes; Tier-1+2 guards; RECOVER seam (`recover.retries: 0`) + HALT/REVIEW family;
  always-on `failure/` diagnostic bundle.
- Dual stage-boundary anchors; manual `--hold-stage` rollback now (auto-revert deferred);
  idempotent promotion + `curriculum.jsonl`.
- B+C determinism (accepted variance + full seed/RNG record + strict-CPU debug switch);
  field-classified resume diff with fail-safe default; statistical-equivalence reproducibility.

## Carve-outs the owner resolves at their designed moments (not decided here)

- **D1-p (fp32 vs fp64):** adjudicated by running the `pinn_architecture.md` §10.3
  componentwise-AD probe dual-arm (MPS fp32 with `PYTORCH_ENABLE_MPS_FALLBACK` unset +
  fp64-CPU reference) as the first build act. Every ratified pick holds under both branches.
- **D4-a wall-clock checkpoint ceiling value:** owner pick in the r1b 15–30 min range,
  informed by the smoke test's measured s/step.
- **D4-c/R-2 RECOVER retry budget + HALT/REVIEW thresholds:** placeholders until the
  Stage-0 pilot calibrates them; then owner-ratified.
- **B-5 identity/operational resume-field list:** owner ratifies before run #1.
- **R-1 guard thresholds** (loss-explosion multiple, disk-floor GB, memory-watermark):
  remain placeholders; calibrated against Stage-0 pilot variance.

## Register items closed at ratification

- **R-3 (hardware confirmation): CLOSED.** Machine verified 2026-07-05 as **Apple M5 Pro,
  24 GB unified memory, 15-core CPU (5 performance + 10 efficiency)** (`sysctl` / About This
  Mac; model `Mac17,9`). The specs' 24 GB assumption is correct; all memory thresholds are
  set for 24 GB. In-memory dataset (~0.55 GB fp32) uses ≈2% of RAM.
- **B-8 / U-3 (ε_H gate direction):** already spec-settled (REJECT if `eps_H > 1e-5`).

## Standing

This is an owner ratification of a **build-design recommendation**, not a science-spec
verdict. `ctl_instruction.md` and `pinn_architecture.md` remain the authoritative specs and
were treated as fixed constraints. The ratified picks are recorded as project Key Decisions
in `.planning/PROJECT.md`; the build milestone follows the postspec-r1 **viability slice**
(Stage-0 first), with the full three-stream platform deferred pending a go/adjust/rethink verdict.

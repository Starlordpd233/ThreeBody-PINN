---
title: CTL-PINN build milestone (FUT-01 code rewrite ∥ training pipeline ∥ user runbook)
planted_date: 2026-06-11
trigger_condition: >
  ALL of: (1) v1.5 milestone complete (data-side contracts settled, spec edits to
  ctl_instruction.md / pinn_architecture.md applied); (2) doc-03 milestone resolved or
  user explicitly waives waiting on it (it owns training-loop usage of SCS/SASD/IPR/PSC,
  M16 collocation scaling, G6 causal training per SCOPE-11); (3) trainex-r1 resolutions
  (r1a decisions/structure + r1b runbook/ops knowledge) delivered AND the user's D1–D7
  decision-sheet picks recorded.
---

# Seed: CTL-PINN Build Milestone

The future milestone that builds the actual system. Three streams developed in parallel
with each other (user decision 2026-06-11, confirming design doc Section 10):

1. **FUT-01 — `pinn/` package rewrite from specs.** The scientific side: network,
   loss formulation, curriculum state machine, all implemented from the post-v1.5
   (and post-doc-03) framework specs. v1.3-era live code is NOT a grounding source;
   it gets replaced wholesale.
2. **Training pipeline (FUT-04 territory).** The mechanical side: dev environment,
   data ingestion (per v1.5 PIPE-XX contracts), training loop shell, verification
   layer — per the training-execution reference design.
3. **User runbook.** The non-expert-facing step-by-step workflow (setup → configure →
   launch → monitor → resume), promoted from Section 5 of the reference design once
   trainex-r1 fixes the framework and the real commands/error surfaces exist; the r1
   K1–K3 findings (health watchlist, unattended-Mac ops, runbook patterns) seed it.

## Starting inputs when triggered

- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`
  (baseline reference design from a quick 2026-06-10 brainstorm — per its 2026-06-11
  standing note a simplified starting point, NOT fundamental trainex structure;
  placeholders PH-1..PH-10 marked; subject to r1 baseline-critique revisions)
- Trainex-r1 resolution docs (r1a + r1b) + filled decision sheet (from `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/`)
- v1.5-revised framework specs (`ctl_instruction.md`, `pinn_architecture.md`)
- doc-03 outcomes (training-loop contracts)
- `.planning/notes/training-execution-parallel-work-boundary.md` (the boundary decision)

## First action when triggered

Per design doc Section 10: a fresh brainstorm/planning session producing the build plan,
with this seed and the design doc as inputs. Do NOT skip straight to code — the design
doc deliberately produced no implementation plan, and the placeholder resolutions
need to be folded into the plan first. Remaining research handoffs after trainex-r1
(which covers PH-1/PH-8/PH-9/PH-10, the structural slices of PH-7/PH-6, determinism
policy, stage-boundary mechanics, feasibility envelope, the trainer-correctness
verification ladder, and runbook research): trainex-r2 (numeric tuning of
PH-7 optimizer/LR and PH-6 collocation inside the r1a-picked skeleton) before the first
real training run; PH-5 split policy once v1.5 data contracts and dataset statistics are
in hand.

## Ratification addenda (2026-07-05)

- **Trigger #3 satisfied.** The trainex-r1a decision set is ratified (owner, as recommended)
  and recorded as Key Decisions in `PROJECT.md`; see
  `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/{trainex-r1a-resolution-doc.md, RATIFICATION.md}`.
  All three build-milestone triggers are now met. **First action** stays as written above
  (fresh planning session; do NOT skip to code) — realized here as the GSD `v1.7` milestone.
- **Scope = viability slice** (per `postspec-r1-direction-assessment.md`): Thrust A
  (data/curriculum characterization) → Thrust B (thin Stage-0 training spine as a viability
  probe) → a go / adjust / rethink verdict. The full three-stream buildout (FUT-01 science
  code + FUT-04 pipeline + operator runbook, all 7 curriculum stages, hardened resume,
  provenance) is DEFERRED until the slice's evidence warrants it. Stages 3–6 additionally
  blocked on the missing stochastic-L-BFGS implementation (U-7); a preflight refusal guard
  makes that impossible to cross silently.
- **Dataset-finalization gate first.** Before Thrust A, discharge the v1.5 forward
  obligations recorded in the v1.5 handoff (`29-HANDOFF.md` / `29-CODE-DIVERGENCE.md`):
  FO-1 (promote the 117 validatable gold + the 184→67 permanent-absent cascade) then
  FO-2 (PSC/SCR first-run sanity + SASD/IPR/PSC validation-constant recalibration +
  AC-VAL-04 numeric run). Gold is final in shape: 117 validatable + 67 permanent-absent.
- **D1-p adjudication route:** the `pinn_architecture.md` §10.3 componentwise-AD probe,
  dual-arm (MPS fp32 with `PYTORCH_ENABLE_MPS_FALLBACK` unset + fp64-CPU reference), is the
  first build act and feeds the owner's fp32-vs-fp64 call. Every ratified pick holds under both.
- **R-3 CLOSED:** hardware verified Apple M5 Pro, 24 GB, 15-core CPU (5P+10E); thresholds set
  for 24 GB. **B-5** owner-ratified before run #1. **trainex-r2** gated before the first
  production-scale run.
- **H1 hypothesis (owner provenance, 2026-07-05):** the dataset was generated with an intended
  built-in difficulty hierarchy — the hierarchical-family trajectories are dynamically simpler
  (cheaper for Brutus to integrate) than the standard/quasi-random family, so they are expected
  to concentrate in curriculum Stages 0–1 while quasi-random dominates the chaotic tail. Thrust A
  MUST compute stage membership from the measured difficulty invariants (not from set labels) and
  TEST H1; if it holds, Stage-0 viability results carry a narrow-family caveat (do not over-generalize).
- **Operational documentation layer (owner requirement, 2026-07-05):** beyond the ratified
  machine logs (canonical JSONL, always-on `failure/` bundle, frozen per-run config,
  environment fingerprint, `curriculum.jsonl`), the build must produce a human narrative layer
  for after-the-fact debugging: a per-run `summary.md` (intent · config delta vs prior run ·
  observations · verdict), a track-level run-journal index (one line per run), and dated
  investigation/forensics notes when debugging. Under GSD, phase plan/verification artifacts
  supply the process transcript for free.

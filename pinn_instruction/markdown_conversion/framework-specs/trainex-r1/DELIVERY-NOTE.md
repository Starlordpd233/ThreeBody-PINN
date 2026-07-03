---
title: Trainex R1 Delivery Note (covers sub-packages R1a and R1b)
package_for: trainex-r1 (foundational research round, split into two parallel sub-packages)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-06-11
---

# Trainex R1 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents** — it
contains repository paths and routing context that mean nothing outside the codebase. The
authored package files (masters and prompts) contain no repo paths and refer to attached
files by filename only; the `specs/` snapshots are verbatim pins of project documents and
retain internal cross-references — the masters instruct agents to treat any unattached
reference as unavailable rather than guessing.

## The split

R1 is delivered as **two parallel sub-packages with different output contracts**
(decision 2026-06-11: a single ~10-item package would cost per-topic depth in
single-prompt research agents):

- **R1a — decisions and structure** (`research_package_a/`): decision areas D1 ML
  framework, D2 tracking/monitoring, D3 compute utilization + in-memory-vs-streaming
  ingestion, D4 checkpoint/resume policy + unattended-run auto-guards + on-failure
  diagnostic bundle, D5 training-loop skeleton capabilities (structural slices of
  optimizer/collocation pulled forward from R2, plus loss-weighting machinery), D6
  reproducibility/determinism policy, D7 curriculum stage-boundary mechanics — plus the
  baseline critique mandate. Output: options menus, door classifications, decision
  sheet, composed first-run recipe.
- **R1b — runbook and operations knowledge** (`research_package_b/`): K4 training
  feasibility envelope and K5 trainer-correctness verification ladder (the two
  priorities; K5 includes the smoke-test pattern and known-solution fixtures), K1 PINN
  health watchlist, K2 unattended-Mac training operations + environment pinning/upgrade
  discipline, K3 runbook design patterns.
  Output: cited runbook-ready findings, parameterized estimates, decision-relevant
  observations.

Hand both off in parallel; they do not depend on each other mid-flight. The join happens
at consolidation (below).

## What to send to each external research agent

For **R1a**: use the R1a `RESEARCH-AGENT-PROMPT.md`. Upload four individual files
named `RESEARCH-CONTEXT-MASTER.md`, `2026-06-10-training-execution-design.md`,
`pinn_architecture.md`, and `ctl_instruction.md`, then paste the prompt below its
horizontal rule.

For **R1b**: use the R1b `RESEARCH-AGENT-PROMPT.md`. Upload four individual files
named `RESEARCH-CONTEXT-MASTER.md`, `2026-06-10-training-execution-design.md`,
`pinn_architecture.md`, and `ctl_instruction.md`, then paste the prompt below its
horizontal rule.

Repo layout is organization only — upload files individually; the agent sees only these
filenames. **Snapshots are stored once at the round root and shared by both
sub-packages** (ERW storage rule: never duplicate snapshot sets per sub-package; a
routing note like this one does the job).

## Scope notes

- **Deliberately excluded from R1:** specwork-owned science (curriculum, loss,
  architecture); PH-5 split policy (needs dataset statistics + v1.5 data contracts);
  the *numeric* tuning of PH-7 optimizer/LR and PH-6 collocation (trainex-r2, now pure
  tuning inside the skeleton R1a's D5 fixes); and **float64-necessity evidence
  gathering** — that is a specwork adjudication input for v1.5 Phase 27, and mixing it
  into a trainex package would route adjudication evidence through a channel whose
  resolutions are explicitly non-grounding. If researched externally, it runs as a
  separate EDL-style support brief through the specwork channel (decision 2026-06-11).
- **Baseline standing:** the 2026-06-10 design doc is a quick-brainstorm baseline (per
  its standing note), not fundamental structure. R1a carries the explicit critique
  mandate; R1b records structure-implying findings as decision-relevant observations.
- **Gate context:** R1 is NOT gated on the v1.5 adjudication phases. The one dependency
  edge — v1.5 Phase 27 adjudicates numerical precision — is handled by the conditional
  inside R1a's D1 menu, so nothing waits on Phase 27.

## Result delivery conventions

1. Results land per sub-package:
   `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_results/r1a/<agent>-resolution.md`
   and `.../research_results/r1b/<agent>-resolution.md`
   (e.g., `chatgpt-pro-resolution.md`, `gemini-deep-research-resolution.md`).
2. Consolidation (reusing the issue-02 consolidation workflow and bundle tooling if
   desired) produces `r1a-resolution-doc.md` and `r1b-resolution-doc.md` at this
   directory's root — or a single joined `r1-resolution-doc.md` at the user's
   discretion. **Join points to check at consolidation:** R1b's K4 duration estimate
   plugs into R1a's first-run recipe; K4's outcome range informs the D4 checkpoint-cadence
   pick and K2 thermal guidance; R1b's K1/K2 signal definitions supply the thresholds for
   R1a's D4 auto-guards; K1's divergence-after-transition signals pair with D7's
   stage-boundary mechanics; K5's verification ladder becomes the runbook pre-flight
   section and informs the test-harness skeleton; R1b's decision-relevant observations
   merge into R1a's decision menus where they overlap.
3. The **decision sheet lives in the R1a output** — the user fills it in (D1–D7 picks +
   keep/change for each proposed baseline deviation). Those picks, not the documents, are
   the decisions, recorded as project Key Decisions.
4. A single high-quality result may be promoted directly at the user's discretion — this
   is a build-design round, not a spec adjudication; the full issue-doc verification
   protocol is not mandatory.

## Standing of the eventual resolution docs

The R1 resolution docs deliver **options menus and findings, not verdicts**. They do NOT
edit framework specs and are not grounding sources for spec adjudication. Once the user's
picks land: trainex-r2 (numeric optimizer/LR + collocation tuning) becomes researchable
against the chosen framework and skeleton; the runbook v0 draft can begin from the K1–K5
findings (with K5 as its pre-flight section); and the picks + resolutions satisfy one
trigger input of
`.planning/seeds/ctl-pinn-build-milestone.md`.

---
title: Trainex r1a Decision-Adjudication — Delivery Note
package_for: trainex-r1 / decision-adjudication sub-round (build-design channel)
role: user-facing routing and provenance — NOT part of any upload to external agents
status: active
created: 2026-07-04
source_baseline: 4bbd5443 (master; v1.6 merged, tag v1.6)
---

# Trainex r1a Decision-Adjudication — Delivery Note

**User-only routing. Do NOT upload this file to any external agent** — it contains
repository paths and provenance that mean nothing outside the codebase.

## What this round is

A decision-adjudication sub-round of `trainex-r1`. It hands the already-produced **r1a
decision sheet** to 2–3 external agents in parallel; each returns a decisive resolution; a
separate consolidation agent merges them into `trainex-r1a-resolution-doc.md` — the final
picks the owner ratifies. This closes the one open precondition of the CTL-PINN build
milestone (seed trigger #3: r1a decisions recorded) and the sole deferred item from the
v1.6 audit.

**Standing:** build-design channel — **recommendation the owner ratifies. NOT a candidate
verdict source, NOT a grounding source for the science specs.**
Design blueprint: `docs/work/designs/cross_cutting/trainex-decision-research/2026-07-04-trainex-r1a-decision-research-package-design.md`.

## Provenance / baselines

- **`ctl_instruction.md`, `pinn_architecture.md` are the CURRENT authoritative specs**,
  snapshotted from `master` at commit `4bbd5443` (v1.6 merged; tag `v1.6`). They are
  **newer** than the `track/trainex` branch copies (pre-v1.6), so they were taken from
  master. sha256: `ctl_instruction.md` `a9d64200…`, `pinn_architecture.md` `e629b2fc…`.
- **Prior-round originals**, copied verbatim:
  - `chatgpt-pro-resolution.md` (`fe71a1ec…`), `trainex-r1a-options-and-decisions.md`
    (`4e26e39c…`, updated 2026-07-04 after the fix-plan edits — was `15a65a60…`) — from `trainex-r1/research_results/r1a/`
  - `trainex-r1b-findings.md` (`544fb717…`), `trainex-r1b-findings-2.md` (`b943dc50…`) —
    from `trainex-r1/research_results/r1b/`
  - `postspec-r1-direction-assessment.md` (`f57c63d5…`) — from `postspec-r1/research_results/`
  - `2026-06-10-training-execution-design.md` (`8395564c…`) — from
    `docs/work/designs/cross_cutting/training-execution/`
- All eight are gathered under this package's `attachments/` for a single-folder handoff.

## Package layout

```
pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/
  DELIVERY-NOTE.md              (this file — user-only)
  research_package/
    RESEARCH-CONTEXT-MASTER.md    (upload)
    RESEARCH-AGENT-PROMPT.md      (attach-list header + paste-below-the-rule prompt)
  consolidation/
    CONSOLIDATION-PROMPT.md       (Stage-2)
  attachments/                  (the 8 raw originals to upload)
  research_results/             (Stage-1 reports land here)
  trainex-r1a-resolution-doc.md   (Stage-2 output; lands later)
```

## Stage 1 — fan-out handoff (per agent, ×2–3)

1. Open `research_package/RESEARCH-AGENT-PROMPT.md`.
2. Attach the 9 files listed in its header — `RESEARCH-CONTEXT-MASTER.md` (from
   `research_package/`) plus the 8 originals (from `attachments/`), individually — no folders.
3. Paste everything below the horizontal rule.
4. Save each result under `research_results/` as `<agent>-decide-resolution.md`
   (e.g., `gpt-pro-decide-resolution.md`, `gemini-decide-resolution.md`,
   `claude-decide-resolution.md`) — note the `-decide-` tag so these are not confused with
   the r1a-round `chatgpt-pro-resolution.md` attachment.

## Stage 2 — consolidation

1. Use `consolidation/CONSOLIDATION-PROMPT.md`.
2. Attach the 2–3 Stage-1 results **plus the same 8 originals** (so the consolidator can
   adjudicate disagreements against the sources).
3. Run on one distinct agent (independence).
4. Save the output as `trainex-r1a-resolution-doc.md` at this package root.

## Carve-outs the owner resolves separately (NOT in this package's scope)

- **D1-p precision (fp32 vs fp64):** route as a specwork/precision question, or run the
  `pinn_architecture.md` §10 numerical probes in fp32 first (empirical). The agents were
  told to keep recommendations valid under both branches.
- **B-8 ε_H gate direction — RESOLVED (2026-07-04):** the attached `ctl_instruction.md`
  (lines 550–555) defines the gate unambiguously as REJECT if `eps_H > 1e-5` (smaller passes),
  `eps_H = 0 → Excellent`. The "contradiction" was an inverted-looking example in the baseline
  design doc's §6.3 (r1b flags it as C-12) — a display typo, not a locked-metric issue; no
  STOP-protocol gap remains. The package reflects this (sheet §8 B-8, §10 decision row,
  register U-3 closed).

## Afterwards

Ratify `trainex-r1a-resolution-doc.md` → record the picks as project **Key Decisions** →
the build milestone's trigger #3 is met. Build scoping then follows the viability slice
(Stage-0 first), per `postspec-r1-direction-assessment.md`.

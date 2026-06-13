---
title: Integrity R1 Delivery Note
package_for: integrity-r1 (framework integrity audit round)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-06-12
source_baseline: 55ab6e4bfba0ada4f8ab48539d2385905d594e8a
---

# Integrity R1 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents** — it
contains repository paths and routing context that mean nothing outside the codebase.
The authored package files (master, prompt, `DATASET-CONTEXT.md`, and the bundle's
authored framing) contain no repo paths and refer to attached files by bare filename
only; the `specs/` snapshots and the bundle's three embedded documents are verbatim pins
of project documents and retain internal cross-references — the master instructs agents
to treat any unattached reference as unavailable rather than guessing.

## What this round is

A **disruption-first integrity audit** of the three framework specs as a whole —
coherence, buildability, mathematical/physics correctness, scientific soundness, and
load-bearing assumptions — commissioned before build-out so that disruptive findings
surface while change is cheap. Single package, multi-AI fan-out (same prompt to several
agents). Review dimensions RD-1..RD-8 with hardened output contract: per-section
coverage matrix over every H1/H2 of every spec, shared severity rubric (S1–S4),
evidence-class labels, novelty classification, constants concordance, and a
consolidated minimum-decision-list in the project's gap-register A/B/C format.

## What to send to each external research agent

Per `research_package/RESEARCH-AGENT-PROMPT.md` — attach these 6 files individually (no
folders; the agent sees filenames, not directories), then paste everything below that
file's horizontal rule:

1. `research_package/RESEARCH-CONTEXT-MASTER.md`
2. `specs/ctl_instruction.md`
3. `specs/pinn_architecture.md`
4. `specs/sampling_method.md`
5. `research_package/DATASET-CONTEXT.md`
6. `research_package/KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md`

The `specs/` snapshots are stored once at this round root (ERW storage rule) and are
byte-identical copies of the three live framework specs at commit `55ab6e4b` (the
`source_baseline` in the master's frontmatter). The `ctl_instruction.md` snapshot was
**refreshed 2026-06-13 to HEAD** after Phase 26 landed its DataLoader ingestion/selection
contracts (snapshot-refresh note below); `pinn_architecture.md` and `sampling_method.md`
are unchanged since the original pin (0 commits since `32a9aa76`). Snapshot SHA-256:

- `ctl_instruction.md` — `3e3d1955aba2b2721ec59ae4da2ed201e4e942d7b295170f768583f4f74d7dff`
- `pinn_architecture.md` — `ae29753dc10a61c1bfa47a0683ebbd991b8ee9b4b86ef09c28d6463adc712507`
- `sampling_method.md` — `750e625efa51767eed0371dc4d6ee73d598fbd77c98592cef18bce5fc84f6f07`

## Standing of the eventual report

**Findings register — NOT a candidate verdict source, NOT a grounding source.** No
finding edits a spec on the report's authority. Findings feed user triage into future
milestones (the issue-03 round, post-v1.5 spec work); `against-in-flight-edit` findings
route to the still-pending owning v1.5 phase (27/28) for consideration there; findings on already-landed Phase-26 contracts route to Phase 29 acceptance or a Phase-26 reopen. This keeps the
CLAUDE.md adjudication governance unambiguous: the v1.5 candidate verdict source remains
the issue-02 resolution doc, not this audit.

## Timing acknowledgment (user-confirmed 2026-06-12; ctl snapshot refreshed 2026-06-13)

v1.5 Phases 26–28 edit `ctl_instruction.md` and `pinn_architecture.md` as issue-02
adjudication applies fixes. **Phase 26 landed on 2026-06-13** (DataLoader
ingestion/selection contracts: B-06 admission gate, B-11 id-resolution, M11 blacklist
exclusion, D7 footer/parameter heterogeneity, M13 gold-counterpart, D-03 HDF5 format);
its edits are now part of the refreshed `ctl_instruction.md` snapshot and are audited as
live spec text. Phases 27–28 (sampling/precision/global-scale; validation-metric
data-side definitions) remain pending. The audit is sent now anyway — the in-flight
register inside the bundle plus the mandatory novelty classification absorb the remaining
overlap; disruption surfaced now is more useful than serialized-later disruption. The
agents audit the pinned snapshots as attached; any finding overlapping a still-pending
in-flight topic arrives tagged `against-in-flight-edit`.

## Scope notes

- **Deliberately excluded:** trainex-r1 topics (framework pick, feasibility, ops — the
  agents are told to note interactions in blast radius, not answer them); runtime
  feasibility estimation; producing spec edits (the output is findings + a
  minimum-decision-list, never edited spec text).
- **Rejected attachments (for the record, so they are not reconsidered):** raw
  `simulation_data/Documentation/README.md` (re-imports claimed-unverified figures the
  curated `DATASET-CONTEXT.md` is designed to police); `data_quality_assessment.md`
  standalone (already embedded in the bundle behind its authority banner);
  `ctl_pinn_resolution.md` (would anchor the agent toward accepting v1.4 decisions it
  should be stress-testing — its locked outcomes are carried as Tier-2
  decisions-of-record in the master instead).
- **DATASET-CONTEXT recency:** authored against the post-remediation dataset state. The
  GAP-24-01 / DATA-05 70-file quarantine was executed, validated, and closed 2026-06-11
  (post-swap probe 0/15,028 mismatches; hierarchical footer-less count now 1,480), so
  the package records the full resolved lifecycle rather than an open quarantine; the
  "Figures that moved" table in `DATASET-CONTEXT.md` maps the stale figures that still
  appear inside the bundle's embedded docs to current values.

## Result delivery conventions

1. Results land at
   `pinn_instruction/markdown_conversion/framework-specs/integrity-r1/research_results/<agent>-resolution.md`
   (e.g., `chatgpt-pro-resolution.md`, `gemini-deep-research-resolution.md`).
2. **Stage-2 consolidation is a follow-up artifact authored when results land** (the
   issue-02 consolidation workflow and bundle tooling under
   `framework-revisions/research_reports/02-data-pipeline-and-validation/consolidation_input/`
   are reusable). Consolidated output: `integrity-r1-resolution-doc.md` at this round
   root.
3. **Consolidation join points:** stable finding IDs (`INT-NNN`) are per-agent — the
   consolidation must dedupe by (spec section × claim), not by ID; the severity rubric,
   novelty classes, and evidence classes are shared across agents and are the
   comparison axes; each agent's §3 coverage matrix shows which spec sections any given
   agent actually audited (coverage union and coverage holes are first-class
   consolidation outputs); §6 minimum-decision-lists merge into a single deduped
   decision list in the gap-register A/B/C format.
4. After consolidation: user triage routes findings to v1.5 phases
   (`against-in-flight-edit`), the future issue-03/doc-03 milestone (curriculum and
   training-loop findings), post-v1.5 spec work, or rejection — recorded per the
   project's adjudication machinery. The registry row in
   `.planning/research/questions.md` tracks round status.

## Bundle assembly verification log (V1–V6, run 2026-06-12)

Per the round's mandatory Bundle Assembly Procedure:

- **V1 byte-fidelity — PASS.** SHA-256 of each embedded block (content between its
  4-backtick fence lines, exclusive) vs. the project source file:
  - `data_quality_assessment.md`: embedded `90ad2df142ec90c6…` = source
    `90ad2df142ec90c6…` ✓ (full: `90ad2df142ec90c687b2ca634948c9086fa853807223dc884dc8ca3e2caa7437`)
  - `02-resolution-doc.md`: embedded `b8cfab704bdc66e7…` = source
    `b8cfab704bdc66e7…` ✓ (full: `b8cfab704bdc66e74c7b7909a3ef2a020e454272f94275c1889a5cbe32fbd66e`)
  - `03-curriculum-and-training-loop.md`: embedded `94c3c03b1323847e…` = source
    `94c3c03b1323847e…` ✓ (full: `94c3c03b1323847eea84233bd29dddba8cf4b32b7dd08ecb0af52cdba4ad1d3a`)
- **V2 authority-banner presence — PASS.** All three banners present with the exact
  wording templates (BANNER-1 NON-AUTHORITATIVE / BANNER-2 CANDIDATE VERDICTS UNDER
  ADJUDICATION / BANNER-3 UNADJUDICATED CRITIQUES), one per embedded doc.
- **V3 in-flight register recency — PASS (re-checked 2026-06-13 after Phase 26 landed).**
  Originally checked 2026-06-12 against `.planning/ROADMAP.md` (v1.5 section),
  `.planning/milestones/v1.5-GAPS.md`, and the phase-25/26 artifacts. Re-checked
  2026-06-13: Phase 25 complete (machinery + three EVID-10 conflict records:
  `scs-thresholds.md`, `compute-globals-D.md`, `m11-m12-severity.md`); **Phase 26 now
  complete** — its 7 spec commits (`b1852b0f`..`ab5f7f06`) landed the DataLoader
  ingestion/selection contracts in `ctl_instruction.md`, the snapshot was refreshed to
  HEAD `55ab6e4b`, and the register's Phase-26 row was updated from "planned" to
  "landed"; Phases 27–29 not started. The register lists exactly these states and topics;
  no closed topic is listed as open and no landed topic is listed as pending.
- **V4 trainex-r1 register recency — PASS.** Checked against both trainex-r1 masters
  and `.planning/research/questions.md`: D1–D7 (package a) + K1–K5 (package b),
  PACKAGE-READY awaiting handoff, no decisions adopted. Register matches.
- **V5 cross-reference check — PASS (with two recorded notes).** Every path-like
  reference inside the embedded docs resolves to an existing file when resolved against
  the referencing document's home location: the resolution doc's `specs/*` and
  `probes/*` references resolve to the issue-02 package `research_package/specs/` and
  the Phase-24 `probes/` directory respectively (all exist); issue-03's relative
  references to `pinn/` and the framework specs all resolve. Notes: (i) issue-03's
  self-reference uses its pre-relocation prefix `issues/…` (file now lives under
  `pinn_instruction/issues/…`) — the target exists and is the embedded doc itself;
  (ii) embedded docs reference package-internal bare filenames that are deliberately
  not attached to this round (e.g., the issue-02 issue doc) — the master's
  treat-unattached-as-unavailable instruction covers these.
- **V6 no-anchor-points — PASS.** Scanned all authored upload text (the bundle's
  manifest/register/banners outside the verbatim fences, the master, the prompt,
  `DATASET-CONTEXT.md`) for repo path patterns, git-log/commit references, Cursor-plan
  references, and phase plan IDs: zero hits. The verbatim embedded documents and
  `specs/` snapshots are exempt per ERW rule 1 (byte-pins are never scrubbed; the
  master handles their internal references via the unavailable-reference instruction).

## Handoff quick reference

1. Open `research_package/RESEARCH-AGENT-PROMPT.md`; attach the 6 files in its header
   (individually); paste everything below the horizontal rule.
2. Repeat across external agents in parallel (multi-AI fan-out).
3. Save each result as `research_results/<agent>-resolution.md` under this round root.
4. When results are in, request the Stage-2 consolidation prompt (follow-up artifact;
   issue-02 consolidation tooling reusable), producing `integrity-r1-resolution-doc.md`.

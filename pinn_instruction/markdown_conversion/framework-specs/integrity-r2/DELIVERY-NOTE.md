---
title: Integrity R2 Delivery Note
package_for: integrity-r2 (pre-build framework integrity audit round)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-07-07
source_baseline: 23a6273cfe21b487f4a6177e0033360c6d1072f5
---

# Integrity R2 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents** — it
contains repository paths and routing context that mean nothing outside the codebase. The
authored uploads (the STORM prompt and `DATASET-CONTEXT.md`) contain no repo paths and
refer to attached files by bare filename only; the six `specs/` snapshots are verbatim
pins of project documents and retain internal cross-references — the prompt (§1, §9)
instructs the agent to treat any unattached reference as unavailable rather than guessing.

## What this round is

A **disruption-first, adversarial pre-build integrity audit** of the locked CTL-PINN
framework foundation — the three framework specs, the v2.0 roadmap (Phases 37–43), and the
ratified trainex-r1a build decisions — run **once, before v2.0 Phase 37** (the project's
first *build* milestone). Unlike advisory integrity-r1, integrity-r2 is a **pre-build
gate**: Phase 37 does not start until every *serious, proven* problem is fixed or waived by
the owner with a recorded reason. The agent decides nothing; it produces findings plus a
recommended GO / NO-GO / GO-WITH-CONDITIONS verdict, and the owner disposes.

Single research package, multi-AI fan-out (same prompt to 2–3 capable agents in parallel).
The design is the STORM four-phase method (multi-perspective question-asking → contradiction
map → synthesis → self-critique) with STORM's retrieval limb re-attached to the closed
corpus of attached files. Skill flow that produced this round:
**grilling → adapting-storm-research-prompts (the prompt) → ERW runbook (this package).**

## What to send to each external research agent

Per `research_package/RESEARCH-AGENT-PROMPT-STORM.md` — attach these **7 files individually**
(no folders; the agent sees filenames, not directories), then paste everything **below the
horizontal rule** in the prompt (the research-context master is folded inline, so there is
no separate master to attach, and no known-issues bundle is attached this round):

| # | Attach (bare filename the agent sees) | Repo location to attach from |
|---|---|---|
| 1 | `ctl_instruction.md` | `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/specs/ctl_instruction.md` |
| 2 | `pinn_architecture.md` | `…/integrity-r2/specs/pinn_architecture.md` |
| 3 | `sampling_method.md` | `…/integrity-r2/specs/sampling_method.md` |
| 4 | `v2.0-build-plan.md` | `…/integrity-r2/specs/v2.0-build-plan.md` |
| 5 | `trainex-r1a-resolution-doc.md` | `…/integrity-r2/specs/trainex-r1a-resolution-doc.md` |
| 6 | `RATIFICATION.md` | `…/integrity-r2/specs/RATIFICATION.md` |
| 7 | `DATASET-CONTEXT.md` | `…/integrity-r2/research_package/DATASET-CONTEXT.md` |

The prompt file itself (`research_package/RESEARCH-AGENT-PROMPT-STORM.md`) is **not**
attached — its below-the-rule body is pasted into the conversation. Files 1–6 live once in
this round's shared `specs/` snapshot set (the ERW one-snapshot-set-per-round storage rule);
`specs/` here holds both the three framework specs and the three build-plan/decision
snapshots, all verbatim pins.

## Snapshot provenance and byte-fidelity pins

All six `specs/` files are verbatim pins. Snapshots 1, 2, 3, 5, 6 are byte-identical copies
of the committed source blob (`git show <commit>:<path>`); snapshot 4 (`v2.0-build-plan.md`)
is a verbatim excerpt of `.planning/ROADMAP.md` from the `## 🚧 v2.0 CTL-PINN Training
Viability Slice (Executing)` heading (line 34) through end-of-file (line 189) — the v2.0
milestone section, which is exactly the build plan under audit. `source_baseline` (this
round's packaging reference) is master `23a6273c`.

| File | Source | Source commit | SHA-256 of snapshot |
|---|---|---|---|
| `ctl_instruction.md` | `…/framework-specs/ctl_instruction.md` | `34ca3473` (2026-06-29) | `a9d642006eaa45bfdc818ed612edb08a122d467620b0f8f1bf56fe0a84b8e150` |
| `pinn_architecture.md` | `…/framework-specs/pinn_architecture.md` | `583a010f` (2026-06-29) | `e629b2fc444317f71cba0fc9e7e9ba75bf18981fc235b9ba4d25acfe681b6dbd` |
| `sampling_method.md` | `…/framework-specs/sampling_method.md` | `916d3f84` (2026-06-07) | `750e625efa51767eed0371dc4d6ee73d598fbd77c98592cef18bce5fc84f6f07` |
| `v2.0-build-plan.md` | `.planning/ROADMAP.md` L34–EOF (lines 34–189, excerpt) | `23a6273c` (2026-07-06) | `eb0e804b8600000fdccfa5339d1d75d31afc827e1eb6802f91335ebbb272e34d` |
| `trainex-r1a-resolution-doc.md` | `…/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` | `a0f67b84` (2026-07-05) | `b4f66bc8292509097ea80d1244aa66a92baf8cb3240d909c2c1a42da35fe9f48` |
| `RATIFICATION.md` | `…/trainex-r1/decision-adjudication/RATIFICATION.md` | `a0f67b84` (2026-07-05) | `6bd0e729714f0a7c1be673695504e4619e5f190c46e6b4f81b974466c78cb112` |

`sampling_method.md` is unchanged since integrity-r1 (identical SHA `750e625e…`);
`ctl_instruction.md` and `pinn_architecture.md` carry their v1.5/v1.6 edits (new hashes).
`DATASET-CONTEXT.md` is an authored curated transcription (not a verbatim pin); its verified
figures are re-confirmed against the live dataset on 2026-07-07 (see the V4 log below).

To re-verify any pin:
`git show <source_commit>:<source_path> | shasum -a 256` (snapshots 1–3, 5–6), or
`git show 23a6273c:.planning/ROADMAP.md | sed -n '34,$p' | shasum -a 256` (snapshot 4).

## Standing of the eventual report

**Recommendation, owner-disposed — a pre-build gate, not an agent veto.** The report's
verdict and punch-list are the agent's view at delivery; the owner clears each Serious,
proven problem (fix or record a waiver reason) before Phase 37 starts. This preserves the
project's standing rule that external research is a *candidate*, never an authority.
Per the OUTPUT-CONTRACT: the verdict is a snapshot; the pre-build punch-list is the living
record — a later reader checks whether the punch-list was subsequently cleared, and a stale
NO-GO on an already-fixed problem is not binding. Findings that touch a spec route to a
future spec milestone (specs are read-only inputs to v2.0); build-plan/decision findings
route to the v2.0 roadmap or the trainex build.

## Scope notes

- **No separate research-context master.** The master is folded inline into the STORM prompt
  below the horizontal rule (trainex-r1 consolidated style). Do not author or attach one.
- **No known-issues / in-flight bundle** (an integrity-r1-style bundle) is attached, so the
  prompt drops the `new / already-known` novelty tag (owner-overridable). integrity-r1
  remains the read-only template — do not edit it.
- **Owner carve-outs are not defects.** `RATIFICATION.md` records five deliberately-deferred
  decisions (D1-p precision; D4-a checkpoint wall-clock ceiling value; D4-c RECOVER retry
  budget + HALT/REVIEW thresholds; B-5 resume-field list; R-1 guard thresholds) and the `⚖`
  placeholders. The prompt (§4) tells the agent these are known-open, not gaps.
- **The dataset is frozen.** Any direction requiring data regeneration beyond the
  already-authorized missing-184 standard-gold rerun is a one-way door and out of scope for
  the punch-list (side-list only). The missing-184 rerun is staged, not promoted (see V4).

## Result delivery conventions

1. Results land at
   `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/research_results/<agent>-integrity-r2.md`
   (e.g., `chatgpt-integrity-r2.md`, `gemini-integrity-r2.md`, `fable-integrity-r2.md`).
   Request one polished, PDF-ready Markdown report from each agent, in the §7 report shape.
2. Optional multi-AI consolidation is a follow-up artifact authored when results land;
   consolidated output would be `integrity-r2-resolution-doc.md` at this round root. (The
   audit's deliverable is findings + a recommended verdict, not a spec edit.)
3. **Owner disposition** of each Serious finding (fix / waive-with-reason) is what clears the
   Phase-37 pre-build gate; record dispositions where the milestone tracks them.

## Package assembly verification log (V1–V6, run 2026-07-07)

- **V1 byte-fidelity — PASS.** Each of the six `specs/` snapshots was generated from
  committed state and its SHA-256 re-checked. Snapshots 1–3, 5–6 equal their source blob
  hash exactly (`git show master:<path>`); snapshot 4 equals the `.planning/ROADMAP.md`
  L34–EOF (lines 34–189) excerpt hash (`eb0e804b…`). All hashes are recorded in the pin table above (in
  committed state), so every claim is re-derivable.
- **V2 attach-list ↔ package consistency — PASS.** The prompt's 7-file attach header
  (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `v2.0-build-plan.md`,
  `trainex-r1a-resolution-doc.md`, `RATIFICATION.md`, `DATASET-CONTEXT.md`) matches the seven
  packaged files one-to-one — no missing or extra attachment. The prompt correctly instructs
  "no separate context-master; no known-issues bundle."
- **V3 spec coverage-table consistency — PASS.** The prompt's Part-4 check-everything tables
  enumerate the H1/H2 headings of each spec by line number. Verified against the snapshots:
  `ctl_instruction.md` = 27 headings at the exact listed lines; `sampling_method.md` = 12
  headings at the exact listed lines; `pinn_architecture.md` = 25 true H1/H2 headings at the
  exact listed lines once the 15 `#`-prefixed code-comment lines inside fenced blocks are
  excluded (as the prompt's Part-4 note specifies). No heading drift.
- **V4 build-decision & dataset currency — PASS.** trainex-r1a decisions ratified 2026-07-05
  (`RATIFICATION.md`, machine confirmed Apple M5 Pro / 24 GB / 15-core, `Mac17,9`); the three
  specs are locked through v1.6. Dataset folder counts re-confirmed on-disk 2026-07-07:
  `brutus_hierarchical` 4,857 · `brutus_hierarchical_gold_standard` 4,857 ·
  `brutus_standard_quasi_random` 2,749 · `brutus_standard_quasi_random_gold_standard` 2,565
  (total 15,028) — unchanged since the 2026-06 probes. Blacklist 65 IDs (2 hier + 63 std).
  Missing-184 standard-gold rerun: all 184 outputs staged, validation 117 pass / 67 fail,
  **none promoted** (live gold count still 2,565) → recorded as `active-staged-remediation`.
- **V5 constants cross-check — PASS.** The load-bearing constants the prompt asserts (§4
  Tier-2 and the Part-5 seeded numbers table) were verified against the snapshot text:
  raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` with the mass-fraction `≈ 6.694` explicitly rejected
  (`ctl_instruction.md`); training softening `ε_train = 10⁻⁵` and the dual-epsilon validation
  softening `ε_inv = 10⁻¹⁰` (`pinn_architecture.md` §3.2 dual-epsilon note; `ctl_instruction.md`
  Step-1A); screening gate `ε_H = max_t|(H(t)−H(0))/H(0)|`, `SCS = log₁₀(ε_H)`, reject if
  `SCS > −5` ⇔ `ε_H > 10⁻⁵` (`ctl_instruction.md`); energy-regularizer floor
  `ε_H = 1e-4·S_H`, `S_H = median_train(K0 + Uabs0)` (`pinn_architecture.md` §3.4); 14D input
  `[τ, IC₁₃]`, `τ = 2u − 1`, raw ordered masses. No misstated constant.
- **V6 no-anchor-points in authored uploads — PASS.** Scanned the two authored uploads (the
  prompt's below-the-rule body and `DATASET-CONTEXT.md`) for repo-path patterns, git-commit
  tokens, and phase-plan IDs: zero hits below the paste line. (The prompt's YAML frontmatter,
  above the paste boundary, is not uploaded; a lone decimal `10.000000000000007` in
  `DATASET-CONTEXT.md` is a numeric value, not a hash.) The six verbatim `specs/` snapshots
  are exempt per ERW rule 1 (byte-pins are never scrubbed; the prompt handles their internal
  references via the treat-unattached-as-unavailable instruction).

## Handoff quick reference

1. Open `research_package/RESEARCH-AGENT-PROMPT-STORM.md`; attach the 7 files listed in its
   header (individually — no folders); paste everything below the horizontal rule.
2. Run the same package on 2–3 capable agents in parallel (multi-AI fan-out); request one
   polished PDF-ready Markdown report each, in the §7 report shape.
3. Save each result as `research_results/<agent>-integrity-r2.md` under this round root.
4. Owner disposes of each Serious, proven finding (fix or waive-with-reason) to clear the
   Phase-37 pre-build gate; optional consolidation → `integrity-r2-resolution-doc.md`.

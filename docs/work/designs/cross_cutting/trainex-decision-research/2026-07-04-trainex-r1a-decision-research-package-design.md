---
status: active
purpose: design
created: 2026-07-04
milestone: untracked
phase: cross-cutting
retirement_trigger: superseded once the trainex-r1a decision-adjudication package is assembled, handed off, its results land, are consolidated, and the r1a decision sheet is filled into recorded Key Decisions
---

# Design — Trainex r1a Decision-Adjudication Research Package

**Date:** 2026-07-04
**Track:** trainex (ERW build-design channel)
**Standing of this doc:** design intent. It specifies the package to build; it does not
assemble it. Assembly (ERW GATHER + PACKAGE) is the next step, in the `track/trainex`
worktree.
**Author role:** in-repo packaging agent — gathers context and specifies the package;
does **not** adjudicate the science or make the picks.

---

## 1. Purpose and context

Specwork is complete (v1.4–v1.6; framework specs authoritative on `master`). The
**trainex-r1 foundational round** was delivered but its **r1a decision sheet was never
filled in** — the sole unmet precondition in the `ctl-pinn-build-milestone` seed (trigger
#3) and the sole deferred item in the v1.6 close-out audit.

The r1a output presents **7 core build decisions (D1–D7)** plus **baseline-review tweaks
(B-1..B-11)**, each with a *suggested default* and a one-way/two-way door classification.
The owner will route this decision sheet, with full context, to external research and
expects back a **decisive resolution** — a clear recommended decision per item, in the
style of the specwork resolution docs (`ctl_pinn_resolution.md`, `02-resolution-doc.md`) —
which the owner will adopt as the default choice and ratify.

This document specifies that package and its two-stage workflow.

## 2. Verdict and guardrails

Routing this to external research is **on-pattern for the ERW build-design channel.** Three
guardrails, all mandated by the ERW runbook and/or r1a's own text:

- **G1 — Decisive form, owner-ratified standing.** The resolution may be as decisive as a
  specwork resolution doc (one clear pick per item), and the owner will adopt it by
  default. But governance standing stays build-design: the picks become decisions **when
  the owner ratifies them** (recorded as Key Decisions). The prompt still instructs the
  agents to *recommend decisively, flag confidence, and never assert final authority.* The
  owner keeps free deviation on preference/empirical rows.
- **G2 — Carve out D1-p (precision branch).** The ERW channel-separation rule is explicit
  and uses this exact example: *"precision-contract evidence must never be folded into a
  build-design package — route it as a separate EDL-style support brief through the
  specwork channel."* fp32-vs-fp64 ships here as **read-only context only**; recommendations
  must hold under both branches; it is settled empirically (the spec's §10 probes) or via
  specwork — never by this package.
- **G3 — Carve out B-8 (ε_H gate direction).** r1a marks it "owner-only … locked metric;
  owner must state." A locked-metric contradiction is spec territory. Ships as context
  only; the owner resolves it against spec intent (or logs a STOP-protocol gap).

## 3. Channel and standing

| Property | Value |
|---|---|
| ERW channel | **build-design (trainex)** |
| Output form | **Decisive resolution doc** — clear pick per item, specwork-resolution-doc style |
| Report standing | **Recommendation the owner ratifies.** NOT a candidate verdict source; NOT a grounding source for spec adjudication; does NOT enter a verification milestone. |
| Decision authority | The **owner**, by ratifying the consolidated resolution → recorded Key Decisions. |
| Unblocks | `ctl-pinn-build-milestone` seed trigger #3 → build scoping (per postspec-r1, a thin Stage-0 viability slice first). |

## 4. Scope

**In scope — a recommended decision is requested for each:**
D1 (framework), D2 (tracking/monitor), D3 (data residency), D4-a/b/c/d, D5-a/b/c,
D6 (determinism), D7-a/b/c/d, and baseline tweaks B-1, B-2, B-3, B-4, B-5, B-6, B-9, B-10,
B-11.

**Carved out — context only, NOT decided by this package:**

| Row | Why carved out | How it is handled instead |
|---|---|---|
| **D1-p** precision (fp32 vs fp64) | Specwork/precision adjudication; channel separation forbids it in a build-design package (ERW rule) | Read-only context; recommendations hold under both branches; settled via the spec's §10 probes or the specwork channel |
| **B-8** ε_H gate direction | Locked-metric contradiction; spec territory; r1a offers no option | Owner resolves against spec intent, or logs a STOP-protocol gap |

## 5. Workflow — two stages (fan-out → consolidation)

Mirrors the specwork rounds (multi-agent reports → consolidation → resolution doc).

**Stage 1 — Adjudication fan-out.** The package is handed to **2–3 external research
agents in parallel**. Each returns its own decisive resolution over the in-scope rows,
landing as `research_results/<agent>-resolution.md`.

**Stage 2 — Consolidation.** The 2–3 individual resolutions, **plus the same raw grounding
originals**, are handed to a **final consolidation agent**, which produces one
`trainex-r1a-resolution-doc.md` — the **final ultimate decision per item**, explicitly
noting where the source agents agreed vs diverged and resolving conflicts with rationale.
Divergence across agents is signal: rows where they disagree are flagged low-confidence for
the owner's closer look. (The issue-02 consolidation bundle tooling — `make_bundles.py`,
bundle manifest — is reusable for assembling the Stage-2 input.)

The owner then ratifies `trainex-r1a-resolution-doc.md` → the picks become Key Decisions.

## 6. Package contents — raw originals only (ERW structure)

Per the ERW runbook, the round root contains a user-only `DELIVERY-NOTE.md`, one shared
commit-pinned `specs/` snapshot set, `research_package/` (RESEARCH-CONTEXT-MASTER +
RESEARCH-AGENT-PROMPT), and a `research_results/` landing folder. **No repo paths appear in
any uploaded file; companion files are referenced by bare filename via a manifest table;
the agent is told it works from attached files only.**

**Grounding: attach full original files — create no new condensed docs.** ERW already
requires the `specs/` snapshots to be *verbatim, commit-pinned copies*, so "raw originals"
is the native rule. The only authored files are the ERW entry points below (orientation,
manifest, framed questions, output contract — not condensations of the grounding content).

| Attachment (bare filename at upload) | Role | Grade |
|---|---|---|
| the raw r1a report (`chatgpt-pro-resolution.md`, full 119 KB) | Full-depth r1a decision content — the object being adjudicated | prior-round original |
| the r1a options/decisions doc (existing) | Structured decision sheet + door table companion | prior-round original (existing; not newly condensed) — include unless owner wants pure-raw |
| `ctl_instruction.md` (full) | Curriculum + training-loop science | **hard constraint** |
| `pinn_architecture.md` (full) | Architecture, AD contract, §10 acceptance probes | **hard constraint** |
| the training-execution design doc (full) | Pipeline baseline the menus critique; also carries the hardware/operator constraints (§2.1) | **baseline intent** (challengeable; carries its standing note) |
| the postspec-r1 direction assessment (full) | Viability-slice strategy → which picks are needed now vs deferred | strategy advisory (context) |
| the trainex-r1b findings (both files, full) | Ops knowledge closing the ⚖ rows (D4 guard thresholds; D7-c signal) | knowledge findings (context) — see Q3 |

**Size note:** this is a large bundle (~500 KB+ of originals). Deep-research agents handle
it, but some have attachment-count/size limits — the delivery note will give a priority
order if an agent can't take everything.

> **Note (2026-07-07):** the ERW runbook (Rule 15, `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`)
> has since established a hard cap of **5 attachments per sub-package**. This design
> doc's 7-attachment manifest table (§6) predates that rule; the r1a assembly
> (still in flight; r1a audit completed 2026-07-04) applies Rule 15 — e.g. bundle
> the two r1b files together with the training-execution design doc and the
> postspec-r1 direction assessment into one combined context attachment, then ship
> ≤ 5 to each agent. The "priority order" fallback in the §6 size note remains
> valid as a contingency.

## 7. Output contract (per agent, Stage 1)

The agents adjudicate an EXISTING decision set; they do not regenerate the option space.
For **each in-scope row**, return:

- **Recommended decision** (decisive).
- **Endorse or override** r1a's suggested default, with explicit reasoning.
- **Confidence** (High/Medium/Low) + the single biggest uncertainty.
- **Cross-decision consistency** — the picks must form one coherent SET (D1 gates
  D2/D3/D5; note where a pick forces another).
- **Viability-slice timing** — needed for the thin Stage-0 first step, or safe to defer.
- **Flag** rows that are genuinely owner-preference (risk tolerance) or empirical (need a
  probe) rather than research-decidable.

Plus, once per report: an **updated composed first-run recipe** (coherence check); a
**claims-and-uncertainty register** (record silence; never invent); and an explicit
restatement that this is a **recommendation the owner ratifies — not a spec-grounding
source**, and that D1-p and B-8 are out of scope.

The Stage-2 consolidation prompt asks for the same per-row fields, resolved to a single
decision, plus an inter-agent agreement/divergence note per row.

## 8. Result landing and afterwards

- Stage-1 reports: `research_results/<agent>-resolution.md`.
- Stage-2 output: `trainex-r1a-resolution-doc.md` (the final ultimate decision).
- The owner ratifies → picks recorded as **project Key Decisions** → closes seed trigger #3.
- Build scoping then proceeds as the viability slice (Thrust A data/curriculum
  characterization → Thrust B thin Stage-0 probe), per postspec-r1.

## 9. Open questions for the owner

**Resolved this round:**
- **Multi-agent:** 2–3 in parallel, then a separate consolidation agent (§5). ✅
- **Raw originals:** attach full original files; no newly-created condensations (§6). ✅
- **Output form:** decisive resolution doc, specwork-resolution style (§3). ✅

**Still open (I will not silently decide these):**

1. **Round name / root.** Not a new foundational round and must **not** be `trainex-r2`
   (reserved for numeric tuning). Proposal: root it in the existing `trainex-r1/` round as
   a decision-adjudication sub-package whose consolidated output is
   `trainex-r1a-resolution-doc.md`. Confirm or rename.
3. **r1b in-package or pointer?** Include the full r1b findings so the ⚖ rows (D4 guards,
   D7-c signal) close in one pass — recommended — or reference them and let those rows
   return "pending r1b join"?
5. **Confirm the D1-p and B-8 carve-outs** (G2/G3) and how you intend to resolve each.
6. **Commit-pin baseline** for the `specs/` snapshots — I'll pin to the current baseline at
   assembly time; no action needed unless you want a specific commit.
7. **Consolidation agent:** a 4th distinct agent, or one of the Stage-1 three? (Minor;
   default to a distinct agent for independence.)

## 10. Next steps

On approval (and the Q1/Q3/Q5/Q7 answers): assemble the package in the `track/trainex`
worktree per ERW GATHER + PACKAGE — write the context-master, the paste-ready prompt, the
delivery note, and the commit-pinned verbatim snapshots — plus a short Stage-2
consolidation prompt. Then you hand off Stage 1 to your 2–3 agents, land their reports, and
run Stage 2. This doc is the blueprint for that assembly.

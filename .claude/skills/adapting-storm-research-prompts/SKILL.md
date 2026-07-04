---
name: adapting-storm-research-prompts
description: Use when building or revising an external research-agent prompt for this project (an ERW package, a trainex or specwork research round) with the Stanford STORM method or any multi-perspective / persona-based research structure — e.g. a request to "apply STORM", "research from multiple perspectives", or run source-grounded expert personas over attached files.
---

# Adapting STORM Research Prompts

## Overview

The popular "STORM in 4 prompts" chat template (Nav Toor / @heynavtoor, adapting Stanford
STORM) **deletes STORM's retrieval limb** — it runs on the model's own knowledge and writes a
generic Wikipedia/CEO-style briefing. This project forbids ungrounded claims (*work only from
the attached files; never invent*) and needs a **specific per-task output contract**. So you
keep STORM's four-phase multi-perspective *structure* but **re-ground it on the attached
corpus** and **re-shape it to the task's contract**. This skill is how to do that adaptation
without breaking governance.

**This skill shapes the research PROMPT. It never authorizes deciding the content, inventing a
number, or blurring the build-design vs. science-spec channel.**

## When to use

- Building or revising an ERW research-agent prompt using STORM / multi-perspective structure
  (trainex or specwork rounds).
- Any ask to "apply STORM", "use multiple expert perspectives", or "persona-based research"
  over attached source files.
- **Not for:** packaging mechanics (attachments, channels-never-mix, upload hygiene) → that is
  the **ERW runbook**. Deciding the actual science → that is **governance + the STOP protocol**.

## Step 0 — classify before adapting (this sets everything downstream)

| Task shape | Standing | Grounding | Output contract |
|---|---|---|---|
| **Build-design** (e.g. trainex-r1a) | recommend; owner ratifies | attached build/ops files | per-decision resolution |
| **Science / spec adjudication** (v1.4/1.5/1.6-style) | STOP protocol; candidate-verdict-source; **never invent** | resolution doc + issue doc + v-touched specs | per-gap adjudication |
| **Open synthesis / characterization** | describe; do not decide | the named corpus | the requested report |

Defer to CLAUDE.md (grounding / standing / STOP) and the ERW runbook
(`docs/runbooks/external-research/`) for the *rules*; this skill only structures the *prompt*.

## The five adaptation moves

1. **Re-attach retrieval to the closed corpus.** Every persona reasons *only* from the attached
   files; each claim cites the filename, or is logged as a gap. Silence → claims register,
   never an invented fact or number. (The #1 rule — it repairs the template's deleted "R".)
2. **Re-cast personas by essence, then add mandated lenses.** Keep each archetype's *function*,
   map it to a project expert, and add the personas your hard constraints demand (e.g. the
   non-expert operator; a spec-compliance guard). Draw from the palette below.
3. **Map the four phases onto the task's existing output contract** — Phase 3 *writes that
   contract*, not a briefing.
4. **Preserve scope / standing / carve-outs.** Keep the verbatim STORM prompts only as labeled
   provenance, with an explicit "execute the adaptation, not the generic template" guard.
5. **Consolidate + reconcile.** Merge to one self-contained paste (or keep the split) per the
   owner's packaging choice; fix the attach-list and delivery note to match.

## The four phases → what each becomes

| STORM phase | Adapted job |
|---|---|
| **1 · Multi-Perspective Scan** | Interrogate the task's items through grounded domain personas; each gives position · strongest *file-cited* evidence · the one thing only it would flag. |
| **2 · Contradiction & Consistency Map** | Per-item conflicts; unanimous agreements = robust picks; items no persona could ground → claims register; spec-drift flags. |
| **3 · Synthesis** | **Write the task's output contract** (per-decision/per-gap fields + a coherence check + what the runbook/consumer inherits). Not a generic briefing. |
| **4 · Peer Review** | Confidence per item; weakest-link / probe-needed; bias check (did one lens override a one-way door?); missing-angle; honesty grade; finalize the claims register. |

## Project persona palette

Re-cast the generic five (practitioner / academic / skeptic / economist / historian) into
project lenses, adding what the constraints demand:

- **Apple-Silicon / MPS practitioner** — real runtime, unified-memory, op-coverage behavior.
- **PINN / numerical-methods researcher + spec-compliance guard** — what the locked specs
  require; where an option now contradicts them (spec-drift).
- **Adversarial build reviewer** — the strongest case the suggested default fails on first run.
- **Compute / memory / dev-hours cost economist** — true cost; the cheapest path that still
  protects the one-way doors.
- **Operations-experience lens** — prior findings (r1b-style): feasibility limits, correctness
  ladder, failure watchlist.
- **Non-expert runbook operator** — simplest operation, best-typed failures (a hard constraint).
- **Stage-0 / one-way-door strategist** — needed-now vs. deferrable; expensive-to-reverse picks.

Match the count in Phase 4's "missing angle" check to however many personas you used.

## Common mistakes

- **Pasting the generic prompts as-is** → ungrounded, world-knowledge output that violates
  *never-invent*. The template *invites* this; move 1 prevents it.
- Producing a Wikipedia/CEO briefing instead of the task's per-decision/per-gap contract (move 3).
- Keeping "who profits" / "historical parallels" personas literally instead of re-casting them.
- Letting "simplest for the operator" override a one-way door a harder lens flagged.
- Inventing ⚖ thresholds or project numbers the sources do not actually give.
- Touching the science specs or deciding content — this skill authors the *prompt* only.

## Reference

- **Verbatim 4-prompt template + attribution:** `storm-source-prompts.md` (this folder) — durable
  copy, because the source article is behind an X.com login wall.
- **Worked example:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/research_package/RESEARCH-AGENT-PROMPT-STORM.md`.
- **Source method:** Stanford STORM, NAACL 2024 (Stanford OVAL Lab); the 4-prompt chat form by
  Nav Toor (@heynavtoor, 2026-06-17).

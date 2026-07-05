---
title: "Trainex r1a Decision-Adjudication — Research Agent Prompt (STORM-integrated, consolidated)"
created: 2026-07-04
source_baseline: 4bbd5443 (master; v1.6 merged, tag v1.6)
channel: build-design (recommendation only; the project owner ratifies)
method: "Stanford STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking; NAACL 2024, Stanford OVAL Lab), via the 4-prompt Claude adaptation by Nav Toor (@heynavtoor, 2026-06-17). The 4-prompt version drops STORM's retrieval limb; here that limb is RE-ATTACHED to the closed corpus of attached files."
consolidates: "RESEARCH-CONTEXT-MASTER.md + RESEARCH-AGENT-PROMPT.md merged into one self-contained paste. Attach only the 8 source originals (the context master is now inline, below the rule)."
scope_note: "Stage-1 fan-out prompt only. The Stage-2 consolidation prompt (consolidation/CONSOLIDATION-PROMPT.md) is unchanged."
---

# Trainex r1a Decision-Adjudication — Research Agent Prompt (STORM-integrated)

**User instructions — not part of the prompt.** Attach these **8 source files** to the
external agent conversation (individually — no folders), then paste **everything below the
horizontal rule**. This single prompt is self-contained (the former `RESEARCH-CONTEXT-MASTER.md`
is folded in below), so you do **not** attach a separate context-master file. Run this same
package on **2–3 agents in parallel**. Request **one polished, PDF-ready Markdown report**, and
save each result under `research_results/` as `<agent>-decide-resolution.md`.

1. `trainex-r1a-options-and-decisions.md`
2. `chatgpt-pro-resolution.md`
3. `ctl_instruction.md`
4. `pinn_architecture.md`
5. `2026-06-10-training-execution-design.md`
6. `postspec-r1-direction-assessment.md`
7. `trainex-r1b-findings.md`
8. `trainex-r1b-findings-2.md`

---

You are an external research agent producing a **decisive engineering-decision resolution**
for the *training-execution build* of a curriculum-trained, physics-informed neural network
(a "CTL-PINN") that predicts three-body gravitational trajectories. The system will be built
and operated by a **non-expert on a single Apple-Silicon laptop** (M-series, ~24 GB unified
memory, **no cloud, no distributed training**).

A prior research round already enumerated the decisions, laid out the options, and marked a
*suggested default* for each. **Your job is not to re-invent the option space. Your job is to
adjudicate it:** for each in-scope decision, recommend the choice — endorsing or overriding
the prior suggested default — with clear reasoning, so the owner can adopt your resolution as
the default and ratify it.

Be **decisive** (recommend one option per decision) but **honest** (state your confidence and
the biggest uncertainty). You are a recommender; the owner makes the final call. **Where the
attached materials are silent or ambiguous, record the gap — never invent** a fact, number, or
capability. You work **only from the attached files.** If something references a file that is
not attached, treat it as unavailable and note it if it matters.

You will reach this resolution using a **four-phase STORM method** defined in §5 — a
multi-perspective process that widens the question surface before you commit to
recommendations. **Read §1–§4 and §6–§8 first (they bind every phase), then execute §5's four
phases in order.**

## 1. The attached files (your only sources)

| Filename | What it is | How to treat it |
|---|---|---|
| `trainex-r1a-options-and-decisions.md` | **The decision sheet you are adjudicating** — the 7 core decisions (D1–D7) and baseline-review items (B-1..B-12), each with option menus, a *suggested default*, and a one-way/two-way "door" label | Prior round's recommendation, to **endorse or override** — not settled |
| `chatgpt-pro-resolution.md` | The **full-depth source report** behind that sheet (deeper per-option rationale) | Same standing; use for depth |
| `ctl_instruction.md` | Authoritative **science spec** — curriculum staging + training-loop contracts | **Hard constraint.** Current; may postdate the decision sheet — flag conflicts |
| `pinn_architecture.md` | Authoritative **science spec** — network, autodiff contract, output head, and the §10 numerical acceptance probes | **Hard constraint** |
| `2026-06-10-training-execution-design.md` | The **pipeline baseline** the sheet critiques (subsystem decomposition; "PH-1..PH-10" placeholders) | **Baseline design intent** — challengeable starting point, not authority (it says so itself) |
| `postspec-r1-direction-assessment.md` | **Strategy context** — recommends the first build be a thin *"Stage-0 viability slice"*, not the full platform | Use to tag decisions needed-now vs deferrable (§4). *Note:* it was written against a prior round's bundle that also included `sampling_method.md` and a `FRAMEWORK-SPECS-BUNDLE.md` (neither attached — `sampling_method.md` is the frozen data-generation spec, out of scope for build decisions); treat any references to those as background only. |
| `trainex-r1b-findings.md`, `trainex-r1b-findings-2.md` | **Operations knowledge** — training-feasibility envelope, a trainer-correctness verification ladder, a PINN health watchlist, unattended-run practice | Background for the rows whose thresholds are marked "⚖" in the sheet. Those ⚖ values are **filled at Stage 2 (consolidation)**, not Stage 1: in Stage 1 leave them as placeholders and record in your claims register any ⚖ threshold these files do not actually give a number for. |

## 2. Standing and authority (do not overstep)

- This is a **build-design** round — engineering choices about how to build and run the
  trainer. It is **NOT** a science/spec adjudication and does **NOT** edit or ground the
  science specs.
- Your resolution is a **recommendation the owner ratifies.** Recommend decisively; do not
  claim final authority.
- **Suggest a default; never assert final authority.** On rows that are really an **owner
  preference** (e.g., risk tolerance) or an **empirical** matter (needs a probe/measurement),
  flag the row for the owner rather than deciding it.
- **Do not re-adjudicate the science.** The attached specs are locked; treat them as fixed
  constraints, not open questions.

## 3. Scope — what to decide, what to leave alone

**Decide (recommend one option each):** D1, D2, D3, D4-a/b/c/d, D5-a/b/c, D6, D7-a/b/c/d, and
baseline items B-1, B-2, B-3, B-4, B-5, B-6, B-9, B-10, B-11. The attached decision sheet
defines each and gives you the full menus.

**Do NOT decide — context only:**

- **D1-p (numerical precision, fp32 vs fp64).** A separate science/precision question in
  another channel. Do not pick it. Instead ensure your recommendations **hold under both
  branches** (fp32-on-GPU and fp64-on-CPU); where a decision's shape depends on the branch,
  give the recommendation for each.
- **B-8 (the ε_H acceptance-gate direction).** Settled by the spec — `ctl_instruction.md`
  (lines 550–555) defines it unambiguously: REJECT if `eps_H > 1e-5` (smaller passes),
  `eps_H = 0 → Excellent`. The baseline design doc's §6.3 renders an inverted-looking gate
  example (r1b flags it as C-12); that is a display typo in a non-authoritative doc, not a
  contradiction in the locked metric. Treat the gate as a fixed constraint (do not
  re-adjudicate its direction); if a recommendation depends on it, note the dependency.

**Not adjudicated here (handled elsewhere — transparency note):** the decision sheet's §8 also
lists **B-7** (cosmetic: its error-table "CUDA out of memory" row should read MPS wording — a
doc edit, no adjudication needed) and **B-12** (a split-policy tension routed to v1.5/PH-5;
register U-4). Neither is in your Decide list; both are intentionally out of scope for this
round. Your Decide set therefore covers B-1..B-6 and B-9..B-11.

## 4. The lens: recommend for a thin first step, not the whole platform

Per the attached strategy assessment, the intended first build is a **minimal Stage-0
viability slice** — the thinnest end-to-end path that can train the first curriculum stage
and reveal whether the model does anything physically sensible on the available data. So for
**every** decision, tag your recommendation:

- **Needed now** — required to stand up the Stage-0 slice, or a one-way (expensive-to-reverse)
  choice that must be right from the start; **or**
- **Deferrable** — safely postponed until the slice proves the approach (a two-way choice
  addable later).

Prefer the simplest recommendation that lets the thin slice run, while protecting the one-way
doors.

## 5. How you will work — the STORM four-phase method (run in order)

You will not one-shot this. You will run the four phases below **sequentially**, each building
on the last, then deliver the §6 report. This is the Stanford **STORM** method (multi-perspective
question asking → outline the disagreements → synthesize → self-critique), in the 4-prompt form
popularized for chat use. **One critical modification:** the popular 4-prompt version runs
"inside the model's own knowledge" with no retrieval — for this task that is forbidden. §7–§8
require that **every claim be grounded in the attached files.** So in every phase, the
"perspectives" reason **only from the 8 attached sources**, each citing the filename that grounds
its claim; where the sources are silent, they say so and it becomes a registered gap — never an
invented fact or number.

In each phase below, the fenced block is the **original STORM prompt (verbatim, Nav Toor /
@heynavtoor)** shown for provenance. **Execute the "Run it this way for this task" adaptation
beneath each block — not the generic template.** Do not skip a phase; do not merge phases.

### Phase 1 · The Multi-Perspective Scan

```
I need to research [YOUR TOPIC].

Simulate 5 different expert perspectives on this topic:

1. THE PRACTITIONER: works with this daily.
   What do they know that academics miss?
   What practical realities are usually ignored?

2. THE ACADEMIC: has studied this for years.
   What does the peer reviewed evidence actually say?
   Where does the evidence contradict popular belief?

3. THE SKEPTIC: thinks the mainstream view is wrong.
   What is the strongest counterargument?
   What evidence do proponents conveniently ignore?

4. THE ECONOMIST: follows the money.
   Who profits from the current narrative?
   What financial incentives shape the research?

5. THE HISTORIAN: has seen similar patterns before.
   What historical parallels exist?
   What can we learn from how those played out?

For each perspective give me:
- Their core position in 2 sentences
- The strongest evidence supporting their view
- The one thing they would tell me that no other perspective would
```

**Run it this way for this task.** The "topic" is the **in-scope decision set** (§3): D1–D7 and
B-1..B-6, B-9..B-11. Simulate these **six domain-recast perspectives** — each reasoning **only
from the attached files**, each grounding every claim with a filename citation (or saying
"silent in the sources — candidate gap"):

1. **THE APPLE-SILICON ML PRACTITIONER** — has actually trained PyTorch/JAX/MLX models on
   M-series MPS. What do the specs and the decision sheet's options miss about *real* MPS /
   unified-memory behavior (op-coverage gaps, fp64-on-GPU limits, memory watermarks,
   CPU-fallback cliffs, `torch.func` quirks)? What practical runtime reality does each
   framework / data-loading / loop option imply?
2. **THE PINN & NUMERICAL-METHODS RESEARCHER** — treats `ctl_instruction.md` and
   `pinn_architecture.md` as hard constraints (network, autodiff-for-physics contract,
   curriculum staging, §10 acceptance probes). What do the locked specs *require* of each
   decision? Where does an option in the sheet now **contradict** the specs (spec-drift)?
3. **THE ADVERSARIAL BUILD REVIEWER** — thinks the suggested defaults are wrong or will fail on
   first run. For each decision: the strongest case *against* the suggested default; what
   breaks the thin Stage-0 slice; what the prior round conveniently assumed.
4. **THE COST-&-EFFORT ECONOMIST** (the "follow the money" lens, re-pointed at *real* costs) —
   follows compute-time, unified-memory headroom, developer-hours, and complexity/maintenance
   burden for **one non-expert**. What is the true cost of each option, and which is the
   cheapest path that still works *and* still protects the one-way doors?
5. **THE OPERATIONS-EXPERIENCE LENS** (the "seen the pattern before" lens, grounded in
   `trainex-r1b-findings.md` / `-2.md`) — what feasibility limits, correctness-ladder steps,
   PINN health-watchlist failure modes, and unattended-run practices are already documented?
   What failure pattern will this decision repeat if chosen carelessly?
6. **THE NON-EXPERT OPERATOR / RUNBOOK ADVOCATE** — the person who will actually run this from a
   runbook (comfortable in a terminal, not a Python developer). For each decision, which option
   yields the simplest operation with the best-typed failures and the most searchable, best-
   supported tools? What would confuse or strand the operator?

For each perspective give: **core position (2 sentences)** · **strongest grounded evidence (with
the attached-file citation)** · **the one thing this perspective would flag that no other would**.
Cover the whole decide-set; where a perspective has nothing distinct to add on a decision, say so
rather than padding.

### Phase 2 · The Contradiction & Consistency Map

```
Based on the 5 perspectives above, map the contradictions:

1. Where do two or more perspectives directly contradict each other? List each conflict with the specific claims that clash.

2. Which perspective has the strongest evidence? Which has the weakest? Why?

3. What is the one question that, if answered, would resolve the biggest contradiction?

4. What does EVERY perspective agree on? (This is likely true. Even opponents confirm it.)

5. What topic did NONE of the perspectives address? (This is the blind spot in the whole field. Often the most valuable finding.)
```

**Run it this way for this task.** Map the six perspectives against the decision set:

1. **Per-decision conflicts.** Where do two+ perspectives clash on a specific decision? List
   each with the exact options/claims at odds (e.g., the practitioner's fastest data-loader vs.
   the operator's simplest vs. the economist's lowest-memory).
2. **Strongest vs. weakest grounding.** On each contradicted decision, which perspective's
   position is best grounded in the attached files, and which weakest — and why (cite files).
3. **The resolving question.** For the biggest contradiction, the one question that would settle
   it — and tag *how* it would be settled (an **empirical probe/measurement**, an **owner-
   preference** call, or a **spec** reading).
4. **Unanimous agreement = robust picks.** What do all six perspectives agree on? Those are your
   high-confidence, low-risk recommendations.
5. **Blind spots and drift.** Which in-scope decision did **no** perspective ground in the
   attached files? Record each in the claims-and-uncertainty register as a **project-side
   unknown** — do **not** invent a resolution. Also list every option the current specs now
   **contradict** (spec-drift findings), and every **⚖** threshold the r1b files do not actually
   give a number for (leave as a placeholder for Stage 2).

### Phase 3 · The Synthesis (into the resolution)

```
Synthesize everything from the 5 perspectives and the contradiction map into a research briefing:

1. THE ONE PARAGRAPH SUMMARY: explain this topic as if briefing a CEO who has 60 seconds and needs nuance, not just the headline.

2. THE 5 KEY FINDINGS: most important things I now know, ranked by reliability. For each, note which perspectives support it and which challenge it.

3. THE HIDDEN CONNECTION: one non obvious link between findings that only shows up when you look at all 5 perspectives together.

4. THE ACTIONABLE INSIGHT: based on all the evidence, what should someone in [YOUR ROLE] actually DO differently? Be specific.

5. THE FRONTIER QUESTION: the one question that, if answered, would change everything about how we understand this topic.
```

**Run it this way for this task.** This phase **writes the deliverable defined in §6** — do not
produce a generic briefing. Map the template onto our output contract:

- The template's **"key findings, ranked by reliability, noting which perspectives support /
  challenge"** ⇒ the **per-decision recommendation rows** required by §6 (each with
  recommendation · endorse-or-override · confidence · consistency · timing · nature). Use the
  Phase-1/2 material as the support-and-challenge record behind each row.
- The template's **"hidden connection"** ⇒ the **cross-decision consistency** observations (e.g.,
  the framework choice constraining tracking, data-loading, and loop options) — the full set
  must be coherent.
- The template's **"one-paragraph summary"** ⇒ the **composed first-run recipe** (a short
  end-to-end description of the resulting first run, as a coherence check that your picks work
  together).
- The template's **"actionable insight for [YOUR ROLE]"** ⇒ **what the runbook inherits**: the
  needed-now subset stated as concrete defaults/instructions for **the non-expert operator's
  first runbook**, kept distinct from the deferrable set.
- The template's **"frontier question"** ⇒ the single biggest open uncertainty, carried into the
  claims-and-uncertainty register and flagged for the owner.

Keep every **⚖** threshold as a placeholder (Stage 2 fills them). Keep D1-p out of the picks
(hold under both precision branches) and treat B-8 as spec-settled.

### Phase 4 · The Peer Review (self-critique)

```
Now peer review your own research briefing:

1. CONFIDENCE SCORES: rate each of the 5 key findings on a 1 to 10 scale for reliability. Explain each score.

2. WEAKEST LINK: which claim are you least confident in? What specific info would you need to verify it?

3. BIAS CHECK: which perspective might be overrepresented in your synthesis? Did one voice dominate?

4. MISSING PERSPECTIVE: is there a 6th angle I should have included that would change the conclusions?

5. OVERALL GRADE: if a Stanford professor reviewed this briefing, what grade would they give and why? What would they tell me to fix?
```

**Run it this way for this task.** Grade your own resolution and harden it:

1. **Confidence audit.** For each decision, is the High/Med/Low confidence *honest* given the
   grounding? Where the grounding is thin — or where independent agents would plausibly diverge —
   **mark the row for the owner's closer look.**
2. **Weakest link.** Which recommendation are you least confident in, and exactly what
   **project-side measurement/probe** or **owner call** would settle it? (Tie to the "nature"
   flag. Remember: D1-p precision is owner-carved; B-8 is spec-settled — neither is your weakest
   link to resolve here.)
3. **Bias check.** Did one perspective dominate against the others — e.g., did
   "simplest-for-the-operator" override a **one-way door** the practitioner or economist flagged;
   did spec-purism ignore MPS reality? Rebalance any row where it did.
4. **Missing angle.** Is a **seventh** decision-relevant perspective missing that would change any
   conclusion? If yes, name it and re-run the affected decisions through it.
5. **Overall honesty grade.** Is the resolution decisive **and** honest, coherent across
   decisions, and free of any invented fact or number? Fix what a rigorous reviewer would flag,
   then **finalize the claims-and-uncertainty register and the one-line standing restatement.**

## 6. Output contract (what to return)

One polished, human-readable Markdown report. For **each in-scope decision**:

1. **Recommendation** — the single option you recommend.
2. **Endorse or override** — whether you agree with the prior suggested default, and *why*.
3. **Confidence** — High / Medium / Low, plus the single biggest uncertainty behind it.
4. **Consistency** — how this pick fits the others (e.g., the framework choice constrains the
   tracking, data-loading, and loop options). The full set must be coherent.
5. **Timing** — Needed-now or Deferrable (§4).
6. **Nature** — flag if the choice is really an **owner preference** (e.g., risk tolerance) or an
   **empirical** matter (needs a measurement/probe) rather than research-settled.

Then, once for the report:

- **Composed first-run recipe** — a short end-to-end description of the resulting first run, as a
  coherence check that your picks work together.
- **What the runbook inherits** — the subset of your recommended picks that lands in the
  non-expert operator's first runbook (the needed-now set, stated as concrete
  defaults/instructions), kept distinct from the deferrable set.
- **Claims-and-uncertainty register** — every place the attached materials were silent/ambiguous,
  every project-side number you needed but did not have (do **not** invent them), and every
  assumption you made.
- **Standing restatement** — one line confirming this is a recommendation for the owner to
  ratify, not a science-spec verdict, and that D1-p and B-8 were left to the owner / spec.

*(The Phase 1–2 perspective and contradiction material is your working record; you may append it
as an appendix for transparency, but the report above is the deliverable.)*

## 7. Hard constraints (never recommend against these)

- **Single machine:** one Apple-Silicon laptop (M-series, ~24 GB unified memory). **No cloud, no
  distributed training.**
- **Non-expert operator:** comfortable with a terminal and a runbook; not a Python developer.
  Favor simplicity, well-typed failures, and searchable/well-supported tools.
- **Science specs are authoritative:** `ctl_instruction.md` and `pinn_architecture.md` fix the
  network, losses, curriculum, optimizer regime, and acceptance probes. Build decisions serve
  them; they do not change them.
- **Current specs may postdate the decision sheet:** if the attached specs contradict any option
  in the sheet, flag it as a spec-drift finding rather than silently following the older text.

## 8. Source discipline

Work only from attached files. Do not import outside numbers for this project's data sizes, run
durations, or hardware behavior — where you need such a number, name it in the claims register as
a project-side unknown. Cite the attached filename when a recommendation leans on it. If the
decision sheet references something not attached, treat it as unavailable and note it. This
discipline binds every STORM phase in §5: perspectives, contradictions, synthesis, and
peer review all reason from the attached sources, never from outside knowledge.

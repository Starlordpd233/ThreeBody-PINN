# Consolidated attachment (mechanical bundle) for external research agent
# This file = concatenation of the following original sources (content unchanged):
#   1. research_package/RESEARCH-CONTEXT-MASTER.md
#   2. attachments/postspec-r1-direction-assessment.md
#   3. attachments/2026-06-10-training-execution-design.md
# Baseline commit: 4bbd5443 (v1.6 tag per DELIVERY-NOTE)
# Consolidated on: 2026-07-04
# IMPORTANT: Original filenames appear in the BEGIN/END markers below.
#            The RESEARCH-AGENT-PROMPT will instruct you which bundle contains which original.
================================================================================
BEGIN ORIGINAL: RESEARCH-CONTEXT-MASTER.md
================================================================================
---
title: "Trainex r1a — Decision-Adjudication Research Brief (Context Master)"
created: 2026-07-04
source_baseline: 4bbd5443 (master; v1.6 merged, tag v1.6)
channel: build-design (recommendation only; the project owner ratifies)
---

# Trainex r1a — Decision-Adjudication Research Brief

## 0. What you are doing (read this first)

You are an external research agent producing a **decisive engineering-decision
resolution** for the *training-execution build* of a curriculum-trained, physics-informed
neural network (a "CTL-PINN") that predicts three-body gravitational trajectories. The
system will be built and operated by a **non-expert on a single Apple-Silicon laptop**
(M-series, ~24 GB unified memory, **no cloud, no distributed training**).

A prior research round already enumerated the decisions, laid out the options, and marked
a *suggested default* for each. **Your job is not to re-invent the option space. Your job
is to adjudicate it:** for each in-scope decision, recommend the choice — endorsing or
overriding the prior suggested default — with clear reasoning, so the owner can adopt your
resolution as the default and ratify it.

Be **decisive** (recommend one option per decision) but **honest** (state your confidence
and the biggest uncertainty). You are a recommender; the owner makes the final call. Where
the attached materials are silent or ambiguous, **record the gap — never invent** a fact,
number, or capability.

You work **only from the attached files.** If something references a file that is not
attached, treat it as unavailable and note it if it matters.

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
- **Suggest a default; never assert final authority.** You suggest a decisive default for the
  owner to ratify — you do not decide with final authority. On rows that are really an **owner
  preference** (e.g., risk tolerance) or an **empirical** matter (needs a probe/measurement),
  flag the row for the owner rather than deciding it.
- **Do not re-adjudicate the science.** The attached specs are locked; treat them as fixed
  constraints, not open questions.

## 3. Scope — what to decide, what to leave alone

**Decide (recommend one option each):** D1, D2, D3, D4-a/b/c/d, D5-a/b/c, D6,
D7-a/b/c/d, and baseline items B-1, B-2, B-3, B-4, B-5, B-6, B-9, B-10, B-11. The attached
decision sheet defines each and gives you the full menus.

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
and reveal whether the model does anything physically sensible on the available data. So
for **every** decision, tag your recommendation:

- **Needed now** — required to stand up the Stage-0 slice, or a one-way (expensive-to-
  reverse) choice that must be right from the start; **or**
- **Deferrable** — safely postponed until the slice proves the approach (a two-way choice
  addable later).

Prefer the simplest recommendation that lets the thin slice run, while protecting the
one-way doors.

## 5. Output contract (what to return)

One polished, human-readable Markdown report. For **each in-scope decision**:

1. **Recommendation** — the single option you recommend.
2. **Endorse or override** — whether you agree with the prior suggested default, and *why*.
3. **Confidence** — High / Medium / Low, plus the single biggest uncertainty behind it.
4. **Consistency** — how this pick fits the others (e.g., the framework choice constrains
   the tracking, data-loading, and loop options). The full set must be coherent.
5. **Timing** — Needed-now or Deferrable (§4).
6. **Nature** — flag if the choice is really an **owner preference** (e.g., risk tolerance)
   or an **empirical** matter (needs a measurement/probe) rather than research-settled.

Then, once for the report:

- **Composed first-run recipe** — a short end-to-end description of the resulting first
  run, as a coherence check that your picks work together.
- **What the runbook inherits** — the subset of your recommended picks that lands in the
  non-expert operator's first runbook (the needed-now set, stated as concrete
  defaults/instructions), kept distinct from the deferrable set.
- **Claims-and-uncertainty register** — every place the attached materials were
  silent/ambiguous, every project-side number you needed but did not have (do **not**
  invent them), and every assumption you made.
- **Standing restatement** — one line confirming this is a recommendation for the owner to
  ratify, not a science-spec verdict, and that D1-p and B-8 were left to the owner.

## 6. Hard constraints (never recommend against these)

- **Single machine:** one Apple-Silicon laptop (M-series, ~24 GB unified memory). **No
  cloud, no distributed training.**
- **Non-expert operator:** comfortable with a terminal and a runbook; not a Python
  developer. Favor simplicity, well-typed failures, and searchable/well-supported tools.
- **Science specs are authoritative:** `ctl_instruction.md` and `pinn_architecture.md` fix
  the network, losses, curriculum, optimizer regime, and acceptance probes. Build decisions
  serve them; they do not change them.
- **Current specs may postdate the decision sheet:** if the attached specs contradict any
  option in the sheet, flag it as a spec-drift finding rather than silently following the
  older text.

## 7. Source discipline

Work only from attached files. Do not import outside numbers for this project's data
sizes, run durations, or hardware behavior — where you need such a number, name it in the
claims register as a project-side unknown. Cite the attached filename when a recommendation
leans on it. If the decision sheet references something not attached, treat it as
unavailable and note it.
================================================================================
END ORIGINAL: RESEARCH-CONTEXT-MASTER.md
================================================================================
================================================================================
BEGIN ORIGINAL: postspec-r1-direction-assessment.md
================================================================================
---
title: "Post-Spec R1 — Strategic Direction Assessment"
subtitle: "What Comes After the Specs for the Curriculum-Trained Three-Body PINN"
author: "External Research Workflow · build-design / strategy advisory"
date: "2026-06-18"
geometry: margin=1in
fontsize: 11pt
linkcolor: black
urlcolor: black
---

*Standing: recommendation only. This report advises a direction of travel; the
project owner makes the decision. It is not a candidate verdict source for
framework-spec adjudication, and it does not re-adjudicate the specs.*

*Scope: written from `RESEARCH-CONTEXT-MASTER.md` and the three specs bundled in
`FRAMEWORK-SPECS-BUNDLE.md` (`ctl_instruction.md`, `pinn_architecture.md`,
`sampling_method.md`). No repository or live-code access; no external sources
were required (the question is internal to the attached framework, and the
underlying ML rationale is already argued inside the specs themselves).*

---

## 1. Executive Summary

The specs are in unusually good shape. The architecture is fully pinned down and
deliberately modest in size, the data-generation pipeline is clean, the data
already exists, and the training loop is specified end to end. What is *not*
settled is whether the approach actually works at the scale of data on hand —
and the specs say so, repeatedly and in the owner's own voice.

That single fact reshapes the EDL-versus-Trainex question. The largest risk
sitting in front of this project is **not** "can we engineer a training
pipeline" — the specs make that comparatively low-risk. The largest risk is
**viability under data scarcity**: whether this curriculum-PINN, trained on the
limited data available, can become something that even *resembles* a working
three-body surrogate, and whether the curriculum's theoretical thresholds and
stage populations survive contact with the real data distribution.

Because that is fundamentally an *empirical* question, the next stage should be
**evidence-first** in purpose — the spirit of EDL. But the evidence that matters
cannot be gathered by small isolated probes alone; the central unknowns ("does
Stage 0 converge to something physical? are the transition thresholds even
reachable? is the data enough?") only reveal themselves when a real, if thin,
training path runs. That requires a *minimal* Trainex spine.

**Recommended direction of travel: a disciplined hybrid that leans EDL in
purpose and Trainex in mechanism — a "viability slice."** Concretely, the next
phase's job is to convert the specs' theoretical assumptions into evidence at
the smallest possible scale: first a cheap **data-and-curriculum
characterization** (which the spec author already proposed), then a **thin
Stage-0 training run instrumented as a viability probe**. Both produce evidence;
neither commits the project to building the whole system. The full
training-execution platform — all seven curriculum stages, robust
checkpoint/resume, a polished operator runbook, reproducibility provenance — and
the production training run are deferred until the slice says the approach is
worth industrializing and, just as importantly, tells us *what* to industrialize.

This is not "abstract EDL probes," and it is not "full Trainex." It is the
narrowest fusion of the two that attacks the real risk.

---

## 2. Current-State Diagnosis

Read against the seven evaluation criteria, the framework's strengths and soft
spots fall into a clear pattern.

**What is solid.**

- **The architecture is finalized and right-sized for the project's reality.**
  `pinn_architecture.md` specifies a SQR-SkipResNet-SIREN backbone of 12 hidden
  layers (6 residual blocks) at width 256, with principled SIREN initialization,
  LayerNorm on odd layers, and soft conservation regularizers for energy
  (matched-Plummer Hamiltonian) and angular momentum. This is a deliberately
  modest network — a strong fit for a single-machine, non-expert-operator
  project. Implementing it is standard PyTorch work, not research.
- **The data exists and the pipeline that made it is clean.** `ctl_instruction.md`
  reports 15,028 IC/Brutus pairs across four sets (high-fidelity hierarchical,
  low-fidelity quasi-random, plus high-temporal-resolution variants).
  `sampling_method.md` passed its audit with no source-level issues — every
  section marked PASS. The generation side is not where risk lives.
- **The training loop is specified end to end.** A two-phase per-stage strategy
  (Adam exploration handing off to L-BFGS refinement), lookahead sampling for
  smooth stage transitions, curriculum-aware adaptive gradient clipping, a
  four-part stage-transition test, and a three-level Hydra configuration are all
  written down in `ctl_instruction.md`.
- **A verification surface is already designed.** `pinn_architecture.md` §10
  defines five numerical acceptance probes — scaling consistency, COM
  invariance, componentwise automatic differentiation against a synthetic
  trajectory, force–energy consistency, and a loss-stability dry run. The
  project has already done much of the conceptual work of *how to check itself*.

**What is genuinely unsettled — and flagged as such by the specs.**

- **The curriculum's stage-transition criteria are explicitly provisional.** The
  author note in `ctl_instruction.md`'s Phase 2 states plainly that all
  transition criteria are "theoretical now" and "will heavily depend on what the
  actual situation is like," worries that the training data may be "maybe not
  even enough," sets a deliberately modest success bar (the network shows "the
  potential to do something similar to a 3-body integrator"), and asks directly:
  *"Should we first test train stage 0 and see how it goes and then go from
  there?"* This is the most important sentence in the bundle for the present
  decision.
- **Several curriculum criteria depend on data statistics that may not be
  characterized yet.** Stage 3 is defined by quantiles of the low-fidelity
  distribution; Stages 4–5 by per-trajectory Lyapunov time $\tau_L$. Whether
  enough trajectories actually populate each stage — Stage 0 above all, since it
  is the starting rung — is an empirical question. The author had already
  suggested scanning the IC files first "to get an insight on what the data
  looks like, and then decide on the criteria."
- **At least one default is openly unevidenced.** The per-trajectory data-loss
  point count `n_pts_cap` is set to 32 with the explicit caveat that this is "not
  evidence-based — revisit with admitted-set snapshot distributions." (Helpfully,
  some characterization already exists: snapshot-count medians of 61 / 127 / 1003
  for standard / hierarchical / gold are recorded.)
- **Two cross-spec reconciliations remain open before training.** `SI-PINN-003`
  flags that the batch-construction strategy in `pinn_architecture.md` is "not
  consistent with the CTL instruction plan," to be resolved during training
  implementation. `SI-PINN-002` notes two SIREN details still marked for
  confirmation (dynamic scheduling for `omega_0`, and a hidden-layer detail). The
  earlier input-vector dimensionality question (`SI-CTL-001`) is, by contrast,
  already resolved.
- **The evaluation section narrates results that do not yet exist for this
  build.** Passages such as "the final model shows minimal energy drift … below
  0.1%" and "it can often reach 1–2 $\tau_L$" read as inherited from a source
  paper. `RESEARCH-CONTEXT-MASTER.md` is clear that the production training
  buildout has not been performed and that older live code is not the source of
  truth. These figures should be treated as *aspirations to test*, not
  established baselines — guarding against false certainty.

**Net diagnosis.** This is a project that has done its design homework
thoroughly and now faces a feasibility gate it has not yet walked through. The
specs are detailed; the *evidence* is thin. The risk has migrated from "is the
design coherent?" to "does the design, with this data, do anything?"

---

## 3. Strategic Evaluation Lens Applied

`RESEARCH-CONTEXT-MASTER.md` asks that the lens *sharpen* the recommendation up
front rather than be deferred. Applying it, three of the seven criteria
dominate the decision and effectively settle it.

- **Reduce the largest risk before full-scale implementation (criterion 1).**
  The largest risk is viability under data scarcity, not pipeline engineering.
  Any direction that pours effort into building the full system before testing
  viability is optimizing the wrong variable.
- **Create useful evidence without building the whole system first (criterion
  2).** The decisive unknowns are observable from a Stage-0-scale run plus a data
  audit. Building all seven stages, robust resume, and a runbook is not required
  to learn what we most need to know — and is partly wasted motion if the answer
  is discouraging.
- **Avoid premature engineering detail (criterion 4).** The specs already over-
  determine the design relative to the evidence behind it. The corrective is more
  evidence, not more engineering.

The remaining criteria reinforce rather than complicate this:

- *Preserve momentum after a long spec period (criterion 3):* after milestones of
  document work, the highest-morale move is to see the network *run* on real
  data — concrete, motivating, and a clean break from prose.
- *Avoid false certainty where sources are unsettled (criterion 5):* the
  inherited "results" prose and the author's own caveats both argue for treating
  the next phase as a question to answer, not a target to hit.
- *Fit a single-machine, non-expert-operator reality (criterion 6):* the modest
  model makes a thin slice cheap to run on one machine, and the slice doubles as
  the seed of the operator's eventual day-to-day workflow.
- *Clarify what broad class of work comes next (criterion 7):* the class is
  "minimal evidence-producing vertical slice," which is neither pure research-
  probing nor pure platform-building.

The lens does not merely permit the recommendation below; it points at it.

---

## 4. Candidate Direction Assessment

The brief asks for at least four directions: EDL-first, Trainex-first, a hybrid,
and any stronger reframing. Here is how each fares against the lens.

### 4.1 EDL-first (small probes and research loops before a larger buildout)

**Strengths.** Correctly oriented toward evidence and toward the genuinely
unsettled questions; cheap; low premature-engineering risk; honest about
uncertainty.

**Weakness.** As usually framed — small, *isolated* probes — EDL struggles to
touch the risk that matters most. "Does Stage 0 train to something physical?",
"are the transition thresholds reachable?", and "is the data enough?" are not
answerable by micro-experiments in isolation; they need a real, if minimal,
end-to-end training path. A purely probe-flavored stage risks producing tidy
findings that sidestep the central feasibility question. EDL's *purpose* is
exactly right; EDL *without any pipeline* is too thin.

### 4.2 Trainex-first (turn the framework into a trainable operational system)

**Strengths.** Produces the runnable artifact the project ultimately needs;
forces the open cross-spec reconciliations (`SI-PINN-003`, `SI-PINN-002`) to be
settled because you cannot build the loop without choosing; aligns with the
owner's instinct to actually run something.

**Weaknesses.** "Trainex" as a *full* reality pipeline — robust
checkpoint/resume, complete monitoring, all seven stages, hardened ingestion of
all four sets, a polished runbook, bit-for-bit provenance — is premature against
unvalidated assumptions. If the approach turns out to be data-starved, much of
that platform is built for a system that needs rethinking. A second caution:
this package contains *no returned result* from the Trainex foundational
research round that `RESEARCH-CONTEXT-MASTER.md` says exists elsewhere, so its
current content and conclusions cannot be assessed here. Committing "Trainex-
first" at full scope would partly rest on material not in evidence.

### 4.3 Hybrid (EDL plus Trainex in parallel)

**Strengths.** Recognizes, correctly, that the right answer combines evidence and
execution.

**Weakness.** A generic "do both" hybrid tends to do *too much* of both —
standing up real platform machinery while also running a research program — which
reintroduces exactly the premature-engineering risk the lens warns against. The
hybrid is the right *family*; it needs discipline to be the right *plan*.

### 4.4 Reframing — the "viability slice" (recommended)

Rather than choosing between EDL and Trainex, reframe the next stage by its
**deliverable**: *evidence about whether the framework, on the data we have,
does anything worth industrializing.* That deliverable is EDL in purpose. The
*cheapest mechanism* that yields it is a **thin Trainex spine** — the minimum
ingestion → preprocess → model → loss → train → observe loop needed to reach
Stage 0 — scoped to one viability question and one data audit, with everything
else deferred. This is the disciplined version of the hybrid: EDL-in-intent,
minimal-Trainex-in-means.

| Direction | Hits the largest risk? | Evidence w/o full build? | Premature-engineering risk | Net fit |
|---|---|---|---|---|
| EDL-first (isolated probes) | Partially — misses end-to-end feasibility | Yes | Low | Right purpose, too thin |
| Trainex-first (full pipeline) | Indirectly, and late | No | **High** | Right artifact, wrong timing |
| Generic hybrid (both at once) | Yes, but diffuse | Mixed | Medium–high | Right family, undisciplined |
| **Viability slice (reframe)** | **Yes, directly** | **Yes** | **Low** | **Recommended** |

---

## 5. Recommended Direction of Travel

Aim the next phase at a single outcome: **decide whether this curriculum-PINN, on
the data in hand, is worth a full buildout — and learn enough to design that
buildout well.** Pursue it as a thin, evidence-first vertical slice with two
sequenced thrusts. (These describe the *shape* and *intent* of the work, not a
task list, and deliberately avoid gates, milestones, or backlogs.)

**Thrust A — Characterize the data and the curriculum against reality (cheap,
first).** This is the move the author already proposed: scan the admitted IC set,
compute the difficulty invariants and $\tau_L$, and see how many trajectories
actually land in each stage — Stage 0 most of all. The point is to replace
theoretical stage definitions with knowledge of the real distribution, to
confirm whether the curriculum's rungs are populated, and to retire unevidenced
defaults such as `n_pts_cap`. This requires almost no training machinery and can
reshape Thrust B before a single epoch runs.

**Thrust B — Train Stage 0 as a viability probe on a minimal spine.** Stand up
the *thinnest* end-to-end path that can train Stage 0 (and, via lookahead, peek
at Stage 1), instrumented so the run answers the owner's own question: does the
network reach something that behaves like a three-body integrator, conserve the
invariants to a believable degree, and show the *potential* to improve with more
data? Building this spine forces the two open cross-spec reconciliations to be
settled — you cannot write the loop without choosing a batch construction
(`SI-PINN-003`) and confirming the SIREN `omega_0` handling (`SI-PINN-002`) — and
the slice itself generates the evidence to choose well. The already-designed §10
acceptance probes are the natural correctness backstop for this spine; they exist
precisely for this.

The product of these two thrusts is a defensible **go / adjust / rethink**
judgment, plus calibration data: realistic transition thresholds, a sane
`n_pts_cap`, and a first read on data sufficiency. That judgment is what unlocks
— and shapes — the full training-execution platform later. Crucially, the thin
spine is not throwaway: it is the seed from which a fuller Trainex platform
grows *if the evidence warrants it*.

---

## 6. Why This Direction Is Better Than The Alternatives

**Versus EDL-first.** It keeps EDL's correct instinct — produce evidence before
locking the path — but fixes EDL's blind spot. The feasibility of a
curriculum-PINN is an *end-to-end* property; a thin training run observes it,
isolated probes do not. The viability slice is EDL that actually reaches the risk.

**Versus Trainex-first.** It refuses to industrialize an unproven approach. Every
piece of platform engineering deferred here — full resume, complete monitoring,
all seven stages, the operator runbook, bit-for-bit provenance (which the spec
itself marks "ignore now, come back later") — is engineering that would be
built against assumptions the slice is designed to test first. It also avoids
leaning on the Trainex foundational research result, which is not in this
package and therefore cannot be evaluated here.

**Versus the generic hybrid.** It is the *disciplined* hybrid. By fixing a single
deliverable (a viability judgment) and a single minimal mechanism (a Stage-0
spine), it captures the "evidence plus execution" insight without the sprawl of
running a full research program and a real platform simultaneously.

**Against the lens, in one line:** it attacks the largest risk directly
(criterion 1), produces decisive evidence without building the whole system
(criterion 2), avoids premature engineering (criterion 4), restores momentum by
getting the model running (criterion 3), treats unsettled claims as questions
rather than targets (criterion 5), and fits a single-machine reality while
seeding the eventual operator workflow (criterion 6) — which is as clean a
mapping to the evaluation lens as any of the candidates achieves (criterion 7).

It also has a quieter merit: it agrees with the project owner's own stated
instinct to "test train stage 0 and see how it goes." The recommendation is not
imposing a foreign plan; it is giving structure to an intuition already on the
record in `ctl_instruction.md`.

---

## 7. What Not To Work On Yet

Deferring the following is part of the recommendation, not an oversight. Each is
either premature against current evidence or explicitly downstream.

- **The full seven-stage curriculum buildout.** Stage 0 (plus a lookahead glance
  at Stage 1) is enough to answer the viability question. Wiring all stages
  before that answer is premature.
- **A hardened training platform.** Robust checkpoint/resume, full monitoring
  dashboards, Hydra sweep infrastructure, and a polished operator runbook are the
  *output* of a successful slice, not its prerequisite.
- **Active-learning data enhancement (the curriculum's Phase 3).** This is far
  downstream of demonstrating that base training works at all.
- **A full long-horizon evaluation harness.** Lyapunov prediction-horizon and
  long-term statistical-outcome metrics are valuable later; a Stage-0 slice needs
  only short-horizon error plus conservation diagnostics to read viability.
- **Reproducibility provenance.** The spec itself defers bit-for-bit
  reproducibility ("ignore now, come back later"); honor that.
- **Re-adjudicating the specs.** Out of scope for this advisory and unnecessary —
  the specs are coherent. The two open reconciliations get settled *as a
  byproduct* of building the slice, not as a separate spec exercise.
- **Chasing the inherited result numbers.** The "0.1% energy drift" and "1–2
  $\tau_L$" figures are aspirations to test, not baselines to match; do not let
  them set premature targets.

---

## 8. Key Risks and Unknowns

State assumptions where they bite, plainly.

- **Data sufficiency could be the binding constraint — possibly fatal.** The
  author's worry that the data may be "not even enough" is the single largest
  unknown. The viability slice is designed precisely to surface this early and
  cheaply, before heavy investment. *If* the data is too thin, the right response
  is to learn that now rather than after building a platform.
- **Stage 0 may be under-populated.** If too few trajectories meet Stage-0
  criteria, the curriculum's starting rung is shaky and the criteria likely need
  empirical loosening — which is exactly what Thrust A would reveal and the
  author anticipated.
- **The theoretical thresholds may be unreachable.** The transition tests
  ($\mathcal{L}_{\text{phys}}^{\text{val}} < 10^{-4}$, energy drift $< 10^{-4}$)
  are provisional by the author's own statement. If a Stage-0 run cannot approach
  them, they need empirical recalibration — a finding, not a failure.
- **A dependency not in evidence: the Trainex foundational research result.**
  `RESEARCH-CONTEXT-MASTER.md` says a Trainex research round exists elsewhere, but
  no result is included here. *Assumption:* nothing in that result contradicts
  this assessment. If it already contains viability evidence or constraints, this
  recommendation should be reconciled with it before acting.
- **The batch-construction inconsistency (`SI-PINN-003`) is unresolved.** The
  slice cannot be built without choosing between the two specs' batch strategies;
  that choice could affect both correctness and the slice's design. It should be
  made deliberately, with the slice's evidence informing it.
- **SIREN training stability is not yet demonstrated here.** The open `omega_0`
  scheduling detail (`SI-PINN-002`) is an empirical matter; SIREN networks can be
  initialization- and frequency-sensitive, and the §10 AD probe plus the slice
  are the right places to confirm behavior.
- **Specs-only vantage point.** This assessment is built from the attached files,
  not from repository access or live code (which is declared outdated and
  unusable). Conclusions about implementation readiness therefore rest on the
  specs' completeness, which is high but not a substitute for a running system —
  which is itself part of why a slice is the recommended next step.

---

## 9. Closing Recommendation

Make the next stage **evidence-first and small**. Spend it answering the question
the specs keep circling — *does this curriculum-PINN, on the data we actually
have, do anything worth building out?* — by characterizing the data against the
curriculum and then running Stage 0 on the thinnest possible training spine,
instrumented as a viability probe. Treat the inherited result figures as
hypotheses, settle the two open cross-spec reconciliations as a byproduct of
building the slice, and explicitly defer the full platform, the remaining
curriculum stages, active learning, and reproducibility provenance until the
evidence justifies them.

This is the disciplined hybrid: EDL in purpose, a minimal Trainex spine in
mechanism. It reduces the largest risk first, produces decisive evidence without
over-building, keeps momentum after a long spec period, and respects a single-
machine, single-operator reality — while honoring the project owner's own
instinct to test-train Stage 0 before committing to the larger road.

The decision remains the owner's. This report recommends the direction; it does
not lock it.

---

## 10. References / Source Notes

**Primary sources (attached).**

- `RESEARCH-CONTEXT-MASTER.md` — governing brief: task framing, ERW standing,
  evaluation lens, failure modes, output contract, source discipline. Defines the
  EDL and Trainex candidate directions and the "leave room for a third path"
  instruction.
- `FRAMEWORK-SPECS-BUNDLE.md` — bundled framework specs, baseline `6a720fe0`,
  comprising:
  - `ctl_instruction.md` — multi-fidelity dataset and the ~15,028 IC/Brutus
    pairs; the difficulty invariants ($E$, $L/L_{\max}$, $Q$, $s_{\min}$,
    $\tau_L$); the seven-stage replay curriculum and its mix of theoretical,
    quantile-based, and Lyapunov-based criteria; the Phase 2 two-phase
    (Adam → L-BFGS) training loop, lookahead sampling, adaptive clipping, and the
    four stage-transition criteria; the `n_pts_cap` "not evidence-based" note and
    recorded snapshot-count medians; the author notes on provisional transition
    criteria and "test train stage 0"; `SI-CTL-001` (resolved).
  - `pinn_architecture.md` — the SQR-SkipResNet-SIREN backbone and finalized
    hyperparameters (depth 12 / width 256, SIREN, LayerNorm on odd layers, soft
    energy and angular-momentum regularizers); the §10 numerical acceptance
    probes; `SI-PINN-002` (open SIREN details) and `SI-PINN-003` (batch-
    construction inconsistency with the CTL plan).
  - `sampling_method.md` — the hierarchical + Sobol quasi-random IC generation
    and pre-screening pipeline; audited clean (no source-level issues).

**External sources.** None used. The question is internal to the attached
framework, and the machine-learning rationale invoked here (SIREN derivative
fidelity and spectral bias, residual/skip stability, L-BFGS refinement,
curriculum learning) is already argued and cited within `pinn_architecture.md`
itself; no date-sensitive external claims were required.

**Uncertainty flags carried in-text.** The unresolved viability and data-
sufficiency questions; the dependency on the Trainex foundational research result
not included in this package; the inherited evaluation figures that do not yet
correspond to a real run of the current build; and the specs-only vantage point
(no repository or live-code access).
================================================================================
END ORIGINAL: postspec-r1-direction-assessment.md
================================================================================
================================================================================
BEGIN ORIGINAL: 2026-06-10-training-execution-design.md
================================================================================
---
status: active
purpose: design
created: 2026-06-10
milestone: untracked
phase: training-execution
retirement_trigger: v1.5 milestone work; active until superseded
---

# CTL-PINN Training Execution Design

**Status:** Design intent — framework-agnostic, mechanical surface committed, scientific/technical internals deferred to research.
**Date:** 2026-06-10
**Scope:** How a non-expert user will run, monitor, and assess CTL-PINN training on a single M5 Pro MacBook.
**Out of scope:** On-disk dataset format (owned by v1.5 PIPE-XX), curriculum stage design (owned by `ctl_instruction.md`), network architecture (owned by `pinn_architecture.md`), IC sampling (owned by `sampling_method.md`).

> **Standing note (user directive, 2026-06-11):** This document is the artifact of a
> brief, quick brainstorm session (2026-06-10) and should be read as a **simplified
> baseline / starting point** for the trainex (training-execution) development — NOT as
> the fundamental or final structure of the pipeline. The brainstorming agent may not
> have broken the pipeline down optimally: the subsystem decomposition and the
> PH-1..PH-10 placeholder inventory are good starting considerations but may be further
> enhanced and revised by later research (trainex-r1 and beyond). Where Section 10 calls
> this a "frozen reference design," that freeze marks the end of the brainstorm session,
> not design authority — evidence-based challenges to any part of this design are
> expected and welcome in the trainex research rounds. Hard constraints that survive
> regardless of any revision: single M5 Pro machine, no cloud / no distributed training,
> non-expert operator, and framework-spec authority over the science.

---

## 1. Purpose

The CTL-PINN project has well-developed *framework specs* (curriculum staging, network architecture, sampling methodology) and a *produced dataset* (`simulation_data/`). What it does not yet have is a *user-facing training execution design* — a specification of how a non-expert user will go from "I want to train this model" to "the model is trained and verified, here is how good it is."

This document fills that gap. It defines:

- The **mechanical surface** of training (what the user types, what the user sees, what files appear).
- The **subsystem decomposition** (developer environment, data ingestion, training loop) and their boundaries.
- The **verification surface** (how the user knows if training is healthy, better, or good enough).
- The **placeholders** for internals that need external research before they can be honestly specified.

It explicitly does **not** define:
- The ML framework (deferred to PH-1).
- The on-disk dataset format (owned by v1.5 PIPE-XX).
- The loss function, network architecture, or curriculum promotion rules (owned by framework specs).
- Any scientific/technical internals where the source materials are silent (per the project's STOP protocol).

The intended reader is the project owner, who is non-expert at model training. This is a **reference design document** — a record of the design ideas, constraints, and deferred decisions captured during an early-stage brainstorm. It is not a build spec, a runbook, or a contract for immediate implementation. The user will refer back to this document later, when the time comes to start designing the training pipeline in earnest. That work will happen **in parallel** with the development of the actual PINN code (the scientific/mathematical side, owned by the framework specs); the mechanical surface captured here can be designed now because it doesn't depend on the science being settled.

---

## 2. Background and Constraints

### 2.1 Hardware reality

The only training machine is a **MacBook Pro M5 Pro**:

- **CPU:** 16 cores
- **GPU:** 15 cores
- **Memory:** 24GB unified (BTO baseline; 48GB available on higher BTO)
- **OS:** macOS 15+ (Apple Silicon, arm64)
- **Neural Engine:** present (used by CoreML, not directly accessible to PyTorch/MLX/JAX for training)

Unified memory is the key hardware fact: CPU and GPU share the same physical RAM. There is no separate VRAM. Total budget for training is 24GB; if the trainer uses 20GB, the OS only has 4GB.

CPU+GPU co-utilization is desired (the M5 Pro is marketed for AI workflows) but the *exact* mechanism is a research question (see PH-8).

### 2.2 Project state

- **Framework specs exist** and are authoritative (`pinn_instruction/markdown_conversion/framework-specs/`).
- **Dataset is produced** (`simulation_data/`).
- **No live code** is a grounding source for v1.4+ spec decisions (user directive 2026-05-19). v1.3-era `pinn/` code (`basic_architecture.py`, `data-processing-pipeline-full.py`) is stale and will be rewritten in FUT-01 from specs.
- **v1.5 milestone** is in progress and owns the data pipeline and validation contracts (PIPE-XX).
- **FUT-04** is the future phase that will implement the training loop. FUT-01 rewrites the `pinn/` package from specs.

### 2.3 User profile

The user is a non-expert at model training. They have never trained a model before. They are comfortable with terminal commands but are not a Python developer. They can read code, follow a runbook, and report what they see.

### 2.4 STOP protocol compliance

The project's STOP protocol (CLAUDE.md, user directive 2026-05-19) forbids inventing content where source materials are silent. This design honors that:

- Internals where the spec is silent are marked as placeholders (PH-1 through PH-10).
- The user is told which decisions are theirs to make, not silently chosen.
- The framework choice is explicitly flagged as a research-driven decision, not committed in this document.

---

## 3. Architecture Overview

### 3.1 Three subsystems

The training execution has three subsystems, each with a clear boundary and a clear interface to its neighbors.

**Subsystem 1 — Developer Environment.** The substrate everything else runs on. A Python environment (Miniforge3-based, Python 3.11+, arm64-native), a machine-learning framework chosen per PH-1, a small set of utility packages, and a one-command setup script. The user interacts with this subsystem exactly once per machine.

**Subsystem 2 — Data Ingestion.** Reads the on-disk `simulation_data/` dataset via a thin adapter that hides the on-disk format from the rest of the trainer. Applies train/val/test splitting, drops NaN/Inf samples, emits fixed-shape mini-batches. The user does not interact with this subsystem directly.

**Subsystem 3 — Training Loop.** Runs an outer curriculum loop (driven by `ctl_instruction.md`) and an inner optimization loop (gradient descent over mini-batches from Subsystem 2, computing a combined data + physics + IC loss and backpropagating). Writes a `runs/<name>/` directory containing checkpoints, logs, and summary.

**Verification layer (not a fourth subsystem).** Reads the run output directory; does not modify training state. Lives in a separate `evaluate` script.

### 3.2 Data flow

```
   ┌──────────────────────┐
   │ simulation_data/     │  (on disk, format owned by v1.5 PIPE-XX)
   │   trajectories, ICs  │
   └──────────┬───────────┘
              │ reads
              ▼
   ┌──────────────────────┐
   │ Subsystem 2:         │
   │ Data Ingestion       │  (adapter layer, format-aware)
   │   train/val/test     │
   │   split manifest     │
   │   NaN/Inf filter     │
   └──────────┬───────────┘
              │ emits fixed-shape batches
              ▼
   ┌──────────────────────┐
   │ Subsystem 3:         │
   │ Training Loop        │  (curriculum outer + optimization inner)
   │   forward pass       │
   │   loss computation   │  ←── physics residuals (AD)
   │   backprop           │
   │   checkpoint         │
   └──────────┬───────────┘
              │ writes
              ▼
   ┌──────────────────────┐
   │ runs/<name>/         │  (consumed by verification)
   │   checkpoints/       │
   │   logs/              │
   │   summary.md         │
   │   status.json        │
   └──────────────────────┘
```

Subsystem 1 (Developer Environment) sits *under* Subsystems 2 and 3 — it is the substrate they run on, not a peer in the data flow.

### 3.3 What this design commits to (the non-placeholder surface)

1. Subsystem count and boundaries are committed.
2. Data flow direction is committed (Disk → Data Ingestion → Training Loop → Run output).
3. The "thin adapter" pattern for data ingestion is committed. The trainer does not import disk-format libraries; only the adapter does.
4. The five user-facing entry points (Setup / Configure / Launch / Monitor / Resume) are the only user-facing surfaces.
5. The `runs/<name>/` directory is the runbook contract.
6. The verification layer is a consumer, not a producer.
7. First-trial defaults are documented and overridable.
8. The ML framework is a researched decision, not a guess.

### 3.4 What this design does NOT commit to

- ML framework (PH-1)
- Network architecture (owned by `pinn_architecture.md`)
- Loss formulation details (owned by `pinn_architecture.md` and `ctl_instruction.md`)
- Optimizer and LR schedule (PH-7)
- Collocation sampling strategy (PH-6)
- Train/val/test split fractions (PH-5)
- CPU/GPU co-utilization mechanism (PH-8)
- Experiment tracker choice (PH-10)
- Checkpoint file format (framework-dependent)

---

## 4. Components

### 4.1 Subsystem 1 — Developer Environment

**Purpose:** Make the training runnable on the M5 Pro Mac. One-time setup, then invisible.

**User-facing surface:** A single setup script that takes a fresh Mac from "no Python" to "ready to train" in under 15 minutes.

**Internal components:**

- **Miniforge3 Python distribution.** The de-facto standard for arm64 Mac ML work. Installs via a single shell script. No Anaconda channel defaults; fully open-source.
- **Conda environment named `pinn-train`.** Isolates the project's Python and packages from system Python and from other projects. Python 3.11+.
- **ML framework.** The framework chosen per PH-1. The setup script installs it after the environment is created.
- **Utility packages:** numpy, h5py (or whatever the on-disk format needs per v1.5 PIPE-XX), pyyaml (for config files), tensorboard or chosen tracker.
- **One-command setup script.** A `setup.sh` or `Makefile` target that does all of the above idempotently.

**M5 Pro–specific notes:**

- Use the `Miniforge3-MacOSX-arm64.sh` installer.
- macOS 14.0+ is the minimum for PyTorch MPS; M5 Pro ships with macOS 15+.
- Total memory budget is 24GB; Subsystem 3's memory pressure is visible to the OS.

**Source grounding:**

- Miniforge3 README — `github.com/conda-forge/miniforge`
- PyTorch MPS notes — `docs.pytorch.org/docs/2.12/notes/mps.html`

### 4.2 Subsystem 2 — Data Ingestion

**Purpose:** Take the on-disk dataset and serve mini-batches to the training loop. Format-aware, framework-agnostic.

**User-facing surface:** None directly. Runs invisibly inside the trainer.

**Internal components:**

- **Adapter layer.** The only place in the trainer that imports disk-format libraries. If v1.5 PIPE-XX changes the on-disk format, only the adapter changes.
- **Split manifest.** A single file (saved to `runs/<name>/` or a shared location) that records which trajectories belong to train/val/test for a given run. Stratified by physical regime (chaotic / non-chaotic / boundary / special configurations per the dataset's metadata). Deterministic seed.
- **NaN/Inf filter.** Samples with non-finite values are dropped at load time, with a logged count.
- **Batch emitter.** Yields fixed-shape mini-batches. The trainer's loop iterates over these without knowing how they were produced.

**Surface commitments:**

- **Train split:** shuffled every epoch with a deterministic per-epoch seed.
- **Val / test splits:** iterated in a fixed order (no shuffle).
- **Sample-level vs. trajectory-level shuffling:** trajectories are shuffled first, then a fixed number of mini-batches are emitted per trajectory. This keeps temporal coherence within a batch.
- **Default split fractions:** ~80/10/10 (design intent; exact values depend on PH-5).
- **Data-version-mismatch check:** the adapter reads `data_version_hash` from the on-disk dataset and refuses to load if it doesn't match the version the trainer was built for. Hard error, no silent proceed.

**What this subsystem does NOT do:**

- Feature engineering (e.g., log-scaled masses, time normalization). Owned by `pinn_architecture.md` output head and `ctl_instruction.md` input vector formulation.
- Curriculum stage assignment. Owned by `ctl_instruction.md`.
- Physics-residual computation. Owned by Subsystem 3.
- Disk format itself. Owned by v1.5 PIPE-XX.

### 4.3 Subsystem 3 — Training Loop

**Purpose:** Actually train the model. Run an outer curriculum loop and an inner optimization loop. Write the run output directory.

**User-facing surface:** The five entry points described in Section 5.

**Internal components (framework-agnostic sketch):**

- **Curriculum state machine.** Driven by `ctl_instruction.md`. The trainer implements the spec, not the design.
- **Network.** Instantiated from a config-supplied architecture spec per `pinn_architecture.md`. Whether that's an MLP, a modified MLP, a transformer, or something else is the spec's call.
- **Loss computation.** A sum of three terms: data loss (against training trajectories), physics loss (against PDE residuals computed via autograd), IC loss (against initial-condition anchors). Exact weights and forms are owned by the framework specs.
- **Optimizer and LR schedule.** First-trial default: Adam with initial LR 1e-3 and exponential decay (rate 0.95 every 500 steps). Subject to PH-7.
- **Logging.** One line per `log_freq` steps (default 100). Contains: step number, three loss values, learning rate, time-per-step, ETA.
- **Checkpointing.** Every `checkpoint_every` steps (default 1000). Contains: model state, optimizer state, current step, current stage, RNG state.
- **Resume logic.** Same config file + checkpoint path → continue. Different config file → hard error.
- **Collocation sampling.** The trainer samples interior points for the physics loss term. Strategy per PH-6.

**Pattern grounding:** The plain-Python-loop style of the PhysicsNeMo inverse-PINN example is the reference shape: data loading, forward pass, loss, optimizer step, all written out explicitly. No heavy abstractions.

**Source grounding:**

- PhysicsNeMo inverse-PINN example — `github.com/nvidia/physicsnemo/blob/main/examples/cfd/inverse_pinns/README.md`
- PyTorch autograd mechanics — `docs.pytorch.org/docs/2.12/notes/autograd.html`

### 4.4 Verification layer (consumer of Subsystem 3's output)

**Purpose:** Tell the user whether training is healthy, better than before, or good enough.

**User-facing surface:** Three surfaces for three time scales (Section 6).

**Internal components:**

- **Live log emitter (inside Subsystem 3).** Writes to `runs/<name>/logs/train.log` and `train.log.jsonl`.
- **Run summary writer (at end of run).** Writes `runs/<name>/summary.md` and `summary.json`.
- **Test-set evaluator (separate script).** Reads a checkpoint, runs the test set, writes `eval/final-on-test/metrics.json` and `metrics.md`.
- **Gate checker (separate script or sub-step of evaluator).** Compares test-set metrics against the post-v1.3 gate (ε_H > 10⁻⁵, SCS > −5). Renders pass/fail.

---

## 5. User Runbook Surface

The user interacts with the training execution through five entry points. Each is a single user action. The internals behind each are not the user's concern.

### 5.1 Mental model

Before any commands, the user is told:

> "Training a model is like running a long calculation. You start it in a terminal. It prints progress. You can stop it anytime (Ctrl-C) and resume it later from where you stopped. The whole run produces a folder of files — the trained model, the training history, and a log. If something goes wrong, the log is the first place to look."

### 5.2 Entry point 1 — Setup (first time only)

A sequence of shell commands that takes a fresh Mac to "ready to train":

```
# Open Terminal, paste these one at a time:
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
# (close terminal, open a new one)
conda create -n pinn-train python=3.11
conda activate pinn-train
# (framework-specific install — command deferred to PH-1; see Section 7.1)
```

**On success:** terminal prompt starts with `(pinn-train) `.

**On failure:** red error message. First troubleshooting step: copy the error, paste it into a search engine, look for the exact same error string.

### 5.3 Entry point 2 — Configure (before each run)

The user edits (or copies) a single config file. The mechanical surface:

```
# File: configs/runs/my-run.yaml
run_name: my-first-run
data_version: <set by v1.5 PIPE-XX>
framework_device: mps    # auto, mps, or cpu
checkpoint_every: 1000
max_steps: 100000
# ... other knobs the user shouldn't touch yet are commented out
```

**Design intent:**

- One file per run, not a giant central config.
- All knobs the user shouldn't touch are commented out or hidden behind an "advanced" marker.
- Validation: if a required field is missing, the run refuses to start with a clear error.

### 5.4 Entry point 3 — Launch (each run)

A single command:

```
cd <home>/Desktop/3_body_problem
conda activate pinn-train
python -m pinn.train --config configs/runs/my-run.yaml
```

**What the user sees on screen (in order):**

1. Environment check: "Found device: mps. Memory available: ~22GB." (or a warning if MPS unavailable)
2. Data check: "Loading dataset v<hash>... N train trajectories, M val, K test. ETA 30s."
3. Curriculum state: "Starting at stage <N> of <M>."
4. First batch: "Step 0 / 100000. data_loss=X physics_loss=Y ic_loss=Z total=W lr=1e-3 (12s/step)"
5. Steady-state: a fresh line every `log_freq` steps (default 100). Same fields as step 0 plus an ETA.

**Stop rules:**

- Ctrl-C once → graceful shutdown, saves checkpoint at current step.
- Ctrl-C twice → immediate exit, no checkpoint.
- MacBook sleep / lid close → training continues when lid reopens (with caveats; see 5.10).

**Hard rule for the user:** "If you see three identical consecutive step lines with no progress (same step number, no new line for 5+ minutes), training is hung. Press Ctrl-C and read the troubleshooting section."

### 5.5 Entry point 4 — Monitor (while running)

**Primary surface:** live terminal log. The user reads the most recent few lines.

**Secondary surface:** browser-based dashboard via `tensorboard --logdir runs/<name>/` (or chosen tracker per PH-10). Plots of loss vs. step, learning rate schedule, validation curves.

**System monitoring (Mac-side):**

- Activity Monitor → Energy tab → check GPU usage isn't 0% (means training is CPU-only) and isn't 100% sustained with very low time-per-step variance (means the model is too small).
- Memory tab → if "Swap used" is non-zero and growing, the OS is thrashing.

### 5.6 Entry point 5 — Resume (after stop/crash)

A single command, mirroring Launch:

```
python -m pinn.train --config configs/runs/my-run.yaml --resume runs/<name>/checkpoints/latest.pt
```

**Resume invariants:**

- Same config file → same model architecture, same data version, same curriculum stage.
- A different config file → error, refuse to resume.
- No checkpoint found → error, with the path it looked at.

### 5.7 Run output structure

After a successful run:

```
runs/
  <name>/
    config.yaml                    # frozen copy of what was run
    checkpoints/
      step-001000.pt
      step-002000.pt
      latest.pt                    # symlink or copy of most recent
    logs/
      train.log                    # human-readable, full
      train.log.jsonl              # machine-parseable, one line per logged step
    summary.md                     # human-readable end-of-run summary
    summary.json                   # machine-parseable end-of-run summary
    status.json                    # one-line run summary
```

**User-facing meaning of each file:**

- `config.yaml` — proof of what was run. "What config produced this model?"
- `checkpoints/latest.pt` — the trained model. Load this to make predictions.
- `train.log` — read this when something looks wrong.
- `summary.md` — end-of-run one-pager. "How did it go?"
- `status.json` — first place to look. "Did the run finish? What was the final loss?"

**Contract:** "If a colleague asks you to reproduce your results, give them the `runs/<name>/` directory. Everything they need is in there."

### 5.8 Error surface

Categorized errors, each with a one-line user instruction:

| Symptom | What it means | User action |
|---|---|---|
| "MPS not available" | PyTorch can't reach the GPU | Check macOS version, reinstall PyTorch |
| "Data version mismatch" | Dataset on disk is newer than trainer expects | Update trainer, OR regenerate dataset |
| "CUDA out of memory" / "MPS memory pressure" | Model + batch too big for 24GB | Reduce batch size, OR check for memory leak |
| "NaN in loss" | Training diverged | Restore last good checkpoint, reduce learning rate |
| "Checkpoint not found" | Bad resume path | Check the path, OR start a fresh run |
| "Permission denied" | File ownership issue | `chmod` the directory (advanced — ask for help) |
| Three identical step lines, no progress | Training is hung | Ctrl-C, restore checkpoint, restart |

Anything more exotic gets categorized as "unknown error — copy the log, ask for help."

### 5.9 What's NOT in the runbook

- Hyperparameter selection. The first run uses documented defaults.
- Distributed training. Not on the table.
- Cloud fall-back. Out of scope per Q2 decision.
- Framework-specific internals. Invisible to the user.

### 5.10 M5 Pro–specific mechanical notes

- **Unified memory:** 24GB is the total budget. Watch memory pressure.
- **macOS 14.0+ required for MPS.** Always satisfied on M5 Pro.
- **Thermal throttling:** long runs heat the laptop. If the fan is at full speed and clocks are dropping below base, training is throttled.
- **Sleep behavior:** use `caffeinate -d` to prevent sleep during unattended runs.
- **No multi-MPS-device parallelism.** `torch.mps.device_count()` returns 1.

---

## 6. Verification & Assessment Surface

The user has three distinct questions at three distinct time scales. Each has its own surface, its own answer, and its own "what to do next."

### 6.1 Question 1 — "Is training healthy?"

**Time scale:** every ~5 minutes during a run.

**Primary surface:** the live terminal log. The user reads the most recent few lines and asks:

- Is the step number going up at roughly the rate the log claims?
- Are the loss values going down, even if slowly?
- Is the time-per-step stable?
- Is the learning rate what the config said it should be?

**Secondary surface:** the dashboard plot of total loss vs. step. Healthy vs. unhealthy patterns:

- **Healthy:** big drop in the first ~1000 steps, then a slow steady decline. Small wiggles are normal.
- **Plateauing too early:** the curve flattens before step 10k. Training is stuck.
- **Diverging / NaN:** the curve shoots up or shows `nan`. Training has failed.
- **Oscillating wildly:** the curve jumps up and down with no trend. Learning rate too high, or batch size too small.

**M5 Pro–specific liveness checks:**

- Activity Monitor → GPU utilization should be 60-95% during steady-state training. 0% means training is CPU-only.
- Memory tab → if "Swap used" is non-zero and growing, stop the run.

**User's action set during a run:**

| Observation | Action |
|---|---|
| Loss going down, GPU busy | Keep watching |
| Loss plateauing, GPU busy | Wait; some plateaus resolve after 10k more steps |
| Loss diverging, NaN appears | Ctrl-C, restore last good checkpoint, start a new run with smaller LR |
| Step number stuck 5+ minutes | Ctrl-C, check log tail, restore checkpoint, restart |
| Memory pressure climbing | Ctrl-C, reduce batch size in config, start a new run |
| MacBook hot, fans full, clocks throttling | Pause run, cool down, OR move to a cooler room |

### 6.2 Question 2 — "Is this run better than my last one?"

**Time scale:** end of run, before launching the next one.

**Primary surface:** a run-comparison report. After every run, the trainer writes a one-page summary into `runs/<name>/summary.md`.

**`summary.md` contains, in order:**

1. **Run header** — name, start time, end time, total wall-clock time, framework device used.
2. **Final losses** — data loss, physics loss, IC loss, total. With their units in plain English.
3. **Validation curves summary** — "validation loss decreased steadily; final value 1.2e-4 at step 95,000."
4. **Curriculum progression** — "Started at stage 1, advanced to stage 3 at step 40,000, advanced to stage 5 at step 70,000."
5. **Test-set preview** — small subset of test trajectories with predicted-vs-true plots.
6. **Comparison hint** — if a previous run is named, "vs. my-previous-run: total loss 3.2× lower, val loss 2.1× lower."

**To compare two runs:** open both `summary.md` files. The numbers at the top are the answer.

### 6.3 Question 3 — "Is this model good enough?"

**Time scale:** milestone boundary (end of a phase or milestone, before declaring work "done").

**Primary surface:** test-set assessment + gate check. The full test set is evaluated **once** at the very end, by a separate script:

```
python -m pinn.evaluate --checkpoint runs/<best-run>/checkpoints/latest.pt --output eval/final-on-test/
```

**Output:**

```
eval/final-on-test/
  metrics.json             # all metrics, machine-parseable
  metrics.md               # human-readable, with the gate verdict
  per-trajectory/          # per-trajectory breakdown if a sample failed
  plots/                   # diagnostic plots
```

**The gate check is binary and visible.** The post-v1.3 gate is the published acceptance criterion: ε_H (energy error) > 10⁻⁵ and SCS (some chaos signature) > −5. The `metrics.md` file renders:

```
## Gate Check
- ε_H: 8.2e-6  (required: > 1e-5)  → ❌ FAIL
- SCS: -3.4    (required: > -5)    → ✅ PASS

OVERALL: ❌ FAIL
```

**Plain-English descriptions** for each metric, in `metrics.md`:

- **ε_H (energy error):** "How much the model's predicted orbits drift from perfect energy conservation. Smaller is better. < 10⁻⁵ is excellent."
- **SCS (some chaos signature):** "How well the model captures sensitive dependence on initial conditions. Larger is better. > -5 is acceptable."

The user can read these without a physics background. They can act on the pass/fail without understanding the math.

**M5 Pro–specific note on test-set evaluation:** Full test-set evaluation is one forward pass with no gradient computation. Much faster than training — typically 5-15 minutes on M5 Pro for the expected test-set size.

### 6.4 The honesty layer

Three rules the user is taught explicitly:

> **"Healthy validation loss ≠ working model."** A model can have low training loss and low validation loss and still fail the gate. The test set is the only honest answer.

> **"Comparison to previous run ≠ progress."** A run that beats the previous run on validation can still fail the gate. Comparison is for *picking* which run to evaluate on test, not for *claiming* success.

> **"A clean loss curve ≠ correct physics."** A PINN can fit the data loss to zero and still get the physics wrong. The gate is what catches this.

### 6.5 Outcome-level failure modes

Beyond the loss-curve shapes in 6.1, there are *outcome-level* failure modes the user sees at the end of a run:

| Failure mode | Symptom in `summary.md` | What it means | What to do |
|---|---|---|---|
| **Memorization** | Train loss near zero, val loss much higher | Network memorized train trajectories but doesn't generalize | Model too small, OR data too small, OR data leak between splits |
| **Mode collapse** | Predicted trajectories all look the same | Network learned a degenerate solution | Bad initialization, OR learning rate too high, OR data has a dominant regime |
| **Energy drift** | Test-set ε_H fails gate | Network doesn't conserve energy | Physics loss term underweighted, OR model can't represent the dynamics |
| **Chaos-blind** | Test-set SCS fails gate | Network doesn't capture sensitive dependence | Network too smooth (activation choice), OR collocation sampling too coarse |
| **Numerical blow-up** | Predicted trajectories have NaN/Inf outside training time range | Network is unstable past training horizon | Output scaling wrong, OR no regularization on higher-order derivatives |

The user does not need to *fix* these — they need to *name* them. The runbook translates "the loss curve looks weird" into "this looks like memorization" so the user can report it precisely.

### 6.6 What's NOT in the verification layer

- Per-batch metric computation. Internal; surfaced only as the loss log line.
- Hyperparameter sweep tooling. Out of scope.
- A/B testing of architectures. Out of scope.
- Cross-run statistical comparison. `summary.md` includes a hint, not a full analysis.
- Human evaluation of trajectory plots. Plots are generated; user can look but isn't required to.

---

## 7. Placeholders — Internals Awaiting External Research

Each placeholder is something this design **does not** decide. Each is paired with a research question that, once answered, will produce the actual decision.

### 7.1 PH-1. ML framework choice

- **Status:** Framework-agnostic design. The trainer writes against an abstraction; the framework is plugged in.
- **Why deferred:** STOP protocol — framework choice is exactly a "candidate verdict source" decision that needs external research.
- **Research question:** Among PyTorch+MPS, MLX, JAX+Optax+Equinox, which is the best fit for (a) a non-expert user maintaining a single training script, (b) autograd-friendly physics-residual computation, (c) Apple Silicon native performance, (d) long-term ecosystem support for a research project?
- **Sources to consult:** PyTorch MPS docs, MLX README, JAX documentation, NVIDIA PhysicsNeMo's PyTorch-based example as a reference shape.
- **Output:** A framework decision document, one paragraph per candidate with a clear recommendation and rationale.

### 7.2 PH-2. Curriculum stage design and promotion rules

- **Status:** Owned by `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.
- **Why deferred:** The spec exists; this design doesn't re-derive it.
- **Research question:** None — the spec is the source. The trainer's job is to *implement* the spec, not to *decide* the spec.

### 7.3 PH-3. Loss formulation (weights, terms, regularization)

- **Status:** The trainer computes a combined loss; the exact terms and weights are owned by `pinn_architecture.md` and `ctl_instruction.md`.
- **Why deferred:** Same as PH-2 — the framework spec is the source.
- **Surface commitment:** The loss will be a sum of three terms: data loss (against training trajectories), physics loss (against PDE residuals), IC loss (against initial-condition anchors). The exact mathematical form of each term is the spec's responsibility.

### 7.4 PH-4. Network architecture

- **Status:** Owned by `pinn_architecture.md`. This design *consumes* whatever that spec says.
- **Why deferred:** Same as PH-2 and PH-3.
- **Surface commitment:** The trainer instantiates a network from a config-supplied architecture spec.

### 7.5 PH-5. Train/val/test split fractions and stratification policy

- **Status:** Defaults proposed as design intent (80/10/10, stratified by physical regime), but exact values are a research question.
- **Why deferred:** The dataset's size, regime distribution, and inter-trajectory variance are empirical facts that affect the right split.
- **Research question:** With the actual `simulation_data/` size and regime distribution, what split fractions give sufficient statistical power on the test set for the SCS/SASD/IPR/PSC metrics?
- **Output:** A split policy paragraph in a future spec, owned by v1.5 or whoever measures this first.

### 7.6 PH-6. Collocation sampling strategy

- **Status:** The trainer samples interior points for the physics loss term. The strategy is undecided.
- **Why deferred:** Collocation sampling is a deep topic in PINN literature. The right choice depends on the problem's geometry, the network's capacity, and empirical results.
- **Research question:** For the three-body phase space and the regime distribution in `simulation_data/`, what collocation strategy (uniform random, low-discrepancy, residual-based adaptive, time-dependent) is the right starting point?
- **Sources to consult:** PINN literature surveys, Wang et al. 2023 "An Expert's Guide to Training PINNs," PhysicsNeMo examples.
- **Output:** A collocation-strategy paragraph in a future spec, owned by doc-03.

### 7.7 PH-7. Optimization algorithm and learning rate schedule

- **Status:** Trainer runs an optimizer. Specific algorithm and schedule are a research question.
- **Why deferred:** Adam is the safe default; whether Adam, AdamW, L-BFGS, or a custom schedule fits this problem is empirical.
- **Research question:** What's the right optimizer + LR schedule for a PINN on three-body trajectories, starting from a documented first-trial default?
- **First-trial default:** Adam with initial LR 1e-3 and exponential decay (rate 0.95 every 500 steps). This is the PhysicsNeMo example's default and is a reasonable starting point. The user is told this is a *first trial* and we will adjust based on observed loss curves.
- **Output:** An optimizer-config paragraph in a future spec, owned by doc-03.

### 7.8 PH-8. CPU/GPU co-utilization strategy

- **Status:** Desired (per user direction), exact mechanism undecided.
- **Why deferred:** The M5 Pro's unified memory makes "CPU+GPU co-utilization" mean different things in different frameworks. PyTorch MPS can use CPU for data loading while GPU computes, but the data-loader worker count is empirical. MLX has unified memory natively.
- **Research question:** Once the framework is chosen (PH-1), what is the recommended pattern for utilizing both CPU (data loading, augmentation) and GPU (forward/backward pass) on the M5 Pro with 24GB unified memory?
- **Sources to consult:** PyTorch DataLoader docs, MLX unified-memory design notes, community blog posts on M-series ML performance.
- **Output:** A short paragraph in a future spec, owned by doc-03 or whoever implements Subsystem 3.

### 7.9 PH-9. Checkpoint format and resume semantics

- **Status:** Checkpoints contain model state + optimizer state + step + stage. Exact on-disk format (pickle, torch.save, MLX save, custom) depends on the framework.
- **Why deferred:** Framework choice (PH-1) determines this.
- **Surface commitment:** Whatever the framework provides. No custom format invented here.

### 7.10 PH-10. Experiment tracking (TensorBoard vs. W&B vs. MLflow vs. none)

- **Status:** Opt-in dashboard in the runbook. Tool selection deferred to PH-10.
- **Why deferred:** TensorBoard is the lowest-friction default and works with most frameworks. W&B requires an account. MLflow is heavy. The right choice depends on whether the user wants offline-only, cloud-synced, or both.
- **Research question:** What experiment tracker is best for a single-user, single-machine, no-cloud PINN training project?
- **First-trial default:** TensorBoard for the first run, no commitment to a specific tracker.

### 7.11 Research priority order

| # | Question | Blocking for |
|---|---|---|
| 1 | ML framework choice (PH-1) | Subsystem 3 implementation |
| 2 | Optimizer + LR schedule (PH-7) | First-trial config |
| 3 | Collocation sampling strategy (PH-6) | First-trial config |
| 4 | CPU/GPU co-utilization on M5 Pro (PH-8) | Subsystem 3 performance |
| 5 | Split fractions and stratification (PH-5) | Subsystem 2 implementation |
| 6 | Experiment tracker choice (PH-10) | Monitoring surface |

Items 1-3 are needed before the first real training run. Items 4-6 can be researched in parallel and folded in later.

---

## 8. Sources Consulted

External sources consulted during the brainstorm session that shaped this design:

| # | Source | Used for |
|---|---|---|
| S-1 | `docs.pytorch.org/docs/2.12/notes/mps.html` | PyTorch MPS device idiom, macOS 14.0+ requirement, memory APIs |
| S-2 | `docs.pytorch.org/docs/2.12/mps.html` | `torch.mps` module reference (is_available, empty_cache, profiler) |
| S-3 | `github.com/ml-explore/mlx` README | MLX unified memory model, Apple-Silicon-native design |
| S-4 | `github.com/nvidia/physicsnemo/blob/main/examples/cfd/inverse_pinns/README.md` | PINN training loop pattern, Adam + exponential LR schedule, scalar residual reporting cadence, non-abstracted style preference |
| S-5 | `github.com/conda-forge/miniforge` README | Miniforge3 install procedure, arm64 Mac installer, environment creation workflow |
| S-6 | `docs.pytorch.org/docs/2.12/notes/autograd.html` | `torch.autograd.grad` for physics-residual computation pattern |

These are starting references for the project's own runbook, not substitutes for one. The project's runbook will be written to `docs/runbooks/` and will cite these plus additional sources discovered during implementation.

---

## 9. Open Questions for the User

These are decisions only the user can make.

1. **Framework choice (PH-1).** This is the single biggest open question. It blocks the most downstream work. Recommend: dedicated research session before the first training run.
2. **How "researched" the first run should be.** Two options:
   - (a) First run uses documented defaults (Adam, simple collocation, 80/10/10 split, etc.) and we learn from the result.
   - (b) First run waits until a deeper research review is done.
   - Recommend: (a).
3. **Whether to commit this framework-agnostic design as the baseline spec or wait for the framework decision and write a framework-specific spec.** Recommend: commit this now as the baseline; the framework-specific internals can be added in a follow-up spec.

---

## 10. Future Use of This Spec

This spec is a **frozen reference design document** for the CTL-PINN training execution pipeline. The brainstorm session that produced it is complete; this document is the artifact.

**Immediate next steps (this session):**

1. **User reviews this spec** for any changes.
2. **Spec is committed to git** per the project's git guidelines (`docs(<scope>): ...` or `spec(<scope>): ...`).

**What this spec is for, later:**

- This document is the **starting reference** for the training-pipeline side of the user's future build effort. The user will be building the entire codebase and project — including the actual PINN code (the theoretical/scientific side, owned by the framework specs) **in parallel with** the training pipeline (the mechanical side this spec describes). When that build effort begins, the user will refer back to this spec to recall the mechanical design decisions captured here.
- The **10 placeholders (PH-1 through PH-10)** in Section 7 are the decisions waiting to be revisited when the build begins. They are not blocking the spec; they are the *work-to-come markers*. The largest is PH-1 (ML framework choice), recommended as the first research session when build work starts.
- The **3 open questions in Section 9** are also decisions waiting for the user.

**No implementation plan is produced now.** The training pipeline does not have a near-term execution target. The scientific side (PINN code, loss, architecture, curriculum) is being designed separately, in the framework specs and the v1.5 phases. Producing a build plan now would be speculative: there is no concrete target, and the placeholders would force the plan to be mostly placeholders itself. When the user is ready to start building, a fresh brainstorm can produce a plan based on this spec as input.
================================================================================
END ORIGINAL: 2026-06-10-training-execution-design.md
================================================================================

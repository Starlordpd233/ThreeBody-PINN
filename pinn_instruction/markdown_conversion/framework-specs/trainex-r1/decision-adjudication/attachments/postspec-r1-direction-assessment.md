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

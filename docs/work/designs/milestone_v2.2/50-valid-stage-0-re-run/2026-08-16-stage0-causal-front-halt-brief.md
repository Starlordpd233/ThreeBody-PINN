---
status: active
purpose: other
created: 2026-08-16
milestone: v2.2
phase: 50-valid-stage-0-re-run
retirement_trigger: After Phase 50 closes and a later grounded diagnosis or owner ruling supersedes this snapshot
---

# Stage-0 causal-front halt — owner brief

**Date:** 2026-08-16
**Audience:** the project owner, as a later-readable explanation
**This document is:** a plain-language snapshot of what Phase 50 is, what the seed-41 halt means, and what is *not* known
**This document is not:** a recipe change, a later-generation authorization, a prediction that a retry will pass, or a reopening of GAP-50-03

If anything here conflicts with a committed Phase 50 artifact, the committed artifact wins.

---

## 1. What this project is trying to do

The repository builds a **physics-informed neural network (PINN)** for the gravitational **three-body problem**: three masses moving under Newton’s law.

A PINN is not a traditional simulator. A simulator such as Brutus steps the true equations forward in time and writes a trajectory. The PINN is a network that *guesses* positions as a function of time and initial conditions. Training tries to make those guesses:

1. match the recorded simulation data, and
2. obey the same physics those simulations used.

Phase 50 is the first **valid Stage-0 re-run** of that training experiment, after earlier phases repaired the code so it matches the locked specs. “Valid” here means: run the specified experiment honestly, and if a designed safety gate fires, record that stop instead of quietly retuning numbers to make the run look finished.

The phase is **not** finished just because plans and tests exist. The ROADMAP still requires a full graded run on which the progress gates hold, and a three-seed characterization of validation error. Those are still false.

---

## 2. The two grades the network receives

Imagine a student who must reconstruct a movie of three bodies.

**Data grade.** Compare the student’s frames to the recorded movie (the Brutus trajectories we already trust).

**Physics grade.** Ignore the movie for a moment. Plug the student’s frames into Newton’s laws. If the laws are satisfied, the leftover is zero. If not, the leftover is the **residual**.

A residual is just “how physically inconsistent is this guess?” Residual near zero means the predicted motion could have come from Newton. A large residual means the predicted motion is not a legal gravitational trajectory.

The physics in question is ordinary:

- Gravity with `G = 1`
- Softening `eps_soft = 1e-5` so two bodies never quite sit on top of each other
- A mass-weighted center-of-mass constraint so the system does not drift as a whole

Nothing in the halt record says those laws were written down wrong, or that Brutus is the problem. The halt is about **whether this network learned to satisfy them in the earliest part of time**.

---

## 3. Why training is not “physics everywhere at once”

Chaotic three-body motion is hard. If the network is punished equally for being wrong at late times while it is still wrong at early times, it can “cheat” later times with nonsense and never lock the opening.

So this project uses a **causal curriculum** — a teaching order, not a new law of nature.

Time is split into bins, like measures of a song: first the opening, then a little later, then later still.

- The opening bin always matters.
- Later bins are allowed to matter only after earlier bins are already reasonably clean.
- The **causal front** is how far into the song the student has earned the right to practice.

In the code this is a set of weights `w_n` on each time bin:

- The first weight is always `1`.
- Each later weight is `exp(−η_c × (sum of earlier residuals))`, with `η_c = 1`.
- If earlier residuals are large, later weights collapse toward zero. The network is told: “do not spend effort on the ending until the beginning is decent.”

The controller then reports a single integer, `front_idx`: the last bin whose weight is still above `0.5`. That number is a **progress meter**, not a second physics equation.

With the locked settings, `front_idx = 0` means only the first bin is above that 0.5 bar. Algebraically, the first bin’s mean squared residual has not yet dropped below `ln(2) ≈ 0.69`. That is a fact about the residual staying large. It is **not** a diagnosis of *why* it stayed large.

---

## 4. What “invariant B” is

You already set a classroom deadline so a stuck student cannot practice forever:

> If the front does not move forward within **N = 500** training steps, stop.

That deadline is **invariant B**. It is owner-ratified (`N = 500 = 0.5 ×` the 1000-step Adam budget). It is not a constant of nature. Agents are forbidden to raise, soften, or bypass it after watching a run fail.

If the front never leaves bin 0, the guard fires at step 501 and writes a failure bundle. That is the gate working.

There is a sibling rule, **invariant A**: no causal weight may be exactly zero. The seed-41 halt was invariant B, not A.

---

## 5. What actually happened on generation 3

The only graded launch in generation 3 was seed 41.

| Fact | Record |
|---|---|
| What fired | `guard = invariant_b` |
| When | step **501** |
| Deadline | `N = 500` |
| Progress meter | `front_idx = 0` on **all 502** logged steps |
| Seeds 42 and 43 | never launched |
| Three-seed band | does not exist |
| Phase goal | not met |

The written reason is: “causal front high-water mark did not advance within N=500 steps.”

In ordinary language: **for 500 training steps, the network never got the opening of the trajectory physically clean enough to unlock later time, so training was stopped.**

That is a designed stop, not a crash, and not a proof that Newton is false.

---

## 6. Is the math or physics wrong?

**No grounded source says the physics formulas are wrong.**

The locked diagnosis classified three separate findings. They do not share one remedy.

| Class | What it is | Did it cause the halt? | What was done |
|---|---|---|---|
| Validation conversion bug | On the Mac GPU (MPS), the extra “how well are we doing?” check used an illegal one-step number conversion and threw `TypeError` | **No.** The progress guard runs *before* that check | Repaired: detach → move to CPU → then convert to float64 |
| Log overwrite | On some steps, the notebook wrote validation numbers over the training numbers | **No.** The guard still saw the training numbers | Repaired the log only. Teaching rule unchanged |
| Causal-front “the network didn’t move” | `front_idx` stayed 0 until the deadline | This *is* the halt | **No recipe change.** Current sources name no wrong formula and no authorized fix |

So two **scorekeeping** defects were real and are now repaired. They explain missing validation scores, not the stuck front.

What the diagnosis does *not* claim:

- that Newton, energy, or the three-body residual is mis-derived
- that the causal-weight formula is implemented differently from the spec
- that `N = 500` was a coding error
- that we know *why* the first-bin residual stayed above the bar
- that another unchanged run will pass, fail, or halt again

The official classification is:

```text
grounded_causal_front_repair: none-in-current-sources
later_generation_likelihood_claim: prohibited
```

---

## 7. The scientific problem, in one paragraph

The network is a function approximator. The physics residual tells it how illegal its current movie is. The causal front withholds later-time credit until the opening residual is small enough. On this Stage-0 recipe, seed 41 never crossed that opening bar in 500 steps. That can happen when the opening is hard, when 500 steps is short for this architecture, when this initial condition is awkward, or for reasons we have not isolated. **We do not have a grounded “because” yet.** Treating the halt number as a license to change `N`, the residual bar, or other recipe knobs would be result-driven tuning, which this phase forbids.

A useful analogy: a piano student is only allowed to practice later measures after the first measure is clean. After 500 attempts the first measure is still not clean, so the teacher stops the lesson. That does not mean the sheet music is wrong. It means this student, with this method, did not clear the opening in the allotted time. We do not yet know whether they need more attempts, a different method, or a different first piece.

---

## 8. Why the project stopped to ask you

Two standing rules collide with “just try again and tweak it”:

- **D-19 / SCOPE-29.** Inside this phase, the only legal code edit is a conformance repair: make the implementation match a locked spec *without* using the observed run as the justification. The two scorekeeping bugs were that kind of repair. Changing the teaching rule because `front_idx` stayed 0 is not.
- **D-20.** An invariant-B halt is an **owner checkpoint**, not a number for an agent to adjust. `N` stays 500 unless you re-rule it.

Generation 3 is therefore closed as honest terminal history (GAP-50-03, Option A): accept the halt, do not invent a band, do not launch 42/43 at that head, do not change `N`.

A later generation is a **new experiment**, not a continuation of generation 3. It needs a separate owner yes, and even then a “yes, preregister the same recipe” is not a forecast that the front will move.

The open 50-08 question is only:

1. **Authorize unchanged-recipe preregistration** — write down a generation-4 identity. Still not a launch.
2. **Supply a grounded causal remedy** — you bring a sourced change; we stop and replan. No inline recipe edit.
3. **Stop incomplete** — leave RUN-01 / RUN-02 open.

---

## 9. Where to read the official record

| If you want… | Read |
|---|---|
| The halt itself | `.planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/failure/trip.json` |
| Why we must not invent a dynamics fix | `.planning/phases/50-valid-stage-0-re-run/evidence/causal-front-diagnosis.md` |
| Phase goal vs what shipped | `.planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md` |
| The three owner options | `.planning/phases/50-valid-stage-0-re-run/50-08-SUMMARY.md` (draft brief; decision not yet recorded) |
| Generation-3 ruling | `.planning/phases/50-valid-stage-0-re-run/50-GAPS.md` (GAP-50-03, Option A) |
| Standing halt policy | `.planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md` (D-19, D-20) |

---

## 10. Snapshot of project state when this brief was written

- Branch: `milestone/v2.2` in the trainex worktree
- Plans 50-01 through 50-07: complete
- Plan 50-08: owner checkpoint; brief written, decision not committed
- Plans 50-09 through 50-12: not started
- ROADMAP success criteria 2 and 3: still false
- RUN-01 / RUN-02: still pending
- No generation-4 artifacts
)

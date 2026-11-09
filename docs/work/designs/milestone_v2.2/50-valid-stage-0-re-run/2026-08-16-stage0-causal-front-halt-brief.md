---
status: active
purpose: other
created: 2026-08-16
milestone: v2.2
phase: 50-valid-stage-0-re-run
retirement_trigger: After Phase 50 closes and a later grounded diagnosis or owner ruling supersedes this snapshot
amended: 2026-08-17
---

# Stage-0 causal-front halt — owner brief

**Date:** 2026-08-16 · **Amended:** 2026-08-17 (sections 11 and 12 added; sections 1-10 unchanged)
**Audience:** the project owner, as a later-readable explanation
**This document is:** a plain-language snapshot of what Phase 50 is, what the seed-41 halt means, and what is *not* known
**This document is not:** a recipe change, a later-generation authorization, a prediction that a retry will pass, or a reopening of GAP-50-03

If anything here conflicts with a committed Phase 50 artifact, the committed artifact wins.

> **Read this first (2026-08-17).** Sections 1-10 below are the original 2026-08-16 text and are left untouched. Two things have since been done, and both change what the open question actually is:
>
> 1. The **retained 502-step training log** — already committed as terminal evidence, never mined — was read.
> 2. A **bounded read-only conformance audit** of the residual frame was run, as the cheapest gate before any external research.
>
> The audit came back **clean**: the physics is implemented correctly. The magnitude of the residual is a property of the locked architecture at initialization, not a bug. **Section 11** gives the numbers; **section 12** restates what each of the three options in section 8 now means. Full working: `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`.
>
> Section 7's sentence "we do not have a grounded *because* yet" is the one statement below that the amendment supersedes. We now do.

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

---

# Amendment — 2026-08-17

Nothing in this amendment changes any file, config, recipe, or decision. No option in section 8 is selected. GAP-50-03 is untouched.

## 11. What the retained log and the conformance audit found

### 11a. The numbers that were already in the record

The residual the student is being graded on — call it `R̄₁`, the leftover in the very first time bin — is recorded on every one of the 502 logged steps. Nobody had read it. Here is what it says.

| Quantity | Value |
|---|---|
| First-bin residual `R̄₁` | median **2.5 × 10¹⁰** (range 6.5 × 10⁸ – 3.9 × 10¹¹) |
| Bar the residual must clear to move the front | `ln 2` = **0.693** |
| Distance from that bar | **10.6 decades** |
| Point past which the weight formula `exp(−R̄)` cannot even be represented in 32-bit arithmetic | `R̄ > 87.3` — i.e. **8.5 decades below where we sat** |
| Change over the 402 steps at full physics weight | **−0.26 decades total**, inside the step-to-step noise |
| Weights on bins 2-16 | pinned at the smallest representable positive number on **502/502** steps |
| Data grade | 0.073 → 0.021, improving cleanly |
| IC (opening-condition) grade | median 2.9 × 10⁴, never settles |

The section 7 reading — "500 steps may be short, this IC may be awkward" — does not survive these numbers. The **smallest** residual ever seen in the whole run was seven orders of magnitude past the point where the causal formula stops carrying any information at all. The teaching mechanism was not slow; it was switched off for the entire lesson.

### 11b. The conformance audit: is the physics implemented wrong?

The first suspicion was a units error — that the code compares an acceleration measured in one time unit against a force measured in another, which would leave a large fake leftover even on a perfect trajectory. **It does not.** Four independent checks agree:

1. **The unit system closes exactly.** The project's length scale `D` and time scale `T` are tied by `D³ = G·T²` — that is the locked convention, and with `T = 10` it gives `D = 4.6416`, so `D³ = 100 = T²`. That identity is precisely what makes the scaled equation have coefficient 1, with no leftover factor.
2. **The written spec says what the code does**, clause for clause — the time coordinate, the "no extra chain factor" rule, the softening, the residual, the weight formula, the constants.
3. **The data on disk is already in the same scaled units** as the network's output, so there is no hidden conversion anywhere in the loop.
4. **A committed 2026-07-13 probe already proved it empirically.** Run on a real Brutus trajectory — a movie we know is physically correct — the same code produces a leftover of **0.65 %**. A units error of the suspected kind would have shown up as **9,900 %**. A companion check matched the gravitational force against the energy gradient to 15 decimal places.

**Verdict: the physics is right. There is no bug to fix here.**

### 11c. So where does 10¹⁰ come from?

From the network itself, before it has learned anything.

The residual asks for an **acceleration** — a second derivative, a rate of change of a rate of change. Second derivatives are brutally sensitive to wiggle. A small ripple that is fast is nearly invisible in position and enormous in acceleration: the amplification goes as the *square* of the frequency.

The chosen architecture is a SIREN, and it is deliberately built to start out wiggly — a high starting frequency (`ω₀ = 30`) is injected on purpose so the network can represent fine detail rather than being biased toward smooth blobs. Twelve layers compound it further.

Building the locked architecture and measuring it **before any training, on no data at all**, across five random seeds and two different initial conditions:

| What | Measured at initialization | What a physical trajectory would give |
|---|---|---|
| Positions | ≈ 1 | ≈ 1 ✓ |
| Velocity (1st derivative) | 230 – 330 | ≈ 1 |
| Acceleration (2nd derivative) | ≈ 2 × 10⁵ | ≈ 1 – 10 |
| Gravitational force | 2 – 6 ✓ | 2 – 6 ✓ |
| Closest approach between bodies | 0.5 – 0.9 | — (softening is 0.00001, so nothing is near-colliding) |
| **Residual `R̄`** | **≈ 10¹⁰** | ≈ 0 |
| **`front_idx`** | **0** | — |

Three readings follow:

- **Gravity is fine.** The force term comes out at the right size, and the three bodies are nowhere near each other, so no near-collision blow-up is involved. The network's own acceleration is 30,000-90,000 times larger than the gravitational force it is being compared against, so the "leftover" is essentially all network and a few thousandths of a percent gravity.
- **`R̄ ≈ 10¹⁰` and `front_idx = 0` are the *starting* values** — true at step zero, for every seed, with no data in sight. Seed 41's median of 2.5 × 10¹⁰ across 502 steps *is* the initialization value. The run never left the state it began in.
- **The same thing happened in the v2.0 pilot** (`front_idx = 0` on 1500/1500 steps in 5/5 runs, residuals 10⁸–10¹⁰) on a different code state. Three independent settings, one number.

### 11d. The mechanism, in one paragraph

The piano analogy in section 7 needs one correction. It is not that the student failed to clean the first measure in 500 attempts. It is that **the grading rule was designed for a student who is already roughly in tune.** The weight formula `exp(−η_c · R̄)` with `η_c = 1` treats a residual of about 1 as "acceptable" and about 0.7 as "clean enough to move on" — which is exactly what a *converged* network gives (0.65 %, per the probe on real data). A freshly initialized SIREN gives 10¹⁰. At that value every later bin's weight collapses to the identical smallest-possible number, so the weight vector carries no information: it cannot rank bins, `front_idx` is arithmetically incapable of being anything but 0, and the physics gradient reaches exactly **one** of the 16 time points — a different randomly drawn one each step.

Both halves of the design are individually sound and internally consistent. The architecture section chooses a network whose acceleration starts at 10⁵; the loss section chooses a curriculum tolerance calibrated for a residual near 1. **The gap is between them, and it is a design-calibration question, not an implementation defect.**

## 12. What this means for the three options in section 8

The standing rules are unchanged, and they still bind:

- **D-19 / SCOPE-29** — the only legal code edit inside this phase is a conformance repair. The audit found no mismatch, so **there is no conformance repair available.** That is not a loophole closing; it is the honest result.
- **SCOPE-30** — no framework-spec file may be edited anywhere in v2.2. The remedy surface (the causal tolerance `η_c`, whether the residual is normalized before weighting, the network's starting frequency) lives entirely in `pinn_architecture.md`.
- **D-20** — `N = 500` stays 500 unless you re-rule it. Nothing above touches `N`, and nothing above is a reason to.
- **Prohibited, and observed:** no statement here forecasts what any future run would do.

With that, the three options mean:

| Option | What it now means |
|---|---|
| **A — authorize preregistration** (unchanged recipe, generation 4) | Still available and still legal. You are entitled to know before choosing it that the blocking quantity is set at initialization by the architecture and came out at ≈ 10¹⁰ with `front_idx = 0` for every initialization seed measured (41, 42, 43, 0, 7) and for both initial conditions tried. This is not a prediction — it is a description of the starting state a generation-4 run would also begin from. |
| **B — supply a grounded remedy** | The remedy is now *identified* (recalibrate the causal tolerance against the actual residual scale, and/or normalize the residual before weighting, and/or reduce the starting derivative scale) but it **cannot land inside v2.2**: every candidate is a framework-spec edit, barred by SCOPE-30. Choosing B means "stop here and move the question", not "patch it now". |
| **C — stop incomplete** | Leaves RUN-01 / RUN-02 honestly open, which is what they are. It spends no further compute on a recipe whose blocking mechanism is now understood, and it is the option that violates no standing boundary. |

### Where the question goes next

`.planning/REQUIREMENTS.md` already anticipated this exact situation, before any of it happened:

> **v2.3 recipe adjudication** — if the conformant run still fails, that failure is the first real evidence about the design; recipe adjudication follows with the trainex-r2 resolution doc as a premise-qualified candidate verdict source (SCOPE-29/31).

That is where we are. The conformant run failed, and now it is characterized. A **new external research round is not the cheapest next step**: the trainex-r2 report already named this mechanism, the milestone plan already designates v2.3 as the vehicle, and SCOPE-31 forbids leaning on that report as grounding inside v2.2 anyway.

**Recommendation (yours to accept or reject):** option **C**, then open v2.3 recipe adjudication against the existing trainex-r2 report, carrying this audit as the new evidence. Option **B** is defensible if you would rather record the remedy direction now and let the replan carry it; the two land in nearly the same place. Option **A** is the one the new evidence argues against, because a generation-4 run at the unchanged recipe would begin from the same measured starting state and would be graded by the same saturated mechanism.

This section recommends. It does not decide. The 50-08 decision remains yours, unrecorded, and no artifact has been written on the strength of it.

---
title: Trainex R1a Research Context Master — Core Decisions and Structure
package_for: trainex-r1a (decisions-and-structure half of the foundational research round)
role: research-context entry point (orientation, constraints, decision areas D1–D7, baseline critique mandate, output contract)
status: active
created: 2026-06-11
source_baseline: c17e23ed0642f01d2eda7e7f65c0f18ed7081487
self_contained: true
---

# Trainex R1a Research Context Master — Core Decisions and Structure

This file is the research-context entry point for **trainex R1a**, the
decisions-and-structure half of the foundational research round for the CTL-PINN
training-execution development ("trainex"): the pipeline, tooling, and step-by-step user
runbook through which a non-expert project owner will train, monitor, and assess a
curriculum-trained physics-informed neural network (CTL-PINN) for the gravitational
three-body problem on a single MacBook.

**The round is split in two.** R1a (this package) covers the core **decisions and
structural questions** — your deliverable is options menus and a decision sheet. A
companion package, R1b, covers runbook and operations **knowledge** (training-health
watchlists, unattended-laptop operations, runbook patterns, feasibility estimates) and is
researched separately in parallel. Stay within R1a's scope; where your work would benefit
from R1b's findings (notably run-duration estimates), note the dependency explicitly
rather than attempting that research yourself.

**R1's purpose:** settle, as early as possible, the core decisions that will heavily
influence every later trainex design — so that later rounds (R2: numeric tuning of
optimizer/learning-rate and collocation values *within* the skeleton R1 fixes) only
adjust inside that structure, leaving flexible room without rework.

**The project owner makes the final decisions.** Trainex is built around reality training
driven by a user runbook, so for every decision area below your job is to lay out the
viable options with their consequences and suggest a default — not to decide. Do not
collapse a decision menu into a single verdict.

**You are working from attached files only.** You have no access to the project's
repository. The three attached project documents are verbatim snapshots and may mention
files or paths that are not attached; treat any such reference as unavailable — note it
in the claims-and-uncertainty register if it matters — rather than guessing at its
content. Alongside this file, you have been given exactly three other documents,
referred to throughout by filename:

| File | Role | How to treat it |
|---|---|---|
| `2026-06-10-training-execution-design.md` | The training-execution reference design this round comes from (its Section 7 placeholders are the origin of the decision areas below) | **Baseline from a brief early brainstorm — a default starting point, not fixed structure.** See "Hard Constraints vs. Baseline Design Intent" and the Baseline Critique Mandate below. Its "first-trial defaults" are proposals, not constraints. |
| `pinn_architecture.md` | Authoritative framework spec — network architecture, autodifferentiation (AD) contract, output head | Source of truth. Your options must be implementable against it; it is not yours to change. |
| `ctl_instruction.md` | Authoritative framework spec — CTL methodology, curriculum staging, input-vector formulation | Source of truth, same standing as `pinn_architecture.md`. |

**Reading order:** this file first (orientation → source treatment → hard constraints
vs. baseline → critique mandate → decision areas → output contract), then the three
documents above as the questions direct you to them.

## Source-Treatment Notes

- **The training-execution design is design intent, not a build spec — and it is
  baseline, not bedrock.** It is the artifact of a brief, quick brainstorm session; its
  own standing note (top of the file) records this. Treat its Section 7 placeholders as
  deliberately unresolved and its mechanical surface as challengeable baseline (next
  section).
- **The framework specs are the scientific source of truth.** `pinn_architecture.md` and
  `ctl_instruction.md` carry the locked conventions the trainer must implement (14D input
  contract, Jacobi coordinates, COM projection head, the AD contract for physics residuals,
  curriculum staging).
- **The specs are under active adjudication in the project.** In particular, **numerical
  precision contracts are being adjudicated and are NOT settled**. The copies you have are
  pinned snapshots. Handle this via the conditional-output requirement below, not by
  guessing the outcome.
- **No project code is provided or citable.** The project's pre-existing training code is
  explicitly non-authoritative; the build this research serves is a from-specs rewrite.

## Hard Constraints vs. Baseline Design Intent

The attached design carries two kinds of content. Treat them differently.

**Hard constraints — non-negotiable (facts, explicit project-owner decisions, or project
governance; not products of the brainstorm):**

1. The hardware and operator realities in the Constraints Register below.
2. No cloud, no distributed training (explicit project-owner decision).
3. The authority of `pinn_architecture.md` and `ctl_instruction.md` over the science.
4. The final quality gate metrics and thresholds referenced in Section 6.3 of the design
   document (project-locked); the verification layer consumes them, it never defines them.
5. The numerical precision requirement stays open pending project adjudication (handled
   via the conditional inside D1).

**Baseline design intent — the brainstorm's output; your default starting point, NOT
fixed walls:**

1. The three-subsystem decomposition (developer environment / data ingestion / training
   loop) plus the verification layer.
2. The five user-facing entry points: Setup / Configure / Launch / Monitor / Resume.
3. The `runs/<name>/` output directory contract (Section 5.7).
4. YAML config files driving each run; a frozen config copy in the run directory.
5. The thin-adapter data-ingestion boundary (the trainer never imports disk-format
   libraries directly).
6. The plain-Python-loop trainer style (single maintainable training script).
7. The developer environment: Miniforge3, conda environment `pinn-train`, Python 3.11+
   (Section 4.1).
8. Resume invariants and checkpoint *contents* (Section 5.6).
9. The placeholder inventory itself (PH-1..PH-10) as the list of open decisions.

Keep each baseline item unless you have well-evidenced reason to change it. When you do,
propose the change explicitly as an option measured against the baseline (see the output
contract) — never silently substitute your own structure.

## Baseline Critique Mandate

The design document is the product of a brief, early brainstorm, and the project owner
has directed that it be treated as a simplified starting point — not the fundamental
structure of the training pipeline. The brainstorm's pipeline breakdown may not be
optimal. As part of R1a you must therefore also review the baseline itself:

- Is the subsystem decomposition the right cut, or is there a cleaner, more useful
  breakdown of the pipeline?
- Is the placeholder inventory complete — are there core, early-settling decisions the
  brainstorm missed entirely?
- Are any baseline commitments (entry points, run contract, config approach) likely to
  constrain later work in ways the project would regret?

Report findings as explicit option-vs-baseline proposals with rationale; route any that
require a choice into the decision sheet.

## Constraints Register

Hard constraints every option must respect (transcribed from
`2026-06-10-training-execution-design.md`):

1. **Hardware:** a single MacBook Pro M5 Pro — 16 CPU cores, 15 GPU cores, 24GB *unified*
   memory (CPU and GPU share physical RAM; no separate VRAM; the OS shares the same 24GB),
   macOS 15+, arm64. The Neural Engine is not directly accessible to training frameworks.
2. **Non-expert maintainer and operator.** The project owner is not an expert at model
   training. Every option must be assessed for how it looks at the mechanical surface:
   what the user types, what the user sees, what files appear.
3. **Physics-residual computation via autodifferentiation.** The loss has three terms
   (data, physics, IC); the physics term requires PDE residuals computed by differentiating
   network outputs with respect to network inputs, per the AD contract in
   `pinn_architecture.md`. Verify each candidate supports the required derivative orders
   efficiently on Apple Silicon — do not assume.
4. **Curriculum training loop.** An outer curriculum state machine with stage promotions
   per `ctl_instruction.md`; checkpoint/resume must survive stage boundaries.
5. **Long-running unattended runs on a laptop.** Multi-hour runs; stability, thermal
   behavior, and crash-resume matter more than peak benchmark numbers.

## Decision Areas (deliver an options menu for each)

### D1. ML framework (the spine — everything else inherits this)

Among **PyTorch + MPS backend**, **MLX**, and **JAX (+ Optax + Equinox) on Apple
Silicon**: which framework should the trainer be built on, judged on (a) a non-expert
user maintaining a single training script; (b) autograd-friendly physics-residual
computation; (c) Apple Silicon native performance under 24GB unified memory; (d)
long-term ecosystem support for a multi-year research project.

Per candidate, answer with citations to current primary sources (official docs, release
notes, issue trackers — not blog hearsay):

1. **Precision support** on the GPU path on Apple Silicon (float32? float64? where does
   it silently fall back to CPU?). The project's precision requirement is pending
   adjudication — report capabilities factually and branch the menu (see output contract).
2. **Higher-order / input-gradient AD:** cost and ergonomics of differentiating outputs
   w.r.t. inputs and through those derivatives in the loss; known MPS/Metal limitations
   for double-backward or per-sample gradients.
3. **Maturity and failure surface:** what commonly breaks (unsupported ops, fallback
   warnings, memory behavior under unified-memory pressure)? How debuggable for a
   non-expert?
4. **Checkpoint/resume ergonomics:** native save/load including optimizer and RNG state.
5. **Ecosystem trajectory** as of your research date: release cadence, Apple Silicon
   commitment, PINN-relevant community usage.

### D2. Experiment tracking and the monitoring surface

The design commits a live terminal log as the primary monitor and a browser dashboard as
secondary. The tracker choice is open: **TensorBoard vs Weights & Biases (offline mode)
vs MLflow vs none/CSV-plus-scripts**, for a single-user, single-machine, no-cloud
project. Per option: what the Monitor entry point concretely looks like (commands, URLs,
screens), integration quality with each D1 candidate, storage/overhead on the same 24GB
machine, learning curve for a non-expert, and lock-in/migration cost if swapped later.

### D3. Compute utilization strategy on unified memory

How should the trainer use 16 CPU cores + 15 GPU cores sharing 24GB? Per D1 candidate:
available mechanisms (GPU compute with CPU-side data preparation, parallel data loading,
async pipelines), what's worth configuring vs. leaving default, how the user verifies
utilization (the design points at Activity Monitor), and memory-pressure management so
training does not starve the OS.

This explicitly includes the **in-memory vs. streaming ingestion** question: whether the
training dataset can be held fully in memory alongside the model, optimizer state, and
autograd graphs within the 24GB budget, or must be streamed/chunked from disk behind the
thin adapter. (The on-disk format itself is owned elsewhere and is out of scope — the
question here is the memory strategy behind the adapter.) Where the answer depends on
dataset size facts not in the attached files, parameterize and say exactly which numbers
the project must supply.

### D4. Checkpoint/resume policy, unattended-run auto-guards, and failure diagnostics

Checkpoint *contents* and resume *invariants* are baseline design intent (keep unless
your baseline review argues otherwise); the *policy* is the open menu here:
checkpoint cadence (the design's first-trial default is every 1000 steps), retention
(latest-only vs best-k vs periodic archive), disk budget over multi-hour curriculum runs,
and corruption safety (atomic write/rename patterns, what happens if the machine dies
mid-write). Stage-boundary checkpoint mechanics are D7's menu — cross-reference, don't
duplicate. Present options with their disk/recovery trade-offs at the user's mechanical
surface.

**Auto-guards for unattended runs.** Every stop rule in the baseline design is manual —
the user watches and presses Ctrl-C — but multi-hour unattended runs are the premise.
The structural menu: which guards live *inside* the training loop vs. are left to the
operator — NaN auto-stop, loss-explosion kill switch, disk-full and memory-pressure
guards, auto-checkpoint-on-anomaly. Design the menu around guard *mechanics* (detection,
action taken, what the user finds afterwards). Join point: the companion R1b package's
health-watchlist and operations findings supply the signal definitions these guards
would act on — note where a threshold must come from that research at consolidation
rather than inventing one.

**On-failure diagnostic bundle.** A short menu (or a single suggested checklist) for
what the trainer always captures when a run dies: environment snapshot, package
versions, config hash, traceback file, last-N log lines — so "copy the bundle and ask
for help" is an actionable runbook step rather than an archaeology exercise.

### D5. Training-loop skeleton capabilities (structural slices of optimizer and collocation)

The numeric tuning of the optimizer, learning-rate schedule, and collocation sampling is
deferred to a later round (R2) — but their **structural** consequences cannot wait,
because they shape the training-loop skeleton itself. Answer: what must the skeleton
accommodate?

- **Optimizer family structure:** standard PINN practice often uses a two-phase
  Adam → L-BFGS regime; L-BFGS requires closure support and full-batch phases — a
  different loop shape than a plain step-per-batch Adam loop. Per D1 candidate, verify
  what optimizer families are actually available and well-supported (L-BFGS on the GPU
  path? CPU-only?). The menu: which loop-shape capabilities to build into the skeleton
  (single-phase mini-batch only / two-phase with full-batch support / pluggable phases),
  with the cost of each in complexity and the cost of NOT having it in retrofit pain.
- **Collocation infrastructure:** residual-based adaptive sampling needs resampling
  machinery inside the training loop (periodic residual evaluation over a candidate
  pool, point-set refresh) that uniform fixed sampling does not. The menu: which
  collocation capabilities the skeleton should accommodate from day one vs. bolt on
  later — again structure only, not densities or schedules.
- **Loss-weighting machinery:** must the skeleton support dynamic loss-term weights as a
  *mechanism* (per-term weight schedules, adaptive rebalancing hooks), or are static
  weights structurally sufficient? Fence: the loss formulation itself — its terms,
  forms, and scientific weighting — is owned by the framework specs and is NOT to be
  redesigned here; this slice asks only what plumbing the loop must have if the
  curriculum or specs ever vary weights.

R2 then becomes pure tuning inside whatever skeleton is picked here.

### D6. Reproducibility and determinism policy

The design's run-comparison surface ("is this run better than my last one?", its
Section 6.2) and its reproducibility contract ("give a colleague the `runs/` folder")
silently assume more determinism than Apple-Silicon backends may deliver. Per D1
candidate, establish with citations: what determinism is actually available on the GPU
path (deterministic ops? seed plumbing? known nondeterministic kernels?), and at what
performance cost. Then present the policy menu: e.g., strict determinism where available
vs. accepted-variance with a defined seed policy and a multi-seed comparison protocol —
including what run-to-run variance means for judging "better than last run" and what the
runbook should tell a non-expert about comparing two runs honestly.

### D7. Curriculum stage-boundary mechanics

Curriculum training is this project's defining feature, and generic PINN material will
not volunteer answers about it. The promotion *rules* (when to promote) are owned by
`ctl_instruction.md` and are out of scope; the **loop mechanics at a stage boundary**
are the open menu here:

- Is a checkpoint guaranteed at every stage promotion, distinguishable from ordinary
  cadence checkpoints?
- What is the rollback policy when a freshly promoted stage goes bad — auto-revert to
  the pre-promotion checkpoint, manual operator decision, or none?
- Can a run resume across a boundary — what happens if the machine dies mid-promotion?
- Does optimizer state reset or carry at a stage transition? This is a real, documented
  question in staged training (e.g., Adam's moment estimates can poison a freshly
  promoted stage). Per D1 candidate, verify with citations what state-reset /
  partial-reset support exists.

Cross-references: the checkpoint machinery itself is D4; the loop-shape capability to
express boundary behavior is D5; divergence-after-transition as a *health signal* is the
companion R1b package's watchlist topic — note the consolidation join rather than
duplicating it.

## Output Contract

Deliver a **single self-contained markdown document** containing:

1. **Per decision area (D1–D7): an options menu** — 2–4 viable options, each with
   strengths/weaknesses at the mechanical surface (what the user types/sees/installs),
   downstream implications for later trainex design, and cross-decision interactions
   (e.g., a D2 tracker that is native to a D1 framework). Close each menu with a
   **suggested default and rationale** — clearly marked as a suggestion. The final pick
   belongs to the project owner.
2. **A precision conditional inside D1**: state the menu's suggested default under
   (i) "float32 on the accelerator suffices for the physics residuals" and (ii) "float64
   is required for the physics residuals" — and whether the suggestion changes. If a
   candidate cannot honestly satisfy branch (ii), say so plainly.
3. **Baseline review findings** (per the Baseline Critique Mandate): your assessment of
   the brainstorm baseline — the subsystem decomposition, the placeholder inventory, and
   the mechanical-surface commitments — with any change proposals presented as explicit
   option-vs-baseline comparisons with rationale.
4. **Door classification**: label every suggested default and every baseline-deviation
   proposal as a **one-way door** (hard to reverse once built against) or a **two-way
   door** (cheaply revisitable later), with one line on what makes it so. The project
   owner needs to know exactly which picks lock structure and which stay flexible.
5. **A decision sheet** at the end: one table — decision | options | suggested default |
   door type | your pick (left blank) — that the project owner can fill in directly.
   Include a row for every D1–D7 decision AND every proposed baseline deviation (option:
   keep baseline vs. change).
6. **A composed first-run recipe**: assemble all suggested defaults (D1–D7) into one
   coherent end-to-end picture of the first training run — environment, install, launch
   command shape, what the user watches, checkpoint/resume behavior. This is a coherence
   check that the menus actually compose: flag any pairwise conflicts you find. (Expected
   run duration is the companion R1b package's feasibility question — note the join
   point, do not estimate it here.)
7. **A "what the runbook inherits" note**: launch/resume command shapes, checkpoint
   artifact formats, monitoring commands implied by each suggested default, and anything
   that would pressure a hard constraint (flag explicitly — hard constraints are never
   redesigned).
8. **A claims-and-uncertainty register**: anything you could not verify from primary
   sources — and anything in the attached materials you found ambiguous or contradictory —
   listed as open rather than asserted.

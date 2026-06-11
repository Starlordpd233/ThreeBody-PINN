---
title: Trainex R1b Research Context Master — Runbook and Operations Knowledge
package_for: trainex-r1b (runbook-and-operations-knowledge half of the foundational research round)
role: research-context entry point (orientation, constraints, research topics K1–K5, output contract)
status: active
created: 2026-06-11
source_baseline: c17e23ed0642f01d2eda7e7f65c0f18ed7081487
self_contained: true
---

# Trainex R1b Research Context Master — Runbook and Operations Knowledge

This file is the research-context entry point for **trainex R1b**, the
runbook-and-operations-knowledge half of the foundational research round for the CTL-PINN
training-execution development ("trainex"): the pipeline, tooling, and step-by-step user
runbook through which a non-expert project owner will train, monitor, and assess a
curriculum-trained physics-informed neural network (CTL-PINN) for the gravitational
three-body problem on a single MacBook.

**The round is split in two.** A companion package, R1a, covers the core decisions and
structural questions (framework choice, tracking, compute strategy, checkpoint policy,
loop skeleton, determinism policy) and delivers options menus for the project owner to
pick from. R1b (this package) covers the **researched knowledge** the user runbook and
verification layer will be built from. Your deliverable is structured, cited findings —
**not decision menus**. Where a finding implies a project decision, list it under
"decision-relevant observations" (see output contract) rather than adjudicating it; the
decision channel lives in R1a and in the project owner's hands.

**You are working from attached files only.** You have no access to the project's
repository. The three attached project documents are verbatim snapshots and may mention
files or paths that are not attached; treat any such reference as unavailable — note it
in the claims-and-uncertainty register if it matters — rather than guessing at its
content. Alongside this file, you have been given exactly three other documents,
referred to throughout by filename:

| File | Role | How to treat it |
|---|---|---|
| `2026-06-10-training-execution-design.md` | The training-execution reference design (entry points, monitoring surfaces, verification questions your findings feed) | **Baseline from a brief early brainstorm — a default starting point, not fixed structure** (its own standing note says so). Where a finding suggests its structure should change, record a decision-relevant observation; do not redesign it here. |
| `pinn_architecture.md` | Authoritative framework spec — network architecture, autodifferentiation (AD) contract, output head | Source of truth. Derive parameter counts and per-step cost structure from it for K4. Not yours to change. |
| `ctl_instruction.md` | Authoritative framework spec — CTL methodology, curriculum staging, input-vector formulation | Source of truth, same standing. The curriculum staging drives K4's full-run estimate and K1's stage-transition failure modes. |

**Reading order:** this file first (orientation → constraints → research topics → output
contract), then the three documents above as the topics direct you to them.

## Hard Constraints and Standing

- **Hardware:** a single MacBook Pro M5 Pro — 16 CPU cores, 15 GPU cores, 24GB *unified*
  memory (CPU and GPU share physical RAM; no separate VRAM; the OS shares the same 24GB),
  macOS 15+, arm64. The Neural Engine is not directly accessible to training frameworks.
- **No cloud, no distributed training** (explicit project-owner decision). If a finding
  pressures this constraint — K4 especially — flag the pressure explicitly; never design
  around it.
- **Non-expert maintainer and operator.** Every finding must land at the mechanical
  surface: what the user types, what the user sees, what files appear.
- **The framework specs are the scientific source of truth**; the project's pre-existing
  training code is non-authoritative and not provided. Numerical precision contracts are
  under active project adjudication — where precision affects an estimate, branch it.
- **Candidate frameworks** under evaluation in R1a (use for per-framework framing where a
  topic needs it): PyTorch + MPS, MLX, JAX (+ Optax + Equinox) on Apple Silicon.
- **Long-running unattended runs on a laptop:** multi-hour runs; stability, thermal
  behavior, and crash-resume matter more than peak benchmark numbers.

## Research Topics (deliver structured, cited findings for each)

### K4. Training feasibility envelope — HIGHEST PRIORITY in this package

Nobody has yet estimated whether a full curriculum run on this machine means hours,
days, or weeks — and every other decision in the round implicitly assumes the answer is
benign. Produce an **order-of-magnitude wall-clock and memory-footprint estimate** for
(a) one curriculum stage and (b) a full curriculum run, per candidate framework,
grounded in:

- the committed network architecture and AD/physics-residual requirements in
  `pinn_architecture.md` (derive parameter counts and per-step cost structure from it);
- the curriculum staging in `ctl_instruction.md`;
- published Apple-Silicon training-throughput data from primary or well-evidenced
  sources (date-stamped).

Where the estimate depends on project-side facts not in the attached files (dataset
size, samples per trajectory, collocation point counts), **parameterize the estimate
over a sensible range and list exactly which numbers the project must supply** to
tighten it. State explicitly which outcome ranges would pressure the no-cloud constraint,
and what they would imply for checkpoint cadence, thermal planning (K2), and the
monitoring rhythm (K1).

### K5. Trainer-correctness verification ladder — co-priority with K4

PINN implementations fail silently: residual sign errors, wrong coordinate frame,
AD-graph mistakes in the double-backward — all of which can produce plausible-looking
loss curves while training garbage. The operator cannot eyeball wrong physics, so the
runbook needs a **pre-flight verification ladder** the trainer must pass before any real
run burns days of compute. Research the validation ladder practitioners use before
trusting a PINN trainer, including at least:

- **Gradient/AD checks:** autodiff residuals validated against finite-difference
  evaluations, and how practitioners structure these checks for physics residuals.
- **Overfit-a-single-batch / tiny-problem tests:** deliberately overfitting a trivially
  small dataset as a capacity-and-plumbing sanity check.
- **Known-solution fixtures:** the three-body domain is unusually blessed here — exact
  and special reference solutions exist (the Euler collinear solutions, the Lagrange
  equilateral solution, the figure-eight choreography) that can serve as ground truth
  the trainer must reproduce. Verify their standard parameterizations from the
  literature with citations. Fixtures must be expressed against the attached specs'
  conventions (input/coordinate/output contracts in `pinn_architecture.md` and
  `ctl_instruction.md`); flag any convention mismatch in the claims register rather than
  improvising one.
- **The smoke-test pattern:** a ~5-minute tiny end-to-end run before any real run, as a
  first-class runbook step — the cheapest rung of the ladder (K3 maps where it lands
  among the entry points).

Deliver the ladder as: rung → what it catches → pass criterion → cost. This becomes the
runbook's "pre-flight check" section and shapes the test-harness skeleton (route
structural implications through decision-relevant observations).

### K1. PINN training-health watchlist and failure modes

The runbook must answer "is training healthy?" for a non-expert. Research the documented
failure modes of PINN training and curriculum/staged training (e.g., loss-term imbalance,
physics-residual stagnation, failure to propagate from initial conditions, divergence
after stage transitions — verify and extend this list from the literature). Deliver a
watchlist mapping each signal to the monitoring surfaces the design describes (terminal
loss lines, dashboard curves, system monitor): signal → what it likely means → first
response a non-expert can take.

### K2. Unattended training operations on a MacBook

The reality of multi-hour runs on a laptop. Research and report current macOS-15-era
practice for: preventing sleep during runs (and what happens on lid close), running
training so it survives a closed terminal (and whether that is advisable), thermal
throttling behavior on Apple Silicon under sustained load and what mitigations are real
vs. folklore, battery/power settings for long runs, and safe manual stop semantics that
cooperate with checkpointing. Flag anything that should become a Launch/Monitor runbook
step.

Also under this topic: **environment maintenance over the project's multi-year life.**
The training stack sits on the fastest-moving corner of the ML ecosystem (Apple-Silicon
backends), and a non-expert operator will not spontaneously connect "I updated macOS"
with "my loss curves changed." Research current practice for: pinning and exporting the
environment (conda env export, lockfiles) so a working setup is exactly reproducible;
when to take — and when to defer — framework, Python, and macOS upgrades mid-project;
how upgrades can silently change GPU-path numerical behavior; and re-validation after
any upgrade — re-running the cheap rungs of K5's verification ladder before trusting
new runs. Flag anything that should become a Setup or maintenance runbook step.

### K3. Runbook design patterns for non-expert operators

The end product of trainex is a step-by-step runbook for a non-expert. Research patterns
from well-regarded operational documentation (runbooks, playbooks, checklists) that fit
this use: how to present a juncture where the operator must decide, error-surface design
(error → meaning → action tables), troubleshooting trees vs. flat FAQs, checklist vs.
narrative formats, and how much context to put inline vs. link out. Deliver concrete
pattern recommendations mapped to the design's five entry points (Setup / Configure /
Launch / Monitor / Resume).

## Output Contract

Deliver a **single self-contained markdown document** containing:

1. **Per topic (K1–K5): structured findings** with citations to primary or
   well-evidenced sources (date-stamped), framed as runbook-ready material
   (signal → meaning → first response; pattern → example → where it applies;
   estimate → assumptions → range; rung → what it catches → pass criterion → cost).
2. **K4 specifics:** parameterized order-of-magnitude estimates with an explicit list of
   the project-side numbers needed to tighten them; explicit flags for outcome ranges
   that would pressure the no-cloud constraint, with downstream implications spelled out.
   The companion R1a round consumes these at consolidation (its "first-run recipe" joins
   your duration estimate).
3. **K5 specifics:** the verification ladder as a rung-by-rung table, written so it can
   be lifted directly into the runbook's pre-flight section; known-solution fixtures
   cited to literature and expressed against the attached specs' conventions; smoke-test
   pattern included as the cheapest rung.
4. **Decision-relevant observations**: a dedicated section listing any finding that
   implies a project decision (structural change, policy choice, constraint pressure,
   test-harness skeleton requirements from K5) — stated as an observation with evidence,
   NOT adjudicated. These merge with R1a's decision menus at consolidation.
5. **A claims-and-uncertainty register**: anything you could not verify from primary
   sources — and anything in the attached materials you found ambiguous or contradictory —
   listed as open rather than asserted.

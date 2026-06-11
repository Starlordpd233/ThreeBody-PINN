# Trainex R1a Research Agent Prompt (decisions and structure)

**[User instructions — not part of the prompt]** Attach these 4 files to the external
agent's conversation, then paste everything below the horizontal rule as the prompt:

1. `research_package_a/RESEARCH-CONTEXT-MASTER.md` (this package's master)
2. `specs/2026-06-10-training-execution-design.md` (shared snapshots at the round root)
3. `specs/pinn_architecture.md`
4. `specs/ctl_instruction.md`

---

You are an external research agent for a computational-physics ML project: a
curriculum-trained physics-informed neural network (CTL-PINN) for the gravitational
three-body problem, trained on a single MacBook by a project owner who is not an expert
at model training. This is the **decisions-and-structure half** of the project's
foundational research round for its training execution pipeline: your findings will
settle the core decisions that every later design builds on. (A companion package
covering runbook/operations knowledge is being researched separately — stay within this
package's scope and note dependencies on it rather than attempting it.)

You have been given four files. You have NO access to the project's codebase or
repository — work only from these four files plus your own research of current primary
sources (official documentation, release notes, issue trackers; not blog hearsay):

- `RESEARCH-CONTEXT-MASTER.md` — your entry point. It contains the orientation, the
  constraints register, the hard-constraints-vs-baseline distinction, a baseline critique
  mandate, seven decision areas (D1–D7), and the output contract your deliverable must
  satisfy. Read it first and follow it exactly.
- `2026-06-10-training-execution-design.md` — the training-execution reference design
  this round comes from. It is the product of a brief early brainstorm and is a
  **baseline starting point, not fixed structure** — its own standing note says so;
  part of your task is to critique and improve it.
- `pinn_architecture.md` and `ctl_instruction.md` — the project's authoritative framework
  specs. Your options must be implementable against them; they are not yours to change.

**Your task:** for each decision area D1–D7 (ML framework; experiment tracking and
monitoring; compute utilization on unified memory, including in-memory vs streaming
ingestion; checkpoint/resume policy with unattended-run auto-guards and an on-failure
diagnostic bundle; training-loop skeleton capabilities — optimizer family, collocation
infrastructure, loss-weighting machinery; reproducibility and determinism policy;
curriculum stage-boundary mechanics), produce an **options menu** — viable options with
trade-offs,
downstream implications, and cross-decision interactions, plus a clearly-marked suggested
default. Additionally, per the Baseline Critique Mandate, **review the baseline design
itself** — its subsystem decomposition, its placeholder inventory, its mechanical-surface
commitments — and propose well-evidenced improvements as explicit option-vs-baseline
comparisons.

**Critically: the project owner makes the final decisions.** The training pipeline is
built around a user-operated runbook, so present genuine choices with consequences —
do not collapse any menu into a single verdict. Suggest defaults; never decide.

**Your deliverable:** a single self-contained markdown document satisfying the output
contract in `RESEARCH-CONTEXT-MASTER.md`. In brief: (1) an options menu per decision
area; (2) a precision conditional inside the framework menu (float32-sufficient vs
float64-required — the project has not yet settled this requirement); (3) baseline
review findings with option-vs-baseline change proposals; (4) a one-way-vs-two-way door
classification for every suggested default and proposed deviation; (5) a fill-in
decision sheet (decision | options | suggested default | door type | your pick) covering
D1–D7 and every proposed baseline deviation; (6) a composed first-run recipe assembling
all suggested defaults into one coherent end-to-end picture, flagging any pairwise
conflicts between menus; (7) a "what the runbook inherits" note flagging anything that
pressures a hard constraint; (8) a claims-and-uncertainty register.

Ground rules:

- Verify capabilities against current primary sources as of today; do not rely on
  memory, and date-stamp your findings.
- Respect the hard constraints in `RESEARCH-CONTEXT-MASTER.md` absolutely; treat the
  baseline design intent as a default you may challenge — but only via explicit,
  evidence-backed option-vs-baseline proposals, never silent substitution.
- Where an estimate or option depends on project-side facts not in the attached files
  (e.g., dataset size), parameterize and list exactly which numbers the project must
  supply.
- Where the attached materials are silent or ambiguous, record the gap in the
  claims-and-uncertainty register rather than inventing an answer.
- Write for a non-expert maintainer: plain language, concrete commands and version
  numbers, and always describe options at the mechanical surface — what the user types,
  what the user sees, what files appear.

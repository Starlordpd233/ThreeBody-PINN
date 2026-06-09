---
title: Empirical Decision Loop
alias: EDL
status: draft
scope: project-wide methodology
created: 2026-05-23
last_updated: 2026-05-24
canonical: false
---

# Empirical Decision Loop

The Empirical Decision Loop (EDL) is a project-wide draft methodology for handling framework-design choices where source documents, theory, and first-principles reasoning are not enough to safely lock a concrete contract.

EDL complements the theoretical framework-spec revision process. The framework specs define the intended mathematical and engineering contracts. EDL supplies a disciplined path for preparing user research and, when the user later approves it, designing small executable experiments that help decide ambiguous numeric values, thresholds, loss-shaping choices, sampling conventions, and stability defaults before those contracts are finalized.

EDL is not the full PINN implementation. It is not production training infrastructure. It is not a substitute for theory. It is not a license for agents to invent empirical conclusions. It is a decision-support method: document the uncertainty, prepare the research context, and build only enough executable evidence to make a better framework decision after the user authorizes that work.

Because this file is marked `canonical: false`, it is a methodology draft and support artifact. It does not override `AGENTS.md`, milestone requirements, phase plans, gap registers, or direct user instruction. Governing planning docs may point to this workflow, but the phase-local gap register remains the authoritative blocking record.

## Conversation Context

EDL was proposed during Phase 19 planning after an unresolved `epsilon_H` default surfaced in the energy-drift loss denominator. The candidate resolution sources named the denominator floor symbol but did not specify an exact numeric value. A draft plan had previously inserted `epsilon_H = 10^-8`, but that value was not grounded in the source materials.

The user clarified that `10^-8` should not be assumed just because it is familiar or convenient. For choices like this, where theory identifies the formula but not the practical constant, the project may need research and experiments to supply evidence. The goal is not to build the entire PINN training stack before deciding one value. The goal is to build enough small experimental machinery to make informed framework decisions.

The user also clarified the agent's role: the agent does not perform the external research needed to decide whether theory is enough, whether EDL should run now, or whether EDL should be deferred. The agent prepares the gap entry and a detailed research brief so the user can conduct that research externally and return an instruction.

This workflow intentionally lives outside individual phase directories because EDL is broader than Phase 19 and broader than v1.4. Individual phase gap registers still record the actual STOP/governance state.

## Why EDL Exists

The framework contains choices that are theoretically motivated but empirically sensitive. Examples include denominator floors, clipping bounds, loss weights, normalization choices, initialization defaults, sampling allocations, and validation tolerances.

For these choices, theory can identify the shape of the correct formula, but may not determine the best practical value. Choosing a value silently can create long-term spec drift. Deferring every such decision until the full PINN exists can block progress unnecessarily.

EDL occupies the middle ground:

- avoid inventing ungrounded constants;
- avoid overbuilding the full system just to test one design choice;
- prepare user research when the agent cannot decide whether theory is enough;
- produce executable evidence only after the user authorizes an EDL probe;
- preserve the STOP/gap discipline when source materials are silent;
- make framework specs more robust before full-scale implementation begins.

## Relationship To Gap Registers

The phase-local gap registers are the canonical governance records for source-silent or ambiguous decisions. Every such decision still starts there.

EDL is a support workflow attached to a subset of gaps. It does not replace the gap register, and it does not decide the outcome by itself.

Use this relationship:

- **Phase gap register**: legal/governance record; owns the decision point, source silence, blocking status, status transitions, and final resolution.
- **Central EDL registry**: project-wide index of research-needed and EDL-supported items.
- **Central EDL research brief**: detailed user-facing context package for external research.
- **EDL probe or decision record**: optional later artifact, created only after user instruction authorizes EDL execution.

A gap entry that has EDL support should include a pointer such as:

```text
Research support: EDL-19-01 at .planning/research/edl/EDL-19-01-epsilon-H.md
```

The gap register remains authoritative for whether dependent work is blocked, whether independent work may continue, and whether the phase may close.

## Relationship To Framework Spec Work

The theoretical framework-spec workflow answers: "What should the framework say?"

The EDL workflow answers: "When the framework needs a concrete choice and the sources are silent, what research or executable evidence is needed before the user can approve a contract?"

A spec gap should remain open when a decision is source-silent and empirically consequential. The gap can point to an EDL item instead of forcing an immediate symbolic or numeric choice.

After an EDL probe runs, the result does not automatically become authoritative. It becomes evidence for a user-approved decision. Once approved, the framework spec can be updated with the chosen contract and the decision record can be cited as supporting rationale.

## Relationship To Validation Probes

EDL is related to, but distinct from, disposable validation probes.

Validation probes test whether an already-specified contract is self-consistent and implementable.

EDL probes help decide what the contract should be before it is finalized.

A successful EDL probe may later become:

- an acceptance check;
- a disposable validation probe;
- a reusable validation script;
- or simply a decision record with no long-term code artifact.

## Core Terms

- **EDL**: the overall methodology, Empirical Decision Loop.
- **Research-needed gap**: a source-silent gap where the agent can explain the decision space but cannot decide whether theory/source material is enough or whether empirical evidence is needed.
- **Research Brief**: the detailed central artifact that packages context for the user's external research.
- **Decision Probe**: a small executable experiment designed to inform one decision after the user approves EDL execution.
- **Decision Record**: the written result of a probe, including candidates, metrics, evidence, and recommendation.
- **EDL ID**: a stable identifier such as `EDL-19-01`, used to link a gap, research brief, probe, and decision record.

## Triage Rule

Every source-silent issue first goes to the relevant phase gap register. Then the agent decides whether the gap needs EDL research support.

A gap should get a central EDL research brief when all of the following are true:

1. The decision affects numerical stability, optimization behavior, validation tolerance, loss scaling, sampling quality, implementation feasibility, or a similar empirical property.
2. The source materials do not explicitly settle the decision.
3. First-principles reasoning narrows the candidates but does not safely select one.
4. User research or a later small executable probe could plausibly change the framework contract.

Do not use EDL for:

- pure transcription from source documents;
- mechanical Markdown or process-format decisions;
- acceptance-check naming, file naming, or verification-regex bugs unless they affect empirical validity;
- identities already settled by short first-principles derivation;
- decisions where a full training system is the only meaningful test and no cheap proxy exists.

If the agent is uncertain whether theory/source material is enough or whether EDL is needed, the agent should not choose. It should record the gap, create a research brief, and wait for the user's research conclusion.

## Blocking Rule

EDL follows dependency-scoped blocking plus a phase-exit gate:

- The open gap blocks the specific decision, spec edit, acceptance check, probe, or plan section that depends on it.
- Independent work may continue when it does not rely on the unresolved decision.
- The phase cannot be marked complete while the gap is unresolved unless the user explicitly marks it `DEFERRED` and defines what is safe to leave symbolic or future-bound.
- Every research brief must include a dependency map that names blocked work, safe independent work, and phase-completion impact.

High-impact gaps may become effectively phase-wide if the unresolved decision controls the entire contract under revision. The dependency map must say so explicitly instead of relying on implicit judgment.

## Lifecycle

Each EDL-supported gap follows this lifecycle:

1. **Gap surfaces**
   The agent finds a source-silent or empirically uncertain decision.

2. **Dependent work stops**
   The agent stops only the affected decision/edit/probe path. Independent work may continue if the dependency map allows it.

3. **Gap register entry is created**
   The phase-local register records the canonical gap with the required STOP-protocol fields.

4. **Central research brief is created**
   The agent writes a detailed context package under `.planning/research/edl/`.

5. **User researches externally**
   The agent does not perform the external research and does not decide the empirical answer.

6. **User returns instruction**
   The user chooses one of: theory/source is enough, run EDL now, defer EDL later, no useful EDL is available yet, or direct contract instruction.

7. **Records are updated**
   The agent updates the gap register, central EDL index, and research brief status.

8. **EDL probe is designed only if approved**
   If the user approves EDL execution, the agent designs the smallest useful probe and records metrics before running it.

9. **Framework specs are patched only after resolution**
   Spec changes land after the decision is resolved or explicitly deferred.

## User Research Outcomes

After reading a research brief and conducting external research, the user can return one of these outcomes:

- **Theory/source is enough**: user explains the grounding or points to the source, and the agent resolves the gap with instruction.
- **Run EDL now**: user authorizes an EDL probe before the dependent spec contract is locked.
- **Defer EDL later**: user allows the current phase to leave the decision symbolic or future-bound with a clear deferral note.
- **No cheap EDL can answer this yet**: user records that only full implementation/training can answer it, so the framework keeps a blocker or future validation requirement.
- **Direct contract instruction**: user supplies the exact contract to apply.

## Research Brief Template

Each central research brief is written for the user as the researcher. It should synthesize context, while preserving a source-audit trail so the user can verify that the agent did not misrepresent the project state.

Use this structure:

```markdown
---
edl_id: EDL-<phase-or-area>-<sequence>
linked_gap: GAP-<phase>-<sequence>
status: OPEN-RESEARCH-NEEDED
phase: <phase name>
topic: <short topic>
created: YYYY-MM-DD
blocking_level: dependency-scoped
canonical: false
---

# EDL-...: <Title>

## Short Answer Needed

State the exact instruction the user needs to return with.

## Current Project State

Summarize what the framework, phase context, and planning artifacts currently say.

## Why This Is A Gap

Explain source silence, ambiguity, or insufficient theory with citations.

## Agent Understanding

Explain the mathematics, physics, or engineering stakes clearly enough for the user to audit.

## Candidate Resolutions

List concrete options and how each changes the framework.

## Dependency Map

- Blocked work:
- Safe independent work:
- Phase-completion impact:

## Core Files To Audit

List must-read files and sections, with why each matters and what the user should verify.

## External Research Questions

List focused questions for the user to answer outside the repo.

## Possible EDL Directions

List provisional probe shapes only. Do not present them as approved designs.

## Return Format

Describe what instruction the agent needs from the user.
```

## Core Files To Audit

Every research brief must include a curated `Core Files To Audit` section. This section should not dump every related file. It should identify the few source paths that most directly control the decision, explain why each matters, and provide section or line anchors when stable enough.

For `EDL-19-01`, the core audit set is:

1. `.planning/milestones/v1.4-phases/19-physics-and-loss-contracts/19-GAPS.md`
   - Why: canonical blocking record for `GAP-19-01`.
   - Check: whether the gap framing and dependency block are accurate.

2. `.planning/milestones/v1.4-phases/19-physics-and-loss-contracts/19-CONTEXT.md`
   - Why: locked Phase 19 decision context.
   - Check: D-07 `L_E` formula and symbolic `epsilon_H` handling.

3. `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
   - Why: candidate source for the `L_E` formula.
   - Check: whether it defines only the symbol or implies a value.

4. `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
   - Why: issue-side discussion of softening and numerical stability.
   - Check: whether any stated epsilon logic transfers to `epsilon_H`.

## Probe Ladder

When the user approves EDL execution, prefer the cheapest meaningful probe first:

1. **Analytic fixture**
   Closed-form or hand-constructed cases that isolate the formula.

2. **Dataset scan**
   Run the decision formula over real or representative existing data.

3. **Perturbation/sensitivity test**
   Add controlled noise or edge cases to measure stability.

4. **Surrogate training test**
   Use a tiny model or fake predictor to inspect loss/gradient behavior.

5. **Minimal real training ablation**
   Use only when cheaper probes cannot answer the decision.

The goal is not exhaustive experimentation. The goal is enough evidence to make the framework decision less arbitrary.

## First Example: `epsilon_H`

Phase 19 surfaced an unresolved `epsilon_H` value in the energy-drift denominator:

```text
Delta H_n =
  (H_epsilon(r_theta'(u_n), v_theta'(u_n)) - H_epsilon(r_0', v_0'))
  / (|H_epsilon(r_0', v_0')| + epsilon_H)
```

The formula requires a denominator floor, but the source materials name the symbol without settling the numeric value.

A possible EDL probe direction, if the user approves EDL execution, could test this without a full PINN:

- compute `H_0` over representative initial conditions;
- compare absolute, scale-relative, and data-dependent denominator-floor candidates;
- measure denominator activation rate, normalized drift quantiles, outlier blowups, ranking stability, and gradient-scale proxy;
- identify whether a candidate is mostly inactive for ordinary samples while still preventing unstable blowups near low-energy cases.

EDL-19-01 is no longer an open research dependency; see the canonical `GAP-19-01` resolution in `19-GAPS.md`.

The first detailed research brief for this decision is `.planning/research/edl/EDL-19-01-epsilon-H.md`.

## Candidate Uses Across v1.4 And Later

- **Phase 18**: gauge degeneracy thresholds, COM/momentum tolerance behavior, rotation-frame edge cases.
- **Phase 19**: `epsilon_H`, Huber `delta_r`, angular-momentum denominator floors, causal clipping bounds, loss normalization.
- **Phase 20**: SIREN frequency/init defaults, LayerNorm behavior, inertia normalization, support-range wording.
- **Phase 20.5**: Sobol allocation coverage, sampling coordinate sensitivity, allocation-order probes.
- **Phase 21**: promote mature EDL probes into acceptance checks where appropriate.
- **Future milestones**: use EDL whenever framework revisions require empirical support before production implementation.

## Naming Convention

Use IDs of the form:

```text
EDL-<phase-or-area>-<sequence>
```

Examples:

- `EDL-19-01`: energy-drift denominator floor `epsilon_H`.
- `EDL-20-01`: SIREN frequency/init sensitivity.
- `EDL-SAMP-01`: sampling allocation coverage probe.

Research-brief filenames should include the EDL ID and a short slug:

```text
.planning/research/edl/EDL-19-01-epsilon-H.md
```

## Status Values

Use these central EDL statuses:

- `OPEN-RESEARCH-NEEDED`: gap has EDL support and waits on user research.
- `USER-RESEARCHING`: user has taken the research task externally.
- `RESOLVED-WITH-INSTRUCTION`: user supplied enough instruction to resolve the linked phase gap.
- `DEFERRED-TO-EDL`: user allows current work to continue with a future EDL requirement.
- `EDL-APPROVED`: user approved designing and running a probe now.
- `EDL-COMPLETE`: probe ran and decision record is available.
- `BLOCKED`: no safe independent work remains until the decision is resolved.

These statuses support the central EDL index. Phase gap registers may keep their existing `OPEN`, `RESOLVED-WITH-INSTRUCTION`, and `DEFERRED` statuses; the gap register remains authoritative.

## Success Criteria

EDL is working if:

- fewer constants are chosen by assumption;
- phase gap registers remain the single source for blocking state;
- research briefs make user research easier without replacing source audit;
- framework specs record why sensitive values were selected;
- probes are small enough to write before full implementation;
- results are concrete enough to change a decision;
- future implementation can trace a contract back to user-approved evidence.

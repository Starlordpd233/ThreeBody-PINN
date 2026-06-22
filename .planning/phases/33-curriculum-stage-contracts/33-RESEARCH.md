# Phase 33: Curriculum-Stage Contracts - Research

**Researched:** 2026-06-22
**Domain:** v1.6 curriculum-stage framework-spec contracts
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

Source: copied from `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md`. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:1-193`]

### Locked Decisions

#### Adaptive Stage Assignment

- **D-33-01:** Use the packet-first / defer-floor disposition from
  `GAP-33-01`: Phase 33 specifies admitted-set EDA, robust transforms, PCA,
  clustering, quantile thresholds, and stable `record_key` labels, but does not
  lock the population safeguard value.
- **D-33-02:** Do not adopt `stage_strat_revision.md` Table 4 wholesale because
  it erases existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold
  refinement roles.
- **D-33-03:** Treat the actual admitted-set EDA run and any population-floor
  owner policy as FUT, not Phase 33 execution.

#### `L_max`, `tau_L`, and Metadata

- **D-33-04:** Use `L_max = M_tot * r_char * sqrt(2 * |E| / M_tot)` as a
  characteristic angular-momentum scale, not a global maximum.
- **D-33-05:** Preserve the v1.5-locked raw-mass `D ~= 4.6416` convention and
  reject `D = 6.694` for the active scale.
- **D-33-06:** Keep `tau_L` excluded from `IC13`; it is staging/evaluation
  metadata only.
- **D-33-07:** Retain the current Rosenstein-style estimator as a revisable
  baseline. Do not normatively adopt the issue-doc shadow method, its
  `epsilon_pert` / `epsilon_soft` parameters, or the unspecified PCA+Rosenstein
  shortcut.

#### Stage Transitions

- **D-33-08:** Model transitions as an operational state machine:
  ADVANCE only on an approved success gate, RECOVER for NaN/Inf rollback and
  bounded retry, and HALT/REVIEW for max-epoch or stagnation unless the owner
  later authorizes degraded advancement.
- **D-33-09:** Keep all numeric thresholds, epoch tables, stagnation windows,
  retry limits, and percentile relaxations provisional pending FUT Stage-0 pilot
  calibration.

#### Stage 0-6 Inventory and Gates

- **D-33-10:** Store raw, unclipped `L_norm` as staging / diagnostic metadata
  and require explicit nonfinite / near-degenerate `L_max` handling.
- **D-33-11:** Do not authorize a global `L_norm` clamp. Do not lock
  `np.clip(L_norm, 0, 1)` as the stage gate in Phase 33.
- **D-33-12:** Define the Stage 0-6 inventory, per-stage criteria, cumulative
  replay behavior, and Stage-6 catch-all while marking unverified trajectory
  counts as claimed / FUT.

#### `s_min`, Epsilon, and Cross-Phase Handoffs

- **D-33-13:** Transcribe Phase 32's D-05 owner instruction: the curriculum
  Stage-6 collision gate uses unsoftened geometric `s_min`; loss-side
  matched-Plummer softening belongs to Phase 35.
- **D-33-14:** When static invariant epsilon appears in curriculum metadata,
  transcribe Phase 32's D-06 owner instruction: offline invariants retain
  `epsilon_inv = 1e-10`, while training keeps `epsilon_train = 1e-5`.
- **D-33-15:** Cross-link Phase 34 / Phase 35 responsibilities only as handoffs;
  do not plan their contracts as Phase 33 work.

#### Planning Workflow

- **D-33-16:** The roadmap says Phase 33 has `UI hint: no`; if the plan-phase UI
  gate reports a frontend block, planning should proceed with `--skip-ui`.
- **D-33-17:** Plans must include forbidden-path guards for read-only reports,
  frozen specs, live `pinn/` code, and unrelated dirty files.

### the agent's Discretion

The planner may decide the number of Phase 33 plan files and task grouping, as
long as every `CURR-01` through `CURR-05` requirement appears in a plan
`requirements` field and the plan remains executable by `$gsd-execute-phase`.

### Deferred Ideas (OUT OF SCOPE)

- Admitted-set EDA and population-floor owner policy are FUT after Phase 33.
- Final `tau_L` estimator, time-unit convention, fit parameters, uncertainty
  flags, and thresholds are owner-pending.
- `np.clip(L_norm, 0, 1)` as a possible derived stage-gate value remains
  owner-pending admitted-set evidence.
- Stage-0 pilot calibration owns transition thresholds, stagnation windows, and
  retry limits.
- Phase 34 owns replay/lookahead batching, batch construction, collocation
  scaling, ALM, and training-side metric contracts.
- Phase 35 owns loss-side softened `s_min`, loss scaling, energy weighting,
  Huber delta, and causal training mode.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CURR-01 | Adaptive stage-assignment methodology contract. [VERIFIED: `.planning/REQUIREMENTS.md:41`] | Plan must author/update the Phase 33 packet and specify offline EDA methodology, stable `record_key` labels, preserved Stage-2/Stage-5 roles, and deferred population floor. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:7-72`] |
| CURR-02 | `tau_L` and `L_max` computation contracts. [VERIFIED: `.planning/REQUIREMENTS.md:42`] | Plan must preserve `D ~= 4.6416`, characteristic `L_max`, `tau_L` outside `IC13`, and Rosenstein baseline/deferred estimator details. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:74-149`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:1-167`] |
| CURR-03 | Dual-path stage-transition criteria contract. [VERIFIED: `.planning/REQUIREMENTS.md:43`] | Plan must replace one-way threshold prose with ADVANCE / RECOVER / HALT-REVIEW state-machine wording and mark numeric values provisional pending FUT Stage-0 pilot. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:60-71`, `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1666-1707`] |
| CURR-04 | Stage 0-6 inventory and gating contract. [VERIFIED: `.planning/REQUIREMENTS.md:44`] | Plan must define inventory/replay/catch-all, raw `L_norm`, nonfinite/degenerate `L_max` handling, no global clamp, and claimed/FUT treatment for unverified counts. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:151-225`] |
| CURR-05 | `s_min` curriculum stage-gate frame. [VERIFIED: `.planning/REQUIREMENTS.md:45`] | Plan must transcribe the resolved Phase 32 owner instruction: unsoftened geometric `s_min` for Stage-6 gate, loss-side matched-Plummer softening handed to Phase 35. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:20-22`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:16`] |
</phase_requirements>

## Summary

Phase 33 is a specwork-only transcription phase, not an implementation or empirical-calibration phase. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:5-14`, `.planning/ROADMAP.md:163-177`] The planner should produce one or more executable plans that first author/update Phase 33-owned evidence packets and the Phase 32 issue ledger rows, then make tightly scoped framework-spec edits in `ctl_instruction.md`, with `pinn_architecture.md` cross-links only if needed for consistency. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:20-31`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-114`]

The main planning hazard is not technical implementation complexity; it is source discipline. [VERIFIED: `AGENTS.md:31-125`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:86-99`] Roadmap/requirements wording that appears to lock `>10%`, shadow-method `tau_L`, or clipped `L_norm` has been superseded by resolved Phase 33 STOP gaps; those values remain deferred/FUT unless the owner later resolves them. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]

**Primary recommendation:** Plan Phase 33 as evidence-packet-first spec editing: packet/ledger update for each CURR-owned row, then `ctl_instruction.md` contract edits, then deterministic source-token and forbidden-path verification. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md` existence via local file listing, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]

## Project Constraints (from AGENTS.md)

| Directive | Planning Impact |
|-----------|-----------------|
| v1.6 phases must not invent content where source materials are silent or ambiguous. [VERIFIED: `AGENTS.md:31-57`] | Any new semantic/process/cross-phase decision encountered during planning or execution must produce `## RESEARCH BLOCKED` or a STOP gap, not a guessed contract. |
| v1.6 specwork edits are limited to `ctl_instruction.md` and `pinn_architecture.md`; `sampling_method.md`, read-only reports, live `pinn/`, EDA, Stage-0 pilot, and training-loop code are out of scope. [VERIFIED: `AGENTS.md:39-57`] | Plans must include forbidden-path checks and must not schedule implementation tasks. |
| Locked v1.4/v1.5 outcomes are hard constraints, including 14D `[tau, IC13]`, Jacobi IC13, mass-weighted COM head, PHYS-03 `eps_soft = 1e-5`, SCS gate, raw-mass `D ~= 4.6416`, and PIPE/VAL contracts. [VERIFIED: `AGENTS.md:44-45`, `.planning/REQUIREMENTS.md:92`] | Phase 33 must reconcile curriculum text against these conventions instead of reopening them. |
| Live `pinn/` code is not a grounding source. [VERIFIED: `AGENTS.md:44`, `AGENTS.md:265-267`] | Plans may only mention live code in FUT handoff/divergence contexts, not as evidence for spec decisions. |
| STOP gaps require phase-local gap register entries and milestone index updates with required fields. [VERIFIED: `AGENTS.md:91-125`] | Plan verification must inspect any new `33-GAPS.md` / `v1.6-GAPS.md` edits for complete STOP fields. |
| Session start git state must be surfaced and unrelated changes preserved. [VERIFIED: `AGENTS.md:143-183`] | Planner/executor must ignore the pre-existing dirty docs plan unless its status/hash changes; this research observed `## milestone/v1.6` and that one modified docs file. [VERIFIED: local `git status --short --branch`] |
| Agent commits, if later authorized by execution workflow, must use `scripts/agent-commit` with explicit owned paths. [VERIFIED: `AGENTS.md:185-224`] | This research does not commit; execution plans should still encode the repo commit protocol if commits are requested later. |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Evidence packet and ledger lifecycle | Planning artifacts | Framework specs | The Phase 32 ledger says Phase 33-owned rows require a packet before spec edits. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:20-31`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`] |
| Adaptive stage-assignment contract | `ctl_instruction.md` framework spec | Phase 33 evidence packet | The roadmap and SPEC target `ctl_instruction.md` for curriculum-stage contracts. [VERIFIED: `.planning/ROADMAP.md:163-177`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-110`] |
| `L_max`, `tau_L`, and metadata contract | `ctl_instruction.md` framework spec | Phase 32 D packet | Existing invariant text lives in Step 3 and the D conflict packet constrains the active scale. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1019-1215`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:1-167`] |
| Stage transitions | `ctl_instruction.md` framework spec | Phase 34/35 handoffs | Current transition text lives under `Stage Transition Criteria`, while Phase 34/35 own later training/loss contracts. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1666-1740`, `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:107-113`] |
| Stage 0-6 inventory/gating | `ctl_instruction.md` framework spec | Dataset-fact citations | Current inventory text is in the early stratification section and Step 5; unverified counts must be marked claimed/FUT. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:105-260`, `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1425-1478`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:73-84`] |
| Loss-side softening cross-reference | `pinn_architecture.md` framework spec | Phase 35 handoff | `pinn_architecture.md` owns training residual/energy softening; Phase 33 only cross-links to prevent `s_min` confusion. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:359-410`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:492-542`] |
| Verification | Local shell/Python checks | Git status guards | Phase 32 precedent uses deterministic source checks and protected-path guards, not runtime training probes. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-04-PLAN.md:128-173`] |

## Standard Stack

### Core

| Library / Artifact | Version | Purpose | Why Standard |
|--------------------|---------|---------|--------------|
| `ctl_instruction.md` | v1.6 active framework spec | Primary edit target for curriculum-stage contracts. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-110`] | Roadmap and SPEC assign Phase 33 curriculum contracts to this file. [VERIFIED: `.planning/ROADMAP.md:163-177`] |
| `pinn_architecture.md` | v1.6 active framework spec | Optional cross-link target for architecture/loss-side consistency. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:107-109`] | Training residual and energy softening already live here. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:359-410`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:492-542`] |
| Phase 32 evidence protocol and issue ledger | v1.6 Phase 32 | Packet-before-edit governance for issue-03 findings. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:1-36`] | Phase 33-owned rows are explicitly seeded there. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:20-31`] |
| `rg` | 15.1.0 | Deterministic source-token and forbidden-path checks. [VERIFIED: local `rg --version`] | Existing Phase 32 plans rely on `rg` checks. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-03-PLAN.md:127-189`] |
| `python3` | 3.14.5 | Parser-backed validation for required text, metadata, and status invariants. [VERIFIED: local `python3 --version`] | Existing Phase 32 plans use inline Python assertions for freshness and field checks. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-03-PLAN.md:123-188`] |
| `git` | 2.54.0 | Scoped status, diff, and protected-path guards. [VERIFIED: local `git --version`] | AGENTS requires git-state visibility and explicit-path discipline. [VERIFIED: `AGENTS.md:143-224`] |

### Supporting

| Library / Artifact | Version | Purpose | When to Use |
|--------------------|---------|---------|-------------|
| `scripts/agent-commit` | present and executable | Commit wrapper for later execution, not this research run. [VERIFIED: local `test -x scripts/agent-commit`] | Use only if execution workflow commits Phase 33 work and user/orchestrator permits it. [VERIFIED: `AGENTS.md:185-224`; user requested no commit for this research] |
| `.planning/milestones/v1.6-GAPS.md` | active, 6 total gaps, 0 open | Milestone STOP index. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:1-36`] | Update only if a new Phase 33 STOP gap is opened. [VERIFIED: `AGENTS.md:91-125`] |
| `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md` | opened 2026-06-21, all Phase 33 gaps resolved | Source of superseding owner instructions for population floor, `tau_L`, and `L_norm`. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:1-228`] | Read before interpreting roadmap/requirements wording that appears to lock deferred values. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Evidence-packet-first spec editing | Directly edit `ctl_instruction.md` from roadmap text | Not acceptable because Phase 32 ledger requires packets before spec edits and several roadmap phrasings were superseded by resolved gaps. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`] |
| Local deterministic source checks | Runtime EDA / Stage-0 pilot / training probes | Out of scope for Phase 33; those are FUT/SCOPE-15. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-121`, `.planning/REQUIREMENTS.md:95`] |
| `ctl_instruction.md` primary edits | `sampling_method.md` or read-only reports | Forbidden by SCOPE-08/SCOPE-09 and Phase 33 SPEC. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-118`, `.planning/REQUIREMENTS.md:97-98`] |

**Installation:**

No package installation is needed for Phase 33. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-137`, local tool probes]

## Package Legitimacy Audit

No external packages are recommended or installed for Phase 33. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-137`]

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| none | n/a | n/a | n/a | n/a | n/a | No package work in scope. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-137`] |

**Packages removed due to [SLOP] verdict:** none. [VERIFIED: no package recommendations in this research]
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: no package recommendations in this research]

## Architecture Patterns

### System Architecture Diagram

```text
Phase 33 plan entry
  -> read 33-SPEC / 33-CONTEXT / 33-GAPS
  -> read Phase 32 ledger + relevant packets
  -> for each CURR-owned row:
       if packet/verdict linkage missing:
         author Phase 33 evidence packet + ledger update
       else:
         consume packet/verdict as constraint
  -> edit ctl_instruction.md curriculum sections
       -> optional pinn_architecture.md cross-link only for consistency
  -> run deterministic source checks
       -> required contract tokens present
       -> owner-pending values not locked
       -> forbidden paths untouched
       -> unrelated dirty docs file preserved
  -> summary / handoff
```

This flow reflects the Phase 32 ledger rule that owner phases must author packets before spec edits and the Phase 33 SPEC target-file boundary. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-121`]

### Recommended Project Structure

```text
.planning/phases/33-curriculum-stage-contracts/
├── 33-RESEARCH.md          # this planning research artifact
├── 33-*-PLAN.md            # planner output; count is planner discretion
├── 33-SUMMARY.md           # execution closeout, if phase execution runs
├── 33-GAPS.md              # existing resolved Phase 33 STOP gaps; update only for new gaps
└── evidence/               # recommended Phase 33-owned packets for CURR rows, if planner creates them
```

The existing Phase 33 directory already contains `33-CONTEXT.md`, `33-SPEC.md`, and `33-GAPS.md`; there is no existing `evidence/` subdirectory yet. [VERIFIED: local file reads/listing] If the planner creates Phase 33 packets, mirror the Phase 32 evidence layout rather than inventing a new schema. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md` existence via local file listing, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]

### Pattern 1: Packet-Before-Spec-Edit

**What:** Before editing a spec section for an owned issue-03 row, create or update the evidence packet, cite line ranges, set verdict/status, and update the ledger row. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]

**When to use:** Use for Phase 33-owned rows `M6`, `M7`, `D5`, `adaptive stage assignment`, and `L_max / tau_L`, and for consuming D-05/D-06 resolved owner instructions. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:16-31`]

**Example:**

```bash
# Source: Phase 32 packet/ledger verification pattern.
rg -n "M6|M7|D5|adaptive stage assignment|L_max / tau_L|AC-CURR" \
  .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
```

### Pattern 2: Contract Text With Explicit Deferred Holes

**What:** Write normative structure, but explicitly label unresolved numeric values as FUT/owner-pending rather than selecting defaults. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]

**When to use:** Use for population safeguard, final `tau_L` estimator/units/thresholds, clipped `L_norm` gate, and Stage-0 pilot thresholds. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:139-147`]

### Pattern 3: Protected-Path Guard

**What:** Run scoped git checks proving Phase 33 did not touch frozen/read-only files, live `pinn/`, generated data, or unrelated dirty docs. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`, `AGENTS.md:39-57`]

**When to use:** Use at every plan closeout and phase gate. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-04-PLAN.md:157-173`]

### Anti-Patterns to Avoid

- **Editing specs before packets:** Violates the Phase 32 ledger handoff. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]
- **Treating roadmap wording as newer than resolved gaps:** The resolved Phase 33 gap notes supersede roadmap/requirements phrases for population floor, `tau_L`, and `L_norm`. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]
- **Using live `pinn/` code as evidence:** Explicitly forbidden for v1.6 grounding. [VERIFIED: `AGENTS.md:44`, `.planning/REQUIREMENTS.md:98`]
- **Running EDA or Stage-0 pilot:** Explicitly FUT/SCOPE-15, not Phase 33. [VERIFIED: `.planning/REQUIREMENTS.md:95`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-121`]
- **Letting Phase 34/35 contracts leak in:** Phase 33 may cross-link handoffs but must not resolve replay/lookahead, ALM, loss, or causal-mode contracts. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:107-113`, `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:184-193`]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Evidence adjudication schema | New packet format or ad hoc notes | Phase 32 evidence template/protocol | The ledger and Phase 36 handoff expect packet/verdict linkage. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`] |
| STOP handling | Informal TODO or planner assumption | `33-GAPS.md` plus `.planning/milestones/v1.6-GAPS.md` | AGENTS requires full STOP fields and milestone index updates. [VERIFIED: `AGENTS.md:91-125`] |
| Source validation | Manual eyeballing only | `rg` and `python3` assertions | Phase 32 precedent uses deterministic token/field checks. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-03-PLAN.md:123-189`] |
| Numeric calibration | One-off defaults in spec prose | Explicit FUT/owner-pending holes | Population floor, `tau_L` thresholds, clipped gates, and pilot thresholds are not Phase 33 decisions. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:139-147`] |
| Softening semantics | One shared epsilon rule | Dual-context `epsilon_inv` / `epsilon_train` wording | Phase 32 resolved D-06 as offline `epsilon_inv = 1e-10`, training `epsilon_train = 1e-5`. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:21-22`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:17`] |

**Key insight:** Phase 33's hardest work is preserving adjudication provenance while editing prose; custom shortcuts create spec drift faster than they save time. [VERIFIED: `AGENTS.md:31-125`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:86-99`]

## Common Pitfalls

### Pitfall 1: Re-Locking Superseded Values

**What goes wrong:** The plan copies roadmap/requirements text that appears to lock `>10%`, shadow-method `tau_L`, or `np.clip(L_norm, 0, 1)`. [VERIFIED: `.planning/ROADMAP.md:170-173`, `.planning/REQUIREMENTS.md:41-44`]

**Why it happens:** Those older phrasings were superseded by resolved Phase 33 gaps. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]

**How to avoid:** Treat gap resolutions as the controlling source when they contradict roadmap shorthand. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:50-84`]

**Warning signs:** Plan text says `>10%` is locked, shadow trajectory is canonical, or clipped `L_norm` is authorized. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:219-228`]

### Pitfall 2: Spec Edits Without Packet/Linked Ledger

**What goes wrong:** `ctl_instruction.md` changes land without Phase 33-owned evidence packet and ledger update. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]

**Why it happens:** Phase 32 completed only the shared machinery and selected headline packets; non-headline rows remain owner-phase packet work. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:20-31`] 

**How to avoid:** Make packet/ledger tasks the first wave or first task in each contract slice. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-01-PLAN.md:167-179`]

**Warning signs:** A plan's first edit action targets `ctl_instruction.md` before referencing `32-ISSUE-LEDGER.md` and evidence packet paths. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]

### Pitfall 3: Blurring Stage Gate and Loss Softening

**What goes wrong:** The curriculum `s_min` gate is softened because loss-side residual/energy uses matched-Plummer softening. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md:1-151`]

**Why it happens:** The same close-encounter vocabulary appears in curriculum labels and training loss. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md:113-117`]

**How to avoid:** Write Stage-6 gate as unsoftened geometric `s_min`; cross-link Phase 35 for matched-Plummer loss-side terms. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:20-22`]

**Warning signs:** Contract text says `max(s_min, epsilon)` for the Stage-6 stage gate. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:16`]

### Pitfall 4: Reopening Raw-Mass `D`

**What goes wrong:** Phase 33 reintroduces `D = 6.694` into `L_max` / `tau_L` discussion. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:1-167`]

**Why it happens:** The issue doc contains a conflicting `D = 6.694` claim. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:15-31`]

**How to avoid:** Use the Phase 32 D packet and current `ctl_instruction.md` global-scale section as governing sources. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:33-60`, `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:929`]

**Warning signs:** Any Phase 33 spec diff contains `6.694` outside a rejection/provenance note. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:222-224`]

### Pitfall 5: UI Gate False Positive

**What goes wrong:** Planning tries to create a UI spec or frontend tasks. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:20-22`]

**Why it happens:** The plan-phase UI gate may report a frontend block. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:98-100`]

**How to avoid:** Treat roadmap `UI hint: no` as controlling and use `--skip-ui` if needed. [VERIFIED: `.planning/ROADMAP.md:177`, `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:98-100`]

**Warning signs:** A Phase 33 plan includes frontend files, UI acceptance criteria, or visual review. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:20-22`]

## Code Examples

Verified local patterns for planner/executor commands:

### Source-Token Contract Check

```bash
# Source: Phase 32 parser-backed validation pattern and Phase 33 SPEC acceptance criteria.
python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); required=['characteristic angular-momentum scale','tau_L','IC13','unsoftened geometric s_min','No global clamp']; missing=[x for x in required if x not in txt]; assert not missing, missing"
```

### Forbidden-Path Guard

```bash
# Source: AGENTS v1.6 boundaries and Phase 33 SPEC prohibitions.
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn/ \
  simulation_data/
```

Expected output is empty for Phase 33-owned diffs. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-137`]

### Requirements-to-Plan Coverage Check

```bash
# Source: 33-SPEC acceptance criterion requiring CURR-01..05 in plan requirements fields.
python3 -c "from pathlib import Path; root=Path('.planning/phases/33-curriculum-stage-contracts'); plans=list(root.glob('33-*-PLAN.md')); text='\\n'.join(p.read_text() for p in plans); req=['CURR-01','CURR-02','CURR-03','CURR-04','CURR-05']; missing=[r for r in req if r not in text]; assert plans, 'no plans found'; assert not missing, missing"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Lock `>10%` population safeguard from roadmap shorthand. | Specify offline EDA methodology and defer population floor to FUT admitted-set EDA. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`] | 2026-06-22 Phase 33 gap resolution. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:58-72`] | Prevents unsupported stage distribution policy from becoming contract. |
| Adopt shadow-trajectory `tau_L` plus PCA shortcut. | Retain Rosenstein-style baseline as revisable; defer estimator/units/thresholds. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`] | 2026-06-22 Phase 33 gap resolution. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`] | Avoids selecting ungrounded chaos-estimation method. |
| Treat `L_max` as global maximum and clamp `L_norm`. | Treat `L_max` as characteristic scale; store raw `L_norm`; no global clamp. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:151-225`] | 2026-06-22 Phase 33 gap resolution. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`] | Preserves diagnostic overshoot and degenerate-scale handling. |
| D-05/D-06 owner decisions deferred after Phase 32 packet creation. | D-05 and D-06 have resolved owner instructions in the milestone gap index and ledger. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:20-22`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:16-17`] | 2026-06-21 owner instruction. [VERIFIED: `.planning/milestones/v1.6-GAPS.md:20-22`] | Phase 33 can transcribe unsoftened `s_min` gate and dual epsilon context without blocking. |
| `D = 6.694` issue-doc scale. | Raw-mass `D ~= 4.6416` remains active; `6.694` rejected as mass-fraction convention. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:1-167`] | Verified in Phase 32 Plan 32-02. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:30`] | Phase 33 must use `4.6416` in `L_max`/`tau_L` contract context. |

**Deprecated/outdated:**

- Roadmap shorthand that appears to lock population floor, shadow `tau_L`, or clipped `L_norm` is outdated relative to `33-GAPS.md`. [VERIFIED: `.planning/ROADMAP.md:170-173`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:54-72`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:131-149`, `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]
- Issue-doc `D = 6.694` is rejected for the active raw-mass framework. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:140-151`]
- Global `L_norm` clamp is not authorized. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:213-225`]

## Assumptions Log

No `[ASSUMED]` claims are used in this research. All substantive recommendations are tied to local project artifacts or command probes. [VERIFIED: local research process]

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| none | n/a | n/a | n/a |

## Open Questions

1. **How many Phase 33 plan files should exist?**
   - What we know: Planner may decide the number and grouping if every `CURR-01` through `CURR-05` appears in a plan `requirements` field. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:102-105`]
   - What's unclear: The optimal grouping is not locked. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md:102-105`]
   - Recommendation: Use 2-3 plans if keeping packet work separate from spec edits improves reviewability; use 1 plan only if it still preserves packet-before-edit ordering. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]

2. **Should Phase 33 create a local `evidence/` directory?**
   - What we know: Phase 32 used an `evidence/` directory and seeded Phase 33-owned rows that need packets. [VERIFIED: local file listing, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:20-31`]
   - What's unclear: `33-SPEC.md` does not mandate the directory name. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-137`]
   - Recommendation: Mirror Phase 32 as `.planning/phases/33-curriculum-stage-contracts/evidence/` to keep packet paths predictable. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md` local existence]

3. **STOP risks the planner must preserve**
   - What we know: No new STOP gap was found during this research. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:1-228`, `.planning/milestones/v1.6-GAPS.md:1-36`]
   - What's unclear: Execution may surface new source-silent details when writing exact prose. [VERIFIED: `AGENTS.md:91-125`]
   - Recommendation: If exact prose requires selecting a population floor, `tau_L` estimator, clipped gate, transition threshold, unverified trajectory count, or Phase 34/35 contract, STOP and record the gap before dependent edits. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:139-147`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:219-228`]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `rg` | source-token checks and file scans | yes | 15.1.0 [VERIFIED: local `rg --version`] | Python text search if missing. |
| `python3` | parser-backed assertions | yes | 3.14.5 [VERIFIED: local `python3 --version`] | POSIX shell checks for simple tokens; lower confidence. |
| `git` | status/protected-path guards | yes | 2.54.0 [VERIFIED: local `git --version`] | none for git-state policy. |
| `node` | GSD tooling shim | yes | v24.16.0 [VERIFIED: local `node --version`] | none needed during phase execution if GSD already invoked. |
| `scripts/agent-commit` | later execution commits, if authorized | yes | executable [VERIFIED: local `test -x scripts/agent-commit`] | no raw `git commit`; stop if wrapper unavailable and commit required. [VERIFIED: `AGENTS.md:185-224`] |
| `pytest` | repository tests | no | n/a [VERIFIED: local `command -v pytest`] | Phase 33 should use shell/Python source checks; no pytest requirement is in scope. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`] |

**Missing dependencies with no fallback:**

- None for Phase 33 planning/execution. [VERIFIED: local tool probes]

**Missing dependencies with fallback:**

- `pytest` is missing; Phase 33 validation should use deterministic local shell/Python checks rather than pytest. [VERIFIED: local `command -v pytest`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | No dedicated Phase 33 test framework; use `rg`, `python3 -c`, and git protected-path checks. [VERIFIED: local file scan; `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`] |
| Config file | none for Phase 33; `.planning/config.json` has `workflow.nyquist_validation: true`. [VERIFIED: `.planning/config.json:1-15`] |
| Quick run command | `rg -n "CURR-01|CURR-02|CURR-03|CURR-04|CURR-05" .planning/phases/33-curriculum-stage-contracts/33-*-PLAN.md` [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-130`] |
| Full suite command | planner should compose per-plan `python3 -c` token checks plus forbidden-path git diff checks. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:131-137`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-04-PLAN.md:128-173`] |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| CURR-01 | Adaptive assignment contract and deferred population floor. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:35-44`] | source-token / negative-token | `python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); assert 'record_key' in txt; assert '>10%' not in txt or 'not locked' in txt"` | no Wave 0 command file; embed in plan. |
| CURR-02 | Characteristic `L_max`, raw-mass D, `tau_L` metadata exclusion. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:46-58`] | source-token | `python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['characteristic','D ~= 4.6416','tau_L','IC13']; missing=[r for r in req if r not in txt]; assert not missing, missing"` | no Wave 0 command file; embed in plan. |
| CURR-03 | ADVANCE/RECOVER/HALT-REVIEW state machine. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:60-71`] | source-token / negative-token | `python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['ADVANCE','RECOVER','HALT','REVIEW','NaN','Inf']; missing=[r for r in req if r not in txt]; assert not missing, missing"` | no Wave 0 command file; embed in plan. |
| CURR-04 | Stage 0-6 inventory, raw `L_norm`, nonfinite/degenerate guard, no clamp. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:73-84`] | source-token / negative-token | `python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['Stage 0','Stage 6','raw','L_norm','No global']; missing=[r for r in req if r not in txt]; assert not missing, missing"` | no Wave 0 command file; embed in plan. |
| CURR-05 | Unsoftened geometric `s_min` stage gate and Phase 35 loss-side handoff. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:86-90`] | source-token | `python3 -c "from pathlib import Path; txt=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['unsoftened geometric','s_min','Phase 35','matched-Plummer']; missing=[r for r in req if r not in txt]; assert not missing, missing"` | no Wave 0 command file; embed in plan. |

### Sampling Rate

- **Per task commit:** Run task-local source-token checks and `git diff --name-only` guard for forbidden paths. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]
- **Per wave merge:** Run all requirement-token checks and plan coverage check for `CURR-01..05`. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]
- **Phase gate:** Full structural/source suite green before `$gsd-verify-work`; no EDA, Stage-0 pilot, or training implementation. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:231-232`]

### Wave 0 Gaps

- [ ] No dedicated Phase 33 validation script exists; each plan must embed deterministic `rg` / `python3 -c` commands. [VERIFIED: local file scan, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`]
- [ ] If the planner creates Phase 33 evidence packets, it should create `evidence/` and copy/adapt the Phase 32 packet schema rather than designing a new schema. [VERIFIED: local Phase 32 evidence directory, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth surface is in Phase 33; specwork-only docs. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-121`] |
| V3 Session Management | no | No session surface is in Phase 33. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-121`] |
| V4 Access Control | yes, repository write boundary | Explicit allowed/forbidden paths and git status guards. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:116-137`, `AGENTS.md:143-183`] |
| V5 Input Validation | yes, source-input discipline | Line-range citations, source hierarchy, packet/verdict linkage, and token checks. [VERIFIED: `AGENTS.md:59-89`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`] |
| V6 Cryptography | no | No cryptographic feature or secret handling is in scope. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-121`] |

### Known Threat Patterns for Specwork

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Silent semantic default selection | Tampering | STOP protocol and gap register before dependent edits. [VERIFIED: `AGENTS.md:91-125`] |
| Unauthorized file modification | Tampering | Protected-path `git diff --name-only` guard. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:129-137`] |
| Evidence provenance confusion | Repudiation | Evidence packets with line ranges and ledger links. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`] |
| Treating live code as authority | Tampering | Ban live `pinn/` grounding and confine it to FUT handoff contexts. [VERIFIED: `AGENTS.md:44`, `.planning/REQUIREMENTS.md:98`] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md` - locked decisions, discretion, deferred scope. [VERIFIED: local file read]
- `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md` - locked requirements, boundaries, acceptance criteria, prohibitions. [VERIFIED: local file read]
- `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md` - resolved Phase 33 owner instructions for population floor, `tau_L`, and `L_norm`. [VERIFIED: local file read]
- `.planning/REQUIREMENTS.md` - CURR-01..05, SCOPE-12..15. [VERIFIED: local `rg`]
- `.planning/ROADMAP.md` - Phase 33 goal/dependency/success criteria and `UI hint: no`. [VERIFIED: local `rg`]
- `.planning/STATE.md` - v1.6 phase state/history and STOP protocol reminders. [VERIFIED: local `rg`]
- `AGENTS.md` - v1.6 STOP protocol, source hierarchy, scope boundaries, git protocol. [VERIFIED: local file read]
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` - packet-before-edit rows and Phase 33 ownership. [VERIFIED: local `rg`]
- Phase 32 evidence packets `d-05-s-min-frame.md`, `d-06-epsilon-strategy.md`, `d-6-694-conflict.md`. [VERIFIED: local file read]
- Framework specs `ctl_instruction.md` and `pinn_architecture.md` - current edit surfaces and softening/global-scale baselines. [VERIFIED: local `rg` / `nl -ba`]

### Secondary (MEDIUM confidence)

- None. External web or package documentation was not needed for this internal specwork phase. [VERIFIED: research-plan seam produced no applicable real library target]

### Tertiary (LOW confidence)

- GSD research-store cached a local-project digest under provider `codebase`; it is informational only and not used as authority. [VERIFIED: `research-store put` command output]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - direct local tool probes and project artifacts define the stack; no external dependencies are recommended. [VERIFIED: local tool probes, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-137`]
- Architecture: HIGH - Phase 32 ledger and Phase 33 SPEC define the packet-before-edit and target-file architecture. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md:36`, `.planning/phases/33-curriculum-stage-contracts/33-SPEC.md:104-137`]
- Pitfalls: HIGH - pitfalls are grounded in resolved gaps, AGENTS STOP protocol, and existing Phase 32 packet precedent. [VERIFIED: `.planning/phases/33-curriculum-stage-contracts/33-GAPS.md:1-228`, `AGENTS.md:31-125`]

**Research date:** 2026-06-22
**Valid until:** 2026-07-22, unless Phase 33 gaps, Phase 32 ledger rows, or v1.6 governance change first. [VERIFIED: local research date and active planning artifacts]

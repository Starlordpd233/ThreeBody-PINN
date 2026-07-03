# Phase 32 Research

**Date:** 2026-06-21
**Status:** Ready for planning
**Workspace:** `<home>/Desktop/3_body_problem/.worktrees/specwork` on `milestone/v1.6` [VERIFIED: `git status --short --branch`]

<user_constraints>
## User Constraints (from CONTEXT.md)

The following Phase 32 constraints are copied from `32-CONTEXT.md`; keep these as locked planning inputs. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:43-65`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:129-135`]

### Locked Decisions

#### Artifact Topology
- **D-01:** Use the v1.5 Phase 25 pattern as the implementation baseline: a phase-local evidence directory, an evidence-packet template, a protocol README, a stable issue ledger, and later verification/validation artifacts in the Phase 32 directory.
- **D-02:** Keep Phase 32 artifacts process-local. The only acceptable cross-file planning mutations are STOP/gap register updates if a source-silent semantic decision is encountered.
- **D-03:** Do not update `.planning/STATE.md` directly in this discussion run because GSD's `gsd-tools.cjs` is currently failing and the existing `STATE.md` modification is user-owned.

#### Headline Conflict Handling
- **D-04:** Create separate evidence packets for D-04 causal-training mode, D-05 `s_min` frame, D-06 epsilon strategy, M14 gradient clipping, and the `D = 6.694` conflict. Do not collapse these into one umbrella packet; each has different downstream owners and different STOP risk.
- **D-05:** Treat D-04/D-05/D-06 as owner-routed semantic decisions. If no explicit prior user instruction resolves one at Phase 32 execution time, the packet records `defer-with-blocker` or an OPEN STOP gap instead of selecting a default.
- **D-06:** Treat the `D = 6.694` conflict as constrained by v1.5 Phase 25 EVID-10 and SCOPE-12: `D = (G*T^2)^(1/3) ~= 4.6416` stands unless Phase 32 surfaces a genuine first-principles contradiction and obtains user instruction.
- **D-07:** Treat M14 as a split record: Phase 32 can lock the structural merge (`clip_value = C_stage * median(recent global gradient norms)`) if grounded, while bootstrap floor, early-stage exact `C`, and history-reset mechanics remain downstream/FUT if source-silent.

#### Ledger and Verification
- **D-08:** Seed the ledger with every selected issue-03 finding consumed by Phases 32-36, not just the five headline conflicts. Headline packets are Phase 32-owned; remaining packets may be authored by owning contract phases immediately before their edits, matching the v1.5 split-reading precedent.
- **D-09:** Preserve the lifecycle invariant exactly: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` or `DEFERRED`; `FIX_APPLIED` is never terminal.
- **D-10:** Phase 32 must include deterministic structural checks for packet schema, protocol lifecycle, ledger row coverage, headline verdict/defer coverage, no forbidden spec edits, and absence of `32-*-PLAN.md` before this workflow stops.

#### Planning Boundary
- **D-11:** Auto-advance is intentionally stopped after discussion because the user explicitly requested "stop before planning phase starts." No `32-*-PLAN.md` should exist at the end of this run.

### the agent's Discretion
- Exact packet filename slugs, as long as they are stable, grep-friendly, and mapped in the protocol.
- Exact Markdown table layout for the ledger, as long as required fields and lifecycle states are present.
- Exact shell commands used for structural checks, as long as they are deterministic and recorded.

### Deferred Ideas (OUT OF SCOPE)
- Framework-spec contract transcription is deferred to Phases 33, 34, and 35.
- Runnable acceptance execution and milestone handoff are deferred to Phase 36.
- Training-loop/DataLoader/ALM implementation, adaptive-stage EDA, Stage-0 pilot calibration, and data regeneration remain FUT-01/FUT-04/FUT.
</user_constraints>

## Project Constraints (from AGENTS.md)

| Constraint | Planning Impact |
|---|---|
| v1.6 Phases 30-36 are adjudication phases where source-silent or ambiguous MUST-surface decisions stop affected work. [VERIFIED: `AGENTS.md:18`, `AGENTS.md:31-40`] | Plans must include STOP-safe branches for D-04/D-05/D-06 and any locked-convention overturn attempt. |
| The v1.6 resolution doc is a candidate verdict source, not authority. [VERIFIED: `AGENTS.md:36`, `AGENTS.md:108`] | Packets must cite independent grounding beside the resolution-doc position before assigning a verdict. |
| v1.6 is specwork-only; Phase 32 must not implement training-loop code, run adaptive-stage EDA, or run a Stage-0 pilot. [VERIFIED: `AGENTS.md:39`] | Validation should be structural/formula sanity only; no `pinn/` production-code work. |
| Live `pinn/` code is not grounding. [VERIFIED: `AGENTS.md:53`] | Packet templates must ban live-code evidence except FUT handoff notes. |
| The v1.6 milestone gap index is `.planning/milestones/v1.6-GAPS.md`, created on the first v1.6 STOP gap. [VERIFIED: `AGENTS.md:40`; verified absent in workspace] | Do not create `v1.6-GAPS.md` unless a real STOP gap is opened. |
| Sequentialthinking is required for multi-step tasks. [VERIFIED: `AGENTS.md:8`] | Already used for this research run; planner should preserve STOP-step reasoning checks in execution tasks. |

## Phase Requirements

| Requirement | Phase 32 Support Needed |
|---|---|
| EVID-11 | Evidence packets cite issue-doc, resolution-doc, current-spec, and relevant locked-convention or dataset evidence by line range. [VERIFIED: `.planning/REQUIREMENTS.md:33`] |
| EVID-12 | Each finding gets exactly one fixed-set verdict with reasoning. [VERIFIED: `.planning/REQUIREMENTS.md:34`] |
| EVID-13 | False positives are documented as intentional non-changes. [VERIFIED: `.planning/REQUIREMENTS.md:35`] |
| EVID-14 | Accepted findings get before/after notes naming spec section, contract, and verification step. [VERIFIED: `.planning/REQUIREMENTS.md:36`] |
| EVID-15 | Source conflicts are adjudicated at root cause, with D-04/D-05/D-06, M14, and the D conflict explicitly named. [VERIFIED: `.planning/REQUIREMENTS.md:37`] |

## Research Decision

Research is required because Phase 32 is not a code implementation phase; it defines the adjudication machinery that Phases 33-36 must consume before framework-spec transcription and acceptance. [VERIFIED: `.planning/ROADMAP.md:140-152`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-SPEC.md:21-56`]

Primary recommendation: adapt the v1.5 Phase 25 packet/protocol/ledger pattern into a Phase 32-local issue-03 evidence system, author only the five headline packets in Phase 32, seed the full selected-finding ledger, and route D-04/D-05/D-06 through `defer-with-blocker` or STOP gaps unless explicit owner instruction exists at execution time. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:43-57`, `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:79-98`]

Do not browse the web or install packages; all required evidence is local and the phase has no external package dependency. [VERIFIED: user prompt; `.planning/ROADMAP.md:41-57`]

## Source Map

| Source | What It Contributes | Citation Strategy |
|---|---|---|
| `AGENTS.md` | v1.6 STOP protocol, candidate-source standing, specwork-only boundary, no-live-code rule, gap-index path. [VERIFIED: `AGENTS.md:18`, `AGENTS.md:31-40`, `AGENTS.md:53`] | Cite by line range for governance constraints in protocol and gap instructions. |
| `.planning/ROADMAP.md` | Phase 32 goal, dependency on Phase 31, EVID requirement list, success criteria, verification loop, downstream phase owners. [VERIFIED: `.planning/ROADMAP.md:41-57`, `.planning/ROADMAP.md:140-152`, `.planning/ROADMAP.md:156-214`] | Cite Phase 32 lines for scope; cite Phase 33-36 lines when routing downstream owners. |
| `.planning/REQUIREMENTS.md` | EVID-11..15, SCOPE-12..15, no-live-code and frozen/read-only boundaries. [VERIFIED: `.planning/REQUIREMENTS.md:31-38`, `.planning/REQUIREMENTS.md:88-99`] | Use requirement IDs in packet header and acceptance-check handoff. |
| `.planning/PROJECT.md` | Current milestone state: Phase 31 READY-WITH-CAVEATS, Phases 32-36 unblocked, Phase 32 next, v1.6 specwork-only. [VERIFIED: `.planning/PROJECT.md:76-82`, `.planning/PROJECT.md:119-138`] | Use as status context only; do not treat as packet evidence. |
| `32-CONTEXT.md` | Locked implementation decisions D-01..D-11, artifact topology, no-spec-edit boundary, exact discretion areas. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:20-65`] | Copy constraints into plans; do not re-open without user instruction. |
| `32-SPEC.md` | Seven locked Phase 32 requirements, boundaries, constraints, acceptance criteria, prohibitions. [VERIFIED: `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-SPEC.md:21-99`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-SPEC.md:135-147`] | Use as the executable plan contract. |
| `31-READINESS-REPORT.md` | Gate result: READY-WITH-CAVEATS; 18/18 selected findings covered; D-04/D-05/D-06 and GAP-17 routed to Phase 32 EVID-15. [VERIFIED: `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:15-36`, `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:207-218`, `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:271-303`] | Cite for readiness and caveat routing, not final verdicts. |
| `31-RESOLUTION-MAP.md` | Resolution-doc identity, section line ranges, selected-finding map, citation guide, direction preview, GAP carry-forward table. [VERIFIED: `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:16-34`, `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:71-130`, `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:132-164`, `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:190-225`] | Packet authors should start here, then verify against the underlying doc lines. |
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | Non-authoritative issue positions and proposed fixes for D-04/D-05/D-06/M14/D conflict. [VERIFIED: `pinn_instruction/issues/03-curriculum-and-training-loop.md:16-86`, `pinn_instruction/issues/03-curriculum-and-training-loop.md:229-326`, `pinn_instruction/issues/03-curriculum-and-training-loop.md:383-430`, `pinn_instruction/issues/03-curriculum-and-training-loop.md:463-485`] | Packets cite exact issue-doc line ranges beside resolution-doc ranges; do not cite whole file. |
| `03-final-resolution.md` | Candidate verdict source with §1.1/§1.2/§1.3/§1.8/§1.16 headline anchors, claim matrix, disagreement register, gap register. [VERIFIED: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:24-35`, `.../03-final-resolution.md:52-55`, `.../03-final-resolution.md:84-87`, `.../03-final-resolution.md:104-118`, `.../03-final-resolution.md:134-138`, `.../03-final-resolution.md:169-172`, `.../03-final-resolution.md:188-212`, `.../03-final-resolution.md:213-238`] | Cite `path:start-end` plus §/claim IDs. Treat report columns as provenance, not votes. |
| v1.5 Phase 25 `_TEMPLATE.md` and `README.md` | Packet sections, verdict enum, status lifecycle, packet-start procedure, ID-to-filename map pattern. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md:1-110`, `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:1-148`] | Adapt schema, source paths, and IDs to issue-03; preserve enum and lifecycle exactly. |
| v1.5 `compute-globals-D.md` | Worked precedent for `D=6.694` root-cause adjudication and first-principles dimensional analysis. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:46-82`, `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:84-123`] | Reuse reasoning pattern; Phase 32 should not re-open raw-mass D without a genuine contradiction and user instruction. |
| Current framework specs | Read-only baseline evidence for current contracts: `ctl_instruction.md` §2.5 D convention and clipping/loss sections; `pinn_architecture.md` softening, causal loss, ALM, gradient clipping. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:897-929`, `ctl_instruction.md:1554-1666`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:359-416`, `pinn_architecture.md:492-540`, `pinn_architecture.md:671-720`] | Packet authors must cite exact current-spec line ranges but must not edit specs in Phase 32. |

## Existing Pattern

Use the v1.5 Phase 25 pattern, not a new schema. [VERIFIED: `32-CONTEXT.md:43-57`; `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:1-13`]

Key pattern to adapt:

| Pattern | Phase 32 Adaptation |
|---|---|
| Phase-local `evidence/README.md` describes artifact roles, source policy, verdict enum, lifecycle, ID-to-filename map, packet-start procedure, non-goals. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:5-13`, `README.md:33-68`, `README.md:115-148`] | Create `32.../evidence/README.md` for issue-03 with source paths, SCOPE-12/13/14/15 boundaries, no-live-code rule, and Phase 32 headline packet ownership. |
| `_TEMPLATE.md` has stable sections for header, source positions, spec evidence, FUT handoff, first-principles check, verdict, root cause, locked convention, source correctness, before/after note, AC ID, status log. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md:1-110`] | Create `32.../evidence/_TEMPLATE.md`; replace issue-02 dataset annex with v1.6 locked-convention/current-spec/Phase31-map evidence fields. |
| `PENDING + Verdict + Evidence Packet` means adjudicated-but-unfixed when the fix is owned downstream. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:63-68`] | Use this for headline packets whose spec edits are owned by Phases 33-35. |
| `FIX_APPLIED` is never terminal and status transitions are mirrored in ledger and packet logs. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:47-61`, `.planning/ROADMAP.md:49-57`] | Preserve exact lifecycle and require same-commit ledger/packet updates during execution. |
| Phase 25 authored only machinery plus named conflict records, while non-conflict packets could be authored by owning downstream phases. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:95-102`, `32-CONTEXT.md:54-57`] | Phase 32 authors five headline packets; Phases 33-35 may author remaining packets immediately before edits, using the Phase 32 protocol. |

## Artifact Plan

Phase 32 execution should create or update exactly these Phase 32-local artifacts unless a STOP gap requires the two gap files. [VERIFIED: `32-SPEC.md:23-56`, `32-CONTEXT.md:43-57`]

| Artifact | Required? | Purpose |
|---|---:|---|
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md` | Yes | Protocol, source hierarchy, verdict enum, lifecycle, packet-start procedure, ID-to-filename map. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md` | Yes | Issue-03 packet schema adapted from v1.5. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` | Yes | Stable issue ledger for all selected findings consumed by Phases 32-36. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-04-causal-training-mode.md` | Yes | Headline packet for D-04 causal mode. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md` | Yes | Headline packet for D-05 stage-gate / loss-frame split. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-06-epsilon-strategy.md` | Yes | Headline packet for static/invariant epsilon strategy. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md` | Yes | Headline packet for M14 structural merge plus deferred execution details. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md` | Yes | Headline packet for raw-mass D ~= 4.6416 vs issue-doc 6.694. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md` | Yes | Recorded structural validation commands and outputs before Phase 32 closes. |
| `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` | Only on STOP | Phase-local STOP register. Do not create if no gap is opened. |
| `.planning/milestones/v1.6-GAPS.md` | Only on first v1.6 STOP | Milestone-wide STOP index. It is currently absent and should remain absent unless a gap is opened. |

Ledger seed rows should include all 18 selected findings from the Phase 31 map: `D-04`, `D-05`, `D-06`, `B-07`, `B-08`, `M6`, `M7`, `M14`, `M15`, `M16`, `D5`, `NS-12`, `NS-13`, `NS-18`, `adaptive stage assignment`, `D = 6.694`, `L_max / tau_L`, `ALM mu_p clamp`. [VERIFIED: `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:79-98`; `32-SPEC.md:33-36`]

Each ledger row should include: `Finding ID`, `Title`, `Owner Phase`, `Status`, `Verdict`, `Evidence Packet`, `Acceptance Check`, `Spec Targets`, `Dependents`, `Transition Log`. This field set is required by the Phase 32 spec and v1.5 precedent. [VERIFIED: `32-SPEC.md:33-36`; `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:7-13`]

## Headline Conflict Handling

| Conflict | Evidence Must Gather | Likely Handling | Downstream Owner | STOP Risk |
|---|---|---|---|---|
| D-04 causal-training mode | Issue options A/B/C and risk disclosure [VERIFIED: `03-curriculum-and-training-loop.md:16-40`, `03-curriculum-and-training-loop.md:121-150`, `03-curriculum-and-training-loop.md:383-410`]; resolution §1.1 and claim rows `CAU-01..CAU-05` [VERIFIED: `03-final-resolution.md:24-27`, `03-final-resolution.md:106-110`]; current loss/ALM baseline from specs [VERIFIED: `pinn_architecture.md:359-416`, `pinn_architecture.md:671-700`; `ctl_instruction.md:1554-1583`]. | `defer-with-blocker` or OPEN STOP gap unless explicit owner instruction exists. The resolution doc records current baseline and rejects dense-residual pseudo-ALM, but still surfaces final mode selection. [VERIFIED: `03-final-resolution.md:24-27`, `31-RESOLUTION-MAP.md:140-142`, `31-READINESS-REPORT.md:207-211`] | Primary Phase 35 `LOSS-04`; secondary Phase 34 `LOOP-01` if batch-windowing changes. [VERIFIED: `.planning/ROADMAP.md:174-183`, `.planning/ROADMAP.md:188-198`] | HIGH: choosing Option A/B/C changes training paradigm and cannot be inferred from auto mode. |
| D-05 `s_min` frame | Issue D-05 options and considered alternative [VERIFIED: `03-curriculum-and-training-loop.md:42-63`, `03-curriculum-and-training-loop.md:412-418`, `03-curriculum-and-training-loop.md:520-528`]; resolution §1.2, `SMIN-01..03`, DGR-02/03 [VERIFIED: `03-final-resolution.md:28-31`, `03-final-resolution.md:111-113`, `03-final-resolution.md:191-193`]; current spec baseline for geometric gate and matched-Plummer residual. [VERIFIED: `ctl_instruction.md:897-929`, `pinn_architecture.md:359-400`, `pinn_architecture.md:492-512`] | `defer-with-blocker` or OPEN STOP gap unless owner ratifies geometric gate or defines softened gate. Packet may state the loss-side matched-Plummer distinction but must not select the stage-gate frame without grounding. [VERIFIED: `03-final-resolution.md:28-31`, `31-RESOLUTION-MAP.md:141-142`] | Primary Phase 33 `CURR-05`; Phase 35 consumes loss-side implications. [VERIFIED: `.planning/ROADMAP.md:156-168`, `.planning/ROADMAP.md:188-198`] | HIGH: a gate-frame choice changes stage labels and downstream curriculum semantics. |
| D-06 epsilon strategy | Issue options A/B/C [VERIFIED: `03-curriculum-and-training-loop.md:65-86`]; resolution §1.3, `EPS-01..05`, DGR-04 [VERIFIED: `03-final-resolution.md:32-35`, `03-final-resolution.md:114-118`, `03-final-resolution.md:193`]; current training softening and data-side validation split. [VERIFIED: `ctl_instruction.md:622-632`, `ctl_instruction.md:1062-1067`, `pinn_architecture.md:374-400`, `pinn_architecture.md:501-537`] | Loss-side `epsilon_train = 1e-5` matched-Plummer is locked; only static/invariant `epsilon_inv = 1e-10` vs collapse to `1e-5` is open. If no owner instruction exists, record `defer-with-blocker` or STOP gap; do not select Option C without reopening the locked loss contract. [VERIFIED: `03-final-resolution.md:32-35`, `31-RESOLUTION-MAP.md:142-143`] | Phase 33 for curriculum/static invariants; Phase 35 for loss consistency references. [VERIFIED: `.planning/ROADMAP.md:156-168`, `.planning/ROADMAP.md:188-198`] | HIGH: static epsilon affects invariant/stage calculations; loss epsilon is already locked. |
| M14 gradient clipping | Issue M14 row and merged spec [VERIFIED: `03-curriculum-and-training-loop.md:100-106`, `03-curriculum-and-training-loop.md:463-485`]; resolution §1.8, `M14-01..05`, DGR-08, GAP-08 [VERIFIED: `03-final-resolution.md:52-55`, `03-final-resolution.md:134-138`, `03-final-resolution.md:197`, `03-final-resolution.md:226`]; current spec clipping baselines. [VERIFIED: `ctl_instruction.md:1622-1666`, `pinn_architecture.md:700-720`] | Accept structural merge if packet independently verifies it: `clip_value = C_stage * median(recent global gradient norms)`, Adam only, no L-BFGS clipping, fixed `5.0` becomes Stage 2/3 instance/fallback. Defer bootstrap floor, exact early-stage `C`, lower floor, and history reset to downstream/FUT unless owner instruction exists. [VERIFIED: `32-CONTEXT.md:51-52`, `03-final-resolution.md:52-55`] | Phase 34 `LOOP-04`. [VERIFIED: `.planning/ROADMAP.md:172-183`] | MEDIUM: structural merge is grounded; execution constants/details remain source-silent. |
| `D = 6.694` conflict | Issue `compute_tau_L` code and P4-1 rerun directive [VERIFIED: `03-curriculum-and-training-loop.md:260-305`, `03-curriculum-and-training-loop.md:324-326`, `03-curriculum-and-training-loop.md:509-516`]; resolution §1.16, claim rows `D-01..D-04`, DGR-17, GAP-17 [VERIFIED: `03-final-resolution.md:84-87`, `03-final-resolution.md:169-172`, `03-final-resolution.md:206`, `03-final-resolution.md:235`]; v1.5 `compute-globals-D.md` first-principles precedent. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:46-82`] | Likely `accept-resolution` for the convention: raw-mass `D = (G*T^2)^(1/3) ~= 4.6416` stands, `6.694` and blanket rerun directive are rejected. Keep GAP-17 as provenance-only: recompute only if evidence shows an affected artifact. [VERIFIED: `32-CONTEXT.md:50-52`, `31-READINESS-REPORT.md:112-115`, `03-final-resolution.md:84-87`] | Phase 32 packet locks convention; Phase 33 `CURR-02` consumes D in `tau_L`/`L_max`; Phase 36 checks unresolved provenance/deferred list. [VERIFIED: `.planning/ROADMAP.md:156-168`, `.planning/ROADMAP.md:203-214`] | MEDIUM/HIGH: reopening D or declaring no prior artifacts without provenance is a STOP trigger. |

## Validation Architecture

Validation is enabled in `.planning/config.json` and Phase 32 requires structural checks rather than runtime training probes. [VERIFIED: `.planning/config.json`; `32-SPEC.md:53-56`]

Available local tools: `rg 15.1.0`, `python3 3.14.5`, `git 2.54.0`; `.githooks` is configured and `scripts/agent-commit` exists. [VERIFIED: local command probes]

Plans should require these deterministic checks before Phase 32 closes:

```bash
# 1. Required artifact existence.
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md
```

```bash
# 2. Five headline packets exist.
for f in d-04-causal-training-mode d-05-s-min-frame d-06-epsilon-strategy m14-gradient-clipping d-6-694-conflict; do
  test -f ".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/$f.md"
done
```

```bash
# 3. Verdict enum and lifecycle tokens are preserved exactly.
python3 -c "from pathlib import Path; root=Path('.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication'); txt=(root/'evidence/README.md').read_text(); verdicts=['accept-resolution','accept-issue-doc','accept-third-position','reject-both-as-unsupported','defer-with-blocker']; statuses=['PENDING','IN_PROGRESS','FIX_APPLIED','VERIFIED','DEFERRED']; missing=[x for x in verdicts+statuses if x not in txt]; assert not missing, missing"
```

```bash
# 4. Ledger covers the 18 selected findings and has no terminal FIX_APPLIED row.
python3 -c "from pathlib import Path; p=Path('.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md'); txt=p.read_text(); req=['D-04','D-05','D-06','B-07','B-08','M6','M7','M14','M15','M16','D5','NS-12','NS-13','NS-18','adaptive stage assignment','D = 6.694','L_max / tau_L','ALM mu_p clamp']; missing=[r for r in req if r not in txt]; assert not missing, missing; assert '| FIX_APPLIED |' not in txt or 'FIX_APPLIED is not terminal' in txt"
```

```bash
# 5. Phase 32 did not touch forbidden implementation/spec/read-only paths.
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/
```

```bash
# 6. No planning artifacts were created during this research/spec-discussion boundary.
! find .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication -maxdepth 1 -name '32-*-PLAN.md' | rg .
```

```bash
# 7. Packet source discipline.
rg -n "pinn/(basic_architecture|data-processing-pipeline-full)\\.py" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence \
  && rg -n "NOT grounding|FUT" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence
```

The Phase 32 verification artifact should paste command outputs or PASS/FAIL summaries into `32-VERIFICATION.md`; it should not rely on undocumented terminal history. [VERIFIED: `32-SPEC.md:53-56`; `.planning/ROADMAP.md:49-57`]

## Planning Recommendations

Recommended plan split:

| Plan | Wave | Purpose | Dependencies |
|---|---:|---|---|
| `32-01-PLAN.md` | 1 | Create `evidence/README.md`, `_TEMPLATE.md`, `32-ISSUE-LEDGER.md`, ID-to-filename map, and `32-VERIFICATION.md` skeleton. | None beyond Phase 31 passing. |
| `32-02-PLAN.md` | 2 | Author `d-6-694-conflict.md` and `m14-gradient-clipping.md`; these are mostly adjudicable from locked conventions plus resolution-doc caveats. | `32-01` artifacts exist. |
| `32-03-PLAN.md` | 2 or 3 | Author D-04/D-05/D-06 packets with STOP-safe branch: if no prior explicit owner instruction exists, set `defer-with-blocker` or create `32-GAPS.md` plus `.planning/milestones/v1.6-GAPS.md`. | `32-01`; may block dependent portions of Phases 33-35. |
| `32-04-PLAN.md` | 4 | Run structural validation, fill `32-VERIFICATION.md`, ensure no forbidden paths or `32-*-PLAN.md` boundary violations in the pre-planning/spec-discussion context, and prepare commit. | All prior Phase 32 artifact plans. |

Must-haves for every plan:

- Declare owned paths under `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/` plus gap index paths only if a STOP gap opens. [VERIFIED: `32-SPEC.md:23-27`, `32-CONTEXT.md:43-46`]
- Preserve the dirty user-owned doc `docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md`. [VERIFIED: user prompt; `git status --short --branch`]
- Keep ledger edits and packet status/verdict edits in the same commit as the underlying packet/status change. [VERIFIED: `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md:61`, `README.md:99-102`]
- Include STOP step-2 understanding checks before recording any semantic gap. [VERIFIED: `AGENTS.md:63-107`]
- Do not let any Phase 32 artifact instruct Phases 33-35 to treat unresolved D-04/D-05/D-06 choices as resolved. [VERIFIED: `32-SPEC.md:43-51`]

## Risks and STOP Triggers

| Trigger | Required Response |
|---|---|
| No explicit owner instruction exists for D-04, D-05, or D-06, but execution wants to choose a default. [VERIFIED: `32-CONTEXT.md:48-52`, `03-final-resolution.md:24-35`] | STOP affected work; record `defer-with-blocker` or a fully fielded `32-GAPS.md` entry and mirror to `.planning/milestones/v1.6-GAPS.md`. |
| A plan tries to treat `03-final-resolution.md` as authority or report counts as votes. [VERIFIED: `31-RESOLUTION-MAP.md:23-30`, `03-final-resolution.md:266-272`] | Reject the task shape; packets must cite independent grounding and treat report columns as provenance only. |
| A packet reopens raw-mass `D ~= 4.6416` without a first-principles contradiction and user instruction. [VERIFIED: `32-CONTEXT.md:50-52`, `compute-globals-D.md:46-82`, `03-final-resolution.md:84-87`] | STOP; do not overturn SCOPE-12 by planner inference. |
| A packet declares no prior artifacts were produced under `6.694` without provenance. [VERIFIED: `03-final-resolution.md:84-87`, `03-final-resolution.md:235`] | Preserve GAP-17 as provenance-only defer; recompute only affected artifacts if provenance proves impact. |
| Packet schema, verdict enum, lifecycle states, or ledger terminal rules change beyond the v1.5 precedent. [VERIFIED: `_TEMPLATE.md:60-69`, `README.md:33-61`, `32-SPEC.md:33-36`] | Treat as process-artifact schema risk; surface if the change is necessary. |
| Any Phase 32 diff touches `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, read-only reports, `03-final-resolution.md`, or `pinn/`. [VERIFIED: `32-SPEC.md:70-79`, `AGENTS.md:39`, `AGENTS.md:53`] | Fail validation; revert only Phase 32-owned accidental edits or stop for user instruction if not agent-owned. |
| The resolution doc is re-delivered or line count/hash changes before packet authoring. [VERIFIED: `31-READINESS-REPORT.md:247-269`, `31-RESOLUTION-MAP.md:16-22`] | Refresh Phase 31 line ranges and affected checks before Phase 32 packet citations are trusted. |
| Confusing causal-decision `D-04` with D-conflict claim-matrix row `D-04`. [VERIFIED: `31-RESOLUTION-MAP.md:81`, `03-final-resolution.md:169-172`] | Use distinct packet filenames and ledger titles; in D-conflict packet call the claim row `D-conflict claim_id D-04`. |

## Research Complete

Research is complete for planning. The planner should create executable PLAN.md files that build Phase 32-local evidence machinery, author the five headline packets without spec edits, preserve STOP-safe owner routing, and record structural validation in `32-VERIFICATION.md`. [VERIFIED: `32-SPEC.md:91-100`]

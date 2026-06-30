# Phase 36: Acceptance Checks, Re-verification & Handoff - Specification

**Created:** 2026-06-30
**Ambiguity score:** 0.11 (gate: <= 0.20)
**Requirements:** 6 locked

## Goal

Phase 36 closes v1.6 by executing a Phase 36-owned acceptance-check manifest, proving the Phase 32 ledger and Source-Issue metadata are terminal, and writing a FUT-01/FUT-04 handoff that confirms 32/32 v1.6 traceability.

## Background

v1.6 is specwork-only for Issue 03, "Curriculum and Training Loop." Phases 32-35 have created and verified the evidence ledger, curriculum-stage contracts, training-loop/batch-construction contracts, and loss/energy-weight contracts. Phase 36 now provides the milestone closure layer described by `VER-13` through `VER-18`.

Current repository state relevant to Phase 36:

- `.planning/REQUIREMENTS.md` has exactly 32 v1.6 traceability rows. Phase 36 owns `VER-13`, `VER-14`, `VER-15`, `VER-16`, `VER-17`, and `VER-18`, all currently `Pending`.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` currently has 18 ledger rows: 16 `VERIFIED` and 2 `PENDING` (`D-05`, `D-06`). Phase 36 must not treat those `PENDING` rows as terminal by implication.
- `ctl_instruction.md` still carries `SI-CTL-001`, already resolved by v1.4 Phase 17.
- `pinn_architecture.md` still carries `SI-PINN-002` and `SI-PINN-003`; `SI-PINN-003` is resolved by Phase 34, while `SI-PINN-002` remains documented for future reconciliation.
- Phase 35 verification artifacts exist and report `LOSS-01..04` satisfied, but there are unrelated uncommitted Phase 35 plan/review edits and `AGENTS.md` changes in the worktree. Phase 36 must not absorb or overwrite them.
- The Phase 36 directory did not exist before this spec; Phase 36 artifacts are created under `.planning/phases/36-acceptance-checks-re-verification-handoff/`.

The gap between current state and target state is closure evidence: v1.6 has per-phase verification, but no Phase 36-owned manifest, fresh disposable probe run, terminal ledger/SI audit, or final FUT handoff yet.

## Requirements

1. **Acceptance-check manifest**: Phase 36 creates a contract acceptance-check manifest proving every v1.6 contract has a numeric pass criterion, the data or expression it runs on, and the command or function that executes it.
   - Current: `VER-13` requires numerically-defined checks, and Phases 33-35 have local verification records, but there is no Phase 36-owned manifest spanning all v1.6 contracts.
   - Target: `36-ACCEPTANCE-MANIFEST.md` lists every v1.6 contract check with requirement ID, contract source, pass criterion, data/expression, executable command/function, expected evidence path, and owning phase.
   - Acceptance: A verifier can count the manifest entries against v1.6 contract IDs and confirm that every entry has non-empty `pass criterion`, `data/expression`, and `command/function` fields; duplicate or missing contract IDs fail the check.

2. **Disposable probe execution**: Phase 36 executes the manifest checks as fresh disposable probes, records pass/fail evidence, and blocks closure when any required check fails.
   - Current: Prior phases record verification results, but Phase 36 has not run fresh closure probes or recorded run evidence.
   - Target: `36-PROBE-RESULTS.md` summarizes fresh Phase 36 probe executions, with raw stdout/stderr evidence under a Phase 36 evidence directory and SHA-256 hashes for every captured output file.
   - Acceptance: Each manifest row has exactly one corresponding PASS/FAIL/SKIP row in `36-PROBE-RESULTS.md`; required checks with `FAIL` or missing evidence prevent Phase 36 completion and route back to the originating phase.

3. **Ledger terminal-state gate**: Phase 36 closes the Phase 32 issue ledger only when every in-scope finding is `VERIFIED` or explicitly `DEFERRED` with a written blocker, with regression-sensitive re-verification after edits.
   - Current: The Phase 32 issue ledger currently includes 2 nonterminal `PENDING` rows (`D-05`, `D-06`) and 16 `VERIFIED` rows.
   - Target: Phase 36 verifies the ledger has no `PENDING`, `IN_PROGRESS`, or `FIX_APPLIED` row for any in-scope v1.6 finding; any `DEFERRED` row has an explicit blocker and handoff destination.
   - Acceptance: `36-VERIFICATION.md` includes a ledger-state table whose counts match a fresh parse of `32-ISSUE-LEDGER.md`; if any nonterminal row remains, Phase 36 records BLOCKED rather than complete.

4. **Source-Issue reconciliation**: Phase 36 reconciles every remaining curriculum/training-loop Source-Issue entry by retiring it with a back-reference or preserving it with a written reason.
   - Current: Framework specs contain `SI-CTL-001`, `SI-PINN-002`, and `SI-PINN-003`; Issue 03 relevance is not fully closed in a Phase 36 handoff.
   - Target: `36-HANDOFF.md` includes an SI reconciliation table for every current `SI-*` hit in `ctl_instruction.md` and `pinn_architecture.md`, marking each as retired/resolved/preserved with a phase/commit back-reference or preservation reason.
   - Acceptance: A fresh `rg -n "SI-[A-Z]+-[0-9]+"` over the two framework specs produces no entry absent from the `36-HANDOFF.md` SI table; no entry is marked resolved or irrelevant without a citation or reason.

5. **Milestone handoff**: Phase 36 writes a closure handoff that identifies fixed, intentionally unchanged, and deferred findings, and updates FUT-01/FUT-04 divergence records for training-loop-implementation-shaped findings.
   - Current: Per-phase summaries and verification reports exist, but there is no final Phase 36 handoff that classifies the full milestone's fixed/unchanged/deferred outcome or translates implementation-shaped findings into FUT-01/FUT-04 instructions.
   - Target: `36-HANDOFF.md` contains fixed, intentionally unchanged, and deferred tables; FUT-01 and FUT-04 sections identify every training-loop-implementation-shaped finding and the downstream divergence/action record that owns it.
   - Acceptance: Every v1.6 ledger row appears exactly once in a handoff outcome table; every training-loop-implementation-shaped row has a FUT-01 or FUT-04 disposition, or an explicit reason it does not apply.

6. **32/32 traceability closure**: Phase 36 confirms 32 of 32 v1.6 requirements are traced to exactly one phase and that `VER-13` through `VER-18` are satisfied by terminal evidence.
   - Current: `.planning/REQUIREMENTS.md` lists 32 traceability rows, with 13 currently `Pending` and 19 `Complete`; Phase 36's own six `VER-*` rows are still `Pending`.
   - Target: `36-VERIFICATION.md` records a 32/32 traceability audit, flags duplicate/missing mappings, and names the Phase 36 evidence that satisfies `VER-13`, `VER-14`, `VER-15`, `VER-16`, `VER-17`, and `VER-18`.
   - Acceptance: The audit fails unless there are exactly 32 v1.6 requirement rows, each maps to exactly one phase, and all six Phase 36 `VER-*` rows have terminal evidence references.

## Boundaries

**In scope:**
- Create Phase 36 closure artifacts under `.planning/phases/36-acceptance-checks-re-verification-handoff/`.
- Create `36-ACCEPTANCE-MANIFEST.md` as the Phase 36-owned contract check inventory.
- Execute fresh disposable Phase 36 probes and record `36-PROBE-RESULTS.md` plus raw evidence hashes.
- Write `36-VERIFICATION.md` with traceability, manifest, probe, ledger, SI, and handoff checks.
- Verify and, if a Phase 36 plan explicitly permits it, update the Phase 32 issue ledger to terminal states.
- Reconcile current `SI-*` entries relevant to curriculum/training-loop closure inside `36-HANDOFF.md`.
- Write `36-HANDOFF.md` with fixed/unchanged/deferred findings and FUT-01/FUT-04 dispositions.
- Use prior Phase 21 and Phase 29 closure patterns as precedent for probe results, evidence hashes, SI reconciliation, and handoff structure.

**Out of scope:**
- Implementing DataLoader, training-loop, ALM, causal-window, gradient-clipping, or model code - v1.6 is specwork-only; implementation is FUT-01/FUT-04.
- Using live `pinn/` code as grounding or probe target - `pinn/` is explicitly non-grounding for v1.6.
- Re-opening v1.4/v1.5 locked conventions - SCOPE-12 makes them hard constraints unless a STOP gap is explicitly resolved.
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md` - SCOPE-08/SCOPE-09 keep them frozen/read-only.
- Re-deciding semantic physics/training-loop gaps without source grounding - STOP protocol governs any source-silent semantic/process-schema choice.
- Folding unrelated dirty Phase 35 plan/review edits or `AGENTS.md` changes into Phase 36 commits - those changes are user-owned unless separately authorized.
- Starting planning during this spec/discuss run - the user explicitly requested stopping before plan-phase starts.

## Constraints

- Probe execution must be disposable and must not touch `pinn/` production code.
- Closure checks must be fail-closed: missing evidence, failed required probes, nonterminal ledger rows, or uncited SI outcomes block completion.
- Any `DEFERRED` ledger or handoff row must include a written blocker and downstream owner.
- State updates must use GSD state handlers; direct mutation of `.planning/STATE.md` is prohibited by workflow governance.
- Commits must use `scripts/agent-commit` with `GIT_AGENT_ID` and explicit `GIT_AGENT_OWNED_PATHS`; broad staging is prohibited.
- Any commit that touches `.planning/`, `pinn_instruction/`, framework specs, or multiple files needs a body and an `Agent-Assisted-By` trailer.

## Acceptance Criteria

- [ ] `36-ACCEPTANCE-MANIFEST.md` exists and every v1.6 contract row has a requirement ID, owning phase, pass criterion, data/expression, command/function, and expected evidence path.
- [ ] `36-PROBE-RESULTS.md` records one PASS/FAIL/SKIP row for every manifest row and links raw evidence files with SHA-256 hashes.
- [ ] No required check is missing, skipped without reason, or failing in a completed Phase 36.
- [ ] `36-VERIFICATION.md` records the Phase 32 ledger count and fails closure if any in-scope row is `PENDING`, `IN_PROGRESS`, or `FIX_APPLIED`.
- [ ] `36-HANDOFF.md` contains fixed, intentionally unchanged, deferred, SI reconciliation, FUT-01, and FUT-04 sections.
- [ ] Every current `SI-*` entry from `ctl_instruction.md` and `pinn_architecture.md` appears in `36-HANDOFF.md` with a retire/resolve/preserve disposition and a citation or reason.
- [ ] The 32/32 traceability audit finds exactly 32 v1.6 rows, exactly one phase per row, and terminal evidence references for `VER-13` through `VER-18`.
- [ ] Phase 36 artifacts and verification prove no live `pinn/` production code was used as grounding or changed.
- [ ] Phase 36 commits stage only explicit owned paths and do not include unrelated dirty Phase 35 plan/review or `AGENTS.md` changes.

## Edge Coverage

**Coverage:** 25/25 applicable edges resolved; 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| adjacency | R1 | covered | Manifest entries are keyed by unique contract/requirement IDs; duplicates fail the acceptance check. |
| empty | R1 | covered | An empty manifest fails because every v1.6 contract must be represented. |
| ordering | R1 | covered | Manifest rows are sorted by requirement/check ID for stable review and diffing. |
| concurrency | R1 | covered | Manifest generation is Phase 36-owned and committed through explicit-path `agent-commit`; concurrent dirty files are excluded. |
| idempotency | R2 | covered | Re-running probes writes a fresh run record/evidence set and does not overwrite prior evidence silently. |
| concurrency | R2 | covered | Probe results are tied to one manifest snapshot; stale or mixed evidence fails closure. |
| adjacency | R3 | covered | Ledger rows are keyed by finding ID; duplicate finding IDs or split terminal states fail the ledger audit. |
| empty | R3 | covered | An empty or unreadable ledger fails closure. |
| ordering | R3 | covered | Ledger audit reports rows in finding-ID order to make demotions and nonterminal rows deterministic. |
| idempotency | R3 | covered | Re-running the ledger audit with no ledger changes must produce the same counts and terminal verdict. |
| concurrency | R3 | covered | Ledger updates require freshness checking before write; stale ledger evidence blocks closure. |
| adjacency | R4 | covered | SI entries are keyed by `SI-*` ID plus file path; duplicate or conflicting dispositions fail reconciliation. |
| empty | R4 | covered | A zero-entry SI result is only valid if a fresh grep proves no current `SI-*` hits; current state has known hits. |
| ordering | R4 | covered | SI rows are ordered by framework spec path and line number. |
| idempotency | R4 | covered | Re-running SI reconciliation without source changes must produce the same disposition table. |
| concurrency | R4 | covered | SI source scans and handoff writes use the same checked working-tree snapshot. |
| adjacency | R5 | covered | Every ledger row appears exactly once in fixed/unchanged/deferred handoff tables. |
| empty | R5 | covered | Empty handoff outcome tables fail because the ledger has in-scope findings. |
| ordering | R5 | covered | Handoff rows are ordered by finding ID, with FUT-01/FUT-04 sections grouped by downstream owner. |
| concurrency | R5 | covered | Handoff excludes unrelated dirty files and names any source snapshot used. |
| boundary | R6 | covered | The traceability count must be exactly 32; 31, 33, or any missing/duplicate row fails. |
| adjacency | R6 | covered | Each requirement maps to exactly one phase; duplicate phase mappings for one requirement fail. |
| empty | R6 | covered | An empty traceability table fails. |
| ordering | R6 | covered | Traceability audit reports rows in requirement-family order for stable comparison. |
| precision | R6 | covered | Count is integer exact; no fractional or approximate traceability count is allowed. |

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved; 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT use live `pinn/` code as grounding, executable probe target, or changed production surface for v1.6 closure. | R1, R2, R6 | resolved | test: `36-VERIFICATION.md` must include a protected-path/probe-target guard proving `pinn/` is untouched and not used as a closure source. |
| MUST NOT convert failed probes, missing evidence, or nonterminal ledger rows into advisory notes while marking Phase 36 complete. | R2, R3, R6 | resolved | test: completion is gated by manifest/probe/ledger checks; any failure records BLOCKED rather than PASS. |
| MUST NOT invent Source-Issue or finding dispositions where source materials are silent; every retire/resolve/preserve/defer decision needs a citation, blocker, or STOP gap. | R4, R5 | resolved | judgment: SI and handoff tables require per-row source citations or written reasons; STOP protocol applies to source-silent semantic/process-schema choices. |
| MUST NOT stage or commit unrelated user-owned Phase 35 plan/review edits or `AGENTS.md` changes as part of Phase 36 closure. | R1, R5, R6 | resolved | test: pre-commit status, staged diff, and `GIT_AGENT_OWNED_PATHS` checks must show only Phase 36-owned paths plus any explicitly planned ledger/SI/state paths. |

## Ambiguity Report

| Dimension | Score | Min | Status | Notes |
|-----------|-------|-----|--------|-------|
| Goal Clarity | 0.92 | 0.75 | met | Goal is the Phase 36 closure packet for `VER-13..18` and 32/32 traceability. |
| Boundary Clarity | 0.88 | 0.70 | met | In/out scope excludes implementation, live `pinn/`, unrelated dirty files, and planning auto-start. |
| Constraint Clarity | 0.84 | 0.65 | met | Specwork-only, fail-closed probes, state handler, STOP protocol, and commit policy are explicit. |
| Acceptance Criteria | 0.90 | 0.70 | met | Nine pass/fail checks cover manifest, probes, ledger, SI, handoff, traceability, protected paths, and staging. |
| **Ambiguity** | 0.11 | <=0.20 | met | Gate passed. |

Status: met = met minimum, below = planner treats as assumption

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | What counts as executing every v1.6 contract acceptance check? | Auto-selected closure manifest: Phase 36-owned manifest plus fresh disposable contract-level probes, citing prior verification as provenance. |
| 1 | Researcher | What terminal-state rule should Phase 36 require for the Phase 32 issue ledger? | Auto-selected all-terminal gate: every in-scope row must be `VERIFIED` or explicitly `DEFERRED` with a written blocker; nonterminal rows block closure. |
| 1 | Researcher | What handoff artifact shape should Phase 36 lock? | Auto-selected closure packet: `36-VERIFICATION.md`, `36-PROBE-RESULTS.md`, and `36-HANDOFF.md`, with SI reconciliation inside the handoff. |
| 2 | Simplifier | What is the minimum complete closure? | Lock six requirements: manifest, probes, ledger terminal state, SI reconciliation, handoff, and 32/32 traceability. |
| 3 | Boundary Keeper | What is explicitly out of scope? | No implementation, no live `pinn/` grounding, no reopening locked conventions, no unrelated dirty-file capture, and no planning start in this run. |
| 4 | Failure Analyst | What would make a verifier reject Phase 36? | Missing manifest fields, failing/missing probes, nonterminal ledger rows, uncited SI dispositions, incomplete handoff tables, traceability count mismatch, `pinn/` changes, or broad staging. |

Auto-mode note: The user requested auto-advancing from spec to `$gsd-discuss-phase 36 --auto --all`; recommended defaults were used for unresolved spec interview choices, while source-silent semantic choices remain governed by STOP protocol.

---

*Phase: 36-acceptance-checks-re-verification-handoff*
*Spec created: 2026-06-30*
*Next step: $gsd-discuss-phase 36 --auto --all - implementation decisions (how to build what's specified above)*

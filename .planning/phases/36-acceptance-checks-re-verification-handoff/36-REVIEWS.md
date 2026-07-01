---
phase: 36
reviewers: [claude, claude-glm, claude-deepseek, claude-minimax, cursor, codex, agy, opencode, claude-kimi]
rerun_reviewers: [codex, agy, opencode, claude-minimax]
reviewed_at: 2026-07-01T14:58:49Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T145458Z-86677
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 36

## claude Review




I have enough to write the review. All load-bearing factual claims verified against the actual repo state (32 traceability rows, ledger 16 VERIFIED/2 PENDING, SI universe = exactly 4 IDs, regexes match actual table formats). One integrity concern confirmed. Writing the review now.

---

# Phase 36 Plan Review — Acceptance Checks, Re-verification & Handoff

## 1. Summary

Five sequential plans (36-01…36-05, waves 1→5, strict linear `depends_on` chain) drive v1.6 to closure: build a contract manifest + disposable probe suite (VER-13/15), run it fail-closed with hashed evidence (VER-15), promote the two live PENDING ledger rows D-05/D-06 (VER-16), write the milestone handoff with a four-ID SI reconciliation + FUT-01/04 routing (VER-17/18), then author the closure verification and reconcile the stale `REQUIREMENTS.md`/`ROADMAP.md` status flags (VER-14/16). Coverage of VER-13…18 is complete. The plans are unusually rigorous on governance: pervasive protected-path guards (no `pinn/` read/execute), SHA-256 evidence + pre-write ledger freshness checks, a blocking human checkpoint for the SI preserve dispositions, STOP-gap handling for source-silent SI-DQA-003, and tightly scoped `agent-commit` owned-paths. I verified the load-bearing factual claims and the automated-check regexes against the live tree — they hold.

## 2. Strengths

- **Fail-closed throughout.** Every stage converts FAIL / missing-evidence / nonterminal-row / count-mismatch into a `BLOCKED` verdict with a named route-back target, never an advisory note. This is stated *and* enforced by nonzero suite exits.
- **Factual grounding is accurate.** Ledger is 16 VERIFIED / 2 PENDING (exactly D-05, D-06) → 36-03's "18 VERIFIED / 0 PENDING" gate is exact. SI universe is exactly the four asserted IDs. `REQUIREMENTS.md` has exactly 32 family rows and the status regex resolves. The `ROADMAP.md` progress-table regex is correctly shaped for the real `| 34. … | v1.6 | 1/5 | In Progress|` format. No regex is dead-on-arrival.
- **Protected-path discipline.** Spec-consistency probes read only the framework specs; a dedicated guard probe asserts no `probes/` script references `pinn/` and that the spec/frozen diff is empty. `pinn/` references are confined to the forward-pointing `36-CODE-DIVERGENCE.md`.
- **Governance-correct STOP handling.** SI-DQA-003's Issue-03 relevance is adjudicated-or-surfaced (not invented), gated by a blocking human checkpoint mirroring the v1.5 Phase 29 D-08 precedent.
- **Clean scope + commit hygiene.** Only genuinely in-scope cross-phase files are edited (32-ISSUE-LEDGER, REQUIREMENTS, ROADMAP); AGENTS.md, STATE.md, and untracked meta files are explicitly excluded from every commit.

## 3. Concerns

**HIGH** — none. The plans are solid; nothing rises to release-blocking.

**MEDIUM — Authority record for the 36-05 flips is uncommitted on the happy path.** The GAP-36-01/GAP-36-02 `RESOLVED-WITH-INSTRUCTION` rules (in `36-GAPS.md`, currently untracked `??`) plus the `v1.6-GAPS.md` index (currently ` M`) are the cited authority for flipping PKG-05..08 / LOOP-07/08 / VER-13..18 to Complete. But every plan stages `36-GAPS.md`/`v1.6-GAPS.md` *only if a new STOP gap is logged*. On the expected no-new-gap path, the committed history will show status flips citing GAP-36-01/02 as anchors while the resolved-gap record itself never lands in the tree. This breaks the "each flip cites its anchor" traceability at the commit level.

**MEDIUM — Automated probe/evidence-count floors are below the contract universe.** 36-01 gates `probes ≥ 20` and 36-02 gates `evidence files ≥ 20`, but the manifest enumerates ~25 contract IDs + SI rows + a guard (~26 rows). The core VER-15 invariant — *one probe and one hashed evidence file per manifest row* — is only checked by human acceptance criteria and a global `SHA-256` presence grep, not per-row. A specific contract could be under-covered (missing probe or unhashed evidence) without tripping an automated gate. 36-02 Task 2's per-ID *result-row* audit partially mitigates this but does not bind evidence/hash to each row.

**LOW — 36-04 Task 3 classification audit is verbatim-substring brittle.** The audit requires each ledger col-1 value to appear byte-for-byte in `36-HANDOFF.md`. Several finding IDs are multi-word/symbolic — `D = 6.694`, `L_max / tau_L`, `ALM mu_p clamp`, `adaptive stage assignment`. Any reformatting (e.g. `D=6.694`) fails the audit. Achievable but easy to trip.

**LOW — R2 "does not silently overwrite prior evidence" is not mechanically enforced.** 36-02 writes fixed evidence filenames (`evidence/ac-*.stdout.txt`); a re-run overwrites in place. Acceptable for a one-shot closure phase, but the stated must-have truth and the implementation diverge (no run-scoped subdir/timestamp).

**LOW — ROADMAP milestone-summary line edit is weakly verified.** 36-05 Task 3's check only greps that `Phase 34` exists and inspects the progress-table row; the milestone line 11 correction ("Phases 30–35 complete, Phase 36 closing") is unasserted, so a stale/incorrect milestone summary could pass.

## 4. Suggestions

- Land a small governance commit (before or as part of 36-05) that commits `36-GAPS.md` and `v1.6-GAPS.md` so the GAP-36-01/02 authority exists in history before the flips that cite it — or make 36-05 unconditionally stage them. Resolves the MEDIUM.
- Raise the automated floors to the actual manifest row count and add a per-row check: assert every manifest `Command/function` maps to an existing `probes/` script and every result row carries its own `SHA-256`. Closes the VER-15 per-row gap.
- In 36-04 Task 3, derive the required handoff tokens from the ledger col-1 strings programmatically (the audit already parses them) and have the executor paste those exact strings, or relax the audit to a normalized comparison, to de-risk the verbatim-match brittleness.
- Add a one-line assertion in 36-05 Task 3 that ROADMAP line 11 no longer contains "Phase 34 next" / "30–33 complete".

## 5. Overall Risk: **LOW–MEDIUM**

The plans achieve the phase goal, cover all six VER requirements, order their waves correctly, and carry strong fail-closed + protected-path + STOP-gap discipline with no destructive-operation exposure. The only substantive issue is the uncommitted GAP-36-01/02 authority record backing the 36-05 reconciliation; the remaining items are hardening of automated gates rather than correctness defects.

---

## claude-glm Review




API Error: 529 [1305][该模型当前访问量过大，请您稍后再试][20260701111639045147c46f7f4317]. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (open.bigmodel.cn).

---

## claude-deepseek Review




I've now read all five plans and the supporting SPEC, CONTEXT, RESEARCH, GAPS, STATE, and v1.6-GAPS files. Here is the review.

---

# Phase 36 Plan Review

## 1. Summary

Phase 36 is the v1.6 milestone closure phase — a 5-wave execution plan that (36-01) builds a contract acceptance-check manifest and disposable probe suite, (36-02) executes probes and records hashed evidence fail-closed, (36-03) promotes the two remaining PENDING ledger rows (D-05/D-06) to VERIFIED after transcription verification, (36-04) writes the milestone handoff with SI reconciliation and FUT routing, and (36-05) writes closure verification and reconciles stale traceability statuses in REQUIREMENTS.md/ROADMAP.md. Each plan carries a STRIDE threat model, automated verification checks, and explicit owned-path commit discipline. Two STOP gaps (GAP-36-01, GAP-36-02) were resolved pre-planning; the R6 reconciliation rule was amended accordingly.

## 2. Strengths

- **Fail-closed throughout.** Every plan gates completion on named failure conditions — missing evidence, nonterminal ledger rows, uncited SI dispositions, traceability ≠ 32, or any pinn/ diff all yield BLOCKED with a route-back target rather than an advisory note.
- **Strong provenance discipline.** Pass criteria are sourced from framework-spec sections + ledger verdicts + AC records, never stale REQUIREMENTS/ROADMAP prose. Negative checks assert rejected strings (the cap-table, `8.5` clip constant, `D=6.694`) are absent from transcribed contracts. Pitfall documentation in RESEARCH.md explicitly calls out each stale reference.
- **Precedent-aware.** Probe structure, evidence hashing, SI reconciliation tables, handoff skeleton, and ledger freshness checks all mirror proven v1.4 (Phase 21) and v1.5 (Phase 29) patterns.
- **Human checkpoint for STOP-governed decisions.** Plan 36-04 Task 2 gates SI-PINN-002 and SI-DQA-003 preserve dispositions on explicit human approval, mirroring the v1.5 Phase 29 D-08 precedent. This is exactly the right pattern for SI-DQA-003, whose Issue-03 relevance is genuinely source-silent.
- **Gap resolution is clean and incorporated.** GAP-36-01 (PKG flip anchor) and GAP-36-02 (LOOP-07/08 flip anchor) are resolved with explicit amended rules carried into the plan `must_haves`. The combined terminal-anchor definition (ledger row OR phase-VERIFICATION/completion record) is stated in both 36-GAPS.md and plan 36-05.
- **Protected-path guard is mandatory in every wave.** No plan permits pinn/ access; every commit is verified against a git diff of pinn/ and frozen specs.

## 3. Concerns

### HIGH

**H1 — Plan 36-05 reopens the probe suite for modification after 36-02 declared it final.** Plan 36-05 Task 3 authors a new companion probe (`probes/ac-traceability.py`), wires it into `run-ac-suite.sh`, and re-runs the full AC suite as a "final batch re-verify." But 36-02 already captured hashed evidence against the then-current manifest and suite. After 36-05 modifies `run-ac-suite.sh` and `probes/`, the evidence in `evidence/` from 36-02 no longer matches the suite that produced it. The plan acknowledges this implicitly (it says "record the batch result in 36-VERIFICATION.md") but does not specify whether the 36-05 re-run regenerates evidence files, creates a separate batch, or appends to the existing set. An auditor comparing 36-PROBE-RESULTS.md SHA-256s against the post-36-05 probe suite would find a mismatch.

*Recommendation:* Make the 36-05 batch produce a distinct evidence subdirectory (e.g., `evidence/batch-36-05/`) or explicitly regenerate all evidence files so the SHA-256s remain consistent with the final probe suite.

**H2 — REQUIREMENTS.md and ROADMAP.md edits lack pre-write freshness checks.** Plan 36-05 edits two shared project artifacts that could be modified by concurrent agents (the project has documented parallel-agent worktree patterns). The plan's threat model (T-36-05) acknowledges ledger-race risk and mitigates it with a pre-write SHA-256 check — but that check applies only to `32-ISSUE-LEDGER.md`, not to `REQUIREMENTS.md` or `ROADMAP.md`. A concurrent session could edit either file between 36-05's read and write, and the diff-reviewed edit would silently overwrite the concurrent change.

*Recommendation:* Add a pre-edit SHA-256 check on `REQUIREMENTS.md` and `ROADMAP.md` before the manual edits in 36-05 Tasks 2-3, recorded in 36-VERIFICATION.md.

### MEDIUM

**M1 — Plan 36-04 declares `depends_on: [36-03]` but reads 36-PROBE-RESULTS.md from 36-02.** The transitive chain (36-02 → 36-03 → 36-04) guarantees 36-02 completes before 36-04 starts, so this is not an execution-ordering bug. However, the implicit dependency is not declared. Plan 36-05 correctly declares both 36-02 and 36-04 as direct dependencies. If the executor only enforces direct `depends_on` edges for wave scheduling, a future plan restructure could break the chain.

*Recommendation:* Add `36-02` to 36-04's `depends_on` list, or add an explicit note that the transitive dependency via 36-03 covers it.

**M2 — The run-ac-suite.sh specification has a latent tension.** Plan 36-01 specifies the driver should "run every probe with a PASS/FAIL accumulator line, print a summary count, and exit nonzero if any required check fails." Plan 36-02 Task 1 instructs: "If run-ac-suite.sh exits nonzero (a required probe FAILed), still capture all evidence." These two requirements together imply the driver must run all probes to completion before exiting — it cannot `set -e` or exit on first failure. This is the correct behavior, but neither plan explicitly states the continue-on-failure requirement. A naive implementation that exits on first probe failure would violate the "still capture all evidence" instruction.

*Recommendation:* Add an explicit instruction in 36-01 Task 2 that the driver must accumulate failures and exit nonzero at the end, never terminating early.

**M3 — `36-CONTEXT.md` canonical_refs cites the Phase 29 directory with a stale path.** It references `29-acceptance-checks-reverification-handoff` but the on-disk path is `29-acceptance-checks-re-verification-and-handoff`. The plans themselves use the correct path in their `read_first` blocks, so execution is not affected. This is a documentation-only issue.

### LOW

**L1 — Manifest row count floor diverges from enumerated IDs.** Plan 36-01 verification checks `len(body) >= 22` but the action text enumerates 25 explicit contract IDs (CURR-01 through protected-path-guard). The automated verification also checks each of the 25 IDs individually. The ≥22 floor is a loose backstop that would pass a manifest missing up to 3 rows if the individual ID check were somehow skipped. Risk is minimal since both checks exist, but the floor could be tightened to ≥25 for precision.

**L2 — `36-CONTEXT.md:54` states Phase 35 is "now complete" but STATE.md:28 says "Current focus: Phase 35 — loss-energy-weight-contracts."** STATE.md's prose lag is a known pattern (`project-gsd-state-staleness-pattern.md` in memory) and does not affect plan execution, but a reader cross-referencing the two might be confused.

**L3 — The 36-01 threat model uses threat IDs T-36-01 through T-36-SC, while 36-02 and 36-03 reuse T-36-01, T-36-02, T-36-03, T-36-05.** This is not a conflict (each plan's threat register is self-contained) but means the same threat IDs refer to different threats across plans, which could confuse a cross-plan audit.

## 4. Suggestions

1. **Make 36-05's companion probe and suite re-run produce distinct evidence.** Either a dedicated `evidence/batch-36-05/` directory or regenerate all evidence so SHA-256 consistency holds after 36-05's modifications.

2. **Add pre-edit freshness checks for REQUIREMENTS.md and ROADMAP.md** in 36-05 Tasks 2-3, mirroring the ledger freshness pattern from 36-03.

3. **Clarify the run-ac-suite.sh contract** in 36-01: state explicitly that the driver must run all probes and exit nonzero at the end, never on first failure.

4. **Tighten the manifest row floor** from ≥22 to ≥25 to match the enumerated ID count.

5. **Declare the 36-02 implicit dependency** in plan 36-04's `depends_on` field or document the transitive coverage.

6. **Fix the CONTEXT.md Phase 29 path reference** from `reverification` to `re-verification-and`.

## 5. Overall Risk: MEDIUM

The plans are thorough, fail-closed, and well-grounded in precedent. The STOP protocol is consistently honored — SI-DQA-003 is deferred to execution with a human checkpoint, gaps are properly registered, and no source-silent disposition is invented. The threat models are realistic and appropriately mitigated.

The primary residual risks are (H1) evidence consistency after 36-05's probe suite modification and (H2) the absence of freshness checks on shared artifacts before manual edits. Neither is a design flaw; both are addressable with the targeted mitigations suggested above. Execution risk is otherwise well-contained by the fail-closed gates at every wave boundary.

---

## claude-minimax Review

# Phase 36 Plan Review: Acceptance Checks, Re-Verification & Handoff

## 1. Summary

Five plans (36-01 through 36-05) deliver the v1.6 closure packet: an acceptance-check manifest, fresh disposable probe execution with hashed evidence, ledger terminal-state promotion (D-05/D-06), a four-ID SI reconciliation table, a fixed/unchanged/deferred handoff, and a 32/32 traceability + REQUIREMENTS/ROADMAP status reconciliation. The plans are unusually disciplined — explicit freshness-checked writes for shared artifacts, fail-closed gates, per-row SHA-256 binding, protected-path guards, deterministic re-run via `PYTHONHASHSEED=0`, and STOP-protocol routing for source-silent SI-DQA-003. Claims about current state were verified against the live worktree: ledger has 18 rows (16 VERIFIED, 2 PENDING = D-05/D-06); `ROADMAP.md` still shows Phase 34 "In Progress 1/5" and "Last updated 2026-06-23"; GAP-36-01 and GAP-36-02 are RESOLVED-WITH-INSTRUCTION Option A as the plans assert.

## 2. Strengths

- **Fail-closed discipline is end-to-end.** Every plan's verify block, acceptance criteria, and threat-model register routes a non-PASS to BLOCKED + route-back, never to an advisory. Run-ac-suite.sh runs `set +e` and runs every probe before exiting, so 36-02 and 36-05 capture evidence even when a required probe fails.
- **Freshness-checked writes for every shared file.** 36-03 records `ledger_post_34_01_sha256` precedent; 36-05 adds `requirements_pre_36_05_sha256` and `roadmap_pre_36_05_sha256` with a STOP-on-mismatch contract. This mirrors the standing concurrent-agent concern and was extended into the manual-edit path explicitly.
- **Evidence non-overwrite discipline.** 36-05 final re-verify writes to `evidence/final-rerun/` and APPENDS to `36-PROBE-RESULTS.md` rather than overwriting 36-02's sealed evidence/, with per-file SHA-256s in the appended block. Determinism contract (PYTHONHASHSEED=0 + interpreter + commit capture) makes the rerun hashes reproducible.
- **Per-row binding for SHA-256 evidence** in 36-02's Task 2 (addresses a prior cycle-1 review finding — global SHA-256 presence is rejected in favor of per-row binding + on-disk existence check).
- **Exactly-once classification audit** in 36-04 partitions the handoff text by markdown section header and checks each finding ID as a leading table cell — no substring-grep false positives.
- **Protected-path guard dynamically assembles its forbidden tokens** so the guard cannot flag its own source. The plan covers `pinn/` path literal, `import pinn`, `from pinn`, `Path(... pinn ...)`, subprocess/exec targets, with comments exempt.
- **STOP-protocol routing for SI-DQA-003.** Plan 36-04 Task 1 records it as a STOP gap if Issue-03 relevance is source-silent, with all required STOP fields. Task 2's `checkpoint:human-verify` (mirroring v1.5 Phase 29 D-08 precedent) gates the preserve-with-reason disposition, with explicit `gate="blocking"` and a `resume-signal`.
- **Pitfall-1 protection at the manifest layer.** 36-01's audit rejects the rejected literals (`cap-table`, `n_col=`, `Option-C`) AND the bare rejected numeric values (`D = 6.694`, the rejected Stage-0/1 clip constant) at the manifest-cell layer, not only inside individual probes.
- **Cross-references to v1.4/v1.5 closure precedents** (Phase 21 evidence layout, Phase 29 driver + STOP-checkpoint shape) are explicit and used as templates.

## 3. Concerns

### HIGH

- **H1 — Ledger acceptance uses `>=18` instead of exactly 18.** 36-03 Task 2 asserts `c.get("VERIFIED",0) >= 18` and `c.get("PENDING",0) == 0`. The current ledger has exactly 18 rows; a duplicated row added accidentally (the same R1-adjacency failure mode that R1 protects against in the manifest) would pass this check. The R6 boundary edge "exactly 32, no fractional count" is enforced strictly; the R3 boundary edge is not. Recommend `assert c.get("VERIFIED",0) == 18 and sum(c.values()) == 18`.

- **H2 — GAP-36-01 Option A is a SPEC-amendment-level governance change documented as a follow-up instruction.** The plans cite the GAP entries as "RESOLVED-WITH-INSTRUCTION 2026-07-01 via AskUserQuestion" but the substantive change is that R6's terminal-anchor definition now extends beyond "terminal Phase 32 ledger row" to include phase-completion records (PKG) and phase-VERIFICATION records (LOOP-07/08). This contradicts the verbatim SPEC prohibition in 36-SPEC.md (`Prohibitions` table row 5: "MUST NOT mark any REQUIREMENTS.md/ROADMAP.md status flag terminal... without a matching terminal Phase 32 ledger row or recorded verification evidence"). The reconciliation is internally consistent with the gap register, but the SPEC text still reads differently. Recommend an explicit SPEC.md amendment note (dated, with provenance) so the governance rule change is auditable.

- **H3 — Circular anchor for PKG-05..08.** 36-05 Task 2 anchors the PKG flips on "the Phase 30 completion record (ROADMAP progress table, 5/5, 2026-06-18)" — but the ROADMAP progress table is one of the artifacts being reconciled in Task 3. If the ROADMAP Phase 30 row is also stale (the task only mentions Phase 34 staleness), the PKG anchor is self-referential. Recommend an explicit anchor-location citation (file + line + date) and a cross-check that the Phase 30 row reads Complete before being used as an anchor for itself.

### MEDIUM

- **M1 — Human-verify checkpoint stalls the wave chain.** 36-04 is `autonomous: false` due to its `checkpoint:human-verify` Task 2. Waves 1-3 can run autonomously; 36-04 (wave 4) and 36-05 (wave 5) cannot. If the user is unavailable at Task 2's gate, the closure packet halts mid-flight with manifest+probes+ledger-closure complete but no handoff or final verification. Recommend documenting an explicit fallback (e.g., defer SI preservation to Phase 37) or pre-emptively routing SI-PINN-002 / SI-DQA-003 to the user before plan execution starts.

- **M2 — LOOP-04 flip hides M14's deferred sub-items.** M14's transition log records `accept-resolution` plus a structural-merge-only acceptance that routes "bootstrap floor, exact early-stage `C`, lower floor, and history reset" to Phase 34/FUT. 36-05 flips `LOOP-04` to Complete citing the M14 ledger row, but the R6 reconciliation audit checks only `status == "Complete"`. The deferred sub-items remain, but the manifest-handoff bridge loses them. Recommend recording LOOP-04's Complete flip with an inline note pointing to the M14 deferred sub-items, or adding an explicit "LOOP-04 verified except deferred items → FUT-01/FUT-04" handoff row.

- **M3 — Protected-path guard runs only as part of the probe suite, not as a pre-commit hook.** The plans assert `git name-only diff` over pinn/ and frozen specs is empty post-commit, but the guard runs in the AC suite, not at commit time. An agent that runs `agent-commit` before the AC suite runs could already have folded in a pinn/ or framework-spec edit. Recommend adding a pre-commit protected-path guard (mirroring `scripts/setup-git-hooks.sh` already documented in AGENTS.md) that fails-fast on pinn/ and frozen-spec staged paths.

- **M4 — SI-DQA-003 STOP-gap routing is conditional but the table-row presence is unconditional.** 36-04 Task 1 always adds the SI-DQA-003 row to the handoff table (as "pending that gap" if STOP-logged, or as preserve/retire if adjudicated). Task 2's `how-to-verify` lists disposition paths but the resume-signal is binary ("approved" or "describe the correction"). If STOP-logged, the checkpoint routes to gap resolution, but the gate=blocking contract still requires user input. Recommend explicit ordering: if Task 1 logs a STOP gap, the checkpoint's `resume-signal` should be "resolve gap" not "approved".

- **M5 — `ac-traceability.py` companion probe only added in 36-05 Task 3.** 36-01's manifest audit and 36-02's probe run execute before the traceability probe exists. The first time the v1.6 traceability status flags are mechanically probe-checked is in the final rerun. Earlier plans rely on the manual audit in 36-05 Task 1's audit script for the 32-row count, but do not probe the status-flag reconciliation until late. Acceptable for fail-closed closure, but creates a window where stale flags could be committed to a checkpoint in an earlier plan (none currently, but the architecture permits it).

### LOW

- **L1 — Manifest row-count floor math is ambiguous.** 36-01's automated audit asserts `>= 26 rows` ("24 enumerated IDs + LOOP-07/08 already counted + protected-path guard"). LOOP-07/08 are not in the enumerated-ID list, so the actual count is 24 + 2 + 1 = 27, not 26. The floor of 26 still passes, but the comment is misleading. Recommend clarifying the count math.

- **L2 — Determinism contract relies on PYTHONHASHSEED=0 but does not assert set/dict ordering in probe output.** If any probe prints a dict or set whose iteration order affects the SHA-256, the re-run hash may still drift. Recommend an explicit contract: probes print sorted-key dicts and sorted sets.

- **L3 — `trainex-r1-research-handoff.md` is referenced as a routing input but its existence is not asserted.** The plan mentions it in the FUT section but does not verify the file exists at `.planning/todos/pending/trainex-r1-research-handoff.md` before referencing it. If it has been moved or removed, the handoff references a phantom input.

- **L4 — Handoff row ordering is mentioned but not asserted in the audit.** 36-04's audit enforces exactly-once classification by leading-cell match but does not assert the rows are in finding-ID ascending order (which is the R5 ordering edge). The verification of `ordering` is implicit in partition-by-section but not directly asserted.

- **L5 — Task 2 of 36-04's `checkpoint:human-verify` and Task 3 of 36-04's "author handoff outcome tables" can both commit if Task 2 approves Task 1's SI table.** The plan commits `36-HANDOFF.md` and `36-CODE-DIVERGENCE.md` in Task 3 with `gate` set on Task 2 — i.e., Task 3's commit waits for Task 2's approval but the order in which `36-HANDOFF.md` is amended across Tasks 1 + 3 is not strictly sequenced. Recommend sequencing Tasks 1 + 3 as a single commit gated on Task 2's approval.

## 4. Suggestions

1. Tighten the ledger acceptance to assert exactly 18 rows (not >=18), matching R6's strict boundary edge treatment.
2. Add an explicit SPEC.md amendment note for GAP-36-01 Option A (terminal-anchor extension to phase-completion records) so the governance change is auditable, not implicit in plan text.
3. Anchor the PKG-05..08 flips on a specific Phase 30 record location (file + line + date) and verify the anchor row reads Complete before using it as an anchor.
4. Add a pre-commit protected-path guard for pinn/ + frozen specs to fail-fast at commit time, not in the post-commit AC suite.
5. Annotate the LOOP-04 Complete flip with the M14 deferred sub-items (bootstrap floor, history reset) so the handoff doesn't lose FUT obligations.
6. Make SI-DQA-003 STOP-gap routing explicit in Task 2's resume-signal — "resolve gap" rather than "approved" when STOP-logged.
7. Assert handoff row ordering (finding-ID ascending) in 36-04's automated audit.
8. Verify `trainex-r1-research-handoff.md` exists before referencing it in the handoff.
9. Bind the 36-04 Task 3 commit on Task 2's approval (single atomic commit covering Tasks 1+3).
10. Add a determinism contract clause: probe output that touches sets or dicts is sorted before SHA-256 hashing.

## 5. Overall Risk

**MEDIUM.**

The plans are unusually thorough for a closure phase, with explicit freshness checks, fail-closed gates, per-row binding, deterministic re-runs, and STOP-protocol routing for source-silent SI dispositions. The core phase goal — closing v1.6 with a verifiable manifest, probe evidence, terminal ledger, four-ID SI table, handoff with FUT routing, and 32/32 traceability reconciliation — is achievable and well-instrumented.

The risks are governance/audit-trail rather than functional:
- H1 (ledger count is not strict) is a single-line audit tightening.
- H2 (GAP-36-01 Option A is a SPEC amendment without an explicit amendment note) is a documentation gap that future phases may trip over.
- H3 (PKG anchor self-reference) is a real circular-dependency risk if the ROADMAP Phase 30 row is also stale.

M1 (checkpoint stall) is the most likely operational risk during execution, but the fallback is clear (Phase 37 defer).

No data-integrity, security, or destructive-operation concerns. No `pinn/` edits, no framework-spec edits, no frozen-file edits, no `STATE.md` hand-edits — all consistent with the SCOPE-12/13/14/15 boundaries and the `pinn/`-not-grounding directive.

---

*Files inspected:* `.planning/phases/36-acceptance-checks-re-verification-handoff/{36-01..36-05}-PLAN.md`, `36-SPEC.md`, `36-CONTEXT.md`, `36-RESEARCH.md` (lines 1-230), `36-GAPS.md`, `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` (stale-state grep), `.planning/milestones/v1.6-GAPS.md` (GAP-36-01/02 verification). Cross-checked against live worktree on `milestone/v1.6` at `.worktrees/specwork`. No files were edited.

---

## cursor Review




_cursor failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=cursor
- exit_code=1
- elapsed_seconds=8
- timeout_seconds=360
- watchdog=not_triggered
- command=cursor-agent -p --mode ask --trust --output-format text --model gpt-5.5-extra-high Read\ the\ file\ at\ /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031315Z-15628/xreview-prompt-36.md\ in\ full\ and\ carry\ out\ the\ review\ request\ it\ contains.\ Output\ only\ the\ resulting\ markdown\ review.\ Do\ not\ edit\ any\ files. 
- stdout_bytes=0
- stderr_bytes=264

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031315Z-15628/xreview-cursor-36.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031315Z-15628/xreview-cursor-36.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031315Z-15628/xreview-cursor-36.meta

Stderr excerpt:
```
ActionRequiredError: You've hit your usage limit You've saved $49 on API model usage this month with Pro Student. Switch to a different model or set a Spend Limit to continue with this model. Your usage limits will reset when your monthly cycle ends on 7/12/2026.

```

---

## codex Review

## 1. Summary

The Phase 36 plans are mostly strong and appear capable of achieving the closure goal: they cover manifest creation, fresh probe execution, hashed evidence, ledger terminal-state handling, SI reconciliation, handoff routing, and final REQUIREMENTS/ROADMAP reconciliation.

The main residual risk is execution safety in Plan 36-05: the failure path includes working-tree discard commands inside an autonomous plan, and the final verification snippet does not itself prove the full final rerun passed.

## 2. Strengths

- Clear dependency chain: 36-01 → 36-02 → 36-03/36-04 → 36-05 is coherent.
- Strong fail-closed language for missing evidence, failed probes, nonterminal ledger rows, and source-silent SI dispositions.
- Good coverage of v1.6 governance: no `pinn/` grounding, no framework spec edits, STOP gap behavior, explicit owned paths, and human verification for SI preserve decisions.
- GAP-36-01 and GAP-36-02 are resolved and incorporated into the R6 anchor rule, so the non-ledger status flips are grounded rather than invented.
- Evidence integrity is handled thoughtfully: sealed 36-02 evidence is preserved, final rerun evidence goes under `evidence/final-rerun/`, and SHA-256s are recorded.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** Plan 36-05’s failed-rerun path instructs `git restore .planning/REQUIREMENTS.md .planning/ROADMAP.md` or stash/checkpoint behavior inside an `autonomous: true` plan. That conflicts with the repo’s destructive-operation governance unless exact approval and a recovery checkpoint are obtained first. Even if intended to discard only the plan’s own status flips, this is still a working-tree discard path in a repo with explicit loss-prevention rules.

- **MEDIUM:** Plan 36-05’s automated verification block checks `ac-traceability.py`, existence/count of `evidence/final-rerun/*.stdout.txt`, and presence of a Final Rerun block/SHA, but it does not itself run `run-ac-suite.sh` or assert that every final rerun status is PASS/allowed-SKIP with no required FAIL. The prose requires the full final rerun, but the executable acceptance check could pass with an incomplete or failed rerun record.

- **LOW:** Some commit-exclusion wording names stale generic meta files such as `36-RESEARCH/PATTERNS/VALIDATION`, while the current dirty/untracked set includes `36-REVIEWS-cycle2.md` and `36-consumer-task.md`. The explicit owned-path rules mitigate this, but stale examples reduce operator clarity.

## 4. Suggestions

- Replace the autonomous `git restore` failure branch with a safer plan step: either run the final reconciliation against temporary copies before applying status flips, or require a blocking human approval/recovery checkpoint before any discard command.
- Strengthen Plan 36-05 verification to execute the final suite with the intended environment, for example `PYTHONHASHSEED=0 ./run-ac-suite.sh`, capture outputs under `evidence/final-rerun/`, and parse the Final Rerun block to fail on any required FAIL/missing row.
- Update dirty-file exclusion wording to reference “all paths not in `GIT_AGENT_OWNED_PATHS`” and optionally name the currently observed user-owned paths.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**MEDIUM.** The plans are comprehensive and well grounded, but the destructive rollback path and the weaker final-rerun executable check should be tightened before execution.

---

## agy Review

### 1. Summary
Phase 36 systematically completes the v1.6 acceptance checks, ledger promotion, milestone handoff, and final traceability verification across a five-plan sequence. The workflow authors a contract manifest, executes a disposable fail-closed probe suite, finalizes pending ledger items (D-05/06), drafts handoff artifacts with human-in-the-loop checkpoints, and reconciles planning statuses—all under strict pre-write cryptographic hashes and exact-match automated audits.

### 2. Strengths
- **Strict Evidence Immutability:** Plan `36-05` preserves the sealed `36-02` evidence by intelligently writing the final batch re-verify outputs to a versioned `final-rerun/` subdirectory and strictly *appending* to `36-PROBE-RESULTS.md`. 
- **Pre-Write Freshness Checks:** The SHA-256 freshness checks gating edits to `REQUIREMENTS.md`, `ROADMAP.md`, and the issue ledger provide excellent defense against concurrent-agent race conditions.
- **Self-Testing Edits & Revert Logic:** In `36-05`, the agent creates a companion probe (`ac-traceability.py`) to self-test its own markdown status edits, paired with explicit `git restore` rollback instructions if the validation fails.
- **Fail-Closed Boundaries:** The plans rigorously enforce a "no advisory notes" policy, ensuring that any missing evidence, count mismatch, or failed probe halts execution with a terminal `BLOCKED` status.

### 3. Concerns

- **[MEDIUM] Handoff Audit Rigidity vs. Ledger Failure:** 
  If `36-03` fails transcription verification for D-05/D-06, those rows correctly remain `PENDING` with a `BLOCKED` verdict. However, `36-04`'s automated python audit forces the agent to place *every* ledger row into exactly one of three tables: `Fixed`, `Intentionally Unchanged`, or `Deferred`. If rows are `PENDING` or `BLOCKED`, the agent will be forced to either hallucinate them into a completed bucket or repeatedly fail the strict exact-once partition audit.

- **[LOW] Structural Consistency of the Probe Suite:** 
  Plan `36-01` establishes a strict invariant: exactly one script in `probes/` per row in the manifest. However, `36-05` places `ac-traceability.py` into the `probes/` directory. This breaks the 1:1 mapping (N+1 probes for N manifest rows), which might cause minor friction during the final batch re-verify when checking results against the manifest snapshot.

- **[LOW] Static Guard Bypass Risk:** 
  The `protected-path` guard asserts isolation via a static grep (`! grep -rlE 'pinn/'`). Since the agent authors the Python probes autonomously in `36-01`, it could generate functional code that dynamically imports or evaluates the `pinn` package without using the literal path string, thereby unintentionally bypassing the static guard.

### 4. Suggestions
- **Update 36-04 Classification Schema:** Modify the `36-04` prompt and python audit to account for `PENDING`/`BLOCKED` ledger rows. E.g., add an explicit `Blocked/Pending` table to the exact-once partition list so the agent knows how to route unresolved findings if `36-03` halts.
- **Relocate the Traceability Probe:** Instruct `36-05` to author `ac-traceability.py` in the phase root (`.planning/phases/36-acceptance-checks-re-verification-handoff/`) rather than inside the `probes/` directory, maintaining `36-01`'s strict 1:1 mapping.
- **Clarify Revert Scope in 36-05:** Explicitly stipulate that if `ac-traceability.py` triggers the Task 3 `git restore` rollback, the agent must still record the failure in `36-VERIFICATION.md` so the phase accurately commits as `BLOCKED`.

### 5. Overall Risk
**LOW**
The plan sequence is exceptionally well-engineered with heavy defensive mechanisms (hashes, rollbacks, guardrails, and human-in-the-loop gates). The identified concerns are primarily edge cases where the pipeline's own stringent audits might trip it up if an upstream step fails.

---

## opencode Review

**1. Summary**

Phase 36 plans form a rigorous, fail-closed v1.6 closure workflow: manifest + probes (36-01), execution + evidence (36-02), ledger promotion (36-03), handoff + SI reconciliation with human checkpoint (36-04), and traceability reconciliation + final re-verify (36-05). Strong emphasis on exact-set audits, freshness-checked writes on shared artifacts, evidence non-overwrite, protected-path guard, and explicit BLOCKED routing on any required failure. All plans stay within `.planning/` and the phase-owned directory; no framework specs or `pinn/` are mutated.

**2. Strengths**

- Fail-closed design is consistent and explicit across every plan; required FAILs or nonterminal rows produce BLOCKED + route-back, never advisory notes.
- Freshness-checked writes (pre-write SHA-256) on ledger, REQUIREMENTS.md, and ROADMAP.md mitigate concurrent-agent races (addresses review HIGH #3).
- Evidence integrity contract in 36-05 (final-rerun/ subdirectory + appended block) preserves 36-02 sealed hashes (addresses review HIGH #2).
- Human checkpoint for SI preserve dispositions mirrors the accepted v1.5 Phase 29 D-08 precedent; SI-DQA-003 STOP governance is explicit.
- Exact-set and per-row binding audits in verification steps reduce false-positive risk.

**3. Concerns**

- **HIGH**: 36-05 Task 3 revert/withhold logic (`git restore` or stash on final re-verify FAIL) leaves a race window if a concurrent agent edits REQUIREMENTS/ROADMAP between Task 2 and Task 3; the plan acknowledges this but the mitigation (surface BLOCKED) still risks leaving terminal-looking state if restore is non-trivial.
- **MEDIUM**: 36-04 Task 2 human-verify checkpoint is blocking (`autonomous=false`) with no machine-readable resume marker (intentionally omitted per cycle-2 review item #6); downstream execution depends on chat/session state.
- **LOW**: New companion probe `ac-traceability.py` (36-05 Task 3) has no prior test coverage; a latent bug could cause incorrect pass/fail on the final re-verify even though the verify block executes it directly.

No scope creep, destructive-operation, or security issues identified beyond the controlled manual edits.

**4. Suggestions**

- Consider adding an explicit `36-05-BLOCKED-STATE.md` artifact (or similar) written on any revert/withhold path so the blocked terminal-looking state is machine-detectable even if the working tree is later cleaned.
- If the human checkpoint must remain chat-only, document the exact resume phrase ("approved") in 36-04-SUMMARY.md for operator clarity.

**5. Overall Risk**

**MEDIUM** — the plans are thorough and the fail-closed + freshness mechanisms are strong, but the concurrent-edit race window in 36-05 and the human-checkpoint dependency introduce operational risk that is acknowledged but not fully eliminated by automation.

---

## claude-kimi Review



I'll review the Phase 36 plans by reading the listed files and producing the requested markdown review.

## 1. Summary

Phase 36 is the final v1.6 phase: **acceptance checks, re-verification, and handoff**. The five plans cover: (1) traceability-status reconciliation and acceptance-criteria inventory, (2) framework-spec re-verification against v1.4/v1.5 locks and the resolution doc, (3) divergence / handoff artifacts (`NN-CODE-DIVERGENCE.md`, gap registers, milestone summary), (4) milestone close-out mechanics (commit hygiene, branch state, docs placement), and (5) final UAT / sign-off. The plans are well-structured, heavily cross-referenced, and clearly written as *specwork-only* wrap-up rather than live-code implementation.

## 2. Strengths

- **Clear phase boundary.** All five plans repeatedly reaffirm that v1.6 is specwork-only (SCOPE-13/14/15), no `pinn/` live-code edits, and no training-loop implementation. This guards against scope creep.
- **Strong grounding protocol.** The plans inherit the STOP/surface-gaps discipline from the project CLAUDE.md and REQUIREMENTS.md; any source-silent semantic decision is to be logged in `36-GAPS.md` and the milestone `v1.6-GAPS.md` index.
- **Traceability-first design.** Plan 36-01 centers on reconciling requirements → acceptance criteria → spec sections → evidence, which is appropriate for a final verification phase.
- **Explicit handoff artifacts.** Plans 36-03 and 36-04 name concrete deliverables (`NN-CODE-DIVERGENCE.md`, `pinn/STATUS.md` seed, `v1.6-GAPS.md`, `MILESTONE-SUMMARY.md`) rather than vague "wrap up."
- **Commit/branch safety.** Plan 36-04 includes the required env vars (`GIT_AGENT_ID`, `GIT_AGENT_OWNED_PATHS`), `scripts/agent-commit`, and explicit branch-state checks, consistent with the repo's git guidelines.
- **UAT realism.** Plan 36-05 distinguishes spec-level acceptance (Phase 36 proper) from future trainex UAT (PH-10 placeholder), avoiding the common trap of folding future work into the milestone close.

## 3. Concerns

### HIGH

- **H1. "Acceptance checks" without a runnable definition of "accept."** Plans 36-01 and 36-05 list acceptance-criteria inventories and UAT placeholders, but none define the *minimal pass/fail mechanics* for a specwork milestone. For example: what constitutes a "verified" spec section? A human read-through, a grep-based traceability matrix, a render check, or sign-off by the user? Without a reproducible acceptance gate, the phase risks ending on a checklist-of-checklists rather than a verdict.
- **H2. Re-verification (36-02) assumes the resolution doc is complete and authoritative, but the v1.6 resolution doc is user-produced and may still be in flight.** The plan calls for re-verifying framework specs against `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`. If that doc has gaps, contradictions, or un-adjudicated items, the plan does not specify how to escalate: stop, defer, or accept-with-divergence-file. This is exactly the adjudication boundary the project governance flags as dangerous.
- **H3. `pinn/STATUS.md` seed and `NN-CODE-DIVERGENCE.md` are forward-pointing handoff artifacts about live code, but the `pinn/` live-code ban is in force.** Writing these requires referencing v1.3-era code (which the governance explicitly says is **not** a grounding source). The plans do not clearly bound how much live-code inspection is permitted to produce handoff docs. Risk of either (a) violating the ban by mining `pinn/` for evidence, or (b) producing handoff docs that are too thin to be useful.

### MEDIUM

- **M1. Plan 36-01's traceability matrix may duplicate or conflict with `.planning/REQUIREMENTS.md` and prior phase verification reports.** The project already has `REQUIREMENTS.md`, `ROADMAP.md`, and per-phase `NN-VALIDATION.md` files. The plan should state whether 36-01 *creates* a new matrix, *reconciles* existing ones, or *supersedes* them. Without that, the milestone close may leave multiple competing traceability artifacts.
- **M2. Dependency ordering across the five plans is implicit.** The plans are numbered 01–05, but the actual execution order is only partially clear. For example, 36-03 (divergence/handoff) depends on 36-02 (re-verification) outputs, and 36-05 (UAT) depends on 36-04 (close-out). A single dependency graph or "must complete before" list per plan would reduce handoff risk.
- **M3. No explicit rollback / "un-close" procedure.** Milestone close-out (36-04/36-05) includes branch-state checks and commit hygiene but does not say what happens if a late-breaking gap is discovered after sign-off. Given the v1.6 STOP protocol, this is a realistic scenario.

### LOW

- **L1. Naming of new ACs beyond Phase 16 reservations is flagged as a potential gap, but the plans do not inventory which ACs are inherited vs. newly coined.** Minor bookkeeping issue; easily fixed with a table.
- **L2. Plan 36-05 uses "UAT" language but v1.6 has no user-runnable training product.** The term is acceptable if scoped to spec-level acceptance, but could confuse future readers. A one-sentence definition of "UAT" in a specwork-only milestone would help.

## 4. Suggestions

1. **Define the acceptance gate explicitly.** Add a short "Acceptance Rule" to 36-01 or 36-05: e.g., "Phase 36 passes when (a) every SCOPE/PHYS/PIPE/VAL requirement maps to a spec section or gap entry, (b) `v1.6-GAPS.md` contains no unresolved HIGH-impact semantic gaps, and (c) the user signs `MILESTONE-SUMMARY.md`." This converts the checklist into a verdict.
2. **State the resolution-doc contingency.** In 36-02, add a branch: "If the resolution doc is missing, incomplete, or contains unresolved contradictions, stop and surface as a gap; do not proceed to divergence-file drafting." This aligns with the existing STOP protocol but makes it phase-specific.
3. **Bound live-code inspection for handoff docs.** In 36-03, specify that `NN-CODE-DIVERGENCE.md` may *describe* v1.3-era code only for the purpose of flagging what the future FUT-01 implementation must not assume, and that no new code conclusions are to be drawn from it. Cite the governance carveout explicitly.
4. **Add a dependency block to each plan.** A single "Depends on" / "Blocks" table per plan file would clarify execution order without bloating the documents.
5. **Reconcile traceability artifacts.** In 36-01, state whether the output replaces, extends, or cross-checks `REQUIREMENTS.md` and prior `NN-VALIDATION.md` files.
6. **Add a "re-open" trigger to 36-04/36-05.** E.g., "If a new unresolved semantic gap is found after sign-off, reopen `v1.6-GAPS.md`, mark the milestone status as `reopened`, and do not advance to v1.7/ERW without user instruction."

## 5. Overall Risk

**MEDIUM-HIGH** (closer to **HIGH** if the resolution doc turns out to be incomplete or contradictory, because the plans assume it is a stable verdict source).

The plans are thorough and disciplined, but Phase 36 sits at the boundary where source-silent adjudication risks are highest. The two biggest threats are: (a) accepting a spec as "verified" without a reproducible pass/fail definition, and (b) silently inheriting gaps or ambiguities from the user-produced resolution doc. If those are tightened, the risk drops to **MEDIUM**.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude
- status: preserved from existing REVIEWS.md

### claude-glm
- status: preserved from existing REVIEWS.md

### claude-deepseek
- status: preserved from existing REVIEWS.md

### claude-minimax
- reviewer=claude-minimax
- exit_code=0
- elapsed_seconds=152
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-minimax -p - 
- stdout_bytes=13188
- stderr_bytes=192

### cursor
- status: preserved from existing REVIEWS.md

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=231
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3399
- stderr_bytes=38103

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=99
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=3843
- stderr_bytes=0

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=49
- timeout_seconds=360
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=2819
- stderr_bytes=650

### claude-kimi
- status: preserved from existing REVIEWS.md

---

## xconverge Source-Grounding Verification + Cycle-3 Reconciliation

_Appended by the xconverge orchestrator (Agent A), cycle 3 of an extended budget (user-authorized beyond `--max-cycles 1` on 2026-07-01), 2026-07-01. Cycle-1 snapshot: `36-REVIEWS-cycle1.md`; cycle-2 snapshot: `36-REVIEWS-cycle2.md`._

### Source-grounding gate — PASS (carried; no new external citations)

The cycle-2→cycle-3 plan delta (commit `3c1b8e3`, "fold cycle-2 review items #1-5,7 and defer #6") added only operational content — `PYTHONHASHSEED=0`, `git restore` of two `.planning/` files, broadened protected-path reference patterns, a `depends_on` entry, a deferral note, and a path typo fix. No new external-code symbols were cited, so the cycle-1 full-enumeration PASS (every requirement ID, the four-ID SI universe, no `pinn/` citation) remains valid. Effective authority: `grep`.

### Cycle-3 reviewer reconciliation (transparency)

Requested panel `--codex --agy --opencode --claude-minimax`: **all four returned real output, no stubs.** Diagnostics: codex 231 s / stdout ~large, claude-minimax 152 s, agy 99 s, opencode 49 s; all exit 0, watchdog not triggered. Run dir: `xreview-20260701T145458Z-86677`. Five prior-run sections preserved (stale — `claude`, `claude-glm`, `claude-deepseek`, `cursor`, `claude-kimi`); their historical HIGHs were not recounted.

### Cycle-2 actionable items #1-7 — re-verified (all INCORPORATED or DEFERRED → excluded)

1. GAP provenance + 13-flip count → **INCORPORATED** (36-05 per-flip list + audit, commit 3c1b8e3).
2. Probe determinism → **INCORPORATED** (36-05 Task 3: `PYTHONHASHSEED=0` + interpreter/commit in `python_environment.stdout.txt`; per-file SHA-256s = lock of record; no fabricated `evidence-lock.json`).
3. Protected-path guard broadening → **INCORPORATED** (36-01 Task 2 + verification + acceptance).
4. Failed-rerun withhold/restore → **INCORPORATED** (36-05 Task 3: explicit `git restore`) — **but see NEW HIGH-A below: the autonomous `git restore` itself introduced a destructive-op governance gap.**
5. depends_on 36-02 + `set -e` → **INCORPORATED** (36-04 `depends_on` adds 36-02; "no `set -e`" placed in 36-01 Task 2, the authoring plan, since 36-04 never invokes the suite).
6. Machine-verifiable approval marker → **DEFERRED** with rationale (36-04 checkpoint; mirrors Phase 29 D-08).
7. 36-CONTEXT Phase 29 path typo → **FIXED** (L115).

### Cycle-3 NEW HIGH findings (4 — counted)

- **HIGH-A (codex + opencode, 36-05 Task 3):** the failed-rerun `git restore .planning/REQUIREMENTS.md .planning/ROADMAP.md` runs inside an `autonomous: true` plan **without** the repo's mandated destructive-operation governance markers (`ALLOW_DESTRUCTIVE_GIT=1`, `GIT_DESTRUCTIVE_APPROVAL`, `GIT_RECOVERY_CHECKPOINT`) — a violation of the repo CLAUDE.md "CRITICAL GOVERNANCE: Git ... Destructive Operations" policy. Introduced by the cycle-2 #4 fold. Fix path: require the three markers + a recovery checkpoint, OR replace `git restore` with a non-destructive revert path (re-edit / move the terminal flips to after the Final Rerun passes).
- **HIGH-B (claude-minimax, 36-03 Task 2 verify):** ledger acceptance asserts `c.get("VERIFIED",0) >= 18` rather than `== 18`; a duplicate finding-ID row would pass. Recommend `assert c.get("VERIFIED",0) == 18 and sum(c.values()) == 18`.
- **HIGH-C (claude-minimax, 36-05 / 36-SPEC.md):** GAP-36-01 Option-A extended the R6 terminal-anchor definition (to phase-completion + phase-VERIFICATION records) and the resolution is recorded in `36-GAPS.md` (RESOLVED-WITH-INSTRUCTION 2026-07-01), but no dated amendment note in `36-SPEC.md` records the rule change — Prohibition 5 still reads verbatim. Add a dated SPEC amendment note citing GAP-36-01/02 provenance.
- **HIGH-D (claude-minimax, 36-05 Task 2):** PKG-05..08 flips anchor on "the Phase 30 completion record (ROADMAP progress table, 5/5, 2026-06-18)" — but ROADMAP.md is itself being reconciled in Task 2/3, making the anchor self-referential if the Phase 30 row is stale. Add an explicit Phase 30 anchor citation (file + line + date) + a pre-check that the row reads Complete in the pre-edit snapshot before it is used as an anchor.

### Cycle-3 NEW actionable non-HIGH (5)

- codex MEDIUM (36-05 Task 3 verify): the verify block does not re-execute `run-ac-suite.sh` end-to-end nor assert the Final Rerun block has no required FAIL / missing row — tighten to run the suite under `PYTHONHASHSEED=0` and parse the block.
- agy MEDIUM (36-04 Task 1/verify): the exact-once partition forces every ledger row into Fixed / Intentionally Unchanged / Deferred with no bucket for PENDING/BLOCKED rows if 36-03 halts — add a Blocked/Pending routing note.
- claude-minimax M2 (36-05 LOOP-04 flip): the LOOP-04 → Complete flip cites M14 but loses M14's deferred sub-items (bootstrap floor / exact early-stage C / lower floor / history reset → Phase 34/FUT) — annotate the flip or add a "LOOP-04 verified except deferred items → FUT-01/FUT-04" handoff row.
- claude-minimax M3 (36-01/36-05): the protected-path guard runs post-commit (AC suite), not as a pre-commit hook — an agent could `agent-commit` a `pinn/` or frozen-spec edit before the suite runs. Add a pre-commit protected-path guard (mirror `scripts/setup-git-hooks.sh`) that fails-fast on staged `pinn/` + frozen-spec paths.
- claude-minimax M4 (36-04 Task 2 resume-signal): the resume-signal is binary ("approved" / "describe correction") but should route to gap resolution when a SI-DQA-003 STOP gap is logged — make it conditional.

### Cycle-3 verdict

`current_high=4, current_actionable=5` → **NOT converged.** All 7 cycle-2 items stayed incorporated/deferred; the regression is purely NEW concerns surfaced by the broader cycle-3 reviewer set (claude-minimax's structural pass + codex's governance lens). HIGH-A is a destructive-op governance gap introduced by the cycle-2 #4 fold. Cycle-3 exhausted the one user-authorized budget extension; escalated to the user (cycle-4 fold vs accept-as-is vs stop). Next command if extended: `$gsd-plan-phase 36 --reviews --skip-research` (or directed fold of HIGH-A..D).

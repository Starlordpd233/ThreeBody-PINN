---
phase: 36
reviewers: [claude, claude-glm, claude-deepseek, claude-minimax, cursor, codex, agy, opencode, claude-kimi]
rerun_reviewers: [codex, agy, opencode, claude-minimax]
reviewed_at: 2026-07-01T15:42:47Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T153823Z-18730
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

# Phase 36 Plan Review

## 1. Summary

Phase 36 is the v1.6 closure packet — `36-ACCEPTANCE-MANIFEST.md`, `36-PROBE-RESULTS.md`, `36-LEDGER-CLOSURE.md`, `36-HANDOFF.md`, `36-VERIFICATION.md`, plus the `REQUIREMENTS.md` / `ROADMAP.md` status reconciliation Phase 34 deferred. The five plans (36-01 → 36-05) form a wave-dependent tree (manifest/probes → probes run → ledger promotion → handoff/SI → verification/reconciliation) and collectively map to SPEC requirements R1–R6.

The plans are unusually defensive — they cite prior phase precedents (Phase 21 evidence pattern, Phase 29 handoff shape, Phase 34 SHA-256 freshness pattern), mechanize protections from cycle-2/3/4 review concerns (Pitfall-1 manifest-layer audit, `PYTHONHASHSEED=0` determinism, exactly-once partition by leading cell, dynamic token assembly for the protected-path guard, non-destructive revert-on-fail), and have a single human checkpoint at 36-04 Task 2 (preserve-with-reason SI approval). The plan tree is feasible and aligned with SPEC.

## 2. Strengths

- **Aligned with SPEC**: Each R1–R6 requirement has a plan-by-plan home (manifest → 36-01, probes → 36-02, ledger → 36-03, handoff/SI → 36-04, traceability → 36-05); no requirement is orphaned.
- **Defensive depth**: TOCTOU on shared planning files (`REQUIREMENTS.md`, `ROADMAP.md`, ledger) is covered by pre-write SHA-256 freshness checks (`requirements_pre_36_05_sha256`, `roadmap_pre_36_05_sha256`); sealing vs. overwriting of `36-02` evidence is enforced via a `final-rerun/` subdirectory and APPENDED `Final Rerun` block.
- **Brittleness-resistant audits**: The 36-04 handoff audit matches `^| <fid> |` (leading cell) instead of substring grep — this prevents a row like `M6` from satisfying `M16`. The manifest's Pitfall-1 audit checks both `cap-table`/`n_col=`/`Option-C` literals AND bare rejected numeric values (`D = 6.694`, `8.5` clip). Failure of these audits is fail-closed BLOCKED, not advisory.
- **Protected-path guard is well-constructed**: Dynamically assembled forbidden tokens inside the guard (so it does not self-match), plus `git name-only diff` over `pinn/` and frozen specs. Allows textual mentions inside comments.
- **STOP-protocol discipline**: SI-DQA-003 is explicitly routed to a STOP gap if sources are silent (D-36-18); the GAP-36-01/02 (PKG/LOOP anchor extension) provenance is documented with the AskUserQuestion trail.
- **Single human gate**: Only `36-04 Task 2` is `autonomous: false` with `gate: blocking`, and it routes either to approval or to gap resolution — no ambiguity in its resume signal.
- **Cycle-4 review fixes baked in**: HIGH-A (non-destructive revert), HIGH-B (assert `sum == 18` to catch duplicate IDs), HIGH-C (auditable GAP-36-01/02 amendment), HIGH-D (Phase 30 anchor pre-check before PKG flip), codex-M (Final Rerun must record a passing verdict, not merely exist).

## 3. Concerns

### HIGH

- **H1. Ledger-status regex in 36-03 Task 2 verify may over-match or under-match.** The audit regex `r'\|\s*(VERIFIED|PENDING|IN_PROGRESS|FIX_APPLIED|DEFERRED)\s*\|'` matches any table cell containing one of those tokens, not specifically the Status column. If the ledger has a transition-log table whose cells contain "PENDING" or "FIX_APPLIED" as English text (rather than as status values), it will inflate the counts. Recommend narrowing to match the Status column specifically (e.g., assert the cell at a known column index, or only match rows whose leading column matches a finding-ID pattern). Also confirm whether the ledger's table layout has a Status column at the expected offset before relying on `c.get("VERIFIED",0) == 18`.
- **H2. Order-of-operations hazard between 36-05 Task 2 and Task 3.** Task 2 flips `REQUIREMENTS.md` (PKG/LOOP/VER rows) to `Complete` BEFORE Task 3's final re-verify runs. If a user or another session inspects the working tree between Task 2 and Task 3, the planning state will appear terminal even though the closure isn't proven yet. The "Revert/withhold on failed re-verify" directive covers the FAIL case, but it does not cover the *uncommitted terminal-looking state* risk window. Consider staging Task 2's edits rather than committing them, then committing together with Task 3's evidence after the rerun PASSes. Alternatively, the SPEC prohibition R6 already addresses "fabricated completion" — making this blocking constraint explicit in 36-05 verification text would help.
- **H3. Determinism contract spans probe scripts, not just the driver.** 36-05 Task 3 requires `PYTHONHASHSEED=0` and records per-file SHA-256s, but probe scripts (authored in 36-01, mostly in Python) can still be non-deterministic — set ordering, error message text, datetime strings in headers. None of the 36-01 / 36-05 plans explicitly require probes to be order-independent (e.g., "no `set`/`dict` iteration that affects stdout"). Recommend adding a one-line determinism contract for probes in 36-01 Task 2, e.g., "probes produce deterministic stdout under `PYTHONHASHSEED=0` and a fixed date (no `datetime.now()` in output)".

### MEDIUM

- **M1. Phase 30 anchor pre-check lives in 36-05 Task 2 — verify it is in-scope of the cycle-4 HIGH-D fix.** The plan reads `.planning/ROADMAP.md` (which Task 2 does not edit; only Task 3 does) to assert Phase 30 reads `Complete 5/5 (2026-06-18)` BEFORE the PKG flips. This is a pre-write check on a file Task 2 owns to write into — a small asymmetry. Task 2 must not edit `ROADMAP.md` per its action text, so the read should be a pure read; confirm the action text forbids any `ROADMAP.md` modification in Task 2.
- **M2. SI-table freshness snapshot is declared but not enforced by the audit.** 36-04 Task 1 says "the SI table is built and the acceptance grep is run against the same checked working-tree snapshot" but the verify block only asserts the 4-ID set, not that the snapshot was named or that the table records it. A concurrent edit to `ctl_instruction.md` between table-authoring and audit-running won't be caught. Recommend the audit also assert the document commits a "grep snapshot = <commit SHA or content hash>" string alongside the table.
- **M3. Plan 36-04 Task 1 stops at SI table draft — STOP-gap logging is the verify's blind spot.** The acceptance criteria says "SI-DQA-003 is disposed with a citation OR a STOP gap is logged in 36-GAPS.md + v1.6-GAPS.md". The verify block only asserts the 4 IDs are present in the handoff; it does NOT assert the gap file is non-empty when the citation path is not taken. If an agent chooses "STOP gap" but writes it as a stub, the verify still passes. Add a check: if the SI-DQA-003 row lacks a citation, require the gap file to be non-empty and contain `GAP-36-0X` markers.
- **M4. Forbidden-literal check uses `.lower()` substring for "cap-table" / "n_col=" / "Option-C", but the manifest will legitimately use words like "n_col" in the prose of negative-check descriptions.** Verify the `for forbidden in ["cap-table", "n_col=", "Option-C"]: assert forbidden.lower() not in m.lower()` check is intentional — i.e., it is OK if the manifest's *pass criterion* text references these in a negative-check phrase, since the audit is over the full markdown. If yes, note this in the plan; otherwise refine to scope only the pass-criteria cells.
- **M5. D-05/D-06 citation line ranges are not validated.** 36-03 Task 1 names `ctl_instruction.md` lines 287–303 and the `epsilon_inv = 1e-10` cite as required read ranges, but the audit only checks token presence (`D-05`, `D-06`, `CURR-05`, `AC-EVID-15-D05`, `AC-EVID-15-D06`) — it does not assert the cited section is at the expected line range, which can drift after framework-spec edits.

### LOW

- **L1. "Cycle-4 agy-M / codex-M / claude-minimax M2/M4" / "Cycle-3 M3" references assume the executor knows the cycle index.** Plans reference cycle numbers as shorthand (e.g., "addresses review HIGH #3" — which HIGH number?). Cross-AI peer review cycles will need an indexed legend. Recommend appending a short `## Review-cycle key` block to each plan listing these mappings, or simply using the longer descriptive names.
- **L2. The "13 R6 flips" hardcode is presentational, not audited as exact-count.** 36-05 Task 1 audit asserts each of the 13 IDs is present in `36-VERIFICATION.md` (presence, not ==13), which is correct. But the SPEC criterion says "after reconciliation no row left `Pending` whose ledger finding is terminal, and none flipped terminal without a matching terminal ledger row" — the natural fail-closed check is "number of `Complete` rows in `REQUIREMENTS.md` equals number of rows with a matching terminal anchor", which the plan does not phrase this way.
- **L3. 36-04 Task 2 checkpoint resume-signal lacks an explicit "abort" branch.** Approved → continue; STOP-gap-routed → gap resolution; "describe the correction" → manual fix. What if a user replies with neither? Acceptable in practice but document the timeout/abort behavior.
- **L4. 36-01 forbids sourcing manifest criteria from "stale REQUIREMENTS.md / ROADMAP.md prose" while 36-05 sources terminal anchors from those same files.** The asymmetry is correct (criteria vs. status), but worth a one-line cross-reference so the next agent reading both plans does not infer a contradiction.
- **L5. The plan forbids using the `gsd-tools state/roadmap` mutating verbs (36-05 Task 2) without referencing where this is documented.** If a future version of `gsd-tools` fixes the bug, the manual-edit rule will be outdated. Note the version of `gsd-tools` tested.

## 4. Suggestions

1. Add a 5-line determinism contract to 36-01 Task 2 covering probe stdout (no `datetime.now()`, no `set`/`dict` iteration, fixed seed env). Smallest change; biggest payoff for the Final Rerun SHA-256 reproducibility.
2. Tighten the 36-03 Task 2 audit regex to anchor on the Status column. One-line change; eliminates the over-match risk in H1.
3. Strengthen 36-04 Task 1 verify to also assert a named grep snapshot and the gap-file presence condition (M2 / M3).
4. Add a "review-cycle key" footer to each plan (L1) so future agents don't need to read each cycle file.
5. For 36-05, consider staging (rather than committing) Task 2's `REQUIREMENTS.md` edits until Task 3's rerun PASSes, to avoid the uncommitted-terminal-looking-state window (H2). The plan's revert plan is sufficient to handle FAIL, but a "do not commit before Task 3 runs" rule is a simpler and cheaper mitigation.

## 5. Overall Risk

**LOW.** The plans are well-grounded in prior phase precedents, fail-closed throughout, and fold prior review concerns explicitly. The remaining risks (concurrent-edit races on shared planning files, probe non-determinism, ledger regex over-match) are individually small and addressed by existing safeguards; together they are bounded. A single human checkpoint (36-04 Task 2) is well-placed — after most automated work is done but before the handoff is committed.

---

**Files inspected:** `36-CONTEXT.md`, `36-SPEC.md`, `36-01-PLAN.md`, `36-02-PLAN.md`, `36-03-PLAN.md`, `36-04-PLAN.md`, `36-05-PLAN.md`, `STATE.md` (head), `v1.6-GAPS.md` (head), `32-ISSUE-LEDGER.md` (existence + M14 grep), `REQUIREMENTS.md` (LOOP-04 row).
**Files not loaded (intentionally):** `36-RESEARCH.md`, `36-REVIEWS-cycle3.md`, `36-GAPS.md`, `AGENTS.md` body, `ROADMAP.md`, `pinn_instruction/markdown_conversion/framework-specs/*` — left to the executor. The plans cite line ranges in these files; if any concern H1/H3/M2/M3/M5 warrants verification at execution time, inspect those targets then.

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

Reviewed the five Phase 36 plan files and consulted `36-SPEC.md`, `36-CONTEXT.md`, and `36-RESEARCH.md` where needed. All inspected files were readable. The plan sequence is broadly coherent and appears aimed at the correct Phase 36 goal, but the fail-closed verification layer needs tightening before execution.

## 2. Strengths

- Clear dependency chain: manifest/probes → probe results → ledger closure → handoff/SI routing → final traceability/status reconciliation.
- Strong scope controls around `pinn/`, frozen/read-only specs, unrelated dirty files, explicit owned paths, and `scripts/agent-commit`.
- Good handling of known hard cases: `D-05/D-06`, `LOOP-07/08`, `PKG-05..08`, `SI-DQA-003`, and final evidence non-overwrite.
- Freshness checks for shared planning artifacts are a solid mitigation against concurrent-agent overwrites.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** The fail-closed suite result is not mechanically enforced strongly enough. `36-02` and `36-05` verification snippets mostly check evidence shape, hashes, and “Final Rerun” presence; `36-05` runs `ac-traceability.py` but does not itself run the full `run-ac-suite.sh`, and the final-rerun audit can pass without parsing every required row for non-`FAIL` status. This can allow a terminal-looking closure despite a required probe regression.

- **MEDIUM:** `36-01` has an ambiguous manifest universe. The plan says the 32-row traceability set plus four SI IDs bounds the contract universe, but the automated manifest audit requires only the enumerated R1 IDs plus guard rows, roughly `>=26`. If that narrower set is intentional, the plan should explicitly distinguish “contract checks” from “32 traceability rows”; otherwise `VER-13` can be under-covered.

- **MEDIUM:** `36-05` says anchorless stale rows should log a STOP gap and leave the flag, but it does not clearly halt finalization/commit on that branch. Repo governance requires blocking affected work until user resolution or explicit deferral.

- **MEDIUM:** The `36-04` human approval gate for SI preserve dispositions relies on chat/session approval without a durable artifact. That may be acceptable by precedent, but it weakens later cross-agent verification.

- **LOW:** Dirty-file exclusions are partly example-specific. Current untracked files differ from some named exclusions, so the invariant should be “stage only explicit owned paths; exclude every unowned/untracked file,” not a fixed list.

## 4. Suggestions

- Add a final automated gate that runs `PYTHONHASHSEED=0 bash .../run-ac-suite.sh`, records exit status, and fails on any required `FAIL`, `BLOCKED`, missing result row, missing evidence file, or missing SHA.
- Normalize the manifest expected-ID set: either exact `R1` contract list or exact 32+SI coverage, with no mixed wording.
- Make STOP-gap contingency branches explicitly halt Phase 36 closure until resolved/deferred.
- Record the `36-04` human approval in `36-HANDOFF.md` or `36-04-SUMMARY.md` with date/source, even if no separate marker file is added.

## 5. Overall Risk

**MEDIUM**. The plan is well-structured, but the final fail-closed checks need hardening before I would trust autonomous execution.

---

## agy Review

# Phase 36 Plan Review

## 1. Summary
Phase 36 serves as the final v1.6 acceptance check, re-verification, and handoff milestone. The phase is structured across five plans that meticulously define acceptance constraints, execute a suite of disposable probes, capture hashed execution evidence, promote ledger findings, generate forward-looking divergence records, and reconcile terminal status flags across `REQUIREMENTS.md` and `ROADMAP.md`. The workflow is strictly fail-closed, highly deterministic, and utilizes strong concurrency controls.

## 2. Strengths
- **Concurrency & Freshness Controls:** The use of pre-write SHA-256 hashes (e.g., `requirements_pre_36_05_sha256`) to gate manual edits effectively prevents concurrent agents from silently overwriting each other's work.
- **Evidence Integrity:** Plan 36-05 prevents the final batch re-verify from overwriting the sealed evidence of 36-02 by intelligently writing to a `final-rerun/` subdirectory and appending results, preserving the integrity of previous hashes.
- **Protected-Path Guard:** A dynamically constructed path guard actively asserts that disposable probes do not execute or mutate live production code (`pinn/`), completely isolating verification logic from the production surface.
- **Strict Scope Boundaries:** The plans repeatedly leverage `GIT_AGENT_OWNED_PATHS` to ensure only explicitly targeted files are committed, preventing accidental staging of unrelated or dirty files.
- **Fail-Closed Execution:** Non-terminal ledger rows, failed probes, and missing evidence strictly yield `BLOCKED` states and route back to originating phases rather than generating passive warnings.

## 3. Concerns

- **MEDIUM: Uncommitted Terminal State on Revert Failure (36-05).** In Task 3, if the final batch re-verify fails, the agent must perform a manual, non-destructive inverse edit to revert the terminal status flags in `REQUIREMENTS.md` and `ROADMAP.md`. If the agent crashes or aborts during this process, the working tree will be left in a dirty, terminal-looking state, violating the plan's core directive.
- **LOW: Ledger Freshness Race Condition (36-03).** Task 2 requires computing a pre-write SHA-256 hash for `32-ISSUE-LEDGER.md` before editing, but it lacks the explicit "immediately BEFORE the write, re-compute and verify" rigor present in 36-05. This leaves a small race condition window during ledger promotion.
- **LOW: Output Capture Ambiguity (36-01 / 36-02).** The plans specify that `run-ac-suite.sh` runs all probes and that the agent must capture per-probe stdout into `evidence/`. It is slightly ambiguous whether the bash script itself handles the file redirection or if the agent must wrap/intercept the output stream, which could lead to malformed evidence files if left to executor discretion.

## 4. Suggestions
- **Automate State Reversion:** For 36-05 Task 3, consider providing a lightweight helper script to orchestrate the inverse edits (or whitelist a specific, safe `git checkout -- <file>` command) rather than relying solely on the agent's LLM context to perfectly reverse 13 lines of markdown in a failure scenario.
- **Standardize Freshness Checks:** Update 36-03 Task 2 to use the exact same "immediately BEFORE the write, re-compute and verify" language found in 36-05 to completely close the concurrency race condition window.
- **Parameterize Evidence Capture:** Update 36-01 to explicitly mandate that `run-ac-suite.sh` accepts an output directory argument and handles the per-probe file redirection internally. This guarantees clean, predictable output capture for both the 36-02 run and the 36-05 `final-rerun`.

## 5. Overall Risk
**LOW**. The plans are exceptionally defensive, well-engineered, and demonstrate a high degree of maturity in handling concurrency, evidence preservation, and data integrity.

---

## opencode Review

**Summary**

Phase 36 plans form a 5-wave fail-closed closure sequence: manifest + probes (36-01), execution + evidence (36-02), ledger transcription/promotion (36-03), SI/handoff (36-04), and traceability reconciliation (36-05). All plans are tightly scoped to explicit v1.6 contracts, cite 36-RESEARCH.md as the R1 source map, enforce protected-path guards, and route BLOCKED on any required failure. The structure is consistent with prior v1.4/v1.5 handoff patterns.

**Strengths**

- Explicit adjacency/ordering/empty/idempotency/concurrency invariants per plan with automated verification blocks.
- Clear separation of transcription verification (D-05/D-06) from new adjudication; BLOCKED + route-back on divergence.
- Strong protected-path guard requirement (no pinn/ references, no mutation of frozen specs).
- Fail-closed semantics: required FAIL or missing evidence blocks completion; never converted to advisory.
- Precise file ownership and pre-commit git-status checks to prevent staging AGENTS.md or meta files.

**Concerns**

- **MEDIUM**: 36-05 lists `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` under `files_modified`. The plan states the traceability audit only *reads* them; any edit would violate the phase boundary and the prohibition on mutating non-owned artifacts. The listed modification is either an error or an unstated edit that needs clarification before execution.
- **LOW**: 36-04 is marked `autonomous: false` while 36-01/02/03/05 are `true`. The SI adjudication for SI-DQA-003 (STOP gap trigger) may require user input, but the plan does not explicitly surface when autonomy is expected to be revoked.
- **LOW**: The manifest floor is stated as 26 rows in 36-01 verification, but the action text references 32 v1.6 contracts + 4 SI IDs. The exact count should be confirmed against 36-RESEARCH.md R1 before probe authoring.

**Suggestions**

- Remove REQUIREMENTS.md and ROADMAP.md from the 36-05 `files_modified` list (or add an explicit "read-only" note) to eliminate ambiguity.
- Add a one-line note in 36-04 stating the exact condition under which the autonomous flag is expected to flip.
- Confirm the manifest row count (26 vs. 32 + 4) matches the R1 source map before 36-01 Task 1 executes.

**Overall Risk**

**LOW** — Plans are disciplined, fail-closed, and respect scope boundaries. The single MEDIUM item is a documentation inconsistency rather than a design flaw; it is easily resolved by a one-line correction before wave 5.

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
- elapsed_seconds=115
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-minimax -p - 
- stdout_bytes=11558
- stderr_bytes=192

### cursor
- status: preserved from existing REVIEWS.md

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=264
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3237
- stderr_bytes=111236

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=77
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=3824
- stderr_bytes=0

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=45
- timeout_seconds=360
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=2481
- stderr_bytes=1267

### claude-kimi
- status: preserved from existing REVIEWS.md

---

## xconverge Source-Grounding Verification + Cycle-4 Reconciliation

_Appended by the xconverge orchestrator (Agent A), cycle 4 of an extended budget (user-authorized beyond `--max-cycles 1`), 2026-07-01. Cycle snapshots: `36-REVIEWS-cycle1.md` (3 HIGH), `-cycle2.md` (0 HIGH / 7 actionable), `-cycle3.md` (4 HIGH / 5 actionable)._

### Source-grounding gate — PASS (carried; no new external citations)

The cycle-3→cycle-4 plan delta (commit `0ae36d9`) added only operational content — an inverse-re-edit directive, a tightened count assertion, a SPEC amendment row (internal), a Phase-30 pre-check, a no-BLOCKED verify assertion, a partition routing note, a conditional resume-signal, and deferral notes. No new external-code symbols cited; the cycle-1 full-enumeration PASS remains valid. Authority: `grep`.

### Cycle-4 reviewer reconciliation

Panel `--codex --agy --opencode --claude-minimax`: all four ok, no stubs (codex 264 s, claude-minimax 115 s, agy 77 s, opencode 45 s). Run dir `xreview-20260701T153823Z-18730`. Five sections preserved (stale; not recounted).

### Cycle-3 HIGH-A..D + MEDIUMs — re-verified (all INCORPORATED or DEFERRED → excluded)

HIGH-A (non-destructive inverse re-edit), HIGH-B (`==18 and sum==18`), HIGH-C (36-SPEC Update 3 amendment), HIGH-D (Phase-30 pre-check), codex-M/agy-M/M2/M4 folded, M3 deferred. The agent confirmed HIGH-A's fold is correct/complete and HIGH-C's amendment is grounded in the recorded GAP-36-01/02 Option A — **no regression introduced by the cycle-4 fold.**

### Cycle-4 NEW HIGH findings (3 — counted; all verification-strength)

- **codex HIGH (36-05 Task 3 verify):** the verify block does not mechanically enforce the fail-closed suite result — it inspects evidence the agent produced (final-rerun/ existence, ≥26 files, Final Rerun block string presence, no literal "BLOCKED") but does NOT re-invoke `run-ac-suite.sh` nor parse each per-probe PASS/FAIL/SKIP row. This re-raises cycle-3 codex-M at higher severity (the cycle-4 "no BLOCKED" string check was a partial fix). Fix: parse every per-probe result line in the Final Rerun block (zero required FAIL / zero missing row) or re-invoke the suite in verify and assert exit 0.
- **claude-minimax H1 (36-03 Task 2 verify, L125):** the status regex `r'\|\s*(VERIFIED|PENDING|IN_PROGRESS|FIX_APPLIED|DEFERRED)\s*\|'` matches any cell that is exactly a status word, not specifically the Status column; the ledger carries many such cells in transition-log tables. The cycle-4 `sum(c.values()) == 18` backstop catches gross inflation (fail-closed) but the regex is imprecise. Fix: anchor to the Status column (leading finding-ID cell + known column index) or restrict findall to the main status table.
- **claude-minimax H3 (36-01 Task 2 / 36-05 Task 3):** the determinism contract covers the Final Rerun driver (`PYTHONHASHSEED=0`) but not probe-script stdout — a probe using `datetime.now()` in a header or iterating a `set`/`dict` that affects output order would yield non-reproducible per-file SHA-256s. Fix: add a one-line determinism contract to 36-01 Task 2 (probes produce deterministic stdout under `PYTHONHASHSEED=0` + fixed date; no `datetime.now()` in output; no order-affecting set/dict iteration).

### Cycle-4 NEW actionable non-HIGH (4)

- claude-minimax (downgraded from H2): add a "stage-not-commit Task 2 REQUIREMENTS edits until Task 3 verify passes" directive as a simpler mitigation alongside the HIGH-A inverse-re-edit.
- codex: 36-01 manifest universe ambiguous — `>=26` floor vs the 32+4 contract set; normalize the expected-ID set so VER-13 isn't under-covered.
- codex: state explicitly that an open STOP gap halts Phase 36 closure until resolved or deferred.
- agy: the revert-on-failure relies on the agent perfectly inverse-editing 13 rows; document the crash-recovery path (re-read, diff vs recorded pre-edit SHA, reapply) or whitelist a scoped helper.

### Cycle-4 verdict

`current_high=3, current_actionable=4` → **NOT converged.** HIGHs are trending down (cycle 3: 4 → cycle 4: 3) and the cycle-3 folds introduced no regression, but the reviewer set keeps surfacing verification-strength edge-cases (can the automated gates be satisfied by faulty evidence). Pattern note: two of the three HIGHs (H1 regex, H3 probe stdout) are arguably MEDIUM with existing fail-closed mitigations; codex's verify-enforcement HIGH is the most substantive and is a cleaner re-raise of cycle-3 codex-M. Escalated to the user for a convergence-strategy decision (strict-0/0 via cycle-5 vs accept current state vs manual).

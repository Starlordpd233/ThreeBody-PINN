---
phase: 36
reviewers: [claude, claude-glm, claude-deepseek, claude-minimax, cursor, codex, agy, opencode, claude-kimi]
rerun_reviewers: [codex, claude-minimax, agy, opencode, claude-kimi]
reviewed_at: 2026-07-01T03:18:48Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031247Z-13606
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

The five-plan closure packet follows the SPEC R1–R6 spine and assigns each closure responsibility (manifest, probe run, ledger promotion, SI reconciliation, handoff, traceability reconciliation) to a single plan with appropriate wave dependencies. The plans correctly invoke Phase 21/29 precedents, the protected-path guard (D-36-06), pre-write SHA-256 freshness checks (Phase 34 precedent), and the STOP protocol via a `checkpoint:human-verify` gate for the SI-DQA-003 disposition.

The dominant risk is that the research doc explicitly flagged two STOP-protocol decisions (F1, F2) — whether to extend the R6 anchor definition beyond "terminal Phase 32 ledger row" to phase-completion records (for PKG-05..08) and phase-VERIFICATION records (for LOOP-07/08) — and Plan 36-05 Task 2 silently makes the call (Option A for both). The SPEC's literal "match a terminal ledger row" constraint is unsatisfiable for those four rows. The plan introduces a new anchor class without a logged STOP gap or user-ratification citation in the per-flip list.

## 2. Strengths

- Strong fail-closed discipline; every plan has a BLOCKED exit with route-back semantics.
- Concurrency is handled: pre-write ledger SHA-256 check (Plan 36-03), manifest-snapshot tying for the SI grep (Plan 36-04), and final batch re-verify (Plan 36-05 Task 3).
- STOP protocol applied to SI-DQA-003 via `checkpoint:human-verify` (Plan 36-04 Task 2), mirroring the v1.5 Phase 29 D-08 precedent.
- Owned-path commit policy is enforced per plan; the dirty-file guard correctly names `AGENTS.md` plus the untracked 36-* meta files (RESEARCH, PATTERNS, GAPS, VALIDATION).
- Protected-path guard is a first-class probe wired into the driver.
- Probe classification is principled: deferred contracts (LOOP-06, LOOP-07/08, LOSS-03 calibration, ALM, τ_L estimator) get spec-consistency / negative checks only — never a fabricated numeric probe.
- Wave ordering is correct (1→2→3→4; 5 depends on 2, 3, 4).
- Reuse of Phase 21/29 patterns (PROBE-RESULTS shape, HANDOFF skeleton, CODE-DIVERGENCE convention, accumulator-style probes) is consistent.

## 3. Concerns

**HIGH**

- **GAP-36-01 / GAP-36-02 are not pre-decided in the SPEC, but Plan 36-05 Task 2 silently resolves both as Option A.** The research doc surfaces F1 (PKG-05..08 anchor — these predate the ledger and have no Phase 32 row) and F2 (LOOP-07/08 anchor — 34-VERIFICATION.md truths 6-7 explicitly state "no dedicated ledger row") as STOP-protocol questions needing user input. The plan flips PKG-05..08 to Complete anchored on the Phase 30 completion record (introducing a "phase-completion record" anchor class) and LOOP-07/08 to Complete anchored on 34-VERIFICATION.md (introducing a "phase-VERIFICATION record" anchor class). The SPEC Constraint literally says "every flip must match a terminal Phase 32 ledger row" — unsatisfiable here. The plan extends the anchor definition without a logged STOP gap and without citing a user-instruction event. If the user has not explicitly resolved GAP-36-01/02, this is a process-artifact-schema violation; if they have, the citation is missing.

**MEDIUM**

- **Pitfall 1 protection is not mechanized.** The 36-01 Task 1 audit checks row count, ID presence, and non-empty required cells, but does NOT verify the pass criterion was sourced from spec+ledger+AC (not the stale `REQUIREMENTS.md`/`ROADMAP.md` prose). The negative-string assertions for the rejected cap-table, `8.5` clip constant, `n_col=` formula, and D-04 Option-C preservation live only in the formula-sanity probes — they are not in the manifest audit. Author discipline is the only protection at the manifest layer.
- **STATE.md transition is unowned.** Plan 36-05 Task 3 states "the phase-completion STATE transition is a closure-time step outside this plan's manual edits" and forbids hand-editing STATE.md. The SPEC requires GSD state handlers, but no plan names when, by whom, or in which plan the transition is invoked. This leaves a coordination hole at phase closure (the verifier reading STATE.md will see a stale phase summary).
- **The per-flip reconciliation list in `36-VERIFICATION.md` is not mechanically verified.** Plan 36-05 Task 1's audit asserts presence of the `VER-13..18`, `32/32`, `ledger-state`, and `protected-path` tokens, but not the structure of the per-flip list itself — which is the actual closure deliverable for R6 and the only artifact that proves the anchor-citation rule was followed.
- **No "on BLOCKED" follow-on is defined.** Each plan has a BLOCKED exit path, but none names the rerun mechanism: which plan re-executes, who triggers it, and what gets marked. A BLOCKED in 36-02 (probe FAIL) should re-route to 36-01 or the originating phase; this operational coordination is asserted but not specified.
- **R1 must_have wording is imprecise.** The plan says "every enumerated v1.6 contract (the 32-row traceability set plus the four SI IDs) must be represented," but the 32 rows are REQUIREMENTS — only 17 of them are contracts (5 CURR + 8 LOOP + 4 LOSS), plus 3 EVID-15 headlines, plus 4 SI IDs, plus the protected-path guard. The verify threshold of `>=22` rows is correct in practice, but the must_have text could mislead the executor into trying to enumerate all 32 REQs.
- **The 36-VERIFICATION.md Plan 36-05 frontmatter is not explicitly required.** The action says it "replicates the 35-VERIFICATION frontmatter schema" but Plan 36-05 does not call out a frontmatter-block verify step. The other plans emit `*-SUMMARY.md` but only 36-VERIFICATION.md needs the `phase/verified/status/score/gaps_remaining/must_haves/artifacts/prohibitions` schema to be machine-checkable.

**LOW**

- **Plan 36-05 Task 3 modifies `run-ac-suite.sh`** (adding `ac-traceability.py`) authored in Plan 36-01. The owned paths include `run-ac-suite.sh` in 36-05 so this is permitted, but cross-plan ownership of the driver should be noted explicitly to avoid double-edit risk if both plans re-execute.
- **Plan 36-04 Task 1 builds the SI table, then Task 2 asks the human to verify it.** If the human rejects a disposition, Task 1 must be re-done. A "draft proposal first, then approve, then write" sequence would be more efficient — minor optimization.
- **F4 path drift in 36-CONTEXT.md** (line 115: `29-acceptance-checks-reverification-handoff` vs the actual `29-acceptance-checks-re-verification-and-handoff`) is a CONTEXT bug, not a plan bug. Plans reference the correct path. The untracked 36-PATTERNS.md is correctly excluded by the dirty-file guard.
- **Plan 36-05 produces a 5-file commit** (REQUIREMENTS.md, ROADMAP.md, run-ac-suite.sh, ac-traceability.py, 36-VERIFICATION.md, summary). Commit policy requires a body and `Agent-Assisted-By` trailer — the plan calls this out. Consider splitting the manual ROADMAP/REQUIREMENTS edits from the verification/probe work for cleaner rollback.
- **The run-ac-suite.sh manifest-snapshot tie (R2 concurrency)** is not explicitly stated. The plan ties the SI grep to a working-tree snapshot, but the probe-results document should likewise record the manifest snapshot (commit or content hash) the run is tied to.

## 4. Suggestions

- **Before executing Plan 36-05 Task 2, confirm GAP-36-01 and GAP-36-02 are user-resolved.** If not, surface them as STOP gaps (per protocol) and obtain Option A ratification, or pick a different option. Cite the user-instruction event in the per-flip list (e.g., "GAP-36-01 Option A ratified <date>") so the provenance is re-derivable.
- **Strengthen the manifest audit (Plan 36-01 Task 1) to assert absence of rejected strings** (the cap-table fragment, `8.5`, `n_col=`, D-04 Option-C preservation) in both the manifest and the framework specs. This mechanizes Pitfall 1 protection.
- **Add a Phase 36 closure: STATE.md transition task** to Plan 36-05 (or a new plan) that names the GSD state handler invocation, the trigger condition (e.g., "after the final batch re-verify passes"), and the commit owned path. The current "outside this plan" deferral leaves a coordination hole.
- **Add a "re-execute" subsection to each plan's BLOCKED exit** that names the originating phase, the rerun command, and the audit step that proves the rerun is clean.
- **Mechanically verify the per-flip list in Plan 36-05 Task 1's audit:** assert each of the 13 flips is present with its anchor citation. Add a "per-flip count = 13" assertion alongside the existing 32/32 check.
- **Add a frontmatter-block verify step to Plan 36-05 Task 1** that asserts the `phase/verified/status/score/gaps_remaining/must_haves/artifacts/prohibitions` fields are present in `36-VERIFICATION.md` (mirroring the 35-VERIFICATION schema).
- **Record the manifest snapshot in `36-PROBE-RESULTS.md`** (commit hash or content hash) so stale/mixed evidence is detectable — R2 concurrency edge.
- **Consider splitting the wave 5 commit** into the manual ROADMAP/REQUIREMENTS edits (one commit, agent-owned-paths scoped tightly) and the verification/probe work (another commit). The commit policy permits this and improves rollback granularity.

## 5. Overall Risk: MEDIUM

The plans are competent, well-tested, and follow the SPEC R1–R6 spine faithfully. The HIGH concern is the only real blocker: if GAP-36-01/02 are not user-resolved, Plan 36-05 Task 2 makes an unauthorized extension of the closure anchor definition. Confirming those two gap decisions (or logging them as STOP gaps with proper OPTION selection) brings the overall risk to LOW. The MEDIUM concerns are addressable by tightening the manifest audit, owning the STATE.md transition, defining the BLOCKED rerun path, and mechanizing the per-flip list verification.

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

The Phase 36 plans are mostly coherent and well-grounded for closing v1.6: they build a manifest, run probes, close the ledger, reconcile SI metadata, write the handoff, and reconcile traceability. The dependency order is sensible.

The main risk is that Plan 36-05 adds a new traceability probe after the manifest/probe-results flow has already been sealed, without updating all artifacts and declared modified paths that earlier plans make authoritative.

## 2. Strengths

- Clear five-wave ordering: manifest → probe evidence → ledger closure → handoff/SI routing → final verification.
- Strong grounding discipline: plans consistently avoid live `pinn/` as a source, route silent SI decisions through STOP, and preserve frozen/read-only boundaries.
- Good fail-closed intent: failed probes, nonterminal ledger rows, missing SI dispositions, and traceability mismatches are supposed to block closure rather than become advisory.
- GAP-36-01 and GAP-36-02 are resolved and give Plan 36-05 a grounded rule for PKG and LOOP-07/08 status reconciliation.
- The plans explicitly protect unrelated dirty files and avoid hand-editing `STATE.md`.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

**HIGH — Plan 36-05 breaks the manifest/probe-results invariant.**  
Plan 36-05 creates `probes/ac-traceability.py` and says to add it to `run-ac-suite.sh`, but `run-ac-suite.sh` is not listed in `files_modified`. It also does not update `36-ACCEPTANCE-MANIFEST.md`, `36-PROBE-RESULTS.md`, or `evidence/`, even though Plans 36-01/02 define the suite as one probe/result/evidence record per manifest row. This can leave the final traceability probe outside the authoritative manifest and hashed probe-results record.

**MEDIUM — Several automated audits are weaker than the acceptance criteria they claim to enforce.**  
Examples: Plan 36-01 uses `>=22` rows despite requiring a specific manifest inventory and does not fully enforce duplicates/protected-path row coverage. Plan 36-02 checks that manifest IDs appear in `36-PROBE-RESULTS.md`, but not exactly once, and does not verify each cited evidence file exists or its SHA-256 matches. Plan 36-04 checks finding IDs appear somewhere in the handoff, but not exactly once across Fixed / Intentionally Unchanged / Deferred.

**MEDIUM — Status reconciliation happens before the final re-verification gate.**  
Plan 36-05 flips `REQUIREMENTS.md` statuses to `Complete` in Task 2, then adds the companion probe and performs final batch re-verification in Task 3. If Task 3 fails, the plan does not explicitly say to revert or withhold those status flips. The fail-closed intent is clear, but the edit order can leave terminal-looking planning state in a blocked working tree.

**LOW — Protected-path guard is brittle.**  
The `grep -rlE 'pinn/' probes/` guard will fail if the guard script itself or probe comments contain the literal `pinn/`. This is avoidable, but the plan should spell out the implementation pattern to prevent self-failure.

## 4. Suggestions

- In Plan 36-05, add `run-ac-suite.sh` to `files_modified`, and either add `ac-traceability.py` to the manifest/results/evidence flow or explicitly define it as a separate verification-only probe with its own recorded evidence.
- Strengthen audits from substring/count checks to exact set checks: manifest IDs, result sections, evidence files, hashes, and handoff classification partitions.
- Move `REQUIREMENTS.md`/`ROADMAP.md` terminal flips after final batch re-verification, or state that failed final verification requires reverting/marking those edits blocked before commit.
- Make the protected-path guard avoid literal self-matches, for example by constructing the forbidden path token dynamically.

## 5. Overall Risk

**MEDIUM**. The phase design is sound, but Plan 36-05’s late probe integration and the weak exactness checks could undermine the closure evidence unless corrected before execution.

---

## agy Review

# Cross-AI Plan Review: Phase 36 Acceptance Checks & Re-Verification Handoff

## 1. Summary
The Phase 36 plan sequence (Waves 1-5) is a highly defensive, comprehensive closure workflow for v1.6. It establishes acceptance criteria via a manifest, builds disposable probes, captures hashed test evidence, finalizes the Phase 32 issue ledger, builds the closure handoff, and reconciles the core project tracking files. The workflow successfully delegates complex verification into executable, reproducible scripts.

## 2. Strengths
- **Exceptional Security & Integrity:** The `protected-path` guard explicitly forbids probes from executing against or importing live `pinn/` code, forcing the use of isolated toy samples. This prevents accidental mutations of the production surface.
- **Fail-Closed Architecture:** Relies heavily on SHA-256 evidence hashing, explicit transcription verifications, and deterministic fail-closed gating (assigning `BLOCKED` instead of ignoring failures).
- **Human-in-the-Loop Gates:** `36-04-PLAN.md` correctly toggles `autonomous: false` and uses an explicit checkpoint to solicit human approval for subjective `SI` preserve dispositions prior to completion.

## 3. Concerns

- **HIGH: Missing Files in `36-05-PLAN.md` Frontmatter**
  Task 2 instructs the agent to log a STOP gap in `36-GAPS.md` and `v1.6-GAPS.md` if an anchorless row is found. Task 3 instructs the agent to append the new `ac-traceability.py` probe to `run-ac-suite.sh`. The `<output>` block correctly scopes these files in the `GIT_AGENT_OWNED_PATHS`. However, **none of these three files are declared in the `files_modified` YAML frontmatter**. The GSD execution framework will likely block the agent from editing these files, causing the plan to fail.
  
- **LOW: Inconsistent Row Bound in `36-01-PLAN.md` Automated Audit**
  The Task 1 Python verification script asserts `len(body) >= 22`. However, the script then explicitly iterates over and enforces the presence of exactly 25 unique `AC-*` / `SI-*` IDs. While mathematically safe (`25 >= 22`), the 22 bound is artificially low and inconsistent with the actual required minimum (26 rows, including the `protected-path-guard`).

## 4. Suggestions
- **Fix `36-05-PLAN.md` Frontmatter:** Add `.planning/phases/36-acceptance-checks-re-verification-handoff/run-ac-suite.sh`, `.planning/phases/36-acceptance-checks-re-verification-handoff/36-GAPS.md`, and `.planning/milestones/v1.6-GAPS.md` to the `files_modified` array so the agent is authorized to complete its instructions.
- **Adjust `36-01-PLAN.md` Assertion:** Update `len(body) >= 22` to `len(body) >= 26` to accurately reflect the true minimum bounds of the manifest table.

## 5. Overall Risk
**LOW** 
The plans are incredibly rigorous and logically sound. Resolving the frontmatter discrepancy in `36-05-PLAN.md` removes the only material execution risk.

---

## opencode Review

_opencode failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=opencode
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=opencode run - 
- stdout_bytes=0
- stderr_bytes=58

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031247Z-13606/xreview-opencode-36.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031247Z-13606/xreview-opencode-36.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260701T031247Z-13606/xreview-opencode-36.meta

Stderr excerpt:
```
[0m
> build · grok-4.3
[0m
[0m→ [0mSkill "xreview"

```

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
- elapsed_seconds=182
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-minimax -p - 
- stdout_bytes=9702
- stderr_bytes=192

### cursor
- status: preserved from existing REVIEWS.md

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=265
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3940
- stderr_bytes=25248

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=77
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=2867
- stderr_bytes=0

### opencode
- reviewer=opencode
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=opencode run - 
- stdout_bytes=0
- stderr_bytes=58

### claude-kimi
- reviewer=claude-kimi
- exit_code=0
- elapsed_seconds=67
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp kimi -p - 
- stdout_bytes=7306
- stderr_bytes=192

---

## xconverge Source-Grounding Verification + Cycle-1 Reconciliation

_Appended by Agent B (xconverge orchestrator), cycle 1 of max-cycles 1, 2026-07-01._

### Source-grounding gate — PASS

Every symbol cited by `36-01..36-05-PLAN.md` was enumerated and verified against source:

- **Requirement IDs** — VER-13..18 (`REQUIREMENTS.md:67-72`), SCOPE-12..15 (`:92-95`), LOOP-01..08 / CURR-01..05 / PKG-05..08 / EVID-15 / PHYS-03/05 (traceability rows present). All present.
- **SI universe (exactly four)** — SI-CTL-001 (`ctl_instruction.md:2140`), SI-DQA-003 (`:548`), SI-PINN-002 (`pinn_architecture.md:1047`), SI-PINN-003 (`:1056/1059`; `ctl:1793`). All present.
- **Ledger anchors** — D-05/D-06 PENDING (`32-ISSUE-LEDGER.md:16-17`); M14 LOOP-04 row + LOOP-07/08 provisional SATISFIED (`34-VERIFICATION.md:115/118-119`); D-36-17 ROADMAP-defer anchor (`34-VERIFICATION.md:102`). All present.
- **Phase artifacts** — `32-ISSUE-LEDGER.md`, `32-GAPS.md`, `33/34/35-VERIFICATION.md`, `v1.6-GAPS.md`, `scripts/agent-commit` — all exist on disk.
- **Forbidden-grounding scan** — no `pinn/basic_architecture` or `pinn/data-processing-pipeline` reference in any plan. ✓

Verdict: no fabricated citations; plans are well-grounded (independent of review findings).

### Cycle-1 reviewer reconciliation (transparency)

Requested panel `--codex --claude-minimax --agy --opencode --claude-kimi`: codex=ok, claude-minimax=ok, agy=ok, **opencode=stub (empty/timeout at 360 s)**, claude-kimi=ok. xreview upsert also preserved four prior-run sections (`claude`, `claude-deepseek`, `cursor`=usage-limited, `claude-glm`=529) from an earlier `36-REVIEWS.md`.

**HIGH findings — counted (3):**
1. `files_modified` omits `run-ac-suite.sh`, `36-GAPS.md`, `v1.6-GAPS.md` despite Task 2/3 editing them — execution-blocking (codex, agy — fresh panel; verified `36-05-PLAN.md:10-15` vs `:141/:173/:235`).
2. 36-05 re-opens the probe suite after 36-02 sealed hashed evidence without specifying regenerate/subdir/append — evidence/ SHA-256s can mismatch the final suite (claude-deepseek — preserved section; verified unaddressed at `36-05-PLAN.md:173` vs `36-02-PLAN.md:78`).
3. 36-05 edits REQUIREMENTS.md/ROADMAP.md without the pre-write SHA-256 freshness check 36-03 applies to the ledger (claude-deepseek — preserved section; verified `36-05-PLAN.md:141` vs `36-03-PLAN.md:21/117`).

**HIGH findings — assessed and NOT counted (3, all claude-kimi, fresh panel):**
- _"No runnable definition of accept"_ — addressed: `36-01` defines a manifest (pass-criterion + data + command per AC) mapped 1:1 to disposable probes + fail-closed `run-ac-suite.sh`; residual edge (spec-consistency probes are token-grep) is MEDIUM-at-most and matches VER-13/15.
- _"Resolution doc may be in flight"_ — invalid premise: Phase 31 readiness PASSED (READY-WITH-CAVEATS, 2026-06-20) and the doc landed (commit `49fb7958`); STATE.md confirms 32-36 unblocked on that gate.
- _"pinn/STATUS.md + NN-CODE-DIVERGENCE.md violate live-code ban"_ — invalid: repo CLAUDE.md carries an explicit carveout permitting `pinn/` references **only** in those forward-pointing handoff docs.

**Actionable non-HIGH (4):** codex (revert/withhold Task-2 status flips if Task-3 re-verify fails); mixed (tighten audit floors — manifest >=22->>=26, per-row hash binding, handoff exactly-once partition); claude-minimax (own the STATE.md closure transition — `36-05:173` defers it unnamed); claude-minimax (mechanize Pitfall-1 absence at the manifest layer).

### Cycle-1 verdict

`current_high=3, current_actionable=4` -> **NOT converged.** Cycle budget (max-cycles 1) exhausted. Recommended next command: `$gsd-plan-phase 36 --reviews` (replan to fold in the 3 HIGHs), or direct Agent A to apply the frontmatter/clarification fixes. The single fresh-panel HIGH (#1, `files_modified`) is mechanical and execution-blocking; #2/#3 are underspecifications in 36-05 Task 3.

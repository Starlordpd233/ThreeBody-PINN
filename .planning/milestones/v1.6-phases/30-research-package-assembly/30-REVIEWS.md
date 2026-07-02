---
phase: 30
reviewers: [codex, qwen, opencode, claude, cursor]
reviewers_failed: [antigravity]
reviewed_at: 2026-06-18T04:32:52Z
plans_reviewed: [30-01-PLAN.md, 30-02-PLAN.md, 30-03-PLAN.md, 30-04-PLAN.md, 30-05-PLAN.md]
---

# Cross-AI Plan Review — Phase 30: Research Package Assembly

Five independent AI CLIs reviewed the five Phase-30 plans (30-01..30-05) against the same prompt
(PROJECT context, the ROADMAP Phase-30 section, REQUIREMENTS, CONTEXT user decisions, SPEC, and
RESEARCH). Models/harnesses: **Codex** = OpenAI codex-cli 0.135.0; **Qwen** = Qwen Code;
**opencode** = gemini-3.1-pro-preview; **Claude** = claude CLI v2.1.181 (separate headless
session); **Cursor** = cursor-agent. Antigravity (`agy`) was requested but could not return a
review in this environment (see its section).

To incorporate this feedback into planning, run: `/gsd-plan-phase 30 --reviews`

---

## Codex Review

**Summary**

The Phase 30 plan set is strong overall: it decomposes the research-package assembly into the right sequence, preserves the D-09 user gate, keeps adjudication out of scope, and repeatedly reinforces read-only and no-invention constraints. The main risks are not conceptual coverage but execution inconsistencies: PKG-07 is not clearly included in the uploaded package, `pinn/` wording conflicts with the zero-repo-path checks, `source_baseline` is defined inconsistently, and STATE.md may be mutated outside the final commit scope.

**Strengths**

- Clear dependency ordering: 30-01 characterizes inputs and seeds claims, 30-02 gates consolidation, 30-03 snapshots, 30-04 authors questions, 30-05 delivers.
- Strong read-only discipline for `review_of_framework.md`, `stage_strat_revision.md`, frozen specs, and `pinn/`.
- D-09 is correctly modeled as a blocking user gate in `30-02-PLAN.md`.
- Claims discipline is well-designed in `30-01-PLAN.md`, especially the v1.6 no-Phase-24 boundary.
- Neutrality is mostly explicit: D-04, D-05, D-06, and the `D = 6.694` conflict are repeatedly marked unsettled.
- The plans include concrete verification checks for hashes, repo-path leakage, finding coverage, and read-only source diffs.

**Concerns**

- **HIGH:** `30-01-PLAN.md` creates `30-CLAIMS-INVENTORY.md` under `.planning`, but `30-04` and `30-05` do not clearly place a claims register in the uploaded package. PKG-07 requires the package itself to present claimed-vs-verified figures.
- **HIGH:** `30-04-PLAN.md` and `30-05-PLAN.md` require stating the `pinn/` override, but their zero-repo-path grep rejects `pinn/`. This creates either a verification failure or a path-leak violation.
- **HIGH:** `30-05-PLAN.md` says framework specs plus SCOPE-12 constraints are hard. That risks over-grading current doc-03-relevant spec content as non-revisable. Only locked v1.4/v1.5 outcomes should be hard constraints; other current spec positions are baseline evidence.
- **HIGH:** `30-05-PLAN.md` commits the package before recording gate-open via gsd-tools. If gsd-tools mutates `.planning/STATE.md` afterward, the state change is uncommitted and outside `files_modified`.
- **MEDIUM:** `source_baseline` is inconsistent. `30-01` cuts a pre-phase recovery tag, while `30-03` also describes `source_baseline` as current HEAD at assembly time. These are different commits after 30-01 and 30-02 commits.
- **MEDIUM:** `30-04-PLAN.md` asks writers to state “current framework-spec position” but does not explicitly require reading the relevant sections of `ctl_instruction.md` and `pinn_architecture.md` for each finding. Relying on summaries risks accidental invention.
- **MEDIUM:** `30-01-PLAN.md` seeds claims from `30-RESEARCH` C-1..C-13, but its stated truth is “every dataset/empirical figure stated by issue-03.” Add a full numeric/figure sweep against issue-03 to avoid omissions.
- **LOW:** `30-SNAPSHOT-HASHES.txt` terminology mixes SHA-256 file hashes and source commit hashes. The columns should distinguish file digest, canonical source, and source commit.

**Suggestions**

- Add an explicit uploaded claims artifact, e.g. `claims-register.md`, or require `RESEARCH-CONTEXT-MASTER.md` to include the full claims register in all delivery forms.
- Replace literal `pinn/` in upload-class files with wording like “live implementation-code citations” and keep repo-path specifics only in `DELIVERY-NOTE.md`.
- In `30-05`, revise source grading: “SCOPE-12 locked outcomes are hard constraints; current framework specs are the baseline/current design state except where those locked outcomes apply.”
- Move the gsd-tools STATE update before the final commit and include `.planning/STATE.md` in explicit owned paths, or add a separate final planning-state commit.
- Define two separate values: `source_baseline` for source snapshots and `package_commit` for the final delivered package commit.
- In `30-04`, require per-finding checks against the relevant spec snapshots, and state “framework spec silent/ambiguous” when no grounded position exists.
- In `30-01`, add a verification step that scans issue-03 for numeric claims and reconciles each against a CLM row or an explicit “not dataset/empirical” exclusion note.
- Clarify `30-SNAPSHOT-HASHES.txt` schema before execution: `basename | source path | file sha256 | source commit | notes`.

**Risk Assessment**

Overall risk: **MEDIUM**. The plan set is directionally complete and well-governed, with strong ordering and scope boundaries. The remaining risks are specific and fixable, but several are capable of producing a non-compliant package: omitting the claims register from the upload, failing repo-path checks, over-hardening current spec positions, or leaving STATE.md uncommitted. Fixing those before execution should reduce the phase risk to low.


---

## Qwen Review

# Cross-AI Plan Review: Phase 30 — Research Package Assembly (Plans 30-01 through 30-05)

## Summary

The five-plan decomposition for Phase 30 is well-structured, closely following the proven v1.5 Phase 23 pattern while correctly adapting for the critical v1.6 structural difference (no Phase-24 analog). The plans collectively cover all six locked requirements (PKG-05 through PKG-08, the skeleton, and delivery/gate-open), maintain strict sequential dependency ordering with the D-09 user gate as a hard serialization point, and consistently enforce the no-invention / read-only discipline that the STOP protocol demands. The primary weaknesses are: (1) a gap in the claims-register lifecycle — the phase-local register is seeded in 30-01 but no plan explicitly produces its *uploaded* (package-internal) form; (2) the single-master-vs-multi-companion architectural decision is deferred as "Claude's discretion" but materially shapes plans 30-04 and 30-05 and should be resolved earlier; and (3) the full finding inventory is supposed to be "locked during assembly after reading issue-03 in full" but the full read is deferred to 30-04, creating a sequencing tension with the claims register seeded in 30-01.

## Strengths

- **Recovery-tag pre-flight (30-01 Task 1) is exemplary.** The orphaned-tag state is surfaced with exact evidence (`85f72f88` not ancestor of `4f260aa3`), two resolution options are presented (re-cut with `-f` vs. fresh tag), and the three destructive-git governance markers are required. This is the highest-risk operational step in the phase and it is handled correctly.

- **D-09 user gate (30-02 Task 2) is a properly modeled blocking-human checkpoint.** The three open inclusion calls (sim_data excerpt selection, standalone-vs-folded verified-facts, ALM-μ_p-clamp coverage) are each posed as explicit user decisions with a concrete approve-as-proposed / approve-with-changes option pair. Assembly cannot proceed without the "D-09 APPROVED" record being committed. This matches the PKG-05 hard requirement exactly.

- **Byte-for-byte snapshot verification (30-03 Task 1) is rigorous.** The `cmp -s` per-pair check across all six snapshots, plus `git diff --quiet` re-confirmation on the two read-only reports, provides strong tamper evidence. The `30-SNAPSHOT-HASHES.txt` with per-file source-commit hashes and a package-wide `source_baseline` pin makes the snapshot set reproducible.

- **Neutral-framing enforcement (30-04) is well-designed.** The automated verification explicitly checks all 15 required finding IDs (`B-07` through `D=6.694`), the repo-path-leak grep covers the five forbidden path prefixes, and Task 2 explicitly requires D-04/D-05/D-06 and the D conflict to state both positions without presupposing a resolution. The seed-conflict example (`D=6.694` vs `D≈4.6416`) is cited as a worked example of issue-doc non-authoritativeness.

- **The no-in-milestone-verification boundary (D-17) is consistently threaded.** It appears in the claims register (30-01 Task 3, with a verbatim transcription requirement), is called out as a v1.6≠v1.5 delta in the delivery note (30-05 Task 3, "REMOVE Phase 24 parallel section; ADD no-verification note"), and the claims register seed includes a "FUT-flag" column replacing v1.5's "Phase-24 check" column.

- **Scope discipline is strong across all plans.** No plan creates, edits, or references `pinn/` live code as grounding. Framework specs are consistently marked "NEVER consolidated" (30-02 Task 1, 30-03 Task 1). The read-only reports are consistently marked "baseline design intent + baseline-critique mandate" (ERW rule 6). `sampling_method.md` is consistently marked FROZEN/SCOPE-08.

- **STRIDE threat models are proportionate.** For a documentation-assembly phase, the identified threats (repo-path leaks into uploads, tampering with read-only sources, direct STATE.md edits, destructive git ref moves) are the correct risk surface. No plan wastes effort on N/A categories (npm/pip/cargo — explicitly "no installs").

## Concerns

- **HIGH — Claims-register uploaded form has no explicit producer.** Plan 30-01 Task 3 creates `30-CLAIMS-INVENTORY.md` as a *phase-local* artifact (under `.planning/phases/30-*/`). But the package needs a claims register *inside* the upload set — either as a named companion file in `research_package/` or as a section of `RESEARCH-CONTEXT-MASTER.md`. No plan explicitly creates this uploaded copy. The CONTEXT recommends companion files, and 30-04 creates three companions (framed-questions, preamble, skeleton), but the claims register is not among them. Plan 30-05's master (Task 1) says "If the single-master form is chosen over companions, fold framed-questions/preamble/skeleton/**claims-register** in as master sections" — but the claims register was never created as a companion to fold. The executor must either (a) add a claims-register companion in 30-04 or (b) explicitly plan to embed it in the master in 30-05. As written, this is a gap.

- **MEDIUM — Single-master vs. multi-companion decision deferred too late.** The CONTEXT marks this "Claude's discretion" and the RESEARCH recommends companions. But this decision materially shapes 30-04 (how many files to create) and 30-05 (how the master references them). It should be resolved at the D-09 gate (30-02) as a fourth inclusion call, or at minimum stated explicitly in 30-03's "package-nesting note" so 30-04 inherits a settled architecture. Deferring it to 30-05 execution risks rework.

- **MEDIUM — Finding-inventory timing mismatch.** The claims register is seeded in 30-01 from the RESEARCH's pre-scanned inventory (C-1..C-13, V-1..V-6). But the SPEC says the full finding inventory is "locked during assembly **after reading issue-03 in full**" — and the full read of issue-03 (711 lines) is a 30-04 Task 2 `read_first`. If the 30-04 full read discovers additional figures not in the 30-01 seed, the claims register must be updated — but no plan accounts for this. The 30-01 seed should be explicitly marked "provisional; extended in 30-04 after full issue-03 read," or 30-04 should include a claims-register-extension step.

- **MEDIUM — gsd-tools invocation in 30-05 Task 3 is vague.** The plan says "record the gate-open state in STATE.md via a gsd-tools state handler ONLY (e.g. `gsd-tools state ...`)" but does not specify the exact subcommand, arguments, or expected STATE.md fields to change. If the executor cannot determine the correct invocation, the gate-open record fails (VC-10). The plan should either provide the exact command or mandate a `gsd-tools --help` lookup step before execution.

- **LOW — 30-03 `autonomous: true` tension.** The plan header says `autonomous: true`, but Task 2 (consolidated-context file) depends on the D-09 APPROVED record's resolved inclusion calls — which are user decisions made in 30-02. The plan's `read_first` for Task 2 correctly references the D-09 record, so the executor *can* proceed autonomously given the approved plan, but the `autonomous` flag might mislead an orchestrator into thinking no human input is consumed. Consider `autonomous: false` or adding a note that D-09 decisions are consumed as inputs.

- **LOW — Verification regex inconsistency in 30-04 Task 2.** The coverage check includes `D5` (for the stage-transition finding) but the finding ID in the issue doc and the SPEC is `D5` while the human-approval decision is `D-05` (s_min frame). These are different findings. The regex `for t in B-07 B-08 M6 M7 M14 M15 M16 D5 NS-12 NS-13 NS-18 D-04 D-05 D-06 6.694` correctly lists both `D5` and `D-05`, but an executor unfamiliar with the naming might confuse them. A brief disambiguation note would help.

- **LOW — DELIVERY-NOTE.md placement inconsistency with D-03.** CONTEXT D-03 says the ERW-fixed file set is "at the round root" including `DELIVERY-NOTE.md`. Plan 30-05 places it at `03-curriculum-and-training-loop/DELIVERY-NOTE.md` (round root), while the master/prompt/specs are nested under `research_package/`. This matches the delivered v1.5 form and is correct, but the RESEARCH's "layout caveat" (noting the runbook nests everything under `research_package/`) is resolved differently for the delivery note vs. the other files. Plan 30-03's "package-nesting note" should explicitly state this split: delivery note at round root, everything else under `research_package/`.

## Suggestions

- **Add a claims-register companion creation step to 30-04, or explicitly scope it as a master section in 30-05.** The simplest fix: add a Task 4 to 30-04 that creates `research_package/claims-register.md` (or whatever the companion is named) by copying/adapting the phase-local `30-CLAIMS-INVENTORY.md` into upload-ready form (stripping any repo-path references, adding the D-17 boundary statement, cross-referencing the framed-questions' CLM IDs). Alternatively, 30-05 Task 1 should explicitly state that the claims register is embedded in the master as a section, not shipped as a companion.

- **Resolve the single-master vs. multi-companion decision at the D-09 gate (30-02).** Add it as a fourth open inclusion call in the consolidation plan: "Are the framed questions, SCOPE-12 preamble, resolution-doc skeleton, and claims register shipped as named companion files (research recommends) or consolidated into RESEARCH-CONTEXT-MASTER.md as sections (v1.5 delivered form)?" This prevents 30-04 and 30-05 from discovering the decision mid-execution.

- **Add a claims-register extension step to 30-04.** After the full issue-03 read in Task 2, check whether any newly-discovered figures lack CLM rows, and extend `30-CLAIMS-INVENTORY.md` (and the package copy) accordingly. This closes the finding-inventory timing gap.

- **Specify the exact gsd-tools subcommand in 30-05 Task 3.** Either provide the literal command (e.g., `gsd-tools state set-phase 30 --status delivered`) or add a mandatory `gsd-tools state --help` step that the executor runs before the STATE mutation. The current "e.g. `gsd-tools state ...`" is too vague for a governance-controlled operation.

- **Add a pre-delivery acceptance sweep task to 30-05.** Before the final commit (Task 3), run the full acceptance-check sweep from 30-VALIDATION.md: VC-01 (repo-path grep on all uploads), VC-02 (snapshot hash spot-check), VC-04 (figure→CLM coverage sweep on the master), VC-07 (coverage checklist), VC-08 (unsettled-check on D-04/D-05/D-06/D). Currently, each plan verifies its own tasks, but no single task runs the *cumulative* pre-delivery sweep across all package files.

## Risk Assessment

**Overall risk: LOW**

The plan set is well-grounded in the v1.5 Phase 23 precedent, the ERW runbook, and the locked CONTEXT decisions. The two highest-consequence risks — leaking a repo path into an uploaded file (undermining the repo-blind guarantee) and consolidating a framework spec (undermining the byte-for-byte grounding) — are each mitigated by multiple overlapping controls (automated grep checks, explicit "NEVER consolidated" statements, `cmp -s` verification, hash provenance). The claims-register lifecycle gap (concern #1) is the most likely source of execution friction, but it is a missing-deliverable problem, not a correctness problem — the executor will discover it during 30-04/30-05 assembly and can recover by creating the companion or embedding in the master. The D-09 user gate provides a natural recovery point for any architectural decisions that were deferred too far. No plan risks inventing content, asserting a verdict, or editing a frozen/read-only file.


---

## opencode Review

# Cross-AI Plan Review: Phase 30 (Research Package Assembly)

## 1. Summary
The phase-30 implementation plans represent a highly disciplined, rigorously governed approach to assembling a neutral, spec-engineering research package. The decomposition successfully maps the complex web of ERW (External Research Workflow) constraints, hard requirements (PKG-05 through PKG-08), and STOP-protocol mandates into an ordered execution pipeline. The plans excel at explicitly defining verification checks (e.g., `cmp -s`, `git diff --quiet`, negative grep searches for repo paths) to guarantee that source files are not edited and upload boundaries are not violated. 

## 2. Strengths
*   **Impenetrable Grounding Guardrails:** The use of `cmp -s` in `30-03` and `git diff --quiet` in `30-01` guarantees that the framework specs and research reports are not inadvertently summarized, consolidated, or edited. This perfectly enforces the "no-invention" STOP mandate.
*   **Excellent Handling of Edge Cases:** Proactively identifying and addressing the orphaned recovery tag (`v1.6-pre-phase-30`) in `30-01` as a user-approved blocking task prevents a potential destructive git history disaster.
*   **Honest Accounting of Verification Debt:** The plans correctly identify that v1.6 lacks a parallel empirical verification phase (unlike v1.5's Phase 24) and explicitly weave the "no-in-milestone-verification" boundary into both the claims register (`30-01`) and the delivery note (`30-05`).
*   **Information Governance:** The strict `grep` validation in `30-04` and `30-05` to ensure zero internal repo paths leak into the externally uploaded prompt or master files is a brilliant operational security measure.

## 3. Concerns
*   **[MEDIUM] Single-Master vs. Multi-Companion Ambiguity:** In `30-04` and `30-05`, the choice between folding questions, preambles, and skeletons into a single `RESEARCH-CONTEXT-MASTER.md` versus leaving them as separate companion files is left to "Claude's discretion." If the execution agent vacillates between these two files during sequential waves, it risks creating dangling companion files that are omitted from the manifest, or a bloated master that breaks ERW formatting rules.
*   **[MEDIUM] Hardcoded Snapshot Lists vs. User Gate Decisions:** In `30-03` Task 1, the list of six framework specs/reports to snapshot is hardcoded into the action instructions and the `verify` script. However, the `30-02` plan surfaces the final document list at a blocking user gate (D-09). If the user alters the candidate list during the gate, the hardcoded verification script in `30-03` will fail or copy an incorrect subset.
*   **[LOW] "MINOR" ALM-clamp Finding Scope Leak:** `30-02` defers the inclusion of the MINOR ALM-clamp finding to the user gate. If the user excludes it from the framed questions, the external agent might still stumble upon it in the raw `issue-03` document and hallucinate a verdict. 

## 4. Suggestions
*   **Surface the Layout Decision at the D-09 Gate:** Add the "single-master vs. multi-companion files" choice to the explicit inclusion calls in `30-02` Task 1. Having the user lock this decision removes assembly-time ambiguity and ensures the external research agent receives a consistently formatted package.
*   **Make `30-03` Dynamic to the D-09 Record:** Instruct the agent in `30-03` Task 1 to dynamically read the "Approved Document List" from the `30-CONSOLIDATION-PLAN.md` D-09 record to drive the snapshotting process, rather than relying on a hardcoded list. Update the bash verification script to parse the approved list.
*   **Pre-empt Excluded Findings in the Preamble:** If the user excludes the ALM-clamp finding (or any other finding) during the `30-02` gate, explicitly list it in the `30-04` SCOPE-12 preamble as "Out of Scope for this Adjudication" so the external AI knows to ignore it.

## 5. Risk Assessment
**Overall Risk Level: LOW**

The architectural integrity of these plans is exceptionally high. The risk of the agent inventing spec content or altering the "candidate verdict source" is fully mitigated by the bash-level byte-for-byte comparisons and diff checks. The separation of the process into distinct waves—particularly putting the consolidation plan behind a blocking user gate (`30-02`) before any snapshotting (`30-03`) begins—ensures the human user maintains absolute authority over the research payload. Implementing the minor suggestions regarding layout ambiguity and dynamic snapshot lists will close the remaining procedural gaps.


---

## Claude Review

# Cross-AI Plan Review — Phase 30: Research Package Assembly

## 1. Summary

This is a disciplined, well-structured five-plan set that closely and faithfully reuses the directly-analogous v1.5 Phase 23 pattern, and it correctly internalizes the single most important structural delta for v1.6: there is **no in-milestone verifier** (no Phase-24 analog), so the package must carry "claimed, unverified" honestly and delegate verification downstream. Dependency ordering is clean and linear, the two human gates (recovery-tag, D-09 consolidation) are correctly modeled as blocking and their plans flagged non-autonomous, the no-invention/no-verdict discipline is strong throughout, and traceability to the six locked requirements is complete. The plan set will *largely* produce a complete, neutrally-framed handoff. However, there is one genuine completeness gap that threatens the self-containment goal — **the uploaded form of the claims register (PKG-07) is never concretely produced**, leaving inline `CLM-NN` references potentially unresolvable for a repo-blind agent — and a recurring **action-vs-verify contradiction** around the literal string `pinn/` that collides with the repo-path leak grep. Both are fixable with small, targeted edits before execution.

## 2. Strengths

- **Faithful template reuse.** Every artifact maps to a verified v1.5 analog (`23-CONSOLIDATION-PLAN.md`, `23-CLAIMS-INVENTORY.md`, `23-DQA-CHARACTERIZATION.md`, `23-SNAPSHOT-HASHES.txt`, the delivered `02-*/` master/delivery-note). This is low-risk and concretely cited in each `read_first`.
- **The v1.6≠v1.5 delta is threaded correctly end-to-end.** 30-01 Task 3 transcribes the D-17 no-in-milestone-verification boundary verbatim into the register; the register drops the "Phase-24 check" column for a "FUT-flag" column; 30-05 Task 3 explicitly *removes* the v1.5 "Phase 24 runs in parallel" delivery-note section and *adds* the no-verification note. This is the subtlest part of the phase and it is handled well.
- **No-invention / read-only discipline is enforced at multiple layers.** Characterization is descriptive (provenance + content map + relation), not adjudicative; frozen/read-only files are snapshot-only with `cmp -s` *and* `git diff --quiet` checks (30-01 VC-03, 30-03 Task 1); framework specs are explicitly "NEVER consolidated" (D-04) and that rule is restated in 30-02, 30-03, and the threat models.
- **Decisions kept genuinely open.** 30-04 poses D-04/D-05/D-06 + the `D` conflict as UNSETTLED, states both the issue-doc and framework-spec positions, and tells the external agent that *both* the issue doc and its "Recommended Resolutions" are non-authoritative (VC-08). The baseline-critique mandate (ERW rule 6) on the two reports correctly preserves their challengeability.
- **Correct gate modeling and autonomy flags.** 30-01 and 30-02 (the plans containing blocking-human checkpoints) are `autonomous: false`; 30-03/04/05 are `autonomous: true`. The D-09 consolidation gate is correctly framed as a hard PKG-05 requirement, not a courtesy, with `depends_on: ["30-02"]` serializing assembly behind approval.
- **Clean traceability.** All six locked requirements map to tasks (PKG-08→30-01; PKG-07→30-01 seed + 30-05; PKG-05→30-02/30-03; PKG-06→30-04; skeleton→30-04; delivery/gate→30-05); frontmatter `requirements:` fields are consistent with the SPEC.
- **Recovery-tag governance.** 30-01 Task 1 correctly treats the orphaned `v1.6-pre-phase-30` tag as a blocking-human destructive-git decision, requiring the three governance markers for `git tag -f` or a non-destructive fresh tag, and uses `git tag --points-at HEAD` (dynamic) rather than trusting a hardcoded hash.

## 3. Concerns

- **[HIGH] The uploaded claims register (PKG-07) is never concretely produced.** 30-01 creates `30-CLAIMS-INVENTORY.md` as a *phase artifact* under `.planning/` (never uploaded, and full of repo-path citations). 30-04 produces exactly three companions (questions, preamble, skeleton) — **no claims-register companion**. 30-05 Task 1's master action only folds the register in *conditionally* ("If the single-master form is chosen…"), and the master manifest enumerates "the three 30-04 companions" with no register among them. Under the CONTEXT-default multi-companion path, a repo-blind agent attaching the `research_package/` set sees inline `CLM-NN` references (mandated by 30-04 Task 2) with **no resolving table** in the upload. This directly fails PKG-07's "all inline figure mentions reference their register ID" and the self-containment goal.
- **[HIGH] `pinn/` override statement contradicts the repo-path leak grep.** The SCOPE-10 governance message ("issue-03's 'Canonical' `pinn/` citations are overridden") is explicitly instructed in 30-04 Task 1 (action), 30-04 Task 2 (action), and **30-05 Task 1 (action: "pinn/ 'Canonical' citations OVERRIDDEN")** — yet the upload-class verify is `! grep -qE '(…|pinn/)'` (30-04 Task 2, 30-05 Task 1/2). So the master/questions tasks instruct writing `pinn/` while their own verify bans it. A careful executor will rephrase ("the live `pinn` implementation files", name the two `.py` files bare); a careless one may *delete the governance-required override statement* to pass the grep. The plans never call out this tension or prescribe the safe phrasing.
- **[MEDIUM] Citation upload-safety is unresolved when folding the register into the master.** The register's `verified` rows must cite v1.5 sources (PKG-07), but the seeded citations are repo paths — `simulation_data/Documentation/...`, `.planning/milestones/v1.5-phases/24-...` — which trip the master's own repo-path grep (`simulation_data`, `.planning`). No task specifies the translation from repo-path citations (phase artifact) to bare-filename citations (upload form), so folding the register risks either a verify failure or a weakened "cite the v1.5 grounding" claim.
- **[MEDIUM] Single-master vs multi-companion is left undecided across two dependent plans.** RESEARCH flagged this as "materially shaping how many companion files the plans produce," yet 30-04 *always* writes three companion files and 30-05 *may* fold them into the master — with no reconciliation of the resulting duplication, and no rule for whether the prompt's attach list (30-05 Task 2: "master + the three companions + the 7 specs") should then list both the master and the now-redundant companions. This is a coordination weakness, not just a presentation call.
- **[MEDIUM] `D = 6.694` "posed unsettled" risks re-opening a locked value.** SCOPE-12/D-13 lists `D ≈ 4.6416` (with 6.694 rejected by EVID-10) as a *hard constraint, never re-opened*, and 30-01 registers `D ≈ 4.6416` as **verified**. But 30-04 Task 2 instructs posing "the D = 6.694 vs D ≈ 4.6416 conflict … UNSETTLED." If the author frames this as "which value is correct?", it contradicts the locked constraint and the verified register row, and the package reads self-contradictorily to the external agent. The correct (and intended) framing — "the value `D ≈ 4.6416` is locked; issue-03's `tau_L` derivation conflictingly uses 6.694; reconcile the *downstream derivation* given the locked value" — is not spelled out in the task.
- **[MEDIUM] `NS-12/13/18` coverage grep is brittle.** 30-04 Task 2 verify greps `grep -qF "NS-13"` and `grep -qF "NS-18"` individually, but every source doc (SPEC, RESEARCH, REQUIREMENTS) uses the shorthand `NS-12/13/18`. If the author follows that house style, the verify false-fails. It self-corrects toward the right behavior (separate questions) but via an implicit, confusing mechanism.
- **[MEDIUM] gsd-tools gate-open is under-specified and VC-10 is not diff-verifiable.** 30-05 Task 3 says record gate-open "via a gsd-tools state handler (e.g. `gsd-tools state …`)" without naming the handler/subcommand for an *external-gate-open* semantic, and VC-10 ("no direct STATE.md edit appears in the diff") cannot distinguish a gsd-tools-produced STATE.md diff from a Write-produced one. The real control is procedural; the automated check as written proves nothing.
- **[MEDIUM] Dual `D-NN` numbering is a latent confusion source.** `D-04/D-05/D-06` mean *implementation decisions* in CONTEXT (D-04 = one package, D-05 = zero repo paths, D-06 = inclusion criterion) and *issue-03 human-approval decisions* (causal mode / s_min / epsilon) in the questions domain. The plans disambiguate by parenthetical, but `grep -qF "D-04"` cannot tell them apart, and an external agent could conflate them. (Also note `D5` the stage-transition finding vs `D-05` the s_min decision both appear in the coverage set.)
- **[LOW-MEDIUM] Report-level "baseline-critique" grade vs claim-level SCOPE-12 locks.** `review_of_framework.md` mixes hard-constraint content (`eps_soft = 1e-5`, §2.2) with contested content (D-04 Option B, D-06 strategy). Grading the *whole* report "baseline design intent, critique freely" could invite challenge to a SCOPE-12-locked value. The SCOPE-12 preamble is the safety net, but the characterization/manifest applies the critique mandate wholesale without flagging the locked-within-baseline values.
- **[LOW-MEDIUM] `source_baseline` pin is self-contradictory.** 30-03 Task 3 says pin to "the current `milestone/v1.6` HEAD at assembly time **(the 30-01 recovery-tag commit)**" — but after 30-01/30-02 commit their artifacts, current HEAD ≠ the recovery-tag commit. Both reproduce the (unchanged) snapshots, so it's cosmetic, but it should be resolved to one definite commit for reproducibility (RESEARCH Open Question #4 recommended "actual HEAD at assembly time").
- **[LOW-MEDIUM] Manifest/attach-list completeness is not cross-checked against actual files.** Neither the master manifest (30-05 Task 1) nor the prompt attach list (30-05 Task 2) is verified against the real `research_package/` contents. A dropped row/attachment silently breaks self-containment — the very property this phase exists to guarantee.
- **[LOW] Neutrality is inherently manual-only.** `grep` confirms token presence, not the absence of leading framing. VC-08 ("both positions, no presupposed verdict") relies on author discipline + the 30-VALIDATION manual check. Acceptable for a doc phase, but the strongest acceptance criterion in the set is the least automatable.
- **[LOW] Empty "D-09 APPROVED" block could false-pass the status grep.** 30-01/30-02 make `grep -q "D-09 APPROVED"` pass via the *empty* block header; 30-02 Task 2's `grep -qE "Status:.*APPROVED"` will false-pass if the template seeds `Status: APPROVED` rather than a blank.
- **[LOW] Hardcoded absolute worktree path + possibly-stale HEAD hash in prose.** Plans hardcode `<home>/Desktop/3_body_problem-v1.6` (CONTEXT/REQUIREMENTS describe it as `../3_body_problem-v1.6`) and recite HEAD `4f260aa3` in prose; the executor should re-derive both at runtime (the verifies mostly do).
- **[LOW] DELIVERY-NOTE location diverges from the stated rationale.** 30-03 nests under `research_package/` "to match the v1.5 delivered form," but 30-05 Task 3 places `DELIVERY-NOTE.md` at the round root, whereas RESEARCH notes v1.5 placed the delivery note *inside* `research_package/`. The round-root placement is arguably *better* (clearer never-upload boundary) but is inconsistent with the "match v1.5" justification.

## 4. Suggestions

- **Resolve the uploaded claims register explicitly.** Add a task (in 30-04 or 30-05) that produces an **upload-safe claims register** as either a named companion (`claims-register.md`) or an explicitly-required master section, with `verified` rows citing **bare filenames** (e.g., "v1.5 verified-facts reference, CLM-10") rather than repo paths. Make its presence a hard acceptance criterion in 30-05, and add a verify that every `CLM-NN` referenced in `framed-research-questions.md` is *defined* in the uploaded register (`comm`/grep cross-check).
- **Fix the `pinn/` contradiction once, centrally.** Prescribe the safe phrasing in 30-04 Task 1/Task 2 and 30-05 Task 1 (e.g., "the live `pinn` implementation directory" / name `data-processing-pipeline-full.py` and `basic_architecture.py` bare), and either narrow the leak grep to path-shaped matches (e.g. `pinn/[A-Za-z]`) or add an explicit allowance note so the SCOPE-10 override survives. Audit the grep similarly for the legitimate prose "framework specs" (space) vs the banned `framework-specs/` (dir).
- **Decide single-master vs multi-companion now**, in 30-02's discussion record or the 30-03/30-04 frontmatter, and propagate the consequence: if folding, have 30-04 mark its outputs as fold-source (or 30-05 delete the redundant companions post-fold) and make the attach list match exactly.
- **Tighten the `D`-conflict framing in 30-04 Task 2.** State explicitly that the *value* `D ≈ 4.6416` is SCOPE-12-locked and must NOT be re-opened; only the reconciliation of issue-03's conflicting `tau_L`/`L_max` *usage* is the open question. This removes the apparent contradiction with the verified register row and keeps the question genuinely neutral without re-litigating a locked constant.
- **Make coverage greps shorthand-tolerant.** Replace per-token `grep -qF "NS-13"` with a check that tolerates `NS-12/13/18`, or add an explicit instruction "expand NS-12/13/18 to one question each." Apply the same care to the `D-04`/`D-05`/`D-06`/`D5` tokens given the dual-numbering collision.
- **Name the gsd-tools gate-open command and strengthen VC-10.** Identify the exact handler/subcommand for recording the external-gate-open state; replace the un-verifiable "no direct STATE.md edit in the diff" with a procedural assertion plus a check that the expected gate field/value is present in STATE.md after the handler runs.
- **Disambiguate the two `D-NN` schemes in any upload-class file** by referring to the issue decisions consistently (e.g., "Decision A: causal training mode") with the `D-04` tag in parentheses, so the external agent never has to know the internal CONTEXT numbering.
- **Add a self-containment cross-check to 30-05:** diff the manifest entries and the prompt attach list against `ls research_package/` (and `research_package/specs/`) so a dropped file fails the verify.
- **Resolve the `source_baseline` pin to one commit** (recommend: actual HEAD at 30-03 assembly time, post-recovery-tag), and have 30-01 Task 1 record that exact commit so 30-03 and 30-05 are consistent.
- **Note the locked-within-baseline values** in 30-01's characterization / 30-03's manifest annotation for `review_of_framework.md` (e.g., "baseline design intent, *except* `eps_soft = 1e-5` which is SCOPE-12-locked"), so the critique mandate cannot be read as inviting challenge to a hard constraint.

## 5. Risk Assessment

**Overall risk: MEDIUM.** The phase is genuinely low-risk in its hardest dimensions — it touches no executable code, edits no frozen/read-only file (snapshot + `cmp` + `git diff --quiet` discipline is solid), invents nothing, asserts no verdict, keeps the contested decisions open, and faithfully reuses a proven precedent with clean linear dependencies and correct human-gate modeling. What pulls it up from LOW is that the marquee deliverable — a *self-contained, repo-blind* package that hands off cleanly — has one real completeness gap (the uploaded claims register is never concretely produced, leaving `CLM-NN` references potentially dangling) and one self-contradiction baked into multiple tasks (`pinn/` override text vs. the repo-path leak grep), compounded by an undecided single-master/multi-companion structure that two dependent plans handle differently. None of these are deep design flaws; all are addressable with small, targeted pre-execution edits to 30-04 and 30-05 plus two verify-grep adjustments. With the HIGH items resolved, this drops cleanly to LOW.


---

## Cursor Review

# Cross-AI Plan Review: Phase 30 — Research Package Assembly

## 1. Summary

The Phase-30 plan set is a disciplined, well-structured 5-plan decomposition that faithfully mirrors the verified v1.5 Phase 23 precedent and correctly internalizes the milestone's hardest constraints: read-only/no-edit fidelity, no-invention framing of the open decisions, and the single most important v1.6≠v1.5 delta (no in-milestone verifier). The two human gates (recovery-tag, D-09 consolidation) are correctly modeled as blocking checkpoints, dependency ordering is clean and strictly sequential, and the repo-path-leak governance is correctly scoped to authored uploads only. The plans will very likely produce a conformant package — **but there is one structural gap that threatens PKG-07 in the default path (the uploaded claims register is never assigned to a plan), plus a cluster of coordination/consistency issues** (a structural form-decision deferred until after the files are already written, an orphaned verified-facts-reference file, an ambiguous `source_baseline` pin, and a lock-vs-open framing tension on `D` and `eps_soft`) that should be resolved before execution rather than improvised mid-flight.

## 2. Strengths

- **Clean, precedent-grounded decomposition.** Five plans (`30-01`..`30-05`) map 1:1 onto the verified v1.5 Phase 23 pattern (characterize+seed → consolidation gate → snapshots → questions → deliver), with correct `depends_on` and a strictly serial wave ordering. Each reused v1.5 artifact has a named template.
- **Both human gates are real blocking checkpoints.** `30-01` Task 1 (recovery-tag) and `30-02` Task 2 (D-09 consolidation) are `checkpoint:*` / `blocking-human`, and those two plans are correctly `autonomous: false`; assembly is gated on the recorded D-09 approval.
- **Strong read-only / frozen-file discipline.** `git diff --quiet` on both reports (`30-01` VC-03, re-confirmed in `30-03`), `cmp -s` snapshot==source (`30-03` VC-02), and Pitfall 4 enumerating every frozen file. Tampering threats are explicitly registered.
- **No-invention framing is well-internalized.** D-04/D-05/D-06 + the `D` conflict are posed "UNSETTLED" (`30-04` VC-08); the issue doc *and* its "Recommended Resolutions" are flagged non-authoritative; ERW rule 9 ("log silence, never invent") is propagated into `RESEARCH-AGENT-PROMPT.md` (`30-05` Task 2).
- **The no-Phase-24 delta is threaded correctly.** The D-17 boundary statement is transcribed verbatim into the register (`30-01` Task 3, VC-05), the "Phase-24 check" column is replaced by a FUT-flag, and the delivery note drops the "Phase 24 runs in parallel" section (`30-05` Task 3).
- **Repo-blindness is correctly scoped.** The zero-repo-path rule is enforced only on authored uploads (master/prompt/companions, VC-01), while intact snapshots and `consolidated-context.md` are correctly *exempted* (ERW rule 1 / D-10) — a subtle distinction the plans get right.
- **Destructive-git governance.** The orphaned recovery tag was caught empirically; `30-01` requires the three governance markers + explicit user approval for `git tag -f`, or a non-destructive fresh tag.
- **Commit hygiene.** Explicit `GIT_AGENT_OWNED_PATHS`, never `git add -A/-u`, no `--no-verify`, no push to the protected `milestone/*` branch, one atomic commit per plan.

## 3. Concerns

- **[HIGH] The uploaded claims register is unassigned — PKG-07 breaks in the CONTEXT-default (multi-companion) path.** `30-01` creates `30-CLAIMS-INVENTORY.md` as a `.planning/` phase artifact (**never uploaded**). `30-04` authors only three companions (`framed-research-questions.md`, `scope-12-hard-constraints.md`, `resolution-doc-skeleton.md`) — **no claims-register companion**. `30-05` mentions folding the register into the master *only* in the conditional "if the single-master form is chosen" clause, and its primary manifest enumeration ("6 specs + consolidated-context + the three 30-04 companions + master + prompt") omits it. So in the default multi-companion form, **no plan emits an uploaded claims register**: the inline `CLM-NN` references in the framed questions dangle, and the D-17 boundary statement is never communicated to the external research. This directly defeats PKG-07's "every figure stated in the package is marked claimed/verified."
- **[MEDIUM] The single-master vs multi-companion decision is deferred to `30-05`, but `30-04` has already committed to companions by writing the files.** `30-04` unconditionally creates three companion files; `30-05` Task 1 then says single-master-vs-companion is "Claude's discretion … final call at assembly." If single-master is chosen in `30-05`, you end up with both the committed companions (orphaned) *and* the folded master sections (duplicated content). A structural form decision cannot be made after the artifacts that depend on it are already written.
- **[MEDIUM] The standalone verified-facts reference is orphaned from the file lists.** CONTEXT recommends it standalone (the default). `30-01`'s artifact note attributes it to `30-04`; `30-03` Task 2 says *it* creates it ("If the user approved a SEPARATE standalone verified-facts reference, create it"); `30-04` does not create it; and it appears in **neither** `30-03`'s nor `30-04`'s `files_modified`/owned-paths, **nor** in `30-05`'s manifest. If approved at D-09 (the likely outcome), the file falls outside every plan's committed path set and the master manifest.
- **[MEDIUM] `source_baseline` pin is internally contradictory.** `30-03` Task 3 says pin to "the current `milestone/v1.6` HEAD at assembly time (the 30-01 recovery-tag commit)" — but `30-01` and `30-02` each commit before `30-03` runs, so assembly-time HEAD is two commits ahead of the recovery-tag commit. They are not the same ref. RESEARCH Open-Question 4 says pin to assembly-time HEAD; the parenthetical equating it with the recovery-tag commit is wrong and will confuse the executor (and any later `git show <source_baseline>:<path>` reproduction).
- **[MEDIUM] Lock-vs-open framing tension on `D` and `eps_soft` risks a self-contradictory package and a neutrality leak.** The SCOPE-12 preamble (`30-04` Task 1) lists `D ≈ 4.6416` and `eps_soft = 1e-5` as hard constraints that "must be respected and never re-opened," while `30-04` Task 2 simultaneously poses the **`D` conflict** and **D-06 epsilon strategy** as "unsettled." Without explicit delineation of *which sub-part is locked vs open*, the external research sees a contradiction ("D is locked / examine the D conflict"; "eps_soft is locked at 1e-5 / the epsilon strategy is open") and may be nudged to re-open a locked decision — the opposite-direction no-invention violation. The genuinely open part is *reconciliation/propagation under the locked value* (how `tau_L`/`L_max` re-derive under `D ≈ 4.6416`; whether a *second* `1e-10` context coexists with the locked loss `1e-5`), not "which value is correct."
- **[MEDIUM] Snapshot-fidelity verification doesn't cover the three framework specs.** `30-03` Task 1 re-confirms `git diff --quiet` only on the two reports, but it also snapshots `ctl_instruction.md`, `pinn_architecture.md`, and `sampling_method.md`, all of which the SPEC AC requires to be "zero edits." `cmp -s snapshot==source` proves the copy is faithful but does **not** prove the source itself was unmodified/clean. The three specs' immutability is assumed, not verified.
- **[MEDIUM] "SHA-256" vs "source commit hash" is conflated for `30-SNAPSHOT-HASHES.txt`.** The file format is described as `basename | canonical source path | source commit hash` (provenance), but the Validation Architecture table and the `30-01` threat model call it "SHA-256" / byte-fidelity proof. A commit hash does not by itself prove byte-for-byte content fidelity (that is actually proven by `cmp`/`git diff`). The artifact and the verification language disagree about what is being recorded.
- **[MEDIUM] Framed-question "framework-spec position" statements have no citation requirement.** `30-04` requires inline *figures* to reference `CLM-NN`, but the "current framework-spec position" prose for 15+ findings is an unverified paraphrase with no bare-filename/section anchor into the shipped snapshots — inviting paraphrase drift that reads as an asserted position (a soft no-invention risk). Phase 32 EVID-11 mandates line-range citations; the package framing has no analog.
- **[MEDIUM] Gate-open is verified only negatively, and the handler is unspecified.** `30-05` VC-10 checks "no direct STATE.md edit in the diff" — a no-op (doing nothing) also passes. There is no positive assertion that STATE now reflects gate-open, and the exact `gsd-tools` subcommand is left as "e.g. `gsd-tools state …`".
- **[LOW] No end-to-end manifest/self-containment cross-check.** Nothing verifies that every file in `research_package/` is listed in the manifest and every manifest bare-filename resolves to a shipped file. Such a check would have caught the missing claims register and the orphaned verified-facts file.
- **[LOW] Coverage greps are weak and `min_lines` floors are uncalibrated.** `30-04`'s `grep -qF` per token confirms a literal substring exists, not that a *neutral question* exists (e.g., `M6` could appear in passing). `framed-research-questions.md min_lines: 40` for 15+ findings × two positions each is far below the realistic size and provides no meaningful floor.
- **[LOW] PKG-05's "canonical source path + source commit hash per entry" is scattered.** The acceptance attribute is split across the never-uploaded `30-SNAPSHOT-HASHES.txt`, `30-CONSOLIDATION-PLAN.md`, and `DELIVERY-NOTE.md` — and the delivery note (`30-05` Task 3) is not actually required to carry a per-file source-path/commit table, so no single artifact unambiguously presents the full annotated list with paths.
- **[LOW] ALM-μ_p-clamp coverage is conditional with an unflagged downstream impact.** It is added to the questions only iff D-09 approves it (`30-04` Task 2); if declined, Phase 34 LOOP-05 has no resolution-doc verdict path. Defensible (settled INFO finding) but the downstream consequence isn't noted.
- **[LOW] Package nesting deviates from the cited v1.5 form without being flagged as a deviation.** `30-05` places `DELIVERY-NOTE.md` at the round root while v1.5 (per RESEARCH) placed it *inside* `research_package/`. Reasonable, but inconsistent with the precedent it cites.
- **[LOW] No final user-surface of the assembled master/prompt before gate-open.** After the D-09 gate, `30-03`/`30-04`/`30-05` run autonomously and `30-05` records the gate open; the actual uploaded artifacts are never explicitly surfaced for a "ready to upload?" confirmation. PKG-08's "reported to the user" is likewise satisfied only by the artifact + SUMMARY, not an active surface.

## 4. Suggestions

- **Assign the uploaded claims register explicitly (resolves the HIGH).** Make `30-04` emit a `claims-register.md` companion (a repo-path-scrubbed, upload-safe rendering of `30-CLAIMS-INVENTORY.md`, carrying the D-17 boundary statement), add it to `30-04` `files_modified`/owned-paths and to the `30-05` manifest. Add a positive verify that the register ships and that every `CLM-NN` referenced in `framed-research-questions.md` resolves to a row in it.
- **Lock the single-master vs multi-companion form before `30-04` runs.** Either commit to multi-companion up front (the CONTEXT default) and delete the single-master branch from `30-05` Task 1, or make `30-04` conditional. Decide it at the D-09 gate so the file set is known before any companion is written.
- **Pin down the verified-facts reference owner.** Resolve standalone-vs-folded at the D-09 gate, then put the resulting file (e.g., `verified-facts-reference.md`) in exactly one plan's `files_modified`/owned-paths and in the `30-05` manifest. Remove the duplicate ownership between `30-01`'s note and `30-03` Task 2.
- **Fix the `source_baseline` definition.** State plainly: `source_baseline` = `milestone/v1.6` HEAD at `30-03` assembly time; drop the "(the 30-01 recovery-tag commit)" equivalence. Optionally add a check that the snapshotted sources are byte-identical between the recovery-tag commit and assembly HEAD, and note it.
- **Add an explicit lock/open delineation for `D` and `eps_soft` in `30-04`.** For the `D`-conflict and D-06 questions, state the locked sub-part (cite SCOPE-12: `D ≈ 4.6416`; loss `eps_soft = 1e-5`) as fixed, and scope the open question to reconciliation/propagation (re-derivation of `tau_L`/`L_max`; whether a distinct `1e-10` *static/gate* context coexists) — never "which `D`/epsilon is correct." This protects both neutrality *and* the "never re-open" constraint.
- **Extend snapshot-fidelity verification to all six sources.** In `30-03`, run `git diff --quiet` (or working-tree-clean check) on `ctl_instruction.md`, `pinn_architecture.md`, and `sampling_method.md` too, to fully satisfy the "zero edits" AC.
- **Record both content hash and provenance, and align the wording.** Have `30-SNAPSHOT-HASHES.txt` carry a content `SHA-256` (byte-fidelity, per PKG-08) *and* the source commit (provenance), and make the validation/threat-model language match the format.
- **Require citations for spec-position prose.** In `30-04`, require each "current framework-spec position" statement to cite the shipped snapshot by bare filename + section (e.g., `ctl_instruction.md §2.5`) — repo-blind-safe and groundable, mirroring EVID-11 discipline.
- **Strengthen the gate-open and manifest checks.** Name the exact `gsd-tools` subcommand in `30-05` Task 3, and add a *positive* assertion that STATE reflects gate-open (not just "no direct edit"). Add a manifest-completeness sweep (every shipped file listed; every listed bare-filename shipped) as a final `30-05` check.
- **Tighten coverage verification.** Replace bare `grep -qF` token checks with per-finding heading checks (e.g., a `### <finding>` section per item) and raise/justify `min_lines` to a realistic floor; keep the manual VC-07 checklist as the authority.

## 5. Risk Assessment

**Overall risk: MEDIUM** (trending LOW once two or three plan edits land). The plan set's guardrails — read-only fidelity, no-invention framing, the no-Phase-24 boundary, and repo-path governance — are genuinely strong, and the dependency graph and human gates are sound, so the phase is unlikely to invent content, edit a frozen file, or leak repo structure. The risk is concentrated in **coordination/completeness seams between plans**: one HIGH gap where the uploaded claims register is not assigned to any plan in the default path (defeating PKG-07 as written), and a handful of MEDIUM issues (a structural form-decision deferred until after dependent files are written, an orphaned verified-facts reference, an ambiguous `source_baseline`, and the `D`/`eps_soft` lock-vs-open framing). None are architecturally fatal and all are fixable with small, local edits to the plan front-matter, task actions, and verify blocks before execution. The phase produces only documentation artifacts under explicit user gates, so the blast radius of any miss is low and recoverable; the primary exposure is shipping a package whose figure-grounding (claims register) or self-containment is incomplete, which the suggested manifest/coverage checks would catch deterministically.


---

## Antigravity Review

**Status: FAILED — could not be obtained in this environment (not a model verdict).**

The Antigravity CLI (`agy` 1.0.9) was requested and attempted six times but never produced
output. Diagnosis (documented, reproducible):

- `agy` takes its prompt **only as a command-line argument** (`-p "<prompt>"`); it does not
  read stdin.
- A **tiny** ASCII or Unicode prompt returns instantly (`PONG` smoke tests passed repeatedly).
- Any **review-sized** prompt (tested at 220 KB, 118 KB, and 85 KB) wedges at
  argument-ingestion: the process sits at **0 % CPU**, writes a **0-byte log**, produces no
  transcript, and never exits — its own `--print-timeout` does not engage because the stall
  precedes the model stream.
- Ruled out as causes: repo-workspace indexing (retried from `/tmp`), tool-permission
  blocking (`--dangerously-skip-permissions`), and Unicode in the argument (small-Unicode
  smoke test passed). The remaining discriminator is **prompt size** — the five plans alone
  are ~83 KB of text, above the threshold at which `agy -p` reliably stalls here.

This is an `agy` non-interactive large-argument limitation, not a defect in the plans. The
other five reviewers provide robust, diverse coverage (OpenAI, Alibaba, Google/Gemini, and two
Anthropic-family harnesses).

---

## Consensus Summary

Five reviewers (Codex, Qwen, opencode, Claude, Cursor) independently reviewed the five Phase-30
plans. Convergence is strong: every reviewer judged the decomposition sound, precedent-grounded
(faithful to the v1.5 Phase 23 analog), and well-governed, with **one dominant must-fix gap**
and a cluster of coordination/consistency issues to resolve before execution. Overall-risk
ratings split LOW (Qwen, opencode) vs MEDIUM (Codex, Claude, Cursor) — the split is about the
*severity/recoverability* of the claims-register gap, not its existence.

### Agreed Strengths (raised by 3+ reviewers)

- **D-09 consolidation gate correctly modeled as a hard blocking-human checkpoint** (all 5).
  Assembly is serialized behind a recorded approval; gate-bearing plans are `autonomous: false`.
- **Read-only / no-invention discipline enforced at multiple layers** (all 5): `cmp -s`
  snapshot==source, `git diff --quiet` on read-only reports, repo-path-leak greps on uploads.
- **The no-in-milestone-verification delta (D-17, v1.6 ≠ v1.5) threaded end-to-end** (all 5):
  verbatim boundary transcription, "Phase-24 check" column replaced by a FUT-flag, delivery-note
  section swapped.
- **Open decisions kept genuinely unsettled** (Codex, Qwen, Claude, Cursor): D-04/D-05/D-06 + the
  `D` conflict posed without presupposing a verdict; the issue doc AND its "Recommended
  Resolutions" flagged non-authoritative.
- **Clean, strictly-serial dependency ordering** with named v1.5 templates per artifact (Codex,
  Qwen, Claude, Cursor).
- **Recovery-tag pre-flight handled as a blocking destructive-git decision** with the three
  governance markers (Qwen, opencode, Claude, Cursor).

### Agreed Concerns (ranked by consensus + severity)

1. **[HIGH — Codex, Qwen, Claude, Cursor; implied by opencode] The uploaded claims register
   (PKG-07) is never assigned to a plan.** `30-CLAIMS-INVENTORY.md` is created as a `.planning/`
   phase artifact (never uploaded, full of repo paths). 30-04 authors three companions but no
   claims-register companion; 30-05 folds it in only conditionally and omits it from the primary
   manifest. In the CONTEXT-default multi-companion path, **no plan emits an uploaded register** —
   the inline `CLM-NN` references dangle and the D-17 boundary never reaches the external
   research. This is the unanimous top fix.
2. **[HIGH/MEDIUM — Codex, Qwen, Claude, Cursor] Gate-open / STATE.md handling in 30-05 is
   under-specified and only negatively verified.** The exact `gsd-tools` handler/subcommand is
   left as "e.g. `gsd-tools state …`"; VC-10 ("no direct STATE.md edit in the diff") is a no-op a
   do-nothing run also passes; Codex adds that committing the package before the STATE mutation
   leaves the state change uncommitted/outside owned paths.
3. **[MEDIUM — Qwen, opencode, Claude, Cursor] The single-master vs multi-companion form decision
   is made too late.** 30-04 unconditionally writes three companion files, but the form choice is
   deferred to 30-05 "Claude's discretion" — choosing single-master then orphans the
   already-written companions and duplicates content. Reviewers converge on resolving this at the
   D-09 gate (or in 30-03), before the dependent files exist.
4. **[HIGH — Codex, Claude] The `pinn/` override statement contradicts the repo-path-leak grep.**
   Plans require uploads to state the SCOPE-10 `pinn/` override, but the same uploads are verified
   with `! grep … pinn/ …` (e.g. `30-05-PLAN.md` line 78 requires the master preamble to state
   the override; line 81 greps the master rejecting the literal `pinn/`). A careful executor
   rephrases ("the live PINN implementation files"); a careless one deletes the
   governance-required override to pass the grep. *(Divergent: Qwen and opencode praised this grep
   as a strength without noticing the collision — see Divergent Views.)*
5. **[MEDIUM — Claude, Cursor] Lock-vs-open framing tension risks re-opening a locked value (the
   opposite-direction no-invention violation).** The SCOPE-12 preamble lists `D ≈ 4.6416` (and
   `eps_soft = 1e-5`) as hard, never-reopen constraints, while 30-04 simultaneously poses the `D`
   conflict (and D-06 epsilon strategy) as "unsettled." Both warn this reads self-contradictorily;
   the genuinely-open part is *reconciliation/propagation under the locked value* (re-deriving
   `tau_L`/`L_max`; whether a separate `1e-10` context coexists with the locked loss `1e-5`), not
   "which value is correct." Must be spelled out so the package neither asserts nor re-opens.
6. **[MEDIUM — Codex, Claude, Cursor] Framed-question grounding/citation discipline + claims-seed
   completeness.** Inline figures must cite `CLM-NN`, but the per-finding "current framework-spec
   position" prose has no bare-filename/section anchor into the shipped snapshots (paraphrase-drift
   risk); and the 30-01 claims seed (RESEARCH C-1..C-13) precedes the full issue-03 read in 30-04
   with no register-extension step (a numeric/figure sweep against issue-03 is recommended).
7. **[MEDIUM — Codex, Cursor] `source_baseline` pin is internally contradictory** — 30-03 equates
   "assembly-time HEAD" with "the recovery-tag commit," but 30-01/30-02 commit in between, so they
   are different refs (breaking `git show <baseline>:<path>` reproduction). Define separate values
   for the snapshot source baseline and the final package commit.
8. **[MEDIUM/LOW — Codex, Cursor] `30-SNAPSHOT-HASHES.txt` conflates SHA-256 (byte-fidelity) with
   source-commit hash (provenance)** — the format records a commit hash while the verification
   language claims byte-for-byte proof; those are different guarantees. Clarify the schema
   (`basename | source path | file sha256 | source commit | notes`).
9. **[MEDIUM/LOW — opencode, Qwen] 30-03's snapshot list is hardcoded but the document set is
   decided at the D-09 gate** — if the user alters the list, the hardcoded copy/verify diverges;
   make 30-03 read the approved list from the D-09 record.

### Notable single-reviewer findings worth keeping

- **Codex [HIGH] — spec over-hardening:** treating *all* current framework-spec content (beyond
  the locked v1.4/v1.5 outcomes) as a hard constraint risks grading revisable doc-03 spec
  positions as non-revisable; only the locked outcomes should be hard, the rest is baseline
  evidence.
- **Cursor [MEDIUM] — orphaned verified-facts reference:** the standalone v1.5-verified-facts file
  is attributed to 30-04 in one place and 30-03 in another, appears in neither plan's owned-paths,
  and is absent from the master manifest — if approved at D-09 it falls outside every committed
  path set.
- **Cursor [MEDIUM] — spec-source immutability assumed, not verified:** `cmp -s` proves the
  snapshot copy is faithful but not that `ctl_instruction.md` / `pinn_architecture.md` /
  `sampling_method.md` sources were themselves unmodified; only the two reports get
  `git diff --quiet`.
- **Cursor [LOW] — no end-to-end manifest/self-containment cross-check:** nothing verifies every
  `research_package/` file is in the manifest and every manifest filename resolves — such a check
  would have caught finding #1 and the orphaned reference.
- **opencode [LOW] — excluded-finding leak:** if the user drops the ALM-clamp finding at D-09, the
  external agent may still find it in raw issue-03 and adjudicate it; the preamble should list
  deliberately out-of-scope findings.

### Divergent Views

- **The `pinn/`-override-vs-grep collision (concern #4):** Codex and Claude flag it HIGH; Qwen and
  opencode independently praised the *same* repo-path grep as a clean strength without noticing
  that the plans also require the literal token `pinn/` in those files. Verification against the
  plans confirms the collision is real. The optimistic reviewers missed it; the fix is to mandate
  non-literal phrasing of the override.
- **Overall risk LOW vs MEDIUM:** Qwen and opencode rate the set LOW, treating the claims-register
  gap as a recoverable missing-deliverable that surfaces naturally at assembly. Codex, Claude, and
  Cursor rate it MEDIUM, judging that gap (plus the gate-open and form-decision issues) capable of
  producing a non-compliant or self-contradictory package if executed as written. The disagreement
  is about recoverability, not the findings.

### Recommended pre-execution actions (synthesis)

Before executing Phase 30, resolve the five convergent items: (1) assign an upload-safe
claims-register companion, including its repo-path→bare-filename citation translation; (2) specify
the exact `gsd-tools` gate-open handler and make VC-10 a positive assertion; (3) lock the
single-master-vs-companion form at the D-09 gate, before 30-04 writes files; (4) mandate
non-literal `pinn/` phrasing in uploads so the leak grep passes without dropping the SCOPE-10
override; (5) delineate locked-vs-open sub-parts for `D` / `eps_soft` so neutrality framing does
not re-open a locked value. Feed these back via `/gsd-plan-phase 30 --reviews`.

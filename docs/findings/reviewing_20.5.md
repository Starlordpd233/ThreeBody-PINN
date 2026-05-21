  Code Review — Phase 20.5 Adversarial-Review Fix Verification

  Scope: commit b727b15 on milestone/v1.4 (parent b8688a3f); 2 files, +1445 lines, both new documents.
  Intent: Verify the commit's claim that it resolves all 3 BLOCK and 7 FLAG findings from
  docs/superpowers/reviews/2026-05-19-phase-20-5-adversarial-review.md, and faithfully implements
  Option A from docs/findings/addressing_sobol_sequence_suggestion.md.
  Mode: Interactive
  Reviewer team:
  - correctness (always-on) — verify each claimed fix actually resolves its finding
  - maintainability (always-on) — cross-doc and within-doc consistency
  - project-standards (always-on) — CLAUDE.md v1.4 governance compliance
  - Skipped: adversarial (file-type awareness — markdown-only), testing (probe not yet executed),
  agent-native (no agent surfaces in spec docs), stack-specific (no code)

  Headline: ✅ All 10 claimed fixes ARE present and resolve their findings. ⚠️ The fixes left 3 P1
  cross-document inconsistencies between the design doc and the plan doc that will mislead a future
  agent or reader.

  ---
  Verified Claims (the "good" half)

  The reviewers independently confirmed:

  - All 3 BLOCK findings addressed. BLOCK-1 (gap count 14), BLOCK-2 (probe now tests allocation order
  via _process_sobol_batch with synthetic batch + assertions on column 3 → scale and 4–6 → velocity),
  BLOCK-3 (§2.1 "6 additional dimensions" qualified to no-scale case only).
  - All 7 claimed FLAG findings addressed. FLAG-1 (rotate=False scoping in both design §3.1 and plan
  Edit 2), FLAG-2 (SCOPE-05 narrowed to ic_generation/), FLAG-3 (sub-conflict #1 reclassified
  "contradictory in outcome distribution" with FUT-01 follow-the-code guidance), FLAG-4 (Success
  Criterion 2 narrowed), FLAG-6 (s_min used as inline-code, not as $s_{\min}$ LaTeX symbol), FLAG-8
  (GAP-20-5-03 reclassified "operational coordination"), FLAG-10 (post-completion cross-ref re-verify
  note in both docs and plan's Follow-ups).
  - Option A faithfully implemented in Plan Task 4 Edits 1–5: u_1–u_3 position, u_4 scale, u_5–u_7
  velocity for standard config; d = 3 + δ_s + 3δ_v formula; v_i = Φ⁻¹(u_{3+δ_s+i}) shifted formula.
  - FROM text in Edits 1–5 is verbatim from
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md (the correctness reviewer
  spot-checked lines 6, 90, 94–98, 108–111, 113–119).
  - FLAG-5 and FLAG-9 omissions are correct — the adversarial review itself said "no fix needed" for
  both.

  ---
  P1 — High (block plan execution / mislead readers)

  #: 1
  File: docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md (6 occurrences: §D6 row,

    §5.3 heading + binding text, §5.3 post-phase task line, "Next steps" item 5)
  Issue: Design doc still calls the new rule SCOPE-D throughout; plan uses SCOPE-05. The plan's
    Self-Review §1 line 921 acknowledges the rename but the design was never updated. A reader landing
    on the design doc grep-finds zero hits for SCOPE-05.
  Reviewer(s): maintainability
  Conf: 100
  Route: manual → human
  ────────────────────────────────────────
  #: 2
  File: design §5.1 (lines 281–291) vs plan Task 1 Step 4 (lines 107–112)
  Issue: Success Criteria drift. Design enumerates 5 criteria; plan writes 4 to ROADMAP.md (criterion 3

    widened from GAP-20-5-01 to GAP-20-5-01/02/03; criteria 4+5 merged). The plan is what lands in
    ROADMAP; the design is the rationale of record. They should agree on "phase done."
  Reviewer(s): maintainability + correctness ×2 (cross-reviewer agreement)
  Conf: 100
  Route: manual → human
  ────────────────────────────────────────
  #: 3
  File: design §6 (lines 402–405) vs plan Task 6 (lines 739–742)
  Issue: AC-SAMP-01 pass criterion contradicted. Design says pass criterion finalized in Phase 21 once
    sample size is chosen. Plan writes a fully-finalized 6-line PASS spec now with fixed n_rows =  5. A

    future Phase-21 agent reading the design will look for an unfinished AC; reading the plan will find

    it already finalized.
  Reviewer(s): maintainability
  Conf: 75
  Route: manual → human

  P2 — Moderate

  #: 4
  File: design §5.4 line 333 + §5.5
  Issue: GAP-20-5-02/03 record bodies live only in the plan. Design §5.4 says "see the implementation
    plan, Task 3, for the GAP-20-5-02/03 records" — but per CLAUDE.md the design (decision artifact)
    should be self-contained, not require reading the execution artifact for the audit trail.
  Reviewer(s): maintainability
  Conf: 100
  Route: manual → human
  ────────────────────────────────────────
  #: 5
  File: plan Task 4 (line 412), Task 8 (line 851)
  Issue: SCOPE-05 propagation to CLAUDE.md happens AFTER risk-elevated spec edits. Task 4 commits
    citations to ic_generation_utils.py BEFORE Task 8 propagates the SCOPE-05 carveout into root
    CLAUDE.md. The chain is valid via GAP-20-5-01's RESOLVED-WITH-INSTRUCTION, but a reviewer of the
    Task 4 commit reads CLAUDE.md and sees only the unqualified no-live-code directive. Reorder Task 8
    (or its CLAUDE.md edit) before Task 4, or add the GAP forward-ref to Task 4's commit message.
  Reviewer(s): project-standards
  Conf: 75
  Route: manual → human
  ────────────────────────────────────────
  #: 6
  File: design §5.5 lines 342–343 (line-numbered) vs plan Task 3 Step 1 lines 271–272 (section-only)
  Issue: GAP-20-5-01 Where in artifact citations drifted. Design cites §1.1 (line 90), etc.; plan drops

    line numbers. The plan's form lands in the committed gap register; the design's line-numbered form
    becomes orphaned after Phase 20.5 execution shifts line positions.
  Reviewer(s): maintainability
  Conf: 75
  Route: manual → human
  ────────────────────────────────────────
  #: 7
  File: design §9 (lines 479–497)
  Issue: Verification summary §9 does not mention the upgraded probe's allocation-order coverage.
  Design
     §6 (post-BLOCK-2 fix) describes the probe testing both dimension and allocation; §9 was not
  updated
     to match. Minor internal incongruity within the design doc.
  Reviewer(s): maintainability
  Conf: 75
  Route: manual → review-fixer
  ────────────────────────────────────────
  #: 8
  File: design §5.6 line 378
  Issue: Hanging reference to originally-planned 20-5-CODE-DIVERGENCE.md. No prior reference
  establishes
     the original name; readers see a dangling provenance comment. Combine with #4 by adding the
    GAP-20-5-03 record body (with operational coordination classification) and dropping or rephrasing
    this clause.
  Reviewer(s): maintainability
  Conf: 75
  Route: manual → review-fixer

  P3 — Low

  #: 9
  File: plan Task 6 (lines 714–717), 20-5-DATA-ALIGNMENT.md content
  Issue: FLAG-7 (dataset provenance) not addressed. The 20-5-DATA-ALIGNMENT.md template asserts the
    existing dataset was generated under this convention with no cited log/commit/manifest. The commit
    message correctly does not claim FLAG-7 is addressed, but the assumption is load-bearing for
    AC-SAMP-01 and warrants an explicit "Provenance assumption" caveat.
  Reviewer(s): correctness
  Conf: 75
  Route: manual → review-fixer
  ────────────────────────────────────────
  #: 10
  File: plan Task 3 Step 1 (266–348)
  Issue: 20-5-GAPS.md entries omit the Documents to review field established by the Phase 17 register
    precedent. Especially for GAP-20-5-01 (HIGH), the omission removes the curated citation set future
    agents need for re-verification.
  Reviewer(s): project-standards
  Conf: 75
  Route: manual → human
  ────────────────────────────────────────
  #: 11
  File: plan Task 3 Step 1 (253–262)
  Issue: 20-5-GAPS.md frontmatter omits slug and governance fields present in Phase 17's precedent
    frontmatter. The governance field would be especially valuable here because GAP-20-5-01 depends on
    the SCOPE-05 carveout.
  Reviewer(s): project-standards
  Conf: 75
  Route: manual → human
  ────────────────────────────────────────
  #: 12
  File: plan Task 3 (GAP-20-5-02 line 315–316; GAP-20-5-03 line 339)
  Issue: GAP-20-5-02 and GAP-20-5-03 grounding marked n/a. CLAUDE.md §STOP Protocol step 3 requires
    articulating why this gap is consequential, not just that the source is silent. A one-sentence
    engineering rationale (e.g., "AC names form a stable namespace used in Phase 21's verification
    suite; introducing a new prefix without surfacing risks namespace collision...") would satisfy
    intent.
  Reviewer(s): project-standards
  Conf: 75
  Route: manual → human
  ────────────────────────────────────────
  #: 13
  File: plan Task 8 Step 2 (882–890)
  Issue: Task 8 stages files via <files-modified-by-gsd-docs-update> placeholder without an explicit
    "enumerate manifest then git-add each path" step. Tighten by adding: "Run git status --short,
  verify
     the list matches the skill's reported manifest, then git add each path explicitly."
  Reviewer(s): project-standards
  Conf: 75
  Route: manual → review-fixer

  ---
  Pre-existing

  None — commit only adds new files.

  Coverage

  - Suppressed: 1 finding at anchor 50 (ps-006 — empty probes/ directory, P3, acceptable as written).
  - Mode-aware demotion suppressions: 0.
  - Untracked files excluded: docs/superpowers/plans/2026-05-19-delete-v13-closure-audit.md (separate
  work), docs/superpowers/reviews/2026-05-19-phase-20-5-adversarial-review.md (the review itself —
  already on disk, untracked from this commit's perspective).
  - Failed reviewers: 0 of 3.
  - Skipped always-on personas: testing, agent-native, learnings-researcher (instruction-prose,
  single-purpose verification).
  - Run artifact: /tmp/compound-engineering/ce-code-review/20260520-030810-90da33f5/

  ---
  Verdict — Ready with fixes

  The commit's core claim is sound: the 3 BLOCK + 7 FLAG findings it lists are actually addressed, and
  Option A is faithfully implemented. However, the fixes were applied asymmetrically to the design doc
  and plan doc — notably leaving 6 SCOPE-D references in the design, drifting Success Criteria between
  the two, and embedding a now-contradictory "Phase 21 finalizes the pass criterion" claim in the
  design when the plan has already finalized it. These are P1 because a future agent executing Phase
  20.5 reads the plan, while a reviewer auditing the decision reads the design — and the two will
  disagree.

  Fix order if you address them:
  1. #1 Replace SCOPE-D → SCOPE-05 throughout design doc (mechanical; deterministic) — safe_auto
  candidate
  2. #2 Reconcile Success Criteria between design §5.1 and plan ROADMAP block (decision: 4 or 5?)
  3. #3 Reconcile AC-SAMP-01 pass-criterion timing (decision: finalized now or in Phase 21?)
  4. #4, #8 Add GAP-20-5-02/03 record bodies to design §5.5; drop the "originally-planned" hanging
  clause
  5. #5 Reorder SCOPE-05 propagation (Task 8 before Task 4), OR amend Task 4's commit message with the
  GAP forward-ref
  6. #6, #7, #9, #10, #11, #12, #13 — small schema/discipline tightenings before Phase 20.5 execution


    Final Summary

  /ce-code-review — Phase 20.5 fix verification

  Verdict: Ready with fixes. The commit's headline claim is sound — all 10 claimed adversarial-review
  fixes (BLOCK-1/2/3 + FLAG-1/2/3/4/6/8/10) are actually present and resolve their findings, and Option
   A from docs/findings/addressing_sobol_sequence_suggestion.md is faithfully implemented in Plan Task
  4. FROM text in Edits 1–5 is verbatim from sampling_method.md. FLAG-5 and FLAG-9 omissions are
  correct per the review's own recommendations.

  But the parallel fixes drifted between the two docs. Three P1 inconsistencies the review surfaced —
  these will mislead an executing agent or auditing reviewer:

  ┌─────┬───────────────────────────────────────────────────────────────────────────┬──────────────┐
  │  #  │                                   Issue                                   │    Where     │
  ├─────┼───────────────────────────────────────────────────────────────────────────┼──────────────┤
  │     │ Design doc still uses SCOPE-D (6 occurrences in §D6 row, §5.3 heading +   │              │
  │ 1   │ binding text, §5.3 post-phase, "Next steps" item 5); plan uses SCOPE-05   │ design doc   │
  │     │ everywhere. Hanging identifier the design doc Self-Review acknowledged    │ only         │
  │     │ but the design was never updated.                                         │              │
  ├─────┼───────────────────────────────────────────────────────────────────────────┼──────────────┤
  │     │ Success Criteria drift — design enumerates 5, plan writes 4 to ROADMAP    │ design §5.1  │
  │ 2   │ (criterion 3 widened to GAP-20-5-01/02/03 plural; criteria 4+5 merged).   │ vs plan Task │
  │     │                                                                           │  1 Step 4    │
  ├─────┼───────────────────────────────────────────────────────────────────────────┼──────────────┤
  │     │ AC-SAMP-01 pass criterion — design §6 says "finalized in Phase 21 once    │ design §6 vs │
  │ 3   │ sample size is chosen"; plan Task 6 writes a fully-finalized 6-line PASS  │  plan Task 6 │
  │     │ spec with n_rows = 5.                                                     │              │
  └─────┴───────────────────────────────────────────────────────────────────────────┴──────────────┘

  Plus 5 P2 (gap-record placement, line-number drift, missing §9 update, "originally-planned" hanging
  ref, SCOPE-05 propagation ordering) and 5 P3 (FLAG-7 dataset provenance unacknowledged,
  Phase-17-precedent frontmatter fields missing, etc.). Full table is in the report above; artifact at
  /tmp/compound-engineering/ce-code-review/20260520-030810-90da33f5/.

  Recommended fix order before Phase 20.5 execution:
  1. Replace SCOPE-D → SCOPE-05 throughout the design doc (mechanical).
  2. Reconcile Success Criteria (decide: 4 or 5 criteria?).
  3. Reconcile AC-SAMP-01 pass-criterion timing (decide: finalized now or in Phase 21?).
  4. Backport the GAP-20-5-02/03 record bodies into design §5.5 + drop the hanging "originally-planned"
   clause.
  5. Decide on the SCOPE-05 ordering: either reorder Task 8 ahead of Task 4, or add a GAP-20-5-01
  forward-reference to Task 4's commit message.

  /gsd-docs-update — committed as a9ecd51

  3 targeted updates, 5 insertions, narrow scope per your "do not invent updates" guidance:

  - .planning/PROJECT.md — Added a Key Decisions row for the Phase 20.5 design+plan lock (Option A,
  SCOPE-05 introduction, execution-pending status). Footer bumped to 2026-05-20.
  - .planning/STATE.md — Added a Roadmap Evolution entry alongside the existing Phase 15.1 insertion
  notes.
  - .planning/MILESTONES.md — Added Phase 20.5 to the v1.4 phases-planned summary and
  next-workflow-step list.

  Deferred (would have re-created the same ordering problem code review finding #5 flagged):
  - CLAUDE.md / AGENTS.md / GEMINI.md / ANTIGRAVITY.md — Their (Phases 17, 18, 19, 20, 21) enumeration
  and SCOPE-05 mention belongs in plan Task 8, after Task 1 lands Phase 20.5 in ROADMAP and Task 2
  lands SCOPE-05 in REQUIREMENTS.
  - .planning/ROADMAP.md, .planning/REQUIREMENTS.md, .planning/milestones/v1.4-GAPS.md,
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md — Owned by plan Tasks 1–4 at
  execution time.
  - README.md — generic, no v1.4 phase references.

  Recommended next steps (for you to choose)

  1. Address the 3 P1 design↔plan inconsistencies in commit b727b15 (a separate amend or follow-up
  commit on the design/plan docs) so Phase 20.5 execution doesn't trip on stale SCOPE-D references or
  contradictory Success Criteria.
  2. Then execute Phase 20.5 plan — superpowers:executing-plans or
  superpowers:subagent-driven-development on
  docs/superpowers/plans/2026-05-19-phase-20-5-sampling-coordinate-allocation.md. Task 8 there will
  itself invoke /gsd-docs-update to propagate SCOPE-05 into CLAUDE.md once REQUIREMENTS.md has it.
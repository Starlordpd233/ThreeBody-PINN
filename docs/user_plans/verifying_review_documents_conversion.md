  Prompt:

  You are performing an independent verification of Phase 9 — an
  issues directory consolidation in this project. You have no
  prior knowledge of this phase, so read everything below
  carefully before beginning.

  What Phase 9 Did

  Seven scattered audit/issue files in
  pinn_instruction/original_latex/review-of-framework/issues/
  were archived into an archive/ subdirectory. Their findings
  were synthesized into three thematic Markdown documents
  organized by system layer. The goal was reorganization only —
  no new analysis, no changed conclusions, no dropped findings.
  Everything unique from the originals must be present in at
  least one new doc.

  Your Verification Methodology: Sequential Document-by-Document
  Build-Up

  Work through the 7 archived documents one at a time, in this
  exact order. For each original:

  1. Read the original fully — understand every finding, formula,
   code snippet, and claim
  2. Use MIGRATION.md to find which destination doc(s) and
  sections map to each original section
  3. Read the corresponding destination section(s) in the new
  docs
  4. Verify three things:
    - Completeness: Was anything from the original dropped or
  silently deleted?
    - Accuracy: Were formulas, numbers, and technical claims
  transcribed correctly? Ground every mathematical claim in
  computation — don't trust numbers at face value
    - Attribution: Was the finding placed in the right thematic
  doc? Does the severity label match?
  5. Carry knowledge forward — when you move to the next
  original, you already know what the earlier originals
  contributed. This lets you spot: (a) duplicated content that
  should have been deduplicated, (b) cross-references that are
  now broken, and (c) findings that split across docs but don't
  reconcile with each other

  After all 7 originals: Do a final pass checking the 3 new docs
  for internal consistency — do cross-links resolve? Do findings
  that reference each other across docs agree on values?

  Files to Read (In Order)

  Start with the planning context (brief):
  1. .planning/phases/09-issues-directory-consolidation/09-CONTEX
  T.md
  2.
  .planning/phases/09-issues-directory-consolidation/MIGRATION.md
   — this is your map

  The 3 destination docs (skim first for structure, then
  deep-read as you go):
  3. pinn_instruction/original_latex/review-of-framework/issues/0
  1-architecture-and-physics-foundations.md
  4. pinn_instruction/original_latex/review-of-framework/issues/0
  2-data-pipeline-and-validation.md
  5. pinn_instruction/original_latex/review-of-framework/issues/0
  3-curriculum-and-training-loop.md

  The 7 archived originals (verify one-by-one, in this order):
  6.
  archive/three_body_pinn_pre-implementation_audit_2026-04-27.md
  — the main audit, 11 critical + 16 major + 10 design
  ambiguities
  7. archive/Causal_Trainingmismatch_resolution_blueprint.md —
  causal training, dual-epsilon, temporal resolution
  8. archive/Issue_on_data_validation_protocol_and_compatbility_w
  ith_project_context.md — 6-gap analysis
  9. archive/review.md — AD chain-rule factor, scaling contract
  10. archive/stage-assignment-issue.txt — PCA + K-means adaptive
   staging
  11. archive/next-step-for-data-processing-pipeline.txt — file
  format, I_norm inconsistency, author comments
  12. archive/next steps.txt — tau_L/L_max formulas,
  compute_globals, softening analysis, normalization table

  Specific Things to Check

  Mathematical claims to verify independently (compute them
  yourself):
  - D formula: D = (G * M_tot * T^2)^(1/3) with G=1, M_tot=3,
  T=10 → should be 6.694. Check whether the docs correctly
  describe what the original CTL and PINN documents said
  - SIREN init variance ratio: 30^4 = 810,000x — verify
  - AD chain-rule: d/du = 2d/dτ, d²/du² = 4d²/dτ² — verify
  against the actual physics
  - L_norm formula: L_max = M_tot * r_char * v_char — verify the
  code in docs matches this
  - Dataset gap stats: standard 1250/4000, hierarchical 143/5000,
   gold 184 missing — verify arithmetic
  - dt_out ratios: 0.17/0.01 = 17x — verify
  - Softening at r=0.001 with eps=1e-5 vs eps=1e-10 — verify the
  ~1% potential difference claim
  - I_3 normalization: if I_max = I_3 (largest distance), then
  I_3/I_max is always 1.0 — verify the docs handle this correctly

  Structural checks:
  - The three new docs total ~109 KB while the 7 originals
  totaled ~246 KB. This size reduction is partly intentional
  (deduplication), but verify nothing substantive was lost
  - Check that verbatim sections (audit Section 5 input vector
  spec in doc 01, audit Section 6 batch construction in doc 03)
  are actually verbatim
  - Check that the 5 DECISION-NEEDED callouts are distributed
  correctly: 2 in doc 01, 1 in doc 02, 2 in doc 03 (verify the
  actual count)
  - Check that MIGRATION.md's claimed 86 mapped sections is
  accurate
  - Check that cross-references between the 3 new docs are valid
  (files exist, section names make sense)

  Known correction to be aware of: A fix was already applied in
  commit 265c0fe correcting B-02's D formula description (from
  "two contradictory formulas" to "same wrong formula in both
  docs") and L_norm impact (97% → 108%). Verify that fix is
  present and check whether there are other errors like it that
  haven't been caught.

  Output Format

  Write your findings to .planning/phases/09-issues-directory-con
  solidation/09-VERIFICATION-REPORT.md with this structure:

  # Phase 9 Verification Report

  ## Summary
  - Overall verdict: PASS / FAIL / PASS WITH CONCERNS
  - Number of issues found: X critical, Y moderate, Z minor

  ## Per-Original Verification

  ### Original:
  three_body_pinn_pre-implementation_audit_2026-04-27.md
  - Sections checked: N
  - Findings verified: all present / X missing / Y misplaced
  - Math errors found: [list or "none"]
  - Notes: ...

  [repeat for all 7 originals]

  ## Mathematical Verification
  [Each claim listed above with your independent computation
  result: CORRECT or WRONG with explanation]

  ## Structural Verification
  [size analysis, verbatim copy check, DECISION-NEEDED count,
  cross-link validation]

  ## Unresolved Issues
  [Any findings that require human judgment to classify]

  Work through this methodically. The document-by-document
  sequential build-up is critical — each original builds your
  knowledge base for evaluating the next. Don't skip originals
  and don't jump between them randomly.

  ---
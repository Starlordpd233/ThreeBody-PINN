---
phase: 34
reviewers: [codex, opencode, claude, claude-minimax, claude-jiekou]
rerun_reviewers: [codex, opencode, claude, claude-minimax, claude-jiekou]
reviewed_at: 2026-06-25T05:40:55Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260625T053720Z-93929
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 34

## codex Review

## 1. Summary

The Phase 34 plans are coherent, well-sequenced, and largely achieve the phase goal: transcribe adjudicated LOOP-01..08 and SI-PINN-003 contracts into the two allowed framework specs, preserve deferred decisions as deferred, verify the result, and close the relevant Phase 32 ledger rows only after checks pass.

No listed file failed to read. I found no HIGH blocker.

## 2. Strengths

- Clear dependency ordering: `34-01` creates packet/baseline prerequisites before any spec edit; `34-05` verifies before ledger closure.
- Strong scope control: plans repeatedly guard against editing frozen specs, read-only reports, live `pinn/` code, generated data, and user-owned `.planning/STATE.md`.
- Good anti-fabrication handling: source-silent batch edge cases are routed to `GAP-34-01` instead of being filled with defaults.
- Good data-integrity controls: ledger SHA freshness guard, preserved verdicts, explicit transition logs, and protected-path checks.
- Strong handling of superseded roadmap wording: plans explicitly follow adjudicated SPEC/resolution/ledger outcomes over stale preview text.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

**HIGH:** None.

**MEDIUM:** Some final verification checks are still broader than the plans’ stated “discriminating exact phrase” standard. `34-VALIDATION.md` and `34-05` include useful exact checks, but several per-requirement checks still rely on whole-file tokens like `ALM`, `optional`, `deferred`, `IPR`, `PSC`, `provisional`, and `VAL-0`. These could false-pass if old or nearby text contains the words without the intended Phase 34 contract landing correctly.

**LOW:** The plans correctly gate closure on `GAP-34-01`, but they also close related ledger rows to `VERIFIED`. That is defensible because the deferral transcription is what Phase 34 verifies, but execution summaries must keep saying “phase closure blocked pending user resolution/deferral” so `VERIFIED` rows are not mistaken for full phase completion.

**LOW:** STOP-gap completeness validation is mostly covered by `34-05`, but `34-VALIDATION.md` only runs the field check conditionally when an OPEN gap is detected. If gap status formatting drifts, the validation file alone may not catch it.

## 4. Suggestions

- Tighten final per-requirement checks to anchor each LOOP/SI item to its Phase 34 callout, status tag, citation, and target section, not just whole-file token presence.
- In `34-VERIFICATION.md`, make the overall verdict explicitly “blocked pending GAP-34-01 resolution/deferral” until the user resolves or defers it.
- Make the `GAP-34-01` presence/index/count check unconditional after `34-03` has run.

## 5. Overall Risk

**MEDIUM**. The plan architecture is strong, but the final gate needs slightly sharper token anchoring to avoid a false-positive verification pass.

---

## opencode Review

Let me read a few supporting files to verify concerns.
Let me check one more thing — the RESEARCH file's relevant section and verify the ROADMAP staleness claim.
# Phase 34 Plan Review

## 1. Summary

Five plans (34-01 through 34-05) implementing training-loop and batch-construction spec contracts (LOOP-01..08 + SI-PINN-003) across `ctl_instruction.md` and `pinn_architecture.md`. The architecture is sound: packet-before-edit, sequential dependency graph with wave grouping, comprehensive automated verification, and proper STOP-gap discipline for source-silent decisions. All plans correctly identify and work around the known ROADMAP/REQUIREMENTS superseded preview wording.

## 2. Strengths

- **Exhaustive prohibition checks** — `8.5`, duplicated mechanism formulas, LOOP-06 probe-able formulas, and SI-PINN-003 remnant strings all have negative-token guards with `rg`/`python3` checks.
- **Concurrency guard** — `ledger_post_34_01_sha256` in 34-05 provides a SHA-256 freshness check before any ledger write, preventing silent overwrites.
- **Closure gating** — Phase 34 explicitly refuses to close over `GAP-34-01`, recording the OPEN gap as a blocker requiring user resolution/deferral.
- **Re-verify-after-every-batch** — LOOP-04 (c)/(d)/(e) re-runs after every batch editing either half, preventing cross-file drift from accumulating.
- **Dirty-doc preservation** — dynamic SHA-256 capture of user-owned changes (STATE.md) with a documented divergence path.

## 3. Concerns

### HIGH
- **v1.6-GAPS.md frontmatter will be stale**: Current `total_gaps: 6, open_gaps: 0` — 34-03 must update these counts when GAP-34-01 is opened, and 34-05 must verify the update. Plan 34-03 says "front-matter counts updated by 34-03" but the milestone gap register is owned by no single plan and could be silently overwritten by a concurrent gap open. If the frontmatter counts are not updated atomically with the gap creation, the index becomes misleading.

### MEDIUM
- **ROADMAP staleness not reconciled in this milestone**: 34-05-PLAN.md correctly notes that ROADMAP success criteria directly contradict the adjudicated LOOP-03/04/06 outcomes (8.5, "both sets", n_col formula), but defers reconciliation to Phase 36. This means Phase 34's contracts will be correct but will conflict with ROADMAP wording that Phase 36 and any human reviewer will read as authoritative. This is a latent verification-failure risk — anyone running the ROADMAP's stated success criteria against Phase 34 output will see failures. The deferral to Phase 36 is acknowledged but warrants explicit user buy-in.
- **Manual judgment required for (d)/(e) dupe checks**: The LOOP-04 "no duplicated normative text" check (d) and "status-tag parity" (e) are flagged as manual-only in `34-VALIDATION.md`. The automated checks prove token presence but not semantic single-sourcing. An agent executing these checks could falsely PASS a near-miss where the mechanism formula appears once in pinn but a semantically equivalent formula (e.g., re-deriving `C_stage·median` from ctl prose) exists in ctl. Consider adding a stronger automated check: extract all numeric/formula patterns from both files and assert each unique value maps to exactly one canonical home.

### LOW
- **Wave serialization risk**: The five-plan chain (01→02→03→04→05) with tight dependency ordering means a failure in 34-01 Task 3 (ledger link) cascades to all downstream. Consider a fast-fail acceleration: if 34-01 packets pass verification, the ledger link task could be made parallel-safe to let 34-02 start before 34-01 fully closes.
- **No explicit ctl_instruction.md compatibility check between 34-02 and 34-03**: Both plans edit `ctl_instruction.md` — 34-02 collapses the C-schedule/Consolidated table, and 34-03 restructures Mini-Batch Construction. The LOOP-04 (a)-(e) re-verify is the backstop, but there is no forward-looking compatibility check that the C-schedule collapse does not interfere with the Mini-Batch Construction anchors used by 34-03.

## 4. Suggestions

1. **Update v1.6-GAPS.md frontmatter with a task-owned command** — make the count update part of the 34-GAPS.md creation task's `<verify>` block so it cannot be a forgotten step (e.g., a `sed` in-place update or a Python script that re-reads the gap entries and rewrites the YAML counts before commit).
2. **Add a stronger (d) automated guard** — extract every mathematical expression and numeric value from both files into a set of `(file, value)` pairs; assert each value appears in exactly one file. This catches e.g., `5.0` appearing in both the ctl schedule and a pinn code comment.
3. **Surface the ROADMAP staleness in 34-VERIFICATION.md** — the current plan records it as a note, but since it's the most likely source of confusion for future readers, elevate it to a highlighted "ROADMAP divergence" section with a concrete mapping of which ROADMAP success criteria lines now disagree with Phase 34 output.
4. **Consider merging 34-02 Task 2 (template-first) into 34-01 or parallelizing** — the wave dependency chain could be shortened if template/workbench setup in 34-02 doesn't need to wait for ledger linking, since 34-01 already captures the baseline before any edit.

## 5. Overall Risk

**MEDIUM** — The core architecture (packet-before-edit, deterministic verification, STOP-gap routing) is robust. The primary risk is downstream confusion from ROADMAP staleness and the manual-judgment gaps in the dupe/parity checks. The serial wave chain and GAPS.md frontmatter updating are secondary concerns. If the executor pays careful attention to the manual (d)/(e) judgment and the ROADMAP divergence note is prominently recorded, Phase 34 will deliver correct, verifiable spec contracts.

---

## claude Review

I've read the SPEC and all five plans. Here is my review.

# Phase 34 Plan Review — Training-Loop & Batch-Construction Contracts

## 1. Summary

The five plans transcribe LOOP-01..08 + SI-PINN-003 into `ctl_instruction.md` and `pinn_architecture.md` as status-tagged spec contracts, with no training-loop code (specwork-only). The wave structure is sound: 34-01 stands up packets + baseline (packet-before-edit), 34-02 lands the LOOP-04 cross-file clipping split, 34-03 lands the ctl batch contract + total-loss skeleton + LOOP-06/07/08, 34-04 reconciles SI-PINN-003 + LOOP-05 ALM, 34-05 verifies and closes the ledger. Dependency ordering (`depends_on` + sequential `wave`) is correct and acyclic; each spec-editing plan re-runs the LOOP-04 (a)-(e) cross-file suite after its batch. The plans faithfully implement the SPEC's adjudicated-verdict-plus-status discipline and the STOP-protocol routing of the source-silent batch edge cases to `GAP-34-01` (closure-gated). This is an unusually rigorous plan set; the concerns below are refinements, not structural defects.

## 2. Strengths

- **Verification-before-closure** is genuinely enforced: 34-05 Task 2 cannot mark rows `VERIFIED` until `34-VERIFICATION.md` records PASS, with a pre-write ledger SHA-256 freshness guard against concurrent edits.
- **Scope guards are strong and closed-set**, catching both tracked changes *and* untracked files under `pinn/` (`git ls-files --others`), preventing a new file from slipping past.
- **STATE.md preservation** is handled dynamically (no hardcoded filename) via captured dirty-doc hashes, respecting D-34-18.
- **Anti-fabrication discipline** is consistent: deferred constants are body-deferred with citations, genuinely source-silent edges become a STOP gap, and the win condition for LOOP-04 ("one coherent rule, zero duplicated normative text") is explicit rather than merely "8.5 absent."
- **Discriminating-check notes** correctly distinguish Phase-34-introduced tokens from pre-existing ones, so checks would fail against un-edited files.

## 3. Concerns

**MEDIUM — Inconsistent `8.5` absence check (substring vs. word-boundary).** 34-02 Task 1 uses word-boundary `re.search(r'\b8\.5\b', t)` for pinn, but Task 2/3 and 34-03/34-04/34-05 use plain `'8.5' not in ctl`. A plain substring match false-positives on any unrelated `18.5`, `8.50`, `48.5`, etc. The plans rely on a RESEARCH finding that `8.5` is currently absent from both files, but the C-schedule edits introduce numeric content; a single incidental "8.5"-containing token would hard-fail the suite for the wrong reason. Recommend the word-boundary form everywhere.

**LOW — Over-broad LOOP-06 negative regex.** `not re.search(r'n_col\s*=\s*', ctl)` scans the whole file. Legitimate prose ("where `n_col` = number of collocation points", or a pre-existing `n_col =` elsewhere in ctl) would trip it. The intent (no probe-able formula) is right; the check should be scoped to the LOOP-06 section or target the assignment-with-RHS-formula pattern specifically.

**LOW — Schedule-value deduplication only enforces `7-10`.** The (d) no-duplication check counts `7\s*-\s*10` exactly once, but the `5`/`3` stage values are unenforceable single digits, so the Consolidated-table collapse for those relies entirely on the manual win-condition judgment. Acceptable, but the automated guarantee is narrower than the prose claims.

**LOW — Exact-spacing dependence on `clip_value = C_stage`.** Several checks (`count(...) == 1`, `not in ctl`) require that literal spacing. A reformat to `clip_value=C_stage` or a line break would silently break both the positive and the single-home assertions. Consider a whitespace-tolerant match.

**LOW — `git diff ... HEAD` vs. working-tree under incremental commits.** The 34-01 Task 3 closed-set guard and several scope guards compare against `HEAD`. If the executor commits mid-plan (the repo's atomic-commit cadence), `HEAD` advances and the diff base shifts. The guards mostly still hold, but the semantics of "stray write" change once commits land; worth confirming the executor runs these before committing.

## 4. Suggestions

- Standardize all `8.5` checks to `\b8\.5\b`.
- Scope the LOOP-06 `n_col` negative check to the deferral section, or match `n_col\s*=\s*\S` requiring an RHS.
- Add a pre-flight assertion in 34-02 that confirms `n_col =`, `8.5`, and `clip_value = C_stage` are absent from the *committed HEAD* of both files, so any later failure is provably introduced by Phase 34 (turns a fragile absence-check into a delta-check, matching the `6.694` HEAD-count pattern already used well).
- In 34-05, state explicitly whether scope guards run pre- or post-commit, given the repo's atomic-commit policy.

## 5. Overall Risk: **LOW**

The plans achieve the phase goal, respect the SCOPE-13 boundary (only the two spec files edited), correctly defer rather than invent on source-silent points, and gate closure on the open gap. Residual risk is confined to a few fragile/over-broad verification predicates that could produce false failures (not false passes) — i.e., they fail safe. No data-integrity, destructive-operation, or scope-creep risk identified.

---

## claude-minimax Review

# Phase 34 Plan Review — Training-Loop & Batch-Construction Contracts

## 1. Summary

Five plans (34-01..34-05) execute a tightly scoped v1.6 specwork phase that writes four evidence packets, transcribes LOOP-01/02/03/04/05/06/07/08 contracts plus the SI-PINN-003 reconciliation into `ctl_instruction.md` and `pinn_architecture.md`, runs the final structural gate, and closes five Phase-32 ledger rows. The plans demonstrate strong governance discipline: packet-before-edit, no live code, no invented defaults, locked-convention regression guards, and a pre-write ledger-freshness concurrency check. They explicitly stop on the source-silent batch edge cases (`GAP-34-01`) and gate phase closure on user resolution. Cross-file invariants for LOOP-04 are re-run after every batch that touches either half.

## 2. Strengths

- **Packet-before-edit discipline (D-34-10)** is enforced by both per-task `read_first` and parser-visible token checks; reusing the Phase-32 schema and reserved AC IDs is a clean win for process continuity.
- **Concurrency guard** via `ledger_post_34_01_sha256` (Plan 34-01 Task 3) plus the pre-write SHA check in Plan 34-05 Task 2 is a real protection against parallel-agent ledger overwrite — the halt-and-surface behavior is correctly chosen over blind overwrite.
- **Discriminating token checks** (e.g. `B_replay`, `realized-as-deferred`, `AC-LOOP-04`, the SI-PINN-003 `RESOLVED` log) would all fail against pre-Phase-34 content; this is the right design and prevents the typical "check passed but no work done" false-positive.
- **34↔35 boundary** is held by treating loss components, `λ_E`, and Huber-δ as opaque with Phase-35 forward-references — no scope creep.
- **STRIDE threat models** are concrete and per-plan; threat IDs T-34-01..T-34-23 trace directly to mitigations.
- **STOP protocol** is followed faithfully: source-silent edge cases route to `GAP-34-01` (full schema), M14-deferred constants route body-deferred to FUT citing the M14 owner-route + §1.8/GAP-08 (no fabricated `34-GAPS.md` entry). The distinction between source-silent and source-routed deferrals is correctly maintained (D-34-16a vs D-34-16b).
- **Proactive ROADMAP staleness surfacing** in Plan 34-05 (LOOP-03/04/06 wording) plus the explicit reconciliation deferral to Phase 36 is honest and reduces future verifier confusion.
- **Anti-duplication discipline** for the LOOP-04 single-canonical-home rule (mechanism one home in pinn §4.4, schedule one home in ctl) is enforced with both positive tokens and negative checks (`7-10` count = 1; `clip_value = C_stage` count = 0 in ctl).
- **Sub-gap split precedent** in Plan 34-05 Task 3 is well-framed — only if verification surfaces a genuine multi-decision structure, not speculatively.

## 3. Concerns

### HIGH

- **H1 — Resolution-doc citation line-number drift (Plans 34-01, 34-02, 34-03, 34-04).** The action steps cite resolution-doc sections by section number and/or specific line ranges (e.g. `03-final-resolution.md:36-38`, `:40-42`, `:60-62`, `:92-94`, `:122`, `:223`, `:224`, `:228`, `:237`). No task verifies that those line numbers still resolve to the cited content. If the resolution doc has been edited, the citation links in the packets and callouts become silently wrong, and the "consume §1.4" / "consume §1.18" chain is broken. **Recommendation:** add a per-packet and per-callout verification step that re-greps the cited section-marker or the first 5-10 lines and asserts at least one discriminating token is present (e.g. `b-07` packet asserts that `03-final-resolution.md` still contains the B-07 verdict token under §1.4; ditto for §1.5/§1.10/§1.18).
- **H2 — Sub-gap split precedent + closure-gating rule interaction (Plan 34-05 Task 3).** The plan says "if GAP-34-01 is not a single decision but 2-3 distinct decisions… split it as GAP-34-01a/b/c — Surface the split to the user rather than collapsing distinct decisions into one underspecified gap." But the gate on phase closure is "user resolving or deferring `GAP-34-01`" (singular). If the split happens during execution, the closure-blocking language and the `v1.6-GAPS.md` index counts need to update in the same pass; the plan does not currently make the split's downstream closure-gate updates explicit. **Recommendation:** if the split is performed, also rewrite the closure-gate text to reference the new gap IDs, and update the `total_gaps`/`open_gaps` front-matter as part of the split (not as a follow-up).

### MEDIUM

- **M1 — `7–10` vs `7-10` vs `7--10` en-dash gap (Plan 34-02 Task 2 verify, Plan 34-05 Task 1 verify).** The no-duplication check uses `re.findall(r'7\s*-\s*10', t)` plus `re.findall(r'7--10', t)`. A writer who uses an en-dash `7–10` (U+2013) or em-dash `7—10` (U+2014) would silently fail the no-duplication invariant. **Recommendation:** add `re.findall(r'7\s*[\-–—]\s*10', t)` and assert the count is exactly 1.
- **M2 — M14 row preservation check is row-level only (Plan 34-01 Task 3 verify, Plan 34-05 Task 2).** The M14 row is asserted byte-unchanged via the row-string match, but the M14 row's Evidence Packet and Verdict cells should also be verified verbatim against a pre-edit snapshot. The current check ensures the row exists and is `PENDING` and references the right packet — but does not catch a partial cell mutation. **Recommendation:** include a per-cell hash for the M14 row (Packet / Verdict / AC / Status) in `34-BASELINE-CAPTURED` (extending the existing `ledger_post_34_01_sha256` discipline) and assert all four cells unchanged.
- **M3 — SI-PINN-002 item-3 reconciliation is asserted in action but not in verify (Plan 34-04 Task 1).** Plan 34-04 says the SI-PINN-002 item-3 reference should be reconciled to agree with the SI-PINN-003 RESOLVED entry, but the Task 1 verify block only checks the SI-PINN-003 log. A sub-agent that updates SI-PINN-003 but forgets the SI-PINN-002 item-3 update will pass verification. **Recommendation:** add a verify check that the SI-PINN-002 item-3 reference text no longer asserts the author-comment string and now points at the SI-PINN-003 resolution.
- **M4 — `[1e-4, 100]` deferral is positive in pinn §4.2; negative check on the default loop is coarser (Plan 34-04 Task 2).** The acceptance criteria require the clamp to be `deferred` and not adopted in the default loop; the verify checks `ALM is enabled by default` and `dense-residual ALM in the default loss` are absent — but a writer who adds `μ_p = 1e-4` to the default loop under a different surface (e.g. inside the loss assembly section) would not be caught. **Recommendation:** add a negative regex check that `μ_p = 1e-4` (or `mu_p = 1e-4`) and `μ_p clamp` outside the `deferred` body of the §4.2 section are absent from pinn.
- **M5 — Plan 34-03's "single forward-reference for Consolidated table" verify assumes a specific table grammar (Plan 34-02 Task 2 verify).** The regex `^## Consolidated Hyperparameter Schedule.*?(?=^## )` assumes the next top-level section starts with `^## ` (two hashes). If the Consolidated section is the last section in the file, the regex falls through; if the file is restructured, the assert silently passes. **Recommendation:** use a line-number-anchored slice (e.g. `defsection = t.split('## Consolidated')[1].split('## ', 2)[1] if '## Consolidated' in t else ''`) and verify the cell content; or fall back to "the cell text references `AC-LOOP-04` OR `Adaptive Median-Based Gradient Clipping` somewhere in the file" plus a positive pin to a single section.
- **M6 — Author-comment removal is string-equality (Plan 34-04 Task 1 verify).** The check `'is not consistent with the CTL instruction plan' not in t` is fine, but the plan also says to "reconcile" the comment — if the executor rewords the comment rather than removing it, the verify still passes. **Recommendation:** add a verify check that the surrounding context no longer contains an inconsistency assertion (e.g. assert that the §3.1 Data Batch Construction section contains `ctl_instruction` and a Phase-34 callout near the old comment location).

### LOW

- **L1 — Probe definitional drift between plans.** Plan 34-02 Task 3 calls a formula-sanity probe, Plan 34-03 Task 1 calls two probes (LOOP-01 + LOOP-03), and Plan 34-05 Task 1 says "do NOT introduce new probes — only the disposable formula-sanity probes already defined by 34-02/34-03 may be re-run." This is consistent, but the per-plan call to "disposable probe" without a single canonical probe-naming convention could lead a future plan to mint a near-duplicate. **Recommendation:** in `34-SPEC.md` or `34-VALIDATION.md`, list the canonical probe names so the discipline is one-source.
- **L2 — `python3 -c` shell-escape robustness.** Several `python3 -c` blocks contain `assert` statements with multi-line scripts. If a future code-style change wraps the assert in a try/except or adds `python3 -O` (which strips asserts), the gate could silently pass. **Recommendation:** document `python3 -OO` disable is the intended interpreter mode for the gate commands in `34-VALIDATION.md`.
- **L3 — Plan 34-01 Task 1's "dynamically captured dirty-doc set" does not include untracked files.** `git diff --name-only` returns tracked modified files only. If a concurrent agent adds an untracked file (e.g. a new evidence packet draft), it would not be in the dirty-doc SHA baseline. The plan handles STATE.md explicitly but not other untracked files. **Recommendation:** include `git ls-files --others --exclude-standard` in the baseline capture so untracked agent drafts are also hashed.
- **L4 — `8.5` absent check uses word-boundary regex in 34-02 but string `in` in 34-03/05.** Mixed token-discipline. A number like `18.5` would match the string `in` check (false positive) — Plan 34-02 catches this with `\b8\.5\b`, but 34-03 Task 2 verify and 34-05 Task 1 verify do not. **Recommendation:** standardize on the word-boundary regex everywhere.
- **L5 — "win-condition judgment confirmation" is left to the executor's prose.** Plans 34-02 Task 3 and 34-04 Task 3 require a "judgment confirmation" that the merged rule is recoverable as one coherent rule. This is the right thing to verify, but it is not machine-checkable. **Recommendation:** add a small structural proxy — e.g. assert that the ctl cross-reference line contains the words `pinn_architecture` AND `AC-LOOP-04` AND `4.4` (heading reference).

## 4. Suggestions

- **Add a citation-freshness verification block** (one per plan, or one shared in `34-VALIDATION.md`) that re-greps the resolution-doc section markers cited by the packets/callouts (`§1.4`, `§1.5`, `§1.10`, `§1.18`) and asserts the cited content is still findable.
- **Standardize the no-duplication regex** across all plans: en-dash/em-dash coverage for `7-10`, word-boundary coverage for `8.5`, and a single `clip_value = C_stage` regex.
- **Tighten the SI-PINN-002 item-3 reconciliation check** in Plan 34-04 (and add it to the Plan 34-05 final verify as a per-SI-entry log).
- **Pin the M14 row's per-cell state** in the baseline (not just the full ledger hash) so partial-cell mutations are caught.
- **Consider adding `git ls-files --others` to the dirty-doc baseline** so untracked agent drafts are also covered by the SHA.
- **For the GAP-34-01 split precedent**, also update the closure-gate language and the `v1.6-GAPS.md` index in the same pass — the plan currently describes the split but does not link the downstream gate updates to it explicitly.

## 5. Overall Risk

**MEDIUM** — The plans are well-architected, governance-disciplined, and the right things are guarded. The two HIGH concerns are both about citation freshness and gap-split cascade — neither is a structural flaw, but both could be missed by a fast executor. The MEDIUM concerns are mostly about regex/discriminator completeness; standardizing the token-discipline fixes all of them at once. No plan is logically broken, no dependency ordering is wrong, no destructive operation is in scope, and the phase boundary (specwork-only, no live code, no EDA, no training) is held throughout.

---

## claude-jiekou Review

I have read all five plans plus the SPEC, and verified the key cross-references against the system-reminder context (ledger state, ROADMAP staleness). Below is the review. I did not edit any files.

---

# Phase 34 Plan Review — Training-Loop & Batch-Construction Contracts

## 1. Summary

The five plans (34-01..34-05) decompose Phase 34 into a clean packet-before-edit pipeline: 34-01 stands up the baseline + four evidence packets and links the Phase-32 ledger; 34-02 transcribes the LOOP-04 split clipping contract; 34-03 lands the ctl-side batch/loss/metric contracts and the STOP gap; 34-04 reconciles SI-PINN-003 and the ALM deferral in pinn; 34-05 verifies and closes the ledger. Coverage of all nine requirements (LOOP-01..08 + SI-PINN-003) is complete and traceable, wave/dependency ordering is correct, and the anti-fabrication / STOP-gap / scope-guard discipline mandated by AGENTS.md is faithfully embedded. The plans achieve the phase goal. The concerns below are almost entirely about **brittleness in the automated verification commands**, not about the contract logic.

## 2. Strengths

- **Dependency ordering is sound.** 34-02→34-01, 34-03→34-02, 34-04→{34-02,34-03}, 34-05→{02,03,04}. 34-04's pinn pointer correctly depends on 34-03 (which creates the canonical ctl contract it points at). No cycle, no premature edit.
- **Packet-before-edit + single-canonical-home (no second SI-PINN-003)** is enforced with bidirectional anchor checks and no-duplication counts — the win condition is stated as "recoverable as one coherent rule with zero duplicated normative text," not merely "8.5 removed."
- **STOP-gap handling is exemplary.** GAP-34-01 is opened (not filled), indexed, and Phase-34 closure is explicitly *gated* on user resolve/defer, with a sub-gap-split precedent built in. This matches the governance protocol precisely.
- **Concurrency guard** (ledger SHA-256 freshness vs `ledger_post_34_01_sha256`) and **dynamic dirty-doc/STATE.md preservation** are real, re-derivable, and respect the user-owned STATE.md (D-34-18).
- **ROADMAP staleness is pre-surfaced** (34-05 line 306) so the Phase-36 verifier won't misread superseded preview wording (8.5 / "both sets" / inverse n_col) as failures.

## 3. Concerns

**HIGH — Missing `import re` in a 34-02 verify command will crash, not assert.**
34-02 Task 1, the verification one-liner at ~line 122 begins `from pathlib import Path; ...` then calls `re.search(r'\b8\.5\b', t)` without importing `re`. This raises `NameError`, producing a hard failure that looks like a check failure but is actually a broken command. The adjacent line 123 *does* `import re`. This will block 34-02 execution or mislead the executor. Fix: add `import re` to that command.

**MEDIUM — Substring `'8.5' not in t` is brittle (false positives).**
34-02 Task 2 (line 148), 34-03 Task 4, and 34-05 use bare-substring `'8.5'` rather than the word-boundary `\b8\.5\b` used (correctly) in 34-02 Task 1. Any unrelated `18.5`, `0.85`→no, but `18.5`, `8.55`, `$8.5$`, or a line-range/percentage in these large specs would trip the guard falsely. Recommend standardizing on the word-boundary regex everywhere.

**MEDIUM — `clip_value = C_stage` "exactly once" (`== 1`) conflicts with having both prose and pseudocode.**
34-02 Task 1 converts Listing 6 pseudocode to read `C_stage · median(...)` *and* states the mechanism in the callout prose. If the literal `clip_value = C_stage` appears in both the pseudocode block and the prose, the `t.count(...) == 1` assertion fails. The intent (single canonical *home* = §4.4) is satisfied by two occurrences in one section; the check conflates "one section" with "one string occurrence." Either relax to `>= 1` within §4.4 (as 34-03/34-05 already do) or have the prose reference the formula without restating the literal.

**MEDIUM — `7\s*-\s*10` exactly-once across the whole ctl file is fragile.**
The `n == 1` assertion scans the entire (large) `ctl_instruction.md`. Any unrelated `7-10` (a line range, "7-10 epochs", a citation) outside the C-schedule yields `n >= 2` and a false failure. Scoping the regex to the Adaptive-Median section (as Task 2 line 149 does for the Consolidated table) would be more robust than a whole-file count.

**MEDIUM — Forbidden ALM string check can collide with legitimate contract prose.**
34-04 Task 2 asserts `'dense-residual ALM in the default loss'` is absent from pinn, while the contract body is required to *state* that dense-residual ALM is rejected from the default loss. Natural phrasings like "no dense-residual ALM in the default loss" contain the forbidden substring. The intended-forbidden meaning is "ALM *enabled*," so the negative token should target the affirmative-enable phrasing, not the noun phrase that legitimate rejection text also uses.

**LOW — Cross-plan token coupling is implicit.**
34-05's per-requirement token map (e.g. `data-fidelity`, `realized-as-deferred`, `VAL-0`) hard-codes exact phrases the earlier plans must emit. This is intentional (discriminating checks) but means a benign wording change in 34-03 silently breaks 34-05. Acceptable given the spec-fidelity goal; worth noting as maintenance coupling.

## 4. Suggestions

1. Add `import re` to the 34-02 Task 1 verify command (HIGH; trivial).
2. Standardize the `8.5` guard on `\b8\.5\b` across 34-02/03/05.
3. Change the pinn mechanism-formula count to `>= 1` (or scope it to §4.4) to tolerate prose+pseudocode co-occurrence.
4. Scope the `7-10` count to the Adaptive-Median-Based Gradient Clipping section rather than the whole file.
5. Re-target the forbidden-ALM negative check to an enable-phrasing (e.g. `ALM is enabled by default` / `apply ALM to the dense ODE residual` *without* a "Never"/"rejected" qualifier) instead of the bare noun phrase.

## 5. Overall Risk

**LOW.** The contract logic, scope boundaries, dependency ordering, anti-fabrication discipline, and closure gating are all correct and well-guarded. The findings are verification-command robustness issues — one will hard-crash (HIGH, trivial fix) and several risk false negatives/positives against legitimate spec text. None threaten data integrity, scope, or the phase goal; all are local edits to the embedded check strings.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=214
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=2832
- stderr_bytes=221440

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=56
- timeout_seconds=360
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=5752
- stderr_bytes=1126

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=96
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=5179
- stderr_bytes=0

### claude-minimax
- reviewer=claude-minimax
- exit_code=0
- elapsed_seconds=102
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-minimax -p - 
- stdout_bytes=12132
- stderr_bytes=192

### claude-jiekou
- reviewer=claude-jiekou
- exit_code=0
- elapsed_seconds=187
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-jiekou --model claude-opus-4-8 -p - 
- stdout_bytes=6251
- stderr_bytes=192

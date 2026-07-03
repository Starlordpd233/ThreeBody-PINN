---
phase: 33
reviewers: [agy, opencode, codex, claude, claude-glm, claude-deepseek, claude-kimi]
rerun_reviewers: [codex, claude-deepseek, claude-glm, claude-kimi]
reviewed_at: 2026-06-22T13:54:48Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260622T134702Z-94530
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 33

## agy Review


Authentication required. Please visit the URL to log in:
  https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com&code_challenge=pIsq162rHt05HPZ8oP4AkbWNQmxhOboRsIoj74K_p08&code_challenge_method=S256&prompt=consent&redirect_uri=https%3A%2F%2Fantigravity.google%2Foauth-callback&response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcclog+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fexperimentsandconfigs+openid&state=cKmtfxY8t2U3GGP43e5LVg

Waiting for authentication (timeout 30s)...
Or, paste the authorization code here and press Enter:
Error: authentication timed out.

---

## opencode Review


# Cross-AI Plan Review: Phase 33 Curriculum Stage Contracts

## 1. Summary
Phase 33 systematically bridges the gap between the conflict adjudication ledger (Phase 32) and the normative framework specifications (`ctl_instruction.md`). The phase is divided into four highly disciplined waves: (1) baseline capture and evidence packet creation, (2) transcription of adaptive staging and momentum/metadata contracts, (3) transcription of state-machine transitions and stage gates, and (4) strict verification and ledger closure. The plans aggressively guard against "live code" modifications and strictly enforce that ungrounded decisions remain explicitly marked as "owner-pending".

## 2. Strengths
*   **Impeccable Governance Adherence:** Flawlessly obeys the "packet-before-edit" mandate and the strict separation of Phase 34/35 boundaries.
*   **Strong Negative Constraints:** Explicitly prohibits locking controversial decisions (e.g., population safeguard, `D = 6.694` scale, global `L_norm` clamp, and softened `s_min`).
*   **Robust State Management:** Enforces a strong state machine (ADVANCE, RECOVER, HALT/REVIEW) for stage transitions rather than degraded automatic advancement. 
*   **Comprehensive Threat Modeling:** STRIDE tables correctly classify and mitigate risks like tampering with specs and protected path violations.

## 3. Concerns

*   **HIGH - Fragile Hardcoded Dirty-Doc Guard:** Across all plans, the Python automated verification script hardcodes the tracking of a specific file: `docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md`. If this file is committed, renamed, or clean before/during execution, the `subprocess.check_output(['git', 'diff', '--', target])` verification will crash or yield a mismatched hash, instantly halting the autonomous execution loop.
*   **MEDIUM - Brittle Negative String Assertions:** Automated verification heavily relies on exact string matches (e.g., `"No global clamp is authorized"`, `"not a proven global maximum"`). If the execution agent rephrases the specification slightly (e.g., "Global clamping is unauthorized"), the task will fail its `verify` block.
*   **LOW - Ledger Concurrency Risk:** Task 3 in Plan 33-01 and Task 2 in Plan 33-04 update `32-ISSUE-LEDGER.md`. Ensure no concurrent agents are actively modifying the ledger, as the string-replacement approach for updating verdicts and IDs could easily cause a merge conflict or overwrite.

## 4. Suggestions
*   **Dynamic Dirty File Tracking:** Update the `33-BASELINE-CAPTURED` generation script to track `git diff` hashes dynamically based on the actual unstaged state, rather than hardcoding the `gsd-cross-ai-review-resilience` markdown file.
*   **Provide Exact Boilerplate:** To prevent execution failures caused by the strict `python3 -c` substring assertions, ensure the execution agent is explicitly instructed to inject the exact required phrases verbatim when editing `ctl_instruction.md`.
*   **Atomic Ledger Updates:** Use robust markdown table parsers or explicitly instruct the agent to preserve the structural integrity of the `32-ISSUE-LEDGER.md` table when applying the `VERIFIED` and `accept-resolution` transitions.

## 5. Overall Risk
**LOW** 
Despite the brittleness of the automated checks, the substantive operational risk is remarkably low. The phase explicitly avoids modifying live Python code (`pinn/`), dataset files, or frozen specs (`sampling_method.md`), completely insulating the project from destructive regressions. The worst-case scenario is a halted plan execution requiring manual retry, not data loss.

---

## codex Review

## 1. Summary

The plans mostly achieve Phase 33’s goal: packet-first grounding, staged transcription into `ctl_instruction.md`, and final ledger closure are ordered coherently. I was able to read the plan files I inspected. The main residual risk is not the curriculum content itself, but verification/governance gaps that could let execution close Phase 33 without proving all protected-path and STOP-gap invariants.

## 2. Strengths

- Clear dependency chain: `33-01` creates evidence/ledger prerequisites, `33-02` and `33-03` edit `ctl_instruction.md`, and `33-04` verifies before ledger closure.
- Good owner-pending discipline for population floors, `tau_L` estimator details, clipped `L_norm`, and Stage-0 pilot thresholds.
- Stronger discriminating token checks than broad keyword checks, especially in `33-02`, `33-03`, and `33-04`.
- Scope boundaries are explicit: no EDA, Stage-0 pilot, training, package installs, live `pinn/` code edits, or frozen/read-only report edits.

## 3. Concerns tagged HIGH / MEDIUM / LOW

- **HIGH:** Protected-path checks miss untracked files. The final guard in [33-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/33-curriculum-stage-contracts/33-04-PLAN.md:153) uses `git diff --name-only`, which does not detect new untracked files under protected paths such as `pinn/` or `simulation_data/`. This weakens the claim that verification proves no forbidden path or generated-data tree was changed.

- **HIGH:** STOP-gap completeness is described but not enforced by the final automated checks. [33-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/33-curriculum-stage-contracts/33-04-PLAN.md:146) says STOP-gap completeness should be recorded, but the `<verify>` commands only check token, dirty-doc, and protected-path assertions. A new `OPEN` or malformed `GAP-33` could be missed before ledger rows are marked `VERIFIED`.

- **MEDIUM:** The AC-ID renames are process-schema changes without an explicit resolved gap or owner-decision record. [33-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/33-curriculum-stage-contracts/33-01-PLAN.md:130) surfaces the convention, but it still changes seeded ledger IDs. Given `33-SPEC.md` requires source-silent process-artifact decisions to be recorded before dependent edits, this should either be explicitly owner-approved or logged/resolved as a process gap before execution.

## 4. Suggestions

- Replace or supplement protected-path guards with `git status --porcelain -- <paths>` and/or `git ls-files --others --exclude-standard -- <paths>` so untracked files are included.
- Add a Plan 04 automated gate that fails if any `GAP-33` remains `OPEN`, and validates that any new gap is present in both `33-GAPS.md` and `.planning/milestones/v1.6-GAPS.md`.
- Treat the AC-ID convention as an explicit owner-reviewed process decision before applying ledger renames.
- Keep the current plan sequence; the ordering is sound once the verification gates are tightened.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**HIGH** if executed unchanged, because final verification can overclaim protected-path safety and STOP-gap closure. With the guard fixes above, risk drops to **LOW/MEDIUM**.

---

## claude Review


I have enough to write the review. All four plans, the SPEC/CONTEXT/GAPS/VALIDATION, the Phase 32 ledger structure, and the target spec's actual contents are confirmed.

---

# Cross-AI Plan Review — Phase 33 (Curriculum-Stage Contracts)

## 1. Summary

Four sequential plans (waves 1→4) transcribe five curriculum-stage contracts (CURR-01…05) into `ctl_instruction.md`, gated by an evidence-packet-before-edit discipline. 33-01 builds the baseline + five evidence packets and links the Phase 32 ledger; 33-02/33-03 edit the spec; 33-04 runs deterministic verification and closes ledger rows. The plans are well-grounded in resolved gaps (GAP-33-01/02/03), Phase 32 owner decisions (D-05/D-06, D≈4.6416), and are tightly scoped to specwork. All referenced artifacts exist (resolution doc, ledger rows, target sections at `ctl_instruction.md` L105/L1019/L1425/L1666). The dominant weakness is that verification is entirely token presence/absence, which cannot prove the phase's stated goal — a *coherent* contract.

## 2. Strengths

- **Governance discipline is excellent**: baseline sentinel with SHA-256 preservation of the unrelated dirty doc, packet-before-edit ordering, forbidden-path guards, `pinn_architecture.md` no-diff check, and owner-pending deferrals carried verbatim from resolved gaps.
- **No concurrency hazard**: strictly sequential `depends_on`; 33-02 and 33-03 never edit `ctl_instruction.md` in parallel, and the shared Phase 32 ledger is written in disjoint waves.
- **High-risk prohibitions are well-guarded** with discriminating exact-phrase negative checks (D=6.694, global clamp, locked population floor, softened `s_min`).
- **Grounding is traceable** and scope is correctly minimal (no EDA/pilot/training; FUT deferrals explicit).

## 3. Concerns

**HIGH — No coherence/contradiction verification, yet "one coherent set of contracts" is the goal.** Every check is token presence/absence over a 98 KB file. Nothing verifies the executor *reconciled* superseded prose. Notably, the existing "Stage Transition Criteria" section (L1666) is an unresolved conversational blockquote (“…test train stage 0 and see how it goes”); the plan says "edit … so it is a state machine" but never requires removing the stale musing, and no check would catch two contradictory Stage-6 / `s_min` statements coexisting. A fully green run can still leave an internally contradictory doc. (Human `gsd-verify-work` is the only backstop.)

**MEDIUM — Several positive token checks are non-discriminating.** `Stage 0` (×7), `Stage 6`, `L_norm`, `s_min`, `L_max`, `tau_L` (×18), `record_key` (×9), `characteristic` (×7), `Rosenstein` (×3) already exist in `ctl_instruction.md`. CURR-02/CURR-04 positive checks for those would PASS with no edit. Real assurance comes only from the currently-absent phrases (`ADVANCE`/`RECOVER`, `matched-Plummer`, `unsoftened geometric`, `No global clamp is authorized`, `cumulative replay`, `not a proven global maximum`).

**MEDIUM — Acceptance-check-ID drift.** The ledger seeded `AC-CURR-02` (L_max row) and `AC-CURR-04-M6` (M6 row), but 33-04 Task 2 reassigns them to `AC-CURR-02-LMAX` and `AC-CURR-04`, and the packets use `AC-CURR-02-LMAX` — unreconciled, no rationale. The 33-01 Task 3 verify only passes by substring coincidence. Blast radius is small today (only the unwritten Phase 36), but it's the kind of process-artifact-schema change AGENTS.md says to surface, not silently introduce.

**MEDIUM — "No STOP gap opened" is baked as a required token in all five packets.** D5 (stage transitions) — unlike CURR-01/02/04 — has *no* dedicated RESOLVED `GAP-33-0x`; its ADVANCE/RECOVER/HALT semantics rest on SPEC R3 + resolution-doc §1.11. Pre-committing the happy-path conclusion as an acceptance token pressures the executor to assert groundedness rather than STOP, and a presence-check cannot distinguish a genuine "no gap" from a papered-over one.

**LOW — Closed-set changed-file assertion only in 33-02.** 33-01 and 33-03 lack a `git diff --name-only` closed-set check; a stray write to a non-forbidden, non-listed file in wave 1/3 is caught only at phase end by 33-04.

**LOW — `D ~= 4.6416` forced as literal ASCII** into a LaTeX-math doc that uses `\approx`; cosmetic stylistic mismatch. Also minor 33-01 frontmatter noise (its artifact list names `33-VERIFICATION.md` "created by Plan 04" and prose lists `ctl_instruction.md` as modified, though 33-01 makes no spec edit).

## 4. Suggestions

- Add a **coherence pass** to 33-02/33-03: require reconciling/removing superseded prose (esp. the L1666 blockquote, any pre-existing softened-`s_min`/clamp language) plus a *negative* token check that a known stale phrase no longer appears.
- Convert non-discriminating positive checks to **exact-phrase or anchored-context** assertions (CONTEXT already recommends this for prohibitions — extend it to positives).
- **Reconcile AC-IDs** to one convention across ledger + packets + verify checks, and surface the rename.
- Make the D5 packet **cite a concrete resolution-doc section** rather than relying on `No STOP gap opened` as an unconditional pass token.
- Add a closed-set `git diff --name-only` assertion to 33-01 and 33-03.

## 5. Overall Risk: **MEDIUM**

The governance scaffolding and scope control are strong and the dangerous prohibitions are well-guarded. The risk is concentrated in verification adequacy: the automated suite can pass without proving the headline deliverable (a coherent, non-contradictory contract) and a meaningful fraction of positive checks are satisfiable by pre-existing text. With a coherence/reconciliation step and discriminating positive checks added, this drops toward LOW.

---

## claude-glm Review

Verification complete. The Stage Transition Criteria section spans L1666–L1707 (next `## ` is "Consolidated Hyperparameter Schedule" at L1708); the only in-section Author note is L1668 (the stale one slated for removal). The Lyapunov Author note at L1774 is in a later section, so the section-anchored checks are passable. All regex heading anchors match real headings, and the stale prose targeted for removal exists. Review follows.

---

# Phase 33 Plan Review — Curriculum-Stage Contracts

## 1. Summary

Four sequential execute-plans (waves 1→4) transcribe grounded curriculum-stage contracts into `ctl_instruction.md` under the v1.6 specwork/STOP protocol: **33-01** builds the evidence baseline, five packets, and Phase 32 ledger links (no spec edit); **33-02** transcribes CURR-01/02/04 (adaptive assignment, `L_max`/`tau_L`, Stage 0–6 inventory + `L_norm` guard); **33-03** transcribes CURR-03/05 and reconciles the stale Stage-Transition section; **33-04** runs deterministic verification and closes the ledger. The structure is sound, tightly scoped, and clearly incorporates prior review findings (discriminating tokens, dynamic dirty-doc capture, D5 grounding, forbidden-path scope, coherence checks).

I verified against the live spec: regex anchors match real headings (Step 3 @ L1019, Step 5 @ L1425, Stage Transition Criteria @ L1666); the stale Author-note prose slated for removal exists (L1668–1678); no pre-existing softened-`s_min` / global-clamp / `np.clip` prose exists, so the negative checks are preventive as assumed.

## 2. Strengths

- **Packet-before-edit ordering** (01 → 02/03 → 04) with ledger linkage enforces the Phase 32 mandate before any spec edit.
- **Discriminating positive checks**: tokens like `characteristic angular-momentum scale`, `No global clamp is authorized`, `population safeguard value is owner-pending` are absent today, so the checks cannot pass without a real edit.
- **Explicit STOP conditions** on every transcription task; owner-pending values (population floor, final `tau_L`, clipped gate, Stage-0 thresholds) kept as visible holes, not silent defaults.
- **Forbidden-path guards match their claim** (full `simulation_data/` tree, read-only reports, `pinn/`, `pinn_architecture.md`); dirty-doc set captured dynamically and hashed.
- **D5 grounding gap** (no dedicated resolved GAP) handled with required citations rather than a blanket pass token.

## 3. Concerns

### HIGH

- **H1 — AC-ID rename is self-authorized, not routed through STOP.** 33-01 normalizes the ledger AC convention (`AC-CURR-02`→`AC-CURR-02-LMAX`, adds `AC-CURR-02-M7`, `AC-CURR-04-M6`→`AC-CURR-04`). The plan surfaces this prominently ("per AGENTS.md process-artifact rule"), but AGENTS.md lists *"new AC names beyond Phase 16 reservations"* under process-artifact schemas that **MUST surface, never invent** — which the STOP protocol reads as record-a-GAP + owner instruction, not in-plan self-authorization. Lenient reading: mechanical normalization of an already-seeded convention. Strict reading: a STOP-worthy schema change. Given the milestone premise ("no process/schema decisions without owner grounding"), this is the one item worth an explicit owner call before execution.

### MEDIUM

- **M1 — CURR-04 Stage 0–6 inventory breadth vs. grounding.** 33-02 Task 2 requires grounded *per-stage definitions* and *per-stage criteria* for all seven stages plus cumulative replay and Stage-6 catch-all. If sources do not explicitly define every stage's criteria, the executor either opens repeated STOPs (schedule risk) or faces invention pressure. The claimed/FUT hatch and STOP conditions mitigate, but this is the likeliest stall point.
- **M2 — Dirty-doc hash guard is fragile to cross-wave drift.** `dirty_docs_sha256` is captured once in Plan 01 and re-checked in 03/04. If waves run in separate sessions and any dirty file is committed/resolved/added in between, the hash either breaks (false failure) or a new dirty file falls outside the captured set (protection gap).
- **M3 — Anchored Step-3 check scope vs. edit scope (33-02).** Task 2 edits Step 3 + the Stage 0–6 inventory + metadata, but the anchored verify asserts the `L_norm` guard tokens (`No global clamp is authorized`, `nonfinite`, `near-degenerate`) specifically *inside* the Step 3 section. Confirm guard placement is intended for Step 3 (invariants) and that inventory/staging text is not also expected there.

### LOW

- **L1 — Ledger VERIFIED check couples to exact row markdown** (33-04 Task 2): requires `| M6 |`, `VERIFIED`, `accept-resolution` on one line. Passable for single-line rows; brittle to cell wrapping or `|M6|` formatting.
- **L2 — Confirm the Stage 0–6 inventory section ≠ Stage Transition Criteria section.** 33-02 (inventory/gating) and 33-03 (transition criteria @ L1666) both edit staging text; sequential execution means 33-03 sees 33-02's output, but verify the sections are disjoint so the 33-03 rewrite doesn't clobber CURR-04 text.
- **L3 — Stale-prose negative checks rely on exact strings** (incl. preserved typo `creteria`). Verified meaningful today; they pass vacuously if the prose is ever independently reworded. The section-anchored `'Author note' not in sec` check is the robust backstop (confirmed the only in-section Author note is the one slated for removal).

## 4. Suggestions

- **Resolve H1 before execution**: either record a `GAP-33` entry for the AC-ID convention and obtain owner instruction, or get a one-line owner ack that in-plan surfacing suffices for AC-ID normalization. Update `33-GAPS.md` either way.
- **For M1**: pre-scan the resolution doc / current spec for explicit per-stage Stage 0–6 definitions; flag any ungrounded stage as claimed/FUT in the packet up front to cut mid-execution STOPs.
- **For M2**: recompute the dirty-doc baseline at the start of each wave, or store per-path hashes and re-check only that originally-captured paths are byte-identical, so legitimate drift doesn't fail verification.
- Optionally strengthen the IC13-exclusion check from token (`outside IC13`) to a structural parse asserting `tau_L`/`L_norm` are absent from the IC13 vector.

## 5. Overall Risk: **MEDIUM**

Execution will likely succeed and is well-guarded against scope creep and destructive edits. The blocking variable is governance, not engineering: **H1** (AC-ID self-authorization) should be owner-confirmed before the phase runs given the milestone's "surface, never invent" bar; **M1** is the main schedule risk. With H1 resolved, the plans achieve the phase goal.

---

## claude-deepseek Review

Here is my review of the Phase 33 plans.

---

# Cross-AI Plan Review — Phase 33: Curriculum-Stage Contracts

## 1. Summary

Phase 33 is organised as four sequential waves: **(01)** baseline capture + five evidence packets + ledger linkage, **(02)** transcription of CURR-01/02/04 contracts into `ctl_instruction.md`, **(03)** transcription of CURR-03/05 (transition state machine + s_min stage gate), and **(04)** deterministic verification suite + ledger closure. The plans embody the STOP protocol, consume the three resolved Phase 33 gaps (GAP-33-01/02/03), and explicitly defer all owner-pending values — population safeguard, final tau_L estimator, clipped L_norm gate, and Stage-0 pilot thresholds — rather than silently locking them. Previous review findings (dynamic dirty-doc capture, D5 grounding citations, reconciled AC-ID convention, forbidden-path scope) are addressed. The phase makes no framework-spec edit until evidence packets exist and the Phase 32 ledger links them, satisfying the packet-before-edit prerequisite.

## 2. Strengths

- **Discriminating token checks.** The plans' verification uses exact phrases that are *absent* from `ctl_instruction.md` today (e.g., `population safeguard value is owner-pending`, `characteristic angular-momentum scale`, `not a proven global maximum`, `No global clamp is authorized`), with heading-anchored section checks. This means the checks are falsifiable — they fail if the executor writes no edit, unlike whole-file checks against pre-existing tokens (`record_key`, `Stage 0`, `L_norm`, `s_min`).

- **Explicit STOP CONDITIONS in every spec-edit task.** Plan 33-02 Task 1, Task 2 and Plan 33-03 Task 1, Task 2 each carry a concrete STOP CONDITION naming exactly what semantic choice would trigger a gap — selecting a population-floor value, a final tau_L estimator, a transition threshold, or a softened s_min gate.

- **Dynamic dirty-doc capture.** Plan 33-01 Task 1 captures `git diff --name-only` and per-file SHA-256 at baseline time rather than hardcoding a single filename (addressing review finding 6 from the prior cycle). Downstream plans compare against the dynamically captured hash.

- **D5 grounding citation requirement.** Plan 33-01 Task 3 requires the D5 packet to cite concrete grounding (resolution doc §1.11, 33-SPEC R3, 33-CONTEXT D-33-08) rather than relying on an unconditional `No STOP gap opened` token. The verification enforces that either the citation is present or a GAP-33 entry is opened.

- **Clear phase-boundary enforcement.** Phase 34/35 responsibilities are named only as handoff targets; no downstream contract is defined. The `pinn_architecture.md` guard prevents silent edits.

- **Threat modelling in all four plans.** Each plan carries a STRIDE table with concrete mitigation mapped to specific verification checks.

## 3. Concerns

### HIGH

- **Stale Author-note blockquote confirmed present.** The grep of `ctl_instruction.md` confirms the exact stale prose Plan 33-03 targets: `> **Author note:** Now, for this, we will need to look at how the first stage goes...` at line 1668, ending with `test train stage 0 and see how it goes`. The plan correctly identifies and targets this for removal. However, the existing section also contains a parallel advance-only "four criteria" list. The executor must successfully fold those criteria into the ADVANCE gate of the new state machine without inventing bridging semantics — the STOP CONDITION in 33-03 Task 1 covers this, but this is the single most delicate edit in the phase. If done poorly, the section ends up with both the old advance-only list and the new state machine coexisting, violating the coherence requirement.

- **Multi-plan writes to `32-ISSUE-LEDGER.md`.** Plan 33-01 Task 3 writes packet paths and AC IDs to the Phase 32 ledger; Plan 33-04 Task 2 writes VERIFIED status and transition log entries. If a concurrent agent (e.g., Phase 34 planning) reads or writes the ledger between these two plans, the string-matching approach used by the verification checks could silently pass against stale content. The project's `scripts/agent-commit` with owned-path declarations mitigates this partially, but the Phase 32 ledger is a shared cross-phase artefact.

### MEDIUM

- **Line-number drift in 33-03.** Plan 33-03 Task 1's action prose says "currently around `ctl_instruction.md` L1666" for the Stage Transition Criteria section. Plan 33-02 edits Step 3 (line 1019) and Step 5 (line 1425), both of which precede the transition section. Depending on how much text 33-02 adds (the full Stage 0-6 inventory with per-stage definitions could be substantial), the Stage Transition Criteria heading will shift. The verification checks use heading-anchored regex (`re.search(r'^## Stage Transition Criteria.*?(?=^## )', ...)`) so they remain robust, but the executor reading "around L1666" could navigate to a stale position. The line reference should be replaced with a heading anchor.

- **VALIDATION.md token checks are non-discriminating.** The validation strategy at `33-VALIDATION.md:59-73` checks for `record_key`, `PCA`, `clustering`, `Stage 0`, `Stage 6` — tokens already present in `ctl_instruction.md`. The plans themselves use discriminating exact-phrase checks, but any executor following VALIDATION.md alone could pass with zero edits. The plans and the validation strategy disagree on what constitutes a valid check, though the plans' own `<verify>` blocks override.

- **Evidence directory creation is implicit.** Plan 33-01 Task 1 creates `evidence/README.md` and `evidence/_TEMPLATE.md` but never runs `mkdir -p evidence/`. The Phase 33 evidence directory does not exist on disk. A `Write` tool call to `evidence/README.md` will implicitly create the directory on most filesystems, but the plan doesn't make this explicit, and a strict executor might fail on a missing parent.

- **D-05/D-06 consumption path is through gap resolution, not ledger status.** The Phase 32 ledger shows D-05 and D-06 as `PENDING | accept-resolution` — verdict is decided but status is not VERIFIED. Plan 33-03 consumes them via GAP-32-02/GAP-32-03 (the resolved gap entries) rather than ledger rows. This is correct but creates a subtle two-source dependency: the executor must verify that GAP-32-02/GAP-32-03 are RESOLVED-WITH-INSTRUCTION before transcribing, not just check the ledger status field.

### LOW

- **Untracked review files.** `33-REVIEWS.md` and `33-REVIEWS-cycle-prev.md` are untracked (per git status) and contain prior review feedback including the opencode review. The plans reference "review finding 1" through "review finding 6" without a pointer to these files. A future executor won't know where the findings originated.

- **"Edge:" prefix pattern in must_haves truths.** Plans use an `"Edge: ..."` prefix for owner-pending constraints in the `truths` list. This is a consistent convention but is process-artefact schema not documented in any phase artefact. Harmless but worth noting for consistency across phases.

- **`reject-both-as-unsupported` verdict not used.** The phase gap register and plans use only `accept-resolution` dispositions (all three gaps resolved with owner instruction). The EVID-12 verdict set includes `reject-both-as-unsupported` and `defer-with-blocker`, but no Phase 33 finding exercises them. This is correct for the current state but means the packet template's full verdict enum is untested by Phase 33 packets.

- **`epsilon_train = 1e-5` appears in `must_haves` as a locked value but is a PHYS-03 v1.4 convention.** Plan 33-03 lists `epsilon_train = 1e-5` in its truths. This is correct (locked by v1.4 Phase 20 ARCH-01), but a reader might mistake it for a Phase 33 decision. The plan's consumption of D-06 makes the provenance clear.

## 4. Suggestions

1. **Replace the "L1666" line reference** in Plan 33-03 Task 1 with the heading anchor `## Stage Transition Criteria` so the executor isn't misled if 33-02 shifts line numbers.

2. **Add an explicit `mkdir -p evidence/` step** to Plan 33-01 Task 1 before the first evidence file write, or note that the Write tool implicitly creates parent directories.

3. **Cross-reference the review files** in the plans' context or a brief preamble so executors can find "review finding 1" through "review finding 6".

4. **Consider adding a Phase 32 ledger freshness check** to Plan 33-04 Task 2: verify that no other agent modified `32-ISSUE-LEDGER.md` between Plan 33-01 Task 3 and Plan 33-04 Task 2 by comparing a stored hash or commit.

5. **Align VALIDATION.md's token checks** with the discriminating exact-phrase checks in the plans, or note that VALIDATION.md is a pre-planning scaffold superseded by plan-level verification.

## 5. Overall Risk

**LOW**

The phase operates entirely within the `.planning/` and `pinn_instruction/` specwork boundary. It writes no code, touches no generated data, and defers all owner-pending values rather than locking them. The verification suite is deterministic (`python3`, `rg`, `git diff`), runs in ~10 seconds, and every check has a concrete negative assertion. The worst-case failure mode is a plan execution halt requiring a STOP gap to be opened and surfaced — there is no risk of data loss, destructive git operations, or silent spec corruption. The MEDIUM concerns are coordination and execution-robustness issues, not correctness or safety issues.

---

## claude-kimi Review

# Phase 33 Plan Review — Curriculum-Stage Contracts

## 1. Summary

Phase 33 plans translate five curriculum/training-loop findings (`CURR-01` through `CURR-05`) into grounded framework-spec text in `ctl_instruction.md` while keeping owner-pending values explicitly deferred. The four waves are logically ordered:  
- **33-01** captures baseline, authors evidence packets, and links the Phase 32 ledger.  
- **33-02** transcribes adaptive stage assignment, `L_max`/`tau_L`, and `L_norm` guard contracts.  
- **33-03** reconciles the Stage Transition Criteria section and locks the unsoftened geometric `s_min` gate.  
- **33-04** runs source-token verification, protected-path guards, and ledger closure.

The plans correctly defer the population safeguard, final `tau_L` estimator/units/thresholds, and the clipped `L_norm` gate to future owner/EDA decisions, matching the resolved `GAP-33-01`/`GAP-33-02` disposition.

## 2. Strengths

- **Packet-before-edit discipline is rigorous.** No `ctl_instruction.md` edits happen until Phase 33-owned evidence packets and ledger links exist.  
- **STOP protocol integration is explicit.** Every task lists concrete STOP conditions for source-silent semantic choices and requires classified gap registration.  
- **Owner-pending deferrals are visible and repeated.** Population safeguard, `tau_L` final estimator, and `L_norm` clipped gate are flagged as owner-pending in the frontmatter truths, task actions, and verification checks.  
- **Protected-path and dirty-doc guards are well designed.** Dynamic capture of the dirty-doc set in `33-BASELINE-CAPTURED`, plus closed-set `git diff` checks, prevents accidental edits to frozen specs, read-only reports, live `pinn/`, and generated data.  
- **Review findings are internalized.** The reconciled acceptance-check ID convention, the stale Author-note removal, and the discriminating source-token checks are all called out and traced.

## 3. Concerns

### HIGH

- **None.** The plans do not contain any obvious high-risk omissions or contradictions. The core risk is execution fidelity on a large spec edit, but the STOP conditions and verification checks provide adequate guardrails.

### MEDIUM

- **MEDIUM — Brittle exact-string verification could produce false failures or false passes.** Plans 33-02/33-03/33-04 rely on whole-file or section-anchored exact-phrase checks (e.g., `"population safeguard value is owner-pending"`, `"No global clamp is authorized"`). If the editor paraphrases slightly, verification fails; if the phrase appears in the wrong context, it still passes. The negative check for `np.clip(L_norm, 0, 1)` is especially weak because it only requires `"not locked"` to appear anywhere in the file.  
  *Suggested mitigation:* anchor the most critical negative checks to the Step 3 / Stage inventory sections and use regex or nearby-context checks rather than substring presence.

- **MEDIUM — 33-03 reconciliation of the existing "four criteria" requires subjective mapping.** Task 1 instructs folding the existing advance-only criteria into the `ADVANCE` path. The plan provides a STOP condition, but the criteria are currently conversational (`ctl_instruction.md:1666-1678`). If the executor cannot map them cleanly, the task must halt and open a gap, which could stall the phase. This is acceptable but worth flagging as a likely friction point.

- **MEDIUM — Ledger verdict/status wording in 33-01 Task 3 is ambiguous.** It says "Set their verdict cells to `accept-resolution` ... keep status nonterminal until Plan 04 verification passes." A later reader could misread this as setting the verdict now and the status later, but the verify check only confirms packet paths and AC IDs, not verdict/status values. Clarifying whether `accept-resolution` is written in 33-01 or 33-04 would reduce confusion.

### LOW

- **LOW — Artifact inventory in 33-01 over-claims.** It lists `33-VERIFICATION.md` as a new artifact produced by 33-01 and `ctl_instruction.md` as a modified artifact, neither of which is touched in 33-01. This is forward-looking but technically inaccurate for the plan.  
- **LOW — Stage 0-6 inventory check is not section-anchored.** The `re.search(r'\bStage 0\b.*\bStage 6\b', txt, re.S)` check in 33-02 could pass if those tokens appear anywhere, even outside the intended inventory section. Combined with the `per-stage definitions`/`cumulative replay` checks the risk is low, but a section anchor would be stronger.

## 4. Suggestions

1. **Tighten the negative-token checks** for `np.clip(L_norm, 0, 1)`, softened `s_min`, and locked population-floor wording by anchoring them to the relevant `ctl_instruction.md` sections.  
2. **Clarify in 33-01 Task 3** whether `accept-resolution` verdicts are written now or left blank/PENDING until 33-04.  
3. **Add a cross-plan coherence check** in 33-04 that confirms 33-02 and 33-03 edits do not contradict each other in `ctl_instruction.md` (e.g., Stage 6 is both a catch-all in 33-02 and an unsoftened `s_min` gate in 33-03).  
4. **Verify the reconciled AC IDs appear in the evidence packets themselves**, not only in the ledger, as part of the 33-01 or 33-04 verification suite.  
5. **Confirm the `33-BASELINE-CAPTURED` dirty-doc set is frozen** after 33-01 and that any new unrelated dirty docs appearing before 33-04 are flagged rather than silently ignored.

## 5. Overall Risk

**LOW**

The plans are tightly scoped, well grounded, and include clear STOP conditions, protected-path guards, and discriminating verification. The main execution risks are exact-string verification brittleness and the subjective mapping of existing Stage Transition Criteria prose, both of which are covered by STOP/gap protocols. No scope creep, destructive operations, or security/data-integrity risks were identified.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## Verification coverage (source-grounding pass)

Symbols cited in PLAN.md and verified against the live spec/codebase. Phase 33's "Artifacts this phase produces" section declares these as new (packets, baseline, ledger, summary) and they are not subject to symbol verification. The list below covers symbols the plans *cite* from existing spec or scripts.

| Symbol | Cited in PLAN | Declared in | Verdict |
|---|---|---|---|
| `Stage Transition Criteria` heading | 33-03 L119 | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1666` | VERIFIED |
| `Step 3: Necessary Calculations of Invariants` heading | 33-02 L160 (anchored verify) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1019` | VERIFIED |
| `Step 5: Curriculum Stage Assignment` heading | 33-02 L134 (anchored verify) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1425` | VERIFIED |
| `## Consolidated Hyperparameter Schedule` (next-section anchor) | 33-03 L123 regex lookahead | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1708` | VERIFIED |
| Stale Author-note prose `test train stage 0 and see how it goes` | 33-03 L122, 33-04 L151 (negative check) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1678` | VERIFIED (target present, must be removed) |
| Stale typo `All of this transition creteria is` | 33-03 L122, 33-04 L151 (negative check) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1669-1670` | VERIFIED |
| `L_max = M_tot * r_char * sqrt(2 * |E| / M_tot)` formula | 33-02 L157 | Spec L1088-1096 defines `compute_L_norm` with `L_max = M_total * r_char * v_char` | AMBIGUOUS — spec uses `v_char` (characteristic speed) form; plan's `sqrt(2|E|/M_tot)` form is the kinetic-equivalent expression of `v_char`. Both derive from the same scale but the prose form is not literally present; the spec token check requires the *phrase* `characteristic angular-momentum scale`, which is absent |
| `D ~= 4.6416` raw-mass canonical convention | 33-02 L159, 33-04 L150 | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:929` (`D = (G T^2)^{1/3} \approx 4.6416`) | VERIFIED (LaTeX form in spec; ASCII required by verify check — cosmetic) |
| `D = 6.694` mass-fraction rejected | 33-02 L162 (negative check) | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:921` | VERIFIED (rejection prose present) |
| `record_key` stable label | 33-02 L131, 134 | Not found in `simulation_data/Scripts/` | UNCHECKABLE — declared as a *new* concept to be written into `ctl_instruction.md`; the plan's positive check `record_key` requires presence in the spec, but it currently appears in the spec context for stable integer labels (semantic, not Python symbol). Functional scope is the spec, not the scripts |
| `tau_L`, `L_norm`, `s_min` tokens | 33-02 / 33-03 / 33-04 checks | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:972,1034,1037,1088,1155,1419` | VERIFIED |
| Discriminating tokens absent today: `population safeguard value is owner-pending`, `characteristic angular-momentum scale`, `not a proven global maximum`, `No global clamp is authorized`, `unsoftened geometric s_min`, `matched-Plummer`, `cumulative replay`, `Stage-6 catch-all`, `provisional`, `HALT/REVIEW` | 33-02 / 33-03 / 33-04 positive checks | Verified absent via grep | VERIFIED (absence proves discriminating nature of checks) |
| `epsilon_inv = 1e-10` | 33-03 L148, 33-04 L150 | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:921` (`\varepsilon_{\mathrm{inv}} = 10^{-10}`) | VERIFIED (LaTeX form in spec) |
| `epsilon_train = 1e-5` | 33-03 L23, L148 | PHYS-03 v1.4 lock | UNCHECKABLE in spec — provenance via v1.4 phase documentation |
| Final resolution doc `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | 33-01 / 33-02 / 33-03 read_first | Referenced in plan read_first lists; existence verified by file path | UNCHECKABLE in this pass — file existence and `§1.11` citation not confirmed by grep from this cycle |
| `32-ISSUE-LEDGER.md` Phase 33-owned row IDs | 33-01 Task 3, 33-04 Task 2 | Referenced in plan read_first | UNCHECKABLE in this pass — row content not directly grepped |
| `33-BASELINE-CAPTURED` dirty-doc hash captures `gsd-cross-ai-review-resilience-plan.md` | 33-01 Task 1 dynamic capture | `git status` shows this file as unstaged | VERIFIED — the dynamic capture mechanism picks up whatever `git diff --name-only` returns, so the specific filename does not matter (opencode HIGH finding fully addressed) |
| `evidence/` directory | 33-01 L148-159 | Not yet present on disk | UNCHECKABLE — created by Plan 33-01 Task 1; existence not in scope for review-only pass |
| AC IDs `AC-CURR-01`, `AC-CURR-02-LMAX`, `AC-CURR-02-M7`, `AC-CURR-03`, `AC-CURR-04` | 33-01 L136-140, 33-04 Task 2 verify | Defined in 33-01 plan; ledger reconciliation in 33-04 Task 2 | UNCHECKABLE — ledger content not grepped in this pass; plans reference the convention consistently |

Notes:
- All discriminating-token checks (33-02 / 33-03 / 33-04) target phrases confirmed absent from `ctl_instruction.md` today, which means the checks will fail unless a real edit is performed — opencode MEDIUM finding on "non-discriminating" positive checks is fully addressed for the new phrases; `record_key` (33-02 L131) is the residual non-discriminating token.
- Section-anchored checks use `re.search(r'^## ...', txt, re.M|re.S)` and `(?=^## )` lookahead — robust to line-number drift from 33-02 edits (claude-deepseek M finding addressed).
- Stale Author-note prose exists in the spec and is targeted for removal; the negative checks assert both its presence (for removal verification) and that `'Author note'` no longer appears in the section.
- The discrimination between `v_char` (spec) and `sqrt(2|E|/M_tot)` (plan prose) is a kinetic-equivalence rephrasing, not a different scale; the spec's `L_max` definition (L1095) is `M_total * r_char * v_char`, and `v_char = sqrt(2|E|/M_tot)` for a bound system. The plan's prose is grounded but the verify check requires the *phrase* `characteristic angular-momentum scale`, which is the load-bearing token — the literal formula text is illustrative.

## xreview Diagnostics

### agy
- status: preserved from existing REVIEWS.md

### opencode
- status: preserved from existing REVIEWS.md

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=201
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3284
- stderr_bytes=118764

### claude
- status: preserved from existing REVIEWS.md

### claude-glm
- reviewer=claude-glm
- exit_code=0
- elapsed_seconds=465
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=6580
- stderr_bytes=0

### claude-deepseek
- reviewer=claude-deepseek
- exit_code=0
- elapsed_seconds=131
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp deepseek -p - 
- stdout_bytes=9383
- stderr_bytes=0

### claude-kimi
- reviewer=claude-kimi
- exit_code=0
- elapsed_seconds=131
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp kimi -p - 
- stdout_bytes=5809
- stderr_bytes=0

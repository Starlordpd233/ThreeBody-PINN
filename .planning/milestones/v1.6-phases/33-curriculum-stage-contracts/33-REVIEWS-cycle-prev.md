---
phase: 33
reviewers: [agy, opencode, codex, claude, claude-glm]
rerun_reviewers: [agy, opencode, codex, claude, claude-glm]
reviewed_at: 2026-06-22T11:50:37Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260622T114436Z-53386
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

The Phase 33 plans are coherent and likely achieve the phase goal: they sequence evidence packets before spec edits, keep scope centered on `ctl_instruction.md`, preserve owner-pending decisions, and include final ledger/verification closeout. I found no HIGH-risk blockers.

## 2. Strengths

- Clear dependency order: `33-01` creates packets/ledger links, `33-02` and `33-03` make bounded spec edits, and `33-04` verifies/ closes ledger state.
- Strong scope discipline around v1.6 constraints: no EDA, Stage-0 pilot, training-loop code, dataset regeneration, or live `pinn/` use.
- Good handling of known resolved gaps: population floor, final `tau_L`, clipped `L_norm`, transition thresholds, and Phase 34/35 ownership stay deferred or owner-pending.
- Evidence-packet-first design matches the Phase 32 ledger pattern and reduces unsupported transcription risk.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **MEDIUM:** Verification is mostly whole-file token presence, not section-scoped semantic validation. The checks in `33-02-PLAN.md:133-160`, `33-03-PLAN.md:117-141`, and `33-04-PLAN.md:149` can pass if required phrases exist anywhere in `ctl_instruction.md`, even if placed in the wrong section or contradicted elsewhere.
- **MEDIUM:** The protected-path guard is narrower than the plan’s own claim. `33-04-PLAN.md:145` and `33-04-PLAN.md:155` claim protection for generated data, schema files, and UI files, but the automated guard at `33-04-PLAN.md:151` checks `simulation_data/Data` rather than the broader `simulation_data/` shown in research guidance, and does not explicitly name schema/UI paths.
- **LOW:** `33-02` is the densest semantic edit wave but lacks the explicit task-local STOP wording present in `33-03`. Global governance still applies, but repeating the STOP trigger in `33-02` would reduce execution drift around owner-pending population floor, `tau_L`, and `L_norm` decisions.

## 4. Suggestions

- Strengthen final verification with section-scoped checks around the intended `ctl_instruction.md` headings, plus negative scans for contradictory legacy wording.
- Align the forbidden-path command with the stated guard scope, especially generated data and any schema/UI paths that could exist in this repo.
- Add one explicit STOP sentence to each `33-02` task: if exact prose requires a new semantic choice or contradicts packet evidence, stop and open/update the required gap records before continuing.

## 5. Overall Risk

**MEDIUM.** The plan direction and sequencing are sound; the main residual risk is that validation may certify token presence and file-scope claims more strongly than the automated checks actually prove.

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

_claude-glm failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=claude-glm
- exit_code=143
- elapsed_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp glm -p - 
- stdout_bytes=0
- stderr_bytes=0

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260622T114436Z-53386/xreview-claude-glm-33.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260622T114436Z-53386/xreview-claude-glm-33.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260622T114436Z-53386/xreview-claude-glm-33.meta

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=32
- watchdog=not_triggered
- stdout_bytes=848
- stderr_bytes=0

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=40
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=3629
- stderr_bytes=356

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=225
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=2679
- stderr_bytes=199594

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=334
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=5707
- stderr_bytes=0

### claude-glm
- reviewer=claude-glm
- exit_code=143
- elapsed_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp glm -p - 
- stdout_bytes=0
- stderr_bytes=0

---

## Verification coverage

_Appended by the isolated REVIEW agent (source-grounding pass). Authority resolved via `gsd-tools drift-guard authority --raw` = **`grep`** (severity for MISSING = `needs-acknowledgement`, `hardBlock: false`). Under `grep` authority no MISSING symbol can be a hard block; the cycle is not stopped by drift-guard. Symbols the plans declare they CREATE this phase (per each plan's "Artifacts This Phase Produces" / `files_modified`) are excluded as outputs, not references._

### MISSING (adapter can check this kind and it is absent — real findings)
- None. Every concrete pre-existing symbol the plans cite resolves in the repo (see VERIFIED below). All absent phrases are either (a) symbols the plans CREATE this phase, or (b) Markdown spec prose tokens — both UNCHECKABLE, not MISSING.

### AMBIGUOUS (multiple candidates)
- None.

### VERIFIED (cited pre-existing symbols that resolve; `file:line`)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` exists; cited anchors resolve: "Multi-Stage Data Stratification" (L105), Step 3 invariants (L1019/L1034), "Step 5: Curriculum Stage Assignment" (L1425), "Stage Transition Criteria" (L1666), `compute_L_norm` + `L_max = M_total * r_char * v_char` (L1088/L1095), Rosenstein-style `tau_L` estimator (L1155), `record_key` (L429+).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` exists (no-diff target for 33-03).
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` exists (read_first source).
- `pinn_instruction/.../research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` exists (resolution doc).
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` exists; all five Phase-33-owned rows present with the row labels the plans target: `M6`(L20), `M7`(L21), `D5`(L25), `adaptive stage assignment`(L29), `L_max / tau_L`(L31).
- Phase 32 evidence packets cited all exist: `d-05-s-min-frame.md`, `d-06-epsilon-strategy.md`, `d-6-694-conflict.md`, `README.md`, `_TEMPLATE.md`.
- Requirements `CURR-01`..`CURR-05` exist in `.planning/REQUIREMENTS.md` (L41-45); `SCOPE-14`/`SCOPE-15` scope annotations exist (L94-95).
- Gaps `GAP-33-01` (RESOLVED-WITH-INSTRUCTION 2026-06-22), `GAP-32-02`, `GAP-32-03` (both RESOLVED-WITH-INSTRUCTION 2026-06-21) exist in `.planning/milestones/v1.6-GAPS.md` / `33-GAPS.md`.
- Pre-existing spec tokens the plans rely on: `epsilon_inv = 1e-10` (ctl L622/L632/L1729), `epsilon_train = 1e-5` (ctl L632/L815), Plummer `eps = 1e-10` (ctl L475/L580/L1088).
- Dirty-doc guard target exists and is currently dirty (` M`): `docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md`.

### UNCHECKABLE / skipped (one-line reason each)
- `ADVANCE`, `RECOVER`, `HALT/REVIEW` — CREATE tokens; 0 occurrences in ctl_instruction.md today; Plan 33-03 Task 1 writes them (output, not reference).
- `matched-Plummer`, `unsoftened geometric`, `No global clamp is authorized`, `not a proven global maximum`, `characteristic angular-momentum scale`, `outside IC13`, `cumulative replay`, `per-stage definitions`, `per-stage criteria`, `Stage-6 catch-all`, `nonfinite`, `near-degenerate`, `revisable baseline`, `D ~= 4.6416` (ASCII form) — Markdown spec prose the plans CREATE this phase; 0 occurrences today; UNCHECKABLE by grep adapter.
- `record_key`, `Stage 0`..`Stage 6`, `L_norm`, `s_min`, `L_max`, `tau_L`, `Rosenstein`, `characteristic` — Markdown spec prose tokens that ALREADY occur in ctl_instruction.md; positive presence-checks on these are non-discriminating (would pass with no edit). Treated as UNCHECKABLE for the kind, and flagged to reviewers as a verification-adequacy concern (see codex/claude MEDIUM).
- All `.planning/phases/33-curriculum-stage-contracts/evidence/*.md` packets, `33-BASELINE-CAPTURED`, `33-VERIFICATION.md`, `33-0N-SUMMARY.md` — files this phase creates; not-yet-written, UNCHECKABLE.
- AC IDs (`AC-CURR-01`, `AC-CURR-02`, `AC-CURR-02-LMAX`, `AC-CURR-02-M7`, `AC-CURR-03`, `AC-CURR-04`, `AC-CURR-04-M6`) — process-artifact schema strings written this phase; ledger currently seeds `AC-CURR-04-M6`/`AC-CURR-02` but 33-04 rewrites to `AC-CURR-04`/`AC-CURR-02-LMAX` (see AC-ID-drift finding); not a code symbol, UNCHECKABLE by adapter.

### Hard block
- None possible this cycle (authority = `grep`; drift-guard `hardBlock: false` for all MISSING, and there are no MISSING symbols regardless).

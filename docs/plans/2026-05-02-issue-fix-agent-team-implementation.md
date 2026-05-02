# Issue-Fix Agent Team Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Run a 13-worker sequential-gate agent team that patches the upstream plan
`~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md` so that all 13 actionable
findings from `docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md` are
addressed and the plan's own SHA-256 round-trip verification passes 7/7 against the live archive
files.

**Architecture:** The Orchestrator session (the engineer running this plan) processes one finding
at a time. For each finding it spawns a Worker subagent (which proposes a structured edit), then a
Supervisor subagent (which runs a 7-check review and emits APPROVE / REWORK / ESCALATE_TO_USER).
The Orchestrator applies approved edits via the `Edit` tool with backup snapshots, retries up to
3 times on REWORK, and pauses for user input on ESCALATE. After all 13 findings are processed, a
final E2E test extracts the patched plan's construction script and verification script, runs them,
and expects `PASS: 7/7`.

**Tech Stack:** Claude Code in-session orchestration. Tools: `Agent` (general-purpose subagent),
`Read`, `Edit`, `Bash`, `AskUserQuestion`, `TaskCreate`, `TaskUpdate`. Python 3 for the final E2E
test (already on the user's mac). No project dependencies needed.

**Reference docs (read these before starting):**
- Design contract: `docs/plans/2026-05-02-issue-fix-agent-team-design.md`
- Findings to address: `docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md`
- Plan being patched: `~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md`

---

## Conventions Used in This Plan

- **`$RUN_DIR`** = `~/.claude/plans/.consolidate-fix-run/` (created by Task 1)
- **`$PLAN`** = `~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md`
- **`$SYNTH`** = `~/Desktop/3_body_problem/docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md`
- **`$ARCHIVE_DIR`** = `~/Desktop/3_body_problem/pinn_instruction/original_latex/review-of-framework/issues/archive/`

Throughout: paths are absolute. JSON blobs are pretty-printed for readability but Worker/Supervisor
return raw single-line JSON.

---

## Task 1: Bootstrap run state

**Files:**
- Create: `$RUN_DIR/journal.json`
- Create: `$RUN_DIR/run-log.md`
- Create: `$RUN_DIR/ledger.txt`
- Create: `$PLAN.bak.original`

**Step 1: Verify input files exist**

Run:
```bash
test -f "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md" && \
test -f "$HOME/Desktop/3_body_problem/docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md" && \
test -d "$HOME/Desktop/3_body_problem/pinn_instruction/original_latex/review-of-framework/issues/archive/" && \
echo "OK: all inputs exist"
```
Expected: `OK: all inputs exist`

**Step 2: Create run directory**

Run:
```bash
mkdir -p "$HOME/.claude/plans/.consolidate-fix-run"
ls -la "$HOME/.claude/plans/.consolidate-fix-run/"
```
Expected: empty directory listed.

**Step 3: Create the always-recoverable original snapshot**

Run:
```bash
cp "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md" \
   "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md.bak.original"
shasum -a 256 "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md.bak.original"
```
Expected: a SHA-256 hash printed (record it in the run-log).

**Step 4: Initialize journal, ledger, and run-log**

Use `Write` to create three files with these exact initial contents.

`$RUN_DIR/journal.json`:
```json
{
  "started_at": "<ISO 8601 now>",
  "completed_findings": [],
  "current_finding": null,
  "attempt_count": 0,
  "ledger": [],
  "snapshot_paths": {
    "original": "~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md.bak.original"
  }
}
```

`$RUN_DIR/ledger.txt`:
```
# Applied findings ledger — empty at start. Each approved finding adds one block.
```

`$RUN_DIR/run-log.md`:
```markdown
# Issue-Fix Agent Team Run Log

Started: <ISO 8601 now>
Original plan SHA-256: <from Step 3>

---
```

**Step 5: Verify run state**

Run:
```bash
ls -la "$HOME/.claude/plans/.consolidate-fix-run/"
cat "$HOME/.claude/plans/.consolidate-fix-run/journal.json" | python3 -m json.tool > /dev/null && echo "journal.json valid"
```
Expected: 3 files listed, `journal.json valid`.

**Step 6: Run baseline E2E (expect FAIL)**

This proves the patched-plan E2E will be a meaningful test. Use the procedure in Task 16 (Final
E2E Test) but expect FAILURE — record which assertion fails.

Append to `$RUN_DIR/run-log.md`:
```
## Baseline E2E (before any worker)

Result: <FAIL with which assertion>
This confirms the plan-as-written is broken (matches finding C-1).
```

**Step 7: Create TaskCreate entries for visibility**

Use the `TaskCreate` tool to add 14 tasks (13 findings + 1 final E2E):
- Subject: "Apply finding C-1 (Phase 1)"
- Subject: "Apply finding M-1 (Phase 2)"
- ... etc through "Apply finding N-2 (Phase 4)"
- Subject: "Run final E2E integration test"

These are tracked but not yet started.

**No commit** — plan file lives outside the repo. Snapshots are the audit trail.

---

## Task 2: Define the Worker prompt template

**Files:**
- Create: `$RUN_DIR/worker_prompt_template.md`

**Step 1: Write the template**

Use `Write` to create `$RUN_DIR/worker_prompt_template.md` with this EXACT content:

````
You are a Worker subagent in the Issue-Fix Agent Team for the ARCHIVE_MASTER plan.

Your job: Address ONE finding from the synthesis report by proposing a structured edit to the plan.

YOU DO NOT WRITE TO THE PLAN FILE DIRECTLY. The Orchestrator will apply your proposed edit after a
Supervisor reviews it.

INPUTS

Finding ID: {{FINDING_ID}}

Finding text (verbatim from synthesis report):
---
{{FINDING_TEXT}}
---

Current plan state (live read; includes all prior approved fixes):
---
{{CURRENT_PLAN_TEXT}}
---

Applied findings ledger (prior fixes that have already landed; do not undo or contradict):
---
{{APPLIED_FINDINGS_LEDGER}}
---

{{REWORK_HISTORY_BLOCK}}

YOUR PROCESS

1. PREMISE CHECK — Verify the finding's described problem actually exists in the current plan state.
   - Re-read the relevant plan section(s)
   - Decide: is the problem real? Has it been addressed already by a prior fix?
   - Document evidence

2. PRESCRIPTION CHECK — If the finding has a "Recommended fix", evaluate whether it would solve
   the root problem.
   - Is the recommendation correct?
   - Is there a better alternative?

3. CHOOSE APPROACH (one of):
   - implement_as_recommended — premise verified AND prescription verified
   - implement_modified — premise verified BUT prescription is not best (you propose a better one)
   - no_change_needed — premise is moot (already fixed, or not a real issue)
   - disagree_with_finding — the finding itself is wrong

4. PROPOSE THE EDIT (if any):
   - Identify the exact section to change
   - Provide removed_content (exact bytes for Edit tool's exact-match)
   - Provide new_content (exact replacement text)

OUTPUT — return ONLY this JSON object, no commentary, no markdown fence around it:

{
  "finding_id": "{{FINDING_ID}}",
  "edit_type": "section_rewrite | targeted_replace | append | no_change_needed",
  "target_locator": {
    "section_heading": "...",
    "line_range": "L62-L68",
    "unique_anchor_string": "..."
  },
  "removed_content": "...",
  "new_content": "...",
  "premise_check": {
    "finding_claims": "<paraphrase of the finding's claim>",
    "verified_against_plan": true,
    "evidence": "<what you did to verify>"
  },
  "prescription_check": {
    "recommended_fix": "<paraphrase of recommendation>",
    "would_actually_solve_root_problem": true,
    "reasoning": "<why or why not>"
  },
  "chosen_approach": "implement_as_recommended",
  "deviation_rationale": "<REQUIRED if chosen_approach != implement_as_recommended; else empty string>",
  "follow_up_findings_affected": []
}

RULES
- Stay in your lane: touch only sections relevant to your finding
- No invented requirements
- One coherent edit per turn
- If chosen_approach == "no_change_needed": set removed_content and new_content to ""
- If chosen_approach == "disagree_with_finding": still fill premise_check and prescription_check
  with your reasoning; the Supervisor will likely escalate to user
````

**Step 2: Verify**

Run:
```bash
wc -l "$HOME/.claude/plans/.consolidate-fix-run/worker_prompt_template.md"
```
Expected: ~60 lines.

---

## Task 3: Define the Supervisor prompt template

**Files:**
- Create: `$RUN_DIR/supervisor_prompt_template.md`

**Step 1: Write the template**

Use `Write` to create `$RUN_DIR/supervisor_prompt_template.md` with this EXACT content:

````
You are the Supervisor subagent in the Issue-Fix Agent Team.

Your job: Review ONE Worker's proposed edit and emit a verdict.

INPUTS

Finding ID: {{FINDING_ID}}

Finding text (verbatim):
---
{{FINDING_TEXT}}
---

Worker's structured output:
---
{{WORKER_OUTPUT_JSON}}
---

Current plan state (live):
---
{{CURRENT_PLAN_TEXT}}
---

Applied findings ledger:
---
{{APPLIED_FINDINGS_LEDGER}}
---

Full synthesis report (all 15 findings — for cross-finding context):
---
{{FULL_SYNTHESIS_REPORT}}
---

YOUR 7-CHECK REVIEW (in order)

1. Premise check is sound — Worker actually verified the claim, not just asserted it
2. Prescription check is sound — Worker actually evaluated whether the fix solves the root problem
3. Chosen approach matches verification result — internally consistent
4. Edit reflects the chosen approach — diff matches stated intent, no scope creep
5. No regression on prior approved fixes — diff doesn't undo/contradict the ledger
6. No invasion of another finding's lane — diff doesn't touch sections owned by future findings
7. Plan stays internally consistent — no dangling references to removed concepts

VERDICTS
- APPROVE — all 7 pass
- REWORK — one or more failed; provide specific feedback referencing which check failed
- ESCALATE_TO_USER — you cannot confidently judge (e.g., Worker disagrees with finding and you're
  uncertain whether the disagreement holds water)

OUTPUT — return ONLY this JSON object, no commentary, no markdown fence:

{
  "verdict": "APPROVE | REWORK | ESCALATE_TO_USER",
  "checks_passed": [1, 2, 3, 4, 5, 6, 7],
  "checks_failed": [
    {"check": 5, "reason": "Diff modifies the SHA-256 expected value, contradicts M-1's fix"}
  ],
  "ledger_entry": "<one-paragraph summary of what was approved; only if verdict == APPROVE>",
  "feedback_to_worker": "<specific actionable feedback; only if verdict == REWORK>",
  "escalation_reason": "<why you're uncertain; only if verdict == ESCALATE_TO_USER>"
}

RULES
- An APPROVE requires checks_passed = [1,2,3,4,5,6,7] AND empty checks_failed
- A REWORK requires non-empty feedback_to_worker
- Be specific in feedback_to_worker — "your premise_check only said 'verified' without showing
  how you verified it; show the actual evidence"
````

**Step 2: Verify**

Run:
```bash
wc -l "$HOME/.claude/plans/.consolidate-fix-run/supervisor_prompt_template.md"
```
Expected: ~55 lines.

---

## Task 4: Define the Worker Iteration Recipe (executed 13 times)

This task documents the procedure that Tasks 5-15 each invoke once with a specific finding ID.
Read this carefully — it is the heart of the plan.

### Recipe inputs

- `FINDING_ID` — e.g. `C-1`
- `FINDING_LINE_START` — line number in synthesis report (provided in each per-finding task)
- `FINDING_LINE_END` — line number in synthesis report
- `EXPECTATION` — short note (e.g., "likely no_change_needed" for L-3, N-1)

### Recipe steps

**Step R1: Extract finding text**

Use `Read` on `$SYNTH` with `offset=FINDING_LINE_START` and `limit=(FINDING_LINE_END - FINDING_LINE_START + 1)`.
Strip the line-number prefixes the Read tool adds. Save as `FINDING_TEXT` (in-memory).

**Step R2: Read current plan state**

Use `Read` on `$PLAN` with no offset (full file). Strip line-number prefixes. Save as
`CURRENT_PLAN_TEXT`.

**Step R3: Read ledger**

Use `Read` on `$RUN_DIR/ledger.txt`. Save as `APPLIED_FINDINGS_LEDGER`.

**Step R4: Compose Worker prompt**

Read `$RUN_DIR/worker_prompt_template.md`. Substitute `{{FINDING_ID}}`, `{{FINDING_TEXT}}`,
`{{CURRENT_PLAN_TEXT}}`, `{{APPLIED_FINDINGS_LEDGER}}`. For first attempt set
`{{REWORK_HISTORY_BLOCK}}` to empty string. For reworks (R12), substitute the rework history block.

**Step R5: Append the Worker prompt to the run-log**

Append to `$RUN_DIR/run-log.md`:
```
## Finding {FINDING_ID} — Worker attempt {ATTEMPT_NUM} ({ISO timestamp})

### Worker prompt (truncated to first 500 chars + last 200)
[paste]
```

**Step R6: Spawn Worker subagent**

Call `Agent` with:
- `subagent_type: "general-purpose"`
- `description: "Worker for finding {FINDING_ID}"`
- `prompt: <composed Worker prompt from R4>`

**Step R7: Parse Worker output**

The Agent returns a string. The Worker should return ONLY a JSON object. Strip any leading/trailing
whitespace or accidental markdown fences (e.g. ```json ... ```), then parse with `python3 -c "import json,sys; json.load(sys.stdin); print('OK')"`.

If parsing fails: log the raw output to run-log, treat as REWORK, increment attempt counter, go to R12.

If parsing succeeds: validate required keys (`finding_id`, `chosen_approach`, `premise_check`,
`prescription_check`). Validate `finding_id` matches expected. Save as `WORKER_OUTPUT_JSON`.

**Step R8: Append Worker output to run-log**

Append the full JSON to `$RUN_DIR/run-log.md` under the Worker attempt heading.

**Step R9: Compose Supervisor prompt**

Read `$RUN_DIR/supervisor_prompt_template.md`. Read `$SYNTH` (full file) for
`{{FULL_SYNTHESIS_REPORT}}`. Substitute all placeholders.

**Step R10: Spawn Supervisor subagent**

Call `Agent` with:
- `subagent_type: "general-purpose"`
- `description: "Supervisor review for finding {FINDING_ID}"`
- `prompt: <composed Supervisor prompt from R9>`

**Step R11: Parse Supervisor verdict**

Same parsing approach as R7. Validate `verdict` is one of `APPROVE`, `REWORK`, `ESCALATE_TO_USER`.
Append the full JSON to `$RUN_DIR/run-log.md`.

**Step R12: Branch on verdict**

#### Branch A — APPROVE

1. Snapshot before:
   ```bash
   cp "$PLAN" "$PLAN.bak.before-{FINDING_ID}"
   ```

2. If `WORKER_OUTPUT_JSON.chosen_approach == "no_change_needed"`:
   - No edit applied.
   - Append to ledger: `{FINDING_ID}: APPROVED (no_change_needed). {ledger_entry}`
   - Skip to step 5.

3. Apply edit using `Edit` tool:
   - `file_path: $PLAN`
   - `old_string: WORKER_OUTPUT_JSON.removed_content`
   - `new_string: WORKER_OUTPUT_JSON.new_content`
   - If `Edit` fails (exact-match miss): treat as system error. Restore from `.bak.before-{ID}`,
     spawn fresh Worker with note "the plan section may have changed; re-locate", attempt counter
     UNCHANGED.

4. Validate plan after apply:
   ```bash
   # Markdown sanity: file is non-empty, has at least 5 headings, no unterminated code fence
   PLAN_PATH="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
   test -s "$PLAN_PATH" && \
   test "$(grep -c '^#' "$PLAN_PATH")" -ge 5 && \
   test "$(grep -c '^```' "$PLAN_PATH")" -ge 0 && \
   [ "$(($(grep -c '^```' "$PLAN_PATH") % 2))" -eq 0 ] && \
   echo "validation OK" || echo "validation FAIL"
   ```
   If validation FAIL: restore `cp "$PLAN.bak.before-{ID}" "$PLAN"`, treat as REWORK with reason
   "applied edit broke markdown structure", increment attempt, go to R5.

5. Snapshot after:
   ```bash
   cp "$PLAN" "$PLAN.bak.after-{FINDING_ID}"
   ```

6. Append to `$RUN_DIR/ledger.txt`:
   ```
   {FINDING_ID}: APPROVED. {SUPERVISOR_VERDICT.ledger_entry}
   ```

7. Update journal: add `{FINDING_ID}` to `completed_findings`, reset `attempt_count` to 0, set
   `current_finding` to next.

8. Mark TaskUpdate status `completed` for the finding's task.

9. Continue to next per-finding task.

#### Branch B — REWORK

1. Append rework reason to `$RUN_DIR/run-log.md`.
2. Increment `attempt_count`.
3. If `attempt_count >= 3`: treat as ESCALATE_TO_USER with reason "rework limit hit". Go to
   Branch C.
4. Else: build `REWORK_HISTORY_BLOCK`:
   ```
   PRIOR ATTEMPT(S) — REWORK FEEDBACK YOU MUST ADDRESS:

   Attempt {N-1}: <one-line summary of what worker proposed>
   Supervisor feedback: <verbatim feedback_to_worker from R11>

   {repeat for each prior attempt}
   ```
5. Go back to R4 with the new REWORK_HISTORY_BLOCK. (Spawn fresh Worker subagent — R6 again.)

#### Branch C — ESCALATE_TO_USER

1. Build escalation message using the "Escalation Message Template" section at the end of this plan.
2. Use `AskUserQuestion` with 4 options:
   - Approve last attempt as-is (override Supervisor)
   - Provide custom direction (free text)
   - Skip this finding (record as deferred)
   - Abort entire run

3. Branch on user choice:
   - **Approve last attempt:** apply that attempt's edit (per Branch A steps 1-7), but append
     `OVERRIDE` flag to ledger entry. Mark task complete.
   - **Custom direction:** spawn one more Worker with the user's direction injected into
     `REWORK_HISTORY_BLOCK` as `USER OVERRIDE: <text>`. Reset attempt counter to 1. Go to R4.
   - **Skip:** append to ledger `{FINDING_ID}: SKIPPED (user-deferred). Reason: ESCALATE`.
     Mark task with description prefix `[SKIPPED]`. Continue to next finding.
   - **Abort:** record current state in journal (`status: aborted`), print summary of what was
     completed, exit. Plan stays at last `.bak.after-*` snapshot.

### Recipe end

When the recipe completes (Branch A or skipped), the Orchestrator advances to the next per-finding
task.

---

## Task 5: Apply finding C-1 — Extraction protocol rewrite (Phase 1)

**Finding:** C-1 — body-capture regex cannot produce byte-exact extraction.
**Synthesis report lines:** 44–95
**Plan sections likely affected:** "Boundary Marker Design", "Extraction regex", "Verification"
**Expectation:** `implement_as_recommended` with verbatim length-prefixed extraction code from C-1's
"Recommended fix" block. This is the most architecturally consequential fix.
**Risk note:** Worker may want to also fix M-4 (provide construction script) — that is a separate
finding. Supervisor must enforce check 6 (lane discipline).

**Step 1: Run the Worker Iteration Recipe (Task 4)** with:
- `FINDING_ID = "C-1"`
- `FINDING_LINE_START = 44`
- `FINDING_LINE_END = 95`

**Step 2: Verify outcome**

After recipe completes, confirm:
```bash
ls "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md.bak.after-C-1"
grep -c "length-prefixed\|FILE_SIZE_BYTES" "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
grep "<!-- =+ -->\\\\n\\\\n(.*?)\\\\n\\\\n" "$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md" || echo "old regex removed (good)"
```
Expected: snapshot exists; length-prefixed terminology present; old regex pattern absent.

---

## Task 6: Apply finding M-1 — read_text → read_bytes (Phase 2)

**Finding:** M-1 — `read_text()` is a latent bug.
**Synthesis report lines:** 141–150
**Plan sections likely affected:** Verification block (the Python script).
**Expectation:** `implement_as_recommended`. Replace `read_text(encoding='utf-8')` and
`body.encode('utf-8')` with `read_bytes()` and hash on raw bytes.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "M-1"`
- `FINDING_LINE_START = 141`
- `FINDING_LINE_END = 150`

**Step 2: Verify outcome**

```bash
PLAN="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
grep -c "read_bytes" "$PLAN"
grep -c "read_text" "$PLAN" | { read n; [ "$n" -le 1 ] && echo "read_text uses removed (≤1 mention OK)" || echo "STILL HAS read_text: $n"; }
```

---

## Task 7: Apply finding M-3 — Absolute paths in verification (Phase 2)

**Finding:** M-3 — verification script uses relative paths.
**Synthesis report lines:** 159–166
**Plan sections likely affected:** Verification block.
**Expectation:** `implement_as_recommended` or `implement_modified`. Worker should choose
`pathlib.Path(__file__).resolve().parent` only if the verification script is co-located with the
master file (it is, by L-2). Otherwise accept argv[1].

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "M-3"`
- `FINDING_LINE_START = 159`
- `FINDING_LINE_END = 166`

**Step 2: Verify outcome**

```bash
PLAN="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
grep -E "Path\(__file__\)|argv\[1\]" "$PLAN" && echo "absolute path approach present"
```

---

## Task 8: Apply finding M-4 — Provide inline Python construction script (Phase 3)

**Finding:** M-4 — no actual Python construction script provided.
**Synthesis report lines:** 167–178
**Plan sections likely affected:** "Implementation Steps" → step 2 (the construction step).
**Expectation:** `implement_as_recommended`. Worker provides a full Python script that:
- Reads each source file with `pathlib.Path(p).read_bytes()`
- Composes BEGIN block + body bytes + END block (no separator inserted, per C-1)
- Writes master with `open(path, 'wb')`
- Pinned 7-file allowlist (no globs — covers L-2)

**Risk note:** Worker may want to bundle L-2's allowlist comment. That's allowed — L-2's premise
check should then return `no_change_needed` (already covered by M-4).

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "M-4"`
- `FINDING_LINE_START = 167`
- `FINDING_LINE_END = 178`

**Step 2: Verify outcome**

```bash
PLAN="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
grep -c "read_bytes" "$PLAN"            # should be ≥2 now (verification + construction)
grep -E "open\(.*'wb'\)|open\(.*\"wb\"\)" "$PLAN" && echo "binary write mode present"
grep -c "next steps.txt" "$PLAN"        # should appear in pinned allowlist
```

---

## Task 9: Apply finding L-2 — Pinned allowlist comment (Phase 3)

**Finding:** L-2 — co-locating ARCHIVE_MASTER.md inside archive/ is a re-run hazard.
**Synthesis report lines:** 195–202
**Plan sections likely affected:** Construction script (M-4's output) OR Risks section.
**Expectation:** Likely `no_change_needed` if M-4's construction script already pinned the
7-file allowlist with an explicit "no globs" comment. Otherwise `implement_as_recommended` —
add the comment.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "L-2"`
- `FINDING_LINE_START = 195`
- `FINDING_LINE_END = 202`

**Step 2: Verify outcome**

```bash
PLAN="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
grep -iE "no glob|pinned.*7|allowlist" "$PLAN" && echo "pinning safeguard present"
```

---

## Task 10: Apply finding N-3 — Fix the "Why a script" rationale (Phase 3)

**Finding:** N-3 — plan's rationale for using a script is correct but undercuts itself.
**Synthesis report lines:** 257–end (read until next major section or EOF, ~270)
**Plan sections likely affected:** "Why a script instead of the Read/Write tools" rationale block.
**Expectation:** Likely `no_change_needed` if M-4 already provided the script (the criticism was
that the plan argued for a script but didn't include one — M-4 fixed that). If the rationale
prose still reads awkwardly, light prose edit.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "N-3"`
- `FINDING_LINE_START = 257`
- `FINDING_LINE_END = 270`  (Worker may need to read further; that's fine)

**Step 2: Verify outcome**

Spot-check the rationale section reads coherently with M-4's script in place.

---

## Task 11: Apply finding M-2 — Pre-flight collision wording (Phase 4)

**Finding:** M-2 — pre-flight collision check wording conflates two different checks.
**Synthesis report lines:** 151–158
**Plan sections likely affected:** "Pre-flight verification" paragraph.
**Expectation:** `implement_as_recommended`. Drop the claim about bare-60-equals being absent;
keep only the `<!--` collision check.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "M-2"`
- `FINDING_LINE_START = 151`
- `FINDING_LINE_END = 158`

**Step 2: Verify outcome**

```bash
PLAN="$HOME/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md"
# Bare 60-equals claim should be gone
grep -c "60-equals\|bare.*=\{60\}" "$PLAN" && echo "(check the matches; should be 0 or only inside finding-quote)"
```

---

## Task 12: Apply finding L-1 — FILE_LINES undercount note (Phase 4)

**Finding:** L-1 — FILE_LINES undercounts for 3 files.
**Synthesis report lines:** 179–194
**Plan sections likely affected:** Inventory table OR a clarifying note in Risks.
**Expectation:** `implement_as_recommended` or `implement_modified` (a one-line note explaining
that FILE_LINES uses `wc -l` semantics is sufficient).

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "L-1"`
- `FINDING_LINE_START = 179`
- `FINDING_LINE_END = 194`

---

## Task 13: Apply finding L-3 — Leading blank lines (Phase 4)

**Finding:** L-3 — `next-step-for-data-processing-pipeline.txt` starts with three blank lines.
**Synthesis report lines:** 203–208
**Plan sections likely affected:** Probably none after C-1.
**Expectation:** **Likely `no_change_needed`.** The finding says: "With the recommended length-
prefixed extraction, this is handled correctly." C-1 already landed length-prefixed extraction.
Worker's premise check should detect this and return `no_change_needed`.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "L-3"`
- `FINDING_LINE_START = 203`
- `FINDING_LINE_END = 208`

**Step 2: Verify outcome**

Confirm ledger entry says `no_change_needed`. If Worker proposed an actual edit, double-check
the Supervisor's reasoning — but trust the Supervisor's verdict.

---

## Task 14: Apply finding L-4 — YAML date convention (Phase 4)

**Finding:** L-4 — hardcoded date in YAML frontmatter.
**Synthesis report lines:** 209–214
**Plan sections likely affected:** Master File Structure → YAML example.
**Expectation:** `implement_as_recommended` or `implement_modified`. Specify how `generated:` is
injected (e.g., today's date at write time, set by the construction script).

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "L-4"`
- `FINDING_LINE_START = 209`
- `FINDING_LINE_END = 214`

---

## Task 15: Apply finding L-5 — Interior `---` mention (Phase 4)

**Finding:** L-5 — interior `---` lines in source .md files.
**Synthesis report lines:** 215–224
**Plan sections likely affected:** Risks/Notes section.
**Expectation:** `implement_as_recommended`. Add one bullet to Risks noting interior `---` in two
.md files; clarify they don't conflict with the master's YAML frontmatter (which only parses at
start-of-file).

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "L-5"`
- `FINDING_LINE_START = 215`
- `FINDING_LINE_END = 224`

---

## Task 16: Apply finding N-1 — Visual vs text marker contradiction (Phase 4)

**Finding:** N-1 — plan's visual example contradicts its textual `\n\n` instruction.
**Synthesis report lines:** 225–244
**Plan sections likely affected:** Probably none — C-1 either removed or rewrote the marker example.
**Expectation:** **Likely `no_change_needed`.** Per N-1: "with length-prefixed extraction, the
visual example becomes moot." If C-1's rewrite removed the visual example, no edit needed. If C-1
kept a visual example, this Worker may want to clarify it.

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "N-1"`
- `FINDING_LINE_START = 225`
- `FINDING_LINE_END = 244`

---

## Task 17: Apply finding N-2 — Marker overhead estimate (Phase 4)

**Finding:** N-2 — marker block overhead estimate is slightly off.
**Synthesis report lines:** 245–256
**Plan sections likely affected:** Post-write line-count estimate paragraph in Implementation Steps.
**Expectation:** `implement_as_recommended` — update the line-count estimate from ~4,154 to ~4,161
(or similar, depending on whether C-1 changed the marker block).

**Step 1: Run the Worker Iteration Recipe** with:
- `FINDING_ID = "N-2"`
- `FINDING_LINE_START = 245`
- `FINDING_LINE_END = 256`

---

## Task 18: Final E2E integration test

This is the moment of truth. The patched plan must produce a working ARCHIVE_MASTER.md and pass
its own verification block.

**Files:**
- Read: `$PLAN` (the patched version)
- Create temporary: `/tmp/build_archive_master.py`
- Create temporary: `/tmp/verify_archive_master.py`
- Create: `$ARCHIVE_DIR/ARCHIVE_MASTER.md` (the output we are testing)

**Step 1: Extract the construction script from the patched plan**

The plan should now contain (per M-4) a full Python construction script in the Implementation Steps
section. Locate it (look for ```python ... ``` fence inside step 2 of Implementation Steps). Save
its contents to `/tmp/build_archive_master.py`.

If you cannot find the construction script: this means M-4 didn't actually deliver the script
(should have been caught by Supervisor). Escalate to user with: "Patched plan still doesn't contain
a construction script. Re-run M-4?"

**Step 2: Extract the verification script from the patched plan**

The plan's Verification section contains a `python3 - <<'PY' ... PY` heredoc. Extract the Python
inside the heredoc to `/tmp/verify_archive_master.py`. Add `#!/usr/bin/env python3` shebang and
make it executable.

**Step 3: Run the construction script**

```bash
cd "$HOME/Desktop/3_body_problem"   # in case the script uses relative paths
python3 /tmp/build_archive_master.py 2>&1 | tee /tmp/build_output.log
echo "exit code: $?"
ls -la "$HOME/Desktop/3_body_problem/pinn_instruction/original_latex/review-of-framework/issues/archive/ARCHIVE_MASTER.md"
```
Expected: ARCHIVE_MASTER.md exists, size ~250-260 KB (sum of 7 source files plus marker overhead).

If the script fails or output is wrong size: escalate to user with full output.

**Step 4: Run the verification script**

```bash
cd "$HOME/Desktop/3_body_problem"
python3 /tmp/verify_archive_master.py 2>&1 | tee /tmp/verify_output.log
echo "exit code: $?"
```
Expected: `PASS: 7/7 files extracted, all SHA-256 hashes match originals.` and exit 0.

**Step 5: Branch on result**

#### If PASS

1. Append to `$RUN_DIR/run-log.md`:
   ```
   ## Final E2E Test — PASS

   Construction: built ARCHIVE_MASTER.md at <path>, size <N> bytes
   Verification: 7/7 SHA round-trip
   ```
2. Mark TaskUpdate "Run final E2E integration test" as `completed`.
3. Update journal: `status: success`.
4. Continue to Task 19.

#### If FAIL

1. Append failure details to run-log:
   ```
   ## Final E2E Test — FAIL

   Construction output: <last 50 lines of /tmp/build_output.log>
   Verification output: <full /tmp/verify_output.log>
   First failing finding (best guess based on which file's hash mismatched): <finding>
   ```

2. Use `AskUserQuestion`:
   - Question: "E2E test failed. How to proceed?"
   - Options:
     - "Bisect" — Re-run E2E against each `.bak.after-{ID}` snapshot to find the first one that
       breaks the test. Identifies which finding's fix is at fault.
     - "Roll back" — Restore plan from `.bak.original`, mark run as failed.
     - "Show diff" — Display diff between `.bak.original` and current plan; let user decide manually.

3. Branch on choice; in all cases the abort path keeps snapshots intact for forensic review.

---

## Task 19: Final report and cleanup

**Step 1: Generate run summary**

Append to `$RUN_DIR/run-log.md`:

```
# Run Summary

Started: <from journal>
Ended: <ISO 8601 now>
Duration: <computed>

Findings processed: <count>
- Approved as_recommended: <count>
- Approved modified: <count>
- Approved no_change_needed: <count>
- Skipped (escalation): <count>
- Override (user approved): <count>

Snapshots retained:
- Original: <path>
- Per-finding before/after: <count>

Final plan SHA-256: <shasum>
Final plan size: <bytes>

E2E test result: PASS | FAIL
```

**Step 2: Print the summary to the user**

Use plain text output (not just file). Show the user:
- One-line per finding: "C-1 ✓ APPROVED implement_as_recommended"
- E2E result
- Path to run-log

**Step 3: Decide on snapshot retention**

Use `AskUserQuestion`:
- "Run is complete. Keep all per-finding snapshots, or clean them up?"
- Options:
  - Keep all (audit trail intact)
  - Keep only `.bak.original` and `.bak.after-N-2` (final state)
  - Clean all `.bak.*` (risky — no rollback after this)

Apply user choice.

**Step 4: Done**

The patched plan at `$PLAN` is now executable. The final E2E pass proves it. The user can run the
plan's construction step at any time to regenerate ARCHIVE_MASTER.md.

---

## Escalation Message Template (referenced from Task 4 Branch C)

When ESCALATE_TO_USER fires (either Supervisor verdict or rework limit hit), build a message
like this:

```
ESCALATION — finding {FINDING_ID}

Reason: {Supervisor's escalation_reason OR "rework limit (3) hit"}

Finding text:
---
{FINDING_TEXT — full verbatim}
---

Worker attempts:

  Attempt 1:
    chosen_approach: {worker_output.chosen_approach}
    Worker's edit summary: {one-line description of what they proposed}
    Supervisor verdict: {APPROVE | REWORK | ESCALATE}
    Supervisor reason: {feedback_to_worker or escalation_reason}

  Attempt 2: {if any}
    ...

  Attempt 3: {if any}
    ...

Current plan state at this finding's section:
---
{relevant excerpt from CURRENT_PLAN_TEXT — find by Worker's target_locator if available}
---

Your options:
  [1] Approve last attempt as-is (override Supervisor)
  [2] Provide custom direction (free text)
  [3] Skip this finding (record as deferred, continue loop)
  [4] Abort entire run (snapshots preserved at {snapshot directory})
```

Render via `AskUserQuestion` with the 4 options. Free text for option 2 captured via the user's
"Other" option.

---

## What "Done" Looks Like

- All 13 per-finding tasks (Tasks 5-17) marked `completed` in the task tracker
- Task 18 (Final E2E) marked `completed` with PASS recorded
- `$RUN_DIR/run-log.md` contains the full audit trail
- `$RUN_DIR/journal.json` shows `status: success`
- Patched plan at `$PLAN` produces a valid ARCHIVE_MASTER.md when its construction script is run
- The plan's verification script prints `PASS: 7/7 files extracted, all SHA-256 hashes match originals.`
- `.bak.original` snapshot is preserved (whatever the user chose for other snapshots)

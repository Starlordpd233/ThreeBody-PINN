# Phase 20.5 - Plan Part 3 of 3: Closure & Status Synchronization (Tasks 9)

### Precondition

Do not execute until Task 0 in `20-5-PLAN.md` has passed in this session. The Non-Execution
Guard and Git context in `20-5-PLAN.md` apply to every task here.

### Guardrails

- Commit via `scripts/agent-commit` with `GIT_AGENT_ID` set. Never raw `git commit`, never
  `--no-verify`.
- Stage only explicitly named files. Never `git add -A` or `git add .`.
- Exclude any pre-existing unrelated working-tree edits from staging.
- No destructive operations (no resets, rebases, force-pushes, branch deletions).
- STOP and surface any decision that is not grounded per the `20-5-PLAN.md` Non-Execution
  Guard.

### Navigation

- Back to index: [`20-5-PLAN.md`](./20-5-PLAN.md)
- Previous: [`20-5-PLAN-part2.md`](./20-5-PLAN-part2.md)
- Next: (this is the last part)

---

## Task 9: Final Phase 20.5 closure and status synchronization

**Files:**
- Modify: `.planning/REQUIREMENTS.md`
- Modify: `.planning/ROADMAP.md`
- Modify: `.planning/STATE.md`
- Modify: `.planning/MILESTONES.md`
- Modify: `.planning/PROJECT.md`

This task runs only after Tasks 1–8 have completed successfully. It performs mechanical status
bookkeeping: SAMP-01/02 move from `Pending` to `Complete`, the Phase 20.5 ROADMAP entry moves
from planned to complete, and active planning docs point to Phase 21 as the next phase. Do not
change the SCOPE-05 rule text, the Sobol convention, the gap resolutions, or any physics/spec
content in this task.

- [ ] **Step 1: Verify closure prerequisites**

Run from the repository root:
```bash
SPEC=pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
DA=.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md
PROBE=.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py

grep -cF "### Phase 20.5: Sampling Coordinate Allocation" .planning/ROADMAP.md       # expect 1
grep -cF "**SAMP-01**:" .planning/REQUIREMENTS.md                                    # expect 1
grep -cF "**SAMP-02**:" .planning/REQUIREMENTS.md                                    # expect 1
grep -cF "| SAMP-01 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md              # expect 1 before closure flip
grep -cF "| SAMP-02 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md              # expect 1 before closure flip
grep -c "^#### Sobol Coordinate Allocation Convention$" "$SPEC"                      # expect 1
grep -cF 'u_{4+\delta_s}' "$SPEC"                                                    # expect >= 1
test -f "$DA"
grep -cF "AC-SAMP-01" "$DA"                                                          # expect >= 2
test -f "$PROBE"
.venv/bin/python3 "$PROBE"
```
If any prerequisite fails, STOP and return to the task that owns that artifact. Do not mark
Phase 20.5 complete until the prerequisite artifact is present and verified.

- [ ] **Step 2: Mark SAMP traceability complete**

In `.planning/REQUIREMENTS.md`, replace:
```markdown
| SAMP-01 | Phase 20.5 | Pending |
| SAMP-02 | Phase 20.5 | Pending |
```
With:
```markdown
| SAMP-01 | Phase 20.5 | Complete |
| SAMP-02 | Phase 20.5 | Complete |
```

Update the final `Last updated` note so it records Phase 20.5 completion and Phase 21 as next.
Do not change the Phase 21 VER rows, which remain `Pending`.

- [ ] **Step 3: Mark ROADMAP Phase 20.5 complete**

In `.planning/ROADMAP.md`, update only the Phase 20.5 top-level list item and progress row:
- Change the Phase 20.5 checkbox from `- [ ]` to `- [x]`.
- Replace the trailing "execution pending" wording with completion wording that includes the
  execution date.
- Change the progress row from `0/1 | Planned (design+plan locked) | -` to
  `1/1 | Complete | <execution date>`.
- Update the final `Last updated` note to say Phase 20.5 is complete and Phase 21 is next.

Do not alter Phase 21 scope or success criteria here.

- [ ] **Step 4: Update active state docs narrowly**

In `.planning/STATE.md`, `.planning/MILESTONES.md`, and `.planning/PROJECT.md`, update only
active-status text that says Phase 20.5 execution is pending. The new state should say Phase
20.5 is complete and Phase 21 is next. Preserve historical notes that identify `b727b15` as
the design/plan-lock commit and `a9ecd51` as the prior status-record commit; do not rewrite
those roles.

If a status sentence is ambiguous or appears to encode a new project decision rather than
bookkeeping, leave it unchanged and surface it separately. This task is not authority for a
new milestone-scope decision.

- [ ] **Step 5: Verify final status synchronization**

Run:
```bash
grep -cF "| SAMP-01 | Phase 20.5 | Complete |" .planning/REQUIREMENTS.md             # expect 1
grep -cF "| SAMP-02 | Phase 20.5 | Complete |" .planning/REQUIREMENTS.md             # expect 1
grep -cF "| SAMP-01 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md              # expect 0
grep -cF "| SAMP-02 | Phase 20.5 | Pending |" .planning/REQUIREMENTS.md              # expect 0
grep -cF "| 20.5 Sampling Coordinate Allocation (INSERTED) | v1.4 | 1/1 | Complete |" .planning/ROADMAP.md  # expect 1
rg -n "Phase 20\\.5.*execution pending|Execute Phase 20\\.5|Plan: Next — Phase 20\\.5" \
  .planning/ROADMAP.md .planning/STATE.md .planning/MILESTONES.md .planning/PROJECT.md
```
The final `rg` should return no active pending/execute-next status lines. If it returns a
historical note that should be preserved, document why before committing; otherwise update the
stale active status text and re-run the check.

- [ ] **Step 6: Commit**

Stage only the five status files and commit with `scripts/agent-commit` (body required —
multi-file `.planning/` commit):
```bash
git add .planning/REQUIREMENTS.md .planning/ROADMAP.md .planning/STATE.md .planning/MILESTONES.md .planning/PROJECT.md
GIT_AGENT_ID="codex-gpt-5" scripts/agent-commit \
  -m "docs(planning): close Phase 20.5 execution state" \
  -m "Mark SAMP-01 and SAMP-02 complete after the Phase 20.5 spec, probe, and data-alignment hand-off pass. Update ROADMAP progress and active planning status so Phase 20.5 is complete and Phase 21 is next, without changing the Sobol convention or SCOPE-05 rule text."
```

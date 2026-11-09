Here are the exact steps for each manual verification check:

  ---
  D1: Cross-worktree two-session live handoff

  What this proves: B in a linked worktree wakes unattended, integrates A's head, and begins its task.

  Prerequisites:
  - Two Claude Code sessions open in the same repo (3_body_problem)
  - Session A: main worktree on master
  - Session B: linked worktree on its own branch

  Exact steps:

  Session B (consumer)

  # In the 3_body_problem directory, create a linked worktree
  git worktree add -q .worktrees/wd-consumer -b wd-consumer master

  # Change to the worktree
  cd .worktrees/wd-consumer

  # Create a consumer task file
  cat > consumer-task.md << 'EOF'
  # Task for B when WAKE occurs

  Run these commands in order:
  1. tools/watchdog/wd-integrate --channel xw-live
  2. tools/watchdog/wd-check --channel xw-live --require-integration
  3. Report the integrated head (run: git log -1 --oneline)

  If ALREADY-CLAIMED or PRODUCER-STALLED, stop and report.
  EOF

  # Arm the watchdog in the background
  tools/watchdog/wd-arm --channel xw-live --poll-secs 20 --timeout-secs 1800 --task-file consumer-task.md &

  # Note the PID that prints (e.g., "Watchdog armed with PID: 12345")
  # End your turn - B will wake unattended when A publishes

  Session A (producer)

  # Stay in the main 3_body_problem worktree (not the .worktrees one)
  # Make a trivial change
  echo "test $(date)" > test-file.txt
  git add test-file.txt
  git commit -m "test: cross-worktree handoff demo"

  # Publish the done marker
  tools/watchdog/wd-publish-done --channel xw-live --stage demo --scope "test-file.txt"

  What to observe

  In Session B's terminal (the one running wd-arm), you should see:
  WAKE <commit-hash>

  The Claude harness should re-enter Session B unattended, run the integration commands, and report the result.

  Cleanup

  # From Session B
  tools/watchdog/wd-disarm --channel xw-live
  cd ..
  git worktree remove .worktrees/wd-consumer

  Evidence to record

  Create tools/watchdog/evidence/<date>-xworktree-live-handoff.md with:
  - Result: PASS/FAIL
  - Wake latency (time from A's publish to B's re-entry)
  - Observed re-entry mode (background-Bash-exit)
  - Environment (macOS version, Claude Code version)
  - Steps run (verbatim commands)
  - Observed output

  ---
  D2: Real PUSH with real tmux

  What this proves: External tmux injector can wake an idle Claude pane via keyboard injection.

  Prerequisites:
  - tmux installed
  - Two Claude Code sessions
  - Session B running in a tmux pane

  Exact steps:

  Session setup (operator terminal)

  # Create a tmux session with a Claude pane
  tmux new-session -d -s wd -n claude
  tmux send-keys -t wd:0 "cd /path/to/3_body_problem" Enter
  tmux send-keys -t wd:0 "claude" Enter

  # Let Claude start, then wait for idle prompt
  # Press Enter to get to a clean prompt
  tmux send-keys -t wd:0 Enter

  # Note the pane target: wd:0.0

  Session B (in tmux pane wd:0.0)

  # Create consumer task
  cat > consumer-task.md << 'EOF'
  # Task when WAKE via PUSH occurs

  Report: "Woke via tmux PUSH injection at $(date)"
  EOF

  # Arm the watchdog (via Claude's Bash tool)
  tools/watchdog/wd-arm --channel push-live --poll-secs 10 --timeout-secs 900 --task-file consumer-task.md &

  Session A (producer)

  # Make a commit
  echo "push test" > push-test.txt
  git add push-test.txt
  git commit -m "test: PUSH wake demo"

  # Publish done marker
  tools/watchdog/wd-publish-done --channel push-live --stage demo --scope "push-test.txt"

  From operator terminal (NOT Session B's pane)

  # Run wd-push - it will poll and inject when WAKE detected
  tools/watchdog/wd-push --channel push-live --pane wd:0.0 --poll-secs 10 --timeout-secs 900

  What to observe

  wd-push should print:
  PUSHED <commit-hash>

  In the tmux pane (wd:0.0), you should see the fixed wake prompt get injected, and Session B should re-enter and run the task.

  Verification

  # Re-run wd-push - should say ALREADY-CLAIMED
  tools/watchdog/wd-push --channel push-live --pane wd:0.0 --poll-secs 10 --timeout-secs 900
  # Expected: "ALREADY-CLAIMED <commit-hash>"

  # Check claim exists
  ls .git/live-monitor/channels/push-live/claimed.*

  # Cleanup
  tools/watchdog/wd-disarm --channel push-live

  Evidence to record

  Create tools/watchdog/evidence/<date>-real-push.md with the same fields as D1.

  ---
  D3: P2 cron under termination contract

  What this proves: The durable cron path respects its termination contract (disarm-on-success + TTL self-termination + on-disk
  verification).

  Prerequisites:
  - One Claude Code session
  - Foreground tab (macOS CronCreate pauses in background)

  Exact steps:

  Create consumer task

  cat > consumer-task.md << 'EOF'
  # P2 cron task

  Report: "Woke via P2 cron at $(date)"
  EOF

  Arm P2 (require explicit "yes, durable" + TTL)

  When Claude asks for confirmation, type: yes, durable

  # Arm with a short TTL (60 seconds) to test self-termination
  tools/watchdog/wd-arm --channel p2-test --poll-secs 10 --timeout-secs 120 --ttl 60 --task-file consumer-task.md

  # Expected: warning about foreground tab caveat, then "Watchdog armed"

  Step 1: Verify job is on disk (IMMEDIATELY after arming)

  # Check via Claude Code's CronList
  # In Claude: ask to list cron jobs (or check if there's a /cron command)

  # Check the file directly
  cat ~/.claude/scheduled_tasks.json | grep -A 5 p2-test

  # BOTH must show the job for the arm to be considered complete

  Step 2: Trigger wake and observe disarm-on-success

  # In another terminal, publish done
  echo "p2 test" > p2-test.txt
  git add p2-test.txt
  git commit -m "test: P2 cron"
  tools/watchdog/wd-publish-done --channel p2-test --stage demo --scope "p2-test.txt"

  # In Claude session, wait for wake
  # Expected: job self-deletes via CronDelete BEFORE running the task
  # armed.json should be removed

  Step 3: Verify TTL self-termination

  # Arm again with a short TTL, DON'T publish
  tools/watchdog/wd-arm --channel p2-test-ttl --poll-secs 10 --timeout-secs 120 --ttl 10 --task-file consumer-task.md

  # Wait 10+ seconds
  # Expected: job deletes itself, armed.json removed, no leftover cron

  Step 4: Verify wd-disarm --all cleanup

  # If anything is still armed
  tools/watchdog/wd-disarm --all

  # Verify nothing live
  tools/watchdog/wd-status
  # Expected: empty output (no active arms)

  Evidence to record

  Create tools/watchdog/evidence/<date>-p2-cron-contract.md with the same fields, noting:
  - Job verified on disk (both CronList and .claude/scheduled_tasks.json)
  - Disarm-on-success observed
  - TTL self-termination observed
  - Foreground caveat surfaced
  - No stranded cron after run

  ---
  E1: Discovery / load in each profile

  What this proves: The skill is surfaced and loadable in every CCP profile, even from foreign CWD.

  Prerequisites:
  - Multiple CCP profiles installed (alt/free/max)

  Exact steps:

  # Test each profile that exists
  for profile in "" "alt" "free" "max"; do
      if [ -n "$profile" ]; then
          profile_dir=".claude-$profile"
      else
          profile_dir=".claude"
      fi

      if [ ! -d "$HOME/$profile_dir" ]; then
          echo "SKIP: $profile_dir does not exist"
          continue
      fi

      echo "Testing profile: $profile_dir"

      # Start Claude in this profile
      CLAUDE_PROFILE_DIR="$HOME/$profile_dir" claude --project /tmp/test-project << EOF
  Run this command and show me the result:
  ~/.claude/skills/cross-session-watchdog/bin/wd-status
  EOF

  done

  Step 2: Test from foreign project directory

  # From a directory that is NOT 3_body_problem
  cd /tmp
  mkdir test-foreign-cwd && cd test-foreign-cwd
  git init -q
  git config user.email "test@example.com"
  git config user.name "Test"
  echo "test" > README.md
  git add README.md
  git commit -q -m "init"

  # Start Claude here and verify skill loads
  claude --project . << EOF
  Check if the cross-session-watchdog skill is available. Then run:
  ~/.claude/skills/cross-session-watchdog/bin/wd-status
  EOF

  What to verify

  - Skill loads in each present profile
  - $HOME/.claude/skills/cross-session-watchdog/bin/wd-status runs and exits 0
  - Tools resolve to executables (not broken symlinks)

  Evidence to record

  Create tools/watchdog/evidence/<date>-global-discovery.md with:
  - Each profile tested and result
  - Foreign CWD test result
  - Any failures or missing profiles

  ---
  E2: Foreign-project live within-project handoff

  What this proves: Global deployment is real - a handoff works in a project other than 3_body_problem.

  Prerequisites:
  - A second git repo Y ≠ 3_body_problem
  - Two Claude Code sessions

  Exact steps:

  Setup: Create a foreign project

  mkdir /tmp/foreign-watchdog-test && cd /tmp/foreign-watchdog-test
  git init -q
  git config user.email "test@example.com"
  git config user.name "Test"
  echo "Foreign project" > README.md
  git add README.md
  git commit -q -m "init"

  Session B (in foreign project)

  cd /tmp/foreign-watchdog-test

  cat > consumer-task.md << 'EOF'
  # Foreign project watchdog task

  Report: "Handoff successful at $(date) in $(pwd)"
  EOF

  # Arm with ABSOLUTE tool path (critical - tests global install)
  ~/.claude/skills/cross-session-watchdog/bin/wd-arm --channel fp-live --poll-secs 20 --timeout-secs 900 --task-file
  consumer-task.md &

  Session A (in foreign project)

  cd /tmp/foreign-watchdog-test

  # Make a change
  echo "change in foreign project" > test.txt
  git add test.txt
  git commit -m "test: foreign project handoff"

  # Publish using ABSOLUTE tool path
  ~/.claude/skills/cross-session-watchdog/bin/wd-publish-done --channel fp-live --stage demo --scope "test.txt"

  What to verify

  # Check channel resolved under the foreign project's .git
  ls /tmp/foreign-watchdog-test/.git/live-monitor/channels/fp-live/

  # Should see: done.json and claimed.<hash>
  cat /tmp/foreign-watchdog-test/.git/live-monitor/channels/fp-live/done.json

  CRITICAL: If this fails, global deployment is NOT real (highest-severity finding).

  Evidence to record

  Create tools/watchdog/evidence/<date>-foreign-project-resolution.md with all fields, noting:
  - Channel resolved under foreign project's .git/live-monitor/…
  - B woke and ran the task
  - Used absolute tool paths from ~/.claude/...

  ---
  E3: Fresh-agent instruction-following rehearsal

  What this proves: An agent can correctly execute a watchdog handoff using ONLY the skill text (no repo context).

  Prerequisites:
  - A fresh Claude session with no prior context

  Exact steps:

  Step 1: Start a fresh agent

  Open a new Claude session with minimal or no context. Give it this task:

  Use the cross-session-watchdog skill to hand off from Agent A to Agent B.

  Agent A should:
  1. Create a file named "hello.txt" with content "world"
  2. Commit the change
  3. Publish the done marker

  Agent B should:
  1. Arm and wait
  2. When it wakes, report the content of hello.txt

  Use only the cross-session-watchdog skill documentation. Do not reference any prior context or this conversation.

  Step 2: Observe the agent's execution

  Watch for these potential misreads (record as findings):

  ┌────────────────┬─────────────────────────────────────────────────────────┬────────────────────────────────────┐
  │     Check      │                    Correct behavior                     │          Finding if wrong          │
  ├────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────┤
  │ Tool paths     │ Uses absolute paths from ~/.claude/.../bin/             │ Uses repo-relative tools/watchdog/ │
  ├────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────┤
  │ Wake prompt    │ Uses the FIXED wake prompt verbatim                     │ Interpolates channel file contents │
  ├────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────┤
  │ Order          │ Arms → waits → wakes → begins task                      │ Wrong order                        │
  ├────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────┤
  │ Cross-worktree │ Uses wd-integrate before wd-check --require-integration │ Skips integration                  │
  ├────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────┤
  │ P2 gating      │ Surfaces "yes, durable" requirement for P2              │ Tries P2 without gating            │
  └────────────────┴─────────────────────────────────────────────────────────┴────────────────────────────────────┘

  Step 3: Verify correctness

  # Check the result
  cat hello.txt  # Should contain "world"

  Evidence to record

  Create tools/watchdog/evidence/<date>-agent-rehearsal.md with:
  - Result: PASS/FAIL
  - Every misread observed with severity
  - The exact mistakes (wrong path, interpolated prompt, wrong order, etc.)

  ---
  F1: Dogfooded A→B acceptance run (after G0-G4 complete)

  What this proves: The watchdog can verify itself - B's armed task is to run the full test suite.

  Prerequisites:
  - G0-G4 all PASS

  Exact steps:

  Session B

  cd <home>/Desktop/3_body_problem

  cat > consumer-task.md << 'EOF'
  # Watchdog self-verification task

  Run the full watchdog test suite and report results:

  python3 -m unittest discover -s tests/watchdog -v

  Report: PASS count / total count
  EOF

  # Arm with background watcher
  tools/watchdog/wd-arm --channel dogfood --poll-secs 20 --timeout-secs 1800 --task-file consumer-task.md &

  Session A

  cd <home>/Desktop/3_body_problem

  # Make a trivial commit
  echo "dogfood" > dogfood-test.txt
  git add dogfood-test.txt
  git commit -m "test: watchdog self-verification"

  # Publish done marker
  tools/watchdog/wd-publish-done --channel dogfood --stage self-verify --scope "dogfood-test.txt"

  What to observe

  Session B wakes unattended, runs the test suite, reports results:
  - Expected: 45 tests pass (or current count)
  - Any failures would be a CRITICAL finding

  Evidence to record

  Run the full watchdog test suite and report results:

  python3 -m unittest discover -s tests/watchdog -v

  Report: PASS count / total count
  EOF

  # Arm with background watcher
  tools/watchdog/wd-arm --channel dogfood --poll-secs 20 --timeout-secs 1800 --task-file consumer-task.md &

  Session A

  cd <home>/Desktop/3_body_problem

  # Make a trivial commit
  echo "dogfood" > dogfood-test.txt
  git add dogfood-test.txt
  git commit -m "test: watchdog self-verification"

  # Publish done marker
  tools/watchdog/wd-publish-done --channel dogfood --stage self-verify --scope "dogfood-test.txt"

  What to observe

  Session B wakes unattended, runs the test suite, reports results:
  - Expected: 45 tests pass (or current count)
  - Any failures would be a CRITICAL finding

  Evidence to record

  Create tools/watchdog/evidence/<date>-dogfood-capstone.md with all standard fields plus:
  - Test suite output (PASS count / total count)
  - Any failures or anomalies
  - Any failures would be a CRITICAL finding

  Evidence to record

  Create tools/watchdog/evidence/<date>-dogfood-capstone.md with all standard fields plus:
  - Test suite output (PASS count / total count)
  - Any failures or anomalies

  ---
  Commits for each evidence file

  After each D/E/F task, commit the evidence:

  # Replace <date> and <task-name> appropriately
  git add tools/watchdog/evidence/<date>-<task-name>.md tools/watchdog/VERIFICATION-CHECKLIST.md
  GIT_AGENT_ID="<your-name>" GIT_AGENT_OWNED_PATHS="tools/watchdog/evidence/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
    scripts/agent-commit -m "evidence(governance): record <task-name>" \                                                             -m "T<test-number> / G<gate-number>: <brief description>"
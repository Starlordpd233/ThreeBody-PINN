---
date: "2026-06-22 00:34"
promoted: false
---

Post-update repair checklist for this machine and project.

Context: On 2026-06-21/2026-06-22, marketplace and plugin cache issues were investigated across Claude Code profiles, Codex, claude-mem, context-mode, and GSD. The earlier Claude Code errors were primarily marketplace/cache/scope issues, not evidence that project memory stores were corrupt. The profile/plugin checks are currently clean.

Current verified state:
- Claude profiles `.claude`, `.claude-free`, `.claude-alt`, and `.claude-max` all return `claude plugin list --json` successfully.
- `claude-mem` repair checks pass:
  - `tools/claude-mem-codex-hooks-check.cjs` passes for 12 files.
  - `tools/claude-mem-worker-protocol-check.cjs` passes for 12 bundles and 72 mode files.
  - `tools/claude-mem-profile-audit.cjs` passes for all four Claude profile roots, 16 env entries, and Codex config.
- `context-mode` Codex doctor passes: hooks, FTS5/SQLite, storage, server test, plugin registration, and version are OK.
- GSD Codex validation passes: all expected agents are installed, runtime resolves to `codex`, and `workflow.use_worktrees` resolves to `false`.

Routine after updating Claude Code, Codex, Claude plugin marketplaces, claude-mem, context-mode, or GSD:

```bash
# Claude profile plugin cache sanity checks
CLAUDE_CONFIG_DIR="$HOME/.claude" claude plugin list --json >/dev/null
CLAUDE_CONFIG_DIR="$HOME/.claude-free" claude plugin list --json >/dev/null
CLAUDE_CONFIG_DIR="$HOME/.claude-alt" claude plugin list --json >/dev/null
CLAUDE_CONFIG_DIR="$HOME/.claude-max" claude plugin list --json >/dev/null

# claude-mem post-update drift checks
cd "$HOME/Desktop/3_body_problem"
node tools/claude-mem-codex-hooks-repair.cjs --dry-run
node tools/claude-mem-worker-protocol-repair.cjs --dry-run
node tools/claude-mem-codex-hooks-check.cjs
node tools/claude-mem-worker-protocol-check.cjs
node tools/claude-mem-profile-audit.cjs

# context-mode / Codex hook health
ctx doctor

# GSD Codex health, especially after GSD updates
node "$HOME/.codex/gsd-core/bin/gsd-tools.cjs" validate agents
node "$HOME/.codex/gsd-core/bin/gsd-tools.cjs" config-get runtime --default codex --raw
node "$HOME/.codex/gsd-core/bin/gsd-tools.cjs" config-get workflow.use_worktrees --default false --raw
```

Repair policy:
- If the claude-mem dry-runs report drift, run the non-dry versions:
  - `node tools/claude-mem-codex-hooks-repair.cjs`
  - `node tools/claude-mem-worker-protocol-repair.cjs`
- Do not run `tools/claude-mem-install.sh` for routine repair. It is closer to reinstall/upgrade behavior.
- After Claude Code marketplace/plugin updates, run `/reload-plugins` in already-open Claude sessions.
- Prefer HTTPS marketplace sources over SSH for public marketplaces to avoid `known_hosts` failures.
- For GSD updates, create a snapshot of `~/.codex`, `~/.gsd`, and relevant project `.planning` state first. If local Codex adaptations are displaced, use GSD's `--reapply` path before hand-patching.
- For context-mode, prefer `ctx doctor` first and `ctx upgrade` only when intentionally updating context-mode.

Important separation:
- Promoting `claude-mem` or `context-mode` to user-level does not by itself merge project memory/session data. claude-mem data is project-keyed in its database, and context-mode session/content storage records project/session context.
- Running Claude Code or Codex from a different directory can change which project-scoped settings/plugins/hooks are active, so always reproduce plugin-cache errors from the same directory/profile where they occur.

Useful local artifacts:
- claude-mem repair/audit scripts live in `tools/claude-mem-*.cjs` and `tools/lib/`.
- The GSD update workflow and reapply guidance live under `$HOME/.codex/gsd-core/workflows/update.md` and `$HOME/.codex/gsd-core/workflows/reapply-patches.md`.
- Previous backup directories from claude-mem repairs are under `$HOME/.claude-mem/backups/`.

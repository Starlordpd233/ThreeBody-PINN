# Provider Config Reference

Companion to `SKILL.md`. Verified facts for this machine. **The env-var table reflects a
specific Claude Code version — re-run the grep method against your installed version before
trusting it. Do not treat this table as eternal truth; treat the *method* as the truth.**

> Last verified: **Claude Code v2.1.177**, 2026-06-13.

## 1. Verify an env var against the installed binary (ground truth)

The installed Claude Code CLI — not the Anthropic SDK — decides which variables are real.

```bash
ls -la "$(command -v claude)"     # follow wrapper/symlink to the real bundle
claude --version                  # e.g. 2.1.177
# Resolve the versioned binary (macOS default install):
bin=~/.local/share/claude/versions/$(claude --version | awk '{print $1}')
# Is a variable recognized? (exact-string search of the binary)
strings "$bin" | grep -F 'CLAUDE_CODE_MAX_CONTEXT_TOKENS'
```

A string **present** in the binary ⇒ recognized. **Absence** in `strings` output is
*suggestive, not conclusive* for a compiled/minified binary — re-check spelling and try the
provider/official docs. Never conclude "real/not real" from grepping `@anthropic-ai/sdk` or
the Python/TS API client; that is a different package.

## 2. Verified variables (Claude Code v2.1.177)

### Environment variables (set per-profile via CCP — see §3)

| Var | Status | Notes |
|---|---|---|
| `ANTHROPIC_BASE_URL` | REAL | Anthropic-compatible endpoint; **required** for third-party providers. |
| `ANTHROPIC_AUTH_TOKEN` | REAL | Bearer token; preferred over `ANTHROPIC_API_KEY` for these providers. |
| `ANTHROPIC_MODEL` | REAL | Main model id. |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` / `_SONNET_MODEL` / `_HAIKU_MODEL` | REAL | Map Claude tiers → provider models. |
| `CLAUDE_CODE_SUBAGENT_MODEL` | REAL | Model for subagents. |
| `API_TIMEOUT_MS` | REAL | Request timeout; raise for long agent runs. |
| `CLAUDE_CODE_EFFORT_LEVEL` | REAL | `low`/`medium`/`high`/`xhigh`/`max`. Overrides settings `effortLevel`. CCP sets it via the profile `effort` key. |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | REAL | Auto-compact threshold; set to the model's context size. |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | REAL | Declares the model's context size to the harness. |
| `ENABLE_TOOL_SEARCH` | REAL | Use `"0"`/`"1"` (not `"false"`). Some providers require `"0"`; if the doc is silent, leave at default and set `"0"` only if tool calls fail. |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | REAL | Disables Anthropic beta headers (provider compatibility). |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | REAL | Turns off non-essential telemetry. |
| `CLAUDE_CODE_DISABLE_THINKING` | REAL | Disables thinking. Do **not** set if you want thinking. |
| `MAX_THINKING_TOKENS` | REAL | Thinking budget. If the provider doc gives no value, **leave unset** and rely on effort. |
| `MAX_MCP_OUTPUT_TOKENS` | REAL | Caps MCP tool output. |

### settings.json keys (these are SHARED across all profiles — avoid for per-provider tuning)

| Key | Status | Notes |
|---|---|---|
| `effortLevel` | REAL | `low`/`medium`/`high`/`xhigh`. Shared default; override per-provider via the `CLAUDE_CODE_EFFORT_LEVEL` env (profile `effort` key). |
| `alwaysThinkingEnabled` | REAL (boolean) | Shared; no per-profile env equivalent. |
| `model` | REAL | Default model. |
| `autoCompactEnabled` | NOT FOUND in 2.1.177 | Likely renamed/removed — do not rely on it. |

**Precedence:** env var **>** settings.json. In CCP, `extra_env` is exported *after* the
dedicated-key exports, so an `extra_env` entry wins over a dedicated key on collision (don't
set the same thing both ways). This binary has **no** settings-`env`→process mechanism, so
per-profile env MUST come from CCP, not from a settings.json `env` block.

## 3. CCP profile mechanism (this machine)

- **Manifest:** `~/.config/claude-profiles/profiles.json`
- **Launcher:** `~/.local/bin/ccp`   **Lib:** `~/.local/share/claude-profiles/claude-profile-env.zsh`
- **Invoke:** `ccp <profile> [claude args...]` → exports the profile's env, then `exec claude`.

**Dedicated profile keys → env var (exported by `ccp`):**

| Profile key | Becomes | 
|---|---|
| `base_url` | `ANTHROPIC_BASE_URL` |
| `auth_env` + `keychain_service`/`keychain_account`/`keychain` | `<auth_env>` = secret read from macOS Keychain (never stored in the file) |
| `models.{main,opus,sonnet,haiku,subagent}` | `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` / `CLAUDE_CODE_SUBAGENT_MODEL` |
| `api_timeout_ms` | `API_TIMEOUT_MS` |
| `effort` | `CLAUDE_CODE_EFFORT_LEVEL` |
| `subscription: true` | OAuth path (`CLAUDE_CODE_OAUTH_TOKEN`) instead of API-key path |
| `claude_config_dir` | `CLAUDE_CONFIG_DIR` (separate home). **Omit** to share `~/.claude`. |
| `extra_env` (object) | every other env var, verbatim |

**Isolation guarantee:** before each launch, `ccp` unsets a static var list **plus every
`extra_env` key across all profiles**, so nothing leaks between profiles. That is why
per-provider env belongs here and not in the shared home.

## 4. Worked example — GLM (applied 2026-06-13)

Sources: Zhipu official Claude Code guide (`docs.bigmodel.cn/cn/coding-plan/tool/claude`)
for provider values; binary grep for var names.

```jsonc
"glm": {
  "display_title": "GLM",
  "base_url": "https://open.bigmodel.cn/api/anthropic",   // REQUIRED (prior "don't set" advice was wrong)
  "auth_env": "ANTHROPIC_AUTH_TOKEN",
  "keychain_service": "GLM_API_KEY",                       // secret lives in Keychain, not here
  "keychain_account": "<user>",
  "keychain": "<home>/Library/Keychains/login.keychain-db",
  "models": {                                              // glm-5.2 + [1m] = official 1M-context variant
    "main": "glm-5.2[1m]", "opus": "glm-5.2[1m]", "sonnet": "glm-5.2[1m]",
    "haiku": "glm-5.2[1m]", "subagent": "glm-5.2[1m]"
  },
  "api_timeout_ms": "3000000",
  "effort": "max",                                         // GLM maps xhigh/max/ultracode → its "max"
  "extra_env": {
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",          // pairs with [1m]
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "1000000",
    "ENABLE_TOOL_SEARCH": "0",                             // GLM workaround, Claude Code issue #30926
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1",         // GLM workaround, issue #30926
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

**Grounding decisions made here:**
- `effort: "max"` set (documented lever); `MAX_THINKING_TOKENS` **deliberately omitted** —
  the GLM doc specifies no value, so none was invented. Reasoning depth follows GLM's effort tier.
- `ENABLE_TOOL_SEARCH` fixed from `"false"` → `"0"` (doc value; avoids the truthy-string trap).
- `ANTHROPIC_BASE_URL` (`base_url`) kept — a "do not set base_url" claim was contradicted by
  the working profile and the `/anthropic` endpoint path.

## 5. Caveats observed

- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` (required by some providers) may suppress the
  *interleaved-thinking* beta header; per-turn thinking via effort still works.
- Free-tier provider accounts may not be entitled to large-context or max-effort tiers; if a
  profile errors, revert just that profile's tuning lines.
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` semantics for a third-party endpoint are not documented;
  setting it to the full window is low-risk, but it can be removed if behavior looks off.

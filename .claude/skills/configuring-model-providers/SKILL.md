---
name: configuring-model-providers
description: Use when configuring Claude Code to run on a non-Anthropic model provider (GLM/Zhipu, DeepSeek, Kimi/Moonshot, Qwen, MiniMax, OpenRouter, etc.) — setting ANTHROPIC_BASE_URL, model mappings, or provider env vars; tuning a CCP profile in profiles.json for performance (1M context, effort, timeout); or checking whether a Claude Code env var or settings key actually exists.
---

# Configuring Model Providers for Claude Code

## Overview

Point Claude Code at an alternate (non-Anthropic) model backend, tuned for maximum
performance and matching the provider's official guidance — **without inventing values or
polluting shared config.** Two phases: **(1) research the provider's official docs**,
then **(2) place only verified values in the correct, isolated config file.**

**Core principle — ground every value.** A value belongs in the config only if confirmed by
(a) the provider's official *Claude Code* integration doc, or (b) the *actually-installed*
Claude Code binary. Never trust a screenshot, a prior agent's list, or training-data
memory — they are routinely wrong about model names, exotic suffixes, and which env vars
exist. Where a doc is **silent** (e.g. no recommended thinking-token budget), set nothing;
use the documented lever instead (e.g. effort level).

## When to use

- Adding or tuning a provider profile (GLM, DeepSeek, Kimi, Qwen, MiniMax, OpenRouter, …).
- Setting `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, model mappings, context window, effort.
- Verifying whether a `CLAUDE_CODE_*` / `ANTHROPIC_*` env var or a settings.json key is real.

**Not for:** configuring Anthropic-hosted Claude (just use `/model`), or app-feature work.

## Phase 1 — Research the provider's official docs

Find the provider's **"Claude Code" / "coding plan" integration guide** (NOT its OpenAI-SDK
compatibility page — different endpoint, different auth). Label each value
`OFFICIAL-DOC` / `COMMUNITY-WORKAROUND` / `UNVERIFIED`:

- **Base URL** — the Anthropic-compatible endpoint (commonly ends in `/anthropic`).
- **Auth** — bearer-token providers use `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`.
- **Model IDs** — the *current* names + the most capable coding model. Confirm the model
  exists *now*; be skeptical of version numbers and special suffixes (e.g. a `[1m]`
  context-window suffix).
- **Mandated flags** — provider-specific workarounds; cite the GitHub issue number.
- **Effort / thinking / timeout** — record only what the doc actually states.

**If the provider has no dedicated Claude Code guide** (common): fall back to its
Anthropic-compatibility / API reference plus reputable community sources, and mark every
borrowed value `UNVERIFIED` until proven. **Surface consequential open choices to the user**
(region/endpoint, model tier, context size) rather than guessing — confirm, then verify
empirically (`ccp <profile>` → `/status`).

Tooling: WebSearch + WebFetch / context7 / tavily. Provider docs are often dynamically
rendered — try alternate URLs and search snippets if a page won't load, and say so.

## Phase 2 — Place verified values in the right file

**Verify env-var names against the installed binary, then isolate.** The verified-var
table, the binary-grep method, and the CCP `profiles.json` mechanism for this machine are in
**`provider-config-reference.md`** (read it before editing).

Decision rule: **per-provider config goes in the CCP profile (`profiles.json`: `extra_env`
+ dedicated keys). NEVER in the shared `~/.claude/settings.json`** — that file applies to
*every* profile. The `ccp` launcher exports a profile's vars, then scrubs them on the next
switch, so this isolates cleanly.

## Safe-apply checklist

1. `cp profiles.json profiles.json.bak` — it feeds every profile.
2. Edit by JSON key. Use `replace_all` only when the matched string is unique to the
   target profile(s) (e.g. a model id that only those profiles use).
3. `jq empty profiles.json` — a syntax error breaks ALL profiles.
4. `diff` backup vs new — confirm only intended lines changed and no other profile moved.
5. Runtime verify: `ccp <profile>` → `/status` (model + context window) and `/effort`;
   `printenv` the new vars; then launch a *different* profile and confirm they are **unset**
   (proves isolation).

## Common mistakes

| Mistake | Fix |
|--------|-----|
| Editing `~/.claude/settings.json` for one provider | Use the CCP profile's `extra_env`; settings.json is shared by all profiles. |
| Creating a separate Claude home per provider | The shared home is intentional; set `claude_config_dir` only when truly required. |
| Grepping the Anthropic SDK to "verify" Claude Code vars | Grep the installed Claude Code binary — the SDK is a different package and will mislead you. |
| Inventing a value the doc didn't give (e.g. `MAX_THINKING_TOKENS`) | Leave it unset; use the documented lever (effort level). |
| Boolean flag written as `"false"` | Use `"0"` / `"1"`; a non-empty `"false"` can be read as truthy. |
| Removing `ANTHROPIC_BASE_URL` | Anthropic-compatible third-party providers REQUIRE it. |

## Red flags — STOP

- About to edit `~/.claude/settings.json` to tune one provider → wrong file.
- About to copy an env-var list from a screenshot/memory without grep-verifying it.
- About to set a numeric budget the provider doc never specified.
- About to `git`-less overwrite `profiles.json` with no backup and no `jq empty`.

#!/usr/bin/env node
"use strict";

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const targets = [
  {
    name: "claude-default",
    kind: "claude-code",
    configDir: "<home>/.claude",
    pluginRoot: "<home>/.claude/plugins/marketplaces/thedotmack/plugin",
  },
  {
    name: "claude-alt",
    kind: "claude-code",
    configDir: "<home>/.claude-alt",
    pluginRoot: "<home>/.claude-alt/plugins/marketplaces/thedotmack/plugin",
  },
  {
    name: "claude-free",
    kind: "claude-code",
    configDir: "<home>/.claude-free",
    pluginRoot: "<home>/.claude-free/plugins/marketplaces/thedotmack/plugin",
  },
  {
    name: "claude-max",
    kind: "claude-code",
    configDir: "<home>/.claude-max",
    pluginRoot: "<home>/.claude-max/plugins/marketplaces/thedotmack/plugin",
  },
  {
    name: "codex-local",
    kind: "codex",
    configDir: "<home>/.codex",
    pluginRoot: "<home>/.codex/plugins/cache/claude-mem-local/claude-mem/13.6.0",
  },
];

const projectRoot = "<home>/Desktop/3_body_problem";
let failed = false;

for (const target of targets) {
  const runner = path.join(target.pluginRoot, "scripts", "bun-runner.js");
  const worker = path.join(target.pluginRoot, "scripts", "worker-service.cjs");
  if (!fs.existsSync(runner) || !fs.existsSync(worker)) {
    console.log(`FAIL ${target.name}: missing runner or worker`);
    failed = true;
    continue;
  }

  const marker = `SMOKE_PROFILE_HOOK_${target.name.replace(/[^A-Za-z0-9]/g, "_")}_${Date.now()}`;
  const payload = {
    session_id: marker,
    cwd: projectRoot,
    hook_event_name: "SessionStart",
    source: "startup",
    prompt: `claude-mem profile hook smoke ${marker}`,
    transcript_path: path.join("/tmp", `${marker}.jsonl`),
  };

  const result = spawnSync(process.execPath, [runner, worker, "hook", target.kind, "context"], {
    input: JSON.stringify(payload),
    encoding: "utf8",
    timeout: 60000,
    env: {
      ...process.env,
      CLAUDE_CONFIG_DIR: target.configDir,
      CLAUDE_MEM_DATA_DIR: "<home>/.claude-mem",
      CLAUDE_MEM_WORKER_HOST: "127.0.0.1",
      CLAUDE_MEM_WORKER_PORT: "37701",
      CLAUDE_MEM_PROVIDER: "claude",
      CLAUDE_MEM_MODEL: "poolside/laguna-m.1:free",
      CLAUDE_MEM_CLAUDE_AUTH_METHOD: "gateway",
      CLAUDE_CODE_PATH: "<home>/.local/bin/claude-mem-openrouter",
    },
  });

  const stdout = result.stdout.trim();
  let parsed = null;
  try {
    parsed = stdout ? JSON.parse(stdout.split("\n").at(-1)) : null;
  } catch {
    parsed = null;
  }
  const context = parsed?.hookSpecificOutput?.additionalContext || parsed?.systemMessage || "";
  const ok = result.status === 0 && context.includes("[3_body_problem] recent context");
  console.log(`${ok ? "OK" : "FAIL"} ${target.name} exit=${result.status} contextChars=${context.length} marker=${marker}`);
  if (!ok) {
    console.log(`  stdout=${stdout.slice(0, 400).replace(/\n/g, " ")}`);
    console.log(`  stderr=${result.stderr.trim().slice(0, 400).replace(/\n/g, " ")}`);
    failed = true;
  }
}

if (failed) process.exitCode = 1;

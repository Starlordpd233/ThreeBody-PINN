# Phase 37: Developer Environment & Precision Adjudication - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-07-11
**Phase:** 37-developer-environment-precision-adjudication
**Mode:** `--auto --all`
**Areas discussed:** Bootstrap entry and idempotence, Environment provenance, Dual-arm AD evidence, Precision and device seam

---

## Bootstrap Entry And Idempotence

| Option | Description | Selected |
|--------|-------------|----------|
| Root-level `./setup.sh` | Direct fresh-Mac entry with no Make or Python prerequisite. | yes |
| `make setup` | Make target wrapping setup helpers. | |
| Manual conda commands | Document commands without one executable entry. | |

**Auto choice:** Root-level `./setup.sh` (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Self-contained verification with explicit activation handoff | Use conda directly or `conda run`, avoid dotfile edits, and print activation. | yes |
| Spawn an activated subshell | Leave the user inside a child shell. | |
| Modify shell startup files | Persist activation by changing user configuration. | |

**Auto choice:** Self-contained verification with explicit activation handoff (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Detect and install only if missing | Preserve existing installations and keep the prefix configurable. | yes |
| Always reinstall | Replace the environment at a fixed path on every run. | |
| Require manual Miniforge setup | Stop before the one-command requirement is met. | |

**Auto choice:** Detect and install only if missing (recommended default).

---

## Environment Provenance

| Option | Description | Selected |
|--------|-------------|----------|
| Committed loose plus pinned pair | Normal setup validates; an explicit refresh rewrites the lock. | yes |
| Regenerate on every setup | Setup may dirty or silently change the reproducibility contract. | |
| Loose environment only | No exact replay artifact. | |

**Auto choice:** Committed loose plus pinned pair (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| JSON plus human rendering | Stable machine schema and readable owner output. | yes |
| Plain text only | Readable but harder to compare automatically. | |
| Console only | No durable fingerprint. | |

**Auto choice:** JSON plus human rendering (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Timestamped raw evidence plus Markdown | Retains every run and gives the owner a stable reading surface. | yes |
| Overwrite one latest file | Loses provenance across reruns. | |
| Console only | Leaves no adjudication artifact. | |

**Auto choice:** Timestamped raw evidence plus Markdown (recommended default).

---

## Dual-Arm AD Evidence

| Option | Description | Selected |
|--------|-------------|----------|
| One orchestrator, isolated same-path arms | Runs fp32-MPS and fp64-CPU through one implementation in separate processes. | yes |
| Two unrelated scripts | Risks comparing implementation differences. | |
| One mutable process | Relies on global dtype/device state across arms. | |

**Auto choice:** One orchestrator, isolated same-path arms (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve locked fixture and add deterministic repetitions | Keeps the section 10.3 criterion while enabling timing. | yes |
| Replace with random trajectories | Changes the acceptance workload. | |
| Timing only | Drops analytical correctness. | |

**Auto choice:** Preserve locked fixture and add deterministic repetitions (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Structured correctness, timing, and environment evidence | Records all comparison inputs and outputs without a verdict. | yes |
| Single pass/fail line | Omits the evidence needed for D1-p. | |
| Benchmark winner | Lets the agent choose the owner-carved decision. | |

**Auto choice:** Structured evidence with no verdict (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Owner checkpoint | Stop before setting a default or beginning dependent work. | yes |
| Choose faster passing arm | Agent decides D1-p. | |
| Default fp32-MPS | Treat an unratified branch as settled. | |

**Auto choice:** Owner checkpoint (required by ratification, not discretionary).

---

## Precision And Device Seam

| Option | Description | Selected |
|--------|-------------|----------|
| Central explicit resolver | Resolve config once and pass dtype/device through the shared path. | yes |
| Global dtype and implicit device | Hides state and makes branch parity hard to verify. | |
| Separate arm implementations | Duplicates the code path ENV-04 requires to remain shared. | |

**Auto choice:** Central explicit resolver (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| Fail-fast validation | Reject unsupported combinations without fallback. | yes |
| Silent CPU fallback | Can invalidate MPS evidence. | |
| Late framework error | Produces inconsistent failure points. | |

**Auto choice:** Fail-fast validation (recommended default).

| Option | Description | Selected |
|--------|-------------|----------|
| No implicit default before D1-p | Probe arms are explicit; owner choice later changes one config default. | yes |
| Default fp32-MPS | Pre-decides D1-p. | |
| Default fp64-CPU | Pre-decides D1-p. | |

**Auto choice:** No implicit default before D1-p (recommended fail-closed behavior).

---

## Agent Discretion

- Exact module names, CLI flag spelling, JSON field names, and evidence directory layout.
- Exact deterministic warmup and repetition counts, with raw counts recorded and no invented performance threshold.
- Exact pinned-lock mechanism within the required loose-plus-pinned contract.

## Deferred Ideas

- The D-06 static-epsilon sensitivity todo remains outside v2.0.
- The remaining trainex-r1b tuning handoff remains Future work.
- Phase 38 model rebuild and later data/training/pilot work were not pulled into Phase 37.

## Automatic Todo Review

The todo matcher scored both legacy todos at 0.6. The authoritative `STATE.md`
entry explicitly marks both unlinked to v2.0 phases, so the phase scope
guardrail overrides the keyword-only match. Both are reviewed and deferred,
not folded.

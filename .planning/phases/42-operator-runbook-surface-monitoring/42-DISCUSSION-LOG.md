# Phase 42: Operator Runbook Surface & Monitoring - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-18
**Phase:** 42-operator-runbook-surface-monitoring
**Areas discussed:** Step-log emission & E1 policy, TensorBoard & residual panel, Signals & wrapper, Heartbeat & mem line, runs/ contract & summary, Runbook & config surface

**Mode:** `--all` (all gray areas auto-selected) with owner-delegated
auto-resolution — operator instruction: *"auto advance on choosing the default
and best option … follow your best judgment … root yourself in the mathematics
and physics."* Every question below was resolved by Claude on the recommended
option, single pass, each choice logged. Run under watchdog chain
`phase-42-work` position 2 (contract: produce + commit 42-CONTEXT.md +
42-DISCUSSION-LOG.md).

`[--all] Auto-selected all gray areas: step-log emission & E1, TB residual
panel, signals & wrapper, heartbeat & mem, runs/ contract & summary, runbook &
config surface.`

---

## Step-Log Emission & E1 Non-Finite Policy (OPS-03)

| Option | Description | Selected |
|--------|-------------|----------|
| Widen `_log_step` + attach handlers at composition root | The CTX-45 designed seam: one emission point, sinks are formatter/handler concerns | ✓ |
| New `metrics_hook` closure threaded like `guard_hook` | Second parallel seam; duplicates an emission path that already exists | |
| train.py polls controller state | Decouples cadence from the step loop; racy, samples rather than records | |

`[auto] Emission path → "Widen _log_step + composition-root handlers" (recommended; 40-CONTEXT CTX-45 pre-designed exactly this).`

| Option | Description | Selected |
|--------|-------------|----------|
| null + `finite:false` + `nonfinite_keys` | `allow_nan=False`; every line parses under any strict JSON parser; divergence recorded at record level | ✓ |
| Raw NaN tokens (`allow_nan=True`) | Emits literal `NaN` — not valid JSON; breaks strict parsers | |
| String sentinel ("NaN") | Rejected by SPEC E1 (breaks typed parsers); guards' trip.json sentinel stays local | |

`[auto] E1 non-finite mechanism → "null + finite flag + nonfinite_keys" (recommended; only option satisfying strict parseability + recorded divergence).`

**Notes:** `run.log_every` kept as the `log_freq` cadence knob (no rename —
Phase-41 schema churn for zero gain); example config sets 100 per design §5.4.
B-2 field list ships as ⚖ provisional `STEP_LOG_FIELDS` registry; owner
ratifies before run #1 (seam, not invented).

---

## TensorBoard Secondary View & Per-Time-Bin Residual Panel (OPS-03/04b)

| Option | Description | Selected |
|--------|-------------|----------|
| SummaryWriter fed from the same step record | Internal background event-writer thread = the async mechanism; add_scalar is an enqueue; no matplotlib | ✓ |
| Separate tailer process reading train.log.jsonl | Purest "derived view" but adds a process/lifecycle to manage; overkill for v2.0 | |
| Synchronous plotting in the loop | Violates the SPEC's async/no-blocking constraint | |

`[auto] TB mechanism → "SummaryWriter from the same record" (recommended; tensorboard 2.21.0 verified in pinn-train; JSONL stays canonical per D2).`

| Option | Description | Selected |
|--------|-------------|----------|
| Per-bin scalars + w_n stats + front index | 16 collocation bins as `residuals/bin_nn`; `causal/w_min·w_mean·w_max·front_idx`; readable collapse + propagation-front signal | ✓ |
| TB histograms only | Histograms bin by value, not by time-bin — cannot show which τ-bins are unresolved | |
| Rendered heatmap images | Needs figure rendering (matplotlib-adjacent) in or near the loop | |

`[auto] Panel form → "per-bin scalars + w_n stats + front_idx" (recommended; grounded in w_n = exp(-η_c Σ stopgrad(R̄_m)) collapse phenomenology; emits unconditionally incl. NaN/collapse).`

**Notes:** per-bin `R̄_n`/`w_n` exposed via an additive detached details path on
`causal_physics_loss` — default return type unchanged, no Phase-38/40 test
churn, no autograd-graph retention.

---

## Signal Handling & Unattended Wrapper (OPS-01/02, E2)

| Option | Description | Selected |
|--------|-------------|----------|
| Flag-based graceful stop at step boundaries + timed debounce escalation | 1st SIGINT/SIGTERM → checkpoint + `interrupted` + exit 130/143; 2nd SIGINT after ~1 s window → best-effort status flip + `os._exit` | ✓ |
| Raise KeyboardInterrupt from handler | Interrupts mid-tensor-op; unwinds through torch internals; checkpoint state incoherent | |
| Ignore repeats entirely (no escalation) | Violates the SPEC's SIGINT-twice → immediate-exit requirement | |

`[auto] Signal design → "flag + step-boundary graceful, debounced escalation" (recommended; E2 atomicity already carried by tmp+fsync+rename; handlers composition-root-only).`

| Option | Description | Selected |
|--------|-------------|----------|
| `exec caffeinate -is python -m pinn.train "$@"` | caffeinate exits with the utility's status; `exec` removes the shell layer → verbatim exit propagation | ✓ |
| Wrapper with post-hoc `$?` plumbing | More moving parts to get the same guarantee; easier to get wrong | |

`[auto] Wrapper form → "exec caffeinate -is …" (recommended; satisfies the must-NOT exit-propagation test by construction; no machine paths in the script).`

---

## status.json Heartbeat & mem: Line (OPS-04a, E3)

| Option | Description | Selected |
|--------|-------------|----------|
| Daemon heartbeat thread + synchronous transition writes | K-seconds guarantee holds during multi-minute L-BFGS line searches; freshness ≡ process liveness (the SPEC's robustness reading) | ✓ |
| In-loop writes only | Fails the "at least every K seconds" guarantee whenever the thread is trapped in optimizer.step(closure) | |
| Closure-hook emission | Ties heartbeat cadence to line-search evaluation rate; irregular and stops in non-closure phases | |

`[auto] Heartbeat mechanism → "daemon thread + atomic_write_text" (recommended; every rewrite atomic; initializing written pre-build with no fabricated losses).`

**Notes:** schema is self-describing (`heartbeat_interval_secs` +
`staleness_threshold_secs` in the file; default threshold 3×K) and carries
`pid` as the unattended kill target. `mem:` reuses the guard memory signal
(`torch.mps.driver_allocated_memory`) — no psutil.

---

## runs/ Contract Completion & Summary One-Pager (OPS-05, E4)

| Option | Description | Selected |
|--------|-------------|----------|
| Honest stub at launch, atomic terminal rewrite | `summary.md` present under every death mode incl. SIGKILL; stub is an honest "did not complete" | ✓ |
| Write only at exit | Fails E4 presence under kill -9 / power loss | |
| Post-hoc generator script | Presence depends on someone running it; not a contract | |

`[auto] Summary lifecycle → "stub-then-finalize" (recommended; the only design that satisfies E4's always-present invariant).`

**Notes:** curriculum progression rendered from the existing
`curriculum.jsonl`; B-6/D-12 env-fingerprint fields embedded in the
`summary.json` run header (reconciles ratified B-6 with the SPEC's member list
without inventing a file); `logs/`, `tb/`, empty `failure/` created at launch
(SPEC lists `failure/` in the successful-run contract); artifacts record
run-dir-relative paths only (Phase-39 `/Users/` leak precedent).

---

## Runbook & Config Surface (OPS-01/06)

| Option | Description | Selected |
|--------|-------------|----------|
| `docs/runbooks/training/` + `configs/stage0-example.yaml` | New runbook category per docs/README.md taxonomy; date-prefixed name; example config loadable by `load_config` | ✓ |
| Runbook under docs/work/ | Wrong lifecycle — runbooks are durable operational procedures, not phase work artifacts | |
| README-embedded operator docs | Fails the SPEC's "written runbook under docs/runbooks/" requirement | |

`[auto] Runbook placement → "docs/runbooks/training/ + configs/" (recommended; planner reads docs/README.md in full before creating files).`

**Notes:** five entry points map to existing commands (Setup = Phase-37 setup;
Configure = copy+edit example YAML; Launch = `python -m pinn.train` / wrapper;
Monitor = `train.log` + TensorBoard + `status.json`; Resume = `--resume
latest`) — no new CLI beyond the wrapper. New knobs live under `run.monitor`,
all operational under the locked B-5 classification.

---

## Claude's Discretion

Module filenames under `pinn/training/`; exact debounce window (~1 s); s/step
EMA constant; heartbeat default within 15–60 s; TB histogram/`mem:` cadences;
wrapper filename; human log-line micro-format; TB tag taxonomy beyond the
mandated tags; ETA = current-stage scope (null until EMA warms).

## Deferred Ideas

None new (Phase-43 items already out of scope by roadmap). Reviewed-not-folded
todos: `d-06-static-epsilon-sensitivity-check` (spurious keyword match — a
data/physics probe, no monitoring surface; the auto-fold ≥0.4 rule was
overridden with rationale), `trainex-r1-research-handoff` (score 0.2, below
threshold).

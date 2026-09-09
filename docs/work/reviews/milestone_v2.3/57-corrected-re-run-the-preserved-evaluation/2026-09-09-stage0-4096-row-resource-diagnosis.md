---
status: active
purpose: review-findings
created: 2026-09-09
milestone: v2.3
phase: 57-corrected-re-run-the-preserved-evaluation
retirement_trigger: After the owner rules on the resource/guard/environment decision and a band generation 2 run window is admitted or Phase 57 is closed
---

# Stage-0 4096-row resource diagnosis — band generation 1 block

**Audience:** the project owner
**This document is:** a read-only diagnosis of why the generation-1 smoke halted, built entirely from artifacts already on disk
**This document is not:** a recipe change, a guard change, a tuning proposal, or an authorization to re-run

No config, source file, threshold, or recipe value was modified in producing this document. One
transcription defect in `run-ledger.md` was corrected (section 6); nothing else in the evidence
tree was touched. The held-out evaluation remains unspent.

---

## 1. What happened, in one paragraph

The corrected Stage-0 smoke was launched, loaded its data, passed every preflight check, built its
first training batch, computed all five loss terms, and then stopped — before it had finished a
single optimizer step. It stopped because a safety guard noticed the process was holding almost all
of the machine's memory. The guard did its job. Nothing was corrupted, nothing was lost, and the one
held-out evaluation the whole phase is protecting was never touched.

Two facts that were not previously visible are now established: the memory the process was holding
was **not** the model or the data (those are tiny), and one training step at this recipe took
**11 minutes**.

---

## 2. The block itself

| Fact | Value |
|---|---|
| Run | `stage0-v23-smoke`, seed 42, band generation 1 |
| Guard | `memory_watermark`, Tier 2, disposition `HALT` |
| Measured | `memory_fraction` = 0.9688 |
| Threshold | 0.7, flagged `threshold_provisional: true` |
| Stopped at | stage 0, step 0, phase `2a` — before any optimizer update |
| Evaluation | `preserved-unspent`; no graded seed was launched |
| Terminal? | **No.** This is an operational block, not the authorized invariant-B closure |

Source: `runs/stage0-v23-smoke/failure/trip.json`,
`.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state.json`.

---

## 3. The central finding: reserved memory, not live memory

The run logged both memory numbers on the same line, and they disagree by more than three orders of
magnitude:

```
mem: driver_bytes=24964661248  current_bytes=9193984
```

| Quantity | Bytes | Human |
|---|---:|---|
| `driver_bytes` — memory the Metal driver has handed to this process | 24,964,661,248 | **23.25 GiB** |
| `current_bytes` — memory actually occupied by live tensors | 9,193,984 | **8.8 MiB** |
| Machine total (`hw.memsize`, Apple M5 Pro) | 25,769,803,776 | 24.00 GiB |

**The model, its gradients, and its optimizer state occupy 8.8 MiB.** The 23.25 GiB is the
allocator's reserved pool — memory it requested from the driver to satisfy short-lived intermediate
tensors during the step, and then kept rather than returning.

So nothing is leaking, and nothing large is being retained between steps. The pressure is entirely a
**transient peak inside one step**.

Two consequences that matter for the decision:

1. The guard reads `driver_bytes` (`pinn/training/guards.py:241`, `torch.mps.driver_allocated_memory`).
   That is the reserved pool, which only ever grows during a run. It is a legitimate thing to watch —
   the machine really is under pressure — but it is a *high-water* signal, not a live-footprint signal.
2. The denominator is `_DEFAULT_MEMORY_TOTAL_BYTES = 24 * (1024 ** 3)` (`guards.py:41`), a hard-coded
   constant. On this machine it happens to be exactly correct (`hw.memsize` = 25,769,803,776). On any
   other machine the reported fraction would be wrong. This matters only if the environment changes.

---

## 4. Where the transient peak comes from

The peak is the product of three things that multiply together, all of them in the step's phase `2a`.

**(a) The physics term needs second-derivative autograd.** The residual compares predicted
acceleration against Newtonian force, so the graph is built with `create_graph=True`
(`pinn/physics_residual.py:174,176`). A second-order graph is substantially larger than an ordinary one.

**(b) It is built over 4096 collocation rows.** Confirmed in the step record:
`n_collocation_rows: 4096`, `n_bins: 16`. This is the ratified amended-recipe value.

**(c) That graph is then traversed six times before a single parameter update.** This is the part
that was not obvious. `_build_gradient_stats` (`pinn/training/controllers.py:482-496`) calls
`_global_parameter_grad_norm(..., retain_graph=True)` once per loss term to produce the per-term
diagnostic norms, and only afterwards does `loss_terms.total.backward()` run
(`controllers.py:1706`):

| Pass | Purpose | Recorded output |
|---|---|---|
| 1 | `data` raw grad norm | `grad_norm_raw_data = 6.59` |
| 2 | `ic` raw grad norm | `grad_norm_raw_ic = 6.27e8` |
| 3 | `phys` raw grad norm | `grad_norm_raw_phys = 440.33` |
| 4 | `energy` raw grad norm | `grad_norm_raw_energy = 8.03e6` |
| 5 | `angmom` raw grad norm | `grad_norm_raw_angmom = 1.02e5` |
| 6 | the actual `total.backward()` | `grad_norm = 6.27e8` |

Because every diagnostic pass sets `retain_graph=True`, the full second-order graph stays alive
across all six. Nothing can be released until the last one finishes, so the allocator's pool grows to
the union of all six peaks rather than the largest single one.

A detail worth noting: at step 0 the physics weight is `lambda_phys = 0.0` (warm-up is
`I_warm = 30` steps). The physics term therefore contributes **nothing** to the loss that is
optimized at this step — but its full 4096-row second-order graph is built and traversed twice
anyway, once for the `grad_norm_raw_phys` telemetry and once inside `total.backward()`.

**This is a description of the observed mechanism, not a proposal to change it.** The per-term
gradient telemetry is a declared contract (`STEP_LOG_FIELDS`, INST-02, and the conformance census at
`pinn/conformance/census.py:75-79`), and the run log flags that registry as owner-ratifiable. It is
not the agent's to alter.

---

## 5. The second finding: throughput

File modification times give an exact split of the 852-second run:

| Segment | Window (local) | Duration |
|---|---|---|
| Launch → preflight complete (`splits.json`, `stage-0-init.pt`, `preflight.json` written) | 23:00:56 → 23:03:57 | **181 s** |
| First optimizer step (→ `failure/trip.json`) | 23:03:57 → 23:15:08 | **671 s** |

**One Adam step at the 4096-row recipe took 671 seconds.** Projecting the ratified budgets at that
observed rate:

| Workload | Steps | Projected |
|---|---:|---:|
| Smoke (`n_adam = 300`) | 300 | 55.9 h (2.3 days) |
| One graded seed (`n_adam = 1000`) | 1,000 | 186 h (7.8 days) |
| Full graded band, 3 seeds | 3,000 | **559 h (23.3 days)** |

**Caveat, stated plainly:** 671 s/step was measured while the process held 97% of physical memory,
so the machine was almost certainly paging. If the memory peak were reduced, step time would very
likely fall — by an unknown factor. These projections are therefore an *upper* bound at the observed
operating point, not a prediction of what a memory-repaired run would cost. But even an optimistic
10× improvement leaves the graded band at roughly 2.3 days, which is a planning fact the phase has
not yet accounted for.

This is why raising the guard threshold alone would not have produced a usable band: the run would
have proceeded into paging at ~11 minutes per step.

---

## 6. Evidence integrity — verified, with one defect corrected

All 18 artifacts in `runs/stage0-v23-smoke/` were re-hashed and compared against the ledger and the
blocked state.

- **17 of 18 matched exactly on first check.**
- **1 defect:** `run-ledger.md` recorded `artifact_hashes["config.yaml"]` as a **62-character**
  string — two characters dropped mid-hash. The correct 64-character value was independently present
  and correct in `blocked-state.json` (`config.resolved_sha256`) and matches the file on disk.
  The ledger value has been corrected to the dual-attested hash. **After correction: 18/18 match.**

This was caught before the ledger was committed. Had it been committed as-is, generation 1's record
would have carried a permanently unverifiable hash.

### Preservation risk — the reason this section matters

`runs/` is covered by a blanket `.gitignore` rule (`.gitignore:339`). The generation-1 evidence is
therefore:

- **18 files, 23 MB, zero of them tracked by git**
- referenced by hash from a ledger that *is* about to be tracked
- the only copy in existence

The `.planning/` records (`blocked-state.json`, `run-ledger.md`) are being committed and are safe.
The run directory itself is not, and cannot be made safe without a decision (section 7, D-3).

---

## 7. What now blocks a fresh run window

The Wave-5 admission check was run read-only. It fails closed on exactly one condition:

```
verify_phase57_evidence FAIL-CLOSED: target run directory already exists:
  .../runs/stage0-v23-smoke
```

Everything else it checks is currently satisfiable. So re-admission is gated on the run-name
namespace — and that collides directly with the preservation risk above, because the simplest way to
clear the blocker (delete the directory) is also the way to destroy the only copy of the evidence.

### A gap the block exposed

Wave 5's Task 3 required the run to "require the timing fingerprint, **exact-4096 resource
preflight**, and all other preflight checks before optimization."

**No such resource preflight exists.** `pinn/conformance/preflight.py` contains zero references to
memory, resource, or watermark, and the Phase-57 verifier mentions "resource" only when *classifying
a failure after the fact*. The 4096-row recipe's memory cost was therefore discovered by spending
852 seconds on it rather than by predicting it in advance. Whatever is decided below, a cheap
predictive check would convert a 14-minute failure into a sub-minute one.

---

## 8. Decisions the owner owns

None of these are the agent's to make. They are listed with what is known, not with a chosen answer.

**D-1 — The memory watermark (0.7).** The threshold is an explicitly uncalibrated placeholder; the
code comment states `disk_floor_fraction / memory_watermark_fraction remain owner-carved and
uncalibrated`, and the log flags it as owner-calibrate-at-the-Stage-0-pilot. Phase 57 *is* that
pilot. Note that the observed 0.969 is against *physical RAM*, so raising the threshold does not buy
headroom that exists — it buys paging. Section 5 is the argument that this alone does not yield a
usable band.

**D-2 — The transient-peak cause.** The six retained traversals in section 4 are instrumentation
plus one real backward. Reducing that cost touches a declared telemetry contract (`STEP_LOG_FIELDS`
/ INST-02 / conformance census), which is owner-ratifiable and not agent-editable. Distinct from
D-1: this addresses the *cause*, where D-1 only moves the alarm.

**D-3 — Preserving generation-1 evidence.** 23 MB of untracked, gitignored, single-copy evidence
that must survive whatever clears the re-admission blocker. Choosing where it goes and whether any
of it enters git is a process-artifact decision, which governance reserves to the owner.

**D-4 — Run-name namespace for generation 2.** Either the generation-1 directory moves, or
generation 2 uses new run names. Run name is a fingerprinted config field, so changing it is a config
change; moving the directory depends on D-3.

**D-5 — Execution environment.** Section 5's throughput projection applies to this Apple M5 Pro at
24 GiB. A different environment changes both the memory arithmetic (and would expose the hard-coded
24 GiB denominator in `guards.py:41`) and the schedule.

---

## 9. One scientific observation, recorded without interpretation

The Phase 56/57 correction introduced a frozen reference `r_ref = 1.975e10` that normalizes the
causal residual. At step 0 the monitor recorded:

```
w_max = 1.0    w_mean = 0.0698    w_min = 1.445e-10    front_idx = 0    n_bins = 16
```

For contrast, the v2.2 halt brief records that across all 502 logged steps of the previous
generation, the bin weights sat pinned at the smallest representable positive float, and the
first-bin residual sat ~10.6 decades above the bar it had to clear.

Here the weights span a real range and the leading bin carries full weight. `front_idx = 0` is simply
where the front starts, and one step is one step.

This is a **training-only monitor** reading from a blocked run, not held-out data and not a result.
It is recorded because it is the only scientific signal generation 1 produced, and because it would
otherwise be lost. It should not be read as evidence that the corrected recipe trains — that is
precisely the question the band exists to answer, and it remains open.

---

## 10. Provenance

Every number above is derived from committed or on-disk artifacts:

| Claim | Source |
|---|---|
| Guard trip, threshold, provisional flag | `runs/stage0-v23-smoke/failure/trip.json` |
| driver vs current bytes | `runs/stage0-v23-smoke/logs/train.log`; `status.json` `memory` |
| Machine total | `sysctl hw.memsize`; `pinn/training/guards.py:41` |
| Memory signal API | `pinn/training/guards.py:228-241` |
| Threshold provenance | `pinn/training/config.py:291-297`; run-start provisional-thresholds log line |
| Six traversals | `pinn/training/controllers.py:417-496`, `1673-1740` |
| Second-order graph | `pinn/physics_residual.py:174,176` |
| Per-term grad norms, weights, losses | `runs/stage0-v23-smoke/logs/train.log.jsonl` (single step-0 record) |
| Timing split | file mtimes in `runs/stage0-v23-smoke/` |
| Hash verification | recomputed sha256 over all 18 files vs ledger + blocked state |
| Re-admission blocker | `verify_phase57_evidence.py admit-run-window`, read-only |
| Missing resource preflight | `pinn/conformance/preflight.py`; `verify_phase57_evidence.py:247` |
| `runs/` untracked | `.gitignore:339`; `git ls-files runs/stage0-v23-smoke` → 0 |

---

# Amendment — 2026-09-09: the probe result

Nothing in this amendment changes a config, a threshold, or a recipe value. The owner
selected the probe-first path on GAP-57-02; this records what the measurement returned.
**Section 4's hypothesis is refuted by it**, and that is the amendment's main point.

## 11. What was measured

Condition A was already in the record from band generation 1. Condition B held every
scientific input identical and varied exactly one thing: the five `retain_graph=True`
per-term diagnostic traversals in `_build_gradient_stats` were bypassed by routing the
production function through its own existing `raw_overrides` parameter, so no production
code was edited or reimplemented. The probe config differed from
`configs/stage0-v23-smoke.yaml` in exactly two fields — `run_name` (to `probe-mem-b`) and
`log_every` (50 → 1, to get a memory reading every step). Same seed 42, same 4096 rows,
same 240 replay, same 16 bins, same frozen `r_ref`, same guard at 0.7.

| | Condition A (gen 1) | Condition B (probe) | Δ |
|---|---:|---:|---:|
| `driver_bytes` | 24,964,661,248 (23.25 GiB) | 22,812,983,296 (21.25 GiB) | **−2.00 GiB, −8.6%** |
| `memory_fraction` | 0.9688 | **0.8853** | still **> 0.7** |
| `current_bytes` (live) | 9,193,984 | 9,193,984 | identical |
| Preflight | 181 s | 177 s | consistent |
| **Step 0 wall clock** | **671 s** | **153 s** | **−77%, 4.4× faster** |
| `grad_norm` | 627404864.0 | 627404864.0 | **bit-identical** |

Two controls confirm the experiment was clean. The step record carries
`grad_stats_provenance = "pre_total_backward|PROBE-B-no-per-term-traversal"`, proving the
patch took effect. And `grad_norm` is bit-identical across the two runs, proving the
diagnostic traversals are observation-only — removing them moved the memory and the clock
without perturbing the optimization by a single bit.

## 12. What it means

**The instrumentation is not the memory bottleneck.** Section 4 reasoned that six retained
traversals of a second-order graph would make the peak roughly the union of six working
sets. That was wrong. Removing five of the six recovered 2.00 GiB — 8.6% — and the run
still tripped, at 0.885. The peak is set by the **single `total.backward()` over the
4096-row second-order graph**, which by itself needs ~21.25 GiB on this machine.

This is precisely the outcome that justified measuring first. Had the telemetry-contract
change been ratified straight from section 4's reasoning, the project would have spent an
owner ratification on a contract change that does not clear the guard.

**But the instrumentation is very much the time bottleneck.** The same five traversals cost
**4.4× in wall clock** — 671 s → 153 s per step. Section 5's projections revise accordingly:

| Workload | Steps | At 671 s/step (A) | At 153 s/step (B) |
|---|---:|---:|---:|
| Smoke | 300 | 55.9 h | **12.8 h** |
| One graded seed | 1,000 | 186.4 h | **42.5 h** |
| Full graded band | 3,000 | 559.2 h (23.3 d) | **127.5 h (5.3 d)** |

Both B figures are still measured under memory pressure (0.885), so they remain upper
bounds rather than predictions for a memory-repaired run.

So the memory question and the throughput question have **different answers and different
remedies**, which section 5 could not distinguish.

## 13. Where the memory remedy actually lives

The ratified spec already contemplates the mechanism. `pinn_architecture.md:456` — the
Phase-56 amended-recipe contract — states verbatim, twice:

> "Microbatching preserves complete bin aggregates and never resets the prefix."

and repeats it in the re-issued acceptance criterion. The GAP-57-01 resolution likewise
names "microbatch-preserved aggregates" among the things the authorized bounded patch must
implement, and `57-02-SUMMARY.md` records that the built aggregation uses differentiable
`index_add` specifically "so microbatch accumulation preserves counts, loss, and
gradients" (`controllers.py:233-234`).

So the implementation is microbatch-**safe**. The measurement says it is not microbatch-
**executed**: 4096 rows enter one graph, and one backward over that graph is the 21.25 GiB.

The engineering subtlety, stated plainly because it decides whether this is cheap or hard:
the causal weight for a row depends on a batch-global exclusive prefix over all sixteen bin
means, so every row's loss depends on every other row's residual. Splitting the forward pass
alone saves nothing, because a single backward at the end still retains the whole graph.
Bounding memory requires two passes — one to compute the bin means and hence the weights,
then a second that walks microbatches with those weights held fixed and accumulates
gradients per microbatch. That is only exact if the causal weights are detached, which
`57-02-PLAN.md` indicates the contract requires ("keep causal weights detached where the
contract requires without detaching model residuals"). The codebase already has this exact
gradient-accumulation pattern implemented for the data term
(`accumulate_chunked_data_term`, `controllers.py:567`).

**Whether "microbatch-preserved aggregates" (a correctness property the code already
satisfies) also authorizes memory-bounded microbatch execution (a change to how the step
runs) is an inference, and it is not the agent's to make.** It is put to the owner as the
narrowed GAP-57-02 decision rather than assumed. Section 8's D-2 is superseded by this
section; D-1 is superseded by section 12's finding that recalibration alone still faces a
5.3-day band; D-5 (environment) is unchanged and now the clearest alternative if
microbatch execution is judged out of scope.

## 14. Probe provenance

- Driver: `probe_mem_b.py` (scratchpad, not committed) — inserts the worktree on
  `sys.path`, wraps `controllers._build_gradient_stats` to force
  `raw_overrides={term: 0.0}` for all five terms, then calls `pinn.train.main`.
- Config: `configs/stage0-v23-smoke.yaml` with `run_name: probe-mem-b` and
  `log_every: 1`. Removed after the run so the admitted config set is untouched.
- Output: `runs/probe-mem-b/` (gitignored, retained on disk; not Phase-57 evidence).
- Wrote no Phase-57 evidence file, touched no admitted config, spent no evaluation, and
  did not collide with any `stage0-v23-*` run name.

---
status: active
purpose: implementation-plan
created: 2026-09-09
milestone: v2.3
phase: 57-corrected-re-run-the-preserved-evaluation
retirement_trigger: After band generation 2 completes, closes terminally, or the scope is superseded by a later owner ruling
---

# Band generation 2 — scope brief

**This document is:** the agreed scope for the work that must land before a generation 2 run
window is admitted, so the next wave can be planned and executed against a fixed target.
**This document is not:** a plan file, an authorization to run training, or a change to any
recipe value. GSD plan files remain the planner's output.

Grounding: `2026-09-09-stage0-4096-row-resource-diagnosis.md` (sections 11–14) and
`57-GAPS.md` GAP-57-02 / GAP-57-03.

---

## 0. Decision provenance

Both decisions below were **owner-delegated on 2026-09-09** ("decide on the previous
questions yourself; you have control and decision making over this"). This project already
recognises express delegation as a grounding source — the R-1 `loss_explosion_ceiling` was
ratified this way on 2026-07-21, and Phase 54's checkpoint ② was discharged under express
delegation on 2026-09-04.

Delegation is read narrowly, as covering **engineering scope and conformance judgement**.
It is **not** read as covering:

- spending the sole preserved held-out evaluation (EVAL-02) — that remains the Wave-6
  blocking checkpoint it already is;
- the Phase-58 go / adjust / rethink verdict (owner checkpoint ⑤);
- any change to a ratified scientific value — 4096 rows, 16×256 bins, the batch-global
  prefix, `R_ref`, the N=500 window, and the 1000/1000 budget are all untouched below.

---

## 1. Decision A — memory-bounded microbatch execution is in-scope conformance

**Ruled: yes.**

Reasoning, so it is auditable:

1. `pinn_architecture.md:456` — the ratified Phase-56 amended-recipe contract — states
   verbatim, and repeats inside its re-issued acceptance criterion, that *"Microbatching
   preserves complete bin aggregates and never resets the prefix."* The spec does not merely
   tolerate microbatching; it writes the correctness constraint microbatching must satisfy.
   A constraint on how a thing is done presupposes that it may be done.
2. GAP-57-01's resolution names **"microbatch-preserved aggregates"** inside the inventory
   the authorized bounded patch must implement. That authorization is scoped by behaviour,
   not by a file list.
3. `57-02-SUMMARY.md` records that the delivered aggregation uses differentiable `index_add`
   *specifically* "so microbatch accumulation preserves counts, loss, and gradients"
   (`controllers.py:233-234`). The capability was built deliberately; only the execution
   strategy is missing.
4. It changes **no recipe value**, so SCOPE-37 conformance-only iteration is satisfied. The
   loss computed is the same loss.

The residual risk — that "preserved aggregates" was meant only as a correctness property and
not as licence to restructure the step — is recorded and accepted. It is mitigated by the
mandatory equivalence test in §1.2, which makes the claim falsifiable rather than asserted.

### 1.1 Required shape

Two passes, exact because the causal weights are detached:

```
Pass 1 — weights (no parameter graph retained)
  compute residuals over all 4096 rows in microbatches
  index_add into the 16 bin sums / counts -> 16 bin means
  one batch-global exclusive 16-term prefix -> w_n, detached
  free each microbatch's graph before the next

Pass 2 — gradients (parameter graph, per microbatch)
  for each microbatch:
      recompute residual with create_graph
      loss_chunk = w_n[bin] * (chunk contribution) / R_ref
      loss_chunk.backward()      # accumulates into .grad
      graph freed before the next chunk
```

The residual is evaluated twice, trading ~2× physics forward cost for a peak bounded by the
microbatch rather than by 4096. That trade is the point: the measurement in §11 of the
diagnosis shows the monolithic backward alone needs ~21.25 GiB.

Mirror the existing pattern in `accumulate_chunked_data_term` (`controllers.py:567`),
including its weighting discipline — that function's docstring already warns that an
unweighted chunk sum scales the gradient by the chunk count.

### 1.2 Non-negotiable constraints

- **Bin aggregates complete; prefix never reset.** One batch-global exclusive prefix over
  the 16 bin means, formed once, never per microbatch.
- **Equivalence test is mandatory and blocking.** Loss and parameter gradients from the
  microbatched path must match the monolithic path to float tolerance, across at least two
  different microbatch sizes and one size that does not divide 4096 evenly. This is the test
  that converts §1's inference into a checked claim; `57-02-PLAN.md` already reserves
  T-57-04 for it and `57-VALIDATION.md:102` already lists microbatch equivalence.
- **Default microbatch = 256 rows (one bin).** Chosen to align with the ratified bin
  structure rather than to hit a memory number, so the aggregation boundary and the chunk
  boundary coincide and every chunk carries exactly one weight. Configurable, because peak
  memory is hardware-dependent and this is an operational knob that provably cannot change
  results once §1.2's equivalence test passes.
- **No recipe value moves.** 4096 rows, 16 bins × 256, batch-global prefix, frozen `R_ref`,
  `eps_soft`, the N=500 window, 1000/1000 budget: all unchanged.
- **The guard stays at 0.7.** The remedy reduces the peak; it does not move the alarm. If
  the peak still exceeds 0.7 after this work, that is a new fact requiring a new decision,
  not a licence to raise the threshold.

---

## 2. Decision B — per-term gradient telemetry becomes periodic

**Ruled: emit on a declared cadence, retaining all ten fields.**

Reasoning:

- The five `retain_graph=True` per-term traversals cost **4.4× wall clock** (671 s → 153 s
  per step) and are **provably observation-only**: `grad_norm` was bit-identical with them
  removed (627404864.0 in both runs). The project is paying 77% of its step time for data
  it does not use to make any decision inside the step.
- They are nonetheless a real instrument — they are what would show *which* loss term drives
  the causal front, and that is the question this band exists to answer. Deleting them would
  be trading away the diagnostic that matters.
- Cadence resolves both: keep the instrument, stop paying for it 980 times out of 1000.

### 2.1 Required shape

- Compute the five per-term norms on steps where the step record is logged
  (`run.log_every`, default 50), and on any step where a guard trips or a failure bundle is
  written — a failing step must carry full telemetry.
- On non-cadence steps, emit the ten fields as `null` with `grad_stats_complete: false` and
  a `grad_stats_provenance` value that names the skip explicitly. This reuses the schema's
  existing affordances rather than inventing new ones: the fields are already
  `Optional`, and `grad_stats_complete` already exists to mark incompleteness.
- **`STEP_LOG_FIELDS` keeps all ten field names.** The vocabulary is unchanged; only the
  population cadence is declared. This is what makes it a cadence ratification rather than a
  contract reduction.

### 2.2 Must be verified, not assumed

- **The guard must not weaken.** `grad_norm` reaches the guard from
  `clip_outcome.total_norm` after `total.backward()`, which is independent of
  `_build_gradient_stats`. Confirm this by test, so the loss-explosion and invariant-B
  guards keep full per-step fidelity.
- **No other consumer may depend on per-step availability.** Sweep the conformance census
  (`pinn/conformance/census.py:75-79`), the validation gate, and the TB sink before landing.

Expected effect at `log_every = 50`: ~45 h per graded seed instead of ~186 h, before any
gain from Decision A.

---

## 3. Also in scope — the resource preflight that does not exist

`57-05-PLAN.md` Task 3 already requires an "exact-4096 resource preflight … abort rather
than reduce it if resource preflight fails." No such check exists:
`pinn/conformance/preflight.py` contains no memory, resource, or watermark reference, and
`verify_phase57_evidence.py:247` mentions "resource" only when classifying a failure after
the fact. Generation 1 therefore discovered its ceiling by spending 852 seconds on it.

Build it: before the first optimizer step, exercise the real step path once at the
configured microbatch size and compare the observed `driver_bytes` against the watermark,
refusing with a typed error that names the measured fraction. This is a plan requirement
already on the books, not new scope.

---

## 4. Namespace and preservation (GAP-57-03, already resolved)

- Generation 1 is preserved: all 18 artifacts tracked in place under
  `runs/stage0-v23-smoke/`, 18/18 hash-verified, via 18 exact entries in the staged-path
  allowlist. No `runs/` wildcard was introduced.
- Generation 2 uses **`stage0-v23g2-{smoke,seed41,seed42,seed43}`**. Four new configs,
  identical to the current four except `run.run_name`, plus whatever knob §1.2 adds. This
  clears the sole `admit-run-window` fail-closed condition without moving preserved
  evidence.

---

## 5. Ordering

1. Decision A implementation + blocking equivalence test (§1).
2. Decision B cadence + guard-fidelity test (§2).
3. Resource preflight (§3).
4. Generation 2 configs (§4).
5. Re-run `admit-run-window`; expect a clean admission.
6. Then, and only then, the Wave-5 re-run under a fresh immutable HEAD — smoke first, its
   split/`S_H`/`n_train` equality checked against graded seed 42 per D-10, then seeds
   41/42/43.
7. Wave 6 remains gated exactly as written: it may not run on an operational block, and the
   held-out evaluation stays an owner checkpoint.

Steps 1–5 are preparation and carry no run authorization. Step 6 needs a fresh operator
authorization at the Wave-5 Task-2 checkpoint, which is unchanged.

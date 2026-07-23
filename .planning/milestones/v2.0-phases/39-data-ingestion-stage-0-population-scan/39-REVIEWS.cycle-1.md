---
phase: 39
reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
rerun_reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
reviewed_at: 2026-07-14T00:51:17Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T004323Z-21702
---

# Cross-AI Plan Review — Phase 39

## claude Review

I've read all seven plans, the SPEC, CONTEXT, gap register, and verified the disputed stage predicates directly against `ctl_instruction.md` and `.planning/REQUIREMENTS.md`. Review below.

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

Seven plans across six waves build a sole-reader in-memory admitted-set adapter (`pinn/data/`), a seven-clause Step-1A gate, a grouped split manifest, a replay/lookahead batch constructor, a Thrust-A Stage-0 scan, and a real-corpus phase-close gate. Structure is strong: Wave 0 lands a dataset-free unittest contract, Waves 1–4 implement TDD against it, Wave 5 runs the single expensive 6.3 GB pass and retains evidence in-repo.

The plans knowingly diverge from `39-SPEC.md` on stage classification. I verified this against the authoritative source: `ctl_instruction.md:138-198` defines Stage 0 as a **conjunction** (`E < -0.5`, `L/L_max > 0.5`, `0.7 ≤ Q ≤ 1.3`, strict `s_min > s₀`) over **Set 1a only** (original hierarchical, 4,857 files; `ctl_instruction.md:18-28`). `39-SPEC.md:55,106` states the opposite (`s_min > s₀` ⇒ Stage 1, equality ⇒ Stage 0) and omits the conjunction entirely. GAP-39-03/08 correctly route to CTL under SCOPE-18. **The plans are right and the SPEC is wrong** — but the consequences of that correction are not fully absorbed into the plans (see HIGH-1, HIGH-2).

## 2. Strengths

- **Sole-reader seam is mechanically enforced**, not just asserted: an AST audit with an exact allowlist (`pinn/data/adapter.py` + the grandfathered `pinn/verification/fixture_loader.py`), plus write-spies and root-containment checks. This is the right way to make DATA-01 durable.
- **Scientific prohibitions are tested, not documented**: footer `dE/E`, metrics JSON, and denominator-floor paths each get a negative test where the wrong source *disagrees* with the recomputed value. That is the correct shape for a "must-NOT" test.
- **Gap register is honest and well-grounded.** GAP-39-03's mathematical grounding, GAP-39-04's cancellation-scale reasoning, and GAP-39-07's RSS-vs-`resident_tensor_bytes` argument all demonstrate real understanding rather than pro-forma logging.
- **Determinism discipline throughout**: local `numpy.random.Generator` per signature, no global RNG/dtype mutation, canonical JSON + fsync + `os.replace`, byte-identity assertions on re-runs.
- **Wave 5 isolation** keeps the expensive corpus pass out of the inner loop while still refusing to accept synthetic-green as proof.

## 3. Concerns

### HIGH-1 — Plan 07 cannot close if Stage 0 is under-populated (self-contradiction)

`39-07-02` explicitly permits a below-240 outcome: *"A typed below-240 fatal is scientifically valid evidence but prevents a train-ready claim; record it rather than changing thresholds."* But `39-07-03`'s automated verify unconditionally requires `real_stage0_replay=240`, and `select_stage_records` (Plan 05) hard-fails with fewer than 240 replay keys. Note `has_stage1` gets a conditional branch in the same check — Stage 0 does not.

This matters more than it would have under the SPEC's definition. The SPEC's Stage-0 rule (`s_min ≤ s₀` over all admitted) would sweep in most of the corpus; the CTL conjunction restricted to Set 1a draws from at most 4,857 trajectories and then applies four simultaneous cuts. A sub-240 result is a live possibility, and the phase-close plan has no defined path for it — the executing agent will be pushed toward relaxing something to make the check pass.

**Fix:** make `39-07-03` branch on the fatal state exactly as it branches on `has_stage1` (e.g. `stage0_fatal=true` ⇒ record `observed=<n>`, skip the batch build, and close the phase with an honest fatal verdict routed to the owner).

### HIGH-2 — The split manifest and the batch constructor are never connected

DATA-04 exists to guarantee no `physical_key` spans train/val/test. But `select_stage_records` (Plan 05) consumes a `StageQuery` built by `StageIndex(records)` over the **whole admitted set** (Plan 04), and Plan 07 builds its real Stage-0 batch from that same unrestricted index. Nothing in any plan requires — or tests — that training batches draw only from the train split. The leakage invariant is enforced in a JSON file that no consumer reads.

Phase 40 owns training-loop plumbing, so this may be intentional, but the seam is undocumented, and it interacts with HIGH-1: if batches must eventually come from the train split, the effective replay pool is ~80% of Stage 0, so the real minimum is closer to 300 Stage-0 trajectories, not 240.

**Fix:** state the seam explicitly (e.g. `StageIndex.from_split(records, manifest, "train")`), add one test that a train-restricted index excludes val/test keys, and have Plan 07 record `stage0_train_split_count` alongside `real_stage0_replay`.

### HIGH-3 — `39-SPEC.md` is left standing with two acceptance criteria the plans deliberately violate

GAP-39-03 chose to *"keep the contradictory `39-SPEC.md` wording visible as the routed build-discovered spec defect."* The result is a locked SPEC whose AC at `:106` ("`s_min = s₀` exactly lands in Stage 0") and requirement at `:55` are now known-false, and whose AC at `:89` (repo-wide sole-reader grep) is superseded by GAP-39-02. Any downstream verifier checking implementation against SPEC will report failures that are actually correct behavior, and a future reader has no in-file signal that the SPEC is defective.

**Fix:** SCOPE-18 forbids editing the *framework specs*; it says nothing about the phase-local derived SPEC. Add a defect banner to `39-SPEC.md` pointing at GAP-39-03/08 next to each affected requirement/AC. Leaving a wrong criterion unmarked in the artifact that defines "done" is the failure mode SCOPE-18 is trying to prevent.

### MEDIUM-1 — Owner-facing `s_min` evidence is likely mis-scoped for its purpose

The scan's stated purpose is to let the owner ratify `s₀` for the **Stage-0/1 boundary**, which per CTL applies only to Set 1a. Plan 06 reports "exact sorted float64 s_min values" over adapter records without specifying the population; if that mixes standard-family and gold records, the distribution the owner ratifies against is not the distribution the threshold acts on. The report also gives a single count at the interim `s₀ = 0.01` — the owner cannot see how Stage-0 population responds to `s₀` without re-running.

**Fix:** break the `s_min` distribution out per (variant, fidelity), and add a small `s₀` sweep (Stage-0 count vs. a handful of candidate `s₀` values) to the report. This is read-only evidence, not ratification, so it stays inside the phase boundary — and it is exactly what makes the fatal signal in HIGH-1 actionable.

### MEDIUM-2 — Several invented constants are not gap-registered

GAP-39-04 correctly surfaced the `64·eps` factor. But the same class of choice appears un-surfaced elsewhere: the **1% measured-vs-reference `dt_out` disagreement warning** (Plan 02), the **Gumbel-top-k** weighted-sampling mechanism and `floor(n/2)` split (Plan 05), and the **Hamilton tie-order** (registered, but its consequences for rare strata are not bounded). The `dt_out` threshold in particular decides whether the real corpus emits a wall of warnings. These are all reversible, but the gap register's own standard would log them.

### MEDIUM-3 — Clause-2 quarantine input has no supplier

`evaluate_admission(parsed, *, blacklist, remediation_quarantine)` (Plan 02) requires a `remediation_quarantine` argument, but `AdmittedSetAdapter.__init__` (Plan 03) has no parameter or default for it. SPEC says this set is "empty in the verified baseline," which likely makes it an empty default — but the plans never say so, and clause 2 is a fail-closed gate. Specify the source and the empty-baseline default explicitly.

### MEDIUM-4 — IC/Brutus pairing failure is not an enumerated edge

The adapter must read both an IC file and a Brutus file per record to build IC₁₃. Plans cover missing/invalid blacklists, absent blacklisted IDs, duplicates, path escapes, malformed blocks, and non-finite values — but not a Brutus file present with **no matching IC file** (or the reverse). `simulation_data/Documentation/README.md` documents real dataset anomalies; this is the most likely one to bite on first contact.

### LOW-1 — Absolute personal path baked into a committed plan

`39-07-02` hardcodes `GSD_DATA_ROOT=<home>/Desktop/3_body_problem/simulation_data/Data`, and it will be echoed into committed `scan.log`. Given the repo may go public, prefer resolving from the environment and recording a repo-relative or redacted form in the evidence log.

### LOW-2 — Full-repo regression may be worktree-fragile

`39-07-01` runs `unittest discover -s tests`, which includes Phase 38 tests that depend on a trajectory fixture the trainex worktree does not carry by default. If that fixture is absent, `repository_suite=PASS` is unreachable for reasons unrelated to Phase 39. Worth a preflight check.

## 4. Suggestions

1. Make the Stage-0 fatal path a **first-class branch** in `39-07-03`, mirroring the `has_stage1` pattern (resolves HIGH-1).
2. Add the split→batch seam and one leakage test at the batch boundary; record the train-split Stage-0 count in Wave 5 evidence (resolves HIGH-2).
3. Annotate `39-SPEC.md` in place with a GAP-39-03/08 defect banner rather than leaving silently-false ACs (resolves HIGH-3).
4. Scope the `s_min` distribution per family/fidelity and add an `s₀` sensitivity sweep to `stage_population.json` (resolves MEDIUM-1, and makes a sub-240 result diagnosable rather than merely fatal).
5. Register the `dt_out` 1% threshold, the Gumbel-top-k choice, and `floor(n/2)` as gap entries or explicitly label them reversible defaults, consistent with how `64·eps` was handled.
6. Consider a single **owner ratification checkpoint before Wave 1**: GAP-39-04 (`64·eps`), GAP-39-06 (Hamilton signature), and GAP-39-07 (`resident_tensor_bytes`) were all self-resolved under the 2026-07-13 full-autonomy instruction. GAP-39-03 and GAP-39-08 are genuinely grounded in CTL and need no ruling — but the other three are agent-chosen semantics with HIGH/MEDIUM stated impact, and a single batched confirmation is cheap insurance against the exact drift the STOP protocol exists to prevent.

## 5. Overall Risk

**MEDIUM.**

The engineering is unusually disciplined — fail-closed defaults, mechanical audits, atomic writes, read-only corpus handling, and no destructive operations anywhere in the seven plans. Data-integrity and security risk is genuinely low.

The risk is concentrated in **phase-goal achievement**, not in safety. The plans correctly adopt the CTL stage definition, which is far narrower than the one the SPEC (and therefore the acceptance criteria, and therefore the 240 threshold's calibration) assumed. That narrowing makes an under-populated Stage 0 a realistic outcome, and Plan 07 currently has a self-contradictory response to it: one task says record the fatal honestly, the next task's gate refuses to pass without 240. Fix that branch and the split→batch seam, annotate the stale SPEC, and this drops to LOW.

---

## claude-glm Review

I have everything needed. The gaps are resolved with instruction (GAP-39-02, GAP-39-03 confirmed `RESOLVED-WITH-INSTRUCTION` under the 2026-07-13 autonomy directive), and I've confirmed the Wave-4 validation rows omit `test_prohibitions`. Here is the review.

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

Phase 39 builds the Phase-40-independent data substrate: a single in-memory admitted-set adapter (DATA-01), the full seven-clause Step-1A admission gate (DATA-02), compare-and-refuse data-version handling (DATA-03), a physical-key-grouped split manifest (DATA-04), a replay/lookahead two-point-set batch constructor (DATA-05), and the Thrust-A Stage-0 population scan with fatal-class flag (DATA-06).

The phase is decomposed into 7 plans across 6 waves: **W0** test contract (01) → **W1** types/parser/preprocessing/classifier/admission (02) → **W2** adapter residency (03) → **W3** splits (04) → **W4** batches (05) ∥ stage-scan (06) → **W5** phase close + real-corpus gate (07). The design is TDD-first: Plan 01 lands deferred unittests that skip on absent symbols, and Plan 07 gates that no skips remain. All eight GAP-39 entries are resolved with instruction; the plans cite CTL line ranges and gap resolutions at every numeric/semantic decision.

## 2. Strengths

- **Exemplary grounding discipline.** Every contested decision (near-zero H₀ quarantine, whole-trajectory non-finite quarantine, `mem:` byte numerator, sole classifier, reversed SPEC predicate) routes through a GAP entry with full STOP-protocol fields and a `RESOLVED-WITH-INSTRUCTION` note. GAP-39-03 (a build-discovered reversed predicate in the phase SPEC) is correctly resolved in favor of the authoritative CTL contract.
- **Clean scope boundaries.** Phase 40 adaptive sampler, FUT-02 Stage 1–6 recalibration, `s₀` ratification, and the hash producer are explicitly deferred in every plan's `prohibitions`. `files_modified` lists are tight and disjoint across the parallel W4 plans.
- **Defense-in-depth where it matters.** Blacklist membership is re-asserted at selection *and* at final batch assembly (Plan 05). The sole-reader and sole-classifier rules are mechanically AST-audited, not just grep-asserted.
- **Honest fatal handling.** A below-240 Stage-0 count is fatal *evidence*, not a threshold mutation; the report is still written and the phase can close with an honest "not train-ready" verdict (Plan 06/07).
- **Strong integrity controls at the corpus gate.** Plan 07 records spec SHA-256, a corpus fingerprint, byte-identical scratch→repo evidence copy, read-only `num_workers=0` adapter, and `git diff` guards against spec/corpus mutation.
- **Memory accounting is deterministic.** `resident_tensor_bytes` deduplicates by `untyped_storage()` identity (GAP-39-07), not RSS — making the 0.7-watermark assertion reproducible.

## 3. Concerns

### MEDIUM-1 — Prohibition audit not re-verified when W4 modules land
`test_prohibitions.py` is last tightened in Plan 03 (task 39-03-03) for the adapter/preprocessing/stages/admission set. The W4 plans (05 `batches.py`, 06 `stage_scan.py`) do **not** list `test_prohibitions.py` in `files_modified`, and their validation rows (39-05-01/02, 39-06-01/02) omit `test_prohibitions` from the automated command — it only re-runs at Plan 07 (39-07-01 discover, 39-07-03 explicit). Plan 01 states the "known-module superset becomes strict as each file lands," but no task extends that superset for the two W4 modules. If the superset is a strict whitelist, the audit could fail late (W5, not W4); if it is a generic scan, the coverage is fine but the plan should say so. The disjoint-files constraint that enables W4 parallelism is precisely what prevents either plan from editing the shared `test_prohibitions.py`.

### MEDIUM-2 — Phase SPEC acceptance criteria deliberately diverge from implementation
Per GAP-39-03, `39-SPEC.md` is intentionally left with the reversed predicate (`s_min > s₀` → Stage 1; equality → Stage 0) at lines 53–56 and 104–106, while the implementation (Plan 02 classifier) uses the authoritative CTL conjunction with strict `s_min > s₀` → Stage 0. The SPEC acceptance criterion "a trajectory with `s_min = s₀` exactly lands in Stage 0" (line 106) will therefore **not** be satisfied by the code. This is governance-resolved, but the divergence is reconcilable only by reading `39-GAPS.md` — a future verifier checking SPEC acceptance literally would flag a mismatch.

### LOW-1 — Hard-coded absolute corpus path in Plan 07
Task 39-07-02 bakes `GSD_DATA_ROOT=<home>/Desktop/3_body_problem/simulation_data/Data` into the validation command. This is correct for the owner's Mac (the payload lives in the master-root checkout, not the trainex worktree) but is machine-specific and non-portable. The SPEC describes `GSD_DATA_ROOT` as a configurable env var with a main-repo default; the plan command does not reflect that configurability.

### LOW-2 — Concurrent-session exposure at phase close
Three other sessions are active in this same `trainex` worktree on `milestone/v2.0`. Plan 07's verify asserts `git diff --check`, `git diff --exit-code -- ctl_instruction.md pinn_architecture.md`, and `test -z "$(git status --short -- simulation_data)"`. A concurrent agent committing during the real-corpus gate could trip these spuriously. The corpus scan itself is read-only, so the risk is confined to the git-state assertions.

### LOW-3 — Full-repository unittest gate
Task 39-07-01 runs `unittest discover -s tests` (the whole repo) and stops on any failure. An unrelated pre-existing regression would block phase close with no instruction to distinguish Phase-39 regressions from ambient ones.

### LOW-4 — GAP-39-08 status not fully confirmed
I could not capture the `Status`/`Resolution note` fields for GAP-39-08 (the sole-classifier seam) — my read window truncated at its option list. The plans consistently implement its option A and reference it as resolved, and GAP-39-02/03 follow the same `RESOLVED-WITH-INSTRUCTION` pattern, so it is very likely resolved; worth a direct confirmation.

## 4. Suggestions

1. **Resolve the W4 audit ambiguity explicitly.** Either (a) add `test_prohibitions` to the 39-05/39-06 verify commands and document that the generic prohibition scans auto-cover new `pinn/data/*.py` modules (so no superset extension is needed), or (b) if the superset *does* require extension, add a serial micro-task (before W4 or as a W4→W5 bridge) that registers `batches.py`/`stage_scan.py` — avoiding the shared-file edit inside the parallel wave.
2. **Annotate the SPEC in place.** Add a one-line pointer at `39-SPEC.md:104–106` noting the `s_min` predicate is superseded by CTL per GAP-39-03, so the spec is self-reconciling rather than dependent on the gap register.
3. **Parametrize the corpus path.** Read `GSD_DATA_ROOT` from env with the absolute main-repo path as the documented default, instead of hard-coding it in the 39-07-02 command.
4. **Triage rule for 39-07-01.** State whether an unrelated repository-suite failure blocks phase close (and must be triaged first) or is reported separately from the Phase-39 verdict.
5. **Confirm GAP-39-08 status** is `RESOLVED-WITH-INSTRUCTION` in the register.

## 5. Overall Risk

**MEDIUM (low end).** No HIGH concerns. The plans are well-grounded, scope-disciplined, and carry strong integrity and fail-closed controls; the gap register is resolved with instruction. The two MEDIUM findings are a deferred-audit-coverage question (catches regressions two waves late rather than at introduction) and a deliberate-but-underannotated spec divergence — both addressable by clarification/annotation without replanning.

---

## claude-deepseek Review

I now have a thorough understanding of all seven plans and their supporting documents. Here is my review.

---

# Phase 39 Plan Review

## 1. Summary

Phase 39 delivers the data ingestion and Stage-0 population scan for the v2.0 training pipeline: a format-aware fp32 in-memory adapter (DATA-01), the full seven-clause Step-1A admission gate (DATA-02), `data_version_hash` compare-and-refuse with typed absent-field deferral (DATA-03), a `physical_key`-grouped split manifest (DATA-04), a replay/lookahead two-point-set batch constructor (DATA-05), and the Thrust-A Stage-0 population scan with a fatal-class under-population flag (DATA-06).

The seven plans are organized as a TDD wave pipeline: Wave 0 writes deferred test contracts, Wave 1 implements pure types/parsing/admission/classification, Wave 2 integrates the production adapter, Wave 3 builds splits/StageIndex, Wave 4 constructs batches (Plan 05) and the scan (Plan 06) in parallel, and Wave 5 closes the phase with a real-corpus validation gate. All 18 tasks have automated verification. The goal is directly traceable to the ROADMAP.md Phase 39 entry and all six DATA requirements in REQUIREMENTS.md.

**Overall verdict: the plans are thorough and well-structured. They will likely achieve the phase goal.**

## 2. Strengths

- **TDD enforced throughout.** Every task from Wave 1 onward uses `tdd="true"` and references the Wave 0 deferred test contracts. The unlock-tests-first-then-implement pattern is consistent and traceable.
- **Edge coverage is comprehensive.** 19/19 edge cases resolved in SPEC.md (adjacency, empty, ordering, boundary, precision). Two new edge-derived acceptance criteria (`s_min == s₀` boundary, empty-admitted-set hard failure) close gaps not in the original REQUIREMENTS.md text.
- **Single-classifier invariant enforced across all components.** GAP-39-08 resolves the stage-label production seam: only `pinn/data/stages.py` assigns numeric labels, only for original/base hierarchical Set 1a, with all gold records as `UNASSIGNED`. Every plan from splits to batches to scan reinforces this with `gold_numeric_stage_count == 0` assertions.
- **Threat modeling is systematic.** All 12 STRIDE threats (T-39-01 through T-39-12) are mapped to tasks with specific mitigations — path containment, write-spy audits, AST-based reader audits, atomic fsync+replace manifest/report writes.
- **Phase 40 boundary is clean.** The plans repeatedly enforce that adaptive collocation, epoch iteration, loss wiring, and optimizer feeding are NOT in scope. The batch constructor emits fixed point sets; Phase 40 makes them adaptive.
- **Real-corpus gate is isolated in Wave 5 only.** The 6.3 GB real dataset is touched exactly once during phase close, preventing it from slowing normal feedback loops. All other waves use synthetic `TemporaryDirectory` fixtures.

## 3. Concerns

### HIGH — SPEC.md contains a known contradictory acceptance criterion

**What**: SPEC.md line 106 (acceptance criteria) states: *"A trajectory with `s_min = s₀` exactly lands in Stage 0 (Stage-1 criterion is strict `> s₀`)."* This is acknowledged in GAP-39-03 and RESEARCH.md line 109 as a "routed build-discovered spec defect" — the authoritative CTL and integrity-r2 clearance mandate strict `s_min > s₀` for Stage 0, meaning equality does NOT land in Stage 0.

**Why it matters**: An implementer reading the SPEC directly (without tracing through GAP-39-03) would implement the wrong boundary condition. The plans correctly implement the strict interpretation (Plan 02 task 39-02-02 uses `strict s_min > interim_s0`), but the SPEC document remains authoritative-adjacent and contradictory.

**Mitigation**: The SPEC should be amended to match the GAP-39-03 resolution before execution begins, or a prominent warning should be added to the SPEC's R6-boundary row referencing the override.

### HIGH — Wave 4 parallelism risk between Plans 05 and 06

**What**: Both plan 05 (batches) and plan 06 (stage scan) execute in Wave 4 with plan 04 as their only dependency. Both are marked `autonomous: true`. Each explicitly says it modifies no files owned by the other plan. However, both consume `pinn/data/types.py` and `pinn/data/adapter.py` — if either plan discovers a need to modify `types.py` (e.g., adding a batch-related field or a scan-related field to a shared frozen dataclass), they will conflict. Plans 05 and 06 were written before any Wave 4 code exists, so undiscovered type-sharing needs are the risk.

**Why it matters**: A type conflict discovered during parallel execution would force one plan to wait, or worse, a merge conflict that silently drops one plan's additions.

**Mitigation**: Consider sequencing Plan 06 after Plan 05 (or vice versa), or adding an explicit coordination check in both plans' success criteria that they must `diff --check` against each other's touched files.

### MEDIUM — No synthetic end-to-end integration test

**What**: The plans test each component in isolation (adapter, admission, splits, batches, scan) but there is no single test that exercises the full pipeline end-to-end: adapter init → StageIndex → split → batch → scan, all on the same synthetic fixture. Plan 07 covers this with the real corpus, but a synthetic E2E test would catch wiring bugs (e.g., the adapter's persisted stage label not matching what `StageIndex` expects) without needing the 6.3 GB dataset.

**Why it matters**: Integration bugs across module boundaries are the most common failure mode in multi-wave implementations. The Phase 38 rebuild likely had similar risks.

**Mitigation**: Add a single synthetic E2E test in Plan 07 task 39-07-01 (or a new task in Plan 03) that runs the full pipeline on a `TinyCorpus` fixture.

### MEDIUM — `resident_tensor_bytes` uses PyTorch internal storage API

**What**: Plan 03 task 39-03-02 specifies memory accounting via `untyped_storage()` identity/data pointer deduplication to compute `resident_tensor_bytes`. This uses PyTorch's internal storage representation which is not part of the stable public API.

**Why it matters**: A PyTorch version bump could change the internal storage identity semantics, causing the memory check to silently over-count or under-count. The `mem:` line is a hard gate (fails if fraction > 0.7), so a miscount would incorrectly refuse or allow preload.

**Mitigation**: The plan already prohibits RSS/MPS as a replacement — that's correct. Consider adding a coarse-grained sanity check (e.g., `n_snapshots × 7 × 4 bytes` ballpark) as a cross-validation log line.

### MEDIUM — `data_version_hash` deferral is non-functional on the real corpus

**What**: GAP-39-01 resolves that Phase 39 implements compare-and-refuse but no hash producer exists (U-12 upstream). Plan 07 task 39-07-02 will invoke the real-corpus scan without a hash, triggering the typed `DataVersionHashDeferred` path. The scan proceeds. This means the real-corpus gate provides no version-integrity protection.

**Why it matters**: If the on-disk corpus changes between the scan and a future training run (due to a user copy, symlink shift, or accidental edit), nothing will detect it. This is an acknowledged deferral, not a bug, but it means the DATA-03 safety mechanism is a no-op during phase close.

**Mitigation**: Document in the phase-close `scan.log` that no hash was supplied and the deferral was triggered. Consider computing and recording a lightweight corpus fingerprint (file count, total bytes, hash of sorted path listing) in the report as an informal cross-check even without the formal hash producer.

### LOW — Phase-close evidence directory re-run friction

**What**: Plan 07 task 39-07-01 says to "fail if `phase-close` already contains unrelated evidence rather than overwriting it." This means re-running the phase close requires manual cleanup of the evidence directory.

**Why it matters**: Minor operational friction. If a real-corpus scan fails partway through, re-running requires deleting the evidence directory first. The plan's intent (never silently overwrite evidence) is correct, but the UX could be smoother.

### LOW — Batch constructor shape-alignment complexity

**What**: The batch constructor must emit `(N, 14)` with time-sampled τ values concatenated with normalized IC13, plus aligned `(N, 3)` raw masses per trajectory. Plan 05 specifies this correctly, but the per-record `n_pts = min(32, n_snapshots)` can differ across the 240 selected trajectories, producing irregular per-trajectory point counts that must be concatenated into the final `FixedBatch`.

**Why it matters**: Shape alignment bugs here would manifest as silent training corruption (mismatched IC13/mass rows) that unit tests on tiny fixtures might miss. The Plan 05 task 39-05-02 requirement for a "smoke call" against the network partially mitigates this.

## 4. Suggestions

1. **Amend SPEC.md line 128 (Edge Coverage R6-boundary row)** to match the GAP-39-03 resolution and the plans' implementation: change from "`s_min = s₀` exactly → Stage 0" to "`s_min = s₀` → NOT Stage 0 (strict `>` criterion)." This removes the contradiction before implementation begins.

2. **Sequence Plans 05 and 06** instead of running them in parallel, or add a cross-check in both plans that `git diff --check -- pinn/data/types.py` shows no conflict with the other plan's intended modifications. The risk of a hidden `types.py` conflict outweighs the modest wall-clock savings of parallel execution.

3. **Add a synthetic E2E test** (adapter → StageIndex → split → batch → scan on a `TinyCorpus`) in Plan 07 task 39-07-01 or as a new task. This would catch integration bugs before the real-corpus gate.

4. **Add a coarse memory ballpark cross-check** alongside the `untyped_storage()` dedup: log `expected_bytes ≈ total_snapshots × 7 × 4` as a sanity line. A discrepancy > 5% between expected and `resident_tensor_bytes` should warn.

5. **Record a lightweight corpus fingerprint** (sorted path list + sizes, no file content) in `scan.log` even when the formal `data_version_hash` is absent, as an informal cross-check for the deferred hash producer.

6. **Consider making the evidence directory re-run-safe**: accept a `--force` flag or auto-archive the prior evidence directory rather than failing.

## 5. Overall Risk: MEDIUM

The plans are thorough, well-referenced, and correctly implement all six DATA requirements. The TDD wave structure, consistent gold-exclusion invariant enforcement, and isolated real-corpus gate are all strong design choices.

The risk is MEDIUM rather than LOW because of: (a) the execution complexity of six interconnected production modules built across five waves with 8 autonomy-resolved gaps (GAP-39-03..08) — each a place where the implementation must correctly interpret a non-authoritative ruling; (b) the Wave 4 parallelism risk; and (c) the absence of a synthetic E2E integration test before the real-corpus gate. None of these are blockers, but they warrant attention during execution.

---

## codex Review

## 1. Summary

Phase 39 plans are largely coherent and appear capable of delivering the DATA-01..06 substrate: adapter, admission, version handling, splits, batches, Stage-0 scan, and retained evidence. The main risk is not missing scope, but that the final real-corpus proof in `39-07-PLAN.md` can be made stricter to avoid false-positive closure.

## 2. Strengths

- Clear wave ordering: tests/contracts first, then parser/admission, adapter integration, splits, batches/reporting, and final real-corpus gate.
- Strong scope control: Phase 40 training-loop/adaptive work, `s0` ratification, hash production, corpus mutation, and framework-spec edits are repeatedly excluded.
- Good data-integrity posture: single-reader rule, read-only corpus handling, root containment, blacklist fail-closed behavior, atomic manifest/report writing, and byte-retained evidence are explicitly planned.
- Edge coverage is unusually strong for numeric and scientific-data cases: near-zero Hamiltonian handling, non-finite quarantine, sparse IDs, base/gold separation, exact `s_min` boundary, and zero numeric gold labels.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** `39-07-PLAN.md` can still accept stale or failed real-corpus evidence too easily. It uses fixed `/tmp/phase39-real-scan` scratch state and verifies only that `scan_exit_code` is numeric, not that it is zero or an explicitly allowed typed fatal outcome. Since Phase 39’s success depends on the real-corpus gate, the final proof should require freshness and an allowed terminal state.

- **MEDIUM:** The real-corpus command source is inconsistent. `39-07-PLAN.md` treats the scan command as exact and says to read it from `39-VALIDATION.md`, but `39-VALIDATION.md` only contains post-checks, while `39-RESEARCH.md` says the command shape is proposed. This should be reconciled before execution.

- **MEDIUM:** The final “no deferred production-symbol skip” check relies on grepping a specific phrase. `39-01-PLAN.md` requires localized skips, but does not clearly require the `_require` helper to emit that exact phrase. A different skip message could leave a Phase 39 test skipped while the final grep still passes.

- **LOW:** Threat references drift across artifacts. `39-VALIDATION.md` references IDs such as `T-39-08`, `T-39-10`, `T-39-11`, and `T-39-12`, while its consolidated threat table only lists `T-39-01..06`. The per-plan threat registers cover more IDs, but central traceability is harder to audit.

## 4. Suggestions

- Make the phase-close run directory unique or record a run nonce/start/end marker in both scratch and retained evidence, then verify it.
- Require `scan_exit_code=0` unless the report contains a specific typed fatal/admission outcome from an allowlist.
- Move the exact real-corpus command into `39-VALIDATION.md` or change `39-07-PLAN.md` to name the plan itself as the command source.
- Standardize `_require` skip text and make final validation fail on any Phase 39 skip after Wave 5.
- Normalize threat IDs or add a central threat-ID index in `39-VALIDATION.md`.

## 5. Overall Risk (MEDIUM)

The plans are strong enough to execute after tightening the phase-close evidence gate. The remaining risks are concentrated in validation/provenance, not in the core dependency order or phase scope.

---

## agy Review

# Cross-AI Plan Review: Phase 39 Data Ingestion

## 1. Summary
The Phase 39 plans present a comprehensive, read-only, dataset-free ingestion and Stage-0 batching pipeline. It correctly uses five sequential waves to build isolated unittests, implement parser/admission/classification, build an in-memory resident adapter, and construct physical splits, batching, and a Thrust-A scan report. The test-driven approach and explicit invariants (such as `gold_numeric_stage_count == 0`) provide excellent defense-in-depth, though a few unhandled numerical edge cases pose crash risks.

## 2. Strengths
- **Strict Verification First**: Wave 0 defines all assertions up front, allowing deferred tests to act as exact contracts for the later waves without premature test execution.
- **Data Protection**: Explicit read-only handling of the corpus, strict root containment, mechanical audits to ban unintended readers, and the use of an AST write-spy provide exceptional data integrity guarantees.
- **Clear Invariants**: End-to-end enforcement of `gold_numeric_stage_count == 0` and strict reliance on the single pre-residency `classify_stage_label` seam prevents split/batch/report logic from drifting or leaking base/gold fidelity.

## 3. Concerns

- **HIGH: Potential TypeError in Stage 0 Classifier (`L_norm`)** 
  Plan 39-02-02 defines `Lmax` computation, specifying it resolves to `None` when non-finite or `<1e-10`. The Stage 0 predicate then evaluates `L_norm > 0.5`. In Python, evaluating `None > 0.5` will raise a `TypeError`, consistently crashing classification on near-degenerate records.
- **HIGH: Potential TypeError in Batch Construction (`tau`)** 
  Plan 39-05-02 specifies calculating `tau = 2*(t/T) - 1`. If `T` refers to `t_end` from the reference metadata, Plan 39-02-01 explicitly states that `t_end` remains `null` when a footer is absent. Python will raise a `TypeError` when evaluating `t / None`. 
- **MEDIUM: Lost Report on Fatal Threshold** 
  Plan 39-06-01 instructs `build_population_report` to "create/raise `StageZeroUnderpopulated`" if the Stage 0 count is < 240. If the exception is raised before the builder returns the report, the caller in `main()` cannot write the report for diagnosis as instructed by 39-06-02 ("Fatal report remains written for diagnosis before nonzero exit").
- **LOW: Division by Zero Risk in `eps_H`** 
  Plan 39-02-03 instructs the admission logic to "apply GAP-39-04 exactly with no denominator substitute, then `eps_H = max(abs((H-H0)/H0))`". If a trajectory triggers the near-zero `H0` quarantine (GAP-39-04), computing `eps_H` immediately after without short-circuiting will cause a `ZeroDivisionError` or overflow.

## 4. Suggestions
- **Handle `None` in Classifier**: Update 39-02-02 to explicitly handle `L_norm is None` within the Stage 0 gate (e.g., short-circuiting to `UNASSIGNED`).
- **Clarify `T` in Batching**: Update 39-05-02 to explicitly define `T` as `times[-1]` (the last valid timestamp of the parsed array) or provide a fallback if `T` refers to a nullable `t_end`.
- **Evaluate Threshold After Writing or Attach Report**: In 39-06, instruct `build_population_report` to either attach the constructed report to the `StageZeroUnderpopulated` exception object, or have the CLI evaluate the fatal `<240` threshold *after* `write_population_report` completes.
- **Short-circuit Admission Quarantines**: In 39-02-03, explicitly instruct the admission evaluator to short-circuit and return the quarantine state for near-zero `H0` *before* attempting the `eps_H` relative drift division.

## 5. Overall Risk
**HIGH** — The pipeline architecture and security controls are exceptionally strong, but unhandled Python type semantics (`None > 0.5` and `t / None`) will cause runtime crashes during real-corpus batching and classification. Fixing the explicit numerical null-handling will reduce this to LOW.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=221
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=11197
- stderr_bytes=0

### claude-glm
- reviewer=claude-glm
- exit_code=0
- elapsed_seconds=474
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=7760
- stderr_bytes=192

### claude-deepseek
- reviewer=claude-deepseek
- exit_code=0
- elapsed_seconds=146
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp deepseek -p - 
- stdout_bytes=11015
- stderr_bytes=192

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=265
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3297
- stderr_bytes=56972

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=94
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=3871
- stderr_bytes=0

---

## Verification coverage (xconverge source-grounding pass, cycle 1)

Effective authority: `grep` (from `gsd drift-guard authority --raw`).

Symbol scope: Phase 39 plans are greenfield — they declare their targets
(`pinn/data/*.py`, `tests/phase39/`, evidence paths) under each plan's
"Artifacts this phase produces" / `files_modified`, so those are excluded
from verification per the workflow's new-artifact rule. Verified
pre-existing references instead:

- Framework spec hash-lock targets — VERIFIED:
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (exists, 126313 B)
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (exists, 65522 B)
- Requirement IDs DATA-01..DATA-06 — VERIFIED at `.planning/REQUIREMENTS.md:48-53`; all map to Phase 39 in the req→phase matrix (`:161-165`).
- `pinn/` package — VERIFIED (exists); `pinn/data/` is absent (greenfield, declared as new artifact).
- FUT-02 deferral cross-reference — VERIFIED at `.planning/REQUIREMENTS.md:110`.

No hard-block symbols (authority `lsp`/`scip` with MISSING) were found.
No AMBIGUOUS or UNCHECKABLE signature claims were asserted under `grep`
(the plans reference no pre-existing callable signatures; all callables
are new artifacts created this phase).

Verdict: source-grounding gate PASSED (no hard blocks). Proceed to replan.

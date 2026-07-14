---
phase: 39
reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
rerun_reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
reviewed_at: 2026-07-14T02:03:17Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T015738Z-21382
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 39

## claude Review

I read all seven plans plus the SPEC, CONTEXT, gap register, validation map, and cross-checked the dataset README and the CTL batch/normalization contract. Review below.

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

Seven plans across six waves: a Wave-0 dataset-free test contract (39-01), pure production contracts + parser + seven-clause admission + sole stage classifier (39-02), the production `AdmittedSetAdapter` (39-03), the grouped split manifest (39-04), the replay/lookahead batch constructor (39-05), the Thrust-A scan/CLI (39-06), and a real-corpus phase-close gate with retained evidence (39-07). The decomposition is sound, the dependency chain (0→1→2→3→{4,5}→5) is coherent, and every SPEC requirement and gap resolution is traceable to a task. The plans do achieve the phase goal on paper. My concerns are concentrated in three places: a memory cross-check that is arithmetically wrong and will fire on every real run, a Stage-0 fatal threshold applied to the wrong population, and an IC/Brutus pairing rule that the plans never state and that the real corpus violates in a way the synthetic fixtures will not catch.

## 2. Strengths

- **Single-seam discipline is enforced mechanically, not by convention.** The AST reader audit, the `pinn/data/stages.py` sole-classifier rule (GAP-39-08), and the write-spy/root-containment tests are strong controls, and the `gold_numeric_stage_count == 0` invariant is re-asserted at adapter init, StageIndex, split, batch assembly, and report — the right defense-in-depth for a leakage-class bug.
- **Fail-closed scientific gates.** `eps_H` recomputed in float64 from raw arrays, no denominator floor, no footer `dE/E`, no metrics-JSON shortcut, whole-trajectory quarantine on non-finite blocks, and blacklist schema hard-failure are all specified with negative tests rather than prose.
- **The GAP-39-03 spec-defect routing is handled correctly.** Rather than editing the authoritative CTL spec or silently implementing the reversed predicate, the plans implement CTL and add a banner to the phase-local SPEC. That is the right call under SCOPE-18.
- **Real-corpus evidence hygiene.** Freshness markers, allowlisted exit codes, byte-identity between scratch and retained report, spec-hash and corpus-fingerprint checks, and path redaction are unusually thorough for a phase-close gate.
- **Determinism is specified at the level that matters**: canonical JSON + fsync/replace, seeded local `Generator`s, Hamilton apportionment with a fixed tie order, no global RNG mutation.

## 3. Concerns

### HIGH

**H1 — The `resident_tensor_bytes` ballpark cross-check is off by ~2.7× and will warn on every real run (39-03, task 39-03-02).**
The plan defines `ballpark_bytes = total_admitted_snapshots * 7 * 4`, glossing 7 as "3 positions + 3 velocities + 1 time". But 7 is the per-*body row* width in the Brutus format; a snapshot holds three body rows, so the resident payload per snapshot is ~19–22 fp32 (1 time + 9 positions + 9 velocities), not 7. The SPEC's own figure confirms this: ~8.23M snapshots ≈ 0.72 GB fp32 ⇒ ~87 bytes/snapshot ⇒ ~22 floats. With the planned formula the ballpark is ~230 MB against a true ~0.72 GB, a 171% misfit — far above the 50% threshold — so `resident_tensor_bytes_misfit` fires unconditionally on the real corpus. Worse, the natural "fix" during execution is to adjust whichever number is easier, and one of those adjustments (tuning the dedup count down to meet the ballpark) silently defeats the 0.7 watermark hard gate the check exists to protect.

**H2 — The Stage-0 fatal threshold is evaluated on the full admitted set, but batches are drawn from the train split (39-06 vs 39-05/39-04).**
`build_population_report` raises `StageZeroUnderpopulated` only when the *full-corpus* Stage-0 count is < 240, while `select_stage_records` requires 240 unique replay keys — and per the HIGH-3 seam, Phase 40 draws them from `StageIndex.from_split(..., "train")`, i.e. ~80% of Stage 0. A Stage-0 population of, say, 260 passes the DATA-06 scan with exit 0 and then makes training structurally impossible (~208 train keys). Plan 07 does record `stage0_train_split_count` and a `phase39_stage0_fatal` branch, but that is evidence-time detection in Wave 5 — the shipped scan CLI, which is the artifact the owner runs and ratifies `s₀` from, still reports the wrong readiness verdict. The fatal criterion should be the train-restricted count (or equivalently ≥ 240/train_ratio on the full set), with both numbers in the report.

**H3 — Gold Brutus folders pair to the *base* IC folders; no plan says so, and the new missing-sibling quarantine will punish that.**
`simulation_data/Documentation/README.md:155,176-177` is explicit: the `*_for_gold_standard` IC folders were deleted, so `brutus_hierarchical_gold_standard/brutus_hierarchical_XXXX.txt` reads its IC from `ic_final/ic_hierarchical/`. Four Brutus folders map to **two** IC folders. Plan 02 says only "exact filename regex/folder tables for the four Brutus variants and paired IC folders" — the 4→2 mapping is never stated — while Plan 01's fixture builder says it creates `ic_final` and "all four exact `brutus_output` folders" without pinning the IC side to two. If the fixture materializes four IC folders and the adapter assumes a 1:1 folder pairing, every gold record on the real corpus quarantines as `missing_ic_sibling` while the entire synthetic suite stays green. Gold is ~91% of all snapshots and supplies the `gold_stage_or_missing` slot in the DATA-04 split signature, so this corrupts admission counts, split strata, and the Thrust-A byte report — and it surfaces only at the Wave-5 corpus gate.

### MEDIUM

**M1 — Collocation point allocation across trajectories is unspecified (39-05).** The batch fixes `collocation_count=4096` and draws over `[0, T]` with per-record `T = times[-1]`, but never says how the 4096 points distribute over the selected trajectories. It divides evenly for a 256-trajectory batch (16 each) and not for a 240-trajectory replay-only batch. Each collocation point also needs an IC₁₃/mass channel to reach the network, so the assignment is load-bearing, not cosmetic. State the rule (e.g. per-trajectory `ceil`/remainder with a deterministic order, or `collocation_per_traj` as the knob).

**M2 — `FixedBatch` carries no per-record `T`, and DATA-01 exposes no `T` accessor.** CTL:1596 defines `T = t_max` and the loss assembly (CTL:1757) is dimensionless in `u = t/T`, so the Phase 40 physics/energy residuals need `T` per trajectory to rescale derivatives. The batch fields listed are τ/IC₁₃/masses/targets/times/keys/provenance, and DATA-01's accessors are `n_snapshots` and `dt_out` only. Phase 40 would have no supported way to recover `T`. Add it to `FixedBatch` (and/or as an accessor) now — it is a one-field change here and a cross-phase seam break later.

**M3 — `StageIndex.from_split` has two different signatures across plans.** 39-04 defines `from_split(records, manifest, split_name)`; 39-05 and 39-07 both call `from_split(adapter, manifest, "train")`. Passing an adapter where a record collection is expected will not type-check as written. Pick one (an adapter-or-records union is fine, but say so).

**M4 — Wave-4 parallelism is not as clean as `files_modified` suggests.** Plans 05 and 06 declare disjoint files, but 39-06's verify command runs `tests.phase39.test_prohibitions`, which is a whole-tree AST audit that discovers `pinn/**/*.py` — including `pinn/data/batches.py` while Plan 05 is mid-write. That is an ordering-sensitive, potentially flaky gate. Either drop `test_prohibitions` from 39-06's verify (39-07-03 re-runs it anyway) or serialize the two.

**M5 — The Wave-5 verify gate depends on `/tmp` surviving.** 39-07-02's automated check does `test -s /tmp/phase39-real-scan/stage_population.json` and `cmp` against the retained copy. Re-running the phase verification after a reboot or a `/tmp` sweep fails even though the committed evidence is intact — contradicting the plan's own "`/tmp` is disposable scratch" stance. Record the scratch SHA-256 in `scan.log` and compare hashes instead of requiring the scratch file.

**M6 — The data-root fallback is unspecified and worktree-hostile.** Plans say "explicit arg → `GSD_DATA_ROOT` → main-repo `simulation_data/Data`", but never how the third leg is derived. In `.worktrees/trainex` there is no `simulation_data/Data`, so a `__file__`-relative default silently points at a nonexistent path, and a literal `<home>/...` default would bake a personal path into production code — directly against the redaction discipline the same phase enforces on its logs. Specify the derivation (e.g. `git rev-parse --git-common-dir`-based, or make `GSD_DATA_ROOT` mandatory and fail loudly).

### LOW

**L1 — `mem_ballpadck` is a typo baked into a contract string.** It appears as the literal log key and in an acceptance criterion in 39-03. Fix to `mem_ballpark` before it becomes a grepped invariant.

**L2 — Redaction enforcement is pattern-narrow.** 39-07-02's verify only rejects `^GSD_DATA_ROOT=/Users/` and `command: .*GSD_DATA_ROOT=/Users/`. Adapter-emitted lines (resolved root, blacklist path, per-folder logs) can carry absolute `/Users/...` and pass. A blanket `! rg -q "/Users/"` over the retained logs matches the stated N12 intent.

**L3 — `regime` in the DATA-04 split signature `(regime, base_stage_label, gold_stage_or_missing)` is never defined** — presumably `variant` (hierarchical/standard). Name it consistently with `PhysicalKey`.

**L4 — Two SPEC acceptance criteria remain knowingly false by design.** DATA-06's "`s_min > s₀` ⇒ Stage 1, else Stage 0" and the AC "`s_min = s₀` exactly lands in Stage 0" are contradicted by the CTL conjunction the plans implement (equality ⇒ neither Stage 0 nor Stage 1 ⇒ `UNASSIGNED`). The banner approach in 39-02-04 is the right mitigation, but any downstream goal-backward verifier reading the AC checklist literally will flag correct behavior. Make sure the phase VERIFICATION step is routed to GAP-39-03/08 explicitly.

## 4. Suggestions

1. Fix H1 by deriving the ballpark from the actual resident layout (`snapshots × 19 × 4`, or better, `sum(t.numel() * t.element_size())` over a second independent traversal) and keep the 50% band; a check that always fires is worse than no check.
2. Fix H2 by making `build_population_report` take the split manifest (or the train ratio) and adjudicate the fatal on the train-restricted Stage-0 count, reporting both counts. This also makes the owner's `s₀` ratification evidence match the population that actually trains.
3. Fix H3 by pinning the folder table in 39-02 (four Brutus variants → two IC folders, gold reads the base IC) and by making 39-01's `TinyCorpus` mirror the real two-IC-folder layout, with an explicit test that a gold record admits with its base IC sibling.
4. Add per-record `T` to `FixedBatch` and state the collocation-per-trajectory rule (M1/M2) before Wave 4 starts — both are cheap now, expensive at the Phase 40 boundary.
5. Reconcile the `from_split` signature (M3) in 39-04 and let 39-05/39-07 quote it verbatim, the same way 39-07-02 defers the real-corpus command to 39-VALIDATION.md.
6. Note for the record: because gold records can never carry a numeric label, the adapter preloads ~91% of all snapshots (gold) that cannot enter a Phase 39 batch. That is correct under GAP-39-08 and harmless at 0.72 GB, but worth stating in the summary so it is not mistaken for a bug later.

## 5. Overall Risk

**MEDIUM.** The governance, security, and determinism posture is strong, and no destructive-operation or corpus-mutation risk is present (read-only adapter, write spy, atomic writers, containment checks, no history rewriting). The risk is concentrated in three correctness defects that all share one property: they pass the entire dataset-free suite and surface only at the Wave-5 real-corpus gate — H3 potentially as a mass gold quarantine, H2 as a false "proceed", H1 as a warning the operator is trained to ignore. Fixing H1–H3 and M1–M3 before Wave 1 starts would put this at LOW.

---

## claude-glm Review

API Error: 529 [1305][该模型当前访问量过大，请您稍后再试][20260714100125cd46a86228ed421f]. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (127.0.0.1:4148).

---

## claude-deepseek Review

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

The seven plans (39-01 through 39-07) deliver a complete, well-structured implementation of the six DATA requirements. The plan architecture uses a five-wave pipeline: Wave 0 establishes deferred test contracts before any production code; Waves 1–4 build types, parser, admission, adapter, splits, batches, and scan in strict dependency order; Wave 5 gates everything behind a single read-only real-corpus run with retained evidence. Nine gaps were discovered during research, all resolved or deferred with explicit engineering decisions — including one critical SPEC defect (GAP-39-03: reversed `s_min` predicate) that was correctly routed around via the authoritative CTL contract. Cross-AI review findings (N1–N13, HIGH-1 through HIGH-5) are thoroughly integrated.

## 2. Strengths

- **Test-first architecture.** Wave 0 creates the complete nine-file test suite as deferred contracts (`_require` skip helper) before any production module exists. This enforces spec-faithful implementation and prevents test-after-the-fact gaps.
- **Gap discipline.** Nine gaps were correctly surfaced under the STOP protocol and resolved with engineering grounding. GAP-39-03 (reversed SPEC predicate) is the standout — the plans implement the authoritative CTL conjunction, not the derived-SPEC error, and Plan 02-04 annotates the SPEC with defect banners rather than silently rewriting it.
- **Fail-closed everywhere.** Blacklist missing → hard failure. Hash mismatch → hard error. Empty admitted set → init failure. Stage 0 < 240 → fatal signal with report persisted before nonzero exit. Corpus write → mechanical audit rejection. No silent proceed path exists.
- **Cross-module integration contract.** The `StageIndex.from_split(records, manifest, "train")` seam (HIGH-3) connects DATA-04's split manifest to DATA-05's batch constructor, with Plan 07 exercising it end-to-end on the real corpus. This prevents the split manifest from becoming a file no consumer reads.
- **Memory accounting rigor (N7).** The `resident_tensor_bytes` dedup + `mem_ballpadck` ballpark cross-check prevents a `untyped_storage()` miscount from silently flipping the 0.7 watermark.
- **Per-plan threat models.** Every plan carries a STRIDE register with specific mitigations, not boilerplate.
- **Wave-4 parallelism.** Plans 05 (batches) and 06 (stage scan) are correctly independent — both consume Plan 04's splits but don't share mutable state — and Plan 07's Phase 38 fixture preflight (N13) guards against regression masking.

## 3. Concerns

### HIGH

- **GAP-39-01 — `data_version_hash` producer remains open.** The compare-and-refuse path works, but the typed `DataVersionHashDeferred` deferral means the hard-refuse path is effectively dead code on the real corpus until an upstream producer is ratified. This is correctly documented and deferred, but Phase 40 (training loop) will inherit the same unresolved seam. **Mitigation**: already surfaced in the gap register; the Phase 39 → Phase 40 handoff should explicitly flag this.

- **SPEC.md defect banner edit (Plan 02-04).** Editing `39-SPEC.md` post-spec-phase is unusual. The CONTEXT.md states at line 12: "this document does not reopen their what or why." The annotations are defensive (preventing a future literal verifier from flagging correct behavior as a failure), and the task verification confirms no framework spec is touched. Still, this crosses the "SPEC is frozen after spec phase" expectation. **Mitigation**: the task is scoped to annotation-only (no text rewrite) and the acceptance criteria are precise about what changes.

### MEDIUM

- **`mem_ballpadck` typo.** Plan 03-02 introduces the ballpark cross-check field as `mem_ballpadck` (missing "r"). This will propagate to log output and tests. Trivial to fix, but once committed in log format, it becomes a permanent artifact.

- **Plan 07 evidence redaction edge case (N12).** The verification grep at line 110 checks `GSD_DATA_ROOT=/Users/` and expects it absent from retained logs. If `GSD_DATA_ROOT` is unset and the fallback main-repo path is used, the fallback path (which resolves to `<home>/...`) could leak into logs through other channels (e.g., the adapter's resolved root). The redaction logic in the plan text is sound, but the implementation must be thorough.

- **`s0_sensitivity_sweep` scope expansion (N1).** Plan 06-01 adds a diagnostic sensitivity sweep recomputing Stage-0 counts at a geometric grid via the sole `classify_stage_label` seam. This is not in the original SPEC's DATA-06 requirement but is explicitly read-only, never mutates residency, and is clearly labeled as reversible. It's a reasonable diagnostic addition, but technically expands scope beyond the letter of DATA-06.

### LOW

- **`39-PATTERNS.md` and `39-VALIDATION.md` referenced but not in review file list.** Plan 01 cites both as context. These are likely present and well-formed given the plan quality, but I cannot verify their content against the plans.

- **`phase-close` directory naming.** The evidence directory name `phase-close` is slightly confusing — it IS the phase close, not a sub-phase. Minor.

- **R1-empty acceptance criterion.** SPEC line 103 adds "An empty admitted set is a hard init failure" as an edge-derived AC — this is correct, but it's listed in the AC block for DATA-01..06 without a clear requirement assignment. It's really a DATA-02/DATA-01 cross-cutting guard.

## 4. Suggestions

1. **Fix the `mem_ballpadck` → `mem_ballpark` typo** before implementation reaches Plan 03-02. It appears in the `must_haves.truths` and action text of task 39-03-02.

2. **Consider a handoff note for Phase 40** documenting that GAP-39-01 (hash producer) is still open and the typed deferral path will fire on every real-corpus adapter init until resolved.

3. **Verify `39-VALIDATION.md` is the single source of truth for the real-corpus command** (as Plan 07 claims at line 100: "that file is the SINGLE source of truth for the exact `GSD_DATA_ROOT`/interpreter/`--run-dir` invocation"). This is a strong design choice — confirm the file exists and the command is correct before Wave 5.

4. **Add a Phase 39 → Phase 40 integration checklist item** for the `StageIndex.from_split(records, manifest, "train")` seam. Plan 07 already exercises it, but Phase 40's training loop is the real consumer and should know this is the documented entry point.

## 5. Overall Risk: **LOW**

The plans are thorough, the dependency ordering is correct, all nine gaps are resolved or deferred, cross-AI review feedback is integrated, and every DATA requirement is covered with specific acceptance criteria and test coverage. The primary residual risk is GAP-39-01 (hash producer still open), which is a deferred operational decision, not a plan defect. The SPEC defect banner annotation and the `s0_sensitivity_sweep` scope expansion are well-justified and self-documenting. No blocking issues.

---

## codex Review

## 1. Summary

The Phase 39 plans are mostly coherent and well sequenced. They cover the main substrate: deferred tests, parser/admission, resident adapter, split manifest logic, batch construction, Stage-0 scan, and real-corpus closeout.

The main risk is in Plan 39-07: the real-corpus closeout depends on train-split Stage-0 evidence, but the plan does not explicitly generate, retain, or hash the real split manifest used for that evidence, and the automated check only confirms the fatal flag exists.

## 2. Strengths

- Clear wave ordering: tests first, then parser/admission, resident adapter, splits, batches, scan, and real-corpus evidence.
- Strong attention to data integrity: fail-closed blacklist handling, typed hash deferral, non-finite quarantine, no corpus mutation, no global RNG/default mutation.
- Good single-source classifier discipline: `stage_label` is shared across adapter, split, batch, and scan plans.
- Strong prohibition coverage around v1 code reuse, framework-spec mutation, footer/metrics misuse, and duplicate on-disk readers.
- Plan 39-07 correctly separates fast regression from the expensive real-corpus gate.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** Plan 39-07 requires `stage0_train_split_count`, but the exact real-corpus validation command only runs `pinn.data.stage_scan`; it does not specify generation/retention of a real `splits.json`. The plan also omits a manifest seed/path/hash from retained evidence. This weakens DATA-04 closure and makes the Phase 40 training seam hard to reproduce.

- **HIGH:** The fatal train-split gate is under-verified. [39-07-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/39-data-ingestion-stage-0-population-scan/39-07-PLAN.md:132) only checks that `phase39_stage0_fatal` is present, not that it equals `true` exactly when `stage0_train_split_count < 240`, nor that train-readiness is refused in that branch.

- **MEDIUM:** Evidence redaction verification is weaker than the acceptance criteria. The plan says retained logs must avoid absolute `/Users/...`, host, and username data, but the grep checks only a narrow `GSD_DATA_ROOT=/Users/` pattern. Other absolute paths or tracebacks could leak into committed evidence.

- **LOW:** Plan 39-02 edits the phase-local `39-SPEC.md` even though the context calls it locked. The edit is narrowly framed as a defect banner, not a requirement rewrite, but it should be treated as provenance-only and mechanically constrained.

## 4. Suggestions

- Add an explicit 39-07 step to create the real-corpus split manifest with a fixed seed, retain it under the phase-close evidence directory, and record its SHA-256/hash, seed, ratios, and byte identity.

- Strengthen the 39-07 verification script to parse `stage0_train_split_count` and assert:
  `phase39_stage0_fatal == (stage0_train_split_count < 240)`.

- Add a positive train-readiness marker only when the train split has at least 240 Stage-0 replay candidates, and assert that marker is absent/false in the fatal branch.

- Broaden evidence redaction checks to reject any retained `/Users/`, local username, hostname, or unredacted interpreter/data-root path.

- For the `39-SPEC.md` banner edit, verify that only banner text was inserted and no locked requirement wording was silently changed.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**HIGH** until the real split-manifest evidence and train-split fatal verification are made explicit.

---

## agy Review

# Phase 39 Plan Review

## 1. Summary
The Phase 39 execution plans (01-07) define a highly rigorous, defensively engineered pipeline for ingesting the dataset into a memory-resident PyTorch adapter. The rollout is meticulously phased: it begins with comprehensive test scaffolding (Wave 0), progresses through pure parsing and admission logic (Wave 1), integrates the in-memory adapter (Wave 2), establishes stage-stratified splitting (Wave 3), and implements batching and population scanning (Wave 4), culminating in a read-only real-corpus validation gate (Wave 5). The plans demonstrate excellent command of memory constraints, edge-case handling, and strict separation of physics from data-fidelity sets.

## 2. Strengths
*   **Defensive Architecture**: The use of a read-only real-corpus validation gate (39-07) ensures that expensive tests don't bleed into normal iteration loops, while the `_require` test scaffolding prevents premature failures.
*   **Robust Edge-Case Handling**: The `T = times[-1]` fix explicitly prevents a `t/None` crash. The handling of missing siblings (Brutus/IC mismatch) quarantines safely without silently dropping or admitting data.
*   **Impeccable Memory Accounting**: Implementing a fallback cross-check (`mem_ballpadck`) in 39-03 to verify `untyped_storage` deduplication ensures the 0.7 memory watermark cannot be bypassed by subtle pointer aliasing bugs.
*   **Fail-Safe Diagnostics**: In 39-06, attaching the fully-built report to the `StageZeroUnderpopulated` exception guarantees that fatal evidence is persisted atomically prior to a nonzero exit (agy N10).

## 3. Concerns
*   **MEDIUM: Acceleration Calculation Overhead (39-05)**: Task 39-05-02 requires calculating "acceleration magnitudes from resident snapshots" for the Gumbel-top-k sampler. Depending on how this is implemented (e.g., finite differences vs. gravitational calculation), it risks introducing significant performance overhead during batch construction if not strictly vectorized.
*   **LOW: Test Discovery Import Errors (39-01)**: Task 39-01-03 specifies using a `_require` helper to skip tests for absent production symbols. If the test modules import missing production files at the top level, `unittest discover` will crash with an `ImportError` before the skip logic can execute. 
*   **LOW: Spec Modification During Execution (39-02)**: Task 39-02-04 edits `39-SPEC.md` to add defect banners. While the rationale is sound, modifying a specification file during the execution phase is generally an anti-pattern.
*   **LOW: Floating-Point Sweep Grids (39-06)**: The `s0_sensitivity_sweep` uses geometric multipliers (`{0.5, 1, 2} * interim_s0`). Floating-point arithmetic on `0.01` could yield minor precision artifacts (e.g., `0.005000000000000001`), which is a slight cosmetic/diagnostic risk.

## 4. Suggestions
*   **Lazy Test Imports**: Explicitly mandate in 39-01 that imports for Phase 39 production modules must be deferred (placed inside the test methods) or wrapped in `try/except` blocks to ensure `unittest discover` functions smoothly across waves.
*   **Vectorize Acceleration**: Ensure the batch constructor in 39-05-02 relies on heavily vectorized NumPy operations to compute the acceleration magnitudes across the `n_snapshots` array, avoiding any Python `for`-loops per trajectory.
*   **Acknowledge Spec Edit**: Treat the `39-SPEC.md` modification as a one-time necessary exception to prevent literal verifier failures, rather than a precedent for altering specs mid-implementation.

## 5. Overall Risk
**LOW**. The execution plans are exceptionally detailed, highly defensive, and rigorously cross-referenced against the specification and threat models.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=325
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=12234
- stderr_bytes=0

### claude-glm
- reviewer=claude-glm
- exit_code=1
- elapsed_seconds=228
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=245
- stderr_bytes=192

### claude-deepseek
- reviewer=claude-deepseek
- exit_code=0
- elapsed_seconds=147
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp deepseek -p - 
- stdout_bytes=7024
- stderr_bytes=192

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=339
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3463
- stderr_bytes=131019

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=79
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=3694
- stderr_bytes=0

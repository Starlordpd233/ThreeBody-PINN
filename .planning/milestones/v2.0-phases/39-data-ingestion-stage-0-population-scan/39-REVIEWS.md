---
phase: 39
reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
rerun_reviewers: [claude, claude-glm, claude-deepseek, codex, agy]
reviewed_at: 2026-07-14T03:27:57Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T032222Z-19760
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 39

## claude Review

I read all seven plans plus 39-SPEC, 39-CONTEXT, the gap register, and the validation map, and checked two claims against the filesystem. Review follows.

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

Seven plans across six waves: a dataset-free test contract (39-01), pure production contracts — parser/preprocessing/classifier/admission (39-02), the `AdmittedSetAdapter` (39-03), the grouped split manifest (39-04), the replay/lookahead batch constructor (39-05), the Thrust-A scan CLI (39-06), and a real-corpus phase-close gate (39-07). Dependency chain is linear except Waves 4 (05 ‖ 06), and the file-ownership partition across those two plans is genuinely disjoint.

This is a third-cycle set: prior review rounds are visibly folded in (`HIGH-1..5`, `claude M1–M6`, `N1–N13`), and the three biggest earlier defects — the memory-ballpark arithmetic, the full-set-vs-train-split fatal operand, and the 1:1 Brutus↔IC folder assumption — are all correctly fixed. Requirements DATA-01..06 trace cleanly to tasks, and every SPEC edge row has a named test.

The remaining problems are concentrated in **the fatal-Stage-0 branch and corpus-root resolution**, i.e. exactly the paths that only execute on the real corpus and therefore cannot be caught by the dataset-free suite.

## 2. Strengths

- **The sole-seam discipline is enforced mechanically, not by convention.** One reader (`pinn/data/adapter.py` + the retained `fixture_loader.py` exception), one stage classifier (`pinn/data/stages.py`), one memory numerator (`resident_tensor_bytes`), each backed by an AST audit rather than a code-review promise.
- **Scientific fail-closed behavior is well specified**: float64 `eps_H` recomputation from raw arrays, the near-zero `H(0)` short-circuit *before* the division (GAP-39-04), no denominator floor, whole-trajectory quarantine on non-finite blocks, and negative tests that footer `dE/E` and metrics JSON never influence the verdict.
- **The `L_norm is None` → `UNASSIGNED` guard** in 39-02-02 is a real catch: without it `None > 0.5` raises `TypeError` on degenerate-`Lmax` records.
- **Determinism is treated as a first-class contract** — canonical JSON, sibling-temp/fsync/replace, Hamilton apportionment with a fixed tie order, per-signature local RNG, byte-identical re-runs.
- **`StageIndex.from_split(adapter, manifest, "train")`** now connects DATA-04's no-leakage manifest to DATA-05's constructor, so the split manifest is no longer a file nobody reads.

## 3. Concerns

### HIGH-A — The worktree *does* contain a partial `simulation_data/Data/`, so the root-resolution guard cannot fire
39-03-PLAN asserts as fact that "the `.worktrees/trainex` worktree case … carries no `simulation_data/Data/`", and builds the typed `DataSourceRootMissing` error on that premise. It is false: this worktree has `simulation_data/Data/` with **74 files (2.7 MB)** — only `ic_standard_quasi_random` and `brutus_standard_quasi_random_gold_standard` — versus **38,017 files** in the main repo. Consequence: the plan permits "`git rev-parse --git-common-dir` **or an equivalent repository-relative resolution**". A naive repo-relative derivation resolves to the *worktree* copy, which **exists**, so `DataSourceRootMissing` never raises, the empty-admitted-set hard-fail never trips (those gold records admit fine), and — because GAP-39-08 grants numeric labels only to base *hierarchical* Set 1a — every record scores `UNASSIGNED`, yielding **Stage-0 = 0, a spurious fatal, and `gold_numeric_stage_count == 0` passing**. Every invariant in the phase reports green while the scan ran on 0.007% of the corpus.

### HIGH-B — The phase-close verify makes the fatal branch unsatisfiable
39-07-03's automated verify greps unconditionally for `^real_stage0_replay=240$`, but `select_stage_records` (39-05-01) *hard-fails* below 240 replay keys. The Stage-1 lookahead assertion is properly guarded behind `has_stage1=true`; the Stage-0 replay assertion has no equivalent guard, even though a sub-240 Stage-0 population is an outcome the phase explicitly contemplates. If the full admitted Stage-0 pool is under 240, the executor can neither produce the line nor pass the gate — and this is not remote: GAP-39-08 confines the numeric pool to base hierarchical Set 1a only.

### HIGH-C — "Fatal" has two contradictory phase-close meanings
39-07's `must_haves` say the gate "refuses to claim train-readiness, and **exits the documented nonzero code**" when `stage0_train_split_count < 240`. Its actual 39-07-03 verify **exits 0** whenever `phase39_stage0_fatal` merely agrees with the count. So a fatal is simultaneously a nonzero-exit failure and a coherent-evidence pass. Nothing states whether Phase 39 *closes* on a fatal, or whether the phase goal ("the trainer serves fixed-shape Stage-0 mini-batches") is then unmet and the phase blocks. An executor has no rule to follow.

### MEDIUM-D — `write_split_manifest`'s signature is unreconciled across Plans 04 and 06
Exactly the defect class `claude M3` fixed for `from_split`, left open one function over. Plan 04 describes `write_split_manifest(..., run_dir, seed, ratios)` as a *serializer* that "returns the typed manifest", with the partition as a separate, unnamed pure function absent from the export list. Plan 06's CLI calls `write_split_manifest(adapter, run_dir=…, seed=…, ratios=…)`, assuming it partitions the admitted set internally. One of the two is wrong, and Plan 06's HIGH-4 sequencing depends on it.

### MEDIUM-E — The validation map's post-check contradicts `claude M5` and skips `splits.json`
39-VALIDATION.md row 39-07-02 is declared the *single source of truth* for both the command and its post-check, and that post-check is `cmp /tmp/phase39-real-scan/stage_population.json …` — i.e. it depends on `/tmp` surviving, which 39-07-02 explicitly forbids ("the verify relies on the retained evidence copies … NOT on `/tmp/phase39-real-scan` surviving"). It also omits any `splits.json` byte-identity check, which HIGH-4 makes load-bearing.

### MEDIUM-F — Collocation points are never asserted to be model-ready
39-05-02's behavior notes that each collocation point "needs an IC13/mass channel", but the acceptance criteria only assert collocation *cardinality, continuity, bounds and independence*. The `(N,14)` / `(N,3)` shape+dtype smoke assertion is scoped to the data-fidelity set. Since the physics residual in Phase 40 feeds collocation through `network.forward(tau_ic13, masses)`, a constructor that emits bare times with no IC13/mass/`T` channel would pass every Phase 39 check and break at the Phase 40 seam.

### MEDIUM-G — `scan.log` has no single owner
Plan 06 says `main` "records its SHA-256 + byte identity in `scan.log`", but `scan.log` appears in neither Plan 06's `files_modified` nor its artifacts; Plan 07 treats it as an executor-assembled capture of stdout plus appended markers. The 39-07-02 verify greps a mix of CLI-authored lines (`mem:`, `mem_ballpark=`, `n_blacklist_entries`) and executor-authored lines (`run_nonce=`, `evidence_byte_identity=true`, `stage0_train_split_count=`) with no statement of which side emits which.

### LOW-H — `DT_OUT_WARN_REL_THRESHOLD = 0.01` may flood the real-corpus log
The warning fires per-trajectory on >1% measured-vs-reference disagreement, with no aggregation or cap. On ~38k records this could bury the disposition summary. Aggregate to a count in the per-folder report.

### LOW-I — Every gap closed under a blanket autonomy delegation
All nine entries read "RESOLVED-WITH-INSTRUCTION … *Under the user's full-autonomy instruction*, choose option A." GAP-39-03 (overriding the phase SPEC's `s_min` predicate with CTL) and GAP-39-08 (which record classes may carry numeric stage labels) are semantic calls, which project governance classes as MUST-surface. The autonomy delegation is on record, but these two deserve an explicit owner acknowledgement line rather than inheriting a blanket one — GAP-39-08 in particular determines the entire Stage-0 population.

### LOW-J — A train pool of exactly 240 yields zero replay diversity
Replay samples 240 *unique* keys without replacement (no padding path, unlike lookahead). At `stage0_train_split_count == 240` every batch is the identical trajectory set. Worth surfacing the margin explicitly in the report, not just the pass/fail.

## 4. Suggestions

1. **Pin corpus-root resolution to `git rev-parse --git-common-dir` only** — delete the "or an equivalent repository-relative resolution" latitude — and add a corpus-shape assertion at init (all four Brutus folders present; found-record count above an explicit floor) that hard-fails, plus log the resolved root and file count. This is what converts HIGH-A from silent to loud.
2. **Guard `real_stage0_replay=240` behind a full-set condition**, symmetric to the `has_stage1` fork: `if stage0_full_split_count >= 240 → real_stage0_replay=240; else → record the shortfall`.
3. **State the phase-close rule for a fatal in one sentence** in 39-07's success criteria: either "a coherent fatal is a valid phase close, Phase 40 is blocked pending owner ratification of `s₀`", or "a fatal blocks phase close". Then make the 39-07-03 verify match.
4. **Quote one canonical `write_split_manifest` signature verbatim in Plans 04 and 06**, the way `from_split` is now handled, and add the partition entry point to Plan 04's `exports`.
5. **Rewrite the 39-VALIDATION.md 39-07-02 post-check** to compare the retained evidence copies against their recorded SHA-256 (and include `splits.json`), removing the `/tmp` dependency.
6. **Add an acceptance criterion to 39-05-02** that collocation emits `(N,14)` `tau_ic13`, `(N,3)` raw masses, and per-point `T`, and that a network smoke call accepts the *collocation* tensors too.

## 5. Overall Risk

**MEDIUM.** The synthetic-path engineering is strong and the earlier review cycles have visibly hardened it; requirement coverage is complete and the invariants are mechanically enforced. The residual risk is concentrated in the paths that only run once, on the real corpus, at phase close — root resolution (HIGH-A), the fatal branch (HIGH-B/C) — where the current design can report a fully green, fully self-consistent phase close over a 74-file partial corpus. Fixing suggestions 1–3 would bring this to LOW.

---

## claude-glm Review

API Error: 529 [1305][该模型当前访问量过大，请您稍后再试][20260714112558a20268bc93dd4bb4]. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (127.0.0.1:4148).

---

## claude-deepseek Review

I now have full coverage of all seven plans, the gap register, SPEC, CONTEXT, and the REQUIREMENTS/ROADMAP scope boundaries. Here is the review:

---

# Phase 39 Plan Review — Data Ingestion & Stage-0 Population Scan

## 1. Summary

Phase 39 delivers six DATA requirements (DATA-01 through DATA-06) across seven plans organized in five waves: Wave 0 (dataset-free test contracts), Wave 1 (production types, parser, admission, classifier), Wave 2 (adapter integration, fp32 residency, memory accounting), Wave 3 (split manifest, StageIndex), Wave 4 parallel (batch constructor + Thrust-A scan/CLI), and Wave 5 (real-corpus evidence gate + audits). The dependency chain is `01 → 02 → 03 → 04 → {05, 06} → 07`. Nine gap-register entries (GAP-39-01 through GAP-39-09) are resolved with proper STOP-protocol compliance, mathematical grounding, and owner-delegated agent judgment. Prior cross-AI review feedback is extensively incorporated (HIGH-1 through HIGH-5, claude M1–M6, N1–N13 markers in the plan text). The plans are thorough and executable.

## 2. Strengths

1. **Gap register rigor.** Nine entries with full STOP-protocol documentation: decision point, source silence citations, mathematical/engineering grounding, agent temptation, user-decision options, and resolution notes. Each gap that required a numeric or semantic default (GAP-39-04 near-zero threshold, GAP-39-05 non-finite salvage, GAP-39-07 memory numerator, GAP-39-09 dt_out warning) labels its chosen value as a reversible implementation default, not source authority.

2. **TDD-first wave structure.** Wave 0 (Plan 01) builds the complete nine-file `tests/phase39/` scaffold with deferred `_require` skips before any production code exists. The `_require` helper emits the exact skip phrase `skipped Phase39 production symbol <module>.<symbol>` consumed by the Wave 5 final grep. This ensures every DATA requirement has a discoverable test module before implementation begins.

3. **Mechanical prohibition enforcement.** AST-based reader audits, write-spy for corpus mutation, global-state checks (Torch/NumPy defaults, RNG, device availability), and v1 import prohibition are specified with exact allowlists (e.g., `ALLOWED_CORPUS_READERS = {pinn/data/adapter.py, pinn/verification/fixture_loader.py}`).

4. **Cross-phase seam documentation.** The DATA-04→DATA-05 seam is explicitly documented: `StageIndex.from_split(adapter, manifest, "train")` is the single canonical signature reconciled across Plans 04, 05, 07, and documented for Phase 40. Plan 05's batch constructor accepts any `StageQuery`, enabling Phase 40 to supply a train-restricted source.

5. **Clear scope discipline.** Phase 40 adaptive collocation, FUT-02 curriculum EDA, s₀ ratification, data-version-hash production, training-loop DataLoader plumbing — all explicitly excluded and deferred. Every plan carries a `prohibitions` block naming what must NOT be introduced.

6. **Memory accounting with cross-check.** GAP-39-07 defines `resident_tensor_bytes` as deduplicated owned fp32 storage. Plan 03 adds a `mem_ballpark` lower-bound cross-check (19 floats/snapshot: 3 bodies × 6 dof + shared time) with a documented misfit band, catching the prior review's ~2.7× undercount. The `mem_ballpadck` typo is explicitly corrected.

7. **Real-corpus gate isolation.** Wave 5 (Plan 07) runs the expensive 6.3 GB corpus scan exactly once, separate from normal test feedback loops. Evidence is committed to the repository with SHA-256 hashes, freshness markers (`run_timestamp` + `run_nonce`), allowlisted exit codes, and path redaction (`$GSD_DATA_ROOT` placeholder, no `/Users/...` in committed files).

8. **Edge coverage.** SPEC edge coverage table resolves 19/19 applicable edges with citations to authoritative sources. Two new edge-derived acceptance criteria (`s_min = s₀` boundary, empty-admitted-set hard failure) are added.

## 3. Concerns

### HIGH

*None identified.* The prior cross-AI review's HIGH concerns (H1: memory ballpark arithmetic ~2.7× off, H2: Stage-0 fatal threshold evaluated on wrong population, H3: IC/Brutus folder 1:1 pairing assumption mass-quarantining gold records) are all addressed: `floats_per_snapshot = 19` with correct decomposition, train-split-restricted fatal verdict via `StageIndex.from_split(adapter, manifest, "train")`, and `(variant, id)` physical-key grouping with variant-based 4→2 Brutus→IC folder mapping.

### MEDIUM

**M1: SPEC "locked at commit" claim conflicts with Plan 02 edit.** `39-CONTEXT.md:12-13` states the SPEC is "locked by `39-SPEC.md` at commit `4fed73f4`; this document does not reopen their what or why." Plan 02 Task 39-02-04 edits `39-SPEC.md` to add defect banners for GAP-39-02, GAP-39-03, and GAP-39-08. The edits are non-destructive annotations (they preserve contradictory text verbatim and add clarifying banners), so they don't change requirements. But the "locked at commit" claim in CONTEXT.md becomes stale — a reader checking the commit hash would find a different file. *Recommendation:* Update CONTEXT.md after Plan 02 executes to note the annotation edits and the new commit reference, or qualify the "locked" claim to apply to requirement text only, not annotations.

**M2: `GSD_DATA_ROOT` git-based fallback is underspecified.** Plan 03 Task 39-03-01 uses `git rev-parse --git-common-dir` as an example for deriving the main-repo `simulation_data/Data/` path. However, `--git-common-dir` returns the `.git` directory path (e.g., `/path/to/repo/.git`), not the repo root (`/path/to/repo`). The plan says "or an equivalent repository-relative derivation" which leaves the exact derivation to the executor. The acceptance test covers failure by asserting a `DataSourceRootMissing` error when the derived path doesn't exist. However, if the derivation is subtly wrong (e.g., resolves to a valid but wrong directory that happens to contain data files), the test won't catch it. *Recommendation:* Pin the derivation to a specific algorithm in Plan 03 (e.g., resolve `$(git rev-parse --show-toplevel)/simulation_data/Data/` from any worktree, which correctly returns the main repo root). `--show-toplevel` is the standard git command for this purpose and is more robust than deriving the root from `--git-common-dir`.

**M3: SPEC defect-banner approach creates latent readability hazard.** The SPEC still carries the reversed `s_min` predicate ("s_min > s₀ for Stage 1, else Stage 0") while the CTL requires the opposite. Plan 02 adds defect banners but deliberately preserves the wrong text. A future maintainer reading the SPEC without consulting the gap register could implement the wrong predicate. The defect banners mitigate this, but only if they remain visibly attached to the defective text. If the SPEC is ever reformatted or the banners are pruned during cleanup, the hazard returns. *Recommendation:* Add a prominent warning at the top of the SPEC (in addition to the inline banners) stating that GAP-39-03 supersedes certain predicate wording and listing the affected line ranges. This makes the hazard discoverable even on a cursory read.

### LOW

**L1: `mem_ballpark` upper bound (3.0×) is very loose.** Plan 03's misfit band uses `resident_tensor_bytes > ballpark_bytes * 3.0` as the upper threshold. Since the real ratio should be close to 1.0× (ballpark excludes per-record IC13/mass overhead, ~16 floats × ~3,400 trajectories), a 3.0× band only catches catastrophic miscounts. The lower bound (`< ballpark * 0.5`) is the load-bearing check since `resident_tensor_bytes` must be ≥ `ballpark_bytes`. *Recommendation:* Tighten the upper bound to 2.0× to catch moderate double-counting while still tolerating per-record overhead. The current 3.0× is safe but less diagnostic.

**L2: Plan 05 collocation global-draw semantics are load-bearing for Phase 40.** Plan 05 Task 39-05-02 specifies collocation as "a SINGLE global pool drawn over the union of all selected trajectories' [0,T] ranges" — exactly 4,096 points regardless of whether the batch has 240 or 256 trajectories. Each point is tagged with its source trajectory for IC₁₃/mass channel resolution. This design means Phase 40 cannot assume a fixed per-trajectory collocation allocation (the point count per trajectory varies). The plan correctly documents this as "load-bearing" and the semantics are explicit. No action needed; noted for Phase 40 awareness.

**L3: Plan 07 verify script depends on exact log line formats.** The `39-07-02` verify block uses an extensive bash script with regex patterns (e.g., `mem: [0-9]+ \([0-9]+\.[0-9]{6}\) watermark=0\.7`). If the adapter's log format deviates from the expected pattern (e.g., different whitespace, additional fields), the verify fails even if the behavior is correct. The tight coupling between log format and verify regex is deliberate (it's the evidence contract), but it means any intentional log format change must also update the verify script. *Recommendation:* Add a comment in Plan 03's `mem:` log emission code citing the verify regex so future editors know the format is contract-locked.

## 4. Suggestions

1. **Use `git rev-parse --show-toplevel` for repo-root derivation (M2).** Replace the `--git-common-dir` example in Plan 03 with `--show-toplevel`, which directly returns the main repo root from any worktree. This eliminates the need to derive the root from the `.git` directory path.

2. **Add a SPEC-top warning banner (M3).** In addition to the inline defect banners in Plan 02 Task 39-02-04, add a prominent warning at the top of `39-SPEC.md` listing all GAP-superseded sections so the hazard is visible on initial read.

3. **Tighten `mem_ballpark` upper bound from 3.0× to 2.0× (L1).** Still generous enough to avoid false positives from per-record overhead, but narrow enough to catch moderate double-counting bugs.

4. **Add cross-reference comments between log emission and verify regex (L3).** In `pinn/data/adapter.py`'s `mem:` log emission, add a comment citing the verify regex in `39-07-PLAN.md` to lock the format contract at both ends.

5. **Consider a Phase 38 regression preflight in Wave 2 or 3.** Currently, `tests/phase38/test_prohibitions.py` is only re-run at Wave 5 (Plan 07). While Phase 39 writes to disjoint directories (`pinn/data/`, `tests/phase39/`), adding a mechanical preflight check at Wave 2 (when `pinn/data/` modules first land) would catch any accidental Phase 38 test contamination earlier. At minimum, `git diff --check` over Phase 38 test files during Wave 2/3 execution.

6. **Update CONTEXT.md after SPEC annotation (M1).** After Plan 02 executes, update the "locked at commit" claim in `39-CONTEXT.md` to note the annotation-only edit and its purpose, keeping the "what and why" lock semantically intact.

## 5. Overall Risk: **LOW**

The plans are comprehensive, internally consistent, and grounded in authoritative sources. All nine gap-register entries are properly resolved. The prior cross-AI review's three HIGH concerns are fully addressed with explicit acceptance criteria and tests. The wave structure correctly sequences dependencies, and Wave 4 parallel execution is safe (disjoint file ownership between Plans 05 and 06). The three MEDIUM concerns are documentation/clarity issues, not correctness risks. The remaining LOW concerns affect diagnostic sensitivity and maintainability, not scientific correctness. The plans achieve the phase goal: a complete DATA-01 through DATA-06 data substrate ready for Phase 40 consumption.

---

## codex Review

## 1. Summary

Phase 39 plans are broadly coherent and likely achieve the stated data-ingestion / Stage-0 scan goal if executed faithfully. No listed file failed to read. No HIGH blockers found; the main risks are final-gate consistency issues around retained evidence and validation-map drift.

## 2. Strengths

- Strong phased dependency structure: tests/contracts first, parser/admission next, residency, split, batches, scan, then real-corpus close.
- Good edge coverage for scientific/data-integrity risks: NaN/Inf quarantine, near-zero `H(0)`, hash mismatch/deferred absence, gold exclusion, strict Stage-0 predicate, train-split readiness.
- Clear scope controls: no framework-spec edits, no corpus mutation, no v1 data-handling import, no Phase 40 training-loop creep.
- Strong final evidence intent: retained logs/reports, freshness markers, exit-code allowlist, redaction, byte identity, reader/classifier audits.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH:** None found.

- **MEDIUM:** [39-07-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/39-data-ingestion-stage-0-population-scan/39-07-PLAN.md:103) says [39-VALIDATION.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/39-data-ingestion-stage-0-population-scan/39-VALIDATION.md:60) is the single source of truth for the real-corpus invocation and post-check, but that row’s post-check is much weaker than the plan’s acceptance criteria. It only compares `stage_population.json` and greps `gold_numeric_stage_count=0`; it does not verify retained `splits.json`, exit-code coherence, freshness markers, redaction, `mem:`/`mem_ballpark`, or train-split count derivation.

- **MEDIUM:** `splits.json` is a must-have retained artifact, but it is missing from the `must_haves.artifacts` list and from task `39-07-02`’s `<files>` ownership list, despite appearing in `files_modified` and acceptance checks. See [39-07-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/39-data-ingestion-stage-0-population-scan/39-07-PLAN.md:27) and [39-07-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/39-data-ingestion-stage-0-population-scan/39-07-PLAN.md:95). This could cause execution/commit tooling to omit the manifest evidence.

- **LOW:** The fixed scratch path `/tmp/phase39-real-scan` is acceptable, but repeat runs could be ambiguous unless the executor enforces exclusive creation or explicit stale-scratch refusal before the scan. The plan says not to overwrite silently, but the validation command itself does not encode that guard.

- **LOW:** Phase 39 consumes the Phase 38 network contract while the roadmap notes Phase 38 plan completion but phase-close held on deferred real-trajectory evidence. This is probably nonblocking, but the Phase 39 execution precondition should state that the Phase 38 interface is frozen enough for DATA-05.

## 4. Suggestions

- Make the `39-VALIDATION.md` row 39-07-02 match the stronger `39-07-PLAN.md` checks, or stop calling the validation row the single source of truth for post-checks.
- Add retained `splits.json` to `39-07` artifacts and task `<files>`.
- Use a nonce/stamped scratch run directory, or require `/tmp/phase39-real-scan` to be absent/empty before execution.
- Add a short Phase 38 interface precondition before Plan 39-05.

## 5. Overall Risk

**MEDIUM**. The plan is technically strong, but final-gate evidence consistency and real-corpus execution details need tightening before execution.

---

## agy Review

_agy failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=agy
- exit_code=1
- elapsed_seconds=2
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=0
- stderr_bytes=164

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T032222Z-19760/xreview-agy-39.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T032222Z-19760/xreview-agy-39.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260714T032222Z-19760/xreview-agy-39.meta

Stderr excerpt:
```
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required

```

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=256
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=10398
- stderr_bytes=0

### claude-glm
- reviewer=claude-glm
- exit_code=1
- elapsed_seconds=217
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=245
- stderr_bytes=192

### claude-deepseek
- reviewer=claude-deepseek
- exit_code=0
- elapsed_seconds=215
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp deepseek -p - 
- stdout_bytes=11498
- stderr_bytes=192

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=335
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3561
- stderr_bytes=330164

### agy
- reviewer=agy
- exit_code=1
- elapsed_seconds=2
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=0
- stderr_bytes=164

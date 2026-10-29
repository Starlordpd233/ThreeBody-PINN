---
gsd_state_version: "1.0"
milestone: v2.5
milestone_name: Root-Cause Confirmation
current_phase: 65
current_phase_name: Probe on the Record & Fit Harness
status: executing
stopped_at: "Completed 65-06-PLAN.md (the registered smoke fit and measured cost)"
last_updated: "2026-10-29T21:50:00Z"
last_activity: 2026-10-29
last_activity_desc: Plan 65-06 executed (Wave 6)
state_head: 3caf4869
progress:
  total_phases: 5
  completed_phases: 0
  total_plans: 6
  completed_plans: 6
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-10-27)

**Core value:** An evidence-backed, pre-registered answer at each milestone to whether the approach learns three-body motion, in physical units, against this charter's bars.
**Current focus:** Phase 65 — Probe on the Record & Fit Harness (all 6 plans executed; phase verification next)

## Current Position

Phase: 65 (Probe on the Record & Fit Harness) — EXECUTING
Plan: 6 of 6 (executed)
Status: Executing Phase 65 (Wave 6 complete; phase verification is next)
Last activity: 2026-10-29 — Plan 65-06 executed (Wave 6)

v2.5 opened 2026-10-27 on the owner's direction to confirm the cause of the
v2.4 time-constant failure before any redesign (the redesign is v2.6), on
branch `milestone/v2.5`, created from `milestone/v2.4` at `dac9d9c1`. Before
it: v2.4 closed 2026-10-26 at Gate G2 (verdict `RETHINK-REPRESENTATION`;
owner decision `change-course`; archived under `milestones/v2.4-*`, local tag
`v2.4`). The Phase 64 verifier and its tests now read
`milestones/v2.4-PROJECT.md` (`dbc96887`), so PROJECT.md could be rewritten
to the charter's C-12 and C-13 drafts. Phase folders 53–60 and 64 stay in
`.planning/phases/`, because code and tests hardcode their paths. The plan
may pivot on test results (owner, 2026-10-27): phases after the first
experiments are provisional, the agent proposes changes, and the owner
decides. The held-out evaluation stays preserved unspent.

**This file is maintained by hand in this checkout.** The `gsd-tools`
mutating verbs have corrupted it before (the full note is in this file at
commit `b8632832`). The v2.5 start was written by hand and its diff reviewed.

Phase 64 record (kept for reference): Phase 64 complete 2026-10-26; planned 2026-10-25 and executed in 7 waves. The verdict is RETHINK-REPRESENTATION; at owner checkpoint ① the owner decided `change-course` (ruling `64-CHECKPOINT-1-RULING.md`, SHA-256 `b0a80c114d1ddc7994c7e02abdd8105f7ae418c776981cf109951bb8f31fac82`), and every charter row C-1 to C-14 was recorded `open`, so PROJECT.md and the twelve skipped-phase requirement statuses are unchanged. FEAS-06, FEAS-10 and VER-22 are complete, and VER-22 was re-verified at close on the final text: 24 defined, 24 in the traceability table, 24 in the roadmap. Phase 60 closed and verified (5/5 success criteria; `60-VERIFICATION.md`); Phases 61–63 skipped at G2.

### Decisions from 65-06 (2026-10-29)

- The registered smoke fit ran once and completed mechanically (registration `ac4358cb` re-pinned by `b1dcacc4`, bytes `ba54e8124a33…`; run evidence commit `84128fe2`, record sha256 `f6faee77d527…`): locked-12 on the Stage-0 training gold record `hierarchical/gold/1632` (split train, manifest stage 0, 1,001 samples, physical [0, 10]), MPS float32, seed 42, **20/20 finite updates (2 warmup + 18 measured) within the 600-second supervised cap**, similarity logged at steps 0/5/10/15/20 through the shared `measure_time_signal`, frozen FEAS-01 score beside the window-mean-constant and two-Kepler comparators on identical times/masses/body order (network E 24.80 tier 0; constant E 1.1538 tier 0; two-Kepler E 0.9168 tier 0; loss 0.0405 as context — no E/tier threshold imposed). Access: exactly one corpus open, zero validation/test opens, clean attestation, 33 pinned digests; marked `inst08-diagnostic` record and weights published exclusively (attempt running → published). `verify-result` printed `VERIFY-RESULT-OK` (exit 0).
- **Measured cost (INST-08e): seconds_per_step 0.014265** — the sum of the 18 measured synchronized update durations (0.25678 s) over 18; warmup 0.13147 s, logging 0.57212 s, scoring 1.21599 s, setup 0.52892 s, data load 0.25356 s and publication 0.01508 s recorded separately; end-to-end 0.13597 s per completed step; sync overhead 0.000120 s over 42 calls. 18 steps is explicitly not steady-state throughput; no other depth/width/rate/device is costed, and no Phase 66–67 experiment is selected. Longer diagnostics refuse at an hour until governed pause/resume/power is proven.
- The guarded bounded fit CLI shipped TDD-first in `diagnostic_fit.py` (RED `f7007b5e` machine-verified `RED_EVIDENCE_OK`, GREEN `59647328`, 131-test gate): `phase65-fit-registration/v1` admission through a new fit-schema branch in the shared `require_committed_registration` (guard edit; probe path unchanged), settings agreement with the sealed registry, sub-hour cap refusal before data access, MPS-availability gate, committed run-commit-faithful logger-parity receipt (D-10), exclusive attempt ownership with explicit incomplete status, supervised-worker cap enforcement, and `check-registration` / `run` / `verify-result`. The smoke's settings and mechanical reading rule were committed before the run (`65-SMOKE-PREDICTION.md` + registration). SUMMARY `3caf4869`; findings `65-FINDINGS.md` (`bdc600fb`).
- The first smoke attempt refused in admission before any claim (nothing created): the receipt check originally demanded bytes at the run commit, but the logger-parity receipt was materialized after the probe run from the run's recorded entry (65-05's provenance). Fixed pre-run (`b1dcacc4`) to verify the receipt against its own introducing commit plus the run commit as ancestor; the registration re-pinned the corrected `diagnostic_fit.py` digest in the same commit; a `receipt_after_run` fixture test pins the 65-05 shape as admitting.
- Owner-only items (preserved, not acted on): the 65-05 probe registration's pinned digests drifted for exactly `diagnostic_fit.py` and `diagnostic_guard.py` (the files this plan was mandated to edit) — one content test fails on those two entries and the amendment/re-commit-vs-historical decision belongs to the owner (the probe's committed result remains verifiable; its `verify-result` exits 0); the 65-05 routed runner defects remain queued; the two bespoke scientific-reporting prohibitions are flagged for review in `65-FINDINGS.md`, not judged by any test. GAP-59-08 stays open and unadjudicated.
- Verification: task-01 gate 131 tests OK; full phase65 discovery 202/203 (the one failure is the owner-routed digest drift); `check-registration` OK with a real ancestor commit; `verify-result` exit 0; `load_protocol()` `PROTOCOL-OK` (33 digests unchanged); `git diff --check` clean at every commit; the held-out evaluation remains unspent. Phase 65's plans are 6/6; the phase verification act flips DIAG-09/INST-08 and closes the phase.

### Decisions from 65-05 (2026-10-29)

- The registered seven-arm reproduction ran once, read-only, under the committed gate (run commit `22cee7d2`, registration `f469e003`): the runner re-checked committed-clean admission before any access, verified every weight SHA-256 before `torch.load`, and read only the seven arms' Stage-0 training orbits through the guarded seam (`hierarchical/gold/1632`, `/4658`, `/851`; split `train`; orbit stage 0; 1,001 samples; window [0, 10]). **Reading-rule verdict: `retained` — all 144 required historical fields reproduced under exact formatter equality, 0 not_reproduced, 0 provenance limitations**, 64 preserved-only fields (moving/spike/skip-siren) reported verbatim, 130 raw per-layer new-measurement entries with range deltas. Zero optimizer steps (interlock), 15/15 parameter digest pairs matched, no test-split open, held-out evaluation unspent, historical scripts never executed. Commits `7a943da5` + `484ea30c` (evidence(65)), SUMMARY `ffb12522`; result page `65-PROBE-RESULT.md`.
- Logger parity (INST-08c): the run's actual `diagnostic_fit.log_similarity` call on r1-1632 polish (same gates, same weights/coordinates, CPU64, no updates) is materialized as `evidence/probe/logger-parity.json` and `verify-result` printed `VERIFY-RESULT-OK` (exit 0) — recomputed reading rule matches, registration bytes unchanged, five code dependencies verified at the run commit, parity entry exactly equal. The plan's named standalone `logger-parity` subcommand does not exist in the shipped runner; the receipt uses the runner's inline parity call in its own test-pinned file shape.
- No SCOPE-49 pivot: the retained branch asks nothing of the owner for the roadmap. The exploratory association stays on record as a reproduction of already-seen results — association only, no causal claim (D-02/D-07); the D-04 reconstruction label and the D-05 labelled gold-finite-difference-in-tau comparator travel with the numbers.
- Routed to the orchestrator/owner (not repaired here; `diagnostic_probe.py` is digest-pinned by the committed registration): (1) the runner's `_render_stdout` crashed with `KeyError: 'measured'` on `preserved_only` verdicts *after* publishing the complete result — `reproduction.stdout.txt` was regenerated from the committed result bytes with the preserved-only branch corrected and a provenance header (no re-run, no retry); (2) `reading_rule.new_measurements` is empty by construction (the 130 entries live at the result's top level); (3) the missing standalone `logger-parity` subcommand and the stdout-rendering suite gap. Any runner edit changes what the probe registration admits — the registration-digest decision belongs to the owner.
- Verification: `verify-result` exit 0; phase65 suite 168 tests OK; `git diff --check` clean; `load_protocol()` revalidated all 33 pinned digests. DIAG-09's acceptance evidence is complete on disk and INST-08(c) is proven; requirement flips stay with the phase verification act (65-06 also declares both IDs and owns the fit work).

### Decisions from 65-04 (2026-10-29)

- The 2026-10-27 exploratory probe is on the record before any rerun (DIAG-09, D-02/D-03): both original scripts preserved byte-exact under `evidence/original/` (SHA-256s `16db5c8c…` / `a4dea7d0…` re-verified; never imported or executed), the complete verbatim text of exactly the two historical numerical tool outputs (`toolu_01PUFNWxrDDsVrU8DTCH4tX3`, `toolu_01NHGWRv6pEQCJmqeAXxqonK`) with timestamps, precision and signed zero, and re-derivable scoped provenance in `source-manifest.json` — including the recovery chain for the scratchpad originals lost to macOS cleanup (restored by the orchestrator from the durable file-history store, snapshots `85ac6b7d6b97691b@v2` / `4f2e7a23e12db4e1@v2`, re-hashed byte-exact). Commits `e71daf0a` (evidence), `b9645d36` (test RED) + `7255835f` (feat GREEN), `f469e003` (evidence(65), the registration), SUMMARY `d2cbc1d3`.
- Reproduction is exact formatter equality with pre-derived rounding cells: every historical token's acceptance region is its formatter-defined cell (first/last representable doubles as float hex, boundary inclusion, excluded `nextafter` neighbours) under the original `.2f`/`.3f`/`.4f`/`.3g` formatters — signed zero, round-half-even ties, exponent changes and `.3g`'s omitted trailing zeros sit inside the cells, and no tolerance is widened after results. The reading rule is immutable after observation: all required fields reproduced keeps the association (`retained`); any failed required comparison withdraws the lead (`withdrawn`, SCOPE-49 proposal to the owner); missing source output is a `provenance_limitation`, never a fabricated failure or success; the single-arm moving/spike/skip-siren columns are `preserved_only`; other arms' individual deep-layer values are `new_measurement` entries with raw values and deltas, never invented targets (D-03/D-07).
- `require_committed_registration` (diagnostic_guard, shared with the fit registration) admits only a committed-clean registration before any data resolution, weight deserialization or attempt creation: git tracked/clean checks scoped to the registration's own enumerated artifacts, exact byte digests, ancestor-commit proof, arms in stable committed-record path order; an unrelated dirty file elsewhere is never a refusal. The read-only runner has exclusive attempt claims, no automatic retry, complete evidence records even when figures fail, `reproduction.stdout.txt` beside `reproduction.json`, hash-before-load weights (`weights_only=True`, CPU), an optimizer interlock refusing construction/steps with counted attempts and parameter digests, and the `check-registration` / `run` / `verify-result` CLI; `verify-result` verifies historical dependencies against the recorded run commit, not current bytes. The CPU float64 seed-42 initialization is labelled a reconstruction, distinct from historical MPS float32 training (D-04).
- Task 65-04-03 committed the registration (`f469e003`: `65-PROBE-PREDICTION.md` + `evidence/probe/expectations.json`, 2975 lines) and the read-only gate proved live admission: `CHECK-REGISTRATION-OK registration-commit=f469e003…` with every artifact hash, zero corpus/weight opens, no probe result or attempt. Verification: task verifies (5, 72 tests) and the full phase65 suite (168 tests) OK at the final HEAD; `git diff --check` clean; `load_protocol()` revalidates all 33 pinned digests; no real probe ran and no corpus was accessed — the seven-arm rerun belongs to 65-05 under this committed gate. Process notes: the plan executed across two executor sessions (prior session committed all four task commits and was interrupted before close-out; the resume re-ran every verify at HEAD and completed SUMMARY/STATE/ROADMAP), and the executor ran under the general-purpose runtime with the gsd-executor role definition. DIAG-09 and INST-08 stay open (later plans own them).

### Decisions from 65-03 (2026-10-29)

- Diagnostic isolation now holds at the actual production entry points (INST-08 d / D-09): `evaluate_run` calls `require_not_diagnostic` after the canonical-frame precondition and the prior-attempt check and before the config/manifest load, the exclusive claim or any adapter construction, translating the typed refusal into its existing public `CheckpointOwnershipError` convention; `train.main` runs the new read-only `require_resume_not_diagnostic` admission (explicit file / directory / literal latest, mirroring `load_resume_target`'s routing over the run's own checkpoints directory) before `run_dir.mkdir`, never constructing a checkpoint store. A marked newest candidate refuses instead of falling through to an older ordinary file; ordinary production resumes keep their exact routing and ordering. Four RED/GREEN commits (`e887ac24`, `14529e8a`, `bcbf762c`, `6449a2ec`), each RED machine-verified `RED_EVIDENCE_OK`; SUMMARY `039d78ab`.
- Payload-level refusals make every return path diagnostic-proof: `DiagnosticCheckpointRefused` (a `NoValidCheckpointError` subclass, so existing callers, Phase 60's `assertRaises(NoValidCheckpointError)` tests and the CLI nonzero convention keep working) is raised on `load_latest` (outside the corrupt-file handler), `fallback_scan`, `load_checkpoint` (marker before the structural test, so CTX-53 key absence cannot supply the refusal) and `load_resume_target`'s returned-payload boundary; `_is_structurally_valid` also refuses marked payloads. checkpoint.py owns the single selection implementation (`fallback_candidates`/`peek_latest_selection`, store methods delegate) and imports the marker predicate from diagnostic_guard at module level; diagnostic_guard reaches the selection seam via a deferred in-function import, so no import cycle exists.
- Verification: the 77-test verify command and the 108-test full phase65 suite pass; regression suites for every touched seam (phase41 checkpoint+resume 78 OK, train entrypoint 26 OK, phase60 refusals + phase57 gate 32 OK, phase43 evaluate 28 OK, phase40 checkpoint + phase41 controllers_ext OK); `load_protocol()` revalidates all 33 pinned digests; `git diff --check` clean; no pinned file touched; no real corpus record opened; no `runs/` tree; the held-out evaluation remains unspent. Negative cases sit beside fully valid provenance with a nonempty test split and a completing ordinary control, so no refusal rides on missing config, empty split or ownership. INST-08 and DIAG-09 stay open (later plans own them).

### Decisions from 65-02 (2026-10-29)

- The guarded Stage-0 data seam landed in `pinn/verification/diagnostic_data.py`: `Stage0TrainingReader`/`require_stage0_training` admit only train-split orbits whose manifest stage (the group signature's `base_stage`; a gold record's own label is `UNASSIGNED` by schema, and both readings are recorded) is 0, before any read, exists or path call; `load_diagnostic_data` validates train/score/beside as a set before the first read, so an invalid ancillary key blocks a valid target with zero opens. The reader stays an `AllowlistedCorpusReader`, so `production_reference` and the preprocessing chain are unchanged and admitted records are bitwise the `load_arm_data` output. Four RED/GREEN commits (`56bac6e6`, `b64f4ba0`, `dadb523b`, `22768976`), each RED machine-verified `RED_EVIDENCE_OK`; SUMMARY `e51ab3cd` (hash correction `13588cd9`).
- `open_diagnostic_context` builds the context from committed metadata only (hash-checked generation-7 manifest, the process open attestation as the independent second test-split check, the Stage-0 reader, the recorded normalizer). `load_recorded_stats` hashes the Phase 59 `reader_acceptance.json` against the committed manifest digest before parsing and requires `stats_digest` == recorded `stats_sha256` == `EXPECTED_STATS_SHA256` (`77526e53…`); zero stds, non-finite entries and substituted subsets halt. Spies prove `open_real_context`, `recover_normalizer_from_checkpoint`, `fallback_normalizer_from_allowlist` and `compute_normalization_stats` are never called — research A3 resolved without the 256-monitor recovery (16 Stage-1 identities are outside this phase's read authority).
- Windows are exact float64 masks `0 <= t <= window_length` (endpoint in, above out, nextafter-pinned), times finite/distinct/strictly increasing, at least two samples; out-of-domain windows (NaN, infinities, non-numbers, an explicit `None`) refuse before any read. Omitting `window_length` keeps the scored horizon (Task-1 call sites unchanged; the full window is bitwise the scored horizon); `tau` uses the locked `T_CHARACTERISTIC_TIME`, never rescaled; the recorded `times_physical`/`tau` come from the exact record grid shared with the score views while `tau_ic13` keeps the resident float32 times for seam parity.
- Process: the plan was interrupted mid-GREEN of Task 2 and resumed by a fresh executor; the partial uncommitted draft was inspected, kept where correct and completed (three implementation defects and three test bugs fixed — the plan's one deviation). Verification: the 52-test verify command and the 83-test full Phase 65 suite pass (33 pinned digests unchanged; `split_allowlist.py`/`learnability_data.py` untouched), `git diff --check` clean, no real corpus record opened, no `runs/` tree. DIAG-09 and INST-08 stay open (later plans own them).

### Decisions from 65-01 (2026-10-29)

- Wave 0 shipped the synthetic fit harness with no corpus access: `pinn/verification/diagnostic_{variants,similarity,fit,guard}.py` and all four `tests/phase65` modules (58 tests, 1.1 s). One tiny fixture orbit traverses named locked-12 variant → two guarded constant-rate Adam steps (OptConfig betas/eps, lr 1e-4) → init+final similarity once each → frozen `score_network` (full `to_json_dict`) → window-mean-constant and two-Kepler comparison rows through the frozen `score_trajectory` → one exclusive `inst08-diagnostic/v1` record plus an intrinsically marked tensor payload. Six RED/GREEN commits (`6c728271`…`b548da0a`), each RED machine-verified `RED_EVIDENCE_OK`; SUMMARY `d6065296`.
- `measure_time_signal` is the one shared centred-neighbour implementation (D-05), transcribed from the preserved originals: feature-wise centring across time samples, cosine of successive centred rows at the torch default epsilon, first-layer frequency `|w[:,0]|·omega_0/π`, output movement as the centered norm ratio, and the labelled network-autograd/gold-finite-difference tau-rate comparator. Hooks ride the actual forward (input layer + each hidden layer) and never survive a raised forward; physical time and normalized tau are recorded separately; non-finite or non-increasing times refuse before any forward, never sort.
- Registry sealed to exactly `locked-12` (12×256, raw [tau, IC13], locked frequencies, lr 1e-4, window [0,10]); `register_variant` extends a copy in registration order, refuses duplicates, and later prediction pages register there without altering the catalog. The locked variant is bitwise the production network at the same seed (CPU float64 `torch.equal`; MPS float32 same-weights case skips only when unavailable, per D-04 — independently initialized cross-runtime nets are never compared).
- The frozen two-Kepler Newton solver does not converge on the synthetic fixture orbit; that `RuntimeError` is caught narrowly around the call and recorded as a non-applicable row (`failure: solver_did_not_converge`, the frozen message verbatim), never a successful score. All 33 `PINNED_MODULES` digests still match the committed protocol `93486d24…`; the scorecard stays `f4b17688…`. Spies prove no `open_real_context`, `run_arm` or `admit_arm` call, and no `runs/phase65` tree exists. DIAG-09 and INST-08 stay open (later plans own them).

### Decisions from Phase 64 (2026-10-26)

- The verdict is `RETHINK-REPRESENTATION`, the frozen rule's output for "G2 fired and the sweep rescued nothing" (`.planning/phases/64-feasibility-verdict/64-VERDICT.md`), and it stays unamended. The page states the time-constant-predictor evidence beside the label, the ladder position (Level 1), the cost on this Mac (22.378 arm hours), the eight unranked candidate fixes for v2.5, and the next milestone, v2.5's trainex-r5 research round.
- The owner's decision at checkpoint ① is V-1 `change-course`, recorded in `.planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md` (SHA-256 `b0a80c114d1ddc7994c7e02abdd8105f7ae418c776981cf109951bb8f31fac82`), and applied by 64-07 as the verdict's `owner_decision`, its sign-off block and the charter's Owner column. v2.5 opens with the trainex-r5 research round (open-book, diagnosis first) and runs no new long training until it explains the time-constant output.
- Every charter row C-1 to C-14 is recorded `open`: the owner's one message addressed no row and did not approve the page. So no spec, amendment or gap register was edited (C-6 and C-7; the `10⁻⁵` bar is neither retained nor replaced and GAP-59-08 stays OPEN), PROJECT.md is byte-identical to the phase base `1ebb1d9b` (C-12 and C-13), and the twelve skipped-phase requirements keep `Pending` with unticked boxes and no label (C-14, GAP-64-01 stays OPEN).
- The requirements marks: FEAS-06, FEAS-10 and VER-22 are ticked with `Complete` status cells, and only those three rows changed in `REQUIREMENTS.md`. VER-22's binding count certifies mapping completeness (no orphans, no duplicates), not that any requirement is satisfied.
- The next steps are not the agent's. `/gsd-complete-milestone`, any merge of `milestone/v2.4` into master, any push, and the GitHub backup are the owner's, or a separate agent's on the owner's instruction. No run is authorized by this phase.

### Decisions from the Phase 64 discussion (2026-10-25)

- The owner discussed all four areas. The decisions are in `64-CONTEXT.md` (D-01 to D-14, `d3fb9816`) and the alternatives in `64-DISCUSSION-LOG.md`.
- Verdict: the frozen output RETHINK-REPRESENTATION is stated exactly, with the time-constant-predictor evidence side by side, and the label is not amended. Design and recipe fixes are listed unranked for trainex-r5. One figure shows system 1632's real orbit beside the prediction, from the committed weights.
- The frozen rule records `representation_limit_qualifier: false` on the G2 path without evaluating it (`pinn/verification/feasibility_scorecard.py:735-752`). The verdict explains that `false` here means "not evaluated on this branch". On the committed numbers the amendment's qualifier condition holds anyway: Rung 1 is Tier 0 on all three systems and has a lower E than the formula only on 4658.
- Cost: measured hours on this Mac plus a labelled for-scale figure, with no GPU figures or routes. The rented-GPU wording in ROADMAP criterion 3, FEAS-06 and FEAS-10 contradicted the owner's standing rule (`PROJECT.md` Constraints, and the trainex-r1 design of 2026-06-10) and was removed in `bb323a52`.
- Charter: the purpose is recorded verbatim (learning plus a proof of concept: "it's just good to see some positive results coming out"). The draft is pre-filled with a recommended answer per item. Stage 0 gets a real bar and Stages 1-6 are open. GAP-59-08 is decided at checkpoint ① beside the pass bars.
- Next milestone: v2.5, committed only to its name and its first phase, the trainex-r5 research round.

### Decisions from the Phase 60 verification (2026-10-23)

- An independent `gsd-verifier` pass wrote `60-VERIFICATION.md` (status passed, 5/5 success criteria, no gaps, `human_verification` empty), judged against the stop-at-G2 contract: the harness is real and tested, the pre-registered rules were followed, the records verify and re-derive, and FEAS-04 and FEAS-09 are recorded as skipped with the exact reason `no rescue`. Nothing that should be absent exists (no r2a, r2b, p1, p2b or c- arm, no rescue.json, no ruling file, no `evidence/continue/`).
- Observation for Phase 64, not a Phase 60 gap. Every trained network is a time-constant predictor: its output varies in time by about 0.3% of the real orbit's variation, and its error equals that of predicting each body's average position (RMS error over the RMS of the orbit about its own mean is 0.9999 to 1.0001; the final training loss is within 4e-4 relative of the mean predictor's). The frozen scorer grades the constant mean predictor Tier 0 with E 1.1538, 1.2337 and 1.1396 on 1632, 851 and 4658, against the trained 1.1574, 1.2375 and 1.1432. That is why E sits in a narrow band and does not move with the first-layer setting. The verifier found no harness defect; the weights moved 5 to 14 times their initial norm. The records cannot say whether this is a representation limit or an outcome of the fixed recipe (Adam at 1e-3 on a cosine, median clipping, 12 layers of 256), because the pre-registered sweep varied only `first_omega_0`. I re-ran the verifier's two scripts and reproduced the figures above. RETHINK-REPRESENTATION is the frozen rule's mechanical label for "G2 fired and no rescue"; Phase 64 should state this observation beside it. The details and table are in `60-VERIFICATION.md`.
- Minor open items, none blocking: `60-VALIDATION.md` is still `status: draft` (Phase 59's was too); the plan and VALIDATION.md say the tests/phase60 discovery takes "under about 60 s" and it takes about 13 minutes; plan 60-22's literal clause `tail -n 1 ... | grep -qx 'EXIT=0'` does not hold because the rescore log ends with an `END=` line after `EXIT=0` (RESCORE-OK and EXIT=0 are both present); the `plan_head_before` in `60-13-SUMMARY.md` is malformed (the verifier read it as `8df69886cb360ff0424eb8b830d4ba3042718a3e`) and was left alone because the verification fingerprint covers the SUMMARY files. The verifier's rescue check has still never run on a real rescue.
- Not run: `/gsd-secure-phase 60` (security enforcement is on; Phases 54 and 55 have a SECURITY.md, Phase 59 had none) and `/gsd-validate-phase 60`. Both are user-invoked follow-ups.
- The generic regression gate was not run as such: it finds no Makefile, pyproject or requirements.txt here and would pass on `true` (memory: execute-phase-wave-gate-vacuous-trainex). The real gate ran in 60-22 and again in the verification: tests/phase60 992 OK, the Phase 59 scorer suites 139 OK, the prohibition suites 35 OK.

### Decisions from 60-22 (2026-10-23)

Wave 22 (60-22) closed Phase 60 on the stop path (Gate G2 fired, no rescue; Phase 64 next). `verify_phase60_evidence.py final` printed PHASE60-EVIDENCE-OK (1.291 s, at `2ca6a821`). `rescore --all` crashed on its first real use, from three defects in the unpinned verifier (the data context used as a context manager, the test-split counter read from the wrong attribute, `.to()` called on NumPy arrays); the orchestrator repaired it in `2ca6a821` with four tests, and the one detached run then printed RESCORE-OK, EXIT=0, in 53 s over all seven arms (committed weights re-scored on the CPU in float64 within 1e-12 and on MPS float32 on tier and counts; nothing retrained). The full `tests/phase60` discovery ran before and after that repair: 989 tests in 789.861 s at `e6ff187d` and 992 tests in 787.906 s at `2ca6a821`, both OK (one by-design platform-probe skip); it takes about 13 minutes, not the under-60-s the plan and `60-VALIDATION.md` state. The nine scorer-dependent Phase 59 suites (139 tests, 29.8 s) and the prohibition suites (35 tests, 1.7 s) passed; the other two Phase 38 tests still fail for their unrelated, pre-existing reason. Phase 59 was not re-run: the diff of its inputs since `4df5d4a8` is empty, so the 60-04 log (PHASE59-EVIDENCE-OK, 604 s) stands. `60-FINDINGS.md` (commit `49940029`, SHA-256 `e13243c611912c57390663c952afd73df42d9ca50b656a4f3011b12f63697450`) reports the seven arms (22.378 machine hours; every arm Tier 0, E 1.1432 to 1.2375), Rung 2 and the probes as skipped with the reason no rescue, and Level 3 as not tested (skipped at G2); it calls nothing a verdict. INST-05, FEAS-03, FEAS-04 and FEAS-09 are marked complete in REQUIREMENTS.md (FEAS-04 and FEAS-09 as recorded skipped). The verifier's rescue check has still never run on a real rescue. NEXT: Phase 64.

### Decisions from 60-19, 60-20 and 60-21 (2026-10-23)

- All three queries printed BRANCH-NOT-TAKEN, re-run by the executor: `branch continue-gate` -> `BRANCH-NOT-TAKEN: continue-gate (no rescue)`; `branch ladder` -> `BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue)` for both 60-20 and 60-21. Nothing was launched, no R_ref was re-measured, no GATE-04 check ran, and the owner was not asked anything. Summaries `24716b7f`, `fb36ee4b` and `0c74ab68`. `verify_phase60_evidence.py g2 --require outcome,skip-records,stop-handoff` printed G2-OK before each.
- The three plans ran in one executor session, a recorded deviation. Each SUMMARY has `status: complete`, `requirements-completed: []`, and `commits` and `plan_head_before` under `actuals`. The 60-19 SUMMARY states "about 16:04 CDT" and "about 6 min"; it was committed at 16:02:57 after a 15:58:19 start (about 4.6 minutes); it was not amended.
- No `60-CHECKPOINT-4-RULING.md`, `evidence/continue/` or r2a, r2b, p1, p2b or c- arm exists.

### Decisions from 60-18 (2026-10-23)

- Wave 18 took the stop branch: `learnability_g2 branch stop` printed `BRANCH-TAKEN: stop (no rescue)`. The skip writer recorded FEAS-04 (Rung 2) and FEAS-09 (the hard-stage probes) as skipped with the exact reason `no rescue`, once: `evidence/g2/skip-records.json`, SHA-256 `e15ad37d95e452637014f18c0eeb5d1795589717b6b82af14691bc3edd580bf8`, commit `9f67d687`. No Rung-2, probe or continue arm has any file.
- The handoff writer wrote `evidence/g2/stop-handoff.json` once, from the committed records: SHA-256 `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5`, commit `8bfa9875`. Its verdict is `RETHINK-REPRESENTATION` (G2 fired and the sweep rescued nothing), computed with no later-rung inputs. Level 3 reads "not tested (skipped at G2)", Phases 61-63 read "skipped at G2, not failed", and the next phase is 64. The verdict is Phase 64's to confirm; Phase 60 only hands over the evidence.
- Machine hours carried into the handoff: 22.38 h across seven arms (r1-1632 2.573, r1-851 2.842, r1-4658 5.693, and the four sweep arms 2.730, 2.903, 3.046 and 2.591). Timed seconds per step ran 0.0109 to 0.0136.
- The verifier's skip-records and stop-handoff checks ran on real artifacts for the first time and printed `G2-OK` in both the required-token and full modes. I had checked beforehand, read-only, that the verdict dict survives a JSON round trip unchanged, since the wave-15 crash was a shape mismatch of this kind. The rescue check has still never run on a real rescue.
- ROADMAP: Phases 61, 62 and 63 read "Skipped at G2 (no rescue), not failed" in the list and the Progress table; their checkboxes stay unticked. STATE: the position names Phase 64 next, once Phase 60 closes. Edits `d54627d8`; summary `4a0dbd9e`.
- NEXT: 60-19 (continue gate), 60-20 (Rung 2) and 60-21 (probes) print BRANCH-NOT-TAKEN, checked read-only after the commits (`branch continue-gate`, `branch ladder`). Then 60-22 closes the phase: the full tests, the evidence check, the re-scoring from committed weights, `60-FINDINGS.md` and the requirement marks.

### Decisions from 60-16 and 60-17 (2026-10-23)

- The owner's go-ahead, verbatim (2026-10-23, about 11:00 CDT): "okay let's run this until phase 60 is closed." It was taken as covering waves 16-22; it names no wave, so each SUMMARY lists it as a deviation. The Mac was on AC power (71%, charging).
- Wave 16 (60-16, the single confirmation run): `learnability_g2 branch confirmation` printed `BRANCH-NOT-TAKEN: confirmation (no sweep setting reached Tier 1)`. Nothing launched. Summary `d2ab99e6`.
- Wave 17 (60-17, owner checkpoint ④): `learnability_g2 branch owner-decision` printed `BRANCH-NOT-TAKEN: owner-decision (no rescue: no sweep setting reached Tier 1)`. The owner was not asked, and no ruling file exists. The go-ahead above is not an answer to checkpoint ④. Summary `6d164a7e`.
- Each SUMMARY has `status: complete` (so the plan index counts the wave done), `requirements-completed: []` (FEAS-03's confirmation and checkpoint ④ were not run, so FEAS-03 is not claimed), and `commits` and `plan_head_before` nested under `actuals`, as in 60-14 and 60-15.
- The other branch queries, read-only: `branch stop` prints `BRANCH-TAKEN: stop (no rescue)`; `branch continue-gate` and `branch ladder` print BRANCH-NOT-TAKEN. So 60-18 runs, and 60-19, 60-20 and 60-21 record branch not taken.

### Decisions from 60-15 (2026-10-23)

- The sweep ran each setting once on system 1632 (g2s-1632-w060, -w120, -w240 and -w480; first_omega_0 60, 120, 240 and 480), seed 42 and MPS float32, in grid order, in one invocation with no pause, stop or resume. It launched at 12:01:51 CDT on 2026-10-22 and ended at 23:18:16 CDT, 11.27 hours in all. The power guard never paused it and exited on its own at 23:28:33. The owner's replies are in the SUMMARY verbatim: "okay let's run that wave 15 now" (taken as "ready", with the 2026-10-21 6 GiB waiver carried over) and "should be done now?" (taken as "finished": the orchestrator had said that asking "done?" starts the check-and-record step).
- All four settings ended at Tier 0, with valid horizon 0.0 at both 1% and 10%. None was extended, and Adam was the better state on each.
  - w060: E 1.1569, 2.730 h.
  - w120: E 1.1561, 2.903 h.
  - w240: E 1.1539, 3.046 h.
  - w480: E 1.1575, 2.591 h.
  - r1-1632 at the locked 30 ended at E 1.1574, so the setting did not move the error. Records and weights: commit `003009a3`.
- `evidence/g2/sweep-curve.json` (SHA-256 `946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc`) records `no_rescue`: all four rows are "below Tier 1", and the confirmation arm and the confirmed setting are null. So there is no confirmation run on system 851 and no rescue, and the plan's stop path follows. It was written once, after the records were committed. Commit `e091916a`; summary `42289790`.
- Verifier fix (Rule 1, `e3841c73`): `verify_phase60_evidence.py g2 --require outcome,sweep-curve` crashed on its first real curve, because the sweep-curve check called `confirmed_omega` without the scorecard and with tuples in place of row mappings. It now mirrors `learnability_g2._build_sweep_curve`. Three regression tests cover no rescue, a mismatch negative control and a Tier-1 case; the 175 tests of `test_verifier_phase60` and `test_g2` pass, and PROTOCOL-OK holds. The verifier is not one of the 33 pinned files, and the protocol does not seal it. Its rescue, skip-records and stop-handoff checks have still not run on real artifacts; 60-18's stop path will be the first to use skip-records and stop-handoff.
- Timing: each arm took 2.59-3.05 hours, against the plan's about 3.75. Each budget is sized to the 3-hour cap by the arm's own timing run, and sustained Adam ran between 1.4% slower and 13.8% faster than that run.
- NEXT, by the plans' branch rules (the `learnability_g2 branch` queries decide): 60-16 (confirmation), 60-17 (owner decision), 60-19 (continue gate), 60-20 (Rung 2) and 60-21 (probes) should each print BRANCH-NOT-TAKEN and commit a "branch not taken" SUMMARY. 60-18 (stop) should print BRANCH-TAKEN with the reason "no rescue", write the skip records and the stop handoff, and mark Phases 61-63 as skipped at G2. 60-22 closes the phase (end-to-end verification, re-scoring from the committed weights, `60-FINDINGS.md`). None of them trains. The owner paces the waves.
- Wave 15 close: `execute:wave:post` ran `verify.schema-drift` and `ui.safety-gate`, and neither blocked. The non-blocking `verify.codebase-drift` advisory again reports 210 pre-existing structural elements since the last codebase map.

### Decisions from 60-14 (2026-10-22)

- Rung 1 ran once on each panel system, seed 42 and MPS float32, in one invocation with no pause, stop or resume. It launched at 21:29:01 CDT on 2026-10-21 and ended at 08:35:40 CDT, 11.11 hours in all. The power guard never paused it and exited on its own at 08:46:04. The owner's replies are in the SUMMARY verbatim: the 6 GiB waiver, "start" (taken as "ready") and "go ahead and check it now" (taken as "finished").
- All three arms ended at Tier 0, on the gold grid and on the base grid beside it. Valid horizon was 0.0 at both 1% and 10%, and no arm counts against the two-Kepler formula. The worst error is the inner pair's in every arm.
  - r1-1632: E 1.1574 (polish), not extended, 2.573 h.
  - r1-851: E 1.2375 (adam), not extended, 2.842 h.
  - r1-4658: E 1.1432 (adam), doubled once (980,623 to 1,961,246 steps) with no gain, 5.693 h.
  - The CPU float64 cross-check agreed on every arm. Records and weights: commit `0a135eca`.
- Gate G2 fired on tiers 0 0 0. By the pinned lap-count rule:
  - sweep system 1632 (10.47 inner laps);
  - confirmation system 851;
  - uncovered system 4658.
  - `evidence/g2/g2-outcome.json` (SHA-256 `3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529`) was written once, after the records were committed. Commit `ee739e64`; summary `b25c4b88`. A G2 fire is a recorded branch, not an owner checkpoint by itself.
- Timing against the plan: polish stopped after about 4.5 s per arm on its five-calls-without-improvement rule, not up to 45 minutes. Sustained Adam ran 5-14% faster than each timing run, so each budget finished under 3 hours. Expect about 2.6 hours per data-only arm on system 1632, plus 2.6 more for each arm that earns its doubling.
- FOR PLAN 60-15 (done; see "Decisions from 60-15" above): Task 1 printed BRANCH-TAKEN and admitted the four sweep arms; the owner was asked again about the 6 GiB figure and gave the go-ahead; the plan's pause and resume steps now use the scripts (`c9f96a38`).
- Wave 14 close: `execute:wave:post` ran `verify.schema-drift` and `ui.safety-gate`, and neither blocked. The non-blocking `verify.codebase-drift` advisory reports 210 structural elements since the last codebase map (pre-existing `configs/`, `runs/` and root files, none from this wave); `/gsd-map-codebase` would refresh it.

### Decisions from 60-13 (2026-10-21)

- `verify_phase60_evidence.py` (new) is the fail-closed evidence verifier, independent of the runner, with `protocol`, `preflight`, `records`, `g2`, `rescore` and `final` subcommands. `tests/phase60/test_verifier_phase60.py` holds its 26 tests. Commit `a264d2e8`.
- The assigned-record preflight checked all ten assigned records (hierarchical 1632, 851 and 4658, gold and base; standard 2279 and 3418, gold and base). Counts were 1,001 within T on gold, 126 on hierarchical base and 59 on standard base, with zero attestation opens. The result is `evidence/preflight/records.json`, SHA-256 `7f4fffe8702da3da8307582310221ccc0d4b1abab1156dd48b2c6103c89892cd`, and `PREFLIGHT-OK`. Commit `fb15e438`.
- The owner's pre-seal answers, verbatim. GAP-60-03: "Keep clipping in data-only arms (delegated default: Adam limits unusually large gradient steps using GradClipper at Stage 0 multiplier 8.5)". GAP-60-09: "No pre-answer: ask me if it happens (stop the phase and prompt for decision if a failed confirmation occurs)".
- The run protocol is sealed: `evidence/run-protocol.json`, SHA-256 `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`, with its plain-language twin `60-RUN-PROTOCOL.md`, written with `--amendment-commit dc3edac0`. The verifier printed `PROTOCOL-OK`, and the dry run admitted all three Rung-1 arms. Commit `52d98211`; summary `7293ef2a`.
- After 60-13 (2026-10-21): `scripts/phase60_run_control.py` and its wrappers `phase60-pause.sh`, `phase60-resume.sh` and `phase60-power-guard.sh` add a governed pause, a pre-checked resume and a battery / 09:00 power guard for Phase 60 runs (commit `91f53e58`). Plan 60-14 points its pause and resume steps at them (commit `768ade36`). Plans 60-15, 60-16, 60-20 and 60-21 still describe a launcher-direct `--resume`; use `scripts/phase60-resume.sh` there the same way.

### Decisions from 60-12 (2026-10-20)

- `learnability_run.py` (SPEC Requirement 8, SCOPE-44) now carries the real-arm command line and exact resume. `python -B -m pinn.verification.learnability_run <arm-id> [--resume | --admit-only]` parses only a catalog arm id and the two mutually exclusive flags (any runtime, precision, seed or path argument is a usage refusal), calls `admit_arm` before anything else and prints `ADMIT-OK` / `ADMIT-REFUSED: <reason>` (exit 2), and `--admit-only` returns there without opening the corpus or creating a run tree. A run writes `runs/phase60/<arm-id>/process.json` with its own PID before `run_arm`, takes the Phase 60 one-launch lock with `begin_long_step("phase60", arm_id, ...)`, releases it in a `finally` on every path, and installs SIGHUP, SIGINT and SIGTERM handlers (`pinn/training/signals.py` is not edited). One top-level handler maps `OwnerRouted` and `CrossCheckDisagreement` to `OWNER-ROUTED: <message>` with exit 3 exactly once and `GovernedStop` to 129, 130 or 143; the codes are 0 ok, 2 refused, 3 owner-routed, 129, 130, 143. Commit `2da19abe`; summary `911beebd`.
- Exact resume. `request_stop(signum)` only sets a flag and a code, and `run_arm` checkpoints at an Adam step boundary (through a `stop_fn` the budget driver consults), at the Adam-to-polish boundary and between polish outer calls, where the closure raises `_StopRequested(BaseException)` so a long outer call aborts at its next evaluation and the parameters plus the pre-call L-BFGS `state_dict` are restored. The `phase60-resume/v1` checkpoint in `resume.pt` holds the model, Adam, the scheduler and its cosine index, `ScheduledWeights`, `GradClipper`, the four RNG streams from `determinism.capture_rng_state`, the readings, trace and monitor log, B, the extension flag, the summed Adam and polish wall seconds, the timing record, the frozen monitor rows, the frozen handoff segment, the L-BFGS state during the polish, the polish counters, the Adam state's scores, and the protocol SHA-256 with the pinned module digests. A resume restores every component after the objects are rebuilt, continues the budget driver from its saved step and readings (so the extension decision at B is made once by the frozen function), never re-runs the timing run unless the stop came during it (the record then says `timing_runs` 2), never re-times B, and adds each segment's time. `stop-<n>.json` is written with `write_record_exclusive` per stop and the record's `launch {invocations, stops}` block carries the exit history. Both `torch.load` calls pass the literal `weights_only=True`.
- The refusals. `ResumeRefused` covers a missing checkpoint or stop marker, another arm id, a changed protocol SHA-256, a changed pinned module digest, an unknown phase and a polish checkpoint without its segment state, in the trainer's words ("resume checkpoint is missing active L-BFGS segment state; refusing to redraw samples or causal weights", mirroring `controllers.py` lines 845-850 and 2213-2218). `ClaimExists` refuses a fresh start over an owned run tree, and a polish checkpoint without its L-BFGS state or a checkpoint at another `first_omega_0` is refused as well. `tests/phase60/test_resume.py` (25 tests) proves exact continuation in Adam, at the extension boundary and in the polish, the same collocation draws on a physics arm, the refusals, a repeated timing run and real SIGHUP/SIGINT/SIGTERM/SIGKILL in a child process; `tests/phase60/test_cli.py` (24 tests) proves the argv surface, admit-only, the lock and `process.json` and the exit mapping.
- Wave 12 gate: 25 tests (Task 1 verify), 960 tests (the full Phase 60 discovery, run once at the final code, one by-design platform-probe skip), 43 tests (signals plus the phase38/39 prohibition suite), and the real `python -B -m pinn.verification.learnability_run r1-1632 --admit-only` exits 2 with one `ADMIT-REFUSED:` line and creates nothing under `runs/`. No real arm record, no `runs/phase60` directory and no protocol or preflight was written. The full discovery was run once at the final code and its complete log is retained.
- DEVIATIONS (the SUMMARY lists them): one Rule 3 rewrite of `test_budget_driver`'s owner-stop handler test, because `main` adds the one handler that must not re-raise; one code commit for both tasks as the plan prescribes, so the RED evidence for Task 2 is retained from a log instead of committed; the Sonnet 5.5 co-author trailer instead of the Opus 5.5 the plan text names.
- OPEN for the owner or verifier (60-12 coverage item D11): the per-evidence-root default run tree (the command line passes the canonical `runs/phase60/<arm-id>`), the first-signal-wins rule, the Adam-to-polish boundary checkpoint, `ClaimExists`, `timing_run` returning `None` when stopped, the two extra refusals, the nullable memory field and the data-only arm's unused generator. Each fails closed and moves no locked value, but together they fix the shapes Plan 60-13 seals into the protocol.
- FOR PLAN 60-13: `learnability_run.py` is final for this phase at SHA-256 `a031b9373db7dbd7a15429f7e699fb1743b7f33f2563b6f01ac3166a63bf711c` (the pre-plan file was `dad7e218...0a55`). `PINNED_MODULES` pins it, so any later edit is drift and the protocol is written after every such edit.

### Decisions from 60-11 (2026-10-20)

- `learnability_run.py` (SPEC Requirements 3-5 and 7, D-01, D-05, D-06, D-08, D-10, GAP-60-05, GAP-60-07, GAP-60-10, GAP-60-12) now runs arms with a physics term. `run_arm` builds the arm's own `np.random.default_rng(SEED)` after the timing run (the timing run keeps its own throwaway generator), draws the frozen monitor set before step 1, then draws a fresh 16-bin, 4,096-row stratified collocation set every Adam step and calls the trainer's memory-bounded `physics_adam_step` with `ScheduledWeights.current(step)` and the PHYS-05 warmup of the arm's own budget. `physics_ic` passes `data_points=None`, so Rung 2a never evaluates a data term. `frozen_monitor_log` runs only at the budget readings (D-06) and the runner never names `front_idx`. At the handoff `scheduled.freeze()` / `current(0)`, one row set, one pass-1 evaluation and the frozen `LossWeights` feed `physics_polish_objective` for the whole polish; a recorder test proves the polish redraws nothing. The record gains `r_ref` (with the ratified "Stage-0 reference in force, applied unchanged" note), `scorer_context_r_ref`, `s_h` for the probe Rung-2b arms, `schedule.warmup_steps`, `monitor_log`, `handoff` and the D-05 readout note. Commit `b5f47fac`; summary `a60fff5d`.
- Both scored states are re-scored on the CPU in float64 (GAP-60-07): the saved weights move to the CPU and then widen, the same float32-rounded IC13 is fed back, and `score_network` runs at float64 on the CPU. A tier or counts difference writes `owner-stop.json` (stage `cross_check`, both scores and both counts) and raises `CrossCheckDisagreement`; a spy shows `better_state` is never called, so the better of the two scores is never taken. Counted arms call the frozen `counts` against the committed Phase 59 two-Kepler rows (recorded with the file's SHA-256); a missing formula goes through the one module-level owner-routed clause, which writes `owner-stop.json` (stage `counts`) and re-raises the same exception object; a probe calls `counts` zero times and records `not applicable: no hierarchical split`.
- The real-arm record is now a contract: `REQUIRED_REAL_FIELDS` lists 54 dotted paths and each one is proven by removal; `validate_record` also checks the literals (seed 42, MPS float32, schema, diagnostic, `run_kind`, the weights file names, zero attestation counters, tier 0..3, both horizons, non-finite values only as the JSON sentinels) and the continue-arm ruling block; `build_real_record` fills versions, code, `config_sha256`, the four protocol digests, the attestation, the normalizer digest and `wall.hours` from the admission, the protocol and the context. `run_arm` writes nothing it has not validated (SPEC Requirements 4 and 5, D-10).
- Two existing tests were rewritten in place because this plan supersedes their premises: `test_run_short`'s "only the data-only loss arm is trained here" now pins the new `fixture_r_ref` gate, and `test_budget_driver`'s "only handler" test now pins that every owner-routed handler ends in a bare raise. A fixture arm with a physics term must pass `fixture_r_ref` explicitly (the plan says fixtures pass r_ref but names no keyword); a real arm without an admission keeps the Plan 60-08 record shape, while the admitted path (the one Plan 60-12 launches) is the strict, validated one.
- Wave 11 gate: 21 tests (the tracer gate, re-run on the committed tree), 41 tests (cross-check and static guards), 911 tests (the full Phase 60 discovery, run once at the final code, one by-design platform-probe skip) and 35 prohibition tests all pass. No real arm record, no `runs/phase60` directory, no protocol and no preflight was written; the governed `r_ref_stage0.json` (`c3a14924...`) and the frozen scorecard (`f4b17688...`) are unchanged; the evidence directory still holds exactly `launch_phase60_arm.py` and `scorer-successor.json`.
- OPEN for the owner or verifier (60-11 coverage items D9 and D10): the unadmitted real-arm record shape, the `fixture_r_ref` keyword, the probe formula keyed on the rung, the inert `epsilon_H` where the stage's energy weight is zero, the five `counts` calls for a counted two-state arm, `module_sha256` as the protocol's pin mapping, and the two rewritten test files.

### Decisions from 60-10 (2026-10-20)

- `learnability_protocol.py` (new, SPEC Requirements 4 and 8, D-08, D-11, GAP-60-03 to GAP-60-13) holds three things and a command line. `build_protocol`, `write_protocol` and `load_protocol` produce and re-check the run protocol (`phase60-run-protocol/v1`): every value comes from the code's own constants, the frozen scorecard or committed Phase 59 and Phase 60 evidence, and the SHA-256 of each of the 33 `PINNED_MODULES` entries is recorded so `load_protocol` raises `ProtocolDrift` naming any changed file. `write_preflight` checks all ten assigned records (`phase60-preflight/v1`) with no substitute for a missing, empty, unreadable or wrongly counted record. `admit_arm` is the check every real arm passes before it starts. The module never imports `learnability_run` (the runner imports it). Commits `108ca2e8` and `304742bf` (tracer, test-first), `763fc8c8`, `2d78ab9d` and `af81ac24` (preflight and admission, test-first, then a hardening pass), `51cfb094` and `83974900` (summary).
- Nothing real was written. No `run-protocol.json`, `60-RUN-PROTOCOL.md`, `preflight/records.json` or arm record exists; the evidence directory still holds exactly `launch_phase60_arm.py` and `scorer-successor.json`, and `runs/phase60` does not exist. Guardrails verified independently by the orchestrator: `r_ref_stage0.json` is still SHA-256 `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`, the scorecard JSON is still `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`, the only `terminal-state.json` is the existing Phase 57 file, `git diff --name-only 31467d7e HEAD` lists only the three owned files and the SUMMARY, and `git diff --check` is clean. The executor's one read-only smoke of `write_preflight` against the real corpus (writer replaced by a capture) found all ten keys ok with counts 126, 1,001 and 59 and zero test-split opens.
- Literals checked by the orchestrator: `EXPECTED_S_H` 22.321729071058996 and `EXPECTED_EPS_H` 0.0022321729071058997 equal the values in the tracked `runs/stage0-v23g7-seed42/training_metadata.json`; the within-T counts 1,001, 126 and 59 are the plan's (60-RESEARCH Finding G).
- Wave 10 gate, re-run by the orchestrator: the contract verify command (schedule, budget driver, re-measure, protocol and admission suites) ran 263 tests, OK, in 519 s. The executor's retained full `tests/phase60` discovery (842 tests, OK, 1 by-design platform-probe skip, 876 s of tests, run once at the final code `af81ac24`; later commits changed only the SUMMARY) is reused, not rerun. The executor's 80 single-line mutations of the module were read from its retained logs: 29 of 29 and 51 of 51 caught on the final code.
- DEVIATIONS (the SUMMARY lists them): five code commits instead of the plan's one (test-first); the Sonnet 5.5 co-author trailer instead of the Opus 5.5 the plan text names; the `af81ac24` body says "seven uncaught" where the exact figure is eight (not amended, no history rewrite); two checks that could never trigger were removed; Rule 2 hardening (`load_protocol` also checks the recorded source digests, and `write` requires an existing preflight and an amendment commit that is an ancestor of HEAD).
- OPEN for the owner or verifier (60-10's coverage item D8; the protocol is sealed in Plan 60-13): (1) a window count other than 1,001, 126 or 59 blocks the arm, although SPEC Requirement 8 names only missing, empty and unreadable records; (3) `load_protocol` also compares the recorded digests of the Phase 59 panels, picks and two-Kepler files, the Stage-0 metadata and the scorer successor record; (6) the data-only Rung 1 arm on the uncovered system waits for the re-measure, because the ladder is taken only after a passed re-measure. The other five readings (one exception type for every unusable protocol; extra protocol sections; admission result extras; extra command-line tokens; `write_protocol` refusing with `HarnessHalt` after a result) are listed in the SUMMARY.
- FOR PLANS 60-11, 60-12 AND 60-13: `PINNED_MODULES` includes `learnability_run.py` and `learnability_protocol.py`, which Plans 60-11 and 60-12 still edit. Any edit to a pinned file after the real protocol is written is drift, so Plan 60-13 writes the protocol only after every such edit. `admit_arm(arm_id, repo_root=None, evidence_root=None, resume=False)` returns what the arm must cite and creates nothing, so `--admit-only` can call it before touching `runs/`.

### Decisions from 60-09 (2026-10-20)

- `gate04_train_free.py` gained an optional keyword `first_omega_0=None` on `_measure_raw_bin_means`, `compute_r_ref`, `evaluate_case` and `run_gate`. `None` keeps the original `build_network(ArchitectureSpec(seed=case.seed), ...)` call with the same arguments; a value builds the network through `diagnostic_architecture.build_network_with_first_omega`, and `ArchitectureSpec` stays omega-locked. The orchestrator read `git diff f1238d9e -- gate04_train_free.py`: it is one import, the four signatures, the threading and the construction branch, and nothing else.
- `gate04_omega_remeasure.py` (new, D-07) loads the committed D-11 ruling, refuses unless the answer is continue and the approved value is finite and positive, runs the GATE-04 re-measure at that value, and writes only under the Phase 60 evidence root: `continue/gate04-remeasure.json` (schema `phase60-gate04-remeasure/v1`), and on a complete PASS `continue/r-ref-approved.json`. A BLOCK prints `GATE04-BLOCK` and exits 5 so the continue path stops for the owner; a refusal exits 2. It never calls the GATE-04 CLI `main` and never writes `terminal-state.json`. Commits `da946364` and `c9b3f597` (tracer, test-first), `7f7088b5` and `b4fd949c` (command line and second-run refusal, test-first), `56c3dcba` (summary).
- The real six-case re-measure was NOT run; it runs only on the owner's continue path (Plan 60-19). Guardrails verified independently by the orchestrator after the executor: the governed `r_ref_stage0.json` still has SHA-256 `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff` (git blob `f78084543dbb4e42d6c56bc7922782cf8f61a8af`, unchanged since the plan's reference commit `0d0ec297`), the only `terminal-state.json` is the existing Phase 57 file, and no `evidence/continue/` directory exists.
- Wave 9 gate, re-run by the orchestrator: 123 tests (the re-measure, Phase 57 gate and evaluation, Phase 60 static guards, Phase 38/39 prohibitions) pass in 43 s. The executor's retained full `tests/phase60` discovery (698 tests, OK, 1 by-design platform-probe skip, 332 s, run after the last code change) is reused, not rerun; the broadest check runs once after wave 10.
- DEVIATIONS (two Rule 2 fail-closed input checks, the SUMMARY lists them): a missing or uncommitted sweep curve is refused before any measurement, because `equals_confirmed` needs the committed confirmed value; and a second run refuses before measuring if any of the three outputs already exists, not only the record. Also: a gate PASS over a case set other than the six defaults is recorded as BLOCK with an added reason, because the record schema pairs PASS with `complete_pass` true; the plan's baseline commit `0d0ec297` is cited but the governed artifact was verified against the starting HEAD `f1238d9e` and is byte-identical to both.
- OPEN for the owner or verifier (60-09's coverage item D7): the three choices the plan and the gap register leave open, namely the missing-sweep-curve refusal, the non-canonical-case-set PASS recorded as BLOCK, and the stop-on-any-existing-output rule. Each fails closed and none changes a frozen value, schema field, threshold or default.

### Decisions from 60-08 (2026-10-20)

- `learnability_run.py` now gives real arms the frozen budget rule. A timing run of the arm's exact configuration sets B through the frozen `steps_budget` (3-hour cap); Adam runs the ratified schedule over exactly B (D-01, D-04, D-05: `OptConfig().lr_for_stage(k)` with no literal rate, cosine to zero over B, `lambda_ic` = `PHYS05_LAMBDA_IC_ADVISORY` = 1.0); readings follow the frozen cadence; `drive_adam` branches only on the frozen `budget_outcome` and on divergence (its only numeric constants are 0.0 and 1, checked by AST). At most one extension runs as a second cosine on the same optimizer (D-03: every group's lr reset to `initial_lr`, moments kept, no re-ramp of the physics weights). Every Adam step goes through the trainer's `GradClipper` before `optimizer.step()` (GAP-60-03); a non-finite loss, clip outcome or gradient skips the step and ends Adam at the last finite state with no restart (GAP-60-06); the one `except OwnerRouted` in the file writes `adam.weights` and `owner-stop.json` and re-raises. Commits `37a76a90` (tracer), `9b18d8da` and `c1909e77` (schedule, test-first), `ad15d86b` and `2c23f4b9` (guards, test-first), `4ac6b558` and `b914dc75` (summary).
- Wave 8 gate, re-run by the orchestrator: 229 tests across the schedule, budget-driver, run-short, Phase 38/39 prohibition and Phase 59 scorer suites pass in 56 s. The executor's retained full `tests/phase60` discovery (657 tests, OK, 1 by-design platform-probe skip, 256 s) is reused, not rerun; the broadest check runs once after wave 10. No real arm was started.
- DEVIATIONS (the SUMMARY lists them): a gradient-finiteness check when clipping is off (Rule 2); extra keywords `fixture_timing_steps`, `enforce_cadence`, and `data` and `clock` on `timing_run`; seven commits instead of the single commit the plan names (test-first flow); the Sonnet 5.5 co-author trailer instead of the Opus 5.5 the plan text names.
- PLAN-TEXT MISMATCH: Task 3 says an all-non-finite reference window gives `OwnerRouted`. The frozen `budget_outcome` (`feasibility_scorecard.py` 814-839) returns "extend" for that case when the run is not yet extended and raises `OwnerRouted` only once extended, when the reference minimum is not finite or exactly 0.0. The tests cover the reachable form against the real frozen function and the same-object propagation.
- OPEN for the owner or verifier (60-08's coverage items D10 and D11): D10, Adam weights that are not finite after the driver returns (unreachable by construction, since a non-finite step is skipped) stop the arm with `HarnessHalt` and write nothing, because no source says what result such an arm has and the scorer refuses non-finite networks; D11, a "clipped" step is a pre-clip norm strictly above that step's clip value and a fixture arm's timing run defaults to the frozen 50-step minimum (neither can change training, only the audit field). Real-arm `formula`, counting and the complete record stay with Plan 60-11, and the real-arm CLI and resume with Plan 60-12.

### Decisions from 60-07 (2026-10-20)

- `evidence/launch_phase60_arm.py` is the detached, one-at-a-time sequence launcher. It resolves a sequence only through `learnability_arms.SEQUENCES`, starts a supervisor that detaches from the terminal and the agent session, runs the arms under `caffeinate`, writes `exit.json` for every arm, and allows a resume only after a governed stop. Commits `ba8d30f6` (tracer), `e1f64139` (launcher), `ffbda06b` (summary). Wave 7 gate: 578 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests pass, with the one by-design platform-probe skip.
- No real arm was started. Every test used a stub under a temporary directory and patched `caffeinate`; the real `--sequence rung1 --status` printed `SEQUENCE-NOT-LAUNCHED` and created nothing; no `runs/` directory exists, and no launcher or runner process was left running after the executor or the gate. 81 injected faults were run; 80 are caught and 1 is equivalent (the membership check in `resume_arm_ids` refuses the same input).
- DEVIATIONS (the SUMMARY lists two process notes): two task commits instead of the single commit Task 2's action names, and the Sonnet 5.5 co-author trailer instead of the Opus 5.5 the plan text names. Also disclosed under its readings: `start(invocation_dir, argvs, *, cwd, identity)` keeps the plan's signature but requires `identity["arm_ids"]` (one id per command) because the signature has no other channel, so a call without that key is refused; `status`, `main`, `resume_argvs` and `launch` gained optional keyword-only test seams, and `status` also returns the lines it prints. Calls written to the plan's signatures still work, apart from the `arm_ids` requirement.
- OPEN for the owner or verifier before the first real arm (60-07's coverage item D9): readings of the plan text that fix the launcher's refusal and output shapes that Plans 60-12 to 60-22 read. Each fails closed. The chief ones: any death by a signal refuses the resume, even SIGTERM, because the runner's handler never ran and no checkpoint exists; a supervisor that is gone with no `exit.json` makes `--status` and the resume gate exit 1 with "owner decides" rather than report RUNNING; `--dry-run` runs without caffeinate, probes every arm and needs exit 0 as well as an `ADMIT-OK` line, which is stricter than the plan's wording. Others: the gate checks `exit.json` only and leaves checkpoint validity to Plan 60-12; extra refusals for ids outside the catalog, a stopped arm not in the sequence, a gap in invocation numbers and an unreadable record. Two limits: liveness is `kill(pid, 0)`, which cannot detect a reused PID, and the launcher does not itself stop two sequences running at once (the runner's lock in Plan 60-12 does). The full list is in `60-07-SUMMARY.md` under Readings of the plan text.

### Decisions from 60-06 (2026-10-20)

- `learnability_g2.py` and `learnability_ruling.py` hold the rules that decide what runs after Rung 1, as pure functions with small fail-closed writers. Gate G2 calls the frozen `g2_fires` and the sweep and verdict rules call the frozen scorecard functions; none is re-implemented. The ruling loaders accept a file only when it is tracked and clean, holds exactly one machine block and one opaque owner quote, and cites a SHA-256. No ruling text was written, paraphrased or fabricated; the test rulings are synthetic and live in temporary directories. The six-name branch query (`sweep`, `confirmation`, `owner-decision`, `stop`, `continue-gate`, `ladder`) answers TAKEN, NOT-TAKEN or PENDING from committed records and recomputes from the underlying arm records. Commits `f3780d6d`, `ba4df889`, `be5ed70f` (one per task) and `ff042094` (summary). Wave 6 gate: 488 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests pass, with the one by-design platform-probe skip.
- 144 one-at-a-time mutants were run against the new modules; 141 are caught and 3 are equivalent (another check refuses the same input). Eleven test gaps the first batches exposed were closed before the commits. The work was interrupted once by a session limit and resumed from the saved state; the resume re-checked that all four owned files still matched the hashes in the retained verify log.
- DEVIATION (not listed under the SUMMARY's "Deviations", which says none; it is recorded there under its decisions): the plan shows `repo_root` as a required keyword for `branch_state`, `write_skip_records` and `stop_handoff`. The code gives `repo_root` and `scorecard` a default everywhere (`repo_root` defaults to the git top level above the evidence root). Every call written to the plan's signature still works; the change only adds callable forms.
- OPEN for the owner or verifier before the first real arm (60-06's coverage item D8, not to be confused with 60-23's D8): readings of the plan text that the sources leave open. Each fails closed and moves no locked value, but together they fix record and refusal shapes that Plans 60-09, 60-10, 60-13 and 60-14 to 60-22 read, so they need confirming or a gap entry first. They are: a go-to-verdict ruling that also names `approved_first_omega_0` is refused; a non-null protocol pre-answer is final and the GAP-60-09 file is then ignored; a confirmed rescue always goes to checkpoint 4 and so needs the committed run protocol; `branch_state` recomputes from arm records, so later fixtures need committed arm records; a missing deciding file exits 4, an uncommitted one is PENDING in a query and exit 2 in a writer; `owner-decision` and `confirmation` stay TAKEN once taken; skip and ladder interplay, including a skip with the wrong reason on a stop path halting; `stop-handoff` refuses once a ladder arm has started and requires `wall.hours`; the JSON field names and writer command-line tokens beyond those the plan names; `R_REF_APPROVED_REL` is exported but only the shape of `r_ref_artifact` is checked, since Plan 60-09 owns that file; and the ruling-parser fence and key-line rules. The full list is in `60-06-SUMMARY.md` under Decisions Made.
- Three commits (one per task) replace the single commit the Task 3 action names, because `learnability_g2.py` now imports `learnability_ruling` and a split would leave a commit that cannot import.
- FIXTURE RACE found at the chain closeout and fixed (commit `08ea9a2a`, summary note `c363fad6`): the contract's four-module verify command failed once, intermittently, with `shutil.copytree` raising ENOENT on 18 entries under `.git/objects` of a cached template repository in `test_g2.py`. Every `git commit` starts a detached `git maintenance run --auto`, which can run `git repack -d` and delete loose objects mid-copy (a traced run spawned 310 maintenance processes and 2 repacks; after the fix, none). The fixture now sets `maintenance.auto` false and `gc.auto` 0, and `FixtureRepoTests` pins both. The same command passed on an immediate rerun and on the fixed bytes: `tests/phase60` discovery 579 tests, the four-module command 358 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests. The single failure was not reproduced on demand, so the mechanism is established but that one occurrence is not proven to be this one. Other fixtures that copy a live git repository (the shared Phase 59 `init_repo` helper does not disable maintenance) have the same exposure and were not audited.

### Decisions from 60-05 (2026-10-19)

- `learnability_losses.py` composes the harness physics step from the production trainer's own functions, in the trainer's order (pass 1 freezes the causal weights, `(data + IC)` backward, then the pass-2 chunk loop). One harness step equals `RunController._run_adam_step_microbatched` on `data`, `ic`, `phys`, `energy`, `angmom`, `total` and on all 28 parameter gradients (rtol 1e-10, atol 1e-12; the difference is 0.0) for the Stage-0 weights and for `lambda_e = lambda_l = 1`. Twelve trainer objects are identical to the trainer's, and patching any of eight named trainer functions (plus `compose_total`) moves the harness output. Every evaluation path stays at 256 rows or fewer; the frozen monitor logs and never halts; the polish objective uses only the frozen rows, causal weights and loss weights. Commits `4fc9f60f`, `042ed09d`, `1e9a948a`.
- The committed oracle uses 400 collocation rows (chunks of 256 and 144), not 4,096, because one production-shape step takes about 29 s on this CPU and would use most of the plan's 30 s module budget. A one-off production-shape run (4,096 rows in 16 chunks, both weight cases) was also exact; it is not a committed test. 25 injected faults were all caught (6 in the oracle, 19 elsewhere). Wave 5 gate: 285 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests pass, with the one by-design platform-probe skip.
- OPEN for the owner or verifier before the first real arm (coverage item D7): `frozen_monitor_log` returns exactly the seven keys the plan and Plan 60-11 name, so the 16 causal weights are not themselves logged although D-06's wording says "per-bin causal weights". They follow from the logged normalized residuals, so nothing is lost. If the owner wants the vector written out, it is one added `w_n` key plus Plan 60-11's key test.
- READING for the verifier: the plan's "energy and angular momentum evaluated only when `weights.lambda_e` or `weights.lambda_l` is above zero" is read as each term on its own weight. A skipped term reports exactly 0.0, which changes no gradient. No other semantic choice beyond the plan's text was made, and no gap was raised.

### Decisions from 60-23 (2026-10-19)

- `run_arm` resolves and checks the `first_omega_0` setting first, before runtime resolution, fixture gating, the first-result test, any data read and any network build. `resolve_first_omega_0` and `check_override` compare literal values only; an unauthorized setting raises `OverrideRefused`; a non-locked value routes to `build_network_with_first_omega`. A fixture arm at `first_omega_0 = 60` records `first_omega_0` 60, `grid_omega` 60 and `g2_sweep_override`, and the evaluator and the production checkpoint store both refuse its weights. Commits `b913e5a0`, `e15c32eb`, `64c843eb`, `c0810079`, `2e7c34d6`.
- The closed 42-arm catalog, `SEQUENCES`, `catalog()` and the `EXIT_*` codes are final. A test-split key in any role is refused before any file is opened (zero-open spies and a subprocess attestation). `preflight_records` classifies the assigned records. Wave 4 gate: 221 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests pass.
- DEVIATION 1: the executor replaced one Plan 60-01 test in `tests/phase60/test_run_short.py` (not in the plan's `files_modified`) because it pinned the locked-only behavior this plan reverses; the Task 1 commit therefore lists that file too.
- DEVIATION 2: the plan's preflight handler cannot label an empty file, because the production admission gate (`pinn/data/admission.py`) raises `IndexError` on a file with no complete snapshot block. The preflight classifies exactly that error as `empty`. The gate bug is pre-existing and was not fixed (deferred).
- OPEN for the owner or verifier before the first real arm (coverage item D8): contract details the plan leaves implicit were settled conservatively. A locked-provenance arm that carries a `grid_omega` is refused; the catalog's rung and path labels are inferred from arm names; every arm is scored on gold with the base record beside it; `OverrideRefused` and `UnknownArm` are not `HarnessHalt`, so launchers must map them to `EXIT_REFUSED`; `inner_pair` is in ok preflight entries; `run_arm` gained `ruling=None`. They move no locked value but set the record and refusal shapes that Plans 60-06 to 60-13 read.

### Decisions from 60-04 (2026-10-19)

- `verify_phase59_evidence.py` accepts a scorer mismatch only for `pinn/verification/feasibility_scorer.py`, only when the result records the predecessor digest `cd5019a2…3870b` and the file has the successor digest `00edf81d…c7`, both taken from the committed `scorer-successor.json` (tracked, clean, exactly the six v1 string keys). Every other fingerprint is still checked. Commits `ec8bd4e8`, `4df5d4a8` (manifest rehash: the verifier's digest and size plus `produced_at_head`, 3 lines), `8d422955`.
- The baselines re-derivation runs against a temporary copy of the committed baselines with only the digest string swapped, and passed (`BASELINES-OK`, 61 s). The scorer fix therefore changed no CPU float64 baseline number, and the GAP-60-02 stop condition did not trigger.
- Phase 59 `final` passed at HEAD `4df5d4a8`: `PHASE59-EVIDENCE-OK`, 604 s, `EXIT=0`. The log is `$HOME/.cache/3bp-phase60-logs/phase59-final-60-04.log` (outside the repository). Plan 60-22 can reuse this evidence while no Phase 59 input changes after `4df5d4a8`.
- `tests/phase60/test_verifier_successor.py` (34 tests) was run RED first, and a mutation check caught 13 of 13 injected faults. Wave 3 gate: 138 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests pass.

### Decisions from 60-03 (2026-10-19)

- `REQUIREMENTS.md` carries the locked scope amendment word for word after whitespace collapse: four edits (the SCOPE-39 row, the FEAS-09 opening line, the SCOPE-44 row and Owner Checkpoint ④). Inside Owner Checkpoint ④ the amendment was 0 of 3 present, not "1 of 3" as GAP-60-01 says (the one existing sentence sat in the FEAS-03 rescue bullet, outside the designated section). No requirement was ticked.
- `tests/phase60/test_amendment.py` (21 tests) parses the six paragraphs from `60-SPEC.md` itself. The frozen scorecard SHA-256 `f4b17688…444b` is unchanged.
- The amendment commit is `dc3edac0` (summary `f9d0b439`). Plan 60-13 should pin that hash in the run protocol.

### Decisions from 60-02 (2026-10-19)

- `network_trajectory` widens on the CPU and then to float64 at all three sites (position, velocity, acceleration), so a float32 network on this Mac's MPS device is scored end to end. CPU float64 behaviour is unchanged. Commits `57f48478`, `2c84d43a`, `08189ab1`, `2734f4c9`.
- D-09 scorer digests: predecessor `cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b`, successor `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7`, recorded in `evidence/scorer-successor.json`. `verify_phase59_evidence.py` stays red on the scorer digest until Plan 60-04 lands, as planned.
- The MPS L-BFGS smoke passed (tiny and production network, the harness's chunked polish closure on a 1001-point gold batch), so no owner stop is needed before Plan 60-08.
- DEVIATION for the owner or verifier: the plan's element-wise float32 tolerance (rtol 1e-4, atol 1e-5) cannot hold for the production network, whose first SIREN layer runs at frequency 30 (17%, 41% and 42% of the position, velocity and acceleration elements fall outside). The test uses a bound of 1e-3 of each array's largest magnitude instead; measured agreement is 4.7e-5, 8.7e-5 and 9.5e-5 of that magnitude.

### Decisions from 60-01 (2026-10-19)

- The data-only fixture arm now runs end to end in `pinn/verification/learnability_{arms,data,losses,run}.py`: allowlisted read, Stage-0 cosine Adam, the frozen L-BFGS polish, both states scored, one exclusive record, plain-git weights. Commits `5e31f46a`, `a9cc3c14`, `015f03b3`. The Phase 60 static guard (`tests/phase60/test_static_guards.py`) finds modules by their "Phase 60" docstring marker, so later modules join the scan without a list edit.
- Fixture runs record `cadence_ok: false` without enforcing it, because whole-step gaps cannot meet a 0.5-step limit below a 20-step budget. Real arms are refused in this plan.
- OPEN for the owner or verifier before the first real arm (coverage item D8): two GAP-60-05 readings are not stated in the sources and change when the polish stops. A polish call's objective is taken at the iterate the call ends with (`LBFGS.step` returns the start-of-call objective), and polish wall time includes the per-call scoring time.
- Wave 1 gate: 64 Phase 60 tests, 31 + 4 prohibition tests and 139 Phase 59 scorer-suite tests all pass, with no skips.

### Decisions from 59-10 (2026-10-16)

- `59-FINDINGS.md` is the owner-facing page (commit `087e4179`). It records the formula's Tier-1 result (1 of 1812 training, 0 of 227 validation), Gate G1 "proceed", and GAP-59-08 reported and not fixed. The Stage-4b and Stage-6 energy-bar reading is labelled a judgment, not a gate.
- `evidence/manifest.json` hashes 49 files. The detached `verify_phase59_evidence.py final` printed PHASE59-EVIDENCE-OK with EXIT=0 in 644 s.
- `59-VALIDATION.md` is signed off (`69bd0cad`), except for feedback latency: `test_evidence_verifier` takes 69.7 s and `test_diag07` 13.6 s.
- FEAS-01, FEAS-02, FEAS-07, FEAS-08 and DIAG-07 are complete.

### Decisions from 59-09 (2026-10-16)

- One detached `--experiment all` run (576.5 s, 513 MB, preflight 7.09 GB) produced every committed jx02-jx05 result. Evidence commit `ce1e6104`; `diag07 --require all --require-committed` prints DIAG07-OK. The manifest supersedes the Plan-07 version (`a2e8d488`), and the Plan-07 files keep their hashes.
- JX-2: estimator noise not excluded. The bin-2 prefix moved 0.155 from step 900 to 951, against 20-draw ranges of 0.172 and 0.141. Every draw gives the frozen front.
- JX-4: relative descent without useful accuracy. The front went 0 to 2, but every fixture is Tier 0 at step 951 (E 13 to 62) and the physical front stays 0. It informs JD-3 only.
- JX-3: mixed, exposure-specific by IC loss (median ratio 0.0052 on the 7 most-anchored systems against 0.33 and 0.27) and global by the residual sum (0.37, 0.45, 0.33). The batch replay is proven on every checkpoint, with 40 distinct anchors.
- JX-5 (structural only): at initialization the acceleration RMS is 2.9e5 against a force RMS of 44, and the skip-branch du-derivative roughly doubles per skip block.
- DIAG-07 readings from single-anchor checkpoints must not set a recipe value (R-2). DIAG-07 stays pending until 59-10.

### Decisions from 59-08 (2026-10-16)

- The two-Kepler formula does not already reach Tier 1 on Stage 0: Tier 1 or better on 1 of 1812 training and 0 of 227 validation systems, median E 0.989 and 0.940. Its error starts at zero and grows with the third body's pull (inner pair 6% off at t = 1, 43% at t = 10 on one system).
- The nearest-neighbour copy reaches Tier 1 on 0 of 227 validation systems, median E 2.14, so 1,812 systems do not cover Stage 0 densely enough for lookup.
- FEAS-09: the formula reads not applicable on both probes (no hierarchical split, D-38). The normalizer matched the audit stats_sha256. The run took 64.6 s and its --check 65.9 s (BASELINES-CHECK-OK). Evidence commit `c5c6cd18`; `baselines --require-committed` prints BASELINES-OK.
- GAP-59-13 (59-09, delegation): the scorer's `network_trajectory` crashes on MPS. 59-09 scores JX-4 through a byte-equivalent MPS-safe copy. Phase 60 must fix the scorer in place before it scores a network on MPS.

### Decisions from 59-06 (2026-10-16)

- The survey covers all 12,023 training-split records and opened no test-split file. Its detached pass (457.6 s, `ru_maxrss` 507 MB, 2 GiB preflight unchanged) and detached `--check` (byte-identical, SURVEY-CHECK-OK) both ended EXIT=0. Evidence commit `04e17dac`; `survey --skip-rederive --require-committed` prints SURVEY-OK.
- Diagnostic stage counts: 0 = 1,812, 1 = 2,074, 2 = 3,886, 3 = 0 (standard base Q spans only 0.0006 to 0.119), 4a = 1,404, 4b = 654, 5 = 1,923, 6 = 269, unlabelled = 1 (`standard/base/3362` ends at t = 9.86). The labels and tau_L are diagnostic, and the official mapping stays owner-pending.
- Envelope medians: Stage 4b tau_L 2.98 (error growth 28.5 by t = 10); Stage 6 tau_L 1.71 (growth 352). Plan 59-10 writes the 1e-5 plausibility reading from these and labels it a judgment.
- FEAS-09 picks by the frozen median rule: `standard/base/2279` (Stage 4b) and `standard/base/3418` (Stage 6). Every sensitivity window moves both picks. This is reported and not acted on (D-20).
- FEAS-08 stays pending until Plan 59-10.

### Decisions from 59-07 (2026-10-16)

- The owner ruled GAP-59-11 option A. A rounded packet field is compared in exact decimal units, so exactly one fourth-decimal step passes and two steps fail. The frozen `phase58_packet_rounded_abs` stays `1e-4`, and every other tolerance and the scorecard are unchanged. Under the float comparison 15 of the 90 one-step cases would have failed, not only the one seen. The evidence verifier does not recompute a packet comparison and was not changed.
- JX-10 reproduces the Phase 58 packet on MPS float32 and CPU float64: 54 of 54 frozen checks pass (seed-42 fronts 0, 1, 2, 2, 2; smoke fronts 0 at steps 100, 200, 300). The reading supports C-F14 and F-H2b.
- JX-1 at checkpoint 900 (`best.pt`) and 951: the physics term supplied a primary share of 7.19e-07 and 2.60e-08 of the Adam-preconditioned update, and both read "physics was a passenger (PC-2)". The IC term supplied almost all of it (primary share about 1.0), the data term about 3e-06 and 6e-06, and energy and angular momentum 0 because Stage 0 sets their weights to 0. CPU float64 agrees (6.94e-07 and 2.59e-08).
- Gate G1 did not fire. Its outcome is `proceed`, identical on CPU float64, so the conformance-first premise of Phase 61 is not re-examined on this evidence. Phase 59 itself was unaffected either way.
- The committed files come from one detached `--experiment all` run (365.7 s, `ru_maxrss` 3.58 GiB, vm_stat preflight 7.48 GB against the unchanged 6 GiB bar). Evidence commit `41dee29a`. `diag07 --require jx01,jx10,g1 --require-committed` prints DIAG07-OK and the guardrails print GUARDRAILS-OK. Plan 59-09 rewrites the diag07 manifest and records this version's SHA-256 as superseded.
- DIAG-07 stays pending. Plans 59-01, 59-03, 59-04, 59-06, 59-09, and 59-10 also declare it.

### Decisions from 59-05 (2026-10-14)

- The owner ruled GAP-59-10 option A. The frozen `monitor_reproduction_ic13_abs` stays `1e-7`; the measured IC13 residual `1.1920928955078125e-07` (`2**-23`) is a recorded deviation and is also the ceiling. The acceptance records `passed` false against the frozen value as measured, carries an `owner_accepted_deviation` block, and the verifier prints an `AUDIT-DEVIATION` line. A larger residual, any target, time, or mass mismatch, a normalizer fallback, or a moved frozen value still halts.
- The acceptance (8,192 rows, 256 identities, zero mismatches) and the census (1,812 training and 227 validation systems) are committed after the freeze, re-derive byte for byte, and open no test-split file. Pair-tracking failures 0; gold-base maximum deviation `9.68e-07` against `1e-6`.
- Panels come from the frozen rule only: singles 1632, 851, and 4658 (N_in 10.47, 18.61, 39.35), a 16-system family, and all 227 validation systems. The median phase-accuracy figure is about 1 part in 1,169 at 10% and 1 part in 11,692 at 1%. 148 training systems have fewer than 3 base samples per inner period.
- FEAS-02 stays pending. Plans 59-03, 59-04, and 59-10 also declare it.

### Decisions from 59-04 (2026-10-14)

- Evidence is canonical JSON written atomically. A payload that contains the home directory or the data root is refused, and a target under `simulation_data` is refused.
- The verifier does not import the writer. It re-derives only by running each tool's `--check`. Gate G1 is recomputed with the frozen `g1_fires` rule.
- The main-checkout corpus guard is `data_root`'s parent when that directory is named `simulation_data`. Refusing the grandparent would refuse the whole worktree.
- FEAS-01, FEAS-02, FEAS-07, FEAS-08, and DIAG-07 stay pending. Later plans also declare them.

### Decisions from 59-03 (2026-10-14)

- Corpus reads go through one hash-checked allowlist. A test-split key raises `SplitRefused` before any path is built.
- Checkpoint record keys are the three-element list the trainer serializes. The stage-0-init normalizer residual is `1.192e-7` over 256 keys.
- FEAS-02, FEAS-07, FEAS-08, and DIAG-07 stay pending. Later plans also declare them.

### Decisions from 59-02 (2026-10-14)

- The scorer tiers only `autograd`, `analytic`, and `brutus` velocities. Finite-difference eps_H is `fd_context_eps_h`, a labelled context column.
- The physics residual mean and max are context fields. `tier_of` does not read them.
- A constant 5% scale of the rigid orbit is vacuous for eps_H, so the frame test applies that 1.05 factor on the later half of the native times. No new tolerance was added.
- FEAS-01 stays pending. Plans 59-04 and 59-10 also declare it.

### Decisions from 59-01 (2026-10-14)

- The feasibility scorecard is frozen before any real-data result. `phase_start_head` is `f3d2f42044ec7d53c8b42dc264866a3a5daab432`. The JSON SHA-256 is `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`.
- Task 1 landed as one tracer commit so that parent stays the commit before the first execution commit. Task 2 followed RED (`04980af4`) then GREEN (`0aac08d8`).
- An improvement rate with no finite reference-window reading raises `OwnerRouted`. No new threshold was added.
- FEAS-01 stays pending. Plans 59-02, 59-04, and 59-10 also declare it.

**v2.4 amendment (2026-10-11, owner-approved).** The owner asked what else
v2.4 should achieve and what is needed to judge where the project stands.
The re-examination
(`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`)
added four requirements:

- FEAS-07, comparison points: a two-Kepler formula and a nearest-neighbour copy;
- FEAS-08, a read-only survey of every stage;
- FEAS-09, two probes on a Stage-4b and a Stage-6 system, run only if G2 passes;
- FEAS-10, a project charter at the verdict.

It also changed the rules:

- a system counts only if it is at Tier ≥ 1 and beats the formula;
- single-system arms get the spec's L-BFGS polish;
- G2 runs a settings sweep before any RETHINK-REPRESENTATION, and a rescue
  is owner checkpoint ④;
- Rung 3 and the control are scored along the way, as accuracy curves;
- the scorer must pass known-error tests;
- the verdict places the project on a readiness ladder (levels 0–9), with
  costs.

The owner leans toward a looser `10⁻⁵` bar, to be decided later with evidence.
It is set in the charter, never by energy alone, and before any held-out
exam.

v2.4 opened 2026-10-09 from the proposal ratified under owner delegation
(`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`,
`0b400dfa`), on branch `milestone/v2.4`, created from `milestone/v2.3` at
`b8632832`. Before it: v2.3 closed 2026-10-04 on its declared terminal state
(owner verdict `rethink`; archived under `milestones/v2.3-*`), and the
`trainex-r4` round was ruled on 2026-10-07 under owner delegation
(`trainex-r4-ruling.md`, `c4bea18a`). The v2.3 phase folders 53–58 stay in
`.planning/phases/` through v2.4 (decided in the proposal; the Phase-57
verifier and its tests hardcode that path).

**This file is maintained by hand in this checkout.** The `gsd-tools`
mutating verbs have corrupted it before (the full note, "Note on this file's
own history", is in this file at commit `b8632832`). `state.milestone-switch`
was used for the v2.4 start and its diff was reviewed; it dropped that note,
which this pointer replaces.

### trainex-r4 re-framing ruling (2026-10-07, owner-delegated)

The owner delegated the round's re-framing decision to the in-repo agent on
2026-10-07. The ruling is recorded in full in
`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/DELIVERY-NOTE.md`
("Re-framing ruling"). In brief:

- **The premise was false.** Generation 7 did not execute the ratified
  recipe's physics term: it ran on one trajectory per step, and the monitor
  scored one trajectory. The round is re-framed, not re-commissioned (R-1).
- **How the answers may be used (R-2).**
  - Structural findings are usable.
  - The run's empirical rates and magnitudes may not set recipe values.
  - The Q4 budget answer is void.
- **Conformance leads the decision sheet (R-3).** The default is the owner's
  GAP-57-01 Option A instruction. Any fix re-triggers `R_ref` and GATE-04. The
  IC term's batch behavior is its own decision.
- **The v2.3 verdict `rethink` stands (R-4).** Its rationale is annotated as
  unsupported in `.planning/milestones/v2.3-GAPS.md` ("Post-close finding").
- **Claude's training- and validation-data reads are permitted (R-5).**
- **Fan-out is closed (R-6).**

### Decisions from 57-01 (2026-09-08)

- **RED-only wave, no production code.** Plan 57-01 committed 46 focused
  stdlib-unittest tests across `tests/phase57/{test_recipe_production_path,
  test_runtime_freeze,test_gate_and_evaluation}.py` plus `_fixtures.py`; zero
  `pinn/` files created or modified. `workflow.tdd_mode` is not set in
  `.planning/config.json`, so the plan's `type: tdd` frontmatter carries no
  enforced GREEN/REFACTOR gate in this checkout — see `57-01-SUMMARY.md`
  "TDD Gate Compliance".
- **The bounded conformance API contract is now fixed by test, not prose.**
  `causal_physics_loss` must gain keyword-only `r_ref` (required) and
  `frozen_weights` (optional); `condition_ii_verdict` changes from
  `(weights) -> None-always-raises` to `(raw_bin_means, r_ref, ...) ->
  Mapping`; `build_checkpoint_payload`/`RunController.state_dict()` need new
  `front_monitor`/`lbfgs_segment_state` keys; `pinn.evaluate` needs a new
  `assert_canonical_frame_precondition()` called before
  `StageIndex.from_split`; a new `pinn.verification.candidate_eligibility`
  module hosts the ported Phase-50 four-fact eligibility/selection pattern
  and a terminal-vs-blocking run-outcome classifier. Full detail and
  rationale: `57-01-SUMMARY.md` frontmatter `key-decisions`.
- **`condition_ii_verdict`'s six-case check replays real committed Phase-56
  evidence, not a fresh network measurement.** A full `compute_r_ref` over
  `DEFAULT_CASES` timed at 167s — too slow for a routine unit suite. The
  sha256-pinned `.planning/phases/56-contract-amendment-train-free-gate/
  evidence/gate04/20260907T033409Z/raw.json` is the six-case data source
  instead; the real production-path re-measurement is explicitly a later,
  separate verification wave's job (57-RESEARCH.md wave 4).
- **`completed_plans` corrected to 25/30 (83%), not the stale 24/30 shown as
  "67%".** The prior `percent: 67` did not match its own paired counts
  (24/30 = 80%, not 67%) — a pre-existing STATE.md data error, corrected
  here as the same field is updated (Rule 1), not a separate cleanup pass.

### Phase 57 owner decisions (2026-09-08)

- **GAP-56-01 resolved.** GATE-04 requires a `2:1` non-anchor spread and the
  fixed all-residual reduction `alpha = log(2)/(2 * P_15)`, followed by
  `front_idx = 15` and every perturbed weight `>= 0.70`.
- **Checkpoint ③ / GAP-54-06 resolved.** `N = 500` is explicitly re-ratified;
  invariant B uses one frozen training-only monitor; L-BFGS samples and
  detached causal weights are frozen for the entire segment.
- **Checkpoint ④ resolved.** Seed 42 is pre-registered, with fallback 41 then
  43 only for structural ineligibility.
- **No run authorization yet.** `57-RULING.md` is the exact record. Phase 57
  still requires plans, bounded implementation, production-path verification,
  and a new complete GATE-04 PASS before RUN-04.

### Decisions from 57-03 (2026-09-08)

- **Strict recipe is an explicit opt-in.** v2.3 configs bind
  `stage.collocation_count=4096` and
  `loss.r_ref_artifact_path=pinn/verification/artifacts/r_ref_stage0.json`;
  run construction rejects partial opt-ins, reduced rows, and invalid or
  provenance-incomplete artifacts while legacy test configs remain compatible.
- **Checkpoint ③ state is additive and fail-closed.** One training-only
  monitor and active L-BFGS samples/detached weights are separate from the
  derived `invariant_b_state`, carry hashes/counters, and restore exact bytes
  or refuse rather than redraw.
- **Config comparability is explicit.** The seed-42 smoke and seed-41/42/43
  graded configs use the full 240-row Stage-0 replay pool, corrected recipe,
  and distinct v2.3 run names; `57-CONFIG-DELTA.md` records the recursive
  predecessor/final scalar diff.

**Phase-54 transition note.** The ROADMAP row is now derived from the completed
artifact set: 13 plans, 13 summaries, passing UAT and canonical verification.
The historical pre-gate records remain unchanged; the terminal ruling and gap
outcomes are additive governance records. `gsd-tools query phase.complete` was
not used because this checkout repeatedly records that mutating state verbs
overwrite STATE.md with malformed generic placeholders. The shared stale-aware
completion predicate was run instead and returned `passed: true` with no blockers;
the exact command and assertions are retained in `54-CLOSE-CHECK.sh`, whose
terminal literal is `PHASE54-CLOSE-PASS`. ROADMAP, REQUIREMENTS, PROJECT and this
state file were then updated explicitly.

### Phase 49 verification (2026-08-10)

- **Phase 49 is not closed.** `49-VERIFICATION.md` records `gaps_found`
  with 4/6 must-haves verified despite the full Phase 49 suite passing 176 tests.

- **Run-local invariant-B eligibility is incomplete.** A real synthetic
  `main()` run with `front_advance_window_n = None` remained record-only but
  emitted `eval01_precondition_i = true` after the global divergence entry was
  closed.

- **Run-start evidence is not required by the eligibility projection.** A
  schema-valid, passed `stage_boundary`-only preflight with no `run_start` or
  census loaded successfully and also yielded `eval01_precondition_i = true`.

- **Phase 50 remains blocked.** `$gsd-plan-phase 49 --gaps` ran on 2026-08-10 and
  produced `49-09-PLAN.md` (wave 6, depends on 49-08), which closes both gaps at the
  single eligibility seam: bind the run-local invariant-B window so an N-unset run is
  structurally ineligible (D-20), and require the run-start table + census evidence the
  predicate claims to summarize. Plan-checker passed with 0 blockers after one revision.
  Next action is gap-only execution of 49-09, then re-verification. The gaps remain OPEN
  until re-verification says otherwise — the plan is forbidden from self-certifying them.

### Decisions from 49-08

- **Phase 49 review BLOCKERs are closed.** CR-03/04/06/09 landed in Plan
  49-08; CR-08's producer-contract repair at `7d4ffd8d` was independently
  re-run without further code changes. The final required gate is 943 passed,
  3 skipped, and 289 subtests passed.

- **Invariant-B policy is owner-ratified, not inferred.** The 2026-08-05 owner
  ruling is `N = 500 (= 0.5 * N_Adam,0)`; the shipped Stage-0 config carries
  that exact value and `INV-B-N-UNSET` is closed by its enforcing trip test.

- **Preflight evidence is append-only across resumed attempts.** Existing
  artifacts are validated and retained before the next run-start event; any
  ordinary setup/probe refusal records its failed event before controlled exit.

- **Phase 50 is authorized to be planned, not auto-launched.** No admitted
  corpus or held-out evaluator was touched during Phase 49 remediation.

### Decisions from 47-02

- **CONF-02 discharged.** `_matched_plummer_components` is the single home of
  the softened pairwise sum (D-11); `k0`/`uabs0` are captured in float64 at
  admission at `EPS_SOFT` before the fp32 residency cast (D-09/D-10/D-12);
  `pinn/training/run_metadata.py` computes the train-split median once at
  setup and persists `s_h`/`eps_h`/`n_train` via `atomic_write_text` with
  re-validate-on-load and explicit `expected_energy_floor_factor`/
  `expected_eps_train` bindings (D-13..D-18).

- **Both setup branches bind the same `s_h` local** — the resume helper
  `_assert_s_h_matches_artifact` RETURNS the validated value, so the 47-03
  `RunController` hand-off is structural, not conventional.

- **First authoritative real-corpus `S_H`/`eps_H`/`N_train` deferred to Phase
  50** (owner ruling 2026-07-30, Option B); Phase 47 proves the semantics
  with deterministic fixtures. No zero-step emitter added; no training
  launched.

- **REQUIREMENTS.md CONF-02 checkbox deliberately NOT flipped by the
  executor** — same phase-close/verification-act precedent as CONF-09.

### Decisions from 47-01

- **CONF-09 discharged.** Residency is `pre.r_gauge`/`pre.v_gauge`;
  `RATIFIED_VALIDATION_FRAME` is `(r_prime, u_t_over_T, ordered_raw)`, re-ratified
  in the same commit; the one pairing test is corrected in place. The one-shot
  re-probe records `identity_scaled` true and a zero max difference against
  `r_gauge`/`v_gauge` for 1651/1651 — record-only, not a new CONF-01 verdict.

- **`r_com_ordered`/`v_com_ordered` survive** on `PreprocessedTrajectory` (D-03);
  `pinn/data/preprocessing.py` is byte-unchanged.

- **REQUIREMENTS.md CONF-09 checkbox deliberately NOT flipped by the executor** —
  that is a phase-close/verification act, and this plan does not mutate the locked
  governance docs it was planned against.

### ⚠ OPEN — surfaced for owner ruling (47-01, D-08)

The D-08 derived bound is **exceeded on the validation-side reading for 9 of 50
sampled real trajectories** (max ratio 4.76); the loss-side reading is inside the
bound on all 50. The physics claim holds — both arms' `eps_H` agree to ~13
significant digits — but Step 4's float64 allowance omits the cancellation
amplification the finite-difference velocity incurs on real Brutus sampling.
Nothing was widened or relaxed (SCOPE-29/D-26). Options: extend Step 4 with a
finite-difference cancellation term; narrow the D-08 claim to the loss-side
reading; or accept the record. Full record: `evidence/frame-re-ratification/20260731T012304Z/re-ratification.md` §4.2.

**Phase 47 scope changed 2026-07-28 (GAP-46-07, owner option A) — read before planning it.** An independent verification of the conformance handoff confirmed all six carried divergences and surfaced a seventh that no requirement owned: CONF-08 excluded the rotation gauge and the `D`/`V` scaling by design, GAP-46-06 ratified the resulting intermediate as the **validation** frame, and neither reached the **training** path, which pairs unrotated/unscaled residents with `u = t/T` — a pairing `COHERENT_FRAME_PAIRS` does not admit. New requirement **CONF-09** completes the residency transform to the locked canonical contract and is sequenced **ahead of CONF-02** (`S_H` is frame-dependent). Milestone is now **24 requirements**; Phase 47 is renamed "Frame Completion & S_H Pipeline" and runs CONF-09 → CONF-02 → CONF-03. The Phase 48 CONF-05 clip bound now waits on CONF-09 as well as CONF-04. `RATIFIED_VALIDATION_FRAME` is re-ratified by CONF-09, so GAP-46-06 is superseded **in part** — CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged. Report: `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`.

## Deferred Items

Items deferred at milestone close on 2026-10-26 (v2.4). Owner decision (2026-10-26): record them here only, as at the v2.3 close. The GSD acknowledge tool was not run, because it writes markers into the archived files, so these items will reappear in the next `audit-open` scan.

| Category | Item | Status |
|----------|------|--------|
| debug | phase39-collocation-slot-multiplicity, phase39-memory-guard-validation | Carried from the v2.0 and v2.3 closes; session records never formally closed |
| uat | 38-UAT partial (v2.0); 24-UAT, 25-UAT (v1.5) | Carried from the v2.3 close unchanged |
| verification | 41-, 42-VERIFICATION human_needed (v2.0); 50-VERIFICATION gaps_found (v2.2) | Carried from the v2.3 close unchanged |
| pending_todo | trainex-r1-research-handoff, d-06-static-epsilon-sensitivity-check | Carried from the v1.6, v2.0 and v2.3 closes |
| deferred_items | Phase 57: Phase-50 test paths; Phases 46/47: `tests/phase43` paths | Resolved 2026-10-04 (see the v2.3 table below); still listed by the scanner because no acknowledge marker exists |
| deferred_items | DI-46-05-01 watchdog packaging drift; DI-43-04-02 `tests/phase42` launch gate | Carried; informational |
| verification_flag | Phases 61–63 have no VERIFICATION.md | Skipped at Gate G2 (no rescue), not failed; no phase directory by design |
| verification_flag | Phase 60 `stale` | Its covered `REQUIREMENTS.md` received Phase 64's edits (`bb323a52`, `5a447624`); no Phase 60 requirement row changed, and `60-VERIFICATION.md` is `passed` |
| requirements | CONF-10/11, INST-06/07, SPEC-07..10, GATE-05, FEAS-05, RUN-06, DIAG-08 | Pending: skipped at G2, not failed. Their label and carry-forward are charter row C-14 (GAP-64-01), open |
| gap | GAP-59-08, GAP-64-01 | OPEN, owner-routed (charter rows C-7 and C-14) |
| gap | GAP-56-02 | Still DEFERRED (it was SPEC-10's subject, and Phase 61 was skipped) |
| validation | 59-, 60-, 64-VALIDATION.md at `status: draft` | Nyquist NOT-VALIDATED; `/gsd-validate-phase` not run |

Closeout type: `override_closeout`. The scan reported 18 open items (2 debug, 3 uat, 3 verification, 2 todos, 8 deferred_items; the first six rows above group them), the same 18 as at the v2.3 close, with 0 acknowledged by a prior close. The milestone audit (`milestones/v2.4-MILESTONE-AUDIT.md`) is `gaps_found` for the twelve skipped-phase requirements only, and the owner chose to close over them (2026-10-26). Milestone verdict: `RETHINK-REPRESENTATION`; owner decision `change-course` (`64-CHECKPOINT-1-RULING.md`).

<details>
<summary>Prior close (v2.3, 2026-10-04)</summary>

Items deferred at milestone close on 2026-10-04 (v2.3). Owner decision: record them here only. The GSD acknowledge tool was not run, because it writes markers into the archived files, so these items will reappear in the next `audit-open` scan.

| Category | Item | Status |
|----------|------|--------|
| debug | phase39-collocation-slot-multiplicity | Carried from the v2.0 close; session record [diagnosed], never formally closed |
| debug | phase39-memory-guard-validation | Carried from the v2.0 close; session record [investigating], never formally closed |
| uat | 38-UAT partial (v2.0) | Carried from the v2.0 close; stale-satisfied, frontmatter never updated |
| uat | 24-UAT, 25-UAT (v1.5) | Flagged by the scanner with status `passed` and 0 pending scenarios; no outstanding item found |
| verification | 41-VERIFICATION, 42-VERIFICATION human_needed (v2.0) | Carried from the v2.0 close (41 stale-satisfied; 42 non-blocking manual checks) |
| verification | 50-VERIFICATION gaps_found (v2.2) | v2.2 Phase 50 closed incomplete by owner decision (`stop-incomplete`, 2026-08-17) |
| pending_todo | trainex-r1-research-handoff, d-06-static-epsilon-sensitivity-check | Carried from the v1.6 and v2.0 closes; deliberate carry-forwards |
| deferred_items | Phase 57: Phase-50 adjacent tests expect `.planning/phases/50-…` | **Resolved 2026-10-04** (owner instruction): test-only fix, with the archived evidence unchanged; `tests/phase50` 52/52 OK |
| deferred_items | Phase 46 DI-46-04-01, Phase 47 ×4: `tests/phase43` path failures (v2.2) | **Resolved 2026-10-04**: the tests read from `milestones/v2.0-phases/`; `tests/phase43` 198/198 OK |
| deferred_items | Phase 46 DI-46-05-01: `tests/watchdog/test_global_packaging.py` (v2.2) | Carried; watchdog repo source vs global deploy drift |
| deferred_items | Phase 43 DI-43-04-02: `tests/phase42` launch-gate failures (v2.0) | Carried; informational |
| verification_flag | Phases 55 and 56 `stale` | Closeout files added after verification (55: UAT and coverage; 56: GATE-04 re-run and gap rulings). Both VERIFICATION.md files are `passed`; Phase 57 re-confirmed GATE-04 PASS |
| verification_flag | Phase 58 has no VERIFICATION.md | Adapted closeout, the v2.2 Phase 52 precedent; VER-21 re-verified 15/15 in `58-SUMMARY.md` |
| gap | GAP-56-02 | DEFERRED by the owner to the milestone after `trainex-r4` |

Closeout type: `override_closeout`. The scan reported 18 open items (2 debug, 3 uat, 3 verification, 2 todos, 8 deferred_items; rows above group them), with 0 acknowledged by a prior close. There is no v2.3 milestone audit file (v2.2 precedent). Milestone verdict: owner-signed `rethink` (`58-VERDICT.md`).

</details>

<details>
<summary>Prior close (v2.0, 2026-07-23)</summary>

Items acknowledged and deferred at milestone close on 2026-07-23 (v2.0):

| Category | Item | Status |
|----------|------|--------|
| debug | phase39-collocation-slot-multiplicity | Open session record [diagnosed]; deferred — session never formally closed |
| debug | phase39-memory-guard-validation | Open session record [investigating]; deferred — session never formally closed |
| uat | 38-UAT partial | Stale-satisfied — its one outstanding item (real-trajectory rung 3/4 gate) passed 2026-07-13 with GAP-38-01 closure; frontmatter never updated |
| verification | 41-VERIFICATION human_needed | Stale-satisfied — both human items (B-5 ratification; R-1/D4-a calibration) owner-ratified during Phase 43 |
| verification | 42-VERIFICATION human_needed | Genuinely open, explicitly non-blocking — 2 Manual-Only visual checks (runbook walkthrough legibility; sleep-assertion identity) |
| pending_todo | trainex-r1-research-handoff | Deliberate carry-forward (r1b tuning round); unlinked to v2.0 phases |
| pending_todo | d-06-static-epsilon-sensitivity-check | Deliberate carry-forward (spec-side sensitivity question); not a v2.0 build item |
| audit_warning | W-1 evaluation-attempt.json absent (seed-42) | Provenance-only; claim hardening postdates the sole evaluation; refusal holds via receipt path; do NOT re-run |
| audit_warning | W-2 runbook omits verify/evaluate entry points | Discoverability only; correctness protected by fail-closed train.py gate |
| audit_warning | W-3 ACC-05 spread location | Spread lives in 43-CALIBRATION.md, not pilot summary.md; substance complete and ratified |

Closeout type: `override_closeout` — all 7 v2.0 phases verification-scored in full and 42/42 requirements Complete; overrides are the acknowledged items above (see `.planning/v2.0-MILESTONE-AUDIT.md`, status `tech_debt`). Milestone verdict: owner-signed `adjust` (43-VERDICT.md).

</details>

<details>
<summary>Prior close (v1.6, 2026-07-02)</summary>

| Category | Item | Status |
|----------|------|--------|
| pending_todo | trainex-r1-research-handoff | Deferred to trainex track (FUT-01/FUT-04); not v1.6 specwork |

Closeout type: `override_closeout` — the only override is the acknowledged trainex-r1 todo above; all 7 v1.6 phases are verification-passed and 32/32 requirements Complete.

</details>

## Performance Metrics

**Velocity:**

- Total plans completed: 892 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 26)
- Average duration: ~10 minutes per plan (v1.1)

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Code Rewrites | 3 | — | — |
| 2. Documentation | 3 | — | — |
| 3. Data Deletion | 2 | — | — |
| 4. Stale Refs | 2 | — | — |
| Phase 05 P01 | 4min | 2 tasks | 2 files |
| Phase 06 P01 | 4min | 2 tasks | 2 files |
| Phase 07-structure-fidelity-verification P01 | 15min | 2 tasks | 1 files |
| Phase 07-structure-fidelity-verification P02 | 38min | 3 tasks | 3 files |
| Phase 08-compilability-verification P01 | 10min | 2 tasks | 3 files |
| Phase 10 P01 | 3 min | 3 tasks | 1 files |
| Phase 10 P02 | 4 min | 2 tasks | 2 files |
| Phase 10 P03 | 4 min | 3 tasks | 6 files |
| Phase 11 P02 | 15min | 2 tasks | 2 files |
| 11 | 3 | - | - |
| 12 | 3 | - | - |
| 13 | 3 | 3 waves | 17 fixes |
| 14 | 3 | 3 waves | 14 fixes |
| 15 | 3 | - | - |
| 16 | 3 | - | - |
| 17 | 3 | - | - |
| 18 | 3 | - | - |
| 19 | 4 | - | - |
| 20 | 5 | - | - |
| 20.5 | 1 | - | - |
| 21 | 2 | complete | 2026-06-08 |
| Phase 23 P04 | 12min | 2 tasks | 1 files |
| Phase 23 P05 | 15min | 2 tasks | 2 files |
| 23 | 5 | - | - |
| 24.5 | 1 | - | - |
| 25 | 2 | - | - |
| Phase 26 P26-02 | 28 | 2 tasks | 3 files |
| Phase 26 P26-05 | ~25 min | 3 tasks | 4 files |
| 26 | 5 | - | - |
| Phase 27 P01 | 15min | 3 tasks | 3 files |
| Phase 27 P02 | 15min | 3 tasks | 3 files |
| Phase 32 P01 | 11 min | 3 tasks | 6 files |
| Phase 32 P02 | 9 min | 2 tasks | 5 files |
| Phase 32 P03 | 10 min | 3 tasks | 6 files |
| Phase 32 P04 | 7 min | 2 tasks | 4 files |
| 32 | 4 | - | - |
| 33 | 4 | - | - |
| Phase 34 P01 | 8min | 3 tasks | 8 files |
| Phase 35-loss-energy-weight-contracts P35-02 | 728 | 2 tasks | 2 files |
| Phase 35 P03 | 12 min | 3 tasks | 2 files |
| Phase 35 P04 | 11 min | 3 tasks | 3 files |
| 35 | 4 | - | - |
| 37 | 5 | - | - |
| Phase 38 P04 | 9min | 3 tasks | 6 files |
| Phase 39 P01 | 18min | 3 tasks | 9 files |
| Phase 39 P02 | 22min | 4 tasks | 8 files |
| Phase 39 P03 | 35min | 3 tasks | 4 files |
| Phase 39 P06 | 17 min | 2 tasks | 2 files |
| 40 | 9 | - | - |
| 44 | 5 | - | - |
| 46 | 10 | - | - |
| 47 | 3 | - | - |
| 48 | 4 | - | - |
| 49 | 9 | - | - |
| 53 | 1 | - | - |
| 54 | 13 | 6 waves + 6 post-delivery waves | complete 2026-09-04 |
| 56 | 6 | - | - |
| 57 | 6 | - | - |
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 39 P11 | 12min | 2 tasks | 3 files |
| Phase 39 P12 | 4min | 2 tasks | 2 files |
| Phase 40 P06 | 20 min | 2 tasks | 3 files |
| Phase 40 P07 | 12min | 2 tasks | 3 files |
| Phase 40 P08 | 25min | 3 tasks | 6 files |
| Phase 40 P09 | 10min | 3 tasks | 3 files |
| Phase 41 P01 | 6min | 3 tasks | 9 files |
| Phase 41 P02 | 5min | 3 tasks | 2 files |
| Phase 41 P03 | 5min | 2 tasks | 4 files |
| Phase 41 P04 | 25min | 3 tasks | 2 files |
| Phase 41 P05 | 10min | 3 tasks | 6 files |
| Phase 43 P02 | ~7min | 2 tasks | 5 files |
| Phase 43 P04 | ~50min | 1 tasks | 2 files |
| Phase 43 P05 | 9min | 2 tasks | 5 files |
| Phase 46 P04 | ~45min | 2 tasks | 4 files |
| Phase 46 P05 | 58min | 2 tasks | 4 files |
| Phase 46 P06 | ~25min | 3 tasks | 3 files |
| Phase 46 P10 | 50min | 2 tasks | 5 files |
| Phase 47 P02 | ~30min | 2 tasks | 7 files |
| Phase 48 P01 | 7 min | 2 tasks | 4 files |
| Phase 48 P2 | 16 min | 2 tasks | 7 files |
| Phase 48 P3 | 14 min | 2 tasks | 8 files |
| Phase 48-loss-math-conformance P04 | 20 min | 2 tasks | 4 files |
| Phase 49 P01 | 50min | 3 tasks | 8 files |
| Phase 49 P02 | 7min | 3 tasks | 7 files |
| Phase 49 P04 | 20min | 3 tasks | 6 files |
| Phase 50 P01 | ~50min | 3 tasks | 15 files |
| Phase 50 P06 | 11 min | 3 tasks | 7 files |
| Phase 50 P07 | 23 min | 3 tasks | 8 files |
| Phase 54 P11 | 37 min | 4 tasks | 4 files |
| Phase 56 P01 | 42 min | 2 tasks | 5 files |
| Phase 56 P04 | 15 min | 3 tasks | 1 files |
| Phase 56 P02 | 52 min | 2 tasks | 3 files |
| Phase 56 P05 | 15 min | 3 tasks | 3 files |
| Phase 57 P01 | 63 min | 3 tasks | 5 files |
| Phase 57 P03 | 45min | 3 tasks | 11 files |
| Phase 57 P04 | 45min | 3 tasks | 13 files |

## Accumulated Context

### Roadmap Evolution

- v1.0: Codebase Cleanup (Phases 1-4) — shipped 2026-03-20
- v1.1: LaTeX Modularization Verification (Phases 5-8) — shipped 2026-03-22
- v1.2: PINN Implementation Readiness (Phase 9) — complete; 3 thematic docs + MIGRATION.md + README.md written, verified and validated
- v1.3: Markdown Conversion Verification & Correction (Phases 10-15, 15.1) — shipped 2026-05-08; post-ship SCS gate correction verified 2026-05-15
- v1.4: Resolving 01 Architecture and Physics Foundations (Phases 16-22, plus inserted Phase 20.5) — shipped 2026-06-09. All phases closed; archived under `.planning/milestones/v1.4-*`. EDL support remains a non-canonical support workflow under `.planning/research/edl/`.
- v1.5: Resolving 02 Data Pipeline and Validation (Phases 23-29) — shipped 2026-06-17. 36/36 requirements mapped; standard granularity; 8 phases (incl. inserted 24.5). Phase 23 (research package) first; Phase 24 (verification + DATA-07 addendum) ran in parallel with the external-research gate; Phases 25-29 gated on the resolution doc AND Phase 24. Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md` (SCOPE-08/09/10). Branch `milestone/v1.5` from master HEAD `b8b39a4`; `--no-ff` merged to master (fe9b3c92) and archived under `milestones/v1.5-*` 2026-06-17 (tag v1.5).
- v1.6: Resolving 03 Curriculum and Training Loop (Phases 30-36) — roadmap created 2026-06-17. 32/32 requirements mapped; standard granularity; 7 phases (no inserted decimal). Phase 30 (research package) first and ungated; its delivery opens the external resolution-doc gate. Phase 31 (resolution-doc readiness verification, operational, 0 IDs) gates Phases 32-36. Phase 32 stands up the evidence ledger and adjudicates the headline conflicts (D-04/D-05/D-06 + `D=6.694` + M14) before the contract phases transcribe verdicts: Phase 33 (CURR), Phase 34 (LOOP), Phase 35 (LOSS). Phase 36 (VER) executes acceptance checks + handoff. Specwork-only (SCOPE-13/14/15); `pinn/` never grounding (SCOPE-10). Branch `milestone/v1.6` (worktree) cut from the v1.5 deliverable tip `88aa1e4f`; rebased onto completed master 2026-06-17 once v1.5 shipped.
- v2.0: CTL-PINN Training Viability Slice (Phases 37–43) — roadmap created 2026-07-06. The project's first **build** milestone, opening the trainex track. 42 requirements mapped; standard granularity; 7 phases continuing from v1.6's Phase 36 (no reset). Dependency-ordered, no external gate: 37 ENV (dev env + D1-p probe) → 38 NET (`pinn/` rebuild, FUT-01) → 39 DATA (in-memory adapter + Stage-0 scan) → 40 TRAIN (Adam→L-BFGS Stage-0 loop, FUT-04) → 41 CTRL (config/checkpoint/guards/determinism) → 42 OPS (operator runbook + monitoring) → 43 ACC (verify + Stage-0 pilot + go/adjust/rethink verdict). Grounded in the ratified trainex-r1a decision set (2026-07-05); `pinn/` ban lifted; owner-carved decisions built as seams. Planning on `master`; build in `.worktrees/trainex`.
- v2.1: Physics-Gate Investigation & trainex-r2 Research Package (Phases 44-45) — roadmap created 2026-07-23; both phases complete 2026-07-24, 7/7 requirements delivered; close PENDING five open gaps. Small granularity, 2 phases, no external gate inside the milestone (the gate opens at close). Phase 44 (DIAG-01..04) read-only forensics from retained v2.0 artifacts → `44-DIAGNOSIS.md`; Phase 45 (PKG-09..11) the trainex-r2 ERW package, delivered and audited PASS. SCOPE-22..26 held throughout: no evaluation, no training, no spec edits, no remedy chosen. **Post-delivery:** the returned report (Route B / open-book) established that the v2.0 Stage-0 pilot diverged from the locked specs in five verified respects, qualifying Phase 44's DIAG-04 rankings (`44-ERRATUM.md`) and opening GAP-44-02 + GAP-45-01..04. Branch `milestone/v2.1` in `.worktrees/trainex`.
- v2.4: Stage-0 Feasibility Checkpoint (Phases 59–64) — roadmap created 2026-10-09, inline from the proposal ratified under owner delegation (`0b400dfa`). 20 requirements; standard granularity; 6 phases continuing from v2.3's Phase 58. A learnability ladder in front of the `trainex-r4` corrected control: 59 read-only baseline and scorecard (G1) → 60 single-system rungs, data only then physics (G2 can exit to the verdict) → 61 conformance and instrumentation → 62 gates and the 16-system rung (G3) → 63 the corrected control and its readout → 64 the feasibility verdict (owner decides). SCOPE-39..44: Stage-0 only, every run diagnostic, no graded run or held-out evaluation, pre-registration, amendment discipline, compute budgets. Branch `milestone/v2.4` in `.worktrees/trainex`. Amended 2026-10-11 with owner approval: FEAS-07..10 added (24 requirements, 24/24 mapped: FEAS-07/08→59, FEAS-09→60, FEAS-10→64), SCOPE-39/41/44 widened, owner checkpoint ④ added. (v2.2 and v2.3 bullets were never added here; their records are in `MILESTONES.md`.)
- v2.5: Root-Cause Confirmation (Phases 65–69) — roadmap created 2026-10-27, inline from the owner-approved milestone text (`633f8eb4`) and requirements (`85c1a930`). 13 requirements; standard granularity; 5 phases continuing from v2.4's Phase 64: 65 the probe on the record and the fit harness (DIAG-09, INST-08) → 66 the small-network control (EXP-01; owner checkpoint ① reviews the plan) → 67 the depth, learning-rate, time-input and window ladders (EXP-02..05; provisional) → 69 findings and the owner's redesign decision (VERD-01/02, VER-23); 68 the yardstick (YARD-01..03; owner checkpoint ②) is independent of the experiments. SCOPE-45..49: Stage-0 training records only, no spec edits, one prediction page per experiment, this Mac only, and the pivot rule (results may add, drop or re-aim phases; the owner decides). Branch `milestone/v2.5` in `.worktrees/trainex`.
- Phase 15.1 inserted (URGENT) after Phase 15: Fix milestone v1.3 markdown conversion issues
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked (2026-05-20, commit b727b15); completed execution 2026-06-07.

### v1.6 Phase Summary

| Phase | Focus | Requirements | Gate |
|-------|-------|--------------|------|
| 30 | Research package assembly (annotated doc list + framed questions, figures "claimed, unverified" unless v1.5-verified; D-04/D-05/D-06 + `D=6.694` posed neutrally) + read-only characterization of `review-of-framework.md` / `stage-strat-revision.md` | PKG-05..08 | None (first phase); delivery opens external gate |
| 31 | Resolution Doc Readiness Verification (v1.5 Phase 24.5 analog) | Operational (no new IDs) | Consolidated resolution doc landing |
| 32 | Evidence framework, issue ledger, root-cause conflict adjudication (D-04/D-05/D-06, M14, `D=6.694`) + re-verification ledger | EVID-11..15 | Phase 31 |
| 33 | Curriculum-stage contracts (adaptive assignment, `tau_L`/`L_max`, dual-path transitions, Stage 0–6 gating, s_min stage-gate frame) | CURR-01..05 | Phase 31 (via Phase 32 verdicts) |
| 34 | Training-loop & batch-construction contracts (replay/lookahead, two point sets, mixed sampling, merged clipping, ALM+`μ_p` clamp, `dt_out` collocation scaling, SASD/IPR/PSC training-side use) | LOOP-01..08 | Phase 31 (via Phase 32 verdicts) |
| 35 | Loss & energy-weight contracts (loss scaling, capped-hybrid `λ_E`, Huber-δ, D-04 causal-mode contract) | LOSS-01..04 | Phase 31 (via Phase 32 verdicts) |
| 36 | Acceptance checks executed, ledger close, SI-ledger reconcile, FUT-01/FUT-04 handoff, 32/32 traceability | VER-13..18 | Phases 32–35 |

**Execution order:** 30 → ⛔gate opens (user ERW research starts) → 31 readiness check → 32 (evidence + conflict adjudication) → 33 (curriculum) → 34 (training-loop) → 35 (loss) → 36 (acceptance + handoff).

**Verification protocol (applies to every adjudication phase 32–36):** adjudicate → fix → verify → re-verify after every batch → close only when the acceptance check passes. The issue ledger lives at a stable path under the Phase 32 (evidence-framework) directory. Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; probes never touch `pinn/`. STOP protocol in full; phase-local `NN-GAPS.md` + milestone index `.planning/milestones/v1.6-GAPS.md`.

### v1.5 Phase Summary

| Phase | Focus | Requirements | Gate |
|-------|-------|--------------|------|
| 23 | Research package assembly (annotated doc list + framed questions, figures "claimed, unverified") + DQA characterization | PKG-01..04 | None (first phase); delivery opens external gate |
| 24 | Empirical dataset verification + DATA-07 correction addendum (seeds the issue ledger) | DATA-01..07 | None external; runs in parallel with gate window; depends on Phase 23 |
| 24.5 | Resolution doc readiness verification (INSERTED) | Operational (no new IDs) | Consolidated resolution doc + Phase 24 |
| 25 | Evidence framework, verdicts, root-cause conflict adjudication, re-verification ledger | EVID-06..10, VER-10 | Phase 24.5 |
| 26 | DataLoader ingestion & selection contracts | PIPE-01, 02, 03, 05, 06, 10 | Phase 24.5 |
| 27 | Sampling, precision, dt_out/stage-query, global-scale contracts | PIPE-04, 07, 08, 09 | Phase 24.5 |
| 28 | Validation-metrics contracts (SCS, SASD, IPR, PSC) | VAL-01..04 | Phase 24.5 |
| 29 | Acceptance checks executed, ledger close, SI-ledger reconcile, handoff | VER-07, 08, 09, 11, 12 | Phase 24.5 |

**v1.5 execution order:** 23 → ⛔gate opens (user research starts) ‖ 24 runs in parallel → 24.5 readiness check → 25 → 26 → 27 → 28 → 29.

### v1.4 Phase Summary

| Phase | Focus | Requirements |
|-------|-------|--------------|
| 16 | Evidence framework, issue ledger, conflict adjudication | EVID-01..05, VER-02, VER-05 (defined) |
| 17 | Input and output contracts (incl. COM projection head) | IO-01..04 |
| 18 | Frame and gauge contracts | FRAME-01..04 |
| 19 | Physics and loss contracts (incl. M4 constraint counting) | PHYS-01..06 |
| 20 | Architecture and normalization cleanup | ARCH-01..05 |
| 20.5 | Sampling coordinate allocation | SAMP-01, SAMP-02; SCOPE-05 boundary; complete |
| 21 | Acceptance checks executed, SI-ledger reconciled, handoff | VER-01, VER-03, VER-04, VER-06 — complete |
| 22 | Presentation-preserving framework-spec cleanup | Complete; G1-G4 and VER-05 passed |

### v1.3 Phase Summary

| Phase | Source | Sections | Candidates | Key Challenge | Status |
|-------|--------|----------|------------|---------------|--------|
| 10 | ctl-instruction | 8 | 3 (.md, _v2.md, pandoc) | Heavy math, stage criteria formulas | COMPLETE |
| 11 | Data-quality-assessment | 7 | 2 (.md, pandoc) | Cross-references, HTML table corruption | COMPLETE |
| 12 | pinn-architecture | 7 active + 3 inactive | 3 (.md, _v2.md, pandoc) | Comment block exclusion, inactive sections | COMPLETE |
| 13 | review_of_framework | 7 | 1 (pandoc only) | Sub-document structure | COMPLETE |
| 14 | stage_strat_revision | 6 | 1 (pandoc only) | Table normalization, bibliography reconstruction | COMPLETE |
| 15 | sampling-method | monolithic | 2 (.md, pandoc) | Monolithic source (no sections/ dir) | COMPLETE |

### Decisions

Recent decisions affecting current work:

- [Phase 54 checkpoint ②, 2026-09-04]: **Owner-authorized recalibration `A1 + B2 (residual-wide) + C1 + D3 + E1`.** Retain `eta_c=1`; define a finite positive `R_ref` as the median of 96 raw bin means from six fixed initialization-probe cases and freeze it for Stage 0; normalize both the causal exponent and training physics loss; retain `first_omega_0=30`; retain the dtype-derived underflow-only clip and make binding observable.
- [Phase 54 checkpoint ②, 2026-09-04]: **GAP-39-12 remains the count-unit authority.** `n_col=4096` is total per training batch, not per trajectory. D3 re-ratifies only the time-allocation clause: 16 fixed equal-`u` bins, exactly 256 rows per bin, one batch-global 16-bin prefix. The single-anchor 16-point controller is a divergence Phase 56 must replace, not the calibration target.
- [Phase 54 checkpoint ②, 2026-09-04]: **Resampled training fronts are diagnostics, not invariant evidence.** Checkpoint ③ must pre-register a fixed monitoring context and re-ratify the advancement window. GAP-54-06 defers the conditional L-BFGS detached-weight/line-search question to that checkpoint because SCOPE-33 does not authorize an optimizer-contract amendment in Phase 56. Ten Phase-54 gaps are resolved and one is explicitly deferred; Phase 56 remains closed until Phase 55 completes.
- [Phase 54 Plan 54-11, 2026-09-03]: **`REFRAME-DETERMINATION=REFRAME-PARTIAL`** and **`CONSOLIDATION-AUTHORIZED=YES`** (commit 83447250). Three packet premises are contradicted and eleven qualified, but none of the three reaches the round's framing, and the one finding that would have — that a pathology survives disposing of all five enumerated surfaces — carries `NOT-VERIFIABLE-HERE` rather than a contradicting verdict, so the premise it bears on is `UNSETTLED` and not `CONTRADICTED`. `UNDETERMINED` was rejected because the choice among the four values is answerable from confirmed verdicts and the packet's own text; `NO-REFRAME` was rejected because eleven qualifications reach answers the round returned. The same value is recorded for each of the five enumerated surfaces separately. Wave 5 may proceed, carrying every premise finding attached to the answers it reaches.
- [Phase 54 Plan 54-11, 2026-09-03]: **`ANSWERS-NOT-USABLE=0`, and the reason is a finding rather than an absence.** Both returned reports discharged the ERW Rule-17 premise-challenge duty, so they answered against the corrected readings rather than the contradicted ones — two of the three contradictions were found and reported by the reports themselves, and the third was found by one and resolved by the verification pass computing the arithmetic a third time.
- [Phase 54 Plan 54-11, 2026-09-03]: **Ten owner decisions routed as `GAP-54-02`..`GAP-54-11`; one routed to the anchor; seven disposed of as operational coordination.** Nineteen candidates were assessed, none grounded, and all ten surfacing candidates passed the STOP protocol's step-2 understanding test. Whether the authorized decision-surface set is complete is classified **cross-phase reframing** and handed over unresolved — the enumeration is the owner's to widen. Where a normalization of the residual belongs is inside `GAP-54-01`'s scope and was routed there by appending rather than duplicated under a new identifier (D-17 boundary applied, D-10 unchanged, granularity offered back).
- [Phase 46 Plan 46-04]: CONF-01 evidence layer landed (commit aa094f37). Population rule fixed and manifest-parametric: eligible = train-or-validation under EVERY supplied manifest; excluded = test under ANY, attributed `test_under_<label>`; the test partition is read as a manifest-payload physical-key set, never a StageIndex (D-16). Exclusion ledger keyed on PhysicalKey so the excluded set is exactly the supplied manifests' test partitions. Resident-reader routing uses the first supplied manifest's membership (routing-only choice, recorded via `first_manifest_label`). Control reader streams per key under a `--chunk-size` FIFO window, never caching the corpus. Manifest labels derive from path stems with deterministic `~2` collision suffixes. Rule-3 deviation: the plan-mandated control reader was registered in the Phase 39 GAP-39-02 sole-reader audit allow-list (`tests/phase39/test_prohibitions.py`) — a registration gate, exactly one coherent resolution. Pre-existing `tests/phase43` failures (12; worktree-environmental + stale archived-milestone paths, zero coupling) logged as DI-46-04-01, not fixed.
- [Phase 39 verification 2026-07-16]: Verification closeout ran under owner "Full closeout" instruction. 39-10-03 authority checkpoint resolved as Option A (gsd-core hard-gate at <home>/Desktop/code/gsd-core `fix/phase-complete-uat-predicate`, deployed to .claude-alt); 39-10 closed with SUMMARY. Canonical 39-VERIFICATION.md produced by gsd-verifier → **gaps_found (6/7)**. DATA-01..06 substance solid (251/251 dataset-free tests pass; all requirements map to real code), but an independently-reproduced evidence-integrity gap blocks completion: 39-VALIDATION row 39-07-02 is marked green yet its command fails against the retained 9-line scan.log — the original 41-line scan.log (acf9b207) was hand-assembled (its `# adapter init_log` block cannot come from the CLI), and 39-10-01 honestly regenerated the minimal true CLI output without correcting the ledger. Root cause: `pinn/data/stage_scan.py` CLI never serializes `AdmittedSetAdapter.init_log` (mem/watermark/blacklist/freshness). Phase 39 stays In Progress; fix routed to /gsd-plan-phase 39 --gaps. Memory-below-watermark held mechanically (adapter fail-closed) but is not independently provable from retained bytes.
- [Phase 39 closeout 2026-07-16]: Gap-closure plans 39-11..39-14 executed and committed. 39-11 added fail-closed redacted `evidence_lines()` + per-fidelity `n_present_on_disk`/`n_excluded` to `AdmittedSetAdapter`; 39-12 wired `evidence_lines()` into the scan CLI with `run_timestamp`/`run_nonce`/`evidence_byte_identity` freshness markers and renamed `exit_code`→`scan_exit_code`; 39-13 regenerated real-corpus evidence (scan.log now carries `mem:`/`n_blacklist_entries`/`n_present_on_disk`/freshness fields, no `/Users/` leakage); 39-14 repaired the vacuous row 39-10-02 awk assertion. Row 39-07-02 command re-run: observed exit 0. 39-UAT updated: Test 24 → pass, 27/27 pass, status complete, G-39-24 resolved. ROADMAP Phase 39 marked `[x]`. STATE advanced to Phase 40.
- [D1-p RESOLVED 2026-07-12]: Owner recorded **fp32-MPS** (Option A) for D1-p, resolving GAP-37-01 and retiring the same-day deferral below. Verbatim ruling (*"...we will remain with the entire training happening on the MacBook Pro with M5 chip. Let's carry on with that choice and decision for now."*) plus an explicit branch-naming confirmation (owner selected "fp32-MPS" from {fp32-MPS, fp64-CPU, keep deferred}) are recorded in the gap register, including the R-6 dual-arm tolerance ratification (fp64-CPU reference arm; fp32-MPS within ~1e-4). Production default: `precision=float32, device=mps`; fp64-CPU remains the in-framework escape hatch (ENV-04). **Phase 38 (NET) UNBLOCKED**; ENV-03 closable. Single-machine M5 Pro training reaffirmed — a Lenovo/multi-machine split is a later cost-benefit question outside v2.0. No code changed (CTX-14): `pinn/runtime.py` encodes no default; the Phase 40/41 training config consumes the recorded value.
- [D1-p DEFERRED 2026-07-12]: Owner recorded an explicit DEFERRED verdict for D1-p (precision branch, fp32-MPS vs fp64-CPU) at the Plan 37-05 blocking checkpoint. Verbatim: *"i picked the wrong option. let's defer that and we'll decide on this later."* The owner retracted an initial fp32-MPS selection. **Phase 38 (NET) is blocked at the D1-p seam until the owner records a branch.** The agent did NOT choose, recommend, or apply a precision default. The retained dual-arm evidence (`evidence/precision/20260712T150406Z/`) is reusable; no re-run required when the owner records a branch. Full gap record: GAP-37-01 (`.planning/phases/37-developer-environment-precision-adjudication/37-GAPS.md`); milestone index: `.planning/milestones/v2.0-GAPS.md`.
- [integrity-r2-clearance 2026-07-11]: Owner disposed the integrity-r2 pre-build audit punch-list (MASTER-FINAL-RESOLUTION, status candidate/owner-disposes, verdict NO-GO): **PB-1 Option A + interim floor** (Stage-0/1a/1b `s_min` criterion becomes data-derived `s₀` ratified at the Phase 39 DATA-06 scan; interim `s₀ = 0.01`), **PB-2/PB-3/PB-4/PB-5 all Option A** (five-term Huber loss catalog; corrected replay/lookahead data/collocation contract; `physical_key` grouped-split invariant; Tier-1 dataset-count correction — corpus arithmetic becomes ≈8.23M snapshots ≈0.72 GB fp32, no ratified decision changes). Owner authorized a bounded spec micro-pass on `ctl_instruction.md` now (departing from the delivery-note "future spec milestone" routing): `s_min` repair, Set 1b/2a count swap, `compute_L_norm` degenerate-branch fix (IR2-007), DATA-05 quarantine historical note (IR2-008). v2.0 REQUIREMENTS/ROADMAP patched accordingly (NET-04, DATA-02, DATA-04, DATA-05, DATA-06 + Phase 38/39 criteria). **Phase-37 pre-build gate: CLEARED** (nothing waived). Clearance record: `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md` (trainex worktree, `milestone/v1.7` commit `09c972c6`).
- [v2.0-init 2026-07-06]: v2.0 is the first **build** milestone (trainex track), scoped as the postspec-r1 **viability slice** (Stage-0 first); the full multi-stage platform is deferred pending an ACC-06 go/adjust/rethink verdict. Owner chose a major bump (v1.7 → v2.0) marking the spec→implementation inflection. Grounding is authoritative, not a candidate verdict source: the ratified trainex-r1a decision set (2026-07-05; D1–D7 / B-1–B-11 + §5 first-run recipe) for build-engineering, and the locked v1.4/v1.5/v1.6 specs for the science. The `pinn/` live-code ban is **LIFTED** (FUT-01 rebuilds from specs). Five owner-carved decisions (D1-p precision, D4-a checkpoint ceiling, RECOVER budget + HALT/guard thresholds R-1/R-2, B-5 resume-field list) are built as seams with safe defaults and calibrated/ratified by the owner at their designed moments — the build analog of the STOP protocol; the agent surfaces evidence, it does not pick the values.
- [v2.0-roadmap 2026-07-06]: 7 phases (37–43), standard granularity, continuing numbering from v1.6's Phase 36. 42/42 requirements mapped 1:1 by category (ENV=4, NET=5, DATA=6, TRAIN=7, CTRL=8, OPS=6, ACC=6). Straight dependency order 37→43, no external research gate (unlike v1.4–v1.6 — the research is already delivered and ratified). Planning artifacts committed on `master`; build execution in `.worktrees/trainex` on `milestone/v2.0` (renamed/created from the stale anticipatory `milestone/v1.7` at first phase execution).
- [v1.6-roadmap 2026-06-17]: 7 phases (30–36), standard granularity, continuing numbering from v1.5's Phase 29 (no reset). Phase 30 (research package, ungated) first; its delivery opens the external resolution-doc gate. Phase 31 (resolution-doc readiness verification) is operational (0 requirement IDs) and given the next whole number rather than a decimal because it is a planned milestone phase, not an urgent insertion (departs from the v1.5 inserted-Phase-24.5 convention). Phase 32 (EVID) stands up the ledger AND adjudicates the headline conflicts before the contract phases transcribe verdicts — there is intentionally NO standalone empirical-dataset-verification phase (doc-03's dataset facts were settled in v1.5; remaining empirical work is FUT/trainex). Contract phases 33/34/35 (CURR/LOOP/LOSS) follow the EVID verdicts; Phase 36 (VER) executes acceptance checks and writes the handoff. 32/32 mapped (VER-14).
- [v1.6-init]: v1.6 targets issue doc 03 (curriculum + training loop); specwork-only, ERW package-first. Resolution doc is NOT authoritative — candidate verdict source only, same standing `ctl_pinn_resolution.md` had in v1.4 and `02-resolution-doc.md` had in v1.5. Issue doc non-authoritative. Locked v1.4 + v1.5 outcomes are hard-constraint grounding (SCOPE-12), incl. raw-mass `D ≈ 4.6416` (doc-03's `D=6.694` must reconcile, EVID-15). `pinn/` never grounding (SCOPE-10). Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md` (SCOPE-13); `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` / `review-of-framework.md` / `stage-strat-revision.md` read-only (SCOPE-09); training-loop code + EDA run + Stage-0 pilot are FUT-01/FUT-04 (SCOPE-14/15).
- [v1.6-init]: v1.6 initialized in an isolated worktree (`../3_body_problem-v1.6`, branch `milestone/v1.6`) cut from the v1.5 deliverable tip `88aa1e4f` — departs from the v1.4/v1.5 "no worktree" convention because v1.5 closure runs concurrently in the main tree. The branch is rebased onto the completed `master` once v1.5's `--no-ff` merge + `/gsd-complete-milestone` land. Tag `v1.6-pre-phase-NN` from branch HEAD before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.
- [v1.5-roadmap-revision 2026-06-10]: Phase-order swap — **research package first (Phase 23)**, **empirical verification second (Phase 24)**. Rationale: the user's external multi-AI research is the milestone critical path (it gates all adjudication, Phases 25–29), so the package must ship first; figures in the package are marked "claimed, unverified" (PKG-03). PKG-04 (DQA characterization) moves to Phase 23 (read-only, fast, informs the document-list decision). DATA-07 added — a post-verification correction addendum forwarded to the in-flight external research; nil addendum if nothing contradicted. Phase 24 runs in parallel with the gate window and gates on nothing external.
- [v1.5-roadmap]: 7 phases (23–29; 8 incl. inserted 24.5), standard granularity, derived from issue-02's simpler shape (one issue doc, two spec-edit targets). Research package (Phase 23) precedes; verification + correction addendum (Phase 24) runs in parallel with the external resolution-doc gate; EVID/PIPE/VAL adjudication (Phases 25–28) and acceptance/handoff (Phase 29) follow the gate AND Phase 24.
- [v1.5-roadmap]: VER-10 (re-verification ledger) owned by Phase 25; the ledger file lives at a stable path under the **Phase 24 (empirical-dataset-verification)** directory, seeded with the finding inventory + DATA evidence by Phase 24 and operated through the protocol established in Phase 25.
- [v1.5-roadmap]: VER-08 satisfied by this roadmap (every requirement maps to exactly one phase, 36/36); confirmed again at Phase 29 closure.
- [v1.5-init]: Resolution doc is NOT authoritative — candidate verdict source only, same standing `ctl_pinn_resolution.md` had in v1.4. Issue doc non-authoritative. Every finding verified empirically before any fix.
- [v1.5-init]: Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` read-only/characterized (SCOPE-09); `pinn/` never touched and not grounding (SCOPE-10).
- [v1.5-init]: On-disk dataset (SCOPE-06) and `simulation_data/Scripts/` (SCOPE-07) are grounding for v1.5; extends the v1.4 SCOPE-05 carveout.
- [v1.5-workflow]: All v1.5 work on `milestone/v1.5` branch (cut from master HEAD `b8b39a4`). Tag `v1.5-pre-phase-NN` before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.
- [v1.4-EDL]: Empirically consequential source-silent gaps may attach central EDL research briefs under `.planning/research/edl/`; phase-local gap registers remain authoritative.
- [Post-v1.3]: SCS gate — raw Hamiltonian drift is `\epsilon_H`, SCS is `\log_{10}(\epsilon_H)`, gate is `\epsilon_H > 10^{-5}` / `SCS > -5`. v1.5 Phase 25 EVID-10 locked the log-based gate and rejected issue-02 ratio thresholds; the raw-mass `D ≈ 4.6416` convention stands (`D = 6.694` rejected). v1.6 reconciles issue-03's `D = 6.694` against this hard constraint (EVID-15).
- [Phase 25 2026-06-12]: Four v1.5 EVID-10 verdicts locked: SCS `accept-resolution` (locked log-based gate `SCS > -5` stands); D=6.694 `accept-resolution` (raw-mass D ≈ 4.6416 stands; CLM-13 ratified `convention-rejected`); M12 `accept-third-position` (`n_pts = min(n_pts_cap, n_snapshots)`); M11 MAJOR→BLOCKING reclassification STANDS. These are SCOPE-12 hard constraints for v1.6.
- [Phase 30]: Phase 30 research package delivered; external resolution-doc gate OPEN, user multi-AI ERW research starts
- [Phase 31 2026-06-20]: Resolution-doc readiness verdict READY-WITH-CAVEATS. Pre-exec gate PASS (doc 48,049 B / 282 lines, byte-identical to commit `49fb7958`; Phase 30 `5/5 complete + verified`). 18/18 selected findings `covered` by identity (0 `silent`, 0 `partial`); 0 v1.5-verified-fact contradictions (CLM IDs cited as provenance anchors; `D ≈ 4.6416` exact-matches EVID-10); 0 SCOPE-12 violations (§1.16 read fresh — upholds `4.6416`, rejects `6.694`). 12 non-blocking caveats routed by design: D-04/D-05/D-06 + §1.17 `tau_L` + GAP-17 provenance → Phase 32 EVID-15; M16/NS-13/ALM defers → Phases 34/35; unverified figures → FUT; §6 non-independence → provenance hygiene. Phases 32-36 UNBLOCKED. The resolution doc is the candidate verdict source (not authoritative); Phase 31 adjudicated nothing. No STOP-protocol gap arose.
- [Phase 32 Plan 32-01]: Created first-write baselines plus issue-03 evidence protocol/template/ledger machinery; the resolution doc remains a candidate verdict source, not authority, and live `pinn/` code remains NOT grounding.
- [Phase 32 Plan 32-01]: D-04, D-05, and D-06 remain owner-routed decisions; Plan 32-01 seeded routing without selecting causal mode, `s_min` gate frame, or static epsilon strategy.
- [Phase 32 Plan 32-01]: Every non-headline row must get an evidence packet and ledger update before downstream spec edits; `FIX_APPLIED` is not terminal.
- [Phase 32]: Plan 32-03: D-04 remains defer-with-blocker; no causal-training Option A/B/C selected without explicit owner instruction. — The issue doc and candidate verdict source preserve D-04 as owner-routed, and Phase 32 must not select a semantic default.
- [Phase 32]: Plan 32-03: D-05 remains defer-with-blocker; no final s_min stage-gate frame selected without explicit owner instruction. — Matched-Plummer loss-side evidence is recorded, but the curriculum stage-gate frame remains owner-routed.
- [Phase 32]: Plan 32-03: D-06 remains defer-with-blocker; loss-side epsilon_train = 1e-5 stays locked while static/invariant epsilon remains owner-routed. — The resolution doc narrows the open decision to static/invariant context; no sensitivity study or explicit owner instruction resolves it.
- [Phase 32]: Plan 32-04 closed Phase 32 structural verification; closeout remediation subsequently registered the known D-04/D-05/D-06 owner-route blockers as GAP-32-01/02/03 with `DEFERRED` status per user instruction. D-04, D-05, and D-06 remain defer-with-blocker owner-routed decisions; all final structural and closeout guards passed.
- [Phase 32]: Plan 32-04 protected-path and baseline guards passed before closeout — Framework specs, frozen/read-only reports, final resolution doc, .planning/STATE.md, and pinn/ remained untouched during task verification; the unrelated dirty docs patch, gap-file state, untracked pinn state, and resolution-doc identity matched the Phase 32 baseline.
- [Phase 32 closeout 2026-06-21]: Created `32-GAPS.md` and `.planning/milestones/v1.6-GAPS.md` for GAP-32-01/02/03; added the ledger `Owner Phase` legend without changing owner values; reconciled Phase 32 complete -> Phase 33 next state.
- [Phase 34]: B-07 (LOOP-01): consume resolution-doc §1.4 modified verdict; keep 240/16 and n_pts_cap=32 as provisional defaults; route source-silent edge cases to 34-GAPS.md by Plan 34-03
- [Phase 34]: B-08 (LOOP-02/03): consume resolution-doc §1.5 modified verdict; formalize two independent point sets; carry 8192/4096 as provisional; defer mandatory collocation 50/50
- [Phase 34]: M16 (LOOP-06): consume resolution-doc §1.10 defer; record dt_out scaling as realized-as-deferred with no transcribed formula and no probe
- [Phase 34]: ALM mu_p clamp (LOOP-05): consume resolution-doc §1.18 defer; reject dense-residual ALM from default loss; clamp conditional on optional scalar-conservation ablation
- [Phase 34]: LOOP-04 reuses existing Phase 32 M14 packet; no new M14 packet authored
- [Phase 34]: LOOP-07 and LOOP-08 are v1.5 carry-forwards with no ledger row and no packet
- [Phase 34]: Phase 34 evidence packets mirror Phase 32 template/schema without reinvention
- [Phase 35]: No new semantic/spec decision was invented in 35-02; loss contract text follows Phase 35 evidence packets and owner-ratified D-04 Option A.
- [Phase 39-02]: AdmittedRecord field renamed s_min -> min_separation to keep pinn/data/types.py off the sole-classifier prohibition audit (only pinn/data/stages.py may co-occur s_min with STAGE_0/STAGE_1).
- [Phase 39-02]: evaluate_admission blacklist kwarg defaults to frozenset() (not required) to match the frozen tests/phase39/test_admission.py contract from Plan 01, which calls evaluate_admission(parsed) with no blacklist arg.
- [Phase 39-02]: Admission clause 6 COM/momentum checks are optional com_norm/momentum_norm kwargs (default None) since ParsedTrajectory carries no preprocessed state; Plan 39-03 wires them after running preprocessing.
- [Phase 39-02]: REQUIREMENTS.md DATA-01..06 left Pending (not marked complete) despite the plan frontmatter listing all six: Plan 39-02 delivers only the pure building-block layer (types/parser-helpers/preprocessing/stages/admission); DATA-01/02/03 need Plan 39-03's AdmittedSetAdapter integration and DATA-04/05/06 have zero code yet (splits.py/batches.py/stage_scan.py are Plans 39-04/05/06). Matches Plan 39-01's identical precedent.
- [Phase 39-03]: DATA-01/02/03 marked Complete — Plan 39-03 landed the production AdmittedSetAdapter (two-pass scan→admit→classify→fp32 residency), the deterministic GAP-39-07 resident_tensor_bytes numerator + mem_ballpark lower-bound cross-check, and the DATA-01..03 integration/containment gate. DATA-04/05/06 remain Pending (splits.py/batches.py/stage_scan.py are Plans 39-04/05/06).
- [Phase 39-03]: The full production adapter (residency, accessors, mem accounting, module-level resident_tensor_bytes/format_mem_line) landed in the task-01 commit rather than being split across tasks 01/02, because the frozen Wave-0 deferred tests (AdapterResidencyTests, ResidentBytesTests) activate the instant the AdmittedSetAdapter symbol exists and cannot be partially satisfied. Tasks 02/03 add the plan's additional named requirements as additive tests. Mirrors Plan 39-02's frozen-test-is-load-bearing precedent.
- [Phase 39-03]: Adapter constructor follows the frozen Wave-0 test's interface (root=, precision=, device=, run_dir=, version_metadata_path=, capacity_bytes=) rather than the plan prose's data_root=/memory_capacity_bytes= naming, since the deferred tests are the load-bearing contract; plan-named features (GSD_DATA_ROOT/git-common-dir default, DataSourceRootMissing/Incomplete, GSD_ALLOW_PARTIAL_DATA_ROOT, mem_ballpark, resident_tensor_bytes_misfit, remediation_quarantine, records_at/records_at_or_below/has_stage) are layered in as additive behavior + tests.
- [Phase 39-03]: adapter.py references .s_min (building the interim classify record) but deliberately contains NO STAGE_0/STAGE_1 literal — numeric-stage detection uses `label is not StageLabel.UNASSIGNED` / `label.value` — so it stays off the sole-classifier prohibition audit while stages.py remains the sole numeric classifier. The classifier floor is stored as self.classifier_interim_s0 (word-boundary-safe against the s0-mutation detector) and passed positionally to classify_stage_label.
- [Phase 41]: Retained exit_code as internal param while renaming emitted scan.log field to scan_exit_code=; plan acceptance grep over-broad on param names
- [Phase 40]: [Phase 40 Plan 40-05]: RunController anchors L_IC/L_E/L_L on one representative identity per fixed batch (pinn.loss_catalog single-trajectory-scoped signatures), computing h0/l0 from that identity ground-truth snapshot-0 via loss_catalog own helpers, eps_h provisional |h0|*1e-4; GradClipper.clip fixed to materialize its params iterable (was silently no-oping the apply call on a live generator) and gained state_dict/load_state_dict for RunController checkpoint composition.
- [Phase 40]: CurriculumController requires exactly one of run_controller/forced_disposition at construction — Defensive Rule 2 addition beyond the plan's T-40-09 both-supplied guard; a controller with neither could never produce a StageDisposition
- [Phase 41]: CR-01: RECOVER restores RunController from rollback payload before retry (dual-guard: live controller + run_controller key)
- [Phase 41]: CR-02: zero L-BFGS headroom polls StageExitMachine once; n_adam==max_epochs stays legal (GAP-40-02 A)
- [Phase 41]: WR-01: GradClipper checkpoint carries dtype as string and restores via closed local float32/float64 map
- [Phase 41]: WR-03: percentile_10_relaxation is a reserved owner-authorized degraded-advancement seam with no automatic consumer
- [Phase 41]: GAP-40-04 Option C: stage_factory yields RunController; ADVANCE swaps + rebinds schedule before stage-init save
- [Phase 41]: stage_factory=None preserves PLAT-01 single-stage; no default factory / no invented per-stage tables (SCOPE-19)
- [Phase 41]: 41-01: checkpoint cadence under run.checkpoint; guards under run.guards; RNG format UNDECIDED (A sidecar vs B sibling)
- [Phase 41]: TorchSaveCheckpointStore name preserved as production body; CHECKPOINT_SCHEMA_VERSION owned by checkpoint.py
- [Phase 41]: failure-* excluded from fallback_scan and latest.pt; bounded by failure_keep
- [Phase 41]: should_checkpoint elapsed is time-since-last-write via last_written_time + injectable time.monotonic
- [Phase 41]: GuardOutcome per-family RECOVER/HALT (LOW-1); memory signal torch.mps.driver_allocated_memory with injectable total
- [Phase 41]: apply_strict_cpu_determinism returns float64/cpu RuntimeSpec for pinn.train build override (HIGH 4)
- [Phase ?]: Dual save path: Phase-40 nested save() + CTX-53 save_anchor via build_checkpoint_payload
- [Phase ?]: Beyond-terminal promote soft-fail; TRAIN-07 preflight owns stage>=3 hard stop
- [Phase ?]: checkpoint_hook/guard_hook are closures with phase-specific placement (Adam before step, L-BFGS after)
- [Phase ?]: Seed fan-out: ArchitectureSpec.seed = config.run.seed for weight init + sampling
- [Phase ?]: B-5 RESUME_FIELD_REGISTRY is provisional; unclassified-to-refuse is locked
- [Phase ?]: python -m pinn.train is the CTRL-01/05/08 composition root with exact-anchor resume routing
- [Phase ?]: 43-02: velocity for the gate Hamiltonian is derived by finite-differencing the model's predicted positions (never input-time autograd), keeping the model forward pass a single torch.no_grad() call; gate_verdict is the sole PASS/FAIL source (SCS is display-only), avoiding a two-independent-booleans render; the evaluation receipt is colocated with metrics.json/metrics.md at the operator-supplied --output directory per the plan's literal artifact contract
- [Phase ?]: [Phase 43 43-04]: ACC-01 completed — pinn.train._check_duration_gate wired into the launch preflight before run_dir.mkdir; reconciled pre-existing uncommitted work rather than rewriting (matched plan + 43-REVIEWS.md HIGH finding + SPEC edges R1/R2). Discovered (not fixed, out of scope): tests/phase41/test_train_entrypoint.py (17/193) and tests/phase42 subprocess-launch tests now fail against the new fail-closed gate since they launch fresh non-smoke pinn.train without a persisted calibration; logged as DI-43-04-01/02 in deferred-items.md for a follow-up fixture update.
- [Phase 43 43-06, 2026-07-21]: ACC-02 real smoke complete over the real admitted corpus: 32 identities, 300/300 gap-free steps, checkpoints 100/158/200/300, one SIGTERM interrupt + `--resume latest` to finished, `s_per_step=0.11570`, forecast 34.71s. Loss bounded but non-descending across the 300-step Adam budget — recorded as an ACC-05 pilot watch-item, never framed as convergence. Three owner-carved seams closed this plan: B-5 `ratify-current` (unchanged registry); R-1 `loss_explosion_ceiling=1e11` via owner delegation (revisable at ACC-05); D4-a `wall_clock_ceiling_s=120` via owner's explicit selection, persisted in `configs/stage0-example.yaml`. Two Rule-3 operational auto-fixes: `data.blacklist_path` threaded to fix DI-43-06-01 (owner-authorized, legacy Documentation blacklist designated authoritative), and `rolling_keep` 3→4 in `configs/smoke.yaml` to preserve checkpoint 100 across the required interrupt.
- [Phase 46 Plan 46-05]: INST-01 safety properties proven as tests (commit 270e045). Held-out isolation enforced doubly — AST scan over raw validation_gate source covering absolute/from/relative import spellings, plus a fresh-subprocess sys.modules check (T-46-05-01). Prior-mode restoration proven from BOTH prior states under an injected mid-population failure; mode bracket AST-pinned handler-less try/finally. Non-interference proven bitwise (real CPU/float64 network), structurally (exact signature pin), behaviorally (deterministic passes). Artifact contract pinned: atomic publication with no temp residue, schema fail-closed over the full 16-key 46-03 schema list, NaN/Infinity/-Infinity quoted sentinels under plain json.loads, pointer fields only behind a durable schema-valid sidecar; valid-FAIL observation still yields gate_status ok (metric FAIL is honest evidence). Both suites dataset-free with inline FrameConvention (the wave-5 ratified-frame constant never referenced — T-46-05-04). Clarified 46-03 contract: validator enforces the 16 top-level keys; nested frame/row shape pinned on the published payload; Inf-aggregate shape constructed directly with gate_metrics-derived SCS/verdict. Pre-existing watchdog packaging failures (2, live-deploy drift) logged as DI-46-05-01, not fixed.
- [Phase ?]: [Phase 46 Plan 46-06]: CONF-01 real-corpus evidence run (commit f106889b) returned VERDICT_AMBIGUOUS over 1651 GAP-46-02-Option-A trajectories -- routes D-09, not the clean D-08 continuation. 100% of eligible trajectories carry a body-permutation confound and a com_recenter_boost gauge divergence; identity_raw=true for 100% but only 66.6% (1100/1651) clear the corrected-raw residual tolerance, short of decide_verdict rule 4's unanimity requirement, so the verdict falls to the rule-6 fail-closed catch-all. 46-VERDICT.md (commit 6638204d) records the branch; Plan 46-07 and Phase 47 stay BLOCKED pending owner resolution. GAP-46-01's consequence note: the verdict selects neither of that gap's two evaluator-pairing readings cleanly, though the identity classification leans structurally toward the raw-target reading.
- [Phase 46 GAP-46-05, 2026-07-27]: Phase 46 re-scoped by owner instruction after GAP-46-04's option-A routing proved circular — Plan 46-07 waited on a repair owned by Phases 47/48, while Phase 47 was gated on Phase 46 closing (`ROADMAP.md:103`), so neither phase could start. Option A: move the **minimum** repair (body permutation + COM-recentre/boost gauge) and its follow-up CONF-01 re-probe into Phase 46, traced as new requirement **CONF-08** (milestone 22 → 23). The `D` scaling is excluded from the repair because it is the raw-vs-scaled question CONF-01 exists to answer; rotation gauge enters only if the re-probe measures it as the new `first_diverging_step`. New plans: 46-08 (repair, wave 5), 46-09 (re-probe + verdict, wave 6, `autonomous: false`); 46-07 moves to wave 7 with its hard gate unchanged. GAP-46-04 is superseded **in part** — only on which phase performs the minimum repair; `VERDICT_AMBIGUOUS` is still not upgraded and residual conformance repair stays with Phases 47/48. Engineering basis: `S_H = median_train(K0 + Uabs0)` is mass-weighted in both terms, so computing it over the un-permuted corpus would yield an `S_H` for a different three-body system and mis-scale `ε_H = 1e-4·S_H` across the milestone. Correction recorded in the same amendment: CONF-01 and INST-01 had been marked Complete prematurely (RG-02 is measurably unresolved and sits under EVAL-01 precondition (ii); INST-01's production wiring is the unexecuted 46-07) — both reverted to Pending.
- [Phase 46 GAP-46-06 + Plan 46-07, 2026-07-28]: **The validation frame is ratified by owner instruction, not by a machine verdict.** Plan 46-09's one post-repair probe returned rule-5 `VERDICT_NON_FRAME_DIVERGENCE`. Root cause is structural, not empirical: `decide_verdict` rule 4 requires `all_identity_raw` — a byte-match against the parsed file-order array (`target_frame_probe.py:641`) — which CONF-08's authorized repair deliberately removed, plus `all_raw_corrected_consistent`, whose unconditional inverse-permutation correction post-repair *creates* the mismatch it was written to undo (1100 → 0). **Our own repair made the clean verdict unreachable.** Orchestrator analysis of the committed `raw.json` showed option B's "only 1086/1651" caveat is a zero-margin tolerance artifact: raw-vs-provenance-control median ratio 0.999996, failing trajectories exceeding by ~0.002%, `tolerance_floor` equal to the control median for 1651/1651, and `tolerance_fp32_increment` exactly 0 for 801/1651 — while the two float64 controls agree to 8.6e-16 and the float32 resident to ~1e-6, i.e. residency quantization. The substantive raw-vs-scaled question is answered by measurement (scaled arm separated by a factor of 12.3); only the token was unobtainable. Owner ruled option B: ratify `("r_raw", "t_native", "ordered_raw")` with `conf01_evidence_ref` on the `20260728T014532Z` run. Plan 46-07 then landed `RATIFIED_VALIDATION_FRAME` (quoted from the resolution note, never inferred — D-12), the `_run_validation_gate_pass` seam inside checkpoint_hook's existing validation branch (no new cadence — D-10), sidecar-before-pointer ordering (D-17), fail-closed `failed:` conversion (D-15/D-20), and the summary projection with `eval01_precondition_iii`. Verified by inspecting a real run's artifacts, not by a passing test: 240 per-trajectory `{record_key, eps_h, scs}` rows per validation event, ratified frame embedded in the sidecar, `gate_status ok` with `gate_verdict FAIL` kept distinct.
- [Phase 46 Plan 46-10]: Closed both remaining INST-01 verifier gaps: validate_sidecar_payload now recomputes every per-row/aggregate gate value through gate_metrics and binds compact fields via compact_validation_fields_from_payload; every validation event (finite/NaN/+Inf/-Inf loss, ok/failed gate) is durably persisted, and eval01_precondition_iii selects only the physical latest JSONL line with type-and-value-sensitive equality against the validated sidecar, so a failed/malformed/cross-run/wrong-step event can never expose an older eligible success.
- [Phase ?]: [Phase 47 Plan 47-02]: CONF-02 S_H pipeline landed (commits 2b985eee, 2ecc53d3). _matched_plummer_components is the single home of the softened pairwise sum (D-11); k0/uabs0 captured in float64 at admission at EPS_SOFT before the fp32 cast (D-09/D-10/D-12); run_metadata.py computes the train-split median once at setup and persists s_h/eps_h/n_train via atomic_write_text with re-validate-on-load and explicit expected_energy_floor_factor/expected_eps_train bindings (D-13..D-18); _assert_s_h_matches_artifact RETURNS the validated s_h so both setup branches bind the local 47-03 threads into RunController. First authoritative real-corpus S_H/eps_H/N_train deferred to Phase 50 (owner Option B); REQUIREMENTS.md CONF-02 checkbox deliberately not flipped by the executor.
- [Phase ?]: Phase 48 Plan 48-01: Rbar is assembled as sum(residual**2, body/component)/3 before the existing causal consumer.
- [Phase ?]: Phase 48 Plan 48-01: data_huber_loss retains .mean(), documented as sum(Huber)/(9*N_t) under GAP-45-01/D-01.
- [Phase ?]: LossConfig.lambda_e_max defaults to exact 0.0 while retaining finite, nonnegative, <=1 validation.
- [Phase ?]: Both shipped Stage-0 YAML entry points explicitly declare lambda_e_max: 0.0; ScheduledWeights remains generic with nonzero caps supported.
- [Phase ?]: CONF-05 causal weights clamp at the active dtype/backend upward-directed representable log-tiny floor, with exact five-field runtime provenance.
- [Phase ?]: Fresh and resumed training setup derive and enforce the same causal clip facts from RuntimeSpec through strict atomic training_metadata.json.
- [Phase ?]: Adam and L-BFGS gradient telemetry uses non-mutating autograd.grad diagnostics with explicit pre-total-backward and last-closure provenance.
- [Phase ?]: Missing or non-finite required gradient statistics fail closed as null telemetry with grad_stats_complete=false and step_completed=false.
- [Phase 49 Plan 49-06]: Owner ruling 2026-08-05 sets `front_advance_window_n = 500`; invariant B is enforcing and `INV-B-N-UNSET` is closed with a passing proof test.
- [Phase ?]: GATE-03 invariant A, invariant B, and causal_stats_missing remain HALT-family StepGuards entries; existing step-log and failure-bundle paths are unchanged.
- [Phase 49 Plans 49-04/49-08]: The ordered census manifest resolves concrete producer contracts; the fail-closed divergence register and preflight preserve open caveats verbatim.
- [Phase ?]: Every closed register entry carries a passing proof-test node; waivers cite existing authority only.
- [Phase 49 Plan 49-08]: Scheduler state is scalar-validated before PHYS-05 arithmetic/comparison; ordinary setup/probe failures persist refusal evidence; resume retains the validated preflight history.
- [Phase ?]: Plan 50-01: --stage-0-only fresh-run Stage-0 ceiling added to CurriculumController/pinn.train (SCOPE-27); guarded ADVANCE skips stage increment, stage_factory, stage-1-init, promotion, and the k->k+1 disposition record
- [Phase ?]: Plan 50-01: four Phase-50 configs committed with D-04 diff receipt; 50-PRE-REGISTRATION.md fixes seed-42 candidate/checkpoint/fallback order before any graded run; 50-CONFIG-DELTA.md derived by structural load_config() diff; STAGE0-BUDGET-DELTA qualification appended to divergence register via API
- [Phase ?]: Plan 50-01: RUN-01/RUN-02 requirement checkboxes deliberately NOT flipped (D-30 reserves that to phase verification); all wave-1 files landed in one commit (abd5f8d) on milestone/v2.2 per D-17
- [Phase 50 Plan 50-06]: MPS prediction conversion is detach then CPU then float64, matching `_as_cpu_f64`; metric/frame/population/thresholds unchanged
- [Phase 50 Plan 50-06]: `telemetry_overwrite_proven: true` on Adam and L-BFGS validation-step logs; training causal snapshot is passed explicitly to `_log_step`
- [Phase 50 Plan 50-06]: `grounded_causal_front_repair: none-in-current-sources`; later-generation authorization is exclusively Plan 50-08; GAP-50-03 untouched
- [Phase 50 Plan 50-07]: Normal extract/identity-baseline/identity/attempt/band/candidate/finalize/all are fixture-tested; terminal generations 1–3 remain `TERMINAL-EVIDENCE-OK`
- [Phase 50 Plan 50-07]: Candidate selection replays 42→41→43 eligibility-only facts and never reads a metric value; no run, smoke, or graded seed was launched
- [Phase 50 Plan 50-07]: REQUIREMENTS.md RUN-01/RUN-02 checkboxes not flipped (D-30); `final_band_generation` remains null; GAP-50-03 untouched
- [Phase 56]: [Phase 56 Plan 56-01]: GATE-04's Phase-57-facing public contract frozen by owner answer "confirmed" (2026-09-06, option accept-proposed) — the ratified_causal_weights probe-helper signature, the Gate04Verdict/Gate04CaseResult/VERDICT_PASS/VERDICT_BLOCK/gate04_verdict surface, and the r_ref_stage0.json artifact path with schema phase56-r-ref-stage0/v1 are accepted exactly as proposed in 56-01-PLAN.md Task 1; no name was amended. — Phase 57's RUN-04 imports these names and reads this JSON schema as a hard precondition on spending the milestone's single Stage-0 run, so the contract was frozen by an explicit checkpoint before any of it was written (one-way-door naming freeze; 56-CONTEXT.md D-04/D-05/D-07/D-09 delegated the exact names to Claude's discretion with owner confirmation).
- [Phase 56]: [Phase 56 Plan 56-04]: The SCOPE-38 core amendment landed in pinn_architecture.md section 3.2 as three additive blockquotes after the retained-byte-identical Phase 35 contract: Block 1 (causal exponent amended to the frozen-reference normalized bin residual, AC-LOSS-04 re-issued verbatim), the frozen residual reference (median-of-96-raw-bin-means procedure, two-central-order-statistics convention, detached/frozen for Stage 0, residual-wide application, the fifteen-trigger invalidation list transcribed verbatim, no numeric value fixed), and Block 4 (4096 rows total per training batch exact, 16 fixed equal-u bins with the half-open/closed boundary convention, 256 rows per bin, one batch-global exclusive 16-term prefix, the 240-slot replay-only construction and its re-issued acceptance criterion verbatim, GAP-39-12 Option C superseded only as to its independent full-domain time-draw clause, SPEC-06 binding + re-check trigger). All verbatim passages byte-exact-verified against 54-RULING.md; zero removed lines in the plan diff; render oracle 0 DEFINITE. — 54-RULING.md checkpoint 2 (owner delegation 2026-09-04, ratified surface set A1 + B2 residual-wide + C1 + D3 + E1) is the authorizing source; SCOPE-38 requires amendment-not-value-edit with named superseded rulings and re-issued acceptance criteria. Transcription (not composition) eliminates spec drift; additive placement keeps the partially superseded Phase 35 text readable so the supersession stays meaningful.
- [Phase 56]: 56-02: condition_ii_verdict always raises NotImplementedError naming GAP-56-01; condition_ii/iii diagnostics are descriptive-statistics-only with status UNRATIFIED, no verdict-shaped field
- [Phase 56]: 56-02: main() refreshes the governed r_ref_stage0.json artifact only for the default six-case run (args.cases_config is None), since a custom case list fails the artifact's own DEFAULT_CASES identity check
- [Phase 56]: [Phase 56 Plan 56-05]: The two NOT-AMENDED contracts (§2.2 first_omega_0 fixed-at-30, §4.1 causal-exponent clip underflow-only purpose) are recorded separately and by name, each immediately adjacent to its own locked sentence, with Phase 20 ARCH-01 and GAP-56-02 named for the SIREN block and the ruling's observability addendum (reject non-finite before clipping, log unclipped exponent + guard-binding count, fail GATE-04 on init-time binding — explicitly stated as observability, not a repurposing of the clip) transcribed for the clip block. Three secondary reconciliation sentences land in prose only: the run-driver collocation_count=16 vs ratified 4096-total divergence (SPEC-06, D-03, no pinn/ file touched), the Listing-3 recommended-range wording reconciled as historical (D-11, closes 53-UNSWEPT-INVENTORY item 5, listing byte-unchanged), and the §4.1 eta_c=1 default bullet now cross-references the §3.2 re-issued AC-LOSS-04 instead of standing beside the still-displayed raw-residual formula (D-10, coefficient value byte-preserved). The render oracle was re-adjudicated (6 pre-existing entries corrected for a +2 line shift caused by the §2.2 insertion, re-verified by content match per 54-RULING.md's anchor-drift warning rather than assumed; 1 new entry for the NOT-AMENDED blockquote's first_omega_0 citations; the 12 pre-existing unrelated Phase 34/35 REVIEW findings left untouched) and a 13-test committed pytest guard (tests/phase56/test_spec_amendment_contract.py) now protects the whole transcription after the plan closes, with genuine RED/GREEN proven for its line/token-position check. Whole-plan diff carries exactly one removed line (the authorized eta_c cross-reference edit); render oracle 0 DEFINITE; no pinn/ file touched; §2.4 table untouched. ROADMAP Phase 56 success criteria 2 and 3 are now met.
- [Phase 56]: [Phase 56 Plan 56-06]: Phase close-out. `56-OPEN-ITEMS.md` records, without resolving: GAP-56-01 (GATE-04 condition (ii) — `condition_ii_verdict` always raises naming the gap, `condition_ii_diagnostics` reports descriptive statistics only under `status: "UNRATIFIED"`, no numeric threshold anywhere in this phase's output, the four candidate options pointed at `56-GAPS.md` without ranking); the two structural findings the owner's ruling will need (all six audited cases show `front_idx=0` at init under the healthy amended recipe because each case's second weight already falls below the half threshold, and a residual reduction confined to the late bins cannot move `front_idx` at any magnitude because a weight depends only on the exclusive prefix over the bins before it); GAP-56-02 (§2.4 table scope, still untouched, three candidate mechanisms pointed at `56-GAPS.md`); and the accepted pre-existing Phase 38 spec-freeze-guard failure, with all four scoping reasons (outside SCOPE-33's grant on a plain reading; re-baselining would be self-certification; Phase 55 set the precedent; the base-reference choice is a governance decision, not a phase-scoped one) and the expected failure signature (exactly two failures, both naming the superseded SCOPE-18 prohibition) so a future red suite reads as this known condition rather than a new regression. Separately, the finished `gate04_train_free.py` (every Phase 56 plan landed) was run once for the record over the six default cases: verdict PASS (`unratified: ii`, GAP-56-01 OPEN), all six cases satisfy condition (i) (min weights 2.100040e-11 to 1.313271e-06, orders of magnitude above the float64 clamp floor), `front_idx=0` on all six as expected. `R_ref = 19749775821.24417` (numpy.median of 96 raw bin means) is numerically identical to every prior run in this phase (fully deterministic computation) but the regenerated, committed `pinn/verification/artifacts/r_ref_stage0.json` now carries this run's own provenance (commit `be823429`) rather than the 56-01 tracer's — the artifact that gates Phase 57's RUN-04 should carry the finished code path's provenance. The full command, tree state, verdict, per-case table, and reference value are recorded re-derivably in `.planning/phases/56-contract-amendment-train-free-gate/evidence/gate04/20260907T033409Z/` (raw.json + summary.md). Neither GAP-56-01 nor GAP-56-02 was resolved, narrowed, or pre-empted; the Phase 38 guard was not edited (`git status --porcelain -- tests/phase38/` empty); the Phase 38 spec-freeze baseline was not regenerated. REQUIREMENTS.md GATE-04/SPEC-01/SPEC-06 checkboxes and ROADMAP's Phase 56 completion marker deliberately NOT flipped by this executor — reserved for the phase-close/verification act, per this milestone's established precedent (Phases 49/53/55; every prior Phase 56 plan).
- [Phase 57]: GATE-04 now requires the owner-ratified non-anchor 2:1 spread and fixed all-residual alpha reduction, with a complete six-case PASS before any run.
- [Phase 57]: The independent production verifier binds exact 4096-row conformance, frozen monitor/L-BFGS checkpoint state, and final R_ref/Gate provenance without launching training.
- [Phase 57]: The evaluator asserts canonical r_prime/u_t_over_T/ordered_raw before held-out split materialization and candidate selection remains structural-only in order 42/41/43.

### Pending Todos

v2.0 CTL-PINN Training Viability Slice initialized 2026-07-06. Next: `/gsd-plan-phase 37` (or `/gsd-discuss-phase 37`) from the `.worktrees/trainex` worktree once its branch is aligned to `milestone/v2.0`.

- [x] Update PROJECT.md with the v2.0 Current Milestone (goal, target features, grounding, git workflow); archive v1.6 context
- [x] Reset STATE.md for v2.0 (`gsd-tools state.milestone-switch`)
- [x] Define v2.0 requirements (42 across ENV/NET/DATA/TRAIN/CTRL/OPS/ACC)
- [x] Create v2.0 roadmap (Phases 37–43; 42/42 mapped)
- [ ] At first phase execution: align the `.worktrees/trainex` branch to `milestone/v2.0` (currently the stale `milestone/v1.7`); tag a pre-phase recovery point
- [ ] Carried-forward: `trainex-r1-research-handoff` (r1a ratified 2026-07-05; r1b tuning round pending — a Future item) and `d-06-static-epsilon-sensitivity-check` (spec-side sensitivity question, not a v2.0 build phase) remain in `.planning/todos/pending/`, unlinked to v2.0 phases

### Prerequisites

**v1.4/v1.5/v1.6 shipped and merged to master** — the framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are complete and authoritative: 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-02 AD contract, PHYS-03 softening, PHYS-05 scheduled weights, the post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), raw-mass `D ≈ 4.6416`, the Stage 0–6 curriculum + CURR-03 stage-exit machine, LOOP-01..08 batch/loop contracts, LOSS-01..04 loss contracts. **Trainex-r1a decision set ratified 2026-07-05** (D1–D7 / B-1–B-11 + §5 first-run recipe). Both are v2.0's authoritative grounding. The on-disk `simulation_data/` admitted set + v1.5-verified dataset facts are the training data. **Hardware confirmed** (R-3 CLOSED): Apple M5 Pro, 24 GB unified memory, 15-core CPU.

### Blockers/Concerns

- **The memory-footprint reader test fails on this machine (found 2026-10-09, at the v2.4 start).** The failing test is `tests/phase57/test_resource_preflight.py::FootprintReaderTests::test_current_footprint_rises_and_falls_with_a_touched_allocation`. After a ≥200 MiB allocation is freed, macOS `phys_footprint` drops by only 8,421,400 bytes (the assertion needs ≥ 209,715,200). The failure reproduces in isolation.
  - **Not a v2.4 regression.** The v2.4 commits changed only Markdown (`git diff b8632832 HEAD -- tests pinn scripts` is empty). The rest of the run was green: `tests/phase57` plus `tests/phase37/test_componentwise_ad.py` gave 116 passed, 1 skipped, and this 1 failed in 174.5 s; `tests/git_policy` gave 77 passed.
  - **Why it matters.** The generation-7 launcher's resource preflight and memory guard read this counter.
  - **Action.** Phase 61 or 63 planning must check how the guard behaves on this OS before any long run.

- **Build execution branch:** v2.0 code work happens in `.worktrees/trainex` on `milestone/v2.0`. Alignment completed at merge commit `89daf842`, preserving the trainex-only history and the master planning/spec updates. Do NOT commit v2.0 build code to `master`. Every session surfaces `git status --short --branch` before any file mutation.
- **Owner-carved decisions are NOT invented:** D1-p (precision), D4-a (checkpoint ceiling), the RECOVER retry budget + HALT/guard thresholds (R-1/R-2), and the B-5 resume-field list are built as seams with safe defaults and calibrated/ratified by the owner at their designed moments (probe / smoke test / Stage-0 pilot / before run #1). The agent surfaces evidence; it does not pick these values.
- **`pinn/` ban lifted for v2.0:** FUT-01 rebuilds `pinn/` FROM the specs; v2.0 is the first milestone to write production `pinn/` code. The v1.3-era `basic_architecture.py` / `data-processing-pipeline-full.py` are reference-only and replaced wholesale.
- **Spec inputs are read-only in v2.0:** a build-discovered spec defect is surfaced as a gap and routed to a spec milestone; v2.0 implements the specs, it does not edit them.
- **No external research gate:** unlike v1.4–v1.6, v2.0 has no candidate-verdict-source gate — the research (trainex-r1a) is already delivered and ratified. Phases run in straight dependency order 37 → 43.
- **CONF-01 is settled by owner instruction, not by a machine verdict (2026-07-28, GAP-46-06).** The ratified frame constant `RATIFIED_VALIDATION_FRAME` in `pinn/training/validation_gate.py` carries its ratification source in an adjacent comment block. **Standing consequence:** if Phase 47/48 moves residency to the locked canonical scaled contract (`r'` with `u = t/T`), that constant goes stale and must be re-ratified under the same D-12 discipline — and any `S_H` already computed in the raw frame is invalidated (`H' = D·H`). Do not let a `Complete` checkbox on CONF-01 stand in for this qualification when Phase 51 checks EVAL-01 precondition (ii).
- **Pre-existing suite failures, NOT introduced by Phase 46 (2026-07-28).** `pytest tests/ -q` reports 14 failures in this worktree: 7 in `tests/phase43/test_verdict_grounding.py`, 2 in `test_verify_gate.py`, 2 in `test_pilot_calibration.py`, 1 in `test_smoke.py`, 2 in `tests/watchdog/test_global_packaging.py`. Cause: `.planning/phases/` now holds only phase 46 (the phase-43 artifacts those tests read were archived at v2.0 close), plus gitignored `runs/` being present here — its presence flips those tests from *skip* to *fail*. Verified by A/B in a throwaway worktree at `fe3d45de`: identical failure sets with and without plan 46-07's five changed files. Do not treat a red full suite as a Phase 46 regression.
- **Thin pre-existing timeout margin in `tests/phase42/test_signals.py`.** Three subprocess tests run at 92–105s against a 120s per-subprocess timeout. Plan 46-07 did not consume this margin (measured before/after), but an unrelated slowdown on a loaded machine could surface it as a flaky timeout. D-10 forbids escaping via a new cadence/chunking knob.
- CONF-01 D-09 STOP (2026-07-27, Plan 46-06) — **resolved, gap registers written.** The real-corpus target-frame probe returned VERDICT_AMBIGUOUS, not the clean D-08 VERDICT_TARGETS_ARE_SCALED. GAP-46-04 (commit `be0867ab`/`997c731b`) routed the confound repair to Phases 47/48; GAP-46-05 corrected that routing the same day after it deadlocked the milestone, moving the minimum repair + re-probe into Phase 46 as CONF-08. Plan 46-07 remains gated on 46-09's verdict — that gate is by design. Its Task-1 hard gate was repointed to `46-VERDICT-POSTREPAIR.md` (absence ⇒ BLOCKED), because the pre-repair `46-VERDICT.md` must never be used to ratify a frame; the gate's three-state logic is otherwise unchanged.
- **Repair discipline for CONF-08 (SCOPE-29 boundary):** the repair is defined by the canonical pipeline in `preprocess_trajectory`, not by which transform lowers the probe residual. The probe reports the *first* diverging step, so repairing permutation + COM/boost may surface `rotation_gauge` as the next one; that is a measurement to route, not a licence to iterate against the probe. The `D` scaling is excluded from the repair specifically because it is the raw-vs-scaled question CONF-01 must answer.
- **Branch-ref hygiene:** `milestone/v2.2` was created 2026-07-27 at `997c731b`, after plans 46-01..46-06 had already executed on `milestone/v2.1`. Tag `v2.1` (`f72eaabd`) is the durable v2.1 record; `milestone/v2.1` still points at `997c731b` and carries 23 v2.2 commits, so owner-controlled master integration should target the **tag**, not the branch ref.

## Session Continuity

**Resume file:** .planning/phases/65-probe-on-the-record-fit-harness/65-01-PLAN.md

Last session: 2026-10-29T02:09:10.856Z
Stopped at: Phase 65 planning complete: six plans in six waves, 15 tasks; independent plan check passed
Next action: Execute Phase 65 via $gsd-execute-phase 65, starting with 65-01-PLAN.md. Six plans and 15 tasks passed independent planning verification. Probe and smoke execution remain gated on their committed registrations; no run has started. Any roadmap pivot, merge to master or protected push remains owner-controlled. All computation is on this Mac.

## Operator Next Steps

- ~~Finish `trainex-r4`~~ — done 2026-10-07: consolidated (`53b7c008`) and ruled under owner delegation (`trainex-r4-ruling.md`, `c4bea18a`; Key Decision in `PROJECT.md`). The four disputes were settled by making the next run the corrected control with an observe-only guard and plateau handoff, Adam-only, on seeds 42, 41 and 43.
- ~~Open the next milestone~~ — v2.4 Stage-0 Feasibility Checkpoint started 2026-10-09 (`0b400dfa`; branch `milestone/v2.4`). It keeps the ruling's order of work and adds the learnability ladder in front of the corrected control.
- ~~Re-examine v2.4~~ — done 2026-10-11: the owner approved the ten amendments ("go"), which are folded into REQUIREMENTS/ROADMAP/PROJECT (`2026-10-11-v2.4-feasibility-amendments.md`).
- ~~Plan Phase 59~~ — planned 2026-10-12 (10 plans, 5 waves; plan checker passed).
- ~~Execute Phase 59~~ — done and verified 2026-10-17 (10/10 plans; `59-VERIFICATION.md` 6/6 success criteria; Gate G1 proceed). Owner page: `59-FINDINGS.md`.
- ~~Plan Phase 60~~ — planned 2026-10-18 (23 plans, 22 waves; the third plan check found 0 blockers, and its 3 warnings were fixed in an owner-chosen targeted pass).
- ~~Execute Phase 60~~ — closed and verified 2026-10-23 (Gate G2 fired and the sweep found no rescue; Phases 61-63 skipped at G2; `60-FINDINGS.md`, `60-VERIFICATION.md`).
- ~~Discuss Phase 64~~ — done 2026-10-25 (`64-CONTEXT.md`, `d3fb9816`).
- ~~Plan and execute Phase 64~~ — done 2026-10-26: verdict `RETHINK-REPRESENTATION`; at checkpoint ① the owner decided `change-course` and left every charter row open; `64-VERIFICATION.md` PASS-WITH-OBSERVATIONS.
- ~~v2.4 milestone close~~ — archived 2026-10-26: audit `gaps_found` for the twelve skipped-phase requirements only, learnings extracted for Phases 59, 60 and 64, override closeout, local annotated tag `v2.4`.
- ~~Start v2.5~~ — started 2026-10-27 (`/gsd-new-milestone`): confirm the cause of the time-constant output in-house first, with the redesign in v2.6; `trainex-r5` is re-aimed at the redesign question (order A). The eight unranked candidate fixes are in `64-VERDICT.md`.
- **Owner decision, open: GAP-59-08** (`.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`).
  - **The finding.** The validation gate and the held-out evaluator compute energy error from finite-difference velocities on the 0.08 data grid. That grid gives 5–38% error even on Brutus's exact answers, so the `1e-5` exam cannot be passed as implemented.
  - **Recommendation.** Option A: autograd velocities, written in by a formal clarifying amendment.
  - **Scope.** It blocks any held-out spend, not v2.4. Phase 64 puts it on checkpoint ① beside the pass bars (`64-CONTEXT.md` D-10). v2.5 puts it to the owner in its yardstick work (charter row C-7).
- **Owner decisions carried forward** (FEAS-10 charter rows C-1..C-14 in `64-CHARTER.md`; checkpoint ① on 2026-10-26 left every row open; the v2.5 start decided C-12, C-13 and C-14):
  - ~~the project's purpose~~ — answered 2026-10-25: learning plus a proof of concept (verbatim in `64-CONTEXT.md` D-07);
  - the budget: how many months of computing on this Mac (rented or cloud GPU time is not an option; standing owner rule, `PROJECT.md` Constraints);
  - the pass bar per stage — the Stage-0 rows (C-2, C-4 to C-7) are set inside v2.5;
  - ~~approval to rewrite `PROJECT.md`'s "What This Is"~~ — approved 2026-10-27 (C-12 A, C-13 A) and applied at the v2.5 start; C-14 B (the twelve skipped v2.4 requirements are not carried forward).
- ~~Hand off `trainex-r4`~~ — done; two engagements recorded with Rule-20 pins in the delivery note.
- ~~Owner decision still open: where the v2.3 phase folders should live~~ — decided in the v2.4 proposal under owner delegation: they stay in `.planning/phases/` through v2.4; revisit at the v2.4 close.
- **Phase-folder placement after the v2.4 close.** The owner decided on 2026-10-26 that the v2.4 folders 59, 60 and 64 stay in `.planning/phases/`, because 18 code and test files hardcode their paths. The close ran with `--no-archive-phases`, so the v2.3 folders 53–58 also stayed in place; their placement was not separately revisited and remains open.
- **Owner-controlled integration (NOT performed by the agent):** any merge of `milestone/v2.3` or `milestone/v2.4` to master; pushing tags `v2.3` and `v2.4`.
- ~~v2.3 milestone close~~ — archived 2026-10-04 (verdict `rethink`).
- ~~Execute Plan 57-05 only after its precondition is checked.~~ Done 2026-10-03 (generation-7 terminal branch). The fresh complete GATE-04, final-R_ref production conformance, and `admit-run-window` receipt now pass; the next action is the explicit operator authorization before any smoke/band compute.
- **Keep checkpoint ④'s selection rule fixed.** Seed 42, then 41 and 43 only for structural ineligibility; no observed scientific metric may trigger fallback.
- **Keep checkpoint ⑤ owner-only.** The DIAG-06 go / adjust / rethink verdict remains downstream of RUN-04/05 and EVAL-02.
- ~~Execute Phase 44~~ — complete 2026-07-23 (qualified by `44-ERRATUM.md` 2026-07-24)
- ~~Adjudicate GAP-44-01~~ — RESOLVED-WITH-INSTRUCTION 2026-07-23 (owner option A: the physics gate is defined over the worst-case `max` per-trajectory ε_H; headline `max = 237.2086056078468`. See `.planning/phases/44-physics-gate-forensics/44-GAPS.md` and the updated `44-DIAGNOSIS.md`.)
- ~~Execute Phase 45~~ — complete 2026-07-24, `45-AUDIT.md` all ten checks PASS, package delivered
- ~~Adjudicate the five open gaps~~ — all five RESOLVED/DEFERRED 2026-07-24. GAP-45-03: per-stage PHYS-05 values are locked (option A). GAP-45-02: λ_E provenance unrecoverable, treated as drift, reverts to 0 (option C) → C-05 is a defect. GAP-45-04: mandate the invariant "no causal weight may be exactly zero", defer the number to the implementer with a recording obligation (option C). GAP-45-01: deferred to the conformance-fix phase, must resolve **before** any re-run (option C). GAP-44-02: erratum + mandatory re-derivation as a mapped requirement (option C). Index: `.planning/milestones/v2.1-GAPS.md`.
- ~~Frame the next milestone~~ — owner decision 2026-07-24: **conformance first**, then re-run, then tuning adjudication. Six inherited obligations enumerated in `v2.1-GAPS.md`.
- **Owner-controlled integration (NOT performed by the agent):** `--no-ff` merge of `milestone/v2.1` to master, archive under `milestones/v2.1-*`, tag `v2.1`. Closeout is committed on the branch and ready.
- **Provenance gap to close:** the returned research report does not identify which external agent produced it (landed as `trainex-r2-research-report.md`, not the convention's `<agent>-resolution.md`). Owner to confirm the agent/service so the delivery-note provenance record is complete.
- **Open the next milestone** — conformance-first roadmap; the six inherited obligations are the seed scope.
- **Spawn the verification-enforcement workstream** — separate concurrent session; charter at `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`, initial register contents ready in the conformance audit's C-01..C-08.
- Hygiene (non-blocking): `44-VALIDATION.md` remains `status: draft` / `nyquist_compliant: false`.

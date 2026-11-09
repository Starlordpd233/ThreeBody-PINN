---
phase: 69
phase_name: "Findings & Redesign Decision"
project: "Three-Body Physics-Informed LLM"
generated: "2026-11-08"
counts:
  decisions: 7
  lessons: 6
  patterns: 6
  surprises: 4
missing_artifacts:
  - "69-UAT.md"
---

# Phase 69 Learnings: Findings & Redesign Decision

Phase 69 synthesized all v2.5 diagnostic evidence (`DIAG-09`, `EXP-01` through `EXP-05`, and `YARD-01..03`), reconciled the historical v2.4 failed single-orbit fits against the successful Phase 67 locked-network controls, accounted for measured v2.5 compute and `SCOPE-49` dispositions, and recorded the owner's closing decisions for milestone v2.6. In two verbatim replies bound to the digest-pinned packet (`f55cd870`), the owner commissioned `trainex-r5` redesign research on the packet's focused question and selected Direction A (retaining the locked architecture as the supervised fit control while prioritizing the training recipe and physics pipeline). Closeout verification also remediated seven code-review findings in `verify_phase69.py` (expanding the Phase 69 test suite from 31 to 39 passing tests) and verified live 13/13 requirement traceability across Phases 65–69. Extracted from `69-01-PLAN.md`, `69-01-SUMMARY.md`, `69-02-PLAN.md`, `69-02-SUMMARY.md`, `69-03-PLAN.md`, `69-03-SUMMARY.md`, `69-FINDINGS.md`, `69-EVIDENCE.md`, `69-ACCOUNTING.md`, `69-CHECKPOINT.md`, `69-RULING.md`, `69-HANDOFF.md`, `69-REVIEW.md`, `69-VALIDATION.md`, `69-VERIFICATION.md`, and `STATE.md`. No UAT file exists for this phase.

## Decisions

### Owner selects Direction A: keep the locked architecture as the supervised control and prioritize training and physics
In Reply 2 (`sure goa head`, responding to the assistant's explicit offer to record Direction A after Reply 1 requested a long-term recommendation), the owner selected Direction A for v2.6: retain the current locked architecture (`12x256`, `first_omega_0=30`, raw `[tau, IC13]`) as the supervised fit control while repairing the training recipe and physics pipeline first.

**Rationale:** the locked architecture already achieved settled Tier 1 position fits on `1632/42` ($E = 0.041$), `851/42` ($E = 0.095$), and `1632/41` ($E = 0.035$) under the diagnostic recipe; keeping that demonstrated control lets v2.6 test whether single-orbit progress transfers into the repaired physics rung before considering architectural replacement.
**Source:** 69-RULING.md, 69-HANDOFF.md, 69-03-SUMMARY.md, STATE.md

### Owner commissions trainex-r5 redesign research under Order A on the packet's focused question
In Reply 1 (`for v2.6 direction, I'm not sure. which one would be better and benefit us more in the long term? for trainex-r5, sure we can authorize the redesign research.`), the owner authorized `trainex-r5` as redesign research under Order A, adopting by reference the packet's single proposed question: *"How should v2.6 retain the demonstrated single-orbit position fit while repairing the physics training and energy measurement, and what evidence should trigger a representation change before expanding to the 16-system family?"*

**Rationale:** `DIAG-09` retained the original hidden-state association and the locked architecture succeeded under the diagnostic recipe, so Order A routes `trainex-r5` to redesign research rather than reopening v2.4 diagnosis.
**Source:** 69-RULING.md, 69-CHECKPOINT.md, 69-HANDOFF.md, 69-03-SUMMARY.md

### Reconcile historical v2.4 failures against successful Phase 67 locked-network controls without claiming a single isolated cause
`69-FINDINGS.md` and `69-EVIDENCE.md` pair the historical v2.4 Tier-0 failures (`r1-1632` official $E = 1.1574$, `r1-851` official $E = 1.2375$) directly against the matched `EXP-03` `lr1e-4` locked-network controls (settled Tier 1 at $E = 0.0407$ and $E = 0.0955$, plus repeat seed `1632/41` at $E = 0.0349$) and classify all 10 recipe aspects as `checked-equivalent`, `checked-different`, or `source-unresolved`, leaving the single historical causal mechanism open.

**Rationale:** the old and new runs shared architecture, seed construction, targets, and loss, but differed simultaneously in optimizer schedule (cosine from $10^{-3}$ vs constant $10^{-4}$), gradient clipping, executed diagnostic polish, update budget, and scored-state selection, while archived initial-tensor and runtime identity remain unproved.
**Source:** 69-01-SUMMARY.md, 69-FINDINGS.md, 69-CONTEXT.md (D-04, D-05, D-06), 69-VERIFICATION.md

### Verify historical records against publication-time registrations, never later re-pinned bytes
`verify_phase69.py` validates each experiment record's captured `registration_sha256` against the registration blob at its original publication anchor commit (`df40671e` for `1632/42`, `23df087c` for `851/42`, `623f8df6` for `1632/41`, and `a686d26e` for historical v2.4 execution), and explicitly rejects substituting later re-pinned registration bytes.

**Rationale:** Phase 67 legitimately re-pinned harness-freeze digests during later experiments; verifying against publication-anchor bytes proves historical capture integrity without false refusals or retroactive mutation.
**Source:** 69-01-PLAN.md, 69-01-SUMMARY.md, 69-VERIFICATION.md (Truth 11)

### Include the committed Phase 68 yardstick capture in measured v2.5 compute while keeping timing bases separate
Under parent approval of the Plan 69-01 deviation, `build_cost` and `69-ACCOUNTING.md` report 129 timed published training/timing/metadata attempts (`107,626` UTC seconds) plus the committed Phase 68 yardstick capture (`0.594706` UTC seconds from `utc_started`/`utc_finished`) for 130 timed activities totaling `107,626.594706` UTC seconds (`29.90 hours`), while reporting the 125-record fit-wall total (`107,582.1065162036579550` seconds) and the yardstick's `elapsed_seconds` (`0.5945865410612896` seconds) as separate non-additive views.

**Rationale:** different timing bases (1-second UTC attempt timestamps, monotonic fit-wall durations, and nested sub-step segments) measure overlapping intervals and must never be summed together, while untimed activities (the `DIAG-09` probe, pre-claim refusals, and operator/development time) must remain explicitly `unknown` rather than zero.
**Source:** 69-01-SUMMARY.md, 69-02-SUMMARY.md, 69-VERIFICATION.md (Truth 9)

### Derive active v2.5 requirement traceability dynamically from live files while binding the phase marker to v2.5
`traceability_report` parses live `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` on every invocation without hardcoding the 13-requirement count, checks multiplicity before forming sets, verifies phase directory existence on disk, and (after closeout review `CR-01`) requires the active milestone header to identify `v2.5`.

**Rationale:** dynamic derivation ensures any late `SCOPE-49` amendment is caught automatically, while pinning the `v2.5` milestone identifier prevents a future milestone's internally consistent planning files from falsely passing the Phase 69 closeout verifier.
**Source:** 69-01-PLAN.md, 69-03-PLAN.md, 69-REVIEW.md (CR-01)

### Route all v2.6 obligations and blockers explicitly without executing them in Phase 69
`69-HANDOFF.md` carries forward the commissioned `trainex-r5` question, Direction A, Phase 68's C-7 Option A autograd routes (`ROUT-68-01..05`), C-11 evaluation rewrite, open companion bars (C-2, C-4, C-5, C-6), the four named physics-pipeline defects (single-anchor physics calculation, IC reduction over selected slots, $10^4\text{--}10^6$ IC/physics gradient imbalance, and unreachable production L-BFGS stage kept distinct from Phase 60's executed diagnostic polish), and blocked Stage 1+ / `PLAT-01..07`.

**Rationale:** Phase 69 is a synthesis and decision phase (`SCOPE-45..49`); assembling `trainex-r5` or editing specs/code belongs strictly to authorized v2.6 workflows.
**Source:** 69-HANDOFF.md, 69-03-PLAN.md, 69-03-SUMMARY.md

---

## Lessons

### Retrospective recipe comparisons with multiple simultaneous changes prove learnability but do not isolate a historical cause
Comparing the failed v2.4 `r1-1632` and `r1-851` runs against the successful `EXP-03` `lr1e-4` controls decisively refutes the claim that the locked `12x256` SIREN cannot represent single Stage-0 orbits, yet cannot isolate whether the $10^{-3}$ cosine start, median gradient clipping, diagnostic polish, step count, or checkpoint selection caused the historical collapse.

**Context:** reconciling v2.4 Phase 60 records with v2.5 Phase 67 `EXP-03` controls in `69-FINDINGS.md` and `69-EVIDENCE.md`.
**Source:** 69-FINDINGS.md, 69-CHECKPOINT.md, 69-CONTEXT.md (D-05, D-06)

### Narrative tables can swap repeat-case columns unless joins use explicit (experiment, case, system, seed, arm) keys
In Phase 67's narrative summary of `EXP-03`, the relative effect values `39.16428044173176` (belonging to `repeat-1632-s41`, $1632$ seed $41$) and `15.376889578229147` (belonging to `repeat-851-s42`, $851$ seed $42$) were swapped across repeat columns; joining directly against `evidence/exp03/review.json` by full `(experiment, case, system, seed, arm)` keys caught and corrected the attribution in `69-evidence.json` and `69-EVIDENCE.md` without altering the historical Phase 67 file.

**Context:** building the keyed experiment inventory in Task 69-01-02.
**Source:** 69-01-PLAN.md (Task 2), 69-01-SUMMARY.md, 69-VERIFICATION.md (Truth 7)

### Saved research missed the nested provenance timing inside yardstick-audit.json
`69-RESEARCH.md` and `69-01-PLAN.md` initially assumed that Phase 68's `yardstick-audit.json` recorded no duration, but inspecting the committed file at `.planning/phases/68-yardstick/evidence/yardstick-audit.json:187,195-196` revealed `provenance.elapsed_seconds = 0.5945865410612896` alongside `utc_started` and `utc_finished` (`0.594706` UTC seconds).

**Context:** auditing all v2.5 measured activities during Task 69-01-02 (`Deviations from Plan`).
**Source:** 69-01-SUMMARY.md

### Naive Markdown and JSON parsing in verifiers can accept indented duplicates, fenced examples, CRLF hash drift and repeated JSON keys
During Phase 69 closeout code review (`69-REVIEW.md`), adversarial in-memory probes against `verify_phase69.py` showed that column-zero regexes missed two-space-indented duplicate requirement definitions and fenced `md` blocks (`CR-02`), `Path.read_text()` normalized CRLF line endings before hashing live files (`WR-02`), and plain `json.loads()` silently kept only the last value when an inventory JSON contained duplicate keys (`WR-03`).

**Context:** remediating `CR-01..04` and `WR-01..03` in `verify_phase69.py` during Plan 69-03 closeout.
**Source:** 69-REVIEW.md, 69-03-SUMMARY.md

### Incomplete attempt claims without a published record.json are a valid failure shape that accounting must retain
`diagnostic_fit.py` writes `attempt.json` first and marks it `incomplete` if setup or the worker fails before publishing `record.json`. `verify_phase69.py` initially opened `record.json` unconditionally for every non-probe attempt, which aborted `build_cost` on valid claim-only incomplete attempts (`CR-04`).

**Context:** fixing `build_cost` in `verify_phase69.py` so claim-only incomplete attempts retain their UTC interval and mark fit-wall unknown while published claims still require `record.json`.
**Source:** 69-REVIEW.md (CR-04)

### A two-turn owner checkpoint requires preserving each verbatim reply and its exact authority scope chronologically
At the Phase 69 closing checkpoint, the owner first authorized `trainex-r5` while asking which v2.6 direction would benefit the project more in the long term (Reply 1), and then approved Direction A after receiving the assistant's recommendation (Reply 2). Recording both verbatim quotes in chronological order with separate disposition tables kept the research commission anchored to Reply 1 and the direction choice anchored to Reply 2.

**Context:** executing the blocking-human checkpoint in Plan 69-03 (`69-RULING.md`).
**Source:** 69-RULING.md, 69-03-SUMMARY.md, 69-VERIFICATION.md (Truths 16, 17, 19)

---

## Patterns

### Publication-anchor registration verification via git show at the introducing commit
Load historical registration blobs via `git show <publication_commit>:<repo_rel_path>` using subprocess argument arrays and repository-containment checks, and verify that the run record's `registration_sha256` matches the publication-time bytes while rejecting current re-pinned bytes when substituted.

**When to use:** cross-phase synthesis verifiers that audit records produced across multiple harness-freeze re-pins.
**Source:** 69-01-PLAN.md, 69-01-SUMMARY.md, 69-VERIFICATION.md

### Keyed multi-dimensional identity joins with strict duplicate-key JSON loading
Index and join every reviewed experiment outcome by its full `(experiment, case, system, seed, arm, window, state, metric_route)` tuple after verifying the as-captured registration's `configured_length` and velocity route (`CR-03`), and load JSON inventories with an `object_pairs_hook` that raises on any repeated key at any nesting depth (`WR-03`).

**When to use:** building and verifying machine-checked scientific evidence inventories from multi-arm experiment matrices.
**Source:** 69-01-PLAN.md, 69-REVIEW.md (CR-03, WR-03)

### Multi-view Decimal compute accounting with explicit unknown-duration categories
Compute all duration sums in `Decimal` over deduplicated activity identities, reporting UTC attempt intervals (`107,626.594706` s across 130 timed activities) separately from monotonic fit-wall durations (`107,582.1065162036579550` s across 125 fit records), validating every non-null timestamp endpoint (`WR-01`), and keeping untimed activities (`DIAG-09` probe, pre-claim refusals, operator/dev work) explicitly labelled `unknown`.

**When to use:** milestone compute accounting when artifacts record multiple overlapping timing granularities and some activities lack wall timestamps.
**Source:** 69-01-PLAN.md, 69-01-SUMMARY.md, 69-ACCOUNTING.md, 69-REVIEW.md (WR-01)

### Dynamic live-source traceability verification with fence stripping and raw-byte SHA-256
Read `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` once via `read_bytes()`, compute SHA-256 over the raw on-disk bytes (`WR-02`), strip fenced code blocks before regex matching (`CR-02`), count all indented definitions, traceability rows, and roadmap mappings before constructing sets, and verify 1-to-1 phase assignment and on-disk phase directory existence.

**When to use:** phase and milestone closeout traceability gates (`VER-22`, `VER-23`).
**Source:** 69-01-PLAN.md (Task 3), 69-03-PLAN.md (Task 3), 69-REVIEW.md (CR-01, CR-02, WR-02)

### Digest-bound closing decision packet with separate technical judgment review
Pin the exact SHA-256 digests of `69-FINDINGS.md`, `69-EVIDENCE.md`, `69-ACCOUNTING.md`, and `evidence/69-evidence.json` inside `69-CHECKPOINT.md`, record an explicit technical judgment review against the spec prohibitions (scientific overclaim, omission of adverse/unsettled results or cost unknowns, inferred owner authority), and bind the owner's subsequent reply in `69-RULING.md` to the packet commit and all five component hashes.

**When to use:** presenting synthesis findings and redesign options at a blocking owner checkpoint.
**Source:** 69-02-PLAN.md, 69-CHECKPOINT.md, 69-RULING.md

### Chronological multi-reply owner ruling and obligation handoff ledger
When an owner replies to part of a checkpoint and asks a clarifying question before deciding the remaining item, record `Reply 1` and `Reply 2` in separate `owner-quote` blocks with a per-reply reading table, then emit a standalone `69-HANDOFF.md` mapping every decided route, open charter bar, and named technical defect into the next milestone.

**When to use:** multi-part owner checkpoints at milestone boundaries.
**Source:** 69-RULING.md, 69-HANDOFF.md, 69-03-SUMMARY.md

---

## Surprises

### The exact v2.4 locked architecture (12x256, omega_0=30) reaches settled Tier 1 on both historical failed systems under the diagnostic recipe
Whereas all seven v2.4 Phase 60 arms collapsed to time-constant mean predictors (Tier 0, $E = 1.1574$ on `1632` and $1.2375$ on `851`), the exact same 12-layer, width-256, `first_omega_0=30`, raw `[tau, IC13]` architecture in Phase 67's `EXP-03` `lr1e-4` controls achieved settled Tier 1 position fits on `1632/42` ($E = 0.04069$), `851/42` ($E = 0.09550$), and `1632/41` ($E = 0.03492$) under constant Adam $10^{-4}$ without gradient clipping or polish.

**Impact:** overturned the suspicion that the 12-layer SIREN architecture was inherently incapable of fitting single Stage-0 orbits and shifted v2.6 to a recipe-and-physics-first redesign (Direction A) using the locked network as the supervised control.
**Source:** 69-FINDINGS.md, 69-01-SUMMARY.md, 69-CHECKPOINT.md

### Phase 67's narrative findings had swapped the repeat-851-s42 and repeat-1632-s41 effect columns in EXP-03
When `verify_phase69.py` joined `evidence/exp03/review.json` by explicit case and system/seed keys, it revealed that the narrative table in Phase 67 had transposed the two repeat-case relative effects (`39.16428044173176` for `1632/41` vs `15.376889578229147` for `851/42`).

**Impact:** validated the decision to drive Phase 69 synthesis strictly from keyed raw JSON records and review files rather than copying earlier narrative markdown tables.
**Source:** 69-01-PLAN.md (Task 2), 69-01-SUMMARY.md, 69-VERIFICATION.md (Truth 7)

### Code review uncovered seven fail-open parser and accounting edge cases despite 31 passing tests
Even with 31 focused unit tests passing in Plan 69-01, the Plan 69-03 code review (`69-REVIEW.md`) found four critical and three warning defects in `verify_phase69.py` (accepting non-`v2.5` milestones, ignoring indented duplicate definitions or fenced markdown blocks, dropping window/route checks on review joins, crashing on claim-only incomplete attempts, ignoring malformed timestamps when the partner timestamp was `None`, normalizing CRLF before hashing, and allowing duplicate JSON keys).

**Impact:** all seven edge cases were fixed and locked down with 8 new regression tests (39 total tests passing) before final phase verification.
**Source:** 69-REVIEW.md, 69-03-SUMMARY.md, 69-VERIFICATION.md

### Measured v2.5 execution totaled 29.90 hours across 130 timed activities (129 published attempts plus one yardstick capture)
Summing all deduplicated timed activities across Phases 65–68 yielded `107,626.594706` UTC seconds (`29.90 hours`): `3` s for Phase 65 smoke (1 attempt), `5,725` s for Phase 66 science (3 attempts), `25` s for Phase 66 timing (1 attempt), `100,882` s for Phase 67 science (60 attempts), `987` s for Phase 67 timing (60 attempts), `4` s for Phase 67 metadata (4 attempts), and `0.594706` s for the Phase 68 yardstick capture (1 activity).

**Impact:** gave the owner an exact, re-derivable machine-hour total on this Mac alongside explicit boundaries for untimed probe, refusal, and development work.
**Source:** 69-01-SUMMARY.md, 69-02-SUMMARY.md, 69-FINDINGS.md, 69-VERIFICATION.md


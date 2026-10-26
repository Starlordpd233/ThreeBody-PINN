# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Codebase Cleanup

**Shipped:** 2026-03-20
**Phases:** 4 | **Plans:** 10 | **Sessions:** 3

### What Was Built
- Consolidated IC folders from 4 to 2 (removed duplicate gold IC folders)
- Externalized raw ICs via `IC_RAW_DIR` environment variable
- Added 184-ID gold subset exclusion for standard quasi-random configurations
- Removed legacy directories (`old_templates/`, `brutus_simulation_documentation/`) and build artifacts
- Fixed all stale code imports, documentation references, and agent instruction file drift

### What Worked
- Strict phase ordering (code → docs → deletion) prevented broken references
- Wave-based parallelization of independent plans within phases
- Verification agents caught stale references that phase-level verifiers missed (Phase 4 gap closure)
- Archiving milestone artifacts kept ROADMAP.md and REQUIREMENTS.md at constant size

### What Was Inefficient
- Phase 4 (stale reference fixes) shouldn't have been needed — Phase 1 verifiers should have caught renamed file references in docs and agent files
- Agent instruction file drift (AGENTS.md diverging from CLAUDE.md) happened because Section 3.2 was updated in 3 of 4 files during Phase 2

### Patterns Established
- Phase ordering: code rewrites → documentation → destructive deletion (strict dependency)
- Agent instruction files must be updated identically (all 4 files, same section)
- Verification agents run after phase completion to catch cross-file reference drift
- Milestone archival: roadmap + requirements → `milestones/v{X}-*.md`, originals collapsed/deleted

### Key Lessons
1. Grep-based verification should run across ALL file types (code, docs, agent files) during phase verification, not just code
2. When renaming files, track both import references AND documentation filename mentions separately
3. Agent instruction files with duplicated sections (like Section 3.2) are a maintenance risk — one missed update creates drift

### Cost Observations
- Model mix: primarily sonnet (planning/execution), opus used for verification agents
- Sessions: 3 (spread across 2026-03-18 to 2026-03-20)
- Notable: 10 plans executed with zero regressions; Phase 4 was the only "rework" and it was pre-planned gap closure

---

## Milestone: v1.4 — Resolving 01 Architecture and Physics Foundations

**Shipped:** 2026-06-09
**Phases:** 8 | **Plans:** 26 | **Tasks:** 65

### What Was Built
- Evidence-backed adjudication and STOP-gap governance for every Issue 01 decision
- Coherent input/output, frame/gauge, sampling, physics/loss, architecture, and normalization contracts
- Five executable acceptance probes with recorded evidence and full requirement traceability
- FUT-01 implementation-divergence and FUT-05 author-comment handoffs
- A presentation-preserving cleanup pass with all milestone gates green

### What Worked
- The ledger lifecycle prevented `FIX_APPLIED` from being mistaken for completion
- Dependency-scoped STOP gaps allowed independent work to continue without inventing semantic decisions
- Phase-local verification plus the final milestone audit caught missing validation metadata and handoff links
- Keeping live `pinn/` code outside the grounding set prevented v1.3 assumptions from contaminating the v1.4 specs

### What Was Inefficient
- Several closure artifacts required late repair because plan-count and validation heuristics were not checked early enough
- Phase 20.5 naming and summary conventions needed remediation before GSD could resolve the phase correctly
- The generated milestone accomplishment list required manual consolidation because summary metadata was inconsistent across phases

### Patterns Established
- Candidate verdict sources are evidence, not authority
- Semantic and process-schema silence triggers the STOP protocol
- Acceptance checks must include executable evidence when the contract is empirically consequential
- Completed milestone phase directories move intact to `.planning/milestones/v{version}-phases/`

### Key Lessons
1. Validate GSD artifact naming and summary discovery at phase start, not only at milestone close.
2. Record acceptance commands, stdout, hashes, and pass criteria together so closure remains reproducible.
3. Keep future implementation divergence explicit and forward-pointing rather than treating old code as specification evidence.

### Cost Observations
- Model mix: not captured reliably
- Sessions: not captured reliably
- Notable: 198 branch commits produced 32/32 satisfied requirements, 8/8 verified phases, and 25/25 resolved STOP gaps.

---

## Milestone: v1.5 — Resolving 02 Data Pipeline and Validation

**Shipped:** 2026-06-17
**Phases:** 8 | **Plans:** 27

### What Was Built
- Research package that opened the external resolution-doc gate; empirical dataset verification with re-derivable probes (DATA-01..07, including a 70-file base-hierarchical rerun for DATA-05)
- Evidence-packet / EVID-10 root-cause adjudication machinery and the re-verification issue ledger; SCS-threshold, D=6.694, and M11/M12 conflicts adjudicated at root cause
- Locked DataLoader ingestion/selection contracts and sampling/precision/global-scale contracts in `ctl_instruction.md` / `pinn_architecture.md`
- Canonical SCS/SASD/IPR/PSC validation-metric contracts with training-loop usage deferred to doc-03
- Executed the 13-check acceptance suite (G1–G8 gate PASS), closed the 19-row ledger, reconciled SI dispositions, and produced the two-artifact FUT-01 handoff

### What Worked
- The v1.4 adjudication machinery (evidence packets, EVID-10, ledger lifecycle, STOP protocol) carried over cleanly and kept every decision grounded
- Running empirical verification (Phase 24) in parallel with the external research gate compressed the critical path
- The G1–G8 milestone-closure gate with fresh re-execution caught reconciliation drift (unchecked requirement checkboxes, stale traceability rows) before archive

### What Was Inefficient
- The milestone audit found unchecked DATA/PIPE checkboxes and stale Phase-24.5-gated traceability rows that should have been flipped at each phase close, not at the milestone audit
- Four phases (24, 25, 27, 28) lacked a phase-level VERIFICATION.md; the issue ledger carried verification, but this required an explicit audit interpretation
- The v1.5 learnings extraction (commit 01274c6) covered only phases 26-29; the phases 23-25 learnings and the audit file were left in a stash and had to be recovered at archive
- A concurrent-session phase-dir move staged probe-output files that the `outputs/*` policy blocks, stalling its commit until a coordinated takeover

### Patterns Established
- Candidate verdict sources remain evidence, not authority; the resolution doc was transcribed only where it survived empirical and first-principles checks
- Provisional thresholds (VAL-02/03/04) land with an explicit FUT-01/doc-03 recalibration forward-reference rather than blocking the milestone
- Gold is final in shape (117 validatable + 67 permanent-absent); the promotion cascade is a FUT-01 data-generation dependency, not a v1.5 closure blocker

### Key Lessons
1. Flip requirement checkboxes and advance traceability rows at each phase close, not deferred to the milestone audit.
2. A milestone learnings extraction must cover all phases in one pass, or the remainder lands in scratch and must be recovered at archive.
3. When two sessions share a worktree, a pre-commit hook rejection (e.g., `outputs/*` policy) can stall one agent indefinitely — serialize commits via the `agent-commit` lock and coordinate takeovers explicitly.

### Cost Observations
- Model mix: not captured reliably
- Sessions: many (v1.5 spanned 2026-06-10 to 2026-06-17 with concurrent sessions)
- Notable: 36/36 requirements, 8/8 phases, G1–G8 gate PASS, 10/10 STOP gaps resolved; audit verdict `tech_debt` with all 3 non-blocking items closed at archive.

---

## Milestone: v1.6 — Resolving 03 Curriculum and Training Loop

**Shipped:** 2026-07-02
**Phases:** 7 | **Plans:** 30

### What Was Built
- Repo-blind ERW research package (master + prompt + companions + commit-pinned specs/snapshots) that opened the external resolution-doc gate; PKG-07 claims register; read-only PKG-08 characterizations
- Resolution-doc readiness gate (READY-WITH-CAVEATS: 18/18 findings covered, 0 v1.5-fact contradictions, 0 SCOPE-12 violations, 12 caveats routed)
- Evidence-packet / EVID-15 root-cause adjudication of the headline conflicts (D-04 causal mode, D-05 s_min frame, D-06 epsilon strategy, M14 gradient clipping) and reconciliation of issue-03's `D = 6.694` against the v1.5-locked raw-mass `D ≈ 4.6416`
- Curriculum-stage (CURR-01..05), training-loop/batch-construction (LOOP-01..08), and loss/energy-weight (LOSS-01..04) contracts transcribed into `ctl_instruction.md` / `pinn_architecture.md`
- 26/26 acceptance probes PASS, issue ledger driven to terminal 18/18 VERIFIED, four-ID SI reconciliation, and the FUT-01/FUT-04 handoff (`36-CODE-DIVERGENCE.md`)

### What Worked
- The v1.4/v1.5 adjudication machinery (evidence packets, verdict set, ledger lifecycle, STOP protocol) carried over cleanly for a third milestone
- Specwork-only scoping (SCOPE-13/14/15) kept the milestone bounded: verbatim audit pseudocode transcribed as normative contracts, implementation explicitly routed to the trainex track
- Owner-routed decisions (D-04/D-05/D-06) were surfaced and held as `defer-with-blocker` until the owner ratified them, never invented — 10/10 STOP gaps resolved with instruction

### What Was Inefficient
- The milestone-closure relay (audit → milestone-summary → extract-learnings → complete-milestone) ran as concurrent sessions in one shared worktree; the final agent nearly took over the still-running middle stage on a stale liveness read, and only a Write-guard + a fresh quiescence re-check prevented a shared-index race
- `gsd-tools milestone.complete` (a mutating verb) corrupted the `current_phase` frontmatter (`36` → `6`) and had to be hand-repaired after diffing STATE.md
- Requirement *description* wording (LOOP-03/04/06, LOSS-02/03) and ROADMAP per-phase plan checkboxes were left in pre-adjudication/stale form and surfaced only at the milestone audit

### Patterns Established
- Multi-agent milestone closure via the cross-session watchdog relay, with the final agent (complete-milestone) waiting on the middle stages rather than racing them
- Provisional / owner-pending contract parameters land with an explicit GAP reference (GAP-33-01/02/03) and FUT routing rather than blocking the milestone
- `/gsd-extract-learnings` is phase-scoped (`NN-LEARNINGS.md`); a milestone-level `LESSONS-LEARNED.md` is not a standard output and closure must not gate on it

### Key Lessons
1. In a shared worktree with a multi-agent closure relay, the final agent MUST verify quiescence (no recent `.planning` writes + the middle stage's artifacts committed, not dangling) before acting — a stale liveness snapshot nearly caused a shared-index race.
2. Diff STATE.md (and any file a mutating `gsd-tools` verb touches) before committing — `milestone.complete` silently corrupted `current_phase` here.
3. Do not gate milestone closure on a milestone-level `LESSONS-LEARNED.md`: no standard workflow emits one, and v1.4 shipped without it; the RETROSPECTIVE + MILESTONE_SUMMARY carry the lessons.

### Cost Observations
- Model mix: not captured reliably
- Sessions: many concurrent (closure ran as a 4-stage relay across separate sessions in one worktree on 2026-07-02)
- Notable: 32/32 requirements, 7/7 phases verified, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED, 10/10 STOP gaps resolved; audit verdict `tech_debt`; closeout `override_closeout` (sole override: the deferred trainex-r1 todo). Master merge/publish deliberately NOT performed (repo governance: `master` is governance-only).

---

## Milestone: v2.0 — CTL-PINN Training Viability Slice

**Shipped:** 2026-07-23
**Phases:** 7 | **Plans:** 60

### What Was Built
- The project's first production code: the full Stage-0 mechanical training stack rebuilt from the locked specs — MPS/fp32 runtime + fp64-CPU reference (37), 14D SQR-SkipResNet-SIREN with COM projection, AD residuals, five-term loss (38), fail-closed admitted-data adapter with physical-key splits (39), Adam→L-BFGS curriculum loop with ADVANCE/RECOVER/HALT (40), config/checkpoint/exact-resume/guards/determinism (41), operator runbook + JSONL/TB monitoring (42)
- The acceptance machinery: five-rung verify ladder + fail-closed fresh marker, >30-min duration gate, real-data smoke with SIGTERM interrupt + exact resume, three-seed Stage-0 pilot with owner-ratified guard calibration, one-time receipt-bound held-out evaluator, receipt-grounded verdict backstop
- The honest answer: sole held-out gate **FAIL** (`ε_H = 237.21` vs ≤ 1e-5; `SCS = 2.375`; 1,500 trajectories); pilots mechanically clean but non-convergent; owner verdict **`adjust`** with a `pinn/STATUS.md` shipped/seam/deferred handoff

### What Worked
- Owner-carved seams (D1-p, D4-a, R-1/R-2, B-5) held safe defaults until their designed calibration moments and were all ratified on real evidence — the build analog of the STOP protocol worked end to end
- The verification culture transferred from specwork to build: the Phase 43 verifier reproduced the prior report's bypass probes rather than trusting closure summaries, and the five CR blockers were independently confirmed closed
- Rendering FAIL honestly: the gate, summary, verdict grounding test, and audit all agree on the failing numbers — no viability inference was laundered through healthy-looking validation

### What Was Inefficient
- Phase 38's completion was never recorded after GAP-38-01 resolved (2026-07-13): the ROADMAP checkbox, NET-01..05 requirement rows, and STATE counters stayed stale for ten days and had to be reconciled at close (commit 7567be24) — phase-close bookkeeping should happen in the same session as the gap resolution
- Verification-status staleness accumulated the same way: 41-VERIFICATION stayed `human_needed` after its human items were satisfied at Phase 43; 38-UAT stayed `partial` after its outstanding item passed
- Two Phase-39 debug-session records were left open (`diagnosed`/`investigating`) with no formal closure, surfacing only at the close-out artifact audit

### Patterns Established
- Build milestones close through the full chain: open-artifact audit (acknowledge-all with per-item annotations distinguishing stale-satisfied from genuinely-deferred) → milestone audit with integration checker → archive → evolution review
- One-time, budget-bound evaluation as a governance object: the held-out evaluator is exhausted by policy, and re-evaluation requires a new owner policy + evidence boundary, not a retry
- Threshold ratification via delegated calibration: agent runs the diagnostic, surfaces the band, owner ratifies the exact value (R-1 `1e11` from the warmup-spike diagnostic)

### Key Lessons
1. When a gap resolution un-holds a phase close, flip the phase's completion records (ROADMAP/REQUIREMENTS/STATE/UAT frontmatter) in that same session — stale "pending" claims in STATE compound into false milestone-close blockers.
2. Verification reports whose `human_needed` items are satisfied later need a dated status reconciliation note; otherwise every downstream audit re-litigates them.
3. A failing acceptance gate can still be a successful milestone: v2.0's definition of done was an honest verdict, and `adjust` grounded in a FAIL receipt is a stronger platform decision than an unexamined `go`.

### Cost Observations
- Model mix: not captured reliably
- Sessions: many (multi-wave watchdog-chain execution for Phase 43; concurrent docs/planning sessions at close)
- Notable: 42/42 requirements, 7/7 phases, audit `tech_debt` with zero blockers; closeout `override_closeout` (10 acknowledged deferrals incl. 3 integration warnings); held-out budget exhausted after 3 attempts (2 failed, 1 completed FAIL). Master merge deliberately NOT performed — user-controlled integration.

---

## Milestone: v2.1 — Physics-Gate Investigation & trainex-r2 Research Package

**Shipped:** 2026-07-24
**Phases:** 2 (44–45) | **Plans:** 9

### What Was Built
- A read-only forensic diagnosis of the v2.0 physics-gate FAIL from retained evidence only: the per-trajectory ε_H distribution over all 1,500 held-out trajectories (preserved `metrics.json`; evaluator NOT re-run), the five-term loss decomposition + ~3.7e9 warmup-spike attribution, and the three-seed 41/42/43 band — consolidated into `44-DIAGNOSIS.md` (≥4 hypothesis-ranked causes, remedy-abstinent), with a SHA-256 `manifest.json` making every quoted number re-derivable
- The trainex-r2 ERW package under `framework-specs/trainex-r2/`: commit-pinned document snapshots, 5 neutrally framed research questions + evaluation-policy question, a [FACT]/[HYP] claims register, and a delivery note — audited PASS (`45-AUDIT.md`, ten checks)
- A bounded Stage-0 conformance audit (C-01..C-08) that reframed the whole milestone: the executed pilot diverged from the locked specs in five verified respects, so the gate FAIL is not evidence about the design — issued as `44-ERRATUM.md`

### What Worked
- Scope discipline under a signed verdict: SCOPE-22..26 (no held-out evaluation, no new training, no spec edits, no PLAT-01..07, no remedy selection) held for all 9 plans; every spec-parameter suspicion became an ERW research question, not an edit
- The STOP-protocol spirit on a build-adjacent milestone: the diagnosis ranked hypotheses and abstained; the remedy stayed owner-routed and no physics-adjudication call was made inline
- Verify-what-was-executed paid off: auditing the returned report against the live repo (Route B / open-book, 6/6 claims confirmed) surfaced that the pilot never implemented the specs — the single most consequential finding of the milestone, and it came from conformance-checking rather than trusting the recipe

### What Was Inefficient
- Phase 45 shipped without a gsd-verifier `45-VERIFICATION.md` (the `45-AUDIT.md` ten-check record was substantively equivalent but formally asymmetric vs Phase 44); the PKG-09/10/11 checkboxes and SUMMARY `requirements:` frontmatter were reconciled at closeout (chain position 2), not in-phase
- `44-VALIDATION.md` remained `status: draft` / `nyquist_compliant: false` (pre-existing, non-blocking hygiene) through close
- The returned report landed as `trainex-r2-research-report.md` rather than the convention's `<agent>-resolution.md`; producer identity remains unconfirmed by owner

### Patterns Established
- Diagnose-then-hand-off as its own milestone shape: the package-first rhythm (v1.5/v1.6) applied to a build failure — characterize the failure re-derivably, package it for external research, and defer the remedy to the post-resolution milestone
- Conformance-before-tuning: when a returned research doc reasons about a recipe that did not run as specified, the verified divergences must be fixed and re-run before any tuning is adjudicated — the origin of the conformance-first v2.2 scope
- A diagnosis can be delivered *and* qualified: `44-ERRATUM.md` records that the DIAG-04 rankings are under-determined pending re-derivation against a conformant run (GAP-44-02), rather than silently retracting or over-trusting them

### Key Lessons
1. Verify what actually executed, not what the recipe says: the pilot's five conformance divergences (C-01..C-08) meant the physics-gate FAIL was never evidence about the design — a lesson that reorders the entire next milestone.
2. A forensic diagnosis over a non-conformant run is provisional by construction; mark the re-derivation obligation explicitly (erratum + mapped GAP) so the next milestone cannot skip it.
3. Read-only investigation milestones still need the full lifecycle stamp (verification artifact + checkbox/frontmatter reconciliation) or the close-out audit re-litigates delivered work as "gaps."

### Cost Observations
- Model mix: not captured reliably
- Sessions: several (Phase 44/45 execution inline on the data-bearing worktree; multi-position `v2-1-closeout` watchdog chain at close)
- Notable: 7/7 requirements delivered; 2/2 phases; package audited PASS (ten checks); milestone audit `gaps_found` by the strict 3-source gate (PKG-09/10/11 verification-gap over complete work), reconciled inline to 7/7. Master merge + tag push deliberately NOT performed — owner-controlled integration.

---

## Milestone: v2.2 — Stage-0 Conformance Repair & Valid Re-Run

**Closed incomplete:** 2026-08-17 (owner decision `stop-incomplete`)
**Phases:** 7 (46–52) | **Plans:** 38 (34 executed)

*Backfilled 2026-10-04: the v2.2 close recorded no retrospective section. Drawn only from the v2.2 archive and the v2.3 roadmap's own statements about v2.2.*

### What Was Built
- Repairs for all nine verified Stage-0 conformance divergences (C-01..C-09):
  - frame and gauge (Phases 46–47);
  - the `S_H` pipeline and `ε_H` wiring (Phase 47);
  - the loss math, including `R̄`, the clip, `λ_E`, and the `L_data` reduction (Phase 48).
- Gate-aligned instrumentation: per-trajectory `ε_H`/SCS validation receipts, per-term gradient statistics, and a preflight conformance gate with runtime invariants A/B and a divergence register (Phase 49).
- The first conformant Stage-0 re-run (Phase 50), which halted at invariant B at step 501 with `front_idx = 0`.
- The bounded 2026-08-17 residual-frame conformance audit, which attributed the halt to the locked architecture at initialization.

### What Worked
- Train-free checks before spending a run:
  - RG-02 was tested by a residual-on-stored-targets check with no training run, and the owner settled it from that check's measured evidence;
  - the 2026-08-17 audit characterized the architecture at initialization without data or an optimizer.
- Owner checkpoints at designed moments: the CONF-01 branch point, GAP-45-01's `L_data` reduction, and invariant-B `N`.
- Preserving the single held-out evaluation instead of spending it on a run known not to have trained.

### What Was Inefficient
- Phase 49's first verification found gaps (4/6), and the phase needed three remediation waves (49-07, 49-08, 49-09).
- Phase 50 used three band generations before the halt. The cause sat in the spec calibration itself, which no v2.2 phase was authorized to change (SCOPE-30).
- Moving the phase folders at the v2.3 start broke the `tests/phase50` path assumptions. This was found during v2.3 and fixed on 2026-10-04.

### Patterns Established
- Conformance-first: repair verified divergences and prove the repair before re-running or tuning.
- A preflight conformance gate and a machine-readable divergence register as run preconditions.
- Fail-closed, run-bound receipts for validation-side gate metrics.

### Key Lessons
1. A conformant implementation can still fail by design. Once the divergences were repaired, the remaining failure was a calibration mismatch between two independently locked spec sections.
2. Name the terminal branch before it is needed. v2.3 wrote this into its roadmap as "v2.2's lesson".
3. A gate at initialization can catch a saturated causal weighting before a run is spent. v2.3's GATE-04 demonstration is recorded as "the check that would have spared v2.2's generation-3 run".

### Cost Observations
- Model mix: not captured reliably.
- Sessions: many.
- Notable: 211 commits, 2026-07-25 → 2026-08-17. The milestone closed without MILESTONES.md or RETROSPECTIVE.md entries; both were backfilled on 2026-10-04.

---

## Milestone: v2.3 — Causal-Weight/SIREN-Scale Recipe Adjudication

**Closed:** 2026-10-04 on the declared terminal state (owner verdict `rethink`, 2026-10-03)
**Phases:** 6 (53–58) | **Plans:** 30

### What Was Built
- The four research-free VER-20 items codified in `pinn_architecture.md` (SPEC-02..05)
- The governed recalibration decision: a non-recommending packet, the `trainex-r3` ERW round with Rule-19 verification of both returned reports, and an owner-delegated ruling (`54-RULING.md`), written into §3.2 as a SCOPE-38 contract amendment (SPEC-01/06)
- INST-04, the architecture-only characterization probe, and GATE-04, a fail-closed train-free gate shown to BLOCK the pre-amendment recipe and to PASS the amended one with a governed `R_ref`
- Production-trainer conformance to the amended recipe (4096 rows in 16 bins, frozen-`R_ref` normalization, one frozen invariant-B monitor, frozen L-BFGS segments), a version-2 per-invocation run ledger, Git-retained run evidence with size/SHA-256 manifests, and a detached run launcher
- The Phase-58 verdict packet, with a frozen-monitor replay of the generation-7 stall

### What Worked
- Declaring the terminal state in the roadmap: when the front stalled, the milestone closed cleanly with the evaluation unspent and no pressure to tune
- Proving the gate refuses (Phase 56 SC5) made the GATE-04 PASS evidence rather than a no-op
- Gap discipline under repeated operational failure: each of generations 1–6 got an owner ruling and preserved evidence instead of a silent retry (GAP-57-02..12)
- The verifier failed closed after the terminal branch: re-admission of a new run window is refused

### What Was Inefficient
- Six of seven band generations ended for operational reasons (memory guard, interrupted smoke, sandbox block, operator stop, telemetry fix, silent process loss) before one produced a graded result; Phase 57 ran from 2026-09-08 to 2026-10-03
- Process-lifetime infrastructure arrived last: the detached launcher with retained output came only after generation 6 died with no recoverable cause
- GSD state tooling again mangled STATE.md at close (`milestone.complete` regressed `completed_phases` 6→3 and wiped the position block); restored from a snapshot and edited by hand
- Archive moves keep breaking hardcoded test paths (`tests/phase43`, `tests/phase50`); v2.3 left its phase folders in place rather than repeat it

### Patterns Established
- A roadmap-declared terminal state, carried explicitly by the phases that can reach it
- A train-free gate with a demonstrated refusal, required before any run is spent
- Per-invocation run ledgers plus exact-path Git retention with size/SHA-256 manifests for run evidence
- Detached, supervised launch for long runs (own session, retained output, exit record)

### Key Lessons
1. A train-free gate at initialization is necessary but not sufficient: GATE-04 passed and the front left the floor, yet it stalled at 2 under training. Initialization health does not establish front advance.
2. Settle run infrastructure (process lifetime, logging, memory bounds) before opening a single-look run window; operational losses cost more wall-clock time than the science.
3. Naming the failure branch in advance turns a negative result into a clean close instead of a drift.

### Cost Observations
- Model mix: not captured reliably
- Sessions: many (a multi-session run window across about four weeks)
- Notable: 172 commits, 2026-08-18 → 2026-10-03; the generation-7 window took 4 h 21 min (smoke 64 min, graded seed 42 194 min). Master merge and tag push deliberately NOT performed — owner-controlled integration.

---

## Milestone: v2.4 — Stage-0 Feasibility Checkpoint

**Closed:** 2026-10-26 on its pre-registered exit at Gate G2 (verdict `RETHINK-REPRESENTATION`; owner decision `change-course`, 2026-10-26)
**Phases:** 6 (59–64; 59, 60 and 64 executed, 61–63 skipped at G2, not failed) | **Plans:** 40

### What Was Built
- A feasibility scorecard in physical units, frozen with its decision rule before any rung ran, with the FEAS-01 scorer, one allowlisted reader that refuses held-out files, the Stage-0 census and panels, a read-only survey of all 12,023 training-split records, and two comparison points: the two-Kepler formula and a nearest-neighbour copy (Phase 59)
- DIAG-07's read-only experiments on generation 7's checkpoints, and Gate G1, which recorded "proceed" (Phase 59)
- INST-05, the learnability harness: the production network on one Stage-0 system at a time, the trainer's own losses, the frozen L-BFGS polish, a CPU float64 cross-check, a closed 42-arm catalog, a run protocol SHA-pinned to 33 modules, admission, a detached supervisor with governed pause and resume, and an independent evidence verifier (Phase 60)
- Rung 1 on three systems and the four-setting `first_omega_0` sweep: seven arms, 22.378 machine hours, all Tier 0, so G2 fired with no rescue (Phase 60)
- The owner-facing verdict and charter: a 365-entry numbers manifest re-derived from the committed weights, a regenerated figure, a verifier with an aggregate `final` mode, and the checkpoint ① ruling record (Phase 64)

### What Worked
- Freezing the ruler and every rung's rules before results: when every arm came back Tier 0, the label followed mechanically and nothing was re-set
- Gates that may skip phases: the G2 stop path recorded Phases 61–63 as skipped, not failed, and sent the milestone straight to the verdict without spending further runs
- Reading scores against comparison points: set beside the constant mean predictor, the Tier-0 results showed that the networks had learned only the average position
- Independent verification: Phase 60's verifier found the time-constant observation, and Phase 64's caught a wording error that 287 passing tests had not
- Branch plans that end cleanly ("branch not taken", `status: complete`) kept a 23-plan conditional phase legible

### What Was Inefficient
- The Phase 60 evidence verifier crashed on first real use twice (the sweep-curve and `rescore` checks), because its tests mocked the wrong shapes
- Phase 60 ran as 23 plans in 22 mostly sequential waves; its suite takes about 13 minutes against a 60 s estimate, and Phases 59 and 64 also missed their feedback-latency targets
- The pre-registered sweep varied only `first_omega_0`, so the records cannot separate a representation limit from an outcome of the fixed recipe
- GSD state tooling again mangled STATE.md at close (`milestone.complete` regressed `completed_phases` 3→2, set `percent` to 33 and erased Operator Next Steps); the file was restored from a snapshot and edited by hand
- Close-time coupling: 18 code and test files hardcode the phase-folder paths, and the Phase 64 verifier and two test modules read the live REQUIREMENTS.md and ROADMAP.md, so the close needed a path repair onto the archives

### Patterns Established
- A pre-registered ladder whose gates fix their consequences (skip, stop, go to the verdict) before any result
- A sealed run protocol plus admission: an arm starts only under a drift-free, SHA-pinned protocol
- Every quoted number is a labelled, sourced manifest entry, re-derived by a verifier that shares no code with the producer
- Owner answers enter code only through a strict ruling reader, with byte-equal quotes
- Taken and not-taken branch records for conditional plans

### Key Lessons
1. Read every score against a no-learning baseline: the constant mean predictor scored within 0.004 of every trained network, which turned "Tier 0" into "learned only the average".
2. A one-setting rescue sweep cannot separate a representation limit from a recipe outcome; a verdict built on it must say so beside its label.
3. Exercise every verifier mode on real artifacts before it gates anything; mocks of the wrong shape hide first-use crashes.
4. When code reads planning files by path, milestone archival needs a planned path repair.

### Cost Observations
- Model mix: not captured reliably (the Phase 60 executor SUMMARYs record their commits under Claude Sonnet 5.5)
- Sessions: many (detached multi-hour arms on 2026-10-21 to 2026-10-23, plus planning, owner-checkpoint and verification sessions)
- Notable: 234 commits, 2026-10-09 → 2026-10-26; 22.378 machine hours of training on this Mac across seven arms; no graded run and no held-out evaluation. Master merge and tag push deliberately NOT performed — owner-controlled integration.

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 3 | 4 | Established GSD workflow: strict phase ordering, wave parallelization, post-phase verification |
| v1.4 | not captured | 8 | Added evidence adjudication, STOP-gap governance, executable acceptance checks, and archived phase history |
| v1.5 | not captured | 8 | Extended adjudication to data-pipeline/validation contracts; empirical dataset verification in parallel with the research gate; G1–G8 milestone-closure gate |
| v1.6 | many (relay) | 7 | Third adjudication milestone (curriculum + training loop); specwork-only with implementation routed to trainex; multi-agent closure relay via cross-session watchdog |
| v2.0 | many (watchdog waves) | 7 | First build milestone (trainex track): production `pinn/` from specs, owner-carved seams ratified at designed moments, one-time budget-bound held-out evaluation, honest FAIL → `adjust` verdict |
| v2.1 | several (inline + closeout chain) | 2 | Diagnose-then-hand-off investigation: read-only forensics over retained artifacts + trainex-r2 ERW package; conformance audit reframed the FAIL as an assembly divergence, seeding conformance-first v2.2 |
| v2.2 | many | 7 | Conformance-first repair of nine verified divergences plus a preflight conformance gate; the first conformant Stage-0 re-run halted at initialization; closed `stop-incomplete` with the evaluation preserved |
| v2.3 | many (multi-session run window) | 6 | Recipe adjudication through the governed ERW channel, a SCOPE-38 contract amendment, and a train-free gate; first milestone to close on a roadmap-declared terminal state (`rethink`, evaluation preserved) |
| v2.4 | many (detached arms + owner checkpoints) | 6 (3 executed) | Feasibility ladder with pre-registered gates: scorecard frozen before any rung; the G2 stop path skipped Phases 61–63 and went straight to an owner verdict (`RETHINK-REPRESENTATION` → `change-course`) |

### Cumulative Quality

| Milestone | Plans | Verification Score | Regressions |
|-----------|-------|-------------------|-------------|
| v1.0 | 10 | 9/9 (Phase 4) | 0 |
| v1.4 | 26 | 32/32 requirements; 8/8 phases | 0 open at close |
| v1.5 | 27 | 36/36 requirements; 8/8 phases; G1–G8 gate PASS | 0 open at close |
| v1.6 | 30 | 32/32 requirements; 7/7 phases; 26/26 acceptance probes PASS; ledger 18/18 VERIFIED | 0 open at close |
| v2.0 | 60 | 42/42 requirements; 7/7 phases; integration 6/6 WIRED; held-out gate honestly FAIL | 0 open at close (10 acknowledged deferrals) |
| v2.1 | 9 | 7/7 requirements; 2/2 phases; integration 3/3 WIRED; package audited PASS (ten checks) | 0 open at close (6 obligations inherited by v2.2) |
| v2.2 | 38 (34 executed) | 20/24 requirements (2 closed incomplete, 2 not attempted); phases 46–49 verified; Phase 50 closed incomplete | 0 open gaps at close (4 obligations inherited by v2.3) |
| v2.3 | 30 | 12/15 requirements (2 closed incomplete, 1 not attempted); 6/6 phases; VER-21 15/15; GATE-04 PASS | 0 open gaps at close (GAP-56-02 deferred; 5 obligations inherited) |
| v2.4 | 40 | 12/24 requirements (12 skipped at G2, not failed); 3/3 executed phases verified; integration 4/4, 0 blockers; VER-22 24/24/24 | 0 blockers at close (GAP-59-08 and GAP-64-01 owner-routed; 14 charter rows open) |

### Top Lessons (Verified Across Milestones)

1. Strict phase dependency ordering (code → docs → deletion) prevents broken references
2. Post-phase verification agents catch what inline verifiers miss
3. Duplicated content across files (agent instruction sections) creates drift risk
4. Source-silent semantic decisions must stop for user instruction rather than being inferred
5. Executable acceptance evidence is part of the specification closure contract
6. Verify what actually executed against the spec before trusting any result derived from it — a failing gate over a non-conformant run is evidence about the assembly, not the design (v2.1)
7. Declare the failure branch before it is needed: a pre-named terminal state lets a negative result close cleanly and keeps a single-look evaluation unspent (v2.3)
8. Read every result against a no-learning baseline before calling it learning: a time-constant predictor can earn the same grade as a trained network (v2.4)

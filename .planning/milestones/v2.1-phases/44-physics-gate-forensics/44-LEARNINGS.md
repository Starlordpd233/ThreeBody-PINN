---
phase: 44
phase_name: "Physics-Gate Forensics"
project: "Three-Body Physics-Informed LLM"
generated: "2026-07-25"
counts:
  decisions: 8
  lessons: 8
  patterns: 7
  surprises: 6
missing_artifacts: []
---

# Phase 44 Learnings: Physics-Gate Forensics

Phase 44 is a read-only forensics phase diagnosing why the Stage-0 CTL-PINN physics gate failed on the held-out set (energy-conservation ε_H). Extracted from the Phase 44 artifacts: 44-01..05 PLAN/SUMMARY, 44-VERIFICATION, 44-UAT, 44-GAPS, 44-ERRATUM, 44-DIAGNOSIS, 44-PATTERNS. STATE.md was not consulted (it carries unrelated pending changes); no phase artifact was missing.

## Decisions

### Read-only forensics scope — no evaluator, no training, no spec edits
Phase 44 was scoped as pure read-only diagnosis (analysis scripts + JSON outputs + pinning manifest + 44-DIAGNOSIS.md). Explicit prohibitions: do not invoke `pinn.evaluate`, touch the held-out test split, regenerate `metrics.json`, execute/schedule training, edit specs, recommend/select a remedy, or decide the D-07 gate-statistic question.

**Rationale:** keep the phase verdict-neutral and within the v2.1 read-only-data boundary (SCOPE-22..26); a forensics phase must not smuggle a remedy or gate-statistic decision past governance.
**Source:** 44-all-PLAN (prohibitions/STRIDE), 44-VERIFICATION (Scope-Boundary Compliance), 44-UAT Test 7

### Remedy-abstinent diagnosis (≥4 ranked causes, no remedy)
The diagnosis must rank ≥4 candidate causes with supporting AND contradicting citations, explicitly abstain from remedy selection, and route source-silent adjudication calls to the gap register.

**Rationale:** ROADMAP success criteria 4–5 require a discriminating, honestly-evidenced diagnosis, not a recommendation; remedy selection belongs to a downstream milestone.
**Source:** 44-05-SUMMARY (Key content), 44-VERIFICATION (Goal Achievement), 44-DIAGNOSIS §5/§7

### Re-derivability is a hard gate (byte-identical regeneration)
All analysis outputs must regenerate byte-identical from pinned inputs; every input is SHA-256 + commit-hash pinned; JSON is deterministic (`sort_keys`, full-repr floats, no timestamps). Two consecutive runs at the same commit produce identical bytes.

**Rationale:** forensic claims must be independently re-derivable from frozen inputs to be admissible as evidence.
**Source:** 44-UAT Test 1, 44-PATTERNS (Shared Patterns), 44-VERIFICATION (Re-derivability Evidence)

### Fail-closed self-check assertions in every analysis script
Each script fails closed on missing/malformed records — a missing loss term is never imputed as zero; the 26-key schema and the exact step set {1..300} are asserted before computing; the peak tie-break is documented in the output.

**Rationale:** silent imputation would corrupt the forensic record; the script must refuse rather than guess.
**Source:** 44-all-PLAN (DIAG-02 must_haves), 44-PATTERNS (Shared Patterns: Fail-closed self-check assertions)

### GAP-44-01 resolved — worst-case max IS the held-out gate statistic
The max-vs-mean ε_H aggregation question (D-07, MUST-SURFACE) was recorded as a STOP-protocol gap and resolved by owner instruction (Option A, 2026-07-23): worst-case max IS the gate statistic; headline `max = 237.2086056078468`; mean (5.6222) and median (2.2327) remain distribution facts, not gate numbers. Spec codification deferred (SCOPE-24).

**Rationale:** max encodes a worst-case per-trajectory conservation guarantee; the choice was a source-silent physics/spec-intent adjudication the agent must surface, not decide.
**Source:** 44-GAPS GAP-44-01, 44-UAT Test 6, 44-DIAGNOSIS §2

### GAP-44-02 resolved — erratum now, mandatory re-derivation later (Option C)
Phase 44 stays closed; `44-ERRATUM.md` qualifies (does not correct) the DIAG-04 rankings as under-determined, because the executed Stage-0 run diverged from the locked specs in ≥5 verified respects. The next milestone carries an explicit, mapped requirement to re-derive the diagnosis from a conformant run, with an acceptance check — the condition on which Phase 44 is permitted to stay closed.

**Rationale:** re-ranking without a conformant run would substitute one under-determined inference for another; only a valid Stage-0 run can discriminate the candidate causes.
**Source:** 44-GAPS GAP-44-02, 44-ERRATUM (Standing — RESOLVED 2026-07-24)

### Fixed run order + pinned interpreter for all analyses
Fixed run order everywhere: `stage0-smoke`, `stage0-pilot-seed41/42/43`; pinned interpreter `~/miniforge3/envs/pinn-train/bin/python3` (Python 3.11.15, numpy 2.4.6) — bare `python3` is system 3.14.6 without numpy.

**Rationale:** deterministic ordering + a numpy-bearing interpreter are preconditions for byte-identical re-derivation.
**Source:** 44-all-PLAN (interfaces), 44-UAT Test 1

### stage0-smoke is a separate fourth trace, never pooled into seed statistics (D-10)
The smoke run is reported as its own trace and never pooled into the three-seed statistics; `tb/` event files are not parsed (all required DIAG-02 fields are present in `train.log.jsonl`).

**Rationale:** pooling a budget smoke run with pilot seeds would corrupt seed-band statistics; the decision and its reason are recorded in the output.
**Source:** 44-all-PLAN (DIAG-02 must_haves)

## Lessons

### The physics gate fails uniformly — all 1,500/1,500 held-out trajectories fail ε_H
The failure is population-wide, not outlier-driven: `min ≈ 0.97 >> 1e-5`. Under uniform failure the current FAIL verdict is invariant to the max-vs-mean statistic choice — which is exactly why the gate-statistic decision is about future semantics, not today's verdict.

**Context:** DIAG-01 distribution analysis over the full held-out set.
**Source:** 44-GAPS GAP-44-01 (math grounding), 44-DIAGNOSIS §2.1

### The angular-momentum loss term contributed zero gradient across all 300 steps in all four runs
`loss_angmom`'s λ-weight was 0.0 at every one of the 300 steps in all four runs — the angular-momentum term never contributed gradient signal. The PHYS-05 scheduled `lambda_phys` ramp was characterized per run from the data.

**Context:** DIAG-02 five-term loss decomposition.
**Source:** 44-all-PLAN (DIAG-02 must_haves), 44-DIAGNOSIS §3

### An executed-evaluator convention is not spec authority
`pinn/verification/gate_metrics.py`'s "worst-trajectory (maximum)" docstring documents what executed, not that max is the spec-intended gate statistic. Citing it as spec authority is an anti-pattern (RESEARCH §C / Pitfall 5) — it is the D-07 gap to route, not resolve.

**Context:** the central trap that made D-07 a MUST-SURFACE gap.
**Source:** 44-PATTERNS (diag01 Pattern Assignment, Anti-Pattern warning), 44-GAPS GAP-44-01

### A fail-closed self-check caught a path-resolution bug during development
`build_manifest.py` had a path bug (diag outputs under `evidence/`, not `evidence/evidence/`) caught by its own fail-closed guard before commit.

**Context:** 44-04 evidence manifest build.
**Source:** 44-04-SUMMARY (Deviations)

### A "27 vs 26 keys" off-by-one was mechanical, not a physics decision
The artifact carried 27 keys/step (the extra is the `event` discriminator), not the planned 26. The script asserts the 26 required keys are present and records the actual 27-key set, imputing nothing. Correctly classified as mechanical (recorded), not a semantic deviation.

**Context:** DIAG-02 schema verification.
**Source:** 44-02-SUMMARY (Deviations)

### Scope re-derivability to "consecutive re-runs at this commit"
`manifest.json`'s re-run differed only in its `git_head` provenance stamp because HEAD advanced two commits after 44-04 was committed; all 15 input SHA-256 hashes were unchanged. Documenting this scope prevents false re-derivability-failure alarms.

**Context:** 44-UAT re-derivation of the manifest.
**Source:** 44-UAT Test 1 (note)

### Surface metrics can disagree while the underlying numbers reproduce exactly
DIAG-03's first-vs-last trend (1/3 worsened) DISAGREES with 43-CALIBRATION's "2/3 worsened" purely because of direction definition (last-window step200→300 vs first-vs-last step100→300), yet the final-loss relative span `3.8224247683129153` reproduces 43-CALIBRATION exactly. The disagreement is a definition artifact, adjudicated neither way.

**Context:** DIAG-03 three-seed band characterization, cross-phase calibration anchor.
**Source:** 44-UAT Test 4

### Gap registers are written by the parent orchestrator, never subagents
Per governance, the parent session owns gap-register writes; subagents return findings to the parent, which decides whether something is a gap and logs it.

**Context:** STOP-protocol ownership rule applied throughout the phase.
**Source:** 44-GAPS (header note), 44-PATTERNS (44-GAPS.md assignment)

## Patterns

### SHA-256 + commit-hash input pinning with embedded provenance blocks
Each output JSON embeds `provenance = {"inputs": {<path>: <sha256>}, "interpreter_expected": "..."}`; `build_manifest.py` cross-checks all input hashes; re-derivation regenerates byte-identical output.

**When to use:** any forensic/analysis phase whose outputs must be admissible evidence.
**Source:** 44-PATTERNS (Shared Patterns), 44-all-PLAN (interfaces)

### Pinned self-checking analysis script (RESEARCH Pattern 1)
Stdlib `json`/`hashlib`/`subprocess` + numpy only; JSON `indent=2, sort_keys=True`, trailing newline; no CLI args; `REPO_ROOT = Path(__file__).resolve().parents[N]`; fail-closed assertions before computing.

**When to use:** deterministic, re-derivable analysis over committed data.
**Source:** 44-all-PLAN (44-04 interfaces), 44-PATTERNS (diag scripts Pattern Assignment)

### Verified-fact vs agent-hypothesis separation with explicit citations
44-DIAGNOSIS.md separates verified fact (cited to a JSON output) from agent hypothesis; every claim traces to a pinned, regenerable source.

**When to use:** any diagnosis report that must distinguish measurement from inference.
**Source:** 44-PATTERNS (Shared Patterns), 44-DIAGNOSIS (How to read this report)

### Gap-register field schema (CLAUDE.md STOP protocol), copied verbatim
The exact 11-field STOP-protocol schema, field order matching `43-GAPS.md` / CLAUDE.md — no field renamed, none omitted.

**When to use:** every new STOP-protocol gap entry, phase-local or milestone-wide.
**Source:** 44-PATTERNS (44-GAPS.md assignment)

### Deterministic JSON serialization idiom
`indent=2, sort_keys=True`, full-repr floats, no timestamps → two consecutive runs at the same commit produce byte-identical JSON.

**When to use:** any JSON output that must re-derive identically.
**Source:** 44-PATTERNS (Shared Patterns: JSON output idiom)

### Reuse a prior phase's evidence-README structure as an analog, noting divergences explicitly
`evidence/README.md` was modeled on the phase-43 pilot README, with the inline-block vs separate-JSON divergence (D-01) called out rather than silently copied.

**When to use:** authoring a new evidence/README against an existing structural analog.
**Source:** 44-PATTERNS (evidence/README.md assignment)

### Governance risks encoded as prohibitions + textual acceptance criteria, not STRIDE threats
Read-only local synthesis has no network/auth surface; the real risks (deciding D-07, recommending a remedy) are encoded as MUST-NOT prohibitions with textual acceptance criteria.

**When to use:** threat-modeling a read-only analysis phase.
**Source:** 44-all-PLAN (STRIDE Threat Register, Honest note)

## Surprises

### The diagnosis's premise was falsified AFTER delivery
Post-delivery verification of the returned trainex-r2 report (Route B / open-book) confirmed 6/6 repository-derived claims; a bounded conformance audit then found the executed Stage-0 training path diverged from the locked specs in ≥5 verified respects — meaning DIAG-04's candidate-cause rankings (built assuming spec compliance) are under-determined. This surfaced GAP-44-02 and produced `44-ERRATUM.md`.

**Impact:** a delivered, verified diagnosis had to be retroactively qualified; the phase's interpretive layer could not stand as-is.
**Source:** 44-GAPS GAP-44-02 (Task context), 44-ERRATUM

### The remedy for a falsified-premise diagnosis is to NOT re-rank
Counter-intuitively, the correct response was to record the DIAG-04 rankings as under-determined rather than re-rank them — re-ranking without a conformant run would substitute one under-determined inference for another. The only discriminator (a valid Stage-0 run) does not yet exist.

**Impact:** defined the Option C resolution and the mandatory re-derivation requirement carried to the next milestone.
**Source:** 44-ERRATUM (Standing), 44-GAPS GAP-44-02 (Resolution)

### No revision protocol exists for completed phase artifacts whose premise is later falsified
`docs/README.md` defines a supersession protocol for `docs/` review reports, but `44-DIAGNOSIS.md` is a `.planning/` phase artifact with no equivalent protocol; CLAUDE.md's STOP protocol governs gaps found *during* a phase, not retroactive qualification of a completed phase.

**Impact:** the retroactive-qualification route itself had to be surfaced as a gap and owner-decided (GAP-44-02).
**Source:** 44-GAPS GAP-44-02 (Source silence)

### max vs mean differ by ~42× on this population
The aggregation choice changes the gate number by ~42×. Today's uniform failure makes the verdict invariant, but the choice defines the gate's future semantics — worst-case per-trajectory guarantee vs population-typical drift.

**Impact:** elevated D-07 from a presentation detail to a consequential physics/spec-intent adjudication.
**Source:** 44-GAPS GAP-44-01 (math grounding)

### Held-out splits: smoke == seed42 (identical SHA-256), seed41/seed43 diverge
The smoke run's held-out split is byte-identical to seed42's, while the other seeds diverge — a non-obvious data artifact requiring a caveat that cross-seed magnitude spans different populations.

**Impact:** cross-seed comparisons in DIAG-03 required an explicit split-divergence caveat.
**Source:** 44-UAT Test 4

### The Phase 38 machinery-integrity control was cited, not recomputed
The Phase 38 overfit rung (ratio 1097.6107, ≥1e3 PASS) was flagged CITATION-NOT-COMPUTATION and never re-run, because Phase 44 is read-only (SCOPE-23).

**Impact:** the machinery-integrity control is referenced as evidence but cannot be refreshed within this phase's scope.
**Source:** 44-UAT Test 4

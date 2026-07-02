# Phase 31: Resolution Doc Readiness Verification — Research

**Researched:** 2026-06-20
**Domain:** Operational documentation-verification phase (the v1.5 Phase 24.5 analog; 0 requirement IDs)
**Confidence:** HIGH — every claim is grounded in an in-repo source (CONTEXT/SPEC/ROADMAP/REQUIREMENTS, the verified 24.5 analog, and a direct structural read of the subject doc). No external research was needed or performed.

## Summary

Phase 31 is a single-agent, read-and-check pass that produces two markdown deliverables — `31-READINESS-REPORT.md` (the gate verdict) and `31-RESOLUTION-MAP.md` (the navigation aid) — over a resolution doc that has already landed. It **adjudicates nothing**: it confirms coverage of 18 selected findings, confirms zero contradictions of v1.5-verified dataset facts, and confirms zero violations of locked v1.4/v1.5 conventions, then emits a `READY` / `READY-WITH-CAVEATS` / `NOT-READY` verdict by a fixed precedence. The entire deliverable schema is already fixed by the **verified** v1.5 Phase 24.5 analog (`24.5-PLAN.md`, `24.5-READINESS-REPORT.md`, `24.5-RESOLUTION-MAP.md`, all of which PASSED) — the planner's job is to adapt that schema to v1.6's 18-finding set and the subject doc's §0–§7 / §1.1–§1.18 structure. [VERIFIED: 31-SPEC.md, 31-CONTEXT.md, 24.5-* analog]

The subject document — `…/03-curriculum-and-training-loop/research_result/03-final-resolution.md`, **282 lines / 48,049 bytes**, landed in commit `49fb7958` (2026-06-20) and clean in the worktree — has a clean, line-range-citable structure: §0 method, §1.1–§1.18 one subsection per finding (each tagged with a verdict word in its heading), §2 claim matrix, §3 disagreement register, §4 gap register, §5 source-coverage checklist, §6 non-independence note, §7 deliverable index. This RESEARCH provides the **structural** line-range inventory (sections + titles + ranges only) that grounds the map's §1 section index — it does **not** assess which finding maps where, does **not** judge coverage, and does **not** pre-judge any verdict. Those four checks are EXECUTION work under the STOP protocol. [VERIFIED: direct read of 03-final-resolution.md; git log]

**Primary recommendation:** Plan a single plan / single wave (CONTEXT D-01) with 8 ordered tasks following CONTEXT D-08's data-dependency order (pre-exec gate → presence/structural → crosswalk → consistency → compliance → map → report → gate-decision), lifting the report and map section sets verbatim from the 24.5 analog and adapting them to 18 findings + §0–§7. No source-silent semantic decision exists (SPEC ambiguity 0.09); there is nothing for the planner to surface.

## Architectural Responsibility Map

> Phase 31 builds no software and crosses no application tier. The "tiers" here are the planning-artifact responsibilities the planner must keep separate.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Pre-exec gate (doc present + Phase 30 complete) | Verification-report (`31-READINESS-REPORT.md` §2) | STATE.md (read-only citation) | Gate is recorded as evidence, not enforced in code; Phase-30-complete is read from STATE, never written here |
| Four readiness checks (R2–R5) | Verification-report (`31-READINESS-REPORT.md` §3) | Map (R3 crosswalk is reused in the map) | Checks are authored judgments backed by tables; the crosswalk feeds the map's §2 |
| Finding→section navigation | Quick-reference map (`31-RESOLUTION-MAP.md`) | — | Map is the standalone navigation aid for Phase 32; consumes R3's mapping |
| Gate verdict + fix-routing | Verification-report (exec summary + gate decision) | STATE/ROADMAP (via gsd-tools handlers) | Verdict is derivable from the check tables; outcome recorded to STATE only through handlers |
| Gate-state record | gsd-tools STATE/ROADMAP handlers | — | STATE.md mutated only via handlers (anti-pattern 15); never direct Write/Edit |

## Phase Requirements

> Phase 31 is operational — **0 new requirement IDs** (ROADMAP §"Phase 31"). It *supports* downstream requirement families but introduces none. The table below records the support relationship the planner should preserve, not requirements Phase 31 satisfies directly.

| Supports (downstream) | Relationship | Research support |
|-----------------------|--------------|------------------|
| EVID-11..15 (Phase 32) | Phase 32 consumes `31-RESOLUTION-MAP.md` to begin evidence-packet construction; EVID-11 needs line-range citations into the doc | The map's citation guide + §1 section index supply the verbatim path, §/finding-ID anchors, and a concrete `…:START–END` example for EVID-11 (CONTEXT D-04; SPEC R6) |
| CURR-01..05, LOOP-01..08, LOSS-01..04 (Phases 33–35) | These contract phases transcribe verdicts the doc records; Phase 31 confirms each selected finding is *covered* so a verdict can later be assigned | The crosswalk (R3) over 18 findings; the 3 contract extras (CURR-01, CURR-02, LOOP-05) are explicitly in the 18-set (CONTEXT D-09) |
| VER-13..18 (Phase 36) | Acceptance/handoff; VER-18 reviews SI-* entries | Out of Phase 31's scope — listed only as the support chain (ROADMAP §"Phase 31") |

## Execution Approach (the task breakdown for the planner)

**Plan shape (CONTEXT D-01):** single plan `31-01-PLAN.md`, single wave. Phase 31 is a lightweight single-agent read-and-check pass — no probe authoring, no spec edits. The four checks are independent reads of one document and do **not** warrant wave parallelization. The planner MAY split into ordered tasks within the one plan (the analog used 7 tasks) but SHOULD NOT fan out into multiple plans. [VERIFIED: 31-CONTEXT.md D-01; 24.5-PLAN.md is single-plan single-wave]

**Task order (CONTEXT D-08), derived from data dependencies and matching the analog's 7-task sequence.** The recommended 8-task decomposition (the analog's 7 + an explicit pre-exec-gate task, which the analog ran as a pre-execution gate block rather than a numbered task):

| # | Task | Reads | Produces | Pass/fail rule (lifted from SPEC; do NOT execute here) |
|---|------|-------|----------|--------------------------------------------------------|
| 1 | **Pre-execution gate (R1)** | the subject doc (existence + non-empty + not-a-stub); STATE.md (Phase-30 COMPLETE) | the report's pre-exec gate table | Both conditions PASS with evidence (path + byte count for (a); STATE Phase-30-complete citation for (b)). A stub/empty doc OR missing Phase-30 marker → **STOP**, not a partial run. Extra candidate docs in the dir are ignored; `research_result/03-final-resolution.md` is canonical. |
| 2 | **Presence / structural (R2)** | the subject doc structure | report §3 Task-1 detail + section inventory | `PASS`/`FAIL` on: single coherent doc (not a raw concatenation); numbered/labeled sections citable by line range; identifiable sections for the four v1.6 topic areas (curriculum-stage, training-loop/batch-construction, loss/energy, human-approval decisions). A raw concatenation (duplicate/competing top-level numbering, coherence-breaking §6 non-independence) → `FAIL` with reason. |
| 3 | **Finding-coverage crosswalk (R3)** | the subject doc §1.1–§1.18 (by identity); the 18-finding set | crosswalk table (18 rows) | Each of the 18 findings → section + `covered`/`partial`/`silent`. Match by finding **identity**, not heading text. `surface_to_user` → `covered`-as-routed-human-approval; `defer` → `covered`-with-routing; **neither is `silent`**. A section that states no actual position → `partial`. Every `partial`/`silent` flagged as a gap. Row count over the selected set = 18, none omitted. |
| 4 | **Dataset-figure consistency (R4)** | the subject doc figures; `24-VERIFIED-FACTS.md` (CLM-01..13 + DATA-05) | consistency table | For each doc figure mapping to a verified-facts row: `consistent? yes/no`. A **contradiction** fails; agreement within the verified fact's stated precision is consistent; a never-verified figure → unverified-(claimed) caveat flagged FUT (**not a failure**); zero mapped figures → recorded **vacuous pass**. Check passes iff 0 contradictions. |
| 5 | **Locked-convention compliance (R5)** | the subject doc; SCOPE-12 conventions | compliance table | Each locked convention marked `compliant? yes/no`. A recommendation to **change** a convention → recorded **scope observation** (surfaced, not a failure); a silent **breach** → **violation**. Passes iff 0 violations. No re-adjudication of any convention (incl. `D = 6.694`). |
| 6 | **Resolution-doc map (R6)** | R3's crosswalk; the §-line-range inventory (this RESEARCH §"Structural inventory") | `31-RESOLUTION-MAP.md` | Section index (line ranges) + finding→section mapping (18) + citation guide (verbatim path, §/finding-ID anchors, a concrete `…/03-final-resolution.md:START–END` example for EVID-11) + per-finding one-word verdict-direction preview + out-of-scope forward refs + open-items carry-forward (from the doc's §4 gap register + §6 note). |
| 7 | **Readiness report (R7)** | R2–R5 results | `31-READINESS-REPORT.md` | Consolidates the four checks + exec-summary verdict + gap list + fix instructions + re-check protocol. |
| 8 | **Gate decision + STATE/ROADMAP update (R7 close)** | the consolidated report | gate verdict; STATE/ROADMAP record via gsd-tools handlers | Verdict by fixed precedence (below); STATE updated only via handlers, never direct Write/Edit. |

**Why this order (CONTEXT D-08 rationale):** the gate precedes all checks (a stub/empty doc or missing Phase-30 marker STOPs before any check runs); R2 precedes R3–R5 (a structurally incoherent doc makes the crosswalk meaningless); R3–R5 are mutually independent and run in SPEC order; the map derives from the crosswalk; the report consolidates everything; the gate decision is last. [VERIFIED: 31-CONTEXT.md D-08; 24.5-PLAN.md Tasks 1–7]

**Single atomic commit** via `scripts/agent-commit` (set `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; `.githooks` active). No commit touches `pinn/` or the framework specs. [VERIFIED: 31-CONTEXT.md code_context; CLAUDE.md git protocol]

## Structural Inventory of the Resolution Doc (STRUCTURE ONLY — no coverage assessment)

> This is the line-range scouting that grounds the map's §1 section index (CONTEXT D-06/D-07). Captured by `grep -nE "^#{1,4} "` against the **committed** doc. Ranges are start-of-heading to line-before-next-heading; the doc is 282 lines total. **Anchor:** 48,049 bytes, commit `49fb7958` (2026-06-20), clean in worktree. The **stable citation key is the §/finding-ID anchor**, not the line number — line numbers are revision-scoped and refresh on re-pagination (D-07). This inventory records sections + verbatim headings + ranges ONLY; it does NOT say which finding maps where, does NOT assess coverage, and does NOT read or judge any verdict word as a position. [VERIFIED: direct read; `git log -1 -- <doc>`]

| Section | Line range | Title / heading (verbatim) |
|---------|-----------|----------------------------|
| Title | 1–7 | `# Issue 03 Final Resolution — Curriculum and Training Loop` |
| §0 | 8–21 | `## 0. Adjudication method` |
| §1 | 22–23 | `## 1. Final Issue 03 resolutions` |
| §1.1 | 24–27 | `### 1.1 Causal-training mode — ` `surface_to_user` |
| §1.2 | 28–31 | `### 1.2 ` `s_min` ` frame — ` `surface_to_user` |
| §1.3 | 32–35 | `### 1.3 Epsilon strategy — ` `surface_to_user` |
| §1.4 | 36–39 | `### 1.4 B-07 replay/lookahead batching — ` `modified` |
| §1.5 | 40–43 | `### 1.5 B-08 data versus collocation points — ` `modified` |
| §1.6 | 44–47 | `### 1.6 M6 ` `L_norm` ` clamping — ` `modified` |
| §1.7 | 48–51 | `### 1.7 M7 ` `tau_L` ` exclusion from ` `IC13` ` — ` `accepted` |
| §1.8 | 52–55 | `### 1.8 M14 gradient clipping — ` `modified` |
| §1.9 | 56–59 | `### 1.9 M15 energy-loss weights — ` `rejected` ` as an issue-doc replacement` |
| §1.10 | 60–63 | `### 1.10 M16 ` `dt_out` `-aware collocation scaling — ` `defer` |
| §1.11 | 64–67 | `### 1.11 D5 stage transitions — ` `modified` |
| §1.12 | 68–71 | `### 1.12 NS-12 componentwise automatic differentiation — ` `accepted` |
| §1.13 | 72–75 | `### 1.13 NS-13 energy Huber delta — ` `defer` |
| §1.14 | 76–79 | `### 1.14 NS-18 loss scaling and units — ` `modified` |
| §1.15 | 80–83 | `### 1.15 Data-driven adaptive stage assignment — ` `modified` |
| §1.16 | 84–87 | `### 1.16 Locked ` `D` ` conflict — ` `accepted` ` for ` `4.6416` `, ` `rejected` ` for ` `6.694` |
| §1.17 | 88–91 | `### 1.17 ` `L_max` ` and ` `tau_L` ` formulas — ` `modified` ` / ` `surface_to_user` |
| §1.18 | 92–95 | `### 1.18 ALM ` `mu_p` ` clamp — ` `defer` |
| §2 | 96–183 | `## 2. Claim matrix` |
| §3 | 184–212 | `## 3. Disagreement register` |
| §4 | 213–238 | `## 4. Gap register` |
| §5 | 239–265 | `## 5. Source-coverage checklist` |
| §6 | 266–273 | `## 6. Non-independent-input note` |
| §7 | 274–282 | `## 7. Deliverable index` |

**Notes for the planner (structural only):**
- The heading words (`surface_to_user`, `modified`, `accepted`, `rejected`, `defer`) are part of the verbatim heading text and are reproduced here as transcription, not as an assessment that any finding is covered/partial/silent or that any verdict is correct. The crosswalk (R3) and verdict-direction preview (R6 §4) are EXECUTION work.
- Each §1.x is a short (≈4-line) per-finding subsection. The §2 claim matrix is the largest block (96–183). §4 is the doc's own gap register and §6 the non-independence note — both feed the map's open-items carry-forward (R6 §6, CONTEXT D-04).
- Line numbers are valid for commit `49fb7958` only; the map's identity block must record `48,049 bytes` + this commit/date (D-07), and a `NOT-READY` re-delivery refreshes only the ranges (affected-only re-check, D-03 §6).

## The 18-Finding Set (restate from CONTEXT D-09 / SPEC R3 — do NOT pre-compute the crosswalk)

The crosswalk (R3) checks exactly **18** findings. This is the locked set; the planner restates it so the executor checks all 18 and drops none (row count = 18, SPEC prohibition). **Matching is by finding identity, not literal heading text** — the executor must reconcile the doc's heading wording to the selected-set key. [VERIFIED: 31-CONTEXT.md D-09; 31-SPEC.md R3; ROADMAP SC1]

**The 15 ROADMAP-SC1 findings:**
`B-07`, `B-08`, `M6`, `M7`, `M14`, `M15`, `M16`, `D5`, `NS-12`, `NS-13`, `NS-18`, `D-04`, `D-05`, `D-06`, `D = 6.694`.

**The 3 contract-phase extras (consumed by the contract phases):**

| Extra finding | Doc subsection (per CONTEXT D-09) | Consumed by |
|---------------|-----------------------------------|-------------|
| Data-driven adaptive stage assignment | §1.15 | CURR-01 |
| `L_max` / `tau_L` formulas | §1.17 | CURR-02 |
| ALM `mu_p` clamp | §1.18 | LOOP-05 |

**By-identity matching examples the SPEC gives (heading text ≠ finding ID; do NOT treat these as the crosswalk — they are the matching *rule*, illustrated):**
- doc §1.12 "componentwise automatic differentiation" = NS-12 (SPEC R3 example)
- doc §1.1 "Causal-training mode" = D-04 (SPEC R3 / CONTEXT D-09 example)

**Coverage-status semantics the executor applies (lift verbatim; do NOT pre-judge):** a `surface_to_user` verdict (the three human-approval decisions D-04/D-05/D-06) is recorded `covered`-as-routed-human-approval; a `defer` verdict is `covered`-with-routing — **neither is `silent`**. A section that exists but states no actual position is `partial`. A finding the doc does not address at all is `silent` (a gap, never filled). A finding may map to >1 section and a section may cover >1 finding — record the actual mapping, not an assumed 1:1. [VERIFIED: 31-SPEC.md R3 + Edge Coverage; 31-CONTEXT.md D-09]

## Report / Map Structure (lift from the 24.5 analog, adapt to 18 findings + §0–§7)

**Ground both deliverables byte-structure on the verified v1.5 24.5 analog** (CONTEXT D-02), adapted to v1.6's 18-finding set and the §0–§7 / §1.1–§1.18 structure. The *schema* is fixed; the planner settles rendering/mechanics only (Claude's discretion: exact column headers, table vs bullets, heading capitalization — the analog headers are the recommended default). [VERIFIED: 31-CONTEXT.md D-02..D-04, Claude's Discretion; 24.5-READINESS-REPORT.md; 24.5-RESOLUTION-MAP.md]

### `31-READINESS-REPORT.md` — 8 sections (CONTEXT D-03, from `24.5-READINESS-REPORT.md` + SPEC R7)

1. **Executive-summary verdict** — `READY` / `READY-WITH-CAVEATS` / `NOT-READY`, re-derivable from the four check tables (no rubber-stamp).
2. **Pre-execution gate table** — `Gate condition | Result | Evidence` (record path + byte count for the doc; STATE Phase-30-complete citation).
3. **Check results** — a summary table (`# | Check (R-task) | Result`) followed by per-check detail for R2–R5 (the crosswalk table, the consistency table, the compliance table). *Recommended: inline detail, mirroring `24.5-READINESS-REPORT.md` §3.*
4. **Gap list** — `ID | Caveat/Gap | Affects (finding/convention) | Owner / route | Blocking?`.
5. **Fix instructions** — per gap: what is missing, which finding it affects, what the fix should produce.
6. **Re-check protocol** — affected-only re-run + line-range refresh on re-pagination.
7. **Gate decision** — the verdict + STATE/ROADMAP update note.
8. **Acceptance-criteria check** — against the SPEC's 9 acceptance criteria (mirrors the analog's §8 success-criteria check).

### `31-RESOLUTION-MAP.md` — sections (CONTEXT D-04, from `24.5-RESOLUTION-MAP.md` + SPEC R6)

- **Resolution-doc identity** — path, byte count (48,049), committed revision (`49fb7958`, 2026-06-20), date — the line-range anchor (D-07).
- **§1 Section index** — `§ | Lines | Covers` (built from this RESEARCH's structural inventory).
- **§2 Finding→section mapping** over all **18** findings — `Finding ID | Title | Resolution-Doc Section | Lines | Coverage` (from R3).
- **§3 Citation guide** — verbatim file path, §/finding-ID anchors, a concrete `…/03-final-resolution.md:START–END` example for EVID-11; note that §/finding-ID anchors are stable, line numbers revision-scoped.
- **§4 Verdict-direction preview** — `Finding | Direction | one-line note` — one word per finding.
- **§5 Out-of-scope / forward-reference notes** — what Phase 31 does NOT adjudicate (D-04/D-05/D-06 → Phase 32 EVID-15; `D = 6.694` re-adjudication → EVID-15; FUT re-measurement).
- **§6 Open-items carry-forward** — drawn from the doc's own §4 gap register + §6 non-independent-input note.

### Gate-verdict precedence (FIXED by SPEC R7 / CONTEXT D-05 — not a discretion item)

Any `NOT-READY` trigger — a `silent` finding, a contradiction of a v1.5-verified fact, or a locked-convention violation — yields `NOT-READY` **regardless of how many checks pass**. Absent any trigger, any caveat (`surface_to_user` / `defer` rows, non-contradicting unverified figures, scope observations, the §6 non-independence note) yields `READY-WITH-CAVEATS`. All-clean yields `READY`. The exec-summary verdict MUST be re-derivable from the four check tables by this precedence. [VERIFIED: 31-SPEC.md R7; 31-CONTEXT.md D-05; 24.5-READINESS-REPORT.md §7]

## The Four-Check Mechanics (R2–R5 — source + pass/fail rule; do NOT execute)

> Lifted verbatim from `31-SPEC.md`. The executor performs these checks under the STOP protocol; this RESEARCH only names the source each reads and its rule so the plan is concrete.

### R2 — Presence / structural check
- **Reads:** the subject doc's structure (the §0–§7 / §1.1–§1.18 inventory above).
- **Rule:** `PASS`/`FAIL` on single-coherent-doc (not a raw concatenation), line-range-citable sections, and identifiable sections for the four v1.6 topic areas (curriculum-stage; training-loop/batch-construction; loss/energy; human-approval decisions). Raw concatenation → `FAIL` with reason. [SPEC R2]

### R3 — Finding-coverage crosswalk
- **Reads:** the subject doc §1.1–§1.18 (by identity); the 18-finding set (above).
- **Rule:** each of 18 findings → section + `covered`/`partial`/`silent`; by-identity matching; `surface_to_user`/`defer` are `covered`-with-caveat (never `silent`); position-less section → `partial`; every `partial`/`silent` flagged as gap; row count = 18, none dropped. [SPEC R3]

### R4 — Dataset-figure consistency check
- **Reads:** the subject doc's stated figures; the **verified-facts register** `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — the only in-repo verified-facts source (v1.6 has no Phase-24 analog). Rows: **CLM-01..12** (confirmed/corrected dataset figures), the **DATA-05** mass-drift row (70 base-hier artifacts quarantined), **CLM-13** (`D = 6.694`, PENDING — not probed, a contested convention not a dataset fact), and the CLM-14+ extension (zero rows). [VERIFIED: direct read of `24-VERIFIED-FACTS.md`; CONTEXT D-10]
- **Rule:** for each doc figure mapping to a verified row, `consistent? yes/no`.
  - **Contradiction-only fails** — a materially different value fails the check.
  - **Within-precision = consistent** — agreement within the verified fact's stated rounding/precision (e.g. doc `~2,565` vs verified `~2,565`) is consistent.
  - **Never-verified = caveat** — a figure v1.5 never verified is an unverified-(claimed) caveat flagged FUT, **not a failure**; never presented as a verified fact.
  - **Vacuous pass** — zero mapped figures → recorded vacuous pass (0 contradictions).
  - Check passes iff 0 contradictions. [SPEC R4; CONTEXT D-10]

### R5 — Locked-convention compliance (SCOPE-12)
- **Reads:** the subject doc; the SCOPE-12 locked conventions (verbatim from REQUIREMENTS.md / 31-SPEC.md R5):
  1. 14D input `[τ, IC₁₃]`
  2. Jacobi IC₁₃ (13 components)
  3. Mass-weighted COM projection head
  4. PHYS-03 softening `eps_soft = 1e-5`
  5. Post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`)
  6. PHYS-01 raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` (`D = 6.694` rejected by v1.5 Phase 25 EVID-10)
  7. v1.5 data-side contracts PIPE-01..10 / VAL-01..04
- **Rule:** each convention `compliant? yes/no`. A recommendation to **change** a convention → recorded **scope observation** (surfaced, never a failure); a silent **breach** → **violation** (`NOT-READY` trigger). Passes iff 0 violations. No re-adjudication of any convention — incl. the `D = 6.694` conflict (the doc §1.16 upholds `≈ 4.6416` and rejects `6.694`; Phase 31 confirms compliance only — re-adjudication is Phase 32 EVID-15). [VERIFIED: 31-SPEC.md R5; REQUIREMENTS.md SCOPE-12; CONTEXT specifics]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Report/map schema | A new readiness-report or map structure | The verified 24.5 analog section sets (CONTEXT D-02..D-04) | The analog PASSED (`24.5-VERIFICATION.md`); inventing a schema risks a process-artifact-schema gap (MUST-surface under the STOP protocol) |
| Recording the gate outcome to STATE | Direct STATE.md Write/Edit | gsd-tools STATE/ROADMAP handlers | Universal anti-pattern 15; direct STATE edits are prohibited |
| Committing the plan | Raw `git commit` / broad `git add` | `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` (explicit paths) | `.githooks` active; project git protocol forbids raw commits and broad staging |
| Line-range capture | Manual eyeballing | `grep -nE "^#{1,4} "` on the committed doc (this RESEARCH did exactly this) | Any method yielding revision-anchored ranges is acceptable (CONTEXT D-06, Claude's discretion) |

## Common Pitfalls

### Pitfall 1: Inventing coverage or a verdict where the doc is silent
**What goes wrong:** the executor infers a position for a `silent` finding or assigns a verdict.
**Why it happens:** the doc is the candidate verdict source and reads as authoritative.
**How to avoid:** a `silent` finding is **always** a gap row, never filled; Phase 31 records coverage status only — no finding carries a Phase 31 verdict (SPEC R8 prohibition). Verdicts are Phase 32+.
**Warning signs:** any inferred-position text in the crosswalk; any `READY`/`READY-WITH-CAVEATS` while a `silent`/contradiction/violation trigger is present (rubber-stamp). [SPEC R8 prohibitions]

### Pitfall 2: Failing the figure check on a non-contradicting unverified figure
**What goes wrong:** a figure v1.5 never verified is treated as a failure, or presented as a verified fact.
**How to avoid:** contradiction-only fails; an unverified-but-non-contradicting figure is a caveat flagged FUT, never a failure and never cited as verified. [SPEC R4 prohibition]

### Pitfall 3: Re-adjudicating a locked convention (esp. `D = 6.694`)
**What goes wrong:** the compliance check slides into re-deciding `D = 6.694` vs `≈ 4.6416`.
**How to avoid:** Phase 31 confirms compliance only; the `D = 6.694` conflict is confirmed-compliant-and-flagged (the doc upholds `≈ 4.6416`); re-adjudication is Phase 32 EVID-15. A *recommendation* to change a convention is a scope observation (surfaced), not a failure; a *silent breach* is a violation. [SPEC R5 prohibition; CONTEXT specifics]

### Pitfall 4: Editing the doc or a framework spec
**What goes wrong:** the executor "fixes" a gap by editing the resolution doc or a spec.
**How to avoid:** the doc is the user's external product — read and map only; if `NOT-READY`, route fix instructions to the consolidation agent. `git diff` for the Phase 31 commit must show zero changes to `ctl_instruction.md`, `pinn_architecture.md`, the resolution doc, or any `pinn/` path. [SPEC R8; Validation Architecture below]

## Validation Architecture

> `nyquist_validation: true` in `.planning/config.json` — section included. Phase 31 produces markdown deliverables, not code, so "tests" are structural/derivability assertions over the two files plus a git-diff invariant. These make the plan testable without re-running adjudication.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None (no code; documentation-verification phase). Checks are structural assertions runnable as shell one-liners + a reviewer judgment pass. |
| Config file | none |
| Quick run command | `grep`/`wc`/`git diff` one-liners (below) |
| Full suite command | the same set, run at plan close before `/gsd-verify-work` |

### Phase Deliverable → Check Map
| Check | Behavior | Test type | Automated command (illustrative) | Exists? |
|-------|----------|-----------|----------------------------------|---------|
| Map row-count = 18 | The crosswalk / §2 mapping covers exactly the 18 selected findings | structural | count finding rows in `31-RESOLUTION-MAP.md` §2 (e.g. `grep -c` over the mapping table body) → expect 18 | ❌ Wave 0 (deliverable not yet written) |
| Report required sections present | The report carries all 8 sections (exec verdict, pre-exec gate, 4 checks, gap list, fix instructions, re-check protocol, gate decision, acceptance check) | structural | `grep -nE "^#{1,3} " 31-READINESS-REPORT.md` → assert each required heading present | ❌ Wave 0 |
| Map required sub-sections present | Identity block + §1 section index + §2 mapping + §3 citation guide + §4 verdict-direction + §5 out-of-scope + §6 carry-forward | structural | `grep -nE "^#{1,3} " 31-RESOLUTION-MAP.md` → assert each present; assert a concrete `…03-final-resolution.md:START–END` example string appears | ❌ Wave 0 |
| Verdict derivable | Exec-summary verdict matches the precedence applied to the four check tables | judgment | reviewer re-derives the verdict from the tables (no rubber-stamp) | ❌ Wave 0 |
| Zero spec/pinn/doc edits | The Phase 31 commit edits nothing it must not | invariant | `git show --stat <commit>` (or `git diff --name-only`) shows zero `ctl_instruction.md` / `pinn_architecture.md` / `03-final-resolution.md` / `pinn/**` paths | ❌ Wave 0 (asserted at commit time) |
| Citation example resolves | The `…:START–END` example points at a real range in the committed doc | structural | sed/awk the named line range out of the doc and confirm it lands inside the cited section | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** the structural greps for whichever deliverable the task wrote.
- **Phase gate:** the full check set (all greps + the git-diff invariant) green before `/gsd-verify-work`; the verdict-derivability judgment pass.

### Wave 0 Gaps
- [ ] `31-READINESS-REPORT.md` — does not exist yet (Task 7 produces it).
- [ ] `31-RESOLUTION-MAP.md` — does not exist yet (Task 6 produces it).
- [ ] No test framework needed; the assertions are shell one-liners + a reviewer judgment pass. The analog used no framework either.

## State of the Art

| Old (v1.5) | Current (v1.6) | Why changed | Impact |
|------------|----------------|-------------|--------|
| Crosswalk over a pre-built **19-row issue ledger** (`24-ISSUE-LEDGER.md`) | Crosswalk over the **ROADMAP-enumerated 18-finding set** (no pre-built ledger; the issue ledger is built later in Phase 32) | v1.6 sequences the issue ledger after readiness | The planner restates the 18 findings inline (CONTEXT D-09); there is no ledger file to read for R3 |
| Consistency check vs an **in-milestone** Phase-24 verified-facts register | Consistency check vs the **archived v1.5** register `24-VERIFIED-FACTS.md` | v1.6 has **no Phase-24 analog** — no in-milestone empirical verification | R4 reads the archived v1.5 file; figures are checked for *contradiction only*, never re-measured (CONTEXT D-10; SPEC Background) |
| 6 HC conventions (HC-1..HC-6) | 7 SCOPE-12 conventions (adds v1.5 PIPE-01..10 / VAL-01..04 data-side contracts) | v1.5 locked the data-side pipeline/validation contracts | R5 checks 7 convention groups, not 6 |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| — | (none) | — | All claims are VERIFIED against an in-repo source: CONTEXT/SPEC/ROADMAP/REQUIREMENTS, the verified 24.5 analog, a direct structural read of the subject doc, and `git log`. No `[ASSUMED]` claim appears in this research. |

**This table is empty:** every claim was verified or cited — no user confirmation needed.

## Open Questions

None at the planning level. The SPEC ambiguity score is 0.09 (well under the 0.20 gate); CONTEXT records that **no source-silent semantic decision arose** — the three open decisions (report/map markdown, line-range capture, four-check order) are operational/presentation form whose *schema* is already fixed by the SPEC + the verified analog, so the STOP protocol recorded no gap. [VERIFIED: 31-SPEC.md Ambiguity Report; 31-CONTEXT.md header + decisions]

## Surfaced to Orchestrator

**No planning-level ambiguity remained unresolved by the sources.** Every planning question the planner faces — plan/wave shape, task order, report/map section sets, the 18-finding set, the four-check sources and rules, the verdict precedence, the verified-facts source, the line-range anchor — is answered explicitly by `31-CONTEXT.md` (D-01..D-10), `31-SPEC.md` (R1–R8 + Edge Coverage + Prohibitions), and the verified 24.5 analog. There is nothing source-silent to surface; this research invented nothing and pre-judged none of the four EXECUTION checks (coverage status, figure consistency, convention compliance, verdict). [VERIFIED: 31-CONTEXT.md; 31-SPEC.md]

## Environment Availability

> Phase 31 is purely documentation work (read internal markdown, write two markdown files, one git commit). External tool dependencies: `grep` / `wc` / `git` (standard, present) and `scripts/agent-commit` + gsd-tools handlers (in-repo, used by every prior phase). No runtime, database, or network dependency. **Step 2.6 effectively SKIPPED** — no blocking external dependency.

## Sources

### Primary (HIGH confidence — in-repo, read this session)
- `.planning/phases/31-resolution-doc-readiness-verification/31-CONTEXT.md` — D-01..D-10, canonical refs, deferred ideas
- `.planning/phases/31-resolution-doc-readiness-verification/31-SPEC.md` — R1–R8, boundaries, constraints, acceptance, edge coverage, prohibitions, ambiguity report
- `.planning/ROADMAP.md` §"Phase 31" — goal + SC1–SC4; the ⛔ external-gate semantics
- `.planning/REQUIREMENTS.md` — SCOPE-12 (locked v1.4/v1.5 conventions), VER-13..18, source-treatment policy
- `CLAUDE.md` — the STOP protocol (v1.6 adjudication-milestone applicability); git commit protocol
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` — the subject; structural read (headers + line ranges); `git log -1` for identity
- `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — CLM-01..13 + DATA-05 (R4 source)
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-PLAN.md` — the 7-task execution template (D-08 grounding)
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` — the report template (D-03 grounding)
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — the map template incl. citation guide (D-04/D-06/D-07 grounding)
- `.planning/config.json` — `nyquist_validation: true`

### Secondary / Tertiary
- None. No external web research was performed (none needed or wanted — all grounding is internal).

## Metadata

**Confidence breakdown:**
- Execution approach: HIGH — directly grounded in CONTEXT D-01/D-08 + the verified 24.5 7-task analog.
- Structural inventory: HIGH — direct `grep -nE` read of the committed doc; ranges re-derivable; anchored to commit `49fb7958`.
- Report/map structure: HIGH — lifted from the verified, PASSED 24.5 analog.
- Four-check mechanics: HIGH — lifted verbatim from `31-SPEC.md` R2–R5; sources confirmed present (`24-VERIFIED-FACTS.md` read).

**Research date:** 2026-06-20
**Valid until:** Stable until the subject doc is re-delivered (a `NOT-READY` re-delivery refreshes the structural line ranges only; §/finding-ID anchors are stable). Otherwise no expiry — all sources are in-repo and committed.

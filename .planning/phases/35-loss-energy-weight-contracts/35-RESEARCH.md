# Phase 35: Loss & Energy-Weight Contracts - Research

**Researched:** 2026-06-27
**Domain:** v1.6 spec-side loss-contract adjudication and framework-spec transcription
**Confidence:** HIGH for project-local planning decisions; LOW for public-web research, which produced no authoritative source for this private phase.

<user_constraints>
## User Constraints (from CONTEXT.md)

All content in this section is copied from `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md`; it is included so the planner can honor the locked discussion output before using the research synthesis below. [VERIFIED: codebase grep]

### Locked Decisions

#### Phase Boundary

Phase 35 makes `ctl_instruction.md` and `pinn_architecture.md` carry the
adjudicated **loss-component, energy-weight, energy-Huber, and causal-training-mode
contracts**, each transcribed *by verdict status* (not by the stale issue-doc or
roadmap proposal). It is v1.6 **specwork only** — it edits framework specs and
adjudication artifacts; it implements no training-loop code (FUT-01/FUT-04).

The four contracts and their settled dispositions (locked by `35-SPEC.md`):

- **LOSS-01 / NS-18 (+NS-12)** — loss scaling & units: **`modified`** verdict.
- **LOSS-02 / M15** — energy-weight schedule: issue-doc cap table **`rejected`** as a
  replacement; retain the current PHYS-05 warmup (`λ_E ≤ 1`).
- **LOSS-03 / NS-13** — energy Huber-δ: **`defer`**; keep `delta_E = 1.0` baseline.
- **LOSS-04 / D-04** — causal-training mode: **`RESOLVED-WITH-INSTRUCTION`**
  (owner-ratified **Option A**), resolving GAP-32-01.

Much of this content **already exists** in `pinn_architecture.md` (data Huber
`δ_r = 1`, energy Huber `δ = 1.0`, causal weighting with `stopgrad`, PHYS-05
schedule `≤ 1`, deferred causal-exponent clip). Phase 35's work is therefore
largely: author evidence packets, **tag** the existing math with the Phase 35
verdict-status callouts, make the `τ`/`u` chain-factor distinction explicit, add
the M15 logging requirement, enforce the canonical-home cross-reference split,
and close the ledger.

#### Requirements (locked via SPEC.md)

**4 requirements are locked** (`LOSS-01`, `LOSS-02`, `LOSS-03`, `LOSS-04`;
ambiguity 0.11). See `35-SPEC.md` for full requirements, boundaries, and
acceptance criteria (`AC-LOSS-01` … `AC-LOSS-04`). Requirements are **not**
duplicated here.

Downstream agents MUST read `35-SPEC.md` before planning or implementing.

> **Source-precedence warning:** `REQUIREMENTS.md` LOSS-01..04 and `ROADMAP.md`
> Phase 35 still carry the *superseded* phrasing (capped-hybrid `λ_E`, per-stage
> `0.01–0.1` Huber calibration, "Option-C preserved"). `35-SPEC.md` supersedes
> them with the resolution-doc verdicts. **Anchor to `35-SPEC.md`, never to the
> stale roadmap/requirements wording.**

**In scope (from SPEC.md):**
- Create Phase 35 evidence packets before spec edits for M15, NS-12, NS-13, NS-18;
  consume the existing D-04 packet + gap resolution.
- Edit `ctl_instruction.md` and `pinn_architecture.md` only — `ctl` canonical for
  training-methodology/assembly, `pinn_architecture` canonical for component math
  where it already lives.
- Stable section-heading + AC-ID cross-references; one canonical home per half; no
  duplicated normative body text.
- Update the Phase 32 issue ledger and v1.6 tracking only as needed for
  Phase-35-owned rows (`IN_PROGRESS → FIX_APPLIED → VERIFIED`).
- Preserve verdict status in the edited specs (`locked` / `modified` / `rejected` /
  `deferred` / `owner-ratified`).

**Out of scope (from SPEC.md):**
- Implementing training-loop or DataLoader code (FUT-01/FUT-04).
- Running the admitted-set EDA, Stage-0 pilot, energy-δ quantile calibration, or
  causal-mode A/B/C ablation (FUT/calibration).
- Inventing a causal-exponent clip bound (resolution GAP-01 defers it).
- Specifying Option C time-windowed causal design (owner ratified Option A).
- Adopting the issue-doc `λ_E` cap table, `λ_E = 1000` premise, automatic
  dominance-reweighting law, or per-stage Huber-δ table (rejected/deferred).
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`,
  `stage-strat-revision.md`, or `pinn/` live code (SCOPE-13/14).

#### Implementation Decisions

##### Verdict-status transcription convention

- **D-35-01:** Transcribe each loss contract at its **adjudicated verdict +
  status** with source citations — NEVER the issue-doc/roadmap "preview"
  proposal (the failure mode Phase 34 caught in LOOP-04's `8.5`). This is the
  central v1.6 transcription discipline (Phase 34 D-34-01).
- **D-35-02:** Reuse the Phase 33/34 **blockquote-callout convention verbatim**,
  swapping `LOOP`→`LOSS`:
  `> **Phase 35 contract: <name> (LOSS-NN; <verdict>; AC-LOSS-NN; grounded by <source>).**`
  with an inline status tag (`locked` / `modified` / `rejected` / `deferred` /
  `owner-ratified`) and a grounded-by citation — file-internal consistency with
  the existing CURR callouts (`ctl_instruction.md` ~lines 1630, 1832) and the
  LOOP callouts (`pinn_architecture.md`). (Phase 34 D-34-07.)
- **D-35-03:** Any transcribed pseudocode is rendered in a fenced block
  explicitly labeled **"normative spec contract — not executable; FUT-01/FUT-04
  implements"** (SCOPE-14, Phase 34 D-34-08). Pure-deferral/owner sub-parts record
  the deferral + forward-reference in the body, same convention, status-driven
  (Phase 34 D-34-09).

##### Canonical-home split & anti-duplication (SI-PINN-003 guardrail)

- **D-35-04:** `pinn_architecture.md` is canonical for the **component math where
  it already lives** — `L_data` Huber (§3.1), `L_phys^causal` causal weights
  (§3.2), `L_IC` (§3.3), `L_E` energy Huber `δ_E = 1.0` + shared physics/energy
  collocation set (§3.4), `L_L` angular-momentum (§3.5), and the PHYS-05 warmup
  schedule with `λ_E^max(k) ≤ 1` + deferred causal-exponent clip (§4.1, ~lines
  625–655). `ctl_instruction.md` is canonical for the **training-methodology /
  total-loss assembly** contract — the Total-Loss / Data-Flow section (~1718–1745)
  that Phase 34's D-34-15 ordering skeleton augments (loss terms currently opaque
  with a Phase-35 forward-reference; Phase 35 now makes them concrete via
  cross-reference, NOT by moving the math).
- **D-35-05:** Each half names the other for the portion it does not own via
  **bidirectional stable-anchor cross-references** (section heading + `AC-LOSS-NN`,
  **never line numbers**), with **status-tag parity** across halves and **zero
  duplicated normative body text** (Phase 34 D-34-04/05/06). The mechanism/assembly
  split must not become a second SI-PINN-003: single canonical home per
  value/formula + a pointer, plus a verifier that *proves no duplication* — a
  bidirectional arrow alone does not stop drift.

##### Per-contract transcription targets (what each edit asserts)

- **D-35-06 (LOSS-01 / NS-18+NS-12, `modified`):** State the modified verdict at its
  canonical homes — projected scaled positions for data, **Huber** data loss
  (reject the stale L1/MAE reading), componentwise normalized-time derivatives for
  physics, matched `epsilon_train = 1e-5` in physics **and** energy, raw masses,
  shared physics/energy collocation set, IC anchor, angular-momentum regularizer,
  **no linear-momentum loss**, and the chain factors **`2` and `4` only when
  differentiating w.r.t. `τ`** rather than when `u` is already the autograd leaf
  (grounded by the locked v1.4 `τ = 2u − 1`, autograd leaf `u`; short
  first-principles calculus, not an invention). Must not contradict the Phase 34
  data-vs-collocation contract. Sources: resolution §1.14 / NS18-01..04, Phase 32
  ledger rows NS-12 + NS-18, Phase 34 LOOP-02/03.
- **D-35-07 (LOSS-02 / M15, `rejected` as replacement):** Reject the issue-doc cap
  table (up to `500`) and the stale `λ_E = 1000` premise as replacements; **retain**
  the current PHYS-05 warmup (`λ_E^max ≤ 1`, already in §4.1 ~line 655); **require
  logging** of weighted losses, scheduled weights, and gradient statistics; keep
  **automatic dominance reweighting deferred** until measured weighted-loss/gradient
  evidence exists. Sources: resolution §1.9 / M15-01..04 / DGR-09..10. *(If §1.9
  does not enumerate the exact logging fields, treat the field list as transcribe-
  what-is-explicit; a silent field list is a packet-time STOP item, not an
  invention — see D-35-09.)*
- **D-35-08 (LOSS-03 / NS-13, `defer`):** Keep `delta_E = 1.0` as the configurable
  baseline (already §3.4 ~line 531); state that per-stage `|ΔH|` quantile
  calibration is **deferred** pending measurement of normalized `|ΔH|` quantiles,
  linear-branch occupancy, validation energy drift, and weighted gradients. The
  `0.01–0.1` range appears **only** as deferred calibration evidence, never a locked
  table. Sources: resolution §1.13 / NS13-01..03 / DGR-14.
- **D-35-08b (LOSS-04 / D-04, `RESOLVED-WITH-INSTRUCTION`, Option A):** Lock the
  current per-time causal weighting (`w_1 = 1`,
  `w_n = exp(−η_c · Σ_{m<n} stopgrad(R̄_m))`, `η_c = 1`); preserve the
  dense-residual pseudo-ALM **rejection** as locked; keep optional
  scalar-conservation ALM **deferred P2 only**; **defer** the numeric
  causal-exponent clip bound to FUT (already deferred in §4.1 ~lines 640–642). The
  stale "Option B = global + dense-ALM" label is superseded and not reused.
  Sources: resolution §1.1 / CAU-01..05 / GAP-01..02, Phase 32 GAP-32-01 + D-04 row,
  Phase 34 LOOP-01 compatibility note.

##### Adjudication: packet-before-edit & ledger lifecycle

- **D-35-09 (packet-before-edit; STOP stays armed):** Author **one evidence packet
  per finding** for **M15, NS-12, NS-13, NS-18** in a Phase-35 `evidence/` dir
  **before any spec edit**, reusing the Phase 32 `evidence/_TEMPLATE.md` +
  `README.md` schema and the existing EVID/AC reservation scheme (do **NOT** mint a
  new ID schema). **D-04 (LOSS-04) consumes the existing Phase 32 packet** + the
  GAP-32-01 resolution — no new D-04 packet (Phase 34 D-34-12 analog). Packets
  **consume** the resolution-doc verdict; they do not re-litigate. **If a packet
  surfaces a NEW conflict** (a v1.5-verified fact contradicting a verdict, or a
  source-silent field/value the SPEC names but the source omits), **STOP per
  EVID-15** and record a `35-GAPS.md` gap + a `.planning/milestones/v1.6-GAPS.md`
  index row — never invent. (Phase 34 D-34-10/11.)
- **D-35-10 (ledger lifecycle):** Move Phase-35-owned rows (M15, NS-12, NS-13,
  NS-18, D-04) through `IN_PROGRESS → FIX_APPLIED → VERIFIED` in
  `32-ISSUE-LEDGER.md` with packet link + AC ID. "Fix applied" is **not** closure;
  re-verify previously-`VERIFIED` rows the edit batch could regress (VER-16).
- **D-35-11 (GAP-32-01 closure):** Confirm `GAP-32-01` reads
  `RESOLVED-WITH-INSTRUCTION` in **both** `32-GAPS.md` and `v1.6-GAPS.md`. The v1.6
  index already records it resolved (2026-06-26, Option A); Phase 35 **verifies and
  echoes**, it does not re-decide. (`AC-LOSS-04` requires the dual-register mark.)

##### Hard prohibitions (must-NOT, from SPEC + STOP protocol)

- **D-35-12:** No framework-spec edit introduces, as a locked/default construct:
  the issue-doc `λ_E` cap table, a fabricated per-stage Huber-δ table, Option-C
  window mechanics, a numeric causal-exponent clip bound, default dense-residual
  ALM, or a `λ_E = 1000` premise. Each may appear only as explicitly
  rejected/deferred. (SPEC Prohibitions + Constraints; STOP protocol.)

### the agent's Discretion

- The planner decides the **number of plan files and task grouping**, provided:
  every `LOSS-01..04` requirement appears in a plan `requirements` field;
  **packet-before-edit precedes each spec edit** (D-35-09); and the plan is
  executable by `gsd-execute-phase`. Natural wave shape (non-binding): **W1**
  packets (M15/NS-12/NS-13/NS-18) + consume D-04 packet → **W2** spec edits
  (`pinn_architecture` component-math tags + `ctl_instruction` assembly &
  bidirectional cross-refs) → **W3** ledger closure + GAP-32-01 dual-register
  confirmation + the no-duplication consistency check.
- Exact evidence-packet filename slugs (stable, grep-friendly, ledger-mapped),
  exact ledger Markdown layout, and the exact deterministic check commands — at
  the planner/executor's discretion. Suggested slugs mirroring the Phase 34 set
  (`b-07-…`, `m16-…`): `m15-energy-weight-schedule.md`,
  `ns-12-…`, `ns-13-energy-huber-delta.md`, `ns-18-loss-scaling-units.md`.

### Deferred Ideas (OUT OF SCOPE)

- **Energy-δ quantile calibration** (`0.01–0.1` per-stage Huber-δ) — FUT/calibration;
  needs measured `|ΔH|` quantiles, branch occupancy, validation drift, gradients.
- **Automatic dominance reweighting** (`λ_E·L_energy > 10·L_data` → warn/reduce) —
  deferred until measured weighted-loss/gradient evidence exists (LOSS-02).
- **Numeric causal-exponent clip bound** — deferred to FUT (resolution GAP-01).
- **Optional scalar-conservation ALM** — deferred P2 only; not in the default loss.
- **Option C time-windowed causal-ALM hybrid** — not commissioned (owner ratified A).
- **Numeric acceptance-check execution via disposable probes** — Phase 36 (VER-15),
  not Phase 35.
- **Training-loop / DataLoader / ALM implementation** — FUT-01/FUT-04 (trainex track).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| LOSS-01 | Transcribe NS-18/NS-12 loss scaling and units into the framework specs. | Use resolution doc §1.12 and §1.14, current `pinn_architecture.md` component math, and `ctl_instruction.md` total-loss assembly; require packet-before-edit and a chain-factor verification. [VERIFIED: codebase grep] |
| LOSS-02 | Transcribe M15 energy-weight verdict. | Reject the stale issue cap table and retain PHYS-05 `λ_E^max <= 1`; add logging requirement and defer dominance reweighting. [VERIFIED: codebase grep] |
| LOSS-03 | Transcribe NS-13 energy Huber-delta verdict. | Keep `delta_E = 1.0`; mark per-stage quantile calibration deferred pending measured evidence. [VERIFIED: codebase grep] |
| LOSS-04 | Transcribe D-04 causal-training mode owner decision. | Consume existing D-04 packet plus `GAP-32-01` owner resolution; lock Option A per-time causal weighting and preserve dense-residual ALM rejection. [VERIFIED: codebase grep] |
</phase_requirements>

## Summary

Phase 35 is a private, repository-local specification phase, not a package or implementation phase. Public web search did not return authoritative sources for the private LOSS contract questions, so the planner should rely on local GSD/spec artifacts: `35-SPEC.md`, `35-CONTEXT.md`, the issue-03 resolution doc, Phase 31 readiness/map artifacts, the Phase 32 evidence protocol/ledger/gaps, and the current framework specs. [VERIFIED: websearch] [VERIFIED: codebase grep]

The most important planning correction is source precedence. `ROADMAP.md` and `.planning/REQUIREMENTS.md` still contain stale Phase 35 success-criteria language for the capped-hybrid `λ_E` schedule, per-stage Huber calibration, and Option-C preservation, while `35-SPEC.md` and `35-CONTEXT.md` explicitly supersede that wording. The plan must transcribe adjudicated verdicts/status, not roadmap preview text. [VERIFIED: codebase grep]

**Primary recommendation:** plan three waves: evidence packets first, then status-tagged spec edits in the two canonical homes, then ledger/gap/negative-check verification before closing rows. [VERIFIED: codebase grep]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Evidence adjudication for M15, NS-12, NS-13, NS-18 | GSD planning/evidence layer | Framework specs | Packets must establish verdict, sources, and AC IDs before any spec edit. [VERIFIED: codebase grep] |
| Loss component math (`L_data`, `L_phys^causal`, `L_E`, `L_L`, `L_IC`) | `pinn_architecture.md` spec layer | `ctl_instruction.md` assembly pointer | `pinn_architecture.md` already owns the component formulas and PHYS-05 catalog; moving them would duplicate canonical text. [VERIFIED: codebase grep] |
| Training methodology / total-loss assembly | `ctl_instruction.md` spec layer | `pinn_architecture.md` component pointer | `ctl_instruction.md` owns data flow, default loss assembly, and training-step ordering; it should cross-reference component math by stable heading + AC ID. [VERIFIED: codebase grep] |
| D-04 causal-mode transcription | Framework specs | Phase 32 gap/ledger artifacts | The owner decision is recorded in GAP-32-01, while existing D-04 packet supplies the earlier evidence and blocker history. [VERIFIED: codebase grep] |
| Ledger closure and regression verification | Phase 32 issue ledger + Phase 35 verification artifact | Framework specs | `FIX_APPLIED` is not terminal; closure requires verification evidence and preserved verdict/status logs. [VERIFIED: codebase grep] |

## Project Constraints (from AGENTS.md)

- Use Sequentialthinking for multi-step work; this research used it before multi-step analysis. [VERIFIED: AGENTS.md]
- v1.6 phases 30-36 run under the adjudication STOP protocol: do not invent source-silent semantic, process-schema, or cross-phase decisions. [VERIFIED: AGENTS.md]
- v1.6 specwork targets only `ctl_instruction.md` and `pinn_architecture.md`; `sampling_method.md` is frozen, `data_quality_assessment.md`, `review-of-framework.md`, and `stage-strat-revision.md` are read-only, and training-loop implementation/EDA/Stage-0 pilot are FUT. [VERIFIED: AGENTS.md]
- Live `pinn/` code is not grounding evidence; references to `pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py` are allowed only in forward handoff notes. [VERIFIED: AGENTS.md]
- STOP gaps require the full gap record: decision point, artifact location, task context, classification, source silence with citations, math/engineering grounding, tempted decision, user options, impact confidence, status, and resolution note. [VERIFIED: AGENTS.md]
- Start-session git state must be surfaced, existing changes are user-owned, and destructive operations require exact approval plus recovery markers. [VERIFIED: AGENTS.md]
- GSD phase workflows must verify the correct milestone worktree before phase initialization; Phase 35 is registered in `.worktrees/specwork` on `milestone/v1.6`. [VERIFIED: AGENTS.md]
- The user explicitly instructed this researcher not to commit; despite `.planning/config.json` setting `commit_docs: true`, no commit should be made for this research turn. [VERIFIED: user prompt]
- The one existing worktree change at research start was `M AGENTS.md`; it is user-owned and must remain separate from the Phase 35 research artifact. [VERIFIED: git status]

## Standard Stack

### Core

| Library / Artifact | Version | Purpose | Why Standard |
|--------------------|---------|---------|--------------|
| `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md` | 2026-06-26, ambiguity 0.11 | Authoritative Phase 35 WHAT, boundaries, acceptance criteria, and stale-source overrides | It locks LOSS-01..04 and supersedes stale roadmap/requirements phrasing. [VERIFIED: codebase grep] |
| `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md` | 2026-06-27 | Locked implementation decisions and planner discretion | It records D-35-01..12, canonical-home split, packet-before-edit, and deferred ideas. [VERIFIED: codebase grep] |
| `03-final-resolution.md` | byte-identical to commit `49fb7958` per Phase 31 | Candidate verdict source for D-04, M15, NS-13, NS-18, NS-12 | Phase 31 mapped the required sections and found 18/18 selected findings covered with zero silent findings. [VERIFIED: codebase grep] |
| Phase 32 evidence protocol/template | Current v1.6 protocol | Evidence packet schema, verdict enum, status lifecycle | Required by packet-before-edit; prevents spec edits from outrunning evidence. [VERIFIED: codebase grep] |
| `32-ISSUE-LEDGER.md` | Current v1.6 ledger | Stable status index for Phase 35-owned rows | M15, NS-12, NS-13, and NS-18 are `PENDING`; D-04 must be reconciled with the later GAP-32-01 resolution. [VERIFIED: codebase grep] |
| `ctl_instruction.md` | Current framework spec | Training-methodology and total-loss assembly canonical home | Owns data flow, total loss assembly, optimizer-phase semantics, and training-step ordering. [VERIFIED: codebase grep] |
| `pinn_architecture.md` | Current framework spec | Component math canonical home | Owns data Huber, causal physics residual, energy Huber, angular momentum, AD chain factors, PHYS-05 warmup. [VERIFIED: codebase grep] |

### Supporting

| Library / Tool | Version | Purpose | When to Use |
|----------------|---------|---------|-------------|
| `rg` | 15.1.0 | Fast source-token and forbidden-token checks | Use for locating anchors and proving stale constructs are absent. [VERIFIED: command output] |
| `python3 -c` | Python 3.14.5 | Deterministic structural assertions over Markdown files | Use for multi-file count/absence/presence checks in verification tasks. [VERIFIED: command output] |
| `git` | 2.54.0 | Status/diff/path-scope verification | Use before edits and before any future commit; do not commit in this research task. [VERIFIED: command output] |
| `gsd-tools.cjs` | available, no `--version` flag | Phase initialization and GSD query seam | Use for `init.phase-op`, research-plan caching, and later workflow transitions. [VERIFIED: command output] |
| `tools/spec-render-check/detect.mjs` | local Node tool | Optional Markdown render-risk detector | Use only if Phase 35 edits complex math/table rendering and planner wants a render guard. [VERIFIED: codebase grep] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `35-SPEC.md` verdicts | ROADMAP/REQUIREMENTS LOSS wording | Rejected for planning because those files preserve stale capped-hybrid, Huber-calibration, and Option-C preview language. [VERIFIED: codebase grep] |
| Phase 32 packet schema | New Phase 35 packet schema | Rejected because D-35-09 requires reuse of Phase 32 template/protocol and existing EVID/AC scheme. [VERIFIED: codebase grep] |
| Stable section + AC-ID references | Line-number-only references | Rejected because line numbers drift and D-35-05 requires stable anchors. [VERIFIED: codebase grep] |
| Public web/PINN general advice | Local adjudication artifacts | Rejected for the plan because the phase concerns repository-specific verdict transcription, not general technique selection. [VERIFIED: websearch] |

**Installation:**
```bash
# No package installation is required for Phase 35.
```

**Version verification:** no external package versions are recommended or installed. Tool availability was verified with `git --version`, `node --version`, `rg --version`, and `python3 --version`. [VERIFIED: command output]

## Package Legitimacy Audit

Not applicable. Phase 35 installs no external npm, PyPI, or crates packages; it uses existing local tools and repository artifacts only. [VERIFIED: codebase grep]

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```text
Phase 35 PLAN
  |
  v
Wave 1: evidence packet(s)
  |-- M15 packet -> verdict: rejected as issue-doc replacement
  |-- NS-12 packet -> verdict: accepted componentwise AD
  |-- NS-13 packet -> verdict: defer Huber-delta calibration
  |-- NS-18 packet -> verdict: modified loss scaling/units
  |-- D-04 existing packet + GAP-32-01 owner resolution
  |
  v
Decision gate: any new source-silent semantic/process/cross-phase choice?
  |-- yes -> STOP, create 35-GAPS.md + v1.6-GAPS.md entry, halt dependent work
  |-- no  -> continue
  |
  v
Wave 2: framework-spec transcription
  |-- pinn_architecture.md: component math callouts/status tags
  |-- ctl_instruction.md: assembly/cross-reference callouts/status tags
  |
  v
Wave 3: verification and ledger closure
  |-- forbidden stale constructs absent or explicitly rejected/deferred
  |-- AC-LOSS-01..04 anchors present in correct files
  |-- no duplicated normative body text
  |-- GAP-32-01 resolved in both registers
  |-- M15 / NS-12 / NS-13 / NS-18 / D-04 ledger rows VERIFIED only after checks pass
```

### Recommended Project Structure

```text
.planning/phases/35-loss-energy-weight-contracts/
├── 35-RESEARCH.md          # this planner input
├── 35-*-PLAN.md            # planner-created executable phase prompts
├── 35-VALIDATION.md        # expected structural gate if planner follows Phase 34 pattern
├── 35-VERIFICATION.md      # durable verification record
├── 35-GAPS.md              # create only if a real STOP gap appears
└── evidence/
    ├── m15-energy-weight-schedule.md
    ├── ns-12-componentwise-ad.md
    ├── ns-13-energy-huber-delta.md
    └── ns-18-loss-scaling-units.md
```

### Pattern 1: Packet Before Edit

**What:** Start each Phase 35-owned row with an evidence packet that cites issue doc, resolution doc, current specs, locked conventions, engineering check, verdict, AC ID, and STOP handling. [VERIFIED: codebase grep]

**When to use:** Before editing any framework-spec text for M15, NS-12, NS-13, or NS-18. [VERIFIED: codebase grep]

**Example:**
```markdown
## Verdict

Verdict: accept-resolution

Explicit user instruction: None

Reasoning:
- Cite resolution doc section and claim rows.
- Cite current spec line ranges.
- Cite locked v1.4/v1.5 conventions where applicable.
- State whether any STOP gap opened.
```

### Pattern 2: Verdict-Status Callout

**What:** Open each new normative spec contract with a Phase 35 blockquote callout that includes requirement ID, finding ID, verdict/status, AC ID, and grounded source. [VERIFIED: codebase grep]

**When to use:** At the canonical home for each LOSS contract and at the cross-reference half when needed for status parity. [VERIFIED: codebase grep]

**Example:**
```markdown
> **Phase 35 contract: energy-loss weights (LOSS-02; M15 rejected as issue-doc replacement; AC-LOSS-02; grounded by resolution doc §1.9 and evidence/m15-energy-weight-schedule.md).**
```

### Pattern 3: Single Canonical Home + Bidirectional Pointer

**What:** Keep formulas in the owning spec file and point from the other file by stable section heading + AC ID rather than copying formula bodies. [VERIFIED: codebase grep]

**When to use:** LOSS-01/02/03/04 all span `ctl_instruction.md` and `pinn_architecture.md`; every cross-file split needs a no-duplication verifier. [VERIFIED: codebase grep]

**Example verification shape:**
```bash
python3 -c "from pathlib import Path; import re; ctl=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); pinn=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text(); assert 'AC-LOSS-02' in ctl and 'AC-LOSS-02' in pinn; assert not re.search(r'cap\\s*=\\s*\\{0:1,\\s*1:5', ctl+pinn), 'M15 cap table must not be locked'"
```

### Anti-Patterns to Avoid

- **Copying ROADMAP/REQUIREMENTS LOSS wording literally:** those files preserve superseded Phase 35 preview text; use `35-SPEC.md` and resolution verdicts. [VERIFIED: codebase grep]
- **Writing specs before packets:** D-35-09 requires packets for M15, NS-12, NS-13, and NS-18 before edits. [VERIFIED: codebase grep]
- **Creating a new evidence schema:** Phase 32 already owns the packet schema, verdict enum, and lifecycle. [VERIFIED: codebase grep]
- **Duplicating formulas in both specs:** D-35-05 requires one canonical home per body of normative text. [VERIFIED: codebase grep]
- **Closing ledger rows at `FIX_APPLIED`:** `FIX_APPLIED` is not terminal; rows close only after verification. [VERIFIED: codebase grep]
- **Using live `pinn/` code as grounding:** AGENTS and Phase 32 evidence protocol ban this for v1.6 adjudication. [VERIFIED: AGENTS.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Evidence schema | New packet format or new verdict names | Phase 32 `evidence/_TEMPLATE.md` and `README.md` | Existing schema is required by D-35-09 and downstream verification. [VERIFIED: codebase grep] |
| M15 energy schedule | New capped-hybrid schedule or dominance controller | Current PHYS-05 warmup with `λ_E^max <= 1`, plus logging | Resolution §1.9 rejects the cap table and defers automatic reweighting. [VERIFIED: codebase grep] |
| Energy Huber calibration | Per-stage `delta_E` table | `delta_E = 1.0` baseline and deferred calibration requirements | Resolution §1.13 says no measured distribution supports immediate change. [VERIFIED: codebase grep] |
| D-04 causal mode | Option-C window mechanics or dense-residual ALM | Owner-ratified Option A per-time causal weighting, scalar ALM deferred P2 | GAP-32-01 resolves D-04 to Option A and preserves dense-residual ALM rejection. [VERIFIED: codebase grep] |
| Causal exponent clipping | Numeric clip bound | Deferred/FUT note only | Resolution GAP-01 leaves the bound unset. [VERIFIED: codebase grep] |
| Verification | Manual review only | Deterministic `rg`/`python3 -c` source-token and negative checks | Phase 34 precedent uses structural source checks for specwork-only phases. [VERIFIED: codebase grep] |

**Key insight:** this phase is mostly adjudicated transcription. The risk is not algorithmic implementation complexity; it is silent spec drift from stale proposals, duplicated canonical homes, or invented deferred values. [VERIFIED: codebase grep]

## Common Pitfalls

### Pitfall 1: Stale ROADMAP/REQUIREMENTS Phrasing
**What goes wrong:** The plan transcribes the cap table, per-stage Huber range, or Option-C mechanics because those still appear in roadmap/requirements. [VERIFIED: codebase grep]
**Why it happens:** Phase 35 SPEC was created after roadmap initialization and explicitly supersedes preview text. [VERIFIED: codebase grep]
**How to avoid:** Put `35-SPEC.md` and `35-CONTEXT.md` above roadmap/requirements for LOSS semantics. [VERIFIED: codebase grep]
**Warning signs:** `cap = {0:1, 1:5, ... 6:500}`, `lambda_E = 1000`, `0.01-0.1` as a locked table, or Option-C window partitioning appears without "rejected/deferred". [VERIFIED: codebase grep]

### Pitfall 2: Packet-Edit Order Inversion
**What goes wrong:** A spec edit lands before the evidence packet for that row. [VERIFIED: codebase grep]
**Why it happens:** The current specs already contain much of the math, tempting a quick tag-only edit. [VERIFIED: codebase grep]
**How to avoid:** Planner should make packet tasks prerequisites for spec-edit tasks and include validation that packet paths exist before edited LOSS anchors close. [VERIFIED: codebase grep]
**Warning signs:** `ctl_instruction.md` or `pinn_architecture.md` changes but no Phase 35 `evidence/*.md` packet exists for M15/NS-12/NS-13/NS-18. [VERIFIED: codebase grep]

### Pitfall 3: D-04 Packet Misread
**What goes wrong:** The existing D-04 packet is treated as still blocking Option A, or as sufficient by itself to select a mode. [VERIFIED: codebase grep]
**Why it happens:** The Phase 32 packet records `defer-with-blocker`, while the later gap register records `RESOLVED-WITH-INSTRUCTION`. [VERIFIED: codebase grep]
**How to avoid:** Consume both artifacts: D-04 packet for evidence history, GAP-32-01/v1.6-GAPS for owner resolution. [VERIFIED: codebase grep]
**Warning signs:** Plan asks the user to choose D-04 again, or transcribes D-04 without confirming both gap registers. [VERIFIED: codebase grep]

### Pitfall 4: Unconditional Chain Factors
**What goes wrong:** The spec implies `2x`/`4x` factors always apply to `dr'/du` and `d²r'/du²`. [VERIFIED: codebase grep]
**Why it happens:** The roadmap shorthand is easy to read as unconditional. [VERIFIED: codebase grep]
**How to avoid:** State the canonical autograd leaf is `u=t/T`; factors apply only if differentiating directly with respect to `τ = 2u - 1`. [VERIFIED: codebase grep]
**Warning signs:** Text says `dr'/du = 2 dr'/dτ` without the `τ`-leaf condition. [VERIFIED: codebase grep]

### Pitfall 5: Canonical-Home Duplication
**What goes wrong:** Both framework specs contain full copies of the same formula or schedule. [VERIFIED: codebase grep]
**Why it happens:** Cross-file readability can be confused with duplicating normative text. [VERIFIED: codebase grep]
**How to avoid:** Put component math in `pinn_architecture.md`, assembly/cross-reference in `ctl_instruction.md`, and prove no duplicate normative body via a count check. [VERIFIED: codebase grep]
**Warning signs:** Full `lambda_E` warmup formula, causal weight formula, or Huber energy definition appears as independent normative text in both files without a pointer relationship. [VERIFIED: codebase grep]

## Code Examples

Verified patterns from local project sources:

### LOSS-02 Negative Check
```bash
python3 -c "from pathlib import Path; import re; text=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text(); assert 'AC-LOSS-02' in text; assert 'M15' in text and 'rejected' in text; assert not re.search(r'cap\\s*=\\s*\\{0:1,\\s*1:5,\\s*2:20,\\s*3:50,\\s*4:100,\\s*5:200,\\s*6:500\\}', text), 'cap table must not be locked'; assert 'lambda_E = 1000' not in text"
```

### LOSS-03 Deferred Calibration Check
```bash
python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); required=['AC-LOSS-03','NS-13','defer','delta_E = 1.0']; missing=[r for r in required if r not in text]; assert not missing, missing; assert 'per-stage Huber-delta table' not in text"
```

### D-04 Dual-Register Check
```bash
python3 -c "from pathlib import Path; a=Path('.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md').read_text(); b=Path('.planning/milestones/v1.6-GAPS.md').read_text(); assert 'GAP-32-01' in a and 'RESOLVED-WITH-INSTRUCTION' in a; assert 'GAP-32-01' in b and 'RESOLVED-WITH-INSTRUCTION' in b; assert 'Option A' in a+b"
```

### No Live-Code Grounding Guard
```bash
git diff --name-only -- pinn . ':!pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md' ':!pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md'
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Copy issue-doc M15 cap table and `λ_E = 1000` concern | Reject cap table as replacement; retain PHYS-05 max `<= 1`; log losses/weights/gradients | Resolution §1.9, Phase 35 SPEC 2026-06-26 | Planner must forbid locked cap table and dominance controller. [VERIFIED: codebase grep] |
| Change `delta_E` immediately to `0.01-0.1` or stage table | Keep `delta_E = 1.0`; defer calibration until measured distribution/occupancy/drift/gradient evidence exists | Resolution §1.13, Phase 35 SPEC 2026-06-26 | Planner must preserve baseline and route calibration to FUT. [VERIFIED: codebase grep] |
| Preserve blueprint Option-C recommendation as default | Owner ratified Option A; Option C not commissioned | GAP-32-01 resolved 2026-06-26 | Planner must not specify windowed causal-ALM mechanics. [VERIFIED: codebase grep] |
| Treat D-04 as unresolved owner decision | Consume D-04 packet plus resolved gap registers | Phase 35 SPEC gate 2026-06-26 | Planner should verify dual-register resolution rather than ask again. [VERIFIED: codebase grep] |
| Use live `pinn/` code as evidence | Framework specs and planning/evidence artifacts are grounding; live code is FUT only | User directive 2026-05-19, carried into v1.6 | Planner must avoid implementation-code evidence in Phase 35. [VERIFIED: AGENTS.md] |

**Deprecated/outdated:**
- ROADMAP Phase 35 success criteria for `lambda_E(k) = min(10^(k-3), cap[k])`, `0.01-0.1` as active Huber calibration, and Option-C preservation are superseded by `35-SPEC.md`. [VERIFIED: codebase grep]
- Issue-doc B-08/NS-18 L1/MAE data-loss language is superseded by the spec Huber data-loss contract. [VERIFIED: codebase grep]
- Dense-residual pseudo-ALM as default loss is rejected; scalar-conservation ALM is optional/deferred only. [VERIFIED: codebase grep]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| — | No unverified assumptions were used for core Phase 35 planning guidance; public web research was LOW-confidence and not used as evidence. | All | — |

## Open Questions (RESOLVED)

No blocking research questions remain for Phase 35 planning. The items below are
resolved as planning decisions or execution-time STOP checks.

1. **Do any packets surface a new source-silent field/value? — RESOLVED AS STOP CHECK**
   - What we know: `35-CONTEXT.md` says no new STOP gap was found during discussion and resolution doc §1.9 names logging categories. [VERIFIED: codebase grep]
   - Resolution: this is not an open research question. Packet authors must still perform line-range confirmation while filling evidence, and if a required field/value is not explicit they must open `35-GAPS.md` and mirror to `.planning/milestones/v1.6-GAPS.md`; they must not infer. [VERIFIED: AGENTS.md]

2. **Should Phase 35 create one plan or multiple plans? — RESOLVED BY PLANNER**
   - What we know: grouping is explicitly planner discretion if packet-before-edit and all LOSS IDs are covered. [VERIFIED: codebase grep]
   - Resolution: planning uses four PLAN.md files in three waves: packets/ledger setup, parallel framework-spec edits split by canonical file ownership, then verification/ledger closure. [VERIFIED: planner output 2026-06-27]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Git | status/diff/path guards | yes | 2.54.0 | none needed |
| Node.js | `gsd-tools.cjs`, optional spec-render-check | yes | v24.16.0 | none needed |
| `rg` | source-token searches | yes | 15.1.0 | `grep`, less preferred |
| Python | structural assertion snippets | yes | 3.14.5 | Node one-liners |
| pytest | existing Python test runner | no | — | Use direct `python3 -c` checks; Phase 35 is specwork-only |
| GSD tools | phase init/research cache | yes | no `--version` flag | direct local path already works |

**Missing dependencies with no fallback:**
- None for Phase 35 research/planning. [VERIFIED: command output]

**Missing dependencies with fallback:**
- `pytest` is unavailable, but Phase 35 can use direct source-token and structural checks. [VERIFIED: command output]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Specwork structural validation via `rg`, `git diff`, and `python3 -c`; pytest is not installed. [VERIFIED: command output] |
| Config file | none for Phase 35; no LOSS-specific validation suite exists yet. [VERIFIED: codebase grep] |
| Quick run command | `rg -n "AC-LOSS|LOSS-|M15|NS-12|NS-13|NS-18|D-04" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| Full suite command | Planner should create a Phase 35 `python3 -c` structural suite modeled on Phase 34 verification: contract tokens, forbidden stale constructs, cross-file no-duplication, gap-register state, ledger closure, protected-path diff. [VERIFIED: codebase grep] |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| LOSS-01 | NS-18/NS-12 loss scaling, Huber data, no linear momentum, conditional `τ` factors | structural/source | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['AC-LOSS-01','NS-18','modified','Huber','no linear-momentum','tau','u=t/T']; missing=[r for r in req if r not in text]; assert not missing, missing"` | no, Wave 0/plan-created |
| LOSS-02 | M15 rejected, PHYS-05 warmup retained, cap table not locked | structural/source | Use the LOSS-02 negative check in Code Examples. | no, Wave 0/plan-created |
| LOSS-03 | NS-13 deferred, `delta_E = 1.0` retained, no per-stage table | structural/source | Use the LOSS-03 check in Code Examples. | no, Wave 0/plan-created |
| LOSS-04 | D-04 Option A owner resolution transcribed, dense ALM rejected, clip bound deferred | structural/source | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['AC-LOSS-04','D-04','RESOLVED-WITH-INSTRUCTION','w_1 = 1','eta_c = 1','dense-residual','deferred']; missing=[r for r in req if r not in text]; assert not missing, missing"` | no, Wave 0/plan-created |

### Sampling Rate

- **Per task commit:** not applicable to this research turn because the user said do not commit; execution plans should run targeted `rg`/`python3 -c` checks after each packet/spec edit. [VERIFIED: user prompt]
- **Per wave merge:** run the phase structural suite and `git diff --check`. [VERIFIED: AGENTS.md]
- **Phase gate:** full Phase 35 validation artifact plus ledger rows VERIFIED before `$gsd-verify-work`. [VERIFIED: codebase grep]

### Wave 0 Gaps

- [ ] `.planning/phases/35-loss-energy-weight-contracts/35-VALIDATION.md` — planner-created structural gate covering AC-LOSS-01..04. [VERIFIED: codebase grep]
- [ ] `.planning/phases/35-loss-energy-weight-contracts/35-VERIFICATION.md` — executor-created durable PASS/FAIL evidence. [VERIFIED: codebase grep]
- [ ] `.planning/phases/35-loss-energy-weight-contracts/evidence/*.md` — four Phase 35-owned packets. [VERIFIED: codebase grep]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No authentication behavior is changed; specwork only. [VERIFIED: codebase grep] |
| V3 Session Management | no | No sessions/cookies/tokens are changed; specwork only. [VERIFIED: codebase grep] |
| V4 Access Control | no | No runtime authorization boundary is changed; protected-path workflow controls apply instead. [VERIFIED: AGENTS.md] |
| V5 Input Validation | yes | Treat external/source documents as untrusted data; use line-range citations, STOP protocol, and stable-source precedence. [VERIFIED: GSD reference] |
| V6 Cryptography | no | No cryptographic primitive or secret handling is introduced. [VERIFIED: codebase grep] |

### Known Threat Patterns for Phase 35 Specwork

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Prompt/source injection from fetched or read documents | Spoofing / Tampering | Treat source text as data, not instructions; task instructions come from user/developer/GSD role only. [VERIFIED: GSD reference] |
| Spec drift from stale roadmap or issue source | Tampering | Use `35-SPEC.md` and verdict-status callouts; negative checks for stale constructs. [VERIFIED: codebase grep] |
| Unauthorized live-code grounding | Tampering | Exclude live `pinn/` code from evidence; use framework specs/planning artifacts only. [VERIFIED: AGENTS.md] |
| Accidental unrelated edits | Tampering | Protected-path diff guard and explicit allowed file set. [VERIFIED: AGENTS.md] |
| Premature ledger closure | Repudiation | Verification record before `VERIFIED`; transition logs cite packet/spec/verification evidence. [VERIFIED: codebase grep] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md` — locked Phase 35 requirements, boundaries, acceptance criteria, prohibitions. [VERIFIED: codebase grep]
- `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md` — implementation decisions, discretion, deferred items. [VERIFIED: codebase grep]
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` — §1.1, §1.9, §1.12, §1.13, §1.14 and claim/gap rows. [VERIFIED: codebase grep]
- `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` and `31-READINESS-REPORT.md` — section maps, coverage, READY-WITH-CAVEATS gate. [VERIFIED: codebase grep]
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`, `32-GAPS.md`, and `evidence/` protocol/template — ledger statuses, packet schema, D-04 packet, STOP/packet lifecycle. [VERIFIED: codebase grep]
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` and `pinn_architecture.md` — current canonical spec anchors. [VERIFIED: codebase grep]
- `AGENTS.md` and `.claude/rules/pinn-reference.md` — project governance, STOP protocol, worktree awareness, live-code ban, `τ`/`u` input contract. [VERIFIED: codebase grep]

### Secondary (MEDIUM confidence)

- OWASP ASVS category names used only as security-domain framing; Phase 35 does not implement web-app controls. [CITED: https://owasp.org/www-project-application-security-verification-standard/]

### Tertiary (LOW confidence)

- Generic web search for the private Phase 35 questions returned no authoritative public source; result cached as LOW and not used for substantive recommendations. [VERIFIED: websearch]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all substantive stack/artifact recommendations are local project artifacts verified in this worktree. [VERIFIED: codebase grep]
- Architecture: HIGH — canonical-home split is locked in `35-CONTEXT.md` and matches current spec anchors. [VERIFIED: codebase grep]
- Pitfalls: HIGH — each pitfall corresponds to a concrete stale-source, STOP, ledger, or spec-anchor risk found in local artifacts. [VERIFIED: codebase grep]
- Public ecosystem research: LOW — no authoritative public source exists for these private phase decisions; web search was not used as evidence. [VERIFIED: websearch]

**Research date:** 2026-06-27
**Valid until:** 2026-07-04 for phase-planning purposes, or earlier if `35-SPEC.md`, `35-CONTEXT.md`, the resolution doc, or Phase 32 ledger/gap files change.

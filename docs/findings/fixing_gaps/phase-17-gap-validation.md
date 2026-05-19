---
title: "Phase 17 Gap Validation"
artifact_under_review: ".planning/phases/17-input-and-output-contracts/17-GAPS.md"
audit_basis: "<home>/Downloads/reviewing_gaps.md (Phase 17 Gap Validation Plan)"
auditor: "Read-only validation pass"
date: 2026-05-19
scope: "Read-only validation of the 11 entries in 17-GAPS.md against approved grounding sources. No modifications to 17-GAPS.md, framework specs, or .planning artifacts."
verdict_legend:
  - "valid-resolved: was a real gap when opened; already RESOLVED-WITH-INSTRUCTION with no further input needed"
  - "valid-needs-input: real gap; resolution still requires user decision"
  - "invalid: not a real gap — grounding source explicitly answers the question, gap should not have been opened"
  - "duplicate: shadows another gap; resolution belongs in the parent gap"
  - "mechanical-not-gap: presentation-only or trivially derivable; agent had latitude per CLAUDE.md/AGENTS.md mechanical-choice carve-out"
---

# Phase 17 Gap Validation

## Scope and Method

This report independently audits every entry in `.planning/phases/17-input-and-output-contracts/17-GAPS.md` against the v1.4 grounding hierarchy in CLAUDE.md / AGENTS.md / GEMINI.md "CRITICAL GOVERNANCE" block (strengthened 2026-05-19): the resolution doc, issue doc, prior user decisions (chat history, `RESOLVED-WITH-INSTRUCTION` gap entries, `NN-CONTEXT.md` `✅ LOCKED` decisions), planning artifacts (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`), Phase 16 evidence framework + ledger, v1.4-touched framework spec sections, and first-principles physics. Live `pinn/` code is excluded from grounding sources per the 2026-05-19 directive and is treated only as FUT-01 hand-off context.

Two questions are separated per gap:

1. *Was this a valid gap when opened?* — i.e., were source materials actually silent or ambiguous, given the agent's available grounding sources?
2. *Does it still require user input now?* — i.e., is the resolution note grounded enough that Phase 17 / FUT-01 can proceed without another user decision?

For `GAP-17-01` through `GAP-17-10`, the 2026-05-19 user auto-advance instruction is treated as a `prior user decision` per the grounding hierarchy. For `GAP-17-11`, the planning text in `17-03-PLAN.md` Task 2 and its `17-CODE-DIVERGENCE.md` header preamble is examined to verify whether it already labels row priorities as non-binding hints.

## Summary Table

| Gap | Impact | Status | Verdict | Resolution-doc answer present? | Current user-input need | Primary evidence |
|-----|--------|--------|---------|--------------------------------|-------------------------|------------------|
| **GAP-17-01** Mass slot encoding (raw vs fraction) | HIGH | RESOLVED-WITH-INSTRUCTION | `valid-resolved`, leans toward `invalid` | **YES — explicit** (resolution doc lines 116, 535) | None | `ctl_pinn_resolution.md:116`, `:535`; `01-architecture-and-physics-foundations.md:437,520` (issue doc fractions); `PROJECT.md` Key Decision: "resolution doc is the default verdict source per user directive 2026-05-18" |
| **GAP-17-02** AC-IO-04 invention | MEDIUM | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (process-artifact schema, not a resolution-doc question) | None | `16-CONTEXT.md` D-13 (naming policy), `16-ISSUE-LEDGER.md` (no AC-IO-04 reservation), `REQUIREMENTS.md` IO-04 (no finding ID), 2026-05-19 auto-advance |
| **GAP-17-03** AC-IO-01/02/03 pass-criteria wording | MEDIUM | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (process-artifact schema; VER-01 numeric form does not cover IO linguistic checks) | None | `REQUIREMENTS.md` VER-01, `16-CONTEXT.md` D-09, D-12, D-13; 2026-05-19 auto-advance |
| **GAP-17-04** `17-CODE-DIVERGENCE.md` schema | MEDIUM | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (process-artifact decision; no source pre-specifies divergence schema) | None | `REQUIREMENTS.md` IO-02 SC5, SCOPE-01, FUT-01; 2026-05-19 auto-advance |
| **GAP-17-05** M5 reframe to metadata-only | HIGH | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | **Partial — derivable, not literal** (resolution doc §5.5–5.6 puts `I3` in metadata; doesn't literally say "this reframes M5's Phase 20 scope") | None | `ctl_pinn_resolution.md:71–72`, `:459–465`, `:517–524` (Jacobi IC has no I3 slot), `:576–588` (metadata role), `:620` (correct affine map); 2026-05-19 auto-advance |
| **GAP-17-06** Canonical-home topical split | LOW-MEDIUM | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (operational coordination; no source pre-specifies file ownership) | None | `17-CONTEXT.md` D-04, D-05; framework spec roles (`ctl_instruction.md` = preprocessing; `pinn_architecture.md` = architecture); 2026-05-19 auto-advance |
| **GAP-17-07** Symbolic μ, σ until Phase 18 | LOW | RESOLVED-WITH-INSTRUCTION | `valid-resolved`, leans toward `mechanical-not-gap` | **YES — implicit** (resolution doc leaves μ, σ symbolic by definition: "dataset statistics computed after the full frame/gauge/scale pipeline") | None | `ctl_pinn_resolution.md:533–572`; `ROADMAP.md` Phase 18 FRAME-01; 2026-05-19 auto-advance |
| **GAP-17-08** Forward-reference wording — Phase 18 FRAME-01 | LOW | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (coordination point grounded; specific "Phase 18 (FRAME-01)" naming is agent phrasing — explicitly classified as operational coordination by CLAUDE.md/AGENTS.md) | None | `ctl_pinn_resolution.md` §5.4; `ROADMAP.md` Phase 18 FRAME-01; 2026-05-19 auto-advance |
| **GAP-17-09** Forward-reference wording — Phase 19 PHYS-02 | LOW | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (same as GAP-17-08, applied to τ / autograd-leaf / chain-rule contract) | None | `ctl_pinn_resolution.md:240–248`; `ROADMAP.md` Phase 19 PHYS-02; 2026-05-19 auto-advance |
| **GAP-17-10** Forward-reference wording — Phase 21 VER-04 | LOW | RESOLVED-WITH-INSTRUCTION | `valid-resolved` | NO (same coordination class; VER-04 is a planning-side artifact, framework specs don't reference VER-* numbering) | None | `REQUIREMENTS.md` VER-04 (updated 2026-05-19); 2026-05-19 auto-advance |
| **GAP-17-11** Row-level FUT-01 priority values in `17-CODE-DIVERGENCE.md` | MEDIUM | OPEN | `valid-needs-input` | NO (none of the grounding sources sequence the eight rows) | **YES — pick (a)/(b)/(c)/(d) per gap entry** | `17-03-PLAN.md` Task 2 (hard-coded values); `17-PATTERNS.md` (priority intuition only); `17-CONTEXT.md` D-14 (lists surfaces, not priorities); `REQUIREMENTS.md` FUT-01 (no row sequencing); GAP-17-04 schema is resolved, row values are not |

**Counts:** 1 OPEN (`valid-needs-input`) + 10 RESOLVED-WITH-INSTRUCTION (all `valid-resolved`; one leans `invalid`, one leans `mechanical-not-gap`). 0 `duplicate`, 0 `mechanical-not-gap` outright. Total = 11.

---

## Per-Gap Validation

### GAP-17-01 — Mass slot encoding (raw vs fraction)

**Verdict:** `valid-resolved` *(leans `invalid`: resolution doc explicitly answers raw vs fraction at two distinct lines that the gap entry's source-silence claim did not cite)*

**Was it a valid gap when opened?**

The gap entry's source-silence claim cites `ctl_pinn_resolution.md:540, 547` and `REQUIREMENTS.md` PHYS-01. The agent missed two more dispositive lines in the same grounding source:

- `ctl_pinn_resolution.md:116` — Final Decision Matrix row "Characteristic length and mass convention": **"Keep $D=(GT^2)^{1/3}$ and raw masses. Replace mass-fraction input channels."** This is a P0-priority direction in the resolution doc's own executive summary table.
- `ctl_pinn_resolution.md:535` — Section 5.4 opening sentence, immediately above the formulas the gap entry cited as silent: **"Mass channels must preserve absolute mass scale. Do not use mass fractions as the final input representation under raw-mass dynamics."**

This is also confirmed by `17-PATTERNS.md:156` (which transcribes line 535 verbatim) and by the issue doc's `m_norm = 2*(m_i/m_total) - 1` formula at `01-architecture-and-physics-foundations.md:437` and `:520`. The two sources do not agree on raw vs fraction; the resolution doc explicitly proposes raw, the issue doc explicitly proposes fractions. The structural class is "contested EVID-05" (sources disagree), not "source silent."

Under the milestone-level user directive 2026-05-18 — "resolution doc is the default verdict source; override only on EVID-05 evidence that the resolution-doc position fails" — the answer was already pre-committed to raw masses, before the 2026-05-19 auto-advance was issued. The gap entry's framing therefore double-recorded an answer already determined by the standing milestone directive.

**Does it still require user input now?**

No. The 2026-05-19 auto-advance applied option (a) raw, which matches the resolution doc's explicit position at lines 116 and 535, satisfies the 2026-05-18 milestone directive (default to resolution doc), and is consistent with PHYS-01 (raw-mass nondimensionalization). Mathematical grounding in the gap entry is sound: raw masses preserve absolute scale and distinguishability between SQR (constant 1.0) and hierarchical (variable) datasets; fractions would force SQR mass-slot variance to zero. `17-CONTEXT.md` D-07 records the resolved content; `17-CODE-DIVERGENCE.md` will record the v1.3-era fraction-encoding code as a forward-pointing FUT-01 hand-off note.

**Citation trail:** `ctl_pinn_resolution.md:116`, `:535`, `:537–547`; `01-architecture-and-physics-foundations.md:437`, `:520`; `17-PATTERNS.md:154–172`; `PROJECT.md` Key Decisions (line 154 — "Resolution doc is NOT authoritative in v1.4" + milestone directive 2026-05-18); `17-CONTEXT.md` D-07.

---

### GAP-17-02 — AC-IO-04 invention

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes. `16-CONTEXT.md` D-13 establishes the AC naming policy `AC-{REQ-ID}[-{NN}]` but Phase 16 only reserved `AC-IO-01` (B-03, M2), `AC-IO-02` (B-04, M1), and `AC-IO-03` (B-06) — see `16-ISSUE-LEDGER.md:21–30, 86–96`. `IO-04` is a phase-wide cleanup requirement with no finding ID (see `REQUIREMENTS.md:25`), so it has no natural per-finding AC slot. Phase 16 did not pre-commit to whether requirement-level cleanup ACs are extended to the AC-naming scheme or rolled into the Phase 17 phase-exit gate without a named AC. This is the canonical process-artifact schema gap class per the CLAUDE.md/AGENTS.md governance block.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): `AC-IO-04` is reserved as a Phase 17-local AC with pass criterion clarified by ce-doc-review 2026-05-19 ("no unqualified 11D/12D/ambiguous 13D mentions remain in normative framework-spec prose before Source Issues metadata except where labeled historical; `17-CODE-DIVERGENCE.md` exists and enumerates known Phase 17 spec↔code gaps from D-14"). The naming `AC-IO-04` is syntactically admissible under D-13 (`AC-{REQ-ID}` with REQ-ID = IO-04) and the Phase 17-local scope does not require a Phase 16 ledger row.

**Citation trail:** `16-CONTEXT.md` D-13 (lines 95–98); `16-ISSUE-LEDGER.md:21–30, 86–96`; `REQUIREMENTS.md:25, 53` (IO-04, VER-01); `17-CONTEXT.md` D-13 (lines 147–151).

---

### GAP-17-03 — AC-IO-01 / AC-IO-02 / AC-IO-03 pass-criteria wording

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes. `REQUIREMENTS.md:53` (VER-01) mandates **numerically-defined** acceptance checks with `relative_error < 1e-10` style pass criteria for PHYS/FRAME-side checks. IO-side findings (B-03, B-04, B-06, M1, M2) are linguistic-syntactic decisions about spec content, not numerical computations — they cannot map onto VER-01's numeric mold. `16-CONTEXT.md` D-13 says pass criteria "are defined in Phase 21 per VER-01," but Phase 17 needs *some* pass criteria to gate the `FIX_APPLIED → VERIFIED` transition (`16-CONTEXT.md` D-09, D-12) before phase exit. The pass-criteria wording for text/structural ACs was therefore source-silent and required either Phase 17 to write it or Phase 21 to inherit it.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): agent-proposed text/structural pass criteria are approved (`17-CONTEXT.md` D-13, lines 148–151). The criteria are structurally verifiable by grep — e.g., "exactly one canonical input-contract definition per spec, total width 14, no contradiction across files" for `AC-IO-01`; "IC₁₃ ordering matches across files, per-slot normalization named, B-04 EVID-05 record complete" for `AC-IO-02`; "9D position output, COM head formula present, AD-derived v/a defined, `ctl_instruction.md:879–880` no longer claims direct velocity output" for `AC-IO-03`. Phase 21 VER-04 may layer disposable numeric probes on top during execution.

**Citation trail:** `REQUIREMENTS.md:53` (VER-01); `16-CONTEXT.md` D-09 (lines 82), D-12 (line 93), D-13 (lines 95–98); `17-CONTEXT.md` D-13 (lines 147–151).

---

### GAP-17-04 — `17-CODE-DIVERGENCE.md` schema

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes. No upstream source specifies the schema for the divergence-register file. `REQUIREMENTS.md` IO-02 success criterion 5 and SCOPE-01 establish that divergences must be recorded and that v1.3-era code is treated as FUT-01 hand-off only; neither specifies a fields list, ordering, or format. This is a process-artifact decision with no upstream answer.

**Does it still require user input now?**

No, **for the schema itself**. 2026-05-19 auto-advance applied option (a): 5-column Markdown schema `Surface | Live code (file:line) | Spec target (Phase 17 decision) | FUT-01 item | FUT-01 priority (HIGH/MEDIUM/LOW)`. The schema is reusable across Phases 18/19/20 unless those phases surface their own variant.

The *row-level priority values* that populate the fifth column are a separate decision and are tracked under GAP-17-11 (still OPEN). GAP-17-04 resolved the schema; GAP-17-11 governs the row values.

**Citation trail:** `REQUIREMENTS.md:23` (IO-02), `:62` (FUT-01), `:71` (SCOPE-01); `PROJECT.md` Key Decisions line 158 (no-live-code directive 2026-05-19); `17-CONTEXT.md` D-14 (lines 155–166).

---

### GAP-17-05 — M5 reframe to metadata-only (Phase 20 scope change)

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes. The reframe combines two pieces:

1. **The metadata role is grounded.** `ctl_pinn_resolution.md:576–588` is explicit that `I3`, `I_norm_raw`, `I1`, `I2`, `tau_L`, etc. are "mandatory, but they are not the final network IC vector. They are used for: curriculum stage assignment; lookahead/replay sampling; diagnostics and validation; loss scaling and reporting; possible auxiliary-head or widened-input ablations." Combined with D-01 (LOCKED) — the Jacobi-state IC₁₃ at `ctl_pinn_resolution.md:517–524` has no `I3` slot — the network input under v1.4 does not feed I3.

2. **The cross-phase-scope implication is derivable, not literal.** The resolution doc does not contain the sentence "this reframes M5's Phase 20 scope." That is the planning-layer consequence: under the new IC contract, M5's contested formula (`I3_norm = 6*I3 - 1` per resolution doc vs `2*I3 - 1` per issue doc) applies only to staging metadata, not to network input. Phase 16's M5 row (`16-ISSUE-LEDGER.md:33`) was opened under the old IC framing, and the reframe changes the Phase 20 success-criterion application from "IC slot" to "metadata channel." That cross-phase reframing is the classic `cross-phase reframing` class per CLAUDE.md/AGENTS.md governance — MUST surface.

The mathematical grounding in the gap entry is sound: for `I_3 ∈ [0, 1/3]` (by triangle inequality at `ctl_pinn_resolution.md:611`), the resolution doc's `6*I3 - 1` map covers the canonical `[-1, 1]` range, while the issue doc's `2*I3 - 1` maps to `[-1, -1/3]` and misses the upper bound by a factor of 3. M5 is mathematically determined toward the resolution doc independent of the reframe question.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): M5 scope is reframed to metadata-only under the Jacobi-state IC contract. Phase 20 ARCH-03 work narrows to applying `I3_in = 6*I3 - 1` to staging metadata. The Phase 20 ARCH-03 success criterion in `ROADMAP.md` Phase 20 is preserved verbatim ("Reader can verify `I_3` maps the documented triangle-shape range to `[-1, 1]`") — only the application surface (metadata, not IC input) is narrowed by the reframe. `17-CONTEXT.md` D-10 records the reframe.

**Citation trail:** `ctl_pinn_resolution.md:71–72` (rejects invariant-only IC), `:459–465`, `:517–524` (Jacobi IC has no I3 slot), `:576–588` (metadata role), `:611` (`I_3 ∈ [0, 1/3]`), `:620` (`I_3^{in}=6I_3-1`); `01-architecture-and-physics-foundations.md:87` (issue doc's contested `2*I3 - 1`); `16-ISSUE-LEDGER.md:33` (M5 row); `ROADMAP.md` Phase 20 ARCH-03; `17-CONTEXT.md` D-10 (line 134).

---

### GAP-17-06 — Canonical-home topical split — specific topic→file assignment

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes. No source document specifies which spec file (`ctl_instruction.md` vs `pinn_architecture.md`) owns which content. The two current spec files both define overlapping (and contradictory) IO content; the natural split must be reasoned from each file's historical role. This is the canonical operational-coordination class — must log per CLAUDE.md/AGENTS.md, but minimal substantive content is unspecified.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): IC₁₃ composition + per-slot normalization primary in `ctl_instruction.md` Step 4 (data-pipeline side); network input width + τ semantics + 9D output + COM head primary in `pinn_architecture.md` §5.2–5.3 (architecture side). Secondary file carries a one-line summary + back-reference. The assignment maps to historical file roles — `ctl_instruction.md` is data/curriculum, `pinn_architecture.md` is model/AD — and the drift-prevention rule in `17-CONTEXT.md` D-04 (edit `ctl_instruction.md` first, regenerate `pinn_architecture.md` summary) closes the cross-file divergence loop.

**Citation trail:** `17-CONTEXT.md` D-04 (line 111), D-05 (line 113); spec file roles per the file headers in `pinn_instruction/markdown_conversion/framework-specs/`.

---

### GAP-17-07 — Symbolic μ, σ until Phase 18

**Verdict:** `valid-resolved` *(leans `mechanical-not-gap`: the resolution doc itself defines μ, σ symbolically; Phase 17 deferring concrete values is a natural derivation, not invention)*

**Was it a valid gap when opened?**

Marginal. `ctl_pinn_resolution.md:533–572` defines `μ_{m,i} = mean_{traj}(m_i)` and `σ_{m,i} = std_{traj}(m_i)` symbolically — the resolution doc itself does not compute numerical values, only the form. The values depend on (i) which trajectories are in the training set and (ii) the FRAME-01 preprocessing order locked in Phase 18 (`ROADMAP.md` Phase 18 FRAME-01). Phase 17 leaving μ, σ symbolic is the direct transcription of the resolution doc's stance; the only "decision" is whether to *also* compute numerical values now or defer them — and the latter is the obvious choice because Phase 18's preprocessing order is not yet locked.

The gap is on the boundary between "operational coordination" (which is MUST surface) and "mechanical / presentation-only" (agent has latitude). It was conservative to log it; it is not catastrophic that it was logged.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): μ, σ remain symbolic in Phase 17; concrete values populated downstream (Phase 18 or FUT-01 when the data pipeline is rebuilt). This is consistent with the resolution doc's own symbolic treatment and with Phase 18 owning preprocessing finalization.

**Citation trail:** `ctl_pinn_resolution.md:533–572`; `ROADMAP.md` Phase 18 FRAME-01; `17-CONTEXT.md` D-06 (lines 117–126).

---

### GAP-17-08 — Forward-reference wording — Phase 18 FRAME-01

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes, in the operational-coordination class. The coordination point (IC₁₃ is computed from preprocessed trajectories) is grounded by `ctl_pinn_resolution.md` §5.4 — the spec content is grounded. The wording choice of how to *name the downstream phase* inside the framework spec is agent invention: framework specs predate GSD planning and don't currently reference GSD phase numbers. Per the CLAUDE.md/AGENTS.md governance block, operational-coordination decisions where the coordination point is itself established are OK if minimal and factual, but **must** be logged in the gap register. Logging GAP-17-08 satisfies that rule.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): use "Phase 18 (FRAME-01)" inline in both planning artifacts and framework spec text. Trade-off accepted: precision over portability (the framework spec will need editing if phase numbering changes downstream, but the cross-phase dependency is structural enough that precision wins).

**Citation trail:** `ctl_pinn_resolution.md` §5.4 (lines 533–572); `ROADMAP.md` Phase 18 FRAME-01; `17-CONTEXT.md` D-08 (line 132).

---

### GAP-17-09 — Forward-reference wording — Phase 19 PHYS-02

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes — same operational-coordination class as GAP-17-08. The chain-rule contract is grounded by `ctl_pinn_resolution.md:240–248` and the autograd-leaf identification by `:209–250`. The naming "Phase 19 PHYS-02" inside the framework spec text is agent invention.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): use "Phase 19 (PHYS-02)" inline in planning artifacts and framework spec text. Same rationale as GAP-17-08.

**Citation trail:** `ctl_pinn_resolution.md:209–250`; `ROADMAP.md` Phase 19 PHYS-02; `17-CONTEXT.md` D-09 (line 133).

---

### GAP-17-10 — Forward-reference wording — Phase 21 VER-04

**Verdict:** `valid-resolved`

**Was it a valid gap when opened?**

Yes — same class as GAP-17-08/09. VER-04 is a planning-side artifact; framework specs do not reference VER-* numbering at all.

**Does it still require user input now?**

No. 2026-05-19 auto-advance applied option (a): mention VER-04 only in planning artifacts, not framework spec edits. This keeps the framework specs decoupled from GSD verification numbering.

**Citation trail:** `REQUIREMENTS.md:56` (VER-04, updated 2026-05-19 to remove live-code references); `17-CONTEXT.md` D-11 (line 135).

---

### GAP-17-11 — Row-level FUT-01 priority values in `17-CODE-DIVERGENCE.md`

**Verdict:** `valid-needs-input`

**Was it a valid gap when opened?**

Yes. GAP-17-04 resolved the 5-column schema and approved a `FUT-01 priority` column, but the **per-row HIGH/MEDIUM/LOW assignments** are governed by no upstream source:

- `17-CONTEXT.md` D-14 (lines 155–166) lists the divergence surfaces and FUT-01 items but contains no priority column.
- `17-PATTERNS.md:447` ("The context recommends HIGH for mass-encoding and IC composition, LOW for docstring drift") supplies intuition only; per the gap entry, this is a pattern artifact, not a governance-approved grounding source for cross-phase scheduling.
- `REQUIREMENTS.md:62` (FUT-01) does not sequence the rows.
- The schema decision (GAP-17-04) approved the *column*, not the *values*.

`17-03-PLAN.md` Task 2 hard-codes priorities for all eight rows (5 HIGH, 2 MEDIUM, 1 LOW). The gap correctly identified that those values are agent-derived cross-phase scheduling guidance with no explicit grounding source.

**Does the current planning text already label row priorities as non-binding hints?**

**Partially — but the labeling is OPEN-gap-aware framing, not yet a commitment to option (a).** Three pieces of current text are relevant:

1. `17-03-PLAN.md` Task 2 action — `"If 17-GAPS.md still lists GAP-17-11 as OPEN, stop before committing this task. The row-level FUT-01 priority values below are candidate hand-off values only until that gap is resolved."`
2. `17-03-PLAN.md` Task 2 — the proposed `17-CODE-DIVERGENCE.md` header preamble: `"Row-level FUT-01 priority values are governance-controlled by GAP-17-11; do not treat them as final while that gap is open."`
3. `17-CONTEXT.md` Decision Status Summary D-14 — `"Schema is actionable. Row-level FUT-01 priority values are blocked until GAP-17-11 is resolved."`

This text uses **conservative, OPEN-gap-aware wording** — "candidate", "do not treat them as final", "blocked" — but it does **not yet pick one of the four options listed in the gap entry**:

> - (a) Keep the current row-level values as **non-binding FUT-01 hand-off hints**; FUT-01 can re-prioritize.
> - (b) Keep the current row-level values as **binding Phase 17 priority guidance** for FUT-01.
> - (c) Replace ungrounded priority values with `TBD by FUT-01` while keeping the priority column.
> - (d) User supplies exact HIGH/MEDIUM/LOW values for all eight rows.

Saying "candidate values until the gap resolves" is *not* the same as saying "the values are non-binding hand-off hints" (option a) — the former is a status assertion, the latter is a final framing. Furthermore, `17-03-PLAN.md` Task 2 explicitly gates the Phase 17 commit on GAP-17-11 being resolved: `"If 17-GAPS.md still lists GAP-17-11 as OPEN, stop before committing this task."` Phase 17 cannot complete until the gap is resolved.

**Does it still require user input now?**

**Yes.** The user needs to select one of (a) / (b) / (c) / (d). The 2026-05-19 auto-advance applied to GAP-17-01..10; GAP-17-11 was discovered after by `ce-doc-review` and is explicitly noted in `17-GAPS.md` line 18 (`"GAP-17-11 was discovered later by ce-doc-review and remains OPEN"`) and in the milestone-wide index `.planning/milestones/v1.4-GAPS.md:32`. The auto-advance authorization does *not* cover this gap.

**Confidence of impact:** MEDIUM per gap entry — affects FUT-01 sequencing and reader expectations, not the Phase 17 IO spec contracts themselves.

**Citation trail:** `17-03-PLAN.md` Task 2 (lines 190–210, especially the "candidate hand-off values" sentence at lines 191 and 198); `17-CONTEXT.md` Decision Status Summary D-14 row (line 68); `17-PATTERNS.md:447`; `17-CONTEXT.md` D-14 table (lines 155–166); `REQUIREMENTS.md:62` (FUT-01); `.planning/milestones/v1.4-GAPS.md:32`.

---

## Remaining User Decisions

Only one Phase 17 gap requires further user input:

### GAP-17-11 — Row-level FUT-01 priority values in `17-CODE-DIVERGENCE.md`

The 5-column schema is resolved (GAP-17-04). The HIGH/MEDIUM/LOW values currently in `17-03-PLAN.md` Task 2 (5 HIGH for IC vector composition / mass encoding / orientation slots / time input / COM projection head; MEDIUM for direct velocity output wording / metadata-only invariants; LOW for docstring drift) are agent-derived. The user must pick one of:

- **(a) Non-binding FUT-01 hand-off hints.** Keep the current row-level values as initial hints; FUT-01 may re-prioritize without amending Phase 17. Phase 17 ships a final-status `17-CODE-DIVERGENCE.md` with a header sentence stating the priorities are non-binding hand-off intuition.
- **(b) Binding Phase 17 priority guidance.** Keep the current row-level values as final and commit Phase 17 to the eight-row priority assignment. FUT-01 inherits the priorities without re-prioritization.
- **(c) `TBD by FUT-01`.** Replace ungrounded values with `TBD by FUT-01` while keeping the column. Phase 17 records the surfaces but explicitly defers per-row sequencing.
- **(d) User supplies exact values.** Override the agent-derived assignments with explicit user-provided HIGH/MEDIUM/LOW for each of the eight rows.

The agent-recommended option per the gap entry's "Agent was tempted to" line is **(a)** with an explicit non-binding sentence in the divergence file. The plan currently uses OPEN-gap-aware language ("candidate values until the gap resolves") but has not committed to (a).

Confidence of impact per the gap entry: **MEDIUM**. The decision affects FUT-01 sequencing and reader expectations but does not affect any Phase 17 input/output spec contract.

---

## Gaps Where Resolution-File Is Silent But Prior User Instruction Resolves the Decision

The 2026-05-19 user auto-advance instruction ("auto advance now yourself without having to ask for my user input") is recorded in `17-GAPS.md` line 18 and `v1.4-GAPS.md:18` as authorization to apply GAP-17-01 through GAP-17-10's "Agent was tempted to" option. Per the v1.4 grounding hierarchy in CLAUDE.md/AGENTS.md (a `prior user decision` is a grounding source), this instruction itself supplies the missing grounding for every gap in this list. **None of these gaps still require further user input.**

| Gap | Resolution-doc explicit answer? | Prior user instruction that resolves | Final framing |
|-----|--------------------------------|--------------------------------------|---------------|
| GAP-17-01 | YES (`:116`, `:535`) — overlooked in gap entry source-silence claim | 2026-05-18 milestone directive ("default to resolution doc") + 2026-05-19 auto-advance | Raw ordered masses; v1.3 mass-fraction code routed to FUT-01 hand-off |
| GAP-17-02 | NO (process-artifact schema) | 2026-05-19 auto-advance | AC-IO-04 Phase 17-local with pass criterion clarified by ce-doc-review 2026-05-19 |
| GAP-17-03 | NO (process-artifact schema; VER-01 numeric form excludes IO) | 2026-05-19 auto-advance | Agent-proposed text/structural pass criteria approved |
| GAP-17-04 | NO (no source pre-specifies schema) | 2026-05-19 auto-advance | 5-column Markdown schema |
| GAP-17-05 | PARTIAL (metadata role explicit at `:576–588`; cross-phase reframe is derivable) | 2026-05-19 auto-advance | M5 scope reframed to metadata-only under Jacobi IC |
| GAP-17-06 | NO (no source pre-specifies file ownership) | 2026-05-19 auto-advance | Proposed topical split confirmed |
| GAP-17-07 | YES — implicit (resolution doc itself uses symbolic μ, σ) | 2026-05-19 auto-advance | μ, σ symbolic in Phase 17, concrete downstream |
| GAP-17-08 | NO (coordination point grounded; specific phrasing is operational coordination) | 2026-05-19 auto-advance | "Phase 18 (FRAME-01)" inline in both planning and spec text |
| GAP-17-09 | NO (same class as GAP-17-08) | 2026-05-19 auto-advance | "Phase 19 (PHYS-02)" inline in both planning and spec text |
| GAP-17-10 | NO (same class as GAP-17-08) | 2026-05-19 auto-advance | VER-04 in planning artifacts only |

Notable observations:

- **GAP-17-01 over-cautious classification.** The gap's source-silence claim cited only `ctl_pinn_resolution.md:540, 547`, missing the explicit `:116` (Final Decision Matrix: "Replace mass-fraction input channels") and `:535` (§5.4 opening: "Do not use mass fractions as the final input representation under raw-mass dynamics"). Both lines are inside the same grounding source. The decision was *already* grounded by the resolution doc independent of the auto-advance; the milestone-level 2026-05-18 directive (default to resolution doc) would also have resolved it. Logging the gap was conservative but the source state was contested disagreement between resolution doc (raw) and issue doc (fractions), not silence. This is an EVID-05 candidate that fell naturally under B-04's already-flagged EVID-05 work.
- **GAP-17-07 borderline mechanical.** The resolution doc itself leaves μ, σ symbolic; the gap's classification as "operational coordination" rather than "mechanical / presentation-only" is conservative. No harm — the outcome is the same — but useful to flag the boundary.
- **GAP-17-05 cross-phase reframe** is the most consequential reframing: it narrows Phase 20's M5 scope to staging metadata. This is correctly classified as `cross-phase reframing` per the governance block. The 2026-05-19 auto-advance authorization applied option (a), and the math grounding in the gap entry independently confirms the resolution doc's `6*I3 - 1` map is the correct affine map (`I_3 ∈ [0, 1/3]` → `[-1, 1]`).

---

## Verification

- [x] All 11 gaps received a verdict (one of `valid-resolved`, `valid-needs-input`, `invalid`, `duplicate`, `mechanical-not-gap`).
- [x] Each verdict has at least one cited source trail (resolution doc line, issue doc line, planning artifact citation, or Phase 16 ledger reference).
- [x] No live-code evidence is used to validate any spec decision. All references to `pinn/` files in this report (e.g., `pinn/data-processing-pipeline-full.py` for the v1.3-era mass-fraction code) are framed as **forward-pointing FUT-01 hand-off context only**, not as v1.4 evidence.
- [x] The only `valid-needs-input` gap (GAP-17-11) has an explanation of why no grounding source or prior instruction resolves it: GAP-17-04 resolved the schema but not the values; `17-PATTERNS.md` intuition is not a governance-approved source; `REQUIREMENTS.md` FUT-01 does not sequence rows; the 2026-05-19 auto-advance only covered GAP-17-01..10. The gap entry options (a)/(b)/(c)/(d) require explicit user selection.
- [x] No `.planning/` artifacts, framework specs, or other files were modified by this validation. Only this findings report was created.
- [x] After this report is written, `git diff --name-only` should show only `docs/findings/fixing_gaps/phase-17-gap-validation.md` plus the pre-existing dirty-tree changes that were present before validation began (none of those are touched by this task).

---

*Validation performed 2026-05-19 against `17-GAPS.md` as last-updated 2026-05-19. The gap register is treated as the artifact under review; this report does not amend it.*

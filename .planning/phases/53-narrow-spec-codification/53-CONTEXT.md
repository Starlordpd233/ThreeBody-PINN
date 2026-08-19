# Phase 53: Narrow Spec Codification - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 53 lands the four VER-20 routing items that carry **no open research
question** (`52-VER-20-ROUTING-HANDOFF.md` items (a)–(d)) as framework-spec
text. Each is a **transcription of an owner ruling that already exists** but was
never written into the spec:

| Req | Ruling being transcribed | Ruled |
|---|---|---|
| SPEC-02 | GAP-45-03 option A — the PHYS-05 per-stage `λ^max(k)` table is **locked**, not defaulted | 2026-07-24 |
| SPEC-03 | GAP-45-03's exposed gap — no spec convention distinguishes a locked constant from an illustrative default inside a table | 2026-07-24 |
| SPEC-04 | GAP-45-01 option A — `L_data` reduces as **mean over time, bodies, and spatial components** | 2026-07-31 |
| SPEC-05 | GAP-44-01 option A — the held-out physics gate's aggregate statistic is **worst-case max** over trajectories | 2026-07-23 |

**Ungated.** Roadmap: "Depends on: Nothing — ungated first v2.3 phase (ratified
sequencing track A). Runs in parallel with Phases 54 and 55." Phase 53 exists so
that "a worst-case v2.3 still discharges four of the five routed amendments" —
its value is that it ships **regardless of how the recalibration lands**.
Preserving that independence is a design constraint on every decision below, not
an incidental property.

**Not this phase.** The recalibration itself (item (e) — `η_c` / `R̄`
normalization / `ω₀` / `N_t`) is Phases 54 and 56. SPEC-01 and SPEC-06 are not
touched here. No value carrying a SCOPE-38 contract marker (`η_c`,
`first_omega_0`, the causal-exponent clip's underflow-only purpose) is changed
by this phase — roadmap Success Criterion 5 makes that an assertion Phase 53
must be able to **defend**, so the plans must show the reasoning, not just claim it.

</domain>

<decisions>
## Implementation Decisions

**Delegation of authority.** The owner selected all four gray areas and then
instructed (2026-08-19): *"run all the areas worth discussing yourself by
choosing the best option automatically following your best judgement and logical
reasoning grounded in the mathematics, physics, and codebase. no need to ask the
user for their input unless the decision is very important and can create a
bigger impact later."*

This is an **owner-delegated resolution**, the same pattern as GAP-45-04
("the implementer selects and records the clip") and GAP-46-01 ("delegated
ruling 2026-07-26"). It is the grounding authority for D-01..D-06. Note the
boundary: SCOPE-34's "never agent-decided" rule binds **the recalibration
decision** (`η_c` / normalization / SIREN-scale / `N_t`), which is Phase 54/56
content and is *not* delegated by this instruction. Phase 53's wording and
placement questions are what was delegated.

The escalation carve-out the owner named — *"unless the decision is very
important and can create a bigger impact later"* — was applied. Where it fired,
the item is recorded in **Open Items for Owner Visibility** below rather than
decided silently.

### Locked-vs-default convention (SPEC-03)

- **D-01: Apply the convention to §4.1's PHYS-05 values ONLY. Do not sweep the rest of the file. Record the un-swept tables as a routed inventory.**

  GAP-45-03's ruling text ends with *"Generalization to other spec tables NOT
  decided."* That is an explicit owner **withholding**, not an omission, so a
  sweep would reverse a standing ruling. It is also concretely hazardous: the
  sharpest instance of the systemic problem is §2.4's table header
  (`pinn_architecture.md:253`), which reads **"Recommended Value"** while listing
  `first_omega_0 | 30` — a value §2.2:167 locks (*"fixed at 30 and is not
  scheduled during training"*) and that **Phase 56 may amend under SCOPE-38**.
  Stamping it LOCKED in Phase 53 would couple this phase to the recalibration
  outcome, destroying the independence that is Phase 53's entire reason to exist.
  §9's "Definitive Specification" table (`:978`–`:992`) is worse — it mixes locked
  (`epsilon_train=1e-5`, PHYS-03) with explicit defaults (`λ_IC=1`, `δ_r=1`),
  so marking it means ~15 fresh status adjudications no ruling covers.

  The deliverable required by SPEC-03 is *"add a spec convention"* — the
  convention is added and demonstrated at one site. Universal application was
  never in the requirement text.
  — **Reversibility:** reversible — a later phase extends the sweep by adding
  markers; nothing has to be undone.

- **D-02: Notation is an inline ASCII marker — `**[LOCKED]**` / `**[DEFAULT]**` — declared in one short dedicated subsection, and defined as attaching to a *value*, not to a table row.**

  Two alternatives were rejected on mechanical grounds:
  - *Add a Status column to tables.* **Structurally impossible at the one site
    Phase 53 applies it to** — §4.1's PHYS-05 values are bulleted LaTeX
    (`:658`–`:664`), not a markdown table. A column cannot mark them.
  - *Reuse the existing `> **Phase NN contract:**` blockquote as the only locking
    mechanism.* Under-delivers: routing item (b) is specifically about marking
    values **"within the same table"**, and a blockquote adjacent to a table
    cannot say which row it binds.

  A value-attached inline marker is the only form that works across markdown
  tables, prose bullets, and LaTeX lines alike — which the spec has all three of.

  **ASCII, not emoji.** These specs are converted-from-LaTeX Markdown headed for
  the deferred Final Publication LaTeX Sync milestone, and the repo actively
  polices render fidelity (`tools/spec-render-check/`). A `🔒` glyph is a
  round-trip hazard; `**[LOCKED]**` survives both renderers and greps cleanly —
  which matters because GAP-45-03 obligation 4 already requires preflight to
  assert the whole PHYS-05 table, and a greppable marker lets a test tie spec
  text to that assertion.

  **Scope of the convention's authority:** state that it governs both framework
  specs (`pinn_architecture.md`, `ctl_instruction.md`), but make **zero marker
  edits in `ctl_instruction.md`** — declaring intent costs nothing and prevents
  an incoherent half-convention; applying markers there would expand the diff for
  an item with no instance in that file.
  — **Reversibility:** costly — once other sections adopt the marker, changing
  the syntax means re-marking every site plus any preflight or grep-based check
  keyed on the literal string.

### `L_data` reduction (SPEC-04)

- **D-03: Correct the displayed formula, add the prose sentence, AND land a contract block. Not prose-only.**

  The formula at `pinn_architecture.md:304` currently reads
  `L_data = (1/N_t) Σ_n Σ_i Huber(...)` — mean over time, **sum** over bodies,
  with the spatial reduction left undefined inside a Huber applied to a vector.
  GAP-45-01's ratified reading is mean over time, bodies, and components.
  The gap record's own evidence pins the factor: mean `0.1539..0.1630` vs sum
  `1.3852..1.4673`, *"exactly 9×"* — and 9 = 3 bodies × 3 spatial components.
  So the displayed formula computes **9× the ratified quantity**.

  Prose-only fails the phase's own Success Criterion 3 (*"a reader can determine
  the `L_data` reduction from spec prose alone, without consulting `pinn/`"*): a
  reader who reads the formula gets the wrong answer. The formula must be
  corrected to the explicit triple sum with `1/(N_t · N_b · d)` normalization
  (equivalently `1/(9 N_t)` at `N_b = 3, d = 3`).

  **Code already conforms** — `pinn/loss_catalog.py:262` computes
  `_huber(residual, ...).mean()` over a `(N_t, 3, 3)` tensor, and its docstring
  at `:252` states the reduction as `sum(Huber) / (9 * N_t)`. CONF-07 is Complete.
  **This phase changes no code.** The edit closes a spec-vs-ruling divergence,
  not a spec-vs-code one.

  **Why this does not fire SCOPE-38:** SCOPE-38 triggers on changing a value or
  formula that carries an owner-ratified **contract marker**, and enumerates
  three (`η_c`, `first_omega_0`, the clip's underflow-only purpose). The
  `L_data` reduction is on none of them. The adjacent LOSS-01 / AC-LOSS-01 block
  (`:307`) fixes scaling and units and assigns component-math ownership — it does
  **not** fix the reduction. The reduction was genuinely undetermined, which is
  precisely why GAP-45-01 had to exist. Correcting it **resolves an ambiguity
  rather than superseding a ruling.** The plan must state this reasoning in the
  edit so SC-5 is defensible on inspection.
  — **Reversibility:** reversible — a text correction aligning spec to an
  existing owner ruling and to shipped code; no dependent artifact assumes the
  old normalization.

### Held-out physics gate statistic (SPEC-05)

- **D-04: New `## 10.6` subsection in `pinn_architecture.md` §10 Numerical Acceptance Checks. Do NOT place it in `ctl_instruction.md`'s per-stage ADVANCE gate.**

  **This is the finding that decided it, and it is a correctness issue rather
  than a placement preference.** The only "held-out" hit in either framework spec
  is `ctl_instruction.md:1939` — and that gate is the **per-stage curriculum
  ADVANCE gate** (a conjunction of four criteria evaluated on a 10–20% per-stage
  hold-out, with all its numeric thresholds marked *"provisional pending FUT
  Stage-0 pilot calibration"*). GAP-44-01 ruled on a **different object**: the
  terminal held-out **physics** evaluation — `ε_H`, threshold `1e-5`,
  `SCS = log10(max)`, the single-look budget SCOPE-35 governs and v2.2 preserved
  unspent. Writing the max statistic at `:1939` would **conflate two distinct
  gates**.

  §10 (`:1014`) is already the register of numeric acceptance contracts (§10.1
  Scaling Consistency … §10.5 Loss Stability Dry Run), so §10.6 adds no new
  structure. LOSS-01's ownership precedent points the same way: `ctl_instruction.md`
  owns methodology and total-loss assembly, `pinn_architecture.md` owns numeric
  and component contracts — an aggregate statistic over a metric is the latter.

- **D-05: Write the statistic as max over held-out trajectories, and do not define the within-trajectory reduction.**

  GAP-44-01 is explicit and bounded: *"the gate fails if ANY trajectory exceeds
  `1e-5`, headline `max = 237.2086056078468` … consistent with
  `SCS = log10(max)`"*, with *"mean/median stay quoted as distribution facts."*
  So §10.6 states: max over held-out trajectories of the per-trajectory `ε_H`
  **as already defined**; fail-if-any-exceeds-`1e-5`; `SCS = log10(max ε_H)`;
  mean and median are explicitly **non-gating** distribution facts.

  It must **not** define how `ε_H` reduces *within* a trajectory (final value vs
  max over time). GAP-44-01 did not rule on that axis. If the planner finds that
  axis undefined in the spec, it is a **gap to route** — not a Phase 53 invention.

  Include one disambiguating sentence stating §10.6 is distinct from the per-stage
  ADVANCE gate, because the conflation risk above is real and a reader needs the
  boundary drawn.
  — **Reversibility:** reversible — additive subsection; no existing text depends
  on its absence.

### Ratification-marker schema (all four edits)

- **D-06: Use the house contract-block pattern with the requirement ID plus the originating GAP ruling. Mint no new AC-namespace IDs.**

  Form:
  `> **Phase 53 contract: <topic> (<SPEC-NN>; <GAP-ID> owner ruling <date>, option <X>; grounded by <full relative path>).**`

  There are 26 `> **Phase NN contract:**` blocks and 2 `guard` blocks across the
  two spec files — this is unambiguously the house pattern for landing a ratified
  ruling, and Phase 53's edits should be indistinguishable in form from them.

  **No new `AC-*` IDs at discuss time.** In this repo the `AC-*` namespace denotes
  an acceptance check *defined by a phase plan* (AC-LOSS-01..04 came from v1.6
  Phase 35's plans), and the STOP protocol names new AC IDs as process-artifact
  schema. The authority for each Phase 53 edit is a **GAP ruling**, and citing
  `GAP-45-01 / GAP-45-03 / GAP-44-01` with date and option letter is strictly
  more traceable than a freshly minted ID. If the plans define acceptance checks,
  they get IDs through the normal GSD planning mechanism — not invented here.
  This also keeps VER-21's traceability check clean against 15 requirements with
  no phantom namespace.
  — **Reversibility:** reversible — citation format; an AC ID can be added later
  if a plan defines a check that needs one.

### Claude's Discretion

Delegated to the planner/executor without owner input — none of these change a
ratified quantity:

- **Plan decomposition.** One plan or several across SPEC-02..05. Note that
  SPEC-02 and SPEC-03 are coupled (SPEC-02's instance is closed *by* the
  convention, per roadmap SC-2), so they should land together or in a fixed order.
- **Commit granularity** within `scripts/agent-commit` discipline.
- Exact section number if `## 10.6` collides with concurrent work.
- Exact prose wording, provided every ruling's date, option letter, and source
  path are carried.

### Open Items for Owner Visibility (non-blocking)

Recorded per the owner's escalation carve-out. None blocks planning.

1. **§2.4's "Recommended Value" header stays wrong after Phase 53.** Under D-01
   the spec will carry a declared LOCKED/DEFAULT convention while
   `pinn_architecture.md:253` still labels `first_omega_0 = 30` a "Recommended
   Value". This is deliberate — it is the value Phase 56 may amend under
   SCOPE-38, and reconciling it belongs to the phase that is already editing
   §2.2/§2.4 territory. **Routed to Phase 56**, first item of the D-01 inventory.
2. **Correcting a displayed formula (D-03) is a larger edit than "reword".**
   Judged in-scope because SC-3 cannot be met otherwise and the SCOPE-38
   reasoning above holds. Flagged so the owner can review it at Phase 53 close.
3. **`ε_H`'s within-trajectory reduction may be undefined** (D-05). If the
   planner confirms it is, that is a **new gap** — create
   `.planning/milestones/v2.3-GAPS.md` (standing trigger; it does not exist yet)
   plus `53-GAPS.md`, and route it. Do not resolve it inside Phase 53.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Edit targets (the only files Phase 53 may modify)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — §3.1 (`:292`–`:310`, `L_data`), §4.1 (`:633`–`:684`, PHYS-05 / `λ_phys^max`), §10 (`:1014`+, Numerical Acceptance Checks). The primary and expected-sole edit target.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — **read-only in Phase 53 under D-02/D-04.** `:1930`–`:1945` is the per-stage ADVANCE gate; read it to confirm the D-04 distinction, do not edit it.

### Authorizing rulings (the grounding for every edit)
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` — items (a)–(d) verbatim; the routing authority for this phase.
- `.planning/milestones/v2.1-GAPS.md` — GAP-45-03 (`:12`, SPEC-02/03, incl. the "Generalization … NOT decided" clause), GAP-45-01 (`:13`, SPEC-04, with the 9× magnitude evidence), GAP-44-01 (`:11`, SPEC-05, max/`SCS = log10(max)`).
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` — full records for GAP-45-01 and GAP-45-03 (the index above is the summary).
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md` — full GAP-44-01 record. (The v2.1 index cites the pre-archive path `.planning/phases/44-.../44-GAPS.md`, which no longer resolves; the archived path above is verified 2026-08-19.)

### Governing scope and milestone frame
- `.planning/REQUIREMENTS.md` — SPEC-02..05 texts (`:87`–`:90`); SCOPE-33 (narrow spec-edit authorization), SCOPE-34, SCOPE-37, SCOPE-38 (`:114`–`:119`).
- `.planning/ROADMAP.md` — Phase 53 detail block: goal, "Depends on: Nothing", and the five Success Criteria the plans must satisfy.
- `CLAUDE.md` — STOP protocol, gap-register required fields, Git commit protocol (`scripts/agent-commit`, `GIT_AGENT_ID`, `GIT_AGENT_OWNED_PATHS`, no blanket staging).

### Conformance context (read-only — do not edit code in this phase)
- `pinn/loss_catalog.py:246`–`:262` — `data_huber_loss`; docstring `:252` states `sum(Huber) / (9 * N_t)`. Confirms code already satisfies GAP-45-01; D-03 changes spec only.
- `.planning/milestones/v2.2-REQUIREMENTS.md:45` — CONF-07, Complete: the `L_data` reduction was already implemented per GAP-45-01.

### Tooling that constrains the notation choice (D-02)
- `tools/spec-render-check/` — render-detector suite; the reason the marker is ASCII rather than emoji.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **The `> **Phase NN contract:**` blockquote pattern** — 9 blocks in `pinn_architecture.md`, 18 in `ctl_instruction.md` (plus 2 `guard` blocks). Copy the form exactly; see `pinn_architecture.md:667` (Phase 35 / LOSS-02) and `:307` (Phase 35 / LOSS-01) as the closest models.
- **§10 Numerical Acceptance Checks** (`:1014`) — an existing register of numeric acceptance contracts, §10.1–§10.5. D-04's §10.6 extends it rather than inventing structure.
- **`pinn/loss_catalog.py`** — the authority on what the shipped reduction actually is; use it to verify the corrected formula, not to derive it (the ruling is the authority).

### Established Patterns
- **Spec files are converted-from-LaTeX Markdown.** Preserved author comments live inline (e.g. `pinn_architecture.md:306` *"Author Comment: again, the syntax is broken"*, directly under the `L_data` formula; and `:249` under §2.4). These are tracked in "Source Issues / Notes for Future Reconciliation" (`:1043`). **Do not remove them** — cleanup is not a VER-20 item and SCOPE-33 does not authorize it. Edit around them.
- **Contract blocks record provenance densely** — requirement ID, option letter, date, grounding path. Phase 53 matches this density (D-06).
- **PHYS-05's values are prose bullets, not a table** (`:658`–`:664`) — the single most load-bearing structural fact for D-02.

### Integration Points
- **GAP-45-03 obligation 4** already requires preflight to assert the whole PHYS-05 table at run start and every stage boundary. D-02's greppable marker is chosen so a test can tie spec text to that assertion; wiring such a test is **not** Phase 53 scope.
- **Phase 56** edits §2.2/§3.2 of the same file. Phase 53 touches §3.1, §4.1, §10 and adds one convention subsection — **disjoint**, so the two can proceed in parallel. Phase 53 must not touch §2.2, §2.4, or §3.2.

</code_context>

<specifics>
## Specific Ideas

- Owner instruction, 2026-08-19: decide the gray areas directly using judgement
  grounded in the mathematics, physics, and codebase; escalate only decisions
  that are *"very important and can create a bigger impact later."* Recorded as
  data — it is the authority for D-01..D-06 and does not extend to Phase 54/56's
  recalibration decision, which SCOPE-34 reserves to the owner.
- The `L_data` 9× factor is not abstract: GAP-45-01 recorded both readings against
  retained-run magnitudes (mean `0.1539..0.1630`, sum `1.3852..1.4673`). Cite
  those numbers in the edit's contract block — they are what makes the ruling
  legible to a later reader.

</specifics>

<deferred>
## Deferred Ideas

- **Sweeping the locked/default convention across §2.4 and §9** — deferred by
  D-01. GAP-45-03 explicitly left generalization undecided; §2.4's
  `first_omega_0` row is coupled to Phase 56's possible SCOPE-38 amendment.
  Phase 53 records the inventory; a future phase applies it.
- **A cross-reference from `ctl_instruction.md` to the new §10.6** — improves
  navigability, but routing item (d) does not require it and it would add a
  second edited file. Deferred.
- **Removing the stray preserved author comments** (`:249`, `:306`) — not a
  VER-20 item; SCOPE-33 does not authorize it. Belongs to a future spec-hygiene
  pass alongside SI-PINN-002/003.
- **A preflight/CI test asserting spec markers against the PHYS-05 preflight
  assertion** — enabled by D-02's greppable marker, but tooling work is outside
  Phase 53's spec-text scope.

</deferred>

---

*Phase: 53-narrow-spec-codification*
*Context gathered: 2026-08-19*

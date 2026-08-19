# Phase 53: Narrow Spec Codification - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-19
**Phase:** 53-narrow-spec-codification
**Areas discussed:** SPEC-03 convention (scope + notation), SPEC-04 formula vs prose, SPEC-05 gate-statistic home, ratification-marker schema

---

## Owner delegation (governs every area below)

The owner selected all four presented areas, then instructed:

> *"Also, run all the areas worth discussing yourself by choosing the best
> option automatically folloowing your best judgement and logical reasoning
> grounded in the mathematics, physics, and codebase. no need to ask the user
> for their input unless the decision is very important and can create a bigger
> impact later"*

Treated as an **owner-delegated resolution** — the same pattern as GAP-45-04
(*"the implementer selects and records the clip"*) and GAP-46-01 (*"delegated
ruling 2026-07-26"*). Boundary recorded in CONTEXT.md: this does **not** extend
to Phase 54/56's recalibration decision, which SCOPE-34 reserves to the owner.

One item met the escalation carve-out and was surfaced rather than buried —
§2.4's "Recommended Value" header remaining unmarked after Phase 53, recorded
under **Open Items for Owner Visibility** in CONTEXT.md and routed to Phase 56.

---

## SPEC-03 — locked-vs-default convention: scope of application

| Option | Description | Selected |
|--------|-------------|----------|
| A — §4.1 only, silent | Declare the convention, apply to PHYS-05 values only, say nothing about the rest | |
| B — full sweep | Declare, then retro-mark every table in `pinn_architecture.md` (§2.4, §9) | |
| C — §4.1 + routed inventory | Declare, apply to PHYS-05 values, record the un-swept tables as a routed follow-up | ✓ |

**Choice:** C (agent-decided under delegation) → **D-01**
**Rationale:** GAP-45-03's own text ends *"Generalization to other spec tables
NOT decided"* — an explicit owner withholding, so B reverses a standing ruling.
B is also concretely hazardous: §2.4's header (`:253`) labels `first_omega_0 =
30` a "Recommended Value" while §2.2:167 locks it, and Phase 56 may amend it
under SCOPE-38 — marking it in Phase 53 would couple this phase to the
recalibration outcome and destroy the independence that is Phase 53's reason to
exist ("ships regardless of how the recalibration lands"). §9's table (`:978`–
`:992`) mixes locked (`epsilon_train=1e-5`) with explicit defaults (`λ_IC=1`,
`δ_r=1`), so a sweep means ~15 unruled status adjudications. C over A because a
silent omission would look like an oversight rather than a preserved ruling.

---

## SPEC-03 — locked-vs-default convention: notation mechanism

| Option | Description | Selected |
|--------|-------------|----------|
| A — inline value marker | Dedicated convention subsection + `**[LOCKED]**` / `**[DEFAULT]**` attached to values | ✓ |
| B — Status column | Add a status column to marked tables plus a per-table legend | |
| C — reuse contract blockquotes | Declare that a value is locked iff a `> **Phase NN contract:**` block binds it | |

**Choice:** A (agent-decided under delegation) → **D-02**
**Rationale:** B is **mechanically impossible at the one site Phase 53 applies
it to** — §4.1's PHYS-05 values are bulleted LaTeX (`:658`–`:664`), not a
markdown table, so no column can mark them. C under-delivers against routing
item (b), which is specifically about marking values *"within the same table"*;
an adjacent blockquote cannot say which row it binds. A is the only form that
works across markdown tables, prose bullets, and LaTeX lines — the spec has all
three.
**Notes:** ASCII rather than emoji, because these specs are converted-from-LaTeX
Markdown headed for the deferred LaTeX Sync milestone and `tools/spec-render-check/`
actively polices render fidelity; `**[LOCKED]**` also greps cleanly, which lets a
future test tie spec text to the preflight assertion GAP-45-03 obligation 4
already requires. Convention declared as governing both framework specs, with
zero marker edits in `ctl_instruction.md`.

---

## SPEC-04 — correct the formula, or add prose only

| Option | Description | Selected |
|--------|-------------|----------|
| A — formula + prose | Correct the displayed LaTeX to the triple sum with `1/(N_t·N_b·d)` | |
| B — prose only | Leave the formula, add a superseding note | |
| C — formula + prose + contract block | A, plus a `Phase 53 contract:` block citing GAP-45-01 | ✓ |

**Choice:** C (agent-decided under delegation) → **D-03**
**Rationale:** `:304` currently reads `(1/N_t) Σ_n Σ_i Huber(...)` — mean over
time, **sum** over bodies — which computes 9× the ratified quantity (GAP-45-01's
own evidence: mean `0.1539..0.1630` vs sum `1.3852..1.4673`, *"exactly 9×"*;
9 = 3 bodies × 3 components). B therefore fails the phase's own Success
Criterion 3 (*"determine the reduction from spec prose alone"*): a reader who
reads the formula gets the wrong answer. C over A because 26 contract blocks
across the two files make the blockquote the house pattern for landing a
ratified ruling.
**Notes:** `pinn/loss_catalog.py:262` already computes `.mean()` over `(N_t,3,3)`
with its docstring at `:252` stating `sum(Huber)/(9*N_t)` — CONF-07 Complete, so
**no code change follows**. SCOPE-38 does not fire: its three enumerated
contract markers are `η_c`, `first_omega_0`, and the clip's underflow-only
purpose; the `L_data` reduction is on none of them, and the adjacent LOSS-01
block fixes scaling/units and ownership but not the reduction — which is exactly
why GAP-45-01 had to exist. Escalation carve-out applied: recorded as Open Item 2
for owner review at phase close, since "correct a formula" is a larger edit than
"reword".

---

## SPEC-05 — where the worst-case-max statistic lives

| Option | Description | Selected |
|--------|-------------|----------|
| A — `ctl_instruction.md` success gate | Place near `:1939`, the existing held-out mention | |
| B — `pinn_architecture.md` §10.6 | New subsection in Numerical Acceptance Checks | ✓ |
| C — both | Normative in `ctl_instruction.md`, cross-referenced in `pinn_architecture.md` | |

**Choice:** B (agent-decided under delegation) → **D-04**, **D-05**
**Rationale:** A is not a placement preference but a **correctness error**.
`ctl_instruction.md:1939` is the **per-stage curriculum ADVANCE gate** — four
criteria on a 10–20% per-stage hold-out, thresholds marked *"provisional pending
FUT Stage-0 pilot calibration"*. GAP-44-01 ruled on a different object: the
**terminal held-out physics evaluation** (`ε_H`, `1e-5`, `SCS = log10(max)`, the
single-look budget SCOPE-35 governs). Placing the statistic at `:1939` conflates
two distinct gates. §10 (`:1014`) is already the register of numeric acceptance
contracts (§10.1–§10.5), so §10.6 invents no structure; LOSS-01's ownership
precedent (methodology → `ctl_instruction.md`, numeric contracts →
`pinn_architecture.md`) agrees. C rejected as an unnecessary second edited file.
**Notes:** D-05 bounds the transcription to what GAP-44-01 actually ruled — max
over held-out *trajectories*, fail-if-any-exceeds-`1e-5`, `SCS = log10(max ε_H)`,
mean/median explicitly non-gating. The **within-trajectory** reduction of `ε_H`
was not ruled on and must **not** be invented; if the planner finds it undefined,
that is a new gap requiring `.planning/milestones/v2.3-GAPS.md` (does not exist
yet — standing trigger) plus `53-GAPS.md`. Recorded as Open Item 3.

---

## Ratification-marker schema for all four edits

| Option | Description | Selected |
|--------|-------------|----------|
| A — mint `AC-SPEC-02..05` | New acceptance-criterion IDs in the house pattern | |
| B — requirement ID + originating GAP | `(SPEC-NN; GAP-ID owner ruling <date>, option <X>; grounded by <path>)` | ✓ |
| C — no marker | Plain prose edits with no contract block | |

**Choice:** B (agent-decided under delegation) → **D-06**
**Rationale:** C discards the house pattern (26 contract + 2 guard blocks) and
loses provenance. A mints a new ID namespace at discuss time: in this repo `AC-*`
denotes an acceptance check *defined by a phase plan* (AC-LOSS-01..04 came from
v1.6 Phase 35's plans), and the STOP protocol names new AC IDs as
process-artifact schema. B is strictly more traceable — the authority for each
edit **is** a GAP ruling, so citing it with date and option letter beats a fresh
ID — and keeps VER-21's traceability clean against 15 requirements with no
phantom namespace. Plan-defined acceptance checks still get IDs through the
normal GSD mechanism.

---

## Claude's Discretion

- Plan decomposition across SPEC-02..05 (noting SPEC-02 and SPEC-03 are coupled —
  roadmap SC-2 closes SPEC-02's instance *by* the convention, so ordering matters).
- Commit granularity within `scripts/agent-commit` discipline.
- Exact subsection number if `## 10.6` collides with concurrent work.
- Exact prose wording, provided each ruling's date, option letter, and source
  path are carried.

## Deferred Ideas

- Sweeping the convention across §2.4 and §9 — deferred by D-01; §2.4's
  `first_omega_0` row routed to Phase 56.
- A cross-reference from `ctl_instruction.md` into the new §10.6.
- Removing the preserved author comments at `:249` and `:306` — not a VER-20
  item; SCOPE-33 does not authorize it.
- A CI test asserting spec markers against the PHYS-05 preflight assertion —
  enabled by D-02's greppable marker, but tooling is outside Phase 53's scope.

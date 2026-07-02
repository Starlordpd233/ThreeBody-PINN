# Phase 35: Loss & Energy-Weight Contracts - Context

**Gathered:** 2026-06-27
**Status:** Ready for planning

> **Mode note:** Discussed under `--all --auto` (all gray areas auto-selected,
> recommended option taken per area), then **stopped before planning** per user
> instruction. Every decision below is operational/transcription discipline
> grounded in the locked `35-SPEC.md`, the resolution-doc verdicts, and the
> Phase 32/33/34 precedent. **No new STOP-protocol gap was found** — Phase 35
> invents no semantic spec content; the four loss verdicts are already settled
> by the SPEC. The STOP obligation stays armed for execution (D-35-09).

<domain>
## Phase Boundary

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

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

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

</spec_lock>

<decisions>
## Implementation Decisions

### Verdict-status transcription convention

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

### Canonical-home split & anti-duplication (SI-PINN-003 guardrail)

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

### Per-contract transcription targets (what each edit asserts)

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

### Adjudication: packet-before-edit & ledger lifecycle

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

### Hard prohibitions (must-NOT, from SPEC + STOP protocol)

- **D-35-12:** No framework-spec edit introduces, as a locked/default construct:
  the issue-doc `λ_E` cap table, a fabricated per-stage Huber-δ table, Option-C
  window mechanics, a numeric causal-exponent clip bound, default dense-residual
  ALM, or a `λ_E = 1000` premise. Each may appear only as explicitly
  rejected/deferred. (SPEC Prohibitions + Constraints; STOP protocol.)

### Claude's Discretion (forward to planner)

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

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked phase requirements
- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md` — the 4 locked LOSS
  requirements, boundaries, `AC-LOSS-01..04`, prohibitions. **Authoritative WHAT;
  supersedes the stale ROADMAP/REQUIREMENTS phrasing.**

### Candidate verdict source (consume, do not re-litigate)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
  — **§1.1** (D-04 causal mode), **§1.9** (M15 energy-weight), **§1.13** (NS-13
  energy Huber-δ), **§1.14** (NS-18 loss scaling/units); supporting CAU-01..05 /
  GAP-01..02, M15-01..04 / DGR-09..10, NS13-01..03 / DGR-14, NS18-01..04.
- `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md`
  — finding→section map, status table, caveat routing (READY-WITH-CAVEATS gate).

### Framework specs — edit targets (SCOPE-13)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` —
  canonical component math: §3.1 `L_data` Huber, §3.2 `L_phys^causal`, §3.3 `L_IC`,
  §3.4 `L_E` (`δ_E = 1.0`) + shared collocation, §3.5 `L_L`, §4.1 PHYS-05 warmup
  (`λ_E^max ≤ 1`) + deferred causal clip; §2.4 total-loss formula.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` —
  canonical training-methodology/assembly: Total-Loss / Data-Flow section
  (~1718–1745, Phase 34 D-34-15 skeleton); CURR callout style at ~1630, 1832.

### Phase 32 evidence, ledger & gaps (consume + close)
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`
  — rows for M15, NS-12, NS-13, NS-18, D-04; the lifecycle Phase 35 advances.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md`
  and `evidence/README.md` — packet schema + protocol/lifecycle to reuse.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md`
  — GAP-32-01 (D-04 Option A, RESOLVED-WITH-INSTRUCTION) to confirm.

### Phase 35 gap register (create on first STOP gap)
- `.planning/phases/35-loss-energy-weight-contracts/35-GAPS.md` — created only if a
  packet/edit surfaces a source-silent semantic decision (D-35-09).
- `.planning/milestones/v1.6-GAPS.md` — milestone-wide index; mirror any new gap +
  confirm GAP-32-01 resolved.

### Transcription-convention precedent (reuse, do not re-derive)
- `.planning/phases/34-training-loop-batch-construction-contracts/34-CONTEXT.md` —
  D-34-04/05/06 (canonical-home split), D-34-07/08/09 (callout convention),
  D-34-10/11/12 (packet-before-edit), D-34-15 (total-loss skeleton boundary).
- `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md` — original
  blockquote-callout convention + GAP packet-first/defer precedent.

### Locked-convention grounding (SCOPE-12 hard constraints)
- `.planning/REQUIREMENTS.md` — SCOPE-12 (locked v1.4/v1.5 outcomes: 14D `[τ, IC₁₃]`,
  raw-mass `D ≈ 4.6416` not `6.694`, `eps_soft = 1e-5`, SCS gate), SCOPE-13/14/15
  (specwork-only / FUT boundaries), VER-13..18 (acceptance/ledger discipline).
- `.claude/rules/pinn-reference.md` — locked input/output contract (`τ = 2u − 1`,
  autograd leaf `u`) grounding the LOSS-01 `τ`/`u` chain-factor distinction.

</canonical_refs>

<code_context>
## Existing Code Insights

(Spec-authoring phase — "code" here = the framework-spec documents being edited.)

### Reusable Assets
- **Existing loss math in `pinn_architecture.md`** already implements the settled
  verdicts: data Huber `δ_r = 1` (§3.1), causal weighting with `stopgrad` (§3.2),
  energy Huber `δ = 1.0` (§3.4), PHYS-05 schedule `λ_E^max ≤ 1` (§4.1), deferred
  causal-exponent clip (§4.1 ~640–642). Phase 35 **tags** this, mostly does not
  rewrite it.
- **Phase 32 `evidence/_TEMPLATE.md` + `README.md`** — packet schema reused as-is.
- **Phase 33/34 callout + cross-ref conventions** — reused verbatim (D-35-02/05).

### Established Patterns
- **Verdict-status blockquote callout** (`> **Phase NN contract: … (ID; verdict;
  AC; grounded by …).**`) — the file-internal house style for v1.6 contracts.
- **Single canonical home + bidirectional stable-anchor pointer** — the
  SI-PINN-003 anti-duplication discipline; verifier must *prove* no duplicated
  normative text.
- **Packet → ledger transition → re-verify** — `PENDING → IN_PROGRESS →
  FIX_APPLIED → VERIFIED`, "fix applied" ≠ closure.

### Integration Points
- `ctl_instruction.md` (assembly) ↔ `pinn_architecture.md` (component math) via
  stable-anchor cross-references; the Phase 34 D-34-15 total-loss skeleton's opaque
  loss terms are the seam Phase 35 fills by reference.
- The Phase 32 issue ledger is the coordination point Phase 35 advances; **Phase 36**
  consumes the closed ledger + AC list and executes the numeric acceptance checks
  via disposable probes (VER-15) — Phase 35 does not run them.

</code_context>

<specifics>
## Specific Ideas

- The `τ`/`u` chain-factor `2`/`4` distinction (LOSS-01) is grounded in
  first-principles calculus on the locked `τ = 2u − 1` map with autograd leaf `u`
  — transcribe it as an explicit clarification, not a new derivation to debate.
- Verdict labels to surface literally in the specs so a verifier can grep them:
  `LOSS-01`/`NS-18`/`modified`; `LOSS-02`/`M15`/`rejected`; `LOSS-03`/`NS-13`/`defer`/
  `delta_E = 1.0`; `LOSS-04`/`D-04`/`RESOLVED-WITH-INSTRUCTION`/`locked`; plus the
  no-linear-momentum-loss statement and the `AC-LOSS-01..04` IDs.

</specifics>

<deferred>
## Deferred Ideas

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

*(No phase todos matched Phase 35 scope — `todo.match-phase 35` returned 0 matches.)*

</deferred>

---

*Phase: 35-loss-energy-weight-contracts*
*Context gathered: 2026-06-27*

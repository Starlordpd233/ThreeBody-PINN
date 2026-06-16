# Phase 29 Gap Register

STOP-protocol gaps surfaced during Phase 29 (Acceptance Checks, Re-verification, and
Handoff). Milestone index: `.planning/milestones/v1.5-GAPS.md`.

---

## GAP-29-01 — Gold-completeness reconciliation action scope

- **Decision point:** Does Phase 29 *promote* the 117 validated standard-gold reruns into
  the canonical gold dataset and apply the 184 → 67 framework-spec / AC / dataset cascade,
  or does it reconcile *only* the planning/governance/ledger layer and **defer** the
  dataset-mutation + framework-spec edits to a separate ruling?
- **Where in artifact:** `29-SPEC.md` Req 5 — Target: *"which 117 outputs are
  validated/**promoted or intentionally left staged**"* — and the Constraint *"staged
  validation, promotion into canonical output folders, documentation updates, and
  normative spec/ledger updates ... are separate states and must not be collapsed."*
- **Task context:** discuss-phase gray-area surfacing for Phase 29 (gold/PSC
  reconciliation area), `--all --auto` invocation, 2026-06-16.
- **Classification:** **semantic + cross-phase reframing** — it sets whether the terminal
  v1.5 phase mutates the canonical `simulation_data/` gold dataset and edits LOCKED M13 /
  AC-PIPE-05 rulings, versus staying spec-side.
- **Source silence:** `29-SPEC.md` Req 5 names *both* dispositions ("promoted or
  intentionally left staged") without choosing; the SPEC Constraint declares the states
  separate but does not say which Phase 29 *performs*; the 2026-06-14 user ruling
  (agent-memory `missing-67-gold-decision`, "How to apply" item 6) flags the M13/AC edits
  as *"a semantic change to a LOCKED ruling — surface, do not silently invent,"* and
  records that execution was deliberately held read-only.
- **Mathematical / engineering grounding:** `AC-PIPE-05` is a **set-difference probe**:
  it asserts `{standard IDs} − {gold IDs} == standard_quasi_random_ids_not_in_gold.md`,
  currently **184/184 and VERIFIED**. The specs are internally consistent *at 184* only
  because the 117 successes are **unpromoted** (gold = 2,565; 0 promoted). Promotion
  changes `{gold}` by +117, which forces a coupled, largely-irreversible cascade:
  `not_in_gold.md` 184 → 67 → `AC-PIPE-05` must assert 67/67 (else it fails) → runner
  `EXPECTED_ID_COUNT` 184 → 67 → Set-2b / issue-02 counts 2,565 → 2,682 → M13/GAP-26-01
  packet records OI-7b partial. PSC's pooled population depends on the final gold count;
  settling that count discharges PSC's *data* dependency but not the *composition* choice
  (GAP-28-03). Promotion mutates the canonical dataset (precedent: the Phase 24 DATA-05
  swap did mutate `simulation_data/`), so it is feasible-in-scope but consequential.
- **Agent was tempted to:** under pure `--auto`, auto-select "record the reconciliation"
  and write CONTEXT.md in a single pass — which would silently resolve a semantic /
  cross-phase scope decision the SPEC and the user both left open.
- **What the user needs to decide:**
  - **(A)** Reconcile the planning/governance/ledger layer only; defer the dataset
    promotion + framework-spec/AC cascade to a separate explicit ruling.
  - **(B)** Full promote + cascade now (gold 2,565 → 2,682 + all 6 cascade edits, each
    LOCKED-ruling edit with an explicit sign-off line).
  - **(C)** Document-only — record the reconciliation table but touch no records at all.
- **Confidence of impact:** **HIGH** — determines the terminal milestone's end-state
  consistency and whether LOCKED rulings + the canonical dataset are mutated at closure.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-16) — **Option A**. Phase 29
  reconciles only the planning/governance/ledger layer to the locked 117-validated /
  67-permanent-absent / 0-promoted fact (issue-ledger gold rows kept VERIFIED with an
  OI-7b-partial note; GAP-28-03 + GAP-26-01 rationale reframed; STATE.md gold-framing
  reconciled; `29-UAT.md` reconciliation table + stale-artifact inventory). The dataset
  promotion of the 117 and the 184 → 67 framework-spec/AC cascade are **NOT performed in
  Phase 29** and remain **DEFERRED** to a separate explicit user ruling, recorded as a
  FUT-01 forward obligation in `29-CODE-DIVERGENCE.md`. PSC/VAL-04 stays DEFERRED
  (GAP-28-03); its blocker is reframed from "wait for gold completion" to "gold settled;
  composition awaits explicit GAP-28-03 reopen." The M13/GAP-26-01 packet update is a
  factual-outcome record grounded by `29-SPEC.md`; the LOCKED M13 verdict is untouched,
  and if execution finds the packet edit reads as re-adjudication it must re-surface.
- **Resolution note:** User selected Option A in the discuss-phase 29 AskUserQuestion
  (2026-06-16). The embedded DEFERRED sub-item (promote + cascade) is tracked by this gap
  until the user explicitly reopens it. No PSC composition and no reinterpretation of the
  67 permanent holes was invented.

---

*Phase: 29-acceptance-checks-re-verification-and-handoff*
*Register opened: 2026-06-16*

# Phase 39 Gap Register

## GAP-39-01 — Authoritative `data_version_hash` producer

- **Decision point:** Define the authoritative producer, serialization location,
  and generation algorithm for `data_version_hash`. Phase 39 can compare an
  expected value with supplied metadata, but cannot manufacture authoritative
  metadata without this decision.
- **Where in artifact:** `39-SPEC.md` DATA-03 and `39-CONTEXT.md` D-05.
- **Task context:** Recording implementation decisions for the DATA-03
  compare-and-refuse seam.
- **Classification:** operational coordination.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md:153`
    explicitly leaves the production mechanism open (U-12) while requiring the
    adapter to implement compare-and-refuse only.
  - `.planning/REQUIREMENTS.md` DATA-03 requires mismatch refusal but does not
    designate a producer, canonical payload, or metadata location.
  - `39-SPEC.md` DATA-03 locks a typed `DataVersionHashDeferred` outcome for an
    absent field; it deliberately does not invent the missing producer.
- **Mathematical / engineering grounding:** Version comparison is meaningful
  only when both sides derive from the same stable identity function over the
  same corpus/metadata scope. A locally chosen file-order or text-format hash
  could change for non-semantic formatting differences, or fail to change for a
  semantic change outside its chosen payload. A hard mismatch refusal therefore
  needs a ratified producer; the typed deferral keeps the unverified state
  observable without falsely claiming compatibility.
- **Agent was tempted to:** Generate a local manifest or file-content hash so
  the compare path always has a value. This would silently choose scope,
  ordering, normalization, and storage semantics that the sources reserve.
- **What the user needs to decide:**
  - **A.** Designate the authoritative data producer, canonical payload, and
    metadata location for `data_version_hash`.
  - **B.** Explicitly retain the typed absent-field deferral until the upstream
    PIPE contract is supplied.
  - **C.** Supply a specific owner-maintained sidecar/manifest contract to use
    as the canonical source.
- **Confidence of impact:** HIGH — an unratified hash can make the safety check
  either spuriously reject unchanged data or silently accept incompatible data.
- **Status:** DEFERRED — non-blocking for the locked compare/refuse plus typed
  deferral seam. It blocks a claim of mandatory version enforcement where the
  metadata field is absent.
- **Resolution note:** User instruction, 2026-07-13: “follow your best
  judgement.” Agent judgment chooses option B: retain the typed absent-field
  deferral and do not invent a producer, payload, or sidecar contract in Phase
  39. Revisit only when an upstream canonical producer is ratified.

## GAP-39-02 — DATA-01 single-reader rule versus Phase 38 fixture loader

- **Decision point:** Resolve whether DATA-01's requirement that the new
  adapter is the only `pinn/` component reading the on-disk `.txt` format
  includes the pre-existing Phase 38 verification fixture loader.
- **Where in artifact:** `39-SPEC.md:28-30` and `:89`; `39-CONTEXT.md` D-02.
- **Task context:** Validating the DATA-01 implementation boundary before
  planning the new adapter.
- **Classification:** cross-phase reframing.
- **Source silence:**
  - `39-SPEC.md:28-30` calls the new adapter the sole `.txt` importer, and
    `:89` makes that a grep-verified acceptance criterion; it does not name an
    exception or migration for `pinn/verification/fixture_loader.py`.
  - `pinn/verification/fixture_loader.py:12-16,235-237,300-323` resolves and
    parses Brutus/IC `.txt` files through direct reads, and its module contract
    says it is deliberately not the Phase 39 adapter.
  - `tests/phase38/test_prohibitions.py:48-60,158-160,254-258` treats that
    fixture loader as a Phase 38 module and actively consumes it in retained
    verification coverage. Neither the roadmap nor requirements specifies
    whether it must be exempted, migrated, or replaced.
- **Mathematical / engineering grounding:** The sole-reader rule prevents two
  production parsers from diverging on record identity, completeness, and
  numerical interpretation. The existing loader instead supplies evidence
  probes and has a separately tested read-only contract. Narrowing the rule to
  the production ingestion surface preserves the probe; migrating or delegating
  the probe changes its provenance and Phase 38 regression surface. These are
  materially different system boundaries and cannot be inferred from a grep
  phrase.
- **Agent was tempted to:** Exempt the loader by narrowing the grep to new
  Phase 39 modules. That is plausible but changes the universal requirement.
  Alternatively, making the loader delegate to the adapter would modify a
  completed Phase 38 artifact and expand Phase 39's scope.
- **What the user needs to decide:**
  - **A.** Narrow DATA-01 to the production ingestion surface and explicitly
    exempt the Phase 38 probe-local fixture loader from the single-reader grep.
  - **B.** Require the fixture loader to delegate parsing to the Phase 39
    adapter, with Phase 38 regression coverage included in scope.
  - **C.** Retire/replace the fixture loader and define a new verification
    boundary, accepting the corresponding Phase 38 scope change.
- **Confidence of impact:** HIGH — without a ruling, no implementation can both
  preserve the existing Phase 38 probe contract and satisfy the stated
  repository-wide grep criterion.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-01 planning.
- **Resolution note:** User instruction, 2026-07-13: “follow your best
  judgement.” Agent judgment chooses option A: the DATA-01 single-reader rule
  applies to the production ingestion surface. Preserve
  `pinn/verification/fixture_loader.py` as the sole existing, probe-local Phase
  38 exception; it is neither the admitted-set adapter nor a reusable production
  parser. The Phase 39 reader audit must allow that exact module and fail on any
  other non-adapter on-disk reader.

---

**Milestone-index follow-up:** `.planning/milestones/v2.0-GAPS.md` is currently
claimed by another active session. Do not overwrite that shared index; add the
GAP-39-01 deferred and GAP-39-02 resolved entries once the owner releases the
claim or coordinates the update.

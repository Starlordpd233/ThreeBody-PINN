# Phase 26: DataLoader Ingestion and Selection Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-12
**Phase:** 26-dataloader-ingestion-and-selection-contracts
**Mode:** `--all --auto` — `[--all/--auto] Selected all gray areas: Spec-edit strategy, Evidence-packet workflow & batching, User-decision findings, Acceptance-check definitions.` Recommended options auto-selected by Claude per explicit user instruction ("go with the default recommended options ... stop before you start planning"); each selection logged below with its grounding.
**Areas discussed:** Spec-edit strategy, Evidence-packet workflow & batching, User-decision findings (D-03 gate / M13 fallback), Acceptance-check definitions

---

## Spec-edit strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Consume resolution-doc part-6 text as candidate edits | Transcribe unless spec/dataset/first-principles evidence shows failure (Phase 25 D-09 discipline); locked conventions are hard constraints | ✓ |
| Author contracts independently, use resolution doc as one input among equals | Discards the candidate-verdict-source standing REQUIREMENTS.md assigns the doc | |
| Transcribe resolution-doc proposals as authority | Violates the source-treatment policy (doc is NOT authoritative) | |

`[auto] Spec-edit strategy — Q: "How do the six contracts get their text?" → Selected: "Consume part-6 proposed spec text as candidate, transcribe-unless-evidence-fails" (recommended default; grounded in REQUIREMENTS.md source-treatment policy + 24.5-RESOLUTION-MAP §3 + Phase 25 D-09).`

`[auto] Spec-edit strategy — Q: "Which file hosts the contracts?" → Selected: "ctl_instruction.md primary; pinn_architecture.md only for architecture-side statements" (recommended default; grounded in the ledger Spec Targets column — D-03 row names ctl alone).`

---

## Evidence-packet workflow & batching

| Option | Description | Selected |
|--------|-------------|----------|
| Packet-before-edit per finding; M11 extends existing packet; G-rows close with parents; autonomous findings first, user-gate findings isolated | Follows evidence/README.md D-03 enforcement, GAP-25-01 split reading, GAP-25-02 legend, Phase 25 D-12 | ✓ |
| Author all six packets up front, then edit in one pass | Front-loads adjudication; weaker evidence-to-edit locality; not the README's "immediately before its edits" rule | |
| New M11 packet separate from m11-m12-severity.md | Duplicates an adjudicated record; breaks the ledger's existing Evidence-Packet link | |

`[auto] Workflow — Q: "Packet authorship pattern?" → Selected: "One packet per finding immediately before its edit; M11 reuses/extends m11-m12-severity.md; G1–G4 close with parents" (recommended default; grounded in evidence/README.md, GAP-25-01/02 resolutions, Phase 25 D-12).`

`[auto] Workflow — Q: "Finding order?" → Selected: "B-06, B-11, M11, D7 autonomous chain; M13 and D-03 in dedicated user-interaction plans" (recommended default; operational coordination, logged per governance; grounded in dependency-scoped blocking practice).`

---

## User-decision findings (D-03 format gate / M13 fallback)

| Option | Description | Selected |
|--------|-------------|----------|
| D-03: dedicated non-autonomous user-gate plan; M13: full Q-A4+OI-7 read then adopt-if-grounded else STOP gap | Honors PIPE-10's "user decides" verbatim and roadmap criterion 4's STOP-gap mandate; precedent 23-02/24-04 | ✓ |
| Auto-select HDF5 now (resolution doc recommends it) | Violates PIPE-10 — the format choice is reserved to the user; --auto cannot override a requirement-level user gate | |
| Pre-decide M13 fallback in this discussion | Violates the STOP protocol — the fallback is exactly the decision the roadmap says is surfaced, not invented | |

`[auto] User gates — Q: "How are PIPE-10 and PIPE-05's user-reserved decisions handled?" → Selected: "Execution-time user gates: non-autonomous D-03 evidence-presentation plan; M13 adopt-if-fully-grounded else GAP-26-NN" (recommended default; grounded in REQUIREMENTS.md PIPE-10 verbatim + ROADMAP Phase 26 criterion 4 + STOP protocol). Note: this is the one area where "recommended default" means routing the decision to the user, not making it.`

---

## Acceptance-check definitions

| Option | Description | Selected |
|--------|-------------|----------|
| Each packet defines its reserved AC numerically (criterion, data, command) and Phase 26 executes it via disposable probe before closure | Matches VER-07 wording + roadmap verification-protocol step 3 + README AC-ID section; Phase 29 re-executes the suite | ✓ |
| Define ACs but defer all execution to Phase 29 | Conflicts with the verification protocol (step 3 runs in the owning phase) and the phase-exit rule (VERIFIED requires a passing check) | |
| Build the full reusable acceptance suite now | Phase 29 scope (VER-09); over-builds in the owning phase | |

`[auto] Acceptance checks — Q: "Define only, or define and run?" → Selected: "Define numerically in the packet AND execute per finding via disposable probe" (recommended default; grounded in ROADMAP verification protocol step 3 + evidence/README.md phase-exit rule + VER-07).`

---

## Claude's Discretion

- Packet filenames for the five new packets (README sanitization rule).
- Spec heading/numbering placement inside `ctl_instruction.md`.
- Wave structure and plan count (within D-09/D-11/D-12 constraints).
- Inline probe commands vs small probe scripts under the phase dir.

## Deferred Ideas

- Phase 27 contracts (M12, precision, dt_out/stage-query, compute_globals; G5).
- Phase 28 metric contracts (SCS edit per the EVID-10 record).
- Phase 29 acceptance suite, SI-ledger reconciliation, FUT-01 handoff.
- Doc-03 items (M16, G6, training-loop metric usage).
- FUT-01 DataLoader implementation.

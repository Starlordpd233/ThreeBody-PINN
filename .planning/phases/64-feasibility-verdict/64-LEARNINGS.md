---
phase: 64
phase_name: "Feasibility Verdict"
project: "Three-Body Physics-Informed LLM"
generated: "2026-10-26"
counts:
  decisions: 8
  lessons: 6
  patterns: 7
  surprises: 5
missing_artifacts:
  - "64-UAT.md"
---

# Phase 64 Learnings: Feasibility Verdict

Phase 64 wrote the owner-facing feasibility verdict and the project charter from Phase 60's sealed handoff, without training anything. The frozen rule's label RETHINK-REPRESENTATION is stated unamended, beside the evidence that every network learned only each body's average position, with the ladder position (Level 1), the cost on this Mac and unranked candidate fixes for v2.5. At owner checkpoint ① the owner decided `change-course`; every charter row was recorded open. Extracted from 64-01..64-07 PLAN/SUMMARY, 64-VERIFICATION.md (independent gsd-verifier pass, PASS-WITH-OBSERVATIONS), 64-CHECKPOINT-1-RULING.md, STATE.md (Phase 64 decisions) and the v2.4 gap index. No UAT file exists for this phase.

## Decisions

### State the frozen label exactly, with the evidence beside it
The verdict is RETHINK-REPRESENTATION, the frozen rule's output for "G2 fired and the sweep rescued nothing", and it stays unamended; the time-constant-predictor evidence sits beside it, and design and recipe fixes are listed unranked for trainex-r5.

**Rationale:** the label is pre-registered and mechanical; the observation qualifies how to read it without re-setting a rule after the result.
**Source:** STATE.md (Decisions from Phase 64 and from the Phase 64 discussion), 64-04-SUMMARY.md

### Cost is measured hours on this Mac, never GPU figures
The cost section gives measured machine hours on this Mac plus a labelled for-scale figure; the rented-GPU wording in ROADMAP criterion 3, FEAS-06 and FEAS-10 was removed because it contradicted the owner's standing rule.

**Rationale:** all computation runs on the owner's Mac (PROJECT.md Constraints); a GPU route is not an option the verdict may cost.
**Source:** STATE.md (Decisions from the Phase 64 discussion), 64-VERIFICATION.md (Observation O-1)

### Apply only what the owner's ruling records
The owner sent one message, "let's change course". It decides V-1 and addresses none of the fourteen charter rows and gives no blanket approval, so every C-row is recorded `open`. PROJECT.md, the twelve skipped-phase requirement statuses and both framework specs stay byte-identical to the phase base.

**Rationale:** under the page's own rule an item not mentioned, without a blanket approval, is recorded open; nothing is inferred and the owner is not re-asked when the reply is unambiguous about what it addresses.
**Source:** 64-06-SUMMARY.md, 64-07-SUMMARY.md

### The verifier never imports the producer
The verifier keeps its own id-to-key table, its own CPU formulas and its own render rules; the producer imports no verifier code.

**Rationale:** agreement between two independent implementations is evidence; a shared implementation would only agree with itself.
**Source:** 64-02-SUMMARY.md

### Sum floats in the sealed order with an explicit loop
Every exactly-compared float sum uses `ordered_sum`, a left-to-right `+=` loop from 0.0 in handoff arm order, which reproduces the sealed total 22.37828873402778.

**Rationale:** `math.fsum` and any sorted order land one ulp below, and builtin `sum()` matches only on CPython 3.9 and 3.11.
**Source:** 64-01-SUMMARY.md, 64-02-SUMMARY.md

### Fail closed before the rule runs
The `inputs` check rejects a sweep outcome other than `no_rescue` and a panel other than `[1632, 851, 4658]` before re-deriving the label, so a silently changed input cannot reach the rule as a different-but-plausible verdict.

**Rationale:** a re-derivation that accepts any input proves nothing about the sealed one.
**Source:** 64-01-SUMMARY.md

### Literal floors, not derived counts
`EXPECTED_PATHSPEC_COUNT` is the literal 45, `VERDICT_REQUIRED_COUNT` 161 and `EVIDENCE_INDEX_COUNT` 22, never derived from the lists they check; the novelty denial is required as the positive sentence "No novelty claim is made".

**Rationale:** a count derived from its own list cannot catch a list that silently shrinks, and a negated phrase must not satisfy a phrase check.
**Source:** 64-01-SUMMARY.md, 64-04-SUMMARY.md

### The ruling check runs only-if, and quotes are never parsed
The `ruling` mode checks applied edits in the only-if direction, so 64-06 can pass it before 64-07 applies anything; the owner's quote sits in an opaque fence that is never machine-read, and a quote that closes its fence early is refused.

**Rationale:** the owner's words must be recorded byte-for-byte, never policed or reinterpreted by a parser.
**Source:** 64-05-SUMMARY.md

---

## Lessons

### Python 3.12 changed builtin sum()
CPython 3.12 switched `sum()` to compensated summation, so a float total sealed under a plain loop is reproduced by `sum()` only on 3.9 and 3.11.

**Context:** re-deriving the sealed 22.378-hour total.
**Source:** 64-01-SUMMARY.md

### A number check does not check the words around the number
The `numbers` check enforces that every verdict-marked entry renders; it does not check scope words. The verdict said "across the seven arms" for a range that is the three Rung-1 systems' gap, although 64-02 had already flagged that wording as loose. The independent verifier caught it (G-1), and it was fixed in `67c31af6`.

**Context:** the constant-gap sentence in 64-VERDICT.md.
**Source:** 64-VERIFICATION.md (G-1, section 10), 64-02-SUMMARY.md

### Path and text identity traps
A `tempfile` path under `/var` resolves through `/private/var`, so `relative_to` on an unresolved root raised; a cited token carried the micro sign (µ) where the source has superscript five (⁵); a test anchor matched a backticked mention before the real heading.

**Context:** verifier and test construction in 64-01, 64-02 and 64-04.
**Source:** 64-01-SUMMARY.md, 64-02-SUMMARY.md, 64-04-SUMMARY.md

### An empty-line pattern can hide the real defect
The `**Requirements**:` pattern required a space after the colon, so a present-but-empty line failed as "found 0" instead of "lists no requirement ID"; both failed closed, but the message hid the defect.

**Context:** the requirements-line check.
**Source:** 64-01-SUMMARY.md

### "Approve all" is the only blanket answer
A reply that addresses no charter row leaves every row open: the page's own rule records an unmentioned item as open unless the owner gives a blanket approval, and the ruling record's closed vocabulary (one verbatim block plus a 15-row answers table, GAP-64-02) made that outcome mechanical rather than a judgment. Even "approve all" would not have covered C-6 or C-7.

**Context:** owner checkpoint ①.
**Source:** 64-06-SUMMARY.md, .planning/milestones/v2.4-GAPS.md (GAP-64-02 and its disposition note)

### The quick-run target was not met
The Phase 64 unit suite took 82 to 86 s against the validation contract's "at most 30 s"; the latency item stays unticked and `64-VALIDATION.md` remains `draft`.

**Context:** the pre-checkpoint gate and the verification run.
**Source:** 64-06-SUMMARY.md, 64-VERIFICATION.md (Observation O-5)

---

## Patterns

### Sealed-input verification
Pin the handoff digest, re-check every citation, recompute the tier vector and the sweep outcome, then call the frozen rule and compare the whole returned dict.

**When to use:** confirming a verdict that an earlier phase sealed.
**Source:** 64-01-SUMMARY.md

### Frozen-tree verification
Diff the pinned pathspecs against the phase base and status them with `--untracked-files=all`, so committed, uncommitted and untracked changes all fail.

**When to use:** proving that nothing frozen moved during a phase.
**Source:** 64-01-SUMMARY.md

### Registry recount
Build exact-string ID sets from the definitions, the traceability table and the roadmap, parse every stated count as an integer, compare with `==`, and print a fixed-order, byte-identical report.

**When to use:** traceability checks such as VER-22.
**Source:** 64-01-SUMMARY.md

### Every quoted number is a labelled, sourced manifest entry
`numbers.json` holds every number the verdict and charter quote (365 entries), each labelled `official-mps-float32`, `committed-record`, `arithmetic`, `cited` or `rederived-cpu-float64` with its source, and CPU float64 re-derivations are kept as a separate fact from the official MPS result.

**When to use:** any owner-facing document whose numbers must be re-derivable.
**Source:** 64-02-SUMMARY.md

### Regenerate the figure and require byte equality
The `figure` check rebuilds the series from the committed weights and calls the producer's `render_svg`, requiring byte equality; inputs are checked by existence and SHA-256, and legibility (legend inside the canvas, non-zero predicted-track extent) is measured in code.

**When to use:** committed figures that support a decision.
**Source:** 64-03-SUMMARY.md

### Byte-equal owner quotes in opaque fences
Owner replies are stored verbatim in `owner-quote` fences that the `rules` scan strips, so the owner's own words are never policed.

**When to use:** recording any owner checkpoint.
**Source:** 64-05-SUMMARY.md

### One aggregate check with a single success token
`verify_phase64_verdict.py final` runs every mode in order and ends with `PHASE64-VERDICT-OK`, and its completeness step checks the if-direction the ruling mode leaves out.

**When to use:** phase close-out gates.
**Source:** 64-07-SUMMARY.md, 64-VERIFICATION.md (7.1)

---

## Surprises

### One short reply decided the milestone
The owner's whole checkpoint answer was "let's change course": V-1 change-course, all fourteen charter rows open, so v2.5 opens with the trainex-r5 research round and runs no new long training until it explains the time-constant output.

**Impact:** the charter rows (including C-12/C-13 on PROJECT.md and C-14 on the skipped requirements) carry forward undecided.
**Source:** 64-06-SUMMARY.md, STATE.md (Decisions from Phase 64)

### At full scale the prediction is a dot
The predicted tracks span 0.0022 to 0.0041 units against an orbit about 0.54 × 0.53 wide, so the figure needed three magnified insets to show the prediction at all.

**Impact:** the figure's design was driven by how little the network moves.
**Source:** 64-03-SUMMARY.md

### The two error curves are thinner than a stroke
The network's error curve and the constant predictor's differ by about 0.006, so a same-width dashed reference vanished beneath the solid curve; a wider dashed grey reference was needed.

**Impact:** a visual restatement of "learned only the average".
**Source:** 64-03-SUMMARY.md

### A for-scale full training takes weeks on this Mac
The labelled for-scale figure for a full single-orbit training is 28.5 to 42.8 days.

**Impact:** frames the cost of any next level that needs long training on the owner's Mac.
**Source:** 64-VERIFICATION.md (Observation O-1)

### The independent verifier caught what 287 tests did not
The aggregate check and the full unit suite passed while the verdict still carried the seven-arm wording error.

**Impact:** independent reading remains necessary on owner-facing prose even with exhaustive number checks.
**Source:** 64-VERIFICATION.md (G-1, section 10)

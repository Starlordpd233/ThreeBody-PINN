# Evidence Packet: B-11 - ID Resolution (ID ≠ array index)

## Header

| Field | Value |
|---|---|
| ID | `B-11` (v1.5 Issue-02; directory-qualified — distinct from any v1.4 issue-01 namesake) |
| Title | `Non-contiguous IDs (ID ≠ array index; id_to_path / TrajectoryIndex contract)` |
| Severity | `BLOCKING` (per `24-ISSUE-LEDGER.md:24`; dense indexing mis-addresses ~1 in 3 standard lookups) |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 26` (PIPE-02; Plan 26-01) |
| Acceptance Check ID | `AC-PIPE-02` |
| Spec Sections Touched | `ctl_instruction.md` Step 1, appended item 7 (`ID resolution (no dense-index assumption)`), cross-referenced from Step 5. `pinn_architecture.md`: None (D-04 — the contract is data-side; no architecture-side statement required). |
| Code Paths Touched | `Not code-applicable` (framework-spec contract only; TrajectoryIndex implementation is FUT-01) |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§3.2 Q-A2:178-217` (7-clause `id_to_path` scan contract; proposed spec text `:202-216`) | Trajectory identity is `(variant_folder, zero-padded 4-digit numeric ID)`; folder is the sole authority for variant + gold status. Build `id_to_path` by **scanning** the four Brutus output folders, accepting only `^brutus_(hierarchical|standard)_(\d{4})\.txt$`; IDs normalize to `int`, format `%04d` at path boundaries; duplicate `record_key` = hard init error; absent-key lookup raises an explicit miss with **no positional fallback, no `paths[id]` array indexing, no density/contiguity/zero-base assumption**; deterministic iteration over **sorted present keys**, never `range(n_files)`. Dual keys: `physical_key = (variant, id)` (blacklist/gold/IC-granularity) and `record_key = (variant, fidelity, id)` (file lookup). `Result:` footer paths never used for mapping. Per-folder init logging (files found, IDs parsed, duplicates=0, min/max span vs count). Issue-doc P1-2 accepted in substance; this verdict pins what P1-2 leaves open. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:58` (B-11 row), `:284` (P1-2), `:314-318`, `:356`, `:361` | Build an `id_to_path` / `TrajectoryIndex` mapping; the numeric ID is NOT an index and gaps exist; do not assume contiguity. P1-2 names the requirement but leaves the key structure, regex, collision/miss semantics, and iteration discipline open. |

BOTH citations are present (D-04 §2), even though this verdict is uncontested (ledger Sources Disagree? = NO).

## Spec Evidence

Current framework-spec evidence for the convention being added:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:340-378` — Step 1 ("Parse Raw Simulation Data") reads `ic_.txt`/`brutus_.txt` files (item 1, `:342`) and infers metadata from filenames (item 4, `:362-366`) but states **no** ID-resolution contract: nothing forbids dense/positional indexing, and the mapping from on-disk filenames to a trajectory key is undefined. The new item 7 lands at the end of the Step 1 item list.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1061-1068` — Step 5 ("Curriculum Stage Assignment") already describes the stage map as "a mapping from each simulation ID to its assigned stage index" — ID-keyed in principle, but with no statement that the key is `record_key` rather than a positional index. The B-11 item makes the key discipline explicit and cross-references it from Step 5.

### Dataset Evidence (§3b)

- `24-VERIFIED-FACTS.md CLM-01:15` — standard base: `n=2,749` files, `min_id=0`, `max_id=3,998`, **1,250 gaps** in `[0..max]`. The ID space is provably non-dense: a 2,749-element dense array cannot address IDs up to 3,998.
- `24-VERIFIED-FACTS.md CLM-04:18` — the CLM-04 evidence base (184 standard IDs without gold; the `standard_quasi_random_ids_not_in_gold.md` list) contains IDs (e.g. 3958) exceeding the standard-base file count 2,749, so positional/array indexing would mis-address them with certainty.
- `24-VERIFIED-FACTS.md CLM-02:16` — hierarchical: `n=4,857` files, `max_id=4,999`, **143 gaps**. Non-dense in the hierarchical folder too.
- `24-VERIFIED-FACTS.md CLM-12:27` — nominal counts confirmed via observed `max_id` (standard 3,998 → ~4,000; hierarchical 4,999 → ~5,000), pinning the gap magnitude: roughly one in three standard lookups would be wrong under dense indexing.
- `24-VERIFIED-FACTS.md CLM-05b:20` — standard base 2,749 vs gold 2,565 (base−gold=184); the base↔gold join is realized at `record_key` granularity, motivating the dual-key abstraction (`physical_key` for gold availability, `record_key` for file lookup).

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.5 evidence source (user directive 2026-05-19). Forward-pointing only:

- `pinn/data-processing-pipeline-full.py` — the v1.3-era pipeline must be rebuilt to implement the scan-built `id_to_path` with the dual `physical_key`/`record_key` abstraction, anchored-regex acceptance, collision/miss semantics, and sorted-key iteration; any existing positional or `range(n_files)` access path is a FUT-01 rewrite target. Indexed for the eventual `NN-CODE-DIVERGENCE.md` / `pinn/STATUS.md`. NOT v1.5 evidence.

## First-Principles Physics Check

Not an EVID-10 finding (ledger `Sources Disagree? = NO`); this section is optional. One short cardinality argument anchors the verdict:

```
Standard-base file count (CLM-05b):   2,749
Observed max standard ID (CLM-01):    3,998   (and CLM-04 list holds ID 3958)
A dense array of length 2,749 can address indices 0..2,748 only.
3,998 > 2,748  =>  positional/dense indexing cannot address the full ID set.
```

This is pure cardinality, not physics: an injective filename→key map keyed on the parsed 4-digit ID is the only addressing scheme that survives the verified gap structure (1,250 standard / 143 hierarchical gaps). Dense indexing mis-addresses any trajectory whose ID exceeds its sorted position.

## Verdict

`accept-resolution`

The resolution doc's 7-clause `id_to_path` scan contract (`02-resolution-doc.md §3.2 Q-A2:178-217`) is adopted after independent verification. The decisive independent check is the CLM-01/CLM-04 cardinality argument (`24-VERIFIED-FACTS.md:15,:18`): the standard ID space reaches 3,998 against 2,749 files with 1,250 verified gaps, so dense/positional indexing is provably incorrect — exactly the failure the contract's `ID ≠ array index` invariant prohibits. Every clause is grounded: the scan-built mapping and anchored regex match the verified File Naming Conventions; the dual `physical_key`/`record_key` abstraction is justified by the base↔gold realization-granularity split (CLM-05b); sorted-key iteration and collision/miss semantics are operational hardening with no source conflict. The issue doc's P1-2 is accepted in substance; the resolution doc pins what P1-2 left open. The verdict is `accept-resolution`, not `accept-third-position`, because the candidate text survives every check unchanged, and no candidate clause is source-silent. No new cross-source conflict surfaced (so no EVID-10 sections are required).

## Root-Cause Framework Ambiguity

Optional (not EVID-10). The current `ctl_instruction.md` Step 1 (`:340-378`) parses filenames but never states an addressing contract, and Step 5 (`:1061-1068`) names an "ID → stage index" mapping without pinning the key type. That silence is what allows a positional/dense implementation to creep in. Item 7 closes the gap by stating the `record_key`/`physical_key` discipline and the explicit prohibition on dense, contiguous, zero-based, or array-index addressing.

## Locked Convention

Optional (not EVID-10). The contract adopted is the candidate spec text at `02-resolution-doc.md:202-216` (scan-built `id_to_path`, anchored regex `^brutus_(hierarchical|standard)_(\d{4})\.txt$`, dual `physical_key`/`record_key`, hard duplicate-key error, explicit absent-key miss with no positional fallback, sorted-key iteration, `Result:`-footer paths never used for mapping, per-folder init logging), transcribed into `ctl_instruction.md` Step 1 item 7 with a Step-5 cross-reference.

## Which Source Was Correct / Wrong

- **Resolution doc:** correct and mechanism-complete. The scan contract, dual-key abstraction, and `ID ≠ index` invariant are all grounded in CLM-01/02/04/05b/12.
- **Issue doc:** correct in substance (P1-2: build `id_to_path`/`TrajectoryIndex`; the numeric ID is not an index; gaps exist) but under-specified — it leaves the key structure, regex, collision/miss semantics, and iteration discipline open, which the resolution doc supplies. No clause of the issue doc is wrong; it is incomplete, not incorrect.

## Before / After Spec Note

**Affected section:** `ctl_instruction.md` — Step 1 item list, appended item 7 (post-edit `:381-405`), cross-referenced from Step 5 (post-edit `:1138-1142`).

**Before:** `ctl_instruction.md` Step 1 (pre-edit `:340-378`) parses filenames and infers metadata but states **no** ID-resolution contract; nothing prohibits dense, positional, or array-index addressing, and Step 5's "ID → stage index" mapping (`:1061-1068`) does not pin the key type. A dense or positional implementation would mis-address trajectories given the verified gap structure.

**After:** Step 1 item 7 states the scan-built `id_to_path` contract — dual `physical_key`/`record_key`, anchored regex, `%04d` normalization, hard duplicate-key error, explicit absent-key miss with **no positional fallback**, sorted-key iteration, `Result:`-footer paths never used for mapping, per-folder init logging, and the explicit invariant that IDs are never contiguous/dense/zero-based/equal to an array index (grounded by the verified ID 3958 vs 2,749-file non-density). Step 5 is annotated to key the stage map by `record_key` and to include only Step-1A-admitted trajectories. The B-06↔B-11 coupling (B-06 admission clause 1 "the ID resolves per the Step-1 ID-resolution contract") is satisfied by this item; the two were reconciled in one before/after pass (mutually consistent).

## Named Acceptance Check

**AC-PIPE-02** (reserved in `24-ISSUE-LEDGER.md:24`; no new AC-ID minted — VER-07).

- **Pass criterion:** (a) `ctl_instruction.md` Step 1 states a scan-built `id_to_path` contract naming both `physical_key` and `record_key`, the anchored regex `^brutus_(hierarchical|standard)_(\d{4})\.txt$`, and the explicit invariant that an ID is never contiguous/dense/zero-based/equal to an array index, with no positional fallback; (b) the verified non-density (CLM-01: max_id 3,998 with 2,749 files, 1,250 gaps; CLM-04 list holds ID 3958) confirms dense indexing would mis-address trajectories — i.e. the prohibited addressing scheme is empirically incompatible with the data.
- **Data it runs on:** the edited `ctl_instruction.md` (spec-consistency probe) and the recorded CLM-01/CLM-04 facts in `24-VERIFIED-FACTS.md:15,:18` (dataset facts; re-derivable via the CLM-01 probe `data01_id_gaps.py` and CLM-04 probe `data03_gold_gap.py`, not re-run here per the Phase-24 probe-capture convention `24-VERIFIED-FACTS.md:100-104`).
- **Exact command + captured output (re-derivable, D-15):**

```
$ grep -nE 'id_to_path|record_key|physical_key|array index|brutus_\(hierarchical' \
    pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
381:    `record_key = (variant, fidelity, id)`; the physical IC is
382:    `physical_key = (variant, id)`; `id` is the 4-digit zero-padded
383:    integer in the filename. At DataLoader init, build `id_to_path` by
385:    filenames matching `^brutus_(hierarchical|standard)_(\d{4})\.txt$`
388:    to the same `record_key` is a hard init error. Lookup of an absent
391:    zero-based, or equal to an array index. All deterministic iteration
392:    is over sorted `record_key`s, never `range(n_files)`. Stage labels
393:    (Step 5) are keyed by `record_key`, never by positional index.
394:    Blacklist and gold-availability semantics attach to `physical_key`
395:    and apply to every `record_key` beneath it. `Result:` footer paths
1140:mapping is keyed by `record_key`, never by positional index, per the
```

Interpretation: the scan-built `id_to_path` contract is present with both key levels, the anchored regex, the explicit `array index` prohibition (line 391), the `range(n_files)` prohibition (line 392), and the Step-5 cross-reference (line 1140). PASS. The CLM-01/CLM-04 non-density facts (max_id 3,998 / ID 3958 vs 2,749 files, recorded `24-VERIFIED-FACTS.md:15,:18`) confirm dense indexing is empirically impossible. PASS.

AC-PIPE-02 is a spec-consistency + dataset-fact probe; it touches no `pinn/` path. Phase 29 (VER-09) builds and re-executes the full runnable acceptance suite from this AC-ID (the resolution-doc part-5 property test `max(parsed IDs) >= file_count` and the CLM-04 explicit-miss unit tests).

## Status Transition Log

```text
2026-06-13 b1852b0f PENDING -> IN_PROGRESS (Phase 26 P01 by gsd-executor; B-11 packet authored, accept-resolution verdict, AC-PIPE-02 defined)
2026-06-13 b1852b0f IN_PROGRESS -> FIX_APPLIED (Phase 26 P01; Step 1 item-7 ID-resolution contract transcribed into ctl_instruction.md from 02-resolution-doc.md:202-216)
2026-06-13 b1852b0f FIX_APPLIED -> VERIFIED (Phase 26 P01; AC-PIPE-02 spec-consistency + CLM-01/04 dataset probe PASS; G2 closes with B-11)
```

The Plan 26-01 commit SHA is `b1852b0f` — all three transitions, the spec edit, and the ledger edits travelled in that one commit (D-08); this SHA was backfilled into the packets and the ledger per-finding subsections in the immediately following provenance commit (a commit cannot reference its own hash inline).

**Carried caveats (D-13):** none specific to B-11. The resolution doc records this verdict as "High; unconditional" (`02-resolution-doc.md:196`); the only modifying (not overturning) factor is IDs violating the 4-digit pattern in a future extension, which widens the regex and nothing else.

**Dependents / regression (D-08):** B-11 shares the Step-1 region with B-06 (this plan's other finding); B-06's admission clause 1 depends on B-11's item 7. The two were reconciled in one before/after pass (mutually consistent). No previously-VERIFIED Phase 26 row exists yet, so the regression surface is internal to this plan.

**G2 close-with-parent (D-07):** G2 (synthesis view over B-11) closes with B-11 — no separate evidence packet; annotated in the ledger's G2 per-finding note.

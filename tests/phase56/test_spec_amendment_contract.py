"""Content-match guard for the plan 56-05 SCOPE-38 amendment completion.

Plan 56-04 landed the AMENDED §3.2 blocks (Block 1 causal-exponent argument,
the frozen R_ref procedure, Block 4 collocation allocation/time-draw); plan
56-05 completes the amendment by recording the two NOT-AMENDED contracts
(§2.2 first_omega_0, §4.1 clip underflow-only purpose) separately and by
name, landing three secondary reconciliation wordings, and re-adjudicating
the render oracle over the new prose.

This file exists alongside the plan's plan-time shell `<verify>` gates for
one reason: the shell gates (the removed-line negative-diff check, the
section-2.4-table-untouched check, the render-oracle re-run) run once at
commit time and then disappear with the plan -- they prove the edit was
correct *when it was made*, but nothing re-checks it afterward. A committed
pytest module runs with the ordinary suite on every future change to this
repository, so a later edit that accidentally rewords a NOT-AMENDED
contract, drops a re-issued acceptance criterion, or lets a render-oracle
adjudication entry rot out of sync with the file it describes is caught
the next time `pytest` runs -- not only during this one plan's execution.

The long verbatim strings below are stored as module-level constants (not
inlined into each assertion) so a future reader can see exactly what text
this file is protecting without re-deriving it from `54-RULING.md`.
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC_PATH = (
    ROOT
    / "pinn_instruction"
    / "markdown_conversion"
    / "framework-specs"
    / "pinn_architecture.md"
)
ADJUDICATIONS_PATH = (
    ROOT / "tools" / "spec-render-check" / "adjudications" / "22-02-pinn-architecture.json"
)

# Read once; every test below asserts against this single in-memory copy.
SPEC_TEXT = SPEC_PATH.read_text(encoding="utf-8")

# --- Block 1 (§3.2, landed by plan 56-04): AC-LOSS-04 re-issued verbatim ---
AC_LOSS_04_REISSUED = (
    "AC-LOSS-04 is re-issued without a new identifier: the default Stage-0 "
    "causal loss uses exactly `η_c = 1`, `n_col = 4096` total per training "
    "batch, `M = 16` fixed equal-`u` bins with exactly 256 rows per bin, "
    "`R̃_b = R̄_b/R_ref`, one batch-global exclusive 16-bin prefix, and "
    "residual-wide normalization. Each of the fixed six initialization-probe "
    "cases uses exactly 4096 recorded-seed stratified times (256 per bin); "
    "`R_ref` is the finite positive median of the resulting 96 raw bin means, "
    "is detached and frozen, all 96 constituents and provenance are retained, "
    "and every trigger named in the checkpoint-② discharge section "
    "invalidates it. Raw and normalized diagnostics are both recorded; "
    "raw-unit thresholds are never silently applied to normalized values. "
    "GATE-04 must evaluate the actual full vectors and fail closed on any "
    "non-finite input, any floor-bound initialization weight, a degenerate "
    "weight vector, or a front that cannot respond to controlled residual "
    "reduction. A resampled training-batch front is diagnostic only; "
    "invariant-B evidence follows the fixed-monitor boundary above. "
    "GAP-54-06's L-BFGS question is not part of this criterion and must be "
    "settled at checkpoint ③ before RUN-04. This amendment does not decide "
    "the second-optimizer-phase and L-BFGS causal-weight recomputation "
    "semantics, which remain deferred to the Phase 57 owner checkpoint "
    "③ (GAP-54-06), and it does not decide the train-free gate's "
    "condition-(ii) pass criterion, which is unratified and tracked as "
    "GAP-56-01."
)

# --- Block 4 (§3.2, landed by plan 56-04): re-issued acceptance criterion ---
BLOCK4_AC_REISSUED = (
    "A full 256-slot batch emits exactly 4096 physics rows as one "
    "independently sampled time in each of 16 fixed bins for every selected "
    "slot. A 240-slot replay-only batch uses the seeded 3840-plus-256 "
    "remainder construction stated above, yielding exactly 256 rows per bin "
    "and per-slot totals 17 or 18. Replacement multiplicity is preserved; "
    "every bin is non-empty by construction; each bin residual is the mean "
    "of exactly 256 rows; one batch-global exclusive prefix is formed over "
    "the 16 bin means; energy reuses the same set; and microbatching "
    "preserves complete bin aggregates and never resets the prefix."
)

# --- Batch-allocation bin-policy sentence (§3.2, landed by plan 56-04) ---
BIN_POLICY_EMPTY_BINS_IMPOSSIBLE = (
    "Empty bins are impossible, and the causal prefix is one batch-global "
    "16-bin prefix."
)

# --- Reference-invalidation opening clause (§3.2, landed by plan 56-04) ---
REFERENCE_INVALIDATION_OPENING = (
    "Reference invalidation (transcribed verbatim from `54-RULING.md`): "
    "Re-measure `R_ref` and re-run GATE-04 after any change to "
    "`first_omega_0`, depth, width, power-skip exponent, LayerNorm "
    "placement or stabilizer, initialization bounds, `D`, `T`, "
    "`epsilon_soft`, IC13 normalization, `n_col`, `M`, count unit, "
    "selected-slot semantics, or bin/allocation semantics."
)

# --- Original, pre-Phase-56 contract sentences: must survive byte-identical ---
SIREN_FIXED_FREQUENCY_SENTENCE = (
    "`first_omega_0` is fixed at `30` and is not scheduled during training."
)
CLIP_UNDERFLOW_ONLY_SENTENCE = (
    "The causal exponent clip is required only to avoid underflow."
)

# --- The illustrative session-computed R_ref figure (56-RESEARCH.md b.2): ---
# ratified is the *procedure* (median of 96 raw bin means), never a number.
ILLUSTRATIVE_REFERENCE_FIGURE_RE = re.compile(r"1\.97[0-9]*e\+?10|19749775821|1974977582")

REQUIRED_ADJUDICATION_KEYS = {"file", "line", "token", "verdict", "rationale"}


def test_block1_reissued_acceptance_criterion_present_verbatim():
    assert AC_LOSS_04_REISSUED in SPEC_TEXT


def test_block4_reissued_acceptance_criterion_present_verbatim():
    assert BLOCK4_AC_REISSUED in SPEC_TEXT


def test_batch_allocation_bin_policy_empty_bins_impossible_present():
    assert BIN_POLICY_EMPTY_BINS_IMPOSSIBLE in SPEC_TEXT


def test_reference_invalidation_opening_clause_present():
    assert REFERENCE_INVALIDATION_OPENING in SPEC_TEXT


def test_not_amended_marker_appears_at_least_twice():
    # Two contracts (§2.2 first_omega_0, §4.1 clip purpose) are each
    # dispositioned "NOT AMENDED" by name and separately (ROADMAP Phase 56
    # success criterion 2) -- silence would not satisfy that criterion.
    assert SPEC_TEXT.count("NOT AMENDED") >= 2


def test_siren_fixed_frequency_sentence_byte_identical():
    assert SIREN_FIXED_FREQUENCY_SENTENCE in SPEC_TEXT


def test_clip_underflow_only_sentence_byte_identical():
    assert CLIP_UNDERFLOW_ONLY_SENTENCE in SPEC_TEXT


def test_no_illustrative_reference_figure_literal_present():
    # 54-RULING.md ratifies the R_ref *procedure*, not a number; the spec
    # must never hard-code the one session's illustrative computed value.
    match = ILLUSTRATIVE_REFERENCE_FIGURE_RE.search(SPEC_TEXT)
    assert match is None, f"illustrative R_ref figure leaked into spec: {match.group(0)!r}"


def test_run_driver_and_ratified_total_named_together():
    # SC3 / D-03: the spec must name both the run driver's current
    # hard-coded count and the ratified per-batch total it diverges from.
    assert "collocation_count = 16" in SPEC_TEXT
    assert "4096-row total per training batch" in SPEC_TEXT


def test_recommended_range_wording_reconciled_as_historical():
    # D-11 / 53-UNSWEPT-INVENTORY item 5: the listing's docstring range
    # wording is reconciled as historical; the ratified total is fixed.
    assert "recommended: 2048-4096" in SPEC_TEXT
    assert "n_col = 4096` rows total per training batch, fixed and exact" in SPEC_TEXT


def test_causal_coefficient_bullet_cross_references_section_3_2():
    # D-10: the §4.1 eta_c default bullet points at the re-issued AC rather
    # than restating the exponent formula a second time.
    assert "AC-LOSS-04), not restated here" in SPEC_TEXT


def test_adjudication_file_entries_have_required_keys_and_rationale():
    rows = json.loads(ADJUDICATIONS_PATH.read_text(encoding="utf-8"))
    assert rows, "adjudication file must not be empty"
    for row in rows:
        missing = REQUIRED_ADJUDICATION_KEYS - set(row)
        assert not missing, f"row {row!r} missing keys: {missing}"
        assert str(row["rationale"]).strip(), f"row {row!r} has an empty rationale"


def test_adjudication_entries_point_at_lines_containing_their_token():
    # Task 1's insertion shifted every pre-existing entry below its anchor
    # by +2 lines; this proves each entry was re-derived by content match
    # (54-RULING.md's anchor-drift warning) rather than left stale.
    spec_lines = SPEC_TEXT.splitlines()
    rows = json.loads(ADJUDICATIONS_PATH.read_text(encoding="utf-8"))
    for row in rows:
        line_no = row["line"]
        assert 1 <= line_no <= len(spec_lines), (
            f"adjudication entry {row!r} line {line_no} is out of range "
            f"(file has {len(spec_lines)} lines)"
        )
        actual_line = spec_lines[line_no - 1]
        assert row["token"] in actual_line, (
            f"adjudication entry {row!r} does not match live line "
            f"{line_no}: {actual_line!r}"
        )

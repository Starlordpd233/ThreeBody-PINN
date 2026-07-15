---
status: diagnosed
trigger: "Diagnose root cause only for Phase 39 UAT gap: Replacement-padded lookahead retains its locked collocation weight."
created: 2026-07-15T13:50:38Z
updated: 2026-07-15T13:58:58Z
---

## Current Focus

hypothesis: CONFIRMED — `sample_collocation_points` violates GAP-39-12 because `sorted(set(record_keys))` converts the 256 selected replay/lookahead slots into unique RecordKeys before computing `M`; replacement-padded lookahead slots therefore lose multiplicity and collocation weight.
test: Exact singleton Stage-1 reproduction plus a slot-preserving quota counterfactual and data-versus-collocation multiplicity contrast.
expecting: Confirmed result: selection and data sampling preserve 16 lookahead slot occurrences, while collocation alone collapses them and allocates by 241 unique keys.
next_action: Return the diagnose-only root-cause report; do not modify production or tests.

## Symptoms

expected: When a Stage-1 pool is padded with replacement to 16 slots, GAP-39-12 allocates 4096 collocation points over all 256 selected replay/lookahead slots, preserving 16 points per slot.
actual: With one Stage-1 identity padded to 16, `selected_slots=256`, `selected_unique=241`, and lookahead receives 17 collocation points instead of 256.
errors: No exception; allocation weight is reduced from the slot-multiplicity contract to near-unique-identity weight.
reproduction: Construct the Phase 39 reproduction with one Stage-1 identity padded with replacement to 16 lookahead slots, then observe selected slot/unique counts and the lookahead collocation allocation.
started: Discovered during Phase 39 UAT at commit `e9e2996acf5ffe4c82dbbbefbc8672538833515c`; earlier status not supplied.

## Eliminated

- hypothesis: `allocate_collocation_quota` has an off-by-one or quotient/remainder bug.
  evidence: Direct 256-slot allocation returns exactly 256 quotas of 16 summing to 4096; 241-key allocation returns the exact observed 16/17 distribution implied by `divmod(4096, 241)`.
  timestamp: 2026-07-15T13:56:48Z

- hypothesis: `select_stage_records` fails to pad singleton Stage-1 lookahead to 16 entries.
  evidence: The production reproduction returns 16 lookahead slots and 256 total selected slots before collocation construction.
  timestamp: 2026-07-15T13:56:48Z

- hypothesis: GAP-39-12 intends allocation over unique RecordKeys, so deduplication is correct.
  evidence: The UAT oracle and `39-05-PLAN.md` explicitly require the populated 240+16 selected case to use `M=256` with 16 points per selected slot; the 1..15 pool is explicitly padded with replacement to 16.
  timestamp: 2026-07-15T13:56:48Z

- hypothesis: Selection or shared batch assembly loses the replacement occurrences before both point samplers.
  evidence: The singleton production batch retains 16 lookahead occurrences and emits 512 data-fidelity rows for that key (`16 * 32`), while collocation emits only 17 rows.
  timestamp: 2026-07-15T13:58:58Z

## Evidence

- timestamp: 2026-07-15T13:51:12Z
  checked: `.planning/debug/knowledge-base.md`
  found: No debug knowledge base exists in this worktree.
  implication: There is no known-pattern candidate to privilege; investigate from the supplied contract and reproduction evidence.

- timestamp: 2026-07-15T13:53:06Z
  checked: GAP-39-12 and `39-05-PLAN.md` task 39-05-02
  found: The resolved contract allocates `C=4096` across the `M` selected replay/lookahead slots; the populated 240+16 case must give exactly 16 points to every one of 256 slots, including replacement-padded slots.
  implication: Replacement occurrences are weighting slots even when several slots share one RecordKey; unique-key cardinality is not the contract's `M`.

- timestamp: 2026-07-15T13:53:06Z
  checked: `pinn/data/batches.py` selection and collocation implementations
  found: `select_stage_records` returns 240 unique replay keys plus 16 lookahead entries sampled with replacement when the next-stage pool is undersized, but `sample_collocation_points` immediately builds `identities = tuple(sorted(set(record_keys)))` before calling the quota allocator.
  implication: The producer preserves replacement multiplicity and the consumer destroys it at the representation boundary; for a singleton Stage-1 pool, `M` changes from 256 slots to 241 unique keys.

- timestamp: 2026-07-15T13:53:06Z
  checked: `tests/phase39/test_batches.py`
  found: Tests prove padded selection and abstract 256-way quota allocation separately. Integrated collocation tests cover replay-only or a default Stage-1 pool with at least 16 unique keys, so no test carries an undersized replacement-padded selection through `sample_collocation_points`.
  implication: Existing green tests can miss the interaction because deduplication is behaviorally inert for the integrated fixtures they exercise.

- timestamp: 2026-07-15T13:54:01Z
  checked: `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v`
  found: All 27 existing batch tests pass unchanged.
  implication: The regression is not covered by the current suite; a green targeted suite does not refute the supplied integrated UAT failure.

- timestamp: 2026-07-15T13:55:15Z
  checked: Exact singleton Stage-1 reproduction through unmodified `build_stage_batch`
  found: The run produced `selected_slots=256`, `selected_unique=241`, `lookahead_slots=16`, `lookahead_unique=1`, and `lookahead_collocation_points=17`; unique-key quota counts were one key at 16 and 240 keys at 17.
  implication: The reported failure is repeatable and numerically matches `4096 divmod 241 = (16, 240)`, directly tying the output to the deduplicated denominator.

- timestamp: 2026-07-15T13:56:48Z
  checked: Pure slot-preserving quota counterfactual over the same selected multiset
  found: With all 256 selected slots retained, `allocate_collocation_quota(256, 4096, ...)` returns 256 quotas of 16 and the 16 singleton-lookahead occurrences aggregate to 256 points.
  implication: The quota allocator is correct; changing only the denominator input from 241 unique keys back to 256 selected slots makes the original symptom disappear.

- timestamp: 2026-07-15T13:56:48Z
  checked: `git blame`/`git log -S` for `tuple(sorted(set(record_keys)))`
  found: The set conversion was introduced with the initial collocation implementation in commit `56c223c955c02e6301bca4b40383c8c6a7886915`, not by a later compatibility change.
  implication: This is an implementation-time contract miss at the slot-to-collocation seam, not a subsequent regression in selection or quota arithmetic.

- timestamp: 2026-07-15T13:58:58Z
  checked: Singleton data-versus-collocation multiplicity contrast through unmodified `build_stage_batch`
  found: The sole lookahead key occurs in 16 selected slots and receives 512 data-fidelity points, but receives only 17 collocation points.
  implication: Multiplicity survives selection and adjacent data sampling; the first and only observed divergence is the `set(record_keys)` conversion inside `sample_collocation_points`.

## Resolution

root_cause: `pinn/data/batches.py:302` deduplicates the selected RecordKey multiset with `tuple(sorted(set(record_keys)))` before `allocate_collocation_quota` computes `M`. A singleton Stage-1 identity padded into 16 lookahead slots therefore contributes once to a 241-unique-key denominator instead of 16 times to the locked 256-slot denominator; `4096 divmod 241 = (16, 240)` yields the observed 17 points for that key.
fix: Not applied (diagnose-only). Minimal direction is to preserve the sorted selected-slot multiset in `sample_collocation_points` (remove unique-key deduplication while retaining deterministic sorting), allocate quotas across all slots, and add integrated `build_stage_batch` regression coverage for Stage-1 pools of size 1 and 15 so replacement padding and collocation allocation are tested together. `allocate_collocation_quota` itself needs no algorithm change.
verification: All 27 existing batch tests pass, confirming the coverage gap. The exact singleton reproduction returned 256 selected slots, 241 unique keys, and 17 lookahead collocation points. A pure 256-slot counterfactual returned 16 points per slot and 256 aggregate lookahead points; the same production batch retained 512 lookahead data-fidelity rows, localizing the fault to collocation deduplication.
files_changed:
  - `.planning/debug/phase39-collocation-slot-multiplicity.md` (diagnosis record only)

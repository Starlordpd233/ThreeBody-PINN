# FO-1 Gold-Rerun Manifest Record — standard quasi-random missing-gold 184

Durable, re-derivable **record** of the FO-1 rerun of the 184 standard quasi-random IDs that had
no gold counterpart. This directory holds the manifest and validation metadata only; the bulky
raw outputs are kept out of git by policy (see "Raw outputs" below).

- **Produced by:** `simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py`
  (committed in `1b1c939e`) reading `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`.
- **Outcome:** 184 attempted = **117 validated** (full `Result:` footer) + **67 failed**
  (missing footer — irreducible Stage-5 holes). Matches the locked v1.5 gold framing
  (117 validatable + 67 permanent-absent; GAP-29-01 Option A).
- **Recorded:** 2026-06-17.

## Files (committed here)

| File | Bytes | SHA-256 | Contents |
|---|---|---|---|
| `run_manifest.json` | 313109 | `a419597e4109bb6c6071eb7bbacf3c5fccb60a06b2f2f8e98427e36bb2684080` | Per-ID: `status`, `ic_path`/`ic_sha256`, `output_path`/`output_sha256`, `brutus_bin_sha256`, `params`, `command`, `start`/`end`/`duration`, `validation`. |
| `validation_summary.json` | 73849 | `9afc37aee3d95346485bf54276304ee3d2dcc669badcb5c826805df869554de5` | `total` (184) + per-ID `ok`/`errors`/`footer`/`final_time`. |

Both were copied byte-for-byte from the gitignored staging dir
`simulation_data/Data/rerun_staging/standard_gold_missing_184/`; the SHA-256s above are the
copy hashes, verified equal to source at commit time.

## Raw outputs (NOT in git — by design)

The 184 raw Brutus output `.txt` files (~64M) are a **bulky simulation payload**. Per
`.gitignore:316` (`simulation_data/Data/rerun_staging/`) and the migration runbook
(`docs/runbooks/migration/exact-state-mac-migration.md`), bulky simulation payloads are excluded
from git and preserved in the **out-of-git simulation-payload backup set** (copied separately),
not committed. Each raw output's SHA-256 is recorded in `run_manifest.json` (`output_sha256`), so
the backed-up payload can be integrity-verified against this manifest later.

## Scope guard

This is a record only. It does **not** promote the 117 validated reruns and does **not** apply the
`184 → 67` cascade — those remain **FO-1 deferred to FUT-01** (see
`.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-CODE-DIVERGENCE.md`,
GAP-29-01 Option A). No canonical dataset file, framework spec, or `pinn/` code is touched.

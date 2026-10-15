## In plain language

This check asks whether the allowlisted reader sees the same numbers the trainer stored in its Stage-0 monitor batch.
The reader matched the trainer's own resident numbers: 8192 rows, 256 identities, and no mismatch in targets, times, or masses. The largest IC13 difference is 1.1920928955078125e-07.
Owner-accepted deviation (GAP-59-10). That IC13 difference is above the frozen tolerance of 1e-07, so the frozen check is not met as measured, and the frozen value was not changed. On 2026-10-14 the owner accepted this result as a recorded deviation, with a ceiling of exactly 1.1920928955078125e-07 (2**-23). A larger IC13 difference, any mismatch in targets, times, or masses, or a normalizer residual over 1e-06 would still have stopped the run.
The normalizer residual is 1.1920928955078125e-07 against tolerance 1e-06. The normalizer fallback deviation is false.
No held-out file was opened. The test split was not read.

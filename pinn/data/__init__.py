"""Phase 39 data-ingestion package (v2.0 BUILD milestone, FUT-01).

This package owns the production Stage-0 data substrate: frozen shared types,
the sole format-aware corpus parser/adapter, CTL preprocessing/invariants, the
record-level Stage-0/1 classifier, and the seven-clause Step-1A admission gate.

Intentionally a minimal package marker: it does NOT import ``adapter`` (or any
module that scans the corpus) at package-import time. All loading/scanning is an
explicit call so ``import pinn.data.types`` never triggers disk I/O. See
``39-PATTERNS.md`` (``pinn/data/__init__.py`` assignment).
"""

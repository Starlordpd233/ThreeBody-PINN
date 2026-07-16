"""Phase 39 data-ingestion package (v2.0 BUILD milestone, FUT-01).

This package owns the production Stage-0 data substrate: frozen shared types,
the sole format-aware corpus parser/adapter, CTL preprocessing/invariants, the
record-level Stage-0/1 classifier, and the seven-clause Step-1A admission gate.

Public surface (39-PATTERNS.md ``pinn/data/__init__.py`` assignment, mirroring
the minimal ``pinn/verification/__init__.py`` analog): the Plan-02 frozen shared
contracts plus the production ``AdmittedSetAdapter``. Parser helpers
(``parse_brutus_text``/``parse_footer``/...) are intentionally NOT re-exported —
they belong to the adapter's internal ingestion surface.

Importing this package (or any submodule) binds these names but performs NO
corpus discovery and NO adapter initialization: scanning happens only when an
``AdmittedSetAdapter`` instance is explicitly constructed, so
``import pinn.data`` never touches the on-disk corpus.
"""

from pinn.data.adapter import (
    AdmittedSetAdapter,
    EvidenceRedactionError,
)
from pinn.data.types import (
    AdmittedRecord,
    DataFidelityPoints,
    DataVersionHashDeferred,
    DataVersionHashMismatch,
    DataVersionHashVerified,
    Fidelity,
    FixedBatch,
    MISSING_BASE,
    MISSING_GOLD,
    NormalizationStats,
    ParsedTrajectory,
    PhysicalKey,
    PhysicsCollocationPoints,
    RecordKey,
    StageLabel,
    StageQuery,
    StageZeroUnderpopulated,
    Variant,
)

__all__ = [
    "AdmittedSetAdapter",
    "AdmittedRecord",
    "DataFidelityPoints",
    "DataVersionHashDeferred",
    "DataVersionHashMismatch",
    "DataVersionHashVerified",
    "EvidenceRedactionError",
    "Fidelity",
    "FixedBatch",
    "MISSING_BASE",
    "MISSING_GOLD",
    "NormalizationStats",
    "ParsedTrajectory",
    "PhysicalKey",
    "PhysicsCollocationPoints",
    "RecordKey",
    "StageLabel",
    "StageQuery",
    "StageZeroUnderpopulated",
    "Variant",
]

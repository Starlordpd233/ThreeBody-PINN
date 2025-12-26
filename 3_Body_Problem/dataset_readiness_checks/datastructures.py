#!/usr/bin/env python3
"""
Core data structures for the Three-Body Problem database validation system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from pathlib import Path


class ValidationStatus(Enum):
    """Severity levels for validation issues."""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class ValidationIssue:
    """Individual validation issue/finding."""
    issue_id: str                    # Unique identifier
    severity: ValidationStatus       # PASS/FAIL/WARNING/ERROR
    module: str                     # Which validation module
    message: str                    # Human-readable description
    file_path: Optional[str] = None # Associated file
    line_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional context


@dataclass
class FileValidationResult:
    """Validation results for a single file."""
    file_path: str
    file_type: str                  # 'ic' or 'brutus'
    dataset_variant: str            # e.g., 'hierarchical_gold'
    file_number: int                # Extracted numeric ID
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)  # File statistics

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)

    def overall_status(self) -> ValidationStatus:
        if any(i.severity == ValidationStatus.ERROR for i in self.issues):
            return ValidationStatus.ERROR
        elif any(i.severity == ValidationStatus.FAIL for i in self.issues):
            return ValidationStatus.FAIL
        elif any(i.severity == ValidationStatus.WARNING for i in self.issues):
            return ValidationStatus.WARNING
        return ValidationStatus.PASS


@dataclass
class DatasetValidationResult:
    """Validation results for an entire dataset variant."""
    variant_name: str
    ic_results: Dict[int, FileValidationResult] = field(default_factory=dict)
    brutus_results: Dict[int, FileValidationResult] = field(default_factory=dict)
    correspondence_issues: List[ValidationIssue] = field(default_factory=list)
    summary_stats: Dict[str, Any] = field(default_factory=dict)

    def get_missing_brutus(self) -> List[int]:
        """Return IC file numbers without corresponding Brutus output."""
        return [num for num in self.ic_results.keys()
                if num not in self.brutus_results.keys()]

    def get_missing_ic(self) -> List[int]:
        """Return Brutus file numbers without corresponding IC."""
        return [num for num in self.brutus_results.keys()
                if num not in self.ic_results.keys()]


@dataclass
class ValidationReport:
    """Complete validation report for all datasets."""
    timestamp: str
    config: Dict[str, Any]
    datasets: Dict[str, DatasetValidationResult] = field(default_factory=dict)
    global_issues: List[ValidationIssue] = field(default_factory=list)

    def get_summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        total_files = 0
        total_issues = 0
        status_counts = {status.value: 0 for status in ValidationStatus}

        for dataset in self.datasets.values():
            # Count across all files in dataset
            for file_result in list(dataset.ic_results.values()) + list(dataset.brutus_results.values()):
                total_files += 1
                total_issues += len(file_result.issues)
                status = file_result.overall_status()
                status_counts[status.value] += 1

        return {
            "total_files": total_files,
            "total_issues": total_issues,
            "status_counts": status_counts,
            "dataset_count": len(self.datasets)
        }


@dataclass
class Snapshot:
    """Represents a single snapshot in a Brutus output file."""
    time: float
    n_bodies: int
    t_cpu: float
    particles: List[Tuple[float, ...]]  # List of (m, x, y, z, vx, vy, vz) tuples


@dataclass
class ResultFooter:
    """Represents a Result: footer line from Brutus output."""
    filename: Optional[str] = None
    n: Optional[int] = None
    t_begin: Optional[float] = None
    t_end: Optional[float] = None
    dt: Optional[float] = None
    eta: Optional[float] = None
    tol: Optional[str] = None
    lw: Optional[int] = None
    t_cpu: Optional[float] = None
    e_initial: Optional[float] = None
    e_final: Optional[float] = None
    de_e: Optional[float] = None
    line_number: Optional[int] = None

    def is_complete(self) -> bool:
        """Check if footer has all expected fields."""
        return all([
            self.filename is not None,
            self.n is not None,
            self.t_begin is not None,
            self.t_end is not None,
            self.dt is not None,
            self.e_initial is not None,
            self.e_final is not None,
            self.de_e is not None
        ])

    def missing_fields(self) -> List[str]:
        """Return list of missing field names."""
        missing = []
        if self.filename is None: missing.append('filename')
        if self.n is None: missing.append('N')
        if self.t_begin is None: missing.append('t_begin')
        if self.t_end is None: missing.append('t_end')
        if self.dt is None: missing.append('dt')
        if self.e_initial is None: missing.append('E_initial')
        if self.e_final is None: missing.append('E_final')
        if self.de_e is None: missing.append('dE/E')
        return missing


# Utility function to create issue objects
def create_issue(issue_id: str, severity: ValidationStatus, module: str,
                message: str, file_path: Optional[str] = None,
                line_number: Optional[int] = None,
                metadata: Optional[Dict[str, Any]] = None) -> ValidationIssue:
    """Helper function to create ValidationIssue objects."""
    if metadata is None:
        metadata = {}
    return ValidationIssue(
        issue_id=issue_id,
        severity=severity,
        module=module,
        message=message,
        file_path=file_path,
        line_number=line_number,
        metadata=metadata
    )
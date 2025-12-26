#!/usr/bin/env python3
"""
File format validation module for the Three-Body Problem database.

Validates:
1. IC files: 3 lines, each with 7 values (m, x, y, z, vx, vy, vz)
2. Brutus output files: Correct header format, 3 body lines per snapshot
"""

import logging
from pathlib import Path
from typing import List, Tuple, Optional

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_ic_file, parse_brutus_file


def validate_ic_format(ic_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate the format of an IC file.

    Args:
        ic_path: Path to the IC file
        variant: Dataset variant name (for context)

    Returns:
        List of validation issues
    """
    issues = []

    try:
        # Check file exists and is readable
        if not ic_path.exists():
            issues.append(create_issue(
                issue_id="ic_file_missing",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"IC file does not exist: {ic_path}",
                file_path=str(ic_path)
            ))
            return issues

        if ic_path.stat().st_size == 0:
            issues.append(create_issue(
                issue_id="ic_file_empty",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"IC file is empty: {ic_path.name}",
                file_path=str(ic_path)
            ))
            return issues

        # Parse the file (which validates the format)
        try:
            particles = parse_ic_file(ic_path)

            # Additional format checks
            if len(particles) != 3:
                issues.append(create_issue(
                    issue_id="wrong_particle_count",
                    severity=ValidationStatus.ERROR,
                    module="file_format",
                    message=f"Expected 3 particles, found {len(particles)}",
                    file_path=str(ic_path)
                ))

            # Check each particle has exactly 7 values
            for i, particle in enumerate(particles):
                if len(particle) != 7:
                    issues.append(create_issue(
                        issue_id=f"particle_{i}_wrong_value_count",
                        severity=ValidationStatus.ERROR,
                        module="file_format",
                        message=f"Particle {i}: Expected 7 values, found {len(particle)}",
                        file_path=str(ic_path),
                        metadata={"particle_index": i, "value_count": len(particle)}
                    ))

                # Check for NaN or infinite values
                for j, value in enumerate(particle):
                    if not isinstance(value, (int, float)):
                        issues.append(create_issue(
                            issue_id=f"particle_{i}_value_{j}_non_numeric",
                            severity=ValidationStatus.ERROR,
                            module="file_format",
                            message=f"Particle {i}, value {j}: Non-numeric value {value}",
                            file_path=str(ic_path),
                            metadata={"particle_index": i, "value_index": j, "value": value}
                        ))

                    import math
                    if math.isnan(value) or math.isinf(value):
                        issues.append(create_issue(
                            issue_id=f"particle_{i}_value_{j}_nan_inf",
                            severity=ValidationStatus.ERROR,
                            module="file_format",
                            message=f"Particle {i}, value {j}: NaN or infinite value",
                            file_path=str(ic_path),
                            metadata={"particle_index": i, "value_index": j, "value": value}
                        ))

            # If no issues, add a success marker
            if not issues:
                issues.append(create_issue(
                    issue_id="ic_format_valid",
                    severity=ValidationStatus.PASS,
                    module="file_format",
                    message=f"IC file format is valid",
                    file_path=str(ic_path)
                ))

        except ValueError as e:
            issues.append(create_issue(
                issue_id="ic_format_error",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"IC file format error: {str(e)}",
                file_path=str(ic_path)
            ))

    except Exception as e:
        issues.append(create_issue(
            issue_id="ic_validation_error",
            severity=ValidationStatus.ERROR,
            module="file_format",
            message=f"Unexpected error validating IC file: {str(e)}",
            file_path=str(ic_path)
        ))
        logging.error(f"Error validating IC file {ic_path}: {e}", exc_info=True)

    return issues


def validate_brutus_format(brutus_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate the format of a Brutus output file.

    Args:
        brutus_path: Path to the Brutus output file
        variant: Dataset variant name (for context)

    Returns:
        List of validation issues
    """
    issues = []

    try:
        # Check file exists and is readable
        if not brutus_path.exists():
            issues.append(create_issue(
                issue_id="brutus_file_missing",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"Brutus file does not exist: {brutus_path}",
                file_path=str(brutus_path)
            ))
            return issues

        if brutus_path.stat().st_size == 0:
            issues.append(create_issue(
                issue_id="brutus_file_empty",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"Brutus file is empty: {brutus_path.name}",
                file_path=str(brutus_path)
            ))
            return issues

        # Parse the file (which validates the format)
        try:
            snapshots, footer = parse_brutus_file(brutus_path)

            # Check we have at least one snapshot
            if not snapshots:
                issues.append(create_issue(
                    issue_id="no_snapshots",
                    severity=ValidationStatus.ERROR,
                    module="file_format",
                    message=f"No valid snapshots found in file",
                    file_path=str(brutus_path)
                ))

            # Validate each snapshot
            for i, snapshot in enumerate(snapshots):
                # Check snapshot has exactly 3 particles
                if len(snapshot.particles) != 3:
                    issues.append(create_issue(
                        issue_id=f"snapshot_{i}_wrong_particle_count",
                        severity=ValidationStatus.ERROR,
                        module="file_format",
                        message=f"Snapshot {i}: Expected 3 particles, found {len(snapshot.particles)}",
                        file_path=str(brutus_path),
                        metadata={"snapshot_index": i, "particle_count": len(snapshot.particles)}
                    ))

                # Check each particle has at least 7 values
                for j, particle in enumerate(snapshot.particles):
                    if len(particle) < 7:
                        issues.append(create_issue(
                            issue_id=f"snapshot_{i}_particle_{j}_insufficient_values",
                            severity=ValidationStatus.ERROR,
                            module="file_format",
                            message=f"Snapshot {i}, particle {j}: Expected at least 7 values, found {len(particle)}",
                            file_path=str(brutus_path),
                            metadata={"snapshot_index": i, "particle_index": j, "value_count": len(particle)}
                        ))

                # Check for NaN or infinite values
                for j, particle in enumerate(snapshot.particles):
                    for k, value in enumerate(particle[:7]):  # Check first 7 values
                        import math
                        if math.isnan(value) or math.isinf(value):
                            issues.append(create_issue(
                                issue_id=f"snapshot_{i}_particle_{j}_value_{k}_nan_inf",
                                severity=ValidationStatus.ERROR,
                                module="file_format",
                                message=f"Snapshot {i}, particle {j}, value {k}: NaN or infinite value",
                                file_path=str(brutus_path),
                                metadata={"snapshot_index": i, "particle_index": j, "value_index": k, "value": value}
                            ))

            # Check for footer presence (optional but noted)
            if not footer:
                issues.append(create_issue(
                    issue_id="missing_footer",
                    severity=ValidationStatus.WARNING,
                    module="file_format",
                    message="Result footer missing (optional)",
                    file_path=str(brutus_path)
                ))

            # If no issues, add a success marker
            if not issues:
                issues.append(create_issue(
                    issue_id="brutus_format_valid",
                    severity=ValidationStatus.PASS,
                    module="file_format",
                    message=f"Brutus file format is valid",
                    file_path=str(brutus_path)
                ))

        except ValueError as e:
            issues.append(create_issue(
                issue_id="brutus_format_error",
                severity=ValidationStatus.ERROR,
                module="file_format",
                message=f"Brutus file format error: {str(e)}",
                file_path=str(brutus_path)
            ))

    except Exception as e:
        issues.append(create_issue(
            issue_id="brutus_validation_error",
            severity=ValidationStatus.ERROR,
            module="file_format",
            message=f"Unexpected error validating Brutus file: {str(e)}",
            file_path=str(brutus_path)
        ))
        logging.error(f"Error validating Brutus file {brutus_path}: {e}", exc_info=True)

    return issues
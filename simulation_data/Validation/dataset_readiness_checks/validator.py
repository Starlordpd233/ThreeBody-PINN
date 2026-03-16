#!/usr/bin/env python3
"""
Main validator orchestration for the Three-Body Problem database validation system.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .datastructures import ValidationReport, DatasetValidationResult, FileValidationResult, create_issue, ValidationStatus
from .config import config, ValidationConfig
from .utils.logging import setup_logging, get_logger


class Validator:
    """Main validator class that orchestrates all validation modules."""

    def __init__(self, config_instance=None):
        self.config = config_instance or config
        self.logger = get_logger()

        # Import modules dynamically to avoid circular imports
        self.modules = {}
        self._load_modules()

    def _load_modules(self):
        """Dynamically load validation modules."""
        try:
            from .modules import (
                validate_correspondence,
                validate_ic_format,
                validate_brutus_format,
                validate_completeness,
                validate_metadata,
                validate_ic_physics,
                validate_parameters,
                validate_metrics,
                validate_against_blacklist,
                validate_coverage,
                validate_curriculum,
                validate_temporal
            )

            self.modules = {
                'correspondence': validate_correspondence,
                'file_format': {
                    'ic': validate_ic_format,
                    'brutus': validate_brutus_format
                },
                'completeness': validate_completeness,
                'metadata': validate_metadata,
                'physics': validate_ic_physics,
                'parameters': validate_parameters,
                'metrics': validate_metrics,
                'blacklist': validate_against_blacklist,
                'coverage': validate_coverage,
                'curriculum': validate_curriculum,
                'temporal': validate_temporal
            }

        except ImportError as e:
            self.logger.error(f"Failed to load validation modules: {e}")
            raise

    def validate_dataset(self, variant: str) -> DatasetValidationResult:
        """
        Validate a single dataset variant.

        Args:
            variant: Dataset variant name

        Returns:
            DatasetValidationResult with all validation findings
        """
        self.logger.info(f"Validating dataset variant: {variant}")

        result = DatasetValidationResult(variant_name=variant)

        # Check if directories exist
        ic_dir = self.config.get_ic_dir(variant)
        brutus_dir = self.config.get_brutus_dir(variant)

        if not ic_dir.exists():
            self.logger.error(f"IC directory not found: {ic_dir}")
            result.global_issues.append(create_issue(
                issue_id="ic_dir_missing",
                severity=ValidationStatus.ERROR,
                module="validator",
                message=f"IC directory does not exist: {ic_dir}",
                file_path=str(ic_dir)
            ))
            return result

        if not brutus_dir.exists():
            self.logger.error(f"Brutus directory not found: {brutus_dir}")
            result.global_issues.append(create_issue(
                issue_id="brutus_dir_missing",
                severity=ValidationStatus.ERROR,
                module="validator",
                message=f"Brutus directory does not exist: {brutus_dir}",
                file_path=str(brutus_dir)
            ))
            return result

        # List all files in directories
        ic_files = list(ic_dir.glob("*.txt"))
        brutus_files = list(brutus_dir.glob("*.txt"))

        self.logger.info(f"Found {len(ic_files)} IC files and {len(brutus_files)} Brutus files")

        # Validate IC files
        for ic_file in sorted(ic_files):
            file_number = self._extract_file_number(ic_file, variant, 'ic')
            if file_number is None:
                self.logger.warning(f"Skipping non-conforming IC file: {ic_file.name}")
                continue

            file_result = self._validate_ic_file(ic_file, variant, file_number)
            result.ic_results[file_number] = file_result

        # Validate Brutus files
        for brutus_file in sorted(brutus_files):
            file_number = self._extract_file_number(brutus_file, variant, 'brutus')
            if file_number is None:
                self.logger.warning(f"Skipping non-conforming Brutus file: {brutus_file.name}")
                continue

            file_result = self._validate_brutus_file(brutus_file, variant, file_number)
            result.brutus_results[file_number] = file_result

        # Check correspondence (if module is enabled)
        if 'correspondence' in self.config.enabled_modules:
            try:
                issues = self.modules['correspondence'](variant)
                result.correspondence_issues.extend(issues)
            except Exception as e:
                self.logger.error(f"Error in correspondence validation for {variant}: {e}")
                result.correspondence_issues.append(create_issue(
                    issue_id="correspondence_module_error",
                    severity=ValidationStatus.ERROR,
                    module="validator",
                    message=f"Correspondence module failed: {str(e)}",
                    file_path=f"{variant}"
                ))

        # Generate summary statistics
        self._generate_summary_stats(result)

        self.logger.info(f"Completed validation for {variant}")
        return result

    def _extract_file_number(self, filepath: Path, variant: str, file_type: str) -> Optional[int]:
        """Extract numeric file number from filename."""
        from .utils.naming import validate_filename_pattern
        return validate_filename_pattern(variant, file_type, filepath.name)

    def _validate_ic_file(self, filepath: Path, variant: str, file_number: int) -> FileValidationResult:
        """Validate a single IC file."""
        result = FileValidationResult(
            file_path=str(filepath),
            file_type='ic',
            dataset_variant=variant,
            file_number=file_number
        )

        # Run enabled validation modules for IC files
        if 'file_format' in self.config.enabled_modules:
            issues = self.modules['file_format']['ic'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        if 'physics' in self.config.enabled_modules:
            issues = self.modules['physics'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        if 'blacklist' in self.config.enabled_modules:
            issues = self.modules['blacklist'](filepath, variant, file_number)
            for issue in issues:
                result.add_issue(issue)
                
        if 'coverage' in self.config.enabled_modules:
            issues = self.modules['coverage'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)
                
        if 'curriculum' in self.config.enabled_modules:
            issues = self.modules['curriculum'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        return result

    def _validate_brutus_file(self, filepath: Path, variant: str, file_number: int) -> FileValidationResult:
        """Validate a single Brutus output file."""
        result = FileValidationResult(
            file_path=str(filepath),
            file_type='brutus',
            dataset_variant=variant,
            file_number=file_number
        )

        # Run enabled validation modules for Brutus files
        if 'file_format' in self.config.enabled_modules:
            issues = self.modules['file_format']['brutus'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        if 'completeness' in self.config.enabled_modules:
            issues = self.modules['completeness'](filepath, self.config.completeness_threshold)
            for issue in issues:
                result.add_issue(issue)

        if 'metadata' in self.config.enabled_modules:
            issues = self.modules['metadata'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        if 'parameters' in self.config.enabled_modules:
            issues = self.modules['parameters'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        if 'metrics' in self.config.enabled_modules:
            metrics_file = self.config.get_metrics_dir(variant) / f"metrics_{variant}_{file_number:04d}.json"
            if metrics_file.exists():
                issues = self.modules['metrics'](filepath, metrics_file, variant)
                for issue in issues:
                    result.add_issue(issue)
            else:
                result.add_issue(create_issue(
                    issue_id="metrics_file_missing",
                    severity=ValidationStatus.WARNING,
                    module="validator",
                    message=f"Metrics file not found: {metrics_file.name}",
                    file_path=str(filepath)
                ))
                
        if 'temporal' in self.config.enabled_modules:
            issues = self.modules['temporal'](filepath, variant)
            for issue in issues:
                result.add_issue(issue)

        return result

    def _generate_summary_stats(self, result: DatasetValidationResult):
        """Generate summary statistics for a dataset validation result."""
        # Count files by status
        ic_status_counts = {status.value: 0 for status in ValidationStatus}
        brutus_status_counts = {status.value: 0 for status in ValidationStatus}

        for file_result in result.ic_results.values():
            status = file_result.overall_status()
            ic_status_counts[status.value] += 1

        for file_result in result.brutus_results.values():
            status = file_result.overall_status()
            brutus_status_counts[status.value] += 1

        # Count issues by severity
        issue_counts = {status.value: 0 for status in ValidationStatus}
        for file_result in list(result.ic_results.values()) + list(result.brutus_results.values()):
            for issue in file_result.issues:
                issue_counts[issue.severity.value] += 1

        result.summary_stats = {
            'ic_count': len(result.ic_results),
            'brutus_count': len(result.brutus_results),
            'ic_status_counts': ic_status_counts,
            'brutus_status_counts': brutus_status_counts,
            'issue_counts': issue_counts,
            'missing_brutus': result.get_missing_brutus(),
            'missing_ic': result.get_missing_ic(),
            'total_issues': sum(issue_counts.values())
        }

    def validate_datasets(self, variants: List[str]) -> ValidationReport:
        """
        Validate multiple dataset variants.

        Args:
            variants: List of dataset variant names

        Returns:
            Complete ValidationReport with results for all datasets
        """
        self.logger.info(f"Starting validation for {len(variants)} dataset variants: {', '.join(variants)}")

        report = ValidationReport(
            timestamp=datetime.now().isoformat(),
            config={
                'completeness_threshold': self.config.completeness_threshold,
                'energy_tolerance': self.config.energy_tolerance,
                'enabled_modules': self.config.enabled_modules
            }
        )

        for variant in variants:
            if variant not in self.config.dataset_variants:
                self.logger.error(f"Unknown dataset variant: {variant}")
                report.global_issues.append(create_issue(
                    issue_id="unknown_variant",
                    severity=ValidationStatus.ERROR,
                    module="validator",
                    message=f"Unknown dataset variant: {variant}"
                ))
                continue

            try:
                dataset_result = self.validate_dataset(variant)
                report.datasets[variant] = dataset_result
            except Exception as e:
                self.logger.error(f"Failed to validate dataset variant {variant}: {e}")
                report.global_issues.append(create_issue(
                    issue_id="dataset_validation_error",
                    severity=ValidationStatus.ERROR,
                    module="validator",
                    message=f"Failed to validate dataset variant {variant}: {str(e)}"
                ))

        self.logger.info(f"Completed validation for all {len(variants)} dataset variants")
        return report

    def get_status_summary(self, report: ValidationReport) -> Dict[str, Any]:
        """Get a summary of validation status across all datasets."""
        return report.get_summary()


# Convenience function for quick validation
def run_validation(variants: Optional[List[str]] = None,
                  output_dir: Optional[Path] = None,
                  threshold: Optional[float] = None,
                  modules: Optional[List[str]] = None) -> ValidationReport:
    """
    Convenience function to run validation with minimal configuration.

    Args:
        variants: List of dataset variants to validate (default: all)
        output_dir: Directory for output reports (default: config default)
        threshold: Completeness threshold (default: config default)
        modules: Specific validation modules to run (default: all)

    Returns:
        ValidationReport with results
    """
    # Set up configuration
    validation_config = ValidationConfig()

    if modules:
        validation_config.enabled_modules = modules

    if threshold is not None:
        validation_config.completeness_threshold = threshold

    if output_dir is not None:
        validation_config.output_dir = output_dir

    if variants is None:
        variants = list(validation_config.dataset_variants.keys())

    # Set up logging
    setup_logging(validation_config.output_dir / 'logs')

    # Run validation
    validator = Validator(validation_config)
    report = validator.validate_datasets(variants)

    return report
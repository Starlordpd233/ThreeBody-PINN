#!/usr/bin/env python3
"""
Logging utilities for the Three-Body Problem database validation system.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class ValidationLogger:
    """Centralized logging for validation system."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_dir: Optional[Path] = None, level: int = logging.INFO):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.log_dir = log_dir
        if self.log_dir is None:
            # Default to validation_system/logs/
            base_dir = Path(__file__).parent.parent.parent
            self.log_dir = base_dir / "validation_system" / "logs"

        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        self.logger = logging.getLogger("three_body_validator")
        self.logger.setLevel(level)

        # Clear existing handlers to avoid duplicate logs
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.log_dir / f"validation_{timestamp}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

        self._initialized = True

    def log_validation_start(self, variant: str, file_count: int):
        """Log start of validation for a dataset variant."""
        self.logger.info(f"Starting validation for {variant} ({file_count} files)")

    def log_module_start(self, module: str, file_path: Path):
        """Log start of a validation module for a specific file."""
        self.logger.debug(f"Module {module}: processing {file_path.name}")

    def log_issue(self, issue):
        """Log a validation issue."""
        from ..datastructures import ValidationStatus

        level_map = {
            ValidationStatus.ERROR: logging.ERROR,
            ValidationStatus.FAIL: logging.WARNING,
            ValidationStatus.WARNING: logging.WARNING,
            ValidationStatus.PASS: logging.DEBUG,
            ValidationStatus.SKIPPED: logging.DEBUG
        }

        log_level = level_map.get(issue.severity, logging.INFO)
        message = f"{issue.severity.value} - {issue.module} - {issue.message}"
        if issue.file_path:
            message += f" (File: {issue.file_path})"

        self.logger.log(log_level, message)

    def log_summary(self, report):
        """Log validation summary."""
        summary = report.get_summary()
        self.logger.info("Validation complete:")
        self.logger.info(f"  Total files: {summary['total_files']}")
        self.logger.info(f"  Total issues: {summary['total_issues']}")
        for status, count in summary['status_counts'].items():
            if count > 0:
                self.logger.info(f"  {status}: {count}")

    def log_error(self, message: str, exc_info: bool = False):
        """Log an error message."""
        self.logger.error(message, exc_info=exc_info)

    def log_warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)

    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def log_debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)


def setup_logging(log_dir: Optional[Path] = None, level: int = logging.INFO) -> ValidationLogger:
    """Set up logging and return logger instance."""
    logger = ValidationLogger(log_dir, level)
    return logger


def get_logger() -> ValidationLogger:
    """Get the global logger instance."""
    if ValidationLogger._instance is None:
        setup_logging()
    return ValidationLogger._instance


# Context manager for timing operations
class TimedOperation:
    """Context manager for timing operations with logging."""

    def __init__(self, operation_name: str, logger: Optional[ValidationLogger] = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger()
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        if exc_type is None:
            self.logger.info(f"Completed {self.operation_name} in {duration:.2f} seconds")
        else:
            self.logger.error(f"Operation {self.operation_name} failed after {duration:.2f} seconds: {exc_val}")
        return False  # Don't suppress exceptions


# Decorator for error handling
def handle_validation_errors(func):
    """Decorator to catch and log validation errors."""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logger = get_logger()
            logger.error(f"File not found: {e}")
            return []  # Return empty issues list
        except PermissionError as e:
            logger.error(f"Permission denied: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            return []
    return wrapper
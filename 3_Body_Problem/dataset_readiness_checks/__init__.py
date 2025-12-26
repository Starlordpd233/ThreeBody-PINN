"""
Dataset Readiness Checks
========================

A comprehensive validation suite for the Three-Body Problem dataset, ensuring 
readiness for PINN training.

Modules:
    - validator: Main orchestration
    - config: Configuration
    - reports: Reporting utilities
    - modules: Individual validation logic
"""

from .validator import Validator, run_validation
from .config import config
from .datastructures import ValidationReport, DatasetValidationResult, ValidationStatus

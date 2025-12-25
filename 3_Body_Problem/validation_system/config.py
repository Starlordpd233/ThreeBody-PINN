#!/usr/bin/env python3
"""
Configuration management for the Three-Body Problem database validation system.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class ValidationConfig:
    """Central configuration for validation."""

    # Base paths
    base_dir: Path = Path("<home>/Desktop/cursor/3_Body_Problem")

    # Dataset mappings - these define the 4-to-4 correspondence
    dataset_variants: Dict[str, Dict[str, str]] = None

    # Validation thresholds
    completeness_threshold: float = 9.5
    energy_tolerance: float = 1e-6
    com_tolerance_standard: float = 1e-10
    com_tolerance_hierarchical: float = 0.05
    min_snapshots: int = 10

    # File patterns (handling naming inconsistencies)
    ic_patterns: Dict[str, str] = None
    brutus_patterns: Dict[str, str] = None

    # Module enable/disable
    enabled_modules: List[str] = None

    # Output settings
    output_dir: Path = None
    report_formats: List[str] = None  # ['json', 'markdown', 'csv']

    def __post_init__(self):
        """Initialize default configurations."""
        if self.dataset_variants is None:
            self.dataset_variants = {
                "hierarchical": {
                    "ic_dir": "final_stage_ic_datasets/ic_hierarchical",
                    "brutus_dir": "brutus_output/brutus_hierarchical"
                },
                "hierarchical_gold": {
                    "ic_dir": "final_stage_ic_datasets/ic_hierarchical_for_gold_standard",
                    "brutus_dir": "brutus_output/brutus_hierarchical_gold_standard"
                },
                "standard": {
                    "ic_dir": "final_stage_ic_datasets/ic_standard_quasi_random",
                    "brutus_dir": "brutus_output/brutus_standard_quasi_random"
                },
                "standard_gold": {
                    "ic_dir": "final_stage_ic_datasets/ic_standard_quasi_random_for_gold_standard",
                    "brutus_dir": "brutus_output/brutus_standard_quasi_random_gold_standard"
                }
            }

        if self.ic_patterns is None:
            self.ic_patterns = {
                "hierarchical": "ic_hierarchical_{num:04d}.txt",
                "hierarchical_gold": "ic_hierarchical_{num:04d}.txt",
                "standard": "ic_standard_{num:04d}.txt",
                "standard_gold": "ic_standard_{num:04d}.txt"
            }

        if self.brutus_patterns is None:
            self.brutus_patterns = {
                "hierarchical": "brutus_hierarchical_{num:04d}.txt",
                "hierarchical_gold": "brutus_hierarchical_gold_{num:04d}.txt",  # Note: gold not gold_standard
                "standard": "brutus_standard_{num:04d}.txt",  # Note: missing _quasi_random
                "standard_gold": "brutus_standard_gold_{num:04d}.txt"  # Note: missing _quasi_random
            }

        if self.enabled_modules is None:
            self.enabled_modules = [
                "correspondence",
                "file_format",
                "completeness",
                "metadata",
                "physics",
                "parameters",
                "metrics",
                "blacklist"
            ]

        if self.output_dir is None:
            self.output_dir = self.base_dir / "validation_system" / "reports"

        if self.report_formats is None:
            self.report_formats = ["json", "markdown", "csv"]

    def get_ic_dir(self, variant: str) -> Path:
        """Get the full path to the IC directory for a given variant."""
        if variant not in self.dataset_variants:
            raise ValueError(f"Unknown dataset variant: {variant}")
        return self.base_dir / self.dataset_variants[variant]["ic_dir"]

    def get_brutus_dir(self, variant: str) -> Path:
        """Get the full path to the Brutus output directory for a given variant."""
        if variant not in self.dataset_variants:
            raise ValueError(f"Unknown dataset variant: {variant}")
        return self.base_dir / self.dataset_variants[variant]["brutus_dir"]

    def get_ic_pattern(self, variant: str) -> str:
        """Get the filename pattern for IC files for a given variant."""
        if variant not in self.ic_patterns:
            raise ValueError(f"No IC pattern for variant: {variant}")
        return self.ic_patterns[variant]

    def get_brutus_pattern(self, variant: str) -> str:
        """Get the filename pattern for Brutus output files for a given variant."""
        if variant not in self.brutus_patterns:
            raise ValueError(f"No Brutus pattern for variant: {variant}")
        return self.brutus_patterns[variant]

    def get_metrics_dir(self, variant: str) -> Path:
        """Get the metrics directory for a given variant."""
        # Map variant names to metrics directory names
        variant_to_metrics = {
            "hierarchical": "sim_result_metric_hierarchical",
            "hierarchical_gold": "sim_result_metric_hierarchical_gold_standard",
            "standard": "sim_result_metric_standard",
            "standard_gold": "sim_result_metric_standard_gold_standard"
        }
        if variant not in variant_to_metrics:
            raise ValueError(f"No metrics directory mapping for variant: {variant}")
        return self.base_dir / "brutus_metrics" / variant_to_metrics[variant]

    def get_blacklist_ids(self) -> Dict[str, List[int]]:
        """Load blacklisted IC IDs from the problematic_ics_blacklist.json file."""
        import json
        blacklist_file = self.base_dir / "problematic_ics_blacklist.json"
        if blacklist_file.exists():
            with open(blacklist_file, 'r') as f:
                return json.load(f)
        return {"hierarchical": [], "standard": []}

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'ValidationConfig':
        """Load configuration from YAML file."""
        import yaml
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, yaml_path: Path):
        """Save configuration to YAML file."""
        import yaml
        data = {
            "completeness_threshold": self.completeness_threshold,
            "energy_tolerance": self.energy_tolerance,
            "com_tolerance_standard": self.com_tolerance_standard,
            "com_tolerance_hierarchical": self.com_tolerance_hierarchical,
            "min_snapshots": self.min_snapshots,
            "enabled_modules": self.enabled_modules
        }
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)


# Global configuration instance
config = ValidationConfig()
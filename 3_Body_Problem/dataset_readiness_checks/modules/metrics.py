"""
Metrics validation module.
"""

from pathlib import Path
from typing import List
import json

from ..datastructures import ValidationIssue, ValidationStatus, create_issue

def validate_metrics(brutus_path: Path, metrics_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate metrics JSON file.
    """
    issues = []
    
    try:
        with open(metrics_path, 'r') as f:
            data = json.load(f)
            
        # Check required nested keys
        conservation = data.get('conservation', {})
        energy = conservation.get('energy', {})
        momentum = conservation.get('linear_momentum', {})

        if not energy:
            issues.append(create_issue(
                "missing_metric_key", ValidationStatus.WARNING, "metrics",
                "Missing conservation.energy section", str(metrics_path)
            ))
        if not momentum:
            issues.append(create_issue(
                "missing_metric_key", ValidationStatus.WARNING, "metrics",
                "Missing conservation.linear_momentum section", str(metrics_path)
            ))

        # Basic sanity check on energy conservation
        if 'relative_error' in energy:
            rel_err = abs(energy['relative_error'])
            if rel_err > 1.0:
                issues.append(create_issue(
                    "extreme_energy_drift", ValidationStatus.WARNING, "metrics",
                    f"Extreme energy relative error: {rel_err:.4e}", str(metrics_path)
                ))
                
    except json.JSONDecodeError:
        issues.append(create_issue(
            "corrupt_metrics_json", ValidationStatus.ERROR, "metrics",
            "Metrics file is not valid JSON", str(metrics_path)
        ))
    except Exception as e:
        issues.append(create_issue(
            "metrics_check_error", ValidationStatus.ERROR, "metrics",
            f"Error checking metrics: {str(e)}", str(metrics_path)
        ))
        
    return issues

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
            
        # Check required keys
        required_keys = ['final_energy_error', 'energy_drift', 'momentum_drift']
        for key in required_keys:
            if key not in data:
                issues.append(create_issue(
                    "missing_metric_key", ValidationStatus.WARNING, "metrics",
                    f"Missing metric key: {key}", str(metrics_path)
                ))
                
        # Basic sanity check on values
        # Energy error shouldn't be massive (unless it's a failed run, which is interesting to know)
        if 'energy_drift' in data:
            drift = abs(data['energy_drift'])
            if drift > 1.0: # 100% error
                 issues.append(create_issue(
                    "extreme_energy_drift", ValidationStatus.WARNING, "metrics",
                    f"Extreme energy drift: {drift:.4f}", str(metrics_path)
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

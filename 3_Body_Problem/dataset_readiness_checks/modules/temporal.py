"""
Temporal validation module.
"""

from pathlib import Path
from typing import List
import numpy as np

from ..datastructures import ValidationIssue, ValidationStatus, create_issue

def validate_temporal(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate temporal consistency (uniform dt).
    """
    issues = []
    
    try:
        # Read timestamps
        times = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3 and parts[1] == '3':
                try:
                    times.append(float(parts[0]))
                except ValueError:
                    pass
                    
        if len(times) < 2:
             return [] # Handled by completeness
             
        # Check dt consistency
        times = np.array(times)
        dts = np.diff(times)
        
        mean_dt = np.mean(dts)
        std_dt = np.std(dts)
        
        # If std is high relative to mean, dt is not uniform
        if std_dt / mean_dt > 0.01: # 1% variation
             issues.append(create_issue(
                "non_uniform_dt", ValidationStatus.WARNING, "temporal",
                f"Timesteps are not uniform: mean={mean_dt:.4f}, std={std_dt:.6f}", str(file_path)
            ))
            
        # Check monotonicity
        if np.any(dts <= 0):
             issues.append(create_issue(
                "non_monotonic_time", ValidationStatus.ERROR, "temporal",
                "Timestamps are not strictly increasing", str(file_path)
            ))
            
    except Exception as e:
        issues.append(create_issue(
            "temporal_check_error", ValidationStatus.ERROR, "temporal",
            f"Error checking temporal consistency: {str(e)}", str(file_path)
        ))
        
    return issues

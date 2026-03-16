"""
Parameter validation module.
"""

from pathlib import Path
from typing import List
import re

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_result_footer

def validate_parameters(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate simulation parameters (dt_out, tolerance, etc.).
    
    Expected dt_out:
    - Hierarchical (standard): 0.08
    - Standard (standard): 0.17
    - Gold (any): 0.01
    """
    issues = []
    
    # Determine expected values
    expected_dt = None
    if 'gold' in variant:
        expected_dt = 0.01
    elif 'hierarchical' in variant:
        expected_dt = 0.08
    elif 'standard' in variant:
        expected_dt = 0.17
        
    try:
        # Try to find Result footer first
        footer = None
        # ... logic to read footer ...
        # But we also want to check actual dt from snapshots if footer is missing/wrong
        
        # Read first few lines to get dt from snapshots
        with open(file_path, 'r') as f:
            lines = [f.readline() for _ in range(50)] # Read header + a few snapshots
            
        # Parse first two timestamps
        times = []
        for line in lines:
            parts = line.strip().split()
            # Header format: t N t_cpu
            if len(parts) == 3 and parts[1] == '3':
                try:
                    times.append(float(parts[0]))
                    if len(times) >= 2:
                        break
                except ValueError:
                    pass
                    
        measured_dt = None
        if len(times) >= 2:
            measured_dt = times[1] - times[0]
            
        # Validate dt
        if expected_dt is not None:
            # Check footer if exists
            # (omitted for brevity, relying on measured_dt which is ground truth)
            
            if measured_dt is not None:
                # Allow small float error
                if abs(measured_dt - expected_dt) > 1e-4:
                     issues.append(create_issue(
                        "dt_mismatch", ValidationStatus.WARNING, "parameters",
                        f"Measured dt={measured_dt:.4f}, expected {expected_dt}", str(file_path)
                    ))
            else:
                 issues.append(create_issue(
                    "cannot_determine_dt", ValidationStatus.WARNING, "parameters",
                    "Could not extract timestamps to verify dt", str(file_path)
                ))
                
    except Exception as e:
        issues.append(create_issue(
            "parameter_check_error", ValidationStatus.ERROR, "parameters",
            f"Error checking parameters: {str(e)}", str(file_path)
        ))
        
    return issues

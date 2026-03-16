"""
Coverage validation module (PINN Input Vector).
"""

from pathlib import Path
from typing import List
import numpy as np

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_ic_file
from ..utils.physics_core import compute_13_component_vector

def validate_coverage(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate that PINN input vector can be computed and is finite.
    """
    issues = []
    
    try:
        particles = parse_ic_file(file_path)
        
        # Unpack
        masses = np.array([p[0] for p in particles])
        r_initial = np.array([[p[1], p[2], p[3]] for p in particles])
        v_initial = np.array([[p[4], p[5], p[6]] for p in particles])
        
        # Scaling
        # We need global scales ideally, but for checking NaNs/Infs, local scaling or unit scaling is enough
        # provided we don't divide by zero.
        # The physics_core uses defaults which are safe (1.0).
        
        vector = compute_13_component_vector(masses, r_initial, v_initial)
        
        if not np.all(np.isfinite(vector)):
             issues.append(create_issue(
                "input_vector_nan", ValidationStatus.ERROR, "coverage",
                f"Input vector contains NaNs or Infs: {vector}", str(file_path)
            ))
            
        # Check range [-1, 1] (roughly)
        # Tanh ensures [-1, 1] mostly, but check outliers
        if np.any(np.abs(vector) > 1.0001): # slight tolerance
             issues.append(create_issue(
                "input_vector_out_of_bounds", ValidationStatus.WARNING, "coverage",
                "Input vector components outside [-1, 1]", str(file_path)
            ))
            
    except Exception as e:
        issues.append(create_issue(
            "coverage_check_error", ValidationStatus.ERROR, "coverage",
            f"Error computing input vector: {str(e)}", str(file_path)
        ))
        
    return issues

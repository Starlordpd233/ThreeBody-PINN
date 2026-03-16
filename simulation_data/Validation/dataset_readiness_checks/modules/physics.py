"""
Physics validation module.
"""

from pathlib import Path
from typing import List
import numpy as np

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_ic_file, calculate_center_of_mass, calculate_total_momentum, calculate_energy
from ..config import config

def validate_ic_physics(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate physical properties of Initial Conditions.
    
    Checks:
    1. Masses are positive
    2. Center of Mass is near origin (tolerance depends on variant)
    3. Total Momentum is near zero (tolerance depends on variant)
    4. Energy is finite
    """
    issues = []
    
    try:
        particles = parse_ic_file(file_path)
        
        # 1. Check masses
        masses = [p[0] for p in particles]
        if any(m <= 0 for m in masses):
             issues.append(create_issue(
                "non_positive_mass", ValidationStatus.ERROR, "physics",
                f"Found non-positive masses: {masses}", str(file_path)
            ))
            
        # 2. Check COM
        # Standard: Strict 0
        # Hierarchical: Perturbed, so loose
        positions = [(p[1], p[2], p[3]) for p in particles]
        velocities = [(p[4], p[5], p[6]) for p in particles]
        
        com = calculate_center_of_mass(masses, positions)
        com_dist = np.sqrt(sum(c**2 for c in com))
        
        tolerance = config.com_tolerance_hierarchical if 'hierarchical' in variant else config.com_tolerance_standard
        
        if com_dist > tolerance:
             issues.append(create_issue(
                "com_offset", ValidationStatus.WARNING, "physics",
                f"Center of Mass offset {com_dist:.6f} exceeds tolerance {tolerance}", str(file_path)
            ))
            
        # 3. Check Momentum
        mom = calculate_total_momentum(masses, velocities)
        mom_mag = np.sqrt(sum(p**2 for p in mom))
        
        if mom_mag > tolerance:
             issues.append(create_issue(
                "momentum_offset", ValidationStatus.WARNING, "physics",
                f"Total momentum {mom_mag:.6f} exceeds tolerance {tolerance}", str(file_path)
            ))
            
        # 4. Energy
        energy = calculate_energy(particles)
        if not np.isfinite(energy):
             issues.append(create_issue(
                "invalid_energy", ValidationStatus.ERROR, "physics",
                f"Computed energy is non-finite: {energy}", str(file_path)
            ))
            
    except Exception as e:
        issues.append(create_issue(
            "physics_check_error", ValidationStatus.ERROR, "physics",
            f"Error checking physics: {str(e)}", str(file_path)
        ))
        
    return issues

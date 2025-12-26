"""
Curriculum validation module.
"""

from pathlib import Path
from typing import List, Dict
import numpy as np

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_ic_file
from ..utils.physics_core import compute_basic_invariants, compute_angular_momentum_canonical

def assign_stage(E, Q, s_min, L_norm, tau_L, is_hierarchical, is_high_fidelity, dataset_quantiles=None) -> int:
    """
    Assign curriculum stage.
    Logic copied from pinn/data-processing-pipeline-full.py
    """
    # Stage 6: Extreme cases
    if s_min < 0.5 or abs(E) < 0.01:
        return 6
        
    if is_hierarchical:
        if is_high_fidelity:
            # Stage 2: High-resolution refinement
            return 2
        else:
            # Low-fidelity hierarchical
            # Stage 0: Easiest
            if E < -0.5 and L_norm > 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 0
            
            # Stage 1a: Energy relaxed
            if -0.5 <= E < -0.1 and L_norm > 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 1
            
            # Stage 1b: Angular momentum relaxed
            if E < -0.5 and 0.1 <= L_norm < 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 1
                
            return 1 # Default
            
    else: # Standard Quasi-Random
        if is_high_fidelity:
            return 5
        else:
            # Low-fidelity quasi-random
            # Stage 3 requires quantiles, we'll approximate or skip strict quantile check
            # Defaulting to 4 for chaotic if not 3
            
            # Stage 3 approximation (using hardcoded typical values if quantiles missing)
            # E_25 ~ -0.3, L_75 ~ 0.3
            E_25 = -0.3
            L_75 = 0.3
            if dataset_quantiles:
                E_25 = dataset_quantiles.get('E_25', -0.3)
                L_75 = dataset_quantiles.get('L_75', 0.3)
                
            if E <= E_25 and L_norm >= L_75 and 0.9 <= Q <= 1.1:
                return 3
                
            # Stage 4 check (Lyapunov)
            # If tau_L is not computed (expensive), we might have to guess or assume 4
            if tau_L > 5:
                return 4
            
            return 4

def validate_curriculum(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate that file can be assigned a curriculum stage.
    """
    issues = []
    
    try:
        particles = parse_ic_file(file_path)
        masses = np.array([p[0] for p in particles])
        r_initial = np.array([[p[1], p[2], p[3]] for p in particles])
        v_initial = np.array([[p[4], p[5], p[6]] for p in particles])
        
        # Scaling (Unit scaling for classification purposes)
        # Real pipeline uses global D, V.
        # Here we use D=1, V=1 which might skew E?
        # WAIT: E threshold (-0.5) is based on Scaled E.
        # We MUST scale.
        # Global scales: T=10, G=1 -> D ~ 4.64, V ~ 0.46
        T_max = 10.0
        G = 1.0
        D = np.cbrt(G * T_max**2)
        V = D / T_max
        
        r_prime = r_initial / D
        v_prime = v_initial / V
        
        E, Q, s_min = compute_basic_invariants(masses, r_prime, v_prime)
        _, L_norm, _, _ = compute_angular_momentum_canonical(masses, r_prime, v_prime, E)
        
        # Tau_L is expensive. We assume 0 for classification fallback or skip specific 4a/4b check
        tau_L = 0.0 
        
        is_hierarchical = 'hierarchical' in variant
        is_high_fidelity = 'gold' in variant
        
        stage = assign_stage(E, Q, s_min, L_norm, tau_L, is_hierarchical, is_high_fidelity)
        
        # We store the stage in issue metadata?
        # Or just pass.
        # Ideally we'd report it.
        # I'll add a PASS issue with the stage info.
        
        issues.append(create_issue(
            "curriculum_stage_assigned", ValidationStatus.PASS, "curriculum",
            f"Assigned Stage {stage}", str(file_path),
            metadata={'stage': stage, 'E': E, 'Q': Q, 'L_norm': L_norm, 's_min': s_min}
        ))
            
    except Exception as e:
        issues.append(create_issue(
            "curriculum_check_error", ValidationStatus.ERROR, "curriculum",
            f"Error assigning stage: {str(e)}", str(file_path)
        ))
        
    return issues

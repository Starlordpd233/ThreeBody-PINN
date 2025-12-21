"""Curriculum stage assignment logic"""

import numpy as np
from typing import Dict, Optional, List
from ..core.data_structures import PhysicalInvariants, ProcessedTrajectory


def compute_dataset_quantiles(trajectories: List[ProcessedTrajectory]) -> Dict[str, float]:
    """
    Compute dataset quantiles for Stage 3 assignment.
    Only uses low-fidelity quasi-random data.
    """
    low_fidelity_E = []
    low_fidelity_L_norm = []
    
    for traj in trajectories:
        if not traj.metadata.is_hierarchical and traj.metadata.fidelity == 'low':
            low_fidelity_E.append(traj.invariants.E)
            low_fidelity_L_norm.append(traj.invariants.L_norm)
    
    if not low_fidelity_E:
        return {}
    
    return {
        'E_25': np.percentile(low_fidelity_E, 25),
        'L_75': np.percentile(low_fidelity_L_norm, 75)
    }


def assign_curriculum_stage(invariants: PhysicalInvariants, 
                          is_hierarchical: bool,
                          is_high_fidelity: bool,
                          dataset_quantiles: Optional[Dict] = None) -> int:
    """
    Assign curriculum stage based on invariants and data type.
    
    Stages:
    0: Easiest hierarchical (low-fidelity)
    1: Moderately stable hierarchical (low-fidelity)
    2: High-resolution hierarchical refinement
    3: Moderately chaotic low-fidelity
    4: Chaotic low-fidelity
    5: High-resolution chaotic
    6: Near-collision and extreme cases
    """
    E = invariants.E
    Q = invariants.Q
    s_min = invariants.s_min
    L_norm = invariants.L_norm
    tau_L = invariants.tau_L
    
    # Stage 6: Extreme cases (highest priority, any dataset)
    if s_min < 0.5 or abs(E) < 0.01:
        return 6
    
    # For hierarchical data
    if is_hierarchical:
        if is_high_fidelity:
            # Stage 2: High-resolution refinement of stable orbits
            # This includes all hierarchical high-fidelity data
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
            
            # Other hierarchical that don't fit stages 0 or 1
            # These will be included in stage 2 during training
            return 1  # Default to stage 1 for consistency
    
    # For quasi-random data
    else:
        if is_high_fidelity:
            # Stage 5: High-resolution chaotic
            return 5
        else:
            # Low-fidelity quasi-random
            # Stage 3: Moderately chaotic (needs quantiles)
            if dataset_quantiles:
                E_25 = dataset_quantiles.get('E_25', -0.3)
                L_75 = dataset_quantiles.get('L_75', 0.3)
                
                if E <= E_25 and L_norm >= L_75 and 0.9 <= Q <= 1.1:
                    return 3
            
            # Stage 4a: Chaotic with longer predictability
            if tau_L > 5:
                return 4
            
            # Stage 4b: Highly chaotic
            if 2 < tau_L <= 5:
                return 4
            
            # Default for other chaotic cases
            return 4


def assign_stages_to_dataset(trajectories: List[ProcessedTrajectory], 
                           verbose: bool = True) -> None:
    """
    Assign curriculum stages to all trajectories in dataset.
    Modifies trajectories in-place by setting the stage attribute.
    """
    # First compute dataset quantiles
    dataset_quantiles = compute_dataset_quantiles(trajectories)
    
    if verbose and dataset_quantiles:
        print(f"Dataset quantiles for Stage 3:")
        print(f"  E_25: {dataset_quantiles['E_25']:.3f}")
        print(f"  L_75: {dataset_quantiles['L_75']:.3f}")
    
    # Assign stages
    stage_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    for traj in trajectories:
        stage = assign_curriculum_stage(
            traj.invariants,
            traj.metadata.is_hierarchical,
            traj.metadata.is_high_fidelity,
            dataset_quantiles
        )
        traj.stage = stage
        stage_counts[stage] += 1
    
    if verbose:
        print("\nStage assignment summary:")
        for stage in sorted(stage_counts.keys()):
            count = stage_counts[stage]
            if count > 0:
                print(f"  Stage {stage}: {count} trajectories")
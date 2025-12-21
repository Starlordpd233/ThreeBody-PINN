"""PINN input vector formulation"""

import numpy as np
from typing import Tuple, Optional
from ..core.data_structures import ScaledTrajectoryData, GlobalScales


def compute_shape_invariants(r_prime: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute universal shape invariants I1, I2, I3.
    
    Returns:
        I1: d_short/d_long ∈ [0, 1]
        I2: d_mid/d_long ∈ [I1, 1]
        I3: (d_short + d_mid - d_long)/(d_short + d_mid + d_long) ∈ [-1, 1]
    """
    # Compute pairwise distances
    d12 = np.linalg.norm(r_prime[0] - r_prime[1])
    d13 = np.linalg.norm(r_prime[0] - r_prime[2])
    d23 = np.linalg.norm(r_prime[1] - r_prime[2])
    
    # Sort distances
    distances = sorted([d12, d13, d23])
    d_short, d_mid, d_long = distances
    
    # Compute invariants
    I1 = d_short / (d_long + 1e-10)
    I2 = d_mid / (d_long + 1e-10)
    I3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long + 1e-10)
    
    return I1, I2, I3


def compute_velocity_angles(r_prime: np.ndarray, v_prime: np.ndarray, 
                          eps: float = 1e-10) -> Tuple[float, float]:
    """
    Compute angles between position and velocity vectors.
    
    Returns:
        Two normalized angles ∈ [0, 1]
    """
    angles = []
    for i in range(2):  # Only 2 angles needed
        r_norm = np.linalg.norm(r_prime[i])
        v_norm = np.linalg.norm(v_prime[i])
        
        if r_norm < eps or v_norm < eps:
            angle = np.pi / 2  # Default perpendicular
        else:
            dot = np.dot(r_prime[i], v_prime[i])
            cross = np.cross(r_prime[i], v_prime[i])
            cross_norm = np.linalg.norm(cross)
            angle = np.arctan2(cross_norm, dot)  # Stable [0, pi]
        
        angles.append(angle / np.pi)  # Normalize to [0,1]
    
    return tuple(angles)


def normalize_ic_components(invariants, masses, shape_invariants, velocity_angles,
                          global_scales: GlobalScales) -> np.ndarray:
    """
    Normalize all IC components to [-1, 1] range.
    
    Returns:
        13-component normalized IC vector
    """
    # Extract invariants
    E = invariants.E
    Q = invariants.Q
    s_min = invariants.s_min
    L_norm = invariants.L_norm
    I_norm = invariants.I_norm
    
    # Extract shape invariants
    I1, I2, I3 = shape_invariants
    
    # Extract velocity angles
    theta1, theta2 = velocity_angles
    
    # Normalize components
    E_norm = np.tanh(E / global_scales.E_scale)
    Q_norm = np.tanh((Q - 1) / global_scales.Q_scale)
    smin_norm = np.tanh(s_min / global_scales.smin_scale)
    
    # Mass fractions
    m_total = np.sum(masses) + 1e-8
    m_norm = 2 * (masses / m_total) - 1  # Array for all 3 masses
    
    # Shape invariants normalization
    I1_norm = 2 * I1 - 1  # Map [0,1] to [-1,1]
    I2_norm = 2 * I2 - 1  # Map [0,1] to [-1,1]
    # I3 already in [-1,1]
    
    # Velocity angles normalization
    theta_norm = 2 * np.array([theta1, theta2]) - 1  # Map [0,1] to [-1,1]
    
    # Moment of inertia normalization
    I_norm_bounded = np.tanh(I_norm)  # Bound to [-1,1]
    
    # Assemble IC vector
    ic_vector = np.concatenate([
        m_norm,                    # 3 components
        [E_norm],                  # 1 component
        [L_norm],                  # 1 component (already in [0,1], map to [-1,1])
        [Q_norm],                  # 1 component
        [smin_norm],               # 1 component
        [I1_norm, I2_norm, I3],    # 3 components
        theta_norm,                # 2 components
        [I_norm_bounded]           # 1 component
    ])
    
    # L_norm adjustment (it's already in [0,1], so map to [-1,1])
    ic_vector[4] = 2 * L_norm - 1
    
    assert len(ic_vector) == 13, f"IC vector should have 13 components, got {len(ic_vector)}"
    
    return ic_vector


def formulate_ic_vector(scaled_traj: ScaledTrajectoryData, 
                       invariants,
                       global_scales: GlobalScales,
                       apply_ordering: bool = True) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Formulate the 13-component IC vector for PINN input.
    
    Returns:
        ic_vector: 13-component normalized vector
        ordering: permutation indices if apply_ordering=True, else None
    """
    masses = scaled_traj.masses
    r_prime = scaled_traj.r_prime
    v_prime = scaled_traj.v_prime
    
    # Apply canonical ordering if requested
    if apply_ordering:
        from ..core.scaling import apply_canonical_ordering
        masses, r_prime, v_prime, ordering = apply_canonical_ordering(
            masses, r_prime, v_prime
        )
    else:
        ordering = None
    
    # Compute shape invariants
    shape_invariants = compute_shape_invariants(r_prime)
    
    # Compute velocity angles
    velocity_angles = compute_velocity_angles(r_prime, v_prime)
    
    # Normalize all components
    ic_vector = normalize_ic_components(
        invariants, masses, shape_invariants, velocity_angles, global_scales
    )
    
    return ic_vector, ordering
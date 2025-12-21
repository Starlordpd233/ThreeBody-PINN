# com_transform_ic.py
"""
COM frame transformation utilities, aligned with CTL document Step 2.5 (Section 4.3).
Transforms scaled initial conditions (ICs) to COM frame if not already centered.
Does not transform time-series trajectory data.
Includes verification after transformation.
Compatible with parsing.py and scaling.py outputs.
"""

import numpy as np
from typing import Optional
from pathlib import Path
from data_structures import ScaledTrajectoryData  # Import your dataclass
import copy

def transform_to_com_frame(
    scaled_traj: ScaledTrajectoryData, 
    eps: float = 1e-12,
    verbose: bool = False,
    save_transformed: bool = False,
    output_dir: Optional[str] = None
) -> ScaledTrajectoryData:
    """
    Check if scaled IC data is in COM frame; transform if not.
    Applies only to initial conditions; time-series data is left unchanged.
    Returns a new ScaledTrajectoryData with transformed ICs.
    Optionally saves transformed IC data to a new file in original format.
    """
    masses = scaled_traj.masses
    r_prime = scaled_traj.r_prime  # Scaled initial positions (3,3)
    v_prime = scaled_traj.v_prime  # Scaled initial velocities (3,3)
    M_total = np.sum(masses)
    
    # Compute initial COM position and velocity (from ICs)
    com_pos_init = np.sum(masses[:, np.newaxis] * r_prime, axis=0) / M_total
    com_vel_init = np.sum(masses[:, np.newaxis] * v_prime, axis=0) / M_total
    
    if verbose:
        print(f"Initial COM position norm: {np.linalg.norm(com_pos_init):.2e}")
        print(f"Initial COM velocity norm: {np.linalg.norm(com_vel_init):.2e}")
    
    # If already in COM, return copy
    if np.linalg.norm(com_pos_init) <= eps and np.linalg.norm(com_vel_init) <= eps:
        if verbose:
            print("IC data already in COM frame within tolerance. No transformation needed.")
        return copy.deepcopy(scaled_traj)
    
    # Transform ICs
    r_prime_transformed = r_prime - com_pos_init
    v_prime_transformed = v_prime - com_vel_init
    
    # Create new dataclass with transformed ICs (time-series unchanged)
    transformed_traj = ScaledTrajectoryData(
        metadata=scaled_traj.metadata,
        raw_data=scaled_traj.raw_data,
        masses=masses.copy(),
        r_prime=r_prime_transformed,
        v_prime=v_prime_transformed,
        times=scaled_traj.times.copy(),
        positions_scaled=scaled_traj.positions_scaled.copy(),
        velocities_scaled=scaled_traj.velocities_scaled.copy(),
        length_scale=scaled_traj.length_scale,
        velocity_scale=scaled_traj.velocity_scale,
        time_scale=scaled_traj.time_scale
    )
    
    # Verify the transformed ICs
    if not verify_com_frame(masses, transformed_traj.r_prime, transformed_traj.v_prime, eps):
        raise ValueError("Transformation failed to achieve COM frame within tolerance for ICs.")
    
    if verbose:
        print("Transformation successful. IC data now in COM frame.")
    
    # Optional: Save transformed IC data to new file
    if save_transformed and output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save transformed IC (3 lines, each: m, x,y,z, vx,vy,vz)
        ic_out_path = output_dir / f"{scaled_traj.metadata.trajectory_id}_com.txt"
        with open(ic_out_path, 'w') as f:
            for bi in range(3):
                body_data = [masses[bi], *transformed_traj.r_prime[bi], *transformed_traj.v_prime[bi]]
                f.write(' '.join(f"{x:.15g}" for x in body_data) + '\n')
    
    return transformed_traj

def verify_com_frame(m: np.ndarray, positions: np.ndarray, velocities: np.ndarray, eps: float = 1e-12) -> bool:
    """Verify COM frame for given positions (3,3) and velocities (3,3).
    Returns True if within tolerance, else False. Prints issues but does not raise.
    """
    M_total = np.sum(m)
    com_pos = np.sum(m[:, np.newaxis] * positions, axis=0) / M_total
    com_vel = np.sum(m[:, np.newaxis] * velocities, axis=0) / M_total
    
    pos_ok = np.linalg.norm(com_pos) <= eps
    vel_ok = np.linalg.norm(com_vel) <= eps
    
    if not pos_ok:
        print(f"COM position {com_pos} exceeds tolerance {eps}")
    if not vel_ok:
        print(f"COM velocity {com_vel} exceeds tolerance {eps}")
    
    return pos_ok and vel_ok
# scaling.py
"""
Scaling and normalization utilities, aligned with CTL document Step 2.
This script is responsible for computing the global dataset scales needed
before calculating invariants and constructing the PINN input vector.
"""
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
import tqdm
from data_structures import RawTrajectoryData, ScaledTrajectoryData, GlobalScales
from parsing import parse_ic_file

def _worker_compute_properties_from_ic(
    ic_path: Path, 
    T_max: float = 10.0, 
    G: float = 1.0, 
    eps: float = 1e-10
) -> Optional[Tuple[float, float]]:
    """
    Worker function for parallel processing. Parses a single IC file,
    scales the initial conditions, and computes the unnormalized energy (E)
    and characteristic radius (r_char).
    Returns a tuple of (E, r_char) or None if parsing fails.
    """
    try:
        masses, r_raw, v_raw = parse_ic_file(ic_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Warning: Could not parse {ic_path}. Skipping. Error: {e}")
        return None
    
    # Define characteristic scales for this trajectory 
    D = np.cbrt(G * T_max**2)
    V = D / T_max
    
    # Scale initial conditions to dimensionless units 
    r_prime = r_raw / D
    v_prime = v_raw / V
    
    # 1. Compute scaled total energy E 
    T = 0.5 * np.sum(masses[:, np.newaxis] * v_prime**2)
    V_pot = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            r_ij = np.linalg.norm(r_prime[i] - r_prime[j]) + eps
            V_pot -= (masses[i] * masses[j]) / r_ij
    E = T + V_pot
    
    # 2. Compute characteristic radius r_char 
    pairwise_dists = [
        np.linalg.norm(r_prime[i] - r_prime[j]) 
        for i in range(3) for j in range(i + 1, 3)
    ]
    r_char = np.mean(pairwise_dists)
    
    if not (np.isfinite(E) and np.isfinite(r_char)):
        print(f"Warning: Non-finite value computed for {ic_path}. E={E}, r_char={r_char}. Skipping.")
        return None
        
    return E, r_char

def verify_scaled_values_in_range(
    scaled_data_list: Sequence[ScaledTrajectoryData],
    tolerance: float = 1e-6
) -> bool:
    """
    Verify that all scaled values are within [-1, 1] with a small tolerance.
    This implements the critical sanity check mentioned in Section 4.2 of the document.
    
    Returns True if all values are within range, False otherwise.
    """
    all_within_range = True
    
    for i, scaled_data in enumerate(scaled_data_list):
        # Check initial positions
        if not np.all(np.abs(scaled_data.r_prime) <= 1 + tolerance):
            max_val = np.max(np.abs(scaled_data.r_prime))
            print(f"Warning [Trajectory {i}]: Scaled initial positions exceed [-1, 1] range. Max abs value: {max_val:.6f}")
            all_within_range = False
            
        # Check initial velocities
        if not np.all(np.abs(scaled_data.v_prime) <= 1 + tolerance):
            max_val = np.max(np.abs(scaled_data.v_prime))
            print(f"Warning [Trajectory {i}]: Scaled initial velocities exceed [-1, 1] range. Max abs value: {max_val:.6f}")
            all_within_range = False
            
        # Check time series positions
        if scaled_data.positions_scaled.size > 0 and not np.all(np.abs(scaled_data.positions_scaled) <= 1 + tolerance):
            max_val = np.max(np.abs(scaled_data.positions_scaled))
            print(f"Warning [Trajectory {i}]: Scaled positions exceed [-1, 1] range. Max abs value: {max_val:.6f}")
            all_within_range = False
            
        # Check time series velocities
        if scaled_data.velocities_scaled.size > 0 and not np.all(np.abs(scaled_data.velocities_scaled) <= 1 + tolerance):
            max_val = np.max(np.abs(scaled_data.velocities_scaled))
            print(f"Warning [Trajectory {i}]: Scaled velocities exceed [-1, 1] range. Max abs value: {max_val:.6f}")
            all_within_range = False
            
    if all_within_range:
        print("Verification successful: All scaled values are within [-1, 1] range.")
    else:
        print("Verification failed: Some scaled values exceed [-1, 1] range.")
        
    return all_within_range

def compute_global_scales(
    ic_paths: List[Path], 
    num_workers: Optional[int] = None,
    verbose: bool = True
) -> GlobalScales:
    """
    Computes global normalization scales across the entire dataset using parallel processing.
    This function implements Step 2 of the data preparation pipeline.
    Note: As specified in the document, only IC files are needed for this step.
    
    CRITICAL FIX: Uses 1e-10 for E_scale (not 1e-8) to match document specification.
    """
    scales = GlobalScales()
    all_E, all_r_char = [], []
    
    if verbose:
        print(f"Computing global scales from {len(ic_paths)} IC files...")
        print(f"  Characteristic Scales: D = {scales.D:.4f}, V = {scales.V:.4f}")
        print(f"  Note: Using softening parameter ε = 1e-10 for potential energy calculations")
        print(f"        and E_scale = |median(E)| + 1e-10 per document specification")
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_path = {executor.submit(_worker_compute_properties_from_ic, path): path for path in ic_paths}
        progress = tqdm.tqdm(as_completed(future_to_path), total=len(ic_paths), disable=not verbose)
        
        for future in progress:
            result = future.result()
            if result is not None:
                E, r_char = result
                all_E.append(E)
                all_r_char.append(r_char)
    
    if not all_E:
        raise ValueError("No valid trajectories were processed. Cannot compute global scales.")
    
    # CRITICAL FIX: Using 1e-10 (not 1e-8) to match document specification
    scales.E_scale = np.abs(np.median(all_E)) + 1e-10
    scales.smin_scale = np.median(all_r_char)
    
    # Store additional stats for analysis
    scales.dataset_stats = {
        'E_median': np.median(all_E),
        'E_mean': np.mean(all_E),
        'E_std': np.std(all_E),
        'E_min': np.min(all_E),
        'E_max': np.max(all_E),
        'r_char_median': np.median(all_r_char),
        'r_char_mean': np.mean(all_r_char),
        'r_char_std': np.std(all_r_char),
        'n_trajectories_processed': len(all_E)
    }
    
    if verbose:
        print("\nGlobal scales computed successfully:")
        print(f"  E_scale: {scales.E_scale:.12f} (|median(E)| + 1e-10)")
        print(f"  smin_scale: {scales.smin_scale:.6f}")
        print(f"  Q_scale (fixed): {scales.Q_scale:.2f}")
        print(f"  Processed {len(all_E)}/{len(ic_paths)} trajectories.")
        print(f"  Characteristic length D: {scales.D:.6f}")
        print(f"  Characteristic velocity V: {scales.V:.6f}")
    
    return scales

def scale_trajectory(raw_traj: RawTrajectoryData, global_scales: GlobalScales) -> ScaledTrajectoryData:
    """
    Scales a single RawTrajectoryData object to dimensionless units using pre-computed global scales.
    """
    # Scale positions and velocities using the characteristic D and V scales
    r_prime = raw_traj.r_initial / global_scales.D
    v_prime = raw_traj.v_initial / global_scales.V
    
    # Handle empty time series (for validation)
    if raw_traj.positions.size > 0:
        positions_scaled = raw_traj.positions / global_scales.D
        velocities_scaled = raw_traj.velocities / global_scales.V
    else:
        positions_scaled = np.array([])
        velocities_scaled = np.array([])
    
    return ScaledTrajectoryData(
        metadata=raw_traj.metadata,
        raw_data=raw_traj,
        masses=raw_traj.masses.copy(),
        r_prime=r_prime,
        v_prime=v_prime,
        times=raw_traj.times.copy(),
        positions_scaled=positions_scaled,
        velocities_scaled=velocities_scaled,
        length_scale=global_scales.D,
        velocity_scale=global_scales.V,
        time_scale=global_scales.T_max
    )

def scale_entire_dataset(
    raw_trajectories: List[RawTrajectoryData],
    ic_paths: Optional[List[Path]] = None,
    num_workers: Optional[int] = None,
    verbose: bool = True
) -> Tuple[GlobalScales, List[ScaledTrajectoryData]]:
    """
    Complete workflow for scaling the entire dataset:
    1. Compute global scales from IC files
    2. Scale all trajectories using the global scales
    3. Verify scaled values are in [-1, 1] range
    
    If raw_trajectories already contain parsed data, ic_paths is optional.
    If only IC paths are available (before full parsing), provide ic_paths.
    """
    # If ic_paths not provided, extract from raw trajectories
    if ic_paths is None:
        ic_paths = [traj.metadata.ic_file for traj in raw_trajectories]
    
    # Step 1: Compute global scales
    global_scales = compute_global_scales(ic_paths, num_workers, verbose)
    
    # Step 2: Scale all trajectories
    if verbose:
        print("\nScaling individual trajectories...")
    
    scaled_trajectories = []
    for raw_traj in tqdm.tqdm(raw_trajectories, disable=not verbose):
        scaled_traj = scale_trajectory(raw_traj, global_scales)
        scaled_trajectories.append(scaled_traj)
    
    # Step 3: Verify scaled values are in [-1, 1]
    if verbose:
        print("\nVerifying scaled values are within [-1, 1] range...")
    
    verification_result = verify_scaled_values_in_range(scaled_trajectories)
    
    if not verification_result and verbose:
        print("\nWARNING: Some scaled values exceed [-1, 1] range. This may affect training performance.")
        print("Consider reviewing the scaling parameters or dataset characteristics.")
    
    return global_scales, scaled_trajectories

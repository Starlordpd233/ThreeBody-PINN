# com_transform_brutus.py
"""
Standalone script to transform Brutus time-series trajectory files to COM frame.
Transforms positions and velocities at each time snapshot independently to ensure COM centering.
Handles potential numerical drifts by recomputing COM per snapshot.
Input: Path to Brutus file (txt format with repetitive blocks: header + 3 body lines).
Output: Transformed Brutus file in the same format.
"""

import numpy as np
from pathlib import Path
from typing import Tuple, List

def parse_brutus_file(input_path: str) -> Tuple[np.ndarray, List[float], np.ndarray, np.ndarray, np.ndarray]:
    """
    Parse Brutus file into times, cpu_times, masses (constant), positions (T,3,3), velocities (T,3,3).
    Assumes N=3 and constant masses across time steps.
    """
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    i = 0
    times = []
    cpu_times = []
    positions = []
    velocities = []
    masses = None
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        header = list(map(float, line.split()))
        t = header[0]
        N = int(header[1])
        t_cpu = header[2] if len(header) > 2 else 0.0  # Fallback if no t_cpu
        times.append(t)
        cpu_times.append(t_cpu)
        
        pos_t = []
        vel_t = []
        mass_t = []
        for _ in range(N):
            i += 1
            body_line = lines[i].strip()
            body = list(map(float, body_line.split()))
            mass_t.append(body[0])
            pos_t.append(body[1:4])
            vel_t.append(body[4:7])
        
        if masses is None:
            masses = np.array(mass_t)
        else:
            # Check consistency
            if not np.allclose(masses, mass_t):
                raise ValueError("Masses are not constant across time steps.")
        
        positions.append(np.array(pos_t))
        velocities.append(np.array(vel_t))
        i += 1
    
    return np.array(times), cpu_times, masses, np.array(positions), np.array(velocities)

def transform_brutus_to_com(
    times: np.ndarray,
    cpu_times: List[float],
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    eps: float = 1e-12,
    verbose: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Transform positions and velocities to COM frame per snapshot.
    Returns transformed positions and velocities.
    """
    M_total = np.sum(masses)
    T = len(times)
    positions_transformed = np.zeros_like(positions)
    velocities_transformed = np.zeros_like(velocities)
    
    for t in range(T):
        # Compute COM at this snapshot
        com_pos = np.sum(masses[:, np.newaxis] * positions[t], axis=0) / M_total
        com_vel = np.sum(masses[:, np.newaxis] * velocities[t], axis=0) / M_total
        
        # Transform
        positions_transformed[t] = positions[t] - com_pos
        velocities_transformed[t] = velocities[t] - com_vel
        
        # Optional verification
        if verbose:
            com_pos_new = np.sum(masses[:, np.newaxis] * positions_transformed[t], axis=0) / M_total
            com_vel_new = np.sum(masses[:, np.newaxis] * velocities_transformed[t], axis=0) / M_total
            if np.linalg.norm(com_pos_new) > eps or np.linalg.norm(com_vel_new) > eps:
                print(f"Warning: Snapshot at t={times[t]} not perfectly transformed (norm pos: {np.linalg.norm(com_pos_new):.2e}, vel: {np.linalg.norm(com_vel_new):.2e})")
    
    if verbose:
        print("Transformation completed for all snapshots.")
    
    return positions_transformed, velocities_transformed

def save_transformed_brutus(
    output_path: str,
    times: np.ndarray,
    cpu_times: List[float],
    masses: np.ndarray,
    positions_transformed: np.ndarray,
    velocities_transformed: np.ndarray
):
    """
    Save transformed data back to Brutus format.
    """
    T = len(times)
    with open(output_path, 'w') as f:
        for t in range(T):
            f.write(f"{times[t]} 3 {cpu_times[t]}\n")
            for bi in range(3):
                body_data = [masses[bi]] + list(positions_transformed[t, bi]) + list(velocities_transformed[t, bi])
                f.write(' '.join(f"{x:.15g}" for x in body_data) + '\n')

def main(input_path: str, output_path: str, eps: float = 1e-12, verbose: bool = True):
    """
    Main function to transform a Brutus file to COM frame.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    times, cpu_times, masses, positions, velocities = parse_brutus_file(input_path)
    
    if verbose:
        print(f"Parsed {len(times)} time steps from {input_path}.")
    
    positions_transformed, velocities_transformed = transform_brutus_to_com(
        times, cpu_times, masses, positions, velocities, eps, verbose
    )
    
    save_transformed_brutus(output_path, times, cpu_times, masses, positions_transformed, velocities_transformed)
    
    if verbose:
        print(f"Transformed file saved to {output_path}.")

# Example usage (comment out or replace with actual paths)
# main('brutus_hierarchical_0084.txt', 'brutus_hierarchical_0084_com.txt')
"""
Main preprocessing script that parses raw files and saves in reusable format.
This should be run once on your dataset.
"""

import numpy as np
import argparse
from pathlib import Path
import pickle
import h5py
from typing import List, Dict
import json
from tqdm import tqdm

# Import all necessary modules
from ..core.data_structures import *
from ..core.parsing import parse_trajectory_pair
from ..core.scaling import compute_global_scales, scale_trajectory, verify_com_frame
from ..processing.invariants import compute_all_invariants
from ..processing.stage_assignment import assign_stages_to_dataset
from ..processing.input_vector import formulate_ic_vector


def save_dataset_hdf5(trajectories: List[ProcessedTrajectory], 
                     global_scales: GlobalScales,
                     output_path: Path):
    """Save processed dataset in HDF5 format."""
    with h5py.File(output_path, 'w') as f:
        # Save global scales
        scales_group = f.create_group('global_scales')
        scales_group.attrs['T_max'] = global_scales.T_max
        scales_group.attrs['G'] = global_scales.G
        scales_group.attrs['D'] = global_scales.D
        scales_group.attrs['V'] = global_scales.V
        scales_group.attrs['E_scale'] = global_scales.E_scale
        scales_group.attrs['smin_scale'] = global_scales.smin_scale
        scales_group.attrs['Q_scale'] = global_scales.Q_scale
        
        # Save dataset statistics
        stats_group = f.create_group('dataset_stats')
        for key, value in global_scales.dataset_stats.items():
            stats_group.attrs[key] = value
        
        # Save trajectories
        traj_group = f.create_group('trajectories')
        
        for i, traj in enumerate(trajectories):
            traj_id = traj.metadata.trajectory_id
            g = traj_group.create_group(traj_id)
            
            # Metadata
            meta = g.create_group('metadata')
            meta.attrs['trajectory_id'] = traj_id
            meta.attrs['dataset_type'] = traj.metadata.dataset_type
            meta.attrs['fidelity'] = traj.metadata.fidelity
            meta.attrs['dt_out'] = traj.metadata.dt_out
            meta.attrs['set_name'] = traj.metadata.set_name
            meta.attrs['ic_file'] = str(traj.metadata.ic_file)
            meta.attrs['brutus_file'] = str(traj.metadata.brutus_file)
            
            # Raw data
            raw = g.create_group('raw')
            raw.create_dataset('masses', data=traj.scaled_data.raw_data.masses)
            raw.create_dataset('r_initial', data=traj.scaled_data.raw_data.r_initial)
            raw.create_dataset('v_initial', data=traj.scaled_data.raw_data.v_initial)
            raw.create_dataset('times', data=traj.scaled_data.raw_data.times)
            raw.create_dataset('positions', data=traj.scaled_data.raw_data.positions)
            raw.create_dataset('velocities', data=traj.scaled_data.raw_data.velocities)
            
            # Scaled data
            scaled = g.create_group('scaled')
            scaled.create_dataset('r_prime', data=traj.scaled_data.r_prime)
            scaled.create_dataset('v_prime', data=traj.scaled_data.v_prime)
            scaled.create_dataset('positions_scaled', data=traj.scaled_data.positions_scaled)
            scaled.create_dataset('velocities_scaled', data=traj.scaled_data.velocities_scaled)
            
            # Invariants
            inv = g.create_group('invariants')
            inv.attrs['E'] = traj.invariants.E
            inv.attrs['Q'] = traj.invariants.Q
            inv.attrs['s_min'] = traj.invariants.s_min
            inv.attrs['L_norm'] = traj.invariants.L_norm
            inv.attrs['I_norm'] = traj.invariants.I_norm
            inv.attrs['tau_L'] = traj.invariants.tau_L
            inv.attrs['L_max'] = traj.invariants.L_max
            inv.attrs['r_char'] = traj.invariants.r_char
            inv.attrs['v_char'] = traj.invariants.v_char
            
            # Stage assignment
            g.attrs['stage'] = traj.stage if traj.stage is not None else -1
            
            # IC vector
            if traj.ic_vector is not None:
                g.create_dataset('ic_vector', data=traj.ic_vector)


def main():
    parser = argparse.ArgumentParser(description='Preprocess CTL-PINN dataset')
    parser.add_argument('--ic_dir', type=Path, required=True,
                       help='Directory containing IC files')
    parser.add_argument('--brutus_dir', type=Path, required=True,
                       help='Directory containing BRUTUS files')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output HDF5 file')
    parser.add_argument('--max_trajectories', type=int, default=None,
                       help='Maximum number of trajectories to process')
    parser.add_argument('--verify_com', action='store_true',
                       help='Verify center-of-mass frame')
    parser.add_argument('--compute_ic_vectors', action='store_true',
                       help='Compute IC vectors for all trajectories')
    
    args = parser.parse_args()
    
    # Find all IC files
    ic_files = sorted(args.ic_dir.glob('ic_*.txt'))
    if args.max_trajectories:
        ic_files = ic_files[:args.max_trajectories]
    
    print(f"Found {len(ic_files)} IC files")
    
    # Parse all trajectories
    print("Parsing trajectories...")
    raw_trajectories = []
    
    for ic_file in tqdm(ic_files):
        # Find corresponding BRUTUS file
        brutus_name = ic_file.name.replace('ic_', 'brutus_')
        brutus_file = args.brutus_dir / brutus_name
        
        if not brutus_file.exists():
            print(f"Warning: No BRUTUS file for {ic_file.name}")
            continue
        
        try:
            raw_traj = parse_trajectory_pair(ic_file, brutus_file)
            
            # Verify COM frame if requested
            if args.verify_com:
                is_com = verify_com_frame(
                    raw_traj.masses, 
                    raw_traj.r_initial, 
                    raw_traj.v_initial
                )
                if not is_com:
                    print(f"Warning: {ic_file.name} not in COM frame")
            
            raw_trajectories.append(raw_traj)
        
        except Exception as e:
            print(f"Error processing {ic_file.name}: {e}")
            continue
    
    print(f"Successfully parsed {len(raw_trajectories)} trajectories")
    
    # Compute global scales
    print("\nComputing global scales...")
    global_scales = compute_global_scales(raw_trajectories)
    
    # Process all trajectories
    print("\nProcessing trajectories...")
    processed_trajectories = []
    
    for raw_traj in tqdm(raw_trajectories):
        # Scale trajectory
        scaled_traj = scale_trajectory(raw_traj, global_scales)
        
        # Compute invariants
        invariants = compute_all_invariants(scaled_traj)
        
        # Create processed trajectory
        proc_traj = ProcessedTrajectory(
            metadata=raw_traj.metadata,
            scaled_data=scaled_traj,
            invariants=invariants
        )
        
        # Compute IC vector if requested
        if args.compute_ic_vectors:
            ic_vector, ordering = formulate_ic_vector(
                scaled_traj, invariants, global_scales
            )
            proc_traj.ic_vector = ic_vector
            proc_traj.canonical_ordering = ordering
        
        processed_trajectories.append(proc_traj)
    
    # Assign stages
    print("\nAssigning curriculum stages...")
    assign_stages_to_dataset(processed_trajectories)
    
    # Save dataset
    print(f"\nSaving to {args.output}...")
    save_dataset_hdf5(processed_trajectories, global_scales, args.output)
    
    print("Done!")


if __name__ == '__main__':
    main()
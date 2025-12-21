"""
Script to prepare final training data for PINN from preprocessed HDF5 file.
This creates the actual training batches organized by curriculum stage.
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import pickle
from tqdm import tqdm
import json


def load_stage_data(hdf5_path: Path, stage: int, 
                   include_previous: bool = True) -> Dict:
    """
    Load training data for a specific curriculum stage.
    
    Args:
        hdf5_path: Path to preprocessed HDF5 file
        stage: Current curriculum stage
        include_previous: Whether to include all previous stages (replay)
    
    Returns:
        Dictionary with training data
    """
    training_data = {
        'ic_vectors': [],
        'times': [],
        'positions': [],
        'velocities': [],
        'metadata': [],
        'invariants': []
    }
    
    with h5py.File(hdf5_path, 'r') as f:
        # Get trajectories for this stage
        for traj_id in f['trajectories']:
            traj = f['trajectories'][traj_id]
            traj_stage = traj.attrs.get('stage', -1)
            
            # Include if in current stage or previous stages (if replay enabled)
            if traj_stage == stage or (include_previous and traj_stage < stage and traj_stage >= 0):
                # Load IC vector
                if 'ic_vector' in traj:
                    ic_vector = traj['ic_vector'][:]
                else:
                    continue  # Skip if no IC vector
                
                # Load trajectory data
                times = traj['raw/times'][:]
                positions = traj['scaled/positions_scaled'][:]
                velocities = traj['scaled/velocities_scaled'][:]
                
                # Store data
                training_data['ic_vectors'].append(ic_vector)
                training_data['times'].append(times)
                training_data['positions'].append(positions)
                training_data['velocities'].append(velocities)
                
                # Store metadata
                meta = {
                    'trajectory_id': traj.attrs['trajectory_id'],
                    'stage': traj_stage,
                    'dataset_type': traj['metadata'].attrs['dataset_type'],
                    'fidelity': traj['metadata'].attrs['fidelity']
                }
                training_data['metadata'].append(meta)
                
                # Store invariants
                inv = {k: v for k, v in traj['invariants'].attrs.items()}
                training_data['invariants'].append(inv)
    
    # Convert lists to arrays where appropriate
    training_data['ic_vectors'] = np.array(training_data['ic_vectors'])
    
    return training_data


def create_training_batches(training_data: Dict, 
                           batch_size: int = 256,
                           points_per_trajectory: int = 32,
                           time_sampling: str = 'mixed') -> List[Dict]:
    """
    Create training batches from stage data.
    
    Args:
        training_data: Dictionary with training data
        batch_size: Number of trajectory samples per batch
        points_per_trajectory: Number of time points per trajectory
        time_sampling: 'uniform', 'acceleration', or 'mixed'
    
    Returns:
        List of batch dictionaries
    """
    batches = []
    n_trajectories = len(training_data['ic_vectors'])
    
    # For each trajectory, create multiple samples
    all_samples = []
    
    for i in range(n_trajectories):
        ic_vector = training_data['ic_vectors'][i]
        times = training_data['times'][i]
        positions = training_data['positions'][i]
        velocities = training_data['velocities'][i]
        
        # Sample time points
        n_times = len(times)
        if n_times < points_per_trajectory:
            # Use all available points
            time_indices = np.arange(n_times)
        else:
            if time_sampling == 'uniform':
                time_indices = np.linspace(0, n_times-1, points_per_trajectory, dtype=int)
            elif time_sampling == 'acceleration':
                # Compute acceleration magnitudes
                if n_times > 1:
                    accel = np.diff(velocities, axis=0) / np.diff(times)[:, None, None]
                    accel_mag = np.sum(np.linalg.norm(accel, axis=2), axis=1)
                    # Sample proportional to acceleration
                    probs = accel_mag / (np.sum(accel_mag) + 1e-10)
                    time_indices = np.random.choice(n_times-1, size=points_per_trajectory, p=probs)
                else:
                    time_indices = np.zeros(points_per_trajectory, dtype=int)
            else:  # mixed
                # 50% uniform, 50% acceleration-weighted
                n_uniform = points_per_trajectory // 2
                n_accel = points_per_trajectory - n_uniform
                
                uniform_indices = np.linspace(0, n_times-1, n_uniform, dtype=int)
                
                if n_times > 1:
                    accel = np.diff(velocities, axis=0) / np.diff(times)[:, None, None]
                    accel_mag = np.sum(np.linalg.norm(accel, axis=2), axis=1)
                    probs = accel_mag / (np.sum(accel_mag) + 1e-10)
                    accel_indices = np.random.choice(n_times-1, size=n_accel, p=probs)
                else:
                    accel_indices = np.zeros(n_accel, dtype=int)
                
                time_indices = np.concatenate([uniform_indices, accel_indices])
        
        # Create samples for this trajectory
        for idx in time_indices:
            sample = {
                'ic_vector': ic_vector,
                't': times[idx],
                'positions': positions[idx],
                'velocities': velocities[idx],
                'trajectory_idx': i,
                'time_idx': idx
            }
            all_samples.append(sample)
    
    # Shuffle samples
    np.random.shuffle(all_samples)
    
    # Create batches
    for i in range(0, len(all_samples), batch_size):
        batch_samples = all_samples[i:i+batch_size]
        
        batch = {
            'ic_vectors': np.array([s['ic_vector'] for s in batch_samples]),
            'times': np.array([s['t'] for s in batch_samples]),
            'positions': np.array([s['positions'] for s in batch_samples]),
            'velocities': np.array([s['velocities'] for s in batch_samples]),
            'trajectory_indices': np.array([s['trajectory_idx'] for s in batch_samples]),
            'time_indices': np.array([s['time_idx'] for s in batch_samples])
        }
        
        batches.append(batch)
    
    return batches


def save_stage_training_data(stage: int, training_data: Dict, 
                           batches: List[Dict], output_dir: Path):
    """Save training data for a stage."""
    stage_dir = output_dir / f'stage_{stage}'
    stage_dir.mkdir(exist_ok=True, parents=True)
    
    # Save raw training data
    np.savez(
        stage_dir / 'training_data.npz',
        ic_vectors=training_data['ic_vectors'],
        metadata=training_data['metadata'],
        invariants=training_data['invariants']
    )
    
    # Save batches
    with open(stage_dir / 'batches.pkl', 'wb') as f:
        pickle.dump(batches, f)
    
    # Save summary
    summary = {
        'n_trajectories': len(training_data['ic_vectors']),
        'n_batches': len(batches),
        'n_samples': sum(len(b['times']) for b in batches)
    }
    
    with open(stage_dir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Prepare CTL-PINN training data')
    parser.add_argument('--input', type=Path, required=True,
                       help='Input preprocessed HDF5 file')
    parser.add_argument('--output_dir', type=Path, required=True,
                       help='Output directory for training data')
    parser.add_argument('--stages', type=int, nargs='+', default=[0, 1, 2, 3, 4, 5, 6],
                       help='Stages to prepare')
    parser.add_argument('--batch_size', type=int, default=256,
                       help='Batch size')
    parser.add_argument('--points_per_trajectory', type=int, default=32,
                       help='Time points per trajectory')
    parser.add_argument('--no_replay', action='store_true',
                       help='Disable curriculum replay')
    
    args = parser.parse_args()
    
    args.output_dir.mkdir(exist_ok=True, parents=True)
    
    # Process each stage
    for stage in args.stages:
        print(f"\nPreparing Stage {stage}...")
        
        # Load data
        training_data = load_stage_data(
            args.input, stage, 
            include_previous=not args.no_replay
        )
        
        if len(training_data['ic_vectors']) == 0:
            print(f"No data for stage {stage}, skipping...")
            continue
        
        print(f"Loaded {len(training_data['ic_vectors'])} trajectories")
        
        # Create batches
        batches = create_training_batches(
            training_data,
            batch_size=args.batch_size,
            points_per_trajectory=args.points_per_trajectory,
            time_sampling='mixed'
        )
        
        print(f"Created {len(batches)} batches")
        
        # Save
        save_stage_training_data(stage, training_data, batches, args.output_dir)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
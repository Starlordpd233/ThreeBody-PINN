#!/usr/bin/env python3
"""
Stage 2: Pre-screening for Short-Term Stability (with REVISED thresholds)
Based on analysis of actual IC distributions.
AUTOMATED VERSION: Processes both standard and hierarchical datasets automatically.
"""

import numpy as np
import os
import glob
from numba import jit
import time
from typing import Tuple, Dict, List
import json
import hashlib
from datetime import datetime

# REVISED Pre-screening parameters based on data analysis
TMAX = 1.0  # Integration time
DT = 0.0001  # Time step for Leapfrog
ENERGY_ERROR_THRESHOLD = 0.01  # 1% relative energy error
MIN_DISTANCE_THRESHOLD = 0.01  # Minimum separation during integration

# REVISED THRESHOLDS - Much more appropriate for cold systems
VIRIAL_RATIO_MIN = 0.001  # Was 0.7 - now accepts cold systems
VIRIAL_RATIO_MAX = 2.0    # Was 1.5 - slightly wider upper bound
MIN_ANGULAR_MOMENTUM = 0.0  # Was 0.1 - now no minimum (can filter later if needed)

# Optional: Use percentile-based thresholds for adaptive filtering
USE_PERCENTILE_THRESHOLDS = True
VIRIAL_PERCENTILE_MIN = 1   # Keep top 99% of systems (was 5)
VIRIAL_PERCENTILE_MAX = 99.5  # Remove top 0.5% outliers (was 99)
ANGULAR_PERCENTILE_MIN = 0  # No angular momentum filtering for now

# Constants
G = 1.0  # Gravitational constant (natural units)

# IC_RAW_DIR environment variable for external ic_raw directory
IC_RAW_DIR = os.environ.get('IC_RAW_DIR')
if IC_RAW_DIR is None:
    raise RuntimeError(
        "IC_RAW_DIR environment variable not set. "
        "Export the path to your ic_raw directory: "
        "export IC_RAW_DIR=/path/to/ic_raw"
    )

# Dataset configurations
DATASET_CONFIGS = [
    {
        'name': 'ic_hierarchical',
        'input_dir': os.path.join(IC_RAW_DIR, 'ic_hierarchical'),
        'output_dir': "<home>/Desktop/3_body_problem/simulation_data/Data/ic_final/ic_hierarchical",
    },
    {
        'name': 'ic_standard_quasi_random',
        'input_dir': os.path.join(IC_RAW_DIR, 'ic_standard_quasi_random'),
        'output_dir': "<home>/Desktop/3_body_problem/simulation_data/Data/ic_final/ic_standard_quasi_random",
    }
]


@jit(nopython=True)
def compute_forces(positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """Compute gravitational forces between all bodies."""
    n_bodies = len(masses)
    forces = np.zeros_like(positions)
    
    for i in range(n_bodies):
        for j in range(i + 1, n_bodies):
            dr = positions[j] - positions[i]
            r = np.sqrt(np.sum(dr**2))
            r3 = r**3
            
            # Force on body i due to body j
            F_ij = G * masses[i] * masses[j] * dr / r3
            forces[i] += F_ij
            forces[j] -= F_ij  # Newton's third law
    
    return forces


@jit(nopython=True)
def compute_kinetic_energy(velocities: np.ndarray, masses: np.ndarray) -> float:
    """Compute total kinetic energy."""
    return 0.5 * np.sum(masses[:, np.newaxis] * velocities**2)


@jit(nopython=True)
def compute_potential_energy(positions: np.ndarray, masses: np.ndarray) -> float:
    """Compute total gravitational potential energy."""
    n_bodies = len(masses)
    U = 0.0
    
    for i in range(n_bodies):
        for j in range(i + 1, n_bodies):
            dr = positions[j] - positions[i]
            r = np.sqrt(np.sum(dr**2))
            U -= G * masses[i] * masses[j] / r
    
    return U


@jit(nopython=True)
def compute_angular_momentum(positions: np.ndarray, velocities: np.ndarray, 
                            masses: np.ndarray) -> float:
    """Compute magnitude of total angular momentum."""
    L_total = np.zeros(3)
    
    for i in range(len(masses)):
        L_i = masses[i] * np.cross(positions[i], velocities[i])
        L_total += L_i
    
    return np.sqrt(np.sum(L_total**2))


@jit(nopython=True)
def compute_min_separation(positions: np.ndarray) -> float:
    """Compute minimum pairwise separation."""
    n_bodies = len(positions)
    min_sep = np.inf
    
    for i in range(n_bodies):
        for j in range(i + 1, n_bodies):
            dr = positions[j] - positions[i]
            r = np.sqrt(np.sum(dr**2))
            if r < min_sep:
                min_sep = r
    
    return min_sep


@jit(nopython=True)
def leapfrog_step(positions: np.ndarray, velocities: np.ndarray, 
                  masses: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    """Single step of Leapfrog integrator."""
    # Kick: v(t + dt/2) = v(t) + a(t) * dt/2
    forces = compute_forces(positions, masses)
    accelerations = forces / masses[:, np.newaxis]
    velocities_half = velocities + 0.5 * dt * accelerations
    
    # Drift: x(t + dt) = x(t) + v(t + dt/2) * dt
    new_positions = positions + dt * velocities_half
    
    # Kick: v(t + dt) = v(t + dt/2) + a(t + dt) * dt/2
    new_forces = compute_forces(new_positions, masses)
    new_accelerations = new_forces / masses[:, np.newaxis]
    new_velocities = velocities_half + 0.5 * dt * new_accelerations
    
    return new_positions, new_velocities


@jit(nopython=True)
def integrate_and_check(positions: np.ndarray, velocities: np.ndarray, 
                       masses: np.ndarray, tmax: float, dt: float) -> Tuple[bool, int, float, float, float]:
    """
    Integrate system using Leapfrog and check stability criteria.
    
    Returns:
        Tuple of (passed, failure_reason, max_energy_error, min_separation, integration_time)
        where failure_reason is:
            0: passed
            1: min_separation failure
            2: energy_conservation failure
    """
    # Initial calculations
    E_init = compute_kinetic_energy(velocities, masses) + compute_potential_energy(positions, masses)
    min_sep_overall = compute_min_separation(positions)
    
    # Integration loop
    t = 0.0
    n_steps = int(tmax / dt)
    max_energy_error = 0.0
    
    pos = positions.copy()
    vel = velocities.copy()
    
    for step in range(n_steps):
        # Check minimum separation
        min_sep = compute_min_separation(pos)
        if min_sep < MIN_DISTANCE_THRESHOLD:
            return False, 1, max_energy_error, min_sep, t
        
        if min_sep < min_sep_overall:
            min_sep_overall = min_sep
        
        # Integrate
        pos, vel = leapfrog_step(pos, vel, masses, dt)
        t += dt
        
        # Check energy conservation periodically
        if step % 100 == 0:  # Check every 100 steps
            E_current = compute_kinetic_energy(vel, masses) + compute_potential_energy(pos, masses)
            energy_error = abs((E_current - E_init) / E_init)
            if energy_error > max_energy_error:
                max_energy_error = energy_error
            
            if energy_error > ENERGY_ERROR_THRESHOLD:
                return False, 2, energy_error, min_sep_overall, t
    
    return True, 0, max_energy_error, min_sep_overall, tmax


def compute_adaptive_thresholds(sample_files: List[str]) -> Dict[str, float]:
    """
    Compute adaptive thresholds based on a representative sample of files.
    Sample size = min(1000, max(200, int(0.05 * total_files))) for statistical robustness.
    """
    if not sample_files:
        return None
    
    # Calculate dynamic sample size: 5% of dataset (min 200, max 1000)
    sample_size = min(1000, max(200, int(0.05 * len(sample_files))))
    sampled = np.random.choice(sample_files, size=sample_size, replace=False)
    
    print(f"  Sampling {len(sampled)}/{len(sample_files)} files for adaptive thresholds")
    
    virial_ratios = []
    angular_momenta = []
    
    for filepath in sampled:
        try:
            positions, velocities, masses = load_ic_file(filepath)
            T = compute_kinetic_energy(velocities, masses)
            U = compute_potential_energy(positions, masses)
            virial_ratio = 2 * T / abs(U)
            L_mag = compute_angular_momentum(positions, velocities, masses)
            
            virial_ratios.append(virial_ratio)
            angular_momenta.append(L_mag)
        except Exception as e:
            print(f"    Error processing {os.path.basename(filepath)}: {str(e)}")
    
    if not virial_ratios:
        print("  WARNING: No valid samples for thresholds!")
        return None
    
    # Compute percentile-based thresholds
    thresholds = {
        'virial_min': np.percentile(virial_ratios, VIRIAL_PERCENTILE_MIN),
        'virial_max': np.percentile(virial_ratios, VIRIAL_PERCENTILE_MAX),
        'angular_min': np.percentile(angular_momenta, ANGULAR_PERCENTILE_MIN) 
                      if ANGULAR_PERCENTILE_MIN > 0 else 0.0
    }
    
    print(f"  Adaptive thresholds computed:")
    print(f"    Virial ratio: {thresholds['virial_min']:.6f} to {thresholds['virial_max']:.6f}")
    if ANGULAR_PERCENTILE_MIN > 0:
        print(f"    Angular momentum min: {thresholds['angular_min']:.6f}")
    
    return thresholds

'''
Old one without adaptive thresholds computation:
def compute_adaptive_thresholds(sample_files: List[str], n_samples: int = 100) -> Dict[str, float]:
    """
    Compute adaptive thresholds based on a sample of files.
    This allows the thresholds to adapt to the actual distribution of ICs.
    """
    virial_ratios = []
    angular_momenta = []
    
    # Sample a subset of files
    sample_size = min(n_samples, len(sample_files))
    sampled = np.random.choice(sample_files, size=sample_size, replace=False)
    
    for filepath in sampled:
        try:
            positions, velocities, masses = load_ic_file(filepath)
            T = compute_kinetic_energy(velocities, masses)
            U = compute_potential_energy(positions, masses)
            virial_ratio = 2 * T / abs(U)
            L_mag = compute_angular_momentum(positions, velocities, masses)
            
            virial_ratios.append(virial_ratio)
            angular_momenta.append(L_mag)
        except:
            pass
    
    if not virial_ratios:
        return None
    
    # Compute percentile-based thresholds
    virial_ratios = np.array(virial_ratios)
    angular_momenta = np.array(angular_momenta)
    
    thresholds = {
        'virial_min': np.percentile(virial_ratios, VIRIAL_PERCENTILE_MIN),
        'virial_max': np.percentile(virial_ratios, VIRIAL_PERCENTILE_MAX),
        'angular_min': np.percentile(angular_momenta, ANGULAR_PERCENTILE_MIN) if ANGULAR_PERCENTILE_MIN > 0 else 0.0
    }
    
    return thresholds
'''

def check_static_criteria(positions: np.ndarray, velocities: np.ndarray, 
                         masses: np.ndarray, thresholds: Dict[str, float] = None) -> Tuple[bool, Dict[str, float]]:
    """Check virial ratio and angular momentum criteria."""
    T = compute_kinetic_energy(velocities, masses)
    U = compute_potential_energy(positions, masses)
    virial_ratio = 2 * T / abs(U)
    
    L_mag = compute_angular_momentum(positions, velocities, masses)
    
    # Use adaptive or fixed thresholds
    if thresholds:
        virial_min = thresholds['virial_min']
        virial_max = thresholds['virial_max']
        angular_min = thresholds['angular_min']
    else:
        virial_min = VIRIAL_RATIO_MIN
        virial_max = VIRIAL_RATIO_MAX
        angular_min = MIN_ANGULAR_MOMENTUM
    
    passed = (virial_min <= virial_ratio <= virial_max and 
              L_mag >= angular_min)
    
    return passed, {
        'virial_ratio': virial_ratio,
        'angular_momentum': L_mag,
        'kinetic_energy': T,
        'potential_energy': U
    }


def load_ic_file(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load initial conditions from file."""
    data = np.loadtxt(filepath)
    
    # Assuming format: mass x y z vx vy vz (for each body)
    n_bodies = len(data)
    masses = data[:, 0]
    positions = data[:, 1:4]
    velocities = data[:, 4:7]
    
    return positions, velocities, masses


def compute_file_hash(filepath: str) -> str:
    """Compute SHA256 hash of file content for tracking."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def load_processing_index(index_file: str) -> Dict:
    """Load the processing index from file."""
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            return json.load(f)
    return {
        'processed_files': {},
        'processing_runs': []
    }


def save_processing_index(index_file: str, index_data: Dict):
    """Save the processing index to file."""
    with open(index_file, 'w') as f:
        json.dump(index_data, f, indent=2)


def prescreen_ic(filepath: str, thresholds: Dict[str, float] = None) -> Tuple[bool, Dict]:
    """
    Pre-screen a single initial condition file.
    Returns (passed, results_dict).
    """
    try:
        positions, velocities, masses = load_ic_file(filepath)
        
        # Check static criteria first (cheap)
        static_passed, static_metrics = check_static_criteria(positions, velocities, masses, thresholds)
        if not static_passed:
            return False, {
                'filename': os.path.basename(filepath),
                'passed': False,
                'stage': 'static_check',
                **static_metrics
            }
        
        # Run dynamic integration check
        passed, failure_reason, max_energy_error, min_separation, integration_time = integrate_and_check(
            positions, velocities, masses, TMAX, DT
        )
        
        # Convert failure_reason integer to string
        reason_map = {
            0: 'passed',
            1: 'min_separation',
            2: 'energy_conservation'
        }
        
        results = {
            'filename': os.path.basename(filepath),
            'passed': passed,
            'stage': 'dynamic_check' if passed else 'dynamic_failed',
            'reason': reason_map.get(failure_reason, 'unknown'),
            'max_energy_error': max_energy_error,
            'min_separation': min_separation,
            'integration_time': integration_time,
            **static_metrics
        }
        
        return passed, results
        
    except Exception as e:
        return False, {
            'filename': os.path.basename(filepath),
            'passed': False,
            'stage': 'error',
            'error': str(e)
        }


def process_dataset(config: Dict, run_id: str) -> Dict:
    """Process a single dataset configuration."""
    dataset_name = config['name']
    input_dir = config['input_dir']
    output_dir = config['output_dir']
    
    print(f"\n{'='*60}")
    print(f"Processing dataset: {dataset_name}")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load processing index for this dataset
    index_file = os.path.join("<home>/Desktop/3_body_problem/simulation_data/Validation/prescreening",
                              f"processing_index_{dataset_name}.json")
    index_data = load_processing_index(index_file)
    
    # Find all IC files
    ic_files = glob.glob(os.path.join(input_dir, "*.txt"))
    if not ic_files:
        ic_files = glob.glob(os.path.join(input_dir, "*.dat"))
    
    print(f"Found {len(ic_files)} total files in input directory")
    
    if not ic_files:
        print(f"No files found in {input_dir}, skipping this dataset")
        return {
            'dataset_name': dataset_name,
            'files_processed': 0,
            'files_passed': 0,
            'files_failed': 0,
            'skipped': True
        }
    
    # Compute adaptive thresholds if enabled
    adaptive_thresholds = None
    if USE_PERCENTILE_THRESHOLDS:
        print("\nComputing adaptive thresholds from data distribution...")
        adaptive_thresholds = compute_adaptive_thresholds(ic_files)
        if adaptive_thresholds:
            print(f"  Virial ratio: {adaptive_thresholds['virial_min']:.4f} < Q < {adaptive_thresholds['virial_max']:.4f}")
            print(f"  Angular momentum: L > {adaptive_thresholds['angular_min']:.4f}")
        else:
            print("  Failed to compute adaptive thresholds, using fixed values")
    
    # Filter out already processed files
    new_files = []
    skipped_files = []
    
    for filepath in ic_files:
        filename = os.path.basename(filepath)
        file_hash = compute_file_hash(filepath)
        
        # Check if file was already processed
        if filename in index_data['processed_files']:
            prev_hash = index_data['processed_files'][filename].get('hash')
            if prev_hash == file_hash:
                skipped_files.append(filename)
                continue
            else:
                print(f"File {filename} has changed since last run, reprocessing...")
        
        new_files.append(filepath)
    
    print(f"Skipping {len(skipped_files)} already processed files")
    print(f"Processing {len(new_files)} new/modified files")
    
    if not new_files:
        print("No new files to process for this dataset!")
        return {
            'dataset_name': dataset_name,
            'files_processed': 0,
            'files_passed': 0,
            'files_failed': 0,
            'skipped_files': len(skipped_files)
        }
    
    # Process each new file
    passed_files = []
    failed_files = []
    all_results = []
    
    start_time = time.time()
    
    for i, filepath in enumerate(new_files):
        if (i + 1) % 100 == 0:
            print(f"Processing file {i + 1}/{len(new_files)}...")
        
        filename = os.path.basename(filepath)
        file_hash = compute_file_hash(filepath)
        
        passed, results = prescreen_ic(filepath, adaptive_thresholds)
        results['dataset'] = dataset_name  # Add dataset info to results
        all_results.append(results)
        
        # Update index
        index_data['processed_files'][filename] = {
            'hash': file_hash,
            'passed': passed,
            'last_processed': run_id,
            'results': results
        }
        
        if passed:
            passed_files.append(filepath)
            # Copy passed file to output directory
            output_path = os.path.join(output_dir, filename)
            with open(filepath, 'r') as f_in, open(output_path, 'w') as f_out:
                f_out.write(f_in.read())
        else:
            failed_files.append(filepath)
        
        # Save index periodically (every 100 files) to handle crashes
        if (i + 1) % 100 == 0:
            save_processing_index(index_file, index_data)
    
    # Final save of index
    save_processing_index(index_file, index_data)
    
    # Update run info in index
    elapsed_time = time.time() - start_time
    run_info = {
        'run_id': run_id,
        'dataset': dataset_name,
        'timestamp': run_id,
        'elapsed_time': elapsed_time,
        'files_processed': len(new_files),
        'files_passed': len(passed_files),
        'files_failed': len(failed_files),
        'parameters': {
            'tmax': TMAX,
            'dt': DT,
            'energy_error_threshold': ENERGY_ERROR_THRESHOLD,
            'min_distance_threshold': MIN_DISTANCE_THRESHOLD,
            'virial_ratio_range': [
                adaptive_thresholds['virial_min'] if adaptive_thresholds else VIRIAL_RATIO_MIN,
                adaptive_thresholds['virial_max'] if adaptive_thresholds else VIRIAL_RATIO_MAX
            ],
            'min_angular_momentum': adaptive_thresholds['angular_min'] if adaptive_thresholds else MIN_ANGULAR_MOMENTUM,
            'use_adaptive_thresholds': USE_PERCENTILE_THRESHOLDS
        }
    }
    
    index_data['processing_runs'].append(run_info)
    save_processing_index(index_file, index_data)
    
    # Summary statistics
    print(f"\nDataset {dataset_name} completed in {elapsed_time:.2f} seconds")
    print(f"Files processed in this run: {len(new_files)}")
    print(f"Passed: {len(passed_files)} ({len(passed_files)/len(new_files)*100:.1f}%)")
    print(f"Failed: {len(failed_files)} ({len(failed_files)/len(new_files)*100:.1f}%)")
    
    # Overall statistics
    total_processed = len(index_data['processed_files'])
    total_passed = sum(1 for f in index_data['processed_files'].values() if f['passed'])
    print(f"\nOverall statistics for {dataset_name} (all runs):")
    print(f"Total files ever processed: {total_processed}")
    print(f"Total passed: {total_passed} ({total_passed/total_processed*100:.1f}%)")
    
    # Analyze failure reasons for this run
    failure_reasons = {}
    for result in all_results:
        if not result['passed']:
            reason = result.get('reason', result.get('stage', 'unknown'))
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
    
    if failure_reasons:
        print(f"\nFailure breakdown for {dataset_name} (this run):")
        for reason, count in failure_reasons.items():
            print(f"  - {reason}: {count}")
    
    return {
        'dataset_name': dataset_name,
        'run_info': run_info,
        'failure_reasons': failure_reasons,
        'detailed_results': all_results,
        'elapsed_time': elapsed_time,
        'files_processed': len(new_files),
        'files_passed': len(passed_files),
        'files_failed': len(failed_files),
        'skipped_files': len(skipped_files)
    }


def main():
    """Main pre-screening pipeline that processes all datasets automatically."""
    print("Starting automated pre-screening pipeline")
    print(f"\nPre-screening parameters:")
    print(f"  - Integration time: {TMAX}")
    print(f"  - Time step: {DT}")
    print(f"  - Energy error threshold: {ENERGY_ERROR_THRESHOLD * 100}%")
    print(f"  - Minimum distance threshold: {MIN_DISTANCE_THRESHOLD}")
    print(f"  - Virial ratio range (fixed): [{VIRIAL_RATIO_MIN}, {VIRIAL_RATIO_MAX}]")
    print(f"  - Minimum angular momentum (fixed): {MIN_ANGULAR_MOMENTUM}")
    print(f"  - Using adaptive thresholds: {USE_PERCENTILE_THRESHOLDS}")
    
    # Create a single run ID for this execution
    run_id = datetime.now().isoformat()
    
    # Overall statistics
    overall_start_time = time.time()
    all_dataset_results = []
    
    # Process each dataset
    for config in DATASET_CONFIGS:
        dataset_results = process_dataset(config, run_id)
        all_dataset_results.append(dataset_results)
    
    # Overall summary
    overall_elapsed_time = time.time() - overall_start_time
    
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    print(f"Total execution time: {overall_elapsed_time:.2f} seconds")
    
    total_files_processed = 0
    total_files_passed = 0
    total_files_failed = 0
    
    for results in all_dataset_results:
        if 'skipped' not in results:
            total_files_processed += results['files_processed']
            total_files_passed += results['files_passed']
            total_files_failed += results['files_failed']
            
            print(f"\n{results['dataset_name']}:")
            print(f"  - Processed: {results['files_processed']}")
            print(f"  - Passed: {results['files_passed']}")
            print(f"  - Failed: {results['files_failed']}")
            print(f"  - Skipped (already processed): {results.get('skipped_files', 0)}")
    
    if total_files_processed > 0:
        print(f"\nTotal across all datasets:")
        print(f"  - Files processed: {total_files_processed}")
        print(f"  - Files passed: {total_files_passed} ({total_files_passed/total_files_processed*100:.1f}%)")
        print(f"  - Files failed: {total_files_failed} ({total_files_failed/total_files_processed*100:.1f}%)")
    
    # Save combined results to the new results directory
    run_results_file = os.path.join(
        "<home>/Desktop/3_body_problem/simulation_data/Validation/prescreening/prescreen_run_results",
        f"run_results_{run_id.replace(':', '-')}.json"
    )
    
    combined_results = {
        'run_id': run_id,
        'overall_elapsed_time': overall_elapsed_time,
        'total_files_processed': total_files_processed,
        'total_files_passed': total_files_passed,
        'total_files_failed': total_files_failed,
        'datasets': all_dataset_results
    }
    
    with open(run_results_file, 'w') as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"\nRun results saved to: {run_results_file}")
    print("\nProcessing complete!")


if __name__ == "__main__":
    main()

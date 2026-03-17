#!/usr/bin/env python3
"""
Brutus Metrics Calculator
- Processes completed Brutus output files
- Calculates conservation metrics (energy, momentum, angular momentum)
- Skips incomplete simulations
- Creates JSON metric files only for complete simulations
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import time

# Paths
BASE_DIR = Path("<home>/Desktop/3_body_problem")
PROBLEM_DIR = BASE_DIR / "simulation_data"

# Output and metrics directories
OUTPUT_DIRS = {
    "hierarchical": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical",
    "standard": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random"
}

METRICS_DIRS = {
    "hierarchical": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical",
    "standard": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard"
}

# Brutus parameters for reference
BRUTUS_PARAMS = {
    "hierarchical": {
        "tolerance": "1e-15",
        "word_length": "130",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.08",
        "n_particles": "3"
    },
    "standard": {
        "tolerance": "1e-13",
        "word_length": "118",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.17",
        "n_particles": "3"
    }
}

def parse_brutus_output(output_file):
    """Parse brutus output file to extract particle data at different times."""
    snapshots = []
    
    try:
        with open(output_file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"Failed to read output file {output_file}: {e}")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # Skip empty lines
            i += 1
            continue
            
        # Each snapshot starts with: time N t_cpu
        parts = line.split()
        if len(parts) == 3:
            try:
                time = float(parts[0])
                n = int(parts[1])
                t_cpu = float(parts[2])
            except ValueError:
                i += 1
                continue
            
            # Read particle data
            particles = []
            for j in range(n):
                i += 1
                if i < len(lines):
                    particle_line = lines[i].strip()
                    if particle_line:
                        particle_parts = particle_line.split()
                        if len(particle_parts) >= 7:
                            try:
                                particle = {
                                    'mass': float(particle_parts[0]),
                                    'x': float(particle_parts[1]),
                                    'y': float(particle_parts[2]),
                                    'z': float(particle_parts[3]),
                                    'vx': float(particle_parts[4]),
                                    'vy': float(particle_parts[5]),
                                    'vz': float(particle_parts[6])
                                }
                                particles.append(particle)
                            except ValueError as e:
                                print(f"Warning: Failed to parse particle data at line {i}: {e}")
            
            if len(particles) == n:  # Only add if we got all expected particles
                snapshots.append({
                    'time': time,
                    't_cpu': t_cpu,
                    'particles': particles
                })
        i += 1
    
    return snapshots

def calculate_total_energy(particles):
    """Calculate total energy (kinetic + potential) of the system."""
    kinetic = 0.0
    potential = 0.0
    
    # Kinetic energy
    for p in particles:
        v_squared = p['vx']**2 + p['vy']**2 + p['vz']**2
        kinetic += 0.5 * p['mass'] * v_squared
    
    # Potential energy (G=1 in N-body units)
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            dx = particles[i]['x'] - particles[j]['x']
            dy = particles[i]['y'] - particles[j]['y']
            dz = particles[i]['z'] - particles[j]['z']
            r = np.sqrt(dx**2 + dy**2 + dz**2)
            potential -= particles[i]['mass'] * particles[j]['mass'] / r
    
    return kinetic + potential

def calculate_linear_momentum(particles):
    """Calculate total linear momentum vector."""
    px = sum(p['mass'] * p['vx'] for p in particles)
    py = sum(p['mass'] * p['vy'] for p in particles)
    pz = sum(p['mass'] * p['vz'] for p in particles)
    return np.array([px, py, pz])

def calculate_angular_momentum(particles):
    """Calculate total angular momentum vector."""
    L = np.zeros(3)
    for p in particles:
        r = np.array([p['x'], p['y'], p['z']])
        v = np.array([p['vx'], p['vy'], p['vz']])
        L += p['mass'] * np.cross(r, v)
    return L

def is_simulation_complete(snapshots, expected_duration=10.0, tolerance=0.5):
    """Check if a simulation completed successfully."""
    if not snapshots:
        return False
    
    if len(snapshots) < 10:  # Too few snapshots
        return False
    
    # Check if simulation reached expected duration (with tolerance)
    last_time = snapshots[-1]['time']
    if last_time < expected_duration - tolerance:
        return False
    
    return True

def calculate_metrics(output_file, sim_type):
    """Calculate comprehensive metrics from simulation output."""
    try:
        # Parse output file
        snapshots = parse_brutus_output(output_file)
        
        # Check if simulation is complete
        if not is_simulation_complete(snapshots):
            return None  # Skip incomplete simulations
        
        # Get initial and final snapshots
        initial = snapshots[0]
        final = snapshots[-1]
        
        # Energy conservation
        E_initial = calculate_total_energy(initial['particles'])
        E_final = calculate_total_energy(final['particles'])
        dE_absolute = abs(E_final - E_initial)
        dE_relative = dE_absolute / abs(E_initial) if E_initial != 0 else float('inf')
        
        # Linear momentum conservation
        P_initial = calculate_linear_momentum(initial['particles'])
        P_final = calculate_linear_momentum(final['particles'])
        dP_magnitude = np.linalg.norm(P_final - P_initial)
        P_initial_norm = np.linalg.norm(P_initial)
        dP_relative = dP_magnitude / P_initial_norm if P_initial_norm > 1e-15 else dP_magnitude
        
        # Angular momentum conservation
        L_initial = calculate_angular_momentum(initial['particles'])
        L_final = calculate_angular_momentum(final['particles'])
        dL_magnitude = np.linalg.norm(L_final - L_initial)
        L_initial_norm = np.linalg.norm(L_initial)
        dL_relative = dL_magnitude / L_initial_norm if L_initial_norm > 1e-15 else dL_magnitude
        
        # Calculate timestep statistics
        time_diffs = [snapshots[i]['time'] - snapshots[i-1]['time'] for i in range(1, len(snapshots))]
        avg_timestep = np.mean(time_diffs) if time_diffs else 0
        timestep_stability = np.std(time_diffs) / np.mean(time_diffs) if time_diffs and np.mean(time_diffs) > 0 else 0
        
        # Get parameters for this simulation type
        params = BRUTUS_PARAMS[sim_type]
        
        metrics = {
            'file_info': {
                'output_file': str(output_file),
                'file_size_bytes': output_file.stat().st_size if output_file.exists() else 0
            },
            'simulation_parameters': {
                'simulation_type': sim_type,
                'tolerance': params['tolerance'],
                'word_length': int(params['word_length']),
                'time_begin': float(params['t_begin']),
                'time_end': float(params['t_end']),
                'dt_output': float(params['dt_out']),
                'n_particles': int(params['n_particles'])
            },
            'timing': {
                'simulation_time': final['time'],
                'simulation_duration': final['time'] - initial['time'],
                'cpu_time_seconds': final['t_cpu'],
                'snapshots_count': len(snapshots),
                'average_timestep': avg_timestep,
                'timestep_stability_coefficient': timestep_stability
            },
            'conservation': {
                'energy': {
                    'initial': E_initial,
                    'final': E_final,
                    'absolute_error': dE_absolute,
                    'relative_error': dE_relative,
                    'conservation_quality': 'excellent' if dE_relative < 1e-12 else 'good' if dE_relative < 1e-9 else 'fair' if dE_relative < 1e-6 else 'poor'
                },
                'linear_momentum': {
                    'initial': P_initial.tolist(),
                    'final': P_final.tolist(),
                    'initial_magnitude': P_initial_norm,
                    'final_magnitude': np.linalg.norm(P_final),
                    'absolute_error': dP_magnitude,
                    'relative_error': dP_relative,
                    'conservation_quality': 'excellent' if dP_relative < 1e-12 else 'good' if dP_relative < 1e-9 else 'fair' if dP_relative < 1e-6 else 'poor'
                },
                'angular_momentum': {
                    'initial': L_initial.tolist(),
                    'final': L_final.tolist(),
                    'initial_magnitude': L_initial_norm,
                    'final_magnitude': np.linalg.norm(L_final),
                    'absolute_error': dL_magnitude,
                    'relative_error': dL_relative,
                    'conservation_quality': 'excellent' if dL_relative < 1e-12 else 'good' if dL_relative < 1e-9 else 'fair' if dL_relative < 1e-6 else 'poor'
                }
            },
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'brutus_version': 'Newton-main',
                'analysis_script_version': '1.0'
            }
        }
        
        return metrics
        
    except Exception as e:
        print(f"Error calculating metrics for {output_file}: {e}")
        return None

def process_simulation_type(sim_type):
    """Process all output files for a simulation type."""
    output_dir = OUTPUT_DIRS[sim_type]
    metrics_dir = METRICS_DIRS[sim_type]
    
    # Create metrics directory
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all output files
    output_files = sorted(output_dir.glob(f"brutus_{sim_type}_*.txt"))
    
    if not output_files:
        print(f"No output files found for {sim_type}")
        return 0, 0, 0
    
    print(f"\nProcessing {sim_type.upper()} simulations")
    print(f"Output directory: {output_dir}")
    print(f"Metrics directory: {metrics_dir}")
    print(f"Total output files found: {len(output_files)}")
    print("-" * 80)
    
    processed = 0
    complete = 0
    incomplete = 0
    start_time = time.time()
    
    for i, output_file in enumerate(output_files):
        file_num = output_file.stem.split('_')[-1]
        metrics_path = metrics_dir / f"metrics_{sim_type}_{file_num}.json"
        
        # Skip if metrics already exist
        if metrics_path.exists():
            print(f"[{i+1:3d}/{len(output_files)}] Skip {output_file.name} - Metrics exist")
            continue
        
        # Calculate metrics
        metrics = calculate_metrics(output_file, sim_type)
        
        if metrics:
            # Save metrics
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            print(f"[{i+1:3d}/{len(output_files)}] ✓ {output_file.name} - Complete")
            complete += 1
        else:
            print(f"[{i+1:3d}/{len(output_files)}] ✗ {output_file.name} - Incomplete")
            incomplete += 1
        
        processed += 1
    
    elapsed = time.time() - start_time
    
    print("-" * 80)
    print(f"Summary for {sim_type}:")
    print(f"  Processed: {processed}")
    print(f"  Complete simulations: {complete}")
    print(f"  Incomplete simulations: {incomplete}")
    print(f"  Time taken: {elapsed:.1f} seconds")
    
    return processed, complete, incomplete

def main():
    print("Brutus Metrics Calculator")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_start = time.time()
    
    # Process hierarchical simulations
    hier_processed, hier_complete, hier_incomplete = process_simulation_type("hierarchical")
    
    # Process standard simulations
    std_processed, std_complete, std_incomplete = process_simulation_type("standard")
    
    # Final summary
    total_time = time.time() - total_start
    
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {total_time:.1f} seconds")
    print("")
    print("RESULTS:")
    print(f"  Hierarchical simulations:")
    print(f"    • Processed: {hier_processed}")
    print(f"    • Complete: {hier_complete}")
    print(f"    • Incomplete: {hier_incomplete}")
    print(f"  Standard simulations:")
    print(f"    • Processed: {std_processed}")
    print(f"    • Complete: {std_complete}")
    print(f"    • Incomplete: {std_incomplete}")
    print("")
    print("METRICS LOCATIONS:")
    print(f"  • Hierarchical metrics: {METRICS_DIRS['hierarchical']}")
    print(f"  • Standard metrics: {METRICS_DIRS['standard']}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

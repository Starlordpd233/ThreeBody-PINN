#!/usr/bin/env python3
"""
Brutus Metrics Calculator
- Processes all Brutus output files (no completeness checks)
- Calculates conservation metrics (energy, momentum, angular momentum)
- Creates JSON metric files for every file, even if partial or erroneous
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import time

# Paths
BASE_DIR = Path("<home>/Desktop/3_body_problem")
PROBLEM_DIR = BASE_DIR / "simulation_data"

# Input and metrics directories
INPUT_DIRS = {
    "hierarchical": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical",
    "hierarchical_gold_standard": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard",
    "standard": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random",
    "standard_gold_standard": PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random_gold_standard"
}

METRICS_DIRS = {
    "hierarchical": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical",
    "hierarchical_gold_standard": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical_gold_standard",
    "standard": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard",
    "standard_gold_standard": PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard_gold_standard"
}

# Metrics file name prefixes (to ensure consistent naming without gold_standard in filename)
METRICS_PREFIXES = {
    "hierarchical": "hierarchical",
    "hierarchical_gold_standard": "hierarchical",
    "standard": "standard",
    "standard_gold_standard": "standard"
}

# Glob patterns for output files (updated to match actual naming)
GLOB_PATTERNS = {
    "hierarchical": "brutus_hierarchical_*.txt",
    "hierarchical_gold_standard": "brutus_hierarchical_*.txt",
    "standard": "brutus_standard_*.txt",
    "standard_gold_standard": "brutus_standard_*.txt"
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
    "hierarchical_gold_standard": {
        "tolerance": "1e-13",
        "word_length": "130",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.01",
        "n_particles": "3"
    },
    "standard": {
        "tolerance": "1e-13",
        "word_length": "118",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.17",
        "n_particles": "3"
    },
    "standard_gold_standard": {
        "tolerance": "1e-13",
        "word_length": "130",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.01",
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
            
            if particles:  # Add even if partial particles (no strict n check)
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
            if r > 0:  # Avoid div by zero
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

def calculate_separation_metrics(snapshots):
    """Calculate min/max/avg particle separations over time."""
    separations = []
    for snapshot in snapshots:
        particles = snapshot['particles']
        if len(particles) < 2:
            continue
        
        seps = []
        for i in range(len(particles)):
            for j in range(i+1, len(particles)):
                dx = particles[i]['x'] - particles[j]['x']
                dy = particles[i]['y'] - particles[j]['y']
                dz = particles[i]['z'] - particles[j]['z']
                r = np.sqrt(dx**2 + dy**2 + dz**2)
                seps.append(r)
        
        if seps:
            separations.append({
                'time': snapshot['time'],
                'min_separation': min(seps),
                'max_separation': max(seps),
                'avg_separation': np.mean(seps)
            })
    
    return separations

def calculate_system_metrics(particles):
    """Calculate center of mass, total mass, virial ratio."""
    if not particles:
        return None
    
    total_mass = sum(p['mass'] for p in particles)
    
    # Center of mass
    com_x = sum(p['mass'] * p['x'] for p in particles) / total_mass if total_mass > 0 else 0
    com_y = sum(p['mass'] * p['y'] for p in particles) / total_mass if total_mass > 0 else 0
    com_z = sum(p['mass'] * p['z'] for p in particles) / total_mass if total_mass > 0 else 0
    
    # Virial ratio (2K/|U|)
    kinetic = sum(0.5 * p['mass'] * (p['vx']**2 + p['vy']**2 + p['vz']**2) 
                  for p in particles)
    potential = 0
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            dx = particles[i]['x'] - particles[j]['x']
            dy = particles[i]['y'] - particles[j]['y']
            dz = particles[i]['z'] - particles[j]['z']
            r = np.sqrt(dx**2 + dy**2 + dz**2)
            if r > 0:
                potential -= particles[i]['mass'] * particles[j]['mass'] / r
    
    virial_ratio = 2 * kinetic / abs(potential) if potential != 0 else np.inf
    
    return {
        'center_of_mass': [com_x, com_y, com_z],
        'total_mass': total_mass,
        'virial_ratio': virial_ratio
    }

def detect_escape_or_collision(separations, threshold_escape=100, threshold_collision=0.01):
    """Detect if system shows escape or collision behavior."""
    if not separations:
        return None
        
    min_sep_final = separations[-1]['min_separation']
    max_sep_final = separations[-1]['max_separation']
    
    return {
        'possible_escape': max_sep_final > threshold_escape,
        'possible_collision': min_sep_final < threshold_collision,
        'final_min_separation': min_sep_final,
        'final_max_separation': max_sep_final
    }

def identify_hierarchical_structure(particles):
    """Identify if system has hierarchical structure (close binary + distant third)."""
    if len(particles) != 3:
        return None
        
    # Calculate all pairwise separations
    seps = []
    for i in range(3):
        for j in range(i+1, 3):
            dx = particles[i]['x'] - particles[j]['x']
            dy = particles[i]['y'] - particles[j]['y']
            dz = particles[i]['z'] - particles[j]['z']
            seps.append(np.sqrt(dx**2 + dy**2 + dz**2))
    
    if not seps or min(seps) == 0:
        return None
    
    seps.sort()
    hierarchy_ratio = seps[2] / seps[1] if seps[1] > 0 else np.inf
    
    return {
        'is_hierarchical': hierarchy_ratio > 5,  # Threshold for hierarchical
        'hierarchy_ratio': hierarchy_ratio,
        'binary_separation': seps[0],
        'tertiary_separation': seps[2]
    }

def calculate_time_series_stats(values):
    """Calculate statistics for a list of values."""
    if not values:
        return None
    return {
        'mean': np.mean(values),
        'std': np.std(values),
        'min': np.min(values),
        'max': np.max(values),
        'range': np.max(values) - np.min(values)
    }

def calculate_metrics(output_file, sim_type):
    """Calculate comprehensive metrics from simulation output, handling partial data."""
    metrics = {
        'file_info': {
            'output_file': str(output_file),
            'file_size_bytes': output_file.stat().st_size if output_file.exists() else 0
        },
        'simulation_parameters': BRUTUS_PARAMS[sim_type],
        'timing': {},
        'conservation': {},
        'separation_metrics': [],
        'system_metrics': {},
        'detection': {},
        'hierarchical_structure': {},
        'time_series_stats': {},
        'metadata': {
            'analysis_timestamp': datetime.now().isoformat(),
            'brutus_version': 'Newton-main',
            'analysis_script_version': '1.2'  # Updated version
        },
        'error': None  # Field for any issues
    }
    
    try:
        # Parse output file
        snapshots = parse_brutus_output(output_file)
        
        if not snapshots:
            metrics['error'] = 'No valid snapshots found in file'
            return metrics
        
        # Get initial and final (even if same)
        initial = snapshots[0]
        final = snapshots[-1] if len(snapshots) > 1 else initial
        
        # Energy conservation
        E_initial = calculate_total_energy(initial['particles'])
        E_final = calculate_total_energy(final['particles'])
        dE_absolute = abs(E_final - E_initial)
        dE_relative = dE_absolute / abs(E_initial) if abs(E_initial) > 1e-15 else dE_absolute
        
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
        
        # Timestep statistics (handle few snapshots)
        time_diffs = [snapshots[i]['time'] - snapshots[i-1]['time'] for i in range(1, len(snapshots))]
        avg_timestep = np.mean(time_diffs) if time_diffs else 0.0
        timestep_stability = np.std(time_diffs) / avg_timestep if time_diffs and avg_timestep > 0 else 0.0
        
        metrics['timing'] = {
            'simulation_time': final['time'],
            'simulation_duration': final['time'] - initial['time'],
            'cpu_time_seconds': final['t_cpu'],
            'snapshots_count': len(snapshots),
            'average_timestep': avg_timestep,
            'timestep_stability_coefficient': timestep_stability
        }
        
        metrics['conservation'] = {
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
        }
        
        # Add separation metrics (full time series for plotting)
        separations = calculate_separation_metrics(snapshots)
        metrics['separation_metrics'] = separations
        
        # Add system metrics for initial and final
        initial_system = calculate_system_metrics(initial['particles'])
        final_system = calculate_system_metrics(final['particles'])
        metrics['system_metrics'] = {
            'initial': initial_system,
            'final': final_system
        }
        
        # Add detection
        detection = detect_escape_or_collision(separations)
        if detection:
            metrics['detection'] = detection
        
        # Add hierarchical structure if applicable
        if 'hierarchical' in sim_type and len(initial['particles']) == 3:
            initial_hier = identify_hierarchical_structure(initial['particles'])
            final_hier = identify_hierarchical_structure(final['particles'])
            metrics['hierarchical_structure'] = {
                'initial': initial_hier,
                'final': final_hier
            }
        
        # Add time series stats for energy
        energies = [calculate_total_energy(s['particles']) for s in snapshots if s['particles']]
        if energies:
            metrics['time_series_stats']['energy'] = calculate_time_series_stats(energies)
        
        # Add time series stats for virial ratio
        virials = []
        for s in snapshots:
            sys_met = calculate_system_metrics(s['particles'])
            if sys_met and np.isfinite(sys_met['virial_ratio']):
                virials.append(sys_met['virial_ratio'])
        if virials:
            metrics['time_series_stats']['virial_ratio'] = calculate_time_series_stats(virials)
        
        # Add stats for separations
        if separations:
            min_seps = [sep['min_separation'] for sep in separations]
            max_seps = [sep['max_separation'] for sep in separations]
            avg_seps = [sep['avg_separation'] for sep in separations]
            metrics['time_series_stats']['min_separation'] = calculate_time_series_stats(min_seps)
            metrics['time_series_stats']['max_separation'] = calculate_time_series_stats(max_seps)
            metrics['time_series_stats']['avg_separation'] = calculate_time_series_stats(avg_seps)
        
    except Exception as e:
        metrics['error'] = f'Error during metrics calculation: {str(e)}'
    
    return metrics

def is_valid_metrics_file(metrics_path):
    """Check if the metrics file exists and is a valid JSON."""
    if not metrics_path.exists():
        return False
    try:
        with open(metrics_path, 'r') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False

def process_simulation_type(sim_type):
    """Process all output files for a simulation type."""
    input_dir = INPUT_DIRS[sim_type]
    metrics_dir = METRICS_DIRS[sim_type]
    
    # Create metrics directory
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all output files
    output_files = sorted(input_dir.glob(GLOB_PATTERNS[sim_type]))
    
    if not output_files:
        print(f"No output files found for {sim_type}")
        return 0, 0, 0
    
    print(f"\nProcessing {sim_type.upper()} simulations")
    print(f"Input directory: {input_dir}")
    print(f"Metrics directory: {metrics_dir}")
    print(f"Total output files found: {len(output_files)}")
    print("-" * 80)
    
    processed = 0
    generated = 0
    with_errors = 0
    start_time = time.time()
    
    metrics_prefix = METRICS_PREFIXES[sim_type]
    
    for i, output_file in enumerate(output_files):
        # Extract file_num
        file_num = output_file.stem.split('_')[-1]
        
        metrics_path = metrics_dir / f"metrics_{metrics_prefix}_{file_num}.json"
        
        # Skip if valid metrics already exist
        if is_valid_metrics_file(metrics_path):
            print(f"[{i+1:3d}/{len(output_files)}] Skip {output_file.name} - Valid metrics exist")
            continue
        
        # Calculate metrics (always returns a dict)
        metrics = calculate_metrics(output_file, sim_type)
        
        # Save metrics
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        if metrics.get('error'):
            print(f"[{i+1:3d}/{len(output_files)}] ! {output_file.name} - Generated with error")
            with_errors += 1
        else:
            print(f"[{i+1:3d}/{len(output_files)}] ✓ {output_file.name} - Generated")
            generated += 1
        
        processed += 1
    
    elapsed = time.time() - start_time
    
    print("-" * 80)
    print(f"Summary for {sim_type}:")
    print(f"  Processed: {processed}")
    print(f"  Metrics generated: {generated}")
    print(f"  Metrics with errors: {with_errors}")
    print(f"  Time taken: {elapsed:.1f} seconds")
    
    return processed, generated, with_errors

def main():
    print("Brutus Metrics Calculator")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_start = time.time()
    
    # Process hierarchical simulations
    hier_processed, hier_generated, hier_errors = process_simulation_type("hierarchical")
    
    # Process hierarchical gold standard simulations
    hier_gold_processed, hier_gold_generated, hier_gold_errors = process_simulation_type("hierarchical_gold_standard")
    
    # Process standard simulations
    std_processed, std_generated, std_errors = process_simulation_type("standard")
    
    # Process standard gold standard simulations
    std_gold_processed, std_gold_generated, std_gold_errors = process_simulation_type("standard_gold_standard")
    
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
    print(f"    • Generated: {hier_generated}")
    print(f"    • With errors: {hier_errors}")
    print(f"  Hierarchical gold standard simulations:")
    print(f"    • Processed: {hier_gold_processed}")
    print(f"    • Generated: {hier_gold_generated}")
    print(f"    • With errors: {hier_gold_errors}")
    print(f"  Standard simulations:")
    print(f"    • Processed: {std_processed}")
    print(f"    • Generated: {std_generated}")
    print(f"    • With errors: {std_errors}")
    print(f"  Standard gold standard simulations:")
    print(f"    • Processed: {std_gold_processed}")
    print(f"    • Generated: {std_gold_generated}")
    print(f"    • With errors: {std_gold_errors}")
    print("")
    print("METRICS LOCATIONS:")
    print(f"  • Hierarchical metrics: {METRICS_DIRS['hierarchical']}")
    print(f"  • Hierarchical gold standard metrics: {METRICS_DIRS['hierarchical_gold_standard']}")
    print(f"  • Standard metrics: {METRICS_DIRS['standard']}")
    print(f"  • Standard gold standard metrics: {METRICS_DIRS['standard_gold_standard']}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
"""
Utility functions for parsing IC and metric files from Brutus simulations
"""
import numpy as np
import os
import json
from typing import List, Tuple, Dict


def parse_ic_file(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Parse initial condition file to extract positions and velocities.

    Args:
        filepath: Path to IC file

    Returns:
        positions: (N,3) array of particle positions
        velocities: (N,3) array of particle velocities
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    positions = []
    velocities = []
    for line in lines:
        if line.strip():  # Skip empty lines
            values = np.array([float(x) for x in line.split()])
            positions.append(values[1:4])  # x, y, z
            velocities.append(values[4:7])  # vx, vy, vz

    return np.array(positions), np.array(velocities)


def load_ic_file(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load initial condition file and extract positions and masses.

    Args:
        filepath: Path to IC file

    Returns:
        positions: (N,3) array
        masses: (N,) array
    """
    positions, _ = parse_ic_file(filepath)
    masses = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.split()
                masses.append(float(parts[0]))
    return positions, np.array(masses)


def parse_metric_file(filepath: str) -> Dict:
    """
    Parse metric file to extract simulation metrics.

    Args:
        filepath: Path to metric file

    Returns:
        Dictionary containing metric data
    """
    metrics = {}

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Parse based on expected format - adjust as needed
        for line in lines:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                try:
                    metrics[key.strip()] = float(value.strip())
                except ValueError:
                    metrics[key.strip()] = value.strip()
            elif line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        metrics[parts[0]] = ' '.join(parts[1:])
                    except:
                        pass
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return metrics


def load_metrics(filepath: str) -> Dict:
    """
    Load simulation metrics from a JSON file.
    This function dynamically locates the corresponding initial condition (IC) file
    based on the metric file's path and handles different data formats.

    Args:
        filepath: Absolute path to the metric file (JSON).

    Returns:
        Dictionary of metrics with expected keys for compatibility.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.json':
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            transformed_data = {}
            
            # FIX #1: Robustly get duration from either wall_time or cpu_time
            if 'timing' in data:
                duration = data['timing'].get('wall_time_seconds')
                if duration is None:
                    duration = data['timing'].get('cpu_time_seconds', 0.0)
                transformed_data['duration'] = duration
            
            if 'conservation' in data and 'energy' in data['conservation']:
                transformed_data['energy_error'] = data['conservation']['energy'].get('relative_error', 0.0)

            # FIX #2: Dynamically construct the IC file path, removing hardcoded directories
            transformed_data['positions'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Default
            
            # Try to get IC filename from input_file_info first
            ic_filename = None
            if 'input_file_info' in data and 'filename' in data['input_file_info']:
                ic_filename = data['input_file_info']['filename']  # e.g., 'ic_hierarchical_0006.txt'
            
            # If not found, derive it from the output filename
            if not ic_filename and 'file_info' in data and 'output_file' in data['file_info']:
                output_file = data['file_info']['output_file']
                # Extract the number from brutus_hierarchical_XXXX.txt
                output_basename = os.path.basename(output_file)
                if 'hierarchical' in output_basename:
                    # Extract number from brutus_hierarchical_XXXX.txt
                    try:
                        num = output_basename.split('_')[-1].split('.')[0]
                        ic_filename = f'ic_hierarchical_{num}.txt'
                    except:
                        pass
                elif 'standard' in output_basename:
                    # Extract number from brutus_standard_XXXX.txt
                    try:
                        num = output_basename.split('_')[-1].split('.')[0]
                        ic_filename = f'ic_standard_{num}.txt'
                    except:
                        pass
            
            if ic_filename:
                # Determine simulation type ('hierarchical' or 'standard')
                sim_type = 'standard'
                if 'hierarchical' in filepath:
                    sim_type = 'hierarchical'
                    
                # Construct the correct IC file path from the metric file path
                # Assumes a structure like: .../simulation_data/Data/{metrics/sim_result_metric_..., ic_raw/}/
                base_project_path = os.path.dirname(os.path.dirname(filepath))
                
                # Fix: The directories are already named ic_hierarchical and ic_standard_quasi_random
                if sim_type == 'hierarchical':
                    ic_dir = 'ic_hierarchical'
                else:
                    ic_dir = 'ic_standard_quasi_random'
                    
                ic_filepath = os.path.join(
                    base_project_path, 
                    'ic_raw_datasets', 
                    ic_dir, 
                    ic_filename
                )

                if os.path.exists(ic_filepath):
                    try:
                        positions, _ = parse_ic_file(ic_filepath)
                        transformed_data['positions'] = positions.tolist()
                    except Exception as e:
                        print(f"Could not parse IC file {ic_filepath}: {e}")
                else:
                    print(f"IC file not found at constructed path: {ic_filepath}")

            # Robustly get the initial parameter number
            ic_param_found = False
            if 'input_file_info' in data:
                filename = data['input_file_info'].get('filename', '')
                try:
                    sim_num = int(filename.split('_')[-1].split('.')[0])
                    transformed_data['initial_param'] = sim_num
                    ic_param_found = True
                except (ValueError, IndexError):
                    pass
            
            if not ic_param_found:
                try:
                    # Fallback for metric files that don't have an input_file_info block
                    metric_filename = os.path.basename(data['file_info']['output_file'])
                    sim_num = int(metric_filename.split('_')[-1].split('.')[0])
                    transformed_data['initial_param'] = sim_num
                except (KeyError, ValueError, IndexError):
                    transformed_data['initial_param'] = 0
            
            transformed_data['original_data'] = data
            return transformed_data
            
        except Exception as e:
            print(f"Error loading JSON metrics {filepath}: {e}")
            return {}
    else:
        return parse_metric_file(filepath)


def load_metrics_with_positions(filepath: str, ic_base_dir: str = None) -> Dict:
    """
    Load simulation metrics with positions from corresponding IC file.
    
    Args:
        filepath: Path to metric file (JSON)
        ic_base_dir: Base directory for IC files (optional, now handled in load_metrics)
    
    Returns:
        Dictionary of metrics with actual positions
    """
    # This function now just calls the main load_metrics function
    data = load_metrics(filepath)
    return data


def calculate_hierarchical_properties(positions: np.ndarray) -> Dict:
    """
    Calculate properties specific to hierarchical systems.

    Args:
        positions: (3,3) array of particle positions

    Returns:
        Dictionary of properties
    """
    positions = np.array(positions)
    # Pairwise distances
    r01 = np.linalg.norm(positions[0] - positions[1])
    r02 = np.linalg.norm(positions[0] - positions[2])
    r12 = np.linalg.norm(positions[1] - positions[2])

    # Determine binary and distant particle
    if r01 < r02 and r01 < r12:
        binary_pair = (0, 1)
        distant_particle = 2
        binary_separation = r01
        hierarchical_ratio = min(r02, r12) / r01
    elif r02 < r01 and r02 < r12:
        binary_pair = (0, 2)
        distant_particle = 1
        binary_separation = r02
        hierarchical_ratio = min(r01, r12) / r02
    else:
        binary_pair = (1, 2)
        distant_particle = 0
        binary_separation = r12
        hierarchical_ratio = min(r01, r02) / r12

    binary_com = (positions[binary_pair[0]] + positions[binary_pair[1]]) / 2
    com_distance = np.linalg.norm(positions[distant_particle] - binary_com)

    return {
        'binary_pair': binary_pair,
        'distant_particle': distant_particle,
        'binary_separation': binary_separation,
        'hierarchical_ratio': hierarchical_ratio,
        'com_distance': com_distance
    }


def get_sample_files(directory: str,
                    sample_size: int = 200,
                    strategy: str = 'stratified') -> List[str]:
    """
    Sample files from a directory by different stratification strategies.
    This is the function expected by particle_positions_viz.py.

    Args:
        directory: Path to directory of files
        sample_size: Total number of samples to return
        strategy: 'random', 'round_robin', or 'stratified'

    Returns:
        List of sampled file paths
    """
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not all_files:
        return []
    
    if strategy == 'random':
        n_samples = min(sample_size, len(all_files))
        selected_files = np.random.choice(all_files, size=n_samples, replace=False)
        return [os.path.join(directory, f) for f in selected_files]
    
    elif strategy == 'round_robin':
        step = max(1, len(all_files) // sample_size)
        selected_files = all_files[::step][:sample_size]
        return [os.path.join(directory, f) for f in selected_files]
    
    elif strategy == 'stratified':
        n_strata = 5  # Default number of strata
        selected = []
        strata_size = len(all_files) // n_strata
        remainder = len(all_files) % n_strata
        samples_per_stratum = sample_size // n_strata
        
        start = 0
        for i in range(n_strata):
            end = start + strata_size + (1 if i < remainder else 0)
            stratum_files = all_files[start:end]
            
            if samples_per_stratum >= len(stratum_files):
                selected.extend(stratum_files)
            else:
                indices = np.random.choice(len(stratum_files), samples_per_stratum, replace=False)
                selected.extend([stratum_files[idx] for idx in indices])
            start = end
        
        # If we have fewer than sample_size, add more randomly
        if len(selected) < sample_size:
            remaining_files = [f for f in all_files if f not in selected]
            if remaining_files:
                additional_needed = sample_size - len(selected)
                additional = np.random.choice(remaining_files, 
                                            size=min(additional_needed, len(remaining_files)), 
                                            replace=False)
                selected.extend(additional)
        
        return [os.path.join(directory, f) for f in selected[:sample_size]]
    
    else:
        raise ValueError(f"Unknown sampling strategy: {strategy}")


def sample_files(directory: str,
                 strategy: str = 'random',
                 samples_per_stratum: int = 1,
                 n_strata: int = 5) -> List[str]:
    """
    Sample files from a directory by different stratification strategies.
    Original function kept for backward compatibility.

    Args:
        directory: Path to directory of files
        strategy: 'random', 'round_robin', or 'stratified'
        samples_per_stratum: Number of samples per stratum (for stratified)
        n_strata: Number of strata (for stratified)

    Returns:
        List of sampled file paths
    """
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if strategy == 'random':
        return [os.path.join(directory, f) for f in np.random.choice(all_files, size=samples_per_stratum, replace=False)]
    elif strategy == 'round_robin':
        return [os.path.join(directory, f) for f in all_files[::max(1, len(all_files)//samples_per_stratum)]]
    elif strategy == 'stratified':
        selected = []
        strata_size = len(all_files) // n_strata
        remainder = len(all_files) % n_strata
        start = 0
        for i in range(n_strata):
            end = start + strata_size + (1 if i < remainder else 0)
            stratum_files = all_files[start:end]
            if samples_per_stratum >= len(stratum_files):
                selected.extend(stratum_files)
            else:
                indices = np.random.choice(len(stratum_files), samples_per_stratum, replace=False)
                selected.extend([stratum_files[idx] for idx in indices])
            start = end
        return [os.path.join(directory, f) for f in selected]
    else:
        raise ValueError(f"Unknown sampling strategy: {strategy}")


"""
Utility functions for parsing IC and metric files from Brutus simulations

import numpy as np
import os
import json
from typing import List, Tuple, Dict


def parse_ic_file(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    
    Parse initial condition file to extract positions and velocities.

    Args:
        filepath: Path to IC file

    Returns:
        positions: (N,3) array of particle positions
        velocities: (N,3) array of particle velocities
    
    with open(filepath, 'r') as f:
        lines = f.readlines()

    positions = []
    velocities = []
    for line in lines:
        if line.strip():  # Skip empty lines
            values = np.array([float(x) for x in line.split()])
            positions.append(values[1:4])  # x, y, z
            velocities.append(values[4:7])  # vx, vy, vz

    return np.array(positions), np.array(velocities)


def load_ic_file(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    
    Load initial condition file and extract positions and masses.

    Args:
        filepath: Path to IC file

    Returns:
        positions: (N,3) array
        masses: (N,) array
    
    positions, _ = parse_ic_file(filepath)
    masses = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.split()
                masses.append(float(parts[0]))
    return positions, np.array(masses)


def parse_metric_file(filepath: str) -> Dict:
    
    Parse metric file to extract simulation metrics.

    Args:
        filepath: Path to metric file

    Returns:
        Dictionary containing metric data
    
    metrics = {}

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Parse based on expected format - adjust as needed
        for line in lines:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                try:
                    metrics[key.strip()] = float(value.strip())
                except ValueError:
                    metrics[key.strip()] = value.strip()
            elif line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        metrics[parts[0]] = ' '.join(parts[1:])
                    except:
                        pass
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return metrics


def load_metrics_with_positions(filepath: str, ic_base_dir: str = None) -> Dict:
    
    Load simulation metrics with positions from corresponding IC file.
    
    Args:
        filepath: Path to metric file (JSON)
        ic_base_dir: Base directory for IC files (optional)
    
    Returns:
        Dictionary of metrics with actual positions
    
    data = load_metrics(filepath)
    
    # Try to load positions from IC file
    if 'original_data' in data and 'input_file_info' in data['original_data']:
        ic_filename = data['original_data']['input_file_info'].get('filename', '')
        if ic_filename and ic_base_dir:
            ic_filepath = os.path.join(ic_base_dir, ic_filename)
            try:
                positions, _ = parse_ic_file(ic_filepath)
                data['positions'] = positions.tolist()
            except Exception as e:
                print(f"Warning: Could not load positions from {ic_filepath}: {e}")
                # Keep placeholder positions
                pass
    
    return data


def load_metrics(filepath: str, ic_base_dir: str = '<home>/Desktop/3_body_problem/simulation_data/Data/ic_raw/ic_hierarchical/') -> Dict:
    
    Load simulation metrics from JSON or text file.
    Handles the actual Brutus metrics format and provides expected keys for metrics_analysis.py.

    Args:
        filepath: Path to metric file (JSON or text)
        ic_base_dir: Base directory where the initial condition files are stored.

    Returns:
        Dictionary of metrics with expected keys for compatibility
    
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.json':
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            transformed_data = {}
            
            if 'timing' in data:
                transformed_data['duration'] = data['timing'].get('wall_time_seconds', 0.0)
            
            if 'conservation' in data and 'energy' in data['conservation']:
                transformed_data['energy_error'] = data['conservation']['energy'].get('relative_error', 0.0)
            
            # Load actual positions from the corresponding IC file
            transformed_data['positions'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Default placeholder
            if 'input_file_info' in data and 'filename' in data['input_file_info']:
                ic_filename = data['input_file_info']['filename']
                ic_filepath = os.path.join(ic_base_dir, ic_filename)
                
                if os.path.exists(ic_filepath):
                    try:
                        positions, _ = parse_ic_file(ic_filepath)
                        transformed_data['positions'] = positions.tolist()
                    except Exception as e:
                        print(f"Could not parse IC file {ic_filepath}: {e}")
                else:
                    print(f"IC file not found: {ic_filepath}")


            if 'input_file_info' in data:
                filename = data['input_file_info'].get('filename', '')
                try:
                    sim_num = int(filename.split('_')[-1].split('.')[0])
                    transformed_data['initial_param'] = sim_num
                except:
                    transformed_data['initial_param'] = 0
            else:
                transformed_data['initial_param'] = 0
            
            transformed_data['original_data'] = data
            
            return transformed_data
            
        except Exception as e:
            print(f"Error loading JSON metrics {filepath}: {e}")
            return {}
    else:
        return parse_metric_file(filepath)
    

def calculate_hierarchical_properties(positions: np.ndarray) -> Dict:
    
    Calculate properties specific to hierarchical systems.

    Args:
        positions: (3,3) array of particle positions

    Returns:
        Dictionary of properties
    
    # Pairwise distances
    r01 = np.linalg.norm(positions[0] - positions[1])
    r02 = np.linalg.norm(positions[0] - positions[2])
    r12 = np.linalg.norm(positions[1] - positions[2])

    # Determine binary and distant particle
    if r01 < r02 and r01 < r12:
        binary_pair = (0, 1)
        distant_particle = 2
        binary_separation = r01
        hierarchical_ratio = min(r02, r12) / r01
    elif r02 < r01 and r02 < r12:
        binary_pair = (0, 2)
        distant_particle = 1
        binary_separation = r02
        hierarchical_ratio = min(r01, r12) / r02
    else:
        binary_pair = (1, 2)
        distant_particle = 0
        binary_separation = r12
        hierarchical_ratio = min(r01, r02) / r12

    binary_com = (positions[binary_pair[0]] + positions[binary_pair[1]]) / 2
    com_distance = np.linalg.norm(positions[distant_particle] - binary_com)

    return {
        'binary_pair': binary_pair,
        'distant_particle': distant_particle,
        'binary_separation': binary_separation,
        'hierarchical_ratio': hierarchical_ratio,
        'com_distance': com_distance
    }


def get_sample_files(directory: str,
                    sample_size: int = 200,
                    strategy: str = 'stratified') -> List[str]:
    
    Sample files from a directory by different stratification strategies.
    This is the function expected by particle_positions_viz.py.

    Args:
        directory: Path to directory of files
        sample_size: Total number of samples to return
        strategy: 'random', 'round_robin', or 'stratified'

    Returns:
        List of sampled file paths
    
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not all_files:
        return []
    
    if strategy == 'random':
        n_samples = min(sample_size, len(all_files))
        selected_files = np.random.choice(all_files, size=n_samples, replace=False)
        return [os.path.join(directory, f) for f in selected_files]
    
    elif strategy == 'round_robin':
        step = max(1, len(all_files) // sample_size)
        selected_files = all_files[::step][:sample_size]
        return [os.path.join(directory, f) for f in selected_files]
    
    elif strategy == 'stratified':
        n_strata = 5  # Default number of strata
        selected = []
        strata_size = len(all_files) // n_strata
        remainder = len(all_files) % n_strata
        samples_per_stratum = sample_size // n_strata
        
        start = 0
        for i in range(n_strata):
            end = start + strata_size + (1 if i < remainder else 0)
            stratum_files = all_files[start:end]
            
            if samples_per_stratum >= len(stratum_files):
                selected.extend(stratum_files)
            else:
                indices = np.random.choice(len(stratum_files), samples_per_stratum, replace=False)
                selected.extend([stratum_files[idx] for idx in indices])
            start = end
        
        # If we have fewer than sample_size, add more randomly
        if len(selected) < sample_size:
            remaining_files = [f for f in all_files if f not in selected]
            if remaining_files:
                additional_needed = sample_size - len(selected)
                additional = np.random.choice(remaining_files, 
                                            size=min(additional_needed, len(remaining_files)), 
                                            replace=False)
                selected.extend(additional)
        
        return [os.path.join(directory, f) for f in selected[:sample_size]]
    
    else:
        raise ValueError(f"Unknown sampling strategy: {strategy}")


def sample_files(directory: str,
                 strategy: str = 'random',
                 samples_per_stratum: int = 1,
                 n_strata: int = 5) -> List[str]:
    
    Sample files from a directory by different stratification strategies.
    Original function kept for backward compatibility.

    Args:
        directory: Path to directory of files
        strategy: 'random', 'round_robin', or 'stratified'
        samples_per_stratum: Number of samples per stratum (for stratified)
        n_strata: Number of strata (for stratified)

    Returns:
        List of sampled file paths
    
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if strategy == 'random':
        return [os.path.join(directory, f) for f in np.random.choice(all_files, size=samples_per_stratum, replace=False)]
    elif strategy == 'round_robin':
        return [os.path.join(directory, f) for f in all_files[::max(1, len(all_files)//samples_per_stratum)]]
    elif strategy == 'stratified':
        selected = []
        strata_size = len(all_files) // n_strata
        remainder = len(all_files) % n_strata
        start = 0
        for i in range(n_strata):
            end = start + strata_size + (1 if i < remainder else 0)
            stratum_files = all_files[start:end]
            if samples_per_stratum >= len(stratum_files):
                selected.extend(stratum_files)
            else:
                indices = np.random.choice(len(stratum_files), samples_per_stratum, replace=False)
                selected.extend([stratum_files[idx] for idx in indices])
            start = end
        return [os.path.join(directory, f) for f in selected]
    else:
        raise ValueError(f"Unknown sampling strategy: {strategy}")
"""
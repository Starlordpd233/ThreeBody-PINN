# parsing.py
"""
File parsing utilities for IC and BRUTUS files, aligned with CTL document Step 1.
UPDATED to be fully compatible with data_structures.py.
Can now run standalone to parse and save individual files.
MODIFIED to use HDF5 (.h5) output format instead of .npz.

ONE-CLICK EXECUTION:
Simply run: python parsing.py
The script will use the default paths defined below and process the default number of test files.

To override defaults, use command line arguments:
python parsing.py --ic_dir /path/to/ic --brutus_dir /path/to/brutus --ic_output_dir /path/to/ic_output --brutus_output_dir /path/to/brutus_output --max_ic_files 10 --max_brutus_files 10
"""
import numpy as np
from pathlib import Path
import re
import pickle
import argparse
from typing import Tuple, Dict, Optional
from tqdm import tqdm
import json
import h5py  # Import h5py for HDF5 support
from data_structures import RawTrajectoryData, SimulationMetadata
import concurrent.futures  # For parallel processing

# ============================================================================
# CONFIGURATION - TESTING SETTINGS
# ============================================================================
# Set these to control how many files to process for testing
# Set to None to process all files
DEFAULT_MAX_IC_FILES_FOR_TESTING = 3
DEFAULT_MAX_BRUTUS_FILES_FOR_TESTING = 3

# ============================================================================
# DEFAULT PATHS - MODIFY THESE FOR ONE-CLICK EXECUTION
# ============================================================================
DEFAULT_IC_DIR = Path("<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_hierarchical")
DEFAULT_BRUTUS_DIR = Path("<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_hierarchical")
DEFAULT_IC_OUTPUT_DIR = Path("<home>/Desktop/cursor/pinn/data-handling/core/preprocessed-data/parsed-data/ic")
DEFAULT_BRUTUS_OUTPUT_DIR = Path("<home>/Desktop/cursor/pinn/data-handling/core/preprocessed-data/parsed-data/brutus")

# Note: These paths are relative to the parsing.py script location
# Adjust them based on your actual directory structure
# The 'detect_simulation_metadata' and 'parse_ic_file' functions
# are already compatible and remain unchanged.
# ... (functions from previous response would go here) ...

def detect_simulation_metadata(ic_path: Path, brutus_path: Path) -> SimulationMetadata:
    """
    Detect simulation metadata from file paths and names.
    This logic cross-references filename patterns with time-step inference
    from the BRUTUS file to determine the dataset set (1a, 1b, 2a, 2b).
    """
    ic_name = ic_path.stem
    # Extract dataset type ('hierarchical' or 'quasi-random')
    if 'hierarchical' in ic_name:
        dataset_type = 'hierarchical'
    elif 'quasirandom' in ic_name or 'quasi-random' in ic_name:
        dataset_type = 'quasi-random'
    else:
        raise ValueError(f"Cannot determine dataset type from IC file name: {ic_name}")
    # Extract trajectory ID
    match = re.search(r'(\d+)', ic_name)
    traj_id = match.group(1) if match else ic_name.split('_')[-1]
    # Infer fidelity and dt_out by reading the first few timestamps from BRUTUS file
    try:
        with open(brutus_path, 'r') as f:
            times = []
            for line in f:
                parts = line.strip().split()
                if len(parts) == 3:  # Header line format: t, N, t_cpu 
                    try:
                        times.append(float(parts[0]))
                    except ValueError:
                        continue
                    if len(times) >= 2:
                        break
    except FileNotFoundError:
        print(f"Warning: BRUTUS file not found at {brutus_path}. Cannot infer dt.")
        times = []
    # Use inferred dt to determine fidelity, with wider tolerance for robustness
    if len(times) >= 2:
        dt_approx = times[1] - times[0]
        if abs(dt_approx - 0.01) < 0.005:  # For Set 2a/2b 
            fidelity, dt_out = 'high', 0.01
        elif abs(dt_approx - 0.08) < 0.02: # For Set 1a 
            fidelity, dt_out = 'low', 0.08
        elif abs(dt_approx - 0.17) < 0.02: # For Set 1b 
            fidelity, dt_out = 'low', 0.17
        else:
            print(f"Warning: Unrecognized dt={dt_approx:.4f} in {brutus_path}. Using default.")
            fidelity = 'low'
            dt_out = 0.08 if dataset_type == 'hierarchical' else 0.17
    else:
        # Fallback for short files or if dt inference fails
        print(f"Warning: Fewer than 2 timestamps in {brutus_path}. Using default metadata.")
        fidelity = 'low'
        dt_out = 0.08 if dataset_type == 'hierarchical' else 0.17
    # Determine set name ('1a', '1b', '2a', '2b') based on type and fidelity
    if dataset_type == 'hierarchical':
        set_name = '2a' if fidelity == 'high' else '1a'
    else: # quasi-random
        set_name = '2b' if fidelity == 'high' else '1b'
    return SimulationMetadata(
        trajectory_id=f"{dataset_type}_{traj_id}",
        ic_file=ic_path,
        brutus_file=brutus_path,
        dataset_type=dataset_type,
        fidelity=fidelity,
        dt_out=dt_out,
        set_name=set_name
    )

def parse_ic_file(filepath: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Parses an initial condition file, handling both single-line (21 values)
    and 3-line (7 values per body) formats.
    """
    with open(filepath, 'r') as f:
        lines = [line for line in f.readlines() if line.strip()]
    if len(lines) == 1:
        data = np.fromstring(lines[0], sep=' ')
        if data.size != 21:
            raise ValueError(f"Expected 21 values in single-line IC file {filepath}, got {data.size}")
        data = data.reshape(3, 7)
    elif len(lines) == 3:
        data = np.array([np.fromstring(line, sep=' ') for line in lines])
        if data.shape != (3, 7):
            raise ValueError(f"Expected 3 lines with 7 values each in {filepath}, shape is {data.shape}")
    else:
        raise ValueError(f"IC file {filepath} must have 1 or 3 non-empty lines, found {len(lines)}")
    masses = data[:, 0].copy()
    positions = data[:, 1:4].copy()
    velocities = data[:, 4:7].copy()
    return masses, positions, velocities

def parse_brutus_file(filepath: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict]:
    """
    Parses a BRUTUS output file, extracting time series and final metadata.
    This version ensures metadata keys match the RawTrajectoryData dataclass.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    brutus_metadata = {}
    if lines and lines[-1].startswith('Result:'):
        result_line = lines.pop()
        # Map file keys to dataclass field names
        key_map = {
            'E_initial': 'energy_initial',
            'E_final': 'energy_final',
            'dE/E': 'energy_error'
        }
        for file_key, data_key in key_map.items():
            match = re.search(rf'{file_key}=\s*([-\d.eE]+)', result_line)
            if match:
                brutus_metadata[data_key] = float(match.group(1))
    times, positions, velocities, cpu_times = [], [], [], []
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        header = lines[i].strip().split()
        if len(header) != 3:
            i += 1
            continue
        try:
            t, n_bodies, t_cpu = float(header[0]), int(header[1]), float(header[2])
            if n_bodies != 3: raise ValueError
            body_data = np.array([np.fromstring(lines[i + j + 1], sep=' ') for j in range(3)])
            if body_data.shape != (3, 7): raise ValueError
            times.append(t)
            positions.append(body_data[:, 1:4])
            velocities.append(body_data[:, 4:7])
            cpu_times.append(t_cpu)
            i += 4
        except (ValueError, IndexError):
            i += 1
            continue
    if not times:
        print(f"Warning: No valid snapshots found in {filepath}. Returning empty arrays.")
        return np.array([]), np.array([]), np.array([]), brutus_metadata
    brutus_metadata['cpu_times'] = np.array(cpu_times)
    return np.array(times), np.array(positions), np.array(velocities), brutus_metadata

def parse_trajectory_pair(ic_path: Path, brutus_path: Path) -> RawTrajectoryData:
    """
    Parses a pair of IC and BRUTUS files into a single RawTrajectoryData object.
    """
    masses, r_initial, v_initial = parse_ic_file(ic_path)
    times, positions, velocities, brutus_metadata = parse_brutus_file(brutus_path)
    metadata = detect_simulation_metadata(ic_path, brutus_path)
    return RawTrajectoryData(
        metadata=metadata,
        masses=masses,
        r_initial=r_initial,
        v_initial=v_initial,
        times=times,
        positions=positions,
        velocities=velocities,
        **brutus_metadata  # Unpacks dict into matching dataclass fields
    )

# ============================================================================
# STANDALONE EXECUTION FUNCTIONS - MODIFIED FOR HDF5
# ============================================================================

def save_parsed_ic(ic_data: Tuple[np.ndarray, np.ndarray, np.ndarray], 
                   metadata: SimulationMetadata, output_path: Path) -> None:
    """
    Save parsed IC data to HDF5 file with attributes for metadata.
    Args:
        ic_data: Tuple of (masses, positions, velocities)
        metadata: SimulationMetadata object
        output_path: Path to save the HDF5 file
    """
    masses, r_initial, v_initial = ic_data
    # Convert metadata to JSON-serializable format
    metadata_dict = {
        'trajectory_id': metadata.trajectory_id,
        'dataset_type': metadata.dataset_type,
        'fidelity': metadata.fidelity,
        'dt_out': float(metadata.dt_out),
        'set_name': metadata.set_name,
        'filename': metadata.ic_file.name,
        'ic_file_path': str(metadata.ic_file),
        'brutus_file_path': str(metadata.brutus_file)
    }
    
    # Save as HDF5
    with h5py.File(output_path, 'w') as f:
        f.create_dataset('masses', data=masses, compression='gzip')
        f.create_dataset('r_initial', data=r_initial, compression='gzip')
        f.create_dataset('v_initial', data=v_initial, compression='gzip')
        # Store metadata as attributes on the root group
        for key, value in metadata_dict.items():
            f.attrs[key] = value

def save_parsed_brutus(brutus_data: Tuple[np.ndarray, np.ndarray, np.ndarray, Dict],
                       metadata: SimulationMetadata, output_path: Path) -> None:
    """
    Save parsed Brutus data to HDF5 file with attributes for metadata.
    Args:
        brutus_data: Tuple of (times, positions, velocities, brutus_metadata)
        metadata: SimulationMetadata object
        output_path: Path to save the HDF5 file
    """
    times, positions, velocities, brutus_metadata = brutus_data
    # Convert metadata to JSON-serializable format
    metadata_dict = {
        'trajectory_id': metadata.trajectory_id,
        'dataset_type': metadata.dataset_type,
        'fidelity': metadata.fidelity,
        'dt_out': float(metadata.dt_out),
        'set_name': metadata.set_name,
        'filename': metadata.brutus_file.name,
        'ic_file_path': str(metadata.ic_file),
        'brutus_file_path': str(metadata.brutus_file)
    }
    # Add energy conservation data if available
    if brutus_metadata.get('energy_initial') is not None:
        metadata_dict['energy_initial'] = float(brutus_metadata['energy_initial'])
    if brutus_metadata.get('energy_final') is not None:
        metadata_dict['energy_final'] = float(brutus_metadata['energy_final'])
    if brutus_metadata.get('energy_error') is not None:
        metadata_dict['energy_error'] = float(brutus_metadata['energy_error'])

    # Save as HDF5
    with h5py.File(output_path, 'w') as f:
        f.create_dataset('times', data=times, compression='gzip')
        f.create_dataset('positions', data=positions, compression='gzip')
        f.create_dataset('velocities', data=velocities, compression='gzip')
        
        # Add CPU times if available
        cpu_times = brutus_metadata.get('cpu_times', np.array([]))
        if len(cpu_times) > 0:
            f.create_dataset('cpu_times', data=cpu_times, compression='gzip')
        
        # Store metadata as attributes on the root group
        for key, value in metadata_dict.items():
            f.attrs[key] = value

def parse_and_save_individual_files(ic_dir: Path, brutus_dir: Path, 
                                    ic_output_dir: Path, brutus_output_dir: Path, 
                                    max_ic_files: Optional[int] = None, 
                                    max_brutus_files: Optional[int] = None) -> Dict:
    """
    Parse IC and Brutus files individually and save them separately.
    Args:
        ic_dir: Directory containing IC files
        brutus_dir: Directory containing Brutus files
        ic_output_dir: Base output directory for parsed IC files
        brutus_output_dir: Base output directory for parsed Brutus files
        max_ic_files: Maximum number of IC files to process (for testing)
        max_brutus_files: Maximum number of Brutus files to process (for testing)
    Returns:
        Dictionary with processing statistics
    """
    # Create output subdirectories
    ic_output_subdir = ic_output_dir / ic_dir.name
    brutus_output_subdir = brutus_output_dir / brutus_dir.name
    ic_output_subdir.mkdir(parents=True, exist_ok=True)
    brutus_output_subdir.mkdir(parents=True, exist_ok=True)
    
    # Find all IC files
    ic_files = sorted(ic_dir.glob('ic_*.txt'))
    if max_ic_files:
        ic_files = ic_files[:max_ic_files]
    print(f"Found {len(ic_files)} IC files to process")
    
    # Processing statistics
    stats = {
        'total_ic_files': len(ic_files),
        'ic_processed': 0,
        'ic_errors': [],
        'total_brutus_files': 0,
        'brutus_processed': 0,
        'brutus_errors': [],
        'missing_brutus': []
    }
    
    # Process IC files in parallel
    def process_ic(ic_file):
        try:
            ic_name = ic_file.stem
            traj_id = ic_name.replace('ic_', '')
            brutus_name = ic_name.replace('ic_', 'brutus_')
            brutus_file = brutus_dir / f"{brutus_name}.txt"
            if not brutus_file.exists():
                print(f"Warning: No Brutus file for {ic_file.name}")
                return {'missing_brutus': ic_file.name}
            
            # Parse IC
            ic_data = parse_ic_file(ic_file)
            metadata = detect_simulation_metadata(ic_file, brutus_file)
            ic_output_path = ic_output_subdir / f"{ic_name}.h5"
            save_parsed_ic(ic_data, metadata, ic_output_path)
            return {'ic_processed': ic_file.name}
        except Exception as e:
            error_msg = f"Error parsing IC file {ic_file.name}: {e}"
            print(error_msg)
            return {'ic_error': {'file': ic_file.name, 'error': str(e)}}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ic_results = list(executor.map(process_ic, ic_files))
    
    for result in ic_results:
        if 'ic_processed' in result:
            stats['ic_processed'] += 1
        elif 'ic_error' in result:
            stats['ic_errors'].append(result['ic_error'])
        elif 'missing_brutus' in result:
            stats['missing_brutus'].append(result['missing_brutus'])
    
    # Find all Brutus files separately
    brutus_files = sorted(brutus_dir.glob('brutus_*.txt'))
    if max_brutus_files:
        brutus_files = brutus_files[:max_brutus_files]
    stats['total_brutus_files'] = len(brutus_files)
    print(f"Found {len(brutus_files)} Brutus files to process")
    
    # Process Brutus files in parallel
    def process_brutus(brutus_file):
        try:
            brutus_name = brutus_file.stem
            ic_name = brutus_name.replace('brutus_', 'ic_')
            ic_file = ic_dir / f"{ic_name}.txt"
            if not ic_file.exists():
                print(f"Warning: No IC file for {brutus_file.name}")
                return {'missing_ic': brutus_file.name}
            
            # Parse Brutus
            brutus_data = parse_brutus_file(brutus_file)
            metadata = detect_simulation_metadata(ic_file, brutus_file)
            brutus_output_path = brutus_output_subdir / f"{brutus_name}.h5"
            save_parsed_brutus(brutus_data, metadata, brutus_output_path)
            return {'brutus_processed': brutus_file.name}
        except Exception as e:
            error_msg = f"Error parsing Brutus file {brutus_file.name}: {e}"
            print(error_msg)
            return {'brutus_error': {'file': brutus_file.name, 'error': str(e)}}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        brutus_results = list(executor.map(process_brutus, brutus_files))
    
    for result in brutus_results:
        if 'brutus_processed' in result:
            stats['brutus_processed'] += 1
        elif 'brutus_error' in result:
            stats['brutus_errors'].append(result['brutus_error'])
        # Note: 'missing_ic' not tracked in stats, but can be added if needed
    
    return stats

def load_parsed_file(filepath: Path) -> Dict:
    """
    Load a parsed file for inspection/validation.
    Args:
        filepath: Path to the HDF5 file
    Returns:
        Dictionary with parsed data and metadata
    """
    if filepath.suffix == '.pkl':
        # Backward compatibility for pickle files
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    elif filepath.suffix == '.npz':  # Backward compatibility for old npz
        # Load NPZ file
        data = {}
        with np.load(filepath, allow_pickle=True) as npz_file:
            for key in npz_file.files:
                if key == 'metadata':
                    # Parse JSON metadata
                    metadata_json = npz_file[key].item()
                    data['metadata'] = json.loads(metadata_json)
                else:
                    data[key] = npz_file[key]
        return data
    elif filepath.suffix == '.h5':
        # Load HDF5 file
        data = {}
        with h5py.File(filepath, 'r') as f:
            # Load datasets
            for key in f.keys():
                data[key] = f[key][()]  # Load the entire dataset
            # Load metadata from attributes
            data['metadata'] = dict(f.attrs)
        return data
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

def load_parsed_file_pickle(filepath: Path) -> Dict:
    """
    Load a pickle file for backward compatibility.
    Args:
        filepath: Path to the pickle file
    Returns:
        Dictionary with parsed data
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def inspect_parsed_file(filepath: Path, show_data: bool = False) -> None:
    """
    Pretty-print HDF5 file contents for debugging.
    Args:
        filepath: Path to the HDF5 file
        show_data: Whether to show actual data arrays (can be large)
    """
    print(f"\nInspecting: {filepath.name}")
    print("=" * 50)
    if filepath.suffix == '.pkl':
        print("File format: Pickle (binary)")
        data = load_parsed_file_pickle(filepath)
        for key, value in data.items():
            if hasattr(value, 'shape'):
                print(f"  {key}: {type(value).__name__} {value.shape}")
                if show_data and value.size <= 20:
                    print(f"    Data: {value}")
            else:
                print(f"  {key}: {type(value).__name__} = {value}")
        return
    if filepath.suffix == '.npz':  # Backward compatibility
        print("File format: NPZ (NumPy compressed)")
        print(f"File size: {filepath.stat().st_size / 1024:.1f} KB")
        print("\nStructure:")
        with np.load(filepath, allow_pickle=True) as npz_file:
            print(f"  Arrays in file: {list(npz_file.files)}")
            for key in npz_file.files:
                if key == 'metadata':
                    print(f"  {key}: JSON metadata")
                    metadata = json.loads(npz_file[key].item())
                    for meta_key, meta_value in metadata.items():
                        print(f"    {meta_key}: {meta_value}")
                else:
                    array = npz_file[key]
                    print(f"  {key}: {array.dtype} {array.shape}")
                    if show_data and array.size <= 20:
                        print(f"    Data: {array}")
                    elif show_data and len(array.shape) > 0:
                        print(f"    Data: {array.flat[:3]}... (truncated, showing first 3 elements)")
        return

    if filepath.suffix != '.h5':
        print(f"Unsupported file format: {filepath.suffix}")
        return
    print("File format: HDF5")
    print(f"File size: {filepath.stat().st_size / 1024:.1f} KB")
    print("\nStructure:")
    with h5py.File(filepath, 'r') as f:
        print(f"  Datasets: {list(f.keys())}")
        for key in f.keys():
            dataset = f[key]
            print(f"    {key}: {dataset.dtype} {dataset.shape}")
            if show_data and dataset.size <= 20:
                print(f"      Data: {dataset[()]}")
            elif show_data and len(dataset.shape) > 0:
                print(f"      Data: {dataset.flat[:3]}... (truncated, showing first 3 elements)")
        print(f"  Attributes (Metadata):")
        for key, value in f.attrs.items():
            print(f"    {key}: {value}")

def get_h5_summary(filepath: Path) -> Dict:  # Renamed function for HDF5
    """
    Get a summary of HDF5 file contents.
    Args:
        filepath: Path to the HDF5 file
    Returns:
        Dictionary with file summary
    """
    if filepath.suffix != '.h5':
        return {'error': f"Not an HDF5 file: {filepath.suffix}"}
    summary = {
        'filename': filepath.name,
        'size_kb': filepath.stat().st_size / 1024,
        'datasets': {},
        'metadata': {}
    }
    try:
        with h5py.File(filepath, 'r') as f:
            # Get dataset info
            for key in f.keys():
                dataset = f[key]
                summary['datasets'][key] = {
                    'shape': dataset.shape,
                    'dtype': str(dataset.dtype),
                    'size': dataset.size
                }
            # Get attributes (metadata)
            summary['metadata'] = dict(f.attrs)
    except Exception as e:
        summary['error'] = f"Error reading HDF5 file: {e}"
    return summary

def validate_parsed_data(parsed_ic_path: Path, parsed_brutus_path: Path, 
                         original_ic_path: Path, original_brutus_path: Path) -> bool:
    """
    Validate that parsed data matches original files.
    Args:
        parsed_ic_path: Path to parsed IC HDF5 file
        parsed_brutus_path: Path to parsed Brutus HDF5 file  
        original_ic_path: Path to original IC text file
        original_brutus_path: Path to original Brutus text file
    Returns:
        True if validation passes, False otherwise
    """
    try:
        # Load parsed data - Updated to use load_parsed_file for HDF5
        ic_data = load_parsed_file(parsed_ic_path)
        brutus_data = load_parsed_file(parsed_brutus_path)
        # Parse original files again
        orig_ic_masses, orig_ic_pos, orig_ic_vel = parse_ic_file(original_ic_path)
        orig_brutus_times, orig_brutus_pos, orig_brutus_vel, _ = parse_brutus_file(original_brutus_path)
        # Compare IC data
        if not np.allclose(ic_data['masses'], orig_ic_masses, rtol=1e-12):
            print(f"IC masses mismatch in {parsed_ic_path.name}")
            return False
        if not np.allclose(ic_data['r_initial'], orig_ic_pos, rtol=1e-12):
            print(f"IC positions mismatch in {parsed_ic_path.name}")
            return False
        if not np.allclose(ic_data['v_initial'], orig_ic_vel, rtol=1e-12):
            print(f"IC velocities mismatch in {parsed_ic_path.name}")
            return False
        # Compare Brutus data
        if not np.allclose(brutus_data['times'], orig_brutus_times, rtol=1e-12):
            print(f"Brutus times mismatch in {parsed_brutus_path.name}")
            return False
        if not np.allclose(brutus_data['positions'], orig_brutus_pos, rtol=1e-12):
            print(f"Brutus positions mismatch in {parsed_brutus_path.name}")
            return False
        if not np.allclose(brutus_data['velocities'], orig_brutus_vel, rtol=1e-12):
            print(f"Brutus velocities mismatch in {parsed_brutus_path.name}")
            return False
        print(f"Validation passed for {parsed_ic_path.name} and {parsed_brutus_path.name}")
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def main():
    """Main CLI entry point for standalone parsing."""
    parser = argparse.ArgumentParser(
        description='Parse IC and Brutus files individually',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--ic_dir', type=Path, default=None,
                        help=f'Directory containing IC files (default: {DEFAULT_IC_DIR})')
    parser.add_argument('--brutus_dir', type=Path, default=None,
                        help=f'Directory containing Brutus files (default: {DEFAULT_BRUTUS_DIR})')
    parser.add_argument('--ic_output_dir', type=Path, default=None,
                        help=f'Base output directory for parsed IC files (default: {DEFAULT_IC_OUTPUT_DIR})')
    parser.add_argument('--brutus_output_dir', type=Path, default=None,
                        help=f'Base output directory for parsed Brutus files (default: {DEFAULT_BRUTUS_OUTPUT_DIR})')
    parser.add_argument('--max_ic_files', type=int, default=None,
                        help='Maximum number of IC files to process (for testing)')
    parser.add_argument('--max_brutus_files', type=int, default=None,
                        help='Maximum number of Brutus files to process (for testing)')
    parser.add_argument('--validate', action='store_true',
                        help='Validate parsed files against originals')
    parser.add_argument('--validate_count', type=int, default=3,
                        help='Number of files to validate')
    parser.add_argument('--inspect', type=Path, default=None,
                        help='Inspect a specific HDF5 file')
    parser.add_argument('--show_data', action='store_true',
                        help='Show actual data arrays when inspecting (can be large)')
    args = parser.parse_args()
    # Handle inspection mode
    if args.inspect:
        if not args.inspect.exists():
            print(f"Error: File {args.inspect} does not exist")
            return
        inspect_parsed_file(args.inspect, args.show_data)
        return
    # Use default paths if not provided via command line
    ic_dir = args.ic_dir if args.ic_dir is not None else DEFAULT_IC_DIR
    brutus_dir = args.brutus_dir if args.brutus_dir is not None else DEFAULT_BRUTUS_DIR
    ic_output_dir = args.ic_output_dir if args.ic_output_dir is not None else DEFAULT_IC_OUTPUT_DIR
    brutus_output_dir = args.brutus_output_dir if args.brutus_output_dir is not None else DEFAULT_BRUTUS_OUTPUT_DIR
    # Validate input directories
    if not ic_dir.exists():
        print(f"Error: IC directory {ic_dir} does not exist")
        return
    if not brutus_dir.exists():
        print(f"Error: Brutus directory {brutus_dir} does not exist")
        return
    # Create output directories
    ic_output_dir.mkdir(parents=True, exist_ok=True)
    brutus_output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Processing files from:")
    print(f"  IC directory: {ic_dir}")
    print(f"  Brutus directory: {brutus_dir}")
    print(f"  IC Output directory: {ic_output_dir}")
    print(f"  Brutus Output directory: {brutus_output_dir}")
    if args.max_ic_files:
        print(f"  Max IC files: {args.max_ic_files}")
    else:
        print(f"  Max IC files: {DEFAULT_MAX_IC_FILES_FOR_TESTING} (default testing limit)")
    if args.max_brutus_files:
        print(f"  Max Brutus files: {args.max_brutus_files}")
    else:
        print(f"  Max Brutus files: {DEFAULT_MAX_BRUTUS_FILES_FOR_TESTING} (default testing limit)")
    print()
    # Process files - use default testing limit if not specified
    max_ic_to_process = args.max_ic_files if args.max_ic_files is not None else DEFAULT_MAX_IC_FILES_FOR_TESTING
    max_brutus_to_process = args.max_brutus_files if args.max_brutus_files is not None else DEFAULT_MAX_BRUTUS_FILES_FOR_TESTING
    stats = parse_and_save_individual_files(
        ic_dir, brutus_dir, ic_output_dir, brutus_output_dir, max_ic_to_process, max_brutus_to_process
    )
    # Print summary
    print(f"\nProcessing Summary:")
    print(f"  Total IC files found: {stats['total_ic_files']}")
    print(f"  IC files processed: {stats['ic_processed']}")
    print(f"  Total Brutus files found: {stats['total_brutus_files']}")
    print(f"  Brutus files processed: {stats['brutus_processed']}")
    print(f"  Missing Brutus files: {len(stats['missing_brutus'])}")
    print(f"  IC parsing errors: {len(stats['ic_errors'])}")
    print(f"  Brutus parsing errors: {len(stats['brutus_errors'])}")
    # Save detailed statistics
    stats_file = ic_output_dir.parent / 'parsing_stats.json'  # Save at common parent
    with open(stats_file, 'w') as f:
        # Convert Path objects to strings for JSON serialization
        json_stats = {
            'total_ic_files': stats['total_ic_files'],
            'ic_processed': stats['ic_processed'],
            'total_brutus_files': stats['total_brutus_files'],
            'brutus_processed': stats['brutus_processed'],
            'missing_brutus': stats['missing_brutus'],
            'ic_errors': stats['ic_errors'],
            'brutus_errors': stats['brutus_errors']
        }
        json.dump(json_stats, f, indent=2)
    print(f"\nDetailed statistics saved to: {stats_file}")
    # Validation if requested
    if args.validate and stats['ic_processed'] > 0 and stats['brutus_processed'] > 0:
        print(f"\nValidating {args.validate_count} parsed files...")
        ic_output_subdir = ic_output_dir / ic_dir.name
        brutus_output_subdir = brutus_output_dir / brutus_dir.name
        # Get list of successfully parsed files
        ic_files = sorted(ic_output_subdir.glob('*.h5'))[:args.validate_count]
        validation_results = []
        for ic_file in ic_files:
            # Find corresponding brutus file
            ic_name = ic_file.stem
            brutus_name = ic_name.replace('ic_', 'brutus_')
            brutus_file = brutus_output_subdir / f"{brutus_name}.h5"
            if brutus_file.exists():
                # Find original files
                orig_ic = ic_dir / f"{ic_name}.txt"
                orig_brutus = brutus_dir / f"{brutus_name}.txt"
                if orig_ic.exists() and orig_brutus.exists():
                    result = validate_parsed_data(ic_file, brutus_file, orig_ic, orig_brutus)
                    validation_results.append(result)
        passed = sum(validation_results)
        total = len(validation_results)
        print(f"Validation results: {passed}/{total} files passed")
    print("\nParsing complete!")

if __name__ == '__main__':
    main()
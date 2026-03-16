#!/usr/bin/env python3
"""
Brutus Batch Runner for macOS — Revised version

Processes both hierarchical and standard quasi-random initial conditions (ICs)
with separate Brutus parameters. Validates output completeness and moves
problematic ICs to dedicated folders.

Workflow:
1. Generate ICs using generate_enhanced_ics.py
2. Run stage2_prescreening_revised_auto.py to prescreen ICs
3. Run this script to execute Brutus simulations
4. Use calculate_brutus_metrics.py to extract metrics
"""

import subprocess
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from datetime import datetime
import shutil
import re

# --- CONFIGURATION ---
# Control how many ICs are processed per run
HIERARCHICAL_ICS_PER_RUN = 10   # Max hierarchical ICs to process per run
STANDARD_ICS_PER_RUN = 0    # Max standard ICs to process per run
TIMEOUT_SECONDS = 3000          # Timeout for each simulation (50 minutes)

# Base directory
BASE_DIR = Path("<home>/Desktop/cursor/simulation_data")
BRUTUS_EXEC = Path("<home>/Desktop/cursor/brutus_Newton-main/brutus")

# Input/output directories
IC_DIRS = {
    "hierarchical": BASE_DIR / "Data" / "ic_final" / "ic_hierarchical",
    "standard": BASE_DIR / "Data" / "ic_final" / "ic_standard_quasi_random"
}
OUTPUT_DIRS = {
    "hierarchical": BASE_DIR / "Data" / "brutus_output" / "brutus_hierarchical",
    "standard": BASE_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random"
}

# Problematic IC directories
PROBLEMATIC_DIRS = {
    "hierarchical": BASE_DIR / "Documentation" / "problematic_ics" / "hierarchical",
    "standard": BASE_DIR / "Documentation" / "problematic_ics" / "standard"
}

# Brutus parameters
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

LINE_COUNT_THRESHOLDS = {
    "hierarchical": (600, 700),  # Hierarchical: 600–700 lines (~150–175 clusters)
    "standard": (250, 350)       # Standard: 300–350 lines (~75–87 clusters)
}



# --- VALIDATION LOGIC ---

def validate_brutus_output(output_path: Path, time_threshold: float = 9.5) -> tuple[bool, str]:
    """
    Validates Brutus output files by checking:
    - File existence
    - Final timestep reaches threshold (~10)
    
    Args:
        output_path: Path to the Brutus output file
        time_threshold: Minimum time value for complete simulation (default: 9.5)
    
    Returns:
        tuple: (is_valid, reason_message)
    """
    
    # Check if file exists
    if not output_path.exists():
        return False, "Output file does not exist"

    try:
        # Pattern to match timestep lines: [time] 3 [cpu_time]
        timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
        
        with open(output_path, 'r') as f:
            lines = f.readlines()
        
        # Find all timestep lines
        timestep_values = []
        for line in lines:
            match = timestep_pattern.match(line.strip())
            if match:
                time_value = float(match.group(1))
                timestep_values.append(time_value)
        
        # Check if any timestep lines were found
        if not timestep_values:
            return False, "No timestep lines found in output"
        
        # Get the final timestep
        final_timestep = timestep_values[-1]
        
        # Check if simulation reached completion
        if final_timestep < time_threshold:
            return False, f"Incomplete simulation (final time: {final_timestep:.3f}, threshold: {time_threshold})"
        
        return True, f"Validation successful (final time: {final_timestep:.3f})"

    except Exception as e:
        return False, f"Error reading/validating file: {e}"

'''
old version
def validate_brutus_output(output_path: Path) -> tuple[bool, str]:
    """
    Validates Brutus output files by checking:
    - No error keywords
    - Sufficient line count (based on simulation type)
    """
    if not output_path.exists():
        return False, "Output file does not exist"

    try:
        with open(output_path, 'r') as f:
            lines = f.read().strip().split('\n')  # Splits on newline, including empty lines

        # Check for error keywords
        error_indicators = ["error", "fail", "timeout", "segmentation fault", "killed"]
        for line in lines:
            if any(indicator in line.lower() for indicator in error_indicators):
                return False, f"Found error keyword in output: {line}"

        # Check line count
        sim_type = "hierarchical" if "hierarchical" in str(output_path) else "standard"
        min_lines, max_lines = LINE_COUNT_THRESHOLDS[sim_type]
        line_count = len(lines)
        if line_count < min_lines or line_count > max_lines:
            return False, f"Invalid line count ({line_count} lines). Expected {min_lines}-{max_lines}."

        return True, "Validation successful"

    except Exception as e:
        return False, f"Validation error: {e}"
'''




# --- SIMULATION LOGIC ---
def run_simulation(input_file, output_dir, sim_type):
    """
    Runs a single Brutus simulation, validates output, and handles failures.
    """
    file_num = input_file.stem.split('_')[-1]
    output_filename = f"brutus_{sim_type}_{file_num}.txt"
    output_path = output_dir / output_filename
    problem_dir = PROBLEMATIC_DIRS[sim_type]

    # Skip if valid output already exists
    if output_path.exists():
        is_valid, reason = validate_brutus_output(output_path)
        if is_valid:
            return (input_file.name, True, "Already valid", 0)

    # Get parameters for this simulation type
    params = BRUTUS_PARAMS[sim_type]
    cmd = [str(BRUTUS_EXEC),
           params['tolerance'],
           params['word_length'],
           params['t_begin'],
           params['t_end'],
           params['dt_out'],
           params['n_particles'],
           str(input_file)]

    start_time = time.time()

    # Announce simulation start
    print(f"▶️  Starting {sim_type.upper()} simulation for {input_file.name}", flush=True)

    success = False
    result_message = ""

    try:
        with open(output_path, 'w') as outfile:
            subprocess.run(
                cmd,
                stdout=outfile,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=TIMEOUT_SECONDS,
                check=True
            )
        is_valid, reason = validate_brutus_output(output_path)
        if is_valid:
            success = True
            result_message = "Success"
        else:
            result_message = f"Invalid output ({reason})"
    
    except subprocess.TimeoutExpired:
        result_message = "Timeout"
    except subprocess.CalledProcessError as e:
        result_message = f"Error (code {e.returncode})"
    except Exception as e:
        result_message = f"Unexpected error: {str(e)}"

    wall_time = time.time() - start_time

    if not success:
        # Move IC to problematic directory
        problem_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(input_file), str(problem_dir / input_file.name))
            result_message += f". Moved IC to '{problem_dir.name}'"
        except Exception as e:
            result_message += f". Failed to move IC: {e}"
        # Clean up partial output
        if output_path.exists():
            output_path.unlink()

    status_icon = "✅" if success else "❌"
    return (input_file.name, success, f"{result_message} in {wall_time:.1f}s", wall_time)


# --- DIRECTORY PROCESSING ---
def process_directory(sim_type, ic_dir, output_dir, max_files):
    """
    Processes up to `max_files` ICs of a given type, starting from the lowest-numbered.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    problem_dir = PROBLEMATIC_DIRS[sim_type]

    # Build blacklist of problematic ICs
    blacklisted_numbers = set()
    for f in problem_dir.glob(f"ic_{sim_type}_*.txt"):
        try:
            num = int(f.stem.split('_')[-1])
            blacklisted_numbers.add(num)
        except (ValueError, IndexError):
            continue

    # Get all potential IC files
    try:
        all_potential_files = sorted(
            [f for f in ic_dir.iterdir() if f.suffix == '.txt' and f.is_file()],
            key=lambda f: int(f.stem.split('_')[-1]) if f.stem.split('_')[-1].isdigit() else 0
        )
    except Exception as e:
        print(f"Error reading {ic_dir}: {e}")
        return 0, 0

    # Filter files needing processing
    files_to_process = []
    skipped_blacklist = 0
    skipped_valid = 0

    for f in all_potential_files:
        try:
            file_num_str = f.stem.split('_')[-1]
            file_num = int(file_num_str)
            
            # Check if output already exists and is valid
            output_path = output_dir / f"brutus_{sim_type}_{file_num_str}.txt"
            if output_path.exists():
                is_valid, _ = validate_brutus_output(output_path)
                if is_valid:
                    skipped_valid += 1
                    continue
            
            # Check if in blacklist
            if file_num in blacklisted_numbers:
                skipped_blacklist += 1
                continue
                
            files_to_process.append(f)
        except (ValueError, IndexError):
            continue
    
    files_to_process = files_to_process[:max_files]

    # --- DIAGNOSTICS ---
    print(
        f"Found {len(files_to_process)} {sim_type.upper()} ICs to process "
        f"(skipped {skipped_valid} already valid, {skipped_blacklist} black-listed)"
    )

    if not files_to_process:
        print(f"✓ No new ICs to process for {sim_type}")
        return 0, 0

    '''
    for f in all_potential_files:
        try:    
            file_num_str = f.stem.split('_')[-1]
            file_num = int(file_num_str)

            # NEW: skip ICs with already-trusted outputs
            if file_num <= PREVALIDATED_MAX_ID.get(sim_type, -1):
                output_path = output_dir / f"brutus_{sim_type}_{file_num_str}.txt"
                if output_path.exists():
                    skipped_valid += 1
                    continue

            if file_num in blacklisted_numbers:
                skipped_blacklist += 1
                continue
            files_to_process.append(f)
        except (ValueError, IndexError):
            continue

    '''

    # Parallel execution
    num_cpus = max(1, multiprocessing.cpu_count() - 1)
    print(f"Processing {sim_type.upper()} ICs ({len(files_to_process)} files)")
    print(f"Using {num_cpus} parallel processes")
    print(f"Brutus params: tol={BRUTUS_PARAMS[sim_type]['tolerance']}, wordlen={BRUTUS_PARAMS[sim_type]['word_length']}")
    print("-" * 80)

    start_time = time.time()
    completed = 0
    successful = 0
    total_sim_time = 0

    with ProcessPoolExecutor(max_workers=num_cpus) as executor:
        futures = {
            executor.submit(run_simulation, f, output_dir, sim_type): f
            for f in files_to_process
        }
        for future in as_completed(futures):
            completed += 1
            filename, success, message, sim_time = future.result()
            if success:
                successful += 1
                total_sim_time += sim_time
            progress_pct = (completed / len(files_to_process)) * 100
            status_icon = "✅" if success else "❌"
            print(f"[{completed}/{len(files_to_process)}] {status_icon} {filename}: {message} | Progress: {progress_pct:.1f}%")

    total_time = time.time() - start_time
    print("-" * 80)
    print(f"COMPLETED {sim_type.upper()}: {successful}/{completed} success in {total_time/60:.1f} minutes")
    return successful, total_time


# --- MAIN FUNCTION ---
def main():
    print("Brutus Batch Simulation Runner (Revised for macOS)")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Brutus executable: {BRUTUS_EXEC}")
    print("=" * 80)

    if not BRUTUS_EXEC.exists():
        print(f"ERROR: Brutus executable not found at {BRUTUS_EXEC}")
        return

    total_start = time.time()

    print("\n" + "=" * 80)
    print("PHASE 1: HIERARCHICAL INITIAL CONDITIONS")
    print("=" * 80)
    hier_success, hier_time = process_directory(
        "hierarchical",
        IC_DIRS["hierarchical"],
        OUTPUT_DIRS["hierarchical"],
        HIERARCHICAL_ICS_PER_RUN
    )

    print("\n" + "=" * 80)
    print("PHASE 2: STANDARD QUASI-RANDOM INITIAL CONDITIONS")
    print("=" * 80)
    std_success, std_time = process_directory(
        "standard",
        IC_DIRS["standard"],
        OUTPUT_DIRS["standard"],
        STANDARD_ICS_PER_RUN
    )

    total_time = time.time() - total_start
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {total_time/60:.1f} minutes")
    print(f"Total simulations completed: {hier_success + std_success}")
    print(f"• Hierarchical: {hier_success} in {hier_time/60:.1f} min")
    print(f"• Standard: {std_success} in {std_time/60:.1f} min")
    print("=" * 80)


if __name__ == "__main__":
    main()
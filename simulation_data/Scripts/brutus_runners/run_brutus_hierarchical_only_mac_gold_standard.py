#!/usr/bin/env python3

"""

##############################################################
First check out the things to do on window's script (made a note there);
lower the precision/tolerance of this script and test how long it'll run
Don't forget to copy and past the brutus output files to another folder to save them for now
Move back those timed-out ICs from yerterday's run because they're moved probably because it's taking them
too long, and so lowering the tolerance can help with that
For new runs, remember to fix the bug first and then run rhe script again. You can first check if those
moved-backed ICs from the blacklist will successfully run. Then continue with the rest.

<home>/Desktop/cursor/brutus_Newton-main/Brutus.cpp

Later this file can be modified to run for the coarser ICs with dt=0.08. Same with the window's script

"""

import time
import shutil
import multiprocessing
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import re

# Paths
BASE_DIR = Path("<home>/Desktop/cursor")
BRUTUS_EXEC = BASE_DIR / "brutus_Newton-main" / "brutus"
PROBLEM_DIR = BASE_DIR / "simulation_data"

# Input and output directories
IC_DIR = PROBLEM_DIR / "Data" / "ic_final" / "ic_hierarchical_for_gold_standard"
OUTPUT_DIR = PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard"
PROBLEMATIC_DIR = PROBLEM_DIR / "Documentation" / "problematic_ics" / "hierarchical_for_gold_standard"

# Brutus parameters for hierarchical simulations
BRUTUS_PARAMS = {
    "tolerance": "1e-13",
    "word_length": "130",
    "t_begin": "0",
    "t_end": "10",
    "dt_out": "0.01",
    "n_particles": "3"
}

# Number of ICs to process per run (configurable)
ICS_PER_RUN = 1000


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


def run_simulation(input_file: Path):
    """
    Runs a single hierarchical simulation with 50-minute timeout.
    Validates output and handles failures.
    """
    file_num_str = input_file.stem.split('_')[-1]
    output_filename = f"brutus_hierarchical_{file_num_str}.txt"
    output_path = OUTPUT_DIR / output_filename

    print(f"🚀 STARTING: {input_file.name} -> {output_filename}")

    cmd = [
        str(BRUTUS_EXEC),
        BRUTUS_PARAMS['tolerance'],
        BRUTUS_PARAMS['word_length'],
        BRUTUS_PARAMS['t_begin'],
        BRUTUS_PARAMS['t_end'],
        BRUTUS_PARAMS['dt_out'],
        BRUTUS_PARAMS['n_particles'],
        str(input_file)
    ]

    start = time.time()
    success = False
    result_message = ''

    try:
        from subprocess import run, TimeoutExpired
        run(cmd, stdout=open(output_path, 'w'), stderr=open(output_path, 'a'), timeout=50*60, check=True)
        is_valid, validation_message = validate_brutus_output(output_path)
        if is_valid:
            success = True
            result_message = 'Validation passed'
        else:
            result_message = f'Validation failed: {validation_message}'
    except TimeoutExpired:
        result_message = 'Timed out'
    except Exception as e:
        result_message = f'Error: {e}'

    wall_time = time.time() - start

    if not success:
        try:
            PROBLEMATIC_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(input_file), str(PROBLEMATIC_DIR / input_file.name))
            result_message += f". Moved Problematic IC to '{PROBLEMATIC_DIR.name}'"
        except Exception as e:
            result_message += f". Failed to move IC: {e}"

        if output_path.exists():
            output_path.unlink()

    status_icon = '✅' if success else '❌'
    print(f"{status_icon} FINISHED: {input_file.name} - {result_message} in {wall_time:.1f}s")

    return input_file.name, success, f"{result_message} in {wall_time:.1f}s"


def process_hierarchical_ics():
    """
    Processes up to ICS_PER_RUN hierarchical ICs, starting from the lowest
    numbered IC that hasn't been processed.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBLEMATIC_DIR.mkdir(parents=True, exist_ok=True)

    blacklisted_numbers = set()
    for f in PROBLEMATIC_DIR.glob("ic_hierarchical_*.txt"):
        try:
            num = int(f.stem.split('_')[-1])
            blacklisted_numbers.add(num)
        except (ValueError, IndexError):
            continue
    print(f"Found {len(blacklisted_numbers)} blacklisted ICs in '{PROBLEMATIC_DIR.name}'")

    try:
        all_potential_files = sorted(
            [f for f in IC_DIR.iterdir() if f.suffix == '.txt' and f.is_file()],
            key=lambda f: int(f.stem.split('_')[-1])
        )
    except (ValueError, IndexError):
        print(f"Error: Could not sort files in {IC_DIR}. Check filenames.")
        return 0

    available_files = []
    skipped_blacklist = 0
    skipped_valid = 0

    for f in all_potential_files:
        try:
            file_num_str = f.stem.split('_')[-1]
            file_num = int(file_num_str)

            if file_num in blacklisted_numbers:
                skipped_blacklist += 1
                continue

            output_filename = f"brutus_hierarchical_{file_num_str}.txt"
            output_path = OUTPUT_DIR / output_filename
            is_valid, _ = validate_brutus_output(output_path)
            if is_valid:
                skipped_valid += 1
                continue

            available_files.append(f)
        except (ValueError, IndexError):
            continue

    print(f"Total ICs found: {len(all_potential_files)}")
    print(f"Skipping {skipped_blacklist} blacklisted ICs.")
    print(f"Skipping {skipped_valid} ICs with existing valid outputs.")
    print(f"Available for processing: {len(available_files)}")

    if not available_files:
        print("✓ No new ICs to process for hierarchical.")
        return 0

    files_to_process = available_files[:ICS_PER_RUN]
    first_num = int(files_to_process[0].stem.split('_')[-1])
    last_num = int(files_to_process[-1].stem.split('_')[-1])
    print(f"\nProcessing ICs {first_num:04d} to {last_num:04d} ({len(files_to_process)} files)")
    print(f"Files to process: {len(files_to_process)}")

    num_cpus = max(1, multiprocessing.cpu_count() - 1)
    print(f"Using {num_cpus} parallel processes.")
    print(f"Brutus params: t=[{BRUTUS_PARAMS['t_begin']},{BRUTUS_PARAMS['t_end']}], dt={BRUTUS_PARAMS['dt_out']}, tolerance={BRUTUS_PARAMS['tolerance']}, word_length={BRUTUS_PARAMS['word_length']}")
    print("-" * 80)

    start_time = time.time()
    completed = 0
    successful = 0

    with ProcessPoolExecutor(max_workers=num_cpus) as executor:
        futures = {executor.submit(run_simulation, f): f for f in files_to_process}
        for future in as_completed(futures):
            completed += 1
            _, success, _ = future.result()
            if success:
                successful += 1
            progress_pct = (completed / len(files_to_process)) * 100
            success_rate = (successful / completed) * 100 if completed > 0 else 0
            print(f"📊 PROGRESS: [{completed:3d}/{len(files_to_process)}] ({progress_pct:5.1f}%) completed | Success: {successful}/{completed} ({success_rate:.1f}%)")

    total_time = time.time() - start_time
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {total_time/3600:.2f} hours ({total_time/60:.1f} minutes)")
    print(f"Successfully completed: {successful} simulations")
    print(f"Input directory: {IC_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Problematic ICs moved to: {PROBLEMATIC_DIR}")
    print("\n" + "=" * 80)


def main():
    """Main function to orchestrate the simulation process."""
    print("=" * 80)
    print(f"Brutus Batch Runner - Hierarchical ICs ({ICS_PER_RUN} per run)")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Brutus executable: {BRUTUS_EXEC}")
    print("=" * 80)

    if not BRUTUS_EXEC.exists():
        print(f"FATAL ERROR: Brutus executable not found at '{BRUTUS_EXEC}'")
        return

    process_hierarchical_ics()


if __name__ == "__main__":
    main() 
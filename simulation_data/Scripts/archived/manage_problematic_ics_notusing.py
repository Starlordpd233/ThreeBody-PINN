#!/usr/bin/env python3
"""
The purpose of this script is to avoid BRUTUS from running on the same problematic ICs (from last run)
that will likely result in a timeout again. Correct?
 
Manage problematic IC files that timeout or fail during ****LAST RUN**** of Brutus simulations
- Only checks files that have been attempted (up to a specified number)
- Maintains a blacklist of problematic files
- Option to delete or move problematic files

"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

# Directories
BASE_DIR = Path("<home>/Desktop/cursor/simulation_data")
IC_DIRS = {
    "hierarchical": BASE_DIR / "Data" / "ic_final" / "ic_hierarchical",
    "standard": BASE_DIR / "Data" / "ic_final" / "ic_standard_quasi_random"
}
BRUTUS_DIRS = {
    "hierarchical": BASE_DIR / "brutus_output" / "brutus_hierarchical",
    "standard": BASE_DIR / "brutus_output" / "brutus_standard_quasi_random"
}

# Blacklist file to track problematic ICs
BLACKLIST_FILE = BASE_DIR / "problematic_ics_blacklist.json"

# Track progress file
PROGRESS_FILE = BASE_DIR / "brutus_progress.json"

# Directory to move problematic files (optional)
PROBLEMATIC_DIR = BASE_DIR / "problematic_ics"

def load_progress():
    """Load the progress tracking file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"hierarchical": {"last_attempted": -1}, "standard": {"last_attempted": -1}}

def save_progress(progress):
    """Save the progress tracking file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_blacklist():
    """Load the blacklist of problematic IC files."""
    if BLACKLIST_FILE.exists():
        with open(BLACKLIST_FILE, 'r') as f:
            return json.load(f)
    return {"hierarchical": [], "standard": []}

def save_blacklist(blacklist):
    """Save the blacklist of problematic IC files."""
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(blacklist, f, indent=2)

def validate_brutus_output(brutus_file):
    """
    Check if a brutus output file is valid and complete.
    Returns True if valid, False if problematic.
    """
    if not brutus_file.exists():
        return False
    
    try:
        # Read the file to check for common issues
        with open(brutus_file, 'r') as f:
            content = f.read()
        
        # Check if file is empty or nearly empty
        if len(content.strip()) < 100:
            
            return False
        
        # Check for common error indicators
        error_indicators = [
            "Error",
            "error",
            "ERROR",
            "Failed",
            "failed",
            "FAILED",
            "Timeout",
            "timeout",
            "TIMEOUT",
            "Segmentation fault",
            "segmentation fault",
            "core dumped",
            "Killed",
            "killed"
        ]
        
        for indicator in error_indicators:
            if indicator in content:
                return False
        
        # Check if file has proper structure (should have multiple lines with numbers)
        lines = content.strip().split('\n')
        if len(lines) < 5:  # Should have at least 5 lines for a proper simulation
            return False
        
        # PRIMARY CHECK: Verify simulation reached the target end time of 10 time units
        # Find all time header lines (format: "time 3 parameter")
        time_lines = []
        for line in lines:
            line = line.strip()
            if ' 3 ' in line and not line.startswith('1 '):  # Time header, not particle data
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        time_value = float(parts[0])
                        time_lines.append(time_value)
                    except ValueError:
                        continue
        
        if not time_lines:
            return False  # No time data found
        
        # Check if simulation reached close to the target time of 10.0
        final_time = max(time_lines)
        TARGET_END_TIME = 10.0
        MIN_COMPLETION_TIME = 9.5  # Allow some tolerance for near-complete simulations
        
        if final_time < MIN_COMPLETION_TIME:
            return False  # Simulation didn't reach completion - likely timeout
        
        # SECONDARY CHECK: File size (but only if time check failed)
        # If we got here, the simulation reached completion time, so it's likely valid
        file_size = brutus_file.stat().st_size
        if file_size < 200:  # Very small files are still suspicious
            return False
        
        # Check if the file has some numerical data structure
        numerical_lines = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip comments
                # Count lines that look like numerical data
                parts = line.split()
                if len(parts) >= 3:  # Should have at least 3 numbers per line
                    try:
                        # Try to parse some numbers to verify it's numerical data
                        float(parts[0])
                        float(parts[1])
                        numerical_lines += 1
                    except ValueError:
                        continue
        
        # Should have some numerical data lines
        if numerical_lines < 3:
            return False
        
        return True
        
    except Exception as e:
        # If we can't read the file or any other error, consider it problematic
        return False

def find_problematic_files(sim_type, max_num):
    """Find IC files that don't have corresponding brutus output files OR have problematic outputs."""
    ic_dir = IC_DIRS[sim_type]
    brutus_dir = BRUTUS_DIRS[sim_type]
    
    # Get IC files up to max_num
    ic_files = set()
    for f in ic_dir.glob(f"ic_{sim_type}_*.txt"):
        try:
            num = int(f.stem.split('_')[-1])
            if num <= max_num:
                ic_files.add(num)
        except ValueError:
            continue
    
    # Get brutus output files up to max_num
    brutus_files = set()
    for f in brutus_dir.glob(f"brutus_{sim_type}_*.txt"):
        try:
            num = int(f.stem.split('_')[-1])
            if num <= max_num:
                brutus_files.add(num)
        except ValueError:
            continue
    
    # Find missing files (no output at all)
    missing = sorted(ic_files - brutus_files)
    
    # NEW: Also find files with problematic/incomplete outputs
    problematic_existing = []
    for num in sorted(ic_files & brutus_files):  # Files that have both IC and output
        brutus_file = brutus_dir / f"brutus_{sim_type}_{num:04d}.txt"
        if not validate_brutus_output(brutus_file):
            problematic_existing.append(num)
    
    # Combine missing and problematic existing files
    all_problematic = sorted(missing + problematic_existing)
    
    return ic_files, brutus_files, all_problematic, missing, problematic_existing

def handle_problematic_files(sim_type, problematic_nums, action="move"):
    """Handle problematic IC files by moving or deleting them."""
    ic_dir = IC_DIRS[sim_type]
    handled = []
    
    if action == "move":
        # Create problematic directory if it doesn't exist
        problematic_type_dir = PROBLEMATIC_DIR / sim_type
        problematic_type_dir.mkdir(parents=True, exist_ok=True)
    
    for num in problematic_nums:
        ic_file = ic_dir / f"ic_{sim_type}_{num:04d}.txt"
        if ic_file.exists():
            if action == "delete":
                ic_file.unlink()
                print(f"  Deleted: {ic_file.name}")
            elif action == "move":
                dest = problematic_type_dir / ic_file.name
                shutil.move(str(ic_file), str(dest))
                print(f"  Moved: {ic_file.name} -> {dest}")
            handled.append(num)
    
    return handled

def get_user_input_number(prompt, default=None):
    """Get a number from user input with optional default."""
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    
    while True:
        user_input = input(prompt).strip()
        if not user_input and default is not None:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("Problematic IC File Manager")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load existing data
    blacklist = load_blacklist()
    progress = load_progress()
    
    # Process both simulation types
    for sim_type in ["hierarchical", "standard"]:
        print(f"\n{sim_type.upper()} Simulations")
        print("-" * 40)
        
        # Get the range of files that have been attempted
        last_attempted = progress[sim_type]["last_attempted"]
        
        print(f"Last recorded attempt: up to {last_attempted:04d}")
        max_num = get_user_input_number(
            f"Enter the highest {sim_type} IC number you've attempted to process",
            default=last_attempted if last_attempted >= 0 else None
        )
        
        if max_num < 0:
            print("Skipping this simulation type.")
            continue
        
        # Update progress
        progress[sim_type]["last_attempted"] = max_num
        save_progress(progress)
        
        # Find missing outputs only up to the attempted range
        ic_files, brutus_files, all_problematic, missing, problematic_existing = find_problematic_files(sim_type, max_num)
        
        print(f"\nChecking files 0000-{max_num:04d}:")
        print(f"  IC files in range: {len(ic_files)}")
        print(f"  Brutus outputs in range: {len(brutus_files)}")
        print(f"  Missing outputs: {len(missing)}")
        print(f"  Problematic existing outputs: {len(problematic_existing)}")
        
        if all_problematic:
            print(f"\nProblematic files for {sim_type}:")
            if missing:
                print(f"  Missing outputs ({len(missing)} files):")
                for num in missing:
                    print(f"    {num:04d} - ic_{sim_type}_{num:04d}.txt (no output)")
            
            if problematic_existing:
                print(f"  Problematic existing outputs ({len(problematic_existing)} files):")
                for num in problematic_existing:
                    print(f"    {num:04d} - ic_{sim_type}_{num:04d}.txt (incomplete/timeout/error)")
            
            # Check which ones are already in blacklist
            new_problematic = [num for num in all_problematic if num not in blacklist[sim_type]]
            
            if new_problematic:
                print(f"\nNew problematic files detected: {len(new_problematic)}")
                print("These files were attempted but produced no output or problematic output.")
                print("Automatically moving files to problematic_ics directory and updating blacklist...")
                
                # Update blacklist
                blacklist[sim_type].extend(new_problematic)
                blacklist[sim_type] = sorted(list(set(blacklist[sim_type])))
                
                # Move files and clean up outputs
                handled = handle_problematic_files(sim_type, new_problematic, "move")
                print(f"Moved {len(handled)} IC files")
                
                # Also remove problematic existing output files
                if problematic_existing:
                    removed_outputs = []
                    for num in new_problematic:
                        if num in problematic_existing:
                            output_file = BRUTUS_DIRS[sim_type] / f"brutus_{sim_type}_{num:04d}.txt"
                            if output_file.exists():
                                output_file.unlink()
                                removed_outputs.append(num)
                    if removed_outputs:
                        print(f"Also removed {len(removed_outputs)} problematic output files")
                
                save_blacklist(blacklist)
                print("Blacklist updated")
            else:
                print("\nAll problematic files are already in the blacklist.")
        else:
            print("\n✓ All attempted files have valid brutus outputs!")
    
    # Show current blacklist
    print("\n" + "=" * 60)
    print("CURRENT BLACKLIST:")
    for sim_type in ["hierarchical", "standard"]:
        if blacklist[sim_type]:
            print(f"\n{sim_type}: {len(blacklist[sim_type])} files")
            for num in sorted(blacklist[sim_type])[:10]:  # Show first 10
                print(f"  ic_{sim_type}_{num:04d}.txt")
            if len(blacklist[sim_type]) > 10:
                print(f"  ... and {len(blacklist[sim_type]) - 10} more")
    
    # Save report
    report_file = BASE_DIR / f"problematic_ics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(f"Problematic IC Files Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("Progress Tracking:\n")
        for sim_type in ["hierarchical", "standard"]:
            f.write(f"  {sim_type}: attempted up to {progress[sim_type]['last_attempted']:04d}\n")
        f.write("\n")
        
        for sim_type in ["hierarchical", "standard"]:
            f.write(f"{sim_type.upper()} Simulations\n")
            f.write("-" * 40 + "\n")
            f.write(f"Blacklisted files: {len(blacklist[sim_type])}\n")
            if blacklist[sim_type]:
                for num in sorted(blacklist[sim_type]):
                    f.write(f"  ic_{sim_type}_{num:04d}.txt\n")
            f.write("\n")
    
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    main()

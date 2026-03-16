#!/usr/bin/env python3
"""
Script to check brutus output files for completeness.
Uses the final timestep value to determine if simulations completed successfully.
Supports both 'hierarchical' and 'standard' file naming patterns.
"""

import os
import re
import glob

def check_brutus_completeness(directory_path, file_type="hierarchical", time_threshold=9.5, min_file_number=None):
    """
    Check brutus output files for completeness based on final timestep.
    
    Args:
        directory_path (str): Path to directory containing brutus output files
        file_type (str): Type of files to check ('hierarchical' or 'standard')
        time_threshold (float): Minimum time value for complete simulation (default: 9.5)
        min_file_number (int): Only check files with numbers >= this value (default: None for all files)
    
    Returns:
        tuple: (incomplete_files, complete_files, missing_timestep_files) - lists of (file_number, final_time) or file_numbers
    """
    
    if file_type not in ["hierarchical", "standard"]:
        raise ValueError("file_type must be 'hierarchical' or 'standard'")
    
    # Set pattern based on file_type
    pattern_prefix = f"brutus_{file_type}_"
    file_pattern = os.path.join(directory_path, f"{pattern_prefix}*.txt")
    regex_pattern = re.compile(rf'{pattern_prefix}(\d+)\.txt')
    
    # Pattern to match timestep lines: [time] 3 [cpu_time]
    timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
    
    incomplete_files = []
    complete_files = []
    missing_timestep_files = []
    
    # Find all matching brutus output files
    files = glob.glob(file_pattern)
    
    print(f"Checking {len(files)} {file_type} files in: {directory_path}")
    print(f"Time threshold for completion: {time_threshold}")
    print("-" * 50)
    
    for file_path in sorted(files):
        # Extract file number from filename
        filename = os.path.basename(file_path)
        match = regex_pattern.search(filename)
        if not match:
            print(f"Skipping non-matching file: {filename}")
            continue
            
        file_number = int(match.group(1))
        
        # Skip files below minimum number if specified
        if min_file_number is not None and file_number < min_file_number:
            continue
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Find all timestep lines
            timestep_lines = []
            for line in lines:
                match = timestep_pattern.match(line.strip())
                if match:
                    time_value = float(match.group(1))
                    timestep_lines.append(time_value)
            
            if not timestep_lines:
                missing_timestep_files.append(file_number)
                print(f"File {file_number}: NO TIMESTEP LINES FOUND")
            else:
                # Get the final timestep
                final_timestep = timestep_lines[-1]
                
                if final_timestep < time_threshold:
                    incomplete_files.append((file_number, final_timestep))
                    print(f"File {file_number}: INCOMPLETE (final time: {final_timestep})")
                else:
                    complete_files.append((file_number, final_timestep))
                    
        except Exception as e:
            print(f"Error reading file {file_number}: {e}")
    
    return incomplete_files, complete_files, missing_timestep_files

def main():
    # Configuration: Set your directory here
    BRUTUS_OUTPUT_DIR = "<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_standard_quasi_random"
    
    # Detect file_type from directory name (or set manually)
    if "hierarchical" in BRUTUS_OUTPUT_DIR.lower():
        FILE_TYPE = "hierarchical"
    elif "standard" in BRUTUS_OUTPUT_DIR.lower():
        FILE_TYPE = "standard"
    else:
        FILE_TYPE = "standard"  # Default; adjust as needed
    
    # Time threshold for determining completion (simulations should reach ~10.03)
    TIME_THRESHOLD = 9.8
    
    # Optional: Check only files above a certain number (set to None to check all files)
    MIN_FILE_NUMBER = None  # Set to 2550 to check only files > 2550
    
    print("Brutus Output File Completeness Checker")
    print(f"Directory: {BRUTUS_OUTPUT_DIR}")
    print(f"File type: {FILE_TYPE}")
    print(f"Time threshold: {TIME_THRESHOLD}")
    if MIN_FILE_NUMBER:
        print(f"Checking only files > {MIN_FILE_NUMBER}")
    print()
    
    # Check file completeness
    incomplete, complete, missing = check_brutus_completeness(
        BRUTUS_OUTPUT_DIR, FILE_TYPE, TIME_THRESHOLD, MIN_FILE_NUMBER
    )
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    if incomplete:
        print(f"\nINCOMPLETE FILES ({len(incomplete)}):")
        for file_num, final_time in incomplete:
            print(f"  {file_num}: {final_time}")
    else:
        print(f"\nNo incomplete files found!")
    
    if missing:
        print(f"\nFILES WITH NO TIMESTEP DATA ({len(missing)}):")
        for file_num in missing:
            print(f"  {file_num}")
    
    print(f"\nTotal files checked: {len(complete) + len(incomplete) + len(missing)}")
    print(f"Complete files: {len(complete)}")
    print(f"Incomplete files: {len(incomplete)}")
    print(f"Files with no timestep data: {len(missing)}")
    
    # Option to show specific file number ranges
    if incomplete:
        print(f"\nFile numbers with incomplete simulations:")
        file_numbers = [str(num) for num, _ in incomplete]
        print(", ".join(file_numbers))

if __name__ == "__main__":
    main()
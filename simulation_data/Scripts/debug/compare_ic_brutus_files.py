#!/usr/bin/env python3
"""
Script to compare IC files with BRUTUS output files to find missing simulations.
"""

import os
import glob
from pathlib import Path

def get_file_numbers(directory, prefix, suffix):
    """Extract file numbers from filenames in a directory."""
    pattern = os.path.join(directory, f"{prefix}_*.{suffix}")
    files = glob.glob(pattern)
    
    numbers = set()
    for file in files:
        # Extract number from filename like "ic_hierarchical_1234.txt"
        filename = os.path.basename(file)
        if filename.startswith(prefix) and filename.endswith(suffix):
            # Extract the number part
            number_part = filename[len(prefix)+1:-len(suffix)-1]  # Remove prefix_ and .suffix
            try:
                number = int(number_part)
                numbers.add(number)
            except ValueError:
                print(f"Warning: Could not parse number from {filename}")
    
    return numbers

def main():
    # Define paths
    ic_dir = "<home>/Desktop/cursor/simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard"
    brutus_dir = "<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard"
    
    # Get file numbers
    ic_numbers = get_file_numbers(ic_dir, "ic_hierarchical", "txt")
    brutus_numbers = get_file_numbers(brutus_dir, "brutus_hierarchical", "txt")
    
    print(f"Found {len(ic_numbers)} IC files")
    print(f"Found {len(brutus_numbers)} BRUTUS output files")
    
    # Find missing BRUTUS outputs (IC files without corresponding BRUTUS output)
    missing_brutus = ic_numbers - brutus_numbers
    
    print(f"\nMissing BRUTUS output files: {len(missing_brutus)}")
    
    # NEW CHECK: Find BRUTUS outputs without corresponding IC files
    missing_ic = brutus_numbers - ic_numbers
    
    print(f"\n=== CHECKING 1:1 CORRESPONDENCE FOR COMPLETED SIMULATIONS ===")
    print(f"BRUTUS output files without corresponding IC files: {len(missing_ic)}")
    
    if missing_ic:
        print("\nBRUTUS output files that have no corresponding IC file:")
        for num in sorted(missing_ic):
            print(f"  brutus_hierarchical_{num:04d}.txt")
        print(f"\n❌ NOT 1:1 correspondence! There are {len(missing_ic)} BRUTUS files without IC files.")
    else:
        print(f"\n✅ PERFECT 1:1 correspondence! Every BRUTUS output file has a corresponding IC file.")
    
    # Show some statistics
    print(f"\nSummary:")
    print(f"  Total IC files: {len(ic_numbers)}")
    print(f"  Completed BRUTUS simulations: {len(brutus_numbers)}")
    print(f"  Remaining simulations needed: {len(missing_brutus)}")
    print(f"  Completion percentage: {len(brutus_numbers)/len(ic_numbers)*100:.1f}%")
    print(f"  1:1 correspondence for completed: {'YES' if len(missing_ic) == 0 else 'NO'}")

if __name__ == "__main__":
    main() 
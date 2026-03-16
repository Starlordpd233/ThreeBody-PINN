#!/usr/bin/env python3
import os
import glob

def check_last_line(filepath):
    """Check if the last non-empty line of a file starts with 'Result: filename='"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        # Find the last non-empty line
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line:  # Found a non-empty line
                return line.startswith('Result: filename=')
        
        # File is empty or has only empty lines
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def main():
    folders = [
        'brutus_hierarchical',
        'brutus_hierarchical_gold_standard', 
        'brutus_standard_quasi_random',
        'brutus_standard_quasi_random_gold_standard'
    ]
    
    missing_results = {}
    total_files = {}
    
    for folder in folders:
        print(f"\nChecking folder: {folder}")
        pattern = os.path.join(folder, '*.txt')
        txt_files = glob.glob(pattern)
        txt_files.sort()
        
        missing_in_folder = []
        
        for filepath in txt_files:
            if not check_last_line(filepath):
                missing_in_folder.append(os.path.basename(filepath))
        
        missing_results[folder] = missing_in_folder
        total_files[folder] = len(txt_files)
        
        print(f"  Total files: {len(txt_files)}")
        print(f"  Missing 'Result:' line: {len(missing_in_folder)}")
    
    # Print detailed results
    print("\n" + "="*80)
    print("DETAILED RESULTS")
    print("="*80)
    
    for folder in folders:
        if missing_results[folder]:
            print(f"\n{folder}: {len(missing_results[folder])} files missing 'Result:' line")
            print("-" * 50)
            for filename in sorted(missing_results[folder])[:10]:  # Show first 10
                print(f"  - {filename}")
            if len(missing_results[folder]) > 10:
                print(f"  ... and {len(missing_results[folder]) - 10} more files")
        else:
            print(f"\n{folder}: All files have 'Result:' line ✓")

if __name__ == "__main__":
    main() 
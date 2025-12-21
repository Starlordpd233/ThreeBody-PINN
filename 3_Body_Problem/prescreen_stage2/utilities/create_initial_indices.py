#!/usr/bin/env python3
"""
Create initial processing index files for the automated prescreening.
This will check if indices already exist and only create them if needed.
"""

import json
import os
from datetime import datetime

def create_initial_indices():
    """Create initial processing index files if they don't exist."""
    
    base_dir = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2"
    
    # Define index files
    indices = {
        'ic_hierarchical': os.path.join(base_dir, 'processing_index_ic_hierarchical.json'),
        'ic_standard_quasi_random': os.path.join(base_dir, 'processing_index_ic_standard_quasi_random.json')
    }
    
    # Check and create each index
    for dataset_name, index_path in indices.items():
        if os.path.exists(index_path):
            print(f"Index for {dataset_name} already exists at {index_path}")
            with open(index_path, 'r') as f:
                data = json.load(f)
            print(f"  - Contains {len(data.get('processed_files', {}))} processed files")
            print(f"  - Contains {len(data.get('processing_runs', []))} processing runs")
        else:
            print(f"Creating new index for {dataset_name}...")
            initial_data = {
                'processed_files': {},
                'processing_runs': [{
                    'run_id': 'initialization_' + datetime.now().isoformat(),
                    'timestamp': datetime.now().isoformat(),
                    'note': f'Initial creation of processing index for {dataset_name}'
                }]
            }
            with open(index_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
            print(f"  - Created at {index_path}")
    
    # Check if old processing_index.json exists and suggest migration
    old_index = os.path.join(base_dir, 'processing_index.json')
    if os.path.exists(old_index):
        print(f"\nNote: Found old processing_index.json at {old_index}")
        print("The automated script will use separate indices for each dataset.")
        print("The old index will be kept as-is for the original script.")
    
    print("\nDone! The automated prescreening script is ready to use.")

if __name__ == "__main__":
    create_initial_indices()

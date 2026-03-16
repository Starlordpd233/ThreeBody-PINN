#!/usr/bin/env python3
"""
Example workflow showing how to use incremental prescreening efficiently.
"""

import os
import subprocess
import time
import numpy as np

def simulate_new_batch_arrival():
    """Simulate adding new IC files to the raw dataset directory."""
    raw_dir = "<home>/Desktop/cursor/3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random"
    
    # Generate a small batch of new ICs
    print("Generating new batch of ICs...")
    from scipy.stats import qmc
    
    engine = qmc.Sobol(d=6, scramble=True)
    n_new = 50
    samples = engine.random(n_new)
    
    # Get current file count to continue numbering
    import glob
    existing = glob.glob(os.path.join(raw_dir, "ic_*.txt"))
    start_idx = len(existing)
    
    generated = 0
    for i, sample in enumerate(samples):
        # Simple IC generation (similar to Stage 1)
        u1, u2, u3, u4, u5, u6 = sample
        
        # Map to positions
        cos_theta = 1 - 2 * u1
        theta = np.arccos(cos_theta)
        phi = 2 * np.pi * u2
        r = u3**(1/3)
        s = 0.5 + 1.5 * u4
        
        p1 = np.array([1.0, 0.0, 0.0]) * s
        p2 = np.array([
            r * np.sin(theta) * np.cos(phi),
            r * np.sin(theta) * np.sin(phi),
            r * np.cos(theta)
        ]) * s
        p3 = -(p1 + p2)
        
        # Check minimum separation
        if min(np.linalg.norm(p2-p1), np.linalg.norm(p3-p1), np.linalg.norm(p3-p2)) < 0.05:
            continue
        
        # Small velocities
        v1 = np.random.normal(0, 0.1, 3)
        v2 = np.random.normal(0, 0.1, 3)
        v3 = -(v1 + v2)
        
        # Save
        filename = f"ic_{start_idx + generated:04d}.txt"
        filepath = os.path.join(raw_dir, filename)
        
        data = np.array([
            [1.0, p1[0], p1[1], p1[2], v1[0], v1[1], v1[2]],
            [1.0, p2[0], p2[1], p2[2], v2[0], v2[1], v2[2]],
            [1.0, p3[0], p3[1], p3[2], v3[0], v3[1], v3[2]]
        ])
        
        np.savetxt(filepath, data, fmt='%.10e')
        generated += 1
        
        if generated >= n_new:
            break
    
    print(f"Added {generated} new IC files")
    return generated


def main():
    """Example workflow for continuous IC processing."""
    print("=" * 60)
    print("INCREMENTAL PRESCREENING WORKFLOW EXAMPLE")
    print("=" * 60)
    
    # Paths
    utils_script = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2/prescreening_utils.py"
    prescreening_script = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py"
    
    print("\nThis example demonstrates a typical workflow where new IC batches")
    print("are continuously added and processed efficiently.\n")
    
    # Step 1: Check current status
    print("Step 1: Checking current processing status...")
    print("-" * 40)
    subprocess.run(["python", utils_script, "stats"])
    
    # Step 2: Check for any new files
    print("\n\nStep 2: Checking for unprocessed files...")
    print("-" * 40)
    subprocess.run(["python", utils_script, "check"])
    
    # Step 3: Simulate new batch arrival
    response = input("\n\nSimulate adding a new batch of ICs? (y/n): ")
    if response.lower() == 'y':
        print("\nStep 3: Adding new IC batch...")
        print("-" * 40)
        n_added = simulate_new_batch_arrival()
        time.sleep(1)  # Brief pause for clarity
        
        # Step 4: Check again to see new files
        print("\n\nStep 4: Checking for new files after batch addition...")
        print("-" * 40)
        subprocess.run(["python", utils_script, "check"])
        
        # Step 5: Process only the new files
        response = input("\n\nProcess the new files? (y/n): ")
        if response.lower() == 'y':
            print("\nStep 5: Processing new files (incremental mode)...")
            print("-" * 40)
            start_time = time.time()
            subprocess.run(["python", prescreening_script])
            elapsed = time.time() - start_time
            
            print(f"\n\nProcessing completed in {elapsed:.2f} seconds")
            print("Notice how only the new files were processed!")
            
            # Step 6: Final status check
            print("\n\nStep 6: Final status check...")
            print("-" * 40)
            subprocess.run(["python", utils_script, "stats"])
            
            # Step 7: Analyze any failures
            print("\n\nStep 7: Analyzing failures (if any)...")
            print("-" * 40)
            subprocess.run(["python", utils_script, "analyze"])
    
    print("\n\n" + "=" * 60)
    print("WORKFLOW COMPLETE")
    print("=" * 60)
    print("\nKey benefits of incremental processing:")
    print("- Only new files are processed (huge time savings)")
    print("- Processing history is maintained")
    print("- Can resume after interruptions")
    print("- Easy to track what's been done")
    print("\nYou can run this workflow repeatedly as new data arrives!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Example usage script for the enhanced IC generator
Run this to generate new initial conditions
"""

import sys
sys.path.append('<home>/Desktop/cursor/3_Body_Problem')

from FINAL_ic_generator_enhanced import continuation_enhanced_ic_generation

# Configuration
GENERATE_STANDARD = True  # Set to True to generate standard ICs
GENERATE_HIERARCHICAL = True  # Set to True to generate hierarchical ICs
N_SAMPLES_STANDARD = 2500  # Number of samples to generate for each type
N_SAMPLES_HIERARCHICAL = 1500  # Number of samples to generate for each type



if __name__ == "__main__":
    
    if GENERATE_STANDARD:
        print("\n" + "="*60)
        print("GENERATING ENHANCED STANDARD INITIAL CONDITIONS")
        print("="*60)
        print("Features:")
        print("- Epsilon = 0.05 (5x larger than before)")
        print("- Non-zero initial velocities")
        print("- Sobol sequence with scrambling")
        print("- Scale variation: 0.8-1.2")
        
        continuation_enhanced_ic_generation(
            n_samples=N_SAMPLES_STANDARD,
            ic_type="standard",

            #########################################################
            start_from_last=True,  # Continue from existing files
            #########################################################

            epsilon=0.05,  # As recommended in PDF
            velocity_scale=0.1,  # Non-zero velocities
            scale_range=(0.8, 1.2),  # Some variety in scale
            seed=42,
            mass=1.0
        )
    
    if GENERATE_HIERARCHICAL:
        print("\n" + "="*60)
        print("GENERATING HIERARCHICAL INITIAL CONDITIONS")
        print("="*60)
        print("Features:")
        print("- Stable hierarchical triple systems")
        print("- Inner binary: a ~ 0.1-0.3")
        print("- Outer body: 3-10× inner separation")
        print("- Kozai-Lidov stability enforced")
        print("- Saves to ic_raw_datasets/ic_hierarchical/ folder")
        
        continuation_enhanced_ic_generation(
            n_samples=N_SAMPLES_HIERARCHICAL,
            ic_type="hierarchical",

            #########################################################
            start_from_last=True,  # Set to False to start from 0000
            #########################################################

            seed=43,
            mass=1.0
        )
    
    print("\n✓ Generation complete!")
    print("\nNext steps:")
    print("1. Run Stage 2 pre-screening on generated ICs")
    print("2. Run BRUTUS")
    print("3. Calculate metrics using calculate_brutus_metrics.py")

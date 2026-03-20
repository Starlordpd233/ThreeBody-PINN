#!/usr/bin/env python3
"""
Test Pipeline for IC Generation and Brutus Execution
Tests the complete workflow: IC Generation -> (Optional) Prescreening -> Brutus

Usage:
    cd <home>/Desktop/3_body_problem/simulation_data/Data/testing_data
    python test_pipeline.py

This script will:
1. Generate test ICs (both standard and hierarchical)
2. Optionally run prescreening
3. Run Brutus on the ICs
4. Validate outputs
"""

import sys
import os
import subprocess
from pathlib import Path

# Add paths for imports
sys.path.insert(0, '<home>/Desktop/3_body_problem/simulation_data/Scripts/ic_generation')
sys.path.insert(0, '<home>/Desktop/3_body_problem/simulation_data/Validation/prescreening')

# Configuration
TEST_DIR = Path("<home>/Desktop/3_body_problem/simulation_data/Data/testing_data")
BRUTUS_EXEC = Path("<home>/Desktop/3_body_problem/brutus_Newton-main/brutus")

# Number of test samples
N_STANDARD = 3  # Generate 3 standard ICs for testing
N_HIERARCHICAL = 3  # Generate 3 hierarchical ICs for testing

# Brutus parameters for testing (faster than production)
BRUTUS_PARAMS = {
    "hierarchical": {
        "tolerance": "1e-13",
        "word_length": "130",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.1",  # Larger dt for faster testing
        "n_particles": "3"
    },
    "standard": {
        "tolerance": "1e-11",  # Lower precision for faster testing
        "word_length": "100",
        "t_begin": "0",
        "t_end": "10",
        "dt_out": "0.2",  # Larger dt for faster testing
        "n_particles": "3"
    }
}


def step1_generate_ics():
    """Step 1: Generate test initial conditions."""
    print("\n" + "="*70)
    print("STEP 1: GENERATING TEST INITIAL CONDITIONS")
    print("="*70)

    from ic_generation_utils import continuation_enhanced_ic_generation

    # Generate standard ICs
    print(f"\n--- Generating {N_STANDARD} Standard Quasi-Random ICs ---")
    continuation_enhanced_ic_generation(
        n_samples=N_STANDARD,
        ic_type="standard",
        start_from_last=False,  # Start fresh
        directory=str(TEST_DIR / "ic_raw" / "ic_standard_quasi_random"),
        base_filename="ic_standard_",
        epsilon=0.05,
        velocity_scale=0.1,
        scale_range=(0.8, 1.2),
        seed=42,
        mass=1.0
    )

    # Generate hierarchical ICs
    print(f"\n--- Generating {N_HIERARCHICAL} Hierarchical ICs ---")
    continuation_enhanced_ic_generation(
        n_samples=N_HIERARCHICAL,
        ic_type="hierarchical",
        start_from_last=False,  # Start fresh
        directory=str(TEST_DIR / "ic_raw" / "ic_hierarchical"),
        base_filename="ic_hierarchical_",
        seed=43,
        mass=1.0
    )

    print("\n✓ IC Generation Complete")


def step2_prescreening():
    """Step 2: Run prescreening on generated ICs."""
    print("\n" + "="*70)
    print("STEP 2: PRESCREENING (Optional - Press Ctrl+C to skip)")
    print("="*70)

    try:
        import numpy as np
        from numba import jit
    except ImportError as e:
        print(f"⚠ Warning: Missing dependencies for prescreening: {e}")
        print("  Copying ICs directly from ic_raw to ic_final...")
        import shutil
        for ic_type in ["ic_hierarchical", "ic_standard_quasi_random"]:
            src_dir = TEST_DIR / "ic_raw" / ic_type
            dst_dir = TEST_DIR / "ic_final" / ic_type
            dst_dir.mkdir(parents=True, exist_ok=True)
            for f in src_dir.glob("*.txt"):
                shutil.copy(f, dst_dir / f.name)
        print("✓ ICs copied to ic_final/")
        return

    # Manual prescreening using the script's functions
    from stage2_prescreening_revised_auto import (
        parse_ic_file, compute_system_properties,
        integrate_and_check, DATASET_CONFIGS
    )

    # Override paths for testing
    test_configs = [
        {
            'name': 'ic_hierarchical',
            'input_dir': str(TEST_DIR / "ic_raw" / "ic_hierarchical"),
            'output_dir': str(TEST_DIR / "ic_final" / "ic_hierarchical"),
        },
        {
            'name': 'ic_standard_quasi_random',
            'input_dir': str(TEST_DIR / "ic_raw" / "ic_standard_quasi_random"),
            'output_dir': str(TEST_DIR / "ic_final" / "ic_standard_quasi_random"),
        }
    ]

    for config in test_configs:
        print(f"\n--- Prescreening {config['name']} ---")
        input_dir = Path(config['input_dir'])
        output_dir = Path(config['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)

        ic_files = sorted(input_dir.glob("*.txt"))
        passed = 0
        failed = 0

        for ic_file in ic_files:
            try:
                positions, velocities, masses = parse_ic_file(str(ic_file))
                props = compute_system_properties(positions, velocities, masses)

                # Run integration check
                passed_check, reason, max_e_err, min_sep, int_time = integrate_and_check(
                    positions, velocities, masses, tmax=1.0, dt=0.0001
                )

                if passed_check:
                    # Copy to output
                    import shutil
                    shutil.copy(ic_file, output_dir / ic_file.name)
                    passed += 1
                    print(f"  ✓ {ic_file.name}: PASSED")
                else:
                    failed += 1
                    print(f"  ✗ {ic_file.name}: FAILED ({reason})")

            except Exception as e:
                failed += 1
                print(f"  ✗ {ic_file.name}: ERROR ({e})")

        print(f"  Result: {passed} passed, {failed} failed")

    print("\n✓ Prescreening Complete")


def step3_run_brutus():
    """Step 3: Run Brutus on the ICs."""
    print("\n" + "="*70)
    print("STEP 3: RUNNING BRUTUS SIMULATIONS")
    print("="*70)

    if not BRUTUS_EXEC.exists():
        print(f"✗ ERROR: Brutus executable not found at {BRUTUS_EXEC}")
        print("  Please build Brutus first:")
        print("    cd <home>/Desktop/3_body_problem/brutus_Newton-main")
        print("    make clean && make")
        return False

    print(f"Using Brutus executable: {BRUTUS_EXEC}")

    results = {"hierarchical": [], "standard": []}

    for sim_type in ["hierarchical", "standard"]:
        print(f"\n--- Running {sim_type.upper()} Simulations ---")

        ic_dir = TEST_DIR / "ic_final" / f"ic_{sim_type if sim_type == 'hierarchical' else 'standard_quasi_random'}"
        output_dir = TEST_DIR / "brutus_output"
        output_dir.mkdir(parents=True, exist_ok=True)

        ic_files = sorted(ic_dir.glob("*.txt"))
        if not ic_files:
            print(f"  ⚠ No IC files found in {ic_dir}")
            continue

        params = BRUTUS_PARAMS[sim_type]

        for ic_file in ic_files:
            file_num = ic_file.stem.split('_')[-1]
            output_filename = f"brutus_{sim_type}_{file_num}.txt"
            output_path = output_dir / output_filename

            cmd = [
                str(BRUTUS_EXEC),
                params['tolerance'],
                params['word_length'],
                params['t_begin'],
                params['t_end'],
                params['dt_out'],
                params['n_particles'],
                str(ic_file)
            ]

            print(f"  ▶ Running {ic_file.name}...", end=" ", flush=True)

            try:
                with open(output_path, 'w') as outfile:
                    result = subprocess.run(
                        cmd,
                        stdout=outfile,
                        stderr=subprocess.STDOUT,
                        text=True,
                        timeout=300  # 5 minute timeout per simulation
                    )

                # Quick validation
                valid, msg = validate_brutus_output(output_path)
                if valid:
                    print(f"✓ SUCCESS ({msg})")
                    results[sim_type].append((ic_file.name, True, msg))
                else:
                    print(f"✗ FAILED ({msg})")
                    results[sim_type].append((ic_file.name, False, msg))

            except subprocess.TimeoutExpired:
                print(f"✗ TIMEOUT")
                results[sim_type].append((ic_file.name, False, "Timeout"))
                if output_path.exists():
                    output_path.unlink()
            except Exception as e:
                print(f"✗ ERROR: {e}")
                results[sim_type].append((ic_file.name, False, str(e)))

    # Summary
    print("\n" + "-"*70)
    print("BRUTUS EXECUTION SUMMARY")
    print("-"*70)
    for sim_type, res_list in results.items():
        success = sum(1 for _, ok, _ in res_list if ok)
        total = len(res_list)
        print(f"\n{sim_type.upper()}:")
        for name, ok, msg in res_list:
            status = "✓" if ok else "✗"
            print(f"  {status} {name}: {msg}")
        print(f"  Total: {success}/{total} successful")

    return True


def validate_brutus_output(output_path: Path, time_threshold: float = 9.5) -> tuple:
    """Validate Brutus output file."""
    if not output_path.exists():
        return False, "Output file does not exist"

    try:
        import re
        timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')

        with open(output_path, 'r') as f:
            lines = f.readlines()

        timestep_values = []
        for line in lines:
            match = timestep_pattern.match(line.strip())
            if match:
                timestep_values.append(float(match.group(1)))

        if not timestep_values:
            return False, "No timestep lines found"

        final_timestep = timestep_values[-1]

        if final_timestep < time_threshold:
            return False, f"Incomplete (final time: {final_timestep:.3f})"

        return True, f"Complete (final time: {final_timestep:.3f})"

    except Exception as e:
        return False, f"Validation error: {e}"


def step4_verify():
    """Step 4: Verify outputs and show examples."""
    print("\n" + "="*70)
    print("STEP 4: VERIFICATION")
    print("="*70)

    output_dir = TEST_DIR / "brutus_output"

    if not output_dir.exists():
        print("✗ Output directory does not exist")
        return

    output_files = list(output_dir.glob("brutus_*.txt"))

    print(f"\nGenerated {len(output_files)} Brutus output files:")
    for f in sorted(output_files):
        size = f.stat().st_size
        lines = sum(1 for _ in open(f))
        print(f"  • {f.name}: {size} bytes, {lines} lines")

    # Show first few lines of first output file as example
    if output_files:
        example = sorted(output_files)[0]
        print(f"\n--- Example Output ({example.name}) - First 20 lines ---")
        with open(example) as f:
            for i, line in enumerate(f):
                if i >= 20:
                    print("  ...")
                    break
                print(f"  {line.rstrip()}")

    print("\n✓ Verification Complete")


def main():
    """Main test execution."""
    print("="*70)
    print("IC GENERATION AND BRUTUS TEST PIPELINE")
    print("="*70)
    print(f"Test directory: {TEST_DIR}")
    print(f"Brutus executable: {BRUTUS_EXEC}")

    # Check if Brutus exists
    if not BRUTUS_EXEC.exists():
        print("\n⚠ WARNING: Brutus executable not found!")
        print("  Please build it first:")
        print("    cd <home>/Desktop/3_body_problem/brutus_Newton-main")
        print("    make clean && make")
        response = input("\nContinue with IC generation only? (y/n): ")
        if response.lower() != 'y':
            return

    # Run steps
    try:
        step1_generate_ics()
    except Exception as e:
        print(f"\n✗ IC Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    try:
        step2_prescreening()
    except KeyboardInterrupt:
        print("\n\n⚠ Prescreening skipped by user")
        print("  Copying ICs directly to ic_final...")
        import shutil
        for ic_type in ["ic_hierarchical", "ic_standard_quasi_random"]:
            src_dir = TEST_DIR / "ic_raw" / ic_type
            dst_dir = TEST_DIR / "ic_final" / ic_type
            dst_dir.mkdir(parents=True, exist_ok=True)
            for f in src_dir.glob("*.txt"):
                shutil.copy(f, dst_dir / f.name)
    except Exception as e:
        print(f"\n⚠ Prescreening failed: {e}")
        print("  Copying ICs directly to ic_final...")
        import shutil
        for ic_type in ["ic_hierarchical", "ic_standard_quasi_random"]:
            src_dir = TEST_DIR / "ic_raw" / ic_type
            dst_dir = TEST_DIR / "ic_final" / ic_type
            dst_dir.mkdir(parents=True, exist_ok=True)
            for f in src_dir.glob("*.txt"):
                shutil.copy(f, dst_dir / f.name)

    if BRUTUS_EXEC.exists():
        try:
            success = step3_run_brutus()
            if success:
                step4_verify()
        except KeyboardInterrupt:
            print("\n\n⚠ Brutus execution interrupted by user")
        except Exception as e:
            print(f"\n✗ Brutus execution failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n⚠ Skipping Brutus execution (executable not found)")

    print("\n" + "="*70)
    print("TEST PIPELINE COMPLETE")
    print("="*70)
    print(f"\nOutput locations:")
    print(f"  ICs (raw):     {TEST_DIR}/ic_raw/")
    print(f"  ICs (final):   {TEST_DIR}/ic_final/")
    print(f"  Brutus output: {TEST_DIR}/brutus_output/")


if __name__ == "__main__":
    main()

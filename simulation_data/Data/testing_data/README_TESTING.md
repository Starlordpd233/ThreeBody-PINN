# IC Generation and Brutus Testing Guide

This directory contains everything needed to test the IC generation and Brutus execution pipeline.

## Quick Start

### Option 1: Automated Full Pipeline Test

Run the complete test pipeline with a single command:

```bash
cd simulation_data/Data/testing_data
python test_pipeline.py
```

This will:
1. Generate 3 standard and 3 hierarchical ICs
2. Run prescreening (optional - can skip with Ctrl+C)
3. Run Brutus simulations
4. Validate outputs

### Option 2: Manual Step-by-Step Testing

#### Step 1: Build Brutus (if not already built)

```bash
cd brutus_Newton-main
make clean
make
```

Verify the executable exists:
```bash
ls -la brutus_Newton-main/brutus
```

#### Step 2: Generate Test ICs

**Generate a single test IC manually:**

```bash
cd simulation_data/Scripts/ic_generation
python3 -c "
import sys
sys.path.insert(0, '.')
from ic_generation_utils import EnhancedThreeBodySampler

# Create sampler
sampler = EnhancedThreeBodySampler(epsilon=0.05, velocity_scale=0.1, seed=42)

# Generate one IC
positions, velocities, _ = sampler.generate_batch(1)

# Save to testing directory
output_dir = '../../Data/testing_data/ic_raw/ic_standard_quasi_random'
import os
os.makedirs(output_dir, exist_ok=True)
sampler.save_brutus_format_single(
    positions[0], velocities[0],
    f'{output_dir}/ic_standard_0000.txt',
    mass=1.0
)
print('IC saved to ic_standard_0000.txt')
"
```

**Or use the generator script directly:**

```bash
cd simulation_data/Scripts/ic_generation
python3 -c "
import sys
sys.path.insert(0, '.')
from ic_generation_utils import continuation_enhanced_ic_generation

# Generate 3 standard ICs
continuation_enhanced_ic_generation(
    n_samples=3,
    ic_type='standard',
    start_from_last=False,
    directory='../../Data/testing_data/ic_raw/ic_standard_quasi_random',
    base_filename='ic_standard_',
    epsilon=0.05,
    velocity_scale=0.1,
    scale_range=(0.8, 1.2),
    seed=42,
    mass=1.0
)

# Generate 3 hierarchical ICs
continuation_enhanced_ic_generation(
    n_samples=3,
    ic_type='hierarchical',
    start_from_last=False,
    directory='../../Data/testing_data/ic_raw/ic_hierarchical',
    base_filename='ic_hierarchical_',
    seed=43,
    mass=1.0
)
"
```

#### Step 3: Copy ICs to Final Directory (Skip Prescreening for Quick Test)

```bash
cd simulation_data/Data/testing_data

# Copy standard ICs
cp ic_raw/ic_standard_quasi_random/*.txt ic_final/ic_standard_quasi_random/

# Copy hierarchical ICs
cp ic_raw/ic_hierarchical/*.txt ic_final/ic_hierarchical/

# Verify
ls -la ic_final/ic_standard_quasi_random/
ls -la ic_final/ic_hierarchical/
```

#### Step 4: Run Brutus on a Single IC

**For hierarchical ICs:**
```bash
cd brutus_Newton-main

./brutus 1e-15 130 0 10 0.15 3 \
  ../simulation_data/Data/testing_data/ic_final/ic_hierarchical/ic_hierarchical_0000.txt \
  > ../simulation_data/Data/testing_data/brutus_output/brutus_hierarchical_0000.txt
```

**For standard ICs:**
```bash
cd brutus_Newton-main

./brutus 1e-14 122 0 10 0.18 3 \
  ../simulation_data/Data/testing_data/ic_final/ic_standard_quasi_random/ic_standard_0000.txt \
  > ../simulation_data/Data/testing_data/brutus_output/brutus_standard_0000.txt
```

**Brutus parameter explanation:**
```
./brutus <tolerance> <word_length> <t_start> <t_end> <dt_out> <n_bodies> <input_file> > <output_file>
```

| Parameter | Hierarchical | Standard | Description |
|-----------|-------------|----------|-------------|
| tolerance | 1e-15 | 1e-14 | Integration tolerance (lower = more accurate) |
| word_length | 130 | 122 | Working precision in bits |
| t_start | 0 | 0 | Start time |
| t_end | 10 | 10 | End time (simulation runs 0 to 10 time units) |
| dt_out | 0.15 | 0.18 | Output timestep (how often to write snapshots) |
| n_bodies | 3 | 3 | Number of particles |

#### Step 5: Verify Output

```bash
# Check output exists
ls -la simulation_data/Data/testing_data/brutus_output/

# View first 30 lines
head -30 simulation_data/Data/testing_data/brutus_output/brutus_hierarchical_0000.txt

# Check final timestamp (should be >= 9.5)
tail -20 simulation_data/Data/testing_data/brutus_output/brutus_hierarchical_0000.txt
```

## Directory Structure

```
testing_data/
├── ic_raw/                          # Raw generated ICs
│   ├── ic_hierarchical/             # Hierarchical ICs
│   └── ic_standard_quasi_random/    # Standard quasi-random ICs
├── ic_final/                        # Final ICs (after prescreening or copy)
│   ├── ic_hierarchical/
│   └── ic_standard_quasi_random/
├── brutus_output/                   # Brutus simulation outputs
├── test_pipeline.py                 # Automated test script
└── README_TESTING.md               # This file
```

## IC File Format

Each IC file contains 3 lines (one per body):
```
mass x y z vx vy vz
```

Example:
```
1.0 1.0 0.0 0.0 0.0 0.0 0.0
1.0 -0.5 0.866 0.0 0.0 0.0 0.0
1.0 -0.5 -0.866 0.0 0.0 0.0 0.0
```

## Brutus Output Format

Brutus output contains snapshots at each timestep:
```
# Header: time N t_cpu
0.000 3 0.001
# Body lines: mass x y z vx vy vz
1.0 1.0 0.0 0.0 0.0 0.0 0.0
1.0 -0.5 0.866 0.0 0.0 0.0 0.0
1.0 -0.5 -0.866 0.0 0.0 0.0 0.0

# Next snapshot
0.150 3 0.002
...
```

## Prescreening (Optional)

To run the full prescreening pipeline:

```bash
cd simulation_data/Validation/prescreening
python stage2_prescreening_revised_auto.py
```

**Note:** The default prescreening script uses hardcoded paths to the production directories. For testing, either:
1. Modify the `DATASET_CONFIGS` in the script to point to `testing_data/`
2. Or manually copy files as shown in Step 3 above

## Troubleshooting

### Brutus Not Found
```bash
cd brutus_Newton-main
make clean && make
```

### Missing Python Dependencies
```bash
pip install numpy scipy numba
```

### Permission Denied
```bash
chmod +x brutus_Newton-main/brutus
```

### Incomplete Simulation Output
If the final timestamp is < 9.5, the simulation failed. Check:
- Brutus parameters (try less strict tolerance)
- IC validity (check minimum separations)
- Timeout issues (increase timeout in scripts)

## Running Batch Simulations

For production batch runs, use the runner scripts:

```bash
cd simulation_data/Scripts/brutus_runners
python run_brutus_both_type_simple.py
```

**Note:** Edit the script to change:
- `HIERARCHICAL_ICS_PER_RUN` - Number of hierarchical ICs to process
- `STANDARD_ICS_PER_RUN` - Number of standard ICs to process
- Input/output directories (currently set to production paths)

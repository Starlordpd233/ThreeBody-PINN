# Data Documentation README Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Create a comprehensive README.md in `3_Body_Problem/` that documents all data-related components (IC generation, prescreening, integration, metrics, validation) and their interactions within the data pipeline.

**Architecture:** Use a team of 5 subagents working in parallel to explore different component areas, then a consolidator agent to synthesize findings into the final README.

**Tech Stack:** Python 3, subprocess for file exploration

---

### Task 1: Create Agent Team and Launch Parallel Exploration

**Step 1: Create team with 5 subagents**

Launch 5 subagents in parallel, each with a specific area of responsibility:

- **Agent 1 (IC Generation)**: Explore `final_stage_ic_datasets/`, `ic_raw_datasets/`, `generate_enhanced_ics.py`, `FINAL_ic_generator_enhanced.py`
- **Agent 2 (Prescreening)**: Explore `prescreen_stage2/` in depth
- **Agent 3 (Brutus Integration)**: Explore `run_brutus_both_type_simple.py`, `run_brutus_hierarchical_only_mac_gold_standard.py`, `brutus_output/`
- **Agent 4 (Metrics & Validation)**: Explore `brutus_metrics/`, `dataset_readiness_checks/`, `problematic_ics/`, `problematic_ics_blacklist.json`
- **Agent 5 (Documentation)**: Read `data_documentation/DATASET_DOCUMENTATION.md` and `README.md` for context

**Step 2: Provide exploration prompt to each agent**

Each agent should:
1. List all files in their assigned directories
2. Read key Python scripts to understand functionality
3. Identify interactions with other components (what inputs they need, what outputs they produce)
4. Document the data flow

**Step 3: Run agents in parallel**

```bash
# Launch all 5 agents in parallel via Agent tool with run_in_background
```

---

### Task 2: Agent 1 - IC Generation Exploration

**Files:**
- Modify: `3_Body_Problem/generate_enhanced_ics.py`
- Modify: `3_Body_Problem/FINAL_ic_generator_enhanced.py`
- Explore: `3_Body_Problem/final_stage_ic_datasets/`
- Explore: `3_Body_Problem/ic_raw_datasets/`

**Step 1: Read and document generate_enhanced_ics.py**

Read the script to understand:
- What IC variants it generates (hierarchical, standard quasi-random)
- Input parameters and their defaults
- Output format and folder structure
- Key functions used

**Step 2: Read and document FINAL_ic_generator_enhanced.py**

Compare with generate_enhanced_ics.py to understand differences.

**Step 3: List and document final_stage_ic_datasets/**

```bash
ls -la 3_Body_Problem/final_stage_ic_datasets/
ls -la 3_Body_Problem/final_stage_ic_datasets/ic_hierarchical/ | head -20
ls -la 3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random/ | head -20
```

Document the file naming conventions and folder structure.

**Step 4: List and document ic_raw_datasets/**

```bash
ls -la 3_Body_Problem/ic_raw_datasets/
```

---

### Task 3: Agent 2 - Prescreening Stage Exploration

**Files:**
- Explore: `3_Body_Problem/prescreen_stage2/`

**Step 1: Read stage2_prescreening_revised_auto.py**

```bash
# Read the main prescreening script
```

Document:
- What it does (filters unstable ICs via leapfrog)
- Input: IC files from final_stage_ic_datasets
- Output: filtered ICs, processing_index JSON files
- Key parameters (TMAX, DT, ENERGY_ERROR_THRESHOLD, etc.)

**Step 2: Read prescreening_utils.py**

Document utility functions.

**Step 3: Examine processing_index JSON files**

```bash
# Read processing_index files to understand what gets tracked
```

---

### Task 4: Agent 3 - Brutus Integration Exploration

**Files:**
- Modify: `3_Body_Problem/run_brutus_both_type_simple.py`
- Modify: `3_Body_Problem/run_brutus_hierarchical_only_mac_gold_standard.py`
- Explore: `3_Body_Problem/brutus_output/`

**Step 1: Read run_brutus_both_type_simple.py**

Document:
- How it invokes Brutus C++ binary
- Parameters passed (tol, Lw, dt_out, etc.)
- Input: filtered ICs from prescreening
- Output: simulation trajectories in brutus_output/

**Step 2: Read run_brutus_hierarchical_only_mac_gold_standard.py**

Document differences from the simple runner.

**Step 3: List brutus_output/**

```bash
ls -la 3_Body_Problem/brutus_output/
ls 3_Body_Problem/brutus_output/brutus_hierarchical/ | wc -l
ls 3_Body_Problem/brutus_output/brutus_standard_quasi_random/ | wc -l
```

---

### Task 5: Agent 4 - Metrics & Validation Exploration

**Files:**
- Explore: `3_Body_Problem/brutus_metrics/`
- Explore: `3_Body_Problem/dataset_readiness_checks/`
- Explore: `3_Body_Problem/problematic_ics/`
- Read: `3_Body_Problem/problematic_ics_blacklist.json`

**Step 1: Read brutus_metrics/calculate_metrics.py**

Document:
- What metrics are calculated
- Input: brutus_output/ files
- Output: JSON metric files

**Step 2: Examine dataset_readiness_checks/**

```bash
ls -la 3_Body_Problem/dataset_readiness_checks/
```

Note: This is known to be broken per README.md.

**Step 3: Read problematic_ics_blacklist.json**

```bash
# Read to understand what ICs have failed
```

---

### Task 6: Agent 5 - Documentation Context

**Files:**
- Read: `3_Body_Problem/data_documentation/DATASET_DOCUMENTATION.md`
- Read: `README.md` (root level)

**Step 1: Read DATASET_DOCUMENTATION.md**

This contains detailed dataset specs and anomalies.

**Step 2: Review root README.md**

For context on how this fits into the bigger picture.

---

### Task 7: Consolidator Agent - Synthesize Findings

**Step 1: Review all agent findings**

Read the exploration results from all 5 agents.

**Step 2: Create consolidated documentation outline**

Structure for README.md:

```
# 3_Body_Problem Data Pipeline

## Overview
- What this folder contains
- Where it fits in the bigger project

## Pipeline Stages
- Stage 1: IC Generation
- Stage 2: Prescreening
- Stage 3: Brutus Integration
- Stage 4: Metrics
- Stage 5: PINN Preprocessing (reference to pinn/)

## Component Details
[For each component: purpose, key files, inputs, outputs]

## Data Variants
- Hierarchical
- Standard Quasi-Random
- Gold Standard variants

## Dataset Folders
- final_stage_ic_datasets/
- brutus_output/
- ic_raw_datasets/
- problematic_ics/

## Interactions
[How components connect]

## Known Issues
- dataset_readiness_checks broken
- Other limitations
```

---

### Task 8: Write Final README.md

**File:**
- Create: `3_Body_Problem/README.md`

**Step 1: Write the comprehensive README**

Following the outline from Task 7, write complete documentation.

**Step 2: Verify the file**

Read the created file to ensure completeness.

---

## Execution Notes

- This plan involves parallel exploration via subagents
- Each exploration task is independent and can run in parallel
- The consolidator depends on all exploration agents completing
- Final README creation depends on consolidator
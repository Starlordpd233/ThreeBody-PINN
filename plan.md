# Plan: Revise and Unify Agent Instruction Files for Three-Body Problem Project

## Current State Analysis

### 1. File Overview

**CLAUDE.md** (445 lines):
- Comprehensive project-specific instructions for Three-Body Problem project
- Contains both generic AI guidance (sections 1-7) and detailed project architecture (section 8+)
- Well-structured with clear sections for Brutus simulator, pipeline, PINN system, paper templates
- Includes essential commands, data formats, precision settings, implementation details
- Has validation, workflow best practices, debugging, advanced features, etc.

**GEMINI.md** (329 lines):
- Mix of generic AI assistant instructions and analysis text
- Contains repeated "Improved CLAUDE.md" sections that appear to be suggestions rather than actual instructions
- Includes website analysis dated July 24, 2025 about Claude Code best practices
- Lacks project-specific details from the Three-Body Problem project
- Appears to be a template or analysis document rather than a proper instruction file

**QWEN.md** (329 lines):
- Nearly identical to GEMINI.md, just with different filename/title
- Same structure and content issues

### 2. Key Inconsistencies

1. **Content Type Mismatch**:
   - CLAUDE.md: Actual project instructions
   - GEMINI.md/QWEN.md: Generic AI guidelines + website analysis

2. **Structure Differences**:
   - CLAUDE.md: Logical progression from generic to project-specific
   - GEMINI.md/QWEN.md: Disorganized with repeated sections

3. **Project Knowledge Gap**:
   - Only CLAUDE.md contains essential project architecture details
   - GEMINI.md/QWEN.md lack Brutus, pipeline, PINN, paper template information

4. **Duplicate/Redundant Content**:
   - GEMINI.md/QWEN.md have multiple "improved CLAUDE.md" sections
   - Contains analysis text that shouldn't be in final instruction files

### 3. Project Exploration Findings

From the three parallel Explore agents:

**Three-Body Problem Folder** (`<home>/Desktop/cursor/3_Body_Problem/`):
- Sophisticated pipeline: IC Generation → Prescreening → Simulation → Metrics Calculation
- Key scripts: `FINAL_ic_generator_enhanced.py`, `run_brutus_both_type_simple.py`, `calculate_metrics.py`
- Data directories: `ic_raw_datasets/`, `final_stage_ic_datasets/`, `brutus_output/`, `brutus_metrics/`
- Hierarchical vs standard systems with different precision parameters
- Gold-standard simulations with higher precision

**Brutus Newton Main** (`<home>/Desktop/cursor/brutus_Newton-main/`):
- C++ N-body simulator with Bulirsch-Stoer integration
- Arbitrary precision arithmetic using GMP, MPFR, mpreal libraries
- Makefile configured for macOS Homebrew at `/opt/homebrew`
- Command-line: `./brutus tolerance wordlength t_begin t_end dt_out N file_in`
- Typical parameters: hierarchical (tolerance=1e-15, precision=130), standard (tolerance=1e-14, precision=122)

**PINN and Paper Templates**:
- PINN system: SQR-SkipResNet-SIREN with 12 layers, 256 neurons
- 13-component IC vector normalized to [-1, 1]
- Data processing pipeline with 7 curriculum learning stages
- Paper templates: PINN instruction, MDPI journal template, framework review
- Reference code with Lyapunov analysis and neural network implementations

### 4. Missing Information in Current Files

Current CLAUDE.md is comprehensive but could be enhanced with:
1. More detailed pipeline workflow from exploration findings
2. Specific file paths and directory structures
3. Recent developments in the codebase
4. Additional debugging commands and validation procedures
5. Integration points between components

## Revision Strategy

### 1. Unified Template Structure

Create a master template with the following structure:

```
# [AGENT_NAME].md: Enhanced Instructions for [Agent Name] Code Agent

## Part 1: Core AI Assistant Guidelines
### 1.1 Core Behavior and Response Principles
### 1.2 Code Style and Best Practices
### 1.3 Workflow Guidelines
### 1.4 Mathematics and Science
### 1.5 Writing and Essays
### 1.6 Document Analysis and Extraction
### 1.7 Research and Information Gathering
### 1.8 Available Tools and Customization

## Part 2: Three-Body Problem Project Architecture
### 2.1 Project Overview and Components
### 2.2 Brutus N-body Simulator (`brutus_Newton-main/`)
### 2.3 Three-Body Problem Pipeline (`3_Body_Problem/`)
### 2.4 PINN System (`pinn/`)
### 2.5 Paper Templates (`paper_templates/`)
### 2.6 Reference Code (`reference-code/`)

## Part 3: Essential Development Commands
### 3.1 Building and Running Brutus Simulator
### 3.2 Pipeline Execution Commands
### 3.3 PINN Development and Training

## Part 4: Data Flow and Formats
### 4.1 Complete Pipeline Workflow
### 4.2 Initial Condition File Format
### 4.3 Brutus Output Format
### 4.4 PINN Input Vector (13 components)

## Part 5: Precision and Performance Settings
### 5.1 Brutus Simulator Parameters
### 5.2 PINN Architecture Specifications
### 5.3 Memory and Performance Considerations

## Part 6: Critical Implementation Details
### 6.1 Brutus Integration Method
### 6.2 PINN Training Strategy
### 6.3 Curriculum Learning Implementation

## Part 7: Common Issues and Solutions
### 7.1 Brutus Compilation Issues
### 7.2 Simulation Timeouts and Failures
### 7.3 Memory Management
### 7.4 PINN Training Instability

## Part 8: Validation and Quality Assurance
### 8.1 Conservation Metrics
### 8.2 Code Quality Standards
### 8.3 Testing Strategy

## Part 9: Development Workflow Best Practices
### 9.1 Setup and Environment
### 9.2 Iterative Development
### 9.3 Data Processing Pipeline
### 9.4 Performance Optimization

## Part 10: File Organization Patterns
### 10.1 Directory Structure
### 10.2 Naming Conventions
### 10.3 Data Storage Strategies

## Part 11: Debugging and Troubleshooting
### 11.1 Common Error Patterns
### 11.2 Diagnostic Commands
### 11.3 Validation Procedures

## Part 12: Advanced Features and Extensions
### 12.1 Parallel Processing
### 12.2 Curriculum Learning Details
### 12.3 High-Performance Computing

## Part 13: Security and Safety Considerations
### 13.1 Input Validation
### 13.2 Numerical Stability

## Part 14: Collaboration and Version Control
### 14.1 Git Workflow
### 14.2 Code Review Standards

## Part 15: Performance Monitoring
### 15.1 Key Metrics
### 15.2 Profiling Tools

## Part 16: Emergency Procedures
### 16.1 Data Recovery
### 16.2 System Failure Recovery

## Part 17: Customization Notes
### 17.1 Environment-Specific Settings
### 17.2 User Preferences

## Part 18: Research and Reproducibility
### 18.1 Experiment Tracking
### 18.2 Computational Experiments
```

### 2. Content Sources

**Part 1 (Generic Guidelines):**
- Merge best from CLAUDE.md sections 1-7
- Incorporate useful workflow details from GEMINI.md/QWEN.md
- Remove redundant/analysis text
- Keep "Let's think step by step" for complex reasoning

**Parts 2-18 (Project-Specific):**
- Enhance CLAUDE.md section 8+ with exploration findings
- Add detailed directory structures and file paths
- Include specific command examples
- Integrate pipeline workflow details
- Add validation procedures and debugging commands
- Include recent developments and current state

### 3. Agent-Specific Customization

For each agent file (CLAUDE.md, GEMINI.md, QWEN.md):
- Change filename and title
- Replace "[AGENT_NAME]" and "[Agent Name]" with actual agent name
- Keep all other content identical
- Optionally add brief agent-specific tool notes if relevant (but maintain same structure)

## Implementation Steps

### Step 1: Create Unified Template
1. Start with CLAUDE.md as base template
2. Extract and merge generic AI guidance sections from all three files:
   - Core Behavior and Response Principles (best from each)
   - Code Style and Best Practices (merge Python/C++ emphasis)
   - Workflow Guidelines (include test-driven, visual iteration from GEMINI.md/QWEN.md)
   - Mathematics and Science (keep LaTeX emphasis)
   - Writing and Essays (merge insights)
   - Document Analysis and Extraction
   - Research and Information Gathering
   - Available Tools and Customization
3. Remove redundant text, website analysis, and "improved CLAUDE.md" suggestions from GEMINI.md/QWEN.md
4. Ensure consistent formatting and hierarchical structure

### Step 2: Enhance Project-Specific Content
1. Expand "Project-Specific Architecture" section with exploration findings:
   - Add detailed directory structures for each component
   - Include specific file paths and naming conventions
   - Add pipeline workflow with stage descriptions
   - Include Brutus compilation and execution details
   - Add PINN architecture specifications (13-component vector, 7 curriculum stages)
   - Include paper template descriptions
2. Update "Essential Development Commands" with specific parameters:
   - Brutus parameters: hierarchical vs standard vs gold-standard
   - IC generation commands with Sobol sampling details
   - Batch processing with timeout settings
   - PINN development commands
3. Enhance "Data Flow and Formats" with exact file formats
4. Update "Precision and Performance Settings" with discovered values
5. Add "Critical Implementation Details" from code examination:
   - Brutus integration method (Bulirsch-Stoer with adaptive timestep)
   - PINN training strategy (curriculum learning, physics loss)
   - Numerical stability considerations
6. Expand "Common Issues and Solutions" with compilation fixes
7. Update "Validation and Quality Assurance" with conservation thresholds
8. Enhance all remaining sections with exploration insights

### Step 3: Create Agent-Specific Files
1. Create three files: CLAUDE.md, GEMINI.md, QWEN.md
2. For each file:
   - Copy unified template content
   - Replace `[AGENT_NAME]` with filename (CLAUDE/GEMINI/QWEN)
   - Replace `[Agent Name]` with agent name (Claude/Gemini/Qwen)
   - Optionally add agent-specific tool note section if tools differ significantly
3. Verify all three files have identical content except for agent name references

### Step 4: Validation and Quality Check
1. Verify all essential project information is included:
   - Brutus simulator details and compilation
   - Three-Body Problem pipeline workflow
   - PINN system architecture
   - Paper templates structure
   - Reference code overview
2. Check command examples are accurate and executable
3. Verify file paths are correct for current system
4. Ensure no redundant or contradictory information
5. Test readability and structure for AI agent comprehension

## Critical Files to Modify

**Primary Files:**
1. `<home>/Desktop/cursor/CLAUDE.md` - Will be replaced with enhanced version
2. `<home>/Desktop/cursor/GEMINI.md` - Will be replaced with unified template
3. `<home>/Desktop/cursor/QWEN.md` - Will be replaced with unified template

**Source Files for Content:**
1. `<home>/Desktop/cursor/CLAUDE.md` - Current comprehensive project instructions
2. `<home>/Desktop/cursor/GEMINI.md` - Generic AI guidance and workflow details
3. `<home>/Desktop/cursor/QWEN.md` - Consistency check for generic guidance
4. `<home>/Desktop/cursor/3_Body_Problem/FINAL_ic_generator_enhanced.py` - IC generation parameters
5. `<home>/Desktop/cursor/3_Body_Problem/run_brutus_both_type_simple.py` - Simulation parameters
6. `<home>/Desktop/cursor/brutus_Newton-main/makefile` - Brutus compilation details
7. `<home>/Desktop/cursor/pinn/basic_architecture.py` - PINN architecture specifications
8. `<home>/Desktop/cursor/pinn/data-processing-pipeline-full.py` - Data processing pipeline
9. `<home>/Desktop/cursor/paper_templates/pinn_instruction/CTL-instruction-final.tex` - Paper content

## Expected Outcome

Three agent instruction files (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`) with:
1. **Identical structure and content** (except agent name references)
2. **Comprehensive generic AI guidance** merged from all sources
3. **Enhanced project-specific architecture** with exploration findings
4. **Accurate commands and parameters** for all project components
5. **Complete troubleshooting and validation** procedures
6. **Clear organization** for easy reference by AI agents

## Risk Mitigation

1. **Backup original files** before modification
2. **Validate commands** against actual project state
3. **Test file paths** for accuracy
4. **Maintain version control** of changes
5. **Verify agent-specific customization** doesn't create inconsistencies
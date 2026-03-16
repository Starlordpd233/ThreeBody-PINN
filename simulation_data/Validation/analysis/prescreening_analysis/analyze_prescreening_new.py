#!/usr/bin/env python3
"""
Analyze and visualize the results from Stage 2 pre-screening.
Completely revised following the new instructions:
    1.  Replace old scatter plots with clear, category-separated visuals.
    2.  Add a pie + stacked bar failure summary.
    3.  Add KDE-based comparison distributions.
    4.  Add an "Outcome Map" scatter colored by failure reason.
    5.  Add a deep-dive energy vs separation plot.

Main fixes
----------
1. Guard against missing 'reason' key in plot_failure_summary().
2. Guard against empty lists in pie/bar charts.
3. Ensure numeric columns exist before plotting KDE.
4. Add robust log-scale handling for zero/NaN values in energy_deep_dive.
5. General NaN / empty-dataframe checks.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List, Optional
from collections import Counter, defaultdict
import pandas as pd
import platform

# ---------- Generic JSON I/O ----------
def load_prescreening_results(results_file: str) -> Dict:
    """Load a single prescreening JSON."""
    with open(results_file, 'r') as f:
        return json.load(f)

def load_all_prescreening_results(
    results_dir: str,
    files_to_process: List[str] = None
) -> Dict:
    all_detailed_results = []
    total_summary = Counter()
    all_failure_reasons = Counter()

    if not os.path.isdir(results_dir):
        print(f"Directory not found: {results_dir}")
        return None

    if files_to_process:
        json_files = files_to_process
    else:
        json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]

    if not json_files:
        print(f"No JSON files found in {results_dir}")
        return None

    print(f"Processing {len(json_files)} file(s) from {results_dir}")

    for file_name in json_files:
        file_path = os.path.join(results_dir, file_name)
        try:
            results = load_prescreening_results(file_path)
            
            # Handle nested "datasets" structure if present
            if "datasets" in results and isinstance(results["datasets"], list):
                datasets = results["datasets"]
            else:
                # Treat as single dataset (flat structure)
                datasets = [results]
            
            for ds in datasets:
                # Process each dataset (nested or flat)
                if 'detailed_results' in ds:
                    all_detailed_results.extend(ds['detailed_results'])
                
                run_info = ds.get('run_info', {})
                total_summary['total_files'] += run_info.get('files_processed', 0)
                total_summary['passed'] += run_info.get('files_passed', 0)
                total_summary['failed'] += run_info.get('files_failed', 0)
                total_summary['elapsed_time'] += run_info.get('elapsed_time', 0)
                
                all_failure_reasons.update(ds.get('failure_reasons', {}))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Could not process file {file_name}: {e}")

    if not all_detailed_results:
        print("No valid results found in any of the files.")
        return None

    if total_summary['total_files'] > 0:
        total_summary['pass_rate'] = total_summary['passed'] / total_summary['total_files']
    else:
        total_summary['pass_rate'] = 0.0

    return {
        'summary': dict(total_summary),
        'failure_reasons': dict(all_failure_reasons),
        'detailed_results': all_detailed_results,
    }

# ---------- NEW PLOTTING FUNCTIONS ----------
def plot_failure_summary(results: Dict, output_dir: str) -> Optional[plt.Figure]:
    """
    1. Pie chart: overall failure breakdown.
    2. Stacked bar chart: failures by dataset.
    """
    failure_reasons = results['failure_reasons']
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Failure Summary", fontsize=16)

    # ---- 1. Pie chart ----
    if failure_reasons:
        labels, counts = zip(*failure_reasons.items())
        axes[0].pie(counts, labels=labels, autopct='%1.1f%%', startangle=90,
                    colors=plt.cm.Set3.colors)
    else:
        axes[0].text(0.5, 0.5, "No failures", ha='center', va='center')
    axes[0].set_title("Overall Failure Reasons")

    # ---- 2. Stacked bar chart by dataset ----
    dataset_fail = defaultdict(lambda: defaultdict(int))
    for item in results['detailed_results']:
        if not item.get('passed', True):
            reason = item.get('reason', item.get('stage', 'unknown'))
            ds = item.get('dataset')  # Get dataset, returns None if missing
            if ds:  # Only process if a dataset key exists
                dataset_fail[ds][reason] += 1

    if dataset_fail:
        datasets = sorted(dataset_fail.keys())
        reasons = sorted(set().union(*(d.keys() for d in dataset_fail.values())))
        bottom = np.zeros(len(datasets))
        colors = plt.cm.tab10.colors[:len(reasons)]
        for idx, reason in enumerate(reasons):
            vals = [dataset_fail[ds].get(reason, 0) for ds in datasets]
            axes[1].bar(datasets, vals, bottom=bottom, label=reason, color=colors[idx])
            bottom += vals
        axes[1].set_ylabel("Count of Failures")
        axes[1].set_title("Failures by Dataset")
        axes[1].legend(title="Reason")
    else:
        axes[1].text(0.5, 0.5, "No failures", ha='center', va='center')
        axes[1].set_title("Failures by Dataset")

    plt.tight_layout()
    out_path = os.path.join(output_dir, "failure_summary.png")
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    return fig

def plot_property_correlations(results: Dict, output_dir: str) -> None:
    """
    Creates 4 individual plots that match the original Property Correlations for Passed ICs figure.
    Saves them in the property_correlations subfolder.
    """
    df = pd.DataFrame(results['detailed_results'])
    # Filter to only passed ICs
    df_passed = df[df['passed'] == True].copy()
    
    if df_passed.empty:
        print("No passed ICs to plot.")
        return
    
    # Create the subdirectory for these plots
    correlations_dir = os.path.join(output_dir, "property_correlations")
    os.makedirs(correlations_dir, exist_ok=True)
    print(f"Saving individual property correlation plots to: {correlations_dir}")
    
    # Plot 1: Virial Ratio vs Angular Momentum (colored by min_separation)
    if all(col in df_passed.columns for col in ['virial_ratio', 'angular_momentum', 'min_separation']):
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(df_passed['virial_ratio'], df_passed['angular_momentum'], 
                           c=df_passed['min_separation'], cmap='viridis', alpha=0.6, s=50)
        ax.set_xlabel('Virial Ratio')
        ax.set_ylabel('Angular Momentum')
        ax.set_title('Virial Ratio vs Angular Momentum')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Min Separation')
        plt.tight_layout()
        fig.savefig(os.path.join(correlations_dir, "virial_ratio-vs-angular_momentum.png"), 
                   dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("  - Saved: virial_ratio-vs-angular_momentum.png")
    
    # Plot 2: Virial Ratio vs Minimum Separation
    if all(col in df_passed.columns for col in ['virial_ratio', 'min_separation']):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df_passed['virial_ratio'], df_passed['min_separation'], 
                  alpha=0.6, s=50, color='tab:blue')
        ax.set_xlabel('Virial Ratio')
        ax.set_ylabel('Minimum Separation')
        ax.set_title('Virial Ratio vs Minimum Separation')
        plt.tight_layout()
        fig.savefig(os.path.join(correlations_dir, "virial_ratio-vs-min_separation.png"), 
                   dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("  - Saved: virial_ratio-vs-min_separation.png")
    
    # Plot 3: Angular Momentum vs Minimum Separation
    if all(col in df_passed.columns for col in ['angular_momentum', 'min_separation']):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df_passed['angular_momentum'], df_passed['min_separation'], 
                  alpha=0.6, s=50, color='tab:blue')
        ax.set_xlabel('Angular Momentum')
        ax.set_ylabel('Minimum Separation')
        ax.set_title('Angular Momentum vs Minimum Separation')
        plt.tight_layout()
        fig.savefig(os.path.join(correlations_dir, "angular_momentum-vs-min_separation.png"), 
                   dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("  - Saved: angular_momentum-vs-min_separation.png")
    
    # Plot 4: Energy Distribution (Kinetic vs Potential Energy)
    if all(col in df_passed.columns for col in ['kinetic_energy', 'potential_energy']):
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate colors based on distance from virial equilibrium
        # For virial equilibrium: -Potential Energy = 2 * Kinetic Energy
        virial_ratio_energy = -df_passed['potential_energy'] / (2 * df_passed['kinetic_energy'])
        
        scatter = ax.scatter(df_passed['kinetic_energy'], -df_passed['potential_energy'], 
                           c=virial_ratio_energy, cmap='coolwarm', alpha=0.6, s=50)
        
        # Add virial equilibrium line
        ke_range = np.linspace(df_passed['kinetic_energy'].min(), 
                              df_passed['kinetic_energy'].max(), 100)
        ax.plot(ke_range, 2 * ke_range, 'k--', alpha=0.5, label='Virial equilibrium')
        
        ax.set_xlabel('Kinetic Energy')
        ax.set_ylabel('-Potential Energy')
        ax.set_title('Energy Distribution')
        ax.legend()
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Virial Ratio (Energy)')
        plt.tight_layout()
        fig.savefig(os.path.join(correlations_dir, "energy_distribution.png"), 
                   dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("  - Saved: energy_distribution.png")
    elif 'kinetic_energy' not in df_passed.columns or 'potential_energy' not in df_passed.columns:
        print("  - Skipping energy distribution plot: kinetic_energy or potential_energy columns not found")

def plot_outcome_map(results: Dict, output_dir: str) -> Optional[plt.Figure]:
    """
    Scatter: Virial Ratio vs Angular Momentum, color-coded by outcome.
    """
    df = pd.DataFrame(results['detailed_results'])

    def outcome(row):
        if row.get('passed', True):
            return 'Passed'
        reason = row.get('reason') or row.get('stage', 'unknown')
        # Guard against NaN
        if pd.isna(reason):
            return 'Unknown'
        return str(reason).replace('_', ' ').title()

    if 'virial_ratio' not in df.columns or 'angular_momentum' not in df.columns:
        print("Outcome map skipped: missing required fields.")
        return None

    df['outcome'] = df.apply(outcome, axis=1)
    palette = {
        'Passed': 'green',
        'Min Separation': 'red',
        'Energy Conservation': 'orange',
        'Static Check': 'gray',
        'Dynamic Failed': 'purple',  # Fallback for unspecified dynamic fails
        'Unknown': 'black'
    }

    g = sns.jointplot(
        data=df,
        x='virial_ratio',
        y='angular_momentum',
        hue='outcome',
        palette={k: v for k, v in palette.items() if k in df['outcome'].values},
        alpha=0.7,
        height=8,
        ratio=3
    )
    g.fig.suptitle("Outcome Map: Virial Ratio vs Angular Momentum", y=1.03)
    plt.tight_layout()
    out_path = os.path.join(output_dir, "outcome_map.png")
    g.fig.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    return g.fig

def plot_energy_deep_dive(results: Dict, output_dir: str) -> Optional[plt.Figure]:
    """
    Scatter: Max Energy Error vs Minimum Separation (log-log), color by virial ratio.
    """
    df = pd.DataFrame(results['detailed_results'])
    # Keep only dynamic runs with both fields
    df = df[df['stage'] != 'static_check'].dropna(subset=['max_energy_error', 'min_separation'])

    if df.empty or df['max_energy_error'].le(0).all():
        print("Energy deep-dive skipped: no valid dynamic ICs.")
        return None

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(
        df['min_separation'],
        df['max_energy_error'] * 100,  # percent
        c=df['virial_ratio'],
        cmap='viridis',
        alpha=0.7
    )
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Minimum Separation")
    ax.set_ylabel("Max Energy Error (%)")
    ax.set_title("Energy Error vs Minimum Separation")
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Virial Ratio")
    plt.tight_layout()
    out_path = os.path.join(output_dir, "energy_deep_dive.png")
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    return fig

def print_summary_statistics(results: Dict) -> None:
    """Console summary."""
    summary = results['summary']
    print("=" * 60)
    print("STAGE 2 PRE-SCREENING SUMMARY")
    print("=" * 60)
    print(f"Total ICs processed: {summary['total_files']}")
    print(f"Passed: {summary['passed']} ({summary['pass_rate']*100:.1f}%)")
    print(f"Failed: {summary['failed']} ({(1-summary['pass_rate'])*100:.1f}%)")
    print(f"Processing time: {summary['elapsed_time']:.2f} seconds")
    print(f"Average time per IC: {summary['elapsed_time']/summary['total_files']:.3f} seconds" if summary['total_files'] > 0 else "N/A")
    print()
    print("Failure Breakdown:")
    for reason, count in results['failure_reasons'].items():
        pct = (count / summary['failed']) * 100 if summary['failed'] else 0
        print(f"  - {reason}: {count} ({pct:.1f}% of failures)")
    print()

# ---------- Main ----------
def main():
    results_dir = "simulation_data/Validation/prescreening/prescreen_run_results"
    output_dir = "simulation_data/Validation/prescreening/analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    # Debug: Optionally limit to first N files (set to None to process all)
    debug_limit = None  # Change to 1 to process only the first file

    all_json_files = sorted([f for f in os.listdir(results_dir) if f.endswith('.json')])
    if not all_json_files:
        print(f"No JSON files found in {results_dir}")
        return
    
    files_to_process = all_json_files[:debug_limit] if debug_limit else all_json_files
    if debug_limit:
        print(f"--- Debug mode: processing first {debug_limit} file(s), starting with {files_to_process[0]} ---")
    
    results = load_all_prescreening_results(results_dir, files_to_process=files_to_process)
    if not results:
        print("No results to analyze.")
        return

    print_summary_statistics(results)

    print("\nGenerating figures...")
    figures = []
    figures.append(plot_failure_summary(results, output_dir))
    plot_property_correlations(results, output_dir)  # This now saves files directly
    figures.append(plot_outcome_map(results, output_dir))
    figures.append(plot_energy_deep_dive(results, output_dir))

    # Filter out any None values in case a plot was skipped
    valid_figures = [fig for fig in figures if fig is not None]

    if valid_figures:
        print(f"\nDisplaying {len(valid_figures)} figure(s). Close all windows to exit.")
        plt.show()  # This will block until all figure windows are closed
    else:
        print("\nNo figures were generated to display.")
    
    # Clean up figure objects from memory after they are closed
    for fig in valid_figures:
        plt.close(fig)

    print("\nAnalysis complete. Figures saved to:", output_dir)


if __name__ == "__main__":
    main()
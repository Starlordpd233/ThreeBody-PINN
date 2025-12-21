#!/usr/bin/env python3
"""
Analyze and visualize the results from Stage 2 pre-screening.
Completely revised following the new instructions:
    1.  Replace old scatter plots with clear, category-separated visuals.
    2.  Add a pie + stacked bar failure summary.
    3.  Add KDE-based comparison distributions.
    4.  Add an “Outcome Map” scatter colored by failure reason.
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

def plot_comparison_distributions(results: Dict, output_dir: str) -> None:
    """
    Saves 4 individual KDE plots comparing all ICs vs passed ICs into a subfolder.
    """
    df_all = pd.DataFrame(results['detailed_results'])
    df_pass = df_all[df_all['passed'] == True]

    # Create the subdirectory for these plots
    correlations_dir = os.path.join(output_dir, "property_correlations")
    os.makedirs(correlations_dir, exist_ok=True)
    print(f"Saving individual property distributions to: {correlations_dir}")

    properties = [
        ('virial_ratio', 'Virial Ratio'),
        ('angular_momentum', 'Angular Momentum'),
        ('min_separation', 'Minimum Separation'),
        ('max_energy_error', 'Max Energy Error')
    ]
    thresholds = {
        'virial_ratio': 1.0,
        'min_separation': 0.01,
        'max_energy_error': 0.01
    }

    plot_generated = False
    for key, label in properties:
        if key not in df_all.columns or df_all[key].isna().all():
            print(f"  - Skipping {label} plot: no data available.")
            continue

        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.kdeplot(df_all[key].dropna(), ax=ax, fill=True, color='lightgray', label='All')
        if not df_pass.empty and key in df_pass.columns and not df_pass[key].isna().all():
            sns.kdeplot(df_pass[key].dropna(), ax=ax, color='tab:blue', label='Passed')
        if key in thresholds:
            ax.axvline(thresholds[key], color='red', ls='--', lw=1,
                       label=f'Threshold ({thresholds[key]})')
        ax.set_xlabel(label)
        ax.set_ylabel("Density")
        ax.set_title(f"Distribution for {label}: All vs Passed")
        ax.legend()
        
        plt.tight_layout()
        
        filename = f"{key.replace('_', '-')}-distribution.png"
        out_path = os.path.join(correlations_dir, filename)
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        print(f"  - Saved: {out_path}")
        plt.close(fig)
        plot_generated = True

    if not plot_generated:
        print("No comparison distributions were generated due to lack of data.")

    # This function now saves files directly and does not return a figure.
    return None

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
    results_dir = "3_Body_Problem/prescreen_stage2/prescreen_run_results"
    output_dir = "3_Body_Problem/prescreen_stage2/analysis_output"
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
    plot_comparison_distributions(results, output_dir)  # This now saves files directly
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
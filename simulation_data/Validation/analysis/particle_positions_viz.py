"""
Visualization of particle positions for hierarchical three-body systems
Creates comprehensive visualizations showing the distribution and patterns
of initial conditions across the hierarchical dataset.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from utils import parse_ic_file, calculate_hierarchical_properties, get_sample_files
import os
from matplotlib.patches import Circle
import matplotlib.patches as mpatches


def analyze_hierarchical_dataset(ic_dir):
    """Analyze the full hierarchical dataset to understand patterns"""
    
    # Get comprehensive sample - using stratified sampling for representative coverage
    sample_files = get_sample_files(ic_dir, sample_size=200, strategy='stratified')
    
    # Storage for analysis
    all_positions = []
    binary_separations = []
    hierarchical_ratios = []
    com_distances = []
    distant_particles = []
    
    print(f"Analyzing {len(sample_files)} files from hierarchical dataset...")
    
    for i, filepath in enumerate(sample_files):
        if i % 50 == 0:
            print(f"  Processing file {i+1}/{len(sample_files)}...")
        
        positions, velocities = parse_ic_file(filepath)
        all_positions.append(positions)
        
        # Calculate hierarchical properties
        hier_props = calculate_hierarchical_properties(positions)
        binary_separations.append(hier_props['binary_separation'])
        hierarchical_ratios.append(hier_props['hierarchical_ratio'])
        com_distances.append(hier_props['com_distance'])
        distant_particles.append(hier_props['distant_particle'])
    
    return {
        'positions': np.array(all_positions),
        'binary_separations': np.array(binary_separations),
        'hierarchical_ratios': np.array(hierarchical_ratios),
        'com_distances': np.array(com_distances),
        'distant_particles': np.array(distant_particles),
        'sample_files': sample_files
    }


def create_3d_scatter_overview(data, output_dir):
    """Create 3D scatter plot showing all sampled systems"""
    fig = plt.figure(figsize=(15, 12))
    
    # Main 3D view
    ax = fig.add_subplot(221, projection='3d')
    
    positions = data['positions']
    n_systems = len(positions)
    
    # Color particles by their index
    colors = ['red', 'blue', 'green']
    markers = ['o', '^', 's']
    
    for particle_idx in range(3):
        # Extract positions for this particle across all systems
        x = positions[:, particle_idx, 0]
        y = positions[:, particle_idx, 1]
        z = positions[:, particle_idx, 2]
        
        ax.scatter(x, y, z, c=colors[particle_idx], marker=markers[particle_idx], 
                  s=30, alpha=0.6, label=f'Particle {particle_idx}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D Distribution of Particles ({n_systems} Systems)', fontsize=14)
    ax.legend()
    
    # Add projections
    # XY projection
    ax2 = fig.add_subplot(222)
    for particle_idx in range(3):
        x = positions[:, particle_idx, 0]
        y = positions[:, particle_idx, 1]
        ax2.scatter(x, y, c=colors[particle_idx], marker=markers[particle_idx], 
                   s=20, alpha=0.5, label=f'Particle {particle_idx}')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('XY Projection')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # XZ projection
    ax3 = fig.add_subplot(223)
    for particle_idx in range(3):
        x = positions[:, particle_idx, 0]
        z = positions[:, particle_idx, 2]
        ax3.scatter(x, z, c=colors[particle_idx], marker=markers[particle_idx], 
                   s=20, alpha=0.5, label=f'Particle {particle_idx}')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z')
    ax3.set_title('XZ Projection')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # YZ projection
    ax4 = fig.add_subplot(224)
    for particle_idx in range(3):
        y = positions[:, particle_idx, 1]
        z = positions[:, particle_idx, 2]
        ax4.scatter(y, z, c=colors[particle_idx], marker=markers[particle_idx], 
                   s=20, alpha=0.5, label=f'Particle {particle_idx}')
    ax4.set_xlabel('Y')
    ax4.set_ylabel('Z')
    ax4.set_title('YZ Projection')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'particle_positions_3d_overview.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_hierarchical_properties_plot(data, output_dir):
    """Visualize hierarchical properties of the systems"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Binary separation distribution
    ax = axes[0, 0]
    ax.hist(data['binary_separations'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Binary Separation')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Binary Separations')
    ax.grid(True, alpha=0.3)
    
    # Hierarchical ratio distribution
    ax = axes[0, 1]
    ax.hist(data['hierarchical_ratios'], bins=50, color='darkgreen', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Hierarchical Ratio (distant/binary separation)')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Hierarchical Ratios')
    ax.grid(True, alpha=0.3)
    
    # COM distance distribution
    ax = axes[1, 0]
    ax.hist(data['com_distances'], bins=50, color='darkred', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Distance from Binary COM to Distant Particle')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of COM Distances')
    ax.grid(True, alpha=0.3)
    
    # Scatter plot: Binary separation vs COM distance
    ax = axes[1, 1]
    scatter = ax.scatter(data['binary_separations'], data['com_distances'], 
                        c=data['hierarchical_ratios'], cmap='viridis', 
                        alpha=0.6, s=30)
    ax.set_xlabel('Binary Separation')
    ax.set_ylabel('COM Distance')
    ax.set_title('Binary Separation vs COM Distance')
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Hierarchical Ratio')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hierarchical_properties.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_example_systems_plot(data, output_dir, n_examples=12):
    """Show individual example systems to illustrate hierarchical structure"""
    fig = plt.figure(figsize=(16, 12))
    
    # Select diverse examples based on hierarchical ratio
    ratios = data['hierarchical_ratios']
    # Get examples from different ratio ranges
    ratio_percentiles = np.percentile(ratios, np.linspace(0, 100, n_examples))
    example_indices = []
    for pct in ratio_percentiles:
        idx = np.argmin(np.abs(ratios - pct))
        example_indices.append(idx)
    
    for i, idx in enumerate(example_indices):
        ax = fig.add_subplot(3, 4, i+1, projection='3d')
        
        positions = data['positions'][idx]
        hier_props = calculate_hierarchical_properties(positions)
        
        # Plot particles with different sizes based on role
        for j in range(3):
            if j in hier_props['binary_pair']:
                # Binary particles - smaller
                size = 100
                alpha = 0.8
            else:
                # Distant particle - larger
                size = 150
                alpha = 0.6
            
            color = ['red', 'blue', 'green'][j]
            ax.scatter(positions[j, 0], positions[j, 1], positions[j, 2], 
                      c=color, s=size, alpha=alpha, edgecolors='black', linewidth=1)
        
        # Draw line between binary pair
        binary = hier_props['binary_pair']
        ax.plot([positions[binary[0], 0], positions[binary[1], 0]],
                [positions[binary[0], 1], positions[binary[1], 1]],
                [positions[binary[0], 2], positions[binary[1], 2]],
                'k--', alpha=0.5, linewidth=1)
        
        # Set axis limits
        all_coords = positions.flatten()
        margin = 0.1 * (all_coords.max() - all_coords.min())
        ax.set_xlim([all_coords.min() - margin, all_coords.max() + margin])
        ax.set_ylim([all_coords.min() - margin, all_coords.max() + margin])
        ax.set_zlim([all_coords.min() - margin, all_coords.max() + margin])
        
        ax.set_title(f'Ratio: {hier_props["hierarchical_ratio"]:.2f}', fontsize=10)
        
        # Remove tick labels for cleaner look
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
    
    plt.suptitle('Example Hierarchical Systems (sorted by hierarchical ratio)', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'example_hierarchical_systems.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_particle_role_analysis(data, output_dir):
    """Analyze which particles tend to be in which roles"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Count which particle is distant
    distant_counts = np.bincount(data['distant_particles'])
    
    ax1.bar(range(len(distant_counts)), distant_counts, color=['red', 'blue', 'green'])
    ax1.set_xlabel('Particle Index')
    ax1.set_ylabel('Count as Distant Particle')
    ax1.set_title('Frequency of Each Particle Being Distant')
    ax1.set_xticks(range(3))
    
    # Analyze position distributions by role
    positions = data['positions']
    n_systems = len(positions)
    
    # Separate positions by role
    distant_positions = []
    binary_positions = []
    
    for i in range(n_systems):
        hier_props = calculate_hierarchical_properties(positions[i])
        distant_idx = hier_props['distant_particle']
        binary_idx = list(hier_props['binary_pair'])
        
        distant_positions.append(positions[i, distant_idx])
        binary_positions.extend([positions[i, idx] for idx in binary_idx])
    
    distant_positions = np.array(distant_positions)
    binary_positions = np.array(binary_positions)
    
    # Plot position distributions
    ax2.hist(np.linalg.norm(distant_positions, axis=1), bins=30, alpha=0.5, 
             label='Distant particles', color='orange')
    ax2.hist(np.linalg.norm(binary_positions, axis=1), bins=30, alpha=0.5, 
             label='Binary particles', color='purple')
    ax2.set_xlabel('Distance from Origin')
    ax2.set_ylabel('Count')
    ax2.set_title('Position Distribution by Role')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'particle_role_analysis.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_configuration_space_plot(data, output_dir):
    """Visualize the configuration space coverage"""
    fig = plt.figure(figsize=(14, 10))
    
    positions = data['positions']
    
    # Calculate relative vectors for each system
    rel_vectors = []
    for pos in positions:
        # Vector from particle 0 to 1
        v01 = pos[1] - pos[0]
        # Vector from particle 0 to 2
        v02 = pos[2] - pos[0]
        rel_vectors.append([v01, v02])
    
    rel_vectors = np.array(rel_vectors)
    
    # Plot relative configuration space
    ax1 = fig.add_subplot(221)
    # Magnitude of relative vectors
    mag_v01 = np.linalg.norm(rel_vectors[:, 0], axis=1)
    mag_v02 = np.linalg.norm(rel_vectors[:, 1], axis=1)
    
    scatter = ax1.scatter(mag_v01, mag_v02, c=data['hierarchical_ratios'], 
                         cmap='plasma', alpha=0.6, s=20)
    ax1.set_xlabel('|r₁ - r₀|')
    ax1.set_ylabel('|r₂ - r₀|')
    ax1.set_title('Relative Distance Configuration Space')
    plt.colorbar(scatter, ax=ax1, label='Hierarchical Ratio')
    
    # Angular distribution
    ax2 = fig.add_subplot(222)
    # Calculate angles between relative vectors
    angles = []
    for v01, v02 in rel_vectors:
        cos_angle = np.dot(v01, v02) / (np.linalg.norm(v01) * np.linalg.norm(v02))
        angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
        angles.append(angle)
    
    ax2.hist(angles, bins=50, color='darkblue', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Angle between (r₁-r₀) and (r₂-r₀) [degrees]')
    ax2.set_ylabel('Count')
    ax2.set_title('Angular Distribution in Configuration Space')
    ax2.grid(True, alpha=0.3)
    
    # Phase space slice - positions vs velocities magnitude
    ax3 = fig.add_subplot(223)
    velocities_data = []
    positions_mag = []
    
    # Read velocities for a subset
    subset_files = data['sample_files'][:100]  # Use first 100 for clarity
    for filepath in subset_files:
        pos, vel = parse_ic_file(filepath)
        positions_mag.extend(np.linalg.norm(pos, axis=1))
        velocities_data.extend(np.linalg.norm(vel, axis=1))
    
    ax3.scatter(positions_mag, velocities_data, alpha=0.4, s=10, c='darkgreen')
    ax3.set_xlabel('Position Magnitude')
    ax3.set_ylabel('Velocity Magnitude')
    ax3.set_title('Phase Space Projection (subset)')
    ax3.grid(True, alpha=0.3)
    
    # Hierarchical ratio vs angle
    ax4 = fig.add_subplot(224)
    ax4.scatter(angles, data['hierarchical_ratios'], alpha=0.5, s=20, c='darkred')
    ax4.set_xlabel('Angle between relative vectors [degrees]')
    ax4.set_ylabel('Hierarchical Ratio')
    ax4.set_title('Hierarchical Structure vs Angular Configuration')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'configuration_space_analysis.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def main():
    # Paths
    ic_dir = "<home>/Desktop/3_body_problem/simulation_data/Data/ic_final/ic_hierarchical"
    output_dir = "<home>/Desktop/3_body_problem/simulation_data/Validation/analysis/figures/hierarchical_positions"
    
    print("Starting comprehensive analysis of hierarchical systems...")
    
    # Analyze dataset
    data = analyze_hierarchical_dataset(ic_dir)
    
    print(f"\nDataset statistics:")
    print(f"  Number of systems analyzed: {len(data['positions'])}")
    print(f"  Mean binary separation: {np.mean(data['binary_separations']):.4f}")
    print(f"  Mean hierarchical ratio: {np.mean(data['hierarchical_ratios']):.4f}")
    print(f"  Hierarchical ratio range: [{np.min(data['hierarchical_ratios']):.2f}, {np.max(data['hierarchical_ratios']):.2f}]")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    print("  1. 3D scatter overview...")
    create_3d_scatter_overview(data, output_dir)
    
    print("  2. Hierarchical properties...")
    create_hierarchical_properties_plot(data, output_dir)
    
    print("  3. Example systems...")
    create_example_systems_plot(data, output_dir)
    
    print("  4. Particle role analysis...")
    create_particle_role_analysis(data, output_dir)
    
    print("  5. Configuration space analysis...")
    create_configuration_space_plot(data, output_dir)
    
    print("\nAll visualizations saved to:", output_dir)


if __name__ == "__main__":
    main()

"""
Visualization of the reference plane for particle 2 sampling
Shows the 3D sampling space and valid positions for quasi-random sampling
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.offline as pyo
from matplotlib.patches import Circle
import os


def create_reference_plane_static(output_dir):
    """Create static matplotlib visualizations of the reference plane"""
    
    # Parameters for the reference plane
    # Assuming particle 2 is sampled on a hemisphere or spherical section
    radius = 2.0  # Example radius
    
    # Create spherical grid
    theta = np.linspace(0, 2*np.pi, 100)  # Azimuthal angle
    phi = np.linspace(0, np.pi/2, 50)     # Polar angle (hemisphere)
    
    THETA, PHI = np.meshgrid(theta, phi)
    
    # Convert to Cartesian coordinates
    X = radius * np.sin(PHI) * np.cos(THETA)
    Y = radius * np.sin(PHI) * np.sin(THETA)
    Z = radius * np.cos(PHI)
    
    # Create figure with multiple views
    fig = plt.figure(figsize=(16, 12))
    
    # 3D view
    ax1 = fig.add_subplot(221, projection='3d')
    
    # Plot the hemisphere surface
    surf = ax1.plot_surface(X, Y, Z, alpha=0.3, cmap='viridis', 
                           linewidth=0, antialiased=True)
    
    # Add wireframe for better visibility
    ax1.plot_wireframe(X, Y, Z, alpha=0.1, color='black', linewidth=0.5)
    
    # Add coordinate axes
    axis_length = radius * 1.5
    ax1.plot([0, axis_length], [0, 0], [0, 0], 'r-', linewidth=2, label='X')
    ax1.plot([0, 0], [0, axis_length], [0, 0], 'g-', linewidth=2, label='Y')
    ax1.plot([0, 0], [0, 0], [0, axis_length], 'b-', linewidth=2, label='Z')
    
    # Add sample points
    n_samples = 50
    sample_theta = np.random.uniform(0, 2*np.pi, n_samples)
    sample_phi = np.random.uniform(0, np.pi/2, n_samples)
    
    sample_x = radius * np.sin(sample_phi) * np.cos(sample_theta)
    sample_y = radius * np.sin(sample_phi) * np.sin(sample_theta)
    sample_z = radius * np.cos(sample_phi)
    
    ax1.scatter(sample_x, sample_y, sample_z, c='red', s=20, alpha=0.8, 
               label='Sample Points')
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3D Reference Plane for Particle 2 Sampling', fontsize=14)
    ax1.legend()
    
    # Set equal aspect ratio
    ax1.set_box_aspect([1,1,0.5])
    
    # Top view (XY projection)
    ax2 = fig.add_subplot(222)
    # Draw circle boundary
    circle = Circle((0, 0), radius, fill=False, edgecolor='black', linewidth=2)
    ax2.add_patch(circle)
    
    # Project hemisphere onto XY plane
    ax2.scatter(sample_x, sample_y, c=sample_z, cmap='viridis', s=30, alpha=0.7)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Top View (XY Projection)')
    ax2.set_xlim(-radius*1.2, radius*1.2)
    ax2.set_ylim(-radius*1.2, radius*1.2)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(ax2.scatter(sample_x, sample_y, c=sample_z, cmap='viridis'), ax=ax2)
    cbar.set_label('Z coordinate')
    
    # Side view (XZ projection)
    ax3 = fig.add_subplot(223)
    # Draw hemisphere outline
    phi_outline = np.linspace(0, np.pi/2, 100)
    x_outline = radius * np.sin(phi_outline)
    z_outline = radius * np.cos(phi_outline)
    ax3.plot(x_outline, z_outline, 'k-', linewidth=2)
    ax3.plot([-radius, radius], [0, 0], 'k-', linewidth=2)
    
    ax3.scatter(sample_x, sample_z, c='red', s=30, alpha=0.7)
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z')
    ax3.set_title('Side View (XZ Projection)')
    ax3.set_xlim(-radius*1.2, radius*1.2)
    ax3.set_ylim(-0.2*radius, radius*1.2)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    
    # Angular distribution
    ax4 = fig.add_subplot(224, projection='polar')
    ax4.scatter(sample_theta, sample_phi * 180/np.pi, c='red', s=30, alpha=0.7)
    ax4.set_ylim(0, 90)
    ax4.set_title('Angular Distribution (θ, φ)', y=1.08)
    ax4.set_ylabel('φ (degrees)', labelpad=30)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reference_plane_static.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_reference_plane_interactive(output_dir):
    """Create interactive Plotly visualization of the reference plane"""
    
    # Parameters
    radius = 2.0
    
    # Create finer grid for smooth surface
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi/2, 50)
    
    THETA, PHI = np.meshgrid(theta, phi)
    
    X = radius * np.sin(PHI) * np.cos(THETA)
    Y = radius * np.sin(PHI) * np.sin(THETA)
    Z = radius * np.cos(PHI)
    
    # Create the figure
    fig = go.Figure()
    
    # Add hemisphere surface
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        opacity=0.3,
        showscale=False,
        name='Reference Plane'
    ))
    
    # Add wireframe
    # Sample fewer lines for wireframe
    theta_wire = theta[::10]
    phi_wire = phi[::5]
    
    # Longitude lines
    for t in theta_wire:
        x_line = radius * np.sin(phi) * np.cos(t)
        y_line = radius * np.sin(phi) * np.sin(t)
        z_line = radius * np.cos(phi)
        fig.add_trace(go.Scatter3d(
            x=x_line, y=y_line, z=z_line,
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False
        ))
    
    # Latitude lines
    for p in phi_wire:
        x_line = radius * np.sin(p) * np.cos(theta)
        y_line = radius * np.sin(p) * np.sin(theta)
        z_line = radius * np.cos(p) * np.ones_like(theta)
        fig.add_trace(go.Scatter3d(
            x=x_line, y=y_line, z=z_line,
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False
        ))
    
    # Add coordinate axes
    axis_length = radius * 1.5
    # X-axis
    fig.add_trace(go.Scatter3d(
        x=[0, axis_length], y=[0, 0], z=[0, 0],
        mode='lines+text',
        line=dict(color='red', width=5),
        text=['', 'X'],
        textposition='top center',
        showlegend=False
    ))
    
    # Y-axis
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, axis_length], z=[0, 0],
        mode='lines+text',
        line=dict(color='green', width=5),
        text=['', 'Y'],
        textposition='top center',
        showlegend=False
    ))
    
    # Z-axis
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, axis_length],
        mode='lines+text',
        line=dict(color='blue', width=5),
        text=['', 'Z'],
        textposition='top center',
        showlegend=False
    ))
    
    # Add sample points with quasi-random distribution
    n_samples = 100
    # Use Fibonacci spiral for quasi-random sampling
    golden_ratio = (1 + 5**0.5) / 2
    i = np.arange(0, n_samples)
    theta_samples = 2 * np.pi * i / golden_ratio
    phi_samples = np.arccos(1 - 2 * i / n_samples) * 0.5  # Scale to hemisphere
    
    x_samples = radius * np.sin(phi_samples) * np.cos(theta_samples)
    y_samples = radius * np.sin(phi_samples) * np.sin(theta_samples)
    z_samples = radius * np.cos(phi_samples)
    
    fig.add_trace(go.Scatter3d(
        x=x_samples, y=y_samples, z=z_samples,
        mode='markers',
        marker=dict(
            size=5,
            color=z_samples,
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title='Z coordinate')
        ),
        name='Quasi-Random Samples'
    ))
    
    # Add annotations
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=10, color='black'),
        text=['Origin (Binary COM)'],
        textposition='bottom center',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Interactive 3D Reference Plane for Particle 2 Sampling',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=True,
        width=1000,
        height=800
    )
    
    # Save as HTML
    output_file = os.path.join(output_dir, 'reference_plane_interactive.html')
    pyo.plot(fig, filename=output_file, auto_open=False)
    print(f"    Interactive plot saved to: {output_file}")


def create_sampling_method_comparison(output_dir):
    """Compare different sampling methods on the reference plane"""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    radius = 2.0
    n_samples = 200
    
    # 1. Uniform random sampling
    ax = axes[0, 0]
    theta_uniform = np.random.uniform(0, 2*np.pi, n_samples)
    phi_uniform = np.random.uniform(0, np.pi/2, n_samples)
    x_uniform = radius * np.sin(phi_uniform) * np.cos(theta_uniform)
    y_uniform = radius * np.sin(phi_uniform) * np.sin(theta_uniform)
    
    circle = Circle((0, 0), radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(circle)
    ax.scatter(x_uniform, y_uniform, s=10, alpha=0.6, c='blue')
    ax.set_title('Uniform Random Sampling')
    ax.set_aspect('equal')
    ax.set_xlim(-radius*1.1, radius*1.1)
    ax.set_ylim(-radius*1.1, radius*1.1)
    
    # 2. Quasi-random (Fibonacci spiral)
    ax = axes[0, 1]
    golden_ratio = (1 + 5**0.5) / 2
    i = np.arange(0, n_samples)
    theta_quasi = 2 * np.pi * i / golden_ratio
    phi_quasi = np.arccos(1 - 2 * i / n_samples) * 0.5
    x_quasi = radius * np.sin(phi_quasi) * np.cos(theta_quasi)
    y_quasi = radius * np.sin(phi_quasi) * np.sin(theta_quasi)
    
    circle = Circle((0, 0), radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(circle)
    ax.scatter(x_quasi, y_quasi, s=10, alpha=0.6, c='green')
    ax.set_title('Quasi-Random (Fibonacci Spiral)')
    ax.set_aspect('equal')
    ax.set_xlim(-radius*1.1, radius*1.1)
    ax.set_ylim(-radius*1.1, radius*1.1)
    
    # 3. Grid sampling
    ax = axes[0, 2]
    n_theta = int(np.sqrt(n_samples) * 2)
    n_phi = int(np.sqrt(n_samples) / 2)
    theta_grid = np.linspace(0, 2*np.pi, n_theta, endpoint=False)
    phi_grid = np.linspace(0, np.pi/2, n_phi)
    THETA_GRID, PHI_GRID = np.meshgrid(theta_grid, phi_grid)
    x_grid = radius * np.sin(PHI_GRID.flatten()) * np.cos(THETA_GRID.flatten())
    y_grid = radius * np.sin(PHI_GRID.flatten()) * np.sin(THETA_GRID.flatten())
    
    circle = Circle((0, 0), radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(circle)
    ax.scatter(x_grid, y_grid, s=10, alpha=0.6, c='red')
    ax.set_title('Grid Sampling')
    ax.set_aspect('equal')
    ax.set_xlim(-radius*1.1, radius*1.1)
    ax.set_ylim(-radius*1.1, radius*1.1)
    
    # Angular distributions
    for i, (theta, phi, title, color) in enumerate([
        (theta_uniform, phi_uniform, 'Uniform', 'blue'),
        (theta_quasi, phi_quasi, 'Quasi-Random', 'green'),
        (THETA_GRID.flatten(), PHI_GRID.flatten(), 'Grid', 'red')
    ]):
        ax = axes[1, i]
        ax.hist2d(theta, phi*180/np.pi, bins=20, cmap='viridis')
        ax.set_xlabel('θ (radians)')
        ax.set_ylabel('φ (degrees)')
        ax.set_title(f'{title} - Angular Distribution')
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(0, 90)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sampling_methods_comparison.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_constraint_visualization(output_dir):
    """Visualize constraints on particle 2 placement"""
    
    fig = plt.figure(figsize=(14, 10))
    
    # Constraint parameters
    radius_min = 1.5
    radius_max = 3.0
    phi_max = np.pi/3  # 60 degrees
    
    # Create constrained region
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, phi_max, 50)
    
    # 3D visualization of constraints
    ax1 = fig.add_subplot(221, projection='3d')
    
    # Inner boundary
    THETA, PHI = np.meshgrid(theta, phi)
    X_inner = radius_min * np.sin(PHI) * np.cos(THETA)
    Y_inner = radius_min * np.sin(PHI) * np.sin(THETA)
    Z_inner = radius_min * np.cos(PHI)
    
    # Outer boundary
    X_outer = radius_max * np.sin(PHI) * np.cos(THETA)
    Y_outer = radius_max * np.sin(PHI) * np.sin(THETA)
    Z_outer = radius_max * np.cos(PHI)
    
    ax1.plot_surface(X_inner, Y_inner, Z_inner, alpha=0.3, color='red', label='Min radius')
    ax1.plot_surface(X_outer, Y_outer, Z_outer, alpha=0.3, color='blue', label='Max radius')
    
    # Add valid sample region
    n_samples = 50
    r_samples = np.random.uniform(radius_min, radius_max, n_samples)
    theta_samples = np.random.uniform(0, 2*np.pi, n_samples)
    phi_samples = np.random.uniform(0, phi_max, n_samples)
    
    x_samples = r_samples * np.sin(phi_samples) * np.cos(theta_samples)
    y_samples = r_samples * np.sin(phi_samples) * np.sin(theta_samples)
    z_samples = r_samples * np.cos(phi_samples)
    
    ax1.scatter(x_samples, y_samples, z_samples, c='green', s=30, alpha=0.8)
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Constrained Sampling Region')
    
    # Top view with constraints
    ax2 = fig.add_subplot(222)
    # Draw annulus
    outer_circle = Circle((0, 0), radius_max, fill=False, edgecolor='blue', linewidth=2)
    inner_circle = Circle((0, 0), radius_min, fill=False, edgecolor='red', linewidth=2)
    ax2.add_patch(outer_circle)
    ax2.add_patch(inner_circle)
    
    # Fill valid region
    radii = np.linspace(radius_min, radius_max, 20)
    angles = np.linspace(0, 2*np.pi, 100)
    for r in radii:
        x_ring = r * np.cos(angles)
        y_ring = r * np.sin(angles)
        ax2.plot(x_ring, y_ring, 'gray', alpha=0.1, linewidth=0.5)
    
    ax2.scatter(x_samples, y_samples, c=z_samples, cmap='viridis', s=30, alpha=0.7)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Top View - Valid Annulus Region')
    ax2.set_aspect('equal')
    ax2.set_xlim(-radius_max*1.1, radius_max*1.1)
    ax2.set_ylim(-radius_max*1.1, radius_max*1.1)
    
    # Radial distribution
    ax3 = fig.add_subplot(223)
    ax3.hist(r_samples, bins=20, color='green', alpha=0.7, edgecolor='black')
    ax3.axvline(radius_min, color='red', linestyle='--', linewidth=2, label='Min radius')
    ax3.axvline(radius_max, color='blue', linestyle='--', linewidth=2, label='Max radius')
    ax3.set_xlabel('Radial Distance')
    ax3.set_ylabel('Count')
    ax3.set_title('Radial Distribution of Samples')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Angular constraint visualization
    ax4 = fig.add_subplot(224, projection='polar')
    # Show angular limit
    theta_limit = np.linspace(0, 2*np.pi, 100)
    r_limit = np.ones_like(theta_limit) * phi_max
    ax4.plot(theta_limit, r_limit * 180/np.pi, 'r--', linewidth=2, label=f'φ max = {phi_max*180/np.pi:.0f}°')
    
    ax4.scatter(theta_samples, phi_samples * 180/np.pi, c='green', s=30, alpha=0.7)
    ax4.set_ylim(0, 90)
    ax4.set_title('Angular Constraints', y=1.08)
    ax4.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sampling_constraints.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()


def main():
    output_dir = "<home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/figures/reference_plane"
    
    print("Creating reference plane visualizations...")
    
    print("  1. Static reference plane views...")
    create_reference_plane_static(output_dir)
    
    print("  2. Interactive 3D reference plane...")
    create_reference_plane_interactive(output_dir)
    
    print("  3. Sampling method comparison...")
    create_sampling_method_comparison(output_dir)
    
    print("  4. Constraint visualization...")
    create_constraint_visualization(output_dir)
    
    print(f"\nAll visualizations saved to: {output_dir}")


if __name__ == "__main__":
    main()

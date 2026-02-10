
import xarray as xr
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Import node and element data
import sys
sys.path.append('data')
from node import nodes
from element import members


# Configuration
OUTPUT_FOLDER = "output"
XARRAY_DATA_PATH = "data/screening_task (2).nc"

# Define all 5 girders
GIRDERS = {
    'Girder 1': {
        'elements': [13, 22, 31, 40, 49, 58, 67, 76, 81],
        'nodes': [1, 11, 16, 21, 26, 31, 36, 41, 46, 6],
        'color': 'red'
    },
    'Girder 2': {
        'elements': [14, 23, 32, 41, 50, 59, 68, 77, 82],
        'nodes': [2, 12, 17, 22, 27, 32, 37, 42, 47, 7],
        'color': 'orange'
    },
    'Girder 3': {
        'elements': [15, 24, 33, 42, 51, 60, 69, 78, 83],
        'nodes': [3, 13, 18, 23, 28, 33, 38, 43, 48, 8],
        'color': 'green'
    },
    'Girder 4': {
        'elements': [16, 25, 34, 43, 52, 61, 70, 79, 84],
        'nodes': [4, 14, 19, 24, 29, 34, 39, 44, 49, 9],
        'color': 'blue'
    },
    'Girder 5': {
        'elements': [17, 26, 35, 44, 53, 62, 71, 80, 85],
        'nodes': [5, 15, 20, 25, 30, 35, 40, 45, 50, 10],
        'color': 'purple'
    }
}

HATCHING_DENSITY = 8  # Increase for more hatching (5-15 recommended)


os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_xarray_data(file_path):
    ds = xr.open_dataset(file_path)
    print(f"Loaded dataset: {ds.dims}")
    return ds

def extract_girder_forces(dataset, element_ids):
    #Extract Mz and Vy values for specified elements
    forces = dataset['forces']
    girder_forces = forces.sel(Element=element_ids)
    
    mz_i = girder_forces.sel(Component='Mz_i').values
    mz_j = girder_forces.sel(Component='Mz_j').values
    vy_i = girder_forces.sel(Component='Vy_i').values
    vy_j = girder_forces.sel(Component='Vy_j').values
    
    mz_values = np.concatenate([mz_i, [mz_j[-1]]])
    vy_values = np.concatenate([vy_i, [vy_j[-1]]])
    
    return mz_values, vy_values


def create_interpolated_points(x_coords, y_coords, z_coords, density=8):
    # Create interpolated points for denser hatching
    x_interp, y_interp, z_interp = [], [], []
    
    for i in range(len(x_coords) - 1):
        x_seg = np.linspace(x_coords[i], x_coords[i+1], density + 2)
        y_seg = np.linspace(y_coords[i], y_coords[i+1], density + 2)
        z_seg = np.linspace(z_coords[i], z_coords[i+1], density + 2)
        
        x_interp.extend(x_seg)
        y_interp.extend(y_seg)
        z_interp.extend(z_seg)
    
    return x_interp, y_interp, z_interp


def create_3d_bridge_frame():
    # Create the base bridge frame structure
    frame_lines_x = []
    frame_lines_y = []
    frame_lines_z = []
    
    for elem_id, node_pair in members.items():
        node_start, node_end = node_pair
        x1, y1, z1 = nodes[node_start]
        x2, y2, z2 = nodes[node_end]
        
        frame_lines_x.extend([x1, x2, None])
        frame_lines_y.extend([y1, y2, None])
        frame_lines_z.extend([z1, z2, None])
    
    return frame_lines_x, frame_lines_y, frame_lines_z

def plot_3d_bmd(dataset, scale_factor=0.5):
    #Create 3D Bending Moment Diagram
    
    fig = go.Figure()
    
    # Add bridge frame
    frame_x, frame_y, frame_z = create_3d_bridge_frame()
    fig.add_trace(go.Scatter3d(
        x=frame_x, y=frame_y, z=frame_z,
        mode='lines',
        line=dict(color='lightgray', width=2),
        name='Bridge Frame',
        showlegend=True
    ))
    
    # Plot each girder with extruded moments
    for girder_name, girder_info in GIRDERS.items():
        element_ids = girder_info['elements']
        node_ids = girder_info['nodes']
        color = girder_info['color']
        
        # Get moment values
        mz_values, _ = extract_girder_forces(dataset, element_ids)
        
        # Get node coordinates
        x_coords = [nodes[nid][0] for nid in node_ids]
        z_coords = [nodes[nid][2] for nid in node_ids]
        
        # Extrude moments in Y direction
        y_coords = [mz * scale_factor for mz in mz_values]
        
        # Plot the extruded moment diagram
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='lines+markers',
            line=dict(color=color, width=4),
            marker=dict(size=4, color=color),
            name=girder_name,
            hovertemplate=f'{girder_name}<br>X: %{{x:.2f}}<br>Mz: %{{y:.2f}} kN·m<br>Z: %{{z:.2f}}<extra></extra>'
        ))
        
        # Add vertical lines from baseline to moment value
        x_hatch, y_hatch, z_hatch = create_interpolated_points(x_coords, y_coords, z_coords, HATCHING_DENSITY)
        for x, y, z in zip(x_hatch, y_hatch, z_hatch):
            fig.add_trace(go.Scatter3d(
                x=[x, x],
                y=[0, y],
                z=[z, z],
                mode='lines',
                line=dict(color=color, width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Update layout
    fig.update_layout(
        title="3D Bending Moment Diagram (BMD) - All Girders",
        scene=dict(
            xaxis_title="X (m) - Longitudinal",
            yaxis_title="Bending Moment (kN·m)",
            zaxis_title="Z (m) - Transverse",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=0.5)
        ),
        width=1400,
        height=800,
        showlegend=True,
        template='plotly_white'
    )
    
    html_path = os.path.join(OUTPUT_FOLDER, "task2_3d_bmd.html")
    fig.write_html(html_path)
    print(f"3D BMD saved: {html_path}")
    # Add PNG export
    png_path = os.path.join(OUTPUT_FOLDER, "task2_3d_bmd.png")
    fig.write_image(png_path, width=1400, height=800, scale=2)
    print(f"PNG saved: {png_path}")

    fig.show()


def plot_3d_sfd(dataset, scale_factor=2.0):
    # Create 3D Shear Force Diagram
    
    fig = go.Figure()
    
    # Add bridge frame
    frame_x, frame_y, frame_z = create_3d_bridge_frame()
    fig.add_trace(go.Scatter3d(
        x=frame_x, y=frame_y, z=frame_z,
        mode='lines',
        line=dict(color='lightgray', width=2),
        name='Bridge Frame',
        showlegend=True
    ))
    
    # Plot each girder with extruded shear
    for girder_name, girder_info in GIRDERS.items():
        element_ids = girder_info['elements']
        node_ids = girder_info['nodes']
        color = girder_info['color']
        
        # Get shear values
        _, vy_values = extract_girder_forces(dataset, element_ids)
        
        # Get node coordinates
        x_coords = [nodes[nid][0] for nid in node_ids]
        z_coords = [nodes[nid][2] for nid in node_ids]
        
        # Extrude shear in Y direction
        y_coords = [vy * scale_factor for vy in vy_values]
        
        # Plot the extruded shear diagram
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='lines+markers',
            line=dict(color=color, width=4),
            marker=dict(size=4, color=color),
            name=girder_name,
            hovertemplate=f'{girder_name}<br>X: %{{x:.2f}}<br>Vy: %{{y:.2f}} kN<br>Z: %{{z:.2f}}<extra></extra>'
        ))
        
        # Add vertical lines from baseline to shear value
        x_hatch, y_hatch, z_hatch = create_interpolated_points(x_coords, y_coords, z_coords, HATCHING_DENSITY)
        for x, y, z in zip(x_hatch, y_hatch, z_hatch):
            fig.add_trace(go.Scatter3d(
                x=[x, x],
                y=[0, y],
                z=[z, z],
                mode='lines',
                line=dict(color=color, width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    # Update layout
    fig.update_layout(
        title="3D Shear Force Diagram (SFD) - All Girders",
        scene=dict(
            xaxis_title="X (m) - Longitudinal",
            yaxis_title="Shear Force (kN)",
            zaxis_title="Z (m) - Transverse",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=0.5)
        ),
        width=1400,
        height=800,
        showlegend=True,
        template='plotly_white'
    )
    
    html_path = os.path.join(OUTPUT_FOLDER, "task2_3d_sfd.html")
    fig.write_html(html_path)
    print(f" 3D SFD saved: {html_path}")
    # Add PNG export
    png_path = os.path.join(OUTPUT_FOLDER, "task2_3d_sfd.png")
    fig.write_image(png_path, width=1400, height=800, scale=2)
    print(f"PNG saved: {png_path}")
    fig.show()

def plot_combined_3d(dataset):
    # Create combined view with both BMD and SFD side by side
    
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
        subplot_titles=('Bending Moment Diagram (BMD)', 'Shear Force Diagram (SFD)'),
        horizontal_spacing=0.05
    )
    
    # BMD on left
    frame_x, frame_y, frame_z = create_3d_bridge_frame()
    fig.add_trace(go.Scatter3d(
        x=frame_x, y=frame_y, z=frame_z,
        mode='lines', line=dict(color='lightgray', width=2),
        name='Frame', showlegend=False
    ), row=1, col=1)
    
    for girder_name, girder_info in GIRDERS.items():
        element_ids = girder_info['elements']
        node_ids = girder_info['nodes']
        color = girder_info['color']
        
        mz_values, vy_values = extract_girder_forces(dataset, element_ids)
        
        x_coords = [nodes[nid][0] for nid in node_ids]
        z_coords = [nodes[nid][2] for nid in node_ids]
        
        # BMD
        y_mz = [mz * 0.5 for mz in mz_values]
        fig.add_trace(go.Scatter3d(
            x=x_coords, y=y_mz, z=z_coords,
            mode='lines+markers', line=dict(color=color, width=4),
            marker=dict(size=3), name=girder_name, showlegend=False
        ), row=1, col=1)
        
        # SFD
        y_vy = [vy * 2.0 for vy in vy_values]
        fig.add_trace(go.Scatter3d(
            x=x_coords, y=y_vy, z=z_coords,
            mode='lines+markers', line=dict(color=color, width=4),
            marker=dict(size=3), name=girder_name, showlegend=False
        ), row=1, col=2)
    
    # Add frame to SFD
    fig.add_trace(go.Scatter3d(
        x=frame_x, y=frame_y, z=frame_z,
        mode='lines', line=dict(color='lightgray', width=2),
        name='Frame', showlegend=False
    ), row=1, col=2)
    
    fig.update_layout(
        title_text="3D Force Diagrams - Complete Bridge Analysis",
        width=1600,
        height=700,
        showlegend=False
    )
    
    # Update scene properties
    scene_props = dict(
        xaxis_title="X (m)",
        yaxis_title="Force/Moment",
        zaxis_title="Z (m)",
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        aspectmode='manual',
        aspectratio=dict(x=2, y=1, z=0.5)
    )
    
    fig.update_scenes(scene_props)
    
    html_path = os.path.join(OUTPUT_FOLDER, "task2_3d_combined.html")
    fig.write_html(html_path)
    print(f"✓ Combined 3D plot saved: {html_path}")
    fig.show()

def main():
    print("\n Task 2: 3D SFD & BMD for All Girders")
    print("="*60)
    
    dataset = load_xarray_data(XARRAY_DATA_PATH)
    
    print(f"\n Analyzing {len(GIRDERS)} girders...")
    for name, info in GIRDERS.items():
        print(f"  • {name}: {len(info['elements'])} elements")
    
    print("\nCreating 3D visualizations...")
    plot_3d_bmd(dataset, scale_factor=0.5)
    plot_3d_sfd(dataset, scale_factor=2.0)
    plot_combined_3d(dataset)
    
    print("\nComplete! Check 'output' folder for 3D plots.")
    print("  • task2_3d_bmd.html - Bending Moment Diagram")
    print("  • task2_3d_sfd.html - Shear Force Diagram")
    print("  • task2_3d_combined.html - Both diagrams side-by-side")
    print("="*60)

if __name__ == "__main__":
    main()

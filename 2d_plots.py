import xarray as xr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuration
CENTRAL_GIRDER_ELEMENTS = [15, 24, 33, 42, 51, 60, 69, 78, 83]
XARRAY_DATA_PATH = "data/screening_task (2).nc"
OUTPUT_FOLDER = "output"
HATCHING_DENSITY = 5

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def analyze_all_elements(dataset):
    # Perform statistical analysis on all elements 
    print("\n Analyzing all elements...")
    
    df = dataset.forces.to_dataframe().reset_index()
    pivot_df = df.pivot(index='Element', columns='Component', values='forces')
    pivot_df_clean = pivot_df.dropna(axis=1, how='all')
    
    print(f"Found {len(pivot_df_clean.columns)} force components")
    
    print("\n" + "="*60)
    print("CRITICAL ELEMENTS")
    print("="*60)
    
    for component in pivot_df_clean.columns:
        max_elem = pivot_df_clean[component].abs().idxmax()
        max_val = pivot_df_clean.loc[max_elem, component]
        print(f"{component:12s}: Element {max_elem:2d} = {max_val:10.2f}")
    
    moment_cols = [c for c in pivot_df_clean.columns if 'M' in c]
    shear_cols = [c for c in pivot_df_clean.columns if 'V' in c]
    
    print("\n" + "="*60)
    print("TOP 5 MOMENTS")
    print("="*60)
    moments_df = pivot_df_clean[moment_cols]
    moments_df['Max_Moment'] = moments_df.abs().max(axis=1)
    top_moments = moments_df.nlargest(5, 'Max_Moment')
    print(top_moments)
    
    print("\n" + "="*60)
    print("TOP 5 SHEAR FORCES")
    print("="*60)
    shears_df = pivot_df_clean[shear_cols]
    shears_df['Max_Shear'] = shears_df.abs().max(axis=1)
    top_shears = shears_df.nlargest(5, 'Max_Shear')
    print(top_shears)
    
    pivot_df_clean.to_csv(os.path.join(OUTPUT_FOLDER, 'forces_complete.csv'))
    top_moments.to_csv(os.path.join(OUTPUT_FOLDER, 'critical_moments.csv'))
    top_shears.to_csv(os.path.join(OUTPUT_FOLDER, 'critical_shears.csv'))
    
    print(f"\n Exported: forces_complete.csv, critical_moments.csv, critical_shears.csv")

def load_xarray_data(file_path):
    ds = xr.open_dataset(file_path)
    print(f"✓ Loaded dataset: {ds.dims}")
    return ds

def extract_girder_data(dataset, element_ids):
    forces = dataset['forces']
    girder_forces = forces.sel(Element=element_ids)
    
    mz_i = girder_forces.sel(Component='Mz_i').values
    mz_j = girder_forces.sel(Component='Mz_j').values
    vy_i = girder_forces.sel(Component='Vy_i').values
    vy_j = girder_forces.sel(Component='Vy_j').values
    
    n_elements = len(element_ids)
    mz_values = np.concatenate([mz_i, [mz_j[-1]]])
    vy_values = np.concatenate([vy_i, [vy_j[-1]]])
    positions = np.arange(n_elements + 1)
    
    return mz_values, vy_values, positions

def create_hatching_lines(positions, values, density=5):
    hatching_positions = []
    hatching_values = []
    
    for i in range(len(positions) - 1):
        x_interp = np.linspace(positions[i], positions[i+1], density + 2)
        y_interp = np.linspace(values[i], values[i+1], density + 2)
        hatching_positions.extend(x_interp)
        hatching_values.extend(y_interp)
    
    return np.array(hatching_positions), np.array(hatching_values)

def plot_2d_diagrams_plotly(mz_values, vy_values, positions, element_ids):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Bending Moment Diagram (BMD)', 'Shear Force Diagram (SFD)'),
        vertical_spacing=0.15,
        row_heights=[0.5, 0.5]
    )
    
    hatch_pos_mz, hatch_val_mz = create_hatching_lines(positions, mz_values, HATCHING_DENSITY)
    
    for pos, val in zip(hatch_pos_mz, hatch_val_mz):
        fig.add_trace(
            go.Scatter(x=[pos, pos], y=[0, val], mode='lines',
                      line=dict(color='red', width=1), showlegend=False, hoverinfo='skip'),
            row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(x=positions, y=mz_values, line=dict(color='darkred', width=3),
                  name='Bending Moment', mode='lines+markers', marker=dict(size=8, color='darkred')),
        row=1, col=1
    )
    
    fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=2.5, row=1, col=1)
    
    max_mz_idx = np.argmax(np.abs(mz_values))
    max_mz_val = mz_values[max_mz_idx]
    fig.add_annotation(
        x=positions[max_mz_idx], y=max_mz_val, text=f"Max: {max_mz_val:.2f} kN·m",
        showarrow=True, arrowhead=2, arrowcolor="red", bgcolor="white",
        bordercolor="red", borderwidth=2, row=1, col=1
    )
    
    for i, elem_id in enumerate(element_ids):
        fig.add_annotation(
            x=i + 0.5, y=min(mz_values) * 1.15 if min(mz_values) < 0 else max(mz_values) * 0.1,
            text=f"E{elem_id}", showarrow=False, font=dict(size=9, color="green", family="Arial Black"),
            row=1, col=1
        )
    
    hatch_pos_vy, hatch_val_vy = create_hatching_lines(positions, vy_values, HATCHING_DENSITY)
    
    for pos, val in zip(hatch_pos_vy, hatch_val_vy):
        fig.add_trace(
            go.Scatter(x=[pos, pos], y=[0, val], mode='lines',
                      line=dict(color='blue', width=1), showlegend=False, hoverinfo='skip'),
            row=2, col=1
        )
    
    fig.add_trace(
        go.Scatter(x=positions, y=vy_values, line=dict(color='darkblue', width=3),
                  name='Shear Force', mode='lines+markers', marker=dict(size=8, color='darkblue')),
        row=2, col=1
    )
    
    fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=2.5, row=2, col=1)
    
    max_vy_idx = np.argmax(np.abs(vy_values))
    max_vy_val = vy_values[max_vy_idx]
    fig.add_annotation(
        x=positions[max_vy_idx], y=max_vy_val, text=f"Max: {max_vy_val:.2f} kN",
        showarrow=True, arrowhead=2, arrowcolor="blue", bgcolor="white",
        bordercolor="blue", borderwidth=2, row=2, col=1
    )
    
    fig.update_xaxes(title_text="", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_xaxes(title_text="Position along Girder (Node Index)", row=2, col=1, showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text="Bending Moment (kN·m)", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text="Shear Force (kN)", row=2, col=1, showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    fig.update_layout(
        title_text="Central Longitudinal Girder (Girder 3) - SFD and BMD Analysis",
        title_font_size=16, showlegend=False, height=900, width=1200,
        template='plotly_white', font=dict(size=12)
    )
    
    html_path = os.path.join(OUTPUT_FOLDER, "task1_2d_diagrams.html")
    fig.write_html(html_path)
    print(f"HTML saved: {html_path}")
    fig.show()

def plot_2d_diagrams_matplotlib(mz_values, vy_values, positions, element_ids):
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Central Longitudinal Girder (Girder 3) - SFD and BMD Analysis', 
                 fontsize=18, fontweight='bold')
    
    hatch_pos_mz, hatch_val_mz = create_hatching_lines(positions, mz_values, HATCHING_DENSITY)
    
    for pos, val in zip(hatch_pos_mz, hatch_val_mz):
        ax1.plot([pos, pos], [0, val], 'r-', linewidth=1, alpha=0.6)
    
    ax1.plot(positions, mz_values, 'darkred', linewidth=3, marker='o', markersize=8)
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=2.5)
    ax1.set_xlabel('Position along Girder (Node Index)', fontsize=13)
    ax1.set_ylabel('Bending Moment (kN·m)', fontsize=13, fontweight='bold')
    ax1.set_title('Bending Moment Diagram (BMD)', fontsize=15, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
    
    max_mz_idx = np.argmax(np.abs(mz_values))
    max_mz_val = mz_values[max_mz_idx]
    ax1.annotate(f'Max: {max_mz_val:.2f} kN·m',
                xy=(positions[max_mz_idx], max_mz_val), xytext=(20, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.7', fc='yellow', alpha=0.8, edgecolor='red', linewidth=2),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', color='red', lw=2),
                fontsize=11, fontweight='bold')
    
    for i, elem_id in enumerate(element_ids):
        mid_pos = i + 0.5
        y_pos = min(mz_values) * 1.15 if min(mz_values) < 0 else max(mz_values) * 0.1
        ax1.text(mid_pos, y_pos, f'E{elem_id}', ha='center', va='center',
                fontsize=9, color='green', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.6))
    
    hatch_pos_vy, hatch_val_vy = create_hatching_lines(positions, vy_values, HATCHING_DENSITY)
    
    for pos, val in zip(hatch_pos_vy, hatch_val_vy):
        ax2.plot([pos, pos], [0, val], 'b-', linewidth=1, alpha=0.6)
    
    ax2.plot(positions, vy_values, 'darkblue', linewidth=3, marker='o', markersize=8)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=2.5)
    ax2.set_xlabel('Position along Girder (Node Index)', fontsize=13)
    ax2.set_ylabel('Shear Force (kN)', fontsize=13, fontweight='bold')
    ax2.set_title('Shear Force Diagram (SFD)', fontsize=15, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
    
    max_vy_idx = np.argmax(np.abs(vy_values))
    max_vy_val = vy_values[max_vy_idx]
    ax2.annotate(f'Max: {max_vy_val:.2f} kN',
                xy=(positions[max_vy_idx], max_vy_val), xytext=(20, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.7', fc='yellow', alpha=0.8, edgecolor='blue', linewidth=2),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', color='blue', lw=2),
                fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    png_path = os.path.join(OUTPUT_FOLDER, 'task1_2d_diagrams.png')
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    print(f" PNG saved: {png_path}")
    plt.show()

def main():
    print("\n Bridge Analysis - SFD & BMD")
    print("="*60)
    
    dataset = load_xarray_data(XARRAY_DATA_PATH)
    
    analyze_all_elements(dataset)
    
    print(f"\n Plotting central girder: {CENTRAL_GIRDER_ELEMENTS}")
    mz_values, vy_values, positions = extract_girder_data(dataset, CENTRAL_GIRDER_ELEMENTS)
    
    print(f" Bending Moment: {mz_values.min():.2f} to {mz_values.max():.2f} kN·m")
    print(f" Shear Force: {vy_values.min():.2f} to {vy_values.max():.2f} kN")
    
    print(f"\n Creating diagrams (hatching: {HATCHING_DENSITY}x)...")
    plot_2d_diagrams_plotly(mz_values, vy_values, positions, CENTRAL_GIRDER_ELEMENTS)
    plot_2d_diagrams_matplotlib(mz_values, vy_values, positions, CENTRAL_GIRDER_ELEMENTS)
    
    print("\n Complete! Check 'output' folder for all files.")
    print("="*60)

if __name__ == "__main__":
    main()

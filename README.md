# OSDAG Bridge Screening Assignment - SFD and BMD Visualization

A comprehensive bridge analysis tool for visualizing Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for bridge girders using Python and modern visualization libraries.

## 📋 Project Overview

This project implements two main analysis tasks for a bridge grillage model:

### **Task 1: 2D SFD/BMD for Central Girder**
- Extracts and visualizes shear force and bending moment data for the central longitudinal girder (Elements: 15, 24, 33, 42, 51, 60, 69, 78, 83)
- Creates 2D plots showing force distribution along the girder length
- Includes both interactive (Plotly) and static (Matplotlib) visualizations

### **Task 2: 3D SFD/BMD for All Girders**
- Generates 3D force diagrams for all 5 transverse girders
- Uses extruded visualization style (force values in vertical Y direction)
- Shows both Bending Moment Diagram (BMD) and Shear Force Diagram (SFD)
- Provides MIDAS-style engineering visualization with color-coded girders

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone/Extract the project**
```bash
cd osdag-bridge-analysis
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages**
```bash
pip install xarray netCDF4 plotly matplotlib numpy
```

### Running the Analysis

**Use Jupyter Notebook:**
```bash
jupyter notebook Osdag_Screening_Assignment.ipynb
```

## 📁 Project Structure

```
osdag-bridge-analysis/
├── README.md                              # This file
├── Osdag_Screening_Assignment.ipynb       # Jupyter Notebook (main analysis)
├── screening_task (2).nc                  # Input data (netCDF format)
├── venv/                                  # Virtual environment
└── requirements.txt                       # Python dependencies
```

## 📊 Input Data

**File:** `screening_task (2).nc`

**Format:** NetCDF4 (Xarray compatible)

**Structure:**
- **Element dimension:** 85 elements total
- **Component dimension:** Force components (Vy_i, Vy_j, Mz_i, Mz_j)
- **Forces variable:** Force values at element ends (i and j nodes)

**Girders Configuration:**
- **Girder 1:** Red (#E74C3C) - Elements [13, 22, 31, 40, 49, 58, 67, 76, 81]
- **Girder 2:** Blue (#3498DB) - Elements [14, 23, 32, 41, 50, 59, 68, 77, 82]
- **Girder 3:** Green (#2ECC71) - Elements [15, 24, 33, 42, 51, 60, 69, 78, 83]
- **Girder 4:** Orange (#F39C12) - Elements [16, 25, 34, 43, 52, 61, 70, 79, 84]
- **Girder 5:** Purple (#9B59B6) - Elements [17, 26, 35, 44, 53, 62, 71, 80, 85]

## 📈 Output Visualizations

### Task 1: 2D Diagrams
- **Shear Force Diagram (SFD):** Force distribution along girder length
- **Bending Moment Diagram (BMD):** Moment distribution with filled areas
- **Features:**
  - Data point markers at element ends
  - Value annotations
  - Grid lines and reference axes
  - Responsive Plotly interactive plots
  - High-quality Matplotlib static exports

### Task 2: 3D Diagrams
- **3D Bending Moment Diagram:** All 5 girders with moment values extruded vertically
- **3D Shear Force Diagram:** All 5 girders with shear force values extruded vertically
- **Features:**
  - Baseline representation (girder centerlines)
  - Vertical connector lines between baseline and forces
  - Color-coded by girder
  - Interactive rotation and zoom (Plotly)
  - Professional engineering visualization style

## 💻 Usage Examples

### Jupyter Notebook
Open and run cells sequentially:
```python
# Cell 1: Install libraries
%pip install xarray netCDF4 plotly -q

# Cell 2: Import and load data
import xarray as xr
import numpy as np
ds = xr.open_dataset('screening_task (2).nc')

# Cell 3: Extract central girder data
positions, shear_forces, bending_moments = extract_girder_data(
    ds, central_girder_elements, nodes, members
)

# Cell 4-6: Create and view visualizations
fig_2d = plot_2d_diagrams_plotly(positions, shear_forces, bending_moments)
fig_2d.show()

fig_bmd = create_3d_diagram_plotly(ds, girders_info, nodes, members, 
                                    force_type='Mz', scale_factor=0.01)
fig_bmd.show()
```

### Saving Visualizations
```python
# Save as HTML (interactive)
fig_2d.write_html('Task1_2D_Diagrams.html')
fig_bmd_3d.write_html('Task2_3D_BMD.html')
fig_sfd_3d.write_html('Task2_3D_SFD.html')

# Save as image (static)
# Right-click on Plotly plots and select "Download plot as PNG"
# For Matplotlib: plt.savefig('diagram.png', dpi=300, bbox_inches='tight')
```

## 🔧 Key Functions

### `extract_girder_data()`
Extracts shear force and bending moment data for a specific girder from the dataset.

**Parameters:**
- `ds`: Xarray Dataset
- `element_ids`: List of element IDs forming the girder
- `nodes_dict`: Dictionary of node coordinates
- `members_dict`: Dictionary of element connections

**Returns:** Positions, shear forces, and bending moments arrays

### `plot_2d_diagrams_plotly()`
Creates interactive 2D SFD and BMD plots using Plotly with subplots.

**Parameters:**
- `positions`: X-coordinates along girder
- `shear_forces`: Shear force values
- `bending_moments`: Bending moment values

### `create_3d_diagram_plotly()`
Creates 3D force diagrams for all girders in MIDAS style.

**Parameters:**
- `ds`: Xarray Dataset
- `girders_info_dict`: Dictionary of girder configurations
- `nodes_dict`: Dictionary of node coordinates
- `members_dict`: Dictionary of element connections
- `force_type`: 'Mz' for bending moment or 'Vy' for shear force
- `scale_factor`: Scaling factor for force visualization

## 📊 Bridge Model Details

**Bridge Type:** Grillage Model (5 parallel girders)

**Dimensions:**
- **Longitudinal:** 25.0 m (9 elements per girder)
- **Transverse:** 10.35 m spacing (5 girders)

**Node Count:** 50 nodes total

**Element Count:** 85 elements
- Longitudinal members (deck girders): 45 elements
- Transverse members (diaphragms): 25 elements
- Vertical members (supports): 15 elements

## 🎨 Visualization Features

### Interactive Elements (Plotly)
- ✅ Hover tooltips with force values
- ✅ Zoom and pan controls
- ✅ Toggle series on/off
- ✅ Download as PNG
- ✅ 3D rotation in all directions
- ✅ Dynamic legend

### Static Elements (Matplotlib)
- ✅ Publication-quality output
- ✅ Filled areas for better visualization
- ✅ Customizable fonts and colors
- ✅ High DPI export capability

## 📋 Requirements

```
xarray>=2022.0.0
netCDF4>=1.6.0
plotly>=5.0.0
matplotlib>=3.5.0
numpy>=1.20.0
```

Install all requirements:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'xarray'`
**Solution:** Install required packages
```bash
pip install xarray netCDF4 plotly matplotlib
```

### Issue: `AttributeError: 'Dataset' object has no attribute 'element_id'`
**Solution:** Ensure you're using the correct dimension name `Element` (capital E)

### Issue: Plots not displaying in Jupyter
**Solution:** Ensure you have Plotly and Jupyter extensions installed
```bash
pip install plotly-orca psutil
jupyter nbextension enable --py --sys-prefix plotly
```

### Issue: Large file size when saving as HTML
**Solution:** The interactive HTML files contain all data. Use PNG export for smaller file sizes.

## 📈 Performance Notes

- **Notebook Startup:** ~3-5 seconds (first cell with imports)
- **Dataset Loading:** ~1-2 seconds
- **Data Extraction:** ~0.5 seconds
- **2D Plot Generation:** ~2 seconds
- **3D Plot Generation:** ~3 seconds per diagram
- **Total Execution Time:** ~10 seconds (complete notebook run)

## 🔬 Technical Details

### Data Processing Pipeline
1. Load NetCDF dataset using Xarray
2. Select specific elements by ID
3. Extract force components from dataset
4. Map forces to element nodes using connectivity dictionary
5. Visualize using Plotly (interactive) or Matplotlib (static)

### Coordinate System
- **X-axis:** Longitudinal direction (0-25 m)
- **Y-axis:** Force magnitude (vertical extrusion for 3D)
- **Z-axis:** Transverse direction (girder spacing)

### Force Components
- **Vy:** Shear force in local Y direction
- **Mz:** Bending moment about local Z axis
- **_i:** Force at element start node
- **_j:** Force at element end node

## 📝 Notes

1. **Scale Factors:** 
   - BMD scale factor: 0.01 (to fit visualization)
   - SFD scale factor: 0.02 (for better visibility)
   - Adjust in code if needed for different data ranges

2. **Compact Graphs:**
   - Matplotlib figure size for 3D diagrams: (0.8, 0.8) inches
   - Designed to fit within notebook display

3. **Color Coding:**
   - Each girder has a unique color for easy identification
   - Baseline shown in gray dashed lines

## 📚 References

- **Xarray Documentation:** https://docs.xarray.dev/
- **Plotly Documentation:** https://plotly.com/python/
- **Matplotlib Documentation:** https://matplotlib.org/
- **NetCDF Format:** https://www.unidata.ucar.edu/software/netcdf/

## 👨‍💼 Author

OSDAG Screening Assignment - Bridge Analysis Tool

## 📄 License

Open source - Use and modify as needed for educational and professional purposes.

---

**Last Updated:** February 3, 2026

For questions or issues, refer to the troubleshooting section or check the inline code comments in the notebooks.

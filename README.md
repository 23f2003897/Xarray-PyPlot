# OSDAG Bridge Screening Assignment - SFD and BMD Visualization

A comprehensive bridge analysis tool for visualizing Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for bridge girders using Python and modern visualization libraries.

![OSDAG Bridge Analysis](images/banner.png)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.14-3F4F75?logo=plotly&logoColor=white)
![Xarray](https://img.shields.io/badge/Data-Xarray-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)

---

## 📖 Description

The **OSDAG Bridge Screening & Analysis Tool** is a specialized engineering utility designed to visualize Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for complex bridge grillage models.

Processing data from NetCDF (`.nc`) formats, this tool performs statistical analysis on force components and generates high-fidelity 2D and 3D visualizations. It is specifically engineered to handle multi-girder bridge decks, offering engineers both interactive insights (via Plotly) and publication-ready static exports (via Matplotlib).

---

## ✨ Key Features

* **Automated Data Extraction:** Seamlessly loads and processes NetCDF data to extract forces ($M_z$, $V_y$) for specific bridge elements.
* **2D Critical Analysis (Task 1):** * Focuses on the Central Longitudinal Girder (Girder 3).
    * Generates dual-axis plots for SFD and BMD with hatching and peak value annotations.
    * Exports critical data points to CSV (`critical_moments.csv`, `forces_complete.csv`).
* **3D Grillage Visualization (Task 2):** * Renders a complete 3D wireframe of the bridge.
    * Visualizes forces for all 5 girders simultaneously using vertical extrusion.
    * Color-coded girders for easy identification (e.g., Girder 1 is Red, Girder 3 is Green).
* **Hybrid Output Formats:** Produces interactive HTML files for exploration and high-DPI PNG images for reports.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.x | Main programming language |
| **Data Handling** | Xarray, Pandas, NumPy | Multi-dimensional array handling and data manipulation |
| **File I/O** | NetCDF4 | Reading engineering simulation data |
| **Visualization** | Plotly | Interactive 3D and 2D plotting |
| **Static Plots** | Matplotlib | High-quality static image generation |

---

## ⚙️ Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/23f2003897/Xarray-PyPlot
cd osdag-bridge-analysis
```
## 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies
``` bash
pip install -r requirements.txt
```

---

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

---


## 🚀 Usage
The project is split into two main analysis tasks. Run the scripts directly from your terminal.
### Run Task 1: 2D Analysis (Central Girder)
Analyzes the central girder, calculates critical moments, and generates 2D plots.
```bash
python 2d_plots.py
```

* Outputs: **output/task1_2d_diagrams.html**, **output/critical_moments.csv**, etc.
### Run Task 2: 3D Visualization (All Girders)
Generates the 3D bridge model with extruded force diagrams for all 5 girders.
```bash
python 3d_plots.py

---
```
## 📂 Folder Structure
```
.
├── data/
│   ├── element.py             # Element definitions
│   ├── node.py                # Node coordinate definitions
│   └── screening_task (2).nc  # Input NetCDF dataset
├── output/                    # Generated plots and CSVs (Auto-created)
├── 2d_plots.py                # Script for Task 1 (2D Analysis)
├── 3d_plots.py                # Script for Task 2 (3D Visualization)
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```
---
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


---

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

---

## 📚 References

- **Xarray Documentation:** https://docs.xarray.dev/
- **Plotly Documentation:** https://plotly.com/python/
- **Matplotlib Documentation:** https://matplotlib.org/
- **NetCDF Format:** https://www.unidata.ucar.edu/software/netcdf/

---


## 🤝 Contributing
Contributions are welcome! Please follow these steps:

* Fork the repository.

* Create a feature branch (**git checkout -b feature/AmazingFeature**).

* Commit your changes (**git commit -m 'Add some AmazingFeature'**).

* Push to the branch (**git push origin feature/AmazingFeature**).

* Open a Pull Request.
 ----

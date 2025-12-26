# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Download Data

Download the Vietnam boundary file from GADM:
```bash
wget https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_VNM_0.json
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Script

```bash
python vietnam_protected_areas_viz.py
```

That's it! Your visualization will be saved to `outputs/vietnam_protected_areas_xmas_tree.png`

## 📁 Project Structure

```
vietnam-protected-areas-viz/
├── vietnam_protected_areas_viz.py  # Main script
├── example_usage.py                # Usage examples
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
├── LICENSE                         # MIT License
├── setup.py                        # Package setup
├── .gitignore                      # Git ignore rules
└── CONTRIBUTING.md                 # Contribution guidelines
```

## 🎨 Customize Your Visualization

### Change Colors

Edit the color palettes in `vietnam_protected_areas_viz.py`:

```python
# Line ~230: Tree colors
pine_greens = ['#a8c9a8', '#9bc19b', ...]  # Your colors here

# Line ~490: Star gradient
colors = plt.cm.YlOrRd(...)  # Try: YlGnBu, RdPu, etc.
```

### Adjust Star Sizes

```python
# Line 155: Modify size range
def calculate_star_sizes(areas, min_size=80, max_size=1000):
    # Increase max_size for larger stars
```

### Add More Protected Areas

```python
# Line 85: Edit protected_areas dictionary
protected_areas = {
    'name': ['Your Park Name', ...],
    'lat': [latitude, ...],
    'lon': [longitude, ...],
    'area_km2': [area, ...]
}
```

## 🔧 Troubleshooting

### "File not found" error
- Make sure `gadm41_VNM_0.json` is in the same directory
- Or specify the full path: `main(gadm_file='/full/path/to/gadm41_VNM_0.json')`

### Import errors
- Check Python version: `python --version` (needs 3.7+)
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`

### Memory issues
- The GADM file is large. If you have memory issues, increase the simplification tolerance:
  ```python
  # Line 50
  gdf.geometry.simplify(tolerance=0.05, ...)  # Increase from 0.03
  ```

## 📊 Output Files

The script creates:
1. **PNG image** (high resolution, 300 DPI)
2. **CSV file** with protected areas data

## 🆘 Need Help?

- Read the full [README.md](README.md)
- Check [example_usage.py](example_usage.py) for more examples
- Open an issue on GitHub

---

Happy visualizing! 🎄✨

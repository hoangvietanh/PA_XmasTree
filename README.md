# Vietnam Protected Areas Visualization - Các VQG lớn ở Việt Nam

A beautiful Christmas-themed visualization of Vietnam's major protected areas (National Parks) displayed as sparkling stars on a watercolor Christmas tree background.

![Vietnam Protected Areas](example_output.png)

## Features

🎄 **Watercolor Christmas Tree Background** - Soft, artistic pine tree with organic shapes
⭐ **Sparkling Stars** - Protected areas shown as glowing stars with size proportional to area
🗺️ **Accurate Vietnam Boundary** - GADM-sourced administrative boundaries
📊 **Cartographic Scaling** - Flannery's square root scaling for perceptually accurate size representation
🎨 **Beautiful Design** - Light blue smoky background with harmonious color palette

## Data Sources

- **Vietnam Boundary**: GADM 4.1 (Global Administrative Areas)
  - Download: https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_VNM_0.json
  
- **Protected Areas**: WDPA (World Database on Protected Areas)
  - Download: https://www.protectedplanet.net/country/VNM
  - Note: Current version uses sample data of 25 major protected areas

## Installation

### Requirements

```bash
pip install geopandas matplotlib pandas shapely numpy
```

### Python Version

Python 3.7 or higher

## Usage

### Basic Usage

```python
from vietnam_protected_areas_viz import main

# Run with default settings
fig, gdf_pa, gdf_boundary = main(
    gadm_file='path/to/gadm41_VNM_0.json',
    output_dir='./outputs'
)
```

### Custom Visualization

```python
from vietnam_protected_areas_viz import (
    fetch_vietnam_boundary,
    fetch_wdpa_vietnam,
    create_visualization
)

# Load data
gdf_boundary = fetch_vietnam_boundary('gadm41_VNM_0.json')
gdf_pa = fetch_wdpa_vietnam()

# Create visualization
fig = create_visualization(gdf_pa, gdf_boundary)

# Save
fig.savefig('my_visualization.png', dpi=300, bbox_inches='tight')
```

### Command Line

```bash
python vietnam_protected_areas_viz.py
```

## Output Files

The script generates two files:

1. **vietnam_protected_areas_xmas_tree.png** - High-resolution visualization (300 DPI)
2. **vietnam_protected_areas_data.csv** - Protected areas data with coordinates

## Customization

### Modify Protected Areas Data

Edit the `fetch_wdpa_vietnam()` function to use your own data:

```python
def fetch_wdpa_vietnam():
    # Load your own data
    gdf = gpd.read_file('path/to/your/protected_areas.geojson')
    return gdf
```

### Adjust Tree Colors

Modify the color palettes in `create_soft_watercolor_tree()`:

```python
pine_greens = ['#a8c9a8', '#9bc19b', ...]  # Light greens
dark_greens = ['#7aa67a', '#6d9a6d', ...]  # Dark greens
ornament_colors = ['#e74c3c', '#f39c12', ...]  # Ornament colors
```

### Change Star Appearance

Adjust star glow layers in `create_visualization()`:

```python
# Outer glow size multiplier (default: 2.5)
s=star_sizes * 2.5

# Glow transparency (default: 0.15)
alpha=0.15
```

## Technical Details

### Cartographic Scaling

The visualization uses **Flannery's perceptual scaling** (square root scaling) to make star sizes proportional to protected area sizes in a way that human perception accurately interprets:

```
size = min_size + ((√area - √area_min) / (√area_max - √area_min)) × (max_size - min_size)
```

### Boundary Simplification

Vietnam's boundary is simplified using the Douglas-Peucker algorithm with a tolerance of 0.03 degrees (~3km) to balance visual quality and performance:

- Original: ~17,926 coordinates
- Simplified: ~5,382 coordinates (70% reduction)

### Color Scheme

- **Background**: Light smoky blue (#d4e4f7, #e8f1fa)
- **Tree**: Soft greens (#a8c9a8 - #6d9a6d)
- **Stars**: Yellow-Orange-Red gradient (matplotlib YlOrRd)
- **Boundary**: Muted green (#5a7c65)

## Protected Areas Included

Sample data includes 25 major protected areas:

| Name | Area (km²) | Location |
|------|-----------|----------|
| VQG Yok Đôn | 1,156 | Central Highlands |
| VQG Pù Mát | 912 | Nghệ An |
| VQG Phong Nha-Kẻ Bàng | 857 | Quảng Bình |
| KDTSQ Cần Giờ | 757 | Hồ Chí Minh |
| VQG Cát Tiên | 720 | Đồng Nai |
| ... | ... | ... |

## Author

**Viet Anh**  
Green Field Consulting and Technology Company Limited (GFD)

📍 Phòng 705, 14 Trần Hưng Đạo, Cửa Nam, Hà Nội  
📧 info@gfd.com.vn  
🌐 gfd.com.vn  
📞 +(84)(24)39264830

## License

MIT License

## Acknowledgments

- **GADM** for Vietnam administrative boundaries
- **WDPA** for protected areas data
- **Matplotlib** for visualization capabilities
- **GeoPandas** for geospatial data handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Citation

If you use this visualization in your work, please cite:

```
Viet Anh (2024). Vietnam Protected Areas Visualization. 
Green Field Consulting and Technology Company Limited.
https://github.com/[your-username]/vietnam-protected-areas-viz
```

## Changelog

### Version 1.0.0 (December 2024)
- Initial release
- Watercolor Christmas tree background
- Sparkling star effects with glow
- GADM boundary integration
- Sample protected areas data (25 locations)
- Cartographic scaling implementation

---

🎄 **Chúc mừng Giáng sinh! Merry Christmas!** 🎅

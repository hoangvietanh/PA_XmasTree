#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnam Protected Areas Christmas Tree Visualization
Các VQG lớn ở Việt Nam

Author: Viet Anh - Green Field Consulting and Technology Company Limited
Date: December 2024
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon as MPLPolygon
from matplotlib.collections import PatchCollection
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
import json
import warnings
warnings.filterwarnings('ignore')

# Set Vietnamese font support
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def fetch_vietnam_boundary(gadm_file='/mnt/user-data/uploads/gadm41_VNM_0.json'):
    """
    Fetch Vietnam boundary from GADM GeoJSON file and simplify
    
    Parameters:
    -----------
    gadm_file : str
        Path to GADM GeoJSON file for Vietnam
    
    Returns:
    --------
    geopandas.GeoDataFrame
        Simplified Vietnam boundary
    """
    print("Đang tải ranh giới Việt Nam từ GADM...")
    
    # Try to load from uploaded GADM file
    try:
        import os
        if os.path.exists(gadm_file):
            gdf = gpd.read_file(gadm_file)
            
            # Count original coordinates
            total_coords = 0
            if gdf.geometry.iloc[0].geom_type == 'MultiPolygon':
                for poly in gdf.geometry.iloc[0].geoms:
                    total_coords += len(poly.exterior.coords)
            else:
                total_coords = len(gdf.geometry.iloc[0].exterior.coords)
            
            print(f"✓ Đã tải ranh giới GADM ({total_coords}+ tọa độ gốc)")
            
            # Simplify geometry more aggressively (tolerance in degrees, ~0.03 degree ≈ 3km)
            # Using preserve_topology to maintain shape integrity
            gdf['geometry'] = gdf.geometry.simplify(tolerance=0.03, preserve_topology=True)
            
            # Count simplified coordinates
            simplified_coords = 0
            if gdf.geometry.iloc[0].geom_type == 'MultiPolygon':
                for poly in gdf.geometry.iloc[0].geoms:
                    simplified_coords += len(poly.exterior.coords)
            else:
                simplified_coords = len(gdf.geometry.iloc[0].exterior.coords)
            
            reduction = (1 - simplified_coords/total_coords) * 100
            print(f"✓ Đã simplify xuống {simplified_coords} tọa độ (giảm {reduction:.1f}%)")
            print(f"  Loại hình học: {gdf.geometry.iloc[0].geom_type}")
            print(f"  Bounds: {gdf.total_bounds}")
            return gdf
    except Exception as e:
        print(f"Lỗi đọc file GADM: {e}")
    
    raise Exception("Không tìm thấy file ranh giới Việt Nam!")


def fetch_wdpa_vietnam():
    """
    Load Vietnam protected areas data
    
    Note: This uses sample data. For complete WDPA data, download from:
    https://www.protectedplanet.net/country/VNM
    
    Returns:
    --------
    geopandas.GeoDataFrame
        Protected areas with coordinates and area
    """
    print("Đang tải dữ liệu khu bảo tồn Việt Nam từ WDPA...")
    
    # Sample data of major protected areas in Vietnam
    protected_areas = {
        'name': [
            'VQG Ba Bể', 
            'VQG Cát Tiên',
            'VQG Phong Nha-Kẻ Bàng',
            'VQG Cúc Phương',
            'VQG Tam Đảo',
            'VQG Ba Vì',
            'VQG Xuân Sơn',
            'VQG Hoàng Liên',
            'VQG Yok Đôn',
            'VQG Bidoup - Núi Bà',
            'VQG Côn Đảo',
            'VQG Phú Quốc',
            'VQG Tràm Chim',
            'VQG U Minh Thượng',
            'VQG Mũi Cà Mau',
            'KDTSQ Cần Giờ',
            'VQG Bạch Mã',
            'VQG Núi Chúa',
            'VQG Chư Yang Sin',
            'VQG Xuân Thủy',
            'VQG Vũ Quang',
            'VQG Bến En',
            'VQG Pù Mát',
            'VQG Bù Gia Mập',
            'VQG Lò Gò - Xa Mát',
        ],
        'lat': [
            22.25, 11.45, 17.60, 20.30, 21.48, 21.07, 21.12, 22.37, 12.92, 
            12.18, 8.68, 10.22, 10.75, 9.58, 8.60, 10.40, 16.20, 11.70,
            14.42, 20.22, 18.33, 19.58, 18.97, 11.83, 11.52
        ],
        'lon': [
            105.62, 107.43, 106.28, 105.67, 105.63, 105.37, 104.95, 103.78, 107.75,
            108.68, 106.60, 104.00, 105.52, 105.07, 104.78, 106.93, 107.85, 109.15,
            108.37, 106.55, 105.37, 105.48, 105.08, 107.20, 106.48
        ],
        'area_km2': [
            100, 720, 857, 222, 368, 108, 155, 298, 1156, 650, 76, 314, 75, 82,
            410, 757, 220, 295, 589, 71, 552, 166, 912, 260, 185
        ]
    }
    
    df = pd.DataFrame(protected_areas)
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    
    print(f"Đã tải {len(gdf)} khu bảo tồn")
    return gdf


def create_soft_watercolor_tree(ax, bounds):
    """
    Create realistic Christmas tree with continuous connected shape
    Soft watercolor style harmonious with map colors
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to draw on
    bounds : list
        [min_x, max_x, min_y, max_y] boundaries
    """
    min_x, max_x = bounds[0], bounds[1]
    min_y, max_y = bounds[2], bounds[3]
    
    # Calculate center and dimensions
    center_x = (min_x + max_x) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    np.random.seed(42)
    
    # Green palette for pine tree
    pine_greens = [
        '#a8c9a8', '#9bc19b', '#8eb88e', '#b5d0b5',
        '#a3c5a3', '#96bd96', '#bad4ba', '#9fc49f'
    ]
    dark_greens = ['#7aa67a', '#6d9a6d', '#87ad87']
    
    # Tree parameters
    tree_base_y = min_y - 0.05 * height
    tree_top_y = max_y + 0.05 * height
    tree_height = tree_top_y - tree_base_y
    
    # Trunk - brown
    trunk_width = width * 0.05
    trunk_height = height * 0.12
    
    # Draw trunk with texture
    for i in range(3):
        trunk_color = ['#8b7355', '#9d8468', '#a89176'][i]
        offset = i * trunk_width * 0.08
        
        trunk = plt.Rectangle(
            (center_x - trunk_width/2 + offset, tree_base_y),
            trunk_width - offset * 2,
            trunk_height,
            facecolor=trunk_color,
            edgecolor='none',
            alpha=0.25 - i * 0.05,
            zorder=1
        )
        ax.add_patch(trunk)
    
    branch_base_y = tree_base_y + trunk_height
    
    # Create continuous triangle tree shape with overlapping layers
    tree_width_base = width * 1.1
    
    # Create overall triangle shape with multiple overlapping segments
    n_segments = 15  # More segments for smoother look
    
    for seg in range(n_segments):
        seg_t = seg / n_segments
        y_bottom = branch_base_y + seg_t * (tree_top_y - branch_base_y)
        
        # Segment height with overlap
        seg_height = tree_height / n_segments * 1.4  # Overlap factor
        y_top = y_bottom + seg_height
        
        # Width at bottom and top of this segment
        width_bottom = tree_width_base * (1 - seg_t * 0.75)
        width_top = tree_width_base * (1 - min(1.0, (seg_t + 1/n_segments)) * 0.75)
        
        # Create trapezoid/triangle segment with irregular edges
        n_edge_pts = 15
        left_edge = []
        right_edge = []
        
        # Left edge
        for i in range(n_edge_pts):
            t = i / (n_edge_pts - 1)
            y = y_bottom + t * seg_height
            w = width_bottom + t * (width_top - width_bottom)
            x = center_x - w/2
            # Add organic irregularity
            x += np.random.uniform(-width * 0.015, width * 0.015)
            y += np.random.uniform(-height * 0.008, height * 0.008)
            left_edge.append([x, y])
        
        # Top edge
        top_pts = []
        for i in range(5):
            t = i / 4
            x = center_x - width_top/2 + t * width_top
            y = y_top + np.random.uniform(-height * 0.008, height * 0.008)
            top_pts.append([x, y])
        
        # Right edge (reverse)
        for i in range(n_edge_pts-1, -1, -1):
            t = i / (n_edge_pts - 1)
            y = y_bottom + t * seg_height
            w = width_bottom + t * (width_top - width_bottom)
            x = center_x + w/2
            x += np.random.uniform(-width * 0.015, width * 0.015)
            y += np.random.uniform(-height * 0.008, height * 0.008)
            right_edge.append([x, y])
        
        # Bottom edge
        bottom_pts = []
        for i in range(5, 0, -1):
            t = i / 4
            x = center_x - width_bottom/2 + t * width_bottom
            y = y_bottom + np.random.uniform(-height * 0.008, height * 0.008)
            bottom_pts.append([x, y])
        
        segment_pts = left_edge + top_pts + right_edge + bottom_pts
        
        # Alternate between dark and light greens
        if seg % 2 == 0:
            color = np.random.choice(dark_greens)
            alpha = 0.14
        else:
            color = np.random.choice(pine_greens)
            alpha = 0.12
        
        segment = MPLPolygon(
            segment_pts,
            facecolor=color,
            edgecolor='none',
            alpha=alpha,
            zorder=2
        )
        ax.add_patch(segment)
    
    # Add texture with pine needle clusters
    n_clusters = 60
    for n in range(n_clusters):
        # Random position within tree triangle
        tier_t = np.random.uniform(0.05, 0.95)
        y = branch_base_y + tier_t * (tree_top_y - branch_base_y)
        
        # Width at this height
        max_width = tree_width_base * (1 - tier_t * 0.75)
        x = center_x + np.random.uniform(-max_width/2 * 0.8, max_width/2 * 0.8)
        
        # Small needle cluster
        cluster_size = width * np.random.uniform(0.01, 0.02)
        
        needle = plt.Circle(
            (x, y),
            cluster_size,
            color=np.random.choice(pine_greens),
            alpha=np.random.uniform(0.08, 0.14),
            zorder=3
        )
        ax.add_patch(needle)
    
    # Christmas ornaments - colorful baubles
    ornament_colors = [
        '#e74c3c', '#f39c12', '#3498db', '#9b59b6',
        '#e67e22', '#c0392b', '#2980b9', '#8e44ad'
    ]
    
    n_ornaments = 22
    for i in range(n_ornaments):
        # Position within tree triangle
        tier_t = np.random.uniform(0.15, 0.88)
        y = branch_base_y + tier_t * (tree_top_y - branch_base_y)
        
        # Width at this height
        max_width = tree_width_base * (1 - tier_t * 0.75)
        x = center_x + np.random.uniform(-max_width/2 * 0.65, max_width/2 * 0.65)
        
        # Ornament size
        size = width * np.random.uniform(0.013, 0.027)
        color = np.random.choice(ornament_colors)
        
        # Main bauble
        bauble = plt.Circle(
            (x, y),
            size,
            color=color,
            alpha=0.38,
            zorder=10
        )
        ax.add_patch(bauble)
        
        # Highlight
        highlight = plt.Circle(
            (x - size * 0.3, y + size * 0.3),
            size * 0.28,
            color='white',
            alpha=0.28,
            zorder=11
        )
        ax.add_patch(highlight)
    
    # Star on top
    star_y = tree_top_y + height * 0.015
    star_size = width * 0.065
    
    from matplotlib.patches import RegularPolygon
    
    # Yellow star with glow
    for idx in range(3):
        scale = 1.0 - idx * 0.18
        alpha = 0.38 - idx * 0.08
        
        star = RegularPolygon(
            (center_x, star_y),
            5,
            radius=star_size * scale,
            orientation=np.pi/2,
            facecolor='#f1c40f',
            edgecolor='none',
            alpha=alpha,
            zorder=12
        )
        ax.add_patch(star)


def create_abstract_tree_background(ax, bounds):
    """
    Placeholder for backward compatibility
    """
    pass


def calculate_star_sizes(areas, min_size=80, max_size=1000):
    """
    Calculate star marker sizes using cartographic scaling principles
    Using square root scaling (Flannery's perceptual scaling)
    
    Parameters:
    -----------
    areas : array-like
        Area values in km²
    min_size : float
        Minimum marker size
    max_size : float
        Maximum marker size
    
    Returns:
    --------
    numpy.ndarray
        Scaled marker sizes
    """
    areas = np.array(areas)
    
    # Apply square root scaling for better visual perception
    sqrt_areas = np.sqrt(areas)
    
    # Normalize to size range
    min_sqrt = sqrt_areas.min()
    max_sqrt = sqrt_areas.max()
    
    # Linear interpolation on square root values
    normalized = (sqrt_areas - min_sqrt) / (max_sqrt - min_sqrt)
    sizes = min_size + normalized * (max_size - min_size)
    
    return sizes


def create_visualization(gdf_pa, gdf_boundary):
    """
    Create the Christmas tree visualization with protected areas as stars
    
    Parameters:
    -----------
    gdf_pa : geopandas.GeoDataFrame
        Protected areas data
    gdf_boundary : geopandas.GeoDataFrame
        Vietnam boundary
    
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    # Create figure with light smoky blue background
    fig, ax = plt.subplots(figsize=(14, 18), facecolor='#d4e4f7')
    ax.set_facecolor('#e8f1fa')
    
    # Get bounds from boundary
    bounds = gdf_boundary.total_bounds  # [minx, miny, maxx, maxy]
    
    # Add harmonious watercolor tree background
    create_soft_watercolor_tree(ax, [bounds[0], bounds[2], bounds[1], bounds[3]])
    
    # Plot Vietnam boundary - darker outline for better visibility
    gdf_boundary.plot(
        ax=ax,
        facecolor='none',
        edgecolor='#5a7c65',
        linewidth=2.0,
        alpha=0.65,
        zorder=5
    )
    
    # NO FILL - completely transparent
    
    # Calculate star sizes using cartographic scaling
    star_sizes = calculate_star_sizes(gdf_pa['area_km2'].values)
    
    # Create color gradient (golden to red for Christmas theme)
    norm = plt.Normalize(vmin=gdf_pa['area_km2'].min(), vmax=gdf_pa['area_km2'].max())
    colors = plt.cm.YlOrRd(norm(gdf_pa['area_km2'].values))
    
    # Plot protected areas as sparkling stars with glow effect
    # First layer - outer glow (largest, most transparent)
    ax.scatter(
        gdf_pa.geometry.x, 
        gdf_pa.geometry.y,
        s=star_sizes * 2.5,
        c=colors,
        marker='*',
        edgecolors='none',
        linewidths=0,
        alpha=0.15,
        zorder=8
    )
    
    # Second layer - medium glow
    ax.scatter(
        gdf_pa.geometry.x, 
        gdf_pa.geometry.y,
        s=star_sizes * 1.8,
        c=colors,
        marker='*',
        edgecolors='none',
        linewidths=0,
        alpha=0.25,
        zorder=9
    )
    
    # Third layer - inner glow (white)
    ax.scatter(
        gdf_pa.geometry.x, 
        gdf_pa.geometry.y,
        s=star_sizes * 1.3,
        c='white',
        marker='*',
        edgecolors='none',
        linewidths=0,
        alpha=0.35,
        zorder=10
    )
    
    # Main star - bright and solid
    scatter = ax.scatter(
        gdf_pa.geometry.x, 
        gdf_pa.geometry.y,
        s=star_sizes,
        c=colors,
        marker='*',
        edgecolors='#34495e',
        linewidths=1.2,
        alpha=0.95,
        zorder=11
    )
    
    # Add sparkle points at star tips
    for idx, row in gdf_pa.iterrows():
        size = star_sizes[idx]
        x, y = row.geometry.x, row.geometry.y
        
        # Calculate star tip radius
        tip_radius = np.sqrt(size / np.pi) * 0.6
        
        # 5 sparkle points at star tips
        for i in range(5):
            angle = i * 2 * np.pi / 5 + np.pi/2  # 5-pointed star orientation
            tip_x = x + tip_radius * np.cos(angle)
            tip_y = y + tip_radius * np.sin(angle)
            
            # Small white sparkle
            ax.scatter(
                tip_x, tip_y,
                s=size * 0.08,
                c='white',
                marker='o',
                edgecolors='none',
                alpha=0.7,
                zorder=12
            )
    
    # Add labels for largest protected areas
    gdf_sorted = gdf_pa.sort_values('area_km2', ascending=False)
    for idx, row in gdf_sorted.head(10).iterrows():
        ax.annotate(
            row['name'],
            xy=(row.geometry.x, row.geometry.y),
            xytext=(6, 6),
            textcoords='offset points',
            fontsize=7,
            color='#2c3e50',
            alpha=0.90,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='#5a7c65', linewidth=0.8, alpha=0.85),
            zorder=11
        )
    
    # Add title only - no labels
    ax.set_title('Các VQG lớn ở Việt Nam', 
                fontsize=24, color='#1a472a', pad=20, weight='bold',
                fontfamily='sans-serif')
    
    # Remove axis labels, ticks, and spines
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Remove grid
    ax.grid(False)
    
    # Set axis limits with padding
    x_padding = (bounds[2] - bounds[0]) * 0.05
    y_padding = (bounds[3] - bounds[1]) * 0.05
    ax.set_xlim(bounds[0] - x_padding, bounds[2] + x_padding)
    ax.set_ylim(bounds[1] - y_padding, bounds[3] + y_padding)
    
    # Equal aspect ratio
    ax.set_aspect('equal')
    
    plt.tight_layout()
    return fig


def main(gadm_file='/mnt/user-data/uploads/gadm41_VNM_0.json',
         output_dir='/mnt/user-data/outputs'):
    """
    Main execution function
    
    Parameters:
    -----------
    gadm_file : str
        Path to GADM Vietnam boundary file
    output_dir : str
        Directory to save output files
    """
    print("=" * 70)
    print("  VIETNAM PROTECTED AREAS CHRISTMAS TREE - CÂY NOEL KHU BẢO TỒN VN")
    print("=" * 70)
    
    # Fetch Vietnam boundary
    gdf_boundary = fetch_vietnam_boundary(gadm_file)
    
    # Fetch protected areas data
    gdf_pa = fetch_wdpa_vietnam()
    
    # Print statistics
    print("\n" + "="*70)
    print("📊 THỐNG KÊ")
    print("="*70)
    print(f"🌟 Tổng số khu bảo tồn: {len(gdf_pa)}")
    print(f"📏 Tổng diện tích: {gdf_pa['area_km2'].sum():,.2f} km²")
    print(f"📈 Diện tích trung bình: {gdf_pa['area_km2'].mean():,.2f} km²")
    print(f"🏆 Diện tích lớn nhất: {gdf_pa['area_km2'].max():,.2f} km²")
    print(f"    → {gdf_pa.loc[gdf_pa['area_km2'].idxmax(), 'name']}")
    print(f"📍 Diện tích nhỏ nhất: {gdf_pa['area_km2'].min():,.2f} km²")
    print(f"    → {gdf_pa.loc[gdf_pa['area_km2'].idxmin(), 'name']}")
    
    print("\n" + "="*70)
    print("🏆 TOP 10 KHU BẢO TỒN LỚN NHẤT")
    print("="*70)
    top10 = gdf_pa.nlargest(10, 'area_km2')[['name', 'area_km2', 'lat', 'lon']]
    for i, (idx, row) in enumerate(top10.iterrows(), 1):
        print(f"{i:2d}. {row['name']:30s} {row['area_km2']:7.0f} km²  ({row['lat']:.2f}°N, {row['lon']:.2f}°E)")
    
    # Create visualization
    print("\n" + "="*70)
    print("🎨 ĐANG TẠO VISUALIZATION...")
    print("="*70)
    fig = create_visualization(gdf_pa, gdf_boundary)
    
    # Save
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'vietnam_protected_areas_xmas_tree.png')
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#d4e4f7')
    print(f"✅ Đã lưu hình ảnh: {output_file}")
    
    # Also save data to CSV
    csv_file = os.path.join(output_dir, 'vietnam_protected_areas_data.csv')
    gdf_export = gdf_pa.copy()
    gdf_export['longitude'] = gdf_export.geometry.x
    gdf_export['latitude'] = gdf_export.geometry.y
    gdf_export[['name', 'area_km2', 'latitude', 'longitude']].to_csv(
        csv_file, index=False, encoding='utf-8-sig'
    )
    print(f"✅ Đã lưu dữ liệu: {csv_file}")
    
    print("\n" + "="*70)
    print("🎄✨ HOÀN THÀNH! CHÚC MỪNG GIÁNG SINH! MERRY CHRISTMAS! 🎅🎁")
    print("="*70)
    
    return fig, gdf_pa, gdf_boundary


if __name__ == "__main__":
    main()

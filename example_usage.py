#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of Vietnam Protected Areas Visualization

This script demonstrates various ways to use the visualization tool.
"""

from vietnam_protected_areas_viz import (
    main,
    fetch_vietnam_boundary,
    fetch_wdpa_vietnam,
    create_visualization
)

# Example 1: Basic usage with default settings
print("Example 1: Basic usage")
print("-" * 50)
fig, gdf_pa, gdf_boundary = main(
    gadm_file='gadm41_VNM_0.json',  # Download from GADM
    output_dir='./outputs'
)
print("✓ Visualization saved to ./outputs/\n")

# Example 2: Custom workflow
print("Example 2: Custom workflow")
print("-" * 50)

# Load data separately
gdf_boundary = fetch_vietnam_boundary('gadm41_VNM_0.json')
gdf_pa = fetch_wdpa_vietnam()

# Print some statistics
print(f"Number of protected areas: {len(gdf_pa)}")
print(f"Total area: {gdf_pa['area_km2'].sum():.0f} km²")

# Create custom visualization
fig = create_visualization(gdf_pa, gdf_boundary)

# Save with custom settings
fig.savefig(
    'custom_visualization.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='#d4e4f7'
)
print("✓ Custom visualization saved\n")

# Example 3: Analyze protected areas
print("Example 3: Data analysis")
print("-" * 50)

# Get largest protected areas
largest = gdf_pa.nlargest(5, 'area_km2')
print("\nTop 5 Largest Protected Areas:")
for idx, row in largest.iterrows():
    print(f"  • {row['name']}: {row['area_km2']:.0f} km²")

# Get protected areas by region (example: Northern Vietnam)
northern = gdf_pa[gdf_pa['lat'] > 18]
print(f"\nNorthern Vietnam: {len(northern)} protected areas")
print(f"Total area: {northern['area_km2'].sum():.0f} km²")

# Get protected areas by region (example: Southern Vietnam)
southern = gdf_pa[gdf_pa['lat'] < 12]
print(f"\nSouthern Vietnam: {len(southern)} protected areas")
print(f"Total area: {southern['area_km2'].sum():.0f} km²")

print("\n✓ Analysis complete")

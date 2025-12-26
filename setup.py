from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vietnam-protected-areas-viz",
    version="1.0.0",
    author="Viet Anh",
    author_email="info@gfd.com.vn",
    description="Christmas-themed visualization of Vietnam's major protected areas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/[your-username]/vietnam-protected-areas-viz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "geopandas>=0.14.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "shapely>=2.0.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "vietnam-pa-viz=vietnam_protected_areas_viz:main",
        ],
    },
)

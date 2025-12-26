# Contributing to Vietnam Protected Areas Visualization

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, package versions)
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the enhancement
- Why it would be useful
- Proposed implementation (if you have ideas)

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests (if applicable)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/vietnam-protected-areas-viz.git
cd vietnam-protected-areas-viz

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

## Adding New Features

When adding new features:

1. **Update documentation** - Update README.md and docstrings
2. **Add examples** - Add usage examples if applicable
3. **Test thoroughly** - Test with different data inputs
4. **Maintain compatibility** - Ensure backward compatibility

## Data Sources

When working with data:

- **GADM boundaries**: Always use official GADM sources
- **Protected areas**: Prefer WDPA data or official government sources
- **Cite sources**: Add proper citations in documentation

## Questions?

Feel free to open an issue for questions or discussions.

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on collaboration
- Respect different viewpoints

---

Thank you for contributing! 🎄

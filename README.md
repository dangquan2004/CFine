# CFine Analysis

Python package for analyzing CFINE project data, specifically processing electrode metrics (Area, Eccentricity) from microscopic images.

## Structure

The project is modularized into the following components:

- `main.py`: Entry point for running the analysis.
- `config.py`: Centralized configuration for paths and constants.
- `data_loader.py`: Handles loading and parsing of raw data.
- `processing.py`: Computes statistics and summaries.
- `plotting.py`: Generates visualizations.
- `utils.py`: Helper functions for image processing.

## Usage

Run the analysis module from the parent directory:

```bash
python -m CFine.main
```

## Requirements

- pandas
- numpy
- matplotlib
- scikit-image
- openpyxl
- tifffile

## License

MIT License

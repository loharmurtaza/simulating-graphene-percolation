# Graphene Percolation Simulation

A scientific simulation tool for modeling the growth and percolation of graphene on a substrate surface. This project analyzes surface coverage dynamics using logistic growth models and determines percolation thresholds through graph-based connectivity analysis.

## Overview

This project addresses a key question in materials science: **at what coverage percentage and time does graphene form a percolated (connected) network on a surface?**

The simulation:
- Models graphene flakes as growing circles on a 2D substrate
- Fits experimental surface coverage data to a logistic growth model
- Detects percolation (connected paths across the surface) using graph algorithms
- Provides statistical analysis of percolation thresholds

## Installation

```bash
# Clone the repository
git clone https://github.com/loharmurtaza/simulating-graphene-percolation.git
cd simulating-graphene-percolation

# Create a virtual environment
python -m venv venv

# Move inside venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package       | Version   | Purpose                   |
|---------------|-----------|---------------------------|
| numpy         | 1.26.4    | Numerical computations    |
| pandas        | 2.2.1     | Data manipulation         |
| matplotlib    | 3.8.3     | Visualization             |
| scipy         | 1.12.0    | Curve fitting             |
| tqdm          | 4.66.2    | Progress bars             |
| shapely       | 2.0.3     | Geometric calculations    |

## Usage

### Surface Coverage Simulation

Run the complete surface coverage and percolation analysis pipeline:

```bash
python -m main_graphene_percolation --task surface
```

This will:
1. Load experimental data from `data/raw/experimental_raw.csv`
2. Fit a logistic growth model to the data
3. Simulate graphene flake growth at multiple time points
4. Test for percolation connectivity (top-to-bottom and left-to-right)
5. Generate visualizations (if enabled)

### N-Simulations (Monte Carlo)

Run a configurable number of independent simulations with early-stopping at first percolation:

```bash
python -m main_graphene_percolation --task n_simulations
```

Each run uses a different random seed. The pipeline stops each simulation at the first time-step where percolation occurs and records per-run results (percolation time, coverage, top-to-bottom/left-to-right). Set `SIMULATIONS_TO_RUN` in `.env` to control how many runs to execute.

### Results Analysis

Analyze percolation results and generate statistical plots:

```bash
python -m main_graphene_percolation --task results
```

This generates Gaussian distribution fits for percolation time and area fraction for `N` simulations.

## Configuration

Configuration is managed through the `.env` file:

### Simulation Parameters

| Parameter                 | Default   | Description                       |
|---------------------------|-----------|-----------------------------------|
| `GRID_SIZE_MICRONS`       | 100       | Surface grid size in micrometers  |
| `NUM_CIRCLES`             | 48        | Number of graphene flakes         |
| `INITIAL_RADIUS_MICRONS`  | 0.1       | Initial radius of each circle     |
| `RANDOM_SEED`             | 10        | Random seed for reproducibility   |
| `MESH_POINTS`             | 1000      | Grid resolution (N x N points)    |
| `SHOW_PLOTS`              | True      | Display plots during execution    |
| `SIMULATIONS_TO_RUN`      | 1000      | Number of runs for simulations    |

### Directory Structure

```
simulating-graphene-percolation/
├── main_graphene_percolation.py   # CLI entry point
├── requirements.txt               # Python dependencies
├── .env                           # Configuration
├── config/
│   └── settings.py                # Configuration dataclasses
├── models/
│   ├── growth_result.py           # Single-run growth/percolation result
│   └── simulation_result.py       # Per-simulation result (n_simulations)
├── scripts/
│   ├── run_surface.py             # Surface simulation pipeline
│   ├── run_simulations.py         # N-simulations pipeline (early-stopping)
│   └── run_results.py             # Results analysis
├── utils/
│   ├── config_logger.py           # Logging configuration
│   ├── io.py                      # Data input operations
│   ├── math.py                    # Mathematical models
│   ├── save_files.py              # Figure export utilities
│   ├── search_algorithm.py        # Graph search (BFS)
│   ├── seeding.py                 # Random seed management
│   └── visualization.py           # Graph generation
└── data/
    ├── raw/
    │   └── experimental_raw.csv   # Experimental data
    └── output/                    # Output files
```

## Input Data Format

The experimental data file (`data/raw/experimental_raw.csv`) should have:

```csv
data_point (in min),surface_coverage (in %),standard_deviation (in %)
0,0,0
2,3,0.73819
5.5,51,2.9242
...
```

## Mathematical Models

### Logistic Growth Model

Surface coverage $S(t)$ is modeled using the logistic function:

$$
S(t) = \frac{L}{1 + e^{-k(t - t_0)}}
$$

Where:
- **$L$**: Maximum coverage level (asymptote)
- **$k$**: Growth rate parameter
- **$t_0$**: Midpoint time (inflection point)

### Percolation Detection

1. Graphene flakes are represented as circles with random centers
2. An adjacency graph is built based on circle-to-circle contact
3. Breadth-first search determines if a connected path exists from one edge to the opposite edge

## Output

- **Percolation data**: `data/output/csvs/growth_results_simulations.csv`
- **Statistical analysis figure**: `data/output/images/gaussian_curves.png`
- **Simulation visualizations**: Displayed during runtime (if `SHOW_PLOTS=True`) for scripts/run_surface.py

## License

This project is provided for research and educational purposes.

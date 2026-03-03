# Graphene Percolation Simulation

A scientific simulation tool for modeling the growth and percolation of graphene on a substrate surface. The project fits experimental surface coverage data to **logistic** or **exponential** growth models, simulates radial flake growth, and detects percolation using graph-based connectivity analysis.

## Overview

The simulation addresses: **at what coverage and time does graphene form a percolated (connected) network on the surface?**

- Models graphene flakes as growing circles on a 2D substrate
- Fits experimental coverage vs. time to either a **logistic** or **exponential** growth model
- Detects percolation (connected paths across the surface) via graph algorithms
- Supports Monte Carlo runs and statistical analysis of percolation thresholds

## Installation

```bash
# Clone the repository
git clone https://github.com/loharmurtaza/simulating-graphene-percolation.git
cd simulating-graphene-percolation

# Create and activate a virtual environment
python -m venv venv
# Windows (PowerShell):

.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

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
| python-dotenv | 1.2.1     | Environment configuration |

## Usage

The main entry point requires both `--model` and `--task`:

```bash
python -m main_graphene_percolation --model <logistic|exponential> --task <surface|n_simulations|results>
```

### Surface coverage and percolation (single run)

Fit the chosen model to experimental data, simulate growth at multiple time points, and test for percolation:

**Logistic model:**
```bash
python -m main_graphene_percolation --model logistic --task surface
```

**Exponential model:**
```bash
python -m main_graphene_percolation --model exponential --task surface
```

This will:

1. Load experimental data from `data/raw/experimental_raw.csv` (path set in `.env`)
2. Fit the selected growth model (logistic or exponential)
3. Simulate graphene flake growth at multiple time points
4. Test for percolation (top-to-bottom and left-to-right)
5. Save figures and CSVs under `data/output/` (if enabled)

### N-simulations (Monte Carlo)

Run many independent simulations with early stopping at first percolation. Set `SIMULATIONS_TO_RUN` and `MAX_WORKERS` in `.env`.

**Logistic:**
```bash
python -m main_graphene_percolation --model logistic --task n_simulations
```

**Exponential:**
```bash
python -m main_graphene_percolation --model exponential --task n_simulations
```

### Results analysis

Analyze percolation results and generate Gaussian fits and plots from the CSVs produced by `n_simulations`. Configure `PERCOLATIONS_CSV_DIR` in `.env` to point to the CSV directory.

**Logistic:**
```bash
python -m main_graphene_percolation --model logistic --task results
```

**Exponential:**
```bash
python -m main_graphene_percolation --model exponential --task results
```

## Configuration

Configuration is via the `.env` file in the project root.

### Main parameters

| Parameter                 | Description                               |
|---------------------------|-------------------------------------------|
| `PROJECT_ROOT`            | Project root directory (e.g. `./`)        |
| `EXPERIMENTAL_RAW_PATH`   | Path to experimental coverage CSV         |
| `OUTPUT_DIR`              | Base output directory (e.g. `./data/output`) |
| `GRID_SIZE_MICRONS`       | Surface grid size (µm)                    |
| `NUM_CIRCLES`             | Number of graphene flakes                 |
| `INITIAL_RADIUS_MICRONS`  | Initial radius of each circle (µm)        |
| `RADIUS_MICRONS`          | Radius used in geometry (µm)             |
| `RANDOM_SEED`             | Random seed for reproducibility          |
| `MESH_POINTS`             | Grid resolution (N×N)                     |
| `USE_STD`                 | Use standard deviation in fitting        |
| `SHOW_PLOTS`              | Show plots during execution              |
| `SIMULATIONS_TO_RUN`      | Number of runs for `n_simulations`        |
| `MAX_WORKERS`             | Parallel workers for simulations         |
| `PERCOLATIONS_CSV_DIR`    | Directory of percolation CSVs for results |

## Project structure

```
graphene-percolation-reza/
├── main_graphene_percolation.py            # CLI entry point (--model, --task)
├── load_env_variables.py                   # Load .env
├── requirements.txt                        # Required libraries and their versions
├── .env                                    # Configuration (paths, flags, seeds)
├── config/
│   ├── __init__.py
│   └── settings.py                         # Dataclasses: SurfaceCoverageConfig, etc.
├── models/
│   ├── growth_result.py                    # Single-run growth/percolation result
│   └── simulation_result.py                # Per-simulation result (n_simulations)
├── scripts/
│   ├── __init__.py
│   ├── run_surface_logistic.py             # Surface pipeline (logistic)
│   ├── run_surface_exponential.py          # Surface pipeline (exponential)
│   ├── run_simulations_logistic.py         # Simulations pipeline (logistic)
│   ├── run_simulations_exponential.py      # Simulations pipeline (exponential)
│   ├── run_results_logistic.py             # Results analysis pipeline (logistic)
│   ├── run_results_exponential.py          # Results analysis pipeline (exponential)
│   └── test_scripts/                       # Standalone fit/plot scripts
│       ├── test_exponential_function.py    # Test script for exponential fitting function
│       └── test_tanh_squared.py            # Test script for logistic fitting function
├── utils/
│   ├── __init__.py
│   ├── config_logger.py                    # Logging setup
│   ├── io.py                               # Data I/O
│   ├── math.py                             # Growth models, fitting, geometry
│   ├── save_files.py                       # Figure export
│   ├── search_algorithm.py                 # BFS percolation
│   ├── seeding.py                          # Random seed handling
│   └── visualization.py                    # Graph generation
├── data/
│   ├── raw/
│   │   ├── experimental_raw.csv            # time (min), coverage (%), std (%)
│   │   └── original_experimental_data.txt
│   └── output/                             # Created at runtime (gitignored)
│       ├── csvs/                           # Growth and percolation CSVs
│       ├── images/                         # PNGs (logistic/, exponential/)
│       └── pdfs/                           # PDFs (logistic/, exponential/)
└── logs/                                   # Run logs (gitignored)
```

## Input data format

`data/raw/experimental_raw.csv` (or path in `EXPERIMENTAL_RAW_PATH`) should look like:

```csv
data_point (min),surface_coverage (%),standard_deviation (%)
2,3,0.73819
5.5,51,2.9242
...
```

## Mathematical models

### Logistic growth

$$
S(t) = \frac{L}{1 + e^{-k(t - t_0)}}
$$

- **L**: maximum coverage (asymptote)
- **k**: growth rate
- **t₀**: midpoint (inflection) time

### Exponential (tanh-style) growth

$$
\theta_G(t) = \left( \frac{e^{\alpha t + C_1} - 1}{e^{\alpha t + C_1} + 1} \right)^2
$$

- **α**: growth rate
- **C₁**: constant (e.g. for θ_G(0) = 0)

### Percolation

- Flakes are circles with random centers; an adjacency graph is built from circle–circle contact.
- Breadth-first search determines whether a connected path exists from one edge to the opposite edge (top–bottom and left–right).

## Output

- **Single-run surface**: `data/output/csvs/growth_results_single_percolation_<logistic|exponential>.csv`; figures under `data/output/images/` and `data/output/pdfs/` (logistic/ or exponential/).
- **N-simulations**: percolation CSVs in `data/output/csvs/` (and path given by `PERCOLATIONS_CSV_DIR`).
- **Results task**: Gaussian-curve figures, e.g. `data/output/images/gaussian_curve_<logistic|exponential>.png` and corresponding PDFs.

## License

This project is for research and educational use.

# Graphene Percolation Simulation

A scientific simulation tool for modeling the growth and percolation of graphene on a substrate surface. The project fits experimental surface coverage data to **logistic** or **exponential** growth models, simulates radial flake growth, and detects percolation using graph-based connectivity analysis.

**This simulation accompanies the following paper:**

> **Graphene Autocatalytic Growth with Percolation Control on a Dielectric Substrate**  
> *Results in Engineering*, available online 28 February 2026, 109831 (In Press, Journal Pre-proof)  
> DOI: [10.1016/j.rineng.2026.109831](https://doi.org/10.1016/j.rineng.2026.109831)  
> © Open access under a Creative Commons license.

**Authors:** Mohammadreza Salehpoor, Natalia S. Khoteeva, Artem K. Grebenko, Elena S. Zhukova, Kirill E. Malgin, Ghulam Murtaza, Nikita E. Gordeev, Nikita I. Raginov, Oleg R. Trepalin, Boris P. Gorshunov, Dmitry V. Krasnikov, Albert G. Nasibulin.

**Author contributions:** Mohammadreza Salehpoor: Writing – review & editing, Writing – original draft, Visualization, Validation, Software, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. Natalia S. Khoteeva: Visualization, Software, Methodology, Formal analysis, Conceptualization. Artem K. Grebenko: Writing – review & editing, Supervision, Methodology, Conceptualization. Elena S. Zhukova: Writing – review & editing, Visualization, Formal analysis, Data curation, Conceptualization. Kirill E. Malgin: Visualization, Software. Ghulam Murtaza: Software, Data curation. Nikita E. Gordeev: Writing – review & editing, Software, Conceptualization. Nikita I. Raginov: Resources. Oleg R. Trepalin: Resources. Boris P. Gorshunov: Writing – review & editing, Supervision, Formal analysis, Data curation, Conceptualization. Dmitry V. Krasnikov: Writing – review & editing, Validation, Supervision, Resources, Methodology, Conceptualization. Albert G. Nasibulin: Supervision.

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

# Create your local configuration from the template
# Windows (PowerShell):
Copy-Item .env.example .env

# Linux/macOS:
cp .env.example .env
```

Requires **Python 3.9–3.12** (the pinned `numpy==1.26.4` does not support newer versions). Always run commands from the project root, since the paths in `.env` are relative to the current working directory.

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
python -m main --model <logistic|exponential> --task <surface|n_simulations|results>
```

### Surface coverage and percolation (single run)

Fit the chosen model to experimental data, simulate growth at multiple time points, and test for percolation:

**Logistic model:**
```bash
python -m main --model logistic --task surface
```

**Exponential model:**
```bash
python -m main --model exponential --task surface
```

This will:

1. Load experimental data from `data/raw/experimental_raw.csv` (path set in `.env`)
2. Fit the selected growth model (logistic or exponential)
3. Simulate graphene flake growth at multiple time points
4. Test for percolation (top-to-bottom and left-to-right)
5. Save a growth-results CSV under `data/output/csvs/`, plus figures under `data/output/images/` and `data/output/pdfs/` when `SHOW_PLOTS=True`

### N-simulations (Monte Carlo)

Run many independent simulations with early stopping at first percolation. Set `SIMULATIONS_TO_RUN` and `MAX_WORKERS` in `.env`. Each simulation gets a fresh random seed, so `RANDOM_SEED` is not used by this task.

**Logistic:**
```bash
python -m main --model logistic --task n_simulations
```

**Exponential:**
```bash
python -m main --model exponential --task n_simulations
```

### Results analysis

Analyze percolation results and generate Gaussian fits and plots from the CSV produced by `n_simulations` (`growth_results_simulations_<model>.csv`). Configure `PERCOLATIONS_CSV_DIR` in `.env` to point to the directory containing it.

**Logistic:**
```bash
python -m main --model logistic --task results
```

**Exponential:**
```bash
python -m main --model exponential --task results
```

## Configuration

Configuration is via a `.env` file in the project root. It is not tracked by git; create it from the template with `cp .env.example .env`. Variables are loaded by `python-dotenv` when `config/settings.py` is imported. Variables already set in your shell take precedence over `.env`.

### Main parameters

| Parameter                 | Description                               |
|---------------------------|-------------------------------------------|
| `PROJECT_ROOT`            | Project root directory (e.g. `./`); `logs/` is created here |
| `DATA_DIR`, `RAW_DIR`, `PROCESSED_DIR` | Data directories (read but currently unused) |
| `EXPERIMENTAL_RAW_PATH`   | Path to experimental coverage CSV         |
| `OUTPUT_DIR`              | Base output directory (e.g. `./data/output`) |
| `GRID_SIZE_MICRONS`       | Side length of the square surface (µm)    |
| `NUM_CIRCLES`             | Number of graphene flakes                 |
| `INITIAL_RADIUS_MICRONS`  | Initial radius of each circle (µm)        |
| `RADIUS_MICRONS`          | Reserved radius parameter (read but currently unused) |
| `RANDOM_SEED`             | Seed for flake placement in the `surface` task |
| `MESH_POINTS`             | Grid resolution (N×N) used to measure coverage |
| `USE_STD`                 | Weight the fit by the experimental standard deviation |
| `SHOW_PLOTS`              | Generate and save figures (nothing opens in a window) |
| `SIMULATIONS_TO_RUN`      | Number of runs for `n_simulations`        |
| `MAX_WORKERS`             | Parallel worker processes (capped at CPU count) |
| `PERCOLATIONS_CSV_DIR`    | Directory of percolation CSVs for results |

See [docs/configuration.md](docs/configuration.md) for full details.

## Project structure

```
graphene-percolation-reza/
├── main.py                                 # CLI entry point (--model, --task)
├── requirements.txt                        # Required libraries and their versions
├── .env.example                            # Configuration template (copy to .env)
├── .env                                    # Local configuration (gitignored)
├── docs/                                   # Detailed documentation
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
data_point (in min),surface_coverage (in %),standard_deviation (in %)
2,3.2,0.73819
5.5,51.2,2.9242
...
```

The column names must match exactly; they are read by name in `utils/io.py`.

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
- **C₁**: offset constant; the simulated time axis starts at $t_{min} = -C_1/\alpha$, where θ_G = 0

The code returns θ_G as a percentage (×100) so it can be fitted directly to the coverage data.

### Percolation

- Flakes are circles with random centers (pairwise distance between 5 and 140 µm); an adjacency graph is built from circle–circle contact (0.01 µm tolerance).
- At each time step all circles grow to the radius that matches the fitted coverage, refined until the measured coverage is within 1 % of the target.
- Breadth-first search determines whether a connected path exists from one edge to the opposite edge (top–bottom and left–right).

## Output

All paths are relative to `OUTPUT_DIR` (default `data/output/`).

| Task | Files |
|------|-------|
| `surface` (logistic) | `csvs/growth_results_single_percolation_logistic.csv`; figures (if `SHOW_PLOTS`): `{images,pdfs}/logistic/surface_coverage_vs_time_logistic.*`, `{images,pdfs}/logistic/time_index_<t>min.*` |
| `surface` (exponential) | `csvs/growth_results_single_percolation_exponential.csv`; figures (if `SHOW_PLOTS`): `{images,pdfs}/exponential/surface_coverage_vs_time_exponential_with_derivative.*`, `{images,pdfs}/exponential/<t>min.*` |
| `n_simulations` | `csvs/growth_results_simulations_{logistic,exponential}.csv` |
| `results` (logistic) | `images/gaussian_curve_logistic.png`, `pdfs/gaussian_curve_logistic.pdf` |
| `results` (exponential) | `images/exponential/gaussian_curve_exponential.png`, `pdfs/exponential/gaussian_curve_exponential.pdf` |

Each run also writes a log file to `logs/run_<YYYYmmdd_HHMMSS>.log`. See [docs/outputs.md](docs/outputs.md) for CSV column descriptions.

## Documentation

Detailed documentation lives in [docs/](docs/README.md):

- [Getting started](docs/getting-started.md)
- [Configuration](docs/configuration.md)
- [CLI and pipelines](docs/pipelines.md)
- [Growth models and fitting](docs/growth-models.md)
- [Simulation and percolation algorithm](docs/simulation-and-percolation.md)
- [Outputs](docs/outputs.md)
- [Code reference](docs/code-reference.md)
- [Known limitations](docs/known-limitations.md)

## License

**This repository** (the simulation code and related materials in this repo) is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

The **paper** (“Graphene Autocatalytic Growth with Percolation Control on a Dielectric Substrate”) is published open access in *Results in Engineering*; its license is determined by the publisher (see the article page and DOI above).

For this repo, you are free to:

- **Share** — copy and redistribute the material in any medium or format  
- **Adapt** — remix, transform, and build upon the material for any purpose, including commercially  

Under the following terms:

- **Attribution** — you must give appropriate credit, provide a link to the license, and indicate if changes were made.

Full license text: [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)

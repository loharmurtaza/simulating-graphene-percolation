# Configuration

## How configuration is loaded

1. `config/settings.py` calls `load_dotenv()` (from `python-dotenv`) when it is first imported. This happens as soon as `main.py` imports anything from `config` or `utils`.
2. `load_dotenv()` looks for a `.env` file starting from the `config/` directory and walking up the tree, so it finds `<project root>/.env`.
3. Variables **already set in the process environment win**. `load_dotenv()` does not override them by default. This lets you change a value for one run without editing the file:

   ```bash
   # Linux/macOS
   SIMULATIONS_TO_RUN=50 python -m main --model logistic --task n_simulations
   # Windows (PowerShell)
   $env:SIMULATIONS_TO_RUN=50; python -m main --model logistic --task n_simulations
   ```

4. Values are read with `os.getenv` and converted by the helpers `get_str`, `get_int`, `get_float` and `get_bool`. `get_bool` treats `1`, `true`, `yes` and `y` as true (case-insensitive), and anything else as false.

Python does not read `.env` files on its own. `os.getenv` only sees the real process environment, which is why `python-dotenv` is a dependency. If you export every variable in your shell instead, `.env` is optional.

Module-level values (`PROJECT_ROOT`, `OUTPUT_DIR`, …) are read at import time. The dataclass fields (`SurfaceCoverageConfig`, etc.) are read when an instance is created. A missing numeric variable raises a `TypeError` (`int(None)`), and a missing boolean raises an `AttributeError`.

## Variables

### Paths

| Variable | Default | Used by | Notes |
|----------|---------|---------|-------|
| `PROJECT_ROOT` | `./` | `utils/config_logger.py` | `logs/` is created inside it |
| `DATA_DIR` | `./data` | — | Read but currently unused |
| `RAW_DIR` | `./data/raw` | — | Read but currently unused |
| `PROCESSED_DIR` | `./data/processed` | — | Read but currently unused |
| `EXPERIMENTAL_RAW_PATH` | `./data/raw/experimental_raw.csv` | `surface`, `n_simulations` | Experimental coverage data, see [format](#experimental-data-format) |
| `OUTPUT_DIR` | `./data/output` | all tasks | Root for `csvs/`, `images/`, `pdfs/` |
| `PERCOLATIONS_CSV_DIR` | `./data/output/csvs/` | `results` | Directory containing `growth_results_simulations_<model>.csv` |

### Surface and geometry (`SurfaceCoverageConfig`)

| Variable | Default | Type | Meaning |
|----------|---------|------|---------|
| `GRID_SIZE_MICRONS` | `100` | int | Side length of the square substrate in µm. See [known limitations](known-limitations.md#grid-size-is-effectively-fixed-at-100-µm) before changing it |
| `NUM_CIRCLES` | `48` | int | Number of nucleation sites (graphene flakes) |
| `INITIAL_RADIUS_MICRONS` | `0.1` | float | Radius of the circles before growth starts |
| `RADIUS_MICRONS` | `0.0914e-3` | float | Loaded into the config but not used by any pipeline |
| `RANDOM_SEED` | `10` | int | Seed for nucleation-site placement in the `surface` task. `n_simulations` ignores it |
| `MESH_POINTS` | `1000` | int | Resolution N of the N×N grid used to measure covered area. Cost grows with N² |
| `USE_STD` | `True` | bool | Weight the curve fit by the experimental standard deviation (`sigma=std, absolute_sigma=True`) |
| `SHOW_PLOTS` | `True` | bool | Generate **and save** figures. Nothing is shown in a window. With `False`, no figures are produced and the CSVs are still written |

### Monte Carlo (`SimulationsConfig`)

| Variable | Default | Type | Meaning |
|----------|---------|------|---------|
| `SIMULATIONS_TO_RUN` | `1000` | int | Number of independent simulations |
| `MAX_WORKERS` | `8` | int | Worker processes; the effective value is `min(MAX_WORKERS, cpu_count())` |

### Results (`FinalResultsConfig`)

| Variable | Default | Type | Meaning |
|----------|---------|------|---------|
| `PERCOLATIONS_CSV_DIR` | `./data/output/csvs/` | str | Directory searched for the simulations CSV |

## Experimental data format

`EXPERIMENTAL_RAW_PATH` must point to a CSV with exactly these column names (read in `utils/io.py`):

```csv
data_point (in min),surface_coverage (in %),standard_deviation (in %)
2,3.2,0.73819
5.5,51.2,2.9242
6,65.9,2.38343
6.5,78.9,2.42453
15,94.8,4.71513
27,99.9,0.70711
```

- Time is in minutes, coverage and standard deviation are in percent (0–100).
- When `USE_STD=True`, a standard deviation of `0` makes the weighted fit divide by zero. Leave out rows such as `0,0,0`. The full dataset including that point is kept in `data/raw/original_experimental_data.txt` for reference.

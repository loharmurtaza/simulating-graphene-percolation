# Code reference

```text
main.py                        CLI → pipelines
config/settings.py             .env loading, config dataclasses
models/                        result dataclasses
scripts/                       one pipeline per (task, model)
utils/                         maths, geometry, graph search, I/O, logging
```

## `main.py`

`cli()` parses `--model` and `--task`, sets up logging and dispatches to a pipeline. See [pipelines.md](pipelines.md).

## `config/settings.py`

- Calls `load_dotenv()` on import (see [configuration.md](configuration.md)).
- Helpers: `get_str`, `get_int`, `get_float`, `get_bool`.
- Module constants: `PROJECT_ROOT`, `DATA_DIR`, `RAW_DIR`, `PROCESSED_DIR`, `OUTPUT_DIR`.
- Dataclasses, each field read from the environment through `default_factory` when an instance is created:
  - `SurfaceCoverageConfig`: `raw_data_path`, `grid_size_microns`, `num_circles`, `initial_radius_microns`, `radius_microns`, `random_seed`, `mesh_points`, `use_std`, `show_plots`
  - `SimulationsConfig`: `simulations_to_run`, `max_workers`
  - `FinalResultsConfig`: `percolations_csv_dir`

You can override fields in code, e.g. `SurfaceCoverageConfig(num_circles=60)`.

## `models/`

| File | Class | Purpose |
|------|-------|---------|
| `growth_result.py` | `GrowthResult` | One time step: `time_min`, target/initial/final coverage, `top_to_bottom`, `left_to_right` |
| `simulation_result.py` | `SimulationResult` | One Monte Carlo run. See [outputs.md](outputs.md#n_simulations) |

## `scripts/`

| File | Entry function | Notes |
|------|----------------|-------|
| `run_surface_logistic.py` | `run_pipeline_logistic(cfg)` | Contains `simulate_growth()` |
| `run_surface_exponential.py` | `run_pipeline_exponential(cfg)` | Own copy of `simulate_growth()` |
| `run_simulations_logistic.py` | `run_pipeline_logistic(cfg, sim_cfg)` | `simulate_growth_until_percolation()`, `_run_single_simulation()` (top-level so it can be pickled) |
| `run_simulations_exponential.py` | `run_pipeline_exponential(cfg, sim_cfg)` | Same structure |
| `run_results_logistic.py` | `run_pipeline_logistic(cfg, csv_path=None)` | `plot_gaussian_curves()` |
| `run_results_exponential.py` | `run_pipeline_exponential(cfg, csv_path=None)` | Same structure, different styling |
| `test_scripts/test_exponential_function.py` | `exponential_function_fit()` | Fit-and-plot only |
| `test_scripts/test_tanh_squared.py` | `tanh_squared_fit()` | Fit-and-plot only |

The logistic and exponential pipelines are near-duplicates. Apart from plotting, they differ only in the fitted function and the time grid, so a change to the growth or percolation logic has to be made in **all four** `run_surface_*` / `run_simulations_*` files.

## `utils/`

| Module | Key functions |
|--------|---------------|
| `math.py` | Models: `logistic`, `logistic_derivative`, `exponential_function`, `exponential_function_derivative`, `tanh_squared`, `tanh_squared_derivative`. Fitting: `fit_surface_coverage_logistic`, `fit_surface_coverage_exponential`, `fit_surface_coverage_tanh_squared`, `find_inflection_point`, `estimate_mean_areas_from_coverage`. Geometry: `two_points_distance`, `random_points`, `build_initial_circles`, `circle_touches_line`, `two_circles_touching` |
| `visualization.py` | `generate_graph(circles, surface_dim)` → adjacency dict and top/bottom/left/right boundary dicts |
| `search_algorithm.py` | `breadth_first_search(graph, start_node, target_nodes)` → `(visit_order, found)` |
| `io.py` | `load_experimental_raw_data(path)` → `(t, S, std)` NumPy arrays |
| `save_files.py` | `save_fig_as_png`, `save_fig_as_pdf` (create parent dirs), `save_growth_results_summary` |
| `seeding.py` | `set_seed(seed)` seeds `random` and `numpy.random` |
| `config_logger.py` | `setup_logging(level, log_to_file)`: console and file handlers, safe to call more than once |

## Dependencies

| Package | Used for |
|---------|----------|
| numpy | Arrays, mesh, RNG |
| pandas | Reading CSVs, writing simulation results |
| matplotlib | Circle patches and all figures |
| scipy | `curve_fit`, `minimize_scalar`, `norm` |
| shapely | Distance from a circle centre to an edge line |
| tqdm | Progress bar in `n_simulations` |
| python-dotenv | Loading `.env` |

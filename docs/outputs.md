# Outputs

All paths are relative to `OUTPUT_DIR` (default `data/output/`), which is gitignored. Directories are created as needed. Re-running a task **overwrites** its previous files.

## `surface`

### `csvs/growth_results_single_percolation_<model>.csv`

Always written. One row per time step (written by `utils/save_files.save_growth_results_summary`).

| Column | Type | Description |
|--------|------|-------------|
| `time_min` | float | Time step (min) |
| `target_coverage_pct` | float | Coverage from the fitted model (%) |
| `initial_simulated_coverage_pct` | float | Measured coverage before the correction loop (%) |
| `final_simulated_coverage_pct` | float | Measured coverage after correction (%) |
| `top_to_bottom` | bool | Connected path between top and bottom edges |
| `left_to_right` | bool | Connected path between left and right edges |
| `percolates` | bool | `top_to_bottom or left_to_right` |

The first row with `percolates = True` is this run's percolation threshold.

### Figures (only if `SHOW_PLOTS=True`)

Each figure is saved twice, as `images/…png` and `pdfs/…pdf`, at 300 dpi.

| Model | Fit figure | Per-time-step figures |
|-------|------------|-----------------------|
| logistic | `logistic/surface_coverage_vs_time_logistic` | `logistic/time_index_<t:.1f>min` |
| exponential | `exponential/surface_coverage_vs_time_exponential_with_derivative` | `exponential/<t:.2f>min` |

Per-time-step figures show the coverage mask before correction (left) and after (right). With very negative `t_min`, exponential filenames can start with `-`.

## `n_simulations`

### `csvs/growth_results_simulations_<model>.csv`

One row per simulation (fields of `models/simulation_result.SimulationResult`), in completion order.

| Column | Type | Description |
|--------|------|-------------|
| `simulation_id` | int | 1-based run number |
| `seed_used` | int | Seed used for nucleation (lets you reproduce a single run) |
| `percolated` | bool | Whether the run percolated within the time grid |
| `percolation_time_min` | float / empty | Time of first percolation |
| `percolation_target_coverage_pct` | float / empty | Model coverage at that time |
| `percolation_final_coverage_pct` | float / empty | Measured coverage at that time |
| `top_to_bottom` | bool | Direction(s) that percolated |
| `left_to_right` | bool | |
| `steps_simulated` | int | Time steps run (including the percolating one) |

Always written to `OUTPUT_DIR/csvs/`. `PERCOLATIONS_CSV_DIR` only controls where `results` looks for it.

## `results`

| Model | PNG | PDF |
|-------|-----|-----|
| logistic | `images/gaussian_curve_logistic.png` | `pdfs/gaussian_curve_logistic.pdf` |
| exponential | `images/exponential/gaussian_curve_exponential.png` | `pdfs/exponential/gaussian_curve_exponential.pdf` |

Panel **a**: histogram of area fraction at percolation with a Gaussian fit. Panel **b**: the same for percolation time. The legend shows mean ± standard deviation.

## Logs

`logs/run_<YYYYmmdd_HHMMSS>.log` (under `PROJECT_ROOT`, gitignored) records the same messages as the console: fitted parameters, per-step coverages, percolation events and saved file paths. Format:

```text
2026-03-04 12:00:00 | INFO | 123  | scripts.run_surface_logistic.simulate_growth | message
```

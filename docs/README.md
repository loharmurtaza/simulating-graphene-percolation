# Documentation

Detailed documentation for the Graphene Percolation Simulation. For a quick overview, the paper reference and the license, see the [project README](../README.md).

| Document | What it covers |
|----------|----------------|
| [Getting started](getting-started.md) | Installing, configuring and running your first simulation |
| [Configuration](configuration.md) | How `.env` is loaded and what every variable does |
| [CLI and pipelines](pipelines.md) | The `--model` / `--task` CLI and what each pipeline does step by step |
| [Growth models and fitting](growth-models.md) | Logistic, exponential and tanh² coverage models and how they are fitted |
| [Simulation and percolation](simulation-and-percolation.md) | Flake nucleation, radial growth, coverage measurement and percolation detection |
| [Outputs](outputs.md) | Every file the program writes, with CSV column descriptions |
| [Code reference](code-reference.md) | Module-by-module reference of the codebase |
| [Known limitations](known-limitations.md) | Assumptions, caveats and behaviour to be aware of |

## Typical workflow

```text
experimental_raw.csv
        │
        ▼
 ┌──────────────┐   single run, one seed, all time steps
 │   surface    │──► growth_results_single_percolation_<model>.csv + figures
 └──────────────┘
 ┌──────────────┐   N runs, random seeds, stop at first percolation
 │ n_simulations│──► growth_results_simulations_<model>.csv
 └──────────────┘
        │
        ▼
 ┌──────────────┐   Gaussian fit of percolation coverage and time
 │   results    │──► gaussian_curve_<model>.png / .pdf
 └──────────────┘
```

`surface` and `n_simulations` are independent; `results` needs the CSV produced by `n_simulations` for the same model.

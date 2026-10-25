# Getting started

## Requirements

- **Python 3.9–3.12.** The pinned `numpy==1.26.4` has no wheels for newer Python versions.
- Roughly 1 GB of free RAM per worker for `n_simulations` with the default `MESH_POINTS=1000` (each worker holds several 1000×1000 arrays).

## Install

```bash
git clone https://github.com/loharmurtaza/simulating-graphene-percolation.git
cd simulating-graphene-percolation

python -m venv venv
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Configure

The program reads its settings from a `.env` file in the project root. This file is gitignored, so create it from the template:

```bash
# Linux/macOS
cp .env.example .env
# Windows (PowerShell)
Copy-Item .env.example .env
```

The defaults in `.env.example` reproduce the setup used in the paper. Every variable must be present, because a missing one makes `config/settings.py` fail when the configuration is built. See [configuration.md](configuration.md) for what each variable does.

## Run

Always run from the project root. The paths in `.env` are relative to the current working directory, and the modules import each other as top-level packages (`config`, `utils`, ...).

```bash
# 1. Single surface-coverage run (quick, one seed)
python -m main --model logistic --task surface

# 2. Monte Carlo runs (slow; tune SIMULATIONS_TO_RUN / MAX_WORKERS first)
python -m main --model logistic --task n_simulations

# 3. Statistics over the Monte Carlo runs
python -m main --model logistic --task results
```

Swap `logistic` for `exponential` to use the exponential (tanh²-type) growth model.

Results appear under `data/output/` and logs under `logs/`. See [outputs.md](outputs.md).

### Quick smoke test

For a fast check that everything works, temporarily lower the cost in `.env`:

```dotenv
MESH_POINTS=200
SIMULATIONS_TO_RUN=10
MAX_WORKERS=2
```

Coarser meshes make the measured coverage less precise, so restore the defaults for real runs.

## Standalone fit scripts

`scripts/test_scripts/` contains two scripts that only fit and plot a model, with no simulation. They are not automated tests.

```bash
python -m scripts.test_scripts.test_exponential_function
python -m scripts.test_scripts.test_tanh_squared
```

They save figures only when `SHOW_PLOTS=True`.

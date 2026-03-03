# main_graphene_percolation.py

from __future__ import annotations

import logging
import argparse
from utils.config_logger import setup_logging
from load_env_variables import load_dotenv_variables
from scripts.run_surface_logistic import (
    run_pipeline_logistic as run_surface_logistic
)
from scripts.run_surface_exponential import (
    run_pipeline_exponential as run_surface_exponential
)
from scripts.run_results_logistic import (
    run_pipeline_logistic as run_results_logistic
)
from scripts.run_results_exponential import (
    run_pipeline_exponential as run_results_exponential
)
from scripts.run_simulations_logistic import (
    run_pipeline_logistic as run_simulations_logistic
)
from scripts.run_simulations_exponential import (
    run_pipeline_exponential as run_simulations_exponential
)
from config.settings import (
    SurfaceCoverageConfig,
    SimulationsConfig,
    FinalResultsConfig,
)


# -------------------------------------------------
# Command Line Interface
# -------------------------------------------------
def cli() -> None:
    """
    Command line interface for the graphene percolation model.
    """
    setup_logging(level=logging.INFO)

    p = argparse.ArgumentParser(description='Graphene Percolation Model')
    p.add_argument(
        "--model",
        choices=["logistic", "exponential"],
        required=True,
    )
    p.add_argument(
        "--task",
        choices=["surface", "n_simulations", "results"],
        required=True,
    )
    args = p.parse_args()

    if args.task == "surface":
        cfg = SurfaceCoverageConfig()
        if args.model == "logistic":
            run_surface_logistic(cfg)
        elif args.model == "exponential":
            run_surface_exponential(cfg)
    elif args.task == "n_simulations":
        cfg = SurfaceCoverageConfig()
        sim_cfg = SimulationsConfig()
        if args.model == "logistic":
            run_simulations_logistic(cfg, sim_cfg)
        elif args.model == "exponential":
            run_simulations_exponential(cfg, sim_cfg)
    else:
        cfg = FinalResultsConfig()
        if args.model == "logistic":
            run_results_logistic(cfg)
        elif args.model == "exponential":
            run_results_exponential(cfg)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    cli()

# main_graphene_percolation.py

from __future__ import annotations

import logging
import argparse
from utils.config_logger import setup_logging
from scripts.run_surface import run_pipeline as run_surface
from scripts.run_results import run_pipeline as run_results
from scripts.run_simulations import run_pipeline as run_simulations
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
        "--task",
        choices=["surface", "n_simulations", "results"],
        required=True,
    )
    args = p.parse_args()

    if args.task == "surface":
        cfg = SurfaceCoverageConfig()
        run_surface(cfg)
    elif args.task == "n_simulations":
        cfg = SurfaceCoverageConfig()
        sim_cfg = SimulationsConfig()
        run_simulations(cfg, sim_cfg)
    else:
        cfg = FinalResultsConfig()
        run_results(cfg)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    cli()

# main_graphene_percolation.py

from __future__ import annotations

import argparse
from scripts.run_surface import run_pipeline as run_surface
from scripts.run_results import run_pipeline as run_results
from config.settings import SurfaceCoverageConfig, FinalResultsConfig


# -------------------------------------------------
# Command Line Interface
# -------------------------------------------------
def cli() -> None:
    """
    Command line interface for the graphene percolation model.
    """
    p = argparse.ArgumentParser(description='Graphene Percolation Model')
    p.add_argument("--task", choices=["surface", "results"], required=True)
    args = p.parse_args()

    if args.task == "surface":
        cfg = SurfaceCoverageConfig()
        run_surface(cfg)
    else:
        cfg = FinalResultsConfig()
        run_results(cfg)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    cli()

# scripts/run_simulations_logistic.py

from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from dataclasses import asdict
from typing import List, Optional
import matplotlib.patches as patches
from multiprocessing import Pool, cpu_count
from models.growth_result import GrowthResult
from utils.visualization import generate_graph
from utils.io import load_experimental_raw_data
from models.simulation_result import SimulationResult
from utils.search_algorithm import breadth_first_search
from config.settings import (
    SurfaceCoverageConfig, SimulationsConfig, OUTPUT_DIR
)
from utils.math import (
    fit_surface_coverage_logistic,
    logistic,
    random_points,
    build_initial_circles,
)

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(OUTPUT_DIR)


# -------------------------------------------------
# Run Simulations (early-stopping)
# -------------------------------------------------
def simulate_growth_until_percolation(
    circles: List[patches.Circle],
    t_fit: np.ndarray,
    S_fit: np.ndarray,
    cfg: SurfaceCoverageConfig,
) -> tuple[bool, Optional[GrowthResult], int]:
    """
    Simulate radial growth and STOP at the first time-step where
    percolation occurs.
    Returns:
      (percolated?, growth_result_at_percolation_or_None, steps_simulated)
    """
    grid_size = cfg.grid_size_microns
    x = np.linspace(0, grid_size, cfg.mesh_points)
    y = np.linspace(0, grid_size, cfg.mesh_points)
    xv, yv = np.meshgrid(x, y)

    grid_mask = (xv >= 0) & (xv <= grid_size) & (yv >= 0) & (yv <= grid_size)

    for t_index, time in enumerate(t_fit):
        num = len(circles)

        target_area = S_fit[t_index] / num * 100
        target_radius = np.sqrt(target_area / np.pi)

        grown = []
        surface_coverage = np.zeros_like(xv, dtype=bool)

        for c in circles:
            gc = patches.Circle(
                c.center, radius=target_radius, fill=True, edgecolor='blue',
            )
            grown.append(gc)
            dist = np.sqrt((xv - gc.center[0])**2 + (yv - gc.center[1])**2)
            surface_coverage |= dist <= gc.radius

        surface_coverage &= grid_mask
        frac = float(np.sum(surface_coverage) / np.sum(grid_mask))

        final_grown = grown
        final_cov = surface_coverage
        final_frac = frac

        tolerance = 1.0
        while (S_fit[t_index] - final_frac * 100) > tolerance:
            delta_pct = float(S_fit[t_index] - final_frac * 100)
            delta_area = delta_pct / num * 100
            final_target_area = target_area + delta_area
            final_target_radius = np.sqrt(final_target_area / np.pi)

            final_grown = []
            final_cov = np.zeros_like(xv, dtype=bool)
            for gc in grown:
                fgc = patches.Circle(
                    gc.center, radius=final_target_radius,
                    fill=True, edgecolor='blue',
                )
                final_grown.append(fgc)
                dist = np.sqrt(
                    (xv - fgc.center[0])**2 + (yv - fgc.center[1])**2,
                )
                final_cov |= dist <= fgc.radius

            final_cov &= grid_mask
            final_frac = float(np.sum(final_cov) / np.sum(grid_mask))
            target_area = final_target_area

        # Build graph + percolation checks
        graph, top, bottom, left, right = generate_graph(
            final_grown, grid_size,
        )

        top_to_bottom = False
        for start in top.keys():
            _, ok = breadth_first_search(graph, start, bottom.keys())
            if ok:
                top_to_bottom = True
                break

        left_to_right = False
        for start in left.keys():
            _, ok = breadth_first_search(graph, start, right.keys())
            if ok:
                left_to_right = True
                break

        gr = GrowthResult(
            time_min=float(time),
            target_coverage_pct=float(S_fit[t_index]),
            initial_simulated_coverage_pct=float(frac * 100),
            final_simulated_coverage_pct=float(final_frac * 100),
            top_to_bottom=top_to_bottom,
            left_to_right=left_to_right,
        )

        # EARLY STOP condition
        if top_to_bottom or left_to_right:
            return True, gr, t_index + 1

        # otherwise continue growth
        circles = final_grown

    # no percolation found in the full horizon
    return False, None, len(t_fit)


# -------------------------------------------------
# Run single simulation
# -------------------------------------------------
def _run_single_simulation(args: tuple) -> dict:
    """
    Worker function for a single simulation.
    Must be top-level for multi-processing pickling.
    """
    (
        sim_id,
        seed,
        cfg,
        t_fit,
        S_fit,
    ) = args

    # Fresh initial nucleation for each run
    points = random_points(
        cfg.num_circles,
        cfg.grid_size_microns,
        random_seed=seed,
    )

    circles = build_initial_circles(
        points,
        radius=cfg.initial_radius_microns,
    )

    percolated, gr, steps = simulate_growth_until_percolation(
        circles,
        t_fit,
        S_fit,
        cfg,
    )

    if percolated and gr is not None:
        result = SimulationResult(
            simulation_id=sim_id,
            seed_used=seed,
            percolated=True,
            percolation_time_min=gr.time_min,
            percolation_target_coverage_pct=gr.target_coverage_pct,
            percolation_final_coverage_pct=gr.final_simulated_coverage_pct,
            top_to_bottom=gr.top_to_bottom,
            left_to_right=gr.left_to_right,
            steps_simulated=steps,
        )
    else:
        result = SimulationResult(
            simulation_id=sim_id,
            seed_used=seed,
            percolated=False,
            percolation_time_min=None,
            percolation_target_coverage_pct=None,
            percolation_final_coverage_pct=None,
            top_to_bottom=False,
            left_to_right=False,
            steps_simulated=steps,
        )

    return asdict(result)


# -------------------------------------------------
# Run N simulations and write a single CSV
# -------------------------------------------------
def run_pipeline_logistic(
    cfg: SurfaceCoverageConfig = SurfaceCoverageConfig(),
    sim_cfg: SimulationsConfig = SimulationsConfig()
) -> None:
    """
    Run N simulations and write a single CSV
    """
    out_csv_dir = OUTPUT_DIR / 'csvs'
    out_csv_dir.mkdir(parents=True, exist_ok=True)

    # Fit Logistic once (shared)
    t_data, S_data, std_data = load_experimental_raw_data(cfg.raw_data_path)
    if cfg.use_std:
        (L, k, t0), pcov = fit_surface_coverage_logistic(
            t_data, S_data, std_data,
        )
    else:
        (L, k, t0), pcov = fit_surface_coverage_logistic(
            t_data, S_data,
        )

    t_fit = np.arange(0, 27.1, 0.1)
    S_fit = logistic(t_fit, L, k, t0)

    # ensure each simulation gets a different seed
    rng = np.random.default_rng()
    records: list[dict] = []

    n = int(sim_cfg.simulations_to_run)
    logger.info(f"Running {n} simulations (unique seed per simulation)")

    # -------------------------------------------------
    # Multiprocessing execution
    # -------------------------------------------------
    num_workers = min(sim_cfg.max_workers, cpu_count())
    logger.info(f"Using {num_workers} worker processes")

    rng = np.random.default_rng()
    seeds = rng.integers(1, 2_147_483_647, size=n)

    worker_args = [
        (
            sim_id+1,
            int(seeds[sim_id]),
            cfg,
            t_fit,
            S_fit,
        )
        for sim_id in range(n)
    ]

    with Pool(processes=num_workers) as pool:
        records = list(
            tqdm(
                pool.imap_unordered(_run_single_simulation, worker_args),
                total=n,
                desc="Simulations (parallel)",
            )
        )

    df = pd.DataFrame(records)
    out_path = out_csv_dir / "growth_results_simulations_logistic.csv"
    df.to_csv(out_path, index=False)

    logger.info(f"Wrote {len(df)} rows -> {out_path}")


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    cfg = SurfaceCoverageConfig()
    sim_cfg = SimulationsConfig()
    run_pipeline_logistic(cfg, sim_cfg)

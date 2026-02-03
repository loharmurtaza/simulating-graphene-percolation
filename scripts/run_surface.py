# scripts/run_surface.py

from __future__ import annotations

import logging
import numpy as np
from typing import List
from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass
import matplotlib.patches as patches
from config.settings import OUTPUT_DIR
from utils.config_logger import setup_logging
from utils.visualization import generate_graph
from utils.io import load_experimental_raw_data
from config.settings import SurfaceCoverageConfig
from utils.search_algorithm import breadth_first_search
from utils.math import random_points, build_initial_circles
from utils.save_files import save_fig_as_png, save_fig_as_pdf
from utils.math import (
    fit_surface_coverage_logistic, logistic, logistic_derivative,
)

setup_logging()
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(OUTPUT_DIR)


# -------------------------------------------------
# Growth Result
# -------------------------------------------------
@dataclass
class GrowthResult:
    time_min: float
    target_coverage_pct: float
    achieved_coverage_pct: float
    top_to_bottom: bool
    left_to_right: bool
    coverage_mask: np.ndarray


# -------------------------------------------------
# Simulate Growth
# -------------------------------------------------
def simulate_growth(
    circles: List[patches.Circle],
    t_fit: np.ndarray,
    S_fit: np.ndarray,
    cfg: SurfaceCoverageConfig,
    show_plots: bool = False,
) -> List[GrowthResult]:
    """
    Simulate radial growth to match target coverage, then test percolation.
    """
    logger.info(
        f"Simulating growth: circles={circles}, t_fit={t_fit},"
        f"S_fit={S_fit}, cfg={cfg}, show_plots={show_plots}",
    )
    grid_size = cfg.grid_size_microns
    x = np.linspace(0, grid_size, cfg.mesh_points)
    y = np.linspace(0, grid_size, cfg.mesh_points)
    xv, yv = np.meshgrid(x, y)

    results: List[GrowthResult] = []
    grid_mask = (xv >= 0) & (xv <= grid_size) & (yv >= 0) & (yv <= grid_size)

    for t_index, time in enumerate(t_fit):
        logger.info(f"Simulating growth: t_index={t_index}, time={time}")
        num = len(circles)

        target_area = S_fit[t_index] / num * 100
        logger.info(f"Target area: {target_area}")
        target_radius = np.sqrt(target_area / np.pi)
        logger.info(f"Target radius: {target_radius}")

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
        logger.info(f"Surface coverage: {frac}")

        final_grown = grown
        final_cov = surface_coverage
        final_frac = frac
        logger.info(f"Final grown: {final_grown}")
        logger.info(f"Final coverage: {final_cov}")
        logger.info(f"Final fraction: {final_frac}")

        tolerance = 1.0
        while (S_fit[t_index] - final_frac * 100) > tolerance:
            delta_pct = float(S_fit[t_index] - final_frac * 100)
            delta_area = delta_pct / num * 100
            final_target_area = target_area + delta_area
            final_target_radius = np.sqrt(final_target_area / np.pi)
            logger.info(f"Final target area: {final_target_area}")
            logger.info(f"Final target radius: {final_target_radius}")

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

        logger.info(
            f"Generating graph: final_grown={final_grown},"
            f"grid_size={grid_size}",
        )
        graph, top, bottom, left, right = generate_graph(
            final_grown, grid_size,
        )

        logger.info(f"Graph generated: graph={graph}")
        logger.info(f"Top: {top}")
        logger.info(f"Bottom: {bottom}")
        logger.info(f"Left: {left}")
        logger.info(f"Right: {right}")

        top_to_bottom = False
        for start in top.keys():
            _, ok = breadth_first_search(graph, start, bottom.keys())
            if ok:
                logger.info(f"Top to bottom found: {start}")
                top_to_bottom = True
                break

        left_to_right = False
        for start in left.keys():
            _, ok = breadth_first_search(graph, start, right.keys())
            if ok:
                logger.info(f"Left to right found: {start}")
                left_to_right = True
                break

        if show_plots:
            fig, ax = plt.subplots(1, 2, figsize=(18, 8))
            ax[0].imshow(surface_coverage, extent=(0, grid_size, 0, grid_size))
            ax[0].set_xlabel("Length (μm)")
            ax[0].set_ylabel("Length (μm)")
            ax[1].imshow(final_cov, extent=(0, grid_size, 0, grid_size))
            ax[1].set_xlabel("Length (μm)")
            ax[1].set_ylabel("Length (μm)")
            plt.show()
            logger.info("Plots shown")

        results.append(
            GrowthResult(
                time_min=float(time),
                target_coverage_pct=float(S_fit[t_index]),
                achieved_coverage_pct=float(final_frac * 100),
                top_to_bottom=top_to_bottom,
                left_to_right=left_to_right,
                coverage_mask=final_cov,
            )
        )
        logger.info(f"Results appended: {results}")

        circles = final_grown
        logger.info(f"Circles updated: {circles}")

    logger.info(f"Simulated growth completed: {results}")
    return results


# -------------------------------------------------
# Run Surface Coverage Pipeline
# -------------------------------------------------
def run_pipeline(
    cfg: SurfaceCoverageConfig = SurfaceCoverageConfig()
) -> None:
    """
    Run the surface coverage pipeline.
    """
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

    derivative = logistic_derivative(t_fit, S_fit, k, t0)

    if cfg.show_plots:
        logger.info(
            f"Fitting surface coverage logistic: L={L}, k={k}, t0={t0}",
        )

        ylabel_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        plt.figure(figsize=(12, 6))

        plt.errorbar(
            t_data, S_data, yerr=std_data, fmt='o', color='red', capsize=4,
            label=r'Data points ± SD', markersize=4,
        )
        plt.plot(t_fit, S_fit, color='blue', label='Logistic Fit')
        plt.plot(
            t_fit, derivative, linestyle='--',
            label='Derivative', color='green',
        )
        plt.xlabel('Synthesis Time (min)', fontsize=14)
        plt.ylabel(r'graphene coverage ($\theta_G$)', fontsize=14)
        plt.xticks(np.arange(0, 30, 5), fontsize=14)
        plt.yticks(np.arange(0, 120, 20), ylabel_ticks, fontsize=14)

        handles, labels = plt.gca().get_legend_handles_labels()
        order = [
            labels.index('Data points ± SD'),
            labels.index('Logistic Fit'),
            labels.index('Derivative'),
        ]
        plt.legend(
            [handles[i] for i in order],
            [labels[i] for i in order],
            frameon=False,
            fontsize=14,
            loc='upper left',
        )
        plt.grid(False)

        save_fig_as_png(
            plt.gcf(),
            OUTPUT_DIR / 'surface_coverage_vs_synthesis_time.png',
            dpi=300,
        )
        save_fig_as_pdf(
            plt.gcf(),
            OUTPUT_DIR / 'surface_coverage_vs_synthesis_time.pdf',
            dpi=300,
        )
        plt.show()

    points = random_points(
        cfg.num_circles, cfg.grid_size_microns, random_seed=cfg.random_seed,
    )
    circles = build_initial_circles(points, radius=cfg.initial_radius_microns)

    simulate_growth(circles, t_fit, S_fit, cfg, show_plots=cfg.show_plots)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == '__main__':
    cfg = SurfaceCoverageConfig()
    run_pipeline(cfg)

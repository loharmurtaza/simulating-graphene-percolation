# scripts/run_surface_exponential.py

from __future__ import annotations

import logging
import numpy as np
from typing import List
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from config.settings import OUTPUT_DIR
from models.growth_result import GrowthResult
from utils.visualization import generate_graph
from utils.io import load_experimental_raw_data
from config.settings import SurfaceCoverageConfig
from utils.search_algorithm import breadth_first_search
from utils.math import random_points, build_initial_circles
from utils.save_files import (
    save_fig_as_png, save_fig_as_pdf, save_growth_results_summary,
)
from utils.math import (
    fit_surface_coverage_exponential,
    exponential_function,
    exponential_function_derivative,
    estimate_mean_areas_from_coverage,
)

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(OUTPUT_DIR)


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
    grid_size = cfg.grid_size_microns
    x = np.linspace(0, grid_size, cfg.mesh_points)
    y = np.linspace(0, grid_size, cfg.mesh_points)
    xv, yv = np.meshgrid(x, y)

    results: List[GrowthResult] = []
    grid_mask = (xv >= 0) & (xv <= grid_size) & (yv >= 0) & (yv <= grid_size)

    for t_index, time in enumerate(t_fit):
        logger.info(
            f"Simulating growth: t_index={t_index}, "
            f"time={np.round(time, 3)} minutes",
        )
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

        graph, top, bottom, left, right = generate_graph(
            final_grown, grid_size,
        )

        top_to_bottom = False
        for start in top.keys():
            _, ok = breadth_first_search(graph, start, bottom.keys())
            if ok:
                logger.info("Top to bottom percolation found")
                top_to_bottom = True
                break

        left_to_right = False
        for start in left.keys():
            _, ok = breadth_first_search(graph, start, right.keys())
            if ok:
                logger.info("Left to right percolation found")
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

            name = f'exponential/{time:.2f}min'
            save_fig_as_png(
                plt.gcf(),
                OUTPUT_DIR/'images'/f'{name}.png',
                dpi=300,
            )
            save_fig_as_pdf(
                plt.gcf(),
                OUTPUT_DIR/'pdfs'/f'{name}.pdf',
                dpi=300,
            )
            plt.close()

        results.append(
            GrowthResult(
                time_min=float(time),
                target_coverage_pct=float(S_fit[t_index]),
                initial_simulated_coverage_pct=float(frac * 100),
                final_simulated_coverage_pct=float(final_frac * 100),
                top_to_bottom=top_to_bottom,
                left_to_right=left_to_right,
            )
        )

        logger.info(
            f"Percentage area according to exponential function: "
            f"{S_fit[t_index]:.3f}%"
        )
        logger.info(
            f"Percentage area according to simulation: "
            f"{frac * 100:.3f}%"
        )
        logger.info(
            f"Final percentage area according to simulation: "
            f"{final_frac * 100:.3f}%"
        )

        logger.info("Results appended")

        circles = final_grown
        logger.info("Circles updated\n\n")

    logger.info("Simulated growth completed")
    return results


# -------------------------------------------------
# Run Surface Coverage Pipeline
# -------------------------------------------------
def run_pipeline_exponential(
    cfg: SurfaceCoverageConfig = SurfaceCoverageConfig()
) -> None:
    """
    Run the surface coverage pipeline.
    """
    t_data, S_data, std_data = load_experimental_raw_data(cfg.raw_data_path)

    if cfg.use_std:
        params, pcov = fit_surface_coverage_exponential(
            t_data, S_data, std_data,
        )
    else:
        params, pcov = fit_surface_coverage_exponential(
            t_data, S_data,
        )

    alpha, C1 = params[0], params[1]
    t_min = -C1/alpha if alpha != 0 else 0

    t_fit = np.linspace(t_min, 30, 500)
    S_fit = exponential_function(t_fit, alpha, C1)

    derivative = exponential_function_derivative(t_fit, alpha, C1)

    idx_max = np.argmax(derivative)
    logger.info(
        "Derivative maximum: t = %.4f min, S = %.4f %%",
        float(t_fit[idx_max]),
        float(S_fit[idx_max]),
    )

    if cfg.show_plots:
        logger.info(
            "Fitting surface coverage exponential",
        )

        plt.figure(figsize=(12, 6))

        plt.errorbar(
            t_data, S_data, yerr=std_data, fmt='o', color='red', capsize=4,
            label=r'Data points ± SD', markersize=4,
        )
        plt.scatter(
            t_fit[idx_max],
            derivative[idx_max],
            color='black',
            marker='o',
            s=40,
            label='Inflaction Point',
        )
        plt.axhline(
            y=0,
            xmin=0,
            xmax=0.04,
            color='black',
            linestyle='--',
            label='Minimum',
        )
        plt.plot(
            t_fit, S_fit, color='blue',
            label='Exponential Fit'
        )
        plt.plot(
            t_fit, derivative, linestyle='--',
            label='Derivative', color='green',
        )
        plt.xlabel('Synthesis Time (min)', fontsize=14)
        plt.ylabel(r'Graphene Coverage ($\theta_G$)', fontsize=14)
        plt.xticks(np.arange(0, 31, 5), fontsize=14)
        plt.yticks(np.arange(0, 110, 20), fontsize=14)

        ax = plt.gca()
        ax.set_yticklabels(
            labels=np.round(np.arange(0, 1.1, 0.2), 2),
            fontsize=14
        )

        plt.xlim(min(t_min, 0), 30)
        # plt.ylim(-0.05, 100.05)

        handles, labels = plt.gca().get_legend_handles_labels()
        order = [
            labels.index('Data points ± SD'),
            labels.index('Exponential Fit'),
            labels.index('Derivative'),
            labels.index('Inflaction Point'),
        ]
        plt.legend(
            [handles[i] for i in order],
            [labels[i] for i in order],
            frameon=False,
            fontsize=12,
            loc='upper left',
        )
        plt.grid(False)

        name = 'surface_coverage_vs_time_exponential_with_derivative'
        save_fig_as_png(
            plt.gcf(),
            OUTPUT_DIR/'images'/'exponential'/f'{name}.png',
            dpi=300,
        )
        save_fig_as_pdf(
            plt.gcf(),
            OUTPUT_DIR/'pdfs'/'exponential'/f'{name}.pdf',
            dpi=300,
        )
        plt.close()

    # Mean area of flakes for the first two samples
    mean_area = np.array([6.8, 106.58])
    coverage_data = np.array([3.2, 51.2])

    estimated_mean_areas = estimate_mean_areas_from_coverage(
        coverage_data, mean_area, S_data,
    )

    # Display the estimated mean areas
    for t, s, area in zip(t_data, S_data, estimated_mean_areas):
        logger.info(
            f"At time {t:.1f} minutes, "
            f"surface coverage is {s:.1f}% and "
            f"the estimated mean area is {area:.2f} square microns."
        )

    points = random_points(
        cfg.num_circles, cfg.grid_size_microns, random_seed=cfg.random_seed,
    )
    circles = build_initial_circles(points, radius=cfg.initial_radius_microns)

    results = simulate_growth(
        circles, t_fit, S_fit, cfg, show_plots=cfg.show_plots,
    )

    save_growth_results_summary(
        results,
        OUTPUT_DIR/'csvs'/'growth_results_single_percolation_exponential.csv',
    )


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == '__main__':
    cfg = SurfaceCoverageConfig()
    run_pipeline_exponential(cfg)

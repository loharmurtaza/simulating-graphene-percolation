# scripts/test_scripts/test_exponential_function.py

from __future__ import annotations

import logging
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from config.settings import OUTPUT_DIR
from utils.config_logger import setup_logging
from utils.io import load_experimental_raw_data
from config.settings import SurfaceCoverageConfig
from utils.save_files import (
    save_fig_as_png,
    save_fig_as_pdf,
)
from utils.math import (
    fit_surface_coverage_exponential,
    exponential_function_derivative,
    exponential_function,
)

logger = logging.getLogger("test_exponential_function")

OUTPUT_DIR = Path(OUTPUT_DIR)


# -------------------------------------------------
# Run Surface Coverage Pipeline
# -------------------------------------------------
def exponential_function_fit(
    cfg: SurfaceCoverageConfig = SurfaceCoverageConfig()
) -> None:
    """
    Run the surface coverage fit for exponential function.
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
            "Fitting surface coverage exponential function",
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

        name = 'surface_coverage_vs_time_exponential'

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


if __name__ == "__main__":
    setup_logging()
    exponential_function_fit()

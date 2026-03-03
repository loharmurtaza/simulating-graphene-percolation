# scripts/test_scripts/test_tanh_squared.py

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
    fit_surface_coverage_tanh_squared,
    tanh_squared_derivative,
    tanh_squared,
)

logger = logging.getLogger("test_tanh_squared")

OUTPUT_DIR = Path(OUTPUT_DIR)


# -------------------------------------------------
# Run Surface Coverage Pipeline
# -------------------------------------------------
def tanh_squared_fit(
    cfg: SurfaceCoverageConfig = SurfaceCoverageConfig()
) -> None:
    """
    Run the surface coverage fit for tanh^2 function.
    """
    t_data, S_data, std_data = load_experimental_raw_data(cfg.raw_data_path)

    if cfg.use_std:
        params, pcov = fit_surface_coverage_tanh_squared(
            t_data, S_data, std_data,
        )
    else:
        params, pcov = fit_surface_coverage_tanh_squared(
            t_data, S_data,
        )

    t_fit = np.arange(0, 27.1, 0.1)
    S_fit = tanh_squared(t_fit, *params)

    derivative = tanh_squared_derivative(t_fit, *params)

    if cfg.show_plots:
        logger.info(
            "Fitting surface coverage tanh^2 function",
        )

        ylabel_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        plt.figure(figsize=(12, 6))

        plt.errorbar(
            t_data, S_data, yerr=std_data, fmt='o', color='red', capsize=4,
            label=r'Data points ± SD', markersize=4,
        )
        plt.plot(t_fit, S_fit, color='blue', label='tanh^2 Fit')
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
            labels.index('tanh^2 Fit'),
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
            OUTPUT_DIR/'images'/'surface_coverage_vs_time_tanh_squared.png',
            dpi=300,
        )
        save_fig_as_pdf(
            plt.gcf(),
            OUTPUT_DIR/'pdfs'/'surface_coverage_vs_time_tanh_squared.pdf',
            dpi=300,
        )
        plt.close()


if __name__ == "__main__":
    setup_logging()
    tanh_squared_fit()

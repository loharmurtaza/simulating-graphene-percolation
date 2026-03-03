# scripts/run_results_logistic.py

from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import norm
import matplotlib.pyplot as plt
from config.settings import FinalResultsConfig, OUTPUT_DIR
from utils.save_files import save_fig_as_pdf, save_fig_as_png

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(OUTPUT_DIR)


# -------------------------------------------------
# Plot Gaussian Curves
# -------------------------------------------------
def plot_gaussian_curves(
    growth_results: pd.DataFrame,
) -> None:
    """
    Plot Gaussian curves for the percolations.
    """
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))

    # Surface coverage / area fraction
    percentages = growth_results[
        'percolation_final_coverage_pct'
    ].astype(float).to_list()
    mean_pct, std_pct = norm.fit(percentages)
    x_pct = np.linspace(0, 100, 500)

    bins_pct = np.arange(0, 105, 4)
    counts, bin_edges, _ = ax[0].hist(
        percentages,
        bins=20,
        edgecolor='white',
        color='orange'
    )

    bin_width = bin_edges[1] - bin_edges[0]
    N = len(percentages)
    p_pct = norm.pdf(x_pct, mean_pct, std_pct)
    p_pct_counts = p_pct * N * bin_width

    ax[0].plot(
        x_pct,
        p_pct_counts,
        linestyle='--',
        label=f'Mean Area Fraction: {mean_pct:.0f}% ± {std_pct:.0f}%',
        c='purple',
    )
    ax[0].axvline(
        mean_pct,
        ymin=0,
        ymax=p_pct_counts.max() / max(counts),
        color='black',
        linestyle='--'
    )
    ax[0].set_xlabel('Area Fraction (%)', fontsize=15)
    ax[0].set_xticks(bins_pct)
    ax[0].set_xticklabels(labels=bins_pct, fontsize=14)
    ax[0].set_xlim(40, 90)
    ax[0].legend(frameon=False, fontsize=13, loc='upper right')
    ax[0].text(
        0.05,
        0.95,
        'a',
        transform=ax[0].transAxes,
        fontsize=20,
        fontweight='bold',
        va='top',
    )

    # Time
    times = growth_results['percolation_time_min'].astype(float).to_list()
    mean_time, std_time = norm.fit(times)
    x_time = np.linspace(0, 10, 500)

    bins_time = np.arange(0, 10, 0.2)
    counts, bin_edges, _ = ax[1].hist(
        times,
        bins=20,
        edgecolor='white',
        color='orange',
    )
    bin_width = bin_edges[1] - bin_edges[0]
    N = len(times)
    p_time = norm.pdf(x_time, mean_time, std_time)
    p_time_counts = p_time * N * bin_width
    ax[1].plot(
        x_time,
        p_time_counts,
        linestyle='--',
        label=f'Mean Time: {mean_time:.2f} min ± {std_time:.2f}min',
        c='purple',
    )
    ax[1].axvline(
        mean_time,
        ymin=0,
        ymax=p_time_counts.max() / max(counts),
        color='black',
        linestyle='--'
    )
    ax[1].set_xlabel('Time (min)', fontsize=15)
    ax[1].set_xticks(bins_time)
    ax[1].set_xticklabels(labels=np.round(bins_time, 2), fontsize=14)
    ax[1].set_xlim(4.9, 7.0)
    ax[1].legend(frameon=False, fontsize=13, loc='upper right')
    ax[1].text(
        0.05,
        0.95,
        'b',
        transform=ax[1].transAxes,
        fontsize=20,
        fontweight='bold',
        va='top',
    )

    save_fig_as_png(
        plt.gcf(),
        OUTPUT_DIR / 'images' / 'gaussian_curve_logistic.png',
        dpi=300,
    )
    save_fig_as_pdf(
        plt.gcf(),
        OUTPUT_DIR / 'pdfs' / 'gaussian_curve_logistic.pdf',
        dpi=300,
    )
    plt.close()


# -------------------------------------------------
# Run Final Results Pipeline
# -------------------------------------------------
def run_pipeline_logistic(
    cfg: FinalResultsConfig = FinalResultsConfig(),
    csv_path: str | Path | None = None,
) -> None:
    """
    Run the final results pipeline.
    """
    if csv_path is None:
        csv_path = Path(cfg.percolations_csv_dir)

    csv_name = csv_path / 'growth_results_simulations_logistic.csv'
    growth_results = pd.read_csv(csv_name, index_col=0)
    plot_gaussian_curves(growth_results)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == '__main__':
    cfg = FinalResultsConfig()
    run_pipeline_logistic(cfg)

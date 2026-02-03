# scripts/run_results.py

from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import norm
import matplotlib.pyplot as plt
from config.settings import FinalResultsConfig


# -------------------------------------------------
# Plot Gaussian Curves
# -------------------------------------------------
def plot_gaussian_curves(
    all_percolations: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Plot Gaussian curves for the percolations.
    """
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))

    # Surface coverage / area fraction
    percentages = all_percolations['Area (%)'].astype(float).to_list()
    mean_pct, std_pct = norm.fit(percentages)
    x_pct = np.linspace(0, 100, 500)
    p_pct = norm.pdf(x_pct, mean_pct, std_pct)
    p_pct *= 34 * np.max(percentages)

    ax[0].axvline(mean_pct, ymin=0, ymax=0.88, color='black', linestyle='--')
    bins_pct = np.arange(0, 105, 4)
    ax[0].hist(percentages, bins=17, edgecolor='white', color='orange')
    ax[0].plot(
        x_pct,
        p_pct,
        linestyle='--',
        label=f'Mean Area Fraction: {mean_pct:.0f}% ± {std_pct:.0f}%',
        c='purple',
    )
    ax[0].set_xlabel('Area Fraction (%)', fontsize=15)
    ax[0].set_ylabel('Normalized Frequency', fontsize=15)
    ax[0].set_xticks(bins_pct)
    ax[0].set_xticklabels(labels=bins_pct, fontsize=14)
    ax[0].set_yticks(np.arange(0, 1000, 50))
    ax[0].set_xlim(40, 90)
    ax[0].set_ylim(0, 200)
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
    times = all_percolations['Time (min)'].astype(float).to_list()
    mean_time, std_time = norm.fit(times)
    x_time = np.linspace(0, 10, 500)
    p_time = norm.pdf(x_time, mean_time, std_time)
    p_time *= 15.3 * np.max(times)
    ax[1].axvline(mean_time, ymin=0, ymax=0.88, color='black', linestyle='--')
    bins_time = np.arange(0, 10, 0.2)
    ax[1].hist(times, bins=18, edgecolor='white', color='orange')
    ax[1].plot(
        x_time,
        p_time,
        linestyle='--',
        label=f'Mean Time: {mean_time:.2f} min ± {std_time:.2f}min',
        c='purple',
    )
    ax[1].set_xlabel('Time (min)', fontsize=15)
    ax[1].set_ylabel('Normalized Frequency', fontsize=15)
    ax[1].set_xticks(bins_time)
    ax[1].set_xticklabels(labels=np.round(bins_time, 2), fontsize=14)
    ax[1].set_yticks(np.arange(0, 1000, 50))
    ax[1].set_yticklabels(np.round(np.arange(0, 1, 0.05), 4), fontsize=14)
    ax[1].set_xlim(4.9, 7.0)
    ax[1].set_ylim(0, 200)
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

    plt.savefig(output_path)
    plt.close()


# -------------------------------------------------
# Run Final Results Pipeline
# -------------------------------------------------
def run_pipeline(
    cfg: FinalResultsConfig = FinalResultsConfig(),
    csv_path: str | Path | None = None,
) -> None:
    """
    Run the final results pipeline.
    """
    if csv_path is None:
        csv_path = Path(cfg.percolations_csv_name)

    all_percolations = pd.read_csv(csv_path, index_col=0)
    output_path = Path(cfg.output_figure_name)
    plot_gaussian_curves(all_percolations, output_path)


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == '__main__':
    cfg = FinalResultsConfig()
    run_pipeline(cfg)

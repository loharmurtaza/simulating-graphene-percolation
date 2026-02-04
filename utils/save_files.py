# utils/save_files.py

from __future__ import annotations

import csv
import logging
from typing import List
from pathlib import Path
import matplotlib.pyplot as plt
from models.growth_result import GrowthResult

logger = logging.getLogger(__name__)


# -------------------------------------------------
# Save Figure as PNG
# -------------------------------------------------
def save_fig_as_png(
    fig: plt.Figure,
    path: str | Path,
    dpi: int = 300,
) -> None:
    """
    Save the current figure as a PNG file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    logger.info(f"Figure saved as {path}")


# -------------------------------------------------
# Save Figure as PDF
# -------------------------------------------------
def save_fig_as_pdf(
    fig: plt.Figure,
    path: str | Path,
    dpi: int = 300,
) -> None:
    """
    Save the current figure as a PDF file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    logger.info(f"Figure saved as {path}")


# -------------------------------------------------
# Save Growth Results to CSV
# -------------------------------------------------
def save_growth_results_summary(
    results: List[GrowthResult],
    output_path: Path,
) -> None:
    """
    Save a summary CSV of growth simulation results.
    One row per time step.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "time_min",
            "target_coverage_pct",
            "initial_simulated_coverage_pct",
            "final_simulated_coverage_pct",
            "top_to_bottom",
            "left_to_right",
            "percolates",
        ])

        # Rows
        for r in results:
            writer.writerow([
                r.time_min,
                r.target_coverage_pct,
                r.initial_simulated_coverage_pct,
                r.final_simulated_coverage_pct,
                r.top_to_bottom,
                r.left_to_right,
                r.top_to_bottom or r.left_to_right,
            ])
# utils/save_files.py

from __future__ import annotations

import logging
from pathlib import Path
import matplotlib.pyplot as plt
from utils.config_logger import setup_logging

setup_logging()
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

# utils/config_logger.py

from __future__ import annotations

import sys
import logging
from pathlib import Path
from datetime import datetime
from config.settings import PROJECT_ROOT


# -------------------------------------------------
# Setup Logging
# -------------------------------------------------
def setup_logging(
    level: int = logging.INFO,
    log_to_file: bool = True,
) -> None:
    """
    Setup logging for the application.
    """

    logger = logging.getLogger()
    logger.setLevel(level)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ---- Console handler ----
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ---- File handler ----
    if log_to_file:
        logs_dir = Path(PROJECT_ROOT) / "logs"
        logs_dir.mkdir(exist_ok=True)

        log_file = (
            logs_dir / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

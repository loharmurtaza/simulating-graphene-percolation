# utils/io.py

from __future__ import annotations

import logging
import pandas as pd
from utils.config_logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


# -------------------------------------------------
# Read Experimental Raw Data
# -------------------------------------------------
def load_experimental_raw_data(
    raw_data_path: str,
) -> pd.DataFrame:
    """
    Load experimental raw data from CSV file.
    Returns:
        t_data (list[float]): Time data
        S_data (list[float]): Surface coverage data
        std_data (list[float]): Standard deviation data
    """
    logger.info(f"Loading experimental raw data from {raw_data_path}")
    df = pd.read_csv(raw_data_path)

    if not df.empty:
        logger.info("Experimental raw data loaded successfully")
        return (
            df['data_point (in min)'].astype(float).values,
            df['surface_coverage (in %)'].astype(float).values,
            df['standard_deviation (in %)'].astype(float).values,
        )
    else:
        logger.error(
            f"Experimental raw data file {raw_data_path} is empty",
        )
        raise ValueError(
            f"Experimental raw data file {raw_data_path} is empty",
        )

# utils/io.py

from __future__ import annotations

import pandas as pd


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
    df = pd.read_csv(raw_data_path)

    if not df.empty:
        return (
            df['data_point (in min)'].astype(float).values,
            df['surface_coverage (in %)'].astype(float).values,
            df['standard_deviation (in %)'].astype(float).values,
        )
    else:
        raise ValueError(
            f"Experimental raw data file {raw_data_path} is empty",
        )

# config/settings.py

from __future__ import annotations

import os
from dataclasses import dataclass, field


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def get_int(name: str) -> int:
    v = os.getenv(name)
    return int(v)


def get_float(name: str) -> float:
    v = os.getenv(name)
    return float(v)


def get_str(name: str) -> str:
    v = os.getenv(name)
    return v


def get_bool(name: str) -> bool:
    v = os.getenv(name).strip().lower()
    return v in {"1", "true", "yes", "y"}


# -------------------------------------------------
# Settings
# -------------------------------------------------
PROJECT_ROOT = get_str('PROJECT_ROOT')
DATA_DIR = get_str('DATA_DIR')
RAW_DIR = get_str('RAW_DIR')
PROCESSED_DIR = get_str('PROCESSED_DIR')
OUTPUT_DIR = get_str('OUTPUT_DIR')


# -------------------------------------------------
# Configurations
# -------------------------------------------------
@dataclass
class SurfaceCoverageConfig:
    raw_data_path: str = field(
        default_factory=lambda: get_str('EXPERIMENTAL_RAW_PATH'),
    )
    grid_size_microns: int = field(
        default_factory=lambda: get_int('GRID_SIZE_MICRONS'),
    )
    num_circles: int = field(
        default_factory=lambda: get_int('NUM_CIRCLES'),
    )
    initial_radius_microns: float = field(
        default_factory=lambda: get_float('INITIAL_RADIUS_MICRONS'),
    )
    radius_microns: float = field(
        default_factory=lambda: get_float('RADIUS_MICRONS'),
    )
    random_seed: int = field(
        default_factory=lambda: get_int('RANDOM_SEED'),
    )
    mesh_points: int = field(
        default_factory=lambda: get_int('MESH_POINTS'),
    )
    use_std: bool = field(
        default_factory=lambda: get_bool('USE_STD'),
    )
    show_plots: bool = field(
        default_factory=lambda: get_bool('SHOW_PLOTS'),
    )


@dataclass
class SimulationsConfig:
    simulations_to_run: int = field(
        default_factory=lambda: get_int('SIMULATIONS_TO_RUN'),
    )

@dataclass
class FinalResultsConfig:
    percolations_csv_name: str = field(
        default_factory=lambda: get_str('PERCOLATIONS_CSV_NAME'),
    )
    output_figure_name: str = field(
        default_factory=lambda: get_str('OUTPUT_FIGURE_NAME'),
    )

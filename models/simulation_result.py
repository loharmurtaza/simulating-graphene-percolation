# models/simulation_result.py

from __future__ import annotations

from typing import Optional
from dataclasses import dataclass


# -------------------------------
# SimulationResult container
# -------------------------------
@dataclass
class SimulationResult:
    simulation_id: int
    seed_used: int
    percolated: bool
    percolation_time_min: Optional[float]
    percolation_target_coverage_pct: Optional[float]
    percolation_final_coverage_pct: Optional[float]
    top_to_bottom: bool
    left_to_right: bool
    steps_simulated: int
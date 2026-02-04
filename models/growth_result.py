# models/growth_result.py

from __future__ import annotations

from dataclasses import dataclass


# -------------------------------------------------
# Growth Result
# -------------------------------------------------
@dataclass
class GrowthResult:
    # Time information
    time_min: float

    # Coverage values (percent)
    target_coverage_pct: float                  # from logistic fit
    initial_simulated_coverage_pct: float       # before correction
    final_simulated_coverage_pct: float         # after correction

    # Percolation results
    top_to_bottom: bool
    left_to_right: bool
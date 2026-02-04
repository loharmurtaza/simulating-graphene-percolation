# utils/math.py

from __future__ import annotations

import logging
import numpy as np
from tqdm import tqdm
from utils.seeding import set_seed
import matplotlib.patches as patches
from scipy.optimize import curve_fit
from typing import Iterable, List, Tuple
from shapely.geometry import LineString, Point

logger = logging.getLogger(__name__)


# -------------------------------------------------
# Logistic Curve
# -------------------------------------------------
def logistic(
    t: np.ndarray,
    L: float,
    k: float,
    t0: float,
) -> np.ndarray:
    """
    Standard logistic curve.
    """
    return L / (1 + np.exp(-k * (t - t0)))


# -------------------------------------------------
# Derivative of the Logistic Curve
# -------------------------------------------------
def logistic_derivative(
    t: np.ndarray,
    L: float,
    k: float,
    t0: float,
) -> np.ndarray:
    """
    Derivative of the logistic curve.
    """
    return L * k * np.exp(-k * (t - t0)) / (1 + np.exp(-k * (t - t0)))**2


# -------------------------------------------------
# Surface Coverage Model
# -------------------------------------------------
def fit_surface_coverage_logistic(
    t_data: np.ndarray,
    S_data: np.ndarray,
    std_data: np.ndarray = None,
    p0: Tuple[float, float, float] = (100, 0.1, 5.0),
) -> Tuple[float, float, float]:
    """
    Fit logistic model to (time, coverage%) observations.
    """
    if std_data is not None:
        logger.info(
            "Fitting surface coverage logistic model with standard deviation",
        )
        popt, pcov = curve_fit(
            logistic, t_data, S_data, p0=list(p0),
            sigma=std_data, absolute_sigma=True,
        )
        logger.info(
            "Fitted surface coverage logistic model with standard deviation",
        )
    else:
        logger.info(
            "Fitting surface coverage logistic model without standard"
            " deviation",
        )
        popt, pcov = curve_fit(logistic, t_data, S_data, p0=list(p0))
        logger.info(
            "Fitted surface coverage logistic model without standard"
            " deviation",
        )
    return (float(popt[0]), float(popt[1]), float(popt[2])), pcov


# -------------------------------------------------
# Estimate Mean Areas from Coverage
# -------------------------------------------------
def estimate_mean_areas_from_coverage(
    coverage_data: np.ndarray,
    mean_area_data: np.ndarray,
    S_data: np.ndarray,
) -> np.ndarray:
    """
    Linear extrapolation of mean flake area given coverage.
    """
    logger.info("Estimating mean areas from coverage")
    m, b = np.polyfit(coverage_data, mean_area_data, 1)
    logger.info(f"Estimated mean areas from coverage: m={m}, b={b}")
    return m * S_data + b


# -------------------------------------------------
# Two Points Distance
# -------------------------------------------------
def two_points_distance(
    point_one: Iterable[float],
    point_two: Iterable[float],
) -> float:
    """
    Distance between two points: must be between 5 and 140 microns.
    """
    p1 = np.array(list(point_one), dtype=float)
    p2 = np.array(list(point_two), dtype=float)
    d = float(np.linalg.norm(p1 - p2))
    if (d > 5.0) and (d < 140.0):
        return d
    return None


# -------------------------------------------------
# Random Points
# -------------------------------------------------
def random_points(
    num_circles: int,
    surface_dim: float,
    random_seed: int = 10,
) -> List[List[int]]:
    """
    Randomly distribute circle centers with distance constraints.
    """
    logger.info(
        f"Generating random points: num_circles={num_circles}, "
        f"surface_dim={surface_dim}, random_seed={random_seed}",
    )
    set_seed(random_seed)

    points: List[List[int]] = []
    for _ in tqdm(range(num_circles), desc="Generating center points"):
        while True:
            x = int(np.random.randint(0, surface_dim))
            y = int(np.random.randint(0, surface_dim))
            invalid = False
            for px, py in points:
                if two_points_distance([x, y], [px, py]) is None:
                    invalid = True
                    break
            if not invalid:
                points.append([x, y])
                break
    logger.info(f"Generated {len(points)} points")
    return points


# -------------------------------------------------
# Plot Circles
# -------------------------------------------------
def build_initial_circles(
    points: List[List[int]],
    radius: float = 0.1,
) -> List[patches.Circle]:
    """
    Build initial circles from center points.
    """
    logger.info(
        f"Building initial circles with total points={len(points)} and "
        f"initial radius={radius}",
    )
    circles: List[patches.Circle] = []
    for x, y in points:
        circles.append(
            patches.Circle(
                (x, y), radius=radius, fill=True, edgecolor='green',
            )
        )
    logger.info(f"Initial circles built: {len(circles)} circles")
    return circles


# -------------------------------------------------
# Circle Touches Line
# -------------------------------------------------
def circle_touches_line(
    circle: patches.Circle,
    surface_dim: int,
    which_line: str,
) -> bool:
    """
    Check if a circle touches a line.
    """
    if which_line == 'bottom':
        line = LineString([(0, surface_dim), (surface_dim, surface_dim)])
    elif which_line == 'top':
        line = LineString([(0, 0), (surface_dim, 0)])
    elif which_line == 'left':
        line = LineString([(0, 0), (0, surface_dim)])
    elif which_line == 'right':
        line = LineString([(surface_dim, 0), (surface_dim, surface_dim)])
    else:
        raise ValueError(
            f"Invalid line: {which_line} must be"
            "'top', 'bottom', 'left', or 'right'",
        )

    circle_point = Point(circle.center)
    distance_to_line = circle_point.distance(line)
    return distance_to_line <= circle.radius


# -------------------------------------------------
# Two Circles Touching
# -------------------------------------------------
def two_circles_touching(
    circle_one: patches.Circle,
    circle_two: patches.Circle,
    tolerance: float = 0.01,
) -> bool:
    """
    Check if a circle touches another circle.
    """
    d = np.sqrt(
        (circle_one.center[0] - circle_two.center[0])**2 +
        (circle_one.center[1] - circle_two.center[1])**2,
    )
    return d <= (circle_one.radius + circle_two.radius + tolerance)

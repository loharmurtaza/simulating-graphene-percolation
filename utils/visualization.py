# utils/visualization.py

from __future__ import annotations

import logging
from typing import List, Dict, Tuple
import matplotlib.patches as patches
from utils.config_logger import setup_logging
from utils.math import circle_touches_line, two_circles_touching

setup_logging()
logger = logging.getLogger(__name__)


# -------------------------------------------------
# Generate a graph of the circles on the surface.
# -------------------------------------------------
def generate_graph(
    circles: List[patches.Circle],
    surface_dim: int,
) -> Tuple[
    Dict[int, List[int]],
    Dict[int, bool],
    Dict[int, bool],
    Dict[int, bool],
    Dict[int, bool],
]:
    """
    Generate a graph of the circles on the surface.
    """
    logger.info(
        f"Generating graph: circles={circles}, surface_dim={surface_dim}",
    )
    graph: Dict[int, List[int]] = {}
    top: Dict[int, bool] = {}
    bottom: Dict[int, bool] = {}
    left: Dict[int, bool] = {}
    right: Dict[int, bool] = {}

    for i, circle in enumerate(circles):
        if circle_touches_line(circle, surface_dim, 'top'):
            top[i] = True
            logger.info(f"Circle {i} touches top line")
        if circle_touches_line(circle, surface_dim, 'bottom'):
            bottom[i] = True
            logger.info(f"Circle {i} touches bottom line")
        if circle_touches_line(circle, surface_dim, 'left'):
            left[i] = True
            logger.info(f"Circle {i} touches left line")
        if circle_touches_line(circle, surface_dim, 'right'):
            right[i] = True
            logger.info(f"Circle {i} touches right line")

        neighbors: List[int] = []
        for j, other in enumerate(circles):
            if i == j:
                continue
            if two_circles_touching(circle, other):
                neighbors.append(j)
                logger.info(f"Circle {i} touches circle {j}")
        graph[i] = neighbors

    logger.info(f"Graph generated: {graph}")
    return graph, top, bottom, left, right

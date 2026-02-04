# utils/visualization.py

from __future__ import annotations

import logging
from typing import List, Dict, Tuple
import matplotlib.patches as patches
from utils.math import circle_touches_line, two_circles_touching

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
    graph: Dict[int, List[int]] = {}
    top: Dict[int, bool] = {}
    bottom: Dict[int, bool] = {}
    left: Dict[int, bool] = {}
    right: Dict[int, bool] = {}

    for i, circle in enumerate(circles):
        if circle_touches_line(circle, surface_dim, 'top'):
            top[i] = True
        if circle_touches_line(circle, surface_dim, 'bottom'):
            bottom[i] = True
        if circle_touches_line(circle, surface_dim, 'left'):
            left[i] = True
        if circle_touches_line(circle, surface_dim, 'right'):
            right[i] = True

        neighbors: List[int] = []
        for j, other in enumerate(circles):
            if i == j:
                continue
            if two_circles_touching(circle, other):
                neighbors.append(j)
        graph[i] = neighbors

    logger.info("Graph generated with the following boundaries:")
    logger.info(f"- Top: {len(top)} circles touching the top boundary.")
    logger.info(f"- Bottom: {len(bottom)} circles touching the bottom boundary.")
    logger.info(f"- Left: {len(left)} circles touching the left boundary.")
    logger.info(f"- Right: {len(right)} circles touching the right boundary.")
    return graph, top, bottom, left, right

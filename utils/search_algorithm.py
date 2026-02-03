# utils/search_algorithm.py

from __future__ import annotations

import logging
from collections import deque
from typing import Iterable, List, Dict, Tuple
from utils.config_logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


# -------------------------------------------------
# Breadth-First Search
# -------------------------------------------------
def breadth_first_search(
    graph: Dict[int, List[int]],
    start_node: int,
    target_nodes: Iterable[int],
) -> Tuple[List[int], bool]:
    """
    Search for the target nodes from the start node using breadth-first search.
    """
    logger.info(
        f"Breadth-first search: graph={graph}, start_node={start_node},"
        f"target_nodes={target_nodes}",
    )
    target_set = set(target_nodes)
    visited = set([start_node])
    q = deque([start_node])
    path: List[int] = []

    while q:
        node = q.popleft()
        path.append(node)
        for nb in graph[node]:
            if nb in visited:
                logger.info(f"Node already visited: {nb}")
                continue
            visited.add(nb)
            q.append(nb)
            if nb in target_set:
                path.append(nb)
                logger.info(f"Target node found: {nb}")
                return path, True
    logger.info("No target nodes found")
    return path, False

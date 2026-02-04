# utils/search_algorithm.py

from __future__ import annotations

import logging
from collections import deque
from typing import Iterable, List, Dict, Tuple

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
    target_set = set(target_nodes)
    visited = set([start_node])
    q = deque([start_node])
    path: List[int] = []

    while q:
        node = q.popleft()
        path.append(node)
        for nb in graph[node]:
            if nb in visited:
                continue
            visited.add(nb)
            q.append(nb)
            if nb in target_set:
                path.append(nb)
                return path, True
    return path, False

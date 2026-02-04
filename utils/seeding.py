# utils/seeding.py

from __future__ import annotations

import logging
import random
import numpy as np

logger = logging.getLogger(__name__)


# -------------------------------------------------
# Set Seed
# -------------------------------------------------
def set_seed(seed: int) -> None:
    """
    Set the seed for the random number generator.
    """
    logger.info(f"Setting seed: {seed}")
    random.seed(seed)
    np.random.seed(seed)
    logger.info(f"Seed set: {seed}")

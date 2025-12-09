"""
Date-based filtering for search results.
"""

import logging
from typing import List

from ..core.models import Result


logger = logging.getLogger(__name__)


def filter_by_date(results: List[Result], min_year: int) -> List[Result]:
    """
    Filter results by minimum publication year.
    
    Args:
        results: List of Result objects
        min_year: Minimum year to include
        
    Returns:
        Filtered list of results
    """
    filtered = []
    for r in results:
        if r.published_date:
            try:
                year = int(r.published_date)
                if year >= min_year:
                    filtered.append(r)
                else:
                    logger.debug(f"Filtered out (old): {r.title}")
            except ValueError:
                # Keep if can't parse year
                filtered.append(r)
        else:
            # Keep if no date available
            filtered.append(r)
    
    return filtered

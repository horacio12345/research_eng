"""
Keyword-based filtering for search results.
"""

import logging
from typing import List

from ..core.models import Result


logger = logging.getLogger(__name__)


def filter_by_keywords(results: List[Result], required_keywords: List[str]) -> List[Result]:
    """
    Filter results that contain at least one required keyword.
    
    Args:
        results: List of Result objects
        required_keywords: List of keywords to check for
        
    Returns:
        Filtered list of results
    """
    if not required_keywords:
        return results
    
    filtered = []
    for result in results:
        text = (result.title + ' ' + result.snippet).lower()
        if any(keyword.lower() in text for keyword in required_keywords):
            filtered.append(result)
        else:
            logger.debug(f"Filtered by keywords: {result.title}")
    
    return filtered

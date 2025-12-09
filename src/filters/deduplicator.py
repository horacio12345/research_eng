"""
Deduplication of search results.
"""

import hashlib
import logging
import re
from typing import List

from ..core.models import Result


logger = logging.getLogger(__name__)


def deduplicate_results(results: List[Result]) -> List[Result]:
    """
    Remove duplicate results based on URL and title similarity.
    
    Args:
        results: List of Result objects
        
    Returns:
        Deduplicated list of results
    """
    seen_urls = set()
    seen_title_hashes = set()
    unique_results = []
    
    for result in results:
        # Check URL
        if result.url in seen_urls:
            logger.debug(f"Duplicate URL: {result.url}")
            continue
        
        # Check title similarity (simple hash-based approach)
        title_normalized = re.sub(r'\W+', '', result.title.lower())
        title_hash = hashlib.md5(title_normalized.encode()).hexdigest()
        
        if title_hash in seen_title_hashes:
            logger.debug(f"Duplicate title: {result.title}")
            continue
        
        seen_urls.add(result.url)
        seen_title_hashes.add(title_hash)
        unique_results.append(result)
    
    logger.info(f"Deduplication: {len(results)} -> {len(unique_results)} results")
    return unique_results

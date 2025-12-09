"""
Query generation for search topics.
"""

import logging
from datetime import datetime
from typing import List

from ..core.models import Topic


logger = logging.getLogger(__name__)


def build_queries_for_topic(topic: Topic, min_year: int = 2024) -> List[str]:
    """
    Build search queries for a given topic.
    
    Args:
        topic: Topic object with keywords and search variations
        min_year: Minimum year to include in queries
        
    Returns:
        List of search query strings
    """
    current_year = datetime.now().year
    queries = []
    
    # Use predefined search variations if available
    if topic.search_variations:
        queries.extend(topic.search_variations)
    
    # DISABLED: Automatic query generation (wastes money on redundant searches)
    # if topic.keywords:
    #     base_keywords = ' '.join([f'"{kw}"' for kw in topic.keywords[:3]])
    #     queries.append(f'{current_year} {base_keywords} pdf')
    #     queries.append(f'{base_keywords} {min_year} {current_year}')
    #     queries.append(f'{base_keywords} research {min_year}')
    
    logger.debug(f"Generated {len(queries)} queries for topic '{topic.name}'")
    return queries

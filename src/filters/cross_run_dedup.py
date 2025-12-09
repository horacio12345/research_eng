"""
Cross-run deduplication utility.
Checks previous JSON outputs to avoid re-processing duplicate URLs.
"""

import json
import logging
from pathlib import Path
from typing import List, Set

from ..core.models import Result


logger = logging.getLogger(__name__)


def load_previous_urls(output_dir: str = "outputs") -> Set[str]:
    """
    Load URLs from all previous JSON outputs.
    
    Returns:
        Set of URLs that have been processed before
    """
    outputs_path = Path(output_dir)
    if not outputs_path.exists():
        return set()
    
    seen_urls = set()
    
    for json_file in outputs_path.glob("research_data_*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                for topic_results in data.get('topics', {}).values():
                    for result in topic_results:
                        if 'url' in result:
                            seen_urls.add(result['url'])
        except Exception as e:
            logger.warning(f"Could not load {json_file}: {e}")
    
    logger.info(f"Loaded {len(seen_urls)} URLs from previous runs")
    return seen_urls


def filter_seen_urls(results: List[Result], seen_urls: Set[str]) -> List[Result]:
    """
    Remove results that have been processed in previous runs.
    
    Args:
        results: List of Result objects
        seen_urls: Set of URLs from previous runs
        
    Returns:
        Filtered list without previously seen URLs
    """
    if not seen_urls:
        return results
    
    filtered = [r for r in results if r.url not in seen_urls]
    removed = len(results) - len(filtered)
    
    if removed > 0:
        logger.info(f"Removed {removed} duplicate URLs from previous runs")
    
    return filtered

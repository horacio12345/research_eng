"""
Tavily search API integration.
"""

import os
import logging
import re
import urllib.parse
from typing import List, Optional

import requests

from ..core.models import Result


logger = logging.getLogger(__name__)


def tavily_search(
    query: str,
    max_results: int = 10,
    search_depth: str = "basic",
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None
) -> List[Result]:
    """
    Execute a search using the Tavily API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        search_depth: "basic" or "advanced"
        include_domains: Optional list of domains to include
        exclude_domains: Optional list of domains to exclude
        
    Returns:
        List of Result objects
    """
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        logger.error("TAVILY_API_KEY not found in environment variables")
        raise ValueError("TAVILY_API_KEY must be set in environment")
    
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": False,
        "include_raw_content": False
    }
    
    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains
    
    logger.info(f"Executing Tavily search: '{query}'")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            # Extract domain from URL
            domain = extract_domain(item.get('url', ''))
            
            # Extract year from content if available
            published_date = extract_year_from_content(
                item.get('title', '') + ' ' + item.get('content', '')
            )
            
            result = Result(
                title=item.get('title', 'No title'),
                url=item.get('url', ''),
                snippet=item.get('content', '')[:500],  # Limit snippet length
                published_date=published_date,
                domain=domain
            )
            results.append(result)
        
        logger.info(f"Found {len(results)} results for query")
        return results
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily API request failed: {e}")
        return []


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc


def extract_year_from_content(text: str) -> Optional[str]:
    """Extract year from text content (looks for 2020-2025 range)."""
    pattern = r'\b(202[0-5])\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else None

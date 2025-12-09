"""
Core data models for the research automation tool.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Result:
    """Represents a single search result."""
    title: str
    url: str
    snippet: str
    published_date: Optional[str] = None
    domain: Optional[str] = None
    relevance_score: float = 0.0
    ai_summary: Optional[str] = None


@dataclass
class Topic:
    """Represents a search topic with its configuration."""
    name: str
    keywords: List[str]
    search_variations: List[str]


@dataclass
class SearchConfig:
    """Configuration for the search and filtering process."""
    topics: List[Topic]
    search_depth: str
    max_results_per_query: int
    min_year: int
    top_n_results: int
    output_dir: str
    include_domains: List[str]
    exclude_domains: List[str]
    required_keywords: List[str]
    ai_model: str
    ai_temperature: float
    use_ai_filtering: bool

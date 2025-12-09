"""
Configuration loading and validation.
"""

import logging
from typing import List
import yaml

from .models import Topic, SearchConfig


logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> SearchConfig:
    """
    Load and parse configuration from YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        SearchConfig object with validated configuration
    """
    logger.info(f"Loading configuration from {config_path}")
    
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Parse topics - support both old 'topics' and new 'topic_clusters' format
    topics = []
    
    if 'topic_clusters' in config_data:
        # New format with clusters
        for cluster in config_data['topic_clusters']:
            topics.append(Topic(
                name=cluster.get('cluster_name', cluster.get('name', 'Unnamed')),
                keywords=cluster.get('keywords', []),
                search_variations=cluster.get('search_queries', cluster.get('search_variations', []))
            ))
    elif 'topics' in config_data:
        # Old format (backward compatibility)
        for t in config_data['topics']:
            topics.append(Topic(
                name=t['name'],
                keywords=t.get('keywords', []),
                search_variations=t.get('search_variations', [])
            ))
    else:
        raise ValueError("No 'topics' or 'topic_clusters' found in config.yaml")
    
    # Extract search configuration (support nested structure)
    tavily_config = config_data.get('tavily', {})
    
    # Handle domain configuration
    domains_config = config_data.get('domains', {})
    if domains_config:
        # New nested domain structure
        include_domains = domains_config.get('tier1_priority', []) + domains_config.get('tier2_include', [])
        exclude_domains = domains_config.get('exclude', [])
    else:
        # Old flat structure
        include_domains = tavily_config.get('include_domains', [])
        exclude_domains = tavily_config.get('exclude_domains', [])
    
    filtering = config_data.get('filtering', {})
    output_config = config_data.get('output', {})
    ai_config = config_data.get('ai', {})
    
    # Handle output directory configuration
    if isinstance(output_config, dict) and 'directory' in output_config:
        output_dir = output_config['directory']
    else:
        output_dir = 'outputs'
    
    # Handle filtering configuration
    if 'date_range' in filtering:
        min_year = int(filtering['date_range'].get('min_date', '2024-01-01')[:4])
    else:
        min_year = filtering.get('min_year', 2024)
    
    if 'output_limits' in filtering:
        top_n = filtering['output_limits'].get('top_n_per_cluster', 10)
    else:
        top_n = filtering.get('top_n_per_topic', 15)
    
    return SearchConfig(
        topics=topics,
        search_depth=tavily_config.get('search_depth', 'basic'),
        max_results_per_query=tavily_config.get('max_results', 10),
        min_year=min_year,
        top_n_results=top_n,
        output_dir=output_dir,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        required_keywords=filtering.get('required_keywords', filtering.get('content_requirements', {}).get('must_contain_one_of', [])),
        ai_model=ai_config.get('primary_model', 'gpt-4o-mini'),
        ai_temperature=ai_config.get('temperature', 0.3),
        use_ai_filtering=ai_config.get('use_ai_filtering', True)
    )

#!/usr/bin/env python3
"""
Research Automation Tool - Main Orchestrator

A modular, maintainable tool for searching and filtering research on generative AI
in engineering projects. Refactored for clarity and extensibility.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

from src.core.config import load_config
from src.search.query_builder import build_queries_for_topic
from src.search.tavily_client import tavily_search
from src.filters.ranking import rank_and_filter_results
from src.output.markdown_generator import to_markdown_report
from src.output.json_generator import to_json_file
from src.ui.browser_view import generate_browser_view


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main(config_path: str = "config.yaml") -> None:
    """
    Main execution function.
    
    Args:
        config_path: Path to configuration file
    """
    # Load environment variables
    load_dotenv()
    
    # Verify API keys
    required_keys = ['TAVILY_API_KEY', 'OPENAI_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
    
    # Load configuration
    config = load_config(config_path)
    
    # Create output directory
    output_dir = Path(config.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Process each topic
    results_by_topic = {}
    
    for topic in config.topics:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing topic: {topic.name}")
        logger.info(f"{'='*60}")
        
        # Build queries
        queries = build_queries_for_topic(topic, config.min_year)
        
        # Execute searches
        all_results = []
        for query in queries:
            results = tavily_search(
                query=query,
                max_results=config.max_results_per_query,
                search_depth=config.search_depth,
                include_domains=config.include_domains,
                exclude_domains=config.exclude_domains
            )
            all_results.extend(results)
        
        logger.info(f"Total results from all queries: {len(all_results)}")
        
        # Filter and rank
        filtered_results = rank_and_filter_results(
            all_results,
            config,
            topic,
            use_ai=config.use_ai_filtering
        )
        
        results_by_topic[topic.name] = filtered_results
    
    # Generate outputs
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    markdown_path = output_dir / f"research_report_{timestamp}.md"
    to_markdown_report(results_by_topic, config, str(markdown_path))
    
    json_path = output_dir / f"research_data_{timestamp}.json"
    to_json_file(results_by_topic, str(json_path))
    
    browser_path = output_dir / f"research_browser_{timestamp}.html"
    generate_browser_view(results_by_topic, str(browser_path))
    
    logger.info(f"\n{'='*60}")
    logger.info("✅ Research automation completed successfully!")
    logger.info(f"📄 Markdown report: {markdown_path}")
    logger.info(f"📊 JSON data: {json_path}")
    logger.info(f"🌐 Browser view: {browser_path}")
    logger.info(f"{'='*60}\n")


if __name__ == "__main__":
    main()

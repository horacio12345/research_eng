"""
Ranking and filtering orchestration.
"""

import logging
from typing import List

from langchain_openai import ChatOpenAI

from ..core.models import Result, SearchConfig, Topic
from ..ai.analyzer import analyze_result_with_ai, generate_summary_with_ai
from .date_filter import filter_by_date
from .deduplicator import deduplicate_results
from .keyword_filter import filter_by_keywords
from .cross_run_dedup import load_previous_urls, filter_seen_urls


logger = logging.getLogger(__name__)

# Load previous URLs once at module level
PREVIOUS_URLS = load_previous_urls()


def rank_and_filter_results(
    results: List[Result],
    config: SearchConfig,
    topic: Topic,
    use_ai: bool = True
) -> List[Result]:
    """
    Apply all filtering and ranking steps.
    
    Args:
        results: List of raw results
        config: SearchConfig object
        topic: Topic context for AI analysis
        use_ai: Whether to use AI for ranking
        
    Returns:
        Filtered and ranked list of results
    """
    logger.info(f"Starting with {len(results)} raw results")
    
    # Step 1: Filter by date
    results = filter_by_date(results, config.min_year)
    logger.info(f"After date filter: {len(results)} results")
    
    # Step 2: Remove duplicates within this run
    results = deduplicate_results(results)
    
    # Step 3: Remove URLs seen in previous runs
    results = filter_seen_urls(results, PREVIOUS_URLS)
    
    # Step 4: Filter by required keywords
    results = filter_by_keywords(results, config.required_keywords)
    logger.info(f"After keyword filter: {len(results)} results")
    
    # Step 5: AI-powered analysis and ranking
    if use_ai and config.use_ai_filtering and results:
        logger.info("Analyzing results with AI...")
        llm = ChatOpenAI(model=config.ai_model, temperature=config.ai_temperature)
        
        for result in results:
            # Analyze relevance
            analysis = analyze_result_with_ai(result, topic, llm)
            result.relevance_score = analysis['relevance_score']
            
            # DISABLED: Summary generation to save tokens (50% reduction)
            # result.ai_summary = generate_summary_with_ai(result, llm)
        
        # Filter by AI relevance (keep score >= 0.6)
        results = [r for r in results if r.relevance_score >= 0.6]
        logger.info(f"After AI filtering: {len(results)} results")
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x.relevance_score, reverse=True)
    else:
        # Simple sorting by date if available
        results.sort(
            key=lambda x: x.published_date if x.published_date else '0000',
            reverse=True
        )
    
    # Step 6: Limit to top N
    results = results[:config.top_n_results]
    logger.info(f"Final result count: {len(results)}")
    
    return results


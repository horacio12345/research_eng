"""
AI-powered analysis and summarization using LangChain.
"""

import json
import logging
from typing import Dict, Any

from ..core.models import Result, Topic
from .prompt_loader import load_prompt


logger = logging.getLogger(__name__)


def analyze_result_with_ai(result: Result, topic: Topic, llm: Any) -> Dict[str, Any]:
    """
    Use AI to analyze a search result for relevance and quality.
    
    Args:
        result: Result object to analyze
        topic: Topic context for relevance assessment
        llm: LangChain LLM instance
        
    Returns:
        Dictionary with relevance_score, is_relevant, and reasoning
    """
    # Load prompt from external file
    prompt = load_prompt("relevance_analysis")
    
    messages = prompt.format_messages(
        topic_name=topic.name,
        keywords=", ".join(topic.keywords),
        title=result.title,
        url=result.url,
        snippet=result.snippet[:300]
    )
    
    try:
        response = llm.invoke(messages)
        # Parse JSON from response
        parsed = json.loads(response.content.strip())
        
        # Convert relevance_score to float
        parsed['relevance_score'] = float(parsed['relevance_score'])
        
        return parsed
    except Exception as e:
        logger.warning(f"AI analysis failed for {result.url}: {e}")
        return {
            'relevance_score': 0.5,
            'is_relevant': True,
            'reasoning': 'AI analysis unavailable'
        }


def generate_summary_with_ai(result: Result, llm: Any) -> str:
    """
    Generate a concise 1-2 sentence summary using AI.
    
    Args:
        result: Result object to summarize
        llm: LangChain LLM instance
        
    Returns:
        Summary string
    """
    # Load prompt from external file
    prompt = load_prompt("summary_generation")
    
    messages = prompt.format_messages(
        title=result.title,
        snippet=result.snippet[:400]
    )
    
    try:
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        logger.warning(f"Summary generation failed: {e}")
        # Fallback to snippet
        return result.snippet[:200] + "..."

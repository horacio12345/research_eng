"""
Interactive browser-based viewer for search results.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import asdict

from ..core.models import Result


logger = logging.getLogger(__name__)


def generate_browser_view(
    results_by_topic: Dict[str, List[Result]],
    output_path: str
) -> None:
    """
    Generate an interactive HTML file for viewing search results.
    
    Args:
        results_by_topic: Dictionary mapping topic names to result lists
        output_path: Path to save the HTML file
    """
    logger.info(f"Generating browser view: {output_path}")
    
    # Load HTML template
    template_path = Path(__file__).parent / "templates" / "results.html"
    
    if not template_path.exists():
        logger.warning("Browser view template not found, skipping")
        return
    
    template = template_path.read_text(encoding='utf-8')
    
    # Convert results to JSON for embedding
    data = {
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "topics": {}
    }
    
    for topic_name, results in results_by_topic.items():
        data["topics"][topic_name] = [
            asdict(result) for result in results
        ]
    
    # Embed data in template
    html = template.replace(
        '/* DATA_PLACEHOLDER */',
        f'const DATA = {json.dumps(data, indent=2, ensure_ascii=False)};'
    )
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info("Browser view generated successfully")

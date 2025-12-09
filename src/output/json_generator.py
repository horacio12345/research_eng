"""
JSON data export.
"""

import json
import logging
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List

from ..core.models import Result


logger = logging.getLogger(__name__)


def to_json_file(
    results_by_topic: Dict[str, List[Result]],
    output_path: str
) -> None:
    """
    Generate a machine-friendly JSON file.
    
    Args:
        results_by_topic: Dictionary mapping topic names to result lists
        output_path: Path to save the JSON file
    """
    logger.info(f"Generating JSON output: {output_path}")
    
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "topics": {}
    }
    
    for topic_name, results in results_by_topic.items():
        output_data["topics"][topic_name] = [
            asdict(result) for result in results
        ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logger.info("JSON file generated successfully")

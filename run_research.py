#!/usr/bin/env python3
"""
Research Automation Tool - Launcher Script

This script launches the refactored research automation tool.
Run this from the project root directory.
"""

import os
from pathlib import Path
from datetime import datetime, timedelta


def cleanup_old_outputs(days_to_keep=30):
    """Delete output files older than specified days."""
    outputs_dir = Path(__file__).parent / "outputs"
    
    if not outputs_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for file in outputs_dir.glob("research_*"):
        if file.is_file():
            file_modified = datetime.fromtimestamp(file.stat().st_mtime)
            if file_modified < cutoff_date:
                file.unlink()
                deleted_count += 1
    
    if deleted_count > 0:
        print(f"🗑️  Cleaned up {deleted_count} old output file(s)")


if __name__ == "__main__":
    # Auto-cleanup files older than 30 days
    cleanup_old_outputs(days_to_keep=30)
    
    # Run the research tool
    from src.main import main
    main()

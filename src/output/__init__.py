"""Output generation module."""

from .markdown_generator import to_markdown_report
from .json_generator import to_json_file

__all__ = ['to_markdown_report', 'to_json_file']

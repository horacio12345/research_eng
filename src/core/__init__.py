"""Core module for data models and configuration."""

from .models import Result, Topic, SearchConfig
from .config import load_config

__all__ = ['Result', 'Topic', 'SearchConfig', 'load_config']

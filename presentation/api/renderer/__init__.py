"""
Deterministic HTML renderer for slide blueprints.

This module provides LLM-free HTML generation using Jinja2 templates.
"""

from .renderer import SlideRenderer, RendererError

__all__ = ["SlideRenderer", "RendererError"]

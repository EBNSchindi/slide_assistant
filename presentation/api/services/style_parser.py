import os
import re
import sys
from typing import Dict, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import SimpleCache, get_logger

logger = get_logger(__name__)

# Global cache for style parsing (TTL: 5 minutes)
_style_cache = SimpleCache(ttl_seconds=300)


class StyleParser:
    """Parse CSS variables and design guides from project styles"""

    def __init__(self, project_path: str, use_cache: bool = True):
        self.project_path = project_path
        self.styles_path = os.path.join(project_path, "styles")
        self.use_cache = use_cache
        logger.debug(f"StyleParser initialized for: {project_path}")

    def parse_project_style(self) -> Dict:
        """Parse all style information from a project

        Uses caching to avoid repeated file system operations.
        Cache key is based on project path.
        """
        # Check cache first
        cache_key = f"style:{self.project_path}"
        if self.use_cache:
            cached_result = _style_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for style: {self.project_path}")
                return cached_result

        logger.debug(f"Parsing style for project: {self.project_path}")

        style_info = {
            "primary_color": "#238636",  # Default GitHub green
            "secondary_colors": [],
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "spacing_scale": [4, 8, 16, 24, 32, 48],
            "available_components": [
                "stat-grid",
                "bullet-list",
                "quote",
                "heading",
                "paragraph",
            ],
            "design_guide": "",
        }

        # Try to find and parse variables.css files
        variables_file = self._find_variables_css()
        if variables_file:
            colors = self._parse_css_variables(variables_file)
            style_info.update(colors)

        # Try to find and parse design-guide.md
        design_guide_file = self._find_design_guide()
        if design_guide_file:
            style_info["design_guide"] = self._read_design_guide(design_guide_file)

        # Cache the result
        if self.use_cache:
            _style_cache.set(cache_key, style_info)
            logger.debug(f"Cached style for: {self.project_path}")

        return style_info

    def _find_variables_css(self) -> Optional[str]:
        """Find variables.css in project styles"""
        for root, dirs, files in os.walk(self.styles_path):
            if "variables.css" in files:
                return os.path.join(root, "variables.css")
        return None

    def _find_design_guide(self) -> Optional[str]:
        """Find design-guide.md in project styles"""
        for root, dirs, files in os.walk(self.styles_path):
            if "design-guide.md" in files:
                return os.path.join(root, "design-guide.md")
        return None

    def _parse_css_variables(self, css_file: str) -> Dict:
        """Extract CSS variables from variables.css"""
        result = {
            "primary_color": "#238636",
            "secondary_colors": [],
            "spacing_scale": [4, 8, 16, 24, 32, 48],
        }

        try:
            with open(css_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse color variables
            color_pattern = r"--(?:primary|secondary|color)-[\w-]+:\s*([#\w(),%\s]+);"
            colors = re.findall(color_pattern, content)
            if colors:
                result["primary_color"] = colors[0].strip()
                result["secondary_colors"] = [c.strip() for c in colors[1:]]

            # Parse spacing scale
            spacing_pattern = r"--spacing-?(?:xs|sm|base|md|lg|xl):\s*(\d+)px"
            spacings = re.findall(spacing_pattern, content)
            if spacings:
                result["spacing_scale"] = sorted([int(s) for s in spacings])

        except Exception as e:
            logger.error(f"Error parsing CSS file {css_file}: {e}")

        return result

    def _read_design_guide(self, guide_file: str) -> str:
        """Read design guide markdown"""
        try:
            with open(guide_file, "r", encoding="utf-8") as f:
                content = f.read()
                logger.debug(f"Read design guide from: {guide_file}")
                return content
        except Exception as e:
            logger.error(f"Error reading design guide {guide_file}: {e}")
            return ""

    def get_component_recommendations(self, content_type: str) -> List[str]:
        """Recommend components based on content type"""
        recommendations = {
            "statistics": ["stat-grid", "bullet-list"],
            "narrative": ["heading", "paragraph", "bullet-list"],
            "quote": ["quote", "paragraph"],
            "list": ["bullet-list"],
            "mixed": ["heading", "paragraph", "bullet-list", "stat-grid"],
        }
        result = recommendations.get(content_type, ["paragraph", "bullet-list"])
        logger.debug(f"Component recommendations for '{content_type}': {result}")
        return result

    def clear_cache(self) -> None:
        """Clear the style cache for this project

        Useful when styles have been updated and need to be re-parsed.
        """
        cache_key = f"style:{self.project_path}"
        _style_cache.delete(cache_key)
        logger.info(f"Cleared style cache for: {self.project_path}")

    @staticmethod
    def clear_all_cache() -> None:
        """Clear all cached styles across all projects"""
        _style_cache.clear()
        logger.info("Cleared all style caches")

import os
import re
import json
from typing import Dict, List, Optional
from pathlib import Path


class StyleParser:
    """Parse CSS variables and design guides from project styles (JSON + Markdown fallback)"""

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.styles_path = os.path.join(project_path, "styles")

    def parse_project_style(self) -> Dict:
        """Parse all style information from a project (tries JSON first, falls back to Markdown)"""
        style_info = {
            "primary_color": "#238636",  # Default GitHub green
            "secondary_colors": ["#0366d6", "#d1130c"],
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "spacing_scale": [4, 8, 12, 16, 24, 32, 48],
            "available_components": [
                "stat-grid",
                "bullet-list",
                "quote",
                "text",
                "image",
                "image-grid",
                "pricing-table",
                "calculation-grid",
                "feature-grid",
                "process-chain-vertical",
                "process-chain-horizontal",
                "comparison-table",
                "financial-table",
            ],
            "design_guide": "",  # Full markdown will be loaded from file
            "components_schema": [],  # Component definitions from JSON
            "layouts": [],  # Layout patterns from JSON
        }

        # Priority 1: Try to load design-guide.json (NEW!)
        design_guide_json = self._find_design_guide_json()
        if design_guide_json:
            json_data = self._load_design_guide_json(design_guide_json)
            if json_data:
                # Extract tokens and components from JSON
                style_info.update(self._parse_json_tokens(json_data))
                style_info["components_schema"] = json_data.get("components", [])
                style_info["layouts"] = json_data.get("layouts", [])
                print(f"✅ Loaded design-guide.json with {len(style_info['components_schema'])} components")
                return style_info  # JSON loaded successfully, return early

        # Fallback 1: Try variables.css
        variables_file = self._find_variables_css()
        if variables_file:
            colors = self._parse_css_variables(variables_file)
            style_info.update(colors)

        # Fallback 2: Try design-guide.md
        design_guide_file = self._find_design_guide()
        if design_guide_file:
            style_info["design_guide"] = self._read_design_guide(design_guide_file)
            print("⚠️ Using Markdown design-guide.md (consider migrating to JSON)")

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
            print(f"Error parsing CSS: {e}")

        return result

    def _read_design_guide(self, guide_file: str) -> str:
        """Read design guide markdown"""
        try:
            with open(guide_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading design guide: {e}")
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
        return recommendations.get(content_type, ["paragraph", "bullet-list"])

    def _find_design_guide_json(self) -> Optional[str]:
        """Find design-guide.json in project styles (NEW - V2)"""
        for root, dirs, files in os.walk(self.styles_path):
            if "design-guide.json" in files:
                return os.path.join(root, "design-guide.json")
        return None

    def _load_design_guide_json(self, json_file: str) -> Optional[Dict]:
        """Load and parse design-guide.json (NEW - V2)"""
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"⚠️ Error loading design-guide.json: {e}")
            return None

    def _parse_json_tokens(self, json_data: Dict) -> Dict:
        """Extract tokens from design-guide.json and convert to legacy format (NEW - V2)"""
        result = {}

        tokens = json_data.get("tokens", {})

        # Extract colors
        colors = tokens.get("colors", {})
        if colors:
            primary = colors.get("primary", {})
            result["primary_color"] = primary.get("main", "#238636")

            # Collect secondary colors
            secondary_colors = []
            if "accent" in colors.get("semantic", {}):
                secondary_colors.append(colors["semantic"]["accent"].get("main", ""))
            result["secondary_colors"] = [c for c in secondary_colors if c]

        # Extract typography
        typography = tokens.get("typography", {})
        if typography:
            font_family = typography.get("fontFamily", {})
            result["font_family"] = font_family.get("default", "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif")

        # Extract spacing scale
        spacing = tokens.get("spacing", {})
        if spacing:
            # Convert spacing dict to sorted list (e.g., {"xs": "4px", "sm": "8px"} -> [4, 8, ...])
            spacing_values = []
            for key, value in spacing.items():
                # Extract number from "16px" -> 16
                match = re.match(r"(\d+)px", value)
                if match:
                    spacing_values.append(int(match.group(1)))
            result["spacing_scale"] = sorted(spacing_values) if spacing_values else [4, 8, 16, 24, 32, 48]

        # Extract available component IDs
        components = json_data.get("components", [])
        if components:
            result["available_components"] = [comp.get("id", "") for comp in components if comp.get("id")]

        return result

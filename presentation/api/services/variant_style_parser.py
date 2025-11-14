"""
Variant Style Parser - Parses variant_styles.md into structured data for agents
"""
import os
import re
from typing import Dict, List, Optional


class VariantStyleParser:
    """Parse variant style guide from variant_styles.md"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize parser

        Args:
            config_path: Path to api/config directory. If None, auto-detect.
        """
        if config_path is None:
            # Auto-detect: look for config/variant_styles.md relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            api_dir = os.path.dirname(current_dir)
            config_path = os.path.join(api_dir, "config")

        self.config_path = config_path
        self.variant_styles_file = os.path.join(config_path, "variant_styles.md")

    def parse_variant_profiles(self) -> List[Dict]:
        """
        Parse all variant profiles from the style guide

        Returns:
            List of profile dictionaries with structure:
            [
                {
                    "name": "corporate",
                    "character": "Professional, technical, trustworthy",
                    "primary_color": "#238636",
                    "visual_properties": {...},
                    "component_examples": {...}
                },
                ...
            ]
        """
        if not os.path.exists(self.variant_styles_file):
            print(f"Warning: variant_styles.md not found at {self.variant_styles_file}")
            return self._get_default_profiles()

        try:
            with open(self.variant_styles_file, "r", encoding="utf-8") as f:
                content = f.read()

            profiles = []

            # Parse Corporate Profile
            corporate = self._parse_profile_section(content, "Profile 1: Corporate")
            if corporate:
                corporate["name"] = "corporate"
                profiles.append(corporate)

            # Parse Modern Profile
            modern = self._parse_profile_section(content, "Profile 2: Modern")
            if modern:
                modern["name"] = "modern"
                profiles.append(modern)

            # Parse Minimal Profile
            minimal = self._parse_profile_section(content, "Profile 3: Minimal")
            if minimal:
                minimal["name"] = "minimal"
                profiles.append(minimal)

            return profiles if profiles else self._get_default_profiles()

        except Exception as e:
            print(f"Error parsing variant_styles.md: {e}")
            return self._get_default_profiles()

    def _parse_profile_section(self, content: str, profile_header: str) -> Optional[Dict]:
        """Parse a single profile section"""

        # Find the profile section
        pattern = rf"### {profile_header}.*?\n\n(.*?)(?=\n### Profile \d+:|---\n\n## Component-Specific|$)"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return None

        section = match.group(1)

        profile = {
            "character": "",
            "primary_color": "",
            "use_case": "",
            "visual_properties": {},
        }

        # Extract character
        char_match = re.search(r'\*\*Character\*\*:\s*(.+)', section)
        if char_match:
            profile["character"] = char_match.group(1).strip()

        # Extract primary color
        color_match = re.search(r'\*\*Primary Color\*\*:\s*`([^`]+)`', section)
        if color_match:
            profile["primary_color"] = color_match.group(1).strip()

        # Extract use case
        use_case_match = re.search(r'\*\*Use Case\*\*:\s*(.+)', section)
        if use_case_match:
            profile["use_case"] = use_case_match.group(1).strip()

        # Extract visual properties
        profile["visual_properties"] = self._parse_visual_properties(section)

        return profile

    def _parse_visual_properties(self, section: str) -> Dict:
        """Parse visual properties section"""
        properties = {
            "colors": {},
            "typography": {},
            "spacing": {},
            "borders_effects": {}
        }

        # Parse colors
        colors_match = re.search(r'- \*\*Colors\*\*:(.*?)(?=- \*\*Typography\*\*:|$)', section, re.DOTALL)
        if colors_match:
            colors_text = colors_match.group(1)
            properties["colors"] = self._extract_key_values(colors_text)

        # Parse typography
        typo_match = re.search(r'- \*\*Typography\*\*:(.*?)(?=- \*\*Spacing\*\*:|$)', section, re.DOTALL)
        if typo_match:
            typo_text = typo_match.group(1)
            properties["typography"] = self._extract_key_values(typo_text)

        # Parse spacing
        spacing_match = re.search(r'- \*\*Spacing\*\*:(.*?)(?=- \*\*Borders|$)', section, re.DOTALL)
        if spacing_match:
            spacing_text = spacing_match.group(1)
            properties["spacing"] = self._extract_key_values(spacing_text)

        # Parse borders & effects
        borders_match = re.search(r'- \*\*Borders & Effects\*\*:(.*?)$', section, re.DOTALL)
        if borders_match:
            borders_text = borders_match.group(1)
            properties["borders_effects"] = self._extract_key_values(borders_text)

        return properties

    def _extract_key_values(self, text: str) -> Dict:
        """Extract key-value pairs from bullet list"""
        result = {}

        # Pattern: - Key: `value`
        pattern = r'-\s+([^:]+):\s*`([^`]+)`'
        matches = re.findall(pattern, text)

        for key, value in matches:
            clean_key = key.strip().lower().replace(" ", "_")
            result[clean_key] = value.strip()

        return result

    def get_profile_by_name(self, profile_name: str) -> Optional[Dict]:
        """Get a specific profile by name"""
        profiles = self.parse_variant_profiles()
        for profile in profiles:
            if profile["name"] == profile_name.lower():
                return profile
        return None

    def get_all_profile_names(self) -> List[str]:
        """Get list of all available profile names"""
        profiles = self.parse_variant_profiles()
        return [p["name"] for p in profiles]

    def _get_default_profiles(self) -> List[Dict]:
        """Return default profiles if parsing fails"""
        return [
            {
                "name": "corporate",
                "character": "Professional, technical, trustworthy",
                "primary_color": "#238636",
                "use_case": "Enterprise presentations, technical documentation",
                "visual_properties": {
                    "colors": {
                        "primary": "#238636",
                        "text": "#1f2328",
                        "secondary_text": "#59636e",
                        "borders": "#d1d9e0",
                        "background_accent": "#f6f8fa"
                    },
                    "typography": {
                        "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                        "line_height": "1.5"
                    },
                    "spacing": {
                        "padding": "48px",
                        "gap": "40px"
                    },
                    "borders_effects": {
                        "border_width": "2px",
                        "border_radius": "3px",
                        "shadow": "0 1px 3px rgba(35, 134, 54, 0.12)"
                    }
                }
            },
            {
                "name": "modern",
                "character": "Contemporary, dynamic, innovative",
                "primary_color": "#0066cc",
                "use_case": "Startup presentations, product launches",
                "visual_properties": {
                    "colors": {
                        "primary": "#0066cc",
                        "text": "#1a1a1a",
                        "secondary_text": "#666666",
                        "borders": "#e0e0e0",
                        "background_accent": "#f5f7fa"
                    },
                    "typography": {
                        "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                        "line_height": "1.6"
                    },
                    "spacing": {
                        "padding": "48px",
                        "gap": "40px"
                    },
                    "borders_effects": {
                        "border_width": "1px",
                        "border_radius": "4px",
                        "shadow": "0 2px 8px rgba(0, 102, 204, 0.08)"
                    }
                }
            },
            {
                "name": "minimal",
                "character": "Clean, focused, elegant",
                "primary_color": "#666666",
                "use_case": "Minimalist presentations, design portfolios",
                "visual_properties": {
                    "colors": {
                        "primary": "#666666",
                        "text": "#000000",
                        "secondary_text": "#777777",
                        "borders": "#dddddd",
                        "background_accent": "#fafafa"
                    },
                    "typography": {
                        "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                        "line_height": "1.65"
                    },
                    "spacing": {
                        "padding": "48px",
                        "gap": "40px"
                    },
                    "borders_effects": {
                        "border_width": "1px",
                        "border_radius": "2px",
                        "shadow": "none"
                    }
                }
            }
        ]

    def get_variant_guide_summary(self) -> str:
        """
        Get a human-readable summary of all variants for agent prompts

        Returns:
            Formatted string describing all three variants
        """
        profiles = self.parse_variant_profiles()

        summary = "# Available Component Variant Profiles\n\n"

        for profile in profiles:
            summary += f"## {profile['name'].title()} Profile\n"
            summary += f"- **Character**: {profile.get('character', 'N/A')}\n"
            summary += f"- **Primary Color**: {profile.get('primary_color', 'N/A')}\n"
            summary += f"- **Use Case**: {profile.get('use_case', 'N/A')}\n"

            if "visual_properties" in profile:
                vp = profile["visual_properties"]
                if "colors" in vp and vp["colors"]:
                    summary += f"- **Key Colors**: {', '.join([f'{k}: {v}' for k, v in list(vp['colors'].items())[:3]])}\n"
                if "borders_effects" in vp and vp["borders_effects"]:
                    be = vp["borders_effects"]
                    if "border_width" in be:
                        summary += f"- **Border Width**: {be['border_width']}\n"
                    if "shadow" in be and be["shadow"] != "none":
                        summary += f"- **Uses Shadows**: Yes\n"
                    elif "shadow" in be:
                        summary += f"- **Uses Shadows**: No\n"

            summary += "\n"

        return summary

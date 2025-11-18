"""
Mock Agents (v2) - For testing without OpenAI API calls

Uses TEST_MODE to provide fixed outputs that match the new blueprint structure.
"""

import sys
import os
from typing import Dict, Any, List

# Support both relative and absolute imports
try:
    from ..schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent
except ImportError:
    # Fallback to absolute import if relative fails
    api_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)
    from schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent


class MockContentAnalyzerAgentV2:
    """Mock Content Analyzer that returns test ContentBlocks + SlideIntent"""

    def __init__(self, api_key: str = "mock", **kwargs):
        self.api_key = api_key

    def analyze(self, user_input: str) -> Dict[str, Any]:
        """Return mock analysis result"""
        return {
            "slide_intent": {
                "intent_type": "team",
                "primary_message": "Five-person expert team with deep robotics and AI background",
                "target_audience": "investor",
                "language": "de",
                "density": "medium",
            },
            "content_blocks": [
                {
                    "type": "title",
                    "content": "Unser Team",
                    "priority": "must_have",
                },
                {
                    "type": "statistic",
                    "content": "5 Experten",
                    "priority": "must_have",
                },
                {
                    "type": "statement",
                    "content": "20+ Jahre Erfahrung in Robotik und KI",
                    "priority": "should_have",
                },
                {
                    "type": "bullets",
                    "content": "Berlin\nMünchen",
                    "priority": "nice_to_have",
                    "metadata": {"type": "locations"},
                },
            ],
        }


class MockPresentationStrategistAgentV2:
    """Mock Presentation Strategist that returns test SlideBlueprint"""

    def __init__(self, api_key: str = "mock", **kwargs):
        self.api_key = api_key

    def plan(
        self,
        slide_intent: Dict[str, Any],
        content_blocks: List[Dict[str, Any]],
        design_system: Dict[str, Any] = None,
        image_metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Return mock blueprint"""
        return {
            "slide_title": "Unser Team",
            "layout_type": "two_row",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "stat-grid",
                    "position": "top",
                    "content_block_indices": [1],
                    "image_slot": None,
                    "layout_hints": {},
                },
                {
                    "component_id": "comp-2",
                    "type": "text",
                    "position": "middle",
                    "content_block_indices": [2],
                    "image_slot": None,
                    "layout_hints": {},
                },
                {
                    "component_id": "comp-3",
                    "type": "bullet-list",
                    "position": "bottom",
                    "content_block_indices": [3],
                    "image_slot": None,
                    "layout_hints": {},
                },
            ],
            "design_notes": "Team showcase with emphasis on experience and locations",
            "image_count": 0,
        }

    def replan(self, original_blueprint: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Return adjusted blueprint"""
        # For testing: just reduce to 2 components
        return {
            **original_blueprint,
            "components": original_blueprint["components"][:2],
            "design_notes": "Adjusted for feedback",
        }


class MockContentGeneratorAgentV2:
    """Mock Content Generator that returns test FormattedSlide"""

    def __init__(self, api_key: str = "mock", **kwargs):
        self.api_key = api_key

    def generate(
        self,
        slide_title: str,
        slide_blueprint: Dict[str, Any],
        content_blocks: List[Dict[str, Any]],
        language: str = "de",
        design_system: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Return mock formatted slide

        Args:
            design_system: Optional design system with components_schema (for slot validation)
        """
        return {
            "slide_title": "Unser Team",
            "slide_subtitle": None,
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "stat-grid",
                    "title": "Teamgröße",
                    "subtitle": None,
                    "statistics": [
                        {"label": "Experten", "value": "5"},
                    ],
                    "word_count": 2,
                    "formatting_notes": "Stat-grid with team size",
                },
                {
                    "component_id": "comp-2",
                    "type": "text",
                    "title": "Expertise",
                    "subtitle": None,
                    "paragraphs": [
                        "Unser fünfköpfiges Team bringt 20+ Jahre Erfahrung in Robotik, KI und Cloud-Technologien mit. "
                        "Gegründet von Experten aus Forschung und Industrie, fokussieren wir auf innovative Lösungen."
                    ],
                    "word_count": 28,
                    "formatting_notes": "Professional introduction",
                },
                {
                    "component_id": "comp-3",
                    "type": "bullet-list",
                    "title": "Standorte",
                    "subtitle": None,
                    "bullets": [
                        "Berlin — Hauptsitz und R&D",
                        "München — Partnership & Sales",
                    ],
                    "word_count": 7,
                    "formatting_notes": "Clear location list",
                },
            ],
            "language": language,
            "total_word_count": 37,
            "readability_score": "easy",
            "accessibility_notes": ["All text content is semantic and clear"],
        }

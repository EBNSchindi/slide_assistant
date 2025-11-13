"""
Mock Agents for testing without OpenAI API
"""
import json
import random


class MockContentAnalyzerAgent:
    """Mock Content Analyzer for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def analyze(self, user_input: str, slide_title: str = None) -> dict:
        """Mock analysis of user input"""
        # Determine content type based on keywords
        content_type = "mixed"
        if any(word in user_input.lower() for word in ["€", "%", "million", "mio"]):
            content_type = "statistics"
        elif any(word in user_input.lower() for word in ["list", "bullet", "point"]):
            content_type = "list"
        elif any(word in user_input.lower() for word in ["quote", "say", "said"]):
            content_type = "quote"
        elif any(word in user_input.lower() for word in ["problem", "challenge"]):
            content_type = "narrative"

        return {
            "content_type": content_type,
            "key_messages": ["Message 1", "Message 2", "Message 3"],
            "raw_content": user_input,
            "has_statistics": "€" in user_input or "%" in user_input,
            "has_lists": "-" in user_input or "•" in user_input,
            "has_quotes": '"' in user_input,
            "formatting_preferences": ["clean", "modern"],
        }


class MockPresentationStrategistAgent:
    """Mock Presentation Strategist for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def recommend(
        self, analysis: dict, style_guide: dict, preferences: dict = None
    ) -> dict:
        """Mock strategy recommendation"""
        available_components = style_guide.get("available_components", [])
        component_count = min(
            len([c for c in available_components if c in ["stat-grid", "bullet-list"]]) or 2,
            3,
        )

        return {
            "recommended_components": [
                {
                    "type": "bullet-list",
                    "content_indices": [0, 1, 2],
                    "layout_position": "middle",
                },
            ],
            "component_count": component_count,
            "layout_strategy": "Center-aligned with clear hierarchy",
            "styling_suggestions": [
                f"Use primary color {style_guide.get('primary_color')}",
                "Apply 16px spacing",
            ],
            "reasoning": "Simple, clean layout that respects design system",
        }


class MockContentGeneratorAgent:
    """Mock Content Generator for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def generate(
        self,
        analysis: dict,
        strategy: dict,
        style_guide: dict,
        slide_title: str = "Folie",
    ) -> dict:
        """Mock content generation"""
        # Generate simple markdown
        markdown = f"""# {slide_title}

## Komponente 1: Inhalt

- Punkt 1
- Punkt 2
- Punkt 3

## Komponente 2: Details

- Detail A
- Detail B
"""

        # Generate simple HTML
        html = f"""<div class="slide-section">
  <div class="component" id="slide-1-comp-1">
    <div class="component-label">Komponente 1</div>
    <h2>{slide_title}</h2>
    <ul class="bullet-list">
      <li>Punkt 1</li>
      <li>Punkt 2</li>
      <li>Punkt 3</li>
    </ul>
  </div>
  <div class="component" id="slide-1-comp-2">
    <div class="component-label">Komponente 2</div>
    <h2>Details</h2>
    <ul class="bullet-list">
      <li>Detail A</li>
      <li>Detail B</li>
    </ul>
  </div>
</div>"""

        return {
            "markdown": markdown,
            "html": html,
            "component_count": 2,
            "components_used": ["bullet-list", "text"],
        }

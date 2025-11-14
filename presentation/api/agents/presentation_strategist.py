"""
Presentation Strategist Agent - Recommends optimal presentation strategy
"""
from openai import AsyncOpenAI
import json


class PresentationStrategistAgent:
    """Recommends optimal presentation strategy based on content and style"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def recommend(
        self, analysis: dict, style_guide: dict, preferences: dict = None
    ) -> dict:
        """Recommend optimal presentation strategy"""

        style_context = f"""Available design system:
- Primary Color: {style_guide.get('primary_color', '#238636')}
- Secondary Colors: {style_guide.get('secondary_colors', [])}
- Font Family: {style_guide.get('font_family', 'sans-serif')}
- Available Components: {', '.join(style_guide.get('available_components', []))}
- Spacing Scale: {style_guide.get('spacing_scale', [])}

Design Guide Context:
{style_guide.get('design_guide', 'No specific design guide available')}"""

        content_context = f"""Content Analysis:
- Type: {analysis.get('content_type', 'mixed')}
- Key Messages: {analysis.get('key_messages', [])}
- Has Statistics: {analysis.get('has_statistics', False)}
- Has Lists: {analysis.get('has_lists', False)}
- Has Quotes: {analysis.get('has_quotes', False)}
- User Preferences: {preferences or {}}"""

        system_prompt = """You are a Presentation Strategist Agent. Based on the content analysis and design system, recommend:
1. Which components to use (stat-grid, bullet-list, quote, etc.)
2. How many components should be on this slide (max 3)
3. The best layout/arrangement
4. Specific styling suggestions based on the design guide

Respond with a JSON object containing:
{
    "recommended_components": [{"type": "stat-grid|bullet-list|quote|...", "content_indices": [0, 1], "layout_position": "top|middle|bottom"}],
    "component_count": 1-3,
    "layout_strategy": "description of layout",
    "styling_suggestions": ["suggestion1", "suggestion2"],
    "reasoning": "why this strategy is optimal"
}"""

        user_message = f"""{style_context}

{content_context}

Please recommend the optimal presentation strategy for this content."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.6,
                response_format={"type": "json_object"},
            )

            strategy = json.loads(response.choices[0].message.content)
            return strategy

        except Exception as e:
            raise Exception(f"Presentation Strategist error: {str(e)}")

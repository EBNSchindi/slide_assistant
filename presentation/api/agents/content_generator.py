"""
Content Generator Agent - Generates markdown and HTML from strategy
"""
from openai import OpenAI
import json


class ContentGeneratorAgent:
    """Generates markdown and HTML based on strategy and style"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(
        self,
        analysis: dict,
        strategy: dict,
        style_guide: dict,
        slide_title: str = "Folie",
    ) -> dict:
        """Generate markdown and HTML from analysis and strategy"""

        context = f"""Content Analysis: {json.dumps(analysis)}

Presentation Strategy: {json.dumps(strategy)}

Style Guide:
- Primary Color: {style_guide.get('primary_color', '#238636')}
- Font Family: {style_guide.get('font_family', 'sans-serif')}
- Available Components: {', '.join(style_guide.get('available_components', []))}

Slide Title: {slide_title}"""

        system_prompt = """You are a Content Generator Agent. Generate both markdown and HTML for a presentation slide.

MARKDOWN FORMAT:
- Use H1 for slide title
- Use H2 for component titles
- Use plain lists (- item) for content
- Include LLM conversion hints if needed

HTML FORMAT:
Use these component structures:
1. Stat Grid:
<div class="component" id="slide-X-comp-Y">
  <div class="component-label">Component Y</div>
  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-number">VALUE</div>
      <div class="stat-label">LABEL</div>
    </div>
  </div>
</div>

2. Bullet List:
<div class="component" id="slide-X-comp-Y">
  <div class="component-label">Component Y</div>
  <h2>Title</h2>
  <ul class="bullet-list">
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</div>

3. Quote:
<div class="component" id="slide-X-comp-Y">
  <div class="component-label">Component Y</div>
  <blockquote class="quote">
    <p>Quote text</p>
    <footer>Attribution</footer>
  </blockquote>
</div>

4. Text/Paragraph:
<div class="component" id="slide-X-comp-Y">
  <div class="component-label">Component Y</div>
  <h2>Title</h2>
  <p>Content</p>
</div>

IMPORTANT:
- Always use proper semantic HTML
- Use class names exactly as shown
- Component IDs format: slide-{number}-comp-{number}
- Apply style colors in data-attributes or inline styles where appropriate
- Ensure HTML is valid and well-formed

Respond with JSON:
{
    "markdown": "# slide title\\n\\n## Component 1\\ncontent...",
    "html": "<div class='slide-section'>...</div>",
    "component_count": 2,
    "components_used": ["stat-grid", "bullet-list"]
}"""

        user_message = f"""{context}

Please generate both markdown and HTML for this slide based on the analysis and strategy."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.5,
                response_format={"type": "json_object"},
            )

            output = json.loads(response.choices[0].message.content)
            return output

        except Exception as e:
            raise Exception(f"Content Generator error: {str(e)}")

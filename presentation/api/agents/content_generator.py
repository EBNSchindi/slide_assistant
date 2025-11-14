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
        project_scope: str = "",
        image_references: list = None,
        project_name: str = "beispiel-projekt",
    ) -> dict:
        """Generate markdown and HTML from analysis and strategy

        Args:
            analysis: Content analysis from ContentAnalyzer
            strategy: Presentation strategy from PresentationStrategist
            style_guide: Project style guide
            slide_title: Title for the slide
            project_scope: Project scope/context (optional)
            image_references: List of uploaded image filenames to include
            project_name: Name of the project for dynamic paths
        """

        # Build image context if images are provided
        image_context = ""
        if image_references and len(image_references) > 0:
            image_context = f"\n\nAVAILABLE IMAGES TO INCLUDE:\n"
            for idx, img in enumerate(image_references, 1):
                image_context += f"- Image {idx}: {img}\n"
                image_context += f"  Use in HTML as: <img src='projects/{project_name}/images/uploads/{img}' alt='...'>\n"
            image_context += "\nIMPORTANT: Use the EXACT paths shown above in the <img src='...'> tags. Do NOT use relative paths like 'images/uploads/'"

        context = f"""Content Analysis: {json.dumps(analysis)}

Presentation Strategy: {json.dumps(strategy)}

Style Guide:
- Primary Color: {style_guide.get('primary_color', '#238636')}
- Font Family: {style_guide.get('font_family', 'sans-serif')}
- Available Components: {', '.join(style_guide.get('available_components', []))}

Slide Title: {slide_title}{image_context}"""

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

5. Image Component:
<div class="component" id="slide-X-comp-Y">
  <div class="component-label">Component Y</div>
  <h2>Title</h2>
  <div class="image-container">
    <img src="images/uploads/FILENAME.png" alt="Description" style="max-width: 100%; height: auto; border-radius: 6px;">
  </div>
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

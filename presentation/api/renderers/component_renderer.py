"""
HTML Component Renderer - Deterministic, template-based HTML generation

Converts FormattedSlide (pure text) into HTML using fixed templates.
NO LLM involved - pure deterministic rendering with theme support.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from html import escape


@dataclass
class Theme:
    """Design theme configuration"""
    name: str
    primary_color: str = "#238636"
    secondary_color: str = "#6e40aa"
    background: str = "#ffffff"
    text_color: str = "#1f2937"
    border_color: str = "#e5e7eb"
    stat_size: str = "2.5rem"
    bullet_indent: str = "1.5rem"


class HTMLComponentRenderer:
    """Renders FormattedSlide components into HTML"""

    def __init__(self, theme: Optional[Theme] = None):
        """Initialize renderer with optional theme"""
        self.theme = theme or Theme(name="github")
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load component templates"""
        return {
            "stat-grid": self._stat_grid_template,
            "bullet-list": self._bullet_list_template,
            "quote": self._quote_template,
            "text": self._text_template,
            "image-frame": self._image_frame_template,
            "process": self._process_template,
            "table": self._table_template,
        }

    def render_component(self, component_data: Dict[str, Any]) -> str:
        """
        Render a single formatted component to HTML

        Args:
            component_data: FormattedComponentData as dict

        Returns:
            HTML string for the component
        """
        component_type = component_data.get("type", "text")
        component_id = component_data.get("component_id", "unknown")

        if component_type not in self.templates:
            raise ValueError(f"Unknown component type: {component_type}")

        template_fn = self.templates[component_type]
        html = template_fn(component_data)

        # Wrap in component container
        return f'''<div class="slide-component slide-{component_type}" id="{escape(component_id)}" data-type="{escape(component_type)}">
{html}
</div>'''

    def render_slide(self, formatted_slide: Dict[str, Any]) -> str:
        """
        Render complete slide with all components

        Args:
            formatted_slide: FormattedSlide as dict

        Returns:
            Complete HTML for slide
        """
        slide_id = formatted_slide.get("slide_id", "slide-1")
        slide_title = formatted_slide.get("slide_title", "Untitled")
        slide_subtitle = formatted_slide.get("slide_subtitle")
        components = formatted_slide.get("components", [])
        theme_name = formatted_slide.get("theme", "github")

        # Render all components
        components_html = "\n".join([self.render_component(comp) for comp in components])

        # Build slide HTML
        subtitle_html = f'<h2 class="slide-subtitle">{escape(slide_subtitle)}</h2>' if slide_subtitle else ""

        html = f'''<section class="slide slide-theme-{escape(theme_name)}" id="{escape(slide_id)}" data-slide-title="{escape(slide_title)}">
  <div class="slide-header">
    <h1 class="slide-title">{escape(slide_title)}</h1>
    {subtitle_html}
  </div>

  <div class="slide-content">
{components_html}
  </div>
</section>'''

        return html

    # ═══════════════════════════════════════════════════════════
    # Component Templates
    # ═══════════════════════════════════════════════════════════

    def _stat_grid_template(self, data: Dict[str, Any]) -> str:
        """stat-grid: Display statistics in grid format"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        statistics = data.get("statistics", [])

        title_html = f'<h3 class="component-title">{escape(title)}</h3>' if title else ""
        subtitle_html = f'<p class="component-subtitle">{escape(subtitle)}</p>' if subtitle else ""

        # Generate stat items
        stat_items = []
        for stat in statistics:
            label = stat.get("label", "")
            value = stat.get("value", "")
            stat_items.append(f'''    <div class="stat-item">
      <div class="stat-value" style="font-size: {self.theme.stat_size}; color: {self.theme.primary_color};">
        {escape(value)}
      </div>
      <div class="stat-label">{escape(label)}</div>
    </div>''')

        stats_grid = "\n".join(stat_items)

        return f'''{title_html}
{subtitle_html}
  <div class="stat-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 2rem;">
{stats_grid}
  </div>'''

    def _bullet_list_template(self, data: Dict[str, Any]) -> str:
        """bullet-list: Display bullet points"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        bullets = data.get("bullets", [])

        title_html = f'<h3 class="component-title">{escape(title)}</h3>' if title else ""
        subtitle_html = f'<p class="component-subtitle">{escape(subtitle)}</p>' if subtitle else ""

        # Generate bullets
        bullet_items = []
        for bullet in bullets:
            bullet_items.append(f'    <li>{escape(bullet)}</li>')

        bullets_list = "\n".join(bullet_items)

        return f'''{title_html}
{subtitle_html}
  <ul class="bullet-list" style="margin-left: {self.theme.bullet_indent}; list-style-type: disc;">
{bullets_list}
  </ul>'''

    def _quote_template(self, data: Dict[str, Any]) -> str:
        """quote: Display highlighted quote"""
        quote_text = data.get("quote_text", "")
        quote_author = data.get("quote_author")

        author_html = f'<p class="quote-author">— {escape(quote_author)}</p>' if quote_author else ""

        return f'''  <blockquote class="quote-block" style="border-left: 4px solid {self.theme.primary_color}; padding-left: 1.5rem;">
    <p class="quote-text"style="font-style: italic; font-size: 1.1rem;">
      "{escape(quote_text)}"
    </p>
    {author_html}
  </blockquote>'''

    def _text_template(self, data: Dict[str, Any]) -> str:
        """text: Display paragraphs"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        paragraphs = data.get("paragraphs", [])

        title_html = f'<h3 class="component-title">{escape(title)}</h3>' if title else ""
        subtitle_html = f'<p class="component-subtitle">{escape(subtitle)}</p>' if subtitle else ""

        # Generate paragraphs
        para_items = []
        for para in paragraphs:
            para_items.append(f'  <p class="text-paragraph">{escape(para)}</p>')

        paragraphs_html = "\n".join(para_items)

        return f'''{title_html}
{subtitle_html}
{paragraphs_html}'''

    def _image_frame_template(self, data: Dict[str, Any]) -> str:
        """image-frame: Display image with caption and title"""
        image_path = data.get("image_path", "")
        image_caption = data.get("image_caption")
        image_alt_text = data.get("image_alt_text", "Image")
        title = data.get("title")

        title_html = f'<h3 class="image-title">{escape(title)}</h3>' if title else ""
        caption_html = f'<p class="image-caption">{escape(image_caption)}</p>' if image_caption else ""

        return f'''  <div class="image-frame">
{title_html}
    <img src="{escape(image_path)}" alt="{escape(image_alt_text)}" class="frame-image" style="max-width: 100%; height: auto; border-radius: 8px;" />
{caption_html}
  </div>'''

    def _process_template(self, data: Dict[str, Any]) -> str:
        """process: Display sequential steps"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        bullets = data.get("bullets", [])  # Reuse bullets field for steps

        title_html = f'<h3 class="component-title">{escape(title)}</h3>' if title else ""
        subtitle_html = f'<p class="component-subtitle">{escape(subtitle)}</p>' if subtitle else ""

        # Generate step items
        step_items = []
        for i, step in enumerate(bullets, 1):
            step_items.append(f'''    <div class="process-step">
      <div class="step-number" style="background-color: {self.theme.primary_color}; color: white; width: 2rem; height: 2rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
        {i}
      </div>
      <div class="step-content">
        <p>{escape(step)}</p>
      </div>
    </div>''')

        steps_html = "\n".join(step_items)

        return f'''{title_html}
{subtitle_html}
  <div class="process-chain">
{steps_html}
  </div>'''

    def _table_template(self, data: Dict[str, Any]) -> str:
        """table: Display structured data in table format"""
        title = data.get("title")
        # Assuming table data in 'table_data' with headers and rows
        table_data = data.get("table_data", {"headers": [], "rows": []})

        title_html = f'<h3 class="component-title">{escape(title)}</h3>' if title else ""

        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])

        # Generate header row
        header_cells = "".join([f"<th>{escape(h)}</th>" for h in headers])
        header_row = f"    <tr>\n      {header_cells}\n    </tr>"

        # Generate data rows
        body_rows = []
        for row in rows:
            row_cells = "".join([f"<td>{escape(str(cell))}</td>" for cell in row])
            body_rows.append(f"    <tr>\n      {row_cells}\n    </tr>")

        body_html = "\n".join(body_rows)

        return f'''{title_html}
  <table class="data-table" style="width: 100%; border-collapse: collapse;">
    <thead>
{header_row}
    </thead>
    <tbody>
{body_html}
    </tbody>
  </table>'''


def render_styled_slide(
    formatted_slide: Dict[str, Any],
    theme_name: str = "github",
    css: Optional[str] = None,
) -> str:
    """
    Render a complete slide with CSS styling

    Args:
        formatted_slide: FormattedSlide dict
        theme_name: Theme to use (github, modern, minimal)
        css: Optional custom CSS

    Returns:
        Complete HTML with <style> tags
    """
    renderer = HTMLComponentRenderer(theme=Theme(name=theme_name))
    slide_html = renderer.render_slide(formatted_slide)

    default_css = f"""
<style>
  :root {{
    --primary-color: {renderer.theme.primary_color};
    --secondary-color: {renderer.theme.secondary_color};
    --background: {renderer.theme.background};
    --text-color: {renderer.theme.text_color};
    --border-color: {renderer.theme.border_color};
  }}

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text-color);
    background: var(--background);
  }}

  .slide {{
    padding: 3rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }}

  .slide-header {{
    margin-bottom: 2rem;
  }}

  .slide-title {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 0.5rem;
  }}

  .slide-subtitle {{
    font-size: 1.25rem;
    color: #666;
  }}

  .slide-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }}

  .slide-component {{
    padding: 1.5rem;
    border-radius: 8px;
    background: #f9fafb;
    border: 1px solid var(--border-color);
  }}

  .component-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 0.75rem;
  }}

  .component-subtitle {{
    font-size: 0.95rem;
    color: #666;
    margin-bottom: 1rem;
  }}

  .stat-item {{
    text-align: center;
  }}

  .stat-value {{
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.5rem;
  }}

  .stat-label {{
    font-size: 0.9rem;
    color: #666;
  }}

  .bullet-list {{
    list-style-position: inside;
    line-height: 1.8;
  }}

  .bullet-list li {{
    margin-bottom: 0.5rem;
  }}

  .quote-block {{
    background: #f0f4ff;
    padding: 1.5rem;
    border-radius: 8px;
  }}

  .quote-text {{
    margin-bottom: 1rem;
    color: var(--text-color);
  }}

  .quote-author {{
    font-size: 0.9rem;
    color: #666;
  }}

  .text-paragraph {{
    line-height: 1.6;
    margin-bottom: 1rem;
  }}

  .image-frame {{
    text-align: center;
  }}

  .frame-image {{
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }}

  .image-title {{
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }}

  .image-caption {{
    margin-top: 0.75rem;
    font-size: 0.9rem;
    color: #666;
    font-style: italic;
  }}

  .process-chain {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }}

  .process-step {{
    display: flex;
    gap: 1rem;
  }}

  .step-number {{
    flex-shrink: 0;
  }}

  .step-content {{
    flex: 1;
  }}

  .data-table {{
    border: 1px solid var(--border-color);
  }}

  .data-table th {{
    background: var(--primary-color);
    color: white;
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
  }}

  .data-table td {{
    padding: 0.75rem;
    border-bottom: 1px solid var(--border-color);
  }}

  .data-table tr:hover {{
    background: #f9fafb;
  }}
</style>
"""

    final_css = css or default_css

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(formatted_slide.get('slide_title', 'Slide'))}</title>
  {final_css}
</head>
<body>
  {slide_html}
</body>
</html>
"""

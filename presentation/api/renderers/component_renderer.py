"""
HTML Component Renderer - Deterministic, template-based HTML generation

Converts FormattedSlide (pure text) into HTML using Jinja2 templates.
NO LLM involved - pure deterministic rendering with theme support.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from html import escape
import sys
import os

# Add services directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from services.template_loader import TemplateLoader


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
    """Renders FormattedSlide components into HTML using Jinja2 templates"""

    def __init__(self, theme: Optional[Theme] = None):
        """Initialize renderer with optional theme and template loader"""
        self.theme = theme or Theme(name="github")
        self.template_loader = TemplateLoader()

        # Map component types to template names
        self.component_type_map = {
            "stat-grid": "stat-grid",
            "bullet-list": "bullet-list",
            "quote": "quote",
            "text": "text",
            "image-frame": "image-frame",
            "process": "process",
            "table": "table",
            "feature-grid": "feature-grid",
            "image-grid": "image-grid",
            "process-horizontal": "process-horizontal",
            "comparison-cards": "comparison-cards",
            "timeline": "timeline",
            "logo-grid": "logo-grid",
            "team-grid": "team-grid",
            "metric-trend": "metric-trend",
        }

    def render_component(self, component_data: Dict[str, Any], slide_num: int = 1, comp_num: int = 1) -> str:
        """
        Render a single formatted component to HTML using Jinja2 templates

        Args:
            component_data: FormattedComponentData as dict
            slide_num: Slide number for ID generation
            comp_num: Component number for ID generation

        Returns:
            HTML string for the component
        """
        component_type = component_data.get("type", "text")

        if component_type not in self.component_type_map:
            raise ValueError(f"Unknown component type: {component_type}")

        # Prepare data for template (extract fields from component_data)
        template_data = self._prepare_template_data(component_type, component_data)

        # Render using TemplateLoader
        return self.template_loader.render_component(
            component_type=self.component_type_map[component_type],
            data=template_data,
            slide_num=slide_num,
            comp_num=comp_num,
        )

    def render_slide(self, formatted_slide: Dict[str, Any]) -> str:
        """
        Render complete slide with all components using TemplateLoader

        Args:
            formatted_slide: FormattedSlide as dict

        Returns:
            Complete HTML for slide
        """
        slide_id = formatted_slide.get("slide_id", "slide-1")
        slide_title = formatted_slide.get("slide_title", "Untitled")
        components = formatted_slide.get("components", [])

        # Extract slide number from slide_id (format: "slide-N")
        try:
            slide_num = int(slide_id.split("-")[1]) if "-" in slide_id else 1
        except (IndexError, ValueError):
            slide_num = 1

        # Prepare data for TemplateLoader
        slide_data = {
            "slide_num": slide_num,
            "slide_title": slide_title,
            "components": [],
        }

        # Convert components to TemplateLoader format
        for comp in components:
            comp_type = comp.get("type", "text")
            template_data = self._prepare_template_data(comp_type, comp)

            slide_data["components"].append({
                "type": self.component_type_map.get(comp_type, "text"),
                "data": template_data,
            })

        # Render using TemplateLoader
        return self.template_loader.render_slide(slide_data)

    def _prepare_template_data(self, component_type: str, component_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare component data for Jinja2 templates

        Args:
            component_type: Type of component
            component_data: Raw component data from FormattedSlide

        Returns:
            Data dict formatted for template
        """
        # Extract common fields
        data = {
            "title": component_data.get("title"),
            "subtitle": component_data.get("subtitle"),
        }

        # Type-specific data extraction
        if component_type == "stat-grid":
            data["stats"] = component_data.get("statistics", [])

        elif component_type == "bullet-list":
            data["bullets"] = component_data.get("bullets", [])

        elif component_type == "quote":
            data["quote_text"] = component_data.get("quote_text", "")
            data["quote_author"] = component_data.get("quote_author")

        elif component_type == "text":
            data["paragraphs"] = component_data.get("paragraphs", [])

        elif component_type == "image-frame":
            data["image_path"] = component_data.get("image_path", "")
            data["image_caption"] = component_data.get("image_caption")
            data["image_alt_text"] = component_data.get("image_alt_text", "Image")

        elif component_type == "process":
            data["steps"] = component_data.get("steps", [])  # Process uses steps field
            data["show_arrows"] = component_data.get("show_arrows", True)

        elif component_type == "table":
            data["headers"] = component_data.get("table_headers", [])
            data["rows"] = component_data.get("table_rows", [])
            data["table_class"] = component_data.get("table_class")
            data["cell_badges"] = component_data.get("cell_badges")
            data["emphasis_rows"] = component_data.get("emphasis_rows", [])

        elif component_type == "feature-grid":
            data["features"] = component_data.get("features", [])

        elif component_type == "image-grid":
            data["images"] = component_data.get("images", [])
            data["grid_layout"] = component_data.get("grid_layout", "2x2")

        elif component_type == "process-horizontal":
            data["steps"] = component_data.get("steps", [])
            data["show_arrows"] = component_data.get("show_arrows", True)

        elif component_type == "comparison-cards":
            data["items"] = component_data.get("comparison_items", [])

        elif component_type == "timeline":
            data["items"] = component_data.get("timeline_items", [])
            data["orientation"] = component_data.get("timeline_orientation", "horizontal")

        elif component_type == "logo-grid":
            data["logos"] = component_data.get("logos", [])
            data["layout"] = component_data.get("logo_layout", "4-columns")

        elif component_type == "team-grid":
            data["members"] = component_data.get("team_members", [])

        elif component_type == "metric-trend":
            data["metrics"] = component_data.get("metrics", [])

        return data

    # ═══════════════════════════════════════════════════════════
    # Component Templates
    # ═══════════════════════════════════════════════════════════

    def _stat_grid_template(self, data: Dict[str, Any]) -> str:
        """stat-grid: Display statistics in grid format"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        statistics = data.get("statistics", [])

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""
        subtitle_html = f'  <p>{escape(subtitle)}</p>\n' if subtitle else ""

        # Generate stat cards (reference structure)
        stat_cards = []
        for stat in statistics:
            label = stat.get("label", "")
            value = stat.get("value", "")
            stat_cards.append(f'''            <div class="stat-card">
                <span class="stat-number">{escape(value)}</span>
                <span class="stat-label">{escape(label)}</span>
            </div>''')

        stats_grid = "\n".join(stat_cards)

        return f'''{title_html}{subtitle_html}
        <div class="stat-grid">
{stats_grid}
        </div>'''

    def _bullet_list_template(self, data: Dict[str, Any]) -> str:
        """bullet-list: Display bullet points"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        bullets = data.get("bullets", [])

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""
        subtitle_html = f'  <p>{escape(subtitle)}</p>\n' if subtitle else ""

        # Generate bullets
        bullet_items = []
        for bullet in bullets:
            bullet_items.append(f'            <li>{escape(bullet)}</li>')

        bullets_list = "\n".join(bullet_items)

        return f'''{title_html}{subtitle_html}
        <ul class="bullet-list">
{bullets_list}
        </ul>'''

    def _quote_template(self, data: Dict[str, Any]) -> str:
        """quote: Display highlighted quote"""
        quote_text = data.get("quote_text", "")
        quote_author = data.get("quote_author")

        author_html = f'\n    <footer>— {escape(quote_author)}</footer>' if quote_author else ""

        return f'''  <blockquote class="quote">
    <p>"{escape(quote_text)}"</p>{author_html}
  </blockquote>'''

    def _text_template(self, data: Dict[str, Any]) -> str:
        """text: Display paragraphs"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        paragraphs = data.get("paragraphs", [])

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""
        subtitle_html = f'  <p>{escape(subtitle)}</p>\n' if subtitle else ""

        # Generate paragraphs
        para_items = []
        for para in paragraphs:
            para_items.append(f'        <p>{escape(para)}</p>')

        paragraphs_html = "\n".join(para_items)

        return f'''{title_html}{subtitle_html}
{paragraphs_html}'''

    def _image_frame_template(self, data: Dict[str, Any]) -> str:
        """image-frame: Display image with caption and title"""
        image_path = data.get("image_path", "")
        image_caption = data.get("image_caption")
        image_alt_text = data.get("image_alt_text", "Image")
        title = data.get("title")

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""

        # Use structured image layout: .image-container > .image-wrapper + .image-content
        caption_html = f'''    <div class="image-content">
      <p>{escape(image_caption)}</p>
    </div>''' if image_caption else ""

        return f'''{title_html}
  <div class="image-container">
    <div class="image-wrapper">
      <img src="{escape(image_path)}" alt="{escape(image_alt_text)}" />
    </div>
{caption_html}
  </div>'''

    def _process_template(self, data: Dict[str, Any]) -> str:
        """process: Display sequential steps"""
        title = data.get("title")
        subtitle = data.get("subtitle")
        bullets = data.get("bullets", [])  # Reuse bullets field for steps

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""
        subtitle_html = f'  <p>{escape(subtitle)}</p>\n' if subtitle else ""

        # Generate step items (using reference structure)
        step_items = []
        for i, step in enumerate(bullets, 1):
            step_items.append(f'''    <div class="process-step">
      <div class="process-number">{i}</div>
      <div class="process-content">
        <p>{escape(step)}</p>
      </div>
    </div>''')

        steps_html = "\n".join(step_items)

        return f'''{title_html}{subtitle_html}
  <div class="process-chain">
{steps_html}
  </div>'''

    def _table_template(self, data: Dict[str, Any]) -> str:
        """table: Display structured data in table format"""
        title = data.get("title")
        # Assuming table data in 'table_data' with headers and rows
        table_data = data.get("table_data", {"headers": [], "rows": []})

        title_html = f'  <h2>{escape(title)}</h2>\n' if title else ""

        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])

        # Generate header row
        header_cells = "".join([f"<th>{escape(h)}</th>" for h in headers])
        header_row = f"      <tr>\n        {header_cells}\n      </tr>"

        # Generate data rows
        body_rows = []
        for row in rows:
            row_cells = "".join([f"<td>{escape(str(cell))}</td>" for cell in row])
            body_rows.append(f"      <tr>\n        {row_cells}\n      </tr>")

        body_html = "\n".join(body_rows)

        return f'''{title_html}
  <table>
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

"""
Template Loader Service - Jinja2-based HTML template rendering

Loads and renders Jinja2 templates for presentation components.
Guarantees consistent HTML structure matching reference slides.
"""

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from typing import Dict, List, Any, Optional
import os


class TemplateLoader:
    """Load and render Jinja2 templates for presentation components"""

    def __init__(self, template_dir: str = "templates"):
        """
        Initialize template loader with Jinja2 environment

        Args:
            template_dir: Root directory for templates (relative to project root)
        """
        # Get absolute path to template directory
        # Find the 'presentation' directory by searching upwards from __file__
        current = os.path.abspath(__file__)
        while os.path.basename(current) != "presentation" and current != "/":
            current = os.path.dirname(current)

        if os.path.basename(current) == "presentation":
            self.template_dir = os.path.join(current, template_dir)
        else:
            # Fallback: assume we're in api/services
            presentation_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.template_dir = os.path.join(presentation_dir, template_dir)


        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True,  # Auto-escape HTML for security
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_component(
        self,
        component_type: str,
        data: Dict[str, Any],
        slide_num: int = 1,
        comp_num: int = 1,
    ) -> str:
        """
        Render a single component from template

        Args:
            component_type: Type of component (stat-grid, bullet-list, etc.)
            data: Component data dict
            slide_num: Slide number for ID generation
            comp_num: Component number for ID generation

        Returns:
            Complete HTML for component (with wrapper)

        Raises:
            TemplateNotFound: If component template doesn't exist
        """
        # Load component template
        try:
            comp_template = self.env.get_template(f"components/{component_type}.html.j2")
        except TemplateNotFound:
            raise ValueError(f"Template not found for component type: {component_type}")

        # Render component content
        content = comp_template.render(**data)

        # Wrap in component wrapper
        wrapper_template = self.env.get_template("wrappers/component-wrapper.html.j2")
        return wrapper_template.render(
            slide_num=slide_num,
            comp_num=comp_num,
            content=content,
        )

    def render_slide(
        self,
        slide_data: Dict[str, Any],
    ) -> str:
        """
        Render complete slide with all components

        Args:
            slide_data: Slide data dict with structure:
                {
                    "slide_num": 1,
                    "slide_title": "Slide Title",
                    "components": [
                        {"type": "stat-grid", "data": {...}},
                        {"type": "bullet-list", "data": {...}},
                    ]
                }

        Returns:
            Complete HTML for slide
        """
        slide_num = slide_data.get("slide_num", 1)
        slide_title = slide_data.get("slide_title", "Untitled")
        components = slide_data.get("components", [])

        # Render all components
        components_html = []
        for idx, comp in enumerate(components, 1):
            comp_type = comp.get("type")
            comp_data = comp.get("data", {})

            comp_html = self.render_component(
                component_type=comp_type,
                data=comp_data,
                slide_num=slide_num,
                comp_num=idx,
            )
            components_html.append(comp_html)

        # Wrap in slide-section
        slide_template = self.env.get_template("wrappers/slide-section.html.j2")
        return slide_template.render(
            slide_title=slide_title,
            components=components_html,
        )

    def get_available_templates(self) -> List[str]:
        """
        Get list of available component templates

        Returns:
            List of component type names
        """
        components_dir = os.path.join(self.template_dir, "components")
        if not os.path.exists(components_dir):
            return []

        templates = []
        for filename in os.listdir(components_dir):
            if filename.endswith(".html.j2"):
                # Remove .html.j2 extension
                template_name = filename[:-8]
                templates.append(template_name)

        return sorted(templates)

    def get_reference_examples(self, project_name: str = "beispiel-projekt") -> List[Dict[str, str]]:
        """
        Load reference HTML examples from project directory

        Args:
            project_name: Name of project to load examples from

        Returns:
            List of dicts with {'folie': int, 'name': str, 'html': str}
        """
        import glob

        examples = []
        project_path = os.path.join(
            os.path.dirname(self.template_dir),
            "presentation",
            "projects",
            project_name,
            "html",
        )

        # Load folie-01 through folie-08
        for i in range(1, 9):
            pattern = os.path.join(project_path, f"folie-{i:02d}-*.html")
            files = glob.glob(pattern)

            if files:
                with open(files[0], "r", encoding="utf-8") as f:
                    examples.append({
                        "folie": i,
                        "name": os.path.basename(files[0]),
                        "html": f.read(),
                    })

        return examples

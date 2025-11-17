"""
Main renderer class for generating HTML from blueprints.

This is a deterministic, LLM-free renderer that uses Jinja2 templates.
"""

from typing import Dict, Tuple, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from datetime import datetime
import logging

from ..blueprints.models import (
    SlideBlueprint,
    CompleteBlueprint,
    ComponentBlueprint,
    LayoutType,
    ComponentType,
)
from ..blueprints.validator import BlueprintValidator, BlueprintValidationError

logger = logging.getLogger(__name__)


class RendererError(Exception):
    """Base exception for renderer errors"""
    pass


class SlideRenderer:
    """Deterministic HTML renderer for slide blueprints"""

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize renderer with template directory.

        Args:
            templates_dir: Path to templates directory. If None, uses default location.
        """
        if templates_dir is None:
            # Default: templates/ subdirectory in this module
            templates_dir = Path(__file__).parent / "templates"

        self.templates_dir = Path(templates_dir)
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory does not exist: {self.templates_dir}")
            # Create it for now
            self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters
        self.env.filters['component_type'] = self._filter_component_type

        self.validator = BlueprintValidator(validate_image_paths=False)

    def render(
        self,
        blueprint: Dict[str, Any],
        theme: str = "github",
        validate: bool = True,
    ) -> Tuple[str, Optional[str], Dict[str, Any]]:
        """
        Render a blueprint to HTML and optional Markdown.

        Args:
            blueprint: CompleteBlueprint as dict
            theme: Design theme (github, modern, minimal)
            validate: Whether to validate blueprint before rendering (default: True)

        Returns:
            Tuple of (html_string, markdown_string, metadata)

        Raises:
            RendererError: If rendering fails
            BlueprintValidationError: If blueprint is invalid
        """
        # Validate blueprint
        if validate:
            validated_blueprint = self.validator.validate(blueprint)
        else:
            # Parse without strict validation
            validated_blueprint = SlideBlueprint(**blueprint)

        logger.info(f"Rendering slide: {validated_blueprint.slide_id}")

        try:
            # Load layout template
            layout_template = self._load_layout_template(validated_blueprint.layout_type)

            # Render components
            rendered_components = []
            for component in validated_blueprint.components:
                html = self._render_component(component, theme)
                rendered_components.append(html)

            # Assemble slide
            html = self._assemble_slide(
                layout_template,
                validated_blueprint,
                rendered_components,
                theme,
            )

            # Generate markdown (optional, for now return None)
            markdown = None  # TODO: Implement markdown generation

            # Metadata
            metadata = {
                "component_count": len(validated_blueprint.components),
                "layout_type": validated_blueprint.layout_type.value,
                "theme": theme,
                "render_timestamp": datetime.now().isoformat(),
            }

            logger.info(f"Successfully rendered slide: {validated_blueprint.slide_id}")
            return html, markdown, metadata

        except TemplateNotFound as e:
            raise RendererError(f"Template not found: {e}")
        except Exception as e:
            raise RendererError(f"Rendering failed: {e}")

    def _load_layout_template(self, layout_type: LayoutType):
        """Load layout template based on layout type"""
        template_name = f"layouts/{layout_type.value}.html"
        try:
            return self.env.get_template(template_name)
        except TemplateNotFound:
            raise RendererError(
                f"Layout template not found: {template_name}. "
                f"Available templates should be in {self.templates_dir}/layouts/"
            )

    def _render_component(self, component: ComponentBlueprint, theme: str) -> str:
        """Render a single component using its template"""
        template_name = f"components/{component.type.value}.html"

        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            raise RendererError(
                f"Component template not found: {template_name}. "
                f"Available templates should be in {self.templates_dir}/components/"
            )

        # Render component
        return template.render(
            component=component,
            theme=theme,
        )

    def _assemble_slide(
        self,
        layout_template,
        blueprint: SlideBlueprint,
        components: list,
        theme: str,
    ) -> str:
        """Assemble final slide HTML"""
        return layout_template.render(
            slide_id=blueprint.slide_id,
            title=blueprint.slide_title,
            subtitle=blueprint.slide_subtitle,
            language=blueprint.language,
            components=components,
            theme=theme,
            metadata=blueprint.metadata,
            schema_version=blueprint.schema_version,
        )

    def _filter_component_type(self, component: ComponentBlueprint) -> str:
        """Jinja2 filter to get component type as string"""
        return component.type.value

    def render_to_file(
        self,
        blueprint: Dict[str, Any],
        output_path: str,
        theme: str = "github",
    ) -> Path:
        """
        Render blueprint and save to file.

        Args:
            blueprint: CompleteBlueprint as dict
            output_path: Path to save HTML file
            theme: Design theme

        Returns:
            Path to saved file
        """
        html, _, _ = self.render(blueprint, theme=theme)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"Saved HTML to: {output_file}")
        return output_file


# ═══════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════

def render_blueprint(
    blueprint: Dict[str, Any],
    theme: str = "github",
    templates_dir: Optional[str] = None,
) -> str:
    """
    Convenience function to render a blueprint to HTML.

    Args:
        blueprint: CompleteBlueprint as dict
        theme: Design theme
        templates_dir: Optional custom templates directory

    Returns:
        HTML string
    """
    renderer = SlideRenderer(templates_dir=templates_dir)
    html, _, _ = renderer.render(blueprint, theme=theme)
    return html

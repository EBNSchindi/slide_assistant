"""
v2 API Routes - New 3-agent pipeline with feedback loop

Implements the new architecture:
1. ContentAnalyzerAgentV2 (understand)
2. PresentationStrategistAgentV2 (plan) ← feedback loop
3. ContentGeneratorAgentV2 (write) ← validates & gives feedback
4. HTMLComponentRenderer (render HTML)
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import json
import sys
import os

# Add parent for imports
api_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, api_dir)

from agents.content_analyzer_v2 import ContentAnalyzerAgentV2
from agents.presentation_strategist_v2 import PresentationStrategistAgentV2
from agents.content_generator_v2 import ContentGeneratorAgentV2
from renderers.component_renderer import HTMLComponentRenderer, Theme, render_styled_slide
from config import OPENAI_API_KEY, TEST_MODE, DEFAULT_MODEL, PROJECTS_BASE_PATH
from services.file_service import FileService
from services.style_parser import StyleParser

router = APIRouter(prefix="/api/v2", tags=["v2"])


@router.post("/generate")
async def generate_slide_v2(
    request_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate slide using new 3-agent pipeline with feedback loop

    Request body:
    {
      "project_name": "beispiel-projekt",
      "slide_number": 46,
      "user_input": "Raw content for the slide",
      "slide_title": "Optional title",
      "theme": "github|modern|minimal",
      "language": "de|en",
      "images": [{"filename": "img.png", "description": "..."}]
    }

    Returns:
    {
      "success": true,
      "html": "...",
      "markdown": "...",
      "slide_blueprint": {...},
      "formatted_slide": {...},
      "iteration_count": 1
    }
    """

    try:
        # Extract request parameters
        project_name = request_data.get("project_name")
        slide_number = request_data.get("slide_number")
        user_input = request_data.get("user_input", "")
        slide_title = request_data.get("slide_title", "")
        theme = request_data.get("theme", "github")
        language = request_data.get("language", "de")
        images = request_data.get("images", [])

        if not project_name or not user_input:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: project_name, user_input",
            )

        # ═══════════════════════════════════════════════════════════
        # STAGE 1: Content Analysis (Agent 1)
        # ═══════════════════════════════════════════════════════════

        analyzer = ContentAnalyzerAgentV2(
            api_key=OPENAI_API_KEY,
            model=DEFAULT_MODEL,
        )

        analysis_result = analyzer.analyze(
            user_input=user_input,
        )

        slide_intent = analysis_result.get("slide_intent", {})
        content_blocks = analysis_result.get("content_blocks", [])

        # Override language if explicitly set
        if language:
            slide_intent["language"] = language

        # ═══════════════════════════════════════════════════════════
        # STAGE 2: Layout Planning (Agent 2) with retry loop
        # ═══════════════════════════════════════════════════════════

        strategist = PresentationStrategistAgentV2(
            api_key=OPENAI_API_KEY,
            model=DEFAULT_MODEL,
        )

        # Load design system from project (includes components_schema from design-guide.json)
        # Supports shared themes (apple, openai) and project-specific themes
        project_path = os.path.join(PROJECTS_BASE_PATH, project_name)
        style_parser = StyleParser(project_path, theme_name=theme)
        design_system = style_parser.parse_project_style()

        # Fallback for basic fields if not in parsed style
        if "max_components" not in design_system:
            design_system["max_components"] = 3

        image_metadata = None
        if images:
            image_metadata = {
                "images": images,
            }

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
            design_system=design_system,
            image_metadata=image_metadata,
        )

        # ═══════════════════════════════════════════════════════════
        # STAGE 3: Content Generation (Agent 3) with feedback loop
        # ═══════════════════════════════════════════════════════════

        generator = ContentGeneratorAgentV2(
            api_key=OPENAI_API_KEY,
            model=DEFAULT_MODEL,
        )

        iteration_count = 0
        max_iterations = 3
        formatted_slide = None
        validation_result = None

        while iteration_count < max_iterations:
            iteration_count += 1

            # Generate content
            gen_result = generator.generate(
                slide_title=slide_title or blueprint.get("slide_title", ""),
                slide_blueprint=blueprint,
                content_blocks=content_blocks,
                language=language,
                design_system=design_system,  # Pass for slot validation
            )

            # Check if valid
            if "is_valid" in gen_result and not gen_result["is_valid"]:
                # Validation failed - feedback from Agent 3
                validation_result = gen_result
                suggested_changes = gen_result.get("suggested_changes", {})

                # Ask strategist to replan
                if iteration_count < max_iterations:
                    blueprint = strategist.replan(
                        original_blueprint=blueprint,
                        feedback=validation_result,
                    )
                else:
                    # Max iterations reached, return as-is with warning
                    formatted_slide = {
                        "slide_title": slide_title or blueprint.get("slide_title", ""),
                        "components": [],
                        "language": language,
                        "warnings": ["Max iterations reached, some content may be cut"],
                    }
                    break
            else:
                # Success! Got valid formatted slide
                formatted_slide = gen_result
                break

        if not formatted_slide:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate formatted slide after max iterations",
            )

        # ═══════════════════════════════════════════════════════════
        # STAGE 4: HTML Rendering (Deterministic, no LLM)
        # ═══════════════════════════════════════════════════════════

        renderer = HTMLComponentRenderer(theme=Theme(name=theme))

        # Add slide_id for HTML rendering
        formatted_slide["slide_id"] = f"slide-{slide_number}" if slide_number else "slide-1"
        formatted_slide["theme"] = theme

        # Generate HTML
        html = renderer.render_slide(formatted_slide)

        # Convert to markdown (basic conversion)
        markdown = _formatted_slide_to_markdown(formatted_slide)

        # ═══════════════════════════════════════════════════════════
        # SAVE OUTPUT
        # ═══════════════════════════════════════════════════════════

        # Save HTML and Markdown if project_name provided
        if project_name and slide_number:
            try:
                project_path = os.path.join(PROJECTS_BASE_PATH, project_name)
                file_service = FileService(project_path=project_path)

                slide_slug = _slugify(slide_title or f"slide-{slide_number}")
                filename = f"folie-{slide_number:02d}-{slide_slug}"

                file_service.save_html_slide(
                    slide_name=filename,
                    content=html,
                )
                file_service.save_markdown_slide(
                    slide_name=filename,
                    content=markdown,
                )
            except Exception as e:
                # Non-fatal: if saving fails, still return generated content
                print(f"Warning: Failed to save files: {e}")

        return {
            "success": True,
            "html": html,
            "markdown": markdown,
            "slide_blueprint": blueprint,
            "formatted_slide": formatted_slide,
            "iteration_count": iteration_count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}",
        )


def _formatted_slide_to_markdown(formatted_slide: Dict[str, Any]) -> str:
    """Convert FormattedSlide to markdown"""
    lines = []

    # Title
    slide_title = formatted_slide.get("slide_title", "")
    if slide_title:
        lines.append(f"# {slide_title}")
        lines.append("")

    # Subtitle
    slide_subtitle = formatted_slide.get("slide_subtitle")
    if slide_subtitle:
        lines.append(f"## {slide_subtitle}")
        lines.append("")

    # Components
    for comp in formatted_slide.get("components", []):
        comp_type = comp.get("type")

        if comp_type == "stat-grid":
            lines.append("## Statistics")
            for stat in comp.get("statistics", []):
                label = stat.get("label", "")
                value = stat.get("value", "")
                lines.append(f"- **{label}**: {value}")
            lines.append("")

        elif comp_type == "bullet-list":
            title = comp.get("title")
            if title:
                lines.append(f"## {title}")
            for bullet in comp.get("bullets", []):
                lines.append(f"- {bullet}")
            lines.append("")

        elif comp_type == "quote":
            quote_text = comp.get("quote_text", "")
            quote_author = comp.get("quote_author")
            author_str = f" — {quote_author}" if quote_author else ""
            lines.append(f"> \"{quote_text}\"{author_str}")
            lines.append("")

        elif comp_type == "text":
            title = comp.get("title")
            if title:
                lines.append(f"## {title}")
            for para in comp.get("paragraphs", []):
                lines.append(para)
            lines.append("")

        elif comp_type == "image-frame":
            title = comp.get("title")
            if title:
                lines.append(f"## {title}")
            image_path = comp.get("image_path", "")
            if image_path:
                caption = comp.get("image_caption", "")
                lines.append(f"![{caption}]({image_path})")
            lines.append("")

    return "\n".join(lines)


def _slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    import re

    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text[:50]  # Limit to 50 chars

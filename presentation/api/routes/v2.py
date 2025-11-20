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

from agents.orchestrator_v2 import AgentOrchestratorV2
from config import OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, TEST_MODE, DEFAULT_MODEL, PROJECTS_BASE_PATH, MODEL_TO_PROVIDER

router = APIRouter(prefix="/api/v2", tags=["v2"])


@router.post("/generate")
async def generate_slide_v2(
    request_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate slide using new 3-agent pipeline with multi-provider support

    Request body:
    {
      "project_name": "beispiel-projekt",
      "slide_number": 46,
      "user_input": "Raw content for the slide",
      "slide_title": "Optional title",
      "theme": "github|modern|minimal|apple|openai",
      "language": "de|en",
      "model": "gpt-4o|gpt-5|claude-sonnet-4.5|gemini-3.0-pro",  (optional, auto-detects provider)
      "images": [{"filename": "img.png", "description": "..."}]
    }

    Returns:
    {
      "success": true,
      "provider": "openai|anthropic|google",
      "model": "gpt-4o",
      "html_content": "...",
      "markdown_content": "...",
      "feedback_iterations": 0
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
        model = request_data.get("model", DEFAULT_MODEL)

        if not project_name or not user_input:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: project_name, user_input",
            )

        # ═══════════════════════════════════════════════════════════
        # USE ORCHESTRATOR V2 (Multi-Provider Support)
        # ═══════════════════════════════════════════════════════════

        # Auto-detect provider from model
        provider = MODEL_TO_PROVIDER.get(model, "openai")

        # Initialize orchestrator with provider-specific agents
        orchestrator = AgentOrchestratorV2(
            model=model,
            test_mode=TEST_MODE,
            provider=provider,
        )

        # Prepare image references
        image_filenames = [img.get("filename") for img in images] if images else []

        # Generate slide
        result = orchestrator.generate_slide(
            user_input=user_input,
            project_name=project_name,
            slide_title=slide_title or f"Folie {slide_number}",
            slide_number=slide_number,
            theme=theme,
            language=language,
            image_references=image_filenames,
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error"),
            )

        # Return result (already includes html_content, markdown_content, etc.)
        return result

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

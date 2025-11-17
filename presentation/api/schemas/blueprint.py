"""
Agent Blueprint Schemas - Intermediate data structures for the 3-agent pipeline

These models define the strict interfaces between:
1. ContentAnalyzerAgent → ContentBlock + SlideIntent
2. PresentationStrategistAgent → SlideBlueprint
3. ContentGeneratorAgent → FormattedSlide (with optional ValidationResult for feedback)
4. HTMLComponentRenderer → HTML output
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum


# ═══════════════════════════════════════════════════════════
# Content Blocks (Agent 1 Output)
# ═══════════════════════════════════════════════════════════

class ContentBlockType(str, Enum):
    """Types of content blocks"""
    STATISTIC = "statistic"      # Single number with label: "5 Experten"
    STATISTICS = "statistics"    # Multiple numbers: 3+ stats
    STATEMENT = "statement"      # Thesis/claim: "Wir sind führend in..."
    BULLET = "bullet"            # Single bullet point
    BULLETS = "bullets"          # Multiple bullets
    QUOTE = "quote"              # Direct quote/testimonial
    IMAGE_REF = "image_ref"      # Reference to image: "Zeige Team-Foto"
    TITLE = "title"              # Slide title


class ContentBlock(BaseModel):
    """Single content building block from Agent 1"""
    type: ContentBlockType = Field(..., description="Type of content")
    content: str = Field(..., description="Actual content text")
    priority: Literal["must_have", "should_have", "nice_to_have"] = Field(
        default="should_have", description="Importance for slide"
    )
    image_hint: Optional[str] = Field(None, description="Reference to image if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class SlideIntent(BaseModel):
    """Overall intention/goal of the slide from Agent 1"""
    intent_type: Literal[
        "problem", "solution", "team", "kpi", "timeline", "process",
        "use_case", "market", "competition", "roadmap", "other"
    ] = Field(..., description="Type of slide intent")
    primary_message: str = Field(..., description="Main message in 1 sentence")
    target_audience: Optional[str] = Field(None, description="Who should understand this? (e.g. investor, team)")
    language: Literal["de", "en"] = Field(default="de", description="Content language")
    density: Literal["low", "medium", "high"] = Field(
        ..., description="Information density"
    )


# ═══════════════════════════════════════════════════════════
# Component Blueprint (Agent 2 Output)
# ═══════════════════════════════════════════════════════════

class ImageSlot(BaseModel):
    """Reference to an image that should be included"""
    slot_id: str = Field(..., description="Unique slot identifier, e.g., 'main_visual'")
    image_filename: str = Field(..., description="Filename of uploaded image")
    position: Literal["left", "right", "top", "bottom", "center"] = Field(
        default="right", description="Position in component"
    )
    description: Optional[str] = Field(None, description="User-provided image description")


class ComponentBlueprint(BaseModel):
    """Blueprint for a single slide component"""
    component_id: str = Field(..., description="Unique ID, e.g., 'comp-1'")
    type: Literal["stat-grid", "bullet-list", "quote", "text", "image-frame", "process", "table"] = Field(
        ..., description="Component type"
    )
    position: Literal["top", "middle", "bottom"] = Field(
        ..., description="Position in slide layout"
    )
    content_block_indices: List[int] = Field(
        ..., description="Indices of ContentBlocks assigned to this component"
    )
    image_slot: Optional[ImageSlot] = Field(None, description="Image slot if applicable")
    layout_hints: Dict[str, Any] = Field(
        default_factory=dict, description="Layout-specific hints, e.g., {'columns': 2}"
    )


class SlideBlueprint(BaseModel):
    """Complete blueprint for slide layout and component structure (Agent 2 output)"""
    slide_title: str = Field(..., description="Slide title/heading")
    layout_type: Literal["single", "two_column", "two_row", "three_component", "custom"] = Field(
        default="single", description="Overall layout pattern"
    )
    components: List[ComponentBlueprint] = Field(
        ..., description="Components in order", min_items=1, max_items=3
    )
    design_notes: Optional[str] = Field(None, description="Designer notes for component generation")
    image_count: int = Field(default=0, description="Total number of images to be used")


# ═══════════════════════════════════════════════════════════
# Formatted Content (Agent 3 Output)
# ═══════════════════════════════════════════════════════════

class FormattedComponentData(BaseModel):
    """Fully formatted text data for a single component (no HTML)"""
    component_id: str = Field(..., description="Reference to ComponentBlueprint ID")
    type: Literal["stat-grid", "bullet-list", "quote", "text", "image-frame", "process", "table"] = Field(
        ..., description="Component type"
    )

    # Core content fields (all optional to support different component types)
    title: Optional[str] = Field(None, description="Component title")
    subtitle: Optional[str] = Field(None, description="Component subtitle")

    # For stat-grid
    statistics: Optional[List[Dict[str, str]]] = Field(
        None, description="List of {label, value} pairs for stat-grid"
    )

    # For bullet-list
    bullets: Optional[List[str]] = Field(None, description="Formatted bullet points")

    # For quote
    quote_text: Optional[str] = Field(None, description="Quote content")
    quote_author: Optional[str] = Field(None, description="Quote attribution")

    # For text
    paragraphs: Optional[List[str]] = Field(None, description="Text paragraphs")

    # For image-frame
    image_path: Optional[str] = Field(None, description="Path to image file")
    image_caption: Optional[str] = Field(None, description="Image caption")
    image_alt_text: Optional[str] = Field(None, description="Alt text for image")

    # Metadata
    word_count: int = Field(default=0, description="Approximate word count")
    formatting_notes: Optional[str] = Field(None, description="Notes on formatting applied")


class FormattedSlide(BaseModel):
    """Fully formatted slide content, ready for renderer (Agent 3 output)"""
    slide_title: str = Field(..., description="Slide title")
    slide_subtitle: Optional[str] = Field(None, description="Optional slide subtitle")
    components: List[FormattedComponentData] = Field(
        ..., description="Formatted components in order"
    )
    language: Literal["de", "en"] = Field(default="de", description="Output language")
    total_word_count: int = Field(default=0, description="Total words in slide")
    readability_score: Literal["easy", "medium", "complex"] = Field(
        default="medium", description="Readability assessment"
    )
    accessibility_notes: List[str] = Field(
        default_factory=list, description="Accessibility notes"
    )


# ═══════════════════════════════════════════════════════════
# Feedback & Validation
# ═══════════════════════════════════════════════════════════

class ValidationWarning(BaseModel):
    """Single validation warning"""
    component_id: str = Field(..., description="Which component")
    issue: str = Field(..., description="What went wrong")
    suggestion: str = Field(..., description="How to fix it")


class ValidationResult(BaseModel):
    """Feedback from Agent 3 if generation needs adjustment"""
    is_valid: bool = Field(..., description="Can this be rendered as-is?")
    warnings: List[ValidationWarning] = Field(
        default_factory=list, description="List of issues found"
    )
    suggested_changes: Optional[Dict[str, Any]] = Field(
        None, description="Proposed adjustments to blueprint"
    )
    retry_count: int = Field(default=0, description="How many retries have occurred")
    max_retries: int = Field(default=2, description="Maximum retry attempts")


class AgentResponse(BaseModel):
    """Union-like response from Agent 3: either valid slide or validation result"""
    success: bool = Field(..., description="Did generation succeed?")
    formatted_slide: Optional[FormattedSlide] = Field(None, description="If success=true")
    validation_result: Optional[ValidationResult] = Field(None, description="If success=false")


# ═══════════════════════════════════════════════════════════
# Renderer Input/Output
# ═══════════════════════════════════════════════════════════

class ComponentHTML(BaseModel):
    """Single rendered component"""
    component_id: str = Field(..., description="Reference to FormattedComponentData ID")
    type: str = Field(..., description="Component type")
    html: str = Field(..., description="Generated HTML")
    css_classes: List[str] = Field(default_factory=list, description="CSS classes applied")


class RenderedSlide(BaseModel):
    """Complete rendered slide"""
    slide_id: str = Field(..., description="Unique slide identifier")
    slide_title: str = Field(..., description="Slide title")
    html: str = Field(..., description="Complete HTML for slide")
    markdown: str = Field(..., description="Markdown representation")
    components: List[ComponentHTML] = Field(..., description="Individual component renders")
    theme: str = Field(default="github", description="Design theme used")
    language: str = Field(default="de", description="Content language")

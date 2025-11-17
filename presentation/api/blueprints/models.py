"""
Pydantic models for slide blueprints.

These models define the complete type-safe schema for slide blueprints,
ensuring validation at every step of the pipeline.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union, Dict, Any
from enum import Enum
from datetime import datetime


# ═══════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════

class LayoutType(str, Enum):
    """Available layout types"""
    SINGLE_COLUMN = "single_column"      # One column, components stacked
    TWO_COLUMN = "two_column"            # Left + right columns
    THREE_ROW = "three_row"              # Top, middle, bottom rows
    HEADER_CONTENT = "header_content"    # Large header + content below
    SIDEBAR_MAIN = "sidebar_main"        # Sidebar (30%) + main content (70%)


class ComponentType(str, Enum):
    """Available component types"""
    STAT_GRID = "stat_grid"
    BULLET_LIST = "bullet_list"
    QUOTE = "quote"
    TEXT_BLOCK = "text_block"
    IMAGE_FRAME = "image_frame"
    PROCESS_CHAIN = "process_chain"  # Future
    TABLE = "table"                   # Future


class ComponentPosition(str, Enum):
    """Available component positions"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    FULL_WIDTH = "full_width"


# ═══════════════════════════════════════════════════════════
# Component Content Models
# ═══════════════════════════════════════════════════════════

class StatItem(BaseModel):
    """Single statistic item"""
    value: str = Field(..., description="Numeric value (formatted: '€12,5', '85%', '3x')")
    label: str = Field(..., description="Label text (e.g., 'Experten', 'Wachstum')")
    unit: Optional[str] = Field(None, description="Optional unit suffix (e.g., 'Mio', '%')")
    sublabel: Optional[str] = Field(None, description="Optional secondary label")
    emphasis: bool = Field(default=False, description="Whether to emphasize this stat")


class StatGridContent(BaseModel):
    """Content for stat-grid component"""
    title: Optional[str] = Field(None, description="Optional grid title")
    items: List[StatItem] = Field(
        ...,
        min_length=2,
        max_length=4,
        description="Statistics items (2-4)"
    )
    layout: Literal["2x1", "2x2", "3x1", "4x1"] = Field(
        default="2x2",
        description="Grid layout"
    )


class BulletItem(BaseModel):
    """Single bullet point"""
    text: str = Field(..., max_length=120, description="Bullet point text (max 120 chars)")
    level: Literal[1, 2, 3] = Field(default=1, description="Indentation level")
    icon: Optional[str] = Field(None, description="Optional icon (emoji or name)")
    emphasis: bool = Field(default=False, description="Whether to emphasize this item")


class BulletListContent(BaseModel):
    """Content for bullet-list component"""
    title: Optional[str] = Field(None, description="Optional list title")
    items: List[BulletItem] = Field(
        ...,
        min_length=2,
        max_length=6,
        description="Bullet points (2-6)"
    )
    style: Literal["default", "checkmarks", "arrows", "numbers"] = Field(
        default="default",
        description="Bullet style variant"
    )


class QuoteContent(BaseModel):
    """Content for quote component"""
    quote_text: str = Field(..., max_length=300, description="Quote text (max 300 chars)")
    author: Optional[str] = Field(None, description="Quote author")
    author_title: Optional[str] = Field(None, description="Author title/role")
    source: Optional[str] = Field(None, description="Source citation")
    style: Literal["default", "highlighted", "testimonial"] = Field(
        default="default",
        description="Quote style variant"
    )


class TextBlockContent(BaseModel):
    """Content for text-block component"""
    title: Optional[str] = Field(None, description="Optional block title")
    paragraphs: List[str] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Text paragraphs (1-3)"
    )
    emphasis_phrases: Optional[List[str]] = Field(
        None,
        description="Phrases to emphasize (will be bolded)"
    )
    text_align: Literal["left", "center", "right"] = Field(
        default="left",
        description="Text alignment"
    )


class GalleryImage(BaseModel):
    """Single image in a gallery"""
    image_id: str = Field(..., description="Image filename")
    image_path: str = Field(..., description="Relative path to image")
    caption: Optional[str] = Field(None, max_length=100, description="Image caption")
    alt_text: str = Field(..., max_length=150, description="Accessibility alt text")


class ImageFrameContent(BaseModel):
    """Content for image-frame component"""
    # Single image variant
    image_id: Optional[str] = Field(None, description="Image filename (single variant)")
    image_path: Optional[str] = Field(None, description="Relative path (single variant)")
    alt_text: Optional[str] = Field(None, max_length=150, description="Alt text (single variant)")

    # Gallery variant
    images: Optional[List[GalleryImage]] = Field(
        None,
        description="List of images (gallery variants)"
    )

    # Text content
    title: Optional[str] = Field(None, max_length=60, description="Image title")
    caption: Optional[str] = Field(None, max_length=200, description="Image caption")

    # Frame configuration
    frame_variant: Literal["single", "gallery_2", "gallery_3", "fullwidth"] = Field(
        default="single",
        description="Frame variant"
    )
    aspect_ratio: Literal["16:9", "4:3", "1:1", "auto"] = Field(
        default="auto",
        description="Image aspect ratio"
    )

    # Fullwidth-specific
    overlay_text: bool = Field(
        default=False,
        description="Show title as overlay (fullwidth only)"
    )


# ═══════════════════════════════════════════════════════════
# Blueprint Models
# ═══════════════════════════════════════════════════════════

class ComponentBlueprint(BaseModel):
    """Blueprint for a single component"""
    component_id: str = Field(..., description="Unique component ID within slide")
    type: ComponentType = Field(..., description="Component type")
    position: ComponentPosition = Field(..., description="Position in layout")

    # Content is type-specific - using Union for proper typing
    content: Union[
        StatGridContent,
        BulletListContent,
        QuoteContent,
        TextBlockContent,
        ImageFrameContent,
        Dict[str, Any]  # Fallback for future component types
    ] = Field(..., description="Type-specific content")

    styling: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional styling overrides"
    )


class SlideMetadata(BaseModel):
    """Optional metadata for slide tracking"""
    created_by: Literal["ai", "manual", "hybrid"] = Field(
        ...,
        description="Creation method"
    )
    created_at: str = Field(..., description="ISO timestamp")

    agent_versions: Optional[Dict[str, str]] = Field(
        None,
        description="Agent versions used (e.g., {'analyzer': '1.0', 'strategist': '1.0'})"
    )

    content_density: Literal["low", "medium", "high", "too_high"] = Field(
        ...,
        description="Content density indicator"
    )

    tags: List[str] = Field(default_factory=list, description="Content tags")
    notes: Optional[str] = Field(None, description="Developer/creator notes")


class SlideBlueprint(BaseModel):
    """Complete blueprint for a single slide"""
    schema_version: str = Field(default="1.0", description="Blueprint schema version")
    slide_id: str = Field(..., description="Unique slide identifier (e.g., 'slide-01-problem')")
    slide_title: str = Field(..., description="Main slide title")
    slide_subtitle: Optional[str] = Field(None, description="Optional subtitle")

    layout_type: LayoutType = Field(..., description="Layout strategy for this slide")
    language: Literal["de", "en"] = Field(..., description="Content language")

    components: List[ComponentBlueprint] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Ordered list of components (max 3 per slide)"
    )

    metadata: Optional[SlideMetadata] = Field(None, description="Optional metadata")


# ═══════════════════════════════════════════════════════════
# Partial Blueprint (from Agent 2)
# ═══════════════════════════════════════════════════════════

class ComponentMapping(BaseModel):
    """Mapping of content blocks to a component (from Agent 2)"""
    component_id: str = Field(..., description="Component ID (e.g., 'comp-1')")
    component_type: ComponentType = Field(..., description="Component type")
    position: ComponentPosition = Field(..., description="Position in layout")

    content_block_indices: List[int] = Field(
        ...,
        description="Indices of content blocks (from Agent 1) used in this component"
    )

    # Image mapping (if applicable)
    image_filename: Optional[str] = Field(
        None,
        description="Image filename for image-frame components"
    )

    # Structural hints for Agent 3
    structure_hint: Optional[str] = Field(
        None,
        description="Hint for Agent 3 (e.g., '2x2 grid', '4 bullets', 'single image with caption')"
    )


class PartialBlueprint(BaseModel):
    """Partial blueprint from Agent 2 (incomplete, needs Agent 3 to fill text)"""

    # Layout decisions
    layout_type: LayoutType = Field(..., description="Chosen layout type")
    component_mappings: List[ComponentMapping] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Component mappings (max 3)"
    )

    # Quality assessment
    cognitive_load_score: Literal["low", "medium", "high", "too_high"] = Field(
        ...,
        description="Expected cognitive load"
    )

    # Reasoning
    reasoning: str = Field(
        ...,
        description="Explanation for layout choices (references design principles)"
    )

    # Warnings
    warnings: List[str] = Field(default_factory=list, description="Layout warnings")

    # Alternative suggestions
    alternative_layouts: Optional[List[str]] = Field(
        None,
        description="Alternative layout suggestions (if applicable)"
    )


# ═══════════════════════════════════════════════════════════
# Complete Blueprint (from Agent 3)
# ═══════════════════════════════════════════════════════════

class CompleteBlueprint(SlideBlueprint):
    """Complete blueprint ready for rendering (extends SlideBlueprint)"""

    # All fields from SlideBlueprint are inherited and must be filled

    # Additional validation fields
    readability_score: Literal["easy", "medium", "complex"] = Field(
        ...,
        description="Overall readability assessment"
    )
    accessibility_compliant: bool = Field(
        ...,
        description="Whether blueprint meets accessibility requirements"
    )
    word_count_per_component: List[int] = Field(
        ...,
        description="Word count for each component (for content density tracking)"
    )


# ═══════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════

def create_slide_id(slide_number: int, title: str) -> str:
    """
    Generate a slide ID from number and title.

    Args:
        slide_number: Slide number (1-based)
        title: Slide title

    Returns:
        Formatted slide ID (e.g., 'slide-01-team')
    """
    # Sanitize title: lowercase, replace spaces with hyphens, remove special chars
    sanitized_title = title.lower()
    sanitized_title = sanitized_title.replace(" ", "-")
    # Keep only alphanumeric and hyphens
    sanitized_title = "".join(c for c in sanitized_title if c.isalnum() or c == "-")

    return f"slide-{slide_number:02d}-{sanitized_title}"


def create_component_id(component_number: int) -> str:
    """
    Generate a component ID.

    Args:
        component_number: Component number within slide (1-based)

    Returns:
        Formatted component ID (e.g., 'comp-1')
    """
    return f"comp-{component_number}"


def validate_layout_positions(
    layout_type: LayoutType,
    components: List[ComponentBlueprint]
) -> bool:
    """
    Validate that component positions are compatible with layout type.

    Args:
        layout_type: The layout type
        components: List of components

    Returns:
        True if valid, False otherwise

    Raises:
        ValueError: If validation fails with detailed error message
    """
    positions = [c.position for c in components]

    if layout_type == LayoutType.TWO_COLUMN:
        if len(components) != 2:
            raise ValueError(
                f"two_column layout requires exactly 2 components, got {len(components)}"
            )
        if set(positions) != {ComponentPosition.LEFT, ComponentPosition.RIGHT}:
            raise ValueError(
                f"two_column layout requires 'left' and 'right' positions, got {positions}"
            )

    elif layout_type == LayoutType.HEADER_CONTENT:
        if len(components) != 2:
            raise ValueError(
                f"header_content layout requires exactly 2 components, got {len(components)}"
            )
        if ComponentPosition.TOP not in positions:
            raise ValueError(
                "header_content layout requires one component with 'top' position"
            )

    elif layout_type == LayoutType.SIDEBAR_MAIN:
        if len(components) != 2:
            raise ValueError(
                f"sidebar_main layout requires exactly 2 components, got {len(components)}"
            )
        if set(positions) != {ComponentPosition.LEFT, ComponentPosition.RIGHT}:
            raise ValueError(
                f"sidebar_main layout requires 'left' and 'right' positions, got {positions}"
            )

    return True

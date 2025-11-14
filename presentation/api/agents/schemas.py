"""
Pydantic schemas for agent outputs - Type-safe structured outputs
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ═══════════════════════════════════════════════════════════
# Content Analyzer Schemas
# ═══════════════════════════════════════════════════════════

class PhaseInfo(BaseModel):
    """Information about a phase in phased content"""
    name: str = Field(..., description="Phase name (e.g., 'Phase 1')")
    timeframe: str = Field(..., description="Timeframe for this phase (e.g., '2026-2028')")
    target: str = Field(..., description="Target audience or goal for this phase")


class ContentAnalysis(BaseModel):
    """Structured analysis of user input content"""
    content_type: Literal["statistics", "narrative", "list", "quote", "image", "mixed", "phased", "hierarchical"] = Field(
        ..., description="Primary content type classification"
    )
    key_messages: List[str] = Field(
        ..., description="Specific, actionable key messages (max 3)", min_items=1, max_items=3
    )
    raw_content: str = Field(..., description="Structured representation of input")

    # Content flags
    has_statistics: bool = Field(default=False, description="Contains numeric statistics")
    has_lists: bool = Field(default=False, description="Contains list/enumeration content")
    has_quotes: bool = Field(default=False, description="Contains quotes or testimonials")
    has_images: bool = Field(default=False, description="Contains or references images")
    has_icons: bool = Field(default=False, description="Contains icons or emojis")

    # Optional metadata
    image_references: Optional[List[str]] = Field(None, description="Referenced image filenames")
    image_purpose: Optional[str] = Field(None, description="Purpose of the image content")
    icons_used: Optional[List[str]] = Field(None, description="List of icons/emojis used")
    sources: Optional[List[str]] = Field(None, description="Data sources cited (e.g., 'Bank of America')")
    temporal_context: Optional[List[str]] = Field(None, description="Time references (e.g., '2025', 'bis 2030')")
    phases: Optional[List[PhaseInfo]] = Field(None, description="Phase information for phased content")

    # Recommendations
    formatting_preferences: List[str] = Field(
        default_factory=list, description="Formatting suggestions"
    )
    content_density: Literal["low", "medium", "high", "too_high"] = Field(
        ..., description="Density of information"
    )
    recommended_components: Optional[int] = Field(None, ge=1, le=3, description="Recommended number of components")
    narrative_arc: Optional[Literal["problem-solution", "before-after", "chronological"]] = Field(
        None, description="Narrative structure if present"
    )

    # Quality indicators
    warnings: List[str] = Field(default_factory=list, description="Warnings or issues detected")
    needs_user_input: bool = Field(default=False, description="Whether user clarification is needed")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in analysis")


# ═══════════════════════════════════════════════════════════
# Presentation Strategist Schemas
# ═══════════════════════════════════════════════════════════

class ComponentRecommendation(BaseModel):
    """Recommendation for a single component"""
    type: Literal["stat-grid", "bullet-list", "quote", "text", "image"] = Field(
        ..., description="Component type"
    )
    content_indices: List[int] = Field(..., description="Indices of key messages this component addresses")
    layout_position: Literal["top", "middle", "bottom"] = Field(
        ..., description="Position in slide layout"
    )
    structure: Optional[str] = Field(None, description="Special structure (e.g., 'hierarchical_with_h3_sections')")


class AlternativeLayout(BaseModel):
    """Alternative layout option"""
    brief: str = Field(..., description="Brief description of alternative")
    when_to_use: str = Field(..., description="When this alternative would be better")


class PresentationStrategy(BaseModel):
    """Strategic recommendation for presentation layout"""
    recommended_components: List[ComponentRecommendation] = Field(
        ..., description="Recommended components in order", min_items=1, max_items=3
    )
    component_count: int = Field(..., ge=1, le=3, description="Number of components recommended")
    layout_strategy: str = Field(..., description="Named layout strategy being used")

    styling_suggestions: List[str] = Field(
        ..., description="Specific, actionable styling suggestions", min_items=1
    )
    reasoning: str = Field(
        ..., description="Detailed explanation referencing design principles"
    )

    cognitive_load_score: Literal["low", "medium", "high", "too_high"] = Field(
        ..., description="Expected cognitive load"
    )
    accessibility_notes: List[str] = Field(
        default_factory=list, description="Accessibility considerations"
    )
    alternative_layouts: List[AlternativeLayout] = Field(
        default_factory=list, description="Alternative layout options"
    )
    warnings: List[str] = Field(default_factory=list, description="Warnings or concerns")


# ═══════════════════════════════════════════════════════════
# Content Generator Schemas
# ═══════════════════════════════════════════════════════════

class GeneratedContent(BaseModel):
    """Generated markdown and HTML content"""
    markdown: str = Field(..., description="Generated markdown content")
    html: str = Field(..., description="Generated HTML content")

    component_count: int = Field(..., ge=1, le=3, description="Number of components generated")
    components_used: List[str] = Field(
        ..., description="List of component types used", min_items=1
    )

    readability_score: Literal["easy", "medium", "complex"] = Field(
        ..., description="Readability assessment"
    )
    accessibility_compliant: bool = Field(..., description="Whether output meets accessibility requirements")

    word_count_per_component: List[int] = Field(
        ..., description="Word count for each component"
    )
    optimization_notes: List[str] = Field(
        default_factory=list, description="Notes on optimizations applied"
    )


class VariantContent(BaseModel):
    """Single design variant content"""
    profile: str = Field(..., description="Design profile name")
    html_content: str = Field(..., description="HTML content for this variant")
    markdown_content: str = Field(..., description="Markdown content for this variant")
    components_used: List[str] = Field(..., description="Components used in this variant")
    readability_score: Optional[str] = Field(None, description="Readability score")


class VariantGeneration(BaseModel):
    """Multiple design variants"""
    variants: List[VariantContent] = Field(
        ..., description="List of design variants", min_items=1
    )
    variant_count: int = Field(..., ge=1, description="Number of variants generated")
    components_used: List[List[str]] = Field(
        ..., description="Components used per variant"
    )

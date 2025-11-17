"""
Blueprint system for slide generation.

This module provides the core data structures (Pydantic models) for representing
slides as structured blueprints that can be rendered deterministically.
"""

from .models import (
    # Enums
    LayoutType,
    ComponentType,
    ComponentPosition,

    # Content Models
    StatItem,
    StatGridContent,
    BulletItem,
    BulletListContent,
    QuoteContent,
    TextBlockContent,
    GalleryImage,
    ImageFrameContent,

    # Blueprint Models
    ComponentBlueprint,
    SlideMetadata,
    SlideBlueprint,

    # Partial Blueprint (from Agent 2)
    ComponentMapping,
    PartialBlueprint,

    # Complete Blueprint (from Agent 3)
    CompleteBlueprint,
)

__all__ = [
    # Enums
    "LayoutType",
    "ComponentType",
    "ComponentPosition",

    # Content Models
    "StatItem",
    "StatGridContent",
    "BulletItem",
    "BulletListContent",
    "QuoteContent",
    "TextBlockContent",
    "GalleryImage",
    "ImageFrameContent",

    # Blueprint Models
    "ComponentBlueprint",
    "SlideMetadata",
    "SlideBlueprint",
    "ComponentMapping",
    "PartialBlueprint",
    "CompleteBlueprint",
]

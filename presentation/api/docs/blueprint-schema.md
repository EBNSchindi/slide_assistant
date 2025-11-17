# Slide Blueprint Schema

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2025-11-17

## Purpose

The Slide Blueprint is the **central data structure** that connects all three agents and the renderer. It serves as a domain-specific language (DSL) for describing slide content in a structured, LLM-independent format.

## Design Principles

1. **LLM-Independent:** Blueprint can be created manually or by AI
2. **Type-Safe:** Validated with Pydantic schemas
3. **Renderer-Ready:** Contains all information needed for HTML generation
4. **Human-Readable:** JSON format that can be manually edited
5. **Versionable:** Blueprints can be saved and versioned alongside slides

## Schema Definition

### Top-Level Structure

```json
{
  "schema_version": "1.0",
  "slide_id": "slide-01-problem",
  "slide_title": "Das Problem",
  "layout_type": "two_column",
  "language": "de",
  "components": [...],
  "metadata": {...}
}
```

### Component Structure

Each component follows this pattern:

```json
{
  "component_id": "comp-1",
  "type": "stat_grid",
  "position": "left",
  "content": {...},
  "styling": {...}
}
```

## Pydantic Models

### SlideBlueprint (Root Model)

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class LayoutType(str, Enum):
    """Available layout types"""
    SINGLE_COLUMN = "single_column"      # One column, components stacked
    TWO_COLUMN = "two_column"            # Left + right columns
    THREE_ROW = "three_row"              # Top, middle, bottom rows
    HEADER_CONTENT = "header_content"    # Large header + content below
    SIDEBAR_MAIN = "sidebar_main"        # Sidebar (30%) + main content (70%)

class SlideBlueprint(BaseModel):
    """Complete blueprint for a single slide"""
    schema_version: str = Field(default="1.0", description="Blueprint schema version")
    slide_id: str = Field(..., description="Unique slide identifier (e.g., 'slide-01-problem')")
    slide_title: str = Field(..., description="Main slide title")
    slide_subtitle: Optional[str] = Field(None, description="Optional subtitle")

    layout_type: LayoutType = Field(..., description="Layout strategy for this slide")
    language: Literal["de", "en"] = Field(..., description="Content language")

    components: List["ComponentBlueprint"] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="Ordered list of components (max 3 per slide)"
    )

    metadata: Optional["SlideMetadata"] = Field(None, description="Optional metadata")
```

### ComponentBlueprint (Base)

```python
class ComponentPosition(str, Enum):
    """Available component positions"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    FULL_WIDTH = "full_width"

class ComponentType(str, Enum):
    """Available component types"""
    STAT_GRID = "stat_grid"
    BULLET_LIST = "bullet_list"
    QUOTE = "quote"
    TEXT_BLOCK = "text_block"
    IMAGE_FRAME = "image_frame"
    PROCESS_CHAIN = "process_chain"
    TABLE = "table"

class ComponentBlueprint(BaseModel):
    """Base blueprint for any component"""
    component_id: str = Field(..., description="Unique component ID within slide")
    type: ComponentType = Field(..., description="Component type")
    position: ComponentPosition = Field(..., description="Position in layout")

    content: dict = Field(..., description="Type-specific content (see below)")
    styling: Optional[dict] = Field(None, description="Optional styling overrides")
```

### Component Content Models

#### StatGridContent

```python
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
    items: List[StatItem] = Field(..., min_items=2, max_items=4, description="Statistics items")
    layout: Literal["2x1", "2x2", "3x1", "4x1"] = Field(default="2x2", description="Grid layout")
```

#### BulletListContent

```python
class BulletItem(BaseModel):
    """Single bullet point"""
    text: str = Field(..., max_length=120, description="Bullet point text (max 120 chars)")
    level: Literal[1, 2, 3] = Field(default=1, description="Indentation level")
    icon: Optional[str] = Field(None, description="Optional icon (emoji or name)")
    emphasis: bool = Field(default=False, description="Whether to emphasize this item")

class BulletListContent(BaseModel):
    """Content for bullet-list component"""
    title: Optional[str] = Field(None, description="Optional list title")
    items: List[BulletItem] = Field(..., min_items=2, max_items=6, description="Bullet points")
    style: Literal["default", "checkmarks", "arrows", "numbers"] = Field(
        default="default",
        description="Bullet style variant"
    )
```

#### ImageFrameContent

```python
class ImageFrameContent(BaseModel):
    """Content for image-frame component"""
    image_id: str = Field(..., description="Image filename (e.g., 'teamfoto.png')")
    image_path: str = Field(..., description="Relative path to image file")

    title: Optional[str] = Field(None, max_length=60, description="Image title (max 60 chars)")
    caption: Optional[str] = Field(None, max_length=200, description="Image caption (max 200 chars)")
    alt_text: str = Field(..., max_length=150, description="Accessibility alt text (required)")

    frame_variant: Literal["single", "gallery_2", "gallery_3", "fullwidth"] = Field(
        default="single",
        description="Image frame variant"
    )
    aspect_ratio: Literal["16:9", "4:3", "1:1", "auto"] = Field(
        default="auto",
        description="Image aspect ratio"
    )
```

#### TextBlockContent

```python
class TextBlockContent(BaseModel):
    """Content for text-block component"""
    title: Optional[str] = Field(None, description="Optional block title")
    paragraphs: List[str] = Field(..., min_items=1, max_items=3, description="Text paragraphs")

    emphasis_phrases: Optional[List[str]] = Field(
        None,
        description="Phrases to emphasize (will be bolded)"
    )
    text_align: Literal["left", "center", "right"] = Field(default="left", description="Text alignment")
```

#### QuoteContent

```python
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
```

### SlideMetadata

```python
class SlideMetadata(BaseModel):
    """Optional metadata for slide tracking"""
    created_by: Literal["ai", "manual", "hybrid"] = Field(..., description="Creation method")
    created_at: str = Field(..., description="ISO timestamp")

    agent_versions: Optional[dict] = Field(
        None,
        description="Agent versions used (e.g., {'analyzer': '1.0', 'strategist': '1.0'})"
    )

    content_density: Literal["low", "medium", "high"] = Field(
        ...,
        description="Content density indicator"
    )

    tags: List[str] = Field(default_factory=list, description="Content tags")
    notes: Optional[str] = Field(None, description="Developer/creator notes")
```

## Example Blueprints

### Example 1: Team Slide with Stats + Image

```json
{
  "schema_version": "1.0",
  "slide_id": "slide-03-team",
  "slide_title": "Unser Team",
  "slide_subtitle": "Experten für Robotik und KI",
  "layout_type": "two_column",
  "language": "de",
  "components": [
    {
      "component_id": "comp-1",
      "type": "stat_grid",
      "position": "left",
      "content": {
        "title": "Team Expertise",
        "items": [
          {
            "value": "5",
            "label": "Experten",
            "unit": null,
            "emphasis": true
          },
          {
            "value": "20",
            "label": "Jahre Erfahrung",
            "unit": "Jahre",
            "emphasis": false
          },
          {
            "value": "3",
            "label": "Standorte",
            "unit": null,
            "emphasis": false
          }
        ],
        "layout": "2x2"
      }
    },
    {
      "component_id": "comp-2",
      "type": "image_frame",
      "position": "right",
      "content": {
        "image_id": "teamfoto.png",
        "image_path": "projects/beispiel-projekt/images/uploads/teamfoto.png",
        "title": "Unser Kernteam",
        "caption": "Experten für Robotik, KI und Cloud-Technologien",
        "alt_text": "Gruppenfoto der fünf Kernmitglieder des Robo4you-Teams vor dem Bürogebäude",
        "frame_variant": "single",
        "aspect_ratio": "16:9"
      }
    }
  ],
  "metadata": {
    "created_by": "ai",
    "created_at": "2025-11-17T10:30:00Z",
    "agent_versions": {
      "analyzer": "1.0",
      "strategist": "1.0",
      "generator": "1.0"
    },
    "content_density": "medium",
    "tags": ["team", "about-us", "expertise"]
  }
}
```

### Example 2: Problem Slide with Bullets

```json
{
  "schema_version": "1.0",
  "slide_id": "slide-01-problem",
  "slide_title": "Das Problem",
  "layout_type": "single_column",
  "language": "de",
  "components": [
    {
      "component_id": "comp-1",
      "type": "bullet_list",
      "position": "full_width",
      "content": {
        "title": "Aktuelle Herausforderungen in der Industrie",
        "items": [
          {
            "text": "Manuelle Prozesse kosten bis zu 40% der Arbeitszeit",
            "level": 1,
            "icon": "⏱️",
            "emphasis": true
          },
          {
            "text": "Fehlerquote bei repetitiven Aufgaben über 15%",
            "level": 1,
            "icon": "⚠️",
            "emphasis": false
          },
          {
            "text": "Bestehende Lösungen zu teuer oder zu komplex",
            "level": 1,
            "icon": "💰",
            "emphasis": false
          }
        ],
        "style": "default"
      }
    }
  ],
  "metadata": {
    "created_by": "ai",
    "created_at": "2025-11-17T10:25:00Z",
    "content_density": "medium",
    "tags": ["problem", "challenges"]
  }
}
```

## Validation Rules

### Blueprint-Level Rules

1. **Max 3 components per slide** (enforced by `max_items=3`)
2. **Unique component IDs** within a slide
3. **Position compatibility:** Layout type must support chosen positions
4. **Language consistency:** All text content must match declared language

### Component-Level Rules

1. **Stat Grid:**
   - 2-4 items required
   - Layout must match item count (2x2 requires 4 items, etc.)

2. **Bullet List:**
   - 2-6 items required
   - Text max 120 chars per item
   - Levels 1-3 only

3. **Image Frame:**
   - `image_path` must exist
   - Alt text required (accessibility)
   - Title max 60 chars, caption max 200 chars

4. **Text Block:**
   - 1-3 paragraphs
   - No hard character limit, but renderer may truncate

5. **Quote:**
   - Quote text max 300 chars
   - Author optional but recommended

## Usage in Agent Pipeline

### Agent 1 → Agent 2

Agent 1 does NOT produce a Blueprint. It produces a simplified **Content Analysis** with content blocks.

### Agent 2 → Agent 3

Agent 2 produces a **partial Blueprint**:
- `layout_type` ✅
- `components` with `type` and `position` ✅
- `content` fields **partially filled** (structure only, no final text)

Example:
```json
{
  "components": [
    {
      "type": "stat_grid",
      "position": "left",
      "content": {
        "items": [
          {"value": "[TBD]", "label": "[TBD]"},
          {"value": "[TBD]", "label": "[TBD]"}
        ]
      }
    }
  ]
}
```

### Agent 3 → Renderer

Agent 3 produces a **complete Blueprint**:
- All `[TBD]` placeholders filled with final text
- `slide_title`, `slide_subtitle` finalized
- `metadata` added
- Ready for rendering

### Manual Usage

Developers can:
1. Write blueprints manually (JSON files)
2. Render them directly: `python render_slide.py blueprint.json output.html`
3. Bypass agents entirely for prototyping

## Versioning Strategy

### Schema Version Field

The `schema_version` field enables evolution:
- **1.0:** Initial version (this spec)
- **1.1:** Minor additions (new optional fields)
- **2.0:** Breaking changes (different structure)

### Backward Compatibility

Renderer must support **all v1.x** schemas. When loading:
1. Check `schema_version`
2. Apply migrations if needed
3. Validate against target schema

## Next Steps

1. Implement Pydantic models in `presentation/api/blueprints/models.py`
2. Add validation logic in `presentation/api/blueprints/validator.py`
3. Create fixture blueprints for testing in `presentation/api/blueprints/fixtures/`
4. Build renderer that consumes blueprints

## Related Documentation

- [Agent 1 Specification](./agent-1-content-analyzer.md)
- [Agent 2 Specification](./agent-2-presentation-strategist.md)
- [Agent 3 Specification](./agent-3-content-generator.md)
- [Renderer Specification](./renderer-specification.md)
- [Template Inventory](./template-inventory.md)

# Agent 2: Presentation Strategist

**Version:** 1.0
**Status:** Draft
**Agent Role:** Layout & Component Planning
**Last Updated:** 2025-11-17

## Mission Statement

**"Wie übersetze ich diese Content-Blöcke in 2–3 klare Komponenten und einen Layout-Plan?"**

Agent 2 takes structured content blocks from Agent 1 and decides which components to use, how to arrange them, and where to place images—without writing final text.

## Responsibilities

### ✅ What Agent 2 DOES

1. **Component Selection**
   - Choose 1-3 components from available types (stat-grid, bullet-list, quote, text-block, image-frame, etc.)
   - Map content blocks to components (which blocks go into which component?)
   - Decide component order and hierarchy

2. **Layout Planning**
   - Select layout type (single_column, two_column, header_content, etc.)
   - Assign positions to components (left/right, top/middle/bottom)
   - Ensure layout fits chosen component count

3. **Image Placement Strategy**
   - Decide if/where images appear
   - Choose image frame variant (single, gallery, fullwidth)
   - Map uploaded images to components

4. **Design System Compliance**
   - Enforce max 3 components per slide
   - Follow design system rules (e.g., stat-grid requires 2-4 items)
   - Consider cognitive load and accessibility

5. **Quality Assurance**
   - Assess cognitive load (low/medium/high/too_high)
   - Provide reasoning for layout choices
   - Suggest alternatives if appropriate

### ❌ What Agent 2 DOES NOT DO

1. **No Text Writing** - Does not write headings, bullets, or captions
2. **No HTML/Markdown** - Output is structured Blueprint (JSON), not markup
3. **No Content Creation** - Uses only content blocks from Agent 1
4. **No Styling Decisions** - No colors, fonts, specific CSS (follows design system)
5. **No Image Creation** - Only places existing uploaded images

## Process Flow

### When is Agent 2 Called?

**Trigger:** Agent 1 completes content analysis.

**Frequency:** Once per slide, immediately after Agent 1.

**Order:** Second agent in pipeline (after Agent 1, before Agent 3).

### Agent 2 Workflow

```
┌─────────────────────────────────────┐
│  Input from Agent 1                 │
│  - ContentAnalysis                  │
│  - content_blocks                   │
│  - key_messages                     │
│  - content_type                     │
│  - suggested_component_count        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Design System Knowledge            │
│  - Available component types        │
│  - Layout types                     │
│  - Design rules (max 3 components)  │
│  - Template constraints             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Agent 2: Presentation Strategist   │
│                                     │
│  1. Choose component types          │
│  2. Map content blocks → components │
│  3. Select layout type              │
│  4. Assign component positions      │
│  5. Plan image placement            │
│  6. Assess cognitive load           │
│  7. Generate partial blueprint      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Output: Partial Blueprint          │
│  - layout_type                      │
│  - components (type, position)      │
│  - content mapping (blocks → comp)  │
│  - image slots defined              │
│  - [TBD] placeholders for text      │
└─────────────────────────────────────┘
              ↓
         [Agent 3]
```

## Input Specification

### Required Fields

```python
class StrategistInput(BaseModel):
    """Input for Agent 2 from Agent 1"""
    content_analysis: ContentAnalysis = Field(..., description="Full output from Agent 1")

    # Design system info
    available_components: List[str] = Field(
        ...,
        description="List of available component types (from design system)"
    )
    available_layouts: List[str] = Field(
        ...,
        description="List of available layout types"
    )

    # Uploaded images (if any)
    uploaded_images: Optional[List[ImageMetadata]] = Field(
        None,
        description="Metadata for uploaded images"
    )
```

### ImageMetadata Schema

```python
class ImageMetadata(BaseModel):
    """Metadata for an uploaded image"""
    filename: str = Field(..., description="Image filename (e.g., 'teamfoto.png')")
    file_path: str = Field(..., description="Relative path to image")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    dimensions: Optional[str] = Field(None, description="Image dimensions (e.g., '1920x1080')")
    mime_type: Optional[str] = Field(None, description="MIME type (e.g., 'image/png')")
    user_description: Optional[str] = Field(None, description="User-provided description")
```

### Example Input

```json
{
  "content_analysis": {
    "content_type": "mixed",
    "language": "de",
    "key_messages": [
      "Team von 5 Experten",
      "20+ Jahre Erfahrung",
      "3 Standorte in Deutschland"
    ],
    "content_blocks": [
      {
        "block_type": "statistic",
        "raw_text": "5 Experten",
        "importance": "critical",
        "statistic_value": "5",
        "statistic_label": "Experten"
      },
      {
        "block_type": "statistic",
        "raw_text": "20 Jahre Erfahrung",
        "importance": "high",
        "statistic_value": "20",
        "statistic_unit": "Jahre",
        "statistic_label": "Erfahrung"
      },
      {
        "block_type": "image_ref",
        "raw_text": "Teamfoto",
        "importance": "medium",
        "image_filename": "teamfoto.png"
      }
    ],
    "has_statistics": true,
    "has_images": true,
    "suggested_component_count": 2
  },

  "available_components": ["stat-grid", "bullet-list", "quote", "text-block", "image-frame"],
  "available_layouts": ["single_column", "two_column", "three_row", "header_content"],

  "uploaded_images": [
    {
      "filename": "teamfoto.png",
      "file_path": "projects/beispiel-projekt/images/uploads/teamfoto.png",
      "dimensions": "1920x1080",
      "mime_type": "image/png",
      "user_description": "Teamfoto vor dem Büro"
    }
  ]
}
```

## Output Specification

### Output Schema: PartialBlueprint

```python
class ComponentMapping(BaseModel):
    """Mapping of content blocks to a component"""
    component_id: str = Field(..., description="Component ID (e.g., 'comp-1')")
    component_type: ComponentType = Field(..., description="Component type")
    position: ComponentPosition = Field(..., description="Position in layout")

    content_block_indices: List[int] = Field(
        ...,
        description="Indices of content blocks (from Agent 1) used in this component"
    )

    # Image mapping (if applicable)
    image_filename: Optional[str] = Field(None, description="Image filename for image-frame components")

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
        min_items=1,
        max_items=3,
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
```

### Example Output

```json
{
  "layout_type": "two_column",

  "component_mappings": [
    {
      "component_id": "comp-1",
      "component_type": "stat_grid",
      "position": "left",
      "content_block_indices": [0, 1],
      "structure_hint": "2x1 grid - 2 stats"
    },
    {
      "component_id": "comp-2",
      "component_type": "image_frame",
      "position": "right",
      "content_block_indices": [2],
      "image_filename": "teamfoto.png",
      "structure_hint": "single image with title and caption"
    }
  ],

  "cognitive_load_score": "low",

  "reasoning": "Two-column layout balances statistics (left) with visual proof (team photo, right). Stat-grid provides quick scanability of key metrics. Image-frame adds credibility and human connection. Low cognitive load due to only 2 components with clear visual separation.",

  "warnings": [],

  "alternative_layouts": [
    "header_content: Stats as header row, image below (more emphasis on numbers)",
    "single_column: Stack stats and image vertically (mobile-friendly)"
  ]
}
```

## Decision Rules

### Component Selection Logic

| Content Type | Suggested Components | Example |
|--------------|---------------------|---------|
| `statistics` (2-4 items) | 1x `stat_grid` | "5 Experten, 20 Jahre" |
| `statistics` (5+ items) | 1x `stat_grid` + 1x `bullet_list` | Split into key stats + details |
| `list` (2-6 bullets) | 1x `bullet_list` | Problem statements |
| `quote` | 1x `quote` | Customer testimonial |
| `narrative` | 1x `text_block` (or 2x if long) | Story-driven content |
| `mixed` (stats + image) | 1x `stat_grid` + 1x `image_frame` | Team stats + photo |
| `mixed` (bullets + image) | 1x `bullet_list` + 1x `image_frame` | Problems + screenshot |
| `image` only | 1x `image_frame` (fullwidth variant) | Hero image |

### Layout Selection Logic

| Component Count | Layout Type | Rationale |
|-----------------|-------------|-----------|
| 1 component | `single_column` or `header_content` | Full focus on one element |
| 2 components (equal importance) | `two_column` | Side-by-side balance |
| 2 components (title + content) | `header_content` | Title emphasis |
| 3 components | `three_row` or `sidebar_main` | Vertical stacking or sidebar |

### Image Placement Rules

1. **Single Image + Stats/Bullets:**
   - Layout: `two_column` (image on right, content on left)
   - Rationale: Text first (F-pattern reading), image provides proof

2. **Single Image (Hero):**
   - Layout: `single_column`
   - Component: `image_frame` with `fullwidth` variant

3. **Multiple Images (2-3):**
   - Component: `image_frame` with `gallery_2` or `gallery_3` variant
   - Layout: `single_column` or `header_content` (gallery below)

4. **No Image:**
   - Default to text-based layouts

### Cognitive Load Assessment

| Score | Criteria |
|-------|----------|
| `low` | 1-2 components, clear visual hierarchy, < 6 content blocks |
| `medium` | 2-3 components, moderate content density, 6-9 content blocks |
| `high` | 3 components, dense content, 9-12 content blocks |
| `too_high` | > 12 content blocks → **warning: suggest splitting into 2 slides** |

### Position Assignment Logic

For `two_column` layout:
- **Left:** Primary content (stats, bullets, text)
- **Right:** Supporting content (image, quote, secondary stats)

For `three_row` layout:
- **Top:** Title or key metric
- **Middle:** Main content (bullets, text)
- **Bottom:** Supporting info or CTA

For `sidebar_main` layout:
- **Left (sidebar):** Stats, quick facts
- **Right (main):** Narrative text, image

## LLM Prompt Guidelines

### System Prompt (Agent 2)

```
You are a Presentation Strategist for slide layout planning.

Your job is to:
1. Choose 1-3 components from the available component types
2. Map content blocks (from Agent 1) to components
3. Select a layout type
4. Assign positions to components
5. Plan image placement (if images are available)
6. Assess cognitive load

You do NOT:
- Write text (headings, bullets, captions)
- Generate HTML/Markdown
- Create new content (only use Agent 1's content blocks)
- Make detailed styling decisions

Design Principles:
- Max 3 components per slide (enforce strictly)
- Prioritize clarity over density
- Follow visual hierarchy (important content first)
- Consider cognitive load (aim for "low" or "medium")
- Use images strategically (proof, credibility, visual break)

Respond with a PartialBlueprint JSON structure.
```

### User Prompt Template

```
Plan the layout for this slide based on the content analysis:

CONTENT ANALYSIS (from Agent 1):
{content_analysis_json}

AVAILABLE COMPONENTS:
{available_components}

AVAILABLE LAYOUTS:
{available_layouts}

UPLOADED IMAGES:
{uploaded_images_json}

CONSTRAINTS:
- Max 3 components per slide
- Follow design system rules
- Aim for low-to-medium cognitive load

Provide a PartialBlueprint with:
- layout_type
- component_mappings (which components, in which positions, using which content blocks)
- cognitive_load_score
- reasoning (explain your choices)
- warnings (if any issues detected)
```

## Design System Rules (Enforced by Agent 2)

### Component Constraints

1. **Stat Grid:**
   - Requires 2-4 items
   - If < 2 items: Use text-block instead
   - If > 4 items: Split into stat-grid (top 4) + bullet-list (rest)

2. **Bullet List:**
   - Requires 2-6 items
   - If > 6 items: **Warning** (too much content)

3. **Quote:**
   - Requires exactly 1 quote block
   - If no quote in content: Don't use this component

4. **Image Frame:**
   - Requires at least 1 uploaded image
   - If no images: Don't use this component

5. **Text Block:**
   - Default for narrative content
   - Can split long text into 2 components if needed

### Layout Constraints

- **two_column:** Requires exactly 2 components
- **three_row:** Requires 2-3 components
- **single_column:** Works with 1-3 components
- **header_content:** Requires 2 components (header + content)

## Error Handling

### Warning Scenarios

1. **`too_many_components`** - Content suggests > 3 components
   - **Action:** Suggest splitting into 2 slides

2. **`cognitive_overload`** - Cognitive load score = `too_high`
   - **Action:** Simplify layout or suggest splitting content

3. **`missing_image`** - Content block references image not in uploaded list
   - **Action:** Skip image-frame, use text-only layout

4. **`incompatible_layout`** - Component count doesn't match layout
   - **Action:** Adjust layout or component selection

5. **`design_system_violation`** - Violates design system rules
   - **Action:** Apply fallback component choice

### Fallback Strategy

If Agent 2 encounters issues:
1. **First:** Try to simplify (remove least important component)
2. **Second:** Use `single_column` layout (most flexible)
3. **Last Resort:** Return warning + request user clarification

## Testing Strategy

### Unit Tests

1. **Component Selection**
   - Statistics input → stat_grid
   - List input → bullet_list
   - Mixed input → correct combination

2. **Layout Selection**
   - 1 component → single_column
   - 2 components → two_column
   - 3 components → three_row

3. **Image Placement**
   - Image available → image_frame included
   - No image → text-only layout

4. **Constraint Enforcement**
   - > 3 components → warning
   - Stat grid with 1 item → fallback to text_block

### Integration Tests

1. Agent 1 → Agent 2 handoff
2. Agent 2 → Agent 3 handoff (validate partial blueprint structure)

### Fixture Data

Create test fixtures in `presentation/api/tests/fixtures/agent2/`:
- `stats_two_column.json`
- `bullets_single_column.json`
- `mixed_with_image.json`
- `too_many_blocks_warning.json`

## Performance Targets

- **Response Time:** < 1 second (mostly deterministic logic, minimal LLM reasoning)
- **Token Usage:** < 300 tokens per plan (GPT-4o)
- **Accuracy:** 95%+ component selection correctness (manual validation)

## Version History

- **1.0** (2025-11-17) - Initial specification

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Agent 1 Specification](./agent-1-content-analyzer.md)
- [Agent 3 Specification](./agent-3-content-generator.md)
- [Template Inventory](./template-inventory.md)

# Template Inventory

**Version:** 1.0
**Status:** Draft
**Purpose:** Complete catalog of available templates for the renderer
**Last Updated:** 2025-11-17

## Overview

This document catalogs **all available templates** for the deterministic HTML renderer. These templates are the building blocks for slide generation.

## Template Categories

1. **Layout Templates** - Overall slide structure
2. **Component Templates** - Individual slide components
3. **Base Templates** - Foundation HTML structure
4. **Theme Files** - CSS styling per theme

## Layout Templates

Location: `presentation/api/renderer/templates/layouts/`

### 1. Single Column (`single_column.html`)

**Use Case:** 1-3 components stacked vertically

**Structure:**
```
┌─────────────────────┐
│  Title              │
│  Subtitle (opt)     │
├─────────────────────┤
│  Component 1        │
├─────────────────────┤
│  Component 2 (opt)  │
├─────────────────────┤
│  Component 3 (opt)  │
└─────────────────────┘
```

**Compatible Positions:**
- `full_width`
- `top`, `middle`, `bottom` (for 3 components)

**Best For:**
- Bullet lists
- Long text blocks
- Fullwidth images
- Single stat grids

---

### 2. Two Column (`two_column.html`)

**Use Case:** Side-by-side content (requires exactly 2 components)

**Structure:**
```
┌─────────────────────────────┐
│  Title       Subtitle (opt) │
├──────────────┬──────────────┤
│  Component 1 │ Component 2  │
│  (left)      │ (right)      │
└──────────────┴──────────────┘
```

**Compatible Positions:**
- `left`, `right` (exactly one of each)

**Best For:**
- Stats + Image
- Bullets + Image
- Text + Quote

**Common Patterns:**
- Left: Stat Grid → Right: Image Frame
- Left: Bullet List → Right: Image Frame
- Left: Text Block → Right: Quote

---

### 3. Three Row (`three_row.html`)

**Use Case:** Vertical stacking with emphasis (2-3 components)

**Structure:**
```
┌─────────────────────┐
│  Title              │
├─────────────────────┤
│  Component 1 (top)  │
├─────────────────────┤
│  Component 2 (mid)  │
├─────────────────────┤
│  Component 3 (bot)  │
└─────────────────────┘
```

**Compatible Positions:**
- `top`, `middle`, `bottom`

**Best For:**
- Process flows (step 1, 2, 3)
- Hierarchical content
- Multiple distinct sections

---

### 4. Header Content (`header_content.html`)

**Use Case:** Large header component + main content below (requires exactly 2 components)

**Structure:**
```
┌─────────────────────┐
│  Title              │
├─────────────────────┤
│  Component 1        │
│  (header - large)   │
├─────────────────────┤
│  Component 2        │
│  (content - main)   │
└─────────────────────┘
```

**Compatible Positions:**
- `top` (header component)
- `full_width` or `bottom` (content component)

**Best For:**
- Key stat + details below
- Quote + context
- Image hero + description

---

### 5. Sidebar Main (`sidebar_main.html`)

**Use Case:** Sidebar (30%) + main content (70%) - 2 components

**Structure:**
```
┌─────────────────────────────┐
│  Title                      │
├──────┬──────────────────────┤
│ Comp │  Component 2         │
│  1   │  (main - wide)       │
│(side)│                      │
└──────┴──────────────────────┘
```

**Compatible Positions:**
- `left` (sidebar - 30% width)
- `right` (main - 70% width)

**Best For:**
- Stats sidebar + narrative text
- Quick facts + image
- Timeline + description

---

## Component Templates

Location: `presentation/api/renderer/templates/components/`

### 1. Stat Grid (`stat_grid.html`)

**Purpose:** Display 2-4 statistics with labels

**Required Fields:**
- `items` (list, 2-4 items)
  - `value` (string)
  - `label` (string)
  - `unit` (optional string)
  - `sublabel` (optional string)
  - `emphasis` (boolean)
- `layout` (string: `2x1`, `2x2`, `3x1`, `4x1`)

**Optional Fields:**
- `title` (string)

**Example Blueprint:**
```json
{
  "type": "stat_grid",
  "content": {
    "title": null,
    "items": [
      {"value": "5", "label": "Experten", "emphasis": true},
      {"value": "20", "label": "Jahre", "unit": "Jahre"}
    ],
    "layout": "2x1"
  }
}
```

**Visual:**
```
┌──────────┬──────────┐
│    5     │   20     │
│ Experten │  Jahre   │
└──────────┴──────────┘
```

**Variants:**
- **2x1:** 2 items, horizontal
- **2x2:** 4 items, 2x2 grid
- **3x1:** 3 items, horizontal
- **4x1:** 4 items, horizontal (may wrap on mobile)

---

### 2. Bullet List (`bullet_list.html`)

**Purpose:** Display 2-6 bullet points

**Required Fields:**
- `items` (list, 2-6 items)
  - `text` (string, max 120 chars)
  - `level` (int: 1, 2, or 3)
  - `icon` (optional string - emoji or name)
  - `emphasis` (boolean)
- `style` (string: `default`, `checkmarks`, `arrows`, `numbers`)

**Optional Fields:**
- `title` (string)

**Example Blueprint:**
```json
{
  "type": "bullet_list",
  "content": {
    "title": "Herausforderungen",
    "items": [
      {"text": "Manuelle Prozesse kosten 40% der Zeit", "level": 1, "icon": "⏱️"},
      {"text": "Fehlerquote über 15%", "level": 1, "icon": "⚠️"}
    ],
    "style": "default"
  }
}
```

**Visual:**
```
Herausforderungen
• ⏱️ Manuelle Prozesse kosten 40% der Zeit
• ⚠️ Fehlerquote über 15%
```

**Style Variants:**
- **default:** Standard bullets (•)
- **checkmarks:** Checkmarks (✓)
- **arrows:** Arrows (→)
- **numbers:** Numbered list (1., 2., ...)

---

### 3. Quote (`quote.html`)

**Purpose:** Display a quote with attribution

**Required Fields:**
- `quote_text` (string, max 300 chars)

**Optional Fields:**
- `author` (string)
- `author_title` (string)
- `source` (string)
- `style` (string: `default`, `highlighted`, `testimonial`)

**Example Blueprint:**
```json
{
  "type": "quote",
  "content": {
    "quote_text": "Robo4you hat unsere Effizienz um 60% gesteigert.",
    "author": "Dr. Maria Schmidt",
    "author_title": "CTO, AutoTech GmbH",
    "source": "Kundeninterview, März 2025",
    "style": "highlighted"
  }
}
```

**Visual:**
```
┌─────────────────────────────────────┐
│ "Robo4you hat unsere Effizienz um  │
│  60% gesteigert."                   │
│                                     │
│ — Dr. Maria Schmidt                 │
│   CTO, AutoTech GmbH                │
└─────────────────────────────────────┘
```

**Style Variants:**
- **default:** Simple quote with border
- **highlighted:** Large text, background color
- **testimonial:** Photo placeholder + quote

---

### 4. Text Block (`text_block.html`)

**Purpose:** Display 1-3 paragraphs of text

**Required Fields:**
- `paragraphs` (list, 1-3 strings)

**Optional Fields:**
- `title` (string)
- `emphasis_phrases` (list of strings to bold)
- `text_align` (string: `left`, `center`, `right`)

**Example Blueprint:**
```json
{
  "type": "text_block",
  "content": {
    "title": "Unsere Mission",
    "paragraphs": [
      "Wir entwickeln intelligente Robotiklösungen für die Industrie.",
      "Unsere Technologie kombiniert KI, Computer Vision und Sensorik."
    ],
    "emphasis_phrases": ["intelligente Robotiklösungen", "KI"],
    "text_align": "left"
  }
}
```

**Visual:**
```
Unsere Mission

Wir entwickeln **intelligente Robotiklösungen**
für die Industrie.

Unsere Technologie kombiniert **KI**, Computer
Vision und Sensorik.
```

---

### 5. Image Frame (`image_frame.html`)

**Purpose:** Display images with standardized framing

**See:** [Image Frame Specification](./image-frame-specification.md) for full details

**Variants:**
- `single` - Single image with title/caption
- `gallery_2` - 2 images side-by-side
- `gallery_3` - 3 images in grid
- `fullwidth` - Hero image (full width)

**Example Blueprint (Single):**
```json
{
  "type": "image_frame",
  "content": {
    "image_id": "team.png",
    "image_path": "projects/robo4you/images/uploads/team.png",
    "title": "Unser Team",
    "caption": "5 Experten mit 20+ Jahren Erfahrung",
    "alt_text": "Gruppenfoto der fünf Teammitglieder",
    "frame_variant": "single",
    "aspect_ratio": "16:9"
  }
}
```

---

### 6. Process Chain (`process_chain.html`) *[Future]*

**Purpose:** Display step-by-step process (3-5 steps)

**Status:** Planned for v1.1

**Example:**
```
Step 1        Step 2        Step 3
  ↓             ↓             ↓
[Icon]        [Icon]        [Icon]
Analyze       Plan          Execute
```

---

### 7. Table (`table.html`) *[Future]*

**Purpose:** Display tabular data

**Status:** Planned for v1.1

**Example:**
```
┌─────────┬─────────┬─────────┐
│ Feature │ Plan A  │ Plan B  │
├─────────┼─────────┼─────────┤
│ Users   │ 10      │ 100     │
│ Storage │ 1 GB    │ 10 GB   │
└─────────┴─────────┴─────────┘
```

---

## Base Template

Location: `presentation/api/renderer/templates/base.html`

**Purpose:** Foundation HTML structure for all slides

**Key Elements:**
- `<head>` with meta tags, CSS links
- Theme CSS loading (`styles/{{ theme }}/style.css`)
- `<body>` with `.slide-container` wrapper
- Optional metadata footer
- Extensible blocks for layout templates

**Usage:**
All layout templates extend `base.html`:

```html
{% extends "base.html" %}

{% block layout %}
  <!-- Layout-specific content here -->
{% endblock %}
```

---

## Theme Files

Location: `presentation/projects/{project}/styles/{theme}/`

### Available Themes

1. **GitHub Design** (`github/`)
   - Colors: Green accent (#238636), clean grays
   - Style: Professional, subtle shadows
   - Font: System fonts (sans-serif)

2. **Modern** (`modern/`)
   - Colors: Vibrant blues, bold contrasts
   - Style: Contemporary, large shadows
   - Font: Modern sans-serif

3. **Minimal** (`minimal/`)
   - Colors: Black & white, minimal accents
   - Style: Clean lines, no borders/shadows
   - Font: Lightweight sans-serif

### Theme File Structure

Each theme has:
```
styles/{theme}/
├── style.css           # Main stylesheet
├── variables.css       # CSS custom properties
└── components/         # Component-specific overrides (optional)
    ├── stat_grid.css
    ├── bullet_list.css
    └── image_frame.css
```

---

## Component Compatibility Matrix

| Component       | Works with Layout          | Notes                        |
|-----------------|----------------------------|------------------------------|
| `stat_grid`     | All layouts                | Best in `two_column` (left)  |
| `bullet_list`   | All layouts                | Best in `single_column`      |
| `quote`         | All layouts                | Best in `two_column` (right) |
| `text_block`    | All layouts                | Avoid in `sidebar_main`      |
| `image_frame`   | All layouts                | `fullwidth` requires `single_column` |
| `process_chain` | `single_column`, `three_row` | Requires horizontal space   |
| `table`         | `single_column`, `header_content` | Needs full width         |

---

## Template Selection Rules

### For Agent 2 (Presentation Strategist)

When planning layouts, Agent 2 must follow these rules:

**Component Count → Layout:**
- **1 component:** `single_column` or `header_content`
- **2 components:** `two_column`, `header_content`, or `sidebar_main`
- **3 components:** `three_row` or `single_column`

**Content Type → Component:**
- **Statistics (2-4 items):** `stat_grid`
- **Bullet points (2-6):** `bullet_list`
- **Quote:** `quote`
- **Narrative text:** `text_block`
- **Images:** `image_frame` (choose variant based on image count)

**Position Constraints:**
- `two_column` requires exactly: 1x `left`, 1x `right`
- `three_row` requires: `top`, `middle`, `bottom` (or subset)
- `header_content` requires: 1x `top`, 1x `bottom` or `full_width`

---

## Template Versioning

### Schema Version in Templates

Templates check `schema_version` from blueprint:

```html
{# Check schema version #}
{% if blueprint.schema_version == "1.0" %}
  {# Use v1.0 template logic #}
{% elif blueprint.schema_version == "1.1" %}
  {# Use v1.1 template logic with new features #}
{% endif %}
```

### Backward Compatibility

- **v1.0 templates:** Always supported
- **v1.1 templates:** Support v1.0 blueprints (graceful degradation)
- **v2.0 templates:** May break compatibility (major version bump)

---

## Adding New Templates

### Checklist for New Component Templates

1. **Define Pydantic Schema** in `blueprints/models.py`
2. **Create Jinja2 Template** in `renderer/templates/components/{name}.html`
3. **Add CSS Styles** in `styles/{theme}/components/{name}.css` (for each theme)
4. **Update Template Inventory** (this document)
5. **Write Unit Tests** in `tests/test_renderer.py`
6. **Update Agent 2 Prompts** to include new component type
7. **Add Example Blueprints** in `tests/fixtures/blueprints/`

### Example: Adding a "Timeline" Component

1. **Schema:**
```python
class TimelineContent(BaseModel):
    events: List[TimelineEvent] = Field(..., min_items=3, max_items=5)
    orientation: Literal["horizontal", "vertical"] = "horizontal"
```

2. **Template:**
```html
{# templates/components/timeline.html #}
<div class="component timeline orientation-{{ component.content.orientation }}">
  {% for event in component.content.events %}
  <div class="timeline-event">
    <div class="event-date">{{ event.date }}</div>
    <div class="event-title">{{ event.title }}</div>
  </div>
  {% endfor %}
</div>
```

3. **CSS:**
```css
/* styles/github/components/timeline.css */
.timeline { display: flex; gap: 1rem; }
.timeline-event { flex: 1; }
```

4. **Update this doc:**
Add entry under "Component Templates" section.

---

## Testing Templates

### Unit Test Example

```python
def test_stat_grid_renders_correctly():
    """Test stat grid template with 2x2 layout"""
    blueprint = {
        "type": "stat_grid",
        "component_id": "comp-1",
        "position": "left",
        "content": {
            "items": [
                {"value": "5", "label": "Experten"},
                {"value": "20", "label": "Jahre"}
            ],
            "layout": "2x1"
        }
    }

    renderer = SlideRenderer(templates_dir="...")
    html = renderer._render_component(blueprint, theme="github")

    # Assertions
    assert 'class="stat-grid"' in html
    assert 'layout-2x1' in html
    assert '<div class="stat-value">5</div>' in html
    assert '<div class="stat-label">Experten</div>' in html
```

---

## Quick Reference

### Template Files

| File Path | Purpose | Status |
|-----------|---------|--------|
| `layouts/single_column.html` | 1-3 stacked components | ✅ v1.0 |
| `layouts/two_column.html` | Side-by-side (2 comp) | ✅ v1.0 |
| `layouts/three_row.html` | Vertical 3-tier | ✅ v1.0 |
| `layouts/header_content.html` | Header + content | ✅ v1.0 |
| `layouts/sidebar_main.html` | Sidebar (30%) + main (70%) | ✅ v1.0 |
| `components/stat_grid.html` | Statistics grid | ✅ v1.0 |
| `components/bullet_list.html` | Bullet points | ✅ v1.0 |
| `components/quote.html` | Quotes | ✅ v1.0 |
| `components/text_block.html` | Paragraphs | ✅ v1.0 |
| `components/image_frame.html` | Images (4 variants) | ✅ v1.0 |
| `components/process_chain.html` | Step-by-step process | 🔜 v1.1 |
| `components/table.html` | Tabular data | 🔜 v1.1 |
| `base.html` | Foundation | ✅ v1.0 |

---

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Renderer Specification](./renderer-specification.md)
- [Image Frame Specification](./image-frame-specification.md)
- [Agent 2 Specification](./agent-2-presentation-strategist.md) (uses this inventory to plan layouts)

---

## Version History

- **1.0** (2025-11-17) - Initial inventory (5 layouts, 5 components)
- **1.1** (Planned) - Add process_chain, table components

---

**End of Template Inventory**

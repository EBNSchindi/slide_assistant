# Renderer Specification

**Version:** 1.0
**Status:** Draft
**Component:** Deterministic HTML Renderer (No LLM)
**Last Updated:** 2025-11-17

## Mission Statement

**"Ich setze den Text-Blueprint in HTML/CSS um, exakt nach Design-System – völlig ohne LLM."**

The Renderer is a **pure Python function** that takes a CompleteBlueprint (JSON) and produces HTML + Markdown output. It uses fixed templates and never calls an LLM.

## Core Principles

1. **Deterministic:** Same Blueprint → Same HTML (always)
2. **LLM-Free:** Zero API calls, pure template-based rendering
3. **Template-Driven:** All HTML comes from predefined templates
4. **Design-System Compliant:** Enforces design rules automatically
5. **Fast:** Renders in milliseconds (no network calls)

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────┐
│  Input: CompleteBlueprint (JSON)    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  1. Validate Blueprint               │
│     - Schema version check          │
│     - Required fields present       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  2. Load Layout Template            │
│     - Based on layout_type          │
│     - e.g., two_column.html         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  3. Render Each Component           │
│     - Select component template     │
│     - Fill placeholders             │
│     - Apply styling                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  4. Assemble Slide HTML             │
│     - Insert components into layout │
│     - Add slide title/subtitle      │
│     - Inject metadata (optional)    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  5. Generate Markdown (optional)    │
│     - Mirror HTML structure         │
│     - For archival/editing          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Output:                            │
│  - HTML string                      │
│  - Markdown string (optional)       │
│  - Metadata (component count, etc.) │
└─────────────────────────────────────┘
```

## Implementation Structure

### File Organization

```
presentation/api/
├── renderer/
│   ├── __init__.py
│   ├── renderer.py                    # Main renderer class
│   ├── validator.py                   # Blueprint validation
│   ├── templates/                     # HTML templates
│   │   ├── layouts/                   # Layout templates
│   │   │   ├── single_column.html
│   │   │   ├── two_column.html
│   │   │   ├── three_row.html
│   │   │   ├── header_content.html
│   │   │   └── sidebar_main.html
│   │   ├── components/                # Component templates
│   │   │   ├── stat_grid.html
│   │   │   ├── bullet_list.html
│   │   │   ├── quote.html
│   │   │   ├── text_block.html
│   │   │   ├── image_frame.html
│   │   │   ├── process_chain.html
│   │   │   └── table.html
│   │   └── base.html                  # Base slide structure
│   └── markdown_generator.py          # Markdown generation (optional)
```

### Main Renderer Class

```python
from typing import Dict, Tuple
from jinja2 import Environment, FileSystemLoader
from pydantic import ValidationError

class SlideRenderer:
    """Deterministic HTML renderer for slide blueprints"""

    def __init__(self, templates_dir: str):
        """
        Initialize renderer with template directory.

        Args:
            templates_dir: Path to templates directory
        """
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.validator = BlueprintValidator()

    def render(
        self,
        blueprint: Dict,
        theme: str = "github"
    ) -> Tuple[str, str, Dict]:
        """
        Render a blueprint to HTML and Markdown.

        Args:
            blueprint: CompleteBlueprint as dict
            theme: Design theme (github, modern, minimal)

        Returns:
            Tuple of (html_string, markdown_string, metadata)

        Raises:
            ValidationError: If blueprint is invalid
            TemplateNotFoundError: If required template missing
        """
        # 1. Validate
        validated_blueprint = self.validator.validate(blueprint)

        # 2. Load layout template
        layout_template = self._load_layout_template(
            validated_blueprint.layout_type
        )

        # 3. Render components
        rendered_components = []
        for component in validated_blueprint.components:
            html = self._render_component(component, theme)
            rendered_components.append(html)

        # 4. Assemble slide
        html = self._assemble_slide(
            layout_template,
            validated_blueprint,
            rendered_components,
            theme
        )

        # 5. Generate markdown (optional)
        markdown = self._generate_markdown(validated_blueprint)

        # 6. Metadata
        metadata = {
            "component_count": len(validated_blueprint.components),
            "layout_type": validated_blueprint.layout_type,
            "theme": theme,
            "render_timestamp": datetime.now().isoformat()
        }

        return html, markdown, metadata

    def _render_component(self, component: ComponentBlueprint, theme: str) -> str:
        """Render a single component using its template"""
        template_name = f"components/{component.type}.html"
        template = self.env.get_template(template_name)

        return template.render(
            component=component,
            theme=theme
        )

    def _assemble_slide(
        self,
        layout_template,
        blueprint,
        components,
        theme
    ) -> str:
        """Assemble final slide HTML"""
        return layout_template.render(
            title=blueprint.slide_title,
            subtitle=blueprint.slide_subtitle,
            components=components,
            theme=theme,
            metadata=blueprint.metadata
        )
```

## Template System

### Jinja2 Template Engine

**Why Jinja2?**
- Industry-standard Python templating
- Clear separation of logic and presentation
- Easy to test and maintain
- No LLM needed

### Template Variables

All templates receive:
- `component`: ComponentBlueprint object
- `theme`: Theme name (string)
- Additional context as needed

### Template Inheritance

```
base.html
  ↓
layouts/two_column.html
  ↓ (includes)
components/stat_grid.html
components/image_frame.html
```

## Component Templates

### Example: Stat Grid Template

**File:** `templates/components/stat_grid.html`

```html
{# Stat Grid Component Template #}
<div class="component stat-grid" id="{{ component.component_id }}">
  {% if component.content.title %}
  <h3 class="stat-grid-title">{{ component.content.title }}</h3>
  {% endif %}

  <div class="stat-grid-items layout-{{ component.content.layout }}">
    {% for item in component.content.items %}
    <div class="stat-item {% if item.emphasis %}stat-item-emphasis{% endif %}">
      <div class="stat-value">
        {{ item.value }}{% if item.unit %}<span class="stat-unit">{{ item.unit }}</span>{% endif %}
      </div>
      <div class="stat-label">{{ item.label }}</div>
      {% if item.sublabel %}
      <div class="stat-sublabel">{{ item.sublabel }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
</div>
```

**CSS Classes:**
- `.component` - Base class for all components
- `.stat-grid` - Component type
- `.stat-grid-items` - Container for items
- `.layout-2x2`, `.layout-2x1`, etc. - Grid layout variants
- `.stat-item` - Individual stat
- `.stat-item-emphasis` - Emphasized stat

### Example: Image Frame Template

**File:** `templates/components/image_frame.html`

```html
{# Image Frame Component Template #}
<div class="component image-frame frame-variant-{{ component.content.frame_variant }}" id="{{ component.component_id }}">
  <div class="image-container aspect-ratio-{{ component.content.aspect_ratio }}">
    <img
      src="{{ component.content.image_path }}"
      alt="{{ component.content.alt_text }}"
      class="frame-image"
      loading="lazy"
    />
  </div>

  {% if component.content.title or component.content.caption %}
  <div class="image-text">
    {% if component.content.title %}
    <h3 class="image-title">{{ component.content.title }}</h3>
    {% endif %}

    {% if component.content.caption %}
    <p class="image-caption">{{ component.content.caption }}</p>
    {% endif %}
  </div>
  {% endif %}
</div>
```

**Frame Variants:**
- `frame-variant-single` - Single image
- `frame-variant-gallery_2` - 2-image gallery
- `frame-variant-gallery_3` - 3-image gallery
- `frame-variant-fullwidth` - Full-width hero image

### Example: Bullet List Template

**File:** `templates/components/bullet_list.html`

```html
{# Bullet List Component Template #}
<div class="component bullet-list bullet-style-{{ component.content.style }}" id="{{ component.component_id }}">
  {% if component.content.title %}
  <h3 class="bullet-list-title">{{ component.content.title }}</h3>
  {% endif %}

  <ul class="bullet-items">
    {% for item in component.content.items %}
    <li class="bullet-item level-{{ item.level }} {% if item.emphasis %}bullet-emphasis{% endif %}">
      {% if item.icon %}
      <span class="bullet-icon">{{ item.icon }}</span>
      {% endif %}
      <span class="bullet-text">{{ item.text }}</span>
    </li>
    {% endfor %}
  </ul>
</div>
```

**Bullet Styles:**
- `bullet-style-default` - Standard bullets
- `bullet-style-checkmarks` - Checkmark bullets
- `bullet-style-arrows` - Arrow bullets
- `bullet-style-numbers` - Numbered list

## Layout Templates

### Example: Two-Column Layout

**File:** `templates/layouts/two_column.html`

```html
{% extends "base.html" %}

{% block layout %}
<div class="layout-two-column">
  <div class="layout-header">
    <h1 class="slide-title">{{ title }}</h1>
    {% if subtitle %}
    <h2 class="slide-subtitle">{{ subtitle }}</h2>
    {% endif %}
  </div>

  <div class="layout-content">
    <div class="column column-left">
      {{ components[0] | safe }}
    </div>

    <div class="column column-right">
      {{ components[1] | safe }}
    </div>
  </div>
</div>
{% endblock %}
```

### Example: Single Column Layout

**File:** `templates/layouts/single_column.html`

```html
{% extends "base.html" %}

{% block layout %}
<div class="layout-single-column">
  <div class="layout-header">
    <h1 class="slide-title">{{ title }}</h1>
    {% if subtitle %}
    <h2 class="slide-subtitle">{{ subtitle }}</h2>
    {% endif %}
  </div>

  <div class="layout-content">
    {% for component in components %}
    <div class="component-wrapper">
      {{ component | safe }}
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

## Base Template

**File:** `templates/base.html`

```html
<!DOCTYPE html>
<html lang="{{ language }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>

  {# Theme CSS #}
  <link rel="stylesheet" href="../styles/{{ theme }}/style.css">

  {# Component-specific CSS (if needed) #}
  {% block extra_css %}{% endblock %}
</head>
<body class="slide-view theme-{{ theme }}">
  <div class="slide-container" id="{{ slide_id }}">
    {% block layout %}
    {# Layout template extends this #}
    {% endblock %}
  </div>

  {# Optional metadata footer #}
  {% if metadata and metadata.show_in_html %}
  <div class="slide-metadata">
    <small>Created: {{ metadata.created_at }} | Density: {{ metadata.content_density }}</small>
  </div>
  {% endif %}

  {% block extra_js %}{% endblock %}
</body>
</html>
```

## Validation

### Blueprint Validator

```python
from pydantic import ValidationError

class BlueprintValidator:
    """Validates blueprints before rendering"""

    def validate(self, blueprint_dict: Dict) -> SlideBlueprint:
        """
        Validate blueprint structure.

        Raises:
            ValidationError: If blueprint is invalid
        """
        try:
            blueprint = SlideBlueprint(**blueprint_dict)
        except ValidationError as e:
            raise RendererValidationError(f"Invalid blueprint: {e}")

        # Additional validation
        self._validate_schema_version(blueprint)
        self._validate_component_positions(blueprint)
        self._validate_image_paths(blueprint)

        return blueprint

    def _validate_schema_version(self, blueprint: SlideBlueprint):
        """Check schema version compatibility"""
        supported_versions = ["1.0", "1.1"]
        if blueprint.schema_version not in supported_versions:
            raise RendererValidationError(
                f"Unsupported schema version: {blueprint.schema_version}"
            )

    def _validate_component_positions(self, blueprint: SlideBlueprint):
        """Ensure positions are compatible with layout"""
        layout = blueprint.layout_type
        positions = [c.position for c in blueprint.components]

        # Example: two_column requires exactly 2 components with left/right positions
        if layout == LayoutType.TWO_COLUMN:
            if len(blueprint.components) != 2:
                raise RendererValidationError(
                    f"two_column layout requires 2 components, got {len(blueprint.components)}"
                )
            if set(positions) != {"left", "right"}:
                raise RendererValidationError(
                    f"two_column layout requires 'left' and 'right' positions, got {positions}"
                )

    def _validate_image_paths(self, blueprint: SlideBlueprint):
        """Check that image paths exist (optional, can be disabled)"""
        from pathlib import Path

        for component in blueprint.components:
            if component.type == ComponentType.IMAGE_FRAME:
                image_path = Path(component.content["image_path"])
                if not image_path.exists():
                    # Log warning but don't fail (image might not be uploaded yet)
                    logger.warning(f"Image not found: {image_path}")
```

## Markdown Generation

### Optional Markdown Output

The renderer can also generate Markdown alongside HTML:

```python
def _generate_markdown(self, blueprint: SlideBlueprint) -> str:
    """Generate markdown representation of slide"""
    md = f"# {blueprint.slide_title}\n\n"

    if blueprint.slide_subtitle:
        md += f"*{blueprint.slide_subtitle}*\n\n"

    for component in blueprint.components:
        md += self._component_to_markdown(component)
        md += "\n\n"

    return md

def _component_to_markdown(self, component: ComponentBlueprint) -> str:
    """Convert component to markdown"""
    if component.type == ComponentType.STAT_GRID:
        return self._stat_grid_to_markdown(component.content)
    elif component.type == ComponentType.BULLET_LIST:
        return self._bullet_list_to_markdown(component.content)
    elif component.type == ComponentType.IMAGE_FRAME:
        return self._image_frame_to_markdown(component.content)
    # ... etc.
```

### Example Markdown Output

```markdown
# Unser Team

*Expertise trifft Innovation*

## Team Expertise

- **5** Robotik-Experten
- **20+ Jahre** Branchenerfahrung

![Unser Kernteam](projects/robo4you/images/uploads/teamfoto.png)
*Führende Experten für Robotik, KI und Automatisierung*
```

## Usage

### Standalone Rendering

```python
from presentation.api.renderer import SlideRenderer

# Initialize renderer
renderer = SlideRenderer(templates_dir="presentation/api/renderer/templates")

# Load blueprint
with open("blueprints/slide-03-team.json") as f:
    blueprint = json.load(f)

# Render
html, markdown, metadata = renderer.render(blueprint, theme="github")

# Save outputs
with open("html/slide-03-team.html", "w") as f:
    f.write(html)

with open("markdown/optimized/slide-03-team.md", "w") as f:
    f.write(markdown)
```

### CLI Usage

```bash
# Render single blueprint
python -m presentation.api.renderer.cli render blueprints/slide-03-team.json output/

# Batch render
python -m presentation.api.renderer.cli batch blueprints/ output/

# Specify theme
python -m presentation.api.renderer.cli render blueprint.json output/ --theme modern
```

## Testing

### Unit Tests

1. **Template Rendering:**
   - Test each component template with fixture data
   - Verify correct HTML structure
   - Check CSS classes applied correctly

2. **Layout Rendering:**
   - Test each layout template
   - Verify component positioning
   - Check responsive structure

3. **Validation:**
   - Valid blueprints pass
   - Invalid blueprints raise errors
   - Schema version checking

### Integration Tests

1. **Full Pipeline:**
   - Blueprint → HTML → Parse → Validate structure

2. **Theme Switching:**
   - Same blueprint renders correctly in all themes

3. **Markdown Generation:**
   - HTML and Markdown outputs are consistent

### Test Fixtures

```
tests/fixtures/renderer/
├── blueprints/
│   ├── valid_two_column.json
│   ├── valid_single_column.json
│   └── invalid_missing_title.json
├── expected_html/
│   ├── two_column_github.html
│   └── single_column_modern.html
└── expected_markdown/
    └── team_slide.md
```

## Performance Targets

- **Render Time:** < 50ms per slide (Python)
- **Memory:** < 10MB per render
- **Throughput:** 100+ slides/second (batch mode)

## Error Handling

### Error Types

1. **ValidationError:** Invalid blueprint structure
2. **TemplateNotFoundError:** Missing template file
3. **ImageNotFoundError:** Referenced image doesn't exist
4. **SchemaVersionError:** Unsupported schema version

### Error Messages

All errors include:
- Clear description of issue
- Offending field/component
- Suggested fix

Example:
```
RendererValidationError: two_column layout requires 2 components, got 3

Blueprint: slide-05-team
Layout: two_column
Components found: 3

Suggestion: Use three_row layout instead, or remove one component.
```

## Version History

- **1.0** (2025-11-17) - Initial specification

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Template Inventory](./template-inventory.md)
- [Image Frame Specification](./image-frame-specification.md)
- [Agent 3 Specification](./agent-3-content-generator.md) (produces input for Renderer)

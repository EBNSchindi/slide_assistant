# Image Frame Specification

**Version:** 1.0
**Status:** Draft
**Component Type:** `image_frame`
**Last Updated:** 2025-11-17

## Purpose

The **Image Frame** is a standardized component for displaying images in slides. It ensures consistent visual presentation regardless of which agent or LLM generated the content.

## Design Principles

1. **Consistency:** All images appear in the same frame structure
2. **Flexibility:** Multiple variants for different use cases
3. **Accessibility:** Alt texts required, ARIA labels included
4. **Responsive:** Adapts to different screen sizes
5. **Template-Based:** All variants are predefined templates (no LLM-generated HTML)

## Component Structure

### Base Elements

Every image frame contains:

1. **Image Container:** Wrapper with aspect ratio control
2. **Image Element:** `<img>` tag with src, alt, loading attributes
3. **Text Container (optional):** Title + caption below image
4. **Frame Border/Shadow (optional):** Visual styling per theme

### HTML Structure (Conceptual)

```html
<div class="component image-frame frame-variant-{variant}">
  <!-- Image container with aspect ratio -->
  <div class="image-container aspect-ratio-{ratio}">
    <img
      src="{image_path}"
      alt="{alt_text}"
      class="frame-image"
      loading="lazy"
    />
  </div>

  <!-- Optional text container -->
  <div class="image-text">
    <h3 class="image-title">{title}</h3>
    <p class="image-caption">{caption}</p>
  </div>
</div>
```

## Frame Variants

### 1. Single Image (`frame-variant-single`)

**Use Case:** Primary image with descriptive text

**Structure:**
- Single image (any aspect ratio)
- Optional title above or below image
- Optional caption below title

**Blueprint Example:**

```json
{
  "component_id": "comp-2",
  "type": "image_frame",
  "position": "right",
  "content": {
    "image_id": "teamfoto.png",
    "image_path": "projects/robo4you/images/uploads/teamfoto.png",
    "title": "Unser Kernteam",
    "caption": "Führende Experten für Robotik und KI",
    "alt_text": "Gruppenfoto von fünf Teammitgliedern vor dem Bürogebäude",
    "frame_variant": "single",
    "aspect_ratio": "16:9"
  }
}
```

**Visual Layout:**

```
┌─────────────────────────┐
│                         │
│      [IMAGE]            │
│                         │
├─────────────────────────┤
│ Title: "Unser Kernteam" │
│ Caption: "Führende..."  │
└─────────────────────────┘
```

### 2. Gallery (2 Images) (`frame-variant-gallery_2`)

**Use Case:** Compare two images side-by-side (e.g., before/after, desktop/mobile)

**Structure:**
- Two images in horizontal layout (50/50 split)
- Optional shared title above
- Individual captions per image

**Blueprint Example:**

```json
{
  "component_id": "comp-1",
  "type": "image_frame",
  "position": "full_width",
  "content": {
    "frame_variant": "gallery_2",
    "title": "Vorher / Nachher",
    "images": [
      {
        "image_id": "before.png",
        "image_path": "projects/robo4you/images/uploads/before.png",
        "caption": "Vorher: Manuelle Prozesse",
        "alt_text": "Screenshot des alten manuellen Workflows"
      },
      {
        "image_id": "after.png",
        "image_path": "projects/robo4you/images/uploads/after.png",
        "caption": "Nachher: Automatisiert",
        "alt_text": "Screenshot des automatisierten Workflows mit Robotik"
      }
    ],
    "aspect_ratio": "16:9"
  }
}
```

**Visual Layout:**

```
┌─────────────────────────────────────┐
│      Title: "Vorher / Nachher"      │
├─────────────────┬───────────────────┤
│   [IMAGE 1]     │    [IMAGE 2]      │
│                 │                   │
├─────────────────┼───────────────────┤
│ Caption 1       │ Caption 2         │
└─────────────────┴───────────────────┘
```

### 3. Gallery (3 Images) (`frame-variant-gallery_3`)

**Use Case:** Show multiple related images (e.g., product views, team photos, feature screenshots)

**Structure:**
- Three images in grid layout (varies by theme)
  - **Option A:** 2 top, 1 bottom (larger)
  - **Option B:** 3 horizontal (equal size)
- Optional shared title
- Individual captions per image

**Blueprint Example:**

```json
{
  "component_id": "comp-1",
  "type": "image_frame",
  "position": "full_width",
  "content": {
    "frame_variant": "gallery_3",
    "title": "Unsere Standorte",
    "images": [
      {
        "image_id": "berlin.png",
        "image_path": "projects/robo4you/images/uploads/berlin.png",
        "caption": "Berlin",
        "alt_text": "Büro in Berlin-Mitte"
      },
      {
        "image_id": "munich.png",
        "image_path": "projects/robo4you/images/uploads/munich.png",
        "caption": "München",
        "alt_text": "Büro in München-Schwabing"
      },
      {
        "image_id": "hamburg.png",
        "image_path": "projects/robo4you/images/uploads/hamburg.png",
        "caption": "Hamburg",
        "alt_text": "Büro in Hamburg-Altona"
      }
    ],
    "aspect_ratio": "4:3"
  }
}
```

**Visual Layout (Option A - 2+1):**

```
┌──────────────────────────────────────┐
│      Title: "Unsere Standorte"       │
├──────────────────┬───────────────────┤
│   [IMAGE 1]      │   [IMAGE 2]       │
│   Caption 1      │   Caption 2       │
├──────────────────┴───────────────────┤
│         [IMAGE 3 - larger]           │
│         Caption 3                    │
└──────────────────────────────────────┘
```

**Visual Layout (Option B - 3 horizontal):**

```
┌──────────────────────────────────────────────────┐
│         Title: "Unsere Standorte"                │
├──────────────┬─────────────┬─────────────────────┤
│  [IMAGE 1]   │  [IMAGE 2]  │   [IMAGE 3]         │
│  Caption 1   │  Caption 2  │   Caption 3         │
└──────────────┴─────────────┴─────────────────────┘
```

### 4. Fullwidth Hero (`frame-variant-fullwidth`)

**Use Case:** Large hero image (product shot, landscape, logo)

**Structure:**
- Full-width image (no padding)
- Optional overlay text (title/caption on top of image)
- No border/shadow

**Blueprint Example:**

```json
{
  "component_id": "comp-1",
  "type": "image_frame",
  "position": "full_width",
  "content": {
    "image_id": "product_hero.png",
    "image_path": "projects/robo4you/images/uploads/product_hero.png",
    "title": "Robo4you Platform",
    "caption": null,
    "alt_text": "Robo4you Robotik-Plattform in industrieller Produktionsumgebung",
    "frame_variant": "fullwidth",
    "aspect_ratio": "16:9",
    "overlay_text": true
  }
}
```

**Visual Layout:**

```
┌──────────────────────────────────────┐
│                                      │
│         [LARGE IMAGE]                │
│                                      │
│  Title: "Robo4you Platform"          │ ← Overlaid on image
│                                      │
└──────────────────────────────────────┘
```

## Content Schema

### ImageFrameContent (Pydantic Model)

Already defined in [Blueprint Schema](./blueprint-schema.md), repeated here for convenience:

```python
class ImageFrameContent(BaseModel):
    """Content for image-frame component"""

    # Single image variant
    image_id: Optional[str] = Field(None, description="Image filename (single variant)")
    image_path: Optional[str] = Field(None, description="Relative path (single variant)")

    # Gallery variant
    images: Optional[List["GalleryImage"]] = Field(None, description="List of images (gallery variants)")

    # Text content
    title: Optional[str] = Field(None, max_length=60, description="Image title")
    caption: Optional[str] = Field(None, max_length=200, description="Image caption")
    alt_text: Optional[str] = Field(None, max_length=150, description="Accessibility alt text (required for single)")

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
    overlay_text: bool = Field(default=False, description="Show title as overlay (fullwidth only)")

class GalleryImage(BaseModel):
    """Single image in a gallery"""
    image_id: str = Field(..., description="Image filename")
    image_path: str = Field(..., description="Relative path to image")
    caption: Optional[str] = Field(None, max_length=100, description="Image caption")
    alt_text: str = Field(..., max_length=150, description="Accessibility alt text")
```

## Template Implementation

### Jinja2 Template

**File:** `presentation/api/renderer/templates/components/image_frame.html`

```html
{# Image Frame Component Template #}
<div class="component image-frame frame-variant-{{ component.content.frame_variant }}" id="{{ component.component_id }}">

  {# Title (if not overlay) #}
  {% if component.content.title and not component.content.overlay_text %}
  <h3 class="image-title">{{ component.content.title }}</h3>
  {% endif %}

  {# Single Image Variant #}
  {% if component.content.frame_variant == 'single' %}
  <div class="image-container aspect-ratio-{{ component.content.aspect_ratio }}">
    <img
      src="{{ component.content.image_path }}"
      alt="{{ component.content.alt_text }}"
      class="frame-image"
      loading="lazy"
    />
    {% if component.content.overlay_text and component.content.title %}
    <div class="image-overlay">
      <h3 class="overlay-title">{{ component.content.title }}</h3>
    </div>
    {% endif %}
  </div>

  {% if component.content.caption %}
  <p class="image-caption">{{ component.content.caption }}</p>
  {% endif %}
  {% endif %}

  {# Gallery 2 Variant #}
  {% if component.content.frame_variant == 'gallery_2' %}
  <div class="gallery-grid gallery-2">
    {% for img in component.content.images %}
    <div class="gallery-item">
      <div class="image-container aspect-ratio-{{ component.content.aspect_ratio }}">
        <img
          src="{{ img.image_path }}"
          alt="{{ img.alt_text }}"
          class="frame-image"
          loading="lazy"
        />
      </div>
      {% if img.caption %}
      <p class="image-caption">{{ img.caption }}</p>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {# Gallery 3 Variant #}
  {% if component.content.frame_variant == 'gallery_3' %}
  <div class="gallery-grid gallery-3">
    {% for img in component.content.images %}
    <div class="gallery-item">
      <div class="image-container aspect-ratio-{{ component.content.aspect_ratio }}">
        <img
          src="{{ img.image_path }}"
          alt="{{ img.alt_text }}"
          class="frame-image"
          loading="lazy"
        />
      </div>
      {% if img.caption %}
      <p class="image-caption">{{ img.caption }}</p>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {# Fullwidth Variant #}
  {% if component.content.frame_variant == 'fullwidth' %}
  <div class="image-container fullwidth aspect-ratio-{{ component.content.aspect_ratio }}">
    <img
      src="{{ component.content.image_path }}"
      alt="{{ component.content.alt_text }}"
      class="frame-image"
      loading="lazy"
    />
    {% if component.content.overlay_text and component.content.title %}
    <div class="image-overlay">
      <h3 class="overlay-title">{{ component.content.title }}</h3>
    </div>
    {% endif %}
  </div>
  {% endif %}

</div>
```

## CSS Styling

### Base Styles (All Themes)

```css
/* Image Frame Component */
.image-frame {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Image Container with Aspect Ratio */
.image-container {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background-color: #f5f5f5; /* Placeholder while loading */
}

.image-container.aspect-ratio-16-9 {
  aspect-ratio: 16 / 9;
}

.image-container.aspect-ratio-4-3 {
  aspect-ratio: 4 / 3;
}

.image-container.aspect-ratio-1-1 {
  aspect-ratio: 1 / 1;
}

.image-container.aspect-ratio-auto {
  aspect-ratio: auto; /* Natural image dimensions */
}

/* Image Element */
.frame-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Text Elements */
.image-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.image-caption {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

/* Gallery Grid */
.gallery-grid {
  display: grid;
  gap: 1rem;
}

.gallery-grid.gallery-2 {
  grid-template-columns: repeat(2, 1fr);
}

.gallery-grid.gallery-3 {
  grid-template-columns: repeat(3, 1fr);
}

/* Fullwidth Variant */
.frame-variant-fullwidth .image-container {
  border-radius: 0;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
}

/* Overlay Text */
.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}

.overlay-title {
  color: white;
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}
```

### Theme-Specific Styles

#### GitHub Theme

```css
/* GitHub theme: Subtle shadows, green accent */
.theme-github .image-frame {
  border: 1px solid #d0d7de;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.theme-github .image-title {
  color: #238636; /* GitHub green */
}
```

#### Modern Theme

```css
/* Modern theme: Bold shadows, vibrant colors */
.theme-modern .image-frame {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.theme-modern .image-container {
  border-radius: 12px;
}
```

#### Minimal Theme

```css
/* Minimal theme: No borders, clean lines */
.theme-minimal .image-frame {
  border: none;
  box-shadow: none;
}

.theme-minimal .image-container {
  border-radius: 0;
}
```

## Accessibility

### Required Elements

1. **Alt Text:** Every image MUST have descriptive alt text
2. **Keyboard Navigation:** Images should be tabbable if clickable
3. **ARIA Labels:** Gallery items should have `aria-label` if interactive
4. **Color Contrast:** Overlay text must meet WCAG AA standards (4.5:1 contrast ratio)

### Example with ARIA

```html
<div class="gallery-grid gallery-3" role="region" aria-label="Standort-Galerie">
  <div class="gallery-item">
    <img src="..." alt="Büro in Berlin-Mitte" />
    <p class="image-caption">Berlin</p>
  </div>
  <!-- ... -->
</div>
```

## Agent Integration

### Agent 1 (Content Analyzer)

- **Detects** image references in user input
- **Extracts** image filenames and basic context
- **Flags** `has_images = true`

### Agent 2 (Presentation Strategist)

- **Decides** image frame variant based on:
  - Number of images (1 → single, 2 → gallery_2, 3 → gallery_3)
  - Content type (hero image → fullwidth, supporting image → single)
  - Layout position (full_width → fullwidth, left/right → single)

### Agent 3 (Content Generator)

- **Writes** title (max 60 chars)
- **Writes** caption (max 200 chars)
- **Writes** alt text (max 150 chars, descriptive)

### Renderer

- **Selects** template based on `frame_variant`
- **Applies** theme CSS
- **Generates** HTML with all accessibility attributes

## Usage Examples

### Example 1: Team Photo (Single)

```json
{
  "type": "image_frame",
  "content": {
    "image_id": "team.png",
    "image_path": "projects/robo4you/images/uploads/team.png",
    "title": "Unser Team",
    "caption": "5 Experten mit über 20 Jahren kombinierter Erfahrung",
    "alt_text": "Gruppenfoto der fünf Robo4you Teammitglieder",
    "frame_variant": "single",
    "aspect_ratio": "16:9"
  }
}
```

### Example 2: Before/After Comparison (Gallery 2)

```json
{
  "type": "image_frame",
  "content": {
    "title": "Vorher / Nachher",
    "frame_variant": "gallery_2",
    "aspect_ratio": "4:3",
    "images": [
      {
        "image_id": "before.png",
        "image_path": "projects/robo4you/images/uploads/before.png",
        "caption": "Manueller Prozess",
        "alt_text": "Screenshot des manuellen Workflows"
      },
      {
        "image_id": "after.png",
        "image_path": "projects/robo4you/images/uploads/after.png",
        "caption": "Automatisiert",
        "alt_text": "Screenshot des automatisierten Workflows"
      }
    ]
  }
}
```

### Example 3: Product Hero (Fullwidth)

```json
{
  "type": "image_frame",
  "content": {
    "image_id": "hero.png",
    "image_path": "projects/robo4you/images/uploads/hero.png",
    "title": "Robo4you Platform",
    "alt_text": "Robo4you Robotik-Plattform in Produktionsumgebung",
    "frame_variant": "fullwidth",
    "aspect_ratio": "16:9",
    "overlay_text": true
  }
}
```

## Future Enhancements

### Potential Extensions (v1.1+)

1. **Image Carousel:** Multiple images with navigation arrows
2. **Lightbox/Zoom:** Click to enlarge functionality
3. **Lazy Loading:** Progressive image loading for performance
4. **Responsive Variants:** Different images for mobile/desktop
5. **Video Support:** Embed videos in same frame structure

## Version History

- **1.0** (2025-11-17) - Initial specification

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Renderer Specification](./renderer-specification.md)
- [Agent 2 Specification](./agent-2-presentation-strategist.md) (decides variant)
- [Agent 3 Specification](./agent-3-content-generator.md) (writes text)
- [Template Inventory](./template-inventory.md)

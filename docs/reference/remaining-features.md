# Remaining Features & Future Work

This document outlines features that are documented in the requirements but not yet implemented in the V2 architecture.

---

## 1. Image Color Extraction & Colored Frames ⭐ HIGH PRIORITY

### Description
Generate colored frames and badges around images based on dominant image colors.

### Requirements from Brief
- Extract dominant color from uploaded images
- Apply color to image frame border
- Add colored badge overlay (top-right corner)

### Technical Details

**Current State:**
- Images are uploaded to `projects/{project}/images/uploads/`
- `image-frame.html.j2` template exists but doesn't include color support
- No color extraction library integrated

**Implementation Strategy:**

1. **Add Image Processing Service**
   - Location: `presentation/api/services/image_processor.py`
   - Library: `pillow` (PIL) + `colorthief` or equivalent
   - Function: `extract_dominant_color(image_path: str) -> str (hex color)`

2. **Extend FormattedSlide Model**
   - Add optional `frame_color` field to image components
   - Add optional `badge_color` field
   - Add optional `badge_text` field

3. **Update ContentGeneratorAgentV2**
   - Detect when image slots are used
   - Call image processor to get dominant color
   - Include color in FormattedSlide output

4. **Update image-frame.html.j2 Template**
   ```jinja2
   {% if frame_color %}
     <div class="image-container" style="border-color: {{ frame_color }};">
   {% else %}
     <div class="image-container">
   {% endif %}
     <div class="image-wrapper">
       <img src="{{ image_src }}" alt="{{ alt_text }}">
       {% if badge_text and badge_color %}
         <div class="image-badge" style="background: {{ badge_color }};">
           {{ badge_text }}
         </div>
       {% endif %}
     </div>
   </div>
   ```

5. **Add Dependencies**
   - `pillow>=9.0.0` for image processing
   - `colorthief>=1.4.0` for dominant color extraction

**Testing:**
- Test with various image types (JPG, PNG, GIF)
- Test color extraction accuracy
- Test frame rendering in reference.html

**Estimated Effort:** 2-3 days

---

## 2. Variant Generation in V2 ⭐ HIGH PRIORITY

### Description
Port variant generation from V1 (LLM-based) to V2 (deterministic template-based).

### Requirements from Brief
- Generate 3 design variants: corporate, modern, minimal
- Same content, different styling
- No additional API calls required
- Instant rendering

### Technical Details

**Current State:**
- V1 had `_generate_variants()` method using LLM
- V2 uses deterministic Jinja2 templates
- Design guides now exist for all 3 themes

**Implementation Strategy:**

1. **Add Variant Generation Method to ContentGeneratorAgentV2**
   ```python
   def generate_variants(
       self,
       formatted_slide: FormattedSlide,
       theme_profiles: list = ["github", "modern", "minimal"]
   ) -> dict:
       """Generate 3 variants using different theme designs"""
       variants = []
       for theme in theme_profiles:
           html = render_slide(formatted_slide, theme)
           variants.append({"profile": theme, "html": html})
       return {"variants": variants}
   ```

2. **Update HTMLComponentRenderer**
   - Add theme-aware rendering method
   - Load appropriate design-guide.json per theme
   - Apply CSS variables from design-guide.json
   - Support theme switching in templates

3. **Update V2 Route**
   - Add optional `generate_variants` parameter
   - Return multi-variant response when requested

4. **CSS Variable System**
   - Leverage existing design-guide.json tokens
   - Generate theme-specific CSS custom properties
   - Apply to Jinja2 templates via context

**Example Response:**
```json
{
  "success": true,
  "variants": [
    {
      "profile": "github",
      "html": "...",
      "design_tokens": {...}
    },
    {
      "profile": "modern",
      "html": "...",
      "design_tokens": {...}
    },
    {
      "profile": "minimal",
      "html": "...",
      "design_tokens": {...}
    }
  ]
}
```

**Advantages Over V1:**
- ✅ Deterministic (no LLM unpredictability)
- ✅ Instant generation (no API calls)
- ✅ Cost-free
- ✅ Consistent styling across variants

**Testing:**
- Test variant generation for all component types
- Visual regression testing (compare themes)
- Performance testing (should be <100ms total)

**Estimated Effort:** 2 days

---

## 3. Project Briefing System (project-brief.json) ⭐ MEDIUM PRIORITY

### Description
Add structured project briefing files that inform all agent decisions.

### Requirements from Brief
- One briefing file per project: `projects/{name}/project-brief.json`
- Contains project metadata, target audience, tone, brand guidelines
- Integrated into agent context for consistent generation

### Technical Details

**Schema:**
```json
{
  "project_name": "beispiel-projekt",
  "language": "de",
  "description": "Project description",
  "target_audience": "Investoren, Interessierte",
  "use_case": "Investor pitch deck",
  "value_proposition": "One-liner unique value",
  "tone_of_voice": {
    "formality": "professional|casual|formal",
    "properties": ["innovative", "trustworthy", "data-driven"],
    "forbidden_buzzwords": ["game-changer", "synergy"],
    "example_phrases": [...]
  },
  "design_preferences": {
    "preferred_layouts": ["title_statgrid_text", "title_two_columns"],
    "icon_usage": true,
    "logo_placement": "top-right",
    "color_overrides": {...}
  },
  "constraints": {
    "must_contain": ["Value proposition on first slide"],
    "never_use": ["Jargon", "Internal terms"],
    "compliance": "GDPR, Data privacy"
  },
  "brand_guidelines": {
    "logo_url": "...",
    "brand_colors": {...},
    "fonts": {...}
  }
}
```

**Implementation:**

1. **Add ProjectBriefService**
   - Location: `presentation/api/services/project_brief_service.py`
   - Load and validate project-brief.json
   - Expose briefing in agent context

2. **Update Agent Prompts**
   - ContentAnalyzerAgentV2: Use tone & language from briefing
   - PresentationStrategistAgentV2: Use design preferences
   - ContentGeneratorAgentV2: Apply tone & constraints

3. **Create Briefing Template**
   - New file: `presentation/projects/beispiel-projekt/project-brief.json`
   - Pre-fill with intelligent defaults
   - Document all fields

4. **Update V2 Routes**
   - Add endpoints to get/update project briefing
   - `/api/v2/projects/{name}/briefing` (GET)
   - `/api/v2/projects/{name}/briefing` (PUT)

**Testing:**
- Test briefing loading
- Test constraint application
- Test tone application in generated content

**Estimated Effort:** 2 days

---

## 4. Enhanced Table Support ⭐ MEDIUM PRIORITY

### Description
Improve table component with advanced features.

### Features to Implement

1. **Markdown Table Round-Trip**
   - Detect markdown tables in input
   - Preserve structure in HTML output
   - Allow editing via Markdown + HTML

2. **Complex Layouts**
   - Support colspan/rowspan
   - Support nested headers
   - Support multi-row headers

3. **Better Badge Positioning**
   - Cell-specific badges (not row-wide)
   - Badge counts and indicators
   - Conditional badge rendering

**Technical Details:**

1. **Markdown Parser Enhancement**
   - Detect markdown table syntax
   - Parse into table data structure
   - Preserve during processing

2. **Template Enhancement**
   - Update `table.html.j2` with advanced features
   - Add colspan/rowspan support
   - Add nested structure support

**Estimated Effort:** 2-3 days

---

## 5. Advanced Process Components ⭐ MEDIUM PRIORITY

### Description
Enhanced timeline and process visualizations.

### Features to Implement

1. **Timeline Visualization**
   - Optional date ranges on timeline
   - Visual duration indicators
   - Milestone markers

2. **Process Variants**
   - Decision trees (branches in process)
   - Parallel paths
   - Loop-back arrows

3. **Process Styling**
   - Color-coded steps by category
   - Icon support for each step
   - Progress indicators

**Technical Details:**

1. **Add timeline.html.j2 Template**
   - Date-based horizontal timeline
   - Milestone positioning
   - Duration visualization

2. **Enhanced process.html.j2**
   - Support for branches/decisions
   - Color per step support
   - Icon slots per step

3. **FormattedSlide Extension**
   - Add timeline component type
   - Add enhanced process variant

**Estimated Effort:** 2-3 days

---

## 6. Style Guide JSON Integration (LOW PRIORITY - BLOCKED BY TASK 1)

### Description
Update agents and services to actively use design-guide.json.

### Current State
- design-guide.json files created ✅
- Not yet integrated into agents
- StyleParser reads markdown, not JSON

### Implementation

1. **Update StyleParser**
   - Load design-guide.json first
   - Fall back to markdown if not found
   - Expose component definitions to agents

2. **Update PresentationStrategistAgentV2**
   - Reference component slots from design-guide.json
   - Validate component availability
   - Use layout definitions from JSON

3. **Update ContentGeneratorAgentV2**
   - Validate against component schemas
   - Use required/optional field definitions
   - Ensure FormattedSlide matches schema

**Estimated Effort:** 1-2 days

---

## 7. Component Library Expansion (LOW PRIORITY)

### Description
Add new component types for specialized content.

### Potential Components

1. **Comparison Matrix** (beyond tables)
   - Multi-dimensional comparison
   - Visual bar indicators
   - Custom scoring

2. **Roadmap Component**
   - Timeline with milestones
   - Quarterly/phase visualization
   - Deliverable tracking

3. **Org Chart Component**
   - Hierarchical structure
   - Team member cards
   - Reporting lines

4. **Metrics Dashboard**
   - KPI cards (similar to stats but more visual)
   - Trend indicators (↑ ↓ →)
   - Color-coded health status

5. **Gallery Component**
   - Carousel of images
   - Lightbox support
   - Thumbnail navigation

**Implementation Pattern:**
- New template: `presentation/templates/components/{component}.html.j2`
- Update design-guide.json with component definition
- Add tests

**Estimated Effort:** 4-5 days total (all components)

---

## 8. Advanced Image Features (LOW PRIORITY)

### Description
Beyond color extraction, enhance image handling.

### Features

1. **Image Optimization**
   - Auto-resize to max dimensions
   - Compression
   - Format conversion

2. **Image Metadata**
   - Store upload metadata
   - Alt text auto-generation
   - Caption suggestions

3. **Image Collections**
   - Image sets/folders
   - Bulk operations
   - Image versioning

4. **Smart Image Selection**
   - Recommend relevant images for content
   - Tag-based organization
   - Usage tracking

**Estimated Effort:** 3-4 days

---

## 9. Feedback & Iteration Loop (LOW PRIORITY)

### Description
Formalize user feedback mechanism for slide regeneration.

### Requirements

1. **Feedback Collection**
   - Specific feedback categories
   - Feedback history per slide
   - Iteration tracking

2. **Improvement Loop**
   - Agents incorporate previous feedback
   - Prevent same mistakes
   - Track improvement metrics

3. **A/B Testing**
   - Compare variants based on criteria
   - Preference scoring
   - Learning from choices

**Estimated Effort:** 2-3 days

---

## 10. Documentation & Migration (IN PROGRESS)

### Current Work
- [x] VARIANT_GENERATION_DOCUMENTATION.md created
- [ ] Migration guide (how to update existing code)
- [ ] CLAUDE.md with V2-only architecture
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Agent protocol documentation

### Estimated Effort
- Migration guide: 1 day
- CLAUDE.md update: 2-3 hours
- API docs: 1 day
- Agent protocol: 2-3 hours

---

## Priority Summary

### 🔴 CRITICAL (Do Now)
- Image color extraction & frames
- Variant generation in V2

### 🟠 HIGH (Next Sprint)
- Project briefing system
- Enhanced table support
- Style guide JSON integration

### 🟡 MEDIUM (Future)
- Advanced process components
- Component library expansion
- Image features

### 🟢 LOW (Nice-to-Have)
- Feedback iteration loop
- Advanced documentation
- A/B testing

---

## Dependency Graph

```
Image Colors ──→ Variant Generation ──→ V2 Completion ✅
                        ↓
                   Design Integration ──→ Full Theming

Project Briefing ──→ Better Content Quality
                        ↓
Style Guide JSON ──→ Validation & Constraints

Enhanced Tables ──→ Data-heavy Slides
Advanced Process ──→ Timeline/Workflow Slides

Component Library ──→ Specialized Use Cases
```

---

## Testing Strategy

Each feature should include:
1. **Unit Tests**: Component/function level
2. **Integration Tests**: End-to-end flows
3. **Visual Tests**: Screenshot comparisons
4. **Performance Tests**: Generation time, API calls
5. **User Acceptance Tests**: Against requirements

---

## Documentation to Update

- [ ] CLAUDE.md - Architecture overview
- [ ] README.md - Feature list
- [ ] API documentation - OpenAPI/Swagger
- [ ] Agent protocols - How agents work
- [ ] Template guide - Creating new components
- [ ] Design system guide - Using design-guide.json

---

## Related Files

- Design-guide JSON files: `projects/beispiel-projekt/styles/{theme}/design-guide.json`
- Reference HTML: `projects/beispiel-projekt/styles/{theme}/reference.html`
- Variant documentation: `presentation/api/VARIANT_GENERATION_DOCUMENTATION.md`
- V2 agent code: `presentation/api/agents/*_v2.py`
- V2 renderer: `presentation/api/renderers/component_renderer.py`

---

*Last Updated: 2025-11-18*
*Status: Planning Phase - V2 Foundation Complete*

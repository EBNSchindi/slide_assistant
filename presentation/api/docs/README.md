# Architecture Specifications

**Version:** 1.0
**Status:** Draft
**Created:** 2025-11-17
**Purpose:** Complete specification for the redesigned multi-agent slide generation system

---

## 📋 Overview

This directory contains the **complete architectural specifications** for the new slide generation system with:

- **3 AI Agents** (Content Understanding, Layout Planning, Text Writing)
- **1 Deterministic Renderer** (LLM-free HTML generation)
- **Standardized Image Frame** (consistent visual presentation)

---

## 🗂️ Documentation Index

### Core Architecture

1. **[Blueprint Schema](./blueprint-schema.md)** ⭐ **START HERE**
   - Central data structure (DSL) connecting all components
   - Pydantic models for type-safe blueprints
   - Complete examples and validation rules

### Agent Specifications

2. **[Agent 1: Content Analyzer](./agent-1-content-analyzer.md)**
   - **Role:** Content understanding & extraction
   - **Input:** User text/markdown
   - **Output:** Structured content blocks + metadata

3. **[Agent 2: Presentation Strategist](./agent-2-presentation-strategist.md)**
   - **Role:** Layout & component planning
   - **Input:** Content analysis (from Agent 1)
   - **Output:** Partial blueprint (layout + component mapping)

4. **[Agent 3: Content Generator](./agent-3-content-generator.md)**
   - **Role:** Text writing & copywriting
   - **Input:** Partial blueprint (from Agent 2)
   - **Output:** Complete blueprint (all text filled)

### Rendering System

5. **[Renderer Specification](./renderer-specification.md)**
   - **Role:** Deterministic HTML generation (no LLM)
   - **Input:** Complete blueprint (from Agent 3)
   - **Output:** HTML + Markdown

6. **[Template Inventory](./template-inventory.md)**
   - Complete catalog of all available templates
   - 5 layout types, 5+ component types
   - Usage rules and compatibility matrix

### Components

7. **[Image Frame Specification](./image-frame-specification.md)**
   - Standardized image display system
   - 4 variants: single, gallery_2, gallery_3, fullwidth
   - Accessibility and responsive design

---

## 🔄 System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT                              │
│  (Stichpunkte, Text, Markdown, optional: Bilder)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 1: Content Analyzer                                  │
│  - Detect language (de/en)                                  │
│  - Extract content blocks (stats, bullets, quotes, images)  │
│  - Identify key messages                                    │
│  Output: ContentAnalysis (structured JSON)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 2: Presentation Strategist                           │
│  - Choose 1-3 components                                    │
│  - Select layout type                                       │
│  - Assign positions                                         │
│  - Plan image placement                                     │
│  Output: PartialBlueprint (layout + component structure)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 3: Content Generator (Copywriter)                    │
│  - Write slide title & subtitle                            │
│  - Write all component text (bullets, labels, captions)     │
│  - Generate alt texts for images                           │
│  - Fill all [TBD] placeholders                             │
│  Output: CompleteBlueprint (ready for rendering)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  RENDERER (Deterministic, No LLM)                           │
│  - Load layout template                                     │
│  - Render each component from template                      │
│  - Assemble slide HTML                                      │
│  - Generate markdown (optional)                             │
│  Output: HTML + Markdown                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     OUTPUT FILES                            │
│  - folie-{NN}-{title}.html                                  │
│  - folie-{NN}-{title}.md                                    │
│  - slide-{NN}-{title}.json (blueprint, optional)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Benefits of This Architecture

### ✅ Separation of Concerns

- **Agent 1:** Understanding (what does the user want?)
- **Agent 2:** Planning (how should it look?)
- **Agent 3:** Writing (what's the final text?)
- **Renderer:** Execution (generate HTML)

Each component has **one job**, clearly defined.

### ✅ Deterministic HTML

- **Zero LLM involvement** in HTML generation
- Same Blueprint → Same HTML (always)
- Upgrade to GPT-6? → HTML stays identical
- Easy to test, version, and maintain

### ✅ Standardized Images

- All images use predefined **Image Frame** templates
- Consistent visual appearance across slides
- 4 variants cover all use cases
- User's request fulfilled: "Bilder sollen standardisiert sein"

### ✅ Type Safety

- **Pydantic models** for all data structures
- Validation at every step
- Compile-time error catching
- No "LLM hallucinated invalid JSON" issues

### ✅ Testability

- **Agent 1-3:** Unit tests on JSON output
- **Renderer:** Unit tests on HTML structure
- **Integration:** End-to-end pipeline tests
- **No flaky LLM behavior** in HTML generation

### ✅ Flexibility

- Blueprints can be **manually edited** (JSON files)
- Renderer can be used **standalone** (no agents)
- Templates can be updated **without touching agents**
- New component types: Just add templates + update Agent 2

---

## 📐 Blueprint Schema (Central DSL)

The **Blueprint** is the core data structure that connects everything:

```json
{
  "schema_version": "1.0",
  "slide_id": "slide-03-team",
  "slide_title": "Unser Team",
  "layout_type": "two_column",
  "language": "de",
  "components": [
    {
      "component_id": "comp-1",
      "type": "stat_grid",
      "position": "left",
      "content": { ... }
    },
    {
      "component_id": "comp-2",
      "type": "image_frame",
      "position": "right",
      "content": { ... }
    }
  ],
  "metadata": { ... }
}
```

**Read more:** [Blueprint Schema](./blueprint-schema.md)

---

## 🧩 Component Types

| Component | Purpose | Example Use Case |
|-----------|---------|------------------|
| **stat_grid** | Display 2-4 statistics | "5 Experten, 20 Jahre Erfahrung" |
| **bullet_list** | Display 2-6 bullet points | Problem statements, feature lists |
| **quote** | Display a quote with attribution | Customer testimonial |
| **text_block** | Display 1-3 paragraphs | Narrative text, mission statement |
| **image_frame** | Display images (4 variants) | Team photo, product screenshot, hero image |
| **process_chain** *(v1.1)* | Display step-by-step process | "Step 1 → Step 2 → Step 3" |
| **table** *(v1.1)* | Display tabular data | Pricing table, feature comparison |

**Read more:** [Template Inventory](./template-inventory.md)

---

## 🎨 Layout Types

| Layout | Components | Use Case |
|--------|------------|----------|
| **single_column** | 1-3 | Stacked content (bullets, text, fullwidth image) |
| **two_column** | 2 | Side-by-side (stats + image, bullets + quote) |
| **three_row** | 2-3 | Vertical tiers (step 1, 2, 3) |
| **header_content** | 2 | Large header + main content |
| **sidebar_main** | 2 | Sidebar (30%) + main (70%) |

**Read more:** [Template Inventory](./template-inventory.md)

---

## 🖼️ Image Frame Variants

| Variant | Use Case | Example |
|---------|----------|---------|
| **single** | Single image with title/caption | Team photo, product shot |
| **gallery_2** | 2 images side-by-side | Before/after, desktop/mobile |
| **gallery_3** | 3 images in grid | Office locations, feature screenshots |
| **fullwidth** | Hero image (full width) | Product hero, landscape photo |

**Read more:** [Image Frame Specification](./image-frame-specification.md)

---

## 🛠️ Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

1. ✅ Write specifications (THIS STEP - DONE!)
2. ⬜ Implement Blueprint Pydantic models
3. ⬜ Create template files (layouts + components)
4. ⬜ Build Renderer (deterministic HTML generator)

### Phase 2: Agents (Week 3-4)

5. ⬜ Rebuild Agent 3 (Copywriter - text only, no HTML)
6. ⬜ Update Agent 2 (output partial blueprint instead of strategy)
7. ⬜ Update Agent 1 (output ContentAnalysis with content blocks)
8. ⬜ Update Orchestrator (new 3-agent pipeline)

### Phase 3: Integration (Week 5)

9. ⬜ Wire agents → renderer pipeline
10. ⬜ Update API endpoints (`/api/generate`)
11. ⬜ Add blueprint storage (save JSON files)
12. ⬜ Update file service (save HTML, Markdown, Blueprint)

### Phase 4: Testing & Polish (Week 6)

13. ⬜ Unit tests (agents, renderer, validation)
14. ⬜ Integration tests (full pipeline)
15. ⬜ Update frontend (ai-editor.html)
16. ⬜ Documentation updates (CLAUDE.md, README.md)

---

## 📚 Design Principles

1. **LLM-Arm, Flow-Stark**
   - Minimize LLM involvement in structure/HTML
   - Use deterministic flows wherever possible

2. **Type-Safe**
   - Pydantic models for all data structures
   - Validation at every step

3. **Template-Driven**
   - All HTML from predefined templates
   - No LLM-generated markup

4. **Blueprint as Source of Truth**
   - Single data structure describes entire slide
   - Can be saved, versioned, manually edited

5. **Accessibility First**
   - Alt texts required
   - ARIA labels where needed
   - WCAG AA compliance

6. **Performance**
   - Renderer runs in milliseconds (no API calls)
   - Agents optimized for minimal token usage

---

## 🧪 Testing Strategy

### Unit Tests

- **Agent 1:** Content type detection, block extraction
- **Agent 2:** Component selection, layout mapping
- **Agent 3:** Text generation, character limits
- **Renderer:** Template rendering, validation

### Integration Tests

- **Agent 1 → 2 → 3:** Full analysis pipeline
- **Agent 3 → Renderer:** Blueprint to HTML
- **End-to-End:** User input → HTML output

### Fixture Data

All test fixtures in `presentation/api/tests/fixtures/`:
- `agent1/` - Content analysis examples
- `agent2/` - Layout planning examples
- `agent3/` - Complete blueprints
- `renderer/` - Expected HTML outputs

---

## 🔧 Development Tools

### CLI Commands (Planned)

```bash
# Render blueprint to HTML
python -m presentation.api.renderer.cli render blueprint.json output/

# Batch render all blueprints
python -m presentation.api.renderer.cli batch blueprints/ output/

# Validate blueprint
python -m presentation.api.blueprints.cli validate blueprint.json

# Generate blueprint from markdown (manual)
python -m presentation.api.blueprints.cli from-markdown input.md output.json
```

---

## 📖 Reading Order

**For Developers:**

1. Start: [Blueprint Schema](./blueprint-schema.md)
2. Then: [Agent 1](./agent-1-content-analyzer.md) → [Agent 2](./agent-2-presentation-strategist.md) → [Agent 3](./agent-3-content-generator.md)
3. Then: [Renderer](./renderer-specification.md)
4. Reference: [Template Inventory](./template-inventory.md), [Image Frame](./image-frame-specification.md)

**For Designers:**

1. Start: [Template Inventory](./template-inventory.md)
2. Then: [Image Frame Specification](./image-frame-specification.md)
3. Reference: [Blueprint Schema](./blueprint-schema.md) (to understand data structure)

**For Product Managers:**

1. Start: This README (overview)
2. Then: Flow diagram (above)
3. Reference: Individual agent specs to understand capabilities

---

## 🤝 Contributing

When adding new features:

1. **Update specs first** (in this docs/ directory)
2. **Get approval** on spec changes
3. **Implement** according to spec
4. **Update tests** to match spec
5. **Update this README** if architecture changes

---

## 📝 Version History

- **1.0** (2025-11-17) - Initial specification release

---

## 🔗 Related Documentation

- [Main Project README](../../../README.md)
- [CLAUDE.md](../../../CLAUDE.md) (project instructions)
- [API Documentation](../README.md) (once implemented)

---

**End of Architecture Specifications**

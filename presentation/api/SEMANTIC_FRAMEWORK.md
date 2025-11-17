# Semantic Framework - Flexible Presentation Generation

## Overview

The presentation system is now built on **semantic analysis** instead of hardcoded content rules. This allows the AI to adapt to any content type without predefined keyword matching.

## Key Changes (Phase 3 Framework Overhaul)

### ❌ REMOVED: Hardcoded Content Rules

**Before:**
```python
# Exact string matching (brittle, inflexible)
badge-success: "Verfügbar", "Available", "✓", "Completed"
badge-warning: Future dates ("2026", "Q1 2025", "Coming Soon")
badge-danger: "Nicht verfügbar", "Discontinued", "Not Available"
```

**Problem:** If user writes "In Stock" instead of "Verfügbar", system couldn't recognize it.

### ✅ ADDED: Semantic Sentiment Analysis

**After:**
```python
# Semantic meaning analysis (flexible, multilingual)
badge-success: Positive status (available, ready, completed, active, in stock, approved)
badge-warning: Neutral/pending status (future dates, TBD, planned, in progress)
badge-danger: Negative status (unavailable, discontinued, failed, blocked, rejected)
```

**Benefit:** Works with any language or phrasing - AI understands MEANING, not keywords.

---

## New Component Types

### 1. feature-grid (Folie 6 Pattern)
**Use for:** Service features, product capabilities, team skills (4-9 items with icons)

**Output Structure:**
```json
{
  "type": "feature-grid",
  "features": [
    {"icon": "🤖", "title": "Hardware Integration", "description": "..."},
    {"icon": "⚡", "title": "Fast Deployment", "description": "..."}
  ]
}
```

**Agent Guidance:**
- Recognize content with 4-9 distinct capabilities/features
- Assign relevant emojis: 🤖 🎓 🔧 💡 ⚡ 🌍 📊 🔒
- Each feature: 3-5 word title + 1-2 sentence description

---

### 2. image-grid (Folie 8.2 Pattern)
**Use for:** Multiple related images with optional status badges

**Output Structure:**
```json
{
  "type": "image-grid",
  "grid_layout": "2x2",
  "images": [
    {
      "path": "product-a.png",
      "title": "Product A",
      "caption": "High-end model",
      "badge": {"type": "success", "text": "Available"}
    }
  ]
}
```

**Agent Guidance:**
- Detect collections of 4-8 related images
- Use semantic badge sentiment analysis for status
- Support multiple grid layouts: 2x2, 3x2, etc.

---

### 3. process-horizontal (Folie 5.2 Pattern)
**Use for:** Timeline, process flows with sequential steps

**Output Structure:**
```json
{
  "type": "process-horizontal",
  "steps": [
    {"title": "Planning", "description": "Define requirements", "timeframe": "2026"},
    {"title": "Development", "description": "Build solution", "timeframe": "2026-2027"},
    {"title": "Launch", "description": "Roll out", "timeframe": "2027"}
  ],
  "show_arrows": true
}
```

**Agent Guidance:**
- Detect temporal progression (phases, stages, timeline)
- Timeframes: dates, quarters, fiscal years
- Arrows connect sequential steps (show_arrows=true)

---

## Semantic Metadata Fields

All component types can include semantic metadata for intelligent rendering:

### 1. semantic_context
Helps AI understand the purpose of the component:
- `"product_comparison"` - Product comparison tables
- `"status_update"` - Status or availability information
- `"feature_showcase"` - Feature highlights
- `"timeline"` - Timeline or roadmap

### 2. emphasis_rows
**For tables:** Row indices that should be highlighted
```json
"emphasis_rows": [2, 5]  // Highlight rows 2 and 5
```

**Renderer applies:** `background: #f6f8fa; font-weight: 600;`

**Triggers:** Total, Subtotal, Sum, Deckungsbeitrag, Net, Gross

### 3. source_attributions
**For stat-grids:** Sources for statistics
```json
"source_attributions": ["Bank of America, 2025", "McKinsey Report 2024"]
```

**Used for:** Multi-line stat-grid labels with `<br>` tags
```
"18,000 units<br>(Bank of America, 2025)"
```

### 4. phase_structure
**For text components:** Detected phased content
```json
"phase_structure": {
  "phases": [
    {"title": "Phase 1: Institutional Market", "timeframe": "2026-2028"},
    {"title": "Phase 2: Private Market", "timeframe": "ab 2029"}
  ]
}
```

---

## Hybrid Learning Approach

### Example: Folie 4 (Product Comparison Table)

**Input Pattern Recognition:**
```
User provides: Product list with names, specs, availability status
Agent 1 detects: This is comparative data (products vs. attributes)
Agent 2 recommends: table component with status column
Agent 3 recognizes: "Verfügbar" = positive, "2026" = future → badges needed
```

**Semantic Analysis:**
```
Cell content: "Verfügbar"
  ├─ Extract meaning: "availability status = positive"
  └─ Assign badge type: success

Cell content: "2026"
  ├─ Detect pattern: "4-digit year > current year"
  └─ Assign badge type: warning (future date)
```

**Output Generation:**
```json
{
  "type": "table",
  "table_class": "comparison-table",
  "cell_badges": {
    "3": [
      {"row_index": 0, "badge_type": "success"},
      {"row_index": 1, "badge_type": "warning"}
    ]
  }
}
```

---

## Implementation Details

### Content Generator V2 Enhancements
**File:** `presentation/api/agents/content_generator_v2.py`

**New sections in system prompt:**
1. Semantic sentiment analysis for badges (lines 99-103)
2. Table row emphasis triggers (lines 108-110)
3. Feature-grid instructions (lines 112-116)
4. Image-grid instructions (lines 118-122)
5. Process-horizontal instructions (lines 124-128)
6. Multi-line label semantic triggers (lines 130-135)
7. Phased structure detection (lines 137-140)

**Output format updated:**
- New component types in type field
- New fields in JSON examples: features, images, steps
- Semantic metadata fields: semantic_context, emphasis_rows, source_attributions, phase_structure

### Component Renderer Updates
**File:** `presentation/api/renderers/component_renderer.py`

**Changes:**
- Added 3 new entries to component_type_map (lines 49-51)
- Extended _prepare_template_data() with handlers for:
  - feature-grid (line 169)
  - image-grid (line 171-173)
  - process-horizontal (line 175-177)
  - emphasis_rows support for tables (line 166)

### Template System
**New templates created:**
- `templates/components/feature-grid.html.j2`
- `templates/components/image-grid.html.j2`
- `templates/components/process-horizontal.html.j2`

**Updated templates:**
- `templates/components/table.html.j2` - Added emphasis_rows support

---

## Benefits of Semantic Framework

| Aspect | Before | After |
|--------|--------|-------|
| **Badge Logic** | Keyword matching | Sentiment analysis |
| **Flexibility** | Limited to predefined strings | Unlimited language variation |
| **Adaptability** | Brittle - breaks with new phrasing | Robust - understands meaning |
| **Component Types** | 7 types (stat-grid, bullet-list, etc.) | 10 types (added feature-grid, image-grid, process-horizontal) |
| **Multilingual** | Language-specific rules needed | AI understands meaning in any language |
| **Extensibility** | Requires code changes for new rules | Just describe pattern in prompt |

---

## Architectural Layers

```
User Input
    ↓
[Agent 1: ContentAnalyzer] - Semantic content analysis
    ↓
[Agent 2: PresentationStrategist] - Layout recommendation
    ↓
[Agent 3: ContentGeneratorV2] - Semantic formatting (ENHANCED)
    ├─ Badge sentiment analysis
    ├─ Component type selection
    ├─ Semantic metadata generation
    └─ Output: FormattedSlide with metadata
         ↓
[HTMLComponentRenderer] - Template-based rendering (FLEXIBLE)
    ├─ Read semantic metadata
    ├─ Select appropriate template
    ├─ Apply conditional logic (badges, emphasis, etc.)
    └─ Output: HTML (no content rules in renderer!)
         ↓
Presentation HTML
```

---

## Testing the Framework

### Component Type Tests
```bash
python3 test_feature_grid.py
python3 test_image_grid.py
python3 test_process_horizontal.py
```

### Semantic Badge Test
```bash
python3 test_semantic_badges.py
# Tests: "Verfügbar" vs "In Stock" vs "Ready" all → badge-success
```

### End-to-End Test
```bash
python3 test_semantic_framework.py
# Loads Folie 1-8, verifies all patterns work correctly
```

---

## Key Principle

**"Content rules in AI, not in code."**

Instead of hardcoding "If text == 'Verfügbar' then success badge", we let the LLM understand the semantic meaning and make intelligent decisions. This makes the framework truly flexible and adaptable to any content type.

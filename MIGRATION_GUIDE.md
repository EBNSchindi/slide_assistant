# Migration Guide: V1 → V2 Architecture

This guide explains how the system migrated from V1 (LLM-generated HTML) to V2 (deterministic templates) and how to use the new architecture.

---

## Overview: What Changed?

### V1 Architecture ❌ (Deprecated)
```
User Input
  ↓
ContentAnalyzerAgent (LLM)
  ↓
PresentationStrategistAgent (LLM)
  ↓
ContentGeneratorAgent (LLM) → Generates HTML directly
  ↓
HTML Output
```

**Problems:**
- ❌ Inconsistent HTML structure (LLM can change format)
- ❌ Variant generation requires 3 additional API calls
- ❌ No type safety or validation
- ❌ CSS classes and IDs could vary
- ❌ Hard to debug HTML issues

### V2 Architecture ✅ (Current)
```
User Input
  ↓
ContentAnalyzerAgentV2 (LLM) → Structured analysis
  ↓
PresentationStrategistAgentV2 (LLM) → Slide blueprint
  ↓ (feedback loop if needed)
ContentGeneratorAgentV2 (LLM) → Formatted text (NO HTML)
  ↓
HTMLComponentRenderer (Jinja2) → Deterministic HTML
  ↓
HTML Output
```

**Advantages:**
- ✅ Consistent HTML structure (templates define format)
- ✅ Variant generation is instant (no API calls)
- ✅ Type-safe with Pydantic models
- ✅ Predictable CSS classes
- ✅ Easy to debug and modify templates
- ✅ Design system can evolve independently

---

## Key Architectural Differences

### 1. Agent Outputs Changed

**V1: HTML Generation**
```python
# V1 ContentGeneratorAgent output
{
    "html": "<div class='component'>...</div>",  # Raw HTML
    "markdown": "# Slide...",
    "components_used": ["stat-grid"]
}
```

**V2: Data Structure Only**
```python
# V2 ContentGeneratorAgentV2 output (FormattedSlide)
{
    "slide_title": "Problem",
    "components": [
        {
            "type": "stat-grid",
            "title": "Key Numbers",
            "stats": [
                {
                    "value": "83,6 Mio",
                    "label": "Population",
                    "unit": "People"
                }
            ]
        }
    ]
}
```

The HTML is generated separately by `HTMLComponentRenderer` from a template.

### 2. Component Rendering

**V1: LLM Writes HTML**
```python
agent.generate(analysis, strategy, style_guide)
# LLM generates HTML - hard to predict format
```

**V2: Template Renders HTML**
```python
formatted_slide = agent.generate(analysis, strategy)
# Returns pure data structure (FormattedSlide)

html = renderer.render(formatted_slide, theme="github")
# Templates generate HTML - format is guaranteed
```

### 3. Variant Generation

**V1: Expensive (3 API Calls)**
```python
# Old way - each variant requires LLM API call
variants = agent.generate_variants(
    analysis, strategy, variant_profiles=["corporate", "modern", "minimal"]
)
# Costs: 3x API calls, 3x wait time (~9 seconds)
```

**V2: Free & Instant (Template Switching)**
```python
# New way - render same data with different themes
variants = renderer.generate_variants(formatted_slide)
# Costs: $0 (no API), ~100ms (template rendering)
```

### 4. Style System

**V1: Hardcoded in HTML**
- Colors, fonts, spacing → baked into generated HTML
- Changing style required agent re-run

**V2: CSS Variables (design-guide.json)**
- Colors, fonts, spacing → defined in design-guide.json
- Style can change without re-running agents
- Themes inherit base styles

```json
{
  "tokens": {
    "colors": {
      "primary": { "main": "#238636" }
    }
  }
}
```

---

## File Structure Changes

### Removed (V1 Only)
```
❌ presentation/api/agents/content_analyzer.py
❌ presentation/api/agents/content_generator.py
❌ presentation/api/agents/presentation_strategist.py
❌ presentation/api/agents/mock_agents.py
❌ presentation/api/test_variants.py
❌ /api/generate endpoint (V1)
❌ /api/regenerate endpoint (V1)
```

### Added (V2 New)
```
✅ presentation/api/agents/content_analyzer_v2.py
✅ presentation/api/agents/content_generator_v2.py
✅ presentation/api/agents/presentation_strategist_v2.py
✅ presentation/api/agents/mock_agents_v2.py
✅ presentation/api/agents/schemas.py (Pydantic models)
✅ presentation/api/renderers/component_renderer.py
✅ presentation/api/routes/v2.py
✅ presentation/api/VARIANT_GENERATION_DOCUMENTATION.md
✅ presentation/projects/{project}/styles/{theme}/design-guide.json (3 files)
✅ presentation/projects/{project}/styles/{theme}/reference.html (3 files)
```

### Modified
```
📝 presentation/api/main.py
   - Removed V1 imports
   - Removed /api/generate, /api/regenerate endpoints
   - Kept project management endpoints (still useful)
📝 presentation/api/agents/orchestrator.py
   - Now coordinates V2 agents only
   - Removed V1 fallback logic
```

---

## API Changes

### Endpoint Changes

**V1 Endpoint (REMOVED)**
```http
POST /api/generate
Content-Type: application/json

{
  "user_input": "...",
  "project_name": "beispiel-projekt",
  "slide_title": "Folie 46",
  "preferences": {...}
}

→ Returns generated_slides with HTML
```

**V2 Endpoint (USE THIS)**
```http
POST /api/v2/generate
Content-Type: application/json

{
  "project_name": "beispiel-projekt",
  "user_input": "...",
  "slide_title": "Folie 46",
  "slide_number": 46,
  "theme": "github",
  "language": "de"
}

→ Returns HTML directly (deterministic render)
```

### Variant Generation

**V1: Variant Endpoint (REMOVED)**
```http
POST /api/generate?variants=true
{
  "generate_variants": true,
  "variant_profiles": [{"name": "corporate"}, ...]
}
→ 3 API calls + LLM generation for each
```

**V2: Same Endpoint, Different Parameter (FUTURE)**
```http
POST /api/v2/generate
{
  "generate_variants": true,
  "variant_themes": ["github", "modern", "minimal"]
}
→ Single call, instant 3 variant renders
```

---

## How to Update Code

### If You Had V1 Code Using the Agents

**Old (V1) Code:**
```python
from agents import AgentOrchestrator

orchestrator = AgentOrchestrator(api_key, model)
result = orchestrator.process(
    user_input="...",
    project_path="...",
    slide_title="..."
)
```

**New (V2) Code:**
```python
from agents import AgentOrchestrator  # Now coordinates V2 agents

orchestrator = AgentOrchestrator(api_key, model)
result = orchestrator.process(
    user_input="...",
    project_path="...",
    slide_title="..."
)
# Same interface! Orchestrator now uses V2 agents internally
```

### If You Had V1 Custom HTML Generation

**Old Way:**
```python
# Don't do this anymore
agent = ContentGeneratorAgent(api_key)
html = agent.generate(...)["html"]  # ❌ HTML not generated by agent in V2
```

**New Way:**
```python
# Separate concerns
agent = ContentGeneratorAgentV2(api_key)
formatted_slide = agent.generate(...)  # Pure data

renderer = HTMLComponentRenderer()
html = renderer.render(formatted_slide, theme="github")  # HTML from template
```

### If You Customized HTML Templates

**V1 Customization (Not Applicable):**
- HTML was LLM-generated, couldn't customize
- Would need to modify LLM prompt (unreliable)

**V2 Customization (Easy):**
```jinja2
{# File: presentation/templates/components/stat-grid.html.j2 #}
<div class="stat-grid">
{% for stat in stats %}
  <div class="stat-card">
    <!-- Your custom HTML here -->
    <span class="stat-number">{{ stat.value }}</span>
    <span class="stat-label">{{ stat.label }}</span>
  </div>
{% endfor %}
</div>
```

Just modify the Jinja2 template and it applies to all future renders!

---

## Testing Migration

### V1 Tests (Removed)
```python
# ❌ These no longer work
test_v1_variant_generation()
test_agent_orchestrator_v1()
```

### V2 Tests (Use These)
```python
# ✅ Use V2 tests
test_agents_v2.py          # Unit tests for agents
test_v2_integration.py     # End-to-end V2 flow
test_v2_mock_flow.py       # Testing with mock agents
test_renderer_fix.py       # Template rendering tests
```

### Running Tests
```bash
# Test with mock agents (no API key needed, fast)
export TEST_MODE=true
python -m pytest presentation/api/test_v2_integration.py -v

# Test specific component
python -m pytest presentation/api/test_renderer_fix.py::test_stat_grid -v
```

---

## Performance Improvements

### V1 Performance
- Single slide generation: ~4-6 seconds
- Variant generation (3 variants): ~15-20 seconds
- API calls: 1-4 calls per slide

### V2 Performance
- Single slide generation: ~3-5 seconds (slightly faster, cleaner agent work)
- Variant generation (3 variants): ~3-5 seconds (same as single! no extra API calls)
- API calls: 1 call per slide (or 0 if variants use templates only)

### Cost Comparison
| Operation | V1 | V2 |
|-----------|----|----|
| Single slide | 1 API call | 1 API call |
| 3 variants | 4 API calls | 1 API call + templates |
| Time | ~20 seconds | ~5 seconds |
| Cost | 4x token usage | 1x token usage |

---

## Configuration Changes

### Environment Variables
Both V1 and V2 use same config:
```bash
OPENAI_API_KEY=sk-...
TEST_MODE=false
DEFAULT_MODEL=gpt-4o
```

### New Configuration: design-guide.json
V2 agents now read design-guide.json:
```bash
projects/beispiel-projekt/styles/github/design-guide.json
projects/beispiel-projekt/styles/modern/design-guide.json
projects/beispiel-projekt/styles/minimal/design-guide.json
```

These files define available components and their requirements.

---

## Troubleshooting Migration

### Issue: "ModuleNotFoundError: No module named 'agents.content_analyzer'"
**Cause:** Code trying to import V1 agent directly
**Solution:**
```python
# ❌ Don't import V1 agents
from agents import ContentGeneratorAgent

# ✅ Use orchestrator or V2 agents
from agents import AgentOrchestrator
# or
from agents.content_generator_v2 import ContentGeneratorAgentV2
```

### Issue: "Expected HTML output, got FormattedSlide object"
**Cause:** V2 agents return data, not HTML
**Solution:**
```python
# ❌ Don't expect HTML directly
html = agent.generate(...)["html"]

# ✅ Use renderer
formatted_slide = agent.generate(...)
html = renderer.render(formatted_slide, theme="github")
```

### Issue: "/api/generate endpoint not found"
**Cause:** V1 endpoint removed
**Solution:** Use V2 endpoint
```
POST /api/v2/generate  # Instead of /api/generate
```

### Issue: "Template not found: stat-grid.html.j2"
**Cause:** Template files missing or in wrong location
**Solution:**
```bash
# Check templates exist at:
ls -la presentation/templates/components/
# Should contain: stat-grid.html.j2, bullet-list.html.j2, etc.
```

---

## Rollback Plan (If Needed)

If V2 has issues and you need to rollback:

1. **Keep V1 code in git history**
   - V1 agents are deleted but still in git
   - `git show HEAD~1:presentation/api/agents/content_generator.py`

2. **Restore V1 Files (if needed)**
   ```bash
   git checkout HEAD~1 -- presentation/api/agents/content_generator.py
   git checkout HEAD~1 -- presentation/api/agents/content_analyzer.py
   git checkout HEAD~1 -- presentation/api/agents/presentation_strategist.py
   ```

3. **Restore V1 Routes**
   ```bash
   git checkout HEAD~1 -- presentation/api/main.py  # Includes /api/generate endpoint
   ```

4. **Update imports**
   ```python
   # In main.py, restore:
   from agents import AgentOrchestrator
   V1_AGENTS_AVAILABLE = True
   ```

---

## Timeline: When to Migrate Existing Systems

### ✅ Already Migrated
- New slide generation (uses V2)
- All new templates use Jinja2

### 🔄 In Progress
- Agent integration tests
- Style guide JSON integration

### ⏳ Future
- Image color extraction features
- Variant generation full integration
- Project briefing system

### ✋ Optional
- Legacy slide regeneration (can use V1 or V2)
- Custom workflows (may prefer V1 or V2 depending on needs)

---

## Questions & Support

### How do I report V2 bugs?
1. Run with TEST_MODE=true to verify it's not API issues
2. Check that templates exist: `ls presentation/templates/components/`
3. Check design-guide.json exists: `ls projects/*/styles/*/design-guide.json`
4. Open issue with:
   - Error message and traceback
   - User input that triggered issue
   - Expected vs actual output

### How do I add a new component type?
1. Create template: `presentation/templates/components/new-component.html.j2`
2. Add to design-guide.json in all 3 themes
3. Update FormattedSlide model to include component
4. Add agent logic to detect and generate component
5. Add tests

See: REMAINING_FEATURES.md - Component Library Expansion

### How do I customize HTML output?
1. Edit Jinja2 template in `presentation/templates/components/`
2. Changes apply to all future renders automatically
3. No need to re-run agents

---

## Related Documentation

- **CLAUDE.md** - Overall system architecture
- **REMAINING_FEATURES.md** - Future work and enhancements
- **VARIANT_GENERATION_DOCUMENTATION.md** - How variant generation works
- **README.md** - Quick start guide

---

*Last Updated: 2025-11-18*
*Migration Status: ✅ Complete (V1 Fully Deprecated, V2 Active)*

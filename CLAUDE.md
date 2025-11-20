# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A **presentation generation system** with two main components:
1. **Unified Editor Interface** - Single-page web app for creating and previewing slides with live theme switching
2. **AI Agent API** - Multi-agent FastAPI backend for intelligent slide content generation (GPT-4o/GPT-5 support with deterministic Jinja2 rendering)

## Project Structure

```
slide_assistant/
├── archive/                                 # Legacy files (archived)
│   ├── legacy-scripts/
│   │   ├── convert_word_to_markdown.py      # (archived) Word→Markdown converter
│   │   └── markdown-to-components.py        # (archived) Markdown→HTML converter
│   └── legacy-editors/
│       ├── component-viewer.html            # (archived) Old slide viewer
│       └── ai-editor.html                   # (archived) Old AI editor
├── presentation/                            # Main presentation system
│   ├── unified-editor.html                  # NEW: Unified slide editor & viewer UI
│   ├── projects.json                        # Project configuration
│   ├── run_api.py                           # FastAPI server entry point
│   ├── api/                                 # FastAPI backend
│   │   ├── main.py                          # API routes & endpoints
│   │   ├── config.py                        # Configuration & environment
│   │   ├── agents/                          # V2 Multi-agent system (deterministic)
│   │   │   ├── orchestrator.py              # Agent coordinator (V2)
│   │   │   ├── content_analyzer_v2.py       # V2 Content analysis agent
│   │   │   ├── presentation_strategist_v2.py # V2 Strategy recommendation agent
│   │   │   ├── content_generator_v2.py      # V2 Text generation agent (NO HTML)
│   │   │   ├── mock_agents_v2.py            # Testing (TEST_MODE)
│   │   │   ├── schemas.py                   # Pydantic models (FormattedSlide, etc.)
│   │   │   └── VARIANT_GENERATION_DOCUMENTATION.md # V1 archive (reference only)
│   │   ├── renderers/                       # Deterministic HTML rendering
│   │   │   ├── component_renderer.py        # Jinja2 template rendering engine
│   │   │   └── __init__.py
│   │   ├── routes/                          # API routes
│   │   │   ├── v2.py                        # V2 API endpoints
│   │   │   └── __init__.py
│   │   ├── services/                        # Utilities
│   │   │   ├── style_parser.py              # design-guide.json + variables.css parsing
│   │   │   ├── file_service.py              # File management & backups
│   │   │   ├── project_service.py           # Project operations
│   │   │   ├── template_loader.py           # Jinja2 template loader
│   │   │   └── variant_style_parser.py      # Design variant parsing (archived)
│   │   ├── schemas/                         # Blueprint schemas
│   │   │   ├── blueprint.py                 # SlideBlueprintGenerator
│   │   │   └── __init__.py
│   │   ├── tests/                           # Test suite
│   │   │   ├── test_agents_v2.py            # V2 agent tests
│   │   │   ├── test_v2_integration.py       # Integration tests
│   │   │   ├── test_v2_mock_flow.py         # Mock agent flow tests
│   │   │   ├── test_renderer_fix.py         # Renderer tests
│   │   │   ├── test_template_system.py      # Template system tests
│   │   │   ├── test_table_*.py              # Table generation tests (3 files)
│   │   │   ├── test_semantic_*.py           # Semantic framework tests (2 files)
│   │   │   ├── test_pitch_deck_regeneration.py  # Pitch deck tests
│   │   │   └── __init__.py
│   │   └── models/                          # Request/response schemas
│   ├── templates/                           # Jinja2 component templates (NOT in api/)
│   │   ├── components/
│   │   │   ├── stat-grid.html.j2
│   │   │   ├── bullet-list.html.j2
│   │   │   ├── text.html.j2
│   │   │   ├── quote.html.j2
│   │   │   ├── table.html.j2
│   │   │   ├── image-frame.html.j2
│   │   │   ├── image-grid.html.j2
│   │   │   ├── feature-grid.html.j2
│   │   │   ├── process.html.j2
│   │   │   └── process-horizontal.html.j2
│   │   └── wrappers/
│   │       ├── component-wrapper.html.j2
│   │       └── slide-section.html.j2
│   └── projects/                            # Project workspace
│       └── beispiel-projekt/                # Example project
│           ├── html/                        # Generated HTML slides
│           ├── markdown/                    # Markdown sources
│           │   ├── input/                   # Full pitch decks
│           │   └── optimized/               # Per-slide optimized (auto-generated)
│           ├── images/uploads/              # User-uploaded images
│           └── styles/                      # Style themes (github, modern, minimal)
│               ├── github/
│               │   ├── design-guide.json   # Component definitions & design tokens (JSON)
│               │   ├── design-guide.md     # Human-readable design guide
│               │   ├── reference.html      # Canonical component showcase
│               │   ├── style.css           # Theme styles
│               │   └── variables.css       # CSS custom properties (tokens)
│               ├── modern/
│               │   ├── design-guide.json
│               │   ├── design-guide.md
│               │   ├── reference.html
│               │   ├── style.css
│               │   └── variables.css
│               └── minimal/
│                   ├── design-guide.json
│                   ├── design-guide.md
│                   ├── reference.html
│                   ├── style.css
│                   └── variables.css
└── requirements.txt                         # Python dependencies
```

## Key Architecture

### 1. Presentation System (Frontend)

**Purpose:** AI-powered slide generation system with unified editor interface.

**Main Workflow (V2 DETERMINISTIC):**
```
User input (text/stichpunkte) in unified-editor.html
  → /api/v2/generate endpoint
  → 3-Agent Pipeline with Feedback Loop
  → Deterministic Jinja2 Template Rendering
  → Auto-generated HTML + Markdown
  → Live preview in unified-editor.html
```

**Component Types:**
- `stat-grid` - Statistics cards (numbers + labels)
- `bullet-list` - Formatted bullet lists
- `quote` - Highlighted quotes
- `text` - Regular paragraphs with formatting
- `image-frame` - Single image with caption
- `image-grid` - Multiple images in grid layout
- `feature-grid` - Feature cards with icons/emojis
- `table` - Markdown-style tables
- `process` - Vertical process/timeline
- `process-horizontal` - Horizontal process flow

**Unified Editor Features:**
- **unified-editor.html** - Single-page editor combining all functionality:
  - Live slide preview with HTML rendering
  - Fullscreen display mode for presentations (with component width controls)
  - Theme switching (GitHub/Modern/Minimal) without page reload
  - Project and slide management
  - Direct integration with /api/v2/generate endpoint
  - Slide regeneration with variant support
  - Export functionality for individual slides or entire decks
  - Compact component editing in side-by-side layout

### 2. Multi-Agent API System (`presentation/api/`) - V2 ARCHITECTURE

**Purpose:** AI-powered intelligent slide content generation using OpenAI GPT-4o/GPT-5 with deterministic HTML rendering.

**V2 Architecture (CURRENT - DETERMINISTIC):**
```
User Input + Project Context
    ↓
ContentAnalyzerAgentV2 (LLM)
  ├─ Analyzes content structure
  ├─ Detects statistics, lists, quotes
  ├─ Auto-detects language (German/English)
  └─ Outputs: ContentBlock[] with metadata
    ↓
PresentationStrategistAgentV2 (LLM) ←──────┐
  ├─ Plans component types & layout     │ Feedback Loop
  ├─ References design-guide.json        (if validation fails)
  └─ Outputs: SlideBlueprintGenerator   │
    ↓─────────────────────────────────────┘
ContentGeneratorAgentV2 (LLM)
  ├─ Generates formatted text (NO HTML!)
  ├─ Respects slide blueprint
  ├─ Validates against component schemas
  └─ Outputs: FormattedSlide (pure data)
    ↓
HTMLComponentRenderer (JINJA2 - NO LLM)
  ├─ Renders templates from FormattedSlide
  ├─ Applies theme tokens from design-guide.json
  ├─ Generates deterministic HTML
  └─ Outputs: HTML string
    ↓
FileService (save to project structure)
    ↓
Response (HTML + Markdown + metadata)
```

**Key V2 Improvements:**
- ✅ **Deterministic HTML:** Templates ensure consistent output
- ✅ **Feedback Loop:** Agent 2 can adjust plan if Agent 3 validation fails
- ✅ **Type Safety:** Pydantic models for all data structures
- ✅ **No HTML in LLM:** Agents generate pure data, not code
- ✅ **Instant Variants:** 3 theme variants in same time as 1 slide (no extra API calls)
- ✅ **Design System:** design-guide.json drives all styling decisions

**Agent Features:**
- **Language Auto-Detection:** German & English automatically detected and matched
- **GPT-5 Support:** `reasoning_effort` and `verbosity` controls for cost/quality optimization
- **Pydantic Structured Outputs:** Type-safe JSON responses via schemas.py
- **Style-Aware:** Respects design-guide.json and theme-specific tokens
- **Variant Generation:** Optional 3 design variants (instant, no extra API calls)
- **Feedback Loop:** Agent 2 can replan if Agent 3 validation fails

**Key Capabilities:**
- Intelligent content type detection (statistics, narrative, lists, quotes, tables, process, etc.)
- Automatic statistics recognition (handles €, %, Mio, Mrd, K, M, B formats)
- Multi-language content generation (German & English)
- Image integration with standardized image frames
- Backup & version management
- Multi-line stat labels with source attribution
- Phased timeline structures
- Icon/emoji preservation
- Markdown table detection

### 3. Projects System

**Configuration:** `projects.json` defines project structure and available styles.

Each project has:
- Multiple markdown sources (input + optimized per slide)
- Generated HTML components
- Style variations (GitHub Design, Modern, Minimal)
- Design-specific variables in `styles/{theme}/variables.css`

**Dynamic Style Loading:** Viewers switch themes at runtime via dropdown.

## Development Commands

### Root Setup
```bash
# Install main dependencies (Word converter)
pip install -r requirements.txt
```

### API Development Setup
```bash
cd presentation/api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY
```

### Running the API Server
```bash
cd presentation

# Activate venv (if not already)
source api/venv/bin/activate

# Start server
python3 run_api.py
# Server runs at http://localhost:8001
# Health check: curl http://localhost:8001/health
```

### Testing (Mock Mode - V2)
```bash
cd presentation/api

# Set TEST_MODE to use mock agents (no API key needed)
export TEST_MODE=true

# Run V2 integration tests
python3 -m pytest tests/test_agents_v2.py -v
python3 -m pytest tests/test_v2_integration.py -v
python3 -m pytest tests/test_v2_mock_flow.py -v

# Run renderer tests
python3 -m pytest tests/test_renderer_fix.py -v

# Run all tests
python3 -m pytest tests/test_*.py -v
```

**Note:** V1 tests have been removed. See MIGRATION_GUIDE.md for upgrading existing code.

### Using the Unified Editor
```bash
# 1. Start API server
cd presentation
python3 run_api.py
# Server runs at http://localhost:8001

# 2. Open unified editor in browser
# Option A: Direct file access (may have CORS issues)
# file:///path/to/presentation/unified-editor.html

# Option B: Local server (recommended)
python3 -m http.server 8000
# Then visit: http://localhost:8000/unified-editor.html
```

## Important Technical Details

### Archived Legacy Tools
The following tools have been moved to `archive/` and are no longer actively maintained:
- **convert_word_to_markdown.py** - Word→Markdown converter (archived in archive/legacy-scripts/)
- **markdown-to-components.py** - Old Markdown→HTML converter (archived in archive/legacy-scripts/)
- **component-viewer.html** - Old standalone viewer (archived in archive/legacy-editors/)
- **ai-editor.html** - Old AI editor interface (archived in archive/legacy-editors/)

These have been replaced by the unified-editor.html which combines all functionality.

### Template System
- **Location:** `presentation/templates/` (NOT in api/)
- **Loader:** `services/template_loader.py` handles Jinja2 template loading
- **Components:** 10 component types in `templates/components/*.html.j2`
- **Wrappers:** Component and slide wrappers in `templates/wrappers/*.html.j2`
- **Rendering:** `renderers/component_renderer.py` converts FormattedSlide → HTML

### Multi-Agent API System

**Configuration (presentation/api/config.py):**
- `TEST_MODE`: When True, uses mock agents (for testing without API)
- `OPENAI_API_KEY`: From `.env` file (required for production)
- Default model: `gpt-4o` (can override to `gpt-5` or `gpt-5-mini`)

**Key Classes:**
- **AgentOrchestrator** (orchestrator.py): Coordinates all agents, handles test mode
- **ContentAnalyzerAgentV2** (content_analyzer_v2.py): Analyzes user input, detects language & content type
- **PresentationStrategistAgentV2** (presentation_strategist_v2.py): Recommends layout & components
- **ContentGeneratorAgentV2** (content_generator_v2.py): Generates formatted text (NO HTML)
- **MockAgentsV2** (mock_agents_v2.py): Fake agents for testing (TEST_MODE)

**Agent Parameters:**
- `reasoning_effort`: `minimal|low|medium|high` (GPT-5 only, saves cost/improves quality)
- `verbosity`: `minimal|low|medium|high` (Controls output verbosity)
- `use_structured_outputs`: Boolean (Enables Pydantic schema validation)

**Language Support:**
- Auto-detects German or English from user input
- Generates output in the detected language
- JSON field names always in English (content_type, key_messages, etc.)
- Content values match input language

**File Service:**
- Saves generated markdown to `projects/{name}/markdown/optimized/folie-{NN}-{title}.md`
- Saves generated HTML to `projects/{name}/html/folie-{NN}-{title}.html`
- Creates backups before regeneration
- Auto-creates missing directories

### Known Issues

None currently. Previous mock agent parameter issue has been resolved (mock_agents_v2.py now uses **kwargs).

## File Naming Conventions

- Markdown input: Any name (`pitch.md`, `pitch-deck.md`)
- Optimized markdown: `folie-{NN}-{descriptor}.md` (e.g., `folie-01-problem.md`)
- HTML output: `folie-{NN}-{descriptor}.html` (matches optimized markdown)
- Use lowercase, hyphens for spaces, German naming

## CSS and Styling

The system uses three style themes:
1. **GitHub Design** (default) - Professional, clean, green accent (#238636)
2. **Modern** - Contemporary design variation
3. **Minimal** - Simplified, minimal styling

Styles are project-specific and located in `projects/{name}/styles/{theme}/style.css`.

The main template CSS is `github-presentation-template.css` in the presentation root.

## Git Workflow

Main branch: `master`

When committing:
- Focus on functional changes
- Document architectural shifts
- Keep markdown sources in version control
- Generated HTML can be gitignored if desired
- Use descriptive commit messages with context

## Common Gotchas & Troubleshooting

### API & Testing
1. **TEST_MODE vs Production:**
   - TEST_MODE=true uses mock agents (no OpenAI API needed)
   - TEST_MODE=false requires valid OPENAI_API_KEY in .env
   - Check presentation/api/config.py for current mode

2. **OPENAI_API_KEY not found:**
   - Ensure presentation/api/.env exists and contains OPENAI_API_KEY
   - Try: `cp presentation/api/.env.example presentation/api/.env`
   - Then edit .env to add your actual API key

### Frontend & Viewing
3. **CORS Issues:** unified-editor.html may require local server
   - Use: `python3 -m http.server 8000` in presentation directory
   - Then visit: http://localhost:8000/unified-editor.html

4. **Component IDs:** Must follow format `slide-{X}-comp-{Y}`
   - Auto-generated by API's component_renderer.py
   - Ensures unique IDs for each component on each slide

5. **Style Paths:** Relative to project. Check projects.json for correct theme paths
   - Example: `projects/beispiel-projekt/styles/github/style.css`

6. **Template Paths:** Templates in `presentation/templates/`, NOT `presentation/api/templates/`
   - Component renderer uses template_loader.py to find templates
   - Template path is relative to presentation/ directory

### Content Generation
7. **Statistics Detection:** Requires units for auto-detection
   - Regex: `\d+[.,\d]*\s*(Mio|Mrd|%|€|$|USD)`
   - Example: "€12,3 Mio" ✅, "12.3 million" ❌

8. **Language Mixing:** API auto-detects primary language
   - Mostly German + one English term? Output in German
   - Use consistent language for best results

### Development
9. **API Venv Location:** API has its own venv
    - Location: presentation/api/venv
    - Dependencies: FastAPI, OpenAI, Jinja2, Pydantic

10. **Image Paths:** Images saved to `projects/{name}/images/uploads/`
    - Generated HTML references this path
    - Ensure project exists before uploading

11. **Python Dependencies:**
    - Root requirements.txt: Minimal (python-docx if Word converter was active)
    - API requirements: presentation/api/requirements.txt (fastapi, uvicorn, openai, pydantic, jinja2)

## Development Tips

- Test mock agents in isolation with: `python3 -m pytest presentation/api/tests/test_agents_v2.py -v`
- Use TEST_MODE=true for development/testing (no API costs)
- Use GPT-5-mini for cost control, GPT-5 for complex strategy
- Enable structured_outputs for production code (type safety)
- German content generation: Set slide_title in German for better context
- Keep components focused (1 idea per component)
- Use pixel-perfect screenshots: Browser DevTools element inspector + 100% zoom
- Batch test: `python3 -m pytest presentation/api/tests/test_*.py -v -k keyword`

## V2 Architecture & Recent Changes (2025-11-18)

### Key Updates
- ✅ **V1 Deprecated:** LLM-based HTML generation completely removed
- ✅ **V2 Active:** Deterministic Jinja2-based HTML rendering (no LLM)
- ✅ **Design Guides Created:** design-guide.json for github, modern, minimal themes
- ✅ **Reference HTML:** Canonical component examples for all themes
- ✅ **Variant Support:** Instant 3-variant generation (no extra API calls)

### Removed Files
- `presentation/api/agents/content_analyzer.py` (V1)
- `presentation/api/agents/content_generator.py` (V1)
- `presentation/api/agents/presentation_strategist.py` (V1)
- `presentation/api/agents/mock_agents.py` (V1)
- API endpoints: `/api/generate`, `/api/regenerate` (use `/api/v2/generate` instead)

### New Files
- `presentation/api/agents/content_analyzer_v2.py`
- `presentation/api/agents/content_generator_v2.py`
- `presentation/api/agents/presentation_strategist_v2.py`
- `presentation/api/renderers/component_renderer.py` (Jinja2 renderer)
- `presentation/api/routes/v2.py` (V2 API endpoints)
- `projects/beispiel-projekt/styles/{theme}/design-guide.json` (3 files)
- `projects/beispiel-projekt/styles/{theme}/reference.html` (3 files)

### Migration & Documentation
See the following files for detailed information:
- **MIGRATION_GUIDE.md** - How to update code from V1 to V2
- **REMAINING_FEATURES.md** - Future enhancements (image colors, variants in V2, etc.)
- **presentation/api/VARIANT_GENERATION_DOCUMENTATION.md** - V1 variant logic (archived reference)

### Design System Integration
All three themes now have structured design-guide.json files defining:
- **Tokens**: Colors, typography, spacing, border radius, shadows
- **Components**: 10 component types with slots and CSS classes
- **Layouts**: Standard layout patterns (1-3 components)
- **Best Practices**: Component-specific guidance

View reference slides at:
- `projects/beispiel-projekt/styles/github/reference.html`
- `projects/beispiel-projekt/styles/modern/reference.html`
- `projects/beispiel-projekt/styles/minimal/reference.html`

### API Changes
**Old Endpoint (REMOVED):**
```http
POST /api/generate
```

**New Endpoint (USE THIS):**
```http
POST /api/v2/generate
{
  "project_name": "beispiel-projekt",
  "user_input": "...",
  "slide_title": "Folie 46",
  "slide_number": 46,
  "theme": "github",
  "language": "de"
}
```

### Performance Improvements
| Metric | V1 | V2 |
|--------|----|----|
| Single Slide | ~4-6s | ~3-5s |
| 3 Variants | ~15-20s | ~3-5s |
| API Calls | 1-4 | 1 |
| Cost | 4x tokens | 1x tokens |

### Current Limitations

1. **design-guide.json partial integration**
   - Files created ✅
   - Agents still need to read and validate against them for improved recommendations
   - See: REMAINING_FEATURES.md task #6

2. **Image color extraction**
   - Not yet implemented for automatic color scheme matching
   - Reference: REMAINING_FEATURES.md task #1
   - Requires: pillow + colorthief

3. **Variant generation**
   - Currently: Each theme manually configured
   - Future: FormattedSlide renders with different themes for instant variants
   - See: REMAINING_FEATURES.md for roadmap

## Questions?

- Struggling with V1→V2 migration? → See MIGRATION_GUIDE.md
- Want to implement new features? → See REMAINING_FEATURES.md
- Need variant logic reference? → See VARIANT_GENERATION_DOCUMENTATION.md
- Questions about agents? → Check agents/*.py docstrings
- Questions about templates? → Check presentation/templates/components/*.j2

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A **presentation generation system** with three main components:
1. **Word-to-Markdown converter** - Converts .docx files to Markdown (preserves exact content)
2. **Component-based presentation system** - Markdown → HTML components for screenshot-friendly pitch decks
3. **AI Agent API** - Multi-agent FastAPI backend for intelligent slide content generation (GPT-4o/GPT-5 support)

## Project Structure

```
slide_assistant/
├── convert_word_to_markdown.py              # Word→Markdown converter
├── presentation/                            # Main presentation system
│   ├── component-viewer.html                # Slide viewer & editor UI
│   ├── ai-editor.html                       # AI content generation UI
│   ├── markdown-to-components.py            # Markdown→HTML converter (Python)
│   ├── projects.json                        # Project configuration
│   ├── run_api.py                           # FastAPI server entry point
│   ├── api/                                 # FastAPI backend
│   │   ├── main.py                          # API routes & endpoints
│   │   ├── config.py                        # Configuration & environment
│   │   ├── agents/                          # Multi-agent system
│   │   │   ├── orchestrator.py              # Agent coordinator
│   │   │   ├── content_analyzer.py          # Content analysis agent
│   │   │   ├── presentation_strategist.py   # Strategy recommendation agent
│   │   │   ├── content_generator.py         # HTML/Markdown generation agent
│   │   │   ├── mock_agents.py               # Testing (TEST_MODE)
│   │   │   └── schemas.py                   # Pydantic models for structured outputs
│   │   ├── services/                        # Utilities
│   │   │   ├── style_parser.py              # Project style guide parsing
│   │   │   ├── file_service.py              # File management
│   │   │   ├── project_service.py           # Project operations
│   │   │   └── variant_style_parser.py      # Design variant parsing
│   │   └── models/                          # Request/response schemas
│   └── projects/                            # Project workspace
│       └── beispiel-projekt/                # Example project
│           ├── html/                        # Generated HTML slides
│           ├── markdown/                    # Markdown sources
│           │   ├── input/                   # Full pitch decks
│           │   └── optimized/               # Per-slide optimized (auto-generated)
│           ├── images/uploads/              # User-uploaded images
│           └── styles/                      # Style themes (github, modern, minimal)
└── requirements.txt                         # Python dependencies
```

## Key Architecture

### 1. Word-to-Markdown Converter (`convert_word_to_markdown.py`)

**Purpose:** Preserves exact word-for-word content from .docx files while converting to Markdown.

**Key Features:**
- Maintains formatting: bold, italic, underline, hyperlinks
- Handles headings (Heading 1-6 → `#` syntax)
- Converts bullet lists and numbered lists
- Converts tables to Markdown tables
- Preserves document element order

**Usage:**
```bash
# Single file
python convert_word_to_markdown.py dokument.docx [ausgabe.md]

# Batch conversion
python convert_word_to_markdown.py --folder ./documents
```

### 2. Presentation System (Frontend)

**Purpose:** Converts Markdown pitch decks into screenshot-ready HTML components for PowerPoint/Keynote.

**Static Workflow (Manual):**
```
Markdown (H1 = slide, H2 = component)
  → LLM-PROMPT.md (Claude/ChatGPT)
  → Manual HTML in projects/{name}/html/
  → component-viewer.html for viewing/screenshots
```

**Dynamic Workflow (AI-Powered - via API):**
```
User input (text/stichpunkte)
  → /api/generate endpoint
  → Multi-agent pipeline
  → Auto-generated HTML + Markdown
  → ai-editor.html for preview
```

**Component Types:**
- `stat-grid` - Statistics cards (numbers + labels)
- `bullet-list` - Formatted bullet lists
- `quote` - Highlighted quotes
- `text` - Regular paragraphs with formatting
- `image` - User-uploaded images

**Tools:**
- **component-viewer.html** - View/screenshot existing components
- **ai-editor.html** - Generate new content via API
- **markdown-to-components.py** - Batch Python conversion

### 3. Multi-Agent API System (`presentation/api/`)

**Purpose:** AI-powered intelligent slide content generation using OpenAI GPT-4o/GPT-5.

**Architecture:**
```
User Input
    ↓
ContentAnalyzerAgent (analyze content type, extract key messages)
    ↓
PresentationStrategistAgent (recommend components, layout, styling)
    ↓
ContentGeneratorAgent (generate HTML + Markdown)
    ↓
FileService (save to project structure)
    ↓
Response (HTML + Markdown + component metadata)
```

**Agent Features:**
- **Language Auto-Detection:** German & English automatically detected and matched
- **GPT-5 Support:** `reasoning_effort` and `verbosity` controls for cost/quality optimization
- **Pydantic Structured Outputs:** Type-safe JSON responses (optional, opt-in)
- **Style-Aware:** Respects project design system and style guides
- **Variant Generation:** Optional 3 design variants per slide

**Key Capabilities:**
- Intelligent content type detection (statistics, narrative, lists, quotes, mixed)
- Automatic statistics recognition (handles €, %, Mio, Mrd formats)
- Multi-language content generation
- Image integration for uploaded files
- Backup & version management

### 4. Projects System

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

### Testing (Mock Mode)
```bash
cd presentation/api

# Set TEST_MODE to use mock agents (no API key needed)
export OPENAI_API_KEY=mock

# Run tests
python3 -m pytest test_*.py -v

# Test with mock agents only (no OpenAI calls)
python3 test_agents.py
```

### Word Document Conversion
```bash
# Single file
python convert_word_to_markdown.py dokument.docx [ausgabe.md]

# Batch conversion
python convert_word_to_markdown.py --folder ./path/to/docs
```

### Markdown-to-HTML Conversion (Local)
```bash
# Python script (no API needed)
python presentation/markdown-to-components.py input.md presentation/output/
```

### Viewing Presentations
```bash
# Static component viewer (works offline)
# Open in browser: file:///path/to/presentation/component-viewer.html

# AI Editor (requires API server running)
# 1. Start API: python3 presentation/run_api.py
# 2. Open: file:///path/to/presentation/ai-editor.html
# 3. API will be called at http://localhost:8001/api/generate

# Local server for CORS issues
cd presentation
python3 -m http.server 8000
# Then visit: http://localhost:8000/component-viewer.html
```

## Important Technical Details

### Word Converter
- Uses `python-docx` library
- Extracts hyperlinks via XML relationships
- Handles standard styles and custom formatting
- Preserves element order via `doc.element.body` iteration

### Markdown-to-Components Script
- Parses H1 as slide boundaries, H2 as component boundaries
- Auto-detects statistics (numbers with units: Mio, Mrd, %, €, $, USD)
- Generates unique component IDs: `slide-{X}-comp-{Y}`
- Outputs HTML with embedded CSS

### Multi-Agent API System

**Configuration (presentation/api/config.py):**
- `TEST_MODE`: When True, uses mock agents (for testing without API)
- `OPENAI_API_KEY`: From `.env` file (required for production)
- Default model: `gpt-4o` (can override to `gpt-5` or `gpt-5-mini`)

**Key Classes:**
- **AgentOrchestrator** (orchestrator.py): Coordinates all agents, handles test mode
- **ContentAnalyzerAgent** (content_analyzer.py): Analyzes user input, detects language & content type
- **PresentationStrategistAgent** (presentation_strategist.py): Recommends layout & components
- **ContentGeneratorAgent** (content_generator.py): Generates HTML + Markdown output
- **MockAgents** (mock_agents.py): Fake agents for testing (⚠️ See below for known issue)

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

**Mock Agent Parameter Issue:**
- Mock agents don't accept `reasoning_effort`, `verbosity`, `use_structured_outputs` parameters
- The orchestrator passes these when in TEST_MODE, causing `TypeError`
- **Fix:** Update mock_agents.py to accept and ignore these parameters in `__init__` methods
- See: presentation/api/agents/mock_agents.py:8, :45, :87

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

Current branch: `master` (also the main branch)

Recent changes show:
- Deleted legacy `pitch/` content
- Added new `presentation/` system
- Established projects-based architecture
- Added component viewer with dynamic loading

When committing:
- Focus on functional changes
- Document architectural shifts
- Keep markdown sources in version control
- Generated HTML can be gitignored if desired

## Common Gotchas & Troubleshooting

### API & Testing
1. **Mock Agent TypeError:** Mock agents missing parameter support
   - Error: `MockContentAnalyzerAgent.__init__() got an unexpected keyword argument 'reasoning_effort'`
   - Cause: TEST_MODE agents don't accept new parameters (reasoning_effort, verbosity, use_structured_outputs)
   - Fix: Update mock_agents.py to accept **kwargs or add explicit parameters

2. **TEST_MODE vs Production:**
   - TEST_MODE=true uses mock agents (no OpenAI API needed)
   - TEST_MODE=false requires valid OPENAI_API_KEY in .env
   - Check presentation/api/config.py for current mode

3. **OPENAI_API_KEY not found:**
   - Ensure presentation/api/.env exists and contains OPENAI_API_KEY
   - Try: `cp presentation/api/.env.example presentation/api/.env`
   - Then edit .env to add your actual API key

### Frontend & Viewing
4. **CORS Issues:** Custom HTML files require local server
   - Use: `python3 -m http.server 8000` in presentation directory
   - Then visit: http://localhost:8000/component-viewer.html

5. **Component IDs:** Must follow format `slide-{X}-comp-{Y}` for viewer
   - Auto-generated by API and Python converter
   - Manual HTML needs proper IDs for viewer to recognize them

6. **Style Paths:** Relative to project. Check projects.json for correct theme paths
   - Example: `projects/beispiel-projekt/styles/github/style.css`

### Content Generation
7. **Markdown Format:** H1 = slide, H2 = component (strict parsing)
   - Deviate from this and parser fails silently

8. **Statistics Detection:** Requires units for auto-detection
   - Regex: `\d+[.,\d]*\s*(Mio|Mrd|%|€|$|USD)`
   - Example: "€12,3 Mio" ✅, "12.3 million" ❌

9. **Language Mixing:** API auto-detects primary language
   - Mostly German + one English term? Output in German
   - Use consistent language for best results

### Development
10. **API Venv Location:** Separate venv for API only
    - Location: presentation/api/venv
    - Root venv for Word converter: ./venv
    - Keep them separate to avoid dependency conflicts

11. **Image Paths:** Images saved to `projects/{name}/images/uploads/`
    - Generated HTML references this path
    - Ensure project exists before uploading

12. **Python Dependencies:**
    - Root requirements: python-docx, fastapi, uvicorn, openai, pydantic
    - Install both root and API requirements

## Development Tips

- Test mock agents in isolation with: `python3 -m pytest presentation/api/test_agents.py -v`
- Use TEST_MODE=true for development/testing (no API costs)
- Use GPT-5-mini for cost control, GPT-5 for complex strategy
- Enable structured_outputs for production code (type safety)
- German content generation: Set slide_title in German for better context
- Keep components focused (1 idea per component)
- Use pixel-perfect screenshots: Browser DevTools element inspector + 100% zoom
- Batch test: `python3 -m pytest presentation/api/test_*.py -v -k keyword`

# Slide Assistant AI API (V2)

FastAPI-based backend for AI-powered presentation slide content generation with **deterministic HTML rendering**.

## Features

- **V2 Deterministic Architecture**: 3-agent pipeline with Jinja2 template rendering
- **OpenAI GPT-4o/GPT-5 Integration**: Intelligent content analysis and strategy
- **Template-Based HTML**: No LLM-generated HTML - pure Jinja2 templates
- **Design System Integration**: Respects design-guide.json and theme tokens
- **Feedback Loop**: Agent 2 can replan if Agent 3 validation fails
- **Multi-Language Support**: German & English auto-detection
- **Type-Safe**: Pydantic models throughout (FormattedSlide, schemas)
- **Instant Variants**: 3 theme variants in single generation (no extra API calls)

## V2 Architecture

```
User Input + Project Context
    ↓
ContentAnalyzerAgentV2 (LLM)
  ├─ Analyzes content structure
  ├─ Detects statistics, lists, quotes, tables
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

### Key V2 Improvements vs V1

| Feature | V1 (Deprecated) | V2 (Current) |
|---------|----------------|--------------|
| HTML Generation | LLM-generated HTML | Jinja2 templates |
| Consistency | Variable output | Deterministic |
| Feedback Loop | No | Yes (Agent 2 ↔ 3) |
| Type Safety | Partial | Full (Pydantic) |
| Variants | 3x API calls | 1x API call |
| Speed | ~15-20s (3 variants) | ~3-5s |
| Cost | 4x tokens | 1x tokens |

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (for production)
- TEST_MODE=true (for development without API)

### Installation

1. Create virtual environment:
```bash
cd presentation/api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add OPENAI_API_KEY
```

### Running the Server

```bash
cd presentation
python3 run_api.py

# Server runs at http://localhost:8001
# Health check: curl http://localhost:8001/health
```

## API Endpoints

### V2 Endpoints (Current)

#### POST /api/v2/generate
Generate slide content with V2 deterministic architecture.

**Request:**
```json
{
  "project_name": "beispiel-projekt",
  "user_input": "3 Hauptvorteile unserer Lösung:\n- Schnell\n- Sicher\n- Einfach",
  "slide_title": "Folie 12: Vorteile",
  "slide_number": 12,
  "theme": "github",
  "language": "de"
}
```

**Response:**
```json
{
  "html": "<div class='slide-section'>...</div>",
  "markdown": "## Folie 12\n...",
  "metadata": {
    "components": ["bullet-list"],
    "language": "de",
    "theme": "github"
  },
  "file_paths": {
    "html": "projects/beispiel-projekt/html/folie-12-vorteile.html",
    "markdown": "projects/beispiel-projekt/markdown/optimized/folie-12-vorteile.md"
  }
}
```

### Legacy Endpoints (Removed)

- ❌ `/api/generate` - Use `/api/v2/generate` instead
- ❌ `/api/regenerate` - Merged into `/api/v2/generate`

## Project Structure

```
presentation/api/
├── main.py                           # FastAPI app entry point
├── config.py                         # Configuration (TEST_MODE, API keys)
├── agents/                           # V2 Multi-agent system
│   ├── orchestrator.py               # Coordinates all agents
│   ├── content_analyzer_v2.py        # Content analysis (LLM)
│   ├── presentation_strategist_v2.py # Strategy planning (LLM)
│   ├── content_generator_v2.py       # Text generation (LLM)
│   ├── mock_agents_v2.py             # Mock agents for TEST_MODE
│   └── schemas.py                    # Pydantic models (FormattedSlide, etc.)
├── renderers/                        # Deterministic HTML rendering
│   └── component_renderer.py         # Jinja2 template engine (NO LLM)
├── routes/                           # API endpoints
│   └── v2.py                         # V2 API routes
├── services/                         # Utilities
│   ├── file_service.py               # File management & backups
│   ├── project_service.py            # Project operations
│   ├── style_parser.py               # design-guide.json parser
│   └── template_loader.py            # Jinja2 template loader
├── schemas/                          # Blueprint schemas
│   └── blueprint.py                  # SlideBlueprintGenerator
├── tests/                            # Test suite
│   ├── test_agents_v2.py             # V2 agent tests
│   ├── test_v2_integration.py        # Integration tests
│   ├── test_renderer_fix.py          # Renderer tests
│   └── ... (11 test files total)
└── models/                           # Request/response schemas
```

## Testing

### Mock Mode (No API Key Required)

```bash
cd presentation/api

# Enable TEST_MODE
export TEST_MODE=true

# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_v2_integration.py -v

# Run specific test
python3 -m pytest tests/test_renderer_fix.py::test_stat_grid -v
```

### Production Mode

```bash
# Requires OPENAI_API_KEY in .env
export TEST_MODE=false

# Run integration tests with real API
python3 -m pytest tests/test_semantic_e2e_gpt4o.py -v
```

## Component Types

The V2 system supports 10 component types via Jinja2 templates:

1. **stat-grid** - Statistics cards (numbers + labels, multi-line support)
2. **bullet-list** - Formatted bullet lists (nested, icons, emojis)
3. **quote** - Highlighted quotes with attribution
4. **text** - Regular paragraphs with rich formatting
5. **table** - Markdown-style tables
6. **image-frame** - Single image with caption
7. **image-grid** - Multiple images in grid layout
8. **feature-grid** - Feature cards with icons/emojis
9. **process** - Vertical process/timeline
10. **process-horizontal** - Horizontal process flow

Templates: `presentation/templates/components/*.html.j2`

## Configuration

### Environment Variables (.env)

```bash
# Required for production
OPENAI_API_KEY=sk-...

# Optional
TEST_MODE=false              # Set to true for mock agents
DEFAULT_MODEL=gpt-4o         # Or gpt-5, gpt-5-mini
ANTHROPIC_API_KEY=...        # Future support
```

### config.py Settings

```python
# Content Generation Limits
MAX_COMPONENTS_PER_SLIDE = 3
MAX_SLIDES_PER_REQUEST = 10

# Model Configuration
DEFAULT_MODEL = "gpt-4o"
TIMEOUT = 60
```

## Agent Parameters

V2 agents support GPT-5 advanced controls:

```python
orchestrator = AgentOrchestrator(
    project_name="beispiel-projekt",
    reasoning_effort="medium",    # minimal|low|medium|high (GPT-5 only)
    verbosity="low",              # minimal|low|medium|high
    use_structured_outputs=True   # Enable Pydantic schema validation
)
```

## Troubleshooting

### Common Issues

1. **OPENAI_API_KEY not found**
   - Ensure `presentation/api/.env` exists
   - Check `.env` contains valid API key
   - Try: `cp .env.example .env`

2. **Mock agents TypeError**
   - If mock agents fail with parameter errors, check `mock_agents_v2.py`
   - Ensure `__init__` accepts new parameters (reasoning_effort, verbosity, etc.)

3. **Template not found**
   - Templates are in `presentation/templates/` (NOT `presentation/api/templates/`)
   - Check `template_loader.py` for correct paths

4. **Import errors**
   - Ensure `__init__.py` exists in `schemas/` and `tests/`
   - Run from `presentation/` directory, not `presentation/api/`

## Migration from V1

See [MIGRATION_GUIDE.md](../../MIGRATION_GUIDE.md) for detailed V1→V2 migration instructions.

**Quick summary:**
- Replace `/api/generate` → `/api/v2/generate`
- No more direct HTML in LLM prompts
- FormattedSlide replaces HTML strings
- Templates handle all HTML rendering

## Documentation

- **V2_ARCHITECTURE.md** - Detailed V2 architecture documentation
- **SEMANTIC_FRAMEWORK.md** - Content semantic classification
- **agents/README.md** - Agent system documentation
- **../../CLAUDE.md** - Full project documentation (includes API section)

## Development

### Adding New Component Type

1. Create Jinja2 template: `presentation/templates/components/my-component.html.j2`
2. Update `schemas.py` with component data model
3. Add to `component_renderer.py` component_type_map
4. Update design-guide.json with component definition
5. Add tests in `tests/test_template_system.py`

### Running Development Server with Auto-Reload

```bash
cd presentation
uvicorn api.main:app --reload --host localhost --port 8001
```

## License

See repository root for license information.

## Support

For issues and questions:
- Check [CLAUDE.md](../../CLAUDE.md) troubleshooting section
- Review [REMAINING_FEATURES.md](../../REMAINING_FEATURES.md) for known limitations
- Open GitHub issue with reproduction steps

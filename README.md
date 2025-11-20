# Slide Assistant

AI-powered presentation slide content generation system with deterministic HTML rendering.

## Overview

Slide Assistant is a V2 deterministic architecture for creating professional presentation slides using:
- **3-Agent AI Pipeline** (GPT-4o/GPT-5) for intelligent content analysis and strategy
- **Jinja2 Template Rendering** for consistent, deterministic HTML output
- **Unified Editor Interface** for live preview and theme switching
- **Design System Integration** with design-guide.json and CSS tokens

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (or use TEST_MODE for development)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd slide_assistant
```

2. **Set up the API backend:**
```bash
cd presentation/api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Server

```bash
cd presentation
python3 run_api.py
```

Server runs at: `http://localhost:8001`

### Using the Unified Editor

1. Start the API server (see above)
2. Open `presentation/unified-editor.html` in your browser
3. Enter slide content and generate!

**Or use a local server to avoid CORS issues:**
```bash
cd presentation
python3 -m http.server 8000
# Visit: http://localhost:8000/unified-editor.html
```

## Features

### V2 Architecture

- ✅ **Deterministic HTML** - Jinja2 templates ensure consistent output
- ✅ **Feedback Loop** - Agent 2 can replan if Agent 3 validation fails
- ✅ **Type-Safe** - Full Pydantic models throughout
- ✅ **No LLM HTML** - Agents generate pure data, templates render HTML
- ✅ **Instant Variants** - 3 theme variants in same time as 1 slide
- ✅ **Multi-Language** - German & English auto-detection

### Component Types

10 professionally designed component types:
- `stat-grid` - Statistics with multi-line labels
- `bullet-list` - Nested lists with icons
- `quote` - Highlighted quotes
- `text` - Rich formatted text
- `table` - Markdown tables
- `image-frame` - Single images
- `image-grid` - Image galleries
- `feature-grid` - Feature cards
- `process` - Vertical timelines
- `process-horizontal` - Horizontal flows

### Themes

3 built-in professional themes:
- **GitHub Design** - Clean, professional (default)
- **Modern** - Contemporary styling
- **Minimal** - Simple, focused

## Project Structure

```
slide_assistant/
├── presentation/
│   ├── unified-editor.html          # Main UI
│   ├── run_api.py                   # API server starter
│   ├── api/                         # FastAPI backend (V2)
│   ├── templates/                   # Jinja2 templates
│   └── projects/
│       └── beispiel-projekt/        # Example project
└── archive/                         # Legacy files (archived)
```

## Usage Examples

### API Request Example

```bash
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "user_input": "3 Hauptvorteile:\n- Schnell\n- Sicher\n- Einfach",
    "slide_title": "Folie 12",
    "slide_number": 12,
    "theme": "github",
    "language": "de"
  }'
```

### Python Example

```python
from presentation.api.agents.orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator(
    project_name="beispiel-projekt",
    reasoning_effort="medium",
    use_structured_outputs=True
)

# Generate slide
result = orchestrator.generate_slide(
    user_input="3 main benefits: Fast, Secure, Simple",
    slide_title="Slide 12",
    slide_number=12,
    theme="github"
)

print(result.html)  # Generated HTML
print(result.markdown)  # Generated Markdown
```

## Testing

### Quick Test (Mock Mode)

```bash
cd presentation/api
export TEST_MODE=true
python3 -m pytest tests/ -v
```

No API key required! See [TESTING.md](TESTING.md) for complete testing guide.

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete project documentation for Claude Code
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
- **[presentation/api/README.md](presentation/api/README.md)** - API documentation
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - V1 → V2 migration guide
- **[REMAINING_FEATURES.md](REMAINING_FEATURES.md)** - Future enhancements

## Architecture

```
User Input → Agent 1 (Analyze) → Agent 2 (Strategy) ↔ Feedback Loop
                                          ↓
                                  Agent 3 (Generate)
                                          ↓
                                  Jinja2 Renderer
                                          ↓
                                    HTML + Markdown
```

**Key Principles:**
- LLMs for intelligence, templates for consistency
- Separation of content (Agent 3) and presentation (Renderer)
- Type-safe data flow with Pydantic models
- Deterministic output via Jinja2

## Configuration

### Environment Variables

Create `presentation/api/.env`:
```bash
OPENAI_API_KEY=sk-...
TEST_MODE=false
DEFAULT_MODEL=gpt-4o
```

### Project Configuration

Edit `presentation/projects.json` to add new projects or themes.

## Development

### Adding a New Project

1. Create directory: `presentation/projects/my-project/`
2. Add structure:
   ```
   my-project/
   ├── html/
   ├── markdown/
   │   ├── input/
   │   └── optimized/
   ├── images/uploads/
   └── styles/
       └── github/
           ├── design-guide.json
           ├── style.css
           └── variables.css
   ```
3. Update `projects.json`

### Adding a New Component Type

1. Create template: `presentation/templates/components/my-component.html.j2`
2. Update `agents/schemas.py` with component model
3. Add to `renderers/component_renderer.py`
4. Update `design-guide.json`
5. Write tests in `tests/`

See [presentation/api/README.md](presentation/api/README.md) for details.

## Troubleshooting

### Common Issues

**1. OPENAI_API_KEY not found**
```bash
cp presentation/api/.env.example presentation/api/.env
# Then edit .env
```

**2. Template not found**
- Templates are in `presentation/templates/`, NOT `presentation/api/templates/`

**3. Module import errors**
- Ensure `__init__.py` exists in `api/schemas/` and `api/tests/`
- Run commands from `presentation/` directory

**4. Tests failing**
- Use `export TEST_MODE=true` for development
- See [TESTING.md](TESTING.md) for detailed troubleshooting

## Performance

### V1 vs V2 Comparison

| Metric | V1 (Deprecated) | V2 (Current) |
|--------|----------------|--------------|
| Single Slide | ~4-6s | ~3-5s |
| 3 Variants | ~15-20s | ~3-5s |
| API Calls | 1-4 | 1 |
| Token Cost | 4x | 1x |
| Consistency | Variable | Deterministic |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

## License

See LICENSE file for details.

## Support

- **Documentation:** Start with [CLAUDE.md](CLAUDE.md)
- **Issues:** Open a GitHub issue with reproduction steps
- **Testing Help:** See [TESTING.md](TESTING.md)
- **API Questions:** Check [presentation/api/README.md](presentation/api/README.md)

## Credits

Built with:
- FastAPI
- OpenAI GPT-4o/GPT-5
- Jinja2
- Pydantic

---

**Note:** The legacy Word-to-Markdown converter has been archived to `archive/legacy-scripts/`. This project now focuses on the V2 AI-powered slide generation system.

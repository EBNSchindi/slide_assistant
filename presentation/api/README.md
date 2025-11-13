# Slides Helper AI API

FastAPI-based backend for AI-powered presentation slide content generation.

## Features

- **Multi-Agent Architecture**: Content Analyzer → Presentation Strategist → Content Generator
- **OpenAI Integration**: Uses GPT-4o for intelligent content generation
- **Style-Aware Generation**: Respects project design systems and style guides
- **Markdown + HTML Output**: Generates both source and rendered formats
- **RESTful API**: Clean, well-documented endpoints

## Architecture

```
User Input (Text/Markdown/Stichpunkte)
          ↓
Content Analyzer Agent
  - Identifies content type
  - Extracts key messages
  - Detects formatting preferences
          ↓
Presentation Strategist Agent
  - Analyzes project style guide
  - Recommends optimal components
  - Plans layout and arrangement
          ↓
Content Generator Agent
  - Generates markdown (optimized/)
  - Generates HTML with CSS classes
  - Respects design system colors/fonts
          ↓
File Service
  - Saves files to project structure
  - Creates backups
  - Manages versions
```

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

1. Create virtual environment:
```bash
cd presentation/api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Server

From the `presentation` directory:

```bash
source api/venv/bin/activate
python3 run_api.py
```

Server will start at `http://localhost:8001`

Check health: `curl http://localhost:8001/health`

## API Endpoints

### Projects

- `GET /api/projects` - List all projects
- `GET /api/projects/{name}` - Get project info
- `GET /api/projects/{name}/style` - Get project style guide
- `GET /api/projects/{name}/slides` - Get all slides
- `POST /api/projects` - Create new project

### Content Generation

- `POST /api/generate` - Generate new content
- `POST /api/regenerate` - Regenerate slide with feedback

### Examples

**Generate new content:**
```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "user_input": "Our team: 5 experts, 20 years experience, Berlin & Munich",
    "slide_title": "Team"
  }'
```

**List projects:**
```bash
curl http://localhost:8001/api/projects
```

## Configuration

### `.env` Variables

```
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=gpt-4o
HOST=localhost
PORT=8001
```

### Project Structure

Each project should have:
```
projects/project-name/
├── markdown/
│   ├── input/       # Full pitch decks
│   └── optimized/   # Individual slides (generated)
├── html/            # Generated HTML (generated)
└── styles/
    ├── github/
    │   ├── style.css
    │   ├── variables.css
    │   └── design-guide.md
    └── [other themes]
```

## Development

### File Structure

```
api/
├── main.py                 # FastAPI app
├── config.py              # Configuration
├── models/
│   ├── requests.py        # Request schemas
│   └── responses.py       # Response schemas
├── agents/
│   ├── content_analyzer.py
│   ├── presentation_strategist.py
│   ├── content_generator.py
│   └── orchestrator.py
└── services/
    ├── style_parser.py
    ├── file_service.py
    └── project_service.py
```

### Adding New Agents

1. Create agent file in `agents/`
2. Inherit from OpenAI API
3. Define system prompt
4. Add to `orchestrator.py`

### Testing

Manual testing with cURL:
```bash
# Health check
curl http://localhost:8001/health

# List projects
curl http://localhost:8001/api/projects

# Generate content
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Frontend Integration

The AI Editor UI is in `ai-editor.html`:
- Chat interface for content input
- Live preview of generated slides
- Project and style selection
- Regeneration with feedback

Open in browser: `file:///path/to/ai-editor.html` (works offline for UI, needs server for generation)

## Notes

- API Key is required for content generation
- Large inputs may take 30+ seconds (depends on OpenAI API)
- Generated files are saved to project structure automatically
- Backups are created before regeneration
- All file paths are relative to project root

## Future Enhancements

- [ ] Anthropic Claude API support
- [ ] Local LLM fallback (Ollama)
- [ ] Batch slide generation
- [ ] Content versioning with git integration
- [ ] WebSocket for streaming responses
- [ ] Database for project metadata

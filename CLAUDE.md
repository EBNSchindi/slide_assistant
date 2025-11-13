# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **slides helper** system with three main components:
1. **Word-to-Markdown converter** - Converts .docx files to Markdown format
2. **Presentation system** - Converts Markdown pitch decks into component-based HTML presentations for screenshots
3. **Project Management GUI** - Web-based interface for creating, renaming, and deleting presentation projects

## Project Structure

```
slides_helper/
├── convert_word_to_markdown.py          # Word to Markdown converter
├── presentation/                         # Presentation system
│   ├── component-viewer.html            # Main viewer tool
│   ├── project-manager.html             # Project management GUI
│   ├── project_manager_api.py           # REST API for project management
│   ├── markdown-to-components.py        # Markdown to HTML converter
│   ├── projects.json                    # Project configuration
│   ├── README-PROJEKTVERWALTUNG.md      # Project management documentation
│   └── projects/                        # Project workspace
│       └── beispiel-projekt/            # Example project
│           ├── html/                    # Generated HTML slides
│           ├── markdown/                # Markdown sources
│           │   ├── input/               # Original markdown
│           │   └── optimized/           # Per-slide optimized markdown
│           └── styles/                  # Style variations (github, modern, minimal)
└── requirements.txt                     # Python dependencies (python-docx, flask, flask-cors)
```

## Key Architecture

### 1. Word-to-Markdown Converter (`convert_word_to_markdown.py`)

**Purpose:** Preserves exact word-for-word content from .docx files while converting to Markdown.

**Key Features:**
- Maintains formatting: bold, italic, underline, hyperlinks
- Handles headings (Heading 1-6 → `#` syntax)
- Converts bullet lists and numbered lists
- Converts tables to Markdown tables
- Processes document elements in correct order (paragraphs and tables)

**Usage:**
```bash
# Single file
python convert_word_to_markdown.py dokument.docx [ausgabe.md]

# Batch conversion
python convert_word_to_markdown.py --folder ./documents
```

### 2. Presentation System

**Purpose:** Converts Markdown pitch decks into screenshot-ready HTML components for PowerPoint/Keynote.

**Architecture:**
- **Input:** Markdown files with H1 sections (slides) and H2 sections (components)
- **Processing:** Either via LLM (Claude/GPT) or Python script
- **Output:** Individual HTML files with styled components
- **Viewing:** `component-viewer.html` with dynamic style switching

**Component Types:**
- `stat-grid` - Statistics cards (numbers + labels)
- `bullet-list` - Formatted bullet lists
- `quote` - Highlighted quotes
- `text` - Regular paragraphs with formatting

**Workflow:**
```
Markdown (H1 = slide, H2 = component)
  → LLM conversion (LLM-PROMPT.md) OR Python script
  → HTML files (projects/{name}/html/)
  → View in component-viewer.html
  → Screenshot individual components
  → Insert into PowerPoint/Keynote
```

### 3. Projects System

**Configuration:** `projects.json` defines project structure and available styles.

Each project has:
- Multiple markdown sources (input + optimized per slide)
- Generated HTML components
- Style variations (GitHub Design, Modern, Minimal)

**Dynamic Style Loading:** The viewer can switch between style themes at runtime via dropdown.

### 4. Project Management System

**Purpose:** Provides a web-based GUI for managing presentation projects.

**Components:**
- **Backend API:** `project_manager_api.py` - Flask REST API
- **Frontend GUI:** `project-manager.html` - Web interface for project management
- **Integration:** Linked from `component-viewer.html` via "⚙️ Projekte" button

**Features:**
- **Create Projects:** Automatically generates proper directory structure with all required folders
- **Rename Projects:** Updates both display name and filesystem paths
- **Delete Projects:** Removes project directory and configuration (with confirmation)
- **Auto-Configuration:** New projects receive default styles (GitHub, Modern, Minimal)

**API Endpoints:**
```
GET    /api/projects         - List all projects
POST   /api/projects         - Create new project
PUT    /api/projects/<name>  - Rename project
DELETE /api/projects/<name>  - Delete project
```

**Usage:**
```bash
# Start API server
python3 presentation/project_manager_api.py

# In another terminal, start web server
python3 -m http.server 8000

# Open in browser
# http://localhost:8000/project-manager.html
```

**Generated Project Structure:**
```
projects/{project-name}/
├── html/                      # Generated HTML components
├── markdown/
│   ├── input/                 # Source markdown files
│   │   └── README.md          # Auto-generated guide
│   └── optimized/             # Per-slide optimized markdown
└── styles/
    ├── github/style.css       # Default GitHub theme
    ├── modern/style.css       # Modern theme
    └── minimal/style.css      # Minimal theme
```

For detailed usage instructions, see [README-PROJEKTVERWALTUNG.md](presentation/README-PROJEKTVERWALTUNG.md).

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or with virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Converting Documents
```bash
# Word to Markdown
python convert_word_to_markdown.py input.docx output.md
python convert_word_to_markdown.py --folder ./path/to/docs

# Markdown to HTML components
python presentation/markdown-to-components.py input.md presentation/output/
```

### Viewing Presentations
```bash
# Start local server (required for loading external HTML files)
cd presentation
python3 -m http.server 8000

# Open in browser
# http://localhost:8000/component-viewer.html
```

**Note:** Example files work without server (embedded), but custom files need the local server due to CORS restrictions.

### Working with the Viewer

The `component-viewer.html` tool:
- Loads HTML components from projects
- Provides style theme switching
- Allows width adjustment for screenshot optimization
- Uses `projects.json` to discover available projects and styles

## Important Technical Details

### Word Converter
- Uses `python-docx` library
- Extracts hyperlinks via XML relationships
- Handles both standard styles and custom formatting
- Preserves document element order by iterating through `doc.element.body`

### Markdown-to-Components Script
- Parses H1 as slide boundaries
- Parses H2 as component boundaries
- Auto-detects statistics (numbers with units like Mio, Mrd, %, €)
- Generates unique component IDs: `slide-{X}-comp-{Y}`
- Outputs complete HTML with embedded CSS

### LLM Integration
The system is designed for LLM-assisted conversion:
- `LLM-PROMPT.md` contains detailed prompt for Claude/ChatGPT
- LLM intelligently categorizes content into appropriate component types
- LLM provides better context understanding than regex parsing

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

## Common Gotchas

1. **CORS Issues:** Custom HTML files require local server. Use `python3 -m http.server 8000` in presentation directory.

2. **Component IDs:** Must follow format `slide-{X}-comp-{Y}` for proper viewer functionality.

3. **Style Paths:** Styles are relative to project path. Check `projects.json` for correct paths.

4. **Markdown Format:** H1 creates new slides, H2 creates components. Follow this strictly for proper parsing.

5. **Statistics Detection:** Regex looks for patterns like `\d+[.,\d]*\s*(Mio|Mrd|%|€|$|USD)`. Include units for auto-detection.

6. **Python Dependencies:** Only `python-docx>=1.1.0` required. Install via requirements.txt.

## Development Tips

- Test Word conversions with various document structures (tables, nested lists, hyperlinks)
- Use LLM conversion for intelligent component categorization
- Use Python script for batch processing or automated workflows
- Preview in viewer before taking screenshots
- Browser DevTools element inspector for pixel-perfect screenshots
- Keep component content focused (1 component = 1 idea)
